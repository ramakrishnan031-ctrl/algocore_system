# FC checker: every statement ID and STUDY item cited in the FC part exists where it should.
# Reads the FC part and the A08 STUDY files (algocore_system, read-only); writes nothing. Run: python3 -I <this>
import re, sys, pathlib

FC = pathlib.Path("/home/claude/a08/parts/A08_AUDIT_PART_FC_2026-11-27.md")
ST = pathlib.Path("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/"
                  "A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT")
EV = {
    "P01": "A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md",
    "P02": "A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md",
    "P03": "A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md",
    "P04": "A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md",
    "P05": "A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md",
    "P06": "A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md",
    "P07": "A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md",
}
fc = FC.read_text(encoding="utf-8")
study = (ST / "A08_STUDY_2026-11-26.md").read_text(encoding="utf-8")


def expand(text):
    """Pnn-Snnn and ranges 'Pnn-Saaa to Pnn-Sbbb'."""
    out = set()
    for m in re.finditer(r"(P\d\d)-S(\d{3})(?: to (?:P\d\d-S)?(\d{3}))?", text):
        p, a, b = m.group(1), int(m.group(2)), m.group(3)
        rng = range(a, (int(b) if b else a) + 1)
        for n in rng:
            out.add(f"{p}-S{n:03d}")
    return out


cited = expand(fc)
defined = {}
for p, f in EV.items():
    t = (ST / "evidence" / f).read_text(encoding="utf-8")
    defined[p] = set(re.findall(r"^\s*- \*\*(" + p + r"-S\d{3})\*\*", t, flags=re.M)) | \
        set(re.findall(r"^\s*- (" + p + r"-S\d{3})\b", t, flags=re.M)) | \
        set(re.findall(r"^\| (" + p + r"-S\d{3}) \|", t, flags=re.M))
missing = sorted(s for s in cited if s not in defined[s[:3]])
print("statement IDs cited:", len(cited), "; not found as a defined statement:", missing or "none")
for p in EV:
    print(" ", p, "defined:", len(defined[p]))

# STUDY items
for pat, name in ((r"A08-AP-\d\d", "A08-AP"), (r"A08-U-\d\d", "A08-U"), (r"A08-Q-\d\d", "A08-Q")):
    c = sorted(set(re.findall(pat, fc)))
    miss = [x for x in c if not re.search(r"\*\*" + x + r"\*\*|\| " + x + r" \|", study)]
    print(name, "cited:", len(c), "; not defined in the STUDY:", miss or "none")

# P02 unknowns cited (P02-Unn) and part points (P02-APnn, P06-APnn, P02-Rn)
for pat in (r"P0\d-U\d\d", r"P0\d-AP\d\d", r"P0\d-R\d"):
    c = sorted(set(re.findall(pat, fc)))
    miss = []
    for x in c:
        t = (ST / "evidence" / EV[x[:3]]).read_text(encoding="utf-8")
        if not re.search(re.escape(x) + r"\b", t):
            miss.append(x)
    print(pat, "cited:", c, "; not found in its part:", miss or "none")
