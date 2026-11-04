# 02 — Project Phases & Master Workflow

**Status:** APPROVED — Revision 5, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report. Revision 3, 2026-11-04: section 2 states that Pre-Phase populates and reviews the one authoritative Source Inventory (Decision Register, D-03). Revision 5, 2026-11-04: section 1 lists all five Pre-Phase deliverables and names the Master System Investigation Index; section 2 limits the inventory to admitted sources (D-12), states who prepares the Master System Investigation Index (D-13) and how Pre-Phase prepares the application of Document 08 (D-16), and adds the Pre-Phase procedure; section 3 states the topic review and approval steps (D-11); section 6 adds the Foundation → Pre-Phase gate and requires ChatGPT's review and Rama's explicit approval at every gate; changes are listed in the Revision 5 report. This document did not change in Revision 4.

## 1. Overall sequence

The project follows this sequence:

Pre-Phase → Phase 1 → Phase 2 → Phase 3

Phases must not overlap or progress prematurely. Pre-Phase starts only after the foundation documents are approved (section 6).

The approved overall sequence (Document 01, section 5) maps onto the phases as follows:

| Phase | Steps of the approved sequence |
|-|-|
| Pre-Phase | Preparation only: the source and repository inventory, the whole-system overview, the operational workflows, the Master System Investigation Index and the preparation for applying Document 08 (section 2). |
| Phase 1 | Existing system study → technical audit → reconciliation of study and audit → repeated topic by topic until the Master System Investigation Index is complete. |
| Phase 2 | New-system proposal → discussion topic by topic → decide what to retain, change, modify, replace or reject (outcome labels: Document 09, section 2) → resolve ambiguities → revise until agreed and approved → freeze the new system design. |
| Phase 3 | Code and develop, then deploy under controls. |

Legacy documentation (Phase 1) and new-system design (Phase 2) are never merged into the same document (Document 07, section 3).

## 2. Pre-Phase — Whole-System Knowledge Gathering

Purpose:

* Obtain a high-level understanding of the complete Live legacy system.
* Establish source and repository inventory, including the commit of trading-system-prod-snapshot to be studied (Document 06, section 6). Pre-Phase populates and reviews the one authoritative Source Inventory, kept with the project registers (Document 10, section 8); it does not keep a second inventory in its working-notes folder (Document 07, section 3). Only admitted sources are inventoried (Document 06, section 3); ignored repositories are not (Decision Register, D-12).
* Understand broad operational workflows and relationships.
* Prepare the Master System Investigation Index, the list of Phase 1 topics: ChatGPT identifies the investigation areas and proposes its content and structure, Claude keeps the file, and Rama approves it at the Pre-Phase → Phase 1 gate (Document 05, section 11.1; D-13). Its minimum content is in Document 10, section 1 (D-16).
* Prepare how Document 08, which remains the governing Phase 1 methodology, is applied to the indexed topics: their order, depth and deliverables. Pre-Phase does not apply Document 08 to individual modules (Decision Register, D-16).

Pre-Phase is preliminary and occurs before Phase 1.

It is not a deep module investigation, technical audit, repair exercise or V2 design exercise.

Completion criterion: enough high-level knowledge to create a reliable investigation index and guide Phase 1.

Pre-Phase procedure:

1. Pre-Phase starts only when the Foundation → Pre-Phase gate is passed (section 6).
2. ChatGPT issues the Pre-Phase instructions.
3. Claude prepares each Pre-Phase deliverable, following Document 04, sections 2 and 6 to 10, and commits working drafts as Document 07, section 6 allows.
4. ChatGPT reviews each deliverable and reports the result to Rama in short, plain English, including any material defect or unresolved question.
5. Rama approves the Pre-Phase deliverables together at the Pre-Phase → Phase 1 gate (section 6).

## 3. Phase 1 — Legacy System Study and Audit

Investigate the legacy system topic by topic using the approved Master System Investigation Index.

For each topic:

1. Review the Topic Investigation Workflow & AI Continuity Protocol (Document 04).
2. Establish scope and relevant approved context.
3. Conduct preliminary investigation.
4. Prepare focused investigation instructions.
5. Claude performs repository fieldwork and gathers evidence: what the code actually does (the study).
6. ChatGPT reviews findings and identifies gaps.
7. Conduct the detailed technical audit of every area and flow of the topic, reviewed and challenged by ChatGPT: actual code behaviour is compared with intended behaviour, and every kind of issue is looked for (Document 04, section 5; Document 08, section 6).
8. Prepare separate study and audit findings.
9. Raise and discuss every issue found with Rama. Record each issue's agreed treatment as input to Phase 2, or its OPEN status (Document 04, section 5.5).
10. Reconcile both into one authoritative topic document, retaining distinct study and audit sections.
11. ChatGPT reviews every file of the topic package and reports the result to Rama in short, plain English, including any material defect or unresolved question.
12. Rama approves or rejects the topic document and its package; ChatGPT's review alone does not finalise it (Document 07, section 6; Decision Register, D-11).
13. Claude marks the approved document APPROVED and commits it, ChatGPT verifies the commit, and the topic is closed (closure with unresolved issues: Document 05, section 11.2).

The detailed procedure for steps 4 to 13 is Document 04, sections 4 and 11.

Phase 1 must be fully closed before Phase 2.

## 4. Phase 2 — New-System Design

* Prepare an initial new-system proposal from the Phase 1 topic documents, including each issue's recorded treatment and the issues still OPEN.
* Discuss the proposal topic by topic, as the Phase 1 topics were run.
* For each legacy concept or new capability, decide RETAIN / REVISE / UPGRADE / REPLACE / REJECT / NEW (Document 09, section 2).
* Discuss and resolve ambiguity, conflicts, gaps and implications.
* Revise until agreed and approved.
* Check cross-topic consistency.
* Finalise the production design documentation and freeze it (Document 09, section 4).

Rama must approve Phase 2 before Phase 3.

## 5. Phase 3 — Development and Deployment

Development begins only after Phase 2 approval and the design freeze.

Before coding, mandatory prerequisites must exist, including:

* Coder/developer instructions (`instructions.md`).
* Required subsystem instructions and specifications.
* Setup and installation prerequisites.
* Phase 3 readiness requirements.

If mandatory prerequisites are missing, stop and identify them to Rama.

Detailed engineering and deployment standards are to be established separately after Phase 2.

## 6. Phase gates

|Transition|Required approval|
|-|-|
|Foundation → Pre-Phase|ChatGPT's final review of all ten foundation documents, Rama's explicit approval of the ten documents, and Rama's explicit authorisation to start Pre-Phase|
|Pre-Phase → Phase 1|Pre-Phase completion, ChatGPT review and Rama's explicit approval|
|Phase 1 → Phase 2|Phase 1 closure, ChatGPT review and Rama's explicit approval|
|Phase 2 → Phase 3|Approved and frozen production design, ChatGPT review and Rama's explicit approval|
|Phase 3 → Live deployment|Implementation, testing and deployment checks, ChatGPT review and Rama's explicit approval|

No transition, Live deployment included, takes place without ChatGPT's review and Rama's explicit approval (Document 05, section 6). This table authorises no transition by itself.

**Related documents:** 01, 04, 05, 06, 07, 08, 09 and 10.
