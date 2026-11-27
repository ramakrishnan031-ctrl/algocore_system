# A08 evidence: the A08 source files at the study baseline

**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26. Revision 1, 2026-11-26: line references and omissions corrected from the checked A08 STUDY parts (part P06, section 8, statements P06-S122 to P06-S135, P06-S187 and P06-S188; parts P01 to P05 as cited there); every corrected cell names its source statement. No path, size, hash or count of section 1's table changed (P06-S136).
**Purpose and scope:** Identifies the A08 paths of the Master System Investigation Index (entry A08; Appendix A for the three scripts) at the study baseline: size, Git object, SHA-256 and history of each path; the A08 call sites in files that other topics own (`main.py`, A01's file, index rule 8; `signals/signal_processor.py`, A06's file; the `orders/` consumers; and others); the declared invocations of the scripts, as declarations only; the configuration block A08's code reads, by key name and committed value only; the related paths that other topics own, which A08 reads at the boundary only (Rama's decisions P1 to P5 of 26-Nov-2026, Decision Register D-41); the tests that reference A08 code (A19's; evidence of stated expectations only); and the A08 changes made after the last recorded deployment (D-21). It supports the STUDY's inventory and decides nothing.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 26-Nov-2026 from the local read-only clone with `git show`, `git ls-tree`, `git log`, `git rev-list`, `git grep` and `git diff`. Nothing in the clone was written or run, and no endpoint, scanner, broker or API was contacted. Every repository-wide search excluded `config/accounts.csv`, `**/.env*`, `**/*.local.yaml` and `**/*token*.json`, and none of them was opened. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. The files

The A08 paths are the twelve files of `sr_detector/`, `screening/retest_monitor.py` and three scripts, `scripts/sr_corp_action_spotcheck.py`, `scripts/sr_detector_backfill.py` and `scripts/sr_level_export.py` (index, entry A08 and Appendix A). `sr_detector/` holds exactly the twelve files listed (`git ls-tree 970aabf sr_detector/`).

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `sr_detector/__init__.py` | 70 | 2532 | 100644 | `0bafa58a43c3e50420090075909479f9089ba308` | `7b52decc4ca508dec0a95df425f245d6aa04e10bf62b11c0cf08d069b1cc5b43` | 2 | 536172c, 2026-07-12 |
| `sr_detector/models.py` | 207 | 8872 | 100644 | `4f49fac5386809539578085fc51dbdee5211da00` | `779501f83cbc70d2889ed40f607713d163a5245f2fe6111cc9f471a8facae56c` | 2 | 536172c, 2026-07-12 |
| `sr_detector/pivots.py` | 55 | 2133 | 100644 | `c1b4f0e4499792524357f76c12749d12ceaef625` | `6c7914ce9c76caf80a669ce60463962c0ea828b8b413da6d5513153fb48fe0f8` | 1 | dea336a, 2026-06-27 |
| `sr_detector/zones.py` | 116 | 3851 | 100644 | `dfcc7736d627fadab72578b981a6be7b805c44ad` | `a263f15b827574709525b2ab89de22d290e39d277b4378605ccdd6121a8ae5c6` | 1 | dea336a, 2026-06-27 |
| `sr_detector/confluence.py` | 211 | 7606 | 100644 | `8448e94be2545cab2410c77b44d80de570e0eab8` | `3a12141fc42775ff6e02421a9eaaad738039ccfcbb9b69884284feff0a5abbb6` | 1 | dea336a, 2026-06-27 |
| `sr_detector/flags.py` | 186 | 8028 | 100644 | `c5ca5b2514d8941a54090685489f13b0a66d5a39` | `69874f0260cdc96062201b2023e184cdd6dc2d4abdc1d508ded364b36cf3c3c4` | 2 | 55c93d3, 2026-06-27 |
| `sr_detector/zone_builder.py` | 224 | 8860 | 100644 | `976721417531869b88502577247f529474cb82ee` | `63618ffad59cdb30fd9df168806d1c21f13940ff56abb0f07a30769bf1e4a21b` | 2 | 536172c, 2026-07-12 |
| `sr_detector/fetch.py` | 159 | 6709 | 100644 | `38636d538667470cda48dde687f4531dcf349bd3` | `557fd70dd358a2c294a25bf6feed555dc13e3b5dbe15a9cd004289c1d2b52385` | 2 | 536172c, 2026-07-12 |
| `sr_detector/detector.py` | 329 | 14572 | 100644 | `a8500c48c8acb7878c9dcb1460caeb7f8eb9722c` | `a77e24a1043caa1e6ef7d0e38d2e25c1ae0de7f4aa1f1c135f0bfdf0fee196a3` | 4 | 132e571, 2026-08-01 |
| `sr_detector/zone_cache.py` | 76 | 2723 | 100644 | `06009c711f99b0601f46b198fdb67b6a913ae0a6` | `831186761909a4555a01740c445c549a39c8beb667b32f741ebfea7fd5f7ec53` | 1 | 9f56b07, 2026-06-27 |
| `sr_detector/zone_warmer.py` | 161 | 6545 | 100644 | `a47058e77cfc38eb569306bfaa5d578edaa3d64f` | `92aed14f3fde00c387abc492d11b90d2d1a4987021f1366aff1c0741eae7dc5a` | 1 | 9f56b07, 2026-06-27 |
| `sr_detector/retest_confirm.py` | 137 | 5459 | 100644 | `5fc212535bbd2e86f1c5899d07ce76331ab72724` | `fd402868833a5e535bb159eae17d04224ef58ca5c6ffc21eb9471305d85c613e` | 2 | 0235713, 2026-06-27 |
| `screening/retest_monitor.py` | 441 | 19889 | 100644 | `26639d6ed5dddb1140f0868bb9f937cad5379f82` | `02415698e111bde262e076c10da487f35f928877a398eeb5dfab46bc8824429c` | 3 | b3a5c94, 2026-07-14 |
| `scripts/sr_corp_action_spotcheck.py` | 102 | 3560 | 100644 | `05b06689a5c41a4e4948dbc16a58d86f175e5923` | `7d865d7c8f8f829f62f38a38efc1538dad778be099360b14c86619d84917a20b` | 1 | dea336a, 2026-06-27 |
| `scripts/sr_detector_backfill.py` | 149 | 4862 | 100644 | `9e6d9a45d2dc9b909c31a39e81d74561b683a6f9` | `c79bf0224f443e8c623e3b78dca3e13be30cba2683462fc7fb29c437bbbb2fc9` | 2 | 09ea725, 2026-07-17 |
| `scripts/sr_level_export.py` | 203 | 9263 | 100644 | `f4a2a3e3c6f5ff509ef49dcddbccb3c8e6b48097` | `f0b10ea928fb620148e1f552fde12d292972b16975e5bbf87a62acc5d9759fe8` | 1 | 536172c, 2026-07-12 |

Total: 2,372 lines in the thirteen modules and package files, and 454 lines in the three scripts (2,826 in all).

Top-level contents (FACT; `class` and `def` at column 0): `__init__.py`: `build_sr_detector` (L25); `models.py`: `Candle` (L24), `Pivot` (L51), `Zone` (L60), `ScoredZone` (L87), `Candidate` (L129), `RetestProposal` (L157), `SRAnalysis` (L190); `pivots.py`: `find_swing_pivots` (L24); `zones.py`: `cluster_zones` (L28), `_zone_from_cluster` (L65), `volume_profile_nodes` (L78); `confluence.py`: `ConfluenceContext` (L37), `ScoringParams` (L46), `score_zones` (L62) and helpers L80 to L195; `flags.py`: `BreakoutContext` (L28), `FlagParams` (L38), `FlagResult` (L46), `compute_flags_and_retest` (L55) and helpers L114 to L184; `zone_builder.py`: `ZoneKnobs` (L29), `build_zone_knobs` (L40), `build_scoring_params` (L52), `build_flag_params` (L69), `prior_day_levels` (L78), `scored_zones_from_candles` (L85), `split_zones` (L110), `round_number_levels` (L124), `intraday_anchors` (L143), `build_anchor_payload` (L185), `build_swings_payload` (L207); `fetch.py`: `OhlcFetcher` (L32); `detector.py`: `SRDetector` (L54); `zone_cache.py`: `ZoneSet` (L23), `ZoneCache` (L29); `zone_warmer.py`: `ZoneWarmer` (L30); `retest_confirm.py`: `_is_long` (L50), `RetestParams` (L55), `RetestResult` (L63), `evaluate` (L80), `_strong_close` (L130); `screening/retest_monitor.py`: `ParkedCandidate` (L27), `RetestMonitor` (L44), `RetestDiverter` (L264); the scripts: `sr_corp_action_spotcheck.py` `main` (L52); `sr_detector_backfill.py` `backfill` (L44), `main` (L96), `_cron_main` (L131); `sr_level_export.py` `flatten_analysis` (L62), `export_levels` (L104), `_make_real_analyze_fn` (L127), `main` (L178). Also at column 0 (Revision 1; P06-S188): `zone_builder.py` `_attr` (L24); `detector.py` `_attr` (L320), `_iso` (L324), `_json` (L328); `scripts/sr_corp_action_spotcheck.py` `_build_kite` (L33), `_token_for` (L45); `scripts/sr_detector_backfill.py` `_is_terminal` (L30), `_win_loss` (L34); `scripts/sr_level_export.py` `_row` (L46), `rows_to_csv` (L94).

## 2. The A08 call sites in files that other topics own

FACT, at the baseline. The STUDY records each one at the interface (call, contract passed, the flag that gates it, the handoff); the calling file stays its owner's (index rules 1 and 8; D-41, P3).

### 2.1 `signals/signal_processor.py` (A06's file)

| Lines | What is there |
|---|---|
| L186 to L188; L229 to L232 | constructor parameters and fields: `sr_detector` (the V1 observer), `zone_warmer`, `retest_sl_buffer_pct` (default 0.2), `_retest_diverter` |
| L356 to L359 | `set_retest_diverter`: late binding of the V2 diverter |
| L361 onwards; L388 | `_warm_zones`: enqueues a signal's symbol into the `ZoneWarmer`; called at L388 |
| L614 to L658 | `_sr_observe`: builds a `Candidate` (import L640) and calls `SRDetector.observe` (L655); called at L1550 (`_admit_and_place`), L2296 (`continue_from_gate`) and L2588 (`continue_from_retest`), each after the `PROCESSED` write (P06-S122; P01-S032; P03-S101) |
| L1042 to L1049; L1056 | `RetestDiverter.enabled` and `maybe_divert` on the FCFS path; the parked return at L1056 (P06-S126; P04-S117) |
| L2375 onwards | `continue_from_retest`, the retest resume entry point (`on_confirm` of the `RetestMonitor`); A08 records only the A08-specific handoff and values, its internal orchestration staying A06's (D-41, P1); its strategy-control check is at L2411 (A07's logic, recorded by A07) |

