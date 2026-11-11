# A03 evidence: The backup scripts

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P09a, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** `scripts/backup_evidence.py`, `scripts/backup_restore_drill.py` and `scripts/backup_retention.py`, traced from code (never run), with their declared invocations as A16 boundary facts. Statement IDs `P09a-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

- Corrector (third pass): read the brief, the draft and the check; re-read at the baseline every line range cited by a finding: `utils/cron_heartbeat.py` L50 to L97; `core/state_store.py` L100 to L115, L120 to L134, L170 to L250, L320 to L460; `core/db_connect.py` L38 to L90; `core/schema.sql` L285 to L300, L430 to L440, L1605 to L1612 (plus a grep for DROP, INSERT, DELETE, UPDATE); `core/exceptions.py` (class lines); `alerts/critical.py` L52 to L63; `alerts/telegram_notifier.py` L78 to L104, L270 to L298; `core/logger.py` L340 to L350; `scripts/backup_restore_drill.py` L25 to L42, L195 to L235, L305 to L377; `scripts/backup_retention.py` L14 to L24, L80 to L200, L276 to L310; `scripts/output_retention.py` L60 to L66; `config/cron_registry.yaml` L33, L48; `deploy/cron/trading-system.cron` L19, L22; `main.py` L134 (path constant only; the file it names was not opened); a `git grep` for `logging.basicConfig` (tests excluded). Home-directory paths were masked in command output. Nothing was run, imported or changed in the clone.

- Read in full at the baseline: `scripts/backup_evidence.py` L1 to L143; `scripts/backup_restore_drill.py` L1 to L377; `scripts/backup_retention.py` L1 to L310.
- Invocation declarations read: `config/cron_registry.yaml` L1 to L81 and L742 to L757; `deploy/cron/trading-system.cron` L1 to L40 and L145 to L151; all seven files in `deploy/systemd/` searched for "backup", "retention" and "drill".
- Dependencies read only where the three scripts call them: `utils/cron_heartbeat.py` L1 to L97; `core/state_store.py` L102, L172 to L198, L3305 to L3325; `core/logger.py` L266 to L274 and L354 to L395 (handler set-up only); `alerts/telegram_notifier.py` L81 to L96 and L271 to L297; `core/cron_registry.py` L128 to L147 and L296 to L309; `core/evidence_contract.py` L298 to L330 (producer file naming only); `scripts/output_retention.py` L48 to L64 (comment only); `scripts/backfill_closure_source_w8.py` L125 to L145 (producer file naming only); `.gitignore`.
- HISTORICAL documents consulted for pointers only: `docs/05_incident_response.md` L215 to L233; `docs/06_deployment_guide.md` L200 to L220; `docs/crash_test_info_04jun2026.md` L676 to L682.
- Tools: `cat -n`, `sed -n`, `grep`, `git grep`, `git log`, `git show`, `git diff`, `git cat-file -e`, `git merge-base --is-ancestor`, `git check-ignore --no-index` (all read-only). No legacy code, SQL or shell was executed or imported; no `ast` parsing was used; every statement comes from reading the text.
- Not opened (security rule): `.env` (sourced by the cron lines), `config/accounts.csv`, any token or key file. Tests (A19) were not traced.
- Notation: `<PROJECT_ROOT>` = the project directory under the operator's home directory; `<VENV_PYTHON>` = a virtual-environment Python interpreter under the operator's home directory. The absolute paths written in the cron file are not reproduced.

| ID | Check | Result |
|---|---|---|
| P09a-S001 | Helper, BEFORE work: `git rev-parse HEAD` and `git status --short` on the local read-only clone at the baseline | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline); status output empty |
| P09a-S002 | Helper, AFTER work: the same two commands | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb`; status output empty |
| P09a-S153 | Checker, BEFORE and AFTER work (as its check file states) | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb` both times; status output empty both times |
| P09a-S154 | Corrector, BEFORE work | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb`; status output empty |
| P09a-S155 | Corrector, AFTER work | FACT: `970aabf3c78d777d9d34549e021f7c8e756c7bdb`; status output empty |

## 1. Invocation declarations (boundary facts for A16; a schedule is never proof of a run)

| ID | Registry key | Registry lines | Cron file lines | Cron expression | Command as declared | Wrapper | Log target (stdout and stderr appended) | Completion marker | `monitored` |
|---|---|---|---|---|---|---|---|---|---|
| P09a-S003 | `evidence_backup` | `config/cron_registry.yaml` L67 to L81 | `deploy/cron/trading-system.cron` L27 to L28 | `10 1 * * *` | `scripts/backup_evidence.py` (no arguments) | `cd <PROJECT_ROOT> && set -a && . ./.env && set +a && PYTHONPATH=. <VENV_PYTHON> ...` | `logs/cron-evidence-backup.log` | `data_store/cron_marks/evidence_backup.done` (exit code and ISO timestamp) | true (L74) |
| P09a-S004 | `backup_retention` | L52 to L66 | L24 to L25 | `0 2 * * *` | `scripts/backup_retention.py --apply` | same python wrapper | `logs/cron-backup-retention.log` | `data_store/cron_marks/backup_retention.done` | true (L59) |
| P09a-S005 | `backup_restore_drill` | L742 to L756 | L150 to L151 | `0 3 1 * *` | `scripts/backup_restore_drill.py --quiet` | same python wrapper | `logs/cron-backup-drill.log` | none: the registry entry has no `marker_name` and the cron line writes no `.done` file | true (L749) |
| P09a-S006 | `db_backup` (producer of the files the drill and retention read) | L22 to L36 | L18 to L19 | `0 1 * * *` | `sqlite3 <PROJECT_ROOT>/data_store/trading_system.db ".backup <PROJECT_ROOT>/data_store/backups/trading_system-$(date +%Y-%m-%d).db"` (both the registry command, L33, and the cron line write each `%` as `\%`; shown here unescaped) | none (`env_wrapper: none`) | `logs/cron-db-backup.log` | `db_backup.done` | false (L29) |
| P09a-S007 | `analytics_backup` (producer) | L37 to L51 | L21 to L22 | `5 1 * * *` | `sqlite3 <PROJECT_ROOT>/data_store/analytics.db ".backup <PROJECT_ROOT>/data_store/backups/analytics-$(date +%Y-%m-%d).db"` (both the registry command, L48, and the cron line write each `%` as `\%`; shown here unescaped) | none | `logs/cron-db-backup.log` | `analytics_backup.done` | false (L44) |

