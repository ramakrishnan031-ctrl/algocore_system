# A03 evidence: SQL outside the state store: runtime modules

**Status:** DRAFT — evidence for the A03 STUDY, for ChatGPT's review
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P06a, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5).
**Purpose and scope:** The SQL issued outside the state-store methods by the 30 runtime modules (`main.py` included), with the table-by-table writers and readers. Statement IDs `P06a-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

- P06a-S001 — FACT (helper pass): before any work, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline) and `git status --short` returned no lines.
- P06a-S002 — FACT: after the work, the same two commands were run again; the result is recorded in P06a-S003.
- P06a-S003 — FACT: after-check result: HEAD `970aabf3c78d777d9d34549e021f7c8e756c7bdb`; `git status --short` returned no lines (0 lines). Nothing was written to the clone.
- P06a-S004 — Scope: the 30 files of the coordinator's file list for this part (line counts at the baseline in brackets): `broker/order_monitor.py` (1351), `capital/fund_manager.py` (2583), `capital/kill_switch.py` (2151), `capital/performance_allocator.py` (174), `capital/shadow_engine.py` (271), `capital/strategy_governor.py` (196), `core/config_snapshotter.py` (217), `main.py` (4293), `ops/control_tower/aggregator.py` (323), `ops/control_tower/db.py` (146), `ops/control_tower/disk.py` (57), `ops/control_tower/freshness.py` (119), `ops/control_tower/health.py` (41), `ops/control_tower/size_logger.py` (130), `ops/control_tower/status.py` (51), `orders/breakeven_manager.py` (419), `orders/cnc_gtt_monitor.py` (753), `orders/entry_engine.py` (119), `orders/eod_squareoff.py` (1887), `orders/full_entry_engine.py` (236), `orders/mis_autosquareoff.py` (1324), `orders/order_manager.py` (769), `orders/order_placer.py` (4706), `orders/order_reconciler.py` (4621), `orders/shadow_tracker.py` (896), `orders/sl_breach_monitor.py` (295), `orders/slippage_recorder.py` (299), `orders/structure_exit_manager.py` (672), `signals/signal_processor.py` (2703), `signals/webhook_receiver.py` (1207).
- P06a-S005 — Method: every file was parsed in full as TEXT with Python's `ast` module by a text-parsing script kept outside the clone (lists every call of `.execute`, `.executemany`, `.executescript`, `.fetch_one`, `.fetch_all`, `.transaction`, `.fetchone`, `.fetchall`, with its line span, enclosing function, receiver and literal SQL text, and whether it sits inside a `with ... .transaction() as cur` block); enclosing functions of other lines were resolved with a second text-parsing script kept outside the clone (also `ast`, text only). In addition, `grep` for SQL keywords (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, PRAGMA, BEGIN, COMMIT, ROLLBACK, `.commit()`, `sqlite3`) over all 30 files, and `grep`/`git grep` for callers. The code around every hit was then read (windows cited per row). No legacy code, test or SQL was run or imported.
- P06a-S006 — Context read outside the 30 files, for semantics only (owned by other parts): `core/state_store.py` L172 to L249 and L506 to L586 (P01), L2474 to L2480 (P05); `core/db_connect.py` L93 to L135 (P01); `core/schema.sql` L42 to L116, L280 to L300, L468 to L501, L565 to L572, L581 to L599, L1405 to L1471, L1491 to L1502 (P02a/P02b); `utils/startup_checks.py` L581 to L625 (A01); `core/effect_telemetry.py` L255 to L263 (A15); `ops/control_tower/cli.py` L39 to L60 and `ops/control_tower/runner.py` L58 to L70 (P01 for their connection set-up); `reports/daily_trade_review.py` L347 to L351 (P06b). Project documents read for handoff IDs only: A01 STUDY/AUDIT (B-14, S-10, C6, C33) and A02 AUDIT (V-11, V-45).
- P06a-S007 — Tests (`tests/`, `ops_dashboard/tests/`) were not traced or cited. Paper-side branches are marked where they split and not traced.
- P06a-S264 — FACT (checker pass, as its file states): before its work `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no lines; after its work the same two commands returned the same HEAD and no lines. It wrote nothing to the clone and ran or imported no legacy code, test or SQL; it used its own text-only `ast` scanner and a coverage matcher (both kept outside the clone) and found no SQL statement in the 30 files missing from the draft.
- P06a-S265 — FACT (corrector pass): before the work `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no lines; after the work the same two commands returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and no lines. The corrector re-read the code at every finding's cited lines (and `core/events.py` L300 to L330 and `broker/order_monitor.py` L1334 for the event route of P06a-S261) with `sed`/`grep` only; nothing was written to the clone and no legacy code, test or SQL was run or imported. No scratch files were written.
- P06a-S266 — Process disclosures from the checker pass (neutral): the checker wrote its first scan output for a moment to the system temporary folder and moved it at once into its work folder (no copy left there). It also noted a scan-output file in the system temporary folder, timestamped seconds after the helper's scan script, that it did not create and did not open; the helper's draft does not mention it.

## 1. Connection and transaction model the scoped files rely on (pointer: part P01)

| ID | Item | What the code does | Label |
|---|---|---|---|
| P06a-S008 | `StateStore.transaction` | `core/state_store.py` L506 to L543: takes the calling thread's connection (`_get_conn`, L524), runs `BEGIN IMMEDIATE` (L531), yields a cursor, `COMMIT` on normal exit (L533); on ANY exception runs `ROLLBACK` (L534 to L540, a failing ROLLBACK is swallowed) and re-raises (L541). Docstring L517 to L519: nesting not supported. | FACT |
| P06a-S009 | `StateStore.execute` | L549 to L562: `conn.execute(sql, params)` on the calling thread's connection, no BEGIN/COMMIT. The connection is opened with `isolation_level=None` (L234). | FACT |
| P06a-S010 | autocommit reading of `execute` | With `isolation_level=None`, Python's `sqlite3` issues no implicit BEGIN, so a single statement through `StateStore.execute` commits on its own. | INTERPRETATION (Python `sqlite3` semantics) |
| P06a-S011 | `fetch_one` / `fetch_all` | L564 to L586: `execute` + `fetchone`/`fetchall`, cursor closed in `finally`; no transaction. | FACT |
| P06a-S012 | per-thread connection | `_get_conn` L215 to L225 keeps one connection per thread (`threading.local`, L192); every StateStore call in this part therefore runs on the connection of the thread that makes it. | FACT |
| P06a-S013 | `db_connect.connect` (Control Tower) | `core/db_connect.py` L93 to L111: `sqlite3.connect(str(main_db_path), timeout=timeout, **kwargs)` (L107), forwarding any extra keyword arguments; the three Control Tower openers (aggregator L197, size_logger L83, cli L48) pass none, so no `isolation_level` is set; `PRAGMA busy_timeout = 30000` (L108), analytics ATTACH only if `attach` is true (L109 to L110). | FACT |
| P06a-S014 | implicit transactions on Control Tower connections | Python's default (legacy) transaction control opens an implicit transaction before INSERT/UPDATE/DELETE/REPLACE, not before DDL or SELECT; changes persist only on `conn.commit()`; `conn.close()` without commit discards them. | INTERPRETATION (Python `sqlite3` semantics; Python version at runtime UNKNOWN) |
| P06a-S015 | Control Tower openers | `ops/control_tower/aggregator.py` L197 (`attach=True`), `ops/control_tower/size_logger.py` L83 (`attach=False`), `ops/control_tower/cli.py` L48 (`attach=False`; not in this part's list, caller of `db.py` functions). Default path argument: `data_store/trading_system.db` under the project root (aggregator L300, size_logger L93). Connection set-up details: see part P01. | FACT |
| P06a-S016 | split of the 30 files | 19 files issue SQL through the shared `StateStore` (sections 2.1 to 2.19); 7 Control Tower files issue SQL through a connection of their own (sections 2.20 to 2.26; `db.py`, `disk.py`, `freshness.py`, `health.py` and `status.py` only receive the connection opened by `aggregator.py` or `cli.py`); 4 files issue no SQL (section 2.27): 19 + 7 + 4 = 30. | FACT |

- P06a-S017 — FACT: the 19 StateStore files are `capital/fund_manager.py`, `capital/kill_switch.py`, `capital/performance_allocator.py`, `capital/shadow_engine.py`, `capital/strategy_governor.py`, `core/config_snapshotter.py`, `main.py`, `orders/breakeven_manager.py`, `orders/cnc_gtt_monitor.py`, `orders/eod_squareoff.py`, `orders/order_manager.py`, `orders/order_placer.py`, `orders/order_reconciler.py`, `orders/shadow_tracker.py`, `orders/sl_breach_monitor.py`, `orders/slippage_recorder.py`, `orders/structure_exit_manager.py`, `signals/signal_processor.py`, `signals/webhook_receiver.py`; the 4 files without SQL are `broker/order_monitor.py`, `orders/entry_engine.py`, `orders/full_entry_engine.py`, `orders/mis_autosquareoff.py`.

## 2. Statement inventory by file

Column key: Txn = inside `StateStore.transaction()` (BEGIN IMMEDIATE ... COMMIT) or not; Conn = connection used; Error route = what the code does if the statement raises. All StateStore rows use the shared StateStore on the calling thread's connection (P06a-S012). No statement in sections 2.1 to 2.19 targets the analytics database.

### 2.1 `main.py` (owner A01; failure callbacks A13; config snapshot wiring A02)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S018 | L619 to L633 | `_write_session` | `session` | INSERT OR REPLACE | writes `id`=1, `session_date`, `account_id` (literal `'default'`), `broker` (`mode` if `mode == "paper"` else literal `"zerodha"`), `mode` (`mode.upper()`), `trade_type` (literal `'INTRADAY'`), `last_config_hash`, `session_start`, `last_updated` (both = `now_iso`) | yes (L622) | none local; exception propagates to the caller |
| P06a-S019 | L2308 to L2314 | `_main_locked` (call 1 of `_write_session`) | `session` | via S018 | `session_date=today_iso` (L2266), `mode=args.mode`, `config_hash=json.dumps(app_config.file_hashes)` (L2312), `now_iso=time_authority.now_ist_iso()` | yes | no try around the call; the exception leaves `_main_locked`, passes `main()` L2187 to L2190 (`try`/`finally` that releases the instance lock) and reaches the outer guard at L4285 to L4293 (`except TradingSystemError` L4288, `except Exception` L4291; part P03's) |
| P06a-S020 | L4174 to L4180 | `_main_locked` (call 2, Phase 0h) | `session` | via S018 | same expressions as call 1 (`json.dumps(app_config.file_hashes)` at L4178); `now_iso` is the value also used for the STARTUP system event (L4167 to L4173) | yes | no try around the call |
| P06a-S021 | L900 to L928 | `_fire_eod_pre_alert` | `trades` | SELECT | reads `symbol, direction, qty_filled, entry_actual_price` WHERE `status = 'OPEN' AND qty_filled > 0` ORDER BY `symbol` | no | try L902 / except L927: logs error, no alert |
| P06a-S022 | L1666 to L1671 | `_shutdown` (lambda passed as `webhook_day_count` to `effect_telemetry.emit_census`) | `webhook_audit` | SELECT | `COUNT(*) WHERE date = ?` (`date` is the generated column, `core/schema.sql` L592) | no | invoked inside `emit_census` under try/except that returns "derive-failed" (`core/effect_telemetry.py` L259 to L263); outer try/except L1662 / L1674 |

- P06a-S023 — FACT: `_fire_eod_pre_alert` is called at L966 from `_start_eod_pre_alert_thread` (L931 onward), so its SELECT runs on that thread's own StateStore connection (P06a-S012). The thread's schedule is A01's/A16's.
- P06a-S024 — Not SQL in `main.py`: the other `store.*` calls are typed state-store methods (`insert_system_event`, `get_session_row`, `close`, `checkpoint_wal`, `count_active_positions`, `get_active_positions_with_identity`, `insert_candle` (analytics: see P07), `cancel_stale_paper_orders` (paper, not traced)): see parts P04/P05. `StateStore(...)` construction at L2233: see parts P01/P03.

### 2.2 `core/config_snapshotter.py` (owner A02)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S025 | L189 to L193 | `snapshot_config` | `config_snapshots` | SELECT | reads `snapshot_id` WHERE `snapshot_date = ? AND config_hash = ?` LIMIT 1 | no | none local; propagates to `main.py` L2613 (logged "non-fatal") |
| P06a-S026 | L202 to L211 | `snapshot_config` | `config_snapshots` | INSERT | writes `snapshot_date, snapshot_ts, account_id, mode, trade_type, config_hash, config_json`; returns `cur.lastrowid` (L211) | yes (L202) | none local; ROLLBACK by `transaction()`; propagates to `main.py` L2613 |

- P06a-S027 — FACT: the existence check (S025) runs outside the transaction and before it; the INSERT (S026) is a separate transaction (L202). `core/schema.sql` L1491 to L1502 defines `config_snapshots` with `snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT` and only a non-unique index `idx_config_snapshots_date` on `snapshot_date`; there is no UNIQUE constraint on `(snapshot_date, config_hash)`.
- P06a-S028 — FACT: the only call is `main.py` L2602 to L2614 inside `try/except Exception` that logs "config_snapshotter: snapshot failed (non-fatal)"; values passed: `snapshot_date=today_iso`, `snapshot_ts=time_authority.now_ist_iso()`, `account_id=selected_account.account_id`, `mode="PAPER" if is_paper else "LIVE"` (L2609; the paper split is in the value only), `trade_type=app_config.system.trade_type`.
- P06a-S029 — FACT: `git grep` over non-test `*.py` finds no other INSERT, UPDATE or DELETE on `config_snapshots`. Readers (pointers): `reports/daily_trade_review.py` L350 to L351 (latest row of a date), L1194 to L1197, L1780 to L1782, L2091 to L2092; `ops_dashboard/backend/readers/config_reader.py` L33, L231 (via `db_reader.latest_config_snapshot`); `ops_dashboard/backend/readers/db_reader.py` L631, L638, L1554, L1564, L3340 to L3342, L3440, L4202 (see part P06b; owner A15); `ops_dashboard/backend/services/audit.py` (pointer only, owner A15).
- P06a-S030 — HISTORICAL: the `account_id` parameter docstring (L168) and the schema column comment give an example account identifier (`<ACCOUNT_ID>`; not reproduced).

### 2.3 `signals/webhook_receiver.py` (owner A06)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S031 | L963 to L980 | `_process_signal` | `signals` | INSERT | writes `signal_id, symbol, scanner, strategy` (= `scanner_name`, L975), `triggered_at, received_at, expires_at, status` (`'QUEUED'`, L977), `fingerprint, fingerprint_date` (= `today_iso`), `trigger_price, webhook_payload` | yes (L964) | `sqlite3.IntegrityError` → S032 route (L981); any other exception → claims released, CRITICAL log, returns `STORE_ERROR` (L1016 to L1044) |
| P06a-S032 | L987 to L991 | `_process_signal` (IntegrityError branch) | `signals` | SELECT | reads `signal_id, status` WHERE `fingerprint = ? AND fingerprint_date = ?` | no | no try of its own inside the `except` block; an exception here leaves `_process_signal` |
| P06a-S033 | L1002 to L1011 | `_process_signal` (re-queue of a `QUEUE_FULL` row) | `signals` | UPDATE | `status = 'QUEUED'` WHERE `signal_id = ?` | yes (L1003) | try/except logs error, still returns `ACCEPTED` (L1008 to L1013) |
| P06a-S034 | L1048 to L1068 | `_process_signal` (queue full after the INSERT) | `signals` | UPDATE | `status = 'QUEUE_FULL'` WHERE `signal_id = ?` | yes (L1053) | try/except logs error (L1058 to L1059); returns `QUEUE_FULL` |
| P06a-S035 | L1126 to L1154 | `_write_audit` | `webhook_audit` | INSERT | writes `ts, scanner_name, source_ip, payload_size_bytes, response_code, signals_accepted, signals_rejected, duration_ms` (`date` is generated, schema L592) | yes (L1138) | try/except logs error (L1153 to L1154) |

- P06a-S036 — FACT: the database-level duplicate guard relied on at L981 is the unique index `idx_signals_fingerprint_today` on `signals(fingerprint, fingerprint_date)` (`core/schema.sql` L82 to L83); `'QUEUED'` and `'QUEUE_FULL'` are in the `status` CHECK set (schema L60 to L63).
- P06a-S037 — FACT, order of steps: the INSERT with `status='QUEUED'` commits (L964 to L980) before the in-memory queue push (L1049); on the re-queue route the queue push (L995) happens before the `QUEUED` flip (L1003 to L1007).
- P06a-S038 — Not SQL in this file beyond the rows above. FACT: `webhook_payload` receives the request body after `_sanitize_payload_for_storage` (L688 to L690; method at L857), passed as `webhook_payload=stored_payload` (L722). HISTORICAL: the comment at L681 to L687 says this removes a secret-bearing URL field before storage; the schema column comment (L76) calls the column the raw JSON. Content not examined.

### 2.4 `signals/signal_processor.py` (owner A06)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S039 | L761 to L767 | `_enforce_strategy_position_cap` | `trades` | SELECT | reads `SUM(CASE status IN ('OPEN','PARTIAL'))` AS `open_partial`, `SUM(CASE status IN ('OPEN','PARTIAL','PENDING_FILL'))` AS `active` WHERE `strategy = ?` | no | no local try; propagates to the three callers (L1311, L2141, L2477) |

- P06a-S040 — FACT: the call at L1311 is made inside `with self._fm.portfolio_lock` (L1307); the lock is an in-process lock, not a database lock.
- P06a-S041 — Not SQL: the other store calls are typed methods (`update_signal_status` 26 call sites, `count_trades_today`, `count_settled_trades_today`, `count_executed_trades_today_for_symbol_direction`): see parts P04/P05.

### 2.5 `capital/fund_manager.py` (owner A09)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S042 | L1918 to L1936 | `_today_release_used_pnl_rows` | `fm_ledger` | SELECT | reads `pnl_delta, bucket` WHERE `entry_type = 'RELEASE_USED' AND ts >= ? AND pnl_delta != 0` ORDER BY `ledger_id` | no | no local try; callers `rehydrate_from_open_trades` L1864 and `today_realized_pnl_carryover` L1964 have no try around it |
| P06a-S043 | L2012 to L2022 | `_replay_open_trade` | `fm_ledger` | SELECT | reads `ledger_id, ts, entry_type, amount, bucket, balance_before, balance_after, signal_id, reservation_id, margin_delta, pnl_delta` WHERE `reservation_id = ?` ORDER BY `ledger_id` | no | no local try; caller `rehydrate_from_open_trades` L1790 |
| P06a-S044 | L2226 to L2235 | `_commit_exists` | `fm_ledger` | SELECT | `1` WHERE `reservation_id = ? AND entry_type = 'COMMIT'` LIMIT 1 | no | no local try; caller `commit_adopted_entry` L1105 |
| P06a-S045 | L2237 to L2266 | `_restore_reserve_from_ledger` | `fm_ledger` | SELECT | reads `ts, amount, bucket, signal_id` WHERE `reservation_id = ? AND entry_type = 'RESERVE'` ORDER BY `ledger_id` LIMIT 1 | no | no local try; callers L1112 (`commit_adopted_entry`), L1156 (`restore_adopted_reservation`), L1199 (`release_adopted_reservation`) |
| P06a-S046 | L2520 to L2575 | `_write_ledger` | `fm_ledger` | INSERT | writes `ts, entry_type, amount, bucket, balance_before, balance_after, signal_id, reservation_id, reason, session_id` (= `self._session_id`), `direction, trade_id, margin_delta, pnl_delta, costs` | yes (L2552) | `except Exception`: `log_exception` then re-raise (L2572 to L2574); the telemetry counter runs only after commit (L2569 to L2571) |

- P06a-S047 — FACT: `_write_ledger` is called from nine methods: `initialize` L468, `reserve` L584, `release` L658, `release_slm_buffer` L727, `top_up_reservation` L838, `commit_to_used` L954, `release_used` L1300, `sync_from_broker` L1438, `reset_daily_pnl` L1702. In `reserve` the ledger row is written (L584 to L595) before the in-memory mutation `_apply_reserve` (L600 onward), as the BL-5 comment L579 to L580 states.
- P06a-S048 — HISTORICAL: module docstring FM10 (L24 to L29) says "Every mutation writes to fm_ledger (state_store) in same txn" and describes write-ahead replay on crash. FACT: `_write_ledger` opens its own transaction holding only the one INSERT (L2552 to L2568).
- P06a-S049 — Not SQL: other store calls are typed methods (`get_all_open_trades`, `get_daily_realized_net_pnl`, `get_entry_commit_margin`, `get_reservation_id_for_signal`): see parts P04/P05.

### 2.6 `capital/kill_switch.py` (owner A13)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S050 | L431 to L441 | `_count_open_positions` | `trades` | SELECT | `COUNT(*)` WHERE `status IN ('OPEN','PARTIAL','PENDING_FILL')` | no | except → logs error, returns 1 ("assuming non-zero") |
| P06a-S051 | L934 to L1002 | `_persist_state` | `kill_switch_state` | INSERT OR REPLACE | writes `id`=1, `state, reason, triggered_at` (`ts.isoformat()`), `triggered_by` | yes (L963) | no `except`; `finally` only logs elapsed time (L977 to L1002); the exception propagates |
| P06a-S052 | L1004 to L1047 (SQL L1011 to L1014) | `_load_state_from_store` | `kill_switch_state` | SELECT | reads `state, reason, triggered_at, triggered_by` WHERE `id = 1` | no | except → logs error, starts INACTIVE (L1015 to L1020) |
| P06a-S053 | L1521 to L1557 | `_mark_trade_exiting` | `trades` | UPDATE | `status = 'EXITING', updated_at` WHERE `trade_id = ? AND status IN ('OPEN','PARTIAL','PENDING_FILL')`; `rowcount == 0` logged as no-op | yes (L1537) | except → CRITICAL log, swallowed |
| P06a-S054 | L1559 to L1596 | `_fetch_co_entry` | `orders` | SELECT | reads `order_id, variety` WHERE `trade_id = ? AND leg IN ('ENTRY','CO')` LIMIT 1 | no | except → warning, returns `("", "")` |
| P06a-S055 | L1606 to L1617 | `_cancel_trade_resting_exits` | `orders` | SELECT | reads `order_id, leg` WHERE `trade_id = ? AND leg IN ('SL','TGT') AND status NOT IN ('CANCELLED','FAILED','EXPIRED','COMPLETE')` | no | except → warning, return |
| P06a-S056 | L1649 to L1661 | `_cancel_trade_resting_exits` (per row, after the broker cancel) | `orders` | UPDATE | `status = 'CANCELLED', updated_at` WHERE `order_id = ? AND status NOT IN ('CANCELLED','FAILED','EXPIRED','COMPLETE')` | yes (L1649) | `except Exception: pass` |
| P06a-S057 | L1697 to L1710 | `_exit_all_trades_indestructible` | `trades`, `orders` | SELECT | reads `t.trade_id, t.symbol, t.qty_filled, t.direction` and a correlated sub-select `o.product` (leg `ENTRY` or `CO`, LIMIT 1) WHERE `t.status IN ('OPEN','PARTIAL','PENDING_FILL')` | no | except → CRITICAL log, returns `CancellationReport(attempted=0, succeeded=0, failed=["fetch_failed"])` |

- P06a-S058 — FACT: the live-status set and the terminal-order set are module constants `_FLATTEN_LIVE_TRADE_STATUSES` (L93) and `_FLATTEN_TERMINAL_ORDER_STATUSES` (L98), interpolated as `?` placeholders into S053, S055, S056 and S057.
- P06a-S059 — FACT: `_persist_state` callers: L349 (stale auto-clear), L416 (scheduled auto-clear), L590 (`soft_kill`), L727 (`hard_kill`, inside `with self._lock` from L721), L778 (`resume`, inside `with self._lock` from L768). In each, the in-memory state assignments follow the call (e.g. L593 to L596, L730 to L733, L780 to L783), so they are not reached if the persist raises.
- P06a-S060 — HISTORICAL: the `_persist_state` docstring (L945 to L958) says the call runs inside `self._lock`, inherits `busy_timeout = 30000`, and records that no SQLITE_BUSY was seen in logs against 25 real kills (a claim about runtime; see section 8).
- P06a-S061 — FACT: `_mark_trade_exiting` callers: L1814, L1874, L1898, L2064, L2127; `_cancel_trade_resting_exits` callers: L1805, L1858. Other store call: `insert_system_event` (L470; typed method, part P05).

### 2.7 `capital/strategy_governor.py` (owner A09)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S062 | L91 to L102 | `_get_today_pnl` | `trades` | SELECT | `COALESCE(SUM(gross_pnl), 0.0)` WHERE `strategy = ? AND status IN ('CLOSED','CLOSED_MANUAL') AND updated_at LIKE ?` (today's IST date + `%`) | no | caller try L67 to L72: logs, returns "not paused" (fail-open comment L72) |
| P06a-S063 | L104 to L126 | `_get_avg_daily_loss` | `trades` | SELECT | `AVG(daily_pnl)` over losing past days, day key `SUBSTR(updated_at, 1, 10)`, window `updated_at >= ?` and day `< today` | no | same caller try as S062 |

- P06a-S064 — FACT: `StrategyGovernor` is constructed in `main.py` L856 (A01 wiring).

### 2.8 `capital/performance_allocator.py` (owner A09; A18 cites)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S065 | L130 to L157 | `_fetch_stats` | `trades` | SELECT | per `strategy`: `COUNT(*)`, wins (`net_pnl > 0`), `COUNT(DISTINCT DATE(exit_time))` WHERE `status IN ('CLOSED','CLOSED_MANUAL') AND net_pnl IS NOT NULL AND DATE(created_at) >= ? AND strategy IN (...)` GROUP BY `strategy` | no | except → error log, returns `{}` |

- P06a-S066 — FACT: a `git grep` over non-test `*.py` finds no construction of `PerformanceAllocator` other than its own docstring example (L41).

### 2.9 `capital/shadow_engine.py` (owner A09; A18 cites)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S067 | L182 to L189 | `get_daily_summary` | `shadow_trades` | SELECT | `*` WHERE `date = ?` ORDER BY `created_at` | no | no local try |
| P06a-S068 | L229 to L249 | `_persist_shadow_trade` | `shadow_trades` | INSERT | writes `shadow_trade_id, date, signal_id, symbol, strategy, direction, entry_price, qty, sys_sl, sys_tgt, live_trade_id, live_status, created_at` | yes (L233) | except → error log, swallowed |
| P06a-S069 | L251 to L271 | `_update_shadow_trade_exit` | `shadow_trades` | UPDATE | `simulated_exit_price, simulated_exit_reason, simulated_pnl` WHERE `shadow_trade_id = ?` | yes (L254) | except → error log, swallowed |

- P06a-S070 — FACT: a `git grep` over non-test `*.py` finds no construction or import of `ShadowEngine` outside its own file.

### 2.10 `orders/order_manager.py` (owner A10)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S071 | L208 to L262 | `create_trade` | `trades` | INSERT | 35 columns: `trade_id, signal_id, symbol, direction, strategy, sector, qty_planned, qty_filled` (0), `entry_target_price, entry_actual_price` (NULL), `sl_initial, tgt_initial, margin_reserved, risk_amount, created_at, updated_at, status` (`'PENDING_FILL'`), `entry_mode` (`'FULL'`), `order_protocol, recovered_flag` (0), `reservation_id, mode, tolerance_fraction_used, tolerance_source, tier_multiplier_mode, tier_weight_applied, perf_weight_applied, flat_value_rs_used, qty_by_risk, qty_by_capital, qty_by_concentration, qty_by_flat, binding_constraint, actual_position_value_rs, tgt_risk_reward_applied` | yes (L211) | none local; propagates |
| P06a-S072 | L272 to L287 | `record_exits_verification` | `trades` | UPDATE | `exits_verified, exits_verify_detail, updated_at` WHERE `trade_id = ?` | yes (L282) | none local (docstring L280 to L281 says "best-effort"); propagates |
| P06a-S073 | L289 to L337 | `insert_order` | `orders` | INSERT | `order_id` (= `broker_order_id`), `trade_id, leg, leg_index, transaction_type, order_type, product, variety, qty_requested, price, trigger_price, status` (`'PENDING'`), `qty_filled` (0), `avg_fill_price` (NULL), `placed_at, updated_at` | yes (L309) | none local; propagates |
| P06a-S074 | L339 to L391 | `insert_orders_atomic` | `orders` | INSERT (one per spec, loop) | same columns as S073, all rows in ONE transaction | yes (L361) | none local; whole batch rolled back and the exception propagates (docstring L347 to L349) |
| P06a-S075 | L393 to L432 | `record_entry_fill` | `trades` | UPDATE | `status = 'OPEN', entry_actual_price, entry_time, qty_filled, updated_at` WHERE `trade_id = ?` (no status condition) | yes (L409) | none local; then calls S076 |
| P06a-S076 | L434 to L506 | `_compute_and_store_latency` | `trades`, `signals`, `orders` | SELECT x3, UPDATE | reads `trades.signal_id`, `signals.received_at`, `orders.placed_at` (leg `ENTRY`); writes `signal_to_order_ms, order_to_fill_ms, total_latency_ms` WHERE `trade_id = ?` | reads no; UPDATE yes (L487), only when at least one latency value is not None (L486) | whole method in try; except → DEBUG log only (L505 to L506) |
| P06a-S077 | L508 to L707 | `close_trade` | `trades` | SELECT (via `get_trade`, L550) then UPDATE | writes `status = 'CLOSED', exit_time, exit_price, exit_reason, gross_pnl, charges, net_pnl, cost_brokerage, cost_stt, cost_exchange_txn, cost_sebi, cost_gst, cost_stamp_duty, closure_source, exit_mechanism, updated_at` WHERE `trade_id = ? AND status IN ('OPEN','PARTIAL','EXITING')`; `rowcount == 1` decides (L674) | UPDATE yes (L640) | validation errors raise `ValueError` before the write (L545, L552, L606, L630, L635); `rowcount == 0` → warning + `ValueError` (L675 onward); success → read-back via `get_trade` (L707) |
| P06a-S078 | L709 to L716 | `update_trade_status` | `trades` | UPDATE | `status, updated_at` WHERE `trade_id = ?` (no status condition) | yes (L712) | none local; propagates |
| P06a-S079 | L718 to L724 | `link_signal_trade` | `signals` | UPDATE | `trade_id` WHERE `signal_id = ?` | yes (L720) | none local; propagates |
| P06a-S080 | L726 to L752 | `update_order_status` | `orders` | UPDATE | `status, qty_filled, avg_fill_price, rejection_reason` (COALESCE with old), `filled_at` (COALESCE with old), `updated_at` WHERE `order_id = ?` | yes (L737) | none local; propagates |
| P06a-S081 | L756 to L761 | `get_trade` | `trades` | SELECT | `*` WHERE `trade_id = ?` | no | none local |
| P06a-S082 | L763 to L769 | `get_orders_for_trade` | `orders` | SELECT | `*` WHERE `trade_id = ?` ORDER BY `placed_at` | no | none local |

- P06a-S083 — FACT: `close_trade`'s WHERE excludes terminal from-states; `core/schema.sql` L291 to L299 defines `trg_trades_terminal_status_guard` (BEFORE UPDATE OF `status` on `trades`, RAISE(ABORT) when the old status is CLOSED, CLOSED_MANUAL, FAILED, CANCELLED or REJECTED* and the new status differs). S075 and S078 write `status` with no status condition.
- P06a-S084 — INTERPRETATION (SQLite and S008): if the trigger aborts an UPDATE inside `transaction()`, the `IntegrityError` reaches the context manager, which rolls back the whole transaction and re-raises.
- P06a-S085 — FACT, callers of the OrderManager writers (owner of each caller in brackets): `create_trade` `orders/order_placer.py` L996 (`place`) [A10]; `link_signal_trade` L1028 (`place`) [A10]; `update_trade_status` L1065, L1449 (`place`), L2005 (`_on_order_status_changed`), L4448 (`_handle_placement_failure`) [A10]; `record_entry_fill` L1867 (`_on_order_partially_terminated`), L2057 (`_on_order_status_changed`), L2139 (`_handle_entry_fill`) [A10]; `close_trade` L2370 (`_handle_exit_fill`) [A10]; `record_exits_verification` L2547 (`_finalize_cnc_gtt`), L2970 (`_place_limit_triple_exits`), L4348 (`_verify_exits_placed`) [A10]; `insert_orders_atomic` L2600, L2769, L3025, L3253, L3691, L4706 [A10]; `insert_order` `orders/order_placer.py` L3965 (`_emergency_market_exit`) [A10], `orders/order_reconciler.py` L3095 (`_emergency_market_close`), L3339 (`_g5b_crash_recovery_sl`), L4584 (`_backfill_entry_order_row`) [A12]; `update_order_status` `orders/order_manager.py` L156 (`_on_order_status_changed`, the EventBus handler for `OrderStatusChanged`, subscribed at L144 when the OrderManager is constructed with a bus, as in `main.py` L3046 to L3050; exceptions logged and swallowed, L164 to L171) [A10; event published by A04's order monitor, `broker/order_monitor.py` L1334], `orders/order_reconciler.py` L4593 (`_backfill_entry_order_row`) [A12]. The reconciler's own OrderManager is built without a bus (`orders/order_reconciler.py` L320).
- P06a-S261 — FACT: the OrderManager built in `main.py` L3046 to L3050 (`bus=event_bus`) subscribes `_on_order_status_changed` to `OrderStatusChanged` (`orders/order_manager.py` L143 to L144); each such event writes `orders.status`, `qty_filled`, `avg_fill_price`, `rejection_reason` (COALESCE), `filled_at` (COALESCE; the handler passes a value only when the status is `COMPLETE`, L155) and `updated_at` through `update_order_status` (P06a-S080, own `transaction()`); a failure is logged and swallowed (L164 to L171). INTERPRETATION: the subscription uses the default synchronous mode, and `EventBus.publish` calls synchronous subscribers in the publisher's thread (`core/events.py` L322 to L327, `subscribe` default `async_dispatch=False` L273; docstring L304), so the UPDATE runs on the order monitor's publishing thread's StateStore connection (P06a-S012).
- P06a-S086 — HISTORICAL: module docstring L5 to L6 and OMgr1 (L10) say OrderManager "Owns all INSERT/UPDATE SQL for the `trades` and `orders` tables". FACT: sections 2.6, 2.11, 2.12, 2.13, 2.14 and 2.16 contain further raw INSERT/UPDATE statements on `trades` and `orders` outside OrderManager (summary in section 3.3).

### 2.11 `orders/order_placer.py` (owner A10)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S087 | L2489 to L2506 | `_handle_exit_fill` (only when `fill_entry.order_protocol == "CO_PLUS_TGT"` and a smart-target manager exists, L2489 to L2492) | `smart_tgt_state` | SELECT | reads `trail_count` WHERE `trade_id = ?` | no | try/except → DEBUG log (L2503 to L2506) |
| P06a-S088 | L2498 to L2502 | `_handle_exit_fill` | `trades` | UPDATE | `sl_trail_count` WHERE `trade_id = ?` | NO: issued through `StateStore.execute` (autocommit, P06a-S010) | same try/except → DEBUG log |
| P06a-S089 | L3817 to L3828 | `_mark_trade_exiting` | `trades` | UPDATE | `status = 'EXITING', updated_at` WHERE `trade_id = ?` (no status condition) | yes (L3821) | except → warning, swallowed |
| P06a-S090 | L3830 to L3852 | `_cancel_trade_resting_exits` | `orders` | SELECT | reads `order_id` WHERE `trade_id = ? AND leg IN ('SL','TGT') AND status NOT IN ('CANCELLED','FAILED','EXPIRED','COMPLETE')` | no | except → warning, return; no DB write in this method (cancel via `_cancel_broker_orders`) |

- P06a-S091 — FACT: all four statements reach the store through `self._om._store`, the private `_store` attribute of the OrderManager instance (L2494, L2499, L3821, L3835). Callers of S089/S090: `_emergency_market_exit` L3879, L3894, L3960. HISTORICAL: comment L2488 says the copy is made "before unregister deletes the row".
- P06a-S092 — Not SQL: `self._engine.execute(...)` (L1345) is the entry engine's order call, not SQL; other store calls are typed methods (`mark_needs_tgt_retry`, `get_open_orders_for_rehydration`, `get_orders_for_trade`, `get_sl_order_for_trade`, `get_trade_for_tgt_retry`): see parts P04/P05.

### 2.12 `orders/eod_squareoff.py` (owner A12)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S093 | L630 to L644 | `_human_order_symbols_for_date` | `reconciliation_log` | SELECT | DISTINCT `symbol` WHERE `check_name = 'ORPHAN_ADOPTION' AND DATE(ts) = ?` and symbol non-empty | no | except → DEBUG log, `[]` |
| P06a-S094 | L894 to L905 | `_cancel_pending_entries` (after a successful broker cancel, L885 to L892) | `trades`, `orders` | UPDATE x2 | `trades.status = 'CANCELLED', updated_at` WHERE `trade_id = ?` (no status condition); `orders.status = 'CANCELLED', updated_at` WHERE `order_id = ?` (no status condition) | yes, both in one (L896) | enclosing try (L884) → `except BrokerError` L930 / `except Exception` L937: CRITICAL log, `failed += 1`; the capital release at L908 to L922 is then not reached |
| P06a-S095 | L994 to L1000 | `_cancel_pending_exit_legs` (after a successful broker cancel) | `orders` | UPDATE | `status = 'CANCELLED', updated_at` WHERE `order_id = ?` (no status condition) | yes (L995) | enclosing excepts L1008 / L1016: CRITICAL log, `failed += 1` |
| P06a-S096 | L1215 to L1241 | `_exit_open_positions` (CO branch, after the broker accepted the CO cancel) | `orders` | INSERT OR IGNORE | `order_id` = `f"{entry_broker_id}_CO_CANCEL"` (L1230), `trade_id, leg` (`'EOD'`), `leg_index` 0, `transaction_type, order_type` (`'CANCEL'`), `product` (`'CO'`), `variety` (`'co'`), `qty_requested, price` NULL, `trigger_price` NULL, `status` (`'OPEN'`), `qty_filled` 0, `avg_fill_price` NULL, `placed_at, updated_at` | yes (L1217) | own try/except (L1234): warning "DB record insert failed (cancel already issued to broker)"; `succeeded += 1` still runs (L1241) |
| P06a-S097 | L1331 to L1350 | `_exit_open_positions` (MIS / LIMIT_TRIPLE branch, after the broker placed the exit) | `orders` | INSERT OR IGNORE | `order_id` (= broker id), `trade_id, leg` `'EOD'`, `leg_index` 0, `transaction_type, order_type, product` `'MIS'`, `variety` `'regular'`, `qty_requested, price` (LIMIT price or NULL), `status` `'OPEN'`, `placed_at, updated_at` | yes (L1333) | no own try; enclosing try (L1171) → `except Exception` L1369: CRITICAL log, `_mark_exit_failed` (S099), `failed += 1` |
| P06a-S098 | L1683 to L1700 | `_promote_limits_to_market` (after the MARKET exit was placed) | `orders` | INSERT OR IGNORE | as S097 with `leg_index` 1, `order_type` `'MARKET'`, `price` NULL | yes (L1683) | enclosing try (L1662) → `except Exception` L1707: CRITICAL log, `_mark_exit_failed`, `promote_failed += 1` |
| P06a-S099 | L1724 to L1734 | `_mark_exit_failed` | `trades` | UPDATE | `exit_reason = 'EOD_EXIT_FAILED', updated_at` WHERE `trade_id = ?` | yes (L1727) | except → `log_exception`, swallowed |

- P06a-S100 — Not SQL: the EOD write-ahead log and other reads go through typed methods (`insert_eod_squareoff_log_start`, `update_eod_squareoff_log_complete`, `insert_eod_squareoff_log`, `get_eod_squareoff_log_for_date`, `get_open_intraday_positions`, `get_pending_exit_orders_for_open_positions`, `get_pending_intraday_orders`, `get_reservation_id_for_signal`, `get_trades_for_date`, `insert_system_event`, `checkpoint`): see parts P04/P05 (and P01 for `checkpoint`). No paper/live split near these SQL sites (no "paper" reference in the file).

### 2.13 `orders/order_reconciler.py` (owner A12)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S101 | L486 to L496 | `sweep_stale_orders` | `orders`, `trades` | SELECT | `order_id` WHERE order status NOT IN ('COMPLETE','CANCELLED','FAILED','EXPIRED') AND `trade_id IN (SELECT trade_id FROM trades WHERE status IN ('CLOSED','CLOSED_MANUAL','CANCELLED','FAILED'))` | no | except → error log, returns 0 |
| P06a-S102 | L501 to L516 | `sweep_stale_orders` | `orders` | UPDATE (one per row, loop) | `status = 'CANCELLED', updated_at` WHERE `order_id = ? AND status NOT IN ('COMPLETE','CANCELLED','FAILED','EXPIRED')`; counts `rowcount` | yes, ALL rows in one (L504) | except → error log, returns 0 (whole batch rolled back, P06a-S008) |
| P06a-S103 | L1308 to L1317 | `_check1_manual_close` | `orders` | SELECT | `order_id, leg, status` WHERE `trade_id = ? AND leg IN ('SL','TGT','EOD')` | no | except → error log, `_legs_read_ok = False` |
| P06a-S104 | L1694 to L1705 | `_cancel_orphaned_orders_for_trade` | `orders` | SELECT | `order_id, leg` WHERE `trade_id = ? AND leg IN ('SL','TGT') AND status NOT IN ('CANCELLED','COMPLETE','REJECTED','FAILED')` | no | except → error log, `out.read_failed = True`, return |
| P06a-S105 | L1765 to L1784 | `_mark_order_cancelled_local` | `orders` | UPDATE | `status = 'CANCELLED', updated_at` WHERE `order_id = ? AND status NOT IN ('COMPLETE','CANCELLED','FAILED','EXPIRED')` | yes (L1773) | except → error log |
| P06a-S106 | L1902 to L1910 | `_detect_system_oversell` | `trades` | SELECT | `trade_id, direction, qty_filled, exit_price, exit_time` WHERE `symbol = ? AND status IN ('CLOSED','CLOSED_MANUAL') AND exit_time IS NOT NULL` ORDER BY `exit_time` DESC LIMIT 1 | no | except → `None` |
| P06a-S107 | L2410 to L2429 | `_check4_partial_close` | `trades` | UPDATE (compare-and-set) | `qty_filled = ?, updated_at` WHERE `trade_id = ? AND qty_filled = ?`; `rowcount == 1` sets `qty_transition_owned` | yes (L2412) | except → error log, `success = False` |
| P06a-S108 | L2645 to L2651 | `_check6_orphan_orders` (third orphan cycle, L2635) | `trades` | UPDATE | `status = 'FAILED', updated_at` WHERE `trade_id = ?` (no status condition) | yes (L2646) | except → error log; the capital release at L2656 to L2660 follows the try whatever its outcome |
| P06a-S109 | L2824 to L2829 | `_check9_missing_exits` | `orders` | SELECT | `COUNT(*)` WHERE `trade_id = ? AND leg IN ('SL','TGT','EOD') AND status = 'COMPLETE'` | no | no local try; caught at cycle level (`except Exception`, L994 to L997; `BrokerTimeoutError` L988 and `BrokerAuthError` L992 are handled separately), ending check 9 for the cycle |
| P06a-S110 | L2842 to L2845 | `_check9_missing_exits` | `trades` | SELECT | `status` WHERE `trade_id = ?` | no | as S109 |
| P06a-S111 | L2886 to L2891 | `_check9_missing_exits` | `orders` | SELECT | `COUNT(*)` WHERE `trade_id = ? AND leg = 'EOD' AND order_type = 'MARKET' AND status IN ('PENDING','SUBMITTED','OPEN')` | no | as S109 |
| P06a-S112 | L3199 to L3214 | `_g5b_crash_recovery_sl` | `orders` | SELECT | `COUNT(*)` WHERE `trade_id = ? AND leg = 'SL' AND status NOT IN ('CANCELLED','FAILED','EXPIRED','COMPLETE')` | no | except → warning "proceeding" (L3211 to L3214) |
| P06a-S113 | L3408 to L3423 | `_entry_fill_age_seconds` | `trades` | SELECT | `entry_time` WHERE `trade_id = ?` | no | except → `None` |
| P06a-S114 | L3564 to L3570 | `_dedupe_exit_leg` | `orders` | SELECT | `order_id` WHERE `trade_id = ? AND leg = ? AND status NOT IN ('CANCELLED','COMPLETE','REJECTED','FAILED','EXPIRED')` | no | except → `remaining = None` |
| P06a-S115 | L3572 to L3575 | `_dedupe_exit_leg` | `trades` | SELECT | `status` WHERE `trade_id = ?` | no | no local try |
| P06a-S116 | L4224 to L4231 | `_recover_in_flight_entries` | `trades` | SELECT | `*` WHERE `trade_id = ?` | no | except → error log, `continue` |
| P06a-S117 | L4509 to L4511 | `_recovery_flatten_under_kill` | `trades` | SELECT | `*` WHERE `trade_id = ?` | no | no local try |

- P06a-S118 — FACT: the reconciler also writes `orders` through OrderManager (`insert_order`, `update_order_status`: P06a-S085) and through typed state-store methods (`adopt_recovery_trade_to_open`, `fail_recovery_trade`, `insert_reconciliation_log`, `mark_needs_tgt_retry`, `mark_recovery_trade_exiting`, `mark_trade_manually_closed`, `record_manual_close_financials`, `revert_exiting_to_open`, `set_trade_closure_axes`, `update_order_reconciliation_status`; reads `get_*`, `sum_fm_ledger_margin_delta`): see parts P04/P05.
- P06a-S119 — HISTORICAL: RC15 (L52) states no paper-mode special-casing in the reconciler; no paper/live branch was found at the SQL sites above.

### 2.14 `orders/structure_exit_manager.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S120 | L349 to L362 | `_mark_exiting` | `trades` | UPDATE | `status = 'EXITING', updated_at` WHERE `trade_id = ?` (no status condition) | yes (L352) | except → error log, returns False; caller L317 then does not proceed |
| P06a-S121 | L365 to L379 | `_cancel_trade_resting_exits` | `orders` | SELECT | `order_id, leg` WHERE `trade_id = ? AND leg IN ('SL','TGT') AND status NOT IN ('CANCELLED','FAILED','EXPIRED','COMPLETE')` | no | except → warning, return |
| P06a-S122 | L396 to L404 | `_cancel_trade_resting_exits` (per row, after the broker cancel) | `orders` | UPDATE | `status = 'CANCELLED', updated_at` WHERE `order_id = ?` (no status condition) | yes (L397) | `except Exception: pass` |
| P06a-S123 | L480 to L501 | `_flatten_one` (after the broker placed the flatten) | `orders` | INSERT OR IGNORE | as S097 (`leg` `'EOD'`, `leg_index` 0, `product` `'MIS'`, `variety` `'regular'`, `status` `'OPEN'`) | yes (L483) | except → warning "EOD leg insert failed" |
| P06a-S124 | L603 to L617 | `_get_sl_leg` | `orders` | SELECT | `order_id, trigger_price, price` WHERE `trade_id = ? AND leg = 'SL' AND status NOT IN ('CANCELLED','COMPLETE','REJECTED','FAILED')` ORDER BY `placed_at` LIMIT 1 | no | except → error log, `None` |

