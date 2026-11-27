# RT writer: coverage of the RT allocation rows by the disposition rows of section 2 of the part file.
# Reads two workspace Markdown files only; imports nothing from the legacy clone; writes nothing.
import re

alloc = open("/home/claude/a08/notes/AUDIT_ALLOCATION.md", encoding="utf-8").read().splitlines()
items = []
for l in alloc:
    m = re.match(r"^\| (.+?) \| RT \| ", l)
    if m:
        items.append(m.group(1).strip())
print("allocated to RT:", len(items))

part = open("/home/claude/a08/parts/A08_AUDIT_PART_RT_2026-11-27.md", encoding="utf-8").read()
s = part.index("## 2. Dispositions")
e = part.index("### 2.7")
sec2 = part[s:e].splitlines()
rows = [l for l in sec2 if l.startswith("| ") and not l.startswith("|---")]
first_cells = []
for r in rows:
    c = r.split("|")[1].strip()
    first_cells.append(c)

def key_of(cell):
    # normalise: "A05-17 (L2404 ...)" -> "A05-17"; "N5 (A07 RTR L560)" -> "note N5"; "A01 S-37 (MATCH row ...)" -> "A01 S-37"
    c = cell
    m = re.match(r"^(A08-(?:AP|U|Q)-\d+)", c)
    if m:
        return m.group(1)
    m = re.match(r"^(N\d)\b", c)
    if m:
        return "note " + m.group(1)
    m = re.match(r"^(A0\d-\d+)\b", c)
    if m:
        return m.group(1)
    m = re.match(r"^(A0\d [A-Z]+-\d+)", c)
    if m:
        return m.group(1)
    return None

found = {}
for c in first_cells:
    k = key_of(c)
    if k:
        found[k] = found.get(k, 0) + 1
missing = [i for i in items if found.get(i, 0) == 0]
dups = [i for i in items if found.get(i, 0) > 1]
extra = [k for k in found if k not in items]
print("missing:", missing)
print("more than once:", dups)
print("rows not in the allocation:", extra)
