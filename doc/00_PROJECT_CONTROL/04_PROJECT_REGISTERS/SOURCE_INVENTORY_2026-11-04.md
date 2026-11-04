# Source Inventory

**Status:** DRAFT — Pre-Phase working record, for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: Pre-Phase Deliverable 1, first pass, under ChatGPT's Pre-Phase instructions of 04-Nov-2026 (Decision Register, D-20), with the study baseline Rama decided (D-21), Rama's answer on external evidence, and the corrections from ChatGPT's review of Pre-Phase checkpoint 1.
**Purpose and scope:** The one authoritative Source Inventory (Document 10, section 8; Document 07, section 3; Decision Register, D-03). It lists the admitted sources only: the algocore_system governance records, the legacy repository trading-system-prod-snapshot, the five existing technical records, and any surviving external evidence that Rama supplies (Document 06, section 3; D-12). Ignored repositories are not inventoried. Each row gives the eight fields of Document 10, section 8, with a reference (Ref) for citation. The inventory records sources; it does not study them.
**Labels:** FACT, UNKNOWN / NOT ESTABLISHED, INTERPRETATION, HISTORICAL and OPEN QUESTION (Document 04, section 6). The status of each source is one of: AVAILABLE — VERIFIED; AVAILABLE — NOT YET INSPECTED; REPORTED BY RAMA — NOT INDEPENDENTLY VERIFIED; MISSING / UNAVAILABLE; PROPOSED — OPEN FOR RAMA.

## 1. Legacy repository and the Phase 1 study baseline

Retrieved by Claude on 04-Nov-2026 at 15:27 IST (`git ls-remote`, then a clone with the full history) into a local read-only clone, which is not written to, run or deployed (Document 06, section 3).

