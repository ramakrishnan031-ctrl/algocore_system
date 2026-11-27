"""Read-only completeness check of the ISA file (writes nothing)."""
import re, pathlib, collections
F = pathlib.Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md").read_text(encoding="utf-8")
S = pathlib.Path("/home/claude/a08/notes/ISA_study_items_index.md").read_text(encoding="utf-8")
lines = F.split("\n")
defs = collections.defaultdict(list)
for i, l in enumerate(lines, 1):
    m = re.match(r"^\| (IS-\d{3}|IC-\d{3}|RS-\d{2}) \|", l)
    if m: defs[m.group(1)].append(i)
for pref, n, w in (("IS", 95, 3), ("IC", 6, 3), ("RS", 23, 2)):
    want = [f"{pref}-{k:0{w}d}" for k in range(1, n + 1)]
    missing = [x for x in want if x not in defs]
    dup = [x for x in want if len(defs.get(x, [])) > 1]
    extra = sorted(k for k in defs if k.startswith(pref + "-") and k not in want)
    print(pref, "defined", sum(1 for x in want if x in defs), "missing", missing, "dup", dup, "extra", extra)
# cross refs (exclude earlier topics' IDs written with a topic prefix like "A05 IS-64", "A07 IC-004", "A07 RS-23")
refs = collections.Counter()
bad = []
for i, l in enumerate(lines, 1):
    for m in re.finditer(r"(?<![A-Za-z0-9-])(IS-\d{3}|IC-\d{3}|RS-\d{2})(?!\d)", l):
        pre = l[max(0, m.start() - 4):m.start()]
        if re.search(r"A0\d $", pre):  # earlier topic's own row ID
            continue
        if m.group(1) not in defs:
            bad.append((i, m.group(1), l[max(0, m.start()-40):m.end()+10]))
        refs[m.group(1)] += 1
print("undefined own-ID refs:", len(bad)); [print("  ", b) for b in bad[:30]]
# STUDY item refs
known = set(re.findall(r"^(A08-(?:AP|U|Q)-\d\d)", S, re.M))
used = set(re.findall(r"A08-(?:AP|U|Q)-\d\d", F))
print("STUDY item refs:", len(used), "unknown:", sorted(used - known))
# coverage of inherited items, entries, records, notes
items = set(int(x) for x in re.findall(r"\bitems? (\d+)", F)) | set(int(x) for y in re.findall(r"\bitems ([\d, and]+)", F) for x in re.findall(r"\d+", y))
entries = set(int(x) for x in re.findall(r"\bentry (\d+)", F)) | set(int(x) for y in re.findall(r"\bentries ([\d, toand]+)", F) for x in re.findall(r"\d+", y))
# expand "entries 13 to 15"
for a, b in re.findall(r"entries (\d+) to (\d+)", F): entries |= set(range(int(a), int(b)+1))
records = set(int(x) for x in re.findall(r"\brecord (\d+)", F)) | set(int(x) for y in re.findall(r"\brecords ([\d, and]+)", F) for x in re.findall(r"\d+", y))
notes = set(re.findall(r"\bN([1-6])\b", F))
print("items missing:", sorted(set(range(1, 49)) - items))
print("entries missing:", sorted(set(range(1, 17)) - entries))
print("records missing:", sorted(set(range(1, 17)) - records))
print("notes missing:", sorted(set("123456") - notes))
# 13.6 records by ID
records_list = ["A03 H-44","A03 U-59","A03 U-60","A01 C40","A02 K-32","A01 C3","A01 C18","A01 S-37","A02 L-08","A02 K-77","A03 Q-13","A03 Q-21","A03 Q-23","A03 U-10","A03 U-16","A03 J-14","A03 H-43","A04 CL-01","A04 CL-13","A04 RL-15","A05 CM-01","A05 CM-08","A05 CM-12","A05 HA-02","A05 HA-11","A05 HA-13","A05 IN-04","A05 IN-05","A05 IN-11","A05 IN-12","A05 XC-04","A05 XC-07","A06 XA-02","A06 EV-08","A06 EV-13","A06 ET-06","A07 EG-02","A03 H-10","A03 Q-52","A01 S-33","A02 L-12","A02 V-22","A02 L-33","A03 R-34","A05 CA-16","A06 EV-14","A06 XA-05","A07 XS-08","A06 PQ-06"]
missing_recs = []
for r in records_list:
    t, i = r.split()
    if not re.search(rf"\b{t} {re.escape(i)}\b", F) and not re.search(rf"\b{re.escape(i)}\b", F):
        missing_recs.append(r)
print("13.6 records:", len(records_list), "missing:", missing_recs)
