# Master System Investigation Index

**Status:** APPROVED — Pre-Phase Deliverable 4, content proposed by ChatGPT (Decision Register, D-13 and D-16) and kept by Claude; approved by Rama on 2026-11-04 at the Pre-Phase → Phase 1 gate (D-27). A change to its topics, order or scope needs Rama's approval (Document 05, section 11.1).
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: compiled by Claude from ChatGPT's index proposal of 04-Nov-2026 and from ChatGPT's reviews of Pre-Phase checkpoint 5 (topic A20; the owners of three `core/` files; the rule for the legacy project's own documents; a complete script crosswalk) and of Claude's `scripts/` function map (the owner of every script, with seven placements settled), and with ChatGPT's corrections from its review of the draft index (file ownership inside another topic's folder; `deploy/token_watcher.sh`; the seven package `__init__.py` files; the prerequisites of A20 and A19; index rule 9). Those proposals and reviews are not kept as files (D-17). Updated, 2026-11-04: rule 9, the prerequisites of A20 and section 6, items 1 and 2, record Rama's decisions on the topic sequence, OI-04 and OI-07 (Decision Register, D-23 to D-25). Approved, 2026-11-04: by Rama, with the other Pre-Phase deliverables, at the Pre-Phase → Phase 1 gate (Decision Register, D-27); status line only.
**Purpose and scope:** The list of Phase 1 topics (Document 02, section 2). For each topic: its scope, the components and paths it covers, the coverage items of Document 08, section 3 that it serves, its study prerequisites and its order (Document 10, section 1; D-16). The paths are candidate ownership boundaries. This index is not authority to begin Phase 1, and no topic starts before the Pre-Phase → Phase 1 gate is passed.
**Basis and labels:** Study baseline: trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21). Governing methodology: Document 08, Revision 5. ChatGPT proposes the content, Claude keeps the file, and Rama approves the index at the gate (Document 05, section 11.1). Labels follow Document 04, section 6.
**Evidence:** Source Inventory, SRC-10 (the legacy repository at the baseline). The file names, module docstrings, `config/cron_registry.yaml`, the units in `deploy/systemd/` and the imports in `main.py`, read at the baseline for Claude's path check and `scripts/` function map of 04-Nov-2026 (handoffs, not kept; D-17). No module implementation was read, and nothing was run.

## 1. Index rules

1. One owning topic per component or path. Other topics cite the owner and record their own boundary handoff; they do not duplicate the component's full investigation. Where a specifically listed file is assigned to a topic different from the topic that broadly covers its parent folder, the file's named topic owns the file; the parent-folder topic cites it as a boundary. Folder coverage does not override explicit file ownership.
2. "Study prerequisites" means the order needed to make a reliable investigation. It is not a claim that the source code has a one-way dependency. The import graph remains a separate evidence map.
3. Every topic covers all applicable Document 08 evidence and audit standards, including inputs, calculations, overrides, guards, outputs, storage, handoffs, all routes, failures and actual-versus-intended behaviour.
4. Live only. Paper workflows are excluded; shared code is examined only where needed to establish Live behaviour.
5. All work is against the fixed production baseline. Changes after the last recorded deployment are noted, but production execution of later commits remains UNKNOWN / NOT ESTABLISHED.
6. The five existing technical records remain unchanged and are checked against production; they are not treated as production evidence.
7. `scripts/` files are assigned by the function they perform. The scheduler topic (A16) owns the schedule registry, cron declarations, watchdog and heartbeat, and the invocation map; the functional topics own the logic of their scripts. Every `scripts/` path is listed exactly once under its owning topic in Appendix A, or in S1 only for `scripts/__init__.py`.
8. `main.py` is owned by A01 for orchestration, startup phases, wiring and runtime control. Other topics cite relevant call sites without duplicating ownership.
9. Topic sequence (Rama, 04-Nov-2026; Decision Register, D-23): topics proceed one at a time, in the order in section 2. The next topic starts only after the preceding topic package has completed ChatGPT's review and Rama's approval; a package that Rama rejects is reworked, reviewed again by ChatGPT and approved by Rama first. The sequence is not evidence of a code dependency (rule 2).
10. Synthesis items S1 to S5 are deliverables built across the topic sequence; they are not separate module investigations.
11. The legacy project's own documents are cross-cutting historical sources, not code-component topics: `docs/` (all tracked files and subfolders); `tasks/lessons.md`; `README.md`, `PATHS.md`, `UNPUSHED_LEDGER.md`, `AGENTS.md` and `GEMINI.md`; `.gitignore` and `.gitattributes`. They are admitted repository material under the Source Inventory, but their statements are HISTORICAL and are checked against the production baseline. They do not govern this project, do not override the ten foundation documents, and do not become a separate topic for every legacy document. Relevant records are cited in the topic where they provide context; S1 inventories the complete repository file map; S3 consolidates the relevant historical findings.
12. The script descriptions and declared invocations of Appendix A are preliminary and source-derived (file names and docstrings), not verified behaviour. A declared invocation does not prove that a script ran; a dash does not prove that it was unused. No schedule, service, import or execution is inferred from them.

