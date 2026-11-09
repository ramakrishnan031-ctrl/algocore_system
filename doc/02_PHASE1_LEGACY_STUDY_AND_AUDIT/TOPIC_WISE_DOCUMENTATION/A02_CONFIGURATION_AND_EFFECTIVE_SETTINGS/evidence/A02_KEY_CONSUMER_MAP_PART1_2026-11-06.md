# A02 evidence: Key-to-consumer map, part 1: `config/system_config.yaml` lines 1 to 358

**Status:** APPROVED — evidence for the A02 STUDY, approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31)
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06. Approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31): status marked APPROVED; content unchanged.
**Purpose and scope:** Records, for every leaf key in lines 1 to 358 of `config/system_config.yaml` (sections L21 to L357), its file value at the baseline, its loader field (type, default, constraints) and every consumer found in the code (call site, how it is read, owner topic). It also lists the exceptions: keys with no consumer, keys read but absent, values that a consumer overrides, transforms or ignores, settings read differently in different places, and direct readers of the file. It supports the STUDY's sections on the effective settings and their consumers.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

## 1. Method, conventions and generic consumers

**Method (FACT about what was done).**
1. The YAML text (`git show 970aabf:config/system_config.yaml`) was parsed with `yaml.safe_load` and `yaml.compose` by a script outside the clone. This listed every leaf key and its line. Sections L21 to L357 hold **100 leaf entries**. Two of them are not scalars: `special_sessions` (null) and `excluded_symbols` (a list).
2. `core/config_loader.py` was read, and parsed with `ast` by a second script, to get each field's type, default and validators. Every YAML key in range has a schema field, and no YAML key in range is outside the schema.
3. For every leaf name, `git grep -n -w` was run over the whole tree with `tests/`, `ops_dashboard/tests/`, `docs/`, `*.md` and `*.txt` excluded. Each hit was checked by following the object it is read from. For common names such as `enabled`, `shadow`, `capacity`, `primary`, `fallback`, `poll_interval_sec`, `entry_start` and `HIGH`, hits on other sections or on unrelated objects were discarded. One example is `v3_chain/pb01_entry.py` L107, which reads `watchlist.entry_start`, not `trading_hours.entry_start`.
4. Direct readers of `system_config.yaml` were found by grepping for the file name and for `load_all(`.

**Conventions.**
- `AC` = the `AppConfig` returned by `load_all()` (`core/config_loader.py` L2457 to L2516). Every key in this range lives at `AC.system.<section>.<key>`, through `SystemConfig` (L1987 to L2086) and `_CONFIG_FILES` (L2441 to L2450). Pydantic v2 runs in its default lax mode. All models set `extra="forbid"`.
- "req." means the field is required (no default). "attr" means attribute access. "getattr(d)" means `getattr` with default d. "get(d)" means dict `.get` with default d.
- **DASH** means a read by the ops dashboard (owner A15). It reads `ops_dashboard/backend/readers/config_reader.py:get_system_config` (L28 to L53): today's `config_snapshots.config_json` (the `AppConfig.model_dump`, defaults applied) or, if there is no snapshot, the **raw YAML** (no defaults applied, L45 to L52).
- "main.py Lnnn" is inside `main.py:_main_locked` unless another function is named. The owner of the wiring is A01; the component's owner is given in brackets.
- Every statement is a FACT at the cited lines unless it is marked INTERPRETATION or HISTORICAL. File values are "the file value at the baseline", not proof that they were in force (UNKNOWN / NOT ESTABLISHED).

**Generic whole-tree consumers.** These read every key and are not repeated in each row.

| Consumer | What it does | Owner |
|---|---|---|
| `core/config_snapshotter.py` (`snapshot_config`, called at main.py L2603 to L2612) | Writes `AppConfig.model_dump(mode="json")` to `config_snapshots.config_json`. `trade_type` is also passed as its own column (main.py L2610). | A02 |
| `core/config_validator.py` `register_all_from_app_config` (main.py L2205) and `validate_all(strict=False)` (main.py L4164) | Registers every leaf as "expected". INTERPRETATION: grep finds no caller of `config_validator.get(` apart from the docstring example (L31 to L34), so every key would be reported as unaccessed. The report is only a warning because `strict=False` (L243 to L255). | A02 |
| `core/config_auditor.py` (startup groups "ACG", L811, run from `SystemConfig._cross_field_sanity_checks` L2056 to L2086; group A with strategies from main.py L3437 and L3459; all groups in pre-flight through `audit_app_config` L821) | Reads specific keys; these are named in the rows below. | A02 |
| DASH `services/config_view.py:build_config_center` (category tabs L255 to L270) and `services/audit.py` (path classification L70 to L94) | Shows or diffs every top-level section in range. | A15 |

---

## 2. Key-to-consumer tables

### 2.1 `broker` (YAML L21; `BrokerConfig` L1921 to L1927; whole section optional, `SystemConfig.broker` default `BrokerConfig()` L1989)

| Key path | YAML L | File value | Loader (path; type; default; constraints) | Consumers (file:function:line; how read) | Owner | Notes |
|---|---|---|---|---|---|---|
| broker.primary | 22 | "zerodha" | `AC.system.broker.primary`; str; "zerodha" (L1924); none | DASH `services/config_view.py:_kpis` L408, L449 (get, no default; Broker KPI); `build_config_center` L721 to L722 (get, passed to `get_broker_costs`) | A15 | **No runtime consumer found by grep.** The runtime code hard-codes "zerodha" instead: `ProductResolver.resolve` default broker (broker/product_resolver.py L95); `ZerodhaAdapter.place_order` L587 and `ZerodhaAdapter.get_live_margin_pct` L1586; main.py L3293. main.py L2556 to L2572 rejects any `accounts.csv` broker other than 'zerodha' (exit 9). |
| broker.fallback | 23 | "angelone" | str; "angelone" (L1925); none | **No consumer found by grep.** | — | |
| broker.fallback_enabled | 24 | false | bool; False (L1926); none | **No consumer found by grep.** It appears only in the docstring of broker/angelone_adapter.py (L12, L26). | — | |
| broker.multi_account_mode | 25 | false | bool; False (L1927); none | **No consumer found by grep.** | — | HISTORICAL: docs/audit/integrity_audit_2026.md L3727 to L3729 calls it an orphan. |

### 2.2 `trading_hours` (YAML L27; `TradingHoursConfig` L86 to L189; required section, L1990)

