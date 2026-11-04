# A01 evidence: workers, callback wiring and shutdown

**Status:** DRAFT — evidence for the A01 STUDY, for ChatGPT's review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04. Corrected, 2026-11-04: after an independent check of the statements against the code, in two passes.
**Purpose and scope:** Every thread, thread pool, server and child process started by or through `main.py`, with its creator, start condition, target, daemon flag, owner, stop and join behaviour and failure handling; the event-bus subscriptions and callbacks that `main.py` wires; the runtime wait and the signal handlers; and `_shutdown` step by step. It supports the STUDY, sections 7, 8 and 12 (Q17 to Q28 of ChatGPT's A01 direction). The internals of each worker belong to its owner topic and are not traced.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on 04-Nov-2026; nothing was run.

Conventions: every row is FACT for the lines it cites, unless a cell says INTERPRETATION. Lines are in `main.py` unless a path is given. Lines in other modules are pointers to the creation or stop site only. Whether any worker ran, and how long any stop took, is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2).

## 1. Threads, pools, servers and child processes

FACT (own AST scan of the 330 non-test `.py` files): 34 `threading.Thread(...)` constructions exist; all pass `daemon=True` except `capital/kill_switch.py` L1193 (`daemon=False`). FACT (grep): `main.py` has no `threading.Timer`, `sched`, `asyncio` or `subprocess`, calls `.join()` on no thread (every `.join(` in it is a `str.join`), and no non-test module registers an `atexit` hook or calls `os._exit`.

### 1.1 Created by `main.py` itself

| Worker | Created at | Start condition | Target | Daemon | Owner | Stop and join | Failure handling |
|---|---|---|---|---|---|---|---|
| "gate-release" pool: `ThreadPoolExecutor(max_workers=2, thread_name_prefix="gate-release")` | L865 to L867, at import | INTERPRETATION (CPython): worker threads start on the first `submit` | `_gate_release_worker` → `signal_processor.continue_from_gate(entry, release_ltp)` (L871 to L877), submitted at L887 when the release reason is `"PRICE_HIT"` | executor workers (INTERPRETATION: joined at interpreter exit by `concurrent.futures`, after queued tasks run) | A01; the work is A06's | never shut down by `main.py` | the worker logs exceptions (L874 to L877); the returned Future is discarded (L887) |
| "eod-pre-alert" | `_start_eod_pre_alert_thread`, L969 to L970; called at L4103 | the call is unconditional; the thread ends at once if `market_windows` is None or today is a holiday (L950 to L951), or if it is past 14:45 (L957 to L959) | `_run` (L945 to L967): sleep until 14:45, then `_fire_eod_pre_alert` (L900 to L928) once | True | A01 | checks `shutdown_event` between sleeps of up to 30 s (L962 to L965); not joined | `_fire_eod_pre_alert` catches everything (L927 to L928); the loop (L946 to L963) is outside any try |
| "market-open-margin-sync" | `_start_market_open_margin_sync_thread`, L1038 to L1039; called at L4113 | the call is unconditional; the thread returns on a holiday (L998 to L999) or if started at or after 09:15 (L1004 to L1007) | `_run` (L996 to L1036): sleep until 09:15, then `get_margins().net` → `fund_manager.sync_from_broker` (L1014 to L1016) and an INFO alert when the change exceeds 1.0 (L1022 to L1034) | True | A01; the re-sync is A09's | checks the event between sleeps of up to 30 s (L1008 to L1012); not joined | the sync and the alert are each in a try (L1013 to L1036); the wait loop is not |
| "eod-self-exit" | `_start_eod_self_exit_thread`, L1562 to L1563; called at L4135 | only when armed: not for `--interactive`, `--resume` or `TS_IGNORE_MARKET_WINDOW=1` (L4129 to L4134) | `_run` (L1391 to L1560): wait until `window_end` on the start date, then every `poll_interval_sec` (default 60, L1337; not overridden at L4135) call `_eod_self_exit_due` (L1230 to L1326); when due, INFO alert and `shutdown_event.set()` (L1525) | True | A01 | returns when it sees the event (L1401 to L1402, L1489, L1559) or right after setting it (L1525 to L1526); not joined | the decision function is fail-safe (L1270 to L1326); the other statements in `_run` are unguarded (the comment at L1540 to L1544 notes that an escaping exception ends the thread) |
| "webhook-server": `waitress.serve(webhook_receiver.app, host, port, threads=8, connection_limit=100)` | L3988 to L4000 | unconditional | the waitress server | True | A06; waitress is third-party | never stopped: `_shutdown` calls only `webhook_receiver.stop()`, which sets the 503 flag and the sweeper stop flag (`signals/webhook_receiver.py` L1166 to L1176); not joined | detected only by the self-check after a fixed 2 s sleep (L4003 to L4054), which degrades the boot; nothing restarts the server |
| "eod-scheduler" | L4094 to L4100 | unconditional | `eod.start_polling(poll_interval_sec=...)`, which starts the daemon "eod_squareoff_poll" and returns (`orders/eod_squareoff.py` L290 to L312) | True | A12 | INTERPRETATION: a short-lived launcher. The poller it starts loops `while True` with no stop condition (`orders/eod_squareoff.py` L300 to L306); `eod` is not passed to `_shutdown` | the poller logs exceptions from `check_and_fire` (L302 to L305) |

