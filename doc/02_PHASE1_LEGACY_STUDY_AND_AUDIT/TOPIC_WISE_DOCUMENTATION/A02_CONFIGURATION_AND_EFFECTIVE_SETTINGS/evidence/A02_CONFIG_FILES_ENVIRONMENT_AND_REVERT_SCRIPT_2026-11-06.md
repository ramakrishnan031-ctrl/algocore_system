# A02 evidence: The configuration files, their readers and provenance, environment-variable names, and the TEMP-revert script

**Status:** DRAFT — evidence for the A02 STUDY, for ChatGPT's review
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06. Corrected, 2026-11-08: after the independent check of the A02 STUDY against the code (the rows named in that check).
**Purpose and scope:** This file records the 50 A02 configuration files under `config/` (identity, purpose, structure, provenance, readers, writers and behaviour on missing or malformed input), where sensitive material sits in them (location only), the files the code expects but the repository does not hold, the configuration sources outside `config/`, every environment-variable site in non-test Python with the `.env.example` key names, and a static trace of `scripts/revert_temp_config.py`. It supports the STUDY sections on the configuration file set and its provenance, environment variables and secrets handling, and the TEMP-revert script.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

## Conventions used in this file

Labels: **FACT**, **INTERPRETATION**, **HISTORICAL**, **UNKNOWN / NOT ESTABLISHED**, **OPEN QUESTION**. A value read from a file is "the file value at the baseline", never proof that it was in force. Sensitive values are never reproduced; where a key name itself embeds a broker account identifier it is written with `<ACCOUNT_ID>`.

Path-base shorthand used in the reader tables:

| Mark | Meaning |
|---|---|
| [D] | path built from a `config_dir` argument (follows `main.py --config` only when the caller passes it on) |
| [C] | literal relative path such as `"config/x.yaml"`, resolved against the process working directory |
| [R] | path built from the module's own location (`Path(__file__)…parent.parent / "config"`) |
| CL | the central loader `core/config_loader.py::load_all` |

---

## 1. File inventory

### 1.1 Scope and counts

FACT: `git ls-tree -r 970aabf config/` lists 51 tracked files; excluding `config/cron_registry.yaml` (A16) leaves **50 A02 files**: 30 YAML (14 top-level or registry files + 16 strategy files) and 20 CSV (2 account files, 17 index-member files, 1 security master).

FACT: History of the directory: the only file ever deleted under `config/` is `config/instruments.csv` (commit `2b4d976`, 2026-06-21, "fix(instruments): untrack config/instruments.csv (deploy-clobber recurrence fix)").

### 1.2 The central loader and its callers

FACT (`core/config_loader.py`): `_CONFIG_FILES` L2441-L2450 registers exactly 8 files: `system_config.yaml`, `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scoring_weights.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml`, and `f"nse_holidays_{_date.today().year}.yaml"` (L2449). `load_all(config_dir=Path("config"))` L2457: for each file, missing → `ConfigMissingError` (L2483-L2488); bytes hashed into `file_hashes` (L2490-L2491); YAML error → `ConfigSchemaError` (L2493-L2500); empty file → `{}` (L2502-L2504); pydantic failure → `ConfigSchemaError` (L2506-L2514). No partial result (docstring CL2, L14-L15). No env-var interpolation, no includes (CL5, L20). Strategy YAMLs are not loaded here (L25, L36).

INTERPRETATION: the holiday file name is evaluated once, at module import, from the host's local date (`date.today()`), not from IST.

Non-test callers of `load_all` (FACT; owner topic per the Master Index):

| Caller | Line | Path base | Handling of a load failure at the call site | Owner |
|---|---|---|---|---|
| `main.py::_main_locked` | L2198 | [D] (`--config` or `Path("config")`, L2099) | any exception → CRITICAL log, `return 5` (L2199-L2201) | A01 |
| `scripts/preflight/checks/config_integrity.py::AppConfigValidCheck` | L140 | [D] `ctx.config_dir` | check FAILED (CRITICAL) L141-L142 | A20 |
| `scripts/preflight/checks/config_sanity.py` | L33 | [D] | result cached as error string L46-L47 | A20 |
| `ops/control_tower/aggregator.py::read_config` | L145 | [D] | CRITICAL finding L146-L152 | A15 |
| `scripts/alert_watcher.py` | L795 / L797 | [D] or default [C] | prints error, `return 1` | A14 |
| `scripts/compute_strategy_metrics.py` | L303 | [D] `--config` default `"config"` | error log, `return 1` (L304-L306) | A07 |
| `scripts/cron_officer.py` | L781 | default [C] | any exception → sentinel directory falls back to `_ROOT / "data_store"` (L782-L783) | A16 |
| `scripts/deploy_preflight.py` | L42-L46 | default [C] | inside a command string sent to the VM | A17 |
| `scripts/eod_broker_reconcile.py` | L343 | default [C] | error log, `return 1` (L352-L354) | A12 |
| `scripts/eod_cleanup.py` | L61 | default [C] | falls back to `EodCleanupConfig` default (L63) | A12 |
| `scripts/fetch_fno_ban.py` | L318 | `Path("config")` [C] | any exception ignored (`pass`): the in-code default URL and fail-open are kept (L321-L322) | A05 |
| `scripts/forward_shadow_record.py` | L116 | [R] | inside the broker-connect `try`: warning, returns `None` (score and decision recorded only) (L123-L125) | A18 |
| `scripts/liveness_probe.py` | L294 | default [C] | any exception → sentinel directory falls back to `Path("data_store")` (L295-L296) | A15 |
| `scripts/monitoring_canary.py` | L314, L340 | default [C] | L314: error log, `return 1` (L315-L317); L340: functional status set to "UNKNOWN" (L346-L347) | A15 |
| `scripts/preflight_scanner_check.py` | L197 | [D] | error print, `return 1` (L198-L200) | A06 |
| `scripts/reconcile_pnl.py` | L329 | [D] `--config` default `"config"` | error log, `return 1` (L330-L332) | A12 |
| `scripts/reconcile_positions.py` | L369 | [D] `--config` default `"config"` | error log, `return 1` (L370-L372) | A12 |
| `scripts/sr_level_export.py` | L139 | [R], passed as `str` | — (no handler at the site) | A08 |
| `scripts/system_manager.py` | L1318 | [D] `--config-dir` | error log, print, `return 1` (L1319-L1322) | A15 |
| `scripts/t2_cnc_gtt_realtest.py` | L159 | `Path("config")` [C] | — (no handler at the site) | A19 |
| `scripts/v3_shadow_soak_report.py` | L45, L108, L189, L317 | [R] | — (no handler at the sites) | A18 |

Strategy files have their own loader, `strategies/loader.py::StrategyLoader.load_all_strategies` L102 (A02), which raises `ConfigSchemaError` if the directory holds no `*.yaml` (L128-L132) and on the first invalid file (L134-L135, `validate_strategy` in `strategies/schema.py`). Non-test callers: `main.py` L3157-L3162 [D]; `utils/startup_checks.py::check_strategy_configs` L1284 [D] (A01); `scripts/preflight/checks/config_integrity.py` L155, L173 [D] (A20); `scripts/preflight/checks/config_sanity.py` L37 [D] (A20); `ops/control_tower/aggregator.py` L156 [D] (A15); `scripts/replay_signals.py` L188 [D] (A19).

A second entry point in the same module, the function `strategies/loader.py::scan_strategy_errors` L70-L88 (A02), does not call `load_all_strategies`: it runs `validate_strategy` on every `*.yaml`, collects each failure as a `(filename, reason)` pair and never raises. Its only non-test caller is `main.py` L2496 [D], on the boot's abort path, when `invalid_strategy_configs` is among the blocking failures (L2494), to build an alert (L2497-L2498; an error in the scan or the alert is logged as non-fatal, L2499-L2500).

### 1.3 Identity, purpose, structure and provenance (50 rows)

"Purpose" quotes the file's own header (shortened); CSV files carry no header comments, so the purpose given is that of the reading module (marked). Lines and commit counts from `git show` and `git log` at the baseline; "Added" from `git log --diff-filter=A`.

