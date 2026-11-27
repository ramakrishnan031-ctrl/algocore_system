# A08 evidence: intended-behaviour sources for the A08 AUDIT — project-records half

**Status:** DRAFT — evidence for the A08 AUDIT (project-records half, written by helper A1; to be checked by a separate read-only helper and merged with the legacy-side half at assembly)
**Date:** 2026-11-27
**Revision history:** First version, 2026-11-27.
**Purpose and scope:** The project-records half of the inventory of admitted sources that state or imply the intended behaviour of A08, technical analysis, S&R and retest context, or that record what Rama said about it: the approved Master System Investigation Index (entry A08, the neighbouring entries, its rules and Appendix A); the Decision Register entries bearing on A08 (D-21, D-23 to D-25, D-28, D-30 to D-33, D-35, D-37, D-40 and D-41, with D-07, D-12 and D-17); the Topic Completion Register entry A08; the Open Issues Register and Audit Findings Register rows that name A08 or touch its code (read only); the governing foundation rules (Documents 01, 03, 04 section 5, 06 section 4.2 and 08); the Source Inventory and the Pre-Phase deliverables; the five existing legacy technical records; the approved A01 to A07 STUDY, AUDIT, RECONCILED TOPIC RECORD and intent-sources files, for what they record about S&R, zones, pivots, the retest path, the V1 observer, the backfill, the two other scripts, the `sr_detector` and `structure_exit` configuration and the candle fetch for S&R; and every statement attributed to Rama or to the operator in those records. By area: (a) the calculation core (CZ); (b) the candle fetch, the zone builder, the zone cache and the warmer (FC); (c) the V1 observer, its flags, the stored row and the backfill (VO); (d) the V2 retest path and the `continue_from_retest` handoff (RT); (e) the spot-check and export scripts (SC); (f) configuration, wiring and consumers (XW); (g) the tests, as earlier topics recorded them. With the conflicts between project sources (IC), the statements attributed to Rama or to the operator (RS), what could not be established and the questions about intent for Rama (ISA-Q). D-41's points P1 to P5 are applied unchanged. It judges no code, decides nothing, answers nothing for Rama, proposes no text for the Audit Findings Register or the Open Issues Register and changes no record; the legacy sources themselves are the legacy-side half's (ISB).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (baseline; written `970aabf` below), used for the clone check only (no legacy file was opened for this half); the project records at algocore_system `main`, commit `20e267d4997986107324f4f1385c96dc89b8b1bf` (written `20e267d`), read on 27-Nov-2026 with `sed`, `grep`, `git log`, `git diff --stat` and inline `python3 -I` programs that read Markdown only and wrote only to the work area. Nothing in either repository was written, run or imported; no endpoint was contacted; the four credential-holding file patterns were not opened; no credential, token, account identifier, personal name other than Rama's, IP address, e-mail address, key fingerprint or machine path is reproduced (D-07).
**Counts:** (completed at the end of the work; see the last revision note)
**Factual baseline:** the A08 STUDY (`A08_STUDY_2026-11-26.md`, DRAFT at `20e267d`) and its eight evidence files, statement IDs Pnn-Snnn; the STUDY items A08-AP-nn, A08-U-nn and A08-Q-nn. They are cited for what they record, never as intent and never as proof of a code fact without the cited lines (the AUDIT's own rule, AUDIT COMMON brief section 1).
**Layout and numbering:** the six sections of this half's brief, on the model of the project-records rows of the approved A07 file `A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/evidence/A07_AUDIT_INTENT_SOURCES_2026-11-24.md` (its sections 1, 2, 3, 5, 7 and 8): 1 Scope and method; 2 Sources by area (2.1 the records that govern every area; 2.2 to 2.8 the areas (a) to (g)); 3 Conflicts between sources (3.1 the IC rows; 3.2, by IS number and without IC numbers, the project-record statements that only the STUDY's code facts contradict, as the A07 file's section 4 kept them); 4 Statements attributed to Rama or to the operator; 5 Could not establish; 6 Questions about intent for Rama. IDs: IS-001 onward, RS-01 onward, IC-001 onward, ISA-Q1 onward; they are never renumbered, and the legacy-side half uses its own ranges.

## 1. Scope and method

### 1.1 Clone checks

- Before the work (27-Nov-2026, 12:31 IST): `<legacy clone>`: `git rev-parse HEAD` = `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, `git status --short` printed nothing; `<algocore_system clone>`: `git rev-parse HEAD` = `20e267d4997986107324f4f1385c96dc89b8b1bf`, branch `main`, `git status --short` printed nothing. After the work: section 5, last bullet.
- FACT (`git diff --stat 52cc811 20e267d` in `<algocore_system clone>`): since A08 was opened (`52cc811`, "A08 opened: Topic Completion Register, D-41, first A08 evidence"), the only project record outside the A08 topic folder that changed is the Topic Completion Register (6 lines, entry A08); the Decision Register, the Open Issues Register, the Audit Findings Register, the Source Inventory, the index, the foundation documents, the Pre-Phase deliverables, the five existing technical records and every A01 to A07 record are identical at `52cc811` and `20e267d`, so the line numbers that part P07 gives for them (read at `52cc811`, P07-S002) hold here.
- FACT (`git diff --stat e0439f2 52cc811`): between A07's closure (`e0439f2`) and A08's opening, the Decision Register (D-41 added) and the Topic Completion Register changed, and the A08 inventory was added.

### 1.2 What was read

All in `<algocore_system clone>` at `20e267d`. Every line cited below was re-opened at that commit; where a row rests on part P07's location of a record, the record was re-opened at P07's line.

- **The Master System Investigation Index** (375 lines): the status line L3; rules 1 to 12 (L12 to L23); section 2, rows A08 (L36), A09 (L37) and A11 (L39); the entries A05 (L89 to L96), A06 (L105), A07 (L107 to L114), A08 (L116 to L123), A09 (L125 to L132), A10 (L141), A11 (L143 to L150), A12 (L152 to L159), A15 (L179 to L186), A16 (L188 to L195), A18 (L215 to L222) and A19 (L224 to L231); the crosswalk row 7 (L251); Appendix A, its lead-in (L280 to L282) and the three A08 rows (L306 to L308). A search for A08 and the S&R terms found no other line.
- **The Decision Register** (583 lines): D-41 (L569 to L583), D-40 (L555 to L567), D-39 (L541 to L553), D-36 (L499 to L512), D-24 (L331 to L343) and D-21 (L289 to L301) in full; the subjects of the other entries (L9 to L569), and a search for A08 and the S&R terms (hits only in D-21, D-36, D-39, D-40 and D-41).
- **The Topic Completion Register** (162 lines): entry A08 (L141 to L158) in full.
- **The Open Issues Register** (4,255 lines; 261 entries): the recording rules (L8 to L19); the 16 entries that name A08, every field (by script; P07-S014 gives their lines); a script search of every entry for S&R terms (`retest`, `S&R`, `sr_detector`, `zone`, `pivot`, `structure exit`, `sr_level`, `spot check`, `backfill`, `OhlcFetcher`, `from_kite`, `Candle`, `session_vwap`, `warmer`), whose further hits were read at the matching lines: A02-11 (L571; structure-exit flatten, A11's), A03-31 (L1186; a structure-exit path, A11's and A12's), A05-07 (L2254 to L2268; Rama's operational background, RS-14), A06-26 (L3390; the expiry on the retest resumption) and A07-26 (EG-01's history question); the other hits were "time zone", candle or closure-source matters with no A08 code.
- **The Audit Findings Register** (1,449 lines): the recording rules (L8 to L24); the treatment-decision sections of A01 to A07 searched for S&R terms (hits read: A03 TG6, A05 TG4 to TG10, TG15, TG17, TG19, A06 TG1, A07 batch 5 items 1 and 2 and batch 6 item 4); the rows of the 48 items as STUDY section 13.2 copies them, with four rows re-opened as a spot check (L1011 HA-06, L1013 HA-08, L1404 EG-01, L424 P-02), which agree with the STUDY's copies.
- **The approved AUDITs of A01 to A07**, by a script that prints the heading, "Intended behaviour and source", "Result and classification", "Owner" and "Rama" fields of named records: 92 records (A01 7, A02 10, A03 18, A04 9, A05 26, A06 15, A07 7) = the A08 sides of the 48 items that have a record, the 16 Owner-field records and the records of STUDY section 13.6 that touch A08 code; multi-line fields of A06 read at their lines (EV-11 L4715 to L4725, PQ-06 L3774 to L3790, the A06 records' lines that name the retest, the warmer or S&R); the MATCH and handoff rows named by P07-S095 re-opened at their lines (A01 L526, L1986, L1989, L2002; A02 L527, L529, L554, L2328; A03 L1053, L1071, L1072, L1075, L2256, L2273, L2279, L2640, L3171, L3172; A04 L3193; A05 L1370, L1665, L1667 to L1669; A06 L3988 to L3992; A07 L100, L1176, L1208, L1214, L2993, L3436, L3739, L3761, L3763, L4323).
- **The approved RECONCILED TOPIC RECORDS of A01 to A07**: the A08 rows (A01 L304; A02 L341; A03 L405; A04 L414; A05 L466; A06 L531; A07 L543) and the lines naming A08 that P07 lists (P07-S015, P07-S094), re-opened: A01 L154, L444; A02 L136; A03 L147, L199, L419; A04 L144; A05 L39 to L43, L205, L480, L704 to L710; A06 L229, L548; A07 L533 to L573 (section 15.2), L592 to L608 (section 17, Rama's statements), L786 to L812 (section 22).
- **The approved intent-sources files of A01 to A07**: a search of each for A08 and the S&R terms; the rows found re-opened (A01 IS-1.16, IS-2.10, IS-2.25, IS-2.27, IS-2.28, IS-2.39, IS-2.44, IS-6.03, IS-6.09, IS-14.01, IS-14.02, CD-03; A02 IS-76, IC-15, CD-04, CD-16, CD-31; A03 IS-69, IS-113, IC-19, CD-31; A04 IS-52, CD-11, CD-14; A05 IS-49, IS-50, IS-55, IS-59, IS-62 to IS-66, IS-69 to IS-73, IS-75, IS-126, IS-131, IS-152, IS-160, IS-163 to IS-165, IS-168, IC-08, IC-13, CD-12, CD-18, CD-21 to CD-24, RS-04; A06 IS-38, IS-41, IS-80, IS-83, IS-91, IS-130, IS-136, IS-188, IS-193, IS-198, IS-199, IS-220, IC-05, IC-10, IC-27; A07 IS-001, IS-003, IS-005, IS-013, IS-028, IS-029, IS-033, IS-039, IS-043, IS-051, IS-053, IS-055, IS-062, IS-074, IS-616, IS-620, IS-621, IS-639, IS-690, IS-908, IS-926, IS-976, IS-978, IS-991, IC-004, CD-512, RS-12). Those that carry an A08 matter are cited in section 2; the time-zone, webhook and dashboard rows that matched only on a word are not.
- **The foundation documents** (`doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/`): Document 01 L39; Document 03 section 1 (L7 to L22); Document 04 section 5 (L56 to L100); Document 05 sections 11.1 to 11.3 (headings L120, L152, L163; the index row L126); Document 06 section 4.2 (L60 to L69); Document 08 sections 2 (L15 to L19), 3 (L21 to L48, item 7 at L31), 5 (L71 to L84), 6 (L86 to L96), 9 (L127 to L141), 10 (L143 to L145) and 12 (L153 to L157).
- **The Source Inventory** (113 lines): the "Reference system" row (L24), SRC-28 (L75), SRC-50 (L104), SRC-51 (L105), question Q2 (L111) and the records lead-in (L90). **The Pre-Phase deliverables**: the whole-system overview (L25, L27, L35, L64, L69), the operational workflows (L50, L61) and the methodology application (L13, L20, L57), found by a search for the S&R terms.
- **The five existing legacy technical records** (`doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`, 4,298 lines in all), searched for the S&R terms and read at the hits: record 01 L3, L46, L48, L82, L109, L110, L150 to L184; record 02 L27 to L28, L83, L864 to L881, L1137 to L1330 (the role lines of the twelve `sr_detector` entries), L1331 to L1345, L2030 to L2034, L3382 to L3386; record 03 L250 to L258; record 03A L39, L72, L79; the manual index L28, L44. Lines that carry an account identifier or a machine path are cited by line only.
- **The A08 STUDY and its evidence** (the factual baseline): STUDY sections 1, 2, 12, 13, 14 (L1 to L134, L559 to L856) and the index of its 92 points, 40 unknown items and 25 draft questions (extracted by script from sections 15 and 16, L856 to L1074); P07 (`A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md`) sections 1, 2, 3.1, 5 and 6 (L1 to L72, L190 to L323), its other sections through STUDY section 13; a script search of the STUDY and the eight evidence files for "Rama" (the legacy attributions of section 4).
- **ChatGPT's A08 investigation direction** (dated 25-Nov-2026, approved by Rama on 26-Nov-2026): not kept as a file (D-17); cited through STUDY section 1.9 (L81 to L100), which maps its requirements.
- **Working inputs (not evidence; not committed project records; D-17):** the three briefs of this work; the working note `<workspace>/notes/RAMA_DECISIONS_A08_STUDY.md` (Rama's working decisions of 26 and 27-Nov-2026), cited in section 4 only for what it records, with its status; the helper register `<workspace>/status/AGENTS_REGISTER_AUDIT.md`.
- **Not read for this half:** no legacy file (the legacy clone was used for the clone check only); no test; no external page (this half states no library, broker or Chartink behaviour of its own; where an earlier record quotes current external context, it is cited as that record's).

### 1.3 Kinds, dates and labels

- **Kinds.** INDEX (project): the approved Master System Investigation Index. DECISION (project): a Decision Register entry, or a decision of Rama that a project record states. REGISTER (project): the Topic Completion, Open Issues, Audit Findings or Source Inventory register. GOVERNANCE (project): a rule of a foundation document. RECORD (project): an approved A01 to A07 record (RTR, AUDIT, STUDY, evidence or intent-sources file), a Pre-Phase deliverable, or the A08 STUDY and its evidence (DRAFT; factual baseline only). DIRECTION (project): ChatGPT's A08 investigation direction. RAMA (STATED): Rama's own words or the record's account of them, with their date (Document 04, section 5.1 makes his statement of intent an intent source). PHASE 2 INPUT: a new-system input or treatment recorded in a register; never legacy intent and never a requirement on the legacy study (Open Issues Register L11 to L14; Audit Findings Register L20; Document 04, section 5.5). LEGACY TECHNICAL RECORD: one of the five existing technical records (SRC-40 to SRC-44), testing-derived and HISTORICAL (Document 08, section 9).
- **Dates.** A project record is dated by its own date and, where approved, by its approval decision: the A01 records 06-Nov-2026 (D-30), A02 09-Nov-2026 (D-31), A03 11-Nov-2026 (D-32), A04 14-Nov-2026 (D-33), A05 17-Nov-2026 (D-35), A06 20-Nov-2026 (D-37), A07 25-Nov-2026 (D-40); the index, the Source Inventory and the Pre-Phase deliverables 04-Nov-2026 (D-27); the foundation documents at Revisions 5 and 6 (D-19, D-26). A Rama statement carries the date the record gives it.
- **Labels.** Every row states what a project record says: HISTORICAL (record) for its content, FACT that the record says it. A project record that describes the legacy code is not evidence of what the code did or of what ran (Document 06, section 4.2); where a code fact is needed to place a conflict, it is the STUDY's statement, named. An earlier topic's result (ISSUE, MATCH, UNKNOWN / NOT ESTABLISHED, KNOWN DEFECT considered or not given) is that topic's and is not re-classified here; where an earlier record records a legacy source as an intent source, it is cited as that record recorded it ("as A0n recorded the source"), and the source itself is the legacy-side half's to list. A treatment, a Phase 2 input or a recorded Phase 2 question is labelled PHASE 2 INPUT wherever it appears. KNOWN DEFECT occurs here only inside quotations of earlier records.
- **The factual baseline's status.** FACT: at `20e267d` the STUDY's status line (L3) reads "DRAFT — the STUDY of topic A08 ...; not yet reviewed by ChatGPT", and the Topic Completion Register (entry A08, L150) "DRAFT, for ChatGPT's review (step 5)", with the AUDIT "Not started (step 6)" (L151). Whether ChatGPT has reviewed the STUDY is not recorded in a committed project record at `20e267d` (section 5).
- **Security (D-07).** No credential value, token, account identifier, personal name other than the Project Owner's, IP address, e-mail address, key fingerprint or machine path is written. The A04 credential records and the entry A04-05 are recorded at the interface only, by their IDs, subjects and A08 sides as the STUDY gives them; no credential value, validity, history or exposure is discussed. No security matter is raised.

### 1.4 Short names

**Project records** (paths under `doc/` of the project repository):

| Short name | Path | Date | What it is |
|---|---|---|---|
| MSII | `01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX/MASTER_SYSTEM_INVESTIGATION_INDEX_2026-11-04.md` | 2026-11-04; approved D-27 | the approved index: topics, paths, boundaries, rules, Appendix A |
| DR | `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/DECISION_REGISTER_2026-11-04.md` | to 2026-11-26 (D-41) | the Decision Register |
| TCR | `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/TOPIC_COMPLETION_REGISTER_2026-11-04.md` | entry A08 last changed at `20e267d` | the Topic Completion Register |
| OIR | `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/OPEN_ISSUES_REGISTER_2026-11-05.md` | to 2026-11-25 | the Open Issues Register |
| AFR | `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md` | to 2026-11-25 | the Audit Findings Register |
| SRCINV | `00_PROJECT_CONTROL/04_PROJECT_REGISTERS/SOURCE_INVENTORY_2026-11-04.md` | 2026-11-04; approved D-22, D-27 | the Source Inventory |
| DOC01, DOC03, DOC04, DOC05, DOC06, DOC08 | `00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/01_...`, `03_...`, `04_...`, `05_...`, `06_...`, `08_..._2026-11-03.md` | Revision 5 (01, 03, 06) or 6 (04, 05, 08); D-19, D-26 | the foundation documents |
| WSO, OPW, PMA | `01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW/WHOLE_SYSTEM_OVERVIEW_2026-11-04.md`; `01_PRE_PHASE/03_OPERATIONAL_WORKFLOW/OPERATIONAL_WORKFLOWS_2026-11-04.md`; `01_PRE_PHASE/05_PHASE1_METHODOLOGY/PHASE1_METHODOLOGY_APPLICATION_2026-11-04.md` | 2026-11-04; approved D-27 | Pre-Phase deliverables 2, 3 and 5 |
| A0n RTR, A0n AUDIT, A0n STUDY | `02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A0n_.../A0n_RECONCILED_TOPIC_RECORD_<date>.md`, `A0n_AUDIT_<date>.md`, `A0n_STUDY_<date>.md` (n = 1 to 7) | as approved (section 1.3) | the earlier topics' authoritative records, AUDITs and STUDYs |
| A0n IS | the same folders, `evidence/A0n_AUDIT_INTENT_SOURCES_<date>.md` | as approved | the earlier topics' intent-sources files (their rows are written with their topic, for example A05 IS-64 or A06 IC-10) |
| STUDY; P01 to P07; INV | `.../A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/A08_STUDY_2026-11-26.md` and its `evidence/` files: P01 `A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md`, P02 `A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md`, P03 `A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md`, P04 `A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md`, P05 `A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md`, P06 `A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md`, P07 `A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md`; INV `A08_SOURCE_FILE_INVENTORY_2026-11-26.md` | 2026-11-26 (DRAFT at `20e267d`) | the A08 factual baseline (statement IDs Pnn-Snnn; items A08-AP-nn, A08-U-nn, A08-Q-nn) |
| DIRECTION | ChatGPT's A08 investigation direction (not kept as a file, D-17), cited through STUDY section 1.9 | dated 25-Nov-2026; approved by Rama 26-Nov-2026 | the requirements A.1 to A.7, B and section 5 |
| R01, R02, R03, R03A, RMI | `02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/` (`01_SYSTEM_OVERVIEW.md`, `02_REPOSITORY_AND_FILE_MAP.md`, `03_STARTUP_RUNTIME_AND_SCHEDULER.md`, `03A_CRON_REGISTRY_TABLE.md`, `LEGACY_SYSTEM_MANUAL_INDEX.md`; SRC-40 to SRC-44) | evidence date 18-Sep-2026 (R01 L4); committed 2026-11-04 | the five existing legacy technical records |
| WNOTE | `<workspace>/notes/RAMA_DECISIONS_A08_STUDY.md` (work area; not a committed project record) | 26 and 27-Nov-2026 | the working note of Rama's decisions during the A08 STUDY and the AUDIT plan |

## 2. Sources by area

(to be written)

### 2.1 All areas: scope, boundaries, method and governing rules

(to be written)

### 2.2 Area (a): the calculation core (CZ)

(to be written)

### 2.3 Area (b): the candle fetch, the zone builder, the zone cache and the warmer (FC)

(to be written)

### 2.4 Area (c): the V1 observer, its flags, the stored row and the backfill (VO)

(to be written)

### 2.5 Area (d): the V2 retest path and the `continue_from_retest` handoff (RT)

(to be written)

### 2.6 Area (e): the spot-check and export scripts (SC)

(to be written)

### 2.7 Area (f): configuration, wiring and consumers (XW)

(to be written)

### 2.8 Area (g): the tests, as earlier topics recorded them

(to be written)

## 3. Conflicts between sources

(to be written)

## 4. Statements attributed to Rama or to the operator

(to be written)

## 5. Could not establish

(to be written)

## 6. Questions about intent for Rama

(to be written)
