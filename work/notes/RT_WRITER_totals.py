# RT writer: totals of the part file by result; KNOWN DEFECT statements; ID cross-checks.
# Reads workspace Markdown files only; imports nothing from the legacy clone; writes nothing.
import re

P = "/home/claude/a08/parts/A08_AUDIT_PART_RT_2026-11-27.md"
t = open(P, encoding="utf-8").read()
s3 = t[t.index("## 3. Issue and UNKNOWN records"):t.index("## 4. Match records")]
s4 = t[t.index("## 4. Match records"):t.index("## 5. Handoffs")]

blocks = re.split(r"(?=^##### RT-\d+)", s3, flags=re.M)
res = {"ISSUE": [], "UNKNOWN / NOT ESTABLISHED": [], "OBS": []}
kd_considered = []
kd_notconsidered = []
for b in blocks:
    m = re.match(r"##### (RT-\d+) — (.*)", b)
    if not m:
        continue
    rid, title = m.group(1), m.group(2)
    if title.startswith("Records observation"):
        res["OBS"].append(rid)
        continue
    r = re.search(r"^- \*\*Result and classification:\*\* (.*)$", b, flags=re.M)
    line = r.group(1) if r else ""
    if line.startswith("ISSUE"):
        res["ISSUE"].append(rid)
    elif line.startswith("UNKNOWN / NOT ESTABLISHED"):
        res["UNKNOWN / NOT ESTABLISHED"].append(rid)
    else:
        print("UNCLASSIFIED", rid, line[:60])
    if "KNOWN DEFECT considered" in line and "not given" in line:
        kd_considered.append(rid)
    elif "KNOWN DEFECT not considered" in line:
        kd_notconsidered.append(rid)
    if "KNOWN DEFECT (provisional)" in line and "not given" not in line:
        print("KD GIVEN?", rid)
match = re.findall(r"^\| (RT-\d+) \|", s4, flags=re.M)
print("ISSUE", len(res["ISSUE"]), res["ISSUE"])
print("UNKNOWN", len(res["UNKNOWN / NOT ESTABLISHED"]), res["UNKNOWN / NOT ESTABLISHED"])
print("MATCH", len(match), match)
print("OBS", res["OBS"])
print("KD considered not given", len(kd_considered), kd_considered)
print("KD not considered", kd_notconsidered)
allids = res["ISSUE"] + res["UNKNOWN / NOT ESTABLISHED"] + res["OBS"] + match
nums = sorted(int(x.split("-")[1]) for x in allids)
print("IDs", len(allids), "gaps:", [n for n in range(1, max(nums) + 1) if n not in nums], "dups:", len(nums) != len(set(nums)))

# every RT-nn referenced exists
refs = set(re.findall(r"\bRT-(\d+)\b", t))
missing = sorted(int(r) for r in refs if int(r) not in nums)
print("RT refs to missing IDs:", missing)

# every IS/IC/CD/RS number cited exists in one of the halves
H1 = open("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md", encoding="utf-8").read()
H2 = open("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md", encoding="utf-8").read()
defined = set(re.findall(r"^\| ((?:IS|IC|CD|RS)-\d+) \|", H1 + "\n" + H2, flags=re.M))
cited = set(re.findall(r"\b((?:IS|IC|CD|RS)-\d{2,3})\b", t))
# exclude earlier topics' numbers written with their topic ("A06 IS-83", "A05 IC-13", "A07's RS-11")
topic_written = set(re.findall(r"A0\d(?:'s)? ((?:IS|IC|CD|RS)-\d+)", t))
undefined = sorted(c for c in cited - defined if c not in topic_written)
print("cited intent IDs not defined in the halves:", undefined)
# A08 STUDY items cited
st = open("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/A08_STUDY_2026-11-26.md", encoding="utf-8").read()
items = set(re.findall(r"\bA08-(?:AP|U|Q)-\d+\b", t))
study_items = set(re.findall(r"\*\*(A08-(?:AP|U|Q)-\d+)\*\*", st))
print("A08 items cited but not in the STUDY:", sorted(items - study_items))
p04 = open("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence/A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md", encoding="utf-8").read()
sids = set(re.findall(r"\bP04-S\d{3}\b", t))
defined_s = set(re.findall(r"^- (P04-S\d{3})\b", p04, flags=re.M)) | set(re.findall(r"^\| (P04-S\d{3}) \|", p04, flags=re.M))
print("P04 statements cited but not defined:", sorted(sids - defined_s))
