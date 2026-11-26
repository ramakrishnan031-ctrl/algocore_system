# H16: token diff between each consolidated A08-AP / A08-U entry and the source items it cites (read-only).
import json,re,sys
idx=json.load(open('/home/claude/a08/notes/ASSEMBLY_CHECKER_index.json'))
S=open('/home/claude/a08/out/A08_STUDY_2026-11-26.md',encoding='utf-8').read().split('\n')
def toks(t):
    s=set()
    s|=set(re.findall(r'`([^`]+)`',t))
    s|=set(re.findall(r'(?<![A-Za-z0-9-])(L\d{1,4})(?![0-9])',t))
    s|=set(re.findall(r'(?<![A-Za-z0-9])(P0\d-(?:S\d{3}|AP\d\d|U\d\d|R\d))',t))
    s|=set(m for m in re.findall(r'(?<![\w.-])(\d+\.\d+|\d{2,})(?![\w.])',t) if not re.match(r'^(19|20)\d\d$',m))
    s|=set(re.findall(r'"([^"]{4,60})"',t))
    s|=set(re.findall(r'\b(A0\d [A-Z]{1,2}-?\d+[a-z]?)\b',t))
    s|=set(re.findall(r'\b(UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL)\b',t))
    return s
verdict=re.compile(r'\b(defect|bug|wrong|incorrect|broken|flaw|fault|should|must be fixed|error-prone|correctly|properly)\b',re.I)
for n,l in enumerate(S,1):
    m=re.match(r'^- \*\*(A08-(?:AP|U)-\d\d)\*\* \(([^)]*)\)', l)
    if not m: continue
    cid=m.group(1); head=m.group(2)
    srcs=re.findall(r'P0\d-(?:AP|U)\d\d|P07-S\d{3}', head)+['P07 '+x for x in re.findall(r'P07 (AP-\d\d)',head)]
    pool='\n'.join(idx[s]['text'] for s in srcs if s in idx)
    body=l[m.end():]
    ts=toks(pool); tb=toks(body)
    lost=sorted(t for t in ts if t not in body and t not in srcs)
    added=sorted(t for t in tb if t not in pool and not re.fullmatch(r'P0\d-(AP|U)\d\d',t))
    v=verdict.findall(body)
    if lost or added or v:
        print(f'== {cid} L{n} srcs={srcs}')
        if lost: print('   LOST:', ' | '.join(lost)[:900])
        if added: print('   ADDED:', ' | '.join(added)[:600])
        if v: print('   VERDICT-WORDS:', v)
