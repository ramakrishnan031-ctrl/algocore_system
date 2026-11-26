# H16 (assembly checker): independent completeness, count and citation checks of the corrected STUDY. Read-only.
import re, json, sys
W = '/home/claude/a08'
S = open(f'{W}/out/A08_STUDY_2026-11-26.md', encoding='utf-8').read()
idx = json.load(open(f'{W}/notes/ASSEMBLY_CHECKER_index.json', encoding='utf-8'))
P7 = open(f'{W}/parts/A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md', encoding='utf-8').read()
REG = '/home/claude/algocore_system/doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/'
fails = []
def ok(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (f'  [{detail}]' if detail and not cond else ''))
    if not cond: fails.append(name)
def sec(a, b):
    i = S.index(a); j = S.index(b, i + 1) if b else len(S); return S[i:j]
def has(text, tok):
    return re.search(r'(?<![A-Za-z0-9-])' + re.escape(tok) + r'(?![0-9A-Za-z])', text) is not None
s15_16 = sec('\n## 15. ', '\n## 17. ')
s13 = sec('\n## 13. ', '\n## 14. ')
# 1. every part AP / U / R ID (from my own index) in sections 15 or 16
part_ids = {k: v for k, v in idx.items() if re.match(r'P0[1-6]-(AP|U|R)\d+$', k)}
miss = [k for k in part_ids if not has(s15_16, k)]
ok(f'1a: every P01-P06 AP/U/R ID ({len(part_ids)}) appears in sections 15/16', not miss, str(miss))
p7ap = [k for k in idx if k.startswith('P07 AP-')]
miss = [k for k in p7ap if k not in s15_16]
ok(f'1b: P07 AP-01..AP-06 ({len(p7ap)}) appear in sections 15/16', not miss, str(miss))
p7u = [k for k, v in idx.items() if k.startswith('P07-S') and v['label'].startswith('UNKNOWN')]
miss = [k for k in p7u if not has(s15_16, k)]
ok(f'1c: P07 UNKNOWN statements ({len(p7u)}: {", ".join(sorted(p7u))}) appear in sections 15/16', not miss, str(miss))
from collections import Counter
cnt = Counter(re.sub(r'\d+$', '', k.split('-', 1)[1]) for k in part_ids)
ap = cnt['AP'] + len(p7ap); u = cnt['U'] + len(p7u); r = cnt['R']
ok(f'1d: part totals AP {ap}, U {u}, R {r} = 104, 61, 27', (ap, u, r) == (104, 61, 27))
# 2. section 13 coverage
d41 = open(REG + 'DECISION_REGISTER_2026-11-04.md', encoding='utf-8').read()
d41 = d41[d41.index('## D-41'):]
p4 = d41[d41.index('(P4)'):d41.index('(P5)')]
items = []
for grp in p4.split('the 16 Open Issues')[0].split('(each record')[1].split(':',1)[1].split(';'):
    m = re.match(r'\s*(A0\d) (.*)', grp.strip())
    if not m: continue
    topic, rest = m.group(1), re.sub(r'\)\s*and\s*$', '', m.group(2).strip()).rstrip(')').strip()
    for i in re.split(r', | and ', rest):
        i = i.strip().rstrip(')')
        r2 = re.match(r'([A-Z]{1,2}-)(\d+) to ([A-Z]{1,2}-)?(\d+)$', i)
        if r2: items += [f'{topic} {r2.group(1)}{n:02d}' for n in range(int(r2.group(2)), int(r2.group(4)) + 1)]
        elif i: items.append(f'{topic} {i}')