| Item | Entry |
|---|---|
| Repository | github.com/ramakrishnan031-ctrl/trading-system-prod-snapshot (public) |
| Refs | FACT: one branch, `main`, which is also HEAD; no tags and no other refs (`git ls-remote`, 04-Nov-2026, 15:27 IST). |
| Repository HEAD | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb` is the head of `main`, committed 2026-09-11 02:05:13 +05:30; 1,438 tracked files. |
| History | FACT: 1,537 commits on `main`, from `bcf03b5` (2026-04-17, "Initial v2 foundation - 1411 tests green") to `970aabf` (2026-09-11). |
| Study baseline | `970aabf3c78d777d9d34549e021f7c8e756c7bdb` — decided by Rama on 04-Nov-2026 (Decision Register, D-21). Evidence cites this full commit, not the branch name, so a later push to `main` cannot move it. |
| Evidence for the baseline | FACT: it is the head of the only branch and the last commit in the repository. HISTORICAL: the five existing technical records state that production's code is "RECORD-DERIVED at git `970aabf`" (`01_SYSTEM_OVERVIEW.md`, lines 27 and 153; `LEGACY_SYSTEM_MANUAL_INDEX.md`, line 13). |
| Last recorded deployment | HISTORICAL: the repository's deploy ledger records the last measured push and deployment on 02-Sep-2026: merge `686df1c`, pushed, deployed and measured, then `7d4970a`, "deployed but UNBOOTED" (`UNPUSHED_LEDGER.md` at `970aabf`, lines 3456 to 3469 and 3549). The subject of `970aabf` itself ends "still unpushed". |
| Changes after the last recorded deployment | FACT: the 33 commits after `686df1c` (32 after `7d4970a`), dated 02-Sep to 11-Sep-2026, change 52 files, in runtime areas as well as tests and documents: `scripts/` 20, `tests/` 8, `docs/` 5, `core/` 4, `signals/`, `orders/` and `config/` 2 each, and `screening/`, `ops/`, `main.py`, `deploy/`, `capital/`, `broker/`, `alerts/`, `PATHS.md` and `UNPUSHED_LEDGER.md` 1 each. Phase 1 notes them topic by topic (D-21). |
| Production runtime commit at shutdown | UNKNOWN / NOT ESTABLISHED: no runtime evidence survives (Document 06, section 4.2). The repository HEAD, the last recorded deployment and the runtime commit at shutdown are three different things; this inventory does not treat them as one "production version". |
| Reference system | The production system is always the reference system (Rama, 04-Nov-2026; D-21). REPORTED BY RAMA — NOT INDEPENDENTLY VERIFIED: the production and testing repositories differ in the S&R change and configuration settings. The five existing technical records describe the testing copy as `970aabf` plus the S&R shadow files, with the `force_qty` change set in configuration and in three code files (`01_SYSTEM_OVERVIEW.md`, lines 164 to 170). |
| Deployment model | HISTORICAL: changes reached the production VM by a git push from the development PC (`DEPLOYMENT.md`, line 222: "`git push vm main`"). The README states that the system was live from 11-May-2026 (`README.md`, line 9). |

Commits cited, with their full SHAs (short forms are used elsewhere in this inventory):

| Short | Full SHA | Repository | What it is |
|---|---|---|---|
| `970aabf` | `970aabf3c78d777d9d34549e021f7c8e756c7bdb` | trading-system-prod-snapshot | The study baseline and repository HEAD (D-21) |
| `7d4970a` | `7d4970a26991fd40774023f5293a00556228e14b` | trading-system-prod-snapshot | The last commit the deploy ledger records as deployed (02-Sep-2026) |
| `686df1c` | `686df1c847d415958c4df406b77503bb45975749` | trading-system-prod-snapshot | The last merge the deploy ledger records as pushed, deployed and measured (02-Sep-2026) |
| `bcf03b5` | `bcf03b517391c8de8fd14240aa4dfe2607a5feb9` | trading-system-prod-snapshot | The first commit (2026-04-17) |
| `e7bf477` | Not available: not a commit of trading-system-prod-snapshot | — | The testing copy's commit named by the five existing technical records |
| `6574d4c` | `6574d4c6c9d3c82e19ce93fd8cd25a5fd91af443` | algocore_system | Main when this inventory was drafted; the foundation documents marked APPROVED (D-19) |
| `f8b86d8` | `f8b86d84183e0766bbe65ffe9bd7af8b1c3a1a20` | algocore_system | The Decision Register with D-21 |
| `9898e8c` | `9898e8c308e8ab8835efd3462aa2f1f97ba1760b` | algocore_system | The last commit that changed the five existing technical records |

## 2. Inventory

This inventory was drafted against algocore_system main at `6574d4c`, where the foundation documents were marked APPROVED (D-19). The Decision Register was then updated at `f8b86d8` (D-21), and SRC-02 cites that version; the other algocore_system rows cite `6574d4c`, as their files did not change in `f8b86d8`. `970aabf` is the study baseline (D-21). File counts are of tracked files at that commit. "Candidate" topics come from folder or file names only (INTERPRETATION); the Master System Investigation Index decides the topics (D-13, D-16).

### 2.1 algocore_system governance records

| Ref | Filename | Repository or upload location | Commit | Source type | Relevant topic | Evidence status | Inspection status | Related document |
|---|---|---|---|---|---|---|---|---|
| SRC-01 | `01_PROJECT_FOUNDATION_AND_SCOPE_2026-11-03.md` to `10_MASTER_PROJECT_INDEX_AND_CONTROL_REGISTERS_2026-11-03.md` (10 files) | algocore_system, `doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/` | `6574d4c` | Project governance documents, APPROVED (D-19) | All: they govern the study; they are not legacy evidence | AVAILABLE — VERIFIED | Reviewed for Pre-Phase, 04-Nov-2026 | Document 10, section 2 |
| SRC-02 | `DECISION_REGISTER_2026-11-04.md` | algocore_system, `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` | `f8b86d8` | Project register (D-01 to D-21) | All | AVAILABLE — VERIFIED | Reviewed: D-03, D-12, D-13, D-16, D-17, D-19 and D-20; D-21 recorded by Claude | Document 10, section 5 |
| SRC-03 | The six revision reports and the three validation scripts | algocore_system, `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/` | `6574d4c` | Revision and validation records | Project control | AVAILABLE — VERIFIED | Not needed for the legacy study. `validate_algocore_workspace_2026-11-04.py` is revised together with this inventory (self-test T39) | Document 07, section 3 |
| SRC-04 | `GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt` | algocore_system, `doc/00_PROJECT_CONTROL/03_GITHUB_AND_REPOSITORY_RECORDS/` | `6574d4c` | Repository setup record | Project control | AVAILABLE — VERIFIED | Not needed for the legacy study | Document 07, section 3 |

### 2.2 trading-system-prod-snapshot

| Ref | Filename | Repository or upload location | Commit | Source type | Relevant topic | Evidence status | Inspection status | Related document |
|---|---|---|---|---|---|---|---|---|
| SRC-10 | The whole repository: 1,438 files | github.com/ramakrishnan031-ctrl/trading-system-prod-snapshot, branch `main`; local read-only clone | `970aabf` (study baseline, D-21) | Legacy source repository: code, configuration, tests, deployment files and the legacy project's own documentation | All coverage items of Document 08, section 3 | FACT for what the repository holds at the commit; runtime behaviour UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2) | AVAILABLE — VERIFIED: refs, commit, history and file list. Contents not yet inspected | Section 1; Document 06, sections 3 and 6 |
| SRC-11 | `alerts/` (6 files: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 14 Alerts and notifications | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-12 | `allocation/` (5: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 9 Risk and capital allocation | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-13 | `broker/` (13: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 10 Order processing; 13 Reconciliation and broker state | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-14 | `capital/` (10: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 9 Risk and capital allocation | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-15 | `config/` (51: .yaml 31, .csv 20) | as SRC-10 | `970aabf` | Legacy configuration | Candidate: 17 Configuration | FACT: present at the commit; a configured value is not evidence of the value in force (Document 08, section 10) | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-16 | `core/` (29: .py 26, .sql 2, .txt 1) | as SRC-10 | `970aabf` | Legacy code and database schema files | Candidate: 1 System overview and architecture; 16 Database and storage | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-17 | `data/` (3: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 4 Market data and data sources | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-18 | `deploy/` (29: service and timer units, cron file, shell and other scripts, notes) | as SRC-10 | `970aabf` | Legacy deployment files | Candidate: 3 Startup, runtime and scheduler; 18 Security, credentials and deployment | FACT: present at the commit; a unit or cron file is not evidence that it was installed or ran (Document 08, section 10) | AVAILABLE — NOT YET INSPECTED | SRC-42, SRC-43 |
| SRC-19 | `docs/` (474: .md 354, .txt 70, .png 34, other 16) | as SRC-10 | `970aabf` | The legacy project's own documentation (evidence priority 4, Document 06, section 4.1) | Candidate: 22 Known issues and historical findings; supporting material for all topics | HISTORICAL: documents are compared with the code, never taken in its place | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-20 | `ops/` (14: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 20 Failure, recovery and operational behaviour | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-21 | `ops_dashboard/` (183: .py 93, .html 33, .gitkeep 28, .md 19, other 10) | as SRC-10 | `970aabf` | Legacy code: operations dashboard | Candidate: 15 Reports, logging and evidence | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-22 | `orders/` (21: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 10 Order processing; 11 Order and position management; 12 Exits and square-off | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-23 | `regime/` (4: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 6 Filtering and trade decision | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-24 | `reports/` (10: .py 5, .md 4, .gitkeep 1) | as SRC-10 | `970aabf` | Legacy code and documents | Candidate: 15 Reports, logging and evidence | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-25 | `screening/` (7: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 6 Filtering and trade decision | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-26 | `scripts/` (88: .py 85, .sh 2, .bat 1) | as SRC-10 | `970aabf` | Legacy code: scheduled and operator scripts | Candidate: 3 Startup, runtime and scheduler; 20 Failure, recovery and operational behaviour | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-42, SRC-43 |
| SRC-27 | `signals/` (4: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 5 Signals and strategies | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-28 | `sr_detector/` (12: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 7 Technical analysis and S&R | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-29 | `strategies/` (5: .py) | as SRC-10 | `970aabf` | Legacy code | Candidate: 5 Signals and strategies | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-30 | `tasks/` (1: .md) | as SRC-10 | `970aabf` | Legacy document | To be established | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | — |
| SRC-31 | `tests/` (442: .py 404, .yaml 31, .csv 5, .sh 2) | as SRC-10 | `970aabf` | Legacy tests | Candidate: 19 Testing and validation | FACT: present at the commit; a test is not evidence that it ran or passed | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-32 | `utils/` (5: .py) | as SRC-10 | `970aabf` | Legacy code: shared utilities | To be established | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-33 | `v3_chain/` (9: .py) | as SRC-10 | `970aabf` | Legacy code | To be established | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-41 |
| SRC-34 | `main.py`, `run_tests.py` | as SRC-10, repository root | `970aabf` | Legacy code: entry point and test runner | Candidate: 3 Startup, runtime and scheduler; 19 Testing and validation | FACT: present at the commit | AVAILABLE — NOT YET INSPECTED | SRC-42 |
| SRC-35 | `requirements.txt`, `requirements-dev.txt`, `.env.example`, `.gitattributes`, `.gitignore` | as SRC-10, repository root | `970aabf` | Dependency lists, the environment-file template and Git settings | Candidate: 17 Configuration; 18 Security, credentials and deployment | FACT: present at the commit. Values in the template are never reproduced (Document 08, section 11) | AVAILABLE — NOT YET INSPECTED | Document 06, section 6 |
| SRC-36 | `README.md` (107 lines; last changed 2026-07-16) | as SRC-10, repository root | `970aabf` | Legacy project documentation | Candidate: 1 System overview and architecture | HISTORICAL | Lines 1 to 45 read for provenance (04-Nov-2026) | Section 1 |
| SRC-37 | `DEPLOYMENT.md` (403 lines; last changed 2026-07-16) | as SRC-10, repository root | `970aabf` | Legacy project documentation: deployment procedure | Candidate: 18 Security, credentials and deployment | HISTORICAL | Searched for the deployment route; line 222 cited (04-Nov-2026) | Section 1 |
| SRC-38 | `UNPUSHED_LEDGER.md` (3,590 lines; last changed 2026-09-02) | as SRC-10, repository root | `970aabf` | Legacy project record: the ledger of commits not yet pushed or deployed | Candidate: 18 Security, credentials and deployment; 22 Known issues and historical findings | HISTORICAL: records what was measured and written at its own dates | Lines 1 to 40, 3456 to 3475 and 3547 to 3590 read for the deployed state (04-Nov-2026) | Section 1 |
| SRC-39 | `PATHS.md` (655 lines; last changed 2026-09-03), `AGENTS.md` (109 lines), `GEMINI.md` (320 lines) | as SRC-10, repository root | `970aabf` | Legacy project documentation, including the instructions used for AI assistants on the legacy project | Candidate: 2 Repository and complete file map; 22 Known issues and historical findings | HISTORICAL. The AI-assistant files are read as records of the legacy project, not as instructions to this project | AVAILABLE — NOT YET INSPECTED | — |

### 2.3 The five existing technical records

Admitted legacy records (Document 08, section 9; D-12), kept unchanged in algocore_system, `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`, unchanged since commit `9898e8c`. The records' headers give their evidence basis: a worktree on the development PC at commit `e7bf477` plus an uncommitted change set (four of them call it byte-equivalent to the testing VM as delivered on 17-Sep-2026), with machine-side facts derived from captures held in trading-system-sbx-snapshot, an ignored repository (D-12). Four of them state that production was never read. FACT (checked 04-Nov-2026): `e7bf477` is not a commit of trading-system-prod-snapshot; `01_SYSTEM_OVERVIEW.md`, line 164, describes it as "`970aabf` plus the S&R shadow files". Phase 1 checks their statements against the production code at the study baseline, which is always the reference (D-21), and records corrections in the topic documents (Document 08, section 9).

| Ref | Filename | Repository or upload location | Commit | Source type | Relevant topic | Evidence status | Inspection status | Related document |
|---|---|---|---|---|---|---|---|---|
| SRC-40 | `01_SYSTEM_OVERVIEW.md` (184 lines; SHA-256 `51d5f315ba9a949f3807e5a68c6d48a46411b0e2eaeaaf9da1bf4693cb3283a9`) | algocore_system, folder above | `6574d4c` | Existing technical record, dated 18-Sep-2026 | 1 System overview and architecture | HISTORICAL: evidence basis as above (its line 3); production never read (lines 3 and 27) | Provenance lines read; content not yet reviewed | Document 08, section 9 |
| SRC-41 | `02_REPOSITORY_AND_FILE_MAP.md` (3,557 lines; SHA-256 `8b5aec74544c7a613ced958f90ca9deedb524db321ae7101b9a577015cbf6d49`) | algocore_system, folder above | `6574d4c` | Existing technical record, dated 18-Sep-2026 | 2 Repository and complete file map | HISTORICAL: evidence basis as above (its line 3); it maps the tree at `e7bf477`, not at `970aabf` | Provenance lines read; content not yet reviewed | Document 08, section 9 |
| SRC-42 | `03_STARTUP_RUNTIME_AND_SCHEDULER.md` (321 lines; SHA-256 `f7d38f2d0f7ea2d61783970b1e8a81fc06d1676ab613ee4db18178ee5cbc3087`) | algocore_system, folder above | `6574d4c` | Existing technical record, dated 18-Sep-2026 | 3 Startup, runtime and scheduler | HISTORICAL: evidence basis as above (its lines 3 to 5) | Provenance lines read; content not yet reviewed | Document 08, section 9 |
| SRC-43 | `03A_CRON_REGISTRY_TABLE.md` (112 lines; SHA-256 `85d0bd23f087f33f9ff1724469faa30893ac3a26fb138abc86c7bfa5e82ece3c`) | algocore_system, folder above | `6574d4c` | Existing technical record, appendix to SRC-42 | 3 Startup, runtime and scheduler | HISTORICAL: evidence basis as above (its line 3); a declared schedule is not evidence that a job ran | Provenance lines read; content not yet reviewed | Document 08, section 9 |
| SRC-44 | `LEGACY_SYSTEM_MANUAL_INDEX.md` (124 lines; SHA-256 `dfe1ac19890df8fffc450adb627b49fcebe73d8545c91ac5ff83448de46c3287`) | algocore_system, folder above | `6574d4c` | Existing technical record: index of a 25-chapter manual, of which only these five files are admitted | 24 Master manual index | HISTORICAL: evidence basis as above (its lines 8 and 12 to 13); its line 3 records Rama's statement, dated 17-Sep-2026, that the system is DEAD / REFERENCE ONLY | Provenance lines read; content not yet reviewed | Document 08, section 9 |

### 2.4 Runtime and external evidence

| Ref | Filename | Repository or upload location | Commit | Source type | Relevant topic | Evidence status | Inspection status | Related document |
|---|---|---|---|---|---|---|---|---|
| SRC-50 | The production VM's runtime state: database, logs, crontab, installed units and environment file | The production VM (terminated) | — | Runtime evidence | 3, 13, 15, 16, 17 and 20 | MISSING / UNAVAILABLE. REPORTED BY RAMA — NOT INDEPENDENTLY VERIFIED: both legacy VMs were terminated and no backup of their databases, logs or crontab is known (05-Oct-2026; Document 06, section 4.2) | Not inspectable | Document 06, section 4.2 |
| SRC-51 | Additional external evidence from Rama | None supplied | — | External evidence | — | REPORTED BY RAMA — NOT INDEPENDENTLY VERIFIED: None supplied by Rama as additional external evidence as of 04-Nov-2026. Rama reports that Telegram and email contain routine production-system alerts only. | Not applicable: nothing supplied. If Rama later supplies particular messages, the inventory is updated then | Document 06, section 4.2; section 3, Q2 |

## 3. Questions put to Rama

**Q1. The Phase 1 study baseline — DECIDED.** Rama chose `970aabf`, the recommended option, and directed that the production system is always the reference system (04-Nov-2026; Decision Register, D-21). Phase 1 notes, topic by topic, where the code changed after the last recorded deployment (`686df1c` and `7d4970a`, 02-Sep-2026).

**Q2. Surviving external evidence — ANSWERED.** Rama: "I do have telegram and emails only & no other records are available" and "Both telegram & emails are similar to production system alerts (nothing special)" (note to ChatGPT, 04-Nov-2026). No additional external evidence is supplied for admission (SRC-51).

**Related documents:** 02, 04, 06, 07, 08 and 10; Decision Register, D-03, D-12, D-13, D-16, D-17, D-19, D-20 and D-21.
