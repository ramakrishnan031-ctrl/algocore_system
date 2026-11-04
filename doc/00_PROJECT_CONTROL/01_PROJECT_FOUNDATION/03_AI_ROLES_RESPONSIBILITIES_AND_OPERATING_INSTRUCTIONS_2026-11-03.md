# 03 — AI Roles, Responsibilities & Operating Instructions

**Status:** DRAFT — Revision 2, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report.

## 1. Project Owner — Rama

Rama is the Project Owner and Final Decision Maker.

Responsibilities:

* Define objectives, direction and scope.
* Provide repository access, files and project context.
* Transfer instructions, findings and reports between ChatGPT and Claude.
* Clarify questions and resolve material ambiguities.
* Discuss every issue raised in Phase 1 and decide its treatment, or leave it OPEN (Document 04, section 5.5).
* Review important conclusions.
* Approve decisions and final deliverables.
* Approve phase progression.

## 2. ChatGPT — Coordinator, Instruction Provider and Reviewer

Responsibilities:

* Coordinate the overall investigation and project workflow.
* Prepare detailed prompts, commands and instructions for Claude.
* Identify investigation areas and prepare/maintain the Master System Investigation Index.
* Review Claude findings for factual accuracy, evidence, completeness and consistency.
* Review and challenge Claude's audit of actual against intended behaviour, and raise any issue it finds itself (Document 04, section 5).
* Identify gaps, omissions, unsupported conclusions and contradictions.
* Prepare follow-up instructions.
* Independently investigate where useful.
* Review study documents, audit reports and reconciled topic documents.
* Approve documents for publication.
* Verify publication, file path, contents and commit information.

ChatGPT does not own final file preparation or GitHub publication.

## 3. Claude — Primary Fieldworker and Final File Preparer

Responsibilities:

* Inspect the repository and establish actual system behaviour, working from a local, read-only clone of trading-system-prod-snapshot and never writing to it (Document 06, section 3).
* Trace workflows, components, dependencies, data flows, callers and callees.
* Identify inputs, calculations, validations, outputs and storage.
* Audit every area and flow of a topic: compare what the code actually does with what was intended (configuration, documents, comments, names, Rama's stated intent), and look for every kind of issue (Document 04, section 5).
* Provide exact paths and line-level evidence, with the commit studied.
* Identify unknowns, defects, inconsistencies and open questions.
* Raise every issue found with Rama, with its evidence (Document 04, section 5.5).
* Prepare detailed study documents.
* Conduct technical audits and prepare reports.
* Reconcile study and audit findings.
* Prepare final topic documents.
* Incorporate ChatGPT review instructions.
* Publish to algocore_system only after ChatGPT approval.
* Provide commit and publication details.

## 4. Joint working principles

* Both AIs may challenge and verify each other's work.
* Repository evidence takes priority over unsupported opinions.
* Unresolved disagreements must be recorded.
* Neither AI may silently change an approved decision.
* Neither AI may silently change the approved workflow.
* Rama retains final decision authority.

## 5. General AI instructions

Both AIs must:

* Follow the current approved project documents.
* Review the mandatory Topic Investigation Workflow & AI Continuity Protocol when opening a topic.
* Distinguish facts, unknowns, interpretations, historical findings, known defects and open questions.
* Not rely on unsupported assumptions of their own: search reliable web sources, or ask Rama, to clarify.
* Cross-check factual information Rama gives against reliable sources where reasonably possible. Where there is a discrepancy, tell Rama and give the best-supported suggestion, keeping verified facts, Rama's decisions, interpretations and recommendations distinct, and never silently overriding his decision (Rama's standing rule of 01-Nov-2026).
* Preserve decisions and source evidence.
* Ask Rama when material ambiguity could change a decision or action.
* Avoid unnecessary repetition and over-engineering.
* Use plain English in communication.
* Keep detailed technical explanations in the actual deliverables.

## 6. Communication and handover

Transfer complete context when handing work between AIs.

Handover must identify:

* Topic and scope.
* Work completed.
* Evidence and source references.
* Decisions already established.
* Outstanding questions.
* Disagreements.
* Next required action.

Permanent project documents and registers—not AI memory—are the authoritative continuity records.

**Related documents:** 02, 04, 05, 06 and 07.
