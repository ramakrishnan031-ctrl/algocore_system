# Decision Register

**Status:** DRAFT — for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: decisions D-01 to D-05 (consolidated correction instruction of 04-Nov-2026). Second version, 2026-11-04: decisions D-06 to D-09, and the status of D-02 (review instruction of 04-Nov-2026 and Rama's direction of the same day).
**Purpose and scope:** The project's Decision Register (Document 10, section 5). Each entry uses exactly the nine fields of Document 10, section 5. Prepared by Claude for ChatGPT's review; Rama decides (Document 05, section 1).

## D-01 — OI-01: repository creator, folder layout and initial staging

| Field | Entry |
|---|---|
| Decision ID | D-01 |
| Date | 2026-11-04 |
| Subject | OI-01: who creates algocore_system, its first folder layout, and the placement of the 20 initial files |
| Exact decision | The `doc/` folder layout prepared under the OI-01 folder-setup instruction is approved as the documentation layout of algocore_system, and the 20 initial files are placed in it as staged on 04-Nov-2026. Rama is the repository's creator (03-Nov-2026). Scope: folder layout and file placement only. This decision does not authorise publication to GitHub, Pre-Phase, Phase 1, V2 design or development. The layout is recorded in Document 07, section 3. |
| Rationale | As stated in the OI-01 folder-setup instruction (folder and file handling rules 1 to 3): all project documentation under one root, `doc/`; the ten foundation documents kept together and apart from the revision reports, the validation script and the GitHub setup record; the five existing technical records kept in a dedicated folder, apart from future topic-wise documents. No other rationale is recorded. |
| Evidence | CLAUDE_OI01_FOLDER_SETUP_AND_FILE_STAGING_INSTRUCTION_2026-11-04.txt (ChatGPT, on Rama's instruction; sent by Rama on 04-Nov-2026 at 08:46 IST). GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt, section 1 (repository created by Rama on 03-Nov-2026). OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt (staging and file manifest). CHATGPT_REVIEW_OI01_STAGING_PACKAGE_2026-11-04.txt, section 1. CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt, D-01. |
| Rama approval | Rama instructed the folder setup and file staging (OI-01 folder-setup instruction, 04-Nov-2026), and authorised this record through the consolidated correction instruction, which ChatGPT issued on Rama's instruction "Ok proceed." (04-Nov-2026). |
| Affected documents | 06 §3 and §6; 07 §2 and §3; 07 §8; 08 §9; 10 §11 (OI-01). |
| Status | APPROVED. OI-01: CLOSED (Document 10, section 11). |

## D-02 — Publication copies of the five existing technical records

| Field | Entry |
|---|---|
| Decision ID | D-02 |
| Date | 2026-11-04 |
| Subject | Publication copies of the five existing technical records |
| Exact decision | Separate publication copies of the five existing technical records are prepared in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/PUBLICATION_REDACTED_COPIES/`, under the same file names. Exactly four values are masked, wherever they occur: the first trading-account identifier as `[ACCOUNT_ID_1_REDACTED]`, the second as `[ACCOUNT_ID_2_REDACTED]`, the production VM IP address as `[PRODUCTION_VM_IP_REDACTED]` and the testing VM IP address as `[TEST_VM_IP_REDACTED]`. The PC worktree (D: drive) paths and the VM home paths stay unchanged. Each copy starts with a redaction note giving the masked categories and the SHA-256 of its unchanged original. The five originals stay byte-for-byte unchanged, are kept privately and are not published. Scope: publication copies only. The masked values are not written in any copy, note, report or register entry. |
| Rationale | The records contain two VM IP addresses and two trading-account identifiers, kinds of value that the foundation keeps out of its own documents (OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt, section 8). ChatGPT's review: account identifiers and historic infrastructure details should not be published casually in a public repository (CHATGPT_REVIEW_OI01_STAGING_PACKAGE_2026-11-04.txt, section 3). The paths name no person, and they are kept (CLAUDE_RESPONSE_TO_CHATGPT_OI01_REVIEW_2026-11-04.txt, section 2.2; CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt, section 3). |
| Evidence | The four files named under Rationale. CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt, D-02. |
| Rama approval | Authorised by Rama through the consolidated correction instruction, which ChatGPT issued on Rama's instruction "Ok proceed." (04-Nov-2026), adopting ChatGPT's recommendation (supplemental review, section 10). |
| Affected documents | 07 §3; 08 §9; the publication copies of the five existing technical records. |
| Status | APPROVED. The part that keeps the originals private is SUPERSEDED by D-08 (2026-11-04); the redacted copies are kept. |

## D-03 — Location of the Source Inventory

| Field | Entry |
|---|---|
| Decision ID | D-03 |
| Date | 2026-11-04 |
| Subject | Location of the Source Inventory |
| Exact decision | There is one authoritative Source Inventory, kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/`. `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` is kept for temporary, non-authoritative Pre-Phase working notes only, with a README saying so; no second inventory is kept there. Pre-Phase populates and reviews the one register once Pre-Phase is authorised. This decision does not authorise Pre-Phase. |
| Rationale | Document 02, section 2 makes the source and repository inventory a Pre-Phase task, while Document 10, section 8 defines the Source Inventory as a register; one authoritative location prevents two inventories (OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt, section 7.3; CHATGPT_REVIEW_OI01_STAGING_PACKAGE_2026-11-04.txt, section 6; CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt, section 6). |
| Evidence | The three files named under Rationale. CLAUDE_RESPONSE_TO_CHATGPT_OI01_REVIEW_2026-11-04.txt, section 3 (D2). CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt, D-03. |
| Rama approval | Authorised by Rama through the consolidated correction instruction, which ChatGPT issued on Rama's instruction "Ok proceed." (04-Nov-2026). |
| Affected documents | 02 §2; 07 §3; 07 §8; 10 §8; the README in `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/`. |
| Status | APPROVED. |

## D-04 — OI-05: Claude's working environment

| Field | Entry |
|---|---|
| Decision ID | D-04 |
| Date | 2026-11-04 |
| Subject | OI-05: Claude's working environment |
| Exact decision | Claude works on this project in a dedicated Claude Project, "Trading_System-v2_redesign (algocore_system)", and ChatGPT in a dedicated ChatGPT project, "Trading_System-v2_redesign". OI-05 is closed. No other open item changes. |
| Rationale | Rama moved the work to the dedicated Claude Project ("We are continuing Trading_System-v2_redesign in this new Claude Project.", 03-Nov-2026, 20:50 IST), and the setup record says OI-05 is settled once the two new projects are set up (GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt, section 4). |
| Evidence | Rama's message in the Claude Project, 03-Nov-2026, 20:50 IST. GITHUB_ALGOCORE_SYSTEM_SETUP_RECORD_2026-11-03.txt, section 4. CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt, section 5. CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt, D-04. |
| Rama approval | Authorised by Rama through the consolidated correction instruction, which ChatGPT issued on Rama's instruction "Ok proceed." (04-Nov-2026). |
| Affected documents | 06 §6; 10 §11 (OI-05). |
| Status | APPROVED. OI-05: CLOSED (Document 10, section 11). |

## D-05 — Versioning of the validation script

| Field | Entry |
|---|---|
| Decision ID | D-05 |
| Date | 2026-11-04 |
| Subject | Versioning of the validation script |
| Exact decision | `validate_base_files_2026-11-03.py` stays byte-for-byte unchanged, and is not renamed, as the validator of the Revision 2 set. A new script, `validate_base_files_2026-11-04.py`, validates the corrected set and the approved folder and file manifest. Both are kept in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`. |
| Rationale | The Revision 2 correction report records the old script's SHA-256 and its 70/70 result (BASE_FILES_REVISION_2_CORRECTION_REPORT_2026-11-03.txt, sections 3 and 4). The old script cannot validate a later revision or an APPROVED status (OI01_FOLDER_SETUP_AND_FILE_STAGING_REPORT_2026-11-04.txt, section 7.4; CHATGPT_SUPPLEMENTAL_REVIEW_CLAUDE_RESPONSE_AND_ZIP_2026-11-04.txt, section 7). |
| Evidence | The three files named under Rationale. CLAUDE_RESPONSE_TO_CHATGPT_OI01_REVIEW_2026-11-04.txt, section 3 (D4). CLAUDE_CONSOLIDATED_OI01_FOUNDATION_CORRECTION_INSTRUCTION_2026-11-04.txt, D-05 and section D. |
| Rama approval | Authorised by Rama through the consolidated correction instruction, which ChatGPT issued on Rama's instruction "Ok proceed." (04-Nov-2026). |
| Affected documents | The validation scripts in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`. No foundation document. |
| Status | APPROVED. |

## D-06 — GitHub as the project working repository until the new system design

| Field | Entry |
|---|---|
| Decision ID | D-06 |
| Date | 2026-11-04 |
| Subject | Use of GitHub (algocore_system) during the project |
| Exact decision | "GitHub (`algocore_system`) is the active project working repository and will be used for project documentation, working records and approved deliverables until the new system design is reached. GitHub commits during this period are project-workspace updates, not a declaration that the system or documents are final." Using GitHub needs no separate confirmation from Rama. Document review, decision control and the phase gates are unchanged, and nothing is pushed to the legacy repository. Recorded in Document 07, section 2. |
| Rationale | Rama: "In project files itself I clearly mentioned GitHub will be used till new system design arrived", and "I hate wasting of time" (message to ChatGPT, 04-Nov-2026). |
| Evidence | CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt, section 2. Rama's message to ChatGPT of 04-Nov-2026, in the screenshot Rama gave Claude. |
| Rama approval | Rama's direction, recorded by ChatGPT in the review instruction, and his "proceed" to Claude (04-Nov-2026, 10:29 IST). |
| Affected documents | 07 §2. |
| Status | APPROVED. A standing rule until the new system design is reached. |

## D-07 — Security-issue reporting until Phase 1 is complete

| Field | Entry |
|---|---|
| Decision ID | D-07 |
| Date | 2026-11-04 |
| Subject | Reporting of suspected credential or security leaks |
| Exact decision | Until Phase 1 is complete, no GitHub issues, discussions, pull-request comments, repository warnings or project-register entries are created about suspected credential or security leaks; no separate credential-leak investigation is started; and routine project-documentation work is not interrupted by speculative pattern alerts. This governs reporting and workflow noise only. It is not permission to knowingly commit an actual working credential, private key, token or password: if Claude positively identifies a concrete active credential value in a proposed commit, Claude does not reproduce it, does not push the affected file, and holds only that file for Rama's private direction, without a GitHub issue or public warning. Recorded in Document 07, section 2. |
| Rationale | Rama: "Never flag security credentials leak issues in GitHub or till completion of Phase-1" (message to ChatGPT, 04-Nov-2026), and "Next time onwards don't waste time due credentials/secret resolving issues with GitHub" (message to Claude, 04-Nov-2026, 10:29 IST). |
| Evidence | CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt, section 3. Rama's two messages quoted under Rationale. |
| Rama approval | Rama's direction, as quoted, and his "proceed" (04-Nov-2026). |
| Affected documents | 07 §2. |
| Status | APPROVED. In force until Phase 1 is complete. |

## D-08 — Nothing kept private

| Field | Entry |
|---|---|
| Decision ID | D-08 |
| Date | 2026-11-04 |
| Subject | Which project records go to the public repository |
| Exact decision | Nothing is kept private. Every project record is kept in the public algocore_system repository, including the five existing technical records in their original, unredacted form (in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`, beside their redacted copies, which are kept) and the ChatGPT and Claude instructions, reviews and reports that Claude holds (in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`). Rama accepts the risk. This supersedes the part of D-02 that keeps the originals private, and the review instruction's points O1, O5 and O6 and its section 6 where they keep files out of GitHub. |
| Rationale | Rama: "I accept the risk phase-1 is completed, Don't keep anything private, keep everything must be in public GitHub, proceed" (message to Claude, 04-Nov-2026, 10:29 IST). |
| Evidence | Rama's message quoted under Rationale. CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt, O1, O5, O6 and section 6 (superseded in part). |
| Rama approval | Given by Rama directly to Claude after he read ChatGPT's review instruction ("proceed", 04-Nov-2026, 10:29 IST). Rama is the final decision authority (Document 05, section 1). |
| Affected documents | 07 §2 and §3; 08 §9; the status of D-02; the redaction notes of the five copies; the validator's manifest. |
| Status | APPROVED. |

## D-09 — Revision 3 open points: conventions, decision IDs and OI-07

| Field | Entry |
|---|---|
| Decision ID | D-09 |
| Date | 2026-11-04 |
| Subject | Revision and date convention, README names, decision IDs, and the OI-07 marker |
| Exact decision | O2: the ten foundation files keep their 2026-11-03 file names and Date lines as their creation (baseline) date; each later review round is dated in the revision history; a document that did not change in a round keeps a note such as "This document did not change in Revision 2."; Document 07, section 4 states the convention. O3: `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/README.md` keeps its name, and README files are folder notes excepted from the dated file-name convention (Document 07, section 5). O4: D-01 to D-05 keep their IDs. O7: Document 07, section 5 marks OI-07 as open for Rama; OI-07 stays open. |
| Rationale | ChatGPT's resolutions of the Revision 3 open points ("Apply these resolutions; do not return them as questions"). |
| Evidence | CLAUDE_REV3_REVIEW_GITHUB_WORKSPACE_INSTRUCTION_2026-11-04.txt, section 4. BASE_FILES_REVISION_3_CORRECTION_REPORT_2026-11-04.txt, section 11. |
| Rama approval | Rama's "proceed" to the review instruction (04-Nov-2026). |
| Affected documents | 07 §4 and §5. |
| Status | APPROVED. OI-07 stays OPEN. |

**Related documents:** 05, 07 and 10.
