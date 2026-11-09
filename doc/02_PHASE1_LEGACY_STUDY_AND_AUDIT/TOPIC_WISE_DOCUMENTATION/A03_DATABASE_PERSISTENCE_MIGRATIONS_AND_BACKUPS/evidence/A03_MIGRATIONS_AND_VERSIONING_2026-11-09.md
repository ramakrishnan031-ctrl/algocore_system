# A03 evidence: Migrations and schema versioning

**Status:** DRAFT — evidence for the A03 STUDY, for ChatGPT's review
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P03, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Corrected, 2026-11-09: after the independent check of the STUDY (STUDY, section 1.5).
**Purpose and scope:** How the schema is applied and versioned on open, the migration steps of `core/migrations.py`, their guards, callers, atomicity and failure routes. Statement IDs `P03-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

- **Baseline checks of all three passes** (`git rev-parse HEAD` and `git status --short` on the local read-only clone):

| Pass | Before work | After work |
|---|---|---|
| Helper (draft) | HEAD `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (baseline); status empty | same commit; status empty |
| Checker | HEAD baseline; status empty | same commit; status empty; also `git status --short --ignored` empty, no `__pycache__` or `.pyc` in the clone, the clone's index file not modified since the clone was made, no tracked file named like a standard-library module |
| Corrector | HEAD baseline; status empty | same commit; status empty (re-run after writing both corrector files) |

- **Helper's baseline record (as drafted).** Before work: `rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty. After work: the same two commands returned the same commit and an empty status (re-run at the end; see the last line of this section).
- **Read in full:** `core/migrations.py` L1 to L444; `core/state_store.py` L1 to L149 (header, constants, exception classes), L172 to L249 (`__init__`, `_get_conn`, `_open_connection`, for the open sequence only; connection details are part P01's), L326 to L499 (`_refuse_migration`, `_initialize_schema`, `_read_existing_version`, `get_schema_version`, `migrate_to_latest`); `main.py` L1 to L20 (exit-code list), L2086 to L2240, L2296 to L2302, L2476 to L2482, L4281 to L4293; `core/db_connect.py` L1 to L137; `core/exceptions.py` (class lines only); `deploy/systemd/trading-system.service` L27 to L35 (boundary only).
- **Read in part:** `core/schema.sql` L1 to L45, L280 to L300, L1595 to L1654 (version stamp and footer; the schema itself is parts P02a and P02b); `core/analytics_schema.sql` (grep only); the store-open lines and exception handlers of every non-test `StateStore(...)` caller (section 2.4); `scripts/preflight/checks/database.py` L15 to L95; `scripts/backfill_closure_source_w8.py` L170 to L200; `scripts/backup_restore_drill.py` L120 to L132; `scripts/deploy_assert.py` L55 to L66; `ops_dashboard/backend/readers/db_reader.py` L113 to L120; `ops/control_tower/db.py` L1 to L25; `utils/cron_heartbeat.py` L76 to L100 and L140 to L173; `alerts/critical.py` L52 to L63 (signature only); `docs/audit/migration_on_open_rule_14jul2026.md` (HISTORICAL); one line each of `PATHS.md` L151 and `docs/MASTER_PENDING_01-Aug-2026.md` L166 to L168 (HISTORICAL).
- **Tools.** `grep` / `git grep` (non-test code, `tests/` and `ops_dashboard/tests/` excluded), `git show`, `git log`. Two scratch scripts kept in the work area's tools folder (outside the clone), run with `python3 -I`, parse legacy text only: `p03_schema_history.py` (reads `core/schema.sql` at every commit that touched it via `git show`, extracts the stamped version and each `CREATE TABLE` block with comments stripped, and reports changed, added and removed tables; also reimplements the `_extract_block` scanner of `core/migrations.py` L144 to L167 to compare it with a comment-aware scanner on the baseline text) and `p03_store_openers.py` (Python `ast` scan of each `StateStore(...)` call: enclosing function, keyword arguments, enclosing `try` handlers). No legacy module was imported and no legacy script, SQL or shell file was run.
- **One synthetic SQLite check (not legacy code or SQL).** To ground one INTERPRETATION about SQLite (section 4.2), the helper ran its own two-statement example against an in-memory database with the helper machine's Python `sqlite3` (SQLite 3.53.1): a `CREATE TABLE IF NOT EXISTS t1 (...);` with a trailing semicolon and an inner `--` comment, and an `ALTER TABLE ... RENAME`. Result: the text stored in `sqlite_master.sql` keeps the comment, drops `IF NOT EXISTS` and has no trailing semicolon; a renamed table's stored text quotes the name. The production SQLite version is UNKNOWN. (The helper did not record the exact statements and kept no script for this check; the checker and the corrector each re-created it, below.)
- **Checker's synthetic checks (second pass; as the checker's file states them).** Run with `python3 -I` from standard input, with the system temporary folder as working directory (no script file written), against `:memory:` on the same machine (Python 3.13.18, SQLite 3.53.1); synthetic table names `zz_alpha`, `zz_beta`, `zz_gamma`, `zz_tmp`/`zz_delta`; no legacy SQL or table definition. Cases: `CREATE TABLE IF NOT EXISTS` with an inner `--` comment, a CHECK and a trailing `;`; a `;` after a space; a `STRICT` table option before the `;`; a create plus `ALTER TABLE ... RENAME` inside `BEGIN IMMEDIATE` and `COMMIT`. Result: no trailing `;` stored in any case; `IF NOT EXISTS` dropped; inner comment kept; renamed name stored quoted. A second synthetic check (AUTOINCREMENT table with a trigger through create-new, copy, drop, rename in one transaction) left the trigger gone and `sqlite_sequence` lowered from 5 to the highest copied id, 3 (next id 4). The checker's other parsing (a text re-implementation of `_extract_block` and `_normalize_ddl`, a schema-history scan, an `ast` scan of openers) also ran from standard input in the system temporary folder; no legacy module was imported and no legacy script, SQL or shell file was run.
- **Corrector's synthetic test, recorded exactly (third pass).** Script `p03fix_synthetic.py`, kept in the work area's tools folder (outside the clone), run with `python3 -I` against `:memory:` (Python 3.13.18, SQLite 3.53.1). It uses only generic statements written for the test; no legacy SQL, table definition or module. The normaliser in it is written from the list of steps in S078 (strip `--` comments, drop `IF NOT EXISTS`, drop double quotes, collapse whitespace, remove spaces around `(`, `)` and `,`, upper-case), not imported or copied from the clone. Statements, in order:
  1. Source text, four lines, ends with `;`: line 1 `CREATE TABLE IF NOT EXISTS zz_t1 (`; line 2 `    id    INTEGER PRIMARY KEY,  -- inner comment`; line 3 `    name  TEXT NOT NULL`; line 4 `);`.
  2. `INSERT INTO zz_t1 (id, name) VALUES (1, 'x')`
  3. `BEGIN IMMEDIATE`; the same source text with the name `zz_t1_tmp`; `INSERT INTO zz_t1_tmp (id, name) SELECT id, name FROM zz_t1`; `DROP TABLE zz_t1`; `ALTER TABLE zz_t1_tmp RENAME TO zz_t1`; `COMMIT`.
  4. `CREATE TABLE zz_c_empty (id INTEGER PRIMARY KEY)`; `CREATE TABLE zz_c_rows (id INTEGER PRIMARY KEY)`; `INSERT INTO zz_c_rows (id) VALUES (1)`; for each: `CREATE TABLE <name>_new (id INTEGER PRIMARY KEY, extra TEXT NOT NULL)` then `INSERT INTO <name>_new (id) SELECT id FROM <name>`.
  5. After steps 1 and 3: `SELECT sql FROM sqlite_master WHERE type='table' AND name=?` for `zz_t1`.

  Result: after step 1 the stored text is `CREATE TABLE zz_t1 (` ... `)`: no trailing `;`, no `IF NOT EXISTS`, inner comment kept; normalised stored text is NOT equal to the normalised source text, and IS equal to it once the source's final `;` is removed. After step 3 the stored text begins `CREATE TABLE "zz_t1" (` (name quoted), again with no trailing `;`; same two comparison results. Step 4: the copy into the table with the new NOT NULL column succeeds when the old table is empty and fails (`NOT NULL constraint failed`) when it has one row. These results ground the INTERPRETATIONS in S131 and S134 on SQLite 3.53.1 only; the production SQLite version stays UNKNOWN (S206).
- **Corrector's reading.** Every checker finding was verified at the baseline: `core/schema.sql` L425 to L440, L543 to L550, L1610 (and a scan of non-CREATE statements); `core/state_store.py` L326 to L331, L420 to L447, L455 to L476; `core/migrations.py` L155 to L207, L270 to L275, L298 to L310; `main.py` L2095 to L2105, L2148 to L2153; `utils/holiday_guard.py` L85 to L110; `scripts/forward_shadow_record.py` L268 to L286; `scripts/reconstruct_excursions.py` L435, L497 to L538; `scripts/generate_screened_stocks_csv.py` (grep `StateStore`, L267 to L271); the 40 lines before each of the 26 `StateStore(` openers and a whole-file grep for a DB `exists()` check in the 16 openers without one; `git show` of commits `22ce538` and `e28800c` (schema diff only). Paths in this file that pointed into the work area or the clone are replaced by descriptions.
- **Security.** No credential file was opened; no value, address, personal name or machine home path is written here.
- **End check.** After writing this file: `rev-parse HEAD` = baseline and `git status --short` empty (confirmed).