- P09a-S008 FACT: the cron file header says it is a generated artefact of `config/cron_registry.yaml` (`deploy/cron/trading-system.cron` L1 to L3); it sets `SHELL=/bin/bash` (L13) and contains no `TZ=` or `CRON_TZ=` line (searched). HISTORICAL: its comment at L11 says "All times IST (Asia/Kolkata)". The time zone of any machine is UNKNOWN / NOT ESTABLISHED.
- P09a-S009 FACT: no file in `deploy/systemd/` mentions any of the three scripts or the strings "backup", "retention" or "drill" (grep over all seven unit and timer files returned nothing).
- P09a-S010 FACT: the registry header says the generation fields (`cron_expression`, `command`, `env_wrapper`, `log_target`, `marker_name`) are authoritative and `schedule` is documentation (`config/cron_registry.yaml` L4 to L5).
- P09a-S011 FACT: `core/cron_registry.py` L131 to L135 makes `effective_heartbeat_required` equal to `monitored` unless `heartbeat_required` is set, and L137 to L147 derives the detection method `heartbeat_db` for heartbeat-required jobs, else `exit_code_file`. None of the three entries sets `heartbeat_required` or `detection_method` (registry L52 to L81, L742 to L756). INTERPRETATION: all three are declared for heartbeat-based detection by the Cron Officer (A16 owns that consumer).
- P09a-S012 HISTORICAL: `docs/crash_test_info_04jun2026.md` L680 lists `backup_restore_drill` as `0  21 1 * *` labelled "(03:00 IST 1st of month)", and L682 says the IST times were converted from UTC and the VM crontab "may differ". The canonical cron file declares `0 3 1 * *` (L151). Which expression any machine used is UNKNOWN / NOT ESTABLISHED.

## 2. `scripts/backup_evidence.py`

### 2.1 Purpose, arguments, environment, configuration

- P09a-S013 HISTORICAL (L2 to L16): the docstring says the script backs up the "forward evidence contract (Batch 1)"; `data_store/evidence/*.jsonl` is excluded from `output_retention.py` and nothing else backed it up; it copies each `signal_evidence_<ARM>_<DATE>.jsonl` and each failure ledger `evidence_failures_<ARM>_<DATE>.jsonl` into `data_store/backups/evidence/`, keeping the file name.
- P09a-S014 HISTORICAL (L18 to L23): the docstring calls it a SAME-DISK copy that protects against deletion, truncation or in-place corruption of the source, not against loss of the disk or machine; it states that nothing in the system copies any artefact off the box, the SQLite backups included, and that off-box protection is "a separate, OPEN item".
- P09a-S015 FACT (L129 to L132): the only command-line argument is `--all` (`store_true`, help "accepted for symmetry; every present file is copied either way"); the parse result is discarded (L132), so the flag changes nothing.
- P09a-S016 FACT: the script reads no environment variable and no configuration file (imports L48 to L54 are standard library only; no `os.environ` or `getenv`). Paths derive from the script's own location: `ROOT` = parent of `scripts/` (L56); `SRC_DIR` = `ROOT/data_store/evidence` (L57); `DST_DIR` = `ROOT/data_store/backups/evidence` (L58).
- P09a-S017 INTERPRETATION: because `ROOT` comes from `__file__`, the working directory does not change the source or destination. The cron line still sources `.env` (cron L28), which this script does not use.

### 2.2 Source, destination, consistency mechanism

- P09a-S018 FACT (L59, L93): source selection is the union of two non-recursive globs in `SRC_DIR`, `signal_evidence_*.jsonl` and `evidence_failures_*.jsonl`, de-duplicated through a set and sorted.
- P09a-S019 FACT (L94 to L95): the destination is `DST_DIR/<same file name>`; the temporary file is in the same directory, named `<file name>.tmp-<process id>`.
- P09a-S020 FACT: no compression and no date or generation suffix is added; there is one destination file per source file name (L94). INTERPRETATION: the backup set holds one generation per source file (the latest accepted copy); earlier states are not kept.
- P09a-S021 FACT (L92): `DST_DIR` is created with `mkdir(parents=True, exist_ok=True)`.
- P09a-S022 FACT (L97 to L100): if the destination exists and its SHA-256 equals the source's (both files read in full by `_sha256`, L63 to L68, in 1 MiB chunks, L60), the file is counted as skipped.
- P09a-S023 FACT (L101 to L106): if the destination exists and is not a byte-prefix of the source (`_is_prefix`, L71 to L83: size comparison, then chunk-by-chunk comparison), a "REFUSED" failure is recorded and the destination is not touched.
- P09a-S024 FACT (L107): the copy is `shutil.copy2(src, tmp)` (content and metadata).
- P09a-S025 FACT (L110 to L114): after the copy, the temporary file must be a byte-prefix of the current source and, if a destination exists, not smaller than it; otherwise a "copy verification failed" failure is recorded and the destination is left as it was.
- P09a-S026 FACT (L115): `os.replace(tmp, dst)` installs the copy.
- P09a-S027 FACT: the script takes no lock, calls no `fsync` and does not coordinate with the writer (grep for lock, fsync, flock: none). The writer appends with `open(path, "a")` at `core/evidence_contract.py` L596 and L697 (owner A15).
- P09a-S028 INTERPRETATION: consistency rests on the files being append-only. A copy taken while the writer appends can end in a partial last line; that still passes the prefix check (L110) and becomes the backup. `os.replace` in the same directory swaps the name atomically on POSIX; without `fsync`, durability of the new copy across a power loss is not ensured by this code.
- P09a-S029 FACT: the mechanism is a plain file copy (no `sqlite3` import); the inputs are JSONL text files.
- P09a-S030 INTERPRETATION: `DST_DIR` lies under `ROOT/data_store`, the same tree as `SRC_DIR`; whether `data_store/backups` was a separate mount on any machine is UNKNOWN / NOT ESTABLISHED.

### 2.3 Verification, evidence and logs, alerts, exit codes, error handling