The validators apply to the whole section:
- `_validate_mis_squareoff_timing` (L109 to L137) calls `core/mis_squareoff_timing.MisSquareoffTiming.build` with a **literal `poll_interval_sec=5`** (L131).
- `_validate_window_ordering` (L139 to L189) requires `market_open <= entry_start < entry_end <= eod_entry_cutoff <= eod_squareoff_time <= market_close` (L168) and `market_close <= service_window_end < 18:15` (`SERVICE_WINDOW_END_MAX` L83; check L179 to L188).
- HH:MM text is parsed only by `split(":")`, `int()` and `time()` (L158 to L160).

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| trading_hours.entry_start | 28 | "10:00" | str; req. (L88); ordering | main.py L2321 attr → `MarketWindows(entry_start=)` (core/market_windows.py L52, L61; `is_entry_allowed` L143 to L150, which the webhook calls at signals/webhook_receiver.py L582; `is_entry_allowed_for_strategy`) [A01]. config_auditor: `LAUNCH_PHASE_PARAMS` getter L165 (group E, pre-flight); `_group_g_cross_field` G5 L746, L758 (only with strategies) [A02]. DASH config_view L795 (by `_HOURS_ROWS` L233 to L236). reports/daily_trade_review.py `build_config_data` L1229 [A15]. | A01, A02, A15 | The `MarketWindows` ctor default is 09:30 (core/market_windows.py L23); it is unused because main passes the value. strategies/schema.py L137 defaults the per-strategy `entry_start_time` to "10:00". The dashboard clock uses a **copy** in ops_dashboard/backend/config/gui_config.yaml L61 to L69 (`market_clock`), not this key. So do the dashboard's Entry Window and Market Session rows (ops_dashboard/backend/services/capacity.py `build_capacity` L209 to L217, which read `market_clock` from the dashboard's own config). `special_sessions` does not move it (`is_entry_allowed` L143 to L150). |
| trading_hours.entry_end | 47 | "15:00" | str; req. (L89); ordering; also `entry_end < CHECK_1` (mis_squareoff_timing L150) | main.py L2322 → `MarketWindows` [A01]. main.py L3335 → `MisSquareoffTiming.build` (mis_squareoff_timing L110, L118, L150; ordering only) [A12]. alerts/mis_squareoff_notifier.py `MisSquareoffNotifier.__init__` L170 (attr on the object passed at main.py L3344) [A14]. Loader L132. config_auditor G1 L684, L690; G5 L747 [A02]. DASH config_view L795. daily_trade_review L1230. | A01, A12, A14, A02, A15 | The `MarketWindows` default is 13:30 (L24). gui_config copy: "15:00". |
| trading_hours.eod_entry_cutoff | 48 | "15:15" | str; req. (L90); ordering | main.py L2326 → `MarketWindows.eod_entry_cutoff_t` (L57, L66; `is_past_eod_entry_cutoff` L177 to L190, called at orders/order_placer.py L1077; OrderPlacer gets `market_windows` at main.py L3082) [A01, A10]. DASH config_view L795. daily_trade_review L1231. | A01, A10, A15 | The `MarketWindows` default is 15:15 (L31). It is not moved per date by `special_sessions`. |
| trading_hours.eod_squareoff_time | 49 | "15:17" | str; req. (L91); ordering; `cutoff < eod` (mis_squareoff_timing L150) | main.py L2325 → `MarketWindows(eod_squareoff=)` (`is_eod_squareoff_due` L194, `eod_squareoff_time` L207, special-session aware) [A01; EodSquareoff A12]. main.py L3336 → `MisSquareoffTiming.build` [A12]. notifier L171 [A14]. main.py L4153 to L4155 → `_start_eod_self_exit_thread(squareoff_time=)` (label only, per comment L4151 to L4152) [A01]. Loader L133. config_auditor G1 L685 [A02]. DASH config_view L795. daily_trade_review L1232. | A01, A12, A14, A02, A15 | The `MarketWindows` default is 15:17 (L27). Per-date override: main.py L467. gui_config copy key `eod_squareoff` "15:17". |
| trading_hours.mis_squareoff_cutoff | 59 | "15:09" | str; default **"15:12"** (L104); `MisSquareoffTiming.build` (L126 to L134) | main.py L3330 → `MisSquareoffTiming.build` → `MisAutoSquareoff(timing=)` (main.py L3359 to L3380) [A12]. notifier L165 (builds its own timing) [A14]. | A12, A14 | The loader default differs from the file value. HISTORICAL: the main.py comment at L3324 to L3327 says "15:07/15:10 ... CAS 15:12", which does not match 15:09 with 6m/3m. Absolute time, not session-relative (YAML comment L86 to L89). |
| trading_hours.mis_squareoff_first_offset | 90 | "6m" | str; default **"5m"** (L105); parsed by `_parse_offset_minutes`; must exceed the second offset (mis_squareoff_timing L140 to L144) | main.py L3331 [A12]; notifier L166 [A14] | A12, A14 | The loader default differs. |
| trading_hours.mis_squareoff_second_offset | 91 | "3m" | str; default **"2m"** (L106) | main.py L3332 [A12]; notifier L167 [A14] | A12, A14 | The loader default differs. |
| trading_hours.mis_squareoff_margin_sec | 96 | 20 | int; 20 (L107); must be an int and `>= poll_interval_sec` (mis_squareoff_timing L121 to L138) | main.py L3333 [A12]; notifier L168 [A14] | A12, A14 | At load the floor is checked against the literal 5 (loader L131). At runtime main.py L3334 and the notifier (main.py L3345) use `eod_squareoff.poll_interval_sec` (YAML L361, value 5; outside this range). |
| trading_hours.market_open | 103 | "09:15" | str; "09:15" (L92); ordering | main.py L2228 to L2232: boot "market open now" check for `StateStore(market_open=)`; uses split(":") and weekday<5 directly, with no holidays and no special sessions [A01, A03]. main.py L2323 → `MarketWindows` [A01]. main.py L3396 → `TokenMonitor(market_open=)` (broker/token_monitor.py L63, L82 to L84) [A04]. scripts/deploy_preflight.py `_VM_MARKET_CODE` L46 to L48 (a `python -c` string that builds its own `MarketWindows`) [A17]. scripts/sr_level_export.py `_make_real_analyze_fn` L147 to L148 [A08]. DASH config_view L795. daily_trade_review L1233. Indirect, through the `MarketWindows.market_open` attribute: main.py L3236 (`StepExecutor`) [A07]; L3501 (sr_detector `session_open`) [A08]; regime/engine.py L332 and v3_chain/pb01_entry.py L316 [A18]. | A01, A03, A04, A17, A08, A07, A18, A15 | Hard-coded 09:15 duplicates: main.py `_start_market_open_margin_sync_thread` L994; screening/step_executor.py L36 (fallback); signals/signal_processor.py L1745 (gap window); scripts/gemini_watchman.py L45; scripts/t2_cnc_gtt_realtest.py L125; gui_config L64. |
| trading_hours.market_close | 104 | "15:30" | str; "15:30" (L93); ordering; lower bound of `service_window_end` | main.py L2231 (boot check) [A01, A03]. L2324 → `MarketWindows` [A01]. L3312 → `EodSquareoff(market_close=)` (orders/eod_squareoff.py L125 default "15:30", L149 strptime) [A12]. L3397 → `TokenMonitor` [A04]. deploy_preflight L49 [A17]. sr_level_export L148 [A08]. DASH config_view L795. daily_trade_review L1234. Indirect: main.py L3502 [A08]; regime/engine.py L333 and v3_chain/watchlist_capture.py L222 [A18]. | A01, A03, A12, A04, A17, A08, A18, A15 | Hard-coded 15:30: ops/control_tower/freshness.py L18; scripts/sr_level_export.py L158; t2 script L125; ops_dashboard execution_analytics.py L129; gui_config L68. `EodSquareoff` and `TokenMonitor` receive the regular-session string, not the per-date value. |
| trading_hours.service_window_end | 112 | "17:35" | str; default **"16:00"** (L98); `market_close <= x < 18:15` (L179 to L188) | main.py L2211 attr → `_parse_hhmm` → boot banner (L2212 to L2216) and `_start_eod_self_exit_thread(window_end=)` L4142. The thread is armed only for normal starts (L4129 to L4133). [A01] | A01 | `main.SERVICE_START_CUTOFF = SERVICE_WINDOW_END_MAX` (main.py L2001). scripts/liveness_probe.py L109 hard-codes `_LIVENESS_END = 16:00` [A15]. The loader default differs from the file value. |

### 2.3 `special_sessions` (YAML L117)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| special_sessions | 117 | null. Only a commented example exists (L118 to L122). | `AC.system.special_sessions`; `dict[str, dict[str, str]]` or None; None (L1992); no check of inner keys or time format | main.py `_load_special_sessions` L456: getattr(None); a falsy value gives `{}`. Otherwise it runs `strptime("%Y-%m-%d")` (L463) and `session['market_open'/'market_close'/'eod_squareoff_time']` (L465 to L467). INTERPRETATION (Python semantics): a missing inner key raises KeyError. The result goes to `MarketWindows(special_sessions=)` L2328 (core/market_windows.py L59, L69 to L71, `_get_effective_times` L87 to L89, holiday exemption L101, `next_trading_day` L119), and a log line at main.py L2333 to L2344 [A01]. DASH: generic only. | A01 | It overrides only market_open, market_close and eod_squareoff per date. It does not move entry_start, entry_end, eod_entry_cutoff, mis_squareoff_* or service_window_end. INTERPRETATION, tested with a script outside the clone using pydantic 2.13.5 (requirements.txt L7 pins 2.13.0): the commented example's **unquoted** date key `2026-11-01:` parses as a `date`, and the schema then rejects it ("Input should be a valid string"). A quoted key passes. |

