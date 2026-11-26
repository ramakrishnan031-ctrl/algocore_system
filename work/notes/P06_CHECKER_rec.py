# P06 checker: print an AUDIT record (heading to next heading) or table row by topic and ID (reads algocore files only)
import re, sys, glob
ROOT = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
maxc = int(sys.argv[1]); args = sys.argv[2:]
for a in args:
    topic, rid = a.split(":")
    f = glob.glob(f"{ROOT}/{topic}_*/{topic}_AUDIT_*.md")[0]
    L = open(f, encoding="utf-8").read().split("\n")
    head = re.compile(r"^#{3,6} " + re.escape(rid) + r" — ")
    row = re.compile(r"^\| *\**" + re.escape(rid) + r"\** *\|")
    done = False
    for i, l in enumerate(L):
        if head.match(l):
            j = i + 1
            while j < len(L) and not L[j].startswith("#"): j += 1
            print(f"== {topic} {rid} REC L{i+1}-L{j}")
            for k in range(i, j):
                if L[k].strip(): print(f"  L{k+1}: {L[k][:maxc]}")
            done = True; break
    for i, l in enumerate(L):
        if row.match(l):
            print(f"== {topic} {rid} ROW L{i+1}: {l[:maxc]}"); done = True
    if not done: print(f"== {topic} {rid} NOT FOUND")
