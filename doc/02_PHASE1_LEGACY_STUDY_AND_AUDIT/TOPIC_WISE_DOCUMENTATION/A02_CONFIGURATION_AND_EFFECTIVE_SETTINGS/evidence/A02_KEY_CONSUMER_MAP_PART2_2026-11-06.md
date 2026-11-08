# A02 evidence: Key-to-consumer map, part 2: `config/system_config.yaml` from line 359, and the smaller YAML files

**Status:** DRAFT — evidence for the A02 STUDY, for ChatGPT's review
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06.
**Purpose and scope:** This file maps every leaf key of `config/system_config.yaml` from line 359 to line 753, and of `config/broker_limits.yaml`, `broker_costs.yaml`, `slippage_model.yaml`, `security.yaml`, `preflight.yaml` and `expected_managers.yaml`, to how it is loaded, its loader field and default, the code that reads it and the owner topic of that code. It also records the cross-cutting results (keys without a functional consumer, fields read but absent from the files, values overridden or ignored, settings read differently or duplicated, and direct readers) and the totals. It supports the STUDY's key-to-consumer map and its account of the effective settings.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

## Scope, method and conventions

- **Scope:** `config/system_config.yaml` L359 to L753 (sections `eod_squareoff` to `scanner_check_delay_sec`), plus `config/broker_limits.yaml`, `config/broker_costs.yaml`, `config/slippage_model.yaml`, `config/security.yaml`, `config/preflight.yaml` and `config/expected_managers.yaml`. Part 1 of the key-to-consumer map covers `system_config.yaml` L1 to L358.
- **Method:** The leaf keys and their lines were listed by a script that parses the YAML text with `yaml.safe_load` / `yaml.compose`. A second script maps each leaf to its pydantic field in `core/config_loader.py`, parsing the loader with `ast`. Enclosing function names came from an `ast` script. Consumers were found with `git grep` over non-test code (`tests/` and `docs/` excluded; `ops_dashboard/tests` ignored), and each hit was followed to the object it reads from. Nothing in the clone was run or imported; the scripts are kept outside the clone.
- **Labels:** Every statement about code or file content is **FACT** at the cited lines unless it is marked INTERPRETATION, HISTORICAL, UNKNOWN / NOT ESTABLISHED or OPEN QUESTION. A YAML value is the *file value at the baseline*. It is not proof that the value was in force: what ran on the VM is **UNKNOWN / NOT ESTABLISHED**.
- **Consumer classes used in the tables:**
  - **F** — functional consumer: code uses the value to change behaviour.
  - **D** — display or report only (ops dashboard, reports, boot log).
  - **P** — paper-only path: marked, not traced (RULES 7).
  - **N** — no functional consumer: no code uses the value to change behaviour, apart from loader validation and the generic walkers below. Display-only, assign-only and read-then-skipped reads found by grep are noted in the row.
- **Generic whole-config consumers** (they touch every key; they are not repeated per row):
  - `core/config_validator.py` `register_all_from_app_config` L144-183 walks `system`, `broker_costs`, `broker_limits` and `slippage`. It is called at `main.py` `_main_locked` L2205. No non-test module calls `config_validator.get()` (grep shows only the docstring at L31), so `validate_all(strict=False)` at `main.py` L4164 sees every key as "unaccessed" and only logs a warning (INTERPRETATION from L240-254).
  - `core/config_snapshotter.py` persists `AppConfig.model_dump` (docstring L16), with redaction of populated secret keys (L46-80).
  - `ops_dashboard/backend/readers/config_reader.py` `get_system_config` L28-53 reads the snapshot first and falls back to a **direct** `system_config.yaml` read at L45-52. `ops_dashboard/backend/services/config_view.py` `_categories` L656-700 flattens every remaining key ("advanced"). `ops_dashboard/backend/services/audit.py` L69-94 classifies `system.<section>` paths.
- **Owner topic codes** come from the Master System Investigation Index, section 3 and Appendix A:
  - A01: `main.py` wiring, `utils/startup_checks.py`
  - A04: `broker/`
  - A05: `data/live_feed.py`, `scripts/fetch_fno_ban.py`
  - A06: `signals/`
  - A07: `screening/` except retest
  - A08: `sr_detector/`, `screening/retest_monitor.py`, `scripts/sr_level_export.py`
  - A09: `capital/`
  - A10: `orders/order_placer.py`
  - A11: `orders/smart_tgt_manager.py`, `tgt_retry_manager.py`, `shadow_tracker.py`, `structure_exit_manager.py`, `slippage_recorder.py`
  - A12: `orders/eod_squareoff.py`, `mis_autosquareoff.py`, `order_reconciler.py`, `core/mis_squareoff_timing.py`, EOD scripts
  - A13: `capital/kill_switch.py`
  - A14: `alerts/`, `scripts/alert_watcher.py`
  - A15: `reports/`, `ops_dashboard/`, `core/effect_telemetry.py`, `scripts/monitoring_canary.py`, `liveness_probe.py`, `system_manager.py`
  - A16: `scripts/cron_officer.py`
  - A17: `scripts/security_monitor.py`, `copy_gate.py`, `request_copy.py`, `approve_ssh_keys.py`
  - A18: `regime/`, `v3_chain/`, `allocation/`, `scripts/v3_shadow_soak_report.py`, `scripts/forward_shadow_record.py`
  - A20: `scripts/preflight/`
  - A02 owns `core/config_*` and `scripts/revert_temp_config.py`.
- "main.py `_main_locked`" is shortened to **`M`** in the tables, for example `M` L3311.

## 1. How each file or section is loaded

| File / section | Loaded by | Object path | Required? | Notes |
|---|---|---|---|---|
| `system_config.yaml` (whole) | `core/config_loader.py` `load_all` L2457-2516 (`_CONFIG_FILES` L2441-2450), `yaml.safe_load` L2494, `SystemConfig.model_validate` L2507 | `AppConfig.system` (L2426) | file required (L2483-2488) | Every model is `extra="forbid"`. The `SystemConfig` model validator L2056-2086 runs `core/config_auditor.audit_system_config` and raises on BLOCK. |
| sections `eod_squareoff`, `alerts`, `logging`, `order_reconciler`, `shadow_tracker`, `smart_tgt`, `entry_gate`, `paper`, `drift_handler` | same | `SystemConfig.<section>` L2004-2007, L2011, L2018-2021 | **required** (no default) | — |
| sections `eod_reconcile`, `eod_cleanup`, `tgt_retry`, `sr_detector`, `regime`, `portfolio_allocator`, `v3_chain`, `watchlist`, `structure_exit`, `circuit_breaker`, `strategy_circuit_breaker`, `live_feed`, `fno_ban`; top-level `slippage_bands`, `scanner_check_delay_sec` | same | `SystemConfig.<section>` L2008-2017, L2022-2029 | optional (model default) | — |
| `broker_limits.yaml` | same loader | `AppConfig.broker_limits` → `BrokerLimitsConfig` L2245-2256 | file required | `rate_limit_backoff` is optional (default factory L2254). |
| `broker_costs.yaml` | same loader | `AppConfig.broker_costs` → `BrokerCostsConfig` L2131-2168 | file required | Also read **directly** by `reports/daily_report.py` and `ops_dashboard` (section 3.6). |
| `slippage_model.yaml` | same loader | `AppConfig.slippage` → `SlippageConfig` L2269-2272 | file required | The only functional consumer is paper-only (section 2.27). |
| `security.yaml` | **not loaded centrally** (header L3-6). Read directly by `scripts/security_monitor.py` `SecConfig.load` L150-183, `scripts/copy_gate.py` `CopyConfig.load` L79-98, `scripts/preflight/checks/security.py` `_load_security_yaml` L36-38, and indirectly by `scripts/system_manager.py` `security_check` L823 and `scripts/approve_ssh_keys.py` L79 (both through `SecConfig.load`) | dataclasses `SecConfig` L108-148 / `CopyConfig` L68-77 | file optional: defaults on missing or bad file (L177-180; L94-97) | No schema validation. Unknown keys are ignored (only listed names are copied, L157-170, L87-93). |
| `preflight.yaml` | **not loaded centrally** (header L3-8). Read by `scripts/preflight/checks/broker.py` `_min_broker_cash_rs` L44-62 | plain dict | optional: defaults to `MIN_BROKER_CASH_RS_DEFAULT` = 2000.0 (L41) | — |
| `expected_managers.yaml` | **not loaded centrally** (header L22-23). Read by `core/effect_telemetry.py` `_load_registry` L129-142 (`yaml.safe_load`, path `config/expected_managers.yaml` L63, cwd-relative) | list of dicts | not validated | The header says the consumer is "Phase B — NOT YET BUILT" (L22-23, HISTORICAL). At the baseline `core/effect_telemetry.py` exists and `main.py` calls it (L2585, L4244, L1665). |

## 2. Leaf-key tables

Loader cells give `Model.field Lnnn · type · default · constraint`. "REQ" means the field is required with no default. Validator lines are the `def` line of the validator.

### 2.1 `eod_squareoff` (L359) — loader `EodSquareoffConfig` L645-731 — 8 leaves

| Key | L | File value | Loader | Consumers (file:function:line — how read; default at read; transform) | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `inter_order_delay_ms` | 360 | 500 | L647 · int · REQ · 0..5000 (L671) | `M` L3311 → `orders/eod_squareoff.py:EodSquareoff.__init__:L147` (ctor default 500; **ms→s** `/1000.0`; sleeps at L1270-1271, L1379-1380, L1507-1508, L1719-1720). `M` L3367-3368 (`/1000.0`) → `orders/mis_autosquareoff.py:MisAutoSquareoff.__init__:L293` (ctor default 0.5 s; sleep L914-915) | A12 (A01 wiring) | F. The same value feeds two mechanisms. |
| `poll_interval_sec` | 361 | 5 | L648 · int · REQ · ≥1 (L678) | `M` L4096 → `EodSquareoff.start_polling:L290` (param default 5). `M` L3334 → `core/mis_squareoff_timing.py:MisSquareoffTiming.build:L125-136` (must be a positive int and ≤ `trading_hours.mis_squareoff_margin_sec`, else raises). `M` L3345 → `alerts/mis_squareoff_notifier.py:__init__:L152/L169`, `start_polling:L264` | A12, A14 | F. Three mechanisms share one key. The error text at `mis_squareoff_timing.py` L127 names `mis_squareoff.poll_interval_sec`, a key that does not exist. |
| `auto_resume_kill_switch` | 362 | true | L649 · bool · REQ · none | none. Grep finds only the loader, the YAML and tests; `M` L3300-3319 does not pass it. `EodSquareoff._fire:L536-544` resumes the kill switch whenever `_we_set_soft_kill` is true, with no flag check | A12/A13 | **N.** The value is ignored and the behaviour is unconditional. |
| `exit_protocol` | 363 | "LIMIT_THEN_MARKET" | L651 · str · "MARKET" · {MARKET, LIMIT_THEN_MARKET} (L685) | `M` L3316 → `EodSquareoff.__init__:L152` (ctor default "MARKET") → `_exit_open_positions:L1135, L1275` | A12 | F. The loader and ctor defaults ("MARKET") differ from the file value. |
| `limit_aggressive_pct` | 364 | 0.01 | L652 · float · 0.01 · (0, 0.10] (L693) | `M` L3317 → `EodSquareoff.__init__:L153` → `_exit_open_positions:L1280/L1284` (`ltp*(1∓pct)`, **fraction**) | A12 | F. Not passed to `MisAutoSquareoff`. |
| `limit_grace_sec` | 365 | 120 | L653 · float · 120.0 · [0, 300] (L702) | `M` L3318 → `EodSquareoff.__init__:L154` → `_exit_open_positions:L1390-1393` (sleep). `M` L3366 → `MisAutoSquareoff.__init__:L292` (**`int()` cast**; ctor default 120; clipped to the remaining room in `effective_grace_sec` L1277-1279) | A12 | F. Float in one consumer, int in the other. |
| `mis_pass_1_market_protection_percent` | 376 | 1.5 | L666 · float · 1.5 · [0.1, 10.0] (L714) | `M` L3372-3373 → `MisAutoSquareoff.__init__:L298` (float; ctor default 1.5) → order kwarg `market_protection_percent` L895 | A12 | F. **Percent** unit. A second bound sits at the adapter chokepoint (loader docstring L721-723; `broker/zerodha_adapter.py` comments L239, L526). |
| `mis_pass_2_market_protection_percent` | 377 | 2.5 | L667 · float · 2.5 · [0.1, 10.0] (L714) | `M` L3374-3375 → `MisAutoSquareoff.__init__:L299` | A12 | F. As above. |

### 2.2 `alerts` (L379) — loader `AlertsConfig` L1100-1123, `TelegramConfig` L978-1003, `TelegramChannelConfig` L971-975, `EmailFallbackConfig` L952-968, `SmtpConfig` L884-949 — 36 leaves

