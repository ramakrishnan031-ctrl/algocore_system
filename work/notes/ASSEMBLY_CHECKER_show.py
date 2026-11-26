# H16: print part statements by ID (read-only). Usage: python3 -I ASSEMBLY_CHECKER_show.py [--w N] ID [ID ...]
# An ID may be a range "P01-S014:P01-S020".
import json, sys, re
idx = json.load(open('/home/claude/a08/notes/ASSEMBLY_CHECKER_index.json', encoding='utf-8'))
args = sys.argv[1:]
w = 100000
if args and args[0] == '--w':
    w = int(args[1]); args = args[2:]
for a in args:
    if ':' in a:
        x, y = a.split(':')
        p, k, n1 = re.match(r'(P0\d)-([A-Z]+)(\d+)', x).groups()
        n2 = int(re.match(r'P0\d-[A-Z]+(\d+)', y).group(1))
        wid = len(re.match(r'P0\d-[A-Z]+(\d+)', x).group(1))
        ids = [f'{p}-{k}{str(n).zfill(wid)}' for n in range(int(n1), n2 + 1)]
    else:
        ids = [a]
    for i in ids:
        v = idx.get(i)
        if not v: print(f'## {i}: NOT FOUND'); continue
        print(f"## {i} [{v['part']} L{v['line']}; {v['label'] or 'table'}] {v['text'][:w]}")
