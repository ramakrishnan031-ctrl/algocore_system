"""A08 STUDY commit preparation: copy the STUDY and the seven evidence parts into the topic folder of the working clone,
and patch the Topic Completion Register (A08 STUDY field, Status tail, revision history). Idempotent; anchored."""
import sys, pathlib, shutil
ROOT = pathlib.Path("/home/claude/algocore_system")
TOPIC = ROOT / "doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT"
SRC = pathlib.Path("/home/claude/a08")
PARTS = [
    "A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md",
    "A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md",
    "A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md",
    "A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md",
    "A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md",
    "A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md",
    "A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md",
]
shutil.copyfile(SRC / "out/A08_STUDY_2026-11-26.md", TOPIC / "A08_STUDY_2026-11-26.md")
for p in PARTS:
    shutil.copyfile(SRC / "parts" / p, TOPIC / "evidence" / p)

TCR = ROOT / "doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/TOPIC_COMPLETION_REGISTER_2026-11-04.md"
t = TCR.read_text(encoding="utf-8")

def sub(old, new, label):
    global t
    if new in t:
        return
    n = t.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL ({label}): {n}")
    t = t.replace(old, new)

sub("Eighty-sixth version, 2026-11-26: topic A08 opened on ChatGPT's A08 investigation direction, approved by Rama on "
    "26-Nov-2026, with Rama's decisions on the first checkpoint (D-41); A08 IN PROGRESS, the STUDY stage.",
    "Eighty-sixth version, 2026-11-26: topic A08 opened on ChatGPT's A08 investigation direction, approved by Rama on "
    "26-Nov-2026, with Rama's decisions on the first checkpoint (D-41); A08 IN PROGRESS, the STUDY stage. "
    "Eighty-seventh version, 2026-11-26: A08's STUDY and evidence files committed as DRAFT for ChatGPT's review; A08 "
    "stays IN PROGRESS.", "history")

sub("no legacy file is run, imported or tested, and no broker, scanner, webhook or other endpoint is contacted. The STUDY stage. |",
    "no legacy file is run, imported or tested, and no broker, scanner, webhook or other endpoint is contacted; ChatGPT's "
    "review passed the opening commit `52cc811` the same day; the STUDY stage. |", "status")

sub("| STUDY | Not started. The topic folder `A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT` (D-28; D-41, P5) holds the first "
    "evidence file, `evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md`, DRAFT. |",
    "| STUDY | `A08_STUDY_2026-11-26.md`, DRAFT, for ChatGPT's review (step 5), in the topic folder "
    "`A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT` (D-28; D-41, P5), with eight evidence files in its `evidence/` "
    "subfolder (`A08_SOURCE_FILE_INVENTORY_2026-11-26.md`, Revision 1, and seven others, listed in the STUDY, section "
    "17.2), all DRAFT. Its fieldwork was done in 7 parts by read-only helpers under the method of D-41, each checked "
    "statement by statement and corrected by a separate helper, and the assembled STUDY was checked independently "
    "against the evidence and the code (the STUDY, section 1.5). By Rama's decisions of 26-Nov-2026, recorded in the "
    "STUDY's section 1.2 for ChatGPT's review, the STUDY also examines A08's side of the 16 earlier AUDIT records whose "
    "Owner field names A08 without handing them to A08, and lists, with their A08 facts, the earlier records that touch "
    "A08 code without naming A08 (the STUDY, section 13). Its Points for the AUDIT are in its section 15, its boundary "
    "points in its section 14 and its draft questions about intent for Rama in its section 16; none has been raised with "
    "Rama yet (Document 04, section 4, step 8). |", "study")

TCR.write_text(t, encoding="utf-8")
print("OK")
