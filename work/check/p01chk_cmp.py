# P01 checker: compares the part file's section 2 table cells with the AFR rows (read-only)
import re, sys
sys.path.insert(0,'/home/claude/a07/check')
from p01chk_afr import afr_rows, cells, ITEMS
P='/home/claude/a07/parts/A07_PRIOR_TOPIC_HANDOFFS_2026-11-21.md'
def part_rows():
    out={}
    for n,l in enumerate(open(P,encoding='utf-8').read().split('\n'),1):
        if l.startswith('| P01-S') and ' HISTORICAL (record) | A0' in l:
            c=cells(l); out[(c[1],c[2])]=dict(n=n,sid=c[0].split()[0],cells=c)
    return out
if __name__=='__main__':
    pr=part_rows(); ar=afr_rows(); bad=0
    print('part rows:',len(pr))
    for t,ids in ITEMS.items():
        for i in ids.split():
            p=pr.get((t,i))
            if not p: print('MISSING in part',t,i); bad+=1; continue
            c=p['cells']; a=ar.get((t,i))
            q=lambda s: re.findall(r'"([^"]*)"',s)
            if a:
                n,d=a[0]
                cls=d['Classification']; tr=d['Agreed treatment (Phase 2 input), or OPEN']; st=d['Status']
                qc=q(c[4]); qt=q(c[5])
                ok1 = qc and qc[0]==cls
                ok2 = len(qt)>=2 and qt[0]==tr and qt[1]==st
                ok3 = f'AFR L{n}' in c[3]
                if not(ok1 and ok2 and ok3): bad+=1; print('DIFF',p['sid'],t,i,'cls',ok1,'treat/status',ok2,'afrline',ok3, qc, qt[:2], n)
            else:
                ok = 'no AFR row' in c[3] and 'not entered' in c[5]
                if not ok: bad+=1; print('DIFF (match)',p['sid'],t,i,c[3][:80],c[5])
    print('differences:',bad)
