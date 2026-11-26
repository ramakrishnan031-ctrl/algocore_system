"""P07 checker coverage script (A08 STUDY, part P07). Read-only.

Reads the P07 part file and the approved records at algocore_system commit 52cc811
(git show only). Writes nothing. Run: python3 -I p07chk_cov.py
"""
import re
import subprocess
import sys
from collections import Counter

PART = '/home/claude/a08/parts/A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md'
REPO = '/home/claude/algocore_system'
REV = '52cc811'
TW = 'doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/'
REG = 'doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/'
DIRS = {
    'A01': 'A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/A01_',
    'A02': 'A02_CONFIGURATION_AND_EFFECTIVE_SETTINGS/A02_',
    'A03': 'A03_DATABASE_PERSISTENCE_MIGRATIONS_AND_BACKUPS/A03_',
    'A04': 'A04_BROKER_INTERFACE_AUTHENTICATION_AND_BROKER_STATE/A04_',
    'A05': 'A05_MARKET_DATA_INSTRUMENTS_AND_EXTERNAL_REFERENCE_DATA/A05_',
    'A06': 'A06_SIGNAL_INTAKE_AND_WEBHOOK_LIFECYCLE/A06_',
    'A07': 'A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/A07_',
}
RTR = {'A01': 'RECONCILED_TOPIC_RECORD_2026-11-06.md', 'A02': 'RECONCILED_TOPIC_RECORD_2026-11-09.md',
       'A03': 'RECONCILED_TOPIC_RECORD_2026-11-11.md', 'A04': 'RECONCILED_TOPIC_RECORD_2026-11-14.md',
       'A05': 'RECONCILED_TOPIC_RECORD_2026-11-17.md', 'A06': 'RECONCILED_TOPIC_RECORD_2026-11-20.md',
       'A07': 'RECONCILED_TOPIC_RECORD_2026-11-25.md'}
AUD = {'A01': 'AUDIT_2026-11-05.md', 'A02': 'AUDIT_2026-11-08.md', 'A03': 'AUDIT_2026-11-10.md',
       'A04': 'AUDIT_2026-11-13.md', 'A05': 'AUDIT_2026-11-15.md', 'A06': 'AUDIT_2026-11-18.md',
       'A07': 'AUDIT_2026-11-24.md'}
LABELS = ('FACT', 'HISTORICAL', 'INTERPRETATION', 'UNKNOWN / NOT ESTABLISHED', 'OPEN QUESTION')
IDRX = re.compile(r'\b(?:[A-Z]{1,2}-\d{2}|C\d{2}[ab]?)\b')
fails = []


def show(path):
    return subprocess.run(['git', '-C', REPO, 'show', REV + ':' + path],
                          capture_output=True, text=True, check=True).stdout.splitlines()


def cells(line):
    out, cur, tick = [], '', False
    for ch in line.strip():
        if ch == '`':
            tick = not tick
        if ch == '|' and not tick:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out[1:-1]


def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)


T = open(PART, encoding='utf-8').read().splitlines()
body_end = next((i for i, l in enumerate(T) if l.startswith('## Check log')), len(T))
B = T[:body_end]

# 1. the 48 items: records (RTR A08 rows) against the part's section 3 rows
want48 = {}
for t in DIRS:
    rows = [l for l in show(TW + DIRS[t] + RTR[t]) if re.match(r'^\| *A08 *\|', l)]
    check(len(rows) == 1, f'{t} RTR has one A08 row')
    want48[t] = IDRX.findall(rows[0].split('|')[2])
part48 = {}
for l in B:
    m = re.match(r'^\| P07-S(\d{3}) ', l)
    if m and 18 <= int(m.group(1)) <= 65:
        c = cells(l)
        part48.setdefault(c[1], []).append(int(m.group(1)))
all48 = [x for v in want48.values() for x in v]
check(len(all48) == 48 and len(set(all48)) == 48, f'48 distinct IDs in the seven RTR A08 rows ({len(all48)})')
check(sorted(part48) == sorted(all48), 'section 3 has a row for every one of the 48 and no other')
check(all(len(v) == 1 for v in part48.values()), 'each of the 48 has exactly one section 3 row')
print('counts by topic:', ', '.join(f'{t} {len(v)}' for t, v in want48.items()))