### 1.2 Started through calls that `main.py` makes (the threads live in the owner modules)

| Worker (thread name) | Creation site (owner module) | Started from `main.py` | Start condition | Daemon | Owner | Stopped by `_shutdown`; join (pointer) |
|---|---|---|---|---|---|---|
| "f_boot_self_test" | `alerts/mis_squareoff_notifier.py` L250 to L252 | L3355 `run_boot_self_test(background=True)` | always | True | A14 | no |
| "mis_f_prepass_poll" | `alerts/mis_squareoff_notifier.py` L274 to L275 | L3357 `start_polling()` | always | True | A14 | no |
| "f_notify_<channel>", one per notification | `alerts/mis_squareoff_notifier.py` L396 to L399 (joined by the notifier with its own timeout) | through the notifier | per notification | True | A14 | no |
| "mis_autosquareoff_poll" | `orders/mis_autosquareoff.py` L410 to L411 | L3380 `start_polling()` | always | True | A12 | no |
| "in_flight_sweeper" | `signals/webhook_receiver.py` L217 to L220, in the constructor | constructed at L3407 | always | True | A06 | its stop flag is set at L1686; not joined |
| "sr-detector" | `sr_detector/detector.py` L114 | L3504 | `_v1_on` | True | A08 | L1695 to L1699; join with the default 2 s (`sr_detector/detector.py` L118, L126) |
| "market-regime" | `regime/runner.py` L50 | L3536 | `_regime_on` | True | A18 | L1701 to L1705; default 2 s (L54, L58) |
| "allocator-window" | `allocation/portfolio_allocator.py` L109 to L110 | L3651 | allocator mode not "off" | True | A18 | L1707 to L1711; join 10 s (L125) |
| "v3-chain" | `v3_chain/runner.py` L83 | L3694 | `_v3_chain_on` | True | A18 | L1713 to L1717; default 3 s (L87, L95) |
| "pb01-capture" | `v3_chain/watchlist_capture.py` L90 | L3748 | `_watchlist_on` | True | A18 | L1725 to L1729; default 3 s (L94, L102) |
| "pb01-entry" | `v3_chain/pb01_entry.py` L121 | L3749 | `_watchlist_on` | True | A18 | L1720 to L1724; default 2 s (L127, L131) |
| "sr-zone-warmer" | `sr_detector/zone_warmer.py` L67 | L3796 or L3816 | `_v2_on`, or `_struct_exit_on` | True | A08 | L1742 to L1746; default 2 s (L71, L79) |
| "sr-retest-monitor" | `screening/retest_monitor.py` L79 | L3797 | `_v2_on` with the zone infrastructure | True | A08 | L1731 to L1735; default 2 s (L83, L87) |
| structure-exit manager (no thread found in its module by grep) | `orders/structure_exit_manager.py` | L3832 | `_struct_exit_on` | - | A11 | L1737 to L1741 (the comment says it unsubscribes from the candle feed) |
| "candle-store-timer" | `data/candle_store.py` L113 to L116 | L3922 | always | True | A05 | L1791 to L1794 |
| "live-feed-consumer", "live-feed-consumer-restarted", "live-feed-watchdog" | `data/live_feed.py` L142 to L145, L648 to L651, L687 to L690 | L3947 `connect()`, which in live starts the consumer and the watchdog (`data/live_feed.py` L136 to L151, L681 to L692); the restarted consumer is started elsewhere in the module (L648 to L651) | live only (in paper `connect()` returns at once, `data/live_feed.py` L138 to L140) | True | A05 | `disconnect()` at L1787 to L1790; the watchdog is joined with a timeout of its check interval plus 1 s, 11 s by default (`data/live_feed.py` L50, L163 to L166; `main.py` does not set the interval, L2927 to L2938) |
| "order-monitor" | `broker/order_monitor.py` L508 to L510 | L3960 | always | True | A04 | L1773 to L1776; join 5 s (L520) |
| "order_reconciler_poll" | `orders/order_reconciler.py` L446 to L448 | L3961 `start()`, which first runs, synchronously, the CNC overnight check, the GTT reconcile and a second `reconcile_once()` (`orders/order_reconciler.py` L428 to L442) | always | True | A12 | L1761 to L1764; join 5 s (L461) |
| "broker_clock_skew_probe" | `broker/clock_skew_probe.py` L78 to L80 | L3963 | live only | True | A04 | L1777 to L1781; join 2 s (L92) |
| "token-monitor" | `broker/token_monitor.py` L103 to L105 | L3964 | always (the comment says it is a no-op in paper) | True | A04 | L1782 to L1786; join 5 s (L118) |
| signal-processor dispatcher thread and executor | `signals/signal_processor.py` L310 (executor), L314 (thread) | L3974 | always | thread True | A06 | L1689 to L1692; dispatcher join 10 s (L336), then the executor is shut down with `wait=True` and no time bound (L339), then the screener's step executor (L342 to L344) |
| entry-gate poll thread and executor | `screening/entry_gate.py` L163 (executor), L167 (thread) | L3975 `start()`, which first restores `gate_state` from the database (`screening/entry_gate.py` L155 to L160) | always | thread True | A07 | L1747 to L1750; poll join 5 s (L247); the executor is shut down without waiting, then a fixed `time.sleep(3.0)` (L254 to L255) |
| "smart-tgt-modify" executor | `orders/smart_tgt_manager.py` L145 to L146, in the constructor (`async_modify=True`, `main.py` L2982) | constructed at L2973; `start()` L3976, which restores `smart_tgt_state` and makes one startup quote check per restored row (`orders/smart_tgt_manager.py` L170 to L204) | always | executor | A11 | L1752 to L1755; an in-flight flush of up to 5 s (L217, L480 to L492), then `shutdown(wait=False, cancel_futures=True)` (L219) |
| "tgt-retry-manager" | `orders/tgt_retry_manager.py` L109 to L111 | L3977 | always | True | A11 | L1756 to L1760; join 5 s (L126) |
| "step-exec" executor | `screening/step_executor.py` L70, L76, in the constructor | constructed at L3234 | always | executor | A07 | not passed to `_shutdown`; the signal processor's `stop()` asks the screener to shut it down (`signals/signal_processor.py` L342 to L344) |
| "healthcheck-server" (waitress, `threads=1`, loopback host by default) | `scripts/healthcheck_server.py` L297 to L326 | L4074 | always | True | A15 | no; the returned thread handle is discarded |
| pre-flight on-demand child processes | `scripts/preflight/startup_hook.py` L58 to L96 (`subprocess.Popen` at L67) | L4089 | only past-due phases (A20) | child processes | A20 | not tracked by `main.py` |
| "ks-hard-kill-flatten" | `capital/kill_switch.py` L1193 to L1196, `daemon=False` | started by the kill switch on a hard kill, not by `main.py` | on hard kill | **False** | A13 | drained at L1643 to L1656 with `drain_flatten(timeout=15.0)` (`capital/kill_switch.py` L1260 to L1306) |
| event-bus async executors, one per async subscription (thread prefix `ev_<EventType>`) | `core/events.py` L290 to L296; subscribed by `orders/slippage_recorder.py` L113 to L114 | constructed at L3095 | inside a try (L3093 to L3101) | executor | A01 (bus); A11 (handlers) | no: `EventBus.shutdown()` (`core/events.py` L347 to L351) is never called outside tests |

