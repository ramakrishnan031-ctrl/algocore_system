# A08 evidence: the 48 inherited items, the 16 Open Issues Register entries that name A08, and the non-ID handoff notes

**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26.
**Purpose and scope:** Part P07 of the A08 STUDY fieldwork (PRIOR_TOPIC_HANDOFFS; the A08 counterpart of A07's part P01). It lists (A) the 48 items that the approved A01 to A07 RECONCILED TOPIC RECORDS hand to A08 (A01 5, A02 7, A03 9, A04 4, A05 11, A06 8, A07 4), (B) the 16 Open Issues Register entries that name A08, (C) the handoff notes without an item ID that name A08, and (D) the difference in the wording of the retest path's owner. For each it records, from the records and registers, the source location, the result and classification, the treatment and status (copied unchanged), what the source says about A08's side, the neutral question it raises for A08, the A08 code location at the baseline where the answer lies, and the A08 STUDY part (P01 to P06) that answers it. It locates code and does not trace it: no A08 finding is written here. D-41 is applied: P1 (A08 owns the V2 retest mechanism; for `continue_from_retest` only the A08-specific handoff and values), P3 (other topics' call sites at the interface only) and P4 (all 48 items and 16 entries examined; IDs, owners, classifications, treatments and statuses unchanged; A04-05 under the security rules). No earlier topic's item is reopened, reclassified, re-treated or re-worded, and no record is edited.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-26 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced. Project records: the algocore_system repository, branch `main`, commit `52cc811` ("A08 opened: Topic Completion Register, D-41, first A08 evidence"), read-only.

## 1. Method, sources and boundaries

P07-S001. FACT (scope): this part records what the approved records and the project registers say about each item and entry handed to A08, and where in the A08 code (at `970aabf`) the A08 side is to be answered. The A08 facts themselves are for parts P01 to P06. Labels follow the COMMON brief, section 4; KNOWN DEFECT is not used; OPEN FOR RAMA is not written.

P07-S002. FACT (project records read; paths under `doc/` of `<algocore_system clone>`; the line numbers below are those of commit `52cc811`):

| Record | Parts read |
|---|---|
| `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/TOPIC_COMPLETION_REGISTER_2026-11-04.md` | entry A08, L141 to L158 (Scope L147; Open issues L154) |
| `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/DECISION_REGISTER_2026-11-04.md` | D-41, L569 to L583 (in full); D-40, L555 to L567 (for the retest-owner point) |
| `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md` | L1 to L24 (purpose; "How entries are recorded"; the "Not entered" rule L22); the table headers L51, L219, L363, L694, L957, L1129, L1307; the rows of the 48 IDs within their topic sections (by script, P07-S004 (a)) |
| `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/OPEN_ISSUES_REGISTER_2026-11-05.md` | L1 to L20; every `### A0n-nn` entry, searched for "A08" (261 entries); the 16 entries that name A08, every field; their summary-table rows |
| `01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX/MASTER_SYSTEM_INVESTIGATION_INDEX_2026-11-04.md` | entry A08, L116 to L123; Appendix A rows L306 to L308 |
| the seven RECONCILED TOPIC RECORDS (RTR) of A01 to A07 under `02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/` | section 15 (A01: L292 to L320, row A08 L304) and section 15.2 (A02 L329 to L358, row L341; A03 L393 to L422, row L405; A04 L402 to L431, row L414; A05 L454 to L483, row L466; A06 L519 to L558, row L531; A07 L531 to L573, row L543); every other line naming A08 (by script, P07-S004 (d)) |
| the seven AUDITs of A01 to A07, same folders | the record (heading, "Result and classification", "Owner") or MATCH row of each of the 48 IDs; every table row naming A08, with its section heading (by script, P07-S004 (c)); the collected indexes (A02 L2437, A03 L5377, A04 L5041, A05 L3327, A06 L6628, A07 L4432) |
| `.../A07_.../A07_STUDY_2026-11-22.md` | the lines naming P02-S040 (L187, L1445) |
| `.../A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md` | in full (129 lines) |
| `.../A07_.../evidence/A07_PRIOR_TOPIC_HANDOFFS_2026-11-21.md` | as the model for structure and depth (not as evidence) |

P07-S003. FACT (working inputs; not evidence): the COMMON brief and the P07 part brief in `<workspace>/briefs/`; the note `<workspace>/notes/handoffs_15_2_raw.txt` (an extract of the section 15.2 rows and prose), used only to locate lines. Result of the comparison: the note holds the A08 rows of A02 to A07 at the same content as found here, and no row for A01, whose record has no section 15.2 (its handoff table is section 15, row L304); every value used below was re-read from the record.