| # | Path | Fmt | Purpose (own header) | Top-level structure | Lines | Added | Commits / last change |
|---|---|---|---|---|---|---|---|
| 1 | `config/accounts.csv` | CSV | none in file; reader `core/account_registry.py` L4-L6: "In-memory registry of trading accounts loaded from config/accounts.csv" | columns `account_id, broker, label, is_primary, api_key_env, api_secret_env, totp_secret_env, paper_capital, capital_share_pct, enabled`; 5 data rows (values not reproduced) | 6 | bcf03b5 2026-04-17 | 6 / 13eb727 2026-06-12 |
| 2 | `config/accounts_multi_example.csv` | CSV | none in file; `docs/SYSTEM_MAP.md` L463: "Template/example (NOT loaded)" (HISTORICAL) | same 10 columns; 3 data rows | 4 | 38fa4e9 2026-05-31 | 1 / 38fa4e9 |
| 3 | `config/broker_costs.yaml` | YAML | "Brokerage rates applied identically in live and paper modes … applied by broker/cost_calculator.py" (L3-L4); `_pct` fields are percentages (L9-L10) | `zerodha` (12 keys incl. `futures`, `options_buy`, `options_sell`) | 35 | bcf03b5 | 2 / 5dc8563 2026-05-14 |
| 4 | `config/broker_limits.yaml` | YAML | "Client-side token bucket limits per Zerodha API endpoint category (G7). broker/rate_limiter.py enforces these" (L3-L4) | `order`, `quote`, `historical`, `margins`, `backoff_sequence_sec` (list 3), `timeouts`, `rate_limit_backoff` | 40 | bcf03b5 | 3 / 316b335 2026-04-19 |
| 5 | `config/chartink_scanners.yaml` | YAML | "Canonical Chartink scanner URLs used by the pre-flight health check (P17)" (L3); "URLs are placeholders. Replace with actual Chartink screener URLs" (L12-L13) | `scanners` (16 name → URL) | 32 | bcf03b5 | 2 / 5a71fb6 2026-07-13 |
| 6 | `config/expected_managers.yaml` | YAML | "EXPECTED-MANAGER / EXPECTED-STATE REGISTRY — the single source of truth"; "Frozen 01-Aug-2026"; "NOT part of the system_config.yaml schema. Consumer: core/effect_telemetry (Phase B — NOT YET BUILT…)" (L2-L4, L22-L23) | `version`, `frozen_at`, `frozen_against`, `managers` (list 70) | 386 | a5c3704 2026-08-01 | 3 / 0197923 2026-08-04 |
| 7 | `config/index_universe.yaml` | YAML | "index instruments ingested for the regime-ranking feature … DATA ONLY"; resolved by `scripts/fetch_daily_candles.py` (L2-L6) | `indices` (list 10) | 28 | 4e2df39 2026-07-17 | 1 / 4e2df39 |
| 8 | `config/nse_holidays_2026.yaml` | YAML | "NSE Trading Holidays 2026 … Capital Market Segment" with the NSE circular named as source (L1-L3) | `holidays` (list 15 of `date`, `name`) | 47 | bcf03b5 | 1 / bcf03b5 |
| 9 | `config/preflight.yaml` | YAML | "thresholds owned by the PRE-FLIGHT process. NOT loaded by AppConfig"; "A missing or unreadable file DEGRADES to the in-code default" (L1-L13) | `startup_floors` (1 key) | 38 | e45f6b2 2026-08-10 | 1 / e45f6b2 |
| 10 | `config/reference_data/index_members/fno_symbols.csv` | CSV | none; reader `scripts/refresh_instruments.py` L15 "is_fno from fno_symbols.csv" | column `symbol`; 206 rows | 207 | bcf03b5 | 1 / bcf03b5 |
| 11 | `…/index_members/nifty100.csv` | CSV | none | `symbol`; 100 rows | 101 | bcf03b5 | 1 / bcf03b5 |
| 12 | `…/index_members/nifty50.csv` | CSV | none | `symbol`; 50 rows | 51 | bcf03b5 | 1 / bcf03b5 |
| 13 | `…/index_members/nifty_auto.csv` | CSV | none; sector file (refresh_instruments L70-L84) | `symbol`; 15 rows | 16 | bcf03b5 | 1 / bcf03b5 |
| 14 | `…/index_members/nifty_bank.csv` | CSV | none; sector file | `symbol`; 14 rows | 15 | bcf03b5 | 1 / bcf03b5 |
| 15 | `…/index_members/nifty_fin_services.csv` | CSV | none; sector file | `symbol`; 20 rows | 21 | bcf03b5 | 1 / bcf03b5 |
| 16 | `…/index_members/nifty_fmcg.csv` | CSV | none; sector file | `symbol`; 15 rows | 16 | bcf03b5 | 1 / bcf03b5 |
| 17 | `…/index_members/nifty_healthcare.csv` | CSV | none; sector file | `symbol`; 20 rows | 21 | bcf03b5 | 1 / bcf03b5 |
| 18 | `…/index_members/nifty_it.csv` | CSV | none; sector file | `symbol`; 10 rows | 11 | bcf03b5 | 1 / bcf03b5 |
| 19 | `…/index_members/nifty_metal.csv` | CSV | none; sector file | `symbol`; 15 rows | 16 | bcf03b5 | 1 / bcf03b5 |
| 20 | `…/index_members/nifty_midcap_select.csv` | CSV | none | `symbol`; 25 rows | 26 | bcf03b5 | 1 / bcf03b5 |
| 21 | `…/index_members/nifty_next50.csv` | CSV | none | `symbol`; 50 rows | 51 | bcf03b5 | 1 / bcf03b5 |
| 22 | `…/index_members/nifty_oil_gas.csv` | CSV | none; sector file | `symbol`; 15 rows | 16 | bcf03b5 | 1 / bcf03b5 |
| 23 | `…/index_members/nifty_pharma.csv` | CSV | none; sector file | `symbol`; 20 rows | 21 | bcf03b5 | 1 / bcf03b5 |
| 24 | `…/index_members/nifty_private_bank.csv` | CSV | none; sector file | `symbol`; 10 rows | 11 | bcf03b5 | 1 / bcf03b5 |
| 25 | `…/index_members/nifty_psu_bank.csv` | CSV | none; sector file | `symbol`; 12 rows | 13 | bcf03b5 | 1 / bcf03b5 |
| 26 | `…/index_members/nifty_realty.csv` | CSV | none; sector file | `symbol`; 10 rows | 11 | bcf03b5 | 1 / bcf03b5 |
| 27 | `config/reference_data/security_master_file.csv` | CSV | none; reader `scripts/refresh_instruments.py` L6, L13: "NSE security master CSV -- symbol universe" | columns `symbol, name_of_company, " series", fno_stock, " date_of_listing", " paid_up_value", " market_lot", " isin_number", " face_value"` (six with a leading space); 2801 rows | 2802 | bcf03b5 | 1 / bcf03b5 |
| 28 | `config/scan_webhook_map.yaml` | YAML | "Maps each Chartink scanner name to its target strategy configuration. Validated at startup (P17, S10)…" (L3-L6) | `scanners` (16 entries: `strategy`, `chartink_url`; `pb01_breakout_retest` also `scanner_type: eod`) | 84 | bcf03b5 | 2 / 5a71fb6 2026-07-13 |
| 29 | `config/scoring_weights.yaml` | YAML | "All secondary screener step weights and tier thresholds (P9b). NO weights are hardcoded in screening/*.py — this file is the single source" (L3-L4) | `steps` (10), `min_pass_score`, `high_score_threshold`, `medium_score_threshold`, `v3_hardgate_mode`, `v3_gate_steps` (list 2), `v3_freshness_max_sec`, `v3_min_pass_score`, `v3_high_score_threshold`, `v3_medium_score_threshold` | 44 | bcf03b5 | 10 / c1ad82e 2026-07-12 |
| 30 | `config/security.yaml` | YAML | "VM Security Manager (Phase 1). Read DIRECTLY by scripts/security_monitor.py … NOT by the trading app's config_loader"; "Alert-ONLY" (L1-L8); `copy_protection` read by `scripts/copy_gate.py` + `scripts/request_copy.py` (L137-L139) | `security` (18 keys), `copy_protection` (8 keys) | 155 | a701b0d 2026-06-19 | 10 / e6ade32 2026-07-26 |
| 31 | `config/slippage_model.yaml` | YAML | "Per-liquidity-tier slippage applied to paper mode fills and cost calculations (P12) … capital/cost_calculator.py reads this; symbol_validator.py assigns tiers" (L3-L5) | `tiers` (3), `default_tier` | 17 | bcf03b5 | 1 / bcf03b5 |
| 32-47 | `config/strategies/<name>.yaml` (16 files: `first_pullback_long`, `first_pullback_short`, `gap_fade_long`, `gap_fade_short`, `gap_go_long`, `gap_go_short`, `open_high_breakdown_short`, `open_low_breakout_long`, `pb01_breakout_retest`, `positional_momentum_long`, `positional_sector_rotation`, `positional_swing_long`, `range_breakout_long`, `range_breakout_short`, `vwap_bounce_long`, `vwap_rejection_short`) | YAML | each opens with its own path (L1); 15 of the 16 (all but `pb01_breakout_retest`) carry "Locked decisions: S1-S15" at L2; `pb01_breakout_retest.yaml` has no such line, its L2-L21 read: "V3 PLAYBOOK PB-01 … REGISTRATION STUB — SHADOW / NON-TRADING" | flat mapping, 35 keys (`name` … `active_days`); 36 in the four `gap_*` files (`sl_gap_buffer_pct`) and in `pb01_breakout_retest` (`v3_playbook`). FACT: `name` equals the file stem in all 16; 15 have `enabled: true`; `intent` INTRADAY 13 / DELIVERY 3 | 54-79 | 15 at bcf03b5; pb01 at 5a71fb6 2026-07-13 | 10-15 each (pb01: 1); all last 5a71fb6 2026-07-13 |
| 48 | `config/strategy_direction_registry.yaml` | YAML | "auto-maintained by scripts/strategy_registry_officer.py … This file is a REGISTRATION + HEALTH tracker that MIRRORS that field; it NEVER overrides it" (L2-L10); "Seeded 2026-07-17" (L23) | `strategies` (16 entries: `direction`, `registration_status`, `health`, `first_seen`, `evidence`) | 154 | 26885bb 2026-07-18 | 1 / 26885bb |
| 49 | `config/symbol_aliases.yaml` | YAML | "Symbol name aliases for Chartink -> Zerodha mapping … Format: chartink_name: zerodha_name" (L1-L7) | 2 top-level alias keys | 10 | 3975e75 2026-05-07 | 2 / 435b3a2 2026-05-07 |
| 50 | `config/system_config.yaml` | YAML | "Master configuration. Every numeric and boolean limit here has a corresponding runtime check, Telegram alert, and daily report row (P2). All time values are "HH:MM" strings interpreted as IST" (L3-L5); tagging convention `[LAUNCH-PHASE]` / `[PERMANENT]` (L10-L18) | **42 top-level keys** (list below) | 753 | bcf03b5 | 124 / 5f75c9b 2026-09-10 |

