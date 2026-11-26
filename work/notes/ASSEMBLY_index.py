import re, sys
path, width = sys.argv[1], int(sys.argv[2])
start = sys.argv[3] if len(sys.argv) > 3 else None
stop = sys.argv[4] if len(sys.argv) > 4 else None
rx = re.compile(r'^(?:- |\| )?\**(P0[1-7]-S\d{3})\**[ .|]*(.*)$')
on = start is None
for line in open(path, encoding='utf-8'):
    s = line.rstrip('\n')
    if s.startswith('#'):
        if start and s.startswith(start): on = True
        if stop and s.startswith(stop): on = False
        if on: print(s)
        continue
    if not on: continue
    m = rx.match(s)
    if m:
        print(m.group(1), m.group(2)[:width].replace('|', '/'))
