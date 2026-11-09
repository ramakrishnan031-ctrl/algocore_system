# A02 — RECONCILED TOPIC RECORD: Configuration and effective settings

**Status:** APPROVED — the RECONCILED TOPIC RECORD of topic A02 (Document 04, section 4, steps 9 and 10), the topic's authoritative document, approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31), after ChatGPT's review of every package file
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09, prepared after the treatment round was committed (`ededc7f`), for ChatGPT's package review. Revised, 2026-11-09, after ChatGPT's package review of the same day: (M-01) the STUDY's questions 4, 5, 7, 8 and 10, which the AUDIT kept as OPEN QUESTIONs without needing them to classify, were raised with Rama in batch 3 and kept OPEN by him, and are recorded as A02-13 to A02-17 (sections 9, 14, 16, 17, 18.1, 19, 20, 23 and 24); (M-02) the provisional KNOWN DEFECT status of T-01 and F-20 is recorded as Rama's decision, not as a question for him (sections 10, 22 and 23). Approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31), after ChatGPT's fresh review of the revised package (PASS): status marked APPROVED; section 23 records the approval; section 24 gives the hashes of the approved files, whose status and revision lines alone changed.
**Purpose and scope:** The authoritative topic document of A02 (Document 07, section 5; Decision Register, D-25). It combines the STUDY and the AUDIT in distinct parts and keeps distinct the study findings (Part A), the audit conclusions (Part B), Rama's decisions (Part C) and the unresolved OPEN items (Part D). It applies the refinements that the AUDIT made to the STUDY, records the corrections that the topic made to the existing technical records, and carries forward every open item and cross-topic handoff. It records the legacy system as it is; it does not repair it, and it is not a V2 design.
**Sources:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (the baseline; Decision Register, D-21), through `A02_STUDY_2026-11-06.md` (content last changed at `5d43484`), `A02_AUDIT_2026-11-08.md` (content last changed at `2a96068`; passed by ChatGPT's complete package review of 08-Nov-2026) and the nine evidence files in this topic's `evidence/` folder (section 24); the Open Issues Register (entries A02-01 to A02-05 and A02-08 to A02-12, as committed at `8392d19`, and A02-13 to A02-17, added with this package) and the Audit Findings Register (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`, its 111 A02 entries and the A02 treatment decisions, as committed at `ededc7f`).
**Related documents:** Documents 02, 04, 05, 06, 07, 08 and 10; the Master System Investigation Index (entry A02 and Appendix A); the Decision Register, D-12, D-17, D-21, D-23 to D-25, D-28 and D-30; the A01 RECONCILED TOPIC RECORD (sections 15 and 22); the Open Issues Register, the Audit Findings Register and the Topic Completion Register.

## 1. How to read this record

### 1.1 Parts and labels

- **Part A, study findings (reconciled):** what the code and the files at the baseline do, from the STUDY, with the AUDIT's refinements applied (section 6) and each marked "[refined: ...]". The STUDY is kept unchanged (Document 07, section 3); where a STUDY statement and this record differ, this record governs.
- **Part B, audit conclusions:** what the AUDIT found when it compared the code with the intended behaviour. The AUDIT records each item in full; this record summarises and cites it.
- **Part C, Rama's decisions:** his answers on the legacy system and his treatments for the new system, as recorded in the Open Issues Register and the Audit Findings Register, which quote his words and govern. A treatment is input to the Phase 2 proposal only: it is not a V2 design decision, it changes no legacy finding, and no legacy behaviour becomes a V2 requirement automatically (Document 04, section 5.5; Document 08, section 12).
- **Part D, unresolved OPEN items:** every item that is not settled, with where it is tracked.
- Labels (Document 04, section 6): FACT, INTERPRETATION, HISTORICAL, KNOWN DEFECT, OPEN QUESTION and UNKNOWN / NOT ESTABLISHED. Decision statuses (Document 05, section 3): AGREED, PROPOSED, UNDER DISCUSSION and OPEN QUESTION. Anything that only Rama can decide is marked OPEN FOR RAMA.
- References: "STUDY 5.4" and "AUDIT 9.3, K-29" are sections and records of those documents; "A02-nn" is an Open Issues Register entry; "batch T3, group G2" is a group of the treatment round, recorded under "A02 treatment decisions" in the Audit Findings Register. L-nn, V-nn, T-nn, F-nn, K-nn and X-01 are the AUDIT's items (part L, the central loader; V, the validator, auditor, snapshot and change detection; T, strategy configuration; F, the files, environment and revert script; K, configured settings from file to consumer; X-01, added at assembly). Line references written "L123" are to the legacy repository at the baseline, with the path given or as in the STUDY and the AUDIT.

### 1.2 Baseline and the runtime-evidence limit

Every code statement is about commit `970aabf` (D-21). The last recorded deployment was `7d4970a` (02-Sep-2026); two A02 paths changed after it, both for the MIS square-off: `config/system_config.yaml` (39 lines added and 4 removed by `5455ced` and `5f75c9b`) and `core/config_loader.py` (38 lines added by `5f75c9b`: the two MIS market-protection percentages, defaults 1.5 and 2.5, range 0.1 to 10.0). Whether production ran any commit after `7d4970a` is UNKNOWN / NOT ESTABLISHED (STUDY 1.8; L-18).

Both legacy VMs were terminated, and their databases, logs, environment files and crontab do not survive (Document 06, section 4.2). The code and the tracked files show what is implemented and what was configured at the baseline. A value in a tracked file is "the file value at the baseline", not proof that it was in force (Document 08, section 10). HISTORICAL: a VM-only edit of `min_pass_score`, made at Rama's request, is recorded (commit `8a3e0b7`; `docs/SYSTEM_MAP.md` L1363), so a tracked value can differ from the value on the VM (AUDIT 3).

### 1.3 Security

Credential values, tokens, account identifiers, personal names, IP addresses, e-mail addresses, key fingerprints and absolute machine paths are not written here; credential variables are named by type, and passages that hold such material are cited by path and line only (Document 08, section 11). Credential values, their history and their exposure are outside A02 by Rama's instruction of 08-Nov-2026 (AUDIT 1.3): F-19 is WITHDRAWN and F-18 is INFORMATION; neither is counted, put to Rama or handed to another topic. Credential variable names and their loading are recorded where they are configuration.

## 2. Scope and coverage

- **Index entry A02:** configuration sources and files, schemas and validation, defaults, fallbacks and precedence, environment-variable names and their use, strategy configuration loading, configuration snapshots and change detection, and the effective settings the code produces for Live behaviour. The 58 paths: the 50 YAML and CSV files under `config/` other than `config/cron_registry.yaml` (A16's); `core/config_loader.py`, `core/config_validator.py`, `core/config_auditor.py`, `core/config_snapshotter.py`; `strategies/schema.py`, `strategies/loader.py`; `.env.example` (key names only); and `scripts/revert_temp_config.py` (index Appendix A) (STUDY 1.2, 3.1).
- **Document 08 coverage (section 3):** item 17 (configuration), with supporting evidence for items 5 to 14 and 18 where those topics consume configuration.
- **Excluded:** every consumer's business logic, which belongs to its owner topic (index rule 1): A02 records the call site, the value received and the owner, and hands the rest over (section 15). `config/cron_registry.yaml` is A16's. Paper-only paths are marked, not traced (Document 08, section 2). A01's findings are not re-classified (AUDIT 4). Nothing was repaired and nothing was designed.
- **Study:** the code and files were read in seven parts by helpers under read-only rules, each part checked by a separate helper and corrected by a third pass; an independent check of the assembled STUDY (about 780 statements) corrected 75 points; nothing from the legacy repository was run or imported (STUDY 1.5).
- **Audit:** 260 items audited against every intent source the admitted evidence holds, matches included, each recorded with the fields of Document 04, section 5.4, in five parts (L, V, T, F, K) and one item added at assembly (X-01); after ChatGPT's first review a separate helper checked every corrected record, every changed count, every handoff and the register line references (AUDIT 1.5, 1.8, 14).
- **What could not be covered (AUDIT 14, summarised):** every runtime fact (which files, values and environment were in force; what the validator, auditor, snapshot table and change detection recorded); the library versions installed on the VMs (behaviour was tested on synthetic inputs); consumers' internals, read at the boundary only and handed to their owners; sources not in the repository (SPEC section 8, a separate document of the twelve BUILD 1 conflicts, assistant memory notes); long registers and audit documents, read where the search hit. Whether these gaps affect closure is set out in section 23.

---

## Part A — Study findings (reconciled)

## 3. Configuration in brief

From STUDY 2, with the AUDIT's refinements applied.

The legacy system keeps its configuration in 50 tracked YAML and CSV files under `config/`. One central loader, `core/config_loader.py::load_all`, reads exactly eight of them, the "registry": `system_config.yaml` (the master file: 753 lines, 42 top-level keys), `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scoring_weights.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml` and the holiday file `nse_holidays_<year>.yaml`, whose year is fixed once, when the module is first imported, from the host-local date. All eight are required; the load is atomic, validates each file against its own pydantic model and returns one `AppConfig` with a SHA-256 of each file's raw bytes. There is no cache and no reload: each of the 26 non-test call sites in 21 files re-reads the files.

The other 42 files are read by their own modules or not at all: the 16 strategy files through `strategies/loader.py` and `strategies/schema.py`; six other YAML files and the 20 CSV files directly by their consumers, without a central schema, or by no reader.

The central schema has 65 models, all refusing unknown keys, with 458 fields (289 with a code default) and 97 validators. Pydantic runs in its default lax, coercing mode; mapping-typed fields accept any keys; there is no cross-file validation; NaN and infinity pass most float fields; duplicate YAML keys are accepted, the last value winning. The configuration auditor (groups A, C and G) runs inside every load; a BLOCK fails the load, which `main.py` turns into exit 5. The key-usage validator is wired but never fed. Change detection and the W0 snapshot cover the eight registry files only.

In the Live boot, `main.py` loads the configuration once, registers it with the validator, compares the file hashes with the previous session's, loads `accounts.csv`, runs the startup checks, writes the W0 snapshot, reports a changed file as CONFIG_DIFF, loads the strategies, re-runs two auditor rules with the strategies, wires the sections into the subsystems' constructors and finally runs the validator's report (STUDY 5.1).

The most important facts:

- FACT: the holiday file name is built from `date.today().year` at the loader's first import (`core/config_loader.py` L2449), the host-local date, not the IST time authority; only the import year's file is loaded, and the baseline holds 2026 only (STUDY 5.3, 10.2; L-01).
- FACT: a missing, unreadable, malformed or invalid registry file, an auditor BLOCK or an invalid MIS timing at load ends the boot with exit 5, before anything is hashed, compared or snapshotted; an unreadable or malformed holiday file ends it earlier, at the holiday guard, with exit 2 (A01's side) (STUDY 4.5, 13.1).
- FACT: 38 key occurrences (24 distinct schema keys) are absent from the eight files and take the code default. Loader defaults differ from the file values, and would apply if the key were deleted, in 26 places in `system_config.yaml`, among them `force_intraday_only` (default True, file false), `delivery_enabled` (default False, file true) and `trade_type` (default "INTRADAY", file BOTH) (STUDY 4.4); across the eight registry files part L counts 31, of which 28 match their field comments (L-42, L-43) and 3 are in L-04, L-06 and L-13 [refined: AUDIT, Appendix A; section 6, row 1].
- FACT: several configured values do not reach the code they describe: the entry-gate liquidity settings, the three `live_feed` keys, `smart_tgt.enabled`, `eod_squareoff.auto_resume_kill_switch` and `broker.primary`; two exit buffers are bypassed by constants on some paths; the 33 Telegram notifier call sites in 31 files use only the on/off switch, read directly from the file (STUDY 5.4 to 5.6).
- FACT: the key-usage validator registers five of the eight sections, but no non-test code calls its tracking method `get()`. INTERPRETATION: every registered key is reported as unaccessed, and drift is never detected (STUDY 7.4).
- FACT: the W0 snapshot stores the whole validated configuration as JSON with a key-substring redaction, de-duplicated per IST date and hash, with no unique constraint; it excludes the strategy files and every other file outside the registry (STUDY 7.1).
- FACT: the 16 strategy files all conform to the 41-field `StrategyConfig` (13 required); each omits 5 or 6 keys; 15 are enabled and 1 disabled. The boot loads them twice; the S10 cross-check against `scan_webhook_map.yaml` is never requested; a duplicate `name` would silently replace an earlier file (STUDY 6).
- FACT: `.env.example` declares 20 key names; the code makes 57 environment reads, 3 writes, 22 `load_dotenv` calls and 2 child-process pass-throughs; 20 names that the code reads (and 4 supplied by the operating system) are absent from the template, and one declared name is never read (STUDY 9).
- FACT and INTERPRETATION: the TEMP-revert script is not declared or invoked anywhere in the code, cron or deployment files, while a deployment guide tells the operator to run it. From a re-implementation of its regular expressions (the script not run), at the baseline it would treat the word "ATTEMPT" as a TEMP marker and, with `--apply --confirm`, change `risk.daily_loss_limit_pct` from the file value 0.03 to 0.05 and replace the inline comments of all six matched lines, writing in place without a backup (STUDY 8; F-20, F-22).

## 4. Key study facts by area

Each subsection condenses the STUDY section named; the STUDY and its evidence files hold the full detail, line by line.

### 4.1 Inventory and provenance (STUDY 3)

- FACT: `config/` holds 51 tracked files; without `config/cron_registry.yaml`, 50 are A02's: 30 YAML (14 top-level files and the 16 strategy files) and 20 CSV (2 account files, 17 index-member files and 1 security master). No discrepancy with the index was found. The only file ever deleted under `config/` is `config/instruments.csv` (untracked on 21-Jun-2026).
- FACT: by how they are read: the eight registry files (`load_all`; seven other modules also read keys of `system_config.yaml` directly); the 16 strategy files (`strategies/loader.py` and seven other readers); six YAML files read directly (`security.yaml` by the security scripts, `preflight.yaml` by a pre-flight check, `expected_managers.yaml` by `core/effect_telemetry.py`, `index_universe.yaml`, `strategy_direction_registry.yaml` as a seed only, `symbol_aliases.yaml`); and the CSV files (`accounts.csv` by `core/account_registry.py`, A01; the reference data by `scripts/refresh_instruments.py`, A05). `accounts_multi_example.csv` is read only by a test, and four index-member files have no reader.
- FACT: required by the central loader: the eight registry files (exit 5 when one is missing), `slippage_model.yaml` included, although its only consumer call site is paper-only. Required by their own readers: `accounts.csv`, the strategy directory and the security master. Optional, a missing file giving a default: `security.yaml`, `preflight.yaml`, `index_universe.yaml`, `symbol_aliases.yaml`, `strategy_direction_registry.yaml` and the reference CSV files. `expected_managers.yaml` has no handler at its read site.
- FACT: configuration sources outside `config/`: the command line (`main.py --config PATH`, relative to the working directory; the declared unit passes no `--config`); readers that do not follow `--config` (working-directory literals or module-relative paths); environment variables (names held in configuration, read by consumers; no expansion inside any file); constants standing in for configuration (the service start window, pre-flight's expected risk caps 5 and 10, three required-secret name lists, three required-file lists besides the loader's registry, the revert script's table, the NTP host and thresholds); no settings table in the database (two configuration records only: the W0 snapshot table and the session's last configuration hash); the dashboard's own configuration tree with its own copy of the trading hours (A15).
- FACT: expected but absent at the baseline: `config/instruments.csv` (removed; a blocking startup-check entry still lists it), holiday files for any year other than 2026, `.env` (the template is `.env.example`), runtime state files under `data_store/`, the dashboard's local overlay, a "config_overrides" file named only in a comment, and systemd drop-ins. Whether any existed on a machine is UNKNOWN / NOT ESTABLISHED.

### 4.2 Parsing, schemas and validation (STUDY 4)

- FACT: the registry files are read as raw bytes and parsed with `yaml.safe_load` (YAML 1.1); each is validated by one root model (`SystemConfig`, `BrokerCostsConfig`, `BrokerLimitsConfig`, `SlippageConfig`, `ScoringConfig`, `ScanWebhookMapConfig`, `ChartinkScannersConfig`, `NseHolidaysConfig`). The strategy files are parsed with an explicit UTF-8 open and validated by `StrategyConfig(**raw)`. The directly read files have no schema.
- FACT and INTERPRETATION (pydantic 2 semantics): unknown keys are refused at every model level, but the keys of mapping-typed fields are free (for example `special_sessions`, `product_map`, the slippage override maps and both scanner maps); no model sets strict mode, so values are coerced in lax mode; defaults are not validated; a loaded model can be changed by assignment without validation (no such assignment was found in non-test code); there is no cross-file validation.
- FACT: what is enforced: types (lax), literal sets in validators, the validators' ranges (for example the market-protection percentages, the leverage bounds and finiteness, `poll_interval_sec >= 1`), cross-field rules in `trading_hours` (the MIS square-off timing and window ordering), `capital` (leverage and the delivery pin) and the score-threshold ordering, the required keys (169 fields without a default) and a few non-empty rules. Not enforced (examples): the token buckets, timeouts and back-off list of `broker_limits.yaml`, the clock-skew tier ordering, the entry-throttle keys, `webhook.bind_port`, two HH:MM-shaped times, `special_sessions` beyond its type, and anything between files.
- FACT: normalisation is minimal: an empty file becomes `{}`; holiday dates are parsed; HH:MM strings are checked but kept as strings and parsed again by consumers; there is no case-folding, environment expansion, include or override layer. INTERPRETATION (YAML 1.1): an unquoted `15:30` is the integer 930 while `09:15` stays a string; bare `off`, `on`, `yes` and `no` are booleans; `.nan` and `.inf` are floats.
- FACT: for the registry files, a missing file gives `ConfigMissingError`; an unreadable file an unwrapped `OSError`; malformed YAML or non-UTF-8 bytes, a missing required key, a rule violation or an auditor BLOCK `ConfigSchemaError`; duplicate keys, a missing defaulted key, unknown keys inside a mapping-typed field, coercible wrong types, NaN or infinity where no rule refuses them, and empty strings or lists where no rule refuses them pass silently; an exception other than `ValueError` or `AssertionError` inside a validator escapes unwrapped; there is no partial result. `main.py` turns any exception from `load_all` into a CRITICAL log line and exit 5.
- FACT: inconsistencies between descriptions and code: the loader's docstring says it does not fill in defaults (289 fields have one) and that the file should be split above 600 lines (it has 2,516); the load-time MIS timing check uses the literal poll interval 5 while the boot build uses the configured one; the auditor's group B duplicates fatal schema checks; its docstring says the startup path runs "ACEG" while the constant is "ACG"; a missing key gives `ConfigSchemaError`, not `ConfigMissingError` as that class's docstring says.

### 4.3 Loading and effective settings (STUDY 5)

- FACT: precedence: a key present in the file wins over the model default; `load_all` reads and expands no environment variable (the only read in the module is the SMTP password resolver); the 22 `load_dotenv` calls pass no `override`, so a variable already in the environment wins (INTERPRETATION of python-dotenv); `main.py` and three other processes have no `load_dotenv` and depend on systemd `EnvironmentFile=` lines or the cron line that sources `.env`; command-line options win over configured values in several scripts; code constants override files in four places (the delivery leverage pin 1.0, the service-window ceiling 18:15, the leverage ceiling 20.0, the MIS check's literal 5).
- FACT: settings are read at import (the holiday year, the default directory), at process start (one load in `main.py`; the strategies twice) and, by some readers, every time they run (the cron notifiers' Telegram switch; `build_direction_map`, which re-validates every strategy file on each call). There is no reload. INTERPRETATION: a value edited after the boot does not reach the running process, while scripts started later read the new value; a process that imported the loader before a year change asks for the earlier year's file.
- FACT: used, transformed, ignored, overridden or replaced (examples): floored or replaced by the consumer (the webhook dedup window floored to 60; the per-IP refill and burst replaced when zero; the entry-throttle keys floored, a zero burst window replaced by 60); validated or configured but not passed, so the constructor default applies (four capital, sizing and risk keys whose defaults equal the file values; the entry-gate liquidity keys, off in the code although the file enables the check; the three `live_feed` keys, a 5-second code maximum delay against a 30-second file value; the S&R zone warmer's queue size); bypassed by a constant on some paths (`capital.emergency_exit_buffer_pct`, `capital.sl_limit_offset_pct`, `watchlist.entry_tf`); overridden by code (`smart_tgt.enabled`, `eod_squareoff.auto_resume_kill_switch`, `broker.primary`); ignored by a whole class of consumers (the 33 Telegram notifier call sites); read only for display, logging or audit (for example `broker.primary` and the performance multipliers); with no consumer (twelve keys, among them the broker fallback keys, the pipeline timeout, `alerts.telegram.whitelist_only` and two `broker_limits.yaml` keys).
- FACT: one setting read differently in different places (examples): the trading hours (the dashboard keeps its own copy and ends its entry window at the square-off time); the MIS square-off timing (built three times); the signal-queue capacity (the receiver rejects at 80 per cent, pre-flight warns at 90); "delivery active" (different predicates in `main.py` and the dashboard); `force_intraday_only` and `trade_type` when absent (different defaults in the loader, the constructors, a cron script and the dashboard); `excluded_symbols` (case-insensitive after alias resolution in the receiver, case-sensitive in the daily report); `alerts.telegram.enabled` (strict through the loader, fail-open in the cron notifiers); the dashboard's `alerts.telegram_enabled`, a key that does not exist.
- FACT for the code; INTERPRETATION for the comparison: where the configured and the code-effective values differ at the baseline: the entry-gate liquidity check (configured on, code-effective off); the live-feed reconnect limits; `smart_tgt.enabled` (the manager is enabled whatever is configured); `auto_resume_kill_switch` (no effect); `broker.primary` (always Zerodha). Where a constructor default or constant equals the file value, the two agree at the baseline, but a change to the file would not reach that consumer. Which values were in force is UNKNOWN / NOT ESTABLISHED.

### 4.4 Strategy configuration (STUDY 6)

- FACT: `StrategyConfig` refuses unknown keys and has 41 fields, 13 required and 28 defaulted; its cross-field rules cover the stop-loss and target percentages under `FIXED_PCT`, the stop-loss bounds and the entry times; no rule ties `intent`, `order_protocol`, `pipeline`, `horizon` and `direction` to one another, `direction` to the name suffix, `name` to the file name, or the per-strategy window to the global trading hours; there is no branch by strategy type. The schema docstring says every YAML declares every field, as locked decision S5 does; the schema does not enforce it.
- FACT and INTERPRETATION: `validate_strategy` gives `ConfigSchemaError` for a missing file, a YAML error, a non-mapping and a schema failure; a non-UTF-8 file (`UnicodeDecodeError`), other `OSError`s and a non-string top-level key (`TypeError`) escape uncaught; a duplicate key keeps the last value. Discovery takes `*.yaml` in one flat directory; no file or no directory is a `ConfigSchemaError`; the first failing file stops the load; enabled and disabled strategies are both loaded (gating is A07's); a second file with the same `name` silently replaces the first; `force_intraday_only` now changes only a log line (the earlier rewrite was removed on 10-Jul-2026); the S10 cross-check runs only when a map path is passed, which only tests do.
- FACT: the boot loads the strategy files twice, in the startup checks and in `main.py`; at the baseline both return the same content. INTERPRETATION (the same reading as A01 S-39): a non-UTF-8 strategy file at boot is caught by the strategy check, but a later step reads the raw text, catches only `OSError` and lets the decode error leave the startup checks, so the start ends with exit 2 instead of the blocking exit 3 with its alert.
- FACT: strategy values reach consumers through the loader (the signal processor, the boot audits, the control tower, pre-flight), through `validate_strategy` file by file (`build_direction_map`, the taxonomy map, the status script) and through three raw readers without the schema (the daily report, `scripts/system_manager.py`, the dashboard) and one text scanner. Ten fields have no non-test reader of the strategy attribute, among them the ATR multipliers, the smart-target and pullback fields, `active_days` and `order_protocol` (the order placer uses its own default protocol; OPEN QUESTION for A10); a `trailing_sl_*` reader sits behind a guard that may be unreachable (OPEN QUESTION for A10 and A11); `sl_gap_buffer_pct` is used as a percentage.
- FACT: the 16 files have no parse, encoding, unknown-key, required-key or rule problem; each omits 5 or 6 keys (the four `trailing_sl_*` keys in all, `v3_playbook` in 15, `sl_gap_buffer_pct` in 12); 15 enabled, 1 disabled (`pb01_breakout_retest`); 10 long and 6 short; 13 intraday and 3 delivery; the six long and short pairs are identical apart from name, description and direction; all 16 declare `entry_start_time` 09:25 and `min_score: 0`, so the global threshold applies.
- FACT: `strategy_direction_registry.yaml` is a seed: the runtime state lives in `data_store/`, and no live trading path reads the tracked file's content. `scoring_weights.yaml` is loaded by `load_all` and passed to the A07 scorers, and also read directly by the auditor (group B, outside the boot), the daily report, the dashboard and two A18 scripts, each with its own handling.

### 4.5 Snapshots, hashes, the auditor and change detection (STUDY 7)

- FACT: the W0 snapshot is called only by `main.py`, non-fatally, after the account and mode are final and before subsystem construction, the CONFIG_DIFF block and the A4 and A5 exit-3 gates. It stores `AppConfig.model_dump` (the eight sub-configurations and the file hashes); it excludes the 43 tracked files outside the registry, the strategy files and `accounts.csv` among them, and every environment value. Redaction replaces a non-empty string value only when its key contains one of five secret-like substrings. The row is skipped when the same IST date already holds the same hash; the check and the insert are separate steps, and the account and mode are not part of the key. No difference is computed and no alert is sent. The INFO log line includes the broker account identifier, while the docstring says only the row id, hash prefix and decision are logged. INTERPRETATION: in a same-day sequence of configurations A, B, then A again, the third boot is skipped and the date's latest row stays B while A is loaded.
- FACT: two hashes exist: the per-file hashes of the raw bytes of the eight registry files (stored in the single session row and compared at the next boot; a changed file becomes a CONFIG_DIFF event and a Telegram warning) and the W0 hash of the redacted canonical JSON (used only for de-duplication). Neither includes the strategy files, `accounts.csv` or any other file outside the registry. A removed registry key is not reported (A01 C7d); at the baseline that can happen only at a year change, when the holiday key changes name.
- FACT: the auditor's groups: A (contradictions; A4 and A5 BLOCK, A3 WARN), B (deleted keys and the threshold ordering, from the raw YAML; B5 BLOCK), C (capital-relative ranges and caps, WARN), D (slippage overrides), E (the launch-phase entry start), F (constructor defaults against configured values) and G (entry-end margin, leverage, minimum tick, per-strategy windows). It runs (1) inside every load, groups ACG, where a BLOCK fails the load and WARN findings are logged by every process that loads; (2) in `main.py` with the strategies, group A only, acting only on A4 and A5 (exit 3); (3) in pre-flight and the control tower, all groups, so group B runs only there. It reads 9 of the 42 `SystemConfig` sections and none of the other seven sub-configurations; A5 and A3 swallow every exception; its `capital` parameter is unused.
- FACT and INTERPRETATION: the key-usage validator registers the leaf values of `system`, `broker_costs`, `broker_limits`, `slippage` and `scoring` (not the scanner maps, the holidays or lists of plain values); `validate_all(strict=False)` runs once after every subsystem is built; with no `get()` caller, each boot that reaches it logs one `CONFIG_UNACCESSED` warning and never raises; the drift branch, which would raise whatever `strict` is, cannot occur.
- FACT: file events at boot: a changed registry file (a comment included) is listed and reported as CONFIG_DIFF if the boot gets that far, with a new W0 row; a missing, unreadable, malformed, invalid or empty registry file gives exit 5 before any comparison; a strategy file or any other file outside the registry is invisible to both hashes; an exit between the session write and the CONFIG_DIFF block stores the new hashes without recording a change, so the next start sees none (A01 S-11, KNOWN DEFECT, whose treatment is A01's).

### 4.6 The temporary-configuration mechanism (STUDY 8)

- FACT (the script was not run): `scripts/revert_temp_config.py` holds a fixed table of seven entries (six in `system_config.yaml`, one in `strategies/gap_fade_long.yaml`), each with an unanchored regular expression, a TEMP value and a "prod" value. An entry is "active" when the whole file contains the substring `TEMP` anywhere and its pattern matches anywhere; the report prints the table's value, not the value found; an apply replaces the first match through the end of the line, comment included, writing the file in place without a backup or atomic rename; `--apply` without `--confirm` exits 3; there is no check of the value replaced, of the running service, of market hours or of the mode.
- INTERPRETATION (from an independent re-implementation of its two regular-expression steps): at the baseline `system_config.yaml` contains `TEMP` only inside the word "ATTEMPT", so all six of its entries would be active; with `--apply --confirm` the only value change would be `risk.daily_loss_limit_pct` from 0.03 to 0.05, the other five matched lines keeping their values but losing their comments; `gap_fade_long.yaml` has no `TEMP` and would be left alone, its `min_score: 0` differing from the table's 60.
- FACT: the script is not declared in the cron registry, any deployment file or systemd unit, and no code imports or calls it; the deployment guide tells the operator to run it when switching from Paper to Live; a TEMP tracker (last updated 03-Jun-2026) and a unit test also mention it. Whether it was ever run is UNKNOWN / NOT ESTABLISHED (F-25). The startup check `check_temp_config_values` counts a different marker, `# TEMP`, and only warns; no such marker occurs in any tracked configuration file.

### 4.7 Environment variables (STUDY 9)

- FACT: `.env.example` has 50 lines and 20 key names, every value a placeholder: per-account broker key, secret and TOTP names for five accounts (15 names), four Telegram names and one webhook-secret name. Its header says to copy it to `.env`, never to commit `.env` and never to put a real value in the template. The 15 names in `accounts.csv`'s three name columns all appear in it.
- FACT: the code has 84 environment-related sites: 57 reads, 3 writes (all in `main.py`, which writes broker session variables into its own environment), 22 `load_dotenv` calls in 22 scripts and 2 child-process pass-throughs. The live boot's required-secret check covers the primary account's broker key and secret names, the Telegram token name and the webhook-secret name; two other required-secret lists exist, in pre-flight and a health-check script; other reads are optional, with fallbacks.
- FACT: 20 names that the code reads are absent from `.env.example` (among them generic broker fallback names, the broker user-identifier and password names, the SMTP and e-mail-fallback names, whose configuration block is enabled, and several operator and tool switches); one declared name, the Telegram personal chat identifier, is never read. HISTORICAL: a comment in `system_config.yaml` says the e-mail-fallback variables were absent from the VM's `.env`.
- FACT: credential-related keys are declared as variable names: the broker names in `accounts.csv` and the template; the Telegram and SMTP names in `system_config.yaml`; the webhook secret in the template. `core/config_loader.py` has no broker-credential or webhook-secret field, and `load_all` never checks that a named variable exists. Locations of sensitive material in tracked files are recorded in STUDY 9.6 by path and key only.

### 4.8 The key-to-consumer map (STUDY 10)

- FACT: every leaf of `system_config.yaml`, `broker_limits.yaml`, `broker_costs.yaml`, `slippage_model.yaml`, `security.yaml`, `preflight.yaml` and `expected_managers.yaml` is traced from file to consumer and owner in the two key-map evidence files; the strategy files by field; the other files per file. `system_config.yaml` has 327 leaf keys (counting the items of its two lists of mappings by their keys): 293 with a functional consumer, 5 paper-only, the rest read only for display, logging or audit, or with no consumer. `slippage_model.yaml`'s 4 keys have no Live consumer.
- FACT: the same value is held in several places (examples): the sentinel directory (a configuration key, two `security.yaml` keys and at least 13 code literals or dataclass defaults); the SMTP host, port and TLS in two configuration blocks; the score thresholds 60, 65 and 80 in `v3_chain` and `scoring_weights.yaml`; the broker cost rates as literals in the daily report; the F&O ban URL in three places. Competing lists: four required-file lists, three required-secret lists, three derivations of the holiday-file year.
- FACT: units: `_pct` means a fraction in some keys and a percentage in others, while two MIS keys use `_percent`; in the strategy schema most `*_pct` fields are fractions while `sl_gap_buffer_pct` is used as a percentage and the `trailing_sl_*_pct` defaults are 60, 80 and 40. Stale or non-existent names include the MIS module's message naming a non-existent key and the dashboard's non-existent `alerts.telegram_enabled`.
- FACT: direct readers that bypass the central loader include the Telegram on/off reader (any error gives enabled), the auditor's group B reader, the daily report, a cron script, pre-flight, the dashboard (the day's snapshot first, the raw YAML as a fallback), two A18 scripts, `scripts/system_manager.py`, the startup checks' file and TEMP-marker checks, the security monitor's watched-file hashing and the revert script, each with its own handling and defaults.

## 5. Cross-topic boundaries

FACT (STUDY 12): every configured value's consumer belongs to an owner topic. A02 records the consumer's call site and what it reads; the owner traces its own consumption (index rule 1). The STUDY's section 12 table states, owner by owner, what A02 hands over: A01 (the `main.py` wiring and the startup checks), A03 (the snapshot table and the session hash), A04 (broker selection, limits and product codes), A05 (the live feed, the F&O ban URL, the reference data), A06 (the webhook settings, the signal-queue thresholds, the strategy fields read by the signal processor), A07 (strategy selection, the unread strategy fields, the direction registry, the scorers), A08 (the S&R keys), A09 (capital and sizing), A10 (the entry gate, `order_protocol`, the `trailing_sl_*` guard), A11 (smart targets, structure exits), A12 (the MIS timing, the exit-buffer constants, `auto_resume_kill_switch`), A13 (the duplicated kill-switch limit), A14 (the notifier call sites), A15 (the dashboard, the snapshot readers, `expected_managers.yaml`), A16 (cron's `.env` loading and the registry officer), A17 (`security.yaml`, `.env` loading by systemd), A18 (the V3 and regime keys), A19 (the tests and a test script) and A20 (pre-flight's own lists and literals). What each owner must examine about an A02 finding is in AUDIT 10 and is carried forward in section 15.

## 6. Refinements that the AUDIT made to the STUDY

The independent check of the STUDY corrected 75 points before the AUDIT was assembled (STUDY 1.5); they are in the STUDY as committed. The AUDIT re-checked the STUDY and recorded where it adds or refines (AUDIT, Appendix A). The STUDY is not changed; the refinements are applied in this record. The STUDY's other statements stand.

| # | STUDY place | STUDY statement | What stands (AUDIT) | Applied in |
|---|---|---|---|---|
| 1 | 4.4; 13.2 item 4 | 13 differing defaults in `system_config.yaml` L21 to L357, 26 in the whole file | part L counts 31 across the eight registry files (13 in L21 to L357; 18 more in L359 onward, `scoring_weights.yaml` and `scan_webhook_map.yaml`), of which 10 and 18 match their field comments (L-42, L-43) and the rest are L-04, L-06 and L-13 | section 3; Part B, section 11 (T1 G2) |
| 2 | 7.3; 13.2 item 8 | the auditor's groups and callers | B5 is a BLOCK in a group that the guide and pre-flight describe as WARN-only (V-05); a failing A5 probe lets the A5 boot gate pass silently (V-06); G1 measures the entry window against the 15:17 backstop, not the first MIS pass (V-09) | Part B, section 11 (T2 G2) |
| 3 | 4.2; 13.2 item 6 | lax coercion | INTERPRETATION (pydantic, synthetic models): a YAML `true` in a slippage-override map becomes 1.0 before the overrides' bool test runs, so that test can never fire (L-10) | Part B, section 11 (T1 G3) |
| 4 | 4.5; 13.2 item 6 | duplicate keys accepted | the "CRITICAL" duplicate-scanner check that the map's header and P17 describe cannot fire, because the parser keeps the last duplicate (L-09) | Part B, section 11 (T1 G3) |
| 5 | 8.1; 13.2 item 16 | the revert script's detection | the re-scan it asks for after an apply can never come back clean, because its own comment contains "TEMP" (F-20, KNOWN DEFECT, provisional) | Part B, section 10 |
| 6 | 3.2; 13.2 item 14 | the scanner URLs' status | all 16 follow the placeholder pattern of the module 27 instruction, while a dashboard comment calls them real (T-21, F-03) | Part B, sections 11 and 12 |
| 7 | 6.5; 10.2 | `scoring_weights.yaml` as the single source | the signal-age threshold is 60 s in code against 90 s in P9a and in the file's comment (T-20) | Part B, section 11 (T3 G3) |
| 8 | 10.2; 13.2 item 14 | stale line references in `system_config.yaml` comments | recorded and rejected as issues, as A01 did for M-27 | Part B, section 9 |

The AUDIT also took a disposition on each of the STUDY's 22 concerns (AUDIT 2.3): 3 CONFIRMED, 1 CONFIRMED as facts with a MATCH (concern 21), and the others SPLIT, NARROWED or partly REJECTED as issues, each with its items; the STUDY's concern list itself is neutral and stands.

## 7. Corrections to the existing technical records (Document 08, section 9)

The STUDY checked the configuration claims of the five existing records (`01_SYSTEM_OVERVIEW.md`, `02_REPOSITORY_AND_FILE_MAP.md`, `03_STARTUP_RUNTIME_AND_SCHEDULER.md`, `03A_CRON_REGISTRY_TABLE.md` and `LEGACY_SYSTEM_MANUAL_INDEX.md`, kept unchanged in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/`) against the code at `970aabf` (STUDY, Appendix A; evidence `A02_LEGACY_RECORDS_CHECK_2026-11-06.md`). HISTORICAL: the records describe a working tree at commit `e7bf477`, with an uncommitted change set; that commit is not in the clone.

| Record | MATCH | PARTLY | DIFFERS | Outside A02 | Not checkable | Paper-only | Total |
|---|---|---|---|---|---|---|---|
| `01_SYSTEM_OVERVIEW.md` | 17 | 4 | 0 | 1 | 2 | 0 | 24 |
| `02_REPOSITORY_AND_FILE_MAP.md` | 135 | 6 | 6 | 5 | 1 | 1 | 154 |
| `03_STARTUP_RUNTIME_AND_SCHEDULER.md` | 28 | 6 | 2 | 4 | 1 | 0 | 41 |
| `03A_CRON_REGISTRY_TABLE.md` | 0 | 0 | 0 | 6 | 0 | 0 | 6 |
| `LEGACY_SYSTEM_MANUAL_INDEX.md` | 1 | 1 | 0 | 2 | 5 | 0 | 9 |
| All five | 181 | 17 | 8 | 18 | 9 | 1 | 234 |

The eight statements the topic finds wrong (DIFFERS), with the correction; the AUDIT confirmed four, the five `sr_shadow/` statements counting as one (AUDIT 2.3, concern 22):

- **R2-19:** at the baseline 90 modules import the loader, 61 of them tests, not 94.
- **R2-74 and R2-104 to R2-107:** the `sr_shadow/` modules do not exist at the baseline.
- **R3-04:** a bare `load_dotenv()` searches from the calling file's directory, not the working directory (INTERPRETATION of python-dotenv).
- **R3-21:** `system_config.yaml` has 42 top-level keys, not 43.

Of the 17 PARTLY results, 7 point to A02 conflicts recorded in the AUDIT and 10 are precision differences of the testing copy (AUDIT 2.3, concern 22); they are listed in the records-check evidence, section 4. The records leave eight questions open; the baseline code answers seven, and one remains an OPEN QUESTION about library semantics (section 22).

## 8. What the study could not establish

UNKNOWN / NOT ESTABLISHED (STUDY 13.3, condensed): which configuration files and values were in force on either VM, whether any tracked file was edited there, and whether production ran any commit after `7d4970a`; the VM's time zone, so the year the loader used for the holiday file, and whether a process ever crossed a year boundary; which environment variables each process had (systemd, cron, `.env`), and whether the named SMTP and e-mail-fallback variables existed; the library and Python versions installed on the VMs; whether the revert script was ever run, and on which files; whether any boot failed on configuration, which exit codes occurred and how many keys the validator reported; whether the direction-registry state file, the SSH operator baseline, the dashboard overlay or any systemd drop-in existed, and what they held; which rows the snapshot table held, and whether the snapshot or CONFIG_DIFF paths ever ran. OPEN QUESTION (library semantics, not repository code): pydantic's handling of shared class-level default instances at the pinned version.

---

## Part B — Audit conclusions

## 9. Method and totals

- The AUDIT compared what the code does with what was intended, for every area and flow of A02, not only individual settings (Document 04, section 5; Document 08, section 6). Every intent source the admitted evidence holds was collected in the evidence file `A02_AUDIT_INTENT_SOURCES_2026-11-06.md`: 149 sources by area (IS-01 to IS-149), 48 conflicts between sources (IC-01 to IC-48), 34 statements that only the code contradicts (CD-01 to CD-34; CD-30 to CD-34 are the records' DIFFERS) and 25 statements attributed to Rama or the operator (RS-01 to RS-25, HISTORICAL). Every legacy source is HISTORICAL; where sources conflict, both are recorded and none is chosen; where no source states the intent, the record says so and audits the code on its own (Document 04, section 5.3).
- Method rules applied alike to every item (AUDIT 1.6): an ISSUE is a difference from intended behaviour, a conflict between sources that the code resolves one way, or, where intent is not established, a defect or weakness that the code itself demonstrates, with its basis named; a lack of intent evidence alone does not make an ISSUE; an item with a MATCH part and an ISSUE part counts as ISSUE; a finding inside another topic's code is a handoff, and A02 counts only its own part; the KNOWN DEFECT rule is the A01 AUDIT's four conditions, unchanged; library semantics are INTERPRETATION.
- **Totals (AUDIT 1.8):**

| Part | MATCH | ISSUE | UNKNOWN / NOT ESTABLISHED | KNOWN DEFECT (within ISSUE) |
|---|---|---|---|---|
| L — the central loader and schema | 29 | 17 | 1 (L-18) | 0 |
| V — validator, auditor, snapshot, change detection | 39 | 12 | 3 (V-14, V-15, V-16) | 0 |
| T — strategy configuration | 23 | 20 | 1 (T-21) | 1 (T-01) |
| F — files, environment, revert script | 22 | 19 | 3 (F-15, F-25, F-26) | 1 (F-20) |
| K — configured settings to consumers | 36 | 34 | 0 | 0 |
| X-01, added at assembly | 0 | 1 | 0 | 0 |
| **All** | **149** | **103** | **8** | **2** |

- Not counted: F-02 and F-05, merged into T-02 and T-19; F-18 (INFORMATION) and F-19 (WITHDRAWN); part K's nine coverage rows; the pointer rows to A01 items. V-12 is a MATCH; V-14 and F-15 are UNKNOWN / NOT ESTABLISHED.
- By key (part K): of the 362 leaves of `system_config.yaml`, `broker_limits.yaml`, `broker_costs.yaml` and `slippage_model.yaml`, 261 match, 96 are in ISSUE items and 5 are paper-only. Locked decisions S1 to S15 (part T): MATCH for S1, S2, S3, S7, S12, S14 and S15; ISSUE for S4, S5, S6, S8, S9, S10, S11 and S13.
- The STUDY's 22 concerns were each re-checked and given a disposition (AUDIT 2.3); stale line references in comments were rejected as issues, as A01 did.
- Every ISSUE and UNKNOWN item is entered, with its fields, in the Audit Findings Register (111 A02 entries). The 10 findings that needed Rama's intent or decision to classify or to settle a conflict (F-22, T-08, T-09, T-10, T-11, V-08, V-14, K-03, K-07 for its stop-loss-offset part, K-34) are the Open Issues Register's entries A02-01 to A02-05 and A02-08 to A02-12, with 11 questions for Rama (A02-01 has three subtopics, two answered by evidence; A02-08 has two questions). A02-06 and A02-07 were withdrawn on 08-Nov-2026, and their IDs are not reused. A02-13 to A02-17 hold the STUDY's questions 4, 5, 7, 8 and 10, which the AUDIT kept as OPEN QUESTIONs without needing them to classify; they were raised with Rama on 09-Nov-2026 (section 14).

## 10. The two KNOWN DEFECTs (provisional)

Each meets the four conditions of AUDIT 1.6 as its record states: the code has a mechanism for the case; by the language's semantics it fails for certain whenever the case occurs; the case is one the code or an intent source says it handles, and it can arise under the documented set-up; and the outcome contradicts every intent source found. Both were marked provisional until the review and the issue discussion; Rama has decided to keep both provisional (batch T3, group G1, qualification 1; batch T4, group G1). Promotion is not authorised unless and until the required detailed review is made and the classification is reconsidered under the project's governance (section 22). Whether either occurred in production is UNKNOWN / NOT ESTABLISHED.

| ID | KNOWN DEFECT (provisional) | Treatment (Part C) |
|---|---|---|
| T-01 (sub-cases (i) and (ii); latent with the committed files) | `validate_strategy` lets a `UnicodeDecodeError` from a non-UTF-8 file and a `TypeError` from a non-string top-level key escape, instead of raising `ConfigSchemaError` as locked decision S8 requires; A02's part of A01 S-39 | batch T3, group G1 |
| F-20 (both parts) | the revert script's "TEMP" test is a plain substring test: at the baseline it matches the word "ATTEMPT", so it reports six active entries in a file with no TEMP marker; after an apply it matches its own "REVERTED from TEMP" comment, so the re-scan it asks for can never be clean | batch T4, group G1 |

KNOWN DEFECT was considered and not given in other records, each stating the failing condition: for example F-22 (condition (b) fails: the stale table value is applied as written), V-01 (condition (b)), V-06 (conditions (c) and (d)), L-01, L-02 and L-08 (condition (d)), and most part K blocks (condition (a): no mechanism consults the key) (AUDIT 5.6 to 9.6).

## 11. The ISSUEs, by subject

The 103 ISSUEs were put to Rama in five batches by area, each group with Claude's recommendation and ChatGPT's suggested choice (Part C). Ten findings were decided with their Open Issues Register entries. Each finding's line, fields and treatment are in the Audit Findings Register; its full record is in AUDIT sections 5.3 to 9.3 and 9.8. KNOWN DEFECTs are marked (KD).

**Batch T1, the central loader (17; AUDIT 5.3):**

- **G1 — dates and times at load (5):** L-01, L-02, L-03, L-06, L-17. Conclusion: one holiday year, fixed at import from the host-local date, and required by every load; the load-time MIS timing check uses a literal poll interval; special sessions are checked by type only, and the documented example fails the load; the MIS timing defaults are the values that the 03-Sep change replaced; validator messages describe a stricter format than the code checks.
- **G2 — required settings and code defaults (2):** L-04, L-13. Conclusion: "no defaults, all required" against 289 code defaults; defaults and field sets stated in instructions and decisions that the schema does not follow.
- **G3 — strict validation (6):** L-09, L-10, L-11, L-12, L-14, L-15. Conclusion: duplicate keys accepted, last value winning; lax coercion against "no coercion"; NaN and infinity pass validators that state a range; constraints stated in comments and decisions not enforced; mapping-typed fields accept any keys; credential-name fields accept any string, an empty one included.
- **G4 — load failure handling (2):** L-07, L-08. Conclusion: a missing key and a YAML parse error give unexpected classes; some failures leave `load_all` outside the two documented classes.
- **G5 — structure and descriptions (2):** L-05, L-16. Conclusion: the module's split rule is not applied; the docstring calls it the loader for all non-strategy YAML files.

**Batch T2, the validator, auditor, snapshot and change detection (12; AUDIT 6.3):**

- **V-08, decided with A02-08:** what the auditor does not inspect: the delivery counterparts of the keys C1, C3, C4 and C5 check, and 33 of the 42 `SystemConfig` sections and the seven other sub-configurations.
- **G1 — the key-usage validator (3):** V-01, V-02, V-03. Conclusion: never fed, so every key is reported unaccessed and drift is never detected; it registers less than "all config values"; its docstrings describe a method, a gate and a usage the code does not have.
- **G2 — the auditor (5):** V-04, V-05, V-06, V-07, V-09. Conclusion: its descriptions of callers, startup groups, logging and context differ from the code; B5 is a BLOCK in a group documented as WARN-only; swallowed probe errors let the A5 boot gate pass silently and show a skipped group B as PASS; slippage-override symbols are never checked where the documents say they are; G1 measures the entry window against the end-of-day backstop.
- **G3 — the daily snapshot (2):** V-10, V-11. Conclusion: the snapshot omits the strategy configuration and every file outside the registry; its duplicate check keys on date and hash only.
- **G4 — what the snapshot logs (1):** V-13. Conclusion: the snapshotter logs the broker account identifier, contrary to its docstring.

**Batch T3, strategy configuration (20; AUDIT 7.3):**

- **T-08 to T-11, decided with A02-02 to A02-05:** S5 ("every field declared") neither met nor enforced (T-08); S6 against the three positional files (T-09); S13 against the intraday files, the gap_go stop-loss (T-10); entry windows, where the file values, their comments and other sources disagree (T-11).
- **G1 — loading strategy files (5):** T-01 (KD), T-03, T-04, T-05, T-16. Conclusion: not every failure raises the documented error (S8); a missing or empty directory blocks the boot without the alert; a duplicate `name` silently replaces an earlier strategy; repeated loads against S9 "loaded once"; a "path-free" error description that returns the path.
- **G2 — value rules and units (3):** T-06, T-07, T-12. Conclusion: the S4 percentage rule and type-only fields; differing `*_pct` units inside the schema; ATR methods accepted that the consumer does not implement.
- **G3 — unread fields, side readers and cross-checks (4):** T-02, T-14, T-15, T-20. Conclusion: the S10 cross-check is never requested although the header says it runs at startup; configured fields that nothing reads (A02's part of the A07 handoff); raw readers without the schema; `scoring_weights.yaml` called "the single source" while copies and fallbacks exist.
- **G4 — out-of-date descriptions (4):** T-13, T-17, T-18, T-19. Conclusion: texts still describe the removed DELIVERY-to-INTRADAY rewrite; S11's import list omits pydantic; the strategy guide describes a schema the code no longer has; the direction registry is called "auto-maintained" while production never writes it.

**Batch T4, the files, the environment and the revert script (19; AUDIT 8.3):**

- **F-22, decided with A02-01:** the revert table's "production" values differ from the file values and the later sources (the daily loss limit 0.03 and `gap_fade_long.min_score` 0 are answered by evidence; the revert procedure's history is OPEN).
- **G1 — the TEMP revert tool (4):** F-20 (KD), F-21, F-23, F-24. Conclusion: the substring "TEMP" test; unanchored, section-blind patterns; a report that prints the table's values; an in-place write without a backup or value check that deletes the line's comment.
- **G2 — configuration files outside the loader and their headers (9):** F-01, F-03, F-04, F-06, F-07, F-08, F-09, F-11, F-12. Conclusion: headers naming consumers or behaviour that do not exist (`slippage_model.yaml`, `expected_managers.yaml`, `security.yaml`, `preflight.yaml`, a "config_overrides" file); a required scanner file whose values cannot reach the check it serves; `security.yaml` read without validation; `--config` honoured by only some readers; four hand-kept required-file lists.
- **G3 — environment variable names (5):** F-10, F-13, F-14, F-16, F-17. Conclusion: a plaintext SMTP password field accepted in every mode; credential names configured in one place, listed in three and required differently (A01 C12); the template omits 20 names the code reads, among them names that scheduled processes require; credential names from two sources; the template's account status disagrees with `accounts.csv`.

**Batch T5, configured settings and their consumers (35; AUDIT 9.3, 9.8):**

- **K-03, K-07 (its stop-loss-offset part) and K-34, decided with A02-10, A02-11 and A02-12:** two sources state different fill-monitor cadences; the crash-recovery stop uses a fixed offset constant; the slippage model has no Live consumer and its sources disagree on its role. K-07's emergency-exit-buffer part is in G2.
- **G1 — settings that govern nothing (12):** K-01, K-08, K-09, K-13, K-14, K-18, K-25, K-26, K-28, K-29, K-30, K-32. Conclusion: the `broker` section, four keys not passed, the performance multipliers, the pipeline timeout, `auto_resume_kill_switch`, `whitelist_only`, `regime.index_symbol`, two watchlist keys, the smart-target master switch, the entry-gate liquidity check (configured on, never run), the three live-feed reconnect keys and two `broker_limits.yaml` keys reach no acting consumer.
- **G2 — values bypassed by fixed numbers or copies (12):** K-02, K-06, K-07 (emergency-exit-buffer part), K-10, K-11, K-15, K-19, K-20, K-23, K-27, K-31, K-33. Conclusion: trading hours held as literals and in the dashboard's copy; broker product codes compared as literals; exit paths using a code constant; a fixed leverage ceiling in the auditor; pre-flight's own port and back-pressure threshold; 33 notifier call sites ignoring the YAML alert settings; SMTP settings held twice with different meanings; the sentinel directory written by literals; a queue size not governed by its key; threshold names and values shared across files, with the dashboard showing the wrong one; three copies of the F&O ban URL, where a load failure drops `fail_closed`; cost rates copied into the daily report.
- **G3 — settings read in different ways (8):** K-04, K-05, K-12, K-16, K-17, K-21, K-22, K-24. Conclusion: `excluded_symbols` read two ways; the delivery-gate flags read with different predicates and defaults; consumer floors and fallbacks replacing loaded values; `alerts.telegram.enabled` read with opposite failure rules; the dashboard reading a non-existent key; `_pct` meaning a fraction or a percentage; a misnamed stop-loss-buffer path and an untied duplicate; a key reused across sections and a lookback key that does not set its fetch.
- **G4 — a stale comment (1):** X-01. Conclusion: the webhook bind comment still rests the all-interfaces bind on `require_hmac=true`, which the file sets false.

## 12. UNKNOWN / NOT ESTABLISHED items

- **L-18:** whether commit `5f75c9b` and the 03-Sep MIS values were ever in force (changed after the last recorded deployment).
- **V-14:** change detection does not see the strategy files, `accounts.csv` or any other file outside the registry, and no source states whether it should (A02-09 keeps Rama's Phase 2 input).
- **V-15:** what the validator and the auditor reported on production boots.
- **V-16:** what the snapshot table held, and whether the CONFIG_DIFF path ran.
- **T-21:** the strategy configuration in force in production (with the scanner URLs' status, section 6, row 6).
- **F-15:** how `.env` reached each process; three mechanisms with different parsing rules exist.
- **F-25:** whether the revert script was ever run, and on which files.
- **F-26:** which environment each process had, and whether the absent files existed on the VM.

UNKNOWN components inside counted items are noted in K-19, K-20 and K-29.

## 13. Intent-source conflicts

The conflicts between intent sources are recorded, not resolved, unless a later source names or replaces the earlier one (AUDIT 1.6, 3; evidence file, IC-01 to IC-48). Those that bear most on Live behaviour:

| Conflict | Sources | Items |
|---|---|---|
| IC-32, the value of `risk.daily_loss_limit_pct` | 0.05 in the revert table, the TEMP tracker and a test fixture; 0.03 in the file, the BUILD 1 commit and the system map | F-22: answered by the later-dated sources (0.03; A02-01 (a)) |
| IC-33, the value of `gap_fade_long.min_score` | 60 in the revert table; 0 in the file, restored by commit `1e41f99` | F-22: answered by evidence (0; A02-01 (c)) |
| IC-06 to IC-08, `force_intraday_only` and `delivery_enabled` | the configuration comments and the guide (the flag rewrites strategies; delivery "stays false") against the loader comment of 10-Jul-2026 and the 04-Aug-2026 commit (no rewrite; delivery on) | T-13 |
| IC-25 and IC-26, the validator's strictness and the startup auditor groups | CV3's "exit(1)" against "only warn"; "ACEG" against "ACG" | V-03, V-04 |
| IC-39 and IC-40, the cron and script notifiers' Telegram settings and the live-feed reconnect limits | the locked decisions route each setting in two ways; the code follows one source in each case | K-15, K-30 |
| IC-38, webhook authentication | the bind comment (27-Apr-2026) against the `require_hmac` value and its comment (02-Jul-2026) | X-01 |

Where the code follows one side of a conflict, the item is an ISSUE; where a history question was needed, it went to Rama (Part C).

## 14. The STUDY's questions 1 to 10

Each question was checked against all admitted evidence before any question went to Rama (AUDIT 11). ANSWERED BY EVIDENCE: 2 (questions 2 and 3). Retained as OPEN QUESTION: 7, of which 6 were narrowed by the evidence and 1 split into four items. NO LONGER MATERIAL: 1 (question 9, by Rama's instruction of 08-Nov-2026).

| Q | Disposition (AUDIT 11) | Where it went |
|---|---|---|
| 1 the daily loss limit and the revert step | OPEN QUESTION, narrowed: the limit (0.03) and `gap_fade_long.min_score` (0) answered by evidence; the revert procedure kept for Rama | A02-01 |
| 2 the entry-gate liquidity check | ANSWERED BY EVIDENCE: every source intends the check on | K-29 (batch T5, group G1) |
| 3 `smart_tgt.enabled` and `auto_resume_kill_switch` | ANSWERED BY EVIDENCE: both were meant to control the behaviour | K-14, K-28 (batch T5, group G1) |
| 4 webhook authentication | OPEN QUESTION, narrowed: the later source sets `require_hmac` false; the bind's premise is not stated | X-01 (batch T5, group G4); the receiver's design to A06; history: A02-13 |
| 5 the cron and script notifiers' Telegram settings | OPEN QUESTION, narrowed to the reach of TASK-10's Option A | K-15 (batch T5, group G2); history: A02-14 |
| 6 the strategy files and the locked decisions | OPEN QUESTION, split into T-08, T-09, T-10 and T-11 | A02-02 to A02-05 |
| 7 broker selection and the fallback keys | OPEN QUESTION, narrowed: scaffold or live switch | K-01 (batch T5, group G1); history: A02-15 |
| 8 the holiday calendar | OPEN QUESTION, narrowed: as A01 R9(a) and R10, plus the loader's host-local year | L-01 (batch T1, group G1); A01-09, A01-20; history: A02-16 |
| 9 sensitive data in tracked configuration and in the snapshot | NO LONGER MATERIAL: F-18 is INFORMATION and V-12 a MATCH | none |
| 10 the key-usage validator | OPEN QUESTION, narrowed to the intended end state of the non-strict warning | V-01 (batch T2, group G1); history: A02-17 |

Questions 4, 5, 7, 8 and 10 were not needed to classify their findings, and Rama's treatment of each finding answers the new-system side (Part C). ChatGPT's package review of 09-Nov-2026 found that their history had not been put to Rama (finding M-01); they were raised with him the same day (batch 3), he kept all five OPEN ("Keep all five OPEN"), and they are A02-13 to A02-17 (section 19).

## 15. Cross-topic handoffs

### 15.1 The A01 handoffs to A02

A01's classification, treatment and owner boundary are unchanged in every row (D-30); A02 recorded only its own part (AUDIT 4).

| A01 item (A01 result) | A02 part | A02 disposition |
|---|---|---|
| C7d (ISSUE) | V-49 (MATCH: the hashed set can lose a key only at a year change); V-14 (UNKNOWN / NOT ESTABLISHED: files outside the registry are never hashed) | confirmed for the configuration side, narrowed to the year rename |
| C10a (ISSUE) | L-01 (the holiday-file year fixed at import from the host-local date) | confirmed; the VM's time zone UNKNOWN / NOT ESTABLISHED |
| C10b (ISSUE) | L-01 (the current year's file only; no fallback year) | confirmed for the configuration side |
| C12 (ISSUE) | L-15; F-13, F-14, F-16 | confirmed; the exit codes are A01's |
| C35 (ISSUE) | L-03 (type only; the commented example, uncommented as written, fails the load with exit 5) | confirmed, with the exit-5 addition |
| S-11 (KNOWN DEFECT) | pointer only; V-46 (MATCH: the W0 snapshot is not meant to alert) | nothing to add |
| S-24 (MATCH) | V-10 to V-13 and V-43 to V-47 | placement unchanged; content audited here |
| W-17 (MATCH) | V-01, V-03, V-18 | confirmed: warn-only; the drift branch unreachable |
| M-19 (ISSUE) | L-46 | confirmed |
| M-20 (ISSUE) | L-07; V-01 (`ConfigValidationError` raised in code but unreachable) | confirmed, with the unreachable-raise addition |
| M-24 (ISSUE) | L-02; V-01 | confirmed |

C10c (the holiday guard's own parser) is not an A01-to-A02 handoff: A01 hands it to A17, which owns it; the AUDIT cross-references A02's holiday-file part only, without reclassifying it (AUDIT 4).

### 15.2 A02 items handed to other topics

A02 keeps and counts its own part of each item; the owner traces its consumer's logic and records any finding there, and a finding is counted once (AUDIT 10). Index by owner topic:

| Owner | A02 items handed over |
|---|---|
| A01 | L-02, L-15, L-44, V-01, V-40, V-47, V-50, T-01, T-02, T-03, T-11, T-13, T-15, F-04, F-08, F-11, F-15, K-02, K-20, K-28, K-36 |
| A03 | V-11, V-12 |
| A04 | L-31, L-44, F-14, F-16, K-01, K-03, K-05, K-06, K-21, K-32, K-34 |
| A05 | F-14, F-35, K-30, K-31 |
| A06 | T-02, T-07, T-12, T-14, F-11, K-02, K-04, K-05, K-09, K-12, K-13, K-22, K-49, X-01 |
| A07 | V-06, V-23, T-14, T-20, F-11, K-05, K-27 |
| A08 | K-02, K-21, K-22, K-23, K-24, K-25, K-26 |
| A09 | V-27, V-33, K-06, K-08, K-09 |
| A10 | L-14, L-44, V-07, V-31, T-14, K-08, K-21, K-28, K-29 |
| A11 | T-14, K-07, K-12, K-21, K-22, K-28 |
| A12 | L-02, L-06, V-09, T-05, F-11, F-14, K-06, K-07, K-12, K-14, K-21 |
| A13 | K-06, K-14 |
| A14 | L-15, V-42, F-14, K-15, K-16, K-19, K-20 |
| A15 | V-05, V-07, V-11, V-41, V-54, T-15, T-20, F-04, F-07, F-11, F-34, F-40, K-02, K-04, K-05, K-08, K-09, K-17, K-19, K-20, K-27, K-33, K-72 |
| A16 | T-19, F-15, K-05, K-20 |
| A17 | F-07, F-15, K-20 |
| A18 | T-20, K-21, K-24, K-25, K-26, K-27 |
| A19 | F-16, K-02, K-07 |
| A20 | L-09, V-05, V-06, V-07, V-41, V-42, V-54, F-07, F-12, F-13, F-16, K-11 |

Handed off as OPEN QUESTIONs or tests for their owners (AUDIT 14; STUDY 6.3): `strategy_will_trade` behind V-06 (A07); the `trailing_sl_*` guard and the order protocol behind T-14 (A10 and A11); the dashboard's reads in K-17 and the status-table claim in K-05 (A15 and A16).

---

## Part C — Rama's decisions

## 16. How the decisions were made

- **The intent questions (Document 04, section 5.5):** the 11 questions of the 10 Open Issues Register entries were raised with Rama in two batches on 08-Nov-2026 and answered the same day; the corrected read-back was confirmed the same day ("All confirmed"). ChatGPT reviewed both batches and the read-back. Committed at `8392d19`.
- **The treatment round, 09-Nov-2026:** the 103 ISSUEs were put to Rama in five batches by area (T1 the loader; T2 the validator, auditor and snapshot; T3 the strategy files; T4 the files, the environment and the revert script; T5 the settings and their consumers). Each batch grouped its findings, each group with Claude's recommendation; ChatGPT reviewed each batch and suggested a choice with its qualifications; Rama chose, in every batch adopting ChatGPT's suggestions (batch T1 by his own decision file, prepared in the ChatGPT chat after he accepted ChatGPT's recommendations); each batch's record was read back to him and confirmed, with two corrections (batch T1, group G1, qualification 2, corrected to "Preserve A01-18 as agreed on 05-Nov-2026"; batch T5, group G1's owner topics, A07 removed, which owns none of those findings). ChatGPT reviewed each read-back and each final diff before its commit. Committed at `71eccd7` (T1 and T2), `5286656` (T3), `e82482a` (T4) and `ededc7f` (T5).
- **Batch 3, 09-Nov-2026:** after ChatGPT's package review of the same day (finding M-01), the STUDY's questions 4, 5, 7, 8 and 10, which the AUDIT had kept as OPEN QUESTIONs without needing them to classify, were put to Rama as history questions; he kept all five OPEN ("Keep all five OPEN"). They are A02-13 to A02-17; their findings' treatments had already been decided in the treatment round.
- The discussion itself is not kept (Document 07, section 3; D-17). The Open Issues Register and the Audit Findings Register quote the words that decide each item, and they govern; this Part summarises them.
- What is recorded in Part C is of two kinds, kept apart: Rama's answers about how the legacy system was meant to work (an intent source, Document 04, section 5.1, not a FACT about the code), and Rama's treatments for the new system (Phase 2 input; not V2 design decisions).

## 17. Rama's statements about the legacy system

- Rama answered OPEN to every one of the 16 history questions put to him: the 11 of 08-Nov-2026 (A02-01 (b), A02-02 to A02-05, A02-08 (a) and (b), A02-09 to A02-12) and the five of batch 3, 09-Nov-2026 (A02-13 to A02-17). No historical answer is inferred from evidence leans, from his new-system inputs or from recommendations (section 19).
- A02-01 (a) and (c) are answered by evidence, not by Rama: the daily loss limit is 0.03 (commit `c69f1fd`, 24-Jun-2026, later than the revert table, the tracker and the guide) and `gap_fade_long.min_score` is 0 (commit `1e41f99`, 08-Jun-2026).
- Rama has made no statement to this project about A02 behaviour beyond these answers (AUDIT 3). The RS entries of the intent-sources evidence are HISTORICAL statements attributed to him or the operator in legacy documents.

## 18. Treatments for the new system (Phase 2 input)

### 18.1 The discussion entries

Summaries only; the Open Issues Register quotes each input in his words and governs. Each of the ten entries below has a treatment that is AGREED in part (the Phase 2 input, confirmed in the read-back of 08-Nov-2026 as accurately recorded) and OPEN QUESTION in part (its design details, left for Phase 2).

| Entry | AUDIT IDs | Rama's new-system input, in brief | Left for Phase 2 |
|---|---|---|---|
| A02-01 | F-22 | no paper mode, no TEMP settings, no revert procedure and no files for them; just-in-time or wrong temporary changes are not carried into operation | the design details |
| A02-02 | T-08 | every setting read from the relevant configuration files (such as `config.yaml` and `strategy.yaml`); no hardcoded settings, no code defaults as an alternative source, no settings read from `.py` files | handling required settings, validation and missing values without a silent fallback; organising strategy configuration |
| A02-03 | T-09 | the legacy stop-loss and target mechanism is scrapped; new rules are set per strategy once the new strategies and filters are settled; ATR is not decided | the new per-strategy rules |
| A02-04 | T-10 | the legacy strategies, filters, targets and stop-losses are scrapped; neither gap_go value (1.0% or 1.2%) is approved | the new strategy, stop-loss and target rules |
| A02-05 | T-11 | `config.yaml` time is the master; each `strategy.yaml` time is supplementary; the earlier cut-off governs (his example: 14:30 against 15:00 gives 14:30); the same principle for the morning start | the exact morning-start rule; missing, invalid or conflicting times |
| A02-08 | V-08 | (a) validation covers the applicable settings of every enabled trading mode, the delivery counterparts included where delivery is enabled, and a proposed guardrail: an immediate warning to Rama before a stop-loss percentage above 10% is accepted; (b) the broadest practicable configuration audit, hardcoded values included | the design details |
| A02-09 | V-14 | broader change detection over the configuration and strategy sources that can affect trading, risk, eligibility, routing or execution, with an alert that never exposes sensitive values | the monitored inventory, the fingerprint method, alert timing and severity, acknowledgement, authorised changes |
| A02-10 | K-03 | fills detected fast enough to protect positions within the broker's limits; reliable broker updates preferred, controlled polling as a fallback; maximum delay, retries, back-off and degraded mode defined | any interval (neither 2 s nor 15 s is chosen) |
| A02-11 | K-07 (stop-loss offset) | normal and crash-recovery stops use the same approved configuration and rules, with no separate silent offset; a missing or invalid setting gives a clear error and an approved safe response | the implementation details |
| A02-12 | K-34 | estimated and actual costs kept distinct; actual Live cost and P&L from the broker's fills and charges; estimates never shown as actual charges | whether or how estimates feed any Live decision metric |

A02-13 to A02-17 (batch 3) hold history questions only: Rama gave no new input, and each entry's treatment is its finding's agreed treatment (A02-13, X-01: batch T5, group G4; A02-14, K-15: batch T5, group G2; A02-15, K-01: batch T5, group G1; A02-16, L-01: batch T1, group G1; A02-17, V-01: batch T2, group G1).

### 18.2 The treatment groups of the 103 ISSUEs

Rama's choices (09-Nov-2026), with the qualifications he adopted; the Audit Findings Register quotes each in full and governs. "A" is accept; "B" is accept with qualifications.

| Batch, group | Choice | The treatment, in brief |
|---|---|---|
| T1 G1, dates and times at load | B | the common IST time and calendar authority and configured values; strict date and time checks; special-session data validated separately from deciding trading; except that the missing-next-year calendar policy stays OPEN under A01-09, A01-18 is preserved as agreed, and no new timing schedule is invented |
| T1 G2, required settings and code defaults | A | every setting from configuration files; no hardcoding or code defaults; a missing setting fails clearly, naming file and key; any intended default lives in the file; the legacy defaults are a finding, not a list of new defaults |
| T1 G3, strict validation | B | duplicate keys refused; strict types; NaN and infinity refused where finite values are required; mapping keys validated against what they refer to; credential names validated and required variables checked without exposing values; only current authoritative rules enforced; optional integrations not made mandatory |
| T1 G4, load failure handling | B | one written failure contract naming file and key; A01 group A's permanent and transient distinction kept; permanent errors not retried; safe, actionable messages |
| T1 G5, structure and descriptions | B | one authoritative loading and validation boundary, which need not be one large file; every in-scope file accounted for; A01's module-size rules; accurate descriptions; strategy configuration under the same contract |
| T2, V-08 | with A02-08 | as A02-08 |
| T2 G1, the key-usage validator | A | no setting silently unused; settings for enabled features have a consumer, settings of disabled features may be dormant under an explicit contract, unknown settings are rejected or reported; any usage checker is fed by real reads and claims no false coverage |
| T2 G2, the auditor | B | one written rule inventory; a check that did not run is NOT RUN, never PASS; a required safety gate that cannot complete fails closed; every check gets its inputs; timing against the configured schedule (A02-05); A02-08's coverage kept |
| T2 G3, the daily snapshot | A | the snapshot represents the complete configuration actually loaded, strategy files included; A→B→A changes visible; never a secret value; schema, fingerprint and retention for Phase 2 |
| T2 G4, what the snapshot logs | A | descriptions match what is logged; one written logging contract in Phase 2; current log fields are not approved by default |
| T3, T-08 to T-11 | with A02-02 to A02-05 | as those entries, with the scope Rama adopted on 09-Nov-2026 |
| T3 G1, loading strategy files | B | one governed strategy boundary and failure contract; encoding and key errors as named failures; a missing folder alerted; unique names matching file stems; T-01's KNOWN DEFECT stays provisional; the loading lifecycle reconciled with A01 C11 and A12, not decided by A02 alone; an error-message contract |
| T3 G2, value rules and units | B | values validated at load; no method without a supported consumer; a field-by-field contract for range and meaning, not one blanket rule; one canonical percentage convention where practicable; ATR not approved for V2 |
| T3 G3, unread fields, side readers, cross-checks | B | every required setting has a consumer, unsupported settings rejected, dormant settings under an explicit contract; the scanner map checked against the strategies before trading; consumers use governed configuration; one source for weights and thresholds, signal-age thresholds included; consumer conclusions stay with their owners |
| T3 G4, out-of-date descriptions | A | documents and headers state the actual contract; stale claims not carried forward; no permission to edit the legacy system or rewrite its decision records |
| T4, F-22 | with A02-01 | as A02-01; (a) and (c) answered by evidence; (b)'s history OPEN |
| T4 G1, the TEMP revert tool | A | confirms A02-01's input; nothing in the dead legacy system is edited; F-20's KNOWN DEFECT stays provisional; the governed change path, alerting and snapshot are Phase 2 work, reconciled with A02-09 and T2 G3 |
| T4 G2, files outside the loader | B | one authoritative inventory of configuration files with owner and readers; every file validated through the governed boundary; one configuration context for every reader, not a decision on CLI or layout; per-process ownership without an unsafe shared object; F-03 stays UNKNOWN; `security.yaml` readers to A17; no legacy file edited |
| T4 G3, environment variable names | B | one declared inventory of required variable names by process and feature, derived from configuration; presence checked at the right boundary without ever showing a value; optional-feature variables required only when the feature is on; secrets only from the environment; accounts as A01-03 and A01-24; F-15 and F-26 stay UNKNOWN |
| T5, K-03, K-07 (stop-loss offset), K-34 | with A02-10 to A02-12 | as those entries; no interval chosen; K-07 recorded in two parts |
| T5 G1, settings that govern nothing | A | every setting has a working consumer or is refused; dormant settings only under an explicit, validated contract and never as a fallback; a safety control shown as on really acts; consumer design with the owner topics |
| T5 G2, values bypassed by fixed numbers or copies | B | one authoritative source per value, with explicit unit and meaning; no operational copies in code, dashboards, pre-flight or reports; one alert configuration for every notifier; fail-closed stays fail-closed; not one giant file or global object; K-07's buffer separate from its offset; K-02 reconciled with A02-05 and A01's time decisions |
| T5 G3, settings read in different ways | B | one semantic contract per setting (meaning, unit, type, range, default policy, failure rule) applied by every consumer; no silent raising, replacing or reinterpreting; no silent fraction-percentage conversion; no new code defaults; a missing or misspelled key fails with a named error |
| T5 G4, a stale comment | A | comments state current premises; the receiver's binding and authentication are A06's to establish in Phase 2; documentation only |

In the Audit Findings Register, the 111 A02 entries stand at: AGREED 94; AGREED in part and OPEN QUESTION in part 9 (V-08, T-08, T-09, T-10, T-11, F-22, K-03, K-07, K-34), their open parts tracked by A02-01 to A02-05, A02-08 and A02-10 to A02-12; UNKNOWN / NOT ESTABLISHED, with no treatment, 8. Every ISSUE has an agreed treatment or an agreed link to the Open Issues Register.

---

## Part D — Unresolved OPEN items

Every item below stays visible here and in the registers until it is resolved or Rama decides it (Document 05, section 11.3), and is carried forward to the topics named and to Phase 2 (Document 04, section 12).

## 19. History questions OPEN (16)

OPEN QUESTION. Rama answered OPEN (08-Nov-2026; batch 3, 09-Nov-2026), and no answer is inferred. The legacy facts stay as the AUDIT records them.

| Entry | The question that stays open |
|---|---|
| A02-01 (b) | was the deployment guide's general TEMP-revert procedure still meant to be followed at the switch from Paper to Live after the June changes and, if so, did its scope exclude the daily-loss entry superseded by the 3% authority? |
| A02-02 | does locked decision S5 ("every strategy YAML must explicitly declare all fields") still govern the strategy files? |
| A02-03 | do S6's ATR stop-loss and target methods remain the intent for the three positional strategies? |
| A02-04 | which gap_go stop-loss was intended: S13's 0.01 or the files' 0.012? |
| A02-05 | was the uniform 15:00 entry end of 15 strategy files meant to be temporary, and which entry windows were intended for Live? |
| A02-08 (a) | were C1, C3, C4 and C5 meant to audit the delivery counterparts of the intraday keys they check? |
| A02-08 (b) | which auditor coverage beyond the listed rules was intended? |
| A02-09 | was configuration-change detection meant to cover the strategy files and `accounts.csv`? |
| A02-10 | which fill-monitor cadence was intended: P14's 15 seconds, or the file's and M14's 2 seconds? |
| A02-11 | was the crash-recovery path's fixed stop-loss offset constant meant to ignore the configured offset? |
| A02-12 | was the slippage model meant to enter Live cost calculations? |
| A02-13 | after `require_hmac` was set false, was the webhook receiver's all-interfaces bind meant to rest on the URL token check alone? |
| A02-14 | were the YAML Telegram settings meant to apply to the script, cron, control-tower and report notifiers, or did TASK-10's Option A leave all but the on/off switch out of them? |
| A02-15 | was the `broker` section meant to be a live switch, or scaffolding for later? |
| A02-16 | was requiring the current year's holiday file only the intended year-end behaviour, and was the loader's host-local year meant to differ from the IST clock? |
| A02-17 | was the key-usage validator meant to be fed by every consumer, or was the non-strict warning the intended end state? |

## 20. Treatments OPEN

- **OPEN in part:** the design details of each of the ten entries A02-01 to A02-05 and A02-08 to A02-12 (section 18.1, last column), left by Rama for Phase 2; the 9 Audit Findings Register entries AGREED in part carry these open parts.
- **Design work left open inside agreed treatments:** many agreed treatments state what they do not decide and leave it to Phase 2 or to an owner topic (for example the missing-next-year calendar policy under A01-09; the snapshot's schema, fingerprint and retention; the configuration-root contract; the loading lifecycle with A01 C11 and A12; the logging contract; consumer-side designs with their owner topics). These are recorded in the Audit Findings Register with each treatment and are not separate open issues.
- No ISSUE is without a treatment or a link: unlike A01's C32, no A02 finding was left with its treatment wholly OPEN.

## 21. UNKNOWN / NOT ESTABLISHED items carried forward

L-18, V-14, V-15, V-16, T-21, F-15, F-25 and F-26 (section 12), the UNKNOWN components of K-19, K-20 and K-29, and the STUDY's list of what cannot be established (section 8). They stay UNKNOWN / NOT ESTABLISHED unless surviving runtime evidence is found (Document 06, section 4.2).

## 22. Classifications, handoffs and ownership points carried forward

- **The two provisional KNOWN DEFECTs (T-01 and F-20):** they stay KNOWN DEFECT (provisional), as Rama decided (batch T3, group G1, qualification 1: "Do not promote it to final without the required detailed review"; batch T4, group G1: "Keep F-20's KNOWN DEFECT classification provisional"). No detailed review has been made. Promotion is not authorised unless and until the required detailed review is made and the classification is reconsidered under the project's governance; the legacy code is not changed and the revert script is not run.
- The cross-topic handoffs of section 15.2 are carried to each owner topic, which examines its side when it is opened (D-23). When an owner topic records a fact that changes an A02 finding, the finding is updated in the Audit Findings Register (Document 05, section 11.1, update timing 5).
- OPEN QUESTIONs handed to owner topics: `strategy_will_trade` (A07, V-06); the `trailing_sl_*` guard and the strategy `order_protocol` with no reader (A10 and A11, T-14); the dashboard's reads and the status-table claim (A15 and A16, K-17 and K-05).
- C10c stays A17's (A01 RECONCILED TOPIC RECORD, section 15); A02 recorded its holiday-file part only.
- A01's open issues that bear on A02 stay under A01: A01-09 (the calendar failure behaviour) and A01-20 (the VM-independent time basis), cross-referenced by batch T1, group G1 and L-01.
- OPEN QUESTION, library semantics for later topics: pydantic's handling of shared class-level default instances at the pinned version (STUDY 13.3, item 10; records check, section 2.6).

## 23. Closure position

ChatGPT reviewed every file of the package on 09-Nov-2026: its first review did not pass the package (M-01, the five unasked history questions; M-02, the provisional KNOWN DEFECT status); after their correction, its fresh review of the revised package passed it the same day. Rama approved the package on 09-Nov-2026 (D-31). Before the review A02 was IN PROGRESS; with it, UNDER REVIEW. The remaining topic statuses are RECONCILED, APPROVED BY RAMA, PUSH VERIFIED and CLOSED (Document 10, section 4). This record does not close the topic; closure follows the verified commit (Document 04, sections 4 and 11; Document 07, section 6).

Document 04, section 11 (before closure):

| Condition | Position |
|---|---|
| required investigation complete | the STUDY and the AUDIT are complete for the 58 paths and Document 08 item 17; what cannot be established is UNKNOWN / NOT ESTABLISHED by the runtime-evidence limit (sections 2, 8 and 12), not by an omitted step |
| the audit complete for every area and flow | 260 items audited, matches included (section 9) |
| every issue raised with Rama, with its agreed treatment or OPEN status | the 11 intent questions raised and answered (08-Nov-2026); the 103 ISSUEs raised and decided in five batches (09-Nov-2026); the five history questions of batch 3 raised and kept OPEN (09-Nov-2026) (Part C) |
| study and audit reconciled | this record (sections 6 and 7) |
| unknowns and open questions recorded | Part D |
| ChatGPT's review of every package file | done, 09-Nov-2026 (first review NOT PASSED: M-01, M-02; fresh review of the revised package PASS) |
| Rama's approval of the topic document and package | approved, 09-Nov-2026 (D-31) |
| committed, and the commit verified by ChatGPT | pending |
| topic status updated | pending (Topic Completion Register) |

Document 05, section 11.2 (closing with unresolved issues), as it applies to A02:

- Every issue has been raised and discussed with Rama, and he has explicitly left each unresolved part OPEN: the 16 history questions and the design details of the ten entries A02-01 to A02-05 and A02-08 to A02-12.
- Each such issue is recorded in the Open Issues Register with its question, evidence, impact, owner and next action, and is shown here: the 15 entries meet this.
- The topic's entry in the Topic Completion Register lists its open issues: yes.
- The evidence and the required coverage are otherwise complete: yes, within the runtime-evidence limit; no material evidence gap, unreviewed contradiction or issue that makes the findings unreliable is known.

## 24. Evidence index

The topic folder is `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A02_CONFIGURATION_AND_EFFECTIVE_SETTINGS/`. The hashes are those of the files as approved: their status and revision lines changed at approval, and nothing else (the line numbers that the Audit Findings Register cites are unchanged). The evidence files substantiate the STUDY and the AUDIT; they are not competing narratives (Document 07, section 5).

| File | Content last changed | SHA-256 (as approved) | What it holds |
|---|---|---|---|
| `A02_STUDY_2026-11-06.md` | `5d43484` | 33a0331325ae819931c8568a9812299a2555f53dee0039a8c8d74e5bd8b465b9 | the STUDY |
| `A02_AUDIT_2026-11-08.md` | `2a96068` | 0b1588d976c3cc617dd2ec58737b9045115568ae350d8b1e46c31dc2e6cee2ac | the AUDIT |
| `evidence/A02_SOURCE_FILE_INVENTORY_2026-11-06.md` | `6fc3c5d` | ecc6906fdb0e79c18e0011574433464aaabb2f844e051fdb6297e7d258c889f4 | the 58 paths: size, Git object, hash, history; the changes after the last recorded deployment |
| `evidence/A02_CONFIG_LOADER_SCHEMA_AND_FLOW_2026-11-06.md` | `d3a2724` | 053191736cabc97132f0742bff0a08a25e008d9b46af85b0f47ecd8a320f93ce | the loader: the 65 models field by field, the load flow, defaults, errors, precedence, callers |
| `evidence/A02_VALIDATOR_AUDITOR_AND_SNAPSHOTTER_2026-11-06.md` | `d3a2724` | 0221df9d2057be925e0ff3680160fa71766ea8f22b19eee9624ce479f41310d3 | the validator, the auditor, the snapshot, the hashes, the exposure paths |
| `evidence/A02_STRATEGY_CONFIGURATION_2026-11-06.md` | `d3a2724` | 305f1f62cdf64072ffcf584f4290d54e505deab4c394f73bb121fe4227f1630d | the strategy schema and loader, the 16 files, the locked decisions, the direction registry, `scoring_weights.yaml` |
| `evidence/A02_CONFIG_FILES_ENVIRONMENT_AND_REVERT_SCRIPT_2026-11-06.md` | `d3a2724` | 0cf8035b4f16fad122c1cde2e4879748311a5a9e8a7c0652d4391d115a0acec6 | the 50 files, sensitive locations (by path only), absent files, outside sources, environment variables, the revert script |
| `evidence/A02_KEY_CONSUMER_MAP_PART1_2026-11-06.md` | `d3a2724` | 0618d80a7f2ac508941b88f11df8303731734f27e8256cc105d4c0a0323563de | the key-to-consumer map of `system_config.yaml` L1 to L358 |
| `evidence/A02_KEY_CONSUMER_MAP_PART2_2026-11-06.md` | `d3a2724` | 56e9166e1e5c447375e594c71184bf5de517c10eaecbfa53d8e013baf67a2c60 | the map of `system_config.yaml` L359 to L753 and six more files |
| `evidence/A02_LEGACY_RECORDS_CHECK_2026-11-06.md` | `d3a2724` | 344cb6543d602373dc4992748f07e3b528019035a3f69a4055127910da007653 | the five existing records' configuration claims against the code (section 7) |
| `evidence/A02_AUDIT_INTENT_SOURCES_2026-11-06.md` | `d3a2724` | 34d96d43de4f42ddb3a47b6c793d6d1a8e718c775cfb82711d1b2804731c05e8 | the intent sources (IS), conflicts (IC), code-only contradictions (CD) and statements attributed to Rama or the operator (RS) |

Registers: the Open Issues Register (`OPEN_ISSUES_REGISTER_2026-11-05.md`; entries A02-01 to A02-05 and A02-08 to A02-17) and the Audit Findings Register (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`; 111 A02 entries and the A02 treatment decisions), in `doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/`.