FACT cross-checks (scripted, on the baseline text): `chartink_scanners.yaml` and `scan_webhook_map.yaml` have the same 16 scanner names and identical URL values; in the map every scanner name equals its `strategy`; the 16 mapped strategies equal the 16 strategy files; the 16 registry keys equal the 16 strategy files, and every registry `direction` equals the strategy file's `direction`.

**`config/system_config.yaml` top-level keys (FACT, 42, in file order with line):** `broker` L21, `trading_hours` L27, `special_sessions` L117 (null; only commented example), `signal_queue` L124, `excluded_symbols` L131 (list 5), `force_intraday_only` L142 (scalar), `trade_type` L149 (scalar), `delivery_enabled` L155 (scalar), `product_map` L157, `mis_filter` L170, `clock` L183, `order_monitor` L192, `capital` L196, `position_sizing` L219, `risk` L261, `webhook` L327, `signal_processor` L344, `kill_switch` L355, `eod_squareoff` L359, `alerts` L379, `logging` L465, `order_reconciler` L468, `eod_reconcile` L477, `eod_cleanup` L481, `tgt_retry` L486, `shadow_tracker` L492, `sr_detector` L508, `regime` L547, `portfolio_allocator` L564, `v3_chain` L573, `watchlist` L619, `structure_exit` L633, `smart_tgt` L641, `entry_gate` L648, `slippage_bands` L712 (list 6), `paper` L720, `drift_handler` L726, `strategy_circuit_breaker` L732, `circuit_breaker` L738, `live_feed` L743, `fno_ban` L748, `scanner_check_delay_sec` L753 (scalar). FACT: `SystemConfig` (`core/config_loader.py`, class L1987-L2086; field annotations L1989-L2044) also has 42 fields, `v3_chain` at L2015. INTERPRETATION: a key count by a pattern restricted to `[a-z_]` gives 41, because it misses `v3_chain` (the name contains a digit).

### 1.4 Readers of each file, behaviour on missing/malformed input, writers

Only non-test code is listed as a reader. Test references are counted at the end of each row (owner A19): "Tests: N" is the number of files under `tests/` and `ops_dashboard/tests/` that contain the full file name (for example `broker_costs.yaml`). A count by the bare stem is higher, because the stem also matches attribute names such as `app_config.scan_webhook_map`. "Missing/malformed" is given only where visible at the read site.

