# A03 evidence: The trading schema, first half: `core/schema.sql` L1 to L990

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P02a, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** The catalogue of `core/schema.sql` L1 to L990: header rules, 23 tables, their columns, constraints, indexes and the trigger. Statement IDs `P02a-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

| ID | Statement |
|---|---|
| P02a-S001 | FACT: before the work, `git rev-parse HEAD` on the local read-only legacy clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline) and `git status --short` returned nothing. |
| P02a-S002 | FACT: after the work, the same two commands returned the baseline commit and an empty status (re-run at the end; see the last row of this table). |
| P02a-S003 | Scope read: `core/schema.sql` L1 to L998 in full. L1 to L990 is this part's range; L991 to L998 (start of `fno_ban`) was read only to fix the range boundary and is part P02b's. |
| P02a-S004 | Context read (owner topics only): `doc/01_PRE_PHASE/04_MASTER_SYSTEM_INVESTIGATION_INDEX/MASTER_SYSTEM_INVESTIGATION_INDEX_2026-11-04.md` section 3 (L51 to L232) and Appendix A (L278 to L373). |
| P02a-S005 | Tools: file reading; `grep` and `awk` over the SQL text; `git log -1 -- core/schema.sql`; `git ls-tree -r --name-only HEAD` (presence of four files the comments cite; their contents were not read). Two scratch scripts in the work area's tools folder (`p02a_parse.py`, `p02a_gen.py`) split each CREATE TABLE body on top-level commas with regular expressions, after removing `--` comments, to list and count columns. The SQL was never executed, loaded or imported. Column lists and counts below rely on that text parsing and were checked against a manual reading. |
| P02a-S006 | FACT: the last commit touching `core/schema.sql` at the baseline is `e39655aaa796d7ebdca9e34859d4cf07127634fa`, dated 2026-08-23 14:47:43 +0530 (`git log -1`). |
| P02a-S007 | Conventions in this file: "Line" is the line where a column definition starts; "nullable" means no NOT NULL is declared; "comment" quotes are HISTORICAL (what someone wrote), never proof of behaviour. Callers are not traced here (parts P04, P05, P06a, P06b). |
| P02a-S008 | FACT (closing check): after the work, `rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty. |

### 0.1 Baseline checks of the later passes

