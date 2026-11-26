# A08 STUDY — Part P02 brief (writer): candle fetch, zone building, zone cache and zone warmer

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P02-S001` onwards.
Output file: `/home/claude/a08/parts/A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/P02_WRITER_PROGRESS.md`.
Context parts (checked; cite by statement ID, do not edit): P01
`/home/claude/a08/parts/A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md` (the calculation core: cite it, do not
re-describe the algorithms) and P07 `/home/claude/a08/parts/A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md` (the inherited
items; section 7 is the assignment table).

## Scope (study in full, every function, every branch)

- `sr_detector/fetch.py` (159 lines): `OhlcFetcher` — constructor arguments; the fetch function it wraps (the shared
  rate-limited closure built in `main.py` L3480 to L3487: record at the interface what it is and what it passes; the
  closure's own logic and the broker client are A01/A04/A05); timeframes and intervals; lookback and date-window
  computation (dates, time zone, market hours, today's forming candle included or not); the cache: key composition,
  stored value, age/TTL rule and its clock (wall-clock vs market time; A05 handoff HA-06: cache key and wall-clock age),
  eviction, size, thread safety; row conversion (`Candle.from_kite` — cite P01) and whether rows are sorted,
  de-duplicated or validated (A05 handoff: unsorted fetched rows); empty results; exceptions caught/raised/logged;
  retries; rate-limit interaction.
- `sr_detector/zone_builder.py` (224 lines): every function (`ZoneKnobs`, `build_zone_knobs`, `build_scoring_params`,
  `build_flag_params`, `prior_day_levels`, `scored_zones_from_candles`, `split_zones`, `round_number_levels`,
  `intraday_anchors`, `build_anchor_payload`, `build_swings_payload`): which configuration attributes each reads and its
  fallbacks/defaults (compare with P01's dataclass defaults by citation), the order of calls into the calculation core,
  how prior-day levels and anchors are derived (which candles, which day boundary, time zone), above/below split rule
  and the reference price used, round-number generation, payload shapes.
- `sr_detector/zone_cache.py` (76 lines): `ZoneSet`, `ZoneCache` — key, stored fields, TTL and `now_fn`, staleness
  rule, locking, invalidation, what a reader gets on a miss or stale entry.
- `sr_detector/zone_warmer.py` (161 lines): `ZoneWarmer` — queue type and bound, enqueue (called from
  `signals/signal_processor.py` `_warm_zones` L361/L388 — interface only), worker thread(s), start/stop, the re-warm
  margin rule, what it fetches and computes, what it writes to the cache, error handling, whether enqueue can block the
  caller (A06 handoff: "whether the dispatcher's zone warming can block"), behaviour at shutdown and with the switches
  off.

For every function: inputs/outputs, branches, guards and their absence, time/clock use, threads and locks, side
effects, logging, exceptions.

## Readers and callers (interface only)

Who calls these objects (`main.py` wiring lines in A08 inventory section 2.2; `signal_processor` 2.1; the regime
engine and V3 chain/watchlist reuse of `OhlcFetcher` and the zone knobs — A18; `orders/structure_exit_manager.py`
reading `ZoneCache` — A11; `RetestDiverter` reading the cache — P04). Record the call and what is passed only.

## Inherited items

Answer A08's side of every item and open issue whose PRIMARY part is P02 in P07 section 7 (as finally checked),
including any of the 16 Owner-field records assigned to P02 (Rama's decision of 26-Nov-2026,
`/home/claude/a08/notes/RAMA_DECISIONS_A08_STUDY.md`), and record P02's side of the items where P02 is SECONDARY.
For each: the item ID, what the source asked, the A08 facts with lines, the label; never change the item's
classification, treatment or status. The A05 note that a KNOWN DEFECT was "considered and not given" for HA-06 at the
boundary: establish the A08-owned facts independently and record any evidence bearing on that assessment as a Point for
the AUDIT; do not classify.

## Intent sources

Docstrings and comments; tests as stated expectations (`tests/unit/test_sr_detector_fetch.py`,
`tests/unit/test_sr_v2_zone_cache.py`, `tests/unit/test_sr_anchors.py` and others found by git grep); configuration
comments in the `sr_detector:` block (`config/system_config.yaml` L508 to L545, committed values only); legacy
documents; git history (HISTORICAL).

## Sections (after section 1, Method)

2. The four files: identity and declared purpose
3. `OhlcFetcher`: windows, cache, conversion, ordering, errors
4. `zone_builder`: knobs, parameters, prior-day levels, anchors, split, payloads
5. `ZoneCache`
6. `ZoneWarmer`: queue, worker, re-warm, blocking, shutdown
7. Threads, locks, clocks and failure behaviour across the four files (summary)
8. Callers and readers (interface only)
9. Inherited items: P02's primary items, then its secondary items
10. Stated intent: docstrings, comments, tests, documents, history
11. Points for the AUDIT
12. UNKNOWN / NOT ESTABLISHED items
13. Questions about intent for Rama
14. Cross-references