## 1. How the schema is applied on open

### 1.1 The open sequence

| ID | Step | Code | Label |
|---|---|---|---|
| P03-S001 | `StateStore.__init__(db_path, schema_path=DEFAULT_SCHEMA_PATH, *, allow_migrate=False, market_open=False)` stores the two flags as booleans, creates the DB's parent directory, then calls `_initialize_schema()`. Migration therefore happens inside the constructor; there is no separate migrate call. | `core/state_store.py` L172 to L198 | FACT |
| P03-S002 | `DEFAULT_SCHEMA_PATH` is `core/schema.sql` beside the module. | `core/state_store.py` L104 | FACT |
| P03-S003 | `_initialize_schema` raises `StateStoreError` if the schema file does not exist, then reads it as UTF-8 text. | L363 to L369 | FACT |
| P03-S004 | It then calls `db_connect.init_analytics_schema(self._db_path)`, which opens a separate direct connection to `analytics.db` beside the main DB, sets WAL, `synchronous=FULL`, `busy_timeout=30000`, and runs `core/analytics_schema.sql` with `executescript`. This happens before any version check (pointer: part P07). | `core/state_store.py` L375; `core/db_connect.py` L67 to L90 | FACT |
| P03-S005 | It obtains the calling thread's connection (`_get_conn`), which on first use opens `sqlite3.connect(..., isolation_level=None, check_same_thread=True, timeout=30)`, applies five PRAGMAs (`journal_mode = WAL`, `synchronous = FULL`, `foreign_keys = ON`, `temp_store = MEMORY`, `busy_timeout = 30000`) and ATTACHes `analytics.db` as schema `analytics` (pointer: part P01). | `core/state_store.py` L377, L215 to L249, L107 to L113; `core/db_connect.py` L52 to L64 | FACT |
| P03-S006 | It reads the stored version BEFORE applying `schema.sql`: `old_version = self._read_existing_version(conn)`. | L379 to L383 | FACT |
| P03-S007 | Newer-DB gate: if `old_version is not None and old_version > EXPECTED_SCHEMA_VERSION`, it raises `SchemaVersionMismatch` before anything is written to the main DB's tables. This gate does not look at `allow_migrate` or `market_open`. | L398 to L405 | FACT |
| P03-S008 | Older-DB gate: if `old_version is not None and old_version < EXPECTED_SCHEMA_VERSION`, then unless `allow_migrate and not market_open`, `_refuse_migration(old_version, EXPECTED_SCHEMA_VERSION)` is called (it always raises). Otherwise `migrations.run_migrations(conn, schema_sql, old_version, EXPECTED_SCHEMA_VERSION, mig_log)` runs, then `migrations.relocate_analytics_tables(conn, ANALYTICS_TABLES, mig_log)`. The logger is `state_store.migrations`. | L420 to L440 | FACT |
| P03-S009 | `conn.executescript(schema_sql)` then runs unconditionally (new, current or just-migrated DB). | L446 | FACT |
| P03-S010 | Post-check: `get_schema_version()` is compared with `EXPECTED_SCHEMA_VERSION`; a difference raises `SchemaVersionMismatch` ("Run migrations or use a fresh database."). | L449 to L455 | FACT |

### 1.2 Where the version lives and how the target is set

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S011 | The version is a row in table `schema_meta` (`key TEXT PRIMARY KEY, value TEXT NOT NULL`), key `'schema_version'`, value stored as text. | `core/schema.sql` L29 to L32, L1610 | FACT |
| P03-S012 | `_read_existing_version` runs `SELECT value FROM schema_meta WHERE key = 'schema_version'` on the raw connection; it returns None when the query raises `sqlite3.OperationalError` (comment: table missing, fresh DB), when no row is found, or when `int(value)` fails (`TypeError` or `ValueError`). | `core/state_store.py` L457 to L474 | FACT |
| P03-S013 | `get_schema_version` runs the same query through `fetch_one`, raises `StateStoreError` if there is no row, and returns `int(row["value"])`. | L476 to L485 (`fetch_one` at L564) | FACT |
| P03-S014 | No code in the non-test tree uses `PRAGMA user_version` (grep for `user_version` in `*.py`: no match). | grep | FACT |
| P03-S015 | The target version is the module constant `EXPECTED_SCHEMA_VERSION = 45`. | `core/state_store.py` L102 | FACT |
| P03-S016 | The value written to the DB comes from a separate literal: the last executable statement of `schema.sql`, `INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '45')`. Only lines L1611 to L1654 (comments) follow it. It is the only `INSERT` in `schema.sql`. | `core/schema.sql` L1610 to L1654; grep `^INSERT` | FACT |
| P03-S017 | The two literals (L102 constant and L1610 string) agree at the baseline (45). Their agreement is checked only after the stamp is written (S010). | as cited | FACT |
| P03-S018 | `core/analytics_schema.sql` contains no version row or version marker (grep for `version` and `schema_meta`: no match). Analytics schema changes are not versioned (pointer: part P07). | grep | FACT |

### 1.3 Outcome by database state

| ID | DB state at open | What the code does | Code | Label |
|---|---|---|---|---|
| P03-S019 | New: file absent or empty (no tables; `old_version` None) | No gate applies; no migration; `executescript` creates every missing table, index and the trigger and stamps 45; post-check passes. This happens for every opener, whatever its flags and whatever the time (the gates at L398 and L420 both require `old_version is not None`). | L398, L420, L446 to L455 | FACT |
| P03-S221 | Existing DB whose `schema_meta` table or version row is missing, or whose value is not an integer (`old_version` None, L463 to L474) | No gate and no migration; `executescript` runs against the existing tables: `CREATE ... IF NOT EXISTS` leaves them as they are, and the `DROP ... IF EXISTS` statements at `core/schema.sql` L436 to L438 run (S222). INTERPRETATION: any statement that needs a newer column (for example `CREATE INDEX IF NOT EXISTS idx_fm_ledger_date ON fm_ledger(date)`, `core/schema.sql` L547 to L548, on an `fm_ledger` from before v27, when the `date` column was added in commit `22ce538`) raises `sqlite3.OperationalError` out of the constructor before the stamp; the post-check is reached only if every statement succeeds. | `core/state_store.py` L463 to L474, L398, L420, L446 to L455; `core/schema.sql` L436 to L438, L547 to L548 | FACT; INTERPRETATION |
| P03-S020 | Current (45) | No gate; no migration; `executescript` runs: `CREATE ... IF NOT EXISTS` statements are no-ops on existing objects, the trigger is re-created only if missing, the three `DROP ... IF EXISTS` statements at `core/schema.sql` L436 to L438 (`capital_ledger` and two indexes) run again (no-ops once those objects are absent), and the `INSERT OR REPLACE` re-stamps 45. Every opener does this on every open. | L446; `core/schema.sql` L291, L436 to L438, L1610 | FACT (INTERPRETATION for the no-op semantics) |
| P03-S021 | Older (below 45), opener NOT allowed (`allow_migrate` False, or `market_open` True) | `_refuse_migration` logs CRITICAL `MIGRATION_REFUSED ...`, tries to write a CRITICAL sentinel, then raises `MigrationNotPermitted`. `run_migrations`, the relocation and `executescript` are not reached, so the main DB's tables and stored version are not changed by this path. | L426 to L427, L326 to L355 | FACT |
| P03-S022 | Older (below 45), opener allowed (`allow_migrate` True and `market_open` False) | `run_migrations` rebuilds tables (section 3), `relocate_analytics_tables` moves analytics tables still in main, `executescript` creates new tables and stamps 45, post-check. | L428 to L455 | FACT |
| P03-S023 | Newer (above 45) | `SchemaVersionMismatch` raised before `executescript`; the stored version is left as it was. Any opener. | L398 to L405 | FACT |

### 1.4 What happens before the version gates

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S024 | Before either gate, `init_analytics_schema` has already created or updated `analytics.db` (S004) and the main connection has applied its PRAGMAs and ATTACH (S005). So a refused or newer-DB open still runs those steps. | `core/state_store.py` L375, L377, L398, L426 | FACT |
| P03-S025 | INTERPRETATION (SQLite semantics): `PRAGMA journal_mode = WAL` is persistent in the file; on a main DB already in WAL mode it changes nothing; ATTACH creates `analytics.db` if absent. | `core/state_store.py` L108; `core/db_connect.py` L55 | INTERPRETATION |

## 2. Entry points, invocation timing, callers and guards

### 2.1 Entry points