- P09a-S031 FACT (L135 to L138): the script prints one summary line to stdout (copied, skipped and failed counts and the absolute source and destination paths) and one "FAILED" line per failure to stderr. It has no logger, no heartbeat, no Telegram call and no database access.
- P09a-S032 FACT (L139, L142 to L143): exit code 1 if any failure was recorded, otherwise 0.
- P09a-S033 FACT (L117 to L124): any exception inside the per-file block is caught and recorded as a failure, and the loop continues; the `finally` block removes the temporary file and swallows `OSError` from that removal.
- P09a-S034 FACT (L90 to L91): if `SRC_DIR` is not a directory, `backup_once` returns `(0, 0, [])`; the summary shows zero counts and the exit code is 0.
- P09a-S035 FACT: the `mkdir` at L92 and the glob at L93 are outside the `try` block. INTERPRETATION: an exception there (for example a permission error) leaves `main()` uncaught; Python prints a traceback to stderr and exits with status 1. HISTORICAL: the docstring says "Never raises into cron" (L37).
- P09a-S036 FACT: there is one copy attempt per file per run, with no retry loop (L107 to L116).
- P09a-S037 FACT: verification is the prefix and size check only (L110 to L111); the installed destination is not hashed after `os.replace`, and JSONL content is not parsed.
- P09a-S038 FACT (cron L28): the cron line appends stdout and stderr to `logs/cron-evidence-backup.log` and writes the exit code and a timestamp to `data_store/cron_marks/evidence_backup.done`.

### 2.4 Inclusion and exclusion

- P09a-S039 FACT (L59, L93): only top-level files of `data_store/evidence` matching the two patterns are included; any other name or subfolder there is excluded.
- P09a-S040 FACT (L57 to L58): the source folder is not inside `data_store/backups`, so no other backup is included, and the evidence backup folder is never a source.
- P09a-S041 FACT (path patterns only; nothing opened): the two patterns, applied in `data_store/evidence`, cannot select `.env`, `config/accounts.csv` or the broker session token file, which lie outside that folder (the token file path used by code is under `data_store/session/`, `main.py` L134; path only). See P09a-S151 for the drill and retention selections.
- P09a-S042 FACT: `backup_retention.py` lists only direct entries of `data_store/backups` that are regular files (L121, L123), so `data_store/backups/evidence/` and its contents are outside its selection. INTERPRETATION: none of the three scripts prunes `data_store/backups/evidence/`; `output_retention.py` declares `data_store/backups/` out of its scope in a comment (L52; see part P09b).
- P09a-S043 FACT: the restore drill reads only `trading_system-*.db` (drill L102); no code in this part restores or re-verifies evidence backups.

### 2.5 Routes

| ID | Route | What the code does |
|---|---|---|
| P09a-S044 | Normal | FACT: new file: copy to temp, verify, `os.replace`; unchanged file: skipped; grown file whose backup is a prefix: copy and replace (L97 to L116). |
| P09a-S045 | Source shrank or was rewritten | FACT: "REFUSED" failure, destination preserved, exit code 1 (L101 to L106, L139). |
| P09a-S046 | Source grows during the copy | FACT: the copy is accepted if it is still a prefix and not smaller than the old backup (L110 to L111); it holds the bytes present when copied. |
| P09a-S047 | Error on one file | FACT: recorded, loop continues, exit code 1 (L117 to L118, L139). |
| P09a-S048 | Source folder missing | FACT: nothing copied, exit code 0 (L90 to L91). |
| P09a-S049 | Process killed mid-copy (restart) | INTERPRETATION: `finally` does not run on SIGKILL, so `<name>.tmp-<pid>` stays in `DST_DIR`; later runs use another process id and no code removes such files; the destination is intact because `os.replace` was not reached. |
| P09a-S050 | Retry | FACT: no retry within a run; a later run re-evaluates every file from L97 (HISTORICAL: "idempotent, cheap to re-run", L36). |

## 3. `scripts/backup_restore_drill.py`

### 3.1 Purpose, arguments, environment

- P09a-S051 HISTORICAL (L1 to L9): header "FIX-149"; purpose: pick the latest backup, restore it to a temporary DB, verify schema integrity, table completeness, FK consistency and data sanity, and output a drill report; "Designed to run monthly via cron (1st of month, 03:00 IST) or manually."
- P09a-S052 HISTORICAL (L20 to L23): documented exit codes: 0 drill passed, 1 drill failed, 2 no backups found.
- P09a-S053 FACT (L345 to L367): arguments `--backup-dir` (Path, default `ROOT/data_store/backups`), `--output-dir` (Path, default `ROOT/docs`), `--quiet` (`store_true`).
- P09a-S054 FACT: the file reads no environment variable directly. INTERPRETATION: `tempfile.mkdtemp` (L227) follows Python's standard temporary-directory resolution (`TMPDIR`, `TEMP`, `TMP`, then the platform's default temporary folder).
- P09a-S055 FACT (L36 to L40): the script puts `ROOT` on `sys.path` and imports `EXPECTED_SCHEMA_VERSION` from `core.state_store` at module load; `core/state_store.py` L102 sets it to 45 at the baseline.
- P09a-S056 FACT (L43 to L69): `EXPECTED_TABLES` names 26 tables, from `schema_meta` to `cron_heartbeat`. HISTORICAL (L70 to L72): the comment says `candles`, `system_metrics` and `system_metrics_daily` moved to `analytics.db` (v28) and are intentionally not expected.

### 3.2 Backup selection, target isolation, overwrite risk to the live database

- P09a-S057 FACT (L100 to L106): the drill selects the file with the newest modification time among the non-recursive glob `trading_system-*.db` in the backup folder.
- P09a-S058 FACT (L102): `pre_*.db` and `analytics-*.db` files are never selected. INTERPRETATION: analytics backups and deploy or ad-hoc backups are never drilled by this script.
- P09a-S059 FACT: the age of the selected backup is not checked; its modification time is only logged (L223).
- P09a-S060 FACT (L227 to L228, L109 to L110): the target is `restore_test.db` in a new temporary folder with prefix `backup_drill_`; the "restore" is `shutil.copy2(backup, target)`, which copies the `.db` file only (no `-wal` or `-shm` file of the backup).
- P09a-S061 FACT: every check runs on the temporary copy (`test_db` at L239, L249, L259, L282, L293, L299); no check opens `data_store/trading_system.db`; the backup file itself is only read by `copy2` and `stat` (L103, L110, L219, L223).
- P09a-S062 FACT: the drill touches the live database path only through the heartbeat (L329 to L334). `record_heartbeat` opens the relative path `data_store/trading_system.db` (`utils/cron_heartbeat.py` L61, L81 to L84) through `StateStore`, whose constructor runs `_initialize_schema()` (`core/state_store.py` L198; `allow_migrate` defaults to False, L177). On every open that step first runs `db_connect.init_analytics_schema` on `analytics.db` beside the live database (`core/state_store.py` L375; `core/db_connect.py` L67 to L90: `PRAGMA journal_mode = WAL`, `synchronous = FULL`, then `executescript` of the analytics schema), then opens the live database with the connection PRAGMAs, `journal_mode = WAL` among them (`core/state_store.py` L107 to L113, applied at L241 to L242), and ATTACHes `analytics.db` (L247). A stored `schema_version` above 45 raises `SchemaVersionMismatch` (L398 to L405); one below 45 is refused by `_refuse_migration` with a CRITICAL log and a critical sentinel file before `MigrationNotPermitted` is raised (L420 to L427, L326 to L355). Otherwise `conn.executescript(schema_sql)` runs unconditionally (L446); `core/schema.sql` includes `DROP TABLE IF EXISTS capital_ledger` and two `DROP INDEX IF EXISTS` (L436 to L438), `CREATE ... IF NOT EXISTS` statements such as the trigger at L291, and `INSERT OR REPLACE INTO schema_meta` of `schema_version` 45 (L1610). `record_heartbeat` swallows any of these exceptions and returns False (L94 to L95; all three exception classes derive from `Exception`, `core/state_store.py` L120 to L134, `core/exceptions.py` L30, L92). When the open succeeds, it inserts a row into `cron_heartbeat` (`core/state_store.py` L3305 to L3325). See parts P01, P03 and P05.
- P09a-S063 INTERPRETATION: the drill never copies restored data back over the live database file; its restore step cannot overwrite the live database.
- P09a-S064 FACT: the drill opens the copy with plain `sqlite3.connect(str(db_path))` at six sites (L114, L123, L137, L158, L172, L184), not through `core/db_connect.py` (see part P01). INTERPRETATION: default opening is read-write, so `-wal` or `-shm` files can appear beside the copy; L317 to L322 remove them.
- Credential-holding files and the drill's selection: see P09a-S151.

