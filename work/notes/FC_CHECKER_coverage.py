# FC checker: allocation coverage by script. Reads the allocation note and the FC part; writes nothing.
# Run: python3 -I <this> [fc_file]
import re, sys, pathlib

ALLOC = pathlib.Path("/home/claude/a08/notes/AUDIT_ALLOCATION.md")
FC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/a08/parts/A08_AUDIT_PART_FC_2026-11-27.md")

items = []
for line in ALLOC.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\| ([^|]+?) \| FC \| ", line)
    if m:
        items.append(m.group(1).strip())
print("allocation rows for FC:", len(items))

fc = FC.read_text(encoding="utf-8")
sec2 = fc.split("## 2. Dispositions of the allocated items", 1)[1].split("## 3. Issue and UNKNOWN records", 1)[0]
first_cells = []
for line in sec2.splitlines():
    if line.startswith("| ") and not line.startswith("|---"):
        cell = line.split("|")[1].strip()
        if cell in ("Item", "Prior item", "Entry", "Record", "Note"):
            continue
        first_cells.append(cell)


def norm(cell):
    cell = re.sub(r"\s*\(.*\)$", "", cell)        # "A05-01 (CM-07)" -> "A05-01"
    if cell in ("N2", "N3"):
        cell = "note " + cell
    return cell


counts = {}
for c in first_cells:
    counts[norm(c)] = counts.get(norm(c), 0) + 1
missing = [i for i in items if counts.get(i, 0) == 0]
dupl = {k: v for k, v in counts.items() if v > 1}
extra = [k for k in counts if k not in items]
print("disposition rows in section 2:", len(first_cells))
print("missing:", missing or "none")
print("more than one row:", dupl or "none")
print("rows not allocated to FC:", extra or "none")

# Each disposition row names at least one FC record
bad = []
for line in sec2.splitlines():
    if line.startswith("| ") and not line.startswith("|---"):
        cell = line.split("|")[1].strip()
        if cell in ("Item", "Prior item", "Entry", "Record", "Note"):
            continue
        if not re.search(r"FC-\d\d", line.split("|")[-2]):
            bad.append(cell)
print("rows whose Records cell names no FC record:", bad or "none")