| ID | Entry point | When it runs | Callers (non-test) | Label |
|---|---|---|---|---|
| P03-S026 | `StateStore.__init__` → `_initialize_schema` | Every construction of a `StateStore` (on open) | 26 constructions, section 2.4 | FACT |
| P03-S027 | `migrations.run_migrations(conn, schema_text, from_version, target_version, log)` | Only from `_initialize_schema` L429, inside the older-DB branch | `core/state_store.py` L429 only (grep `run_migrations`) | FACT |
| P03-S028 | `migrations.relocate_analytics_tables(conn, tables, log)` | Only from `_initialize_schema` L440, inside the same branch, after `run_migrations`, on every migration run whatever `from_version` is | `core/state_store.py` L440 only | FACT |
| P03-S029 | `StateStore.migrate_to_latest()` | A stub: returns if the stored version equals 45, otherwise raises `SchemaVersionMismatch("No migration path ...")`; it runs no migration. | No non-test caller (grep `migrate_to_latest`: only the definition) | FACT |
| P03-S030 | No other entry point | No CLI, script or cron entry runs migrations directly | None; `MIGRATION_TABLES` is referenced only in `core/migrations.py` and in comments (`core/state_store.py` L102, `core/schema.sql`, legacy docs) (grep) | FACT |

### 2.2 The guard and who sets it

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S031 | Both flags default to False; a caller that passes nothing can never migrate an existing older DB. | `core/state_store.py` L177 to L178, L426 | FACT |
| P03-S032 | The only non-test caller that passes either flag is `main.py` `_main_locked`: `StateStore(Path("data_store/trading_system.db"), allow_migrate=True, market_open=_market_open_now)`. The path is a fixed relative literal; there is no paper or live split at this call. | `main.py` L2233 to L2237; grep `allow_migrate` | FACT |
| P03-S033 | `_market_open_now` = `(_now_boot.weekday() < 5) and (_mo_boot <= _now_boot.time() <= _mc_boot)`, where `_now_boot` is `core.time_authority.now_ist()` and `_mo_boot`, `_mc_boot` are parsed from `app_config.system.trading_hours.market_open` and `.market_close` ("HH:MM"). No holiday or special-session test is part of this formula. | `main.py` L2226 to L2232 | FACT |
| P03-S034 | The configured values at the baseline are `market_open: "09:15"` and `market_close: "15:30"`; the loader's defaults are the same (pointer: A02). | `config/system_config.yaml` L103 to L104; `core/config_loader.py` L92 to L93 | FACT |
| P03-S035 | INTERPRETATION (Python `datetime.time` comparison): the closed interval includes exactly 15:30:00.000000; any later instant in the 15:30 minute counts as closed. | `main.py` L2232 | INTERPRETATION |
| P03-S036 | Before the store open, `main()` returns 0 on a non-trading day (holiday guard; a missing holiday file is passed over), and returns 0 outside the service START window [08:00, 18:15) unless `--status`, `--dry-run`, `--interactive`, `--resume` or `TS_IGNORE_MARKET_WINDOW=1` bypasses that window. Config load failure returns 5 before the store open. | `main.py` L2098 to L2152, L2154 to L2176, L2000 to L2016; `core/config_loader.py` L83; `main.py` L2197 to L2201 | FACT |
| P03-S037 | INTERPRETATION (from S033 to S036): without a bypass flag, the boot path can migrate only on a day the holiday guard lets through: a trading day, or any day on which the holiday-file lookup raises `FileNotFoundError` (`main.py` L2101 to L2103, L2151 to L2152; on a weekday via `utils/holiday_guard.py` L94, on a weekend via `next_trading_day` L105 to L108, where `_market_open_now` is False all day); on such a day, in [08:00, 09:15) or (15:30, 18:15) IST; inside [09:15, 15:30] on a weekday it refuses. | as cited; `main.py` L2101 to L2103, L2151 to L2152; `utils/holiday_guard.py` L92 to L94, L105 to L108 | INTERPRETATION |
| P03-S038 | `main.py` writes the single-instance lock and sets up logging before the store open, so `_refuse_migration`'s CRITICAL log goes through the configured logging (pointer: A01, A15). | `main.py` L2178 to L2190 | FACT |

### 2.3 Diagnostic opens (A01 C5)

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S039 | `--status` and `--dry-run` reach the same `StateStore(..., allow_migrate=True, market_open=...)` call before they are handled; `--status` is handled at L2299 to L2302 and `--dry-run` at L2476 to L2482. Off-market, with a pending migration, these diagnostic runs therefore migrate the DB; in market hours they refuse with `MigrationNotPermitted`. | `main.py` L2157 to L2160, L2233 to L2237, L2299, L2476 | FACT (from code path) |

### 2.4 Every non-test `StateStore` opener

All pass no `allow_migrate` and no `market_open` (default False) except `main.py`. "No local handler" means no `try` with an `except` encloses the call in its function (AST scan, section 0). For every row: a new or current DB is applied as in S019 and S020; an older DB raises `MigrationNotPermitted` (S021); a newer DB raises `SchemaVersionMismatch` (S023). The column "on refusal" gives what the code then does with that exception.

| ID | Opener (path, line, function) | Arguments | On refusal or other open error | Owner |
|---|---|---|---|---|
| P03-S040 | `main.py` L2233, `_main_locked` | fixed path, `allow_migrate=True`, `market_open=_market_open_now` | No local handler; `main()` has only `try/finally` (L2187 to L2190); reaches the `__main__` guard (section 5.2) | A01 |
| P03-S041 | `reports/daily_report.py` L1893, `main` | `db_path` (only if the file exists, L1888 to L1890) | No local handler; `__main__` is `sys.exit(main())` (L1945 to L1946) | A15 |
| P03-S042 | `reports/daily_trade_review.py` L2905, `main` | `db_path` (only if the file exists, L2902 to L2904) | No local handler; `raise SystemExit(main())` (L2923 to L2924) | A15 |
| P03-S043 | `scripts/backfill_closure_source_w8.py` L191, `main` | `db_path=str(DB_PATH)` | No local handler (L319 to L320) | A12 |
| P03-S044 | `scripts/check_cron_drift.py` L191, `main` | `args.db_path` (only if the file exists, L182 to L184) | No local handler; `_cron_main` returns `main()` (L226 to L240) | A16 |
| P03-S045 | `scripts/clear_kill_switch.py` L55, `main` | `args.db` (only if the file exists, L51 to L53) | No local handler (L85 to L86) | A13 |
| P03-S046 | `scripts/compute_strategy_metrics.py` L310, `main` | `db_path=db_path` | `except Exception` L311: logs error, `return 1` (L312 to L313) | A07 |
| P03-S047 | `scripts/cron_officer.py` L905, `main` | `args.db_path` (only if the file exists, L904) | No local handler (L951 to L952) | A16 |
| P03-S048 | `scripts/cron_watchdog.py` L46, `main` | `db` (only if the file exists, L43 to L45) | No local handler (L76 to L77) | A16 |
| P03-S049 | `scripts/db_retention.py` L203, `main` | `db_path=db_path` | `except Exception` L204: logs error, `return 1` | A03 (part P09b) |
| P03-S050 | `scripts/eod_broker_reconcile.py` L358, `main` | `db_path=db_path` | `except Exception` L359: logs error, `return 1` | A12 |
| P03-S051 | `scripts/eod_cleanup.py` L280, `main` | `db_path=db_path` | `except Exception` L281: logs error, `return 1` | A12 |
| P03-S052 | `scripts/eod_verify.py` L199, `main` | `db_path=db_path` | `except Exception` L200: logs error, `return 1` | A12 |
| P03-S053 | `scripts/fetch_fno_ban.py` L306, `main` | `db_path=db_path` | `except Exception` L307: logs error, `return 1` | A05 |
| P03-S054 | `scripts/forward_shadow_record.py` L150, `main` | `db_path` | `except Exception` L270: logs `forward_shadow.crash` (L272), attempts a CRITICAL sentinel (L273 to L281), returns 1 (L282); `finally` closes the store only if it was constructed (L283 to L285) | A18 |
| P03-S055 | `scripts/premarket_healthcheck.py` L92, `check_database` | `db_path` (only if the file exists, L86 to L87) | `except Exception` L100: returns `(False, "Database error: ...")` | A20 |
| P03-S056 | `scripts/reconcile_pnl.py` L337, `main` | `db_path=db_path` | `except Exception` L338: logs error, `return 1` | A12 |
| P03-S057 | `scripts/reconcile_positions.py` L376, `main` | `db_path=db_path` | `except Exception` L377: logs error, `return 1` | A12 |
| P03-S058 | `scripts/reconstruct_excursions.py` L459, `main` | `DB_PATH` | `except Exception` L499: status FAILED, logs `reconstruct.crash`, attempts a CRITICAL sentinel (L503 to L511); `finally` releases the lock (L512 to L513); then heartbeat (L515) and `main` returns 1 (L517); `__main__` is `sys.exit(_cron_main())` (L537 to L538) | A15 |
| P03-S059 | `scripts/replay_signals.py` L185, `run_replay` | `Path(db_path)` | No handler in `run_replay` or in `main` (L223 to L234); `main()` called bare (L242 to L243) | A19 |
| P03-S060 | `scripts/sr_detector_backfill.py` L115, `main` | `Path(args.db)` | No local handler; `_cron_main` returns `main(argv)` (L131 to L145) | A08 |
| P03-S061 | `scripts/system_manager.py` L1324, `main` | `args.db_path` (only if the file exists, L1312 to L1314) | No local handler (L1354 to L1355) | A15 |
| P03-S062 | `scripts/t2_cnc_gtt_realtest.py` L221, `_open_throwaway_store` | `db_path` (its comment and docstring: a fresh throwaway file, so the new-DB route of S019 applies; HISTORICAL for intent) | No local handler | A19 |
| P03-S063 | `scripts/trade_journal.py` L157, `main` | `Path(args.db)` | No local handler; `_cron_main` wraps `main` in `HeartbeatTimer`, whose `__exit__` records FAILED and returns False (does not suppress) | A15 (timer: A16) |
| P03-S064 | `scripts/wal_checkpoint.py` L32, `main` | `db_path` (only if the file exists, L27 to L29) | `except Exception` L45: prints `WAL checkpoint FAILED`, `sys.exit(1)` | A03 (part P09b) |
| P03-S065 | `utils/cron_heartbeat.py` L84, `record_heartbeat` | `db_path` (only if the file exists, L81 to L82) | `except Exception` L94: `return False` (docstring: "never raises") | A16 |

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S066 | Count: 26 non-test `StateStore(...)` constructions in 26 files (1 in `main.py`, 2 in `reports/`, 22 in `scripts/`, 1 in `utils/`). `scripts/generate_screened_stocks_csv.py` mentions `StateStore` in its docstring (L8, L26) and in a code comment (L267), and constructs none (it reads through `db_connect.connect_readonly`, L270). | grep `StateStore(`; `scripts/generate_screened_stocks_csv.py` L8, L26, L267, L270 | FACT |
| P03-S067 | INTERPRETATION (Python semantics): for a row with no handler, the exception propagates out of the script and the interpreter ends with exit status 1 after printing the traceback. | rows S041 to S045, S047, S048, S059 to S063 | INTERPRETATION |
| P03-S068 | `HeartbeatTimer.__exit__` calls `record_heartbeat` (L147), which itself constructs a `StateStore` (S065); with a pending migration that inner open also goes through `_refuse_migration` (CRITICAL log, sentinel attempt) and is then swallowed (`return False`). | `utils/cron_heartbeat.py` L140 to L173, L80 to L95 | FACT (from code path) |

