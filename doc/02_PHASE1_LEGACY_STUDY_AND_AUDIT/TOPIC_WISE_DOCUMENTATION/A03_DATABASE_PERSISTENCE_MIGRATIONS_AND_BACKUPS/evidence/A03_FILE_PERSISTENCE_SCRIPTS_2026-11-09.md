# A03 evidence: File persistence under data_store/ and logs/: scripts

**Status:** APPROVED — evidence for the A03 STUDY, approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32)
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09: written by a read-only helper as STUDY part P08b, checked statement by statement by a separate helper, and corrected by a third pass (STUDY, section 1.5). Approved by Rama on 2026-11-11 with the A03 topic package (Decision Register, D-32): status marked APPROVED; content unchanged.
**Purpose and scope:** The files written and read under `data_store/` and `logs/` by 53 scripts (the six A03 scripts excluded). Statement IDs `P08b-Snnn` are kept for traceability; the STUDY cites them.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone; nothing in it was written or run.

## 0. Scope and method

- P08b-S001 FACT: helper pass: before any reading, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline) and `git status --short` returned nothing (clean tree). After the work, the same two commands again returned the baseline commit and an empty status.
- P08b-S002 FACT: scope is the 53 files in the coordinator's file list for this part (all under `scripts/`, including eight files under `scripts/preflight/`). The six A03 scripts (backup, retention, restore drill, WAL checkpoint) are not in the list; they are parts P09a and P09b.
- P08b-S003 FACT: for each of the 53 files I read the module docstring, the path constants, the argument defaults, every function that opens, writes, renames, deletes, locks or stats a file under `data_store/` or `logs/` or names a database file, and the `main` and `_cron_main` entry points. The line ranges actually relied on are the ones cited in each statement below.
- P08b-S004 FACT: tools used: `grep -nE` over each file with a file-I/O pattern set (path fragments, `open(`, `write_text`, `read_text`, `json.dump`, `os.replace`, `rename`, `chmod`, `umask`, `fsync`, `flock`, `fcntl`, `sqlite3`, `unlink`, `mkdir`, `glob`, `shutil`, `FileHandler`, `basicConfig`, `tempfile`, `StateStore(`, `connect(`, `load_dotenv(`), then `sed -n` reads of the cited ranges; `git grep` across the repository (tests excluded) to find other readers and writers of each file family; `awk` over the text of `config/cron_registry.yaml` and `config/system_config.yaml` to locate keys. No Python `ast` parsing was used. No legacy code, test, SQL or shell file was executed or imported.
- P08b-S005 FACT: context files read only to resolve pointers (not in this part's scope): `core/logger.py` L260 to L460; `core/state_store.py` L172 to L245; `core/db_connect.py` L93 to L137; `alerts/critical.py` signatures and docstring L52 to L170; `utils/cron_heartbeat.py` signatures (L55 to L61, L98 to L125, L176 to L179); `scripts/monitoring_canary.py` L166 to L185; `scripts/output_retention.py` L40 to L125; `scripts/backup_retention.py` L1 to L50; `core/strategy_direction.py` L43 to L44; `deploy/cron/trading-system.cron` (redirect and marker fields only); `deploy/systemd/*.service` and `cron-watchdog.timer` (ExecStart, WorkingDirectory, output, UMask lines); `config/system_config.yaml` L372 to L392 and L564 to L631; `config/security.yaml` L95, L120 to L121, L147 to L155; the master index Appendix A for owner topics.
- P08b-S006 FACT (security): no `.env` file, `config/accounts.csv`, token file, key file or other credential file was opened. Where a script reads or writes such a file, only the path or path pattern and environment-variable NAMES are recorded. Account identifiers are written `<ACCOUNT_ID>`; absolute machine home paths are written "the operator's home directory".
- P08b-S007 FACT: runtime limit: no database, log, backup, sentinel or crontab from either legacy machine survives. Every statement below says what the code does when called, never that it ran.
- P08b-S286 FACT: checker pass (independent), as stated in its check file: before and after its work, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty. The check file discloses no scratch files written outside its work folder.
- P08b-S287 FACT: corrector pass: before work, `git rev-parse HEAD` on the local read-only clone returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and `git status --short` was empty; after writing this file and the corrections log, the same two checks returned `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and an empty status.
- P08b-S288 FACT: corrector method: every non-CORRECT statement and every omission in the check was verified by reading the cited lines at the baseline as text with `grep`, `sed` and `awk`: `utils/cron_heartbeat.py` L55 to L61, L113 to L125, L176 to L180; the heartbeat, `HeartbeatTimer`, `skip_if_non_trading_day` and `--db` lines of every script in scope; `scripts/refresh_instruments.py` L206 to L218; `scripts/alert_watcher.py` L155 to L164, L388 to L481, L505 to L722; `scripts/security_monitor.py` L176 to L226, L630 to L840 (state keys), L1151 to L1222, L1336 to L1396; `scripts/system_manager.py` L790 to L800, L912 to L936, L1340 to L1349; `core/strategy_direction.py` L40 to L46; `scripts/disk_monitor.py` L74 to L215; `scripts/cron_officer.py` L362 to L371, L437 to L460, L826 to L848; `scripts/reconstruct_excursions.py` L328 to L344, L398 to L404, L500 to L507; the sentinel-writing lines of `copy_gate.py`, `forward_shadow_record.py`, `gemini_log_review.py`, `liveness_probe.py`, `strategy_registry_officer.py`; `core/account_registry.py` (helper names and L277 to L360); `alerts/telegram_notifier.py` L199 to L201, L271 to L297, L317 to L340, L348 to L500; `scripts/generate_crontab.py` L44 to L70; `deploy/cron/trading-system.cron` L16, L46, L52, L58, L73, L82, L97 and `config/security.yaml` L118 to L135, both read with home paths, addresses and account identifiers masked on screen; `deploy/systemd/*.service` (output and `UMask` lines, `cron-watchdog.service` in full with the home path masked); the paper branches of `compute_strategy_metrics.py`, `eod_broker_reconcile.py`, `reconcile_pnl.py`, `reconcile_positions.py`; `scripts/fetch_daily_candles.py` L276 to L281; `scripts/auto_refresh_token.py` L288 to L304, L334 to L382. No legacy code was run or imported; no `.env`, token, key or `config/accounts.csv` content was opened; nothing was written inside the clone or outside the two output files of this pass.

## 1. Part summary

- P08b-S008 FACT: no script in this part calls `core.logger.setup_logging()`; the only caller in the repository is `main.py` L2178 (`setup_logging(Path("logs"))`). Scripts therefore never write the `logs/system_*`, `trades_*`, `reconciler_*` or `debug_*` files themselves, except when imported into the `main.py` process (`scripts/healthcheck_server.py`, `scripts/zerodha_login.py`, `scripts/preflight/startup_hook.py`; `main.py` L91, L106, L1875, L4088).
- P08b-S009 FACT: one script opens its own log file handler: `scripts/alert_watcher.py` `_setup_watcher_log` L462 to L481 writes `logs/alert_watcher_<YYYY-MM-DD>.log`.
- P08b-S010 FACT: the scripts in scope write the non-database file families under `data_store/` listed in sections 3.1 to 3.10, plus ad-hoc database files (`data_store/backups/pre_w8_backfill_<stamp>.db`, `data_store/t2_proof_<ts>/t2_proof.db`), and one family under `logs/` besides the watcher log (`logs/preflight_autofix_<YYYY-MM-DD>.jsonl`).
- P08b-S011 FACT: one script deletes files under `logs/`: `scripts/disk_monitor.py` `_cleanup_old_files` L104 to L154 (also `reports/output/`), only when disk usage reaches the critical threshold.
- P08b-S012 FACT: three main write disciplines appear: temporary file plus `os.replace`, append-mode open, and plain in-place overwrite (table 2.2); only one writer calls `fsync` (`scripts/preflight/sentinel.py` L85).

## 2. Cross-cutting conventions

### 2.1 How paths are anchored

| ID | Script (owner) | Anchor of its data_store or logs paths | Lines |
|---|---|---|---|
| P08b-S013 | alert_watcher.py (A14) | Config values `alerts.sentinel_dir` = "data_store", `alerts.watcher_lock_path` = "data_store/alert_watcher.lock", `alerts.watcher_log_path` = "logs/alert_watcher.log": relative strings, resolved against the process working directory | `config/system_config.yaml` L380 to L385; `scripts/alert_watcher.py` L501 to L503, L803 to L806 |
| P08b-S014 | security_monitor.py (A17) | State, operator baseline and last-run anchored to the repository root (`_ROOT`); `sentinel_dir` from `config/security.yaml` L121 is relative "data_store"; copy audit log is an absolute path under the operator's home directory from `config/security.yaml` L154, default anchored | `scripts/security_monitor.py` L61, L71, L75, L79, L143, L148, L151 to L183 |
| P08b-S015 | copy_gate.py (A17) | Token and audit defaults anchored to `_ROOT`; overridden by absolute paths under the operator's home directory in `config/security.yaml` L153 to L154; `sentinel_dir` relative "data_store" (L155) | `scripts/copy_gate.py` L56 to L57, L75 to L77, L80 to L97 |
| P08b-S016 | approve_ssh_keys.py (A17) | Imports the anchored constants of security_monitor | `scripts/approve_ssh_keys.py` L31 to L38 |
| P08b-S017 | preflight/orchestrator.py, sentinel.py, startup_hook.py, autofix.py (A20) | Relative defaults: `Path("data_store/trading_system.db")`, `Path("data_store/preflight/today.json")`, `Path("data_store")`, `Path("logs")` | orchestrator L152 to L153, L160, L164; sentinel L23; startup_hook L71 to L76; autofix L46 |
| P08b-S018 | preflight/checks/recovery.py, vm_health.py, security.py (A20) | Project root inferred from the DB path (`ctx.db_path.resolve().parent.parent`), or the DB's parent directory | recovery L16 to L17; vm_health L61 to L63; security L50 to L52 |
| P08b-S019 | cron_officer.py (A16) | `_MARKS_DIR`, `_AUDIT_DIR` anchored to `_ROOT`; `--db-path` default relative; `_email_delivery_health_line` default `Path("data_store")` relative | L49 to L50, L154, L866 |
| P08b-S020 | check_cron_drift.py (A16) | `--db-path` and marks directory defaults relative | L58, L175 |
| P08b-S021 | cron_watchdog.py (A16) | DB and sentinel directory anchored to `_ROOT` | L42, L67 |
| P08b-S022 | liveness_probe.py (A15) | State directory from config `alerts.sentinel_dir` (relative) with fallback `Path("data_store")`; DB default relative | L138, L201, L292 to L299 |
| P08b-S023 | healthcheck_server.py (A15) | Token path relative `Path("data_store/session/zerodha_token.json")` | L40 |
| P08b-S024 | zerodha_login.py (A04) | Token path default relative `Path("data_store/session/zerodha_token.json")` | L42 |
| P08b-S025 | auto_refresh_token.py (A04) | Token path default anchored to `_ROOT` | L61 |
| P08b-S026 | system_manager.py (A15) | Report and artefact paths anchored to `_ROOT`; `--db-path` default relative | L1299, L1324 |
| P08b-S027 | replay_signals.py (A19), trade_journal.py (A15), premarket_healthcheck.py (A20) | `--db` or `--db-path` default relative "data_store/trading_system.db" | replay L227; journal L150; premarket L186 |
| P08b-S028 | t2_cnc_gtt_realtest.py (A19) | Throwaway DB and token path relative | L118 to L119, L160, L190 |
| P08b-S029 | All other scripts in scope that name `data_store/` | Anchored to the repository root via `Path(__file__).resolve().parent.parent` | e.g. `eod_cleanup.py` L26, L278; `fetch_daily_candles.py` L37 to L39; `forward_shadow_record.py` L41 |

- P08b-S030 INTERPRETATION: relative paths resolve against the process working directory. For cron-launched scripts the generated command line starts with `cd <project root> &&` (`scripts/generate_crontab.py` `_ENV_PREFIX` L48 to L53), and the systemd units set `WorkingDirectory` to the project root (`deploy/systemd/alert-watcher.service` L16, `security-watcher.service` L15, `trading-watchman.service` L10, `cron-watchdog.service` L14), so under those launchers relative and anchored paths name the same files. A manual run from another directory would not.
- P08b-S031 FACT: the heartbeat helper used by many scripts has its own relative DB default `Path("data_store/trading_system.db")` (`utils/cron_heartbeat.py` `record_heartbeat` L61, `HeartbeatTimer.__init__` L119, `skip_if_non_trading_day` L179). Fourteen scripts in scope accept a DB option but record their heartbeat without `db_path`, so the heartbeat goes to the relative default, not to the given path: through `record_heartbeat`, `eod_verify.py` L232 (`--db` L187); `capture_metrics_baseline.py` L326 (`--db` L60); `forward_shadow_record.py` L185 and L266 (`--db` L140); `gemini_data_integrity_check.py` L365 (`--db` L77); `gemini_premarket_brief.py` L281 (`--db` L65); `gemini_trade_coach.py` L279 (`--db` L66); `eod_broker_reconcile.py` L423 to L424 (`--db` L332); `premarket_healthcheck.py` L216 (`--db-path` L186); and through `HeartbeatTimer(name, alert=True)`, `compute_strategy_metrics.py` L341 (`--db` L52), `eod_cleanup.py` L313 (`--db` L40), `fetch_fno_ban.py` L367 (`--db` L249), `reconcile_positions.py` L443 (`--db` L56), `strategy_registry_officer.py` L295 (`--db-path` L269), `trade_journal.py` L169 (`--db` L150). Every `skip_if_non_trading_day` call in scope also uses the helper's default (none passes `db_path`), including `sr_detector_backfill.py` L143 (`--db` L102). `auto_refresh_token.py` `_heartbeat` L293 to L304 also uses the default (it has no DB option). Only four scripts pass `db_path` explicitly: `check_cron_drift.py` L219; `cron_officer.py` L921 to L944; `reconstruct_excursions.py` L416; `system_manager.py` L1343 to L1348.

### 2.2 Write-method inventory

| ID | Method | Writers (file:line) |
|---|---|---|
| P08b-S032 | Temporary file in the same directory plus `os.replace` (or `Path.replace`), no fsync | `alert_watcher.py` `_save_attempts` L153 to L158, `_save_smtp_state` L340 to L348, `_write_degraded_marker` L439 to L451, `_write_heartbeat` L731 to L743; `security_monitor.py` `save_state` L623 to L627, `_write_last_run_status` L1290 to L1293; `approve_ssh_keys.py` L115 to L118; `copy_gate.py` `CopyGate.write_token` L186 to L191; `refresh_instruments.py` `_write_csv` L206 to L218 (temp `.csv.tmp`, `Path.replace` L215; temp unlinked and exception re-raised on failure, L216 to L218; writes under `config/`, outside these folders) |
| P08b-S033 | `tempfile.mkstemp` in the target directory, write, `flush`, `os.fsync`, `os.replace`, stray-temp `unlink` in `finally` | `preflight/sentinel.py` `write` L71 to L93 (the only fsync in scope) |
| P08b-S034 | Append-mode open, one JSON line per record, no lock, no fsync | `security_monitor.py` `_append_copy_audit` L1224 to L1235; `copy_gate.py` `CopyGate.audit` L245 to L263; `preflight/autofix.py` `_audit` L67 to L86; `forward_shadow_record.py` L259 to L262; `logging.FileHandler` (append) in `alert_watcher.py` L477 |
| P08b-S035 | Plain overwrite in place (`open(..., "w")` or `write_text`) | `fetch_daily_candles.py` L211 to L217 (candle CSV); `cron_officer.py` L454 to L455 (`job_list_<date>.json`); `backfill_closure_source_w8.py` L161 to L170 (receipt); `alert_watcher.py` L131 (lock file); `cron_officer.py` L612 (self-test probe, then unlinked L613) |
| P08b-S036 | `os.open(..., O_WRONLY or O_CREAT or O_TRUNC, 0o600)` then `json.dump`, then `chmod 0o600`; parent directory `chmod 0o700`; no temporary file | `zerodha_login.py` `save_token` L132 to L176 |
| P08b-S037 | `os.open(..., O_CREAT or O_EXCL or O_WRONLY)` exclusive create (lock) | `reconstruct_excursions.py` `_acquire_lock` L348 to L376 |
| P08b-S038 | SQLite online backup API into a new file | `backfill_closure_source_w8.py` `_take_backup` L125 to L153 |
| P08b-S039 | File deletion | `disk_monitor.py` L147 (logs/ and reports/output/); `alert_watcher.py` L128, L137, L455; `copy_gate.py` L195; `reconstruct_excursions.py` L373, L381; `preflight/sentinel.py` L90 (stray temp); `cron_officer.py` L613 |

- P08b-S040 INTERPRETATION: `os.replace` within one directory is an atomic rename on POSIX, so readers see the old or the new file, never a mix; without an fsync of the file and its directory, a power loss shortly after the rename can still lose or empty the new content (SQLite-independent filesystem semantics).
- P08b-S041 INTERPRETATION: `tempfile.mkstemp` creates its file with mode 0600, and `os.replace` carries that mode to the target, so `data_store/preflight/today.json` ends up owner-only (Python semantics).

### 2.3 Permissions

- P08b-S042 FACT: only two scripts in scope set permissions: `zerodha_login.py` `save_token` sets the session directory to 0700 (L148 to L151) and the token file to 0600 (L170, L173 to L176); `preflight/checks/recovery.py` `_ensure_dir` sets `logs/` and `data_store/cron_marks/` to 0700 (L20 to L33), only when the auto-fix `ensure_dir_perms` runs.
- P08b-S043 FACT: no script in scope calls `os.umask`, and none of the systemd units under `deploy/systemd/` sets `UMask=` (grep over the unit files found no such line).
- P08b-S044 INTERPRETATION: every other file in section 3 is created with the process umask default (commonly 0644 for files), including the security state, the SSH baseline override, the copy token and the copy audit log.

### 2.4 Concurrency control

- P08b-S045 FACT: `scripts/alert_watcher.py` `_acquire_lock` L109 to L132 checks `lock_path.exists()`, reads a PID, tests liveness, unlinks a stale lock, then writes its own PID with `write_text`; there is no exclusive-create flag, `flock` or `fcntl`.
- P08b-S046 FACT: `scripts/reconstruct_excursions.py` `_acquire_lock` L348 to L376 uses exclusive create; on `FileExistsError` it reads the PID, checks liveness with `utils.instance_lock._pid_is_alive`, unlinks a stale lock and retries once (loop of two).
- P08b-S047 FACT: no other writer in scope takes a lock; the read-modify-write cycles on `data_store/preflight/today.json` (`orchestrator.py` L213 to L218), `data_store/security_state.json` (`security_monitor.py` L1358 to L1391), `data_store/alert_watcher_attempts.json` (`alert_watcher.py` L508 to L719) and `data_store/liveness_alarm_state.json` (`liveness_probe.py` L233 to L243) are unlocked.

## 3. File-family register

Columns: path or pattern; format; writer and method; readers; naming, retention and clean-up; behaviour when the folder or file is missing or corrupt, or the write fails; owner topic of the writing script.

### 3.1 Alert-watcher and liveness state (data_store/ root)

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S048 | `data_store/alert_watcher.lock` (config `alerts.watcher_lock_path`) | Text, one PID | `alert_watcher.py` `_acquire_lock` L130 to L131 (`mkdir`, `write_text`); removed by `_release_lock` L135 to L137 in `main`'s `finally` L834 to L835 | `alert_watcher.py` L117 to L118 | Fixed name; removed on normal exit; no other clean-up in scope | Unreadable PID treated as no PID and overwritten (L119 to L120, L130 to L131); live PID: watcher exits 0 (L808 to L810); a write failure raises out of `main` (no handler around L131) | A14 |
| P08b-S049 | `data_store/alert_watcher_attempts.json` | JSON object, sentinel file name to attempt count | `alert_watcher.py` `_save_attempts` L153 to L158 (temp `alert_watcher_attempts.tmp` plus `Path.replace`), called at L719 after pruning L718 | `alert_watcher.py` `_load_attempts` L144 to L150 | Fixed name; entries pruned to still-pending `.flag` names each pass (`_prune_attempts` L161 to L164) | Missing or corrupt: empty dict (L145 to L150); write failure raises (no handler) | A14 |
| P08b-S050 | `data_store/alert_watcher_smtp_state.json` | JSON `consecutive_auth_fails`, `last_fail_iso` | `alert_watcher.py` `_save_smtp_state` L340 to L348 (temp plus `os.replace`), via `_record_smtp_failure` L366 to L369 and `_reset_smtp_state` L372 to L373 | `alert_watcher.py` `_load_smtp_state` L330 to L337 | Fixed name; reset to zero on a healthy pass L713 to L714 | Missing or corrupt: zero state (L332 to L337); `OSError` on write swallowed (L347 to L348) | A14 |
| P08b-S051 | `data_store/alert_watcher_degraded.json` | JSON `degraded`, `reason`, `since`, `last_via_telegram`, `last_stuck` | `alert_watcher.py` `_write_degraded_marker` L439 to L451 (temp plus `os.replace`); deleted by `_clear_degraded_marker` L454 to L455 | `cron_officer.py` `_email_delivery_health_line` L154 to L171; `deploy_assert.py` `assert_monitoring` L70 to L75 (existence only); outside scope: `scripts/monitoring_canary.py` L116 | Presence means degraded; cleared only on a pass that reaches L711 to L715 | Write `OSError` logged (L450 to L451); readers treat absence as healthy | A14 |
| P08b-S052 | Watcher heartbeat file (config key `alerts.watcher_heartbeat_path`) | Text, one IST ISO timestamp | `alert_watcher.py` `_write_heartbeat` L731 to L743 (temp plus `os.replace`), each `--loop` pass L767 | None found in scope | Path is `None` unless configured (L816 to L817; default `None` in `core/config_loader.py` L1109); the key is absent from `config/system_config.yaml` L379 to L392 | Any exception logged as warning (L742 to L743) | A14 |
| P08b-S053 | `data_store/critical_alert_<id>.flag` and its `.delivered`, `.failed` renames | JSON sentinel (writer in `alerts/critical.py`; see part P08a) | Written via `alerts.critical.write_critical_sentinel` by: `copy_gate.py` L295; `cron_officer.py` L845; `cron_watchdog.py` L60; `forward_shadow_record.py` L275; `gemini_log_review.py` L269; `liveness_probe.py` L285; `preflight/deliver.py` L78; `reconstruct_excursions.py` L402, L505; `security_monitor.py` L1217; `strategy_registry_officer.py` L210; `system_manager.py` L932. Direct `write_critical_sentinel` callers only; indirect writes through `alerts.telegram_notifier.TelegramNotifier.send` are row P08b-S289. Renamed by `alert_watcher.py` via `mark_delivered` L591, L642 and L429 (Telegram fallback, `_telegram_fallback_batch`) and `mark_failed` L541, L611, L663, L690 | `alert_watcher.py` `list_pending_sentinels` L510, L705 and in `_prune_attempts` L163; `preflight/checks/recovery.py` `AlertBacklogCheck` L102 to L103 (glob count); `system_manager.py` L482 to L483 (glob count) | See part P08a for naming; delivered-flag retention is a crontab line (`deploy/cron/trading-system.cron` L31, A16 boundary) | Corrupt sentinel: `mark_failed` with reason "corrupt", skipped under `--dry-run` (L536 to L544) | A14 (format); callers' owners in section 10 |
| P08b-S054 | `data_store/liveness_alarm_state.json` (directory from `alerts.sentinel_dir`) | JSON `alarmed_for`, `iso` | `liveness_probe.py` `probe_liveness` L243 calls `scripts.monitoring_canary._save_service_state` (temp plus `os.replace`, `OSError` swallowed: `monitoring_canary.py` L175 to L185) | `liveness_probe.py` L233 via `_load_service_state` (`monitoring_canary.py` L166 to L172) | Fixed name; overwritten only when an alarm fires (L242 to L243) | Missing or corrupt: empty dict; write failure silent | A15 |
| P08b-S055 | `data_store/.cron_officer_selftest.tmp` (in the resolved sentinel directory) | Text "ok" | `cron_officer.py` `_alert_path_health` L609 to L613 (write then unlink) | Same function | Transient probe | Any exception reported as "sentinel-dir: NOT writable" (L615 to L616) | A16 |
| P08b-S289 | `data_store/critical_alert_<id>.flag`, written indirectly | JSON sentinel (format: part P08a) | `alerts.telegram_notifier.TelegramNotifier.send` at CRITICAL severity writes a sentinel before attempting Telegram unless `write_sentinel=False` (default True, `alerts/telegram_notifier.py` L355, L456; writes L470 to L475 and L493 to L498) into its `sentinel_dir`, relative default "data_store" (L201; `from_env` L271 to L297 passes none). Scripts in scope that send at CRITICAL through it: `security_monitor.py` `_send` L1205 (CRITICAL findings), `liveness_probe.py` `deliver_alarm` L276, `copy_gate.py` `send_alert` L286 (CRITICAL severity), `auto_refresh_token.py` L288 (`send_alert`, CRITICAL at L343, L362 to L364, L379), `check_cron_drift.py` L208, `eod_broker_reconcile.py` L416, `premarket_healthcheck.py` L242. Other `notifier.send` calls in scope (for example `disk_monitor.py` L174, `reconcile_pnl.py` L259, `reconcile_positions.py` L308) write one only if the severity passed is CRITICAL. `system_manager.py` L926 to L927 passes `write_sentinel=False` | `alert_watcher.py` (as row S053) | As row S053 | Conditions under which the notifier suppresses or fails the write: part P08a. INTERPRETATION: `liveness_probe.deliver_alarm` writes its own sentinel at L285 whenever the notifier's result is not successful (L279 to L280), after `send` at CRITICAL may already have written one, so one alarm can leave two sentinels; `security_monitor._send` writes its own only when no sentinel path was returned (L1214), `copy_gate.send_alert` only when no sentinel path was returned and Telegram did not deliver (L290 to L292) | A14 (writer code); callers' owners in section 10 |

### 3.2 Security files (data_store/ and data_store/security/)

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S056 | `data_store/security_state.json` | JSON; keys seen in code include `authorized_keys_sha256`, `authorized_keys_fingerprints` (L639 to L640), `known_login_ips` (L682), `file_hashes`, `file_unreadable` (L767 to L768), `last_session_count`, `last_session_peers` (L777 to L778), `geoip_cache` (L781), `copy_protection_enabled` (L804), `copy_bypass_last_check` (L838), `persistent_conditions` (L1195) and the alert-dedup ledger under `alerted` (L1159, L1194) (values not recorded here) | `security_monitor.py` `save_state` L623 to L627 (temp `security_state.tmp` plus `os.replace`): `--baseline` L1376 to L1377; `--watch`, or no mode flag (the mode group is not required, L1338), after alerts L1391. Also rewritten by the `--baseline` subprocess that `approve_ssh_keys.py` launches (L122 to L129) | `security_monitor.py` `load_state` L616 to L620; mtime only: `preflight/checks/security.py` `SecurityWatcherAliveCheck` L50 to L62, `cron_officer.py` `security_watcher_health` L75 to L86, `system_manager.py` `_security_state_age_sec` L801 to L808 | Fixed name; listed as out of scope of `output_retention.py` (comment L66 to L67, HISTORICAL) | Missing or corrupt: `{}` (L617 to L620); INTERPRETATION: the next pass then has no remembered keys, IPs, hashes or dedup ledger. A write failure in `save_state` is not caught in `main` (L1391) | A17 |
| P08b-S057 | `data_store/security/ssh_key_baseline.json` | JSON `fingerprints` (list), `count`, `approved_at`, `approved_by`, `note` (values not recorded) | `approve_ssh_keys.py` `main`, past the `--apply` gate L100 to L104: record L108 to L114, `mkdir` and temp `ssh_key_baseline.tmp` plus `os.replace` L115 to L118; refuses an empty key set (L95 to L98) | `security_monitor.py` `apply_operator_ssh_baseline` L186 to L210, called at L1349 and by `approve_ssh_keys.py` L80 | Fixed name; no retention in scope | Missing or unparseable: `None`, committed config fingerprints stay in force (L198 to L201) | A17 |
| P08b-S058 | `data_store/security/last_run.json` | JSON `version`, `timestamp`, `checks_run`, `findings_count`, `max_severity`, `clean`, `persistent`, `persistent_count` | `security_monitor.py` `_write_last_run_status` L1259 to L1295 (temp `last_run.json.tmp` plus `os.replace`), called at L1394 on every `--watch` (or no-flag) pass after state save; not on `--report` or `--baseline` | Outside scope: `ops/control_tower/aggregator.py` L55 to L69 (part P08a) | Fixed name | `OSError` logged and swallowed (L1294 to L1295) | A17 |
| P08b-S059 | `data_store/security/copy_audit.log` (config `copy_protection.audit_log_path`, an absolute path under the operator's home directory, `config/security.yaml` L154) | JSON Lines; fields `ts`, `event`, `source` or `user`, `ssh_connection`, `peers`, `host`, `pid` plus event fields | Append: `copy_gate.py` `CopyGate.audit` L245 to L263 (from `_enforce` L312, L315, and from `scripts/request_copy.py`, outside scope); `security_monitor.py` `_append_copy_audit` L1224 to L1235 via `_maybe_copy_audit` L1238 to L1249 | `security_monitor.py` `recent_allowed_copy_times` L555 to L579 and `active_token_windows` L582 to L609 (last 500 lines); `system_manager.py` `_read_copy_audit` L756 to L777 (whole file) and `_audit_log_writable` L793 to L798 (not a pure reader: creates the parent directory `data_store/security/` if absent, L795, then tests `os.access W_OK` on it, L796) | Single growing file; no rotation or retention found in scope or in `output_retention.py` scopes (L101 to L114) | Readers return empty on `OSError` and skip unparseable lines; writer `OSError` logged and swallowed (L1234 to L1235; L262 to L263) | A17 |
| P08b-S060 | `data_store/security/copy_token.json` (config `copy_protection.token_path`, absolute under the operator's home directory, `config/security.yaml` L153) | JSON `token_id`, `reason`, `issuer`, `issued_at`, `expires_at` (a copy-authorisation record, not a broker credential) | `copy_gate.py` `CopyGate.write_token` L186 to L191 (temp `copy_token.tmp` plus `os.replace`); `clear_token` L193 to L198 (unlink). Callers are in `scripts/request_copy.py` L88, L108 (outside scope) | `copy_gate.py` `read_token` L177 to L184 (from `check_copy_allowed` L234 and `_print_status` L329) | Fixed name; expiry is a field, not a file deletion | Missing or corrupt: `None`, which blocks the copy (`NO_TOKEN`, L234 to L238) | A17 |

### 3.3 Pre-flight files

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S061 | `data_store/preflight/today.json` (`DEFAULT_SENTINEL_PATH`, relative) | JSON of dataclass `Sentinel` (L38 to L58): `run_date`, three phase statuses and times, `overall_status`, counts, lists, `alert_id`, `last_updated`, `mode`, `account` | `preflight/sentinel.py` `write` L71 to L93 (mkstemp `.today.*.tmp`, fsync, `os.replace`); called by `orchestrator.py` L213 to L218 (load, reset if `run_date` differs, apply, write), skipped under `--dry-run` | `sentinel.load` L61 to L68; `startup_hook.py` L86; `cron_officer.py` `_read_preflight_summary` L488 to L500 | One file, reset per new `run_date` (L215 to L216); no deletion | Missing or corrupt: fresh default `Sentinel()` (L66 to L68); write exception propagates out of `orchestrator.main` (no handler around L218) | A20 |
| P08b-S062 | `logs/preflight_autofix_<YYYY-MM-DD>.jsonl` | JSON Lines `ts`, `run_id`, `check_name`, `fix_action`, `before_state`, `after_state`, `result`, `error_msg` | `preflight/autofix.py` `_audit` L67 to L86 (append), called from `attempt` L148 after each permitted fix | None found in scope (the dashboard reads a DB table `preflight_autofix_log` instead: `ops_dashboard/backend/readers/db_reader.py` L1259 to L1272, part P08a or P06b) | Dated by `_now_iso()[:10]` (IST, UTC fallback L58 to L64); not in `output_retention.py` families (L110 to L114); `.jsonl` is not matched by the crontab's `*.log` clean-up (`deploy/cron/trading-system.cron` L16, boundary) | Every exception swallowed (L84 to L85) | A20 |
| P08b-S063 | Directories `logs/` and `data_store/cron_marks/` | Directories | `preflight/checks/recovery.py` `_ensure_dir` L20 to L34 (`mkdir parents`, `chmod 0o700`), via `TodayLogWritableCheck.fix` L56 to L62 and `CronMarksDirWritableCheck.fix` L82 to L88 | Same checks' `run` (existence and `os.access W_OK`) L48 to L54, L76 to L80 | n/a | `chmod` `OSError` ignored (L32 to L33); result is existence plus writability | A20 |
| P08b-S064 | `logs/system_<yesterday>.log` (existence only) | Text | not written in scope | `preflight/checks/recovery.py` `LogRotationCheck.run` L120 to L126 | n/a | Absent: SKIPPED, not a failure (L125 to L126) | A20 |

### 3.4 Cron control files

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S065 | `data_store/cron_marks/<name>.done` | Text `<rc> <ISO timestamp>` | Not written by any script in scope; the crontab shell suffix writes it (`; rc=$?; mkdir -p ...; echo "$rc $(date -Iseconds)" > .../<name>.done`), composed by `generate_crontab.py` `_marker_block` L67 to L69 and `compose` L72 to L88 from the registry field `marker_name` | `cron_officer.py` `_read_marker` L359 to L371, called by `_classify_job` L419 with `job.name`; `check_cron_drift.py` `check_cron_drift` L75 with `j.marker_name or j.name`; `reconstruct_excursions.py` `_check_backfill_marker` L330 to L344 (`fetch_daily_candles.done`) | One file per marker, overwritten each run; listed as out of scope of `output_retention.py` (comment L66, HISTORICAL) | Missing, stale or unparseable: `NO_SIGNAL` (cron_officer L364 to L371); reconstruct logs a warning and proceeds (L331 to L343) | A16 (generator); readers A16, A15 |
| P08b-S066 | `data_store/cron_audit/job_list_<YYYY-MM-DD>.json` | JSON list of registry job names | `cron_officer.py` `_change_log` L437 to L458 (`mkdir`, `write_text` in place), called from `build_report` L707 only for the EOD report | Same function: newest earlier file by sorted glob L446 to L449 | Dated by the report date (`today`, which is `--as-of-date` when given); no retention found in scope | Every exception logged as warning and swallowed (L456 to L457) | A16 |

### 3.5 Broker session file (credential-holding; path only)

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S067 | `data_store/session/zerodha_token.json` (content not opened by this study) | JSON; field names in code: `account_id`, `broker`, `access_token`, `api_key`, `date`, `saved_at`, `expires_at` (`zerodha_login.py` L157 to L165) | `zerodha_login.py` `save_token` L132 to L176 (O_TRUNC in place, mode 0600, directory 0700); called by `zerodha_login.py` interactive flow L230 and by `auto_refresh_token.py` `_refresh_once` L238 to L244 | `zerodha_login.py` `load_token` L49 to L57 and `is_token_valid` L60 to L77; `healthcheck_server.py` `_check_token` L30 to L46; `refresh_instruments.py` `_resolve_credentials` L329 to L338; `fetch_daily_candles.py` `main` L259 to L268; `forward_shadow_record.py` `_build_kite` L99 to L110; `gemini_data_integrity_check.py` L137; `reconcile_positions.py` L113 to L122; `reconstruct_excursions.py` `_build_fetcher` L290; `sr_corp_action_spotcheck.py` `_build_kite` L33 to L42; `system_manager.py` L460; `t2_cnc_gtt_realtest.py` L160 | Fixed name; expiry is a field (`expires_at` set to the next 05:00 IST, L153 to L155); deletion is a crontab line (`deploy/cron/trading-system.cron` L43, boundary A16 and A04) | `load_token`: `None` on `OSError` or JSON error (L56 to L57); `fetch_daily_candles` exits 1 if absent (L259 to L261); `refresh_instruments` exits 2 if the file is absent or its `access_token` is empty (L330 to L337); `forward_shadow_record` and `reconstruct_excursions` degrade to no-fetch; `sr_corp_action_spotcheck` returns `None` if absent; `t2_cnc_gtt_realtest` raises if absent (no handler at L160) | A04 |

### 3.6 Market-data file

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S068 | `data_store/candles/candle_data_<YYYY-MM-DD>.csv` | CSV header `symbol, datetime, open, high, low, close, volume` | `fetch_daily_candles.py` `_fetch_single_day` L154 to L223: `OUTPUT_DIR.mkdir` L170, `open(output_file, "w", newline="")` L210 to L216 (in place, no encoding argument), only if at least one row was fetched | `reports/daily_report.py` `_load_candle_csv` L384 to L389 (outside scope, part P08a); `reports/daily_trade_review.py` L20, L2384, L2560 states it does not read these files (HISTORICAL) | One file per trade date; overwritten on re-run of the same date; listed as out of scope of `output_retention.py` (comment L66, HISTORICAL) | No rows: no file written (L219 to L220); write exception propagates out of `main` | A05 |

### 3.7 Research and V3 files

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S069 | `data_store/v3/forward_shadow_fs-v1.jsonl` (`_METHOD_VERSION` L40) | JSON Lines, one record per scored signal (fields at L244 to L251 plus provenance) | `forward_shadow_record.py` `main` L259 to L262 (`mkdir`, append, one `write` per record), not under `--dry-run` | Same script L159 to L168 (whole-file scan for the date's `signal_id`s, idempotence) | Versioned name; the comment says a method change bumps the version so a new file is started (L37 to L39, HISTORICAL); `output_retention.py` comment says `data_store/v3/*.jsonl` is never deleted (L54 to L55, HISTORICAL) | Unparseable lines skipped (L166 to L167); any exception: CRITICAL sentinel and exit 1 (L270 to L282) | A18 |
| P08b-S070 | `data_store/allocator/regret.jsonl` (config `portfolio_allocator.regret_log_path`, `config/system_config.yaml` L571) | JSON Lines | not written in scope (writer is runtime allocator code, part P08a) | `v3_shadow_soak_report.py` `allocator_report` L106 to L130 | n/a | Absent: message and return 0 (L113 to L115); bad lines skipped | A18 (reader) |
| P08b-S071 | `data_store/v3/would_be.jsonl` (config `v3_chain.would_be_log_path`, L617) | JSON Lines | not written in scope (`v3_chain/runner.py` L272, part P08a) | `v3_shadow_soak_report.py` `v3_report` L183, read at L190 to L210 | n/a | Absent: message and return 0 (L193 to L195) | A18 (reader) |
| P08b-S072 | `data_store/v3/pb01_would_be.jsonl` (config `watchlist.would_be_log_path`, L631) | JSON Lines | not written in scope (`v3_chain/pb01_runner.py` L246, part P08a) | `v3_shadow_soak_report.py` `pb01_report` L306, read at L354 to L368 | n/a | Absent: section reports empty | A18 (reader) |

### 3.8 Locks

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S073 | `data_store/locks/reconstruct_excursions.lock` | Text, one PID | `reconstruct_excursions.py` `_acquire_lock` L348 to L376 (exclusive create); `_release_lock` L379 to L383 | Same function L359 to L362 | Fixed name; acquired in `main` L448, released at L513 | Live holder: `main` returns 0 "benign" (L448 to L449); unreadable PID becomes 0, so not alive, and the lock is reclaimed (L360 to L362, L365, L371 to L373); unlink failure returns False (L374 to L375); after two failed iterations returns False (L376) | A15 |

### 3.9 Strategy-direction runtime state

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S074 | `data_store/strategy_direction_registry.yaml` (`core/strategy_direction.py` `DEFAULT_STATE_PATH` L44; seed path `DEFAULT_SEED_PATH` L43 of the same module, `config/strategy_direction_registry.yaml`) | YAML (format and write method in `core/strategy_direction.py` `save_registry` L124, part P08a) | `strategy_registry_officer.py` `run` calls `save_registry(new_reg, registry_path)` only when changed (L260 to L261) and not under `--dry-run` (L255 to L258); path built in `main` L281 to L283 | `strategy_registry_officer.py` `run` L231 via `load_registry` (seed fallback while no state file exists, L228 to L231, HISTORICAL docstring) | Fixed name | See part P08a for `load_registry` and `save_registry` behaviour | A07 |

### 3.10 Ad-hoc database copies, receipts and throwaway databases

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S075 | `data_store/backups/pre_w8_backfill_<YYYYMMDD_HHMMSS>.db` | SQLite | `backfill_closure_source_w8.py` `_take_backup` L125 to L153: `sqlite3.connect` on the live DB and a new file, `src.backup(out)`, then `PRAGMA integrity_check` and a `trades` row count on the copy; only on `--commit` (dry run returns at L227 to L229) | Restore is manual; no reader in scope | Stamp from `datetime.now()` (host clock, L235); matched by `backup_retention.py` family `pre_*.db` keep newest 20 (L46, part P09b) | Integrity not "ok" or zero trades: `SystemExit`, no row is written (L146 to L152); the copy file is left on disk in that case | A12 |
| P08b-S076 | `data_store/w8_backfill_receipt_<YYYYMMDD_HHMMSS>.json` | JSON `written_at`, `db`, `note`, `rows` (trade id, symbol, leg, wrote, was) | `backfill_closure_source_w8.py` `_write_receipt` L156 to L170 (`write_text` in place), called at L254 after the row loop L245 to L246 | `backfill_closure_source_w8.py` `_revert` L299 to L317 (`--revert-file`) | No retention found in scope; not in `output_retention.py` scopes | Write failure propagates after rows are already updated | A12 |
| P08b-S077 | `data_store/t2_proof_<YYYYMMDD_HHMMSS>/t2_proof.db` and, per the docstring, a sibling `analytics.db` in the same subdirectory | SQLite | `t2_cnc_gtt_realtest.py` `_open_throwaway_store` L207 to L245: path `_throwaway_store_path` L182 to L190, isolation guard `_assert_isolated` L193 to L204, `StateStore(db_path)` L221, seed rows in one transaction from L225; used by both the live run and `--dry-run` (L584 to L600) | Same run only | Stamp from `now_ist()` (L189); no deletion in the script (grep found no `rmtree` or unlink of the directory); listed as out of scope of `output_retention.py` (comment L66, HISTORICAL) | Guard failure: `SystemExit` before any write (L199 to L204) | A19 |

### 3.11 Log files and log-directory housekeeping

| ID | Path or pattern | Format | Writer and method | Readers | Naming, retention | Missing, corrupt, failed write | Owner |
|---|---|---|---|---|---|---|---|
| P08b-S078 | `logs/alert_watcher_<YYYY-MM-DD>.log` (derived from `alerts.watcher_log_path` "logs/alert_watcher.log") | Plain text `%(asctime)s %(levelname)s %(message)s` | `alert_watcher.py` `_setup_watcher_log` L462 to L480: date computed once at setup from `now_ist()` (L472), `mkdir` (L473), `logging.FileHandler` (append) on logger `alert_watcher` only, added once (L476 to L479) | None found in scope (dated-glob fallbacks of `gemini_log_review.py` L152 and `gemini_watchman.py` L133 can select it, section concerns) | Family `alert_watcher_*.log` kept newest N by `output_retention.py` (L111 to L113, part P09b); also matched by the crontab `*.log` 30-day `find` (L16, boundary) | `mkdir` or handler failure raises out of `main` before the lock is taken (L803 to L806) | A14 |
| P08b-S079 | `logs/system_<YYYY-MM-DD>.log` and the alternatives `trading_<date>.log`, `trading-system_<date>.log`, then any `*<date>*` | Text (JSON lines, written by `main.py` through `core/logger.py`, part P08a) | not written in scope | `gemini_log_review.py` `_find_log_file` L143 to L153, `_process_start_ts` L97 to L113, `_extract_warning_plus` L116 to L140; `gemini_watchman.py` `_find_log_file` L124 to L134, `_tail_new_lines` L137 to L158 (seek to a saved size, reset to 0 if the file shrank, L144 to L148); `system_manager.py` `_count_in_log` L195 to L211 and `report_integrity_check` L412 (size and mtime); `preflight/checks/recovery.py` L120 to L126 (existence) | n/a | Readers return empty, 0 or SKIPPED on absence or `OSError` | A15 (readers) |
| P08b-S080 | All `logs/*.log` (size sum) | n/a | not written | `capture_metrics_baseline.py` `_get_log_size_mb` L95 to L99 (top-level glob, `st_size` sum) | n/a | Missing directory: 0.0 | A15 |
| P08b-S081 | Files in `logs/` and `reports/output/` (top level, any name except suffixes `.db`, `.db-wal`, `.db-shm`) | n/a | `disk_monitor.py` `_cleanup_old_files` L104 to L154: candidates older than `keep_days` (default 2, L34) by mtime, oldest first, deletes `max(1, len // 10)` of them (L137 to L150); only when usage is at or above the critical percentage (default 86, L33; branch L77 to L86) | n/a | This is the only deletion path in scope; it never scans `data_store/` (L117 to L120) | `OSError` from `unlink` logged and skipped (L151 to L152); an `OSError` from `fpath.stat()` at L142 (outside the `try`, also on `--dry-run`) is not caught in `_cleanup_old_files` or `check_disk_usage`: it stops the remaining deletions and reaches `main`, which logs "check failed" and returns 1 without sending the alert (L190 to L201); `--dry-run` logs only (L143 to L144) | A15 |

### 3.12 Existence and age checks on other artefacts

- P08b-S082 FACT: `scripts/system_manager.py` `report_integrity_check` L385 to L414 checks existence, size and mtime-day of `reports/output/daily_report_<day>.xlsx`, `reports/output/daily_trade_review_report_<day>.xlsx`, `reports/watchman/watchman_<day>.md`, `reports/flow_trace/trace_<day>.md`, `logs/system_<day>.log` and `data_store/backups/trading_system-<day>.db` (minimum 10000 bytes, L413); a missing file is a warning.
- P08b-S083 FACT: the expected backup name `trading_system-<day>.db` in `system_manager.py` L413 matches the name produced by the crontab backup line (`deploy/cron/trading-system.cron` L19, `trading_system-$(date +%Y-%m-%d).db`; boundary, part P09a).
- P08b-S084 FACT: `system_manager.py` L396 takes the mtime day with `datetime.fromtimestamp` (host local time) and compares it with an IST day string.

## 4. Database file paths named by the scripts (file level only; statements are in part P06b, analytics in part P07)

| ID | Script (owner) | DB path expression | Opener and mode | Missing-file behaviour |
|---|---|---|---|---|
| P08b-S085 | backfill_closure_source_w8.py (A12) | `ROOT/data_store/trading_system.db` (L66), fixed, no override | `StateStore` L191; raw `sqlite3.connect` for the backup L136 | No existence check; `StateStore` creates the parent directory (`core/state_store.py` L194 to L195) |
| P08b-S086 | capture_metrics_baseline.py (A15) | `--db` default `_ROOT/data_store/trading_system.db` (L49, L60) | `core.db_connect.connect` (read-write, analytics attached) L153, L177, L226, L259; size of DB plus `-wal` file L84 to L92 | No existence check before `connect` |
| P08b-S087 | check_cron_drift.py (A16) | `--db-path` default relative (L175) | `StateStore` L191 | Exits 1 if absent (L182 to L184) |
| P08b-S088 | check_vm_state.py (A15) | Env `DB_PATH` else `PROJECT_ROOT/data_store/trading_system.db` (L48 to L50) | Raw `sqlite3.connect` read-write L55; `UPDATE trades` and `UPDATE orders` with `commit` under `--cleanup-pending` L127 to L144 and `--cleanup-orders` L147 to L173 | Exits 1 if absent (L51 to L53) |
| P08b-S089 | clear_kill_switch.py (A13) | `--db` default `_ROOT/data_store/trading_system.db` (L38) | `StateStore` L55, closed in `finally` L81 to L82 | Exits 1 if absent (L51 to L53) |
| P08b-S090 | compute_strategy_metrics.py (A07) | `--db` default anchored (L308) | `StateStore` L310 | No existence check |
| P08b-S091 | cron_officer.py (A16) | `--db-path` default relative (L866) | `StateStore` L905 | Without DB: briefing or EOD exits 1 unless `--as-of-date` (L904 to L908) |
| P08b-S092 | cron_watchdog.py (A16) | `_ROOT/data_store/trading_system.db` (L42) | `StateStore` L46 | Logs `db_missing`, exits 1 (L43 to L45) |
| P08b-S093 | deploy_assert.py (A17) | `--db` default anchored (L86) | URI `mode=ro` plus `PRAGMA query_only = ON` (L37 to L42) | BLOCKER check fails (L48 to L49) |
| P08b-S094 | eod_broker_reconcile.py (A12) | `--db` default anchored (L356) | `StateStore` L358 | No existence check |
| P08b-S095 | eod_cleanup.py (A12) | `--db` default anchored (L278) | `StateStore` L280 | No existence check |
| P08b-S096 | eod_verify.py (A12) | `--db` default anchored (L197) | `StateStore` L199 | No existence check |
| P08b-S097 | fetch_daily_candles.py (A05) | `ROOT/data_store/trading_system.db` (L39), fixed | Raw `sqlite3.connect` L118 (read); `core.db_connect.connect` L300 (insert into analytics `candles`) | Both functions return early if absent (L116 to L117, L297 to L299) |
| P08b-S098 | fetch_fno_ban.py (A05) | `--db` default anchored (L304) | `StateStore` L306 | No existence check |
| P08b-S099 | forward_shadow_record.py (A18) | `--db` default anchored (L147) | `StateStore` L150 | No existence check |
| P08b-S100 | gemini_data_integrity_check.py (A15) | `--db` default `_ROOT/data_store/trading_system.db` (L44, L77) | `core.db_connect.connect` L85, L99, L115 | No existence check |
| P08b-S101 | gemini_premarket_brief.py (A15) | `--db` default anchored (L39, L65) | Raw `sqlite3.connect` read-write L93, L107, L125, L140 | No existence check |
| P08b-S102 | gemini_trade_coach.py (A15) | `--db` default anchored (L40, L66) | `core.db_connect.connect` L72, L95, L114 | No existence check |
| P08b-S103 | generate_screened_stocks_csv.py (A15) | `project_root/data_store/trading_system.db` (L246) | `core.db_connect.connect_readonly` L270 | Writes a header-only CSV and exits 1 (L253 to L262) |
| P08b-S104 | healthcheck_server.py (A15) | none of its own; uses the `state_store` passed in by `main.py` | `state_store.fetch_one` L55, L80 | n/a |
| P08b-S105 | liveness_probe.py (A15) | Default relative `data_store/trading_system.db` (L138, L201) | `core.db_connect.connect` L147 (read-write, analytics attached) | No existence check; any exception gives "UNKNOWN" (L155 to L157) |
| P08b-S106 | preflight/orchestrator.py (A20) | `--db-path` default relative (L153), passed into `CheckContext` | Checks outside this list (`preflight/checks/database.py`, `state.py`, `engine.py`, part P06b) | n/a |
| P08b-S107 | premarket_healthcheck.py (A20) | `--db-path` default relative (L186) | `StateStore` L92 | Returns failure if absent (L86 to L87) |
| P08b-S108 | reconcile_pnl.py (A12) | `--db` default anchored (L335) | `StateStore` L337 | No existence check |
| P08b-S109 | reconcile_positions.py (A12) | `--db` default anchored (L374) | `StateStore` L376 | No existence check |
| P08b-S110 | reconstruct_excursions.py (A15) | `ROOT/data_store/trading_system.db` (L62), fixed | `StateStore` L459 | No existence check |
| P08b-S111 | replay_signals.py (A19) | `--db` default relative (L227) | `StateStore` L185 (read-write open although the docstring says read-only, L16) | No existence check |
| P08b-S112 | sr_detector_backfill.py (A08) | `--db` default anchored (L24, L102) | `StateStore` L115 | No existence check |
| P08b-S113 | strategy_registry_officer.py (A07) | `--db-path` default anchored (L48, L269) | `core.db_connect.connect` L237 | DB reads skipped if absent (L236) |
| P08b-S114 | system_manager.py (A15) | `--db-path` default relative (L1299) | `StateStore` L1324 | Exits 1 if absent (L1312 to L1314) |
| P08b-S115 | t2_cnc_gtt_realtest.py (A19) | Throwaway `data_store/t2_proof_<ts>/t2_proof.db` (L190); live paths named only for the guard (L118 to L119) | `StateStore` L221 | Fresh file by design |
| P08b-S116 | trade_journal.py (A15) | `--db` default relative (L150) | `StateStore` L157 | No existence check |
| P08b-S117 | v3_hardgate_parity_recompute.py (A18) | `--db` required, documented as a backup under `data_store/backups/` (L18, L209) | URI `file:<path>?mode=ro` without `query_only` (L214) | `mode=ro` fails if absent (INTERPRETATION) |
| P08b-S118 | v3_shadow_soak_report.py (A18) | `_REPO/data_store/trading_system.db` (L37), fixed | URI `mode=ro` plus `busy_timeout` (L66 to L67, L158, L288) | Prints "DB not found" and returns 0 (L62 to L64) |

- P08b-S119 INTERPRETATION: `sqlite3.connect` on a path that does not exist creates an empty database file; the openers above with "No existence check" that use `StateStore`, `core.db_connect.connect` or raw `sqlite3.connect` would therefore create an empty file (and, for `StateStore`, the parent directory) at the named path if it were absent. What `StateStore` then does to a fresh file is part P01 and P03.

## 5. Logging as persistence for the scripts

- P08b-S120 FACT: `core.logger.get_logger` attaches no handler (`core/logger.py` L266 to L274); handlers are attached only by `setup_logging` (L354 onwards), which no script in scope calls (section 1).
- P08b-S121 INTERPRETATION: in a script process that only calls `get_logger`, the root logger has no handlers, so Python's last-resort handler writes records of level WARNING and above to standard error, and INFO and DEBUG records are dropped (Python logging semantics).
- P08b-S122 FACT: four scripts call `logging.basicConfig` (standard error, INFO): `copy_gate.py` L355, `security_monitor.py` L1347, `replay_signals.py` L232, `trade_journal.py` L153.
- P08b-S123 FACT: standard output and error of the long-running scripts go to the journal: `alert-watcher.service` L35 to L36, `security-watcher.service` L25 to L26, `trading-watchman.service` L24 to L25 (`StandardOutput=journal`, `StandardError=journal`).
- P08b-S124 FACT: `preflight/startup_hook.py` `_launch` L58 to L67 starts the orchestrator with standard output and error sent to `subprocess.DEVNULL`, so a phase launched on restart leaves no stdout or stderr record.
- P08b-S293 FACT: `cron_watchdog.py` runs from `deploy/systemd/cron-watchdog.service` (ExecStart L15, `WorkingDirectory` L14), which sets no `StandardOutput=` or `StandardError=` line; the script writes through `get_logger` (L26, L31, no handler) and `print` (L39, L55, L72). INTERPRETATION: systemd's default sends both streams to the journal, so it writes nothing under `logs/` (its sentinel is row S053). HISTORICAL: the unit's header comment says it is not installed by default (L2).

The crontab lines (A16 boundary, file in part P08a) send each cron-run script's standard output and error to a file under `logs/`:

| ID | Script | Redirect target in `deploy/cron/trading-system.cron` | Line |
|---|---|---|---|
| P08b-S125 | cron_officer.py (briefing and EOD) | `logs/cron-officer.log` | L46, L142 |
| P08b-S126 | disk_monitor.py | `logs/cron-disk-monitor.log` | L49 |
| P08b-S127 | auto_refresh_token.py | `logs/cron-auto-token.log` | L52 |
| P08b-S128 | preflight.orchestrator phases A, B, C | `logs/preflight.log` (one file for all three) | L58, L61, L64 |
| P08b-S129 | fetch_fno_ban.py | `logs/cron-fno-ban.log` | L67 |
| P08b-S130 | gemini_premarket_brief.py | `logs/cron-premarket-brief.log` | L70 |
| P08b-S131 | refresh_instruments.py | `logs/cron-refresh-instruments.log` | L73 |
| P08b-S132 | capture_metrics_baseline.py (snapshot and summary) | `logs/cron-metrics.log` | L76, L124 |
| P08b-S133 | liveness_probe.py | `logs/cron-liveness.log` | L79 |
| P08b-S134 | fetch_daily_candles.py | `logs/cron-candle-fetch.log` | L82 |
| P08b-S135 | reconstruct_excursions.py | `logs/cron-excursions.log` | L85 |
| P08b-S136 | forward_shadow_record.py | `logs/cron-forward-shadow.log` | L88 |
| P08b-S137 | sr_detector_backfill.py | `logs/cron-sr-detector-backfill.log` | L91 |
| P08b-S138 | reconcile_positions.py | `logs/cron-reconcile-positions.log` | L97 |
| P08b-S139 | eod_cleanup.py | `logs/cron-eod-cleanup.log` | L100 |
| P08b-S140 | eod_verify.py | `logs/cron-eod-verify.log` | L103 |
| P08b-S141 | eod_broker_reconcile.py | `logs/cron-eod-broker-reconcile.log` | L106 |
| P08b-S142 | generate_screened_stocks_csv.py | `logs/cron-screened-stocks.log` | L112 |
| P08b-S143 | trade_journal.py | `logs/trade_journal.log` | L118 |
| P08b-S144 | compute_strategy_metrics.py | `logs/cron-strategy-metrics.log` | L121 |
| P08b-S145 | strategy_registry_officer.py | `logs/cron-strategy-registry.log` | L127 |
| P08b-S146 | gemini_log_review.py | `logs/cron-gemini-review.log` | L130 |
| P08b-S147 | gemini_trade_coach.py | `logs/cron-trade-coach.log` | L133 |
| P08b-S148 | gemini_data_integrity_check.py | `logs/cron-data-integrity.log` | L136 |
| P08b-S149 | check_cron_drift.py | `logs/cron-drift-check.log` | L139 |
| P08b-S150 | system_manager.py | `logs/system-manager.log` | L145 |

- P08b-S151 FACT: these redirect files are undated and appended (`>>`). `output_retention.py` names `cron-*.log` as never-touched (L114) and has no family for `trade_journal.log`, `system-manager.log` or `preflight.log` (L110 to L114); the crontab clean-up deletes `logs/*.log` older than 30 days by mtime (L16).
- P08b-S152 HISTORICAL: two docstrings name redirect targets that differ from the crontab: `generate_screened_stocks_csv.py` L22 (`logs/cron.log`) and `premarket_healthcheck.py` L28 (`logs/premarket-healthcheck.log`, a script with no crontab line).

## 6. Credential, token and other sensitive files (path patterns and variable names only)

- P08b-S153 FACT: `.env` at the repository root is loaded with `load_dotenv(<root>/.env)` by `auto_refresh_token.py` L53, `check_cron_drift.py` L39, `clear_kill_switch.py` L31, `cron_officer.py` L29, `cron_watchdog.py` L23, `eod_broker_reconcile.py` L53, `fetch_daily_candles.py` L32, `forward_shadow_record.py` L35, `gemini_data_integrity_check.py` L38, `gemini_log_review.py` L32, `gemini_premarket_brief.py` L34, `gemini_trade_coach.py` L35, `gemini_watchman.py` L39, `liveness_probe.py` L65, `reconstruct_excursions.py` L60, `strategy_registry_officer.py` L36, `system_manager.py` L51; and with a bare `load_dotenv()` (search from the working directory) by `refresh_instruments.py` L45 and `zerodha_login.py` L36.
- P08b-S154 FACT: `config/accounts.csv` is loaded through `core.account_registry.AccountRegistry.load` by `auto_refresh_token.py` L339 (default L62), `eod_broker_reconcile.py` L435, `reconcile_positions.py` L103, `refresh_instruments.py` L319, `system_manager.py` L162, `zerodha_login.py` L258; `security_monitor.py` hashes it as a watched file listed in `config/security.yaml` `watched_files` L134 (via `sha256_file` L231 to L240; the code default `_default_watched_files` L223 applies only when the config list is empty, L181 to L182). It is also read indirectly, when the `core.account_registry` helpers `primary_account_tag`, `primary_api_key` or `primary_api_key_env` are called (path anchored to the repository, `core/account_registry.py` `_read_primary_row` L302 to L309); scripts in scope import them, for example `fetch_daily_candles.py` L35, `forward_shadow_record.py` L34, `gemini_data_integrity_check.py` L42, `reconstruct_excursions.py` L59, `cron_officer.py` L44, `alert_watcher.py` L70, `system_manager.py` L57, `preflight/sentinel.py` L21 (dataclass field default L58). A04 boundary.
- P08b-S155 FACT: environment-variable names referenced in scope include `ZERODHA_USER_ID`, `ZERODHA_USER_ID_<ACCOUNT_ID>`, `ZERODHA_PASSWORD`, `ZERODHA_PASSWORD_<ACCOUNT_ID>`, `ZERODHA_TOTP_SECRET`, `ZERODHA_API_KEY`, `ZERODHA_API_KEY_<ACCOUNT_ID>`, `ZERODHA_API_SECRET`, `ZERODHA_ACCESS_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_PRIMARY`, `ALERT_SMTP_PASSWORD` (named in messages), `TRADING_MODE`, `DB_PATH` (`check_vm_state.py` L48), `USER`, `LOGNAME`, `SSH_CONNECTION` (`copy_gate.py` L250 to L251). Account-specific names also come from columns of `config/accounts.csv` (`auto_refresh_token.py` L351 to L353).
- P08b-S156 FACT: the broker session file `data_store/session/zerodha_token.json` is row 3.5; the copy-authorisation record `data_store/security/copy_token.json` is in 3.2.
- P08b-S157 FACT: `security_monitor.py` reads the system authentication log (`_DEFAULT_AUTHLOG` L76, config `authlog_path` `config/security.yaml` L120) and SSH authorised-keys file (config key `authorized_keys_path`) and hashes the files listed in `config/security.yaml` `watched_files` L125 to L134: the authorised-keys file, `/etc/ssh/sshd_config` and a drop-in under `/etc/ssh/sshd_config.d/`, `/etc/sudoers`, two systemd unit files, and `.env`, `config/system_config.yaml` and `config/accounts.csv` given as absolute paths in the project directory under the operator's home directory; the code fallback `_default_watched_files` L213 to L224 (the same set without the drop-in) applies only if that list is empty (L181 to L182). These are outside `data_store/` and `logs/`; recorded as boundary (A17).
- P08b-S290 FACT: `generate_crontab.py` `_ENV_PREFIX` L48 to L53 composes, for the `python` and `python_nopath` wrappers (L50, L51), `cd <project root> && set -a && . ./.env && set +a` in front of the interpreter, so the cron shell reads and exports `.env` before the script starts; the generated lines in `deploy/cron/trading-system.cron` carry it (for example L46, L52, L58; boundary A16, A17). Two generated lines pass `--account <ACCOUNT_ID>` on the command line (`refresh_instruments.py` L73, `reconcile_positions.py` L97).

## 7. Route coverage per writer (normal, error, retry, restart, partial failure)

| ID | Writer | Normal | Error or write failure | Retry | Restart or crash mid-write | Partial failure |
|---|---|---|---|---|---|---|
| P08b-S158 | alert_watcher state files (3.1) | Each pass: load attempts and SMTP state, send, rename flags, save | SMTP and degraded writes swallow `OSError`; attempts save does not | Next pass (`--loop` interval, L753 to L769); attempt counter up to `watcher_max_attempts` then `mark_failed` | Lock left with a dead PID is cleaned on next start (L117 to L128); temp-plus-replace leaves old or new JSON (INTERPRETATION 2.2) | A pass with no pending sentinels returns at L510 to L513 before the degraded marker clear and the attempts save |
| P08b-S159 | security_monitor (3.2) | `--watch`: load state, run checks, send fresh alerts, append copy audit, save state, write last-run | `save_state` failure propagates; last-run and copy-audit failures logged | systemd restarts the one-pass process (`security-watcher.service`, HISTORICAL comment L3 to L4) | State replace is atomic (INTERPRETATION); copy-audit append can leave a torn last line, which readers skip | Alerts are sent (L1386 to L1390) before state is saved (L1391); a crash in between re-sends on the next pass, subject to dedup state not being saved (INTERPRETATION) |
| P08b-S160 | preflight sentinel (3.3) | Load, reset on new day, apply report, write | Write exception propagates (no handler) | Next cron phase; `startup_hook` launches missed A or B phases (L86 to L91) | mkstemp plus fsync plus replace; stray temp unlinked (L87 to L92) | `RUNNING` status counts as not run for the startup hook (L55) |
| P08b-S161 | autofix audit (3.3) | One appended line per fix attempt | Swallowed | n/a | Torn line possible (INTERPRETATION) | Timed-out fix thread keeps running while the line records FAILED (L106 to L109) |
| P08b-S162 | cron_officer job list (3.4) | EOD writes today's snapshot | Swallowed (warning) | Next EOD | In-place `write_text` can leave a truncated file (INTERPRETATION). If that file is from an earlier day, every later EOD raises at L449, inside the same `try`, before the write at L454: no later snapshot is written and the diff stays empty until the file is removed; a truncated file of the same day is skipped by the `< today` filter (L448) and rewritten (FACT from L444 to L457) | n/a |
| P08b-S163 | token file (3.5) | Truncate and write in place | Exception propagates to `auto_refresh_token.main`, which alerts and returns 1 (L377 to L381) | `run_refresh` retries network errors with backoff, three attempts (L71, L248 to L273) | O_TRUNC then write: a crash between leaves an empty or partial file, which `load_token` reports as `None` (INTERPRETATION) | n/a |
| P08b-S164 | candle CSV (3.6) | Write all rows then insert into analytics | Exception propagates | Re-run of the date overwrites | In-place write can leave a partial CSV (INTERPRETATION) | CSV is written before the DB insert (L210 to L218); an insert failure leaves the CSV present |
| P08b-S165 | forward-shadow JSONL (3.7) | Append new records for the date | Any exception: CRITICAL sentinel, exit 1 | Re-run skips signal ids already present for the date (L159 to L168) | A torn final line is skipped by the reader (L166 to L167) | Heartbeat recorded only after the append (L264 to L266) |
| P08b-S166 | reconstruct lock (3.8) | Acquire, run, release | Unlink failure on stale lock returns False, run skipped | Second loop iteration after stale reclaim | Dead-PID lock reclaimed next run | n/a |
| P08b-S167 | W8 backfill (3.10) | Backup, row loop, receipt, verify | Backup check failure: `SystemExit` before writes | Manual | n/a | Rows are written one by one (L245 to L246) before the receipt (L254); an exception inside the loop leaves updated rows with no receipt |
| P08b-S168 | disk_monitor deletion (3.11) | Only at critical usage | Per-file failure logged | Next hourly run deletes the next tenth | n/a | Deletes at most a tenth of the old candidates per run |

## 8. Dry-run and rehearsal paths that still write

- P08b-S169 FACT: `cron_officer.py` EOD with `--dry-run` or `--force-dry-run` still calls `build_report` (L941 to L942), which writes `data_store/cron_audit/job_list_<date>.json` through `_change_log` (L707); with `--as-of-date` the file is named for the simulated date.
- P08b-S170 FACT: `system_manager.py` with `--dry-run` still saves `reports/system_manager/<day>.txt` (L1330) and records a heartbeat row (L1343 to L1348); only sending and the soft kill are suppressed (L1334 to L1335, L917 to L919).
- P08b-S171 FACT: `alert_watcher.py` with `--dry-run` skips sending and renaming (L539, L546 to L548) but still saves the attempts file (L718 to L719) and, on a pass with pending sentinels and no SMTP backoff, resets SMTP state and clears the degraded marker (L711 to L715). When SMTP is in backoff (`skip_smtp`, L521 to L525), `--dry-run` still runs the Telegram fallback (L701 to L708): `_telegram_fallback_batch` has no dry-run parameter, sends through Telegram and renames sentinels to `.delivered` (`mark_delivered` L429), and `_write_degraded_marker` writes `alert_watcher_degraded.json` (L707).
- P08b-S172 FACT: `preflight/orchestrator.py` with `--dry-run` skips the sentinel write (L213) and auto-fixes are refused (`autofix.py` L137 to L138); `preflight/deliver.py` returns before writing a sentinel (L69 to L71).
- P08b-S173 FACT: `t2_cnc_gtt_realtest.py --dry-run` still creates the throwaway database directory and file (L579 to L595).
- P08b-S174 FACT: `forward_shadow_record.py --dry-run` prints and writes no JSONL (L254 to L257); `strategy_registry_officer.py --dry-run` returns before `save_registry` (L255 to L258); `backfill_closure_source_w8.py` without `--commit` returns before the backup (L227 to L229).

## 9. Paper and Live splits (marked, not traced)

- P08b-S175 FACT: `eod_verify.py` L204 sets `is_paper` from `--mode` or `TRADING_MODE`; the paper branch changes the P&L evaluation (L81, L131) and message (L215) and has no file effect in this part.
- P08b-S176 FACT: `t2_cnc_gtt_realtest.py` `_build_live_adapter` L144 to L177 builds a paper adapter for `--dry-run` (`paper_mode=paper`, synthetic quotes L128); the paper side was not traced beyond its throwaway-store write (3.10).
- P08b-S177 FACT: `system_manager.py` `_day_capital` L149 to L168 falls back to the `paper_capital` column of `config/accounts.csv`; not traced further.
- P08b-S178 FACT: `preflight/orchestrator.py` `--mode live or paper` (L154) flows into `CheckContext` (L173 to L181); the paper side of the checks was not traced.
- P08b-S291 FACT: further Live/paper splits, not traced: `compute_strategy_metrics.py` L298 to L299 (mode label from `TRADING_MODE`); `eod_broker_reconcile.py` L344 (`is_paper`), branch L369; `reconcile_pnl.py` L311 to L312, paper branch L157; `reconcile_positions.py` L352 to L353, paper branch L225. Their database statements are part P06b; no file effect under `data_store/` or `logs/` was traced on the paper side.

## 10. Per-script crosswalk (all 53 files)

| ID | Script (owner) | data_store or logs touches in this part (section refs) |
|---|---|---|
| P08b-S179 | alert_watcher.py (A14) | Writes lock, attempts, SMTP state, degraded marker, optional heartbeat (3.1); own log (3.11); renames sentinels (3.1) |
| P08b-S180 | approve_ssh_keys.py (A17) | Writes SSH baseline override; launches state re-seed (3.2) |
| P08b-S181 | auto_refresh_token.py (A04) | Writes token file via `save_token` (3.5); `.env` and accounts file paths (6); CRITICAL sentinel indirectly through the notifier, L288 (row S289) |
| P08b-S182 | backfill_closure_source_w8.py (A12) | Backup copy and receipt (3.10); DB (4) |
| P08b-S183 | capture_metrics_baseline.py (A15) | DB size, log size sum (3.11); DB (4) |
| P08b-S184 | check_cron_drift.py (A16) | Reads cron marks (3.4); DB (4); CRITICAL sentinel indirectly through the notifier at CRITICAL, L208 (row S289) |
| P08b-S185 | check_vm_state.py (A15) | DB read-write via raw connect (4) |
| P08b-S186 | clear_kill_switch.py (A13) | DB (4) |
| P08b-S187 | compute_strategy_metrics.py (A07) | DB (4) |
| P08b-S188 | copy_gate.py (A17) | Copy token and copy audit log (3.2); CRITICAL sentinel via `send_alert` L295, and through `TelegramNotifier.send` L286 (3.1, row S289) |
| P08b-S189 | cron_officer.py (A16) | Reads marks, security-state mtime, degraded marker, pre-flight sentinel; writes job list and self-test probe (3.1, 3.2, 3.3, 3.4); DB (4); writes the email sentinel in `deliver_report` L845 (EOD, ban window or CRITICAL; not under dry-run, L831 to L834) (3.1) |
| P08b-S190 | cron_watchdog.py (A16) | DB (4); CRITICAL sentinel (3.1) |
| P08b-S191 | deploy_assert.py (A17) | Degraded-marker existence (3.1); DB read-only (4) |
| P08b-S192 | disk_monitor.py (A15) | Deletes old files in `logs/` and `reports/output/` (3.11) |
| P08b-S193 | eod_broker_reconcile.py (A12) | DB (4); CRITICAL sentinel indirectly through the notifier, L416 (row S289) |
| P08b-S194 | eod_cleanup.py (A12) | DB (4) |
| P08b-S195 | eod_verify.py (A12) | DB (4); heartbeat to relative default DB (2.1) |
| P08b-S196 | fetch_daily_candles.py (A05) | Candle CSV (3.6); token file read (3.5); DB (4) |
| P08b-S197 | fetch_fno_ban.py (A05) | DB (4) |
| P08b-S198 | forward_shadow_record.py (A18) | Forward-shadow JSONL (3.7); token file read (3.5); DB (4); CRITICAL sentinel on crash L275 (3.1) |
| P08b-S199 | gemini_data_integrity_check.py (A15) | Token file read (3.5); DB (4); writes `reports/integrity/` (boundary) |
| P08b-S200 | gemini_log_review.py (A15) | Reads dated log (3.11); writes `reports/log_review/` (boundary); sentinel L269, `sentinel_dir` L275 (3.1) |
| P08b-S201 | gemini_premarket_brief.py (A15) | DB (4); reads `reports/log_review/`, writes `reports/briefing/` (boundary) |
| P08b-S202 | gemini_trade_coach.py (A15) | DB (4); writes `reports/coach/` (boundary) |
| P08b-S203 | gemini_watchman.py (A15) | Tails dated log (3.11); appends `reports/watchman/` and `reports/flow_trace/` (boundary) |
| P08b-S204 | generate_crontab.py (A16) | Composes marker and redirect strings (3.4, 5); writes only the `--out` file (L387 to L392) |
| P08b-S205 | generate_screened_stocks_csv.py (A15) | DB read-only (4); writes `reports/daily_review/` (boundary) |
| P08b-S206 | healthcheck_server.py (A15) | Token file read (3.5); DB via main's store (4) |
| P08b-S207 | liveness_probe.py (A15) | Liveness alarm state (3.1); DB (4); CRITICAL sentinel through `TelegramNotifier.send` L276 and own fallback sentinel in `deliver_alarm` L285 when Telegram fails (3.1, row S289) |
| P08b-S208 | preflight/autofix.py (A20) | Autofix audit JSONL (3.3) |
| P08b-S209 | preflight/checks/recovery.py (A20) | Directory creation and 0700 (3.3); flag glob (3.1); yesterday's log existence (3.3) |
| P08b-S210 | preflight/checks/security.py (A20) | Security-state mtime (3.2); reads `config/security.yaml` |
| P08b-S211 | preflight/checks/vm_health.py (A20) | Disk usage of the project root and `/` only (L37 to L40, L91, L111); no file read or write under these folders |
| P08b-S212 | preflight/deliver.py (A20) | CRITICAL sentinel, default directory "data_store" (3.1) |
| P08b-S213 | preflight/orchestrator.py (A20) | Pre-flight sentinel load and write (3.3); DB path into checks (4) |
| P08b-S214 | preflight/sentinel.py (A20) | Pre-flight sentinel writer and loader (3.3) |
| P08b-S215 | preflight/startup_hook.py (A20) | Reads pre-flight sentinel (3.3); launches orchestrator with output discarded (5) |
| P08b-S216 | premarket_healthcheck.py (A20) | DB (4); CRITICAL sentinel indirectly through the notifier, L242 (row S289) |
| P08b-S217 | reconcile_pnl.py (A12) | DB (4) |
| P08b-S218 | reconcile_positions.py (A12) | Token file read (3.5); DB (4) |
| P08b-S219 | reconstruct_excursions.py (A15) | Lock (3.8); reads candle-fetch marker (3.4); token file read (3.5); DB (4); CRITICAL sentinels L402, L505 (3.1) |
| P08b-S220 | refresh_instruments.py (A05) | Token file read with `--account` (3.5); writes `config/instruments.csv` (outside these folders) |
| P08b-S221 | replay_signals.py (A19) | DB (4); writes `reports/output/replay_<date>.csv` in place (L214 to L218) |
| P08b-S222 | security_monitor.py (A17) | Security state, SSH baseline, last-run, copy audit (3.2); CRITICAL sentinel L1217, and through `TelegramNotifier.send` L1205 (3.1, row S289) |
| P08b-S223 | sr_corp_action_spotcheck.py (A08) | Token file read (3.5) |
| P08b-S224 | sr_detector_backfill.py (A08) | DB (4) |
| P08b-S225 | strategy_registry_officer.py (A07) | Strategy-direction state (3.9); DB (4); sentinel L210, `sentinel_dir` L214 (3.1) |
| P08b-S226 | system_manager.py (A15) | Reads system log, copy audit, security-state mtime, flag glob, token validity; existence checks (3.2, 3.11, 3.12); DB (4); writes `reports/system_manager/<day>.txt` (boundary); temporary git index in the system temp directory (L1171 to L1181, unlinked L1247 to L1251); email sentinel on each non-dry-run run, L932 (dry-run returns at L917 to L919) (3.1) |
| P08b-S227 | t2_cnc_gtt_realtest.py (A19) | Throwaway DB directory (3.10); token file read (3.5) |
| P08b-S228 | trade_journal.py (A15) | DB (4) |
| P08b-S229 | v3_hardgate_parity_recompute.py (A18) | DB at an operator-given path, read-only (4) |
| P08b-S230 | v3_shadow_soak_report.py (A18) | Reads three shadow JSONL files (3.7); DB read-only (4) |
| P08b-S231 | zerodha_login.py (A04) | Token file writer and reader (3.5) |

## 11. Owner topics of out-of-scope files named in this part (from the master index)

| ID | File or folder | Owner topic | Index line |
|---|---|---|---|
| P08b-S232 | `alerts/critical.py`, `deploy/systemd/alert-watcher.service` | A14 | L174 |
| P08b-S233 | `core/logger.py`, `reports/` (incl. `daily_report.py`, `daily_trade_review.py`), `ops/` (incl. `control_tower/aggregator.py`), `ops_dashboard/`, `deploy/systemd/trading-watchman.service`, `scripts/monitoring_canary.py` | A15 | L183, L330 |
| P08b-S234 | `utils/cron_heartbeat.py`, `config/cron_registry.yaml`, `deploy/cron/trading-system.cron` | A16 | L192 |
| P08b-S235 | `scripts/request_copy.py`, other `deploy/systemd/` units (deployment and security declarations) | A17 | L343, L204 |
| P08b-S236 | `v3_chain/runner.py`, `v3_chain/pb01_runner.py` | A18 | L219 |
| P08b-S237 | `core/strategy_direction.py` | A07 | L111 |
| P08b-S238 | `main.py`, `utils/instance_lock.py`, `core/account_registry.py` | A01 | L57 |
| P08b-S239 | `core/config_loader.py`, `config/system_config.yaml`, `config/security.yaml` | A02 | L66 |
| P08b-S240 | `core/state_store.py`, `core/db_connect.py`, `scripts/output_retention.py`, `scripts/backup_retention.py` | A03 | L75, L289 to L294 |

## Concerns for the AUDIT (neutral)

- P08b-S241 `alert_watcher.py` `_acquire_lock` L109 to L132 is check-then-write without exclusive create; two processes starting together could both pass the check. A recycled PID makes a stale lock look alive, and the watcher then exits 0 (L808 to L810).
- P08b-S242 `alert_watcher.py` `run_once` returns at L510 to L513 when no sentinel is pending, so the degraded marker (L715) and SMTP state reset (L713 to L714) are reached only on a pass that has pending sentinels.
- P08b-S243 `alert_watcher.py` computes the dated log file name once at start-up (L472); under `--loop` (the systemd unit's mode, `alert-watcher.service` L24 to L25) the watcher keeps writing to the start day's file until restarted.
- P08b-S244 The heartbeat helper writes to its relative default DB unless `db_path` is passed; fourteen scripts that accept a DB option do not pass it, and every `skip_if_non_trading_day` call in scope uses the default (2.1).
- P08b-S245 The read-modify-write cycles on `today.json`, `security_state.json`, the attempts file and the liveness state are unlocked (2.4). Pre-flight phases B (09:14) and C (09:15) both write `today.json` (crontab L61, L64; boundary), and `startup_hook` can launch phases A and B as two detached processes in one call (L88 to L91).
- P08b-S246 `approve_ssh_keys.py --apply` re-seeds `security_state.json` through a subprocess (L121 to L127) while the security-watcher service may be writing the same file.
- P08b-S247 Only `preflight/sentinel.py` calls `fsync`; every other temp-plus-replace writer and every append writer has no fsync (2.2).
- P08b-S248 Files holding security material (`security_state.json`, `security/ssh_key_baseline.json`, `security/copy_token.json`, `security/copy_audit.log`) are created with the default umask; no unit sets `UMask=` (2.3).
- P08b-S249 `zerodha_login.save_token` truncates and rewrites the token file in place (L170 to L172), with no temporary file; concurrent readers listed in 3.5 could read an empty or partial file during the write.
- P08b-S250 `check_vm_state.py` docstring says "read-only diagnostics only" (L2), while `--cleanup-pending` and `--cleanup-orders` run `UPDATE` plus `commit` on `trades` and `orders` through a raw read-write connection (L127 to L173).
- P08b-S251 `replay_signals.py` docstring says "Read-only: NO database writes" (L16) but opens the database through `StateStore` (L185), a read-write opener.
- P08b-S252 Several openers have no existence check and would create an empty database file at a missing path (section 4), including `liveness_probe.py`, whose DB default is relative (L138, L201).
- P08b-S253 `gemini_log_review.py` L152 to L153 and `gemini_watchman.py` L133 to L134 fall back to the alphabetically first file in `logs/` whose name contains the date when the three expected names are absent; such a file can be `alert_watcher_<date>.log` or `preflight_autofix_<date>.jsonl`. `gemini_watchman.py` keeps tailing the first file found while it exists (L277 to L302).
- P08b-S254 `gemini_watchman.py` `_tail_new_lines` passes a byte size from `stat` to `seek` on a text-mode file (L144 to L148); for text files Python documents `seek` positions as opaque values from `tell` (INTERPRETATION).
- P08b-S255 The two marker readers resolve marker file names differently: `cron_officer.py` L419 uses `job.name`, `check_cron_drift.py` L75 uses `marker_name or name`; `config/cron_registry.yaml` L154 has one job (`db_retention_vacuum`) whose marker name differs from its job name.
- P08b-S256 The marker timestamp is written with the host's `date -Iseconds` (crontab, boundary) and compared with an IST date by `cron_officer._read_marker` L367 and by `reconstruct_excursions._check_backfill_marker` L337 to L339; host time-zone dependence. `backfill_closure_source_w8.py` L235, `generate_screened_stocks_csv.py` L238 and L319 (default date and CSV name) and `trade_journal.py` L156 also use the host clock.
- P08b-S257 No retention or rotation was found, in scope or in `output_retention.py` scopes, for `data_store/security/copy_audit.log`, `data_store/cron_audit/job_list_*.json`, `logs/preflight_autofix_*.jsonl`, `data_store/w8_backfill_receipt_*.json`, `data_store/t2_proof_*/`, and the undated cron redirect logs (5).
- P08b-S258 `disk_monitor.py` at critical usage deletes any top-level file in `logs/` older than two days, including hidden state markers such as `logs/.holiday_notified_<date>` (written by `main.py` L2133), which `output_retention.py` deliberately never touches (L43, L114).
- P08b-S259 `backfill_closure_source_w8.py` docstring and comments say an undo record exists "from the instant anything changes" (L248 to L253, HISTORICAL), while the receipt is written after the whole row loop (L245 to L254).
- P08b-S260 `cron_officer.py` and `system_manager.py` dry-run modes still write files or heartbeat rows (section 8); `alert_watcher.py --dry-run` still changes its state files.
- P08b-S261 The candle CSV is written in place with no explicit encoding (L211) and before the analytics insert; a re-run overwrites the earlier CSV (3.6).
- P08b-S292 Identifier content can reach cron redirect files under `logs/` (values not recorded here): `fetch_daily_candles.py` L279 prints the broker profile's user identifier and user name to standard output, appended to `logs/cron-candle-fetch.log` (crontab L82); `auto_refresh_token.py` writes an account identifier into ERROR log lines (L361, L378), which reach standard error through the last-resort handler (S121), and prints it under `--dry-run` (L372), appended to `logs/cron-auto-token.log` (crontab L52); its CRITICAL alert texts with the account identifier (L362 to L364, L379) also go through the notifier, which can write them into a sentinel under `data_store/` (row S289). The redirect files are undated and only removed by the 30-day `find` (crontab L16).

## Questions about intent (OPEN QUESTION, for the project owner)

- P08b-S262 OPEN QUESTION: was `data_store/security/copy_audit.log` meant to grow without rotation or retention?
- P08b-S263 OPEN QUESTION: were the cron-redirect files `logs/trade_journal.log`, `logs/system-manager.log` and `logs/preflight.log`, which match no `output_retention.py` family, meant to be kept indefinitely?
- P08b-S264 OPEN QUESTION: was `check_vm_state.py` meant to keep its two data-changing flags after being described as read-only?
- P08b-S265 OPEN QUESTION: were throwaway `data_store/t2_proof_<ts>/` directories meant to be removed after a proof run?
- P08b-S266 OPEN QUESTION: was the heartbeat of scripts run with `--db` meant to go to the same database?

## UNKNOWN / NOT ESTABLISHED

- P08b-S267 UNKNOWN / NOT ESTABLISHED: whether any of the files in section 3 existed on either machine, their sizes, permissions or contents; no runtime artefact survives.
- P08b-S268 UNKNOWN / NOT ESTABLISHED: the effective umask of the cron and systemd processes on the machines, and therefore the actual modes of the files in section 2.3.
- P08b-S269 UNKNOWN / NOT ESTABLISHED: whether `alerts.watcher_heartbeat_path` was ever set on a machine (it is absent from the baseline `config/system_config.yaml`).
- P08b-S270 UNKNOWN / NOT ESTABLISHED: the host time zone of the machines, which decides whether the host-clock dates in the concerns above equal IST dates.
- P08b-S271 UNKNOWN / NOT ESTABLISHED: whether the critical-usage branch of `disk_monitor.py` ever deleted files, whether `backfill_closure_source_w8.py --commit` or `t2_cnc_gtt_realtest.py` were ever run, and whether `approve_ssh_keys.py --apply` was ever used.
- P08b-S272 UNKNOWN / NOT ESTABLISHED: whether concurrent writers named in the concerns ever overlapped in practice.

## Boundary handoffs (owner topic: what crosses)

- P08b-S273 A14 and part P08a: `alerts/critical.py` sentinel format, `.flag` write, `.delivered` and `.failed` renames; this part lists only the callers and their `sentinel_dir` argument.
- P08b-S274 A15 and part P08a: `core/logger.py` handlers and the `logs/system_*`, `trades_*`, `reconciler_*`, `debug_*` files written by `main.py`; log content belongs to A15.
- P08b-S275 A16 and part P08a: `deploy/cron/trading-system.cron` redirect targets, marker writes, `logs/*.log` 30-day clean-up (L16), delivered-flag clean-up (L31), token-file deletion (L43); `config/cron_registry.yaml` `marker_name` and `log_target`; schedules are declarations only.
- P08b-S276 A16: `utils/cron_heartbeat.py` relative DB default and heartbeat rows (part P08a for the file, P06a or P04/P05 for the table).
- P08b-S277 A03 parts P09a and P09b: `backup_retention.py` (`pre_*.db` keep 20 covers the W8 backup), `output_retention.py` families and exclusions, and the crontab backup naming that `system_manager.py` checks.
- P08b-S278 A03 part P01 and P03: what `StateStore` and `core.db_connect.connect` do on open of a missing or fresh file, including analytics attach; part P07 for analytics tables (`candles`, `system_metrics`).
- P08b-S279 A03 part P06b: every SQL statement of the scripts in section 4 and the read-only or read-write classification per script.
- P08b-S280 A04: the broker token file life cycle (writers, readers, expiry field, 05:00 deletion), `.env` and `config/accounts.csv` resolution; this part records paths and variable names only.
- P08b-S281 A17: security monitor checks, copy-protection policy, `scripts/request_copy.py` (token issue and revoke, outside this part's list), watched-file hashing, the systemd units' working directory and absence of `UMask=`.
- P08b-S282 A07 and part P08a: `core/strategy_direction.py` `load_registry` and `save_registry` for `data_store/strategy_direction_registry.yaml`.
- P08b-S283 A18 and part P08a: writers of `data_store/allocator/regret.jsonl`, `data_store/v3/would_be.jsonl`, `data_store/v3/pb01_would_be.jsonl` (`v3_chain/runner.py` L272, `v3_chain/pb01_runner.py` L246).
- P08b-S284 A15: files written under `reports/` (integrity, log_review, briefing, coach, watchman, flow_trace, daily_review, system_manager, output) are outside `data_store/` and `logs/` and are recorded here only as boundaries.
- P08b-S285 A20: pre-flight checks not in this list (`preflight/checks/database.py`, `state.py`, `engine.py`, `broker.py`) and their database and token-file reads.
