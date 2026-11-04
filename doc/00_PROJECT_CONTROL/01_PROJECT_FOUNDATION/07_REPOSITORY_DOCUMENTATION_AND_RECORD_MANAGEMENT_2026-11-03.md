# 07 — Repository, Documentation & Record Management

**Status:** APPROVED — Revision 5, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 3, 2026-11-04: section 2 records that Rama created algocore_system; section 3 replaces the proposed layout with the approved `doc/` layout and states where the registers and the one authoritative Source Inventory are kept; section 8 names the registers' folder (Decision Register, D-01 to D-03). This document did not change in Revision 2. Revision 4, 2026-11-04: section 2 records GitHub as the working repository until the new system design is reached, that nothing is kept private, and the security-issue reporting rule until Phase 1 is complete; section 3 records that the existing technical records are public in their original form and that the history folder holds the revision instructions, reviews and reports; section 4 states the revision and date convention; section 5 states the README exception and marks OI-07 as open for Rama (Decision Register, D-06 to D-09). Revision 5, 2026-11-04: section 2 records the first workspace push, ends GitHub's working period at the completion and freeze of the Phase 2 design (D-14), and makes public what the repository retains (D-17); section 3 names Pre-Phase in area 2 and the place of the preparation for applying Document 08 (D-16), states the retention rule: which records the repository keeps (D-17, which closes OI-10 and supersedes part of D-08), and records that the redacted copies of the existing technical records were removed as duplicates (D-18); section 5 states the file-name exceptions; section 6 becomes the one statement of working commits, foundation-controlled files, approval, validation and commit authorship (D-10, D-11 and D-15); section 7 refers to the retention rule; section 8 records register governance (D-13); changes are listed in the Revision 5 report. Carried forward (Document 05, section 10; Rama, 04-Nov-2026): the label "Proposed document statuses:" in section 4 is corrected in the revision that settles OI-04 and OI-07, before Phase 1.

## 1. Purpose

Maintain an organised, traceable and durable collection of project records and approved deliverables.

The objective is to prevent scattered information, duplicate authoritative documents, undocumented revisions and loss of project continuity.

## 2. Repository principles

- GitHub is the central location for project documentation, working records and approved deliverables: the new public repository algocore_system (Rama, 03-Nov-2026).
- The legacy production repository is studied from a local, read-only clone; nothing is written to the legacy repository or to its clone (Document 06, section 3).
- Claude maintains the agreed documentation structure.
- ChatGPT reviews documentation, commits and topic packages (section 6).
- Rama approves material structural or governance changes.

Rama created algocore_system on 03-Nov-2026 (Decision Register, D-01). The first project-workspace population was pushed on 04-Nov-2026 (commit 9898e8c308e8ab8835efd3462aa2f1f97ba1760b).

GitHub (algocore_system) is the active project working repository. It is used for project documentation, working records and approved deliverables until the Phase 2 new-system design is completed and frozen (Document 09, section 4; Decision Register, D-14). That end point is the completion and formal freeze of the design, not the start of Phase 2, and it is not an automatic stop to GitHub use: any later repository or workflow arrangement is decided separately, if needed. GitHub commits in this period are project-workspace updates, not a declaration that the system or the documents are final (Rama, 04-Nov-2026; D-06). Using GitHub needs no separate confirmation from Rama. Commits and approvals follow section 6; decision control (Document 05) and the phase gates (Document 02, section 6) are unchanged, and nothing is pushed to the legacy repository.

Nothing is kept private: every record the repository retains (section 3) is public, including the existing technical records in their original form; Rama accepts the risk (04-Nov-2026; D-08). Which records are retained is set by the retention rule of section 3 (D-17).

Security-issue reporting until Phase 1 is complete (Rama, 04-Nov-2026; D-07): no GitHub issues, discussions, pull-request comments, repository warnings or register entries are created about suspected credential or security leaks; no separate credential-leak investigation is started; and routine documentation work is not interrupted by speculative pattern alerts. This rule governs reporting only. It is not permission to commit a working credential: if Claude positively identifies a concrete active credential value in a proposed commit, Claude does not reproduce it, does not push the affected file, and holds only that file for Rama's private direction, without any public warning.

## 3. Documentation areas and folder layout