### 2.5 Version readers that never migrate

| ID | Reader | How | Owner | Label |
|---|---|---|---|---|
| P03-S069 | `scripts/preflight/checks/database.py` `_read_schema_version` and `DbSchemaVersionCheck` | Raw `sqlite3.connect(str(db_path))`, same `SELECT`; DB = code → PASS, DB < code → WARN "migration pending: app will migrate ... at startup", DB > code → FAILED; no `StateStore` | A20 | FACT (L23 to L32, L55 to L95) |
| P03-S070 | `scripts/deploy_assert.py` | Read-only URI connection; check `db.schema_version` is a BLOCKER when `ver != EXPECTED_SCHEMA_VERSION` | A17 | FACT (L11, L28, L37 to L39, L60 to L64) |
| P03-S071 | `scripts/backup_restore_drill.py` `check_schema_version` | Raw `sqlite3.connect` on the restored copy; compares with `EXPECTED_SCHEMA_VERSION` | A03 (part P09a) | FACT (L40, L122 to L131) |
| P03-S072 | `ops_dashboard/backend/readers/db_reader.py` `get_schema_version` | Read-only helper `_ro(cfg)`; returns the int or None | A15 | FACT (L113 to L119) |
| P03-S073 | `core/db_connect.connect` and `connect_readonly` | Open raw connections (the second with `mode=ro` and `query_only = ON`); neither applies `schema.sql` or reads the version | A03 (part P01) | FACT (`core/db_connect.py` L93 to L137) |

### 2.6 Other DDL applied outside `schema.sql` and the migration runner

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S074 | `ops/control_tower/db.py` `ensure_indexes` runs `CREATE INDEX IF NOT EXISTS idx_ct_findings_last_seen ON control_tower_findings(last_seen)`; the same index is also declared in `schema.sql`. Called from `ops/control_tower/aggregator.py` L199 (pointer: parts P06a/P06b; owner A15). | `ops/control_tower/db.py` L16 to L24; `core/schema.sql` L1414 | FACT |
| P03-S075 | No `ALTER TABLE` statement exists in non-test code other than the rename inside the rebuild (grep `ALTER TABLE` in `*.py` and `*.sql`). | `core/migrations.py` L310 | FACT |

## 3. The migration steps

### 3.1 The rebuild mechanism (`_rebuild_table_from_schema`, L254 to L331)

| ID | Step | Code | Label |
|---|---|---|---|
| P03-S076 | Target DDL = the table's single `CREATE TABLE` block extracted from the schema text (`extract_create_table`: zero blocks or more than one raise `MigrationError`). | L267, L170 to L180 | FACT |
| P03-S077 | Live DDL = `sqlite_master.sql` for the table; if absent (table does not exist yet), return False (no-op; `executescript` will create it). | L268 to L272, L210 to L214 | FACT |
| P03-S078 | If `_normalize_ddl(live) == _normalize_ddl(target)` return False ("idempotent skip"). `_normalize_ddl` strips `--` comments, drops `IF NOT EXISTS`, removes double quotes, collapses whitespace, removes spaces around `(`, `)` and `,`, upper-cases. | L273 to L274, L194 to L207 | FACT |
| P03-S079 | The temp table name is `<table>__mig_new`; the target DDL is rewritten with that name (regex, first match); `MigrationError` if the rename did not happen. | L276 to L285 | FACT |
| P03-S080 | Old column set = non-generated columns of the live table (`PRAGMA table_xinfo`, `hidden` 2 or 3 excluded). The table's indexes are extracted from the schema text (`CREATE [UNIQUE] INDEX ... ON <table>`). | L288, L290, L217 to L227, L183 to L191 | FACT |
| P03-S081 | If `PRAGMA foreign_keys` is on, it is set OFF before the transaction (comment: a no-op inside a transaction). | L292 to L297 | FACT |
| P03-S082 | Inside `BEGIN IMMEDIATE`: `DROP TABLE IF EXISTS <tmp>`; create tmp from the target DDL; new non-generated columns read from tmp; copy list = new columns that also exist in the old table, in the new order; `INSERT INTO <tmp> (cols) SELECT cols FROM <table>`; `DROP TABLE <table>`; `ALTER TABLE <tmp> RENAME TO <table>`; re-create each extracted index; `PRAGMA foreign_key_check` (no table argument); any row returned raises `MigrationError`; `COMMIT`. | L298 to L319 | FACT |
| P03-S083 | On any exception: `ROLLBACK` (an `sqlite3.Error` from the rollback itself is ignored) and re-raise. `finally`: `PRAGMA foreign_keys = ON` if it was on. Success logs `migration: rebuilt table %s to match schema.sql` and returns True. | L320 to L331 | FACT |
| P03-S084 | The rebuild re-creates indexes only; it does not re-create triggers. The one trigger in `schema.sql`, `trg_trades_terminal_status_guard` (`BEFORE UPDATE OF status ON trades`), is created only by `executescript` (L446) from `CREATE TRIGGER IF NOT EXISTS`. There are no views in `schema.sql`. | `core/migrations.py` L311 to L312; `core/schema.sql` L291 to L300; tool scan | FACT |
| P03-S085 | INTERPRETATION (SQLite semantics): `DROP TABLE trades` also drops that trigger and the table's indexes; so after a `trades` rebuild commits and until `executescript` runs, `trades` has its indexes but no trigger. | as cited | INTERPRETATION |
| P03-S086 | `run_migrations(conn, schema_text, from_version, target_version, log)`: returns 0 if `from_version >= target_version`; otherwise loops `version` from `from_version + 1` to `target_version`, and for each table in `MIGRATION_TABLES.get(version, [])` not already seen: skips it (debug log) if `_table_in_schema` is False, else calls `_rebuild_table_from_schema`; any exception is re-raised as `MigrationError("migration v<from>->v<target> failed rebuilding '<table>': ...")` chained to the cause. Ends with an info log and returns the count rebuilt. | L400 to L444 | FACT |
| P03-S087 | Each table is rebuilt at most once per run (the `seen` set), always to the CURRENT `schema.sql` definition; intermediate versions are never applied one by one. | L420 to L425, L267 | FACT |
| P03-S088 | `_table_in_schema` returns False whenever `extract_create_table` raises `MigrationError`, which covers both "no block" and "more than one block". | L241 to L247, L176 to L179 | FACT |

### 3.2 `MIGRATION_TABLES` at the baseline (rebuild steps)

