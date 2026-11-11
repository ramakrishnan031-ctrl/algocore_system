# A03 evidence: The trading schema, second half: `core/schema.sql` L991 to L1654

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P02b, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** The catalogue of `core/schema.sql` L991 to L1654: 22 tables, their columns, constraints and indexes, and the schema-version statement. Statement IDs `P02b-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

- P02b-S001 FACT — Repository and baseline (helper's draft pass): the local read-only clone of the legacy repository, read only. Before any work, `git -C <legacy clone> rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline) and `git status --short` returned nothing. After the output file was written, both commands were run again: HEAD was still `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` again returned nothing.
- P02b-S002 FACT — Files and lines read: `core/schema.sql` L960 to L1654 (L960 to L990 for context only; they belong to part P02a) and L1 to L36 (header and `schema_meta` definition, for context only; part P02a records them); `core/migrations.py` L112 to L140 (only to give an exact pointer for `MIGRATION_TABLES`; part P03 owns that file); the project's Master System Investigation Index, section 3 and Appendix A (topic owners only); plus whole-file grep hits in `core/schema.sql` used for S402 (L291) and S428 (L155, L193, L210 to L236).
- P02b-S003 FACT — Tools: the Read tool, `grep` and `awk` on the range, and three scratch scripts kept in the work area's tools folder, outside the clone, run with `python3 -I`: `p02b_parse_schema.py` (regular-expression parse that lists each CREATE TABLE with its line span and columns, and each CREATE INDEX), `p02b_gen_columns.py` (regular-expression parse that produced the column tables in section 3) and `p02b_assemble.py` (assembled the draft from the intermediate files `p02b_template.md.txt` and `p02b_columns.md.txt` and numbered the statement IDs). The schema file was parsed as TEXT only; it was never executed, not even against an in-memory database. The table, column and index counts in section 6 and the column tables in section 3 rely on that text parsing and were checked by eye against the source lines.
- P02b-S004 FACT — Not traced here: callers of these tables (parts P04 to P06), the way the file is executed (parts P01 and P03), the analytics database (part P07), backups (part P09a), tests (topic A19, out of scope). Paper-only meaning of columns is recorded only as stated by the DDL comment; the paper side is not traced.
- P02b-S005 FACT — Security handling: one inline comment in the range (L1495) quotes an example broker account identifier; it is written here as `<ACCOUNT_ID>`. One block comment (L1547) names the parties that approved an invariant; the names are omitted here. No credential file was opened.
- P02b-S517 FACT — Checker pass: the independent check file records that, before and after its work, `git -C <legacy clone> rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing; it wrote nothing in the clone and ran or imported no legacy code, SQL or test. Its own text-parsing script (`checker_p02b_parse.py`) was kept in the work area's tools folder, outside the clone.
- P02b-S518 FACT — Corrector pass: before and after the correction work, `git -C <legacy clone> rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing. The corrector read as text `core/schema.sql` (the lines cited by the findings: L1058, L1112 to L1113, L1128, L1142 to L1148, L1162, L1217, L1256, L1308 to L1312, L1359, L1384 to L1388, L1396, L1478 to L1496, L1517, L1554 to L1566, L1582 to L1591, L1604 to L1612, and greps for v29, v30, v34, v35 and CREATE TRIGGER), `core/state_store.py` L102, L350 to L356 and L396 to L448, `screening/secondary_screener.py` L380 to L418, `core/daily_stats.py` L1 to L16, and ran a non-test `git grep` for `_build_market_data` and `daily_symbol_stats`. No legacy code, SQL or test was run or imported; no scratch file was written (the corrected file was produced by an in-memory text substitution over the draft).

## 1. Range overview

