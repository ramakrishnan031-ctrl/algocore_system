# A07 evidence: the A07 source files at the study baseline

**Status:** APPROVED — evidence for the A07 STUDY, approved by Rama on 2026-11-25 with the A07 topic package (Decision Register, D-40)
**Date:** 2026-11-20
**Revision history:** First version, 2026-11-20. Approved by Rama on 2026-11-25 with the A07 topic package (Decision Register, D-40): status marked APPROVED; content unchanged.
**Purpose and scope:** Identifies the A07 paths of the Master System Investigation Index (entry A07; Appendix A for the three scripts) at the study baseline: size, Git object, SHA-256 and history of each path; the A07 call sites in files that other topics own (`main.py`, A01's file, index rule 8; `signals/signal_processor.py`, A06's file; and others); the declared invocations of the scripts, as declarations only; the related paths that other topics own, which A07 reads at the boundary only (the start line of Decision Register D-38 and Rama's decisions P1 to P3 of 20-Nov-2026, D-39); the tests that reference A07 code (A19's; evidence of stated expectations only); and the A07 changes made after the last recorded deployment (D-21). It supports the STUDY's inventory and decides nothing.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 20-Nov-2026 from the local read-only clone with `git show`, `git ls-tree`, `git log`, `git grep` and `git diff`. Nothing in the clone was written or run, and no endpoint, scanner, broker or API was contacted. Every repository-wide search excluded `config/accounts.csv`, `**/.env*`, `**/*.local.yaml` and `**/*token*.json`, and none of them was opened. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07); a commit message that carries an account identifier is paraphrased.

## 1. The files

