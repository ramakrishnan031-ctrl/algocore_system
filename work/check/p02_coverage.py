"""P02 checker coverage script (reads only; writes nothing).

Parses the five P02 files at the baseline as TEXT (git show output; ast.parse only,
nothing imported or executed) and checks that every function, method and class
(and, for information, every module-level name) is named in at least one P02
statement; maps the assigned focused questions to the sections that answer them;
and lists the statements that cross-reference each inherited item of P02's row.
"""
import ast
import re
import subprocess
import sys

REPO = "/home/claude/repos/legacy"
BASE = "970aabf"
PART = sys.argv[1]
FILES = [
    "strategies/control.py",
    "strategies/taxonomy.py",
    "core/strategy_direction.py",
    "strategies/__init__.py",
    "screening/__init__.py",
]
QUESTIONS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q16"]
INHERITED = ["C11", "V-06", "V-23", "T-14", "F-11", "K-05", "E-08", "CG-05", "PQ-14", "XA-11"]

text = open(PART, encoding="utf-8").read()
lines = text.splitlines()

# statements: "- P02-Snnn ..." (one line each)
stmts = {}
for ln in lines:
    m = re.match(r"^- (P02-S\d{3}) (.*)$", ln)
    if m:
        stmts[m.group(1)] = m.group(2)
others = {}
for ln in lines:
    m = re.match(r"^- (P02-(?:AP|U|R)\d+) (.*)$", ln)
    if m:
        others[m.group(1)] = m.group(2)


def src(path):
    return subprocess.run(["git", "-C", REPO, "show", f"{BASE}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def names_of(path):
    tree = ast.parse(src(path), filename=path)
    defs, mod_names = [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defs.append(("function", node.name, node.lineno))
        elif isinstance(node, ast.ClassDef):
            defs.append(("class", node.name, node.lineno))
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    defs.append(("method", f"{node.name}.{sub.name}", sub.lineno))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t, ast.Name):
                    mod_names.append(("name", t.id, node.lineno))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                mod_names.append(("import", a.asname or a.name, node.lineno))
    return defs, mod_names


def cited_in(token):
    short = token.split(".")[-1]
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(short) + r"(?![A-Za-z0-9_])")
    return [sid for sid, body in stmts.items() if pat.search(body)]


missing = 0
print("== (a) functions, methods and classes")
for f in FILES:
    defs, mod_names = names_of(f)
    print(f"-- {f}: {len(defs)} function/method/class definitions")
    if not defs:
        ids = [sid for sid, body in stmts.items() if f in body]
        print(f"   (no function, method or class; the file itself is named in: {', '.join(ids) or 'NONE'})")
    for kind, name, ln in defs:
        ids = cited_in(name)
        if not ids:
            missing += 1
        print(f"   {kind:8} {name:28} L{ln:<4} -> {', '.join(ids) if ids else 'NOT COVERED'}")
    print(f"   module-level names (information): ")
    for kind, name, ln in mod_names:
        if kind == "import":
            continue
        ids = cited_in(name)
        print(f"     {name:28} L{ln:<4} -> {', '.join(ids) if ids else 'not named'}")

print("\n== (b) focused questions: sections whose heading names the question")
heading = None
qsec = {q: [] for q in QUESTIONS}
for ln in lines:
    if ln.startswith("## "):          # section heading (the subsections inherit it)
        heading = ln
        continue
    m = re.match(r"^- (P02-S\d{3}) ", ln)
    if m and heading:
        for q in QUESTIONS:
            if re.search(r"\b" + q + r"\b", heading):
                qsec[q].append(m.group(1))
for q in QUESTIONS:
    ids = qsec[q]
    print(f"   {q}: {len(ids)} statements under headings naming {q}"
          f"{(' (' + ids[0] + ' .. ' + ids[-1] + ')') if ids else ' -> NONE'}")

print("\n== (c) inherited items of P02's row (P01-S074)")
for item in INHERITED:
    ids = [sid for sid, body in {**stmts, **others}.items() if item in body]
    if not ids:
        missing += 1
    print(f"   {item:6} -> {', '.join(ids) if ids else 'NOT CROSS-REFERENCED'}")

print(f"\nstatements: {len(stmts)}; points/unknowns/questions: {len(others)}")
print("RESULT:", "PASS (nothing missing)" if missing == 0 else f"FAIL ({missing} missing)")