### 2.4 `signal_queue` (YAML L124; `SignalQueueConfig` L192 to L197; required section, L1991; no validators)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| signal_queue.capacity | 125 | 300 | int; req. (L194); none | main.py L3403 → `queue.Queue(maxsize=)` [A06]. signals/webhook_receiver.py `WebhookReceiver._process_request` L537, L571 (attr); `_register_routes.health` L397 [A06]. DASH capacity.py L170. | A06, A15 | |
| signal_queue.backpressure_pct | 126 | 0.80 | float; req. (L195); none | webhook_receiver `_process_request` L573: HTTP 503 when `qsize >= int(capacity × pct)` (L575 to L578) [A06]. DASH capacity.py L171. | A06, A15 | INTERPRETATION: 240 at the file values. Pre-flight `WebhookBackpressureCheck` uses a hard-coded 0.9 × capacity read from `/metrics` (scripts/preflight/checks/signals.py L78) [A20]. |
| signal_queue.expiry_sec | 127 | 600 | int; req. (L196; the comment there says "default 60") | webhook_receiver `_process_request` L679 (reads the value); `WebhookReceiver._process_signal` age check L925 and `expires_at` L960 [A06]. main.py L3614 → `SignalProcessor(signal_expiry_sec=)` (signals/signal_processor.py L175 default **60**, L222, check L917) [A06]. | A06 | The ctor default 60 differs from the file value 600. config_validator docstring L12 (HISTORICAL) cites this mismatch. |
| signal_queue.warning_pct | 128 | 0.60 | float; 0.60 (L197); none | webhook_receiver `_process_request` L574 getattr(0.60) → `X-Queue-Warning` header (L743 to L744) [A06]. | A06 | |

### 2.5 Top-level scalars and lists (`excluded_symbols` L131; `force_intraday_only` L142; `trade_type` L149; `delivery_enabled` L155)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| excluded_symbols | 131 | list of 5: E2E, GVPIL, BIRLACABLE, SHANKARA, MCLEODRUSS | `list[str]`; `[]` (L1993); none | webhook_receiver `_process_request` L709 getattr([]); compared case-insensitively after alias resolution (L710 to L717) [A06]. reports/daily_report.py `load_report_data` L145 to L149: **raw YAML** get([]); membership is case-sensitive (L481, L695) [A15]. | A06, A15 | Read differently in two places: through the model in the receiver, and as raw YAML in the report. The loader default `[]` differs from the file value. |
| force_intraday_only | 142 | false | bool; default **True** (L2030); none | main.py L2410 → `ZerodhaAdapter(force_intraday_only=)` (broker/zerodha_adapter.py L397 default **False**, L422; intent coercion L579 to L584) [A04]. L2697, L2700 to L2701: active-book predicates for `resolve_bucket_allocation` [A09]. L3161 → `StrategyLoader.load_all_strategies` (strategies/loader.py L106 default False; L142 logs dormant, no rewrite) [A02]. L3169, L3191: boot logs. L3621 → `SignalProcessor` (L194 default False, L238; passed to `strategies/control.strategy_will_trade` at L961, L2064, L2413; control.py L90) [A06, A07]. config_auditor A1 L196, A3 L307, A5 L272 [A02]. ops/control_tower/aggregator.py `read_config` L158 [A15]. scripts/preflight/checks/config_sanity.py `_build_report` L39 [A20]. scripts/cron_officer.py `_strategy_status_payload` L475: **raw YAML** get(True) [A16]. DASH capacity.py L128 (get(True); marks the delivery caps "inert" at L186, L190); controls.py `build_controls_screen` L229 (get(True)); operations.py `build_controls_summary` L37 (get(True)). daily_trade_review L1225. | A04, A09, A02, A06, A07, A20, A16, A15 | Defaults differ: True in the loader, cron_officer and DASH; False in the ZerodhaAdapter, SignalProcessor and StrategyLoader ctors. HISTORICAL: the main.py comment at L2690 to L2693 says "force_intraday_only=true (current state)"; the file value is false. |
| trade_type | 149 | BOTH | str; default **"INTRADAY"** (L2044); one of {INTRADAY, DELIVERY, BOTH} (L2046 to L2054) | main.py L2610 → `snapshot_config(trade_type=)` [A02]. L2698, L2700: bucket predicates [A09]. L3168, L3193, L3198: boot logs. L3620 → `SignalProcessor(trade_type=)` (L193 default "INTRADAY", L237; used at L960, L2063, L2412) [A06, A07]. config_auditor A1 L196, A2 L207, A3 L309, A5 L275 [A02]. scripts/cron_officer.py L474: **raw YAML** get("INTRADAY") [A16]. DASH controls.py L230 (get or "INTRADAY"); operations.py L38. config_view L411 and L781 read `trade_type` from the snapshot **row** or session, not from `config_json`. daily_trade_review L1224. | A02, A09, A06, A07, A16, A15 | The loader default differs from the file value. |
| delivery_enabled | 155 | true | bool; default **False** (L2037); none | main.py L2406 → `ZerodhaAdapter(delivery_enabled=)` (L391 default False, L420; CNC refusal L593 to L603) [A04]. L2696: bucket predicate [A09]. L3031 → `CncGttPlacer(delivery_enabled=)` (orders/cnc_gtt.py L64, L76) [A11]. L3190: boot log. L3458 getattr(False) `is True` → runs config_auditor group A (A5) with strategies; exits 3 on a block (L3459 to L3466) [A01, A02]. config_auditor A5 L271 [A02]. DASH: generic only. daily_trade_review L1226. | A04, A09, A11, A01, A02, A15 | The loader default differs from the file value. The adapter's lock compares the literal `broker_code == "CNC"` (zerodha_adapter L593), not `product_map`. |

### 2.6 `product_map` (YAML L157; `SystemConfig.product_map: dict[str, dict[str, str]]`, req., L1995; no check of brokers or intents)

All four leaves have one consumer: the whole map is passed at main.py L2349 → `ProductResolver(app_config.system.product_map)` (broker/product_resolver.py `__init__` L63 to L93: rejects an empty map or non-dict entries; makes a copy). It is then read through `resolve(intent, broker="zerodha")` (L95). The callers of `resolve` are: `ZerodhaAdapter.place_order` L587 and `ZerodhaAdapter.get_live_margin_pct` L1586 [A04]; the screener's `resolve_product` (main.py L3293) [A07]; OrderPlacer L2584, L2757, L2994, L3235, L3664, L3964, L4661 [A10]; scripts/t2_cnc_gtt_realtest.py `_build_live_adapter` L170 [A19]. Owner of ProductResolver: A04.

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| product_map.zerodha.INTRADAY | 159 | "MIS" | str inside dict; req. section | ProductResolver (above) | A04 | The literal "MIS" occurs 58 times in non-test, non-dashboard Python (count from git grep; not traced one by one), e.g. order_placer L3964 fallback, mis_autosquareoff L89 (`MIS_PRODUCT`), structure_exit_manager L630, cost_calculator L147 to L224. |
| product_map.zerodha.DELIVERY | 160 | "CNC" | as above | ProductResolver | A04 | Literal "CNC" comparisons: zerodha_adapter L593 (delivery lock); kill_switch L1749, L1928; order_reconciler L2049; mis_autosquareoff L467. |
| product_map.zerodha.COVER_ORDER | 161 | "CO" | as above | ProductResolver | A04 | |
| product_map.zerodha.BRACKET_ORDER | 162 | "" | as above | ProductResolver; an empty code raises `ProductNotSupportedError` (`resolve` L125 to L136; docstring L106 to L109) | A04 | `capital.leverage_map.BRACKET_ORDER` is still set to 5.0 (L211). |