| ID | Statement |
|---|---|
| P02a-S536 | FACT (checker, as stated in its file): before its work `git rev-parse HEAD` on the local read-only legacy clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing; after its work (2026-11-09 14:07 IST) the same commit and an empty status. The checker's text-parsing scripts were kept in the work area's tools folder and run with `python3 -I`; it states that the SQL was never executed, loaded or imported, and that the content of the legacy `AGENTS.md`, displayed by the environment during its check, was treated as data and used for nothing. |
| P02a-S537 | FACT (corrector, before the work, 2026-11-09 15:46 IST): `git rev-parse HEAD` on the local read-only legacy clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing. The corrector re-read `core/schema.sql` L1 to L30, L36 to L72, L105 to L110, L160 to L168, L196 to L200, L234 to L300, L320 to L324, L386 to L408, L430 to L438, L471 to L500, L519 to L525, L574 to L586, L603 to L618, L640 to L660, L673 to L678 and L732 to L760 as text; ran `git show bcf03b5:core/schema.sql` (L244 to L251), `git rev-list --max-parents=0 HEAD`, `git grep` for the two `idx_ledger_*` names (tests excluded) and a `grep` for statement keywords; and read the project index L276 to L278, L337, L353 and L372 to L375. No file was written outside the two output files; no legacy code or SQL was run. |
| P02a-S538 | FACT (corrector, after the work): after both output files were written (2026-11-09 15:47 IST), `git rev-parse HEAD` on the local read-only legacy clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` returned nothing. |

## 1. Header comments, version rule and migration instructions (HISTORICAL unless marked FACT)

| ID | Lines | Statement |
|---|---|---|
| P02a-S009 | L2 | HISTORICAL: title "Trading System v2 — State Store Schema". |
| P02a-S010 | L4 to L5 | HISTORICAL: "Version: 1" and "Last updated: 2026-04-14". |
| P02a-S011 | L7 to L9 | HISTORICAL: the file "defines all tables for the v2 trading system's persistent state" and "is the SOURCE OF TRUTH for the schema. Migrations to new versions add new sections at the bottom and bump the schema_version row." |
| P02a-S012 | L11 to L16 | HISTORICAL: conventions: all TEXT timestamps are ISO-8601 IST (example with `+05:30`); all IDs are UUID4 strings unless noted (broker order IDs are broker-assigned); all monetary amounts are REAL (Python float), with float rounding "within 1 paise" tolerated. |
| P02a-S013 | L17 to L18 | HISTORICAL: "All FK relationships are explicit even though SQLite does not enforce them by default — application code MUST set PRAGMA foreign_keys = ON". Whether connections do so: see part P01. |
| P02a-S014 | L20 to L21 | HISTORICAL: "DO NOT modify this file by hand without bumping schema_version and adding a corresponding migration in state_store.py." Migration mechanics: see part P03. |
| P02a-S015 | L25 to L27 | HISTORICAL: `schema_meta` is the "Single source of truth for schema version and migration tracking. Always exists. Single row per key." |
| P02a-S016 | L604 to L610 | HISTORICAL: an "INITIALIZATION" block says "Schema version marker. Application code reads this on startup and runs migrations if it differs from the code's expected version. OR REPLACE so that re-running this script on an existing DB bumps the version." |
| P02a-S017 | L604 to L618 | FACT: no version-marker statement (no INSERT into `schema_meta`) follows the INITIALIZATION comment inside this range; the next statement is `CREATE TABLE IF NOT EXISTS eod_squareoff_log` at L618 (with its own TABLE 12 comment at L611 to L617). |
| P02a-S018 | L1610 (outside range) | FACT (pointer only): the file's only `schema_meta` write is `INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '45')` at L1610, found by `grep`; it belongs to part P02b. |
| P02a-S019 | L858 to L860 | FACT: a comment header "SCHEMA VERSION BUMP: v16 -> v17" is followed by no statement other than the TABLE 21 comments and `CREATE TABLE IF NOT EXISTS telegram_alerts` at L866. |
| P02a-S020 | L287 to L290 | HISTORICAL: the trigger comment says RAISE(ABORT) "surfaces in Python as sqlite3.IntegrityError and rolls back only the offending statement", and that "CREATE TRIGGER IF NOT EXISTS is re-applied idempotently by executescript on every boot (after any migration rebuild), so it needs NO schema_version bump (stays v41)". How the file is applied at boot: see part P03. |
| P02a-S021 | L430 to L434 | HISTORICAL: "TABLE 6: (removed v10)": the legacy `capital_ledger` table "was never written to"; "No CREATE statement here on purpose. Drop handled below for upgrade path." |
| P02a-S022 | L804 to L808 | HISTORICAL: "TABLE 18: candles -- RELOCATED (O6, v28) to analytics.db": the table lives in `analytics.db` (`core/analytics_schema.sql`, `core/db_connect.py`), "ATTACHed as schema `analytics` on every connection", and was "Kept out of the trading DB so the nightly .backup stays small and fast." FACT: there is no CREATE TABLE for `candles` in this range. See parts P07 (analytics), P01 (ATTACH) and P09a (backup). |
| P02a-S023 | whole range | FACT (`grep`): schema-version tags in comments in this range are v10, v11, v14, v15, v16, v17, v20, v21, v25, v26, v27, v28, v29, v30, v32, v34, v35, v41 and v45; the highest is v45 (L241, L247). `v2` (L2, L7) is part of the system's name ("Trading System v2") and `v2.1` (L165) labels the SCALE entry mode; neither is a schema-version tag. The header still reads "Version: 1" (L4). |
| P02a-S024 | whole range | FACT: the comments number the tables "TABLE 1" to "TABLE 25" in this range; TABLE 6 is removed (L430) and TABLE 18 relocated (L804), so the range holds 23 CREATE TABLE statements. "TABLE 26: fno_ban" begins at L987 to L990 (comment only in this range; its CREATE TABLE is at L991, part P02b). |
| P02a-S025 | L115, L244, L245, L408 | FACT (`git ls-tree`): files cited by comments exist at the baseline: `docs/audit/db_schema_review_15jun2026.md` (L115), `core/closure_source.py` (L244), `docs/closure_source_contract.md` (L245), `docs/audit/capital_snapshot_redirect_25jul2026.md` (L408). Their contents were not read in this part. |

## 2. Tables

### 2.0 Common facts for all 23 tables

| ID | Statement |
|---|---|
| P02a-S026 | FACT: all 23 CREATE TABLE statements in the range use `IF NOT EXISTS`. |
| P02a-S027 | FACT: no table in the range is declared `WITHOUT ROWID` or `STRICT`. |
| P02a-S028 | FACT: the declared column types in the range are only TEXT, INTEGER and REAL. |
| P02a-S029 | FACT: no FOREIGN KEY clause in the range has an ON DELETE, ON UPDATE or DEFERRABLE clause; all 13 FOREIGN KEY clauses are table-level clauses (none is written inline on a column). No COLLATE clause appears. |
| P02a-S030 | FACT: 12 tables use `INTEGER PRIMARY KEY AUTOINCREMENT` (system_events, fm_ledger, webhook_audit, eod_squareoff_log, reconciliation_log, screener_results, innings, pnl_reconciliation, telegram_alerts, trade_journal, position_reconciliation, strategy_metrics). INTERPRETATION: in SQLite, AUTOINCREMENT makes the engine keep an internal `sqlite_sequence` table. |
| P02a-S031 | FACT: 3 tables are single-row by `id INTEGER PRIMARY KEY CHECK (id = 1)`: capital_snapshot (L411), session (L479), kill_switch_state (L566). |
| P02a-S032 | FACT: 8 tables have a TEXT PRIMARY KEY with no explicit NOT NULL: schema_meta.key (L30), signals.signal_id (L43), trades.trade_id (L118), orders.order_id (L316), smart_tgt_state.trade_id (L714), gate_state.signal_id (L781), trade_excursions.trade_id (L825), shadow_trades.shadow_trade_id (L958). INTERPRETATION: in an ordinary (rowid) SQLite table a non-INTEGER PRIMARY KEY column accepts NULL unless NOT NULL is declared. |
| P02a-S033 | FACT: 2 columns are generated: fm_ledger.date (L541) and webhook_audit.date (L592), both `GENERATED ALWAYS AS (substr(ts, 1, 10)) STORED`. INTERPRETATION: generated columns need SQLite 3.31.0 or later; the runtime SQLite version is UNKNOWN / NOT ESTABLISHED. |

### 2.1 schema_meta (L29 to L32)

| ID | Statement |
|---|---|
| P02a-S034 | FACT: `CREATE TABLE IF NOT EXISTS schema_meta`, L29 to L32; no table-level constraints. Comment (HISTORICAL, L25 to L27): schema version and migration tracking, "Single row per key". |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S035 | L30 | `key` | TEXT | PRIMARY KEY (no explicit NOT NULL) |
| P02a-S036 | L31 | `value` | TEXT | NOT NULL |

### 2.2 signals (L42 to L79)

| ID | Statement |
|---|---|
| P02a-S037 | FACT: `CREATE TABLE IF NOT EXISTS signals`, L42 to L79. Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L78 (a forward reference: `trades` is created later, at L117). Comment (HISTORICAL, L36 to L40): "Immutable log of EVERY incoming webhook signal. One row per (symbol, scanner) pair extracted from a webhook. Status field tells you what happened to it." |
| P02a-S038 | FACT: the `status` CHECK (L60 to L70) admits 20 listed values ('QUEUED', 'ACCEPTED', 'PROCESSING', 'PROCESSED', 'PROCESSED_NO_PLACER', 'PLACEMENT_FAILED', 'RESERVED', 'QUEUE_FULL', 'PASSED', 'TRADED', 'DUPLICATE', 'EXPIRED', 'INVALID_SYMBOL', 'INVALID_PRICE', 'OUTSIDE_HOURS', 'IN_PROCESS', 'CANCELLED', 'FAILED', 'PENDING', 'TIMEOUT') or any value matching one of 5 GLOB patterns: 'REJECTED*', 'DROPPED_*', 'SKIPPED_*', 'GATE_*', 'RETEST_*'. |
| P02a-S039 | HISTORICAL (L51 to L59): the status set is "an OPEN set written by many modules (webhook_receiver, signal_processor, secondary_screener, entry_gate)"; the CHECK is "a shape/typo guard ... NOT a closed enum — by design, because a wrongly-rejected signal write would crash the pipeline"; "Verified complete against the full test suite" (tests are out of scope, topic A19). |
| P02a-S528 | HISTORICAL: the comment at L53 to L54 says "Four open prefix families are allowed via GLOB"; the inline value list at L50 names REJECTED*, GATE_*, DROPPED_* and SKIPPED_* only; the fifth pattern `RETEST_*` (L70) carries its own inline comment "SNR-V2: WAIT_FOR_RETEST parking states". FACT: the CHECK at L60 to L70 has five GLOB patterns. |
| P02a-S040 | INTERPRETATION: SQLite GLOB is case-sensitive and `*` matches any sequence including an empty one, so 'REJECTED*' admits 'REJECTED' itself and 'DROPPED_*' admits 'DROPPED_' with nothing after it. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S041 | L43 | `signal_id` | TEXT | PRIMARY KEY (no explicit NOT NULL) |
| P02a-S042 | L44 | `symbol` | TEXT | NOT NULL |
| P02a-S043 | L45 | `scanner` | TEXT | NOT NULL |
| P02a-S044 | L46 | `strategy` | TEXT | NOT NULL |
| P02a-S045 | L47 | `triggered_at` | TEXT | NOT NULL |
| P02a-S046 | L48 | `received_at` | TEXT | NOT NULL |
| P02a-S047 | L49 | `expires_at` | TEXT | NOT NULL |
| P02a-S048 | L50 | `status` | TEXT | NOT NULL; CHECK (20 listed values or 5 GLOB patterns, L60 to L70) |
| P02a-S049 | L71 | `rejection_reason` | TEXT | nullable |
| P02a-S050 | L72 | `trade_id` | TEXT | nullable; FK -> trades(trade_id) (clause at L78) |
| P02a-S051 | L73 | `trigger_price` | REAL | nullable |
| P02a-S052 | L74 | `fingerprint` | TEXT | NOT NULL |
| P02a-S053 | L75 | `fingerprint_date` | TEXT | NOT NULL |
| P02a-S054 | L76 | `webhook_payload` | TEXT | nullable (comment L76: "raw JSON from Chartink for forensics") |

### 2.3 trades (L117 to L255)

| ID | Statement |
|---|---|
| P02a-S055 | FACT: `CREATE TABLE IF NOT EXISTS trades`, L117 to L255, 59 columns. Table-level constraint: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L254. Comment (HISTORICAL, L97 to L99): "One row per logical position lifecycle. Created at capital reservation. A trade may have many orders". |
| P02a-S056 | HISTORICAL (L104 to L115, "O9"): `signals.trade_id` and `trades.signal_id` form a "SOFT CIRCULAR REFERENCE (intentional design, no fix needed)"; `trades.signal_id` is set at creation, `signals.trade_id` is set post-fill; "FK enforcement on BOTH directions is safe here because each side is populated at a different lifecycle moment". |
| P02a-S057 | FACT: the `status` CHECK (L158 to L161) admits 10 listed values ('PENDING', 'PENDING_FILL', 'OPEN', 'PARTIAL', 'EXITING', 'CLOSED', 'CLOSED_MANUAL', 'CANCELLED', 'FAILED', 'UNKNOWN_IN_FLIGHT') or any value matching GLOB 'REJECTED*'. Comment L152 lists "PENDING_FILL/OPEN/PARTIAL/EXITING/CLOSED/CANCELLED/FAILED/REJECTED*"; L155 to L157 (HISTORICAL) say EXITING was added by "FIX-179 (v29)" as a transitional state set by the kill switch hard kill. |
| P02a-S058 | HISTORICAL (L171): `reservation_id` is described as "FK to fm_ledger.reservation_id (not enforced)"; FACT: no FOREIGN KEY clause names it. |
| P02a-S059 | HISTORICAL (L241 to L248): the permitted values of `closure_source` and `exit_mechanism` "live in ONE place -- core/closure_source.py ... and are deliberately NOT restated here"; NULL means "we do not know". FACT: neither column has a CHECK. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S060 | L118 | `trade_id` | TEXT | PRIMARY KEY (no explicit NOT NULL) |
| P02a-S061 | L119 | `signal_id` | TEXT | NOT NULL; FK -> signals(signal_id) (clause at L254) |
| P02a-S062 | L122 | `symbol` | TEXT | NOT NULL |
| P02a-S063 | L123 | `direction` | TEXT | NOT NULL |
| P02a-S064 | L124 | `strategy` | TEXT | NOT NULL |
| P02a-S065 | L125 | `sector` | TEXT | nullable |
| P02a-S066 | L128 | `qty_planned` | INTEGER | NOT NULL |
| P02a-S067 | L129 | `qty_filled` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S068 | L130 | `entry_target_price` | REAL | NOT NULL |
| P02a-S069 | L131 | `entry_actual_price` | REAL | nullable |
| P02a-S070 | L132 | `sl_initial` | REAL | NOT NULL |
| P02a-S071 | L133 | `tgt_initial` | REAL | NOT NULL |
| P02a-S072 | L136 | `margin_reserved` | REAL | NOT NULL |
| P02a-S073 | L137 | `risk_amount` | REAL | NOT NULL |
| P02a-S074 | L140 | `created_at` | TEXT | NOT NULL |
| P02a-S075 | L141 | `entry_time` | TEXT | nullable |
| P02a-S076 | L142 | `exit_time` | TEXT | nullable |
| P02a-S077 | L145 | `exit_price` | REAL | nullable |
| P02a-S078 | L146 | `exit_reason` | TEXT | nullable |
| P02a-S079 | L147 | `gross_pnl` | REAL | nullable |
| P02a-S080 | L148 | `charges` | REAL | nullable |
| P02a-S081 | L149 | `net_pnl` | REAL | nullable |
| P02a-S082 | L152 | `status` | TEXT | NOT NULL; CHECK (10 listed values or GLOB 'REJECTED*', L158 to L161) |
| P02a-S083 | L164 | `recovered_flag` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S084 | L165 | `entry_mode` | TEXT | NOT NULL; DEFAULT 'FULL' |
| P02a-S085 | L166 | `order_protocol` | TEXT | NOT NULL |
| P02a-S086 | L171 | `reservation_id` | TEXT | nullable (no FK clause) |
| P02a-S087 | L174 | `cost_brokerage` | REAL | nullable |
| P02a-S088 | L175 | `cost_stt` | REAL | nullable |
| P02a-S089 | L176 | `cost_exchange_txn` | REAL | nullable |
| P02a-S090 | L177 | `cost_sebi` | REAL | nullable |
| P02a-S091 | L178 | `cost_gst` | REAL | nullable |
| P02a-S092 | L179 | `cost_stamp_duty` | REAL | nullable |
| P02a-S093 | L182 | `mode` | TEXT | nullable |
| P02a-S094 | L183 | `sl_trail_count` | INTEGER | DEFAULT 0; nullable |
| P02a-S095 | L189 | `signal_to_order_ms` | INTEGER | nullable |
| P02a-S096 | L190 | `order_to_fill_ms` | INTEGER | nullable |
| P02a-S097 | L191 | `total_latency_ms` | INTEGER | nullable |
| P02a-S098 | L198 | `needs_tgt_retry` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S099 | L199 | `tgt_retry_count` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S100 | L200 | `tgt_last_retry_at` | TEXT | nullable |
| P02a-S101 | L207 | `tolerance_fraction_used` | REAL | nullable |
| P02a-S102 | L208 | `tolerance_source` | TEXT | nullable |
| P02a-S103 | L214 | `tier_multiplier_mode` | TEXT | nullable |
| P02a-S104 | L215 | `tier_weight_applied` | REAL | nullable |
| P02a-S105 | L216 | `perf_weight_applied` | REAL | nullable |
| P02a-S106 | L217 | `flat_value_rs_used` | REAL | nullable |
| P02a-S107 | L218 | `qty_by_risk` | INTEGER | nullable |
| P02a-S108 | L219 | `qty_by_capital` | INTEGER | nullable |
| P02a-S109 | L220 | `qty_by_concentration` | INTEGER | nullable |
| P02a-S110 | L221 | `qty_by_flat` | INTEGER | nullable |
| P02a-S111 | L222 | `binding_constraint` | TEXT | nullable |
| P02a-S112 | L225 | `actual_position_value_rs` | REAL | nullable |
| P02a-S113 | L232 | `tgt_risk_reward_applied` | REAL | nullable |
| P02a-S114 | L238 | `exits_verified` | INTEGER | nullable |
| P02a-S115 | L239 | `exits_verify_detail` | TEXT | nullable |
| P02a-S116 | L249 | `closure_source` | TEXT | nullable |
| P02a-S117 | L250 | `exit_mechanism` | TEXT | nullable |
| P02a-S118 | L252 | `updated_at` | TEXT | NOT NULL |

### 2.4 orders (L315 to L368)

| ID | Statement |
|---|---|
| P02a-S119 | FACT: `CREATE TABLE IF NOT EXISTS orders`, L315 to L368. Table-level constraints: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L366 and `FOREIGN KEY (superseded_by) REFERENCES orders(order_id)` at L367 (self-reference). Comment (HISTORICAL, L304 to L311): "One row per broker order"; on a trail SL update the old SL row "stays (status=CANCELLED) but its superseded_by points to the new SL's order_id". |
| P02a-S120 | FACT: the `status` CHECK (L343 to L346) admits exactly 11 values: 'PENDING', 'SUBMITTED', 'OPEN', 'PARTIAL', 'COMPLETE', 'CANCELLED', 'FAILED', 'EXPIRED', 'UNKNOWN_IN_FLIGHT', 'TRIGGER_PENDING', 'TRIGGER PENDING' (with a space). No GLOB pattern. |
| P02a-S121 | HISTORICAL (L335 to L342): the write vocabulary is `OrderStateMachine.STATES` (`broker/order_state_machine.py`); "Kite 'REJECTED' maps to FAILED in order_monitor and no raw broker strings reach this column"; both TRIGGER_PENDING spellings are permitted because "wrongly rejecting an SL status write would mean a naked position". |
| P02a-S122 | FACT: the `leg` CHECK (L322) admits 'ENTRY', 'SL', 'TGT', 'EOD', 'CO', 'CANCEL'. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S123 | L316 | `order_id` | TEXT | PRIMARY KEY (no explicit NOT NULL) |
| P02a-S124 | L317 | `trade_id` | TEXT | NOT NULL; FK -> trades(trade_id) (clause at L366) |
| P02a-S125 | L320 | `leg` | TEXT | NOT NULL; CHECK (leg IN ('ENTRY','SL','TGT','EOD','CO','CANCEL')) |
| P02a-S126 | L323 | `leg_index` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S127 | L326 | `transaction_type` | TEXT | NOT NULL |
| P02a-S128 | L327 | `order_type` | TEXT | NOT NULL |
| P02a-S129 | L328 | `product` | TEXT | NOT NULL |
| P02a-S130 | L329 | `variety` | TEXT | NOT NULL |
| P02a-S131 | L330 | `qty_requested` | INTEGER | NOT NULL |
| P02a-S132 | L331 | `price` | REAL | nullable |
| P02a-S133 | L332 | `trigger_price` | REAL | nullable |
| P02a-S134 | L335 | `status` | TEXT | NOT NULL; CHECK (11 listed values, L343 to L346) |
| P02a-S135 | L347 | `qty_filled` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S136 | L348 | `avg_fill_price` | REAL | nullable |
| P02a-S137 | L351 | `placed_at` | TEXT | NOT NULL |
| P02a-S138 | L352 | `filled_at` | TEXT | nullable |
| P02a-S139 | L353 | `updated_at` | TEXT | NOT NULL |
| P02a-S140 | L356 | `rejection_reason` | TEXT | nullable |
| P02a-S141 | L361 | `reconciliation_status` | TEXT | nullable |
| P02a-S142 | L364 | `superseded_by` | TEXT | nullable; FK -> orders(order_id) (clause at L367) |

### 2.5 capital_snapshot (L410 to L427)

| ID | Statement |
|---|---|
| P02a-S143 | FACT: `CREATE TABLE IF NOT EXISTS capital_snapshot`, L410 to L427; single-row by `CHECK (id = 1)`; no table-level constraints. Comment (HISTORICAL, L386 to L387): "Current capital state. Single-row table ... the 'fast read' of capital." |
| P02a-S144 | HISTORICAL (L391 to L408): "UNUSED SINCE 2026-07-25 — READS REDIRECTED, TABLE DELIBERATELY KEPT. Nothing writes this table and it holds 0 rows in production." It names three former readers (`scripts/preflight/checks/engine.py`, `scripts/healthcheck_server.py`, `ops_dashboard/backend/readers/db_reader.py`), states where each value is now sourced (cash_floor from opening capital less margin on open positions, L400; realized_pnl_today from fm_ledger, L401; margin_used and margin_reserved from trades, L402 to L403), and says it was "NOT DROPPED: a schema change was not authorised". The production row count is UNKNOWN / NOT ESTABLISHED (no database survives). |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S145 | L411 | `id` | INTEGER | PRIMARY KEY; CHECK (id = 1) |
| P02a-S146 | L414 | `cash_floor` | REAL | NOT NULL |
| P02a-S147 | L415 | `realized_pnl_today` | REAL | NOT NULL; DEFAULT 0 |
| P02a-S148 | L416 | `margin_used` | REAL | NOT NULL; DEFAULT 0 |
| P02a-S149 | L417 | `margin_reserved` | REAL | NOT NULL; DEFAULT 0 |
| P02a-S150 | L420 | `charges_today` | REAL | NOT NULL; DEFAULT 0 |
| P02a-S151 | L423 | `last_broker_sync` | TEXT | nullable |
| P02a-S152 | L424 | `sync_source` | TEXT | nullable |
| P02a-S153 | L426 | `updated_at` | TEXT | NOT NULL |

### 2.6 system_events (L455 to L461)

| ID | Statement |
|---|---|
| P02a-S154 | FACT: `CREATE TABLE IF NOT EXISTS system_events`, L455 to L461; no table-level constraints. Comment (HISTORICAL, L442 to L451): "Lifecycle marker log. Used by G5a startup detection to determine COLD vs WARM vs CRASH vs HALT scenarios"; event types named: STARTUP, SHUTDOWN, CRASH_DETECTED, KILL_SWITCH, RECOVERY, CONFIG_DIFF. FACT: no CHECK on `event_type` or `scenario`. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S155 | L456 | `event_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S156 | L457 | `timestamp` | TEXT | NOT NULL |
| P02a-S157 | L458 | `event_type` | TEXT | NOT NULL |
| P02a-S158 | L459 | `scenario` | TEXT | nullable |
| P02a-S159 | L460 | `details` | TEXT | nullable (comment L460: "JSON blob") |