## 2. Proposed study order

| Order | Topic | Coverage items (Document 08, section 3) | Study prerequisites |
|---|---|---|---|
| P1 | A01 System orchestration, startup, runtime and shutdown | 1, 3, 20 | None |
| P1 | A02 Configuration and effective settings | 17 | None |
| P1 | A03 Database, persistence, migrations and backups | 16 | A01, A02 |
| P2 | A04 Broker interface, authentication and broker state | 10, 13, 18 | A01 to A03 |
| P2 | A05 Market data, instruments and external reference data | 4 | A01 to A04 |
| P3 | A06 Signal intake and webhook lifecycle | 5 | A01 to A03 |
| P3 | A07 Strategies, screening, filtering and trade decision | 5, 6 | A02, A05, A06 |
| P3 | A08 Technical analysis, S&R and retest context | 7 | A05; A07 for the screening/retest boundary |
| P4 | A09 Entry price, R:R, sizing, risk and capital allocation | 8, 9 | A04, A07, A08 |
| P4 | A10 Order creation, placement and entry protocols | 10 | A04, A09 |
| P5 | A11 Position management, protection and trade exits | 11, 12 | A08 to A10 |
| P5 | A12 End-of-day, square-off, closure and reconciliation | 12, 13 | A04, A10, A11 |
| P6 | A13 Kill switch, circuit breakers, failure and recovery | 20 | A01, A09 to A12 |
| P6 | A14 Alerts and notifications | 14 | A01; A03 for persisted alert state |
| P6 | A15 Reports, logs, monitoring and evidence | 15 | A03, A14 |
| P7 | A16 Scheduler, cron registry and scheduled-job control | 3 | A01 to A03 |
| P7 | A17 Deployment, environment, security controls and dependencies | 18 | A01, A04, A16 |
| P7, after A17 | A20 Pre-flight orchestration and readiness checks | 3, 20 | A01 to A17 (provisional) |
| P8 | A18 V3, shadow and allocation extensions | 5, 6, 9 | A05, A07 to A09 |
| P9 | A19 Testing, test infrastructure and validation | 19 | A01 to A18, and A20 |
| Across | S1 to S5, synthesis deliverables (section 4) | 2, 21 to 24 | Built across the topic sequence |

## 3. Topics

### A01 — System orchestration, startup, runtime and shutdown

- **Order:** P1.
- **Scope:** process entry, orchestration, lifecycle, runtime loop, startup checks, shutdown, time authority and top-level wiring.
- **Paths:** `main.py` (orchestration and wiring); `utils/startup_checks.py`; `utils/instance_lock.py`; `utils/holiday_guard.py`; `core/time_authority.py`; `core/market_windows.py`; `core/events.py`; `core/ids.py`; `core/exceptions.py`; `core/constants.py`; `core/account_registry.py`; `core/__init__.py` and `utils/__init__.py` (package initialisation and exports; provisional, see S1); `scripts/`: 2 files (Appendix A).
- **Coverage:** 1; 3 (startup and runtime); 20 (startup and shutdown boundary).
- **Prerequisites:** none.
- **Boundary:** startup configuration and database initialisation are cross-referenced to A02 and A03; the broker session to A04; subsystem behaviour to the owning topics. The health endpoint (`scripts/healthcheck_server.py`) is A15's; A01 may cite its startup import boundary.

### A02 — Configuration and effective settings

- **Order:** P1.
- **Scope:** configuration sources, schemas, validation, defaults, precedence, environment-variable names, strategy configuration loading and snapshots.
- **Paths:** `config/` (all YAML and CSV, except `config/cron_registry.yaml`, which A16 owns); `core/config_loader.py`; `core/config_validator.py`; `core/config_auditor.py`; `core/config_snapshotter.py`; `strategies/schema.py`; `strategies/loader.py`; `.env.example` (keys only; never values); `scripts/`: 1 file (Appendix A).
- **Coverage:** 17; supporting evidence for 5 to 14 and 18.
- **Prerequisites:** none.
- **Boundary:** configuration is the intended or configured side of every topic; each later topic traces where its settings are actually read, overridden or ignored. A02 cites `config/cron_registry.yaml` (A16) as a cross-topic boundary and does not duplicate its investigation.

### A03 — Database, persistence, migrations and backups

- **Order:** P1.
- **Scope:** database schemas, state-store access, the analytics database, migrations, transactions, persistence contracts, and backup, retention and restore declarations.
- **Paths:** `core/state_store.py`; `core/schema.sql`; `core/analytics_schema.sql`; `core/db_connect.py`; `core/migrations.py`; the `data_store/` and `logs/` persistence paths (runtime paths named in configuration, not tracked folders at the baseline); `scripts/`: 6 files (Appendix A), the backup, retention, restore-drill and WAL-checkpoint scripts, whose schedule declarations are referenced by A16.
- **Coverage:** 16; supporting evidence for 15 and 20.
- **Prerequisites:** A01, A02.
- **Boundary:** each topic identifies its tables and columns and its write and read handoffs; A03 owns the storage implementation, not the business meaning of every stored field.