### 2.2 `main.py` (A01's file)

| Lines | What is there |
|---|---|
| L3421 to L3427 | `_sr_cfg = app_config.system.sr_detector`; `_v1_on` (`enabled`), `_v2_on` (`wait_for_retest_enabled`), `_struct_exit_on` (`structure_exit_enabled`) |
| L3480 to L3487 | the market-data client and the shared rate-limited fetch closure `_sr_fetch_fn`, built when any of six switches is on |
| L3490 to L3508 | `build_sr_detector(...)` and `sr_detector.start()` when `_v1_on`; a wiring failure is logged and the detector set to `None` |
| L3515 to L3523 | an `OhlcFetcher` for the regime engine (A18) |
| L3549 to L3572 | `ZoneCache`, `OhlcFetcher`, `build_zone_knobs`, `build_scoring_params` and `ZoneWarmer` when `_v2_on` or `_struct_exit_on` |
| L3575 to L3610 | `SignalProcessor(..., sr_detector=..., zone_warmer=..., retest_sl_buffer_pct=_sr_cfg.sl_buffer_pct, ...)` |
| L3673 to L3693 | an `OhlcFetcher` and the zone knobs reused by the V3 chain (A18) |
| L3712 to L3763 | the PB-01 block (A18): imports L3717 to L3718, the zone knobs L3723 to L3724, an `OhlcFetcher` L3728 to L3732, reused by the PB-01 watchlist (P06-S123; P02-X08) |
| L3765 to L3802 | `RetestParams`, `RetestMonitor(on_confirm=signal_processor.continue_from_retest, ...)`, `RetestDiverter`; `set_retest_diverter`; `eod.set_retest_monitor`; `rehydrate()`; `zone_warmer.start()`; `retest_monitor.start()` |
| L3804 to L3837 | `StructureExitManager` (A11) with the zone cache, when `_struct_exit_on`: the warmer start L3816, construction L3817 to L3831, `start()` L3832, `except` L3835 to L3837 (P06-S127) |
| L1599 onwards (L1697, L1733, L1739, L1744) | `_shutdown`: `sr_detector.stop()`, `retest_monitor.stop()`, `structure_exit_manager.stop()`, `zone_warmer.stop()` |
| L4266 to L4269 | `sr_detector` (L4266), `zone_warmer` and `retest_monitor` (L4267 to L4268) and `structure_exit_manager` (L4269) passed to `_shutdown` (P06-S128) |
| L393 to L438 | the closure's helpers `_build_market_data_kite` (L393 to L418) and `_make_sr_fetch_fn` (L421 to L438), used by the fetch of every A08 object (P06-S129) |
| L3428 to L3443 | the structure-exit guard before the S&R blocks (P06-S129) |
| L3524, L3563, L3683, L3733, L3778 | the five `register_constructed("ohlc_fetchers")` calls (P06-S129) |