- FACT: `RateLimiter(app_config.broker_limits, shutdown_event=_shutdown_event)` (L2348) is not a thread; while waiting for a token it watches the event and raises `RateLimitAbortedError` once the event is set (`broker/rate_limiter.py` L236 to L244; A04).
- FACT: `_shutdown_event` (L116) is set at L1525 (self-exit), L1573 (signal handler) and L1629 (`_shutdown`), awaited at L4249, and never cleared.

## 2. Event subscriptions and callback wiring

### 2.1 Bus mechanics (`core/events.py`, A01)

- FACT: `subscribe` raises `TypeError` unless the event type is an `Event` subclass (L286 to L289). With `async_dispatch=True` it creates a dedicated single-worker executor for that subscription (L290 to L296); otherwise it appends the handler to the synchronous list (L297 to L298). There is no lock and no de-duplication.
- FACT: `publish` dispatches on the exact type (`type(event)`, L315). It first submits every async handler without waiting (L317 to L319), then calls every synchronous handler in registration order in the publisher's thread, logging each failure (L321 to L336). If any synchronous handler failed, it raises `EventDispatchError` to the publisher (L338 to L345). Async handler failures are only logged (L354 to L365). Publishing with no subscriber does nothing.

### 2.2 Subscriptions

| Event | Handler | Subscribed at | Mode | Publishers (pointers) |
|---|---|---|---|---|
| `KillSwitchActivated` | `_log_kill_switch_event` (L1586 to L1592): one CRITICAL log line | L3847 | sync | `capital/kill_switch.py` L1059 (wrapped) |
| `CapitalDriftDetected` | `drift_handler.on_drift` (`CapitalDriftHandler`, built at L3853 to L3857) | L3858 | sync | `capital/fund_manager.py` L1489 and L1512; `orders/order_reconciler.py` L2568, L3914, L4048 |
| `OrderStatusChanged` | `OrderManager` (`orders/order_manager.py` L144) | constructor at L3046 | sync | `broker/order_monitor.py` L1334 |
| `OrderFilled`, `OrderPartiallyTerminated`, `OrderStatusChanged` | `OrderPlacer` (`orders/order_placer.py` L693, L697, L700) | constructor at L3061 | sync | `broker/order_monitor.py` L999, L1037, L1334 |
| `PositionClosed`, `EodSquareoffComplete` | `ShadowTracker` (`orders/shadow_tracker.py` L194 to L195) | constructor at L2946 | sync | `orders/order_placer.py` L2473; `orders/order_reconciler.py` L1407; `orders/cnc_gtt_monitor.py` L598; `orders/eod_squareoff.py` L514 |
| `OrderFilled`, `PositionClosed` | `SlippageRecorder` (`orders/slippage_recorder.py` L113 to L114) | constructor at L3095 | async | as above |
| `PositionClosed` | the adapter (`broker/zerodha_adapter.py` L477) | constructor at L2383 | sync | paper only (L476) |

