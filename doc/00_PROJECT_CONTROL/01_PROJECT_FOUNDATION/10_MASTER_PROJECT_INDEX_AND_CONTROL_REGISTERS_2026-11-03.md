# 10 — Master Project Index & Control Registers

**Status:** DRAFT — Revision 3, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report. Revision 3, 2026-11-04: section 5 names the Decision Register's folder; section 8 states where the one authoritative Source Inventory is kept; section 11 adds a status column and closes OI-01 and OI-05 (Decision Register, D-01, D-03 and D-04).

## 1. Purpose

Provide a central navigation and tracking point for the project.

The Master Index identifies the authoritative documents, investigation topics, progress status, decisions and outstanding issues.

## 2. Master document index

| ID | Document | File |
|---|---|---|
| 01 | Project Foundation & Scope | `01_PROJECT_FOUNDATION_AND_SCOPE_2026-11-03.md` |
| 02 | Project Phases & Master Workflow | `02_PROJECT_PHASES_AND_MASTER_WORKFLOW_2026-11-03.md` |
| 03 | AI Roles, Responsibilities & Operating Instructions | `03_AI_ROLES_RESPONSIBILITIES_AND_OPERATING_INSTRUCTIONS_2026-11-03.md` |
| 04 | Topic Investigation Workflow & AI Continuity Protocol | `04_TOPIC_INVESTIGATION_WORKFLOW_AND_AI_CONTINUITY_PROTOCOL_2026-11-03.md` |
| 05 | Project Governance & Decision Control | `05_PROJECT_GOVERNANCE_AND_DECISION_CONTROL_2026-11-03.md` |
| 06 | Technical Environment, Tools & Research Sources | `06_TECHNICAL_ENVIRONMENT_TOOLS_AND_RESEARCH_SOURCES_2026-11-03.md` |
| 07 | Repository, Documentation & Record Management | `07_REPOSITORY_DOCUMENTATION_AND_RECORD_MANAGEMENT_2026-11-03.md` |
| 08 | Legacy Study & Audit Methodology | `08_LEGACY_STUDY_AND_AUDIT_METHODOLOGY_2026-11-03.md` |
| 09 | New-System Design & Development Phase Framework | `09_NEW_SYSTEM_DESIGN_AND_DEVELOPMENT_FRAMEWORK_2026-11-03.md` |
| 10 | Master Project Index & Control Registers | `10_MASTER_PROJECT_INDEX_AND_CONTROL_REGISTERS_2026-11-03.md` |

Legacy technical manuals, including the existing technical records of Document 08, section 9, are maintained separately under Phase 1.

## 3. Topic completion register

Suggested fields:

| Field | Purpose |
|---|---|
| Topic ID | Unique topic reference |
| Topic name | Investigation subject |
| Scope | Agreed boundaries |
| Phase | Current phase |
| Status | Current workflow stage |
| Study document | Relevant document |
| Audit document | Relevant audit |
| Issues raised with Rama | Count and date of discussion (Document 04, section 5.5) |
| Open issues | Outstanding questions, and issues left OPEN |
| Reviewer | Review responsibility |
| Approval | Required approval |
| Publication reference | Repository path/commit |
| Closure date | Verified closure date |

## 4. Topic workflow statuses

Proposed sequence:

IN PROGRESS → UNDER REVIEW → RECONCILED → PUSH VERIFIED → CLOSED

These are topic statuses, not document statuses.

Whether a topic can close with unresolved issues: a recommended rule is in Document 05, section 11.2 (OPEN FOR RAMA). In every case, unresolved issues stay visible (Document 05, section 11.3).

## 5. Decision register

Record:
- Decision ID.
- Date.
- Subject.
- Exact decision.
- Rationale.
- Evidence.
- Rama approval.
- Affected documents.
- Status.

The Decision Register is kept in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (Document 07, section 3). It uses exactly these nine fields, which Document 05, section 4 also uses.

## 6. Open Issues Register

Record:
- Issue ID.
- Topic.
- Question or discrepancy.
- Evidence.
- Impact.
- Owner.
- Raised with Rama (date).
- Next action.
- Status.
- Resolution.

## 7. Audit Findings Register

Record:
- Finding ID.
- Topic.
- Component.
- Area and flow.
- Finding description.
- Issue category (Document 04, section 5.3).
- Intended behaviour and its source (file, key or passage, line; or Rama's statement and its date).
- Code path (file, function or class, lines, commit).
- Actual behaviour and effective value.
- Evidence.
- Classification.
- Severity or impact where established.
- Raised with Rama (date).
- Agreed treatment (Phase 2 input), or OPEN.
- Status.

## 8. Source inventory

Maintain a source inventory containing:
- Filename.
- Repository or upload location.
- Commit, for repository sources.
- Source type (surviving external runtime evidence is listed with the source type "external evidence" and its origin; Document 06, section 4.2).
- Relevant topic.
- Evidence status.
- Inspection status.
- Related document.

There is one authoritative Source Inventory, kept with the registers in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/` (Document 07, section 3; Decision Register, D-03). Pre-Phase populates and reviews it (Document 02, section 2). `doc/01_PRE_PHASE/01_SOURCE_INVENTORY/` holds only non-authoritative working notes.

## 9. Register governance

Who maintains and verifies each register, and when registers are updated: a recommendation is in Document 05, section 11.1 (OPEN FOR RAMA).

## 10. Continuity rule

Before opening any new topic, both ChatGPT and Claude must review Document 04 and the current Master Index status.

The Master Index and approved project records are the authoritative source for project continuity—not conversational memory.

## 11. Open items at Revision 3

| Ref | Open item | Where | Decides | Status |
|---|---|---|---|---|
| OI-01 | Who creates algocore_system, and its first folder layout, including where the existing technical records go | 06 §3 and §6; 07 §2 and §3; 08 §9 | Rama | CLOSED, 2026-11-04 (Decision Register, D-01): Rama created algocore_system and approved the `doc/` folder layout, in which the files are staged |
| OI-02 | The earlier project's work in trading-system-v2 (39 frozen manuals, A-001 to D-005, and later records): retain as reference material, or set aside | 06 §3 | Rama | OPEN |
| OI-03 | Register responsibilities and update timing | 05 §11.1 | Rama | OPEN |
| OI-04 | Whether a topic can close with unresolved issues | 05 §11.2 | Rama | OPEN |
| OI-05 | Claude's working environment: a new Claude Project, or new instructions in the current one | 06 §6 | Rama | CLOSED, 2026-11-04 (Decision Register, D-04): a dedicated Claude Project, with ChatGPT in a dedicated ChatGPT project |
| OI-06 | Recording "change" and "modify" as REVISE or UPGRADE | 09 §2 | Rama | OPEN |
| OI-07 | Names for the topic document types | 07 §5 | ChatGPT proposes (Claude if ChatGPT does not); Rama | OPEN |

**Related documents:** All project master documents, especially 02, 04, 05, 06, 07 and 08.
