# P06 checker: print the text of statement IDs from the A08 part files (reads workspace parts only)
import re, sys, glob
parts = {
 "P01": "A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md",
 "P02": "A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md",
 "P03": "A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md",
 "P04": "A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md",
 "P05": "A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md",
 "P06": "A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md",
 "P07": "A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md",
}
cache = {}
def lines(p):
    if p not in cache:
        cache[p] = open("/home/claude/a08/parts/" + parts[p], encoding="utf-8").read().split("\n")
    return cache[p]
maxlen = int(sys.argv[1]) if sys.argv[1].isdigit() else 600
ids = sys.argv[2:] if sys.argv[1].isdigit() else sys.argv[1:]
for sid in ids:
    p = sid[:3]
    pat = re.compile(r"(^- \*{0,2}" + re.escape(sid) + r"\b)|(^\| *" + re.escape(sid) + r" *\|)|(^#+ .*\b" + re.escape(sid) + r"\b)")
    found = False
    for i, l in enumerate(lines(p)):
        if pat.search(l):
            print(f"[{sid} @L{i+1}] {l[:maxlen]}"); found = True; break
    if not found:
        # fallback: first line where the ID starts a bullet-like or appears as a definition
        for i, l in enumerate(lines(p)):
            if re.search(r"\b" + re.escape(sid) + r"\b", l) and (l.startswith("- ") or l.startswith("|")):
                print(f"[{sid} ~@L{i+1}] {l[:maxlen]}"); found = True; break
    if not found: print(f"[{sid}] NOT FOUND")
