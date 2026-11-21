# P10 helper: self-check of the P10 file (numbering, labels, required question wording, cited part IDs exist).
import re, glob
p='/home/claude/a07/parts/A07_LEGACY_RECORDS_INTENT_SOURCES_AND_TESTS_2026-11-21.md'
t=open(p,encoding='utf-8').read()
ids=[int(x) for x in re.findall(r'^P10-S(\d{3})\. ', t, re.M)]
print('statements', len(ids), 'first', min(ids), 'last', max(ids), 'gaps', sorted(set(range(1,max(ids)+1))-set(ids)), 'dups', sorted({i for i in ids if ids.count(i)>1}))
labels=('FACT','HISTORICAL','INTERPRETATION','UNKNOWN / NOT ESTABLISHED','OPEN QUESTION')
bad=[m.group(1) for m in re.finditer(r'^P10-S(\d{3})\. (.{0,30})', t, re.M) if not m.group(2).startswith(labels)]
print('bad labels', bad)
for k in ('AP','U'):
    xs=[int(x) for x in re.findall(r'^- P10-%s(\d{2}) — '%k, t, re.M)]
    print(k, len(xs), 'gaps', sorted(set(range(1,max(xs)+1))-set(xs)))
    bl=[x for x in re.findall(r'^- P10-%s\d{2} — (.{0,30})'%k, t, re.M) if not x.startswith(labels)]
    print(k,'bad labels',bl)
print('R', re.findall(r'^- (P10-R\d+)', t, re.M))
q24='Which intended-behaviour sources exist (configuration, documents, comments, docstrings, names, tests, logs, historical records and Rama\'s statements)? Where sources conflict or intent is absent, preserve the conflict or mark UNKNOWN / NOT ESTABLISHED.'
q26='What is the complete inventory of A07-owned code, scripts, call sites, tests cited as evidence, dependencies and external interfaces at the baseline? Record exclusions and ownership reasons.'
print('Q24 verbatim', q24 in t, '| Q26 verbatim', q26 in t)
# cited peer IDs exist
peer=set()
for f in glob.glob('/home/claude/a07/parts/A07_*.md'):
    if f==p: continue
    peer|=set(re.findall(r'P0\d-(?:S\d{3}|AP\d{2}|U\d{2}|R\d)', open(f,encoding='utf-8').read()))
cited=set(re.findall(r'P0\d-(?:S\d{3}|AP\d{2}|U\d{2}|R\d)', t))
missing=sorted(c for c in cited if c not in peer)
print('peer IDs cited', len(cited), 'not found in peer files', missing)