P07-S004. FACT (scripts; inline `python3 -I` programs and `grep`, written to no file, reading Markdown only): (a) a register reader that splits each Audit Findings Register table row on `|` outside backticks and prints the cells "Classification", "Agreed treatment (Phase 2 input), or OPEN", "Status" and "Component" of a given ID within its topic's section; (b) a record reader that finds the AUDIT heading `#### <ID> — ...` or `##### <ID> — ...`, joins wrapped field lines and prints the "Result and classification" and "Owner" fields; for MATCH items it prints the row and its table header; (c) a row finder that prints every AUDIT table row naming A08, with its nearest heading; (d) a line finder that prints every RTR line naming A08 (word match), with its heading; (e) an Open Issues Register reader that splits the register into its `### A0n-nn` entries and keeps those whose text contains the word A08. Every displayed line passed through a mask built from the identifier shapes of the backup scan (`<workspace>` tools, `scan.py`) before display.

P07-S005. FACT (legacy commands, for locating only; `<legacy clone>`, HEAD `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, working tree clean): `git show 970aabf:<path>` with line numbers, of `screening/retest_monitor.py`, `sr_detector/fetch.py`, `sr_detector/models.py` (L20 to L50), `sr_detector/zone_warmer.py` (L30 to L102), `sr_detector/detector.py` (L104 to L170, L255 to L326), `sr_detector/zone_builder.py` (L143 to L170), `sr_detector/zones.py` (L50 to L56), `sr_detector/retest_confirm.py` (L53 to L100), the three scripts in full, `main.py` (L393 to L440, L3417 to L3430, L3478 to L3510, L3545 to L3575, L3760 to L3805), `signals/signal_processor.py` (L354 to L392, L614 to L660, L1036 to L1062, L2375 to L2445) and `core/state_store.py` (L3015 to L3075); `git grep -n` at `970aabf` limited to the sixteen A08 paths (A08 inventory, section 1), and to named A07 files; two repository-wide `git grep` searches (an S&R shadow-database path; P07-S088) carrying the four exclusions of the COMMON brief, section 1. Nothing was run, imported or tested; no file of the four credential-holding patterns was opened.

P07-S006. FACT (columns of the section 3 tables). "Source": the RTR row that hands the item over (A0n RTR Lnnn), the AUDIT record heading or MATCH row (AUDIT Lnnn), the AUDIT handoff row naming A08, and the Audit Findings Register row (AFR Lnnn). "Result and classification": the AFR cell "Classification" where the register has a row; otherwise the AUDIT's own result, with the absence stated (the register does not enter MATCH items or items handed off whole, AFR L22). "Treatment; status": the AFR cells "Agreed treatment (Phase 2 input), or OPEN" and "Status", copied unchanged, or "not entered". "A08 side (source)": a short paraphrase of the record's Owner field and of the handoff row naming A08; quotations are under 15 words. "A08 question": neutral, what A08 must establish. "A08 code location": FACT, the file and lines at `970aabf` located by P07-S005, not traced. "Part": INTERPRETATION, the A08 STUDY part (part brief, list of parts P01 to P06) whose files hold the location; primary part first, secondary parts after a semicolon.

P07-S007. FACT (labels): each table row is one statement. Its record cells are HISTORICAL (record): they state what the record says, not what the legacy code did or what ran. Its "A08 code location" cell is FACT about the file at the baseline. Its "A08 question" and "Part" cells are INTERPRETATION. Nothing here is evidence that any code ran or that any value was in force on a machine (Document 06, section 4.2).

P07-S008. FACT (boundaries, D-41): A08's files are the twelve `sr_detector/` files, `screening/retest_monitor.py` and the three scripts (A08 inventory, section 1). Where an item's A08 side lies in another topic's file (`main.py`, A01; `signals/signal_processor.py`, A06; `core/state_store.py`, A03; `orders/`, A10 to A12), the location is given as an interface only (D-41, P3); for `continue_from_retest` (`signals/signal_processor.py` L2375) only what the monitor passes in, the retest-derived values that reach it and what A08 receives back are A08's (D-41, P1).

P07-S009. FACT (security): no credential value, token, account identifier, IP address, e-mail address, key fingerprint or absolute machine path is written. For A04 CL-11, CL-15 and the entry A04-05, only the A08 interface is recorded (whether and where A08 code uses a broker client, and the lines of its construction); no credential value, validity or exposure is read, derived, checked or discussed, and the token file was not opened. Credential field names that appear in the code are not reproduced.

P07-S010. FACT (external sources): none was read. This part quotes project records and locates lines in the legacy repository; it states no library or broker behaviour of its own.

## 2. How the list was confirmed

## 3. The 48 inherited items, by source topic

## 4. The 16 open issues that name A08

## 5. The non-ID handoff notes

## 6. The retest-ownership wording

## 7. Assignment table

## 8. Points for the AUDIT

## 9. UNKNOWN / NOT ESTABLISHED items

## 10. Questions about intent for Rama

## 11. Cross-references