### 2.7 `mis_filter` (YAML L170; `MisFilterConfig` L432 to L450; section optional, `default_factory`, L1994)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| mis_filter.enabled | 179 | true | bool; default **False** (L441) | main.py L3291 → `SecondaryScreener(mis_filter_enabled=)` (screening/secondary_screener.py L75 default False, L115, gate L148) [A07]. | A07 | The loader default differs. The YAML comment at L173 cites "secondary_screener.py:144 ... :159". At the baseline the check is at L148 to L150 and the fall-through comment is at L165. |
| mis_filter.shadow | 180 | true | bool; True (L442) | main.py L3292 → screener L76 default True, L116, L150 [A07] | A07 | |
| mis_filter.ttl_days | 181 | 1 | int; 1; `>= 1` (L443 to L450) | main.py L3057 → `MisLearnedBlocklist(ttl_days=)` (core/mis_blocklist.py L68 default **5**, L73) [A12] | A12 | The ctor default 5 differs from the loader and file value 1. |

### 2.8 `clock` (YAML L183; `ClockConfig` L214 to L220; `ClockSkewProbeConfig` L200 to L211; required section, L1996)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| clock.warn_skew_sec | 184 | 2.0 | float; req. (L216); no validator | main.py `_init_time_authority` L372 → `time_authority.configure(thresholds={"warn_sec"})` (core/time_authority.py defaults L66 to L70; use L223 to L233) [A01]. DASH capacity.py L291. | A01, A15 | The loader does not check `warn < alert < halt`. |
| clock.alert_skew_sec | 185 | 5.0 | float; req. (L217) | main.py L373 [A01]; DASH L292 | A01, A15 | |
| clock.halt_skew_sec | 186 | 30.0 | float; req. (L218) | main.py L374; the critical callback calls `kill_switch.soft_kill` (main.py L364 to L368) [A01, A13]; DASH L293 | A01, A13, A15 | |
| clock.startup_max_skew_sec | 187 | 30.0 | float; req. (L219) | main.py L375 → time_authority `startup_max_sec` (used at L283) [A01]. utils/startup_checks.py `run_all_startup_checks` L1572 (`tolerance_sec=`) [A01]. | A01 | Read in two places. |
| clock.probe.enabled | 189 | true | bool; True (L203); the probe section defaults through `default_factory` (L220) | main.py L3910 passes the probe config object, live only (`if not is_paper` L3906; paper logs a skip at L3918) → `BrokerClockSkewProbe.start` L71 [A04] | A04 | |
| clock.probe.probe_interval_sec | 190 | 60 | int; 60; `> 0` (L204 to L211) | broker/clock_skew_probe.py `start` L86 (log); `_run_loop` L107 (wait timeout) [A04] | A04 | |

### 2.9 `order_monitor` (YAML L192; `OrderMonitorConfig` L412 to L429; required section, L1997)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| order_monitor.poll_interval_sec | 193 | 2 | int; req.; `>= 1` (L414, L417 to L422) | main.py L3003 → `OrderMonitor(poll_interval_sec=)` (broker/order_monitor.py L174 default 2, L211) [A04] | A04 | The `config_validator` docstring (L31 to L34) shows this key as a usage example only. |
| order_monitor.fill_timeout_sec | 194 | 60 | int; req.; `>= 5` (L415, L424 to L429) | main.py L3004 → `OrderMonitor` (L175 default 60, L212) [A04] | A04 | |

### 2.10 `capital` (YAML L196; `CapitalConfig` L330 to L409; `LeverageMapConfig` L292 to L327; `LeverageSafetyConfig` L250 to L289; required section, L1998)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| capital.intraday_bucket_pct | 197 | 0.70 | float; req.; `0 < x < 1` (L332, L382 to L387). **The sum with positional is not checked at load.** | main.py L2706 → `resolve_bucket_allocation` (capital/fund_manager.py L112 to L146) → `FundManager(intraday_bucket_pct=)` L2722 (ctor default 0.70 L299; sum check L324 to L328) [A09]. config_auditor A5 L282 (in the message) [A02]. DASH risk_capital.py `get_capital` L76, `get_capital_segments` L205; capacity.py L152; config_view `_mode_specific` L573; strategy_tower.py L165. | A09, A02, A15 | When `conditional_allocation_enabled` is true, this key is ignored (fund_manager L138 to L146): intraday = 1.0 − positional when both books are active; otherwise 1.0 when delivery is not active (including when neither book is active) and 0.0 when only delivery is active. INTERPRETATION: the split then always sums to 1.0, so the FundManager sum check (L324 to L328) cannot fail in that mode. |
| capital.positional_bucket_pct | 198 | 0.30 | as above (L333) | main.py L2707 → `FundManager` L2723 (ctor default 0.30 L300) [A09]. DASH risk_capital L77, L206; config_view L573. | A09, A15 | When `conditional_allocation_enabled` is true, this key is used only when both books are active; otherwise the positional share is 0.0 or 1.0 by active books (fund_manager L138 to L146). |
| capital.conditional_allocation_enabled | 199 | false | bool; False (L340) | main.py L2703 (and the log at L2711) [A09]. config_auditor A5 L270 [A02]. DASH config_view L807. | A09, A02, A15 | |
| capital.slm_margin_buffer_pct | 203 | 0.05 | float; 0.05 (L345); no validator | **No runtime consumer.** The `FundManager(...)` call at main.py L2718 to L2736 does not pass it, so the ctor default 0.05 applies (capital/fund_manager.py L309, L341). DASH risk_capital L268; config_view L804. | A15 | HISTORICAL: integrity_audit_2026.md L3739 says "half-dead". |
| capital.sl_limit_offset_pct | 204 | 0.005 | float; 0.005; `0 <= x < 0.10` (L346, L357 to L363) | main.py L3021 → `LimitTripleProtocol` (orders/order_protocol_limit.py L157, L167) [A10]. L3030 → `CncGttPlacer(gtt_tgt_limit_offset_pct=)`, re-used as the GTT target offset [A11]. L3829 to L3830 getattr(0.005) → `StructureExitManager` (L111, L125) [A11]. scripts/t2_cnc_gtt_realtest.py `main` L571 [A19]. DASH config_view L798. | A10, A11, A19, A15 | **Bypassed by a constant**: `OrderReconciler._g5b_crash_recovery_sl` L3297, L3314 uses `DEFAULT_SL_LIMIT_OFFSET_PCT` (orders/price_math.py L159, 0.005) [A12]. `BreakevenManager` (orders/breakeven_manager.py L80) has its own default; grep finds no construction of it in main.py. |
| capital.gtt_sl_limit_offset_pct | 205 | 0.03 | float; 0.03; `0 < x < 0.20` (L350, L365 to L372) | main.py L3029 → `CncGttPlacer` (orders/cnc_gtt.py L62, L74) [A11]. t2 script L570 [A19]. DASH config_view L800. | A11, A19, A15 | |
| capital.emergency_exit_buffer_pct | 206 | 0.01 | float; 0.01; `0 <= x < 0.10` (L351, L374 to L380) | main.py L2250 → `KillSwitch` (capital/kill_switch.py L264, L281) [A13]. L3084 → `OrderPlacer` (orders/order_placer.py L593, L624) [A10]. DASH config_view L802. | A13, A10, A15 | **Bypassed by the constant** `EMERGENCY_EXIT_BUFFER_PCT` (price_math L124, 0.01) at: `EodSquareoff._place_marketable_limit_exit` L1543 [A12]; `OrderReconciler._flatten_broker_position` L2324 [A12]; `StructureExitManager._flatten_one` L438 [A11]; and, outside the trading process, the real-API test script scripts/t2_cnc_gtt_realtest.py `_marketable_limit` L265, L275 [A19]. `SlBreachMonitor` (L51) has its own default; grep finds no construction of it in main.py. |
| capital.leverage_map.INTRADAY | 208 | 5.0 | float; req.; finite; inside `leverage_safety` (L307, L312 to L315, L389 to L409) | main.py L2679 → dict → `FundManager(leverage_map=)` L2728 (`required_margin` L267 `.get(intent, 1.0)`) and `PositionSizer(leverage_map=)` L2842 [A09]. config_auditor G2 L695 to L702 (warns above 10) [A02]. DASH risk_capital L199; config_view L561. daily_trade_review L1207, L1236. | A09, A02, A15 | `FundManager` falls back to a hard-coded map (5/6/1/5) when given None (L312 to L318); main always passes the map. |
| capital.leverage_map.COVER_ORDER | 209 | 6.0 | as above (L308) | main.py L2680 → same; config_auditor G2 L696; DASH; daily_trade_review L1237 | A09, A02, A15 | |
| capital.leverage_map.DELIVERY | 210 | 1.0 | float; req.; **exactly 1.0** (L317 to L327, `_DELIVERY_PINNED_LEVERAGE` L232) | main.py L2681 → same; DASH; daily_trade_review L1239 | A09, A15 | |
| capital.leverage_map.BRACKET_ORDER | 211 | 5.0 | as INTRADAY (L310) | main.py L2682 → same; DASH; daily_trade_review L1238 | A09, A15 | `product_map` BRACKET_ORDER is "" (not supported). |
| capital.leverage_safety.min_allowed | 213 | 1.0 | float; req.; finite; `>= 1.0` (L262, L265 to L277) | **Loader only**: the bound check in `CapitalConfig._validate_leverage_within_safety` L400. No consumer outside core/config_loader.py found by grep. | A02 | |
| capital.leverage_safety.max_allowed | 214 | 10.0 | float; req.; finite; `>= min_allowed`; `<= ABSOLUTE_MAX_LEVERAGE` 20.0 (L229, L278 to L288) | **Loader only**: L401. No consumer outside the loader found by grep. | A02 | YAML L215 to L216 says it re-uses auditor G2's `> 10`. G2 keeps its own literal (L697). INTERPRETATION: with max_allowed 10.0 the loader already rejects any value above 10, so G2 cannot fire. |