- P06a-S125 — FACT: `StructureExitManager` is constructed in `main.py` L3817 inside a conditional block (A11/A18 own the activation conditions). HISTORICAL: docstrings L350 and L366 to L367 say these methods mirror `kill_switch.py`; FACT: S120 and S122 carry no status condition, whereas the kill-switch writes S053 and S056 do.

### 2.15 `orders/breakeven_manager.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S126 | L387 to L419 | `_get_sl_broker_order_id` | `orders` | SELECT | `order_id` WHERE `trade_id = ? AND leg = 'SL' AND status NOT IN ('CANCELLED','COMPLETE','REJECTED','FAILED')` LIMIT 1 | no | except → error log, `None` |

- P06a-S127 — FACT: `git grep` over non-test `*.py` finds no construction of `BreakevenManager` except its docstring example (L65); `orders/order_placer.py` holds it as an optional constructor argument defaulting to None (L577, L622). HISTORICAL: the docstring L393 to L396 says the same ("main.py never constructs a BreakevenManager").

### 2.16 `orders/sl_breach_monitor.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S128 | L133 to L159 | `_get_exposed_trades` | `trades`, `orders` | SELECT | `t.trade_id, t.symbol, t.direction, t.sl_initial, t.qty_filled`, sub-select `o2.product`; WHERE `t.status IN ('OPEN','PARTIAL') AND t.qty_filled > 0 AND NOT EXISTS` an SL order with status in ('OPEN','TRIGGER PENDING','SUBMITTED','PENDING') and `superseded_by IS NULL` | no | no local try |
| P06a-S129 | L250 to L288 | `_update_trade_exit` | `trades`, `orders` | UPDATE then INSERT | UPDATE `trades` SET `exit_reason = 'EMERGENCY_SL_TICK', exit_price, exit_time, updated_at` WHERE `trade_id = ? AND status IN ('OPEN','PARTIAL')`; INSERT `orders` (`order_id, trade_id, leg` `'EOD'`, `transaction_type, order_type` `'MARKET'`, `product` `'MIS'`, `variety` `'regular'`, `qty_requested, status` `'PENDING'`, `placed_at, updated_at`) only when `broker_order_id` is not None | yes, both in one (L257) | except → error log, swallowed |