# 2. the 16 Open Issues Register entries that name A08
oir = show(REG + 'OPEN_ISSUES_REGISTER_2026-11-05.md')
heads = [i for i, l in enumerate(oir) if re.match(r'^### A0\d-\d{2}\b', l)]
want16 = []
for h in heads:
    j = h + 1
    while j < len(oir) and not re.match(r'^#{2,3} ', oir[j]):
        j += 1
    if any(re.search(r'\bA08\b', x) for x in oir[h:j]):
        want16.append(re.match(r'^### (A0\d-\d{2})', oir[h]).group(1))
part16 = []
for l in B:
    m = re.match(r'^\| P07-S(\d{3}) ', l)
    if m and 70 <= int(m.group(1)) <= 85:
        part16.append(re.match(r'(A0\d-\d{2})', cells(l)[1]).group(1))
check(len(heads) == 261, f'Open Issues Register has 261 entries ({len(heads)})')
check(want16 == part16, f'section 4 rows equal the {len(want16)} register entries naming A08, in order')

# 3. the 16 records whose Owner field names A08 outside the 48 (wrapped field lines joined)
HEAD = re.compile(r'^(#{3,6}) ([A-Z]{1,3}-\d{2}[a-z]?|C\d{2}[a-z]?)\b')
want_rec = []
for t in DIRS:
    L = show(TW + DIRS[t] + AUD[t])
    for i, l in enumerate(L):
        if re.match(r'^\s*(?:[-*] )?\*\*Owners?\b[^*]*\*\*', l):
            txt, j = l, i + 1
            while j < len(L) and L[j].startswith('  ') and not L[j].lstrip().startswith('- **'):
                txt += ' ' + L[j].strip()
                j += 1
            if re.search(r'\bA08\b', txt):
                k = i
                while k >= 0 and not HEAD.match(L[k]):
                    k -= 1
                rid = HEAD.match(L[k]).group(2)
                if rid not in all48:
                    want_rec.append((t, rid))
s097 = []
in54 = False
for l in B:
    if l.startswith('### 5.4'):
        in54 = True
    elif l.startswith('### 5.5'):
        in54 = False
    if in54 and re.match(r'^\| A0\d \| ', l):
        c = cells(l)
        s097.append((c[0], c[1].split(' ')[0]))
s55 = []
for l in B:
    m = re.match(r'^\| P07-S(\d{3}) ', l)
    if m and 125 <= int(m.group(1)) <= 140:
        c = cells(l)
        s55.append(tuple(c[1].split(' ')[:2]))
check(len(want_rec) == 16, f'16 AUDIT records outside the 48 name A08 in their Owner field ({len(want_rec)})')
check(s097 == want_rec, 'section 5.4 table lists exactly those 16, in order')
check(s55 == want_rec, 'section 5.5 rows P07-S125 to P07-S140 list exactly those 16, in order')

# 4. the prose notes: RTR section 15 / 15.2 lines naming A08, other than the A08 rows
want_notes = []
for t in DIRS:
    L = show(TW + DIRS[t] + RTR[t])
    sec = ''
    for i, l in enumerate(L, 1):
        m = re.match(r'^#{2,4} ([0-9]+(?:\.[0-9]+)?)[. ]', l)
        if m:
            sec = m.group(1)
        if sec in ('15', '15.2') and re.search(r'\bA08\b', l) and not re.match(r'^\| *A08 *\|', l):
            want_notes.append(f'{t} RTR L{i}')
notes = {}
for l in B:
    m = re.match(r'^\| P07-S(\d{3}) [A-Z]+ \(record\) \| (N\d) \| ([^|]+)\|', l)
    if m:
        notes[m.group(2)] = re.match(r'(A0\d RTR L\d+)', m.group(3).strip()).group(1)
check(sorted(notes.values()) == sorted(want_notes), f'notes N1 to N6 cover the {len(want_notes)} prose lines {want_notes}')