- P02b-S006 FACT — The range L991 to L1654 holds 22 CREATE TABLE statements (first at L991, last at L1593), 33 CREATE INDEX statements, no CREATE TRIGGER, no CREATE VIEW, and exactly one executable non-DDL statement, the INSERT at L1610. Everything else in the range is comment or blank.
- P02b-S007 FACT — Every CREATE TABLE and every CREATE INDEX in the range uses `IF NOT EXISTS`.
- P02b-S008 FACT — No table in the range is declared `WITHOUT ROWID` or `STRICT`; no column is `GENERATED`; no `COLLATE`, `ON CONFLICT`, `ON DELETE` or `ON UPDATE` clause appears; no index has a partial `WHERE` clause (grep of L991 to L1654 for these keywords found them only inside comments or column names).
- P02b-S009 FACT — No `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `PRAGMA`, `ATTACH`, `ALTER`, `DROP`, `UPDATE` or `DELETE` statement appears in the range (same grep).
- P02b-S010 FACT — The table-number labels in the comments for this range's tables (counting the `fno_ban` banner at L988) are 26 to 28, 31 to 47, 49 and 50. Labels 29 and 30 appear only as "RELOCATED" notes (L1035 to L1036). No "TABLE 48" label appears anywhere in `core/schema.sql` (grep of the whole file).
- P02b-S011 FACT — The comment banner for the first table of the range, `fno_ban` (L987 to L990), lies just before L991, inside part P02a's line range; it is read here for context.

## 2. Table summary

| ID | Label in comment | Table | CREATE TABLE lines | Version tag in its comment | Columns | Primary key | Other table-level constraints | FOREIGN KEY clauses | Column CHECKs | Indexes in range |
|---|---|---|---|---|---|---|---|---|---|---|
| P02b-S012 | TABLE 26 (L988) | `fno_ban` | L991 to L996 | v21 / FIX-135 Item 44 (L988) | 3 | composite (`symbol`, `ban_date`), table-level, L995 | none | none | none | 1 |
| P02b-S013 | TABLE 27 (L1002) | `eod_verification` | L1005 to L1012 | none in its own comment (L1002 says FIX-137 Item 59; the end-of-file trailer L1639 says v22) | 6 | `date` TEXT NOT NULL PRIMARY KEY, L1006 | none | none | none | 0 |
| P02b-S014 | TABLE 28 (L1015) | `cron_heartbeat` | L1019 to L1026 | v23 / FIX-145 (L1015) | 6 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1020 | none | none | none | 2 |
| P02b-S015 | TABLE 31 (L1049) | `order_execution_log` | L1050 to L1077 | v31 (block L1042); two columns tagged v32 (L1072) | 24 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1051 | none | none | none | 3 |
| P02b-S016 | TABLE 32 (L1082) | `trade_slippage_log` | L1083 to L1115 | v31 (block L1042) | 27 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1084 | none | none | none | 4 |
| P02b-S017 | TABLE 33 (L1121) | `market_execution_context` | L1123 to L1140 | v31 (block L1042) | 16 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1124 | none | none | none | 2 |
| P02b-S018 | TABLE 34 (L1148) | `preflight_runs` | L1149 to L1163 | v33 (block L1144) | 13 | `run_id` TEXT PRIMARY KEY, L1150 | none | none | none | 1 |
| P02b-S019 | TABLE 35 (L1166) | `preflight_check_results` | L1167 to L1178 | v33 (block L1144) | 10 | none declared | none | none | none | 2 |
| P02b-S020 | TABLE 36 (L1182) | `preflight_autofix_log` | L1183 to L1193 | v33 (block L1144) | 9 | `log_id` INTEGER PRIMARY KEY AUTOINCREMENT, L1184 | none | none | none | 1 |
| P02b-S021 | TABLE 37 (L1197) | `gtt_state` | L1219 to L1238 | v36 / SLICE2.5-P2 (L1197) | 14 | `gtt_id` INTEGER PRIMARY KEY (no AUTOINCREMENT), L1220 | none | `trade_id` REFERENCES `trades(trade_id)`, L1237 | `status`, L1229 to L1231 | 2 |
| P02b-S022 | TABLE 38 (L1247) | `sr_detector_results` | L1258 to L1291 | schema v37 (L1247) | 29 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1259 | none | `signal_id` REFERENCES `signals(signal_id)`, L1290 | none | 3 |
| P02b-S023 | TABLE 39 (L1303) | `retest_state` | L1313 to L1334 | schema v38 (L1303) | 17 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1314 | none | `signal_id` REFERENCES `signals(signal_id)`, L1333 | `state`, L1325 to L1326 | 2 |
| P02b-S024 | TABLE 40 (L1343) | `excursion_reconstruction_runs` | L1361 to L1372 | schema v39 (L1343) | 10 | `run_id` TEXT PRIMARY KEY, L1362 | none | none | none | 1 |
| P02b-S025 | TABLE 41 (L1390) | `control_tower_findings` | L1391 to L1407 | v40 (block L1378) | 15 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1392 | none (dedupe is a separate UNIQUE index, L1410) | none | none | 3 |
| P02b-S026 | TABLE 42 (L1417) | `control_tower_runs` | L1418 to L1430 | v40 (block L1378) | 11 | `run_id` TEXT PRIMARY KEY, L1419 | none | none | none | 1 |
| P02b-S027 | TABLE 43 (L1433) | `control_tower_trends` | L1435 to L1445 | v40 (block L1378) | 9 | `date` TEXT PRIMARY KEY, L1436 | none | none | none | 0 |
| P02b-S028 | TABLE 44 (L1447) | `control_tower_status` | L1448 to L1460 | v40 (block L1378) | 11 | `run_date` TEXT PRIMARY KEY, L1449 | none | none | none | 0 |
| P02b-S029 | TABLE 45 (L1462) | `control_tower_freshness` | L1463 to L1470 | v40 (block L1378) | 6 | none declared | none | none | none | 1 |
| P02b-S030 | TABLE 46 (L1474) | `config_snapshots` | L1491 to L1500 | schema v41 (L1474) | 8 | `snapshot_id` INTEGER PRIMARY KEY AUTOINCREMENT, L1492 | none | none | none | 1 |
| P02b-S031 | TABLE 47 (L1507) | `eod_broker_reconciliation` | L1519 to L1535 | v42 (L1507) | 15 | `date` TEXT NOT NULL PRIMARY KEY, L1520 | none | none | none | 1 |
| P02b-S032 | TABLE 49 (L1540) | `pb01_watchlist` | L1559 to L1576 | schema v43 (L1540) | 12 | `id` INTEGER PRIMARY KEY AUTOINCREMENT, L1560 | UNIQUE (`symbol`, `trading_date`), L1575 | none | `status`, L1569 to L1570 | 1 |
| P02b-S033 | TABLE 50 (L1582) | `daily_symbol_stats` | L1593 to L1603 | schema v44 (L1582) | 7 | composite (`symbol`, `trading_date`), table-level, L1602 | none | none | none | 1 |

## 3. Tables in detail

Column tables: "NOT NULL" and "DEFAULT" show only what is declared on the column line(s). Inline comments are HISTORICAL, abridged, with any `|` written as "or".

### 3.1 `fno_ban` (L991 to L996)

- P02b-S034 HISTORICAL — Banner L987 to L990: "TABLE 26: fno_ban (v21 / FIX-135 Item 44)"; "Daily F&O ban list from NSE. Fetched at 08:30 IST." The fetch time is a comment only; schedules are A16's.
- P02b-S035 FACT — Table-level constraint: `PRIMARY KEY (symbol, ban_date)` at L995.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S036 | L992 | `symbol` | TEXT | yes | none | — | — |
| P02b-S037 | L993 | `ban_date` | TEXT | yes | none | — | YYYY-MM-DD |
| P02b-S038 | L994 | `fetched_at` | TEXT | yes | none | — | ISO-8601 IST |

### 3.2 `eod_verification` (L1005 to L1012)

- P02b-S039 HISTORICAL — Banner L1001 to L1003: "TABLE 27: eod_verification — FIX-137 Item 59". The banner gives no description and no version tag.
- P02b-S040 FACT — No table-level constraint; the primary key is declared on the `date` column (L1006).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S041 | L1006 | `date` | TEXT | yes | none | PRIMARY KEY | YYYY-MM-DD |
| P02b-S042 | L1007 | `open_trades` | INTEGER | yes | 0 | — | — |
| P02b-S043 | L1008 | `pending_orders` | INTEGER | yes | 0 | — | — |
| P02b-S044 | L1009 | `pnl_variance` | REAL | yes | 0.0 | — | — |
| P02b-S045 | L1010 | `status` | TEXT | yes | 'VERIFIED' | — | VERIFIED or ISSUES_FOUND |
| P02b-S046 | L1011 | `verified_at` | TEXT | yes | none | — | ISO-8601 IST |

### 3.3 `cron_heartbeat` (L1019 to L1026)

- P02b-S047 HISTORICAL — Banner L1014 to L1018: "TABLE 28: cron_heartbeat (v23 / FIX-145)"; "Records successful cron job executions. Each cron job writes a row on success. Used by scripts/check_cron_drift.py to detect missing heartbeats."
- P02b-S048 FACT — No table-level constraint and no FOREIGN KEY.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S049 | L1020 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S050 | L1021 | `job_name` | TEXT | yes | none | — | e.g., "daily_report", "token_watcher" |
| P02b-S051 | L1022 | `executed_at` | TEXT | yes | none | — | ISO-8601 IST when job ran |
| P02b-S052 | L1023 | `status` | TEXT | yes | 'SUCCESS' | — | SUCCESS or PARTIAL or FAILED |
| P02b-S053 | L1024 | `duration_sec` | REAL | no | none | — | job duration in seconds |
| P02b-S054 | L1025 | `message` | TEXT | no | none | — | optional diagnostic |

### 3.4 Relocation note for tables 29 and 30 (L1034 to L1040)

- P02b-S055 HISTORICAL — L1035 to L1040: "TABLE 29: system_metrics" and "TABLE 30: system_metrics_daily" are marked "RELOCATED (O6, v28) to analytics.db"; both "now live in analytics.db (see core/analytics_schema.sql, core/db_connect.py), ATTACHed as schema `analytics` on every connection so unqualified `FROM system_metrics[_daily]` still resolves"; kept out of the trading DB "so the nightly .backup stays small and fast".
- P02b-S056 FACT — No CREATE TABLE for `system_metrics` or `system_metrics_daily` appears in the range. See part P07 (analytics database) and part P01 (ATTACH in `core/db_connect.py`); see part P09a for the backup.

### 3.5 Block note for tables 31 to 33 (L1041 to L1047)

- P02b-S057 HISTORICAL — L1042 to L1046: "TABLES 31-33: Slippage / execution-intelligence RAW data layer (v31)"; "Append-only raw FACTS only — all analytics ... computed ON-DEMAND in reports (no aggregate tables, no stale derived data)"; "Recording is best-effort + decoupled (async event subscribers) so it can NEVER block or fail trade execution."

### 3.6 `order_execution_log` (L1050 to L1077)

- P02b-S058 HISTORICAL — L1049: "TABLE 31: order_execution_log — one row per filled broker order/leg."
- P02b-S059 HISTORICAL — Comment inside the column list, L1072 to L1073: "Slippage tolerance override (Phase 3a, v32) — copied from the parent trade onto the execution row so Phase-2/3b reports can see WHICH rule applied." It introduces `tolerance_fraction_used` (L1074) and `tolerance_source` (L1075).
- P02b-S060 FACT — No table-level constraint and no FOREIGN KEY; `order_id`, `parent_trade_id` and `signal_id` (L1052 to L1054) are plain nullable TEXT columns.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S061 | L1051 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S062 | L1052 | `order_id` | TEXT | no | none | — | — |
| P02b-S063 | L1053 | `parent_trade_id` | TEXT | no | none | — | — |
| P02b-S064 | L1054 | `signal_id` | TEXT | no | none | — | — |
| P02b-S065 | L1055 | `symbol` | TEXT | yes | none | — | — |
| P02b-S066 | L1056 | `strategy_name` | TEXT | no | none | — | — |
| P02b-S067 | L1057 | `leg` | TEXT | yes | none | — | ENTRY / SL / TGT |
| P02b-S068 | L1058 | `order_type` | TEXT | no | none | — | LIMIT / SL / CO ... |
| P02b-S069 | L1059 | `side` | TEXT | no | none | — | BUY / SELL |
| P02b-S070 | L1060 | `intended_price` | REAL | no | none | — | expected/planned price |
| P02b-S071 | L1061 | `actual_price` | REAL | no | none | — | avg fill price |
| P02b-S072 | L1062 | `slippage_rs` | REAL | no | none | — | adverse = positive (paid worse) |
| P02b-S073 | L1063 | `slippage_pct` | REAL | no | none | — | adverse = positive (OM9 convention) |
| P02b-S074 | L1064 | `qty` | INTEGER | no | none | — | — |
| P02b-S075 | L1065 | `filled_qty` | INTEGER | no | none | — | — |
| P02b-S076 | L1066 | `is_partial` | INTEGER | no | 0 | — | — |
| P02b-S077 | L1067 | `retry_count` | INTEGER | no | 0 | — | — |
| P02b-S078 | L1068 | `status` | TEXT | no | none | — | — |
| P02b-S079 | L1069 | `order_timestamp` | TEXT | no | none | — | — |
| P02b-S080 | L1070 | `fill_timestamp` | TEXT | no | none | — | — |
| P02b-S081 | L1071 | `exchange_timestamp` | TEXT | no | none | — | — |
| P02b-S082 | L1074 | `tolerance_fraction_used` | REAL | no | none | — | resolved sl_fraction at entry (NULL for non-sl_fraction) |
| P02b-S083 | L1075 | `tolerance_source` | TEXT | no | none | — | "symbol:IDEA" / "strategy:gap_fade" / "band:0-100" / "global" |
| P02b-S084 | L1076 | `created_at` | TIMESTAMP | no | CURRENT_TIMESTAMP | — | — |

### 3.7 `trade_slippage_log` (L1083 to L1115)

- P02b-S085 HISTORICAL — L1082: "TABLE 32: trade_slippage_log — one row per completed trade (roll-up)." Section comments inside the column list: "entry" (L1092), "stop loss" (L1097), "target" (L1102), "R:R analysis" (L1107).
- P02b-S086 FACT — No table-level constraint and no FOREIGN KEY; `trade_id` (L1085) is a plain nullable TEXT column. `trade_date` is declared with type `DATE` (L1086), the only `DATE` column in the range.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S087 | L1084 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S088 | L1085 | `trade_id` | TEXT | no | none | — | — |
| P02b-S089 | L1086 | `trade_date` | DATE | yes | none | — | — |
| P02b-S090 | L1087 | `symbol` | TEXT | yes | none | — | — |
| P02b-S091 | L1088 | `strategy_name` | TEXT | yes | none | — | — |
| P02b-S092 | L1089 | `side` | TEXT | yes | none | — | LONG / SHORT |
| P02b-S093 | L1090 | `qty` | INTEGER | no | none | — | — |
| P02b-S094 | L1091 | `price_band` | TEXT | no | none | — | e.g. "200-300" (from slippage_bands) |
| P02b-S095 | L1093 | `entry_signal_price` | REAL | no | none | — | — |
| P02b-S096 | L1094 | `entry_fill_price` | REAL | no | none | — | — |
| P02b-S097 | L1095 | `entry_slippage_rs` | REAL | no | none | — | adverse = positive |
| P02b-S098 | L1096 | `entry_slippage_pct` | REAL | no | none | — | — |
| P02b-S099 | L1098 | `sl_trigger_price` | REAL | no | none | — | — |
| P02b-S100 | L1099 | `sl_fill_price` | REAL | no | none | — | — |
| P02b-S101 | L1100 | `sl_slippage_rs` | REAL | no | none | — | adverse = positive |
| P02b-S102 | L1101 | `sl_slippage_pct` | REAL | no | none | — | — |
| P02b-S103 | L1103 | `tgt_price` | REAL | no | none | — | — |
| P02b-S104 | L1104 | `tgt_fill_price` | REAL | no | none | — | — |
| P02b-S105 | L1105 | `tgt_slippage_rs` | REAL | no | none | — | favourable = positive (better fill) |
| P02b-S106 | L1106 | `tgt_slippage_pct` | REAL | no | none | — | — |
| P02b-S107 | L1108 | `planned_sl_distance` | REAL | no | none | — | absolute value of (entry - sl) |
| P02b-S108 | L1109 | `planned_rr` | REAL | no | none | — | strategy's designed R:R |
| P02b-S109 | L1110 | `actual_rr` | REAL | no | none | — | realised R:R after slippage |
| P02b-S110 | L1111 | `rr_damage_pct` | REAL | no | none | — | THE KEY METRIC: % of risk budget eaten |
| P02b-S111 | L1112 | `trade_result` | TEXT | no | none | — | WIN / LOSS / BREAKEVEN |
| P02b-S112 | L1113 | `exit_reason` | TEXT | no | none | — | SL_HIT / TGT_HIT / EOD / MANUAL ... |
| P02b-S113 | L1114 | `created_at` | TIMESTAMP | no | CURRENT_TIMESTAMP | — | — |

### 3.8 `market_execution_context` (L1123 to L1140)

- P02b-S114 HISTORICAL — L1121 to L1122: "TABLE 33: market_execution_context — Priority-2, ALL nullable, best-effort. Bid/ask/spread at execution; absence NEVER blocks recording or execution."
- P02b-S115 FACT — No table-level constraint and no FOREIGN KEY. Apart from the primary key, one column is declared NOT NULL: `symbol` (L1127).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S116 | L1124 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S117 | L1125 | `trade_id` | TEXT | no | none | — | — |
| P02b-S118 | L1126 | `order_id` | TEXT | no | none | — | — |
| P02b-S119 | L1127 | `symbol` | TEXT | yes | none | — | — |
| P02b-S120 | L1128 | `leg` | TEXT | no | none | — | ENTRY / SL / TGT |
| P02b-S121 | L1129 | `captured_at` | TEXT | no | none | — | — |
| P02b-S122 | L1130 | `ltp` | REAL | no | none | — | — |
| P02b-S123 | L1131 | `bid_price` | REAL | no | none | — | — |
| P02b-S124 | L1132 | `ask_price` | REAL | no | none | — | — |
| P02b-S125 | L1133 | `spread_rs` | REAL | no | none | — | — |
| P02b-S126 | L1134 | `spread_pct` | REAL | no | none | — | — |
| P02b-S127 | L1135 | `bid_qty` | INTEGER | no | none | — | — |
| P02b-S128 | L1136 | `ask_qty` | INTEGER | no | none | — | — |
| P02b-S129 | L1137 | `volume_traded` | INTEGER | no | none | — | — |
| P02b-S130 | L1138 | `recent_range_pct` | REAL | no | none | — | — |
| P02b-S131 | L1139 | `created_at` | TIMESTAMP | no | CURRENT_TIMESTAMP | — | — |

### 3.9 Block note for tables 34 to 36 (L1144 to L1146)

- P02b-S132 HISTORICAL — L1144 to L1146: "v32 -> v33 : Pre-flight check audit trail (3 NEW append-only tables). PURE additions: no MIGRATION_TABLES entry (nothing rebuilt); executescript creates them (CREATE IF NOT EXISTS) and the trailing INSERT bumps the version."

### 3.10 `preflight_runs` (L1149 to L1163)

- P02b-S133 HISTORICAL — L1148: "TABLE 34: preflight_runs — one row per pre-flight phase run (A/B/C/FINAL)." The inline comment on `phase` (L1152) lists "A or B or C" only.
- P02b-S134 FACT — No table-level constraint and no FOREIGN KEY. The primary key `run_id` is TEXT without a NOT NULL declaration (L1150).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S135 | L1150 | `run_id` | TEXT | no | none | PRIMARY KEY | — |
| P02b-S136 | L1151 | `run_date` | TEXT | yes | none | — | — |
| P02b-S137 | L1152 | `phase` | TEXT | yes | none | — | A or B or C |
| P02b-S138 | L1153 | `started_at` | TEXT | no | none | — | — |
| P02b-S139 | L1154 | `completed_at` | TEXT | no | none | — | — |
| P02b-S140 | L1155 | `total_checks` | INTEGER | yes | 0 | — | — |
| P02b-S141 | L1156 | `passed` | INTEGER | yes | 0 | — | — |
| P02b-S142 | L1157 | `failed_critical` | INTEGER | yes | 0 | — | — |
| P02b-S143 | L1158 | `warnings` | INTEGER | yes | 0 | — | — |
| P02b-S144 | L1159 | `autofixes_attempted` | INTEGER | yes | 0 | — | — |
| P02b-S145 | L1160 | `autofixes_succeeded` | INTEGER | yes | 0 | — | — |
| P02b-S146 | L1161 | `overall_status` | TEXT | no | none | — | READY or READY_WITH_WARNINGS or CRITICAL_FAILURE |
| P02b-S147 | L1162 | `alert_id` | TEXT | no | none | — | — |

### 3.11 `preflight_check_results` (L1167 to L1178)

- P02b-S148 HISTORICAL — L1166: "TABLE 35: preflight_check_results — one row per check per run."
- P02b-S149 FACT — No PRIMARY KEY, no UNIQUE constraint and no FOREIGN KEY are declared; `run_id` (L1168) is TEXT NOT NULL with no REFERENCES clause to `preflight_runs`.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S150 | L1168 | `run_id` | TEXT | yes | none | — | — |
| P02b-S151 | L1169 | `run_date` | TEXT | no | none | — | — |
| P02b-S152 | L1170 | `check_name` | TEXT | yes | none | — | — |
| P02b-S153 | L1171 | `check_group` | TEXT | no | none | — | — |
| P02b-S154 | L1172 | `criticality` | TEXT | no | none | — | CRITICAL or WARN or INFO |
| P02b-S155 | L1173 | `status` | TEXT | no | none | — | PASS or FAIL or WARN or AUTOFIXED or SKIPPED |
| P02b-S156 | L1174 | `duration_ms` | INTEGER | no | none | — | — |
| P02b-S157 | L1175 | `details_json` | TEXT | no | none | — | — |
| P02b-S158 | L1176 | `fix_attempted` | INTEGER | yes | 0 | — | — |
| P02b-S159 | L1177 | `fix_result` | TEXT | no | none | — | SUCCESS or FAILED or (empty) |

### 3.12 `preflight_autofix_log` (L1183 to L1193)

- P02b-S160 HISTORICAL — L1182: "TABLE 36: preflight_autofix_log — one row per auto-fix attempt (audit trail)."
- P02b-S161 FACT — No table-level constraint and no FOREIGN KEY; `run_id` (L1185) is nullable TEXT with no REFERENCES clause.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S162 | L1184 | `log_id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S163 | L1185 | `run_id` | TEXT | no | none | — | — |
| P02b-S164 | L1186 | `check_name` | TEXT | no | none | — | — |
| P02b-S165 | L1187 | `attempted_at` | TEXT | no | none | — | — |
| P02b-S166 | L1188 | `fix_action` | TEXT | no | none | — | — |
| P02b-S167 | L1189 | `before_state` | TEXT | no | none | — | — |
| P02b-S168 | L1190 | `after_state` | TEXT | no | none | — | — |
| P02b-S169 | L1191 | `result` | TEXT | no | none | — | SUCCESS or FAILED |
| P02b-S170 | L1192 | `error_msg` | TEXT | no | none | — | — |

