# A03 evidence: The state-store API, part A

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P04, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** The state-store methods of `core/state_store.py` L618 to L1901: tables, SQL, transactions, state transitions, error handling and every non-test caller. Statement IDs `P04-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

Topic A03, "Database, persistence, migrations and backups". Scope: `core/state_store.py` L618 to L1901, from `count_open_positions` to `get_pending_all_products`, inclusive. Baseline commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`.

## 0. Scope and method

| ID | Statement | Label |
|---|---|---|
| P04-S001 | Helper pass (draft). Before any work, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing (clean). | FACT |
| P04-S002 | Helper pass (draft). After the work, `git rev-parse HEAD` on the clone again returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` again returned nothing. Nothing was written inside the clone; the only file written was the draft (a temporary caller-search listing briefly saved in the work area's scratch-tools folder was deleted). | FACT |
| P04-S003 | Read in full: `core/state_store.py` L618 to L1901 (the scope). Read for context only: `core/state_store.py` L1 to L617 (header, connection, `transaction()`, fetch helpers; owned by parts P01 and P03) and L3200 to L3215 (part P05's range, pointer only). | FACT |
| P04-S004 | Schema read for context only (part P02a owns it): `core/schema.sql` L42 to L381 (`signals`, `trades`, trigger `trg_trades_terminal_status_guard`, `orders`), L518 to L556 (`fm_ledger`), L605 to L645 (`eod_squareoff_log`). | FACT |
| P04-S005 | Caller sites were read at the cited lines with a few surrounding lines: `orders/eod_squareoff.py` L340 to L500 and L1736 to L1840; `orders/order_reconciler.py` L928 to L945, L1222 to L1245, L1330 to L1410, L1500 to L1575, L2612 to L2620, L4169 to L4246, L4320 to L4365, L4430 to L4510, L4566 to L4580; `orders/tgt_retry_manager.py` L286 to L362; `orders/order_placer.py` L2612 to L2626; `screening/secondary_screener.py` L598 to L630; `main.py` L1282 to L1326 and L3628 to L3960; `allocation/portfolio_allocator.py` L42, L53, L162 to L171; `orders/shadow_tracker.py` L168 to L185; `utils/startup_checks.py` L330 to L350; `orders/order_manager.py` L755 to L769; `ops_dashboard/backend/readers/db_reader.py` L28 to L42 and L270 to L300; `scripts/system_manager.py` L96 to L104; `scripts/backfill_closure_source_w8.py` L186 to L196 and L236 to L250. | FACT |
| P04-S006 | Owner topics were taken from the Master System Investigation Index, section 3 (topics A01 to A20) and Appendix A (`scripts/` crosswalk). | FACT |
| P04-S007 | Caller search: `git grep -n -w <name>` for each of the 46 method names and the 3 class constants in the range, over all tracked files of types `.py`, `.sh`, `.sql`, `.js`, `.html`, `.bat`, `.ps1`, `.service`, `.timer` and `deploy/`, excluding `tests/` and `ops_dashboard/tests/`; a second whole-repository search including documents was used only to separate documentary mentions (HISTORICAL) from code callers. | FACT |
| P04-S008 | Python's `ast` module was run from standard input with `python3 -I -` (no script file written) over the legacy source as TEXT to: map each caller line to its enclosing function; list every attribute reference to the 46 method names in non-test `.py` files; and test whether each call sits lexically inside a `with ... transaction()` block or a `try` body. No legacy code, SQL or test was executed or imported. | FACT |
| P04-S238 | Checker pass. Before and after its work, `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing; `git status --short --ignored` after the work also returned nothing. The checker kept a text-only `ast` scan script and its method list in the work area's scratch-tools folder (run with `python3 -I`); no legacy code, SQL or test was run or imported. | FACT |
| P04-S239 | Corrector pass. Before its work, `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing. After its work, `git rev-parse HEAD` again returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` again returned nothing. Nothing was written inside the clone; the corrector wrote only the corrected part file and its corrections log, and no scratch file. A first background run of the `ast` scan hung on standard input and was stopped before producing output; it wrote nothing. | FACT |
| P04-S240 | Corrector method: every non-CORRECT finding and every omission of the check was verified against the code at the baseline by reading the cited lines (`core/state_store.py` L505 to L543, L1556 to L1614, L1668 to L1686; `core/schema.sql` FOREIGN KEY lines; the caller files named in sections 7 and 8). Try and function context of caller lines was confirmed with Python's `ast` module, run from standard input with `python3 -I -` over the source as TEXT (no script file written, nothing imported or executed from the legacy code). | FACT |
| P04-S009 | The range defines 46 methods (31 read-only, 15 writing) and 3 class constants (`_EXECUTED_TRADE_STATUSES`, `_SETTLED_TRADE_STATUSES`, `_SECTOR_EXPOSURE_STATUSES`). No method name in the range is defined twice in `core/state_store.py`. | FACT |

## 1. Common mechanics used by every method in the range (pointer: part P01 owns these helpers)

