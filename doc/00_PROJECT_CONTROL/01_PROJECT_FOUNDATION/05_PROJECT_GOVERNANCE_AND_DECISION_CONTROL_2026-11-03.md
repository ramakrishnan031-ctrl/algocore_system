# 05 — Project Governance & Decision Control

**Status:** DRAFT — Revision 3, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 3, 2026-11-04: section 4 uses the field names of the Decision Register (Document 10, section 5); its guidance is unchanged. This document did not change in Revision 2.

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

Preserve revision history. Do not silently overwrite approved historical records.

## 6. Phase governance

A phase cannot progress merely because an AI considers the work complete.

Required controls:

* Current phase completion.
* ChatGPT review.
* Rama's explicit phase-transition approval.
* Required documentation and records.
* No premature overlap between phases.

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

### 11.1 Register responsibilities — RECOMMENDATION, OPEN FOR RAMA

The registers are defined in Document 10. Recommended responsibilities, following the roles of Document 03:

| Register | Maintains (prepares updates) | Verifies updates | Decides |
|-|-|-|-|
| Master System Investigation Index (Document 02, section 2) | ChatGPT (Document 03, section 2) | Claude, against the repository | Rama, with the Pre-Phase → Phase 1 gate (Document 02, section 6) |
| Topic Completion Register (Document 10, section 3) | Claude, in each topic's final package | ChatGPT, in its publication review | Rama, at the phase gates |
| Decision Register (Document 10, section 5) | Claude records each decision as Rama stated it | ChatGPT, against Rama's stated decision | Rama |
| Open Issues Register (Document 10, section 6) | Claude | ChatGPT | Rama: treatment, or OPEN |
| Audit Findings Register (Document 10, section 7) | Claude | ChatGPT | Rama: treatment, or OPEN |
| Source Inventory (Document 10, section 8) | Claude | ChatGPT | — |

Recommended update timing: registers are updated with each topic's final package and published with it, after ChatGPT approval (Document 07, section 6).

Only the first row's maintainer is already set (by Document 03). The rest of this section is a recommendation until Rama decides it.

### 11.2 Topic closure with unresolved issues — RECOMMENDATION, OPEN FOR RAMA

Recommended rule: a topic may close with unresolved issues, provided that:

* every issue found has been raised and discussed with Rama (Document 04, section 5.5);
* each issue Rama left open is recorded in the Open Issues Register with its question, impact, evidence, owner and next action (section 8), and is shown in the topic document;
* the topic's entry in the Topic Completion Register lists its open issues.

Basis: Rama's stated working rules in the earlier project, that each matter is finalised or explicitly left open and that work then moves on to the next topic. They are not yet confirmed for this project.

### 11.3 Unresolved issues stay visible

Whatever Rama decides under section 11.2, every unresolved issue remains visible and traceable, in the Open Issues Register and in the topic document, until it is resolved or Rama decides its treatment. No issue is silently closed or discarded. Open issues are carried into the next topic where relevant (Document 04, section 12) and into Phase 2.

**Related documents:** 02, 03, 04, 07, 09 and 10.
