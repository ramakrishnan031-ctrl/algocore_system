"""ISA checker: read-only Open Issues Register entry printer (Markdown only; writes nothing).
Usage: python3 -I ISACHK_oir.py A05-27 A05-28 ... [w=600] [f=Question,Owner,Status,Resolution]"""
import re, sys, pathlib
P = pathlib.Path("/home/claude/algocore_system/doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/OPEN_ISSUES_REGISTER_2026-11-05.md")
L = P.read_text(encoding="utf-8").split("\n")
W = int(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("w=")), "600"))
FL = next((a.split("=")[1].split(",") for a in sys.argv[1:] if a.startswith("f=")), ["Question", "Owner", "Raised", "Status", "Resolution"])
for arg in sys.argv[1:]:
    if "=" in arg: continue
    idx = [i for i, l in enumerate(L) if re.match(r"^### " + re.escape(arg) + r"\b", l)]
    print(f"######## {arg}: heading at {[i + 1 for i in idx]}")
    if not idx: continue
    i = idx[0]
    print(f"  L{i + 1}: {L[i][:250]}")
    j = i + 1
    while j < len(L) and not L[j].startswith("### "):
        l = L[j]
        m = re.match(r"^\| ([^|]+) \| (.*)$", l)
        if m and any(m.group(1).strip().startswith(f) for f in FL):
            print(f"  L{j + 1} [{m.group(1).strip()}] {m.group(2)[:W]}")
        j += 1
