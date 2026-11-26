# P02 checker coverage script (H7). Static parse only: reads source TEXT from stdin (piped from
# `git show 970aabf:<path>`), parses it with ast, never imports or executes it.
# Usage: git -C <legacy clone> show 970aabf:<path> | python3 -I P02_CHECKER_coverage.py <path> <part file>
# For each def/class/module constant: which statements name it.
# For each branch line (If/For/While/Try/except/Return/IfExp/With/comprehension-if): whether some
# statement of the file's own section (3 fetch, 4 zone_builder, 5 zone_cache, 6 zone_warmer, 7 summary)
# cites a line range that contains it.
import ast, re, sys

path, part = sys.argv[1], sys.argv[2]
src = sys.stdin.read()
tree = ast.parse(src)
text = open(part, encoding="utf-8").read()

# split the part into sections by "## n." headings
secs = {}
cur = None
for line in text.split("\n"):
    m = re.match(r"^## (\d+)\.", line)
    if m:
        cur = int(m.group(1))
    if cur is not None:
        secs.setdefault(cur, []).append(line)
stmts = []   # (sid, section, body)
for sec, lines in secs.items():
    body = "\n".join(lines)
    # a statement runs from its "- Pxx-Snnn" bullet to the next bullet or heading
    for m in re.finditer(r"^- (P02-S\d{3}) (.*?)(?=^- P02-|^## |^### |\Z)", body, flags=re.M | re.S):
        stmts.append((m.group(1), sec, m.group(2)))

FILESEC = {"sr_detector/fetch.py": {3, 7}, "sr_detector/zone_builder.py": {4, 7},
           "sr_detector/zone_cache.py": {5, 7}, "sr_detector/zone_warmer.py": {6, 7}}
own = FILESEC.get(path, set())

def covering(name):
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")
    return sorted({sid for sid, sec, body in stmts if pat.search(body)})

def cited_lines(body):
    out = set()
    for a, b in re.findall(r"L(\d+) to L(\d+)", body):
        out.update(range(int(a), int(b) + 1))
    for a in re.findall(r"L(\d+)(?! to)", body):
        out.add(int(a))
    return out

own_cited = {}
for sid, sec, body in stmts:
    if sec in own:
        for ln in cited_lines(body):
            own_cited.setdefault(ln, set()).add(sid)

print(f"## {path}")
missing_names = []
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        kind = "class" if isinstance(node, ast.ClassDef) else "def"
        cov = covering(node.name)
        if not cov:
            missing_names.append(node.name)
        print(f"{kind} {node.name} L{node.lineno}-L{node.end_lineno}: named in {len(cov)} stmt(s) {cov[:10]}{' ...' if len(cov) > 10 else ''}")
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                cov = covering(t.id)
                if not cov:
                    missing_names.append(t.id)
                print(f"const {t.id} L{node.lineno}: named in {len(cov)} stmt(s) {cov[:10]}")
BR = (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.Return, ast.IfExp, ast.With)
blines = set()
for node in ast.walk(tree):
    if isinstance(node, BR):
        blines.add((node.lineno, type(node).__name__))
    if isinstance(node, ast.comprehension) and node.ifs:
        for c in node.ifs:
            blines.add((c.lineno, "comp-if"))
uncited = [(ln, k) for ln, k in sorted(blines) if ln not in own_cited]
print(f"branch-type lines: {len(blines)}; cited by a statement of the file's own section(s) {sorted(own)}: {len(blines) - len(uncited)}")
for ln, k in uncited:
    print(f"    NOT CITED in own section: L{ln} ({k})")
print(f"names not named in any statement: {missing_names if missing_names else 'none'}")
print()