### 2.3 Other callers

| Caller (owner) | Lines | What |
|---|---|---|
| `orders/structure_exit_manager.py` (A11) | L70; L102 to L130; L203 to L208; L256 to L277, L281 to L296 (`_strong_close` at L290, L293) | imports `retest_confirm._strong_close`; reads the `ZoneCache` and the zones' fields for the structure stop (P06-S135) |
| `orders/eod_squareoff.py` (A12) | L157 to L159; L191 to L193; L349 to L356 | `set_retest_monitor`; `RetestMonitor.clear_all()` at square-off |
| `orders/order_placer.py`, `orders/order_protocol_limit.py`, `orders/full_entry_engine.py`, `orders/order_protocol_co.py` (A10) | L888, L1345 to L1356; L183, L206 to L219; L85, L93 to L119; L103 | `entry_order_type` "MARKET" for the retest-confirm entry (`order_protocol_co.py` takes and ignores it) (P06-S130; P04-S121) |
| `regime/engine.py` (A18) | L50; L193 to L194; L108, L117 to L118, L321 to L323 | `find_swing_pivots` (import and call); the injected fetcher through `_fetch` (P06-S131) |
| `v3_chain/runner.py`, `v3_chain/pb01_runner.py`, `v3_chain/watchlist_capture.py` (A18) | L32 to L34; L37 to L39; L205 | `CONF_ANCHOR_ONLY`, `find_swing_pivots`, `scored_zones_from_candles`, `split_zones`; the runners and the capture also call the fetcher (`fetch_timeframes`) (P06-S131) |
| `v3_chain/pb01_entry.py` (A18) | L279 to L280, L289 to L291, L308 | the shared PB-01 `OhlcFetcher`, without importing A08 (P06-S131) |
| `v3_chain/truncate.py` (A18) | L54 to L68, L71 onwards (L92) | reads the `ts` of the fetched A08 `Candle` objects; called by the V3 runner, the PB-01 runner and the entry stage (P06-S187) |
| `core/candle_math.py` (A05), `core/daily_stats.py` (A15) | L42, L376; L24 | the `Candle` type (function-local imports in `core/candle_math.py`) |
| `scripts/forward_shadow_record.py` (A18; index, Appendix A) | L133 | the `Candle` type |
| `core/state_store.py` (A03) | L1979 to L2024; L3026 to L3072; L1408 to L1426 | the `sr_detector_results` methods (writes, the backfill reads and updates); the `retest_state` methods (`insert_retest_state` L3026, `update_retest_state` L3041); `update_signal_status` (P06-S133) |
| `core/schema.sql`, `core/migrations.py` (A03) | L1247 to L1300; L1303 to L1340; L81 to L83, L131 to L132 | the `sr_detector_results` table and indexes (schema v37) and the `retest_state` table and indexes (v38; rebuild entry L132) (P06-S133) |
| other readers of A08 code or of A08's stored output (owners as the index states) | — | `screening/hard_gate.py` `gate_htf` (A07); `reports/daily_trade_review.py`, `reports/signal_status.py`, `core/effect_telemetry.py` with `config/expected_managers.yaml`, `core/evidence_contract.py` and its manifest (A15); `scripts/eod_cleanup.py` (A12); `ops_dashboard/backend/readers/db_reader.py` and the `ops_dashboard` label maps; `core/config_auditor.py` (A02); `core/time_authority.py` as the clock (P06-S132; the STUDY's consumer table) |