| File | Readers (module::function, line, path base, owner) | Missing / malformed at the read site | Writer in the repository |
|---|---|---|---|
| `system_config.yaml` | CL (§1.2), every caller; `alerts/telegram_notifier.py::_read_telegram_enabled` L81-L102 [D, default "config"] (A14); `core/config_auditor.py::_safe_load_yaml` L850-L858 via `audit_app_config` L835 [D] (A02); `reports/daily_report.py::load_report_data` L145-L149 [D] (A15); `scripts/cron_officer.py::_strategy_status_payload` L471-L475 and `_tier_mode_line` L507 [D] (A16); `scripts/forward_shadow_record.py::_provenance` L84 (hash only) [R] (A18); `scripts/preflight/checks/config_integrity.py`: `ConfigFilesPresentCheck` L46-L50 (presence), `ConfigYamlValidCheck` L85-L93 (parse, glob of top-level `*.yaml`), `CapsConfigDriftCheck` L105-L111, `TierMultiplierModeCheck` L220-L224 [D] (A20); `scripts/premarket_healthcheck.py::check_config_files` L54-L72 (presence) (A20); `utils/startup_checks.py::check_config_files_present` L833-L871 (presence) and `check_temp_config_values` L1477-L1486 (text scan for `# TEMP`) [D] (A01); `scripts/security_monitor.py` watched-file hash (config `watched_files` L133; in-code fallback L222) [absolute path] (A17); `ops_dashboard/backend/readers/config_reader.py::get_system_config` L46-L53 (fallback after DB snapshot) [gui config `paths.config_dir`] (A15); `scripts/revert_temp_config.py` L119-L124 [R] (A02) | telegram: any error → `True` (fail-open) L101-L102; auditor: any error → `None`, group B skipped L857-L858; daily_report: `exists()` check, any exception swallowed, defaults kept (L140-L161); cron_officer: any exception → `None` (L483-L485) / "unknown" text (L512-L513); defaults applied when a key is absent: `trade_type` "INTRADAY", `force_intraday_only` True (L474-L475); preflight: missing → FAILED, parse error → FAILED (caps) or WARN (tier); startup_checks: missing → name returned; `OSError` → file skipped (L1486-L1487); ops_dashboard: missing → `{"_source": "unavailable"}`; a YAML error is not caught at L48-L49 | `scripts/revert_temp_config.py::apply_reverts` L169 (in place). Test tree: `tests/crash_test/revert_temp_configs.sh` L12, L16 (`sed -i`). Tests: 25 files |
| `broker_costs.yaml` | CL → `BrokerCostsConfig` (`core/config_loader.py` L2131); consumers `main.py` L2350 (`CostCalculator`, A04), `scripts/t2_cnc_gtt_realtest.py` L171; direct: `reports/daily_report.py` L155-L159 [D] (A15); `ops_dashboard/…/config_reader.py::get_broker_costs` L311-L340 (A15); presence lists (startup_checks L836, preflight L18, premarket L56) | CL as §1.2; daily_report: swallowed, `{}`; ops_dashboard: missing/parse error → `{}` | none found by grep. Tests: 10 |
| `broker_limits.yaml` | CL → `BrokerLimitsConfig` L2245; consumers `main.py` L385, L2348, L2404, L3073 (A01/A04); `scripts/sr_level_export.py` L144; `scripts/t2_cnc_gtt_realtest.py` L169; presence lists | CL | none found. Tests: 3 |
| `slippage_model.yaml` | CL → `SlippageConfig` L2269; the only consumer call site found: `main.py` L2512-L2516 (`SlippageEngine`, inside `if is_paper:` — **paper-only branch, not traced**); presence lists | CL (required in every mode) | none found. Tests: 2 |
| `scoring_weights.yaml` | CL → `ScoringConfig` L2295; consumers `main.py` L3231, L3245, L3296 (A07), `scripts/v3_shadow_soak_report.py` L46 (A18); direct: `core/config_auditor.py` L836 (A02); `reports/daily_report.py` L150-L154 (A15); `scripts/forward_shadow_record.py::_weights` L45-L54 and `_provenance` L83 [R] (A18); `scripts/v3_hardgate_parity_recompute.py::_load_weights` L198-L204 [R] (A18); `ops_dashboard/…/config_reader.py` `get_min_pass_score` L130-L139, `get_scoring_weights` L298-L309 (A15); presence lists | forward_shadow_record `_weights`: no handler at the read site (L52-L53); parity recompute: any error → in-code `_DEFAULT_WEIGHTS` (L203-L204); daily_report default 60 (L141, L154); ops_dashboard → `None` / `{}` | none in non-test code. Test tree: `tests/crash_test/revert_temp_configs.sh` L20. Tests: 10 |
| `scan_webhook_map.yaml` | CL → `ScanWebhookMapConfig` L2374; consumers `main.py` L2458, L3585; `signals/webhook_receiver.py` L552 (A06); `scripts/preflight_scanner_check.py` L209 (A06); `utils/startup_checks.py::check_scanner_connectivity` L652-L681 (A01); direct: `strategies/loader.py::_validate_scan_webhook_map` L170-L213 (A02; reached only when `scan_webhook_map_path` is passed, L152-L153 — no non-test caller passes it); `ops_dashboard/…/config_reader.py` `get_scan_webhook_map` L92-L115, `get_scanner_registry` L249-L278 (A15) | loader: missing → `ConfigMissingError`, YAML → `ConfigSchemaError`; ops_dashboard → `{}` / `[]` | none found. Tests: 6 |
| `chartink_scanners.yaml` | CL → `ChartinkScannersConfig` L2385; consumers `main.py` L2459 → `check_scanner_connectivity` fallback when a map entry has no URL (startup_checks L663-L664, L775); `scripts/preflight_scanner_check.py` L210 (A06); presence lists | CL | none found. Tests: 2 |
| `nse_holidays_2026.yaml` | CL (year at import, L2449) → `NseHolidaysConfig` → `main.py::_load_holidays` L441-L443; `utils/holiday_guard.py` `_load_holiday_set` L25-L66, `get_holiday_name` L114-L131 [D] (A01), called by `main.py` L2102-L2111, `core/cron_registry.py` L182-L185 (A16), `reports/daily_report.py` L110, `reports/daily_trade_review.py` L2859 (A15), `scripts/cron_officer.py` L113, L914, `scripts/liveness_probe.py` L133, `scripts/preflight/checks/broker.py` L96, L295, `scripts/preflight/orchestrator.py` L85, `scripts/preflight/startup_hook.py` L46, `scripts/system_manager.py` L124, L669, `utils/cron_heartbeat.py` L197, and `current_holiday_set` (L69-L82) callers `scripts/fetch_daily_candles.py` L238, `scripts/premarket_healthcheck.py` L194, `scripts/reconcile_pnl.py` L322, `scripts/reconcile_positions.py` L363; `utils/startup_checks.py::check_holiday_calendar` L1366-L1400 (A01); `scripts/security_monitor.py::check_nse_holiday_calendar` L957-L990 (existence, A17); presence lists (startup_checks L865, preflight L36, premarket L62) | holiday_guard: missing → `FileNotFoundError` (L45-L49), bad entry → `ValueError` (L62); `current_holiday_set`: any error → empty set (L79-L82); `main.py` L2151-L2152 catches `FileNotFoundError` and continues; startup check → WARNING only | none found (hand-maintained per `config/security.yaml` L66-L69 HISTORICAL comment). Tests: 6 (7 files contain `nse_holidays_2026`, 10 contain `nse_holidays_`) |
| `preflight.yaml` | `scripts/preflight/checks/broker.py::_min_broker_cash_rs` L44-L61 [D] (A20); top-level glob parse in `ConfigYamlValidCheck` | missing → in-code default 2000.0 (L41, L55-L56); any error → default (L60-L61) | none found. Tests: 1 |
| `security.yaml` | `scripts/security_monitor.py::SecConfig.load` L151-L182 [R default L70] (A17); `scripts/copy_gate.py::CopyConfig.load` L80-L99 [R default L55] (A17); `scripts/request_copy.py` L122, L127 via `CopyConfig` (A17); `scripts/approve_ssh_keys.py` L74, L79 via `SecConfig` (A17); `scripts/preflight/checks/security.py` `_load_security_yaml` L36-L41, `CopyProtectionStateCheck` L65-L83 [D] (A20); `scripts/system_manager.py::security_check` L823-L828 [D] (A15); top-level glob parse in `ConfigYamlValidCheck` | security_monitor / copy_gate: missing → warning + in-code defaults; other error → error log + defaults (L177-L180 / L94-L97); preflight: missing → FAILED (L73-L74), parse error → FAILED (L77-L78); system_manager: the read goes through `SecConfig.load` (L823), so a missing or malformed file gives the in-code defaults and no WARN; the WARN (L826-L828) is reached only if the import or the attribute access fails | none in code; HISTORICAL comment L93-L97 says the operator override is written to `data_store/` by `scripts/approve_ssh_keys.py`, not to this file. Tests: 5 |
| `expected_managers.yaml` | `core/effect_telemetry.py::_load_registry` L129-L143, default path [C] `Path("config")/…` L63 (A15); used by `assert_composition` L152 (read at L165; called `main.py` L4244) and `emit_census` L232 (called `main.py` L1665); top-level glob parse in `ConfigYamlValidCheck` | `assert_composition`: no handler at the read site (L138); `main.py` L4243-L4246 catches only `EffectCompositionError`. `emit_census` wraps the read in `try` (L231) | none found ("Frozen 01-Aug-2026", L4). Tests: 2 |
| `index_universe.yaml` | `scripts/fetch_daily_candles.py::_load_index_universe` L47-L63 [R, L40] (A05) | missing → `[]` (L53-L54); any error → warning print, `[]` (L61-L63) | none found. Tests: 0 |
| `strategy_direction_registry.yaml` | `core/strategy_direction.py::load_registry` L98-L121 (seed used only when the state file `data_store/strategy_direction_registry.yaml` is absent or unreadable: `_read_registry` returns `None` for a missing file and on any read or parse error, L87-L88, L94-L95, and `load_registry` then falls back to the seed, L114-L120) via `scripts/strategy_registry_officer.py` L231, L283 [D `--config-dir`] (A07); top-level glob parse | `_read_registry` returns `None` on missing/unreadable (L84-L95); no usable seed → `{}` | `core/strategy_direction.py::save_registry` L124-L135 writes the **state** path by default (L44, L282); the tracked seed is not written by default (comment L31-L42). The officer's `--registry` option (L270) can point anywhere (INTERPRETATION) |
| `symbol_aliases.yaml` | `signals/webhook_receiver.py::_load_symbol_aliases` L258-L292 [C `Path("config/symbol_aliases.yaml")` L265] (A06), called at construction L227; `main.py::_make_paper_quote_provider` L509-L518 [C] — **paper-only path, not traced**; `scripts/find_symbol_aliases.py` L84 only prints a hint to edit the file (A05) | webhook_receiver: missing → warning, `{}` (L266-L271); any error → error log, `{}` (L288-L292) | none; `scripts/find_symbol_aliases.py` prints candidates to stdout for manual addition (L83-L95). Tests: 0 |
| `accounts.csv` | `core/account_registry.py::AccountRegistry.load` L91-L211 (strict) and `_read_primary_row` L302-L318 ([R] default L308-L310; feeds `primary_account_tag`, `primary_api_key_env`, `primary_api_secret_env`, `primary_api_key` L296-L360) (A01). `AccountRegistry.load` callers: `main.py` L2359 (live pre-load), L2414 [D] (A01); `scripts/auto_refresh_token.py` L339 [R default L62] (A04); `scripts/zerodha_login.py` L258 [C] (A04); `scripts/refresh_instruments.py` L319 [R] (A05); `scripts/reconcile_positions.py` L103 [D] (A12); `scripts/eod_broker_reconcile.py` L435 [R] (A12); `scripts/system_manager.py` L162 [D] (A15). `primary_*` callers include `scripts/fetch_daily_candles.py` L44, `scripts/gemini_data_integrity_check.py` L49, `scripts/reconstruct_excursions.py` L69, `scripts/forward_shadow_record.py` L107, and `primary_account_tag()` callers across A06/A07/A14/A15/A16/A20 (for example `signals/webhook_receiver.py` L129, `scripts/strategy_registry_officer.py` L194, `scripts/preflight/orchestrator.py` L155, `scripts/preflight/report.py` L198, `core/evidence_contract.py` L464). Also `ops_dashboard/…/config_reader.py::load_accounts` L180-L193 (A15); `scripts/security_monitor.py` watched-file hash (config L134; fallback L223); presence list `utils/startup_checks.py` L842 | `load`: missing → `ConfigMissingError` (L104-L108), no header / missing columns / bad row / empty id / enabled row with `paper_capital <= 0` → `ConfigSchemaError` (L118-L170), unreadable → `ConfigMissingError` (L173-L177), zero or >1 primary → `ConfigSchemaError` (L180-L192), more than one enabled account with a `capital_share_pct` sum other than 1.0 → `ConfigSchemaError` (L196-L202); `_read_primary_row`: any failure → `{}` (L315-L318); main L2414: any exception → `return 3` (L2420-L2423); main L2359: only `FileNotFoundError`/`KeyError` handled (L2364, L2371); eod_broker_reconcile / system_manager: any error → `None` / fallback; ops_dashboard → `[]` | none found. Tests: 9 |
| `accounts_multi_example.csv` | **no non-test reader found by grep**; read only by `tests/unit/test_fix133_multi_account.py` L77-L85 | — | none found |
| `index_members/fno_symbols.csv` | `scripts/refresh_instruments.py::_load_fno_set` L133-L147 [R default `--index-dir` L53, L368] (A05) | missing → empty set (L136-L137) | none found |
| 12 sector files (`nifty_bank`, `nifty_fin_services`, `nifty_auto`, `nifty_fmcg`, `nifty_healthcare`, `nifty_it`, `nifty_metal`, `nifty_oil_gas`, `nifty_pharma`, `nifty_realty`, `nifty_private_bank`, `nifty_psu_bank`) | `scripts/refresh_instruments.py::_load_sector_map` L112-L130, file list `_SECTOR_INDEX_PRIORITY` L72-L85 (A05) | a missing file is skipped silently (L122-L123) | none found |
| `nifty50.csv`, `nifty100.csv`, `nifty_next50.csv`, `nifty_midcap_select.csv` | **no reader found by grep** (code or tests; the string "nifty50" in `ops_dashboard/tests/test_screen04_signals.py` L37, L139 is a scanner name in test data, not this file) | — | none found |
| `security_master_file.csv` | `scripts/refresh_instruments.py::_load_security_master` L92-L109 [R default L52, `--security-master` L364] (A05) | missing → error print, `sys.exit(1)` (L94-L96) | none found (INTERPRETATION: an NSE download placed by hand; docstring L6) |
| `strategies/*.yaml` (16) | strategy loader and callers (§1.2); direct, each validating independently: `core/strategy_direction.py::build_direction_map` L52-L71 (A07; e.g. `orders/eod_squareoff.py` L696 passes literal `"config"` [C]); `strategies/taxonomy.py::build_taxonomy_map` L23-L38 (A07); `scripts/strategy_status.py::build_status_rows` L56-L74 (A07; via `scripts/cron_officer.py` L476); raw YAML: `reports/daily_report.py::_build_strategy_min_scores` L313-L334 (A15); `scripts/system_manager.py::_enabled_strategy_names` L503-L520 (A15); `ops_dashboard/…/config_reader.py::get_strategies` L56-L89 (A15); `utils/startup_checks.py::check_temp_config_values` L1477 (text); `scripts/revert_temp_config.py` L91-L99 (`gap_fade_long.yaml` only) | loader: no files or any invalid file → `ConfigSchemaError`; `startup_checks.check_strategy_configs` L1276-L1280: missing dir → CRITICAL error string; direction/taxonomy maps: invalid file skipped; strategy_status: invalid file → "config error" row; daily_report / system_manager / ops_dashboard: unreadable file skipped | `scripts/revert_temp_config.py` L169 (`gap_fade_long.yaml`). Test tree: `tests/crash_test/scenarios/ct133.yaml` L27 appends invalid YAML to `gap_fade_short.yaml` |