| ID | Version | Tables rebuilt | Stated purpose (comment or docstring; HISTORICAL) | Code |
|---|---|---|---|---|
| P03-S089 | 25 | signals, trades, orders, kill_switch_state | O2 status and enum CHECK constraints | L116; docstring L37 to L38 |
| P03-S090 | 26 | screener_results, smart_tgt_state, shadow_trades, reconciliation_log, innings | O1 uniform FOREIGN KEY declarations | L117 to L118; L39 to L41 |
| P03-S091 | 27 | fm_ledger, webhook_audit | O4 STORED `date` generated column and index (candles and system_metrics also changed at v27 but are relocated at v28, comment L119 to L122) | L123; L42 to L43 |
| P03-S092 | 29 | trades | FIX-179: widen `trades.status` CHECK to allow `EXITING` | L124; L47 to L48 |
| P03-S093 | 30 | trades | TGT retry: three new columns | L125; L49 to L51 |
| P03-S094 | 32 | trades, order_execution_log | Phase 3a: `tolerance_fraction_used`, `tolerance_source` | L126; L57 to L60 |
| P03-S095 | 34 | trades | Diary #4: ten sizing-audit columns | L128; L64 to L69 |
| P03-S096 | 35 | trades | Slice 1: three columns | L129; L70 to L74 |
| P03-S097 | 38 | signals | SNR-V2: widen `signals.status` CHECK to allow GLOB `RETEST_*` | L132; L81 to L83 |
| P03-S098 | 45 | trades | W8: `closure_source`, `exit_mechanism` | L130; L91 to L102 |

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S099 | Versions 28, 31, 33, 36, 37, 39, 40, 41, 42, 43 and 44 have no `MIGRATION_TABLES` entry. 28 is the relocation (S103); the others are described as pure additions created by `executescript` (v38 also adds `retest_state`). Versions 1 to 24 have no entry. | L115 to L133; docstring L44 to L46, L52 to L56, L61 to L63, L75 to L90 | FACT (entries); HISTORICAL (descriptions) |
| P03-S100 | All twelve tables named in `MIGRATION_TABLES` have exactly one `CREATE TABLE` block in the baseline `schema.sql`, and for each the legacy scanner (`_extract_block`, which does not skip comments) returns the same block as a comment-aware scanner; each block ends with `;`. Explicit indexes re-created per rebuild: signals 4, trades 4, orders 4, kill_switch_state 0, screener_results 3, smart_tgt_state 0, shadow_trades 2, reconciliation_log 2, innings 2, fm_ledger 4, webhook_audit 3, order_execution_log 3. | tool `p03_schema_history.py` on `core/schema.sql` at the baseline | FACT (text parsing) |
| P03-S101 | Tables whose `CREATE TABLE` contains `REFERENCES` to a rebuilt parent: to `signals`: gate_state, retest_state, screener_results, shadow_trades, sr_detector_results, trades; to `trades`: gtt_state, innings, orders, reconciliation_log, shadow_trades, signals, smart_tgt_state, trade_excursions, trade_journal. No table references any other rebuilt table. | tool scan of the baseline text | FACT (text parsing) |
| P03-S102 | Six rebuilt tables declare `AUTOINCREMENT` columns: fm_ledger (L519), webhook_audit (L582), reconciliation_log (L650), screener_results (L682), innings (L744), order_execution_log (L1051). | `core/schema.sql` as cited | FACT |

### 3.3 The v28 relocation (`relocate_analytics_tables`, L338 to L393)

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S103 | For each table in `ANALYTICS_TABLES` = (`candles`, `system_metrics`, `system_metrics_daily`): skip if not present in main's `sqlite_master`; else copy list = main's non-generated columns that also exist in `analytics.<t>` (`MigrationError` if none); inside `BEGIN IMMEDIATE`: `DELETE FROM analytics.<t>`, `INSERT INTO analytics.<t> (...) SELECT ... FROM main.<t>`, `DROP TABLE main.<t>`, `COMMIT`; on exception `ROLLBACK` and re-raise. Logs `migration: relocated table %s -> analytics.db`; returns the count. | `core/migrations.py` L338 to L393; `core/db_connect.py` L26 to L30 | FACT |
| P03-S104 | Preconditions, met by the call order in `_initialize_schema`: the analytics tables exist (`init_analytics_schema`, L375) and `analytics` is ATTACHed on the connection (`_open_connection`, L247). | `core/state_store.py` L375, L247; docstring `core/migrations.py` L348 to L351 | FACT |
| P03-S105 | None of the three tables is defined in the baseline `schema.sql` (they were removed at v28, commit `f172171`, 2026-06-14). | tool | FACT (text parsing) |
| P03-S106 | Exceptions from `relocate_analytics_tables` are not wrapped: a `sqlite3.Error` reaches the caller as itself; `MigrationError` only for the "no common columns" case. | L370 to L390; `core/state_store.py` L440 | FACT |

### 3.4 Dependencies and ordering

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S107 | Order within one run: versions ascending, tables in list order, each once (S087); then the relocation; then `executescript`. For a DB at v24, the first step rebuilds signals, trades, orders, kill_switch_state (all to the v45 definition), then the v26 and v27 tables; trades and signals are not rebuilt again at 29 to 45. | L421 to L425; `core/state_store.py` L429 to L446 | FACT (from code path) |
| P03-S108 | `order_execution_log` (v32 entry) is created by the v31 pure addition. For a DB below v31 the table is absent at rebuild time, so `_rebuild_table_from_schema` returns False (L269 to L272) and `executescript` later creates it with the current definition. | as cited | FACT (from code path) |
| P03-S109 | Rebuilds of parents (signals, trades) run with `foreign_keys` OFF; the children keep their `REFERENCES signals` or `REFERENCES trades` clauses by name. INTERPRETATION (SQLite 12-step procedure): after the rename, those clauses resolve to the new table. | L292 to L297, L310 | FACT; INTERPRETATION |
| P03-S110 | The FK check after each rebuild (L314) is not limited to the rebuilt table. INTERPRETATION (SQLite documentation): without a table argument the pragma checks every table; any FK violation already present anywhere would therefore fail the rebuild. | L314 to L318 | FACT; INTERPRETATION |

### 3.5 Schema history cross-check (text parsing of every commit that changed `core/schema.sql`)

The tool reports, for each commit, tables whose comment-stripped, normalised `CREATE TABLE` text changed. The first commit (`bcf03b5`, 2026-04-17) is already at v9 with 16 tables.

| ID | Version change (commit, date) | Existing tables whose definition changed | Corresponding `MIGRATION_TABLES` entry | Label |
|---|---|---|---|---|
| P03-S111 | v9→v10 (`e28800c`, 2026-04-19); v10→v11 (`0d80fe9`); v12→v13 (`1a2bca1`); v13→v14 (`dfdeec2`); v15→v16 (`5a52b74`); v16→v17 (`0cc0009`) | fm_ledger (and `capital_ledger` removed; dropped from an existing DB by `DROP TABLE IF EXISTS capital_ledger` and two `DROP INDEX IF EXISTS`, `core/schema.sql` L436 to L438, at every `executescript`, S222); eod_squareoff_log, trades; session; orders, screener_results, signals, trades; orders; trades | None at these versions (the map starts at 25). fm_ledger, trades, orders, screener_results and signals are listed at later versions; `session` and `eod_squareoff_log` are never listed. | FACT (text parsing) |
| P03-S112 | v13→v13, no bump (`d81fd01`, 2026-05-16) | fm_ledger | fm_ledger listed at 27 | FACT (text parsing) |
| P03-S113 | v24→v25 (`4f6c3c5`, 2026-06-14) | kill_switch_state, orders, signals, trades | 25: same four | FACT (text parsing) |
| P03-S114 | v25→v26 (`c29e969`) | innings, reconciliation_log, screener_results, shadow_trades, smart_tgt_state | 26: same five | FACT (text parsing) |
| P03-S115 | v26→v27 (`22ce538`) | candles, fm_ledger, system_metrics, webhook_audit | 27: fm_ledger, webhook_audit (the other two relocated at v28) | FACT (text parsing) |
| P03-S116 | v27→v28 (`f172171`) | removed: candles, system_metrics, system_metrics_daily | relocation (S103) | FACT (text parsing) |
| P03-S117 | v28→v29, v29→v30, v33→v34, v34→v35, v44→v45 | trades | 29, 30, 34, 35, 45: trades | FACT (text parsing) |
| P03-S118 | v31→v32 (`2ce54ab`) | order_execution_log, trades | 32: same two | FACT (text parsing) |
| P03-S119 | v37→v38 (`9f56b07`) | signals (and retest_state added) | 38: signals | FACT (text parsing) |
| P03-S120 | v40→v40, no bump (`3413f27`, 2026-06-29) | control_tower_findings | None; the table is never listed. Its commit message says the columns were "added to the not-yet-live v40 table; no version bump" (HISTORICAL). | FACT (text parsing); HISTORICAL |
| P03-S121 | Every other version step from v11 to v44 | None (only tables added) | From v25 onward every changed existing table has an entry at the version where it changed (or is relocated), except S120 (tool output) | FACT (text parsing) |

### 3.6 Removal step inside `schema.sql` (outside `MIGRATION_TABLES`)

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S222 | `core/schema.sql` L436 to L438 hold `DROP TABLE IF EXISTS capital_ledger;`, `DROP INDEX IF EXISTS idx_ledger_trade_id;` and `DROP INDEX IF EXISTS idx_ledger_timestamp;`. These are the only executable statements in `schema.sql` besides the CREATE statements and the version INSERT (L1610). They run inside `executescript` (`core/state_store.py` L446) on every open that passes both version gates, by any opener, whatever its flags and the time. The v10 removal of `capital_ledger` (commit `e28800c`) therefore reaches an existing DB through `schema.sql`, not through `MIGRATION_TABLES` or `run_migrations`. HISTORICAL: L430 to L434, "No CREATE statement here on purpose. Drop handled below for upgrade path." | `core/schema.sql` L429 to L438, L1610; `core/state_store.py` L446 | FACT; HISTORICAL (comment) |

## 4. Atomicity, idempotency, failure and restart

