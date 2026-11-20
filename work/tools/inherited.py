import re, json
AFR='doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md'
items={'A01':'C11 C14 C15 C20 B-28 B-08','A02':'V-06 V-23 T-14 T-20 F-11 K-05 K-27',
'A03':'D-05 D-09 H-16 H-17 H-50 P-02 P-11 Q-11 Q-12 Q-22 Q-45 U-24 U-25 E-08',
'A04':'OA-22 RD-12 RL-11 PR-23 CG-05','A05':'CM-07 CM-22 FB-01 FB-02 FB-07 FB-14',
'A06':'WA-06 WA-07 PQ-02 PQ-08 PQ-13 PQ-14 PQ-15 EV-02 EV-11 EV-19 ET-06 ET-13 XA-11'}
lines=open(AFR).read().split('\n'); sec=None; rows={}
for l in lines:
    m=re.match(r'## (A\d\d) ',l)
    if m: sec=m.group(1); continue
    if sec and l.startswith('| ') and not l.startswith('| Finding ID') and not l.startswith('|---'):
        c=[x.strip() for x in l.strip().strip('|').split(' | ')]
        if len(c)>=15: rows[(sec,c[0])]=c
out={}
for t,ids in items.items():
    for i in ids.split():
        c=rows.get((t,i))
        if c: out[f'{t}:{i}']=dict(inafr=True,comp=c[1][:80],finding=c[3][:260],cls=c[10][:120],treat=c[13][:160],status=c[14][:120])
        else: out[f'{t}:{i}']=dict(inafr=False)
json.dump(out,open('/home/claude/a07/notes/inherited_afr.json','w'),indent=1)
n=sum(1 for v in out.values() if v['inafr']); print(len(out),'items;',n,'in AFR;',len(out)-n,'not in AFR:',[k for k,v in out.items() if not v['inafr']])
for k,v in out.items():
    if v['inafr']: print(k,'|',v['cls'][:60],'|',v['status'][:70])
