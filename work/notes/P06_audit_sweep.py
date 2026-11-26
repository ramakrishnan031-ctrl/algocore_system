# P06 writer: sweep of the approved A01-A07 AUDIT files for records touching A08 code without naming A08.
# Reads algocore_system files only (read-only). Prints candidate records.
import re, sys, glob, os
ROOT = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
files = sorted(glob.glob(ROOT + "/A0[1-7]_*/A0[1-7]_AUDIT_*.md"))
names = [r"sr_detector", r"retest_monitor", r"RetestMonitor", r"RetestDiverter", r"ParkedCandidate",
         r"ZoneCache", r"ZoneWarmer", r"ZoneSet", r"OhlcFetcher", r"retest_confirm", r"RetestParams",
         r"_strong_close", r"build_sr_detector", r"SRDetector", r"ScoredZone", r"find_swing_pivots",
         r"scored_zones_from_candles", r"split_zones", r"build_zone_knobs", r"build_scoring_params",
         r"CONF_ANCHOR_ONLY", r"from_kite", r"`Candle`", r"Candle\b", r"zone_builder", r"zone_warmer",
         r"zone_cache", r"sr_level_export", r"sr_corp_action_spotcheck", r"retest_state",
         r"fetch_timeframes", r"fetch_interval", r"fetch_by_token", r"_sr_observe", r"_make_sr_fetch_fn",
         r"_build_market_data_kite", r"wait_for_retest", r"structure_exit_enabled", r"intraday_anchors"]
pat = re.compile("|".join(names))
head = re.compile(r"^#{4,5} ([A-Z]{1,3}-?\d+[a-z]?) — ")
row = re.compile(r"^\| *([A-Z]{1,3}-\d+[a-z]?|C\d+[a-z]?) *\|")
excl = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else set()
for f in files:
    topic = os.path.basename(f)[:3]
    lines = open(f, encoding="utf-8").read().split("\n")
    # records by heading
    starts = [(i, head.match(l).group(1)) for i, l in enumerate(lines) if head.match(l)]
    for k, (i, rid) in enumerate(starts):
        j = starts[k+1][0] if k+1 < len(starts) else len(lines)
        # stop at next heading of level <=5
        for t in range(i+1, j):
            if lines[t].startswith("#"):
                j = t; break
        body = "\n".join(lines[i:j])
        hits = sorted(set(m.group(0) for m in pat.finditer(body)))
        if hits and "A08" not in body and f"{topic} {rid}" not in excl:
            print(f"REC\t{topic}\t{rid}\tL{i+1}-L{j}\t{','.join(hits)}")
    for i, l in enumerate(lines):
        m = row.match(l)
        if m and not head.match(l):
            hits = sorted(set(x.group(0) for x in pat.finditer(l)))
            if hits and "A08" not in l and f"{topic} {m.group(1)}" not in excl:
                print(f"ROW\t{topic}\t{m.group(1)}\tL{i+1}\t{','.join(hits)}")
