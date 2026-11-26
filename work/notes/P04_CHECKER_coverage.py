"""P04 checker coverage script. Reads the two P04 legacy files as TEXT through `git show`
(no legacy module is imported or run) and the part file; checks that every def/class, every
module-level name and every branch line of the branch-heavy functions is cited in the part.
Usage: python3 -I P04_CHECKER_coverage.py"""
import re
import subprocess

LEGACY = "/home/claude/repos/legacy"
PART = "/home/claude/a08/parts/A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md"
FILES = ["sr_detector/retest_confirm.py", "screening/retest_monitor.py"]

part = open(PART, encoding="utf-8").read()


def show(path):
    return subprocess.run(["git", "-C", LEGACY, "show", "970aabf:" + path],
                          capture_output=True, text=True, check=True).stdout.split("\n")


def cited_lines(text):
    """Every L<n> and 'L<a> to L<b>' range cited in the text, as a set of line numbers."""
    s = set()
    for a, b in re.findall(r"L(\d+)(?: to L(\d+))?", text):
        a = int(a)
        b = int(b) if b else a
        if b >= a and b - a < 400:
            s.update(range(a, b + 1))
    return s


# statements that cite the two files: approximate by the sections 3 to 9 and 11 to 13 text
cites = cited_lines(part)

total = missing = 0
for f in FILES:
    src = show(f)
    print(f"== {f}: {len(src) - (1 if src[-1] == '' else 0)} lines")
    for i, ln in enumerate(src, 1):
        m = re.match(r"\s*(def|class)\s+(\w+)", ln)
        top = re.match(r"([A-Z_][A-Z_0-9]*)\s*=", ln)
        name = m.group(2) if m else (top.group(1) if top else None)
        if not name:
            continue
        total += 1
        named = ("`" + name + "`" in part) or (name + "(" in part) or (" " + name + " " in part)
        line_cited = i in cites
        ok = named and line_cited
        if not ok:
            missing += 1
        print(f"  L{i:<4} {('def/class ' + name) if m else ('name ' + name):40} named={named} line_cited={line_cited} {'OK' if ok else 'CHECK'}")
    # branch lines: if/elif/else/except/return/for/while
    br = [(i, ln.strip()) for i, ln in enumerate(src, 1)
          if re.match(r"\s*(if |elif |else:|except|return|for |while |try:)", ln)]
    unc = [(i, t) for i, t in br if i not in cites]
    print(f"  branch lines: {len(br)}; not covered by any cited line or range: {len(unc)}")
    for i, t in unc:
        print(f"    L{i}: {t[:90]}")
print(f"TOTAL names {total}; needing a look {missing}")