### 2.7 session (L478 to L501)

| ID | Statement |
|---|---|
| P02a-S160 | FACT: `CREATE TABLE IF NOT EXISTS session`, L478 to L501; single-row by `CHECK (id = 1)`; no table-level constraints. Comment (HISTORICAL, L471 to L473): "Single-row table holding current session metadata + kill switch state + daily counters. Lives in the same DB transaction context as everything else, so kill_switch state changes are atomic with capital changes." |
| P02a-S161 | HISTORICAL (L488 to L493): "2026-04-26 audit CFG-7" dropped session.kill_state, kill_reason, kill_time and kill_type (the `kill_switch_state` table is "the single source of truth (KS3)"); "Audit NSK-1" (no date given) dropped yesterday_pnl, yesterday_wins, yesterday_losses and consecutive_losses ("the values were never written"; risk_engine "recomputes consecutive_losses from recent_trade_pnls() each cycle"). FACT: the DDL at L478 to L501 has no kill-switch column and no daily-counter column. |
| P02a-S162 | FACT: `account_id` (L483) is TEXT NOT NULL. INTERPRETATION (from the column name only): it holds an account identifier (values not examined: security restriction). |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S163 | L479 | `id` | INTEGER | PRIMARY KEY; CHECK (id = 1) |
| P02a-S164 | L482 | `session_date` | TEXT | NOT NULL |
| P02a-S165 | L483 | `account_id` | TEXT | NOT NULL |
| P02a-S166 | L484 | `broker` | TEXT | NOT NULL |
| P02a-S167 | L485 | `mode` | TEXT | NOT NULL |
| P02a-S168 | L486 | `trade_type` | TEXT | NOT NULL |
| P02a-S169 | L496 | `last_config_hash` | TEXT | nullable |
| P02a-S170 | L499 | `session_start` | TEXT | NOT NULL |
| P02a-S171 | L500 | `last_updated` | TEXT | NOT NULL |

### 2.8 fm_ledger (L518 to L542)

