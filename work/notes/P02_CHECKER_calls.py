# P02 checker: list every call in a file (static ast parse of text from stdin; nothing imported or run)
# and whether its final name is named in the part file.
import ast, re, sys
path, part = sys.argv[1], sys.argv[2]
tree = ast.parse(sys.stdin.read())
text = open(part, encoding="utf-8").read()
seen = {}
for n in ast.walk(tree):
    if isinstance(n, ast.Call):
        f = n.func
        if isinstance(f, ast.Attribute):
            name = f.attr
            full = (ast.unparse(f.value) + "." + f.attr)
        elif isinstance(f, ast.Name):
            name = full = f.id
        else:
            continue
        seen.setdefault(full, (name, n.lineno))
print("##", path)
for full, (name, ln) in sorted(seen.items(), key=lambda x: x[1][1]):
    hit = re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", text) is not None
    print(f"  L{ln} {full}: {'named' if hit else 'NOT NAMED'}")