### 3.3 Verification steps

| ID | Step | Lines | Operation | Effect on the verdict |
|---|---|---|---|---|
| P09a-S065 | Integrity | L113 to L119, L238 to L246 | `PRAGMA integrity_check`; passes only if the first row is `ok` | failure sets `passed = False` |
| P09a-S066 | Schema version | L122 to L133, L248 to L256 | `SELECT value FROM schema_meta WHERE key='schema_version'`, compared with `EXPECTED_SCHEMA_VERSION`; no row gives version -1 | mismatch fails |
| P09a-S067 | Table completeness | L136 to L154, L258 to L268 | names from `sqlite_master` where `type='table'`; missing and extra compared with `EXPECTED_TABLES` (`sqlite_sequence` ignored) | missing fails; extra is informational |
| P09a-S068 | Row counts | L147 to L150, L270 to L279 | `SELECT COUNT(*) FROM [table]` for every present table except `sqlite_sequence` | none; "WARNING: empty" marker when `signals`, `trades` or `orders` has 0 rows (L75, L276 to L277) |
| P09a-S069 | Foreign-key orphans | L84 to L97, L157 to L168, L281 to L290 | two LEFT JOIN orphan queries: `trades.signal_id` to `signals`, `orders.trade_id` to `trades`; `PRAGMA foreign_keys = ON` is set (L159) but `PRAGMA foreign_key_check` is not used | any orphan fails |
| P09a-S070 | WAL checkpoint | L183 to L191, L292 to L296 | `PRAGMA wal_checkpoint(PASSIVE)`; True unless an exception; the returned row is not read | none |
| P09a-S071 | Sample queries | L77 to L82, L171 to L180, L298 to L303 | CLOSED and OPEN trade counts, `MAX(DATE(triggered_at))` from `signals`, order count | logged only |

- P09a-S072 INTERPRETATION: the foreign-key step covers two relations only; other foreign keys declared in the schema (see parts P02a and P02b) are not checked. A `trades` row with a NULL `signal_id` would be counted as an orphan by the query at L87 to L89; the business meaning of such a row is not A03's.
- P09a-S073 INTERPRETATION (SQLite semantics): on a database not in WAL mode, `PRAGMA wal_checkpoint` returns without error, so "CLEAN" shows only that no exception was raised.

### 3.4 Outcome recording and exit codes

- P09a-S074 FACT (L197 to L200): every report line is collected and also printed to stdout unless `--quiet`.
- P09a-S075 FACT (L339 to L342): the report is written to `<output-dir>/backup_drill_<YYYY-MM-DD>.md` with `write_text` (a same-day re-run overwrites it); the folder is created if absent. The default folder is `ROOT/docs` (L359).
- P09a-S076 FACT (L202 to L203): the report date comes from `datetime.now()` (naive local time), not from `core.time_authority`.
- P09a-S077 FACT (L204 to L310): the report holds the execution time, the expected schema version, the selected backup's name, size and modification time, the temporary restore path, each step's result, per-table row counts, the sample-query values and the verdict.
- P09a-S078 FACT (L329 to L334): after the report is written, `record_heartbeat("backup_restore_drill")` is called with no status, so the status is the default "SUCCESS" (`utils/cron_heartbeat.py` L57) whether `passed` is True or False; any exception is swallowed.
- P09a-S079 FACT (L211 to L217): when no backup is found, a FAIL report is written and the function returns False before the heartbeat, so no heartbeat is written.
- P09a-S080 FACT (L370 to L377): the process exits 0 when `run_drill` returns True, otherwise 1. INTERPRETATION: exit code 2 (documented at L23) is never produced; the no-backup case exits 1.
- P09a-S081 FACT: the drill makes no Telegram call and no direct alert call (imports L27 to L40, L331). Indirectly, if the live database's stored schema version is below `EXPECTED_SCHEMA_VERSION`, the `StateStore` opened for the heartbeat logs CRITICAL and calls `alerts.critical.write_critical_sentinel` with `sentinel_dir` set to the database's folder (`data_store`) before raising (`core/state_store.py` L326 to L355, L420 to L427); the raise is swallowed (`utils/cron_heartbeat.py` L94 to L95; drill L333 to L334). The sentinel's delivery is A14's.
- P09a-S082 FACT (cron L151): the cron line passes `--quiet`, so stdout is suppressed; stderr is appended to `logs/cron-backup-drill.log`; no `.done` marker is written.
- P09a-S083 FACT: `.gitignore` ignores `data_store/` (L17) and `logs/` (L20) but not `docs/` (only `docs/system_manuals/*.docx`, L42); `git check-ignore` reports no rule for `docs/backup_drill_2026-01-01.md`; no `backup_drill_*.md` file is tracked at the baseline. INTERPRETATION: a report written to the default folder would sit in a tracked folder as an untracked file; whether the deployed project folder was a git working tree is A17's question (UNKNOWN / NOT ESTABLISHED).

### 3.5 Clean-up