| ID | Statement |
|---|---|
| P02a-S172 | FACT: `CREATE TABLE IF NOT EXISTS fm_ledger`, L518 to L542; no table-level constraints; no FOREIGN KEY clause (its `signal_id`, `reservation_id` and `trade_id` columns reference nothing in the DDL). Comment (HISTORICAL, L505 to L515): "Append-only write-ahead log for FundManager capital mutations (FM10). One row per atomic capital operation. NEVER UPDATE OR DELETE a row"; "The row is written BEFORE the in-memory state mutation"; after a crash, rehydrate "replays fm_ledger rows to rebuild in-memory state"; "entry_type is a closed enum (CHECK)". |
| P02a-S173 | FACT: the `entry_type` CHECK (L522 to L524) admits exactly 'INIT', 'RESERVE', 'RELEASE', 'COMMIT', 'RELEASE_USED', 'SYNC', 'RESET_PNL', 'TOP_UP'. FACT: no trigger or constraint in this range prevents UPDATE or DELETE on fm_ledger. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S174 | L519 | `ledger_id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S175 | L520 | `ts` | TEXT | NOT NULL |
| P02a-S176 | L521 | `entry_type` | TEXT | NOT NULL; CHECK (entry_type IN ('INIT','RESERVE','RELEASE','COMMIT','RELEASE_USED','SYNC','RESET_PNL','TOP_UP')) |
| P02a-S177 | L525 | `amount` | REAL | NOT NULL |
| P02a-S178 | L526 | `bucket` | TEXT | NOT NULL |
| P02a-S179 | L527 | `balance_before` | REAL | NOT NULL |
| P02a-S180 | L528 | `balance_after` | REAL | NOT NULL |
| P02a-S181 | L529 | `signal_id` | TEXT | nullable (no FK clause) |
| P02a-S182 | L530 | `reservation_id` | TEXT | nullable |
| P02a-S183 | L531 | `reason` | TEXT | nullable |
| P02a-S184 | L533 | `session_id` | TEXT | nullable |
| P02a-S185 | L534 | `direction` | TEXT | nullable |
| P02a-S186 | L535 | `trade_id` | TEXT | nullable (no FK clause) |
| P02a-S187 | L536 | `margin_delta` | REAL | NOT NULL; DEFAULT 0.0 |
| P02a-S188 | L537 | `pnl_delta` | REAL | NOT NULL; DEFAULT 0.0 |
| P02a-S189 | L538 | `costs` | REAL | NOT NULL; DEFAULT 0.0 |
| P02a-S190 | L541 | `date` | TEXT | GENERATED ALWAYS AS (substr(ts, 1, 10)) STORED |

### 2.9 kill_switch_state (L565 to L572)

| ID | Statement |
|---|---|
| P02a-S191 | FACT: `CREATE TABLE IF NOT EXISTS kill_switch_state`, L565 to L572; single-row by `CHECK (id = 1)`; no table-level constraints. Comment (HISTORICAL, L558 to L561): "Single-row table holding the persistent kill switch state. Used by KillSwitch.__init__ to recover state on restart"; without it "the system would overwrite operator manual halts on restart". |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S192 | L566 | `id` | INTEGER | PRIMARY KEY; CHECK (id = 1) |
| P02a-S193 | L567 | `state` | TEXT | NOT NULL; CHECK (state IN ('INACTIVE','SOFT_KILL','HARD_KILL')) |
| P02a-S194 | L569 | `reason` | TEXT | NOT NULL |
| P02a-S195 | L570 | `triggered_at` | TEXT | NOT NULL |
| P02a-S196 | L571 | `triggered_by` | TEXT | NOT NULL |

### 2.10 webhook_audit (L581 to L593)

| ID | Statement |
|---|---|
| P02a-S197 | FACT: `CREATE TABLE IF NOT EXISTS webhook_audit`, L581 to L593; no table-level constraints. Comment (HISTORICAL, L576 to L577): "Append-only audit row per POST to /webhook/<scanner_name>. Written regardless of outcome (WR13). Used for forensics + rate analysis." FACT: no trigger or constraint in this range prevents UPDATE or DELETE on it. |
| P02a-S198 | FACT: `source_ip` (L585) is TEXT NOT NULL. INTERPRETATION (from the column name and the "row per POST" comment, L576): it holds the network address of each request (values not examined: security restriction). |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S199 | L582 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S200 | L583 | `ts` | TEXT | NOT NULL |
| P02a-S201 | L584 | `scanner_name` | TEXT | NOT NULL |
| P02a-S202 | L585 | `source_ip` | TEXT | NOT NULL |
| P02a-S203 | L586 | `payload_size_bytes` | INTEGER | NOT NULL |
| P02a-S204 | L587 | `response_code` | INTEGER | NOT NULL |
| P02a-S205 | L588 | `signals_accepted` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S206 | L589 | `signals_rejected` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S207 | L590 | `duration_ms` | INTEGER | NOT NULL |
| P02a-S208 | L592 | `date` | TEXT | GENERATED ALWAYS AS (substr(ts, 1, 10)) STORED |

### 2.11 eod_squareoff_log (L618 to L636)

| ID | Statement |
|---|---|
| P02a-S209 | FACT: `CREATE TABLE IF NOT EXISTS eod_squareoff_log`, L618 to L636; no table-level constraints; uniqueness of `fired_date` comes from the separate UNIQUE index at L638 (section 3). Comment (HISTORICAL, L612 to L614): "One row per EOD square-off fire. UNIQUE on fired_date — only one EOD run per trading day is recorded. Used by EOD9 restart recovery check and by the daily report." |
| P02a-S210 | HISTORICAL (L629 to L633): an IN_PROGRESS row "is written at fire start; UPDATE to COMPLETE after squareoff finishes"; restart recovery treats IN_PROGRESS as "crash mid-fire" and COMPLETE as "already done today". FACT: `status` (L634) has `DEFAULT 'COMPLETE'` and no CHECK. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S211 | L619 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S212 | L620 | `fired_date` | TEXT | NOT NULL (unique by index at L638) |
| P02a-S213 | L621 | `fired_at` | TEXT | NOT NULL |
| P02a-S214 | L622 | `positions_attempted` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S215 | L623 | `positions_succeeded` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S216 | L624 | `positions_failed` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S217 | L625 | `cancels_attempted` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S218 | L626 | `cancels_succeeded` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S219 | L627 | `cancels_failed` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S220 | L628 | `duration_sec` | REAL | NOT NULL; DEFAULT 0.0 |
| P02a-S221 | L634 | `status` | TEXT | NOT NULL; DEFAULT 'COMPLETE' |
| P02a-S222 | L635 | `completed_at` | TEXT | nullable |

### 2.12 reconciliation_log (L649 to L665)

| ID | Statement |
|---|---|
| P02a-S223 | FACT: `CREATE TABLE IF NOT EXISTS reconciliation_log`, L649 to L665. Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L664. Comment (HISTORICAL, L643 to L645): "One row per reconciliation action per cycle. Written by order_reconciler ... Append-only audit of all reconciler decisions — cosmetic (no-ops not written), recoverable, and unrecoverable." |
| P02a-S224 | HISTORICAL (L660 to L663): the insert site "wraps this in try/except, so a rare orphan-scenario FK rejection drops one audit row with an error log rather than crashing the reconciler". The insert site itself: see parts P05 and P06a. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S225 | L650 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S226 | L651 | `ts` | TEXT | NOT NULL |
| P02a-S227 | L652 | `check_name` | TEXT | NOT NULL |
| P02a-S228 | L653 | `tier` | TEXT | NOT NULL |
| P02a-S229 | L654 | `symbol` | TEXT | NOT NULL |
| P02a-S230 | L655 | `trade_id` | TEXT | nullable; FK -> trades(trade_id) (clause at L664) |
| P02a-S231 | L656 | `description` | TEXT | NOT NULL |
| P02a-S232 | L657 | `action_taken` | TEXT | NOT NULL |
| P02a-S233 | L658 | `success` | INTEGER | NOT NULL |

### 2.13 screener_results (L681 to L694)

| ID | Statement |
|---|---|
| P02a-S234 | FACT: `CREATE TABLE IF NOT EXISTS screener_results`, L681 to L694. Table-level constraint: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L693 (comment "O1 (v26)"). Comment (HISTORICAL, L675 to L677): "One row per secondary_screener.screen() call. Append-only audit of all screening decisions (PASSED / REJECTED_* / SKIPPED_*). Used by daily report for screening analytics (SS6)." FACT: no CHECK on `status`. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S235 | L682 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S236 | L683 | `signal_id` | TEXT | NOT NULL; FK -> signals(signal_id) (clause at L693) |
| P02a-S237 | L684 | `score` | INTEGER | NOT NULL |
| P02a-S238 | L685 | `tier` | TEXT | NOT NULL |
| P02a-S239 | L686 | `status` | TEXT | NOT NULL |
| P02a-S240 | L687 | `step_results` | TEXT | NOT NULL |
| P02a-S241 | L688 | `latencies` | TEXT | NOT NULL |
| P02a-S242 | L689 | `market_data_snapshot` | TEXT | NOT NULL |
| P02a-S243 | L690 | `ts` | TEXT | NOT NULL |
| P02a-S244 | L691 | `eligible_score` | INTEGER | nullable |

### 2.14 smart_tgt_state (L713 to L730)

| ID | Statement |
|---|---|
| P02a-S245 | FACT: `CREATE TABLE IF NOT EXISTS smart_tgt_state`, L713 to L730. Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L729. Comment (HISTORICAL, L707 to L709): "Per-trade trailing SL state for SmartTgtManager crash recovery (ST15). One row per active tracked trade. Deleted when trade is unregistered. Repopulated on restart to resume trailing from last known SL level." |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S246 | L714 | `trade_id` | TEXT | PRIMARY KEY (no explicit NOT NULL); FK -> trades(trade_id) (clause at L729) |
| P02a-S247 | L715 | `symbol` | TEXT | NOT NULL |
| P02a-S248 | L716 | `instrument_token` | INTEGER | NOT NULL |
| P02a-S249 | L717 | `direction` | TEXT | NOT NULL |
| P02a-S250 | L718 | `entry_price` | REAL | NOT NULL |
| P02a-S251 | L719 | `initial_sl` | REAL | NOT NULL |
| P02a-S252 | L720 | `current_sl` | REAL | NOT NULL |
| P02a-S253 | L721 | `qty` | INTEGER | NOT NULL |
| P02a-S254 | L722 | `trigger_pct` | REAL | NOT NULL |
| P02a-S255 | L723 | `step_pct` | REAL | NOT NULL |
| P02a-S256 | L724 | `best_price` | REAL | nullable |
| P02a-S257 | L725 | `trail_count` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S258 | L726 | `last_trail_ts` | TEXT | nullable |
| P02a-S259 | L727 | `registered_at` | TEXT | NOT NULL |

### 2.15 innings (L743 to L763)

| ID | Statement |
|---|---|
| P02a-S260 | FACT: `CREATE TABLE IF NOT EXISTS innings`, L743 to L763. Table-level constraints: `UNIQUE(trade_id, inning_number)` at L761 and `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L762. Comment (HISTORICAL, L734 to L739): "One row per simulated inning tracked by shadow_tracker. Inning 1 is always real (is_real=1) ... Innings 2 and 3 are simulated (is_real=0): no real broker orders, pure price watching"; "each trade can have at most 3 innings". FACT: no CHECK limits `inning_number` or `is_real`; the "at most 3" limit is not expressed in the DDL. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S261 | L744 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S262 | L745 | `trade_id` | TEXT | NOT NULL; FK -> trades(trade_id) (clause at L762); part of UNIQUE (L761) |
| P02a-S263 | L746 | `inning_number` | INTEGER | NOT NULL; part of UNIQUE (L761) |
| P02a-S264 | L747 | `symbol` | TEXT | NOT NULL |
| P02a-S265 | L748 | `direction` | TEXT | NOT NULL |
| P02a-S266 | L749 | `entry_price` | REAL | NOT NULL |
| P02a-S267 | L750 | `entry_ts` | TEXT | NOT NULL |
| P02a-S268 | L751 | `sl_price` | REAL | NOT NULL |
| P02a-S269 | L752 | `tgt_price` | REAL | NOT NULL |
| P02a-S270 | L753 | `exit_price` | REAL | nullable |
| P02a-S271 | L754 | `exit_ts` | TEXT | nullable |
| P02a-S272 | L755 | `exit_reason` | TEXT | nullable |
| P02a-S273 | L756 | `duration_sec` | INTEGER | nullable |
| P02a-S274 | L757 | `pnl_pct` | REAL | nullable |
| P02a-S275 | L758 | `pnl_per_share` | REAL | nullable |
| P02a-S276 | L759 | `is_real` | INTEGER | NOT NULL |

### 2.16 gate_state (L780 to L798)

