# A07 STUDY helpers: PART BRIEFS (writer scope per part; read the COMMON brief first)

Your output file: `/home/claude/a07/parts/A07_<NAME>_<IST date>.md` with the NAME given below. "Q" numbers are the
focused questions in `/home/claude/a07/briefs/A07_FOCUSED_QUESTIONS.md` (verbatim from ChatGPT's direction, section
8); answer each one your part is assigned, with evidence, or mark it UNKNOWN / NOT ESTABLISHED with the gap. Record matches as well as anything odd. Trace every route (normal, reject,
skip, error, retry, restart, shutdown), defaults, fallbacks, constants, units, rounding and order of precedence.

## P01 — PRIOR_TOPIC_HANDOFFS (the 51 inherited items and the 10 register entries)
Sources: A01 RTR section 15 and A02 to A06 RTRs section 15.2 (the A07 rows); each item's source AUDIT record and
handoff rows; the Audit Findings Register rows; the Open Issues Register entries A02-03, A03-10, A03-11, A03-36,
A03-37, A05-01, A05-25, A06-02, A06-08 (decided by D-38), A06-12. Start from Claude's notes
`/home/claude/a07/notes/inherited_afr.json`, `inherited_handoff_rows.json`, `oir10.json` (verify them; they are
working notes, not evidence).
Sections: 1 method; 2 table of the 51 (ID, source topic, source record and line, result and classification,
treatment and status as recorded, owner field as recorded, what is handed to A07 in the source's words, the A07
code location to trace, and which A07 part traces it); 3 the 10 register entries (status, owner, what A07 must do);
4 items whose A07 side the source does not state (A03 U-24, U-25 and any other), recorded as such; 5 to 7 as the
COMMON brief. Do not trace the code itself beyond locating it.

## P02 — STRATEGY_CONTROL_TAXONOMY_AND_DIRECTION_REGISTRY
Files: `strategies/control.py`, `strategies/taxonomy.py`, `core/strategy_direction.py`, `strategies/__init__.py`,
`screening/__init__.py`; at the interface: every call site of `strategy_will_trade` (processor L959 to L971, L2062,
L2411; `main.py` L3164 to L3188; `core/config_auditor.py` L268, L306; `scripts/strategy_status.py`), the A02
strategy fields it reads (`intent`, `enabled`, and how `force_intraday_only` and `trade_type` reach it), the
consumers of `build_taxonomy_map` and `build_direction_map`, the seed/state registry paths.
Answer Q1 (how the strategy is identified after A06's lookup: interface only), Q2, Q3, Q4 (lifecycle states: is
PAPER_ONLY or any other state read anywhere on the trading path? search for it), Q5 (interface only), Q16 (the
control-layer vocabulary and the reject labels TRADE_TYPE / STRATEGY_CONTROL and how they become statuses at the
interface). Include whether `strategy_will_trade` can raise (A02 V-06/V-23) and how each caller handles it.

## P03 — SECONDARY_SCREENER_ORCHESTRATION_AND_RESULT
File: `screening/secondary_screener.py` except the step logic (P04) and the scorer/HardGate internals (P05).
Cover: constructor arguments and stored state; `screen()` every route L123 to L374 in order (MIS learned blocklist
pre-drop and its shadow mode; quote fetch and `_build_market_data`; the V3 mode switch and its branches at the
call level; circuit proximity; thresholds from the strategy; executor call and error routes; scorer call; minimum
score and its override; signal-age reject; PASSED); `ScreeningResult` fields; `_persist` (what is written, in what
order, which failures are swallowed); `_evidence_capture`; `shutdown`; the caller's contract at L998 to L1028
(interface) and `_record_screener_stats` (interface). Answer Q6, Q7, Q10 (screener statuses), Q11 (for the
screener), Q13 (for the screener). Record the status strings the screener can write, exactly.

## P04 — STEP_EXECUTOR_AND_THE_TEN_STEPS
File: `screening/step_executor.py`; the market-data dictionary the screener builds (`_build_market_data`, which
fields come from the A04 quote, which are None: vwap, atr, rsi; A05 CM-07, CM-22). For each step: inputs,
threshold source, formula, units, boundary conditions (>= or >), missing-data result, output value range, and
what makes it PASSED, REJECTED or ERROR. Executor: thread pool, timeouts (FIX-091), rotation, `run_all` order,
latencies, error_steps; market-open parameter. Answer Q8 and Q9 for the steps; Q13 for the executor. Cross-check
A02 T-20 (signal-age constants) and A06 PQ-08 (6).

