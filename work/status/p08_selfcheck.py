"""P08 writer self-check (reads the P08 part file only; Markdown text; writes nothing).
Run: python3 -I -B /home/claude/a07/status/p08_selfcheck.py
"""
import re

P = "/home/claude/a07/parts/A07_CONFIGURATION_KEYS_AND_EFFECTIVE_VALUES_2026-11-21.md"
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")
Q9 = ("What are the exact thresholds, units, formulae, weights, score aggregation, rounding and "
      "boundary conditions? Trace configured values to effective runtime values; do not assume "
      "configuration is used as declared.")
ITEMS = ["C11", "V-06", "T-14", "T-20", "F-11", "K-05", "K-27", "OA-22", "CG-05"]

text = open(P, encoding="utf-8").read()
lines = text.splitlines()
ids = []
bad_label = []
for ln in lines:
    m = re.match(r"^- (P08-S(\d{3})) (.*)$", ln)
    if m:
        ids.append(int(m.group(2)))
        rest = m.group(3)
        if not rest.startswith(LABELS):
            bad_label.append(m.group(1))
dups = sorted({i for i in ids if ids.count(i) > 1})
expected = list(range(1, max(ids) + 1)) if ids else []
missing = sorted(set(expected) - set(ids))
print("statements:", len(ids), "max:", max(ids) if ids else None)
print("duplicates:", dups, "missing:", missing)
print("statements without a valid leading label:", bad_label)
print("Q9 full wording present:", Q9 in text)
sec10 = text.split("## 10. Inherited items")[1].split("## 11.")[0]
for it in ITEMS:
    print(f"item {it} in section 10:", it in sec10)
print("ADDENDUM 2 record A02 AUDIT L1320 cited:", "A02 AUDIT L1320" in text)
aps = re.findall(r"^- (P08-AP\d{2}) ", text, flags=re.M)
us = re.findall(r"^- (P08-U\d{2}) ", text, flags=re.M)
rs = re.findall(r"^- (P08-R\d) ", text, flags=re.M)
print("Points for the AUDIT:", len(aps), aps[:1], aps[-1:])
print("UNKNOWN items:", len(us))
print("Questions for Rama:", len(rs))
# cited statement IDs that do not exist in this file
cited = set(int(x) for x in re.findall(r"P08-S(\d{3})", text))
print("cited P08 IDs not defined:", sorted(cited - set(ids)))
heads = [l for l in lines if l.startswith("## ")]
print("sections:", len(heads))
for h in heads:
    print("  ", h)
