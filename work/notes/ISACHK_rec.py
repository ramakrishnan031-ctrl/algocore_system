"""ISA checker: read-only record printer. For 'A0n ID' arguments prints the AUDIT record heading line and the
fields Intended behaviour / Result and classification / Owner / Rama (with their line numbers), and the AFR row
(Finding ID, Classification, Agreed treatment, Status cells) for that topic's ID. Reads Markdown only; writes
nothing. Usage: python3 -I ISACHK_rec.py A05:CM-10 A05:HA-08 ..."""
import re, sys, pathlib
BASE = pathlib.Path("/home/claude/algocore_system/doc")
TW = BASE / "02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
AUD = {t: next(TW.glob(f"{t}_*/{t}_AUDIT_2026-*.md")) for t in ("A01", "A02", "A03", "A04", "A05", "A06", "A07")}
AFR = (BASE / "00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md").read_text(encoding="utf-8").split("\n")
FIELDS = ("Intended behaviour", "Result and classification", "Owner", "Rama")
W = int(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("w=")), "900"))
# AFR section per topic
sec = {}
cur = None
for i, l in enumerate(AFR):
    m = re.match(r"^## (A0\d)\b", l)
    if m: cur = m.group(1)
    if cur and l.startswith("| ") and not l.startswith("| Finding ID") and not l.startswith("|---"):
        cid = l.split(" | ")[0].lstrip("| ").strip()
        sec.setdefault((cur, cid), []).append(i + 1)
for arg in sys.argv[1:]:
    if arg.startswith("w="): continue
    t, rid = arg.split(":")
    lines = AUD[t].read_text(encoding="utf-8").split("\n")
    pat = re.compile(r"^#{3,6} " + re.escape(rid) + r"\b")
    idx = [i for i, l in enumerate(lines) if pat.match(l)]
    print(f"######## {t} {rid}: headings at {[i + 1 for i in idx]}")
    if idx:
        i = idx[0]
        print(f"  L{i + 1}: {lines[i][:300]}")
        j = i + 1
        cur_f = None
        while j < len(lines) and not re.match(r"^#{2,6} ", lines[j]):
            l = lines[j]
            if l.startswith("- **"):
                cur_f = next((f for f in FIELDS if l.startswith(f"- **{f}")), None)
                if cur_f:
                    # join continuation lines
                    k = j + 1; txt = l
                    while k < len(lines) and lines[k].startswith("  ") and not lines[k].startswith("- **"):
                        txt += " " + lines[k].strip(); k += 1
                    print(f"  L{j + 1}-L{k}: {txt[:W]}")
            j += 1
    else:
        # table row form
        rows = [k for k, l in enumerate(lines) if l.startswith(f"| {rid} |")]
        for k in rows[:3]:
            print(f"  row L{k + 1}: {lines[k][:W]}")
    for k in sec.get((t, rid), []) + sec.get((t, rid + " (concurrency)"), []):
        cells = AFR[k - 1].split(" | ")
        print(f"  AFR L{k}: id={cells[0].lstrip('| ')} | class={cells[10][:120] if len(cells) > 10 else '?'} | treat={cells[13][:160] if len(cells) > 13 else '?'} | status={cells[14][:80] if len(cells) > 14 else '?'}")