- P06a-S130 — FACT: the Live/paper split is at L205 (`if self._mode == "LIVE" and self._adapter is not None`); the paper side (L243 to L248) is not traced. `git grep` over non-test `*.py` finds no construction or import of `SlBreachMonitor` outside its own file.

### 2.17 `orders/cnc_gtt_monitor.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S131 | L558 to L559 | `_finalize_gtt_exit` (after `mark_trade_closed_gtt` returned true, L552) | `trades` | SELECT | `*` WHERE `trade_id = ?` | no | no local try; callers L506, L526, L528 |

- P06a-S132 — Not SQL: the GTT lifecycle writes go through typed methods (`insert_gtt_state`, `set_gtt_state_status`, `set_gtt_state_needs_review`, `touch_gtt_state_verified`, `mark_trade_closed_gtt`, `record_gtt_close_financials`, `get_*`): see parts P04/P05. `CncGttMonitor` is constructed in `main.py` L3109.

### 2.18 `orders/shadow_tracker.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S133 | L280 to L283 | `_on_position_closed` | `trades` | SELECT | `*` WHERE `trade_id = ?` | no | no local try |
| P06a-S134 | L611 to L615 | `_close_inning` | `trades` | SELECT | `strategy, entry_actual_price, entry_target_price, sl_initial, tgt_initial` WHERE `trade_id = ?` | no | no local try at the call |
| P06a-S135 | L703 to L713 | `_send_alert` | `trades` | SELECT | `qty_filled` WHERE `trade_id = ?` | no | try/except → `total_pnl = None` |