| Key | L | File value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `failed_alerts_log_path` | 380 | "logs/failed_alerts.log" | L1102 · str · REQ | `M` L2631 → `alerts/telegram_notifier.py:TelegramNotifier.__init__:L237` (parent mkdir L264). The 33 `from_env` / `from_config` call sites in 31 files (section 3.3 item 9) use the ctor default "logs/failed_alerts.log" (L200) | A14 | F. |
| `sentinel_dir` | 381 | "data_store" | L1103 · str · REQ | `M` L2632 → `TelegramNotifier.__init__:L238` (used L475, L498). `scripts/alert_watcher.py:run_once:L501`. `scripts/monitoring_canary.py:run_canary:L262`. `scripts/cron_officer.py:_resolve_sentinel_dir:L781` (own `load_all()`). `scripts/liveness_probe.py:main:L294` (fallback `Path("data_store")` L296). `scripts/system_manager.py:main:L1340` (`getattr` default "data_store") | A14, A15, A16 | F. Hard-coded `data_store` sentinel dirs bypass the key: `main.py:_alert_invalid_strategy_configs:L354`; `from_env` notifiers (ctor default L201); `scripts/cron_watchdog.py` L67; `scripts/gemini_log_review.py` L275; `cron_officer.py` default L154. |
| `watcher_max_attempts` | 382 | 5 | L1104 · int · REQ · ≥1 (L1120) | `alert_watcher.py:run_once:L502` (compared at L609, L661, L688) | A14 | F. |
| `alert_digest_threshold` | 383 | 3 | L1105 · int · 3 | `alert_watcher.py:run_once:L506` (`getattr` default 3) → L554 `len(to_send) > threshold` | A14 | F. |
| `watcher_lock_path` | 384 | "data_store/alert_watcher.lock" | L1106 · str · REQ | `alert_watcher.py:main:L806` | A14 | F. |
| `watcher_log_path` | 385 | "logs/alert_watcher.log" | L1107 · str · REQ | `alert_watcher.py:main:L803` | A14 | F. |
| `telegram.enabled` | 387 | true | L980 · bool · True | `M` L2636 → `TelegramNotifier(enabled=)` L245. **Direct YAML read** `telegram_notifier.py:_read_telegram_enabled:L81-102` (fail-open True on any error), called by `from_env:L296` | A14 | F. Read two ways (section 3.4). |
| `telegram.bot_token_env` | 388 | "TELEGRAM_BOT_TOKEN" (env-var name) | L981 · str · "TELEGRAM_BOT_TOKEN" | `M` L2629 `os.environ[tg_cfg.bot_token_env]` (index, no default) | A14 | F. The literal env-var name is duplicated in `from_env:L288`, `monitoring_canary.py:run_canary:L265` and other files (section 3.5). |
| `telegram.telegram_alerts_in_paper_mode` | 389 | true | L982 · bool · True | `M` L2635 → `send_in_paper_mode` (`TelegramNotifier` L244; gates at L468, L541, L576 only when `paper_mode`) | A14 | **P** (paper-only effect; not traced). The ctor default is False (L209). |
| `telegram.max_retries` | 390 | 3 | L986 · int · 3 | `M` L2637 → `__init__:L241` → `_post_with_retry:L710, L734, L740` | A14 | F. Main app only. `from_env` notifiers use the ctor default 3. |
| `telegram.retry_backoff_seconds` | 391 | 2.0 | L987 · float · 2.0 | `M` L2638 → `__init__:L242` → sleeps L712, L742 | A14 | F. As above (ctor default 2.0). |
| `telegram.rate_limit_per_minute` | 392 | 20 | L988 · int · 20 | `M` L2639 → `__init__:L247` (`_SlidingWindowRateLimiter`) | A14 | F. As above (ctor default 20). |
| `telegram.send_deadline_seconds` | 393 | 8 | L996 · Optional[float] · 8.0 | `M` L2640 → `__init__:L254-256` → `_send_to_all_chats` deadline L613-614 | A14 | F. As above (ctor default 8.0). |
| `telegram.channels[0].chat_id_env` | 416 | "TELEGRAM_CHANNEL_PRIMARY" (name) | L973 · str · REQ; list non-empty (L998-1003) | `M` L2620-2627 → `ChannelConfig` → `_send_to_all_chats:L622` `os.environ.get` | A14 | F. The name is also hard-coded in `from_env:L289`. |
| `telegram.channels[0].label` | 417 | "Primary Alert Channel" | L974 · str · REQ | `M` L2623 → log text L624-626 | A14 | F (log text). |
| `telegram.channels[0].enabled` | 418 | true | L975 · bool · False | `M` L2624 → `_send_to_all_chats:L620` | A14 | F. |
| `telegram.channels[1].chat_id_env` | 419 | "TELEGRAM_CHANNEL_SECONDARY" (name) | L973 | same as [0] | A14 | F. The YAML comment L409-412 warns about the shared deadline (HISTORICAL). |
| `telegram.channels[1].label` | 420 | "Secondary Alert Channel" | L974 | same | A14 | F. |
| `telegram.channels[1].enabled` | 421 | false | L975 | same → skipped at L620 | A14 | F. |
| `telegram.personal_chat_id_env` | 422 | "TELEGRAM_PERSONAL_CHAT_ID" (name) | L984 · str · "" | none (grep: loader comment and notifier docstring L222 only) | A14 | **N.** |
| `telegram.whitelist_only` | 423 | true | L985 · bool · True | none (loader only) | A14 | **N.** |
| `email_fallback.enabled` | 441 | true | L955 · bool · False | `M` L2641 passes the whole block → `telegram_notifier.py:_send_email_fallback:L802` (`getattr` default False). Callers: `_handle_critical:L523`; `M` L3346 (the MIS notifier `send_email` lambda) | A14 | F. `from_env` notifiers have `email_fallback_config=None` → returns False at L802. The YAML comment L425-440 says the env vars are absent on the VM: HISTORICAL claim, **UNKNOWN**. |
| `email_fallback.smtp_host` | 442 | "smtp.gmail.com" | L956 · str · same | `_send_email_fallback:L830` (`getattr` default "smtp.gmail.com") | A14 | F. Duplicates `smtp.host`. The SMTP timeout is a literal 15 s (L834). |
| `email_fallback.smtp_port` | 443 | 587 | L957 · int · 587 · 1..65535 (L965) | `_send_email_fallback:L831` (`int(getattr(…,587))`) | A14 | F. Duplicates `smtp.port`. |
| `email_fallback.from_addr_env` | 444 | "ALERT_EMAIL_USER" (name) | L958 | `_send_email_fallback:L805` `os.environ.get` | A14 | F. |
| `email_fallback.password_env` | 445 | "ALERT_EMAIL_PASSWORD" (name) | L959 | `_send_email_fallback:L806` | A14 | F. |
| `email_fallback.to_addr_env` | 446 | "ALERT_EMAIL_TO" (name) | L960 | `_send_email_fallback:L807` | A14 | F. |
| `email_fallback.use_tls` | 447 | true | L961 · bool · True | `_send_email_fallback:L832` | A14 | F. |
| `smtp.host` | 449 | "smtp.gmail.com" | L886 · str · REQ | `alert_watcher.py:_send_email:L282/L287`; `run_once` digest L572/L578; `monitoring_canary.py:check_email_path:L80/L83` | A14, A15 | F. |
| `smtp.port` | 450 | 587 | L887 · int · REQ · 1..65535 (L904) | same sites | A14, A15 | F. |
| `smtp.use_tls` | 451 | true | L888 · bool · REQ | `_send_email:L281`; `run_once:L571`; `check_email_path:L79` (`getattr` default True) | A14, A15 | F. |
| `smtp.username` | 452 | not reproduced (e-mail address) | L889 · str · REQ | `_send_email:L296` `server.login`; `run_once:L583`; `check_email_path:L85` | A14, A15 | F. The value is committed in the YAML and is not a redaction marker key in `config_snapshotter` (L49). |
| `smtp.password_env` | 459 | "ALERT_SMTP_PASSWORD" (name) | L894 · str · ""; model validator L924-933 (`password` or `password_env` required) | `SmtpConfig.resolved_password:L935-949` (raises if the env var is empty), called at `_send_email:L295`, `run_once:L582`, `check_email_path:L85` | A14, A15 | F. Whether the env var was set on the VM is UNKNOWN. |
| `smtp.from_address` | 460 | not reproduced | L898 · str · REQ | `_send_email:L278, L297`; `run_once:L568, L584` | A14 | F. |
| `smtp.to_addresses` | 461 | not reproduced (1 address) | L899 · list[str] · REQ · non-empty (L918) | same sites | A14 | F. |
| `smtp.timeout_sec` | 463 | 30 | L900 · int · REQ · ≥1 (L911) | `_send_email:L282/L287`; `run_once:L573/L579`; `check_email_path:L80/L83` | A14, A15 | F. |

### 2.3 `logging` (L465) — `LoggingConfig` L1126-1136 — 1 leaf

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `min_free_disk_gb` | 466 | 2.0 | L1129 · float · REQ · ≥0.1 (L1133) | `M` L2473 → `utils/startup_checks.py:run_all_startup_checks` (param default 1.0, L1526) → `check_disk_space:L1192-1257` called at L1651 | A01 | F. The `main.py` comment L2468-2472 (HISTORICAL) records an earlier wrong path that always fell back to 1.0. |

### 2.4 `order_reconciler` (L468) — `OrderReconcilerConfig` L1006-1097 — 7 leaves. The whole object is passed at `M` L3123/L3132 → `orders/order_reconciler.py:OrderReconciler.__init__` (`cfg`)

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `poll_interval_sec` | 469 | 15 | L1008 · int · REQ · ≥1 (L1056) | `order_reconciler.py:start:L454`; `_poll_loop:L663` (wait); `_should_alert_capital_drift:L606` (`getattr` default 15; used as a divisor at L608) | A12 | F. |
| `capital_drift_tolerance` | 470 | 50.0 | L1009 · float · REQ · ≥0 (L1070) | `_g3_capital_drift:L3855, L3871, L3907`; `_check7_capital_accounting_drift:L4024`. `scripts/eod_broker_reconcile.py:main:L348` (`float()`) | A12 | F. `scripts/revert_temp_config.py` L57-60 carries `prod_value` "50.0" (A02 tool; regex L58). |
| `capital_drift_tolerance_pct` | 471 | 0.10 | L1014 · float · 0.0 · none | `_g3_capital_drift:L3876` (`getattr` default 0.0; `max(tol, abs(expected)*pct)` L3877-3878, **fraction** despite "_pct"). `eod_broker_reconcile.py:main:L349` (`getattr` default 0.0) | A12 | F. No range check in the loader. |
| `human_order_margin_tolerance` | 472 | 5000.0 | L1019 · float · 5000.0 · ≥0 (L1077) | `OrderReconciler.__init__:L397-401` (`getattr` default 5000.0, float) → `_g3_capital_drift:L3880`. `eod_broker_reconcile.py:main:L350` (`getattr` default 5000.0) | A12 | F. |
| `capital_drift_alert_interval_sec` | 473 | 1800 | L1026 · float · 1800.0 · ≥1 (L1084) | `__init__:L408-412` (`getattr` default 1800.0) → `_should_alert_capital_drift:L608` (**seconds → poll cycles**: `round(interval/poll)`) | A12 | F. |
| `stuck_exiting_timeout_minutes` | 474 | 30 | L1035 · int · 30 · ≥1 (L1063) | `_check_stuck_exiting:L1524` (`int(getattr(…,30) or 30)`) | A12 | F. |
| `check1_mid_fill_defer_sec` | 475 | 0.0 | L1052 · float · 0.0 · ≥0 (L1091) | `_check1_defer_bound_sec:L1113` (`getattr` default 0.0) | A12 | F. 0.0 = OFF (YAML comment L475). |

Display (D): `ops_dashboard/backend/services/capacity.py:build_capacity:L265-267` (the tolerance, pct and human-order keys).

### 2.5 `eod_reconcile` (L477) — `EodReconcileConfig` L1964-1973 — 2 leaves

| Key | L | Value | Loader | Consumers | Owner | Class |
|---|---|---|---|---|---|---|
| `authoritative` | 478 | false | L1972 · bool · False | `scripts/eod_broker_reconcile.py:main:L345` (`bool()`) | A12 | F |
| `pnl_tolerance` | 479 | 100.0 | L1973 · float · 100.0 · none | `eod_broker_reconcile.py:main:L346` (`float()`) | A12 | F |

### 2.6 `eod_cleanup` (L481) — `EodCleanupConfig` L1976-1984 — 1 leaf

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `signal_retention_days` | 482 | 90 | L1984 · int · `Field(default=90, ge=1)` | `scripts/eod_cleanup.py:_resolve_signal_retention_days:L61` (own `load_all()`; on failure the model default `EodCleanupConfig()` L64). CLI `--signal-retention-days` / `--fingerprint-days` (L47-48) **overrides** the config. The cron line does not pass it (`deploy/cron/trading-system.cron` L100) | A12 | F |

### 2.7 `tgt_retry` (L486) — `TgtRetryConfig` L1930-1961 — 4 leaves. Passed at `M` L3143-3155

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 487 | true | L1937 · bool · True | `M` L3153 → `orders/tgt_retry_manager.py:TGTRetryManager.__init__:L81` (used L103, L221-224) | A11 | F |
| `poll_interval_sec` | 488 | 30 | L1938 · int · 30 · ≥1 (L1944) | `M` L3150 → `__init__:L78` (`max(1,int())`) | A11 | F |
| `max_attempts` | 489 | 5 | L1939 · int · 5 · ≥1 (L1951) | `M` L3151 → `__init__:L79` → L357 | A11 | F |
| `backoff_base_sec` | 490 | 30 | L1940 · int · 30 · ≥1 (L1958) | `M` L3152 → `__init__:L80` | A11 | F |

