# A01 evidence: the existing technical records checked against the code

**Status:** APPROVED — evidence for the A01 STUDY, approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30)
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04. Corrected, 2026-11-04: after an independent check of the statements against the code. Approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30): status marked APPROVED; content unchanged.
**Purpose and scope:** The check of the two existing technical records that describe A01 matters, `01_SYSTEM_OVERVIEW.md` and `03_STARTUP_RUNTIME_AND_SCHEDULER.md` (Document 08, section 9), against the code at the baseline: one row per claim, with the record line, the claim, the code evidence and the result. It supports the STUDY, Appendix A (index rule 6; Decision Register, D-21).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on 04-Nov-2026; nothing was run. The two records were read, unchanged, in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/` (184 and 321 lines).

## 1. The records and their stated basis (HISTORICAL)

- HISTORICAL: both records state their evidence basis on their line 3: a PC worktree at commit `e7bf477` with an uncommitted `force_qty` change set, "byte-equivalent" to the testing VM as delivered on 17-Sep-2026 at 19:31 IST. Their machine-side facts come from testing-VM captures of 17-Sep-2026, 20:06 IST, and they say that the production host was never read (`01_SYSTEM_OVERVIEW.md` L3; `03_STARTUP_RUNTIME_AND_SCHEDULER.md` L5). Their evidence date is 18-Sep-2026 (`01_SYSTEM_OVERVIEW.md` L4; `03_STARTUP_RUNTIME_AND_SCHEDULER.md` L6). Record 03 adds that its line numbers hold "for the files as read, not for e7bf477 alone" (L3).
- HISTORICAL: `01_SYSTEM_OVERVIEW.md` L164 describes `e7bf477` as `970aabf` plus the S&R shadow files, and L27 and L153 say that the code of the production host is known only from records, at `970aabf`.
- FACT: `git cat-file -t e7bf477` fails in the clone. That commit is not in the legacy repository, and other repositories are out of bounds (Decision Register, D-12).
- Consequence (D-21): the records describe the testing copy, so each of their statements is checked here against the code at `970aabf`, the study baseline. Whether production ran `970aabf` is UNKNOWN / NOT ESTABLISHED.

## 2. Method and labels

- The records are HISTORICAL documents. They are checked here; they are not evidence of how the code works (Master System Investigation Index, rule 6).
- Result labels: MATCH; DIFFERS (how); PARTLY (which part); NOT CHECKABLE FROM CODE (runtime only); OUTSIDE A01 (the owner topic; not checked); paper-only (not traced, under the Live-only rule). Each result is FACT from the cited baseline lines unless it says INTERPRETATION.
- Line anchors: the records' anchors are for their own tree. Each was re-located at `970aabf`, and a different line number alone is not a DIFFERS (section 3).
- The check was made by an AI helper under the same read-only rules as the STUDY. The DIFFERS results R1-08, R3-92 and R3-117, and a sample of the others (R1-04, R1-07, R1-09, R1-10, R1-12, R1-23, R1-38, R3-05, R3-07 and R3-40), were re-checked against the code for this file. R3-08 rests on the behaviour of a library that is not in the repository and remains an OPEN QUESTION.
- Account identifiers, addresses, absolute paths and e-mail addresses that appear in the records or the code are named generically and not copied.

## 3. The records' tree is not the baseline

FACT, at `970aabf` (the records' figures are HISTORICAL):

| Measure | At 970aabf | In the records |
|---|---|---|
| `main.py` | 4,293 lines | 4,329 |
| Whole tree | 734 `.py` files, 283,180 lines | 757 modules, 289,044 lines (Record 01 L33) |
| `sr_shadow/` package | does not exist | listed by Record 01 L46 |
| `utils/` | 5 files, 2,290 lines | the same |
| `core/` | 26 `.py` files, 13,050 lines | 26 modules, 13,145 lines |

FACT: every `main.py` anchor in both records, except the two listed below the table, re-locates onto `970aabf` at a constant offset within each region of the file:

| Region at 970aabf | Sample anchors (record → 970aabf) | Offset |
|---|---|---|
| L1 to L1573 | 185→185, 650→650, 865→865, 1270→1270, 1305→1305, 1573→1573 | 0 |
| L1599 to L1686 (the `_shutdown` signature to the webhook stop) | 1631→1630, 1646→1645, 1687→1686 | +1 |
| L1768 to L2840 | 1776→1768, 1839→1831, 1866→1858, 2093→2085, 2209→2201, 2459→2451, 2848→2840 | +8 |
| L2896 to L3458 | 2906→2896, 3008→2998, 3310→3300, 3417→3407, 3468→3458 | +10 |
| L3575 | 3609→3575 | +34 |
| L3839 to L4249 | 3874→3839, 3915→3880, 4003→3968, 4129→4094, 4284→4249 | +35 |
| L4278 to L4293 | 4314→4278, 4323→4287, 4326→4290, 4329→4293 | +36 |

- FACT: two anchors do not fit the map. Record 03 L143 cites ":218", one line before the definition at L219; Record 03 L67 cites ":2104", which under +8 lands on L2096 (the `--version` return), not on the argparse conversion at L2092.
- INTERPRETATION: the offsets place the records' 36 extra `main.py` lines as follows: one in the `_shutdown` signature and seven inside `_shutdown` (between L1686 and L1768), two between the PositionSizer and RiskEngine constructions, about twenty-four before SignalProcessor (between L3458 and L3575), one between SignalProcessor and EntryGate, and one in the `_shutdown(...)` call (1 + 7 + 2 + 24 + 1 + 1 = 36). This fits the records' own account that `force_qty` touches `main.py` and that `e7bf477` adds the S&R shadow files. What those lines contain is UNKNOWN / NOT ESTABLISHED.

## 4. Claims in `01_SYSTEM_OVERVIEW.md` (IDs R1-nn)

| ID | Record line | Claim (paraphrase) | Code evidence at 970aabf | Result |
|---|---|---|---|---|
| R1-01 | L10, L12 | Scanners post signals; the system sizes, places, supervises, squares off, reconciles and reports; two books (MIS/CO and CNC) | n/a | OUTSIDE A01 (A06, A07, A09-A12, A15) |
| R1-02 | L12 | Runs in one of two modes | main.py `_parse_args` L184 to L187; interactive picker `_interactive_select_mode` L1913 to L1925 | MATCH |
| R1-03 | L16 | Paper: no Kite client; quote provider and simulator | main.py L2352 to L2353, L2394 (branch point only) | Paper-only, not traced |
| R1-04 | L17 | Live: accounts.csv read, API-key env var aliased, token file "read and validated", real KiteConnect built (2367 to 2383) | main.py L2354 to L2375 (L2359 registry pre-read, L2361 alias, L2362 to L2363 `load_token` and subscript, L2375 `_build_kite_client` L381 to L390); `is_token_valid` only at L2546 to L2552 | PARTLY. The read, the alias and the build MATCH. At this site the token is only loaded, not validated. Validation (account, IST date, non-empty token; `scripts/zerodha_login.py` L60 to L77) happens later, at L2546 to L2552, after the startup checks at L2451. For the missing-file path see R3-92 |
| R1-05 | L19 | CLI default is paper (185 to 186) | main.py L184 to L187 | MATCH |
| R1-06 | L19 | The unit starts it with `--mode live` | n/a | OUTSIDE A01 (A17), not checked |
| R1-07 | L29 | accounts.csv is tracked: 704 bytes, 6 lines, last changed 13eb727 on 2026-06-12; five accounts, one primary; env-var names, paper capital and capital share | git metadata at 970aabf: 704 bytes, 6 lines, last commit 13eb727 on 2026-06-12. Counts only, no values copied: 5 rows, 1 primary; the header is exactly the 10 columns required by `core/account_registry.py` `AccountRegistry.load` L110 to L114 | MATCH. The file is config content (A02); only its shape was checked against the A01 loader |
| R1-08 | L33 | 757 modules, 289,044 lines; 200 reachable from the service and 38 scheduled scripts | 734 `.py` files, 283,180 lines (git ls-tree) | DIFFERS on totals (different tree, section 3). The reachable set was not re-derived (the scheduled-script set is A16) |
| R1-09 | L39 | `core`: 26 modules, 13,145 lines | `core/`: 26 files, 13,050 lines | PARTLY. The count MATCHes; the lines DIFFER by 95 (INTERPRETATION: fits the record's modified `core/config_loader.py`) |
| R1-10 | L43 | `main`: 1 module, 4,329 lines, the single composition root and boot sequence | main.py: 4,293 lines; docstring L1 to L9; `main` L2085 to L2190; `_main_locked` L2193 to L4278 | PARTLY. The role MATCHes; the line count DIFFERS |
| R1-11 | L46 | `sr_shadow` package, 11 modules | no `sr_shadow/` at 970aabf | OUTSIDE A01 (S&R, A08). Absence recorded in section 3 |
| R1-12 | L47 | `utils`: 5 modules, 2,290 lines; startup checks, holiday guard, heartbeats | `__init__` 1, `cron_heartbeat` 209 (A16), `holiday_guard` 131, `instance_lock` 257, `startup_checks` 1,692 | MATCH |
| R1-13 | L65 | main.py builds the Kite session; 10 modules import kiteconnect | main.py `_build_kite_client` L381 to L390, called at L2375 (live) | PARTLY. The main.py part MATCHes; the import census is OUTSIDE A01 (A04) |
| R1-14 | L66 to L69, L71 to L72 | Streaming, Chartink, Telegram, SMTP, F&O ban list, instrument dump | n/a | OUTSIDE A01 (A05, A06, A14, A16) |
| R1-15 | L70 | Holiday calendar: a per-year YAML in config/, read by the boot guard before anything else | main.py L2099 to L2102 (`config` unless `--config`); `utils/holiday_guard.py` `_load_holiday_set` L44 (`nse_holidays_<year>.yaml`). Only argparse and `--version` run first (L2089 to L2096) | MATCH |
| R1-16 | L74 | waitress is the HTTP server | main.py L3987 to L4000 (`waitress.serve` in a daemon thread) | MATCH |
| R1-17 | L74 | fcntl/msvcrt for the cross-platform instance lock | `utils/instance_lock.py` `_lock_fd_exclusive` L88 to L104, `_unlock_fd` L107 to L117 | MATCH |
| R1-18 | L74 | flask, pydantic, openpyxl, pyotp, cachetools | n/a | OUTSIDE A01 (A06, A02, A15, A04) |
| R1-19 | L80 to L82 | Three databases and their tables | n/a | OUTSIDE A01 (A03; `sr_shadow.db` is A08, a component absent at 970aabf) |
| R1-20 | L84 | Store opened once at boot; the only sanctioned migrator; migration only off-market | main.py L2226 to L2237: one `StateStore(...)` in main.py, with `allow_migrate=True` and `market_open=` computed from weekday and trading_hours (L2228 to L2232). No other non-test file passes `allow_migrate=True` (grep) | MATCH for the boot-path call. Pragmas and refusal rules are OUTSIDE A01 (A03) |
| R1-21 | L88 | The day table's schedule column is the installed crontab (42 entries) | n/a | OUTSIDE A01 (A16); HISTORICAL (section 7) |
| R1-22 | L98 | 08:00-18:15 is the start window; outside it the process exits 0 without loading config (2170, 2184) | main.py L2000 to L2001, `_within_service_window` L2004 to L2015, guard L2154 to L2176, all before `load_all` at L2198 | MATCH |
| R1-23 | L100 | 09:15: the in-process margin re-sync thread fires (source given as `trading_hours.market_open`; 4148) | main.py `_start_market_open_margin_sync_thread` L973 to L1039: target `_MARKET_OPEN = _time(9, 15)` at L994; returns at once if started at or after 09:15 or on a holiday (L997 to L1007). Started at L4113 to L4121 | PARTLY. The thread and the 09:15 time MATCH. The source DIFFERS: the time is hard-coded and does not follow `trading_hours.market_open` |
| R1-24 | L102, L104, L106 to L108 | entry_start, entry_end, eod_entry_cutoff, 15:17 sequence, market_close | n/a | OUTSIDE A01 (A02 values; A06, A12 use) |
| R1-25 | L105 | 15:09 cutoff, with the in-process notifier and auto square-off ahead of it (3353, 3369) | main.py L3328 to L3337 (`MisSquareoffTiming.build` from `trading_hours.mis_squareoff_*`), L3343 to L3357 (notifier built, boot self-test, polling started), L3359 to L3380 (auto square-off built, polling started) | MATCH (wiring). Timing and behaviour are OUTSIDE A01 (A12) |
| R1-26 | L111 | 17:35 is the service's own clean-shutdown time, taken only if no position requires the service (4177, 1305) | main.py L2211 (parse), L4142 (passed), `_eod_self_exit_due` L1230 to L1326 (due only if the count is 0, L1305) | MATCH (wiring and gate). The 17:35 value is OUTSIDE A01 (A02); the value in force is NOT CHECKABLE FROM CODE |
| R1-27 | L92 to L97, L99, L101, L103, L109 to L110, L112 | Cron rows | n/a | OUTSIDE A01 (A16) |
| R1-28 | L116 to L129 | Trade path steps 1-12 | n/a | OUTSIDE A01 (A06-A12, A14, A15) |
| R1-29 | L135 | Kill-switch semantics, persistence and recovery | n/a | OUTSIDE A01 (A13) |
| R1-30 | L135 | Prior-day and scheduled kills auto-clear at boot (2251, 2268, 2273) | main.py L2243 to L2251 (construct), L2260 `clear_stale_state`, L2265 `auto_clear_scheduled_kill` | MATCH (call sites and order). The clearing rules are OUTSIDE A01 (A13) |
| R1-31 | L136 | Both boot guards return 0 before configuration is loaded | main.py L2150 and L2176, both before L2198 | MATCH |
| R1-32 | L137 | "15 checks run by the aggregator (17 exist in the module; two are not called)", including the four secret names; a blocking failure is exit 3 | `utils/startup_checks.py` `run_all_startup_checks` L1508 to L1692 (AST parse: 17 `check_*` defined, 15 distinct called once each); main.py L2430, L2451 to L2474, L2484 to L2502; direct calls at L2769 and L2885 | PARTLY. 17/15 and exit 3 MATCH. "Not called" is true only for the aggregator: main.py calls `check_paper_capital_consistency` (L2769) and `check_kill_switch_present` (L2885) directly, each leading to exit 3. "15 run" overstates the boot: see R3-79 |
| R1-33 | L138 | Config auditor runs inside validation "and twice more once strategies are loaded; a BLOCK finding fails the boot" (3447, 3468) | main.py L3436 to L3443 runs only if `structure_exit_enabled is True` and acts only on `A4_structure_exit_trailing_sl` (exit 3). L3458 to L3465 runs only if `delivery_enabled is True` and acts only on `A5_delivery_without_conditional_allocation` (exit 3) | PARTLY. Both re-runs exist (group "A", with strategies), but each is conditional and fails the boot on one finding code, not on any BLOCK. The in-validation run is OUTSIDE A01 (A02) |
| R1-34 | L139, L140 | Capital invariant; Cron Officer and drift check | n/a | OUTSIDE A01 (A09, A16) |
| R1-35 | L141 | Effect telemetry: census asserted at boot and reported at EOD (4275, 4279, 1666) | main.py L4223 to L4242 (registration), L4243 to L4246 (`assert_composition`), L1662 to L1675 (`emit_census` in `_shutdown`) | MATCH (wiring). The census is emitted at every clean stop through `_shutdown`; the code calls it "the EOD census". Internals are OUTSIDE A01 (A15) |
| R1-36 | L145, L146 (first part), L148, L149 | No own signals; NSE equities only; EOD exits not waited for; not started from cron | n/a | OUTSIDE A01 (A06, A05/A10, A12, A16) |
| R1-37 | L146 | A broker other than zerodha in accounts.csv is fatal exit 9 (2580) | main.py L2561 to L2572 (selected account only; case-insensitive) | MATCH |
| R1-38 | L147 | No unattended run across a year boundary without a new holiday file: the filename carries the year and the guard reads it first | `utils/holiday_guard.py` L44, L92 to L95; main.py L2100 (host-local `date.today()`), L2151 to L2152 (`FileNotFoundError` means proceed); `utils/startup_checks.py` L859 to L866 and L1551 to L1553 (blocking, IST year), L1621 to L1623 (calendar check is a warning only) | PARTLY. The year in the filename and the guard order MATCH. The guard itself does not stop the boot on a missing file. A block comes first from `load_all`, which requires the file of the host-local year (main.py L2197 to L2201, exit 5; `core/config_loader.py` L2449 and L2484; A02); `check_config_files_present` (exit 3) requires the IST year's file. INTERPRETATION: a missing next-year file alone does not stop a boot on a year-end weekend (STUDY, section 9.5) |
| R1-39 | L153 to L156 | What could not be established | n/a | NOT CHECKABLE FROM CODE (section 7) |
| R1-40 | L160 to L184 | Appendix 01-A: testing-VM divergences and file counts | n/a | OUTSIDE A01; HISTORICAL (section 7) |

## 5. Claims in `03_STARTUP_RUNTIME_AND_SCHEDULER.md` (IDs R3-nn)

Record-internal note (FACT about the record): Record 03 L34 sends the reader to "the clean-shutdown path of §3.9"; §3.9 is the scheduler section, and the shutdown path is in §3.11.2.

| ID | Record line | Claim (paraphrase) | Code evidence at 970aabf | Result |
|---|---|---|---|---|
| R3-01 | L12 to L19 | systemd and cron start work independently; nothing in cron starts the service; the token watcher can | n/a | OUTSIDE A01 (A16, A17, A04), not checked |
| R3-02 | L25 to L37 | Unit directives: `--mode live`, EnvironmentFile, `KillSignal=SIGINT`, `TimeoutStopSec=30`, `Restart=on-failure`, `RestartPreventExitStatus=3 4 5` | n/a | OUTSIDE A01 (A17), not checked. A01 code comments give the value as "3 4" (main.py L3456; `utils/instance_lock.py` L8); the sources disagree, for A17 to resolve |
| R3-03 | L34 | `systemctl stop` runs the same handler as Ctrl+C | main.py `_install_signal_handlers` L1570 to L1579: one handler for SIGINT and SIGTERM sets `_shutdown_event` | MATCH (handler). The unit side is OUTSIDE A01 (A17) |
| R3-04 | L39 to L51 | Repo vs installed unit drift; one unit only on the machine | n/a | OUTSIDE A01 (A17); HISTORICAL |
| R3-05 | L55 | Boot runs in three regions: import, `main()` (2093 to 2198), `_main_locked()` (2201 to 4314) | main.py module level (L22 to L116, L865 to L867); `main` L2085 to L2190; `_main_locked` L2193 to L4278 | MATCH |
| R3-06 | L55 | 154 steps traced and re-checked | n/a | NOT CHECKABLE FROM CODE (record method) |
| R3-07 | L59 | main.py never calls `load_dotenv()`; it imports `scripts.zerodha_login` (L106), which runs a bare `load_dotenv()` (its L36) | main.py: no `load_dotenv` (grep count 0); import at L106; `scripts/zerodha_login.py` L32, L36 (A04 file, handoff lines only) | MATCH |
| R3-08 | L59 | "No explicit path, so resolution is relative to the process working directory" | `requirements.txt` L14 pins python-dotenv 1.2.2. Library source of `find_dotenv` read from version 1.2.3, as installed in the study environment | DIFFERS. INTERPRETATION about library behaviour, not shown by repository code: without `usecwd`, `find_dotenv()` starts at the calling module's directory (`scripts/`) and walks upward. It uses the CWD only when `usecwd=True`, in an interactive session, under a trace hook, or when frozen. The version installed on the VM is UNKNOWN. OPEN QUESTION |
| R3-09 | L61 | Redundant under systemd; the only loader when run by hand and "may find nothing"; which path supplied each variable is UNKNOWN | n/a | NOT CHECKABLE FROM CODE (unit A17; environment in force). The "may find nothing" part conflicts with R3-08 |
| R3-10 | L63 | A module-level `ThreadPoolExecutor(2)` for entry-gate work (865) | main.py L865 to L867 (`_gate_release_pool`), used at L887 | MATCH |
| R3-11 | L63 | Entry point is `sys.exit(main())` (4323) | main.py L4285 to L4293 (L4287) | MATCH |
| R3-12 | L65 | Four things happen before any log file exists | main.py L2089 to L2176 precede `setup_logging` at L2178 | MATCH |
| R3-13 | L67 | Flags: `--mode` (default paper), `--resume`, `--config`, `--status`, `--dry-run`, `--version`, `--interactive` | main.py `_parse_args` L179 to L212 | MATCH |
| R3-14 | L67 | An argparse SystemExit becomes exit 5 (2209; "return 5 if se.code != 0 else 0" at 2104) | main.py L2089 to L2092 | PARTLY. The logic MATCHes: non-zero gives 5, zero (`--help`) gives 0. The ":2209" anchor maps (+8) to L2201, the config-load-failure `return 5`; ":2104" does not map onto L2092 |
| R3-15 | L68 | `--version` prints and returns 0 | main.py L2094 to L2096 | MATCH |
| R3-16 | L69 | Holiday guard: `is_trading_day` with `date.today()` (host local); on a non-trading day it prints a banner, writes a sentinel and returns 0; the weekend test comes before the file (`holiday_guard.py:92`); a missing file is caught and startup proceeds | main.py L2099 to L2152; `utils/holiday_guard.py` `is_trading_day` L85 to L95, `_load_holiday_set` L44 to L49 | MATCH. Not stated in the record: a once-a-day Telegram is sent by direct HTTPS (L2133 to L2149, L264 to L285). `next_trading_day` (L2103) also reads the file, so on a weekend a missing file also lands in the catch and startup proceeds |
| R3-17 | L70 | Start-window guard prints the window and returns 0; bypassed by `--status`, `--dry-run`, `--interactive`, `TS_IGNORE_MARKET_WINDOW=1`, `--resume`; its comment says it runs before `load_all` | main.py L2154 to L2176 (bypass L2157 to L2160; comment L2163 to L2165) | MATCH |
| R3-18 | L72 | The window is [08:00, 18:15); pure time-of-day; host-timezone independent per its docstring | main.py L2000 to L2001, L2004 to L2015. Input `time_authority.now_ist()` (L2161) uses a fixed UTC+05:30 offset (`core/time_authority.py` L58 to L59, L94 to L99) | MATCH |
| R3-19 | L72 | The upper bound is `SERVICE_WINDOW_END_MAX` = 18:15 (`config_loader.py:83`) | `core/config_loader.py` L83 (value only); main.py L57, L2001 | MATCH |
| R3-20 | L72 | The validator uses the same constant to bound the configured stop time (`:180`); the reason given is the forward-shadow cron time | n/a | OUTSIDE A01 (A02) |
| R3-21 | L74 | Both guards return before `setup_logging`, before the config load and before any secret is required | main.py L2150, L2176 < L2178 < L2198 | MATCH |
| R3-22 | L74 | Logging is configured only at 2186 | main.py L2178 (the only `setup_logging` call) | MATCH |
| R3-23 | L74 | The lock (2191) is an OS file lock plus a TCP bind on the loopback address, port 5001; failure is exit 1 (2194) | main.py L2183 to L2186; `utils/instance_lock.py` `acquire_instance_lock` L129 to L202 (flock/msvcrt on a lock file in the OS temp directory, L50 to L51 and L150 to L176; loopback bind and listen, L178 to L200; default port L55) | MATCH |
| R3-24 | L80 | 0b: `load_all` reads, hashes and validates every config file | main.py L2197 to L2202 (failure: log and exit 5 at L2201) | MATCH (call). Internals are OUTSIDE A01 (A02) |
| R3-25 | L81 | Config values registered for usage tracking | main.py L2205 | MATCH |
| R3-26 | L82 | The configured STOP time is parsed once and logged | main.py L2211 to L2216 | MATCH |
| R3-27 | L83 | 0c: StateStore opens the DB; this is the only sanctioned migrator | main.py L2226 to L2237 | MATCH (call). Rules are OUTSIDE A01 (A03) |
| R3-28 | L84 | Event bus constructed | main.py L2238 | MATCH |
| R3-29 | L85 | KillSwitch built and recovers persisted state | main.py L2243 to L2251 | MATCH (construction). Recovery is OUTSIDE A01 (A13) |
| R3-30 | L86 | TimeAuthority configured with skew thresholds | main.py L2254 calls `_init_time_authority` L360 to L378 | MATCH. Only the critical-skew callback is wired (section 8) |
| R3-31 | L87 | Prior-day kills and same-day scheduled kills auto-cleared | main.py L2260, L2265 | MATCH (calls). Rules are OUTSIDE A01 (A13) |
| R3-32 | L88 | Startup scenario: COLD, WARM, CRASH or HALT | main.py L2268 to L2292; `utils/startup_checks.py` `StartupScenario` L65 to L70, `detect_startup_scenario` L192 to L382 | MATCH |
| R3-33 | L89 | HALT without `--resume` is exit 4 | main.py L2283 to L2290 | MATCH |
| R3-34 | L90 | Config-hash diff against the last session row | main.py L2295; `check_config_hash` L581 to L634 (reads `last_config_hash`) | MATCH |
| R3-35 | L91 | Early session row written (`INSERT OR REPLACE ... id=1`) | main.py L2308 to L2314, via `_write_session` L619 to L633 | MATCH |
| R3-36 | L92 | 0d: market windows from trading_hours; state machine; rate limiter | main.py L2317 to L2329, L2346, L2348 | MATCH |
| R3-37 | L93 | Paper: no Kite client; quote provider | main.py L2352 to L2353, L2394 | Paper-only, not traced |
| R3-38 | L94 | Live: accounts.csv pre-read, env alias, token file read, KiteConnect built | main.py L2354 to L2375 | MATCH (normal path). Failure paths: R3-40, R3-92 |
| R3-39 | L95 | Broker adapter built, needed by the clock-skew check | main.py L2383 to L2411; `check_clock_skew` L414 to L468 calls `broker_adapter.get_server_time()` (L436) | MATCH |
| R3-40 | L96 | Full account-registry load; failure is exit 3 | main.py L2413 to L2423; `core/account_registry.py` `load` L91 to L211 | PARTLY. MATCH in paper. In live the live pre-read (L2359) reads the same file first. It raises `ConfigMissingError` or `ConfigSchemaError` (L104 to L108, L120 to L192), which are not caught there, so the top-level `except TradingSystemError` gives exit 1 (L4288 to L4290); a short row raises `AttributeError` instead (`core/account_registry.py` L135; STUDY, section 10.8), which gives exit 2 (main.py L4291 to L4293) |
| R3-41 | L97 | Required-secret names assembled | main.py L2425 to L2430 | MATCH |
| R3-42 | L98 | Instrument master pre-loaded from config/instruments.csv | main.py L2439 to L2449 (a load failure leaves `None`; section 8) | MATCH |
| R3-43 | L99 | The aggregate startup checks run: 15 of them | main.py L2451 to L2474 | PARTLY (see R3-79) |
| R3-44 | L100 | `--dry-run` prints the report and returns | main.py L2476 to L2482 (0 if ok, otherwise 3) | MATCH |
| R3-45 | L101 | Any blocking failure is exit 3 | main.py L2484 to L2502 (strategy-config alert first, L2494 to L2500) | MATCH |
| R3-46 | L102 | Live non-interactive token gate: missing or expired is exit 6 | main.py L2543 to L2554; `is_token_valid` L60 to L77 (A04 contract: account match, IST date equals today, non-empty token) | PARTLY. The gate's test covers an expired, wrong-account or empty token. In live it is reached only after the aggregate's clock check has made a broker call with the file's token (L2451; `broker/zerodha_adapter.py` L1716 to L1722); a token that the broker rejects ends the boot there with exit 3 (`utils/startup_checks.py` L459 to L468), so exit 6 is reached only for a token the broker accepted, for example one whose file has the wrong account id or date (whether Kite rejects a stale token is UNKNOWN from the code). A missing file never reaches this gate (R3-92) |
| R3-47 | L103 | Resolved config persisted to config_snapshots (idempotent) | main.py L2602 to L2614 (non-fatal) | MATCH (call). Idempotency is OUTSIDE A01 (A02) |
| R3-48 | L104 | 0e: Telegram notifier; notifier and adapter late-bound into the kill switch | main.py L2628 to L2642, L2648, L2653 | MATCH |
| R3-49 | L105 | Bucket split resolved; FundManager constructed and seeded | main.py L2702 to L2708, L2718 to L2736, L2755 to L2761 (live seed `compute_live_seed` L2074 to L2078) | MATCH (wiring). Capital internals are OUTSIDE A01 (A09) |
| R3-50 | L106 | Capital rehydration | main.py L2814 to L2825 (`CapitalStateInconsistent` gives exit 3) | MATCH (call). Internals are OUTSIDE A01 (A09) |
| R3-51 | L107 | PositionSizer, RiskEngine | main.py L2840 to L2863, L2896 to L2925 | MATCH. Between the two, `check_kill_switch_present` (L2884 to L2889, exit 3) is not mentioned |
| R3-52 | L108 | Live feed, candle store, shadow tracker, tick dispatcher | main.py L2927 to L2938, L2940 to L2943, L2946 to L2961, L2964 to L2971 | MATCH |
| R3-53 | L109 | Order monitor, GTT placer (with hydration), order placer, GTT monitor, reconciler, TGT retry | main.py L2998 to L3012, L3027 to L3039, L3061 to L3088, L3109 to L3121, L3124 to L3139, L3144 to L3155 | MATCH (wiring). Internals are OUTSIDE A01 (A10-A12) |
| R3-54 | L110 | Strategy YAMLs loaded; scoring and screening chain built | main.py L3157 to L3162, L3230 to L3298 | MATCH |
| R3-55 | L111 | EOD square-off (15:17 backstop) and MIS timing | main.py L3300 to L3321, L3328 to L3337 | MATCH (construction). The MIS notifier and auto-square-off pollers are also started here (L3355 to L3357, L3380). The 15:17 value is OUTSIDE A01 (A02/A12) |
| R3-56 | L112 | Webhook receiver constructed: "Flask object only" | main.py L3406 to L3415; served only at L3987 to L4000 | MATCH |
| R3-57 | L113 | Config auditor runs a second and a third time with strategies | main.py L3436 to L3443, L3458 to L3465 | PARTLY (as R1-33) |
| R3-58 | L114 | Signal processor and entry gate | main.py L3574 to L3623, L3839 to L3844 | MATCH |
| R3-59 | L115 | Event-bus subscriptions | main.py L3846 to L3858 (two: `KillSwitchActivated` to a log handler, `CapitalDriftDetected` to the drift handler) | MATCH. Other subscriptions are made inside component constructors (grep: `orders/order_placer.py` L693 to L700, `orders/slippage_recorder.py` L113 to L114) |
| R3-60 | L116 | 0f: `reconcile_once()` runs synchronously, then a stale-order sweep; "if it tripped the kill switch" the result is exit 1 | main.py L3880 to L3899 | PARTLY. The sequence MATCHes. The test is `kill_switch.is_active("any")` (L3894): any kill state active at that moment, whatever set it. `eod.post_wire_init()` (L3866) runs before the reconcile. A second synchronous `reconcile_once()` runs inside `order_reconciler.start()` (L3961; `orders/order_reconciler.py` L442), after this kill check, and no kill check follows it |
| R3-61 | L117 | 0g: candle store, tick feed, order-monitor re-tracking, fill-map rehydration, signal handlers, "then the threads" | main.py L3922, L3947, L3952, L3955, L3958, L3960 to L3977 | MATCH (order). Many daemons are already running from 0e (section 8) |
| R3-62 | L118 | A boot-order invariant is asserted: the reconcile ran first | main.py L3881 (flag), L3968 to L3971 (assert) | MATCH (see Concerns) |
| R3-63 | L119 | Webhook listener bound and started on Waitress | main.py L3979 to L4000 (host and port from `system.webhook`; 8 threads; connection limit 100; daemon thread "webhook-server") | MATCH |
| R3-64 | L120 | Sleep 2 s, self-check loopback `/health`; unreachable degrades the boot | main.py L4003 to L4054; `check_webhook_endpoint` L783 to L826 (2xx or 401 counts as reachable) | MATCH |
| R3-65 | L121 | Second listener: the health server on loopback, port 8080 | main.py L4073 to L4082 (`port=8080`, no host passed); the callee's default host is loopback (`scripts/healthcheck_server.py` L297 to L305; A15 handoff line only) | MATCH |
| R3-66 | L122 | EOD scheduler, 14:45 pre-alert, 09:15 margin re-sync, EOD self-exit watchdog | main.py L4094 to L4100, L4103 to L4110, L4113 to L4121, L4129 to L4161 | MATCH. 14:45 and 09:15 are hard-coded (L943, L994) |
| R3-67 | L123 | 0h: STARTUP row; session row rewritten; "System Active" Telegram | main.py L4167 to L4173, L4174 to L4180, L4181 to L4203 | MATCH |
| R3-68 | L124 | Composition-root registration and the composition assertion | main.py L4223 to L4246 | MATCH |
| R3-69 | L125 | Runtime: the main thread waits on a shutdown event | main.py L4249 | MATCH |
| R3-70 | L129 | `config_dir` is `--config` or the relative `config`; no environment variable, no fallback | main.py L2099 | MATCH |
| R3-71 | L131 to L139 | Eight-file registry, load order, strict models | n/a | OUTSIDE A01 (A02) |
| R3-72 | L131 | Strategy YAMLs loaded separately (3169) | main.py L3157 to L3162 | MATCH (call). The count of 16 is OUTSIDE A01 (A02/A07) |
| R3-73 | L133 | The record raises this as an issue of its own: the year comes from a naive `date.today()` in config_loader while the guard reads the calendar through its own path, so a year boundary depends on the host's local date in two places | main.py L2100; `utils/holiday_guard.py` L44, L94; `utils/startup_checks.py` L859 to L866 | PARTLY. The guard half MATCHes (host-local date). The config_loader half is OUTSIDE A01 (A02). At 970aabf the A01 code itself uses two derivations: host-local in the guard and IST (UTC+05:30) in `check_config_files_present` |
| R3-74 | L139 | Auditor inside validation; Group A re-run twice in main.py | as R1-33 | PARTLY (main.py part). Validation is OUTSIDE A01 (A02) |
| R3-75 | L143 to L145 | `required_startup_secrets` returns four names, required in both modes | main.py L219 to L232 | MATCH (the record's anchor is one line before the def) |
| R3-76 | L147 | The docstring records the C-2 (02-Jul-2026) reason for WEBHOOK_SECRET | main.py L220 to L226 | MATCH (docstring) |
| R3-77 | L147 | The enforcing check is at `startup_checks.py:1556`; a failure is exit 3 | `utils/startup_checks.py` L1555 to L1558; `check_required_secrets` L1071 to L1086 (unset or empty counts as missing); main.py L2484 to L2502 | MATCH |
| R3-78 | L149 | The aggregator calls exactly 15 distinct `check_*` functions, each once (list); the module defines 17; two are not called by the aggregator | AST parse at 970aabf; aggregator L1508 to L1692 | MATCH. The aggregator also calls `detect_startup_scenario` (L1561), which the list omits |
| R3-79 | L149 | "15 checks run" at boot | main.py L2451 to L2474 (`webhook_url=None` at L2461). Aggregator gates: scanner check only if its own scenario is not COLD (L1589); webhook check only if a URL is given (L1601); cache check only if the cache is not None (L1608) | PARTLY. At most 14 execute at boot. The webhook check never runs inside the aggregator at boot; main.py runs it itself after the server starts (L4005) |
| R3-80 | L157 | Webhook host and port come from config; the receiver's comment records the deployed endpoint (all interfaces, port 5000) | main.py L3979, L3992 to L3993 | MATCH (main.py part). The receiver comment is OUTSIDE A01 (A06); HISTORICAL |
| R3-81 | L158 | Health server is loopback-only by decision C-3 (`healthcheck_server.py:301`) | as R3-65 | MATCH |
| R3-82 | L159 | Instance lock: file lock plus loopback bind on 5001 | as R3-23 | MATCH |
| R3-83 | L160 | Poll threads: order monitor, reconciler, clock-skew probe (live only), token monitor, signal-processor pool, entry gate, smart-TGT, TGT retry | main.py L3960 to L3977; the probe is built only when not paper (L3905 to L3918) | MATCH |
| R3-84 | L161 | Timed daemons: MIS notifier, MIS auto square-off, EOD scheduler, 14:45, 09:15, self-exit | main.py L3357, L3359/L3380, L4094 to L4100, L4103, L4113, L4135 | MATCH. The list is incomplete (section 8) |
| R3-85 | L162 | Token monitor polls `kite.profile` every 1800 s in live; a no-op in paper | main.py L3388 to L3400 (`profile_fn=broker_adapter._kite.profile` in live; `check_interval_sec=1800`), started at L3964 | MATCH (wiring). Polling is OUTSIDE A01 (A04) |
| R3-86 | L168 | Exit 0: holiday or weekend, start window, `--version`, `--status` | main.py L2150, L2176, L2096, L650 (via L2299 to L2302) | PARTLY. The sites MATCH. The row omits the normal clean-shutdown return (L4278), `--dry-run` without blocking failures (L2482) and `--help` (L2092). `--status` reaches L650 only after the lock, the config load, the store open and the HALT test (HALT without `--resume` gives exit 4, L2283 to L2290) |
| R3-87 | L169 | Exit 1: lock failed; kill switch active after the reconcile; TradingSystemError at top level | main.py L2186, L3899, L4288 to L4290 | MATCH. The third site also catches most live accounts.csv failures; a short row gives exit 2 instead (R3-40) |
| R3-88 | L170 | Exit 2: unexpected exception at top level | main.py L4291 to L4293 | MATCH |
| R3-89 | L171 | Exit 3: startup failures, 7 sites | main.py `return 3` at L2423, L2502, L2778, L2825, L2889, L3443, L3465 (7), plus L2482 (`--dry-run`) | MATCH |
| R3-90 | L172 | Exit 4: HALT without `--resume` | main.py L2290 | MATCH |
| R3-91 | L173 | Exit 5: invalid arguments; interactive path with a missing credential variable | main.py L2092, L1898, L1901; also L2201 | PARTLY. The row omits the config-load failure (L2197 to L2201), which is where its ":2209" anchor points |
| R3-92 | L174 | Exit 6: live token file missing or expired; missing credential variable | main.py L2370, L2374, L2552; `scripts/zerodha_login.py` `load_token` L49 to L57 (returns `None` on any `OSError` or JSON decoding failure) | DIFFERS for "token file missing". FACT chain: `load_token` returns `None`; L2363 subscripts the result; only `FileNotFoundError` and `KeyError` are handled (L2364, L2371). The TypeError therefore reaches the top level, giving exit 2 (L4291 to L4293). INTERPRETATION: the `FileNotFoundError` branch (L2364 to L2370) cannot be reached from this read. MATCH for an expired or wrong-account token (L2552) and for a missing API-key variable (`KeyError` at L2361, then L2374) |
| R3-93 | L175 | Exit 7: interactive confirmation declined | main.py L1943 to L1946 | MATCH |
| R3-94 | L176 | Exit 8: account selection cancelled | main.py L1856 to L1858 | MATCH |
| R3-95 | L177 | Exit 9: a broker other than zerodha | main.py L2561 to L2572 | MATCH |
| R3-96 | L166 to L179 | The "Restarts?" column and the record's own issue note on `RestartPreventExitStatus` | n/a | OUTSIDE A01 (A17); NOT CHECKABLE FROM CODE (see R3-02) |
| R3-97 | L183 to L193, L197 | Token chain: cron deletion and refresh, headless login, Windows helpers | n/a | OUTSIDE A01 (A04, A16) |
| R3-98 | L194 | At boot (live) the token file is read and validated for account and freshness; missing or expired is exit 6 | as R1-04, R3-46, R3-92 | PARTLY. Validation happens at L2546 to L2552, not at the read, and only after the clock check's broker call, where a token that the broker rejects gives exit 3 (R3-46). A missing file gives exit 2 at 970aabf |
| R3-99 | L195 | Token monitor polls every 1800 s | main.py L3388 to L3400 | MATCH (wiring) |
| R3-100 | L199 to L240 | Scheduler and deploy hook | n/a | OUTSIDE A01 (A16, A17) |
| R3-101 | L248 | A daemon thread (4129) calls `check_and_fire(now_ist())` every `poll_interval_sec` (5 s) | main.py L4094 to L4100 (daemon "eod-scheduler", target `eod.start_polling`, interval from config) | MATCH (thread). What `start_polling` calls is OUTSIDE A01 (A12); the 5 s value is OUTSIDE A01 (A02) |
| R3-102 | L248 | Fires when the IST clock reaches `eod_squareoff_time`, compared at `market_windows.py:205`, on a non-holiday date | `core/market_windows.py` `is_eod_squareoff_due` L194 to L205 (holiday test L202 to L203; special-session time L204) | MATCH (comparison). "15:17" is OUTSIDE A01 (A02) |
| R3-103 | L248 | Once per IST date | n/a | OUTSIDE A01 (A12) |
| R3-104 | L248 | Time source: the VM clock rendered in IST (`time_authority.py:99`) | `core/time_authority.py` L58 to L59, L94 to L99 | MATCH |
| R3-105 | L250 to L278 | EOD fire sequence, EOD7, delivery exclusion | n/a | OUTSIDE A01 (A12, A03) |
| R3-106 | L276 | Restart recovery through `post_wire_init` | main.py L3863 to L3866 (after the bus subscriptions, before the reconcile) | MATCH (call). Internals are OUTSIDE A01 (A12) |
| R3-107 | L282 | Self-exit is armed only for a normal start | main.py L4129 to L4161 (not for `--interactive`, `--resume` or `TS_IGNORE_MARKET_WINDOW=1`) | MATCH |
| R3-108 | L282 | Stop time is the configured `service_window_end` | main.py L2211, L4142 | MATCH (wiring). The value is OUTSIDE A01 (A02) |
| R3-109 | L282 | Not due before that time (1270) | main.py L1270 to L1271 | MATCH. The comparison is pure time-of-day (section 8) |
| R3-110 | L282 | Refuses while a HARD_KILL flatten is in progress | main.py L1272 to L1277 (also stays up if the probe raises) | MATCH |
| R3-111 | L282 | Due only if zero positions require the service; a fallback if the read raises | main.py L1286 to L1326 | MATCH |
| R3-112 | L282 | Logs and sends "EOD Clean Shutdown" | main.py L1505 to L1525 (event set at L1525) | MATCH |
| R3-113 | L282 | The SIGINT/SIGTERM handler sets the same event (1573) | main.py L1570 to L1579 | MATCH. The unit's KillSignal is OUTSIDE A01 (A17) |
| R3-114 | L284 | Teardown: drain flatten, census, stop webhook, cancel pending ENTRY, stop monitor, probe, token monitor and feed, "System Stopping", SHUTDOWN row, PASSIVE WAL checkpoint, close, "Shutdown complete" | main.py `_shutdown` L1629 to L1831 (L1645, L1665, L1686, L1768, L1774 to L1790, L1797, L1807, L1816, L1828, L1831) | MATCH (relative order of the listed steps). The list is not exhaustive (section 8) |
| R3-115 | L284 | "Shutdown complete" is the function's final statement | main.py L1831 | MATCH |
| R3-116 | L286 | The gate is conditional on no position requiring the service | main.py L1305 | MATCH |
| R3-117 | L286 | "A carried position therefore prevents the clean shutdown, and the process stays up" | main.py `_BROKER_PROTECTED_PRODUCTS` L1161; `_position_requires_service` L1164 to L1179; `_classify_active_positions` L1204 to L1205; fallback L1322 to L1326 | DIFFERS. A DELIVERY position with entry product CNC (the overnight carry) is not counted and does not hold the service up. Intraday survivors, identity CONFLICT or UNRESOLVED, and delivery on a non-CNC product do. Only the product-blind fallback counts every position |
| R3-118 | L286 | "Shutdown complete" is the only positive evidence that the sequence finished | main.py L1643 to L1831 (each step except 1, 4, 26 and 29 has its own try/except; the final log line is unconditional) | PARTLY. The line shows that `_shutdown` reached its end, not that each step succeeded |
| R3-119 | L290 to L302 | Verification accounting: 480 steps by six agents | n/a | NOT CHECKABLE FROM CODE (record method) |
| R3-120 | L306 | The boot mode used in production is NOT ESTABLISHED; the CLI default is paper; the repository unit says live | main.py L184 to L187 | MATCH (CLI default). The unit is OUTSIDE A01 (A17); the mode in force is NOT CHECKABLE FROM CODE |
| R3-121 | L307 to L309, L311 to L315 | Deployed config, `.env` path, crontab installer, MIS unit, delivery close, EOD writers, pre-receive guard, live crontab | n/a | NOT CHECKABLE FROM CODE / OUTSIDE A01 (A02, A12, A16, A17) |
| R3-122 | L310 | The SQL behind three boot calls | main.py L2815, L2077 (via `compute_live_seed`), L3880, L3891 | MATCH (call sites). The SQL is OUTSIDE A01 (A09, A12, A03) |

## 6. Results by count

Each claim is counted by the first label of its Result cell (for example, "MATCH (wiring). ... OUTSIDE A01" counts as MATCH).

| Record | MATCH | PARTLY | DIFFERS | OUTSIDE A01 | NOT CHECKABLE FROM CODE | paper-only | Total |
|---|---|---|---|---|---|---|---|
| `01_SYSTEM_OVERVIEW.md` | 15 | 8 | 1 | 14 | 1 | 1 | 40 |
| `03_STARTUP_RUNTIME_AND_SCHEDULER.md` | 91 | 13 | 3 | 10 | 4 | 1 | 122 |
| Both | 106 | 21 | 4 | 24 | 5 | 2 | 162 |

DIFFERS: R1-08, R3-08, R3-92, R3-117. PARTLY: R1-04, R1-09, R1-10, R1-13, R1-23, R1-32, R1-33, R1-38, R3-14, R3-40, R3-43, R3-46, R3-57, R3-60, R3-73, R3-74, R3-79, R3-86, R3-91, R3-98, R3-118. NOT CHECKABLE FROM CODE: R1-39, R3-06, R3-09, R3-119, R3-121. Paper-only: R1-03, R3-37.

## 7. Runtime and deployment statements in the records (HISTORICAL, not established)

These statements describe machines, captures or practice, not code. They are HISTORICAL; none of them is evidence of what ran in production (Document 06, section 4.2). "R01" and "R03" name the two records.

| Record lines | Statement (paraphrased; addresses, paths and account identifiers not copied) | Label |
|---|---|---|
| R01 L3 to L4; R03 L3 to L6 | The evidence came from a PC worktree "byte-equivalent" to the testing VM as delivered 17-Sep-2026 19:31 IST, plus testing-VM captures of 17-Sep-2026 20:06 IST. The records did not read the production host, so what ran there is not established by them. Evidence date 18-Sep-2026 | HISTORICAL |
| R01 L19; R03 L25, L306 | The unit on the machine starts main.py with `--mode live` (installed capture identical) | HISTORICAL |
| R01 L23 to L27 | Three environments. The PC is the git origin of the deployed code. The testing VM ("the twin", address given in the record, not copied) runs e7bf477 plus force_qty. The production host (address given in the record, not copied) is described as the instance that traded real money; what it ran, its configuration, crontab, units and database are NOT ESTABLISHED | HISTORICAL |
| R01 L29, L155, L178 | The testing VM carries its own 228-byte `accounts.csv`; its contents were not read | HISTORICAL |
| R01 L88 to L112 | The day schedule is taken from the installed crontab (42 entries), for example the 05:00 token deletion, the 08:15 refresh and the 08:30/09:14/09:15 pre-flight. The 16:05 shadow evaluator ran on the testing VM only. The testing VM's `entry_start` is 09:30 against 10:00 in the repository | HISTORICAL |
| R01 L145 to L149 | What the system "did not do" in operation | HISTORICAL |
| R01 L153 to L156; R03 L304 to L315 | The running state of the production host, the mode each instance booted in, whether the scanners were posting, the deployed config, the `.env` path and the crontab owner could not be established | HISTORICAL (the records' own UNKNOWNs) |
| R01 L162 to L184 | Testing VM against e7bf477: identical files; force_qty files and config values; a cron-registry account argument (an account-ID literal, not copied); a retargeted token-copy script; 23 CRLF-only files; 14 extra and 10 missing files; one unexplained file | HISTORICAL |
| R03 L12 to L19 | On "this host" 8 systemd units are installed and the VM user's crontab holds 42 active jobs | HISTORICAL |
| R03 L25 to L51 | Installed unit directives (absolute VM working directory and EnvironmentFile paths, not copied; `KillSignal=SIGINT`; `TimeoutStopSec=30`; `Restart=on-failure`, 10 s; `RestartPreventExitStatus=3 4 5`) and drift between the repository and installed units | HISTORICAL |
| R03 L61 | Which `.env` path supplied each variable "on any given day" | HISTORICAL (UNKNOWN by the record) |
| R03 L157 | The receiver's comment gives the deployed webhook as all interfaces, port 5000 | HISTORICAL (comment) |
| R03 L166 to L179 | Restart behaviour per exit code under the unit, including "unbounded restart every 10 seconds" on exit 6 | HISTORICAL (depends on the installed unit) |
| R03 L187 to L197 | 05:00 daily token deletion; 08:15 headless refresh; Windows helpers; the target of an SSH host alias; a morning PowerShell script run by hand | HISTORICAL |
| R03 L205 to L224 | Registry, canonical and live crontab counts (47/46/42); five gemini jobs commented out on the testing VM ("DISABLED 09-Sep-2026 (Rama)"); a hand-added shadow evaluator; a daily CRITICAL drift report | HISTORICAL |
| R03 L232 to L240 | The armed post-receive hook; a real push on 17-Jul-2026 printed "AUTO-INSTALLED" (per the hook header) | HISTORICAL |
| R03 L248, L282 | "15:17", the 5 s poll and `service_window_end` values, read from the worktree's `system_config.yaml` | HISTORICAL (values in force NOT ESTABLISHED) |
| R03 L290 to L302 | Six parallel research agents traced 480 steps, and every quote matched | HISTORICAL (record method) |

## 8. In the A01 code at the baseline but not in the records

What a reader of the two records also needs to know. Each item is FACT for the lines cited unless it says INTERPRETATION; lines are in `main.py` unless a path is given.

1. Exit codes on failure paths that the records' table does not give: a missing live token file gives exit 2 (R3-92); a live `accounts.csv` failure gives exit 1, or exit 2 for a short row (R3-40); a configuration-load failure gives exit 5 (L2197 to L2201). A present but unloadable `instruments.csv` leaves the cache None (L2440 to L2449), the aggregate skips the size check (`utils/startup_checks.py` L1608), and the assert at L2506 gives exit 2, where the comment at L2434 to L2438 expects exit 3 (INTERPRETATION: this depends on `InstrumentCache.load` raising; A05). An import-time failure (L24 to L106) happens outside the entry guard (L4285 to L4293), so the interpreter's default exit status 1 applies (INTERPRETATION). The module docstring's exit list (L11 to L20) stops at 8; exit 9 (L2572) is missing from it.
2. `--status` and `--dry-run` need the instance lock (L2183), so they exit 1 while the service runs, and they are not read-only: both run `load_all`, open the store with `allow_migrate=True` (L2233 to L2237), run the kill-switch auto-clears (L2260, L2265), may write a `CRASH_DETECTED` event (L2277 to L2282) and exit 4 on HALT without `--resume` (L2283 to L2290). `--dry-run` also writes the early session row (L2308 to L2314) and runs the whole aggregate, with its NTP, scanner and broker calls.
3. No flag bypasses the holiday guard (L2098 to L2152); only argparse and `--version` run before it. It sends Telegram directly, once a day, guarded by a sentinel under `logs/` (L2133 to L2149, L264 to L285). Only `FileNotFoundError` is caught (L2151); a malformed entry (`utils/holiday_guard.py` L56 to L62) or a YAML parse failure escapes before logging is configured and gives exit 2.
4. The signal handlers are installed late, at L3958: after the MIS notifier's boot self-test and poller (L3355, L3357), the MIS auto-square-off poller (L3380), the optional workers (L3504 to L3832), `candle_store.start()` (L3922) and `live_feed.connect()` (L3947). Most of these also start before the startup reconcile (L3880). Until L3958, SIGINT raises `KeyboardInterrupt` and SIGTERM takes its default action; neither path runs `_shutdown`.
5. Threads and servers missing from the records' tables: the waitress webhook server, with 8 threads and a connection limit of 100 (L3988 to L4000); the health server (L4074); the gate-release pool (L865 to L867); the detached pre-flight on-demand hook (L4087 to L4091; A20); the event-bus async executors used by the slippage recorder (`core/events.py` L290 to L296; `orders/slippage_recorder.py` L113 to L114). `EventBus.shutdown()` is called nowhere outside the tests, and the gate-release pool is never shut down.
6. Hard-coded times in `main.py`: the 14:45 pre-alert (L943), the 09:15 margin re-sync (L994), the 1800 s token check (L3394), the 2 s webhook settle (L4003) and the 15 s flatten-drain grace on an external stop (L1075; its comment cites the unit's 30 s stop timeout).
7. EOD self-exit details: the thread first sleeps until `window_end` on the start date (L1393 to L1402); the due test compares the time of day only (L1270), so after midnight it reads as "before window_end" again (INTERPRETATION); a CNC delivery carry does not hold the service (L1161 to L1179), while CONFLICT and UNRESOLVED positions, intraday survivors and non-CNC delivery do, each with a CRITICAL or WARNING log and alert (L1410 to L1487, L1527 to L1556); a start with `--interactive`, `--resume` or `TS_IGNORE_MARKET_WINDOW=1` never self-exits (L4129 to L4161).
8. `_shutdown` steps that the records omit: the token invalidation after a broker authentication failure (L1677 to L1679; the flag is set at L666 to L667); the stops of the signal processor and the optional workers (L1689 to L1746); the stops of the entry gate, smart TGT, TGT retry and reconciler (L1747 to L1764); `candle_store.stop()` (L1791 to L1794). Every step except 1, 4, 26 and 29 catches and logs its own failure (L1643 to L1830; in step 4 only the rename is guarded, L158 to L165), and `main()` releases the lock in a `finally` (L2187 to L2190). Handled early returns close the store but skip `_shutdown`; exceptions that leave `_main_locked` skip `store.close()`.
9. Duplicate boot checks: the scenario detection and the config-hash check run in `main.py` (L2268, L2295) and again in the aggregate (`utils/startup_checks.py` L1561, L1578), after the early session-row write (L2308 to L2314). INTERPRETATION: the aggregate therefore sees today's session row and the current hashes, so its scenario cannot be COLD (except for a boot that crosses midnight IST), its "skip scanners on COLD" rule (L1589) does not apply at boot, and its hash check cannot report a change.
10. Instance lock: the lock file sits in the OS temporary directory and is never unlinked (`utils/instance_lock.py` L35 to L39, L50 to L51, L205 to L217); `main.py` calls `acquire_instance_lock()` with no argument (L2183), so the port is always 5001, although the docstring says it is configurable through `system_config.yaml` (L141 to L142).
11. Event bus (`core/events.py`): dispatch is synchronous by default; every handler runs, and failures are re-raised to the publisher as `EventDispatchError` (L300 to L345); async subscriptions run in one single-thread executor each (L290 to L296); the module defines 8 event types (L82 to L234), while its docstring says four.
12. Exceptions and the exit code: `TradingSystemError` is the root (`core/exceptions.py` L30), which gives exit 1 at the guard; `StartupCheckFailed` subclasses `ConfigError` (`utils/startup_checks.py` L956); `EffectCompositionError(RuntimeError)` (`core/effect_telemetry.py` L71) and `MigrationError(Exception)` (`core/migrations.py` L136) are outside that tree, so they give exit 2 if they reach the guard. The docstring's claim that no custom exception is defined elsewhere (`core/exceptions.py` L5 to L7) does not hold at the baseline.
13. Date and time sources in A01 code: the holiday guard uses the host-local `date.today()` (L2100); the start-window guard and `_main_locked` use `now_ist()` (L2161, L2255); `check_config_files_present` uses UTC plus 05:30 (`utils/startup_checks.py` L859 to L866); `check_holiday_calendar` uses the IST date passed in (L1548, L1384).
14. Clock-skew wiring: only `on_critical_skew` is wired (L364 to L378); it soft-kills when the average skew is at or above `halt_sec` with at least 3 samples (`core/time_authority.py` L227 to L244); no ALERT or WARN callback is wired anywhere outside the tests (grep; `tests/unit/test_time_authority.py` L173 and L186 wire them), so those tiers fire nothing in the system (L245 to L248); the startup clock check is the only caller of `assert_clock_at_startup` (`utils/startup_checks.py` L437).
15. `check_market_holiday_today` compares an ISO string with `MarketWindows.holidays`, a set of `date` objects (`utils/startup_checks.py` L898 to L900; `core/market_windows.py` L67). INTERPRETATION: a configured weekday holiday is never reported by this warning.
16. `scripts/ist_now.sh` and `scripts/check_tz.sh` are operator tools that `main.py` never calls (STUDY, section 10.10). Neither record names these scripts, `core/ids.py`, `core/constants.py` or `core/account_registry.py`.
17. A second synchronous reconcile: `order_reconciler.start()` (L3961) runs the CNC overnight check, the GTT reconcile and `reconcile_once()` (`orders/order_reconciler.py` L428 to L442) before its poll thread starts, after the startup reconcile's kill check (main.py L3894 to L3899), and no kill check follows it. The comment at main.py L3877 to L3878 calls the second and later reconciles the background poll.