1. Project foundation and governance.
2. Pre-Phase, and Phase 1 legacy study and audit.
3. Phase 2 new-system design.
4. Project-wide decisions and registers.
5. Archive and superseded records.

Legacy documentation (area 2) and new-system design (area 3) are kept in separate areas and are never merged. A Phase 2 document may cite a Phase 1 document; it does not copy or amend it.

Approved folder layout for algocore_system (APPROVED BY RAMA, 04-Nov-2026; Decision Register, D-01). All project documentation is kept under the single root `doc/`:

| Folder | Area | Contents |
|---|---|---|
| `doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/` | 1 | The ten base documents (01 to 10) |
| `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/` | 1 | The change report of each revision round, and the validation scripts (retention rule below) |
| `doc/00_PROJECT_CONTROL/03_GITHUB_AND_REPOSITORY_RECORDS/` | 1 | GitHub and repository setup records |
| `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` | 4 | The registers defined in Document 10, including the Decision Register and the one authoritative Source Inventory |
| `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` | 2 | Temporary, non-authoritative Pre-Phase working notes only; not a second Source Inventory |
| `doc/01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW/` | 2 | Pre-Phase whole-system overview |
| `doc/01_PRE_PHASE/03_OPERATIONAL_WORKFLOW/` | 2 | Pre-Phase operational workflows |
| `doc/01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX/` | 2 | The Master System Investigation Index |
| `doc/01_PRE_PHASE/05_PHASE1_METHODOLOGY/` | 2 | The Pre-Phase preparation for applying Document 08, which remains the governing methodology (D-16) |
| `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/` | 2 | The existing technical records of Document 08, section 9 |
| `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/` | 2 | One subfolder per Phase 1 topic |
| `doc/03_PHASE2_NEW_SYSTEM_DESIGN/DESIGN_TOPIC_DOCUMENTATION/` | 3 | One subfolder per design topic |
| `doc/99_ARCHIVE/` | 5 | Superseded records |

The registers, including the one authoritative Source Inventory, are kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (Decision Register, D-03). `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` holds only temporary, non-authoritative working notes; no second inventory is kept there.

The existing technical records are kept in their original form, and are public (D-08). Their redacted copies (D-02), and the subfolder that held them, were removed as duplicates under the retention rule below (Rama, 04-Nov-2026; D-18); they stay in the repository's Git history.

Retention rule (Rama, 04-Nov-2026; Decision Register, D-17). The repository keeps the project knowledge and evidence needed to understand, review, propose, design, develop, test and govern the new system:

- The ten foundation documents and the current governing decisions.
- The Decision Register, the Master Project Index (Document 10), the Source Inventory and the other registers.
- The admitted source records, with their provenance.
- The Pre-Phase deliverables.
- The Phase 1 study, audit, reconciliation and final topic documents, with their evidence.
- The consolidated findings and unresolved issues that affect the new-system proposal.
- The approved Phase 2 design documents, and the later development, testing and acceptance records.
- Only the final approval and revision records that have durable governance or audit value: the change report of each revision round, and the validation scripts.

It does not keep as permanent records: standalone prompts and instructions sent to Claude or ChatGPT; follow-up instructions, chat discussions, routine handoff messages and conversational responses; superseded or intermediate review drafts and duplicate reports; and temporary ZIP files, staging copies and working manifests, once the approved files are committed and verified. A reusable rule found in an instruction is written into the governing document it belongs to; the instruction itself is not kept. Files removed under this rule stay in the repository's Git history.

Git shows a folder only once it holds a file. Empty folders are not filled with placeholder files.

## 4. Document control

Each document should identify:
- Title.
- Date.
- Status.
- Purpose and scope.
- Version or revision history where applicable.
- Related documents.
- Evidence references where relevant.

Proposed document statuses:

| Status | Meaning |
|---|---|
| DRAFT | Being prepared |
| UNDER REVIEW | Awaiting review |
| APPROVED | Approved authoritative version |
| SUPERSEDED | Replaced by a later approved version |

These statuses are separate from topic workflow statuses.

Revision and date convention (Decision Register, D-09): a document keeps its file name and its Date line, which give its creation (baseline) date. Each later review round is a revision, and the revision history gives its date. A document's status shows the last round that changed it; where a document did not change in a round, its history says so (for example: This document did not change in Revision 2).

## 5. Naming convention

The established convention is:

`<FILE_NAME>_YYYY-MM-DD.<extension>`

Use ISO dates in filenames.

Indian date format may be used in non-code document presentation. Preserve historical dates.

Exceptions: the five existing technical records keep their original names (Document 08, section 9), and README files are named README.md (below).

README files are folder notes, not dated project documents. They are named README.md, without a date suffix (D-09).

The names used so far for the topic document types (for example "study file" and "audit file") are illustrative only (Rama, 03-Nov-2026). ChatGPT proposes the names; if it does not, Claude recommends them (OPEN FOR RAMA; Document 10, section 11, OI-07).

## 6. Commits, approval and validation

This section is the one statement of how files reach algocore_system and how a document or decision becomes approved (Decision Register, D-10 and D-11). The other documents refer to it and do not restate it. algocore_system is public, so a commit to it is publication.

### 6.1 Working commits

1. Working records, and documents marked DRAFT, may be committed without ChatGPT's prior approval, except the foundation-controlled files of section 6.2.
2. Before each commit, Claude runs the current validation script on the tree to be committed (section 6.5). A failure is corrected before the commit, or reported to ChatGPT and Rama with its reason.
3. Claude reports each commit to ChatGPT promptly, with its details and the validation result. ChatGPT reviews it afterwards and identifies any correction needed; Claude makes the correction in a later commit.
4. A working commit does not make a document approved or frozen, or a decision authoritative.
5. Rama's direct instruction to make a specific commit is sufficient authority for that commit.

### 6.2 Foundation-controlled files and the Decision Register

Until Rama approves the foundation set, changes to the ten foundation documents and to the validation script are prepared locally and reviewed by ChatGPT before they are committed, and a correction set is committed only after Rama has approved it. The working-commit rule of section 6.1 is not used to bypass this safeguard. After the foundation is approved, a change to an approved document follows Document 05, section 5.

The Decision Register is a working record. Claude records each explicit decision of Rama's promptly and may commit the entry without ChatGPT's prior approval; ChatGPT then reviews it. No decision that Rama has not made is created or inferred.

### 6.3 Approval

A document may be marked APPROVED or frozen, or treated as an authoritative governance decision, only after ChatGPT's review and Rama's explicit approval. Neither AI makes a material project decision, closes an open item without Rama's explicit decision, or advances a phase.

For a Phase 1 topic (Decision Register, D-11):

1. Claude prepares the topic document and its evidence package.
2. ChatGPT reviews every file of the package and reports the result to Rama in short, plain English, including any material defect or unresolved question. Rama does not perform the technical review.
3. Rama approves or rejects the topic document and package. ChatGPT's review alone does not finalise a topic document.
4. Claude marks the approved document APPROVED, commits it and updates the registers (Document 05, section 11.1); ChatGPT verifies the commit.

Each phase gate still needs the complete phase review and Rama's explicit approval (Document 02, section 6).

### 6.4 Commit messages and author

Claude's commit messages end with the Co-Authored-By line only; no session link goes into any commit or project record (Rama's standing rule). The commit author is Rama's GitHub noreply address, never a personal e-mail address.

### 6.5 Validation script

The current validation script is the latest version in `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/`. It checks a working tree: new working records may be added in the approved folders, under the naming rules of section 5, without a new version of the script. Earlier versions stay unchanged as the validators of their own baselines (Decision Register, D-05 and D-15). A new version, or a change to the script's behaviour, is documented and reviewed by ChatGPT before it is committed.

## 7. Revision and archival

- Preserve previous approved versions.
- Do not silently overwrite historical decisions.
- Clearly identify superseded documents.
- Keep working drafts distinct from authoritative documents: a working draft stays DRAFT until it is approved (section 6.3).
- Avoid unnecessary permanent files: keep only what the retention rule of section 3 lists.

## 8. Registers

Maintain central records for:
- Decisions.
- Open issues.
- Topic completion.
- Audit findings.
- Sources (the Source Inventory).
- The Master System Investigation Index, kept in its Pre-Phase folder (section 3).
- The foundation's open items (Document 10, section 11).

The registers are defined in Document 10 and kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (section 3). Who maintains, reviews and decides each of them, and when each is updated, is set in Document 05, section 11.1 (Decision Register, D-13).

**Related documents:** 03, 04, 05, 06, 08 and 10.
