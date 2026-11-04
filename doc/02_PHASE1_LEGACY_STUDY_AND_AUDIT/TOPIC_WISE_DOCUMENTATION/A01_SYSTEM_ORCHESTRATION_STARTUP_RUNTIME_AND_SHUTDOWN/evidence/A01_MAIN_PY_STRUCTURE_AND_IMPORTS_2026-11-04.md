# A01 evidence: main.py structure, phase markers and imports

**Status:** DRAFT — evidence for the A01 STUDY, for ChatGPT's review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04.
**Purpose and scope:** The top-level definitions of `main.py` with their line ranges and roles, the section and phase markers inside `_main_locked`, and every import statement with its line, enclosing function and owner topic. It supports the STUDY, sections 3, 5 and 13 (Q1 and Q5 to Q8 of ChatGPT's A01 direction).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on 04-Nov-2026; nothing was run.

Method: the definitions and the import statements were listed by parsing the source text of `main.py` at the baseline with Python's `ast` module, in a script kept outside the clone and run with `python3 -I`; the markers were read with `git show`. Owner topics follow the Master System Investigation Index (entry A01; rules 1 and 8; entry A13 for the `main.py` failure callbacks; entry A05 for the historical-data call sites in `main.py`). Every row is FACT for the lines it cites. Where the Role column names a purpose, it is INTERPRETATION of the code at those lines.

## 1. Top-level definitions

`main.py` has 4,293 lines at the baseline (STUDY, section 3). The module-level import statements are at L22 to L106 (section 3 below).

| Lines | Kind | Name | Role, or owner topic | Notes |
|---|---|---|---|---|
| L108 | assignment | `VERSION` | A01: version string `"2.0.0"` | read at L649, L1800, L2095, L2180, L4172 |
| L113 | assignment | `_log` | A01: the module logger, `logging.getLogger("main")`; logging set-up is A15's | rebound in `main()` at L2179 (`global` at L2086) |
| L116 | assignment | `_shutdown_event` | A01: the runtime stop event, a `threading.Event` | set at L1525, L1573 and L1629; awaited at L4249; never cleared |
| L119 | assignment | `_broker_auth_failed` | A13: the FIX-062 failure flag; A01 holds the global | set at L171; read at L1678; never reset |
| L134 | assignment | `_TOKEN_PATH` | A04 boundary: the broker token file, a path relative to the working directory | the same literal is repeated at L410, L495, L2362 and L2525 |
| L135 | assignment | `_TOKEN_INVALID_PATH` | A04 boundary | `_TOKEN_PATH.with_suffix(".invalid")` |
| L138 to L165 | function | `_invalidate_token` | A13 (failure path; the token file is A04's) | called only at L1679 |
| L168 to L172 | function | `_mark_auth_failed` | A13 | called only at L667 |
| L179 to L212 | function | `_parse_args` | A01: the CLI parser | called at L2090 |
| L219 to L232 | function | `required_startup_secrets` | A01: names of the environment variables the startup checks require | called at L2430 |
| L235 to L261 | function | `_http_fetch` | A01: the HTTP fetcher used by the startup checks | passed at L2460; used at L4005 |
| L264 to L285 | function | `_send_holiday_notification` | A01 holiday guard; a direct Telegram send (A14 boundary) | called at L2144 |
| L288 to L357 | function | `_alert_invalid_strategy_configs` | A01 abort path; alert delivery A14; strategy scan A02 | called at L2498 |
| L360 to L378 | function | `_init_time_authority` | A01: time-authority configuration; its callback calls the A13 kill switch | called at L2254 |
| L381 to L390 | function | `_build_kite_client` | A01 wiring of the A04 broker client | called at L2375, live only |
| L393 to L418 | function | `_build_market_data_kite` | A05 (historical-data call site); its paper branch is out of scope | called at L3481 |
| L421 to L438 | function | `_make_sr_fetch_fn` | A05 (historical-data call site); consumers A08 and A18 | called at L3487 |
| L441 to L443 | function | `_load_holidays` | A01: holidays for `MarketWindows` (schema A02) | called at L2317 |
| L446 to L470 | function | `_load_special_sessions` | A01: special sessions for `MarketWindows` (schema A02) | called at L2318 |
| L473 to L610 | function | `_make_paper_quote_provider` | paper-only, out of scope | called at L2394 only when paper |
| L613 to L616 | function | `_parse_hhmm` | A01 | called at L465 to L467, L2211, L2321 to L2326 and L4153 to L4155 |
| L619 to L633 | function | `_write_session` | A01 startup marker; the `session` table is A03's | called at L2308 and L4174 |
| L636 to L650 | function | `_print_status` | A01: `--status` | called at L2300 |
| L657 to L685 | function | `_make_critical_failure_cb` | A13 (failure callback) | wired at L2930 to L2932 |
| L688 to L724 | function | `_make_force_close_cb` | A13 | wired at L3010 |
| L727 to L752 | function | `_make_api_failure_hard_kill_cb` | A13 | wired at L3006 |
| L756 to L817 | function | `_make_daily_loss_cb` | A13 | wired at L2729 to L2734 |
| L820 to L843 | function | `_make_orphan_cb` | A13 | wired at L3005 |
| L846 to L862 | function | `_build_strategy_governor` | A01 wiring; the governor is A09's | called at L3618 |
| L865 to L867 | assignment | `_gate_release_pool` | A01: a module-level `ThreadPoolExecutor(max_workers=2, thread_name_prefix="gate-release")`, created when `main.py` is imported | submitted to at L887 |
| L870 to L893 | function | `_make_gate_release_cb` | A01 wiring callback, from the A07 entry gate to the A06 signal processor | wired at L3843 |
| L900 to L928 | function | `_fire_eod_pre_alert` | A01 helper-thread body; the alert is A14's | called at L966 |
| L931 to L970 | function | `_start_eod_pre_alert_thread` | A01 | called at L4103 |
| L973 to L1039 | function | `_start_market_open_margin_sync_thread` | A01; the capital re-sync is A09's | called at L4113 |
| L1064 | assignment | `_ACTIVE_FLATTEN_IN_PROGRESS` | A01 (EOD self-exit gate), value -2 | |
| L1075 | assignment | `_FLATTEN_DRAIN_GRACE_SEC` | A01 (shutdown), value 15.0 | default of `_shutdown(flatten_drain_timeout_sec=...)` at L1624 |
| L1115 to L1118 | assignments | `_PIPELINE_INTRADAY`, `_PIPELINE_DELIVERY`, `_IDENTITY_CONFLICT`, `_IDENTITY_UNRESOLVED` | A01 (EOD self-exit gate) | strings |
| L1121 to L1148 | function | `_resolve_position_pipeline` | A01 (EOD self-exit gate) | lazy import of `core.constants` at L1131 |
| L1161 | assignment | `_BROKER_PROTECTED_PRODUCTS` | A01, `frozenset({"CNC"})` | |
| L1164 to L1179 | function | `_position_requires_service` | A01 | |
| L1182 to L1227 | function | `_classify_active_positions` | A01 | |
| L1230 to L1326 | function | `_eod_self_exit_due` | A01 | |
| L1329 to L1563 | function | `_start_eod_self_exit_thread` | A01 | called at L4135 |
| L1570 to L1579 | function | `_install_signal_handlers` | A01 | called at L3958 |
| L1586 to L1592 | function | `_log_kill_switch_event` | A01: a bus subscriber that only logs | subscribed at L3847 |
| L1599 to L1831 | function | `_shutdown` | A01 | called at L4252 to L4277 |
| L1838 to L1867 | function | `_interactive_select_account` | A01 (interactive path) | called at L2536 |
| L1870 to L1910 | function | `_interactive_check_or_login` | A01 (interactive path); the login flow is A04's | called at L2540 to L2542 |
| L1913 to L1925 | function | `_interactive_select_mode` | A01 (interactive path) | called at L2538 |
| L1928 to L1946 | function | `_interactive_confirm` | A01 (interactive path) | called at L2539 |
| L1949 to L1965 | function | `_print_welcome_banner` | A01 (interactive path) | called at L4209 |
| L2000 | assignment | `SERVICE_WINDOW_START` | A01, 08:00 | |
| L2001 | assignment | `SERVICE_START_CUTOFF` | A01, `= SERVICE_WINDOW_END_MAX`, which is 18:15 (`core/config_loader.py` L83; A02) | |
| L2004 to L2015 | function | `_within_service_window` | A01 | called at L2162 |
| L2018 to L2038 | function | `_config_error_detail` | A01: detail text of an A02 configuration exception | called at L2200 |
| L2041 to L2052 | function | `_service_window_banner` | A01 | called at L2212 to L2216 |
| L2074 to L2078 | function | `compute_live_seed` | A01 wiring of A04 margins and the A09 carryover | called at L2758 |
| L2085 to L2190 | function | `main` | A01: entry, guards and instance lock | called at L4287 |
| L2193 to L4278 | function | `_main_locked` | A01: startup, wiring, runtime wait and the shutdown call | called only at L2188 |
| L4285 to L4293 | if | `__name__ == "__main__"` | A01: the entry guard | |

Module-level comment banners, for orientation: `CLI (MAIN2)` L176; `Helpers` L216; `Callbacks (MAIN18)` L654; `EOD pre-alert at 14:45 (FIX-130 Item 7)` L897; the FIX-189 EOD self-exit block comment L1043 to L1112; `Signal handlers (MAIN13)` L1567; `Event-bus log handlers (MAIN9)` L1583; `Shutdown (MAIN15)` L1596; `Interactive startup helpers (SU7-SU13)` L1835; `Entry point (MAIN3)` L4282.

- FACT: the label MAIN13 heads both the signal-handler section (L1567) and the runtime-loop marker inside `_main_locked` (L4248).
- INTERPRETATION: the block comment at L1052 to L1055 says the self-exit "NEVER exits while any position has live exposure" and names `count_active_positions()`. The gate that L1078 to L1112 describes, and that L1270 to L1326 implement, counts only positions that require the service; `count_active_positions()` is its fallback (L1322 to L1326). The earlier comment describes the older, product-blind rule.

## 2. Section and phase markers inside `main()` and `_main_locked`

A marker covers its line up to the line before the next marker. The marker text is quoted from the code.

| Line | Marker text | Function | What follows (summary) |
|---|---|---|---|
| L2088 | `Phase 0a: Logger setup (MAIN4)` | `main` | argument parsing and `--version` (L2089 to L2096); logging is set up only at L2178 |
| L2098 | `Holiday guard (SU6) -- BEFORE setup_logging` | `main` | the holiday and weekend guard (L2099 to L2152) |
| L2154 | `FIX-189 (P1-A): service-window guard` | `main` | the START window guard (L2157 to L2176) |
| L2182 | `Single-instance lock` | `main` | lock, then `_main_locked` inside try/finally (L2183 to L2190) |
| L2196 | `Phase 0b: Config load (MAIN5)` | `_main_locked` | `load_all` (L2197 to L2202) |
| L2204 | `CV1: Register all config values for usage tracking` | `_main_locked` | L2205 |
| L2207 | `Service window (25-Jul-2026)` | `_main_locked` | stop time parsed and logged (L2211 to L2216) |
| L2218 | `Phase 0c: StateStore + EventBus + KillSwitch + TimeAuthority (MAIN6)` | `_main_locked` | market-open test, store, bus, kill switch, time authority, auto-clears, scenario (L2226 to L2292) |
| L2294 | `CL4 config-hash diff check (MAIN6)` | `_main_locked` | L2295 to L2296 |
| L2298 | `--status mode (MAIN16)` | `_main_locked` | L2299 to L2302 |
| L2304 | `MED #10: Write session row early` | `_main_locked` | L2308 to L2314 |
| L2316 | `Phase 0d: Startup checks (MAIN7)` | `_main_locked` | market windows, broker stack, registry, secrets, instrument cache, aggregate checks, `--dry-run`, abort (L2317 to L2522) |
| L2524 | `Account selection + token handling (SU4, SU8-SU14)` | `_main_locked` | L2525 to L2591 |
| L2593 | `W0: config snapshot` | `_main_locked` | L2602 to L2614 |
| L2616 | `Phase 0e: Construct subsystems (MAIN8)` | `_main_locked` | every subsystem constructed (L2617 to L3844) |
| L3248 | `Batch 1: the forward evidence contract` | `_main_locked` | `EvidenceRecorder` (L3257 to L3279) |
| L3323 | `MIS AUTO-SQUAREOFF (28-Aug-2026)` | `_main_locked` | `MisSquareoffTiming.build` (L3328 to L3337) |
| L3338 | `F / D-1b — human-facing delivery for the orchestrator's CRITICALs` | `_main_locked` | MIS notifier and auto-square-off, both started (L3343 to L3380) |
| L3417 | `SNR-DETECTOR-V1 + V2` | `_main_locked` | feature flags (L3421 to L3427) |
| L3428 | `Q4(c) capital-safety construction guard` | `_main_locked` | L3436 to L3443 (exit 3) |
| L3444 | `SLICE2.5 #16a (27-Jul-2026)` | `_main_locked` | the A5 guard (L3458 to L3465, exit 3) |
| L3466, L3470, L3474 | V3 03.02, V3 Step 10, V3 Step 10b flag comments | `_main_locked` | flags and the shared fetch closure (L3468 to L3487) |
| L3489 | `SNR-DETECTOR-V1 shadow observer` | `_main_locked` | L3490 to L3508 |
| L3510 | `V3 03.02: Market Regime shadow runner` | `_main_locked` | L3514 to L3540 |
| L3542 | `SNR-V2 Phase A: ZoneCache + ZoneWarmer` | `_main_locked` | L3545 to L3572 |
| L3625 | `V3 03.05 Portfolio Allocator` | `_main_locked` | L3631 to L3662 |
| L3664 | `V3 Step 10 decision chain` | `_main_locked` | L3672 to L3702 |
| L3704 | `V3 Step 10b — PB-01 OVERNIGHT WATCHLIST` | `_main_locked` | L3712 to L3763 |
| L3765 | `SNR-V2 Phase A: RetestMonitor + Diverter` | `_main_locked` | L3769 to L3802 |
| L3804 | `SNR-V2 Phase B: StructureExitManager` | `_main_locked` | L3807 to L3844 (the `EntryGate` is built at L3839 to L3844) |
| L3846 | `Phase 0e: Event bus subscriptions (MAIN9)` | `_main_locked` | two subscriptions and `eod.post_wire_init()` (L3847 to L3866) |
| L3868 | `Phase 0f: Startup reconciliation (MAIN10, RC14)` | `_main_locked` | L3880 to L3918 |
| L3920 | `Phase 0g: Start subsystems (MAIN11)` | `_main_locked` | starts, webhook server, health server, helper threads (L3922 to L4164) |
| L4002 | `Post-start webhook self-check (P17, MAIN11)` | `_main_locked` | L4003 to L4054 |
| L4093 | `EOD scheduler daemon thread (MAIN14)` | `_main_locked` | L4094 to L4100 |
| L4166 | `Phase 0h: Mark startup complete (MAIN12)` | `_main_locked` | L4167 to L4215 |
| L4217 | `effect-telemetry (ledger #1, B2)` | `_main_locked` | L4223 to L4246 |
| L4248 | `Runtime loop (MAIN13)` | `_main_locked` | L4249 |
| L4251 | `Shutdown (MAIN15)` | `_main_locked` | L4252 to L4278 |

- FACT: the phase label "Phase 0e" is used twice, at L2616 (MAIN8, construction) and at L3846 (MAIN9, bus subscriptions).
- FACT: there are no markers named Phase 0i or later; the runtime and shutdown markers carry no phase letter (L4248, L4251).
- INTERPRETATION: the label "Phase 0a: Logger setup" (L2088) heads argument parsing; logging is set up at L2178, after the holiday and window guards.

## 3. Import statements

Count (AST): 137 import statements, 74 at module level and 63 inside functions. Statements that span several lines are given as a range. "Owner" is the topic that owns the imported module under the index; the standard library and third-party packages are named as such (third-party dependency declarations are A17's).

### 3.1 Module-level imports (run when `main.py` is imported)

| Lines | Module | Names | Owner |
|---|---|---|---|
| L22 | `__future__` | annotations | standard library |
| L24 | `argparse` | (module) | standard library |
| L25 | `concurrent.futures` | (module) | standard library |
| L26 | `json` | (module) | standard library |
| L27 | `logging` | (module) | standard library |
| L28 | `os` | (module) | standard library |
| L29 | `queue` | (module) | standard library |
| L30 | `signal` | (module) | standard library |
| L31 | `sys` | (module) | standard library |
| L32 | `threading` | (module) | standard library |
| L33 | `time` | (module) | standard library |
| L34 | `urllib.error` | (module) | standard library |
| L35 | `urllib.request` | (module) | standard library |
| L36 | `datetime` | date, datetime, time as _time | standard library |
| L37 | `pathlib` | Path | standard library |
| L38 | `typing` | Callable, Optional | standard library |
| L40 | `core.time_authority` | (module, as time_authority) | A01 |
| L41 | `alerts.delivery` | send_alert_recorded | A14 |
| L42 | `alerts.telegram_notifier` | TelegramNotifier | A14 |
| L43 | `broker.clock_skew_probe` | BrokerClockSkewProbe | A04 |
| L44 | `broker.token_monitor` | TokenMonitor | A04 |
| L45 | `broker.cost_calculator` | CostCalculator | A04 |
| L46 | `broker.order_monitor` | OrderMonitor | A04 |
| L47 | `broker.order_state_machine` | OrderStateMachine | A04 |
| L48 | `broker.product_resolver` | ProductResolver | A04 |
| L49 | `broker.rate_limiter` | RateLimiter | A04 |
| L50 | `broker.zerodha_adapter` | ZerodhaAdapter | A04 |
| L51 | `capital.drift_handler` | CapitalDriftHandler | A09 |
| L52 | `capital.fund_manager` | FundManager, resolve_bucket_allocation | A09 |
| L53 | `capital.kill_switch` | KillSwitch | A13 |
| L54 | `capital.position_sizer` | PositionSizer | A09 |
| L55 | `capital.risk_engine` | RiskEngine | A09 |
| L56 | `core.account_registry` | AccountRegistry | A01 |
| L57 | `core.config_loader` | SERVICE_WINDOW_END_MAX, load_all | A02 |
| L58 | `core.config_auditor` | audit as audit_config | A02 |
| L59 | `core.config_snapshotter` | snapshot_config | A02 |
| L60 | `core.config_validator` | config_validator | A02 |
| L61 | `core` | effect_telemetry | A15 |
| L62 | `core.events` | EventBus, CapitalDriftDetected, KillSwitchActivated | A01 |
| L63 | `core.exceptions` | CapitalStateInconsistent, TradingSystemError | A01 |
| L64 | `core.instrument_cache` | InstrumentCache | A05 |
| L65 | `core.logger` | get_logger, setup_logging | A15 |
| L66 | `core.market_windows` | MarketWindows | A01 |
| L67 | `core.mis_blocklist` | MisLearnedBlocklist | A12 |
| L68 | `core.state_store` | StateStore | A03 |
| L69 | `data.candle_store` | CandleStore | A05 |
| L70 | `data.live_feed` | LiveFeedManager | A05 |
| L71 | `orders.eod_squareoff` | EodSquareoff | A12 |
| L72 | `orders.mis_autosquareoff` | MisAutoSquareoff | A12 |
| L73 | `core.mis_squareoff_timing` | MisSquareoffTiming | A12 |
| L74 | `alerts.mis_squareoff_notifier` | MisSquareoffNotifier | A14 |
| L75 | `orders.shadow_tracker` | ShadowTracker | A11 |
| L76 | `orders.cnc_gtt` | CncGttPlacer | A11 |
| L77 | `orders.cnc_gtt_monitor` | CncGttMonitor | A11 |
| L78 | `orders.full_entry_engine` | FullEntryEngine | A10 |
| L79 | `orders.order_manager` | OrderManager | A10 |
| L80 | `orders.order_placer` | OrderPlacer | A10 |
| L81 | `orders.order_protocol_co` | CoPlusTgtProtocol | A10 |
| L82 | `orders.order_protocol_limit` | LimitTripleProtocol | A10 |
| L83 | `orders.order_reconciler` | OrderReconciler | A12 |
| L84 | `orders.tgt_retry_manager` | TGTRetryManager | A11 |
| L85 | `orders.smart_tgt_manager` | SmartTgtManager | A11 |
| L86 | `screening.entry_gate` | EntryGate, WatchEntry | A07 |
| L87 | `screening.quality_scorer` | QualityScorer | A07 |
| L88 | `screening.secondary_screener` | SecondaryScreener | A07 |
| L89 | `screening.step_executor` | StepExecutor | A07 |
| L90 | `signals.signal_processor` | SignalProcessor | A06 |
| L91 | `scripts.healthcheck_server` | start_healthcheck_server | A15 |
| L92 | `signals.webhook_receiver` | WebhookReceiver | A06 |
| L93 | `strategies.loader` | StrategyLoader, scan_strategy_errors | A02 |
| L94 | `utils.holiday_guard` | is_trading_day, next_trading_day, get_holiday_name | A01 |
| L95 | `utils.instance_lock` | acquire_instance_lock, check_port_available, release_instance_lock | A01 |
| L96 to L105 | `utils.startup_checks` | StartupCheckFailed, StartupScenario, check_config_hash, check_kill_switch_present, check_paper_capital_consistency, check_webhook_endpoint, detect_startup_scenario, run_all_startup_checks | A01 |
| L106 | `scripts.zerodha_login` | is_token_valid, load_token | A04 |

- FACT (AST): `check_port_available` (L95) is imported and never loaded; only a comment names it (L3980 to L3981).
- FACT (AST): `Callable` (L38) is never loaded at run time; it appears only inside string annotations (for example L1184, L1234 to L1236 and L1338 to L1339), which `from __future__ import annotations` (L22) leaves unevaluated.
- FACT: importing `scripts.zerodha_login` (L106) runs that module's top level, which calls `load_dotenv()` with no arguments (`scripts/zerodha_login.py` L32 and L36; A04). main.py itself never calls `load_dotenv` (grep). INTERPRETATION: importing `main.py` can therefore load variables from a `.env` file before `main()` runs; which file python-dotenv finds is library behaviour and is not shown by the repository (see the legacy records check, R3-08).
- INTERPRETATION: importing `main.py`, as `scripts/sr_level_export.py` and the tests do, imports every module listed above and creates `_shutdown_event` (L116) and `_gate_release_pool` (L865 to L867); `main()` runs only under the guard at L4285.

### 3.2 Imports inside functions (run when the function runs)

| Lines | Enclosing function | Module | Names | Owner | Note |
|---|---|---|---|---|---|
| L346 | `_alert_invalid_strategy_configs` | `alerts.critical` | write_critical_sentinel | A14 | |
| L383 | `_build_kite_client` | `kiteconnect` | KiteConnect | third-party | live |
| L384 | `_build_kite_client` | `requests.adapters` | HTTPAdapter | third-party | live |
| L407 | `_build_market_data_kite` | `json` | (module) | standard library | paper branch |
| L408 | `_build_market_data_kite` | `pathlib` | Path | standard library | paper branch |
| L409 | `_build_market_data_kite` | `kiteconnect` | KiteConnect | third-party | paper branch |
| L454 | `_load_special_sessions` | `datetime` | datetime | standard library | |
| L485 | `_make_paper_quote_provider` | `broker.zerodha_adapter` | Quote | A04 | paper-only |
| L486 | `_make_paper_quote_provider` | `kiteconnect` | KiteConnect | third-party | paper-only |
| L487 | `_make_paper_quote_provider` | `json` | (module) | standard library | paper-only |
| L488 | `_make_paper_quote_provider` | `logging` | (module) | standard library | paper-only |
| L489 | `_make_paper_quote_provider` | `threading` | (module) | standard library | paper-only |
| L490 | `_make_paper_quote_provider` | `time` | (module, as _time_mod) | standard library | paper-only |
| L491 | `_make_paper_quote_provider` | `pathlib` | Path | standard library | paper-only |
| L492 | `_make_paper_quote_provider` | `requests.adapters` | HTTPAdapter | third-party | paper-only |
| L513 | `_make_paper_quote_provider` | `yaml` | (module) | third-party | paper-only |
| L531 | `_make_paper_quote_provider` (nested `_raw_fetch`) | `core.time_authority` | now_ist | A01 | paper-only |
| L848 | `_build_strategy_governor` | `capital.strategy_governor` | StrategyGovernor | A09 | |
| L940 | `_start_eod_pre_alert_thread` | `time` | (module, as _time_mod) | standard library | |
| L941 | `_start_eod_pre_alert_thread` | `core.time_authority` | now_ist as _now_ist | A01 | |
| L991 | `_start_market_open_margin_sync_thread` | `time` | (module, as _time_mod) | standard library | |
| L992 | `_start_market_open_margin_sync_thread` | `core.time_authority` | now_ist as _now_ist | A01 | |
| L1131 | `_resolve_position_pipeline` | `core.constants` | PRODUCT_TO_INTENT | A01 | |
| L1354 | `_start_eod_self_exit_thread` | `time` | (module, as _time_mod) | standard library | |
| L1355 | `_start_eod_self_exit_thread` | `core.time_authority` | now_ist as _now_ist | A01 | |
| L1663 | `_shutdown` | `core.time_authority` | now_ist as _census_now_ist | A01 | |
| L1843 | `_interactive_select_account` | `core.account_registry` | AccountRow | A01 | never loaded (AST) |
| L1875 to L1879 | `_interactive_check_or_login` | `scripts.zerodha_login` | is_token_valid as _is_valid, load_token as _load, run_login_flow | A04 | interactive |
| L2226 | `_main_locked` | `core.time_authority` | now_ist as _now_ist_boot | A01 | |
| L2227 | `_main_locked` | `datetime` | time as _dtime_boot | standard library | |
| L2513 | `_main_locked` | `broker.slippage_engine` | SlippageEngine | A04 | paper-only |
| L2619 | `_main_locked` | `alerts.telegram_notifier` | ChannelConfig as _ChannelConfig | A14 | |
| L2749 | `_main_locked` | `core.time_authority` | now_ist | A01 | |
| L3094 | `_main_locked` | `orders.slippage_recorder` | SlippageRecorder | A11 | inside a try |
| L3107 | `_main_locked` | `core.time_authority` | now_ist as _now_ist_mh | A01 | |
| L3167 | `_main_locked` | `strategies.control` | strategy_will_trade as _swt | A07 | inside a try |
| L3221 | `_main_locked` | `orders.order_placer` | validate_slippage_overrides | A10 | inside a try |
| L3241 | `_main_locked` | `screening.hard_gate` | HardGate | A07 | |
| L3258 | `_main_locked` | `core.evidence_contract` | EvidenceRecorder, notifier_critical_sink | A15 | inside a try |
| L3493 | `_main_locked` | `sr_detector` | build_sr_detector | A08 | when the V1 flag is on |
| L3517 | `_main_locked` | `sr_detector.fetch` | OhlcFetcher | A08 | when the regime flag is on |
| L3518 | `_main_locked` | `regime` | MarketRegimeShadowRunner, build_market_regime | A18 | when the regime flag is on |
| L3551 | `_main_locked` | `sr_detector.zone_cache` | ZoneCache | A08 | when V2 or structure exit is on |
| L3552 | `_main_locked` | `sr_detector.zone_warmer` | ZoneWarmer | A08 | as L3551 |
| L3553 | `_main_locked` | `sr_detector.fetch` | OhlcFetcher | A08 | as L3551 |
| L3554 | `_main_locked` | `sr_detector.zone_builder` | build_scoring_params, build_zone_knobs | A08 | as L3551 |
| L3635 | `_main_locked` | `allocation` | PortfolioAllocator | A18 | when the allocator mode is not "off" |
| L3675 | `_main_locked` | `sr_detector.fetch` | OhlcFetcher | A08 | when the V3 chain is on |
| L3676 | `_main_locked` | `sr_detector.zone_builder` | build_scoring_params, build_zone_knobs | A08 | as L3675 |
| L3677 | `_main_locked` | `v3_chain` | V3ChainRunner | A18 | as L3675 |
| L3716 | `_main_locked` | `core.config_loader` | V3ChainConfig | A02 | when the watchlist is on |
| L3717 | `_main_locked` | `sr_detector.fetch` | OhlcFetcher | A08 | as L3716 |
| L3718 | `_main_locked` | `sr_detector.zone_builder` | build_scoring_params, build_zone_knobs | A08 | as L3716 |
| L3719 | `_main_locked` | `v3_chain.pb01_entry` | Pb01EntryStage | A18 | as L3716 |
| L3720 | `_main_locked` | `v3_chain.pb01_runner` | Pb01WouldBeRunner | A18 | as L3716 |
| L3721 | `_main_locked` | `v3_chain.watchlist_capture` | WatchlistCaptureWorker | A18 | as L3716 |
| L3771 | `_main_locked` | `sr_detector.fetch` | OhlcFetcher | A08 | when the V2 retest is on |
| L3772 | `_main_locked` | `sr_detector.retest_confirm` | RetestParams | A08 | as L3771 |
| L3773 | `_main_locked` | `screening.retest_monitor` | RetestDiverter, RetestMonitor | A08 | as L3771 |
| L3813 | `_main_locked` | `orders.structure_exit_manager` | StructureExitManager | A11 | when structure exit is on |
| L3987 | `_main_locked` | `waitress` | serve as _waitress_serve | third-party | the webhook server |
| L4038 | `_main_locked` | `alerts.critical` | write_critical_sentinel | A14 | webhook self-check failure branch |
| L4088 | `_main_locked` | `scripts.preflight.startup_hook` | run_on_demand_if_missed | A20 | inside a try |

- FACT: the conditions in the Note column are the `if` and `try` blocks that enclose each import, read at the cited lines; whether any optional block ran is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2).
- FACT (requirements file, A17's): `requirements.txt` pins kiteconnect 5.1.0 (L8) and python-dotenv 1.2.2 (L14). The versions installed on the VM are UNKNOWN / NOT ESTABLISHED.
