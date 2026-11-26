# Read-only: compare the register cells quoted in STUDY section 13 with the Audit Findings Register.
import re, subprocess
R='/home/claude/algocore_system/doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md'
S=open('/home/claude/a08/out/A08_STUDY_2026-11-26.md',encoding='utf-8').read()
sec=S[S.index('\n## 13. '):S.index('\n## 14. ')]
lines=open(R,encoding='utf-8').read().split('\n')
sections={}; cur=None
for i,l in enumerate(lines,1):
    m=re.match(r'^## (A0\d) ',l)
    if m: cur=m.group(1); sections[cur]=[]
    if cur and l.startswith('| '): sections[cur].append(l)
def cells(row):
    out,buf,tick=[], '',False
    for ch in row.strip()[1:-1]:
        if ch=='`': tick=not tick
        if ch=='|' and not tick: out.append(buf.strip()); buf=''
        else: buf+=ch
    out.append(buf.strip()); return out
ok=bad=0
for row in sec.split('\n'):
    if not row.startswith('| '): continue
    m=re.search(r'\| (A0\d) ([A-Z]{1,2}-?\d+[a-z]?)\b', row)
    if not m: continue
    topic,fid=m.group(1),m.group(2)
    hits=[c for c in (cells(r) for r in sections.get(topic,[])) if c[0]==fid or c[0].startswith(fid+' (')]
    if not hits: continue
    c=hits[0]
    for k,v in (('class',c[10]),('treat',c[13]),('status',c[14])):
        if ('"'+v+'"') in row or (k=='status' and v=='AGREED' and '"AGREED"' in row): ok+=1
        else: bad+=1; print('MISMATCH', topic, fid, k, '| register:', v[:90])
print('cells matched:', ok, '| mismatches:', bad)