FACT: `scripts/preflight/checks/config_integrity.py::ConfigYamlValidCheck` L83-L93 parses every top-level `config/*.yaml` (so also `cron_registry.yaml`, `security.yaml`, `preflight.yaml`, `expected_managers.yaml`, `index_universe.yaml`, `strategy_direction_registry.yaml`, `symbol_aliases.yaml`), but not `config/strategies/` or any CSV.

FACT: `deploy/security/trading-security.rules` L19 declares an auditd write watch on the production `config/` directory (A17; a declaration, not proof it was loaded).

---

## 2. Sensitive material (location only; value not reproduced)

| File | Location | Kind |
|---|---|---|
| `config/accounts.csv` | column `account_id` (5 rows) | broker account identifiers — value not reproduced |
| `config/accounts.csv` | column `label` | per `ops_dashboard/…/config_reader.py` L201 "label (= client name)": personal names — value not reproduced |
| `config/accounts.csv` | columns `api_key_env`, `api_secret_env`, `totp_secret_env` | environment-variable NAMES, not secret values; each name embeds the account identifier (pattern `ZERODHA_API_KEY_<ACCOUNT_ID>`, `ZERODHA_API_SECRET_<ACCOUNT_ID>`, `ZERODHA_TOTP_<ACCOUNT_ID>`) — value not reproduced |
| `config/accounts.csv` | columns `paper_capital`, `capital_share_pct` | money amounts / shares (not credentials) |
| `config/accounts_multi_example.csv` | same columns, 3 rows | identifiers and names (FACT: none of the 3 identifiers equals an `accounts.csv` identifier; whether they are real is NOT ESTABLISHED); env-name columns follow the same pattern (one with an `ANGELONE_` prefix and an empty TOTP name) — values not reproduced |
| `.env.example` | 15 key names L17-L39 | key names embed five broker account identifiers (masked here); values are placeholder-shaped strings (FACT: 17 of 20 values are one identical alphabetic placeholder) — values not reproduced |
| `.env.example` | comment headers L16, L21, L26, L31, L36 | each names an account identifier and an account-holder's personal name — not reproduced |
| `config/security.yaml` | `security.expected_key_fingerprint` L117 | SSH public-key fingerprint — value not reproduced |
| `config/security.yaml` | comments L98, L102, L106, L107 | partial SSH key fingerprints and key comment labels — not reproduced |
| `config/security.yaml` | comment L99 | an IP address with ISP/region, and a key comment label — not reproduced |
| `config/security.yaml` | `watched_files[].path` L126, L132-L134; `copy_protection.token_path` L153, `copy_protection.audit_log_path` L154 | absolute home-directory paths (L132 is the production `.env` path) — not reproduced |
| `config/system_config.yaml` | `alerts.smtp.username` L452, `alerts.smtp.from_address` L460, `alerts.smtp.to_addresses` L461-L462 | e-mail addresses — not reproduced |
| `config/system_config.yaml` | `webhook.bind_host` L328 (and comment L330) | IP literal — not reproduced |
| `config/system_config.yaml` | `alerts.telegram.bot_token_env` L388, `channels[].chat_id_env` L416, L419, `personal_chat_id_env` L422, `alerts.email_fallback.from_addr_env/password_env/to_addr_env` L444-L446, `alerts.smtp.password_env` L459 | env-var NAMES only; no secret values in the file (FACT) |
| `config/system_config.yaml` | `webhook.require_hmac` L336 comment | says auth uses a `?token=` query parameter, i.e. the secret travels in the Chartink-side URL (that URL is not in the repository) |
| `config/chartink_scanners.yaml`, `config/scan_webhook_map.yaml` | `scanners.*` / `scanners.*.chartink_url` | Chartink screener web addresses (host chartink.com, `/screener/…`); no token-like part visible (INTERPRETATION) — not reproduced |
| `config/index_universe.yaml` | comments L9-L12 | Kite instrument tokens for indices (public instrument numbers, not credentials) |
| `config/reference_data/security_master_file.csv` | column `" isin_number"` | public ISINs (not credentials) |

Outside `config/` (noted, not inventoried): account identifiers also appear in code comments and defaults (for example `main.py` L2356 comment, `scripts/reconcile_positions.py` L69 help text, `scripts/zerodha_login.py` L246 help text, `deploy/cron/trading-system.cron` L73 and L97 `--account` arguments, `core/schema.sql` L1495 comment); absolute home-directory paths appear in `scripts/security_monitor.py` L142, L213-L224 and `scripts/deploy_preflight.py` L33-L34; `ops_dashboard/backend/config/gui_config.yaml` has `auth.username`, `auth.password_hash`, `auth.totp_secret` keys that are empty in the tracked file (values live in the untracked overlay, §3).

---

## 3. Expected but absent

"Not tracked" is a FACT about the baseline. Whether the file existed on the VM is **UNKNOWN / NOT ESTABLISHED** in every row.

| Path as referenced | Referencing code (examples) | Tracked? | `.gitignore` | Notes |
|---|---|---|---|---|
| `config/instruments.csv` | `main.py` L2441 [D]; `utils/startup_checks.py` L841 (required, blocking `missing_config_files`, L1551-L1553); `scripts/preflight/checks/broker.py` L217, L226; `scripts/find_symbol_aliases.py` L61 [C]; `scripts/sr_level_export.py` L141 [R]; loader `core/instrument_cache.py` L101-L182 (A05); writer `scripts/refresh_instruments.py` L51 (`--csv` L361) | no | yes, L39 (reason L35-L38) | HISTORICAL: tracked until `2b4d976` (2026-06-21). A05 owns the content |
| `config/nse_holidays_<year>.yaml` for any year other than 2026 (e.g. 2027) | CL L2449 (required at boot); `utils/holiday_guard.py` L44 (`next_trading_day` L98-L111 crosses into the next year near 31-Dec); `utils/startup_checks.py` L865, L1385; preflight L36; premarket L62; `scripts/security_monitor.py` L957-L990 (alerts from mid-December) | no (only 2026) | no | `config/security.yaml` L66-L69 (HISTORICAL comment) says only NSE can supply and only Rama can commit it |
| `.env` (repo root) | 22 `load_dotenv` points (§5 ii); systemd `EnvironmentFile=` in `deploy/systemd/trading-system.service` L13, `alert-watcher.service` L18, `security-watcher.service` L18, `trading-watchman.service` L13; cron `set -a && . ./.env` (`deploy/cron/trading-system.cron`, e.g. L25); `deploy/resume.sh` L29; `deploy/token_watcher.sh` L78; `config/security.yaml` L132 (watched) | no | yes, L6 (`.env`), L7 (`env`), L59 (`.env/`) | `.env.example` is the tracked template. HISTORICAL comment `config/system_config.yaml` L425-L429 states three `ALERT_EMAIL_*` variables were absent from the VM `.env` |
| `data_store/strategy_direction_registry.yaml` | `core/strategy_direction.py` L44; officer L282 | no | yes, `data_store/` L17 | runtime state that wins over the tracked seed once present (L98-L121) |
| `data_store/security/ssh_key_baseline.json` | `scripts/security_monitor.py` L75, L186-L210 | no | yes (`data_store/`) | when present it REPLACES the committed `expected_key_fingerprint` and count (L194-L195, L202-L209) |
| `data_store/session/zerodha_token.json` | `main.py` L2362; `scripts/refresh_instruments.py` L329; `scripts/reconcile_positions.py` L113; `scripts/preflight/checks/broker.py` L66; others | no | yes (`data_store/`) | credential file (A04); `.env.example` L11-L13 points to it |
| `ops_dashboard/backend/config/gui_config.local.yaml` | `ops_dashboard/backend/app.py` L153-L168 (deep-merge overlay) | no | yes, `ops_dashboard/.gitignore` L9 | A15 |
| "a non-committed config_overrides file" | only the comment `config/system_config.yaml` L455-L456 | no | — | **no reader found by grep**; `load_all` has no override or include mechanism (CL5, `core/config_loader.py` L20) |
| systemd drop-in `/etc/systemd/system/trading-system.service.d/*.conf` | documents only, no code: for example `docs/SYSTEM_MAP.md` L470-L472 (HISTORICAL: "Telegram bot token / chat IDs are also injected via the systemd drop-in") and L852, `PATHS.md` L236, `docs/CONFIG_GUIDE.md` L455, and several `docs/audit/` reports | no tracked file | — | read by systemd, not by code |

