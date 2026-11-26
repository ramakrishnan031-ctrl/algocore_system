# A08 STUDY — Part P03 brief (writer): the V1 observer, flags, results storage and the end-of-day backfill

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P03-S001` onwards.
Output file: `/home/claude/a08/parts/A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/P03_WRITER_PROGRESS.md`.
Context parts (checked; cite by statement ID, do not edit): P01
`/home/claude/a08/parts/A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md` and P07
`/home/claude/a08/parts/A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md` (section 7: assignment table). P02 is written at the
same time as P03: for `OhlcFetcher`/`zone_builder` behaviour write "see part P02" with the function name and lines,
without describing their internals.

## Scope (study in full; D-41 P2)

- `sr_detector/__init__.py` (70 lines): `build_sr_detector` — arguments, what it constructs, configuration read,
  defaults, failure behaviour.
- `sr_detector/detector.py` (329 lines): `SRDetector` — constructor, `start`/`stop`, `observe` (called from
  `signals/signal_processor.py` `_sr_observe`, L614 to L658, call sites L1550, L2296 and L2588 — interface only: record
  what each call site passes and when, not the processor's logic), any queue/thread/executor, what it computes per
  candidate (timeframes, fetches via `OhlcFetcher`, zone building, flags), the `SRAnalysis` produced, the
  `sr_detector_results` row it writes (columns, values, JSON payloads via `_json`, timestamps via `_iso`, `_attr`), the
  store method used (`core/state_store.py` L1992 to L2020 — A03's code: interface only), whether it is non-gating in
  fact (can it delay, block, raise into, or alter the order path?), logging, error handling, behaviour when disabled.
- `sr_detector/flags.py` (186 lines): `BreakoutContext`, `FlagParams`, `FlagResult`, `compute_flags_and_retest` and
  every helper (`_breakout_flags`, `_retest_for_long`, `_retest_for_short`, others): every flag and its exact rule,
  thresholds and units, the `RetestProposal` (V1's retest concept — distinct from the V2 retest path of P04 and the
  PB-01 watchlist retest of A18; record the distinction from the code).
- `scripts/sr_detector_backfill.py` (149 lines): `backfill`, `main`, `_cron_main` — arguments, what rows it selects,
  what it computes (end-of-day outcome columns), what it writes, idempotency, date/time-zone handling, failure and exit
  behaviour, logging; declared invocation (A08 inventory section 3: cron 15:58 Mon-Fri — a declaration, not evidence
  it ran; never reproduce the cron line's machine path).
- The `sr_detector_results` table at the interface (`core/schema.sql` L1247 to L1294; `core/migrations.py` v37 — A03's):
  columns A08 writes and reads; readers outside A08 (git grep), named with owners.

## Inherited items

Answer A08's side of every item and open issue whose PRIMARY part is P03 in P07 section 7 (as finally checked),
including any of the 16 Owner-field records assigned to P03 (Rama's decision of 26-Nov-2026,
`/home/claude/a08/notes/RAMA_DECISIONS_A08_STUDY.md`), and record P03's side where P03 is SECONDARY. Never change any
item's classification, treatment or status.

## Intent sources

Docstrings/comments ("SNR-DETECTOR-V1", "non-gating", "shadow"); tests as stated expectations
(`tests/unit/test_sr_detector_observer.py`, `tests/unit/test_sr_detector_backfill.py`, `tests/unit/test_sr_detector_units.py`
and others by git grep); the `sr_detector:` configuration comments (committed values only); legacy documents
(`PATHS.md` — note P01-S129 on `sr_detector.enabled` — `docs/SYSTEM_MAP.md`, others); git history (HISTORICAL).

## Sections (after section 1, Method)

2. The files: identity and declared purpose
3. `build_sr_detector`
4. `SRDetector`: lifecycle, threading, `observe` and the per-candidate computation
5. Flags and the V1 retest proposal (`flags.py`)
6. The `sr_detector_results` row: what is written and read
7. Is the observer non-gating? (the facts, with lines)
8. The end-of-day backfill script
9. Call sites in other topics' files (interface only)
10. Inherited items: P03's primary items, then its secondary items
11. Stated intent: docstrings, comments, tests, documents, history
12. Points for the AUDIT
13. UNKNOWN / NOT ESTABLISHED items
14. Questions about intent for Rama
15. Cross-references