- FACT: `main.py` itself subscribes exactly two handlers (grep for `.subscribe(`: L3847 and L3858). The component subscriptions happen earlier, inside their constructors. Because synchronous handlers run in registration order, `OrderManager` handles `OrderStatusChanged` before `OrderPlacer` does.
- FACT: the kill switch exists on the same bus from L2243, and its state can change at L2260, L2265 and L2291 before L3847. INTERPRETATION: those transitions reach no `main.py` handler, because a publish with no subscriber does nothing.
- FACT: the comment at L3850 to L3852 says only "fund_manager-sourced events" escalate; `capital/drift_handler.py` L66 to L70 lists three escalating sources (`fund_manager`, `fund_manager_self_check`, `fund_manager_bucket_overflow`).

### 2.3 Callbacks wired by `main.py`

| Callback (factory lines) | Wired at | Receiver (owner) | Invoked by (pointer) | What it does when it fires | Guarded |
|---|---|---|---|---|---|
| `_on_critical_failure(source, reason)` (`_make_critical_failure_cb`, L657 to L685) | L2930 to L2932, a lambda that builds a new closure on every call | `LiveFeedManager` (A05) | `data/live_feed.py` L422 to L424 ("feed gap"), L477 to L480 ("KiteTicker max reconnect ... exhausted"), L774 to L777 ("tick-age watchdog") | CRITICAL log; if `"BrokerAuthError"` is in `reason`, `_mark_auth_failed()` (L666 to L667); `kill_switch.soft_kill(reason=f"{source}: {reason}", triggered_by="auto")` (L669 to L671); CRITICAL Telegram | `soft_kill` not wrapped; the send is wrapped |
| `_on_force_close()` (`_make_force_close_cb`, L688 to L724) | L3010 | `OrderMonitor` (A04) | `broker/order_monitor.py` L861 | CRITICAL log; `soft_kill(reason="circuit_breaker_force_close_15:15", ...)` (L698 to L701); WARNING Telegram naming "15:17" | `soft_kill` not wrapped |
| `_on_api_failure(reason)` (`_make_api_failure_hard_kill_cb`, L727 to L752) | L3006 | `OrderMonitor` (A04) | `broker/order_monitor.py` L648 to L652, after three consecutive `BrokerAuthError`, reason `"BrokerAuthError x<n> -- monitor stopping"`; the monitor then sets its own stop event (L653) | CRITICAL log; `kill_switch.hard_kill(...)` (L735 to L741); CRITICAL Telegram "3 consecutive broker API failures detected". It does not call `_mark_auth_failed()` | `hard_kill` and the send are wrapped |
| `_on_daily_loss_breach()` (`_make_daily_loss_cb`, L756 to L817) | L2729 to L2734, with `_eod_ref` filled at L3321 | `FundManager` (A09) | `capital/fund_manager.py` L1356 to L1361, inside `release_used` under its lock (L1261) | CRITICAL log and Telegram; `eod.fire_now(...)` when `eod` is wired, else WARNING (L794 to L805); `soft_kill(reason="daily_loss_limit_breached", ...)` (L811 to L814) | `soft_kill` not wrapped |
| `_on_orphan(order_id, reason)` (`_make_orphan_cb`, L820 to L843) | L3005 | `OrderMonitor` (A04) | `broker/order_monitor.py` L874 and L1126, called with (internal order id, broker order id) | CRITICAL log; `soft_kill(reason=f"orphan_order:{order_id}:{reason}", ...)`; CRITICAL Telegram | `soft_kill` not wrapped |
| `_on_gate_release(entry, reason)` (`_make_gate_release_cb`, L870 to L893) | L3843 | `EntryGate` (A07) | `screening/entry_gate.py` L531 to L532, inside a try | on `"PRICE_HIT"`, submits `continue_from_gate` to `_gate_release_pool` (L880 to L887); otherwise INFO | the worker logs its own exceptions |
| `_on_critical_skew(skew, reason)` (`_init_time_authority`, L360 to L378) | L2254 | `core/time_authority.py` (A01) | `record_broker_skew` (`core/time_authority.py` L243 to L244), called only by `broker/clock_skew_probe.py` L138 to L141 | CRITICAL log; `soft_kill(reason="clock_skew_critical: ...", triggered_by="time_authority")` | no |
| `on_expiry` lambda | L3390 to L3392 | `TokenMonitor` (A04) | the token monitor | `soft_kill(reason="token_expired", triggered_by="token_monitor")` | no |
| reconnect lambda | L2992 to L2994 | `LiveFeedManager` (A05) | the live feed | `candle_store.mark_reconnect(ts)`, then `smart_tgt.on_reconnect(ts)` | no |
| `_tick_dispatcher(ticks)` | L2964 to L2971 | `LiveFeedManager` (A05) | the live feed | per tick: `candle_store.on_tick(...)` and `shadow_tracker.on_tick(t)` | no per-tick try |
| `_persist_candle(candle)` | L3927 to L3944 | `CandleStore` (A05) | candle close | `store.insert_candle(...)` | its own try, DEBUG log |
| `_daemon_liveness()` | L4060 to L4071, passed at L4081 | health server (A15) | `/health` | liveness of the order monitor, reconciler and EOD poller (gating) and the live-feed connection (reported only) | each item returns False on an exception |

