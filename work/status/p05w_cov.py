import re, sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
# statements: lines or table rows starting with P05-Snnn
ids = re.findall(r"(?m)^(?:- |\| )P05-S(\d{3}) ", t)
nums = [int(x) for x in ids]
print("statements:", len(nums), "first", min(nums), "last", max(nums))
missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
dups = sorted({n for n in nums if nums.count(n) > 1})
print("missing:", missing, "duplicates:", dups)
labels = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")
bad = []
for m in re.finditer(r"(?m)^(?:- |\| )P05-S(\d{3}) (.{0,40})", t):
    if not m.group(2).startswith(labels):
        bad.append(m.group(1))
print("bad labels:", bad)
defs = ["ScoreResult", "QualityScorer", "__init__", "score()", "_G2_CEILING_TRIPWIRE",
        "GATE_AT_CIRCUIT", "GATE_CIRCUIT_PROXIMITY", "GATE_STALE", "DEFAULT_FRESHNESS_MAX_SEC",
        "GateVerdict", "circuit_proximity_reason", "_pos_num", "HardGate", "evaluate",
        "rescaled_total", "tier_for", "rescale_min_score", "GATE_RR", "GATE_HTF", "GATE_EXTREME",
        "_is_long", "gate_rr", "gate_htf", "gate_extreme", "GATE_CONFIRM", "GATE_PULLBACK",
        "gate_confirm", "gate_pullback", "_screen_v3_enforce", "_log_v3_shadow_compare"]
print("definitions not named:", [d for d in defs if d not in t])
for q in ("Q8:", "Q9:", "Q17:"):
    print(q, "answered" if ("(" + q) in t else "MISSING")
for it in ("T-20", "K-27", "RD-12", "WA-06", "WA-07", "PQ-08"):
    print(it, "row" if re.search(r"\| P05-S1\d\d [^|]*\| A0\d " + re.escape(it), t) else "MISSING")
aps = re.findall(r"(?m)^- P05-AP(\d\d) ", t)
us = re.findall(r"(?m)^- P05-U(\d\d) ", t)
rs = re.findall(r"(?m)^- P05-R(\d) ", t)
print("APs", len(aps), "Us", len(us), "Rs", len(rs))
refs = sorted({int(x) for x in re.findall(r"P05-S(\d{3})", t)})
print("references beyond last:", [r for r in refs if r > max(nums)])
