# A01 — RECONCILED TOPIC RECORD: System orchestration, startup, runtime and shutdown

**Status:** APPROVED — the RECONCILED TOPIC RECORD of topic A01 (Document 04, section 4, steps 9 and 10), the topic's authoritative document, approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30), after ChatGPT's review of every package file
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06, prepared with Rama's approval of 06-Nov-2026; before its first commit, after ChatGPT's package review of the same day, C32's recording-only entry A01-25 cross-referenced (sections 18, 20, 23 and 24), with Rama's approval. Approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30): status marked APPROVED; section 23 records the approval; section 24 gives the hashes of the approved files, whose status and revision lines alone changed.
**Purpose and scope:** The authoritative topic document of A01 (Document 07, section 5; Decision Register, D-25). It combines the STUDY and the AUDIT in distinct parts and keeps distinct the study findings (Part A), the audit conclusions (Part B), Rama's decisions (Part C) and the unresolved OPEN items (Part D). It applies the corrections that the AUDIT made to the STUDY, records the corrections that the topic made to the existing technical records, and carries forward every open item and cross-topic handoff. It records the legacy system as it is; it does not repair it, and it is not a V2 design.
**Sources:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline; Decision Register, D-21), through `A01_STUDY_2026-11-04.md` (content last changed at `36184f0`), `A01_AUDIT_2026-11-05.md` (content last changed at `2b27af4`) and the eight evidence files in this topic's `evidence/` folder (section 24); the Open Issues Register (entries A01-01 to A01-24, as committed at `781908e`, with the corrections of this package, and the recording-only entry A01-25 for C32, added with this package) and the Audit Findings Register (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`, first committed with this package).
**Related documents:** Documents 02, 04, 05, 06, 07, 08 and 10; the Master System Investigation Index (entry A01); the Decision Register, D-21 and D-23 to D-27; the Open Issues Register, the Audit Findings Register and the Topic Completion Register.

## 1. How to read this record

### 1.1 Parts and labels

- **Part A, study findings (reconciled):** what the code at the baseline does, from the STUDY, with the AUDIT's corrections applied (section 6) and each correction marked "[corrected: ...]". The STUDY is kept unchanged (Document 07, section 3); where a STUDY statement and this record differ, this record governs.
- **Part B, audit conclusions:** what the AUDIT found when it compared the code with the intended behaviour, from the AUDIT. The AUDIT records each item in full; this record summarises and cites it.
- **Part C, Rama's decisions:** his statements about the legacy system and his treatments for the new system, as recorded in the Open Issues Register and the Audit Findings Register, which quote his words. A treatment is input to the Phase 2 proposal only: it is not a V2 design decision, it changes no legacy finding, and no legacy behaviour becomes a V2 requirement automatically (Document 04, section 5.5; Document 08, section 12).
- **Part D, unresolved OPEN items:** every item that is not settled, with where it is tracked.
- Labels (Document 04, section 6): FACT, INTERPRETATION, HISTORICAL, KNOWN DEFECT, OPEN QUESTION and UNKNOWN / NOT ESTABLISHED. Decision statuses (Document 05, section 3): AGREED, PROPOSED, UNDER DISCUSSION and OPEN QUESTION. Anything that only Rama can decide is marked OPEN FOR RAMA.
- References: "STUDY 6.3" and "AUDIT 6.1, C13" are sections and records of those documents; "A01-nn" is an Open Issues Register entry; line references written "L123" are to the legacy `main.py` at the baseline unless a path is given, as in the STUDY and the AUDIT.

### 1.2 Baseline and the runtime-evidence limit

Every code statement is about commit `970aabf` (D-21). The last recorded deployment was `7d4970a` (02-Sep-2026); two A01 paths changed after it, by additions only (STUDY 1.8): `core/account_registry.py` (the helpers at L247 to L360) and `main.py` (42 lines net). Whether production ran any commit after `7d4970a` is UNKNOWN / NOT ESTABLISHED.

Both legacy VMs were terminated, and their databases, logs, journals and crontab do not survive (Document 06, section 4.2). The code shows what is implemented; whether a path ran, how often, with which values and with what timing is UNKNOWN / NOT ESTABLISHED, and a schedule, unit file, default or comment is not evidence that something ran (Document 08, section 10).

### 1.3 Security

Credential values, tokens, account identifiers, IP addresses, e-mail addresses and absolute machine paths are not written here; credential variables are named by type, as in the STUDY and the AUDIT (Document 08, section 11).

## 2. Scope and coverage

- **Index entry A01:** process entry, orchestration, lifecycle, runtime loop, startup checks, shutdown, time authority and top-level wiring. Fifteen paths: `main.py` (orchestration and wiring); `utils/startup_checks.py`, `utils/instance_lock.py`, `utils/holiday_guard.py`; `core/time_authority.py`, `core/market_windows.py`, `core/events.py`, `core/ids.py`, `core/exceptions.py`, `core/constants.py`, `core/account_registry.py`; the package files `core/__init__.py` and `utils/__init__.py`; and the operator scripts `scripts/check_tz.sh` and `scripts/ist_now.sh` (STUDY 1.2, 3).
- **Document 08 coverage (section 3):** item 1 (system overview and architecture), item 3 for startup and runtime, and item 20 for the startup and shutdown boundary.
- **Excluded:** the internals of every subsystem that `main.py` constructs or calls, which belong to their owner topics (index rule 1); A01 records the call sites, what crosses the boundary and the owner (section 5; AUDIT 8). Paper-only paths are out of scope and were marked, not traced (Document 08, section 2). Nothing was repaired and nothing was designed.
- **Study:** the code was read in five parts, re-checked against the code and corrected after two independent checks; nothing from the legacy repository was run (STUDY 1.5).
- **Audit:** 214 items were audited against the intended behaviour, with every intent source the admitted evidence holds, each item recorded with the fields of Document 04, section 5.4, matches included (AUDIT 1.5 to 1.8, 2).
- **What could not be covered (AUDIT 12, summarised):** every runtime fact (no production VM, log, journal, database or crontab survives); third-party behaviour (waitress, kiteconnect); owner internals, read at the boundary only; some long legacy documents beyond the passages cited and 31 of 34 dashboard captures (checked by name and index, and showing no A01 procedure); tests, read as documents and never run; and Rama's intent where the documents cannot settle it (Part D). Whether these gaps affect closure is set out in section 23.

---

## Part A — Study findings (reconciled)

## 3. The lifecycle in brief

From STUDY 2, with the AUDIT's corrections applied.

The legacy trading process is one Python program, `main.py`. The repository's service file starts it as `main.py --mode live` under systemd; whether that file was installed is UNKNOWN / NOT ESTABLISHED (B-40). On start, `main()` reads the command line and applies two guards before any log file exists: a weekend and holiday guard, which exits 0 on a non-trading day, and a start window, which exits 0 outside 08:00 to 18:15 IST. It then sets up logging and takes a single-instance lock, a file lock plus a local TCP port; a second copy exits 1.

Everything else happens in `_main_locked`, one function of about 2,100 lines. It loads and validates the configuration (exit 5 on failure), opens the database (which may migrate its schema only while the market is closed), builds the event bus and the kill switch, and classifies the start as COLD, WARM, CRASH or HALT from the stored session row and kill state. A HALT stops the start with exit 4 unless `--resume` is given. It then writes today's session row, builds the broker client from the stored token, and runs an aggregate of sixteen startup checks; any blocking result stops the start with exit 3. In live mode it then checks the token file (exit 6, reached only for a token that the broker has just accepted in the clock check) and the broker name (exit 9).

Next it constructs every subsystem and wires them together through constructor arguments, callbacks and two event-bus subscriptions. Some workers start during this construction: the MIS square-off pollers, the webhook sweeper and the optional S&R and V3 workers. After a first, synchronous broker reconciliation (exit 1 if a kill switch is then active), it installs the signal handlers and starts the remaining workers; starting the reconciler runs a second synchronous reconciliation, which no kill check follows. It then starts the webhook server, the health server and three helper threads: a 14:45 pre-alert, a 09:15 margin re-sync and the end-of-day self-exit. It writes a STARTUP event, rewrites the session row and sends a "System Active" alert.

The main thread then waits on one event and does nothing else. The event is set by SIGINT or SIGTERM, or by the self-exit thread once the configured service window has ended and no open position needs the service. The main thread then runs `_shutdown`: it waits up to 15 seconds for a hard-kill flatten, only while one is running [corrected: AUDIT Appendix A, row 4], stops the subsystems one by one, cancels pending entry orders, writes a SHUTDOWN event, checkpoints and closes the database, and the process exits 0. A failure during startup ends the process with exit 1 or 2 (or a handled code), without this sequence and without a SHUTDOWN event. No kill-switch activation stops the process.

The most important facts (STUDY 2):

