# A03 evidence: SQL outside the state store: scripts, dashboard and reports

**Status:** DRAFT — evidence for the A03 STUDY, for ChatGPT's review
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P06b, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5).
**Purpose and scope:** The SQL issued by 33 scripts, dashboard and report modules (the six A03 scripts excluded), with the table-by-table writers and readers. Statement IDs `P06b-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

| ID | Statement |
|---|---|
| P06b-S001 | FACT (helper pass): Before work, `git rev-parse HEAD` on the local read-only clone at the baseline returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no output (0 lines). The same two commands were run again after the work; the result is recorded in the last row of this table. |
| P06b-S002 | Scope: the 33 files of the coordinator's file list for this part (1 dashboard reader, 1 report, 31 scripts). The six A03 scripts are parts P09a and P09b and are not covered here. |
| P06b-S003 | Read in full: `scripts/check_vm_state.py` L1 to L202; `scripts/deploy_assert.py` L25 to L99; `scripts/eod_cleanup.py` L30 to L324; `scripts/eod_verify.py` L60 to L245; `scripts/trade_journal.py` L30 to L180; `scripts/preflight/checks/database.py` L1 to L157; `scripts/backfill_closure_source_w8.py` L55 to L320. For every other file: every function that contains an SQL statement or a store call, its connection set-up, its caller up to `main`/`_cron_main`, and its error handling (ranges are cited at each statement). `ops_dashboard/backend/readers/db_reader.py`: L1 to L120 in full; the 130 SQL-bearing functions through the text-parsing output below, with spot reads at L171 to L185, L462 to L486, L817 to L868, L944 to L962, L1170 to L1178, L1280 to L1348, L1770 to L1802, L2690 to L2705, L3429 to L3456, L3585 to L3607, L3631 to L3652, L3743 to L3757, L4059 to L4079, L4139 to L4154. |
| P06b-S004 | Context read outside the scope, only to state what a call does: `core/db_connect.py` L1 to L137; `core/state_store.py` L102, L107 to L113, L172 to L260, L357 to L455, L505 to L586 and the store methods named at each call (one-line pointers to parts P04/P05); `utils/cron_heartbeat.py` L55 to L95, L140 to L160, L176 to L210; the table definitions in `core/schema.sql` named in section 5 (column presence only; the schema is parts P02a/P02b); `core/analytics_schema.sql` L24 to L50; `scripts/preflight/autofix.py` L33 to L36; `main.py` L91 and L4073 to L4081. |
| P06b-S005 | Tools: `grep`, `sed`, `awk`, `git rev-parse`, `git status`. Text-parsing scratch scripts using Python `ast` (run with `python3 -I`, kept in the work area outside the clone): `p06b_sqlscan.py` (every call named execute, fetch_one, fetch_all, transaction, connect, StateStore, commit, rollback), `p06b_sqllits.py` (every string literal that starts like SQL), `p06b_functables.py` (table names after FROM, JOIN, INTO or UPDATE in each function, docstrings excluded), `p06b_cols.py` and `p06b_colcheck.py` (column names compared with the TEXT of `core/schema.sql` and `core/analytics_schema.sql`). No legacy code, test, SQL or shell file was executed or imported. Where this part says a statement "would raise", that is an INTERPRETATION of SQLite semantics, not an observed result. |
| P06b-S006 | Not read (security restriction): the credential-resolution code of `scripts/reconcile_positions.py` (`_resolve_credentials`, L80 to L138) beyond its file and variable names; no `.env`, token file or `config/accounts.csv` was opened. Stopped: security restriction. |
| P06b-S007 | Rule applications: tests were not consulted (rule 6). Paper branches are marked where they split and not traced (rule 7). No schedule is taken as proof that a job ran (helper rules, section 3; A16 owns schedules). |
| P06b-S008 | Terms used: RW = a connection opened without a read-only URI (SQLite may write through it); RO = a connection opened with the URI `mode=ro`. "Store" = `core.state_store.StateStore`. "Heartbeat" = `utils.cron_heartbeat.record_heartbeat`. "Txn" = how the statement is grouped into a transaction. Owner topics are from the Master System Investigation Index, Appendix A (scripts) and section 3 (`ops_dashboard/`, `reports/`: A15). |
| P06b-S009 | FACT (helper pass): After work, `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no output (0 lines). |
| P06b-S480 | FACT (checker pass, as its file states): before its work `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no output; after its work the same two commands returned the same HEAD and no output (0 lines). It ran or imported no legacy code, test, SQL or shell file; it used text-only `ast` and regular-expression scripts kept in the work area outside the clone (an SQL and DB-call scanner, an independent parse of `db_reader.py`, a coverage matcher and a column check against the schema text). For `scripts/reconcile_positions.py` it grepped only the lines that name environment variables and file paths. It reported 443 CORRECT, 20 IMPRECISE, 0 WRONG, 0 UNSUPPORTED, 0 LABEL, 0 SECURITY and 3 omissions. No process disclosure about files outside its work folder. |
| P06b-S481 | FACT (corrector pass): before the work `git rev-parse HEAD` on the clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned no output; after the work the same two commands returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and no output (0 lines). The corrector re-read the code at every finding's cited lines with `grep`, `sed` and `awk` only (`db_reader.py` L430 to L441, L505 to L540; `scripts/backfill_closure_source_w8.py` L74 to L110, L186 to L260, L298 to L316; `scripts/eod_broker_reconcile.py` L293 to L314, L356, L423 to L425; `scripts/eod_verify.py` L76 to L92, L112 to L165, L197 to L206; `scripts/fetch_fno_ban.py` L273 to L300, L325 to L360; `scripts/reconstruct_excursions.py` L62, L116 to L127, L412 to L416; `scripts/sr_detector_backfill.py` L49 to L92; `scripts/strategy_registry_officer.py` L51; `scripts/trade_journal.py` L149 to L169; `reports/daily_trade_review.py` L2895 to L2918; `scripts/system_manager.py` L1343 to L1349; `utils/cron_heartbeat.py` L55 to L95, L119, L170 to L210; every heartbeat-helper call line in the 33 files; the `db_reader` import lines under `ops_dashboard/backend/`; in `scripts/reconcile_positions.py` only the lines naming environment variables and file paths). Nothing was written to the clone; no legacy code, test, SQL or shell file was run or imported; no scratch file was written (edits were applied by a script read from standard input). |

## 1. Connection behaviour shared by many files (context; owners: parts P01 and P03)

| ID | Statement |
|---|---|
| P06b-S010 | FACT: Every `StateStore(...)` construction runs `_initialize_schema` (`core/state_store.py` L357 to L455): it calls `db_connect.init_analytics_schema` (L375); when the stored schema version is older than `EXPECTED_SCHEMA_VERSION` (45, L102) it refuses unless `allow_migrate` is true and `market_open` is false (L426 to L427); it then runs `conn.executescript(schema_sql)` unconditionally (L446). |
| P06b-S011 | FACT: No file in this part passes `allow_migrate` or `market_open` to `StateStore` (grep over the 33 files: the only match is the report key `market_open` at `reports/daily_trade_review.py` L1233, which is not a StateStore argument). INTERPRETATION: every file here that constructs a StateStore (a) executes the full `core/schema.sql` script against the trading database at open, which writes to the file (schema objects `IF NOT EXISTS` and the schema-version row; see P02b and P03) even when the script itself only reads, and (b) cannot open the database while a migration is pending (it raises `MigrationNotPermitted`). |
| P06b-S012 | FACT: Store connections use `isolation_level=None` (`core/state_store.py` L234), the PRAGMAs at L107 to L113 (including `foreign_keys = ON` and `busy_timeout = 30000`) and an ATTACH of the analytics database (L247). `transaction()` (L505 to L547) runs `BEGIN IMMEDIATE` (L531), `COMMIT` (L533) and `ROLLBACK` on any exception (L536). INTERPRETATION: `store.execute`, `store.fetch_one` and `store.fetch_all` (L549 to L586) therefore run in autocommit, one statement per implicit transaction; only `transaction()` groups statements atomically. |
| P06b-S013 | FACT: `db_connect.connect` (`core/db_connect.py` L93 to L111) opens RW with `PRAGMA busy_timeout = 30000` and calls `attach_analytics` (L52 to L64), which creates the analytics folder (L58), ATTACHes the analytics file (L59 to L61; INTERPRETATION: ATTACH creates the file if absent, as the docstring L55 also says) and sets the analytics `journal_mode = WAL` and `synchronous = FULL` (L38 to L41, L62 to L63). `db_connect.connect_readonly` (L114 to L137) opens RO with `PRAGMA query_only = ON` and no ATTACH. |
| P06b-S014 | INTERPRETATION (Python `sqlite3` semantics): a plain `sqlite3.connect(path)` without a `mode=ro` URI opens RW and creates an empty database file if the path does not exist; with the default isolation level an INSERT, UPDATE or DELETE opens an implicit transaction that persists only on `commit()`; closing without `commit()` discards it. The Python version used in production is UNKNOWN, so the exact default transaction control is not established. |
| P06b-S015 | FACT: `record_heartbeat` (`utils/cron_heartbeat.py` L55 to L95) returns False when the database path does not exist (L81 to L82); otherwise it opens a NEW StateStore (L84), calls `insert_cron_heartbeat` (L85 to L91; store method at `core/state_store.py` L3305), closes the store and swallows every exception (L94 to L95). Its default path is the relative `data_store/trading_system.db` (L61). `HeartbeatTimer.__exit__` calls it (L147); `skip_if_non_trading_day` records a `SKIPPED` heartbeat on a non-trading day (L202). Owner A16. INTERPRETATION: each heartbeat also triggers the open-time schema script described above. |
| P06b-S478 | FACT: `HeartbeatTimer.__init__` (`utils/cron_heartbeat.py` L119) and `skip_if_non_trading_day` (L179) also default to the relative path `data_store/trading_system.db` (`skip_if_non_trading_day` also defaults `config_dir` to the relative `config`, L178). Only `reports/daily_trade_review.py` (L2897 to L2917), `scripts/cron_officer.py` (L921 to L944), `scripts/system_manager.py` (L1343 to L1348) and `scripts/reconstruct_excursions.py` (L416, `db_path=DB_PATH`, a repository-root path, L62) pass their own database path to the heartbeat helper. Every other heartbeat call in this part uses the default: `scripts/eod_verify.py` L232, `scripts/eod_broker_reconcile.py` L423 to L424, `scripts/capture_metrics_baseline.py` L326, `scripts/gemini_data_integrity_check.py` L365, `scripts/gemini_premarket_brief.py` L281, `scripts/gemini_trade_coach.py` L279, `scripts/forward_shadow_record.py` L185 to L187 and L266, every `HeartbeatTimer(...)` call (8 files) and every `skip_if_non_trading_day(...)` call. INTERPRETATION: when such a script is run with `--db` (for example `scripts/eod_verify.py` L197, `scripts/eod_broker_reconcile.py` L356, `scripts/forward_shadow_record.py` L147) or from a working directory other than the repository root, its heartbeat goes to a different file from its own reads and writes, or is skipped when that relative file does not exist (`record_heartbeat` L81 to L82). |

## 2. Per-file inventory of SQL and store calls

Column "Conn" names the connection: "own StateStore" = a StateStore constructed by that script; "main.py store" = the StateStore of the trading process; "raw RW", "raw RO" = a direct `sqlite3.connect`; "dbc RW" = `db_connect.connect`; "dbc RO" = `db_connect.connect_readonly`. Every row is a FACT about the code at the cited lines unless it says otherwise.

### 2.1 `ops_dashboard/backend/readers/db_reader.py` (A15)

| ID | Statement |
|---|---|
| P06b-S016 | Open mode RO. `open_readonly_connection` (L65 to L82) opens `file:<main_db>?mode=ro` with `uri=True` and timeout 30 (L72), sets `row_factory` (L73) and `PRAGMA busy_timeout=30000` (L74); if `paths.analytics_db` is configured it ATTACHes that file as `analytics` through a `mode=ro` URI (L78) and ignores an `OperationalError` (L79 to L81). `_ro` (L85 to L91) opens one such connection per call and always closes it. No `PRAGMA query_only` is set (contrast `db_connect.connect_readonly`). |
| P06b-S017 | The main database path is `cfg["paths"]["main_db"]` (L71). At the baseline `ops_dashboard/backend/config/gui_config.yaml` L9 to L10 set `main_db` and `analytics_db` to absolute paths on a Windows development machine (values not reproduced; path selection is parts P01 and P08a). |
| P06b-S018 | The file contains no INSERT, UPDATE, DELETE, REPLACE, CREATE, ALTER or DROP literal (p06b_sqllits.py output). Its statements are SELECTs, `PRAGMA busy_timeout` (L74), `ATTACH` (L78) and a read of `PRAGMA journal_mode` (L1322 to L1323). Writes the trading database: no. INTERPRETATION: SQLite rejects any write through a `mode=ro` connection. |
| P06b-S019 | It is the only non-test file under `ops_dashboard/` that imports `sqlite3` (grep). Its callers are modules under `ops_dashboard/backend/services/` and `ops_dashboard/backend/api/` (for example `api/analytics.py` L17, `api/risk_capital.py` L13, `api/system.py` L16, `api/trading.py` L15) and `readers/config_reader.py` (L25) (grep for `db_reader` imports); they are A15's and are not traced here. |
| P06b-S020 | Helpers `_scalar` (L94 to L98) and `_count` (L101 to L103) execute a caller-supplied SQL string; the tables below are taken from the literals of each calling function. Several SQL strings are built by concatenation or `%` formatting (for example L3451, L3649, L3754) from fixed tuples in the same function. |
| P06b-S464 | FACT: Two module-level SQL fragments, `_DELIVERY_ENTRY_SQL` (L433 to L436) and `_NOT_DELIVERY_ENTRY_SQL` (L437 to L440), are `EXISTS` and `NOT EXISTS` subqueries on `orders` (`o.trade_id = t.trade_id`, `leg = 'ENTRY'`, `product = 'CNC'`); `capital_by_segment` (L508 to L509) and `strategy_capital_by_segment` (L535, L537) embed them, so both functions also read `orders`. |
| P06b-S021 | The file has 44 `except sqlite3.OperationalError` clauses (grep count); functions with such a clause return None, an empty result or skip the source on an error, the others let the error propagate to the caller. Which function does which is not listed here (A15). |

All statements in the following table are SELECT reads through `_ro(cfg)` (raw RO, autocommit read; no transaction).

| ID | Function | Function lines | Execute, `_scalar` or `_count` lines | Tables read |
|---|---|---|---|---|
| P06b-S022 | `get_schema_version` | L113 to L119 | L115 | schema_meta |
| P06b-S023 | `get_session_info` | L122 to L130 | L124 | session |
| P06b-S024 | `get_kill_switch` | L133 to L141 | L135 | kill_switch_state |
| P06b-S025 | `webhook_funnel` | L147 to L168 | L150 | webhook_audit |
| P06b-S026 | `signals_duplicate_count` | L171 to L185 | L180 | signals |
| P06b-S027 | `signals_status_family_count` | L188 to L194 | L194 | signals |
| P06b-S028 | `orders_entry_counts` | L205 to L222 | L208 | orders |
| P06b-S029 | `orders_exit_leg_filled` | L225 to L233 | L228 | orders |
| P06b-S030 | `trades_closed_counts` | L236 to L259 | L240, L246, L253 | trades |
| P06b-S031 | `daily_trades_used` | L265 to L296 | L291 | trades |
| P06b-S032 | `open_positions_count` | L299 to L306 | L302 | trades |
| P06b-S033 | `delivery_open_count` | L309 to L318 | L312 | orders, trades |
| P06b-S034 | `delivery_daily_used` | L321 to L328 | L323 | orders |
| P06b-S035 | `realized_loss_today` | L331 to L340 | L334 | fm_ledger |
| P06b-S036 | `opening_capital` | L343 to L379 | L371 | fm_ledger |
| P06b-S037 | `capital_usage` | L382 to L426 | L405, L410, L415 | fm_ledger, trades |
| P06b-S038 | `current_total_capital` | L443 to L459 | L453 | fm_ledger |
| P06b-S039 | `last_capital_sync` | L462 to L486 | L471, L477 | fm_ledger |
| P06b-S040 | `capital_by_segment` | L489 to L525 | L510, L516 | orders, trades (orders through the module-level predicates at L433 to L440) |
| P06b-S041 | `strategy_capital_by_segment` | L528 to L549 | L533 | orders, trades (orders through the module-level predicates at L433 to L440) |
| P06b-S042 | `consecutive_loss_streak` | L552 to L571 | L559 | trades |
| P06b-S043 | `strategy_trade_stats` | L577 to L610 | L584, L594 | trades |
| P06b-S044 | `strategy_signal_counts` | L613 to L621 | L616 | signals |
| P06b-S045 | `latest_config_snapshot` | L627 to L641 | L629, L636 | config_snapshots |
| P06b-S046 | `recent_events` | L644 to L652 | L647 | system_events |
| P06b-S047 | `strategy_signal_funnel` | L684 to L704 | L688 | signals |
| P06b-S048 | `webhook_by_scanner` | L707 to L725 | L710 | webhook_audit |
| P06b-S049 | `strategy_order_stats` | L728 to L750 | L735 | orders, trades |
| P06b-S050 | `strategy_perf_stats` | L753 to L787 | L761 | trades |
| P06b-S051 | `strategy_open_capital` | L790 to L801 | L794 | trades |
| P06b-S052 | `list_signals` | L817 to L868 | L864 | orders, signals, trades |
| P06b-S053 | `list_orders` | L910 to L941 | L941 | orders, trades |
| P06b-S054 | `open_positions_list` | L944 to L962 | L951 | innings, trades |
| P06b-S055 | `holdings_list` | L965 to L979 | L970 | gtt_state, trades |
| P06b-S056 | `exposure_extremes` | L986 to L1014 | L993, L999, L1005 | trades |
| P06b-S057 | `max_order_qty_today` | L1017 to L1021 | L1019 | orders |
| P06b-S058 | `entries_in_window` | L1024 to L1029 | L1027 | orders |
| P06b-S059 | `rate_limited_posts_today` | L1032 to L1037 | L1035 | webhook_audit |
| P06b-S060 | `signals_stored_count` | L1040 to L1044 | L1043 | signals |
| P06b-S061 | `strategy_reject_split` | L1051 to L1062 | L1054 | signals |
| P06b-S062 | `strategy_loss_streaks` | L1065 to L1089 | L1072 | trades |
| P06b-S063 | `open_risk_amount_sum` | L1096 to L1102 | L1099 | trades |
| P06b-S064 | `ledger_entries` | L1105 to L1114 | L1108 | fm_ledger |
| P06b-S065 | `equity_curve_points` | L1117 to L1130 | L1120 | fm_ledger |
| P06b-S066 | `pnl_summary_today` | L1133 to L1166 | L1137, L1144, L1151 | trades |
| P06b-S067 | `exposure_breakdown` | L1169 to L1197 | L1175, L1178, L1184 | trades |
| P06b-S068 | `latest_heartbeats` | L1204 to L1213 | L1207 | cron_heartbeat |
| P06b-S069 | `latest_preflight` | L1221 to L1256 | L1237, L1246 | preflight_check_results, preflight_runs |
| P06b-S070 | `preflight_autofix_events` | L1259 to L1277 | L1269 | preflight_autofix_log |
| P06b-S071 | `db_health` | L1280 to L1329 | L1312, L1315, L1322 | trades, schema_meta; PRAGMA journal_mode (read) |
| P06b-S072 | `last_successful_order` | L1332 to L1348 | L1341 | orders (selects orders.symbol; see AUDIT concerns) |
| P06b-S073 | `system_events_recent` | L1351 to L1366 | L1360 | system_events |
| P06b-S074 | `control_tower_open_findings` | L1369 to L1379 | L1372 | control_tower_findings |
| P06b-S075 | `audit_feed` | L1382 to L1454 | L1400, L1410, L1419, L1428, L1438, L1446 | control_tower_findings, eod_verification, preflight_runs, reconciliation_log, system_events, webhook_audit |
| P06b-S076 | `telegram_alerts_today` | L1457 to L1467 | L1460 | telegram_alerts |
| P06b-S077 | `slippage_rows_today` | L1474 to L1487 | L1477 | trade_slippage_log |
| P06b-S078 | `execution_log_today` | L1490 to L1502 | L1493 | order_execution_log |
| P06b-S079 | `latency_rows_today` | L1505 to L1513 | L1508 | trades |
| P06b-S080 | `statistics_bundle` | L1516 to L1547 | L1520, L1532, L1540 | innings, trade_excursions, trades |
| P06b-S081 | `config_snapshot_history` | L1550 to L1557 | L1553 | config_snapshots |
| P06b-S082 | `config_snapshot_for_date` | L1560 to L1567 | L1562 | config_snapshots |
| P06b-S083 | `system_metrics_disk_history` | L1570 to L1601 | L1595 | system_metrics (analytics: see P07) |
| P06b-S084 | `system_metrics_history` | L1604 to L1625 | L1618 | system_metrics (analytics: see P07) |
| P06b-S085 | `closed_trades_today` | L1628 to L1641 | L1632 | trades |
| P06b-S086 | `scanner_for_trades` | L1651 to L1666 | L1660 | signals, trades |
| P06b-S087 | `strategy_sltgt_hits` | L1669 to L1682 | L1673 | trades |
| P06b-S088 | `exposure_by_direction` | L1685 to L1703 | L1691 | trades |
| P06b-S089 | `profit_factor_today` | L1706 to L1718 | L1711 | trades |
| P06b-S090 | `slippage_trend_today` | L1721 to L1737 | L1726 | trade_slippage_log, trades |
| P06b-S091 | `slippage_rows_range` | L1751 to L1812 | L1801 | orders, trade_slippage_log, trades |
| P06b-S092 | `execution_rows_range` | L1815 to L1914 | L1911 | orders, signals, trades |
| P06b-S093 | `screening_latencies` | L1917 to L1961 | L1939 | screener_results |
| P06b-S094 | `signal_throughput_range` | L1964 to L1979 | L1972 | signals |
| P06b-S095 | `closed_trades_range` | L1989 to L2042 | L2041 | orders, trades |
| P06b-S096 | `trades_in_range` | L2045 to L2069 | L2069 | trades |
| P06b-S097 | `signals_scanner_funnel_range` | L2072 to L2090 | L2076 | signals |
| P06b-S098 | `strategy_signal_counts_range` | L2093 to L2101 | L2096 | signals |
| P06b-S099 | `screener_scores` | L2104 to L2119 | L2112 | screener_results |
| P06b-S100 | `signal_scores` | L2122 to L2177 | L2156, L2163 | screener_results |
| P06b-S101 | `signal_kpi_counts` | L2180 to L2226 | L2193, L2199 | signals, trades |
| P06b-S102 | `trade_story_parts` | L2229 to L2264 | L2235, L2244, L2248, L2253 | order_execution_log, orders, signals, trades |
| P06b-S103 | `webhook_by_scanner_range` | L2267 to L2281 | L2271 | webhook_audit |
| P06b-S104 | `recon_actions_for_trades` | L2284 to L2301 | L2291 | reconciliation_log |
| P06b-S105 | `order_screen_rows` | L2329 to L2359 | L2343 | orders, trades |
| P06b-S106 | `order_exec_context` | L2426 to L2445 | L2443 | order_execution_log |
| P06b-S107 | `position_screen_rows` | L2578 to L2644 | L2603 | orders, trades |
| P06b-S108 | `position_broker_exits` | L2647 to L2684 | L2672 | orders |
| P06b-S109 | `position_excursions` | L2687 to L2706 | L2703 | trade_excursions |
| P06b-S110 | `position_open_set` | L2709 to L2726 | L2719 | trades |
| P06b-S111 | `position_kpis` | L2773 to L2815 | L2795 | trades |
| P06b-S112 | `trade_recorded_slippage` | L3035 to L3060 | L3056 | order_execution_log |
| P06b-S113 | `trade_explorer_rows` | L3063 to L3181 | L3108 | orders, signals, trades |
| P06b-S114 | `audit_system_events_range` | L3304 to L3321 | L3313 | system_events |
| P06b-S115 | `audit_config_snapshots` | L3324 to L3349 | L3338 | config_snapshots |
| P06b-S116 | `audit_kill_switch` | L3352 to L3364 | L3358 | kill_switch_state |
| P06b-S117 | `audit_reconciliation_range` | L3367 to L3378 | L3371 | reconciliation_log |
| P06b-S118 | `audit_webhook_range` | L3381 to L3394 | L3387 | webhook_audit |
| P06b-S119 | `audit_control_tower_range` | L3397 to L3410 | L3401 | control_tower_findings |
| P06b-S120 | `audit_preflight_range` | L3413 to L3426 | L3417 | preflight_runs |
| P06b-S121 | `audit_retention_meta` | L3429 to L3466 | L3451 | system_events, config_snapshots, reconciliation_log, webhook_audit, control_tower_findings, preflight_runs (table names from a probes tuple, L3438 to L3447; SQL built with % formatting) |
| P06b-S122 | `tradelog_signals_range` | L3493 to L3511 | L3502 | signals |
| P06b-S123 | `tradelog_screener` | L3514 to L3539 | L3529 | screener_results |
| P06b-S124 | `tradelog_trades_range` | L3542 to L3561 | L3547 | trades |
| P06b-S125 | `tradelog_orders_range` | L3564 to L3582 | L3569 | orders, trades |
| P06b-S126 | `tradelog_execution_range` | L3585 to L3607 | L3595 | order_execution_log |
| P06b-S127 | `tradelog_recovery_range` | L3610 to L3628 | L3619 | reconciliation_log |
| P06b-S128 | `tradelog_retention` | L3631 to L3664 | L3649 | signals, trades, orders, order_execution_log, reconciliation_log (probes tuple L3639 to L3645; % formatting) |
| P06b-S129 | `tradelog_trades_by_id` | L3668 to L3685 | L3674 | trades |
| P06b-S130 | `tradelog_signals_by_id` | L3688 to L3703 | L3695 | signals |
| P06b-S131 | `syslog_events_range` | L3711 to L3722 | L3714 | system_events |
| P06b-S132 | `syslog_cron_range` | L3725 to L3740 | L3732 | cron_heartbeat |
| P06b-S133 | `syslog_retention` | L3743 to L3769 | L3754 | system_events, cron_heartbeat, reconciliation_log (probes tuple L3746 to L3750; % formatting) |
| P06b-S134 | `tradelog_orders_of_trade` | L3772 to L3783 | L3775 | orders |
| P06b-S135 | `activity_signals_today` | L3810 to L3828 | L3820 | signals |
| P06b-S136 | `activity_trade_exits` | L3831 to L3847 | L3839 | trades |
| P06b-S137 | `activity_positions_opened` | L3850 to L3862 | L3855 | trades |
| P06b-S138 | `activity_pipeline` | L3865 to L3943 | L3885, L3905 | signals, trades |
| P06b-S139 | `activity_day_counts` | L3946 to L3962 | L3955, L3957, L3960 | orders, signals, trades |
| P06b-S140 | `activity_strategy_rows` | L3965 to L4011 | L3977, L3981, L3986 | orders, signals, trades |
| P06b-S141 | `health_daily_counts` | L4014 to L4036 | L4033 | signals, trades |
| P06b-S142 | `health_strategy_daily_signals` | L4039 to L4056 | L4048 | signals |
| P06b-S143 | `activity_pulse` | L4059 to L4079 | L4077 | orders, signals, trades |
| P06b-S144 | `signals_rejected_by_status` | L4087 to L4106 | L4099 | signals |
| P06b-S145 | `position_reconciliation_latest` | L4109 to L4126 | L4120 | position_reconciliation |
| P06b-S146 | `position_reconciliation_timeline` | L4129 to L4154 | L4139, L4146 | position_reconciliation |
| P06b-S147 | `holdings_system_rows` | L4157 to L4186 | L4174 | orders, trades |
| P06b-S148 | `config_snapshot_trail` | L4197 to L4205 | L4200 | config_snapshots |

### 2.2 `reports/daily_trade_review.py` (A15)

| ID | Statement |
|---|---|
| P06b-S149 | Open: own StateStore `StateStore(db_path)` at L2905 (RW; `--db` default `data_store/trading_system.db`, L2867, relative to the working directory), only after the holiday check (L2889 to L2900) and a database-exists check (L2902 to L2904); `store.close()` in `finally` (L2920). |
| P06b-S150 | No write literal exists in the file. Trading-database writes happen only through the open-time schema script (section 1) and heartbeats: L2897 (non-trading day, only if the file exists), L2911 (success) and L2915 (failure; the exception is then re-raised, L2918). |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S151 | L349 to L351 | `_load_min_score` | config_snapshots | SELECT | `config_json` for `snapshot_date = ?`, latest `snapshot_ts` | autocommit read | own StateStore (`fetch_one`) |
| P06b-S152 | L378 to L379 | `build_records` | trade_slippage_log | SELECT | all columns, `trade_date = ?` | autocommit read | own StateStore (`fetch_all`) |
| P06b-S153 | L391 to L393 | `build_records` | sr_detector_results | SELECT | all columns, `signal_id IN (...)`, ORDER BY `created_at` | autocommit read | own StateStore |
| P06b-S154 | L809 to L811 | `build_signal_records` | webhook_audit | SELECT | COUNT and SUMs for `date = ?` | autocommit read | own StateStore |
| P06b-S155 | L1005 (run by `_latest` L1002 to L1004) | `build_reconciliation` | signals | SELECT | `MAX(received_at)` for the date | autocommit read | own StateStore |
| P06b-S156 | L1006 | `build_reconciliation` | trades | SELECT | `MAX(updated_at)` for trades created on the date | autocommit read | own StateStore |
| P06b-S157 | L1007 | `build_reconciliation` | fm_ledger | SELECT | `MAX(ts)` for `date = ?` | autocommit read | own StateStore |
| P06b-S158 | L1042 to L1043 | `build_reconciliation` | fm_ledger | SELECT | first `INIT` `balance_after` of the date | autocommit read | own StateStore |
| P06b-S159 | L1045 to L1046 | `build_reconciliation` | fm_ledger | SELECT | `SUM(pnl_delta)` of `RELEASE_USED` rows of the date | autocommit read | own StateStore |
| P06b-S160 | L1194 to L1197 | `build_config_data` | config_snapshots | SELECT | full row (id, date, ts, account, mode, trade type, hash, json), latest for the date | autocommit read | own StateStore |
| P06b-S161 | L1430 to L1433 | `_build_t5_ranking` | trades | SELECT | distinct created dates up to the date | autocommit read | own StateStore |
| P06b-S162 | L1441 to L1443 | `_build_t5_ranking` | trade_slippage_log | SELECT | `trade_id`, `actual_rr` in a date range | autocommit read | own StateStore |
| P06b-S163 | L1449 to L1453 | `_build_t5_ranking` | trades | SELECT | closed trades (`CLOSED`, `CLOSED_MANUAL`) with `net_pnl` in a range | autocommit read | own StateStore |
| P06b-S164 | L1780 to L1782 | `_slip_tiers_for_date` | config_snapshots | SELECT | `config_json`, latest for the date | autocommit read | own StateStore |
| P06b-S165 | L1796 to L1797 | `build_slippage_data` | trade_slippage_log | SELECT | all columns, `trade_date = ?` | autocommit read | own StateStore |
| P06b-S166 | L1862 to L1864 | `build_slippage_data` | trade_slippage_log | SELECT | last 10 distinct `trade_date` values up to the date | autocommit read | own StateStore |
| P06b-S167 | L1866 to L1868 | `build_slippage_data` | trade_slippage_log | SELECT | qty and slippage columns for one date | autocommit read | own StateStore |
| P06b-S168 | L2012 to L2014 | `_prior_trading_day` | trades | SELECT | `MAX(substr(created_at,1,10))` before the date | autocommit read | own StateStore |
| P06b-S169 | L2087 to L2089 | `build_dashboard_data` | trade_excursions | SELECT | `COUNT(DISTINCT trade_id)` for given trades | autocommit read | own StateStore |
| P06b-S170 | L2091 to L2092 | `build_dashboard_data` | config_snapshots | SELECT | existence of a snapshot for the date | autocommit read | own StateStore |
| P06b-S171 | L2169 to L2170 | `build_dashboard_data` | fm_ledger | SELECT | first `INIT` `balance_after` | autocommit read | own StateStore |
| P06b-S172 | L2172 to L2173 | `build_dashboard_data` | fm_ledger | SELECT | `SUM(pnl_delta)` of `RELEASE_USED` | autocommit read | own StateStore |
| P06b-S173 | L2175 to L2177 | `build_dashboard_data` | trades | SELECT | `SUM(net_pnl)` of closed trades created on the date | autocommit read | own StateStore |
| P06b-S174 | L2179 | `build_dashboard_data` | fm_ledger | SELECT | `MAX(balance_after)` for the date | autocommit read | own StateStore |
| P06b-S175 | L373, L791, L2414, L2564, L2707 | `build_records`, `build_signal_records`, `build_capital_data`, `build_candles_data`, `build_telegram_data` | trades | SELECT (store method `get_trades_for_date`, `core/state_store.py` L2596) | `DATE(created_at) = ?` | autocommit read | own StateStore |
| P06b-S176 | L374, L792, L2415, L2565 | same functions | orders | SELECT (`get_orders_for_date`, L2604) | `DATE(placed_at) = ?` | autocommit read | own StateStore |
| P06b-S177 | L375, L790, L2416, L2566, L2708 | same functions | signals | SELECT (`get_signals_for_date`, L2588) | `DATE(received_at) = ?` | autocommit read | own StateStore |
| P06b-S178 | L376; L382, L797; L377, L2576 | `build_records`, `build_signal_records`, `build_candles_data` | reconciliation_log (`get_reconciliation_log_for_date`, L2756); screener_results (`get_screener_results_for_date`, L2764); trade_excursions joined to trades (`get_trade_excursions_for_date`, L2781) | SELECT | by date | autocommit read | own StateStore |
| P06b-S179 | L1055; L2417 | `build_reconciliation`; `build_capital_data` | trades (`get_today_closed_pnl`, L3194); fm_ledger (`get_fm_ledger_for_date`, L2612) | SELECT | by date | autocommit read | own StateStore |
| P06b-S180 | L2570 | `build_candles_data` | candles (`get_candles_for_date`, L2772) | SELECT | analytics: see P07 | autocommit read | own StateStore (analytics ATTACH) |

### 2.3 `scripts/backfill_closure_source_w8.py` (A12)

| ID | Statement |
|---|---|
| P06b-S181 | Open: own StateStore `StateStore(db_path=str(DB_PATH))` at L191 with `DB_PATH` = `<repository root>/data_store/trading_system.db` (L66); `store.close()` in `finally` (L296). The backfill write needs `--commit` (L104); without it the script prints and returns at L227 to L229 (dry run is the default). The revert write runs on `--revert-file` alone (L106 to L107; dispatched at L195 to L196 after `_require_v45`), without `--commit`. |
| P06b-S182 | Writes the trading database: yes, `trades.closure_source` through a store method, and (revert mode) through raw SQL inside `store.transaction()`. It also writes a separate SQLite backup file and a JSON receipt (files: part P08b). |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S183 | L176 | `_require_v45` | trades | PRAGMA `table_info(trades)` | refuses with SystemExit if `closure_source` is absent (L177 to L183); never adds the column | autocommit read | own StateStore (`fetch_all`) |
| P06b-S184 | L198 and L261 (SQL L77 to L90) | `main` | trades, orders (correlated subquery) | SELECT | `CLOSED_MANUAL` trades with `GROUP_CONCAT(DISTINCT leg)` of COMPLETE orders whose leg is SL, TGT or EOD | autocommit read | own StateStore |
| P06b-S185 | L245 to L246 | `main` | trades | UPDATE (store method `set_trade_closure_axes`, `core/state_store.py` L1772 to L1792) | sets `closure_source = COALESCE(closure_source, ?)` and `exit_mechanism = COALESCE(exit_mechanism, ?)` with `exit_mechanism` passed as None, `WHERE trade_id = ?` | one `transaction()` per row | own StateStore |
| P06b-S186 | L136 to L142 | `_take_backup` | whole database; trades on the copy | backup, PRAGMA, SELECT | `src.backup(out)` (SQLite online backup API, L140) from a raw RW connection to the live file (L136) into `data_store/backups/pre_w8_backfill_<stamp>.db` (L134, L138); `PRAGMA integrity_check` (L141) and `SELECT COUNT(*) FROM trades` (L142) on the copy | not applicable | raw RW (two connections) |
| P06b-S187 | L305 to L310 | `_revert` | trades | UPDATE | `closure_source = NULL WHERE trade_id = ? AND closure_source = ?` for each receipt row whose `was` is None (L303) | one `transaction()` for all rows | own StateStore |
| P06b-S188 | L312 to L314 | `_revert` | trades | SELECT | count of `CLOSED_MANUAL` rows with a non-NULL `closure_source` | autocommit read | own StateStore |

| ID | Statement |
|---|---|
| P06b-S189 | Normal `--commit` route: refuse on a two-leg contradiction (L211 to L221) → backup (L236) → per-row writes (L245 to L246) → receipt JSON (L254) → re-read and verify against the evidence (L261 to L294); a verification mismatch returns 1 and leaves the written rows in place (L283 to L287). |
| P06b-S190 | The backup refuses (SystemExit) before any write if `integrity_check` is not `ok` (L147 to L148) or the copy holds 0 trades (L149 to L152). |
| P06b-S191 | Partial failure: each row's write commits on its own; INTERPRETATION: an exception inside the loop at L245 to L246 ends the run with the earlier rows written and no receipt, because the receipt is written only after the loop (L254). |
| P06b-S192 | Retry: the `COALESCE` guard in the store method means a re-run cannot overwrite a non-NULL `closure_source` (SQL at `core/state_store.py` L1787 to L1790). The revert is atomic (one transaction). |

### 2.4 `scripts/capture_metrics_baseline.py` (A15)

| ID | Statement |
|---|---|
| P06b-S193 | Open: dbc RW per function (`capture_snapshot` L153, `compute_daily_summary` L177 and L226, `_check_drift` L259), each closed in `finally`. |
| P06b-S194 | Every SQL statement targets analytics tables: INSERT `system_metrics` (L155 to L165, commit L166), SELECT `system_metrics` (L179 to L186), INSERT OR REPLACE `system_metrics_daily` (L228 to L247, commit L248), SELECT `system_metrics_daily` (L261 to L267). Analytics: see P07. |
| P06b-S195 | Trading-database writes: none by SQL. Heartbeat `capture_metrics_baseline` (L325 to L326, default relative path, exceptions swallowed L327 to L328) and, on a non-trading day, a SKIPPED heartbeat under the job name `capture_metrics` or `metrics_summary` (L351 to L354). |

### 2.5 `scripts/check_vm_state.py` (A15)

| ID | Statement |
|---|---|
| P06b-S196 | Open: module-level raw RW `sqlite3.connect(db_path)` (L55) with the default timeout and isolation level; `db_path` from the environment variable `DB_PATH` or `<repository root>/data_store/trading_system.db` (L47 to L50); exits if the file is absent (L51 to L53). `c.close()` at L202 is not in a `finally`. |
| P06b-S197 | The module docstring says "read-only diagnostics only" (L2; HISTORICAL) and records that a `--reset` flag that updated `kill_switch_state` was removed and is now rejected before the database is opened (L4 to L20, L29 to L41; HISTORICAL and FACT respectively). |
| P06b-S198 | Writes the trading database: yes, with raw SQL that bypasses the store methods, when run with `--cleanup-pending` or `--cleanup-orders` as the first argument. |

| ID | Lines | Gate | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S199 | L59 | always | sqlite_master | SELECT | table names | read | raw RW |
| P06b-S200 | L64 | if the table exists (L63) | kill_switch_state | SELECT | `* WHERE id=1` | read | raw RW |
| P06b-S201 | L75 to L78 | `--signals` (L73) | signals | SELECT | last 10 by `received_at` | read | raw RW |
| P06b-S202 | L87 to L90 | any `--symbol=` argument (L83 to L85) | signals | SELECT | last 5 for the symbol | read | raw RW |
| P06b-S203 | L99 to L103 | `--trades` (L97) | trades | SELECT | last 10 with `net_pnl` | read | raw RW |
| P06b-S204 | L113 to L117 | `--positions` (L111) | trades | SELECT | status not CLOSED or CANCELLED | read | raw RW |
| P06b-S205 | L129 to L132 | `--cleanup-pending` (L127) | trades | SELECT | `status = 'PENDING_FILL'` | read | raw RW |
| P06b-S206 | L136 to L140 | `--cleanup-pending` | trades | UPDATE | `status = 'CANCELLED'`, `exit_reason = 'cleanup_stale_pending'` `WHERE status = 'PENDING_FILL'`; `updated_at` not set | implicit; `c.commit()` L141 | raw RW |
| P06b-S207 | L149 to L155 | `--cleanup-orders` (L147) | orders LEFT JOIN trades | SELECT | PENDING orders whose trade is CANCELLED, CLOSED, CLOSED_MANUAL or missing | read | raw RW |
| P06b-S208 | L162 to L169 | `--cleanup-orders` | orders (subquery on trades) | UPDATE | `status = 'CANCELLED'` `WHERE status = 'PENDING' AND trade_id IN (trades in CANCELLED, CLOSED, CLOSED_MANUAL)`; `updated_at` not set | implicit; `c.commit()` L170 | raw RW |
| P06b-S209 | L179, L182, L185, L188 | `--health` (L176) | kill_switch_state, trades, signals, orders | SELECT | state; open count; signals in the last 10 minutes by `datetime('now', '-10 minutes')`; pending order count | read | raw RW |
| P06b-S210 | L194 to L198 | `--orders` (L192) | orders | SELECT | counts by order type and status | read | raw RW |

### 2.6 `scripts/compute_strategy_metrics.py` (A07)

| ID | Statement |
|---|---|
| P06b-S211 | Open: own StateStore at L310 (open failure returns 1, L311 to L313); closed at L328 (error path, then return 1) and L331. Writes skipped with `--dry-run` (gate L273). |
| P06b-S212 | Writes the trading database: yes, `strategy_metrics`. No other write: `_check_demotion` (L176 to L230) only logs and calls a notifier, and `main` passes `notifier=None` (L322). Appendix A's description "may set a strategy to PAPER_ONLY" comes from the file's own documentation (HISTORICAL); no statement in this file writes such a status. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S213 | L89 to L103 | `compute_sharpe` | trades | SELECT | daily `SUM(net_pnl)` of `CLOSED` trades of a strategy by `SUBSTR(updated_at,1,10)` range | autocommit read | own StateStore |
| P06b-S214 | L135 to L146 | `compute_win_rate` | trades | SELECT | `net_pnl` of `CLOSED` trades in range | autocommit read | own StateStore |
| P06b-S215 | L165 to L172 | `_get_active_strategies` | trades | SELECT | distinct strategy of `CLOSED` trades since a date | autocommit read | own StateStore |
| P06b-S216 | L187 to L195 | `_check_demotion` | strategy_metrics | SELECT | last N `sharpe` values of a strategy | autocommit read | own StateStore |
| P06b-S217 | L274 to L287 | `run_strategy_metrics` | strategy_metrics | INSERT OR REPLACE | `strategy, date, sharpe, win_rate, avg_pnl, total_trades, computed_at` (`computed_at` = `now_ist().isoformat()`, L244) | one `transaction()` per strategy | own StateStore |
| P06b-S218 | Route: an exception inside the loop is logged, the store closed and 1 returned (L326 to L329); INTERPRETATION: strategies processed before the exception stay written. Heartbeat through `HeartbeatTimer` (L341). | | | | | | |
| P06b-S465 | Heartbeat (FACT): `skip_if_non_trading_day("compute_strategy_metrics")` at L339 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L340). | | | | | | |

### 2.7 `scripts/cron_officer.py` (A16)

| ID | Statement |
|---|---|
| P06b-S219 | Open: own StateStore `StateStore(args.db_path)` at L905 only if the path exists (L904); `--db-path` default is the relative `data_store/trading_system.db` (L866); `store.close()` in `finally` (L946 to L948). |
| P06b-S220 | L147 (`_today_heartbeats`, L144): store method `get_cron_heartbeats_since` (cron_heartbeat SELECT, `core/state_store.py` L3327); autocommit read. |
| P06b-S221 | L350 to L351 (`_detect_mode`, L347 to L356): `SELECT mode FROM trades WHERE mode IS NOT NULL ORDER BY created_at DESC LIMIT 1`; every exception swallowed (L354 to L355), default `Live`. |
| P06b-S222 | Trading-database writes: heartbeats `cron_officer_briefing` (L921, L931) and `cron_officer_eod` `STARTED` (L938) and `SUCCESS` (L944), each skipped in dry-run; plus the open-time schema script. |

### 2.8 `scripts/deploy_assert.py` (A17)

| ID | Statement |
|---|---|
| P06b-S223 | Open mode RO: `_ro_conn` (L37 to L42) opens a `mode=ro` URI with timeout 15 and sets `PRAGMA query_only = ON` (L41). Writes: none. |
| P06b-S224 | `assert_db_integrity` (L45 to L67): `PRAGMA quick_check` (L55), `PRAGMA foreign_key_check` (L57), `SELECT value FROM schema_meta WHERE key='schema_version'` (L60 to L61) compared with `EXPECTED_SCHEMA_VERSION` imported from `core.state_store` (L28; constant import, no StateStore constructed). Connection closed in `finally` (L65 to L66). A failed blocker returns exit code 2 (L80 to L81). |

### 2.9 `scripts/eod_broker_reconcile.py` (A12)

| ID | Statement |
|---|---|
| P06b-S225 | Open: own StateStore at L358 (open failure returns 1, L359 to L361); `store.close()` at L428 on the normal path only (no `finally`). Paper split at L369 (not traced). |
| P06b-S226 | Writes the trading database: yes, `eod_broker_reconciliation` and `pnl_reconciliation`, both through store methods. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S227 | L254 | `gather_local` | trades joined to orders | SELECT (`get_all_open_trades`, `core/state_store.py` L1432) | open trades | autocommit read; exceptions swallowed (L261) | own StateStore |
| P06b-S228 | L264 | `gather_local` | trades joined to orders | SELECT (`get_pending_intraday_orders`, L1015) | pending intraday orders | autocommit read; swallowed (L265) | own StateStore |
| P06b-S229 | L268 | `gather_local` | trades | SELECT (`get_today_closed_pnl`, L3194) | realised P&L of the date | autocommit read; swallowed (L269) | own StateStore |
| P06b-S230 | L273 to L275 | `gather_local` | position_reconciliation | SELECT | `status WHERE date = ?` | autocommit read; swallowed (L279) | own StateStore |
| P06b-S231 | L393 | `main` | eod_verification | SELECT (`get_eod_verification_status`, L3293) | status of the date | autocommit read; swallowed (L394) | own StateStore |
| P06b-S232 | L445 to L451 | `_local_capital_snapshot` | fm_ledger | SELECT | latest `balance_after` by `ledger_id DESC` (the comment L446 to L449 records an earlier `ORDER BY id` that always failed; HISTORICAL) | autocommit read; swallowed (L456 to L458) | own StateStore |
| P06b-S233 | L295 to L304 | `persist` | eod_broker_reconciliation | INSERT OR REPLACE (`upsert_eod_broker_reconciliation`, L3269) | date, mode, self_consistency, authoritative, broker_reachable, five dimension statuses, overall_status, eod_verify_status, mismatch, detail (first 1000 characters), verified_at | own `transaction()` | own StateStore |
| P06b-S234 | L305 to L312 | `persist` | pnl_reconciliation | INSERT OR REPLACE (`upsert_pnl_reconciliation`, L3232) | date, broker_pnl, system_pnl, variance, status `OK` or `VARIANCE`, notes NULL, created_at; only when the broker realised P&L is not None (L305) | own `transaction()` | own StateStore |
| P06b-S235 | Route: the two upserts run in separate transactions; INTERPRETATION: an exception in the second leaves the first committed. `persist` is not wrapped: an exception propagates out of `main`, skipping the heartbeat (L421 to L426) and `store.close()` (L428). | | | | | | |
| P06b-S466 | Heartbeat (FACT): `skip_if_non_trading_day("eod_broker_reconcile")` at L472 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L473). | | | | | | |

### 2.10 `scripts/eod_cleanup.py` (A12)

| ID | Statement |
|---|---|
| P06b-S236 | Open: own StateStore at L280 (open failure returns 1); `run_eod_cleanup` (L70 to L102) runs four steps in order; an exception is logged, the store closed and 1 returned (L298 to L301); normal close L303. Heartbeat through `HeartbeatTimer` (L313). |
| P06b-S237 | Writes the trading database: yes, raw SQL inside `store.transaction()` (not the named store methods), on eight tables: signals, orders, smart_tgt_state, screener_results, gate_state, shadow_trades, sr_detector_results, retest_state. With `--dry-run` each step only counts. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S238 | L109 to L115 | `_cleanup_stale_signals` (dry run) | signals | SELECT | COUNT where `status = 'PROCESSING' AND SUBSTR(triggered_at,1,10) < ?` | autocommit read | own StateStore |
| P06b-S239 | L120 to L125 | `_cleanup_stale_signals` | signals | UPDATE | `status = 'EXPIRED'`, same predicate | one `transaction()` | own StateStore |
| P06b-S240 | L137 to L140 | `_cleanup_stale_orders` (dry run) | orders | SELECT | COUNT where status in OPEN, SUBMITTED, PENDING, TRIGGER_PENDING and `SUBSTR(placed_at,1,10) < ?` (no condition on the trade) | autocommit read | own StateStore |
| P06b-S241 | L146 to L157 | `_cleanup_stale_orders` | orders (subquery trades) | UPDATE | `status = 'CANCELLED'`, `updated_at = datetime('now','localtime')`, same status and date predicate AND trade in CLOSED, CLOSED_MANUAL, CANCELLED, FAILED | one `transaction()` with the next row | own StateStore |
| P06b-S242 | L159 to L166 | `_cleanup_stale_orders` | orders (subquery trades) | UPDATE | same SET, same predicate AND `trade_id NOT IN (SELECT trade_id FROM trades)` | same `transaction()` (L146) | own StateStore |
| P06b-S243 | L176 to L178 | `_cleanup_orphaned_smart_tgt` (dry run) | smart_tgt_state (subquery trades) | SELECT | COUNT where `trade_id NOT IN (trades in OPEN, PARTIAL)` | autocommit read | own StateStore |
| P06b-S244 | L183 to L186 | `_cleanup_orphaned_smart_tgt` | smart_tgt_state (subquery trades) | DELETE | `trade_id NOT IN (SELECT trade_id FROM trades WHERE status IN ('OPEN','PARTIAL'))` | one `transaction()` | own StateStore |
| P06b-S245 | L239 to L242 | `_cleanup_old_fingerprints` (dry run) | signals (subquery trades) | SELECT | COUNT with the predicate `where` (L234 to L236): status EXPIRED or DUPLICATE or GLOB `REJECTED*`, `fingerprint_date < cutoff`, and no trades row with that `signal_id` | autocommit read | own StateStore |
| P06b-S246 | L250 to L255 | `_cleanup_old_fingerprints` | signals | SELECT | `signal_id` with the same predicate, `LIMIT 2000` (`_PRUNE_BATCH`, L208) | per-batch `transaction()` (L250) | own StateStore |
| P06b-S247 | L260 to L263 | `_cleanup_old_fingerprints` | screener_results, gate_state, shadow_trades, sr_detector_results, retest_state (`_SIGNAL_ANALYTICS_CHILDREN`, L198 to L204) | DELETE | `signal_id IN (batch)` | same per-batch `transaction()` | own StateStore |
| P06b-S248 | L264 to L266 | `_cleanup_old_fingerprints` | signals | DELETE | `signal_id IN (batch)` | same per-batch `transaction()`; the loop repeats until a batch is empty (`break` at L257 inside the `with`) | own StateStore |

| ID | Statement |
|---|---|
| P06b-S249 | Retention window of step 4: `cutoff` = run date minus `signal_retention_days` (L215 to L217). The value comes from `--signal-retention-days` or its alias `--fingerprint-days` (L47 to L48), else configuration `system.eod_cleanup.signal_retention_days` (L61), else `EodCleanupConfig().signal_retention_days` on a configuration error (L63 to L69). The comments state a default of 90 days (L44, L54; HISTORICAL; the configured value is A02's). |
| P06b-S250 | Foreign keys referencing `signals(signal_id)` in `core/schema.sql`: trades (L254), screener_results (L693), gate_state (L797), shadow_trades (L977), sr_detector_results (L1290), retest_state (L1333) (grep). The five tables deleted at L260 to L263 plus the protected `trades` are all six. The comment at L195 to L197 says "seven children" (HISTORICAL). |
| P06b-S251 | Partial failure: INTERPRETATION: each step commits on its own, and step 4 commits per batch, so an exception leaves the earlier steps and batches committed and the later ones not run. Step 4 is a database-retention action outside `scripts/db_retention.py` (part P09b). |
| P06b-S467 | Heartbeat (FACT): `skip_if_non_trading_day("eod_cleanup")` at L311 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L312). |

### 2.11 `scripts/eod_verify.py` (A12)

| ID | Statement |
|---|---|
| P06b-S252 | Open: own StateStore at L199 (open failure returns 1); `store.close()` at L236 on the normal path only. Heartbeat `eod_verify` (L231 to L232, exceptions swallowed). Exit code 2 when the status is `ISSUES_FOUND` (L241). Paper split at L81 in `_evaluate_pnl` (mode from `--mode` or the `TRADING_MODE` environment variable, L204): in paper mode it returns before the `pnl_reconciliation` query; the trade and order counts (L117 to L128) and the `eod_verification` write (L157 to L163) in `run_eod_verification` run in both modes (paper side not traced further). |
| P06b-S253 | Writes the trading database: yes, `eod_verification`. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S254 | L84 to L88 | `_evaluate_pnl` | pnl_reconciliation | SELECT | `variance, broker_pnl WHERE date = ? ORDER BY id DESC LIMIT 1`; a query error is caught and becomes `NOT_CHECKED` (L89 to L91) | autocommit read | own StateStore |
| P06b-S255 | L117 to L121 | `run_eod_verification` | trades | SELECT | COUNT in OPEN, PARTIAL created on the date (not caught) | autocommit read | own StateStore |
| P06b-S256 | L124 to L128 | `run_eod_verification` | orders | SELECT | COUNT `PENDING` placed on the date (not caught) | autocommit read | own StateStore |
| P06b-S257 | L157 to L163 | `run_eod_verification` | eod_verification | INSERT OR REPLACE | `date, open_trades, pending_orders, pnl_variance, status, verified_at`; status `ISSUES_FOUND`, `PENDING` or `VERIFIED` (L148 to L153); `verified_at` = `now_ist().isoformat()` (L155) | one `transaction()` | own StateStore |
| P06b-S258 | Route: INTERPRETATION: an exception in either count query propagates out of `main`, so no row is written and the store is not closed explicitly. | | | | | | |
| P06b-S468 | Heartbeat (FACT): `skip_if_non_trading_day("eod_verify")` at L255 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L256). | | | | | | |

### 2.12 `scripts/fetch_daily_candles.py` (A05)

| ID | Statement |
|---|---|
| P06b-S259 | `_get_traded_symbols` (L114 to L127): raw RW `sqlite3.connect(str(DB_PATH))` (L118); `SELECT DISTINCT symbol FROM signals WHERE status = 'PROCESSED' AND date(triggered_at) = ?` (L120 to L124); `conn.close()` at L126, not in a `finally`. |
| P06b-S260 | `_insert_into_candles_db` (L294 to L326): dbc RW (L300), `INSERT OR IGNORE INTO candles` (L306 to L320), commit L324. Analytics: see P07. |
| P06b-S261 | Trading-database writes: none by SQL; heartbeats through `skip_if_non_trading_day` (L333) and `HeartbeatTimer` (L335). |

### 2.13 `scripts/fetch_fno_ban.py` (A05)

| ID | Statement |
|---|---|
| P06b-S262 | Open: own StateStore at L306 (open failure returns 1); closed at L296 (soft-fail path), L338 (dry run) and L357 (success). Writes the trading database: yes, `fno_ban`. Heartbeat through `HeartbeatTimer` (L367). |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S263 | L182 to L190 | `store_fno_ban` | fno_ban | INSERT OR REPLACE | `symbol, ban_date, fetched_at` per symbol; an exception for one symbol is logged and the loop continues (L192 to L193) | one `transaction()` per symbol | own StateStore |
| P06b-S264 | L209 to L213 | `store_fetch_failed_sentinel` | fno_ban | INSERT OR REPLACE | one sentinel symbol row for the date; called only when `fail_closed` is true (L286 to L290) | one `transaction()` | own StateStore |
| P06b-S265 | L227 to L230, L233 to L236 | `is_symbol_fno_banned` | fno_ban | SELECT | sentinel row, then the symbol's row, for a date | autocommit read | caller's store |
| P06b-S266 | No `store_fno_ban` write when the fetch fails (L331) or the CSV date differs from today (L342 to L349); both routes go to `_soft_fail`, which writes only the sentinel row, and only when `fail_closed` is true (L286 to L290). No write at all with `--dry-run` (L333 to L339, returns after printing). `is_symbol_fno_banned` and the table `fno_ban` have no non-test reader outside this file (grep); the docstring L31 says so too (HISTORICAL). | | | | | | |
| P06b-S469 | Heartbeat (FACT): `skip_if_non_trading_day("fetch_fno_ban")` at L365 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L366). | | | | | | |

### 2.14 `scripts/forward_shadow_record.py` (A18)

| ID | Statement |
|---|---|
| P06b-S267 | Open: own StateStore at L150 inside a `try`; `store.close()` in `finally` (L285). Docstring: "RECORDS ONLY" and "appends JSONL only" (L2, L10 to L11; HISTORICAL). |
| P06b-S268 | L151 to L158 (`main`): `screener_results s JOIN signals sig` with `date(s.ts) = ?`, `score` and `step_results` not NULL; autocommit read. |
| P06b-S269 | L228 to L229 (`main`): candles SELECT (analytics: see P07). L242 (`main`): `SELECT net_pnl FROM trades WHERE trade_id=?`; autocommit read. |
| P06b-S270 | L225 (`main`): `ensure_candles(store, ...)` (imported from `scripts/reconstruct_excursions.py`) may insert candles through `store.insert_candle` (analytics: see P07); skipped with `--dry-run` (L223). |
| P06b-S271 | Trading-database writes: none by SQL; heartbeats at L185 to L187 (empty day) and L266 (success), exceptions swallowed. Output JSONL is part P08b. |
| P06b-S470 | Heartbeat (FACT): `skip_if_non_trading_day("forward_shadow_record")` at L300 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L301). |

### 2.15 `scripts/gemini_data_integrity_check.py` (A15)

| ID | Statement |
|---|---|
| P06b-S272 | Open: dbc RW per function (L85, L99, L115), each closed in `finally`. Writes: none by SQL; heartbeat at L365. |
| P06b-S273 | L87 to L92 (`_get_traded_symbols`, L84 to L95): distinct `symbol` from trades in CLOSED or OPEN created on the date. |
| P06b-S274 | L102 to L108 (`_get_system_candles`, L98 to L111): candles (analytics: see P07). |
| P06b-S275 | L117 to L120 (`_get_instrument_token`, L114 to L131): `SELECT instrument_token FROM instruments`. No `CREATE TABLE ... instruments` exists in `core/schema.sql`, `core/analytics_schema.sql` or `core/migrations.py` (grep). The code catches `OperationalError`, logs a warning that the table is CSV-based and returns None (L122 to L129). |
| P06b-S471 | Heartbeat (FACT): `skip_if_non_trading_day("gemini_data_integrity_check")` at L387 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L388). |

### 2.16 `scripts/gemini_premarket_brief.py` (A15)

| ID | Statement |
|---|---|
| P06b-S276 | Open: raw RW `sqlite3.connect(db_path)` per function (L93, L107, L125, L140), each closed in `finally`. Writes: none by SQL; heartbeat at L280 to L281. |
| P06b-S277 | L96 to L100 (`_get_open_positions`, L92 to L103): trades `WHERE status = 'OPEN'`; errors not caught. |
| P06b-S278 | L110 to L116 (`_get_strategy_state`, L106 to L121): selects `sharpe_ratio`, `trade_count` and `status` from `strategy_metrics`. At the baseline `core/schema.sql` L933 to L943 defines `strategy_metrics` with `sharpe` and `total_trades` and no `status` column (p06b_cols.py). `OperationalError` is caught and `[]` returned (L117 to L118). INTERPRETATION: against a table of the baseline shape this query always fails and the function always returns `[]`. |
| P06b-S279 | L127 to L129 (`_get_kill_switch_state`, L124 to L136): `SELECT state, reason FROM kill_switch_state ORDER BY rowid DESC LIMIT 1`; `OperationalError` returns `UNKNOWN` (L133 to L134); no row returns `INACTIVE`. |
| P06b-S280 | L142 to L150 (`_get_yesterday_summary`, L139 to L158): COUNT and SUMs of `CLOSED` trades created on the previous date; errors not caught. |
| P06b-S472 | Heartbeat (FACT): `skip_if_non_trading_day("gemini_premarket_brief")` at L303 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L304). |

### 2.17 `scripts/gemini_trade_coach.py` (A15)

| ID | Statement |
|---|---|
| P06b-S281 | Open: dbc RW per function (L72, L95, L114), each closed in `finally`. Writes: none by SQL; heartbeat at L278 to L279. |
| P06b-S282 | L75 to L86 (`_get_closed_trades`, L71 to L91): trades LEFT JOIN trade_excursions, `status = 'CLOSED'` created on the date; `OperationalError` returns `[]` (L88 to L89). |
| P06b-S283 | L98 to L105 (`_get_rejected_signals`, L94 to L110): signals with `status LIKE 'REJECTED%%'` received on the date. |
| P06b-S284 | L116 to L126 (`_get_candle_summary`, L113 to L137): candles (analytics: see P07). |
| P06b-S473 | Heartbeat (FACT): `skip_if_non_trading_day("gemini_trade_coach")` at L301 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L302). |

### 2.18 `scripts/generate_screened_stocks_csv.py` (A15)

| ID | Statement |
|---|---|
| P06b-S285 | Open mode RO: `db_connect.connect_readonly(db_path)` at L270, closed in `finally` (L274 to L275). The comment at L266 to L268 records that an earlier `store.transaction(readonly=True)` raised TypeError on every run (HISTORICAL). |
| P06b-S286 | L123 to L131 (`get_traded_symbols`, L112 to L132): distinct `symbol` from trades created on the date, status not CANCELLED or FAILED. L146 to L154 (`get_non_traded_symbols`, L135 to L165): signals received on the date with status LIKE `REJECTED_%`, `DROPPED_%` or `SKIPPED_%`. |
| P06b-S287 | Writes: none by SQL; heartbeats through `skip_if_non_trading_day` (L339) and `HeartbeatTimer` (L341), which open their own StateStore (section 1). |

### 2.19 `scripts/healthcheck_server.py` (A15)

| ID | Statement |
|---|---|
| P06b-S288 | No connection of its own: `start_healthcheck_server` (L297 to L326) receives a `state_store` object; `main.py` imports it (L91) and passes its own `store` (L4074 to L4075). The server runs under waitress with `threads=1` in a daemon thread (L318 to L324). INTERPRETATION: by `StateStore._get_conn` (`core/state_store.py` L215 to L225) the server thread uses its own per-thread connection of the trading process's store. |
| P06b-S289 | Reads only, all through `state_store.fetch_one`: `_check_kill_switch` L55 to L57 (kill_switch_state `id = 1`); `health` L80 to L83 (trades created today); `metrics` L157 to L160 (trades today), L164 to L167 (signals today), L171 to L174 (signals `TRADED` today), L178 to L181 (trades OPEN or PARTIAL), L185 to L188 (`SUM(net_pnl)` of `CLOSED` trades today), L207 to L211 (`SUM(margin_reserved)` of OPEN, PARTIAL, EXITING trades), L215 (`get_day_opening_capital`, fm_ledger, `core/state_store.py` L2724), L229 to L232 (kill_switch_state), L236 to L239 (last signal received today); `metrics_prometheus` L277, L280, L283, L286 through `_q` (L270 to L275, which swallows exceptions). |
| P06b-S290 | "Today" in these queries is `date.today().isoformat()` (L79, L136, L267), the host's local date. Writes: none. |

### 2.20 `scripts/liveness_probe.py` (A15)

| ID | Statement |
|---|---|
| P06b-S291 | `read_kill_state` (L138 to L157): dbc RW `connect(str(db_path))` (L147 to L148; default relative path L138); `SELECT state FROM kill_switch_state WHERE id = 1` (L149); closed in `finally` (L150 to L151); any exception returns `UNKNOWN` (L155 to L157). |
| P06b-S292 | Writes: none by SQL; the comment at L126 to L128 explains that `skip_if_non_trading_day` is deliberately not called because it would write a SKIPPED heartbeat every 5 minutes (HISTORICAL). INTERPRETATION: the dbc RW open can create the analytics file and set its journal mode (section 1). |

### 2.21 `scripts/preflight/checks/database.py` (A20)

| ID | Statement |
|---|---|
| P06b-S293 | Open: raw RW `sqlite3.connect` per call (L25, L36, L114, and L139 with `timeout=5`), each closed in `finally`. The module docstring states that it never constructs a StateStore so as never to trigger a migration (L4 to L8; HISTORICAL; FACT: no StateStore in the file). |
| P06b-S294 | L27 to L29 (`_read_schema_version`, L23 to L32): `SELECT value FROM schema_meta WHERE key = 'schema_version'`. L38 (`_read_journal_mode`, L35 to L40): `PRAGMA journal_mode` (read). |
| P06b-S295 | L116 (`DbJournalModeWalCheck.fix`, L112 to L126): `PRAGMA journal_mode=WAL`, a persistent change of the database file's journal mode; `fix_action = "set_journal_mode_wal"` (L101) is on the pre-flight autofix whitelist (`scripts/preflight/autofix.py` L36; A20). |
| P06b-S296 | L143 to L144 (`DbWritableCheck.run`, L135 to L149): `BEGIN IMMEDIATE` then `conn.rollback()`: takes the write lock and releases it without changing a row. |
| P06b-S297 | Writes rows: none. Writes the file header only through the WAL fix. |

### 2.22 `scripts/preflight/checks/engine.py` (A20)

| ID | Statement |
|---|---|
| P06b-S298 | `_capital_now` (L105 to L137): raw RW `sqlite3.connect(str(db_path))` (L117), closed in `finally` (L136 to L137); `SELECT balance_after FROM fm_ledger WHERE date = ? AND entry_type = 'INIT' ORDER BY ts ASC LIMIT 1` (L119 to L123); `_sum_margin` (L96 to L102): `SUM(margin_reserved)` from trades for the status sets at L92 to L93. The comment L87 to L91 says pre-flight must not construct a StateStore (HISTORICAL). Writes: none. |

### 2.23 `scripts/preflight/checks/state.py` (A20)

| ID | Statement |
|---|---|
| P06b-S299 | `_safe_count` (L34 to L42) and `_kill_state` (L45 to L58): raw RW `sqlite3.connect`, closed in `finally`; exceptions return `(None, error)` or `UNKNOWN`. Writes: none. |
| P06b-S300 | Queries: L49 to L51 kill_switch_state `id = 1`; L93 trades in OPEN, PARTIAL; L112 orders in PENDING, SUBMITTED, OPEN, PARTIAL, TRIGGER_PENDING, `TRIGGER PENDING` (L26 to L27); L130 trades `EXITING`; L147 trades `needs_tgt_retry = 1`. |

### 2.24 `scripts/reconcile_positions.py` (A12)

| ID | Statement |
|---|---|
| P06b-S301 | Open: own StateStore at L376; closed at L406 (credential failure), L423 and L426. Paper split at L225 (not traced). Writes the trading database: yes, `position_reconciliation`. Credential sources named at L80 to L138 (names and paths only; no value read; A04): the account registry file `config/accounts.csv` (L103); the API-key environment-variable name held in the registry's `api_key_env` field (L109); the session token file `data_store/session/zerodha_token.json` (L113); the fallback environment-variable names `ZERODHA_API_KEY` and `ZERODHA_ACCESS_TOKEN` (L131 to L132). The docstring (L90 to L91) gives an account-suffixed variable name as an example of `api_key_env` (HISTORICAL; not reproduced). Not opened (security restriction). |
| P06b-S302 | L181 to L190 (`_get_system_positions`, L176 to L198): trades in OPEN, PARTIAL created up to the date with `qty_filled > 0`; autocommit read. |
| P06b-S303 | L330 to L345 (`_insert_position_reconciliation`, L327 to L345): plain `INSERT INTO position_reconciliation (date, symbol, broker_qty, system_qty, status, created_at)`; one `transaction()` per row; called in a loop at L296 to L298 unless `--dry-run`; every row of a run carries the same `created_at` (`now_str`, L217). |
| P06b-S304 | On a broker-fetch failure the function returns one `ERROR` result (L244 to L253) before the insert loop, so nothing is written for that run. `position_reconciliation` has no UNIQUE constraint on date and symbol (`core/schema.sql` L911 to L920); INTERPRETATION: a second run on the same date appends a second set of rows. |
| P06b-S474 | Heartbeat (FACT): `skip_if_non_trading_day("reconcile_positions")` at L441 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L442). On a trading day the run is wrapped by `HeartbeatTimer("reconcile_positions", alert=True)` (L443), default path. |

### 2.25 `scripts/reconstruct_excursions.py` (A15)

| ID | Statement |
|---|---|
| P06b-S305 | Open: own StateStore `StateStore(DB_PATH)` at L459 after a file lock (L448; lock file is part P08b); closed in `finally` (L497 to L498). Writes the trading database: yes, `trade_excursions` and `excursion_reconstruction_runs` through store methods, unless `--dry-run`. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S306 | L104 to L106, L127 to L129, L322 to L324 | `ensure_candles`, `_may_need_fetch` | candles | SELECT | analytics: see P07 | autocommit read | own StateStore |
| P06b-S307 | L118 to L126 | `ensure_candles` | candles | INSERT OR IGNORE (`insert_candle`) | analytics: see P07 | own `transaction()` | own StateStore |
| P06b-S308 | L246 to L254 | `select_trades` | trades | SELECT | CLOSED or CLOSED_MANUAL, all or by exit date | autocommit read | own StateStore |
| P06b-S309 | L163 | `reconstruct_one` | trades, candles | SELECT (`compute_trade_excursions`, `core/state_store.py` L2089) | one trade's window | autocommit read | own StateStore |
| P06b-S310 | L171 | `reconstruct_one` | trade_excursions | INSERT OR REPLACE (`insert_trade_excursion`, L2060) | MFE, MAE and entry-candle columns, `updated_at` | own `transaction()` per trade | own StateStore |
| P06b-S311 | L484 to L495 | `main` | excursion_reconstruction_runs | INSERT OR REPLACE (`insert_excursion_reconstruction_run`, L2179) | run_id (new uuid), mode, started_at, completed_at, counts, status, notes | own `transaction()` | own StateStore |
| P06b-S312 | Route: per-trade errors are classified `FAILED` and the run continues (L164 to L166, L172 to L174); a crash outside writes a critical sentinel (L499 to L511) and the heartbeat records the status (L515). | | | | | | |
| P06b-S475 | Heartbeat (FACT): `skip_if_non_trading_day("reconstruct_excursions")` at L532 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L533). On a trading day `_record_heartbeat` (L412 to L416) calls `record_heartbeat` with `db_path=DB_PATH` (L416); it is called at L515. | | | | | | |

### 2.26 `scripts/replay_signals.py` (A19)

| ID | Statement |
|---|---|
| P06b-S313 | Open: own StateStore at L185; the file has no `store.close()` (grep). Docstring RP1: "Read-only: NO database writes" (L16; HISTORICAL). INTERPRETATION: the open-time schema script still runs (section 1). |
| P06b-S314 | L43 to L50 (`fetch_signals`): signals received in a date range. L58 to L61 (`fetch_trade_for_signal`): trades by `trade_id`. L106 to L110 (`replay_one_signal`): latest screener_results row for a signal. All autocommit reads; writes: none by SQL. |

### 2.27 `scripts/sr_detector_backfill.py` (A08)

| ID | Statement |
|---|---|
| P06b-S315 | Open: own StateStore at L115; closed in `finally` (L118 to L122). Writes the trading database: yes, `sr_detector_results`. |
| P06b-S316 | L49 (`backfill`, L44 to L93): `get_sr_results_for_backfill` (`core/state_store.py` L1997 to L2006): sr_detector_results with `date(ts) = ?` and `actual_result IS NULL`. L55 to L59: latest trades row for the signal. |
| P06b-S317 | L63 to L66 and L84 to L90: `update_sr_outcome` (L2008 to L2024): `UPDATE sr_detector_results SET actual_fill, actual_result, win_loss, pnl WHERE id = ?`, one `transaction()` per row. No try in the loop; INTERPRETATION: an exception stops the run with earlier rows updated. |
| P06b-S318 | No heartbeat call on a trading day in this file; `skip_if_non_trading_day` (L141 to L144) writes a SKIPPED heartbeat on a non-trading day only. |

### 2.28 `scripts/strategy_registry_officer.py` (A07)

| ID | Statement |
|---|---|
| P06b-S319 | Open: dbc RW at L237 if the file exists (L236), closed in `finally` (L242 to L243). The section comment says "read-only" (L51; HISTORICAL). Writes: none by SQL (it writes the registry YAML; part P08b); heartbeat through `HeartbeatTimer` (L295). |
| P06b-S320 | L59 (`_distinct_signal_names`): `SELECT DISTINCT <col> FROM signals WHERE <col> IS NOT NULL` with `<col>` from the fixed tuple `scanner`, `strategy` (L57). L71 to L73 (`_filled_strategies`) and L85 to L88 (`_realized_directions`): trades with `qty_filled > 0`. Exceptions swallowed. |
| P06b-S476 | Heartbeat (FACT): `skip_if_non_trading_day("strategy_registry_officer")` at L293 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L294). |

### 2.29 `scripts/system_manager.py` (A15)

| ID | Statement |
|---|---|
| P06b-S321 | Open: own StateStore at L1324; `store.close()` in `finally` (L1350 to L1351). Heartbeat `system_manager_eod` (L1343 to L1348). |
| P06b-S322 | Reads (all autocommit, own StateStore): `_day_capital` L156 (`get_day_opening_capital`, fm_ledger); `_max_concurrent_positions` L174 to L178 (trades); `config_vs_actual_check` L242 to L292 through `_scalar` (L133 to L138) (trades: counts, SUM, MAX); `order_quality_report` L306 to L312 (trades), L342 to L345 (orders), L349 to L354 (orders JOIN trades); `system_health_check` L425 to L428 (cron_heartbeat), L438 (`PRAGMA integrity_check`), L466 to L475 (system_events `STARTUP` and `CRASH_DETECTED`), L489 (kill_switch_state); `trade_strategy_health` L524 to L528 (trades), L564 to L567 (strategy_metrics `win_rate, total_trades`); `risk_events_check` L584 to L586 and L610 to L613 (reconciliation_log), L593 (kill_switch_state); `compare_with_yesterday` L631 to L640 (trades, signals); `tomorrow_readiness_check` L680 to L686 (signals, trades, orders JOIN trades), L708 to L709 (kill_switch_state); `slippage_overrides_check` L994 to L997 (trades by `tolerance_source`). |
| P06b-S323 | Write path: `trigger_soft_kill` (L950 to L964) constructs `KillSwitch(store, EventBus(), ...)` and calls `soft_kill` (L960) unless the switch is already active (L955 to L957); `main` calls it only when reasons exist and neither `--no-soft-kill` nor `--dry-run` is given (L1334 to L1335). The SQL that `KillSwitch` runs is in `capital/kill_switch.py` (A13; part P06a). Writes the trading database: yes, through that path, plus the heartbeat. |

### 2.30 `scripts/t2_cnc_gtt_realtest.py` (A19)

| ID | Statement |
|---|---|
| P06b-S324 | The store is a throwaway database `data_store/t2_proof_<stamp>/t2_proof.db` in its own sub-folder (L182 to L190); `_assert_isolated` (L193 to L205) refuses the live main file or a live analytics sibling; own StateStore on that path at L221; closed in `finally` (L598 to L602). |
| P06b-S325 | L225 to L242 (`_open_throwaway_store`): one `transaction()` with `INSERT INTO signals (signal_id, symbol, scanner, strategy, triggered_at, received_at, expires_at, status, fingerprint, fingerprint_date)` (L226 to L232) and `INSERT INTO trades (trade_id, signal_id, symbol, direction, strategy, qty_planned, entry_target_price, sl_initial, tgt_initial, margin_reserved, risk_amount, created_at, status, order_protocol, updated_at)` (L233 to L242), into the throwaway file. |
| P06b-S326 | Further throwaway-store use: `CncGttPlacer(..., store=store)` and `hydrate_from_store` (L586 to L592; `orders/cnc_gtt.py`, A11); `_cancel_gtt_state` L345 (`set_gtt_state_status`, `UPDATE gtt_state SET status, updated_at WHERE gtt_id`, `core/state_store.py` L2394 to L2401); reads `get_active_gtt_for_trade` (L394, L499) and `get_active_gtt_states` (L500, L522). |
| P06b-S327 | The live trading database: the file has no connection site other than L221 (p06b_sqlscan.py). Whether imported modules open the live file during this script is UNKNOWN (not traced; A19, A04). |

### 2.31 `scripts/trade_journal.py` (A15)

| ID | Statement |
|---|---|
| P06b-S328 | Open: own StateStore `StateStore(Path(args.db))` at L157 (`--db` default relative `data_store/trading_system.db`, L150); the file has no `store.close()`. The date default is `date.today()` (L156), the host's local date. Heartbeat through `HeartbeatTimer` (L169). Writes the trading database: yes, `trade_journal`, through `store.execute` (autocommit), not `transaction()`. |

| ID | Lines | Function | Table(s) | Op | Predicate or columns (short) | Txn | Conn |
|---|---|---|---|---|---|---|---|
| P06b-S329 | L44 to L54 | `generate_journal` | trades LEFT JOIN signals | SELECT | trades created on the date with `status = 'CLOSED'` | autocommit read | own StateStore |
| P06b-S330 | L61 to L64 | `generate_journal` | trade_journal | DELETE | `WHERE date = ?`, only when trades exist (L56 to L58) | autocommit (`store.execute`) | own StateStore |
| P06b-S331 | L68 to L75 | `generate_journal` | screener_results JOIN signals | SELECT | scores of signals received on the date | autocommit read | own StateStore |
| P06b-S332 | L81 to L86 | `generate_journal` | trade_excursions | SELECT | `trade_id, mfe_price WHERE DATE(created_at) = ?`; `core/schema.sql` L824 to L836 defines no `created_at` in trade_excursions (it has `updated_at`); every exception is swallowed (L88 to L89). INTERPRETATION: against the baseline table shape this query fails and the MFE map stays empty | autocommit read | own StateStore |
| P06b-S333 | L103 to L105 | `generate_journal` | trades | SELECT | `signal_id` by `trade_id` | autocommit read | own StateStore |
| P06b-S334 | L128 to L140 | `generate_journal` | trade_journal | INSERT | `date, trade_id, strategy, symbol, direction, entry_reason, exit_reason, slippage_assessment, mfe_captured_pct, entry_price, exit_price, net_pnl, notes, created_at`, one statement per trade | autocommit (`store.execute`) | own StateStore |
| P06b-S335 | Route: INTERPRETATION: the DELETE commits at once; an exception during the INSERT loop leaves the date's journal partly rebuilt; a re-run deletes and rebuilds it again. | | | | | | |
| P06b-S477 | Heartbeat (FACT): `skip_if_non_trading_day("trade_journal")` at L167 in `_cron_main`; on a non-trading day it writes a SKIPPED cron_heartbeat row through a new StateStore (`utils/cron_heartbeat.py` L201 to L206; only if the default-path file exists, L81 to L82) and `_cron_main` returns 0 (L168). | | | | | | |

### 2.32 `scripts/v3_hardgate_parity_recompute.py` (A18)

| ID | Statement |
|---|---|
| P06b-S336 | `main` (L207 to L237): raw RO `sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)` (L214) on the required `--db` argument, described as a database backup (L209); `SELECT * FROM screener_results ORDER BY id` with an optional integer LIMIT (L216 to L219); closed at L220. Writes: none. |

### 2.33 `scripts/v3_shadow_soak_report.py` (A18)

| ID | Statement |
|---|---|
| P06b-S337 | Raw RO URI on `_DB` = `<repository root>/data_store/trading_system.db` (L37) with timeout 30 and `PRAGMA busy_timeout = 30000`, per function (L66 to L67, L158 to L159, L288 to L289), each closed in `finally`. Writes: none. |
| P06b-S338 | L70 to L74 (`scorer_report`): screener_results since a date. L162 to L164 (`_trade_outcomes`): trades `signal_id, net_pnl` (errors printed, L168 to L169). L292 to L294 (`_pb01_watchlist_rows`): pb01_watchlist (errors return `[]`, L296 to L298). |

## 3. Open mode and trading-database writes, per file

| ID | File | Owner | Opens through | RO or RW | Writes the trading database? |
|---|---|---|---|---|---|
| P06b-S339 | `ops_dashboard/backend/readers/db_reader.py` | A15 | raw `mode=ro` URI | RO | No |
| P06b-S340 | `reports/daily_trade_review.py` | A15 | own StateStore | RW | No business row; open-time schema script; heartbeats |
| P06b-S341 | `scripts/backfill_closure_source_w8.py` | A12 | own StateStore; raw RW for the backup | RW | Yes: trades (`closure_source`), with `--commit` or `--revert-file` |
| P06b-S342 | `scripts/capture_metrics_baseline.py` | A15 | dbc RW | RW | No trading-table SQL (analytics only, P07); heartbeats |
| P06b-S343 | `scripts/check_vm_state.py` | A15 | raw RW | RW | Yes: trades and orders, with `--cleanup-pending` or `--cleanup-orders` |
| P06b-S344 | `scripts/compute_strategy_metrics.py` | A07 | own StateStore | RW | Yes: strategy_metrics (not with `--dry-run`); heartbeat |
| P06b-S345 | `scripts/cron_officer.py` | A16 | own StateStore | RW | No business row; open-time schema script; heartbeats |
| P06b-S346 | `scripts/deploy_assert.py` | A17 | raw `mode=ro` URI plus `query_only` | RO | No |
| P06b-S347 | `scripts/eod_broker_reconcile.py` | A12 | own StateStore | RW | Yes: eod_broker_reconciliation, pnl_reconciliation; heartbeat |
| P06b-S348 | `scripts/eod_cleanup.py` | A12 | own StateStore | RW | Yes: signals, orders, smart_tgt_state and five signal-child tables (not with `--dry-run`); heartbeat |
| P06b-S349 | `scripts/eod_verify.py` | A12 | own StateStore | RW | Yes: eod_verification; heartbeat |
| P06b-S350 | `scripts/fetch_daily_candles.py` | A05 | raw RW (read); dbc RW (analytics write) | RW | No trading-table write; heartbeats |
| P06b-S351 | `scripts/fetch_fno_ban.py` | A05 | own StateStore | RW | Yes: fno_ban; heartbeat |
| P06b-S352 | `scripts/forward_shadow_record.py` | A18 | own StateStore | RW | No trading-table write (candles: P07); heartbeats |
| P06b-S353 | `scripts/gemini_data_integrity_check.py` | A15 | dbc RW | RW | No; heartbeat |
| P06b-S354 | `scripts/gemini_premarket_brief.py` | A15 | raw RW | RW | No; heartbeat |
| P06b-S355 | `scripts/gemini_trade_coach.py` | A15 | dbc RW | RW | No; heartbeat |
| P06b-S356 | `scripts/generate_screened_stocks_csv.py` | A15 | dbc RO (`connect_readonly`) | RO | No SQL write; heartbeats through their own StateStore |
| P06b-S357 | `scripts/healthcheck_server.py` | A15 | main.py store (in the trading process) | RW (shared) | No |
| P06b-S358 | `scripts/liveness_probe.py` | A15 | dbc RW | RW | No |
| P06b-S359 | `scripts/preflight/checks/database.py` | A20 | raw RW | RW | No row; the WAL autofix changes the file's journal mode |
| P06b-S360 | `scripts/preflight/checks/engine.py` | A20 | raw RW | RW | No |
| P06b-S361 | `scripts/preflight/checks/state.py` | A20 | raw RW | RW | No |
| P06b-S362 | `scripts/reconcile_positions.py` | A12 | own StateStore | RW | Yes: position_reconciliation (not with `--dry-run`); heartbeat |
| P06b-S363 | `scripts/reconstruct_excursions.py` | A15 | own StateStore | RW | Yes: trade_excursions, excursion_reconstruction_runs (not with `--dry-run`); heartbeat |
| P06b-S364 | `scripts/replay_signals.py` | A19 | own StateStore | RW | No business row; open-time schema script |
| P06b-S365 | `scripts/sr_detector_backfill.py` | A08 | own StateStore | RW | Yes: sr_detector_results |
| P06b-S366 | `scripts/strategy_registry_officer.py` | A07 | dbc RW | RW | No; heartbeat |
| P06b-S367 | `scripts/system_manager.py` | A15 | own StateStore | RW | Yes, conditionally: kill_switch_state through `KillSwitch.soft_kill` (P06a); heartbeat |
| P06b-S368 | `scripts/t2_cnc_gtt_realtest.py` | A19 | own StateStore on a throwaway file | RW (throwaway) | Not the live file by its own connections; writes signals, trades, gtt_state in the throwaway file |
| P06b-S369 | `scripts/trade_journal.py` | A15 | own StateStore | RW | Yes: trade_journal; heartbeat |
| P06b-S370 | `scripts/v3_hardgate_parity_recompute.py` | A18 | raw `mode=ro` URI on `--db` | RO | No |
| P06b-S371 | `scripts/v3_shadow_soak_report.py` | A18 | raw `mode=ro` URI | RO | No |

| ID | Statement |
|---|---|
| P06b-S372 | Counts from the table above: 5 files open only RO (db_reader, deploy_assert, generate_screened_stocks_csv for its SQL, v3_hardgate_parity_recompute, v3_shadow_soak_report); 16 construct their own StateStore; 1 uses main.py's store; the rest open raw RW or dbc RW connections. 11 files write trading-database business rows by their own statements or store calls (backfill_closure_source_w8, check_vm_state, compute_strategy_metrics, eod_broker_reconcile, eod_cleanup, eod_verify, fetch_fno_ban, reconcile_positions, reconstruct_excursions, sr_detector_backfill, trade_journal), plus system_manager through `KillSwitch`. |
| P06b-S373 | Writes that bypass the named store methods (raw SQL against the trading database): `check_vm_state.py` (own raw connection, no store), `eod_cleanup.py`, `compute_strategy_metrics.py`, `eod_verify.py`, `fetch_fno_ban.py`, `reconcile_positions.py`, `trade_journal.py`, `backfill_closure_source_w8.py` (`_revert` only) (SQL passed into the store's `transaction()` or `execute`). No CREATE TABLE, ALTER or DROP exists in any of the 33 files (p06b_sqllits.py output). |

## 4. All write statements of this part, consolidated (trading database)

| ID | Table | Operation | File and lines | Function | Txn | Gate |
|---|---|---|---|---|---|---|
| P06b-S374 | trades | UPDATE `closure_source` (COALESCE) | `scripts/backfill_closure_source_w8.py` L245 to L246 (store `set_trade_closure_axes`) | `main` | per row | `--commit` |
| P06b-S375 | trades | UPDATE `closure_source = NULL` | `scripts/backfill_closure_source_w8.py` L305 to L310 | `_revert` | one for all | `--revert-file` |
| P06b-S376 | trades | UPDATE `status`, `exit_reason` | `scripts/check_vm_state.py` L136 to L141 | module level | implicit, commit | `--cleanup-pending` |
| P06b-S377 | orders | UPDATE `status` | `scripts/check_vm_state.py` L162 to L170 | module level | implicit, commit | `--cleanup-orders` |
| P06b-S378 | strategy_metrics | INSERT OR REPLACE | `scripts/compute_strategy_metrics.py` L274 to L287 | `run_strategy_metrics` | per strategy | not `--dry-run` |
| P06b-S379 | eod_broker_reconciliation | INSERT OR REPLACE | `scripts/eod_broker_reconcile.py` L295 to L304 (store method) | `persist` | own | none |
| P06b-S380 | pnl_reconciliation | INSERT OR REPLACE | `scripts/eod_broker_reconcile.py` L306 to L312 (store method) | `persist` | own | broker P&L available |
| P06b-S381 | signals | UPDATE `status = 'EXPIRED'` | `scripts/eod_cleanup.py` L120 to L125 | `_cleanup_stale_signals` | own | not `--dry-run` |
| P06b-S382 | orders | UPDATE `status`, `updated_at` (two statements) | `scripts/eod_cleanup.py` L146 to L166 | `_cleanup_stale_orders` | one for both | not `--dry-run` |
| P06b-S383 | smart_tgt_state | DELETE | `scripts/eod_cleanup.py` L183 to L186 | `_cleanup_orphaned_smart_tgt` | own | not `--dry-run` |
| P06b-S384 | screener_results, gate_state, shadow_trades, sr_detector_results, retest_state, signals | DELETE | `scripts/eod_cleanup.py` L250 to L266 | `_cleanup_old_fingerprints` | per batch of 2000 | not `--dry-run` |
| P06b-S385 | eod_verification | INSERT OR REPLACE | `scripts/eod_verify.py` L157 to L163 | `run_eod_verification` | own | none |
| P06b-S386 | fno_ban | INSERT OR REPLACE | `scripts/fetch_fno_ban.py` L182 to L190; L209 to L213 | `store_fno_ban`; `store_fetch_failed_sentinel` | per symbol; own | fresh CSV, not `--dry-run`; `fail_closed` |
| P06b-S387 | position_reconciliation | INSERT | `scripts/reconcile_positions.py` L330 to L345 | `_insert_position_reconciliation` | per row | not `--dry-run`; broker fetch succeeded |
| P06b-S388 | trade_excursions | INSERT OR REPLACE (store method) | `scripts/reconstruct_excursions.py` L171 | `reconstruct_one` | per trade | not `--dry-run` |
| P06b-S389 | excursion_reconstruction_runs | INSERT OR REPLACE (store method) | `scripts/reconstruct_excursions.py` L484 to L495 | `main` | own | not `--dry-run` |
| P06b-S390 | sr_detector_results | UPDATE outcome columns (store method) | `scripts/sr_detector_backfill.py` L63 to L66, L83 to L89 | `backfill` | per row | none |
| P06b-S391 | trade_journal | DELETE then INSERT per trade | `scripts/trade_journal.py` L61 to L64, L128 to L140 | `generate_journal` | autocommit per statement | trades exist for the date |
| P06b-S392 | kill_switch_state (through `KillSwitch`) | see P06a | `scripts/system_manager.py` L950 to L964, called at L1335 | `trigger_soft_kill` | see P06a | reasons exist; not `--no-soft-kill`; not `--dry-run` |
| P06b-S393 | cron_heartbeat | INSERT (store method through `record_heartbeat`) | 20 files of this part (section 1; the call lines are cited per file in sections 2.2 to 2.31, including P06b-S465 to P06b-S477; default or own path per P06b-S478) | various | own | see A16 |
| P06b-S394 | schema objects and schema-version row | executescript at open | every file that constructs a StateStore (section 1) | `StateStore.__init__` | see P03 | always |

## 5. Table-by-table summary (this part's files only)

"db_reader" means `ops_dashboard/backend/readers/db_reader.py` (A15); its functions are listed in section 2.1. "DTR" means `reports/daily_trade_review.py` (A15).

| ID | Table | Writers in this part (file: function; owner) | Readers in this part (file: function; owner) |
|---|---|---|---|
| P06b-S395 | trades | backfill_closure_source_w8: `main`, `_revert` (A12); check_vm_state: module (A15) | db_reader (53 functions); DTR (several); backfill_closure_source_w8; check_vm_state; compute_strategy_metrics (A07); cron_officer `_detect_mode` (A16); eod_broker_reconcile `gather_local` (A12); eod_cleanup subqueries (A12); eod_verify (A12); forward_shadow_record (A18); gemini_data_integrity_check, gemini_premarket_brief, gemini_trade_coach (A15); generate_screened_stocks_csv (A15); healthcheck_server (A15); preflight engine and state checks (A20); reconcile_positions (A12); reconstruct_excursions (A15); replay_signals (A19); sr_detector_backfill (A08); strategy_registry_officer (A07); system_manager (A15); trade_journal (A15); v3_shadow_soak_report (A18) |
| P06b-S396 | orders | check_vm_state: module (A15); eod_cleanup: `_cleanup_stale_orders` (A12) | db_reader (27 functions, two of them through the module-level predicates at L433 to L440); DTR; backfill_closure_source_w8 subquery; check_vm_state; eod_broker_reconcile (store methods); eod_verify; preflight state check; system_manager |
| P06b-S397 | signals | eod_cleanup: `_cleanup_stale_signals`, `_cleanup_old_fingerprints` (A12) | db_reader (26 functions); DTR; check_vm_state; fetch_daily_candles (A05); forward_shadow_record; gemini_trade_coach; generate_screened_stocks_csv; healthcheck_server; replay_signals; strategy_registry_officer; system_manager; trade_journal |
| P06b-S398 | screener_results, gate_state, shadow_trades, retest_state | eod_cleanup: `_cleanup_old_fingerprints` (DELETE; A12) | screener_results only: db_reader (4 functions); DTR (store method); forward_shadow_record; replay_signals; trade_journal; v3_hardgate_parity_recompute and v3_shadow_soak_report (A18) |
| P06b-S399 | sr_detector_results | eod_cleanup: `_cleanup_old_fingerprints` (DELETE; A12); sr_detector_backfill: `backfill` (UPDATE; A08) | DTR `build_records`; sr_detector_backfill (store method) |
| P06b-S400 | smart_tgt_state | eod_cleanup: `_cleanup_orphaned_smart_tgt` (DELETE; A12) | eod_cleanup (dry-run count) |
| P06b-S401 | strategy_metrics | compute_strategy_metrics: `run_strategy_metrics` (A07) | compute_strategy_metrics `_check_demotion`; gemini_premarket_brief `_get_strategy_state` (columns absent, section 2.16); system_manager `trade_strategy_health` |
| P06b-S402 | eod_verification | eod_verify: `run_eod_verification` (A12) | db_reader `audit_feed`; eod_broker_reconcile (store method) |
| P06b-S403 | eod_broker_reconciliation | eod_broker_reconcile: `persist` (A12) | none in this part |
| P06b-S404 | pnl_reconciliation | eod_broker_reconcile: `persist` (A12) | eod_verify `_evaluate_pnl` |
| P06b-S405 | position_reconciliation | reconcile_positions: `_insert_position_reconciliation` (A12) | db_reader `position_reconciliation_latest`, `position_reconciliation_timeline`; eod_broker_reconcile `gather_local` |
| P06b-S406 | fno_ban | fetch_fno_ban: `store_fno_ban`, `store_fetch_failed_sentinel` (A05) | fetch_fno_ban `is_symbol_fno_banned` only |
| P06b-S407 | trade_excursions | reconstruct_excursions: `reconstruct_one` (A15) | db_reader `statistics_bundle`, `position_excursions`; DTR (store method and `build_dashboard_data`); gemini_trade_coach; trade_journal (query names an absent column) |
| P06b-S408 | excursion_reconstruction_runs | reconstruct_excursions: `main` (A15) | none in this part |
| P06b-S409 | trade_journal | trade_journal: `generate_journal` (A15) | none in this part |
| P06b-S410 | kill_switch_state | system_manager through `KillSwitch` (A15 caller; A13 code; P06a) | db_reader `get_kill_switch`, `audit_kill_switch`; check_vm_state; gemini_premarket_brief; healthcheck_server; liveness_probe; preflight state check; system_manager |
| P06b-S411 | cron_heartbeat | 20 files through `record_heartbeat` (A16 code) | db_reader `latest_heartbeats`, `syslog_cron_range`, `syslog_retention`; cron_officer `_today_heartbeats`; system_manager `system_health_check` |
| P06b-S412 | fm_ledger | none in this part | db_reader (7 functions); DTR; eod_broker_reconcile; healthcheck_server (store method); preflight engine check; system_manager (store method) |
| P06b-S413 | config_snapshots | none in this part | db_reader `latest_config_snapshot`, `config_snapshot_history`, `config_snapshot_for_date`, `audit_config_snapshots`, `config_snapshot_trail`, `audit_retention_meta`; DTR `_load_min_score`, `build_config_data`, `_slip_tiers_for_date`, `build_dashboard_data` |
| P06b-S414 | session | none in this part | db_reader `get_session_info` (columns `session_date, account_id, broker, mode, trade_type, session_start, last_updated`; not `last_config_hash`) |
| P06b-S415 | schema_meta | none by SQL in this part (the StateStore open writes it; section 1) | db_reader `get_schema_version`, `db_health`; deploy_assert; preflight database check |
| P06b-S416 | system_events, reconciliation_log, webhook_audit, trade_slippage_log, order_execution_log, innings, gtt_state, telegram_alerts, control_tower_findings, preflight_runs, preflight_check_results, preflight_autofix_log | none in this part (gtt_state only in the t2 throwaway file) | db_reader (functions in section 2.1); DTR (reconciliation_log, webhook_audit, trade_slippage_log); system_manager (system_events, reconciliation_log) |
| P06b-S417 | pb01_watchlist | none in this part | v3_shadow_soak_report `_pb01_watchlist_rows` |
| P06b-S418 | instruments | none | gemini_data_integrity_check `_get_instrument_token` (table not defined in the schema files) |
| P06b-S419 | candles, system_metrics, system_metrics_daily | analytics: see P07 (capture_metrics_baseline, fetch_daily_candles, reconstruct_excursions, forward_shadow_record through `ensure_candles`) | analytics: see P07 (db_reader, DTR, forward_shadow_record, gemini_data_integrity_check, gemini_trade_coach, reconstruct_excursions, capture_metrics_baseline) |

## Concerns for the AUDIT (neutral)

| ID | Concern (what the code does, where; no verdict) |
|---|---|
| P06b-S420 | `scripts/check_vm_state.py` is documented as "read-only diagnostics only" (L2) but updates `trades` (L136 to L141) and `orders` (L162 to L170) with raw SQL on two flags, outside the store and with no `updated_at`. The `--cleanup-orders` preview SELECT (L149 to L155) also lists orders with no trade, but the UPDATE (L162 to L169) does not cover them, and the printed count is the preview's row count (L171). |
| P06b-S421 | `scripts/eod_cleanup.py`: the dry-run count for stale orders (L137 to L140) uses a wider predicate than the two live UPDATEs (L146 to L166), which also require a terminal or missing trade. |
| P06b-S422 | `scripts/eod_cleanup.py` L183 to L186 deletes every `smart_tgt_state` row whose trade is not OPEN or PARTIAL, which includes trades in other non-terminal statuses (for example EXITING or PENDING_FILL, both allowed by the trades CHECK at `core/schema.sql` L158 to L160). |
| P06b-S423 | `scripts/eod_cleanup.py` L149 and L161 stamp `orders.updated_at` with SQLite `datetime('now','localtime')` (host local time, `YYYY-MM-DD HH:MM:SS` format), while the other writers in this part use `now_ist().isoformat()`. |
| P06b-S424 | `scripts/eod_cleanup.py` step 4 (L211 to L271) deletes rows from `signals` and five child tables on a retention window; this is a retention mechanism separate from `scripts/db_retention.py` (P09b). |
| P06b-S425 | `scripts/trade_journal.py` writes with `store.execute` (autocommit) rather than `transaction()` (L61 to L64, L128 to L140); never closes its store; selects `trade_excursions.created_at`, a column absent from the baseline schema, and swallows the error (L81 to L89); uses the host date (L156). |
| P06b-S426 | `scripts/gemini_premarket_brief.py` L110 to L116 names three columns absent from the baseline `strategy_metrics` and returns `[]` on the error. |
| P06b-S427 | `ops_dashboard/backend/readers/db_reader.py` `last_successful_order` (L1341 to L1345) selects `orders.symbol`; the baseline `orders` table (`core/schema.sql` L315 to L351) has no `symbol` column; the function returns None on `OperationalError` (L1346 to L1347). |
| P06b-S428 | `scripts/gemini_data_integrity_check.py` L117 to L120 queries an `instruments` table that no schema file defines (the code's own warning says so). |
| P06b-S429 | Read-only jobs that open the trading database RW: through StateStore (`reports/daily_trade_review.py`, `scripts/cron_officer.py`, `scripts/replay_signals.py` whose docstring says "NO database writes", `scripts/forward_shadow_record.py`), through `db_connect.connect` (`scripts/strategy_registry_officer.py` whose comment says "read-only", `scripts/gemini_data_integrity_check.py`, `scripts/gemini_trade_coach.py`, `scripts/liveness_probe.py`) and through raw `sqlite3.connect` (`scripts/gemini_premarket_brief.py`, `scripts/fetch_daily_candles.py`, the three pre-flight checks). The StateStore opens run the schema script at open (section 1). |
| P06b-S430 | `ops_dashboard/backend/readers/db_reader.py` opens `mode=ro` without `PRAGMA query_only`; `db_connect.connect_readonly` sets both. |
| P06b-S431 | Status vocabularies: `scripts/eod_verify.py` writes `PENDING` (L151) where the schema comment for `eod_verification.status` lists `VERIFIED` and `ISSUES_FOUND` (`core/schema.sql` L1010); `scripts/eod_broker_reconcile.py` writes `pnl_reconciliation.status` `OK` or `VARIANCE` (L310) where the schema comment lists `OK`, `VARIANCE_MINOR`, `VARIANCE_MAJOR`, `PAPER_SKIPPED`, `ERROR` (L850). Neither column has a CHECK constraint at those lines. |
| P06b-S432 | `scripts/backfill_closure_source_w8.py` writes the receipt after the whole per-row write loop (L245 to L246, receipt L254; the comment at L248 to L253, under the section header "THE WRITE" at L240, places the receipt after the write step as a whole: "Backup -> write -> receipt -> verify"), so an exception inside the loop leaves the rows already written without a receipt; the backup taken at L236 exists at that point. |
| P06b-S433 | `scripts/reconcile_positions.py`: per-row transactions (L330); plain INSERT into a table without a unique key; the broker-failure `ERROR` result is not persisted (L244 to L253). |
| P06b-S434 | `scripts/fetch_fno_ban.py`: per-symbol transactions with errors logged and skipped (L180 to L193); `fno_ban` has no reader outside this script and tests. |
| P06b-S435 | `scripts/compute_strategy_metrics.py`: the documented PAPER_ONLY demotion is not written anywhere by this file (L176 to L230). |
| P06b-S436 | `scripts/eod_broker_reconcile.py`: two upserts in separate transactions (L295, L307); `persist` and `store.close()` are not protected by try/finally (L397 to L428). |
| P06b-S437 | `scripts/system_manager.py` can trip the kill switch in the database from a separate cron process (L950 to L964, L1334 to L1335). |
| P06b-S438 | `scripts/preflight/checks/database.py` `DbJournalModeWalCheck.fix` (L116) changes the live file's journal mode from a pre-flight process; `DbWritableCheck` (L143 to L144) briefly takes the write lock. |
| P06b-S439 | Heartbeats open a new StateStore per call with a relative default path (`utils/cron_heartbeat.py` L61, L84); `scripts/capture_metrics_baseline.py` records its success heartbeat as `capture_metrics_baseline` (L326) but its skip heartbeat as `capture_metrics` or `metrics_summary` (L351 to L354). |
| P06b-S440 | `scripts/healthcheck_server.py` and `scripts/trade_journal.py` use `date.today()` (host date) to pick the day in SQL predicates (healthcheck L79, L136, L267; journal L156). |
| P06b-S441 | `scripts/sr_detector_backfill.py` writes without a heartbeat on trading days (no `record_heartbeat` or `HeartbeatTimer` in the file). |
| P06b-S479 | Heartbeat path versus working path (P06b-S478): `skip_if_non_trading_day`, `HeartbeatTimer` and most `record_heartbeat` calls in this part use the relative default `data_store/trading_system.db` (`utils/cron_heartbeat.py` L61, L119, L179), while several of the same scripts open their own database at `--db` or at a repository-root path (for example `scripts/eod_verify.py` L197, `scripts/eod_broker_reconcile.py` L356, `scripts/forward_shadow_record.py` L147); only four files pass their own path to the helper. |

## Questions about intent (OPEN QUESTION, for the project owner)

| ID | Question |
|---|---|
| P06b-S442 | OPEN QUESTION: Were the `--cleanup-pending` and `--cleanup-orders` flags of `scripts/check_vm_state.py` sanctioned operator tools, or left over from before the file was documented as read-only? |
| P06b-S443 | OPEN QUESTION: Was `scripts/eod_cleanup.py` meant to delete `smart_tgt_state` rows for trades that are EXITING or PENDING_FILL? |
| P06b-S444 | OPEN QUESTION: Was it intended that reporting and research jobs open the trading database read-write (and run the schema script) rather than read-only? |
| P06b-S445 | OPEN QUESTION: Was the trade-journal rebuild meant to be atomic per date? |
| P06b-S446 | OPEN QUESTION: Which status vocabulary is intended for `eod_verification.status` and `pnl_reconciliation.status`: the values the code writes or the ones in the schema comments? |
| P06b-S447 | OPEN QUESTION: Was a database write of the PAPER_ONLY demotion intended for `scripts/compute_strategy_metrics.py`? |
| P06b-S448 | OPEN QUESTION: Should `orders.symbol`, `trade_excursions.created_at`, `strategy_metrics.sharpe_ratio`, `trade_count`, `status` and the `instruments` table exist, or are these queries out of date? |

## UNKNOWN / NOT ESTABLISHED

| ID | Item |
|---|---|
| P06b-S449 | UNKNOWN / NOT ESTABLISHED: whether any of these scripts ran in production, when, how often, with which flags and against which database file; no database, log or crontab survives. |
| P06b-S450 | UNKNOWN / NOT ESTABLISHED: whether the production tables had older or extra columns (for example `trade_excursions.created_at` or `strategy_metrics.sharpe_ratio`); `CREATE TABLE IF NOT EXISTS` keeps an existing table's shape, so the baseline schema text does not prove the production shape. |
| P06b-S451 | UNKNOWN / NOT ESTABLISHED: whether the check_vm_state cleanup flags, the system_manager soft-kill path or the pre-flight WAL autofix ever wrote to the production database. |
| P06b-S452 | UNKNOWN / NOT ESTABLISHED: the Python version, and so the exact default transaction control of raw `sqlite3` connections. |
| P06b-S453 | UNKNOWN / NOT ESTABLISHED: where and with which configured paths the dashboard ran in production (the baseline `gui_config.yaml` holds development-machine paths). |
| P06b-S454 | UNKNOWN / NOT ESTABLISHED: whether modules imported by `scripts/t2_cnc_gtt_realtest.py` open the live database. |

## Boundary handoffs (owner topic: what crosses)

| ID | Handoff |
|---|---|
| P06b-S455 | P01: connection set-up of every opener listed in section 3 (path resolution, URI flags, timeouts, PRAGMAs). |
| P06b-S456 | P03: the open-time schema script and migration refusal for the 16 StateStore openers and every heartbeat. |
| P06b-S457 | P04 and P05: the store methods called here (`set_trade_closure_axes`, `get_*_for_date`, `get_today_closed_pnl`, `get_all_open_trades`, `get_pending_intraday_orders`, `get_eod_verification_status`, `upsert_eod_broker_reconciliation`, `upsert_pnl_reconciliation`, `get_sr_results_for_backfill`, `update_sr_outcome`, `insert_candle`, `compute_trade_excursions`, `insert_trade_excursion`, `insert_excursion_reconstruction_run`, `get_day_opening_capital`, `get_cron_heartbeats_since`, `insert_cron_heartbeat`, `set_gtt_state_status`, `get_active_gtt_for_trade`, `get_active_gtt_states`). |
| P06b-S458 | P06a: `capital/kill_switch.py` SQL reached from `scripts/system_manager.py`. |
| P06b-S459 | P07: every candles, system_metrics and system_metrics_daily statement listed here, and the ATTACH side effects of `db_connect.connect`. |
| P06b-S460 | P08b: the backup copy and receipt of `backfill_closure_source_w8.py`, the JSONL of `forward_shadow_record.py`, the lock of `reconstruct_excursions.py`, the registry YAML of `strategy_registry_officer.py`, report and CSV outputs, sentinel files. |
| P06b-S461 | P09b: `eod_cleanup.py` step 4 as a second retention mechanism beside `db_retention.py`. |
| P06b-S462 | A16: heartbeat writes and job names; the declared schedules of these scripts (Appendix A) are boundary facts only. |
| P06b-S463 | A12: business meaning of the closure, cleanup, verification and reconciliation writes. A13: the kill-switch write path of `system_manager.py` and the removed `--reset` of `check_vm_state.py`. A20: the pre-flight checks and the WAL autofix. A02: the `config_snapshots` readers in db_reader and DTR (the writer and handoffs V-11, V-45 are P06a's); db_reader's `session` read does not read `last_config_hash`. A05, A07, A08, A15, A17, A18, A19: the business logic of their scripts listed in section 3. A04 and A11: credential handling of `reconcile_positions.py` and the `CncGttPlacer` store use in `t2_cnc_gtt_realtest.py`. |
