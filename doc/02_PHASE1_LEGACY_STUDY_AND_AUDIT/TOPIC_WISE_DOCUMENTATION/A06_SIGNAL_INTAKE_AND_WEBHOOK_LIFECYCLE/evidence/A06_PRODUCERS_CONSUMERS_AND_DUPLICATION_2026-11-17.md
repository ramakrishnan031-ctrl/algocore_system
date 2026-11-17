# A06 evidence: producers, consumers, storage handoffs and duplication

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P11, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude.
**Purpose and scope:** every A06 artefact (the HTTP request, the internal signal object, the queue item, the `signals` rows, the `webhook_audit` rows, the EOD-webhook heartbeat, counters/metrics, alerts) as a producer-to-consumer map; the A03 storage handoffs for `signals`, `webhook_audit` and the EOD-webhook heartbeat store; places that do the same intake job separately (duplication record). Direction questions 20 (storage side), 23 and 27 (duplication and consistency, record only). Readers and writers owned by other topics are recorded at the interface only (call site, what crosses, owner) (STUDY part P11).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)

In whole (every printed line passed through the identifier filter of the security rule (D-07)):
- `signals/webhook_receiver.py` (1,207 lines; structure by Python `ast.parse` of the source text, which executes
  nothing). At L954 the filter masked the hash function's name; a count-only match (`grep -c`) confirmed the call is
  `hashlib.sha256(fp_raw...)`, as the docstring WR7 (L18) says; no other text was masked in that file's output.