## 3. Declared invocations of the scripts

FACT (declarations only; not evidence that any job ran; Document 06, section 4.2; index rule 12):

| Script | Declarations |
|---|---|
| `scripts/sr_detector_backfill.py` | `config/cron_registry.yaml` L408 to L423 (`schedule: 15:58 Mon-Fri`, `cron_expression: 58 15 * * 1-5`, `market_day_only: true`, `monitored: true`, `enabled: true`); `deploy/cron/trading-system.cron` L90 to L91 (the line's machine path is not reproduced) |
| `scripts/sr_corp_action_spotcheck.py` | no schedule; its docstring gives a manual command line (L18) |
| `scripts/sr_level_export.py` | no schedule; the comment on `intraday_anchors_enabled` (`config/system_config.yaml` L542) and `docs/SYSTEM_MAP.md` L233 describe it as a manual export for comparison |

## 4. The configuration A08's code reads

FACT: the `sr_detector:` block of `config/system_config.yaml` (A02's file), L508 to L545, loaded through `SRDetectorConfig` (`core/config_loader.py` L1153 onwards, A02's file). Committed values only; whether any was in force in production is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2). The switches are `enabled: true` (L509, the V1 observer), `wait_for_retest_enabled: false` (L529, the V2 retest path) and `intraday_anchors_enabled: false` (L542); `structure_exit_enabled: false` (L634) sits in the structure-exit block, read by `main.py` L3427, by `core/config_auditor.py` L224 (rule A4, run at `main.py` L3437 to L3439) and by `orders/structure_exit_manager.py` L127 to L129 (P06-S134). The other keys (timeframes, lookback and cache, pivot, clustering, merge, buffers, volume, the confluence weights and thresholds, the retest parameters, the zone cache and warmer, the poll interval, the structure-stop buffer, the anchor settings) are listed by the STUDY with their readers and defaults.

