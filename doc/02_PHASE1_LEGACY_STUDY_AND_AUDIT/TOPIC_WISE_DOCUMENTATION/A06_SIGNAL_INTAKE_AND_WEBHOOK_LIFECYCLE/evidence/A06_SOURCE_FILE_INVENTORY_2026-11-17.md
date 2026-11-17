# A06 evidence: the A06 source files at the study baseline

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17. Corrected the same day, before the STUDY was committed: section 5 named the three unchanged A06 files wrongly (found by the independent check of the STUDY; verified with `git diff 7d4970a 970aabf`).
**Purpose and scope:** Identifies the A06 paths of the Master System Investigation Index (entry A06; Appendix A for the one script) at the study baseline: size, Git object, SHA-256 and history of each path; the A06 call sites in `main.py`, which A01 owns as a file (index rule 8); the declared invocations of the script, as declarations only; the related paths that other topics own, which A06 reads at the boundary only (Rama's decisions A to E of 17-Nov-2026, on ChatGPT's review of the first fieldwork checkpoint); and the A06 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY's inventory and decides nothing.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone with `git show`, `git ls-tree`, `git log`, `git grep` and `git diff`. Nothing in the clone was written or run, and no endpoint, scanner URL, broker or API was contacted. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07); a line that carries an account identifier is cited by line only.

## 1. The files

The A06 paths are `signals/webhook_receiver.py`, `signals/signal_processor.py` and `signals/entry_throttle.py` (with the empty package file `signals/__init__.py`); the Chartink integration and configuration references (section 4); the relevant `main.py` wiring call sites (section 2); and the one script that Appendix A assigns to A06, `scripts/preflight_scanner_check.py`. FACT: all five files exist at the baseline, and the clone's working tree was clean and at the baseline. `signals/` holds no other file.

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `signals/webhook_receiver.py` | 1207 | 59565 | 100644 | `0f15a0ab033529d80d9c14c993a5077690b72871` | `bcbacba9df7d1e91c5123a7dde75ab7ea3f672752fe3a15a9490c141faf2f3fd` | 31 | 3b15bbf, 2026-09-09 |
| `signals/signal_processor.py` | 2703 | 139403 | 100644 | `7fab0a02a302770ac72bbbd662549d5c091086c1` | `2c22327bfe4c498e753c061158c1f3accdc807a9c33c5d7eb0dc20427b8c1696` | 64 | 056905b, 2026-09-11 |
| `signals/entry_throttle.py` | 125 | 5266 | 100644 | `b887a4be78a4dcfe3c2541d7528bd3b96ec351ea` | `86ea633a44f19dc2e3669a7a838e9c07b437aef8a1746b31d71f696ce7591ae6` | 1 | c0554c6, 2026-06-19 |
| `signals/__init__.py` | 0 | 0 | 100644 | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 1 | bcf03b5, 2026-04-17 |
| `scripts/preflight_scanner_check.py` | 235 | 9181 | 100644 | `3151263d6e247b04884e9fbe99f3cd0e44725167` | `b48ee785877ea7b7700bbf16a0ee8e9affed4d9087492fb89154db1738b6f5a2` | 2 | 53e61e2, 2026-04-26 |

## 2. The A06 call sites in `main.py`

FACT, at the baseline (line numbers of `main.py` at `970aabf`). The STUDY traces each one; this table only locates them. `main.py` is A01's file (index rule 8).

| Lines | What is there |
|---|---|
| L90, L92, L102 | imports of `SignalProcessor`, `WebhookReceiver` and `check_webhook_endpoint` |
| L222 to L224; L2427 to L2428 | the webhook secret required in every mode (C-2, 02-Jul-2026), checked at start; the variable is recorded by name only |
| L2450 to L2465 | `run_all_startup_checks(...)` with `scan_webhook_map`, `chartink_scanners` and `webhook_url=None` ("Flask not started yet"); the checks are in `utils/startup_checks.py` (A01) |
| L3402 to L3403 | the signal queue: `queue.Queue(maxsize=app_config.system.signal_queue.capacity)` |
| L3406 to L3413 | `WebhookReceiver(...)` built first, "so we can wire in_flight_release to signal_processor" |
| L3574 to L3622 | `SignalProcessor(...)`: the queue, `scan_webhook_map.scanners`, `in_flight_release_fn=webhook_receiver.release_in_flight`, `signal_expiry_sec=signal_queue.expiry_sec` ("Use same expiry as webhook_receiver"), and at L3622 `evidence=evidence_recorder` (added after `7d4970a`; section 5) |
| L3626 to L3700 | the allocator and the V3 chain, late-bound into the processor (`set_allocator`, `set_v3_chain`) |
| L3747 | `webhook_receiver.set_eod_capture(pb01_capture_worker)` (the capture worker is A18's; Rama's decision D) |
| L3765 to L3793; L3843 | the retest diverter and the gate-release callback, late-bound into the processor |
| L3870 to L3974 | the boot-order invariant; `signal_processor.start()` at L3974 |
| L3979 to L4000 | the `webhook` settings; the thread "webhook-server" running waitress `serve(webhook_receiver.app)`, started at L4000 |
| L4002 to L4041 | the post-start self-check of the local `/health` route |
| L1601 to L1719 | shutdown: `webhook_receiver.stop()` first (H-16), then `signal_processor.stop()`; the `webhook_audit` day count for effect telemetry (L1668 to L1670) |