The A07 paths are `strategies/control.py` and `strategies/taxonomy.py` (`strategies/schema.py` and `strategies/loader.py` are A02's); `screening/secondary_screener.py`, `screening/hard_gate.py`, `screening/quality_scorer.py`, `screening/entry_gate.py` and `screening/step_executor.py`; `core/strategy_direction.py`; `strategies/__init__.py` and `screening/__init__.py` (package initialisation and exports, provisional, see S1); the relevant `regime/` and `v3_chain/` integration call sites (section 2.3); and the three scripts that Appendix A assigns to A07. FACT: all thirteen files exist at the baseline, and the clone's working tree was clean and at the baseline. `strategies/` holds no other file than these and A02's two; `screening/` holds no other file than these and `screening/retest_monitor.py`, which is A08's (index, entry A08).

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `strategies/control.py` | 117 | 5552 | 100644 | `b6eecb480b83471149fb9362bafc980c967ff6c9` | `77350fdcda237588515ed2c2a98547e90ccbe8cd0272094b46449872a5179822` | 3 | 8116b74, 2026-07-10 |
| `strategies/taxonomy.py` | 38 | 1653 | 100644 | `069644bc1bdb464ffe5faec31f710acdc02e4837` | `e508691b930dccb0e5b3d135e9e3c2bcb523e0f633544807f4936cfb56973bb9` | 1 | 5a71fb6, 2026-07-13 |
| `strategies/__init__.py` | 6 | 245 | 100644 | `ee3a2879f0fa022d22fdd62d9aed206964b3e64b` | `ca405e8cf4448f9cf7cad329a50945c757e222ed01e1a4745d8d8551a39d307f` | 1 | bcf03b5, 2026-04-17 |
| `screening/secondary_screener.py` | 705 | 35461 | 100644 | `b6f8ff7223ad803869e976f92d794dfc7c811b59` | `6c030c0107a461a90283652b6fedb2c2235d21fcf075cfb75e6010587f9e387b` | 17 | 056905b, 2026-09-11 |
| `screening/hard_gate.py` | 466 | 23101 | 100644 | `a8e7e2e49675ca46989898174adf8e0afe419a61` | `eaf7f2b4130d57b186145c2871a510e88f0c82b099ece7d3800953821303dca5` | 4 | 132e571, 2026-08-01 |
| `screening/quality_scorer.py` | 150 | 6337 | 100644 | `b125e9ce324336fb8beba8012eee6669dbf91848` | `7581c5e8bff4d8492b030c419586472016d188b3f61c53c450ce033000ebcb1e` | 4 | 132e571, 2026-08-01 |
| `screening/entry_gate.py` | 537 | 21303 | 100644 | `46b173171bdfeba48af641b67a361618e5acba58` | `edb7d7dc8469d2c63fd39ac252ec219f3b19c8d0615193f8e4d00196984bca5e` | 10 | 132e571, 2026-08-01 |
| `screening/step_executor.py` | 423 | 17364 | 100644 | `d83b04860f0ff97b33ca60faa20230004d04ae5e` | `e5399ae42770bcad3438cf288c70fe4cb61391eaaeb3cf16e69d6bce48bb42da` | 12 | 8d753a0, 2026-07-25 |
| `screening/__init__.py` | 12 | 358 | 100644 | `f5069dd61fb8696394428c079f4dd162c8df9276` | `445beb9e5288cd5369bd292958b7186e7e251991ae6c5780439beb0393a8d7f1` | 1 | bcf03b5, 2026-04-17 |
| `core/strategy_direction.py` | 142 | 6954 | 100644 | `0e6f8b6686f393dcf38ddf036e565190cec0863a` | `43177d7338ec0bb38b6a9d6705bdc723627d96270b5ef0e4379ef07d71d7e53c` | 3 | 5094a32, 2026-08-10 |
| `scripts/compute_strategy_metrics.py` | 352 | 10423 | 100644 | `c081a0a8f76804301ada8d07733cf583f1c99287` | `36f4e8d4d0f43a03d8d6e928cdc48e791f2db787d1ce4773547c5e3b43de4fa1` | 4 | 75d5e99, 2026-06-18 |
| `scripts/strategy_registry_officer.py` | 305 | 13075 | 100644 | `c013518bc49c2323922292af5fa9eeacb3cc4d0b` | `f3f025e42fa61c6f73c67f3b2521cbbc480dac789d73c6300e1bcbb9274e4706` | 4 | 2846988, 2026-09-09 |
| `scripts/strategy_status.py` | 221 | 10643 | 100644 | `d15942ccde89d30e45df310a643ba0dacec17bce` | `22f155d8ec2261c7398463d089faadb4125582b24e9a34aeabaf63d0ac3d99c4` | 3 | 5a71fb6, 2026-07-13 |

Total: 2,596 lines in the ten modules and package files, and 878 lines in the three scripts.

FACT: `screening/__init__.py` re-exports `QualityScorer`, `ScoreResult`, `StepExecutor`, `StepExecutorResult`, `SecondaryScreener` and `ScreeningResult`; `strategies/__init__.py` re-exports A02's `StrategyConfig`, `validate_strategy` and `StrategyLoader`. No tracked file contains `from screening import` or `from strategies import`.

## 2. The A07 call sites in files that other topics own

FACT, at the baseline. The STUDY traces each one on A07's side; this section only locates them. The calling file stays its owner's (index rules 1 and 8).

### 2.1 `signals/signal_processor.py` (A06's file)

| Lines | What is there |
|---|---|
| L58 to L61 | import of `strategy_will_trade` and `CAUSE_TRADE_TYPE` from `strategies/control.py` |
| L959 to L971 | the strategy-control check in `_process_one`, before the screening call: a verdict that is not `will_trade` raises `_PipelineReject` with `TRADE_TYPE` (cause `CAUSE_TRADE_TYPE`) or `STRATEGY_CONTROL`; A07 covers the logic (D-38) |
| L977; L986 | the strategy's own entry window (A01) and the strategy governor (A09), between the strategy-control check and the screening call; interface only |
| L998 to L1004 | the screening call (the D-38 start line): `screen(signal_id, symbol, scanner_name, trigger_price, triggered_at, direction=strategy_obj.direction, intent=strategy_obj.intent, strategy=strategy_obj, market_data=None)` |
| L1006 to L1028 | `_record_screener_stats`; a `SKIPPED_` status returns (L1013); `passed` false returns (L1020); a pass leads to the heartbeat (L1023) and A09's price derivation (L1028) |
| L343 to L344 | `stop()` calls the screener's `shutdown()` |
| L2010 onwards; L2062 | `continue_from_gate`, the entry gate's resume entry point, and its strategy-control check (Rama's decision P2, D-39: interface only, except the strategy-control logic) |
| L2375 onwards; L2411 | `continue_from_retest`, the retest resume entry point, and its strategy-control check (interface only) |
| L1136 | `v3_chain.observe(...)` after screening and sizing (A18's; mapped by A06 at the interface) |

### 2.2 `main.py` (A01's file)

| Lines | What is there |
|---|---|
| L86 to L89 | imports of `EntryGate`, `WatchEntry`, `QualityScorer`, `SecondaryScreener` and `StepExecutor` |
| L865 to L893 | the gate-release pool (`max_workers=2`) and `_make_gate_release_cb`: a `PRICE_HIT` release is submitted to the pool, which calls `continue_from_gate`; other release reasons take no action |
| L3164 to L3188 | the boot summary: `strategy_will_trade` over every loaded strategy, logged as `strategy_control.summary`; wrapped, so a failure does not block start-up |
| L3230 to L3237 | `QualityScorer(weights=app_config.scoring, ...)` and `StepExecutor(..., market_open=...)` |
| L3238 to L3247 | `HardGate(...)`, built always ("Consumed by the screener only when scoring.v3_hardgate_mode != off") |
| L3281 to L3298 | `SecondaryScreener(...)`: the step executor, the scorer, the state store, the broker's `get_quote`, circuit-proximity switch, the MIS learned blocklist and its two switches, a product-resolver closure, the hard gate, the scoring configuration and the evidence recorder |
| L3586 to L3587 | the screener and the scorer passed to `SignalProcessor` |
| L3839 to L3844 | `EntryGate(quote_fn=broker_adapter.get_quote, ..., state_store=store, on_release=_make_gate_release_cb(signal_processor))` |
| L3975; L1748 | `entry_gate.start()`; `entry_gate.stop()` at shutdown |
| L3468 to L3700 | the regime and V3-chain wiring (A01's file; A18's modules) |

FACT and UNKNOWN / NOT ESTABLISHED (the entry gate, as worded at ChatGPT's checkpoint review of 20-Nov-2026): `EntryGate.add()` (`screening/entry_gate.py` L288) has no non-test caller at the baseline, so the normal live path that creates a new gate entry is not established. However, `EntryGate.start()` rehydrates any persisted `gate_state` rows (`rehydrate_from_gate_state`, L179) and can poll and release them through the callback path above. Whether such rows existed in the production database is UNKNOWN / NOT ESTABLISHED.

### 2.3 Other callers

| Caller (owner) | Lines | What |
|---|---|---|
| `core/config_auditor.py` (A02) | L268, L306 | `strategy_will_trade` in the A5 boot-gate probes (A02 V-06, V-23) |
| `scripts/cron_officer.py` (A16) | L461 to L484; L729 to L744 | `build_status_rows` and the renderers of `scripts/strategy_status.py`, in the cron briefing |
| `reports/daily_report.py` (A15) | L1518 | `build_taxonomy_map` |
| `orders/eod_squareoff.py` (A12) | L695 | `build_direction_map` |
| `v3_chain/runner.py`, `v3_chain/pb01_runner.py`, `v3_chain/pb01_entry.py` (A18) | L29; L33; L41 | imports of the V3 playbook gates in `screening/hard_gate.py` (Rama's decision P1, D-39: A07 studies the gate functions; A18 owns these calls) |
| `scripts/v3_hardgate_parity_recompute.py` (A18) | L34 | imports of `screening/hard_gate.py` functions |
| `config/expected_managers.yaml` (A02) | L65, L71, L77, L178, L383 | the declared manager classes `SecondaryScreener`, `QualityScorer`, `HardGate`, `EntryGate` and `StepExecutor` |

FACT: no A07 file imports `regime/` or `v3_chain/`. The integration points are the V3 playbook gates above; the screener's V3 modes on `scoring.v3_hardgate_mode` (`screening/secondary_screener.py` L202, "enforce"; L310, "shadow"; "off" by default), which use A07's own `HardGate`; the processor's `v3_chain.observe` (section 2.1); and the wiring in `main.py` (section 2.2).

## 3. Declared invocations of the scripts

FACT (declarations only; not evidence that any job ran; Document 06, section 4.2; index rule 12):

| Script | Declarations |
|---|---|
| `scripts/compute_strategy_metrics.py` | `config/cron_registry.yaml` L589 to L603 (`schedule: 16:15 Mon-Fri`, `cron_expression: 15 16 * * 1-5`, `market_day_only: true`, `monitored: true`, `enabled: true`); `deploy/cron/trading-system.cron` L120 to L121 (the line's machine path is not reproduced) |
| `scripts/strategy_registry_officer.py` | `config/cron_registry.yaml` L626 to L640 (`schedule: 16:22 Mon-Fri`, `cron_expression: 22 16 * * 1-5`, `market_day_only: true`, `monitored: true`, `enabled: true`), with the comment L618 to L625; `deploy/cron/trading-system.cron` L126 to L127 |
| `scripts/strategy_status.py` | no schedule of its own; imported by A16's `scripts/cron_officer.py` (section 2.3), whose own declarations Appendix A gives as cron 09:20 daily and 18:50 Mon-Fri |

## 4. Related paths that other topics own

These paths are read at the boundary only, for the A07 side of a flow; their owners investigate them (index rule 1; D-38; D-39). Owners are as the index states.

| Path | Bytes | Owner (index) | Why A07 reads it |
|---|---|---|---|
| `strategies/schema.py`, `strategies/loader.py` | 14263; 9811 | A02 | the strategy fields A07 reads, their validation and their loading |
| `config/strategies/` (16 strategy files), `config/scoring_weights.yaml`, `config/system_config.yaml` (`trade_type`, `force_intraday_only`, `delivery_enabled`, `entry_gate`, `mis_filter`), `config/strategy_direction_registry.yaml`, `config/expected_managers.yaml` | —; 2610; 55901; 5745; 22155 | A02 (`config/`) | the configured side of strategy control, screening, scoring, the entry gate and the direction registry |
| `core/config_auditor.py` | 45055 | A02 | a caller of `strategy_will_trade` (section 2.3) |
| `signals/signal_processor.py` | — | A06 | the strategy-control and screening call sites and the resume entry points (section 2.1; D-38; D-39) |
| `main.py`, `core/market_windows.py` | —; 13938 | A01 | the wiring (section 2.2); the strategy's own entry window |
| `core/state_store.py`, `core/schema.sql`, `core/db_connect.py` | — | A03 | the `signals`, `gate_state`, screener-result and `strategy_metrics` storage that A07's code writes and reads |
| `broker/zerodha_adapter.py`, `broker/product_resolver.py` | — | A04 | `get_quote` and the product resolution used by the screener and the entry gate |
| `core/candle_math.py`, `data/` | — | A05 | the market data behind the screener's step inputs |
| `screening/retest_monitor.py`, `sr_detector/` | 19889; — | A08 | the retest path and the S&R zones that callers pass to `gate_rr` |
| `capital/` (the governor, the sizer, the risk engine) | — | A09 | the decisions after the screening result and the capital use of the metrics script |
| `core/mis_blocklist.py`, `orders/eod_squareoff.py` | 6651; 85123 | A12 | the MIS learned blocklist read by the screener; the end-of-day reader of the direction map |
| `core/evidence_contract.py`, `core/effect_telemetry.py`, `reports/daily_report.py` | 35426; 12924; 84776 | A15 | the evidence recorder and the telemetry the A07 modules call; a reader of the taxonomy map |
| `config/cron_registry.yaml`, `deploy/cron/trading-system.cron`, `scripts/cron_officer.py`, `utils/cron_heartbeat.py` | 27116; 15842; 46613; — | A16 | the schedule declarations (section 3), the status-table caller and the heartbeat helper |
| `regime/`, `v3_chain/`, `scripts/v3_hardgate_parity_recompute.py` | — | A18 | the V3 chain that calls the playbook gates (D-39, P1) |
| `tests/` | — | A19 | evidence of stated expectations only (section 6) |
| legacy documents under `docs/` | — | evidence (HISTORICAL; index rule 11) | intent sources for the AUDIT |

## 5. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21).

FACT (`git diff 7d4970a 970aabf`): two of the thirteen A07 files changed after `7d4970a`; the other eleven are identical at both commits.

| Path | Lines added / removed (`7d4970a` to the baseline) | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `screening/secondary_screener.py` | 77 / 15 | `8d27fdb` (2026-09-10 19:07): "feat(evidence): CHECKPOINT -- wire P1, all five P2 reject paths, and P3"; `d646347` (20:48): "fix(evidence): CHECKPOINT -- every observer failure is counted, alerted once and PERSISTED"; `02d1e3f` (20:58): "fix(evidence): CHECKPOINT -- P3 no longer depends on the DB write succeeding"; `056905b` (2026-09-11 01:45): "fix(evidence): CHECKPOINT -- P2 identity is REQUIRED, measured first; completeness is what APPLIES" |
| `scripts/strategy_registry_officer.py` | 2 / 1 | `2846988` (2026-09-09 12:47): the alerts read the account tag from the account file instead of a hardcoded tag (paraphrased; the message carries an account identifier, not reproduced) |

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether either change was ever in force.

## 6. Tests that reference A07 code (A19; evidence of stated expectations only)

FACT: 36 tracked files under `tests/` match `git grep -l -E 'strategies\.control|strategies\.taxonomy|strategy_direction|screening\.|strategy_will_trade|compute_strategy_metrics|strategy_registry_officer|strategy_status|EntryGate|SecondaryScreener|StepExecutor|QualityScorer|HardGate|hard_gate' 970aabf -- tests` (with the four exclusions of the Source line). A test states an expectation under its own conditions; it is never evidence of production behaviour, and none was run.

`tests/crash_test/ct_day2_isolated.py`; `tests/integration/conftest.py`; `tests/integration/sim_kite.py`; `tests/integration/test_hardening_scenarios.py`; `tests/unit/test_e1_report_config_dir.py`; `tests/unit/test_entry_gate.py`; `tests/unit/test_eod_squareoff.py`; `tests/unit/test_evidence_contract.py`; `tests/unit/test_fix067_ms1_fresh_anchor.py`; `tests/unit/test_fix134_liquidity_check.py`; `tests/unit/test_fix134_strategy_metrics.py`; `tests/unit/test_fix136_batch9.py`; `tests/unit/test_fix140_price_movement_cancel.py`; `tests/unit/test_hard_gate.py`; `tests/unit/test_main.py`; `tests/unit/test_mis_blocklist.py`; `tests/unit/test_ms3_step_timeout_bounds_caller.py`; `tests/unit/test_nocil_prefill.py`; `tests/unit/test_p0_live_day1_fixes.py`; `tests/unit/test_pb01_registration.py`; `tests/unit/test_phase19_batch3.py`; `tests/unit/test_phase4_trade_type_gate.py`; `tests/unit/test_quality_scorer.py`; `tests/unit/test_registry_seed_state_split.py`; `tests/unit/test_secondary_screener.py`; `tests/unit/test_signal_processor.py`; `tests/unit/test_slice2_strategy_control.py`; `tests/unit/test_sr_v2_continue.py`; `tests/unit/test_sr_v2_divert.py`; `tests/unit/test_sr_v2_monitor.py`; `tests/unit/test_step_executor.py`; `tests/unit/test_strategies.py`; `tests/unit/test_strategy_registry_officer.py`; `tests/unit/test_v3_chain.py`; `tests/unit/test_v3_pb01_gates_score.py`; `tests/unit/test_v3_strategy_taxonomy.py`.