- P06a-S136 — Not SQL: innings are written through typed methods (`insert_inning`, `update_inning_close`, `get_eod_squareoff_log_for_date`): see parts P04/P05. `ShadowTracker` is constructed in `main.py` L2946.

### 2.19 `orders/slippage_recorder.py` (owner A11)

| ID | Lines | Function | Table | Op | Columns written / read | Txn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S137 | L265 to L273 | `_enrich_order` | `orders` | SELECT | `leg, order_type, qty_requested, placed_at, trade_id` WHERE `order_id = ?` | no | enclosing try (L264) → `except Exception: pass` (L283 to L284) |
| P06a-S138 | L274 to L281 | `_enrich_order` | `trades` | SELECT | `signal_id, strategy, tolerance_fraction_used, tolerance_source` WHERE `trade_id = ?` | no | as S137 |
| P06a-S139 | L288 to L299 | `_fetch_trade` | `trades` | SELECT | `trade_id, symbol, strategy, direction, qty_filled, created_at, entry_target_price, entry_actual_price, sl_initial, tgt_initial, exit_price, exit_reason, net_pnl` WHERE `trade_id = ?` | no | except → `None` |

- P06a-S140 — Not SQL: the three slippage rows are written through typed methods (`insert_order_execution_log`, `insert_trade_slippage_log`, `insert_market_execution_context`): see parts P04/P05. `SlippageRecorder` is constructed in `main.py` L3095.

