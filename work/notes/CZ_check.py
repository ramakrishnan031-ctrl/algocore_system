"""CZ scratch check (A08 AUDIT part CZ): counts results by record, checks the
allocation coverage of section 2 and the record IDs. Reads only the part file and
the allocation note in the work area; reads and imports nothing from either clone.
Working material (D-17), not kept as a record."""
import re
import sys

PART = sys.argv[1]
ALLOC = sys.argv[2]
text = open(PART, encoding="utf-8").read()
alloc = open(ALLOC, encoding="utf-8").read()

# 1. allocation rows for CZ
cz_items = re.findall(r"^\| (.+?) \| CZ \| ", alloc, flags=re.M)
cz_items = [i for i in cz_items if i != "Part"]
print("allocated CZ items:", len(cz_items))

# 2. section 2 first cells
sec2 = text.split("## 2. Dispositions of the allocated items", 1)[1].split("## 3. Issue and UNKNOWN records", 1)[0]
first_cells = re.findall(r"^\| ([^|]+?) \| ", sec2, flags=re.M)
first_cells = [c.strip() for c in first_cells if c.strip() not in ("Item", "Prior item", "Record", "---")]
missing = [i for i in cz_items if i not in first_cells]
extra = [c for c in first_cells if c not in cz_items]
dups = sorted({c for c in first_cells if first_cells.count(c) > 1})
print("section 2 rows:", len(first_cells), "missing:", missing, "extra:", extra, "duplicates:", dups)

# 3. records: issue/unknown blocks and match rows
blocks = re.findall(r"^##### (CZ-\d\d) — ", text, flags=re.M)
sec4 = text.split("## 4. Match records", 1)[1].split("## 5. Handoffs to other topics", 1)[0]
rows = re.findall(r"^\| (CZ-\d\d) \| ", sec4, flags=re.M)
ids = blocks + rows
print("blocks:", len(blocks), "match rows:", len(rows), "ids defined:", len(ids),
      "duplicates:", sorted({i for i in ids if ids.count(i) > 1}))
expected = ["CZ-%02d" % n for n in range(1, len(ids) + 1)]
print("contiguous from CZ-01:", ids == expected)

res = {}
for b in blocks:
    body = text.split("##### %s — " % b, 1)[1].split("\n##### ", 1)[0].split("\n## ", 1)[0]
    m = re.search(r"\*\*Result and classification:\*\* (ISSUE|UNKNOWN / NOT ESTABLISHED|MATCH)", body)
    res[b] = m.group(1) if m else "?"
    kd = re.search(r"KNOWN DEFECT (considered and not given|not considered|given)", body)
    res[b] += " | KD: " + (kd.group(1) if kd else "none stated")
for r in rows:
    line = [l for l in sec4.splitlines() if l.startswith("| %s |" % r)][0]
    last = line.rstrip("|").split("|")[-1]
    res[r] = "MATCH" if last.strip().startswith("MATCH") else "?" + last[:40]
for k in ids:
    print("  ", k, res[k])
counts = {}
for k in ids:
    key = res[k].split(" |")[0]
    counts[key] = counts.get(key, 0) + 1
print("counts:", counts)
kd_cons = [k for k in blocks if "considered and not given" in res[k]]
kd_not = [k for k in blocks if "not considered" in res[k]]
print("KNOWN DEFECT considered and not given:", kd_cons)
print("KNOWN DEFECT not considered (first statement):", kd_not)

# 4. every CZ-nn referenced exists
refs = sorted(set(re.findall(r"\bCZ-\d\d\b", text)))
print("referenced but undefined:", [r for r in refs if r not in ids])

# 5. which records each allocated item names in section 2
for item in cz_items:
    line = [l for l in sec2.splitlines() if l.startswith("| %s |" % item)]
    recs = sorted(set(re.findall(r"\bCZ-\d\d\b", line[0]))) if line else []
    print("   %-10s -> %s" % (item, ", ".join(recs) if recs else "NONE"))
