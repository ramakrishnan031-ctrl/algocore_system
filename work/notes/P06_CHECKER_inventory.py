# P06 checker: verify the A08 inventory's section 1 table, top-level contents and section 5 bytes against 970aabf
# (git show / ls-tree / log only; nothing from legacy code is imported or run). Reads the committed inventory (algocore, read-only).
import re, subprocess, hashlib
G = ["git", "-C", "/home/claude/repos/legacy"]
INV = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md"
inv = open(INV, encoding="utf-8").read().split("\n")
def run(a): return subprocess.run(G + a, capture_output=True, check=True).stdout
bad = 0
for l in inv[16:32]:
    c = [x.strip().strip("`") for x in l.strip("|").split("|")]
    p, lines, by, mode, blob, sha, ncom, last = c
    raw = run(["show", "970aabf:" + p])
    ls = run(["ls-tree", "970aabf", p]).decode().split()
    log = run(["log", "--format=%h %ad", "--date=short", "970aabf", "--", p]).decode().strip().split("\n")
    got = (str(raw.count(b"\n")), str(len(raw)), ls[0], ls[2], hashlib.sha256(raw).hexdigest(), str(len(log)), log[0].split()[0][:7] + ", " + log[0].split()[1])
    exp = (lines, by, mode, blob, sha, ncom, last)
    ok = got == exp
    bad += not ok
    print(("OK  " if ok else "DIFF") + f" {p}" + ("" if ok else f"\n   inv={exp}\n   got={got}"))
# top-level contents
tl = [l for l in inv if l.startswith("Top-level contents")][0]
for m in re.finditer(r"`([A-Za-z_0-9]+)` \(L(\d+)\)", tl):
    pass
mods = {"__init__.py":"sr_detector/__init__.py","models.py":"sr_detector/models.py","pivots.py":"sr_detector/pivots.py","zones.py":"sr_detector/zones.py","confluence.py":"sr_detector/confluence.py","flags.py":"sr_detector/flags.py","zone_builder.py":"sr_detector/zone_builder.py","fetch.py":"sr_detector/fetch.py","detector.py":"sr_detector/detector.py","zone_cache.py":"sr_detector/zone_cache.py","zone_warmer.py":"sr_detector/zone_warmer.py","retest_confirm.py":"sr_detector/retest_confirm.py","screening/retest_monitor.py":"screening/retest_monitor.py","sr_corp_action_spotcheck.py":"scripts/sr_corp_action_spotcheck.py","sr_detector_backfill.py":"scripts/sr_detector_backfill.py","sr_level_export.py":"scripts/sr_level_export.py"}
segs = re.split(r"; (?=`?(?:[a-z_]+/)?[a-z_]+\.py`?:|the scripts: )", tl.split("(FACT; `class` and `def` at column 0): ")[1])
tbad = 0
for s in segs:
    s = s.replace("the scripts: ", "")
    for part in re.split(r"; (?=`[a-z_]+\.py`)", s):
        mm = re.match(r"`([^`]+)`:? ?(.*)", part)
        if not mm: continue
        f = mods.get(mm.group(1)); 
        if not f: print("?? no module for", mm.group(1)); continue
        src = run(["show", "970aabf:" + f]).decode().split("\n")
        actual = {}
        for i, ln in enumerate(src):
            q = re.match(r"^(?:class|def) ([A-Za-z_][A-Za-z0-9_]*)", ln)
            if q: actual.setdefault(q.group(1), i + 1)
        for nm, ln in re.findall(r"`([A-Za-z_0-9]+)` \(L(\d+)\)", mm.group(2)):
            if actual.get(nm) != int(ln): tbad += 1; print(f"TOPLEVEL DIFF {f}: {nm} inv L{ln} got L{actual.get(nm)}")
        listed = set(re.findall(r"`([A-Za-z_0-9]+)` \(L\d+\)", mm.group(2)))
        unlisted = [n for n in actual if n not in listed]
        if unlisted: print(f"  {f}: not named individually: {', '.join(unlisted)}")
print("section 1 rows differing:", bad, "; top-level line differences:", tbad)
# section 5 bytes
for l in inv[103:117]:
    c = [x.strip() for x in l.strip("|").split("|")]
    paths = re.findall(r"`([^`]+)`", c[0]); sizes = [x.strip() for x in c[1].split(";")]
    for p, s in zip(paths, sizes):
        if s == "—" or p.endswith("/"): continue
        n = len(run(["show", "970aabf:" + p]))
        print(("OK  " if str(n) == s else "DIFF") + f" bytes {p}: inv {s} got {n}")