### 3.13 `gtt_state` (L1219 to L1238)

- P02b-S171 HISTORICAL — Banner L1196 to L1203: "TABLE 37: gtt_state (v36 / SLICE2.5-P2)"; "Durable source of truth for the ONE OCO-GTT ... that protects a CNC (delivery) position overnight"; Phase 1 held this in an in-memory map in `orders/cnc_gtt.py` (`CncGttPlacer._trade_gtts`) that "did NOT survive a restart"; Phase 2 persists it so "the startup + 15-min reconcile can re-verify each GTT against the broker, recreate a missing one, and finalise a GTT-fired exit"; "The BROKER GTT is the authority; this table is the local mirror."
- P02b-S172 HISTORICAL — L1205 to L1208 ("Y6"): a trade may accumulate multiple rows (each recreate is a new broker `gtt_id`, a new row); the one-GTT-per-trade invariant ("M2") is "at most ONE ACTIVE row per open trade at any time" (L1207 to L1208).
- P02b-S173 HISTORICAL — L1210 to L1213: status lifecycle "ACTIVE -> TRIGGERED -> CLEANED" or "ACTIVE -> CANCELLED or EXPIRED or REJECTED"; `needs_review` ("Y2") "latches a qty-mismatch / ownership anomaly so its CRITICAL alert fires ONCE per state".
- P02b-S174 HISTORICAL — L1215 to L1217: "PURE ADDITION ... no MIGRATION_TABLES entry, nothing rebuilt ... The trailing INSERT bumps schema_version to 36."
- P02b-S175 FACT — Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L1237 (the `trades` table is in part P02a's range). Column CHECK on `status` at L1230 to L1231 lists the six values ACTIVE, TRIGGERED, CANCELLED, EXPIRED, REJECTED, CLEANED. No UNIQUE constraint or unique index involves `trade_id` or `status`.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S176 | L1220 | `gtt_id` | INTEGER | no | none | PRIMARY KEY | broker trigger id |
| P02b-S177 | L1221 | `trade_id` | TEXT | yes | none | — | — |
| P02b-S178 | L1222 | `symbol` | TEXT | yes | none | — | — |
| P02b-S179 | L1223 | `exit_side` | TEXT | yes | none | — | SELL (both OCO legs exit a long) |
| P02b-S180 | L1224 | `qty` | INTEGER | yes | none | — | — |
| P02b-S181 | L1225 | `sl_trigger` | REAL | yes | none | — | — |
| P02b-S182 | L1226 | `sl_limit` | REAL | yes | none | — | — |
| P02b-S183 | L1227 | `tgt_trigger` | REAL | yes | none | — | — |
| P02b-S184 | L1228 | `tgt_limit` | REAL | yes | none | — | — |
| P02b-S185 | L1229 to L1231 | `status` | TEXT | yes | none | CHECK (status IN ('ACTIVE','TRIGGERED','CANCELLED', 'EXPIRED','REJECTED','CLEANED')) | ACTIVE or TRIGGERED or CANCELLED or EXPIRED or REJECTED or CLEANED |
| P02b-S186 | L1232 | `needs_review` | INTEGER | yes | 0 | — | Y2 de-dup latch for anomaly alerts |
| P02b-S187 | L1233 | `last_verified_at` | TEXT | no | none | — | ISO-8601 IST of last broker re-verify |
| P02b-S188 | L1234 | `created_at` | TEXT | yes | none | — | — |
| P02b-S189 | L1235 | `updated_at` | TEXT | yes | none | — | — |

### 3.14 `sr_detector_results` (L1258 to L1291)

- P02b-S190 HISTORICAL — Banner L1246 to L1257: "TABLE 38: sr_detector_results (SNR-DETECTOR-V1, schema v37)"; "One row per PLACED candidate observed by the async, non-gating S&R detector"; "SHADOW analytics only ... nothing here gates or modifies an order"; `actual_*`, `win_loss`, `pnl` and `hypothetical_retest_result` "are backfilled by the EOD outcome step (scripts/sr_detector_backfill.py) and are NULL at insert time"; "PURE ADDITION ... The trailing INSERT bumps schema_version to 37."
- P02b-S191 HISTORICAL — L1283 (inside the column list): "backfilled by the EOD outcome step (nullable now):" precedes `actual_result`, `win_loss`, `pnl`, `hypothetical_retest_result` (L1284 to L1287). Note that `actual_fill` (L1268) also carries the inline comment "backfilled (EOD)".
- P02b-S192 FACT — Table-level constraint: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L1290, inline comment "O1 (mirrors screener_results)". The `signals` table is in part P02a's range.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S193 | L1259 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S194 | L1260 | `signal_id` | TEXT | yes | none | — | — |
| P02b-S195 | L1261 | `symbol` | TEXT | yes | none | — | — |
| P02b-S196 | L1262 | `ts` | TEXT | yes | none | — | candidate ts (ISO-8601 IST) |
| P02b-S197 | L1263 | `mode` | TEXT | yes | none | — | 'paper' or 'live' |
| P02b-S198 | L1264 | `strategy` | TEXT | no | none | — | — |
| P02b-S199 | L1265 | `direction` | TEXT | no | none | — | — |
| P02b-S200 | L1266 | `score` | INTEGER | no | none | — | nullable (gate-release path has none) |
| P02b-S201 | L1267 | `intended_entry` | REAL | no | none | — | — |
| P02b-S202 | L1268 | `actual_fill` | REAL | no | none | — | backfilled (EOD) |
| P02b-S203 | L1269 | `nearest_resistance_zone` | TEXT | no | none | — | JSON zone snapshot |
| P02b-S204 | L1270 | `nearest_support_zone` | TEXT | no | none | — | JSON zone snapshot |
| P02b-S205 | L1271 | `dist_to_resistance_pct` | REAL | no | none | — | — |
| P02b-S206 | L1272 | `dist_to_support_pct` | REAL | no | none | — | — |
| P02b-S207 | L1273 | `resistance_confidence` | TEXT | no | none | — | HIGH or MEDIUM or LOW or NONE |
| P02b-S208 | L1274 | `support_confidence` | TEXT | no | none | — | HIGH or MEDIUM or LOW or NONE |
| P02b-S209 | L1275 | `confluence_evidence` | TEXT | no | none | — | JSON: methods/TFs/touches per zone |
| P02b-S210 | L1276 | `breakout_volume` | REAL | no | none | — | — |
| P02b-S211 | L1277 | `flags` | TEXT | no | none | — | JSON array of flag strings |
| P02b-S212 | L1278 | `would_wait_for_retest` | INTEGER | yes | 0 | — | — |
| P02b-S213 | L1279 | `proposed_retest_entry` | REAL | no | none | — | — |
| P02b-S214 | L1280 | `proposed_retest_sl` | REAL | no | none | — | — |
| P02b-S215 | L1281 | `structure_status` | TEXT | no | none | — | OK or NO_CLEAR_STRUCTURE or FETCH_FAILED |
| P02b-S216 | L1282 | `detector_version` | TEXT | yes | none | — | — |
| P02b-S217 | L1284 | `actual_result` | TEXT | no | none | — | — |
| P02b-S218 | L1285 | `win_loss` | TEXT | no | none | — | — |
| P02b-S219 | L1286 | `pnl` | REAL | no | none | — | — |
| P02b-S220 | L1287 | `hypothetical_retest_result` | TEXT | no | none | — | — |
| P02b-S221 | L1288 | `created_at` | TEXT | yes | none | — | — |

### 3.15 `retest_state` (L1313 to L1334)

- P02b-S222 HISTORICAL — Banner L1302 to L1312: "TABLE 39: retest_state (SNR-V2 Phase A, schema v38)"; "One row per candidate DIVERTED into the WAIT_FOR_RETEST monitor (a LONG entry detected inside a HIGH resistance zone, BEFORE any capital reservation)"; "The restart-safe parking store (mirrors gate_state): RetestMonitor rehydrates from it on boot and deletes the row atomically on release (confirm / reject / EOD)"; "NO capital is held while parked"; "PURE ADDITION ... the trailing INSERT bumps schema_version to 38."
- P02b-S223 FACT — Table-level constraint: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L1333. Column CHECK on `state` at L1326 lists WAIT_BREAKOUT, WAIT_RETEST, WAIT_CONFIRM. No UNIQUE constraint on `signal_id` (its index at L1336 to L1337 is non-unique).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S224 | L1314 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S225 | L1315 | `signal_id` | TEXT | yes | none | — | — |
| P02b-S226 | L1316 | `symbol` | TEXT | yes | none | — | — |
| P02b-S227 | L1317 | `direction` | TEXT | yes | none | — | LONG (Phase A is long-only) |
| P02b-S228 | L1318 | `zone_band_low` | REAL | yes | none | — | — |
| P02b-S229 | L1319 | `zone_band_high` | REAL | yes | none | — | — |
| P02b-S230 | L1320 | `entry_price` | REAL | yes | none | — | original derived entry (pre-divert) |
| P02b-S231 | L1321 | `sl_price` | REAL | yes | none | — | original derived SL (pre-divert) |
| P02b-S232 | L1322 | `strategy` | TEXT | yes | none | — | — |
| P02b-S233 | L1323 | `intent` | TEXT | yes | none | — | — |
| P02b-S234 | L1324 | `tier` | TEXT | no | none | — | — |
| P02b-S235 | L1325 to L1326 | `state` | TEXT | yes | none | CHECK (state IN ('WAIT_BREAKOUT', 'WAIT_RETEST', 'WAIT_CONFIRM')) | WAIT_BREAKOUT or WAIT_RETEST or WAIT_CONFIRM |
| P02b-S236 | L1327 | `trigger_price` | REAL | no | none | — | — |
| P02b-S237 | L1328 | `sizing_inputs` | TEXT | no | none | — | JSON snapshot of inputs to re-size at confirm |
| P02b-S238 | L1329 | `timeout_at` | TEXT | no | none | — | ISO-8601 IST deadline |
| P02b-S239 | L1330 | `added_at` | TEXT | yes | none | — | ISO-8601 IST at divert (the retest clock start) |
| P02b-S240 | L1331 | `created_at` | TEXT | yes | none | — | — |

### 3.16 `excursion_reconstruction_runs` (L1361 to L1372)

- P02b-S241 HISTORICAL — Banner L1342 to L1360: "TABLE 40: excursion_reconstruction_runs (MFE/MAE Option B, schema v39)"; "One row per scripts/reconstruct_excursions.py run (daily EOD or historical backfill)"; every examined trade lands in exactly one of three buckets (written, skipped_unreconstructable, failed); "HARD GUARD (asserted by the script): written + skipped + failed == examined"; "PURE ADDITION ... The trailing INSERT bumps to v39."
- P02b-S242 FACT — No table-level constraint, no FOREIGN KEY and no CHECK; the bucket identity in the banner is not expressed in the DDL. The primary key `run_id` is TEXT without a NOT NULL declaration (L1362).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S243 | L1362 | `run_id` | TEXT | no | none | PRIMARY KEY | uuid4 hex |
| P02b-S244 | L1363 | `mode` | TEXT | yes | none | — | 'daily' or 'backfill' |
| P02b-S245 | L1364 | `started_at` | TEXT | yes | none | — | ISO-8601 IST |
| P02b-S246 | L1365 | `completed_at` | TEXT | yes | none | — | ISO-8601 IST |
| P02b-S247 | L1366 | `trades_examined` | INTEGER | yes | none | — | — |
| P02b-S248 | L1367 | `trades_written` | INTEGER | yes | none | — | — |
| P02b-S249 | L1368 | `trades_skipped_unreconstructable` | INTEGER | yes | none | — | — |
| P02b-S250 | L1369 | `trades_failed` | INTEGER | yes | none | — | — |
| P02b-S251 | L1370 | `status` | TEXT | yes | none | — | OK or OK_WITH_NOTES or FAILED |
| P02b-S252 | L1371 | `notes` | TEXT | no | none | — | human-readable summary |

### 3.17 Block note for tables 41 to 45 (L1377 to L1388)

- P02b-S253 HISTORICAL — L1378 to L1387: "TABLES 41-45: control_tower_* — VM Operations Control Tower (Phase 1a, v40)"; "An AGGREGATOR subsystem (ops/control_tower/) that READS existing monitors and adds data-freshness + disk/backup checks"; "Phase 1a creates the FOUNDATION tables only (the size-logger seeds control_tower_trends; the aggregator/report that populate findings/runs/status/freshness arrive in 1b/1c)"; "PURE ADDITION ... The trailing INSERT bumps schema_version to 40."

### 3.18 `control_tower_findings` (L1391 to L1407)

- P02b-S254 HISTORICAL — L1390: "TABLE 41: control_tower_findings — one row per distinct issue (deduped)." L1408 to L1409: "DEDUP IDENTITY = (category, resource_name, reason): the aggregator UPSERTs last_seen/scan_time/status on re-detection rather than inserting a duplicate."
- P02b-S255 FACT — No table-level constraint in the CREATE TABLE; the dedupe identity is the separate `CREATE UNIQUE INDEX IF NOT EXISTS idx_ct_findings_dedup ON control_tower_findings(category, resource_name, reason)` at L1410 to L1411. Of the three indexed columns, `resource_name` (L1397) is nullable; `category` (L1394) and `reason` (L1399) are NOT NULL.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S256 | L1392 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S257 | L1393 | `scan_time` | TEXT | yes | none | — | ISO IST of the scan that (re)detected it |
| P02b-S258 | L1394 | `category` | TEXT | yes | none | — | security or cron or config or freshness or disk or backup |
| P02b-S259 | L1395 | `severity` | TEXT | yes | none | — | CRITICAL or HIGH or MEDIUM or LOW or INFO |
| P02b-S260 | L1396 | `resource_type` | TEXT | no | none | — | table or file or service or mount or job or dir |
| P02b-S261 | L1397 | `resource_name` | TEXT | no | none | — | e.g. 'candles', 'security-watcher', '/dev/sda1' |
| P02b-S262 | L1398 | `location` | TEXT | no | none | — | path / table / host detail |
| P02b-S263 | L1399 | `reason` | TEXT | yes | none | — | why this is a finding |
| P02b-S264 | L1400 | `recommended_action` | TEXT | no | none | — | — |
| P02b-S265 | L1401 | `status` | TEXT | yes | 'OPEN' | — | OPEN or ACKNOWLEDGED or RESOLVED |
| P02b-S266 | L1402 | `first_seen` | TEXT | yes | none | — | — |
| P02b-S267 | L1403 | `last_seen` | TEXT | yes | none | — | — |
| P02b-S268 | L1404 | `acked_at` | TEXT | no | none | — | 1c: set when an operator acks |
| P02b-S269 | L1405 | `resolved_at` | TEXT | no | none | — | 1c: set on auto-resolve (no longer detected) |
| P02b-S270 | L1406 | `remarks` | TEXT | no | none | — | — |

### 3.19 `control_tower_runs` (L1418 to L1430)

- P02b-S271 HISTORICAL — L1417: "TABLE 42: control_tower_runs — one row per tower run (the 17:00 + Sun-18:00 jobs)." The times are a comment only; schedules are A16's.
- P02b-S272 FACT — No table-level constraint. The primary key `run_id` is TEXT without a NOT NULL declaration (L1419).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S273 | L1419 | `run_id` | TEXT | no | none | PRIMARY KEY | uuid4 hex |
| P02b-S274 | L1420 | `started_at` | TEXT | yes | none | — | ISO IST |
| P02b-S275 | L1421 | `completed_at` | TEXT | no | none | — | ISO IST (NULL while running / on crash) |
| P02b-S276 | L1422 | `duration_s` | REAL | no | none | — | — |
| P02b-S277 | L1423 | `checks_run` | INTEGER | yes | 0 | — | — |
| P02b-S278 | L1424 | `findings_total` | INTEGER | yes | 0 | — | — |
| P02b-S279 | L1425 | `critical_count` | INTEGER | yes | 0 | — | — |
| P02b-S280 | L1426 | `high_count` | INTEGER | yes | 0 | — | — |
| P02b-S281 | L1427 | `medium_count` | INTEGER | yes | 0 | — | — |
| P02b-S282 | L1428 | `low_count` | INTEGER | yes | 0 | — | — |
| P02b-S283 | L1429 | `status` | TEXT | yes | 'RUNNING' | — | RUNNING or OK or OK_WITH_FINDINGS or FAILED |

### 3.20 `control_tower_trends` (L1435 to L1445)

- P02b-S284 HISTORICAL — L1433 to L1434: "TABLE 43: control_tower_trends — one row per DATE (PK). The Phase-1a size-logger UPSERTs the four size fields; the aggregator (1b/1c) fills health_score + counts."
- P02b-S285 FACT — No table-level constraint and no index in the range. The primary key `date` is TEXT without a NOT NULL declaration (L1436).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S286 | L1436 | `date` | TEXT | no | none | PRIMARY KEY | YYYY-MM-DD IST |
| P02b-S287 | L1437 | `health_score` | INTEGER | no | none | — | 0-100 (aggregator, 1b/1c) |
| P02b-S288 | L1438 | `critical_count` | INTEGER | no | none | — | — |
| P02b-S289 | L1439 | `high_count` | INTEGER | no | none | — | — |
| P02b-S290 | L1440 | `medium_count` | INTEGER | no | none | — | — |
| P02b-S291 | L1441 | `disk_used_pct` | REAL | no | none | — | FRESH (shutil.disk_usage), NOT system_metrics |
| P02b-S292 | L1442 | `backup_size_mb` | REAL | no | none | — | — |
| P02b-S293 | L1443 | `log_size_mb` | REAL | no | none | — | — |
| P02b-S294 | L1444 | `db_size_mb` | REAL | no | none | — | — |

### 3.21 `control_tower_status` (L1448 to L1460)

- P02b-S295 HISTORICAL — L1447: "TABLE 44: control_tower_status" (labelled "ChatGPT B" in the comment): "one current-status row per run_date."
- P02b-S296 FACT — No table-level constraint and no index in the range. The primary key `run_date` is TEXT without a NOT NULL declaration (L1449).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S297 | L1449 | `run_date` | TEXT | no | none | PRIMARY KEY | YYYY-MM-DD IST (last run of the day wins) |
| P02b-S298 | L1450 | `security_status` | TEXT | no | none | — | OK or WARN or CRITICAL or UNKNOWN |
| P02b-S299 | L1451 | `cron_status` | TEXT | no | none | — | — |
| P02b-S300 | L1452 | `config_status` | TEXT | no | none | — | — |
| P02b-S301 | L1453 | `freshness_status` | TEXT | no | none | — | — |
| P02b-S302 | L1454 | `disk_pct` | REAL | no | none | — | — |
| P02b-S303 | L1455 | `backup_size_mb` | REAL | no | none | — | — |
| P02b-S304 | L1456 | `critical_count` | INTEGER | no | none | — | — |
| P02b-S305 | L1457 | `high_count` | INTEGER | no | none | — | — |
| P02b-S306 | L1458 | `overall_status` | TEXT | no | none | — | ChatGPT D top-line (1c) |
| P02b-S307 | L1459 | `last_successful_run` | TEXT | no | none | — | ISO IST of the last OK run |

### 3.22 `control_tower_freshness` (L1463 to L1470)

- P02b-S308 HISTORICAL — L1462: "TABLE 45: control_tower_freshness" (labelled "ChatGPT C" in the comment): "per-stage data-pipeline freshness."
- P02b-S309 FACT — No PRIMARY KEY and no UNIQUE constraint are declared; the only index, `idx_ct_freshness_run` on (`run_date`, `stage`) at L1471, is non-unique.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S310 | L1464 | `run_date` | TEXT | yes | none | — | YYYY-MM-DD IST |
| P02b-S311 | L1465 | `stage` | TEXT | yes | none | — | candles or signals or orders or executions or reconstruction or eod |
| P02b-S312 | L1466 | `expected_by` | TEXT | no | none | — | ISO IST deadline |
| P02b-S313 | L1467 | `actual_at` | TEXT | no | none | — | ISO IST when it happened (NULL = missing) |
| P02b-S314 | L1468 | `delay_minutes` | INTEGER | no | none | — | actual - expected (NULL if missing / NA) |
| P02b-S315 | L1469 | `status` | TEXT | yes | none | — | OK or LATE or MISSING or NA |

### 3.23 `config_snapshots` (L1491 to L1500)

- P02b-S316 HISTORICAL — Banner L1473 to L1490: "TABLE 46: config_snapshots (W0 — daily-report redesign foundation, schema v41)"; "One row per distinct resolved-config seen on a date"; the system writes the full effective config "(core/config_snapshotter.snapshot_config, at startup after config is resolved)" so the daily report's Config sheet and any re-run read "the config AS IT WAS on that date, DB-purely (the report reads ONLY this table, never YAML)".
- P02b-S317 HISTORICAL — L1481 to L1483: "Idempotent by (snapshot_date, config_hash): a same-config restart is a no-op; a config change on a same-day restart writes a NEW row"; "config_hash = sha256 of the stable/sorted config_json". L1486 to L1489: "PURE ADDITION ... The trailing INSERT bumps schema_version to 41."
- P02b-S318 FACT — No table-level constraint, no UNIQUE constraint and no unique index on (`snapshot_date`, `config_hash`); the only index is the non-unique `idx_config_snapshots_date` on `snapshot_date` (L1501 to L1502).
- P02b-S319 FACT — L1504 is a separator comment line only.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S320 | L1492 | `snapshot_id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S321 | L1493 | `snapshot_date` | TEXT | yes | none | — | YYYY-MM-DD IST (the run/trading date) |
| P02b-S322 | L1494 | `snapshot_ts` | TEXT | yes | none | — | ISO-8601 IST — when the row was written |
| P02b-S323 | L1495 | `account_id` | TEXT | no | none | — | primary/selected account (e.g. <ACCOUNT_ID>) |
| P02b-S324 | L1496 | `mode` | TEXT | no | none | — | 'PAPER' or 'LIVE' |
| P02b-S325 | L1497 | `trade_type` | TEXT | no | none | — | 'INTRADAY' or 'DELIVERY' or 'BOTH' |
| P02b-S326 | L1498 | `config_hash` | TEXT | yes | none | — | sha256 of config_json (stable/sorted) |
| P02b-S327 | L1499 | `config_json` | TEXT | yes | none | — | FULL resolved AppConfig (model_dump json) |

### 3.24 `eod_broker_reconciliation` (L1519 to L1535)

- P02b-S328 HISTORICAL — Banner L1506 to L1518: "TABLE 47: eod_broker_reconciliation (P1 — broker-authoritative EOD verdict, v42)"; "One row per date"; it "REPLACES eod_verify's local-only false-VERIFY"; "Written by scripts/eod_broker_reconcile.py @15:58 (standalone, own creds → runs even if the trading process was DOWN at EOD)"; overall verdict VERIFIED, ISSUES or UNVERIFIED; required dimensions (positions, orders, broker day-realized P&L) unavailable means UNVERIFIED; MARGIN supplemental, NOT_CHECKED after 15:45; LEDGER is "the fm_ledger 3-balance invariant"; "Paper = SELF_CONSISTENCY (labeled)" (paper side not traced); shadow columns record the same-day `eod_verify` verdict and mismatch; "PURE ADDITION (no rebuild). Trailing INSERT → v42."
- P02b-S329 FACT — No table-level constraint and no CHECK. The primary key `date` is TEXT NOT NULL (L1520), and a separate non-unique index `idx_eod_broker_reconciliation_date` is also declared on `date` (L1536 to L1537).

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S330 | L1520 | `date` | TEXT | yes | none | PRIMARY KEY | YYYY-MM-DD IST |
| P02b-S331 | L1521 | `mode` | TEXT | yes | none | — | LIVE or PAPER |
| P02b-S332 | L1522 | `self_consistency` | INTEGER | yes | 0 | — | 1 in paper (no independent broker) |
| P02b-S333 | L1523 | `authoritative` | INTEGER | yes | 0 | — | 0=shadow, 1=authoritative |
| P02b-S334 | L1524 | `broker_reachable` | INTEGER | yes | 0 | — | — |
| P02b-S335 | L1525 | `positions_status` | TEXT | no | none | — | VERIFIED or ISSUES or UNVERIFIED (REQUIRED) |
| P02b-S336 | L1526 | `orders_status` | TEXT | no | none | — | VERIFIED or ISSUES or UNVERIFIED (REQUIRED) |
| P02b-S337 | L1527 | `pnl_status` | TEXT | no | none | — | VERIFIED or ISSUES or UNVERIFIED (REQUIRED; broker day-realized vs local) |
| P02b-S338 | L1528 | `ledger_status` | TEXT | no | none | — | VERIFIED or ISSUES (local invariant) |
| P02b-S339 | L1529 | `margin_status` | TEXT | no | none | — | VERIFIED or ISSUES or NOT_CHECKED (SUPPLEMENTAL, reliability-gated) |
| P02b-S340 | L1530 | `overall_status` | TEXT | yes | none | — | VERIFIED or ISSUES or UNVERIFIED |
| P02b-S341 | L1531 | `eod_verify_status` | TEXT | no | none | — | same-day eod_verify verdict (shadow comparison) |
| P02b-S342 | L1532 | `mismatch` | INTEGER | no | none | — | 1 if P1 disagrees with eod_verify (shadow readiness) |
| P02b-S343 | L1533 | `detail` | TEXT | no | none | — | human-readable per-dimension notes (NEVER a secret) |
| P02b-S344 | L1534 | `verified_at` | TEXT | yes | none | — | — |

### 3.25 `pb01_watchlist` (L1559 to L1576)

- P02b-S345 HISTORICAL — Banner L1539 to L1546: "TABLE 49: pb01_watchlist (V3 Step 10b — PB-01 overnight watchlist, schema v43)"; "The STATEFUL OVERNIGHT WATCHLIST for the PB-01 'Breakout + Retest' playbook"; an EOD Chartink breakout is captured on day D with the LEVEL it cleared and "a single valid trading_date = D+1"; the next-morning entry stage (09:20-11:00) loads today's rows; "ANALYSIS ONLY — never a position, never capital; PB-01 is SHADOW (would-be records only), enabled:false (fail-closed)."
- P02b-S346 HISTORICAL — L1547 to L1553: two "load-bearing invariants" (approval attribution names omitted): "UNIQUE (symbol, trading_date) — DB-level dedupe"; "trading_date — the ANTI-REHYDRATION key (FIX-046 class): on load, DISCARD any row whose trading_date != today ... Enforced in code + a test". L1555 to L1557: "PURE ADDITION ... The trailing INSERT bumps to v43."
- P02b-S347 FACT — Table-level constraint: `UNIQUE (symbol, trading_date)` at L1575, matching the first stated invariant. The second invariant (discard on load) has no DDL counterpart; it is code (parts P04 to P06). Column CHECK on `status` at L1570 lists PENDING, CONSUMED, EXPIRED_WINDOW, INVALIDATED, SKIPPED_GAP.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S348 | L1560 | `id` | INTEGER | no | none | PRIMARY KEY AUTOINCREMENT | — |
| P02b-S349 | L1561 | `symbol` | TEXT | yes | none | — | — |
| P02b-S350 | L1562 | `trading_date` | TEXT | yes | none | — | YYYY-MM-DD IST; the SINGLE valid session (D+1).; ANTI-REHYDRATION key: load discards trading_date != today. |
| P02b-S351 | L1564 | `level` | REAL | yes | none | — | retest LEVEL = highest daily HIGH of the 20 sessions BEFORE the breakout day (WE compute it; never the payload) (comment continues on L1565) |
| P02b-S352 | L1566 | `breakout_date` | TEXT | yes | none | — | YYYY-MM-DD IST; the session whose daily close cleared LEVEL. |
| P02b-S353 | L1567 | `source` | TEXT | yes | none | — | scanner name (pb01_breakout_retest). |
| P02b-S354 | L1568 | `sr_zone_json` | TEXT | no | none | — | nearest 30m/1h sr_detector zone to LEVEL (S&R validation programme). |
| P02b-S355 | L1569 to L1570 | `status` | TEXT | yes | 'PENDING' | CHECK (status IN ('PENDING','CONSUMED','EXPIRED_WINDOW','INVALIDATED','SKIPPED_GAP')) | — |
| P02b-S356 | L1571 | `outcome_json` | TEXT | no | none | — | entry-stage outcome detail (confirmation candle / gap / expiry ts). |
| P02b-S357 | L1572 | `captured_at` | TEXT | yes | none | — | ISO-8601 IST at capture (EOD). |
| P02b-S358 | L1573 | `created_at` | TEXT | yes | none | — | ISO-8601 IST row-insert. |
| P02b-S359 | L1574 | `consumed_at` | TEXT | no | none | — | ISO-8601 IST when CONSUMED/EXPIRED/INVALIDATED/SKIPPED. |

### 3.26 `daily_symbol_stats` (L1593 to L1603)

- P02b-S360 HISTORICAL — Banner L1581 to L1592: "TABLE 50: daily_symbol_stats (M-S4 — pre-market daily-stats cache, schema v44)"; computed "PRE-MARKET (~08:30 cron, AFTER the token refresh) from daily candles that CLOSED BEFORE trading_date, via the shared rate-limited OhlcFetcher"; "The screener's _build_market_data does an O(1) READ of this table"; on a cache miss the screener keeps "today's fail-safe (0.0 / 0.5)"; "this table NEVER blocks, fetches on the hot path, or fabricates a value"; "All behind a default-OFF wiring flag until the M-S4 threshold re-fit ships (GATE 1)"; "PURE ADDITION ... The trailing INSERT bumps to v44."
- P02b-S361 FACT — Table-level constraint: `PRIMARY KEY (symbol, trading_date)` at L1602 (inline comment "natural dedupe + O(1) point lookup by the screener"). The banner does not name the module or script that writes the rows.

| ID | Line | Column | Declared type | NOT NULL | DEFAULT | PK / UNIQUE / CHECK / REFERENCES | Inline comment (HISTORICAL, abridged) |
|---|---|---|---|---|---|---|---|
| P02b-S362 | L1594 | `symbol` | TEXT | yes | none | — | — |
| P02b-S363 | L1595 | `trading_date` | TEXT | yes | none | — | YYYY-MM-DD IST; the session these stats are FOR; (computed ONLY from candles closed BEFORE it — NO lookahead). |
| P02b-S364 | L1597 | `prev_close` | REAL | no | none | — | previous session's daily close. |
| P02b-S365 | L1598 | `avg_volume_20d` | REAL | no | none | — | SMA of daily volume over the 20 sessions before trading_date. |
| P02b-S366 | L1599 | `atr14` | REAL | no | none | — | Wilder ATR(14) on daily candles (the atr_filter ADR% input). |
| P02b-S367 | L1600 | `rsi14` | REAL | no | none | — | Wilder RSI(14) on daily closes (the rsi_range input). |
| P02b-S368 | L1601 | `computed_at` | TEXT | yes | none | — | ISO-8601 IST when the row was computed (staleness / audit). |

## 4. Indexes, triggers and views in the range

| ID | Lines | Index | Table | Columns (in order) | UNIQUE | Partial WHERE | IF NOT EXISTS | Comment (HISTORICAL) |
|---|---|---|---|---|---|---|---|---|
| P02b-S369 | L998 to L999 | `idx_fno_ban_date` | `fno_ban` | `ban_date` | no | none | yes | — |
| P02b-S370 | L1028 to L1029 | `idx_cron_heartbeat_job_name` | `cron_heartbeat` | `job_name` | no | none | yes | — |
| P02b-S371 | L1031 to L1032 | `idx_cron_heartbeat_executed_at` | `cron_heartbeat` | `executed_at` | no | none | yes | — |
| P02b-S372 | L1078 | `idx_oel_trade` | `order_execution_log` | `parent_trade_id` | no | none | yes | — |
| P02b-S373 | L1079 | `idx_oel_date` | `order_execution_log` | `created_at` | no | none | yes | — |
| P02b-S374 | L1080 | `idx_oel_symbol` | `order_execution_log` | `symbol` | no | none | yes | — |
| P02b-S375 | L1116 | `idx_tsl_date` | `trade_slippage_log` | `trade_date` | no | none | yes | — |
| P02b-S376 | L1117 | `idx_tsl_strategy` | `trade_slippage_log` | `strategy_name` | no | none | yes | — |
| P02b-S377 | L1118 | `idx_tsl_band` | `trade_slippage_log` | `price_band` | no | none | yes | — |
| P02b-S378 | L1119 | `idx_tsl_symbol` | `trade_slippage_log` | `symbol` | no | none | yes | — |
| P02b-S379 | L1141 | `idx_mec_trade` | `market_execution_context` | `trade_id` | no | none | yes | — |
| P02b-S380 | L1142 | `idx_mec_symbol` | `market_execution_context` | `symbol` | no | none | yes | — |
| P02b-S381 | L1164 | `idx_pfr_date` | `preflight_runs` | `run_date` | no | none | yes | — |
| P02b-S382 | L1179 | `idx_pfcr_run` | `preflight_check_results` | `run_id` | no | none | yes | — |
| P02b-S383 | L1180 | `idx_pfcr_name` | `preflight_check_results` | `check_name`, `run_date` | no | none | yes | — |
| P02b-S384 | L1194 | `idx_pfal_run` | `preflight_autofix_log` | `run_id` | no | none | yes | — |
| P02b-S385 | L1240 to L1241 | `idx_gtt_state_trade_id` | `gtt_state` | `trade_id` | no | none | yes | — |
| P02b-S386 | L1243 to L1244 | `idx_gtt_state_status` | `gtt_state` | `status` | no | none | yes | — |
| P02b-S387 | L1293 to L1294 | `idx_sr_detector_results_signal_id` | `sr_detector_results` | `signal_id` | no | none | yes | — |
| P02b-S388 | L1296 to L1297 | `idx_sr_detector_results_ts` | `sr_detector_results` | `ts` | no | none | yes | — |
| P02b-S389 | L1299 to L1300 | `idx_sr_detector_results_mode` | `sr_detector_results` | `mode` | no | none | yes | — |
| P02b-S390 | L1336 to L1337 | `idx_retest_state_signal_id` | `retest_state` | `signal_id` | no | none | yes | — |
| P02b-S391 | L1339 to L1340 | `idx_retest_state_symbol` | `retest_state` | `symbol` | no | none | yes | — |
| P02b-S392 | L1374 to L1375 | `idx_excursion_recon_runs_started` | `excursion_reconstruction_runs` | `started_at` | no | none | yes | — |
| P02b-S393 | L1410 to L1411 | `idx_ct_findings_dedup` | `control_tower_findings` | `category`, `resource_name`, `reason` | yes | none | yes | L1408 to L1409: the dedupe identity used by the aggregator UPSERT |
| P02b-S394 | L1412 to L1413 | `idx_ct_findings_status` | `control_tower_findings` | `status`, `severity` | no | none | yes | — |
| P02b-S395 | L1414 to L1415 | `idx_ct_findings_last_seen` | `control_tower_findings` | `last_seen` | no | none | yes | L1414: "1b query path (auto-resolve sweep)" |
| P02b-S396 | L1431 | `idx_ct_runs_started` | `control_tower_runs` | `started_at` | no | none | yes | — |
| P02b-S397 | L1471 | `idx_ct_freshness_run` | `control_tower_freshness` | `run_date`, `stage` | no | none | yes | — |
| P02b-S398 | L1501 to L1502 | `idx_config_snapshots_date` | `config_snapshots` | `snapshot_date` | no | none | yes | — |
| P02b-S399 | L1536 to L1537 | `idx_eod_broker_reconciliation_date` | `eod_broker_reconciliation` | `date` | no | none | yes | — |
| P02b-S400 | L1578 to L1579 | `idx_pb01_watchlist_trading_date` | `pb01_watchlist` | `trading_date` | no | none | yes | — |
| P02b-S401 | L1605 to L1606 | `idx_daily_symbol_stats_date` | `daily_symbol_stats` | `trading_date` | no | none | yes | — |

- P02b-S402 FACT — No CREATE TRIGGER and no CREATE VIEW statement appears in L991 to L1654. (The file's only trigger, `trg_trades_terminal_status_guard`, is at L291, in part P02a's range.)
- P02b-S403 INTERPRETATION (SQLite semantics) — Besides the 33 named indexes, SQLite creates an automatic index for each non-INTEGER PRIMARY KEY and each UNIQUE table constraint: here for `fno_ban` (L995), `eod_verification` (L1006), `preflight_runs` (L1150), `excursion_reconstruction_runs` (L1362), `control_tower_runs` (L1419), `control_tower_trends` (L1436), `control_tower_status` (L1449), `eod_broker_reconciliation` (L1520), `pb01_watchlist` UNIQUE (L1575) and `daily_symbol_stats` (L1602). An `INTEGER PRIMARY KEY` column (for example `gtt_state.gtt_id`, L1220) is an alias of the rowid and gets no separate index.

## 5. Non-DDL statements and schema version (brief items 4 and 7)

- P02b-S404 FACT — The only non-DDL statement in the range is L1610: `INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '45');` with the trailing comment "W8 (P3-r10): trades gains closure_source + exit_mechanism. REBUILD (see MIGRATION_TABLES[45]) — not a pure addition."
- P02b-S405 FACT — A grep of the whole of `core/schema.sql` for `INSERT` finds only this one executable INSERT (L1610); every other match is inside a comment. It is therefore the only statement in the file that sets `schema_version`, and the final value the file sets is the TEXT value `'45'`.
- P02b-S406 FACT — The form is `INSERT OR REPLACE` (not plain `INSERT` and not `INSERT OR IGNORE`). `schema_meta` is defined at L29 to L32 with `key TEXT PRIMARY KEY` and `value TEXT NOT NULL` (part P02a's range).
- P02b-S407 INTERPRETATION (SQLite semantics) — Because `key` is the primary key, each execution of L1610 deletes any existing `schema_version` row and writes `'45'`, whatever value was stored before. The version value is stored as TEXT; any numeric comparison of it depends on the reading code (part P03).
- P02b-S408 FACT — `MIGRATION_TABLES` is defined in `core/migrations.py` at L115; its key `45` maps to `["trades"]` at L130, consistent with the "REBUILD" note at L1610. The `trades` table is in part P02a's range. Migration behaviour: see part P03.

Version statements in the range's comments (all HISTORICAL; "pure" or "rebuild" as the comment says it):

| ID | Comment line(s) | Version | Block | What the comment says about how it is applied | `MIGRATION_TABLES` pointer (part P03) |
|---|---|---|---|---|---|
| P02b-S409 | L988 | v21 | `fno_ban` | Nothing about pure or rebuild | no key (dict at `core/migrations.py` L115 to L133) |
| P02b-S410 | L1002 | none | `eod_verification` | Nothing; the trailer L1639 lists it under v22 | no key |
| P02b-S411 | L1015 | v23 | `cron_heartbeat` | Nothing about pure or rebuild | no key |
| P02b-S412 | L1035 to L1040 | v28 | tables 29 and 30 relocated to analytics.db | Relocation, not in this file | L119 to L122 comment mentions the relocation (part P03, part P07) |
| P02b-S413 | L1042 to L1047 | v31 | tables 31 to 33 | Nothing explicit in the block; later banners (L1216, L1255) cite "v31 slippage" as the same pure-addition pattern | no key |
| P02b-S414 | L1072 to L1073 | v32 | two new columns on `order_execution_log` | The comment does not say pure or rebuild | key `32` maps to `["trades", "order_execution_log"]` at `core/migrations.py` L126 (a rebuild) |
| P02b-S415 | L1144 to L1146 | v32 to v33 | tables 34 to 36 | "PURE additions: no MIGRATION_TABLES entry (nothing rebuilt)"; "the trailing INSERT bumps the version" | L127 comment: "33: pure additions" |
| P02b-S416 | L1197, L1215 to L1217 | v36 | `gtt_state` | "PURE ADDITION ... no MIGRATION_TABLES entry"; "trailing INSERT bumps schema_version to 36" | L131 comment: "36 (gtt_state) + 37 (sr_detector_results): pure additions" |
| P02b-S417 | L1247, L1254 to L1256 | v37 | `sr_detector_results` | "PURE ADDITION"; "to 37" | same comment, L131 |
| P02b-S418 | L1303, L1310 to L1311 | v38 | `retest_state` | "PURE ADDITION"; "to 38" | key `38` maps to `["signals"]` (a `signals` rebuild, part P02a's table) at L132 |
| P02b-S419 | L1343, L1358 to L1359 | v39 | `excursion_reconstruction_runs` | "PURE ADDITION ... no MIGRATION_TABLES entry"; "to v39" | no key |
| P02b-S420 | L1378, L1384 to L1387 | v40 | tables 41 to 45 | "PURE ADDITION ... no MIGRATION_TABLES entry"; "to 40" | no key |
| P02b-S421 | L1474, L1486 to L1489 | v41 | `config_snapshots` | "PURE ADDITION ... no MIGRATION_TABLES entry"; "to 41" | no key |
| P02b-S422 | L1507, L1517 | v42 | `eod_broker_reconciliation` | "PURE ADDITION (no rebuild). Trailing INSERT → v42." | no key |
| P02b-S423 | L1540, L1555 to L1557 | v43 | `pb01_watchlist` | "PURE ADDITION ... no MIGRATION_TABLES entry"; "to v43" | no key |
| P02b-S424 | L1582, L1590 to L1591 | v44 | `daily_symbol_stats` | "PURE ADDITION ... no MIGRATION_TABLES entry"; "to v44" | no key |
| P02b-S425 | L1610 | v45 | `trades` (part P02a's table) | "REBUILD (see MIGRATION_TABLES[45]) — not a pure addition" | key `45` maps to `["trades"]` at L130 |

- P02b-S426 FACT — Ten banners in the range (L1146; L1217; L1256; L1310 to L1311; L1359; L1386 to L1387; L1488 to L1489; L1517; L1556 to L1557; L1591) say that the trailing INSERT bumps the version. Nine state their own block's number (36, 37, 38, 39, 40, 41, 42, 43, 44). L1146 states no number ("the trailing INSERT bumps the version"); its block heading (L1144) says "v32 -> v33". At the baseline there is a single trailing INSERT, and it sets `'45'` (L1610).
- P02b-S427 INTERPRETATION — The banners read as written when each block was added, with the one INSERT line edited to the new number at each bump. The file's git history was not examined, so this is not established.
- P02b-S428 FACT — Versions v29, v30, v34 and v35 are not mentioned in the range's comments; they are mentioned at L155 (v29), L193 (v30), L210, L213 and L236 (v34), and L227 to L234 (v35), all in part P02a's range.
- P02b-S429 HISTORICAL — End-of-file trailer L1612 to L1654: it opens "END OF SCHEMA v24" and lists version history from v1 to v27 only; it does not mention v28 to v45. At L1644 to L1645 it says the v25 change was "Applied to existing DBs via core/migrations.py table rebuild", and at L1649 that v26 used the "Same table-rebuild migration".
- P02b-S430 HISTORICAL — For comparison only (part P02a's range): the header says "Version: 1" (L4) and "DO NOT modify this file by hand without bumping schema_version and adding a corresponding migration in state_store.py" (L20 to L21), while the range's comments (L1145, L1610, L1645) point to `core/migrations.py` / `MIGRATION_TABLES`.

## 6. Counts for the range L991 to L1654

| ID | Item | Count |
|---|---|---|
| P02b-S431 | CREATE TABLE statements | 22 |
| P02b-S432 | Columns (all 22 tables) | 278 |
| P02b-S433 | CREATE INDEX statements (named) | 33, of which 1 UNIQUE (`idx_ct_findings_dedup`) and 0 partial |
| P02b-S434 | CREATE TRIGGER statements | 0 |
| P02b-S435 | CREATE VIEW statements | 0 |
| P02b-S436 | INSERT statements | 1 (L1610) |
| P02b-S437 | FOREIGN KEY clauses | 3 (L1237, L1290, L1333) |
| P02b-S438 | Column CHECK constraints | 3 (`gtt_state.status`, `retest_state.state`, `pb01_watchlist.status`) |
| P02b-S439 | Table-level UNIQUE constraints | 1 (`pb01_watchlist`, L1575) |
| P02b-S440 | Composite primary keys | 2 (`fno_ban`, `daily_symbol_stats`) |
| P02b-S441 | Tables with `INTEGER PRIMARY KEY AUTOINCREMENT` | 10 (`cron_heartbeat`, `order_execution_log`, `trade_slippage_log`, `market_execution_context`, `preflight_autofix_log`, `sr_detector_results`, `retest_state`, `control_tower_findings`, `config_snapshots`, `pb01_watchlist`) |
| P02b-S442 | Tables with no declared primary key | 2 (`preflight_check_results`, `control_tower_freshness`) |
| P02b-S443 | Columns with declared type other than INTEGER, TEXT or REAL | 4 (`trade_slippage_log.trade_date` DATE; `created_at` TIMESTAMP in `order_execution_log`, `trade_slippage_log`, `market_execution_context`) |

## 7. Data category of each table (as stated by its comment or name only)

Each category below is an INTERPRETATION of the HISTORICAL comment or table name cited in the Basis column.

| ID | Table | Category | Basis |
|---|---|---|---|
| P02b-S444 | `fno_ban` | other: external reference data | L989 "Daily F&O ban list from NSE" |
| P02b-S445 | `eod_verification` | audit or evidence log (by name only) | name; banner L1002 gives no description |
| P02b-S446 | `cron_heartbeat` | scheduler or heartbeat | L1016 "Records successful cron job executions" |
| P02b-S447 | `order_execution_log` | audit or evidence log | L1042 to L1043 "RAW data layer ... Append-only raw FACTS"; L1049 |
| P02b-S448 | `trade_slippage_log` | audit or evidence log | L1042 to L1043; L1082 "one row per completed trade (roll-up)" |
| P02b-S449 | `market_execution_context` | audit or evidence log | L1042 to L1043; L1121 to L1122 |
| P02b-S450 | `preflight_runs` | audit or evidence log | L1144 "Pre-flight check audit trail" |
| P02b-S451 | `preflight_check_results` | audit or evidence log | L1144; L1166 |
| P02b-S452 | `preflight_autofix_log` | audit or evidence log | L1182 "(audit trail)" |
| P02b-S453 | `gtt_state` | trading state | L1198 "Durable source of truth ... local mirror" (L1203) |
| P02b-S454 | `sr_detector_results` | analytics or report output | L1249 "SHADOW analytics only" |
| P02b-S455 | `retest_state` | trading state (candidate parking state; "NO capital is held") | L1306 "restart-safe parking store"; L1308 |
| P02b-S456 | `excursion_reconstruction_runs` | audit or evidence log | L1345 "Audit trail for the post-EOD MFE/MAE reconstruction" |
| P02b-S457 | `control_tower_findings` | analytics or report output (monitoring) | L1378 to L1379 Control Tower "AGGREGATOR"; L1390 |
| P02b-S458 | `control_tower_runs` | analytics or report output (monitoring run record) | L1417 "one row per tower run" |
| P02b-S459 | `control_tower_trends` | analytics or report output (monitoring) | L1433 to L1434 |
| P02b-S460 | `control_tower_status` | analytics or report output (monitoring) | L1447 "one current-status row per run_date" |
| P02b-S461 | `control_tower_freshness` | analytics or report output (monitoring) | L1462 "per-stage data-pipeline freshness" |
| P02b-S462 | `config_snapshots` | configuration snapshot | L1474 to L1479 |
| P02b-S463 | `eod_broker_reconciliation` | audit or evidence log (reconciliation verdict) | L1507 to L1508 "broker-authoritative EOD reconcile verdict" |
| P02b-S464 | `pb01_watchlist` | other: shadow watchlist state ("ANALYSIS ONLY") | L1541, L1544 to L1545 |
| P02b-S465 | `daily_symbol_stats` | other: market-data-derived cache | L1582 "pre-market daily-stats cache" |

## 8. Application routes (what the text shows; how it is executed is parts P01 and P03)

- P02b-S466 INTERPRETATION (SQLite semantics) — Normal route on a database where a table of this range does not yet exist: its `CREATE TABLE IF NOT EXISTS` creates it with the definition shown, and each `CREATE INDEX IF NOT EXISTS` creates the index.
- P02b-S467 INTERPRETATION (SQLite semantics) — Re-apply route on a database where a table of the same name already exists: the `CREATE TABLE IF NOT EXISTS` does nothing, and in particular does not add columns, CHECKs or FOREIGN KEY clauses added to the text later (for example the v32 columns at L1074 to L1075). Such changes reach an existing database only through a rebuild or ALTER performed by code (part P03). An index whose name already exists is likewise skipped, even if its column list in the text has changed.
- P02b-S468 HISTORICAL — The range's comments describe the file as re-executed on existing databases: "executescript creates them" (L1145) and "on the schema re-apply" (L1215, L1386, L1488).
- P02b-S469 FACT — The range contains no transaction-control statement (section 1). INTERPRETATION: whether a re-apply runs inside one transaction, and what remains if execution stops at a failing statement, depends on the executing code (parts P01 and P03); for this range it is UNKNOWN / NOT ESTABLISHED at runtime.
- P02b-S470 INTERPRETATION (SQLite semantics) and FACT (executor order) — Each execution of the file that reaches L1610 rewrites `schema_version` to `'45'`, on the normal route and on every re-apply; the text puts no condition on the INSERT, and an `executescript` run stops at the first failing statement, so L1610 is reached only if every earlier statement succeeds. In the only non-test executor of `core/schema.sql`, `core/state_store.py` `StateStore._initialize_schema`, the file runs (`conn.executescript(schema_sql)`, L446) only after the newer-version guard (L398 to L405, raises `SchemaVersionMismatch`) and, when the stored version is older than `EXPECTED_SCHEMA_VERSION` (45, L102), only after the migration step (L420 to L440: refusal check L426 to L427, `_refuse_migration` raising at L355; `migrations.run_migrations` L429 to L435; `migrations.relocate_analytics_tables` L440); a refused or failed migration raises before L446. HISTORICAL: the comment at L415 to L419 says the trailing INSERT "must run AFTER a successful migration". Migration ordering and failure handling in detail are part P03's.
- P02b-S471 INTERPRETATION (SQLite semantics) — The three FOREIGN KEY clauses (L1237, L1290, L1333) are enforced only on connections that have `PRAGMA foreign_keys = ON`; the header (L17 to L18, part P02a's range) says application code must set it. Whether connections do so is part P01's.
- P02b-S472 FACT — Restart and retry routes: the DDL holds no runtime logic. The restart behaviour described in banners (gtt_state L1201 to L1203; retest_state L1306 to L1307; pb01_watchlist L1551 to L1553) lives in code; see parts P04 to P06 and the owner topics in the handoff section.

## Concerns for the AUDIT (neutral)

- P02b-S473 Enumerated values are listed in comments but not enforced by CHECK for most status-like columns in the range; only `gtt_state.status` (L1230), `retest_state.state` (L1326) and `pb01_watchlist.status` (L1570) have CHECKs. Columns with comment-listed values and no CHECK include `eod_verification.status` (L1010), `cron_heartbeat.status` (L1023), `order_execution_log.leg` and `side` (L1057, L1059), `trade_slippage_log.side` (L1089), `preflight_runs.phase` and `overall_status` (L1152, L1161), `preflight_check_results.criticality`, `status` and `fix_result` (L1172, L1173, L1177), `preflight_autofix_log.result` (L1191), `sr_detector_results.mode`, `resistance_confidence`, `support_confidence` and `structure_status` (L1263, L1273, L1274, L1281), `excursion_reconstruction_runs.mode` and `status` (L1363, L1370), the `control_tower_*` status and category columns (L1394, L1395, L1401, L1429, L1450, L1465, L1469), `config_snapshots.mode` and `trade_type` (L1496, L1497), the `eod_broker_reconciliation` mode and status columns (L1521, L1525 to L1530), `trade_slippage_log.trade_result` (L1112), `market_execution_context.leg` (L1128), `control_tower_findings.resource_type` (L1396), and the open-ended lists `order_execution_log.order_type` (L1058) and `trade_slippage_log.exit_reason` (L1113).
- P02b-S474 Identifier-like columns without a FOREIGN KEY: `order_execution_log.order_id`, `parent_trade_id`, `signal_id` (L1052 to L1054); `trade_slippage_log.trade_id` (L1085); `market_execution_context.trade_id`, `order_id` (L1125 to L1126); `preflight_check_results.run_id` (L1168) and `preflight_autofix_log.run_id` (L1185), which have no REFERENCES to `preflight_runs.run_id`; `preflight_runs.alert_id` (L1162); `config_snapshots.account_id` (L1495). In the same range, `gtt_state`, `sr_detector_results` and `retest_state` do declare FOREIGN KEYs.
- P02b-S475 Invariants stated in comments with no DDL counterpart: at most one ACTIVE `gtt_state` row per open trade (L1206 to L1208; indexes L1240 to L1244 are non-unique); `config_snapshots` "Idempotent by (snapshot_date, config_hash)" (L1481; no unique constraint on that pair); the `excursion_reconstruction_runs` bucket identity (L1355; no CHECK); "Append-only" for tables 31 to 36 (L1043, L1144; no trigger or other DDL guard in the range).
- P02b-S476 The UNIQUE dedupe index `idx_ct_findings_dedup` (L1410 to L1411) includes the nullable `resource_name` (L1397). INTERPRETATION (SQLite semantics): rows whose `resource_name` is NULL are treated as distinct by a UNIQUE index, so the index does not deduplicate them.
- P02b-S477 TEXT primary keys without NOT NULL: `preflight_runs.run_id` (L1150), `excursion_reconstruction_runs.run_id` (L1362), `control_tower_runs.run_id` (L1419), `control_tower_trends.date` (L1436), `control_tower_status.run_date` (L1449). INTERPRETATION (SQLite semantics): SQLite accepts NULL in a non-INTEGER primary-key column unless NOT NULL is declared. By contrast `eod_verification.date` (L1006) and `eod_broker_reconciliation.date` (L1520) declare NOT NULL.
- P02b-S478 `eod_broker_reconciliation.date` is the PRIMARY KEY (L1520) and also has its own non-unique index `idx_eod_broker_reconciliation_date` (L1536 to L1537). INTERPRETATION: the primary key already gives an automatic index on `date`.
- P02b-S479 Timestamp representation: three `created_at` columns are `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` (L1076, L1114, L1139). INTERPRETATION (SQLite semantics): `CURRENT_TIMESTAMP` yields UTC text in the form `YYYY-MM-DD HH:MM:SS`, while the file header's convention (L12, part P02a's range) and many inline comments in the range state ISO-8601 IST. `DATE` and `TIMESTAMP` declared types (L1086, L1076, L1114, L1139) get NUMERIC affinity in SQLite, unlike the TEXT used elsewhere for dates.
- P02b-S480 `market_execution_context` banner says "ALL nullable" (L1121) while `symbol` is NOT NULL (L1127).
- P02b-S481 `preflight_runs` banner says phases "A/B/C/FINAL" (L1148) while the `phase` comment lists "A or B or C" (L1152); no CHECK either way.
- P02b-S482 `cron_heartbeat` banner says it "Records successful cron job executions" and "Each cron job writes a row on success" (L1016), while the `status` comment lists SUCCESS, PARTIAL and FAILED (L1023).
- P02b-S483 Mode-value spelling differs between tables' comments: lower-case "'paper' or 'live'" for `sr_detector_results.mode` (L1263), upper-case "'PAPER' or 'LIVE'" for `config_snapshots.mode` (L1496) and "LIVE or PAPER" for `eod_broker_reconciliation.mode` (L1521); none has a CHECK.
- P02b-S484 Version bookkeeping in comments: ten banners refer to "the trailing INSERT" bumping the version, nine of them to their own block's number and one (L1146) with no number, while the single INSERT sets 45 (section 5); the end-of-file trailer is titled "END OF SCHEMA v24" and stops at v27 (L1613 to L1653); `fno_ban` is tagged "v21 / FIX-135 Item 44" (L988) while the trailer's v21 entry lists only `+shadow_trades (FIX-135 Item 41)` (L1638) and does not list `fno_ban`; the header names `state_store.py` for migrations (L20 to L21) while the range names `core/migrations.py`.
- P02b-S485 L1610 uses `INSERT OR REPLACE`, so the stored version becomes `'45'` on every execution that reaches L1610; the text puts no condition on it. Whether it can run before the v45 `trades` rebuild depends on the executor: in `core/state_store.py` `StateStore._initialize_schema` the file runs (L446) only after the migration step when the stored version is older (L420 to L440), and the comment at L415 to L419 (HISTORICAL) says a failed migration "raises and rolls back, leaving the version untouched". Ordering and failure handling are part P03's.
- P02b-S486 The v32 columns of `order_execution_log` (L1074 to L1075) were added inside a `CREATE TABLE IF NOT EXISTS`; on an existing database they depend on the rebuild listed under `MIGRATION_TABLES[32]` (`core/migrations.py` L126). The L1072 comment itself does not mention the rebuild.
- P02b-S487 `config_snapshots` stores `account_id` (L1495) and the "FULL resolved AppConfig" as JSON (L1499); the comment L1040 says the trading DB is backed up nightly. What fields the snapshot contains is A02's to record (field names only); backups are part P09a's.
- P02b-S488 `preflight_check_results` and `control_tower_freshness` have no primary key or unique constraint (L1167 to L1178, L1463 to L1470); whether duplicate rows per run and check, or per (`run_date`, `stage`), can arise is a question for the writing code (A20, A15).

## Questions about intent (OPEN QUESTION, for the project owner)

- P02b-S489 OPEN QUESTION — Was the "at most ONE ACTIVE row per open trade" rule for `gtt_state` (L1206 to L1208) meant to be enforced by the database (for example a partial unique index) or by code only?
- P02b-S490 OPEN QUESTION — Was the `config_snapshots` idempotence by (`snapshot_date`, `config_hash`) (L1481) meant to be a database constraint or a code check only?
- P02b-S491 OPEN QUESTION — Was the end-of-file version trailer (L1612 to L1654, "END OF SCHEMA v24", history to v27) meant to be kept up to date, and was the header "Version: 1" (L4) meant to track the schema version?
- P02b-S492 OPEN QUESTION — The table-number label 48 is absent between TABLE 47 (L1507) and TABLE 49 (L1540): was a table 48 planned, removed or moved elsewhere (for example to the analytics database)?
- P02b-S493 OPEN QUESTION — Which schema version introduced `fno_ban`: the v21 in its banner (L988) or another version (the trailer does not list it)?
- P02b-S494 OPEN QUESTION — Were the comment-listed status values (Concerns, first item) intended to be enforced by CHECK constraints, as they are for three tables in the range and for the O2 tables named in the trailer (L1642 to L1645)?

## UNKNOWN / NOT ESTABLISHED

- P02b-S495 UNKNOWN / NOT ESTABLISHED — Whether any of the 22 tables existed in any production database, at which schema version, with which definition, and whether rows were written: no database, log or backup survives.
- P02b-S496 UNKNOWN / NOT ESTABLISHED — Whether the statement at L1610 was ever executed against the production database, and what `schema_version` value the production database last held.
- P02b-S497 UNKNOWN / NOT ESTABLISHED — Whether the `MIGRATION_TABLES[32]` rebuild of `order_execution_log` or the v45 rebuild of `trades` ran on any production database.
- P02b-S498 UNKNOWN / NOT ESTABLISHED — Whether `PRAGMA foreign_keys = ON` was in effect on the connections that wrote to `gtt_state`, `sr_detector_results` and `retest_state` (part P01 records what the code sets; runtime remains unknown).
- P02b-S499 UNKNOWN / NOT ESTABLISHED — Whether the schedules mentioned in comments (08:30 for `fno_ban`, L989; 17:00 and Sunday 18:00 for the Control Tower, L1417; 15:58 for `eod_broker_reconciliation`, L1510; about 08:30 for `daily_symbol_stats`, L1583) were installed or ran; schedule declarations are A16's.
- P02b-S500 UNKNOWN / NOT ESTABLISHED — Whether the default-OFF and shadow states stated in comments (PB-01 "enabled:false", L1545; `daily_symbol_stats` wiring flag, L1589) held in production; activation is A18's and A02's.

## Boundary handoffs (owner topic: what crosses)

- P02b-S501 Part P02a (A03): the `trades` and `signals` tables targeted by the FOREIGN KEYs at L1237, L1290 and L1333; the `schema_meta` table (L29 to L32) written by L1610; the header conventions (L1 to L22); the trigger at L291.
- P02b-S502 Part P03 (A03): `MIGRATION_TABLES` (`core/migrations.py` L115; keys 32, 38 and 45 relevant to this range), the reading of `schema_version`, and the order of schema execution versus migration.
- P02b-S503 Part P01 (A03): how `core/schema.sql` is executed, transactions, `PRAGMA foreign_keys`, and the ATTACH of `analytics` (L1038).
- P02b-S504 Part P07 (A03): `system_metrics` and `system_metrics_daily`, relocated to the analytics database (L1035 to L1040; `core/analytics_schema.sql`).
- P02b-S505 Part P09a (A03): the "nightly .backup" of the trading database mentioned at L1040.
- P02b-S506 Parts P04 to P06 (A03): every reader and writer of the 22 tables (store methods, raw SQL, scripts).
- P02b-S507 A05: `fno_ban` acquisition (the index assigns `scripts/fetch_fno_ban.py`, F&O ban-list acquisition, to A05); `daily_symbol_stats` inputs from daily candles via "OhlcFetcher" (L1584 to L1585).
- P02b-S508 A07: the comment at L1585 to L1587 (HISTORICAL) says the screener's `_build_market_data` reads `daily_symbol_stats`, behind a default-OFF flag (L1589). FACT: at the baseline, `screening/secondary_screener.py` `_build_market_data` (L380 to L418) does not read it (L413 to L417 set `atr`, `rsi`, `prev_close` and `avg_volume_20d` to None), and `core/daily_stats.py` L14 (HISTORICAL) says "NONE consumes this on the live path yet". Readers and writers: parts P04 to P06.
- P02b-S509 A12: `eod_verification` (by name; `scripts/eod_verify.py` is A12's per the index) and `eod_broker_reconciliation` (`scripts/eod_broker_reconcile.py`, named at L1510).
- P02b-S510 A16: `cron_heartbeat` and its reader `scripts/check_cron_drift.py` (named at L1017); every schedule time quoted in comments.
- P02b-S511 A11: `order_execution_log`, `trade_slippage_log` and `market_execution_context` (execution and slippage recording; the index assigns `orders/slippage_recorder.py` to A11; the banner L1045 to L1046 mentions "async event subscribers"); `gtt_state` (`orders/cnc_gtt.py`, named at L1200).
- P02b-S512 A20: `preflight_runs`, `preflight_check_results` and `preflight_autofix_log` (pre-flight subsystem, `scripts/preflight/`).
- P02b-S513 A08 (with A18 for shadow activation): `sr_detector_results` (S&R detector; `scripts/sr_detector_backfill.py` named at L1251) and `retest_state` ("RetestMonitor", L1306; `screening/retest_monitor.py` is A08's per the index).
- P02b-S514 A15: `excursion_reconstruction_runs` (`scripts/reconstruct_excursions.py`, named at L1344) and the five `control_tower_*` tables (`ops/control_tower/`, named at L1379).
- P02b-S515 A02: `config_snapshots` (`core/config_snapshotter.snapshot_config`, named at L1476) and the content of `config_json`.
- P02b-S516 A18: `pb01_watchlist` (PB-01 shadow playbook, V3; `v3_chain/` is A18's per the index) and the default-OFF wiring flag for `daily_symbol_stats` (L1589).