- FACT: no handler or callback above sets `_shutdown_event`, calls `_shutdown`, `sys.exit` or `os._exit`; `capital/kill_switch.py` contains no shutdown or exit call (grep). Each callback runs in the thread of the component that invokes it, while the main thread stays blocked at L4249.
- FACT: late binding: the kill switch receives its notifier and adapter only at L2648 and L2653; the daily-loss callback reaches `eod` only after L3321.
- FACT: the table holds the twelve principal callbacks. `main.py` also passes smaller callables and providers: the MIS notifier's send lambdas (L3346 to L3350) and the MIS square-off's `critical_sink` (L3377 to L3378); the self-exit's `flatten_in_progress_fn` and `strategy_intent_fn` (L4144, L4148 to L4150); `_market_hours_fn` (L3108, passed at L3119 and L3137); `sector_lookup_fn` (L2908) and `resolve_product` (L3293); `in_flight_release_fn` (L3612) and the PB-01 and retest `on_confirm` callbacks (L3745, L3786); and the health server's metrics and TGT-retry providers (L4076, L4080).

## 3. The runtime wait and the signal handlers

- FACT: the runtime loop is the single call `_shutdown_event.wait()` at L4249 (marker "Runtime loop (MAIN13)", L4248): no timeout, no cadence, no body, and no try around it. When it returns, `_shutdown(...)` is called with 24 keyword arguments (L4252 to L4277) and `_main_locked` returns 0 (L4278).
- FACT: `_install_signal_handlers` (L1570 to L1579) installs one handler for SIGINT (L1575, unguarded) and SIGTERM (L1576 to L1579; `OSError` and `ValueError` are passed). The handler logs INFO "Signal <n> received -- initiating shutdown" and sets the event (L1571 to L1573). It is called only at L3958.
- INTERPRETATION (CPython and POSIX semantics): before L3958, SIGINT raises `KeyboardInterrupt` in the main thread, which the guard does not catch (L4288 to L4293); `main()`'s `finally` releases the lock and the interpreter exits with a traceback; SIGTERM keeps its default action and ends the process at once. Signals with no handler keep their defaults. After L3958, a signal that arrives while startup is still running only sets the event, and startup normally runs to the end (the STARTUP marker and "System Active" included); the wait then returns at once and `_shutdown` runs. Once the event is set, a rate-limited broker call that has to wait raises `RateLimitAbortedError` (`broker/rate_limiter.py` L236 to L244). FACT: the later startup broker calls found catch it: in `order_reconciler.start()`, the CNC check's `get_positions` (`orders/order_reconciler.py` L755 to L761, caught at L757), the `cnc_gtt_monitor.reconcile()` call (L435 to L439, caught at L438) and the reconcile (L652 to L654); and the smart-TGT startup quote check (`orders/smart_tgt_manager.py` L863 to L867). INTERPRETATION: their work can then be skipped in effect while the boot completes; an abort that an owner does not catch ends the boot with exit 1 (A04, A11 and A12 to confirm). A repeated signal during `_shutdown` only sets the event again.

