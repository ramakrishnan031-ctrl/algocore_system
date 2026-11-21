import re, sys, pathlib
P = pathlib.Path('/home/claude/a07/parts')
me = P / 'A07_STATUSES_PERSISTENCE_CONCURRENCY_AND_DUPLICATION_2026-11-21.md'
t = me.read_text(encoding='utf-8')
labels = ('FACT', 'UNKNOWN / NOT ESTABLISHED', 'INTERPRETATION', 'HISTORICAL', 'OPEN QUESTION')
# definitions: "- P09-Snnn LABEL" or "| P09-Snnn LABEL"
defs = re.findall(r'^(?:- |\| )P09-S(\d{3}) ([A-Z][A-Z /]+)', t, re.M)
nums = [int(n) for n, _ in defs]
ok = True
exp = list(range(1, max(nums) + 1))
if nums != exp:
    ok = False
    print('NUMBERING PROBLEM', sorted(set(exp) - set(nums)), [n for n in nums if nums.count(n) > 1])
else:
    print('NUMBERING OK', len(nums))
for n, lab in defs:
    if not lab.strip().startswith(labels):
        ok = False; print('LABEL?', n, lab)
# cited P09 ids defined
cited = set(int(x) for x in re.findall(r'P09-S(\d{3})', t))
missing = sorted(cited - set(nums))
print('P09 cited but undefined:', missing); ok &= not missing
# cited other-part statement ids exist
files = {f'P0{i}': None for i in range(1, 9)}
names = {'P01': 'PRIOR_TOPIC', 'P02': 'STRATEGY_CONTROL', 'P03': 'SECONDARY_SCREENER', 'P04': 'STEP_EXECUTOR', 'P05': 'QUALITY_SCORER', 'P06': 'ENTRY_GATE', 'P07': 'STRATEGY_SCRIPTS', 'P08': 'CONFIGURATION_KEYS'}
for part, key in names.items():
    fs = [f for f in P.glob('A07_*.md') if key in f.name]
    files[part] = fs[0].read_text(encoding='utf-8') if fs else None
bad = []
for part, num in set(re.findall(r'(P0[1-8])-S(\d{3})', t)):
    s = files.get(part)
    if s is None or not re.search(rf'(?:^|[-|] ){part}-S{num}\b', s, re.M):
        bad.append(f'{part}-S{num}')
print('other-part IDs not found as definitions:', sorted(bad)); ok &= not bad
for q in ('Q11', 'Q14', 'Q15', 'Q16', 'Q22', 'Q23', 'Q25'):
    if not re.search(rf'\({q}[,:]', t): ok = False; print('ANSWER MISSING', q)
for item in ('B-08', 'H-16', 'H-17', 'P-02', 'P-11', 'Q-22', 'U-24', 'U-25', 'FB-01', 'FB-02', 'FB-07', 'FB-14', 'WA-06', 'WA-07', 'EV-02', 'ET-06', 'TG14', 'RTR L130', 'RTR L147', 'RTR L144', 'RTR L205', 'RTR L214'):
    if item not in t.split('## 13.')[1].split('## 14.')[0]: ok = False; print('XREF MISSING', item)
print('APs', len(re.findall(r'^- P09-AP\d\d', t, re.M)), 'Us', len(re.findall(r'^- P09-U\d\d', t, re.M)), 'Rs', len(re.findall(r'^- P09-R\d', t, re.M)))
print('RESULT', 'PASS' if ok else 'FAIL')
