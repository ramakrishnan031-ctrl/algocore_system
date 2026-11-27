"""Read-only: extract the heading, intended-behaviour, result, owner and Rama fields of named AUDIT records
from the approved A01 to A07 AUDITs in the algocore_system clone. Writes only to the notes file given."""
import re, sys, pathlib
BASE = pathlib.Path("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION")
AUD = {"A01": "A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/A01_AUDIT_2026-11-05.md",
       "A02": "A02_CONFIGURATION_AND_EFFECTIVE_SETTINGS/A02_AUDIT_2026-11-08.md",
       "A03": "A03_DATABASE_PERSISTENCE_MIGRATIONS_AND_BACKUPS/A03_AUDIT_2026-11-10.md",
       "A04": "A04_BROKER_INTERFACE_AUTHENTICATION_AND_BROKER_STATE/A04_AUDIT_2026-11-13.md",
       "A05": "A05_MARKET_DATA_INSTRUMENTS_AND_EXTERNAL_REFERENCE_DATA/A05_AUDIT_2026-11-15.md",
       "A06": "A06_SIGNAL_INTAKE_AND_WEBHOOK_LIFECYCLE/A06_AUDIT_2026-11-18.md",
       "A07": "A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/A07_AUDIT_2026-11-24.md"}
IDS = {
 "A01": "C13 C37 C38a C38b C3 C18 C40".split(),
 "A02": "K-02 K-21 K-22 K-23 K-24 K-25 K-26 L-08 L-12 K-32".split(),
 "A03": "D-05 H-11 P-02 P-11 Q-11 Q-17 U-24 U-25 D-09 Q-09 U-05 Q-13 Q-21 Q-23 U-10 U-16 J-14 H-10".split(),
 "A04": "CL-11 CL-15 RL-05 RL-06 CL-12 AU-05 RL-11 CL-01 CL-13".split(),
 "A05": "CM-05 CM-10 HA-01 HA-04 HA-06 HA-07 HA-08 HA-09 IN-02 XC-03 CM-07 CM-11 HA-03 HA-05 HA-10 IN-09 CM-01 CM-08 HA-02 IN-04 IN-05 IN-11 IN-12 XC-04 XC-07 CA-16".split(),
 "A06": "WA-06 WA-07 WD-10 WD-16 PQ-09 EV-11 EV-01 ET-07 XA-02 EV-08 EV-13 ET-06 EV-14 XA-05 PQ-06".split(),
 "A07": "SL-06 EG-01 XS-12 SX-07 RP-12 EG-02 XS-08".split()}
FIELDS = ("Intended behaviour", "Result and classification", "Owner", "Rama")
topic = sys.argv[1]
lines = (BASE / AUD[topic]).read_text(encoding="utf-8").split("\n")
out = []
for rid in IDS[topic]:
    pat = re.compile(r"^#{3,6} " + re.escape(rid) + r"\b")
    idx = [i for i, l in enumerate(lines) if pat.match(l)]
    if not idx:
        out.append(f"#### {topic} {rid}: NO HEADING FOUND"); continue
    i = idx[0]
    out.append(f"#### {topic} {rid} (L{i+1}; headings found {len(idx)}) {lines[i][:220]}")
    j = i + 1
    while j < len(lines) and not re.match(r"^#{2,6} ", lines[j]):
        l = lines[j]
        for f in FIELDS:
            if l.startswith(f"- **{f}"):
                lim = 2600 if f.startswith("Intended") else 700
                out.append(f"  L{j+1} {l[:lim]}")
        j += 1
pathlib.Path(f"/home/claude/a08/notes/ISA_records_{topic}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(topic, len(IDS[topic]), sum(1 for o in out if o.startswith("####")), sum(1 for o in out if "NO HEADING" in o))
