# FC checker: totals re-count and record-field check from the part file itself. Reads the FC part; writes nothing.
# Run: python3 -I <this>
import re, pathlib

FC = pathlib.Path("/home/claude/a08/parts/A08_AUDIT_PART_FC_2026-11-27.md")
t = FC.read_text(encoding="utf-8")
s3 = t.split("## 3. Issue and UNKNOWN records", 1)[1].split("## 4. Match records", 1)[0]
s4 = t.split("## 4. Match records", 1)[1].split("## 5. Handoffs", 1)[0]

recs = re.split(r"^##### ", s3, flags=re.M)[1:]
FIELDS = ["Area and flow", "Issue category", "Intended behaviour and source", "Actual code path",
          "Actual behaviour and effective value", "Evidence", "Result and classification",
          "Severity or impact where established", "Owner", "Cross-reference", "Rama"]
res = {}
for r in recs:
    rid = r.split(" ", 1)[0]
    head = r.splitlines()[0]
    if "Records observation" in head:
        res[rid] = "RECORDS OBSERVATION"
        continue
    m = re.search(r"- \*\*Result and classification:\*\* ([A-Z /]+?)(?:[ (.,;]|$)", r)
    first = m.group(1).strip() if m else "?"
    res[rid] = "UNKNOWN / NOT ESTABLISHED" if first.startswith("UNKNOWN") else first
    missing = [f for f in FIELDS if not re.search(r"- \*\*" + re.escape(f) + r"[^*]*:\*\*", r)]
    # FC-16 combines intended and actual in one field
    if rid == "FC-16":
        missing = [f for f in missing if f not in ("Intended behaviour and source", "Actual behaviour and effective value")]
        if not re.search(r"- \*\*Intended behaviour and source, and the actual behaviour:\*\*", r):
            missing.append("combined intended/actual field")
    if missing:
        print(rid, "missing fields:", missing)
for line in s4.splitlines():
    m = re.match(r"^\| (FC-\d\d) \|", line)
    if m:
        cells = line.split("|")
        res[m.group(1)] = "MATCH" if cells[-2].strip().startswith("MATCH") else "?(" + cells[-2].strip()[:20] + ")"
by = {}
for k, v in sorted(res.items()):
    by.setdefault(v, []).append(k)
for v, ids in by.items():
    print(f"{v}: {len(ids)}: {', '.join(ids)}")
ids = sorted(res)
print("IDs:", ids[0], "to", ids[-1], "count", len(ids))
kd_given = sorted(set(re.findall(r"(FC-\d\d)[^\n]{0,0}", "")))  # placeholder
for rid, r in [(r.split(' ', 1)[0], r) for r in recs]:
    if re.search(r"KNOWN DEFECT \(provisional\) for", r):
        print("KD (provisional) given in:", rid)
    if re.search(r"KNOWN DEFECT considered and not given|KNOWN DEFECT considered for", r):
        print("KD considered/not given in:", rid)
