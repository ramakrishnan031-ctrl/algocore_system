"""P05 checker coverage script: parses the two scripts' text (from git show, passed as file
arguments read as text; no import or execution of legacy code) with ast, lists every def/class,
every argparse option and every call on an external object (attribute calls and imported names),
and checks that the part file mentions each one. Also lists branch-heavy functions and the
statement IDs that describe their branches."""
import ast, re, sys

part_path, *srcs = sys.argv[1:]
part = open(part_path, encoding="utf-8").read()

def mentioned(token):
    return token in part

for src_path in srcs:
    name = src_path.split("/")[-1].replace(".txt", "")
    src = open(src_path, encoding="utf-8").read()
    tree = ast.parse(src)
    print(f"=== {name}")
    defs = [(n.name, n.lineno, n.end_lineno) for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))]
    for d, a, b in defs:
        print(f"def {d} L{a}-L{b}: {'COVERED' if mentioned(d) else 'MISSING'}")
    opts = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument":
            opts.append((n.args[0].value, n.lineno))
    for o, l in opts:
        print(f"option {o} L{l}: {'COVERED' if mentioned(o) else 'MISSING'}")
    calls = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute):
                calls.add((f.attr, n.lineno))
            elif isinstance(f, ast.Name):
                calls.add((f.id, n.lineno))
    builtin = {"print", "len", "abs", "str", "int", "float", "getattr", "list", "range", "dict", "super", "isinstance"}
    for c, l in sorted(calls, key=lambda x: x[1]):
        if c in builtin:
            continue
        print(f"call {c} L{l}: {'COVERED' if mentioned(c) else 'MISSING'}")
    imps = []
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            imps.append((n.module, [a.name for a in n.names], n.lineno))
        elif isinstance(n, ast.Import):
            imps.append((None, [a.name for a in n.names], n.lineno))
    for m, ns, l in imps:
        print(f"import L{l} {m} {ns}")
    # branch-heavy functions
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            br = sum(isinstance(x, (ast.If, ast.For, ast.While, ast.Try, ast.IfExp, ast.BoolOp)) for x in ast.walk(n))
            if br:
                print(f"branches {n.name}: {br}")
