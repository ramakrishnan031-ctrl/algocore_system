# A08 STUDY assembly coverage test (read-only; reads the STUDY and the seven checked parts; writes nothing).
import re, sys
W = '/home/claude/a08'
STUDY = W + '/out/A08_STUDY_2026-11-26.md'
PARTS = {'P01':'A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md','P02':'A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md',
 'P03':'A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md','P04':'A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md',
 'P05':'A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md','P06':'A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md',
 'P07':'A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md'}
S = open(STUDY, encoding='utf-8').read()
def section(text, start, stop):
    a = text.index(start); b = text.index(stop, a + 1) if stop else len(text); return text[a:b]
sec13 = section(S, '\n## 13. ', '\n## 14. ')
sec_15_16 = section(S, '\n## 15. ', '\n## 17. ')
P = {k: open(W + '/parts/' + v, encoding='utf-8').read() for k, v in PARTS.items()}
fails = 0
def check(name, ok, detail=''):
    global fails
    print(('PASS ' if ok else 'FAIL ') + name + (('  ' + detail) if detail else ''))
    if not ok: fails += 1
def has(text, token):
    return re.search(r'(?<![A-Za-z0-9-])' + re.escape(token) + r'(?![0-9A-Za-z])', text) is not None
# 1. every part AP/U/R ID in sections 15 or 16
tot = {'AP':0,'U':0,'R':0}
for p in ['P01','P02','P03','P04','P05','P06']:
    t = P[p]
    for kind in ['AP','U','R']:
        ids = sorted(set(re.findall(r'(?m)^- \*{0,2}(' + p + '-' + kind + r'\d+)\b', t)))
        tot[kind] += len(ids)
        missing = [i for i in ids if not has(sec_15_16, i)]
        check(f'{p} {kind}: {len(ids)} IDs in sections 15/16', not missing, f'missing {missing}' if missing else '')
p7ap = sorted(set(re.findall(r'(?m)^- \*\*(AP-\d+)\.', P['P07'])))
miss = [a for a in p7ap if ('P07 ' + a) not in sec_15_16]
tot['AP'] += len(p7ap); check(f'P07 AP: {len(p7ap)} IDs (as "P07 AP-nn") in sections 15/16', not miss, f'missing {miss}' if miss else '')
p7sec9 = section(P['P07'], '\n## 9. ', '\n## 10. ')
p7u = sorted(set(re.findall(r'(?m)^(P07-S\d{3})\. UNKNOWN', p7sec9)))
miss = [u for u in p7u if not has(sec_15_16, u)]
tot['U'] += len(p7u); check(f'P07 UNKNOWN statements: {len(p7u)} {p7u} in sections 15/16', not miss, f'missing {miss}' if miss else '')
p7q = section(P['P07'], '\n## 10. ', '\n## 11. ')
check('P07 questions: none (P07-S114) cited in section 16', has(sec_15_16, 'P07-S114'))
print(f'part totals: AP {tot["AP"]}, U {tot["U"]}, R {tot["R"]}')
# 2. section 13 coverage
topic_of = {}
items = []
for m in re.finditer(r'(?m)^### 3\.\d The \d+ (A0\d) items.*$', P['P07']):
    topic = m.group(1); start = m.end(); nxt = P['P07'].find('\n### ', start); block = P['P07'][start:nxt]
    for r in re.finditer(r'(?m)^\| (P07-S\d{3}) HISTORICAL \(record\) \| ([A-Z]{1,2}-?\d+[a-z]?) \|', block):
        items.append(topic + ' ' + r.group(2))