| ID | Statement | Label |
|---|---|---|
| P04-S010 | Every read method calls `self.fetch_one` (`core/state_store.py` L564 to L574) or `self.fetch_all` (L576 to L586) and does not open `transaction()`. | FACT |
| P04-S011 | Connections are opened with `isolation_level=None` (L234), so a read issued outside an explicit `BEGIN` runs as its own implicit autocommit statement; two reads made one after the other by a caller are not one snapshot. | INTERPRETATION (Python `sqlite3` and SQLite semantics) |
| P04-S012 | Every write method uses exactly one `with self.transaction() as cur` block: L1122, L1331, L1358, L1386, L1422, L1521, L1571, L1598, L1621, L1644, L1661, L1671, L1785, L1810, L1858. `cancel_stale_paper_orders` names the yielded cursor `conn` (L1122). | FACT |
| P04-S013 | `transaction()` issues `BEGIN IMMEDIATE` (L531) and `COMMIT` on normal exit (L533). On an exception derived from `Exception` (`except Exception:`, L534) it attempts `ROLLBACK` (L536), ignores a ROLLBACK that itself raises `sqlite3.Error` (L537 to L540) and re-raises (L541). The cursor is closed in `finally` (L542 to L543); the connection comes from `self._get_conn()` (L524), one per thread through `threading.local` (L192). An exception not derived from `Exception` (for example `KeyboardInterrupt`, `SystemExit`) skips the ROLLBACK: only the cursor is closed, so the transaction remains open on that thread's connection until the connection ends or a later statement ends it (see S245). | FACT (code) and INTERPRETATION (Python and SQLite semantics, last sentence) |
| P04-S014 | Each write method's transaction contains exactly one write statement; `bump_tgt_retry` adds one `SELECT` after its `UPDATE` in the same transaction (L1682 to L1684). No method in the range groups two writes in one transaction. | FACT |
| P04-S015 | L618 to L1901 contain no `try`, `except`, `raise` or logging statement. Every `sqlite3` exception (constraint, trigger, foreign key, lock timeout) therefore propagates to the caller; for write methods it does so after `transaction()` has rolled back. | FACT (absence) and INTERPRETATION (propagation) |
| P04-S016 | Methods that `return cur.rowcount > 0` (or `cursor.rowcount`, or the SELECT result) do so inside the `with` block; the value is computed before `COMMIT`. If `COMMIT` raises, the exception replaces the return value. | INTERPRETATION (Python `contextmanager` semantics) |
| P04-S017 | Timestamps generated inside the range come from `_now_ist_iso()` (L70 to L74): `datetime.now(_IST).isoformat()` with `_IST` = UTC+05:30 (L67), i.e. the machine clock, not `core.time_authority` (comment L71 to L73, HISTORICAL rationale). | FACT |
| P04-S018 | Connection PRAGMAs include `busy_timeout = 30000` (L112) and the connect `timeout=30` (L236); a `BEGIN IMMEDIATE` blocked by another writer waits up to about 30 s and then raises `sqlite3.OperationalError`. No method in the range retries. | FACT (settings, no retry) and INTERPRETATION (wait-then-raise) |
| P04-S019 | The AST scan found no non-test caller that calls any of the 46 methods lexically inside a `with ... transaction()` block, and no other method in `core/state_store.py` calls them (they are only named in docstrings and comments, for example L645, L1328, L1545, L1839, L2988, L3209). A dynamic nesting (an outer transaction opened by a caller's caller on the same thread) was not traced. | FACT (lexical) and UNKNOWN / NOT ESTABLISHED (dynamic) |

## 2. Read methods: risk-engine query helpers (L613 to L1009)

| ID | Statement | Label |
|---|---|---|
| P04-S241 | The section header comment (L613 to L616) says all these helpers are read-only and issue SELECT only; the methods below issue SELECT only. | HISTORICAL (comment) and FACT (code) |

Every row of the tables in sections 2 to 5 and 7 carries its label in the Label column.

| ID | Method, lines, signature | SQL in short form | WHERE, joins, order | Returns | Label |
|---|---|---|---|---|---|
| P04-S020 | `count_open_positions(self) -> int`, L618 to L626 | `SELECT COUNT(*) AS n FROM trades` | `status IN ('OPEN','PARTIAL')` | `int(row["n"])`, 0 if no row | FACT |
| P04-S021 | `count_in_flight_orders(self) -> int`, L628 to L637 | `SELECT COUNT(*) FROM trades` | `status = 'PENDING_FILL'` | int | FACT |
| P04-S022 | `count_active_positions(self) -> int`, L639 to L656 | `SELECT COUNT(*) FROM trades` | `status IN ('OPEN','PARTIAL','PENDING_FILL')` | int | FACT |
| P04-S023 | `get_active_positions_with_identity(self) -> List[sqlite3.Row]`, L658 to L707 | `SELECT t.trade_id, t.symbol, t.status, t.strategy, o.product AS entry_product FROM trades t LEFT JOIN orders o` | join `o.trade_id = t.trade_id AND o.leg = 'ENTRY'`; `t.status IN ('OPEN','PARTIAL','PENDING_FILL')`; no ORDER BY, no DISTINCT or GROUP BY | list of rows | FACT |
| P04-S024 | `get_trades_by_status_and_symbol(self, statuses: tuple[str, ...], symbol: str) -> List[sqlite3.Row]`, L709 to L727 | `SELECT * FROM trades` | returns `[]` without a query when `statuses` is empty (L719 to L720); `symbol = ? AND status IN (<one ? per status>)`; `ORDER BY created_at DESC`; placeholders built from the tuple length, values bound | list of rows | FACT |
| P04-S025 | Class constant `_EXECUTED_TRADE_STATUSES`, L734 to L736 | — | `('PENDING_FILL','OPEN','PARTIAL','EXITING','CLOSED','CLOSED_MANUAL')` | — | FACT |
| P04-S026 | `count_trades_today(self, date_iso: str) -> int`, L738 to L756 | `SELECT COUNT(*) FROM trades` | `SUBSTR(created_at, 1, 10) = ? AND status IN (_EXECUTED_TRADE_STATUSES)` | int | FACT |
| P04-S027 | `count_executed_trades_today_for_symbol_direction(self, symbol, direction, date_iso, pipeline: str or None = None) -> int`, L758 to L822 | `SELECT COUNT(DISTINCT t.trade_id) FROM trades t LEFT JOIN orders o` | join on `o.leg = 'ENTRY'`; `t.symbol = ? AND t.direction = ? AND SUBSTR(t.created_at,1,10) = ? AND t.status IN (_EXECUTED_TRADE_STATUSES)`; plus, when `pipeline == "delivery"`, `AND (o.product IS NULL OR o.product = 'CNC')` (L808 to L809); when `pipeline == "intraday"`, `AND (o.product IS NULL OR o.product <> 'CNC')` (L810 to L811); any other value, including None, adds nothing (L807) | int | FACT |
| P04-S028 | Class constant `_SETTLED_TRADE_STATUSES`, L831 to L833 | — | `('OPEN','PARTIAL','EXITING','CLOSED','CLOSED_MANUAL')` | — | FACT |
| P04-S029 | `count_settled_trades_today(self, date_iso: str) -> int`, L835 to L853 | `SELECT COUNT(*) FROM trades` | `SUBSTR(created_at,1,10) = ? AND status IN (_SETTLED_TRADE_STATUSES)` | int | FACT |
| P04-S030 | `count_open_delivery_positions(self) -> int`, L867 to L877 | `SELECT COUNT(DISTINCT t.trade_id) FROM trades t JOIN orders o` | inner join `o.trade_id = t.trade_id AND o.leg = 'ENTRY' AND o.product = 'CNC'`; `t.status IN ('OPEN','PARTIAL','PENDING_FILL')` | int | FACT |
| P04-S031 | `count_daily_delivery_trades(self, date_iso: str) -> int`, L879 to L893 | same inner join as S030 | `SUBSTR(t.created_at,1,10) = ? AND t.status IN (_EXECUTED_TRADE_STATUSES)` | int | FACT |
| P04-S032 | `count_signals_today(self, date_iso: str) -> int`, L895 to L907 | `SELECT COUNT(*) FROM signals` | `SUBSTR(received_at,1,10) = ?` | int | FACT |
| P04-S033 | Class constant `_SECTOR_EXPOSURE_STATUSES: tuple`, L909 | — | `("PENDING_FILL","OPEN","PARTIAL")` | — | FACT |
| P04-S034 | `sector_exposure(self, sector: str, *, statuses: tuple = _SECTOR_EXPOSURE_STATUSES) -> float`, L911 to L932 | `SELECT COALESCE(SUM(margin_reserved), 0.0) AS total FROM trades` | `status IN (<one ? per status>) AND sector = ?`; no guard for an empty `statuses` tuple (contrast L719) | `float(row["total"])`, 0.0 if no row | FACT |
| P04-S035 | `has_active_position(self, symbol: str) -> bool`, L934 to L948 | `SELECT COUNT(*) FROM trades` | `symbol = ? AND status IN ('PENDING_FILL','OPEN','PARTIAL')` | `n > 0` | FACT |
| P04-S036 | `get_active_position_direction(self, symbol: str) -> Optional[str]`, L950 to L970 | `SELECT direction FROM trades` | same predicate as S035; `LIMIT 1` with no ORDER BY | `row["direction"]` or None | FACT |
| P04-S037 | `recent_trade_pnls(self, n: int, today: Optional[str] = None) -> List[float]`, L972 to L1009 | `SELECT net_pnl FROM trades` | `status IN ('CLOSED','CLOSED_MANUAL') AND net_pnl IS NOT NULL`, plus `AND SUBSTR(exit_time,1,10) = ?` when `today` is given (L988 to L998); `ORDER BY exit_time DESC LIMIT ?` | list of `float(net_pnl)` | FACT |

## 3. Read methods: EOD square-off helpers (L1011 to L1308)

| ID | Method, lines, signature | SQL in short form | WHERE, joins, order | Returns | Label |
|---|---|---|---|---|---|
| P04-S038 | `get_pending_intraday_orders(self) -> List[sqlite3.Row]`, L1015 to L1039 | `SELECT t.trade_id, t.signal_id, t.symbol, t.direction, o.order_id AS broker_order_id FROM trades t JOIN orders o` | inner join on `o.leg = 'ENTRY'`; `t.status = 'PENDING_FILL' AND o.product IN ('MIS','CO')`; `ORDER BY t.symbol` | list of rows | FACT |
| P04-S039 | `get_open_orders_for_rehydration(self) -> List[sqlite3.Row]`, L1041 to L1078 | `SELECT o.order_id, o.status, o.transaction_type, o.qty_requested, o.price, o.placed_at, t.symbol, o.trade_id, o.leg, t.order_protocol, t.direction FROM orders o JOIN trades t` | `o.status IN ('PENDING','SUBMITTED','OPEN','PARTIAL','TRIGGER_PENDING')`; no condition on `trades.status`; `ORDER BY o.placed_at` | list of rows | FACT |
| P04-S040 | `get_orphaned_pending_trades(self) -> List[sqlite3.Row]`, L1080 to L1111 | `SELECT t.trade_id, t.symbol, t.direction, t.created_at, t.status FROM trades t LEFT JOIN orders o` | join on `o.leg = 'ENTRY'`; `t.status = 'PENDING' AND (o.order_id IS NULL OR o.order_id = '')`; `ORDER BY t.created_at`; no DISTINCT | list of rows | FACT |
| P04-S041 | `get_pending_exit_orders_for_open_positions(self) -> List[sqlite3.Row]`, L1135 to L1168 | `SELECT t.trade_id, t.symbol, o.leg, o.variety, o.order_id FROM trades t JOIN orders o JOIN orders e` | `o.trade_id = t.trade_id`; `e.trade_id = t.trade_id AND e.leg = 'ENTRY'`; `t.status IN ('OPEN','PARTIAL') AND e.product IN ('MIS','CO') AND o.leg IN ('SL','TGT') AND o.status NOT IN ('COMPLETE','CANCELLED','REJECTED','FAILED')`; `ORDER BY t.symbol, o.leg` | list of rows | FACT |
| P04-S042 | `get_open_mis_exit_orders_for_symbol(self, symbol: str) -> List[sqlite3.Row]`, L1170 to L1205 | same columns and joins as S041 | `t.symbol = ? AND t.status IN ('OPEN','PARTIAL') AND e.product = 'MIS' AND o.product = 'MIS' AND o.leg IN ('SL','TGT') AND o.status NOT IN ('COMPLETE','CANCELLED','REJECTED','FAILED')`; `ORDER BY o.leg` | list of rows | FACT |
| P04-S043 | `get_open_intraday_positions(self) -> List[sqlite3.Row]`, L1207 to L1250 | `SELECT t.trade_id, t.signal_id, t.symbol, t.direction, t.qty_filled, t.order_protocol, o.order_id AS entry_broker_order_id, o.variety AS entry_variety FROM trades t JOIN orders o` | inner join on `o.leg = 'ENTRY'`; `t.status IN ('OPEN','PARTIAL') AND t.qty_filled > 0 AND o.product IN ('MIS','CO')`; `GROUP BY t.trade_id ORDER BY t.symbol` | list of rows | FACT |
| P04-S044 | `sum_fm_ledger_margin_delta(self, reservation_id: str) -> float`, L1252 to L1279 | `SELECT COALESCE(SUM(margin_delta), 0.0) AS s FROM fm_ledger` | `reservation_id = ?`; no `entry_type` filter (docstring L1263 to L1266 says this is deliberate, HISTORICAL) | `float(row["s"])`, 0.0 if row is None | FACT (SQL) and HISTORICAL (docstring rationale) |
| P04-S045 | `get_reservation_id_for_signal(self, signal_id: str) -> Optional[str]`, L1281 to L1298 | `SELECT reservation_id FROM fm_ledger` | `signal_id = ? AND entry_type = 'RESERVE' AND reservation_id IS NOT NULL`; `ORDER BY ledger_id DESC LIMIT 1`; no check for later rows of other entry types | `row["reservation_id"]` or None | FACT |
| P04-S046 | `get_eod_squareoff_log_for_date(self, date_iso: str) -> Optional[sqlite3.Row]`, L1300 to L1308 | `SELECT * FROM eod_squareoff_log` | `fired_date = ?` (fetch_one) | row or None | FACT |

## 4. Read methods: reconciler and TGT-retry helpers (L1428 to L1900)

| ID | Method, lines, signature | SQL in short form | WHERE, joins, order | Returns | Label |
|---|---|---|---|---|---|
| P04-S047 | `get_all_open_trades(self) -> List[sqlite3.Row]`, L1432 to L1466 | `SELECT t.trade_id, t.signal_id, t.symbol, t.direction, t.qty_planned, t.qty_filled, t.status, t.sl_initial, t.entry_target_price, t.entry_actual_price, t.reservation_id, o.product, o.order_id AS entry_broker_order_id FROM trades t LEFT JOIN orders o` | join on `o.leg = 'ENTRY'`; `t.status IN ('OPEN','PARTIAL')`; `ORDER BY t.symbol`; no DISTINCT. The docstring column list (L1436 to L1440) omits `reservation_id`, which the SQL returns (L1456). | list of rows | FACT |
| P04-S048 | `get_stuck_exiting_trades(self, older_than_iso: str) -> List[sqlite3.Row]`, L1468 to L1508 | same columns and LEFT JOIN as S047 | `t.status = 'EXITING' AND t.updated_at <= ?` (text comparison); `ORDER BY t.symbol` | list of rows | FACT |
| P04-S049 | `get_tgt_retry_candidates(self) -> List[sqlite3.Row]`, L1687 to L1699 | `SELECT trade_id, symbol, tgt_retry_count, tgt_last_retry_at FROM trades` | `needs_tgt_retry = 1 AND status IN ('OPEN','PARTIAL')`; `ORDER BY tgt_last_retry_at` | list of rows | FACT |
| P04-S050 | `get_trade_for_tgt_retry(self, trade_id: str) -> Optional[sqlite3.Row]`, L1701 to L1729 | `SELECT t.trade_id, t.signal_id, t.symbol, t.direction, t.qty_filled, t.entry_actual_price, t.sl_initial, t.tgt_initial, t.status, t.needs_tgt_retry, t.tgt_retry_count, t.tgt_risk_reward_applied, o.product FROM trades t LEFT JOIN orders o` | join on `o.leg = 'ENTRY'`; `t.trade_id = ?`; no ORDER BY; fetch_one returns the first joined row | row or None | FACT |
| P04-S051 | `get_orders_for_trade(self, trade_id: str) -> List[sqlite3.Row]`, L1731 to L1748 | `SELECT order_id, leg, status, trigger_price, price, qty_requested, qty_filled FROM orders` | `trade_id = ?`; `ORDER BY leg, placed_at` | list of rows | FACT |
| P04-S052 | `get_sl_order_for_trade(self, trade_id: str) -> Optional[sqlite3.Row]`, L1750 to L1770 | `SELECT order_id, trigger_price, qty_requested FROM orders` | `trade_id = ? AND leg = 'SL' AND status NOT IN ('CANCELLED','COMPLETE','FAILED','EXPIRED','REJECTED')`; `ORDER BY placed_at DESC LIMIT 1` | row or None | FACT |
| P04-S053 | `get_pending_all_products(self) -> List[sqlite3.Row]`, L1875 to L1900 | `SELECT t.trade_id, t.signal_id, t.symbol, t.direction, o.order_id AS broker_order_id, t.reservation_id FROM trades t JOIN orders o` | inner join on `o.leg = 'ENTRY'`; `t.status = 'PENDING_FILL'`; no product filter; `ORDER BY t.symbol` | list of rows | FACT |

## 5. Write methods (all 15)

Columns: guard = the WHERE predicate; "ts" = timestamp source.

| ID | Statement | Label |
|---|---|---|
| P04-S242 | Every write method runs one `transaction()` with one write statement (S012, S014), so "atomic together" applies only within that single statement. | FACT |

| ID | Method, lines, signature | SQL in short form | Guard (WHERE) and conflict clause | Timestamps written and source | Returns | Label |
|---|---|---|---|---|---|---|
| P04-S054 | `cancel_stale_paper_orders(self, today_iso: str) -> int`, L1113 to L1133 (paper-named; see S080) | `UPDATE orders SET status = 'CANCELLED', updated_at = ?` (L1124 to L1130) | `status IN ('PENDING','SUBMITTED','OPEN','PARTIAL','TRIGGER_PENDING') AND date(placed_at) < date(?)` | `updated_at` from `_now_ist_iso()` (L1131) | `cursor.rowcount` (L1133) | FACT |
| P04-S055 | `insert_eod_squareoff_log(self, fired_date, fired_at, positions_attempted, positions_succeeded, positions_failed, cancels_attempted, cancels_succeeded, cancels_failed, duration_sec) -> None`, L1310 to L1346 | `INSERT OR REPLACE INTO eod_squareoff_log (fired_date, fired_at, positions_attempted, positions_succeeded, positions_failed, cancels_attempted, cancels_succeeded, cancels_failed, duration_sec, status, completed_at) VALUES (..., 'COMPLETE', ?)` (L1333 to L1346) | no WHERE; `OR REPLACE` resolves a conflict on the UNIQUE index `idx_eod_squareoff_log_date` on `fired_date` (`core/schema.sql` L638 to L639) | `fired_at` and `completed_at` both from the `fired_at` parameter (L1341, L1344) | None | FACT |
| P04-S056 | `insert_eod_squareoff_log_start(self, fired_date, fired_at) -> None`, L1348 to L1368 | `INSERT OR REPLACE INTO eod_squareoff_log (...) VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0.0, 'IN_PROGRESS', NULL)` (L1360 to L1368) | no WHERE; `OR REPLACE` on the same UNIQUE index | `fired_at` from parameter; `completed_at` NULL | None | FACT |
| P04-S057 | `update_eod_squareoff_log_complete(self, fired_date, positions_attempted, positions_succeeded, positions_failed, cancels_attempted, cancels_succeeded, cancels_failed, duration_sec, completed_at) -> None`, L1370 to L1406 | `UPDATE eod_squareoff_log SET <six counts>, duration_sec = ?, status = 'COMPLETE', completed_at = ?` (L1388 to L1406) | `fired_date = ?`; no predicate on the current `status`; `rowcount` is not read | `completed_at` from parameter | None (a zero-row UPDATE is not signalled) | FACT |
| P04-S058 | `update_signal_status(self, signal_id, status, reason="", ts="") -> None`, L1408 to L1426 | `UPDATE signals SET status = ?, rejection_reason = ? WHERE signal_id = ?` (L1423 to L1426) | `signal_id = ?`; no predicate on the current status; `rowcount` not read; an empty `reason` is written as NULL (L1425) | none written; `ts` is accepted and not used (comment L1413: no `updated_at` column) | None | FACT (code) and HISTORICAL (comment L1413) |
| P04-S059 | `revert_exiting_to_open(self, trade_id) -> bool`, L1510 to L1532 | `UPDATE trades SET status = 'OPEN', updated_at = ?` (L1522 to L1531) | `trade_id = ? AND status = 'EXITING'` | `updated_at` from `_now_ist_iso()` | `cur.rowcount > 0` | FACT |
| P04-S060 | `adopt_recovery_trade_to_open(self, trade_id, *, avg_fill_price=None, qty_filled=None, filled_at=None) -> bool`, L1534 to L1581 | `UPDATE trades SET status = 'OPEN', recovered_flag = 1, updated_at = ?` plus `entry_actual_price = ?` (as float) when `avg_fill_price` is not None, `qty_filled = ?` (as int) when given, `entry_time = ?` when `filled_at` is given (SET list built L1559 to L1569 from fixed literals; values bound, L1573 to L1580) | `trade_id = ? AND status IN ('UNKNOWN_IN_FLIGHT','PENDING','PENDING_FILL')` | `updated_at` from `_now_ist_iso()`; `entry_time` from the `filled_at` parameter | `cur.rowcount > 0` | FACT |
| P04-S061 | `mark_recovery_trade_exiting(self, trade_id, *, avg_fill_price: float, qty_filled: int, filled_at: str) -> bool`, L1583 to L1614 | `UPDATE trades SET status = 'EXITING', recovered_flag = 1, entry_actual_price = ?, qty_filled = ?, entry_time = ?, updated_at = ?` (L1599 to L1613) | `trade_id = ? AND status IN ('UNKNOWN_IN_FLIGHT','PENDING','PENDING_FILL')` | `entry_time` from parameter; `updated_at` from `_now_ist_iso()` | `cur.rowcount > 0` | FACT |
| P04-S062 | `fail_recovery_trade(self, trade_id) -> bool`, L1616 to L1632 | `UPDATE trades SET status = 'FAILED', updated_at = ?` (L1622 to L1631) | `trade_id = ? AND status IN ('UNKNOWN_IN_FLIGHT','PENDING')` (PENDING_FILL not included) | `updated_at` from `_now_ist_iso()` | `cur.rowcount > 0` | FACT |
| P04-S063 | `mark_needs_tgt_retry(self, trade_id) -> bool`, L1639 to L1656 | `UPDATE trades SET needs_tgt_retry = 1, tgt_retry_count = 0, tgt_last_retry_at = ?, updated_at = ?` (L1645 to L1655) | `trade_id = ?`; no status predicate | `tgt_last_retry_at` and `updated_at` each from a separate `_now_ist_iso()` call (L1654) | `cur.rowcount > 0` | FACT |
| P04-S064 | `clear_needs_tgt_retry(self, trade_id) -> bool`, L1658 to L1666 | `UPDATE trades SET needs_tgt_retry = 0, updated_at = ?` (L1662 to L1665); `tgt_retry_count` untouched | `trade_id = ?`; no status predicate | `updated_at` from `_now_ist_iso()` | `cur.rowcount > 0` | FACT |
| P04-S065 | `bump_tgt_retry(self, trade_id) -> int`, L1668 to L1685 | `UPDATE trades SET tgt_retry_count = tgt_retry_count + 1, tgt_last_retry_at = ?, updated_at = ?` (L1672 to L1681), then `SELECT tgt_retry_count FROM trades WHERE trade_id = ?` in the same transaction (L1682 to L1684) | `trade_id = ?`; no status predicate | both from `_now_ist_iso()` (L1680) | the new count as int, 0 if the row is absent (L1685) | FACT |
| P04-S066 | `set_trade_closure_axes(self, trade_id, closure_source: Optional[str], exit_mechanism: Optional[str] = None) -> None`, L1772 to L1792 | `UPDATE trades SET closure_source = COALESCE(closure_source, ?), exit_mechanism = COALESCE(exit_mechanism, ?)` (L1786 to L1791) | `trade_id = ?`; no status predicate; no `closure_source IS NULL` predicate | none (`updated_at` is not written) | None | FACT |
| P04-S067 | `mark_trade_manually_closed(self, trade_id) -> bool`, L1794 to L1822 | `UPDATE trades SET status = 'CLOSED_MANUAL', exit_reason = 'MANUAL', updated_at = ?` (L1811 to L1821) | `trade_id = ? AND status IN ('OPEN','PARTIAL','EXITING')` | `updated_at` from `_now_ist_iso()` | `cur.rowcount > 0` | FACT |
| P04-S068 | `record_manual_close_financials(self, trade_id, exit_price: float, net_pnl: float, exit_time: Optional[str] = None, charges: float = 0.0, gross_pnl: Optional[float] = None) -> bool`, L1824 to L1873 | `ts = exit_time or _now_ist_iso()` (L1856); `_gross = net_pnl` when `gross_pnl` is None (L1857); `UPDATE trades SET exit_price = ?, exit_time = COALESCE(exit_time, ?), gross_pnl = ?, charges = ?, net_pnl = ?, updated_at = ?` (L1861 to L1871) | `trade_id = ? AND status = 'CLOSED_MANUAL'` | `exit_time` (only if NULL) and `updated_at` both bound to `ts`, i.e. the `exit_time` parameter when given, else `_now_ist_iso()` (L1871) | `cur.rowcount > 0` | FACT |
| P04-S069 | No method in the range uses `INSERT OR IGNORE` or `ON CONFLICT`; the only conflict clause is `INSERT OR REPLACE` in S055 and S056. | — | — | — | — | FACT |
| P04-S070 | Under SQLite, `INSERT OR REPLACE` that meets an existing `fired_date` deletes the existing row and inserts a new one, so the `id INTEGER PRIMARY KEY AUTOINCREMENT` value (`core/schema.sql` L619) changes and every column not supplied takes its default. | — | — | — | — | INTERPRETATION (SQLite semantics) |

## 6. Interaction with schema constraints and the trigger (pointer: part P02a owns the schema)

| ID | Statement | Label |
|---|---|---|
| P04-S071 | Trigger `trg_trades_terminal_status_guard` (`core/schema.sql` L291 to L300) is `BEFORE UPDATE OF status ON trades`, fires `WHEN OLD.status IN ('CLOSED','CLOSED_MANUAL','FAILED','CANCELLED') OR OLD.status GLOB 'REJECTED*'`, and raises `RAISE(ABORT, ...)` when `NEW.status <> OLD.status`. | FACT |
| P04-S072 | The five status-writing UPDATEs on `trades` in the range (S059, S060, S061, S062, S067) restrict the from-status to non-terminal values, so no row they match can meet the trigger's WHEN condition. The other trades UPDATEs (S063 to S066, S068) do not write `status`, so the `UPDATE OF status` trigger does not fire for them. | INTERPRETATION |
| P04-S073 | The `trades.status` CHECK (`core/schema.sql` L158 to L161) permits PENDING, PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL, CANCELLED, FAILED, UNKNOWN_IN_FLIGHT and `GLOB 'REJECTED*'`; every target value written in the range (OPEN, EXITING, FAILED, CLOSED_MANUAL) is in that set. | FACT |
| P04-S074 | `update_signal_status` passes the caller's `status` through without validation; the `signals.status` CHECK (`core/schema.sql` L60 to L70) permits a fixed list plus the families `REJECTED*`, `DROPPED_*`, `SKIPPED_*`, `GATE_*`, `RETEST_*`. A value outside that set raises `sqlite3.IntegrityError`, which `transaction()` rolls back and re-raises. | FACT (code and schema) and INTERPRETATION (outcome) |
| P04-S075 | The `orders.status` CHECK (`core/schema.sql` L343 to L346) permits PENDING, SUBMITTED, OPEN, PARTIAL, COMPLETE, CANCELLED, FAILED, EXPIRED, UNKNOWN_IN_FLIGHT, `TRIGGER_PENDING` and `TRIGGER PENDING` (space form). `REJECTED` is not a permitted `orders.status` value (comment L336 to L338: broker REJECTED maps to FAILED). | FACT |
| P04-S076 | `eod_squareoff_log.status` is `TEXT NOT NULL DEFAULT 'COMPLETE'` with no CHECK (`core/schema.sql` L634); `fired_date` has a UNIQUE index (L638 to L639). | FACT |
| P04-S077 | `fm_ledger.entry_type` has a CHECK whose set includes `'RESERVE'` (`core/schema.sql` L521 to L524). | FACT |
| P04-S078 | `trades` has no `product` column (`core/schema.sql` L117 to L255); every product-aware method in the range reaches the product through `orders.product` on the ENTRY leg. `orders.product` has no CHECK (L328). | FACT |
| P04-S079 | Writes in the range do not change `trades.signal_id`, `orders.trade_id`, `orders.superseded_by` or `signals.trade_id`, and do not change any parent key (`trades.trade_id`, `signals.signal_id`, `orders.order_id`). The foreign keys declared at `core/schema.sql` L78, L254, L366 and L367 are therefore not exercised by them. No table declares a foreign key to `eod_squareoff_log`, so the delete inside `INSERT OR REPLACE` (S070) meets none. | FACT (columns written; FOREIGN KEY declarations) and INTERPRETATION (SQLite foreign-key semantics) |

## 7. Non-test callers (owner topic from the index)

Column "Note": whether the call sits in a local `try` and what that handler does at storage level, where recorded; business meaning stays with the owner topic.

| ID | Method | Caller (path, line) | Function | Owner | Note | Label |
|---|---|---|---|---|---|---|
| P04-S080 | `cancel_stale_paper_orders` | `main.py` L3949 | `_main_locked` | A01 | Inside `if is_paper:` (L3948). Paper branch: not traced further (rule 7). No local try. | FACT |
| P04-S081 | `count_open_positions` | `capital/risk_engine.py` L304 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S082 | `count_in_flight_orders` | `capital/risk_engine.py` L305 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S083 | `count_active_positions` | `capital/risk_engine.py` L303 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S084 | `count_active_positions` | `main.py` L1323 | `_eod_self_exit_due` | A01 | in try L1322; exception returns `(False, -1)` (L1324 to L1325) | FACT |
| P04-S085 | `count_active_positions` | `main.py` L3640 (bound method passed as `active_count_fn`) | `_main_locked` | A01 (wiring), A18 (use) | only when `allocator_mode` is not "off" (L3633); stored at `allocation/portfolio_allocator.py` L53 and called at L169 in `PortfolioAllocator._capacity_snapshot` (exception there sets `free = self._max_open`, L170 to L171) | FACT |
| P04-S086 | `get_active_positions_with_identity` | `main.py` L1288 | `_eod_self_exit_due` | A01 | Called only when `strategy_intent_fn is not None` (L1286), inside the try at L1287. A non-list or non-tuple result raises `TypeError` (L1294 to L1298). Any exception is logged when `log` is given (L1306 to L1321), and the function falls back to `count_active_positions` at L1323 (S084). | FACT |
| P04-S087 | `get_trades_by_status_and_symbol` | `orders/order_reconciler.py` L934 (statuses `("EXITING",)`) and L938 (`("PENDING_FILL","PENDING")`) | `OrderReconciler._reconcile` | A12 | read | FACT |
| P04-S088 | `count_trades_today` | `capital/risk_engine.py` L306 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S089 | `count_trades_today` | `signals/signal_processor.py` L725 | `SignalProcessor.get_runtime_metrics` | A06 | read | FACT |
| P04-S090 | `count_executed_trades_today_for_symbol_direction` | `signals/signal_processor.py` L855 | `SignalProcessor._enforce_one_trade_per_symbol_direction` | A06 | read | FACT |
| P04-S091 | `count_settled_trades_today` | `capital/risk_engine.py` L310; `signals/signal_processor.py` L726 | `RiskEngine._approve`; `SignalProcessor.get_runtime_metrics` | A09; A06 | read | FACT |
| P04-S092 | `count_open_delivery_positions` | `capital/risk_engine.py` L318 | `RiskEngine._approve` | A09 | called only when `is_delivery_entry` (conditional expression L318) | FACT |
| P04-S093 | `count_daily_delivery_trades` | `capital/risk_engine.py` L320 | `RiskEngine._approve` | A09 | same condition (L320) | FACT |
| P04-S094 | `count_signals_today` | none in code | — | — | only a documentary mention: `docs/web_claude/03_audit_responses/trading_system_v2_audit_report.md` L2443 (HISTORICAL) | FACT (no code caller) and HISTORICAL (document mention) |
| P04-S095 | `sector_exposure` | `capital/risk_engine.py` L354 (default statuses) and L460 (`statuses=("OPEN","PARTIAL")`) | `RiskEngine._approve`; `RiskEngine._effective_sector_margin` | A09 | read | FACT |
| P04-S096 | `has_active_position` | `capital/risk_engine.py` L361 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S097 | `get_active_position_direction` | `capital/risk_engine.py` L364 | `RiskEngine._approve` | A09 | read | FACT |
| P04-S098 | `recent_trade_pnls` | `capital/risk_engine.py` L349 (`n = self._max_consec + 1`, `today=today`) | `RiskEngine._approve` | A09 | read | FACT |
| P04-S099 | `get_pending_intraday_orders` | `orders/eod_squareoff.py` L873; `scripts/eod_broker_reconcile.py` L264 | `EodSquareoff._cancel_pending_entries`; `gather_local` | A12; A12 | read; L873: no local try in `_cancel_pending_entries`, an exception propagates to its caller; L264: in try L263, exception swallowed (`pass`, L265 to L266) | FACT |
| P04-S100 | `get_open_orders_for_rehydration` | `broker/order_monitor.py` L411; `orders/order_placer.py` L803 | `OrderMonitor.rehydrate_from_store`; `OrderPlacer.rehydrate_fill_map` | A04; A10 | read; L411: in try L410, error logged and `return 0` (L412 to L416); L803: in try L802, exception logged and `return 0` (L804 to L810); both are invoked from `main.py` L3952 and L3955, after (not inside) the paper branch | FACT |
| P04-S101 | `get_orphaned_pending_trades` | `broker/order_monitor.py` L360; `orders/order_reconciler.py` L4186 | `OrderMonitor._cleanup_orphaned_pending_trades`; `OrderReconciler._recover_in_flight_entries` | A04; A12 | read; L360: in try L359, error logged and return (L361 to L365); L4186: in try L4185, exception logged and the list treated as empty (L4187 to L4189) | FACT |
| P04-S102 | `get_pending_exit_orders_for_open_positions` | `orders/eod_squareoff.py` L961 | `EodSquareoff._cancel_pending_exit_legs` | A12 | read; in try L960; CRITICAL log, returns `(0, 0, 0)` (L962 to L968) | FACT |
| P04-S103 | `get_open_mis_exit_orders_for_symbol` | `orders/mis_autosquareoff.py` L815 | `MisAutoSquareoff._execute_mis_auto_squareoff` | A12 | read; in try L814; an exception sets `outcome.state = MisState.CANCEL_FAILED` and emits a critical event (L816 to L820) | FACT |
| P04-S104 | `get_open_intraday_positions` | `orders/eod_squareoff.py` L1063 and L1834; `orders/structure_exit_manager.py` L238 | `EodSquareoff._exit_open_positions`; `EodSquareoff._check_restart_recovery` (exception gives `open_count = -1`, L1836 to L1838); `StructureExitManager._find_open_limit_triple_trade` | A12; A12; A11 | read; L1063: no local try in `_exit_open_positions`; L1834: exception gives `open_count = -1` (L1836 to L1838); L238: in try L237, error logged and `return None` (L239 to L241) | FACT |
| P04-S105 | `sum_fm_ledger_margin_delta` | `orders/order_reconciler.py` L4028 | `OrderReconciler._check7_capital_accounting_drift` | A12 | read; in try L4027; error logged and `continue` to the next reservation (L4029 to L4034) | FACT |
| P04-S106 | `get_reservation_id_for_signal` | `capital/fund_manager.py` L2002 and L2223; `orders/eod_squareoff.py` L908 | `FundManager._replay_open_trade`; `FundManager._resolve_reservation_id`; `EodSquareoff._cancel_pending_entries` | A09; A09; A12 | read; L2002 and L2223: no local try in their functions (L2002 runs inside `with self._lock`, see S243); L908: inside the per-row try L884 of `_cancel_pending_entries`, an exception is logged CRITICAL and the row counted as failed (L937 to L943) | FACT |
| P04-S107 | `get_eod_squareoff_log_for_date` | `orders/eod_squareoff.py` L1750 | `EodSquareoff._check_restart_recovery` | A12 | reads `status`; missing or NULL treated as COMPLETE (L1756 to L1761) | FACT |
| P04-S108 | `get_eod_squareoff_log_for_date` | `orders/shadow_tracker.py` L174 | `ShadowTracker.__init__` | A11 | in try L173; exception logged, row taken as None (L175 to L182); uses row presence only (L184 to L185) | FACT |
| P04-S109 | `get_eod_squareoff_log_for_date` | `utils/startup_checks.py` L338 | `detect_startup_scenario` | A01 | in try L337; exception logged as warning (L341 to L343); compares `status` (upper-cased) with COMPLETE (L346) | FACT |
| P04-S110 | `insert_eod_squareoff_log_start` | `orders/eod_squareoff.py` L364 | `EodSquareoff._fire` | A12 | in try L363; exception logged (`EOD_WRITEAHEAD_FAILED`) and the square-off proceeds (L368 to L378) | FACT |
| P04-S111 | `update_eod_squareoff_log_complete` | `orders/eod_squareoff.py` L465 | `EodSquareoff._fire` | A12 | in try L464; on exception (L476) the fallback S112 runs | FACT |
| P04-S112 | `insert_eod_squareoff_log` | `orders/eod_squareoff.py` L482 | `EodSquareoff._fire` | A12 | reached only from the `except` at L476 (S111); inner try L481; second failure logged CRITICAL `EOD_LOG_PERSIST_FAILED` (L493 to L497) | FACT |
| P04-S113 | `update_signal_status` | `signals/signal_processor.py` L435 (`"REJECTED"`, reason `"QUEUE_FULL"`), L473 (`"PLACEMENT_FAILED"`) | `SignalProcessor._process_one_safe` | A06 | both in local try blocks (L434, L472) | FACT |
| P04-S114 | `update_signal_status` | `signals/signal_processor.py` L897 (`"PROCESSING"`), L1201 (`f"REJECTED_{rej.check}"`), L1238 (`"PLACEMENT_FAILED"`) | `SignalProcessor._process_one` | A06 | L897 inside try L895; L1201 and L1238 not in a try body of that function | FACT |
| P04-S115 | `update_signal_status` | `signals/signal_processor.py` L1344 (`"RESERVED"`), L1360 (`"PROCESSED_NO_PLACER"`), L1480 (`"TIMEOUT"`), L1543 (`"PROCESSED"`) | `SignalProcessor._admit_and_place` | A06 | not in a try body of that function | FACT |
| P04-S116 | `update_signal_status` | `signals/signal_processor.py` L1662 (`f"REJECTED_{rej.check}"`), L1683 (`"PLACEMENT_FAILED"`); L1712 (`f"REJECTED_{reason}"`) | `SignalProcessor.admit_prepared`; `SignalProcessor.reject_prepared` | A06 | L1712 inside try L1711; others not in a try body | FACT |
| P04-S117 | `update_signal_status` | `signals/signal_processor.py` L2034 (`"PROCESSING"`), L2171 (`"RESERVED"`), L2186 (`"PROCESSED_NO_PLACER"`), L2278 (`"TIMEOUT"`), L2290 (`"PROCESSED"`), L2316 (`f"REJECTED_{rej.check}"`), L2345 (`"PLACEMENT_FAILED"`) | `SignalProcessor.continue_from_gate` | A06 | L2034 to L2290 inside the try opened at L2033; L2316 and L2345 not in a try body | FACT |
| P04-S118 | `update_signal_status` | `signals/signal_processor.py` L2393 (`"PROCESSING"`), L2501 (`"RESERVED"`), L2509 (`"PROCESSED_NO_PLACER"`), L2573 (`"TIMEOUT"`), L2583 (`"PROCESSED"`), L2598 (`f"REJECTED_{rej.check}"`), L2620 (`"PLACEMENT_FAILED"`) | `SignalProcessor.continue_from_retest` | A06 | L2393 to L2583 inside the try opened at L2392; L2598 and L2620 not in a try body | FACT |
| P04-S119 | `update_signal_status` | `screening/entry_gate.py` L312 (`"GATE_WAITING"`) | `EntryGate.add` | A07 | inside try L310 | FACT |
| P04-S120 | `update_signal_status` | `screening/retest_monitor.py` L349 (`"REJECTED_RETEST_DUP"`), L373 (`"RETEST_WAITING"`) | `RetestDiverter.maybe_divert` | A08 | inside try L333 | FACT |
| P04-S121 | `update_signal_status` | `screening/secondary_screener.py` L615 (`result.status`, a variable; reason = `result.rejected_step or result.status`) | `SecondaryScreener._persist` | A07 | inside try L612; followed by a separate `insert_screener_result` call at L622 (separate transaction, see part P05) | FACT |
| P04-S122 | `get_all_open_trades` | `capital/fund_manager.py` L1788 | `FundManager.rehydrate_from_open_trades` | A09 | read; no local try in `rehydrate_from_open_trades`; the call runs inside `with self._lock` (L1767), see S243 | FACT |
| P04-S123 | `get_all_open_trades` | `orders/cnc_gtt_monitor.py` L290 | `CncGttMonitor._delivery_open_trades_by_symbol` | A11 | read; exception logged (L291 to L292) | FACT |
| P04-S124 | `get_all_open_trades` | `orders/order_reconciler.py` L768; L858 and L979; L3637 | `OrderReconciler._check_cnc_overnight_positions`; `OrderReconciler._reconcile`; `OrderReconciler._refresh_unrealized_mtm` | A12 | read; L768: in try L767, warning logged and return (L769 to L773); L858, L979: no local try in `_reconcile`; L3637: in try L3636, error logged, `mark_unrealized_mtm_refreshed(available=False)` called and return (L3638 to L3642) | FACT |
| P04-S125 | `get_all_open_trades` | `scripts/eod_broker_reconcile.py` L254 | `gather_local` | A12 | read; in try L253, exception swallowed (`except Exception: pass`, L261 to L262) | FACT |
| P04-S126 | `get_stuck_exiting_trades` | `orders/order_reconciler.py` L1527 (cutoff = `now_ist()` minus `stuck_exiting_timeout_minutes`, default 30, L1524 to L1525) | `OrderReconciler._check_stuck_exiting` | A12 | read; exception logged and no action (L1528 to L1533) | FACT |
| P04-S127 | `revert_exiting_to_open` | `orders/order_reconciler.py` L1566 | `OrderReconciler._resume_exiting_to_open` | A12 | in try L1565; exception logged, `reverted` stays False | FACT |
| P04-S128 | `adopt_recovery_trade_to_open` | `orders/order_reconciler.py` L4436 | `OrderReconciler._recovery_adopt_filled` | A12 | no local try; reached via `_adopt_or_fail` (L4296), which `_recover_in_flight_entries` calls inside try L4240 | FACT |
| P04-S129 | `mark_recovery_trade_exiting` | `orders/order_reconciler.py` L4493 | `OrderReconciler._recovery_flatten_under_kill` | A12 | no local try; reached from `_recovery_adopt_filled` (L4429), same outer try as S128 | FACT |
| P04-S130 | `fail_recovery_trade` | `orders/order_reconciler.py` L4329 and L4358 | `OrderReconciler._recovery_absent`; `OrderReconciler._recovery_fail_dead` | A12 | no local try; reached via `_adopt_or_fail` (L4287, L4300), same outer try as S128 | FACT |
| P04-S131 | `mark_needs_tgt_retry` | `orders/order_placer.py` L2620 | `OrderPlacer._persist_sl_only_protected` | A10 | in try L2619; exception logged as warning | FACT |
| P04-S132 | `mark_needs_tgt_retry` | `orders/order_reconciler.py` L4461 | `OrderReconciler._recovery_adopt_filled` | A12 | in try L4460; exception logged as warning | FACT |
| P04-S133 | `clear_needs_tgt_retry` | `orders/tgt_retry_manager.py` L330, L348, L358 | `TGTRetryManager._apply_outcome` | A11 | No try in `_apply_outcome`. Its call at L322 in `_run_once_locked` is not inside a try either. An exception propagates through `run_once` (L264 to L267) to `_loop`, which catches it at L134 and records a cycle failure (L135). The remaining candidates of that cycle are skipped. | FACT |
| P04-S134 | `bump_tgt_retry` | `orders/tgt_retry_manager.py` L356 | `TGTRetryManager._apply_outcome` | A11 | as S133 | FACT |
| P04-S135 | `get_tgt_retry_candidates` | `orders/tgt_retry_manager.py` L293 | `TGTRetryManager._run_once_locked` | A11 | read; in try L292, exception logged and the cycle returns | FACT |
| P04-S136 | `get_trade_for_tgt_retry` | `orders/order_placer.py` L2679 and L3523 | `OrderPlacer.retry_tgt_for_trade`; `OrderPlacer._retry_limit_triple_exits` | A10 | read | FACT |
| P04-S137 | `get_orders_for_trade` | `orders/mis_autosquareoff.py` L963; `orders/order_placer.py` L2698; `orders/order_reconciler.py` L4576 | `MisAutoSquareoff._restore_protection_inner`; `OrderPlacer.retry_tgt_for_trade`; `OrderReconciler._backfill_entry_order_row` | A12; A10; A12 | read; the L4576 call swallows exceptions (L4579 to L4580) | FACT |
| P04-S138 | (homonym, not a caller) `OrderManager.get_orders_for_trade` | defined `orders/order_manager.py` L763 to L769; called at `orders/order_placer.py` L4249, L4492 and `orders/order_reconciler.py` L3495 | — | A10 | a separate method that issues its own `SELECT * FROM orders WHERE trade_id = ? ORDER BY placed_at` through `fetch_all`; see part P06a | FACT |
| P04-S139 | `get_sl_order_for_trade` | `orders/order_placer.py` L2690 and L3536 | `OrderPlacer.retry_tgt_for_trade`; `OrderPlacer._retry_limit_triple_exits` | A10 | read | FACT |
| P04-S140 | `get_sl_order_for_trade` | `orders/order_reconciler.py` L1001 and L2802 | `OrderReconciler._reconcile`; `OrderReconciler._check9_missing_exits` | A12 | read | FACT |
| P04-S141 | `set_trade_closure_axes` | `orders/order_reconciler.py` L1340 | `OrderReconciler._check1_manual_close` | A12 | in try L1339; exception logged as warning; `exit_mechanism` not passed | FACT |
| P04-S142 | `set_trade_closure_axes` | `scripts/backfill_closure_source_w8.py` L246 | `main` | A12 | called once per row in a loop (L245 to L246), one transaction per row, inside the try opened at L192; `exit_mechanism` not passed | FACT |
| P04-S143 | `mark_trade_manually_closed` | `orders/order_reconciler.py` L1231 | `OrderReconciler._check1_manual_close` | A12 | in try L1230; exception logged, `actually_closed` False (L1233 to L1239) | FACT |
| P04-S144 | `record_manual_close_financials` | `orders/order_reconciler.py` L1392 | `OrderReconciler._check1_manual_close` | A12 | Reached only when `entry_price and float(entry_price) > 0 and qty > 0 and intent` (L1345), and then only in the `else` branch (L1385) of the try around `self._fm.release_used` (L1365 to L1375). Own try at L1391; an exception is logged as a warning (L1400 to L1405). `exit_time` is not passed. | FACT |
| P04-S145 | `get_pending_all_products` | `orders/order_reconciler.py` L2616 | `OrderReconciler._check6_orphan_orders` | A12 | read; no local try in `_check6_orphan_orders` | FACT |

Mentions that are not calls:

| ID | Statement | Label |
|---|---|---|
| P04-S146 | Documentary or comment-only mentions found by the search are not callers: `capital/kill_switch.py` L191 and L1156, `capital/risk_engine.py` L428, L436 and L622, `orders/order_placer.py` L713, `orders/breakeven_manager.py` L401, `orders/order_reconciler.py` L930, L1124, L1262, L1512, L2381, L2656, L3338, L3530, L4001, L4256, `orders/structure_exit_manager.py` L101 and L232, `orders/mis_autosquareoff.py` L761, `orders/tgt_retry_manager.py` L14, `capital/fund_manager.py` L1072, `main.py` L1054, L1058, L1107, L1110, L1259, L2789, L2799, `reports/daily_trade_review.py` L108, `core/schema.sql` L283 and L493, `signals/signal_processor.py` L821, `allocation/portfolio_allocator.py` L42, `orders/cnc_gtt_monitor.py` L285, `orders/order_manager.py` L25 (names the homonym, S138), `ops_dashboard/backend/readers/db_reader.py` L279 to L281 (see S147); and the non-code document `docs/locked_decisions.yaml` L1461, L1463, L1547, L2268, L2990 (HISTORICAL). Log-message strings, `steps.append` labels and `action_taken` labels inside the listed callers (for example `orders/order_reconciler.py` L771, L1232, L1235, L1239, L1342, L1402, L1530, L1569, L1606, L3639, L4031, L4188, L4463, `orders/cnc_gtt_monitor.py` L292 and `main.py` L1296) are not separate calls. The AST scan of attribute references (S008) is the basis for the caller list in this section. | FACT (HISTORICAL for the document mentions) |
| P04-S147 | Two modules restate the executed-status set by value instead of calling a range method: `ops_dashboard/backend/readers/db_reader.py` L36 to L37 (`_EXECUTED_TRADE_STATES`, the same six values; its comment L33 and L279 refer to `capital/state_store.py`, a path that does not exist at the baseline, the module being `core/state_store.py`) and `scripts/system_manager.py` L103 (`_EXECUTED`, five values without PENDING_FILL; comment L101 to L102). Both are A15; their own SQL is part P06b's. | FACT |

Lock context of calls:

| ID | Statement | Label |
|---|---|---|
| P04-S243 | Three `update_signal_status` calls run lexically inside `with self._fm.portfolio_lock`: `signals/signal_processor.py` L1344 (lock L1307, `_admit_and_place`), L2171 (lock L2138, `continue_from_gate`), L2501 (lock L2474, `continue_from_retest`). `portfolio_lock` is a property returning the FundManager's `self._lock` (`capital/fund_manager.py` L426 to L441), a `threading.RLock` (L354). `get_all_open_trades` at `capital/fund_manager.py` L1788 runs inside `with self._lock` (L1767, `rehydrate_from_open_trades`), as do the `_replay_open_trade` calls at L1790, which can call `get_reservation_id_for_signal` (L2002). The `BEGIN IMMEDIATE` wait of up to about 30 s (S018) at L1344, L2171 and L2501 therefore happens while that lock is held. Lock context of the other callers (for example `RiskEngine._approve` reached from code that holds the lock) was not traced beyond the lexical level. | FACT (lexical) and INTERPRETATION (wait under lock) |

## 8. Routes (normal, error, retry, restart, partial failure)

| ID | Statement | Label |
|---|---|---|
| P04-S148 | Normal route, write methods: `BEGIN IMMEDIATE`, one statement, `COMMIT`, return (S013, S014). | FACT |
| P04-S149 | Error route: a CHECK violation, the trigger's ABORT, a foreign-key violation or a lock timeout raises inside the single statement or at `BEGIN`; `transaction()` rolls back and re-raises; no partial row change of that method survives. The method itself neither logs nor converts the error (S015). | INTERPRETATION (from S013 to S015) |
| P04-S150 | Zero-row route: a guarded UPDATE that matches nothing returns False (S059 to S064, S067, S068), 0 (S054, S065), or None with no signal (S057, S058, S066). | FACT |
| P04-S151 | Retry route: no method in the range retries; retry behaviour, where present, is in the callers (for example the TGT retry cycle in `orders/tgt_retry_manager.py`, owner A11). | FACT (absence in range) |
| P04-S152 | Restart route: a committed change persists across a process crash under WAL with `synchronous = FULL` (L108 to L109), and an uncommitted transaction is rolled back when the database is next opened. Whether any crash, restart or recovery of this kind happened at runtime is not established. | INTERPRETATION (SQLite semantics) and UNKNOWN / NOT ESTABLISHED (runtime) |
| P04-S153 | Partial-failure route across calls: callers combine several separately committed calls, so a failure or crash between them leaves the earlier commits in place. Examples: `_check1_manual_close` calls S143 (L1231), then S141 (L1340), then `fund_manager.release_used` (L1366), then S144 (L1392); `_recovery_adopt_filled` calls S128 (L4436), then `commit_adopted_entry` (L4447), then `_backfill_entry_order_row`, then S132 (L4461); `_fire` calls S110 (L364) and later S111 or S112; the W8 backfill loop (S142) commits row by row; `SecondaryScreener._persist` calls S121 then `insert_screener_result` (L622). | FACT (call order) and INTERPRETATION (effect) |
| P04-S154 | EOD write-ahead route: if `insert_eod_squareoff_log_start` fails (S110) and no row exists for the date, the later `update_eod_squareoff_log_complete` (S111) matches zero rows and returns normally without raising (S057), so the `except` at `orders/eod_squareoff.py` L476 and the fallback `insert_eod_squareoff_log` (S112) are not reached on that route. The comments at L369 to L372 and L460 to L462 and L478 to L480 state that the fallback covers a missing row. | FACT (code and comments) and INTERPRETATION (route) |
| P04-S155 | Paper/Live split: the only paper-specific method in the range is `cancel_stale_paper_orders` (S054), reached only through `if is_paper:` at `main.py` L3948 (S080). No other method in the range branches on mode; they are mode-agnostic SQL. | FACT |
| P04-S244 | Non-`sqlite3` errors inside the methods: in `adopt_recovery_trade_to_open` a `ValueError` or `TypeError` from `float(avg_fill_price)` or `int(qty_filled)` is raised before `transaction()` is entered (conversions L1561 to L1566, `with` at L1571), so no transaction is opened. The same error in `mark_recovery_trade_exiting` (conversions in the parameter tuple at L1611, inside the `with` opened at L1598) or in `bump_tgt_retry` (`int(...)` at L1685, after the UPDATE, inside the `with` opened at L1671) is raised inside the `with` block, so `transaction()` rolls back and re-raises; in `bump_tgt_retry` this would undo the increment (`tgt_retry_count` is `INTEGER NOT NULL DEFAULT 0`, `core/schema.sql` L199). In read methods such conversions (for example L626, L932, L1009, L1279) run after the read has completed. | FACT (code position) and INTERPRETATION (outcome) |

## 9. Summary

### 9.1 Tables written by this range

| ID | Table | Written by | Operation | Label |
|---|---|---|---|---|
| P04-S156 | `trades` | S059 to S068 (10 methods) | UPDATE only | FACT |
| P04-S157 | `eod_squareoff_log` | S055, S056 (INSERT OR REPLACE); S057 (UPDATE) | INSERT OR REPLACE, UPDATE | FACT |
| P04-S158 | `signals` | S058 | UPDATE | FACT |
| P04-S159 | `orders` | S054 only (paper path) | UPDATE | FACT |
| P04-S160 | No method in the range inserts into `trades`, `signals` or `orders`, and none issues DELETE (the delete inside `INSERT OR REPLACE` is SQLite's conflict handling, S070). | — | — | FACT and INTERPRETATION (S070) |

### 9.2 Tables only read by this range

| ID | Table | Read by | Label |
|---|---|---|---|
| P04-S161 | `fm_ledger` | S044, S045 | FACT |
| P04-S162 | `orders` (read; written only by the paper-path S054) | read (joined or queried) by S023, S027, S030, S031, S038 to S043, S047, S048, S050 to S053; `trades`, `signals` and `eod_squareoff_log` are both read and written by the range | FACT |

### 9.3 State transitions implemented by UPDATE statements (as written in SQL)

| ID | Table.column | From (WHERE) | To (SET) | Method | Label |
|---|---|---|---|---|---|
| P04-S163 | `trades.status` | `'EXITING'` | `'OPEN'` | `revert_exiting_to_open` L1522 to L1531 | FACT |
| P04-S164 | `trades.status` | `'UNKNOWN_IN_FLIGHT'`, `'PENDING'`, `'PENDING_FILL'` | `'OPEN'`, with `recovered_flag = 1` | `adopt_recovery_trade_to_open` L1559 to L1580 | FACT |
| P04-S165 | `trades.status` | `'UNKNOWN_IN_FLIGHT'`, `'PENDING'`, `'PENDING_FILL'` | `'EXITING'`, with `recovered_flag = 1` | `mark_recovery_trade_exiting` L1599 to L1613 | FACT |
| P04-S166 | `trades.status` | `'UNKNOWN_IN_FLIGHT'`, `'PENDING'` | `'FAILED'` | `fail_recovery_trade` L1622 to L1631 | FACT |
| P04-S167 | `trades.status` | `'OPEN'`, `'PARTIAL'`, `'EXITING'` | `'CLOSED_MANUAL'`, with `exit_reason = 'MANUAL'` | `mark_trade_manually_closed` L1811 to L1821 | FACT |
| P04-S168 | `trades.needs_tgt_retry` | any (no status predicate) | `1`, with `tgt_retry_count = 0` | `mark_needs_tgt_retry` L1645 to L1655 | FACT |
| P04-S169 | `trades.needs_tgt_retry` | any | `0` | `clear_needs_tgt_retry` L1662 to L1665 | FACT |
| P04-S170 | `trades.tgt_retry_count` | any value n | n + 1 | `bump_tgt_retry` L1672 to L1681 | FACT |
| P04-S171 | `trades.closure_source`, `trades.exit_mechanism` | NULL (per column, via COALESCE) | the supplied value; a non-NULL value is kept | `set_trade_closure_axes` L1786 to L1791 | FACT |
| P04-S172 | `trades` exit financials (`exit_price`, `gross_pnl`, `charges`, `net_pnl`; `exit_time` only if NULL) | rows with `status = 'CLOSED_MANUAL'` | supplied values; `status` unchanged | `record_manual_close_financials` L1861 to L1871 | FACT |
| P04-S173 | `orders.status` | `'PENDING'`, `'SUBMITTED'`, `'OPEN'`, `'PARTIAL'`, `'TRIGGER_PENDING'` with `date(placed_at) < date(today)` | `'CANCELLED'` | `cancel_stale_paper_orders` L1124 to L1130 (paper path) | FACT |
| P04-S174 | `eod_squareoff_log.status` | any existing row for the date, or none | `'IN_PROGRESS'` (by replacement) | `insert_eod_squareoff_log_start` L1360 to L1368 | FACT |
| P04-S175 | `eod_squareoff_log.status` | any existing row for the date, or none | `'COMPLETE'` (by replacement) | `insert_eod_squareoff_log` L1333 to L1346 | FACT |
| P04-S176 | `eod_squareoff_log.status` | any value (no status predicate) on the row for the date | `'COMPLETE'` | `update_eod_squareoff_log_complete` L1388 to L1406 | FACT |
| P04-S177 | `signals.status` | any value (no status predicate) | the caller-supplied value; `rejection_reason` set to the reason or NULL | `update_signal_status` L1423 to L1426 | FACT |

### 9.4 Status sets used by the read predicates (for comparison only)

| ID | Set | Values | Used by | Label |
|---|---|---|---|---|
| P04-S178 | trades: OPEN, PARTIAL | 2 | S020, S041, S042, S043, S047, S049, S095 (L460 call) | FACT |
| P04-S179 | trades: PENDING_FILL, OPEN, PARTIAL | 3 | S022, S023, S030, S033 (default of S034), S035, S036 | FACT |
| P04-S180 | trades: executed set | PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL | S026, S027, S031 | FACT |
| P04-S181 | trades: settled set | OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL | S029 | FACT |
| P04-S182 | trades: single values | PENDING_FILL (S021, S038, S053); PENDING (S040); EXITING (S048); CLOSED and CLOSED_MANUAL (S037) | as listed | FACT |
| P04-S183 | trades statuses permitted by the CHECK but named in no read predicate of the range: UNKNOWN_IN_FLIGHT, CANCELLED, FAILED, `REJECTED*`. Within the range's `trades` SQL, UNKNOWN_IN_FLIGHT appears only in UPDATE guards (S060 to S062) and FAILED only as an UPDATE target (S062). CANCELLED and `REJECTED*` appear in no `trades` SQL of the range. S024 accepts caller-supplied statuses, but its two callers pass only EXITING, PENDING_FILL and PENDING (S087). | — | — | FACT |
| P04-S184 | orders, IN-list form: PENDING, SUBMITTED, OPEN, PARTIAL, TRIGGER_PENDING | 5 | S039, S054 | FACT |
| P04-S185 | orders, NOT IN form: COMPLETE, CANCELLED, REJECTED, FAILED | 4 | S041, S042 | FACT |
| P04-S186 | orders, NOT IN form: CANCELLED, COMPLETE, FAILED, EXPIRED, REJECTED | 5 | S052 | FACT |

### 9.5 ENTRY-leg joins and row multiplicity

| ID | Statement | Label |
|---|---|---|
| P04-S187 | Methods that join `orders` on `leg = 'ENTRY'` de-duplicate in three ways: `COUNT(DISTINCT t.trade_id)` (S027, S030, S031); `GROUP BY t.trade_id` (S043); nothing (S023, S038, S040, S041, S042, S047, S048, S050, S053). | FACT |
| P04-S188 | Inner joins (S030, S031, S038, S041, S042, S043, S053) drop trades that have no ENTRY row; LEFT joins (S023, S027, S040, S047, S048, S050) keep them with NULL order columns; S027 lets a NULL product match both pipelines (L809, L811). | FACT |
| P04-S189 | With several ENTRY rows for one trade, the methods without de-duplication return one row per ENTRY row; S043's `GROUP BY` returns one row per trade, with `o.order_id` and `o.variety` taken from an arbitrary row of the group (SQLite bare-column rule); S050 (`fetch_one`, no ORDER BY) returns whichever joined row comes first. | INTERPRETATION (SQLite semantics) |
| P04-S190 | The file states the ENTRY multiplicity two ways: L681 to L686 say no trade has more than one ENTRY order (a measurement "on the live book"), while L802 to L804 and L859 say SCALE mode writes several ENTRY legs (`leg_index` 0, 1, 2), as does the schema comment at `core/schema.sql` L323. | HISTORICAL |

## Concerns for the AUDIT (neutral)

| ID | What the code does, where | Label |
|---|---|---|
| P04-S191 | `update_eod_squareoff_log_complete` (L1386 to L1406) does not read `rowcount`; the caller's fallback to `insert_eod_squareoff_log` (`orders/eod_squareoff.py` L476 to L497) is entered only on an exception, while the comments at L369 to L372 and L478 to L480 describe it as covering a missing row (S154). | FACT |
| P04-S192 | `insert_eod_squareoff_log_start` (L1358 to L1368) uses `INSERT OR REPLACE`; a call for a date that already has a COMPLETE row replaces it with an IN_PROGRESS row with zero counts and a new `id` (S070); the docstring (L1355 to L1356) describes this as overwriting a prior IN_PROGRESS row. | FACT and INTERPRETATION |
| P04-S193 | `set_trade_closure_axes` docstring (L1781 to L1783) says it is guarded to rows whose `closure_source IS NULL`; the SQL (L1786 to L1791) has no such predicate and applies COALESCE per column, so `exit_mechanism` can be filled on a row whose `closure_source` is already set; it has no status predicate and does not write `updated_at`. | FACT |
| P04-S194 | `record_manual_close_financials` binds `updated_at` to `ts`, which is the `exit_time` argument when one is passed (L1856, L1871), not the time of the write; on a repeat call it overwrites `exit_price`, `gross_pnl`, `charges` and `net_pnl` while keeping the first `exit_time`. The only caller passes no `exit_time` (S144). | FACT |
| P04-S195 | `mark_needs_tgt_retry`, `clear_needs_tgt_retry` and `bump_tgt_retry` have no status predicate and write `updated_at` (S063 to S065); `get_stuck_exiting_trades` measures the EXITING age from `updated_at` (L1504; docstring L1470 to L1472 calls it the moment the trade entered EXITING). | FACT |
| P04-S196 | `update_signal_status` writes NULL to `rejection_reason` whenever `reason` is empty (L1425), discards `ts` (L1413), does not read `rowcount`, and leaves status validation to the schema CHECK (S074). | FACT |
| P04-S197 | Status sets differ between read methods (9.4): for example S022 and S035 exclude PENDING, UNKNOWN_IN_FLIGHT and EXITING, whereas the executed set (S025) includes EXITING; `fail_recovery_trade` excludes PENDING_FILL while `adopt_recovery_trade_to_open` and `mark_recovery_trade_exiting` include it (S060 to S062). | FACT |
| P04-S198 | Order-status sets differ: S052 treats EXPIRED as terminal, S041 and S042 do not; S041, S042 and S052 exclude `REJECTED`, which the `orders.status` CHECK does not permit (S075); S039 and S054 omit `UNKNOWN_IN_FLIGHT` and the space form `TRIGGER PENDING` that the CHECK permits. | FACT |
| P04-S199 | ENTRY-join multiplicity and de-duplication differ between methods (S187 to S190). | FACT and INTERPRETATION |
| P04-S200 | `get_active_position_direction` uses `LIMIT 1` without ORDER BY (L966); `get_trade_for_tgt_retry` uses `fetch_one` on a LEFT JOIN without ORDER BY (L1706 to L1729). | FACT |
| P04-S201 | `sector_exposure` matches `sector = ?`, so rows with NULL `sector` are counted for no sector; it has no empty-tuple guard (SQLite accepts an empty IN list). | FACT (SQL) and INTERPRETATION (NULL and empty-list semantics) |
| P04-S202 | Day matching uses `SUBSTR(<timestamp>, 1, 10)` on `trades.created_at` (S026, S027, S029, S031), `signals.received_at` (S032) and `trades.exit_time` (S037); `get_stuck_exiting_trades` compares ISO strings lexically (L1504). Both depend on the stored format, written by code outside this range (parts P05, P06a); the paper-path S054 uses SQLite `date()`, which normalises a `+05:30` value to UTC (the file says so for another query at L3210 to L3215). | FACT and INTERPRETATION |
| P04-S203 | `get_reservation_id_for_signal` docstring (L1283 to L1284) says "most recent active reservation_id"; the SQL selects the latest RESERVE row without considering later RELEASE or COMMIT rows of that reservation (L1289 to L1295). | FACT |
| P04-S204 | The comment at L857 to L858 cites a method `get_intraday_entry_orders`, which is not defined in any `.py` file of the repository. | FACT |
| P04-S205 | `count_signals_today` (L895 to L907) has no non-test code caller (S094). | FACT |
| P04-S206 | Two A15 modules duplicate the executed-status set by value, one with a different membership (S147). | FACT |
| P04-S207 | Callers combine separately committed calls that are not atomic as a whole (S153), and the risk engine issues several count reads in sequence, each its own autocommit read (`capital/risk_engine.py` L303 to L320; S011). The docstring L644 to L650 describes a race of this kind for an earlier two-query version (HISTORICAL). | FACT and INTERPRETATION |
| P04-S208 | `_now_ist_iso` reads the machine clock directly rather than the time authority (L70 to L74), by stated design (L71 to L73). | FACT |
| P04-S245 | `transaction()` catches only `Exception` (L534); on an exception not derived from `Exception` (for example `KeyboardInterrupt`, `SystemExit`) the ROLLBACK is skipped and only the cursor is closed (L542 to L543), so the `BEGIN IMMEDIATE` stays open on that thread's connection (S013). | FACT (code) and INTERPRETATION (outcome) |
| P04-S246 | Three `update_signal_status` calls, and the FundManager rehydration reads, run while the FundManager RLock is held (S243); a write lock wait of up to about 30 s (S018) at those calls happens under that lock. | FACT (lexical) and INTERPRETATION |

## Questions about intent (OPEN QUESTION, for the project owner)

| ID | Question | Label |
|---|---|---|
| P04-S209 | Was `update_eod_squareoff_log_complete` meant to signal a missing row so that the fallback in `_fire` runs, as the comments say (S154, S191)? | OPEN QUESTION |
| P04-S210 | Which guard was intended for `set_trade_closure_axes`: the row-level `closure_source IS NULL` described in its docstring, or the per-column COALESCE that the code applies (S193)? | OPEN QUESTION |
| P04-S211 | Were the different status sets for "active", "executed", "settled" and "open" trades, and the different terminal sets for orders, intended to differ as they do (S197, S198)? | OPEN QUESTION |
| P04-S212 | Was a trade intended to have at most one ENTRY order, or several (SCALE legs) (S190)? | OPEN QUESTION |
| P04-S213 | Should `record_manual_close_financials` set `updated_at` to the write time rather than to a supplied exit time (S194)? | OPEN QUESTION |
| P04-S214 | Should `get_reservation_id_for_signal` exclude reservations already released or committed, as "active" in its docstring suggests (S203)? | OPEN QUESTION |
| P04-S215 | Is `count_signals_today` a retained but unused API (S205)? | OPEN QUESTION |

## UNKNOWN / NOT ESTABLISHED

| ID | Statement | Label |
|---|---|---|
| P04-S216 | Whether any method in the range was called at runtime, how often, with what row counts, and with what outcome: no database, log or backup survives. | UNKNOWN / NOT ESTABLISHED |
| P04-S217 | The production measurements quoted in docstrings (for example 743 trades, 148 without an ENTRY row, at L682 to L695) cannot be verified. | UNKNOWN / NOT ESTABLISHED |
| P04-S218 | Whether trades with several ENTRY rows, rows with NULL `sector`, or timestamps in a format other than IST ISO-8601 existed in the live database. | UNKNOWN / NOT ESTABLISHED |
| P04-S219 | Whether a zero-row `update_eod_squareoff_log_complete`, a lock timeout, a CHECK or trigger abort, or a crash between separately committed calls ever occurred. | UNKNOWN / NOT ESTABLISHED |
| P04-S220 | Whether any of these methods was ever called on a thread that already held an open `transaction()` (only lexical nesting was checked, S019). | UNKNOWN / NOT ESTABLISHED |
| P04-S221 | The values `result.status` can take at `screening/secondary_screener.py` L615 were not traced (literal values at L153, L221, L275, L343, L359, L454, L488, L508, L518 are `REJECTED_*` or `PASSED`; L326 and L587 pass a variable). | UNKNOWN / NOT ESTABLISHED |
| P04-S222 | Whether the paper-path `cancel_stale_paper_orders` ran (paper path out of scope). | UNKNOWN / NOT ESTABLISHED |

## Boundary handoffs (owner topic: what crosses)

| ID | Owner | What crosses | Label |
|---|---|---|---|
| P04-S223 | Part P01 (A03) | `transaction()`, `fetch_one`, `fetch_all`, per-thread connections, PRAGMAs and `_now_ist_iso`, on which every method here depends (section 1). | FACT |
| P04-S224 | Part P02a (A03) | The definitions of `signals`, `trades`, `orders`, `fm_ledger`, `eod_squareoff_log` and the trigger `trg_trades_terminal_status_guard` (section 6). | FACT |
| P04-S225 | Part P05 (A03) | The rest of the state-store API, including `insert_screener_result` (S121, S153) and the date-key note at L3200 to L3215 (S202). | FACT |
| P04-S226 | Parts P06a and P06b (A03) | Raw SQL outside the store on the same tables: `OrderManager.get_orders_for_trade` (S138); `ops_dashboard/backend/readers/db_reader.py` and `scripts/system_manager.py` (S147). | FACT |
| P04-S227 | A09 | Meaning of the counts, exposure and P&L reads in `RiskEngine._approve` and `_effective_sector_margin`; `FundManager` reads of open trades and reservation ids; the capital calls between the reconciler's store writes (`release_used`, `commit_adopted_entry`, `release_adopted_reservation`). | FACT |
| P04-S228 | A06 | The signal status values written through `update_signal_status` from `signals/signal_processor.py` and the per-day counts read there (S089 to S091, S113 to S118). | FACT |
| P04-S229 | A07 and A08 | Status values written from `screening/entry_gate.py`, `screening/secondary_screener.py` (A07) and `screening/retest_monitor.py` (A08) (S119 to S121, S221). | FACT |
| P04-S230 | A10 | Rehydration, TGT-retry and SL lookups from `orders/order_placer.py` (S100, S131, S136, S137, S139). | FACT |
| P04-S231 | A11 | `TGTRetryManager` scheduling and flag writes, `StructureExitManager`, `ShadowTracker`, `CncGttMonitor` reads (S104, S108, S123, S133 to S135). | FACT |
| P04-S232 | A12 | The reconciler's recovery, CHECK1, stuck-EXITING, orphan and drift flows; the EOD write-ahead log and square-off reads; MIS auto-square-off; `scripts/eod_broker_reconcile.py` and `scripts/backfill_closure_source_w8.py` (S087, S099, S101 to S107, S110 to S112, S124 to S130, S132, S137, S140 to S145). | FACT |
| P04-S233 | A04 | `OrderMonitor` rehydration and orphan clean-up reads (S100, S101). | FACT |
| P04-S234 | A01 | `_eod_self_exit_due` reads, the allocator wiring and the paper branch in `_main_locked`, and `detect_startup_scenario`'s read of the EOD log (S080, S084 to S086, S109). | FACT |
| P04-S235 | A18 | `PortfolioAllocator._capacity_snapshot` use of `count_active_positions` through `active_count_fn` (S085). | FACT |
| P04-S236 | A15 | The by-value duplicates of the executed-status set (S147). | FACT |
| P04-S237 | A13 | `capital/kill_switch.py` mentions `count_active_positions` in comments only (L191, L1156); no call (S146). | FACT |
