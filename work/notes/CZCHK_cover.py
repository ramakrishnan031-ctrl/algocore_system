"""CZ checker (helper A7): coverage by script, totals by script, citation existence.
Reads only work-area files and algocore_system files; imports and reads nothing from the legacy clone.
Usage: python3 -I CZCHK_cover.py <part file>
Working material (D-17), not a record.
"""
import re
import sys
from pathlib import Path

PART = Path(sys.argv[1])
ALLOC = Path("/home/claude/a08/notes/AUDIT_ALLOCATION.md")
ISP = Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md")
ISL = Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md")
A08 = Path("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/"
           "A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT")
STUDY = A08 / "A08_STUDY_2026-11-26.md"
EV = {
    "P01": A08 / "evidence/A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md",
    "P02": A08 / "evidence/A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md",
    "P03": A08 / "evidence/A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md",
    "P04": A08 / "evidence/A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md",
    "P05": A08 / "evidence/A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md",
    "P06": A08 / "evidence/A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md",
    "P07": A08 / "evidence/A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md",
}

t = PART.read_text(encoding="utf-8")
body = t.split("## 10. Check log", 1)[0]          # the records, not the check log
alloc = ALLOC.read_text(encoding="utf-8")

# ---- 1. allocation coverage by script
items = [m.group(1).strip() for m in re.finditer(r"^\| ([^|]+?) \| CZ \| ", alloc, re.M)]
print("allocated to CZ:", len(items))
sec2 = body.split("## 2. Dispositions of the allocated items", 1)[1].split("## 3. Issue and UNKNOWN records", 1)[0]
cells = [m.group(1).strip() for m in re.finditer(r"^\| ([^|]+?) \|", sec2, re.M)]
cells = [c for c in cells if c not in ("Item", "Prior item", "Record") and not set(c) <= set("-: ")]
print("section 2 first cells:", len(cells))
print("  missing:", [i for i in items if i not in cells])
print("  extra:", [c for c in cells if c not in items])
print("  twice:", sorted({c for c in cells if cells.count(c) > 1}))

# ---- 2. inherited / listed quotes against STUDY 13.2 and 13.6
study = STUDY.read_text(encoding="utf-8")
for rid in ("A05 CM-10", "A05 HA-08", "A05 CM-01", "A05 CM-08", "A05 CM-12"):
    srow = [ln for ln in study.splitlines() if re.match(r"^\| (\d+ \| )?" + re.escape(rid) + r"\b", ln)]
    prow = [ln for ln in sec2.splitlines() if ln.startswith("| " + rid + " |")]
    if not srow or not prow:
        print(rid, "row not found", bool(srow), bool(prow))
        continue
    quotes = re.findall(r'"([^"]+)"', srow[0])
    miss = [q for q in quotes if q not in prow[0]]
    print(rid, "STUDY quotes:", len(quotes), "not in CZ row:", miss)

# ---- 3. records and totals
blocks = re.findall(r"^##### (CZ-\d\d) — ", body, re.M)
sec4 = body.split("## 4. Match records", 1)[1].split("## 5. Handoffs to other topics", 1)[0]
mrows = re.findall(r"^\| (CZ-\d\d) \| ", sec4, re.M)
ids = blocks + mrows
print("blocks", len(blocks), "match rows", len(mrows), "contiguous:", ids == ["CZ-%02d" % i for i in range(1, len(ids) + 1)],
      "dups:", sorted({i for i in ids if ids.count(i) > 1}))
res, kd = {}, {}
for b in blocks:
    seg = body.split("##### %s — " % b, 1)[1]
    seg = re.split(r"\n##### |\n## ", seg)[0]
    m = re.search(r"\*\*Result and classification:\*\* (ISSUE|UNKNOWN / NOT ESTABLISHED|MATCH|WITHDRAWN)", seg)
    res[b] = m.group(1) if m else "?"
    kd[b] = re.findall(r"KNOWN DEFECT (considered and not given|not considered|given|not applicable)", seg)
    for f in ("Area and flow", "Issue category", "Intended behaviour and source", "Actual code path",
              "Actual behaviour and effective value", "Evidence", "Result and classification",
              "Severity or impact where established", "Owner", "Cross-reference", "Rama"):
        if ("**" + f) not in seg:
            print("  field missing:", b, f)
for r in mrows:
    ln = [x for x in sec4.splitlines() if x.startswith("| %s |" % r)][0]
    cellsr = [c.strip() for c in ln.strip().strip("|").split("|")]
    res[r] = cellsr[-1].split(":")[0].split(" (")[0].split(".")[0]
    if len(cellsr) != 6:
        print("  match row cell count", r, len(cellsr))
counts = {}
for k in ids:
    counts[res[k]] = counts.get(res[k], 0) + 1
print("totals:", counts)
for k in blocks:
    print("  ", k, res[k], "| KD:", kd[k])
for k in mrows:
    print("  ", k, res[k])

# ---- 4. CZ references defined
refs = sorted(set(re.findall(r"\bCZ-\d\d\b", body)))
print("CZ refs undefined:", [r for r in refs if r not in ids])

# ---- 5. intent-source numbers cited exist
isp, isl = ISP.read_text(encoding="utf-8"), ISL.read_text(encoding="utf-8")
defined = set(re.findall(r"^\| ((?:IS|IC|CD|RS)-\d+)\b", isp, re.M)) | set(re.findall(r"^\| ((?:IS|IC|CD|RS)-\d+)\b", isl, re.M))
cited = set()
for m in re.finditer(r"(?<![A-Z0-9] )\b((?:IS|IC|CD|RS)-\d{2,3})\b", body):
    pre = body[max(0, m.start() - 4):m.start()]
    if re.search(r"A0\d $", pre):          # another topic's number, e.g. "A07 IS-955"
        continue
    cited.add(m.group(1))
# expand ranges "IS-512 to IS-524"
for a, b in re.findall(r"\b((?:IS|IC|CD|RS)-\d+) to ((?:IS|IC|CD|RS)-\d+)\b", body):
    pa, na = a.split("-"); pb, nb = b.split("-")
    if pa == pb:
        for n in range(int(na), int(nb) + 1):
            cited.add("%s-%0*d" % (pa, len(na), n))
undef = sorted(c for c in cited if c not in defined)
print("intent numbers cited:", len(cited), "undefined:", undef)

# ---- 6. part statements cited exist
evt = {k: v.read_text(encoding="utf-8") for k, v in EV.items()}
stm = set(re.findall(r"\b(P0\d-[SU]\d{2,3})\b", body))
for a, b in re.findall(r"\b(P0\d-[SU]\d+) to (P0\d-[SU]\d+)\b", body):
    if a[:5] == b[:5]:
        for n in range(int(a[5:]), int(b[5:]) + 1):
            stm.add("%s%0*d" % (a[:5], len(a) - 5, n))
missing = []
for s in sorted(stm):
    if not re.search(r"(^|\n)\s*[-|*]\s*\**\s*" + re.escape(s) + r"\b", evt[s[:3]]) and not re.search(r"\|\s*" + re.escape(s) + r"\s*\|", evt[s[:3]]):
        missing.append(s)
print("part statements cited:", len(stm), "not found as a statement:", missing)

# ---- 7. STUDY items cited exist
items_c = set(re.findall(r"\bA08-(?:AP|U|Q)-\d\d\b", body))
st_def = set(re.findall(r"\*\*(A08-(?:AP|U|Q)-\d\d)\*\*", study))
print("STUDY items cited:", len(items_c), "undefined:", sorted(i for i in items_c if i not in st_def))