items = [i for i in items if re.match(r'A0\d [A-Z]{1,2}-?\d+[a-z]?$', i)]
s132 = sec('\n### 13.2 ', '\n### 13.3 ')
miss = [i for i in items if ('| ' + i + ' |') not in s132]
ok(f'2a: the 48 items of D-41 P4 ({len(items)}) each have a row in 13.2', len(items) == 48 and not miss, str(miss))
oirs = re.findall(r'A0\d-\d\d', p4.split('the 16 Open Issues')[1].split(')')[0])
s133 = sec('\n### 13.3 ', '\n### 13.4 ')
miss = [o for o in oirs if ('| ' + o + ' (L') not in s133]
ok(f'2b: the 16 open issues of D-41 P4 ({len(oirs)}) each have a row in 13.3', len(oirs) == 16 and not miss, str(miss))
recs = re.findall(r'(?m)^\| P07-S1(?:2[5-9]|3\d|40) HISTORICAL \(record\) \| (A0\d [A-Z]{1,2}-?\d+[a-z]?) ', P7)
s134 = sec('\n### 13.4 ', '\n### 13.5 ')
miss = [x for x in recs if ('| ' + x + ' (L') not in s134]
ok(f'2c: the 16 Owner-field records of P07 s5.5 ({len(recs)}) each have a row in 13.4', len(set(recs)) == 16 and not miss, str(miss))
s135 = sec('\n### 13.5 ', '\n### 13.6 ')
ok('2d: notes N1 to N6 each have a row in 13.5', all(('| N%d |' % n) in s135 for n in range(1, 7)))
s136 = sec('\n### 13.6 ', '\n## 14. ')
t175 = idx['P06-S175']['text']; t176 = idx['P06-S176']['text']
r175 = re.findall(r'(?m)^\| (A0\d [A-Z]{1,2}-?\d+[a-z]?) \(', t175)
r176 = re.findall(r'(A0\d [A-Z]{1,2}-\d+) \((?:MATCH row, )?L\d', t176)
miss = [x for x in r175 + r176 if ('| ' + x + ' (') not in s136]
ok(f'2e: the 43 records of P06-S175/S176 ({len(r175)} + {len(r176)}) each have a row in 13.6', len(r175) == 34 and len(r176) == 9 and not miss, str(miss))
five = ['A03 H-44', 'A03 U-59', 'A03 U-60', 'A01 C40', 'A02 K-32']
ok('2f: the 5 records of Claude\'s assignment decision and A06 PQ-06 have rows in 13.6', all(('| ' + x + ' |') in s136 for x in five + ['A06 PQ-06']))
# OIR status cells: the one text quoted in 13.3 equals every one of the 16 summary rows
oir = open(REG + 'OPEN_ISSUES_REGISTER_2026-11-05.md', encoding='utf-8').read().split('\n')
quoted = re.search(r'the same text, copied unchanged: "([^"]+)"', s133).group(1)
rows = {l.split('|')[1].strip(): l.strip().strip('|').split('|')[-1].strip() for l in oir if re.match(r'^\| A0\d-\d\d \|', l)}
bad = [o for o in oirs if rows.get(o) != quoted]
ok('2g: the Status text quoted in 13.3 equals each of the 16 summary rows of the Open Issues Register', not bad, str(bad))
# 3. direction requirements mapped in 1.9
s19 = sec('\n### 1.9 ', '\n### 1.10 ')
reqs = ['A.1', 'A.2', 'A.3', 'A.4', 'A.5', 'A.6', 'A.7', 'B']
miss = [q for q in reqs if not re.search(r'(?m)^\| ' + re.escape(q) + r' \|', s19)]
s5rows = re.findall(r'(?m)^\| 5 \| ([^|]+) \|', s19)
ok(f'3: 1.9 maps A.1 to A.7, B and section 5 ({len(s5rows)} rows: 48 items and 16 issues, HA-06, unsorted rows, from_kite, the corporate-action check, L139 vs L141)', not miss and len(s5rows) == 6, str(miss))
# 4. counts stated in the STUDY, re-counted
n_ap = len(re.findall(r'(?m)^- \*\*A08-AP-\d\d\*\*', S)); n_u = len(re.findall(r'(?m)^- \*\*A08-U-\d\d\*\*', S)); n_q = len(re.findall(r'(?m)^- \*\*A08-Q-\d\d\*\*', S))
ok(f'4a: consolidated entries {n_ap} AP, {n_u} U, {n_q} Q = 92, 40, 25', (n_ap, n_u, n_q) == (92, 40, 25))
ok('4b: section 2 states "92 points for the AUDIT, 40 unknown items and 25 draft questions ... from 104, 61 and 27"', 'The STUDY carries 92 points for the AUDIT, 40 unknown items and 25 draft questions for Rama, from 104, 61 and 27 in the parts' in S)
nst = sum(1 for k in idx if re.match(r'P0\d-S\d{3}$', k))
ok(f'4c: statements in the seven parts = {nst} (STUDY 17.2: 1,152)', nst == 1152 and '1,152 statements' in S)
per = Counter(k[:3] for k in idx if re.match(r'P0\d-S\d{3}$', k))
s172 = sec('\n### 17.2 ', None)
bad = [p for p, n in per.items() if f'{p}-S001 to {p}-S{n:03d} ({n})' not in s172]
ok('4d: 17.2 per-part statement ranges and counts', not bad, str(bad))
for p in ['P01', 'P02', 'P03', 'P04', 'P05', 'P06']:
    a = sum(1 for k in idx if k.startswith(p + '-AP')); uu = sum(1 for k in idx if k.startswith(p + '-U')); rr = sum(1 for k in idx if k.startswith(p + '-R'))
    ok(f'4e: 17.2 {p} {a} / {uu} / {rr}', re.search(rf'\({p}\) \| {p}-S001 to {p}-S\d+ \(\d+\) \| {a} / {uu} / {rr}\b', s172) is not None)