### 2.8 `shadow_tracker` (L492) — `ShadowTrackerConfig` L1139-1150 — 3 leaves. Passed at `M` L2945-2958

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 504 | false | L1141 · bool · REQ | `M` L2956 → `orders/shadow_tracker.py:ShadowTracker.__init__:L147` (handlers no-op at L213, L228, L273, L426) | A11 | F. The tracker is always constructed; the flag silences its handlers. |
| `max_innings` | 505 | 3 | L1142 · int · REQ · 1..5 (L1147) | `M` L2954 → `__init__:L145` (used L403, L606) | A11 | F |
| `alert_per_inning` | 506 | true | L1143 · bool · REQ | `M` L2955 → `__init__:L146` (used L397, L600) | A11 | F |

### 2.9 `sr_detector` (L508) — `SRDetectorConfig` L1153-1255 — 34 leaves

The object is read at `M` L3421. The builders are `sr_detector/zone_builder.py:build_zone_knobs` L40-49, `build_scoring_params` L52-66 and `build_flag_params` L69-75 (all `getattr` with a default), called from `sr_detector/detector.py:SRDetector.__init__` L93-95, `M` L3555-3556 (ZoneWarmer), `M` L3686-3687 (V3 chain) and `M` L3723-3724 (watchlist).

| Key | L | Value | Loader (all optional) | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 509 | true | L1163 · bool · False | `M` L3422 (`_v1_on`, construct gate L3491); `detector.py:__init__:L78` (`getattr` default False) | A08 | F. `scripts/sr_level_export.py` L152-155 forces True in a `model_copy` (offline tool). |
| `timeframes` | 510 | [day, 60minute, 30minute] | L1164 · list[str] · same · non-empty, allowed set (L1245) | `build_zone_knobs:L42` (`intervals`) | A08 (also A18 through the knobs) | F |
| `lookback_days` | 511 | 180 | L1165 · int · 180 | `sr_detector/__init__.py:build_sr_detector:L56` (`getattr` default 180); `M` L3560 (structure fetcher); `sr_level_export.py:L165` | A08 | F |
| `cache_ttl_sec` | 512 | 1800 | L1166 · float · 1800.0 | `__init__.py:build_sr_detector:L59`; `M` L3562 (structure fetcher); **`M` L3523, the regime fetcher's TTL** (cross-section) | A08, A18 | F |
| `default_pivot_n` | 513 | 5 | L1168 · int · 5 | `build_zone_knobs:L43` | A08 | F |
| `cluster_pct` | 514 | 0.5 | L1171 · float · 0.5 | `build_zone_knobs:L45` → `zones.py` L54 (`/100`, **percent**) | A08 | F |
| `merge_pct` | 515 | 0.4 | L1172 · float · 0.4 | `build_scoring_params:L63` → `confluence.py` L70 | A08 | F |
| `band_buffer_pct` | 516 | 0.1 | L1173 · float · 0.1 | `build_scoring_params:L64` → `confluence.py` L129, L133 | A08 | F. The `ScoringParams` dataclass default is 0.0 (`confluence.py` L58), a third default. |
| `entry_proximity_pct` | 517 | 1.0 | L1179 · float · 1.0 | `build_flag_params:L71` → `flags.py` L81, L95 | A08 | F |
| `volume_surge_mult` | 518 | 1.5 | L1180 · float · 1.5 | `build_flag_params:L72` → `flags.py` L174 | A08 | F |
| `w_swing` | 520 | 1.0 | L1184 · float · 1.0 | `build_scoring_params:L54` | A08 | F |
| `w_volume` | 521 | 1.0 | L1185 | `build_scoring_params:L55` | A08 | F |
| `w_multi_tf` | 522 | 1.0 | L1186 | `build_scoring_params:L56` | A08 | F |
| `w_prior_day` | 523 | 1.0 | L1187 | `build_scoring_params:L57` | A08 | F |
| `w_round` | 524 | 0.5 | L1188 | `build_scoring_params:L58` | A08 | F |
| `w_recency` | 525 | 0.5 | L1189 | `build_scoring_params:L59` | A08 | F |
| `t_high` | 526 | 5.0 | L1190 | `build_scoring_params:L60` → `confluence.py` L163 | A08 | F |
| `t_med` | 527 | 3.0 | L1191 | `build_scoring_params:L61` → `confluence.py` L165 | A08 | F |
| `wait_for_retest_enabled` | 529 | false | L1200 · bool · False | `M` L3423 (`_v2_on`; gates L3549, L3769); `screening/retest_monitor.py:RetestDiverter.__init__:L294` | A08 | F |
| `near_zone_buffer_pct` | 530 | 0.3 | L1201 · float · 0.3 | `RetestDiverter.__init__:L295` → L386 | A08 | F |
| `require_confidence` | 531 | HIGH | L1202 · str · "HIGH" · {HIGH, MEDIUM, LOW} (L1238) | `RetestDiverter.__init__:L296` → L386 | A08 | F |
| `retest_timeout_sec` | 532 | 1800 | L1203 · float · 1800.0 | `M` L3780 → `RetestParams.timeout_sec` → `retest_confirm.py` L89 | A08 | F |
| `retest_max_away_pct` | 533 | 1.0 | L1204 · float · 1.0 | `M` L3781 → `RetestParams.max_away_pct` | A08 | F |
| `confirm_strong_close_frac` | 534 | 0.6 | L1205 · float · 0.6 | `M` L3782 → `RetestParams` | A08 | F |
| `breakout_margin_pct` | 535 | 0.0 | L1206 · float · 0.0 | `M` L3783 → `RetestParams` | A08 | F |
| `onem_lookback_days` | 536 | 2 | L1207 · int · 2 | `M` L3775 (1-minute fetcher, `cache_ttl_sec=0.0` literal L3777) | A08 | F |
| `zone_cache_ttl_sec` | 537 | 1800 | L1208 · float · 1800.0 | `M` L3558 (`ZoneCache`) | A08 | F |
| `zone_rewarm_margin_sec` | 538 | 300 | L1209 · float · 300.0 | `M` L3568 (`ZoneWarmer`) | A08 | F. `ZoneWarmer` `max_queue` takes its ctor default 512 (`zone_warmer.py` L42), not `sr_detector.max_queue`. |
| `retest_poll_interval_sec` | 539 | 20 | L1210 · float · 20.0 | `M` L3788 (`RetestMonitor`) | A08 | F |
| `sl_buffer_pct` | 540 | 0.2 | L1211 · float · 0.2 | `M` L3610 → `signals/signal_processor.py` param **`retest_sl_buffer_pct`** (L188, L232; used `/100` at L2438-2441); `RetestDiverter.__init__:L297` → L356-358 | A08, A06 | F. **Name collision:** a separate loader field `sr_detector.retest_sl_buffer_pct` (L1182, default 0.3, absent from the YAML) feeds `build_flag_params:L74` → `flags.py` L180-185. |
| `intraday_anchors_enabled` | 542 | false | L1220 · bool · False | `detector.py:__init__:L84` | A08 | F. `sr_level_export.py` L153 forces True (copy). |
| `anchor_intraday_interval` | 543 | 5minute | L1221 · str · "5minute" · {5,15,30minute} (L1227) | `detector.py:__init__:L85` | A08 | F. `sr_level_export` overrides it from the CLI (L154). INTERPRETATION: `model_copy(update=)` does not re-run validators. |
| `anchor_lookback_days` | 544 | 1 | L1222 · int · 1 | `detector.py:__init__:L86` | A08 | F |
| `orb_window_minutes` | 545 | 15 | L1223 · int · 15 | `detector.py:__init__:L87` | A08 | F. `sr_level_export` overrides it from the CLI (L154). |

Loader fields absent from the YAML, so their defaults apply. All are read through `getattr` with the same default:

| Field | Loader L · default | Read at |
|---|---|---|
| `pivot_n_by_tf` | L1169 · {} | `build_zone_knobs:L44` |
| `volume_bins` | L1175 · 24 | `build_zone_knobs:L46` |
| `volume_node_frac` | L1176 · 0.7 | `build_zone_knobs:L47` |
| `breakout_avg_window` | L1178 · 20 | `detector.py:__init__:L97` |
| `weak_breakout_frac` | L1181 · 0.25 | `build_flag_params:L73` |
| `retest_sl_buffer_pct` | L1182 · 0.3 | `build_flag_params:L74` |
| `touch_cap` | L1192 · 4 | `build_scoring_params:L62` |
| `recency_window_days` | L1193 · 90.0 | `build_zone_knobs:L48` |
| `recency_min_factor` | L1194 · 0.0 | `build_scoring_params:L65` |
| `max_queue` | L1196 · 256 | `detector.py:__init__:L100` |
| `max_zones_logged` | L1197 · 12 | `detector.py:__init__:L98` |

### 2.10 `regime` (L547) — `RegimeConfig` L1258-1301 — 15 leaves

The gate is `M` L3468-3469. The engine is `regime/engine.py:MarketRegimeEngine.__init__` L77-91, reading through a `getattr` helper L53-54. The whole block is not constructed at the file value (`enabled: false`).

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 548 | false | L1269 · bool · False | `M` L3469 (`getattr` default False); `engine.py:__init__:L77` | A18 | F |
| `index_symbol` | 549 | "NIFTY 50" | L1270 · str | `engine.py:__init__:L79` (stored as `_index_symbol`) | A18 | **N (assigned only):** `_index_symbol` is never read again (grep of `regime/`). |
| `index_token` | 550 | 256265 | L1271 · int · 256265 | `engine.py:__init__:L78` | A18 | F. The YAML comment says VERIFY on the VM (HISTORICAL; UNKNOWN). |
| `daily_lookback_days` | 551 | 400 | L1272 · int · 400 | `M` L3521 (fetcher lookback); `engine.py:__init__:L80` | A18 | F |
| `intraday_interval` | 552 | 5minute | L1273 · str · {5,15,30minute} (L1289) | `engine.py:__init__:L81` | A18 | F |
| `intraday_lookback_days` | 553 | 1 | L1274 · int · 1 | `engine.py:__init__:L82` | A18 | F |
| `ema_fast` | 554 | 50 | L1275 · int · 50; model check `ema_fast < ema_slow` (L1298) | `engine.py:__init__:L83` | A18 | F |
| `ema_slow` | 555 | 200 | L1276 · int · 200 | `engine.py:__init__:L84` | A18 | F |
| `adx_period` | 556 | 14 | L1278 | `engine.py:__init__:L86` | A18 | F |
| `adx_trend_threshold` | 557 | 25.0 | L1279 | `engine.py:__init__:L87` | A18 | F |
| `atr_period` | 558 | 14 | L1280 | `engine.py:__init__:L88` | A18 | F |
| `vol_high_ratio` | 559 | 1.3 | L1281 | `engine.py:__init__:L89` | A18 | F |
| `vol_low_ratio` | 560 | 0.7 | L1282 | `engine.py:__init__:L90` | A18 | F. No high > low ordering check. |
| `trend_day_range_atr_mult` | 561 | 1.5 | L1283 | `engine.py:__init__:L91` | A18 | F |
| `compute_interval_sec` | 562 | 60.0 | L1285 · float · 60.0 | `M` L3534 (`MarketRegimeShadowRunner interval_sec`) | A18 | F. The persist path is a literal `data_store/regime/regime_state.json` (`M` L3535). |

Absent from the YAML (defaults apply): `slope_lookback` (L1277 · 5 → `engine.py:__init__:L85`, used at L155) and `swing_pivot_n` (L1284 · 3 → `engine.py:_swing_structure:L193`).

### 2.11 `portfolio_allocator` (L564) — `PortfolioAllocatorConfig` L1304-1381 — 7 leaves

The gate is `M` L3632-3633 (`allocator_mode != "off"`). The object goes to `allocation/portfolio_allocator.py:PortfolioAllocator` (`self._cfg`).

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `allocator_mode` | 565 | "shadow" | L1325 · str · "off" · {off, shadow, enforce} (L1343) | `M` L3633 (`getattr` default "off"), L3654 log; `portfolio_allocator.py:mode:L71` | A18 | F |
| `enforce_scope` | 566 | "v3_only" | L1326 · {v3_only, all} (L1350) | `in_scope:L77`; `start:L116` log | A18 | F |
| `candle_interval_seconds` | 567 | 60.0 | L1329 · float · 60.0; model check >0 (L1374) | `_run_worker:L131`; `_compute_regret:L251`; `start:L117` | A18 | F |
| `drain_tail_seconds` | 568 | 2.0 | L1330 · float; model check 0 < tail < interval (L1374) | `_run_worker:L132`; `start:L117` | A18 | F |
| `max_portfolio_deployment_pct` | 569 | null | L1334 · Optional[float] · None · (0, 1] when set (L1357) | `_passes_portfolio_rules:L184` (None = inert) | A18 | F (inert at the file value). |
| `long_short_skew_max` | 570 | null | L1337 · Optional[float] · None · (0.5, 1] when set (L1366) | `_passes_portfolio_rules:L188` | A18 | F (inert). |
| `regret_log_path` | 571 | "data_store/allocator/regret.jsonl" | L1339 · str | `_persist_regret:L277` (as given, cwd-relative); `scripts/v3_shadow_soak_report.py:allocator_report:L109` (`_REPO /` path; `getattr` default same) | A18 | F |

