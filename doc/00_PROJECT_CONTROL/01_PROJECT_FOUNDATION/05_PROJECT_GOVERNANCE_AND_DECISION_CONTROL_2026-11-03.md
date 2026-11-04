# 05 — Project Governance & Decision Control

**Status:** APPROVED — Revision 5, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 3, 2026-11-04: section 4 uses the field names of the Decision Register (Document 10, section 5); its guidance is unchanged. This document did not change in Revision 2. Revision 5, 2026-11-04: section 3 allows a decision to be superseded or clarified in part; sections 5 and 6 refer to the commit and approval rule of Document 07, section 6 and to the gates of Document 02, section 6 (Decision Register, D-10); section 11.1 records Rama's decision on who maintains, reviews and decides the six registers and the open items table, and when each is updated, which closes OI-03 (D-13); changes are listed in the Revision 5 report. This document did not change in Revision 4.

## 1. Authority

Rama is the final decision authority.

ChatGPT provides coordination, review and recommendations. Claude performs fieldwork and prepares deliverables. Neither AI can independently approve a material project decision on Rama's behalf.

## 2. Decision principles

* Preserve established decisions.
* Do not silently change approved decisions.
* Do not convert observations into decisions.
* Do not treat proposals as approved requirements.
* Record unresolved disagreements.
* Support challenges with evidence and reasoning.
* Ask Rama when a material ambiguity could change the decision or action.

## 3. Decision categories

Use clear status labels:

* AGREED / APPROVED.
* PROPOSED.
* UNDER DISCUSSION.
* OPEN QUESTION (marked OPEN FOR RAMA where Rama's decision is needed).
* SUPERSEDED.
* REJECTED.

These labels describe decision status, not document workflow status. A RECOMMENDATION by ChatGPT or Claude remains PROPOSED until Rama decides it.

A decision may be superseded in part, or have a part clarified by a later decision. The Decision Register's Status field then names that part and the later decision (for example, D-08 is superseded in part by D-17 and D-18, and the end of D-06's period is defined by D-14).

## 4. Decision record

Every material decision should record these fields, which are the fields of the Decision Register (Document 10, section 5):

|Field|Description|
|-|-|
|Decision ID|Unique identifier|
|Date|Decision date (always check the current India date from a reliable internet source when recording it)|
|Subject|Topic or affected area|
|Exact decision|Exact agreed outcome|
|Rationale|Supporting rationale|
|Evidence|Relevant sources|
|Rama approval|Rama's approval|
|Affected documents|Affected documents or topics|
|Status|Current decision status|

## 5. Change control

Changes to approved documents must be reviewed by ChatGPT.

If a change affects an established decision, scope, requirement or governance rule, Rama's explicit approval is required.

After the design freeze (Document 09, section 4), any change to the frozen design follows this change control.

How changes reach the repository, and how a document or decision becomes approved, follow Document 07, section 6 (Decision Register, D-10).

Preserve revision history. Do not silently overwrite approved historical records.

## 6. Phase governance

A phase cannot progress merely because an AI considers the work complete.

Required controls:

* Current phase completion.
* ChatGPT review.
* Rama's explicit phase-transition approval.
* Required documentation and records.
* No premature overlap between phases.

The gates, from the Foundation → Pre-Phase gate to Live deployment, and what each requires, are in Document 02, section 6.

## 7. Disagreement handling

Where ChatGPT and Claude disagree:

1. State both positions.
2. Compare source evidence.
3. Identify the exact disagreement.
4. Record what remains unknown.
5. Refer material decisions to Rama.
6. Preserve the resolution in the decision record.

## 8. Open issues

Open issues must identify the question, impact, available evidence, owner and next action.

Unresolved issues must not be silently converted into assumptions, closed or discarded (section 11.3).

## 9. Controlled procedures

The Topic Investigation Workflow & AI Continuity Protocol is a controlled project procedure. Changes require governance review and approval.

## 10. Review-round control

Review findings are of two kinds:

* Material: a finding that could change a fact, an evidence reference, a decision, a rule, the scope, or the meaning of a document.
* Minor: wording, formatting or presentation, with no effect on meaning.

