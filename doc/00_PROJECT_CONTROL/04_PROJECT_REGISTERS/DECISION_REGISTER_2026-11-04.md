# Decision Register

**Status:** DRAFT — for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: decisions D-01 to D-05 (consolidated correction instruction of 04-Nov-2026). Second version, 2026-11-04: decisions D-06 to D-09, and the status of D-02 (review instruction of 04-Nov-2026 and Rama's direction of the same day). Third version, 2026-11-04: decisions D-10 to D-18, the status of D-02, D-06 and D-08, and the note on evidence files (Rama's decisions of 04-Nov-2026). Fourth version, 2026-11-04: decisions D-19 and D-20, the Foundation → Pre-Phase gate (Rama's decisions of 04-Nov-2026). Fifth version, 2026-11-04: decision D-21, the Phase 1 study baseline and the reference system (Rama's decision of 04-Nov-2026). Sixth version, 2026-11-04: decision D-22, Pre-Phase Deliverable 1 (Rama's decision of 04-Nov-2026). Seventh version, 2026-11-04: decisions D-23 to D-25, the Phase 1 topic sequence, OI-04 and OI-07 (Rama's decisions of 04-Nov-2026). Eighth version, 2026-11-04: decision D-26, the approval of Revision 6 (Rama's decision of 04-Nov-2026). Ninth version, 2026-11-04: decision D-27, the Pre-Phase → Phase 1 gate (Rama's decision of 04-Nov-2026). Tenth version, 2026-11-04: D-27's exact decision and evidence distinguish the Revision 6 commit, at which the deliverables' content was approved, from the gate commit that marked them APPROVED (ChatGPT's verification of the two commits, 04-Nov-2026); the decision is unchanged. Eleventh version, 2026-11-05: decisions D-28 (the names of the topic folders) and D-29 (the index's stale methodology label), Rama's decisions of 05-Nov-2026.
**Purpose and scope:** The project's Decision Register (Document 10, section 5). Each entry uses exactly the nine fields of Document 10, section 5. Prepared by Claude for ChatGPT's review; Rama decides (Document 05, section 1).
**Evidence files:** Instructions, reviews and responses named as evidence are not kept as files in the repository (D-17). Those committed before Revision 5 remain in its Git history, at commit 9898e8c308e8ab8835efd3462aa2f1f97ba1760b; the others were never committed. Each entry states what decides it, and quotes Rama's words where they are the decision (Document 10, section 5).

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
| Status | SUPERSEDED (2026-11-04): the part that keeps the originals private by D-08, and the redacted copies by D-18, which removed them. |

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
| Status | APPROVED. A standing rule until the Phase 2 new-system design is completed and frozen; that end point is defined by D-14 (2026-11-04), and the rest of this decision is unchanged. |

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
| Status | APPROVED. Two parts are SUPERSEDED (2026-11-04): keeping the ChatGPT and Claude instructions, reviews and reports in the repository, by D-17; and keeping the redacted copies beside the originals, by D-18. The rest stands: nothing the repository retains is kept private. |

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

## D-10 — Working commits, foundation-controlled files and approval

| Field | Entry |
|---|---|
| Decision ID | D-10 |
| Date | 2026-11-04 |
| Subject | Which commits need ChatGPT's prior review, and how a document or decision becomes approved (FR-04) |
| Exact decision | A. Working records, and documents explicitly marked DRAFT that are not among the ten foundation documents and are not the validator, may be committed to algocore_system without ChatGPT's prior approval. Claude reports each commit to ChatGPT promptly; ChatGPT reviews it afterwards and identifies any correction needed. A working commit does not make a document approved or frozen, or a decision authoritative. B. Until Rama approves the foundation set, changes to the ten foundation documents and the validator are prepared locally and reviewed by ChatGPT before they are committed; the Revision 5 correction proposal stays local until ChatGPT has reviewed it and Rama has approved the correction set. The working-record rule is not used to bypass this safeguard. C. Rama's explicit decisions are recorded promptly in the Decision Register; an entry may be committed as a working record without ChatGPT's prior approval and is then reviewed by ChatGPT. No decision that Rama has not made is created or inferred. D. A document may be marked APPROVED or frozen, or treated as an authoritative governance decision, only after ChatGPT's review and Rama's explicit approval, subject to the topic-document workflow of D-11. Rama's direct instruction to make a specific commit is sufficient authority for that commit. Claude may not make material project decisions, close open items without Rama's explicit decision, or advance a project phase. Document 07, section 6 states the rule once; the other documents refer to it. |
| Rationale | GitHub is the project's working repository (D-06), and the written rule that files are published only after ChatGPT's approval did not fit working records or commits that Rama directs himself (BASE_FILES_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, FR-04). ChatGPT recommended Option A with explicit boundaries (CHATGPT_REVIEW_AND_RECOMMENDATIONS_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, section 2); Claude's response asked that the ten foundation documents and the validator keep review before commit, and listed every document that restated the old rule (CLAUDE_RESPONSE_TO_CHATGPT_FINAL_REVIEW_RECOMMENDATIONS_2026-11-04.txt, C-01 and C-03). |
| Evidence | The three files named under Rationale. CLAUDE_CONSOLIDATED_REVISION_5_PROPOSAL_INSTRUCTION_2026-11-04.txt, section 3 (D-10 / FR-04). Rama's messages to ChatGPT of 04-Nov-2026, in the screenshot Rama gave Claude at 11:38 IST. |
| Rama approval | Rama's "Accepted for OI-03 & C-03" to ChatGPT (04-Nov-2026), on ChatGPT's text "Ordinary DRAFT working records can follow Option A; the Decision Register can record your decisions immediately and receive ChatGPT's review afterwards", recorded by ChatGPT in the consolidated Revision 5 instruction as Rama's decision on FR-04. Rama then confirmed Option A as a whole: "Accepted" (message to Claude, 04-Nov-2026, 12:26 IST), on ChatGPT's recommendation to approve the complete working-commit rule (CHATGPT_REVISION_5_REMAINING_DECISIONS_AND_OI10_DIRECTION_2026-11-04.txt, section 3, A). |
| Affected documents | 01 §8; 02 §2 and §3; 03 §2 and §3; 04 §4; 05 §5; 06 §2 and §3; 07 §2, §6 and §7; 08 §8. |
| Status | APPROVED. |

