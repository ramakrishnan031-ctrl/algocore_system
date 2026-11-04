# Whole-System Overview of the Legacy System

**Status:** DRAFT — Pre-Phase working record, for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: first draft of Pre-Phase Deliverable 2, under ChatGPT's Pre-Phase instructions of 04-Nov-2026, section 6 (Decision Register, D-20 and D-22). Corrected, 2026-11-04: the two wording corrections of ChatGPT's review (sections 3 and 6). Corrected again, 2026-11-04: the sentence on secrets in section 5, after ChatGPT's review of Deliverables 2 and 3.
**Purpose and scope:** A concise, high-level description of the Live legacy system, from admitted evidence only: trading-system-prod-snapshot at the study baseline `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21), read in a local read-only clone. It is an overview, not a module manual, code walkthrough, audit or defect hunt. It reads structure — folders, file lists, module docstrings, imports, declared routes, service units, schedules and the database schema — and does not follow module logic. Paper mode is out of scope (Document 08, section 2); it appears only where the shared code makes it visible.
**Evidence and labels:** Citations give the path at `970aabf` and, where useful, line numbers (L). Labels follow Document 04, section 6. What a module docstring or a legacy document says a component does is documentation: it is recorded as INTERPRETATION or HISTORICAL until Phase 1 checks it against the code (Document 06, section 4.1). Nothing here is runtime evidence: whether a service was installed, a job ran or a value was in force is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2; Document 08, section 10). Sources are listed in the Source Inventory (SRC-nn).

## 1. Purpose and scope of the legacy system

- HISTORICAL: the legacy README describes "An automated **NSE intraday** trading system. It receives scanner alerts by webhook, screens and scores them, sizes the position against real capital, places the order with the broker, and manages the exit — unattended, on a VM, every trading day", live since 11-May-2026 (`README.md`, L3 to L9; SRC-36).
- FACT: the entry point `main.py` accepts `--mode paper|live`, with paper as the default (`main.py`, L184 to L186); the production service unit starts it with `--mode live` (`deploy/systemd/trading-system.service`). Only Live behaviour is in scope.
- FACT: one broker is used through the `kiteconnect` 5.1.0 SDK (Zerodha; `requirements.txt`, `broker/zerodha_adapter.py`). `broker/angelone_adapter.py` describes itself as a stub fallback whose methods raise `NotImplementedError` (its docstring, L4 to L13).
- INTERPRETATION: besides intraday (MIS) positions, the code handles delivery (CNC) positions carried overnight: `orders/cnc_gtt.py` describes "CNC overnight protection via OCO-GTT", and `orders/mis_autosquareoff.py` an MIS auto-square-off orchestrator (their docstrings, L2). The existing record `01_SYSTEM_OVERVIEW.md` also describes an intraday book and a delivery book (HISTORICAL; SRC-40). Phase 1 establishes the scope of each.

## 2. Architectural boundaries and principal components

FACT: one orchestration process, `main.py` (4,294 lines), whose docstring reads "Single orchestration script. Wires all subsystems, runs startup phases, manages the runtime loop, and performs clean shutdown" (L1 to L5). It imports `signals/`, `screening/`, `capital/`, `orders/`, `broker/`, `data/`, `core/`, `strategies/`, `alerts/`, `utils/` and `scripts/`, and the four V3 packages inside functions; it does not import `reports/`, `ops/` or `ops_dashboard/`. It holds the webhook receiver (imported at L92) and the live-feed manager (L70), runs time-triggered threads (L931, L973, L1329), and shuts down in reverse order, stopping the webhook receiver first (L1599; L1681 to L1688). Around it sit scheduled scripts, monitoring services and a read-only dashboard (sections 3 and 6).

The packages, with their size at `970aabf` (Python modules and lines) and their role as their docstrings and the README layout table (`README.md`, L62 to L77) describe it (INTERPRETATION until Phase 1):

| Component | Path, size | Role as described |
|---|---|---|
| Signal intake | `signals/` — 4 modules, 4,035 lines | Webhook receiver, signal processor and queue, entry-rate throttle. FACT: Flask routes `/health` and `/webhook/<scanner_name>` (`signals/webhook_receiver.py`, L364 and L406). |
| Screening | `screening/` — 7, 2,734 | Secondary screener, hard gates, quality scorer, entry gate, retest monitor, step executor. |
| Capital and risk | `capital/` — 10, 7,547 | Fund manager, kill switch, position sizer, risk engine, capital invariant, drift handler, strategy governor, performance allocator, shadow engine. |
| Orders and exits | `orders/` — 21, 19,964 | Order placer, manager and reconciler; CO and limit order protocols; exits (EOD square-off, MIS auto-square-off, stop-loss breach monitor, target, breakeven and structure-exit managers); CNC GTT protection and its monitor; slippage recording; shadow tracking. |
| Broker interface | `broker/` — 13, 5,743 | Zerodha adapter, order monitor and state machine, rate limiter, token monitor and authentication recovery, product resolver, cost calculator, clock-skew probe; the Angel One stub. |
| Market data | `data/` — 3, 1,158 | "KiteTicker WebSocket manager" (`data/live_feed.py`) and "Minute OHLC candle builder" (`data/candle_store.py`). |
| Core services | `core/` — 26, 13,050 | State store (SQLite), configuration loading, validation, auditing and snapshots, events, time authority, market windows, schema migrations, logging, instrument cache, account registry, cron registry, evidence contract. |
| Strategies | `strategies/` — 5, 749 | Strategy YAML schema, loader and control resolver. |
| Alerts | `alerts/` — 6, 1,787 | Telegram and e-mail notifier, critical alerts, alert delivery contract, cron alerts, MIS square-off notifier. |
| Reports | `reports/` — 5, 5,144 | Daily report, daily trade review (spreadsheet output), signal-status classification. |
| Operations monitoring | `ops/` — 14, 1,335; `ops_dashboard/` — 183 files, 93 of them Python | The "Control Tower" (`ops/__init__.py`, L1) and a web dashboard whose unit describes it as a "read-only trading GUI, loopback:8500 behind Tailscale" (`ops_dashboard/deployment/gui-dashboard.service`). |
| V3 engines | `regime/` — 4, 655; `sr_detector/` — 12, 1,931; `v3_chain/` — 9, 1,902; `allocation/` — 5, 525 | Market regime, support and resistance (S&R) detection, a decision-chain enrichment and a portfolio allocator. HISTORICAL: the README calls them "shadow/default-OFF" (`README.md`, L74). Whether any ran in Live is UNKNOWN. |
| Utilities | `utils/` — 5, 2,290 | Start-up checks, single-instance lock, holiday guard, cron heartbeat. |
| Scheduled and operator scripts | `scripts/` — 88 files, 85 Python | The jobs of the cron schedule (section 6) and operator tools. |
| Deployment | `deploy/` — 29 files | Service units, the cron file, Git hooks, log rotation, VM security settings, PC-side login helpers. |
| Configuration | `config/` — 51 files | 31 YAML and 20 CSV files, loaded by `core/config_loader.py`. |
| Tests | `tests/` — 442 files, 404 Python | HISTORICAL: "~4,800 tests" (`README.md`, L77). A test is not evidence that it ran or passed. |
| Documentation | `docs/` — 474 files, and the root `.md` files | The legacy project's own documentation (SRC-19, SRC-36 to SRC-39). |

## 3. External systems and data sources

| External system | Role | Evidence | Label |
|---|---|---|---|
| Zerodha Kite Connect: REST API, KiteTicker WebSocket and login | Orders, positions and margins; live market data; read-only historical candles | `kiteconnect` imported in `broker/`, `data/`, `main.py` and `scripts/`; `main.py`, L381 (Kite client) and L393 (read-only historical-data handle); `data/live_feed.py`, docstring | FACT for the use of the SDK; the roles are INTERPRETATION |
| Chartink | Scanner alerts posted to the webhook | `signals/webhook_receiver.py` (22 mentions; the route at L406); referenced in `config/`, `ops_dashboard/` and `scripts/` | FACT for the references; INTERPRETATION for the flow |
| NSE archives (`nsearchives.nseindia.com`) | Reference-data downloads; for example the F&O ban-list job (section 6) | Referenced in `config/`, `core/` and `scripts/` | INTERPRETATION |
| Telegram Bot API | Alerts | `alerts/telegram_notifier.py`, L50 | FACT |
| E-mail (SMTP) | Alerts and digests | `alerts/telegram_notifier.py`, L36 and L834; mailbox settings under `alerts:` in `config/system_config.yaml` | FACT |
| Google Gemini, through the Gemini command-line tool | AI pre-market brief, log review, trade coach, data-integrity check, weekly patterns, and a live log "watchman" | `scripts/gemini_*.py` (six scripts); `scripts/gemini_log_review.py`, L5: "using Gemini CLI (Google auth, no API key)"; `deploy/systemd/trading-watchman.service` | FACT for the scripts and unit; their outputs UNKNOWN |
| Tailscale | Private network access to the dashboard | `ops_dashboard/deployment/gui-dashboard.service` | FACT for the unit text |
| UptimeRobot | External uptime check of the `/health` endpoint | `deploy/setup_uptimerobot.md`, L3 | HISTORICAL |
| Public-IP check services (`api.ipify.org`, `checkip.amazonaws.com`, `ip-api.com`) | Checks of the machine's public address | Referenced in `broker/` and `scripts/` | INTERPRETATION |
| Git, from the development PC to the VM | The deployment route | `DEPLOYMENT.md`, L222 ("`git push vm main`"); `deploy/hooks/` (`pre-receive`, `post-receive`, `market_hours_guard.sh`) | HISTORICAL for the route; FACT for the hook files |

FACT: the engine's service unit names an environment file, `.env` (`deploy/systemd/trading-system.service`, L13), the scripts load it with `python-dotenv` (for example `scripts/auto_refresh_token.py`, L52 to L53), and the repository contains only the template `.env.example`. Whether a production `.env` file existed at shutdown, and what values it contained, is UNKNOWN / NOT ESTABLISHED. No values are reproduced (Document 08, section 11).

## 4. Broad data movement and control relationships

- HISTORICAL: the README's diagram of how a trade happens (`README.md`, L30 to L57): Chartink scanner → webhook → `signals/` (receive, authenticate, queue) → `screening/` (secondary screener, hard gates, score) → `capital/` (risk gates, position sizing, reserve) → `orders/` (entry, then stop-loss and target legs) → `broker/` (Zerodha adapter, rate limits, fill monitor) → `capital/` (commit the reserve to used capital, release it on exit). Cross-cutting: `capital/kill_switch.py` (soft and hard kill), `core/state_store.py` (SQLite, "the single source of DB truth"), `core/config_loader.py` and `alerts/`.
- FACT: the package structure matches that chain: each named package exists, and `main.py` imports each of them (section 2).
- INTERPRETATION: market data enters through KiteTicker into `data/` (minute candles), and historical candles feed the S&R detector; broker state comes back through the order monitor and the reconcilers in `orders/`; the state store is the shared record between the engine, the scheduled scripts, the reports and the dashboard. Phase 1 establishes the actual paths.
- FACT: `main.py` defines time-triggered functions whose docstrings give, in IST: a market-open capital re-sync from the broker at 09:15 (L973), an end-of-day pre-alert at 14:45 (L931), a force-close circuit breaker at 15:15 (L688), and a clean self-exit once the service window has ended and the book is flat (L1329). What they did at run time is UNKNOWN.

## 5. Storage and persistence

- FACT: the main database is SQLite at `data_store/trading_system.db`, opened in WAL mode (`core/state_store.py`, L13 and L108). Its schema, `core/schema.sql`, defines 45 tables: signals, trades, orders, capital snapshots and the fund-manager ledger, session and kill-switch state, webhook audit, end-of-day square-off and verification logs, reconciliation logs, alert records, the trade journal, strategy metrics, shadow trades, cron heartbeats, pre-flight runs, GTT and S&R state, Control Tower records, configuration snapshots and others.
- FACT: a separate analytics database, `analytics.db` (`core/db_connect.py`), with three tables in `core/analytics_schema.sql`: candles, system metrics and daily system metrics.
- FACT: files under `data_store/` (for example JSONL shadow logs, `config/system_config.yaml`, L571 and L617; an alert sentinel folder and lock files, L381 to L384) and under `logs/` (for example L380; log rotation in `deploy/logrotate/trading-system`).
- FACT: configuration in `config/` (31 YAML, 20 CSV), loaded by `core/config_loader.py`. HISTORICAL: the legacy README states that secrets were kept in `.env` and not committed (`README.md`, L99 to L100). Whether a production `.env` file existed at shutdown, and what values it contained, is UNKNOWN / NOT ESTABLISHED (section 3).
- FACT (declared only): database, analytics and evidence backups at 01:00, 01:05 and 01:10, retention jobs between 02:00 and 02:30, and a monthly restore drill (`config/cron_registry.yaml`).
- UNKNOWN / NOT ESTABLISHED: database contents, sizes and state at shutdown.

## 6. Execution environments and scheduling boundaries

- Deployment environment, as Document 06, section 1 records it: an Oracle Ubuntu VM. FACT: at the study baseline, the repository defines these systemd unit files: `trading-system.service` (the engine, `main.py --mode live`), `alert-watcher.service` (sentinel monitor), `token-watcher.service` (on a fresh broker token), `security-watcher.service` (log and file-integrity monitor), `trading-watchman.service` (the Gemini log watchman), `cron-watchdog.service` with its timer at 19:30, and the dashboard's `gui-dashboard.service`. Whether these units were installed or running on the production VM is UNKNOWN / NOT ESTABLISHED. FACT: the repository also keeps VM security settings in `deploy/security/`.
- FACT (declared only): `config/cron_registry.yaml` lists 47 jobs, 46 enabled (`daily_report` disabled); `deploy/cron/trading-system.cron` has 46 active entries. Their declared time bands (IST): nightly maintenance from 00:00 to 03:00 and a token clean-up at 05:00; an hourly disk check; pre-market from 08:15 to 09:20 (token refresh, three pre-flight phases, F&O ban list, Gemini brief, instrument refresh, briefing); during the market every five minutes from 09:00 to 15:55 (metrics capture, liveness probe); post-market from 15:40 to 18:50 (daily candles, position reconciliation, end-of-day clean-up, verification and broker reconciliation, reports, metrics, Gemini reviews, Control Tower, cron officer); weekly on Sunday at 18:00; monthly at 03:00 on the first day.
- Development PC (Windows; Document 06, section 1). FACT: PC-side helper files `deploy/zerodha_morning.bat` and `deploy/zerodha_morning.ps1` (INTERPRETATION: the morning broker login). HISTORICAL: changes were deployed by a Git push from the PC to the VM (`DEPLOYMENT.md`, L222), guarded by server-side hooks (`deploy/hooks/`).
- UNKNOWN / NOT ESTABLISHED: which units were installed and running on production, the real crontab, and whether any job ran (Document 08, section 10). The machine-side facts in the five existing technical records come from the testing VM and do not describe production (SRC-40 to SRC-44; D-21).

## 7. High-level dependencies and handoffs

- FACT: the runtime dependencies (`requirements.txt`): `pyyaml` 6.0.3, `pydantic` 2.13.0, `kiteconnect` 5.1.0, `requests` 2.33.1, `flask` 3.1.3, `cachetools` 7.1.1, `waitress` 3.0.2, `openpyxl` 3.1.5, `python-dotenv` 1.2.2 and `pyotp` 2.9.0; for development, `pytest` and `pytest-cov` (`requirements-dev.txt`). The standard library's `sqlite3` and `smtplib` carry storage and e-mail.
- OPEN QUESTION: `scripts/` also imports `psutil` and `ntplib`, which neither requirements file lists; how they were installed on the VM is UNKNOWN. For Phase 1.
- INTERPRETATION, the main handoffs: webhook → signal queue → screening → capital reservation → order placement → broker → order monitoring and reconciliation → exits and end-of-day square-off → capital release; the state store as the shared record; alerts to Telegram and e-mail; post-market reports, metrics and AI reviews; the daily broker-token cycle (a TOTP-based refresh job at 08:15, the token watcher and the PC-side helpers). Phase 1 establishes each handoff.

## 8. Repository evidence and historical documents

- Repository evidence at `970aabf` (code, configuration, units, schedules and schema) shows what the code implements and what was declared (Document 06, section 4.1, priority 1).
- The legacy project's documents — `README.md`, `DEPLOYMENT.md`, `PATHS.md`, `UNPUSHED_LEDGER.md`, `docs/`, `AGENTS.md` and `GEMINI.md` — are HISTORICAL records of intent and practice (priority 4), compared with the code, never taken in its place.
- The five existing technical records (SRC-40 to SRC-44) were written from the testing copy (`e7bf477`), not from production; production is the reference (D-21). Phase 1 checks them against `970aabf`.
- Code changed after the last recorded deployment (33 commits after `686df1c`, 02-Sep to 11-Sep-2026; Source Inventory, section 1); Phase 1 notes those changes topic by topic (D-21).

## 9. Important unknowns

UNKNOWN / NOT ESTABLISHED, because no runtime evidence survives (Document 06, section 4.2): the commit production was running when it stopped; which services and cron jobs were installed and ran; the configuration values and secrets in force on the VM; the database contents and logs; the broker-side state; whether the V3 and shadow features were switched on in Live; and the outputs of the Gemini jobs. Rama's Telegram and e-mail alerts are routine and have not been supplied as evidence (SRC-51).

## 10. Use in the next deliverables

The component map (section 2), the external systems (section 3), the storage (section 5) and the schedule bands (section 6) are inputs to Deliverable 3, the broad operational workflows, and to the evidence ChatGPT uses to propose the Master System Investigation Index (D-13, D-16). This overview proposes no topic list.

**Related documents:** 02, 04, 06, 07, 08 and 10; the Source Inventory; Decision Register, D-12, D-20, D-21 and D-22.