### 2.11 `position_sizing` (YAML L219; `PositionSizingConfig` L460 to L561; `PositionSizingTierConfig` L453 to L457; required section, L1999)

All runtime reads go through main.py L2839 to L2879 → `PositionSizer(...)` (capital/position_sizer.py `__init__` L135 to L214) [A09], unless another consumer is named.

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| position_sizing.enabled | 220 | true | bool; True (L479); if false, `flat_value_rs > 0` is required (L551 to L561) | main.py L2855 (`enabled=`), L2865 (mode log) [A09]. scripts/preflight/checks/config_integrity.py `TierMultiplierModeCheck.run` L225 to L226: **raw YAML** get(True) [A20]. scripts/cron_officer.py `_tier_mode_line` L508 to L509: **raw YAML** get(True) [A16]. DASH config_view L823. | A09, A20, A16, A15 | |
| (position_sizing.flat_value_rs) | (223, commented out) | **absent** | `Optional[float]`; None (L480) | main.py L2856 (`flat_value_rs=`), L2877, L2879 (used only when enabled=false); config_integrity L231; cron_officer L511 | A09, A20, A16 | The key is read by code but absent from the YAML, so the default None applies. |
| position_sizing.risk_per_trade_pct | 225 | 0.01 | float; req.; `0 < x < 1` (L462, L515 to L520) | main.py L2843 (ctor param has no default, L147) [A09]. config_auditor C3 L497, C4 L505, C5 L516 [A02]. scripts/system_manager.py `config_vs_actual_check` L296 [A15]. DASH config_view L591. daily_trade_review L1252. | A09, A02, A15 | |
| position_sizing.max_concentration_pct | 226 | 0.10 | float; req.; `0 < x <= 1` (L463, L522 to L527) | main.py L2844 [A09]. config_auditor C2 L453, C4 [A02]. system_manager L296. DASH capacity L220; config_view L595; controls L185, L300; operations L60. daily_trade_review L1251. | A09, A02, A15 | |
| position_sizing.min_qty_threshold | 227 | 1 | int; req.; `>= 1` (L464, L529 to L534) | main.py L2845 (ctor default 1, L159) [A09]. DASH config_view L833. | A09, A15 | |
| position_sizing.lot_skew_rejection_threshold | 228 | 0.25 | float; req.; `0 < x <= 1` (L465, L536 to L541) | main.py L2853 (ctor default 0.25, L163) [A09]. DASH config_view L837. | A09, A15 | |
| position_sizing.min_tick_size | 229 | 0.05 | float; req.; no validator (L466) | **Not passed by main.py**, so the PositionSizer ctor default 0.05 applies (L164, L191). config_auditor G3 L705 (warns below 0.01) [A02]. DASH config_view L835. | A02, A15 | The YAML value is not the source of the runtime value. HISTORICAL: integrity_audit_2026.md L3736 to L3737. |
| position_sizing.max_single_order_qty | 230 | 10000 | int; req.; no validator (L467) | **Not passed by main.py**, so the ctor default 10000 applies (L165, L192). DASH capacity L204; config_view L643. | A15 | as above |
| position_sizing.max_position_value_pct | 236 | 0.40 | float; req.; `0 < x <= 1` (L474, L543 to L549) | main.py L2854 (ctor param has no default, L154) [A09]. config_auditor C2 L454, F registry L176 to L177 [A02]. system_manager L279 getattr(0.0), L282, L286 [A15]. DASH capacity L236; config_view L600; controls L189. daily_trade_review L1250. | A09, A02, A15 | |
| position_sizing.tier_multipliers.HIGH | 238 | 1.0 | float; req.; **no range validator** (L455) | main.py L2847 → dict (ctor fallback `_DEFAULT_TIER_MULTIPLIERS` L58 to L62 when None) [A09]. config_auditor `_max_effective_multiplier` L409 to L410 [A02]. config_integrity L227 (raw YAML) [A20]. DASH capacity L271. main.py L2866 to L2873 (log). | A09, A02, A20, A15 | |
| position_sizing.tier_multipliers.MEDIUM | 239 | 0.70 | as above (L456) | main.py L2848; the same others | as above | |
| position_sizing.tier_multipliers.LOW | 240 | 0.50 | as above (L457) | main.py L2849; the same others | as above | |
| position_sizing.dynamic_by_winrate | 241 | true | bool; True (L476) | main.py L2871: **startup log only**. DASH capacity L272; config_view L825. | A15 | No behavioural consumer found. `SignalProcessor` gets no `perf_weights` (main.py L3575 to L3622), so `perf_weight` is always 1.0 (signal_processor L1120, L2116, L2458, `.get(name, 1.0)`). `capital/performance_allocator.py` is not used outside its own module (grep). |
| position_sizing.min_multiplier | 242 | 0.5 | float; 0.5 (L477); no validator | DASH capacity L273; config_view L828, L830 only. | A15 | No runtime consumer. The same number is hard-coded as `PerformanceAllocator` `min_weight=0.5` (performance_allocator.py L61), and that class is not wired. |
| position_sizing.max_multiplier | 243 | 2.0 | float; 2.0 (L478); no validator | config_auditor `_max_effective_multiplier` L412 [A02]. DASH capacity L274; config_view L829, L831. | A02, A15 | No runtime consumer. The sizer applies a hard-coded 2× clamp (position_sizer L605; mirrored by auditor `_SIZER_TIERED_QTY_HARD_CAP` L398). `PerformanceAllocator` `max_weight=2.0` (L62) is not wired. |
| position_sizing.delivery_risk_per_trade_pct | 253 | 0.01 | `Optional[float]`; req.; a null or missing value is rejected; `0 < x <= 1` (L497, L501 to L513) | main.py L2860 → ctor (default None, L178); `_require_delivery` refuses None at L376 [A09]. DASH config_view L591. | A09, A15 | |
| position_sizing.delivery_max_concentration_pct | 254 | 0.10 | as above (L498) | main.py L2861 (L179, L378) [A09]. config_auditor C2d L479 [A02]. DASH config_view L596; controls L186. | A09, A02, A15 | |
| position_sizing.delivery_max_position_value_pct | 259 | 0.40 | as above (L499) | main.py L2862 (L180, L380) [A09]. config_auditor C2d L480 [A02]. DASH config_view L601; controls L190. | A09, A02, A15 | |

### 2.12 `risk` (YAML L261; `RiskConfig` L747 to L881; required section, L2000)

