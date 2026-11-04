# 07 — Repository, Documentation & Record Management

**Status:** DRAFT — Revision 4, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 3, 2026-11-04: section 2 records that Rama created algocore_system; section 3 replaces the proposed layout with the approved `doc/` layout and states where the registers and the one authoritative Source Inventory are kept; section 8 names the registers' folder (Decision Register, D-01 to D-03). This document did not change in Revision 2. Revision 4, 2026-11-04: section 2 records GitHub as the working repository until the new system design is reached, that nothing is kept private, and the security-issue reporting rule until Phase 1 is complete; section 3 records that the existing technical records are public in their original form and that the history folder holds the revision instructions, reviews and reports; section 4 states the revision and date convention; section 5 states the README exception and marks OI-07 as open for Rama (Decision Register, D-06 to D-09).

## 1. Purpose

Maintain an organised, traceable and durable collection of project records and approved deliverables.

The objective is to prevent scattered information, duplicate authoritative documents, undocumented revisions and loss of project continuity.

## 2. Repository principles

- GitHub is the central location for project documentation and approved deliverables: the new public repository algocore_system (Rama, 03-Nov-2026).
- The legacy production repository is studied from a local, read-only clone; nothing is written to the legacy repository or to its clone (Document 06, section 3).
- Claude maintains the agreed documentation structure.
- ChatGPT reviews documentation and publication readiness.
- Rama approves material structural or governance changes.

Rama created algocore_system on 03-Nov-2026 (Decision Register, D-01). Its first publication is handled separately from the preparation of these base documents, after ChatGPT's approval (section 6).

GitHub (algocore_system) is the active project working repository. It is used for project documentation, working records and approved deliverables until the new system design is reached. GitHub commits in this period are project-workspace updates, not a declaration that the system or the documents are final (Rama, 04-Nov-2026; Decision Register, D-06). Using GitHub needs no separate confirmation from Rama. Document review (section 6), decision control (Document 05) and the phase gates (Document 02, section 6) are unchanged, and nothing is pushed to the legacy repository.

Nothing is kept private. Every project record is kept in this public repository, including the existing technical records in their original form and the AI instructions, reviews and reports; Rama accepts the risk (04-Nov-2026; D-08).

Security-issue reporting until Phase 1 is complete (Rama, 04-Nov-2026; D-07): no GitHub issues, discussions, pull-request comments, repository warnings or register entries are created about suspected credential or security leaks; no separate credential-leak investigation is started; and routine documentation work is not interrupted by speculative pattern alerts. This rule governs reporting only. It is not permission to commit a working credential: if Claude positively identifies a concrete active credential value in a proposed commit, Claude does not reproduce it, does not push the affected file, and holds only that file for Rama's private direction, without any public warning.

## 3. Documentation areas and folder layout

1. Project foundation and governance.
2. Phase 1 legacy study and audit.
3. Phase 2 new-system design.
4. Project-wide decisions and registers.
5. Archive and superseded records.

Legacy documentation (area 2) and new-system design (area 3) are kept in separate areas and are never merged. A Phase 2 document may cite a Phase 1 document; it does not copy or amend it.

Approved folder layout for algocore_system (APPROVED BY RAMA, 04-Nov-2026; Decision Register, D-01). All project documentation is kept under the single root `doc/`:

| Folder | Area | Contents |
|---|---|---|
| `doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/` | 1 | The ten base documents (01 to 10) |
| `doc/00_PROJECT_CONTROL/02_REVISION_AND_VALIDATION_HISTORY/` | 1 | Revision instructions, reviews and reports, and validation scripts |
| `doc/00_PROJECT_CONTROL/03_GITHUB_AND_REPOSITORY_RECORDS/` | 1 | GitHub and repository setup records |
| `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` | 4 | The registers defined in Document 10, including the Decision Register and the one authoritative Source Inventory |
| `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` | 2 | Temporary, non-authoritative Pre-Phase working notes only; not a second Source Inventory |
| `doc/01_PRE_PHASE/02_WHOLE_SYSTEM_OVERVIEW/` | 2 | Pre-Phase whole-system overview |
| `doc/01_PRE_PHASE/03_OPERATIONAL_WORKFLOW/` | 2 | Pre-Phase operational workflows |
| `doc/01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX/` | 2 | The Master System Investigation Index |
| `doc/01_PRE_PHASE/05_PHASE1_METHODOLOGY/` | 2 | The Phase 1 method |
| `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/` | 2 | The existing technical records of Document 08, section 9 |
| `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/PUBLICATION_REDACTED_COPIES/` | 2 | Their redacted copies, with identifying values masked (Decision Register, D-02) |
| `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/` | 2 | One subfolder per Phase 1 topic |
| `doc/03_PHASE2_NEW_SYSTEM_DESIGN/DESIGN_TOPIC_DOCUMENTATION/` | 3 | One subfolder per design topic |
| `doc/99_ARCHIVE/` | 5 | Superseded records |

The registers, including the one authoritative Source Inventory, are kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (Decision Register, D-03). `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` holds only temporary, non-authoritative working notes; no second inventory is kept there.

The existing technical records are kept both in their original form and as redacted copies with identifying values masked (D-02); both are public (D-08).

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

Existing examples that do not follow the date suffix require reconciliation before final publication.

README files are folder notes, not dated project documents. They are named README.md, without a date suffix (D-09).

The names used so far for the topic document types (for example "study file" and "audit file") are illustrative only (Rama, 03-Nov-2026). ChatGPT proposes the names; if it does not, Claude recommends them (OPEN FOR RAMA; Document 10, section 11, OI-07).

## 6. Publication workflow

1. Claude prepares the document.
2. ChatGPT reviews it.
3. Required corrections are completed.
4. ChatGPT approves publication.
5. Claude publishes to algocore_system.
6. Claude supplies commit and publication details.
7. ChatGPT verifies the published path and content.
8. The document status and related registers are updated.

Claude must not publish before the required approval.

Claude's commit messages end with the Co-Authored-By line only; no session link goes into any commit or project record (Rama's standing rule).

## 7. Revision and archival

- Preserve previous approved versions.
- Do not silently overwrite historical decisions.
- Clearly identify superseded documents.
- Keep working drafts separate from authoritative documents.
- Avoid unnecessary permanent files.

## 8. Registers

Maintain central records for:
- Decisions.
- Open issues.
- Topic completion.
- Audit findings.
- Sources (the Source Inventory).

The registers are defined in Document 10 and kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (section 3). Who maintains and verifies each register is recommended in Document 05, section 11.1 (OPEN FOR RAMA).

**Related documents:** 03, 04, 05, 06, 08 and 10.