### 2.12 `v3_chain` (L573) — `V3ChainConfig` L1384-1513 — 39 leaves

The gate is `M` L3472-3473. Consumers are `v3_chain/runner.py` (10a; `self._cfg`), `v3_chain/pb01_runner.py` / `pb01_entry.py` (10b; `self._v3`, which is the same object, `M` L3722) and `v3_chain/score.py:compose_score` (argument `cfg`). The loader model check (`core/config_loader.py` L1500-1513) enforces: `atr30_period` > 0, `rr_floor` > 0, `exec_budget` > 0, and `high` > `medium` > `min_pass`.

| Key | L | Value | Loader L · default | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `v3_chain_mode` | 574 | "shadow" | L1405 · "off" · {off, shadow} (L1486) | `M` L3473 (`getattr` default "off"), L3695; `runner.py:mode:L76` | A18 | F |
| `atr30_period` | 576 | 14 | L1408 · 14 | `runner.py:_build_record:L199`; `pb01_entry.py:_static_inputs:L282-283` | A18 | F |
| `rr_floor` | 577 | 2.0 | L1409 · 2.0 | `runner.py:_build_record:L210`; `pb01_runner.py:_build:L141` → `screening/hard_gate.py` (G-RR L289) | A18, A07 | F |
| `sl_buffer_atr_mult` | 578 | 0.20 | L1410 · 0.20 | `runner.py:_build_record:L211`; `pb01_runner.py:_build:L134, L142` | A18 | F |
| `htf_ema_period` | 579 | 20 | L1411 · 20 | `runner.py:_build_record:L201`; `pb01_runner.py:_build:L148` | A18 | F |
| `htf_swing_pivot_n` | 580 | 3 | L1412 · 3 | `runner.py:_build_record:L202`; `pb01_runner.py:_build:L149` | A18 | F |
| `confirm_min_body_frac` | 582 | 0.50 | L1416 | `pb01_entry.py:_evaluate:L227`; `pb01_runner.py:_build:L168, L196` | A18 | F (10b only) |
| `confirm_volume_mult` | 583 | 1.20 | L1417 | `pb01_entry.py:_evaluate:L228`; `pb01_runner.py:_build:L169` | A18 | F |
| `baseline_candles_per_session` | 584 | 75 | L1418 | `pb01_entry.py:_static_inputs:L295` | A18 | F |
| `pullback_proximity_pct` | 585 | 0.005 | L1419 | `pb01_entry.py:_evaluate:L218`; `pb01_runner.py:_build:L172` → `hard_gate.py` L449 (**fraction** × LEVEL) | A18 | F. A fraction, while the `sr_detector` `*_pct` keys are percents. |
| `pullback_proximity_atr_mult` | 586 | 0.50 | L1420 | `pb01_entry.py:_evaluate:L219`; `pb01_runner.py:_build:L173` | A18 | F |
| `hold_buffer_atr_mult` | 587 | 0.20 | L1421 | `pb01_entry.py:_evaluate:L197, L220`; `pb01_runner.py:_build:L174` | A18 | F |
| `retest_quality_atr_span` | 588 | 0.75 | L1423 | `pb01_runner.py:_build:L193` | A18 | F |
| `level_touches_cap` | 589 | 5 | L1424 | `pb01_runner.py:_build:L198` | A18 | F |
| `w_retest_quality` | 591 | 15.0 | L1428 | `score.py:compose_score:L171` (only when `playbook` is given: the `pb01_runner.py` L206-209 call) | A18 | F |
| `w_confirmation_strength` | 592 | 15.0 | L1429 | `compose_score:L172` | A18 | F |
| `w_level_significance` | 593 | 10.0 | L1430 | `compose_score:L173` | A18 | F |
| `w_regime_preference` | 594 | 8.0 | L1432 | `compose_score:L139` | A18 | F |
| `w_sr_target_quality` | 595 | 8.0 | L1433 | `compose_score:L140` | A18 | F |
| `w_htf_alignment` | 596 | 8.0 | L1434 | `compose_score:L141` | A18 | F |
| `w_sector_strength` | 597 | 8.0 | L1435 | `compose_score:L142` | A18 | F |
| `w_momentum_position` | 598 | 8.0 | L1436 | `compose_score:L143` | A18 | F |
| `exec_budget` | 599 | 20.0 | L1439 | `compose_score:L149` (scale = budget/Σ raw) | A18 | F |
| `w_exec_volume_surge` | 600 | 15.0 | L1440 | `compose_score:L147, L150` | A18 | F |
| `w_exec_atr` | 601 | 10.0 | L1441 | `compose_score:L147, L151` | A18 | F |
| `w_exec_time_of_day` | 602 | 5.0 | L1442 | `compose_score:L148, L152` | A18 | F |
| `w_exec_spread` | 603 | 5.0 | L1443 | `compose_score:L148, L153` | A18 | F |
| `confluence_combine` | 604 | "mean" | L1449 · {mean, max} (L1495) | `compose_score:L129` (`getattr` default "mean") | A18 | F |
| `sr_target_quality_high` | 605 | 1.0 | L1452 | `runner.py:sr_target_fraction:L340` (module function, used by both runners) | A18 | F |
| `sr_target_quality_medium` | 606 | 0.6 | L1453 | `sr_target_fraction:L342` | A18 | F |
| `sr_target_quality_low` | 607 | 0.3 | L1454 | `sr_target_fraction:L343` | A18 | F |
| `min_pass_score` | 609 | 60 | L1470 · 60; ordering check (L1508) | none in code. D: `ops_dashboard/backend/services/controls.py:_limits:L166, L202` shows it as **"Minimum Eligible Score"** | A18 (A15 display) | **N** (display only). The loader comment L1467 says "does not gate". |
| `medium_score_threshold` | 610 | 65 | L1471 · 65 | none (grep hits are `scoring_weights` consumers) | A18 | **N** |
| `high_score_threshold` | 611 | 80 | L1472 · 80 | none | A18 | **N** |
| `structure_intervals` | 613 | [day, 60minute, 30minute] | L1477 | `runner.py:_build_record:L166`; `pb01_runner.py:_build:L109` (`getattr` with the same default list) | A18 | F. No allowed-set validator, unlike `sr_detector.timeframes`. |
| `fetch_lookback_days` | 614 | 180 | L1479 · 180 | `M` L3680 (V3 fetcher); **`M` L3730 (watchlist fetcher)** | A18 | F. Cross-use by the watchlist. |
| `fetch_cache_ttl_sec` | 615 | 1800.0 | L1480 | `M` L3682 (fetcher TTL); `runner.py:_sr_sync_hit:L141` (proxy window) | A18 | F. The watchlist fetcher uses a literal `cache_ttl_sec=0.0` (`M` L3732). |
| `max_queue` | 616 | 512 | L1481 | `runner.py:__init__:L67` | A18 | F |
| `would_be_log_path` | 617 | "data_store/v3/would_be.jsonl" | L1482 | `runner.py:_persist:L272`; `v3_shadow_soak_report.py:v3_report:L190` | A18 | F |

Absent from the YAML (defaults apply): `regime_pref_direction` L1460 {BULL 1.0, SIDEWAYS 0.5, BEAR 0.0}, `regime_pref_day_type` L1462 {TREND_DAY 1.0, UNDETERMINED 0.5, RANGE_DAY 0.4} and `regime_pref_volatility` L1464 {HIGH 0.85, NORMAL 1.0, LOW 1.0}. All three are read at `runner.py:regime_fraction:L324-326`, with a `.get` fallback of 0.5 / 0.5 / 1.0 for an unknown label.

### 2.13 `watchlist` (L619) — `WatchlistConfig` L1516-1574 — 10 leaves

The gate is `M` L3477-3478. Consumers are `v3_chain/watchlist_capture.py`, `pb01_entry.py` and `pb01_runner.py`. The loader model check (`core/config_loader.py` L1561-1574) enforces: start < end, `level_lookback_sessions` > 0, 0 < `gap_guard_pct` < 1, `poll_interval_sec` > 0.

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 620 | true | L1531 · False | `M` L3478 (`getattr` default False) | A18 | F |
| `playbook_scanner` | 621 | "pb01_breakout_retest" | L1535 | none (grep: loader and YAML only) | A18 | **N** |
| `level_lookback_sessions` | 623 | 20 | L1538 | `watchlist_capture.py:_capture:L155, L159` | A18 | F |
| `capture_fetch_lookback_days` | 624 | 60 | L1539 | `pb01_entry.py:_static_inputs:L291` (baseline volume only) | A18 | F. **Not** used by the EOD LEVEL capture: `_capture` L154 calls `fetch_timeframes`, which uses the fetcher's own lookback (`sr_detector/fetch.py` L123), set at `M` L3730 from `v3_chain.fetch_lookback_days` (180). The YAML comment L624 says it is the LEVEL fetch window. |
| `entry_start` | 626 | "09:20" | L1542 · HH:MM (L1553) | `pb01_entry.py:__init__:L107` (`getattr` default "09:20") | A18 | F |
| `entry_end` | 627 | "11:00" | L1543 | `pb01_entry.py:__init__:L108` | A18 | F |
| `entry_tf` | 628 | "5minute" | L1544 · no validator | none. `pb01_entry.py` uses the literal `_TF_5 = "5minute"` (L44; used L177, L243, L308) | A18 | **N** (replaced by a literal). |
| `gap_guard_pct` | 629 | 0.03 | L1545 | `pb01_entry.py:_evaluate:L188, L192` (`level*(1+pct)`, **fraction**) | A18 | F |
| `poll_interval_sec` | 630 | 20.0 | L1546 | `pb01_entry.py:__init__:L104-105` (a ctor argument overrides when given; `M` passes none) | A18 | F |
| `would_be_log_path` | 631 | "data_store/v3/pb01_would_be.jsonl" | L1549 | `pb01_runner.py:_persist:L246`; `v3_shadow_soak_report.py:pb01_report:L354` | A18 | F |

### 2.14 `structure_exit` (L633) — `StructureExitConfig` L1577-1607 — 6 leaves

The gate is `M` L3426-3427, plus the A4 guard at `M` L3436-3443. The consumer is `orders/structure_exit_manager.py:StructureExitManager.__init__` L128-134. Not constructed at the file value.

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `structure_exit_enabled` | 634 | false | L1588 · False | `M` L3427 (`getattr` default False); `structure_exit_manager.py:__init__:L128`; `core/config_auditor.py:_group_a_contradictions:L223-224` (A4 BLOCK when on and an enabled strategy has `trailing_sl_enabled`) | A11, A02 | F |
| `sl_buffer_pct` | 635 | 0.2 | L1589 | `__init__:L131` → L526-528 (`/100`, **percent**) | A11 | F. Same value as `sr_detector.sl_buffer_pct` ("match Phase A", YAML L635). The two are separate keys. |
| `break_buffer_pct` | 636 | 0.0 | L1590 | `__init__:L132` → L287 | A11 | F |
| `require_strong_close` | 637 | true | L1591 | `__init__:L133` | A11 | F |
| `break_strong_close_frac` | 638 | 0.6 | L1592 · [0, 1] (L1604) | `__init__:L134` | A11 | F |
| `min_zone_confidence` | 639 | HIGH | L1593 · {HIGH, MEDIUM, LOW} (L1597) | `__init__:L130` (`.upper()`) | A11 | F |

### 2.15 `smart_tgt` (L641) — `SmartTgtConfig` L1671-1701 — 5 leaves

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 642 | true | L1687 · bool · REQ | `M` L3072 passes the object → `orders/order_placer.py:place:L1746-1750` (`getattr` default False) used **only** to build the ORDER PLACED Telegram text (`smart_on`) | A10, A11 | F (alert text only). `SmartTgtManager` is built with the **literal `enabled=True`** (`M` L2979). `_handle_entry_fill:L2204-2208` registers CO_PLUS_TGT trades **without** checking `enabled`. The YAML comment L642 and loader comment L1687 say that false makes `OrderPlacer` skip the wiring. |
| `trigger_pct` | 643 | 0.005 | L1688 · REQ · 0 < v < 1 (L1695) | `order_placer.py:_handle_entry_fill:L2230` → `register_trade` | A10/A11 | F (CO_PLUS_TGT only) |
| `step_pct` | 644 | 0.003 | L1689 · same | `_handle_entry_fill:L2231` | A10/A11 | F |
| `volume_dependent_trails` | 645 | false | L1690 · REQ | `M` L2986 → `orders/smart_tgt_manager.py:SmartTgtManager.__init__:L110` (ctor default False; used L397) | A11 | F |
| `max_modify_failures` | 646 | 3 | L1691 · 3 · no validator | `M` L2987 → `__init__:L107` (`max(1, v)`; used L771) | A11 | F |

