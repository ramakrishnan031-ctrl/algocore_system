"""P03 checker: coverage test BY SCRIPT (text only).

Usage: python3 -I P03_CHECKER_coverage.py <part file> <dir with git-show text files>
The text files are produced by `git show 970aabf:<path>` and named with '/' replaced by '__'.
This script imports nothing from the legacy code and executes none of it; it reads text only.
"""
import os
import re
import sys

part_path, src_dir = sys.argv[1], sys.argv[2]
part = open(part_path, encoding="utf-8").read()
FILES = ["sr_detector/__init__.py", "sr_detector/detector.py", "sr_detector/flags.py",
         "scripts/sr_detector_backfill.py"]


def load(path):
    with open(os.path.join(src_dir, path.replace("/", "__")), encoding="utf-8") as fh:
        return fh.read().splitlines()


total = missing = 0
print("== 1. every def/class and module-level name, and whether the part names it")
for f in FILES:
    lines = load(f)
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^(\s*)(def|class)\s+(\w+)", ln)
        if m:
            total += 1
            name = m.group(3)
            ok = ("`" + name in part) or ("." + name in part) or (name + "`" in part)
            missing += 0 if ok else 1
            print(f"  {'OK ' if ok else 'MISSING'} {f} L{i} {m.group(2)} {name}")
        m2 = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=", ln)
        if m2:
            total += 1
            name = m2.group(1)
            ok = name in part
            missing += 0 if ok else 1
            print(f"  {'OK ' if ok else 'MISSING'} {f} L{i} constant {name}")
print(f"  defs/classes/constants: {total}; not named in the part: {missing}")

print("== 2. argparse options of the script")
for i, ln in enumerate(load("scripts/sr_detector_backfill.py"), 1):
    m = re.search(r'add_argument\(\s*"([^"]+)"', ln)
    if m:
        opt = m.group(1)
        ok = f"`{opt}`" in part
        print(f"  {'OK ' if ok else 'MISSING'} L{i} {opt}")

print("== 3. external calls (attribute calls on injected collaborators, imports inside functions)")
pat = re.compile(r"self\._(store|fetcher|fx_write|log|now_fn|q|worker|stop)\.(\w+)\(|store\.(\w+)\(|"
                 r"(skip_if_non_trading_day|StateStore|now_ist|datetime\.now|json\.dumps|mean|"
                 r"threading\.Thread|queue\.Queue|_effect_handle|build_\w+|intraday_anchors|"
                 r"scored_zones_from_candles|compute_flags_and_retest|OhlcFetcher|SRDetector)\(")
seen = {}
for f in FILES:
    for i, ln in enumerate(load(f), 1):
        for m in pat.finditer(ln):
            call = m.group(0).rstrip("(")
            seen.setdefault((f, call), []).append(i)
for (f, call), lns in sorted(seen.items()):
    key = call.split(".")[-1]
    ok = key in part
    print(f"  {'OK ' if ok else 'MISSING'} {f} {call} at L{','.join(map(str, lns))}")

print("== 4. branch-heavy functions (if/elif/else/except/for/while/ternary/and-or count)")
for f in FILES:
    lines = load(f)
    cur, start, count = None, 0, 0
    out = []
    for i, ln in enumerate(lines + ["def __end__():"], 1):
        m = re.match(r"^\s*def\s+(\w+)", ln)
        if m:
            if cur:
                out.append((cur, start, i - 1, count))
            cur, start, count = m.group(1), i, 0
            continue
        s = ln.strip()
        if s.startswith("#"):
            continue
        count += len(re.findall(r"\b(if|elif|else|except|for|while)\b", s))
    for name, a, b, c in out:
        if c >= 3:
            print(f"  {f} {name} L{a} to L{b}: {c} branch keywords")