Runtime reads go through main.py L2891 to L2925 → `RiskEngine(...)` (capital/risk_engine.py `__init__` L149 to L205) [A09], unless another consumer is named.

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| risk.max_open_positions | 271 | 5 | int; req.; `>= 1` (L749, L824 to L829) | main.py L2899 (ctor param has no default, L149; L194) [A09]. main.py L3639 reads the **private** `risk_engine._max_open` with getattr(5) for the PortfolioAllocator (only built when `allocator_mode != "off"`) [A18]. config_auditor C5 L516 [A02]. config_integrity `CapsConfigDriftCheck.run` L115 to L116: **raw YAML**, compared with the hard-coded `CAPS_EXPECTED_MAX_OPEN = 5` (L71) [A20]. system_manager `_effective_caps` L145 to L146 [A15]. DASH risk_capital L61; trading.py L155; capacity L138; config_view L414, L605; controls L200, L299; operations L59; strategy_tower L122. daily_trade_review L1245. | A09, A18, A02, A20, A15 | |
| risk.max_daily_trades | 272 | 10 | int; req.; `>= 1` (L750) | main.py L2900 (L150, L195) [A09]. config_integrity L117 vs `CAPS_EXPECTED_MAX_DAILY = 10` (L72) [A20]. system_manager L146. DASH capacity L136; config_view L417, L609; controls L198, L298; operations L58. daily_trade_review L1246. | A09, A20, A15 | |
| risk.max_open_delivery_positions | 283 | 3 | `Optional[int]`; req.; null rejected; `>= 1` (L776, L831 to L846) | main.py L2918 (L166 default None, L204, L334) [A09]. DASH capacity L184; config_view L415, L605. | A09, A15 | |
| risk.max_daily_delivery_trades | 284 | 5 | as above (L777) | main.py L2919 (L167, L205, L336) [A09]. DASH capacity L188; config_view L418, L609. | A09, A15 | |
| risk.one_trade_per_symbol_direction_per_day | 302 | true | bool; default **False** (L784) | main.py L2901 → RiskEngine (L180 default False, L203). signals/signal_processor.py `_enforce_one_trade_per_symbol_direction` L834 reads the **private** `self._risk._one_trade_per_symbol_direction` with getattr(False) [A06]. DASH config_view L814. | A09, A06, A15 | The loader default differs from the file value. |
| risk.max_sector_exposure_pct | 313 | 0.40 | float; req.; `0 < x <= 1` (L785, L848 to L853) | main.py L2902 (L151, L196) [A09]. DASH capacity L228; config_view L621. daily_trade_review L1249. | A09, A15 | Enforcement depends on `sector_cap_mode`. |
| risk.delivery_max_sector_exposure_pct | 314 | 0.40 | `Optional[float]`; req.; null rejected; `0 < x <= 1` (L799, L855 to L867) | main.py L2923 (L189, L199, L331) [A09]. DASH config_view L622. | A09, A15 | |
| risk.max_consecutive_losses | 315 | 4 | int; req.; `>= 1` (L786) | main.py L2903 (L152, L197) [A09]. DASH risk_capital L52; capacity L167; config_view L646. daily_trade_review L1247. scripts/revert_temp_config.py L38 to L45: a text pattern; `prod_value` "4" [A02]. | A09, A15, A02 | |
| risk.daily_loss_limit_pct | 316 | 0.03 | float; req.; `0 < x <= 1` (L787, L848 to L853) | main.py L2727 → `FundManager(daily_loss_limit_pct=)` (L304 default 0.03; check L329 to L332; post-close breach L1342 to L1353) [A09]. main.py L2904 → RiskEngine (L153, L198) [A09]. config_auditor C1 L426, C5, F registry L178 to L179 [A02]. system_manager L263 [A15]. DASH risk_capital L32, L276; capacity L140; config_view L436, L613; controls L192, L301; operations L61. daily_trade_review L1248. revert_temp_config L47 to L54: a text pattern; `prod_value` "0.05" [A02]. | A09, A02, A15 | Read by two runtime components: the pre-trade gate and the post-close breach. `revert_temp_config`'s "prod" value 0.05 differs from the file value 0.03 (see 3.4). DASH controls.py L125 to L127 does not read this key: it tests whether the running process reported a limit in its control-plane response. |
| risk.delivery_daily_loss_limit_pct | 317 | 0.03 | `Optional[float]`; req.; null rejected; `0 < x <= 1` (L800) | main.py L2924 (L190, L200, L329) [A09]. DASH risk_capital L277; config_view L437, L613; controls L193. | A09, A15 | Pre-trade gate only. The FundManager breach uses only the global key (YAML L309 to L312). |
| risk.sector_cap_mode | 322 | observe | str; "observe"; one of {observe, enforce} (L815, L869 to L874) | main.py L2911 → RiskEngine (L174, L202: any other value becomes "observe") [A09]. DASH config_view L811. | A09, A15 | |
| risk.sector_unknown_alert_pct | 323 | 0.20 | float; 0.20; `0 <= x <= 1` (L816, L876 to L881) | main.py L3086 → `OrderPlacer(sector_unknown_alert_pct=)` (order_placer L595 default 0.20, L640) [A10]. DASH config_view L819. | A10, A15 | |
| risk.daily_loss_include_unrealized | 324 | false | bool; False (L806) | main.py L2906 (L170, L201; gate L687 to L718) [A09]. DASH config_view L817. | A09, A15 | |
| risk.price_drift_threshold | 325 | 0.005 | float; 0.005 (L807); no validator | **Not passed by main.py**: the `OrderPlacer(...)` call at L3061 to L3087 has no such argument, so the ctor default 0.005 applies (order_placer L585, L668). DASH config_view L650. | A15 | The YAML value is not the source of the runtime value. HISTORICAL: integrity_audit_2026.md L3737. |

### 2.13 `webhook` (YAML L327; `WebhookConfig` L617 to L642; required section, L2002)

`WebhookReceiver` receives `config=app_config` (main.py L3410). `__init__` resolves `getattr(config, "webhook", None)` and falls back to `config.system.webhook` (signals/webhook_receiver.py L171 to L175). INTERPRETATION: `AppConfig` has no `webhook` attribute, so production takes the fallback.

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| webhook.bind_host | 328 | not reproduced (an all-interfaces bind address, per the L328 comment) | str; req. (L619; the comment there names a loopback default that does not exist in the schema) | main.py L3992 → `waitress.serve(host=)` thread (L3988 to L4000) [A06, A17] | A06, A17 | The YAML comment at L332 to L334 says the bind "relies on require_hmac=true". L336 sets require_hmac false. |
| webhook.bind_port | 335 | 5000 | int; req. (L620); no range check | main.py L3993 (serve), L4004 (self-check URL), L4210 (interactive print) [A06, A01] | A06, A01 | Hard-coded 5000: scripts/preflight/checks/signals.py L17 `WEBHOOK_HEALTH_URL` [A20]; scripts/load_test_signals.py L52 [A19]. |
| webhook.require_hmac | 336 | false | bool; req. (L621) | webhook_receiver `__init__` L176 getattr(False) → `_require_hmac` (L200); construction refuses to proceed when it is true and there is no secret (L177 to L182); the token fallback is disabled when true (`WebhookReceiver._authenticate` L343 to L349) [A06] | A06 | |
| webhook.dedup_window_seconds | 337 | 300 | int; 300 (L622); no validator | webhook_receiver `__init__` L233 getattr(300), **floored by `max(60, …)`** (L236); TTL cache (L237); fingerprint bucket (L952) [A06]. DASH capacity L288. | A06, A15 | |
| webhook.per_ip_rate_limit_enabled | 340 | true | bool; True (L626) | webhook_receiver L241 getattr(True) [A06]. DASH capacity L284. | A06, A15 | |
| webhook.per_ip_burst | 341 | 60 | int; 60; `>= 1` (L627, L630 to L635) | webhook_receiver L243 `int(getattr(…, 60) or 60)` [A06]. DASH capacity L282. | A06, A15 | |
| webhook.per_ip_refill_per_sec | 342 | 5.0 | float; 5.0; `>= 0` (L628, L637 to L642) | webhook_receiver L244 `float(getattr(…, 5.0) or 5.0)` [A06]. DASH capacity L283. | A06, A15 | INTERPRETATION: a configured 0.0 (allowed by the loader) becomes 5.0 at the consumer. |