Display (D): `capacity.py:build_capacity:L304-307` (`enabled` read with default **False**).

### 2.16 `entry_gate` (L648) — `EntryGateConfig` L1787-1813, `SlippageControlConfig` L1749-1784, `SlippageTier` L1704-1710, `SlippageOverridesConfig` L1713-1746 — 27 leaves

`screening/entry_gate.py:EntryGate` is constructed **without** any of these keys (`M` L3839-3844). The consumers are `OrderPlacer`, `OrderMonitor`, `HardGate` and `SecondaryScreener`.

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `slippage_buffer` | 649 | 2.0 | L1803 · float · REQ | `M` L3074 → `OrderPlacer.__init__:L630` (ctor default 2.0) → `place:L910-913` (only when `release_ltp` is given, i.e. the gate-release path) | A10 | F |
| `max_entry_slippage_pct` | 655 | 1.0 | L1804 · 1.0 · none | `M` L3075 → `__init__:L670` (ctor default 1.0) → `place:L1119-1128` (**percent**; `/100`) | A10 | F |
| `max_spread_pct` | 656 | 0.5 | L1805 · 0.5 | none. `M` does not pass `liquidity_max_spread_pct`, so the `OrderPlacer` ctor default 0.5 (L590) applies at `_check_liquidity:L4073` | A10 | **N** |
| `min_depth_qty` | 657 | 500 | L1806 · 500 | none. Ctor default 500 (L591) at `_check_liquidity:L4074` | A10 | **N** |
| `liquidity_check_enabled` | 658 | **true** | L1807 · True | none. Ctor default **False** (L589) → `_check_liquidity:L4075` returns early | A10 | **N.** The file value and the effective code default differ (INTERPRETATION: the liquidity check is off whatever the YAML says). |
| `min_effective_rr` | 659 | 1.0 | L1808 · 1.0 | `M` L3083 → `__init__:L685` (ctor default 0.0) → `place:L938-956` | A10 | F |
| `min_pending_rr` | 660 | 1.0 | L1809 · **0.0** | `M` L3011 → `broker/order_monitor.py:OrderMonitor.__init__:L229` (ctor default 0.0) → `_check_price_movement_cancel` (skip if ≤ 0, L1147) | A04 | F. Lives in `entry_gate` but is consumed by `OrderMonitor`. |
| `circuit_proximity_reject_enabled` | 661 | true | L1810 · True | `M` L3246 → `screening/hard_gate.py:HardGate.__init__:L134`; `M` L3288 → `screening/secondary_screener.py:SecondaryScreener.__init__:L110` | A07 | F (two consumers) |
| `slippage_control.enabled` | 669 | true | L1765 · **False** | `M` L3076 passes the object → `place:L984` (with `mode == sl_fraction` at L985) and `place:L1113` (`getattr` default False; off → legacy flat-% guard L1122-1128) | A10 | F |
| `slippage_control.mode` | 670 | sl_fraction | L1766 · {sl_fraction, flat_tiers, pct} (L1779) | `_compute_slippage_tolerance:L345`; `_slippage_decision:L387`; `place:L985`. `scripts/system_manager.py:slippage_overrides_check:L977` | A10, A15 | F |
| `slippage_control.max_slippage_fraction` | 671 | 0.22 | L1767 · 0.22 | `resolve_slippage_fraction:L264` (`getattr` default 0.22); `_compute_slippage_tolerance:L349` | A10 | F |
| `slippage_control.absolute_cap_rs` | 672 | 5.00 | L1768 · 5.0 | `_compute_slippage_tolerance:L352, L354, L360` | A10 | F |
| `slippage_control.hard_max_slippage_rs` | 673 | 10.0 | L1772 · 10.0 | `_compute_slippage_tolerance:L361` (ceiling in every mode) | A10 | F |
| `slippage_control.also_apply_pct_check` | 674 | true | L1771 · True | `_slippage_decision:L387` | A10 | F |
| `slippage_control.default_max_slippage_rs` | 676 | 2.00 | L1770 · 2.0 | `_compute_slippage_tolerance:L356` (flat_tiers mode only) | A10 | F (inactive branch at the file mode) |
| `slippage_control.tiers[0].max_price` | 678 | 100 | `SlippageTier` L1709 · REQ · no ordering check | `OrderPlacer.__init__:L674-677` (`_slippage_tier_tuples`) → `orders/price_math.py:tier_slippage_tolerance_rs` L60+ (flat_tiers only) | A10 | F (inactive branch) |
| `slippage_control.tiers[0].max_slippage_rs` | 678 | 1.00 | L1710 | same | A10 | F (inactive) |
| `slippage_control.tiers[1].max_price` | 679 | 200 | L1709 | same | A10 | F (inactive) |
| `slippage_control.tiers[1].max_slippage_rs` | 679 | 1.25 | L1710 | same | A10 | F (inactive) |
| `slippage_control.tiers[2].max_price` | 680 | 500 | L1709 | same | A10 | F (inactive) |
| `slippage_control.tiers[2].max_slippage_rs` | 680 | 2.00 | L1710 | same | A10 | F (inactive) |
| `slippage_control.tiers[3].max_price` | 681 | 999999 | L1709 | same | A10 | F (inactive). 999999 is a sentinel (`config_view.py` L505). |
| `slippage_control.tiers[3].max_slippage_rs` | 681 | 3.00 | L1710 | same | A10 | F (inactive) |
| `slippage_control.overrides.enabled` | 691 | true | L1731 · True | `resolve_slippage_fraction:L266`; `validate_slippage_overrides:L295` (called at `M` L3222-3226 and `config_auditor.py:_group_d_active_overrides:L569`; also L541-556) | A10, A02 | F |
| `slippage_control.overrides.by_price_band` | 697 | {} | L1732 · {} · fractions in (0, 1] (L1738) | `resolve_slippage_fraction:L273`; `validate_slippage_overrides:L298` | A10 | F (empty) |
| `slippage_control.overrides.by_strategy` | 701 | {} | L1733 | `resolve_slippage_fraction:L270`; `validate…:L299, L316` | A10 | F (empty) |
| `slippage_control.overrides.by_symbol` | 706 | {} | L1734 | `resolve_slippage_fraction:L267`; `validate…:L300, L309` | A10 | F (empty) |

Display (D) for `slippage_control.*` and `max_entry_slippage_pct`:
- `capacity.py:build_capacity:L297-301`
- `config_view.py:_slippage:L494-529` and `_categories:L683-688`
- `ops_dashboard/backend/api/analytics.py:get_slippage:L36-38`, with literal fallbacks `or 0.22`, `or 5.0`
- `slippage_analytics.py:slippage_model:L141-147`, with literal fallbacks 0.22 / 5.0 / 10.0 and `enabled` default True
- `reports/daily_trade_review.py:build_config_data:L1276-1277`, which also shows `slippage_buffer`
- `scripts/system_manager.py:slippage_overrides_check:L976-988`

### 2.17 `slippage_bands` (L712) — `SystemConfig.slippage_bands` L2027-2029 — 1 leaf

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `slippage_bands` | 712-718 | [0-100, 100-200, 200-300, 300-500, 500-1000, 1000+] | list[str] · same list · no format validator | `M` L3077 → `OrderPlacer.__init__:L680` → `place:L989` `get_price_band` (override band resolution). `M` L3097 → `orders/slippage_recorder.py:SlippageRecorder.__init__:L109` → `_on_position_closed:L190` (price_band column). `get_price_band` L76-90 parses the labels | A10, A11 | F. D: `config_view.py:_slippage:L527`; `daily_trade_review.py:L1278`. The dashboard keeps its **own** 5-bucket partition (`slippage_analytics.py` L82-91, documented as not this key). The `slippage_control.tiers` boundaries (100/200/500) are a third band structure. |

### 2.18 `paper` (L720) — `PaperConfig` L1610-1668 — 4 leaves — **paper-only, not traced**

| Key | L | Value | Loader | Consumer site (marked only) | Owner | Class |
|---|---|---|---|---|---|---|
| `auto_fill_delay_sec` | 721 | 0.5 | L1632 · 0.5 · 0..10 (L1639) | `M` L2398 → `ZerodhaAdapter(paper_auto_fill_delay_sec=)` L369/L410 | A04 | P |
| `ltp_gating_enabled` | 722 | true | L1633 · False | `M` L2400 → adapter L373/L412 | A04 | P |
| `ltp_gating_max_wait_sec` | 723 | 21600 | L1634 · 60.0 · 0..25200 (L1650) | `M` L2401 → L374/L413 | A04 | P |
| `ltp_gating_poll_sec` | 724 | 5.0 | L1635 · 0.5 · (0, 30] (L1661) | `M` L2402 → L375/L414 | A04 | P |

The comment at `M` L2395-2396 says the live adapter ignores these.

### 2.19 `drift_handler` (L726) — `DriftHandlerConfig` L1865-1918 — 4 leaves

The object goes from `M` L3853-3857 → `capital/drift_handler.py:CapitalDriftHandler` (`self._config`). The loader model check (`core/config_loader.py` L1906-1918) enforces log_only < soft < hard; field checks require > 0 (L1892) and cycles ≥ 1 (L1899).

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `log_only_threshold_rs` | 727 | 250.0 | L1884 · 250.0 | `_compute_tier:L137`; `_dispatch:L204` (log) | A09 | F. `revert_temp_config.py` L66-69 `prod_value` "250.0". |
| `soft_kill_threshold_rs` | 728 | 1000.0 | L1885 · 1000.0 | `_compute_tier:L135` | A09 | F. `revert_temp_config.py` L75-78. |
| `hard_kill_threshold_rs` | 729 | 2500.0 | L1886 · 2500.0 | `_compute_tier:L133` | A09 | F. `revert_temp_config.py` L84-87. |
| `consecutive_cycles_before_escalate` | 730 | 3 | L1887 · 3 | `_handle:L181` | A09 | F |

D: `capacity.py:build_capacity:L250-253`.

### 2.20 `strategy_circuit_breaker` (L732) — `StrategyCircuitBreakerConfig` L1838-1844 — 4 leaves

The object goes from `main.py:_build_strategy_governor:L849` (`getattr`; INTERPRETATION: the None branch at L850-851 is unreachable because the field has a default, `core/config_loader.py` L2023) → `capital/strategy_governor.py:StrategyGovernor.__init__` L35-38.

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `enabled` | 733 | true | L1841 · True · none | `__init__:L35` (`getattr` default True) → L57 | A09 | F. D: `capacity.py:L259` (default **False**). |
| `loss_multiplier` | 734 | 2.0 | L1842 · none | `__init__:L36` → L77 | A09 | F |
| `cutoff_time` | 735 | "12:00" | L1843 · str · **no HH:MM validator** | `__init__:L37` → `_parse_hhmm` L191-196 (an invalid value silently becomes 12:00) → L64 | A09 | F |
| `lookback_days` | 736 | 10 | L1844 · none | `__init__:L38` → L109 (`timedelta(days=)`, **calendar days**) | A09 | F |

### 2.21 `circuit_breaker` (L738) — `CircuitBreakerConfig` L1847-1862 — 3 leaves. `M` L2997 → `OrderMonitor`

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `partial_fill_timeout_minutes` | 739 | 5 | L1860 · 5 · none | `M` L3007 → `order_monitor.py:__init__:L232` (**min → s**, ×60) → `_handle_partial:L946` | A04 | F |
| `force_close_time` | 740 | "15:15" | L1861 · str · **no validator** | `M` L3009 → `__init__:L238-248` (parse; an invalid value disables with a warning) → `_check_force_close:L806-822` | A04/A13 | F. No special-session adjustment found (grep "special" in `order_monitor.py`: none). |
| `max_api_failures` | 741 | 3 | L1862 · 3 · none | `M` L3008 → `__init__:L233` → `_process_order:L677` (HARD_KILL path) | A04/A13 | F. Same value as `kill_switch.api_failure_threshold` (YAML L356, part 1 range), which is a separate mechanism. |

D: `capacity.py:L261-263`.

### 2.22 `live_feed` (L743) — `LiveFeedConfig` L1816-1821 — 3 leaves

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `max_reconnect_attempts` | 744 | 10 | L1819 · 10 | none functional. `LiveFeedManager(...)` at `M` L2927-2938 passes no `live_feed` key; ctor default 10 (`data/live_feed.py:__init__` L45/L77; used `_create_ticker:L515`). D: `capacity.py:L295` | A05 | **N** (display only; the file value equals the ctor default). |
| `reconnect_backoff_base_seconds` | 745 | 1 | L1820 · 1 | none (grep) | A05 | **N** |
| `reconnect_backoff_max_seconds` | 746 | 30 | L1821 · 30 | none. The feed uses `reconnect_delay_sec` (ctor default 5) as `reconnect_max_delay` (L46, L78, L516) | A05 | **N.** File 30 vs effective 5 (INTERPRETATION). |

### 2.23 `fno_ban` (L748) — `FnoBanConfig` L1824-1835 — 2 leaves

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `url` | 749 | NSE `fo_secban.csv` URL (public) | L1834 · same URL | `scripts/fetch_fno_ban.py:main:L319` (own `load_all`; on any exception silently keeps `_DEFAULT_URL` L70/L313); CLI `--url` overrides (L252, L324-325) | A05 | F. The URL is duplicated in three places (YAML, loader default, script literal). |
| `fail_closed` | 750 | false | L1835 · False | `fetch_fno_ban.py:main:L320` (fallback False L314) → `_soft_fail` | A05 | F |