## D-11 — Review and approval of Phase 1 topic documents

| Field | Entry |
|---|---|
| Decision ID | D-11 |
| Date | 2026-11-04 |
| Subject | How a Phase 1 topic document and its package are reviewed and approved (C-02) |
| Exact decision | Claude prepares each topic document and its evidence package. ChatGPT reviews every file in the package and reports the result to Rama in short, plain English, including any material defect or unresolved question. Rama then approves or rejects the topic document and package. ChatGPT's approval alone does not finalise a Phase 1 topic document. Rama does not perform the technical review; ChatGPT provides the independent review and a concise explanation. The phase gates still require the complete phase review and Rama's explicit approval. Recorded in Document 07, section 6. |
| Rationale | Rama: "ChatGPT reviews all the files of Claude and informs rama/user about in shortly in plain english then rama/user will approve it" (message to ChatGPT, 04-Nov-2026). Claude had pointed out that Option A, as first recommended, would add Rama's approval of each topic document without asking him (CLAUDE_RESPONSE_TO_CHATGPT_FINAL_REVIEW_RECOMMENDATIONS_2026-11-04.txt, C-02). |
| Evidence | Rama's message quoted under Rationale, in the screenshot Rama gave Claude at 11:38 IST. CLAUDE_CONSOLIDATED_REVISION_5_PROPOSAL_INSTRUCTION_2026-11-04.txt, section 3 (C-02). |
| Rama approval | Rama's explicit decision, as quoted (04-Nov-2026). |
| Affected documents | 02 §3; 03 §1, §2 and §3; 04 §4 and §11; 05 §11.1; 06 §2; 07 §6; 08 §8; 10 §3 and §4. |
| Status | APPROVED. |

## D-12 — OI-02: the other repositories, trading-system-v2 included

