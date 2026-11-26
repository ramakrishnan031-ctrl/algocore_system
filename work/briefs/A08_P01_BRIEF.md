# A08 STUDY — Part P01 brief (writer): the calculation core

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P01-S001` onwards.
Output file: `/home/claude/a08/parts/A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_<YYYY-MM-DD>.md` (IST date of writing).
Progress log: `/home/claude/a08/status/P01_WRITER_PROGRESS.md`.

## Scope (study in full, every function, every branch)

- `sr_detector/models.py` (207 lines): `Candle` (fields, units, `from_kite` L34 and every conversion it makes: field
  names read, type casts, timestamp/timezone handling, defaults for missing keys, what happens on a missing or bad
  value), `Pivot`, `Zone` (`center`, `width`, `contains` with `buffer_pct` — units and boundary inclusivity),
  `ScoredZone` (fields, `center`, `contains`, `to_dict` keys), `Candidate` (fields, `is_long`), `RetestProposal`,
  `SRAnalysis`, the constant `CONF_ANCHOR_ONLY` and any other module constants.
- `sr_detector/pivots.py` (55 lines): `find_swing_pivots` — the algorithm (left/right window, strict or non-strict
  comparison, ties and plateaus, the first and last bars, what "high"/"low" uses), the input ordering it assumes
  (does it sort? does it rely on chronological order? what if rows are unsorted or duplicated?), the output.
- `sr_detector/zones.py` (116 lines): `cluster_zones` (sorting, tolerance and its unit — percent, absolute or ATR —,
  how members join a cluster, chaining effects, minimum touches), `_zone_from_cluster` (band low/high, touches, any
  time fields), `volume_profile_nodes` (binning, bin count/size, volume source, which nodes are returned, empty or
  zero-volume input).
- `sr_detector/confluence.py` (211 lines): `ConfluenceContext`, `ScoringParams` (every field and default),
  `score_zones` and every helper (`_merge_across_tfs`, `_score_group`, `_bucket`, `_level_in_band`,
  `_has_round_number`, `_recency_factor`): the scoring formula exactly (each term, weight, cap, threshold, bucket
  boundaries, round-number rule, recency decay and its time base/clock), merging across timeframes (overlap rule,
  which band survives), ordering of the output, ties, determinism.

For each function: signature, inputs (types, units), outputs, every branch, guards and their absence (empty lists,
zero/negative/NaN/inf prices, zero volume, division by zero, single candle), rounding, time/clock use (does anything
call `datetime.now`/`time.time`? which time zone?), side effects (none expected — confirm), logging, exceptions raised
or swallowed.

## Callers (interface only; cite lines)

Record who calls each public function at the baseline (`git grep ... 970aabf`, exclusions applied): inside
`sr_detector/` (zone_builder, detector, flags, retest_confirm — name the call sites; their logic belongs to parts
P02/P03/P04) and outside (`regime/engine.py` L50; `v3_chain/runner.py` L32-L34; `v3_chain/pb01_runner.py` L37-L39;
`v3_chain/watchlist_capture.py` L205; `core/candle_math.py` L42, L376; `core/daily_stats.py` L24;
`scripts/forward_shadow_record.py` L133 — A08 inventory, section 2.3). Record what each outside caller passes at the
call (arguments, timeframe) only; their logic is A18's/A05's/A15's.

## Intent sources (read; cite as stated intent; never run)

Module docstrings and comments in the four files; the relevant tests as stated expectations
(`tests/unit/test_sr_detector_units.py` and any other test that exercises these functions — find them with git grep);
the legacy documents that describe S&R detection (`docs/SYSTEM_MAP.md` and others found by `git grep -n -i -E
'pivot|confluence|cluster_zones|volume_profile' 970aabf -- docs '*.md'`, exclusions applied); git history of the four
files (`git log --format='%H %ad %s' --date=short 970aabf -- <file>`), cited as HISTORICAL.

## Sections to write (after section 1, Method)

2. The four files, their identity (A08 inventory, section 1) and declared purpose
3. The data model (`models.py`) and `Candle.from_kite`
4. Swing pivots (`pivots.py`)
5. Zone clustering and volume-profile nodes (`zones.py`)
6. Confluence scoring and merging across timeframes (`confluence.py`)
7. Input-order, data-quality and numeric edge cases across the four files (summary with cross-references)
8. Callers and the contracts passed (interface only)
9. Stated intent: docstrings, comments, tests, legacy documents, history
10. Points for the AUDIT
11. UNKNOWN / NOT ESTABLISHED items
12. Questions about intent for Rama
13. Cross-references to other parts and topics

Inherited items: part P07 catalogues all 48 inherited items and 16 open issues and assigns them; you do not need to
handle them. If you meet a fact that bears on A05's handoff about `Candle.from_kite` conversions or unsorted rows,
record it plainly in sections 3, 4 or 7 so P07 and the assembly can cite it.
