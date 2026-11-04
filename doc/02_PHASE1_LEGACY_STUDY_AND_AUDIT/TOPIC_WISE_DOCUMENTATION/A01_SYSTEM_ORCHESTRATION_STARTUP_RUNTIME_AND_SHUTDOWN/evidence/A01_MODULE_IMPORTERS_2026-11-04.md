# A01 evidence: who imports the A01 modules, and who names the A01 scripts

**Status:** DRAFT — evidence for the A01 STUDY, for ChatGPT's review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04.
**Purpose and scope:** The static importers of the ten A01 Python modules other than `main.py`, and the files that name the two A01 scripts, at the study baseline. It supports the STUDY, sections 3, 10 and 11 (Q31 to Q33 of ChatGPT's A01 direction). An import shows that a file can use a module; it does not show that the code ran (Document 06, section 4.2).
**Source:** trading-system-prod-snapshot at commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, searched on 04-Nov-2026 in the local read-only clone with `git grep -nE` over `*.py` for the three import forms `from <package>.<module> import`, `import <package>.<module>` and `from <package> import ... <module>`, at any indentation (so imports inside functions are included). Not covered: imports built at run time (for example with `importlib`) and uses through another module's re-export. Nothing was run.

## 1. Importers of the A01 Python modules

Production files are listed with the line of each import statement; files under `tests/` (owned by A19) are counted only. `core/__init__.py` and `utils/__init__.py` hold one line each and import nothing (STUDY, section 10).

### 1.1 `core/events.py`

17 production import statements in 16 files; in `tests/`, 80 import statements in 71 files.

- `broker/order_monitor.py`: L48
- `broker/zerodha_adapter.py`: L123
- `capital/drift_handler.py`: L58
- `capital/fund_manager.py`: L87
- `capital/kill_switch.py`: L104
- `core/instrument_cache.py`: L47, L206
- `main.py`: L62
- `orders/cnc_gtt_monitor.py`: L46
- `orders/eod_squareoff.py`: L57
- `orders/order_manager.py`: L53
- `orders/order_placer.py`: L230
- `orders/order_reconciler.py`: L78
- `orders/shadow_tracker.py`: L53
- `orders/slippage_recorder.py`: L24
- `scripts/clear_kill_switch.py`: L34
- `scripts/system_manager.py`: L954

### 1.2 `core/ids.py`

13 production import statements in 11 files; in `tests/`, 19 import statements in 17 files.

- `broker/zerodha_adapter.py`: L132
- `orders/eod_squareoff.py`: L59
- `orders/mis_autosquareoff.py`: L200
- `orders/order_manager.py`: L54
- `orders/order_placer.py`: L232
- `orders/order_protocol_co.py`: L52
- `orders/order_protocol_limit.py`: L59
- `orders/order_reconciler.py`: L236, L2331, L3076
- `orders/sl_breach_monitor.py`: L30
- `orders/structure_exit_manager.py`: L58
- `signals/webhook_receiver.py`: L55

### 1.3 `core/exceptions.py`

30 production import statements in 30 files; in `tests/`, 79 import statements in 57 files.

- `broker/clock_skew_probe.py`: L49
- `broker/order_monitor.py`: L49
- `broker/order_state_machine.py`: L58
- `broker/product_resolver.py`: L30
- `broker/rate_limiter.py`: L36
- `broker/slippage_engine.py`: L47
- `broker/zerodha_adapter.py`: L124
- `capital/fund_manager.py`: L88
- `capital/invariant.py`: L47
- `capital/kill_switch.py`: L105
- `core/account_registry.py`: L40
- `core/config_loader.py`: L54
- `core/config_validator.py`: L50
- `core/cron_registry.py`: L33
- `core/events.py`: L54
- `core/instrument_cache.py`: L44
- `core/logger.py`: L49
- `core/state_store.py`: L62
- `core/time_authority.py`: L51
- `main.py`: L63
- `orders/cnc_gtt.py`: L26
- `orders/eod_squareoff.py`: L58
- `orders/order_placer.py`: L231
- `orders/order_protocol_co.py`: L51
- `orders/order_protocol_limit.py`: L58
- `orders/order_reconciler.py`: L83
- `signals/signal_processor.py`: L56
- `strategies/loader.py`: L19
- `strategies/schema.py`: L20
- `utils/startup_checks.py`: L51

### 1.4 `core/constants.py`

9 production import statements in 9 files; in `tests/`, 3 import statements in 3 files.

- `capital/fund_manager.py`: L160
- `capital/kill_switch.py`: L77
- `main.py`: L1131
- `orders/cnc_gtt_monitor.py`: L45
- `orders/eod_squareoff.py`: L52
- `orders/order_placer.py`: L430
- `orders/order_reconciler.py`: L101
- `orders/shadow_tracker.py`: L56
- `orders/sl_breach_monitor.py`: L29

### 1.5 `core/account_registry.py`

30 production import statements in 28 files; in `tests/`, 3 import statements in 3 files.

- `alerts/cron_alerts.py`: L29
- `core/evidence_contract.py`: L463
- `main.py`: L56, L1843
- `ops/control_tower/reporter.py`: L15
- `scripts/alert_watcher.py`: L70
- `scripts/auto_refresh_token.py`: L55
- `scripts/check_cron_drift.py`: L51
- `scripts/cron_officer.py`: L44
- `scripts/cron_report_render.py`: L23
- `scripts/cron_watchdog.py`: L29
- `scripts/eod_broker_reconcile.py`: L434
- `scripts/fetch_daily_candles.py`: L35
- `scripts/forward_shadow_record.py`: L34
- `scripts/gemini_data_integrity_check.py`: L42
- `scripts/gemini_log_review.py`: L38
- `scripts/liveness_probe.py`: L78
- `scripts/monitoring_canary.py`: L65
- `scripts/preflight/base.py`: L17
- `scripts/preflight/orchestrator.py`: L32
- `scripts/preflight/report.py`: L21
- `scripts/preflight/sentinel.py`: L21
- `scripts/reconcile_positions.py`: L100
- `scripts/reconstruct_excursions.py`: L59
- `scripts/refresh_instruments.py`: L318
- `scripts/strategy_registry_officer.py`: L44
- `scripts/system_manager.py`: L57, L161
- `scripts/zerodha_login.py`: L256
- `signals/webhook_receiver.py`: L57

### 1.6 `core/time_authority.py`

99 production import statements in 81 files; in `tests/`, 109 import statements in 94 files.

- `alerts/critical.py`: L41
- `alerts/telegram_notifier.py`: L48
- `broker/order_monitor.py`: L51
- `broker/token_monitor.py`: L35
- `broker/zerodha_adapter.py`: L134, L1347
- `capital/fund_manager.py`: L91
- `capital/kill_switch.py`: L111
- `capital/risk_engine.py`: L65
- `capital/shadow_engine.py`: L29
- `capital/strategy_governor.py`: L92, L106
- `core/events.py`: L55
- `core/evidence_contract.py`: L453
- `core/logger.py`: L50
- `core/market_windows.py`: L283, L309
- `core/mis_blocklist.py`: L31
- `core/state_store.py`: L2073, L3141
- `data/candle_store.py`: L21
- `data/live_feed.py`: L23
- `main.py`: L40, L531, L941, L992, L1355, L1663, L2226, L2749, L3107
- `ops/control_tower/cli.py`: L21
- `orders/cnc_gtt.py`: L27
- `orders/cnc_gtt_monitor.py`: L47
- `orders/eod_squareoff.py`: L63
- `orders/order_manager.py`: L56
- `orders/order_placer.py`: L236
- `orders/order_reconciler.py`: L87
- `orders/shadow_tracker.py`: L55
- `orders/sl_breach_monitor.py`: L31
- `orders/slippage_recorder.py`: L25
- `orders/smart_tgt_manager.py`: L59
- `orders/structure_exit_manager.py`: L671
- `orders/tgt_retry_manager.py`: L47
- `reports/daily_report.py`: L52
- `reports/daily_trade_review.py`: L2879
- `screening/entry_gate.py`: L44
- `screening/secondary_screener.py`: L20
- `screening/step_executor.py`: L17
- `scripts/alert_watcher.py`: L69
- `scripts/approve_ssh_keys.py`: L50
- `scripts/capture_metrics_baseline.py`: L47
- `scripts/check_cron_drift.py`: L44
- `scripts/compute_strategy_metrics.py`: L35
- `scripts/cron_officer.py`: L35
- `scripts/cron_watchdog.py`: L28
- `scripts/db_retention.py`: L50
- `scripts/disk_monitor.py`: L29
- `scripts/eod_broker_reconcile.py`: L57
- `scripts/eod_cleanup.py`: L32
- `scripts/eod_verify.py`: L51
- `scripts/fetch_daily_candles.py`: L34
- `scripts/fetch_fno_ban.py`: L65
- `scripts/forward_shadow_record.py`: L130
- `scripts/gemini_data_integrity_check.py`: L41
- `scripts/gemini_log_review.py`: L35
- `scripts/gemini_premarket_brief.py`: L37
- `scripts/gemini_trade_coach.py`: L38
- `scripts/gemini_watchman.py`: L43
- `scripts/gemini_weekly_patterns.py`: L35
- `scripts/healthcheck_server.py`: L71, L259
- `scripts/liveness_probe.py`: L70
- `scripts/load_test_signals.py`: L49
- `scripts/monitoring_canary.py`: L64
- `scripts/preflight/autofix.py`: L61
- `scripts/preflight/checks/security.py`: L29
- `scripts/preflight/orchestrator.py`: L44
- `scripts/preflight/startup_hook.py`: L37
- `scripts/premarket_healthcheck.py`: L40
- `scripts/reconcile_pnl.py`: L45
- `scripts/reconcile_positions.py`: L43
- `scripts/reconstruct_excursions.py`: L438
- `scripts/sr_detector_backfill.py`: L109
- `scripts/strategy_registry_officer.py`: L43
- `scripts/system_manager.py`: L55
- `scripts/t2_cnc_gtt_realtest.py`: L123, L134, L188, L217, L344
- `scripts/trade_journal.py`: L34
- `scripts/wal_checkpoint.py`: L22
- `scripts/zerodha_login.py`: L34
- `signals/signal_processor.py`: L57
- `signals/webhook_receiver.py`: L56
- `sr_detector/__init__.py`: L50
- `utils/cron_heartbeat.py`: L21, L192

### 1.7 `core/market_windows.py`

11 production import statements in 11 files; in `tests/`, 16 import statements in 12 files.

- `broker/token_monitor.py`: L34
- `main.py`: L66
- `orders/eod_squareoff.py`: L61
- `orders/order_reconciler.py`: L85
- `orders/tgt_retry_manager.py`: L41
- `scripts/fetch_daily_candles.py`: L234
- `scripts/gemini_watchman.py`: L42
- `scripts/premarket_healthcheck.py`: L42
- `scripts/reconcile_pnl.py`: L43
- `scripts/reconcile_positions.py`: L41
- `scripts/sr_level_export.py`: L133

### 1.8 `utils/startup_checks.py`

2 production import statements in 2 files; in `tests/`, 33 import statements in 11 files.

- `main.py`: L96
- `scripts/preflight_scanner_check.py`: L203

### 1.9 `utils/instance_lock.py`

2 production import statements in 2 files; in `tests/`, 6 import statements in 2 files.

- `main.py`: L95
- `scripts/reconstruct_excursions.py`: L364

### 1.10 `utils/holiday_guard.py`

18 production import statements in 15 files; in `tests/`, 9 import statements in 7 files.

- `core/cron_registry.py`: L182
- `main.py`: L94
- `reports/daily_report.py`: L54
- `reports/daily_trade_review.py`: L2858
- `scripts/cron_officer.py`: L110, L912
- `scripts/fetch_daily_candles.py`: L235
- `scripts/liveness_probe.py`: L132
- `scripts/preflight/checks/broker.py`: L90, L294
- `scripts/preflight/orchestrator.py`: L85
- `scripts/preflight/startup_hook.py`: L45
- `scripts/premarket_healthcheck.py`: L193
- `scripts/reconcile_pnl.py`: L320
- `scripts/reconcile_positions.py`: L361
- `scripts/system_manager.py`: L114, L667
- `utils/cron_heartbeat.py`: L195

## 2. Files that name the A01 scripts

Searched with `git grep -nE 'check_tz\.sh|ist_now\.sh'` over every tracked file at the baseline.

| Script | Named in code | Named in tests | Named in documents (HISTORICAL) |
|---|---|---|---|
| `scripts/check_tz.sh` | `scripts/deploy_preflight.py` L12, L60 to L68 (A17's operator script: a comment at L12 says it runs `check_tz.sh` "for VISIBILITY only"; its function `tz_self_check`, L60 to L68, builds the script's path and runs it with `bash` at L62 to L64) | `tests/unit/test_t4_deploy_preflight.py` L7, L108, L118 | `PATHS.md` L224; `docs/SYSTEM_MAP.md` L196, L494; `docs/audit/reconciler_product_filter_build_02aug2026.md` L235 |
| `scripts/ist_now.sh` | `scripts/check_tz.sh` L9, L26 to L27, L48 (it calls `ist_now.sh` at L26) | `tests/unit/test_t4_deploy_preflight.py` L6, L97 | `PATHS.md` L221; `docs/SYSTEM_MAP.md` L196, L494 |

No file under `config/` or `deploy/` names either script (the schedule and service declarations owned by A16 and A17). Neither naming shows that a script ran (index rule 12).