| Field | Entry |
|---|---|
| Decision ID | D-12 |
| Date | 2026-11-04 |
| Subject | OI-02: the earlier project's repository trading-system-v2, and every other repository |
| Exact decision | Every repository other than algocore_system (the project's repository) and trading-system-prod-snapshot (the legacy system under investigation, Document 01, section 2) is ignored for this project, trading-system-v2 and trading-system-sbx-snapshot included. They are not opened, cloned, browsed, inventoried, inspected or used; none of their records is used as governing or historical evidence; and no Source Inventory entry is made for them. Besides the legacy repository itself, the five existing technical records already in algocore_system (Document 08, section 9) remain the only admitted legacy records. This does not authorise Phase 1 investigation or any further legacy source discovery. OI-02 is closed. |
| Rationale | Rama: "Other repos I mentioned that is sandbox system+records repo in GitHub, why do we need to look these, not required and also add trading system v2 also since we started to work on new repo Algocore_system" (message to ChatGPT, 04-Nov-2026). Claude had pointed out that Document 01, section 2 already said "all other repositories are ignored", while Document 06, section 3 kept trading-system-v2 open (CLAUDE_RESPONSE_TO_CHATGPT_FINAL_REVIEW_RECOMMENDATIONS_2026-11-04.txt, C-04). The legacy repository stays in scope: Rama's message excludes the other repositories, not the system under investigation. |
| Evidence | Rama's message quoted under Rationale, in the screenshot Rama gave Claude at 11:38 IST. CLAUDE_CONSOLIDATED_REVISION_5_PROPOSAL_INSTRUCTION_2026-11-04.txt, section 3 (OI-02 / C-04 / C-05). |
| Rama approval | Rama's explicit decision, as quoted (04-Nov-2026). |
| Affected documents | 01 §2; 02 §2; 05 §11.1; 06 §3; 08 §9; 10 §8 and §11 (OI-02). |
| Status | APPROVED. OI-02: CLOSED (Document 10, section 11). |

## D-13 — OI-03: register and index governance

| Field | Entry |
|---|---|
| Decision ID | D-13 |
| Date | 2026-11-04 |
| Subject | OI-03: who maintains, reviews and decides the registers and the Master System Investigation Index, and when they are updated |
| Exact decision | ChatGPT identifies the investigation areas, proposes the content and structure of the Master System Investigation Index, reviews it independently and challenges its gaps. Claude maintains the index file in GitHub, incorporating only authorised content and changes. Rama approves the index at the Pre-Phase → Phase 1 gate. Claude maintains the project registers in GitHub. ChatGPT independently reviews register structure, evidence traceability, consistency and proposed status changes. Rama alone approves material decisions, register-governance rules, open-item closures and phase transitions. Claude does not change an open item from OPEN to CLOSED without Rama's explicit approval recorded in the Decision Register. The rule covers the six registers of Document 05, section 11.1 and the separate open items table of Document 10, section 11; the Open Issues Register (Phase 1 topic issues) and the open items table (foundation open items) are not merged. Update timing: (1) Decision Register, immediately after each explicit decision of Rama's, reviewed by ChatGPT after the update; (2) Source Inventory, during Pre-Phase source discovery and whenever an admitted source is added, removed or reclassified, with no entry for ignored repositories; (3) Master System Investigation Index, during Pre-Phase planning and after any topic, order or scope change that Rama approves; (4) Topic Completion Register, whenever a topic's status changes; (5) Audit Findings Register, with each relevant topic package and whenever a finding is corrected, superseded or otherwise changes; (6) Open Issues Register, with each topic package and immediately after Rama decides an issue's treatment; (7) open items table, immediately after Rama decides an open item, together with its Decision Register entry. OI-03 is closed. |
| Rationale | ChatGPT's recommendation keeps repository editing with Claude and independent review with ChatGPT (CHATGPT_REVIEW_AND_RECOMMENDATIONS_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, section 4). Claude's response suggested keeping ChatGPT's role for the index's content, already set by Document 03, section 2, and covering all six registers and the open items table (CLAUDE_RESPONSE_TO_CHATGPT_FINAL_REVIEW_RECOMMENDATIONS_2026-11-04.txt, C-06 and C-07). |
| Evidence | The two files named under Rationale. CLAUDE_CONSOLIDATED_REVISION_5_PROPOSAL_INSTRUCTION_2026-11-04.txt, section 3 (OI-03). Rama's message to ChatGPT, in the screenshot Rama gave Claude at 11:38 IST. |
| Rama approval | Rama: "Accepted for OI-03 & C-03" (message to ChatGPT, 04-Nov-2026), on ChatGPT's summary: ChatGPT identifies the investigation areas and proposes the index content; Claude maintains the index and all six project registers in GitHub; ChatGPT reviews them; Rama approves decisions, closures and the index at the phase gate. |
| Affected documents | 02 §2; 03 §2 and §3; 05 §11.1; 07 §8; 10 §1, §6, §8, §9 and §11 (OI-03). |
| Status | APPROVED. OI-03: CLOSED (Document 10, section 11). |

## D-14 — End of GitHub's working period

| Field | Entry |
|---|---|
| Decision ID | D-14 |
| Date | 2026-11-04 |
| Subject | When the period in which GitHub (algocore_system) is the project's working repository ends (D-06; FR-14) |
| Exact decision | "GitHub is the active project workspace until the Phase 2 new-system design is completed and frozen." The end point is the completion and formal freeze of the Phase 2 design (Document 09, section 4), not the start of Phase 2. It is not an automatic stop to GitHub use after that point; any later repository or workflow arrangement can be decided separately, if needed. This defines the end of D-06's period; the rest of D-06 is unchanged. |
| Rationale | D-06's "until the new system design is reached" named no event and could be read as the start or the freeze of the design (BASE_FILES_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, FR-14; CLAUDE_RESPONSE_TO_CHATGPT_FINAL_REVIEW_RECOMMENDATIONS_2026-11-04.txt, C-10). Rama chose the freeze. |
| Evidence | Rama: "For FR-14: B Until the Phase 2 design is completed and frozen" (message to ChatGPT, 04-Nov-2026), in the screenshot Rama gave Claude at 11:38 IST. CLAUDE_CONSOLIDATED_REVISION_5_PROPOSAL_INSTRUCTION_2026-11-04.txt, section 3 (FR-14 / D-06), which gives the quoted wording. |
| Rama approval | Rama's explicit decision, as quoted (04-Nov-2026). |
| Affected documents | 01 §8; 05 §3; 06 §3; 07 §2; the Status of D-06. |
| Status | APPROVED. |

## D-15 — Versioning of the validation script, Revision 5

| Field | Entry |
|---|---|
| Decision ID | D-15 |
| Date | 2026-11-04 |
| Subject | Which validation script checks the working tree from Revision 5 on |
| Exact decision | `validate_base_files_2026-11-04.py` stays byte-for-byte unchanged as the validator of the Revision 4 baseline. A new script, `validate_algocore_workspace_2026-11-04.py`, validates normal project working trees and, with `--baseline`, the controlled Revision 5 foundation baseline. Claude reports the validation result with each commit (Document 07, section 6). All validators are kept in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`. This continues D-05. |
| Rationale | The Revision 4 script checks a fixed list of files, so it fails on any new working record, and its self-tests fail on a Git checkout (BASE_FILES_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, FR-05 and FR-20). |
| Evidence | The review named under Rationale. CHATGPT_REVISION_5_REMAINING_DECISIONS_AND_OI10_DIRECTION_2026-11-04.txt, section 3, B. |
| Rama approval | Rama: "Accepted" (message to Claude, 04-Nov-2026, 12:26 IST), on ChatGPT's recommendation to approve D-15. |
| Affected documents | 07 §6.5; the validation scripts in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`. |
| Status | APPROVED. |

## D-16 — OI-08 and OI-09: Pre-Phase preparation for Document 08, and the index's minimum content

| Field | Entry |
|---|---|
| Decision ID | D-16 |
| Date | 2026-11-04 |
| Subject | OI-08 and OI-09: how Pre-Phase prepares the application of Document 08, and the minimum content of the Master System Investigation Index |
| Exact decision | OI-08: Pre-Phase prepares how Document 08, which remains the governing Phase 1 methodology, is applied to the indexed topics: their order, depth and deliverables; Pre-Phase does not apply Document 08 to individual modules. OI-09: for each Phase 1 topic, the Master System Investigation Index gives its scope, the components and paths it covers, the coverage items of Document 08, section 3 that it serves, its dependencies and its order. Both wordings are approved as proposed in Revision 5. OI-08 and OI-09 are closed. |
| Rationale | Document 08 is the one Phase 1 methodology, and Pre-Phase only prepares its application; the index needs a defined content before Pre-Phase starts (BASE_FILES_FINAL_SEMANTIC_REVIEW_2026-11-04.txt, FR-12 and FR-13). |
| Evidence | The review named under Rationale. CHATGPT_REVISION_5_REMAINING_DECISIONS_AND_OI10_DIRECTION_2026-11-04.txt, section 3, C and D. |
| Rama approval | Rama: "Accepted" (message to Claude, 04-Nov-2026, 12:26 IST), on ChatGPT's recommendation to approve both as proposed. |
| Affected documents | 02 §1 and §2; 07 §3; 10 §1 and §11 (OI-08, OI-09). |
| Status | APPROVED. OI-08: CLOSED; OI-09: CLOSED (Document 10, section 11). |

## D-17 — OI-10: what the repository retains

| Field | Entry |
|---|---|
| Decision ID | D-17 |
| Date | 2026-11-04 |
| Subject | OI-10: which records the repository keeps permanently |
| Exact decision | The repository keeps the project knowledge and evidence needed to understand, review, propose, design, develop, test and govern the new system: the ten foundation documents and the current governing decisions; the Decision Register, the Master Project Index, the Source Inventory and the other registers; the admitted source records, with their provenance; the Pre-Phase deliverables; the Phase 1 study, audit, reconciliation and final topic documents, with their evidence; the consolidated findings and unresolved issues that affect the new-system proposal; the approved Phase 2 design documents and later development, testing and acceptance records; and only the final approval and revision records that have durable governance or audit value. It does not keep as permanent records: standalone prompts and instructions sent to Claude or ChatGPT; follow-up instructions, chat discussions, routine handoff messages and conversational responses; superseded or intermediate review drafts and duplicate reports; and temporary ZIP files, staging copies and working manifests, once the approved files are committed and verified. A reusable rule in an instruction is written into the governing document it belongs to, and the instruction itself is not kept. The standalone instruction, review and response files are removed from the proposed repository, and only a concise Revision 5 change report is kept. This supersedes the part of D-08 that keeps the ChatGPT and Claude instructions, reviews and reports in the repository. OI-10 is closed. Recorded in Document 07, sections 2 and 3. |
| Rationale | Rama: "No need to all the instructions or follow-up instruction/discussion files why? Core objective is Files to be saved which files are to be reviewed again for new system proposal, So avoid storing non-valued added files or which files not required for future new system redesign & development" (message to ChatGPT, 04-Nov-2026). |
| Evidence | Rama's message quoted under Rationale, in the screenshot Rama gave Claude at 12:26 IST. CHATGPT_REVISION_5_REMAINING_DECISIONS_AND_OI10_DIRECTION_2026-11-04.txt, section 2 and section 3, E. |
| Rama approval | Rama's direction, as quoted, and his "Accepted" (message to Claude, 04-Nov-2026, 12:26 IST). |
| Affected documents | 07 §2, §3 and §7; 10 §5 and §11 (OI-10); the status of D-08; the history folder; the validator's file lists. |
| Status | APPROVED. OI-10: CLOSED (Document 10, section 11). |

## D-18 — Earlier revision reports kept; redacted copies removed

| Field | Entry |
|---|---|
| Decision ID | D-18 |
| Date | 2026-11-04 |
| Subject | How the retention rule (D-17) applies to the earlier revision reports and to the redacted copies of the five existing technical records |
| Exact decision | The change reports of Revisions 1 to 4, with the Revision 2 correction report, are kept: the foundation documents' revision histories and the Decision Register refer to them, and they are final revision records of lasting audit value (D-17). The five redacted copies of the existing technical records, in the subfolder `PUBLICATION_REDACTED_COPIES/` of `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`, are removed with that subfolder, because the five originals are public (D-08) and the copies duplicate them. The five originals are kept, unchanged. The removed copies stay in the repository's Git history. This supersedes the part of D-02 that keeps the copies, and the part of D-08 that keeps them beside the originals. |
| Rationale | ChatGPT's review: the originals are already public, so the copies do not reduce what is exposed, and the original records are the authoritative evidence for the legacy study, the audit and the new-system proposal; the revision reports are referred to by the documents and give a durable audit trail. |
| Evidence | CHATGPT_INDEPENDENT_REVIEW_REVISION_5_REVISED_PACKAGE_2026-11-04.txt, sections 2 to 4, and CLAUDE_REVISION_5_UPDATE_FOR_CHATGPT_REVIEW_2026-11-04.txt, P-1 and P-2; neither is kept as a file (D-17). |
| Rama approval | Rama: "Accepted" (message to Claude, 04-Nov-2026, 12:48 IST), on ChatGPT's recommended reply: "Keep the Revision 1–4 reports as recommended. Remove the five redacted duplicate copies; retain the five original technical records." |
| Affected documents | 05 §3 (example); 07 §3; 08 §9; the status of D-02 and D-08; the validator's folder and file lists. |
| Status | APPROVED. |

## D-19 — Foundation → Pre-Phase gate: the ten foundation documents approved

| Field | Entry |
|---|---|
| Decision ID | D-19 |
| Date | 2026-11-04 |
| Subject | Rama's approval of the ten foundation documents, the second condition of the Foundation → Pre-Phase gate (Document 02, section 6) |
| Exact decision | The ten foundation documents are approved as they stand in algocore_system, branch main, at commit b1927bd, unchanged since the Revision 5 commit 5afdcdf: Documents 01 to 08 and 10 at Revision 5, and Document 09 at Revision 2, its latest revision. Each is to be marked APPROVED (Document 07, sections 4 and 6.3). The approval closes no open item: OI-04, OI-06 and OI-07 stay OPEN (Document 10, section 11). |
| Rationale | ChatGPT's final review of all ten documents found no material blocker and recommended approval; the one minor point it raised, a wording slip in BASE_FILES_REVISION_5_REPORT_2026-11-04.txt, was corrected in commit b1927bd. The validator passes on main: 95 of 95 checks, 96 of 96 with --baseline, and 51 of 51 self-tests. The Revision 5 report records that the foundation approval confirms the approvals that this register quotes from Rama's chat messages (FR-23). |
| Evidence | ChatGPT's final review of Revision 5 and its recommendation to Rama of 04-Nov-2026, and Claude's reports on commits 5afdcdf and b1927bd; none is kept as a file (D-17). |
| Rama approval | Rama: "Accepted" (message to Claude, 04-Nov-2026, 14:39 IST), on ChatGPT's recommendation "I recommend approving the Revision 5 foundation documents and authorising Pre-Phase", which worded this decision: "I approve all ten foundation documents, Revision 5, in algocore_system main." |
| Affected documents | The Status line of Documents 01 to 10; 02 §6 (the gate); 07 §6.2 (from this approval, a change to an approved document follows Document 05, section 5). |
| Status | APPROVED. |

## D-20 — Foundation → Pre-Phase gate: Pre-Phase authorised

| Field | Entry |
|---|---|
| Decision ID | D-20 |
| Date | 2026-11-04 |
| Subject | Rama's authorisation to start Pre-Phase, the third condition of the Foundation → Pre-Phase gate (Document 02, section 6) |
| Exact decision | Pre-Phase is authorised to start under Document 02. With ChatGPT's final review and D-19, the Foundation → Pre-Phase gate is passed. ChatGPT may now issue the Pre-Phase instructions (Document 02, section 2, procedure step 2). Pre-Phase is limited to whole-system knowledge gathering and its five deliverables (Document 02, sections 1 and 2); it includes no individual module investigation, no Phase 1 audit and no V2 design. OI-04, OI-06 and OI-07 stay OPEN and do not block Pre-Phase; OI-04 and OI-07 are to be settled before Phase 1, and OI-06 before Phase 2. Phase 1 needs the Pre-Phase → Phase 1 gate. |
| Rationale | The three conditions of the Foundation → Pre-Phase gate are met: ChatGPT's final review of all ten foundation documents, Rama's explicit approval of them (D-19), and Rama's explicit authorisation to start Pre-Phase. |
| Evidence | ChatGPT's recommendation to Rama of 04-Nov-2026; not kept as a file (D-17). |
| Rama approval | Rama: "Accepted" (message to Claude, 04-Nov-2026, 14:39 IST), on ChatGPT's recommendation, which worded this decision: "I explicitly authorise commencement of Pre-Phase under Document 02. ChatGPT may now issue the Pre-Phase instructions." It also stated: "OI-04 and OI-07 should be settled before Phase 1, and OI-06 before Phase 2." |
| Affected documents | 02 §2 and §6; 10 §11 (the open items, unchanged). |
| Status | APPROVED. The next gate is Pre-Phase → Phase 1 (Document 02, section 6). |

## D-21 — Phase 1 study baseline and the reference system

| Field | Entry |
|---|---|
| Decision ID | D-21 |
| Date | 2026-11-04 |
| Subject | The commit of trading-system-prod-snapshot that the legacy study cites (Document 06, section 6), and which system is the reference |
| Exact decision | The legacy system is studied as the production system held in trading-system-prod-snapshot at commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (branch `main`), and evidence cites this full commit. The production system is always the reference system: material that describes the testing system, including the statements of the five existing technical records that rest on the testing copy, is checked against the production code at that commit (Document 08, section 9). Phase 1 notes, topic by topic, where the code changed after the last recorded deployment (`686df1c` and `7d4970a`, 02-Sep-2026); whether production ran those later commits is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2). |
| Rationale | `970aabf` is the head of the repository's only branch and its last commit (`git ls-remote`, 04-Nov-2026, 15:27 IST); the five existing technical records give it as production's code (`01_SYSTEM_OVERVIEW.md`, lines 27 and 153; `LEGACY_SYSTEM_MANUAL_INDEX.md`, line 13); its full SHA fixes it. Rama: the production and testing repositories differ in the S&R change and configuration settings, so the production system is the valid reference. |
| Evidence | Claude's Pre-Phase checkpoint 1 of 04-Nov-2026, sections 3 and 5 (not kept as a file, D-17); `UNPUSHED_LEDGER.md` at `970aabf`, lines 3456 to 3469 and 3549. Rama's statement on the two repositories is reported by Rama and not independently verified, as the testing repository is ignored (D-12); it agrees with `01_SYSTEM_OVERVIEW.md`, Appendix 01-A (lines 160 to 178), which describes the testing copy as `970aabf` plus the S&R shadow files, with the `force_qty` change set in configuration and in three code files. |
| Rama approval | Rama: "Agreed, Production repo vs sbx repo differs when? S&R Change and Config settings" and "So always review the production system as valid reference system" (message to Claude, 04-Nov-2026, 15:41 IST), on Claude's recommendation of `970aabf`. |
| Affected documents | The Source Inventory, section 1 and SRC-10 to SRC-39; 06 §6 (the commit to be studied, recorded at Pre-Phase); 08 §9. |
| Status | APPROVED. |