### 2.20 `ops/control_tower/aggregator.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns written / read | Conn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S141 | L103 to L137 (SQL L116 to L119) | `read_cron` | `cron_heartbeat` | SELECT | `job_name, status, MAX(executed_at)` WHERE `substr(executed_at,1,10) = ?` GROUP BY `job_name` | aggregator's own connection (L197) | adapter loop try/except (L214 to L218): logs, category not added to `ran` |
| P06a-S142 | L171 to L186 (SQL L172 to L174) | `read_excursion` | `excursion_reconstruction_runs` | SELECT | `status, started_at, trades_failed` ORDER BY `started_at` DESC LIMIT 1 | same | as S141 |
| P06a-S143 | L280 to L283 | `run_aggregation` (only when `report_dir` is given, after the commit) | `control_tower_trends` | SELECT | `date, disk_used_pct, backup_size_mb, log_size_mb, db_size_mb` ORDER BY `date` DESC LIMIT 7 | same | no local try; propagates; `finally` closes the connection |

- P06a-S144 — FACT, the write sequence of `run_aggregation` (L190 to L295) on one connection: `ensure_indexes` (L199, DDL, see S147) runs before the `write` check at L242, so it also runs when `write=False`; then `prior_status_map` (L245), `upsert_finding` per finding (L246 to L247), `auto_resolve_stale` (L248), `replace_freshness` (L249), `write_run` (L250 to L261), `open_severities` (L264), `health.write_trend_health` (L266), `ctstatus.write_status` (L268 to L273), then ONE `conn.commit()` (L274); `conn.close()` in `finally` (L294 to L295).
- P06a-S145 — FACT: exceptions in the four adapters, `freshness.evaluate` and `disk.evaluate` are caught (L214 to L230); the write phase L245 to L274 has no try/except, so an exception there leaves `run_aggregation` through the `finally`. INTERPRETATION (P06a-S014): writes made before such an exception are not committed and are discarded on `close()`.
- P06a-S146 — FACT: callers of `run_aggregation`: `ops/control_tower/runner.py` L67 to L69 (`run`, after `size_logger.run` at L64, both with the same `now`) and the module's own `main` L315 to L317. Schedules: A16.