## 4. `_shutdown` (L1599 to L1831), step by step

All arguments are keyword-only (L1600). The docstring says "Reverse-order shutdown (MAIN15)" (L1627). The "Maximum wait" column gives the fixed join or sleep found in the owner module (section 1.2); a dash means none was found or it was not traced.

| # | Lines | Step | Owner | Maximum wait (pointer) | Error handling |
|---|---|---|---|---|---|
| 1 | L1629 to L1630 | `_shutdown_event.set()` (the FIX-060 comment: "so rate limiter aborts immediately"); INFO "Shutdown initiated" | A01 | - | none |
| 2 | L1643 to L1656 | if `kill_switch` is given: `drain_flatten(timeout=flatten_drain_timeout_sec)` (default 15.0, L1624); True → INFO; False → CRITICAL "SHUTDOWN WITH FLATTEN STILL RUNNING ... POSITIONS MAY REMAIN OPEN AT THE BROKER" | A13 | 15 s | CRITICAL, continue |
| 3 | L1662 to L1675 | `effect_telemetry.emit_census(..., webhook_day_count=<COUNT(*) FROM webhook_audit for today>)` | A15 | DB read | ERROR, continue |
| 4 | L1678 to L1679 | if `_broker_auth_failed`: `_invalidate_token()` (renames the token file; L138 to L165) | A13 / A04 | - | none around the step; inside, only the rename is guarded (L158 to L165), not the existence test and its warning (L152 to L156) |
| 5 | L1684 to L1688 | `webhook_receiver.stop()`: 503 flag and sweeper stop flag | A06 | - | ERROR, continue |
| 6 | L1689 to L1692 | `signal_proc.stop()` | A06 | 10 s join, then an executor shutdown with no time bound (`signals/signal_processor.py` L336, L339) | ERROR, continue |
| 7 | L1695 to L1699 | `sr_detector.stop()` if not None | A08 | 2 s default | ERROR, continue |
| 8 | L1701 to L1705 | `market_regime_runner.stop()` if not None | A18 | 2 s default | ERROR, continue |
| 9 | L1707 to L1711 | `portfolio_allocator.stop()` if not None | A18 | 10 s | ERROR, continue |
| 10 | L1713 to L1717 | `v3_chain.stop()` (the argument carries `v3_chain_runner`) if not None | A18 | 3 s default | ERROR, continue |
| 11 | L1720 to L1729 | `pb01_entry_stage.stop()`, then `pb01_capture_worker.stop()`, each if not None | A18 | 2 s and 3 s defaults | ERROR, continue, each |
| 12 | L1731 to L1735 | `retest_monitor.stop()` if not None | A08 | 2 s default | ERROR, continue |
| 13 | L1737 to L1741 | `structure_exit_manager.stop()` if not None | A11 | - | ERROR, continue |
| 14 | L1742 to L1746 | `zone_warmer.stop()` if not None | A08 | 2 s default | ERROR, continue |
| 15 | L1747 to L1750 | `entry_gate.stop()` | A07 | 5 s join plus a fixed 3 s sleep | ERROR, continue |
| 16 | L1752 to L1755 | `smart_tgt.stop()` (the comment at L1751 about Flask refers to the webhook server, which is never stopped) | A11 | up to 5 s (the in-flight flush, `orders/smart_tgt_manager.py` L217, L480 to L492), then a shutdown without waiting (L219) | ERROR, continue |
| 17 | L1756 to L1760 | `tgt_retry_manager.stop()` if not None | A11 | 5 s | ERROR, continue |
| 18 | L1761 to L1764 | `order_reconciler.stop()` | A12 | 5 s | ERROR, continue |
| 19 | L1767 to L1772 | `n = order_monitor.cancel_all_entry_orders()`; INFO if n > 0 (the comment says SL, TGT and EOD legs are kept) | A04 | broker calls | ERROR, continue |
| 20 | L1773 to L1776 | `order_monitor.stop()` | A04 | 5 s | ERROR, continue |
| 21 | L1777 to L1781 | `clock_skew_probe.stop()` if not None (live) | A04 | 2 s | ERROR, continue |
| 22 | L1782 to L1786 | `token_monitor.stop()` if not None | A04 | 5 s | ERROR, continue |
| 23 | L1787 to L1790 | `live_feed.disconnect()` | A05 | up to 11 s in live (the watchdog join, default interval 10 s plus 1; `data/live_feed.py` L50, L163 to L166) | ERROR, continue |
| 24 | L1791 to L1794 | `candle_store.stop()` | A05 | - | ERROR, continue |
| 25 | L1795 to L1804 | INFO Telegram "[mode] System Stopping" with version and HH:MM IST | A14 | network | ERROR, continue |
| 26 | L1805 to L1812 | `now_iso = time_authority.now_ist_iso()` (unguarded); `store.insert_system_event(event_type="SHUTDOWN", timestamp=now_iso)` | A03 | DB | the insert only: ERROR, continue |
| 27 | L1815 to L1825 | `store.checkpoint_wal()` (PASSIVE); INFO with its counters | A03 | DB | WARNING, continue |
| 28 | L1827 to L1830 | `store.close()` | A03 | - | ERROR, continue |
| 29 | L1831 | INFO "Shutdown complete" | A01 | - | none |

