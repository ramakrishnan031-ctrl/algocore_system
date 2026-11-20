# A06 evidence: the processor's intake: queue, workers, expiry and normalisation

**Status:** APPROVED — evidence for the A06 STUDY, approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37)
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P04, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude. Approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37): status marked APPROVED; content unchanged.
**Purpose and scope:** `signals/signal_processor.py` from its construction to the point where a queued signal is handed to A07 logic (Rama's decision A of 17-Nov-2026): the construction in `main.py` L3574 to L3622 (every argument; the `signal_processor` SP15 settings by key); the processor's own state; `start()` and `stop()` (worker threads, the get loop, shutdown and drain, queued signals at stop); `main.py` L3870 to L3974 (boot-order invariant) and L1690 to L1693 (stop); every step from `queue.get` to the A07 handoff (intermediate representations, field mapping, the `scan_webhook_map` lookup, strategy controls only as far as they gate intake); expiry (`signal_expiry_sec`, timestamps, time zones, age, stale and future timestamps, where expiry is checked); symbol and alias normalisation at intake (the `config/symbol_aliases.yaml` consumer; the instrument cache at the A05 boundary only); backpressure, ordering, retries, worker failure, the `release_in_flight` call, the QUEUE_FULL reject (853a3a1); concurrency between workers on shared state up to the handoff. Direction questions 14 (processor side), 15, 16, 17, 18, 19 and 21 (processor side). The receiver (P01, P02, P03), event creation and persistence and the map of later call-outs (P05), the entry throttle (P06) and configuration keys (P08) are cross-referenced, not repeated (STUDY part P04).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)
Every printed line passed through the identifier and path filter of the common rules.

In part (line ranges):
- `signals/signal_processor.py` (2,703 lines): structure of the whole file taken with Python `ast.parse` of the source
  text (nothing executed); read line by line L1 to L1326, L1455 to L1646, L1959 to L2010 and L2663 to L2703; L2010 to
  L2075 and L2375 to L2410 scanned for the resume paths' pre-flight checks; the whole file searched (section 1.3).
- `signals/webhook_receiver.py`: L255 to L295, L393 to L400, L535 to L540, L567 to L580, L640 to L655, L660 to L708,
  L914 to L936, L1044 to L1110; searched (section 1.3). The receiver's study is P01's, P02's and P03's.
- `main.py`: L1596 to L1606, L1676 to L1700, L3155 to L3172, L3515 to L3530 (scanned), L3540 to L3630, L3862 to
  L3980; searched (section 1.3). A01 owns the file.