| ID | Statement |
|---|---|
| P02a-S277 | FACT: `CREATE TABLE IF NOT EXISTS gate_state`, L780 to L798. Table-level constraint: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L797. Comment (HISTORICAL, L773 to L778): "One row per signal currently held in the EntryGate. Persisted so that a mid-session restart can rehydrate the in-memory _watchlist"; "Lifecycle: written on entry_gate.add(); deleted on entry_gate._release()." |
| P02a-S278 | HISTORICAL (L794): `added_at` is "naive IST ISO-8601", unlike the header convention of an offset-bearing IST timestamp (L12). |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S279 | L781 | `signal_id` | TEXT | PRIMARY KEY (no explicit NOT NULL); FK -> signals(signal_id) (clause at L797) |
| P02a-S280 | L782 | `symbol` | TEXT | NOT NULL |
| P02a-S281 | L783 | `direction` | TEXT | NOT NULL |
| P02a-S282 | L784 | `trigger_price` | REAL | NOT NULL |
| P02a-S283 | L785 | `entry_price` | REAL | NOT NULL |
| P02a-S284 | L786 | `sl_price` | REAL | NOT NULL |
| P02a-S285 | L787 | `tgt_price` | REAL | NOT NULL |
| P02a-S286 | L788 | `tolerance_pct` | REAL | NOT NULL |
| P02a-S287 | L789 | `timeout_sec` | INTEGER | NOT NULL |
| P02a-S288 | L790 | `strategy_name` | TEXT | NOT NULL |
| P02a-S289 | L791 | `tier` | TEXT | NOT NULL |
| P02a-S290 | L792 | `scanner_name` | TEXT | NOT NULL |
| P02a-S291 | L793 | `intent` | TEXT | NOT NULL |
| P02a-S292 | L794 | `added_at` | TEXT | NOT NULL |
| P02a-S293 | L795 | `extras_json` | TEXT | nullable |

### 2.17 trade_excursions (L824 to L836)

| ID | Statement |
|---|---|
| P02a-S294 | FACT: `CREATE TABLE IF NOT EXISTS trade_excursions`, L824 to L836. Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L835. Comment (HISTORICAL, L813 to L822): "Per-trade MFE/MAE and entry candle snapshot. Written POST-EOD by scripts/reconstruct_excursions.py ... NOT on the hot exit path"; the sign convention is "SIGNED", "NOT floored at zero"; "a sub-minute trade gets no row". |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S295 | L825 | `trade_id` | TEXT | PRIMARY KEY (no explicit NOT NULL); FK -> trades(trade_id) (clause at L835) |
| P02a-S296 | L826 | `mfe_price` | REAL | nullable |
| P02a-S297 | L827 | `mfe_pct` | REAL | nullable |
| P02a-S298 | L828 | `mae_price` | REAL | nullable |
| P02a-S299 | L829 | `mae_pct` | REAL | nullable |
| P02a-S300 | L830 | `entry_candle_open` | REAL | nullable |
| P02a-S301 | L831 | `entry_candle_high` | REAL | nullable |
| P02a-S302 | L832 | `entry_candle_low` | REAL | nullable |
| P02a-S303 | L833 | `entry_candle_close` | REAL | nullable |
| P02a-S304 | L834 | `updated_at` | TEXT | NOT NULL |

### 2.18 pnl_reconciliation (L844 to L853)

| ID | Statement |
|---|---|
| P02a-S305 | FACT: `CREATE TABLE IF NOT EXISTS pnl_reconciliation`, L844 to L853; no table-level constraints; `date` is column-level UNIQUE (L846). Comment (HISTORICAL, L840 to L842): "Daily EOD record comparing broker-reported P&L against system net_pnl. Written by scripts/reconcile_pnl.py at 16:15 IST after market close. Status: OK, VARIANCE_MINOR, VARIANCE_MAJOR, PAPER_SKIPPED, ERROR" (separators changed from the original). FACT: no CHECK on `status`. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S306 | L845 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S307 | L846 | `date` | TEXT | NOT NULL; UNIQUE |
| P02a-S308 | L847 | `broker_pnl` | REAL | nullable |
| P02a-S309 | L848 | `system_pnl` | REAL | NOT NULL |
| P02a-S310 | L849 | `variance` | REAL | nullable |
| P02a-S311 | L850 | `status` | TEXT | NOT NULL |
| P02a-S312 | L851 | `notes` | TEXT | nullable |
| P02a-S313 | L852 | `created_at` | TEXT | NOT NULL |

### 2.19 telegram_alerts (L866 to L875)

| ID | Statement |
|---|---|
| P02a-S314 | FACT: `CREATE TABLE IF NOT EXISTS telegram_alerts`, L866 to L875; no table-level constraints. Comment (HISTORICAL, L862 to L865): "FIX-131 Item 18: Telegram alert delivery log"; "Tracks every Telegram alert attempt for audit + startup retry of CRITICAL"; status values SENT, FAILED, PENDING. FACT: no CHECK on `status` or `severity`. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S315 | L867 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S316 | L868 | `sent_at` | TEXT | NOT NULL |
| P02a-S317 | L869 | `severity` | TEXT | NOT NULL |
| P02a-S318 | L870 | `title` | TEXT | NOT NULL |
| P02a-S319 | L871 | `body` | TEXT | nullable |
| P02a-S320 | L872 | `status` | TEXT | NOT NULL; DEFAULT 'PENDING' |
| P02a-S321 | L873 | `attempts` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S322 | L874 | `source_module` | TEXT | nullable |

### 2.20 trade_journal (L883 to L900)

| ID | Statement |
|---|---|
| P02a-S323 | FACT: `CREATE TABLE IF NOT EXISTS trade_journal`, L883 to L900. Table-level constraint: `FOREIGN KEY (trade_id) REFERENCES trades(trade_id)` at L899. Comment (HISTORICAL, L880 to L882): "FIX-133 Item 30: daily trade journal"; "Structured trade journal for pattern analysis. Populated after EOD." The comment names no writer. FACT: no UNIQUE constraint on (date, trade_id) or on trade_id. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S324 | L884 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S325 | L885 | `date` | TEXT | NOT NULL |
| P02a-S326 | L886 | `trade_id` | TEXT | NOT NULL; FK -> trades(trade_id) (clause at L899) |
| P02a-S327 | L887 | `strategy` | TEXT | NOT NULL |
| P02a-S328 | L888 | `symbol` | TEXT | NOT NULL |
| P02a-S329 | L889 | `direction` | TEXT | NOT NULL |
| P02a-S330 | L890 | `entry_reason` | TEXT | nullable |
| P02a-S331 | L891 | `exit_reason` | TEXT | nullable |
| P02a-S332 | L892 | `slippage_assessment` | TEXT | nullable |
| P02a-S333 | L893 | `mfe_captured_pct` | REAL | nullable |
| P02a-S334 | L894 | `entry_price` | REAL | nullable |
| P02a-S335 | L895 | `exit_price` | REAL | nullable |
| P02a-S336 | L896 | `net_pnl` | REAL | nullable |
| P02a-S337 | L897 | `notes` | TEXT | nullable |
| P02a-S338 | L898 | `created_at` | TEXT | NOT NULL |

### 2.21 position_reconciliation (L911 to L920)

| ID | Statement |
|---|---|
| P02a-S339 | FACT: `CREATE TABLE IF NOT EXISTS position_reconciliation`, L911 to L920; no table-level constraints. Comment (HISTORICAL, L907 to L909): "Per-symbol daily position comparison: broker vs system. Written by scripts/reconcile_positions.py at 15:45 IST after market close"; status values OK, ORPHAN_AT_BROKER, MISSING_AT_BROKER, QTY_MISMATCH, ERROR. FACT: no CHECK on `status`; no UNIQUE on (date, symbol). |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S340 | L912 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S341 | L913 | `date` | TEXT | NOT NULL |
| P02a-S342 | L914 | `symbol` | TEXT | NOT NULL |
| P02a-S343 | L915 | `broker_qty` | INTEGER | nullable |
| P02a-S344 | L916 | `system_qty` | INTEGER | nullable |
| P02a-S345 | L917 | `status` | TEXT | NOT NULL |
| P02a-S346 | L918 | `resolved_at` | TEXT | nullable |
| P02a-S347 | L919 | `created_at` | TEXT | NOT NULL |

### 2.22 strategy_metrics (L933 to L943)

| ID | Statement |
|---|---|
| P02a-S348 | FACT: `CREATE TABLE IF NOT EXISTS strategy_metrics`, L933 to L943. Table-level constraint: `UNIQUE(strategy, date)` at L942. Comment (HISTORICAL, L930 to L931): "Per-strategy daily performance metrics (Sharpe, win rate, etc). Computed at EOD by scripts/compute_strategy_metrics.py." |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S349 | L934 | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| P02a-S350 | L935 | `strategy` | TEXT | NOT NULL; part of UNIQUE (L942) |
| P02a-S351 | L936 | `date` | TEXT | NOT NULL; part of UNIQUE (L942) |
| P02a-S352 | L937 | `sharpe` | REAL | nullable |
| P02a-S353 | L938 | `win_rate` | REAL | nullable |
| P02a-S354 | L939 | `avg_pnl` | REAL | nullable |
| P02a-S355 | L940 | `total_trades` | INTEGER | DEFAULT 0; nullable |
| P02a-S356 | L941 | `computed_at` | TEXT | NOT NULL |

### 2.23 shadow_trades (L957 to L979)

| ID | Statement |
|---|---|
| P02a-S357 | FACT: `CREATE TABLE IF NOT EXISTS shadow_trades`, L957 to L979. Table-level constraints: `FOREIGN KEY (signal_id) REFERENCES signals(signal_id)` at L977 and `FOREIGN KEY (live_trade_id) REFERENCES trades(trade_id)` at L978. Comment (HISTORICAL, L953 to L955): "Shadow paper engine: simulated trades run in parallel with live. Entry at signal trigger price; exit at SL/TGT/EOD simulation. Used for regret analysis in daily report." The paper-engine code that writes it is not traced here (paper-only paths are out of scope; callers in parts P04 to P06). |
| P02a-S358 | HISTORICAL (L969): `live_status` values TRADED, REJECTED, CANCELLED. FACT: its DEFAULT is 'UNKNOWN' (L969) and it has no CHECK. |

