# A03 evidence: The retention and checkpoint scripts

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P09b, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Corrected, 2026-11-09: after the independent check of the STUDY (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** `scripts/db_retention.py`, `scripts/output_retention.py` and `scripts/wal_checkpoint.py`, traced from code (never run), with their declared invocations as A16 boundary facts. Statement IDs `P09b-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

Baseline checks of the three passes (all run against the local read-only clone at the baseline):

- Helper (draft): before and after its work, `git rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty (P09b-S001, P09b-S002). The helper states it wrote no scratch script.
- Checker: before and after its check, the same two commands returned the baseline and an empty status. The checker states it wrote no scratch script and masked absolute home paths on display.
- Corrector: before its work, `git rev-parse HEAD` returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty; after its work, the same (P09b-S195). The corrector read the code lines behind every finding with `sed`, `grep`, `awk` and `git grep` only (absolute home paths masked on display), ran no legacy code and wrote no scratch script; its only writes were this file and its corrections log.

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S001 | Before any work, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline) and `git status --short` printed nothing. | FACT | command output at start of session |
| P09b-S002 | After the work, the same two commands returned the baseline and an empty status (see the closing check at the end of this file). | FACT | command output at end of session |
| P09b-S195 | Corrector: before and after the correction, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` printed nothing. | FACT | command output at start and end of the correction |
| P09b-S003 | Read in full: `scripts/db_retention.py` L1 to L230, `scripts/output_retention.py` L1 to L315, `scripts/wal_checkpoint.py` L1 to L70. | FACT | files at baseline |
| P09b-S004 | Read in part, for the facts the three scripts depend on: `core/state_store.py` L100 to L590 and L3305 to L3321; `core/db_connect.py` L20 to L66; `core/schema.sql` L518 to L702 (six table definitions and indexes); `core/analytics_schema.sql` L24 to L68; `core/logger.py` L266 to L289 and L354 to L452; `core/time_authority.py` L94 to L114; `utils/cron_heartbeat.py` L14 to L95 and L176 to L209; `config/cron_registry.yaml` L1 to L30, L90 to L160, L495 to L565; `deploy/cron/trading-system.cron` L1 to L40 and L100 to L151; `scripts/generate_crontab.py` L45 to L52, L215 to L275; `scripts/cron_officer.py` L512 to L528, L708 to L716; `scripts/preflight/autofix.py` L30 to L45. Further files were reached through `git grep` hits and read at the lines cited where they are used: `config/cron_registry.yaml` L244, L260, L276, L588, L726; `main.py` L1816; `orders/eod_squareoff.py` L501; `ops_dashboard/backend/services/trade_logs.py` L445 to L448; `scripts/backup_evidence.py` L5; `docs/03_daily_operations_runbook.md` L184; `docs/audit/audit_05jul2026.md` L258; `UNPUSHED_LEDGER.md` L1660, L1708; `docs/audit/HANDOFF_30-Aug-2026_night.md` L15; `reports/daily_trade_review.py` L2835; `scripts/alert_watcher.py` L465; `utils/holiday_guard.py`; `.gitignore`. Added at correction: `core/db_connect.py` L44 to L92; `core/state_store.py` L324 to L450; `utils/holiday_guard.py` L38 to L56; `scripts/disk_monitor.py` L30 to L36, L75 to L90, L100 to L154; `deploy/logrotate/trading-system` (whole file); `scripts/backup_restore_drill.py` L180 to L192; `config/cron_registry.yaml` L180 to L198; `deploy/cron/trading-system.cron` L45 to L49. | FACT | files at baseline |
| P09b-S005 | Tools used: `Read`, `grep`, `git grep`, `git log`, `git show`, `git diff`, `git ls-tree`, `sed`/`awk` for line ranges. No legacy code, SQL or shell file was run or imported; no scratch script was written. SQLite and Python behaviour is stated from documented semantics and labelled INTERPRETATION. | FACT | method |
| P09b-S006 | `.env` contents, token files and credential files were not opened. Absolute machine paths in cron lines and docstrings are written here as "the project directory" or "the operator's home directory". | FACT | security rule 4 |
| P09b-S007 | Tests (`tests/`) are not cited. None of the three scripts has a paper/live split, so there is no paper-side path to exclude. | FACT | grep of the three files: no mode branch |

## 1. The three scripts at a glance

| ID | Script | Purpose as written in the file | Entry point | History (commits touching the file, oldest first) | Owner |
|---|---|---|---|---|---|
| P09b-S008 | `scripts/db_retention.py` | HISTORICAL: "deletes rows older than a per-table retention window", the "DB analogue of the log-file cleanup cron" (L11 to L14), from "db_schema_review 15-Jun-2026, observation O5" (L6 to L9). | `main()` L195 to L226, called by `sys.exit(main())` L229 to L230 | `dfe34b2` 2026-06-14 (created, FIX-175); `f172171` 2026-06-14 (VACUUM of main and `analytics` separately); `991f5c3` 2026-06-16 (default DB path made absolute via `_ROOT`). | A03 (index Appendix A) |
| P09b-S009 | `scripts/output_retention.py` | HISTORICAL: "keep-N reaper for reports/output/ and logs/" (L3); retention unit is "SEVEN TRADING DAYS", ranked by the date in the filename, never mtime (L10 to L23). | `main()` L264 to L311, called by `raise SystemExit(main())` L314 to L315 | `12c4ab1` 2026-08-29 (created); `bee9755` 2026-08-29 (dropped the `daily_report_*` family); `28ec9df` 2026-09-10 (comment: evidence exclusion); `e1952e4` 2026-09-11 (comment: SAME-DISK wording). | A03 (index Appendix A) |
| P09b-S010 | `scripts/wal_checkpoint.py` | HISTORICAL: "Runs a PASSIVE WAL checkpoint on the trading DB ... to prevent unbounded WAL growth" (L4 to L5), "FIX-131 Item 23" (L2). | `_cron_main()` L50 to L66, called by `sys.exit(_cron_main())` L69 to L70; `main()` L25 to L47 | `8e884db` 2026-05-30 (created, FIX-131); `f1dc556` 2026-06-02 (heartbeat, FIX-145); `09ea725` 2026-07-17 (holiday skip `_cron_main`). | A03 (index Appendix A) |

## 2. `scripts/db_retention.py`

### 2.1 Arguments, environment and configuration

| ID | Item | Label | Evidence |
|---|---|---|---|
| P09b-S011 | `--db PATH` (default none), `--date YYYY-MM-DD` (default none; help says "defaults to today (IST)"), `--dry-run` (flag), `--vacuum` (flag), `--set TABLE=DAYS` (repeatable). | FACT | L157 to L173 |
| P09b-S012 | With no `--db`, the target is `_ROOT / "data_store" / "trading_system.db"`, where `_ROOT` is the resolved parent of the `scripts/` folder. | FACT | L44, L201 |
| P09b-S013 | With no `--date`, the reference day is `today_ist()`, which returns `now_ist().strftime("%Y-%m-%d")`. | FACT | L208; `core/time_authority.py` L107 to L109 |
| P09b-S014 | The script reads no environment variable and no configuration file; the policy is the in-code dict `DEFAULT_RETENTION`. | FACT | grep for `environ`/`getenv` in the file: none; L63 to L70 |
| P09b-S015 | `--set` values are checked: the item must contain `=`, the table must be a key of `DEFAULT_RETENTION`, and the days must parse as `int`; otherwise `SystemExit` with a message. No lower or upper bound is checked on the days. | FACT | L176 to L192 |
| P09b-S016 | `--date` is not validated by the argument parser; it is first parsed by `datetime.strptime(..., "%Y-%m-%d")` inside `_cutoff`. No comparison with the real current date is made. | FACT | L73 to L77, L105, L208 |

### 2.2 Retention policy and DELETE predicates

The predicate of every DELETE is `DELETE FROM <table> WHERE <date_expr> < ?` with the cutoff string bound as the parameter (L120); the cutoff is `reference date − days`, formatted `YYYY-MM-DD` (L73 to L77). Table and expression come from the in-code dict and are put into the SQL by f-string (L109, L120).

| ID | Table | Database file it lives in | Date expression used (L63 to L70) | Window (days) | What the expression is in the schema | Index on that expression | Label |
|---|---|---|---|---|---|---|---|
| P09b-S017 | `candles` | `analytics.db` (`ANALYTICS_TABLES`, `core/db_connect.py` L26 to L30) | `date` | 90 | STORED generated column `substr(ts, 1, 10)` (`core/analytics_schema.sql` L37); `ts` TEXT NOT NULL (L28) | `idx_candles_date` (L44 to L45) | FACT |
| P09b-S018 | `system_metrics` | `analytics.db` (`core/db_connect.py` L26 to L30) | `date` | 90 | STORED generated column `substr(timestamp, 1, 10)` (`core/analytics_schema.sql` L61); `timestamp` TEXT NOT NULL (L52) | `idx_system_metrics_date` (L67 to L68) | FACT |
| P09b-S019 | `webhook_audit` | main `trading_system.db` | `date` | 90 | STORED generated column `substr(ts, 1, 10)` (`core/schema.sql` L592); `ts` TEXT NOT NULL (L583) | `idx_webhook_audit_date` (L598 to L599) | FACT |
| P09b-S020 | `screener_results` | main | `substr(ts, 1, 10)` | 90 | expression on `ts` TEXT NOT NULL (`core/schema.sql` L690); no `date` column | only `idx_screener_results_ts` on `ts` itself (L699 to L700) | FACT |
| P09b-S021 | `reconciliation_log` | main | `substr(ts, 1, 10)` | 180 | expression on `ts` TEXT NOT NULL (`core/schema.sql` L651); no `date` column | only `idx_reconciliation_log_ts` on `ts` itself (L667 to L668) | FACT |
| P09b-S022 | `fm_ledger` | main | `date` | 365 | STORED generated column `substr(ts, 1, 10)` (`core/schema.sql` L541); `ts` TEXT NOT NULL (L520) | `idx_fm_ledger_date` (L547 to L548) | FACT |

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S023 | The comparison is strict (`<`), so rows whose date equals the cutoff are kept; with the default windows, no row dated on the reference day can match. | FACT (SQL text); INTERPRETATION (effect) | L109, L120; docstring L18 to L19 |
| P09b-S024 | The comparison is a TEXT comparison of `YYYY-MM-DD` strings; for well-formed ISO dates, lexical order equals date order. A `ts` whose first ten characters are not an ISO date would be compared lexically all the same. | INTERPRETATION (SQLite text comparison) | L120; schema lines above |
| P09b-S025 | In `core/schema.sql` and `core/analytics_schema.sql` no `REFERENCES` clause points at any of the six tables and no trigger is defined on any of them (the only trigger is `trg_trades_terminal_status_guard`). | FACT | grep of both schema files: `REFERENCES (fm_ledger or webhook_audit or ...)` none; `CREATE TRIGGER` only at `core/schema.sql` L291 |
| P09b-S026 | The table names in the SQL are unqualified. `candles` and `system_metrics` are found through the `analytics` ATTACH because the main DB no longer defines them after the O6 relocation. | FACT (unqualified names L109, L120; ATTACH `core/state_store.py` L247, `core/db_connect.py` L52 to L64); INTERPRETATION (SQLite name resolution) | see part P07 for the relocation |
| P09b-S027 | `signals` and other tables are not in the policy; the policy has exactly six entries. A legacy audit note says `signals` "has no retention policy". | FACT (L63 to L70); HISTORICAL (`docs/audit/audit_05jul2026.md` L258) | — |

### 2.3 Run flow, transactions and VACUUM

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S028 | `main()` parses arguments and `--set` overrides BEFORE opening the database. | FACT | L196 to L199, then L201 to L206 |
| P09b-S029 | The store is opened with `StateStore(db_path=db_path)` (defaults: `allow_migrate=False`, `market_open=False`). Constructing a `StateStore` creates the parent folder, runs `init_analytics_schema`, opens the connection with the standard PRAGMAs and the `analytics` ATTACH, and runs `executescript(schema_sql)` on every open that passes the schema-file, newer-version and migration-permission checks (see part P01, part P03). The legacy comment at `core/state_store.py` L385 to L387 calls the `executescript` UNCONDITIONAL (HISTORICAL). | FACT; HISTORICAL (comment) | L203; `core/state_store.py` L172 to L198, L195, L363 to L367, L375, L398 to L405, L426 to L427, L446 |
| P09b-S030 | There is no check that the database file exists before opening it. | FACT | L201 to L206 |
| P09b-S031 | `run_retention()` loops over the six policy entries in dict order; for each it computes `days` (override or default) and the cutoff, then works inside a per-table `try`. | FACT | L103 to L106 |
| P09b-S032 | Non-dry-run: each table's DELETE runs inside its own `store.transaction()`, which issues `BEGIN IMMEDIATE`, yields the cursor, then `COMMIT`; on any exception it issues `ROLLBACK` and re-raises. | FACT | L118 to L122; `core/state_store.py` L506 to L543 (L531, L533, L534 to L541) |
| P09b-S033 | Because the connection has `analytics` attached, `BEGIN IMMEDIATE` starts a write transaction on both the main and the analytics database for every table, including the four main-DB tables. | INTERPRETATION (SQLite BEGIN IMMEDIATE semantics) | `core/state_store.py` L247, L531 |
| P09b-S034 | Tables are committed one by one: a failure on a later table does not undo deletions already committed for earlier tables. | INTERPRETATION (per-table COMMIT) | L103 to L131 |
| P09b-S035 | The deleted-row count is `cur.rowcount` after the DELETE. | FACT | L122 |
| P09b-S036 | VACUUM runs only when `vacuum and not dry_run and failures == 0`. It executes `VACUUM` (main) and then `VACUUM analytics` through `store.execute()`, each in its own `try`; a failure adds 1 to `failures`, logs an error and moves on to the next schema. | FACT | L139 to L151 |
| P09b-S037 | `store.execute()` runs the statement directly on the connection opened with `isolation_level=None`, so VACUUM runs outside any explicit transaction. | FACT (`core/state_store.py` L232 to L237, L549 to L562); INTERPRETATION (autocommit) | comment L140 |
| P09b-S038 | When `failures > 0` after the table loop, VACUUM is skipped and no log line says it was skipped. | FACT | L139 (no else branch) |
| P09b-S039 | The "complete" log line (L134 to L137) is written before the VACUUM block; VACUUM failures counted later are not in it. | FACT | L133 to L151 |
| P09b-S040 | `run_retention()` returns the per-table counts (or `-1` for a failed table) plus a `_failures` key. | FACT | L127, L130, L153 to L154 |

### 2.4 Reporting of counts

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S041 | Per-table counts are written only through `log.info(...)` (L113 to L116 dry-run; L123 to L126 apply); the total and failure count only through `extra=` on an INFO record (L134 to L137); start through `extra=` (L209). Nothing is printed to stdout. | FACT | lines cited |
| P09b-S042 | The logger is `get_logger("db_retention")`, which returns `logging.getLogger(name)` and attaches no handler; the docstring says handlers come from `setup_logging()`. `db_retention.py` never calls `setup_logging()` or `logging.basicConfig()`, and no module it imports configures handlers at import time. | FACT | L48, L197; `core/logger.py` L266 to L274 (`get_logger`), L354 to L452 (handlers added only inside `setup_logging`) |
| P09b-S043 | Under default Python logging (root level WARNING, last-resort stderr handler), the INFO records carrying the counts are dropped and only WARNING-and-above records reach stderr, which the cron line appends to `logs/cron-db-retention.log`: from this script, its ERROR lines; from `StateStore`, for example the CRITICAL `MIGRATION_REFUSED` line (`core/state_store.py` L338 to L339) or the ERROR line when the sentinel write fails (L354). The `extra=` fields are not rendered by the last-resort handler. | INTERPRETATION (Python `logging` defaults) | as above; cron L37, L40 |

### 2.5 Safety guards and dry-run

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S044 | Guards present in code: table names only from the fixed dict; `--set` table names checked against it; days must be integers; per-table transaction with rollback; strict `<` cutoff; VACUUM opt-in and skipped after any failure or in dry-run. | FACT | L63 to L70, L176 to L192, L118 to L122, L139 |
| P09b-S045 | Guards absent from code: no lower bound on `--set` days (0 or negative accepted); no check that `--date` is not in the future; no check that a backup exists before pruning; no check of market hours or of another running process; no file lock. | FACT | L157 to L226 (no such check) |
| P09b-S046 | The docstring says to run "after the nightly backup (e.g. 02:30 IST), so a pre-prune snapshot always exists". | HISTORICAL | L28 to L29 |
| P09b-S047 | `--dry-run` replaces the DELETE with `SELECT COUNT(*) AS n FROM <table> WHERE <date_expr> < ?` via `store.fetch_one`, logs the count, and never enters a transaction. | FACT | L107 to L116; `core/state_store.py` L564 to L574 |
| P09b-S048 | `--dry-run` still constructs `StateStore`, so the schema script (`executescript`) and the analytics initialisation still run against the database on a dry run. | FACT | L203; `core/state_store.py` L375, L446 |

### 2.6 Routes and exit codes

| ID | Route | What the code does | Exit code | Label | Evidence |
|---|---|---|---|---|---|
| P09b-S049 | Normal (all tables succeed, no `--vacuum`) | Six per-table transactions; returns `_failures` 0. | 0 | FACT | L103 to L131, L226 |
| P09b-S050 | Normal with `--vacuum` | As above, then `VACUUM` and `VACUUM analytics`. | 0 if both succeed | FACT | L139 to L151, L226 |
| P09b-S051 | One table fails (any exception, e.g. lock wait beyond the 30 s busy timeout, missing table) | That table rolled back, recorded `-1`, error logged with traceback; remaining tables still processed; VACUUM skipped. | 1 | FACT (code); INTERPRETATION (lock example) | L128 to L131, L139, L226; `core/state_store.py` L112, L236 |
| P09b-S052 | VACUUM of one schema fails | `failures` incremented, error logged, next schema attempted. | 1 | FACT | L148 to L151, L226 |
| P09b-S053 | `StateStore` construction fails (including `SchemaVersionMismatch`, `MigrationNotPermitted`, schema file missing, lock timeout during `executescript`) | Error logged "state_store open failed"; returns before any DELETE. A pending migration also makes `StateStore` attempt a CRITICAL sentinel, best-effort (a write failure is logged and swallowed), before it raises (see part P01, part P03). | 1 | FACT | L202 to L206; `core/state_store.py` L326 to L355, L363 to L367, L398 to L405, L426 to L427 |
| P09b-S054 | Database file missing | No existence check; `StateStore` creates the folder and opens the path; a new main database with the full schema is built; the four main-DB DELETEs find no rows, while the `candles` and `system_metrics` DELETEs act on whatever `analytics.db` beside that path already holds (created empty if absent). | 0 | FACT (no check, mkdir, analytics path beside the main path); INTERPRETATION (`sqlite3.connect` creates the file) | L201 to L206, L120; `core/state_store.py` L195, L446; `core/db_connect.py` L47 to L49, L80 to L90 |
| P09b-S055 | Malformed `--date` | `_cutoff` raises `ValueError` at L105, which is OUTSIDE the per-table `try` (L106); it propagates out of `run_retention`, is caught in `main`, logged, store closed. No table is touched. | 1 | FACT | L105 to L106, L211 to L223 |
| P09b-S056 | Bad `--set` | `SystemExit(<message>)` before the DB is opened. | 1 (message on stderr) | FACT (raise); INTERPRETATION (Python exit status for a string `SystemExit`) | L179 to L191 |
| P09b-S057 | Unknown argument | argparse error. | 2 | INTERPRETATION (argparse default) | L157 to L173 |
| P09b-S058 | Unexpected exception outside the per-table `try` | Logged as `db_retention.unexpected_error`, store closed. | 1 | FACT | L220 to L223 |
| P09b-S059 | Retry or restart | No retry logic. A re-run on the same reference date applies the same cutoffs, so rows already deleted are not found again. | — | FACT (no retry); INTERPRETATION (re-run effect) | L80 to L154 |
| P09b-S060 | Process killed mid-DELETE | The open transaction is not committed. | — | INTERPRETATION (SQLite rolls back an uncommitted transaction on next open); UNKNOWN whether it happened | L118 to L122 |
| P09b-S200 | Dry run in which a table's count query fails | The per-table `except` also covers the dry-run `SELECT COUNT(*)`: `failures` is incremented, the table recorded `-1`, and `main` returns 1. The docstring lists exit 0 for "success (all tables pruned, or dry-run)" and 1 for "one or more tables failed, or the store could not be opened" (L31 to L34). | 1 | FACT (code); HISTORICAL (docstring) | L107 to L116, L128 to L131, L226; docstring L31 to L34 |

### 2.7 Declared schedules (boundary facts for A16; no run is inferred)

| ID | Job | Registry lines | Cron line | Expression | Command | Log target | Marker | Flags | Label |
|---|---|---|---|---|---|---|---|---|---|
| P09b-S061 | `db_retention` (Mon to Sat) | `config/cron_registry.yaml` L125 to L139 | `deploy/cron/trading-system.cron` L36 to L37 | `30 2 * * 1-6` (L135) | `scripts/db_retention.py` (L136), no `--vacuum` | `>> logs/cron-db-retention.log 2>&1` (L138) | `db_retention` (L139) | `critical: false`, `market_day_only: false`, `monitored: false` (L129, L130, L132) | FACT |
| P09b-S062 | `db_retention_vacuum` (Sunday) | L140 to L154 | L39 to L40 | `30 2 * * 0` (L150) | `scripts/db_retention.py --vacuum` (L151) | same file (L153) | `db_retention`, the same marker (L154) | same flags (L144, L145, L147) | FACT |
| P09b-S063 | Both registry entries say `schedule: 02:30 daily` (L127, L142) and both cron comments say `[02:30 daily]` (L36, L39), while the expressions are Mon to Sat and Sunday. | — | — | — | — | — | — | — | FACT |
| P09b-S064 | Both cron lines `cd` into the project directory, source `./.env` with `set -a`, set `PYTHONPATH=.`, run the venv Python, append stdout and stderr to the log, then write `"<rc> <date -Iseconds>"` into `data_store/cron_marks/db_retention.done`. | — | — | — | — | — | — | — | FACT (L37, L40) |
| P09b-S065 | `scripts/generate_crontab.py` maps the shared marker back to two job names by the presence of `--vacuum` in the command. | — | — | — | — | — | — | — | FACT (L221 to L222, L270 to L273); A16 |
| P09b-S066 | `db_retention.py` records no cron heartbeat. | — | — | — | — | — | — | — | FACT (no `record_heartbeat` in the file) |

## 3. `scripts/output_retention.py`

### 3.1 Arguments, environment and configuration

| ID | Item | Label | Evidence |
|---|---|---|---|
| P09b-S067 | `--apply` (flag; without it the run is a dry run that deletes nothing), `--keep N` (int, default `KEEP_PER_FAMILY` = 7), `--max-delete N` (int, default `DEFAULT_MAX_DELETE` = 25). | FACT | L96 to L97, L268 to L275 |
| P09b-S068 | No environment variable or configuration file is read; scope, families and exclusions are the in-code list `SCOPES`. The root is `_ROOT`, the resolved parent of `scripts/`, not the working directory. | FACT | L92, L102 to L115, L165; grep for `environ`/`getenv`: none |
| P09b-S069 | `--keep` and `--max-delete` are not range-checked. | FACT | L270 to L274 |

### 3.2 Folders, families and exclusions in code

| ID | Scope folder (under `_ROOT`) | Family globs (each counted on its own) | Never-touch globs | Label | Evidence |
|---|---|---|---|---|---|
| P09b-S070 | `reports/output` | `daily_trade_review_report_*.xlsx` | `.gitkeep` | FACT | L108 to L110 |
| P09b-S071 | `logs` | `system_*.log`, `debug_*.log`, `trades_*.log`, `reconciler_*.log`, `alert_watcher_*.log` | `.holiday_notified_*`, `cron-*.log` | FACT | L111 to L114 |

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S072 | `reports/output/.gitkeep` is a git-tracked file at the baseline; it is the only tracked file under `reports/output`, and `logs/` and `data_store/` are not tracked (`.gitignore` lists `data_store/`, `logs/`, `*.log`, `reports/output/*.xlsx`). | FACT | `git ls-tree -r HEAD reports/output logs data_store`; `.gitignore` L17, L20, L21, L25 |
| P09b-S073 | The code comment says the `daily_report_*.xlsx` family was "dropped here on 29-Aug-2026 when the generator was retired" and that such files on disk are now refused and kept. | HISTORICAL | L103 to L107 |
| P09b-S074 | The header comment still lists `daily_report_*` under the `reports/output/` scope. | FACT | L37 versus L108 to L110 |
| P09b-S075 | The never-touch globs are consulted only for files that matched NO family (the "everything else" loop). A file that matches a family is never checked against them. None of the five log family globs overlaps `cron-*.log` or `.holiday_notified_*`. | FACT (L203 to L210); INTERPRETATION (no overlap, by reading the glob prefixes) | L175 to L182, L203 to L210 |
| P09b-S076 | The comment block "OUT OF SCOPE ON PURPOSE -- DO NOT ADD THESE" names `data_store/backups/` (owned by `backup_retention.py`), `data_store/v3/*.jsonl`, `data_store/evidence/*.jsonl`, `data_store/candles/`, `t2_proof_*/`, `control_tower/`, `cron_marks/` and `security_state.json`. | HISTORICAL | L51 to L67 |
| P09b-S077 | No code path in the script iterates `data_store/` or any folder other than the two scope folders; iteration is `base.iterdir()`, one level only, no recursion. The `data_store` exclusions therefore hold because `data_store` is not in `SCOPES`, not because of any exclusion pattern. | FACT (L169 to L177, L203); INTERPRETATION (consequence) | L102 to L115 |
| P09b-S078 | The comment says the logs "DO NOT REBUILD" and that both xlsx families rebuild from the DB, except `daily_report` files 2026-06-19 to 2026-07-01, archived to `reports/archive_prereconstruct/`. | HISTORICAL | L69 to L74 |

### 3.3 Planning, ranking and deletion

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S079 | `build_plan()` touches nothing; for each scope folder that exists it resolves the folder, and for each family lists files that are regular files, not symlinks, and match the glob by `fnmatch`. A missing scope folder is skipped silently. | FACT | L165 to L182, L170 to L172 |
| P09b-S080 | A family member with no `YYYY-MM-DD` in its name is "REFUSED" ("no date in filename") and is neither kept nor deleted. | FACT | L183 to L186 |
| P09b-S081 | The date is the first match of `(\d{4}-\d{2}-\d{2})` anywhere in the filename; it is not checked to be a real calendar date. | FACT | L99, L129 to L136 |
| P09b-S082 | Members are sorted by `(filename date, name)` descending; the first `keep` are kept and the rest planned for deletion; ties are broken by name. | FACT | L190 to L197 |
| P09b-S083 | Files in a scope folder that matched no family: a symlink is refused ("symlink"); a name matching no never-touch glob is refused ("matches no family"); a never-touch name is silently skipped. Directories and broken symlinks (`is_file()` false) are skipped silently. | FACT (L203 to L210); INTERPRETATION (`Path.is_file` follows symlinks) | L203 to L210 |
| P09b-S084 | Planned size is `p.stat().st_size` for each file to delete, computed during planning. | FACT | L198 |
| P09b-S085 | The cap check `len(plan.to_delete) > args.max_delete` runs before, and independently of, `--apply`; above the cap the run is marked FAILED and NOTHING is deleted. Exactly 25 passes. | FACT | L288 to L293 |
| P09b-S086 | Deletion (`apply_plan`): for each planned path, `_assert_inside(p, fam.base)` compares `os.path.realpath` of the file with the realpath of its family base plus separator, then `stat`, then `p.unlink()`. `FileNotFoundError` logs "already-gone"; any other exception logs "skip" with the error; both continue. | FACT | L215 to L218, L245 to L261 |
| P09b-S087 | The deletion method is a plain `unlink`; nothing is moved, archived or copied first. | FACT | L254 |
| P09b-S088 | `render()` is printed (stdout) before the cap check, with the header "APPLY (deleting)" whenever `--apply` is given, including runs that the cap then aborts. | FACT | L221 to L223, L284, L289 |
| P09b-S089 | Each refused file also produces a WARNING line `output_retention refused <name>: <reason>`. | FACT | L285 to L286 |
| P09b-S090 | Logging is configured by `logging.basicConfig(level=logging.INFO, format="%(message)s")`, so WARNING, INFO and ERROR lines go to stderr. | FACT (L277); INTERPRETATION (basicConfig default stream) | L277 to L278 |
| P09b-S091 | `retention_rule()` builds the sentence stated in the daily cron report from the two constants. | FACT | L118 to L126 |
| P09b-S201 | The printed header always states "keep newest 7 ... cap 25" from the constants through `retention_rule()`, whatever `--keep` or `--max-delete` was given. The `--keep` value itself is not printed (the per-family lines show how many files are kept); the TOTAL line shows the cap actually used. | FACT | L223, L124 to L126, L231 to L233, L240 to L241 |

### 3.4 Heartbeat, routes and exit codes

| ID | Route | What the code does | Exit code | Label | Evidence |
|---|---|---|---|---|---|
| P09b-S092 | Dry run (no `--apply`), under the cap | Prints plan, logs refused files; status SUCCESS; nothing deleted. | 0 | FACT | L281 to L297, L311 |
| P09b-S093 | Dry run over the cap | Status FAILED and ERROR "ABORTED"; nothing deleted. | 1 | FACT | L288 to L293, L311 |
| P09b-S094 | Apply, under the cap | `apply_plan`; INFO `deleted=<n> freed_mb=<x>`; status SUCCESS. | 0 | FACT | L294 to L297, L311 |
| P09b-S095 | Apply, some unlinks fail | Failures logged as WARNING and skipped; status stays SUCCESS; `deleted` counts only successes; no comparison with the planned count. | 0 | FACT | L251 to L261, L294 to L297 |
| P09b-S096 | Apply over the cap | As P09b-S093; nothing deleted. | 1 | FACT | L288 to L293 |
| P09b-S097 | Any exception in planning or rendering (for example a file vanishing between listing and `stat`) | Caught; status FAILED; ERROR logged. | 1 | FACT (catch L298 to L300); INTERPRETATION (example) | L198, L298 to L300 |
| P09b-S196 | Malformed or unknown argument (for example `--keep x`) | `ap.parse_args` runs before `logging.basicConfig` and outside the `try`; argparse exits with its usage error; no plan, no deletion, no heartbeat. | 2 | FACT (order of code); INTERPRETATION (argparse exit status 2) | L264 to L275, L277, L282, L302 to L309 |
| P09b-S197 | Header comment on failure handling | The header says the script "never raises into cron, and records a heartbeat on BOTH the success and failure paths (monitored: true)". | — | HISTORICAL | L76 to L78 |
| P09b-S198 | Pending schema migration at heartbeat time | `record_heartbeat` constructs `StateStore` with the default `allow_migrate=False`; if the stored schema version is older than expected, `_refuse_migration` logs CRITICAL `MIGRATION_REFUSED` (reaching stderr, as `basicConfig` is configured), attempts a CRITICAL sentinel in the database's parent folder (`data_store/`), and raises; `record_heartbeat` catches it and returns False; no heartbeat row is written. The exit code follows `status` as before. See part P03. | 0 or 1 (unchanged) | FACT | L302 to L311; `utils/cron_heartbeat.py` L80 to L95; `core/state_store.py` L326 to L355, L420 to L427 |
| P09b-S098 | Heartbeat | On every route above, `record_heartbeat("output_retention", status=..., duration_sec=..., message="deleted=... freed_mb=...")` is attempted inside a `try` that swallows everything. | — | FACT | L302 to L309 |
| P09b-S099 | Heartbeat target | `record_heartbeat` returns False without writing if `data_store/trading_system.db` does not exist relative to the CURRENT WORKING DIRECTORY; otherwise it constructs a `StateStore` (schema script included) and inserts into `cron_heartbeat` via `insert_cron_heartbeat`; it never raises. | — | FACT | `utils/cron_heartbeat.py` L55 to L62, L80 to L95; `core/state_store.py` L3305, L3321 |
| P09b-S100 | Retry or restart | No retry logic; a re-run recomputes the plan from what is on disk. | — | FACT (no retry); INTERPRETATION (re-run) | L264 to L311 |

### 3.5 Change between `7d4970a` and the baseline

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S101 | `7d4970a` (`7d4970a26991fd40774023f5293a00556228e14b`, 2026-09-02, "docs(ledger,map,paths): close the GUI window ...") is an ancestor of the baseline, 32 commits before it; the file exists there (blob `c250658`). | FACT | `git show 7d4970a`; `git merge-base --is-ancestor`; `git log --oneline 7d4970a..970aabf` |
| P09b-S102 | `git diff 7d4970a 970aabf -- scripts/output_retention.py` shows 10 lines added and 0 removed (blob `c250658` to `e11baf3`), all of them comment lines inside the header block, inserted after the `data_store/v3/*.jsonl` entry; at the baseline they are L56 to L65. | FACT | the diff; L54 to L65 |
| P09b-S103 | No executable line changed: filtering the diff for added or removed lines that are not comments gives 0. `SCOPES`, `KEEP_PER_FAMILY`, `DEFAULT_MAX_DELETE` and all functions are identical at both commits. | FACT | the diff filtered with `grep -v '^[+-]\s*#'` |
| P09b-S104 | The added text names `data_store/evidence/*.jsonl` as out of scope ("Batch 1 forward evidence contract. Append-only and UNREGENERABLE BY CONSTRUCTION ... Never delete."), says it is backed up by `scripts/backup_evidence.py` as "a SAME-DISK copy" that does not protect "against loss of the disk or the machine", and states "excluded-from-pruning is NOT backed-up". | HISTORICAL | L56 to L65 |
| P09b-S105 | The 10 lines came in two steps: `28ec9df` (2026-09-10) added 6 comment lines; `e1952e4` (2026-09-11) replaced one of them with five lines (the SAME-DISK wording). | FACT | `git show 28ec9df -- scripts/output_retention.py`; `git show e1952e4 -- scripts/output_retention.py` |
| P09b-S106 | The commit message of `28ec9df` calls itself "CHECKPOINT, NOT COMPLETE" and says "Nothing was installed to any live crontab". | HISTORICAL | `git show 28ec9df` message |
| P09b-S107 | The evidence exclusion is documentary: the planning and deletion code reached no file under `data_store/` before the change and reaches none after it; the script's only `data_store/` access is the heartbeat write into `data_store/trading_system.db` (P09b-S099). | INTERPRETATION | P09b-S077, P09b-S103; L302 to L309; `utils/cron_heartbeat.py` L61, L84 to L92 |

### 3.6 Declared schedule (boundary fact for A16; no run is inferred)

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S108 | Registry entry `output_retention`: `cron_expression: 10 2 * * *`, `command: scripts/output_retention.py --apply`, `env_wrapper: python`, `log_target: '>> logs/cron-output-retention.log 2>&1'`, `marker_name: output_retention`, `market_day_only: false`, `monitored: true`. | FACT | `config/cron_registry.yaml` L97 to L124 (L115, L117, L120 to L124) |
| P09b-S109 | Generated cron line: `10 2 * * *`, `cd` into the project directory, source `./.env`, `PYTHONPATH=.`, run with `--apply`, append to `logs/cron-output-retention.log`, then write the exit code and time to `data_store/cron_marks/output_retention.done`. | FACT | `deploy/cron/trading-system.cron` L33 to L34 |
| P09b-S110 | `UNPUSHED_LEDGER.md` records the job as "PENDING" with zero `output_retention` lines on the VM crontab at the time it was written; a later legacy handoff note speaks of a first unattended run at 02:10. | HISTORICAL | `UNPUSHED_LEDGER.md` L1660, L1708; `docs/audit/HANDOFF_30-Aug-2026_night.md` L15 |

## 4. `scripts/wal_checkpoint.py`

### 4.1 Target, arguments and connection settings

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S111 | The script defines no command-line arguments (extra words are ignored, as there is no parser) and reads no environment variable. Through `skip_if_non_trading_day` (L61 to L63) it reads the NSE holiday calendar `config/nse_holidays_<year>.yaml`, resolved against the current working directory. | FACT | L1 to L70 (no argparse, no `sys.argv`, no `environ`); `utils/cron_heartbeat.py` L178, L195 to L197; `utils/holiday_guard.py` L44 to L52 |
| P09b-S112 | Target database: `Path(__file__).parent.parent / "data_store" / "trading_system.db"` (not `.resolve()`d). The analytics database is opened directly once by `init_analytics_schema` during `StateStore` construction (WAL, `synchronous = FULL`, `busy_timeout = 30000`, `executescript` of `analytics_schema.sql`) and is then reached through the ATTACH on the working connection. | FACT | L26; `core/state_store.py` L247, L375; `core/db_connect.py` L80 to L90 |
| P09b-S113 | Connection settings come from `StateStore`: `sqlite3.connect(..., isolation_level=None, check_same_thread=True, timeout=30)`, `sqlite3.Row` factory, PRAGMAs `journal_mode = WAL`, `synchronous = FULL`, `foreign_keys = ON`, `temp_store = MEMORY`, `busy_timeout = 30000`; `analytics` attached with `journal_mode = WAL` and `synchronous = FULL`. | FACT | `core/state_store.py` L107 to L113, L227 to L249; `core/db_connect.py` L38 to L41, L52 to L64 |
| P09b-S114 | `StateStore(db_path)` is constructed BEFORE the checkpoint, so the schema script and analytics initialisation run first (see part P01). | FACT | L32; `core/state_store.py` L198, L375, L446 |

### 4.2 Checkpoint mode and outputs

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S115 | The script calls `store.checkpoint_wal()`, which runs `PRAGMA wal_checkpoint(PASSIVE)` and returns `{busy, log, checkpointed}` from the first result row (0s if no row). | FACT | L33; `core/state_store.py` L266 to L283 |
| P09b-S116 | The pragma names no schema. With no schema named, SQLite applies the checkpoint to every attached database in WAL mode, so `analytics.db` is included. | FACT (no schema in the SQL text); INTERPRETATION (SQLite semantics) | `core/state_store.py` L277 |
| P09b-S117 | Which database the single returned row describes when two databases are attached is not established from the legacy code (SQLite-internal behaviour, not verified here). | UNKNOWN / NOT ESTABLISHED | — |
| P09b-S118 | PASSIVE does not wait for readers or writers and does not invoke the busy handler; frames it cannot copy remain in the WAL. | INTERPRETATION (SQLite documented semantics) | `core/state_store.py` L270, L277 |
| P09b-S119 | On success the script closes the store, prints one line to stdout `<IST ISO time> WAL checkpoint(PASSIVE): busy=<b> log=<l> checkpointed=<c>`, then attempts `record_heartbeat("wal_checkpoint")` (default status SUCCESS) inside a `try` that swallows everything. | FACT | L34 to L44; `utils/cron_heartbeat.py` L55 to L57 |
| P09b-S120 | The script does not inspect `busy`, `log` or `checkpointed`; the exit code does not depend on them. | FACT | L35 to L38, L66 |

### 4.3 Routes and exit codes

| ID | Route | What the code does | Exit code | Label | Evidence |
|---|---|---|---|---|---|
| P09b-S121 | Non-trading day | `_cron_main` imports `skip_if_non_trading_day` and calls it; on a weekend or NSE holiday it records a SKIPPED heartbeat ("non-trading day (weekend/NSE holiday)") and returns True; `_cron_main` returns 0 without checkpointing. | 0 | FACT | L61 to L64; `utils/cron_heartbeat.py` L176 to L209 |
| P09b-S122 | Holiday calendar unreadable | `skip_if_non_trading_day` falls back to `weekday() < 5`. | as per route | FACT | `utils/cron_heartbeat.py` L194 to L199 |
| P09b-S123 | Database file missing | Prints "DB not found ... -- skipping" to stdout and calls `sys.exit(0)` inside `main()`; the `SystemExit` passes through `_cron_main`. No heartbeat. | 0 | FACT (L27 to L29); INTERPRETATION (`SystemExit` propagation) | L27 to L29, L65 |
| P09b-S124 | Success | Checkpoint, close, print, SUCCESS heartbeat; `main()` returns None; `_cron_main` returns 0. | 0 | FACT | L31 to L44, L65 to L66 |
| P09b-S125 | Any exception during open, checkpoint, close or print (including `SchemaVersionMismatch`, `MigrationNotPermitted`, a lock held beyond the 30 s wait during the schema script) | Prints "WAL checkpoint FAILED: <exc>" to stderr and `sys.exit(1)`; no heartbeat is recorded. When the checkpoint itself raises, `store.close()` (L34) is skipped; when the open raises there is no store to close; when the print raises, close has already run. | 1 | FACT (L45 to L47, close only at L34); INTERPRETATION (lock example) | L31 to L47; `core/state_store.py` L112, L236, L426 to L427 |
| P09b-S126 | Heartbeat failure | Swallowed (L43 to L44); `record_heartbeat` itself returns False rather than raising. | 0 | FACT | L39 to L44; `utils/cron_heartbeat.py` L94 to L95 |
| P09b-S127 | `utils.cron_heartbeat` cannot be imported in `_cron_main` | The import at L61 is not inside a `try`; the exception is uncaught. | non-zero (traceback) | FACT (unguarded import); INTERPRETATION (Python exit status 1) | L61 |
| P09b-S128 | Database busy | The PASSIVE checkpoint itself returns without waiting (P09b-S118); only the `StateStore` open path waits up to 30 s and then fails into route P09b-S125. | 0 or 1 | INTERPRETATION | L32 to L33; `core/state_store.py` L112, L236 |
| P09b-S129 | Retry or restart | No retry logic. | — | FACT | L1 to L70 |
| P09b-S130 | Path resolution | The heartbeat writer uses `data_store/trading_system.db` relative to the current working directory, while the checkpoint uses a path relative to the script file. Under the cron line (which `cd`s into the project directory) both point to the same file. The holiday calendar folder (`config`, default of `skip_if_non_trading_day`) is also resolved against the working directory; outside the project directory the calendar read fails and the weekday fallback applies. | — | FACT (paths); INTERPRETATION (equality under cron; fallback outside the project directory) | L26; `utils/cron_heartbeat.py` L61, L178, L179, L194 to L199; cron L109 |
| P09b-S199 | Pending schema migration | `main()`'s own `StateStore` open is refused first, so the route is P09b-S125 (exit 1). On a non-trading day the SKIPPED heartbeat's `StateStore` open is refused instead: CRITICAL `MIGRATION_REFUSED` is logged, a CRITICAL sentinel is attempted in `data_store/`, `record_heartbeat` returns False and `_cron_main` still returns 0 (see P09b-S198, part P03). | 1 (trading day) or 0 (non-trading day) | FACT | L32, L61 to L64; `utils/cron_heartbeat.py` L80 to L95, L201 to L208; `core/state_store.py` L326 to L355, L420 to L427 |

### 4.4 Relation to `StateStore.checkpoint_wal` and `StateStore.checkpoint`

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S131 | The script uses `checkpoint_wal()` (PASSIVE), not `checkpoint()`. `checkpoint()` runs `PRAGMA wal_checkpoint(TRUNCATE)` and skips itself only when a `live_feed` argument is passed and the call comes from that feed's ticker thread (FIX-088); the one non-test caller passes no `live_feed` (`orders/eod_squareoff.py` L501). Both are defined in `core/state_store.py` (see part P01). | FACT | L33; `core/state_store.py` L266 to L320 (L277, L299 to L310, L313) |
| P09b-S132 | Other non-test callers: `main.py` L1816, in `_shutdown` (L1599), calls `store.checkpoint_wal()` on shutdown (A01); `orders/eod_squareoff.py` L501, in `EodSquareoff._fire` (class L96, def L326), calls `self._store.checkpoint()` (TRUNCATE) in the end-of-day square-off (A12). | FACT | `git grep` for `.checkpoint_wal(` and `.checkpoint(` |
| P09b-S202 | A third PASSIVE checkpoint site exists outside `StateStore`: `scripts/backup_restore_drill.py` L186, in `check_wal_clean` (L183), runs a raw `PRAGMA wal_checkpoint(PASSIVE)` on its own direct `sqlite3.connect` (see part P09a). | FACT | `scripts/backup_restore_drill.py` L183 to L191 |
| P09b-S133 | The `checkpoint_wal` docstring says it is "Intended for: graceful shutdown + 16:00 IST cron job"; the `checkpoint` docstring says it is "Called by EOD squareoff after all positions closed". | HISTORICAL | `core/state_store.py` L272, L290 |

### 4.5 Declared schedule (boundary fact for A16; no run is inferred)

| ID | Statement | Label | Evidence |
|---|---|---|---|
| P09b-S134 | Registry entry `wal_checkpoint`: `cron_expression: 0 16 * * 1-5`, `command: scripts/wal_checkpoint.py`, `env_wrapper: python_nopath`, `log_target: '>> logs/wal_checkpoint.log 2>&1'`, `market_day_only: true`, `cadence: market_day`, `monitored: true`; no `marker_name` key. | FACT | `config/cron_registry.yaml` L502 to L515 |
| P09b-S135 | Generated cron line: `0 16 * * 1-5`, `cd` into the project directory, source `./.env`, run the venv Python WITHOUT `PYTHONPATH=.`, append to `logs/wal_checkpoint.log`; no `cron_marks` marker is written. | FACT | `deploy/cron/trading-system.cron` L108 to L109; `scripts/generate_crontab.py` L51 |
| P09b-S136 | The cron file header says "All times IST (Asia/Kolkata)"; the file sets `SHELL=/bin/bash` and contains no `CRON_TZ` or `TZ=` line. | FACT (no such line); HISTORICAL (header text) | `deploy/cron/trading-system.cron` L11, L13 |
| P09b-S137 | The script's own docstring gives a different crontab line, `0 10 * * 1-5` with absolute paths in the operator's home directory, explained as "(0 10 UTC = 15:30 IST + 30 min = 16:00 IST; adjusted for UTC+5:30)". INTERPRETATION: 10:00 UTC corresponds to 15:30 IST (UTC+5:30); the docstring then adds 30 minutes to state 16:00 IST. | HISTORICAL (docstring); INTERPRETATION (arithmetic) | L7 to L12 |
| P09b-S138 | No unit or timer in `deploy/systemd/` references any of the three scripts. | FACT | grep of `deploy/systemd/` (7 files): no match |

## 5. Callers and references of the three scripts (non-test)

| ID | Path and lines | Function or context | What it does with the script | Owner topic | Label |
|---|---|---|---|---|---|
| P09b-S139 | `deploy/cron/trading-system.cron` L37, L40, L34, L109 | cron lines | invoke `db_retention.py`, `db_retention.py --vacuum`, `output_retention.py --apply`, `wal_checkpoint.py` | A16 | FACT |
| P09b-S140 | `config/cron_registry.yaml` L97 to L154, L502 to L515 | registry entries | declare the four jobs above | A16 | FACT |
| P09b-S141 | `scripts/cron_officer.py` L516 to L528, called at L713 | `_output_retention_line` | imports `scripts.output_retention.retention_rule` and puts the sentence in the end-of-day report; reads constants only, deletes nothing | A16 | FACT |
| P09b-S142 | `scripts/generate_crontab.py` L221 to L222, L270 to L273 | `resolve_job_name` and the enrichment loop | split the shared `db_retention` marker into two job names | A16 | FACT |
| P09b-S143 | `utils/cron_heartbeat.py` L55 to L95, L176 to L209 | `record_heartbeat`, `skip_if_non_trading_day` | called BY `output_retention.py` L304 to L307 and `wal_checkpoint.py` L41 to L42, L61 to L63; write `cron_heartbeat` rows through `StateStore.insert_cron_heartbeat` | A16 (helper); storage A03 | FACT |
| P09b-S144 | `ops_dashboard/backend/services/trade_logs.py` L445 to L448 | text string | states that `db_retention.py` prunes `screener_results` 90d, `reconciliation_log` 180d, `webhook_audit` 90d, `fm_ledger` 365d; no call | A15 | FACT |
| P09b-S145 | `scripts/preflight/autofix.py` L37 | `SAFE_FIX_ACTIONS` | lists the name `wal_checkpoint_passive`; no handler for that name was found elsewhere in non-test, non-doc code | A20 | FACT |
| P09b-S146 | `docs/03_daily_operations_runbook.md` L184 | runbook text | tells the operator to run `python3 scripts/wal_checkpoint.py` when the database is locked | legacy document | HISTORICAL |
| P09b-S147 | `scripts/backup_evidence.py` L5 | docstring | refers to `output_retention.py` not deleting the evidence files | A03 (see part P09a) | HISTORICAL |

## Concerns for the AUDIT (neutral)

| ID | What the code does, where | Label |
|---|---|---|
| P09b-S148 | `db_retention.py` reports its per-table counts, totals and start/complete only at INFO level (L113 to L137, L209) and configures no logging handler (L197); under Python defaults those lines would not reach `logs/cron-db-retention.log`. | INTERPRETATION |
| P09b-S149 | `db_retention.py --dry-run` still opens `StateStore`, which runs the schema script and analytics initialisation against the live file (L203; `core/state_store.py` L375, L446). | FACT |
| P09b-S150 | `db_retention.py` has no existence check on the database file (L201 to L206), while `wal_checkpoint.py` has one (L27 to L29). | FACT |
| P09b-S151 | `db_retention.py` accepts `--set` days of 0 or below and any `--date`, including a future date (L176 to L192, L208). | FACT |
| P09b-S152 | `db_retention.py` skips VACUUM without a log line when any table failed (L139). | FACT |
| P09b-S153 | `screener_results` and `reconciliation_log` are pruned with `substr(ts, 1, 10) < ?` (L67 to L68); their only date-related index is on `ts` itself (`core/schema.sql` L667 to L668, L699 to L700). | FACT (SQL and indexes); INTERPRETATION (that the expression cannot use the `ts` index) |
| P09b-S154 | Both `db_retention` cron entries write the same marker file and the same log file (registry L139, L154; cron L37, L40), and both registry `schedule` texts say "02:30 daily" (L127, L142). | FACT |
| P09b-S155 | `db_retention` is `monitored: false` and records no heartbeat; `output_retention` and `wal_checkpoint` are `monitored: true` (registry L132, L147, L117, L509). | FACT |
| P09b-S156 | `db_retention.py` performs no check that a backup exists before deleting, though its docstring says it is meant to run after the backup (L28 to L29). | FACT |
| P09b-S157 | `output_retention.py` header comment L37 still lists `daily_report_*`; the code no longer has that family (L108 to L110). | FACT |
| P09b-S158 | `output_retention.py` exclusions by name work only because no family glob overlaps them (L203 to L210). | INTERPRETATION |
| P09b-S159 | `output_retention.py` returns FAILED and exit 1 on a DRY RUN whose plan exceeds the cap (L288 to L293). | FACT |
| P09b-S160 | `output_retention.py` prints "APPLY (deleting)" before a cap abort (L284, L289). | FACT |
| P09b-S161 | `output_retention.py` keeps status SUCCESS when some planned unlinks fail (L251 to L261, L294 to L297). | FACT |
| P09b-S162 | `output_retention.py` accepts `--keep 0` or a negative value (L270 to L271, L193); the "FLOOR" claim in the comment (L29 to L31) assumes a positive keep. | FACT (no check); INTERPRETATION (slice effect) |
| P09b-S163 | Undated append-mode logs in `logs/` other than `cron-*.log` (for example `logs/wal_checkpoint.log`, `logs/preflight.log`, `logs/daily_report.log`, `logs/trade_journal.log`, `logs/system-manager.log`, named as `log_target` in `config/cron_registry.yaml` L244, L260, L276, L515, L555, L588, L726; the L555 entry is marked `enabled: false` at L550) match no family and are refused on every run; none of the three scripts deletes or truncates them. | FACT (globs and log targets); INTERPRETATION (that they are refused) |
| P09b-S164 | Four declared mechanisms delete files in `logs/`: the shell job `log_cleanup` (`find ... -name '*.log' -mtime +30 -delete`, cron L15 to L16); `output_retention.py` (keep newest 7 by filename date); `scripts/disk_monitor.py` `_cleanup_old_files` (A15; only at critical disk usage; files with mtime older than `_KEEP_DAYS` = 2; the oldest tenth, at least one; no name exclusion other than the `.db`, `.db-wal`, `.db-shm` suffixes; also acts on `reports/output/`; L34, L77 to L87, L104 to L154; declared hourly, cron L48 to L49, registry L183 to L197); and the logrotate configuration `deploy/logrotate/trading-system` L15 to L28 (A17; targets `logs/*.log`, `logs/*.log.*`, `logs/cron-*.log`; `daily`, `maxage 30`, `rotate 0`; no installer reference found in `deploy/install_vm_services.sh`). | FACT (code and declarations); UNKNOWN / NOT ESTABLISHED (installation of the logrotate file) |
| P09b-S165 | The evidence exclusion added after `7d4970a` is a comment only (P09b-S102 to P09b-S107). | FACT |
| P09b-S166 | `output_retention.py` does not validate that the filename date is a real date (L99, L135). | FACT |
| P09b-S167 | `wal_checkpoint.py` docstring crontab (`0 10 * * 1-5`, L7 to L12) and the generated cron line (`0 16 * * 1-5`, cron L109) differ; the cron file sets no `CRON_TZ` (P09b-S136). | FACT |
| P09b-S168 | The `_cron_main` docstring says the guard is placed there "so a manual checkpoint still works" (L55 to L56), but the script's `__main__` entry calls `_cron_main` (L69 to L70), so a command-line run such as the runbook's (P09b-S146) also passes through the holiday guard; only a Python call to `main()` bypasses it. | FACT |
| P09b-S169 | `wal_checkpoint.py` records no heartbeat on its failure route or when the DB is missing (L27 to L29, L45 to L47), and its cron line writes no marker (cron L109; registry L502 to L515 has no `marker_name`). | FACT |
| P09b-S170 | `wal_checkpoint.py` exits 0 whatever the checkpoint figures are (L35 to L38, L66). | FACT |
| P09b-S171 | `wal_checkpoint.py` opens `StateStore`, which writes (schema script) before checkpointing (L32; `core/state_store.py` L446). | FACT |
| P09b-S203 | `scripts/disk_monitor.py` `_cleanup_old_files` excludes only the `.db`, `.db-wal`, `.db-shm` suffixes (L126), so `reports/output/.gitkeep`, `logs/cron-*.log` and `logs/.holiday_notified_*`, which `output_retention.py` never deletes, are eligible there (P09b-S164). | FACT (code); INTERPRETATION (eligibility, by reading the suffix test) |
| P09b-S204 | The `wal_checkpoint.py` docstring computes "0 10 UTC = 15:30 IST + 30 min = 16:00 IST" (L12), while 10:00 UTC is 15:30 IST (P09b-S137). | FACT (text); INTERPRETATION (arithmetic) |
| P09b-S205 | `output_retention.py` header says it "never raises into cron" and records a heartbeat on both paths (L76 to L78), while an argument error exits through argparse before the `try`, with exit 2 and no heartbeat (P09b-S196). | FACT (code order); INTERPRETATION (exit status) |
| P09b-S206 | `output_retention.py` prints the constant keep and cap in its header line whatever `--keep` or `--max-delete` was given (L223, L124 to L126; P09b-S201). | FACT |
| P09b-S172 | The Sunday `db_retention --vacuum` (02:30, cron L40) and the monthly `backup_restore_drill.py` (03:00 on the 1st, cron L151) are both declared in the early morning; whether they ever overlapped is not established. | FACT (declarations); UNKNOWN (overlap) |

## Questions about intent (OPEN QUESTION, for the project owner)

| ID | Question | Label |
|---|---|---|
| P09b-S173 | Were the `db_retention` per-table counts meant to appear in `logs/cron-db-retention.log`? The script relies on a logger that it never configures (P09b-S041 to P09b-S043). | OPEN QUESTION |
| P09b-S174 | Was `--dry-run` of `db_retention.py` meant to be free of any write to the database, given that opening `StateStore` re-applies the schema (P09b-S048)? | OPEN QUESTION |
| P09b-S175 | Was the `data_store/evidence/*.jsonl` exclusion meant to be enforced in code, or was the comment the whole of the intended change (P09b-S107)? | OPEN QUESTION |
| P09b-S176 | Was the `wal_checkpoint` job meant to run at 16:00 IST (registry and cron file) or at 10:00 UTC (script docstring), and in which timezone was the cron daemon meant to run (P09b-S136, P09b-S137)? | OPEN QUESTION |
| P09b-S177 | Was a manual command-line `wal_checkpoint.py` run on a holiday meant to be skipped (P09b-S168)? | OPEN QUESTION |
| P09b-S178 | Were the undated append-mode logs in `logs/` (P09b-S163) meant to fall under any retention, and which tables beyond the six (for example `signals`) were meant to be pruned (P09b-S027)? | OPEN QUESTION |

## UNKNOWN / NOT ESTABLISHED

| ID | Item | Label |
|---|---|---|
| P09b-S179 | Whether any of the four cron entries was installed on either legacy machine, and whether any run took place; no crontab, log, marker file or database survives. | UNKNOWN / NOT ESTABLISHED |
| P09b-S180 | Rows deleted per table, VACUUM duration or effect, files deleted by `output_retention`, and WAL sizes before or after any checkpoint. | UNKNOWN / NOT ESTABLISHED |
| P09b-S181 | The timezone in which the cron daemon on the legacy machines interpreted the schedules. | UNKNOWN / NOT ESTABLISHED |
| P09b-S182 | Whether sourcing `./.env` succeeded on any run (a failure would stop the `&&` chain before Python while the marker line still records a code). | UNKNOWN / NOT ESTABLISHED |
| P09b-S183 | Lock contention at 02:30 or 16:00 with the trading application or other jobs. | UNKNOWN / NOT ESTABLISHED |
| P09b-S184 | The SQLite library version on the legacy machines (relevant to `VACUUM <schema>` and checkpoint behaviour across attached databases). | UNKNOWN / NOT ESTABLISHED |
| P09b-S185 | Which database's figures the single `wal_checkpoint` result row reported with `analytics.db` attached (P09b-S117). | UNKNOWN / NOT ESTABLISHED |
| P09b-S186 | Whether the producers of the log families wrote only on trading days, as the `output_retention.py` comment claims (L16 to L18). | UNKNOWN / NOT ESTABLISHED |

## Boundary handoffs (owner topic: what crosses)

| ID | Owner topic | What crosses | Label |
|---|---|---|---|
| P09b-S187 | A16 | The four schedule declarations, the shared `db_retention` marker, the `cron_marks/*.done` lines, the `.env` sourcing prefix, `generate_crontab.py`'s marker split, the `utils/cron_heartbeat.py` helpers (`record_heartbeat`, `skip_if_non_trading_day`) and `cron_officer.py`'s use of `retention_rule()`. | FACT |
| P09b-S188 | A15 | `core/logger.py` (`get_logger`, `setup_logging`) and the log files it names `system_`, `trades_`, `reconciler_`, `debug_` plus the date (`core/logger.py` L391 to L415); the `reports/output` xlsx producer `reports/daily_trade_review.py` L2835; the dashboard text in `ops_dashboard/backend/services/trade_logs.py` L445 to L448; `scripts/disk_monitor.py` `_cleanup_old_files`, which deletes files in `logs/` and `reports/output/` at critical disk usage (L77 to L87, L104 to L154). | FACT |
| P09b-S189 | A14 | `logs/alert_watcher_<YYYY-MM-DD>.log` written by `scripts/alert_watcher.py` (L465 docstring). | FACT |
| P09b-S190 | A01 | `core/time_authority.py` (`today_ist`, `now_ist`), `utils/holiday_guard.py` (`is_trading_day`), and the shutdown call `main.py` L1816 to `checkpoint_wal()`. | FACT |
| P09b-S191 | A12 | `orders/eod_squareoff.py` L501 call to `checkpoint()` (TRUNCATE). | FACT |
| P09b-S192 | A17 | The `.env` file sourced by the cron lines (name only) and the absolute project and venv paths in the cron file; `deploy/logrotate/trading-system`, which declares a 30-day retention (`maxage 30`, `rotate 0`) on `logs/*.log`, `logs/*.log.*`, `logs/cron-*.log` (L15 to L28), installation not established. | FACT; UNKNOWN / NOT ESTABLISHED (installation) |
| P09b-S193 | A20 | The `wal_checkpoint_passive` name in `scripts/preflight/autofix.py` L37. | FACT |
| P09b-S194 | A03 internal | Part P01: `StateStore` connections, PRAGMAs, `transaction()`, `checkpoint_wal()`, `checkpoint()`; part P03: migration refusal on open; part P07: `analytics.db`, ATTACH and relocation; parts P02a and P02b: the six tables' columns and indexes; part P05 or P04: `insert_cron_heartbeat`; part P08b: `data_store/cron_marks/` and other script-written files; part P09a: `db_backup`, `analytics_backup`, `backup_retention.py`, `backup_evidence.py`, `backup_restore_drill.py`. | FACT |

Closing check: after writing the draft, the helper ran `git rev-parse HEAD` and `git status --short` on the local read-only clone again; result recorded in P09b-S002. After writing this corrected file, the corrector ran the same two commands; result recorded in P09b-S195.
