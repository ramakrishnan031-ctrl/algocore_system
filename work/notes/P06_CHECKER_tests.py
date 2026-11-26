# P06 checker: tests/ files that match any top-level A08 name (word or substring), beyond the inventory's 26 (git grep only).
import re, subprocess
G = ["git", "-C", "/home/claude/repos/legacy"]
mods = ["sr_detector/" + m for m in ["__init__.py","confluence.py","detector.py","fetch.py","flags.py","models.py","pivots.py","retest_confirm.py","zone_builder.py","zone_cache.py","zone_warmer.py","zones.py"]] + ["screening/retest_monitor.py","scripts/sr_corp_action_spotcheck.py","scripts/sr_detector_backfill.py","scripts/sr_level_export.py"]
names = set()
for m in mods:
    for ln in subprocess.run(G + ["show", "970aabf:" + m], capture_output=True, text=True).stdout.split("\n"):
        q = re.match(r"^(?:class|def) ([A-Za-z_][A-Za-z0-9_]*)", ln) or re.match(r"^([A-Z][A-Z0-9_]{2,})\s*[:=]", ln)
        if q: names.add(q.group(1))
inv = set(l.strip() for l in open("/tmp/p06chk_inv7.txt"))
generic = {"main", "_attr", "_SENTINEL", "REJECT", "CONFIRMED", "evaluate", "Zone", "Candle", "Pivot", "_iso", "_json", "_row", "_is_long", "backfill"}
for mode in ("word", "substring"):
    hits = {}
    for n in sorted(names - generic):
        args = ["grep", "-l"] + (["-w"] if mode == "word" else []) + ["-F", n, "970aabf", "--", "tests"]
        for f in subprocess.run(G + args, capture_output=True, text=True).stdout.split():
            f = f.split(":", 1)[1]
            if f not in inv: hits.setdefault(f, set()).add(n)
    print(f"== {mode}: {len(hits)} files beyond the 26")
    for f in sorted(hits): print(f"  {f}: {', '.join(sorted(hits[f]))}")
