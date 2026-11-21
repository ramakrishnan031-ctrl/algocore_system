# P01 checker: every table row naming A07 in each AUDIT, with the enclosing section heading (read-only)
import re, sys
sys.path.insert(0,'/home/claude/a07/check')
from p01chk_view import lines, mask
from p01chk_afr import cells
def scan(k, only_handoff=True, w=160):
    L=lines(k); sec=''; hdr=None; out=[]
    for n,l in enumerate(L,1):
        if l.startswith('#'): sec=l.strip(); hdr=None; continue
        if l.startswith('|'):
            c=cells(l)
            if hdr is None: hdr=(n,c); continue
            if set(l.strip())<=set('|-: '): continue
            if re.search(r'\bA07\b',l):
                if only_handoff and not re.search(r'[Hh]andoff|handed|[Cc]ross-topic|Owner',sec): continue
                out.append((n,sec[:70],mask(l)[:w]))
        else: hdr=None
    return out
if __name__=='__main__':
    k=sys.argv[1]; oh=(sys.argv[2]=='h') if len(sys.argv)>2 else True
    for r in scan(k,oh, int(sys.argv[3]) if len(sys.argv)>3 else 160): print(*r, sep=' | ')