### 2.21 `ops/control_tower/db.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns written / read | Conn / commit | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S147 | L16 to L24 | `ensure_indexes` | `control_tower_findings` | DDL: CREATE INDEX IF NOT EXISTS | index `idx_ct_findings_last_seen` on `last_seen` (no rows written) | caller's connection; no commit in function | none local |
| P06a-S148 | L27 to L58 | `upsert_finding` | `control_tower_findings` | INSERT ... ON CONFLICT(`category, resource_name, reason`) DO UPDATE | insert: `scan_time, category, severity, resource_type, resource_name, location, reason, recommended_action, status` (`'OPEN'`), `first_seen, last_seen`; update: `scan_time, last_seen, severity, resource_type, location, recommended_action`, `status` (RESOLVED → OPEN, else kept), `resolved_at` (RESOLVED → NULL, else kept) | caller's; committed by aggregator L274 | none local |
| P06a-S149 | L61 to L71 | `replace_freshness` | `control_tower_freshness` | DELETE then executemany INSERT | DELETE WHERE `run_date = ?`; INSERT `run_date, stage, expected_by, actual_at, delay_minutes, status` | caller's; committed by aggregator | none local |
| P06a-S150 | L74 to L78 | `prior_status_map` | `control_tower_findings` | SELECT | `category, resource_name, reason, status` (all rows) | caller's | none local |
| P06a-S151 | L81 to L94 | `auto_resolve_stale` | `control_tower_findings` | UPDATE | `status = 'RESOLVED', resolved_at` WHERE `category IN (...) AND status IN ('OPEN','ACKNOWLEDGED') AND last_seen < ?`; returns `rowcount`; no-op if no categories ran (L86 to L87) | caller's; committed by aggregator | none local |
| P06a-S152 | L97 to L102 | `ack_finding` | `control_tower_findings` | UPDATE | `status = 'ACKNOWLEDGED', acked_at` WHERE `id = ? AND status != 'RESOLVED'` | caller's; `conn.commit()` L101 | none local |
| P06a-S153 | L105 to L110 | `unack_finding` | `control_tower_findings` | UPDATE | `status = 'OPEN', acked_at = NULL` WHERE `id = ? AND status = 'ACKNOWLEDGED'` | caller's; `conn.commit()` L109 | none local |
| P06a-S154 | L116 to L123 | `get_findings` | `control_tower_findings` | SELECT | `id, severity, category, resource_name, reason, first_seen, last_seen, status, acked_at, resolved_at` WHERE `status IN (...)`, ordered by a CASE over severity names built from the module constant `_SEV_ORDER` (L113, interpolated into the SQL text at L118) | caller's | none local |
| P06a-S155 | L126 to L128 | `open_severities` | `control_tower_findings` | SELECT | `severity` WHERE `status = 'OPEN'` | caller's | none local |
| P06a-S156 | L131 to L146 | `write_run` | `control_tower_runs` | INSERT | `run_id, started_at, completed_at, duration_s, checks_run, findings_total, critical_count, high_count, medium_count, low_count, status` | caller's; committed by aggregator | none local |

- P06a-S157 — FACT: the conflict target of S148 is backed by the unique index `idx_ct_findings_dedup` (`core/schema.sql` L1410 to L1411). `control_tower_freshness` has only a non-unique index on `(run_date, stage)` (schema L1471).
- P06a-S158 — FACT: `ack_finding` and `unack_finding` are called by `ops/control_tower/cli.py` L53 and L56 on a connection opened at L48 (`attach=False`); `get_findings` by `cli.py` L51 and `aggregator.py` L287.
- P06a-S159 — FACT: the index of S147 is also declared in `core/schema.sql` L1414 to L1415 with the same name and column. HISTORICAL: the comment at `db.py` L13 to L15 says this index is "NOT already created by the v40 schema".

### 2.22 `ops/control_tower/freshness.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns read | Conn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S160 | L22 to L24 | `_scalar` (helper used by all rows below) | (per call) | SELECT | first column of the first row | caller's connection (aggregator, analytics attached) | none local; `evaluate` is called under try at aggregator L219 to L224 |
| P06a-S161 | L83 to L85 | `evaluate` | `candles` | SELECT `MAX(date)` | analytics: see P07 (resolved through the ATTACHed analytics database; module docstring L7) | | |
| P06a-S162 | L88 to L91 | `evaluate` | `signals` | SELECT | `COUNT(*)` and `MAX(received_at)` WHERE `substr(received_at,1,10) = ?` | | |
| P06a-S163 | L94 to L97 | `evaluate` | `orders` | SELECT | `COUNT(*)` and `MAX(placed_at)` WHERE `substr(placed_at,1,10) = ?` | | |
| P06a-S164 | L100 to L105 | `evaluate` | `order_execution_log` | SELECT | `COUNT(*)` and `MAX(COALESCE(fill_timestamp, created_at))` for the date | | |
| P06a-S165 | L108 to L112 | `evaluate` | `excursion_reconstruction_runs` | SELECT | `MAX(started_at)` and `COUNT(*)` WHERE `substr(started_at,1,10) = ?` | | |
| P06a-S166 | L115 to L117 | `evaluate` | `eod_squareoff_log` | SELECT | `fired_at` WHERE `fired_date = ? AND status = 'COMPLETE'` | | |

### 2.23 `ops/control_tower/disk.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns read | Conn | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S167 | L38 to L40 | `evaluate` | `control_tower_trends` | SELECT | `date, backup_size_mb, log_size_mb` WHERE `date < ?` ORDER BY `date` DESC LIMIT 1 | caller's (aggregator L226) | none local; aggregator try L225 to L230 |

### 2.24 `ops/control_tower/health.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns written | Conn / commit | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S168 | L22 to L41 | `write_trend_health` | `control_tower_trends` | INSERT ... ON CONFLICT(`date`) DO UPDATE | `date, health_score, critical_count, high_count, medium_count`; update touches only the last four | caller's; committed by aggregator L274 | none local |

### 2.25 `ops/control_tower/status.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns written | Conn / commit | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S169 | L19 to L51 | `write_status` | `control_tower_status` | INSERT ... ON CONFLICT(`run_date`) DO UPDATE | `run_date, security_status, cron_status, config_status, freshness_status, disk_pct, backup_size_mb, critical_count, high_count, overall_status, last_successful_run`; update overwrites all ten non-key columns | caller's; committed by aggregator L274 | none local |

### 2.26 `ops/control_tower/size_logger.py` (owner A15)

| ID | Lines | Function | Table | Op | Columns written | Conn / commit | Error route |
|---|---|---|---|---|---|---|---|
| P06a-S170 | L58 to L74 | `upsert_trend` | `control_tower_trends` | INSERT ... ON CONFLICT(`date`) DO UPDATE | `date, disk_used_pct, backup_size_mb, log_size_mb, db_size_mb`; update touches only the four size columns | own connection from `run` (L83, `attach=False`); `conn.commit()` L74; `close()` in `finally` L86 to L87 | via `size_logger.main`: caught at L110 to L113 (logs, status `FAILED`, exit code 1); via `ops/control_tower/runner.py` `run` (L64, no try): propagates, the aggregation at L67 does not run, caught in `runner.main` L120 to L123 (FAILED heartbeat, exit 1) |

- P06a-S171 — FACT: `size_logger.main` then calls `utils.cron_heartbeat.record_heartbeat` (L115 to L125) unless `--no-heartbeat`; that write is in `utils/cron_heartbeat.py` (owner A16; not in this part). HISTORICAL: docstring L16 states a cron time (schedule: A16).
- P06a-S172 — FACT: `control_tower_trends` has `date` as PRIMARY KEY (`core/schema.sql` L1436); S168 and S170 write disjoint column sets of the same date row.

### 2.27 Files with no SQL (not SQL)

| ID | File (owner) | What was found |
|---|---|---|
| P06a-S173 | `broker/order_monitor.py` (A04) | not SQL: no raw SQL; typed state-store calls `get_open_orders_for_rehydration`, `get_orphaned_pending_trades` (P04/P05); `engine.execute` mentions at L344, L402 are comments about the order engine |
| P06a-S174 | `orders/entry_engine.py` (A10) | not SQL: `execute` is the abstract entry-engine order method (L86) |
| P06a-S175 | `orders/full_entry_engine.py` (A10) | not SQL: `execute` routes to the selected engine (L72 to L119) |
| P06a-S176 | `orders/mis_autosquareoff.py` (A12) | not SQL: typed calls `get_open_mis_exit_orders_for_symbol`, `get_orders_for_trade` (P04/P05); the "SELECT DISTINCT product FROM orders" text at L86 is a comment |

## 3. Items the brief singles out

### 3.1 `main.py` `_write_session` and its two calls (A01 handoffs B-14, C33, S-10, C6)

- P06a-S177 — FACT: `session` (`core/schema.sql` L478 to L501) has exactly the nine columns that `_write_session` lists (`id` with `CHECK (id = 1)`, `session_date`, `account_id`, `broker`, `mode`, `trade_type`, `last_config_hash`, `session_start`, `last_updated`), so every column is supplied on every write.
- P06a-S178 — INTERPRETATION (SQLite REPLACE conflict resolution): when row 1 exists, INSERT OR REPLACE deletes it and inserts the supplied row; the result equals the supplied values, so `session_start` is set to the current `now_iso` at each call and the previous value is not kept.
- P06a-S179 — FACT: the two calls pass the same hash expression `json.dumps(app_config.file_hashes)` (L2312, L4178). HISTORICAL: the comment at L2307 says the Phase 0h call "will UPDATE this row with the final config_hash".
- P06a-S180 — FACT, order in `_main_locked`: scenario detection (L2268 onward), `check_config_hash` reads the session row (L2295; `utils/startup_checks.py` L594), the `--status` return (L2299 to L2302), call 1 (L2308), `run_all_startup_checks` (L2451), which reads the session row again through `detect_startup_scenario` (`utils/startup_checks.py` L1561 → L214) and `check_config_hash` (L1578 → L594), i.e. the row call 1 has just written, interactive mode selection that can reassign `args.mode` (L2538), call 2 (L4174). Call 1 therefore writes the `mode`/`broker` derived from `args.mode` as it stood before L2538.
- P06a-S181 — FACT: `account_id` is the literal `'default'` (L629) while the config snapshot of the same boot stores `selected_account.account_id` (L2608); `trade_type` is the literal `'INTRADAY'` (L629) while the snapshot stores `app_config.system.trade_type` (L2610).
- P06a-S182 — FACT: neither call has a try/except; each runs in its own `transaction()` on the main thread's connection.
- P06a-S183 — FACT, readers of `session` (all through `StateStore.get_session_row`, `core/state_store.py` L2474 to L2480, except the dashboard): `utils/startup_checks.py` L214 (`detect_startup_scenario`) and L594 (`check_config_hash`) [A01]; `main.py` L640 (`_print_status`) [A01]; `reports/daily_report.py` L136 [A15; P06b]; `ops_dashboard/backend/readers/db_reader.py` L122 to L126 (`get_session_info`, own SELECT of all columns except `last_config_hash`) [A15; P06b]. `git grep` finds no other non-test writer of `session`.

### 3.2 CREATE TABLE or ALTER outside `core/schema.sql` and `core/migrations.py`

- P06a-S184 — FACT: in the 30 files, the only DDL is `ops/control_tower/db.py` L16 to L24 (CREATE INDEX IF NOT EXISTS, P06a-S147). No CREATE TABLE, ALTER TABLE, DROP, CREATE TRIGGER, VACUUM, PRAGMA or ATTACH statement is issued by these files (grep, P06a-S005); PRAGMAs and ATTACH come from the openers (part P01).

