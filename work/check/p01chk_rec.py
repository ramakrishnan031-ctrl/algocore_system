# P01 checker: AUDIT record reader (heading line, field lines, Owner and Result fields joined across wraps); read-only
import re, sys
sys.path.insert(0,'/home/claude/a07/check')
from p01chk_view import lines, mask
RECS={'A01A':'C11 C14 C15 C20 B-28','A02A':'V-06 T-14 T-20 F-11 K-05 K-27',
'A03A':'D-05 D-09 H-16 H-17 H-50 P-02 P-11 Q-11 Q-12 Q-22 U-24 U-25 E-08',
'A04A':'OA-22 RD-12 RL-11 CG-05','A05A':'CM-07 FB-01 FB-02 FB-07','A06A':'WA-06 WA-07 PQ-02 PQ-08 EV-02 EV-11 ET-06'}
def record(k,i):
    L=lines(k)
    hs=[n for n,l in enumerate(L,1) if re.match(r'^#{3,6} '+re.escape(i)+r' — ',l)]
    if len(hs)!=1: return dict(err=f'headings {hs}')
    h=hs[0]; e=h
    while e<len(L) and not (re.match(r'^#{1,6} ',L[e])): e+=1
    # e = index of next heading (0-based) -> last line number e
    fields={}; cur=None
    for n in range(h+1,e+1):
        l=L[n-1]
        m=re.match(r'^- \*\*(.+?):\*\*\s*(.*)$',l)
        if m: cur=m.group(1); fields[cur]=[n,m.group(2)]; continue
        if cur and l.startswith('  ') and l.strip(): fields[cur][1]+=' '+l.strip(); continue
        if cur and (not l.strip() or l.startswith('|')): cur=None
    last=e
    while last>h and not L[last-1].strip(): last-=1
    return dict(h=h,last=last,fields=fields)
if __name__=='__main__':
    w=int(sys.argv[1]) if len(sys.argv)>1 else 300
    for k,ids in RECS.items():
        for i in ids.split():
            r=record(k,i)
            if 'err' in r: print(k,i,r['err']); continue
            o=r['fields'].get('Owner'); rc=r['fields'].get('Result and classification')
            print(f"{k} {i} head L{r['h']} last L{r['last']} | Owner L{o[0] if o else '-'}: {mask(o[1])[:w] if o else '-'}")
            print(f"     Result L{rc[0] if rc else '-'}: {mask(rc[1])[:160] if rc else '-'}")