- P09a-S084 FACT (L312 to L325): in `finally`, the drill removes `restore_test.db`, its `-wal` and `-shm` files, then `rmdir`s the temporary folder; any exception is swallowed.
- P09a-S085 INTERPRETATION: if another file remains in the temporary folder, `rmdir` fails silently and the folder stays; a process killed before `finally` leaves the folder and a full-size copy of the backup in the temporary location; no code removes earlier `backup_drill_*` folders.

### 3.6 Routes

| ID | Route | What the code does |
|---|---|---|
| P09a-S086 | Normal pass | FACT: report written, heartbeat "SUCCESS", exit code 0 (L327, L332, L377). |
| P09a-S087 | Verification failure (integrity, version, missing tables, orphans) | FACT: report ends "DRILL FAILED", heartbeat still "SUCCESS" (P09a-S078), exit code 1. |
| P09a-S088 | No backup found | FACT: FAIL report, no heartbeat, exit code 1 (L211 to L217, L377). INTERPRETATION: a missing backup folder behaves the same, because `Path.glob` over a missing folder yields nothing. |
| P09a-S089 | Exception during restore or a check (for example: no `schema_meta` table at L125; a file that is not a database; a missing column in a sample query, L78 to L81; a copy failure at L110) | FACT: the `try` at L231 has only a `finally` (L312), no `except`. INTERPRETATION: the exception propagates after clean-up; the report (L327) and the heartbeat (L330) are not reached; a traceback goes to stderr (the cron log); exit status 1. |
| P09a-S090 | Exception while selecting the backup (a file removed between glob and `stat`, L103) | FACT: L211 is outside the `try`. INTERPRETATION: the same result as P09a-S089: no report, no heartbeat, exit status 1. |
| P09a-S091 | Retry or restart | FACT: no retry; a re-run starts from the beginning and overwrites the same-day report (L342). |
| P09a-S150 | Report cannot be written (for example the output folder is not writable) | FACT: `_write_report` (L339 to L342) has no `try`, and its calls at L216 and L327 are outside any `try`. INTERPRETATION: the exception ends the run with a traceback on stderr and exit status 1; at L327 the temporary copy has already been removed (L312 to L325) and the heartbeat (L330) is not reached; at L216 no temporary folder exists yet. |

## 4. `scripts/backup_retention.py`

### 4.1 Purpose, arguments, environment, configuration

