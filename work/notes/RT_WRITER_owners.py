# RT writer: print the Owner field (and Result line head) of named records in the approved AUDITs at 20e267d.
# Reads Markdown files of the algocore_system clone only; imports nothing from the legacy clone; writes nothing.
import glob
import re
import sys

ROOT = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/"
WANT = {
    "A02": ["K-22"],
    "A03": ["H-11", "P-02", "P-11", "Q-11", "Q-09", "Q-13", "H-10"],
    "A05": ["HA-03"],
    "A06": ["WA-06", "WA-07", "EV-11", "EV-01", "ET-07", "EV-08", "ET-06"],
    "A07": ["SL-06", "EG-01", "RP-12", "EG-02"],
    "A01": [],
}
for topic, ids in WANT.items():
    if not ids:
        continue
    f = sorted(glob.glob(ROOT + topic + "_*/" + topic + "_AUDIT_*.md"))[0]
    lines = open(f, encoding="utf-8").read().splitlines()
    for rid in ids:
        pat = re.compile(r"^#{3,5} " + re.escape(rid) + r" ")
        start = next((i for i, l in enumerate(lines) if pat.match(l)), None)
        if start is None:
            print(topic, rid, "NOT FOUND as heading")
            continue
        owner = None
        for j in range(start + 1, min(start + 40, len(lines))):
            if re.match(r"^#{3,5} ", lines[j]):
                break
            if lines[j].startswith("- **Owner"):
                owner = (j + 1, lines[j].strip())
                break
        print(topic, rid, "heading L%d" % (start + 1), "| owner", owner)
