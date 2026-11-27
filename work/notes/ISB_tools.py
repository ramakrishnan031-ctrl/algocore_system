"""ISB writer helper (read-only). Runs only `git show`, `git blame`, `git log`, `git grep` on the legacy clone
at the baseline; imports no legacy code; writes no file. Output is masked for identifier-shaped text.

Usage (python3 -I):
  show  <path> [a b]            numbered lines a..b at the baseline, with blame commit+date per line
  dates <path> a-b [a-b ...]     introducing commits (full hash) and dates per range, grouped
  com   <path>                  docstrings and comments with line numbers and blame dates
  msg   <commit> [...]          commit messages (full hash, date, body; trailer lines dropped)
  grep  <pattern> [paths...]    git grep -n -I -i -E with the four exclusions, masked
  log   <path>                  commits touching path (full hash, date, subject)
"""
import ast, io, re, subprocess, sys, tokenize
REPO = '/home/claude/repos/legacy'
BASE = '970aabf3c78d777d9d34549e021f7c8e756c7bdb'
EXCL = [':(exclude)config/accounts.csv', ':(exclude,glob)**/.env*', ':(exclude,glob)**/*.local.yaml',
        ':(exclude,glob)**/*token*.json']
FORBID = re.compile(r'(^|/)(config/accounts\.csv|\.env[^/]*|[^/]*\.local\.yaml|[^/]*token[^/]*\.json)$')
MASKS = [
    (re.compile(r"(?<![A-Za-z0-9])[A-Z]{2,4}\d{3,6}(?![0-9A-Za-z])"), '<ID?>'),
    (re.compile(r"(?<![A-Za-z0-9])[a-z]{2,4}\d{3,6}(?![0-9A-Za-z])"), '<id?>'),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), '<IP?>'),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), '<EMAIL?>'),
    (re.compile(r"(/home/\w+|/Users/\w+|[A-Za-z]:\\\\)"), '<HOMEPATH?>'),
]
ALLOW = re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$')


def mask(s):
    for rx, rep in MASKS:
        def f(m):
            t = m.group(0)
            if rep in ('<ID?>', '<id?>') and ALLOW.match(t.upper()):
                return t
            if rep == '<IP?>' and t in ('0.0.0.0', '127.0.0.1'):
                return t
            return rep
        s = rx.sub(f, s)
    return s


def git(*args):
    r = subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True)
    return r.stdout


def check_path(p):
    if FORBID.search(p):
        sys.exit('refused: forbidden path pattern')


_date_cache = {}


def cdate(h):
    if h not in _date_cache:
        out = git('log', '-1', '--format=%H %as', h).split()
        _date_cache[h] = out[1] if len(out) > 1 else '?'
    return _date_cache[h]


def blame_map(path):
    out = git('blame', '-s', '-l', BASE, '--', path)
    m = {}
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        h = parts[0].lstrip('^')
        mm = re.match(r'(\d+)\)', parts[1])
        if not mm:
            continue
        m[int(mm.group(1))] = h
    return m


def text(path):
    check_path(path)
    return git('show', f'{BASE}:{path}')


def cmd_show(path, a=None, b=None):
    lines = text(path).splitlines()
    bm = blame_map(path)
    a = int(a) if a else 1
    b = int(b) if b else len(lines)
    for i in range(a, min(b, len(lines)) + 1):
        h = bm.get(i, '?')
        print(f'{i:5d} [{h[:10]} {cdate(h) if h != "?" else "?"}] {mask(lines[i-1])}')


def ranges_dates(path, specs):
    bm = blame_map(path)
    for spec in specs:
        a, _, b = spec.partition('-')
        a = int(a); b = int(b or a)
        counts = {}
        for i in range(a, b + 1):
            h = bm.get(i)
            if h:
                counts.setdefault(h, []).append(i)
        print(f'L{a} to L{b}:')
        for h, ls in sorted(counts.items(), key=lambda kv: cdate(kv[0])):
            print(f'   {h} {cdate(h)}  {len(ls)} lines  (L{ls[0]}..L{ls[-1]})')


def cmd_com(path):
    src = text(path)
    bm = blame_map(path)
    items = []
    try:
        tree = ast.parse(src)
        for node in [tree] + [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]:
            ds = ast.get_docstring(node, clean=False)
            if ds is not None:
                body0 = node.body[0]
                name = getattr(node, 'name', '<module>')
                items.append((body0.lineno, body0.end_lineno, f'DOCSTRING {name}'))
    except SyntaxError:
        pass
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            items.append((tok.start[0], tok.start[0], 'COMMENT'))
    lines = src.splitlines()
    seen = set()
    for a, b, kind in sorted(items):
        for i in range(a, b + 1):
            if (i, kind == 'COMMENT') in seen:
                continue
            seen.add((i, kind == 'COMMENT'))
            h = bm.get(i, '?')
            print(f'{i:5d} [{h[:10]} {cdate(h) if h != "?" else "?"}] {kind[:3]} {mask(lines[i-1])}')


def cmd_msg(*commits):
    for c in commits:
        out = git('log', '-1', '--format=%H %as%n%B', c)
        keep = [l for l in out.splitlines() if not re.match(r'^(Co-Authored-By|Signed-off-by|Claude-Session|Generated with)', l, re.I)]
        print(mask('\n'.join(keep)))
        print('-' * 60)


def cmd_grep(pattern, *paths):
    args = ['grep', '-n', '-I', '-i', '-E', pattern, BASE, '--'] + (list(paths) if paths else ['.']) + EXCL
    out = git(*args)
    for line in out.splitlines():
        print(mask(line.replace(BASE + ':', '', 1)))


def cmd_log(path):
    check_path(path)
    print(mask(git('log', '--format=%H %as %s', BASE, '--', path)))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'show':
        cmd_show(*sys.argv[2:5])
    elif cmd == 'dates':
        ranges_dates(sys.argv[2], sys.argv[3:])
    elif cmd == 'com':
        cmd_com(sys.argv[2])
    elif cmd == 'msg':
        cmd_msg(*sys.argv[2:])
    elif cmd == 'grep':
        cmd_grep(sys.argv[2], *sys.argv[3:])
    elif cmd == 'log':
        cmd_log(sys.argv[2])
