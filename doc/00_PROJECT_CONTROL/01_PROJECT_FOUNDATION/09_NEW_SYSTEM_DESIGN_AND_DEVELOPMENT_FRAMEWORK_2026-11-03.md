# 09 — New-System Design & Development Phase Framework

**Status:** DRAFT — Revision 2, for ChatGPT review
**Date:** 2026-11-03
**Revision history:** Consolidated framework draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report.

## 1. Purpose

Define the governance framework for the later design and development stages without prematurely designing the new trading system.

## 2. Phase 2 — Design framework

Phase 2 begins only after Phase 1 is fully closed and Rama approves progression.

The design process must:
- Start from the documented Phase 1 findings, including each issue's agreed treatment and the issues still OPEN (Document 04, section 5.5).
- Prepare the new-system proposal.
- Revisit each subject individually, topic by topic, as the Phase 1 topics were run.
- Identify requirements and constraints.
- Evaluate technical and non-technical considerations.
- Discuss and resolve ambiguities, conflicts and gaps.
- Record decisions and reasons.
- Check consistency across subjects.
- Revise the proposal until it is agreed and approved.

For each legacy concept or proposed new capability, the future decision must be classified as:

- RETAIN.
- REVISE.
- UPGRADE.
- REPLACE.
- REJECT.
- NEW.

These are future design outcomes, not decisions made by this framework.

The approved sequence (Document 01, section 5) speaks of deciding what to retain, change, modify, replace or reject. Those decisions use the labels above; "change" and "modify" are recorded as REVISE or UPGRADE. This mapping is proposed in Revision 1 and is OPEN FOR RAMA (Document 10, section 11).

## 3. Phase 2 deliverables

The intended result is a complete, internally consistent, agreed production design and blueprint.

Rama's approval is required before Phase 3 begins.

## 4. Design freeze

When the production design is agreed and approved, it is frozen: the approved design documents become the fixed basis for Phase 3, at the Phase 2 → Phase 3 gate (Document 02, section 6).

After the freeze, any change to the design follows the change control of Document 05, section 5. Nothing is coded against a part of the design that has not been frozen.

## 5. Phase 3 — Development framework

Development is permitted only after:
- Phase 2 is complete.
- The production design is approved and frozen.
- Required developer instructions exist.
- Mandatory subsystem specifications exist.
- Setup and installation prerequisites are available.
- Phase 3 readiness requirements are satisfied.

## 6. Missing prerequisite safeguard

If a required instruction, specification, setup requirement or approval is missing, development must stop.

The missing requirement must be identified to Rama. It must not be invented or silently bypassed.

## 7. Future development guardrails

The project must address the historical risk of:
- Duplicate files.
- Duplicate logic.
- Uncoordinated module changes.
- Inconsistent configuration.
- Behaviour that differs from what was intended, whether configured, documented or stated (the Phase 1 audit, Document 04, section 5).
- Undocumented changes.
- Multiple competing sources of truth.

The actual engineering controls, coding standards, testing standards and deployment procedures must be designed and agreed after Phase 2.

## 8. Scope boundary

This framework does not:
- Design V2 architecture.
- Choose strategies or calculations.
- Specify database schemas.
- Define order-management implementation.
- Authorise coding.
- Authorise Live deployment.

**Related documents:** 01, 02, 04, 05, 06 and 10.