- FACT: the only entry is `sys.exit(main())` under `if __name__ == "__main__"` (L4285 to L4293); an uncaught `TradingSystemError` gives exit 1, any other `Exception` exit 2.
- FACT: the holiday guard uses the host-local date (L2100); the start window uses `now_ist()`, a fixed UTC+05:30 clock (L2161; `core/time_authority.py` L58 to L59, L94 to L99). Both run before logging and before the lock (L2101 to L2176).
- FACT: the instance lock is an exclusive file lock plus a loopback TCP bind on port 5001 (L2183 to L2186; `utils/instance_lock.py` L129 to L202). It is released in the `finally` of `main()` when `_main_locked` returns or raises, before interpreter finalisation, not at the end of the process (L2187 to L2190) [corrected: AUDIT Appendix A, row 1; B-28].
- FACT: the scenario is detected (L2268) before the session row is rewritten (L2308); the aggregate of sixteen checks (L2451; `utils/startup_checks.py` L1508 to L1692) then detects it again, against the rewritten row. The second detection is still a real backstop in two edge cases, each ending with exit 3 [corrected: AUDIT Appendix A, row 16; C6].
- FACT: the first broker call of a boot is the clock check inside the aggregate (`utils/startup_checks.py` L436), before the token gate (L2546 to L2552); any broker exception there is reported as `clock_skew`, exit 3 (`utils/startup_checks.py` L459 to L468). INTERPRETATION: in live, the gate's exit 6 is therefore reached only for a token that the broker accepted (C8).
- FACT and INTERPRETATION: a missing, unreadable, non-JSON or non-UTF-8 live token file, or one whose JSON value is not an object, ends the start with exit 2, not the documented 6 (`scripts/zerodha_login.py` L53 to L57; L2362 to L2363); the path also covers `--interactive --mode live` [corrected: AUDIT Appendix A, row 9; C2, a KNOWN DEFECT].
- FACT and INTERPRETATION: `--interactive` reads a name `today` that `_main_locked` never binds (L2534, L2541, L4209), so it raises `NameError` and exits 2 at the baseline (C1, a KNOWN DEFECT).
- FACT: several workers start before the signal handlers are installed (L3355 to L3947, against L3958): the MIS threads and the webhook sweeper (L3355 to L3407) even before the last fail-fast guards (L3436 to L3465), and the optional workers (L3504 to L3832) before the startup reconcile and its kill check (L3880 to L3899).
- FACT: the runtime loop is the single call `_shutdown_event.wait()` (L4249); only the signal handler (L1573) and the self-exit thread (L1525) set the event before the wait returns.
- FACT: `_shutdown` (L1599 to L1831) has 29 steps, each inside its own try except steps 1, 4, 26 and 29; it stops only what is passed to it; `main.py` joins no thread itself.
- FACT: the code returns exit codes 0 to 9; the module docstring (L11 to L20) lists 0 to 8. The repository unit file declares `Restart=on-failure` and `RestartPreventExitStatus=3 4 5` (`deploy/systemd/trading-system.service` L33 to L35; A17's file, a boundary only) and no explicit start limit; whether a manager-level override limited restarts is UNKNOWN / NOT ESTABLISHED [refined: AUDIT, note 14; A01-04].
- FACT: no callback or kill-switch path sets the shutdown event or exits; the main thread does not watch its workers; worker liveness appears only on `/health` (L4060 to L4082).
- FACT: the time authority's only wired skew callback is the HALT tier, which soft-kills (L360 to L378); the ALERT and WARN tiers have no callback anywhere outside the tests.

## 4. Key study facts by area

Each subsection condenses the STUDY section named; the STUDY and its evidence files hold the full detail, line by line.

### 4.1 Entry point, CLI and exit codes (STUDY 4)

- FACT: at import, `main.py` runs 74 import statements, creates the gate-release pool and the window constants; importing `scripts.zerodha_login` runs that module's `load_dotenv()` (L106; A04). A failure during import happens outside the entry guard (INTERPRETATION: exit 1 with a traceback). Records logged before `setup_logging` (L2178) reach only Python's last-resort handler (INTERPRETATION).
- FACT: `_parse_args` (L179 to L212) defines seven options: `--mode` (default `paper`; `paper` or `live`), `--resume`, `--config PATH`, `--status`, `--dry-run`, `--version` and `--interactive`. `--version` wins over every other option; no option bypasses the holiday guard; `--status`, `--dry-run`, `--interactive`, `--resume` and `TS_IGNORE_MARKET_WINDOW=1` bypass the start window; `--interactive`, `--resume` and that variable leave the self-exit unarmed (L4129 to L4133).
- FACT: `--status` and `--dry-run` are not read-only: after the lock they load the configuration, open the store with migration allowed, run the kill-switch auto-clears and the scenario detection (and record `CRASH_DETECTED` on a CRASH); `--dry-run` also writes the session row, builds the broker stack and runs the whole aggregate (STUDY 4.3; C5).
- FACT (file content only; A17 owns the file): the declared unit starts `main.py --mode live` with `KillSignal=SIGINT`, `TimeoutStopSec=30`, `Restart=on-failure`, `RestartSec=10`, `RestartPreventExitStatus=3 4 5` and `PrivateTmp=true`; whether it was installed or ran is UNKNOWN / NOT ESTABLISHED (STUDY 4.5; B-40).
- FACT: the only non-test importer of `main.py` is `scripts/sr_level_export.py`. It fails at its own L141 (an `AttributeError` from `InstrumentCache(str(path))`) before it calls the `main.py` helper; its owner is not A01 [corrected: AUDIT Appendix A, row 2; C38b]. `deploy/resume.sh` does not run `main.py`: it stops the service, clears the kill with `scripts/clear_kill_switch.py` and starts the service (STUDY 4.6).

The exit codes (STUDY 4.7; the unit's treatment is INTERPRETATION of systemd semantics, for the declared file only):

| Code | Docstring meaning | Main sites (FACT) | Declared unit's treatment |
|---|---|---|---|
| 0 | clean shutdown, or holiday or weekend | `--help`, `--version`, holiday guard, outside the start window, `--status`, `--dry-run` ok, after `_shutdown` (L4278) | not restarted |
| 1 | `TradingSystemError` | lock refused (L2186); a kill active after the startup reconcile (L3899); the guard (L4290), including most live `accounts.csv` failures and `MigrationNotPermitted` | restarted after 10 s |
| 2 | unexpected exception | the guard (L4293): for example the live token-file errors, a short `accounts.csv` row in live, the interactive `NameError`, the instrument-cache `AssertionError`, a holiday-file parse failure before logging | restarted after 10 s |
| 3 | startup check failure | L2423, L2482, L2502, L2825, L2889, L3443, L3465 (L2778 paper only) | not restarted |
| 4 | HALT without `--resume` | L2290 | not restarted |
| 5 | invalid arguments, configuration or missing variable | invalid arguments (L2092); configuration load (L2201); the interactive sites are unreachable | not restarted |
| 6 | token missing or expired (non-interactive live) | L2370 and L2374 (L2370 cannot be reached from the token read, C2); the token gate (L2552), reached only for a token the broker accepted (C8) | restarted after 10 s |
| 7, 8 | live confirmation or account selection cancelled | interactive only; not reachable at the baseline | - |
| 9 | (not listed) | unsupported broker (L2572) | restarted after 10 s |

### 4.2 Orchestration and wiring (STUDY 5)

- FACT: the lifecycle phases are marked in the code: import; `main()` and its guards; Phase 0b (configuration, the stop time); Phase 0c (market-open test, store, bus, kill switch, time authority, auto-clears, scenario, config hash); `--status` and the early session row; Phase 0d (market windows, broker stack, live pre-load, account registry, secrets, instrument cache, the aggregate, `--dry-run`); account selection, the token gate and the broker pin; Phase 0e construction (L2616 to L3844) and Phase 0e subscriptions (L3846 to L3866); Phase 0f (the startup reconcile and its kill check, L3868 to L3918); Phase 0g (starts, signal handlers, servers, helper threads, `validate_all`); Phase 0h (STARTUP event, session row, "System Active"); the runtime wait and shutdown (STUDY 5.1).
- FACT: `_main_locked` constructs more than sixty objects; dependency injection is by constructor keyword arguments; the process environment is used as a channel between steps (`ZERODHA_API_KEY`, `ZERODHA_ACCESS_TOKEN`); which optional features were on in production is UNKNOWN / NOT ESTABLISHED (STUDY 5.2, 5.4).
- FACT: `main.py` subscribes two handlers (`KillSwitchActivated`, which only logs, and `CapitalDriftDetected`, A09's drift handler) and wires twelve principal callbacks; every kill-related callback calls `soft_kill` or `hard_kill`, and none sets the shutdown event or exits (STUDY 5.5).
- FACT: `_shutdown` stops only the objects passed to it; the EOD poller, the MIS pollers, the webhook and health servers, the gate-release pool and the bus executors are never stopped (STUDY 5.6).

### 4.3 Startup sequence, checks and readiness (STUDY 6)

- FACT: the main checks, in execution order: holiday and weekend guard (0; missing file: proceed; other file problems: 2); start window (0); instance lock (1); configuration load (5); migration permission (1); scenario detection (HALT: 4); config-hash comparison (a change: `CONFIG_DIFF` and a WARN alert later); the aggregate of sixteen steps (any blocking entry: 3); the instrument-cache assert (2); the token gate (6); the broker pin (9); capital rehydration consistency (3); the Q4(c) and A5 configuration audits (3); the kill check after the startup reconcile (1); the webhook self-check (CRITICAL sentinel only); and the effect-telemetry composition check (CRITICAL alert only) (STUDY 6.3; the checks catalogue).
- FACT: the aggregate's sixteen steps run in order, none retries, every step runs even after a blocking result, and the runner has no try of its own. NTP is blocking at 5 s and warning at 2 s, with no entry when the server is unreachable; the scanner step is skipped only on COLD, which in the code order happens only for a boot that crosses midnight IST; the webhook step never runs (STUDY 6.3).
- FACT: no in-process "ready" flag exists that another component reads; completion is shown by the STARTUP event, the second session-row write and an INFO line; a failed start writes no failure event (STUDY 6.5).
- FACT: startup is not free of side effects: every start repeats every step, rewrites the session row, may add `CRASH_DETECTED`, `CONFIG_DIFF` and `STARTUP` events, runs the kill-switch auto-clears, the schema migration, two startup reconciliations and broker calls, and sends "System Active" (STUDY 6.6).

### 4.4 Runtime loop and workers (STUDY 7)

- FACT: the runtime loop is one blocking wait with no timeout and no body; the main thread checks no time and watches no worker (STUDY 7.1).
- FACT: every `threading.Thread` created outside the tests is a daemon, except the kill switch's hard-kill flatten worker (`capital/kill_switch.py` L1193 to L1196); worker exceptions stay in their own threads; nothing restarts a worker; `main.py` joins no thread (STUDY 7.2).
- FACT: the event bus runs synchronous handlers in the publisher's thread and raises their failures to the publisher as `EventDispatchError`; async handlers run in one single-worker executor per subscription (STUDY 7.3). Before L3847, the kill-switch auto-clears at L2260 and L2265 publish nothing; only `resume` (L2291) and a rehydrate invariant failure (L2815, which also hard-kills and then exits 3) publish before the subscription, and the only loss is a duplicate CRITICAL log line [corrected: AUDIT Appendix A, row 3; C29 a].
- FACT: the instance lock is the only cross-process guard; within one start the startup reconciliation runs twice, at L3880 and inside `order_reconciler.start()` (L3961), and no kill check follows the second (STUDY 7.4; C41).
- FACT: the market-open margin re-sync waits for a literal 09:15 and the pre-alert for a literal 14:45; `main.py` has no market-close handler of its own (the force-close callback, the EOD and MIS pollers and the daily-loss callback are A04's, A12's and A13's); the self-exit thread polls every 60 s after `window_end` and sets the event when no active position needs the service; a DELIVERY position with entry product CNC does not hold the service up (STUDY 7.5). A process still up after midnight reads "not due" until the next day's `window_end` (INTERPRETATION; C24a).
- FACT: at runtime no kill path stops the process; worker failures are not supervised; `/health` reports the order monitor, reconciler and EOD poller as dead or alive. The order monitor's self-stop after three authentication failures is therefore visible to an external monitor through `/health`; the deaths with no surface are those of the other workers [corrected: AUDIT Appendix A, row 12; C25].

### 4.5 Shutdown, cleanup and exit paths (STUDY 8)

- FACT: the normal routes are the self-exit and SIGINT or SIGTERM after L3958; both reach `_shutdown` and exit 0. A handled startup return skips `_shutdown` (most close the store first; the returns at L2552 and L2572 do not); an exception that leaves `_main_locked` reaches the guard with exit 1 or 2 without `_shutdown` or a store close; a SIGINT before L3958 ends with a traceback and a SIGTERM before L3958 ends the process at once (INTERPRETATION) (STUDY 8.1, 8.2).
- FACT: `_shutdown` runs 29 steps: set the event, drain the flatten, stop intake, the signal processor, the optional workers, the entry gate, smart TGT, TGT retry and reconciler, cancel pending entry orders, stop the order monitor, probe and token monitor, disconnect the feed, stop the candle store, send "System Stopping", write SHUTDOWN, checkpoint and close the store, and log "Shutdown complete". The "reverse-order" docstring is only roughly true (STUDY 8.3; C20).
- FACT: the fixed maximum waits, recounted by the AUDIT: before the SHUTDOWN marker, 56 s without a flatten (64 s with the "System Stopping" send, which `alerts.telegram.send_deadline_seconds` bounds at 8 s in the file), 84 s with the file-value optional workers and 99 s with a flatten; the 15 s drain waits only while a flatten runs; step 6 has a second unbounded wait (the step executor). The declared unit sets `TimeoutStopSec=30`. The real durations are UNKNOWN / NOT ESTABLISHED [corrected: AUDIT Appendix A, row 4; the STUDY's 71 s; C18].
- FACT: each step except 1, 4, 26 and 29 has its own try; the event is set first, so from then on the rate limiter aborts any wait; there is no re-entrancy guard (STUDY 8.4).
- FACT: no A01 failure is recovered in-process; recovery is by a new process (STUDY 8.5).
- FACT: what a partial start can leave behind: the migrated schema, kill-switch auto-clears, `CRASH_DETECTED`, today's session row, `CONFIG_DIFF`, a configuration snapshot, sentinels and alerts, the effects of broker calls and of the two startup reconciles; threads started before the failure keep running until the process exits. After a guard return, those threads keep working database connections until interpreter exit, because `StateStore.close()` closes only the calling thread's connection [corrected: AUDIT Appendix A, row 5; the STUDY's "against a closed store"; C19]. No failed start writes a SHUTDOWN event, so the next start the same day is usually classified CRASH (INTERPRETATION) (STUDY 8.6).

### 4.6 Time authority, service window, market windows and holidays (STUDY 9)

- FACT: `now_ist()` reads the operating-system wall clock at a fixed +05:30 offset, independent of the host's timezone, with no monotonic clock and no skew correction. The default thresholds are warn 2 s, alert 5 s, halt 30 s and startup 30 s; only the HALT callback is wired (a soft kill); `record_broker_skew` has one caller outside the tests, the clock-skew probe (STUDY 9.1).
- FACT: the time authority's docstring calls `now_ist()` the only time source; outside the tests and the time authority itself, code lines read `datetime.now(` 30 times in 23 files and `date.today(` 9 times in 7 files [corrected: AUDIT Appendix A, row 6; the STUDY's 35 in 26 and 10 in 8 counted comment and docstring lines; B-34].
- FACT: the holiday guard (L2100), the default year of `current_holiday_set` and A02's holiday-file year use the host-local date; every other A01 date and time uses IST; if the host is on UTC the two dates differ only between 00:00 and 05:30 IST (INTERPRETATION). The VM's timezone is UNKNOWN / NOT ESTABLISHED (STUDY 9.2; B-41).
- FACT: the start window is [08:00, 18:15) IST, checked once; the stop time is the configured `trading_hours.service_window_end` (file value "17:35"), used only by the self-exit thread (STUDY 9.3).
- FACT: `MarketWindows` reads no clock; it is built once from six `trading_hours` times, the configured holidays and the special sessions (whose schema validates neither keys nor times); its entry functions ignore special sessions; other definitions of "market open" exist elsewhere (STUDY 9.4; C11).
- FACT: the holiday guard returns False on Saturday and Sunday without reading a file, loads the year's holiday file on a weekday, and is cached; `main()` catches only `FileNotFoundError`, so a missing file lets the start continue, and other file problems escape before logging (exit 2). At the baseline only `config/nse_holidays_2026.yaml` exists (15 entries). The holidays are read twice, by the guard and into `MarketWindows`; the startup holiday check cannot see configured holidays (STUDY 9.5; C10b, C10c, C10g).

### 4.7 A01-owned utilities and scripts (STUDY 10)

- `utils/startup_checks.py`: seventeen check functions, the scenario detection and the aggregate; no check retries; the library has side effects beyond logging, and several docstrings differ from the code (STUDY 10.1; S-38).
- `utils/instance_lock.py`: the lock of section 3; `check_port_available` has no caller outside the tests; `scripts/reconstruct_excursions.py` imports its private `_pid_is_alive` (STUDY 10.2).
- `utils/holiday_guard.py`: imported also by A16's cron registry and heartbeat, two reports and ten scripts (STUDY 10.3).
- `core/events.py`: one bus per process; `InstrumentsRefreshed` has no subscriber and its publisher no caller; `EventBus.shutdown()` is never called; the docstring's "no async" and "four event types" do not describe the code (STUDY 10.4).
- `core/ids.py`: the id generators (prefix plus `uuid4().hex`); the validators are unused; `truncate_tag_for_broker` keeps the first 16 characters without the filtering its docstring mentions (STUDY 10.5).
- `core/exceptions.py`: `TradingSystemError` with 25 subclasses under five sub-roots plus three direct children; thirteen custom exception classes are defined in nine other files. Three concrete classes are never constructed (`DedupViolation`, `SignalExpiredError`, `DuplicateSignalError`), the root and the four sub-roots `ConfigError`, `StateError`, `TimeError` and `SignalError` are never constructed directly, and `TransactionError` (`core/state_store.py` L142) is a fourth never-constructed concrete class; of the eight classes outside the tree only `MigrationError` and `MisSquareoffConfigError` can reach the guard in the live process, giving exit 2 [corrected: AUDIT Appendix A, row 7; the STUDY's "four classes"; M-20, M-24].
- `core/constants.py`: `PRODUCT_TO_INTENT` maps CNC and NRML to DELIVERY; `EMERGENCY_FLATTEN_PRODUCTS` is {MIS, CO}. The five membership tests read the latter, and it is also read for message text at `capital/kill_switch.py` L1407 and L1420 (seven reading lines in all); the comment's line numbers are declared a drifting snapshot, so their mismatch is not an issue [corrected: AUDIT Appendix A, row 8; M-27].
- `core/account_registry.py`: the validating `accounts.csv` loader (a duplicate id is not refused; a short row escapes as `AttributeError`) and the never-raise helpers added after the last recorded deployment; the file holds the names of credential variables, not their values (STUDY 10.8).
- `core/__init__.py`, `utils/__init__.py`: one comment line each. `scripts/check_tz.sh` and `scripts/ist_now.sh`: operator tools that test the shell's timezone data, not the clock; nothing declared runs them, and whether they were run is UNKNOWN / NOT ESTABLISHED (STUDY 10.9, 10.10).
- No import cycle exists among the A01 modules; some lazy imports cross the modules' stated layers (STUDY 10.11).

## 5. Cross-topic boundaries

FACT (STUDY 11): `main.py` is the composition root, and every subsystem it builds belongs to an owner topic: A02 configuration, A03 database, A04 broker, A05 market data, A06 signals, A07 screening, A08 S&R, A09 capital, A10 orders, A11 exits, A12 EOD and reconciliation, A13 kill switch and failure callbacks, A14 alerts, A15 reports and monitoring, A16 scheduler (no call site in `main.py`), A17 deployment (the unit file, as a boundary), A18 V3 and allocation, A19 tests and A20 pre-flight. The STUDY's section 11 table gives, for each owner, the A01 call sites, what crosses the boundary and what is left to the owner. What each owner must examine about an A01 finding is in AUDIT 8 and is carried forward in section 15.

## 6. Corrections that the AUDIT made to the STUDY

The AUDIT re-checked the STUDY and recorded where it differs (AUDIT, Appendix A). The STUDY is not changed; the corrections below are applied in this record. The STUDY's other statements stand.

| # | STUDY place | STUDY statement | What stands (AUDIT) | Applied in |
|---|---|---|---|---|
| 1 | startup-trace evidence, row M8 | the lock "held for the process lifetime" | released when `_main_locked` returns or raises, before interpreter finalisation (B-28); STUDY 6.2's wording was right | section 3 |
| 2 | 4.6; 12.2 C38 | `scripts/sr_level_export.py` receives no data | it fails earlier, at its own L141; not an A01 path (C38b) | 4.1 |
| 3 | 7.3; 12.2 C29 | the transitions at L2260, L2265 and L2291 reach no handler | the auto-clears publish nothing; `resume` and a rehydrate failure publish; the only loss is a duplicate CRITICAL log line (C29 a) | 4.4 |
| 4 | 8.4; 12.2 C18 | the fixed waits add up to 71 s | 56 s without a flatten (64 s with the send), 84 s with the file-value optional workers, 99 s with a flatten; the drain waits only during a flatten; a second unbounded wait in step 6 | 4.5 |
| 5 | 8.6; 12.2 C13, C19 | workers "can run against a closed store" | other threads keep working connections until interpreter exit (W-21, merged into C19) | 4.5 |
| 6 | 9.1 | 35 `datetime.now(` lines in 26 files, 10 `date.today(` lines in 8 | code lines only, time authority excluded: 30 in 23 and 9 in 7 (B-34) | 4.6 |
| 7 | 10.6; 12.2 C39 | four classes are never constructed | three concrete classes, plus `TransactionError`; the root and four sub-roots never constructed directly; two outside classes reach the guard (M-20, M-24) | 4.7 |
| 8 | 10.7 | the comment's line numbers do not match the readers | seven reading lines; the comment declares its numbers a snapshot, so no issue (M-27) | 4.7 |
| 9 | 12.1 (token file missing or unreadable) | `TypeError`, exit 2 | also non-JSON, non-UTF-8 (`UnicodeDecodeError`) and non-object files; exit 2 each time; covers `--interactive --mode live` | section 3 |
| 10 | 12.2 C3 | INTERPRETATION: `_invalidate_token` not reached | FACT: the flag can never be set in the wired code; KNOWN DEFECT | Part B, section 10 |
| 11 | 12.2 C20 | a gate release could reach a stopped processor | the processor aborts once stopped, and only restored rows can reach the path: a documentation mismatch only | Part B, section 11 (C20) |
| 12 | 12.2 C25 | the order monitor's death goes unnoticed | it is one of the three workers whose liveness gates `/health`; the unseen deaths are the others' | 4.4 |
| 13 | 12.2 C23 | the pre-alert logs "sent" without a notifier | unreachable in `main.py`'s flow: the notifier is always passed | Part B, section 11 (C23) |
| 14 | 12.2 C28 | the status code is not recorded | it is logged, not kept in the sentinel; the `detail` field never existed | Part B, section 11 (C28) |
| 15 | 12.2 C36 | the 15 s drain is a hard-coded value | hard-coded with a stated reason (half of `TimeoutStopSec=30`): a MATCH (C36e) | Part B, section 11 |
| 16 | 12.2 C6 | the second detection cannot return COLD | confirmed and narrowed: a real backstop in two edge cases, each ending with exit 3 | section 3 |
| 17 | 14, R14 | is cancelling pending entries on every shutdown intended? | answered by evidence: CT-078 expects a mid-trade stop to cancel entry orders and keep positions | section 14 |

## 7. Corrections to the existing technical records (Document 08, section 9)

The STUDY checked the two A01 records, `01_SYSTEM_OVERVIEW.md` and `03_STARTUP_RUNTIME_AND_SCHEDULER.md` (kept unchanged in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`), claim by claim against the code at `970aabf` (STUDY, Appendix A; evidence `A01_LEGACY_RECORDS_CHECK_2026-11-04.md`). HISTORICAL: both records rest on a testing copy at commit `e7bf477`, which is not in the clone; their claims are checked against the baseline, and what production ran is UNKNOWN / NOT ESTABLISHED.

| Record | MATCH | PARTLY | DIFFERS | Outside A01 | Not checkable | Paper-only | Total |
|---|---|---|---|---|---|---|---|
| `01_SYSTEM_OVERVIEW.md` | 15 | 8 | 1 | 14 | 1 | 1 | 40 |
| `03_STARTUP_RUNTIME_AND_SCHEDULER.md` | 91 | 13 | 3 | 10 | 4 | 1 | 122 |
| Both | 106 | 21 | 4 | 24 | 5 | 2 | 162 |

The four statements the topic finds wrong (DIFFERS), with the correction:

- **R1-08** (`01_SYSTEM_OVERVIEW.md` L33): 757 modules and 289,044 lines. At the baseline the tree has 734 `.py` files and 283,180 lines (a different tree; the reachable set is not re-derived here, and the scheduled scripts are A16's).
- **R3-08** (`03_STARTUP_RUNTIME_AND_SCHEDULER.md` L59): the `.env` file is found relative to the working directory. INTERPRETATION, about the library and not shown by the repository's code: `find_dotenv()` without `usecwd` starts at the calling module's directory (`scripts/`) and walks upward; the version installed on the VM is UNKNOWN; OPEN QUESTION.
- **R3-92** (L174): a missing live token file gives exit 6. At the baseline it gives exit 2 (C2, a KNOWN DEFECT; section 3). An expired or wrong-account token (L2552) and a missing API-key variable do give 6.
- **R3-117** (L286): a carried position keeps the process up. A DELIVERY position with entry product CNC does not; intraday survivors, conflicting or unresolved identities and delivery on a non-CNC product do, and only the product-blind fallback counts every position.

The 21 PARTLY results (for example R1-23, the 09:15 re-sync's time, which is hard-coded and does not follow `trading_hours.market_open`; R3-79, at most 14 of the aggregate's steps execute at boot; R3-118, "Shutdown complete" shows only that `_shutdown` reached its end) are listed in full in STUDY, Appendix A, with their code evidence.

## 8. What the study could not establish

UNKNOWN / NOT ESTABLISHED (STUDY 12.3, condensed): which commit production ran, whether the unit was installed and how systemd behaved, and the environment file's contents; the configuration values in force; the VM's timezone, clock and NTP reachability, and whether the time scripts were run; the Python and library versions; which scenarios and exit codes occurred and whether restart loops followed; whether the diagnostic options were used after 05-May-2026; boot and shutdown durations; the kill-switch history; whether the self-exit ran, whether a process ran past midnight and whether any SIGKILL followed; webhook self-check failures and unnoticed worker deaths; token invalidations and holiday messages; lost log records and late tasks; whether `scripts/sr_level_export.py` ran and whether several accounts were enabled; and what the records' extra `main.py` lines contain.

---

## Part B — Audit conclusions

## 9. Method and totals

- The AUDIT compared what the code does with what was intended, for every area and flow of A01, not only configuration settings (Document 04, section 5; Document 08, section 6). Every intent source the admitted evidence holds was collected in the evidence file `A01_AUDIT_INTENT_SOURCES_2026-11-05.md`: intent sources by area (IS-numbers), 76 conflicts between sources (IC-01 to IC-76), 26 statements that only the code contradicts (CD-01 to CD-26) and 16 statements attributed to Rama or the operator (RS-01 to RS-16); conflicts that the evidence file does not list are in AUDIT 3.4.
- Method rules applied alike to every item (AUDIT 1.6): the four-condition KNOWN DEFECT rule; where the exit list has a general entry and an entry that names the case, the named entry states the intent; a source supersedes another only when it names or replaces it; the semantics of Python, the standard library, the kernel, SQLite and systemd are INTERPRETATION; cross-topic findings are handed to their owners and counted once.
- **Totals (AUDIT 1.8):** 214 items audited (56 concern items and 158 other items): **MATCH 101; ISSUE 107; UNKNOWN / NOT ESTABLISHED 4** (B-40, B-41, M-41, W-24). C21b (REJECTED as not material) and C38b (HANDED OFF; not an A01 path) are counted in none of the three. **KNOWN DEFECT: 8 items, within the ISSUE count.** UNKNOWN components of three counted items: the shutdown durations (C18), the boot durations (C32) and the concurrent use of one broker client (C38a, itself a MATCH).
- The STUDY's 41 concerns were each re-checked: C7, C10, C21, C24, C36, C38 and C39 were split; C10f was merged into C35; C21b was rejected as not material and C26 as an issue (it is a MATCH); the rest were confirmed or narrowed (AUDIT 4).
- Every ISSUE and UNKNOWN item is entered, with its fields, in the Audit Findings Register (106 established by evidence, AUDIT 10(a); C32; and the five UNKNOWN entries). The 24 questions that needed Rama's intent or decision (AUDIT 10(b)) are the Open Issues Register's entries A01-01 to A01-24.

## 10. The eight KNOWN DEFECTs

Each meets the four conditions of AUDIT 1.6: the code has a mechanism for the case; by the language's semantics it fails for certain whenever the case occurs; the case can arise under the documented set-up; and the outcome contradicts every intent source found. Whether any of them occurred in production is UNKNOWN / NOT ESTABLISHED.

| ID | KNOWN DEFECT (AUDIT 10(a)) | Treatment (Part C) |
|---|---|---|
| C1 (part (a)) | `main.py --interactive` stops with `NameError` and exit 2 at L2534, after the startup checks; the April 2026 operations documents prescribe it for the first paper days and for restarts (the binding broke on 05-May-2026) | A01-01 |
| C2 (parts (i) and (ii)) | a missing, unreadable, non-JSON, non-UTF-8 or non-object live token file ends the start with exit 2, not 6; a live `accounts.csv` problem ends it with exit 1, where the code written for it gives 3 and the exit list's configuration entry 5 | group A; A01-02, A01-03 |
| C3 | the FIX-062 token-invalidation guard can never fire in the wired code | group A |
| C9 | a present but unloadable `instruments.csv` ends the start through an assert with exit 2, not the blocking exit 3 | group A |
| C10g (latent) | the startup holiday check can never report a configured holiday with the object `main.py` passes; the case arises in a boot that crosses midnight IST through a documented bypass, and on a non-IST host | group D |
| M-33 | `AccountRegistry.load` raises `AttributeError` for a short or whitespace-only row (exit 2 in live, with the store left open) | group A; A01-03 |
| S-11 | a configuration change seen by a boot that ends between L2308 and L2656, or by `--dry-run`, is never recorded as `CONFIG_DIFF` or alerted | group C (with `--dry-run` kept read-only, A01-05) |
| S-39 (the `UnicodeDecodeError` sub-case) | a strategy YAML that is not valid UTF-8 ends the start with exit 2 instead of the blocking exit 3; the runner has no exception isolation; its docstring counts nine of its sixteen steps | group A |

## 11. The ISSUEs, by subject

The 106 findings established by evidence (AUDIT 10(a)) were put to Rama in ten groups; C1 was decided with A01-01; C32 is in neither list. Each finding's line, fields and treatment are in the Audit Findings Register; its full record is in AUDIT 6.1. KNOWN DEFECTs are marked (KD).

- **C1 (KD), decided with A01-01:** the interactive start is broken at the baseline (section 10).
- **Group A — start-up failures that end with the wrong exit code or message (10):** C2 (KD), C3 (KD), B-03, C9 (KD), M-33 (KD), S-39 (KD), C4, C12, M-24, S-52. Conclusion: several known start-up failures end with the generic crash code 2, or with 1, instead of the exit code that the code itself or the exit list names; the token-invalidation guard is dead; the exit-code list, the comments and the declared restart treatment disagree (exit 6 restarted, exit 9 undocumented, the April start limit removed); the required-credential list is built by naming convention while the code reads configured names; the disk-space check runs after logging starts.
- **Group B — start-up order, and cleaning up after a failed start (10):** C13, C41, B-26, C14, C15, C16, C37, W-13, S-25, S-51. Conclusion: workers start before the last guards and the reconciliation; no kill check follows the second reconciliation; the signal handlers are installed only after 7 to 12 threads have started; the late steps are unguarded and no failed start runs a clean-up; the boot-order flag is set even when the reconciliation failed; an optional feature can be left half-wired; the health server's start is unchecked; two early exits leave the database open; the database-permission check runs after the open; the sources disagree on which step comes first (B-26).
- **Group C — start type, session record and configuration-change detection (11):** C5, C6, C7a, C33, C7b, C7c, C7d, S-11 (KD), S-07, S-17, B-15. Conclusion: `--status` and `--dry-run` change state; the repeated detection and hash checks run on changed state; a crash after an earlier clean stop counts as a restart; the session row always says "default" and "INTRADAY"; a same-day kill without a session row gives exit 3, not 4; removed configuration files are not reported; a change seen by a failed start or a dry run is lost; all start types share one procedure; the diagnostics' reports are incomplete.
- **Group D — time, calendar, holidays and fixed clock times (15):** C10a, C10c, C11, C35, C23, C10b, C10e, C10g (KD), B-33, B-34, B-35, B-36, B-37, C24a, B-39. Conclusion: the holiday decision uses the VM's local date while the rest uses IST; the holiday file is read twice with opposite failure rules; market-open, holiday, time, token and path rules are repeated with different rules; special sessions are not traded on weekends or evenings and a malformed entry crashes the start; fixed 14:45 and 09:15 times; a weekend passes the holiday check when next year's file is missing; the "single time source" rule is not met; time-module descriptions differ from the code; a process still running after midnight cannot exit on its own before the next day's window end; an operator script hard-codes a VM path.
- **Group E — shutdown, supervision and logging at exit (11):** C17, C25, W-04, C18, C19, C20, C21c, W-10, C28, C34, B-28. Conclusion: the stop signal is set before the close-out finishes; only a few workers are watched and no kill or worker failure stops the process (against some sources, IC-48); the longest configured shutdown waits (84 s, or 99 s with a flatten) exceed the declared 30 s stop timeout; several workers have no stop method and nothing is joined; the "reverse order" and "threads joined" comments are untrue; two shutdown steps are unguarded; no heartbeat; no detection of a webhook-server failure after start-up; logs are not flushed at exit, and an operator message the procedures name does not exist; the lock is released slightly before the process ends.
- **Group F — start-up checks and their descriptions (11):** C8, S-44, S-56, C30, S-42, S-38, S-40, S-45, S-46, B-07, S-22. Conclusion: a rejected token is reported as a clock problem; a scanner outage gives only a log line; the TEMP check only warns; the clock-skew tiers are not wired and the NTP check is hard-coded, with a 5 s block against the locked decision's 30 s; the checks module changes state although its description says it does not; test lists, comments and ordering claims do not match the code; the scanner check uses GET, not the decided HEAD; the broker check runs after the broker was used.
- **Group G — single instance and ports (2):** C31, B-32. Conclusion: the lock port is fixed and a port taken by another program blocks every start; the webhook port's own check was removed on a wrong premise.
- **Group H — configuration, credentials and accounts (11):** M-35, M-32, M-34, M-36, M-37, M-38, M-39, M-40, C36a, C36b, C40. Conclusion: a disabled primary account is still traded; three registry rules are not implemented and duplicate ids are not refused; a live start can be refused over a paper-only value; a cached account read survives a failure and ignores `--config`; helpers return the text "None"; programs choose accounts differently; a configuration switch is overridden in code and a timeout setting is never read; credentials are loaded at import, and `main.py` is far larger than its size rule.
- **Group I — internal events and error types (20):** C29, C36d, M-04, M-05, M-06, M-07, M-08, M-11, M-12, M-13, M-15, M-16, M-19, M-20, M-21, M-23, M-28, M-29, M-30, M-31. Conclusion: event-delivery failures are not reported to the sender; dead fields, types and validators; descriptions that do not match the code; one event type carries four meanings; thirteen error types live outside the central module and several are never raised; severity drives logging only, not alert routing; unknown product types fall back differently by site; the close-out product list is copied; NRML is mapped to DELIVERY while a comment calls it unrecognised. The handed-off parts of M-08 (A04, A10), M-11 (A09) and M-30 (A13) are their owners'.
- **Group J — documentation and operator text (4):** B-01, B-05, B-16, B-19. Conclusion: "locked decisions" references point to sections that do not exist; help text omits effects; the interactive prompts differ from their specification (latent); the token watcher no longer mirrors `main.py`'s check.
- **C32 (an ISSUE in neither list):** the start-up network checks run one after another; the intended boot-time limit is not established, and the actual durations are UNKNOWN / NOT ESTABLISHED. It is a design concern, recorded as INTERPRETATION; no latency target is inferred.

## 12. UNKNOWN / NOT ESTABLISHED items

- **B-40:** whether the declared service unit and the token watcher were installed on the production VM, and how the supervisor behaved (HISTORICAL for the reports).
- **B-41:** the VM's actual timezone, NTP state and Python version (HISTORICAL for the documents; also A01-20).
- **M-41:** `core/account_registry.py` L247 to L360 were added after the last recorded deployment, so whether they ever ran is not established (HISTORICAL).
- **W-24:** the behaviour of third-party threads (the webhook server's workers, the ticker thread); the evidence lies outside the admitted repository.
- **Components:** the actual shutdown durations (C18), the actual boot durations (C32) and the concurrent use of one broker client by several threads (C38a, a MATCH).

## 13. Intent-source conflicts

The conflicts between intent sources are recorded, not resolved, unless a later source names or replaces the earlier one (AUDIT 1.6, 3.4; evidence file, IC-01 to IC-76). Where the code follows one side of a conflict, the item is an ISSUE, and the history question went to Rama (Part C). Conflicts that recur in Part D: IC-40 (exit 5 or 6 for a missing credential variable), IC-48 (whether a kill stops the process), IC-14 (NTP block at 5 s or 30 s), IC-27 to IC-29 (start types and the detection order), IC-34 (the TEMP check) and IC-49 to IC-51 (fixed times, the pre-alert's delivery listing and deposits at the 09:15 re-sync).

## 14. The STUDY's questions R1 to R24

Each question was checked against all admitted evidence before it went to Rama (AUDIT 9). ANSWERED BY EVIDENCE: 4 (R3, R14, R18, R19). Retained as OPEN QUESTION: 20, of which 13 were narrowed by the evidence. NO LONGER MATERIAL: none.

| R | Disposition (AUDIT 9) | Where it went |
|---|---|---|
| R1 | OPEN QUESTION, narrowed (use after May 2026) | A01-01 |
| R2 | OPEN QUESTION, narrowed (token part answered: exit 6; `accounts.csv`: 3 or 5) | A01-03 |
| R3 | ANSWERED BY EVIDENCE (stay down until a manual token refresh) | none |
| R4 | OPEN QUESTION, narrowed (exit 6 answered) | A01-02, A01-04 |
| R5 | parts 1 and 2 ANSWERED BY EVIDENCE (read-only; stop on holidays); part 3 OPEN | A01-05 |
| R6 | OPEN QUESTION | A01-06 |
| R7 | OPEN QUESTION, narrowed | A01-07 |
| R8 | partly ANSWERED BY EVIDENCE (a broker failure blocks); the label and order OPEN | A01-08 |
| R9 | OPEN QUESTION, narrowed to R9(a) | A01-09 |
| R10 | OPEN QUESTION, narrowed (only the actual VM state) | A01-20 |
| R11 | OPEN QUESTION | A01-18 |
| R12 | OPEN QUESTION | A01-10 |
| R13 | OPEN QUESTION, narrowed | A01-14 |
| R14 | ANSWERED BY EVIDENCE (CT-078: cancel entry orders, keep positions) | none |
| R15 | split: grace and CRITICAL ANSWERED BY EVIDENCE; the event-first rule OPEN | A01-11 |
| R16 | OPEN QUESTION (needed by A09 for C22's handed-off part) | A01-12 |
| R17 | delivery listing ANSWERED BY EVIDENCE; the remaining part OPEN | A01-13 |
| R18 | ANSWERED BY EVIDENCE (an operator override is ended by the operator) | none |
| R19 | ANSWERED BY EVIDENCE (`deploy/resume.sh` on the VM, never `main.py --resume` beside the service) | none |
| R20 | OPEN QUESTION | A01-17 |
| R21 | (a) answered by the sources; (b) OPEN QUESTION | A01-15 |
| R22 | part 2 OPEN QUESTION, narrowed | A01-16 |
| R23 | OPEN QUESTION | A01-23 |
| R24 | OPEN QUESTION | A01-19 |

Three entries have no STUDY R number: A01-21 (B-26, the first step at start), A01-22 (S-44, a scanner outage at boot) and A01-24 (M-35, a disabled primary account).

## 15. Cross-topic handoffs

A01 records its side of each boundary; the owner topic examines its own side when it is audited, and a finding is counted once (AUDIT 8; Methodology Application, section 7). The AUDIT's section 8 table states, row by row, what each owner must examine. Index by owner topic (finding and item IDs as in AUDIT 8; several items name more than one owner):

| Owner | A01 items handed off |
|---|---|
| A02 | C7d, C10a, C10b, C12, C35, S-11, S-24, W-17, M-19, M-20, M-24 |
| A03 | C5, C6, C19, C20, C33, B-14, S-03, S-51, S-25, M-15, M-19, M-20, M-24, M-29 |
| A04 | C1, C2, C3, C4, C8, C11, C12, C14, C15, C17, C23 (e) and (g), C24a, C25, W-13, C29, C30, C32, S-44, C35, C36b, C36d, C38a, C40, B-16, B-19, B-03, B-10, B-38, B-40, M-07, M-08, M-12, M-16, M-19, M-20, M-29, M-30, M-39, R19 |
| A05 | C9, C14, C15, C29, C37, B-36, B-11, W-24, M-43 |
| A06 | C13, C14, C15, C18, C20, C28, C32, S-44, C37, B-36, B-28, B-32, B-07, W-24, M-13, M-19, M-20, M-37, M-43, IS-9.14 |
| A07 | C11, C14, C15, C20, B-28, B-08 |
| A08 | C13, C37, C38a, B-11; C38b, probably (to confirm) |
| A09 | C22, C27, C29, C36d, B-22, M-11, M-28 |
| A10 | C36a, B-36, M-07, M-08, M-28, M-31, M-44 |
| A11 | C11, C14, C15, C36a, C37, B-36, M-28, M-31, M-44 |
| A12 | C11, C13, C14, C15, C16, C19, C23, C23 (e) and (g), C35, C41, B-36, W-15, M-11, M-12, M-16, M-19, M-20, M-24, M-28, M-39 |
| A13 | C3, C4, C5, C7b, S-05, C17, C22, C23 (e) and (g), C27, C29, C30, C41, B-05, B-19, B-28, B-03, B-40, M-12, M-28, M-30, IS-9.14 |
| A14 | C5, C10e, C12, C13, C19, C23, C23 (e) and (g), C28, C30, C36d, B-08, M-19, M-20, M-21 |
| A15 | C10a, C11, C14, C15, C25, W-13, C33, C34, B-33, M-19, M-20, M-21, M-29, M-37, M-39, IS-9.14 |
| A16 | C35, B-33, B-37 |
| A17 | C4, C10c, C18, C24a, C31, B-41, W-24, B-40, M-24, B-38, R19 |
| A18 | C13, C37, B-36, M-17 |
| A20 | C11, C12, C32, S-44, W-14 |

Handed off and not counted as A01 ISSUEs (AUDIT 1.8): the internals behind C22 and C27 (A01's own part of each is a MATCH), C23 (e) and (g) (A13), C29 (c), M-11's drift-handler part (A09), M-28's site postures (their owners), M-30's flatten behaviour (A13) and C38b. Ownership points still to confirm are in section 22.

---

## Part C — Rama's decisions

## 16. How the decisions were made

- The 24 entries of AUDIT 10(b) were raised with Rama in six batches of four on 05-Nov-2026; each batch's record was read back to him and confirmed (batches 1 to 5 on 05-Nov-2026, batch 6 on 06-Nov-2026). ChatGPT reviewed each record.
- In the treatment round of 06-Nov-2026, Claude's treatment-round file put to Rama the eight entries still OPEN for treatment and the 106 findings of AUDIT 10(a), in ten groups, each with a recommendation; ChatGPT reviewed the file independently and recommended a choice for each entry and group, with the qualification behind each. Rama adopted those choices, with the full qualifications, as his decisions ("Adopt section 8"; "Include sections 3-4"). ChatGPT then reviewed the recorded decisions and found none recorded wrongly.
- The discussion itself is not kept (Document 07, section 3; D-17). The Open Issues Register and the Audit Findings Register quote the words that decide each item, and they govern; this Part summarises them.
- What is recorded in Part C is of two kinds, kept apart: Rama's statements about how the legacy system was meant to work or was run (an intent source, Document 04, section 5.1, with its date, not a FACT about the code), and Rama's treatments for the new system (Phase 2 input; not V2 design decisions).

## 17. Rama's statements about the legacy system

- **A01-01** (C1; ANSWERED BY RAMA, 05-Nov-2026): "HEADLESS": the system was operated in headless mode, and interactive mode was not the operating method. No date or recovery event is inferred from it.
- **A01-02** (C2, the missing-credential exit; ANSWERED BY RAMA, 05-Nov-2026): "OPTION B — EXIT 5 (invalid configuration)", confirmed as his recollection of the intended behaviour. It agrees with the docstring and M41C; FIX-163 chose exit 6; the conflict (IC-40) stays recorded.
- **A01-04** (C4; ANSWERED BY RAMA, 05-Nov-2026): Option A, "NO — repeated failures should not restart indefinitely; retain a start limit", confirmed as his recollection. It is not claimed that the legacy configuration had a three-attempt policy.
- **A01-03** (C2 part (ii)): his statement on the purpose of `accounts.csv`, to choose which Zerodha client code was used when the system was started by hand, before the move to headless operation with one configured client code. The historical exit code (3 or 5) stays OPEN.
- **A01-05** (C5): his recollection, recorded as an observation and not as an answer: he saw that the system was running from its live logs, and did not make or test a dry run.
- Every other history question is OPEN: Rama does not remember, or gave no historical answer, and directed that none be inferred from evidence leans or recommendations (section 19).

## 18. Treatments for the new system (Phase 2 input)

### 18.1 The 24 discussion entries

Summaries only; the Open Issues Register quotes each decision in full and governs.

| Entry | AUDIT IDs | Treatment status | Agreed treatment, in brief |
|---|---|---|---|
| A01-01 | C1 | AGREED (06-Nov-2026) | one start path, headless; manual and recovery starts use the same path and checks, and an operator can invoke it by hand; no separate interactive mode |
| A01-02 | C2 (IC-40) | AGREED (05-Nov-2026) | three start attempts in total (the first, then two retries 10 s apart; no fourth), then stop and send severity alerts by Telegram and e-mail that explain the failure; never a secret in an alert |
| A01-03 | C2 part (ii) | AGREED (05-Nov-2026) | no `accounts.csv`; one configured Zerodha client code; credentials from protected environment configuration, never in source control, reports, logs, evidence or alerts |
| A01-04 | C4 | AGREED (05-Nov-2026) | the same three-attempt rule; no endless restart loop |
| A01-05 | C5 | AGREED (05-Nov-2026) | `--status` genuinely read-only and safe beside the running service; `--dry-run` changes no order, state, record, kill state or crash record, is isolated from live execution, or refuses clearly |
| A01-06 | C6 | AGREED (05-Nov-2026) | one explicit start-up classification; the checks for each defined; each check run once unless a second run has a documented reason; scanner-check behaviour explicit for each classification |
| A01-07 | C7a | AGREED (05-Nov-2026) | the clean-stop marker belongs to a process run, not a date; the next start inspects the latest run's outcome |
| A01-08 | C8 | AGREED (05-Nov-2026) | check token and configuration locally before the first broker call; report an authentication failure as such, not as clock skew; keep clock errors separate; never expose secrets |
| A01-09 | C10c, C11 | OPEN QUESTION (left for Phase 2) | none; the exact calendar failure behaviour is decided in Phase 2 |
| A01-10 | C13 | AGREED (06-Nov-2026) | staged start-up: validation, broker reconciliation and kill-state evaluation before any worker that can trade or act; "ready" only when the required checks and critical workers are healthy; critical and optional workers classified; a failed start cleaned up without a misleading "active" notice |
| A01-11 | C17 | AGREED (06-Nov-2026) | an ordinary stop must not cancel risk-reducing close-out actions; the emergency close-out path distinct, bounded, observable and alerting; retry counts, rate-limit handling and the final position state only after A13 |
| A01-12 | C22 | AGREED (06-Nov-2026) | tell a real deposit or withdrawal from an unexplained capital difference; record a real change; never trade on an unverified capital figure; the capital and kill parts stay with A09 and A13 |
| A01-13 | C23 | AGREED (06-Nov-2026) | task times from the actual session timetable, not fixed times; the warning covers every order state that needs action, with filled and remaining quantities apart; cancel a pending entry order at the cutoff set in `config.yaml`, DELIVERY orders excluded |
| A01-14 | C25, W-04 | AGREED in part (06-Nov-2026) | a kill prevents unsafe trading, and "stop trading" is not the same as ending the process; a killed process may stay up for position protection, reconciliation, monitoring and alerts. The exact soft-kill and hard-kill behaviour, and IC-48, stay OPEN |
| A01-15 | C30 | OPEN QUESTION (left for Phase 2) | none; an unreachable time source must be told apart from a measured clock offset when it is decided |
| A01-16 | C31 | AGREED (05-Nov-2026) | a reliable single-instance control; a second process started by hand must not run as a competing live process |
| A01-17 | C33 | AGREED (05-Nov-2026) | no generic "default" label; the session record shows the mode configured that day |
| A01-18 | C35 | AGREED (05-Nov-2026) | never trade a Muhurat session, on any day, with no override; a full-length normal session on a weekend or holiday (such as a Budget day) is not excluded by this rule |
| A01-19 | C41 | AGREED (06-Nov-2026) | every start-up reconciliation that can change the kill state, or reveal an unsafe condition, is followed by a kill-state and readiness evaluation; no "active" notice or new entries until all are evaluated; A12 and A13 establish the mechanisms first |
| A01-20 | B-41, C10a | OPEN QUESTION (left for Phase 2) | none; a time basis independent of the VM's timezone, decided together with A01-15 |
| A01-21 | B-26 | AGREED (05-Nov-2026) | a clear start-up sequence based on dependencies; the old documents' conflict is not settled by guessing |
| A01-22 | S-44 | AGREED (05-Nov-2026) | a required signal-source outage is a classified dependency failure; Phase 2 discussion point: wait one hour from the configured trading start, then stop for the day |
| A01-23 | S-56 | AGREED (06-Nov-2026) | no "# TEMP" mechanism; a configuration or system issue triggers Telegram and e-mail alerts; alerts alone do not make an unsafe setting safe |
| A01-24 | M-35 | AGREED (06-Nov-2026) | one configured client; no `accounts.csv` or account selection; the client validated before any order call; if it is disabled, invalid or unauthorised, fail safely and never switch account |

Status: 20 AGREED, 1 AGREED in part (A01-14), 3 OPEN QUESTION (A01-09, A01-15, A01-20). None is CLOSED. A 25th entry, A01-25, records C32, with no question and its treatment OPEN (section 20).

### 18.2 The ten groups of established findings

Rama's choices (06-Nov-2026), with the qualification he adopted; the Audit Findings Register quotes each in full and governs.

| Group | Choice | The treatment, in brief |
|---|---|---|
| A, start-up failure exits | B | one written start-up failure contract: every anticipated failure has its own check, message, outcome, alert and test; the generic crash outcome stays for genuinely unexpected failures; retryable failures are told apart from permanent ones; the A01-02 and A01-04 retry rule; credential names checked without exposing values |
| B, start-up order and clean-up | A | every start-up step guarded; stop-signal handling before any worker starts; one idempotent clean-up path; resources closed; alerts; readiness and order flags set only on success; critical and optional workers defined; clean-up never conflicts with the emergency close-out path |
| C, start type, session record, configuration changes | B | the kill state read and enforced whatever the session record says; explicit procedures per start type; added, changed and removed configuration detected and reported; except that `--status` and `--dry-run` stay strictly read-only (A01-05): a dry run may display differences but persists nothing, sends no side-effecting alert and creates no broker connection |
| D, time, calendar and fixed times | B | a single time and calendar authority as a design direction; midnight behaviour defined and calendar data validated; except the exact calendar failure policy, the NTP thresholds and reachability behaviour and the VM-independent IST implementation, which stay OPEN under A01-09, A01-15 and A01-20; the agreed Muhurat and A01-13 decisions stand |
| E, shutdown and supervision | B | explicit stop methods and joins, supervised critical workers, heartbeat and liveness, visible server failures and flushed logs; emergency close-out independent of the ordinary shutdown; except that the 30 s stop timeout is not assumed to be a proven safe budget: Phase 2 reconciles the stop budget, bounded waits, escalation, remaining positions and termination |
| F, start-up checks | B | a written list of checks with order, severity, outcome, tests and documents; except that only pure validation checks are read-only, and any initialisation, repair, state change or protective action is a separately named start-up action; the NTP thresholds stay OPEN with A01-15 |
| G, single instance and ports | A | every required port in configuration, validated, and checked at start with a clear failure report; the bind itself handles a port taken between check and bind; the lock port does not protect other ports |
| H, configuration, credentials, accounts | B | the agreed one-client treatment kept (A01-03, A01-24); no setting silently ignored or overridden; credentials loaded at a controlled start, not at import; except that the treatment covers A01's own start-up and configuration behaviour, and other components go to their owning topics |
| I, events and error types | B | real producers and consumers; delivery failures reported; no silent fallback for unknown values; genuinely shared lists in one place; severity-based routing; except that the central event and error architecture and the cross-topic parts (M-08, M-11, M-30) are decided by their owning topics, and "no dead types" is a review rule, not a reason to delete types early |
| J, documentation and operator text | A | comments, help text, procedures and specifications describe the approved behaviour and are checked for consistency; legacy text is not carried forward merely because it exists; not a decision to reproduce any legacy interface |

C32: "Keep as recorded; no new treatment line." Its treatment is OPEN, recorded as A01-25 (section 20).

In the Audit Findings Register, the 112 entries stand at: AGREED 96; AGREED in part and OPEN in part 10 (C10a, C10b, C10c, C11, C25, C30, C35, B-33, S-42, W-04); OPEN QUESTION 1 (C32); UNKNOWN / NOT ESTABLISHED, with no treatment, 5.

---

## Part D — Unresolved OPEN items

Every item below stays visible here and in the registers until it is resolved or Rama decides it (Document 05, section 11.3), and is carried forward to the topics named and to Phase 2 (Document 04, section 12).

## 19. History questions OPEN (21)

OPEN QUESTION. Rama does not remember, or gave no historical answer, and directed that no answer be inferred. The legacy facts stay as the AUDIT records them.

| Entry | The question that stays open |
|---|---|
| A01-03 | at a live start, was a missing or invalid `accounts.csv` meant to give exit 3 or exit 5? |
| A01-05 | were `--status` and `--dry-run` meant to be usable while the service is running? |
| A01-06 | was the scanner check meant to run on the first start of the day, and were the repeated detection and hash checks meant as re-checks? |
| A01-07 | was a crash after an earlier same-day clean stop meant to count as a crash? |
| A01-08 | was a rejected token meant to be reported as a token problem with exit 6, and checked before the first broker call? |
| A01-09 | which holiday reader was meant to win, and was a missing or broken holiday file meant to stop the boot? |
| A01-10 | were the early MIS and optional workers, and leaving them running after a failed start, deliberate? |
| A01-11 | was the event-first rule meant to apply to the flatten's own broker calls during the grace? |
| A01-12 | was a deposit after a pre-market start meant to be able to trip the drift kill ladder at 09:15? |
| A01-13 | were the helper threads meant to follow special sessions, and was the pre-alert meant to list part-filled trades? |
| A01-14 | was a kill meant to stop the process, or to leave it running until the self-exit (IC-48)? |
| A01-15 | were the NTP server and thresholds meant to be configurable, "unreachable" a warning, and the refusal at 5 s or 30 s? |
| A01-16 | was the lock meant to stop a hand-run copy beside the service despite `PrivateTmp`? |
| A01-17 | were the session-row values "default" and "INTRADAY" intended? |
| A01-18 | how were weekend or evening special sessions meant to be traded? |
| A01-19 | was the kill check meant to cover the second synchronous reconcile? |
| A01-20 | was the VM actually set to IST and kept in time by NTP? |
| A01-21 | was the first step at start meant to be the logger, the holiday guard or the lock? |
| A01-22 | was a scanner outage at boot meant to be a warning or CRITICAL, with an alarm? |
| A01-23 | was the TEMP-marker check meant to block above about Rs 25,000 of capital? |
| A01-24 | was a disabled primary account meant to be refused, and was at least one account meant to be enabled? |

## 20. Treatments OPEN

- **Wholly OPEN, left by Rama for Phase 2 (05-Nov-2026; kept OPEN on 06-Nov-2026):** A01-09 (the exact calendar failure behaviour; also covering C10b, B-33 and the malformed special-session entry of C35, under group D's exception), A01-15 (the NTP source, thresholds and reachability behaviour; also covering S-42, under group F's), A01-20 (the VM-independent IST time basis, to be decided with A01-15).
- **OPEN in part:** A01-14, the exact soft-kill and hard-kill behaviour and the resolution of IC-48, after A12 and A13. Ten findings are AGREED in part and OPEN in part, their open parts tracked by those four entries: C10a, C10b, C10c, C11, C35 and B-33 (A01-09, A01-20), C30 and S-42 (A01-15), C25 and W-04 (A01-14).
- **C32:** no treatment line, by Rama's decision ("Keep as recorded; no new treatment line"); its treatment is OPEN, and no boot-time limit or latency target is inferred. It is recorded as A01-25, a recording-only entry with the fields of Document 05, section 11.2, approved by Rama on 06-Nov-2026; the entry asks no question and reopens no decision.

## 21. UNKNOWN / NOT ESTABLISHED items carried forward

B-40, B-41, M-41 and W-24, and the runtime components of C18, C32 and C38a (section 12), with the STUDY's list of what cannot be established (section 8). They stay UNKNOWN / NOT ESTABLISHED unless surviving runtime evidence is found (Document 06, section 4.2).

## 22. Handoffs and ownership points carried forward

- The cross-topic handoffs of section 15 are carried to each owner topic, which examines its side when it is opened (D-23; Methodology Application, section 7). When an owner topic records a fact that changes an A01 finding, the finding is updated in the Audit Findings Register (Document 05, section 11.1, update timing 5).
- OPEN QUESTION, ownership points to confirm (AUDIT 8; none changes the approved index, and a change to the index would be OPEN FOR RAMA under Document 05):
  - `deploy/token_watcher.sh` is A04's file, while the STUDY assigns its restart contract to A13; A01 cites it as a boundary only (C4, B-19, C24a, R19).
  - `scripts/sr_level_export.py` (C38b) is not an A01 path; its owner is probably A08, to be confirmed.
  - `scripts/reconstruct_excursions.py` (C31) reuses a private helper of `utils/instance_lock.py`; its owner topic is to be confirmed.
- OPEN QUESTION, library behaviour for later topics: how python-dotenv's `.env` search behaved on the VM (record claim R3-08; INTERPRETATION: A04 owns the module that calls `load_dotenv`, and A17 the pinned version).

## 23. Closure position

ChatGPT reviewed every file of the package on 06-Nov-2026 (PASS, after the C32 entry A01-25 was added), and Rama approved the package the same day (D-30). Before that review A01 was IN PROGRESS; with it, UNDER REVIEW. The remaining topic statuses are RECONCILED, APPROVED BY RAMA, PUSH VERIFIED and CLOSED (Document 10, section 4). This record does not close the topic; closure follows the verified commit (Document 04, sections 4 and 11; Document 07, section 6).

Document 04, section 11 (before closure):

| Condition | Position |
|---|---|
| required investigation complete | the STUDY and the AUDIT are complete for the fifteen paths and Document 08 items 1, 3 and 20; what cannot be established is UNKNOWN / NOT ESTABLISHED by the runtime-evidence limit (sections 2, 8 and 12), not by an omitted step |
| the audit complete for every area and flow | 214 items audited, matches included (section 9) |
| every issue raised with Rama, with its agreed treatment or OPEN status | the 24 entries and the 106 established findings raised and decided; C32 decided "keep as recorded" and recorded as A01-25 (Part C) |
| study and audit reconciled | this record (sections 6 and 7) |
| unknowns and open questions recorded | Part D |
| ChatGPT's review of every package file | done, 06-Nov-2026 |
| Rama's approval of the topic document and package | approved, 06-Nov-2026 (D-30) |
| committed, and the commit verified by ChatGPT | pending |
| topic status updated | pending (Topic Completion Register) |

Document 05, section 11.2 (closing with unresolved issues), as it applies to A01:

- Every issue has been raised and discussed with Rama, and he has explicitly left each unresolved part OPEN: the 21 history questions, the treatments of A01-09, A01-15 and A01-20, A01-14's open part, and C32's treatment.
- Each such issue must be recorded as OPEN in the Open Issues Register with its question, impact, evidence, owner and next action, and shown here: the 25 entries meet this. C32 is recorded as A01-25, a recording-only entry approved by Rama on 06-Nov-2026 (it asks no question, reopens no decision and infers no latency target).
- The topic's entry in the Topic Completion Register lists its open issues: yes.
- The evidence and the required coverage are otherwise complete: yes, within the runtime-evidence limit; no material evidence gap, unreviewed contradiction or issue that makes the findings unreliable is known.

## 24. Evidence index

The topic folder is `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/`. The hashes are those of the files as approved: their status and revision lines changed at approval, and nothing else (the line numbers that the Audit Findings Register cites are unchanged). The evidence files substantiate the STUDY and the AUDIT; they are not competing narratives (Document 07, section 5).

| File | Content last changed | SHA-256 (as approved) | What it holds |
|---|---|---|---|
| `A01_STUDY_2026-11-04.md` | `36184f0` | 88a7a4b6ec6e0ea331e0d48f5b85e3e659fee98255208474e1927f3b28b82599 | the STUDY |
| `A01_AUDIT_2026-11-05.md` | `2b27af4` | d71307d4a39fbcbd39bbf664448d21e7ad559cc353a569bdd3a4f61b40f40ea3 | the AUDIT |
| `evidence/A01_SOURCE_FILE_INVENTORY_2026-11-04.md` | `97ec336` | dd4c6f6302478cd0ea6bf86acbe30b62fdc7e5dc706edbff73681ed9f83d08e5 | the fifteen paths: sizes, Git objects, hashes, history; the changes after the last recorded deployment |
| `evidence/A01_MODULE_IMPORTERS_2026-11-04.md` | `97ec336` | 435937f5ed91b47de06afaa1410de869d6e4740e6288aa16d602dab0faf74685 | the importers of the A01 modules; the files that name the two scripts |
| `evidence/A01_MAIN_PY_STRUCTURE_AND_IMPORTS_2026-11-04.md` | `2e381fe` | 5ccd4b1fbecafb55d5b780226d28c53e257fba83ae2736ac445076598e6637a8 | `main.py`'s definitions, phase markers and imports |
| `evidence/A01_STARTUP_TRACE_2026-11-04.md` | `2c18c62` | 92676177d165552d9d7c1ead401de3638a07eeae222b87e473529fd34b0d87db | the step-by-step startup trace and the objects constructed (row M8 corrected in section 6) |
| `evidence/A01_WORKERS_AND_SHUTDOWN_2026-11-04.md` | `36184f0` | f84c1116dda5ee1d716be8041a3b845924e2591197e6d54c6de3815824c2adf1 | threads, pools, servers, subscriptions, callbacks; `_shutdown` step by step |
| `evidence/A01_STARTUP_CHECKS_CATALOGUE_2026-11-04.md` | `2c18c62` | 791dfa4a76e24261b03453a79ac3a221f4b5e66197182f99dafd659d7eba27ef | every check function and the aggregate's sixteen steps; docstring differences; side effects |
| `evidence/A01_LEGACY_RECORDS_CHECK_2026-11-04.md` | `2c18c62` | 9f1c81da1aa733139d565fa8823d5c365fb6eca1677488d29273c779d2247de7 | the two existing records' claims against the code (section 7) |
| `evidence/A01_AUDIT_INTENT_SOURCES_2026-11-05.md` | `8ce3215` | 28c5efa4c6b4b034846ff4e769088f76c48c1008b1b92ced70d11fc95d52a152 | the intent sources, conflicts (IC), code-only contradictions (CD) and statements attributed to Rama or the operator (RS) |

Registers: the Open Issues Register (`OPEN_ISSUES_REGISTER_2026-11-05.md`; entries A01-01 to A01-25) and the Audit Findings Register (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`; 112 A01 entries), in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/`.