### 2.24 `scanner_check_delay_sec` (L753) — `SystemConfig.scanner_check_delay_sec` L2026 — 1 leaf

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `scanner_check_delay_sec` | 753 | 5.0 | float · 5.0 · none | `utils/startup_checks.py:run_all_startup_checks:L1591` (`getattr` default **0.0**) → `check_scanner_connectivity(delay_sec=)`; skipped on COLD scenario (L1589) | A01 (A06) | F. Read default 0.0 vs loader default 5.0. |

### 2.25 `config/broker_limits.yaml` — `BrokerLimitsConfig` L2245-2256 — 16 leaves

`RateLimiter` is built at `M` L2348; also at `scripts/forward_shadow_record.py` L116, `scripts/sr_level_export.py` L144, `scripts/t2_cnc_gtt_realtest.py` L169 and `broker/rate_limiter.py` L136 (docstring example).

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `order.burst` / `order.rate_per_sec` | 10 / 11 | 8 / 8 | `TokenBucketConfig` L2178/L2179 · int · REQ · **no >0 check** | `broker/rate_limiter.py:RateLimiter.__init__:L158` → `_Bucket` (rate used as a divisor at L85) | A04 | F (2 leaves) |
| `quote.burst` / `quote.rate_per_sec` | 14 / 15 | 3 / 3 | same | `__init__:L159` | A04 | F (2) |
| `historical.burst` / `historical.rate_per_sec` | 18 / 19 | 2 / 2 | same | `__init__:L160` | A04 | F (2) |
| `margins.burst` / `margins.rate_per_sec` | 22 / 23 | 8 / 8 | same | `__init__:L161` | A04 | F (2) |
| `backoff_sequence_sec` | 25-28 | [1, 5, 30] | L2251 · list[int] · REQ · none | none (grep of non-test code) | A04 | **N.** The header L5 says to apply the sequence and then soft_kill; the comment L29 says the 4th step is soft_kill, "handled in code" (both HISTORICAL). |
| `timeouts.connect_sec` | 32 | 5 | L2184 · int · REQ | none. `KiteConnect` takes a single `timeout` = `read_sec` (`M` L385-386) | A04 | **N** |
| `timeouts.read_sec` | 33 | 10 | L2185 · int · REQ | `main.py:_build_kite_client:L385` → `KiteConnect(timeout=)` L386 (live client only) | A04 | F. The other `KiteConnect(...)` constructions pass no timeout: `main.py` L414, L501 (paper paths); `scripts/eod_broker_reconcile.py` L220; `reconcile_pnl.py` L107; `reconcile_positions.py` L154; `refresh_instruments.py` L304; `forward_shadow_record.py` L111; `preflight/checks/broker.py` L154; and others. |
| `rate_limit_backoff.initial_delay_sec` | 36 | 0.2 | L2203 · 0.2 · ≥0 (L2211) | `M` L2404 → `broker/zerodha_adapter.py:__init__:L429` → `_compute_429_backoff_delay:L2021` | A04 | F |
| `rate_limit_backoff.max_delay_sec` | 37 | 5.0 | L2204 · ≥0, ≥ initial (L2236) | `_compute_429_backoff_delay:L2022` | A04 | F |
| `rate_limit_backoff.max_placer_retries` | 38 | 3 | L2205 · ≥0 (L2228) | `M` L3073 → `OrderPlacer.__init__:L626-628` (fallback `RateLimitBackoffConfig()` if None) → `place:L1316` | A10 | F |
| `rate_limit_backoff.multiplier` | 39 | 2.0 | L2206 · ≥1 (L2218) | `_compute_429_backoff_delay:L2021` | A04 | F |
| `rate_limit_backoff.jitter_sec` | 40 | 0.05 | L2207 · ≥0 | `_compute_429_backoff_delay:L2024-2025` | A04 | F |

### 2.26 `config/broker_costs.yaml` — `BrokerCostsConfig` L2131-2168 — 15 leaves

All values are percentages (header L9-10). The consumer is `broker/cost_calculator.py:CostCalculator.calculate_cost`, built at `M` L2350, with each rate `/100`. The loader model check (`core/config_loader.py` L2140-2168) enforces: the 9 equity rates are ≥ 0, brokerage flat and pct are not both 0, and `gst_pct` > 0. **The futures and options rates have no check.**

| Key | L | Value | Loader | Consumer line in `calculate_cost` | Owner | Class / direct readers |
|---|---|---|---|---|---|---|
| `zerodha.brokerage_flat_intraday` | 14 | 20.0 | L2117 · REQ | L171 (`min(flat, proportional)`) | A04 | F. Also `reports/daily_report.py:_compute_cost_breakdown:L355` (literal default 20.0). |
| `zerodha.brokerage_pct_intraday` | 15 | 0.03 | L2118 | L170 | A04 | F. `daily_report` L356 (default 0.03). |
| `zerodha.stt_sell_pct` | 16 | 0.025 | L2119 | L192 | A04 | F. `daily_report` L357. |
| `zerodha.stt_cnc_pct` | 17 | 0.1 | L2120 | L198 (CNC branch) | A04 | F |
| `zerodha.exchange_txn_pct` | 18 | 0.00297 | L2121 | L201 | A04 | F. `daily_report` L358. |
| `zerodha.gst_pct` | 19 | 18.0 | L2122 | L208 | A04 | F. `daily_report` L360. |
| `zerodha.sebi_pct` | 20 | 0.0001 | L2123 | L204 | A04 | F. `daily_report` L359. |
| `zerodha.stamp_duty_mis_buy_pct` | 21 | 0.003 | L2124 | L225 | A04 | F. `daily_report` L361. |
| `zerodha.stamp_duty_cnc_buy_pct` | 22 | 0.015 | L2125 | L228 | A04 | F |
| `zerodha.futures.stt_pct` | 26 | 0.0125 | L2097 | L180 (F&O branch) | A04 | F (whether F&O was ever traded is outside A02) |
| `zerodha.futures.stamp_duty_buy_pct` | 27 | 0.002 | L2098 | L221 | A04 | F |
| `zerodha.options_buy.stt_pct` | 30 | 0.0 | L2104 | L187 | A04 | F |
| `zerodha.options_buy.stamp_duty_pct` | 31 | 0.003 | L2105 | L223 | A04 | F |
| `zerodha.options_sell.stt_pct` | 34 | 0.0625 | L2111 | L184 | A04 | F |
| `zerodha.options_sell.stamp_duty_pct` | 35 | 0.0 | L2112 | L215 | A04 | F |

Direct readers:
- `reports/daily_report.py:load_report_data:L155-159` reads `broker_costs.yaml` **directly** (yaml.safe_load). `_compute_cost_breakdown:L355-361` recomputes costs itself, with literal defaults identical to the file values.
- `ops_dashboard/backend/readers/config_reader.py:get_broker_costs:L311-335` is a direct read for display, used at `config_view.py` L722 and L865-873.
- The `BrokerCostsConfig` docstring L2133-2135 says "No hardcoded fallback values exist in CostCalculator (CC9)". That is true of `CostCalculator`, not of `daily_report`.

### 2.27 `config/slippage_model.yaml` — `SlippageConfig` L2264-2272 — 4 leaves — **paper-only consumer**

| Key | L | Value | Loader | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `tiers.liquid.slippage_bps` | 11 | 5 | `tiers: dict[str, SlippageTierConfig]` L2271; `slippage_bps` int L2266 · REQ | `broker/slippage_engine.py:SlippageEngine.apply:L113`, built only `if is_paper` (`M` L2511-2515) | A04 | P |
| `tiers.mid.slippage_bps` | 13 | 15 | same | same (`tier_for` returns "mid" for cash symbols, L92) | A04 | P |
| `tiers.small.slippage_bps` | 15 | 30 | same | same; `tier_for` L86-92 never returns "small" (INTERPRETATION) | A04 | P |
| `default_tier` | 17 | liquid | L2272 · str · REQ (no check that it is in `tiers` at load; `slippage_engine.py` L64-66 checks at construction) | `SlippageEngine.tier_for:L70-92` (returns at L89-92) | A04 | P |

D: `daily_trade_review.py:build_config_data:L1270-1274` and `_slip_tiers_for_date:L1787-1788`. The header L5 names `capital/cost_calculator.py` and `symbol_validator.py`; neither exists at the baseline (`git ls-files`). HISTORICAL.

### 2.28 `config/security.yaml` — not loaded centrally — 52 leaves

Readers: `SecConfig.load` (`scripts/security_monitor.py` L150-183), which copies listed keys from `security:` (L157-170) plus `copy_protection.enabled` / `audit_log_path` (L171-176). `CopyConfig.load` (`scripts/copy_gate.py` L79-98) copies 8 keys from `copy_protection:`. The dataclass defaults (`security_monitor.py` L108-148; `copy_gate.py` L68-77) apply for a missing file, a missing key or a load error.

| Key | L | File value | Dataclass default | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `security.enabled` | 11 | true | True (L110) | `security_monitor.py:main:L1354` | A17 | F |
| `security.max_active_sessions` | 15 | 2 | 2 | `check_active_sessions:L779, L791` | A17 | F |
| `security.failed_login_spike_threshold` | 19 | 500 | 500 | `check_failed_spike:L687, L691` | A17 | F |
| `security.root_probe_spike_threshold` | 22 | 400 | 400 | `check_root_probe_spike:L696, L700` | A17 | F |
| `security.new_ip_alert` | 26 | true | True | `check_new_login_ips:L677` | A17 | F |
| `security.sudo_alert` | 29 | true | True | `check_sudo_events:L705` | A17 | F |
| `security.sudo_whitelist_prefixes` | 30-42 | 12 binary prefixes (/usr/bin, /bin, /usr/sbin) | same 12 (L134-139) | `check_sudo_events:L710` | A17 | F |
| `security.realert_cooldown_sec` | 46 | 21600 | 21600 | `main:L1384` → `_dedup` | A17 | F |
| `security.realert_backoff_multipliers` | 56 | [1, 4, 28] | same | `main:L1385` | A17 | F |
| `security.realert_presence_gap_sec` | 63 | 300 | 300 | `main:L1386` | A17 | F |
| `security.holiday_calendar_alert` | 89 | true | True | `check_nse_holiday_calendar:L960` | A17 | F. Not a security check (YAML L65-88). |
| `security.holiday_calendar_lead_days` | 90 | 16 | 16 | `check_nse_holiday_calendar:L965, L987` | A17 | F. The YAML says it must stay > `final_days` (L85); no check found. |
| `security.holiday_calendar_final_days` | 91 | 3 | 3 | `check_nse_holiday_calendar:L966` | A17 | F |
| `security.expected_ssh_keys` | 116 | 1 | 1 | `check_authorized_keys:L664, L667` | A17 | F. **Overridden** when `data_store/security/ssh_key_baseline.json` exists (`apply_operator_ssh_baseline:L200-210`, called at `main:L1349`). Whether that file existed is UNKNOWN. |
| `security.expected_key_fingerprint` | 117 | not reproduced (SSH key fingerprint) | "" | `check_authorized_keys:L655-656`; `scripts/approve_ssh_keys.py:_effective_baseline:L43-44` | A17 | F. **Blanked** by the operator override (L205). |
| `security.authlog_path` | 120 | /var/log/auth.log | same constant | `main:L1350` | A17 | F |
| `security.sentinel_dir` | 121 | data_store | "data_store" | `_send:L1219` | A17 | F. Duplicates `alerts.sentinel_dir`. |
| `security.watched_files[0].path` (1 leaf) | 126 | 1 home-directory path (the SSH authorized-keys file): not reproduced | `_default_watched_files` L213-224 (8 entries, **no** `sshd_hardening_dropin`) if the list is empty | `check_watched_files:L747`, read only to be skipped: the entry's label `ssh_authorized_keys` sends it to `continue` at L748-749 whatever the path | A17 | **N** (read, then skipped). `check_authorized_keys` uses `authorized_keys_path` (L635), not this path. |
| `security.watched_files[1..8].path` (8 leaves) | 127-134 | 5 system paths under /etc (L127-131: `sshd_config`, the sshd drop-in, `sudoers` and 2 systemd units); 3 home-directory paths of trading-system files (L132-134): not reproduced | as above | `check_watched_files:L747`, hashed at L752 | A17 | F |
| `security.watched_files[0].severity` (1) | 126 | CRITICAL | — | none. Entry [0] reaches `continue` at L748-749 before the severity read at L750 | A17 | **N** |
| `security.watched_files[1..8].severity` (8) | 127-134 | 6 × CRITICAL, 2 × WARNING | — | `check_watched_files:L750` (`get` default "WARNING") | A17 | F |
| `security.watched_files[0..8].label` (9) | 126-134 | ssh_authorized_keys, sshd_config, sshd_hardening_dropin, sudoers, unit_trading, unit_security, dotenv, system_config, accounts_csv | — | `check_watched_files:L748, L751` | A17 | F |
| `copy_protection.enabled` | 148 | true | True (both) | `copy_gate.py:check_copy_allowed:L219`; `scripts/request_copy.py:request:L66`; `security_monitor.py:check_copy_protection_switch:L803` (as `copy_protection_enabled`); `scripts/preflight/checks/security.py:CopyProtectionStateCheck.run:L79` (`is True`); `scripts/system_manager.py:security_check:L825` | A17, A20, A15 | F |
| `copy_protection.token_ttl_minutes` | 149 | 15 | 15 | `request_copy.py:request:L85` | A17 | F |
| `copy_protection.time_lock_start` | 150 | 18 | 18 | `copy_gate.py:check_copy_allowed:L211` (`in_time_lock`); `request_copy.py:request:L56`; `preflight/checks/security.py:TimeLockWindowCheck.run:L117-118` (`get` default 18; **own wrap formula** L122) | A17, A20 | F |
| `copy_protection.time_lock_end` | 151 | 8 | 8 | same sites | A17, A20 | F |
| `copy_protection.max_sessions_for_copy` | 152 | 2 | 2 | `copy_gate.py:check_copy_allowed:L227`; `request_copy.py:request:L73` | A17 | F |
| `copy_protection.token_path` | 153 | home-directory path: not reproduced | `_ROOT/data_store/security/copy_token.json` (L56) | `copy_gate.py:read_token:L179` (and L187, L195) | A17 | F |
| `copy_protection.audit_log_path` | 154 | home-directory path: not reproduced | `_ROOT/…/copy_audit.log` (L57) | `copy_gate.py:audit:L258`; `security_monitor.py:check_copy_bypass:L843`, `_append_copy_audit:L1230`; `system_manager.py:security_check:L824` | A17, A15 | F |
| `copy_protection.sentinel_dir` | 155 | data_store | "data_store" | `copy_gate.py:send_alert:L298` | A17 | F |

