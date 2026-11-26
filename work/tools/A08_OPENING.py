"""A08 opening patch: Decision Register D-41 and Topic Completion Register entry A08 (IN PROGRESS).
Idempotent, anchored to exact text; fails on any missing anchor."""
import sys, pathlib
ROOT = pathlib.Path("/home/claude/algocore_system/doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS")
DR = ROOT / "DECISION_REGISTER_2026-11-04.md"
TCR = ROOT / "TOPIC_COMPLETION_REGISTER_2026-11-04.md"

def sub_once(text, old, new, label):
    if new in text:
        return text
    n = text.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL ({label}): found {n}")
    return text.replace(old, new)

FOLDER = "A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT"

P1 = ("(P1) A08 owns the V2 retest mechanism (\"SNR-V2\", built in `main.py` under `sr_detector.wait_for_retest_enabled`) and "
      "studies it in full: `RetestDiverter` (the divert decision), `ParkedCandidate` and A08's use of `retest_state`, "
      "`RetestMonitor` (polling, rehydration on start, `clear_all`, stop) in `screening/retest_monitor.py`, and "
      "`sr_detector/retest_confirm.py` (confirmation, the timeout `timeout_sec`, the wrong-way reject `max_away_pct` (a 1-minute close more than that percentage past the band in the wrong direction; configured as `retest_max_away_pct`) and the strong close). For "
      "`SignalProcessor.continue_from_retest` (`signals/signal_processor.py` L2375 at the baseline, A06's file), A08 documents "
      "only the A08-specific handoff and values: what the monitor passes in, the retest-derived values that reach it (the zone "
      "band, the structure-stop buffer `retest_sl_buffer_pct` and the MARKET entry type of the retest entry) and what A08 "
      "receives back; its internal orchestration remains A06's and is not audited by A08, and the A09 and A10 decisions it "
      "reaches are recorded at the interface only. The PB-01 watchlist's retest confirmation stays A18's, A08 recording only "
      "its reuse of A08 functions. A18 cites A08 for the retest path. A06's PQ-13 wording (\"A18's retest path\") is not "
      "changed; the A08 records note the difference.")
P2 = ("(P2) A08 studies the V1 S&R observer (\"SNR-DETECTOR-V1\"): `SRDetector`, its calculations, its `sr_detector_results` "
      "writes and the end-of-day backfill script; A18 later covers only the S&R shadow's activation controls, integration and "
      "Live activation status, citing A08.")
P3 = ("(P3) A08 records at the interface every call site of A08 code in files other topics own (the call, the contract "
      "passed, the flag that gates it and the handoff): the signal processor (A06's file), `main.py` (A01), the structure exit "
      "manager (A11), the end-of-day square-off (A12), the MARKET retest entry in `orders/` (A10), the regime and V3 reuse "
      "(A18) and the `Candle` type imports (A05, A15, A18); it studies fully only the A08 objects called, and does not take "
      "ownership of the callers' internal logic.")
P4 = ("(P4) A08 examines all 48 items handed to it by the approved records of A01 to A07 (each record's section 15.2: A01 C13, "
      "C37, C38a, B-11 and C38b; A02 K-02 and K-21 to K-26; A03 D-05, H-11, P-02, P-11, Q-11, Q-17, Q-29, U-24 and U-25; A04 "
      "CL-11, CL-15, RL-05 and RL-06; A05 CM-05, CM-10, CM-15, HA-01, HA-04, HA-06, HA-07, HA-08, HA-09, IN-02 and XC-03; A06 "
      "WA-06, WA-07, WD-10, WD-16, PQ-09, PQ-11, EV-11 and EV-23; A07 SL-06, SL-30, EG-01 and XS-12) and the 16 Open Issues "
      "Register entries that name A08 (A03-10, A04-05, A04-28, A05-01, A05-02, A05-17, A05-18, A05-25, A05-27, A05-28, A05-29, "
      "A05-32, A05-35, A05-37, A05-38 and A05-54), recording A08's side only; their IDs, owners, classifications, treatments "
      "and statuses are unchanged. A04-05 is handled under the security rules: no credential value, validity or exposure is "
      "read or checked.")
