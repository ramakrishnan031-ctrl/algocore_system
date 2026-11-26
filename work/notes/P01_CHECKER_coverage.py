# P01 checker coverage script (H4). Static parse only: reads source TEXT from stdin (piped from
# `git show 970aabf:<path>`), parses it with ast, never imports or executes it.
# Usage: git -C <legacy clone> show 970aabf:<path> | python3 -I P01_CHECKER_coverage.py <path> <part file>
import ast, re, sys

path, part = sys.argv[1], sys.argv[2]
src = sys.stdin.read()
tree = ast.parse(src)
text = open(part, encoding="utf-8").read()
stmts = re.findall(r"^- (P01-S\d{3}) (.*)$", text, flags=re.M)
# table rows of section 8.2 carry IDs in the first cell
stmts += re.findall(r"^\| (P01-S\d{3}) \|(.*)$", text, flags=re.M)

def covering(name):
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")
    return sorted({sid for sid, body in stmts if pat.search(body)})

BRANCH = (ast.If, ast.For, ast.While, ast.Return, ast.IfExp, ast.BoolOp, ast.comprehension, ast.Try)
print(f"## {path}")
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        kind = "class" if isinstance(node, ast.ClassDef) else "def"
        branches = []
        if kind == "def":
            for sub in ast.walk(node):
                if isinstance(sub, (ast.If, ast.For, ast.While, ast.Try, ast.Return, ast.IfExp)):
                    branches.append(f"{type(sub).__name__}@L{sub.lineno}")
        cov = covering(node.name)
        print(f"{kind} {node.name} L{node.lineno}-L{node.end_lineno}: covered by {len(cov)} stmt(s) {cov[:12]}{' ...' if len(cov) > 12 else ''}")
        if branches:
            print(f"    branch/return nodes: {', '.join(branches)}")
# module-level assignments (constants)
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                cov = covering(t.id)
                print(f"const {t.id} L{node.lineno}: covered by {len(cov)} stmt(s) {cov[:12]}")
# dataclass fields
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for b in node.body:
            if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name):
                cov = covering(b.target.id)
                if not cov:
                    print(f"  field {node.name}.{b.target.id} L{b.lineno}: NOT NAMED in any statement")
print()