Everything else that code under `config/` names was found tracked (scripted scan of non-test string literals).

---

## 4. Configuration sources outside `config/`

### 4.1 Command line

FACT: `main.py::_parse_args` L179-L212: `--config PATH` ("Override config/ directory path", L192-L195), `--mode {paper,live}` default **paper** (L184-L187), `--resume`, `--status`, `--dry-run`, `--version`, `--interactive`. `config_dir = Path(args.config) if args.config else Path("config")` (L2099), i.e. relative to the working directory.

FACT: the declared unit `deploy/systemd/trading-system.service` starts `main.py --mode live` with no `--config` (L18-L19) and a declared `WorkingDirectory` (L10). Whether this unit was the one installed on the VM is UNKNOWN / NOT ESTABLISHED.

`config_dir` reaches: `load_all` (L2198); the holiday guard (L2102-L2111); `TelegramNotifier.from_env(config_dir=…)` (L331); `AccountRegistry.load` (L2359, L2414); `InstrumentCache.load` (L2441); `run_all_startup_checks(config_dir=…)` (L2463); `scan_strategy_errors` (L2496); the strategy loader (L3157). FACT: these readers do **not** follow `--config` because they build their own path: `signals/webhook_receiver.py` L265 [C]; `core/effect_telemetry.py` L63 [C]; `orders/eod_squareoff.py` L696 [C]; `core/strategy_direction.py` defaults L43-L44 [C]; `core/account_registry.py::_read_primary_row` L308-L310 [R]; `scripts/fetch_daily_candles.py` L40 [R]; and `main.py` L2362, L2466 (`data_store/…` literals).