| ID | Line | Column | Type | Constraints |
|---|---|---|---|---|
| P02a-S359 | L958 | `shadow_trade_id` | TEXT | PRIMARY KEY (no explicit NOT NULL) |
| P02a-S360 | L959 | `date` | TEXT | NOT NULL |
| P02a-S361 | L960 | `signal_id` | TEXT | NOT NULL; FK -> signals(signal_id) (clause at L977) |
| P02a-S362 | L961 | `symbol` | TEXT | NOT NULL |
| P02a-S363 | L962 | `strategy` | TEXT | NOT NULL |
| P02a-S364 | L963 | `direction` | TEXT | NOT NULL |
| P02a-S365 | L964 | `entry_price` | REAL | NOT NULL |
| P02a-S366 | L965 | `qty` | INTEGER | NOT NULL; DEFAULT 0 |
| P02a-S367 | L966 | `sys_sl` | REAL | NOT NULL |
| P02a-S368 | L967 | `sys_tgt` | REAL | NOT NULL |
| P02a-S369 | L968 | `live_trade_id` | TEXT | nullable; FK -> trades(trade_id) (clause at L978) |
| P02a-S370 | L969 | `live_status` | TEXT | DEFAULT 'UNKNOWN'; nullable |
| P02a-S371 | L970 | `simulated_exit_price` | REAL | nullable |
| P02a-S372 | L971 | `simulated_exit_reason` | TEXT | nullable |
| P02a-S373 | L972 | `simulated_pnl` | REAL | nullable |
| P02a-S374 | L973 | `created_at` | TEXT | NOT NULL |

### 2.24 Value sets stated only in comments (no CHECK in the DDL)

FACT for each row: the column has no CHECK constraint; the listed values come only from a comment (HISTORICAL).

| ID | Table.column | Comment line | Values written in the comment |
|---|---|---|---|
| P02a-S375 | trades.direction | L123 | LONG, SHORT |
| P02a-S376 | trades.exit_reason | L146 | SL_HIT, TGT_HIT, EOD, MANUAL, TIMEOUT, CIRCUIT_BREAKER |
| P02a-S377 | trades.entry_mode | L165 | FULL, SCALE |
| P02a-S378 | trades.order_protocol | L166 | CO_PLUS_TGT, LIMIT_TRIPLE |
| P02a-S379 | trades.mode | L182 | PAPER, LIVE |
| P02a-S380 | trades.tier_multiplier_mode | L214 | 'ON', 'OFF_FLAT' |
| P02a-S381 | trades.binding_constraint | L222 to L224 | risk, capital, concentration, flat, multiplier |
| P02a-S382 | trades.closure_source and trades.exit_mechanism | L244 to L246 | not restated; defined in `core/closure_source.py` (comment) |
| P02a-S383 | orders.transaction_type, order_type, product, variety | L326 to L329 | BUY, SELL; LIMIT, MARKET, SL-M, SL; MIS, CNC, CO; regular, co |
| P02a-S384 | orders.reconciliation_status | L359 to L360 | NULL, OK, MISMATCH, SL_MISSING |
| P02a-S385 | capital_snapshot.sync_source | L424 | 'broker', 'csv', 'startup', 'event' |
| P02a-S386 | system_events.event_type and scenario | L446 to L451, L459 | STARTUP, SHUTDOWN, CRASH_DETECTED, KILL_SWITCH, RECOVERY, CONFIG_DIFF; COLD, WARM, CRASH, HALT |
| P02a-S387 | session.mode and trade_type | L485 to L486 | PAPER, LIVE; INTRADAY, POSITIONAL |
| P02a-S388 | fm_ledger.bucket and direction | L526, L534 | 'intraday', 'positional', 'both'; 'LONG', 'SHORT', NULL |
| P02a-S389 | eod_squareoff_log.status | L634 | IN_PROGRESS, COMPLETE |
| P02a-S390 | reconciliation_log.tier | L653 | COSMETIC, RECOVERABLE, UNRECOVERABLE |
| P02a-S391 | screener_results.status | L676 | PASSED, REJECTED_*, SKIPPED_* |
| P02a-S392 | smart_tgt_state.direction, innings.direction, gate_state.direction, trade_journal.direction, shadow_trades.direction | L717, L748, L783, L889, L963 | LONG, SHORT |
| P02a-S393 | innings.exit_reason | L755 | SL, TGT, EOD, OPEN |
| P02a-S394 | pnl_reconciliation.status | L850 | OK, VARIANCE_MINOR, VARIANCE_MAJOR, PAPER_SKIPPED, ERROR |
| P02a-S395 | telegram_alerts.severity and status | L869, L872 | CRITICAL, ERROR, WARN, INFO; SENT, FAILED, PENDING |
| P02a-S396 | trade_journal.slippage_assessment | L892 | HIGH, LOW |
| P02a-S397 | position_reconciliation.status | L917 | OK, ORPHAN_AT_BROKER, MISSING_AT_BROKER, QTY_MISMATCH, ERROR |
| P02a-S398 | shadow_trades.live_status and simulated_exit_reason | L969, L971 | TRADED, REJECTED, CANCELLED; SL_HIT, TGT_HIT, EOD |
| P02a-S530 | trades.recovered_flag, needs_tgt_retry, exits_verified | L164, L198, L238 | 1 or 0 as described in each comment ("1 if reconstructed during crash recovery"; "1 = TGT placement owed"; "1 = SL+TGT verified ok, 0 = mismatch") |
| P02a-S531 | trades.exits_verify_detail | L239 | 'ok' or free text ("human-readable mismatch description") |
| P02a-S532 | orders.leg_index | L323 | 0 for FULL entry; 0, 1, 2 for SCALE legs |
| P02a-S533 | reconciliation_log.success | L658 | 1 succeeded, 0 failed |
| P02a-S534 | innings.is_real | L759 | 1 real (inning 1), 0 simulated |

## 3. Indexes, triggers and views

### 3.1 Explicit indexes (all `CREATE ... INDEX IF NOT EXISTS`)

| ID | Lines | Index | Table | Columns or expression | UNIQUE | Partial WHERE |
|---|---|---|---|---|---|---|
| P02a-S399 | L82 to L83 | `idx_signals_fingerprint_today` | signals | fingerprint, fingerprint_date | yes | no |
| P02a-S400 | L85 to L86 | `idx_signals_status` | signals | status | no | no |
| P02a-S401 | L88 to L89 | `idx_signals_received_at` | signals | received_at | no | no |
| P02a-S402 | L92 to L93 | `idx_signals_trade_id` | signals | trade_id | no | no |
| P02a-S403 | L257 to L258 | `idx_trades_status` | trades | status | no | no |
| P02a-S404 | L260 to L261 | `idx_trades_symbol` | trades | symbol | no | no |
| P02a-S405 | L263 to L264 | `idx_trades_created_at` | trades | created_at | no | no |
| P02a-S406 | L267 to L268 | `idx_trades_signal_id` | trades | signal_id | no | no |
| P02a-S407 | L370 to L371 | `idx_orders_trade_id` | orders | trade_id | no | no |
| P02a-S408 | L373 to L374 | `idx_orders_status` | orders | status | no | no |
| P02a-S409 | L376 to L377 | `idx_orders_leg` | orders | leg | no | no |
| P02a-S410 | L381 to L382 | `idx_orders_superseded_by` | orders | superseded_by | no | `superseded_by IS NOT NULL` |
| P02a-S411 | L463 to L464 | `idx_events_timestamp` | system_events | timestamp | no | no |
| P02a-S412 | L466 to L467 | `idx_events_type` | system_events | event_type | no | no |
| P02a-S413 | L544 to L545 | `idx_fm_ledger_ts` | fm_ledger | ts | no | no |
| P02a-S414 | L547 to L548 | `idx_fm_ledger_date` | fm_ledger | date (generated column) | no | no |
| P02a-S415 | L550 to L551 | `idx_fm_ledger_reservation_id` | fm_ledger | reservation_id | no | no |
| P02a-S416 | L553 to L554 | `idx_fm_ledger_session_id` | fm_ledger | session_id | no | no |
| P02a-S417 | L595 to L596 | `idx_webhook_audit_ts` | webhook_audit | ts | no | no |
| P02a-S418 | L598 to L599 | `idx_webhook_audit_date` | webhook_audit | date (generated column) | no | no |
| P02a-S419 | L601 to L602 | `idx_webhook_audit_scanner` | webhook_audit | scanner_name | no | no |
| P02a-S420 | L638 to L639 | `idx_eod_squareoff_log_date` | eod_squareoff_log | fired_date | yes | no |
| P02a-S421 | L667 to L668 | `idx_reconciliation_log_ts` | reconciliation_log | ts | no | no |
| P02a-S422 | L670 to L671 | `idx_reconciliation_log_trade_id` | reconciliation_log | trade_id | no | no |
| P02a-S423 | L696 to L697 | `idx_screener_results_signal_id` | screener_results | signal_id | no | no |
| P02a-S424 | L699 to L700 | `idx_screener_results_ts` | screener_results | ts | no | no |
| P02a-S425 | L702 to L703 | `idx_screener_results_status` | screener_results | status | no | no |
| P02a-S426 | L765 to L766 | `idx_innings_trade` | innings | trade_id | no | no |
| P02a-S427 | L768 to L769 | `idx_innings_date` | innings | expression `substr(entry_ts, 1, 10)` | no | no |
| P02a-S428 | L800 to L801 | `idx_gate_state_added_at` | gate_state | added_at | no | no |
| P02a-S429 | L855 to L856 | `idx_pnl_reconciliation_date` | pnl_reconciliation | date | no | no |
| P02a-S430 | L877 to L878 | `idx_telegram_alerts_status_severity` | telegram_alerts | status, severity | no | no |
| P02a-S431 | L902 | `idx_trade_journal_date` | trade_journal | date | no | no |
| P02a-S432 | L903 | `idx_trade_journal_strategy` | trade_journal | strategy | no | no |
| P02a-S433 | L922 to L923 | `idx_position_reconciliation_date` | position_reconciliation | date | no | no |
| P02a-S434 | L925 to L926 | `idx_position_reconciliation_status` | position_reconciliation | status | no | no |
| P02a-S435 | L945 to L946 | `idx_strategy_metrics_strategy` | strategy_metrics | strategy | no | no |
| P02a-S436 | L948 to L949 | `idx_strategy_metrics_date` | strategy_metrics | date | no | no |
| P02a-S437 | L981 to L982 | `idx_shadow_trades_date` | shadow_trades | date | no | no |
| P02a-S438 | L984 to L985 | `idx_shadow_trades_signal` | shadow_trades | signal_id | no | no |

