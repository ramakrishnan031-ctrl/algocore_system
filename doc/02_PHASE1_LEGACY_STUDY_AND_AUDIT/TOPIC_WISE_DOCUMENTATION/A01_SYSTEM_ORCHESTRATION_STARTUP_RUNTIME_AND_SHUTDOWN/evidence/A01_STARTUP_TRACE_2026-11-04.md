# A01 evidence: the startup trace, from process invocation to the runtime wait

**Status:** DRAFT — evidence for the A01 STUDY, for ChatGPT's review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04. Corrected, 2026-11-04: after an independent check of the statements against the code.
**Purpose and scope:** Every startup step of `main.py` in code order, from the module import to the runtime wait at L4249, one row per step, and the table of the objects that startup constructs. It supports the STUDY, sections 5, 6 and 12 (Q5, Q10 to Q16 and Q34 of ChatGPT's A01 direction). Live only: paper-only branches are marked and not traced.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on 04-Nov-2026; nothing was run.

Conventions:

- Every row is FACT for the lines it cites, unless a cell says INTERPRETATION. All lines are in `main.py` unless a path is given.
- "Owner" is the topic that owns the callee (Master System Investigation Index). A01 records the call and the handoff; the callee's internals are the owner's.
- "uncaught (1/2)" means: the exception leaves `_main_locked`; `main()` releases the instance lock in its `finally` (L2189 to L2190); the entry guard logs CRITICAL and exits 1 for a `TradingSystemError` subclass (L4288 to L4290) or 2 for any other `Exception` (L4291 to L4293); `_shutdown` is not run and no SHUTDOWN marker is written. Before L2178 the same exits apply, but logging is not yet configured.
- "store not closed" is stated only where the code has a handled return without `store.close()`. Uncaught exceptions never close the store.
- Configuration values quoted from `config/` are facts about the files at the baseline only; the values in force are UNKNOWN / NOT ESTABLISHED (Document 08, section 10).

## 1. Import time and the entry guard

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| I1 | L22 to L106 | 74 module-level import statements (structure file, section 3.1) | various | - | - | every imported module loaded; `scripts.zerodha_login` runs `load_dotenv()` at its L36 (A04) | INTERPRETATION: an import failure happens outside the guard; Python prints a traceback and exits with status 1 | 1 (interpreter) |
| I2 | L108 to L135 | module globals | A01 | - | - | `VERSION`, `_log`, `_shutdown_event`, `_broker_auth_failed`, the two token paths | - | - |
| I3 | L865 to L867 | `_gate_release_pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="gate-release")` | A01 | - | - | executor object; INTERPRETATION (CPython): its worker threads start on the first `submit` | - | - |
| I4 | L2000 to L2001 | `SERVICE_WINDOW_START = 08:00`; `SERVICE_START_CUTOFF = SERVICE_WINDOW_END_MAX` | A01 (A02 constant) | `core/config_loader.py` L83: 18:15 | - | the START window bounds | - | - |
| I5 | L4285 to L4293 | `if __name__ == "__main__": sys.exit(main())` | A01 | `sys.argv` | only when run as a script | - | `TradingSystemError` → CRITICAL `system_error`, exit 1; other `Exception` → CRITICAL `unexpected_error`, exit 2. INTERPRETATION: `SystemExit` and `KeyboardInterrupt` are not `Exception` subclasses and pass through | main()'s value |

## 2. `main()` (L2085 to L2190)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| M1 | L2089 to L2092 | `_parse_args(argv)` (L179 to L212) | A01 | `sys.argv[1:]` | argparse `choices` for `--mode` only | `args` | `SystemExit` with code 0 (`--help`) → 0; any other code → 5 | 0 or 5 |
| M2 | L2094 to L2096 | `--version` | A01 | `args.version` | the first branch | prints the version | - | 0 |
| M3 | L2099 | `config_dir = Path(args.config) if args.config else Path("config")` | A01 | `--config` | no existence check | `config_dir`; a relative path resolves against the working directory | - | - |
| M4 | L2100 | `today = date.today()` | A01 | the host-local date | - | `today`, a local of `main()` only | - | - |
| M5 | L2101 to L2152 | holiday and weekend guard: `is_trading_day`, `next_trading_day`, `get_holiday_name`, `_send_holiday_notification` | A01; the Telegram send is an A14 boundary | `today`; `<config_dir>/nse_holidays_<year>.yaml`; env `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_PRIMARY` | not a trading day → framed message (L2113 to L2128) and, once a day, a Telegram message guarded by the sentinel `logs/.holiday_notified_<date>` (L2133 to L2149) | the sentinel file (written after the send attempt, whatever its result) | `FileNotFoundError` → proceed with startup (L2151 to L2152); any other exception is uncaught, before logging (1/2) | 0 |
| M6 | L2157 to L2176 | START window guard: `time_authority.now_ist()` (L2161), `_within_service_window` (L2004 to L2015) | A01 | IST clock; the flags; env `TS_IGNORE_MARKET_WINDOW` | bypassed by `--status`, `--dry-run`, `--interactive`, `--resume` or the env value `"1"`; otherwise the IST time must be in [08:00, 18:15) | - | outside the window → one printed line (L2166 to L2175) | 0 |
| M7 | L2178 to L2180 | `setup_logging(Path("logs"))`; `_log = get_logger("main")`; INFO start line | A15 | - | - | root log handlers; `_log` rebound | uncaught (1/2) | - |
| M8 | L2183 to L2186 | `acquire_instance_lock()` (`utils/instance_lock.py` L129 to L202) | A01 | default port 5001 | layer 1: exclusive non-blocking file lock; layer 2: loopback TCP bind and `listen(1)` | lock fd and socket held for the process lifetime | refused → CRITICAL `Instance lock failed` | 1 |
| M9 | L2187 to L2190 | `return _main_locked(args, config_dir)` inside `try/finally: release_instance_lock()` | A01 | `args`, `config_dir`; `today` is not passed | - | - | the `finally` runs on every exit from `_main_locked` | the code returned |

## 3. `_main_locked` (L2193 to L4278), in code order

### 3.1 Phase 0b, service window and Phase 0c (L2196 to L2296)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S1 | L2197 to L2202 | `load_all(config_dir)` | A02 | the config files | - | `app_config`; INFO with the file count | any `Exception` → CRITICAL `Config load failed` with `_config_error_detail` (L2018 to L2038) | 5 |
| S2 | L2205 | `config_validator.register_all_from_app_config(app_config)` | A02 | `app_config` | - | the usage-tracking registry | uncaught (1/2) | - |
| S3 | L2211 to L2216 | `_parse_hhmm(trading_hours.service_window_end)`; `_service_window_banner(...)` | A01 | config key (file value "17:35", `config/system_config.yaml` L112) | - | `_service_window_end` (consumed at L4142); INFO banner | uncaught (1/2) | - |
| S4 | L2226 to L2232 | market-open test for the migration rule | A01 | `now_ist()`; `trading_hours.market_open`, `market_close` | weekday and `open <= time <= close`; no holiday or special-session test | `_market_open_now` | uncaught (1/2) | - |
| S5 | L2233 to L2237 | `StateStore(Path("data_store/trading_system.db"), allow_migrate=True, market_open=_market_open_now)` | A03 | the DB path, relative to the working directory | the comment at L2219 to L2225 calls this "the ONLY sanctioned migrator"; migration refused while the market is open (A03) | `store`, schema applied on open (A03) | uncaught; `MigrationNotPermitted` is a `TradingSystemError` (A03) → 1 | 1 or 2 |
| S6 | L2238 | `EventBus()` | A01 | - | - | `event_bus` | - | - |
| S7 | L2241 | `mode_label = str(args.mode or "live").upper()` | A01 | `args.mode` | - | "LIVE" under `--mode live` | - | - |
| S8 | L2243 to L2251 | `KillSwitch(store, event_bus, get_logger("kill_switch"), api_failure_threshold, enable_auto_trip, mode, emergency_exit_buffer_pct)` | A13 | `system.kill_switch.*`; `system.capital.emergency_exit_buffer_pct` | - | `kill_switch`; persisted state loaded by the constructor (A13) | uncaught (1/2); store not closed | - |
| S9 | L2254 | `_init_time_authority(app_config, kill_switch)` (L360 to L378) | A01 | `system.clock` warn, alert, halt, startup-max values | - | thresholds and the critical-skew callback in `core/time_authority.py` | uncaught (1/2) | - |
| S10 | L2255, L2266 | `time_authority.now_ist().date()` | A01 | IST clock | - | `today_ist_date`; `today_iso` | - | - |
| S11 | L2260 | `kill_switch.clear_stale_state(today_ist_date)` | A13 | - | result discarded | kill state may change (A13) | uncaught (1/2) | - |
| S12 | L2265 | `kill_switch.auto_clear_scheduled_kill()` | A13 | - | result discarded | kill state may change (A13) | uncaught (1/2) | - |
| S13 | L2268 to L2269 | `detect_startup_scenario(store, kill_switch, today_ist_date, _log)` | A01 | the session row; the kill status; today's SHUTDOWN event; today's EOD log | COLD, WARM, CRASH or HALT (checks catalogue, section 2) | `scenario_result`, `scenario` | uncaught (1/2) | - |
| S14 | L2271 to L2292 | branch on the scenario | A01 | `scenario`; `args.resume` | COLD, WARM: INFO. CRASH: CRITICAL and `store.insert_system_event(event_type="CRASH_DETECTED", ...)` (L2277 to L2282). HALT without `--resume`: CRITICAL, `store.close()`. HALT with `--resume`: `kill_switch.resume(reason="--resume flag", resumed_by="operator")` (A13), CRITICAL | a `system_events` row for CRASH | HALT without `--resume` returns | 4 |
| S15 | L2295 to L2296 | `check_config_hash(store, app_config, _log)` | A01 | `session.last_config_hash` against `app_config.file_hashes` | - | `hash_result`, `config_hash_changed` | unreadable stored hashes → WARNING, no change reported | - |

### 3.2 `--status`, the early session row and Phase 0d (L2298 to L2522)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S16 | L2299 to L2302 | `_print_status(store, kill_switch, scenario_result)` | A01 | `args.status` | only with the flag | prints scenario, kill state, the previous session row, version | `store.close()` | 0 |
| S17 | L2308 to L2314 | `_write_session(store, today_iso, args.mode, json.dumps(app_config.file_hashes), now)` (L619 to L633) | A01; the table is A03's | - | always | session row id=1, by INSERT OR REPLACE, with the literals `account_id='default'` and `trade_type='INTRADAY'` | uncaught (1/2) | - |
| S18 | L2317 to L2318 | `_load_holidays`; `_load_special_sessions` | A01 (schema A02) | `app_config.nse_holidays`; `system.special_sessions` (file: key present, only commented examples, L117 to L122) | - | `holidays` (a set of dates); `special_sessions` (a dict) | a malformed special session raises `ValueError` or `KeyError`: uncaught (2) | - |
| S19 | L2319 to L2329 | `MarketWindows(...)` from six `trading_hours` times | A01 | config | - | `market_windows` | uncaught (1/2) | - |
| S20 | L2332 to L2343 | special-session INFO | A01 | IST date (a second derivation) | only if today has a special session | log | - | - |
| S21 | L2346 to L2350 | `OrderStateMachine()`; `RateLimiter(app_config.broker_limits, shutdown_event=_shutdown_event)`; `ProductResolver(...)`; `CostCalculator(...)` | A04 | config | - | four objects; the limiter watches `_shutdown_event` | uncaught (1/2) | - |
| S22 | L2352 to L2375 | live credential pre-load, then `_build_kite_client(app_config)` (L381 to L390) | A01 wiring; A04 | `config_dir/accounts.csv`; env named by the primary row's `api_key_env`; the token file | paper: `kite_client = None` (paper-only) | env `ZERODHA_API_KEY` (L2361) and `ZERODHA_ACCESS_TOKEN` (L2363); `kite_client` | handlers: `FileNotFoundError` → 6 and `KeyError` → 6, both after `store.close()` (L2364 to L2374). INTERPRETATION: a missing or unreadable token file makes `load_token` return None (`scripts/zerodha_login.py` L49 to L57), so L2363 raises `TypeError`: uncaught (2). An accounts.csv problem raises `ConfigMissingError` or `ConfigSchemaError` (`core/account_registry.py` L104 to L108, L110 to L192): uncaught (1); a short row raises `AttributeError` (`core/account_registry.py` L135): uncaught (2). `_build_kite_client` (L2375) is outside the try: uncaught | 6, or 1 or 2 |
| S23 | L2377 | `is_paper = (args.mode == "paper")` | A01 | - | - | bool | - | - |
| S24 | L2383 to L2411 | `ZerodhaAdapter(kite_client, rate_limiter, product_resolver, cost_calculator, state_machine, ..., bus=event_bus, ...)` | A04 | the objects above | live: the paper settings are passed; the comment at L2395 to L2396 says the live adapter ignores them | `broker_adapter` | uncaught (1/2) | - |
| S25 | L2413 to L2423 | `AccountRegistry.load(config_dir/"accounts.csv")` and an INFO line | A01 | `accounts.csv` | in live, reached only after S22 succeeded | `account_registry` | any `Exception` → CRITICAL, `store.close()` | 3 |
| S26 | L2425 to L2430 | `required_startup_secrets(primary_id)` (L219 to L232) | A01 | the primary account id | - | the names `ZERODHA_API_KEY_<account-ID>`, `ZERODHA_API_SECRET_<account-ID>`, `TELEGRAM_BOT_TOKEN`, `WEBHOOK_SECRET` | - | - |
| S27 | L2439 to L2449 | `InstrumentCache.load(config_dir/"instruments.csv")` | A05 | `instruments.csv` (absent from the commit; `.gitignore` names it as generated) | - | `instrument_cache`, or None | any `Exception` → ERROR, continue with None | - |
| S28 | L2451 to L2474 | `run_all_startup_checks(...)` (`utils/startup_checks.py` L1508 to L1692) | A01 | store, kill switch, the time-authority module, adapter, windows, config, scanner maps, `_http_fetch`, `webhook_url=None`, the secret names, `config_dir`, the cache, the DB path, `logs`, `system.logging.min_free_disk_gb` | 16 inner steps (checks catalogue, section 3); the first broker call is the clock check | `report` | most inner checks catch their own exceptions, but the runner has no try of its own (AST); an exception that escapes a check (for example, in `utils/startup_checks.py`, a decoding failure in `check_temp_config_values`, which catches only `OSError`, L1480 to L1487, or a failing `count()` in `check_instrument_cache_size`, L936) is uncaught (1/2) | - |
| S29 | L2476 to L2482 | `--dry-run` | A01 | `args.dry_run` | only with the flag | prints `ok`, blocking failures, warnings | `store.close()` | 0 if ok, else 3 |
| S30 | L2484 to L2502 | abort on any blocking failure | A01 | `report.ok`, `report.blocking_failures` | if `invalid_strategy_configs` is listed: `scan_strategy_errors` (A02) and `_alert_invalid_strategy_configs` (L288 to L357), inside their own try (L2495 to L2500) | CRITICAL log; optional Telegram and sentinel (A14) | `store.close()` | 3 |
| S31 | L2506 | `assert instrument_cache is not None` | A01 | - | - | - | `AssertionError`: uncaught (2). INTERPRETATION: reached when the cache file exists but fails to load, because the aggregate skips the size check for None (`utils/startup_checks.py` L1608); removed under `python -O` | 2 |
| S32 | L2512 to L2516 | paper slippage engine | paper-only | - | - | - | - | - |
| S33 | L2522 | `broker_adapter.set_instrument_cache(instrument_cache)` | A04 | - | - | tick-snapping source (comment L2518 to L2521) | uncaught (1/2) | - |

### 3.3 Account selection, token gate and snapshot (L2524 to L2614)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S34 | L2525 to L2526 | token-path literal; `_access_token = None` | A01 | - | - | - | - | - |
| S35 | L2528 to L2542 | `--interactive`: banner, `_interactive_select_account`, `_interactive_select_mode` (overwrites `args.mode`), `_interactive_confirm`, `_interactive_check_or_login(..., today)` | A01; login A04 | `args.interactive` | interactive only | - | FACT (AST): `today` is bound neither in `_main_locked` nor at module level. INTERPRETATION: `NameError` at L2534: uncaught (2); the helpers' exits 5, 7 and 8 are not reached | 2 |
| S36 | L2543 to L2554 | non-interactive: `selected_account = account_registry.primary()`; live: `is_token_valid(account_id, token_path)` (`scripts/zerodha_login.py` L60 to L77), then `load_token` | A01; A04 | the token file | invalid when the file, account, IST date or token is wrong. INTERPRETATION: in live this is reached only after the clock check in S28 made a broker call with the file's token (`broker/zerodha_adapter.py` L1716 to L1722); a token that the broker rejects ends the boot there with exit 3, so exit 6 here means a token the broker accepted, for example a wrong account id or date in the file (whether Kite rejects a stale token is UNKNOWN from the code) | `selected_account`; `_access_token` | invalid → CRITICAL `Token missing or expired`; no `store.close()` | 6 |
| S37 | L2561 to L2572 | broker pin: `(selected_account.broker or "").strip().lower() != "zerodha"` | A01 | `accounts.csv` `broker` | - | CRITICAL `main.unsupported_broker`; stdout `[FATAL]` | no `store.close()` | 9 |
| S38 | L2575 to L2576 | `os.environ["ZERODHA_ACCESS_TOKEN"] = _access_token` | A01 | - | only if set | env (set a second time in live) | - | - |
| S39 | L2582 to L2585 | `is_paper` recomputed; `effect_telemetry.set_mode(is_paper)` | A01; A15 | - | - | telemetry mode, read by `assert_composition` (L4244) | - | - |
| S40 | L2590 to L2591 | paper capital late bind | paper-only | - | - | - | - | - |
| S41 | L2602 to L2614 | `snapshot_config(store, app_config, snapshot_date, snapshot_ts, account_id, mode, trade_type, logger)` | A02 | config; selected account | - | a `config_snapshots` row (A02) | any `Exception` → ERROR, continue | - |

### 3.4 Phase 0e, construction (L2616 to L3844)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S42 | L2617 to L2642 | `TelegramNotifier(bot_token=os.environ[tg_cfg.bot_token_env], channels, ...)` | A14 | env named by `alerts.telegram.bot_token_env` | - | `notifier` | missing env → `KeyError`: uncaught (2) | - |
| S43 | L2645 to L2653 | `mode_label` again; `kill_switch.set_notifier(notifier, mode)`; `kill_switch.set_adapter(broker_adapter)` | A13 | - | - | late binding of notifier and adapter | uncaught (1/2) | - |
| S44 | L2656 to L2675 | `CONFIG_DIFF` system event; WARN Telegram | A01; A03; A14 | `config_hash_changed` | only when hashes changed | a `system_events` row | insert outside the try: uncaught; send failure → ERROR, continue | - |
| S45 | L2677 to L2716 | leverage map; `_eod_ref = {"eod": None}`; `resolve_bucket_allocation(...)` | A09 | `system.capital.*` | - | `leverage_map`, `_eod_ref`, bucket split | uncaught (1/2) | - |
| S46 | L2718 to L2736 | `FundManager(..., on_daily_loss_breach=_make_daily_loss_cb(kill_switch, notifier, mode, eod_ref=_eod_ref), kill_switch)` | A09; callback A13 | - | - | `fund_manager` | uncaught (1/2) | - |
| S47 | L2749 to L2752 | start of the IST day as ISO text | A01 | `now_ist()` | - | `_start_of_today_iso` (one day floor for S48 and S50) | - | - |
| S48 | L2754 to L2761 | live: `compute_live_seed(broker_adapter, fund_manager, _start_of_today_iso)` (L2074 to L2078), then `fund_manager.initialize(...)` | A04; A09 | `get_margins().net` (a broker call) minus today's realised carryover | paper branch paper-only | in-memory capital; `_startup_capital` | uncaught (1 for a `BrokerError`, else 2) | - |
| S49 | L2768 to L2778 | `check_paper_capital_consistency(...)` | A01 | - | live: returns at once (`utils/startup_checks.py` L989 to L990) | - | `StartupCheckFailed` → `store.close()` (paper only) | 3 |
| S50 | L2814 to L2825 | `fund_manager.rehydrate_from_open_trades(_start_of_today_iso)` | A09 | open trades in the DB | - | capital rebuilt | `CapitalStateInconsistent` → CRITICAL, `store.close()`; other exceptions uncaught | 3 |
| S51 | L2831 to L2837 | paper re-sync | paper-only | - | - | - | - | - |
| S52 | L2839 to L2879 | `PositionSizer(...)`; INFO and a stdout line | A09 | `position_sizing.*` | - | `position_sizer` | uncaught (1/2) | - |
| S53 | L2884 to L2889 | `check_kill_switch_present(kill_switch, is_paper, _log)` | A01 | the object from S8 | live and None → raise | - | `StartupCheckFailed` → `store.close()`. INTERPRETATION: cannot trigger as wired | 3 |
| S54 | L2891 to L2925 | `RiskEngine(..., sector_lookup_fn, kill_switch, ...)` | A09 | - | - | `risk_engine` | uncaught (1/2) | - |
| S55 | L2927 to L2938 | `LiveFeedManager(api_key=os.environ.get(selected_account.api_key_env, ""), access_token=os.environ.get("ZERODHA_ACCESS_TOKEN", ""), on_critical_failure=..., market_windows)` | A05; callback A13 | env | - | `live_feed`, not connected | uncaught (1/2) | - |
| S56 | L2940 to L2961 | `CandleStore(candle_interval_sec=60)`; `ShadowTracker(...)`; `set_instrument_cache` | A05; A11 | - | - | `candle_store`; `shadow_tracker` (subscribes `PositionClosed` and `EodSquareoffComplete` in its constructor) | uncaught (1/2) | - |
| S57 | L2964 to L2971 | `_tick_dispatcher`; `live_feed.register_callback(_tick_dispatcher)` | A01 | ticks | - | tick fan-out to candle store and shadow tracker | no per-tick try | - |
| S58 | L2973 to L2994 | `SmartTgtManager(..., enabled=True, async_modify=True, ...)`; reconnect callback | A11 | - | - | `smart_tgt` (constructor executor and candle-close registration) | uncaught (1/2) | - |
| S59 | L2996 to L3012 | `OrderMonitor(..., on_orphan_callback=_make_orphan_cb, on_critical_failure=_make_api_failure_hard_kill_cb, on_force_close=_make_force_close_cb, ...)` | A04; callbacks A13 | `system.order_monitor`; `system.circuit_breaker` | - | `order_monitor`, not started | uncaught (1/2) | - |
| S60 | L3014 to L3050 | CO and LIMIT protocols; `CncGttPlacer(...)` and `hydrate_from_store()` (L3039); `FullEntryEngine`; `OrderManager(bus=event_bus)` | A10; A11 | - | - | four objects; `OrderManager` subscribes `OrderStatusChanged` | uncaught (1/2) | - |
| S61 | L3055 to L3088 | `MisLearnedBlocklist(path=Path("data_store/mis_blocklist.json"), ...)`; `OrderPlacer(...)` | A12; A10 | - | - | `mis_blocklist`; `order_placer` (subscribes `OrderFilled`, `OrderPartiallyTerminated`, `OrderStatusChanged`) | uncaught (1/2) | - |
| S62 | L3093 to L3101 | `SlippageRecorder(store, event_bus, ...)` | A11 | - | - | two async bus subscriptions; the object is bound to no name | any `Exception` → WARNING, continue | - |
| S63 | L3107 to L3155 | `_market_hours_fn`; `CncGttMonitor`; `OrderReconciler(...)`; `TGTRetryManager` | A11; A12 | - | - | three objects, not started | uncaught (1/2) | - |
| S64 | L3157 to L3162 | `StrategyLoader().load_all_strategies(strategies_dir, force_intraday_only=system.force_intraday_only)` | A02 | strategy YAMLs | - | `strategies` | uncaught (1/2) | - |
| S65 | L3166 to L3228 | strategy-control summary; delivery-lock log; `validate_slippage_overrides(...)` | A07; A10 | - | - | logs only | the summary and the validation: any `Exception` → WARNING, continue | - |
| S66 | L3230 to L3247 | `QualityScorer`, `StepExecutor(market_open=market_windows.market_open)`, `HardGate` | A07 | - | - | three objects (the `StepExecutor` constructor creates an executor) | uncaught (1/2) | - |
| S67 | L3257 to L3279 | `EvidenceRecorder(...)` | A15 | - | - | `evidence_recorder`, or None | any `Exception` → None, ERROR, CRITICAL alert; the alert's own failure is passed silently (L3278 to L3279) | - |
| S68 | L3281 to L3298 | `SecondaryScreener(...)` | A07 | - | - | `screener` | uncaught (1/2) | - |
| S69 | L3300 to L3321 | `EodSquareoff(...)`; `_eod_ref["eod"] = eod` | A12 | - | - | `eod`; the daily-loss callback can now reach it | uncaught (1/2) | - |
| S70 | L3328 to L3337 | `MisSquareoffTiming.build(...)` | A12 | `trading_hours.mis_*` | - | `_mis_timing` | uncaught (1/2) | - |
| S71 | L3343 to L3357 | `MisSquareoffNotifier(...)`; `run_boot_self_test(background=True)` (L3355); `start_polling()` (L3357) | A14 | - | - | two daemon threads started | uncaught (1/2) | - |
| S72 | L3359 to L3380 | `MisAutoSquareoff(...)`; `start_polling()` (L3380) | A12 | - | - | one daemon thread started | uncaught (1/2) | - |
| S73 | L3384 | `eod.set_stale_order_sweep(order_reconciler.sweep_stale_orders)` | A12 | - | - | - | uncaught (1/2) | - |
| S74 | L3388 to L3400 | `TokenMonitor(profile_fn=broker_adapter._kite.profile, on_expiry=<soft_kill "token_expired">, check_interval_sec=1800, ...)` | A04; callback A13 | - | - | `token_monitor`, not started | uncaught (1/2) | - |
| S75 | L3402 to L3415 | `queue.Queue(maxsize=system.signal_queue.capacity)`; `WebhookReceiver(..., secret_token=os.environ.get("WEBHOOK_SECRET"))` | A06 | env | - | `signal_queue`; `webhook_receiver`, whose constructor starts its in-flight sweeper thread | uncaught (1/2) | - |
| S76 | L3421 to L3427 | S&R and structure-exit flags | A01 | `system.sr_detector`, `system.structure_exit` | - | `_v1_on`, `_v2_on`, `_struct_exit_on` | - | - |
| S77 | L3436 to L3443 | Q4(c): `audit_config(app_config.system, strategies=strategies, groups="A")`, keeping code `A4_structure_exit_trailing_sl` | A02 | strategies | only if `_struct_exit_on is True` | - | a finding → CRITICAL, `store.close()` | 3 |
| S78 | L3458 to L3465 | A5: the same audit, keeping code `A5_delivery_without_conditional_allocation` | A02 | strategies | only if `delivery_enabled is True` | - | a finding → CRITICAL, `store.close()` | 3 |
| S79 | L3468 to L3487 | regime, V3-chain and watchlist flags; `_build_market_data_kite(is_paper, kite_client)`; `_make_sr_fetch_fn(_md_kite, rate_limiter)` | A05; A08; A18 | config | built if any S&R or V3 feature is on | `_md_kite` (in live, the same client as the adapter's); `_sr_fetch_fn` | a None handle → WARNING | - |
| S80 | L3490 to L3508 | `build_sr_detector(...)`; `start()` | A08 | - | `_v1_on` | `sr_detector`, thread started | any `Exception` → ERROR, None | - |
| S81 | L3514 to L3540 | regime fetcher and runner; `start()` | A18 | - | `_regime_on` | `market_regime_runner`, thread started | any `Exception` → ERROR, None | - |
| S82 | L3545 to L3572 | `ZoneCache`, `ZoneWarmer`, not started here | A08 | - | `_v2_on or _struct_exit_on` | `_v2_zone_cache`, `zone_warmer` | any `Exception` → ERROR, both None | - |
| S83 | L3574 to L3623 | `SignalProcessor(...)`, including `_build_strategy_governor(...)` (L846 to L862) and `in_flight_release_fn=webhook_receiver.release_in_flight` | A06; A09 | - | - | `signal_processor`, not started | uncaught (1/2) | - |
| S84 | L3631 to L3662 | `PortfolioAllocator(...)`; `signal_processor.set_allocator(...)`; `start()` | A18 | - | allocator mode not "off" | `portfolio_allocator`, thread started | any `Exception` → ERROR, None, `set_allocator(None)` | - |
| S85 | L3672 to L3702 | `V3ChainRunner(...)`; `signal_processor.set_v3_chain(...)`; `start()` | A18 | - | `_v3_chain_on` | `v3_chain_runner`, thread started | any `Exception` → ERROR, None, `set_v3_chain(None)` | - |
| S86 | L3712 to L3763 | PB-01 capture worker and entry stage; `webhook_receiver.set_eod_capture(...)`; both `start()` | A18 | - | `_watchlist_on` | two threads started | any `Exception` → ERROR, both None; `set_eod_capture` is not reset | - |
| S87 | L3769 to L3802 | `RetestMonitor`, `RetestDiverter`; `set_retest_diverter`; `eod.set_retest_monitor`; `rehydrate()`; `zone_warmer.start()`; `retest_monitor.start()` | A08 | - | `_v2_on` and the zone infrastructure built | threads started | any `Exception` → ERROR, `retest_monitor = None`; the setters are not reset | - |
| S88 | L3807 to L3837 | `zone_warmer.start()`; `StructureExitManager(...)`; `start()` | A11; A08 | - | `_struct_exit_on` and the infrastructure built | `structure_exit_manager` | any `Exception` → ERROR, None | - |
| S89 | L3839 to L3844 | `EntryGate(quote_fn=broker_adapter.get_quote, ..., on_release=_make_gate_release_cb(signal_processor))` | A07 | - | - | `entry_gate`, not started | uncaught (1/2) | - |

### 3.5 Phase 0e subscriptions, Phase 0f and Phase 0g (L3846 to L4164)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S90 | L3847 | `event_bus.subscribe(KillSwitchActivated, _log_kill_switch_event)` | A01 | - | - | a synchronous subscription | uncaught (1/2) | - |
| S91 | L3853 to L3859 | `CapitalDriftHandler(config=system.drift_handler, kill_switch, logger)`; `subscribe(CapitalDriftDetected, drift_handler.on_drift)` | A09; A01 | config | - | `drift_handler`; a synchronous subscription | uncaught (1/2) | - |
| S92 | L3866 | `eod.post_wire_init()` | A12 | - | its restart-recovery check may fire (A12) | - | uncaught (1/2) | - |
| S93 | L3880 to L3885 | `recon_actions = order_reconciler.reconcile_once()`; `_startup_reconcile_done = True` (L3881) | A12 | broker and DB state | - | `recon_actions`; the flag, set whatever the result | `reconcile_once` catches every `Exception` itself, logs ERROR and returns an empty list (`orders/order_reconciler.py` L643 to L656) | - |
| S94 | L3890 to L3893 | `order_reconciler.sweep_stale_orders()` | A12 | - | - | - | any `Exception` → ERROR, continue | - |
| S95 | L3894 to L3899 | `kill_switch.is_active("any")` | A13 | the kill state, whatever set it | any kill state active | CRITICAL `Kill switch active after startup reconciliation -- aborting` | `store.close()` | 1 |
| S96 | L3905 to L3918 | `BrokerClockSkewProbe(adapter, time_authority, config=system.clock.probe, logger)`; `effect_telemetry.register_constructed("clock_skew_probe")` | A04; A15 | config | live only | `clock_skew_probe` | uncaught (1/2) | - |
| S97 | L3922 | `candle_store.start()` | A05 | - | - | a timer thread (A05) | uncaught (1/2) | - |
| S98 | L3926 to L3944 | `_persist_candle` registered with `candle_store.register_on_candle_close` | A01; A03 | - | - | callback | its own try: DEBUG log | - |
| S99 | L3946 | `candle_store.set_token_map(instrument_cache.token_map())` | A05 | - | - | - | uncaught (1/2) | - |
| S100 | L3947 | `live_feed.connect()` | A05 | env token | - | feed threads (A05) | uncaught (1/2) | - |
| S101 | L3948 to L3951 | stale paper orders | paper-only | - | - | - | - | - |
| S102 | L3952 | `order_monitor.rehydrate_from_store(store)` | A04 | DB | - | tracked orders | uncaught (1/2) | - |
| S103 | L3955 | `order_placer.rehydrate_fill_map(store)` | A10 | DB | - | the fill map | uncaught (1/2) | - |
| S104 | L3958 | `_install_signal_handlers()` (L1570 to L1579) | A01 | - | - | SIGINT and SIGTERM handlers that set `_shutdown_event` | the SIGINT install is unguarded; for SIGTERM, `OSError` and `ValueError` are passed | - |
| S105 | L3960 to L3964 | `order_monitor.start()`; `order_reconciler.start()`; `clock_skew_probe.start()` when not None; `token_monitor.start()` | A04; A12 | broker and DB state | `order_reconciler.start()` first runs, synchronously, the CNC overnight check (a broker `get_positions`, `orders/order_reconciler.py` L428, L756), `cnc_gtt_monitor.reconcile()` inside a try (L435 to L439) and a second `reconcile_once()` (L442), and then starts its poll thread (L445 to L451); no kill check follows (compare S95) | threads (owners); the effects of the second reconcile (A12) | uncaught (1/2), apart from the reconciler's own catches (`orders/order_reconciler.py` L438, L652 to L654, L757) | - |
| S106 | L3968 to L3971 | `assert _startup_reconcile_done, ...` | A01 | the flag set at L3881 | - | - | INTERPRETATION: cannot fail in this straight-line order; removed under `python -O` | (2) |
| S107 | L3974 to L3977 | `signal_processor.start()`; `entry_gate.start()`; `smart_tgt.start()`; `tgt_retry_manager.start()` | A06; A07; A11 | DB state; quotes | the comment at L3972 to L3973 orders the processor before the gate. `entry_gate.start()` first restores `gate_state` from the database (`screening/entry_gate.py` L155 to L160); `smart_tgt.start()` restores `smart_tgt_state` and makes one startup quote check per restored row (`orders/smart_tgt_manager.py` L170 to L204), which catches its own failures (`orders/smart_tgt_manager.py` L854 to L867) | threads and executors (owners); restored in-memory state | uncaught (1/2) | - |
| S108 | L3979 to L4000 | thread "webhook-server": `waitress.serve(webhook_receiver.app, host=wh_cfg.bind_host, port=wh_cfg.bind_port, threads=8, connection_limit=100)`, `daemon=True` | A06; third-party | `system.webhook` (file values: an all-interfaces bind address, port 5000; `config/system_config.yaml` L327 to L335) | - | a daemon server thread | a failure inside the server thread does not reach the main thread | - |
| S109 | L4003 to L4054 | `time.sleep(2)`; `check_webhook_endpoint(<loopback>:<bind_port>/health, _http_fetch, _log)`; unreachable → CRITICAL and `write_critical_sentinel(...)` | A01; A14 | - | 2xx or 401 counts as reachable (`utils/startup_checks.py` L807 to L809) | a CRITICAL sentinel (A14) | the boot continues (degrade); the sentinel write has its own try | - |
| S110 | L4060 to L4082 | `_daemon_liveness()`; `start_healthcheck_server(state_store=store, ..., port=8080, metrics_provider, tgt_retry_provider, daemon_liveness_provider)` | A15 | - | - | daemon thread "healthcheck-server" on the loopback host (`scripts/healthcheck_server.py` L297 to L326); the returned handle is discarded | uncaught (1/2) | - |
| S111 | L4087 to L4091 | `run_on_demand_if_missed()` | A20 | - | runs only past-due pre-flight phases (A20) | possible detached child processes | any `Exception` → WARNING | - |
| S112 | L4094 to L4100 | thread "eod-scheduler": `eod.start_polling(poll_interval_sec=system.eod_squareoff.poll_interval_sec)`, `daemon=True` | A12 | config (file value 5) | - | launches the daemon "eod_squareoff_poll" (`orders/eod_squareoff.py` L290 to L312) | - | - |
| S113 | L4103 to L4110 | `_start_eod_pre_alert_thread(store, notifier, mode, log, market_windows, shutdown_event)` | A01 | - | - | thread "eod-pre-alert" | - | - |
| S114 | L4113 to L4121 | `_start_market_open_margin_sync_thread(broker_adapter, fund_manager, notifier, mode, log, shutdown_event, market_windows)` | A01 | - | - | thread "market-open-margin-sync" | - | - |
| S115 | L4129 to L4161 | `_start_eod_self_exit_thread(..., window_end=_service_window_end, flatten_in_progress_fn=kill_switch.is_flatten_in_progress, strategy_intent_fn=<lambda>, squareoff_time=...)` | A01 | S3; the kill switch; strategies | armed unless `--interactive`, `--resume` or `TS_IGNORE_MARKET_WINDOW=1` (L4129 to L4133); otherwise INFO "not armed" | thread "eod-self-exit" | - | - |
| S116 | L4164 | `config_validator.validate_all(strict=False)` | A02 | - | - | - | uncaught (1/2) | - |

### 3.6 Phase 0h and the runtime wait (L4166 to L4249)

| # | Lines | Step | Owner | Inputs | Branch or guard | State created | Failure behaviour | Exit |
|---|---|---|---|---|---|---|---|---|
| S117 | L4167 to L4173 | `store.insert_system_event(event_type="STARTUP", scenario=scenario.value, details={"mode", "version"})` | A03 | - | - | a `system_events` row | uncaught (1/2) | - |
| S118 | L4174 to L4180 | `_write_session(...)` again | A01; A03 | the same config-hash expression as S17 | - | the session row rewritten, `session_start` reset | uncaught (1/2) | - |
| S119 | L4181 to L4203 | INFO Telegram "System Active": account id, startup capital, market state from `market_windows.is_market_open(...)`, HH:MM IST | A14 | - | - | an alert | any `Exception` → ERROR | - |
| S120 | L4205 | INFO "All subsystems started -- entering runtime loop" | A01 | - | - | log | - | - |
| S121 | L4208 to L4215 | interactive welcome banner and console lines | A01 | - | interactive only | stdout | INTERPRETATION: reads `today` (L4209); not reached, see S35 | - |
| S122 | L4223 to L4242 | `effect_telemetry.register_constructed(...)` for 15 names, plus `instrument_cache` when not None | A15 | - | - | the telemetry registry | uncaught (1/2) | - |
| S123 | L4243 to L4246 | `effect_telemetry.assert_composition(notifier=notifier, logger=_log)`; `except EffectCompositionError: raise` | A15 | `config/expected_managers.yaml` | live: a mismatch logs CRITICAL, alerts and continues (`core/effect_telemetry.py` L204 to L216); paper or an unset mode raises | - | a registry read failure (`core/effect_telemetry.py` L129 to L142) is uncaught (2) | - |
| S124 | L4249 | `_shutdown_event.wait()` | A01 | - | no timeout; returns when the event is set (L1525 or L1573) | - | - | - |

What follows the wait (L4252 to L4278) is in the workers and shutdown file, sections 3 to 5.

## 4. Objects constructed by startup

"Started" gives the line of the start call, or "ctor" where the constructor itself starts a thread, creates an executor or subscribes to the bus. Every long-lived object except those marked "not passed" is also passed to `_shutdown(...)` at L4252 to L4277.

| Variable | Class or function (module) | Owner | Line | Condition | Main consumers (dependency injection) | Started |
|---|---|---|---|---|---|---|
| `app_config` | `load_all` (`core/config_loader.py`) | A02 | L2198 | always | nearly every constructor | - |
| `store` | `StateStore` (`core/state_store.py`) | A03 | L2233 | always | kill switch, checks, session writes, snapshot and most subsystems | opened in the ctor |
| `event_bus` | `EventBus` (`core/events.py`) | A01 | L2238 | always | kill switch, adapter, fund manager, shadow tracker, order monitor, order manager, order placer, slippage recorder, GTT monitor, reconciler, EOD, signal processor | not passed to `_shutdown` |
| `kill_switch` | `KillSwitch` (`capital/kill_switch.py`) | A13 | L2243 | always | time-authority callback, detection, checks, fund manager, risk engine, callbacks, order placer, monitors, reconciler, EOD, token monitor, webhook, signal processor | state loaded in the ctor |
| `market_windows` | `MarketWindows` (`core/market_windows.py`) | A01 | L2320 | always | checks, live feed, shadow tracker, order placer, `_market_hours_fn`, step executor, EOD, MIS auto-square-off, webhook, S&R, regime, signal processor, PB-01, the helper threads | - |
| `state_machine`, `rate_limiter`, `product_resolver`, `cost_calculator` | `broker/` classes | A04 | L2346 to L2350 | always | adapter, order monitor, EOD, smart TGT, order placer, fetch closure | not passed to `_shutdown` |
| `kite_client` | `KiteConnect` via `_build_kite_client` | A04 | L2375 | live | adapter; the market-data handle | - |
| `broker_adapter` | `ZerodhaAdapter` (`broker/zerodha_adapter.py`) | A04 | L2383 | always | checks, kill switch, live seed, every order component, token monitor, entry gate | not passed to `_shutdown` |
| `account_registry` | `AccountRegistry` (`core/account_registry.py`) | A01 | L2414 | always | `primary()` at L2425 and L2545 | - |
| `instrument_cache` | `InstrumentCache.load` (`core/instrument_cache.py`) | A05 | L2441 | None on a load failure | checks, adapter, sizer, risk engine, shadow tracker, smart TGT, order placer, fetchers, signal processor, candle token map | - |
| `report` | `StartupReport` (`utils/startup_checks.py`) | A01 | L2451 | always | read only at L2476 to L2502 | - |
| `selected_account` | `AccountRow` | A01 | L2536 or L2545 | always | token gate, broker pin, snapshot, live feed, "System Active" | - |
| `notifier` | `TelegramNotifier` (`alerts/telegram_notifier.py`) | A14 | L2628 | always | kill switch, callbacks, monitors, EOD, MIS, signal processor, governor, `_shutdown` | - |
| `fund_manager` | `FundManager` (`capital/fund_manager.py`) | A09 | L2718 | always | sizer, risk engine, order placer, GTT monitor, reconciler, EOD, signal processor, allocator, margin-sync thread | `initialize` L2761; rehydrate L2815; not passed to `_shutdown` |
| `position_sizer`, `risk_engine` | `PositionSizer`, `RiskEngine` (`capital/`) | A09 | L2840, L2896 | always | signal processor; allocator (`_max_open`) | - |
| `live_feed` | `LiveFeedManager` (`data/live_feed.py`) | A05 | L2927 | always | shadow tracker, order placer, tick and reconnect callbacks | `connect()` L3947 |
| `candle_store` | `CandleStore` (`data/candle_store.py`) | A05 | L2940 | always | tick dispatcher, smart TGT, structure exit | `start()` L3922 |
| `shadow_tracker` | `ShadowTracker` (`orders/shadow_tracker.py`) | A11 | L2946 | always | tick dispatcher, signal processor | ctor subscribes; not passed to `_shutdown` |
| `smart_tgt` | `SmartTgtManager` (`orders/smart_tgt_manager.py`) | A11 | L2973 | always | reconnect callback, order placer | ctor executor; `start()` L3976 |
| `order_monitor` | `OrderMonitor` (`broker/order_monitor.py`) | A04 | L2998 | always | order placer, EOD, structure exit | `start()` L3960 |
| `co_protocol`, `limit_protocol`, `cnc_gtt_placer`, `full_engine`, `order_manager` | `orders/` classes | A10; A11 | L3014 to L3046 | always | entry engine and order placer | GTT hydrate L3039; ctor subscription (order manager) |
| `mis_blocklist`, `order_placer` | `MisLearnedBlocklist`, `OrderPlacer` | A12; A10 | L3055, L3061 | always | order placer, screener; TGT retry, signal processor | ctor subscriptions (order placer); not passed to `_shutdown` |
| (unbound) | `SlippageRecorder` (`orders/slippage_recorder.py`) | A11 | L3095 | inside a try | the bus only | ctor: two async subscriptions |
| `cnc_gtt_monitor`, `order_reconciler`, `tgt_retry_manager` | `orders/` classes | A11; A12 | L3109, L3124, L3144 | always | reconciler; EOD sweep | reconciler `start()` L3961; TGT retry `start()` L3977 |
| `strategies` | `StrategyLoader().load_all_strategies` | A02 | L3159 | always | audits, signal processor, self-exit intent lambda | - |
| `scorer`, `step_executor`, `hard_gate`, `screener` | `screening/` classes | A07 | L3230 to L3281 | always | screener, signal processor | step executor ctor executor; not passed to `_shutdown` |
| `evidence_recorder` | `EvidenceRecorder` (`core/evidence_contract.py`) | A15 | L3259 | None on failure | screener, signal processor | - |
| `eod` | `EodSquareoff` (`orders/eod_squareoff.py`) | A12 | L3300 | always | `_eod_ref`, sweep, retest monitor, liveness | thread "eod-scheduler" L4094 to L4100; not passed to `_shutdown` |
| `_mis_timing`, `mis_notifier`, `mis_autosq` | `MisSquareoffTiming`, `MisSquareoffNotifier`, `MisAutoSquareoff` | A12; A14 | L3329, L3343, L3359 | always | each other | started at L3355, L3357, L3380; not passed to `_shutdown` |
| `token_monitor` | `TokenMonitor` (`broker/token_monitor.py`) | A04 | L3388 | always | - | `start()` L3964 |
| `signal_queue`, `webhook_receiver` | `queue.Queue`; `WebhookReceiver` (`signals/webhook_receiver.py`) | A06 | L3402, L3407 | always | signal processor | ctor sweeper thread; server thread L4000 |
| `_md_kite`, `_sr_fetch_fn` | `_build_market_data_kite`, `_make_sr_fetch_fn` | A05 | L3481, L3487 | any S&R or V3 flag | S&R detector and the fetchers | - |
| `sr_detector`, `market_regime_runner`, `_v2_zone_cache`, `zone_warmer` | `sr_detector/` and `regime/` classes | A08; A18 | L3494, L3531, L3557, L3564 | their flags | signal processor; V3 runners | started at L3504, L3536, L3796 or L3816 |
| `signal_processor` | `SignalProcessor` (`signals/signal_processor.py`) | A06 | L3575 | always | allocator, setters, gate-release callback | `start()` L3974 |
| `portfolio_allocator`, `v3_chain_runner`, `pb01_capture_worker`, `pb01_entry_stage` | `allocation/` and `v3_chain/` classes | A18 | L3636, L3684, L3734, L3743 | their flags | signal processor; webhook EOD capture | started at L3651, L3694, L3748, L3749 |
| `retest_monitor`, `_retest_diverter`, `structure_exit_manager` | `screening/retest_monitor.py`; `orders/structure_exit_manager.py` | A08; A11 | L3784, L3789, L3817 | their flags | signal processor; EOD | started at L3797, L3832 |
| `entry_gate` | `EntryGate` (`screening/entry_gate.py`) | A07 | L3839 | always | - | `start()` L3975 |
| `drift_handler` | `CapitalDriftHandler` (`capital/drift_handler.py`) | A09 | L3853 | always | the bus (L3858) | not passed to `_shutdown` |
| `clock_skew_probe` | `BrokerClockSkewProbe` (`broker/clock_skew_probe.py`) | A04 | L3907 | live | - | `start()` L3963 |
| `webhook_thread`, `eod_thread` | `threading.Thread` | A01 | L3988, L4094 | always | - | L4000, L4100; not passed to `_shutdown` |

## 5. Key flows (Document 08, section 4)

- **Startup scenario.** FACT: the session row and the kill-switch state (persisted; A03 and A13) → `detect_startup_scenario` (L2268) → `scenario` → logs, a `CRASH_DETECTED` event (L2277 to L2282), exit 4 or `--resume` (L2283 to L2292) → the STARTUP event's `scenario` field (L4171). No other read of `scenario` exists in `main.py` (grep). A second, independent detection runs inside the aggregate (`utils/startup_checks.py` L1561), after the session row was rewritten at L2308.
- **Live credentials.** FACT: the `api_key_env` column of `accounts.csv` → that environment variable → `ZERODHA_API_KEY` (L2361) → `KiteConnect(api_key=...)` (L386). The token file → `ZERODHA_ACCESS_TOKEN` (L2363) → `kite.set_access_token(...)` (L387) → the adapter's client (L2384) → the first broker call, the clock check inside the aggregate (`broker/zerodha_adapter.py` L1709 to L1728) → the live seed (L2758) → `TokenMonitor.profile_fn` (L3389) → the market-data handle (L3481). The token is re-read at L2547 and L2553 and set in the environment again at L2576, then read by the live feed (L2929).
- **Configuration hashes.** FACT: `app_config.file_hashes` (A02) → `check_config_hash` against `session.last_config_hash` (L2295) → `config_hash_changed` → a `CONFIG_DIFF` event and a WARN alert (L2656 to L2675). The same hashes are written to the session row (L2312, L4178), to the `config_snapshots` row (L2603, A02) and to the evidence recorder (L3261).
- **Startup capital.** FACT: `get_margins().net` minus today's realised carryover (L2758 to L2760) → `fund_manager.initialize` (L2761) → `rehydrate_from_open_trades(day floor)` (L2815) → the in-memory capital that the sizer, risk engine, order placer, reconciler, EOD and signal processor read (A09) → the "System Active" message (L4196).
- **Migration permission.** FACT: the configured open and close times and the IST clock (L2228 to L2232) → `market_open` → the StateStore schema guard (A03) → migrate, or raise `MigrationNotPermitted` → exit 1.