## 5. Related paths that other topics own

These paths are read at the boundary only, for the A08 side of a flow; their owners investigate them (index rule 1; D-41). Owners are as the index states.

| Path | Bytes | Owner (index) | Why A08 reads it |
|---|---|---|---|
| `config/system_config.yaml`, `core/config_loader.py` | 55901; 127242 | A02 | the `sr_detector` keys, their defaults and validation (section 4) |
| `core/state_store.py`, `core/schema.sql`, `core/migrations.py` | 153466; 104053; 21663 | A03 | the `sr_detector_results` and `retest_state` storage A08's code writes and reads |
| `main.py` | 208758 | A01 | the wiring, the shared fetch closure and the shutdown (section 2.2) |
| `core/candle_math.py`, `data/` | 21275; — | A05 | the candle functions and the historical-candle boundary (A05's handoffs) |
| `signals/signal_processor.py` | 139403 | A06 | the observer, warmer, divert and resume call sites (section 2.1; D-41, P1 and P3) |
| `screening/hard_gate.py` | — | A07 | the playbook gates that receive S&R inputs (A07, D-39, P1) |
| `capital/` | — | A09 | the entry, stop, target and sizing decisions reached after the retest resume |
| `orders/order_placer.py`, `orders/order_protocol_limit.py`, `orders/full_entry_engine.py` | 219497; 28685; 9338 | A10 | the MARKET entry for the retest confirmation |
| `orders/structure_exit_manager.py` | 30091 | A11 | the structure exit that reads A08's zones |
| `orders/eod_squareoff.py` | 85123 | A12 | the end-of-day clear of parked retest candidates |
| `config/cron_registry.yaml`, `deploy/cron/trading-system.cron` | 27116; 15842 | A16 | the schedule declarations (section 3) |
| `regime/`, `v3_chain/` | — | A18 | the reuse of A08 functions; the S&R shadow's activation and the PB-01 watchlist retest (D-41, P1 and P2) |
| `tests/` | — | A19 | evidence of stated expectations only (section 7) |
| legacy documents (`docs/`, `PATHS.md`, `README.md`) | — | evidence (HISTORICAL; index rule 11) | intent sources for the AUDIT |

## 6. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21).

FACT (`git diff --stat 7d4970a 970aabf` over the sixteen A08 paths): no A08 file changed after `7d4970a`; all sixteen are identical at both commits. UNKNOWN / NOT ESTABLISHED: which commit production actually ran (D-21).

## 7. Tests that reference A08 code (A19; evidence of stated expectations only)

FACT: 26 tracked files under `tests/` match `git grep -l -E 'sr_detector|retest_monitor|RetestMonitor|RetestDiverter|ZoneCache|ZoneWarmer|OhlcFetcher|sr_corp_action_spotcheck|sr_detector_backfill|sr_level_export' 970aabf -- tests`. A test states an expectation under its own conditions; it is never evidence of production behaviour, and none was run. Revision 1 (P06-S124): the search does not match `tests/unit/test_config_auditor.py`, which tests rule A4 on `structure_exit_enabled` (L87 to L132), or `tests/unit/test_sr_v2_market_path.py`, the SNR-V2 MARKET-route test, which names no A08 code (P04-X08); no file under `tests/` outside the 26 imports A08 code.

`tests/integration/test_hardening_scenarios.py`; `tests/unit/test_candle_math.py`; `tests/unit/test_config_loader.py`; `tests/unit/test_daily_stats.py`; `tests/unit/test_evidence_contract.py`; `tests/unit/test_f3_cron_drift_markers.py`; `tests/unit/test_market_regime.py`; `tests/unit/test_output_retention.py`; `tests/unit/test_signal_processor.py`; `tests/unit/test_sr_anchors.py`; `tests/unit/test_sr_detector_backfill.py`; `tests/unit/test_sr_detector_fetch.py`; `tests/unit/test_sr_detector_observer.py`; `tests/unit/test_sr_detector_units.py`; `tests/unit/test_sr_level_export.py`; `tests/unit/test_sr_v2_continue.py`; `tests/unit/test_sr_v2_divert.py`; `tests/unit/test_sr_v2_monitor.py`; `tests/unit/test_sr_v2_retest_confirm.py`; `tests/unit/test_sr_v2_zone_cache.py`; `tests/unit/test_structure_exit_manager.py`; `tests/unit/test_v3_chain.py`; `tests/unit/test_v3_pb01_e2e.py`; `tests/unit/test_v3_pb01_entry.py`; `tests/unit/test_v3_pb01_runner.py`; `tests/unit/test_v3_watchlist_capture.py`.