## D-22 — Pre-Phase Deliverable 1: the Source Inventory

| Field | Entry |
|---|---|
| Decision ID | D-22 |
| Date | 2026-11-04 |
| Subject | Rama's approval of Pre-Phase Deliverable 1, the Source Inventory, after ChatGPT's review |
| Exact decision | Rama approves Pre-Phase Deliverable 1, the Source Inventory (`SOURCE_INVENTORY_2026-11-04.md`), as committed at `cfa70bc`. Claude may begin Deliverable 2, the whole-system overview, under ChatGPT's Pre-Phase instructions of 04-Nov-2026. This does not pass the Pre-Phase → Phase 1 gate: the five Pre-Phase deliverables are approved together at that gate (Document 02, section 2, step 5, and section 6). The Source Inventory remains the live register that Pre-Phase updates (Document 05, section 11.1, timing rule 2). |
| Rationale | ChatGPT's review of commit `cfa70bc` found no material defect, recommended the inventory for Rama's approval, and accepted the validator's T39 correction. |
| Evidence | ChatGPT's review of the Deliverable 1 commit, 04-Nov-2026 (not kept as a file, D-17); commit `cfa70bcf535400c6e61147bb44bf67fc56f10124`. |
| Rama approval | Rama: "Approved" (message to Claude, 04-Nov-2026, 16:09 IST), on ChatGPT's request: "Please approve or return Deliverable 1". |
| Affected documents | The Source Inventory (its Status line); 02 §2. |
| Status | APPROVED. The approval of the five Pre-Phase deliverables together remains for the Pre-Phase → Phase 1 gate. |