### A04 — Broker interface, authentication and broker state

- **Order:** P2.
- **Scope:** the Zerodha API interface, the authentication and token lifecycle, rate limits, product resolution, broker order, position and margin reads, broker-side state translation and the broker adapter boundaries.
- **Paths:** `broker/` (`zerodha_adapter.py`, `rate_limiter.py`, `order_monitor.py`, `order_state_machine.py`, `token_monitor.py`, `auth_recovery.py`, `product_resolver.py`, `cost_calculator.py`, `slippage_engine.py`, `clock_skew_probe.py`, `position_helpers.py`, `angelone_adapter.py`); `deploy/token_watcher.sh` (the whole file, including its token and authentication behaviour; A13 cites its restart contract); `deploy/zerodha_morning.bat`; `deploy/zerodha_morning.ps1`; `scripts/`: 3 files (Appendix A).
- **Coverage:** 10 (broker interface); 13 (broker state); 18 (credential handling, by type and location only).
- **Prerequisites:** A01 to A03.
- **Boundary:** A04 owns the broker protocol and broker-state mapping; A10 to A12 own the system's order and position lifecycle decisions and the reconciliation use of broker state.

### A05 — Market data, instruments and external reference data

- **Order:** P2.
- **Scope:** live feed, tick and candle construction, historical candle access, the instrument cache, external reference-data sources and market-data storage handoffs.
- **Paths:** `data/live_feed.py`; `data/candle_store.py`; `core/instrument_cache.py`; `core/candle_math.py` (the candle construction and calculation boundary); the historical-data integration call sites in `main.py`; `scripts/`: 4 files (Appendix A), including instrument refresh, daily candles and F&O ban-list acquisition.
- **Coverage:** 4.
- **Prerequisites:** A01 to A04.
- **Boundary:** A05 owns data acquisition and normalisation; A08 owns the technical-analysis use of market data; A15 owns the monitoring and reporting of data-quality telemetry.

### A06 — Signal intake and webhook lifecycle

- **Order:** P3.
- **Scope:** scanner and webhook ingress, authentication and validation, deduplication, throttling, queueing, expiry and signal event creation.
- **Paths:** `signals/` (`webhook_receiver.py`, `signal_processor.py`, `entry_throttle.py`); the Chartink integration and configuration references; the relevant `main.py` wiring call sites; `scripts/`: 1 file (Appendix A), the scanner-URL reachability check.
- **Coverage:** 5 (signal intake).
- **Prerequisites:** A01 to A03.
- **Boundary:** A06 ends at the accepted or queued signal handed to A07; downstream trade-decision logic is A07's. A06 keeps scanner-URL reachability; the pre-flight framework is A20's.

### A07 — Strategies, screening, filtering and trade decision