- `reports/signal_status.py` (156 lines; A15's file, read as a consumer of the `signals.status` vocabulary).

In part (line ranges):
- `signals/signal_processor.py` L1 to L300 (header, constructor), L300 to L740 (lifecycle, dispatcher, safe wrapper,
  alert, evidence, heartbeat and metric helpers), L867 to L1065 (intake up to the handoff), L1190 to L1276 (reject,
  error and `finally` handlers), L1340 to L1385 (reservation write and alert call), L1484 to L1530 (FIX-069 re-queue),
  L2663 to L2703 (`stats()`); structure by `ast.parse`.
- `main.py` L3395 to L3425 (queue and receiver construction), L3570 to L3640 (processor construction), L4060 to
  L4090 (health server and metrics provider); grep hits listed in 1.2.
- `core/schema.sql` L36 to L82 (`signals`), L578 to L600 (`webhook_audit`), L1010 to L1035 (`cron_heartbeat`)
  (A03's file, at the boundary).
- `core/state_store.py` L893 to L912 (`count_signals_today`); method boundaries by `ast.parse` for L903, L1424,
  L2591, L2936, L3321, L3335, L3346 (A03's file, at the boundary).
- `utils/cron_heartbeat.py` L30 to L96 (A16's file, at the interface).
- `scripts/eod_cleanup.py` L1 to L60, L95 to L135, L190 to L280 (A12's file, at the interface).
- `scripts/db_retention.py` L60 to L72 (A03's file, at the interface).
- `scripts/healthcheck_server.py` L133 to L262 (`/metrics`; A15's file, at the interface).
- `scripts/preflight/checks/signals.py` L44 to L89 (A20's file, at the interface).
- `ops/control_tower/aggregator.py` L108 to L140 (A15's file, at the interface).
- `reports/daily_trade_review.py` L706 to L722, L800 to L830 (A15's file, at the interface).
- `ops_dashboard/backend/readers/db_reader.py` L146 to L200 (A15's file, at the interface).
- `orders/order_manager.py` L458 to L478 (A10's file, at the interface).
- `config/scan_webhook_map.yaml`: only the lines with a scanner key, `strategy:` or `scanner_type` (no URL line read).
- `core/time_authority.py` (grep: L58 to L59, L94 to L99, `_IST` and `now_ist`; A01's file).
- `core/state_store.py` L105 to L114, L215 to L243 (connection model), L2588 to L2594 (`get_signals_for_date`),
  L3305 to L3326 (`insert_cron_heartbeat`) (A03's file, at the boundary).
- `main.py` L3543 to L3566 (zone-warmer construction).
- `scripts/preflight/checks/signals.py` L14 to L43 (A20's file); `scripts/preflight/checks/engine.py` (grep for the
  metrics URL, L29 to L30).
- `screening/entry_gate.py`, `screening/retest_monitor.py`, `screening/secondary_screener.py`,
  `orders/order_manager.py`: grep for their `signals` writes only (A07, A08, A10; interface only).
- `signals/signal_processor.py` L802 to L830 (docstring of the per-symbol-direction rule; a stock symbol in it is not
  reproduced) and L2186 to L2194, L2508 to L2516 (alert call context).
- `ops_dashboard/backend/readers/db_reader.py` (grep for status-family constants, L41, L53).

### 1.2 Commands and search patterns (all read-only)

- `git -C <legacy clone> show 970aabf:<path>` for every file above, output filtered.
- the search helper `the search wrapper` (non-test, non-doc, with the four mandatory exclusions and redaction) for:
  `(FROM|JOIN|INTO|UPDATE|TABLE( IF NOT EXISTS)?)\s+signals\b`; `webhook_audit`; `pb01_capture`; `cron_heartbeat`;
  `signal_retention_days|eod_cleanup\.py`; `DELETE FROM (cron_heartbeat|webhook_audit|signals)\b`; dynamic
  `DELETE FROM` forms; `count_signals_today|get_signals_for_date|get_last_heartbeat_for_job|get_inning_summary_by_date`;
  `(signal_processor|_processor|proc|sp)\.stats\(|get_runtime_metrics|\.stats\(\)`;
  `X-Queue-Depth|X-Queue-Warning|queue_depth`.
- `git ... grep -n -E` in `main.py` for the A06 wiring names (`signal_queue`, `SignalProcessor(`, `WebhookReceiver(`,
  `in_flight_release_fn`, `in_flight_heartbeat_fn`, `signal_expiry_sec`, `get_runtime_metrics`, `rate_limiter=`,
  `set_eod_capture`, `webhook_receiver.`).
- `grep -n` on scratch copies of the two `signals/` files for `_in_flight_release`, `_heartbeat(`, `_bump_metric(`,
  `_evidence_capture(`, `_notifier.`, `_fx_dispatch`, `update_signal_status`, `_emit_signal_alert(`.
- No legacy file was imported, executed, built or tested; no endpoint, URL, scanner, broker or Chartink page was
  contacted.

### 1.3 Project records and parts read

- Checked parts P01 to P10 (the A06 working parts folder), cited as P0n-Snnn; every fact restated here was re-read in
  the code at `970aabf`.
- A03 RECONCILED TOPIC RECORD (11-Nov-2026) and A03 AUDIT (10-Nov-2026): entries R-08, R-38, R-39, D-08, D-29, U-08,
  U-47, Z-26, P-02, P-11, P-12 and the IC-21 row (read in part); A03 evidence
  `A03_RETENTION_AND_CHECKPOINT_SCRIPTS_2026-11-09.md` (P09b-S019, P09b-S027, P09b-S066, P09b-S099).
- Master System Investigation Index (04-Nov-2026), Appendix A rows for the scripts named in section 2.

### 1.4 External pages read

- SQLite, "Date And Time Functions": https://www.sqlite.org/lang_datefunc.html (read 17-Nov-2026; used in P11-S032,
  P11-S059; re-opened in the check the same day).
- Added in the check: Python, "datetime": https://docs.python.org/3/library/datetime.html (read 17-Nov-2026;
  `isoformat()`, `date.today()`; P11-S032) and SQLite, "Datatypes In SQLite": https://www.sqlite.org/datatype3.html
  (read 17-Nov-2026; text comparison; P11-S059).
- No other external page was read for this part by its drafter; the library behaviour it relies on beyond that page (Python `queue`,
  `sqlite3`, the `try` statement; waitress; cachetools) is cited through the checked parts that read it (P03-S005,
  P03-S051, P05-S004, P05-S005, P05-S053). A first attempt to open the SQLite page was refused by a usage limit and
  succeeded on the second attempt the same evening.

### 1.5 Labels and limits

Labels follow the sourcing and labelling rules. No production log, database or journal is admitted, so every runtime fact (a
request received, a row written, a heartbeat recorded, a metric read) is UNKNOWN / NOT ESTABLISHED. The A03 G-19
finding is not opened or used. No credential, account, overlay or token file was opened; the webhook secret is named
only as the environment variable `WEBHOOK_SECRET`.

## 2. Producer-to-consumer map of A06 artefacts

This section maps each A06 artefact from the code that produces it to every code that reads, changes or removes it.
Lines are at `970aabf`; `WR` is `signals/webhook_receiver.py`, `SP` is `signals/signal_processor.py`. Owners are taken
from the Master System Investigation Index (entries and Appendix A). Other topics' logic is not studied.

### 2.1 Summary map

P11-S001. FACT (lines as cited in P11-S002 to P11-S030): the map in one table.

| # | Artefact | Produced by (A06 code unless marked) | Read or consumed by | Changed or removed by | Persistence |
|---|---|---|---|---|---|
| 1 | Inbound HTTP request | external senders; in the repository: `main.py` self-check and A20's check (GET `/health`), A19 scripts | `WR` `/webhook/<scanner_name>` route (L406 to L408) and `/health` route (L364 to L404) | none | none |
| 2 | HTTP response (code, JSON body, `X-Queue-*` headers) | `WR` `_process_request`, `_handle_eod`, the 503/429 branches, Flask's 500 handler | the sender; `WR` `_handle_webhook` itself (counts for the audit row, L512 to L517); A19's load-test script reads the headers | none | none |
| 3 | Queue item (5-tuple, or a retry dict) | `WR` L1047 to L1049 (new), L993 to L995 (M-S2 re-queue); `SP` L1510 to L1520 (FIX-069 retry dict); `SP` L426 (FIX-007 re-put; not wired under `main.py`) | `SP` dispatcher L385, L395; A08's zone warmer (symbol only, L388); `SP` workers | taken off the queue by the dispatcher only | memory only |
| 4 | Queue depth | `queue.Queue.qsize()` | `WR` L572, L741, L396; `SP` `stats()` L2702 (no production caller) | none | none |
| 5 | In-flight claim (per symbol) | `WR` `_claim_in_flight` L934 | `WR` `_claim_in_flight` (test-and-set), the sweeper L1189 to L1198 | released: `WR` reject routes; `SP` L1267 to L1271, L1699 to L1701, L1733 to L1735, L456 to L460; evicted: `WR` sweeper | memory only |
| 6 | TTL dedup key `(symbol, scanner_name)` | `WR` L947 | `WR` L942 | `WR` L999, L1030, L1066 (rolled back); TTL expiry | memory only |
| 7 | `signals` row | `WR` INSERT L963 to L980 | `WR` L987 to L991 (the only A06 read); A10, A12, A15, A03, A05, A07, A18, A19 readers (P11-S014) | A06: `WR` L1003 to L1007, L1052 to L1057; `SP` 26 `update_signal_status` calls; others: A07, A08, A10, A12 (P11-S013) | main database |
| 8 | `webhook_audit` row | `WR` `_write_audit` L1126 to L1154 | A01 census (`main.py` L1662 to L1675); A15 dashboard and reports; A03 drill | deleted after 90 days by `scripts/db_retention.py` (A03) | main database |
| 9 | EOD-webhook heartbeat (`cron_heartbeat` row, job `pb01_capture`) | `WR` L786 to L787, L801 to L803 through A16's `record_heartbeat` | generic `cron_heartbeat` readers (A15, A16); none names the job | nothing deletes `cron_heartbeat` rows | main database (relative path) |
| 10 | EOD capture hand-over | `WR` L794 to L795 (`submit`) | A18's `WatchlistCaptureWorker` | n/a | A18's |
| 11 | Runtime counters | `SP` `_rt_metrics`, `_stats`, `EntryThrottle` counters, `_fx_dispatch` | `SP.get_runtime_metrics` to A15's `/metrics`; A15/A01 effect telemetry | none (reset at process start) | memory only |
| 12 | Alerts | `SP` `_emit_signal_alert` (L486 to L555), EXPIRED warning (L1221 to L1231) | A14's notifier | n/a | A14's |
| 13 | Evidence records P1/P2 | `SP` `_evidence_capture` (L582 to L612) | A15's `EvidenceRecorder` (JSONL files) | A15's | files (A15) |

### 2.2 The HTTP request and the HTTP response

P11-S002. FACT (`WR` L364 to L413; `main.py` L3979 to L4054 as P01 section 5 records; `scripts/preflight/checks/
signals.py` L17 to L42 as P07-S046 records): the receiver consumes HTTP on two routes only: `POST /webhook/<scanner_name>`
(L406 to L408, to `_handle_webhook`) and `GET /health` (L364 to L404). Inside the repository the producers of requests
are `main.py`'s post-start self-check and A20's `WebhookResponsiveCheck`, both a GET of `/health` on the loopback
address, and the A19 scripts (HISTORICAL evidence only; Rama's decision E). HISTORICAL (`WR` L5): the external producer
is described as "Chartink scanner webhooks". Whether, when and from where any request arrived is UNKNOWN / NOT
ESTABLISHED.

P11-S003. FACT (`WR` L506 to L524): `_handle_webhook` is itself a consumer of the response it builds: it takes the
status code from the returned tuple and, only for a 200, re-reads the JSON body with `resp[0].get_json(silent=True)` to
take `accepted` and `rejected`, which become the audit row's `signals_accepted` and `signals_rejected` (P02-S067).
INTERPRETATION: the audit counts depend on the response's JSON keys; the EOD route's 200 body uses the same key
`accepted` for "symbols received" (L804), so the audit row of an EOD alert counts those symbols as accepted although no
`signals` row and no queue item exist for them (P02-S067; consumers in P11-S050). FACT (L778 to L788): the one exception
is the watchlist-disabled branch, whose 200 body carries `accepted: 0`; no EOD body carries `rejected`, so EOD rows record
0 rejected.

P11-S004. FACT (`WR` L576 to L577, L741 to L744, L395 to L404; search `X-Queue-Depth|X-Queue-Warning|queue_depth`
outside tests and documents): the queue depth leaves the receiver as `X-Queue-Depth: <size>/<capacity>` on the
backpressure 503 and on every batch answer, as `X-Queue-Warning: high` when the depth after the batch is at or above
`int(capacity * warning_pct)` (L574; `warning_pct` defaults to 0.60 in the code and is 0.60 in `config/system_config.yaml`
L128), and in the authenticated `/health` JSON (`queue_size`, `queue_capacity`, `queue_depth`). The
only in-repository reader of the two headers is `scripts/load_test_signals.py` L118 to L119, L132 to L133 (A19). Whether
Chartink reads any header is UNKNOWN / NOT ESTABLISHED.

### 2.3 The internal signal object and the queue item

P11-S005. FACT (`main.py` L3402 to L3415, L3575 to L3577; search of `main.py` for `signal_queue`): one
`queue.Queue(maxsize=app_config.system.signal_queue.capacity)` is built and passed to the receiver (`signal_queue=`,
L3408) and the processor (`signal_queue=`, L3576); no other component receives it.

P11-S006. FACT (lines as cited): the queue has four producers:

| Producer | Lines | Item | Put call | Wired under `main.py` |
|---|---|---|---|---|
| receiver, new signal | `WR` L1047 to L1049 | `(signal_id, scanner_name, symbol, price, triggered_at)` after the INSERT committed | `put_nowait` | yes |
| receiver, M-S2 re-accept of a `QUEUE_FULL` row | `WR` L992 to L995 | the same 5-tuple with the existing row's `signal_id` | `put_nowait` | yes |
| processor, FIX-069 retry on `BrokerRateLimitError` | `SP` L1501 to L1520 | dict with `signal_id`, `scanner_name`, `symbol`, `trigger_price`, `triggered_at`, `retry_count` | `put(..., timeout=1.0)` on a worker thread | yes (path reached only after the handoff, A10's error) |
| processor, FIX-007 rate-limiter pre-check | `SP` L418 to L426 | the item as received | `put(..., timeout=1.0)` | no: `main.py` passes no `rate_limiter` to `SignalProcessor` (L3575 to L3623) |

The consumers are the processor's dispatcher thread, `get(timeout=self._drain_poll_sec)` (L385) while running and
`get_nowait()` (L395) in the drain after the stop flag; each item goes to the executor as
`_process_one_safe(signal_tuple)` (L390, L397). The other readers of the queue read only its size (P11-S008).

P11-S007. FACT (`SP` L361 to L375, L388, L393 to L399; `main.py` L3609): before each submit in the running loop the
dispatcher calls `_warm_zones(signal_tuple)`, which reads the symbol (index 2 of a tuple, key `symbol` of a dict) and,
when a zone warmer is wired, calls `self._zone_warmer.enqueue(symbol)` inside a `try` that swallows every exception; the
drain loop after the stop flag does not call it. The zone warmer is A08's; `main.py` builds it only when the
retest or structure-exit flag is on (`zone_warmer = None` at L3545; built at L3549 to L3568 when `_v2_on or _struct_exit_on`, L3423, L3427; set back to `None` on a
wiring failure, L3569 to L3571). INTERPRETATION: the queue item has two consumers on the processor side: A08's
warmer (the symbol only, on the dispatcher thread, before the item is submitted to a worker) and the worker; the warmer sees retries
too, because retry dicts pass through the same loop.

P11-S008. FACT (`WR` L572, L741, L396; `SP` L2702; search for `.stats()` callers outside tests): the queue's size is
read by the receiver's backpressure test (L572), the batch answer's header (L741) and `/health` (L396), and by the
processor's `stats()` (L2702), which no non-test code calls.

P11-S009. FACT (`SP` L78, L81 to L91, L405 to L413, L876 to L887; `WR` L1047): the item is positional; the processor
names the fourth field `trigger_price` (`_SIGNAL_TUPLE_FIELDS`, L78) where the receiver's local is `price`; every
processor reader accepts both the tuple and the retry dict (L408 to L413, L878 to L887, L368 to L371, L86 to L89). The
contents and the not-carried row fields are P04-S024 and P05-S006. INTERPRETATION: the in-memory item and the `signals`
row are two representations of one signal joined only by `signal_id`; the queue's contents exist in memory only and are
lost at a process stop (P04-S020; P05-S005).

### 2.4 The in-flight claim and the TTL dedup key (in memory)

P11-S010. FACT (`WR` L206 to L208, L934, L944, L1000, L1014, L1031, L1067, L1074 to L1120, L1182 to L1207; `SP` L218,
L456 to L460, L1267 to L1271, L1699 to L1701, L1733 to L1735; `main.py` L3612; search of `SP` for
`_in_flight_release`): the claim is produced only by `_claim_in_flight` on a request thread. It is removed by the
receiver on its five reject routes after a claim (`DUPLICATE` from the cache, L944; `QUEUE_FULL` on the re-accept route,
L1000; `DUPLICATE` from the database, L1014; `STORE_ERROR`, L1031; `QUEUE_FULL`, L1067), by the processor through the
callback `in_flight_release_fn=webhook_receiver.release_in_flight` (`main.py` L3612) at the four processor sites listed
(the `finally` of `_process_one` skips it when the item was re-queued or handed to the allocator), and by the sweeper,
which deletes any claim whose `heartbeat_at` is more than 60 s old, checking every 60 s. The heartbeat refresher
`update_heartbeat` (L1110 to L1120) has no caller under `main.py`, which passes no `in_flight_heartbeat_fn` (L3575 to
L3623; P01 section 6). The resume paths `continue_from_gate` and `continue_from_retest` release nothing (search: no
`_in_flight_release` between L2010 and L2640). INTERPRETATION (P01, P03 section 4, P04 section 7): under `main.py` a
claim lives until the worker's release or, at the latest, about 60 to 120 s after it was taken.

P11-S011. FACT (`WR` L237 to L238, L940 to L947, L997 to L999, L1029 to L1030, L1065 to L1066): the TTL dedup key is
written, read and rolled back only by the receiver; no other module reads it. INTERPRETATION: it is not persisted, so a
process restart empties it (P03 section 2).

### 2.5 `signals` rows: writers and readers

P11-S012. FACT (`WR` L957 to L980; P05-S001 to P05-S003): A06 creates every `signals` row the trading path uses: one
INSERT per symbol that passes the receiver's checks, status `QUEUED`, 12 of 14 columns. The writes and reads by
column are tabulated in section 3.

P11-S013. FACT (search `(FROM|JOIN|INTO|UPDATE|TABLE...)\s+signals\b` and `update_signal_status(` outside tests and
documents; P05-S012, P05-S014): the writers of `signals` rows, with owners:

| Writer | Lines | What it writes | Owner |
|---|---|---|---|
| receiver | `WR` L963 to L980; L1003 to L1007; L1052 to L1057 | INSERT `QUEUED`; `QUEUED` on re-accept; `QUEUE_FULL` | A06 |
| processor | 26 calls of `update_signal_status` (P05-S008) | status and `rejection_reason` | A06 (sequence); A03 (method) |
| secondary screener, entry gate | `screening/secondary_screener.py` L604 to L620; `screening/entry_gate.py` L312, L512 | `PASSED`, `REJECTED_*`, `SKIPPED_*`, `GATE_*` | A07 |
| retest diverter and monitor | `screening/retest_monitor.py` L209, L349, L373 | `RETEST_*`, `REJECTED_RETEST_DUP` | A08 |
| order manager | `orders/order_manager.py` L718 to L724 | `trade_id` | A10 |
| end-of-day cleanup | `scripts/eod_cleanup.py` L120 to L124 (`PROCESSING` to `EXPIRED`), L248 to L267 (DELETE) | status; row deletion | A12 |
| CNC GTT real test | `scripts/t2_cnc_gtt_realtest.py` L227 | INSERT (test row; not traced) | A19 |

P11-S014. FACT (same search; `core/state_store.py` L895 to L907, L2588 to L2594, L2906 to L2942 as located by
`ast.parse`): the readers of `signals` rows, with owners (interface only):

| Reader | Lines | What it reads | Owner |
|---|---|---|---|
| receiver | `WR` L987 to L991 | `signal_id`, `status` by `(fingerprint, fingerprint_date)` after an `IntegrityError` | A06 |
| order manager | `orders/order_manager.py` L468 to L471 | `received_at` by `signal_id` (input to a time difference, L478) | A10 |
| end-of-day cleanup | `scripts/eod_cleanup.py` L109 to L115, L239 to L254 | counts and `signal_id` sets for its own updates and deletes | A12 |
| reports through `get_signals_for_date` (`SELECT * ... WHERE DATE(received_at) = ?`) | `reports/daily_report.py` L122; `reports/daily_trade_review.py` L375, L790, L2416, L2566, L2708 | whole rows of a date | A15 |
| `reports/daily_trade_review.py` | L1005 | `MAX(received_at)` of a date | A15 |
| dashboard reader | `ops_dashboard/backend/readers/db_reader.py` L182, L191, L617, L691, L848, L1043, L1058, L1662, L1894, L1974, L2078, L2097, L2194, L2209, L2246, L3102, L3505, L3698, L3824, L3902, L3909, L3955, L3979, L4027, L4050, L4071, L4100 | counts and rows by date, status, strategy, `signal_id`; `webhook_payload` at L2246 | A15 |
| health server | `scripts/healthcheck_server.py` L164 to L176, L236 to L243, L286 | counts by `DATE(received_at)`; latest `received_at` | A15 |
| Control Tower freshness | `ops/control_tower/freshness.py` L88 to L90 | count and latest `received_at` by `substr(received_at,1,10)` | A15 |
| system manager | `scripts/system_manager.py` L637, L640, L680 | counts by date, `REJECTED%`, stale `PROCESSING` | A15 |
| VM state check | `scripts/check_vm_state.py` L77, L89, L185 | latest rows; count in the last 10 minutes | A15 |
| trade journal, coach, screened CSV | `scripts/trade_journal.py` L50, L71; `scripts/gemini_trade_coach.py` L101; `scripts/generate_screened_stocks_csv.py` L148 | joins and selections | A15 |
| daily candles | `scripts/fetch_daily_candles.py` L121 | distinct symbols | A05 |
| strategy registry officer | `scripts/strategy_registry_officer.py` L59 | distinct column values | A07 |
| forward shadow recorder | `scripts/forward_shadow_record.py` L155 | join with `screener_results` | A18 |
| replay | `scripts/replay_signals.py` L46 | past rows | A19 |
| backup drill | `scripts/backup_restore_drill.py` L79, L88 | on the restored copy | A03 |

FACT (same search): `count_signals_today` (L895 to L907) and `get_inning_summary_by_date` (L2906 to L2942) have no
caller outside their definitions in non-test, non-document code. FACT (P05-S006): the processor never reads `signals`.
INTERPRETATION: after the INSERT, nothing in the trading path reads a `signals` row back to decide anything except the
receiver's own re-accept route (L987 to L1015) and the order manager's time difference; every other reader is a report,
dashboard, monitor, cleanup or research script.

P11-S015. FACT (`WR` L975; `config/scan_webhook_map.yaml` L17 to L84, keys and `strategy:` lines only; P01-S043): the
row's `strategy` column holds the scanner path segment, not the strategy name the processor resolves from the map
(`SP` L933 to L953); in the committed map all 16 keys equal their `strategy` values. INTERPRETATION: the consumers that
group by `strategy` (for example `db_reader.py` L617, L691, L1058, L2097, L3979, L4100) group by scanner name, which
equals the strategy name while the map keeps that property.

P11-S016. FACT (`core/schema.sql` L60 to L65; `reports/signal_status.py` L40 to L48; P05-S015, P02-S070): the schema
CHECK and A15's classifier both list `ACCEPTED`, `DUPLICATE`, `INVALID_SYMBOL`, `INVALID_PRICE`, `OUTSIDE_HOURS` and
`IN_PROCESS`, which are receiver answer statuses that no A06 code writes to `signals.status`; the classifier puts
`RESERVED` among the "qualified" statuses (L40 to L41) and `QUEUED`, `QUEUE_FULL`, `PROCESSING`, `TIMEOUT` among the
"other" statuses. FACT (`ops_dashboard/backend/readers/db_reader.py` L171 to L185): the dashboard counts `signals` rows
with `status='DUPLICATE'`; its docstring (HISTORICAL) says this is "typically ~0" because duplicates are dropped
before the INSERT. INTERPRETATION: at `970aabf` no A06 writer produces such a row; the receiver's duplicates exist only
as answer statuses and as part of the audit row's `signals_rejected` count (P02-S067, P02-S070).

### 2.6 `webhook_audit` rows: writer and readers

P11-S017. FACT (`WR` L487 to L489, L497 to L499, L529 to L534, L1126 to L1154; search for `webhook_audit` outside
tests and documents): the receiver is the only writer (INSERT only; P03-S049, P03-S052). The readers are: the A01
shutdown census (`main.py` L1662 to L1675; P03-S053); A15's dashboard reader (`ops_dashboard/backend/readers/
db_reader.py` L150 to L158, L715, L1036, L1414 to L1421, L2274, L3389, L3442) and the services and templates
built on it; A15's `reports/daily_trade_review.py` L809 to L813; A03's `scripts/backup_restore_drill.py` L53 (on the
restored copy). The deleter is `scripts/db_retention.py` (L66, L120; 90 days by `date` by default; a `--set TABLE=DAYS` command-line
value overrides, L170, L176 to L192, and neither declared command passes one, `config/cron_registry.yaml` L136, L151;
A03 Z-26).

### 2.7 The EOD-webhook heartbeat

P11-S018. FACT (`WR` L786 to L787, L801 to L803, L806 to L834; `utils/cron_heartbeat.py` L55 to L95;
`core/state_store.py` L3305 to L3325; `core/schema.sql` L1019 to L1026): for each EOD alert that passes the body checks the
code calls `record_heartbeat` once, which inserts one `cron_heartbeat` row (when the database file exists and no exception
occurs) with `job_name` `pb01_capture`, `executed_at` the IST time in ISO form, `status`
`SUCCESS` or (watchlist disabled) `FAILED`, no duration, and `message` `scanner=<name> symbols=<n> queued=<m>`, prefixed
`[func=DISABLED]` or `[func=EMPTY_NO_DATA]` when a functional status is given (P03-S056 for the path and the failure
handling). FACT (search `pb01_capture` outside tests and documents): no file other than the receiver names the job
`pb01_capture`, and `config/cron_registry.yaml` has no such job (the hits are `main.py` and `config/expected_managers.yaml`
for the worker's name `pb01_capture_worker`, `v3_chain/watchlist_capture.py` L77, and the receiver). FACT (search
`cron_heartbeat`): the readers of the table are generic: `ops_dashboard/backend/readers/db_reader.py` L1205 to L1209,
L3734, L3748 and the dashboard services built on it (A15); `ops/control_tower/aggregator.py` L116 to L119 (A15);
`scripts/system_manager.py` L426 (A15); and, through `get_cron_heartbeats_since` (`core/state_store.py` L3327 to L3340),
`scripts/cron_officer.py` L147, `scripts/cron_watchdog.py` L49 and `scripts/check_cron_drift.py` L69 (A16); A03's
`scripts/backup_restore_drill.py` names the table in its expected-table list for the restored copy (L43, L69, L144).
`get_last_heartbeat_for_job` (L3342 to L3352) has no caller outside its definition. Whether any row was written is
UNKNOWN / NOT ESTABLISHED (P11-S051).

P11-S019. FACT (`ops/control_tower/aggregator.py` L105 to L135): the Control Tower's cron check builds its `expected`
list from `config/cron_registry.yaml` (`expected_heartbeat_jobs`, L105 to L107), iterates only those jobs and reports a `FAILED` heartbeat only for those. INTERPRETATION: because `pb01_capture` is not a
registry job (P11-S018), the `FAILED`/`[func=DISABLED]` row that the receiver writes when the watchlist is disabled is
not reported by this check; whether the other generic readers show it, and how the A16 cron tools treat a job name
outside the registry, is A15's and A16's (not traced). The comment at `WR` L782 to L785 (HISTORICAL) says the row
makes the two states "distinguishable in one query".

### 2.8 The EOD capture hand-over

P11-S020. FACT (`WR` L156 to L161, L195, L776 to L804, L1156 to L1160; `main.py` L3712 to L3754 as P01 records): the
EOD route hands each symbol (after the alias map) to `self._eod_capture.submit(scanner_name=..., symbol=...,
triggered_at=...)`, counts a truthy return as captured, and logs a raised exception at ERROR without changing the 200
answer; the worker is late-bound by `set_eod_capture` from `main.py` L3747. The submit contract on the receiving side
and the `pb01_watchlist` writes are A18's (Rama's decision D; P01-S052, P01-S053).

### 2.9 Counters and metrics

P11-S021. FACT (`WR` whole file, search for `+= 1`, `counter` and `metric`; P02-S068): the receiver keeps no counter
beyond per-request locals (L507 to L508, L693 to L694, L790); its durable per-request records are the `webhook_audit` row
and, for EOD alerts only, the `pb01_capture` heartbeat row (P11-S018); everything else is log lines.

P11-S022. FACT (`SP` L217, L273 to L294, L675 to L738, L898, L1200, L1218 to L1220, L1244 to L1246, L1415, L1423,
L1463, L2035, L2230, L2268, L2315, L2394, L2535, L2564, L2597; `signals/entry_throttle.py` L117): the processor keeps
three in-memory sets of counters: `_rt_metrics` (`signals_processed` bumped right after the `PROCESSING` write at L898,
L2035, L2394; `entries_rejected` at L1200, L2315, L2597; `entries_throttled` at L1415, L2230, L2535; `entries_placed`
at L1463, L2268, L2564); `_stats` (screener outcomes and per-check reject buckets); and the entry throttle's own
counters. `get_runtime_metrics` (L683 to L738) returns `_rt_metrics`, three screener totals from `_stats`,
`EntryThrottle.metrics()` and five broker-quota gauges read from the store, the fund manager and the risk engine. The
FCFS dispatch also increments the effect-telemetry handle `signal_processor` (L217, L1423; A15 and A01's census).

P11-S023. FACT (`main.py` L4074 to L4082; `scripts/healthcheck_server.py` L133 to L261): the only consumer of
`get_runtime_metrics` is A15's health server, which merges the returned dict into its `/metrics` JSON (L251 to L257)
after its own database counts. FACT (search): `stats()` (L2663 to L2703) has no caller outside tests.

P11-S024. FACT (`SP` L898, L2035, L2394, L2680, L2690): the name `signals_processed` has two meanings in the
processor: in `get_runtime_metrics` it counts entries whose `PROCESSING` write returned (the bump follows the write at
L897 to L898, L2034 to L2035, L2393 to L2394): every `_process_one` entry, every resume entry and every FIX-069 retry,
since a retry re-enters `_process_one`; in `stats()` it is `processed + processed_no_placer`.
INTERPRETATION: `/metrics` carries the first meaning; the second is unused in production code.

P11-S025. FACT (`scripts/healthcheck_server.py` L136 to L176, L251 to L257; `SP` L683 to L738): `/metrics` sets
`signals_received` to the count of `signals` rows whose `DATE(received_at)` equals `date.today()` (the host's local
date), and initialises `queue_depth` and `queue_capacity` to 0; no code path sets either queue key (the health server
holds no queue and `get_runtime_metrics` returns no queue key). FACT (`scripts/preflight/checks/signals.py` L54 to L63,
L72 to L82; `scripts/preflight/checks/engine.py` L30): A20's `SignalsArrivedCheck` reads `signals_received` and
`WebhookBackpressureCheck` reads `queue_depth` and `queue_capacity` from a hard-coded loopback URL, port 8080, path `/metrics`; the latter
warns only when the capacity is non-zero (L78). INTERPRETATION (agrees with P03-S046, which records the dashboard side): at `970aabf`, whenever `/metrics` answers 200 the
backpressure check reports "webhook queue 0/?" and passes, whatever the real queue holds (otherwise it is skipped, L74 to
L75); `EntryThrottle.metrics()` (`signals/entry_throttle.py` L117 to L125) adds no queue key either; the real depth is available only from the receiver's
`/health` and headers (P11-S004). `signals_received` counts stored rows, so symbols refused before the INSERT and EOD
symbols are not in it. The checks are A20's and the server A15's; recorded at the interface only.

### 2.10 Alerts and evidence records

P11-S026. FACT (`SP` L486 to L555, L1221 to L1231, L1371, L2192, L2514; `WR` whole file; P02-S068, P04-S043): A06 code
sends notifications only from the processor: the `INTRADAY SIGNAL` message (`notifier.send`, severity INFO), called
after the reservation and before placement on the FCFS, gate and retest paths (L1370 to L1380, L2192, L2514); and the
`Signal EXPIRED` warning (`send_warning`), at most one per 60 s per processor. The receiver sends none; its store
failure and its sweeper evictions write CRITICAL log lines only (L1036 to L1039, L1202 to L1207). The notifier and any
alerting on log lines are A14's; whether any alert was sent is UNKNOWN / NOT ESTABLISHED.

P11-S027. FACT (P05-S024 to P05-S029, re-checked at `SP` L582 to L612, L1202 to L1211, L1423 to L1445): the processor
produces `P1_ACCEPT` and `P2_REJECT` evidence records for A15's recorder (`EvidenceRecorder`, `core/evidence_contract.py`
L420; built or set to `None` at `main.py` L3259 to L3266), which appends them to dated JSONL files under
`data_store/evidence/` (`core/evidence_contract.py` L302 to L332); nothing in A06 reads them; A03's
`scripts/backup_evidence.py` copies them (L4 to L13, L59; interface only).

## 3. Storage handoffs at the A03 boundary

A03 owns the schema, the store, its connection model and its transactions; A12 owns `scripts/eod_cleanup.py`; A16
owns `utils/cron_heartbeat.py`. This section records what A06 code reads and writes, how, and what other code later
does to the same rows. Earlier parts are cited where they already establish a point.

### 3.1 The connection and transaction model A06 code relies on

P11-S028. FACT (`core/state_store.py` L107 to L113, L215 to L243, L505 to L543; P05-S004; A03's file, at the boundary): every
`StateStore` method runs on a connection owned by the calling thread, opened on first use with `isolation_level=None`,
`timeout=30`, `check_same_thread=True` and the pragmas `journal_mode = WAL`, `synchronous = FULL`, `foreign_keys = ON`,
`temp_store = MEMORY` and `busy_timeout = 30000`; `transaction()` is `BEGIN IMMEDIATE`, the statements, `COMMIT`, or
`ROLLBACK` and re-raise. INTERPRETATION: the receiver's writes run on the waitress worker threads' connections, the
processor's on the `sp-worker` threads' connections, the census read on the shutdown thread's connection, and each EOD
heartbeat on a connection of a separate, short-lived store (P11-S036); all of them meet at SQLite's single write lock,
with up to about 30 s of waiting before an `OperationalError` (P03-S051, A03 P-12).

### 3.2 `signals`: A06's operations

P11-S029. FACT (lines as cited): every A06 operation on `signals`:

| # | Operation | Code | Statement | Columns | Transaction | On failure |
|---|---|---|---|---|---|---|
| 1 | create | `WR` L963 to L980 | `INSERT INTO signals (...) VALUES (12 values)` | the 12 of P05-S003; `rejection_reason`, `trade_id` stay NULL | own `transaction()`, committed before the queue put | `IntegrityError`: re-accept route or `DUPLICATE` (P03-S010 to P03-S012); any other exception: claims released, CRITICAL line, `STORE_ERROR`, batch 503 (L1016 to L1044) |
| 2 | look up the existing row | `WR` L987 to L991 | `SELECT signal_id, status ... WHERE fingerprint = ? AND fingerprint_date = ?` | `signal_id`, `status` | none (plain read) | not caught at this level: leaves `_process_signal` from inside the `except` clause (P03 section 4, the L987 trigger) |
| 3 | re-accept flip | `WR` L1003 to L1007 | `UPDATE signals SET status = 'QUEUED' WHERE signal_id = ?` | `status` | own transaction, after the re-queue put | ERROR line; answer stays `ACCEPTED` (A03 R-08 for the order) |
| 4 | mark queue full | `WR` L1052 to L1057 | `UPDATE signals SET status = 'QUEUE_FULL' WHERE signal_id = ?` | `status` | own transaction | ERROR line; row stays `QUEUED` with no item (P05-S005) |
| 5 | status changes | `SP`, 26 calls of `update_signal_status` (`core/state_store.py` L1408 to L1426) | `UPDATE signals SET status = ?, rejection_reason = ? WHERE signal_id = ?` | `status`, `rejection_reason` (NULL when no reason); `ts` argument not stored (A03 P-02) | one transaction per call; `RESERVED` inside the fund manager's lock (P05-S010) | as P05 section 4 records |

FACT (whole files): no A06 code deletes a `signals` row, writes `trade_id`, or reads `signals` other than operation 2;
no UPDATE carries a predicate on the current status (P05-S007).

P11-S030. FACT (`core/schema.sql` L42 to L79, L581 to L593): `signals` has no column that identifies the HTTP request
or its `webhook_audit` row, and `webhook_audit` has no column that identifies a signal (its columns are `id`, `ts`,
`scanner_name`, `source_ip`, `payload_size_bytes`, `response_code`, `signals_accepted`, `signals_rejected`,
`duration_ms` and the generated `date`). FACT (`WR` L677, L959, L1136): a request's rows carry `received_at`, taken once
before the per-symbol loop, while its audit row's `ts` is taken when the audit row is written. INTERPRETATION: a
`signals` row can be matched to its request only approximately (scanner name and time); `signals.received_at` and
`webhook_audit.ts` of the same request differ by the request's handling time.

P11-S031. FACT (`WR` L719 to L728, L529 to L534; `SP` L895 to L897): for one request the order of durable writes is:
one `signals` INSERT (and possibly an UPDATE) per symbol, in the order of `stocks`, then the `webhook_audit` row in the
`finally`; the processor's `PROCESSING` write comes later on another thread, and may come before the audit row
(INTERPRETATION: a worker can take an item while the request is still handling later symbols). No two of these writes
share a transaction. INTERPRETATION: a stop after some INSERTs and before the audit row leaves rows with no audit row;
a failed audit INSERT has the same effect (logged at ERROR, L1153 to L1154). The request-level answers (429, the
shutting-down and backpressure 503s, 401, 404, 403 and 400) and every EOD answer lead to an audit-row write and no
`signals` write; a batch 503 (`QUEUE_FULL` or `STORE_ERROR`) and a 500 can leave rows for symbols handled before it
(P02-S069). INTERPRETATION (P02-S071 and its rows 1, 2, 4 and 30 to 32): answers produced outside `_handle_webhook`
(Flask's 404 and 405, the 413 raised by the body read at L480 before the `try`, and waitress's own 413, 431 and 400)
write no audit row at all.

### 3.3 `signals`: time and date formats as the consumers read them

P11-S032. FACT (`core/time_authority.py` L58 to L59, L94 to L104; `WR` L652 to L653, L677 to L678, L958 to L961, L1136):
`received_at`, `expires_at`, `triggered_at` and `webhook_audit.ts` are written with `datetime.isoformat()` of aware
datetimes in the fixed zone `_IST` (UTC+05:30). Current external context (Python "datetime", 
https://docs.python.org/3/library/datetime.html, read 17-Nov-2026): `isoformat()` returns
`YYYY-MM-DDTHH:MM:SS.ffffff` "if microsecond is not 0" and `YYYY-MM-DDTHH:MM:SS` "if microsecond is 0", with the UTC offset
appended as `+HH:MM` when `utcoffset()` is not `None`; the default separator is `'T'`; INTERPRETATION: so the stored text
carries a `T` separator and a `+05:30` suffix (microseconds when present);
`fingerprint_date` and `webhook_audit.date` are the IST calendar date (`received_at.date()`; `substr(ts, 1, 10)`). FACT
(lines as cited): readers derive a signal's date in three ways: `DATE(received_at)` (`core/state_store.py` L2591, used by
the reports; `scripts/healthcheck_server.py` L165, L172, L237, L286), `substr(received_at, 1, 10)` or `SUBSTR`
(`core/state_store.py` L903, a method with no caller, P11-S014; `ops/control_tower/freshness.py` L88 to L90; `scripts/system_manager.py` L637, L640;
`scripts/eod_cleanup.py` L113, L122 on `triggered_at`) and `received_at LIKE '<date>%'` (`db_reader.py` L191, L1043 and
others). Current external context (SQLite "Date And Time Functions", https://www.sqlite.org/lang_datefunc.html, read
17-Nov-2026): formats with a `T` separator and fractional seconds are accepted; such values "may be optionally followed
by a timezone indicator of the form "[+-]HH:MM""; "The date and time functions use UTC or "zulu" time internally"; "Any
non-zero "HH:MM" suffix is subtracted from the indicated date and time in order to compute zulu time"; "The date()
function returns the date as text in this format: YYYY-MM-DD." INTERPRETATION: `DATE(received_at)` gives the UTC date,
which equals the IST date for rows received from 05:30 IST onward and is the previous day for rows received between
00:00 and 05:29 IST; the `substr` and `LIKE` forms give the IST date. The health server compares `DATE(received_at)`
with `date.today()` (L21, L136); current external context (the Python page above): `date.today()` "Return[s] the current
local date"; INTERPRETATION: the host's local date. For signals received during market hours the three forms agree; the
installed SQLite version and the hosts' time zones are UNKNOWN / NOT ESTABLISHED. The readers are A15's (the DATE/`substr`
difference before 05:30 IST is already recorded by A03: STUDY section 14.1 point 21 and AUDIT H-11; IDs and
classifications unchanged; a further text comparison is P11-S059).

### 3.4 `signals`: what other topics later do to A06's rows (interface only)

P11-S033. FACT (`scripts/eod_cleanup.py` L1 to L16, L105 to L127; `deploy/cron/trading-system.cron` L100 and
`config/cron_registry.yaml` L454 to L464, declarations only; A12's file): step 1 of the end-of-day cleanup sets
`status = 'EXPIRED'` on rows still `PROCESSING` whose `SUBSTR(triggered_at, 1, 10)` is earlier than the run date, in one
transaction. HISTORICAL (L110 to L112): it used to filter `IN_PROCESS`, "a status the pipeline NEVER persists". The
cron line runs the script at 15:50 Monday to Friday (declaration; whether it ran is UNKNOWN / NOT ESTABLISHED).
INTERPRETATION: a row left `PROCESSING` by a stop is turned into `EXPIRED` at the first run on a later date; rows left
`QUEUED`, `QUEUE_FULL`, `PASSED` or `RESERVED` are never touched (P05-S022).

P11-S034. FACT (`scripts/eod_cleanup.py` L43 to L66, L192 to L271; `config/system_config.yaml` L481 to L482;
`core/config_loader.py` L1976 to L1984; A03 AUDIT U-47 (MATCH, owner A12) and U-08; A03 RECONCILED TOPIC RECORD, row
IC-21): step 4 deletes, in batches of 2,000 signal ids per transaction, the rows whose status is `EXPIRED`,
`DUPLICATE` or `GLOB 'REJECTED*'`, whose `fingerprint_date` is earlier than the run date minus
`signal_retention_days` (90 in the committed file and as the model default; the function default L76 and the
config-failure fallback L62 to L67 are also 90; a command-line value overrides, L47 to L48, L57 to L58), and which
have no `trades` row; it first deletes the same ids from `screener_results`, `gate_state`, `shadow_trades`,
`sr_detector_results` and `retest_state`. HISTORICAL (L9): the docstring says "Prune old signal fingerprints (>7
days)". INTERPRETATION (FACT basis: the search for `DELETE FROM` finds no other `signals` deleter, and `scripts/db_retention.py`
L63 to L70 has no `signals` entry): rows in every other status (`QUEUED`, `QUEUE_FULL`, `PROCESSING`, `PASSED`,
`RESERVED`, `PROCESSED`, `PROCESSED_NO_PLACER`, `PLACEMENT_FAILED`, `TIMEOUT`, `GATE_*`, `RETEST_*`, `SKIPPED_*`,
`DROPPED_*`) are never deleted by any code while they keep that status (only an earlier-dated `PROCESSING` row can move
to `EXPIRED` through step 1 and then fall under the prune); `DUPLICATE` is in the filter although no A06 code writes it (P11-S016); the receiver's
`webhook_payload` (sanitized; P02 section 2.5) is kept for as long as its row. The prune and its guard are A12's and
A03's; their IDs and classifications are unchanged.

### 3.5 `webhook_audit`

P11-S035. FACT (P03-S049 to P03-S054, re-checked at `WR` L1126 to L1154, `main.py` L1662 to L1675, `scripts/
db_retention.py` L63 to L70, L120): one INSERT per audited request in its own transaction on the request thread, error
logged at ERROR and swallowed; never read, updated or deleted by A06 code; counted by date at shutdown by A01's census;
deleted after 90 days by `date` (the default; override as in P11-S017) by A03's `db_retention.py` (A03 Z-26, MATCH; schedule declared 02:30, A03 P09b-S061 and
P09b-S062). FACT (`core/schema.sql` L583): the column comment says `ts` is the time "when request arrived";
P03-S050 records that it is the time of writing. INTERPRETATION: a reader of ranges longer than 90 days (for example
`db_reader.py` L2268 to L2274) sees only what the prune has left; whether that matters is A15's.

### 3.6 The EOD-webhook heartbeat store

P11-S036. FACT (`WR` L806 to L834; `utils/cron_heartbeat.py` L55 to L95; `core/state_store.py` L3305 to L3325;
P03-S056; A03 AUDIT D-08 (owner of the call site: A06), D-09, D-13 and D-29): each heartbeat call constructs a new
`StateStore` on the relative default path `data_store/trading_system.db` (L61, L84) on the request thread, inserts one
`cron_heartbeat` row in its own `transaction()` (L3319 to L3325), and closes the store only on success (L92); a missing
file or any exception returns `False` with no log line; the receiver ignores the return value and catches only what
its own `try` raises. A03 recorded the full store per heartbeat (D-08), the relative default (D-09), the unclosed store
on failure (D-13) and the never-raise guard (D-29, MATCH); their IDs and classifications are unchanged.

P11-S037. FACT (search for deletes of `cron_heartbeat` outside tests and documents; `scripts/db_retention.py` L63 to
L70): no code deletes `cron_heartbeat` rows, and the table is not in the retention policy. INTERPRETATION: the
`pb01_capture` rows accumulate, one per EOD alert, for the life of the database; the retention question is A03's and
A16's.

### 3.7 Error handling at A06's storage call sites, in one view

P11-S038. FACT (sections 3.2 to 3.6; P03-S051, P03-S055, P03-S056; P05 section 4): what a storage failure does at each
A06 call site:

| Call site | Logged as | Effect on the answer or the pipeline | What remains in storage |
|---|---|---|---|
| `signals` INSERT, non-constraint error | CRITICAL (L1036 to L1039) | symbol `STORE_ERROR`; batch 503; claims released | no row |
| `signals` SELECT after `IntegrityError` | CRITICAL "Unhandled exception processing ..." (L526) | 500 for the whole request; later symbols not handled; this symbol's claims stay held (P03 section 4) | earlier symbols' rows; audit row with 500 |
| re-accept flip | ERROR (L1009 to L1011) | answer `ACCEPTED`; item queued | row stays `QUEUE_FULL` until the processor's `PROCESSING` |
| mark `QUEUE_FULL` | ERROR (L1059) | symbol `QUEUE_FULL`; batch 503 | row stays `QUEUED`, no item |
| `webhook_audit` INSERT | ERROR (L1154) | none | no audit row |
| EOD heartbeat | nothing (helper returns `False`); WARNING only for exceptions in the receiver's own `try` (L830 to L834) | none (200 unchanged) | no heartbeat row |
| processor status writes | as P05-S016 to P05-S021 | as P05-S016 to P05-S021 | last committed status |

INTERPRETATION: the only storage failure that changes what the sender is told is a failure on the `signals` INSERT or
the read that follows an `IntegrityError`; every other failure is logged (or, for the heartbeat, not) and leaves the
answer unchanged.

## 4. Duplication record (the same intake job done in more than one place)

This section records, without judging, the places where one intake job is done more than once or where one name or
count is produced in more than one way. It answers direction question 27 on its duplication and consistency side only.
Each item names the places, what differs, and the part that studies it in detail.

### 4.1 Expiry

P11-S039. FACT (`WR` L677 to L679, L916 to L926, L960 to L961; `SP` L222, L914 to L921, L1221 to L1231;
`scripts/eod_cleanup.py` L105 to L127; P04-S036 to P04-S043): the "too old" job is done or represented in four places:

| Place | Basis | Clock read | Outcome | Persisted as |
|---|---|---|---|---|
| receiver, per symbol | `now - triggered_at > expiry_sec` (IST attached only to a naive value) | `now_ist()` at L919, per symbol | answer `EXPIRED`; no row | nothing (answer and audit count only) |
| stored deadline | `received_at + expiry_sec` | `received_at`, once per request (L677) | written to `expires_at` | `signals.expires_at`, read by name only by A15's dashboard reader (`db_reader.py` L826; P04-S041) |
| processor, per worker | `now - triggered_at.replace(tzinfo=IST) > _signal_expiry_sec` (unconditional relabel) | `now_ist()` at L910 | `REJECTED_EXPIRED` row, alert at most once per 60 s | `signals.status = 'REJECTED_EXPIRED'` |
| end-of-day cleanup (A12) | row still `PROCESSING` with an earlier `triggered_at` date | the run date | `EXPIRED` row | `signals.status = 'EXPIRED'` |

Both checks read the same key, `signal_queue.expiry_sec` (the receiver per request, the processor once at
construction; P04-S036). INTERPRETATION: three different stored or answered forms mean "expired" (`EXPIRED` as an
answer, `REJECTED_EXPIRED` as a processor reject, `EXPIRED` as a cleanup status), and the stored deadline is computed
from a different start (`received_at`) than both checks (`triggered_at`). The resume paths of A07/A18 have no age check
(P04-S042).

### 4.2 Duplicate and repeat controls

P11-S040. FACT (`WR` L934, L940 to L947, L949 to L1015; `core/schema.sql` L82 to L83; `SP` L802 to L830, L1311 to
L1313, L2141 to L2143, L2477 to L2479; P03-S001; P06 section 2; `screening/retest_monitor.py` L349 to L351): the
"already seen" job is done in three receiver layers with three different keys (the in-flight claim on `symbol`; the
TTL cache on `(symbol, scanner_name)` with a window from the moment the key is stored; the unique index on the hash of
scanner, symbol and time slot plus `fingerprint_date`; P03-S001). After the screening call, separate repeat controls with
other keys belong to other owners: the entry throttle's per-symbol cooldown (P06; admission decisions A07/A09), the
one-trade-per-symbol-and-direction rule (`SP` L802 to L835, called at L1312, L2142, L2478; A09's admission side under
Rama's decision A; HISTORICAL: its docstring says "DEFAULT OFF"; FACT: the model default is `False`,
`core/config_loader.py` L784, and the committed `config/system_config.yaml` L302 sets
`one_trade_per_symbol_direction_per_day: true`; the effective value is UNKNOWN / NOT ESTABLISHED) and the retest
diverter's `REJECTED_RETEST_DUP` (A08). Further symbol-level checks, not traced: the risk engine's
`DUPLICATE_SYMBOL` check (`capital/risk_engine.py` L788 to L792; A09), the allocator's one-per-symbol rule within a batch
(`allocation/portfolio_allocator.py` L183; A18), both after the screening call, and the shadow-inning guard (`SP` L928,
L1976; A11), which runs before it. INTERPRETATION: the same
symbol can be refused for repetition at six or more points with different keys and windows; the receiver's three layers
are A06's (P03), the rest are recorded at the interface only.

P11-S041. FACT (`WR` L996 to L1001, L1016 to L1031, L1060 to L1067): the "roll back both claims" job (pop the TTL key,
release the in-flight claim) is written out separately at three sites: the re-accept route when the queue is still
full, the `STORE_ERROR` route and the `QUEUE_FULL` route; the cache-hit `DUPLICATE` (L944) and the database `DUPLICATE`
(L1014) release only the in-flight claim. HISTORICAL (L59 to L66): the comment requires every retryable status to have
"released both the in-flight claim and the fast-path dedup claim". INTERPRETATION: at `970aabf` the three retryable
sites each release both; the rule is kept by repetition, not by one shared routine.

P11-S042. FACT (`WR` L206 to L208; `SP` L253 to L257, L711 to L735): the word "in-flight" names three different things:
the receiver's per-symbol claim dict (WR17, FIX-011); the processor's `_in_flight_count`, a counter guarded by an
`RLock` that the FIX-018 comment describes as protection for "signals between approve() and DB insert" (A09's
admission side); and the `/metrics` gauge `broker_in_flight` from the fund manager's `count_live_reservations` (A09).
Likewise "heartbeat" names the in-flight heartbeat (FIX-011, `WR` L1110 to L1120; not wired under `main.py`) and the
EOD `cron_heartbeat` row (P11-S018). INTERPRETATION: these are name collisions, not duplicates of one job; they are
listed because a reader of logs, metrics or code can confuse them.

### 4.3 Symbol, scanner and strategy normalisation

P11-S043. FACT (`WR` L258 to L292, L670, L701, L709 to L710, L774, L792; `SP` L876 to L1006; P04-S045 to P04-S049):
symbol text is normalised only in the receiver, by one rule applied in two places with the same expression
(`self._alias_map.get(raw_symbol.upper(), raw_symbol)`: the intraday loop, L701, and the EOD loop, L792); the
excluded-symbol test compares upper-cased text (L710) although an alias miss keeps the received case; the processor
applies no change. A second loader of `config/symbol_aliases.yaml` in `main.py` serves the paper quote provider
(paper-only; not traced; P04-S048).

P11-S044. FACT (`WR` L552 to L554, L562 to L563, L617 to L633, L975; `SP` L208, L560 to L580, L933 to L953;
`main.py` L3585): the scanner name is checked or resolved in four places: the receiver's membership test against the
live `app_config.scan_webhook_map.scanners` (404 on a miss); the receiver's comparison of the body's `scan_name`
(lower-cased, spaces to underscores, account-tag prefix stripped) with the path; the processor's Step 2, on its own
shallow copy of the same mapping taken at construction (`dict(scan_webhook_map)`, L208), with three
`UNKNOWN_STRATEGY` rejects; and `_evidence_strategy_for`, which repeats Step 2's lookup for evidence records (its
docstring says so, HISTORICAL). The receiver stores the path segment as `strategy` without the lookup (P11-S015).
INTERPRETATION: both sides start from the same object; the receiver reads it on every request, the processor holds a
copy, so they would disagree only if the mapping object or its contents changed in a running process (A02's question);
a scanner that passes the receiver's test always has an entry in the processor's copy while that holds.

### 4.4 Request parsing on the intraday and EOD routes

P11-S045. FACT (`WR` L585 to L674, L751 to L774, L836 to L851; P01-S052): the body is parsed by two separate pieces of
code. Differences: the EOD route accepts a fourth `triggered_at` format (`%Y-%m-%d`); it does not run
`_cast_numeric_fields`; it requires `trigger_prices` to be present but never reads it or checks that it is a string or
that its length matches; it drops empty `stocks` elements (L774) where the intraday route keeps them and answers
`INVALID_SYMBOL` (L670, L905 to L906); it writes none of the intraday route's own WARNING lines for its 400s (for
example L589 to L592, L611 to L614, L659 to L661), although both routes' 400s get `_handle_webhook`'s raw-body
WARNING (L519 to L523); it uses its own `now_ist()` for a time-only value; and it never compares the body's `scan_name` with the path
(the intraday check at L617 to L633 has no EOD counterpart).
INTERPRETATION: a payload accepted on one route can be refused on the other, and the reverse.

### 4.5 Kill switch, entry window and backpressure

P11-S046. FACT (`WR` L566 to L583; `SP` L906 to L912, L977 to L982; P04-S028; P05-S030): the kill switch and the
entry window are checked by the receiver once per request (`is_active()` with no argument; `is_entry_allowed(now)`)
and again by each worker (`is_active("entry")`; `is_entry_allowed(now)` and the per-strategy window), with separate
clock reads; the EOD route skips both, and the backpressure test, because it returns at L563 to L564 before L567
(P01-S052). The meaning of the argument to `is_active` is A13's. The resume paths
repeat the kill-switch, window and shadow checks without the age check (P04-S042).

P11-S047. FACT (`WR` L570 to L578, L1048 to L1068; `main.py` L3402 to L3404; P03 section 5): queue capacity is
enforced twice with two outcomes: the request-level threshold `int(capacity * backpressure_pct)` answers 503 before any
row is written, and the hard `maxsize` makes `put_nowait` raise `queue.Full`, which leaves a `QUEUE_FULL` row and a
batch 503.

### 4.6 Scanner reachability and endpoint checks (Rama's decision C)

P11-S048. FACT (P07-S040 to P07-S047, re-checked at `scripts/preflight/checks/signals.py` L17 to L42 and L44 to L82,
`scripts/preflight_scanner_check.py` L7, L27, L74, L95 to L115, L203 to L231, `utils/startup_checks.py` L652, L1592, and a
search of `scripts/preflight/` for `chartink|check_scanner|scanner_connectivity`, whose only hits are file names in
`config_integrity.py` L22 to L23 and comments):
the outbound Chartink-URL check exists twice, sharing one function (`utils.startup_checks.check_scanner_connectivity`)
with two fetchers: the boot step 7 with `main.py`'s `urllib` fetcher (one attempt, a warning only) and the Appendix A
script with its own `requests` fetcher (up to three attempts; exit code). A20's pre-flight has no Chartink-URL check.
The local endpoint check also exists twice: `main.py`'s post-start GET of `/health` (2xx or 401 pass) and A20's
`WebhookResponsiveCheck` (exactly 200 or 401 pass). INTERPRETATION: the shared function keeps the success rule the
same for the two outbound checks; the retry policy, timeout source and effect differ (P07-S047 table).

### 4.7 Status vocabularies and signal counts

P11-S049. FACT (`WR` L21 to L22, L59 to L66; `core/schema.sql` L50 to L70; `reports/signal_status.py` L39 to L82;
`scripts/eod_cleanup.py` L234 to L236; `ops_dashboard/backend/readers/db_reader.py` L41, L53, L188 to L198): the signal status
vocabulary is written out separately in at least five places: the receiver's docstring list WR10 and
`_RETRYABLE_STATUSES`; the schema CHECK and column comment; A15's classifier sets; A12's prune filter; and the
dashboard reader's status families (`_RISK_REJECT_STATUSES`, L41; `_CAPITAL_REJECT_STATUSES`, L53). They differ: the CHECK and the classifier include answer-only statuses that no
A06 code stores (P11-S016); the column comment (L50) omits, among others, `QUEUE_FULL`, `PROCESSING`, `RESERVED`, `PLACEMENT_FAILED`,
`PROCESSED_NO_PLACER`, `TIMEOUT` and `RETEST_*` (P05-S015); the CHECK, the classifier and A15's readers also carry
`TRADED`, which no code writes (P11-S057); the WR10 list
omits `REJECTED_EXCLUDED_SYMBOL` and includes `OUTSIDE_HOURS`, which the code never returns per symbol (P02-S071).

P11-S050. FACT (lines as cited): "signals received" is computed in at least five ways by the consumers of A06's
stores: `SUM(signals_accepted + signals_rejected)` from `webhook_audit` (dashboard `webhook_funnel`, `db_reader.py`
L147 to L168, which calls `SUM(signals_accepted)` "validated"); `COUNT(*)` of `signals` by `DATE(received_at)`
(`/metrics` and `/metrics/prometheus`, `scripts/healthcheck_server.py` L164 to L169, L286 to L287); `COUNT(*)` by
`substr(received_at, 1, 10)` (Control Tower, `ops/control_tower/freshness.py` L88; system manager,
`scripts/system_manager.py` L637); `COUNT(*)` by `received_at LIKE` (`db_reader.py` L1043, L3955); and the report's
two figures. HISTORICAL (`reports/daily_trade_review.py` L709 to L718): the report states "Reached storage (accepted) =
COUNT(signals) == SUM(webhook_audit.signals_accepted)" and "Dropped pre-storage = SUM(signals_rejected) [dupes +
invalid/out-of-window/backpressure ...]". FACT (A06 producer side, re-checked): the audit counts are recorded only for
200 answers (`WR` L512 to L517); a batch 503 records 0 and 0 although rows exist for its accepted and `QUEUE_FULL`
symbols (L733 to L734, L963 to L980, L1052 to L1057); an EOD 200 records its symbol count as accepted with no rows (L804; 0 in the watchlist-disabled branch, L788); a 500
(for example the L987 read failing) records 0 and 0 although rows exist for symbols handled before it (L506 to L528);
a re-accept counts `ACCEPTED` without a new row (L1012 to L1013); the out-of-window 403 and the request-level
backpressure 503 record 0 rejected (L575 to L583); a failed audit INSERT records nothing while rows exist (L1153 to
L1154). INTERPRETATION: on these routes the report's stated identity is not guaranteed, and out-of-window and backpressure
refusals are not part of `SUM(signals_rejected)`; differences can also offset each other (for example a `QUEUE_FULL` row
recorded as 0 in its batch 503 and counted `ACCEPTED` on its re-accepted retry). FACT (`reports/daily_trade_review.py`
L790, L809 to L811; `core/state_store.py` L2591): the report's `signals` side is selected by `DATE(received_at)` and its
`webhook_audit` side by the stored `date`; INTERPRETATION (P11-S032): rows received between 00:00 and 05:29 IST fall on
the previous day in the first and on the IST day in the second. The report and the dashboard are A15's; how they present the
difference is theirs. The `signals_processed` name collision is P11-S024.

### 4.8 Statements added in the check

P11-S057. FACT (`scripts/healthcheck_server.py` L171 to L176; `core/schema.sql` L63; `reports/signal_status.py` L40;
search for the literal `'TRADED'`/`"TRADED"` outside tests and documents): `/metrics` sets `signals_traded` to the count
of today's `signals` rows with `status = 'TRADED'`; the schema CHECK allows `TRADED` and A15's classifier counts it as
qualified; no writer in the table of P11-S013 writes it (the literal appears only in readers, in the store's class
docstring, `core/state_store.py` L161, and as a `shadow_trades.live_status` default, `capital/shadow_engine.py` L103,
L236 to L246). HISTORICAL (`scripts/eod_cleanup.py` L221): the prune comment names a trade audit trail
"QUEUED->...->TRADED". INTERPRETATION: for every row the code at `970aabf` writes, `signals_traded` is 0; a signal that
became a trade is marked by `trade_id` (A10, P11-S013), not by status. The reader is A15's; recorded at the interface only.

P11-S058. FACT (`core/migrations.py` L115 to L132, L254 to L310; A03's file, at the boundary): A03's migration runner
rebuilds `signals` (versions 25 and 38) and `webhook_audit` (version 27) by creating the current table, copying the
common columns with `INSERT INTO ... SELECT` and renaming it, when it applies those versions. INTERPRETATION: besides the
writers of P11-S013 and P11-S017, a schema migration rewrites existing `signals` and `webhook_audit` rows in bulk; when
the runner is invoked is A03's (not traced here), and whether any rebuild ran is UNKNOWN / NOT ESTABLISHED.

P11-S059. FACT (`scripts/check_vm_state.py` L184 to L186; A15's file): the `--health` count "Signals (last 10 min)"
compares `received_at` text with SQLite's `datetime('now', '-10 minutes')`. Current external context (SQLite "Date And
Time Functions", page of P11-S032, and "Datatypes In SQLite", https://www.sqlite.org/datatype3.html, both read
17-Nov-2026): `datetime()` "returns the date and time formatted as YYYY-MM-DD HH:MM:SS"; for `'now'` "Universal
Coordinated Time (UTC) is used"; two TEXT values are compared with a collating sequence, BINARY by default, which
"Compares string data using memcmp()". INTERPRETATION: the comparison is between IST text with a `T` separator and UTC
text with a space, which A03 has already recorded and classified (A03 AUDIT U-03, KNOWN DEFECT provisional; owner A03,
the meaning of the count A15's); recorded here as one more consumer-side form beside P11-S032; ID and classification
unchanged.

## 5. Points the AUDIT may examine (neutral)

These are pointers only; no issue is counted or judged here, and points owned by other topics are named for their
owners.
- The audit counts and the stored rows do not reconcile on several routes (batch 503, EOD 200, re-accept, failed audit
  write), while A15's daily trade review states an identity between them and calls out-of-window and backpressure
  refusals part of `SUM(signals_rejected)`; the dashboard labels `SUM(signals_accepted)` "validated" (P11-S003,
  P11-S050; P02-S067). Consumers are A15's.
- The EOD route reuses the answer key `accepted` for "symbols received", so EOD symbols enter the audit row's accepted
  count with no `signals` row (P11-S003).
- No column links a `signals` row to its request's `webhook_audit` row (P11-S030).
- `/metrics` carries no live queue depth, so A20's backpressure check cannot warn (P11-S025; P03-S046). A20 and A15
  own the readers; the A06 side is that the depth leaves the receiver only through `/health` and headers (P11-S004).
- The `FAILED` / `[func=DISABLED]` EOD heartbeat is not a registry job and is not reported by the Control Tower's cron
  check, against the comment that it makes the states distinguishable (P11-S018, P11-S019). A15 and A16 own the readers.
- `cron_heartbeat` rows are never deleted (P11-S037).
- Rows left `QUEUED`, `QUEUE_FULL`, `PASSED` or `RESERVED` are never reaped or deleted, and only `PROCESSING` rows of an
  earlier date are turned into `EXPIRED` (P11-S033, P11-S034; P05-S022). The cleanup is A12's; the retention question
  is A03's IC-21.
- `DUPLICATE` is filtered, classified and counted by other topics' code although no A06 writer stores it (P11-S016,
  P11-S034).
- The cleanup docstring says fingerprints older than 7 days are pruned; the committed window is 90 days (P11-S034).
- Consumers derive "the day" of a signal three ways (UTC by `DATE()`, IST by `substr`/`LIKE`), and the health server
  compares with the host's local date (P11-S032).
- Three forms of "expired" are stored or answered, and `expires_at` is computed from `received_at` while both checks use
  `triggered_at` (P11-S039; P04-S041).
- `signals_processed` means worker starts in `/metrics` and completed signals in the unused `stats()` (P11-S024).
- The rule that every retryable status releases both claims is kept by repeating the code at three sites (P11-S041).
- Six or more repeat controls with different keys can refuse the same symbol; the receiver's three are A06's
  (P11-S040; P03-S001). The committed `one_trade_per_symbol_direction_per_day: true` differs from the rule's "DEFAULT OFF"
  docstring (P11-S040; A09's).
- `/metrics` `signals_traded` counts a status no code writes (P11-S057; A15's reader).
- A schema migration rewrites `signals` and `webhook_audit` rows in bulk (P11-S058; A03's).
- The daily trade review compares a UTC-date `signals` count with an IST-date audit sum (P11-S050, P11-S032).
- The intraday and EOD routes parse the same Chartink body with separate code and different rules (P11-S045).
- The status vocabulary is listed in at least five places that differ from each other and from what the code writes
  (P11-S049).
- `signals.strategy` holds the scanner name; consumers grouping by it group by scanner (P11-S015; P01-S043).

## 6. UNKNOWN / NOT ESTABLISHED

P11-S051. UNKNOWN / NOT ESTABLISHED: every runtime fact for this part: whether any request arrived; whether any
`signals`, `webhook_audit` or `cron_heartbeat` row was written, updated or deleted; whether the end-of-day cleanup or
the retention script ran; whether any metric was read or any alert sent; whether any of the storage failures
of P11-S038 occurred (no production log, database or journal is admitted).

P11-S052. UNKNOWN / NOT ESTABLISHED: the installed SQLite and Python versions on the legacy machines (no pin) and the
hosts' time zones; the SQLite behaviour cited in P11-S032 is from the current documentation.

P11-S053. UNKNOWN / NOT ESTABLISHED: whether the heartbeat helper's relative path named the trading database in
production (working directory; A03 D-09; P03-S067).

P11-S054. UNKNOWN / NOT ESTABLISHED in this part (not traced; other owners): how the A16 cron tools
(`scripts/cron_officer.py`, `scripts/cron_watchdog.py`, `scripts/check_cron_drift.py`) and A15's generic heartbeat
readers treat the non-registry job `pb01_capture`; how A15's reports and dashboard present the count differences
of P11-S050; what A18's capture worker does with each `submit`.

P11-S055. UNKNOWN / NOT ESTABLISHED: whether Chartink reads the `X-Queue-*` headers or the answer body (P02-S072,
P03-S065).

P11-S056. UNKNOWN / NOT ESTABLISHED: the stored contents of any `signals`, `webhook_audit` or `cron_heartbeat` row,
including `webhook_payload` (no database was examined).

## 7. Draft questions about intent for Rama

Neutral questions about what was intended; no answer is proposed.
- Was `webhook_audit.signals_accepted` meant to equal the number of `signals` rows created, as the daily trade review's
  comment states, and were EOD symbols meant to count as "accepted" in `webhook_audit` (P11-S003, P11-S050)?
- Was the `pb01_capture` heartbeat meant to be watched by the cron monitoring (the registry, the Control Tower, the
  cron officer), or only read by a manual query (P11-S018, P11-S019)?
- Were `signals` rows left in `QUEUED`, `QUEUE_FULL`, `PASSED` or `RESERVED` meant to be closed or marked at some point,
  at the end of the day or at a restart (P11-S033, P11-S034)?
- Was the pre-flight backpressure check meant to read the real webhook queue depth, and from which source (P11-S025)?
- Was a link between a `signals` row and the HTTP request that produced it (its `webhook_audit` row) intended
  (P11-S030)?
- Which calendar date was meant to define "the signals of a day" in reports and monitors: the IST date of receipt, or
  another (P11-S032)?
- Was `cron_heartbeat` meant to have a retention window (P11-S037)?
- Was a `TRADED` status meant to be written to `signals`, as the schema, the classifier, `/metrics` and the prune comment
  assume (P11-S057)?

## 8. Where the direction's questions are answered

| Direction question (section 4) | Where answered in P11 | Also |
|---|---|---|
| 20 Signal event creation, persistence, fields written, failure and stop between steps (storage side) | P11-S012, P11-S029, P11-S030, P11-S031, P11-S033, P11-S034, P11-S038, P11-S058 | P05 sections 2 to 4 (main answer) |
| 23 A03 storage boundaries: `signals`, `webhook_audit`, EOD heartbeat; reads, writes, transactions, retention, errors | P11-S013, P11-S014, P11-S017, P11-S018, P11-S028 to P11-S038, P11-S058 | P03 section 6 (receiver side) |
| 27 Whole-topic audit: duplicates, consistency (duplication and consistency side only, recorded) | P11-S039 to P11-S050; P11-S003, P11-S015, P11-S016, P11-S024, P11-S025, P11-S057, P11-S059 | section 5 pointers |
| 21 Wiring of A06 components (producer-to-consumer side) | P11-S005 to P11-S008, P11-S010, P11-S020, P11-S023 | P01, P04 |
| 26 Intended-behaviour sources touched (HISTORICAL texts beside code facts) | P11-S019, P11-S033, P11-S034, P11-S035, P11-S041, P11-S050 | P10 section 9 |
| 28 Matches as well as issues; UNKNOWN items | matches: P11-S035 (A03 Z-26 MATCH), P11-S036 (A03 D-29 MATCH), P11-S041 (each retryable site releases both claims), P11-S048 (one shared success rule); UNKNOWN: P11-S051 to P11-S056 | |

Questions 1 to 19, 22, 24 and 25 are answered in parts P01 to P10; this part only cross-refers to them where noted.

## 9. Check log

Checked on 17-Nov-2026 by a separate read-only helper (brief the check rules). Every statement P11-S001 to P11-S056 was
re-read against its cited lines at `970aabf` (`git show`, filtered output), the cited project records under the project
repository and the cited external pages; the searches of section 1.2 were re-run (`signals` SQL, `update_signal_status(`,
`webhook_audit`, `cron_heartbeat`, `pb01_capture`, `DELETE FROM`, the store reader methods, `.stats()`,
`get_runtime_metrics`, the `X-Queue-*` headers, `expires_at`, `'TRADED'`). The pre-check draft is kept in the parts
drafts folder.

**Statements checked:** 56. **Correct as drafted:** 33. **Corrected:** 23. **Withdrawn:** 0. **Added:** 3 (P11-S057 to
P11-S059).

**Owner attributions (special point).** Every owner named in the part was compared with the Master System Investigation
Index (04-Nov-2026), topic entries and Appendix A. All match: `scripts/eod_cleanup.py` A12; `scripts/db_retention.py`,
`scripts/backup_restore_drill.py`, `scripts/backup_evidence.py` A03; `scripts/healthcheck_server.py`,
`scripts/system_manager.py`, `scripts/check_vm_state.py`, `scripts/trade_journal.py`, `scripts/gemini_trade_coach.py`,
`scripts/generate_screened_stocks_csv.py` A15; `scripts/cron_officer.py`, `scripts/cron_watchdog.py`,
`scripts/check_cron_drift.py` A16 (and, by the A16 entry, `utils/cron_heartbeat.py`, `config/cron_registry.yaml`,
`deploy/cron/trading-system.cron`); `scripts/t2_cnc_gtt_realtest.py`, `scripts/replay_signals.py`,
`scripts/load_test_signals.py` A19; `scripts/fetch_daily_candles.py` A05; `scripts/strategy_registry_officer.py` A07;
`scripts/forward_shadow_record.py` A18; `scripts/preflight/` A20; `reports/`, `ops/`, `ops_dashboard/`,
`core/evidence_contract.py`, `core/effect_telemetry.py` A15; `orders/order_manager.py` A10; `screening/` A07 except
`screening/retest_monitor.py` A08; `sr_detector/` (the zone warmer) A08; `v3_chain/` and `allocation/` A18; `capital/`
A09; `core/time_authority.py` A01; `core/state_store.py`, `core/schema.sql`, `core/migrations.py` A03. No script is
attributed to A03 that the index gives to another topic. One owner is a judgement, kept and now stated: the
one-trade-per-symbol-and-direction rule sits in `signals/signal_processor.py` but is recorded as A09's admission side
under Rama's decision A (as P08 does).

**Special points re-verified.** Count mismatches (P11-S003, P11-S050): the five producer-side cases hold at the cited
lines; added the 500 case, the EOD watchlist-disabled `accepted: 0`, the UTC/IST date-basis difference of the report, and
weakened "agree only on days when ..." (differences can offset). `/metrics` zero values (P11-S004, P11-S025):
confirmed (`queue_depth`/`queue_capacity` initialised 0 at L153 to L154, never set; neither `get_runtime_metrics` nor
`EntryThrottle.metrics()` returns a queue key); added the skipped case. `pb01_capture` heartbeat readers (P11-S018,
P11-S019, P11-S037): confirmed; added A03's restore drill as a table-list reader; the Control Tower's expected list comes
from the registry. Row clean-up and prune (P11-S016, P11-S033, P11-S034): confirmed; defaults and override paths added.
Date derivations (P11-S030, P11-S032): confirmed against the SQLite page (re-opened); Python `isoformat()` and
`date.today()` now cited from docs.python.org; A03's prior records (STUDY 14.1 point 21, AUDIT H-11, U-03) credited.

| ID | What changed | Why |
|---|---|---|
| Header | Status line changed | the check rules step 4 |
| 1.4 | external pages added | pages read in the check |
| P11-S003 | EOD disabled branch (`accepted: 0`, L788) added; consumer cross-reference P11-S019 -> P11-S050 | imprecise; wrong cross-reference |
| P11-S004 | threshold is `int(capacity * warning_pct)` (L574); config value cited | imprecise |
| P11-S007 | warmer built at L3549 to L3568 (not L3564), flags L3423, L3427; "before any worker starts" -> "before the item is submitted to a worker" | wrong line range; imprecise wording |
| P11-S017 | 90 days is a default; `--set` override; declared commands pass none | fact incomplete |
| P11-S018 | "produces one row" -> code calls `record_heartbeat` once (row only if file exists and no exception); restore-drill reader added; runtime UNKNOWN | runtime-sounding wording; completeness |
| P11-S019 | lines L105 to L135; expected list from the registry | imprecise lines |
| P11-S021 | the EOD heartbeat row is also a per-request durable record | fact incomplete |
| P11-S024 | "worker starts" -> entries whose `PROCESSING` write returned | imprecise |
| P11-S025 | check skipped when `/metrics` is not 200; throttle metrics carry no queue key | imprecise |
| P11-S027 | recorder location, file names, builder lines and A03 backup reader cited | unsupported location; completeness |
| P11-S028 | `transaction()` lines L505 to L543 added | cited range did not cover `transaction()` |
| P11-S029 | `ts` not stored: A03 P-02 cited | prior record |
| P11-S031 | answers outside `_handle_webhook` write no audit row (P02-S071); "leave" -> "lead to an audit-row write" | completeness; runtime-sounding wording |
| P11-S032 | `isoformat()` and `date.today()` behaviour cited from docs.python.org (INTERPRETATION); L903 marked as uncalled; A03 prior records credited | external fact without source; inherited records |
| P11-S034 | config-loader line L1976; defaults and override lines; INTERPRETATION basis and "while they keep that status" | imprecise lines; overstated |
| P11-S035 | 90 days is a default | as P11-S017 |
| P11-S039 | `expires_at` read "by name" only by `db_reader.py` L826 | `SELECT *` readers also receive it |
| P11-S040 | committed `true` (L302) and model default `False` (L784) beside the "DEFAULT OFF" docstring; further symbol checks (A09, A18, shadow guard); "up to six" -> "six or more"; lines | fact missing; overstated count |
| P11-S045 | EOD route never compares `scan_name` with the path | fact missing |
| P11-S046 | EOD route also skips the backpressure test | fact missing |
| P11-S048 | re-checked lines for the Appendix A script, `utils/startup_checks.py` and the A20 search added | cited re-check covered only A20 lines |
| P11-S049 | column-comment omissions listed fully; `TRADED` noted | incomplete |
| P11-S050 | 500 case; EOD disabled branch; INTERPRETATION weakened (offsets possible); report's UTC/IST date-basis difference added | overstated; completeness |
| 5 | bullets updated and added for P11-S040, P11-S050, P11-S057, P11-S058 | follow the corrections |
| 7 | question on `TRADED` added | follows P11-S057 |
| 8 | P11-S057 to P11-S059 mapped to questions 20, 23 and 27 | completeness |

**Statements added.** P11-S057 (`/metrics` `signals_traded` counts a status no code writes); P11-S058 (A03's migration
runner rewrites `signals` and `webhook_audit` rows in bulk; interface only); P11-S059 (`check_vm_state.py` text
comparison with SQLite UTC time; pointer to A03 AUDIT U-03, ID and classification unchanged).

**Not verified, and why.** Cross-references to sibling parts were spot-checked only (P02-S067, P02-S070, P02-S071,
P03-S001, P03-S046, P04-S041, P04-S042, P05-S022 re-read); the others are taken from parts that their own checkers
verified. A03 record IDs cited (D-08, D-09, D-13, D-29, P-02, P-11, P-12, R-08, R-38, R-39, U-08, U-47, Z-26, IC-21,
P09b-S019, S027, S061, S062, S066, S099) were confirmed to exist and match in substance, but not all were re-read in full.
The `/metrics` dashboard counterpart (P03-S046) and the waitress/Flask outside-view answers (P02-S071) rely on those
parts' external sources. No legacy file was run, imported or executed; no endpoint or external service other than the
three documentation pages was contacted.

- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P11-S040: "After the handoff" -> "After the screening call" (the handoff line is OPEN FOR RAMA, P05-S031).
- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P11-S040: the shadow-inning guard is no longer placed after the handoff: it runs at `SP` L928, before the screening call at L998 (P05-S030).
