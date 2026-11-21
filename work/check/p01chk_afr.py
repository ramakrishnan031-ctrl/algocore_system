# P01 checker: reads the Audit Findings Register rows of the 51 inherited IDs (read-only; prints through the mask)
import re, json, sys
sys.path.insert(0,'/home/claude/a07/check')
from p01chk_view import F, mask
ITEMS={'A01':'C11 C14 C15 C20 B-28 B-08','A02':'V-06 V-23 T-14 T-20 F-11 K-05 K-27',
'A03':'D-05 D-09 H-16 H-17 H-50 P-02 P-11 Q-11 Q-12 Q-22 Q-45 U-24 U-25 E-08',
'A04':'OA-22 RD-12 RL-11 PR-23 CG-05','A05':'CM-07 CM-22 FB-01 FB-02 FB-07 FB-14',
'A06':'WA-06 WA-07 PQ-02 PQ-08 PQ-13 PQ-14 PQ-15 EV-02 EV-11 EV-19 ET-06 ET-13 XA-11'}
def cells(row):
    out=[];cur='';bt=False;i=0;s=row.strip()
    if s.startswith('|'): s=s[1:]
    if s.endswith('|'): s=s[:-1]
    while i<len(s):
        ch=s[i]
        if ch=='\\' and i+1<len(s) and s[i+1]=='|': cur+='|'; i+=2; continue
        if ch=='`': bt=not bt
        if ch=='|' and not bt: out.append(cur.strip()); cur=''
        else: cur+=ch
        i+=1
    out.append(cur.strip()); return out
def afr_rows():
    L=open(F['AFR'],encoding='utf-8').read().split('\n'); sec=None; hdr=None; rows={}
    for n,l in enumerate(L,1):
        m=re.match(r'## (A\d\d) ',l)
        if m: sec=m.group(1); hdr=None; continue
        if l.startswith('## '): sec=None; continue
        if sec and l.startswith('|'):
            c=cells(l)
            if c[0]=='Finding ID': hdr=c; continue
            if hdr and not set(l)<=set('|- ') and len(c)==len(hdr):
                rows.setdefault((sec,c[0]),[]).append((n,dict(zip(hdr,c))))
    return rows
if __name__=='__main__':
    rows=afr_rows(); res={}
    for t,ids in ITEMS.items():
        for i in ids.split():
            r=rows.get((t,i))
            if not r: res[f'{t} {i}']=None; print(t,i,'NO ROW'); continue
            if len(r)>1: print('DUP',t,i,[x[0] for x in r])
            n,d=r[0]
            res[f'{t} {i}']=dict(line=n,cls=d['Classification'],treat=d['Agreed treatment (Phase 2 input), or OPEN'],status=d['Status'],comp=d['Component'])
            if len(sys.argv)>1: print(t,i,'L%d'%n,'|CLS:',mask(d['Classification'])[:200],'|TRT:',mask(d['Agreed treatment (Phase 2 input), or OPEN'])[:200],'|ST:',mask(d['Status'])[:200])
    n=sum(1 for v in res.values() if v); print('rows:',n,'none:',[k for k,v in res.items() if not v])
    first=lambda s: re.split(r'[;.(]',s)[0].strip()
    from collections import Counter
    print('first label:',Counter(first(v['cls']) for v in res.values() if v))
    print('status:',Counter(v['status'] for v in res.values() if v))