- **Order:** P3.
- **Scope:** strategy selection and controls, secondary screening, hard gates, quality scoring, entry gates, step execution, rejection and acceptance outcomes, and the decision handoff.
- **Paths:** `strategies/` (`control.py`, `taxonomy.py`; `schema.py` and `loader.py` are A02's); `screening/` (`secondary_screener.py`, `hard_gate.py`, `quality_scorer.py`, `entry_gate.py`, `step_executor.py`); `core/strategy_direction.py`; `strategies/__init__.py` and `screening/__init__.py` (package initialisation and exports; provisional, see S1); the relevant `regime/` and `v3_chain/` integration call sites; `scripts/`: 3 files (Appendix A).
- **Coverage:** 5 (strategy definition and use); 6.
- **Prerequisites:** A02, A05, A06.
- **Boundary:** A07 owns the decision to accept, reject or advance a signal; A08 owns the technical-analysis and S&R calculations; A09 owns the entry, R:R, risk and capital decisions. A09 may cite the capital and governor handoff of `scripts/compute_strategy_metrics.py`.

### A08 — Technical analysis, S&R and retest context

- **Order:** P3.
- **Scope:** S&R detection, levels and zones, retest monitoring, and the technical context consumed by entry, risk and exit decisions.
- **Paths:** `sr_detector/`; `screening/retest_monitor.py`; the S&R consumers in `orders/` (consumer call sites only; the owning logic stays with A11 where it is an exit manager); `scripts/`: 3 files (Appendix A).
- **Coverage:** 7.
- **Prerequisites:** A05; A07 for the screening and retest boundary.
- **Boundary:** A08 owns the calculation and production of S&R information; downstream consumers cite its output and are investigated in their own topics.

### A09 — Entry price, R:R, sizing, risk and capital allocation

- **Order:** P4.
- **Scope:** entry-price derivation, price math, buffers, stop-loss, target and R:R inputs, position quantity, capital reservation, commit and release, risk limits, invariants, drift and strategy allocation.
- **Paths:** `capital/` (`position_sizer.py`, `risk_engine.py`, `fund_manager.py`, `invariant.py`, `drift_handler.py`, `strategy_governor.py`, `performance_allocator.py`, `shadow_engine.py`); `orders/price_math.py`; the relevant configuration keys in A02; the V3 allocation references owned by A18.
- **Coverage:** 8, 9.
- **Prerequisites:** A04, A07, A08.
- **Boundary:** A09 owns the price, sizing, risk and capital decisions; A10 owns order submission and lifecycle.

### A10 — Order creation, placement and entry protocols

- **Order:** P4.
- **Scope:** order construction, entry orchestration, order placement, the CO and limit protocols, broker submission, acknowledgements and entry-stage state transitions.
- **Paths:** `orders/order_placer.py`; `orders/order_manager.py`; `orders/order_protocol_co.py`; `orders/order_protocol_limit.py`; `orders/entry_engine.py`; `orders/full_entry_engine.py`; the broker submission call sites (A04 owns the adapter implementation).
- **Coverage:** 10.
- **Prerequisites:** A04, A09.
- **Boundary:** A10 ends at the accepted, working or filled order and its handoff to position management; A04 owns the broker protocol, and A11 owns post-entry protection and management.

### A11 — Position management, protection and trade exits

- **Order:** P5.
- **Scope:** the open-position lifecycle, stop-loss and target management, breakeven, stop-loss breach handling, structure exits, retries, CNC GTT protection and post-entry trade state.
- **Paths:** `orders/smart_tgt_manager.py`; `orders/breakeven_manager.py`; `orders/sl_breach_monitor.py`; `orders/structure_exit_manager.py`; `orders/tgt_retry_manager.py`; `orders/slippage_recorder.py`; `orders/shadow_tracker.py`; `orders/cnc_gtt.py`; `orders/cnc_gtt_monitor.py`.
- **Coverage:** 11; 12 (position and exit side).
- **Prerequisites:** A08 to A10.
- **Boundary:** A11 owns per-position protection and exit decisions; A12 owns the session close, square-off orchestration and reconciliation. A11 may cite the trade-management data boundary of `scripts/reconstruct_excursions.py` (A15) and the CNC GTT behaviour under test in `scripts/t2_cnc_gtt_realtest.py` (A19).

### A12 — End-of-day, square-off, closure and reconciliation

- **Order:** P5.
- **Scope:** the end-of-day lifecycle, MIS auto-square-off, end-of-day square-off, closure classification, local and broker reconciliation, residual positions and the next-session handoff.
- **Paths:** `orders/eod_squareoff.py`; `orders/mis_autosquareoff.py`; `orders/order_reconciler.py`; `orders/closure_classifier.py`; `core/mis_squareoff_timing.py`; `core/mis_blocklist.py`; `core/closure_source.py`; `scripts/`: 6 files (Appendix A), the end-of-day and reconciliation scripts (functional logic only).
- **Coverage:** 12 (session close); 13 (reconciliation and broker state).
- **Prerequisites:** A04, A10, A11.
- **Boundary:** A12 owns the close and reconciliation workflow; A04 owns the broker protocol; A03 owns persistence.

### A13 — Kill switch, circuit breakers, failure and recovery

- **Order:** P6.
- **Scope:** kill-switch modes and state, circuit-breaker triggers, halt and resume paths, failure callbacks, restart contracts, recovery and safe state restoration.
- **Paths:** `capital/kill_switch.py`; the `main.py` failure callbacks (A01 owns general orchestration); `deploy/resume.sh`; `scripts/`: 1 file (Appendix A); the restart contract of `deploy/token_watcher.sh`, cited as a boundary only (A04 owns the whole file, including its token and authentication behaviour).
- **Coverage:** 20.
- **Prerequisites:** A01, A09 to A12.
- **Boundary:** A13 owns halt and recovery control; related failure behaviour in other topics is cross-referenced.

### A14 — Alerts and notifications

- **Order:** P6.
- **Scope:** alert creation, delivery contracts, Telegram and e-mail delivery, critical alerts, cron alerts and MIS square-off notifications.
- **Paths:** `alerts/` (`telegram_notifier.py`, `critical.py`, `delivery.py`, `cron_alerts.py`, `mis_squareoff_notifier.py`); `deploy/systemd/alert-watcher.service`; `scripts/`: 1 file (Appendix A); the alert call sites in other topics.
- **Coverage:** 14.
- **Prerequisites:** A01; A03 for persisted alert state.
- **Boundary:** A14 owns delivery and the alert lifecycle; event producers remain owned by their originating topics.

### A15 — Reports, logs, monitoring and evidence

- **Order:** P6.
- **Scope:** daily reports, trade review, signal-status reporting, structured logging, evidence contracts, telemetry, the Control Tower, the dashboard, the Gemini jobs and watchman, and the monitoring probes.
- **Paths:** `reports/`; `core/logger.py`; `core/evidence_contract.py`; `core/effect_telemetry.py`; `core/daily_stats.py`; `core/evidence_artefact_manifest.txt`; `ops/`; `ops_dashboard/`; `deploy/systemd/trading-watchman.service`; `scripts/`: 17 files (Appendix A), including `scripts/gemini_*.py`, the monitoring canary and the liveness probe.
- **Coverage:** 15.
- **Prerequisites:** A03, A14.
- **Boundary:** A15 owns the observability and reporting outputs; it does not re-own the underlying trading decisions or business records. A01 may cite the startup import of the health endpoint, and A11 the trade-management data boundary of the MFE/MAE reconstruction.

### A16 — Scheduler, cron registry and scheduled-job control

- **Order:** P7.
- **Scope:** the schedule source of truth, cron declarations, job enablement, watchdogs, drift detection, heartbeat, invocation, overlap and locking, and the schedule-to-script map.
- **Paths:** `config/cron_registry.yaml`; `core/cron_registry.py`; `deploy/cron/trading-system.cron`; `utils/cron_heartbeat.py`; `scripts/`: 5 files (Appendix A), the cron officer and its report renderer, the drift check, the watchdog and the crontab generator; the scheduled invocation declarations for `scripts/`.
- **Coverage:** 3 (scheduler side); supporting evidence for all scheduled functional topics.
- **Prerequisites:** A01 to A03.
- **Boundary:** A16 owns when and how a job is declared and invoked; the functional topics own what the job's business logic does. A schedule is never proof of execution.

### A17 — Deployment, environment, security controls and dependencies

- **Order:** P7.
- **Scope:** systemd units, deployment hooks, log rotation, VM and security configuration, runtime dependencies, environment-file declarations and credential-handling controls (no secret values).
- **Paths:** `deploy/` (systemd units, hooks, security settings, log rotation), except the files that other topics own (see Boundary); `requirements.txt`; `requirements-dev.txt`; `DEPLOYMENT.md` (HISTORICAL); the relevant environment-variable key declarations; `scripts/`: 6 files (Appendix A).
- **Coverage:** 18.
- **Prerequisites:** A01, A04, A16.
- **Boundary:** A17 owns the deployment and security declarations; actual installation and runtime state is UNKNOWN where surviving evidence does not establish it. D-07 governs the reporting and investigation limits until Phase 1 is complete. A17 cites as cross-topic boundaries, and does not duplicate the investigation of, the `deploy/` files that other topics own: `deploy/cron/trading-system.cron` (A16); `deploy/resume.sh` (A13); `deploy/systemd/alert-watcher.service` (A14); `deploy/systemd/trading-watchman.service` (A15); and `deploy/token_watcher.sh`, `deploy/zerodha_morning.bat` and `deploy/zerodha_morning.ps1` (A04).

### A20 — Pre-flight orchestration and readiness checks

- **Order:** P7, after A17 and before A18 (suggested position; the final order may be adjusted to respect dependencies).
- **Scope:** `scripts/preflight/` as a coherent subsystem: the orchestrator, phase dispatch, checks, sentinels, report and delivery, the startup hook and any autofix declaration.
- **Paths:** `scripts/preflight/` (20 files); `scripts/premarket_healthcheck.py` (deprecated predecessor). All 21 are listed in Appendix A.
- **Coverage:** principally 3 and 20; supporting references to 4, 5, 13, 16, 17, 18 and 19 where the pre-flight checks touch them.
- **Prerequisites:** A01 to A17 — provisional, reflecting the sequential study order (rule 9; D-23).
- **Boundary:** A20 owns the pre-flight framework and its check implementation. It cross-references A02, A03, A04, A06, A13 and A17 for the underlying configuration, database, broker, signal, recovery and deployment contracts, and does not duplicate those topics' investigation of the underlying modules. A16 owns the scheduler declarations, registry entries and invocation control; A20 records its schedule as a boundary reference to A16 and does not duplicate the scheduler audit. `scripts/premarket_healthcheck.py` is a deprecated predecessor and a historical replacement boundary; it is not treated as an active check merely because it exists. A20 does not absorb `scripts/preflight_scanner_check.py`, which remains A06's.

### A18 — V3, shadow and allocation extensions

- **Order:** P8.
- **Scope:** Live integration, activation controls, dependencies and data and state handoffs for regime detection, the V3 decision chain, the S&R shadow and the portfolio allocation extensions.
- **Paths:** `regime/`; `v3_chain/`; `allocation/`; the relevant configuration switches; the integration points in `signals/`, `screening/`, `capital/` and `main.py` (the owners of those integration call sites remain A01, A06, A07 and A09); `scripts/`: 3 files (Appendix A).
- **Coverage:** 5, 6 and 9, where applicable.
- **Prerequisites:** A05, A07 to A09.
- **Boundary:** distinguish repository presence, declared default-OFF or shadow intent, and actual Live activation; actual activation is UNKNOWN until established by evidence.

### A19 — Testing, test infrastructure and validation

- **Order:** P9.
- **Scope:** the test inventory, fixtures, test configuration, the test runner, validation tooling, and the relationship between test coverage and production behaviour.
- **Paths:** `tests/`; `run_tests.py`; `requirements-dev.txt` (the dependency declaration is A17's); `scripts/`: 4 files (Appendix A).
- **Coverage:** 19.
- **Prerequisites:** A01 to A18, and A20.
- **Boundary:** test presence or a test result does not prove production runtime behaviour. Tests are evidence of the tested claim only, at the stated commit and conditions. A11 may cite the CNC GTT behaviour under test in `scripts/t2_cnc_gtt_realtest.py`.

## 4. Synthesis deliverables (not module topics)

- **S1 — Repository and complete file map (item 2).** Re-base the map of SRC-41 from `e7bf477` to the fixed production baseline `970aabf`. Record all tracked paths and classify them by owning topic. Complete it progressively and verify it after A19. Appendix A is its crosswalk for `scripts/`. Listed in S1 only: `scripts/__init__.py`, and the empty package markers `capital/__init__.py`, `data/__init__.py` and `orders/__init__.py`. The non-empty package files `core/__init__.py` and `utils/__init__.py` (A01) and `strategies/__init__.py` and `screening/__init__.py` (A07) are assigned provisionally for package initialisation and exports, by the topic that owns the package's principal contents; this does not transfer ownership of the whole folder or its other files. S1 records all these paths in the complete repository map.
- **S2 — Complete end-to-end system walkthrough (item 21).** After the topic studies, reconcile the eight broad workflows with the actual traced paths, including the normal, rejection, error, retry, restart and end-of-day branches. Preserve the unknowns.
- **S3 — Known issues and historical findings (item 22).** Maintain a consolidated, evidence-backed view during the topic work, using the topic findings and HISTORICAL sources (rule 11). Do not treat the legacy documents or the five testing-derived technical records as production facts.
- **S4 — Legacy lessons and V2 inputs (item 23).** Prepare only at the end of Phase 1, after all topic findings and Rama's issue treatments are reconciled. This is input to Phase 2, not a V2 design.
- **S5 — Master manual index (item 24).** Maintain the index of completed topic documents throughout Phase 1; finalise it when the topic collection is complete.

## 5. Document 08 coverage crosswalk

| Item | Coverage item | Topics |
|---|---|---|
| 1 | System overview and architecture | A01, A03; S2 |
| 2 | Repository and complete file map | S1 |
| 3 | Startup, runtime and scheduler | A01, A16, A20 |
| 4 | Market data and data sources | A05 |
| 5 | Signals and strategies | A06, A07, A18 |
| 6 | Filtering and trade decision | A07, A18 |
| 7 | Technical analysis and S&R | A08 |
| 8 | Entry price and R:R | A09 |
| 9 | Risk and capital allocation | A09, A18 |
| 10 | Order processing | A04, A10 |
| 11 | Order and position management | A11 |
| 12 | Exits and square-off | A11, A12 |
| 13 | Reconciliation and broker state | A04, A12 |
| 14 | Alerts and notifications | A14 |
| 15 | Reports, logging and evidence | A15 |
| 16 | Database and storage | A03 |
| 17 | Configuration | A02 |
| 18 | Security, credentials and deployment | A04, A17 |
| 19 | Testing and validation | A19 |
| 20 | Failure, recovery and operational behaviour | A01, A13, A16, A17, A20 |
| 21 | Complete end-to-end system walkthrough | S2 |
| 22 | Known issues and historical findings | S3 |
| 23 | Legacy lessons and V2 inputs | S4 |
| 24 | Master manual index | S5 |

## 6. Open questions and index controls

1. OI-04 and OI-07 were settled by Rama on 04-Nov-2026 (Decision Register, D-24 and D-25): Document 05, section 11.2 sets when a topic may close with unresolved issues, and Document 07, section 5 names the topic documents.
2. The topic sequencing rule of index rule 9 was decided by Rama on 04-Nov-2026 (Decision Register, D-23).
3. Unknown cross-topic boundaries follow Document 10, section 6: UNKNOWNs are recorded in the topic record; only unresolved Phase 1 topic issues that need tracking are registered; one owner is cross-referenced rather than duplicated.
4. Rama may adjust the topic granularity at the gate. Any merge or split preserves coverage items 1 to 24 and the single-owner rule.
5. No topic starts before the Pre-Phase → Phase 1 gate is passed.

## Appendix A — `scripts/` crosswalk: owner of every file

All 88 files under `scripts/` at the baseline, each listed once under its owning topic (index rule 7); the seven placements that had two candidate topics were settled by ChatGPT on 04-Nov-2026. The function column is what the file's own documentation states (index rule 12): from the module docstring (D), the header comment of a shell or batch file (H), or the file name only where neither exists (N, a low-confidence INTERPRETATION). The declared invocation is a FACT about a declaration only: a job in `config/cron_registry.yaml` with its declared time, a unit in `deploy/systemd/`, or an import in `main.py`; "—" means none of these names the file. Credential values, machine paths and account identifiers that appear in some docstrings are left out.

Files per topic: A01 2, A02 1, A03 6, A04 3, A05 4, A06 1, A07 3, A08 3, A12 6, A13 1, A14 1, A15 17, A16 5, A17 6, A20 21, A18 3, A19 4, S1 only 1; A09, A10 and A11 own none. Total 88.

| Topic | File (under `scripts/`) | Function, as its own documentation states it | Source | Declared invocation |
|---|---|---|---|---|
| A01 | `check_tz.sh` | operator self-check that the shell's IST time is trustworthy | H | — |
| A01 | `ist_now.sh` | operator IST clock from the app's single time source | H | — |
| A02 | `revert_temp_config.py` | find TEMP markers in config YAML; revert them on confirmation | D | — |
| A03 | `backup_evidence.py` | back up the forward-evidence files | D | cron: 01:10 daily |
| A03 | `backup_restore_drill.py` | monthly drill: restore the latest backup to a temporary DB, verify | D | cron: 03:00 1st of month |
| A03 | `backup_retention.py` | by name only: retention of backup files | N | cron: 02:00 daily |
| A03 | `db_retention.py` | delete DB rows older than per-table retention windows | D | cron: 02:30 Mon-Sat; 02:30 Sunday |
| A03 | `output_retention.py` | by name only: retention of output files | N | cron: 02:10 daily |
| A03 | `wal_checkpoint.py` | passive WAL checkpoint on the trading DB | D | cron: 16:00 Mon-Fri |
| A04 | `auto_refresh_token.py` | headless Zerodha token refresh using TOTP | D | cron: 08:15 Mon-Fri |
| A04 | `copy_token_to_vm.bat` | atomic copy of the broker token to the VM | H | — |
| A04 | `zerodha_login.py` | browser-assisted Zerodha login; saves the session token | D | main.py import (L106, L1875) |
| A05 | `fetch_daily_candles.py` | after the close, fetch 1-minute candles for the daily report | D | cron: 15:40 Mon-Fri |
| A05 | `fetch_fno_ban.py` | fetch the NSE F&O ban list into the DB | D | cron: 08:35 Mon-Fri |
| A05 | `find_symbol_aliases.py` | find Zerodha matches for Chartink symbols that failed | D | — |
| A05 | `refresh_instruments.py` | build instruments.csv from NSE and Kite sources | D | cron: 09:00 Mon-Fri |
| A06 | `preflight_scanner_check.py` | operator check that the Chartink scanner URLs are reachable | D | — |
| A07 | `compute_strategy_metrics.py` | end-of-day strategy metrics; may set a strategy to PAPER_ONLY | D | cron: 16:15 Mon-Fri |
| A07 | `strategy_registry_officer.py` | daily upkeep of the strategy-direction registry | D | cron: 16:22 Mon-Fri |
| A07 | `strategy_status.py` | per-strategy 'will it trade today?' table | D | — |
| A08 | `sr_corp_action_spotcheck.py` | one-time check whether historical candles are split-adjusted | D | — |
| A08 | `sr_detector_backfill.py` | end-of-day backfill of trade outcomes into S&R results | D | cron: 15:58 Mon-Fri |
| A08 | `sr_level_export.py` | read-only export of detected S&R levels for manual comparison | D | — |
| A12 | `backfill_closure_source_w8.py` | one-shot backfill of trades.closure_source | D | — |
| A12 | `eod_broker_reconcile.py` | broker-authoritative end-of-day reconcile | D | cron: 15:58 Mon-Fri |
| A12 | `eod_cleanup.py` | end-of-day cleanup of stale signals, orders and state rows | D | cron: 15:50 Mon-Fri |
| A12 | `eod_verify.py` | end-of-day check of positions, orders and P&L | D | cron: 15:55 Mon-Fri |
| A12 | `reconcile_pnl.py` | compare broker and system P&L; alert on variance | D | — |
| A12 | `reconcile_positions.py` | compare broker and system open positions | D | cron: 15:45 Mon-Fri |
| A13 | `clear_kill_switch.py` | clear the kill switch in the DB without starting trading | D | — |
| A14 | `alert_watcher.py` | email the alert sentinel files written by alerts/critical.py | D | unit: alert-watcher |
| A15 | `agy_runner.py` | shared runner for the AI model CLI, with fallback and quota checks | D | — |
| A15 | `capture_metrics_baseline.py` | system health metrics every 5 minutes; daily summary | D | cron: every 5 min 09:00-15:55 Mon-Fri; 16:16 Mon-Fri |
| A15 | `check_vm_state.py` | read-only VM state diagnostics | D | — |
| A15 | `disk_monitor.py` | disk-space check with alerts and log clean-up | D | cron: hourly |
| A15 | `gemini_data_integrity_check.py` | compare stored candles with Zerodha's; AI review | D | cron: 17:00 Mon-Fri |
| A15 | `gemini_log_review.py` | after the close, AI review of the day's warning logs | D | cron: 16:20 Mon-Fri |
| A15 | `gemini_premarket_brief.py` | pre-market AI briefing sent to Telegram | D | cron: 08:55 Mon-Fri |
| A15 | `gemini_trade_coach.py` | AI grading of the day's closed trades | D | cron: 16:40 Mon-Fri |
| A15 | `gemini_watchman.py` | live AI log watchman and flow trace in market hours | D | unit: trading-watchman |
| A15 | `gemini_weekly_patterns.py` | weekly AI review for recurring patterns | D | cron: 18:00 Sunday |
| A15 | `generate_screened_stocks_csv.py` | daily CSV of traded and rejected symbols | D | cron: 16:01 Mon-Fri |
| A15 | `healthcheck_server.py` | HTTP health endpoint for external uptime monitoring | D | main.py import (L91) |
| A15 | `liveness_probe.py` | alarm if the trading service is down in market hours | D | cron: every 5 min 09:00-15:55 Mon-Fri |
| A15 | `monitoring_canary.py` | daily self-test of the alerting and monitoring paths | D | cron: 08:20 daily |
| A15 | `reconstruct_excursions.py` | after the close, per-trade MFE/MAE reconstruction | D | cron: 15:50 Mon-Fri |
| A15 | `system_manager.py` | daily cross-checks across the whole system | D | cron: 18:45 Mon-Fri |
| A15 | `trade_journal.py` | daily trade-journal entries from closed trades | D | cron: 16:10 Mon-Fri |
| A16 | `check_cron_drift.py` | heartbeat-miss and crontab drift check | D | cron: 18:00 Mon-Fri |
| A16 | `cron_officer.py` | cron-job briefing, end-of-day execution report and alerts | D | cron: 09:20 daily; 18:50 Mon-Fri |
| A16 | `cron_report_render.py` | rendering of the cron officer's reports | D | — |
| A16 | `cron_watchdog.py` | checks that the cron officer and drift check ran | D | unit: cron-watchdog |
| A16 | `generate_crontab.py` | generate the crontab from config/cron_registry.yaml | D | — |
| A17 | `approve_ssh_keys.py` | audited SSH-key re-baseline for the security monitor | D | — |
| A17 | `copy_gate.py` | policy engine for VM-to-PC file copying | D | — |
| A17 | `deploy_assert.py` | lightweight pre-deploy assertion | D | — |
| A17 | `deploy_preflight.py` | by name only: pre-deploy checks | N | — |
| A17 | `request_copy.py` | unlock VM-to-PC copying for 15 minutes, with an audit trail | D | — |
| A17 | `security_monitor.py` | alert-only VM security watcher | D | unit: security-watcher |
| A20 | `preflight/__init__.py` | package: daily multi-phase pre-market readiness check | D | — |
| A20 | `preflight/autofix.py` | whitelisted safe auto-fixes | D | — |
| A20 | `preflight/base.py` | the check contract shared by every check | D | — |
| A20 | `preflight/checks/__init__.py` | check groups, one module per group | D | — |
| A20 | `preflight/checks/broker.py` | group 4: broker connectivity | D | — |
| A20 | `preflight/checks/config_integrity.py` | group 6: configuration integrity | D | — |
| A20 | `preflight/checks/config_sanity.py` | configuration sanity auditor checks | D | — |
| A20 | `preflight/checks/database.py` | group 3: database and schema | D | — |
| A20 | `preflight/checks/engine.py` | group 8: engine readiness (phase B) | D | — |
| A20 | `preflight/checks/recovery.py` | group 9: logs and audit hygiene | D | — |
| A20 | `preflight/checks/security.py` | group 7: security (phase A) | D | — |
| A20 | `preflight/checks/services.py` | group 2: OS and support services | D | — |
| A20 | `preflight/checks/signals.py` | group 10: signal warm-up (phase C) | D | — |
| A20 | `preflight/checks/state.py` | group 5: state integrity | D | — |
| A20 | `preflight/checks/vm_health.py` | group 1: VM health | D | — |
| A20 | `preflight/deliver.py` | send the pre-flight report by email and Telegram | D | — |
| A20 | `preflight/orchestrator.py` | entry point: runs a phase's checks and safe fixes | D | cron: 08:30 Mon-Fri; 09:14 Mon-Fri; 09:15 Mon-Fri |
| A20 | `preflight/report.py` | result model and renderers | D | — |
| A20 | `preflight/sentinel.py` | the 'ready today?' status file | D | — |
| A20 | `preflight/startup_hook.py` | after a restart, run a missed phase on demand | D | main.py import (L4088) |
| A20 | `premarket_healthcheck.py` | deprecated predecessor of pre-flight phase A | D | — |
| A18 | `forward_shadow_record.py` | research recorder of scored signals and simulated outcomes | D | cron: 18:15 Mon-Fri |
| A18 | `v3_hardgate_parity_recompute.py` | offline V3 parity recompute over a DB backup | D | — |
| A18 | `v3_shadow_soak_report.py` | read-only V3 shadow-soak reports | D | — |
| A19 | `load_test_signals.py` | load test of the signal queue with synthetic webhooks | D | — |
| A19 | `replay_signals.py` | read-only replay of past signals through current logic | D | — |
| A19 | `t2_cnc_gtt_realtest.py` | real-API proof for CNC GTT, market hours only | D | — |
| A19 | `test_webhook.py` | standalone webhook test that bypasses the holiday guard | D | — |
| S1 only | `__init__.py` | package marker | N | — |

**Related documents:** 02, 04, 05, 06, 07, 08 and 10; the Source Inventory; the whole-system overview; the operational workflows; Deliverable 5 (`PHASE1_METHODOLOGY_APPLICATION_2026-11-04.md`); Decision Register, D-07, D-12, D-13, D-16, D-17, D-20 and D-21.
