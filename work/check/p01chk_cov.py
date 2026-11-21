# P01 checker: coverage script (read-only; prints results)
import re, sys
sys.path.insert(0,'/home/claude/a07/check')
from p01chk_afr import ITEMS, cells
P='/home/claude/a07/parts/A07_PRIOR_TOPIC_HANDOFFS_2026-11-21.md'
B='/home/claude/a07/briefs/A07_PART_BRIEFS.md'
T=open(P,encoding='utf-8').read(); L=T.split('\n')
ok=True
def chk(c,msg):
    global ok
    print(('PASS ' if c else 'FAIL ')+msg); ok&=bool(c)
# 1. the 51 rows of section 2
rows={}
for l in L:
    if re.match(r'^\| P01-S\d{3} HISTORICAL \(record\) \| A0\d \|',l):
        c=cells(l); rows.setdefault((c[1],c[2]),[]).append(c[0].split()[0])
for t,ids in ITEMS.items():
    present=[i for i in ids.split() if (t,i) in rows]
    chk(len(present)==len(ids.split()), f'{t}: {len(present)} of {len(ids.split())} items have a row: {" ".join(present)}')
chk(sum(len(v) for v in rows.values())==51 and all(len(v)==1 for v in rows.values()), f'51 rows in all, each ID once ({sum(len(v) for v in rows.values())})')
print('counts by topic:', ', '.join(f'{t} {sum(1 for (a,b) in rows if a==t)}' for t in ITEMS))
# 2. the 10 register entries of section 3
oir=['A02-03','A03-10','A03-11','A03-36','A03-37','A05-01','A05-25','A06-02','A06-08','A06-12']
got=[e for e in oir if re.search(r'^\| P01-S\d{3} HISTORICAL \(record\) \| '+re.escape(e)+r',',T,re.M)]
chk(len(got)==10, f'section 3: {len(got)} of 10 register entries have a row: {" ".join(got)}')
# 3. the section 2.8 table covers all 51
i=T.index('### 2.8'); j=T.index('## 3. ')
tab=T[i:j]; cover={}
for l in tab.split('\n'):
    m=re.match(r'^\| (P0\d|P10) \| (.*) \| (\d+) \|$',l)
    if not m: continue
    part,body,n=m.group(1),m.group(2),int(m.group(3)); found=[]
    cur=None
    for tok in re.split(r'[;,]',body):
        tok=tok.strip()
        mm=re.match(r'^(A0\d) (.+)$',tok)
        if mm: cur=mm.group(1); tok=mm.group(2)
        mid=re.match(r'^([A-Z]{1,2}-?\d+)',tok)
        if cur and mid and mid.group(1) in ITEMS[cur].split(): found.append((cur,mid.group(1)))
    chk(len(found)==n, f'2.8 row {part}: {len(found)} items listed, count cell {n}')
    for f in found: cover.setdefault(f,[]).append(part)
missing=[f'{t} {i}' for t,ids in ITEMS.items() for i in ids.split() if (t,i) not in cover]
chk(not missing, f'2.8: every one of the 51 has at least one part (missing: {missing})')
# 4. statement numbering and labels
ids=[int(x) for x in re.findall(r'(?m)^(?:\| )?P01-S(\d{3})[. ]',T)]
chk(sorted(set(ids))==list(range(1,max(ids)+1)) and len(ids)==len(set(ids)), f'statements P01-S001 to P01-S{max(ids):03d}, each once, no gap ({len(ids)})')
LAB=('FACT','UNKNOWN / NOT ESTABLISHED','INTERPRETATION','HISTORICAL','OPEN QUESTION')
bad=[]
for m in re.finditer(r'(?m)^(?:\| )?(P01-S\d{3})[. ] ?(.{0,40})',T):
    s=m.group(2).lstrip('. ')
    if not s.startswith(LAB) or re.match(r'^(FACT|HISTORICAL \(record\)|INTERPRETATION|OPEN QUESTION)[^:|]*\) and ',s) or re.match(r'^[A-Z /]+ and [A-Z]',s): bad.append(m.group(1))
chk(not bad, f'every statement starts with one label (bad: {bad})')
# 5. focused questions assigned to P01
bt=open(B,encoding='utf-8').read(); p01=bt[bt.index('## P01'):bt.index('## P02')]
chk(not re.search(r'\bQ\d',p01), 'the P01 brief assigns no focused question (Q1 to Q26): coverage test (b) not applicable')
print('RESULT:', 'ALL PASS' if ok else 'FAILURES')