### 3.3 Writes that bypass the typed state-store methods

- P06a-S185 — FACT: every write in sections 2.1 to 2.19 uses the generic StateStore API (`transaction()` + `cur.execute`, or `execute`) with SQL text held in the calling module, not a typed state-store method. Writers of `trades` outside OrderManager: S053 (kill switch, EXITING, conditional), S088 (`sl_trail_count`, autocommit), S089 (order placer, EXITING, unconditional), S094 (EOD, CANCELLED, unconditional), S099 (EOD, `exit_reason`), S107 (reconciler, `qty_filled` CAS), S108 (reconciler, FAILED, unconditional), S120 (structure exit, EXITING, unconditional), S129 (SL breach, exit fields, conditional). Writers of `orders` outside OrderManager: S056 (conditional CANCELLED), S094, S095 (unconditional CANCELLED), S096, S097, S098, S123 (INSERT OR IGNORE EOD legs), S102, S105 (conditional CANCELLED), S122 (unconditional CANCELLED), S129 (INSERT).
- P06a-S186 — FACT: the Control Tower writes (sections 2.20 to 2.26) bypass `StateStore` entirely and use their own `sqlite3` connection with Python-managed commits (P06a-S013, S144, S152, S153, S170).
- P06a-S187 — FACT: the only write not wrapped in an explicit transaction among the StateStore writes is S088 (`StateStore.execute`).

### 3.4 `core/config_snapshotter.py` writes to `config_snapshots` (A02 handoffs V-11, V-45)

- P06a-S188 — FACT: covered by P06a-S025 to S029: the INSERT columns are the table's seven non-key columns (V-45 storage); the duplicate check keys on `(snapshot_date, config_hash)` only, runs outside the INSERT's transaction, and the table has no UNIQUE constraint on that pair (V-11, the table side). No retention or deletion of `config_snapshots` rows exists in these 30 files (retention scripts: part P09b).

### 3.5 `session.last_config_hash` writes and reads (A02 handoff)

- P06a-S189 — FACT: the only writer is `_write_session` (P06a-S018 to S020); the value is `json.dumps(app_config.file_hashes)`, a JSON object of file name to hash (`core/config_loader.py` L2434 declares `file_hashes: dict[str, str]`).
- P06a-S190 — FACT: the only reader is `utils/startup_checks.py` `check_config_hash` L581 to L634 (via `get_session_row`, L594): it parses the JSON (L598 to L606), treats a NULL, unparseable or empty value as "first run, no change" (L608 to L616), else lists the files whose hash differs (L618 to L622). It is called twice per start: `main.py` L2295 (result used at L2656 to L2663) and `utils/startup_checks.py` L1578 inside `run_all_startup_checks` (called at `main.py` L2451; a change adds the warning `config_hash_changed`, L1579 to L1580). The dashboard reader (`db_reader.py` L125 to L126) does not select this column.
- P06a-S191 — FACT: the read at L2295 happens before call 1 at L2308, so it sees the value left by the previous process; call 1 already stores the current hashes before the rest of startup runs. The second read, `run_all_startup_checks` → `check_config_hash` (`utils/startup_checks.py` L1578, via `main.py` L2451), runs after call 1, so it compares the current hashes with the value call 1 has just stored. INTERPRETATION: in that second call `changed` is False whenever call 1 succeeded and `app_config.file_hashes` is unchanged between L2308 and L2451 (same object, read twice).
- P06a-S259 — FACT: a start reads the session row four times: `detect_startup_scenario` and `check_config_hash` at `main.py` L2268 and L2295 (before call 1), and again inside `run_all_startup_checks` (`main.py` L2451 → `utils/startup_checks.py` L1561 → L214 and L1578 → L594), after call 1 at L2308 has replaced the row with today's date, the pre-selection mode and the current hashes. Owner of the reads: A01; storage side: A03.

## 4. Routes (normal, error, retry, restart, partial failure)

| ID | Path | Normal | Error / partial failure | Retry / restart |
|---|---|---|---|---|
| P06a-S192 | session row (S018 to S020) | two full-row replacements per successful start | an exception in either call is unhandled locally (S182); a start that fails between L2308 and L4174 leaves the call-1 row | the next start reads the call-1 row (S191); runtime outcome of a real failure UNKNOWN |
| P06a-S193 | config snapshot (S025, S026) | one row per distinct `(date, hash)` | failure logged non-fatal by `main.py`; the INSERT rolls back | a restart with the same date and hash writes nothing; a different hash adds a row |
| P06a-S194 | signal intake (S031 to S035) | INSERT QUEUED, then queue push | IntegrityError → duplicate or re-queue of a `QUEUE_FULL` row; other DB error → `STORE_ERROR` with claims released; queue full → `QUEUE_FULL` UPDATE (best-effort) | the sender's retry hits the same fingerprint row (S036); restart handling of rows left `QUEUED` is not in this file (A06) |
| P06a-S195 | capital ledger (S046) | ledger row committed before the in-memory mutation (S047) | INSERT failure re-raised to the caller, mutation skipped | restart replay reads the ledger (S042 to S045); read failures have no local handling |
| P06a-S196 | kill-switch persist (S051) | persisted before the in-memory switch | exception propagates; in-memory state unchanged (S059) | `_load_state_from_store` at construction (S052); read failure → INACTIVE |
| P06a-S197 | kill-switch flatten writes (S053, S056) | conditional writes; `rowcount == 0` logged | write failures swallowed (logged or silent) | the retry loop re-derives from the broker (docstring L1531 to L1534, HISTORICAL) |
| P06a-S198 | EOD order rows (S094 to S099) | broker action first, then the DB write | DB failure after a successful broker action counts the item as failed and, for S097/S098, marks `EOD_EXIT_FAILED`; for S096 the failure is logged and the item still counts as succeeded | INSERT OR IGNORE makes a repeated insert of the same `order_id` a no-op; restart recovery of EOD is via the typed EOD-log methods (P04/P05) |
| P06a-S199 | reconciler writes (S102, S105, S107, S108) | conditional or CAS writes, except S108 | each failure logged; S102 rolls back the whole sweep; S108's capital release proceeds after a failed UPDATE | each cycle re-runs; check-9 SELECT failures end check 9 for the cycle (S109) |
| P06a-S200 | Control Tower run (S141 to S170) | all aggregator writes committed once (S144); size-logger and ACK CLI commit per call | adapter errors isolated; a write-phase error discards uncommitted writes (S145) | a re-run on the same date replaces freshness rows (S149) and upserts trends and status rows (S168 to S170); runs (S156) accumulate |
| P06a-S262 | orders status sync (S080 via `orders/order_manager.py` L156; S261) | one UPDATE per `OrderStatusChanged` event, in its own transaction | failure logged and swallowed in the handler (L164 to L171), not raised to the publisher | no retry in the handler; the WHERE has no status condition, and no trigger guards `orders.status` (the only trigger in `core/schema.sql` is on `trades`, L291) |

## 5. Table-by-table summary for these 30 files

| ID | Table (database) | Writers in these files (file: function) | Readers in these files (file: function) | Owner topics |
|---|---|---|---|---|
| P06a-S201 | `session` (trading) | `main.py`: `_write_session` | none by raw SQL; `main.py`: `_print_status` via typed `get_session_row` (L640); other readers outside (S183) | A01 (wiring), A02 (hash), A03 (storage) |
| P06a-S202 | `config_snapshots` (trading) | `core/config_snapshotter.py`: `snapshot_config` | `core/config_snapshotter.py`: `snapshot_config` (existence check) | A02; A15 (readers outside) |
| P06a-S203 | `signals` (trading) | `signals/webhook_receiver.py`: `_process_signal` (INSERT, 2 UPDATEs); `orders/order_manager.py`: `link_signal_trade` | `signals/webhook_receiver.py`: `_process_signal`; `orders/order_manager.py`: `_compute_and_store_latency`; `ops/control_tower/freshness.py`: `evaluate` | A06, A10, A15 |
| P06a-S204 | `webhook_audit` (trading) | `signals/webhook_receiver.py`: `_write_audit` | `main.py`: `_shutdown` (census count) | A06, A01, A15 |
| P06a-S205 | `trades` (trading) | `orders/order_manager.py`: `create_trade`, `record_exits_verification`, `record_entry_fill`, `_compute_and_store_latency`, `close_trade`, `update_trade_status`; `orders/order_placer.py`: `_handle_exit_fill`, `_mark_trade_exiting`; `capital/kill_switch.py`: `_mark_trade_exiting`; `orders/eod_squareoff.py`: `_cancel_pending_entries`, `_mark_exit_failed`; `orders/order_reconciler.py`: `_check4_partial_close`, `_check6_orphan_orders`; `orders/structure_exit_manager.py`: `_mark_exiting`; `orders/sl_breach_monitor.py`: `_update_trade_exit` | `main.py`: `_fire_eod_pre_alert`; `capital/kill_switch.py`: `_count_open_positions`, `_exit_all_trades_indestructible`; `capital/strategy_governor.py`: `_get_today_pnl`, `_get_avg_daily_loss`; `capital/performance_allocator.py`: `_fetch_stats`; `signals/signal_processor.py`: `_enforce_strategy_position_cap`; `orders/order_manager.py`: `get_trade`, `_compute_and_store_latency`; `orders/order_reconciler.py`: `sweep_stale_orders`, `_detect_system_oversell`, `_check9_missing_exits`, `_entry_fill_age_seconds`, `_dedupe_exit_leg`, `_recover_in_flight_entries`, `_recovery_flatten_under_kill`; `orders/sl_breach_monitor.py`: `_get_exposed_trades`; `orders/cnc_gtt_monitor.py`: `_finalize_gtt_exit`; `orders/shadow_tracker.py`: `_on_position_closed`, `_close_inning`, `_send_alert`; `orders/slippage_recorder.py`: `_enrich_order`, `_fetch_trade` | A10, A11, A12, A13, A09, A06, A01 |
| P06a-S206 | `orders` (trading) | `orders/order_manager.py`: `insert_order`, `insert_orders_atomic`, `update_order_status`; `capital/kill_switch.py`: `_cancel_trade_resting_exits`; `orders/eod_squareoff.py`: `_cancel_pending_entries`, `_cancel_pending_exit_legs`, `_exit_open_positions` (2 inserts), `_promote_limits_to_market`; `orders/order_reconciler.py`: `sweep_stale_orders`, `_mark_order_cancelled_local`; `orders/structure_exit_manager.py`: `_cancel_trade_resting_exits`, `_flatten_one`; `orders/sl_breach_monitor.py`: `_update_trade_exit` | `capital/kill_switch.py`: `_fetch_co_entry`, `_cancel_trade_resting_exits`, `_exit_all_trades_indestructible`; `orders/order_manager.py`: `get_orders_for_trade`, `_compute_and_store_latency`; `orders/order_placer.py`: `_cancel_trade_resting_exits`; `orders/order_reconciler.py`: `sweep_stale_orders`, `_check1_manual_close`, `_cancel_orphaned_orders_for_trade`, `_check9_missing_exits`, `_g5b_crash_recovery_sl`, `_dedupe_exit_leg`; `orders/structure_exit_manager.py`: `_cancel_trade_resting_exits`, `_get_sl_leg`; `orders/breakeven_manager.py`: `_get_sl_broker_order_id`; `orders/sl_breach_monitor.py`: `_get_exposed_trades`; `orders/slippage_recorder.py`: `_enrich_order`; `ops/control_tower/freshness.py`: `evaluate` | A10, A11, A12, A13, A15 |
| P06a-S207 | `fm_ledger` (trading) | `capital/fund_manager.py`: `_write_ledger` | `capital/fund_manager.py`: `_today_release_used_pnl_rows`, `_replay_open_trade`, `_commit_exists`, `_restore_reserve_from_ledger` | A09 |
| P06a-S208 | `kill_switch_state` (trading) | `capital/kill_switch.py`: `_persist_state` | `capital/kill_switch.py`: `_load_state_from_store` | A13 |
| P06a-S209 | `shadow_trades` (trading) | `capital/shadow_engine.py`: `_persist_shadow_trade`, `_update_shadow_trade_exit` | `capital/shadow_engine.py`: `get_daily_summary` | A09, A18 |
| P06a-S210 | `smart_tgt_state` (trading) | none here (typed methods elsewhere) | `orders/order_placer.py`: `_handle_exit_fill` | A10, A11 |
| P06a-S211 | `reconciliation_log` (trading) | none here (typed method `insert_reconciliation_log`) | `orders/eod_squareoff.py`: `_human_order_symbols_for_date` | A12 |
| P06a-S212 | `cron_heartbeat` (trading) | none here (`utils/cron_heartbeat.py`, A16) | `ops/control_tower/aggregator.py`: `read_cron` | A16, A15 |
| P06a-S213 | `excursion_reconstruction_runs` (trading) | none here | `ops/control_tower/aggregator.py`: `read_excursion`; `ops/control_tower/freshness.py`: `evaluate` | A15 |
| P06a-S214 | `order_execution_log` (trading) | none here (typed method via `orders/slippage_recorder.py`) | `ops/control_tower/freshness.py`: `evaluate` | A11, A15 |
| P06a-S215 | `eod_squareoff_log` (trading) | none here (typed methods via `orders/eod_squareoff.py`) | `ops/control_tower/freshness.py`: `evaluate` | A12, A15 |
| P06a-S216 | `control_tower_findings` (trading) | `ops/control_tower/db.py`: `upsert_finding`, `auto_resolve_stale`, `ack_finding`, `unack_finding`; DDL `ensure_indexes` | `ops/control_tower/db.py`: `prior_status_map`, `get_findings`, `open_severities` | A15 |
| P06a-S217 | `control_tower_runs` (trading) | `ops/control_tower/db.py`: `write_run` | none here | A15 |
| P06a-S218 | `control_tower_freshness` (trading) | `ops/control_tower/db.py`: `replace_freshness` | none here | A15 |
| P06a-S219 | `control_tower_trends` (trading) | `ops/control_tower/health.py`: `write_trend_health`; `ops/control_tower/size_logger.py`: `upsert_trend` | `ops/control_tower/disk.py`: `evaluate`; `ops/control_tower/aggregator.py`: `run_aggregation` | A15 |
| P06a-S220 | `control_tower_status` (trading) | `ops/control_tower/status.py`: `write_status` | none here | A15 |
| P06a-S221 | `candles` (analytics) | none here | `ops/control_tower/freshness.py`: `evaluate` (analytics: see P07) | A05, A15 |

