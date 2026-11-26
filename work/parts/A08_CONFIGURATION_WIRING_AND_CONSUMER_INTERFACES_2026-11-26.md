# A08 evidence: configuration keys, `main.py` wiring and every consumer interface
**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26.
**Purpose and scope:** Part P06 of the A08 STUDY fieldwork, the cross-cutting part. It records once (1) every key of the `sr_detector:` block of `config/system_config.yaml` (L508 to L545) and the structure-exit switch `structure_exit_enabled` (L634): committed value, comment, loader field, default, validation, every reader, unit and fallback; (2) the A08 wiring in `main.py` (A01's file, interface only): what is built under which switch, in which order, what a failure leaves, and the start and shutdown order, with a switch-combination table derived from the code's conditions; (3) one consolidated table of every consumer interface of A08 code in other topics' files; (4) the corrections to the A08 inventory found so far and in this part; (5) A08's side of the inherited items whose primary part is P06 (A01 C13, C37, B-11; A02 K-21, K-25, K-26; A03 U-24; A06 PQ-09), P06's side of its secondary items, the facts of the unassigned rows A03 H-44, U-59, U-60 and the records A01 C40 and A02 K-32, and a sweep of the approved A01 to A07 AUDIT files for records that touch A08 code without naming A08. Boundaries (D-41): the configuration files and loader are A02's, `main.py` is A01's and every consumer file is its owner's; they are recorded at the interface only (P3). The behaviour of the A08 objects is cited from the checked parts P01 to P05 and P07 by statement ID and is not re-described. For `continue_from_retest` only the A08-specific handoff is recorded (P1). Inherited items keep their IDs, owners, classifications, treatments and statuses (P4). No V2 design.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-26 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced.

## 1. Method, sources and boundaries

- P06-S001 FACT (governing sources read, not edited): the COMMON brief and the P06 part brief in `<workspace>/briefs/`; the checked parts in `<workspace>/parts/`: P01 (`A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md`), P02 (`A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md`), P03 (`A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md`), P04 (`A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md`), P05 (`A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md`) and P07 (`A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md`), cited by statement ID; Rama's working decisions of 26-Nov-2026 (`<workspace>/notes/RAMA_DECISIONS_A08_STUDY.md`); in `<algocore_system clone>` at `52cc811`: the A08 inventory (`.../A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md`, cited as "A08 inventory, section n") and the approved A01 to A07 AUDIT files (cited by record ID and line).
- P06-S002 FACT (legacy reading list; `<legacy clone>` at `970aabf`, read with `git show 970aabf:<path>`): `config/system_config.yaml` L500 to L640; `core/config_loader.py` L1 to L40, L1140 to L1260, L1575 to L1612, L1980 to L2025, L2440 to L2516; `main.py` L385 to L440, L1590 to L1830, L3405 to L3620, L3660 to L3840, L3862 to L3900, L3960 to L3980, L4240 to L4293; `screening/retest_monitor.py` L264 to L302, L352 to L360; `sr_detector/__init__.py` L25 to L70; `sr_detector/detector.py` L70 to L102; `sr_detector/zones.py` L50 to L56; `sr_detector/confluence.py` L168 to L177; `sr_detector/flags.py` L138 to L146; `sr_detector/models.py` L100 to L112; `sr_detector/retest_confirm.py` L50 to L62, L88 to L96, L128 to L137; `signals/signal_processor.py` L1036 to L1058, L2436 to L2443; `orders/structure_exit_manager.py` L118 to L140; `core/config_auditor.py` L210 to L245; `config/expected_managers.yaml` L112 to L126; `core/evidence_contract.py` L228 to L256; `ops_dashboard/backend/services/audit.py` L60 to L100, `config_view.py` L1 to L60, `system_logs.py` L70 to L84; `scripts/check_cron_drift.py` L60 to L68; `PATHS.md` L384 to L420; `docs/SYSTEM_MAP.md` L234, L487; `docs/audit/integrity_audit_2026.md` L448 to L455, L730 to L735, L803 to L806; `git blame` of `config/system_config.yaml` L508 to L545 and L633 to L634 and of the `main.py` wiring lines; `git log -S` of the switch values.
- P06-S003 FACT (searches; every repository-wide search carried the four exclusions `':(exclude)config/accounts.csv' ':(exclude,glob)**/.env*' ':(exclude,glob)**/*.local.yaml' ':(exclude,glob)**/*token*.json'`): (a) one `git grep -n -w <key>` per field of `SRDetectorConfig` and of the structure-exit switch over every `*.py` file, test files listed separately, the script kept as `<workspace>/notes/P06_keygrep.sh`; for the generic names (`enabled`, `timeframes`, `lookback_days`, `cache_ttl_sec`, `max_queue`, `sl_buffer_pct`) a quoted or attribute-qualified pattern, each hit read; (b) `git grep -n sr_detector` outside the package, `tests/`, `docs/` and the Markdown files; (c) importers of `sr_detector` and `screening.retest_monitor` and every mention of the three script names, over the whole tree; (d) the table and status names `sr_detector_results`, `retest_state`, `RETEST_`; (e) the A08 inventory's section 7 test search re-run with every public A08 name (the top-level classes, functions and constants of the thirteen modules, P06-S115); (f) a sweep of the seven approved AUDIT files by `<workspace>/notes/P06_audit_sweep.py` (`python3 -I`, reading only the algocore files): each record from its `####`/`#####` heading to the next heading, and each table row whose first cell is an ID, kept when it contains an A08 path or public name and not the word "A08", its raw output kept as `<workspace>/notes/P06_audit_sweep_raw.txt`; a second pass added the words "S&R", "support/resistance", "retest", `RETEST_` and "SNR-".
- P06-S004 FACT (what was not done): no legacy file, test, script or SQL was run or imported; no endpoint was contacted; `config/accounts.csv`, `.env*`, `*.local.yaml` and `*token*.json` files were not opened. The paper branch of `main.py` `_build_market_data_kite` (L406 to L418) names a session-token file; it is recorded only as the existence of that branch (A01's, A04's), and Live is the only mode in scope (project instruction 9). The cron line of the backfill contains a machine path, which is described, not copied.
- P06-S005 FACT (boundaries applied, D-41): `config/system_config.yaml` and `core/config_loader.py` are A02's; `main.py` is A01's; the consumer files are their owners' (A03, A05, A06, A07, A10, A11, A12, A15, A18, A19); each is recorded at the interface only (the call, the contract passed, the gating flag, what the consumer receives) (P3). The behaviour of A08's own objects is the other parts' and is cited, not re-described. `continue_from_retest` (A06's file) is recorded only for the A08-specific handoff (P1; P04 section 8). Inherited items: A08's side only, every ID, owner, classification, treatment and status unchanged (P4).
- P06-S006 FACT (Document 06, section 4.2; COMMON brief, section 4): committed configuration values are values in the file; whether any was in force on a legacy machine is UNKNOWN / NOT ESTABLISHED, both machines being terminated with no surviving log, database or journal (P07-S109). The A08 inventory, section 6, records that no A08 file changed between the last recorded deployment `7d4970a26991fd40774023f5293a00556228e14b` and the baseline; whether `config/system_config.yaml` and `main.py` changed there was not checked in this part, and which commit production ran is UNKNOWN / NOT ESTABLISHED (D-21).
- P06-S007 FACT (the local-overlay question of the brief): the trading process's loader `core/config_loader.py` `load_all` (L2457 to L2516) reads exactly the eight files of `_CONFIG_FILES` (L2441 to L2450) from `config_dir`, hashes the raw bytes, parses each with `yaml.safe_load` and validates it with `model_validate`; it has no merge step and no overlay file; its docstring states "CL5 — No env-var interpolation, no includes. yaml.safe_load() only." (L20). The only `*.local.yaml` overlay mechanism the search found concerns the operations dashboard's own configuration (a git-ignored overlay named in `UNPUSHED_LEDGER.md` L523, L567; `ops_dashboard/.gitignore` L8), not the trading configuration; it was not opened or traced (not an A08 path; owner not traced here). So no overlay can change an `sr_detector` key inside the trading process by the loader's code.
- P06-S008 FACT (statement and label rules): one bullet per statement, IDs `P06-Snnn` never renumbered; labels FACT, UNKNOWN / NOT ESTABLISHED, INTERPRETATION, HISTORICAL and OPEN QUESTION as the COMMON brief defines them; tests are stated expectations only (A19); legacy documents and comments are data, cited as HISTORICAL; nothing in this part is a finding.

## 2. The configuration block: key-by-key table

(to be filled: section 2)

## 3. Keys without readers, readers without keys, and default disagreements across layers

(to be filled: section 3)

## 4. `main.py` wiring: construction, switches, order, failure handling

(to be filled: section 4)

## 5. Start and shutdown order of the A08 objects

(to be filled: section 5)

## 6. Switch combinations and the A08 objects they produce

(to be filled: section 6)

## 7. Consolidated consumer-interface table (all topics)

(to be filled: section 7)

## 8. Inventory corrections (facts)

(to be filled: section 8)

## 9. Inherited items: P06's primary items, then its secondary items; the unassigned rows and records; the sweep

(to be filled: section 9)

## 10. Stated intent: comments, documents, history

(to be filled: section 10)

## 11. Points for the AUDIT

(to be filled: section 11)

## 12. UNKNOWN / NOT ESTABLISHED items

(to be filled: section 12)

## 13. Questions about intent for Rama

(to be filled: section 13)

## 14. Cross-references to other parts and topics

(to be filled: section 14)