miss = [i for i in items if i not in sec13]
check(f'48 inherited items: {len(items)} found in P07 section 3, all in section 13', len(items) == 48 and not miss, f'missing {miss}' if miss else '')
oir = re.findall(r'(?m)^\| P07-S0(?:7\d|8[0-5]) HISTORICAL \(record\) \| (A0\d-\d\d) ', P['P07'])
miss = [i for i in oir if not has(sec13, i)]
check(f'16 open issues: {len(oir)} found in P07 section 4, all in section 13', len(set(oir)) == 16 and not miss, f'missing {miss}' if miss else '')
recs = re.findall(r'(?m)^\| P07-S1(?:2[5-9]|3\d|40) HISTORICAL \(record\) \| (A0\d [A-Z]{1,2}-?\d+[a-z]?) ', P['P07'])
sec_13_4 = section(S, '\n### 13.4 ', '\n### 13.5 ')
miss = [r for r in recs if r not in sec_13_4]
check(f'16 Owner-field records: {len(recs)} found in P07 section 5.5, all in section 13.4', len(set(recs)) == 16 and not miss, f'missing {miss}' if miss else '')
notes = ['N1','N2','N3','N4','N5','N6']
sec_13_5 = section(S, '\n### 13.5 ', '\n### 13.6 ')
miss = [n for n in notes if ('| ' + n + ' |') not in sec_13_5]
check('notes N1 to N6 in section 13.5', not miss, f'missing {miss}' if miss else '')
s_a = section(P['P06'], '- P06-S175 ', '- P06-S176 ')
r_a = re.findall(r'(?m)^\| (A0\d [A-Z]{1,2}-?\d+[a-z]?) \(', s_a)
s_b = re.search(r'(?m)^- P06-S176 .*$', P['P06']).group(0)
r_b = re.findall(r'(A0\d [A-Z]{1,2}-\d+) \((?:MATCH row, )?L\d', s_b)
sec_13_6 = section(S, '\n### 13.6 ', '\n## 14. ')
miss_a = [r for r in r_a if r not in sec_13_6]; miss_b = [r for r in r_b if r not in sec_13_6]
check(f'P06-S175 records: {len(r_a)} (expected 34), all in section 13.6', len(r_a) == 34 and not miss_a, f'missing {miss_a}' if miss_a else '')
check(f'P06-S176 records: {len(r_b)} (expected 9) {r_b}, all in section 13.6', len(r_b) == 9 and not miss_b, f'missing {miss_b}' if miss_b else '')
five = ['A03 H-44','A03 U-59','A03 U-60','A01 C40','A02 K-32']
miss = [r for r in five if r not in sec_13_6]
check('the 5 records of P06-S169 to P06-S173 in section 13.6', not miss, f'missing {miss}' if miss else '')
check('A06 PQ-06 (P06-S189) in section 13.6', 'A06 PQ-06' in sec_13_6)
# 3. consolidated numbering defined once each, references resolve
for pre, n in [('A08-AP-', 92), ('A08-U-', 40), ('A08-Q-', 25)]:
    defs = re.findall(r'(?m)^- \*\*(' + re.escape(pre) + r'\d\d)\*\*', S)
    exp = [f'{pre}{i:02d}' for i in range(1, n + 1)]
    check(f'{pre}01 to {pre}{n:02d} each defined once, in order', defs == exp, f'got {len(defs)}')
    refs = set(re.findall(re.escape(pre) + r'\d\d', S))
    bad = sorted(r for r in refs if r not in exp)
    check(f'every {pre}nn reference resolves', not bad, f'unresolved {bad}' if bad else '')
# 4. every part ID cited in the STUDY exists in its part
defined = {}
for p, t in P.items():
    defined[p] = set(re.findall(r'(?m)^(?:- |\| )?\**(' + p + r'-S\d{3})\**[ .|]', t))
    for kind in ['AP','U','R','X']:
        defined[p] |= set(re.findall(r'(?m)^- \*{0,2}(' + p + '-' + kind + r'\d+)\b', t))
cited = set(re.findall(r'(?<![A-Za-z0-9])(P0[1-7]-(?:S\d{3}|AP\d+|U\d+|R\d+|X\d+))(?![0-9])', S))
bad = sorted(c for c in cited if c not in defined[c[:3]])
check(f'every cited part ID exists in its part ({len(cited)} distinct IDs cited)', not bad, f'unresolved {bad}' if bad else '')
p7apcited = set(re.findall(r'P07 (AP-\d\d)', S)); bad = sorted(a for a in p7apcited if a not in p7ap)
check('every "P07 AP-nn" citation exists', not bad, str(bad) if bad else '')
# 5. hygiene
check('no absolute path in the STUDY', re.search(r'/home/|/Users/|[A-Za-z]:\\\\', S) is None)
check('no [FILL- placeholder left', '[FILL-' not in S)
kd = [m.start() for m in re.finditer('KNOWN DEFECT', S)]
ctx = [S[max(0, i-60):i+40].replace('\n', ' ') for i in kd]
print(f'INFO "KNOWN DEFECT" occurrences: {len(kd)}')
for c in ctx: print('   ...' + c + '...')
heads = re.findall(r'(?m)^## (\d+)\. ', S)
check('sections 1 to 17 present in order', heads == [str(i) for i in range(1, 18)], str(heads))
print('RESULT: ' + ('ALL PASS' if fails == 0 else f'{fails} FAIL'))
sys.exit(1 if fails else 0)
