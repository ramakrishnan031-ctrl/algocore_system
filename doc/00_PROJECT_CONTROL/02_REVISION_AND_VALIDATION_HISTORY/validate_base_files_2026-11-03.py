"""Validate the ten project base files (Revision 1 or 2): names, headers, format, cross-references, terms,
labels and secrets.
Usage: python3 validate_base_files.py <folder holding the ten .md files>. Exit 0 = all checks pass, 1 = a failure."""
import re
import sys
from pathlib import Path

DIR = Path(sys.argv[1])
NAMES = [
    "01_PROJECT_FOUNDATION_AND_SCOPE_2026-11-03.md",
    "02_PROJECT_PHASES_AND_MASTER_WORKFLOW_2026-11-03.md",
    "03_AI_ROLES_RESPONSIBILITIES_AND_OPERATING_INSTRUCTIONS_2026-11-03.md",
    "04_TOPIC_INVESTIGATION_WORKFLOW_AND_AI_CONTINUITY_PROTOCOL_2026-11-03.md",
    "05_PROJECT_GOVERNANCE_AND_DECISION_CONTROL_2026-11-03.md",
    "06_TECHNICAL_ENVIRONMENT_TOOLS_AND_RESEARCH_SOURCES_2026-11-03.md",
    "07_REPOSITORY_DOCUMENTATION_AND_RECORD_MANAGEMENT_2026-11-03.md",
    "08_LEGACY_STUDY_AND_AUDIT_METHODOLOGY_2026-11-03.md",
    "09_NEW_SYSTEM_DESIGN_AND_DEVELOPMENT_FRAMEWORK_2026-11-03.md",
    "10_MASTER_PROJECT_INDEX_AND_CONTROL_REGISTERS_2026-11-03.md",
]
fails = []
results = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    results.append(msg)
    if not cond:
        fails.append(msg)

present = sorted(p.name for p in DIR.glob("*.md"))
check(present == sorted(NAMES), f"V1 exactly the ten required file names present ({len(present)} .md files)")

texts, sections = {}, {}
for n in NAMES:
    raw = (DIR / n).read_bytes()
    t = raw.decode("utf-8")
    texts[n[:2]] = t
    fmt = (b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") and not raw.endswith(b"\n\n")
           and not any(l.endswith(" ") for l in t.split("\n")))
    check(fmt, f"V2 {n[:2]} UTF-8, LF only, no tabs, no trailing spaces, single final newline")
    hdr = t.split("\n")[0].startswith(f"# {n[:2]} — ") and re.search(r"\*\*Status:\*\* DRAFT — Revision [12]", t) is not None and "**Date:** 2026-11-03" in t and "**Revision history:**" in t
    check(hdr, f"V3 {n[:2]} title, status (Revision 1 or 2), date and revision history present")
    secs = set()
    nums = []
    for line in t.split("\n"):
        m = re.match(r"^## (\d+)\. ", line)
        if m:
            secs.add(m.group(1)); nums.append(int(m.group(1)))
        m = re.match(r"^### (\d+\.\d+) ", line)
        if m:
            secs.add(m.group(1))
    sections[n[:2]] = secs
    check(nums == list(range(1, len(nums) + 1)), f"V4 {n[:2]} top-level sections numbered 1..{len(nums)} without gaps")
    check("\\&" not in t and not re.search(r"\d\\\.", t), f"V5 {n[:2]} no leftover Markdown escapes (\\& or 1\\.)")

# cross-references
bad = []
count = 0
for d, t in texts.items():
    for m in re.finditer(r"Document (\d\d), sections? ([\d.]+)(?: and ([\d.]+))?", t):
        for s in (m.group(2), m.group(3)):
            if s:
                count += 1
                s = s.rstrip(".")
                if s not in sections.get(m.group(1), set()):
                    bad.append(f"{d}: Document {m.group(1)}, section {s}")
    for m in re.finditer(r"(?<!Document \d\d, )(?<![\w,] )\bsection (\d+(?:\.\d+)?)\b", t):
        pre = t[max(0, m.start() - 20):m.start()]
        if re.search(r"Document \d\d, $", pre) or "sections" in pre[-10:]:
            continue
        count += 1
        if m.group(1) not in sections[d]:
            bad.append(f"{d}: own section {m.group(1)}")
    for m in re.finditer(r"\b(\d\d) §(\d+(?:\.\d+)?)(?: and §(\d+(?:\.\d+)?))?", t):
        for s in (m.group(2), m.group(3)):
            if s:
                count += 1
                if s not in sections.get(m.group(1), set()):
                    bad.append(f"{d}: {m.group(1)} §{s}")
    for m in re.finditer(r"; (\d\d) §(\d+(?:\.\d+)?)", t):
        pass
    rel = re.search(r"\*\*(?:Related documents|Mandatory cross-reference):\*\*(.*)", t)
    check(rel is not None, f"V6 {d} has a related-documents line")
    if rel:
        for r in re.findall(r"\b(\d\d)\b", rel.group(1)):
            count += 1
            if r not in texts:
                bad.append(f"{d}: related document {r}")
check(not bad, f"V7 all {count} cross-references resolve to an existing document and section" + (f": {bad}" if bad else ""))