Read by code but absent from the YAML (defaults apply):
- `security.config_dir`: default `_ROOT/config` (L130), used at `check_nse_holiday_calendar:L963`.
- `security.authorized_keys_path`: default is a home-directory path, not reproduced (L142), used at `check_authorized_keys:L635` and `approve_ssh_keys.py` L76, L81.
- `expected_key_fingerprints`: set only by the operator override (L133, L204).

### 2.29 `config/preflight.yaml` — not loaded centrally — 1 leaf

| Key | L | Value | Default | Consumers | Owner | Class / notes |
|---|---|---|---|---|---|---|
| `startup_floors.min_broker_cash_rs` | 38 | 2000 | `MIN_BROKER_CASH_RS_DEFAULT` 2000.0 (L41) on a missing file, an unreadable file or a null value | `scripts/preflight/checks/broker.py:_min_broker_cash_rs:L58` (`float()`), used in `run:L380-393` | A20 | F. The value equals the code default. The header L36-37 says the check is alert-only (HISTORICAL claim). |

### 2.30 `config/expected_managers.yaml` — not loaded centrally — 414 leaves

The consumer is `core/effect_telemetry.py` (A15). One row per field pattern is given below because the consumer reads every entry the same way. Per-entry lines follow the table.

| Key pattern | Leaves | Lines | Read by code? | Consumers | Notes |
|---|---|---|---|---|---|
| `version` | 1 | 25 | no | — | **N** |
| `frozen_at` | 1 | 26 | no | — | **N** ("2026-08-01") |
| `frozen_against` | 1 | 27 | no | — | **N** ("297b587") |
| `managers[].name` | 70 | 31-386 | yes | `assert_composition:L169-180`; `emit_census:L244, L289` | F |
| `managers[].state` | 70 | 34-386 | yes | `assert_composition:L173, L180, L192`; `emit_census:L245` (an unknown state is surfaced at L287) | F. State counts at the baseline: expected-active 18, covered-existing 1, expected-event-driven 5, expected-dormant 20, expected-absent 8, infra 18. |
| `managers[].modes` | 1 | 385 | yes | `_mode_exempt:L148` (`startswith("live-only")`) | F |
| `managers[].reason` | 30 | 183-366 | partly | `emit_census:L280`, only in the expected-dormant mismatch branch (20 of the 30 entries are dormant) | F (dormant entries only). One stale `yaml:NNN` reference (L211) can reach that output (section 3.7). |
| `managers[].class` | 70 | 32-386 | no | — | **N** (documentation) |
| `managers[].ctor` | 62 | 33-386 | no | — | **N.** The line references are **stale** at the baseline (section 3.7). |
| `managers[].effect_point` | 44 | 35-329 | no | — | **N** |
| `managers[].acted_means` | 44 | 36-330 | no | — | **N** |
| `managers[].note` | 18 | 37-386 | no | — | **N** |
| `managers[].flip_note` | 2 | 324, 332 | no | — | **N** |

Per entry (name line → state):
- **expected-active:** 31 kill_switch, 38 fund_manager, 45 position_sizer, 51 risk_engine, 57 signal_processor, 64 secondary_screener, 70 quality_scorer, 76 hard_gate, 83 order_placer, 90 limit_protocol, 97 order_monitor, 104 order_reconciler, 111 eod_squareoff, 118 sr_detector, 124 v3_chain_runner, 130 pb01_capture_worker, 136 pb01_entry_stage, 142 portfolio_allocator.
- **covered-existing:** 149 webhook_receiver.
- **expected-event-driven:** 157 mis_blocklist, 163 drift_handler, 169 pb01_would_be_runner, 317 cnc_gtt_placer, 325 cnc_gtt_monitor.
- **expected-dormant:** 177 entry_gate, 184 smart_tgt, 191 tgt_retry, 198 co_protocol, 205 shadow_tracker, 212 live_feed, 219 candle_persist, 226 sizer.risk_bind, 233 sizer.live_margin, 240 risk.sector_cap_bound, 247 risk.daily_loss_gate, 254 fm.daily_loss_post_trade, 261 fm.invariant_violation, 268 fm.bucket_overflow, 275 fm.commit_hard_kill, 282 drift.soft_rung, 289 drift.hard_rung, 296 scorer.tier_high, 303 scorer.score_gt_ceiling, 310 placer.emergency_exit.
- **expected-absent:** 335 breakeven_manager, 339 sl_breach_monitor, 343 structure_exit_manager, 347 market_regime_runner, 351 zone_cache, 355 zone_warmer, 359 retest_monitor, 363 retest_diverter.
- **infra:** 369-386 (state_store … ohlc_fetchers, 18 entries).

The registry's flag-dependent states agree with the `system_config.yaml` file values at the baseline:
- `sr_detector` (enabled true) and `v3_chain_runner` (mode shadow) are expected-active.
- `pb01_capture_worker` and `pb01_entry_stage` (watchlist enabled true) and `portfolio_allocator` (shadow) are expected-active; `pb01_would_be_runner` (watchlist enabled true) is expected-event-driven.
- `shadow_tracker` (enabled false) is expected-dormant.
- `structure_exit_manager`, `market_regime_runner` and zone/retest are expected-absent (their flags are false).

## 3. Cross-cutting findings

### 3.1 Keys with no functional consumer

These are FACT about grep results: no code uses these values to change behaviour. Display-only, assign-only and read-then-skipped reads are noted in brackets. The consumer column of each row explains the search.

- **`system_config.yaml` (15):**
  - `eod_squareoff.auto_resume_kill_switch`
  - `alerts.telegram.personal_chat_id_env`
  - `alerts.telegram.whitelist_only`
  - `regime.index_symbol` (assigned only)
  - `v3_chain.min_pass_score` (display only), `v3_chain.medium_score_threshold`, `v3_chain.high_score_threshold`
  - `watchlist.playbook_scanner`
  - `watchlist.entry_tf` (literal used instead)
  - `entry_gate.max_spread_pct`, `entry_gate.min_depth_qty`, `entry_gate.liquidity_check_enabled`
  - `live_feed.max_reconnect_attempts` (display only), `live_feed.reconnect_backoff_base_seconds`, `live_feed.reconnect_backoff_max_seconds`
- **`broker_limits.yaml` (2):** `backoff_sequence_sec`, `timeouts.connect_sec`.
- **`expected_managers.yaml` (243 leaves):** `version`, `frozen_at`, `frozen_against`, and every `class`, `ctor`, `effect_point`, `acted_means`, `note` and `flip_note`. These are documentation fields.
- **`security.yaml` (2):** `watched_files[0].severity` (never read: the entry is skipped at L748-749, before the severity read at L750) and `watched_files[0].path` (read at L747 only to be skipped).
- **`broker_costs.yaml`, `preflight.yaml`:** none.
- **`slippage_model.yaml`:** no live consumer; all 4 leaves are paper-only.

### 3.2 Keys read by code but absent from the YAML (the default applies)

| File | Key | Default (loader line or code) | Read at |
|---|---|---|---|
| system_config | `alerts.watcher_interval_sec` | 60 (L1108) | `alert_watcher.py:main:L815` (`getattr` default 60; the CLI `--interval` overrides; `deploy/systemd/alert-watcher.service` L24-25 passes `--loop` without `--interval`) |
| system_config | `alerts.watcher_heartbeat_path` | None (L1109) | `alert_watcher.py:main:L816-817` → `_write_heartbeat:L735` returns, so the heartbeat is off |
| system_config | `alerts.respawn_restart_delta_threshold` | 3 (L1112) | `monitoring_canary.py:run_canary:L271` (`getattr` default `_RESPAWN_MIN_DELTA` 3, L152) |
| system_config | `alerts.respawn_rate_per_hour_threshold` | 6.0 (L1113) | `monitoring_canary.py:run_canary:L270` (default `_RESPAWN_MAX_PER_HOUR` 6.0, L151) |
| system_config | `alerts.smtp.password` | "" (L890) | `SmtpConfig.resolved_password:L949` (only when `password_env` is empty) |
| system_config | `sr_detector.pivot_n_by_tf`, `volume_bins`, `volume_node_frac`, `breakout_avg_window`, `weak_breakout_frac`, `retest_sl_buffer_pct`, `touch_cap`, `recency_window_days`, `recency_min_factor`, `max_queue`, `max_zones_logged` | the defaults in section 2.9 | section 2.9 |
| system_config | `regime.slope_lookback`, `regime.swing_pivot_n` | 5, 3 | section 2.10 |
| system_config | `v3_chain.regime_pref_direction`, `regime_pref_day_type`, `regime_pref_volatility` | the maps in section 2.12 | `runner.py:regime_fraction:L324-326` |
| security | `security.config_dir`, `security.authorized_keys_path` | code defaults (section 2.28) | `security_monitor.py` L963, L635 |

No loader field in `broker_limits`, `broker_costs` or `slippage_model` is absent from its file, and no file key is unknown to the loader. This was checked by script.

### 3.3 Values that a consumer overrides, ignores or replaces

1. `eod_squareoff.auto_resume_kill_switch` is ignored: the resume is unconditional when EOD set the soft-kill (`orders/eod_squareoff.py:_fire:L536-544`).
2. `smart_tgt.enabled`:
   - `SmartTgtManager` is built with the literal `enabled=True` (`M` L2979).
   - The CO_PLUS_TGT registration does not check the flag (`order_placer.py:_handle_entry_fill:L2204-2208`).
   - The flag only changes the Telegram text (`place:L1746-1750`).
3. `entry_gate.liquidity_check_enabled`, `max_spread_pct` and `min_depth_qty` are not passed. `OrderPlacer` uses its ctor defaults False / 0.5 / 500 (L589-591).
4. `live_feed.*` is not passed. `LiveFeedManager` uses its ctor defaults: 10 attempts and `reconnect_delay_sec` 5 as the maximum delay (`data/live_feed.py` L45-46, L516).
5. `watchlist.entry_tf` is replaced by the literal `_TF_5` (`pb01_entry.py` L44). `watchlist.capture_fetch_lookback_days` is not the capture fetch window: the capture uses `v3_chain.fetch_lookback_days` through the shared fetcher (`M` L3730). The watchlist fetcher TTL is a literal `0.0` (`M` L3732).
6. `regime` fetcher cache TTL = `sr_detector.cache_ttl_sec` (`M` L3523). The regime section has no TTL key of its own.
7. `scripts/sr_level_export.py` L152-155 overrides `enabled`, `intraday_anchors_enabled`, `anchor_intraday_interval` and `orb_window_minutes` in a `model_copy` (offline tool).
8. `eod_cleanup.signal_retention_days` can be overridden from the CLI (not done by the cron line). `fno_ban.url` can be overridden from the CLI. A failed config load in `fetch_fno_ban.py` silently falls back to the literal URL and fail-open (L313-322).
9. The 33 `TelegramNotifier.from_env` / `from_config` call sites in 31 files (main.py L331, `alerts/cron_alerts.py` L111, `ops/control_tower`, `reports/daily_report.py` L1916 and 28 call sites in 26 `scripts/` files) ignore the YAML `max_retries`, `retry_backoff_seconds`, `rate_limit_per_minute`, `send_deadline_seconds`, `channels`, `bot_token_env`, `failed_alerts_log_path`, `sentinel_dir` and `email_fallback`. They use ctor defaults and hard-coded env-var names (`telegram_notifier.py:from_env:L288-297`). Only `alerts.telegram.enabled` is honoured, through a direct YAML read.
10. `security.expected_ssh_keys` / `expected_key_fingerprint` are replaced when the operator baseline file exists (`apply_operator_ssh_baseline:L200-210`). `security.watched_files[0]` is skipped by label (L748-749), so its `severity` is never read and its `path` has no effect.
11. `ZoneWarmer` queue size: the ctor default 512 is used and `sr_detector.max_queue` is not passed (`M` L3564-3568; `zone_warmer.py` L42).
12. Generic: `config_validator` registers every key, but no module reports usage (see the method notes).