# merges: 104 - 12 = 92; 61 - 21 = 40
heads = re.findall(r'(?m)^- \*\*(A08-(?:AP|U)-\d\d)\*\* \(([^)]*)\)', S)
src_ap = sum(len(re.findall(r'P0\d-AP\d\d|P07 AP-\d\d', h)) for c, h in heads if '-AP-' in c)
src_u = sum(len(re.findall(r'P0\d-U\d\d|P07-S\d{3}', h)) for c, h in heads if '-U-' in c)
ok(f'4f: the 92 points cite {src_ap} source points and the 40 unknowns {src_u} source unknowns (104, 61)', (src_ap, src_u) == (104, 61))
qheads = re.findall(r'(?m)^- \*\*A08-Q-\d\d\*\* \(([^)]*)\)', S)
rq = sum(len(re.findall(r'P0\d-R\d', h)) for h in qheads)
ok(f'4g: the 25 questions cite {rq} R IDs, + P06-R1 withdrawn = 27', rq == 26 and 'P06-R1' in sec('**Withdrawn (not to be put).**', '\n## 17. '))
ok('4h: 13.6 counts: 34 + 9 = 43; 48 records; 47 with a pointer; J-14 none', '34 + 9 = 43' in s136 and '47 of them carry a part pointer' in s136 and 'one, A03 J-14, has none' in s136)
s132rows = re.findall(r'(?m)^\| \d+ \| (A0\d) ', s132)
ok(f'4i: 13.2 counts per topic {dict(Counter(s132rows))}', dict(Counter(s132rows)) == {'A01': 5, 'A02': 7, 'A03': 9, 'A04': 4, 'A05': 11, 'A06': 8, 'A07': 4})
# 5. citations resolve
cited = set(re.findall(r'(?<![A-Za-z0-9])(P0[1-7]-(?:S\d{3}|AP\d\d|U\d\d|R\d|X\d\d))(?![0-9])', S))
bad = sorted(c for c in cited if c not in idx)
ok(f'5a: every cited part ID exists ({len(cited)} distinct)', not bad, str(bad))
for pre, n in (('A08-AP-', 92), ('A08-U-', 40), ('A08-Q-', 25)):
    refs = set(re.findall(re.escape(pre) + r'\d\d', S)); defs = [f'{pre}{i:02d}' for i in range(1, n + 1)]
    ok(f'5b: every {pre}nn reference resolves to a defined entry', refs <= set(defs), str(sorted(refs - set(defs))))
d = re.findall(r'(?m)^- \*\*(A08-(?:AP|U|Q)-\d\d)\*\*', S)
ok('5c: consolidated IDs defined once each, in order, with the A08- prefix', d == [f'A08-AP-{i:02d}' for i in range(1, 93)] + [f'A08-U-{i:02d}' for i in range(1, 41)] + [f'A08-Q-{i:02d}' for i in range(1, 26)])
bare = [m.group(0) for m in re.finditer(r'(?<![A-Za-z0-9-])AP-\d\d(?![0-9])', S) if not S[max(0, m.start()-4):m.start()] in ('A08-', 'P07 ') and not re.search(r"P07(?: AP-0\d,|'s own| AP-01 to)|\(P07\) \|[^|]*\| \d \(", S[max(0, m.start()-60):m.start()])]
ok('5d: no point number "AP-nn" written without its prefix (A08- for the STUDY, "P07 " for P07\'s own)', not bare, str(sorted(set(bare))))
# 6. hygiene
ok('6a: no absolute path', re.search(r'/home/|/Users/|/root/|[A-Za-z]:\\\\', S) is None)
ok('6b: sections 1 to 17 present in order', re.findall(r'(?m)^## (\d+)\. ', S) == [str(i) for i in range(1, 18)])
labels_kd = [m.start() for m in re.finditer(r'(?m)^- KNOWN DEFECT|\bKNOWN DEFECT:', S)]
ok('6c: KNOWN DEFECT never used as a label', not labels_kd)
print('RESULT:', 'ALL PASS' if not fails else f'{len(fails)} FAIL: {fails}')