P5 = (f"(P5) The topic folder is `{FOLDER}` (D-28; \"S&R\" written \"SR\").")
METHOD = ("Working method (D-39's method, applied to A08 by this decision): the STUDY in parts P01 to P07, each written by one "
          "read-only helper and checked statement by statement by a second, then assembled and checked independently against "
          "the evidence and the code; read-only helpers on both repositories, at most two at a time, the next pair started only "
          "after both helpers of the current pair have completed and their final hand-back notifications have arrived (a "
          "progress log or partial output is not completion), with saved progress and backups to the temporary branch "
          "`wip/a08-fieldwork`, scanned for identifiers before every push and never merged into `main`; Rama is consulted "
          "before any helper is started, the helpers of the RECONCILED TOPIC RECORD included; no legacy file is run, imported "
          "or tested, and no broker, scanner, webhook or other endpoint is contacted.")

D41 = f"""## D-41 — A08 boundary decisions P1 to P5 and the A08 working method

| Field | Entry |
|---|---|
| Decision ID | D-41 |
| Date | 2026-11-26 |
| Subject | The A08 topic boundaries (points P1 to P5) and the A08 working method, decided on ChatGPT's review of Claude's first A08 fieldwork checkpoint, without any change to the Master System Investigation Index |
| Exact decision | {P1} {P2} {P3} {P4} {P5} {METHOD} |
| Rationale | ChatGPT's review of the first checkpoint, 26-Nov-2026: NOT PASS, one scope correction (P1: `continue_from_retest` is in A06's file, so A08 documents only its A08-specific handoff and values, its internal orchestration remaining A06's); its review of the checkpoint's Revision 1 the same day: PASS, recommending option (a) for P1 as corrected, option (a) for P2 (A08 owns the V1 observer; A18 its activation and integration), option (a) for P3, the examination of all 48 inherited items and 16 open issues for P4, and option (a) for P5, which the validator accepts. The index gives `sr_detector/` and `screening/retest_monitor.py` to A08 and the S&R shadow's activation to A18; the owner of a named path studies it (index rule 1); the retest path is wired under an S&R switch, not under any V3, regime or allocator switch (`main.py` L3423 and L3765 to L3802 at the baseline); the resume function's orchestration stays with its owner, as for `continue_from_gate` (D-39, P2). The retest-path ownership point was carried to A08 by Rama's decision of 25-Nov-2026 (A07 RECONCILED TOPIC RECORD, section 22.1, point 2 (a); D-40). |
| Evidence | ChatGPT's A08 investigation direction (dated 25-Nov-2026), approved by Rama on 26-Nov-2026; Claude's first A08 fieldwork checkpoint, its Revision 1 and ChatGPT's reviews of both, all 26-Nov-2026 (not kept as files, D-17); the Topic Completion Register, entry A08; `evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md` in the A08 topic folder. |
| Rama approval | Rama's selections in the Claude chat on 2026-11-26: the A08 direction, "Approve; prepare checkpoint (Recommended)"; P1, ChatGPT's recommendation pasted as his answer ("Choose Option (a) — as corrected (Recommended) for P1"), recorded as his choice of option (a) as corrected; P2, "A08 studies it (Recommended)"; P3 and P4, "Accept both (Recommended)"; P5 and the method, "Approve folder and method (Recommended)". |
| Affected documents | The A08 topic folder; the Topic Completion Register, entry A08. |
| Status | APPROVED. |

"""

DR_HIST_OLD = ("Twenty-second version, 2026-11-25: decision D-40 (the approval of the A07 topic package, with his decisions on the "
               "seven points of the record's section 22.1), Rama's decision of 25-Nov-2026.")
DR_HIST_NEW = DR_HIST_OLD + (" Twenty-third version, 2026-11-26: decision D-41 (the A08 boundary decisions P1 to P5 and the A08 "
                             "working method), Rama's decisions of 26-Nov-2026.")

