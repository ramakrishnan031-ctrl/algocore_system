# H16 (assembly checker): token-support and label check of STUDY lines against the statements they cite.
# Read-only. Usage: python3 -I ASSEMBLY_CHECKER_support.py <first line> <last line> [--show] [--width N]
import re, json, sys
W = '/home/claude/a08'
idx = json.load(open(f'{W}/notes/ASSEMBLY_CHECKER_index.json', encoding='utf-8'))
S = open(f'{W}/out/A08_STUDY_2026-11-26.md', encoding='utf-8').read().split('\n')
a, b = int(sys.argv[1]), int(sys.argv[2])
show = '--show' in sys.argv
width = int(sys.argv[sys.argv.index('--width') + 1]) if '--width' in sys.argv else 300
# consolidated entries in the STUDY (A08-AP-nn, A08-U-nn, A08-Q-nn) -> their text, so a citation of one counts
cons = {}
for i, l in enumerate(S, 1):
    m = re.match(r'^- \*\*(A08-(?:AP|U|Q)-\d\d)\*\*', l)
    if m: cons[m.group(1)] = l
ID = r'P0[1-7]-(?:S\d{3}|AP\d+|U\d+|R\d+|X\d+)'
def expand(text):
    ids = []
    # ranges: P01-S014 to P01-S101 / P01-S014 to S101 / P01-S014 to -S101
    for m in re.finditer(r'(P0[1-7])-S(\d{3}) to (?:(P0[1-7])-)?S(\d{3})', text):
        p, x, p2, y = m.group(1), int(m.group(2)), m.group(3) or m.group(1), int(m.group(4))
        if p2 == p and y >= x and y - x < 400:
            ids += [f'{p}-S{n:03d}' for n in range(x, y + 1)]
    for m in re.finditer(r'(P0[1-7])-(AP|U)(\d+) to (?:(P0[1-7])-)?(?:AP|U)?(\d+)', text):
        p, k, x, y = m.group(1), m.group(2), int(m.group(3)), int(m.group(5))
        if y >= x and y - x < 40:
            ids += [f'{p}-{k}{n:02d}' for n in range(x, y + 1)]
    ids += re.findall(r'(?<![A-Za-z0-9])(' + ID + r')(?![0-9])', text)
    ids += ['P07 ' + x for x in re.findall(r'P07 (AP-\d\d)', text)]
    return list(dict.fromkeys(ids))
def tokens(text):
    t = set()
    for m in re.findall(r'`([^`]+)`', text): t.add(m)
    for m in re.findall(r'(?<![A-Za-z0-9-])(L\d{1,4})(?![0-9])', text): t.add(m)
    for m in re.findall(r'(?<![\w.-])(\d+\.\d+|\d{2,})(?![\w.])', text):
        if not re.match(r'^(19|20)\d\d$', m): t.add(m)
    for m in re.findall(r'"([^"]{3,80})"', text): t.add(m)
    return t
LAB = re.compile(r'(FACT|INTERPRETATION|UNKNOWN / NOT ESTABLISHED|HISTORICAL|OPEN QUESTION)')
for n in range(a, b + 1):
    l = S[n - 1]
    if not l.strip() or l.startswith('#') or l.startswith('|---'): continue
    ids = expand(l)
    known = [i for i in ids if i in idx]
    unknown = [i for i in ids if i not in idx]
    pool = '\n'.join(idx[i]['text'] for i in known)
    # consolidated IDs cited
    for c in re.findall(r'A08-(?:AP|U|Q)-\d\d', l):
        if c in cons and not l.startswith('- **' + c): pool += '\n' + cons[c]
    toks = tokens(l)
    # remove tokens that are citation fragments
    toks = {t for t in toks if not re.fullmatch(ID, t)}
    miss = sorted(t for t in toks if t not in pool)
    # label check: FACT segments whose cited statements carry no FACT label
    flags = []
    segs = re.split(r'(?=(?:^|(?<=[.;:] )|(?<=\| )|(?<=- ))(?:FACT|INTERPRETATION|UNKNOWN / NOT ESTABLISHED|HISTORICAL|OPEN QUESTION)\b)', l)
    for sg in segs:
        m = LAB.match(sg)
        if not m or m.group(1) != 'FACT': continue
        head = sg[:40]
        if head.startswith('FACT and INTERPRETATION') or head.startswith('FACT, INTERPRETATION') or head.startswith('FACT and UNKNOWN') : continue
        for i in expand(sg):
            if i in idx and '-S' in i:
                lab = idx[i]['label'] or 'FACT(table)'
                if 'FACT' not in lab:
                    flags.append(f'{i}={lab}')
    if miss or unknown or flags or show:
        print(f'--- L{n} cites {len(known)} ({len(unknown)} unresolved {unknown[:5]})')
        if show: print('    ' + l[:width])
        if miss: print('    MISSING TOKENS: ' + ' | '.join(miss)[:1500])
        if flags: print('    FACT-SEGMENT CITES NON-FACT: ' + ', '.join(flags))