- P09a-S092 HISTORICAL (L3 to L12): "T2: category-aware backup reaper", replacing an older 02:00 `find -mtime +7 -delete` that covered the two daily categories only; count-based keep-N per category, newest first by modification time; "Monthly category DROPPED"; "Audit is LOG-ONLY — no table."
- P09a-S093 HISTORICAL (L14 to L24): the safety claims are dry-run by default, never delete the newest, scoped patterns with a realpath check, symlinks refused, unmatched files refused and logged, a sanity cap with a Telegram WARNING, and idempotence.
- P09a-S094 FACT (L247 to L252): arguments `--apply` (`store_true`), `--backups-dir` (string, default `DEFAULT_BACKUPS_DIR` = `ROOT/data_store/backups`, L39; help "(test override)"), `--max-delete` (int, default 10, L40). The value of `--max-delete` is not validated.
- P09a-S095 FACT: environment variable names read indirectly through `TelegramNotifier.from_env`: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHANNEL_PRIMARY` (`alerts/telegram_notifier.py` L288 to L289; None is returned if either is empty, L290 to L291); configuration key `alerts.telegram.enabled` in `config/system_config.yaml` (`alerts/telegram_notifier.py` L81 to L102: file `config/system_config.yaml` relative to the working directory, L92; key read L95 to L99; any error returns True, L101 to L102; called at L296). Values were not examined. The cron line sources `.env` (cron L25; path only).
- P09a-S096 FACT (L45 to L49): the categories are hard-coded; no configuration file supplies them.

### 4.2 Selection

| ID | Category pattern | Keep newest | Line | Comment in code (HISTORICAL) |
|---|---|---|---|---|
| P09a-S097 | `pre_*.db` | 20 | L46 | "deploy / ad-hoc rollback backups (incl. *_analytics.db)" |
| P09a-S098 | `trading_system-*.db` | 14 | L47 | "daily main-DB backups" |
| P09a-S099 | `analytics-*.db` | 14 | L48 | "daily analytics backups" |

- P09a-S100 FACT (L117 to L124): the backup folder path is resolved; a missing folder raises `NotADirectoryError`; `iterdir` lists direct entries only; candidates are regular files that are not symlinks; symlinks are collected separately.
- P09a-S101 FACT (L86 to L88, L127 to L128): names ending in `-wal` or `-shm` are sidecars; every other regular file, of any extension, is a "db file" for matching.
- P09a-S102 FACT (L134 to L149): for each category in order, names are matched with `fnmatch`; a file joins the first category it matches (L137, L143); a file whose resolved path is not under the folder is skipped (L140 to L141); members are sorted by `st_mtime`, newest first (L144); the first N are kept and the rest are delete candidates (L145).
- P09a-S103 INTERPRETATION: order is by modification time, not by the date in the file name; ties keep the `iterdir` order (Python's sort is stable), which is arbitrary.
- P09a-S104 FACT (L171): unmatched = db files matching no category (including any skipped by the path check) plus symlinks; they are never deleted and are logged as a warning (L269 to L271) and listed in the report (L214 to L215).
- P09a-S105 INTERPRETATION (L123): subfolders such as `data_store/backups/evidence/` are neither candidates nor unmatched, because `is_file()` is False for a folder.
- P09a-S106 HISTORICAL: `docs/06_deployment_guide.md` L208 documents a manual backup named `manual_<stamp>.db`. INTERPRETATION: such a name matches no category, so it would be listed as unmatched on every run and never pruned.
- P09a-S107 FACT: producers in code of names these categories match: the cron jobs `db_backup` and `analytics_backup` (cron L19, L22), and `scripts/backfill_closure_source_w8.py` L134 (`pre_w8_backfill_<stamp>.db`, owner A12; see part P08b). A search of `deploy/hooks/`, `deploy/tools/` and `deploy/install_vm_services.sh` for "backup" found nothing.
- P09a-S151 FACT (path patterns only; nothing opened): the retention selection is limited to direct regular files of `data_store/backups` (L121 to L123) matched by `pre_*.db`, `trading_system-*.db` or `analytics-*.db`, or ending in `-wal` or `-shm` (L86 to L88, L134 to L145, L157 to L169); the drill selects only `trading_system-*.db` in its backup folder (drill L102). `.env`, `config/accounts.csv` and the broker session token file under `data_store/session/` (path from `main.py` L134) lie outside `data_store/backups`, so none of the three scripts selects them by path. Whether the SQLite backup copies hold credential material in their tables is not examined here (OPEN QUESTION 10; stopped: security restriction).

### 4.3 Sidecar files (`-wal`, `-shm`)

- P09a-S108 FACT (L153 to L169): a sidecar is left alone when its base `.db` is kept, or when the base is present but unmatched; when the base is a delete candidate or absent, a `-wal` larger than 0 bytes is refused (kept and reported), and any other sidecar (`-shm` of any size, or a 0-byte `-wal`) becomes a delete candidate.
- P09a-S109 FACT (L99 to L103): `_safe_size` returns 0 when `stat` fails. INTERPRETATION: a `-wal` whose `stat` fails is treated as 0 bytes and becomes a candidate; if its later `unlink` fails, `execute` records it as skipped.
- P09a-S152 FACT: sidecar candidates are not restricted to the category patterns: a `-shm`, or a `-wal` of 0 bytes, whose base name is absent from the folder is a delete candidate whatever that base name is (L157 to L169); the path-containment check (L140 to L141) is applied to category members only. INTERPRETATION: such sidecars are direct, non-symlink entries of the folder (L121 to L123), so they lie inside it even without that check. HISTORICAL: the header says a file matching no category is refused and logged (L19 to L21).

### 4.4 Deletion predicate, scope and safety guards

- P09a-S110 FACT (L172 to L176): `total_delete` = category delete candidates + sidecar delete candidates; `abort` = `total_delete > max_delete`.
- P09a-S111 FACT (L180 to L200): `execute` deletes nothing unless `apply` is True and `abort` is False; it deletes base `.db` candidates first, then sidecars, with `Path.unlink`; `FileNotFoundError` is recorded as skipped "already-gone"; any other `OSError` as skipped "locked/error" with a warning; the loop continues.
- P09a-S112 FACT (L187 to L199): `execute` does not repeat the symlink, path-containment or modification-time checks at deletion time. INTERPRETATION: those checks hold only at plan time.
- P09a-S113 FACT: no check is made whether a candidate is open in another process. INTERPRETATION: on Linux, unlinking an open file succeeds. Each category keeps at least its newest file because every keep value is 1 or more (L46 to L48); the keep values can be changed only through the `categories` function argument (L107), not on the command line.
- P09a-S114 FACT (L172, L176): the cap counts files, sidecars included, not bytes.

### 4.5 Modes, logging, alerts, heartbeat, exit codes

- P09a-S115 FACT: the logger is `core.logger.get_logger("backup_retention")` (L254 to L255); `get_logger` attaches no handlers (`core/logger.py` L266 to L274); the script never calls `setup_logging`; a repository-wide `git grep` (tests excluded) finds `setup_logging(` called only in `main.py` L2178, and `logging.basicConfig` called only in other scripts and modules outside this import chain (`core/logger.py` mentions it only in a docstring, L346 to L347), none of which is in this script's import chain (`core/logger.py`, `core/state_store.py`, `core/migrations.py`, `core/db_connect.py`, `core/exceptions.py`, `core/time_authority.py`, `alerts/telegram_notifier.py`, `alerts/critical.py`, `utils/cron_heartbeat.py`).
- P09a-S116 INTERPRETATION (Python logging semantics): with no handler configured, WARNING and higher records reach stderr through Python's last-resort handler, and INFO and DEBUG records are dropped. So the per-line report log (L266 to L267), the audit line (L274, L284, L291) and the Telegram-failure debug line (L243) would not appear anywhere, while the warnings and errors (L199, L260, L270, L283) reach stderr; the printed report (L265) goes to stdout. Under cron both streams go to `logs/cron-backup-retention.log` (cron L25). HISTORICAL: the header says "Audit is LOG-ONLY — no table" (L12).
- P09a-S117 FACT (L273 to L275): dry-run (no `--apply`) logs a DRYRUN audit line and returns 0, with no heartbeat, no Telegram and no deletion, even when `plan.abort` is True.
- P09a-S118 FACT (L257 to L262): an exception in `build_plan` is logged as an error, a message goes to stderr, and the exit code is 1; no heartbeat and no Telegram (both come later, from L278).
- P09a-S119 FACT (L279 to L287): `--apply` with `abort` logs an error and an audit line, sends a Telegram WARNING "Backup Retention ABORT", writes heartbeat status "FAILED" with the message cut to 200 characters, and exits 2.
- P09a-S120 FACT (L289 to L306): `--apply` without `abort` runs `execute`; status is "PARTIAL" if anything was skipped, else "SUCCESS"; a Telegram WARNING "Backup Retention" is sent only when something was deleted or skipped (L295 to L302); the heartbeat is written with that status (L304 to L305); the exit code is 0 for both statuses (L306).
- P09a-S121 FACT (L234 to L243): the Telegram helper returns silently when `from_env` gives None and swallows any exception (debug log); the severity is always "WARNING" (L240).
- P09a-S122 FACT (L278): `from utils.cron_heartbeat import record_heartbeat` is not inside a `try`. INTERPRETATION: an import failure there would end the run (traceback, exit status 1) before any deletion.
- P09a-S123 FACT: `record_heartbeat` never raises (`utils/cron_heartbeat.py` L80 to L95) and returns False if `data_store/trading_system.db`, relative to the working directory, does not exist (L81 to L82). INTERPRETATION: run from another directory, no heartbeat is written; the cron line changes to the project root first (cron L25).
- P09a-S149 FACT: both heartbeat calls (L286, L304 to L305) open the live database through `StateStore`, with the same open-time effects recorded for the drill in P09a-S062 (`init_analytics_schema` on `analytics.db`, the connection PRAGMAs, `executescript` of `core/schema.sql` with its `INSERT OR REPLACE` of `schema_version`; a newer stored version raises; an older one is refused with a CRITICAL log and a critical sentinel file). `record_heartbeat` swallows any such failure (`utils/cron_heartbeat.py` L94 to L95), so the exit code (0 or 2) is unchanged and no heartbeat row is written.

### 4.6 Routes

| ID | Route | What the code does |
|---|---|---|
| P09a-S124 | Normal `--apply`, nothing to delete | FACT: report printed, heartbeat "SUCCESS", no Telegram, exit code 0 (L289 to L306). |
| P09a-S125 | Normal `--apply` with deletions | FACT: files unlinked, Telegram WARNING, heartbeat "SUCCESS", exit code 0 (L187 to L193, L295 to L302, L304 to L306). |
| P09a-S126 | Partial failure (some `unlink` fails) | FACT: heartbeat "PARTIAL", the Telegram WARNING states the number of skipped files (L300 to L302), exit code 0 (L290, L306). |
| P09a-S127 | Sanity cap exceeded | FACT: nothing deleted, Telegram, heartbeat "FAILED", exit code 2 (L279 to L287). |
| P09a-S128 | Error while planning | FACT: exit code 1, no heartbeat, no Telegram (L257 to L262). |
| P09a-S129 | Retry or restart | FACT: no retry within a run and no state file; the next run plans again from the folder listing (L117 to L177). |
| P09a-S130 | Race | FACT: a file gone between plan and delete is skipped "already-gone", giving "PARTIAL" (L194 to L195, L290). INTERPRETATION: a file gone between `iterdir` and `stat` inside `build_plan` (L144, L148) raises `FileNotFoundError`, which takes route P09a-S128. |

## 5. Callers and dependencies (what crosses, owner topic)

| ID | Caller (path, lines) | Function | What it reads or writes | How | Owner topic |
|---|---|---|---|---|---|
| P09a-S131 | `scripts/backup_restore_drill.py` L40 | module level | reads the constant `EXPECTED_SCHEMA_VERSION` | Python import of `core.state_store` | A03 (part P03) |
| P09a-S132 | `scripts/backup_restore_drill.py` L331 to L332 | `run_drill` | inserts a `cron_heartbeat` row (`job_name`, `executed_at`, `status`, `duration_sec`, `message`) into `data_store/trading_system.db` | `record_heartbeat` then `StateStore.insert_cron_heartbeat` (`core/state_store.py` L3305 to L3325, INSERT at L3321 to L3324 inside `self.transaction()`) | A16 (`utils/cron_heartbeat.py`); storage A03 (part P05) |
| P09a-S133 | `scripts/backup_retention.py` L278, L286, L304 to L305 | `main` | the same insert, status "FAILED", "SUCCESS" or "PARTIAL" | the same path | A16; storage A03 |
| P09a-S134 | `scripts/backup_retention.py` L236 to L241 | `_telegram` | sends a WARNING message; reads two environment variable names and one configuration key (P09a-S095) | `TelegramNotifier.from_env` and `send` | A14 |
| P09a-S135 | `scripts/backup_retention.py` L254 to L255 | `main` | logger only | `core.logger.get_logger` | A15 |
| P09a-S136 | `core/evidence_contract.py` L319 to L321, L327, L330, L596, L697 | `evidence_path`, `failure_log_path`, the appenders | writes the source files that `backup_evidence.py` copies | `open(path, "a")` | A15 |
| P09a-S137 | `deploy/cron/trading-system.cron` L25, L28, L151 | cron lines | invoke the three scripts (P09a-S003 to P09a-S005) | cron | A16 |
| P09a-S138 | `scripts/output_retention.py` L52, L56 to L65 | comment only | declares `data_store/backups/` and `data_store/evidence/*.jsonl` out of its scope | comment (HISTORICAL) | A03 (part P09b) |

- P09a-S139 FACT: no other non-test code imports or calls the three scripts; `git grep` for their names, excluding tests, finds only the registry, the cron file, legacy documents, `scripts/output_retention.py` comments and the scripts themselves.

## 6. Changes after the last recorded deployment (`7d4970a`)

- P09a-S140 FACT: `7d4970a` (committed 2026-09-02 23:42 +0530) is an ancestor of the baseline `970aabf` (2026-09-11 02:05 +0530); 32 commits lie between them (`git log --oneline 7d4970a..HEAD`).
- P09a-S141 FACT: `scripts/backup_evidence.py` does not exist at `7d4970a` (`git cat-file -e 7d4970a:scripts/backup_evidence.py` fails).
- P09a-S142 FACT: `28ec9df` (2026-09-10 19:07 +0530; not an ancestor of `7d4970a`) creates `scripts/backup_evidence.py` (100 lines), adds the `evidence_backup` registry entry (15 lines) and its cron line (3 lines), and adds 6 lines to `scripts/output_retention.py`.
- P09a-S143 FACT (from the `4608b83` diff): the `28ec9df` version copied `signal_evidence_*.jsonl` only, copied straight onto the destination with `shutil.copy2` when the hashes differed, and copied once more after a SHA-256 mismatch, recording a failure if the second hash also differed.
- P09a-S144 FACT: `4608b83` (2026-09-10 21:00 +0530; not an ancestor of `7d4970a`) changes `scripts/backup_evidence.py` (71 insertions, 28 deletions, derived from `--stat`: 127 insertions and 28 deletions over two files, of which the test file has 56 insertions) and a test file (not traced). The change adds `PATTERNS` with `evidence_failures_*.jsonl`, `_is_prefix`, the temporary file with `os.replace`, the refusal when the backup is not a prefix, and removes the retry; the docstring gains the SAME-DISK paragraph and loses the statement that the script closes the disk-loss gap.
- P09a-S145 FACT: `e1952e4` (2026-09-11 01:45 +0530; not an ancestor of `7d4970a`) changes only the `evidence_backup` `script` description in `config/cron_registry.yaml` (adds "a SAME-DISK copy, NOT off-box") and a comment in `scripts/output_retention.py`; `scripts/backup_evidence.py` is unchanged by it.
- P09a-S146 FACT: `git diff 7d4970a HEAD` is empty for `scripts/backup_restore_drill.py` and `scripts/backup_retention.py`; their last changing commits, `f172171` (2026-06-14) and `c42e329` (2026-07-24), are ancestors of `7d4970a`.
- P09a-S147 HISTORICAL: the `28ec9df` message says "Nothing was installed to any live crontab. Registry + canonical only, in this tree, unpushed."; the `4608b83` message says "Batch 1: NOT deployed to either VM."; the `c42e329` subject ends "(NOT pushed)".
- P09a-S148 UNKNOWN / NOT ESTABLISHED: whether `scripts/backup_evidence.py` or the `evidence_backup` cron line was ever installed on any machine.

## Concerns for the AUDIT (neutral)

1. `evidence_backup` is declared `monitored: true` (registry L74), which by default means heartbeat-based detection (`core/cron_registry.py` L131 to L147), but `backup_evidence.py` writes no heartbeat (P09a-S031).
2. `backup_evidence.py` exits 0 with nothing copied when `data_store/evidence` is missing (L90 to L91).
3. `backup_evidence.py` has `mkdir` and glob outside its `try` (L92 to L93), while the docstring says it never raises into cron (L37).
4. The evidence backup keeps a single generation per file, accepts a copy that ends mid-line (L110), is not pruned by any script read here, and is not exercised by the restore drill.
5. A killed `backup_evidence.py` run can leave `*.tmp-<pid>` files that no code removes (P09a-S049).
6. `backup_evidence.py` hashes the whole source and backup of every file on every run (L98); the reading cost grows with file size.
7. The drill records heartbeat "SUCCESS" whatever its verdict (L332; `utils/cron_heartbeat.py` L57), records no heartbeat when no backup is found (L217), and records neither report nor heartbeat when any step raises (P09a-S089, P09a-S090); its registry entry is `monitored: true` (L749).
8. The drill documents exit code 2 (L23) but never produces it (L377).
9. The drill tests only the newest `trading_system-*.db` by modification time, with no age check; `analytics-*.db` and `pre_*.db` are never drilled; the restored copy excludes sidecar files (L102, L110).
10. The drill's WAL step and sample queries do not affect the verdict, and its foreign-key step covers two relations (L84 to L97, L292 to L303).
11. The drill writes its report by default into `docs/`, a tracked, non-ignored folder (L359; `.gitignore` L42), dated by naive local time (L202).
12. The drill sends no alert on failure; under cron `--quiet` leaves only stderr in the cron log, and its cron line, unlike the other backup lines, writes no `.done` marker (cron L151).
13. The drill opens the live database through `StateStore` to write its heartbeat, which runs `_initialize_schema` on open (P09a-S062; see parts P01 and P03). The same applies to `backup_retention.py` (L286, L304 to L305; P09a-S149).
14. `backup_retention.py` logs its report and audit line at INFO with no handler configured (P09a-S116), while its header says the audit is log-only (L12).
15. `backup_retention.py` exits 0 on "PARTIAL", 2 on abort and 1 on a planning error; the planning-error route writes no heartbeat (L257 to L262).
16. `backup_retention.py` orders by modification time, applies its symlink and containment checks at plan time only, does not check whether files are in use, and does not validate `--max-delete` (L144, L187 to L199, L250).
17. Files matching no category (for example the documented `manual_<stamp>.db` name) are never pruned and are warned on every run (L171, L269 to L271).
18. Dry-run returns 0 even when the plan would abort (L273 to L275).
19. HISTORICAL procedures in `docs/05_incident_response.md` L223 to L231 and `docs/06_deployment_guide.md` L213 to L215 restore by `cp` of a daily backup over `data_store/trading_system.db`; the incident procedure then runs the drill, which tests the newest backup file, not the restored live database. Those lines do not mention `-wal` or `-shm` files beside the live database.
20. No line read here (the three scripts and the backup cron lines) copies any artefact to another machine; every backup destination is `data_store/backups` in the project tree.
21. Orphan sidecars of any base name are reaped (L157 to L169; P09a-S152), while the header says unmatched files are refused (L19 to L21).

## Questions about intent (OPEN QUESTION, for the project owner)

1. OPEN QUESTION: should a failed drill, or a drill that finds no backup, have recorded a FAILED heartbeat or raised an alert?
2. OPEN QUESTION: was exit code 2 for "no backups found" meant to be implemented?
3. OPEN QUESTION: were the `analytics-*.db` and `pre_*.db` backups meant to be drilled as well?
4. OPEN QUESTION: was the drill report meant to be written into `docs/` on the production machine?
5. OPEN QUESTION: was `backup_evidence.py` meant to write a heartbeat, given `monitored: true`?
6. OPEN QUESTION: was an off-box copy of the backups intended (the docstring calls it an OPEN item)?
7. OPEN QUESTION: was a retention rule intended for `data_store/backups/evidence/`?
8. OPEN QUESTION: was the retention audit line meant to reach a log file?
9. OPEN QUESTION: should retention order by modification time or by the date in the file name?
10. OPEN QUESTION: whether any table copied into the SQLite backups or drill copies holds credential material was not examined (stopped: security restriction). Should the schema parts label it?

## UNKNOWN / NOT ESTABLISHED

1. Whether any of the three scripts, or the two `sqlite3 .backup` jobs, ever ran, on which machine and with what result: no log, marker, report, heartbeat row or backup file survives.
2. The machines' time zone, and so the real clock time of the declared schedules (P09a-S008, P09a-S012).
3. Whether `data_store/backups` was on a separate filesystem or disk from `data_store`.
4. The journal mode of the files produced by the `sqlite3 .backup` jobs, and so what the drill's WAL step actually exercised.
5. The version of `<VENV_PYTHON>`; P09a-S116 assumes standard Python 3 logging behaviour.
6. Whether the evidence writer was active at 01:10, when the evidence copy is declared.
7. Whether `scripts/backup_evidence.py` and its cron line were ever installed (P09a-S148).
8. The temporary folder the drill used (it depends on the runtime environment).
9. Whether any `pre_*` backup existed on any machine.

## Boundary handoffs (owner topic: what crosses)

- A16: the schedule declarations (P09a-S003 to P09a-S012); heartbeat rows written by the drill and retention; the Cron Officer's detection method for `monitored` jobs; the missing `.done` marker on the drill line; the time zone.
- A15: production of the evidence JSONL files (`core/evidence_contract.py`); logger handler set-up (`core/logger.py`); the drill report as an output artefact; other non-test readers of `data_store/backups` that judge backup presence or size (`ops/control_tower/disk.py` L42, `ops/control_tower/size_logger.py` L52, `ops_dashboard/backend/readers/host_reader.py` L209 to L216, `scripts/system_manager.py` L413; pointer for part P08a).
- A14: the Telegram WARNING messages from `backup_retention.py` and the environment variable names they use; a critical sentinel written by `StateStore._refuse_migration` when either script's heartbeat meets a pending migration (P09a-S081, P09a-S149).
- A17: the `.env` sourcing in the cron lines; the virtual-environment interpreter; whether the project folder was a git working tree; off-box backup provision.
- A12: `scripts/backfill_closure_source_w8.py`, a producer of a `pre_*` backup that the retention category covers.
- A03 other parts: P01 (StateStore opening, connections, journal mode); P03 (`_initialize_schema` when the heartbeat opens the live database); P05 (`insert_cron_heartbeat`); P02a and P02b (the tables in `EXPECTED_TABLES` and the declared foreign keys); P07 (`analytics.db` and its backup); P08a (the `sqlite3 .backup` cron lines, `cron_marks`, log files); P08b (the `pre_w8_backfill` backup); P09b (`output_retention.py`, `db_retention.py`, `wal_checkpoint.py`).
- A19: the test file changed by `4608b83` (not traced).
