# A08 STUDY — Part P04 brief (writer): the V2 retest path and its resume handoff

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P04-S001` onwards.
Output file: `/home/claude/a08/parts/A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/P04_WRITER_PROGRESS.md`.
Context parts (checked; cite by statement ID, do not edit): P01, P02, P03 and P07 in `/home/claude/a08/parts/`
(P07 section 7: assignment table; section 6: the retest-ownership wording). Cite P02 for `ZoneCache`/`ZoneWarmer` and
P01 for zone objects; do not re-describe them.

## Boundary (D-41 P1 — read it in the Decision Register)

A08 owns the V2 retest mechanism ("SNR-V2", built in `main.py` L3765 to L3802 under
`sr_detector.wait_for_retest_enabled`; committed value false — a file value, not proof of deployment) and studies it in
full. For `SignalProcessor.continue_from_retest` (`signals/signal_processor.py` L2375 onwards, A06's file) record ONLY:
what the monitor passes in (the `ParkedCandidate` contract and any other arguments), the retest-derived values that
reach it (the zone band, the structure-stop buffer `retest_sl_buffer_pct` — constructor default and the value `main.py`
passes, `sl_buffer_pct` — and the MARKET entry type of the retest entry), and what A08 receives back (return value,
exceptions, status). Do NOT audit its internal orchestration (re-checks, ordering, status writes, calls to A07, A09,
A10, A13): name those call-outs at the interface only, with lines. The PB-01 watchlist retest (A18) is out of scope
except to state, from the code, that it is a distinct mechanism.

## Scope (study in full, every function, every branch)

- `sr_detector/retest_confirm.py` (137 lines): `_is_long`, `RetestParams` (every field: `timeout_sec`, `max_away_pct`,
  `confirm_strong_close_frac`, `breakout_margin_pct`, others), `RetestResult`, the states (`WAIT_BREAKOUT`,
  `WAIT_RETEST`, `WAIT_CONFIRM`, `CONFIRMED`, `REJECT`), `evaluate` (the fold over candles: ordering assumption, every
  transition and its exact price rule for LONG and SHORT, the timeout and its clock, the wrong-way reject, the strong
  close `_strong_close` and its zero-range case), what is returned.
- `screening/retest_monitor.py` (441 lines): `ParkedCandidate` (fields); `RetestMonitor` (constructor, `start`,
  `stop`, `rehydrate` from `retest_state`, parking/adding, the poll loop and its interval, what candles it fetches —
  1-minute? from where? — and how it calls `evaluate`, confirmation → `on_confirm` callback, rejection/timeout handling,
  persistence calls `insert_retest_state` / `update_retest_state` (A03's store: interface only), `clear_all` (called by
  `orders/eod_squareoff.py` L349 to L356 — A12, interface only), repeated triggers, duplicate parking of one symbol,
  threads and locks, exceptions and logging); `RetestDiverter` (`enabled`, `maybe_divert` — called at
  `signals/signal_processor.py` L1042 to L1043, interface only —: the divert decision, the zone lookup in `ZoneCache`,
  what happens on a cache miss/stale zones, which signals are diverted, what it returns to the caller and what status
  the signal gets, the parked record).
- The `retest_state` table at the interface (`core/schema.sql` L1303 to L1336; `core/migrations.py` v38; store methods
  `core/state_store.py` L3017 onwards — A03's): columns written/read, statuses, who else reads it.
- The `continue_from_retest` handoff (boundary above); the `main.py` wiring L3765 to L3802 and the shutdown stop
  (interface only; A01's file); the MARKET entry type in `orders/order_placer.py` L888, L1355,
  `orders/order_protocol_limit.py` L183, L207, `orders/full_entry_engine.py` L85 (A10's: interface only).
- Restart/recovery: what `rehydrate` restores, ordering against `start`, what happens to parked candidates across a
  restart or a day boundary.

## Inherited items

Answer A08's side of every item, open issue and Owner-field record whose PRIMARY part is P04 in P07 section 7 (final:
11 items, 2 open issues, records Q-09, HA-03, EV-01, ET-07, RP-12, and notes N5 and N6), and record P04's side where
P04 is SECONDARY. Never change any item's classification, treatment or status. For A07 SL-06, SL-30, EG-01 and A06
PQ-13 wording, record facts only (D-41 P1).

## Intent sources

Docstrings/comments; tests as stated expectations (`tests/unit/test_sr_v2_retest_confirm.py`,
`tests/unit/test_sr_v2_monitor.py`, `tests/unit/test_sr_v2_divert.py`, `tests/unit/test_sr_v2_continue.py` — the last
at the interface only — and others by git grep); `sr_detector:` configuration comments for the retest keys (committed
values only); legacy documents; git history (HISTORICAL).

## Sections (after section 1, Method)

2. The files: identity, declared purpose, and the three distinct "retest" mechanisms in the code (facts only)
3. `retest_confirm`: parameters, states and `evaluate`
4. `RetestDiverter`: the divert decision and its zone lookup
5. `ParkedCandidate` and `retest_state`
6. `RetestMonitor`: lifecycle, poll loop, confirmation, rejection, persistence
7. Restart, end of day and shutdown (`rehydrate`, `clear_all`, `stop`)
8. The `continue_from_retest` handoff (D-41 P1: inputs, retest-derived values, what comes back; call-outs named only)
9. Threads, locks, clocks and failure behaviour (summary)
10. Call sites in other topics' files (interface only)
11. Inherited items: P04's primary items, then its secondary items
12. Stated intent: docstrings, comments, tests, documents, history
13. Points for the AUDIT
14. UNKNOWN / NOT ESTABLISHED items
15. Questions about intent for Rama
16. Cross-references