| ID | Statement |
|---|---|
| P02a-S439 | HISTORICAL comments on indexes: L81 "P6 dedup: same scanner + same symbol + same minute on same day = duplicate" (for the UNIQUE fingerprint index); L91 and L266 "O3 (v25)" back-reference lookups; L379 to L380 the partial index serves "SL trail replacement-chain walks" and "only the (few) superseded rows carry a non-NULL value"; L539 to L540 and L591 the generated `date` columns exist so date queries "can use an index instead of wrapping ts in DATE()". |
| P02a-S440 | INTERPRETATION (SQLite semantics): besides the 40 explicit indexes, SQLite creates an automatic unique index for each non-INTEGER PRIMARY KEY and each UNIQUE constraint. In this range that is 11: the 8 TEXT primary keys (section 2.0), pnl_reconciliation.date (L846), innings (trade_id, inning_number) (L761) and strategy_metrics (strategy, date) (L942). INTEGER PRIMARY KEY columns use the rowid and get no separate index. |
| P02a-S441 | INTERPRETATION: SQLite uses the expression index `idx_innings_date` only for queries that use the same expression `substr(entry_ts, 1, 10)`, and uses the partial index `idx_orders_superseded_by` only where the query's WHERE clause implies `superseded_by IS NOT NULL`. Whether queries do so: parts P04 to P06. |
| P02a-S442 | FACT: six tables have no explicit index: schema_meta, capital_snapshot, session, kill_switch_state, smart_tgt_state, trade_excursions. |

### 3.2 Trigger

| ID | Statement |
|---|---|
| P02a-S443 | FACT: one trigger in the range: `CREATE TRIGGER IF NOT EXISTS trg_trades_terminal_status_guard`, L291 to L300. Timing BEFORE; event `UPDATE OF status`; table `trades`; `FOR EACH ROW`. |
| P02a-S444 | FACT: its WHEN clause (L294 to L295) fires only when `OLD.status IN ('CLOSED', 'CLOSED_MANUAL', 'FAILED', 'CANCELLED')` or `OLD.status GLOB 'REJECTED*'`. Its body (L296 to L300) is `SELECT CASE WHEN NEW.status <> OLD.status THEN RAISE(ABORT, 'illegal terminal-state transition on trades.status') END`. |
| P02a-S445 | FACT: the terminal set in the WHEN clause does not include 'UNKNOWN_IN_FLIGHT', 'PENDING', 'PENDING_FILL', 'OPEN', 'PARTIAL' or 'EXITING'; changes between those values are not constrained by any trigger. HISTORICAL (L278 to L281): the scope "is deliberately a TERMINAL-LOCK, not a full transition matrix". |
| P02a-S446 | HISTORICAL (L271 to L286): "Terminal-state write guard (Wave-5, 2026-07-07) — Audit-B Phase-4 rec #5"; it forbids changing status once the row is terminal, "catching EVERY writer including any future raw SQL"; `UPDATE OF status` lets backfills that write price or P&L onto a CLOSED row without touching status pass (`record_manual_close_financials`, `record_gtt_close_financials`); same-status writes pass. |
| P02a-S535 | HISTORICAL (L278 to L281): the comment lists as legal and untouched by the trigger: OPEN, PARTIAL or EXITING to CLOSED (including "H-2 EXITING->CLOSED"), "the recovery flows" and an "EXITING->OPEN revert", each said to originate "from a NON-terminal state". |
| P02a-S447 | INTERPRETATION (SQLite semantics): `UPDATE OF status` fires whenever `status` is in the UPDATE's SET list, and the WHEN and CASE then let same-value writes pass. The trigger does not fire on DELETE, and an `INSERT OR REPLACE` that replaces a terminal row performs a delete and an insert rather than an UPDATE, so it is not caught by this trigger. RAISE(ABORT) aborts the current statement and undoes its changes; an enclosing transaction stays open (consistent with the L287 to L288 comment). |

### 3.3 Views

| ID | Statement |
|---|---|
| P02a-S448 | FACT: there is no `CREATE VIEW` (and no temporary object) in L1 to L990. |

## 4. Non-CREATE statements in the range

| ID | Statement |
|---|---|
| P02a-S449 | FACT: L436 `DROP TABLE IF EXISTS capital_ledger;`, L437 `DROP INDEX IF EXISTS idx_ledger_trade_id;`, L438 `DROP INDEX IF EXISTS idx_ledger_timestamp;`. HISTORICAL (L434): "Drop handled below for upgrade path." |
| P02a-S450 | INTERPRETATION: these DROP statements are part of the script text, so they run every time the whole file is applied; on a database without `capital_ledger` they do nothing. Dropping a table also drops its indexes, so L437 and L438 do nothing after L436 has run (this assumes the two indexes belonged to `capital_ledger`; HISTORICAL: the first commit `bcf03b5` created both ON capital_ledger, `core/schema.sql` L246 to L250 at that commit; the baseline file has no CREATE for them, and no other non-test file at the baseline names them). How often the file is applied: part P03. |
| P02a-S451 | FACT (`grep`): there is no INSERT, UPDATE (other than the trigger event at L292), DELETE, ALTER, PRAGMA, ATTACH, BEGIN or COMMIT statement in L1 to L990, apart from the trigger body's `BEGIN ... END` (L296 to L300). Every other occurrence of those words in the range is inside a `--` comment, except 'COMMIT' at L523, which is a string value in the fm_ledger `entry_type` CHECK list. |

## 5. Routes at the schema level (normal, restart, error, partial failure)

| ID | Statement |
|---|---|
| P02a-S452 | INTERPRETATION (normal and restart): every CREATE in the range uses `IF NOT EXISTS`, so applying the file to an existing database leaves existing tables, indexes and the trigger unchanged, and does not add a column that a table's CREATE text now lists but the existing table lacks; that needs a migration (header L8 to L9 and L20 to L21; see part P03). |
| P02a-S453 | INTERPRETATION (error): a write that violates a NOT NULL, CHECK, UNIQUE or (with foreign keys enabled) FOREIGN KEY constraint, or that the trigger aborts, fails that statement with an SQLite integrity error. How each caller handles it: parts P04 to P06. |
| P02a-S454 | UNKNOWN / NOT ESTABLISHED (partial failure): what state a database is left in if applying the file stops part-way depends on how the application runs it (for example `executescript`, named in the comment at L289) and on its transaction handling; part P03 covers the application path. |

## 6. Counts and data categories

### 6.1 Totals for L1 to L990

| ID | Statement |
|---|---|
| P02a-S455 | FACT: tables 23; columns 299 (2 of them generated); explicit indexes 40 (2 UNIQUE, 1 partial, 1 on an expression, 2 on generated columns); triggers 1; views 0. |
| P02a-S456 | FACT: CHECK constraints 9, all column-level (signals.status, trades.status, orders.leg, orders.status, capital_snapshot.id, session.id, fm_ledger.entry_type, kill_switch_state.id, kill_switch_state.state); FOREIGN KEY clauses 13; table-level UNIQUE constraints 2; column-level UNIQUE 1; AUTOINCREMENT tables 12; single-row tables 3; DROP statements 3. |

### 6.2 Per table: counts and data category as stated by the comment or name

The category is taken only from the table's own comment (or its name); it does not interpret business meaning. Owner topics are in the boundary section.

| ID | Table | Lines | Columns | Explicit indexes | FK clauses | Data category (as stated) | Basis |
|---|---|---|---|---|---|---|---|
| P02a-S457 | schema_meta | L29 to L32 | 2 | 0 | 0 | other: schema version and migration tracking | L26 |
| P02a-S458 | signals | L42 to L79 | 14 | 4 (1 UNIQUE) | 1 | audit or evidence log ("Immutable log" of every webhook signal, with a status field) | L36 to L38 |
| P02a-S459 | trades | L117 to L255 | 59 | 4 | 1 | trading state ("one row per logical position lifecycle") | L97 |
| P02a-S460 | orders | L315 to L368 | 20 | 4 (1 partial) | 2 | trading state ("one row per broker order") | L304 |
| P02a-S461 | capital_snapshot | L410 to L427 | 9 | 0 | 0 | trading state ("Current capital state"); comment says unused since 2026-07-25 | L386, L391 |
| P02a-S462 | system_events | L455 to L461 | 5 | 2 | 0 | audit or evidence log ("Lifecycle marker log"), used for startup scenario detection | L442 to L443 |
| P02a-S463 | session | L478 to L501 | 9 | 0 | 0 | session state ("current session metadata") | L471 |
| P02a-S464 | fm_ledger | L518 to L542 | 17 | 4 | 0 | audit or evidence log ("Append-only write-ahead log" of capital mutations; replayed to rebuild state) | L505, L511 to L512 |
| P02a-S465 | kill_switch_state | L565 to L572 | 5 | 0 | 0 | other: persistent kill-switch control state, recovered on restart | L558 to L559 |
| P02a-S466 | webhook_audit | L581 to L593 | 10 | 3 | 0 | audit or evidence log ("Append-only audit row per POST") | L576 |
| P02a-S467 | eod_squareoff_log | L618 to L636 | 12 | 1 (UNIQUE) | 0 | audit or evidence log (one row per EOD fire), also a restart-recovery marker | L612 to L614 |
| P02a-S468 | reconciliation_log | L649 to L665 | 9 | 2 | 1 | audit or evidence log ("Append-only audit of all reconciler decisions") | L644 to L645 |
| P02a-S469 | screener_results | L681 to L694 | 10 | 3 | 1 | audit or evidence log ("Append-only audit of all screening decisions") | L675 to L676 |
| P02a-S470 | smart_tgt_state | L713 to L730 | 14 | 0 | 1 | trading state (per-trade trailing-SL state for crash recovery) | L707 |
| P02a-S471 | innings | L743 to L763 | 16 | 2 (1 expression) | 1 | analytics or report output (simulated innings; indexes "for daily report") | L734, L739 |
| P02a-S472 | gate_state | L780 to L798 | 15 | 1 | 1 | trading state (signals held in the EntryGate, for restart rehydration) | L773 to L775 |
| P02a-S473 | trade_excursions | L824 to L836 | 10 | 0 | 1 | analytics or report output (MFE/MAE, "trade quality analysis") | L813, L816 |
| P02a-S474 | pnl_reconciliation | L844 to L853 | 8 | 1 | 0 | audit or evidence log (daily broker vs system P&L record) | L840 |
| P02a-S475 | telegram_alerts | L866 to L875 | 8 | 1 | 0 | audit or evidence log ("alert delivery log"), also used for startup retry | L862, L864 |
| P02a-S476 | trade_journal | L883 to L900 | 15 | 2 | 1 | analytics or report output ("trade journal for pattern analysis") | L882 |
| P02a-S477 | position_reconciliation | L911 to L920 | 8 | 2 | 0 | audit or evidence log (daily broker vs system position comparison) | L907 |
| P02a-S478 | strategy_metrics | L933 to L943 | 8 | 2 | 0 | analytics or report output (per-strategy daily metrics) | L930 |
| P02a-S479 | shadow_trades | L957 to L979 | 16 | 2 | 2 | analytics or report output ("regret analysis in daily report") | L953, L955 |