- FACT (sum of the maximum waits in the table): the steps that always run in live (2, 6, 15, 16, 17, 18, 20, 21, 22 and 23) add up to 71 s of fixed maximum joins, waits and sleeps (15 + 10 + 5 + 3 + 5 + 5 + 5 + 5 + 2 + 5 + 11), before the signal processor's unbounded executor shutdown, the broker calls of step 19, the send of step 25 and the optional workers' joins (up to 10 s for the allocator and 2 to 3 s each for the others). These are maxima: a join returns as soon as its thread ends, `drain_flatten` returns at once when no flatten is running (`capital/kill_switch.py` L1282 to L1285), and only the entry gate's 3 s sleep is fixed (`screening/entry_gate.py` L255). The repository unit file sets `TimeoutStopSec=30` (`deploy/systemd/trading-system.service` L25; A17, file only). How long the stops actually took is UNKNOWN / NOT ESTABLISHED.
- FACT: not passed to `_shutdown`, and so never stopped by it: `eod` (and its `while True` poller), `mis_notifier`, `mis_autosq`, `fund_manager`, `order_placer`, `broker_adapter`, `event_bus`, `drift_handler`, `shadow_tracker`, `step_executor`, `rate_limiter`, the "webhook-server", "eod-scheduler" and "healthcheck-server" threads and `_gate_release_pool`. The three helper threads of section 1.1 leave on their own within up to 30 s of the event being set; none is joined.
- FACT: the comment at L1814 says "WAL checkpoint after all threads joined"; `main.py` joins no thread. The only joins in this sequence are inside the subsystems' own `stop()` methods.
- FACT: there is no re-entrancy guard. In non-test code `_shutdown` is called once (L4252); the tests call it directly. INTERPRETATION: a second call repeats every step, each inside its try except steps 1, 4, 26 (`now_ist_iso`) and 29, and so cancels entry orders and sends "System Stopping" again; whether each subsystem `stop()` is idempotent is for its owner topic.

### 4.1 Does the shutdown order reverse the startup order?