### 3.4 One setting read differently in different places

| Setting | Place A | Place B | Difference |
|---|---|---|---|
| `alerts.telegram.enabled` | loader, strict (`M` L2636) | direct YAML, fail-open True (`telegram_notifier.py` L81-102) | A malformed file is fatal for main but treated as "enabled" for cron notifiers. |
| alert retry / rate-limit / deadline | YAML values (main app) | ctor defaults (all `from_env` users) | Same numbers at the baseline (3 / 2.0 / 20 / 8.0); they would diverge if the YAML changed. |
| `strategy_circuit_breaker.enabled` | `StrategyGovernor` default True | `capacity.py` L259 default False | Display default only. |
| `smart_tgt.enabled` | `OrderPlacer` `getattr` default False | `capacity.py` L304 default False; loader REQ | — |
| `scanner_check_delay_sec` | loader default 5.0 | `startup_checks.py` L1591 `getattr` default 0.0 | — |
| `logging.min_free_disk_gb` | loader REQ | `run_all_startup_checks` param default 1.0 (L1526) | — |
| `eod_squareoff.limit_grace_sec` | `EodSquareoff`: float, full sleep | `MisAutoSquareoff`: `int()`, clipped to room | — |
| `eod_squareoff.exit_protocol` | loader / ctor default "MARKET" | file "LIMIT_THEN_MARKET"; the `orders/eod_squareoff.py` docstring L1041 calls LIMIT_THEN_MARKET the default | — |
| copy time-lock | `copy_gate.in_time_lock` (start == end means no lock) | `preflight/checks/security.py` L122 `(h >= start) or (h < end)` | Different formulas for the same keys. |
| "Minimum Eligible Score" label | `controls.py:_limits:L202` → `v3_chain.min_pass_score` | `config_view.py` L640 → `scoring_weights.yaml` `min_pass_score` | Two sources under one label. |
| `alerts.telegram_enabled` (non-existent path) | `ops_dashboard/backend/services/controls.py:build_controls_screen:L293, L327-328`; `operations.py:build_controls_summary:L53` | real key `alerts.telegram.enabled` | The dashboard always gets None and shows "UNKNOWN" (INTERPRETATION). |
| `sr_detector.band_buffer_pct` default | loader 0.1 / `zone_builder` 0.1 | `ScoringParams` dataclass 0.0 (`confluence.py` L58) | Matters only if a caller builds `ScoringParams` directly. |

### 3.5 Duplicated settings across files or sections

1. **Sentinel directory `data_store`:** `alerts.sentinel_dir` (system_config L381), `security.sentinel_dir` (security L121), `copy_protection.sentinel_dir` (security L155), and literals in `main.py` L354, the `from_env` ctor default L201, `cron_watchdog.py` L67, `gemini_log_review.py` L275 and `cron_officer.py` L154.
2. **SMTP:** `alerts.email_fallback.smtp_host` / `smtp_port` / `use_tls` duplicate `alerts.smtp.host` / `port` / `use_tls` (same values, two credential env names).
3. **Score thresholds 60 / 65 / 80:** `v3_chain.min_pass_score` / `medium_score_threshold` / `high_score_threshold` and `scoring_weights.yaml` `min_pass_score` / `medium_score_threshold` / `high_score_threshold` (L22, L29, L28) carry the same names and values in two files.
4. **Consecutive API-failure limit 3:** `circuit_breaker.max_api_failures` (OrderMonitor → HARD_KILL) and `kill_switch.api_failure_threshold` (YAML L356 → soft-kill).
5. **SL buffer 0.2:** `sr_detector.sl_buffer_pct` and `structure_exit.sl_buffer_pct`, plus the unconfigured `sr_detector.retest_sl_buffer_pct` 0.3.
6. **Timeframes and lookbacks:** `sr_detector.timeframes` and `v3_chain.structure_intervals` (same list); `sr_detector.lookback_days` and `v3_chain.fetch_lookback_days` (180); 1800-second TTLs in `sr_detector.cache_ttl_sec`, `zone_cache_ttl_sec`, `retest_timeout_sec` and `v3_chain.fetch_cache_ttl_sec`.
7. **Price bands:** `slippage_bands` (6 labels), `slippage_control.tiers` (4 bands: 100 / 200 / 500 / open) and the dashboard `_PRICE_BUCKETS` (5 buckets).
8. **Broker cost rates:** the `broker_costs.yaml` rates are repeated as literal defaults in `reports/daily_report.py` L355-361.
9. **F&O ban URL:** YAML, loader default (L1834) and `fetch_fno_ban.py` `_DEFAULT_URL` (L70).
10. **Telegram and SMTP env-var names:** the YAML names (`bot_token_env`, `chat_id_env`) are repeated as literals in `telegram_notifier.py:from_env` L288-289, `monitoring_canary.py` L265, and the `TELEGRAM_*` users found by grep (`cron_officer.py`, `liveness_probe.py`, `reconcile_pnl.py`, `reconcile_positions.py`, `preflight/checks/config_integrity.py`, `premarket_healthcheck.py`).
11. **`security.yaml` defaults:** every key is repeated as a dataclass default in `SecConfig` / `CopyConfig`. The preflight literals 18 / 8 repeat `time_lock_start` / `time_lock_end`. `preflight.yaml` 2000 = `MIN_BROKER_CASH_RS_DEFAULT`.
12. **A02 tool literals:** `revert_temp_config.py` repeats the current values of `order_reconciler.capital_drift_tolerance` and the three `drift_handler` thresholds as `prod_value`.
13. **MIS protection bands:** `eod_squareoff.mis_pass_*_market_protection_percent` bounds are enforced in the loader and again at the adapter (deliberate, loader docstring L721-723).

### 3.6 Direct readers that bypass the central loader

| Reader | File read | Keys |
|---|---|---|
| `alerts/telegram_notifier.py:_read_telegram_enabled:L81-102` | system_config.yaml | `alerts.telegram.enabled` |
| `reports/daily_report.py:load_report_data:L143-161` | system_config.yaml, scoring_weights.yaml, broker_costs.yaml | `excluded_symbols`; `min_pass_score`; `zerodha.*` |
| `ops_dashboard/backend/readers/config_reader.py:get_system_config:L45-52` (fallback) and `get_broker_costs:L311-335` | system_config.yaml, broker_costs.yaml | all |
| `core/config_auditor.py` L833-840 (raw YAML for group B) | system_config.yaml | not in this range |
| `scripts/cron_officer.py` L472, L507 | system_config.yaml | not in this range (`trade_type`, `force_intraday_only`, `position_sizing`) |
| `scripts/security_monitor.py`, `copy_gate.py`, `request_copy.py` (via `CopyConfig`), `approve_ssh_keys.py` and `system_manager.py` (via `SecConfig`), `preflight/checks/security.py` | security.yaml | section 2.28 |
| `scripts/preflight/checks/broker.py:_min_broker_cash_rs` | preflight.yaml | `startup_floors.min_broker_cash_rs` |
| `core/effect_telemetry.py:_load_registry` | expected_managers.yaml | `managers[].name`, `state`, `modes`, `reason` |

Scripts that call `load_all()` themselves are not bypassing the loader, but each loads its own copy. They include `alert_watcher`, `monitoring_canary`, `cron_officer`, `liveness_probe`, `eod_broker_reconcile`, `eod_cleanup`, `fetch_fno_ban`, `v3_shadow_soak_report`, `forward_shadow_record`, `system_manager` (L1317-1318; reads `alerts.sentinel_dir` L1340 and `entry_gate.slippage_control` L976), `sr_level_export` (L130, L139; reads `sr_detector.*` and `broker_limits` L144) and `t2_cnc_gtt_realtest` (L156, L159; `broker_limits` L169).

### 3.7 `expected_managers.yaml` line references vs the baseline

FACT: the registry's `ctor` and `yaml:NNN` references do not match the baseline files. The registry was last changed at `0197923` (2026-08-04) and is "frozen against 297b587" (L27). `main.py` and `system_config.yaml` were last changed at `ea0e506` / `5f75c9b` (2026-09-10).

| Registry reference | Baseline position |
|---|---|
| `sr_detector.enabled yaml:407` (L120) | YAML L509 |
| `v3_chain_mode yaml:472` (L126) | L574 |
| `watchlist.enabled yaml:518` (L132) | L620 |
| `allocator_mode yaml:463` (L144) | L565 |
| `shadow.enabled yaml:402` (L211) | L504 |
| `structure_exit_enabled yaml:532` (L346) | L634 |
| `regime.enabled yaml:446` (L350) | L548 |
| `wait_for_retest_enabled yaml:427` (L354) | L529 |
| `kill_switch main.py:1861` (L33) | `KillSwitch(` at main.py L2243 |
| `eod_squareoff main.py:2844` (L113) | `EodSquareoff(` at L3300 |
| `drift_handler main.py:3332` (L165) | `CapitalDriftHandler(` at L3853 |

The YAML references are consistently +102 lines out. The references inside `ctor` values (L33, L113, L120, L126, L132, L144, L165) are never read by code. The `yaml:NNN` text inside a `reason` field is read only for an expected-dormant entry whose counter is above 0 (`core/effect_telemetry.py` `emit_census` L279-284; the text before "—" is taken at L280). So the L211 reference (`shadow_tracker`, expected-dormant; text "SH13 shadow.enabled=false (yaml:402)") can be printed in a census MISMATCH(ii) line, while the L346, L350 and L354 references (expected-absent entries) are never read (section 2.30).

## 4. Totals

Class key for this table: F = functional consumer; P = paper-only; N = no functional consumer (display-only, assign-only and read-then-skipped reads included).

| File | Leaf keys | ≥1 consumer (F) | Paper-only (P) | No functional consumer (N) | Overrides / ignores found (section 3.3) |
|---|---|---|---|---|---|
| `system_config.yaml` L359-753 (24 sections) | 227 | 207 | 5 | 15 | 11 items (3.3 items 1-9, 11, 12) |
| `broker_limits.yaml` | 16 | 14 | 0 | 2 | 1 (`timeouts.read_sec` applied only to main's live `KiteConnect`) |
| `broker_costs.yaml` | 15 | 15 | 0 | 0 | 0 overrides; 1 duplicate computation (`daily_report`) |
| `slippage_model.yaml` | 4 | 0 live | 4 | 0 | 0 |
| `security.yaml` | 52 | 50 | 0 | 2 | 2 (operator SSH baseline override; `watched_files[0]` skipped) |
| `preflight.yaml` | 1 | 1 | 0 | 0 | 0 |
| `expected_managers.yaml` | 414 | 171 (`name` 70, `state` 70, `modes` 1, `reason` 30) | 0 | 243 | 0 |

Per-section split for `system_config` (F / P / N):

| Section | Leaves | F / P / N |
|---|---|---|
| eod_squareoff | 8 | 7 / 0 / 1 |
| alerts | 36 | 33 / 1 / 2 |
| logging | 1 | 1 / 0 / 0 |
| order_reconciler | 7 | 7 / 0 / 0 |
| eod_reconcile | 2 | 2 / 0 / 0 |
| eod_cleanup | 1 | 1 / 0 / 0 |
| tgt_retry | 4 | 4 / 0 / 0 |
| shadow_tracker | 3 | 3 / 0 / 0 |
| sr_detector | 34 | 34 / 0 / 0 |
| regime | 15 | 14 / 0 / 1 |
| portfolio_allocator | 7 | 7 / 0 / 0 |
| v3_chain | 39 | 36 / 0 / 3 |
| watchlist | 10 | 8 / 0 / 2 |
| structure_exit | 6 | 6 / 0 / 0 |
| smart_tgt | 5 | 5 / 0 / 0 |
| entry_gate | 27 | 24 / 0 / 3 |
| slippage_bands | 1 | 1 / 0 / 0 |
| paper | 4 | 0 / 4 / 0 |
| drift_handler | 4 | 4 / 0 / 0 |
| strategy_circuit_breaker | 4 | 4 / 0 / 0 |
| circuit_breaker | 3 | 3 / 0 / 0 |
| live_feed | 3 | 0 / 0 / 3 |
| fno_ban | 2 | 2 / 0 / 0 |
| scanner_check_delay_sec | 1 | 1 / 0 / 0 |

"F" includes consumers whose branch is inactive at the file values, for example the `flat_tiers` keys and everything behind a false master flag. Fields read by code but absent from the files (section 3.2): 21 in `system_config` (alerts 5, sr_detector 11, regime 2, v3_chain 3), checked by script; 2 in `security.yaml` (`config_dir`, `authorized_keys_path`), plus the override-only `expected_key_fingerprints`.