- `core/config_loader.py`: L192 to L215, L564 to L616, L2343 to L2385 (A02's schemas, at the boundary).
- `config/system_config.yaml`: L118 to L136, L340 to L380, and the line found by search at L529 (A02's file).
- `config/scan_webhook_map.yaml`: L1 to L84 except every line holding a URL (no URL value read).
- `strategies/loader.py`: L102 to L175 (A02's file, interface). `strategies/control.py` (117 lines; A07's file): L35 to
  L80 (the cause codes, `Verdict` and the start of `strategy_will_trade`), and its search hits for `cause`.
- `config/strategies/*.yaml` (16 files): the `name:` line of each only.
- `utils/startup_checks.py`: L1266 to L1290 and the search hits for `scan_webhook_map` (A01's file, interface).
- `scripts/preflight/checks/config_integrity.py`: L145 to L195 (A20's file, interface).
- `scripts/eod_cleanup.py`: L100 to L128 (interface).
- `deploy/systemd/trading-system.service`: L10 and L14 to L35 (A17's file, interface; no environment line read).
- `tests/unit/test_signal_processor.py`: L458 to L500 and L572 to L600, and its test names found by search
  (HISTORICAL only; never run). `tests/crash_test/ct_day2_isolated.py`: the search hit at L187 only.

In whole:
- `config/symbol_aliases.yaml` (10 lines; A02's file, at the boundary).
- `requirements.txt` (15 lines).

Commits read (`git show`, `git log`, `git blame`; hashes, dates and subjects only, except the message of `853a3a1`,
read as HISTORICAL; a session link in that message is not reproduced): `bcf03b5`, `f67a0c7`, `2e8448c`, `8536b53`,
`586af55`, `3975e75`, `435b3a2`, `31075d0`, `d604c95`, `397105d`, `a4ef762`, `e55cb59`, `1bf65ff`, `853a3a1` (with its
diff to the processor), `056905b`, and the six processor commits after `7d4970a` (`8d27fdb`, `d646347`, `23d2be7`,
`853a3a1`, `3fc1d2e`, `056905b`).

### 1.2 Project records and working inputs read (algocore_system, branch `main`, read-only)
- A05 RECONCILED TOPIC RECORD (2026-11-17) sections 4.6, 4.7 and 4.12 (IN-08, IR-10, IR-13, IR-30, XC-04) and the
  handoff table row for A06.
- A01 RECONCILED TOPIC RECORD (2026-11-06) section 4.5 (shutdown waits, C18).
- Master System Investigation Index (2026-11-04), entries A01, A07, A09, A11, A13, A15 and A18 (paths and scope, for
  the owners named).
- The checked parts P01 and P02 (statements cited by ID, not repeated), Claude's first A06 fieldwork checkpoint
  (17-Nov-2026) and this part's brief, as working inputs. The A06 investigation direction file was not available on
  disk to the first helper; the checking helper read it (section 4) and re-checked the question map (section 13).

### 1.3 Commands and search patterns (all read-only)
- `git -C <legacy clone> show 970aabf:<path>`, `git grep -n -E` at `970aabf` with the four mandatory exclusions (or
  the helper `the search wrapper`), `git blame -s -l -L`, `git log`, `git ls-tree`. Python `ast.parse` of the processor's source
  text only. No legacy code, test or script was run, imported or built; no endpoint was contacted.
- Repository-wide patterns: `pipeline_timeout` (tests included); `signal_queue`; `scan_webhook_map_path|
  _validate_scan_webhook_map|load_all_strategies\(`; `scan_webhook_map`; `'QUEUED'|"QUEUED"|status = 'PROCESSING'|
  'PROCESSING'|"PROCESSING"`; `expires_at`; `python3\.[0-9]+` (in `deploy/`, `scripts/`, `ops/`); `ExecStart|python
  -O|PYTHONOPTIMIZE` (in `deploy/`, `scripts/`).
- In `signals/signal_processor.py`: `_queue|queue\.|requeue|retry_count|in_flight_release|_in_flight_count|QUEUE_FULL|
  expir|_signal_expiry|task_done|join\(|alias|instrument_cache|\.upper\(|\.lower\(|strip\(`; `submit(`;
  `scanner_type`; `shutdown_event|_shutdown`; assignments to `_strategies`, `_scan_webhook_map` and `_running`.
- In `signals/webhook_receiver.py`: `NSE:|-EQ|\.NS\b|BSE:|exchange`; `_alias_map\s*=|_load_symbol_aliases\(`;
  `notifier|send_warning`; the in-flight names.
- In `main.py`: `_startup_reconcile_done`; the processor's names and setters; `os\.chdir|config_dir\s*=`;
  `symbol_aliases`; `zone_warmer`.
- In the processor's unit tests: `def test_.*(drain|stop|expir|stale|queue_full|requeue|dispatcher|worker)`.

### 1.4 External pages read (current external context, all read 17-Nov-2026)
- Python documentation, `queue` (page version 3.15.2): https://docs.python.org/3/library/queue.html
- Python documentation, `concurrent.futures` (3.15.2): https://docs.python.org/3/library/concurrent.futures.html
- CPython published source, 3.12 branch, `Lib/concurrent/futures/thread.py`:
  https://raw.githubusercontent.com/python/cpython/3.12/Lib/concurrent/futures/thread.py
- Python documentation, `threading` (3.15.2): https://docs.python.org/3/library/threading.html
- Python documentation, `datetime` (3.15.2): https://docs.python.org/3/library/datetime.html
- Python Language Reference, simple statements, `assert` (3.15.2): https://docs.python.org/3/reference/simple_stmts.html
- Python documentation, built-in types, mapping `d[key]` (3.15.2): https://docs.python.org/3/library/stdtypes.html

### 1.4a Read in the check (added by the checking helper; same rules)
- `signals/signal_processor.py`: re-read L1 to L482, L482 to L712, L711 to L760 (by search), L860 to L1060, L1185 to
  L1310, L1380 to L1454, L1455 to L1540, L1590 to L1646, L1686 to L1740, L1974 to L2050, L2205 to L2222, L2372 to
  L2408, L2516 to L2530, L2663 to L2703; searched for `_stop_event`, `_shutdown`, `_signal_expiry_sec`, `submit(`,
  `.upper(`, `.lower(`, `strip(`, `instrument_cache`, `_in_flight_count`; `git blame` of L304 to L347, L377 to L480,
  L860 to L1280, L1384 to L1405, L1486 to L1532, L1221 to L1231, L909 to L921; `git log -S` for the FIX-070 shutdown
  text (commit `31c6a62`, 16-May-2026).
- `signals/webhook_receiver.py`: L222 to L230, L255 to L295, L390 to L400, L533 to L582, L636 to L720, L736 to L800,
  L905 to L1012, L1040 to L1112; searched for `_alias_map`, `_load_symbol_aliases(`, `notifier|send_warning|telegram`.
- `main.py`: L1596 to L1632, L1676 to L1700, L2095 to L2102, L3154 to L3166, L3398 to L3412, L3543 to L3625, L3862 to
  L4002, L4072 to L4080; function boundaries from L2000 to L4300 by `awk` on the source text.
- `core/config_loader.py` L190 to L200, L562 to L616, L2343 to L2385 (URL-validator lines skipped), L2420 to L2470;
  `core/time_authority.py` (search hits L58, L59, L94, L99, L102, L104); `strategies/loader.py` L100 to L160;
  `strategies/control.py` L30 to L80; `config/system_config.yaml` L120 to L130, L340 to L356;
  `config/scan_webhook_map.yaml` (URL lines skipped); `config/symbol_aliases.yaml`; `requirements.txt`;
  `requirements-dev.txt` (pins `pytest` and `pytest-cov` only; no interpreter version); `scripts/eod_cleanup.py` L100 to
  L128; `scripts/healthcheck_server.py` L133 to L160, L245 to L262 (A15's file, interface); `scripts/preflight/checks/
  signals.py` L60 to L84 and `engine.py` L30 by search (A20's files, interface); `ops/control_tower/aggregator.py` L156
  to L159, `scripts/preflight/checks/config_sanity.py` L37 to L40, `scripts/preflight/checks/config_integrity.py` L145
  to L195, `utils/startup_checks.py` L1266 to L1290 (callers of the strategy loader); `deploy/systemd/
  trading-system.service` (no environment line; paths filtered); `docs/audit/integrity_audit_2026.md` L3746 to L3750
  (HISTORICAL); the cited unit-test and crash-test lines (text only, never run).
- Repository-wide searches (four mandatory exclusions): `pipeline_timeout` (documents included), `expires_at`,
  `scan_webhook_map`, `scan_webhook_map_path|_validate_scan_webhook_map|load_all_strategies\(`, the `QUEUED` and
  `PROCESSING` literals, `signal_queue\b`, `\._queue\b|queue_depth|...`, `metrics_provider|"/metrics"|queue_capacity`,
  `python3\.[0-9]+` (in `deploy/`, `scripts/`, `ops/`).
- Project records: Decision Register D-21; A01 RECONCILED TOPIC RECORD section 4.5 and the A06 handoff row; A05
  RECONCILED TOPIC RECORD sections 4.6, 4.7, 4.12 and its A06 handoff row; the Master System Investigation Index (owners
  of `market_windows.py`, `sr_detector/`, `strategy_governor.py`, `shadow_tracker.py`, `kill_switch.py`, `strategies/`,
  `healthcheck_server.py`, `preflight/checks/`); P01 and P02 statements cited by P04; the A06 investigation direction
  (17-Nov-2026), section 4.
- External pages re-opened 17-Nov-2026 (all as in section 1.4, page version 3.15.2 where shown): `queue`,
  `concurrent.futures`, `threading`, `datetime`, Language Reference section 7.3, built-in types (`d[key]`), and the
  CPython 3.12 `Lib/concurrent/futures/thread.py`. Every quotation used in the part was found on the page.

### 1.5 Labels and limits
Statements follow the common rules' labels. No runtime fact is given as FACT: every statement about what ran in
production is UNKNOWN / NOT ESTABLISHED. Paper-only code (the paper quote provider's alias loader, `main.py` L510 to
L518) is marked and not traced. Owners named for collaborators follow the Master System Investigation Index; their
logic is not studied here.

## 2. Construction and the processor's own state

### 2.1 The construction in `main.py`

P04-S001. FACT (`main.py` L3574 to L3623): `sp_cfg = app_config.system.signal_processor` is read at L3574, and the
`SignalProcessor(...)` call runs from L3575 to L3623 (the brief's L3622 is the last argument, `evidence`; the closing
parenthesis is L3623). The call passes 36 keyword arguments, in this order: `signal_queue=signal_queue` (L3576),
`state_store=store`, `bus=event_bus`, `fund_manager=fund_manager`, `position_sizer=position_sizer`,
`risk_engine=risk_engine`, `kill_switch=kill_switch`, `market_windows=market_windows`, `strategies=strategies` (L3584),
`scan_webhook_map=app_config.scan_webhook_map.scanners` (L3585), `secondary_screener=screener`,
`quality_scorer=scorer`, `order_placer=order_placer`, `logger=get_logger("signal_processor")` (L3589),
`worker_count=sp_cfg.worker_count` (L3590), `drain_poll_sec=sp_cfg.drain_poll_sec` (L3591),
`instrument_cache=instrument_cache`, `atr_fallback_mode=sp_cfg.atr_fallback_mode`, `tgt_min_pct=sp_cfg.tgt_min_pct`,
the four entry-throttle values read with `getattr(sp_cfg, <key>, <default>)` (L3596 to L3599; P06),
`notifier=notifier` (L3600), `mode=mode_label` (L3601), `shadow_tracker=shadow_tracker` (L3605),
`sr_detector=sr_detector`, `zone_warmer=zone_warmer` (L3609), `retest_sl_buffer_pct=_sr_cfg.sl_buffer_pct`,
`in_flight_release_fn=webhook_receiver.release_in_flight` (L3612), `signal_expiry_sec=
app_config.system.signal_queue.expiry_sec` (L3614, comment "Use same expiry as webhook_receiver (config
signal_queue.expiry_sec)"), `quote_fn=broker_adapter.get_quote`, `strategy_governor=_build_strategy_governor(store,
app_config, notifier, mode_label)` (L3618), `trade_type=app_config.system.trade_type` (L3620),
`force_intraday_only=app_config.system.force_intraday_only` (L3621) and `evidence=evidence_recorder` (L3622). The
arguments used before the handoff to A07 are studied here; the others are mapped by P05 (screening, sizing, risk,
capital, placement, S&R, quotes, evidence) and P06 (throttle).

P04-S002. FACT (`signals/signal_processor.py` L155 to L198; `main.py` L3575 to L3623): the constructor has 41
parameters after `self`. Five are not passed by `main.py` and take their defaults: `in_flight_heartbeat_fn=None`
(L172; P01-S077), `rate_limiter=None` (L189), `perf_weights=None` (stored as `{}`, L236), `allocator=None` (L195) and
`v3_chain=None` (L196). The allocator and the V3 chain are bound later through `set_allocator` (`main.py` L3650, L3660)
and `set_v3_chain` (L3693, L3700); the retest diverter through `set_retest_diverter` (L3793). Every one of these setter
calls comes before `signal_processor.start()` at L3974 in the file (line order). Their use is P05's. The effect of
`rate_limiter=None` on intake is in P04-S053.

P04-S003. FACT (`config/system_config.yaml` L344 to L353; `core/config_loader.py` L564 to L614; A02's file and
schema, read at the boundary): the `signal_processor` section (comment "SP15 — worker pool settings") holds
`worker_count: 5` ("ThreadPoolExecutor workers (1-50)"), `drain_poll_sec: 0.1` ("queue poll interval when empty"),
`pipeline_timeout_sec: 30` ("hard per-signal processing deadline"), `tgt_min_pct: 0.003` and the four FIX-190
entry-throttle keys (P06). The schema `SignalProcessorConfig` (`extra="forbid"`, L565) requires `worker_count`
(validated 1 to 50, L588 to L593), `drain_poll_sec` (> 0, L595 to L600) and `pipeline_timeout_sec` (>= 1, L602 to
L607); `atr_fallback_mode` (default `"WARN"`, L572) is not in the file. The constructor also floors the worker count
with `max(1, worker_count)` (L220). The effective values on the legacy machines are UNKNOWN / NOT ESTABLISHED (A02).

P04-S004. FACT (whole-repository search for `pipeline_timeout`, non-test and test code, with the four exclusions):
`pipeline_timeout_sec` is read only by its schema field and validator (`core/config_loader.py` L568, L602 to L607). The
processor has no such parameter and no per-signal deadline anywhere in its intake or worker code. HISTORICAL
(`tests/crash_test/ct_day2_isolated.py` L187): a test prints "pipeline_timeout_sec enforced at signal_processor, not
screener"; the code at `970aabf` does not enforce it. HISTORICAL (same search, documents): `docs/CONFIG_GUIDE.md` L355
calls the key a "hard deadline per signal", and the legacy integrity audit (`docs/audit/integrity_audit_2026.md` L3746
to L3749) already lists it as a key "consumed by NOTHING (0 hits in signal_processor; verified directly)"; documents are
not proof of what the code does. Configuration keys as a whole are P08's.

P04-S005. FACT (`config/system_config.yaml` L124 to L128; `core/config_loader.py` L192 to L197): `signal_queue` holds
`capacity: 300`, `backpressure_pct: 0.80`, `expiry_sec: 600` (comment "WR6: 10 min - Chartink triggered_at is scan
time, not delivery time") and `warning_pct: 0.60`. The schema field `expiry_sec: int` has no default, although its
comment says "(default 60)" (L196, HISTORICAL); the constructor's own default is `signal_expiry_sec: int = 60` (L175),
which `main.py` overrides. FACT (`git blame`/`git log`): the 600 s value is from commit `2e8448c` (28-Apr-2026, "config:
increase signal expiry to 600s (Chartink scan time != delivery time)"); `main.py` L3611 to L3614 are from `8536b53`
("fix: wire in_flight_release_fn to SignalProcessor") and `586af55` ("fix: pass signal_expiry_sec to SignalProcessor"),
both 28-Apr-2026.

P04-S006. FACT (`main.py` L3585; `core/config_loader.py` L2347 to L2377): the scan map passed is
`app_config.scan_webhook_map.scanners`, a `dict[str, ScannerEntry]`. Each `ScannerEntry` is a pydantic model with a
required `strategy: str`, a required `chartink_url` and `scanner_type` (default `"intraday"`, allowed `intraday` or
`eod`). HISTORICAL (`signals/signal_processor.py` L143, L166): the processor's comments describe the map as
`{scanner: {"strategy": name}}`, a plain dict; the lookup code accepts both forms (L939 to L942; P04-S030).

P04-S007. FACT (`strategies/loader.py` L102 to L156; `main.py` L3157 to L3162): `strategies` is the dict returned by
`StrategyLoader().load_all_strategies(strategies_dir, force_intraday_only=...)`, keyed by `StrategyConfig.name`
(L110, L149). The optional cross-check of the scan map against the loaded strategies ("S10", L151 to L153) runs only
when `scan_webhook_map_path` is passed; `main.py` does not pass it, and no non-test caller does (search for
`scan_webhook_map_path|_validate_scan_webhook_map|load_all_strategies\(`: `main.py` L3159,
`ops/control_tower/aggregator.py` L156, `scripts/preflight/checks/config_integrity.py` L155 and L173,
`scripts/preflight/checks/config_sanity.py` L37, `scripts/replay_signals.py` L188, `utils/startup_checks.py` L1284,
none with the path). HISTORICAL (`config/scan_webhook_map.yaml` L4 to L6): the map's header says the map is "Validated
at startup (P17, S10)"; HISTORICAL (`core/config_loader.py` L2344): the schema's comment says "Locked: P17 (no
duplicate scanner names; every name maps to a valid strategy YAML)", but neither `ScanWebhookMapConfig` (L2374 to
L2377) nor `AppConfig` (L2420 to L2434) has a validator that compares the map with the strategy files (FACT; search for
`model_validator` in the file: none on these two classes). By contrast, `main.py` loads the strategies from
`config_dir / "strategies"` (L3157), so they follow the `--config` directory. FACT (repository files at `970aabf`): the
map has 16 entries and `config/strategies/` has 16 YAML files; every map `strategy` value equals the `name:` of one YAML
file. The effective files are UNKNOWN / NOT ESTABLISHED.

P04-S008. FACT (`main.py` L3402 to L3404, L3408, L3576; search for `signal_queue` in non-test code): the queue the
processor drains is the single `queue.Queue(maxsize=app_config.system.signal_queue.capacity)` that the receiver fills
(P01-S008). Only the receiver and the processor hold the object; the processor keeps it as `self._queue` (L199).

### 2.2 The processor's own state (L199 to L298)

P04-S009. FACT (L199 to L298): the constructor stores its collaborators (L199 to L241) and builds:
- shallow copies `self._strategies = dict(strategies)` and `self._scan_webhook_map = dict(scan_webhook_map)`
  (L207 to L208); no other assignment to either name exists in the file (search);
- the lifecycle state `_running = False`, `_stop_event = threading.Event()`, `_dispatcher_thread = None`,
  `_executor = None` (L244 to L247);
- `_active_workers = 0` with `_active_lock` (a `threading.Lock`, L250 to L251);
- `_in_flight_count = 0` with `_in_flight_lock` (a `threading.RLock`, L256 to L257; FIX-018). This processor counter is
  distinct from the receiver's in-flight claims; it is first changed in `_admit_and_place` (L1302 to L1305), after the
  handoff (P05);
- the `EntryThrottle` instance (L262 to L268; P06);
- `_rt_metrics` with its lock (L273 to L279) and `_stats` with `_stats_lock` (L282 to L294);
- `_last_expired_alert_ts = 0.0` (L295; no lock guards it, P04-S043, P04-S061);
- the effect-telemetry handle `_fx_dispatch` (L217; P05).
It logs one INFO line when `order_placer` is `None` (L297 to L298).

## 3. Lifecycle: `start()`, the dispatcher, `stop()`, boot order and shutdown

### 3.1 `start()` and the threads

P04-S010. FACT (L304 to L324; lines from the initial commit `bcf03b5`, 17-Apr-2026): `start()` returns with a WARNING
if `_running` is already true. Otherwise it clears `_stop_event`, builds
`ThreadPoolExecutor(max_workers=self._worker_count, thread_name_prefix="sp-worker")`, builds one
`threading.Thread(target=self._dispatcher_loop, name="sp-dispatcher", daemon=True)`, sets `_running = True`, starts the
dispatcher and logs INFO "SignalProcessor started: <n> workers, drain_poll=<s>s". `start()` itself starts no worker
thread.

P04-S011. Current external context (read 17-Nov-2026: CPython 3.12 published source
`Lib/concurrent/futures/thread.py`, `submit` and `_adjust_thread_count`; Python documentation, `threading`, page
version 3.15.2): `submit` puts a work item on the executor's work queue and calls `_adjust_thread_count`, which starts a
new thread only when no idle worker is available and fewer than `max_workers` threads exist; the thread is named
`'%s_%d' % (thread_name_prefix, n)` and is created without a `daemon` argument; the documentation says the daemon flag,
when not given, "is inherited from the current thread". FACT (L390, L397; search for `submit(`): the processor calls
`self._executor.submit` only in the dispatcher loop (L1154 is the allocator's own `submit`, P05). INTERPRETATION: the
workers are created on demand, the first when the first signal is submitted, up to `worker_count` (5 in the file),
named `sp-worker_0` to `sp-worker_4` at that value, and they are daemon threads because they are created by the daemon
thread `sp-dispatcher`.

P04-S012. Current external context (read 17-Nov-2026: Python documentation, `concurrent.futures`, page version
3.15.2: "All threads enqueued to ThreadPoolExecutor will be joined before the interpreter can exit"; CPython 3.12
source: `_python_exit`, registered with `threading._register_atexit`, puts a wake-up item on each worker's queue and
joins each worker): INTERPRETATION: at interpreter exit the workers are waited for although they are daemon threads; the
dispatcher, a daemon thread not owned by the executor, is not waited for (Python documentation, `threading`: "Daemon
threads are abruptly stopped at shutdown").

### 3.2 The get loop (SP5)

P04-S013. FACT (L377 to L391): while `_stop_event` is not set, the dispatcher calls
`self._queue.get(timeout=self._drain_poll_sec)`; any exception from the call is treated as "empty" (`except Exception:
# queue.Empty`, then `continue`). For each item it calls `_warm_zones(signal_tuple)` (L388) and then, if `_executor`
is not `None`, `self._executor.submit(self._process_one_safe, signal_tuple)` (L389 to L390). The returned future is not
kept.

P04-S014. Current external context (Python documentation, `queue`, page version 3.15.2, read 17-Nov-2026): with a
positive timeout `get` "blocks at most timeout seconds and raises the Empty exception if no item was available within
that time"; `Queue` is a FIFO queue. CPython 3.12 source (`ThreadPoolExecutor.__init__`): the executor's work queue is
`queue.SimpleQueue()`, which the documentation describes as "an unbounded FIFO (first-in, first-out) queue".
INTERPRETATION: with `drain_poll_sec` 0.1 (file value) the dispatcher checks the stop flag at least every 0.1 s while
idle; it never waits for a free worker, because `submit` only appends to the unbounded work queue. Each item is moved
out of `signal_queue` as soon as it is got (backpressure consequences: P04-S050).

P04-S015. FACT (L361 to L375; `main.py` L3545 to L3572): `_warm_zones` runs on the dispatcher thread before the
submit. It does nothing when `_zone_warmer` is `None`; otherwise it reads the symbol (dict key `symbol`, or tuple index
2) and calls `self._zone_warmer.enqueue(symbol)`, swallowing every exception. `main.py` builds the zone warmer only
inside `if _v2_on or _struct_exit_on:` (L3549) and sets it to `None` on a wiring failure (L3569 to L3571). The
behaviour of `enqueue` (whether it can block) is A08's and is UNKNOWN here. INTERPRETATION: if `enqueue` blocked, the
dispatcher would stop moving signals until it returned.

### 3.3 `stop()` and the drain

P04-S016. FACT (L392 to L399): after the stop flag is set, the dispatcher leaves its loop and drains:
`self._queue.get_nowait()` and, if `_executor` is not `None`, `submit`, repeated until any exception, which ends the
drain (`except Exception: break`). The drain does not call `_warm_zones`.

P04-S017. FACT (L326 to L347; `git blame`: lines from `bcf03b5` except L342 to L345, from `a4ef762`, 18-May-2026,
"FIX-100 reuse step_executor ThreadPoolExecutor across calls"): `stop()` returns at once
when `_running` is false. Otherwise it sets `_stop_event`; joins the dispatcher with `timeout=10.0`; calls
`self._executor.shutdown(wait=True, cancel_futures=False)` and sets `_executor = None`; calls the screener's
`shutdown()`
if it has one (A07's step executor); sets `_running = False`; and logs INFO "SignalProcessor stopped". It does not check
`is_alive()` after the join, does not release receiver claims, does not change the status of any signal, and the file
never calls `task_done()` or `join()` on the queue.

P04-S018. Current external context (read 17-Nov-2026: Python documentation, `threading`, `Thread.join`: "you must call
is_alive() after join() to decide whether a timeout happened"; `concurrent.futures`, `Executor.shutdown`: with
`wait=True` the method "will not return until all the pending futures are done executing", and only
`cancel_futures=True` cancels futures not yet started; calls to `submit` after shutdown "will raise RuntimeError"; page
version 3.15.2): INTERPRETATION:
(a) `stop()` waits, with no time limit, until every signal already submitted (running, or waiting in the executor's
    work queue, the drained ones included) has finished its pipeline run. Because `stop()` sets `_stop_event` first
    (L333), a signal that reaches the pre-placement check at L1398 after that moment is rejected `SHUTDOWN` there, not
    placed (P04-S019); before that point it still runs the intake checks, screening, price derivation, sizing, risk
    approval and reservation (the reservation is released at L1402 to L1404). A placement already under way when
    `stop()` is called continues. The only fixed wait is the 10 s join. HISTORICAL (L327 to L329): the
    docstring says "wait for in-flight tasks to complete (up to 5s per SP4)"; the code sets no such bound. HISTORICAL
    (`tests/unit/test_signal_processor.py` L469 to L479): a test expects `stop()` to finish within 5 s with 20 signals
    queued, using its own mock collaborators.
(b) If the join timed out while the dispatcher was still draining, the executor is shut down underneath it; the next
    `submit` raises `RuntimeError`, which the drain's `except Exception: break` swallows, and the remaining items stay
    in `signal_queue`; once `_executor` is `None` (L340), an item already taken by `get` is not submitted (L389, L396)
    and is dropped without any status change. The drain is a tight loop of `get_nowait` and `submit`, so a 10 s
    timeout needs producers that keep the queue non-empty that long; whether it ever happened is UNKNOWN / NOT
    ESTABLISHED.
A01 RECONCILED TOPIC RECORD section 4.5 (C18) records the shutdown's fixed waits and "a second unbounded wait in step
6 (the step executor)" and the declared unit's `TimeoutStopSec=30`; the A06 side is that the processor's executor
shutdown at L339 is itself unbounded. What the service manager does when its stop timeout passes is A01's and A17's.

P04-S019. FACT (`main.py` L1629, L1681 to L1692; P01-S081): `_shutdown` sets `_shutdown_event` first, then calls
`webhook_receiver.stop()` and `signal_proc.stop()`, each in its own `try`. FACT (search in
`signals/signal_processor.py` for `_stop_event` and `_shutdown`): the processor reads no shutdown event or flag other
than its own `_stop_event`, which it reads at L383 (the dispatcher loop), at L1398 (in `_admit_and_place`, after the
handoff) and at L2215 and L2524 (the gate and retest resume paths). FACT, interface only (L1384 to L1405; lines from
`536172c`, the extraction commit; the check itself was introduced as FIX-070 by `31c6a62`, 16-May-2026): after the
late kill-switch check and immediately before the entry throttle and placement, `if self._stop_event.is_set():` logs a
WARNING "FIX-070: shutdown event set - aborting placement ...", releases any reservation ("shutdown_before_placement")
and raises `_PipelineReject("SHUTDOWN", "System shutdown before placement")`. INTERPRETATION: no intake check refuses a
signal because the processor is stopping: the drained signals pass the same intake checks as any other (kill switch,
entry window, expiry, shadow guard, strategy lookup and controls) and then screening and the later steps; only at
L1398 is a signal whose run reaches that point after `stop()` began rejected as `SHUTDOWN` (status `REJECTED_SHUTDOWN`
through the handler of P04-S035), so the drain ends without new placements from the FCFS path but not without the
screening, sizing and reservation work. The placement-side logic is P05's to map (A09, A10); what the later shutdown
steps do with orders placed before the flag was set is A01's and A10's.

P04-S020. INTERPRETATION (P01-S084; P04-S016): a receiver request that passed its shutdown gate before
`webhook_receiver.stop()` may put an item after the drain's last empty `get_nowait`; that item stays in `signal_queue`,
which nothing else consumes and which exists only in memory. FACT (search for `'QUEUED'`, `"QUEUED"` and `'PROCESSING'`
in non-test code): no code reads `signals` rows with status `QUEUED` back into a queue at start-up; the `QUEUED` hits
are the schema, the dashboard, `reports/signal_status.py` and the receiver, and the `PROCESSING` hits are the
processor's own writes, `scripts/eod_cleanup.py` and a count in `scripts/system_manager.py` L680. FACT, interface
only (`scripts/eod_cleanup.py` L105 to L127; not A06's file): the cleanup marks earlier-day rows with status
`PROCESSING` as `EXPIRED`; it does not touch
`QUEUED` rows. INTERPRETATION: a signal still in the queue, or in the executor's work queue at a hard stop, is lost with
the process; its `signals` row stays `QUEUED` (or `PROCESSING` if a worker had started it), and its receiver claim
disappears with the process memory.

### 3.4 Boot order (`main.py` L3868 to L3974)

P04-S021. FACT (`main.py` L3868 to L3881, L3894 to L3899, L3965 to L3977, L3979 to L4000): under the comment "BUILD 1
INVARIANT (#12, 24-Jun): this SYNCHRONOUS reconcile_once() MUST precede signal_processor.start() and the webhook
server start", `main.py` runs `recon_actions = order_reconciler.reconcile_once()` (L3880) and sets
`_startup_reconcile_done = True` (L3881); an active kill switch after reconciliation closes the store and returns 1
(L3894 to L3899). After the candle store, feed, order monitor, reconciler, skew probe and token monitor starts, it runs
`assert _startup_reconcile_done, (...)` (L3968 to L3971) and `signal_processor.start()` (L3974), before
`entry_gate.start()` (L3975; comment "signal_processor BEFORE entry_gate (BLOCKER #5 fix): gate may call
continue_from_gate() immediately on release", L3972 to L3973), `smart_tgt.start()`, `tgt_retry_manager.start()` and
the waitress server thread (L3979 to L4000; P01-S072). `_startup_reconcile_done` is assigned only at L3881 (search).

P04-S022. Current external context (Python Language Reference 7.3, "The assert statement", page version 3.15.2, read
17-Nov-2026: "The current code generator emits no code for an assert statement when optimization is requested at
compile time"; `__debug__` is False under `-O`). FACT (`main.py` L2193, L3880 to L3974): L3881 and L3968 both sit at
the top indentation level of `_main_locked` (defined at L2193), with no loop between them; L3881 is unconditional, and
the only exit between them is the `return 1` at L3899. INTERPRETATION: reaching L3968 already implies L3881 ran; the
order is held by the statement order, and the assert adds no runtime protection (and none at all under `-O`). FACT, interface only (`deploy/systemd/trading-system.service` L18 to L19;
A17's file): the declared start command runs the venv's `python` on `main.py --mode live` without `-O`. Whether any
production run used optimisation by another route is UNKNOWN / NOT ESTABLISHED.

P04-S023. INTERPRETATION (P04-S021; P01-S072): between L3974 and L4000 the dispatcher polls an empty queue, because
the only external producer, the waitress server, starts at L4000. The processor is stopped at `main.py` L1690 inside
`_shutdown` (P04-S019).

## 4. From `queue.get` to the handoff to A07

### 4.1 What arrives and the safe wrapper

P04-S024. FACT (`signals/webhook_receiver.py` L993 to L995, L1047 to L1049; P01-S042; `signals/signal_processor.py`
L78, L426, L1510 to L1520; search for `\._queue\b` in `main.py`, `signals/`, `scripts/`, `ops/` and `utils/`): four
places put items on `signal_queue`. The receiver puts the 5-tuple `(signal_id, scanner_name, symbol, price,
triggered_at)` with `put_nowait` at two sites: the normal path (L1047 to L1049) and the M-S2 re-accept of an earlier
`QUEUE_FULL` row (L993 to L995), which reuses that row's `signal_id` with the current request's other values (P01-S041;
the re-accept is P03's). The processor itself re-puts the same item in its FIX-007 rate-limiter
branch (L426) and puts a dict `{signal_id, scanner_name, symbol, trigger_price, triggered_at, retry_count}` in its
FIX-069 retry branch (L1510 to L1520). `_SIGNAL_TUPLE_FIELDS` (L78) names the tuple positions `signal_id`,
`scanner_name`, `symbol`, `trigger_price`, `triggered_at`; the receiver's `price` is the processor's `trigger_price`.

P04-S025. FACT (L405 to L413, L463 to L480; FIX-069 lines from `397105d`, 16-May-2026): `_process_one_safe` first
derives `signal_id` and `symbol` for its log lines (dict keys, or tuple positions 0 and 2, with the literal fallback
`"unknown"`), then runs the FIX-007 pre-check (L415 to L461; P04-S053), then increments `_active_workers` under its
lock, calls `_process_one` inside `try`, and on any `Exception` logs ERROR "Unhandled exception in pipeline for ..."
with the traceback and writes `update_signal_status(signal_id, "PLACEMENT_FAILED", f"unhandled: {exc}")`, swallowing
any error of that write; the `finally` decrements `_active_workers`. Its docstring: "catches all exceptions so workers
never die" (L406).

P04-S026. FACT (L876 to L887, L895): `_process_one` unpacks the item before its `try` (L895): a dict is read by key
(`signal_id`, `scanner_name`, `symbol`, `trigger_price`, `triggered_at`; `retry_count` with default 0); anything else
is unpacked as exactly five values with `retry_count = 0`. INTERPRETATION: an item with a missing key or the wrong
length raises before the `try`, so the `finally` that releases the receiver's claim (L1248 to L1271) does not run; the
exception reaches `_process_one_safe` (P04-S025). The receiver's 5-tuple and the FIX-069 dict always carry all five
fields, so no producer at `970aabf` creates such an item.

P04-S027. FACT (L889 to L899): the worker records `start_mono`, sets `reservation_id = None`, `requeued = False`,
`in_flight_incremented = False` and `handed_off = False`, and inside the `try` first writes
`update_signal_status(signal_id, "PROCESSING")` (the status write is P05's), increments the `signals_processed` runtime
metric and calls `_heartbeat(symbol)`, which does nothing because no heartbeat callback is wired (L664 to L673;
P01-S077).

### 4.2 Step 1: pre-flight checks

P04-S028. FACT (L905 to L912): when a kill switch is wired (`if self._ks and ...`, L906), it is asked
`self._ks.is_active("entry")`; true raises `_PipelineReject("KILL_SWITCH", "Kill switch is active")`. The receiver's
own check asks `self._ks.is_active()` with no argument (`signals/webhook_receiver.py` L567); what the argument changes
is A13's. Then `now = now_ist()` (L910) and
`self._mw.is_entry_allowed(now)`; false raises `_PipelineReject("OUTSIDE_ENTRY_WINDOW", "Outside entry window")`. The
kill switch (`capital/kill_switch.py`) is A13's and the market windows (`core/market_windows.py`) are A01's (Master
System Investigation Index, entries A13 and A01); only the call and the reject label are recorded here. The receiver
makes its own kill-switch and window checks before queueing (P02-S069, rows 16 and 18).

P04-S029. FACT (L914 to L921): the age check follows the window check (section 5). FACT (L928, L1976 to L2008;
`main.py` L3605): `_reject_if_shadow_inning_active(symbol)` asks the shadow tracker (`orders/shadow_tracker.py`,
A11's) `is_tracking(symbol)`; true raises `SHADOW_INNING_ACTIVE`; an exception raises `SHADOW_TRACKER_ERROR` ("failing
closed"); no tracker means no check. `main.py` passes `shadow_tracker=shadow_tracker`. HISTORICAL (L565 to L566): a
docstring says "measured on production, 4,168 of 48,934 P2 rejects (all SHADOW_INNING_ACTIVE)"; a docstring is not
evidence of what ran (UNKNOWN / NOT ESTABLISHED).

### 4.3 Step 2: the `scan_webhook_map` lookup

P04-S030. FACT (L933 to L953): the strategy lookup is `self._scan_webhook_map.get(scanner_name)`: an exact,
case-sensitive dictionary-key lookup on the scanner name carried in the item (the receiver's path segment, P01-S042).
Three outcomes raise `_PipelineReject("UNKNOWN_STRATEGY", ...)`: no entry ("No entry in scan_webhook_map for scanner
..."); an entry whose strategy resolves to `None` ("... has no 'strategy' key"); a strategy name not in
`self._strategies` ("Strategy ... not in loaded strategies"). The strategy name is `entry.get("strategy")` for a dict
and `getattr(entry, "strategy", str(entry))` otherwise. There is no default strategy and no fallback.

P04-S031. INTERPRETATION (P04-S006 to P04-S009; P01-S035; P01-S052): under `main.py`'s wiring, (a) the receiver has
already answered 404 for a path segment that is not a key of the same `scan_webhook_map.scanners` mapping, and the
processor's copy holds the same keys taken at construction, so the "no entry" branch is reachable only if that mapping
changed after the processor was built (whether the configuration object can change in-process is A02's); (b) the
"no 'strategy' key" branch cannot be reached with `ScannerEntry` objects, whose `strategy` is a required string; an
empty string would instead reach (c); (c) "not in loaded strategies" is reachable when a map strategy has no loaded
YAML, which the unrun S10 check would have caught (P04-S007); with the repository files every map strategy has a YAML.
FACT (search): the processor never reads `scanner_type`; an `eod` scanner's alert is not queued by the receiver
(P01-S052), so its entry reaches the processor only if some other producer queued it (none does).

### 4.4 Strategy controls, as far as they gate intake

P04-S032. FACT (L955 to L990; `strategies/control.py` L41 to L44, L47 to L72; A07's file, interface only): three
strategy-level checks follow the lookup, each raising a `_PipelineReject` before screening:
`strategy_will_trade(strategy_obj, trade_type=self._trade_type, force_intraday_only=self._force_intraday_only)`
returns a frozen `Verdict` with `will_trade`, `reason`, `product` and `cause` (L47 to L64); when `will_trade` is
false the reject label is `TRADE_TYPE` if `cause` is `CAUSE_TRADE_TYPE`, otherwise `STRATEGY_CONTROL` (L959 to L972);
`self._mw.is_entry_allowed_for_strategy(now, strategy_obj)` false gives `OUTSIDE_ENTRY_WINDOW` with the strategy's
own times (L977 to L982); when a strategy governor
is wired, `self._strategy_governor.check(strategy_name, now.time())` returning paused gives `STRATEGY_CIRCUIT_BREAKER`
(L985 to L990; `capital/strategy_governor.py`, A09's; `main.py` L3618 always passes the result of
`_build_strategy_governor`). Their logic is A07's, A01's and A09's. HISTORICAL (`config/scan_webhook_map.yaml` L79 to
L80): the PB-01 entry's comment says its strategy is `enabled:false` and "a raw firing is rejected at the
strategy-control gate".

### 4.5 Where intake ends for this part

P04-S033. FACT (L992 to L1006): Step 3 calls `self._screener.screen(signal_id, symbol, scanner_name, trigger_price,
triggered_at, direction=strategy_obj.direction, intent=strategy_obj.intent, strategy=strategy_obj, market_data=None)`
and records the screener's statistics. INTERPRETATION (Rama's decision A of 17-Nov-2026: screening belongs to A07):
this part's description stops at this call; everything from L997 on is mapped by P05, which records the contract at
the candidate handoff lines and leaves the exact A06-to-A07 handoff line open (P05-S031; OPEN FOR RAMA, STUDY section 17).

P04-S034. FACT (L876 to L1006; P01-S042): how each field survives from the queue item to the screener call:

| Field | Source in the item | Change in the processor before L998 | Use before L998 |
|---|---|---|---|
| `signal_id` | position 0 / key | none | status writes (L897), passed to the screener |
| `scanner_name` | position 1 / key (the receiver's path segment) | none | map key (L933), passed to the screener; the receiver also stored it as the row's `strategy` (P01-S043) |
| strategy name | not in the item | resolved from the map (L939 to L942): the first strategy identity distinct from the scanner name | strategy lookup, controls, governor |
| `symbol` | position 2 / key (after the receiver's strip and alias) | none: no case, prefix or suffix change (section 6) | zone warming on the dispatcher (L369, L371), the safe wrapper's log text (L410, L413), heartbeat (no-op), shadow guard, passed to the screener; later the claim release |
| `trigger_price` | position 3 / key (the receiver's float `price`) | none | passed to the screener |
| `triggered_at` | position 4 / key (IST-aware, P02-S055) | none to the object; a re-zoned copy is used only for the age (L915) | age check, passed to the screener |
| `retry_count` | dict only (FIX-069) | 0 for a tuple | carried to placement (P05) |
| received time, `expires_at`, fingerprint, payload | not in the item | n/a | only in the `signals` row (P03, P05) |
| direction and intent | not in the item | taken from the strategy object (L1000 to L1001) | passed to the screener |

The worker's own `now` (L910) is new and is used for the window, the age and the governor.

P04-S035. FACT (L1193 to L1231, L1248 to L1276): every intake reject is a `_PipelineReject` caught at L1193: the
worker logs INFO "Signal ... rejected at <check>: <reason>", counts `entries_rejected` (all checks except
`ENTRY_THROTTLED`), writes `update_signal_status(signal_id, f"REJECTED_{check}", reason)` (P05), emits a `P2_REJECT`
evidence record whose strategy comes from `_evidence_strategy_for(scanner_name)` (L560 to L580: the same map lookup as
Step 2; P05), releases a reservation if one exists (none exists before the handoff), counts the reject per check in
`_stats` and, for `EXPIRED` only, may send the alert of P04-S043. FACT (`git blame` L1202 to L1211): the `P2_REJECT`
emission lines are from `8d27fdb` and `056905b` (10 and 11-Sep-2026), later than the last recorded deployment
(`686df1c` and `7d4970a`, 02-Sep-2026; Decision Register D-21); whether production ran them is UNKNOWN / NOT
ESTABLISHED. If the status write at L1201 raises, the later steps of the handler do not run (P04-S055). The `finally` then releases the receiver's claim
(P04-S057) and adds the elapsed time to `_stats`. The reject labels raised before L998 are `KILL_SWITCH`,
`OUTSIDE_ENTRY_WINDOW`, `EXPIRED`, `SHADOW_INNING_ACTIVE`, `SHADOW_TRACKER_ERROR`, `UNKNOWN_STRATEGY`, `TRADE_TYPE`,
`STRATEGY_CONTROL` and `STRATEGY_CIRCUIT_BREAKER`.

## 5. Expiry

P04-S036. FACT (`main.py` L3614; `config/system_config.yaml` L127; `signals/webhook_receiver.py` L537, L679): the
processor's limit `_signal_expiry_sec` is `app_config.system.signal_queue.expiry_sec`, fixed at construction (L222);
the receiver reads the same key from its configuration object on every request (`sq_cfg = self._config.system.
signal_queue`, L537; `expiry_sec = sq_cfg.expiry_sec`, L679). The repository value is 600 s; the effective value is
UNKNOWN / NOT ESTABLISHED. INTERPRETATION: the two sides use one value while the configuration object is unchanged; if
that object were replaced in a running process, the receiver would follow it and the processor would not (whether
that can happen is A02's).

P04-S037. FACT (L897 to L921; `git blame`: L909 to L921 from `bcf03b5`, except L915, whose `_IST` became
`ist_timezone()` in `f67a0c7`, 27-Apr-2026): in the worker
the order is: status `PROCESSING` (L897), kill switch (L906), `now = now_ist()` (L910), entry window (L911), then the
age: `triggered_aware = triggered_at.replace(tzinfo=ist_timezone())` (L915, unconditional), `age_sec = (now -
triggered_aware).total_seconds()` (L916), and `age_sec > self._signal_expiry_sec` raises `_PipelineReject("EXPIRED",
f"Signal age {age_sec:.1f}s > expiry {self._signal_expiry_sec}s")` (L917 to L921). The comment calls it
"defense-in-depth; receiver also checks" (L914). An expired signal that is also outside the window is therefore
rejected as `OUTSIDE_ENTRY_WINDOW`, and every expired signal first has its status set to `PROCESSING`.

P04-S038. Current external context (Python documentation, `datetime`, page version 3.15.2, read 17-Nov-2026): "If you
merely want to attach a timezone object tz to a datetime dt without adjustment of date and time data, use
dt.replace(tzinfo=tz)"; subtracting two aware datetimes with the same `tzinfo` makes "No time zone adjustments";
subtracting a naive from an aware one raises `TypeError`. FACT (P02-S055, P02-S056; `signals/webhook_receiver.py` L640
to L653, L920 to L923; `core/time_authority.py`, A01's file, as P02-S056 records): the receiver's `triggered_at` is
always aware, carrying `_IST`, a fixed UTC+05:30 `timezone`, and `now_ist()` returns `datetime.now(tz=_IST)`.
INTERPRETATION: for every item produced at `970aabf` the re-zoning at L915 changes nothing, and the age is a plain
wall-clock difference in IST. For a naive value (the processor's docstring still says "triggered_at: naive datetime
(IST)", L874, HISTORICAL since FIX-022; the unit tests build tuples with a naive `datetime.now()`,
`tests/unit/test_signal_processor.py` L593, HISTORICAL) the replace labels it IST without conversion. For an aware
value with another offset it would relabel the wall time as IST without converting it (no producer creates one). The
receiver, by contrast, attaches IST only when the value is naive (L920 to L923).

P04-S039. INTERPRETATION (P04-S037; P02-S055, P02-S058; P04-S050): the processor's age runs from Chartink's
`triggered_at` as the receiver parsed it to the worker's `now`. HISTORICAL (`config/system_config.yaml` L127): the
configuration comment says that value "is scan time, not delivery time". The age therefore includes the delivery
delay, the receiver's own handling, the wait in `signal_queue`, the wait in the executor's work queue and the
`PROCESSING`, kill-switch and window calls. For the two time-only formats the receiver sets the seconds to 0
(`signals/webhook_receiver.py` L646 to L647), so the measured age starts at the beginning of the stated minute. The
receiver applies the same limit at receipt (receiver L919 to L926; P02-S058), with a separate `now_ist()` read. A
signal accepted by the receiver with an age just under 600 s can therefore be rejected `EXPIRED` by the worker after
a short wait. An age exactly equal to the limit
passes both checks (`>`).

P04-S040. FACT (L917; P02-S058): the processor has no lower bound either: a `triggered_at` later than the worker's
`now` gives a negative age and passes. Neither side checks that the date is the trading day beyond the age itself.
INTERPRETATION: a time-only value later in the day than the receiver's clock, which the receiver dates "today"
(receiver L645 to L647), passes both checks; a full-format value from an earlier day is stopped only by the age.

P04-S041. FACT (search for `expires_at` outside `tests/` and `docs/`: no hit in `signals/signal_processor.py`; the hits
on the `signals` column are `core/schema.sql` L49 (comment "received_at + signal_expiry_sec", HISTORICAL),
`signals/webhook_receiver.py` L960 to L976, `ops_dashboard/backend/readers/db_reader.py` L826, the dashboard template
that shows that reader's field (`ops_dashboard/frontend/templates/signals.html` L441), a dashboard test fixture
(`ops_dashboard/tests/conftest.py` L54) and a script that inserts rows (`scripts/t2_cnc_gtt_realtest.py` L229); the
other hits are unrelated token-expiry fields in scripts): the stored `expires_at` (`received_at + expiry_sec`, P02-S075)
is not read by the processor. INTERPRETATION: the code holds three expiry notions: the receiver's age from `triggered_at`
at receipt, the worker's age from `triggered_at` when it starts the signal, and the stored `expires_at` from
`received_at`, which only the dashboard reader (A15) selects.

P04-S042. FACT (L2010 to L2048, L2375 to L2405; search for `_signal_expiry_sec`: only L222, L917, L920): the two
resume entry points, `continue_from_gate` and `continue_from_retest`, re-check the kill switch, the window and the
shadow guard but have no age check. HISTORICAL (L2378, L2396): their texts say "NOT the :607 60s expiry" and "NO 60s
expiry — park-and-resume"; the check is at L917 and the configured value is 600 s. These paths are A07's and A18's
(P05 maps them).

P04-S043. FACT (L1221 to L1231, L295; lines from `e55cb59`, 31-May-2026, "FIX-136: batch9 -- ... signal expiry ...",
HISTORICAL): after an `EXPIRED` reject, if a notifier is set and more than 60.0 s (monotonic) have passed since
`_last_expired_alert_ts`, the worker stores the new time and calls `self._notifier.send_warning(f"[{self._mode}] Signal
EXPIRED: {symbol} age={rej.reason}")`, swallowing any exception. INTERPRETATION: because `rej.reason` is the whole
reason text, the message reads "[<mode>] Signal EXPIRED: <symbol> age=Signal age <x>s > expiry <n>s"; at most one such
alert is sent per 60 s for the whole processor, and the other expired signals are only logged (INFO, L1194 to L1196)
and given the status `REJECTED_EXPIRED` (L1201). FACT (search): the receiver sends no alert for its own `EXPIRED`
answer (no notifier in `signals/webhook_receiver.py`). The notifier is A14's; whether any such alert was sent is
UNKNOWN / NOT ESTABLISHED.

P04-S044. FACT (L1510 to L1517; L878 to L884): a FIX-069 retry dict carries the original `triggered_at`, and the
retried signal passes L917 again. INTERPRETATION: each retry is re-tested against the original age, so a retried signal
can expire. The clock behind both ages is the machine clock read through `now_ist()`; how that clock is kept is A01's
and A04's (UNKNOWN / NOT ESTABLISHED here).

## 6. Symbol and alias normalisation at intake

P04-S045. FACT (L876 to L1006; search of `signals/signal_processor.py` for `.upper(`, `.lower(`, `strip(`, `alias`,
`NSE:`, `-EQ`, `BSE:` and `exchange`): the processor applies no transformation to the symbol before the screener call:
it takes `symbol` from the item (L881, L886) and passes it unchanged. The only `.upper()` and `.lower()` hits act on
the direction or side (L532, L839), the mode label (L651) and the reject label in reservation-release reasons
(`rej.check.lower()`, L1215, L1675, L2331, L2609); none acts on a symbol, and the file has no `strip(` hit. The processor makes no instrument lookup before the
handoff: its only use of `instrument_cache` is `_sector_for` (L1605 to L1617), called from `_build_v3_signal` (L1601)
and `_build_candidate` (L1644), both after sizing (P05; the A05 side is IN-08, A05 RECONCILED TOPIC RECORD section
4.6).

P04-S046. FACT (`signals/webhook_receiver.py` L670, L701, L709 to L717; P01-S039, P01-S040, P02-S059): every symbol
change at intake happens in the receiver, before the in-flight claim, the dedup key, the `signals` row and the queue
item: each comma-separated element is stripped of surrounding white space (L670); the alias map is looked up with the
upper-cased text and, on a miss, the stripped raw text is kept in its received case (L701); the excluded-symbol check is
case-insensitive (P01-S040). FACT (search of both files for `NSE:`, `-EQ`, `BSE:`, `exchange`: no hit): neither the
receiver nor the processor removes or adds an exchange prefix or a series suffix. INTERPRETATION: a symbol that
arrives with a prefix or suffix, or in lower case without an alias, reaches the screener in that form; how A07 and the
later lookups treat it is theirs. A05 recorded the same pattern across the market-data code (XC-04: symbol text
normalised separately at each site, none removing a series suffix; A05 RECONCILED TOPIC RECORD section 4.12).

P04-S047. FACT (`signals/webhook_receiver.py` L227, L258 to L292; `main.py` L2099): the alias map is loaded once, in
the receiver's constructor (L227, the only call of `_load_symbol_aliases`), from `Path("config/symbol_aliases.yaml")`,
a path relative to the process's working directory; it does not use the `--config` directory (`main.py` L2099 builds
`config_dir` from `--config`). A missing file gives a WARNING ("no alias translation will occur") and an empty map
(L266 to L271; docstring "fail-open: no aliases = passthrough", L263). Otherwise `yaml.safe_load(f) or {}` is read and
every pair whose key and value are both truthy becomes `str(key).upper(): str(value).upper()` (L274 to L281), with an
INFO count. Any exception (an unreadable file, invalid YAML, a top-level value without `.items()`) gives an ERROR and an
empty map (L287 to L292). There is no reload, no check of a key or value against the instrument file, no strip of the
key or value text, and no check for chains or duplicate targets. Unlike the strategies (`config_dir / "strategies"`,
`main.py` L3157), the alias file does not follow `--config`. FACT (L792; P01-S052): the same map is also applied, in
the same way, on the EOD route before the PB-01 capture submit; that path never reaches the queue. FACT, interface only
(`deploy/systemd/trading-system.service` L10; A17's file): the declared unit sets `WorkingDirectory` to the
repository directory (path not reproduced). INTERPRETATION: under that unit the relative path resolves to the
repository's `config/symbol_aliases.yaml`; started from another directory, the receiver would log one WARNING and run
the whole day without aliases.

P04-S048. FACT (`config/symbol_aliases.yaml` L1 to L10, A02's file read at the boundary; commits `3975e75` and
`435b3a2`, 07-May-2026): the file holds two entries; one maps a base name to a value carrying the "-BE" series suffix
(commit subject: "Chartink sends base, Kite has -BE series"). INTERPRETATION: the alias step can add a suffix, and the
resulting text is the claim key, the dedup key, the row's symbol and the queue item's symbol (P01-S039). The file and
the alias tool are A02's and A05's (A05 IR-10, IR-13, IR-30; A05 RECONCILED TOPIC RECORD section 4.7); a second loader
of the same file in `main.py` L510 to L518 serves the paper quote provider (paper-only; not traced).

P04-S049. INTERPRETATION (P04-S045 to P04-S048): the failure modes at intake are: (a) an alias miss, where the raw text
continues with its received case; (b) a missing or unreadable alias file, where no alias applies for the life of the
process and the only sign is one WARNING or ERROR at construction; (c) an alias value, or a raw symbol, that is not a
broker symbol, which nothing at intake detects (no instrument check in either file, P02-S059) and which continues to
screening (A05 records the instrument cache's lookups as exact and case-sensitive, A05 RECONCILED TOPIC RECORD section
4.6; how A07 and the later consumers meet such a symbol is theirs); (d) two raw names that resolve to the same text share one in-flight claim and one dedup key (the claim and
dedup behaviour is P03's).

## 7. Backpressure, ordering, retries, worker failure and the in-flight release

### 7.1 Backpressure

P04-S050. FACT (`signals/webhook_receiver.py` L571 to L578, L741 to L744, L1049 to L1068, L396 to L397;
`signals/signal_processor.py` L463 to L480, L2699 to L2702): every live queue measure in the two files reads
`signal_queue.qsize()` (or meets `queue.Full`): the receiver's 503 when `q_size >= int(capacity * backpressure_pct)`
(P03), its `X-Queue-Depth` and `X-Queue-Warning` response headers (L741 to L744; P03), its `QUEUE_FULL` on
`put_nowait` failure (P03), its `/health` queue size, and the processor's `stats()["queue_depth"]` (the `/metrics`
fields of the same name are P04-S065). `stats()["workers_active"]` counts only the calls inside
`_process_one_safe`'s `try`. No counter in either file reports signals that have been submitted to the executor but not
started. INTERPRETATION (P04-S013, P04-S014): while the dispatcher runs, it moves each item into the executor's
unbounded work queue at once, whether or not one of the five workers is free, so a backlog builds in that work queue
and `signal_queue` stays close to empty. The receiver's backpressure answers then do not engage however long the
backlog is; they can engage only when the dispatcher is stalled (P04-S015), ended (P04-S056) or not yet started. The
backlog's only limit is the age check when each signal reaches a worker (section 5). Python documentation (`queue`,
read 17-Nov-2026): `qsize()` returns "the approximate size of the queue". Whether a backlog ever formed in production is
UNKNOWN / NOT ESTABLISHED.

P04-S065. (added in the check) FACT, interface only (`scripts/healthcheck_server.py` L133 to L155, L251 to L257, A15's
file; `main.py` L4074 to L4076; `signals/signal_processor.py` L683 to L738; `scripts/preflight/checks/signals.py` L66 to
L82, A20's file; search for `queue_depth|queue_capacity` in `scripts/healthcheck_server.py` and `main.py`, and for
`queue` in `signals/entry_throttle.py`): the health server's `/metrics` answer starts from `"queue_depth": 0` and
`"queue_capacity": 0` (L153 to L154) and merges the dict returned by `metrics_provider()` (L251 to L257), which
`main.py` sets to `signal_processor.get_runtime_metrics`. Neither the health server, nor `get_runtime_metrics`, nor the
throttle metrics it merges (L708) sets either key, so under `main.py`'s wiring `/metrics` reports both as 0. A20's
`WebhookBackpressureCheck` reads these two fields and warns only `if cap and depth >= cap * 0.9` (L76 to L79).
INTERPRETATION: with a capacity of 0 the check always takes its pass branch ("webhook queue 0/? (no backpressure)",
L81); its 0.9 factor differs from the receiver's `backpressure_pct` 0.80 and `warning_pct` 0.60 (file values); and even
a real depth would show `signal_queue`, not the executor backlog (P04-S050). The check's logic is A20's and the
endpoint A15's; only the interface is recorded here (Rama's decision C).

### 7.2 Ordering

P04-S051. Current external context (Python documentation, `queue`: `Queue` and `SimpleQueue` are FIFO; read
17-Nov-2026). FACT (L377 to L399): one dispatcher gets the items and submits them in the order got. INTERPRETATION:
signals start in arrival order, but up to five run at once, so their status writes, reservations and placements can
finish in any order; re-put items (FIX-007, FIX-069) join the back of `signal_queue`. The processor itself does not keep
signals for the same symbol apart before the handoff; the receiver's in-flight claim does (P03; its limits in
P04-S058).

### 7.3 Retries (FIX-069) and the processor's own puts

P04-S052. FACT (L1486 to L1532, in `_admit_and_place`, after the handoff; A10 owns placement and A04 the rate-limit
exception; the A06 side is the put back into the intake queue; `git blame` gives every line to `536172c`, 12-Jul-2026,
"feat(v3): shared engine ... + portfolio allocator", in which the block sits in the extracted `_admit_and_place`
(docstring L1282 to L1288); FIX-069 itself is commit `397105d`, 16-May-2026, "FIX-069 lock travels with signal"): on `BrokerRateLimitError` from placement the worker
records an API failure; if `retry_count >= 3` it re-raises (status `PLACEMENT_FAILED`, L1233 to L1246); otherwise it
increments `retry_count`, sets `ac.requeued = True`, builds the dict of P04-S024 and calls
`self._queue.put(signal_dict, timeout=1.0)`. On success it releases the reservation and returns with the receiver's
claim kept (the `finally` skips the release, L1267); on `queue.Full` it sets `ac.requeued = False` and re-raises
(`PLACEMENT_FAILED`, claim released). HISTORICAL (L1489, L1521): the comments say "Max 3 retries (45s total, 15s each)"
and "reconciler will retry". Current external context (Python documentation, `queue`, `put` with a positive timeout:
"blocks at most timeout seconds and raises the Full exception if no free slot was available"). INTERPRETATION: the
code has no delay between attempts: the dict is put at once at the back of `signal_queue` and the dispatcher takes it
when it reaches it (at once if the queue is otherwise empty); each retry
runs the whole intake and A07 path again (status `PROCESSING`, kill switch, window, age, strategy lookup, screening and
on); there are at most four attempts; the retry count lives only in the dict; the worker can block for up to 1 s on the
put. Whether `BrokerRateLimitError` was raised in production is UNKNOWN / NOT ESTABLISHED.

P04-S053. FACT (L415 to L461; `git blame`: `31075d0` 12-May-2026 FIX-007, `d604c95` 15-May-2026 FIX-048, `1bf65ff`
13-Jun-2026 FIX-165f, `853a3a1` 10-Sep-2026, `056905b` 11-Sep-2026): only when `self._rate_limiter` is not `None`,
`_process_one_safe` calls `try_acquire("order")`; when it fails, the worker logs a WARNING and re-puts the same item
with
`put(signal_tuple, timeout=1.0)`, returning with the claim kept and no status change. If that put raises `queue.Full`,
it logs WARNING "REJECTED_QUEUE_FULL: <symbol> <scanner> - queue at capacity, abandoning signal <id>", writes
`update_signal_status(signal_id, "REJECTED", "QUEUE_FULL")` (bare `REJECTED`, reason `QUEUE_FULL`; errors swallowed),
emits a `P2_REJECT` evidence record built from the item itself (`_raw_signal_field`, L81 to L91), releases the claim
(L456 to L460) and returns. FACT (`main.py` L3575 to L3623): `main.py` passes no `rate_limiter`, so the default `None`
(L189) applies. INTERPRETATION: under `main.py` the whole block, the QUEUE_FULL reject and its evidence capture
included, never runs. HISTORICAL (commit `853a3a1`, message): the capture was added because the bare `REJECTED` status
escaped an earlier "REJECTED_" scan; the message says "Batch 1: NOT deployed to either VM". `853a3a1` and `056905b` are
later than the last recorded deployment (`686df1c` and `7d4970a`, 02-Sep-2026; Decision Register D-21); whether
production ran them is UNKNOWN / NOT ESTABLISHED. The A04 `try_acquire` wiring question is P05's.

P04-S054. Current external context (Python documentation, built-in types, mapping `d[key]`: "Raises a KeyError if key
is not in the map"; read 17-Nov-2026). FACT (L429): in that block the scanner name for the log line is taken as
`signal_tuple[1] if len(signal_tuple) > 1 else "unknown"`, outside any `try`. INTERPRETATION: for a FIX-069 dict
(length 6) this indexes key `1`, which a dict item does not have, so it raises `KeyError` before the status write, the
capture and the claim release; the exception leaves `_process_one_safe` (P04-S055). It needs a wired rate limiter, a
retry dict, an exhausted bucket and a full queue together, so it cannot occur under `main.py` (P04-S053).

### 7.4 Worker and dispatcher failure

P04-S055. Current external context (CPython 3.12 source `Lib/concurrent/futures/thread.py`, read 17-Nov-2026:
`_WorkItem.run` catches `BaseException` from the call and stores it with `future.set_exception`; `_worker` then
continues its loop and returns only when the interpreter or the executor is shutting down or the executor is gone).
FACT (L390, L397, L405 to L480, L876 to L895): the dispatcher discards each future; `_process_one_safe` catches
`Exception` only around `_process_one` (L465 to L477); `_process_one`'s own `try` (L895 to L1276) catches
`_PipelineReject` and `Exception` and has a `finally`. INTERPRETATION: (a) an exception inside `_process_one`'s `try`
is handled there (status, metrics, release); if a handler itself raises (for example a failing status write at L1201
or L1238), the `finally` still runs and `_process_one_safe` logs the error and tries `PLACEMENT_FAILED`; (b) an
exception from the unpacking at L876 to L887 is caught by `_process_one_safe` (logged, `PLACEMENT_FAILED` attempted),
but `_process_one`'s `finally` is not reached, so the claim is not released (P04-S026); (c) an exception raised in
`_process_one_safe` before its `try` (L408 to L461), or a `BaseException` that is not an `Exception`, is stored in the
discarded future: nothing logs it, no status is written and the claim is not released by the processor; (d) in no case
does the worker thread die; the executor keeps it.

P04-S056. Current external context (CPython 3.12 source, `submit`: raises `RuntimeError` "cannot schedule new futures
after shutdown" or "... after interpreter shutdown"; Python documentation, `threading`: an exception in `run()` goes to
`threading.excepthook`, which prints it on `sys.stderr`, and the thread stops being alive; read 17-Nov-2026). FACT
(L383 to L390, L244, L319, L346): in the dispatcher's main loop only `get` is inside a `try`; `submit` is not.
`_running` is changed only by `start()` and `stop()`. INTERPRETATION: `submit` can raise only after the executor or the
interpreter has begun shutting down; if the dispatcher thread ended for any reason, nothing would restart it,
`is_running()` would still return true, the queue would fill, and the receiver would then answer 503 and `QUEUE_FULL`
(P03). Whether the dispatcher ever ended early in production is UNKNOWN / NOT ESTABLISHED.

### 7.5 The `release_in_flight` calls

P04-S057. FACT (L456 to L460, L1248 to L1271, L1699 to L1703, L1733 to L1737; `main.py` L3612): the processor calls
the receiver's `release_in_flight(symbol)` in four places: (1) the FIX-007 `QUEUE_FULL` branch (never under `main.py`,
P04-S053); (2) the `finally` of `_process_one`, unless `requeued` (a successful FIX-069 re-put) or `handed_off` (the
allocator's enforce mode, P05) is true: this covers every exit from the `try`, including the screener's SKIPPED and
rejected returns (L1013, L1020), the retest divert (L1056), every `_PipelineReject`, the `TIMEOUT` return (L1484,
`requeued` false), success and every other exception; (3) `admit_prepared`, unless requeued; (4) `reject_prepared`
(the allocator paths, A18; P05). Each call is wrapped so that an error is logged and ignored. It is not called when the
FIX-007 branch re-puts an item (the claim "travels"), for exceptions that escape before L895 (P04-S026, P04-S055), or by
`stop()`. FACT (`signals/webhook_receiver.py` L934, L1047, L1102 to L1108): the receiver claims, and the processor
releases, the same key: the item's symbol after the alias; the receiver's `release_in_flight` pops that key
unconditionally under its lock.

P04-S058. INTERPRETATION (P04-S057; P01-S076, P01-S079): the release is keyed by symbol, not by signal. If the sweeper
had already evicted a signal's claim (with no heartbeat callback wired, every claim older than 60 s when a sweep runs is
evicted) and a second signal for the same symbol had since claimed it, the first signal's release removes the second
signal's claim while the second is still running, and a third signal for that symbol can then pass the claim. The
same 60 s bound applies to a FIX-069 retry whose claim is meant to travel with it. How long signals held their claims in
production is UNKNOWN / NOT ESTABLISHED. The claim and sweeper are P03's.

P04-S059. FACT (`signals/webhook_receiver.py` L1052 to L1057; `signals/signal_processor.py` L435 to L437): the same
condition, a full queue, is written two ways: the receiver sets the row's status to `QUEUE_FULL` (and later re-accepts
such a row on a retried webhook, P01-S041); the processor's unreachable FIX-007 branch writes `REJECTED` with the reason
`QUEUE_FULL`. The FIX-069 branch, on a full queue, gives `PLACEMENT_FAILED` (P04-S052).

## 8. Concurrency between workers up to the handoff

P04-S060. FACT (L199 to L298, L463 to L480, L675 to L681, L889 to L1006, L1193 to L1276): up to five workers run
`_process_one_safe` at once; the dispatcher alone calls `get` on the queue. Before the screener call the workers share:
`_active_workers` (guarded by `_active_lock`); `_rt_metrics` (guarded by `_rt_metrics_lock`); `_stats` (guarded by
`_stats_lock`, written on a reject and in the `finally`); `_last_expired_alert_ts` (read at L1224 and written at L1225
with no lock); the copied maps `_scan_webhook_map` and `_strategies` (read only after construction, no lock); and the
collaborators (state store, kill switch, market windows, shadow tracker, strategy-control function, governor, notifier,
evidence recorder), whose thread safety belongs to their owners. HISTORICAL (L23): "SP11 -- Thread-safety: all deps are
independently thread-safe". `_warm_zones` runs on the dispatcher thread, not on a worker (P04-S015).

P04-S061. Current external context (Python documentation, `threading`, page version 3.15.2: a `Lock` blocks other
acquirers until released; an `RLock` "may be acquired multiple times by the same thread"; read 17-Nov-2026).
INTERPRETATION (P04-S060): (a) the expired-alert rate limit is a read followed by a write without a lock, so two
workers rejecting `EXPIRED` at nearly the same moment can both pass the 60 s test and both send; (b) the map and
strategy reads are concurrent reads of dicts that no thread writes after construction (whether the configuration
objects inside them are changed elsewhere is A02's); (c) nothing in the processor serialises two signals for the same
symbol before the handoff; that rests on the receiver's claim (P03), with the limits of P04-S058; (d) the FIX-018
counter `_in_flight_count` (an `RLock`) is first touched after the handoff (L1302), so it plays no part in intake.

P04-S062. INTERPRETATION (P04-S004, P04-S013, P04-S050): with no per-signal deadline, a worker that blocks in a
collaborator (before or after the handoff) holds one of the five worker slots until the call returns; while all five are
held, further signals wait in the executor's work queue and age towards the 600 s limit (section 5), unseen by the
receiver's backpressure. How long any collaborator call took in production is UNKNOWN / NOT ESTABLISHED.

P04-S064. (added in the check) FACT (`signals/webhook_receiver.py` L963 to L980, L992 to L1011, L1049;
`signals/signal_processor.py` L377 to L390, L897): on the receiver's normal path the `signals` row is inserted with
status `QUEUED` before the item is put on the queue; on the M-S2 re-accept path the order is reversed: the item is put
first (L995) and the existing row is then set back to `QUEUED` by an unconditional
`UPDATE signals SET status = 'QUEUED' WHERE signal_id = ?` (L1002 to L1007). INTERPRETATION: on the re-accept path the
dispatcher can hand the item to a worker between L995 and that UPDATE; if the worker's `PROCESSING` write (L897), or a
quick final status such as `REJECTED_KILL_SWITCH`, is committed before the receiver's UPDATE, the row then reads
`QUEUED`, and it stays so if the worker writes nothing after that point. Whether this ordering ever occurred is UNKNOWN
/ NOT ESTABLISHED; the store's write behaviour is A03's and the re-accept path is P03's.

## 9. Python version and the library behaviour relied on

P04-S063. FACT (`requirements.txt` L1 to L15; `git ls-tree` of the repository root at `970aabf`; search for
`python3\.[0-9]+` in `deploy/`, `scripts/` and `ops/`; `deploy/systemd/trading-system.service` L18 to L19): no Python
version is pinned: `requirements.txt` lists packages only, the root holds no `pyproject.toml`, `setup.py`, `setup.cfg`,
`.python-version`, `runtime.txt` or `Pipfile`, the search finds no versioned interpreter name, and the declared unit
runs the virtual environment's `python`. The Python version on the legacy machines is UNKNOWN / NOT ESTABLISHED. The
processor's intake uses only the standard library (`queue`, `threading`, `concurrent.futures`, `datetime`, `time`).
Current external context (read 17-Nov-2026): the documentation pages read are the current ones (page version 3.15.2)
and the executor internals were read in the CPython 3.12 branch; the `concurrent.futures` page records that
`cancel_futures` was added in 3.9 and that idle worker threads are reused before new ones are started since 3.8.
INTERPRETATION: `stop()`'s `shutdown(wait=True, cancel_futures=False)` (L339) needs Python 3.9 or later; the
internals relied on in P04-S011, P04-S012, P04-S014, P04-S055 and P04-S056 (the unbounded work queue, lazy thread
creation, names, exception capture, exit joining) are as published for 3.12; whether the installed version behaves the
same is UNKNOWN / NOT ESTABLISHED.

## 10. Points the AUDIT may examine (neutral)

1. The receiver's backpressure and the depth figures read `signal_queue`, which the dispatcher empties into an
   unbounded, unmeasured work queue; nothing reports signals waiting for a worker (P04-S014, P04-S050, P04-S062).
2. `pipeline_timeout_sec: 30`, described as a "hard per-signal processing deadline", is validated but read by nothing;
   the processor has no per-signal deadline (P04-S004, P04-S062).
3. `stop()` waits without limit for every submitted signal to finish its run, while the docstring says "up to 5s";
   the drained signals still pass intake, screening, sizing and reservation before the pre-placement `SHUTDOWN` reject
   (L1398); intake itself refuses nothing because of the stop; a timed-out join can leave items behind or drop one
   already got (P04-S017 to P04-S019).
4. Items put after the drain's last read, or left behind by a timed-out join, are lost with the process and their rows
   stay `QUEUED`; nothing re-queues them at start-up (P04-S020).
5. Expiry: three different notions (receiver age, worker age, stored `expires_at`); no lower bound for future times;
   the worker checks age after the `PROCESSING` write and the window check; the resume paths have no age check and
   their comments speak of a 60 s expiry (P04-S036 to P04-S042).
6. The EXPIRED alert is limited to one per 60 s for the whole processor, repeats "age=" before a reason that already
   says "Signal age", and its rate limit is read and written without a lock (P04-S043, P04-S061).
7. The scanner name serves as the strategy in the receiver's row, while the processor resolves the strategy from the
   map; the map's "Validated at startup (P17, S10)" check is not run by any non-test caller (P04-S007, P04-S031,
   P04-S034).
8. Symbol handling at intake is limited to a strip and the alias map; the alias file is read from a path relative to
   the working directory, once, with failures shown only by one log line; no value is checked against instruments
   (P04-S045 to P04-S049).
9. FIX-069 retries have no delay, although the comment says "15s each", re-run the whole intake and A07 path, and keep
   a claim that the 60 s sweeper may evict (P04-S052, P04-S058).
10. The FIX-007 pre-check, its `QUEUE_FULL` reject and the 853a3a1 evidence capture do not run under `main.py`; the same
    branch would raise `KeyError` for a retry dict (P04-S053, P04-S054).
11. Exceptions raised outside the worker's `try` blocks are stored in discarded futures and never logged; a dispatcher
    that ended would not be noticed, and `is_running()` would stay true (P04-S055, P04-S056).
12. `release_in_flight` is keyed by symbol, so a late release can remove another signal's claim (P04-S057, P04-S058).
13. The boot-order assert adds no protection beyond statement order (P04-S021, P04-S022).
14. Texts that the code contradicts: the `triggered_at` "naive datetime" docstring (L874), the plain-dict map comments
    (L143, L166), "(default 60)" in the schema comment, "up to 5s per SP4", the test print about
    `pipeline_timeout_sec`, the "60s expiry" texts in the resume paths, "45s total, 15s each", and the scan-map schema
    comment "every name maps to a valid strategy YAML" with no validator behind it (P04-S004 to P04-S007, P04-S018,
    P04-S038, P04-S042, P04-S052).
15. A full queue is written as `QUEUE_FULL` by the receiver, as `REJECTED`/`QUEUE_FULL` by the unreachable FIX-007
    branch and as `PLACEMENT_FAILED` by the FIX-069 branch (P04-S059).
16. (added in the check) On the receiver's re-accept path the item is queued before its row is set back to `QUEUED`, so
    a fast worker's status can be overwritten by `QUEUED` (P04-S064).
17. (added in the check) `/metrics` reports `queue_depth` and `queue_capacity` as 0 under `main.py`'s wiring, so A20's
    backpressure check, with its own 0.9 factor, always passes; the receiver uses 0.80 and 0.60 (P04-S065, P04-S050).

## 11. UNKNOWN / NOT ESTABLISHED

- The effective values on the legacy machines of `signal_processor`, `signal_queue`, the scan map, the strategy files
  and the alias file (P04-S003, P04-S005, P04-S007, P04-S036, P04-S048).
- The Python version and library internals installed, and whether any run used optimisation (P04-S022, P04-S063).
- Whether any signal was processed, expired, retried or re-put in production; whether a backlog ever formed in the
  executor's work queue; how long collaborator calls took (P04-S039, P04-S050, P04-S052, P04-S062).
- Whether `stop()` ever ran long or timed out its join, whether the dispatcher ever ended early, and whether any
  queued signal was lost at a stop (P04-S018, P04-S020, P04-S056).
- Whether production ran the processor commits later than the last recorded deployment, `853a3a1` and `056905b`
  included (P04-S053).
- Whether the zone warmer was enabled, and whether its `enqueue` can block (A08) (P04-S015).
- The working directory of production runs, and so whether the alias file was found (P04-S047).
- How long signals held their receiver claims, and whether any claim was evicted and then released by the wrong
  signal (P04-S058).
- Whether any EXPIRED alert was sent (P04-S043); how the machine clock was kept (P04-S044).
- (added in the check) Whether production ran the `P2_REJECT` emission lines from `8d27fdb` and `056905b` (P04-S035);
  whether any signal was rejected `SHUTDOWN` at a stop (P04-S019); whether the re-accept ordering of P04-S064 ever
  overwrote a worker's status; what `/metrics` and the pre-flight check showed in production (P04-S065).

## 12. Draft questions about intent for Rama

1. Was the signal queue's capacity (300, with 503 at 80 %) meant to limit the signals waiting for a worker, or only
   those not yet taken by the dispatcher?
2. Was `pipeline_timeout_sec: 30` ("hard per-signal processing deadline") meant to be enforced by the processor?
3. At shutdown, what was intended for signals still waiting: run through the pipeline (the code runs them as far as
   the pre-placement shutdown check), discarded, or kept for later? Was "up to 5s" the intended limit for `stop()`?
4. From which moment was the 600 s expiry meant to be measured (Chartink's scan time, receipt, or queueing), and was it
   meant to be checked again when a worker starts, on each retry and on gate or retest resumption?
5. Should a `triggered_at` later than the current time be accepted?
6. In what forms did Chartink send symbols (case, exchange prefixes, series suffixes), and was intake meant to
   normalise them beyond the alias file? Was the alias file meant to follow the `--config` directory?
7. Was the FIX-069 retry meant to wait between attempts, as the comment's "15s each" says?
8. Was the FIX-007 rate-limiter pre-check, with its `QUEUE_FULL` reject, meant to be active in production?
9. Was the S10 check, that every scanner's strategy has a strategy file, meant to run at start-up?
10. Was the EXPIRED alert meant to be limited to one per minute across all symbols?
11. (added in the check) Were the `/metrics` fields `queue_depth` and `queue_capacity` meant to report the live signal
    queue, and which fill level was meant to count as backpressure (0.60, 0.80 or 0.90)?

## 13. Where the direction's questions are answered

Re-checked in the check against the A06 investigation direction (17-Nov-2026), section 4. The brief assigns P04
questions 14 (processor side), 15, 16, 17, 18, 19 and 21 (processor side); the rows marked "also touched" give P04's
contribution to other questions, which other parts own.

| Direction question (section 4) | Where in P04 | Other parts |
|---|---|---|
| 14 Concurrency boundaries; duplicate, lost or reordered signals; simultaneous requests, worker threads, shared state, retry paths (processor side) | P04-S020, P04-S051, P04-S052, P04-S055 to P04-S058, P04-S060 to P04-S062, P04-S064 | P03 (receiver side), P06 (throttle) |
| 15 The accepted request through `signal_processor.py` and every queue or intermediate representation to the exact handoff to A07 | P04-S001 to P04-S009, P04-S024 to P04-S035 (intake ends at the screener call, P04-S033) | P05 (exact handoff point and contract, later call-outs) |
| 16 Queue type, capacity, producer/consumer behaviour, backpressure, ordering, overflow/drop/reject, retries, worker lifecycle | P04-S008, P04-S010 to P04-S020, P04-S024, P04-S050 to P04-S056, P04-S059, P04-S065 | P03 (put side, 503 and `QUEUE_FULL`) |
| 17 Expiry: timestamp used, time-zone assumptions, age calculation, thresholds, stale and future timestamps, where expiry happens | P04-S005, P04-S036 to P04-S044 | P02-S055 to P02-S058, P02-S075 (receiver parse and check) |
| 18 Symbol and alias normalisation, the A05 instrument/alias boundary, every transformation, mapping source and failure mode | P04-S045 to P04-S049 | P01-S039, P01-S040, P02-S059; A05 (cache and alias tool) |
| 19 How strategy identity, scanner identity, symbol, price, timestamp and other fields survive or change across each handoff | P04-S024, P04-S030, P04-S034 | P01-S042, P01-S043 (receiver side); P05 (after the handoff) |
| 21 `main.py` construction, dependency injection, callbacks, start-up and shutdown order (processor side) | P04-S001, P04-S002, P04-S010 to P04-S023, P04-S057 | P01 (receiver side) |
| 13 (also touched) the queue threshold and capacity at different consumers | P04-S050, P04-S065 | P03 (owner of the receiver's thresholds), P08 (keys) |
| 20 (also touched) the process stopping between steps; status left on a row | P04-S019, P04-S020, P04-S064 | P05 (event creation and persistence), P03 |
| 22 (also touched) A06 lifecycle against A01's | P04-S019, P04-S021 to P04-S023 | P01 |
| 24 (also touched) the A04 rate limiter and the unwired `try_acquire` pre-check | P04-S002, P04-S053, P04-S054 | P05 (the A04 wiring question) |
| 25 (also touched) where A06 ends and A07 begins | P04-S033 | P05 (owner) |
| 26 to 28 (whole-topic audit inputs) | sections 10 to 12 (neutral points, UNKNOWN items, draft questions) | the AUDIT |

## 14. Check log

Checked by a separate read-only helper on 17-Nov-2026 against `970aabf` (`git show`, `git grep`, `git blame`,
`git log`; nothing run, imported or contacted), the project records under `algocore_system` (branch `main`) and the
official pages of section 1.4 (re-opened 17-Nov-2026). The first helper's text is kept in
`parts/drafts/A06_P04_PROCESSOR_INTAKE_AND_EXPIRY_DRAFT.md`.

- Statements checked: 63 (P04-S001 to P04-S063). Correct as written: 47. Corrected: 16. Withdrawn: 0. Added: 2
  (P04-S064, P04-S065). Total now: 65.
- Every cited line range, commit hash, date and subject was re-read; every external quotation was found on its page.

| ID | What changed | Why |
|---|---|---|
| P04-S004 | Added the document hits of the same search (`docs/CONFIG_GUIDE.md` L355; legacy integrity audit L3746 to L3749), as HISTORICAL | The search the statement cites also returns documents; one already records the key as unused |
| P04-S007 | Added the schema comment at `core/config_loader.py` L2344 (HISTORICAL), the absence of any validator on `ScanWebhookMapConfig` and `AppConfig`, and that strategies follow `--config` (`main.py` L3157) | Completeness: a second "validated" claim exists and is equally unbacked |
| P04-S011 | "up to five" made "up to `worker_count` (5 in the file)" | The count is a configuration value, not a constant |
| P04-S018 | Part (a) corrected: after `stop()` sets `_stop_event` (L333), a signal reaching L1398 is rejected `SHUTDOWN` before placement; added A01's record of `TimeoutStopSec=30` | The draft said drained signals run "placement where it passes those gates"; L1398 to L1405 refuses placement once the flag is set |
| P04-S019 | INTERPRETATION corrected; added the FACT (interface) of L1384 to L1405 (FIX-070, `31c6a62`) and the four read sites of `_stop_event` (L383, L1398, L2215, L2524) | The draft's "nothing in the processor refuses new entries because the process is stopping" is contradicted by L1398; what stays true is that no intake check refuses |
| P04-S022 | "straight-line code" replaced by the FACT that L3881 and L3968 sit at the top level of `_main_locked` (L2193), L3881 unconditional, the only exit between them `return 1` (L3899) | Precision: the span holds branches and a return, so "straight-line" was loose |
| P04-S024 | "three places" corrected to four: the receiver's M-S2 re-accept put (L993 to L995) was missing | Search for `\._queue\b`; P01-S042 already cites L993 |
| P04-S028 | Added the `if self._ks and ...` guard and the receiver's `is_active()` against the processor's `is_active("entry")` | The source shows both; the meaning of the argument is A13's |
| P04-S034 | `symbol` row: added the dispatcher's zone warming and the wrapper's log text; the claim release marked as later | Completeness of "use before L998" |
| P04-S035 | Added that the `P2_REJECT` emission lines (L1202 to L1211) are from `8d27fdb` and `056905b`, after the last recorded deployment (D-21), and the effect of a failing status write | D-21 asks Phase 1 to note post-deployment code topic by topic |
| P04-S041 | Hit list corrected (dashboard template L441, dashboard test fixture L54; other hits are unrelated token-expiry fields) and the schema comment marked HISTORICAL | The cited search returns more hits than listed |
| P04-S045 | `.lower()` hits completed (L1215, L1675, L2331, L2609: the reject label in release reasons); no `strip(` hit | The draft said "the only" hits were L532, L839 and L651 |
| P04-S047 | Added the contrast with the strategies' `config_dir` and the EOD route's use of the same map (L792) | Completeness of the alias consumer; L792 never reaches the queue |
| P04-S049 | Added A05's recorded fact that instrument-cache lookups are exact and case-sensitive (A05 RECONCILED TOPIC RECORD section 4.6) | Failure-mode context at the A05 boundary, cited, not studied |
| P04-S050 | Added the receiver's `X-Queue-Depth` and `X-Queue-Warning` headers (L741 to L744); scope narrowed to "every live queue measure in the two files"; pointer to P04-S065 | L741 was missing; the `/metrics` field of the same name is not a live measure |
| P04-S052 | "the dispatcher takes it on its next `get`" made "put at the back of `signal_queue` ... taken when the dispatcher reaches it" | FIFO order (P04-S051): earlier items go first |

Sections changed besides statements: header Status line; section 1.2 (direction file note); new section 1.4a (what the
check read); section 10 points 3, 4 and 14 corrected and points 16 and 17 added; section 11 one item added; section 12
question 3 reworded neutrally and question 11 added; section 13 rebuilt against the direction's section 4 wording,
with "also touched" rows for questions 13, 20, 22, 24, 25 and 26 to 28.

Statements added:
- P04-S064: on the receiver's re-accept path the item is queued before the row is set back to `QUEUED`, so a worker's
  status can be overwritten (INTERPRETATION; runtime UNKNOWN). Direction question 14, processor side.
- P04-S065: `/metrics` reports `queue_depth` and `queue_capacity` as 0 under `main.py`'s wiring, and A20's
  `WebhookBackpressureCheck` (factor 0.9) therefore always passes (FACT at the interface; INTERPRETATION). Direction
  questions 13 and 16; recorded at the interface only (A15, A20).

Not verified, and why:
- The P01, P02 and P03 statements that P04 cites were checked for wording only; their own sources are those parts'
  checks.
- Runtime behaviour (every item of section 11) has no surviving evidence in what was read and stays UNKNOWN / NOT
  ESTABLISHED.
- The CPython internals were read in the 3.12 branch only; the installed Python version is not pinned (P04-S063).

Security note: one `git show` of a commit header printed an identifier-bearing line (not reproduced). Two
false-positive filter replacements in printed code (a hash-algorithm name and a lint code) were ignored. No
credential file, overlay or effective setting was opened; no URL line of the scan map was read; G-19 is not cited.

- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P04-S033: "intake ends at this call ... P05, which fixes the exact handoff point" made neutral: P05-S031 leaves the handoff line open (OPEN FOR RAMA).