### 2.14 `signal_processor` (YAML L344; `SignalProcessorConfig` L564 to L614; required section, L2003)

Runtime reads go through main.py L3574 to L3622 → `SignalProcessor(...)` (signals/signal_processor.py `__init__` L173 to L267) [A06].

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| signal_processor.worker_count | 345 | 5 | int; req.; 1 to 50 (L566, L588 to L593) | main.py L3590 (ctor default 5 L173; `max(1, …)` L220) [A06] | A06 | |
| signal_processor.drain_poll_sec | 346 | 0.1 | float; req.; `> 0` (L567, L595 to L600) | main.py L3591 (L174, L221; `queue.get(timeout=)` L385) [A06] | A06 | |
| signal_processor.pipeline_timeout_sec | 347 | 30 | int; req.; `>= 1` (L568, L602 to L607) | **No consumer found by grep.** It is not passed at main.py L3575 to L3622, and `SignalProcessor` has no such parameter. | — | HISTORICAL: integrity_audit_2026.md L3731 and L3747 to L3749 report the same finding. |
| (signal_processor.atr_fallback_mode) | — | **absent** | `Literal["WARN","HALT"]`; "WARN" (L572) | main.py L3593 (ctor L177, L224; HALT checks L1803, L1914) [A06] | A06 | The key is read by code but absent from the YAML, so the default "WARN" applies. |
| signal_processor.tgt_min_pct | 348 | 0.003 | float; 0.003; `0 < x < 1` (L575, L609 to L614) | main.py L3594 (L178, L225; comparison L1945) [A06] | A06 | |
| signal_processor.min_gap_between_entries_sec | 350 | 20 | float; default **0.0** (L581); no validator | main.py L3596 getattr(0.0) → `EntryThrottle(min_gap_sec=)` (L179, L264; signals/entry_throttle.py L49 `max(0.0, …)`) [A06]. DASH capacity L207. | A06, A15 | The loader and getattr defaults (0.0 = off) differ from the file value. |
| signal_processor.entry_burst_window_sec | 351 | 60 | float; 60.0 (L582) | main.py L3597 getattr(60.0) (L180, L265; entry_throttle L50 `max(0.0, float(… or 60.0))`) [A06]. DASH capacity L198 (`or 60`). | A06, A15 | |
| signal_processor.entry_burst_max | 352 | 3 | int; default **0** (L583) | main.py L3598 getattr(0) (L181, L266; entry_throttle L51 `max(0, …)`) [A06]. DASH capacity L197. | A06, A15 | The defaults (0 = off) differ from the file value. |
| signal_processor.per_symbol_cooldown_sec | 353 | 300 | float; default **0.0** (L586) | main.py L3599 getattr(0.0) (L182, L267; signals/entry_throttle.py L46, L52 `max(0.0, …)`) [A06]. DASH capacity L208. | A06, A15 | The defaults differ from the file value. |

### 2.15 `kill_switch` (YAML L355; `KillSwitchConfig` L734 to L744; required section, L2001)

| Key path | YAML L | File value | Loader | Consumers | Owner | Notes |
|---|---|---|---|---|---|---|
| kill_switch.api_failure_threshold | 356 | 3 | int; req.; `>= 1` (L736, L739 to L744) | main.py L2247 → `KillSwitch(api_failure_threshold=)` (capital/kill_switch.py L259 default 3, L273; use L864) [A13]. DASH capacity L246. | A13, A15 | scripts/clear_kill_switch.py L57 and scripts/system_manager.py L955 build `KillSwitch(store, EventBus(), log)` without config, so the ctor defaults apply there. |
| kill_switch.enable_auto_trip | 357 | true | bool; req. (L737) | main.py L2248 (L260 default True, L274) [A13]. DASH capacity L247 get(True). | A13, A15 | |

---

## 3. Exceptions

### 3.1 Keys with no consumer outside `core/config_loader.py` (no consumer found by grep)

| Key | YAML L | Comment |
|---|---|---|
| broker.fallback | 23 | Only generic whole-tree display. |
| broker.fallback_enabled | 24 | Docstring mentions only (broker/angelone_adapter.py L12, L26). |
| broker.multi_account_mode | 25 | — |
| signal_processor.pipeline_timeout_sec | 347 | Validated `>= 1` by the loader but never read. |
| capital.leverage_safety.min_allowed | 213 | **Used by the loader itself** as the lower bound for every `leverage_map` value (L400). No other reader. |
| capital.leverage_safety.max_allowed | 214 | As above (L401). |

**Keys read only for display, logging or audit, with no runtime trading-path consumer:** broker.primary; capital.slm_margin_buffer_pct; position_sizing.min_tick_size; position_sizing.max_single_order_qty; position_sizing.dynamic_by_winrate (log only); position_sizing.min_multiplier; position_sizing.max_multiplier (auditor only); risk.price_drift_threshold.

### 3.2 Keys read by code but absent from the YAML (the loader default applies)

| Key | Default | Readers |
|---|---|---|
| position_sizing.flat_value_rs | None (L480) | main.py L2856, L2877, L2879; config_integrity L231; cron_officer L511. Only acts when `enabled=false`. |
| signal_processor.atr_fallback_mode | "WARN" (L572) | main.py L3593 |

Also read by code, though not config keys: the private attributes `risk_engine._max_open`, read with getattr(5) at main.py L3639, and `risk_engine._one_trade_per_symbol_direction`, read with getattr(False) at signal_processor L834.

### 3.3 YAML values that the loader or a consumer overrides, transforms or ignores

| Key | What happens | Where | Effect at the baseline file values (INTERPRETATION) |
|---|---|---|---|
| webhook.dedup_window_seconds | floored to 60 | webhook_receiver L236 | none (300) |
| webhook.per_ip_refill_per_sec | `or 5.0`: a value of 0.0 becomes 5.0 | webhook_receiver L244 | none (5.0) |
| webhook.per_ip_burst | `or 60` | webhook_receiver L243 | none; 0 is impossible because of the loader's `>= 1` |
| signal_processor.worker_count | `max(1, …)` | signal_processor L220 | none |
| signal_processor.min_gap_between_entries_sec | `max(0.0, float(x or 0.0))`: a negative value becomes 0.0 (off) | entry_throttle L49 | none (20) |
| signal_processor.entry_burst_window_sec | `max(0.0, float(x or 60.0))`: a configured 0 becomes 60.0; a negative value becomes 0.0 | entry_throttle L50 | none (60) |
| signal_processor.entry_burst_max | `max(0, int(x or 0))`: a negative value becomes 0 (off) | entry_throttle L51 | none (3) |
| signal_processor.per_symbol_cooldown_sec | `max(0.0, float(x or 0.0))`: a negative value becomes 0.0 (off) | entry_throttle L52 | none (300) |
| risk.sector_cap_mode | an invalid value becomes "observe" | risk_engine L202 | none; the loader already validates |
| capital.intraday_bucket_pct, capital.positional_bucket_pct | when `conditional_allocation_enabled` is true, intraday_bucket_pct is ignored (intraday = 1 − positional when both books are active; 1.0 when delivery is not active, including when neither book is active; 0.0 when only delivery is active); positional_bucket_pct is used only when both books are active | fund_manager L112 to L146, called from main.py L2702 to L2708 | none (flag false) |
| capital.slm_margin_buffer_pct | not wired; the ctor default is used | main.py L2718 to L2736; fund_manager L309 | none (default 0.05 = file value) |
| position_sizing.min_tick_size | not wired; ctor default | main.py L2840 to L2863; position_sizer L164 | none (0.05 = 0.05) |
| position_sizing.max_single_order_qty | not wired; ctor default | as above; position_sizer L165 | none (10000 = 10000) |
| risk.price_drift_threshold | not wired; ctor default | main.py L3061 to L3087; order_placer L585 | none (0.005 = 0.005) |
| signal_processor.pipeline_timeout_sec | never read | — | the "hard per-signal deadline" (YAML L347 comment) has no implementing consumer |
| position_sizing.dynamic_by_winrate, min_multiplier, max_multiplier | no behavioural effect (no perf weights are wired) | main.py L3575 to L3622; signal_processor L1120, L2116, L2458 | perf_weight is always 1.0 |
| capital.emergency_exit_buffer_pct | bypassed by the constant 0.01 on three runtime exit paths and in one real-API test script | eod_squareoff L1543; order_reconciler L2324; structure_exit_manager L438; scripts/t2_cnc_gtt_realtest.py L265, L275 [A19] | none (0.01 = 0.01); a change to the YAML value would not reach these paths |
| capital.sl_limit_offset_pct | bypassed by the constant 0.005 in crash-recovery SL placement | order_reconciler L3297, L3314 | as above |
| broker.primary | not used to choose the broker; "zerodha" is hard-coded | product_resolver L95; zerodha_adapter L587, L1586; main.py L3293, L2561 to L2572 | none ("zerodha") |