Material findings are corrected, and the correction is reviewed.

When a review round identifies only minor issues:

* The reviewer lists the remaining points.
* Rama decides whether they must be fixed immediately or can be carried forward.
* Review rounds do not continue over minor wording or presentation issues without Rama's direction.

Points carried forward are noted in the document's revision history (Document 07, section 4), so that they are not lost.

## 11. Registers and topic closure

### 11.1 Register responsibilities and update timing

Decided by Rama on 04-Nov-2026 (Decision Register, D-13, which closes OI-03). The registers are defined in Document 10; the roles follow Document 03.

| Register | Maintains | Reviews | Decides |
|-|-|-|-|
| Master System Investigation Index (Document 02, section 2) | ChatGPT identifies the investigation areas and proposes the content and structure; Claude keeps the file in GitHub, with authorised content and changes only | ChatGPT, independently, challenging gaps | Rama, at the Pre-Phase → Phase 1 gate (Document 02, section 6) |
| Topic Completion Register (Document 10, section 3) | Claude | ChatGPT | Rama: each topic document (Document 07, section 6) and the phase gates |
| Decision Register (Document 10, section 5) | Claude records each decision as Rama stated it | ChatGPT, against Rama's stated decision | Rama |
| Open Issues Register (Document 10, section 6) | Claude | ChatGPT | Rama: treatment, or OPEN |
| Audit Findings Register (Document 10, section 7) | Claude | ChatGPT | Rama: treatment, or OPEN |
| Source Inventory (Document 10, section 8) | Claude | ChatGPT | Rama, where a source is to be admitted, removed or reclassified (D-12) |
| Open items table (Document 10, section 11) | Claude | ChatGPT | Rama |

Rules:

* ChatGPT reviews each register's structure, evidence traceability, consistency and proposed status changes. It does not edit the repository's registers, and the content it proposes for the Master System Investigation Index stays its own.
* Claude never changes an open item from OPEN to CLOSED without Rama's explicit decision recorded in the Decision Register.
* Rama alone approves material decisions, register-governance rules, open-item closures and phase transitions.
* The Open Issues Register (the issues of Phase 1 topics) and the open items table (the foundation's open items) are kept separate.
* Register updates are working records: Claude commits them as Document 07, section 6 allows, and ChatGPT reviews them afterwards.

Update timing:

1. Decision Register: immediately after each explicit decision of Rama's; ChatGPT reviews the entry after the update.
2. Source Inventory: during Pre-Phase source discovery, and whenever an admitted source is added, removed or reclassified. Ignored repositories are not inventoried (D-12).
3. Master System Investigation Index: during Pre-Phase planning, and after any topic, order or scope change that Rama approves.
4. Topic Completion Register: whenever a topic's status changes (Document 10, section 4).
5. Audit Findings Register: with each relevant topic package, and whenever a finding is corrected, superseded or otherwise changes.
6. Open Issues Register: with each topic package, and immediately after Rama decides an issue's treatment.
7. Open items table: immediately after Rama decides an open item, together with its Decision Register entry.

### 11.2 Topic closure with unresolved issues — RECOMMENDATION, OPEN FOR RAMA

Recommended rule: a topic may close with unresolved issues, provided that:

* every issue found has been raised and discussed with Rama (Document 04, section 5.5);
* each issue Rama left open is recorded in the Open Issues Register with its question, impact, evidence, owner and next action (section 8), and is shown in the topic document;
* the topic's entry in the Topic Completion Register lists its open issues.

Basis: Rama's stated working rules in the earlier project, that each matter is finalised or explicitly left open and that work then moves on to the next topic. They are not yet confirmed for this project.

### 11.3 Unresolved issues stay visible

Whatever Rama decides under section 11.2, every unresolved issue remains visible and traceable, in the Open Issues Register and in the topic document, until it is resolved or Rama decides its treatment. No issue is silently closed or discarded. Open issues are carried into the next topic where relevant (Document 04, section 12) and into Phase 2.

**Related documents:** 02, 03, 04, 07, 09 and 10.
