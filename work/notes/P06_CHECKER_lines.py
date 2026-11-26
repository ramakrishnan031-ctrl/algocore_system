# P06 checker: print a cited AUDIT line (topic, line) around a pattern (reads algocore files only)
import re, sys, glob
ROOT = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
cache = {}
for a in sys.argv[1:]:
    t, ln, pat = a.split("|", 2)
    if t not in cache: cache[t] = open(glob.glob(f"{ROOT}/{t}_*/{t}_AUDIT_*.md")[0], encoding="utf-8").read().split("\n")
    s = cache[t][int(ln) - 1]
    m = re.search(pat, s)
    if m: print(f"{t} L{ln}: ...{s[max(0, m.start()-150):m.end()+150]}...")
    else: print(f"{t} L{ln}: NO MATCH for {pat!r}; starts: {s[:160]}")
