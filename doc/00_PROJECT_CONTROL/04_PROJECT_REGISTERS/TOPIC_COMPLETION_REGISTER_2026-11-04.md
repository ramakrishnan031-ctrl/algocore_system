# Topic Completion Register

**Status:** DRAFT — for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: the register created when topic A01 was opened; A01 IN PROGRESS (Document 05, section 11.1, update timing 4). Second version, 2026-11-04: A01's STUDY and evidence files committed as DRAFT; A01 stays IN PROGRESS.
**Purpose and scope:** The project's Topic Completion Register (Document 10, section 3): one entry per Phase 1 topic of the approved Master System Investigation Index, with the fourteen fields of Document 10, section 3 and the topic statuses of Document 10, section 4. Claude maintains it and ChatGPT reviews it; Rama decides each topic document and the phase gates (Document 05, section 11.1). It is updated whenever a topic's status changes (update timing 4), and Claude keeps each entry's document fields current. An entry is added when its topic is opened.

## A01 — System orchestration, startup, runtime and shutdown

| Field | Entry |
|---|---|
| Topic ID | A01 |
| Topic name | System orchestration, startup, runtime and shutdown |
| Scope | Process entry, orchestration, lifecycle, runtime loop, startup checks, shutdown, time authority and top-level wiring: `main.py` (orchestration and wiring) and the other fourteen A01 paths of the Master System Investigation Index (entry A01; Appendix A for the two scripts); Document 08, section 3, coverage items 1, 3 (startup and runtime) and 20 (startup and shutdown boundary). Study baseline: trading-system-prod-snapshot at `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21). |
| Phase | Phase 1 (authorised by Rama, D-27) |
| Status | IN PROGRESS, since 2026-11-04: opened on ChatGPT's A01 investigation direction of 04-Nov-2026 (Document 04, section 4, step 1); the STUDY stage (steps 2 to 4). |
| STUDY | `A01_STUDY_2026-11-04.md`, DRAFT, committed for ChatGPT's review (step 5), with seven evidence files in the topic's `evidence/` subfolder (listed in the STUDY, section 13.2). |
| AUDIT | Not started. It begins only after ChatGPT has reviewed the STUDY and issued the next direction (step 6). |
| RECONCILED TOPIC RECORD | Not started (step 10). |
| Issues raised with Rama | None yet (Document 04, section 5.5). |
| Open issues | None recorded. The STUDY collects questions about intent for Rama (its section 14) and neutral concerns for the AUDIT (its section 12.2); none has been raised with Rama yet (Document 04, section 5.5). |
| Reviewer | ChatGPT (Document 04, section 4, steps 5, 7 and 12). |
| Approval | None yet. Rama approves or rejects the topic document and package (Document 07, section 6.3). |
| Publication reference | Topic folder: `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/`. The approved topic document's path and commit are entered after its approval and commit (Document 07, section 6.3). |
| Closure date | Not closed. |

## Topics not yet opened

A02 to A17, A20, A18 and A19, in that order (Master System Investigation Index, section 2). Each is entered here when it is opened, after the previous topic package has been reviewed by ChatGPT and approved by Rama (D-23). The synthesis deliverables S1 to S5 (index, section 4) are not module topics (index rule 10).