TCR_HIST_OLD = "A08 is not opened by this version (D-23)."
TCR_HIST_NEW = TCR_HIST_OLD + (" Eighty-sixth version, 2026-11-26: topic A08 opened on ChatGPT's A08 investigation direction, "
                               "approved by Rama on 26-Nov-2026, with Rama's decisions on the first checkpoint (D-41); A08 "
                               "IN PROGRESS, the STUDY stage.")

SCOPE = ("S&R detection, levels and zones, retest monitoring, and the technical context consumed by entry, risk and exit "
         "decisions: `sr_detector/` (twelve files), `screening/retest_monitor.py`, the S&R consumers in `orders/` (consumer "
         "call sites only; the owning logic stays with A11 where it is an exit manager) and three scripts, "
         "`scripts/sr_corp_action_spotcheck.py`, `scripts/sr_detector_backfill.py` and `scripts/sr_level_export.py` (Master "
         "System Investigation Index, entry A08 and Appendix A). Document 08, section 3, coverage item 7. Study baseline: "
         "trading-system-prod-snapshot at `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21). Boundary: A08 owns the calculation "
         "and production of S&R information; downstream consumers cite its output and are investigated in their own topics "
         "(index, entry A08). Boundaries, as Rama decided on 26-Nov-2026 on ChatGPT's recommendations, without any change to "
         "the index (Decision Register, D-41): " + " ".join([P1, P2, P3, P4, P5]))

ENTRY = f"""## A08 — Technical analysis, S&R and retest context

| Field | Entry |
|---|---|
| Topic ID | A08 |
| Topic name | Technical analysis, S&R and retest context |
| Scope | {SCOPE} |
| Phase | Phase 1 (authorised by Rama, D-27) |
| Status | IN PROGRESS, since 2026-11-26: opened on ChatGPT's A08 investigation direction (dated 25-Nov-2026; Document 04, section 4, step 1), issued after A07 closed and approved by Rama on 26-Nov-2026 ("Approve; prepare checkpoint (Recommended)"; D-23); ChatGPT's review of Claude's first fieldwork checkpoint asked for one scope correction (P1) the same day and passed its Revision 1, with its recommendations on the boundary points P1 to P5 and on the working method, and Rama decided them (Decision Register, D-41); {METHOD[0].lower() + METHOD[1:]} The STUDY stage. |
| STUDY | Not started. The topic folder `{FOLDER}` (D-28; D-41, P5) holds the first evidence file, `evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md`, DRAFT. |
| AUDIT | Not started (step 6). |
| RECONCILED TOPIC RECORD | Not started (step 10). |
| Issues raised with Rama | None yet. |
| Open issues | None yet for A08. The open issues of earlier topics that name A08 (A03-10, A04-05, A04-28, A05-01, A05-02, A05-17, A05-18, A05-25, A05-27, A05-28, A05-29, A05-32, A05-35, A05-37, A05-38 and A05-54) stay in the Open Issues Register under their topics, with their IDs and statuses unchanged (D-41, P4). |
| Reviewer | ChatGPT (Document 04, section 4, steps 5, 7 and 12). |
| Approval | None yet. Rama approves or rejects the topic document and package (Document 07, section 6.3). |
| Publication reference | Topic folder: `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/{FOLDER}/`. |
| Closure date | Not closed. |

## Topics not yet opened

A09 to A17, A20, A18 and A19, in that order"""

TCR_TAIL_OLD = "## Topics not yet opened\n\nA08 to A17, A20, A18 and A19, in that order"

dr = DR.read_text(encoding="utf-8")
dr = sub_once(dr, DR_HIST_OLD, DR_HIST_NEW, "DR history")
dr = sub_once(dr, "**Related documents:** 01, 02, 03, 04, 05, 06, 07, 08, 09 and 10.", D41 + "**Related documents:** 01, 02, 03, 04, 05, 06, 07, 08, 09 and 10.", "DR D-41")
DR.write_text(dr, encoding="utf-8")

t = TCR.read_text(encoding="utf-8")
t = sub_once(t, TCR_HIST_OLD, TCR_HIST_NEW, "TCR history")
t = sub_once(t, TCR_TAIL_OLD, ENTRY, "TCR entry")
TCR.write_text(t, encoding="utf-8")
print("OK")
