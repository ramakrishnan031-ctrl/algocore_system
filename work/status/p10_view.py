# P10 helper: display lines of a text file through the identifier mask of the backup scan (read-only).
# Usage: python3 -I -B p10_view.py <file> <start> <end>      or   python3 -I -B p10_view.py <file> --grep <regex>
import re, sys
pats = [re.compile(r"(?<![A-Za-z0-9])[A-Z]{2,4}\d{3,6}(?![0-9A-Za-z])"),
        re.compile(r"(?<![A-Za-z0-9])[a-z]{2,4}\d{3,6}(?![0-9A-Za-z])"),
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
        re.compile(r"(/home/\w+|/Users/\w+|[A-Za-z]:\\)")]
ALLOW = re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$')
def mask(s):
    for i, rx in enumerate(pats):
        def r(m):
            t = m.group(0)
            if i < 2 and ALLOW.match(t.upper()): return t
            if t.startswith('/home/claude'): return t
            return '<MASKED>'
        s = rx.sub(r, s)
    return s
f = sys.argv[1]
import io
lines = (sys.stdin.read() if f == '-' else open(f, encoding='utf-8', errors='replace').read()).splitlines()
if sys.argv[2] == '--grep':
    rx = re.compile(sys.argv[3])
    for n, l in enumerate(lines, 1):
        if rx.search(l): print(f"{n}: {mask(l)[:int(sys.argv[4]) if len(sys.argv)>4 else 400]}")
else:
    a, b = int(sys.argv[2]), int(sys.argv[3])
    for n in range(a, min(b, len(lines)) + 1):
        print(f"{n}: {mask(lines[n-1])}")
