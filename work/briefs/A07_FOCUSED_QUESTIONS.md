# A07 STUDY helpers: FOCUSED QUESTIONS (authoritative)

Copied word for word from ChatGPT's A07 investigation direction of 20-Nov-2026, section 8 (lines 118 to 158 of the
direction file as received). Do not paraphrase, renumber or infer missing questions; if a question is unclear, record
it as an OPEN QUESTION in your file and continue.

```
8. FOCUSED INVESTIGATION QUESTIONS

The STUDY should answer, with exact source and line evidence:

A. Strategy selection and eligibility
1. How is the strategy selected for an incoming signal? What identifies the strategy, maps aliases/types and determines the applicable control/taxonomy?
2. What is the actual role of strategies/control.py and strategies/taxonomy.py? Trace all callers and consumers.
3. What does strategy_will_trade(...) evaluate, in what order, with what inputs, defaults and failure behaviour? Which reasons reject or block a strategy, and how are they represented?
4. How are strategy status, enablement, PAPER_ONLY/other modes and lifecycle states read, set, persisted and enforced? Are all routes consistent?
5. How does the strategy's own entry window interact with A01's window control? Establish the interface only; do not take ownership of A01 logic.

B. Screening pipeline and decision semantics
6. What exact sequence runs from the screening call at signal_processor.py L998 through secondary screening, hard gates, quality scoring, entry gates and step execution?
7. What are the inputs, outputs, types, status/reason fields and side effects at every stage? Is ScreeningResult complete and consistently interpreted by callers?
8. Which checks are hard gates (immediate reject/block), which are scores/rankings, and which can advance or defer a signal? Are names, comments and actual semantics aligned?
9. What are the exact thresholds, units, formulae, weights, score aggregation, rounding and boundary conditions? Trace configured values to effective runtime values; do not assume configuration is used as declared.
10. What does each reject, accept, advance, skip, pending or resume outcome mean? Which state/status is written, by whom, when and where?
11. Can a signal bypass a gate, enter a later step without satisfying an earlier one, be evaluated twice, be lost, be accepted after a prior rejection, or be left in an ambiguous state?
12. How do step_executor.py and continue_from_gate interact? Establish the actual resume/re-entry path, all callers and whether the path is reachable in production rather than tests only.
13. What happens on missing, malformed, stale or contradictory inputs; exceptions; unavailable market/context data; database failures; and partial writes? Are failures surfaced, swallowed, logged, retried or converted to a default decision?

C. Technical and downstream interfaces
14. What technical-analysis/S&R information does A07 consume, where is it produced, and how does A07 treat absent, stale, invalid or conflicting values? A08 owns the calculation.
15. What exact decision/output is handed to A09, and what is explicitly not decided by A07 (entry price, R:R, stop, target, quantity, risk and capital)?
16. How are strategy-control, screener, quality, entry-gate and downstream status vocabularies mapped? Identify mismatched or lossy translations.
17. What is passed to regime/ and v3_chain/ call sites, and what results return? Distinguish A07's integration from A18's internal logic.

D. Scheduled scripts and strategy governance
18. What does compute_strategy_metrics.py calculate, read, write and change? Can it set PAPER_ONLY or otherwise alter eligibility? What conditions trigger that change, and what is the exact handoff to A09's governor/capital logic?
19. What does strategy_registry_officer.py do, including all database writes, strategy state changes, alerts, file writes and failure behaviour? What is its interaction with A03 persistence and A16 scheduling?
20. What does strategy_status.py report or mutate? Is its output authoritative, derived, stale, or inconsistent with the control path?
21. Do scheduled functional scripts and live signal processing use the same source of truth and status semantics? Identify race conditions, timing gaps and conflicting updates without assuming jobs ran merely because a cron declaration exists.

E. Whole-flow audit and evidence
22. Trace representative paths end to end: accepted; rejected at each distinct gate; advanced/resumed; strategy disabled/PAPER_ONLY; missing or invalid context; exception/database failure; and any scheduled status change affecting later signals.
23. For every path, identify the effective decision, status transitions, persistence, caller/callee, concurrency/locking, duplicate/loss risk, logging/alerts and downstream handoff.
24. Which intended-behaviour sources exist (configuration, documents, comments, docstrings, names, tests, logs, historical records and Rama's statements)? Where sources conflict or intent is absent, preserve the conflict or mark UNKNOWN / NOT ESTABLISHED.
25. Are there unused, unreachable, partially wired, test-only or planned components? Distinguish repository presence, declared intent and proven production reachability.
26. What is the complete inventory of A07-owned code, scripts, call sites, tests cited as evidence, dependencies and external interfaces at the baseline? Record exclusions and ownership reasons.

These questions guide the work; they do not limit the audit. Record every additional issue found under Document 04 section 5.
```