## D-23 — Phase 1 topic sequence

| Field | Entry |
|---|---|
| Decision ID | D-23 |
| Date | 2026-11-04 |
| Subject | The order in which the Phase 1 topics are taken (Master System Investigation Index, rule 9; Pre-Phase Deliverable 5, section 1) |
| Exact decision | Phase 1 topics are taken strictly one at a time, in the order of the approved Master System Investigation Index and subject to its stated prerequisites: the next topic's study begins only after the previous topic package has completed ChatGPT's review and Rama has approved it. If Rama rejects a package, the rework is completed, the corrected package is reviewed again by ChatGPT, and Rama approves it before the next topic begins. Cross-topic dependencies and boundary references are still recorded; the sequence is not evidence of a code dependency. Recorded in Document 02, section 3 and Document 04, section 12. |
| Rationale | ChatGPT's recommendation: it follows "topic by topic" (Document 02, section 3), the 13 steps of Document 04, section 4 and D-11; it reduces context switching and prevents unresolved findings from being carried invisibly into dependent topics. Claude agreed. |
| Evidence | ChatGPT's Pre-Phase → Phase 1 gate recommendation of 04-Nov-2026, section 3A, and its review of Pre-Phase checkpoint 4, section D.2 (not kept as files, D-17). |
| Rama approval | Rama chose "Yes, one at a time (Recommended)", described as "The next topic starts only after the previous one is reviewed and approved (or reworked)", when Claude asked: "Phase 1 topic order: should each topic be finished, reviewed by ChatGPT and approved by you before the next topic starts?" (Claude chat, 04-Nov-2026, between 18:55 and 19:00 IST). The rework path is worded to match the question he answered: a reworked package is reviewed again by ChatGPT and approved by Rama before the next topic starts (ChatGPT's review of the Revision 6 package, 04-Nov-2026). |
| Affected documents | 02 §3; 04 §12; the Master System Investigation Index, rule 9 and section 6; Pre-Phase Deliverable 5, sections 1 and 10. |
| Status | APPROVED. |

## D-24 — OI-04: closing a topic with unresolved issues

| Field | Entry |
|---|---|
| Decision ID | D-24 |
| Date | 2026-11-04 |
| Subject | OI-04: whether a Phase 1 topic can close with unresolved issues (Document 05, section 11.2) |
| Exact decision | A Phase 1 topic may close with unresolved issues only when: every issue found has been raised and discussed with Rama, and Rama has explicitly agreed that each unresolved issue stays open; each such issue is recorded as OPEN in the Open Issues Register with its question, impact, evidence, owner and next action, and is shown in the topic's RECONCILED TOPIC RECORD; the topic's entry in the Topic Completion Register lists its open issues; and the topic's evidence and required coverage are otherwise complete. A topic is not closed to bypass a material evidence gap, an unreviewed contradiction, or an issue that prevents its findings from being reliable. Closure does not mean resolution: open issues stay visible and are carried forward. Recorded in Document 05, section 11.2. OI-04 is closed. |
| Rationale | ChatGPT's recommendation adds two conditions to the rule recommended in Document 05, section 11.2 at Revision 5: Rama's explicit agreement that each issue stays open, and otherwise complete evidence and coverage. The records required by Document 05, sections 8 and 11.3 are kept. |
| Evidence | ChatGPT's Pre-Phase → Phase 1 gate recommendation of 04-Nov-2026, section 3B (not kept as a file, D-17); Document 05, section 11.2 at Revision 5. |
| Rama approval | Rama chose "Yes, with conditions (Recommended)", described as "Only if each open issue was discussed with you, you agreed it stays open, it is recorded and carried forward, and the topic is otherwise complete", when Claude asked: "OI-04: may a Phase 1 topic be closed while some of its issues are still unresolved?" (Claude chat, 04-Nov-2026, between 18:55 and 19:00 IST). |
| Affected documents | 05 §11.2 and §11.3; 04 §11; 10 §4 and §11; the Master System Investigation Index, section 6; Pre-Phase Deliverable 5, sections 8 to 10. |
| Status | APPROVED. OI-04: CLOSED (Document 10, section 11). |

## D-25 — OI-07: names of the topic document types

| Field | Entry |
|---|---|
| Decision ID | D-25 |
| Date | 2026-11-04 |
| Subject | OI-07: the names of the Phase 1 topic document types (Document 07, section 5) |
| Exact decision | The three topic document types are named STUDY, AUDIT and RECONCILED TOPIC RECORD, with the files `<TOPIC_ID>_STUDY_YYYY-MM-DD.md`, `<TOPIC_ID>_AUDIT_YYYY-MM-DD.md` and `<TOPIC_ID>_RECONCILED_TOPIC_RECORD_YYYY-MM-DD.md`; each topic's supporting evidence is kept in an `evidence/` subfolder of its topic folder. The RECONCILED TOPIC RECORD is the authoritative topic document; it keeps distinct the study findings, the audit conclusions, Rama's decisions and the unresolved OPEN items. The names are used consistently in the governing documents and the registers. Recorded in Document 07, section 5. OI-07 is closed. |
| Rationale | ChatGPT proposed the names, as Document 07, section 5 provides: STUDY, AUDIT and RECONCILED TOPIC RECORD in its gate recommendation, and the file-name pattern and the evidence subfolder in its review of Pre-Phase checkpoint 5, section D. The retention rule already keeps the study, audit and reconciled topic documents with their evidence (D-17). |
| Evidence | ChatGPT's Pre-Phase → Phase 1 gate recommendation of 04-Nov-2026, section 3C, and its review of Pre-Phase checkpoint 5, section D (not kept as files, D-17). |
| Rama approval | Rama chose "STUDY, AUDIT, RECONCILED TOPIC RECORD (Recommended)", described as "ChatGPT's latest set. Files: `<topic>_STUDY_<date>.md`, `<topic>_AUDIT_<date>.md`, `<topic>_RECONCILED_TOPIC_RECORD_<date>.md`, plus an `evidence/` subfolder", when Claude asked which of ChatGPT's two sets of names to use (Claude chat, 04-Nov-2026, between 18:55 and 19:00 IST). |
| Affected documents | 07 §3 and §5; 02 §3; 04 §4; 08 §8; 10 §3 and §11; Pre-Phase Deliverable 5, section 8. |
| Status | APPROVED. OI-07: CLOSED (Document 10, section 11). |

## D-26 — Revision 6 of the foundation documents

| Field | Entry |
|---|---|
| Decision ID | D-26 |
| Date | 2026-11-04 |
| Subject | Rama's approval of the Revision 6 foundation document set, after ChatGPT's review |
| Exact decision | Rama approves the Revision 6 foundation document set as reviewed and passed by ChatGPT: Documents 02, 04, 05, 07, 08 and 10 at Revision 6, which carry out D-23 to D-25 and correct the labels carried forward from Revision 5, with the Revision 6 report and the validator change. The six documents are marked APPROVED at Revision 6; Documents 01, 03, 06 and 09 are unchanged. |
| Rationale | ChatGPT's final review of the corrected Revision 6 package (zip SHA-256 `10853baa53c4db390b5a594d8333e4b6333b5bb9e22a076e557df5ac22df8752`) passed it and asked for Rama's explicit approval; a document may be marked APPROVED only after ChatGPT's review and Rama's explicit approval (Document 07, section 6.3). |
| Evidence | ChatGPT's final review of the corrected Revision 6 package, 04-Nov-2026 (not kept as a file, D-17); `BASE_FILES_REVISION_6_REPORT_2026-11-04.txt`. |
| Rama approval | Rama chose "Approve Revision 6 (Recommended)" when Claude asked: "Revision 6: do you approve the revised foundation documents (your three decisions written into Documents 02, 04, 05, 07, 08 and 10) as ChatGPT reviewed and passed them?" (Claude chat, 04-Nov-2026, between 19:25 and 19:31 IST). |
| Affected documents | 02, 04, 05, 07, 08 and 10 (their status lines). |
| Status | APPROVED. |

## D-27 — The Pre-Phase → Phase 1 gate

| Field | Entry |
|---|---|
| Decision ID | D-27 |
| Date | 2026-11-04 |
| Subject | The Pre-Phase → Phase 1 gate (Document 02, section 6): the five Pre-Phase deliverables approved together, and Phase 1 authorised |
| Exact decision | Rama approves the five Pre-Phase deliverables together, in their content as it stood at commit `08b3bcbe1ddba6e7247dbef40709dd20f10ba926` (the Revision 6 commit): the Source Inventory, the whole-system overview, the operational workflows, the Master System Investigation Index and the preparation for applying Document 08. The gate commit that followed, `dcdc0c5f47bb5495d1f1362bce4fe3985e4b8508`, recorded this decision and marked each deliverable APPROVED, changing only its status line and revision history. Pre-Phase is complete and the Pre-Phase → Phase 1 gate is passed: Phase 1 is authorised. It proceeds topic by topic under Document 04 and the approved index, one topic at a time (D-23), starting with A01; its first step is ChatGPT's investigation direction for A01 (Document 04, section 4, step 1). The Source Inventory remains the live register that Phase 1 updates (Document 05, section 11.1). |
| Rationale | ChatGPT reviewed and passed each deliverable (Deliverable 1 was also approved on its own, D-22), recommended the gate on 04-Nov-2026, and passed Revision 6, which settles OI-04 and OI-07 before Phase 1 as D-20 requires and fixes the topic sequence (D-23). The gate needs Pre-Phase completion, ChatGPT's review and Rama's explicit approval (Document 02, section 6). |
| Evidence | ChatGPT's reviews of the five deliverables and its Pre-Phase → Phase 1 gate recommendation, 04-Nov-2026 (not kept as files, D-17); commits `1a81f547b6fd138f9262c9cc40ae249e674b6aa8` (the index), `08b3bcbe1ddba6e7247dbef40709dd20f10ba926` (Revision 6) and `dcdc0c5f47bb5495d1f1362bce4fe3985e4b8508` (the gate commit). |
| Rama approval | Rama chose "Approve the gate, start Phase 1 (Recommended)" when Claude asked: "Pre-Phase → Phase 1 gate: do you approve the five Pre-Phase deliverables together (source inventory, system overview, workflows, investigation index, methodology plan) and authorise Phase 1 to start?" (Claude chat, 04-Nov-2026, between 19:25 and 19:31 IST). |
| Affected documents | The five Pre-Phase deliverables (their status lines); 02 §2 and §6. |
| Status | APPROVED. Pre-Phase is complete; Phase 1 is authorised. The next gate is Phase 1 → Phase 2 (Document 02, section 6). |

## D-28 — The names of the Phase 1 topic folders

| Field | Entry |
|---|---|
| Decision ID | D-28 |
| Date | 2026-11-05 |
| Subject | The names of the Phase 1 topic folders (Document 07, section 3) |
| Exact decision | From A02 onwards, each Phase 1 topic folder under `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/` is named `<TOPIC_ID>_<TOPIC_NAME_IN_UPPERCASE_WITH_UNDERSCORES>`: the topic ID of the approved Master System Investigation Index, then the topic's title in capitals with its words joined by underscores, as A01's folder `A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN` already is. The topic documents keep the file names of D-25. The rule is written into Document 07 at its next revision (Document 05, section 5). |
| Rationale | Document 07, section 3 sets one subfolder per topic but no name. ChatGPT's review of the A01 STUDY recommended making A01's folder name a repeatable convention, subject to Rama's confirmation. |
| Evidence | ChatGPT's A01 STUDY review, 05-Nov-2026, section 5.3 (not kept as a file, D-17); A01's folder, created at commit `97ec3367821d4e1c57ddc835e8a05791f7176d05`. |
| Rama approval | Rama chose "Yes, use that pattern (Recommended)" when Claude asked, on 05-Nov-2026: "Topic folder names from A02 onwards: should every topic folder be named like A01's, i.e. `<TOPIC_ID>_<TOPIC NAME IN CAPITALS WITH UNDERSCORES>` (for example A02_CONFIGURATION_...), as ChatGPT recommends? I'd record it as a decision and add it to Document 07 at its next revision." |
| Affected documents | 07 §3 and §5 (at its next revision); the Phase 1 topic folders. |
| Status | APPROVED. Applied from A02; A01's folder already follows it. |

## D-29 — The stale methodology label in the Master System Investigation Index

| Field | Entry |
|---|---|
| Decision ID | D-29 |
| Date | 2026-11-05 |
| Subject | The index's reference to "Document 08, Revision 5" |
| Exact decision | The index's "Basis and labels" line, which names "Document 08, Revision 5" as the governing methodology while Document 08 is at Revision 6 (D-26), is not corrected on its own: the correction is made at the next authorised update of the index. Document 08 as approved at Revision 6 governs meanwhile. |
| Rationale | Revision 6 changed only Document 08's section 8 (the names of the topic documents), so A01's scope and method do not change. The index is APPROVED and is not edited silently (Document 05, section 5). ChatGPT recommended carrying the correction to the next authorised index update unless Rama wanted a separate correction now. |
| Evidence | The index, line 7; Document 08's revision history; Claude's A01 STUDY handoff of 04-Nov-2026 and ChatGPT's A01 STUDY review of 05-Nov-2026, section 5.2 (not kept as files, D-17). |
| Rama approval | Rama chose "At the next index update (Recommended)" when Claude asked, on 05-Nov-2026: "The approved investigation index still says "Document 08, Revision 5" (Document 08 is now Revision 6; only its file-naming section changed). When should this label be corrected?" |
| Affected documents | The Master System Investigation Index (at its next authorised update). |
| Status | APPROVED. The correction is pending the next authorised update of the index. |

**Related documents:** 01, 02, 03, 04, 05, 06, 07, 08, 09 and 10.
