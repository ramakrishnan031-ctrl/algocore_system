# P06 checker: every top-level class/def/CONSTANT of the 13 A08 modules (text parsing of git show; nothing imported),
# then git grep -w each name over the whole tree (four exclusions), listing non-A08, non-test, non-doc files that use it.
import re, subprocess, collections
G = ["git", "-C", "/home/claude/repos/legacy"]
X = [":(exclude)config/accounts.csv", ":(exclude,glob)**/.env*", ":(exclude,glob)**/*.local.yaml", ":(exclude,glob)**/*token*.json"]
mods = ["sr_detector/" + m for m in ["__init__.py","confluence.py","detector.py","fetch.py","flags.py","models.py","pivots.py","retest_confirm.py","zone_builder.py","zone_cache.py","zone_warmer.py","zones.py"]] + ["screening/retest_monitor.py"]
names = collections.OrderedDict()
for m in mods:
    src = subprocess.run(G + ["show", "970aabf:" + m], capture_output=True, text=True, check=True).stdout
    for ln in src.split("\n"):
        mm = re.match(r"^(?:class|def) ([A-Za-z_][A-Za-z0-9_]*)", ln) or re.match(r"^([A-Z][A-Z0-9_]{2,})\s*[:=]", ln)
        if mm: names.setdefault(mm.group(1), m)
A08 = re.compile(r"^(sr_detector/|screening/retest_monitor\.py|scripts/sr_(corp_action_spotcheck|detector_backfill|level_export)\.py)")
skip = re.compile(r"^(tests/|docs/|ops_dashboard/tests/)|\.md$|\.txt$")
generic = {"_attr", "_SENTINEL", "main"}
uses = collections.defaultdict(set)
for n, m in names.items():
    if n in generic: continue
    out = subprocess.run(G + ["grep", "-n", "-w", "-I", n, "970aabf", "--"] + X, capture_output=True, text=True).stdout
    for l in out.split("\n"):
        if not l: continue
        f = l.split(":", 2)[1]
        if A08.match(f) or skip.search(f): continue
        uses[f].add(n)
print("names:", len(names), "->", ", ".join(names))
for f in sorted(uses): print(f"{f}\t{', '.join(sorted(uses[f]))}")