`EntryThrottle` has no `main.py` call site: it is constructed inside `SignalProcessor` (`signals/signal_processor.py` L261 to L263) and called at L1410, L2225 and L2530 (Rama's decision B).

## 3. Declared invocations of the script

FACT: `scripts/preflight_scanner_check.py` is named in neither `deploy/cron/trading-system.cron` nor `config/cron_registry.yaml`; Appendix A gives it no schedule ("—"). It is an operator check. `config/chartink_scanners.yaml` L4 and `requirements.txt` L9 name it. A declaration would not be evidence that a job ran (Document 06, section 4.2; index rule 12).

## 4. Related paths that other topics own

These paths are read at the boundary only, for the A06 side of a flow; their owners investigate them (index rule 1; Rama's decisions A to E of 17-Nov-2026). Owners are as the index states.

| Path | Bytes | Owner (index) | Why A06 reads it |
|---|---|---|---|
| `config/scan_webhook_map.yaml`, `config/chartink_scanners.yaml`, `config/system_config.yaml` (`signal_queue`, `excluded_symbols`, `webhook`, `signal_processor`, `scanner_check_delay_sec`), `config/symbol_aliases.yaml`, `config/expected_managers.yaml` | 3067; 1795; 55901; 393; 22155 | A02 (`config/`) | the Chartink and scanner configuration, the receiver and processor settings, the alias file (A06 owns the consumer), the managers' declared effect points |
| `core/config_loader.py` | 127242 | A02 | the schemas of the scan map, the scanner list and the processor settings |
| `utils/startup_checks.py`; `core/account_registry.py`; `core/exceptions.py` | 68854; 17125; 18013 | A01 | the boot scanner and webhook checks (Rama's decision C); the primary account tag the receiver reads; the signal exception's docstring (records point) |
| `scripts/preflight/checks/signals.py` | 4170 | A20 | the pre-flight framework's signal and scanner checks (Rama's decision C) |
| `core/schema.sql`, `core/state_store.py` | — | A03 | the `signals`, `webhook_audit` and heartbeat storage (A03 owns the implementation) |
| `screening/`, `strategies/`, `capital/`, `allocation/`, `v3_chain/`, `orders/`, `sr_detector/` | — | A07, A09, A18, A10, A08 | the call-outs of `signal_processor.py` after the handoff, mapped at the interface only (Rama's decisions A and B) |
| `v3_chain/watchlist_capture.py` | 11490 | A18 | the PB-01 capture worker that receives end-of-day webhooks (Rama's decision D) |
| `alerts/` | — | A14 | the alerts the receiver and processor raise |
| `reports/signal_status.py`; `ops_dashboard/` (scanner attribution) | 7742; — | A15 | readers of the signal records, at the interface only |
| `scripts/test_webhook.py`, `scripts/load_test_signals.py`, `tests/` | 320; 11675; — | A19 | intent and behaviour evidence only, never proof of runtime behaviour (Rama's decision E) |
| `deploy/cron/trading-system.cron`, `config/cron_registry.yaml` | — | A16 | the schedule declarations (section 3) |
| legacy documents under `docs/` | — | evidence (HISTORICAL; index rule 11) | intent sources for the AUDIT |

## 5. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21); the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): two of the five A06 files changed after `7d4970a`; the other three, `signals/entry_throttle.py`, `signals/__init__.py` and `scripts/preflight_scanner_check.py`, are identical at both commits, as are the two Chartink configuration files `config/scan_webhook_map.yaml` and `config/chartink_scanners.yaml` (section 4).

| Path | Lines added / removed (`7d4970a` to the baseline) | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `signals/webhook_receiver.py` | 39 / 3 | `3b15bbf` (2026-09-09 12:47): "fix(signals): WR4b -- strip a leading account-tag prefix before the scan_name check" (a new function strips a leading primary-account tag from the normalised scan name before it is compared with the webhook path; its docstring carries account identifiers, cited by line only) |
| `signals/signal_processor.py` | 216 / 1 | `8d27fdb` (2026-09-10 19:07): "feat(evidence): CHECKPOINT -- wire P1, all five P2 reject paths, and P3"; `d646347` (20:48): "fix(evidence): CHECKPOINT -- every observer failure is counted, alerted once and PERSISTED"; `23d2be7` (20:58): "fix(evidence): CHECKPOINT -- `reanchored` is recorded from the re-anchor, not inferred"; `853a3a1` (20:59): "fix(evidence): CHECKPOINT -- the QUEUE_FULL reject is captured, and no-bypass is proven over every module"; `3fc1d2e` (21:00): "feat(evidence): CHECKPOINT -- every placement dispatch emits P1, including the two dormant resumes"; `056905b` (2026-09-11 01:45): "fix(evidence): CHECKPOINT -- P2 identity is REQUIRED, measured first; completeness is what APPLIES" |
| `main.py` (A06 call sites only) | 1 / 0 at an A06 call site | `8d27fdb` (2026-09-10 19:07) adds L3622, `evidence=evidence_recorder`, to the `SignalProcessor` construction; the other lines `main.py` gained after `7d4970a` are not A06 call sites |

`config/system_config.yaml` changed after `7d4970a` (commits `5f75c9b` and `5455ced`), but not in its `signal_queue`, `excluded_symbols`, `webhook`, `signal_processor` or `scanner_check_delay_sec` settings.

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether any of these changes was ever in force.