### 4.1 Transaction boundaries

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S122 | Per table rebuild: one `BEGIN IMMEDIATE ... COMMIT` holding the temp create, copy, drop, rename, index re-creation and FK check. | `core/migrations.py` L299 to L319 | FACT |
| P03-S123 | INTERPRETATION (SQLite semantics): DDL is transactional in SQLite, so a `ROLLBACK` after a failure inside that block leaves the original table, its data and its indexes as they were; a process death inside the block is rolled back from the WAL at the next open. | L320 to L325; `core/state_store.py` L108 to L109 | INTERPRETATION |
| P03-S124 | Whole run: there is no enclosing transaction; each table's rebuild is committed on its own, and the relocation commits table by table. | L421 to L439, L376 to L390 | FACT |
| P03-S125 | INTERPRETATION (SQLite documentation on ATTACHed databases in WAL mode): the relocation transaction spans two files (main and analytics, both WAL, `core/db_connect.py` L38 to L41, L85); such a commit is atomic per file but not across the two files as a set. Which file commits first, and what a power loss at that moment leaves, is not established. | L376 to L384 | INTERPRETATION; UNKNOWN |
| P03-S126 | `executescript` runs after the migration with no `BEGIN` in `schema.sql` (the only `BEGIN` is inside the trigger body, L296). INTERPRETATION (Python `sqlite3` with `isolation_level=None`): each statement commits on its own; a failure part-way leaves earlier statements applied. | `core/state_store.py` L446, L234; `core/schema.sql` L296 | FACT; INTERPRETATION |
| P03-S127 | The version is recorded only by the last statement of `executescript` (S016). | `core/schema.sql` L1610 | FACT |