alltext = "\n".join(texts.values())
# terms
check(not re.search(r"sandbox|duplicate/sandbox|duplicate copy", alltext, re.I), "V8 no 'sandbox'/'duplicate copy' study method left (replaced by the read-only clone)")
check(not re.search(r"algocore[ -]system|algocore_systems|AlgoCore", alltext), "V9 algocore_system spelled one way only")
check(len(re.findall(r"algocore_system", alltext)) >= 8, "V9b algocore_system named in the repository, publication and open-item sections")
check(not re.search(r"visibility.*remains OPEN|strategy after Phase 1 remains OPEN", alltext), "V10 settled repository visibility no longer shown as OPEN")
check(not re.search(r"Phase 0|Phase-1|Phase-2|Phase-3|Pre Phase|Prephase", alltext), "V11 phase names consistent (Pre-Phase, Phase 1, Phase 2, Phase 3)")
labels = "RETAIN / REVISE / UPGRADE / REPLACE / REJECT / NEW"
lab09 = re.findall(r"^- (RETAIN|REVISE|UPGRADE|REPLACE|REJECT|NEW)\.$", texts["09"], re.M)
check(labels in texts["02"] and " / ".join(lab09) == labels, "V12 the six Phase 2 outcome labels identical in 02 section 4 and 09 section 2")
ev04 = re.findall(r"^- (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|KNOWN DEFECT|OPEN QUESTION) —", texts["04"], re.M)
ev08 = re.findall(r"^- (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|KNOWN DEFECT|OPEN QUESTION)\.$", texts["08"], re.M)
check(ev04 == ev08 and len(ev04) == 6, "V13 the six evidence classifications identical in 04 section 6 and 08 section 7")
seq_terms = ["study", "audit", "reconciliation", "proposal", "retain", "freeze", "code"]
check(all(s in texts["01"].split("## 5.")[1].split("## 6.")[0].lower() for s in seq_terms), "V14 approved sequence complete in 01 section 5")
check(all(k in texts["02"].split("## 1.")[1].split("## 2.")[0].lower() for k in seq_terms), "V15 approved sequence mapped completely in 02 section 1")
# intended-vs-actual whole-system audit rule referenced wherever it applies
refs = {d: ("Document 04, section 5" in t) for d, t in texts.items()}
check(all(refs[d] for d in ["01", "02", "03", "08", "09"])
      and "## 5. Intended and actual behaviour — the whole-system audit" in texts["04"]
      and "### 5.1 The rule" in texts["04"],
      "V16 intended-vs-actual whole-system audit rule stated once (04 section 5) and referenced from 01, 02, 03, 08, 09")
s52 = texts["04"].split("### 5.2")[1].split("### 5.3")[0]
areas = ["signals", "capital", "order management", "alerts", "market data", "reconciliation", "kill switch", "failure and recovery"]
check("entire system" in s52 and "one illustration of the kind of problem, not its limit" in s52 and all(a in s52 for a in areas)
      and "never limit the audit to configuration settings" in texts["04"],
      "V17 audit rule scoped to the entire system (all areas and flows), stop-loss shown as one illustration only")
narrow = [r"comparison of configured and documented", r"configured and documented behaviour with actual",
          r"Configured or documented value and its source", r"for every item in the topic", r"Comparing configured"]
left = [p for p in narrow if re.search(p, alltext)]
check(not left, "V23 no Revision 1 wording left that limits the audit to configuration items" + (f": {left}" if left else ""))
check("05-Oct-2026" in texts["06"] and "Document 06, section 4.2" in texts["04"] and "Document 06, section 4.2" in texts["08"], "V18 runtime limitation stated once (06 section 4.2) and referenced from 04 and 08")
check("## 10. Review-round control" in texts["05"], "V19 review-round control present (05 section 10)")
# OPEN FOR RAMA items all listed in 10 section 11
ofr = {d: t.count("OPEN FOR RAMA") for d, t in texts.items() if "OPEN FOR RAMA" in t}
oi = re.findall(r"^\| (OI-\d\d) \|", texts["10"], re.M)
check(oi == [f"OI-{i:02d}" for i in range(1, 8)], f"V20 open-items table OI-01..OI-07 in 10 section 11; OPEN FOR RAMA occurrences per file: {ofr}")
# secrets / identifiers
pat = [r"\b\d{1,3}(?:\.\d{1,3}){3}\b", r"LFL\d{3}", r"(?i)(api[_-]?key|secret|token|password|totp)\s*[:=]\s*\S", r"\b[A-Za-z0-9]{32,}\b", r"/home/ubuntu", r"[A-Z]:\\\\"]
hits = [p for p in pat if re.search(p, alltext)]
check(not hits, "V21 no credential value, IP address, account identifier, long key-like string or machine path" + (f": {hits}" if hits else ""))
check("Claude-Session" not in alltext and "claude.ai/code" not in alltext, "V22 no session link")
# revision histories consistent with each file's status, and 10's open-items heading with 10's status
bad_hist = []
for d, t in texts.items():
    rev = int(re.search(r"\*\*Status:\*\* DRAFT — Revision (\d)", t).group(1))
    hist = re.search(r"\*\*Revision history:\*\*(.*)", t).group(1)
    named = sorted({int(x) for x in re.findall(r"Revision (\d), 2026-11-03:", hist)})
    if named != list(range(1, rev + 1)):
        bad_hist.append(f"{d}: status Revision {rev}, history names {named}")
oi_head = re.search(r"^## 11\. Open items at Revision (\d)$", texts["10"], re.M)
rev10 = re.search(r"\*\*Status:\*\* DRAFT — Revision (\d)", texts["10"]).group(1)
if not oi_head or oi_head.group(1) != rev10:
    bad_hist.append(f"10: open-items heading revision {oi_head.group(1) if oi_head else None}, status Revision {rev10}")
check(not bad_hist, "V24 each revision history names every revision up to the file's status, and 10 section 11's heading "
      "matches 10's revision" + (f": {bad_hist}" if bad_hist else ""))
print(f"\nCHECKS RUN: {len(results)}")
print(f"\nRESULT: {'PASS' if not fails else 'FAIL'} ({len(fails)} failed)")
sys.exit(1 if fails else 0)