Script-level options (FACT): `--config-dir` in `scripts/revert_temp_config.py` L112, `scripts/preflight/orchestrator.py` L152, `scripts/premarket_healthcheck.py` L185, `scripts/check_cron_drift.py` L176, `scripts/cron_officer.py` L865, `scripts/strategy_registry_officer.py` L268, `scripts/system_manager.py` L1298, `reports/daily_trade_review.py` L2872, `reports/daily_report.py` L1846, `ops/control_tower/aggregator.py` L302, `ops/control_tower/runner.py` L79; `--config` in `scripts/alert_watcher.py` L780, `scripts/compute_strategy_metrics.py` L48, `scripts/reconcile_pnl.py` L61, `scripts/reconcile_positions.py` L52, `scripts/preflight_scanner_check.py` L40, `scripts/replay_signals.py` L228, and (meaning the security YAML file) `scripts/security_monitor.py` L1343, `scripts/copy_gate.py` L351, `scripts/approve_ssh_keys.py` L74, `scripts/request_copy.py` L122, and (meaning the dashboard's `gui_config.yaml`) `ops_dashboard/backend/auth.py` L339. Defaults mix `"config"` [C] and `_ROOT / "config"` [R].

### 4.2 Environment variables
See §5.

### 4.3 Constants and literals standing in for configuration (examples found in this pass; not exhaustive)

| Where | What | Relation to a config file |
|---|---|---|
| `scripts/preflight/checks/config_integrity.py` L71-L72 | `CAPS_EXPECTED_MAX_OPEN = 5`, `CAPS_EXPECTED_MAX_DAILY = 10` | expected values compared with `risk.max_open_positions` / `risk.max_daily_trades` in `system_config.yaml` (L116-L124) |
| `scripts/preflight/checks/broker.py` L41 | `MIN_BROKER_CASH_RS_DEFAULT = 2000.0` | fallback for `preflight.yaml` `startup_floors.min_broker_cash_rs` |
| `main.py` L2000-L2001; `core/config_loader.py` L83 | `SERVICE_WINDOW_START` 08:00, `SERVICE_START_CUTOFF = SERVICE_WINDOW_END_MAX` 18:15 | service-start window enforced before config is loaded (L2154-L2176) |
| `main.py` L219-L232; `scripts/preflight/checks/config_integrity.py` L27-L31; `scripts/premarket_healthcheck.py` L47-L51 | required secret NAME lists (three separate lists) | — |
| `utils/startup_checks.py` L833-L843; `scripts/preflight/checks/config_integrity.py` L16-L24, L34-L36; `scripts/premarket_healthcheck.py` L54-L63 | three separate required-config-file lists | parallel to `_CONFIG_FILES` L2441-L2450; only the startup list includes `instruments.csv` and `accounts.csv` |
| `scripts/revert_temp_config.py` L33-L100 | `TEMP_REVERTS` "prod_value" table | §6 |
| `scripts/security_monitor.py` L110-L148, L213-L224; `scripts/copy_gate.py` (CopyConfig defaults) | in-code defaults mirroring `security.yaml` | used when the file is missing or unreadable |
| direct readers' own defaults | e.g. `scripts/cron_officer.py` L474-L475; `alerts/telegram_notifier.py` L96-L98 (`enabled` True); `reports/daily_report.py` L141 (60); `ops_dashboard/…/config_reader.py` L70, L80 (`enabled` True, `max_concurrent_positions` 2) | apply only when the key is absent from the file |
| `scripts/refresh_instruments.py` L55-L85 | `_REQUIRED_SYMBOLS`, `_MIN_ROW_COUNT = 1000`, `_EQ_SERIES`, `_SECTOR_INDEX_PRIORITY` | A05 |
| `scripts/compute_strategy_metrics.py` L37-L39 | `_SHARPE_DEMOTION_THRESHOLD = -0.3`, `_CONSECUTIVE_BAD_DAYS = 3` | A07; its alert text says "Strategy set to PAPER_ONLY" (L224) — no write of such a status to any file or table was found by grep |
| pydantic field defaults in `core/config_loader.py` (e.g. `FnoBanConfig.url` L1834; `EmailFallbackConfig` env names L958-L960; `personal_chat_id_env` L984) | apply when a key is absent | mapped key by key in the A02 evidence on key consumers |

### 4.4 Database-backed configuration

FACT (grep of `CREATE TABLE` in `core/schema.sql` and `core/analytics_schema.sql`): no settings or override table exists. Two config-related records exist:

| Table | Written by | Read by | Nature |
|---|---|---|---|
| `config_snapshots` (`core/schema.sql` L1491-L1500) | `core/config_snapshotter.py::snapshot_config` L148-L217, called `main.py` L2602-L2614 (non-fatal) | `ops_dashboard/backend/readers/config_reader.py::get_system_config` L33-L44 (snapshot first, YAML fallback), `ops_dashboard/backend/readers/db_reader.py` L631, L1554, L3324-L3342, L4202; `reports/daily_trade_review.py` L350, L1196 | a copy of the resolved `AppConfig` (secret-named keys redacted, `_env` names kept: L45-L58); downstream readers treat it as "the config as it was" |
| `session.last_config_hash` (`core/schema.sql` L496) | `main.py` L2312, L4178 (`json.dumps(app_config.file_hashes)`) | `utils/startup_checks.py::check_config_hash` L581-L634 | per-file hash comparison between restarts |

Runtime state that changes behaviour but is not configuration (boundary only): `kill_switch_state` (A13), `data_store/strategy_direction_registry.yaml` (A07), the pre-flight sentinel `data_store/preflight/today.json` (A20), the SSH baseline override (A17).

### 4.5 Other configuration files outside `config/`

| File | Read by | Notes |
|---|---|---|
| `ops_dashboard/backend/config/gui_config.yaml` + untracked `gui_config.local.yaml` | `ops_dashboard/backend/app.py::load_gui_config` L153-L168 (A15) | its own `paths.config_dir` (tracked value is a PC path, not reproduced) decides which `config/` the dashboard reads; holds a `market_clock` block (`market_open`, `entry_start`, `entry_end`, `eod_squareoff`, `market_close`, `active_weekdays`) separate from `system_config.yaml` `trading_hours` |
| `deploy/systemd/*.service` `Environment=` lines | systemd | `PATH`, `PYTHONUNBUFFERED`, `PYTHONPATH`, `PROJECT_DIR`, `SLEEP_SEC` (A17) |
| `deploy/cron/trading-system.cron` | cron | generated from `config/cron_registry.yaml` (A16); sources `.env` per job |
| `data_store/session/zerodha_token.json` | broker/session code (A04) | credentials, not settings |

---

## 5. Environment variables

### (i) `.env.example` — key names only

FACT: 50 lines, **20 keys**, all values placeholders (not reproduced).

| Lines | Comment grouping | Keys |
|---|---|---|
| L1-L14 | header: copy to `.env`; never commit `.env`; "NEVER put a real value in THIS template"; pre-commit scanner `deploy/hooks/secret_scan.py`; "Access tokens come from data_store/session/zerodha_token.json … No ACCESS_TOKEN in this file" | — |
| L16-L39 | five blocks "--- Zerodha `<ACCOUNT_ID>` (`<name>`) -- `<status>` ---" (statuses: PRIMARY ×1, ENABLED ×1, DISABLED ×3) | per block: `ZERODHA_API_KEY_<ACCOUNT_ID>`, `ZERODHA_API_SECRET_<ACCOUNT_ID>`, `ZERODHA_TOTP_<ACCOUNT_ID>` (15 keys) |
| L41-L45 | "--- Telegram Alerts ---" | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_PRIMARY`, `TELEGRAM_CHANNEL_SECONDARY`, `TELEGRAM_PERSONAL_CHAT_ID` |
| L47-L50 | "--- Webhook Security ---" (generate once; same value in the Chartink webhook config) | `WEBHOOK_SECRET` |

FACT: the 15 env-name values in `config/accounts.csv` all appear as keys in `.env.example`; none of the 8 names in `accounts_multi_example.csv` do. When `.env.example` is staged, the pre-commit scanner applies a placeholder-only rule to it (`deploy/hooks/secret_scan.py` L97, L116-L128; A17); it does not open the file otherwise.

### (ii) Every environment read in non-test Python (scripted AST scan of the source text; cross-checked with `git grep`)

FACT (AST scan of all non-test Python): **84 environment-related sites**, made up of **57 reads** (every one is in the table below), **3 writes** of the form `os.environ[...] = …` (all in `main.py`, table (iv)), **22 `load_dotenv` calls** (next paragraph) and **2 child-process environment pass-throughs** (table (iv)). The 84 are therefore not 84 reads.

Dotenv load points (FACT, 22, none passes `override`): explicit `<repo root>/.env` — `scripts/agy_runner.py` L23, `auto_refresh_token.py` L53, `check_cron_drift.py` L39, `clear_kill_switch.py` L31, `cron_officer.py` L29, `cron_watchdog.py` L23, `eod_broker_reconcile.py` L53, `fetch_daily_candles.py` L32, `forward_shadow_record.py` L35, `gemini_data_integrity_check.py` L38, `gemini_log_review.py` L32, `gemini_premarket_brief.py` L34, `gemini_trade_coach.py` L35, `gemini_watchman.py` L39, `gemini_weekly_patterns.py` L32, `liveness_probe.py` L65 (inside `try`), `monitoring_canary.py` L58 (inside `try`), `reconstruct_excursions.py` L60, `strategy_registry_officer.py` L36, `system_manager.py` L51; no argument — `scripts/refresh_instruments.py` L45, `scripts/zerodha_login.py` L36. INTERPRETATION (python-dotenv semantics): without `override=True` a variable already in the process environment wins; with no argument, `find_dotenv()` searches upward from the calling file's directory, which reaches the repo-root `.env`. FACT: `main.py`, `scripts/alert_watcher.py`, `scripts/security_monitor.py` and the pre-flight orchestrator have no `load_dotenv`; they depend on the environment given by systemd `EnvironmentFile=` or the cron line (§3, `.env` row).

| Variable (name or source of the name) | Read at (file L, function) | Required / optional | Fallback / effect when unset | Owner |
|---|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | `alerts/telegram_notifier.py` L288 `from_env` | optional | `""` → no notifier (L290-L291) | A14 |
| 〃 | `main.py` L269 `_send_holiday_notification` | optional | silent return (L271-L272) | A01 |
| `alerts.telegram.bot_token_env` (file value `TELEGRAM_BOT_TOKEN`) | `main.py` L2629 | required (`os.environ[...]`, KeyError; no handler at the site) | — | A01 / A14 |
| `TELEGRAM_BOT_TOKEN` | `scripts/cron_officer.py` L595; `scripts/monitoring_canary.py` L265 | optional | health flag "no token" / `""` | A16 / A15 |
| `TELEGRAM_CHANNEL_PRIMARY` | `alerts/telegram_notifier.py` L289; `main.py` L270 | optional | as above | A14 / A01 |
| `channels[].chat_id_env` (file values `TELEGRAM_CHANNEL_PRIMARY`, `TELEGRAM_CHANNEL_SECONDARY`) | `alerts/telegram_notifier.py` L622 | optional per enabled channel (file value: secondary `enabled: false`) | channel skipped with a warning (L623-L627) | A14 |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_PRIMARY`, `WEBHOOK_SECRET` | presence checks `scripts/preflight/checks/config_integrity.py` L60 (list L27-L31); `scripts/premarket_healthcheck.py` L79 | check only | CRITICAL fail / reported missing | A20 |
| `ZERODHA_API_KEY_<id>`, `ZERODHA_API_SECRET_<id>`, `TELEGRAM_BOT_TOKEN`, `WEBHOOK_SECRET` | `utils/startup_checks.py::check_required_secrets` L1071-L1086, names from `main.py::required_startup_secrets` L219-L232 (account part from the primary `account_id`) | check only | any missing → blocking failure `missing_secrets` (L1556-L1558) | A01 |
| `WEBHOOK_SECRET` | `main.py` L3414 | optional at the site | `None` passed as `secret_token` | A01 / A06 |
| `accounts.csv` `api_key_env` (primary) | `core/account_registry.py::primary_api_key` L357-L360 (callers `fetch_daily_candles.py` L44, `gemini_data_integrity_check.py` L49, `reconstruct_excursions.py` L69, `forward_shadow_record.py` L107) | optional | `""` | A01 (callers A05/A15/A18) |
| 〃 | `main.py` L2361 (live) | required (KeyError) | caught L2371-L2374 → `return 6` | A01 |
| 〃 / `api_secret_env` | `main.py` L1894-L1895 (`--interactive`) | required for login | exit 5 (L1896-L1898) | A01 |
| `selected_account.api_key_env` | `main.py` L2928 (live feed) | optional | `""` | A01 / A05 |
| `api_key_env` / `api_secret_env` / `totp_secret_env` (selected account), each with a generic fallback `ZERODHA_API_KEY` / `ZERODHA_API_SECRET` / `ZERODHA_TOTP_SECRET` | `scripts/auto_refresh_token.py` L351-L353 via `_resolve_env` L97-L108 | required | any missing → CRITICAL alert, `return 1` (L359-L367) | A04 |
| `ZERODHA_USER_ID_<id>` → `ZERODHA_USER_ID`; `ZERODHA_PASSWORD_<id>` → `ZERODHA_PASSWORD` | `scripts/auto_refresh_token.py` L349-L350 | required | as above | A04 |
| `api_key_env` / `api_secret_env` | `scripts/zerodha_login.py` L267-L268 | required | error print | A04 |
| `api_key_env` (with `--account`), else `ZERODHA_API_KEY` + `ZERODHA_ACCESS_TOKEN` | `scripts/refresh_instruments.py` L325, L340-L341 | required | exit 1 / error print | A05 |
| `api_key_env` (with account), else `ZERODHA_API_KEY` + `ZERODHA_ACCESS_TOKEN` | `scripts/reconcile_positions.py` L109, L131-L132 | required | `RuntimeError` | A12 |
| `ZERODHA_API_KEY`, `ZERODHA_ACCESS_TOKEN` | `scripts/reconcile_pnl.py` L99-L100 | required | error path | A12 |
| `ZERODHA_API_KEY`, `ZERODHA_ACCESS_TOKEN` | `main.py::_build_kite_client` L386-L387 | required (KeyError) | values are written by `main.py` itself first (iv) | A01 / A04 |
| `ZERODHA_ACCESS_TOKEN` | `main.py` L2929 | optional | `""` | A01 / A05 |
| `f"ZERODHA_API_KEY_{ctx.account}"` | `scripts/preflight/checks/broker.py` L149 | optional | broker probe not built (`None`) | A20 |
| `f"ZERODHA_API_KEY_{account}"` → `ZERODHA_API_KEY` | `scripts/t2_cnc_gtt_realtest.py` L161 | optional | `None` api_key | A19 |
| `alerts.smtp.password_env` (file value `ALERT_SMTP_PASSWORD`) | `core/config_loader.py::SmtpConfig.resolved_password` L935-L948; called `scripts/alert_watcher.py` L295, L582; `scripts/monitoring_canary.py` L85 | required when the name is set | `ValueError` (L942-L947) | A02 (callers A14/A15) |
| `alerts.email_fallback.from_addr_env/password_env/to_addr_env` (file values `ALERT_EMAIL_USER`, `ALERT_EMAIL_PASSWORD`, `ALERT_EMAIL_TO`) | `alerts/telegram_notifier.py::_send_email_fallback` L805-L807 | optional | warning `email_fallback.missing_credentials`, return False (L809-L813) | A14 |
| `TS_IGNORE_MARKET_WINDOW` | `main.py` L2159, L4132 | optional operator override | equals `"1"` → service-window guard and EOD self-exit bypassed | A01 |
| `TRADING_MODE` | `scripts/compute_strategy_metrics.py` L298, `scripts/eod_broker_reconcile.py` L344, `scripts/eod_verify.py` L204, `scripts/reconcile_pnl.py` L311, `scripts/reconcile_positions.py` L352 | optional | default `"live"`; `"paper"` selects paper behaviour (not traced) | A07 / A12 |
| `DB_PATH` | `scripts/check_vm_state.py` L48 | optional | `data_store/trading_system.db` | A15 |
| `GEMINI_BIN` | `scripts/agy_runner.py` L60 | optional | `shutil.which("agy")` | A15 |
| `TRADING_VM` | `scripts/deploy_preflight.py` L32 | optional (PC-side tool) | default host alias | A17 |
| `CONTROL_URL`, `CONTROL_SECRET` | `ops_dashboard/backend/readers/control_client.py` L36, L46 | optional, after the gui config `control_plane` keys | a loopback default URL (L31) / `None` | A15 |
| `OPS_DASHBOARD_LOCAL_DEV` (name at L54) | `ops_dashboard/backend/app.py` L93 | optional gate | must equal `"1"` for local auto-login | A15 |
| `LOGNAME`, `USER`, `SSH_CONNECTION` (OS) | `scripts/copy_gate.py` L250-L251; `scripts/request_copy.py` L84 | optional | audit identity | A17 |
| `TEMP` (OS, Windows only) | `utils/instance_lock.py` L50 | optional | a Windows temp directory | A01 |

Credential-related names are recorded by type above; no values were read from any environment.

### (iii) Mismatches between code and `.env.example`

Read by code, **absent from `.env.example`** (FACT): `ZERODHA_API_KEY`, `ZERODHA_ACCESS_TOKEN` (both also written by `main.py`; `.env.example` L13 says no access token belongs there), `ZERODHA_API_SECRET`, `ZERODHA_TOTP_SECRET`, `ZERODHA_USER_ID_<id>`, `ZERODHA_USER_ID`, `ZERODHA_PASSWORD_<id>`, `ZERODHA_PASSWORD`, `ALERT_SMTP_PASSWORD`, `ALERT_EMAIL_USER`, `ALERT_EMAIL_PASSWORD`, `ALERT_EMAIL_TO`, `TS_IGNORE_MARKET_WINDOW`, `TRADING_MODE`, `DB_PATH`, `GEMINI_BIN`, `TRADING_VM`, `CONTROL_URL`, `CONTROL_SECRET`, `OPS_DASHBOARD_LOCAL_DEV`; OS-supplied `LOGNAME`, `USER`, `SSH_CONNECTION`, `TEMP`.

In `.env.example`, **no read found**: `TELEGRAM_PERSONAL_CHAT_ID` — named by `system_config.yaml` L422 and the schema field `core/config_loader.py` L984 ("reserved for v2.1 bot commands; zero sends"), but no `os.environ` read of it exists. `TELEGRAM_CHANNEL_SECONDARY` has a read path that runs only for an enabled channel (file value disabled). The per-account keys of non-primary accounts are read only when that account is the one selected (`--account`, `--interactive`); this is dynamic, so "no code reads them" cannot be said.

### (iv) Variables the code writes

| Where | Variable | Value source |
|---|---|---|
| `main.py` L2361 | `ZERODHA_API_KEY` | value of the primary account's `api_key_env` variable (live) |
| `main.py` L2363 | `ZERODHA_ACCESS_TOKEN` | `data_store/session/zerodha_token.json` (live) |
| `main.py` L2576 | `ZERODHA_ACCESS_TOKEN` | token resolved during account selection |
| `scripts/agy_runner.py` L116; `scripts/system_manager.py` L1189 | child-process environment only (`{**os.environ}`; `GIT_INDEX_FILE` added) | not written into the parent environment |

---

## 6. `scripts/revert_temp_config.py` (static trace only; not run)

| Aspect | Finding |
|---|---|
| Purpose | FACT, docstring L4-L6: "Scan config YAML files for TEMP markers. Print proposed reverts in dry-run mode (default). Apply reverts with --apply --confirm." HISTORICAL: added `37e6698` (2026-06-03, "FIX-151 … TEMP tracker"); changed `c69f1fd` (2026-06-24, removed the `capital.daily_loss_limit` entry, L34-L36). |
| Arguments | FACT L103-L113: `--apply`, `--confirm` (store_true), `--config-dir` (default `<repo root>/config`, L31, L112). |
| What it recognises | FACT: a fixed table `TEMP_REVERTS` L33-L100 of 7 entries: 6 in `system_config.yaml` (`risk.max_consecutive_losses`, `risk.daily_loss_limit_pct`, `order_reconciler.capital_drift_tolerance`, `drift_handler.log_only_threshold_rs`, `drift_handler.soft_kill_threshold_rs`, `drift_handler.hard_kill_threshold_rs`) and 1 in `strategies/gap_fade_long.yaml` (`min_score`). Each has an unanchored regex (e.g. `daily_loss_limit_pct:\s*[\d.]+`), a `temp_value` and a `prod_value`. No glob; no other file is examined. |
| Detection | FACT L124-L125: an entry is `ACTIVE_TEMP` when the **whole file text** contains the substring `"TEMP"` anywhere AND the regex matches anywhere; otherwise `ALREADY_REVERTED` (L136-L142). The dotted `key` is only a label; the regex is not section-aware. Missing file → warning, entry skipped (L120-L122). |
| Report | FACT L177-L199: prints counts; for active entries prints "Current: {temp_value}" — the hard-coded table value, not the value found in the file (`current_line` L128-L129 is collected but not printed). |
| What it changes | FACT L147-L174: for each `ACTIVE_TEMP` entry, re-reads the file, `re.sub(pattern + r".*?(#.*)?$", f"{key_name}: {prod_value}  # REVERTED from TEMP {temp_value}", count=1, flags=re.MULTILINE)` — replaces the first match through end of line, including any trailing comment. `key_name` is the bare YAML key taken from the pattern (`old_pattern.split(r":\s*")[0]`, L157-L158; for example `daily_loss_limit_pct`), not the dotted `key` label (for example `risk.daily_loss_limit_pct`), which is used only in the log message (L170-L171). |
| How it writes | FACT L169: `Path.write_text(..., encoding="utf-8")` — in place; no backup; no temporary file or rename (INTERPRETATION: not atomic; a failure during the write can leave a truncated file). Each entry re-reads and rewrites, so changes accumulate in one file. |
| Safeguards | FACT: no interactive prompt. Default is dry-run. `--apply` without `--confirm` → message, exit 3 (L222-L224). The order of checks means `--confirm` alone is a dry-run (exit 2, L217-L220). No check that the matched value equals `temp_value`; no check of the running service, market hours or mode. |
| Errors / partial writes | FACT L207-L233: any exception → `log.error`, exit 1. INTERPRETATION: entries already written before the exception stay written. |
| Exit codes and outputs | FACT: 0 clean (L213-L215) or after apply (L226-L229); 2 active entries in dry-run (L220); 3 apply without confirm; 1 error. Docstring L13 says "0 -- … or dry-run complete", but a dry-run that finds entries returns 2 (L217-L220). Output: stdout report and `core.logger.get_logger("revert_temp_config")` (import L29; logging side effects not traced, A15). |
| Against the baseline text | INTERPRETATION, checked with an independent re-implementation of the two regex steps, kept outside the clone (the table read with `ast.literal_eval`; the script itself was not run): `system_config.yaml` contains `"TEMP"` only inside the word "ATTEMPT" at L407, so all 6 `system_config.yaml` entries would classify `ACTIVE_TEMP`. With `--apply --confirm` the only value change would be `risk.daily_loss_limit_pct` L316 from the file value `0.03` to the table value `0.05` (table label "5%", L52); the other 5 lines keep their values but lose their inline comments (L315, L470, L727, L728, L729). `gap_fade_long.yaml` contains no `"TEMP"` → `ALREADY_REVERTED`; its file value `min_score: 0` (L41) differs from the table `prod_value` 60. |
| Relation to the startup check | FACT: `utils/startup_checks.py::check_temp_config_values` L1465-L1502 counts the different marker `"# TEMP"` in top-level and `strategies/` YAMLs; WARNING only (L1643-L1646). |
| Declared or invoked? | FACT: no entry in `config/cron_registry.yaml`, nothing under `deploy/`, no systemd unit, no import from `main.py` or any script (`git grep revert_temp` over config, deploy, scripts, main.py, ops, ops_dashboard: only the script itself). Mentions: `docs/06_deployment_guide.md` L240 ("Switching Paper → Live … 2. Revert TEMP config values: … --apply --confirm"), `docs/temp_config_tracker.md` L4, L31, L34 (HISTORICAL, "Last Updated 2026-06-03", lists 8 entries including the since-removed one), `docs/gui_project/G0_BACKEND_INVESTIGATION_REPORT.md` L126; test `tests/unit/test_revert_temp_config.py` (A19). Whether it was ever run on the VM is UNKNOWN / NOT ESTABLISHED. |
