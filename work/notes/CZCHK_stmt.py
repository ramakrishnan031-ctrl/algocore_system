"""CZ checker helper: print STUDY part statements / items by ID (reads algocore_system files only; imports nothing legacy).

Usage: python3 -I CZCHK_stmt.py P01-S075 P01-S080 ... (ranges: P01-S075:P01-S080)
"""
import re
import sys
from pathlib import Path

EV = Path("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/"
          "A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence")
FILES = {
    "P01": EV / "A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md",
    "P02": EV / "A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md",
    "P03": EV / "A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md",
    "P04": EV / "A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md",
    "P05": EV / "A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md",
    "P06": EV / "A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md",
    "P07": EV / "A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md",
}


def expand(arg):
    if ":" in arg:
        a, b = arg.split(":")
        pa, na = a.rsplit("-S", 1) if "-S" in a else a.rsplit("-U", 1)
        kind = "S" if "-S" in a else "U"
        nb = b.rsplit("-" + kind, 1)[1]
        width = len(na)
        return [f"{pa}-{kind}{str(i).zfill(width)}" for i in range(int(na), int(nb) + 1)]
    return [arg]


def find(sid, maxlen):
    part = sid[:3]
    text = FILES[part].read_text(encoding="utf-8")
    lines = text.splitlines()
    pat = re.compile(r"^\s*[-*]\s+\**" + re.escape(sid) + r"\b|^\|\s*" + re.escape(sid) + r"\b|\b" + re.escape(sid) + r"\b\s*[—:\-]")
    for i, ln in enumerate(lines):
        if pat.search(ln) and (ln.lstrip().startswith(("-", "*", "|")) or ln.lstrip().startswith(sid)):
            return f"[{part} L{i+1}] " + ln[:maxlen]
    return f"[{part}] {sid}: NOT FOUND"


if __name__ == "__main__":
    maxlen = 3000
    ids = []
    for a in sys.argv[1:]:
        if a.startswith("--max="):
            maxlen = int(a.split("=")[1])
            continue
        ids.extend(expand(a))
    for sid in ids:
        print(find(sid, maxlen))
        print()
