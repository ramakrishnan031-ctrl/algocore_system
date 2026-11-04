# Broad Operational Workflows of the Legacy System

**Status:** APPROVED — Pre-Phase Deliverable 3, approved by Rama on 2026-11-04 at the Pre-Phase → Phase 1 gate (Decision Register, D-27)
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: first draft of Pre-Phase Deliverable 3, under ChatGPT's Pre-Phase instructions of 04-Nov-2026, section 7 (Decision Register, D-20 and D-22). Clarified, 2026-11-04: the declared restart policy (workflow 8) and the two 09:15 declarations (workflows 1 and 2), after ChatGPT's review of Deliverables 2 and 3. Approved, 2026-11-04: by Rama, with the other Pre-Phase deliverables, at the Pre-Phase → Phase 1 gate (Decision Register, D-27); status line only.
**Purpose and scope:** The broad Live operating lifecycle of the legacy system and its end-to-end workflows, at system level, from admitted evidence only: trading-system-prod-snapshot at the study baseline `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21). Each workflow is shown as trigger → major stages → component or system boundary → output or state → next handoff. Module internals are not traced, calculations are not audited, defects are not diagnosed, and no execution is inferred from a schedule. Paper mode is out of scope (Document 08, section 2). It builds on the whole-system overview (`WHOLE_SYSTEM_OVERVIEW_2026-11-04.md`).
**Evidence and labels:** Citations give the path at `970aabf` and line numbers (L). FACT is used for what the repository contains: files, section comments in `main.py`, unit settings, declared schedules. What a docstring, comment or legacy document says a component does is INTERPRETATION or HISTORICAL until Phase 1 checks it against the code (Document 06, section 4.1). A declared schedule or unit is not evidence that it ran (Document 08, section 10); whether any workflow below ran on production, and how, is UNKNOWN / NOT ESTABLISHED (Document 06, section 4.2). Times are IST.

## 1. The Live operating day as declared

| Time | Declared activity | Source | Label |
|---|---|---|---|
| 00:00 to 03:00; 05:00; hourly | Log clean-up; database, analytics and evidence backups (01:00, 01:05, 01:10); retention jobs (02:00 to 02:30); token clean-up (05:00); disk check (hourly) | `config/cron_registry.yaml` | FACT, declared only |
| 08:15 to 09:20 | Broker-token refresh (08:15); monitoring canary (08:20); pre-flight phases A, B and C (08:30, 09:14, 09:15); F&O ban list (08:35); Gemini pre-market brief (08:55); instrument refresh (09:00); cron-officer briefing (09:20) | `config/cron_registry.yaml` | FACT, declared only |
| Before market open | The engine starts as a service, or is restarted by the token watcher (workflow 1) | `deploy/systemd/`, `deploy/token_watcher.sh` | FACT for the files |
| 09:15 | Capital re-sync from the broker at market open | `main.py`, L973 (docstring) | INTERPRETATION |
| 09:00 to 15:55, every 5 minutes | Metrics capture and liveness probe | `config/cron_registry.yaml` | FACT, declared only |
| During the session | Webhook signals processed into trades; positions managed; periodic reconciliation (workflows 4, 5 and 7) | Section 2 | INTERPRETATION |
| 14:45 | End-of-day pre-alert | `main.py`, L931 (docstring) | INTERPRETATION |
| 15:15 | Force-close circuit-breaker callback | `main.py`, L688 (docstring) | INTERPRETATION |
| 15:17 | End-of-day square-off of intraday positions | `orders/eod_squareoff.py` (docstring) | INTERPRETATION |
| 15:25 | The broker's own square-off of remaining MIS positions, as the MIS auto-square-off docstring describes it | `orders/mis_autosquareoff.py` (docstring) | HISTORICAL |
| 15:40 to 18:50 | Daily candles (15:40); position reconciliation (15:45); end-of-day clean-up, verification and broker reconciliation (15:50, 15:55, 15:58); WAL checkpoint (16:00); screened-list file (16:01); daily trade review, trade journal and metrics (16:07 to 16:16); strategy-registry officer (16:22); Gemini reviews (16:20, 16:40, 17:00); Control Tower (17:05); cron-drift check (18:00); forward shadow record (18:15); system-manager and cron-officer end-of-day (18:45, 18:50) | `config/cron_registry.yaml` | FACT, declared only |
| After the service window | The engine exits cleanly once the book is flat | `main.py`, L1329 (docstring) | INTERPRETATION |
| 19:30 | Cron watchdog | `deploy/systemd/cron-watchdog.timer` | FACT, declared only |
| Sunday 18:00; 1st of the month 03:00 | Gemini weekly patterns; backup restore drill | `config/cron_registry.yaml` | FACT, declared only |

## 2. Workflows

### 2.1 Workflow 1 — Startup and readiness

- **Trigger.** FACT: `deploy/systemd/trading-system.service` runs `main.py --mode live` with `Restart=on-failure` and `RestartSec=10` (L33 to L34) and `WantedBy=multi-user.target` (L49). FACT: `deploy/systemd/token-watcher.service` is described as "auto-start on fresh token" (L2), with `Restart=always` (L14). INTERPRETATION, from its header comments: `deploy/token_watcher.sh` is a poll loop that decides whether to (re)start the engine from its state, its last exit code and the exit date, with an exit-code contract: 0 for a clean end of day or holiday, 3 for a start-up check failure, 4 for a halt by the kill switch.
- **Major stages.** FACT, from the section comments of `main.py`: `main` (L2085) runs the body once the single-instance lock is held (`_main_locked`, L2193) → Phase 0b, configuration load (L2196) → Phase 0c, state store, event bus, kill switch and time authority (L2218) → Phase 0d, start-up checks (L2316) → account selection and token handling (L2524) → configuration snapshot (L2593) → Phase 0e, construct the subsystems (L2616), including Live capital from broker margins (L2754) → event-bus subscriptions (L3846) → Phase 0f, start-up reconciliation (L3868) → Phase 0g, start the subsystems (L3920) → Phase 0h, mark start-up complete (L4166) → the runtime loop (L4248).
- **Boundary.** The engine process; the broker (token, margins, positions); the state store; the configuration files and the environment file (whose production contents are UNKNOWN); Telegram and e-mail for failures.
- **Output or state.** A running engine whose webhook receiver and live feed are started, with its session and start-up events recorded (INTERPRETATION).
- **Next handoff.** Workflows 2, 3 and 4.
- **Alternate paths visible at system level.** FACT, the command-line options (`main.py`, from L179): `--status` (prints status and exits; L2298), `--dry-run` (start-up checks only), `--resume` (clears a hard or soft kill so that start-up can proceed from a halt). INTERPRETATION: on a holiday or weekend the engine sends a Telegram notice and shuts down (`main.py`, L264, docstring). The declared pre-market jobs prepare the day: the broker-token refresh at 08:15 (TOTP-based, per the `pyotp` entry in `requirements.txt`) and the three pre-flight phases (phase C and the engine's capital re-sync are separate 09:15 declarations; workflow 2).

### 2.2 Workflow 2 — Market session lifecycle and scheduled activity

- **Trigger.** The clock: the time authority (`core/time_authority.py`), the market windows (`core/market_windows.py`), the holiday and special-session calendars (`main.py`, L441 and L446; `utils/holiday_guard.py`), and the cron schedule. FACT for the files; their behaviour is for Phase 1.
- **Major stages.** Pre-market jobs → engine start (workflow 1) → market open and capital re-sync (09:15) → the trading session, with metrics and liveness every five minutes → the end-of-day pre-alert (14:45) → the close sequence (15:15 to 15:25; workflow 7) → post-market jobs (15:40 to 18:50) → the engine's self-exit once flat → nightly maintenance (section 1). The 09:15 capital re-sync (`main.py`, L973, docstring) and pre-flight phase C at 09:15 (`config/cron_registry.yaml`) are separate declarations; their actual ordering and interaction are UNKNOWN / NOT ESTABLISHED.
- **Boundary.** The engine, the cron scripts, the broker and the databases.
- **Output or state.** Session and end-of-day records; reports; backups (INTERPRETATION).
- **Next handoff.** Workflows 6 and 7; the next day's workflow 1.

### 2.3 Workflow 3 — Data acquisition and storage

- **Trigger.** Engine start (the live feed) and the declared jobs.
- **Major stages.** INTERPRETATION, from docstrings and job names: the instrument list is refreshed at 09:00 → live ticks arrive through the KiteTicker WebSocket (`data/live_feed.py`) → minute OHLC candles are built (`data/candle_store.py`) → the S&R detector fetches historical candles through a read-only Kite handle (`main.py`, L393 and L421) → the F&O ban list is fetched at 08:35 and daily candles at 15:40 → metrics are captured every five minutes.
- **Boundary.** Zerodha Kite (REST and WebSocket), the NSE archives, the SQLite databases (`data_store/trading_system.db`; `analytics.db` with its candles and system-metrics tables) and files under `data_store/` and `logs/` (whole-system overview, section 5).
- **Output or state.** Instruments, candles, metrics and the ban list in the databases and files (INTERPRETATION).
- **Next handoff.** Workflow 4 (screening and price derivation) and workflow 5 (position management and exits); workflow 6 (metrics and reports).

### 2.4 Workflow 4 — From signal to trade decision

- **Trigger.** FACT: a Chartink scanner posts to the route `/webhook/<scanner_name>` (`signals/webhook_receiver.py`, L406).
- **Major stages.** INTERPRETATION, from the docstrings: the webhook receiver validates the payload, removes duplicates, enforces back-pressure and expiry, and queues the signal (`signals/webhook_receiver.py`, docstring). A worker pool takes each signal through "pre-flight -> strategy lookup -> secondary screen -> price derivation -> position sizing -> risk approval -> capital reserve -> order placement -> status update" (`signals/signal_processor.py`, docstring), drawing on `screening/` (hard gates, quality score, entry gate), `strategies/` (strategy control), `capital/` (risk engine, position sizer, fund-manager reservation) and the entry throttle. The kill switch is the "last-mile gate" (`capital/kill_switch.py`, docstring).
- **Boundary.** Chartink → the engine's HTTP endpoint (Flask, served by waitress) → the engine's internal pipeline → the state store (for example the `signals`, `webhook_audit` and `screener_results` tables).
- **Output or state.** Either an approved trade with capital reserved, handed to workflow 5, or a signal that ends with a recorded status (`reports/signal_status.py` classifies the statuses).
- **Alternate paths.** The V3 engines (regime, allocator, decision chain) and the S&R retest monitor appear beside this path; the README calls the V3 engines shadow and default-off (`README.md`, L74). Whether any was on in Live is UNKNOWN.

### 2.5 Workflow 5 — Order and position lifecycle

- **Trigger.** INTERPRETATION: `signal_processor` calls the order placer's single public method (`orders/order_placer.py`, docstring, OP1).
- **Major stages.** INTERPRETATION, from the docstrings and the README: the trade row is created → the entry orders are placed (order protocols for CO and limit orders; the Zerodha adapter and its rate limiter) → fills are monitored (`broker/order_monitor.py`, `broker/order_state_machine.py`) → the capital reservation is committed on a fill or released on failure (`orders/order_placer.py`, docstring) → stop-loss and target legs protect the position (`README.md`, L30 to L57) → the position is managed (target, breakeven, structure-exit, stop-loss-breach and target-retry managers in `orders/`) → it is exited, and the capital is released (`README.md`, L49).
- **Boundary.** The engine ↔ Zerodha (orders, fills, positions; OCO-GTT orders for CNC positions held overnight, `orders/cnc_gtt.py`) and the state store (for example `trades`, `orders` and `fm_ledger`).
- **Output or state.** A closed intraday position, or a CNC position carried overnight under GTT protection (INTERPRETATION).
- **Next handoff.** Workflow 7 (reconciliation and end of day); workflow 6 (alerts and reports).

### 2.6 Workflow 6 — Monitoring, alerts and reporting

- **Trigger.** Events in the engine (failures, fills, kill-switch changes) and the declared schedule.
- **Major stages.** FACT for the components; their behaviour is INTERPRETATION: alerts by the Telegram Bot API and SMTP e-mail (`alerts/telegram_notifier.py`, L50 and L834), where "a CRITICAL always has a fallback path" (`README.md`, L56); the alert-watcher service (sentinel monitor); the 14:45 pre-alert; the monitoring canary (08:20) and liveness probe (every five minutes); UptimeRobot on the `/health` route (`signals/webhook_receiver.py`, L364; `deploy/setup_uptimerobot.md`, L3); the Control Tower (17:05); the cron officer (09:20 and 18:50), the cron-drift check (18:00) and the cron watchdog (19:30); the daily trade review, trade journal and metrics (16:07 to 16:16; the daily report job is disabled); the Gemini jobs and the live Gemini watchman; the read-only operations dashboard; the security watcher.
- **Boundary.** The engine and scripts → Telegram, e-mail, the Gemini command-line tool, UptimeRobot, and the dashboard reached through Tailscale.
- **Output or state.** Messages, spreadsheet reports, records in the state store (for example `telegram_alerts` and the `control_tower_*` tables), log and JSON files (INTERPRETATION).
- **Next handoff.** The human operator, Rama: for example a resume after a halt (workflow 8).

### 2.7 Workflow 7 — Reconciliation and end of session, square-off

- **Trigger.** Periodic and event-driven reconciliation during the session; the close-time triggers; the post-market jobs.
- **Major stages.** INTERPRETATION, from the docstrings: "Hybrid periodic + event-driven reconciliation of local trade state vs the live broker state" (`orders/order_reconciler.py`, docstring) → at 15:15 the force-close circuit-breaker callback (`main.py`, L688), which the MIS auto-square-off docstring describes as "a SOFT_KILL that closes nothing" → at 15:17 the end-of-day square-off cancels pending intraday entries and exits intraday positions with MARKET orders (`orders/eod_squareoff.py`, docstring) → the MIS auto-square-off orchestrator runs alongside it (`orders/mis_autosquareoff.py`; `core/mis_squareoff_timing.py`) → by that docstring's account the broker squares off any remaining MIS position at 15:25 → post-market jobs reconcile positions (15:45), clean up (15:50), verify (15:55), reconcile with the broker (15:58) and checkpoint the database (16:00) → CNC positions stay open overnight under GTT protection and are monitored (`orders/cnc_gtt_monitor.py`) → the next start-up reconciles again (workflow 1, Phase 0f).
- **Boundary.** The engine and scripts ↔ Zerodha; the state store (for example `reconciliation_log`, `position_reconciliation`, `eod_squareoff_log`, `eod_verification` and `eod_broker_reconciliation`).
- **Output or state.** A flat intraday book, reconciled records and end-of-day summaries (INTERPRETATION).
- **Next handoff.** Workflow 6 (reports) and workflow 8 when a mismatch or failure needs action.

### 2.8 Workflow 8 — Failure, restart and recovery

- **Halt controls.** INTERPRETATION, from the docstring: the kill switch has three modes — INACTIVE, SOFT_KILL (blocks new entries, allows exits) and HARD_KILL (blocks all orders and attempts broker cancellation) — and its state is persisted in the `kill_switch_state` table "for restart recovery" (`capital/kill_switch.py`, KS1 and KS2). FACT: `main.py` builds callbacks for a critical failure (L657), three consecutive API failures (L727), the daily loss limit (L756), orphans (L820) and the 15:15 force close (L688).
- **Restart.** FACT: the `trading-system.service` unit declares `Restart=on-failure` and `RestartSec=10` (L33 to L34). Whether systemd actually restarted the production engine is UNKNOWN / NOT ESTABLISHED. INTERPRETATION: the token watcher restarts it, or holds it, by exit code and date, and a halt from the same day needs a manual resume (`deploy/token_watcher.sh`, header). The single-instance lock (`utils/instance_lock.py`) prevents two engines; start-up scenario detection and start-up reconciliation (workflow 1, Phases 0c, 0d and 0f) restore the picture after a restart.
- **Manual recovery.** INTERPRETATION, from the header comments: `deploy/resume.sh` stops the service, clears the kill switch in the database and restarts the service under systemd; `scripts/clear_kill_switch.py` and `main.py --resume` also exist (FACT).
- **Broker session.** INTERPRETATION: the token monitor, authentication recovery and token invalidation on an authentication failure (`broker/token_monitor.py`, `broker/auth_recovery.py`; `main.py`, L138 and L168).
- **Data protection.** FACT, declared only: the nightly backups and the monthly restore drill.
- **Next handoff.** Workflow 1 on restart; workflow 6 for the alerts.

## 3. Handoffs between workflows

| From | To | What passes |
|---|---|---|
| 1 Startup | 3 Data, 4 Signal | A running engine with its feed and webhook receiver; reconciled state |
| 3 Data | 4 Signal, 5 Order | Instruments, live prices and candles |
| 4 Signal | 5 Order | An approved trade with capital reserved |
| 5 Order | 7 Reconciliation, 6 Monitoring | Orders, fills, open positions, events |
| 7 Reconciliation | 6 Monitoring, 8 Recovery, next day's 1 | Reconciled records, end-of-day summaries, mismatches, carried CNC positions |
| 6 Monitoring | Rama | Alerts, reports, dashboard views |
| 8 Recovery | 1 Startup | A restart or a resume after a halt |

All handoffs are INTERPRETATION from structure and documentation; Phase 1 establishes each one in the code.

## 4. Unknowns and limits

- No workflow is shown to have run on production: there is no runtime evidence (Document 06, section 4.2). The schedule, units and time triggers are declarations.
- The order of stages comes from section comments, docstrings and the README; the exact paths, branches and values in force are for Phase 1.
- The times 15:15, 15:17 and 15:25 and the exit-code contract come from documentation inside the code; the configuration values in force on production are UNKNOWN.
- The five existing technical records describe the testing copy and are not used here as evidence of production behaviour (D-21).

## 5. Use in the next deliverables

These workflows, with the component map of the whole-system overview, are inputs to the evidence ChatGPT uses to propose the Master System Investigation Index (D-13, D-16) and to Deliverable 5, the preparation for applying Document 08. No topic list is proposed here.

**Related documents:** 02, 04, 06, 07, 08 and 10; the Source Inventory; the whole-system overview; Decision Register, D-12, D-20, D-21 and D-22.
