import sys, re
# Read-only reader of the Audit Findings Register: prints Classification, Agreed treatment, Status for given IDs
# within each topic's section. Usage: python3 -I ASSEMBLY_afr.py <AFR path> A01:C3,C18 A02:L-08 ...
path = sys.argv[1]
lines = open(path, encoding='utf-8').read().split('\n')
sections = {}
cur = None
for i, l in enumerate(lines, 1):
    m = re.match(r'^## (A0\d) ', l)
    if m: cur = m.group(1); sections[cur] = []
    if cur and l.startswith('| '): sections[cur].append((i, l))
def cells(row):
    out, buf, tick = [], '', False
    for ch in row.strip()[1:-1] if row.strip().endswith('|') else row.strip()[1:]:
        if ch == '`': tick = not tick
        if ch == '|' and not tick: out.append(buf.strip()); buf = ''
        else: buf += ch
    out.append(buf.strip()); return out
for arg in sys.argv[2:]:
    topic, ids = arg.split(':')
    for fid in ids.split(','):
        hits = [(i, r) for i, r in sections.get(topic, []) if (cells(r)[0] == fid or cells(r)[0].startswith(fid + ' ('))]
        if not hits:
            print(f"{topic} {fid}: no AFR row"); continue
        for i, r in hits:
            c = cells(r)
            if len(c) < 15: print(f"{topic} {fid} L{i}: {len(c)} cells?"); continue
            print(f"{topic} {c[0]} AFR L{i} | class: {c[10]} | treat: {c[13]} | status: {c[14]}")
