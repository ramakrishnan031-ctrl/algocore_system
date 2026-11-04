# 04 — Topic Investigation Workflow & AI Continuity Protocol

**Status:** APPROVED — Revision 5, mandatory procedure, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report. Revision 5, 2026-11-04: sections 3 and 8 and the cross-reference line name the Master System Investigation Index and the Master Project Index (Document 10, section 1); sections 4 and 11 state the topic review and approval steps, in which ChatGPT reviews the topic package and reports to Rama, and Rama approves or rejects it (Decision Register, D-11); changes are listed in the Revision 5 report. This document did not change in Revisions 3 and 4.

## 1. Purpose

This document establishes one common investigation procedure for ChatGPT and Claude.

It prevents investigation drift, inconsistent working methods, loss of context, hallucination and accidental reopening of settled decisions during long discussions or new conversations.

## 2. Mandatory opening rule

Whenever a new topic or subtopic is opened:

**Both ChatGPT and Claude must review this document before starting work.**

They must also review the relevant approved project instructions, previous topic findings and applicable decision records.

Neither AI may assume that remembered conversation context is a substitute for reviewing the authoritative project records.

## 3. Topic opening procedure

Before investigation begins:

1. Identify the topic and its position in the Master System Investigation Index.
2. Confirm the topic's purpose and scope.
3. Identify what is included and excluded.
4. Review related approved documents.
5. Review established decisions and applicable constraints.
6. Review previous findings and open issues.
7. Identify required evidence and expected deliverables.
8. Confirm the investigation sequence.

Material scope ambiguity must be referred to Rama.

## 4. Investigation procedure

This is the procedure for each Phase 1 topic (Document 02, section 3). Follow this sequence:

1. ChatGPT prepares the investigation direction and focused questions.
2. Claude inspects the actual repository, through its local read-only clone (Document 06, section 3), and supporting evidence.
3. Claude records exact source paths, functions/classes, line references and the repository commit studied, where available.
4. Claude traces inputs, logic, validations, outputs, storage and handoffs, and records unknowns (the study).
5. ChatGPT independently reviews and challenges the study findings; gaps are returned for follow-up.
6. Claude conducts the technical audit of the whole topic: it compares actual with intended behaviour, looks for every kind of issue (section 5), and records defects, discrepancies and unknowns without silently correcting them.
7. ChatGPT reviews and challenges the audit findings; gaps and discrepancies are returned for follow-up.
8. Every issue found is raised and discussed with Rama, and its agreed treatment, or its OPEN status, is recorded (section 5.5).
9. Findings are reconciled with supporting evidence.
10. Study and audit results are combined into the authoritative topic document, while retaining distinct study and audit sections.
11. Claude prepares the topic package: the topic document and its evidence.
12. ChatGPT reviews every file of the package and reports the result to Rama in short, plain English, including any material defect or unresolved question.
13. Rama approves or rejects the topic document and package. ChatGPT's review alone does not finalise it, and Rama does not perform the technical review. Approval and commits follow Document 07, section 6 (Decision Register, D-11).

## 5. Intended and actual behaviour — the whole-system audit

### 5.1 The rule

For every topic, establish from the code what the system actually does, and compare it with what it was intended to do. Never stop at what a configuration file, a document or a comment says, and never limit the audit to configuration settings.

Intended behaviour is taken from every source that states or implies it: configuration (YAML, JSON, CSV, and environment variables named by key), documents (manuals, the legacy technical records, README files), comments and docstrings, function and variable names, log and alert texts, earlier records, and Rama's statement of how he intended the system to work (trader matters are his to state; Document 03, section 1). Where no source states the intent, the code is still audited for defects of its own (section 5.3).

### 5.2 Scope: the entire system

The audit covers the entire system, every area and every flow, not one setting or one example (Rama, 03-Nov-2026). For example: market data; signals and strategies; filtering and the trade decision; entry, stop-loss, target and R:R; risk and capital allocation; order placement and order management; positions, exits and square-off; broker reconciliation; alerts and notifications; the kill switch; startup, scheduler and jobs; storage, reports and logs; failure and recovery.

Rama's stop-loss example (a strategy YAML gives one stop-loss, while the system trades with another) is one illustration of the kind of problem, not its limit. Rama has stated that issues of the same nature exist in signals, capital, alerts, order management and other areas (RAMA (STATED), 03-Nov-2026). The audit is expected to find them and to establish each one with evidence.

Flows that cross topics (for example from a signal, through capital allocation and order placement, to the alert) are traced end to end. An issue found at a boundary is recorded against the topic that owns it and cross-referenced from the others.

### 5.3 What the audit looks for

* Intended against actual: a configured value that the code overrides, ignores or replaces with a hardcoded value; a silent default or fallback; a setting read in more than one place, or with different results; a setting defined but never read, or read but never defined; documented or stated behaviour that the code does not implement; implemented behaviour that nothing describes.
* Logic and calculation: a wrong formula, sign, unit, rounding, time or time zone; steps in the wrong order; the same quantity calculated differently in different modules.
* Flow and state: a route that skips a check or guard that another route applies; a state or status not updated, updated twice, or updated inconsistently; signals, orders, positions or alerts duplicated or lost; the same item processed concurrently.
* Failure handling: errors swallowed or only logged; retries that can repeat an order; no safe recovery on restart; alerts that cannot fire, or fire wrongly; silent fallbacks.
* Consistency across components: two modules disagreeing on a value, format or status; duplicated logic; competing sources of truth (for example the system's records against the broker's).
* Weakness: missing validation; hardcoded values; code that still runs although it appears unused; a paper/live difference, where relevant to establishing actual Live behaviour.

