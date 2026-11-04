# A01 evidence: catalogue of the startup checks in utils/startup_checks.py

**Status:** DRAFT — evidence for the A01 STUDY, for ChatGPT's review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04. Corrected, 2026-11-04: after an independent check of the statements against the code.
**Purpose and scope:** Every check function in `utils/startup_checks.py` (1,692 lines): its lines, what it checks, its pass, warning, failure and skip outcomes, retries, its call sites, and whether anything calls it; the scenario detection; the aggregate runner and how `main.py` consumes its report. It supports the STUDY, sections 6, 10 and 12 (Q12, Q13, Q15 and Q32 of ChatGPT's A01 direction).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on 04-Nov-2026; nothing was run.

Conventions: lines are in `utils/startup_checks.py` unless a path is given. Every row is FACT for the lines it cites, unless a cell says INTERPRETATION. Call sites were found with `git grep` over the whole repository at the baseline; "tests" counts the files under `tests/` (A19) that name the function. Configuration values quoted from `config/` are file facts only; the values in force are UNKNOWN / NOT ESTABLISHED. No check retries: none of the functions below contains a retry loop.

## 1. Module contents

- INTERPRETATION (docstring L1 to L37): the module calls itself a "pure library" of pre-trading checks for Phase 0c and Phase 0d. It claims no state mutation, no `sys.exit`, no subsystem start, no import of the store, kill switch or broker (all injected; "SC13 Layer 6"), "no side effects beyond logging" (SC1) and determinism (SC14), and it lists nine locked checks (SC5 to SC12). Section 6 compares these claims with the code.
- FACT: module state: `_IST`, a fixed +05:30 timezone (L58), is defined and never used in the module (grep); `_logged_none_warnings`, a mutable module-level set (L643); `_REQUIRED_CONFIG_FILES_STATIC` (L833 to L843).
- FACT: imports `core.exceptions` (L51); `strategies.loader` and `strategies.schema` are imported lazily inside `check_strategy_configs` (L1271 to L1272).

Classes (FACT; the line of each `@dataclass(frozen=True)` decorator is the line before the class line):

| Class | Lines | Content |
|---|---|---|
| `StartupScenario` (Enum) | L65 to L70 | COLD, WARM, CRASH, HALT |
| `StartupScenarioResult` | L78 to L86 | scenario, previous session date, kill state and reason, shutdown-marker flag and time, detection details |
| `ClockCheckResult` | L90 to L97 | passed, skew, tolerance, broker time, local time, error |
| `DbPermissionResult` | L101 to L107 | passed, DB path and directory, errors, suggested `chown` commands |
| `ConfigHashResult` | L111 to L116 | changed, changed files, previous and current hashes |
| `ScannerCheck`; `ScannerPreflightResult` | L120 to L127; L131 to L134 | per-scanner result; `all_reachable` and the results |
| `WebhookEndpointResult` | L138 to L142 | reachable, status code, response body (there is no `detail` field) |
| `DiskSpaceResult` | L146 to L151 | passed, free GB, minimum GB, error |
| `NtpCheckResult` | L155 to L163 | passed, skipped, drift, warn and block thresholds, host, error |
| `StartupReport` | L167 to L185 | the aggregate result returned by `run_all_startup_checks` |
| `StartupCheckFailed(ConfigError)` | L956 to L963 | the exception raised by the two boot guards called directly from `main.py`; a `TradingSystemError` subclass |
| `SdkVersionResult`; `HolidayCalendarResult`; `TempConfigResult` | L1301 to L1306; L1358 to L1363; L1458 to L1462 | results of checks 12, 11 and 14 |

## 2. Scenario detection: `detect_startup_scenario` (L192 to L382)

Inputs: `state_store.get_session_row()` (L214; the single row id=1, `core/state_store.py` L2474 to L2480; A03), `kill_switch.status()` keys `state`, `reason`, `triggered_at` (L237 to L240; A13), today's SHUTDOWN event (L310; `core/state_store.py` L2482 to L2500, which matches `SUBSTR(timestamp, 1, 10)` to the date) and today's EOD square-off log (L338 to L340; A12). The result is logged at INFO and returned; the caller writes any event (docstring L211 to L212).

| Step | Condition (lines) | Result |
|---|---|---|
| 1 | no session row (L217 to L228) | COLD, with `kill_state="INACTIVE"`, before any kill state is read |
| 2 | kill state HARD_KILL (L243 to L260) | HALT, whatever the date |
| 3 | kill state SOFT_KILL triggered today, or with a missing or unparseable time (L263 to L286; `_soft_kill_condition_cleared`, L385 to L397) | HALT; a SOFT_KILL from an earlier day falls through, still reported as `kill_state="SOFT_KILL"` |
| 4 | previous session date unparseable, or earlier than today (L230 to L234, L290 to L307) | COLD |
| 5 | same day, a SHUTDOWN event dated today exists (L310 to L329) | WARM |
| 6 | same day, no SHUTDOWN event, today's EOD square-off log COMPLETE (L336 to L365; a lookup failure is logged at WARNING, L341 to L344) | WARM |
| 7 | otherwise (L367 to L382) | CRASH |

- FACT: a previous session date later than today is not handled separately; it reaches the same-day branch at step 5.
- Callers (FACT): `main.py` L2268 (then CRASH writes `CRASH_DETECTED` at L2277 to L2282, and HALT returns 4 unless `--resume`, L2283 to L2292); the aggregate, step 3 (L1561). `core/state_store.py` L2477 and L2486 name it in docstrings only. Tests: 2 files.

## 3. The aggregate runner: `run_all_startup_checks` (L1508 to L1692)

- FACT: called once, at `main.py` L2451 to L2474 (the other `main.py` hits, L104, L225 and L2432, are the import, a docstring and a comment; `signals/webhook_receiver.py` L329 is a comment). Tests: 4 files.
- FACT: `today_date` comes from `time_authority.now_ist().date()` (L1548); `main.py` passes the `core.time_authority` module object (`main.py` L2454). Every step runs; the runner does not stop at the first failure. It has no try of its own (AST), so an exception that escapes a check ends the runner and reaches `main.py` (startup trace, S28). `ok` is True only when no step added a blocking entry (L1662). It logs INFO "run_all_startup_checks: OK scenario=... warnings=..." or WARNING "... FAILED blocking=..." (L1664 to L1672) and returns a `StartupReport` (L1674 to L1692).
- FACT: the docstring lists nine checks (L1531 to L1541); the code runs 16 steps, in this order:

| # | Step (definition lines) | Runner lines | Result entry | Skip condition | In `main.py`'s flow (FACT, with INTERPRETATION where marked) |
|---|---|---|---|---|---|
| 1 | `check_config_files_present` (L846 to L872) | L1550 to L1553 | blocking `missing_config_files` | - | INTERPRETATION: a missing YAML has already stopped `load_all` (exit 5, `main.py` L2197 to L2201), and accounts.csv has been read at `main.py` L2359 and L2414; here it can newly catch `instruments.csv` and the IST-year holiday file |
| 2 | `check_required_secrets` (L1071 to L1086) | L1555 to L1558 | blocking `missing_secrets` | - | names from `main.py` L219 to L232 |
| 3 | `detect_startup_scenario` (L192 to L382), a second time | L1560 to L1565 | blocking `halt_requires_resume` | - | runs after the session row was rewritten at `main.py` L2308; INTERPRETATION: its session date is today, so it can only return WARM, CRASH or HALT, not COLD, unless the boot crosses midnight IST between `main.py` L2255 and L1548, which only a start that bypasses the START window allows |
| 4 | `check_clock_skew` (L414 to L468) | L1567 to L1575 | blocking `clock_skew` | - | the first broker call of the boot (`broker/zerodha_adapter.py` L1709 to L1728; A04) |
| 5 | `check_config_hash` (L581 to L634), a second time | L1577 to L1580 | warning `config_hash_changed` | - | INTERPRETATION: compares against the hashes `main.py` has just written (L2312), so it cannot report a change |
| 6 | `check_market_holiday_today` (L879 to L904) | L1582 to L1585 | warning `market_holiday` | - | INTERPRETATION: detects weekends only (section 4, row 6); on a weekend the `main()` holiday guard has normally exited already |
| 7 | `check_scanner_connectivity` (L652 to L745) | L1587 to L1597 | warning `scanner_unreachable` | the runner's own scenario is COLD (L1589) | INTERPRETATION: the skip applies only to a boot that crosses midnight IST (step 3); otherwise it runs on every boot |
| 8 | `check_webhook_endpoint` (L783 to L826) | L1599 to L1604 | result stored; no warning or blocking entry | `webhook_url` falsy (L1601) | `main.py` passes `webhook_url=None` (L2461): always skipped here; `main.py` calls the function itself at L4005 |
| 9 | `check_instrument_cache_size` (L911 to L949) | L1606 to L1613 | blocking `instrument_cache_too_small` | `instrument_cache is None` (L1608) | `main.py` passes None after a failed pre-load (L2439 to L2449), so the check is skipped then, not failed |
| 10 | `check_strategy_configs` (L1266 to L1293) | L1615 to L1618 | blocking `invalid_strategy_configs` | - | `main.py` then sends the strategy alert (L2494 to L2500) |
| 11 | `check_holiday_calendar` (L1366 to L1450) | L1620 to L1623 | warning `holiday_calendar_issues` | - | - |
| 12 | `check_sdk_version` (L1309 to L1350) | L1625 to L1628 | blocking `sdk_version_mismatch` | - | reads `config_dir.parent / "requirements.txt"` (L1626) |
| 13 | `check_ntp_sync` (L506 to L574) | L1630 to L1641 | blocking `ntp_clock_skew` (drift of 5 s or more); warning `ntp_clock_drift_warning` (2 s or more) | a failed query sets `skipped`; no warning or blocking entry is added (the result is still stored in `report.ntp`, L1689) | host `pool.ntp.org`, warn 2.0 s, block 5.0 s, hard-coded at L1632 to L1637 |
| 14 | `check_temp_config_values` (L1465 to L1501) | L1643 to L1646 | warning `temp_config_values(N)` | - | - |
| 15 | `check_disk_space` (L1192 to L1259) | L1648 to L1653 | blocking `insufficient_disk_space` | `log_dir` None (L1650) | `main.py` passes `Path("logs")` (L2467) and `system.logging.min_free_disk_gb` (L2473; file value 2.0, `config/system_config.yaml` L466) |
| 16 | `check_db_permissions` (L1093 to L1185) | L1655 to L1660 | blocking `db_permission_error` | `db_path` None (L1657) | `main.py` passes `str(Path("data_store/trading_system.db"))` (L2466), after the store was opened at L2233 |

How `main.py` consumes the report (FACT, grep): it reads only `report.ok`, `report.blocking_failures` and `report.warnings`. With `--dry-run` it prints all three, closes the store and returns 0 or 3 (`main.py` L2476 to L2482). If `ok` is False it logs CRITICAL, sends the strategy alert when `invalid_strategy_configs` is listed, closes the store and returns 3 (`main.py` L2484 to L2502). Outside `--dry-run`, `report.warnings` is used only in the runner's own INFO line; `report.scenario` and the other fields are never read.

## 4. Every check function

| # | Function (lines) | What it checks | Pass | Warning | Failure | Skip | Non-test call sites | Tests (files) | Anything calls it? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `check_config_files_present` (L846 to L872) | seven YAML files, `instruments.csv` and `accounts.csv` (L833 to L843) plus `nse_holidays_<year>.yaml`, the year taken from UTC plus 05:30 (L859 to L866), exist under `config_dir` | empty list | one WARNING log per missing file (L868 to L871) | the runner adds `missing_config_files` | - | the runner only (`main.py` L2435 is a comment) | 2 | yes, through the runner |
| 2 | `check_required_secrets` (L1071 to L1086) | each named environment variable is set and non-empty (`not os.environ.get(key)`, L1083) | empty list | one WARNING per missing name; values are never logged (L1084) | the runner adds `missing_secrets` | - | the runner only | 1 | yes, through the runner |
| 3 | `check_clock_skew` (L414 to L468) | `broker_adapter.get_server_time()` (L436), then `time_authority.assert_clock_at_startup(broker_ts)` (L437), which raises `ClockSkewTooLarge` when the absolute skew exceeds `startup_max_sec` (`core/time_authority.py` L283 to L295) and otherwise records the sample (L297 to L299). `tolerance_sec` is used for the report only (docstring L428 to L431) | `passed=True` | - | `ClockSkewTooLarge` → `passed=False`, WARNING (L445 to L458); any other exception, such as a broker, authentication or network failure, → `passed=False`, ERROR log, skew 0.0 (L459 to L468) | - | the runner only. A same-named but separate function: `scripts/premarket_healthcheck.py` L119; `scripts/preflight/checks/vm_health.py` holds a check ported from it under another name (`VmNtpSyncCheck`, L118) (A20); `broker/zerodha_adapter.py` L1706 is a docstring | 2 | yes, through the runner |
| 4 | `check_ntp_sync` (L506 to L574) | one query to the NTP host (`_query_ntp_time`, L475 to L503: one NTPv3 UDP request to port 123, the server transmit time); drift = the absolute difference from `time.time()` (L547 to L548), without round-trip compensation | drift below warn: INFO | drift at or above warn and below block: `passed=True` with a WARNING log (L556 to L560); the runner adds `ntp_clock_drift_warning` | drift at or above block: `passed=False`, CRITICAL (L551 to L555); the runner adds `ntp_clock_skew` | a failed query: `passed=True`, `skipped=True`, WARNING log (L533 to L545); the runner adds no warning or blocking entry | the runner only | 1 | yes, through the runner |
| 5 | `check_config_hash` (L581 to L634) | the JSON dict in `session.last_config_hash` against `app_config.file_hashes` (L594 to L622) | `changed=False` | `changed=True`; the files listed, sorted (L618 to L627) | - | no previous hashes, or a stored value that is not valid JSON or not a dict: WARNING for invalid JSON, treated as a first run, `changed=False` (L597 to L616) | `main.py` L2295; the runner | 3 | yes |
| 6 | `check_market_holiday_today` (L879 to L904) | weekend (L891 to L896); otherwise `today.isoformat() in market_windows.holidays` (L898 to L902) | False | True: the runner adds `market_holiday` | - | - | the runner only | 1 | yes, through the runner. INTERPRETATION: `main.py` passes the `MarketWindows` object (`main.py` L2456), whose `holidays` is a set of `date` objects (`core/market_windows.py` L67); a string is never equal to a date, so only weekends return True. The docstring expects a list of strings (L887 to L888) |
| 7 | `check_scanner_connectivity` (L652 to L745) | optional sleep `delay_sec` (L676 to L678); then, for each entry of `scan_webhook_map.scanners` in turn (L687), the URL from the entry's `chartink_url`, a plain string, a dict, or the `chartink_scanners` fallback (`_resolve_url`, L764 to L776), fetched with `http_fetcher_fn(url, 10.0)` (L657, L702) | every status 2xx (L703) | any scanner unreachable: the runner adds `scanner_unreachable`. The first `None` status per scanner is logged at WARNING and later ones at DEBUG, across calls, through the module-level set (L706 to L717); other statuses always at WARNING (L718 to L722) | - | no URL for a scanner: recorded as unreachable, `no_url_configured` (L689 to L699); an exception: unreachable, WARNING (L731 to L742) | the runner (delay `getattr(app_config.system, "scanner_check_delay_sec", 0.0)`, L1591; file value 5.0, `config/system_config.yaml` L753; schema default 5.0, `core/config_loader.py` L2026); `scripts/preflight_scanner_check.py` L203 to L208 (operator script, A06) | 2 | yes. FACT: the committed map has 16 scanner entries (`config/scan_webhook_map.yaml` L16 to L84) |
| 8 | `check_webhook_endpoint` (L783 to L826) | `http_fetcher_fn(url, 5.0)` on the given `/health` URL | status 2xx or 401 (L807 to L809) | - | any other status: WARNING, `reachable=False` (L810 to L819); an exception: WARNING, unreachable (L820 to L826) | the runner skips it when `webhook_url` is falsy (L1601) | `main.py` L4005 (after the server starts and a 2 s sleep, L4003); the runner (skipped at boot) | 4 | yes, `main.py` L4005 |
| 9 | `check_instrument_cache_size` (L911 to L949) | `instrument_cache.count() >= min_rows` (default 1000, L914; the runner's `min_instrument_rows`, L1523, which `main.py` does not pass); `count()` is called outside any try (L936) | `(True, count)`, INFO | - | `(False, count)` below the minimum, WARNING (L937 to L943); `(False, 0)` for None (L930 to L934) | the runner skips it for None (L1608) | the runner only | 1 | yes, through the runner |
| 10 | `check_paper_capital_consistency` (L966 to L1014) | paper only: adapter margins against the fund manager total | - | - | raises `StartupCheckFailed` on divergence (paper) | live: returns at once (L989 to L990) | `main.py` L2769 (exit 3 at L2775 to L2778) | 2 | yes; a no-op in live |
| 11 | `check_kill_switch_present` (L1017 to L1064) | `kill_switch is not None` | INFO (L1040 to L1045) | paper with None: WARNING (L1047 to L1053) | live with None: CRITICAL and `StartupCheckFailed` (L1055 to L1064) | - | `main.py` L2885 (exit 3 at L2886 to L2889) | 1 | yes. INTERPRETATION: cannot raise as wired; `kill_switch` is built at `main.py` L2243 and never reassigned (grep) |
| 12 | `check_db_permissions` (L1093 to L1185) | the DB directory exists and is readable and writable (L1126 to L1131); the `.db`, `-wal` and `-shm` files, where present, are readable and writable (L1133 to L1166) | INFO (L1176 to L1177) | - | any problem: CRITICAL per problem and suggested `chown` commands on non-Windows systems (L1169 to L1175); a `-wal` file without the `.db` file returns at once as "CORRUPTED STATE" (L1142 to L1152) | the runner skips it when `db_path` is None (L1657) | the runner only | 1 | yes, through the runner |
| 13 | `check_disk_space` (L1192 to L1259) | creates `log_dir` (L1219), then free space from `shutil.disk_usage` (L1220) against the minimum | INFO (L1241 to L1244) | - | below the minimum: CRITICAL plus a direct stderr write (L1223 to L1239); any exception: ERROR, failed (L1251 to L1259) | the runner skips it when `log_dir` is None (L1650) | the runner only. A same-named but separate function: `scripts/premarket_healthcheck.py` L104; `scripts/preflight/checks/vm_health.py` holds a check ported from it under another name (`VmDiskDataCheck`, L101) (A20) | 1 | yes, through the runner |
| 14 | `check_strategy_configs` (L1266 to L1293) | `config_dir/"strategies"` exists (L1276 to L1280) and `StrategyLoader().load_all_strategies(...)` loads it, with the loader's default `force_intraday_only` (L1282 to L1284) | empty list, INFO | - | missing directory, or any exception from the loader: CRITICAL, one error string (L1276 to L1291) | - | the runner only (`strategies/loader.py` L80 is a docstring) | 2 | yes, through the runner |
| 15 | `check_sdk_version` (L1309 to L1350) | the `kiteconnect==` pin in the requirements file (L1320 to L1327) against `importlib.metadata.version` (L1338) | the versions match; or no pin found, which includes a missing requirements file (L1333 to L1335) | - | a read failure (L1328 to L1331), the package not installed (L1339 to L1342), or a different version (L1344 to L1347) | - | the runner only | 1 | yes, through the runner |
| 16 | `check_holiday_calendar` (L1366 to L1450) | `nse_holidays_<year>.yaml` for the year of the IST date passed in (L1384 to L1385): it exists, parses, has a `holidays` list of at least `min_holidays` (10, L1370) entries, with no duplicates and every date in the year (L1389 to L1444) | `passed=True`, INFO | any problem is added to its warnings, `passed=False`: the runner adds `holiday_calendar_issues` | - | - | the runner only | 2 | yes, through the runner |
| 17 | `check_temp_config_values` (L1465 to L1501) | counts the text `# TEMP` in `config_dir/*.yaml` and `config_dir/strategies/*.yaml` (L1477 to L1487); a file that cannot be opened or read (`OSError`) is skipped (L1486); a file that is not valid UTF-8 raises `UnicodeDecodeError`, which is not caught | no marker | markers found: the runner adds `temp_config_values(N)` | - | - | the runner only | 1 | yes, through the runner |

Helpers (FACT): `_soft_kill_condition_cleared` (L385 to L397) is True only when the SOFT_KILL time is on an earlier day; `_parse_ts` (L400 to L407) returns None for an unparseable time; `_query_ntp_time` (L475 to L503) has no caller other than `check_ntp_sync` and no test; `reset_scanner_warnings` (L646 to L649) clears the module-level set and has no non-test caller (its docstring says it is for tests); `_get_scanners_dict`, `_get_chartink_dict` and `_resolve_url` (L748 to L776) look up scanner URLs.

## 5. Which checks can change the outcome of a boot

- FACT: the boot can be stopped only by a blocking entry in the report (exit 3, `main.py` L2484 to L2502), by `--dry-run` (exit 3 when not ok), or by the two direct guards (exit 3). Warnings never stop a boot.
- INTERPRETATION, from the code order: in `main.py`'s flow, the runner's step 8 is always skipped, step 5 cannot report a change, step 3 cannot return COLD except across midnight IST (so the step-7 skip applies only then), step 6 can report weekends only, check 10 is a no-op in live and check 11 cannot raise as wired.
- FACT: twelve of the check functions are reached only through the runner (functions 1 to 4, 6, 9 and 12 to 17 of section 4); function 7 is reached through the runner and the operator script.

## 6. Docstrings and comments compared with the code (INTERPRETATION of each difference; the code is FACT)

- The runner's docstring lists 9 checks (L1531 to L1541); the code runs 16 steps.
- `check_ntp_sync`'s docstring says the warn band gives `passed=False` (L520 to L523); the code sets `passed = drift < block_sec` (L549), so the warn band passes and the runner turns it into a warning (L1640 to L1641).
- The `NtpCheckResult` comment "e.g. paper mode" for `skipped` (L158) has no matching code; `skipped` is set only when the query fails (L533 to L545).
- `check_temp_config_values`'s docstring says it blocks "when capital > 25K (checked by caller in run_all_startup_checks)" (L1471 to L1472); the runner adds only a warning and has no capital input (L1643 to L1646).
- `check_config_files_present` says it runs "before attempting Pydantic parsing" (L853 to L855); `load_all` has already parsed the configuration at `main.py` L2198.
- `check_disk_space` says it "Should be called BEFORE setup_logging()" and that the caller "should exit with code 1" (L1198, L1201, L1213); it runs after `setup_logging` (`main.py` L2178), and a failure gives exit 3.
- `check_db_permissions` says it runs "before StateStore init" (L1098); the store is opened at `main.py` L2233 to L2237 and written at L2308.
- `check_market_holiday_today` expects `holidays` to be a list of ISO strings (L887 to L888); `main.py` passes `MarketWindows`, whose `holidays` is a set of dates.
- The comment in `check_webhook_endpoint` (L799 to L806) cites `main.py:3238` and `:3241` and says a failure "made main.py fire _shutdown_event"; at the baseline the self-check is at `main.py` L4004 to L4005, and its failure branch degrades the boot and writes a sentinel without shutting down (`main.py` L4006 to L4054).
- The `main.py` comment at L2434 to L2438 says a present but corrupt `instruments.csv` makes the check block with `instrument_cache_too_small`; the runner skips the check for None (L1608), and the boot then reaches `assert instrument_cache is not None` (`main.py` L2506).

## 7. Side effects, compared with the "no side effects beyond logging" claim (FACT)

- `check_disk_space` creates `log_dir` (L1219) and writes to stderr (L1229 to L1231).
- `check_scanner_connectivity` sleeps (L676 to L678), mutates the module-level set (L712), and makes one HTTP request per scanner through the injected fetcher.
- `check_clock_skew` makes a broker API call through the adapter, which takes a rate-limiter token (`broker/zerodha_adapter.py` L1717; A04), and appends a sample to the time authority's module-level window (`core/time_authority.py` L297 to L299).
- `check_ntp_sync` sends UDP traffic to a public NTP host (L492 to L495).
- `check_strategy_configs` imports `strategies.loader` and `strategies.schema` lazily (L1271 to L1272); `StrategyConfig` is imported there and not used.