## Concerns for the AUDIT (neutral)

| ID | Statement |
|---|---|
| P02a-S480 | The header says "Version: 1" and "Last updated: 2026-04-14" (L4 to L5) while comments in the range cite versions up to v45 (L241) and the file's version INSERT writes '45' (L1610, part P02b). |
| P02a-S481 | The INITIALIZATION block (L604 to L610) and the "SCHEMA VERSION BUMP: v16 -> v17" header (L858 to L860) are each followed by no version statement in the range. |
| P02a-S482 | Eight TEXT PRIMARY KEY columns carry no NOT NULL (section 2.0). |
| P02a-S483 | Foreign keys depend on each connection setting `PRAGMA foreign_keys = ON` (L17 to L18); no FK clause has an ON DELETE or ON UPDATE action. signals.trade_id and trades.signal_id reference each other (L78, L254; comment L104 to L115). |
| P02a-S484 | Several reference-like columns have no FOREIGN KEY clause: trades.reservation_id (L171, comment says "not enforced"), fm_ledger.signal_id, reservation_id and trade_id (L529, L530, L535). |
| P02a-S485 | Comments call signals an "Immutable log" (L36) and fm_ledger, webhook_audit, reconciliation_log and screener_results "Append-only" (L505 to L506, L576, L644 to L645, L675 to L676); no trigger or constraint in the range enforces append-only or immutability on these tables. The comments say signals.trade_id is set after insertion ("set post-fill ... updated after the trade opens", L108 to L109) and that signals.status is "written by many modules" (L51 to L53); INTERPRETATION: status may therefore change after insertion. |
| P02a-S529 | The signals.status comment counts four GLOB prefix families (L53 to L54) and the L50 list omits RETEST_*, while the CHECK admits five patterns (L66 to L70). |
| P02a-S486 | The trades terminal-state trigger covers `UPDATE OF status` only; it does not cover DELETE or INSERT OR REPLACE (INTERPRETATION, section 3.2), and its terminal list omits 'UNKNOWN_IN_FLIGHT'. |
| P02a-S487 | Many columns have value sets written only in comments, with no CHECK (section 2.24), including several status columns. |
| P02a-S488 | eod_squareoff_log.status defaults to 'COMPLETE' (L634) while the comment describes an IN_PROGRESS write-ahead row (L629 to L633); there is no CHECK. |
| P02a-S489 | shadow_trades.live_status defaults to 'UNKNOWN' (L969) while its comment lists TRADED, REJECTED, CANCELLED. |
| P02a-S490 | capital_snapshot is still created (L410) though its comment says nothing writes it (L391 to L392). |
| P02a-S491 | The session comment says the table holds "kill switch state + daily counters" (L471 to L472); the DDL has neither (L488 to L493 record their removal). |
| P02a-S492 | Timestamps are TEXT. The header convention is offset-bearing IST (L12); gate_state.added_at is described as "naive IST" (L794). The generated `date` columns and `idx_innings_date` take `substr(..., 1, 10)`, which assumes the text starts with YYYY-MM-DD (INTERPRETATION). |
| P02a-S493 | Money is stored as REAL with a stated 1-paise float tolerance (L15 to L16). |
| P02a-S494 | Possible overlapping indexes (INTERPRETATION): `idx_pnl_reconciliation_date` duplicates the automatic unique index on pnl_reconciliation.date; `idx_innings_trade` and `idx_strategy_metrics_strategy` are leading-column prefixes of the automatic UNIQUE indexes at L761 and L942. |
| P02a-S495 | Two FK child columns have no explicit index: trade_journal.trade_id (L886) and shadow_trades.live_trade_id (L968). |
| P02a-S496 | No uniqueness constraint exists on trade_journal (date, trade_id) or on position_reconciliation (date, symbol). |
| P02a-S497 | The trading database stores identifiers in plain columns: session.account_id (L483), webhook_audit.source_ip (L585) and the raw webhook JSON in signals.webhook_payload (L76). Whatever backs up or copies the database carries them too (parts P09a, P09b). |
| P02a-S498 | Schedule times in comments: reconcile_pnl.py "at 16:15 IST" (L841); reconcile_positions.py "at 15:45 IST" (L908); "15:40 backfill" (L815); fno_ban "Fetched at 08:30 IST" (L989). The project index Appendix A lists `reconcile_pnl.py` with no schedule ("—") and `fetch_fno_ban.py` at 08:35; these are A16's to reconcile. |
| P02a-S499 | Generated STORED columns require SQLite 3.31.0 or later (INTERPRETATION); the runtime SQLite version is not established. |

## Questions about intent (OPEN QUESTION, for the project owner)

| ID | Statement |
|---|---|
| P02a-S500 | OPEN QUESTION: was the header "Version: 1 / Last updated: 2026-04-14" (L4 to L5) meant to be kept current, or was the `schema_meta` row always the only version authority? |
| P02a-S501 | OPEN QUESTION: was `DEFAULT 'COMPLETE'` on eod_squareoff_log.status (L634) intended, given the IN_PROGRESS write-ahead design in the comment (L629 to L633)? |
| P02a-S502 | OPEN QUESTION: were the "append-only" and "immutable" statements for fm_ledger, webhook_audit, reconciliation_log, screener_results and signals meant to be enforced by the database, or only by code convention? |
| P02a-S503 | OPEN QUESTION: which topic owns the business meaning of shadow_trades: A09 (whose paths include `capital/shadow_engine.py`) or A18 (shadow extensions)? The comment (L953) names no module. |
| P02a-S504 | OPEN QUESTION: was the absence of uniqueness on trade_journal (date, trade_id) and position_reconciliation (date, symbol) intended (for example, to allow re-runs to append)? |

## UNKNOWN / NOT ESTABLISHED

| ID | Statement |
|---|---|
| P02a-S505 | UNKNOWN / NOT ESTABLISHED: whether any database was created from this file, at which schema version, and with which rows; no database survives. This includes the "0 rows in production" claim for capital_snapshot (L392). |
| P02a-S506 | UNKNOWN / NOT ESTABLISHED: whether `PRAGMA foreign_keys = ON` was in force on the connections that wrote these tables at runtime (code side: part P01). |
| P02a-S507 | UNKNOWN / NOT ESTABLISHED: whether the trigger, the indexes and the generated columns existed in the production database (they depend on the apply and migration path, part P03, and on the SQLite version at runtime). |
| P02a-S508 | UNKNOWN / NOT ESTABLISHED: whether any CHECK, UNIQUE, FK or trigger rejection happened at runtime, and how often. |
| P02a-S509 | UNKNOWN / NOT ESTABLISHED: whether the scheduled writers named in comments (L841, L908, L931, L813 to L814) ran; a schedule is never proof of execution (A16). |

## Boundary handoffs (owner topic: what crosses)

| ID | Statement |
|---|---|
| P02a-S510 | Part P02b: `core/schema.sql` L991 onward, including `fno_ban` (comment header in this range at L987 to L990) and the `schema_version` INSERT at L1610. |
| P02a-S511 | Part P01: connection set-up, `PRAGMA foreign_keys` (L17 to L18) and the ATTACH of the analytics database (L806). |
| P02a-S512 | Part P03: how and when this file is applied (`executescript`, L289), migrations, rebuilds and `schema_version` handling (L8 to L9, L20 to L21, L604 to L610). |
| P02a-S513 | Parts P04, P05, P06a, P06b: every reader and writer of the 23 tables. Part P07: `candles` and `analytics.db` (L804 to L808). Parts P09a and P09b: the "nightly .backup" (L808) and row retention. |
| P02a-S514 | A06 (signal intake): signals and webhook_audit (comment names webhook_receiver and signal_processor, L51 to L53; /webhook POST, L576). |
| P02a-S515 | A07 (screening and decision): screener_results (secondary_screener, L675), gate_state (entry_gate, L778), strategy_metrics (`scripts/compute_strategy_metrics.py`, L931), and the signals statuses written by secondary_screener and entry_gate (L52 to L53). |
| P02a-S516 | A09 (capital, sizing, risk): fm_ledger (FundManager, L505) and the trades sizing and tolerance columns (PositionSizer, L210 to L225; tolerance, L202 to L208). |
| P02a-S517 | A10 (order placement): trades and orders entry fields; order_placer is named at L154, L229 and L231. |
| P02a-S518 | A04 (broker state): the orders.status vocabulary from `broker/order_state_machine.py` and order_monitor (L335 to L338). |
| P02a-S519 | A11 (position management): smart_tgt_state (SmartTgtManager, L707), innings (shadow_tracker, L734), the trades TGT-retry columns (TGTRetryManager, L193 to L200), and the exits_verified after-check (L234 to L239). |
| P02a-S520 | A12 (EOD and reconciliation): eod_squareoff_log (L612 to L614), reconciliation_log (order_reconciler, L643), pnl_reconciliation (`scripts/reconcile_pnl.py`, L841), position_reconciliation (`scripts/reconcile_positions.py`, L908), and trades.closure_source and exit_mechanism (`core/closure_source.py`, L244). |
| P02a-S521 | A13 (kill switch and recovery): kill_switch_state (KillSwitch, L559), the trades EXITING status (kill_switch hard kill, L155 to L157), system_events KILL_SWITCH and RECOVERY events (L449 to L450). |
| P02a-S522 | A01 (startup and orchestration): system_events STARTUP, SHUTDOWN and CRASH_DETECTED scenario detection (L442 to L448) and the session table (L471). |
| P02a-S523 | A14 (alerts): telegram_alerts (L862 to L864). |
| P02a-S524 | A15 (reports and evidence): trade_excursions (`scripts/reconstruct_excursions.py`, L814; A11 may cite), trade_journal (no writer named in the comment; the index lists `scripts/trade_journal.py` under A15, an INTERPRETATION by name), the daily-report uses named at L614, L677, L739, L955, and capital_snapshot's former readers `scripts/healthcheck_server.py` and the dashboard reader (L393 to L394). |
| P02a-S525 | A20 (pre-flight): capital_snapshot's former reader `scripts/preflight/checks/engine.py` (L393). |
| P02a-S526 | A16 (scheduler): the schedule times written in comments (L815, L841, L908, L989) are boundary facts only. |
| P02a-S527 | A09 or A18: shadow_trades (see OPEN QUESTION). A19: the "Verified complete against the full test suite" claim (L59) is tests' evidence and is not examined here. |