**Total: 22 distinct keys** (the two bucket keys, the three multiplier keys and the four entry-throttle keys are counted separately). At the baseline file values none of these rows changes the value that results. The loader has no validators on the four entry-throttle keys (L581 to L586), so a negative value passes the loader and is floored by `EntryThrottle`.

### 3.4 Settings read differently in different places

| Setting | Difference |
|---|---|
| trading_hours.* (market_open, entry_start, entry_end, eod_squareoff, market_close) | The dashboard clock (`ops_dashboard/backend/services/freshness.py` L43 to L93) and the Entry Window and Market Session rows of `ops_dashboard/backend/services/capacity.py` `build_capacity` (L209 to L217) read a **copy** in `ops_dashboard/backend/config/gui_config.yaml` L61 to L69, not system_config. The freshness `in_entry_window` runs from entry_start to eod_squareoff (freshness.py L68), not to entry_end. |
| MIS square-off timing | It is built three times: loader validation with a literal poll of 5 (L131); main.py L3329 to L3337 with `eod_squareoff.poll_interval_sec`; the notifier's own instance (mis_squareoff_notifier L164 to L172, poll from main.py L3345). |
| clock.startup_max_skew_sec | Read in two places: time_authority `startup_max_sec` (main.py L375) and `startup_checks` `tolerance_sec` (L1572). |
| signal_queue backpressure | The receiver returns 503 at capacity × 0.80 (webhook_receiver L573). Pre-flight warns at a hard-coded 0.9 × capacity (preflight signals.py L78). |
| "delivery active" | main.py L2695 to L2698 requires delivery_enabled AND NOT force_intraday_only AND trade_type in {DELIVERY, BOTH}. The DASH `controls.py` L232 leaves out `delivery_enabled`. |
| force_intraday_only / trade_type defaults | Loader: True / "INTRADAY". Adapter, SignalProcessor and StrategyLoader ctors: False for force_intraday_only. cron_officer (L474 to L475) reads the raw YAML: True / "INTRADAY". The DASH readers read the snapshot first (loader defaults already applied) and the raw YAML only as a fallback (config_reader L33 to L52), so their own defaults matter only on that fallback: True for force_intraday_only (capacity L128, controls L229, operations L37); "INTRADAY" for trade_type at controls L230; no default at operations L38, where a missing value maps to the label "Intraday Only" (L42 to L43). |
| signal_queue.expiry_sec | YAML 600. `SignalProcessor` ctor default 60 (L175). The loader comment says "default 60" (L196) but the field is required. |
| mis_filter.ttl_days | YAML and loader 1; `MisLearnedBlocklist` ctor default 5 (mis_blocklist L68). |
| excluded_symbols | Receiver: through the model, case-insensitive, after alias resolution. daily_report: raw YAML, case-sensitive. |
| risk.max_open_positions / max_daily_trades | Pre-flight compares the raw YAML with hard-coded 5/10 (config_integrity L71 to L72, L115 to L118). |
| risk.daily_loss_limit_pct | `revert_temp_config` holds `prod_value` "0.05" (L51); the file value is 0.03. |
| leverage ceiling | Loader `leverage_safety.max_allowed` 10.0 against auditor G2 literal `> 10` (L697). Absolute cap 20.0 (L229). |
| market_open / market_close | The boot "market open now" check (main.py L2228 to L2232), `EodSquareoff.market_close` (L3312) and `TokenMonitor` (L3396 to L3397) use the regular-session strings directly. `MarketWindows` applies holidays and special sessions. Hard-coded 09:15/15:30/16:00 copies are listed in 2.2. |
| system_manager checks | Checks daily loss and position value against the global (intraday) keys only (L263, L279). |

### 3.5 Direct readers of `system_config.yaml` outside the loader

| Reader | Keys read | Owner |
|---|---|---|
| core/config_auditor.py `audit_app_config` L835 (`_safe_load_yaml` L850) | the raw `capital`, `position_sizing` and `risk` dicts, checked for deleted keys (L337 to L360; group B, pre-flight only) | A02 |
| ops_dashboard/backend/readers/config_reader.py `get_system_config` L45 to L52 | the whole tree, as a fallback when there is no snapshot for today | A15 |
| reports/daily_report.py `load_report_data` L145 to L149 | excluded_symbols | A15 |
| scripts/cron_officer.py `_strategy_status_payload` L471 to L475; `_tier_mode_line` L507 to L511 | trade_type, force_intraday_only; position_sizing.enabled, flat_value_rs | A16 |
| scripts/preflight/checks/config_integrity.py `CapsConfigDriftCheck` L105 to L118; `TierMultiplierModeCheck` L220 to L234; `ConfigYamlValidCheck` L88 (parse only) | risk.max_open_positions, max_daily_trades; position_sizing.enabled, tier_multipliers, flat_value_rs | A20 |
| scripts/revert_temp_config.py L33 to L54, L115 to L174 | text regexes for `max_consecutive_losses:` and `daily_loss_limit_pct:`; can rewrite the file with `--apply --confirm` | A02 |
| alerts/telegram_notifier.py L92 | alerts.telegram.enabled (outside this range) | A14 |
| File-level only (presence, hash, watch; no key reads): scripts/forward_shadow_record.py L84; scripts/premarket_healthcheck.py L55; utils/startup_checks.py L834; config_integrity L17; scripts/security_monitor.py L222; config/security.yaml L133 | — | A18, A20, A01, A17, A02 |

---

## 4. Totals

| Measure | Count |
|---|---|
| Leaf entries in L21 to L357 | **100** (98 scalars, 1 null `special_sessions`, 1 list `excluded_symbols`) |
| Leaves with at least one consumer outside the loader | **94** |
| … of which have a runtime (trading-path) consumer | **86** |
| … of which are read only for display, log or audit | **8** (see 3.1) |
| Leaves with no consumer outside the loader | **6** (4 read by nothing; 2 `leverage_safety` keys enforced only by the loader) |
| Schema keys read by code but absent from the YAML | **2** (flat_value_rs, atr_fallback_mode) |
| Keys whose YAML value is overridden, transformed, not wired or bypassed | **22** (see 3.3) |
| Loader defaults that differ from the file value (these would apply if the key were deleted) | **13**: service_window_end, mis_squareoff_cutoff, first_offset, second_offset, mis_filter.enabled, one_trade_per_symbol_direction_per_day, min_gap_between_entries_sec, entry_burst_max, per_symbol_cooldown_sec, force_intraday_only, delivery_enabled, trade_type, excluded_symbols (default `[]`: deleting the key would empty the exclusion list) |

HISTORICAL cross-check: docs/audit/integrity_audit_2026.md L3727 to L3749 (a key sweep on 01-Aug-2026) lists pipeline_timeout_sec, multi_account_mode, price_drift_threshold, max_single_order_qty, min_tick_size, dynamic_by_winrate and slm_margin_buffer_pct as dead or ineffective. That agrees with sections 3.1 and 3.3 at this baseline.