### 4.2 Idempotency

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S128 | The relocation is re-runnable: a table already absent from main is skipped, and the target is emptied before the copy inside the same transaction. | L359 to L363, L378 | FACT |
| P03-S129 | `executescript` is re-runnable: every `CREATE` carries `IF NOT EXISTS`, the three `DROP` statements (`core/schema.sql` L436 to L438) carry `IF EXISTS`, and the version is written by `INSERT OR REPLACE` (L1610). | `core/state_store.py` L442 to L446; `core/schema.sql` L436 to L438, L1610 | FACT; INTERPRETATION (SQL semantics) |
| P03-S130 | The rebuild's skip compares normalised live DDL with normalised target DDL. The target comes from `extract_create_table`, whose block includes the terminating `;` (`schema_text[i : j + 1]` with `j` at the `;`, then `.strip()`), and `_normalize_ddl` does not remove `;`. | L166, L180, L194 to L207, L273 | FACT |
| P03-S131 | INTERPRETATION (SQLite stores CREATE text without the trailing semicolon; shown by the helper's, the checker's and the corrector's synthetic checks on SQLite 3.53.1, section 0; the corrector's test also shows that the normalised texts become equal once the target's final `;` is removed): the normalised live text never ends with `;` while the normalised target always does, so the equality at L273 is never true for an existing table and every listed table in range is rebuilt on every migration run, even if its definition already matches. Whether this holds on the production SQLite version is UNKNOWN. | L273 | INTERPRETATION |
| P03-S132 | INTERPRETATION: a repeated rebuild re-copies the intersecting columns, so for a table whose definition already matches it rewrites the same rows; generated columns are recomputed (excluded from the copy, L224 to L225, L302 to L303). | L302 to L308 | INTERPRETATION |
| P03-S133 | INTERPRETATION (SQLite semantics): for the six AUTOINCREMENT tables (S102), dropping the old table removes its `sqlite_sequence` row; after the copy the counter restarts from the highest copied id, so ids of rows deleted earlier above that value could be issued again. | as cited | INTERPRETATION |
| P03-S134 | INTERPRETATION: only columns present in both definitions are copied (L304). A column in the old table but not in the new definition is not copied; a renamed column is treated as dropped plus added; a new `NOT NULL` column without a default makes the `INSERT` fail when the old table has at least one row (shown on SQLite 3.53.1 by the corrector's synthetic test, section 0), and old data violating a new CHECK or NOT NULL also makes it fail; either failure rolls back the table's rebuild. | L302 to L308 | INTERPRETATION |

### 4.3 Failure part-way

| ID | Route | What the code leaves | Code | Label |
|---|---|---|---|---|
| P03-S135 | Rebuild of table k fails (constraint, lock timeout after 30 s, FK check, any error) | Table k rolled back; tables rebuilt before k in the same run stay committed in their new form; no relocation, no `executescript`; stored version unchanged (old value); `MigrationError` raised out of the constructor. | L319 to L325, L421 to L439; `core/state_store.py` L429 to L446 | FACT (code path); INTERPRETATION (rollback semantics) |
| P03-S136 | `BEGIN IMMEDIATE` itself fails (busy beyond `busy_timeout`) | The `ROLLBACK` attempt raises and is ignored; the original error is re-raised and wrapped as `MigrationError`. | L299, L320 to L325, L435 to L439 | FACT |
| P03-S137 | Relocation of table t fails | Table t's transaction rolled back; tables relocated before it stay relocated; no `executescript`; version unchanged; the raw exception (usually `sqlite3.Error`) leaves the constructor. | L376 to L390; `core/state_store.py` L440 | FACT |
| P03-S138 | `executescript` fails after a successful migration | Rebuilds and relocation committed; statements before the failing one applied; version unchanged (stamp is last); raw `sqlite3.Error` leaves the constructor. | `core/state_store.py` L446; `core/schema.sql` L1610 | FACT; INTERPRETATION (S126) |
| P03-S139 | Post-check mismatch after `executescript` | The new stamp is already written; `SchemaVersionMismatch` raised. INTERPRETATION: if L102 and L1610 ever differed, the DB would keep the L1610 value. | `core/state_store.py` L449 to L455 | FACT; INTERPRETATION |
| P03-S140 | Process killed (signal, power loss) mid-rebuild | INTERPRETATION: the open transaction is rolled back at the next open (WAL, `synchronous = FULL`); `DROP TABLE IF EXISTS <tmp>` (L300) also clears any leftover temp table inside the next attempt's transaction. | L300; `core/state_store.py` L108 to L109 | INTERPRETATION |

### 4.4 Restart after a failure

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S141 | On the next open the stored version is still the old one, so the same gate applies: an allowed opener runs `run_migrations` again over the same version range (already-rebuilt tables are rebuilt again per S131), the relocation skips tables already moved, and `executescript` runs. | `core/state_store.py` L383, L420 to L446 | FACT (code path); INTERPRETATION (S131) |
| P03-S142 | A non-allowed opener after such a failure refuses (`MigrationNotPermitted`), as before. | L426 to L427 | FACT |
| P03-S143 | The declared unit for `main.py` has `Restart=on-failure`, `RestartSec=10`, `RestartPreventExitStatus=3 4 5`; its comment says exit 1 and 2 are restarted. Boundary fact only (owner A17; no claim that it ran). | `deploy/systemd/trading-system.service` L27 to L35 | FACT (declaration) |
| P03-S144 | INTERPRETATION (systemd semantics on that declaration): a deterministic migration failure (exit 2) or a refusal in market hours (exit 1) would be followed by a new start every 10 s while the service window allows a start; a start refused at 09:15 to 15:30 would, at its first restart after 15:30:00, see `market_open` False and migrate. | S033, S036, S143 | INTERPRETATION |

### 4.5 Backup before migrating

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S145 | No backup or copy is taken by the code before migrating: no `backup`, `.backup`, `copy2` or `shutil` in `core/migrations.py` or `core/state_store.py`, and none in `main.py` between L2080 and L2240. | grep | FACT |
| P03-S146 | Legacy deploy notes name operator backups taken before deploys, for example a pre-deploy backup file under `data_store/backups/` (`PATHS.md` L119) and a `pre_deploy_...` backup in `docs/SYSTEM_MAP.md` L181. Whether such backups were taken for each schema change is not established. | as cited | HISTORICAL |

## 5. Exception classes and how they propagate

### 5.1 Classes

| ID | Class | Defined | Base chain | Raised in the migration path | Label |
|---|---|---|---|---|---|
| P03-S147 | `StateStoreError` | `core/state_store.py` L120 | `StateError` (`core/exceptions.py` L92) → `TradingSystemError` (L30) → `Exception` | schema file missing L364; no version row L482 | FACT |
| P03-S148 | `SchemaVersionMismatch` | L130 | `StateStoreError` | newer DB L399; post-check L451; stub L497 (no caller) | FACT |
| P03-S149 | `MigrationNotPermitted` | L134 | `StateStoreError` | `_refuse_migration` L355 | FACT |
| P03-S150 | `TransactionError` | L142 | `StateStoreError` | not raised in the migration path (pointer: part P01 for `transaction`) | FACT |
| P03-S151 | `MigrationError` | `core/migrations.py` L136 | `Exception` only (outside `TradingSystemError`) | L177, L179, L285, L316, L371, L436 | FACT |
| P03-S152 | Raw errors | — | `sqlite3.Error`, `OSError` and others | `init_analytics_schema`, connection PRAGMAs and ATTACH, relocation (unwrapped), `executescript` | FACT |
| P03-S153 | `MigrationError` at L177 and L179 | — | — | Within `run_migrations`, L177 and L179 cannot fire from the rebuild call, because `_table_in_schema` has already returned True for the same text (exactly one block); they remain reachable from direct callers of `extract_create_table` (none outside `core/migrations.py`; grep). Code: L429, L433, L267 | INTERPRETATION |

### 5.2 `main.py`

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S154 | The store open at L2233 is not inside any `try` with an `except` in `_main_locked`; `main()` wraps `_main_locked` in `try/finally` only (releases the instance lock). | `main.py` L2187 to L2190, L2233 | FACT (AST scan and reading) |
| P03-S155 | The `__main__` guard: `except TradingSystemError` logs CRITICAL `system_error` with traceback and exits 1; `except Exception` logs CRITICAL `unexpected_error` and exits 2. `_log` is the module-level logger (L113) reassigned in `main()` (L2086, L2179). | L4285 to L4293 | FACT |
| P03-S156 | Resulting exit codes for a store-open failure: `MigrationNotPermitted`, `SchemaVersionMismatch`, `StateStoreError` → 1; `MigrationError` and raw `sqlite3` or OS errors → 2 (A01 M-24 recorded the `MigrationError` case). | S147 to S152, S155 | FACT (from code path) |
| P03-S157 | The exit-code list in the module docstring names 1 "TradingSystemError" and 2 "unexpected exception"; it has no entry naming a migration. | `main.py` L11 to L20 | FACT |

### 5.3 Scripts

| ID | Statement | Code | Label |
|---|---|---|---|
| P03-S158 | Per opener, see section 2.4: nine openers catch `Exception` at the open and end with 1 (S046, S049 to S053, S056, S057, S064); `forward_shadow_record` and `reconstruct_excursions` catch it in a top-level handler (S054, S058); `record_heartbeat` swallows it (S065); `premarket_healthcheck` turns it into a failed check result (S055); twelve let it escape the script (S041 to S045, S047, S048, S059 to S063); `main.py` reaches its guard (S040). | section 2.4 | FACT |
| P03-S159 | Independently of the caller's handler, every refusal first logs CRITICAL `MIGRATION_REFUSED ...` and attempts `alerts.critical.write_critical_sentinel(title="Schema migration refused (non-boot process)", ..., source_module="state_store", sentinel_dir=<DB parent directory>)`; a failure of the sentinel write is logged as an error and does not stop the raise. | `core/state_store.py` L338 to L355; `alerts/critical.py` L52 to L63 | FACT |
| P03-S160 | `scripts/backfill_closure_source_w8.py` adds its own check after the open: `_require_v45` reads `PRAGMA table_info(trades)` and raises `SystemExit("REFUSING: ...")` if `closure_source` is absent; its docstring says a data script must not migrate. | L173 to L183, L191 to L193 | FACT; HISTORICAL (docstring) |

## 6. Comments, docstrings and legacy documents about migration rules (HISTORICAL), beside the code

| ID | Source (HISTORICAL) | What it says | What the code does (FACT, cited) |
|---|---|---|---|
| P03-S161 | `core/migrations.py` L6, L22 to L33 | "Idempotent, data-preserving"; `schema.sql` is the single source of truth; if live DDL equals the schema DDL "the rebuild is skipped"; "the runner is safe to invoke on every startup". | The target side of the skip comparison ends with `;` (S130, FACT); the stored side does not (S131, INTERPRETATION); the runner is invoked only when `old_version < 45` (S008, S027). |
| P03-S162 | `core/migrations.py` L137 (`MigrationError` docstring) | "the DB is left untouched (rolled back)". | Only the failing table is rolled back; earlier tables of the same run stay committed (S135). |
| P03-S163 | `core/migrations.py` L412 to L413 | "Idempotent and safe to call on every startup ... Each table rebuild is individually atomic." | Per-table transaction (S122); no run-level transaction (S124). |
| P03-S164 | `core/migrations.py` L97 to L102 | v45 dry run on a production copy: 134 ms, integrity ok, 0 FK violations, rows byte-identical, "trigger + all 5 indexes restored"; failure injected after DROP and RENAME left the DB at v44. | The rebuild re-creates 4 explicit `trades` indexes (S100) and no trigger; the trigger comes from `executescript` (S084). INTERPRETATION: a fifth could be the primary-key auto-index. The dry run itself is UNKNOWN (no evidence survives). |
| P03-S165 | `core/migrations.py` L292 to L294; L264 to L265 | `foreign_keys` must be off for a rebuild; the pragma is a no-op inside a transaction; caller must not be inside a transaction. | Pragma set before `BEGIN` and restored in `finally` (S081, S083); `_initialize_schema` calls the runner with no open transaction (`isolation_level=None`, S005). |
| P03-S166 | `core/state_store.py` L13 to L16 (module docstring) | Open = WAL, foreign keys, "Loads schema.sql and runs it (idempotent ...)", "Verifies schema_version matches". | Also runs the newer-DB gate, the migration gate, the runner and the relocation (S007 to S010); not mentioned there. |
| P03-S167 | `core/state_store.py` L135 to L139, L180 to L184, L327 to L330; `main.py` L2219 to L2225 | Only `main.py`'s boot path may migrate, and only off-market; every other opener refuses and fails loudly; the refusal "Touches nothing in the DB". | Flags and gate as stated (S008, S031, S032). Before the refusal the analytics init and the connection PRAGMAs and ATTACH have run (S024). |
| P03-S168 | `core/state_store.py` L332 to L337 (refusal message) | The migration "applies at the next OFF-MARKET boot of the trading app"; "No manual DB surgery." | The next allowed open migrates; under the declared unit that can be an automatic restart after 15:30 (S144, INTERPRETATION). |
| P03-S169 | `core/state_store.py` L385 to L397 (dated 2026-07-08) | Fail fast on a newer DB so `executescript` cannot stamp the version down; rollback of a newer schema "must therefore be via its config flag ... NOT a code revert". | Gate at L398 to L405 (S007). |
| P03-S170 | `core/state_store.py` L407 to L419 | Migrate before `schema.sql`; if a migration fails it "rolls back, leaving the version untouched so the migration is retried on next startup". | Version untouched (S135); tables rebuilt earlier in the run are not rolled back (S124). |
| P03-S171 | `core/state_store.py` L487 to L492 (`migrate_to_latest`) | "Stub for future migrations. v1 has no prior versions." | Unused stub (S029). |
| P03-S172 | `core/schema.sql` L4, L8 to L9, L20 to L21, L1613 to L1653 | "Version: 1"; migrations "add new sections at the bottom and bump the schema_version row"; changes need "a corresponding migration in state_store.py"; footer "END OF SCHEMA v24" with a list to v27. | Stamp is 45 (S016); migration code is in `core/migrations.py`, not in `state_store.py` (S027). Pointer: parts P02a/P02b. |
| P03-S173 | `core/schema.sql` L288 to L290 | The trigger is a "BEHAVIOUR-ONLY pure add" re-applied by `executescript` on every boot, "so it needs NO schema_version bump". | `executescript` runs on every open by any opener (S009, S020), not only at boot. |
| P03-S174 | `docs/audit/migration_on_open_rule_14jul2026.md` L3, L85 | Status: the guard is a "PROPOSAL ONLY — NOT implemented". | The guard exists in the code (S008); the same file's L63 to L75 call the design ratified and describe the implementation; commit `ed1c4b9` (2026-07-14) changed both this document and `core/state_store.py`. |
| P03-S175 | same document L9 to L21, L23 to L29 | Migrations run on the first process that opens the DB with newer code, not at boot; a table records v42→v43 at 13-Jul 19:30 by `cron_watchdog` and v43→v44 at 23:41 by `forward_shadow_record`. | Those events predate the guard; no runtime evidence survives (UNKNOWN). At the baseline only `main.py` can migrate an existing older DB (S031, S032). |
| P03-S176 | same document L39 to L54, L67, L75 | 23 scripts plus `main.py` construct `StateStore`; `generate_screened_stocks_csv` is listed among them; `main.py:1566` passes `allow_migrate=True`; "all 24 openers refuse a pending migration". | At the baseline: 25 non-`main.py` constructions (S066), none in `generate_screened_stocks_csv`; the call is at `main.py` L2233. |
| P03-S177 | same document L68 to L70 (AC2, AC4) | A mid-session crash-restart with a pending migration refuses; recovery is "restart the app off-market (or wait for the 08:15 boot)". | As S033, S039, S144. |
| P03-S178 | `PATHS.md` L151; `docs/MASTER_PENDING_01-Aug-2026.md` L166 to L168 | L151 (pre-guard, 14-Jul) warns that any opener migrates on open; the later note says an evening schema push "trips `_refuse_migration` on every heartbeat cron until the next 08:15 boot". | Code path: with a pending migration, every `record_heartbeat` open goes through `_refuse_migration` (CRITICAL log, sentinel attempt), and the exception is swallowed (`return False`) (S065, S068). |
| P03-S179 | `scripts/preflight/checks/database.py` L3 to L8, L56 to L63 | Pre-flight never migrates; DB below code is the "NORMAL pre-migration state", app migrates at startup. | Raw read, WARN on pending (S069). |
| P03-S224 | `core/migrations.py` L198, L200 to L201 | The normaliser drops `IF NOT EXISTS` because "sqlite_master never stores it" and removes double quotes because RENAME quotes the table name while a fresh CREATE does not. | `_normalize_ddl` (L194 to L207) has no step for the terminating `;`, which the target text keeps (S130). |

## Concerns for the AUDIT (neutral)

| ID | What the code does, where | Label |
|---|---|---|
| P03-S180 | The "idempotent skip" at `core/migrations.py` L273 compares a target text that ends in `;` (L166, L180) with stored text that, per SQLite's storage format, does not; on that reading every listed table in range that exists and is still in `schema.sql` is rebuilt on each migration run (S130, S131; tables absent from the database or from `schema.sql` are skipped, L268 to L272, L429 to L431). | FACT; INTERPRETATION |
| P03-S181 | A multi-table migration is committed table by table (L421 to L439); a failure leaves earlier tables rebuilt and the version unchanged, while the `MigrationError` docstring (L137) says the DB is left untouched. | FACT; HISTORICAL |
| P03-S182 | The `trades` rebuild drops `trg_trades_terminal_status_guard` and does not re-create it; only the later `executescript` does (S084, S085), and if `executescript` fails the trigger stays absent until a later successful open. | FACT; INTERPRETATION |
| P03-S183 | `PRAGMA foreign_key_check` at L314 has no table argument, so an FK violation in an unrelated table fails a rebuild (S110). | FACT; INTERPRETATION |
| P03-S184 | The relocation (L376 to L390) is a two-file transaction in WAL mode and its errors are not wrapped into `MigrationError` (S106, S125); it also empties `analytics.<t>` before copying (L378). | FACT; INTERPRETATION |
| P03-S185 | `_read_existing_version` (L463 to L474) maps an `OperationalError`, a missing row and a non-integer value to None, the same value as a brand-new DB; on that route no gate runs and `executescript` runs against the existing tables without any rebuild, stamping 45 only if every statement succeeds (S019, S221). | FACT; INTERPRETATION (S221) |
| P03-S186 | `_table_in_schema` (L241 to L247) treats duplicate `CREATE TABLE` blocks as "not in schema" and the runner skips that table with a debug log (S088). | FACT |
| P03-S187 | The refusal path is preceded by `init_analytics_schema` and the connection PRAGMAs and ATTACH (S024), while its docstring says it touches nothing in the DB (L327 to L330). | FACT; HISTORICAL |
| P03-S188 | `MigrationError` sits outside `TradingSystemError` and gives exit 2 in `main.py`; refusals give exit 1 (S151, S156). Under the declared unit both are restarted every 10 s (S143, S144). | FACT; INTERPRETATION |
| P03-S189 | `--status` and `--dry-run` open the store with `allow_migrate=True` (S039; A01 C5). | FACT |
| P03-S190 | `executescript` runs on every open that passes both version gates (S009; not on a refused open, S021, nor on a newer-DB open, S023). Any `schema.sql` change made without a version bump (for example the trigger, `core/schema.sql` L288 to L290) is applied by whichever such open comes first, at any time. Every such open re-writes the version row and re-runs the DROP statements at `core/schema.sql` L436 to L438 (S020). | FACT; INTERPRETATION |
| P03-S191 | The target version exists as two literals (`core/state_store.py` L102, `core/schema.sql` L1610) and their agreement is checked only after the stamp is written (S017, S139). | FACT |
| P03-S192 | No pre-migration backup in code (S145). | FACT |
| P03-S193 | Rebuild copy semantics: intersecting columns only, AUTOINCREMENT counters restart from the highest copied id (S133, S134). | INTERPRETATION |
| P03-S194 | Definitions changed with no version bump or no rebuild path: `control_tower_findings` at `3413f27`; `session` and `eod_squareoff_log` before v25 (S111, S120). | FACT (text parsing) |
| P03-S195 | Any opener given a path where no DB exists creates a complete v45 DB there (S019), including openers that cannot migrate; some openers check `exists()` first (S041, S042, S044, S045, S047, S048, S055, S061, S064, S065) and the other 16 do not (S040, S043, S046, S049 to S054, S056 to S060, S062, S063). | FACT |
| P03-S196 | `analytics.db` has no version marker; its schema is re-applied by `executescript` on every open (S004, S018). | FACT |
| P03-S223 | `schema.sql` contains a destructive `DROP TABLE IF EXISTS capital_ledger` (L436) that runs on every open reaching `executescript`: on a new or current DB by any opener, whatever `allow_migrate` and `market_open` are, and on an older DB after an allowed migration; it is not reached on a refused or newer-DB open (S021, S023, S222). | FACT |

## Questions about intent (OPEN QUESTION, for the project owner)

| ID | Question | Label |
|---|---|---|
| P03-S197 | Was the skip at `core/migrations.py` L273 meant to let a matching table go un-rebuilt (so a migration run touches only tables that differ)? | OPEN QUESTION |
| P03-S198 | Was a multi-table step (for example v25's four tables) meant to be all-or-nothing, as the `MigrationError` docstring states? | OPEN QUESTION |
| P03-S199 | After a refusal in market hours, was the migration meant to wait for a deliberate off-market start (as the refusal message says), or was an automatic restart after 15:30 accepted? | OPEN QUESTION |
| P03-S200 | A01-05 (agreed 05-Nov-2026) records the intent that `--status` is read-only and `--dry-run` changes no state; does that intent also settle schema migration on these opens (S039), or is a separate decision needed? | OPEN QUESTION |
| P03-S201 | Should an existing DB whose version row is missing or unreadable be treated as a new DB? | OPEN QUESTION |
| P03-S202 | What is the lowest starting version the runner was meant to support (the map starts at v24→v25; `session` and `eod_squareoff_log` changes before v25 have no path)? | OPEN QUESTION |
| P03-S203 | Was a backup before migration meant to be part of the code or of the operator's deploy procedure only? | OPEN QUESTION |
| P03-S204 | Was `analytics.db` meant to carry its own schema version? | OPEN QUESTION |

## UNKNOWN / NOT ESTABLISHED

| ID | Item | Label |
|---|---|---|
| P03-S205 | Whether, when and by which process any migration actually ran on the production DB, and its outcome (no database, log, sentinel or crontab survives; the legacy notes in S175 and S146 are HISTORICAL). | UNKNOWN / NOT ESTABLISHED |
| P03-S206 | The SQLite version in production, which governs the stored DDL text (S131), RENAME behaviour (S109) and the two-file commit behaviour (S125). | UNKNOWN / NOT ESTABLISHED |
| P03-S207 | The schema version of the production DB when the machines were destroyed. | UNKNOWN / NOT ESTABLISHED |
| P03-S208 | Whether a refusal or migration-failure restart loop ever occurred under systemd (S144). | UNKNOWN / NOT ESTABLISHED |
| P03-S209 | Whether any DB carried the earlier `control_tower_findings` definition (S120). | UNKNOWN / NOT ESTABLISHED |
| P03-S210 | Whether refusal sentinels were written and delivered (A14). | UNKNOWN / NOT ESTABLISHED |
| P03-S211 | Whether pre-deploy backups were taken before each schema change (S146). | UNKNOWN / NOT ESTABLISHED |

## Boundary handoffs (owner topic: what crosses)

| ID | Owner topic | What crosses |
|---|---|---|
| P03-S212 | A01 | `main.py` L2218 to L2237 (market-open formula, the only `allow_migrate=True` open); the guards before it (holiday, service window, bypass flags, config exit 5); `--status`/`--dry-run` (C5); the `__main__` exit mapping L4285 to L4293 (M-24); S-03. |
| P03-S213 | A02 | `trading_hours.market_open` and `market_close` (`config/system_config.yaml` L103 to L104; `core/config_loader.py` L92 to L93). |
| P03-S214 | A17 | `deploy/systemd/trading-system.service` L27 to L35 restart declaration; `scripts/deploy_assert.py` read-only version BLOCKER. |
| P03-S215 | A14 | `write_critical_sentinel` called from `_refuse_migration` with the DB's parent directory as the sentinel directory. |
| P03-S216 | A16 | `utils/cron_heartbeat.py` `record_heartbeat` and `HeartbeatTimer` (refusal swallowed, S065, S068); `cron_officer`, `check_cron_drift`, `cron_watchdog` openers; all declared schedules of openers (declaration only). |
| P03-S217 | A20 | `scripts/preflight/checks/database.py` raw version check; `scripts/premarket_healthcheck.py` opener. |
| P03-S218 | A15 | Report and monitoring openers (S041, S042, S058, S061, S063); `ops_dashboard` raw version read; Control Tower `ensure_indexes`; where the `state_store.migrations` log lines go. |
| P03-S219 | A12, A13, A05, A07, A08, A18, A19 | The openers in section 2.4 owned by each; `_require_v45` in `scripts/backfill_closure_source_w8.py` (A12); `t2_cnc_gtt_realtest` fresh DB (A19). |
| P03-S220 | A03 other parts | P01: connection PRAGMAs, ATTACH, raw `connect`/`connect_readonly`, `fetch_one`, `transaction`; P02a/P02b: the `CREATE` blocks, the trigger L291, the stamp L1610 and header and footer comments; P06a/P06b: DDL outside the store (S074); P07: `analytics_schema.sql`, `init_analytics_schema`, no analytics version; P09a: `backup_restore_drill` version check; P09b: `db_retention` and `wal_checkpoint` openers. |