Startup order of the start calls: MIS pollers (L3355, L3357, L3380); optional S&R and V3 workers (L3504 to L3832); `candle_store.start()` (L3922); `live_feed.connect()` (L3947); signal handlers (L3958); order monitor (L3960); reconciler (L3961); clock-skew probe (L3963); token monitor (L3964); signal processor (L3974); entry gate (L3975); smart TGT (L3976); TGT retry (L3977); webhook server (L4000); health server (L4074); EOD scheduler (L4100); pre-alert (L4103); margin sync (L4113); self-exit (L4135).

| Aspect | FACT |
|---|---|
| Overall | the core chain is roughly reversed: intake stops first (webhook flag L1686, signal processor L1690); the order monitor, live feed and candle store stop late; the store closes last |
| Signal processor and entry gate | started processor then gate (L3974 < L3975; comment L3972 to L3973: the gate may call `continue_from_gate()` at once on release); stopped processor first (L1690) and gate much later (L1748): not reversed |
| Entry gate, smart TGT, TGT retry | started at L3975, L3976, L3977; stopped at L1748, L1753, L1758: the same order, not reversed |
| Order monitor, reconciler, probe, token monitor | started at L3960, L3961, L3963, L3964; stopped at L1774, L1762, L1779, L1784: only the reconciler and order-monitor pair is reversed |
| S&R and V3 workers | started first, before Phase 0f; stopped early, just after the signal processor. INTERPRETATION: they consume signals and candles, so stopping them early is coherent |
| Exit management and fills | smart TGT and TGT retry stop (L1753, L1758) before the order monitor (L1774) and the live feed (L1788); the order placer's fill handlers stay subscribed (it is not stopped) |
| Pending entries | the reconciler stops (L1762) before `cancel_all_entry_orders()` (L1768) |

## 5. Every route to the end of the process

| Trigger | Path | `_shutdown` runs? | Result |
|---|---|---|---|
| EOD self-exit (the normal daily end) | the thread sets the event (L1525); the wait returns (L4249); L4252 | yes | `return 0` (L4278), exit 0 |
| SIGINT or SIGTERM after L3958, including the unit's `KillSignal=SIGINT` on a stop | handler (L1573); L4249; L4252 | yes | exit 0 |
| SIGINT before L3958 | `KeyboardInterrupt` (section 3) | no | INTERPRETATION: traceback; the exit status reflects the signal |
| SIGTERM before L3958, or SIGKILL at any time (INTERPRETATION: including systemd's after `TimeoutStopSec`) | OS default action | no | the process is killed |
| An exception in the main thread during startup or Phase 0h | propagates (startup trace, conventions) | no | exit 1 or 2 |
| An exception inside `_shutdown`, outside its guards (steps 1, 4, 26, 29) | propagates | partly done | exit 1 or 2 |
| An exception in a worker thread at runtime | that thread ends | no | the process keeps running |
| A soft or hard kill (any callback in section 2.3, or the drift handler) | the event is not set (section 2.3) | no | the process keeps running |
| A handled startup return (exit 3, 4, 5, 6, 9, or 1 at L3899) | return before L4249 | no | that exit code; most of these returns close the store first |
| A failed webhook self-check | degrade (L4006 to L4054) | no | the process keeps running |

After `_shutdown` returns: FACT: L4278 returns 0; `main()`'s `finally` calls `release_instance_lock()` (L2189 to L2190; `utils/instance_lock.py` L220 to L238), and `sys.exit(0)` follows (L4287). INTERPRETATION (CPython): interpreter shutdown then joins any non-daemon thread (the "ks-hard-kill-flatten" worker, if it outlived the 15 s drain), joins the executor workers after running their queued tasks (`_gate_release_pool`, the event-bus async executors, and any executor its owner did not shut down), and abandons the daemon threads. FACT: `main.py` never calls `shutdown_logging()` (`core/logger.py` L461 to L472), and the file log handlers sit behind a queue listener (L431 to L445); INTERPRETATION: records still queued at exit may not reach the log files.

The SHUTDOWN `system_events` row (L1807 to L1810) is what the next boot on the same day looks for (`utils/startup_checks.py` L309 to L329, WARM). FACT: every route above on which `_shutdown` does not reach step 26 leaves no SHUTDOWN row for that run. INTERPRETATION: the next same-day boot is classified CRASH, unless an earlier run that day wrote one or today's EOD square-off log is COMPLETE (WARM; `utils/startup_checks.py` L330 to L365), a kill state forces HALT (a HARD_KILL, or a SOFT_KILL of the same day; L243 to L286), or the session row does not yet carry today's date (COLD; L290 to L307).