## 6. Concerns for the AUDIT (neutral)

- P06a-S222 — `session`: two different values of `mode`/`broker` can be written in one boot (call 1 before, call 2 after the interactive mode selection), `session_start` is replaced at each write, and `account_id`/`trade_type` are literals (S178, S180, S181).
- P06a-S223 — `config_snapshots`: check-then-insert in two steps with no UNIQUE constraint on `(snapshot_date, config_hash)` (S027).
- P06a-S224 — Status writes on `trades` without a from-state condition (S075, S078, S089, S094, S108, S120) sit beside conditional ones for the same transitions (S053, S077); the terminal-status trigger aborts some of them (S083, S084), and each caller handles that differently (propagate, swallow, count as failed).
- P06a-S225 — `orders` CANCELLED writes without a terminal-status guard (S094, S095, S122) beside guarded ones for the same purpose (S056, S102, S105).
- P06a-S226 — Broker action first, database row second, in EOD and structure-exit paths: a DB failure after a successful broker action is counted or logged differently per site (S094 to S098, S123).
- P06a-S227 — `orders.order_id` receives a synthetic value `<broker id>_CO_CANCEL` for the CO cancel marker (S096), while other code and comments treat `order_id` as the broker-assigned id (e.g. `capital/kill_switch.py` L1630 to L1633, HISTORICAL).
- P06a-S228 — `sl_trail_count` is written by `StateStore.execute` outside any explicit transaction, through another object's private `_store` attribute (S088, S091).
- P06a-S229 — Webhook intake: a committed `QUEUED` row precedes the queue push; on the re-queue route the queue push precedes the status flip, and a failed flip leaves the row `QUEUE_FULL` while the signal is queued (S037, S033).
- P06a-S230 — Reconciler check 6 releases capital after the FAILED UPDATE whether or not the UPDATE succeeded (S108).
- P06a-S231 — Strategy-governor P&L windows are keyed on `trades.updated_at`, which the other `trades` UPDATEs listed in this part also rewrite (S053, S072, S075, S077, S078, S089, S094, S099, S107, S108, S120, S129), except S076 (latency columns) and S088 (`sl_trail_count`) (S062, S063).
- P06a-S232 — Control Tower: `ensure_indexes` runs DDL even with `write=False`; the write phase has a single commit with no error handling, and its index DDL repeats an index that `core/schema.sql` also declares, while the `db.py` comment says the schema does not (S144, S145, S159).
- P06a-S233 — `capital/fund_manager.py` docstring claims ledger and mutation "in same txn"; the code writes the ledger in its own transaction before the in-memory mutation (S048).
- P06a-S234 — OrderManager's docstring claim of owning all `trades`/`orders` INSERT/UPDATE SQL against the raw writers listed in S185.
- P06a-S235 — Four classes with SQL have no construction site found by text search (`PerformanceAllocator`, `ShadowEngine`, `BreakevenManager`, `SlBreachMonitor`; S066, S070, S127, S130); their SQL is present in the repository.
- P06a-S236 — `fund_manager` ledger reads (S042 to S045), `_check9_missing_exits` reads (S109 to S111) and the other reads marked "no local try" propagate any exception to their callers; how each caller handles it is not traced here.
- P06a-S260 — The second scenario detection and the second config-hash diff of a start read the session row that call 1 wrote earlier in the same start (`utils/startup_checks.py` L1561, L1578; S259).
- P06a-S263 — `orders/sl_breach_monitor.py` L213 to L220 place the emergency exit as a LIMIT order when the last price is positive (MARKET otherwise), while the INSERT at L272 to L278 records `order_type` as the literal `'MARKET'` (S129).

## 7. Questions about intent (OPEN QUESTION, for the project owner)

- P06a-S237 — OPEN QUESTION: was the session row meant to keep the first `session_start` of the day, and to record the selected account and configured trade type, rather than replacing the row with literals at each write (S178, S181)?
- P06a-S238 — OPEN QUESTION: were the unconditional status writes on `trades` and `orders` (S224, S225) meant to differ from the guarded writes for the same transitions?
- P06a-S239 — OPEN QUESTION: was a UNIQUE constraint intended for `config_snapshots(snapshot_date, config_hash)` (S223)?
- P06a-S240 — OPEN QUESTION: were `PerformanceAllocator`, `ShadowEngine`, `BreakevenManager` and `SlBreachMonitor` meant to be wired in Live, or kept as dormant code with live SQL (S235)?

## 8. UNKNOWN / NOT ESTABLISHED

- P06a-S241 — UNKNOWN / NOT ESTABLISHED: whether any of these statements ran in production, how often, and with what outcomes; no database, log or backup survives.
- P06a-S242 — UNKNOWN / NOT ESTABLISHED: whether the terminal-status trigger ever aborted one of the unconditional status writes at runtime (S084).
- P06a-S243 — UNKNOWN / NOT ESTABLISHED: lock waits or `database is locked` errors on `BEGIN IMMEDIATE` (S008) for any path, including the kill-switch persist; the docstring's statement about logs (S060) is HISTORICAL only.
- P06a-S244 — UNKNOWN / NOT ESTABLISHED: the Python version at runtime, which governs the exact implicit-transaction behaviour of the Control Tower connections (S014).
- P06a-S245 — UNKNOWN / NOT ESTABLISHED: whether the Control Tower jobs ran, on which database path, and whether `cli.py` ACK/UNACK was ever used (schedules and invocations: A16).
- P06a-S246 — UNKNOWN / NOT ESTABLISHED: the content of stored `webhook_payload`, `config_json` and `reason` values (not examined; security restriction on identifiers applies).

## 9. Boundary handoffs (owner topic: what crosses)

- P06a-S247 — A01: `_write_session` wiring, its two call sites and order relative to the interactive mode selection (S018 to S020, S180); the four reads of the session row per start, two of them after call 1 (S259); `_fire_eod_pre_alert` thread; census count in `_shutdown` (S021, S022).
- P06a-S248 — A02: `config_snapshots` writer and duplicate key (S025 to S029, V-11, V-45); `session.last_config_hash` writer and reader, read twice per start (S189 to S191, S259).
- P06a-S249 — A06: `signals` and `webhook_audit` writes and the duplicate/re-queue/queue-full routes (S031 to S037); strategy cap query (S039).
- P06a-S250 — A09: `fm_ledger` write-ahead and replay reads (S042 to S048); strategy-governor and performance-allocator reads (S062, S063, S065); `shadow_trades` (S067 to S069).
- P06a-S251 — A10: OrderManager SQL and its callers (S071 to S085); order-placer raw writes (S087 to S090); the `OrderStatusChanged` handler that writes `orders` (S261, S262; the event is published by A04's `broker/order_monitor.py` L1334).
- P06a-S252 — A11: structure-exit, breakeven, SL-breach, CNC GTT, shadow-tracker and slippage SQL (S120 to S140).
- P06a-S253 — A12: EOD and reconciler raw SQL (S093 to S118).
- P06a-S254 — A13: kill-switch persistence and flatten SQL (S050 to S061).
- P06a-S255 — A15: Control Tower DAO, aggregator, freshness, disk, health, status and size logger (S141 to S172); readers of `session` and `config_snapshots` in reports and the dashboard (pointer: P06b).
- P06a-S256 — A16: `cron_heartbeat` writes and every schedule of the Control Tower jobs (S171, S212).
- P06a-S257 — A18: activation of shadow and allocation code (S066, S070).
- P06a-S258 — Parts: P01 (connection set-up of StateStore and the Control Tower openers), P02a/P02b (table, index and trigger definitions cited), P04/P05 (typed state-store methods named as "not SQL"), P06b (readers in reports, scripts and the dashboard), P07 (`candles` and other analytics reads), P09b (retention of these tables).
