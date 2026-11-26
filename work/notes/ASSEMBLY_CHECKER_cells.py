# H16 (assembly checker): compare every register cell quoted in STUDY section 13 with the Audit Findings Register
# (Classification, Agreed treatment, Status) and the AFR line numbers cited; read-only. Run with python3 -I.
import re, json
R = '/home/claude/algocore_system/doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md'
S = open('/home/claude/a08/out/A08_STUDY_2026-11-26.md', encoding='utf-8').read()
sec = S[S.index('\n## 13. '):S.index('\n## 14. ')]
lines = open(R, encoding='utf-8').read().split('\n')
def cells(row):
    out, buf, tick = [], '', False
    body = row.strip()
    body = body[1:-1] if body.endswith('|') else body[1:]
    for ch in body:
        if ch == '`': tick = not tick
        if ch == '|' and not tick: out.append(buf.strip()); buf = ''
        else: buf += ch
    out.append(buf.strip()); return out
afr = {}   # (topic, id) -> (line, class, treat, status)
cur = None
for i, l in enumerate(lines, 1):
    m = re.match(r'^## (A0\d) ', l)
    if m: cur = m.group(1)
    if cur and l.startswith('| ') and not l.startswith('| Finding ID') and not l.startswith('|---'):
        c = cells(l)
        if len(c) >= 15:
            fid = c[0]
            key = re.match(r'^([A-Z]{1,2}-?\d+[a-z]?)', fid)
            if key:
                afr.setdefault((cur, key.group(1)), []).append((i, fid, c[10], c[13], c[14]))
out = []
n_rows = n_ok = 0
for row in sec.split('\n'):
    if not row.startswith('| ') or row.startswith('|---'): continue
    c = cells(row)
    # find the record ID cell: "A0x ID" in cell 1 (13.2 numbered tables) or cell 0
    idcell = None
    for cc in c[:3]:
        m = re.match(r'^(?:record |OIR )?(A0\d) ([A-Z]{1,2}-?\d+[a-z]?)\b', cc)
        if m: idcell = m; break
    if not idcell: continue
    topic, fid = idcell.group(1), idcell.group(2)
    hits = afr.get((topic, fid))
    if not hits:
        out.append(f'NO-AFR {topic} {fid} | row says: {[x[:80] for x in c[2:4]]}')
        continue
    n_rows += 1
    line, rid, cl, tr, st = hits[0]
    probs = []
    for name, v in (('class', cl), ('treat', tr), ('status', st)):
        if ('"' + v + '"') not in row:
            probs.append(f'{name} not quoted exactly: AFR="{v[:120]}"')
    # AFR line cited?
    mline = re.search(r'AFR L(\d+)', row)
    if mline and int(mline.group(1)) not in [h[0] for h in hits]:
        probs.append(f'AFR line cited L{mline.group(1)} but register row is L{line}')
    if probs:
        out.append(f'MISMATCH {topic} {fid} (AFR L{line}, {rid[:40]}): ' + ' || '.join(probs))
    else:
        n_ok += 1
print(f'rows with an AFR row: {n_rows}; all three cells quoted exactly and AFR line right: {n_ok}')
for o in out: print(o)