## P05 — QUALITY_SCORER_HARD_GATE_AND_V3_PLAYBOOK_GATES
Files: `screening/quality_scorer.py`, `screening/hard_gate.py` (all of it, including the five playbook gates under
Rama's decision P1: inputs, arithmetic, thresholds, units, missing-data and error behaviour, GateVerdict; A18
callers at the interface only; gate_rr's stop/target/R:R arithmetic recorded faithfully, the decisions staying
A09's), the screener's `_screen_v3_enforce` and `_log_v3_shadow_compare` (the V3 modes), the scoring
configuration it reads (weights, tiers, min_score, v3_* keys; values in `config/scoring_weights.yaml` as FACT about
the file). Answer Q8, Q9 for scoring and gates; Q17 (what passes to and from the regime/V3 call sites; A07 side).

## P06 — ENTRY_GATE_AND_RESUME_CONTRACT
File: `screening/entry_gate.py` in full (WatchEntry fields, constructor, start, rehydration from `gate_state`,
add, persistence calls, remove, poll loop, `_check_one`, quote reads and the quote-failure count, release reasons,
`_release` and the callback, stop, clear_all, threading and locking); at the interface: `main.py` L865 to L893
(pool and callback) and L3839 to L3844, L3975, L1748; A06's `continue_from_gate` (L2010 onwards): its inputs,
outputs, status and decision contract and its handoff to A09, NOT its internal orchestration; the
`strategy_will_trade` call at L2062 (logic in P02); A12's EOD clear call site. Use the fixed entry-gate wording.
Answer Q12, Q10 and Q11 for the gate. Cross-check A03 H-50, Q-11, Q-12, Q-45; A04 RD-12, RL-11; A06 EV-11, PQ-13,
ET-13; A01 B-28, C20.

## P07 — STRATEGY_SCRIPTS
Files: `scripts/compute_strategy_metrics.py`, `scripts/strategy_registry_officer.py`, `scripts/strategy_status.py`
(functional logic). For each: arguments, inputs read (tables, files, configuration), calculations (Sharpe, win
rate, demotion rule with its constants; registry reconcile rules), writes (tables, YAML state, alerts), heartbeat
and non-trading-day handling (interface to A16's helpers), failure behaviour, and declared invocations as
declarations only. Answer Q18 (does anything set PAPER_ONLY or change eligibility? what does the trading path
read?), Q19, Q20, Q21. Cross-check A03 D-05, D-09, E-08; A02 K-05; docs/audit/audit_05jul2026.md as HISTORICAL.

## P08 — CONFIGURATION_KEYS_AND_EFFECTIVE_VALUES
Every configuration key and strategy field that A07 code reads: where (path and line), how (attribute, `getattr`
with default, dict get), the schema default (A02's `core/config_loader.py`, `strategies/schema.py`, interface
only), the committed file value (FACT about the file), any hardcoded fallback in A07 code, and whether any reader
disagrees. Include `trade_type`, `force_intraday_only`, `delivery_enabled`, `entry_gate.*`, `mis_filter.*`,
`scoring.*` (incl. v3_*), the strategy fields used by screening and the gate (min_score, min_volume_surge,
min_adr_pct, max_spread_pct, pullback_wait_*, intent, enabled, direction, order_protocol), the registry paths.
Cross-check A02 T-14, T-20, F-11, K-05, K-27, V-06. Answer Q9 (configured to effective values) for all keys.
Never open the four credential-holding file patterns, even where a key is read from one: name the key only.

## P09 — STATUSES_PERSISTENCE_CONCURRENCY_AND_DUPLICATION
Across A07 code: every `signals.status` value A07 writes (screener, gate) and where; the companion rows
(`insert_screener_result`, `gate_state`, `strategy_metrics`, registry YAML); the order of writes and their commit
boundaries (A03 P-02, P-11 (5)); readers of those statuses and rows outside A07 (interface, by owner); status
vocabulary mapping between control, screener, gate and downstream (Q16); concurrency (processor workers calling
the screener, the executor pool, the gate poll thread, the gate-release pool) and locks; duplication of the same
check or quantity in more than one place (age, circuit, MIS, delivery predicate, scoring thresholds). Answer Q11
(across components), Q14 (any S&R or technical input consumed), Q15 (exactly what is handed to A09 and what A07
does not decide), Q16, Q23 (concurrency, duplicate or loss risk), Q25 (unused, unreachable, test-only components).
Also Q22 (cross-component integration; P09 runs after the P02 to P08 pairs): using the CHECKED P02 to P08 files, not
re-investigating their internal logic, map each representative path Q22 lists (accepted; rejected at each distinct
gate; advanced/resumed; strategy disabled/PAPER_ONLY; missing or invalid context; exception/database failure; any
scheduled status change affecting later signals) step by step across the parts, citing the statement IDs and the
source lines; mark any path or step that cannot be established UNKNOWN / NOT ESTABLISHED with the evidence gap;
preserve ownership boundaries and report conflicts rather than resolving them. Use a section of its own for Q22.

## P10 — LEGACY_RECORDS_INTENT_SOURCES_AND_TESTS
The five existing technical records (`doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`):
every statement about A07 paths, checked against the code (agrees / disagrees / not checkable). The legacy
project's own documents (index rule 11; HISTORICAL): `docs/` (audit notes, locked_decisions.yaml, web_claude module
instructions 29 and 30, v3 plans, SYSTEM_MAP, MASTER_PENDING), PATHS.md, README.md: list each source that states
intent for an A07 component, with the passage location and what it states (brief). The 36 tests (A19): what each
states as expected behaviour for A07 code (one line each; never run). Answer Q24 (which intent sources exist;
conflicts preserved) and Q26 (inventory completeness: anything A07-owned missed by the source file inventory?).

## ADDENDUM 1 (21-Nov-2026, after pair 1) — which inherited items each part cross-references
- Authoritative assignment: the P01 file `/home/claude/a07/parts/A07_PRIOR_TOPIC_HANDOFFS_2026-11-21.md`, section 2.8
  (statement P01-S074), as corrected by the P01 checker. Every writer from P03 onwards reads its own row there and
  cross-references each listed item (ID, source record, and what A07's code does at the cited baseline lines); its
  checker verifies each one. Items keep their owners, IDs, classifications, treatments and statuses.
- The P02 checker adds statements for any item in P02's row that the P02 writer did not cover (marked "added in the
  check").
- A01 B-08, A03 U-24, A03 U-25 and A03 H-17 (its A07 side) go to P09: record the A07 side if one exists at the
  baseline, or "no A07 side found", without changing the source records; B-08's boundary point (the validation it
  names is in `strategies/loader.py`, which the index gives to A02) is reported, not resolved.
- The two handoff points without item IDs (P01-S072): the PAPER_ONLY demotion goes to P07; A06 TG14's "end-of-day
  route's excluded-symbol check" goes to P09 (find the code if any; otherwise UNKNOWN / NOT ESTABLISHED).
- P10 also uses P01's list of records that name A07 as an owner outside the 51 (in the P01 file) when answering Q26.

## ADDENDUM 2 (21-Nov-2026, after the P01 check) — handoff points without item IDs (P01-S126)
Cite these records where your part traces the code (they carry no item ID; none is added to the 51 or re-owned):
- P07: A02 AUDIT L540 (`scripts/compute_strategy_metrics.py` L302 to L306, the `load_config` call and its handler);
  A02 AUDIT L1320 for the officer (L230) and `scripts/strategy_status.py` (L56 to L109).
- P08: A02 AUDIT L1320, the strategy fields each `validate_strategy` caller reads.
- P09: A06 RTR L130, L162 and L347 (a FIX-069 retry re-runs the A07 path; Q11, a signal evaluated twice); the
  boundary summaries A03 RTR L147, A04 RTR L144, A05 RTR L205 and A06 RTR L214 (statuses and rows).
- Assembly (STUDY section 17): A02 AUDIT L1320 for the direction map and taxonomy and A06 AUDIT L4009 for the
  strategy-control gate (both already traced in P02); A06 RTR L663 and L735 (TG7, a Phase 2 input: not traced; the
  shutdown facts are with C20 and PQ-02); A05 RTR L702 (records note on who owns screening; the index governs: A07).

## ADDENDUM 3 (21-Nov-2026, after the P03 writer) — overlapping scope between parts
- `_build_market_data` (screening/secondary_screener.py): P04 owns its content (which fields come from the quote,
  which are None); P03 records it at the call level only. The STUDY cites P04 for it.
- `_screen_v3_enforce` and `_log_v3_shadow_compare`: P05 owns their internals; P03 records the routes into them at
  the call level only (P03 section 5, E1 to E7). P05 cross-references P03's route statements by ID. The STUDY cites
  P05 for the internals and P03 for the routes.
- A scan hit in any helper's file blocks every helper's backup until it is fixed; a blocked helper waits, re-scans
  and retries (never edits another helper's file, never bypasses), as P03 did.
