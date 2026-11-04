# 08 — Legacy Study & Audit Methodology

**Status:** APPROVED — Revision 5, approved by Rama on 2026-11-04 (Decision Register, D-19)
**Date:** 2026-11-03
**Revision history:** Consolidated baseline draft, 2026-11-03. Revision 1, 2026-11-03: Rama's clarifications of 03-Nov-2026, ChatGPT's revision instruction of 03-Nov-2026 and Claude's review (Revision 1); changes are listed in the Revision 1 report. Revision 2, 2026-11-03: the audit rule widened to the entire system, every area and flow, not only configuration settings (Rama, 03-Nov-2026); changes are listed in the Revision 2 report. Revision 3, 2026-11-04: section 9 names the approved folder of the existing technical records and of their publication copies (Decision Register, D-01 and D-02). Revision 4, 2026-11-04: section 9 records that the originals are public, beside their redacted copies (Decision Register, D-08). Revision 5, 2026-11-04: section 8 states the topic review and approval steps (D-11); section 9 keeps the existing technical records unchanged, with corrections recorded in the topic documents, records that they and the legacy repository are the admitted legacy sources (D-12), and that their redacted copies were removed (D-18); changes are listed in the Revision 5 report.

## 1. Purpose

Establish how the dead legacy trading system is studied and audited to produce a permanent factual technical record.

The legacy system is the production repository trading-system-prod-snapshot only (Document 01, section 2), studied from a local, read-only clone (Document 06, section 3).

This methodology is for documentation and audit only. It does not authorise legacy repair, modification, tuning or operational revival.

## 2. Scope

The documentation must cover the actual Live legacy system.

Paper-mode workflows are excluded. Shared code may be examined only where necessary to establish actual Live behaviour.

## 3. Required technical documentation coverage

The legacy manual collection must cover:

1. System overview and architecture.
2. Repository and complete file map.
3. Startup, runtime and scheduler.
4. Market data and data sources.
5. Signals and strategies.
6. Filtering and trade decision.
7. Technical analysis and S&R.
8. Entry price and R:R.
9. Risk and capital allocation.
10. Order processing.
11. Order and position management.
12. Exits and square-off.
13. Reconciliation and broker state.
14. Alerts and notifications.
15. Reports, logging and evidence.
16. Database and storage.
17. Configuration.
18. Security, credentials and deployment.
19. Testing and validation.
20. Failure, recovery and operational behaviour.
21. Complete end-to-end system walkthrough.
22. Known issues and historical findings.
23. Legacy lessons and V2 inputs.
24. Master manual index.

## 4. Component documentation standard

For each important component explain:

**SOURCE / CONFIGURATION → INPUT → CALCULATION / LOGIC / OVERRIDE → VALIDATION / GUARD → EFFECTIVE VALUE → OUTPUT (order, state or record) → STORAGE / HANDOFF → NEXT CONSUMER**

Where supported, include:
- Exact file path.
- Repository commit studied.
- Function or class.
- Line reference.
- Configuration key.
- Intended behaviour (configured, documented or stated) and its source, beside the actual behaviour and effective value.
- Database table and column.
- API/source.
- Dependencies.
- Caller and callee.
- Inputs and outputs.
- Examples.
- Paper/live differences where relevant to establishing actual Live behaviour.

## 5. Calculation documentation

For important calculations such as S&R, R:R, stop-loss, target, entry price, buffer, submitted price, quantity, capital allocation, concentration, value caps, strategy conditions and filters, document:

- Input.
- Source.
- Intended value (configured, documented or stated), and its source, beside the value the code actually uses.
- Formula or logic.
- Overrides, defaults and fallbacks, where any apply.
- Transformation.
- Output.
- Consumer.

Do not infer a formula where the implementation does not establish it.

## 6. Auditing actual against intended behaviour

The rule is Document 04, section 5: the audit covers the entire system, every area and flow, not only configuration settings or selected examples such as stop-loss. The audit applies it as follows:

1. From the study, list the topic's components, flows and items, and for each its intended behaviour from every source named in Document 04, section 5.1 (configuration keys and environment variables are named by key, never by value). Questions about Rama's intent are listed together for him.
2. For each item, find every place where the code reads, sets or overrides it, by searching for its name, not only by following the obvious caller.
3. Trace each flow end to end along the chain of section 4, on every route (normal, rejection, error, retry, restart and mode branches), not only the main path, including defaults, fallbacks, hardcoded constants, units, rounding and the order of precedence between sources.
4. At each step, check for every kind of issue in Document 04, section 5.3.
5. Compare the actual behaviour with the intended behaviour, and record a match, an issue, or UNKNOWN / NOT ESTABLISHED (section 10).
6. Record each result in the topic document's audit table, with the fields of Document 04, section 5.4.
7. Enter each issue in the Audit Findings Register (Document 10, section 7), and raise it with Rama (Document 04, section 5.5).

## 7. Fact discipline

Use:
- FACT.
- UNKNOWN / NOT ESTABLISHED.
- INTERPRETATION.
- HISTORICAL.
- KNOWN DEFECT.
- OPEN QUESTION.

Never silently correct the legacy implementation in the documentation.

## 8. Study and audit workflow

For each topic:
1. Establish scope.
2. Review source and relevant history.
3. Trace actual implementation.
4. Record evidence.
5. Prepare the study document.
6. Conduct the separate technical audit of every area and flow of the topic (section 6).
7. Record defects, discrepancies, unknowns and open questions.
8. Raise every issue with Rama, and record its agreed treatment or OPEN status (Document 04, section 5.5).
9. Reconcile study and audit findings into one topic document, keeping distinct study and audit sections.
10. ChatGPT reviews every file of the topic package and reports the result to Rama in short, plain English.
11. Rama approves or rejects the topic document and package; approval and commits follow Document 07, section 6 (Decision Register, D-11).

Who does each step is set out in Document 04, section 4.

## 9. Existing technical records

The following remain separate Phase 1 technical documents:

- `01_SYSTEM_OVERVIEW.md`
- `02_REPOSITORY_AND_FILE_MAP.md`
- `03_STARTUP_RUNTIME_AND_SCHEDULER.md`
- `03A_CRON_REGISTRY_TABLE.md`
- `LEGACY_SYSTEM_MANUAL_INDEX.md`

They are kept unchanged, as historical records, in the legacy technical documentation collection. Where Phase 1 finds a statement in them wrong, the relevant topic document records the correction, with its evidence, and cites the record. They are technical legacy documentation, not replacements for the ten project governance documents, and they keep their separate purpose.

They are source material for Phase 1 topics and, besides the legacy repository itself, the only legacy records admitted by the foundation scope (Document 06, section 3; Decision Register, D-12). This does not authorise Phase 1 investigation. Like any other document, their statements are checked against the code (section 6).

Their approved place in algocore_system is `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/` (Document 07, section 3; Decision Register, D-01). They are kept there unchanged, in their original form, and are public (D-08); their redacted copies (D-02) were removed as duplicates (D-18). Their names do not carry the date suffix (Document 07, section 5).

## 10. Runtime evidence

Runtime evidence is limited (Document 06, section 4.2). A schedule, job or value found in the repository or in a document is not evidence that it ran, or that it was in force; where only runtime evidence could decide a point, it is UNKNOWN / NOT ESTABLISHED.

## 11. Security

Never reproduce actual passwords, API secrets, tokens, TOTP secrets or other credentials. Document only their existence, type and location category.

The public exposure of the production repository is accepted by Rama and is not raised as an issue (Document 06, section 3).

## 12. V2 boundary

Legacy findings are factual inputs for a later design phase. This document does not decide what V2 should retain, reject or redesign.

The agreed treatment of each issue (Document 04, section 5.5) is recorded as Phase 2 input. It does not decide the new design, and it does not change the legacy system.

**Related documents:** 02, 04, 06, 07 and 10.