# 5. the assignment table against the Part cells
prim, sec_ = {}, {}
for l in B:
    m = re.match(r'^\| P07-S(\d{3}) ', l)
    if not m:
        continue
    n = int(m.group(1))
    c = cells(l)
    if 18 <= n <= 65:
        key = c[1]
    elif 70 <= n <= 85:
        key = re.match(r'(A0\d-\d{2})', c[1]).group(1)
    elif 125 <= n <= 140:
        key = 'rec ' + c[1].split(' ')[1]
    else:
        continue
    part = c[-1]
    prim[key] = re.match(r'(P0\d|none)', part).group(1)
    sec_[key] = re.findall(r'P0\d', part.split(';', 1)[1]) if ';' in part else []
check(len(prim) == 80, f'80 assigned rows (48 + 16 + 16): {len(prim)}')
check(all(p in ('P01', 'P02', 'P03', 'P04', 'P05', 'P06') for p in prim.values()), 'every row has one primary part P01 to P06')
tab = {}
for l in B:
    if re.match(r'^\| (P0[1-6]|Total) \| ', l):
        c = cells(l)
        tab[c[0]] = c
for p in ('P01', 'P02', 'P03', 'P04', 'P05', 'P06'):
    c = tab[p]
    items = [k for k in prim if prim[k] == p and k in all48]
    iss = [k for k in prim if prim[k] == p and re.match(r'A0\d-\d{2}$', k)]
    recs = [k for k in prim if prim[k] == p and k.startswith('rec ')]
    t_items = set(IDRX.findall(c[1])) if c[1] != 'none' else set()
    t_iss = set(re.findall(r'A0\d-\d{2}', c[2]))
    t_recs = set('rec ' + x for x in IDRX.findall(c[3]))
    cnt = re.match(r'(\d+) \+ (\d+) \+ (\d+) = (\d+)', c[5])
    ok = (t_items == set(items) and t_iss == set(iss) and t_recs == set(recs) and cnt and
          [int(x) for x in cnt.groups()] == [len(items), len(iss), len(recs), len(items) + len(iss) + len(recs)])
    secs = sorted(k for k in prim if p in sec_[k])
    t_sec = set(IDRX.findall(c[6])) | set(re.findall(r'A0\d-\d{2}', c[6]))
    want_sec = set(k.replace('rec ', '') for k in secs)
    check(ok, f'{p}: primary {len(items)} items + {len(iss)} issues + {len(recs)} records = {len(items) + len(iss) + len(recs)}, table cells agree')
    check(want_sec == t_sec, f'{p}: secondary cell equals the secondary assignments of the Part cells ({len(want_sec)})')
tot = tab['Total']
check(tot[1] == '48' and tot[2] == '16' and tot[3] == '16' and tot[5] == '80', 'Total row: 48, 16, 16, 80')
c = Counter(prim.values())
print('primary counts:', ', '.join(f'{p} {c[p]}' for p in sorted(c)))

# 6. statements: each ID once, no gap; one leading label; no KNOWN DEFECT label
ids = []
bad = []
for l in B:
    for m in re.finditer(r'(?:^|^\| )P07-S(\d{3})[. ] ?(.*)', l):
        ids.append(int(m.group(1)))
        rest = m.group(2).lstrip('. ')
        if not rest.startswith(LABELS):
            bad.append(m.group(1))
dup = [k for k, v in Counter(ids).items() if v > 1]
check(sorted(set(ids)) == list(range(1, max(ids) + 1)) and not dup,
      f'statements P07-S001 to P07-S{max(ids):03d}, each once, no gap ({len(ids)}; duplicates {dup})')
check(not bad, f'every statement starts with one label (bad: {bad})')
check(not any(re.match(r'^(?:\| )?P07-S\d{3}[. ] ?KNOWN DEFECT', l) for l in B), 'no statement is labelled KNOWN DEFECT')
print('RESULT:', 'ALL PASS' if not fails else f'{len(fails)} FAIL')
sys.exit(1 if fails else 0)