The list guides the audit; it does not limit it. The method is set out in Document 08, section 6.

### 5.4 What is recorded

For each item checked, and for each issue:

* The area and flow.
* The intended behaviour and its source (file, key or passage, line; or Rama's statement and its date).
* The code path that produces the actual behaviour (file, function or class, lines, commit).
* The actual behaviour, and the effective value where there is one.
* The evidence.
* The result: match, issue, or UNKNOWN / NOT ESTABLISHED (for example where only runtime evidence could decide it; Document 06, section 4.2), with its classification (section 6).

Matches are recorded too, so that the audit's coverage of the topic is visible. Issues are entered in the Audit Findings Register (Document 10, section 7).

### 5.5 Every issue is discussed with Rama

* Every issue found by Claude or ChatGPT (a bug, discrepancy, override, inconsistency, duplication, missing guard or other weakness) is raised and discussed with Rama, not just listed. Issues may be presented together, in the topic's issue list, with ChatGPT's and Claude's recommendations.
* Rama decides each issue's treatment for the new system, or leaves it OPEN. The agreed treatment is recorded as input to the Phase 2 proposal. An issue left open stays visible in the Open Issues Register (Document 10, section 6; Document 05, section 11.3).
* The discussion does not fix the legacy system. Nothing is corrected in Phase 1, legacy behaviour is never silently corrected in the documentation, and no legacy behaviour or issue becomes a new-system requirement automatically.

## 6. Evidence classification

Use these classifications:

- FACT — directly supported by evidence.
- UNKNOWN / NOT ESTABLISHED — evidence is insufficient.
- INTERPRETATION — reasoned explanation, not directly established.
- HISTORICAL — describes past behaviour or decisions.
- KNOWN DEFECT — demonstrated defect or failure.
- OPEN QUESTION — requires clarification or further investigation.

Do not silently turn an interpretation into a fact.

## 7. Technical evidence standard

Where supported, record:
- Exact file path.
- Repository commit studied.
- Function or class.
- Line reference.
- Configuration key.
- Intended behaviour and its source, beside the actual behaviour and effective value (section 5.4).
- Database table and column.
- API or data source.
- Inputs and outputs.
- Formula or calculation.
- Dependencies.
- Caller and callee.
- Validation and guard.
- Storage or handoff.
- Paper/live distinction where relevant to actual Live behaviour.

## 8. Continuity and context-loss recovery

When a conversation becomes lengthy, a new conversation is opened, or context may have been lost:

1. Reopen this protocol.
2. Review the current topic record.
3. Review the topic status in the Master Project Index (Document 10) and the topic's place in the Master System Investigation Index.
4. Review relevant approved decisions.
5. Review the latest findings and evidence.
6. Review open issues and outstanding instructions.
7. Confirm the last completed step.
8. Resume only from the established position.

Do not reconstruct missing facts from memory or guesswork.

If the record is incomplete, identify the missing information and recover it from the source documents or repository.

## 9. Collaboration and disagreement

ChatGPT and Claude may challenge each other using evidence and reasoning.

Disagreements must be recorded with:
- Competing statements.
- Supporting evidence.
- Missing evidence.
- Impact.
- Required clarification or decision owner.

Rama resolves material project decisions.

## 10. Progress recording

At every meaningful checkpoint record:
- Topic and scope.
- Current status.
- Work completed.
- Evidence collected.
- Findings.
- Issues raised with Rama, and their agreed treatment or OPEN status.
- Decisions.
- Open issues.
- Next action.
- Responsible person or AI.

## 11. Topic closure

Before closure:
- Required investigation is complete.
- The audit of section 5 is complete for every area and flow of the topic.
- Every issue found has been raised with Rama, and its agreed treatment or OPEN status is recorded.
- Study and audit findings are reconciled.
- Unknowns and open questions are recorded.
- ChatGPT has reviewed every file of the topic package and reported the result to Rama (section 4).
- Rama has approved the topic document and package (Document 07, section 6).
- The approved document is committed, and ChatGPT has verified the commit.
- Topic status is updated.

Unresolved issues must not be hidden. Whether they prevent closure follows Document 05, section 11.2 (OPEN FOR RAMA) and Rama's authority.

## 12. Next-topic handover

The next topic must start using this same protocol. Previous decisions and unresolved issues must be carried forward where relevant; open issues stay in the Open Issues Register until resolved.

## 13. Change control

This is a controlled project procedure. Neither AI may silently amend it. Proposed amendments require review and approval under Project Governance (Document 05).

**Mandatory cross-reference:** AI Roles (03), Project Governance (05), Technical Environment & Research Sources (06), Repository & Record Management (07), Legacy Study Methodology (08) and Master Project Index (10).
