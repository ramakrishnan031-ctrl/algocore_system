# A06 evidence: receiver deduplication, throttling, in-flight control, queueing and audit

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P03, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude.
**Purpose and scope:** duplicate detection, throttling, in-flight control, the queue put and its threshold, the receiver's writes to `webhook_audit`, `signals` (at the storage boundary) and the EOD heartbeat store, and request concurrency in `signals/webhook_receiver.py` (written `970aabf` below), with the `main.py` wiring, the processor's release calls and the other readers of the same thresholds recorded at the interface only. Direction questions 10, 11 (receiver side), 12, 13, 14 (receiver side), 16 (put side) and 23 (receiver writes). The request flow, routes, server, sweeper and shutdown are P01's; authentication, validation and the response table are P02's; the processor's intake, workers and expiry are P04's; event creation and the handoff map are P05's; the entry throttle is P06's; storage implementation is A03's. This part cites their statement IDs instead of repeating them (STUDY part P03).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)
In whole or in the ranges given; every printed line passed through the identifier filter of the security rule (D-07).
- `signals/webhook_receiver.py`: L1 to L110 (module docstring, imports, `_RETRYABLE_STATUSES`, `_PerIpRateLimiter`),
  L200 to L252 (constructor state: in-flight, sweeper, dedup cache, limiter, Flask app), L360 to L404 (`/health`),
  L477 to L580 (`_handle_webhook`, the start of `_process_request` to the backpressure check), L676 to L750 (per-symbol
  loop, batch answer), L751 to L834 (`_handle_eod`, `_record_eod_heartbeat`), L892 to L1207 (`_process_signal`,
  in-flight methods, `_write_audit`, `set_eod_capture`, `stop`, `_run_sweeper`). The other lines are covered by P01
  and P02 and were consulted through their statements.
- `main.py`: L1658 to L1692 (census and receiver stop), L3398 to L3416 (queue and receiver construction), L3570 to
  L3640 (processor construction: the release callback, no `rate_limiter` argument), L4070 to L4080 (health-check server
  start with the processor's metrics provider).
- `signals/signal_processor.py` (interface only; P04 and P05 own it): L1 to L60 (docstring SP and SPW lines), L140 to
  L260 (constructor parameters and state named in the greps), L300 to L345 (`start`, `stop`), L377 to L470
  (dispatcher loop, `_process_one_safe` and its re-queue route), L660 to L738 (heartbeat helper, runtime metrics),
  L1238 to L1275 and L1686 to L1738 (the release calls), L1500 to L1530 (the transient-error re-queue), L2660 to
  L2703 (`stats`).
- `core/state_store.py` (A03's file; boundary only): L105 to L118 (connection pragmas), L200 to L250 (per-thread
  connection), L500 to L600 (`transaction`, `execute`, `fetch_one`, `fetch_all`).
- `core/schema.sql` (A03's file; boundary only): L34 to L100 (`signals` and its indexes), L574 to L603
  (`webhook_audit` and its indexes).
- `utils/cron_heartbeat.py` (A16's helper; A03's open cost; boundary only): L20 to L110.
- `core/effect_telemetry.py` (A01's census; interface only): L240 to L275, and the grep hits L222, L259, L261.
- `config/system_config.yaml` L120 to L131, L322 to L356; `core/config_loader.py` L190 to L198, L615 to L645 (A02's
  files and schemas; read at the boundary only).
- `ops_dashboard/backend/services/capacity.py` L160 to L185, L278 to L292,
  `ops_dashboard/backend/readers/metrics_client.py` L1 to L60 and `ops_dashboard/backend/readers/db_reader.py` L1030 to
  L1040 (A15; interface only).
- `requirements.txt` L1 to L15 (pins).
- `core/state_store.py` grep hit L3305 (`insert_cron_heartbeat`) and `core/schema.sql` grep hit L1019 (`cron_heartbeat`)
  (A03; existence only).
- `scripts/preflight/checks/signals.py` L1 to L20, L60 to L85; `scripts/preflight/checks/engine.py` grep hits L30,
  L70 (A20; interface only).
- `scripts/healthcheck_server.py` L1 to L30, L60 to L160, L236 to L262 (A15 and A01; interface only).
- `signals/entry_throttle.py` grep hits L59, L117 to L124 (P06's; only to confirm which metric keys it adds).
- Tests (HISTORICAL; never run): `tests/unit/test_c2_webhook_lockdown.py` L20 to L62;
  `tests/integration/test_hardening_scenarios.py` L236 to L262; and the test names found by the grep in section 1.3.

### 1.2 Project records read (algocore_system, branch main, read-only)
- `TOPIC_COMPLETION_REGISTER_2026-11-04.md`, A06 entry (scope, boundaries A to E, the 52 inherited items).
- A02: `A02_RECONCILED_TOPIC_RECORD_2026-11-09.md` section 15.2; `A02_AUDIT_2026-11-08.md` entries K-11, K-12, K-13
  and rows K-38, K-50 and the handoff rows for T-02, T-07, T-12, T-14, F-11, K-02, K-04, K-05, K-09, K-12, K-13,
  K-22, K-49, X-01; `evidence/A02_KEY_CONSUMER_MAP_PART1_2026-11-06.md` rows for `signal_queue.*` and `webhook.*`;
  `evidence/A02_CONFIG_LOADER_SCHEMA_AND_FLOW_2026-11-06.md` rows for `SignalQueueConfig` and `WebhookConfig`.
- A03: `A03_RECONCILED_TOPIC_RECORD_2026-11-11.md` (handoff table, A06 row); `A03_AUDIT_2026-11-10.md` entries D-08,
  P-02, P-11, P-12, Q-11, R-08 and row R-39; `A03_STUDY_2026-11-09.md` rows on `webhook_audit`;
  `evidence/A03_SQL_OUTSIDE_STORE_RUNTIME_2026-11-09.md` rows P06a-S022, P06a-S035;
  `evidence/A03_TRADING_SCHEMA_PART1_2026-11-09.md` rows P02a-S033, P02a-S197.
- A01: `A01_RECONCILED_TOPIC_RECORD_2026-11-06.md` section 15 (A06 row); `A01_AUDIT_2026-11-05.md` rows C13, C14, C18,
  C20, C32, S-44, B-07, M-13, M-19 (to confirm which bear on this part).
- The A06 investigation direction of 17-Nov-2026 (questions 1 to 28) and the A06 first fieldwork checkpoint of
  17-Nov-2026, as working inputs only.
- The checked parts `A06_P01_RECEIVER_INGRESS_AND_LIFECYCLE.md` and `A06_P02_RECEIVER_AUTH_AND_VALIDATION.md`
  (working drafts), for cross-references only.

### 1.3 Commands and search patterns (all read-only)
- `git -C <legacy clone> show 970aabf:<path>` for every file above, filtered; `git status --short` empty.
- `git ... grep -n -E` at `970aabf` with the four mandatory exclusion pathspecs, or the helper `the search wrapper`, patterns:
  `backpressure_pct|warning_pct|signal_queue\.capacity|queue_capacity|queue_depth|dedup_window_seconds|per_ip_`;
  `QUEUE_FULL|status *= *'QUEUED'|"QUEUED"`; `runtime_metrics|_runtime_fn|metrics_fn|healthcheck_server`;
  `METRICS_URL|queue_|qsize` in the pre-flight engine and the health-check server;
  `in_flight|_release_fn|release_in_flight|signal_queue|\.get\(timeout|get_nowait|task_done|_queue\b` and
  `ThreadPoolExecutor|_executor =|max_workers|rate_limiter` in `signals/signal_processor.py`; `rate_limiter` in
  `main.py`; `limit|throttl|cooldown|sleep|semaphore|Lock\(|RLock|Event\(` in the receiver;
  `def transaction|def fetch_one|threading.local|isolation_level|busy_timeout|_CONNECTION_PRAGMAS` in
  `core/state_store.py`; `webhook_day_count|webhook_receiver|webhook_audit` in `core/effect_telemetry.py`;
  `\.shutdown\(` (non-test code, filtered for queue names); `webhook_audit` in the receiver;
  `def insert_cron_heartbeat` and `CREATE TABLE IF NOT EXISTS cron_heartbeat`; test names
  matching `def test_[a-z0-9_]*(dedup|duplicate|rate_limit|limiter|in_flight|inflight|queue_full|requeue|retry|store_error|backpressure|sweeper|bucket|audit)`.
- `git ... blame --line-porcelain -L <range>` on receiver ranges, with only the commit hash and author date extracted;
  `git ... log -1 --format='%h %ad %s' --date=short` for the commits found (subjects only).
- A one-line check that L954 calls the standard-library SHA-256 digest (`grep -c`; the line itself was not printed
  unfiltered).
- No legacy file was imported, executed, built or tested; no endpoint, URL, scanner or broker was contacted; no
  credential, account, overlay or token file was opened.

### 1.4 External pages read (current external context, read 17-Nov-2026)
- Python `queue` (page for Python 3.15.2): https://docs.python.org/3/library/queue.html
- Python Language Reference, "The try statement" (3.15.2): https://docs.python.org/3/reference/compound_stmts.html
- Python Tutorial, "Errors and Exceptions" (3.15.2): https://docs.python.org/3/tutorial/errors.html
- Python `time.monotonic` (3.15.2): https://docs.python.org/3/library/time.html
- Python `datetime.timestamp` (3.15.2): https://docs.python.org/3/library/datetime.html
- Python `sqlite3` exceptions, `connect` timeout and `check_same_thread` (3.15.2):
  https://docs.python.org/3/library/sqlite3.html
- CPython 3.12 published source, `Lib/concurrent/futures/thread.py`:
  https://raw.githubusercontent.com/python/cpython/3.12/Lib/concurrent/futures/thread.py
- CPython 3.12 published source, `Modules/_sqlite/util.c` (result-code to exception mapping):
  https://raw.githubusercontent.com/python/cpython/3.12/Modules/_sqlite/util.c
- SQLite "Result and Error Codes": https://www.sqlite.org/rescode.html
- cachetools documentation (the stable page describes 8.0.0): https://cachetools.readthedocs.io/en/stable/
- cachetools 7.1.1 published source (the pinned version), `src/cachetools/__init__.py`:
  https://raw.githubusercontent.com/tkem/cachetools/v7.1.1/src/cachetools/__init__.py
- Not retrievable (not used): the cachetools documentation page for v7.1.1 (https://cachetools.readthedocs.io/en/v7.1.1/,
  site error); the tagged 7.1.1 source above was used instead.
- waitress and Flask behaviour is taken from P01 section 7 (P01-S067, P01-S068, P01-S075, P01-S086) and P02-S074; no
  waitress or Flask page was re-read for this part.

### 1.5 Labels and limits
- Labels follow the sourcing and labelling rules. Every runtime fact (that a request arrived, a claim was taken, a row was
  written, a limit was reached) is UNKNOWN / NOT ESTABLISHED: no production log, database or journal is admitted.
- The installed versions of Python and cachetools on the legacy machines are UNKNOWN / NOT ESTABLISHED;
  `requirements.txt` pins `cachetools==7.1.1` (L11, P01-S085) and does not pin Python. Python behaviour is cited from
  the current documentation (3.15.2) and the CPython 3.12 source; where a statement depends on the version this is
  said.
- Repository configuration values are the file values only; effective values are UNKNOWN / NOT ESTABLISHED (P01-S110).
- Security: no identifier, address, path or secret value is reproduced. The webhook secret is not involved in this part.

### 1.6 Read in the check (separate helper, 17-Nov-2026)
- Every statement was re-read against its cited lines at `970aabf` (filtered `git show`), its project record or its
  external page. Further legacy sources read: `signals/webhook_receiver.py` in whole except L260 to L339 (alias
  loading and authentication, P01's and P02's); `config/expected_managers.yaml` L147 to L155 (grep `webhook_receiver`);
  `ops_dashboard/backend/config/gui_config.yaml` L42 to L43 and `ops_dashboard/backend/readers/metrics_client.py` L1 to
  L79; `ops_dashboard/backend/services/live_activity.py` L440 to L462 (to exclude a grep hit: it concerns alerts, not
  signals); `signals/signal_processor.py` L274 to L279, L667 to L681, L867, L1646, L1706; `main.py` L1599 to L1662 (for
  the order of the census and the receiver stop) and L4225 to L4256; `git log -S` for `TTLCache(` and
  `_PerIpRateLimiter`, `git log -1` for `84cee3e`, and `git blame` (hashes only) of L233 to L238, L952, L992 to L1001,
  L1029 to L1031, L1065 to L1066, L79 to L100 and L376 to L380.
- Project records read in the check: A01 AUDIT section 1.6 (the KNOWN DEFECT rule) and the rows of the A01 handoffs;
  A02 AUDIT K-11, K-12, T-07, rows K-38, K-50 and the L-12 detail; A02 STUDY section 4.3; A03 AUDIT D-08, D-09, P-12,
  R-08, rows R-39 and Z-26; A03 evidence rows P06a-S022, P06a-S035 and the P06b rows cited in P03-S054; the A06 entry of
  the Topic Completion Register (the 52 inherited items).
- External pages read in the check (current external context, read 17-Nov-2026): waitress "Design", page for 3.0.2,
  https://docs.pylonsproject.org/projects/waitress/en/stable/design.html; waitress 3.0.2 tagged source,
  https://raw.githubusercontent.com/Pylons/waitress/v3.0.2/src/waitress/task.py, `.../server.py` and `.../channel.py`
  (same tag and folder); Werkzeug "Request / Response Objects", page for 3.1.x,
  https://werkzeug.palletsprojects.com/en/stable/wrappers/; Werkzeug published source,
  https://raw.githubusercontent.com/pallets/werkzeug/main/src/werkzeug/wrappers/request.py; Python `json` (3.15.2),
  https://docs.python.org/3/library/json.html; Python `codecs` (3.15.2), https://docs.python.org/3/library/codecs.html.
  Every page of section 1.4 was re-opened and its quotation confirmed, except the cachetools 7.1.1 documentation page
  (not used).

## 2. Duplicate detection (direction question 10)

### 2.1 The three layers, their keys and their window

P03-S001. FACT (`signals/webhook_receiver.py` L904 to L1015; `core/schema.sql` L82 to L83): after the symbol, price and
expiry checks (P02-S061, P02-S058), `_process_signal` applies three layers that can refuse a signal as already present,
in this order:

| Layer | Lines | Key | Window | State and persistence | Lock | Refusal status | Row written |
|---|---|---|---|---|---|---|---|
| 1 in-flight claim | L934, L1074 to L1091 | symbol only | until released, or evicted by the sweeper (section 4) | dict in memory | `_in_flight_lock` | `IN_PROCESS` | none |
| 2 TTL cache | L940 to L947 | `(symbol, scanner_name)` | `_dedup_window_seconds` from the moment the key is stored | `TTLCache` in memory | `_dedup_lock` | `DUPLICATE` | none |
| 3 stored fingerprint | L949 to L1015 | SHA-256 of the scanner name, the symbol and the slot number (P03-S007), with `fingerprint_date` | a fixed slot of `_dedup_window_seconds` on `triggered_at`, per receipt date | unique index on `signals(fingerprint, fingerprint_date)` in the database | the database's write lock | `DUPLICATE`, or the re-queue route | none (the INSERT is refused) |

Layer 1 is a concurrency control (section 4) but it also refuses a second signal, so it is listed here.

P03-S002. FACT (L670, L701, L719 to L723, L940, L953; P01-S035, P01-S039): the keys use the symbol after the alias lookup
(on a hit the upper-cased mapped value; on a miss the `stocks` element as split and stripped of surrounding white space
at L670, its case unchanged) and the scanner name exactly as it
appears in the path, which has already been checked to be a key of `scan_webhook_map` (an exact, case-sensitive
dictionary test). No layer upper-cases, strips or otherwise normalises either value. INTERPRETATION: a symbol sent once
in upper case and once in lower case (alias miss) gives different keys in all three layers.

P03-S003. FACT (L232 to L238, L952; `config/system_config.yaml` L337; `core/config_loader.py` L622): the window is
`int(dedup_window_seconds)` read from the resolved webhook settings (P01-S011), 300 if the attribute is absent or the
conversion raises `TypeError` or `ValueError`, then floored at 60 (`max(60, ...)`). The same value is the cache's TTL
(L237) and the slot width of the fingerprint (L952). The repository file sets 300; the schema default is 300 with no
bound. A02 K-12 recorded the floor (owners A02 and A06; ID and classification kept); the A06 side is that the floor
governs both layers at once.

### 2.2 Layer 2: the TTL cache

P03-S004. FACT (L237 to L238, L940 to L947): the cache is `TTLCache(maxsize=10000, ttl=<window>)` with its own
`threading.Lock`. Under that lock the receiver tests `dedup_key in self._dedup_cache`; on a hit it releases the
in-flight claim and returns `DUPLICATE`; on a miss it stores `True` under the key. The test and the store happen in one
lock acquisition, so among the receiver's threads they are atomic. A cache `DUPLICATE` writes no `signals` row and puts
nothing on the queue (P02-S070).

P03-S005. Current external context (read 17-Nov-2026; cachetools 7.1.1 tagged source `src/cachetools/__init__.py`;
cachetools documentation, stable page for 8.0.0) and INTERPRETATION. The source: `TTLCache` is an "LRU Cache
implementation with per-item time-to-live (TTL) value"; its default timer is `time.monotonic`; `__setitem__` first
removes expired items and then stores the key with `expires = time + ttl`; `__contains__` returns
`self.timer() < link.expires` without reordering or removing anything; when room is needed, `popitem` removes expired
items and then the least recently used live key. The documentation: the cache classes "are *not* thread-safe. Access to
a shared cache from multiple threads must be properly synchronized"; with the default timer "time.monotonic() is used".
INTERPRETATION for the legacy code: (a) the window runs from the moment the key was stored, on the receiver's
monotonic clock, not from `triggered_at`; (b) a hit does not extend the window, because the `in` test only reads, so the
window is fixed from the first stored signal of the pair and does not slide with repeated duplicates; (c) the key is
stored again only once it is absent or expired; (d) the receiver's own lock gives the synchronisation the documentation
requires; (e) the window is not affected by wall-clock changes (Python `time.monotonic`: "a clock that cannot go
backwards. The clock is not affected by system clock updates", read 17-Nov-2026); (f) because keys are only stored
and tested with `in`, the key evicted when more than 10,000 live keys exist is the oldest stored one; such an early
eviction would let a duplicate of that pair pass layer 2 (layer 3 still applies within the same slot). Whether that
volume ever occurred is UNKNOWN / NOT ESTABLISHED. The installed cachetools version is UNKNOWN; the pin is 7.1.1
(`requirements.txt` L11).

P03-S006. FACT (L998 to L999, L1029 to L1030, L1065 to L1066): the cache key is removed again only on three routes:
`QUEUE_FULL` on the re-queue route, `STORE_ERROR`, and `QUEUE_FULL` on the first route. It stays on `ACCEPTED` (both
routes, L1012, L1072), on the stored-fingerprint `DUPLICATE` (L1014 to L1015) and on any exception that leaves
`_process_signal` (P03-S034). HISTORICAL (L59 to L66, comment of 17-Jul-2026): "Every status listed here MUST have
released both the in-flight claim and the fast-path dedup claim before returning"; for the two statuses listed,
`QUEUE_FULL` and `STORE_ERROR`, the code releases both (an observation for the AUDIT, not a judgement).
INTERPRETATION (L947 before L963): the key is stored before the INSERT is tried, so an alert that layer 3 then refuses
(stored-fingerprint `DUPLICATE`) leaves a freshly stored key behind and starts a new window from its own receipt; a
further alert of the pair in a later slot within that new window is then refused by layer 2. A retry accepted on the
re-queue route likewise starts a new window.

### 2.3 Layer 3: the stored fingerprint

P03-S007. FACT (L949 to L954): after layers 1 and 2 pass, the receiver computes
`epoch_bucket = int(triggered_at.timestamp() // self._dedup_window_seconds)`, the text
`f"{scanner_name}|{symbol}|{epoch_bucket}"`, and its SHA-256 hexadecimal digest with the standard-library `hashlib`
(L954; WR7, L18, says "SHA-256 fingerprint").

P03-S008. FACT (L677 to L678, L957 to L980; `core/schema.sql` L74 to L75, L81 to L83): the `signals` INSERT writes the
fingerprint and `fingerprint_date = today_iso`, the IST date of `received_at`. The unique index
`idx_signals_fingerprint_today` on `(fingerprint, fingerprint_date)` refuses a second row with the same pair. The
schema comment on `fingerprint_date` ("YYYY-MM-DD of received_at") matches the code. INTERPRETATION: the slot is taken
from the trigger time, the date from the receipt time; this layer is held in the database and survives a restart.

P03-S009. Current external context (read 17-Nov-2026; Python `datetime.timestamp`: for aware instances "the return
value is computed as: (dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()") and INTERPRETATION:
`triggered_at` is always IST-aware when it reaches L952 (P02-S055, P02-S056), so a slot is a fixed run of `window`
seconds counted from the UTC epoch. The IST offset of 19,800 seconds is a whole multiple of 300 (66 times), so at the
file value the slot edges fall on IST clock times ending in :00 and :05 (for example 09:15:00 and 09:20:00 IST). A
window that does not divide 19,800 (for example 420 seconds, which the schema accepts) would put the edges at other
clock times. The two time-only `triggered_at` formats carry no seconds (P02-S055), so such values always sit at a whole
minute.

P03-S010. FACT (L981 to L991; `core/state_store.py` L524 to L541, L564 to L574, L232 to L237) and current external
context (read 17-Nov-2026; SQLite "Result and Error Codes": SQLITE_CONSTRAINT_UNIQUE "is an extended error code for
SQLITE_CONSTRAINT indicating that a UNIQUE constraint failed"; CPython 3.12 `Modules/_sqlite/util.c`:
`case SQLITE_CONSTRAINT:` returns `IntegrityError`): a second INSERT with the same pair raises
`sqlite3.IntegrityError`; `transaction()` rolls back and re-raises the original exception, so the handler at L981
receives it. The handler then reads `signal_id` and `status` of the existing row with `fetch_one` (a plain read on the
thread's connection, which runs with `isolation_level=None`, outside any transaction). If that row's status is
`QUEUE_FULL` the re-queue route follows (P03-S012); otherwise, including when no row is found, the receiver releases the
in-flight claim and returns `DUPLICATE`; the cache key stored at L947 is kept.

P03-S011. INTERPRETATION (L981, L987 to L992; `core/schema.sql` L42 to L70): every `IntegrityError` from this INSERT is
handled as a fingerprint conflict. A violation of another constraint (the status CHECK, a NOT NULL column, the primary
key) would reach the same handler and, with no row carrying the fingerprint, be answered `DUPLICATE`. At the baseline
the INSERT writes the status `'QUEUED'` (in the CHECK list, L60 to L65), a non-empty symbol (L905) and a new identifier
from `core.ids.new_signal_id` (not examined here), so the other constraints are not expected to fail. Recorded as a
code fact for the AUDIT.

P03-S012. FACT (L992 to L1013): the re-queue route builds
`(existing["signal_id"], scanner_name, symbol, price, triggered_at)`, where `price` and `triggered_at` are those of the
current request, and calls `put_nowait`. On `queue.Full` it removes the cache key, releases the claim and returns
`QUEUE_FULL`. Otherwise it runs `UPDATE signals SET status = 'QUEUED' WHERE signal_id = ?` in its own transaction (no
status condition), logs any failure at ERROR, and returns `ACCEPTED` with the existing id. A03 R-08 recorded the push
before the flip and the unconditional flip (owners A06 and A03; ID and classification kept). INTERPRETATION (A06
side): the route cannot tell a sender's retry from a new alert for the same scanner and symbol in the same slot and on
the same day. In both cases the queue item carries the current request's price and trigger time under the earlier
signal id, while the stored row keeps the first request's `trigger_price`, `triggered_at`, `received_at`, `expires_at`
and `webhook_payload` (only `status` is updated, L1005). On this route the queue item and the stored row can therefore
differ in price and trigger time.

### 2.4 Window edges and how the layers combine

P03-S013. INTERPRETATION (P03-S001 to P03-S012), for two alerts of the same scanner and symbol on one day:

| Case | Layer 1 | Layer 2 | Layer 3 | Outcome for the second alert |
|---|---|---|---|---|
| received while the first claim is held | refuses | not reached | not reached | `IN_PROCESS`, no row |
| received after the claim ends, within the window from the first store | passes | refuses | not reached | `DUPLICATE`, no row |
| triggers on either side of a slot edge (for example 09:19 and 09:20), received within the window | passes | refuses | would pass | `DUPLICATE`; but if layer 2 is empty (restart, key removed after `QUEUE_FULL` or `STORE_ERROR`) the second is accepted |
| same slot, received after the window has ended (for example a delayed delivery) | passes | passes | refuses | `DUPLICATE`, or the re-queue route if the first row is `QUEUE_FULL` |
| different slots, received after the window has ended | passes | passes | passes | accepted as a new signal |
| same slot, different receipt dates | passes | passes or refuses | passes | layer 3 does not apply across dates |

So within a day a pair is refused for at least one window after the key was last stored, unless the key was removed
again on `QUEUE_FULL` or `STORE_ERROR` (layer 2, receipt clock; the key is stored again by an alert that layer 3
refuses, P03-S006), and in addition any alert whose trigger falls in the
slot of a stored row of the same receipt date is refused (layer 3, trigger clock). The two layers share a width but not
a start.

P03-S014. FACT (L934, L940, L953; L66): layers 2 and 3 include the scanner name and never treat two scanners as
duplicates; only layer 1, keyed on the symbol alone, refuses a second scanner's signal for a symbol whose claim is held.
That refusal is `IN_PROCESS`: no `signals` row, counted as rejected, and the batch answers 200 because `IN_PROCESS` is not
in `_RETRYABLE_STATUSES` (L730 to L734; 503 only if another symbol of the same batch is `QUEUE_FULL` or `STORE_ERROR`). INTERPRETATION: a signal from another scanner that arrives while the claim is held (up to about
two minutes, P03-S032) is dropped without a stored row, and the sender is told 200, so no retry is invited.

### 2.5 Retries wrongly accepted or rejected

P03-S015. INTERPRETATION (P03-S004 to P03-S014; P01-S033; P02-S067, P02-S070, P02-S072), for a sender that re-sends the
same body (whether Chartink retries at all is UNKNOWN / NOT ESTABLISHED, P02-S072):

| # | First answer | What the retry meets | Retry outcome |
|---|---|---|---|
| R1 | 503 batch with `QUEUE_FULL` | claims released; row `QUEUE_FULL` | below the request threshold (section 5): re-queue route, `ACCEPTED` with the old id; at or above it: request-level 503, row unchanged until a later retry; no retry at all: the row stays `QUEUE_FULL` and the signal is not processed (P03-S040) |
| R2 | 503 batch with `STORE_ERROR` | claims released; no row | inserted afresh, `ACCEPTED` |
| R3 | 503 batch: symbols that were `ACCEPTED` | claim still held, or cache key, or stored row | `IN_PROCESS` or `DUPLICATE`; not queued again (counted as rejected in the retry's answer) |
| R4 | 500 after an exception inside `_process_signal` | symbols before the failing one keep their effects; the failing one may keep both claims (P03-S034); symbols after it are untouched | earlier symbols `IN_PROCESS` or `DUPLICATE`; the failing symbol refused until its claims lapse; later symbols processed normally |
| R5 | 200 lost in transit, or a sender-side timeout | claim, cache key or stored row | `IN_PROCESS` or `DUPLICATE` |
| R6 | any, with the retry more than `expiry_sec` (600 in the file) after the trigger | the age check before any claim (L919 to L926) | `EXPIRED`, no row; in case R1 the `QUEUE_FULL` row is then never re-queued |
| R7 | `ACCEPTED`, then a process restart before the item was processed | layers 1 and 2 empty; stored row `QUEUED` | `DUPLICATE`: the queue item was lost with the process, and the retry is refused (whether any boot recovery re-reads such rows is P04's; the search of P03-S040 found none) |

### 2.6 Restart effect

P03-S016. FACT (L206 to L208, L237 to L245; `main.py` L3402 to L3404): the in-flight dict, the TTL cache, the limiter's
buckets and the queue are in-memory objects created at construction; no code saves or reloads them. The fingerprint
rows persist in the database. INTERPRETATION: after a restart on the same day, a new alert for a pair that was accepted
before the restart is refused only if its trigger falls in the same slot (layer 3); an alert in a later slot is
accepted even if it arrives within the window of the earlier one.

### 2.7 Records and history

P03-S017. HISTORICAL (L18; L229 to L231; L937 to L939; `core/schema.sql` L74, L81; `config/system_config.yaml` L337;
commit subjects): WR7 says "SHA-256 fingerprint dedup at minute precision"; the schema comments say
"hash(scanner+symbol+trigger_minute)" and "same scanner + same symbol + same minute on same day = duplicate"; the
FIX-036 comment says the TTL cache "replaces minute-string fingerprint" and checks "within last 300 seconds"; the file
comment says "5-min fingerprint bucket (was 60s/1-min)". `git blame`: the cache came with `5dc8563` (14-May-2026,
"FIX-024 through FIX-038 production hardening batch"), the configurable window and slot with `8e884db` (30-May-2026,
"FIX-131: P1 batch4 -- dedup window ..."), the re-queue route and the cache roll-back on `QUEUE_FULL` with `735a6c3`
(14-Jul-2026, "QUEUE_FULL no longer poisons dedup -> backpressure recovery works"), and the roll-back on store failure
with `a9a686e` (17-Jul-2026, "P3-s14 -- release both claims on a store failure and answer retryably").
INTERPRETATION: the minute-precision texts are older than FIX-131 and no longer describe the code; the cache did not
replace the fingerprint, since both are in the code.

P03-S018. HISTORICAL (tests, never run): `tests/integration/test_hardening_scenarios.py` L236 to L262 states the
expectation that a `QUEUE_FULL` signal, after the queue drains, is accepted on retry "reusing its signal_id";
`tests/integration/test_end_to_end_smoke.py` L326 is named `test_dedup_second_signal_rejected`;
`tests/unit/test_e4_event_loop_safety.py` L380 is named
`test_m1_claim_in_flight_atomic_under_concurrent_same_symbol`. Stated expectations only.

## 3. Throttling at the receiver (direction questions 11, receiver side, and 12)

### 3.1 What exists

P03-S019. FACT (`signals/webhook_receiver.py`, search `limit|throttl|cooldown|sleep|semaphore|Lock\(|RLock|Event\(`;
L69 to L108, L240 to L247): the receiver has one rate limit, `_PerIpRateLimiter`, keyed on the source address. It has no
per-signal, per-symbol, per-scanner or global request-rate limit, and no sleep or semaphore. The other limits on the
intake path are elsewhere: the request-level queue threshold (section 5); the fixed pool of eight waitress worker
threads and the connection limit of 100 (P01-S064, P01-S067); the entry throttle inside the processor (P06; Rama's
boundary decision B); and the A04 broker rate limiter, whose non-blocking pre-check in the processor is not wired in
`main.py` (P01 section 10, last point; P04 and P05).

### 3.2 Algorithm, units, burst, refill and defaults

P03-S020. FACT (L79 to L100): a token bucket per address. State: a dict from address to `[tokens, last_ts]` and one
`threading.Lock`. The constructor stores `burst = float(max(1, int(burst)))`, `refill = max(0.0, float(refill_per_sec))`
and `max_ips = 8192` (its default; the receiver passes no value, L245). `allow(ip)` takes `ts = time.monotonic()` and,
under the lock: for an unknown address (after the eviction step of P03-S024 when the map is full) it stores
`[burst - 1.0, ts]` and admits; for a known address it computes `tokens = min(burst, stored + (ts - last_ts) * refill)`;
below 1.0 it stores `[tokens, ts]` and refuses; otherwise it stores `[tokens - 1.0, ts]` and admits. Units: one token per
HTTP request, whatever the number of symbols in it; refill in tokens per second.

P03-S021. FACT (L241 to L247; `config/system_config.yaml` L340 to L342; `core/config_loader.py` L626 to L642): the
limiter is built when `per_ip_rate_limit_enabled` is true (default true), with `int(per_ip_burst or 60)` and
`float(per_ip_refill_per_sec or 5.0)`. The repository file sets true, 60 and 5.0; the schema requires a burst of at least
1 and a refill of at least 0. When the flag is false, `_ip_limiter` is `None` and neither route is limited. A02 K-12
recorded that a configured refill of 0.0, which the schema admits, becomes 5.0 at the receiver (owners A02 and A06; ID
kept). INTERPRETATION (A06 side): the limiter class itself would accept 0.0 (`max(0.0, ...)`), but the receiver
replaces it before construction, so a burst-only limit with no refill cannot be configured.

P03-S022. INTERPRETATION (arithmetic at the file values; P03-S020): a new address may send 60 requests at the same
instant; the 61st in that instant is refused; afterwards about five requests per second are admitted; an emptied bucket
is full again after 12 seconds without requests (60 tokens at 5 per second). HISTORICAL (L72 to L74;
`config/system_config.yaml` L338 to L339): the limit is meant to tolerate "Chartink's legitimate open-bell burst (~40
signals from one IP)". A burst of 40 requests fits within 60; a single request carrying many symbols costs one token.

### 3.3 Scope of the bucket

P03-S023. FACT (L376, L379, L479, L495): `/health` and `/webhook` use the same limiter object and therefore the same
bucket for an address; both test it before authentication, so every admitted request takes a token even if it is then
refused (P02-S068; P02-S069 rows 5, 6, 10, 11). INTERPRETATION: `/health` calls from an address draw on the bucket that
webhook posts from the same address also use. The boot self-check calls `/health` from loopback (P01-S059) and the
pre-flight framework probes `/health` on loopback port 5000 (`scripts/preflight/checks/signals.py` L17; A20); if webhook
posts also reached the receiver from loopback (for example through a tunnel on the same machine), they would share that
bucket. Whether they did is UNKNOWN / NOT ESTABLISHED (P01-S075, P01-S114).

P03-S024. FACT (L91 to L93, L102 to L108): eviction runs only when an unknown address arrives and the map already holds
at least 8,192 entries; it removes the buckets idle for more than 60 seconds; the new address is added whether or not
anything was removed. INTERPRETATION: when more than 8,192 addresses are active within 60 seconds the map grows past
8,192 entries; there is no hard cap. An address whose bucket was removed returns with a full bucket (code L93; comment
L105, HISTORICAL). HISTORICAL (class docstring L75 to L76): "Idle, fully-refilled buckets are evicted lazily so the map
can't grow unbounded under a spoofed-IP flood"; the code evicts on idle time alone (L106) and only from 8,192 entries.

P03-S025. INTERPRETATION (L479; P01-S075; P02-S029) and current external context (read 17-Nov-2026; waitress 3.0.2
tagged source: `server.py` `handle_accept` takes `conn, addr` from `self.accept()` and passes `addr` to the channel,
`channel.py` stores `self.addr = addr`, and `task.py` sets `"REMOTE_ADDR": channel.addr[0]`; Werkzeug published source,
`src/werkzeug/wrappers/request.py` on its main branch: `remote_addr=environ.get("REMOTE_ADDR")`; the installed Werkzeug
version is UNKNOWN / NOT ESTABLISHED, `requirements.txt` does not pin it): the key is `request.remote_addr or
"unknown"`. With no trusted proxy configured (P01-S075), the key is therefore the address of the connection's peer as
accepted by waitress; requests without an address would share one bucket named `"unknown"`. Whether Chartink's requests came from one
address or several is UNKNOWN / NOT ESTABLISHED.

### 3.4 At the limit, missing state, locking, exceptions and restart

P03-S026. FACT (L379 to L380, L495 to L504, L96 to L98): at the limit, `/webhook` writes a `webhook_audit` row (429, 0,
0), logs a WARNING with the path and the address, and answers 429 `{"error": "Rate limit exceeded; slow down"}`;
`/health` answers 429 `{"error": "rate limit exceeded"}` with no audit row and no log. A refused request costs no token:
it stores the fractional token count and the time, so refill continues from that moment. The receiver sends no alert and
keeps no counter of refusals (P02-S068); the dashboard derives "rate_limited_today" from the day's 429 audit rows
(`ops_dashboard/backend/services/capacity.py` L281 to L286; `ops_dashboard/backend/readers/db_reader.py` L1032 to
L1037, `response_code=429`; A15).

P03-S027. FACT (L86 to L100) and INTERPRETATION, current external context (read 17-Nov-2026; Python `time.monotonic`,
quoted in P03-S005): the whole read-compute-write runs inside the limiter's lock, with no I/O, so concurrent requests from
one address are serialised and each sees a consistent count; the elapsed time cannot be negative. Missing state: an
address with no bucket is treated as full and admitted. Corrupt state: the buckets are never loaded from a file or the
database, so no outside source can corrupt them. Exceptions: `allow()` runs before the `try` of L510 on `/webhook` and
outside any `try` on `/health`; an exception there would leave the view and be answered by the Flask 500 handler, with no
audit row (P01-S060). The code states no fail-open or fail-closed rule; no realistic exception source inside `allow()`
was found (float arithmetic and dict operations only). Restart: the buckets start empty, so every address starts with a
full bucket (P03-S016).

### 3.5 Records and history

P03-S028. HISTORICAL (commit `d922007`, 02-Jul-2026, "security(C-2): webhook paper-parity secret + per-IP rate limit";
L70 to L77; L366 to L375; `tests/unit/test_c2_webhook_lockdown.py` L23 to L60, never run): the limiter and its settings
came with C-2; the `/health` route was put behind the same limiter later (commit `84cee3e`, 17-Jul-2026, "authenticate
/health and put it behind the per-IP rate limiter", which `git blame` gives for L376 to L380; the AB-910 comment, "It
also bypassed the per-IP limiter that /webhook is behind"). The tests state these expectations: a burst then refusal, refill over time,
independent addresses, 40 requests admitted at a burst of 60, and removal of idle buckets. WR5 does not list 429
(P01-S007).

## 4. In-flight control (direction questions 12 and 14)

### 4.1 State, claim and release

P03-S029. FACT (L206 to L208, L1074 to L1120): the in-flight state is a dict from symbol to
`{'acquired_at', 'heartbeat_at'}` (monotonic times) with one `threading.Lock` and a literal timeout of 60.0 seconds
(P01-S015). `_claim_in_flight(symbol)`, under the lock, returns False if the symbol is present; otherwise it stores both
times as now and returns True. `_release_in_flight(symbol)` (internal) and `release_in_flight(symbol)` (public) have the
same body: `self._in_flight.pop(symbol, None)` under the lock. `update_heartbeat` has no non-test caller (P01-S077).

P03-S030. FACT (L904 to L935, L944, L1000, L1012, L1014, L1031, L1067, L1070 to L1072): the claim is taken at L934, after
the symbol, price and expiry checks and before the cache. The receiver itself releases it on the five refusals that
follow the claim: cache `DUPLICATE` (L944), `QUEUE_FULL` on the re-queue route (L1000), stored-fingerprint `DUPLICATE`
(L1014), `STORE_ERROR` (L1031) and `QUEUE_FULL` on the first route (L1067). It does not release it on `ACCEPTED` (L1012,
L1072), which is left to the processor (comment L1070 to L1071). `INVALID_SYMBOL`, `INVALID_PRICE`, `EXPIRED` and
`REJECTED_EXCLUDED_SYMBOL` are decided before the claim and take none; the EOD route takes none (P01-S052).

P03-S031. FACT, interface only (`main.py` L3612; `signals/signal_processor.py` L218, L456 to L460, L1267 to L1271, L1699
to L1703, L1733 to L1737; P04 and P05 own these paths): `main.py` passes the bound method `release_in_flight` as
`in_flight_release_fn`, which the processor keeps as `_in_flight_release` and calls with the symbol at four sites:
(i) in `_process_one_safe`, when its order-bucket pre-check fails and the re-queue `put` raises `queue.Full` (L456 to
L460); this route needs a `rate_limiter`, which `main.py` does not pass (L3575 to L3623; default `None`,
`signals/signal_processor.py` L189, L233, L418), so it is not reachable in the `main.py` wiring; (ii) in the `finally`
of `_process_one` (L867), unless the signal was re-queued or handed off (L1267 to L1271); (iii) in the `finally` of
the allocator admission path `admit_prepared` (L1646), unless re-queued (L1699 to L1703); (iv) in `reject_prepared`
(L1706; release at L1733 to L1737). Exceptions from
the call are logged at ERROR at (ii) to (iv) and swallowed at (i). Which routes set "re-queued" or "handed off", and who
releases those claims later, is P04's and P05's (A18 for the allocator). The processor's own `_in_flight_count` (L256
to L257, L1298 to L1305) is a separate counter, not the receiver's dict.

### 4.2 When the release never comes

P03-S032. INTERPRETATION (P03-S029 to P03-S031; P01-S076 to P01-S079): if no release arrives for an accepted signal (a
re-queued or handed-off signal, or a worker that dies or hangs), the claim stays until the sweeper evicts it. With no
heartbeat callback wired (P01-S077), the sweeper evicts at its first 60-second pass after the claim is more than 60
seconds old, that is between 60 and about 120 seconds after the claim (plus the pass's own time), and logs it at
CRITICAL as "STALLED". The claim is therefore a window of one to two minutes, not a lock for the whole processing; while
it lasts, every signal for the symbol from any scanner gets `IN_PROCESS` (P03-S014). If the sweeper thread had ended
(it has no exception handling, P01-S076), a claim that is never released would last until the process ends, and every
later signal for that symbol would get `IN_PROCESS`.

P03-S033. INTERPRETATION (L1093 to L1108, L1197 to L1198): the dict holds one entry per symbol and no signal id; a
release removes whatever entry the symbol has. If the sweeper evicts signal A's claim and signal B for the same symbol
then claims it, A's later release (for example in the processor's `finally`) removes B's claim while B is still being
processed, and a third signal for the symbol can then pass layer 1. This needs a particular run-time interleaving;
whether it ever happened is UNKNOWN / NOT ESTABLISHED.

### 4.3 Claims kept after an exception

P03-S034. KNOWN DEFECT (provisional until the AUDIT, ChatGPT's review and the issue discussion with Rama). FACT (L934
to L1068): the `fetch_one` read (L987) and the re-queue `put_nowait` (L995, whose own `try` catches only `queue.Full`)
run inside the `except sqlite3.IntegrityError` handler of the `try` at L963. The `except Exception` handler of the same
`try` (L1016 to L1044), which releases both claims, does not cover them, and `_process_signal` has no outer `try` or
`finally` after the claim at L934. Current external context (read 17-Nov-2026; Python Tutorial, "Errors and
Exceptions", page for 3.15.2: "Handlers only handle exceptions that occur in the corresponding try clause, not in other
handlers of the same try statement"; SQLite "Result and Error Codes": SQLITE_BUSY means the database file "could not be
written (or in some cases read) because of concurrent activity by some other database connection"; CPython 3.12
`Modules/_sqlite/util.c`: `SQLITE_BUSY`, `SQLITE_LOCKED`, `SQLITE_IOERR` and `SQLITE_FULL` map to `OperationalError`).
Failing condition: `fetch_one` at L987 raises (for example an `OperationalError` after the 30-second busy wait stated
in P03-S051, or on an I/O error), or `put_nowait` at L995 raises anything other than `queue.Full`.
Effect, certain under that condition: the exception leaves `_process_signal` with the in-flight claim (L934) and the
cache key (L947) both still held. The per-symbol loop has no `try` (L696 to L728; P02-S070), so the later symbols of the batch are not
processed and `_handle_webhook` answers 500 and audits (500, 0, 0) (P01-S033). The symbol then gets `IN_PROCESS` until
the sweeper evicts the claim (60 to about 120 seconds, P03-S032) and `DUPLICATE` from the cache until the window ends
(300 seconds at the file value), so a retry in that time is refused. The same holds for an exception other than
`queue.Full` from the first route's `put_nowait` (L1049), which in addition leaves a `QUEUED` row with no queue item.
Current external context (read 17-Nov-2026; Python `queue`, page for 3.15.2): `put` "Raises ShutDown if the queue has
been shut down", and `ShutDown` was "Added in version 3.13" (the Python version on the legacy machines is UNKNOWN / NOT
ESTABLISHED). FACT (search `\.shutdown\(` in non-test code): no code shuts the signal queue down, so no path found at
the baseline makes either `put_nowait` raise; the trigger identified is an exception from the read at L987.
HISTORICAL (comments and docstring; not proof of behaviour): L932 to L933, "From here every reject path MUST release;
every accepted path lets signal_processor release at completion"; L1078 to L1080, "Caller MUST call
_release_in_flight(symbol) on any reject path after a successful claim (DUPLICATE / QUEUE_FULL / IntegrityError)";
L1020 to L1022, claims left held "bounce this (symbol, scanner) as DUPLICATE for the whole dedup window, so the sender's
retry is silently dropped".
The four conditions of the project's KNOWN DEFECT rule (A01 AUDIT section 1.6, applied unchanged by the A02 and A03
AUDITs), for the AUDIT to confirm: (a) holds: the code has a mechanism for a store failure after the claims, the handler
at L1016 to L1044 that releases both; (b) holds: by the language semantics quoted above, an exception raised inside the
sibling `IntegrityError` handler bypasses that mechanism every time; (c) INTERPRETATION: the code says that every path
after the claim releases (L932 to L933, L1078 to L1080) and treats a store failure as a handled case (L1017 to L1018
names `sqlite3.OperationalError` for the INSERT), and a store error can arise with the documented options; (d)
INTERPRETATION: no intent source found says that the claims are kept after an exception, and the sources quoted above
say that they are released. Whether the condition ever occurred is UNKNOWN / NOT ESTABLISHED.

P03-S070. (added in the check) FACT (L934 to L962): between the claim (L934) and the `try` of L963, the cache test and
store (L940 to L947), the slot and fingerprint (L952 to L954), `new_signal_id()` (L957) and the time stamps (L958 to L961)
run outside any `try` of `_process_signal`. An exception raised there leaves the function with the claim, and after L947
also the cache key, still held, with the effects stated in P03-S034 (500, the later symbols of the batch not processed,
a retry refused while the claims last). FACT (L954, checked with a line count; the line was not printed unfiltered): the
fingerprint text is encoded with `fp_raw.encode()`, that is UTF-8 with the default error handling. Current external
context (read 17-Nov-2026; Python `json`, page for 3.15.2: JSON strings may contain "unpaired UTF-16 surrogates", and "By
default, this module accepts and outputs (when present in the original str) code points for such sequences"; Python
`codecs`, page for 3.15.2: 'strict' is the default and raises `UnicodeError`, and without 'surrogatepass' the UTF-8
codec treats "the presence of surrogate code point in str as an error"). INTERPRETATION: an authenticated body whose
`stocks` element is a JSON escape of an unpaired surrogate (code points U+D800 to U+DFFF) passes the symbol, price and
expiry checks (none tests the characters, P02-S061) and makes L954 raise `UnicodeEncodeError`; the claims it leaves are
held on that unusual symbol only. This is the one exception source identified in these lines (`new_signal_id` in
`core/ids.py` was not examined). It needs a body that Chartink is not shown to send; whether it ever occurred is
UNKNOWN / NOT ESTABLISHED. Not classified here; the AUDIT may examine it.

### 4.4 Restart effect

P03-S035. FACT (L206, P03-S016): the in-flight dict starts empty in each process and nothing reloads it; the queue it
protects also starts empty (`main.py` L3402 to L3404). INTERPRETATION: after a restart no symbol is claimed, so the only
layer that can refuse a same-day alert is layer 3 (P03-S016).

## 5. The queue put and its threshold (direction questions 13 and 16, put side)

### 5.1 The queue

P03-S036. FACT (`main.py` L3402 to L3404; `config/system_config.yaml` L125; `core/config_loader.py` L194) and current
external context (read 17-Nov-2026; Python `queue`, page for 3.15.2: "If maxsize is less than or equal to zero, the
queue size is infinite"; "The Queue class in this module implements all the required locking semantics"; "In a FIFO
(first-in, first-out) queue, the first tasks added are the first retrieved"): the signal queue is a FIFO
`queue.Queue(maxsize=signal_queue.capacity)`, 300 in the repository file; the schema field is a required `int` with no
validator (A02 STUDY section 4.3, "Ranges" row, lists `signal_queue` among the keys whose range is not enforced). INTERPRETATION: a
capacity of 0 or less, which the schema accepts, would make the queue unbounded, while the receiver's threshold
`int(capacity * backpressure_pct)` would be 0 or less (with a `backpressure_pct` of 0 or more, which the schema does not
enforce either), so `qsize() >= threshold` would hold for every intraday request
and each would be answered 503. At the file value this does not arise.

### 5.2 The request-level threshold

P03-S037. FACT (L570 to L578; `config/system_config.yaml` L125 to L126; P01-S034 step 5): after authentication, the
scanner lookup, the EOD branch and the kill switch, and before the entry window and the parse, the receiver compares
`self._queue.qsize()` with `int(capacity * backpressure_pct)`, which is `int(300 * 0.80) = 240` at the file values. At
or above it, it answers 503 `{"error": "Signal queue at capacity; retry later"}` with the header
`X-Queue-Depth: <qsize>/<capacity>`. Nothing else happens: no claim, no `signals` row, no queue change, no log line and no
alert; the `finally` of `_handle_webhook` writes the audit row (503, 0, 0) (P02-S069 row 17). EOD alerts never reach the
check (P01-S036).

P03-S038. INTERPRETATION, current external context (read 17-Nov-2026; Python `queue`: `qsize()` returns "the approximate
size of the queue ... nor will qsize() < maxsize guarantee that put() will not block"): the check and the later puts are
separate steps with no common lock, and up to eight requests run receiver code at the same time (P01-S068). Several
requests can pass the check at a depth just under 240, and each then puts all its accepted symbols, so the depth can
pass 240 and reach the hard limit of 300; one request whose accepted symbols outnumber the free slots can do so on its
own. The processor's re-queues (P03-S043) add to the depth with no threshold check. Per-symbol `QUEUE_FULL` therefore
arises only for requests that passed the threshold before the depth rose (A02 K-11 noted the multi-symbol route; K-11's
owners as recorded are A02 for the keys, A20 for the pre-flight and A06 for the receiver, and its handoff row names
A20).

### 5.3 The per-symbol put

P03-S039. FACT (L1046 to L1068, L733 to L734) and current external context (read 17-Nov-2026; Python `queue`:
`put_nowait(item)` is "Equivalent to `put(item, block=False)`", which puts the item "if a free slot is immediately
available, else raise the Full exception (timeout is ignored in that case)"): each accepted symbol is put with
`put_nowait`, never blocking and with no timeout. On `queue.Full` the receiver runs
`UPDATE signals SET status = 'QUEUE_FULL'` in its own transaction (a failure is logged at ERROR and the row stays
`QUEUED`), removes the cache key, releases the claim and returns `QUEUE_FULL`, which makes the whole batch answer 503 and
the audit row (503, 0, 0) (P02-S067). The loop continues with the next symbol, which is accepted if a slot has freed in
the meantime. No alert is sent. INTERPRETATION (P03-S010): if that UPDATE fails, the row stays `QUEUED` although the
signal was never queued, and a sender's retry then meets a `QUEUED` row and is answered `DUPLICATE`, so the signal is
neither queued nor recoverable by retry.

P03-S040. FACT (search `QUEUE_FULL|status *= *'QUEUED'|"QUEUED"` in non-test code): no non-test code reads `signals`
rows with status `QUEUED` or `QUEUE_FULL` in order to put them back on the queue; the readers found are display and
report code (`ops_dashboard/backend/readers/db_reader.py` L668 to L679, L896; `reports/signal_status.py` L46;
`reports/daily_report.py` L496; A15). INTERPRETATION: a `QUEUE_FULL` row leaves that state only through a sender's
retry on the re-queue route (P03-S012) that arrives before the expiry age (P03-S015 R6), on the same day, and when the
depth is below the threshold. The search covered literal status texts only; any processor-side recovery is P04's.

P03-S041. FACT (L696, L719 to L728) and current external context (FIFO, P03-S036): within one request the symbols are
put in payload order, skipping those refused. INTERPRETATION: across concurrent requests the order of puts follows
thread scheduling, since no lock spans a request; the re-queue route puts an earlier signal behind later ones. Ordering
after the get is P04's.

P03-S042. FACT (L574, L740 to L744; `config/system_config.yaml` L128; `core/config_loader.py` L197): after the loop the
receiver adds `X-Queue-Depth` to the batch answer (200 or 503) and adds `X-Queue-Warning: high` when the depth is at or
above `int(capacity * warning_pct)`, 180 at the file values (`warning_pct` is read with `getattr` default 0.60; the file
and the schema default are both 0.60). The request-level 503 carries only `X-Queue-Depth`; the other answers (the 4xx
answers, the shutting-down 503 at L490, the 500 at L528 and the EOD answers at L788 and L804) carry neither. INTERPRETATION: the warning only informs the sender; the receiver logs and alerts nothing at 180.

### 5.4 Other users of the same queue (interface only)

P03-S043. FACT, interface only (`signals/signal_processor.py` L418 to L427, L1501 to L1530; P04 owns them) and current
external context (Python `queue`: with a positive timeout `put` "blocks at most timeout seconds and raises the Full
exception if no free slot was available within that time"): the processor puts items back on the same queue in two
places, `put(signal_tuple, timeout=1.0)` in `_process_one_safe` (only when a `rate_limiter` is set, which `main.py`
does not do, P03-S031) and `put(signal_dict, timeout=1.0)` for the FIX-069 transient-error retry (L1520). INTERPRETATION:
these puts share the 300 slots with the receiver's puts and count in the receiver's depth check; the FIX-069 item is a
dict (L1510 to L1517), a different shape from the receiver's 5-tuple (P01-S042), which `_process_one_safe` accepts
(L407 to L413).

P03-S044. FACT, interface only (`signals/signal_processor.py` L304 to L320, L377 to L399; `config/system_config.yaml`
L345 to L346) and current external context (read 17-Nov-2026; CPython 3.12 `Lib/concurrent/futures/thread.py`:
`self._work_queue = queue.SimpleQueue()`, an unbounded queue, and `submit` puts the work item on it, so `submit` does not
wait for capacity): the processor's single dispatcher thread takes each item with `get(timeout=drain_poll_sec)` (0.1 s in
the file), calls `_warm_zones` on it and submits it to a `ThreadPoolExecutor` of `worker_count` threads (5 in the file).
INTERPRETATION: the signal queue holds only items the dispatcher has not yet taken; work waiting for the five workers
sits in the executor's own unbounded queue, which `qsize()` does not count. The depth that the thresholds of 240 and 300
measure therefore rises only when the dispatcher itself is slow or stopped (for example a slow `_warm_zones` call, or
after `signal_proc.stop()`), not when the workers are busy, and the amount of work waiting for workers has no bound at
the receiver. The dispatcher, `_warm_zones` and the pool are P04's; the Python version on the legacy machines is UNKNOWN
/ NOT ESTABLISHED (the 3.12 source was read).

### 5.5 The same values at other consumers (A02 handoffs)

P03-S045. FACT (lines given; owners named) and INTERPRETATION (last column), the consumers of `signal_queue.capacity`,
`backpressure_pct` and `warning_pct` and of the live depth:

| Consumer | Lines | Value and rule | What it means there (INTERPRETATION) | Owner |
|---|---|---|---|---|
| queue construction | `main.py` L3403 | `maxsize = capacity` (300) | hard limit for every put | A06 (A01 file) |
| receiver, request check | `webhook_receiver.py` L571 to L578 | `int(capacity * backpressure_pct)` = 240 | refuse the whole intraday request with 503 before parsing | A06 |
| receiver, per-symbol put | L995, L1049 | `put_nowait` against `maxsize` | `QUEUE_FULL` for one symbol, batch 503 | A06 |
| receiver, warning header | L574, L743 to L744 | `int(capacity * warning_pct)` = 180 | header to the sender only | A06 |
| receiver, `/health` | L395 to L403 | `qsize()` and `capacity` | authenticated report of the live depth (P01-S058) | A06 |
| processor re-queues | `signal_processor.py` L426, L1520 | `put` with 1 s wait against `maxsize` | a re-queue that fails after 1 s | A06 (P04) |
| processor `stats()` | `signal_processor.py` L2702 | `qsize()` | a metric; its reader was not traced | A06 (P04) |
| dashboard capacity row | `ops_dashboard/backend/services/capacity.py` L170 to L181 | limit `capacity`; `backpressure_at = round(bp * capacity)` = 240; live value from `queue_size` in the health JSON of port 8080 | display of depth against limit, annotated with the refusal point | A15 |
| pre-flight backpressure check | `scripts/preflight/checks/signals.py` L72 to L82; `scripts/preflight/checks/engine.py` L30 | `queue_depth` and `queue_capacity` from `/metrics` on port 8080; WARN at `depth >= cap * 0.9` | an early warning, with its own 0.9 instead of the key | A20 (A02 K-11) |

P03-S046. FACT (`scripts/healthcheck_server.py` L122 to L128, L137 to L155, L251 to L255; `main.py` L4074 to L4076;
`signals/signal_processor.py` L274 to L279, L675 to L681, L683 to L738; `signals/entry_throttle.py` L117 to L124;
`ops_dashboard/backend/readers/metrics_client.py` L42 to L43; `ops_dashboard/backend/config/gui_config.yaml` L42 to
L43): the port-8080 server's `/metrics` starts with `queue_depth: 0` and `queue_capacity: 0` (its only queue keys)
and merges only the processor's runtime metrics, whose keys include no queue key (the initial keys at L274 to L279 and
the four keys passed to `_bump_metric` are signal and entry counts; the entry-throttle keys added at L708 are throttle
counts); the dashboard reads `trader_metrics.health_url`, port 8080 `/health` both as the code default and in the
repository file (the effective value is UNKNOWN / NOT ESTABLISHED); its `/health` answer holds `status`,
`checks`, `uptime_seconds`, `trades_today` and `timestamp`, and no `queue_size`. INTERPRETATION: at the baseline code the
pre-flight backpressure check always reads a capacity of 0, so its condition `cap and depth >= cap * 0.9` is never true
and it passes with "no backpressure"; and the dashboard's signal-queue row never finds `queue_size`, so it shows
UNAVAILABLE with the note "trader down — live queue depth unavailable" even when the trader answers. A02 K-11's
interpretation ("the warning starts at 270") assumed a capacity of 300 reaching the check; at the baseline that input is
0. K-11 keeps its owner (A20), classification and treatment; this is A06's interface observation only, and the A15 and
A20 sides are theirs. The receiver's own `/health` on port 5000 does report the live depth, but neither reader calls it
for the depth.

P03-S047. INTERPRETATION (P03-S036 to P03-S046), answer to question 13 (no design): the same settings carry different
meanings at different consumers. `capacity` is the hard put limit in the queue, the base of the receiver's two
thresholds, a display denominator at `/health` and in the dashboard, and in the pre-flight a value read from an endpoint
that reports 0. `backpressure_pct` is a request refusal point in the receiver, truncated with `int()`, and an annotation
in the dashboard, rounded with `round()`; the two agree at 300 and 0.80 (240) but differ for some other capacities (for
example 301: 240 against 241). The pre-flight uses its own factor 0.9 and not the key. And the depth all of them compare
is the dispatcher's hand-off buffer, not the work waiting for workers (P03-S044), so the 503 text "Signal queue at
capacity" means the dispatcher is behind, not that 300 signals are waiting to be processed.

P03-S048. FACT (A02 records; receiver lines re-read): the A02 items, A06 side. K-38 (A02 MATCH for `capacity`,
`expiry_sec` and `warning_pct` reaching their consumers): the receiver's reads are at L571, L574 and L679 and
`main.py` L3403, as A02 recorded. K-50 (A02 MATCH for `bind_host`, `require_hmac`, `per_ip_rate_limit_enabled` and
`per_ip_burst`): the limiter reads are at L241 to L245 (P03-S021). K-12: the dedup floor and the refill fallback
(P03-S003, P03-S021). K-11 (owners as recorded: A02, A20, A06 for the receiver; handoff row A20): in this part
at P03-S038 and P03-S046. The IDs, owners, classifications and treatments are unchanged.

## 6. The receiver's storage writes and the census read (direction question 23, receiver side)

A03 owns the schema, the store and its transactions; this section records the receiver's side of the boundary only.

### 6.1 `webhook_audit`

P03-S049. FACT (L487 to L489, L497 to L499, L529 to L534, L1126 to L1152; `core/schema.sql` L581 to L593): `_write_audit`
is called from three places in `_handle_webhook`: the shutting-down answer (503), the limiter answer (429) and the
`finally` that follows every outcome of `_process_request`, including the 500 of L525 to L528. Each call inserts one row
with `ts`, `scanner_name` (the path segment as received, not validated), `source_ip`, `payload_size_bytes` (the length of
the body read at L480), `response_code`, `signals_accepted`, `signals_rejected` and `duration_ms`; `id` is assigned by
the database and `date` is a stored generated column, `substr(ts, 1, 10)`. This matches A03's record (P06a-S035). The
requests that write no row are listed in P01-S027, P01-S030, P01-S058, P01-S118 and P02-S069 (rows 1 to 8 and 30 to 32);
the counts' meaning is in P02-S067.

P03-S050. FACT (L478, L486, L496, L530, L1136; `core/schema.sql` L583): `ts` is `now_ist().isoformat()` taken inside
`_write_audit`, at the moment of writing; `duration_ms` is the monotonic time from the start of the handler to just
before the write. HISTORICAL (schema comment L583): "ISO-8601 IST when request arrived". INTERPRETATION: `ts` records the
end of handling, not the arrival; the arrival is about `ts` minus `duration_ms`. `date` is the IST date at the moment of
writing.

P03-S051. FACT (L1137 to L1154; `core/state_store.py` L107 to L113, L215 to L237, L524 to L541): each row is written in
its own `transaction()`: `BEGIN IMMEDIATE`, the INSERT, `COMMIT`, or `ROLLBACK` and re-raise, which `_write_audit`
catches, logs at ERROR and does not pass on, so the answer is never changed. The connection is the calling waitress
worker thread's own, opened on first use with `busy_timeout = 30000`, `timeout=30` and `check_same_thread=True`. A03
R-39 recorded this write as a MATCH (owners A06 and A01; ID kept). Current external context (read 17-Nov-2026; Python
`sqlite3.connect` timeout: "How many seconds the connection should wait before raising an OperationalError when a table
is locked"; Python Language Reference 8.4.4: when a `return` runs in the `try` suite, "the finally clause is also executed
'on the way out'") and INTERPRETATION: while another connection holds the write lock, the audit insert can wait up to
about 30 seconds before failing; because every audit write runs before the view returns (directly before the return on
the 503 and 429 routes, and in the `finally` for the rest), the HTTP answer leaves only after the audit write has
finished or failed, so a slow write delays every `/webhook` answer, the 429 and 503 answers included.

P03-S052. FACT (L1126 to L1154; search of the receiver for `webhook_audit`): the receiver only inserts into
`webhook_audit`; it never reads, updates or deletes it.

### 6.2 The census read of `webhook_audit` (`main.py` L1662 to L1675)

P03-S053. FACT (`main.py` L1599, L1662 to L1675, L1684 to L1688; `core/effect_telemetry.py` L257 to L267;
`config/expected_managers.yaml` L149 to L154): at shutdown, `_shutdown` (L1599) passes `emit_census` a function that
runs `SELECT COUNT(*) FROM webhook_audit WHERE date = ?` with the IST date taken at census time, on the store connection
of the thread that runs `_shutdown` (A01's). The registry file gives the entry `webhook_receiver` the state
`covered-existing` (L152); for that entry `emit_census` calls the function and writes the line
`effect_census | webhook_receiver: acted <n> | covered-existing`; an exception gives `derive-failed`, and the outer `try`
logs any other failure at ERROR. The census runs before `webhook_receiver.stop()` (L1684 to L1688), so the receiver's
shutting-down flag (L485, L1172) is not yet set when the count is made. HISTORICAL (`config/expected_managers.yaml` L153 to L154):
`effect_point` "webhook_audit day-count (WR13 finally, ...) — NO new counter" and `acted_means` "a POST audited".
INTERPRETATION: "acted" is the number of audit rows of that date, that is every POST that wrote an audit row (401, 404,
429, 503 and 500 answers and EOD alerts included), not the number of signals accepted; rows written after the census
(requests in progress, P01-S084; requests arriving before `stop()`; the shutting-down 503 answers after it) are not
counted; a process running past midnight is counted for the census date only. A01 owns the census and the registry
entry; A03 recorded the read (P06a-S022).

P03-S054. FACT, interface only (A03 records): `scripts/db_retention.py` deletes `webhook_audit` rows older than 90 days
(A03 Z-26, MATCH); the readers of the table are dashboard and report code (A03 evidence
`evidence/A03_SQL_OUTSIDE_STORE_SCRIPTS_2026-11-09.md`, P06b-S025, P06b-S048, P06b-S059,
P06b-S075, P06b-S103, P06b-S118, P06b-S121, P06b-S154; A15).

### 6.3 `signals` writes on the dedup and queue routes

P03-S055. FACT (L963 to L1068): the receiver writes `signals` in three statements, each in its own transaction on the
request thread's connection: the INSERT of a new row with status `QUEUED` (L963 to L980; the columns are in P01-S041
and P01-S043; event creation is P05's and P11's), the flip to `QUEUED` on the re-queue route (L1003 to L1007) and the
mark `QUEUE_FULL` (L1052 to L1057). An INSERT that fails with an exception other than `sqlite3.IntegrityError` is
answered `STORE_ERROR` after both claims are released and a CRITICAL line is logged (L1016 to L1044); an
`IntegrityError` takes the route of P03-S010; a failed UPDATE is logged at ERROR and the per-symbol answer is unchanged. The
`fetch_one` of L987 is a plain read outside any transaction. A03 R-08 (the re-queue order) is recorded at P03-S012.
INTERPRETATION (P03-S051; the same 30-second wait that A03 P-12 recorded for the processor's status writes under the
fund manager's lock, whose A06 side, the lock scope, is P04's and P05's): on the receiver's side, an INSERT that waits
for the write lock holds the symbol's in-flight claim and cache key for that time and delays the answer; if the wait
ends in `OperationalError`, the symbol is answered `STORE_ERROR` and the batch 503.

### 6.4 The EOD-webhook heartbeat

P03-S056. FACT (L786 to L787, L801 to L803, L806 to L834; `utils/cron_heartbeat.py` L35 to L41, L55 to L95;
`core/state_store.py` L3305; `core/schema.sql` L1019): each EOD alert that passes the body checks (L757 to L774) leads
to one call
`record_heartbeat("pb01_capture", status=..., functional_status=..., message="scanner=<name> symbols=<n> queued=<m>")`,
made on the request thread before the 200 answer, without `db_path`, so the default relative path
`data_store/trading_system.db` is used. If that path does not exist relative to the working directory, the helper returns
False without writing or logging (L81 to L82). Otherwise it constructs a new `StateStore` on that path, calls
`insert_cron_heartbeat` (job name, `executed_at` as the IST time in ISO form, status, no duration, and the message
prefixed `[func=<status>]` when a functional status is given), closes the store and returns True; any exception returns
False, and the `close()` is then skipped (it is not in a `finally`). The receiver ignores the return value. Its own
`except` (L830 to L834) catches exceptions raised at L825 to L829, such as a failure of the import at L825, and logs
them at WARNING; the helper itself raises none (L80 to L95). INTERPRETATION: a heartbeat that was not written
(missing path, store error) leaves no trace in the receiver's log; whether the relative path names the same database
file that the trading process uses depends on the working directory and the store path, which are UNKNOWN here (A03
D-08 and D-09; A17's unit). A03 D-08 (owner of the call site: A06) recorded that each EOD request constructs a full store
on the request thread; the receiver side is as recorded, and D-08's classification is unchanged. The `cron_heartbeat`
table and the store's open cost are A03's; the helper is A16's; the capture worker is A18's.

## 7. Concurrency (direction question 14, receiver side)

P03-S057. FACT (P01-S017, P01-S064, P01-S067, P01-S068, P01-S080; P03-S031, P03-S053): the threads that touch the
receiver's state are the eight waitress worker threads (`_handle_webhook` and `health`), the sweeper thread, the
processor's worker threads (through `release_in_flight`), whichever thread calls `admit_prepared` or `reject_prepared`
(the allocator's; A18, P03-S031), and the thread that runs `_shutdown` (`stop()` and the census read; A01's). The
"webhook-server" thread runs waitress's I/O loop only (P01-S068). Current external context (waitress "Design", page for
waitress 3.0.2, read 17-Nov-2026: "The thread dispatcher maintains a fixed pool of worker threads available to do client
work"; "When all worker threads are in use, scheduled tasks will wait in a queue for a worker thread to become
available"): with all eight worker threads busy, further complete requests wait in waitress's task queue.

P03-S058. FACT (lines given) and INTERPRETATION (last column), the shared state:

| State | Lines | Lock | Accessed by | Atomicity (INTERPRETATION) |
|---|---|---|---|---|
| `_in_flight` | L206 to L207, L1074 to L1120, L1189 to L1198 | `_in_flight_lock` | request threads (claim, release), processor workers (release), sweeper (evict) | each operation atomic; the sweeper logs after releasing the lock (L1199) |
| `_dedup_cache` | L237 to L238, L941 to L947, L998, L1029, L1065 | `_dedup_lock` | request threads | test-and-store atomic; removals atomic |
| limiter buckets | L83 to L84, L88 to L100 | the limiter's lock | request threads | read-compute-write atomic |
| `signal_queue` | `main.py` L3402 | the queue's internal locks | request threads (put), the dispatcher (get), processor workers (put) | each call atomic; the depth test and the puts are not one step (P03-S038) |
| `_alias_map`, configuration | L227; L171 to L176 | none | read only after construction | no writer after construction (P01-S018) |
| `_eod_capture` | L1156 to L1160 | none | the start-up code (one assignment at `main.py` L3747), request threads (read) | the assignment precedes the server start at `main.py` L4000 (P01-S024, P01-S072) |
| `_shutting_down` | L213 | `threading.Event` | the `_shutdown` thread (set), request threads (test) | thread-safe by the Event |
| database | `core/state_store.py` L215 to L237, L531 | SQLite's write lock (`BEGIN IMMEDIATE`) | one connection per thread | writers serialised; waits up to about 30 s (P03-S051) |

P03-S059. FACT (L941 to L945, L998 to L1000, L1029 to L1031, L1065 to L1067, L1083, L1192): the only nested locking is at
L941 to L945, where `_release_in_flight` takes the in-flight lock while the dedup lock is held; the other three
cache removals release the dedup lock before releasing the claim, and no code takes the dedup lock while holding the
in-flight lock. INTERPRETATION: the two locks are always taken in the same order, so they cannot deadlock each other.

P03-S060. INTERPRETATION (P03-S001 to P03-S059), simultaneous requests:
- Same scanner and symbol at the same moment (for example a double delivery): the first thread to claim wins; the other
  gets `IN_PROCESS`; one `signals` row results.
- Same symbol from different scanners: one wins; the other gets `IN_PROCESS` and no row (P03-S014).
- Different symbols: independent; their database writes are serialised; the order of rows and queue items follows
  thread scheduling (P03-S041).
- Many requests near the threshold: P03-S038.
- A slow database: request threads wait up to about 30 seconds for each write while holding their claims (P03-S051,
  P03-S055); with all eight threads waiting, new requests wait in waitress; how the sender treats slow answers is
  UNKNOWN / NOT ESTABLISHED.
- A request in progress at shutdown: P01-S084.

P03-S061. INTERPRETATION, summary of the receiver-side routes by which signals can be duplicated, lost, reordered or
changed (each with its basis; whether any occurred is UNKNOWN / NOT ESTABLISHED):

| Kind | Route | Basis |
|---|---|---|
| duplicate | a claim evicted by the sweeper while its signal is still processed lets a second signal for the symbol in | P01-S079, P03-S032 |
| duplicate | a release by symbol removes another signal's claim | P03-S033 |
| duplicate | a second scanner's signal for the same symbol after the claim ends (the keys of layers 2 and 3 include the scanner; later guards are A07's and A09's) | P03-S014 |
| duplicate | after a restart, a same-day alert in a later slot | P03-S016 |
| duplicate | more than 10,000 live cache keys evict a key early | P03-S005 |
| loss | another scanner's signal refused `IN_PROCESS`, with no row and a 200 answer | P03-S014 |
| loss | claims kept after an exception refuse the retries for the window | P03-S034 |
| loss | an exception after the claim and outside any `try` ends the request with 500, abandons the later symbols of the batch and keeps the claims (added in the check) | P03-S070 |
| loss | a `QUEUE_FULL` row never retried, or retried after the expiry age | P03-S015 R1 and R6, P03-S040 |
| loss | a failed `QUEUE_FULL` mark leaves a `QUEUED` row for a signal never queued; a retry is refused as `DUPLICATE` | P03-S039 |
| loss | queued items lost at a restart while their rows say `QUEUED`; a retry is refused as `DUPLICATE` | P03-S015 R7 |
| loss | a request-level 429 or 503 not retried by the sender | P03-S026, P03-S037; P02-S072 |
| loss | requests in progress at shutdown | P01-S084 |
| status | a failed flip leaves `QUEUE_FULL` on a queued signal; the flip can overwrite a later status (A03 R-08) | P03-S012 |
| reorder | concurrent requests; re-queued items go to the back | P03-S041, P03-S043 |
| changed fields | the re-queue route queues the current request's price and trigger time under the earlier signal id | P03-S012 |

## 8. Inherited items touched by this part (A06 side only)

Each item keeps its original owners, ID, classification, status and treatment; only the A06 side is recorded here.

| Item | Source record | Owners as recorded | A06 side in this part |
|---|---|---|---|
| K-12 (one of the 52) | A02 AUDIT | A02; A06, A11, A12 | the receiver's floor of the dedup window and refill fallback, and the floor governing both dedup layers (P03-S003, P03-S021) |
| K-38 (A02 row naming A06; not one of the 52) | A02 AUDIT, key-section table | A06, A20 | the receiver's reads of `capacity`, `warning_pct`, `expiry_sec` confirmed (P03-S048) |
| K-50 (A02 row naming A06; not one of the 52) | A02 AUDIT, key-section table | A06, A17 | the limiter's reads confirmed (P03-S021, P03-S048) |
| K-11 (A20's item; not one of the 52) | A02 AUDIT | A02; A20; A06 (receiver) | the receiver's threshold (P03-S037, P03-S038); interface observation that the pre-flight's inputs are 0 at the baseline (P03-S046) |
| R-08 (one of the 52) | A03 AUDIT | A06; A03 | the re-queue route as recorded; in addition, the queue item's price and trigger time come from the current request (P03-S012) |
| D-08 (one of the 52) | A03 AUDIT | A16; A06 (call site); A15; A03 | the EOD heartbeat call as recorded; its return value ignored and a missing path silent (P03-S056) |
| P-12 (one of the 52) | A03 AUDIT | A03; A06, A09 | not this part's: P-12's A06 side is the processor's lock scope (P04, P05); this part records only that the receiver's own writes use the same 30-second wait (P03-S051, P03-S055) |
| R-39 (A03 row naming A06; not one of the 52) | A03 AUDIT | A06; A01 | the audit write and the census read as recorded (P03-S051, P03-S053) |

A03 P-02, P-11 and Q-11 concern the processor's status writes and are not touched here (P04, P05).

## 9. Points the AUDIT may examine (neutral)

These are pointers only; no issue is counted or judged here.
- The three duplicate layers start their windows differently (receipt clock, fixed from the first store; trigger-time
  slot grid); the minute-precision texts (WR7, schema comments) and the FIX-036 "replaces" comment no longer describe the
  code (P03-S005, P03-S013, P03-S017).
- Layer 1, keyed on the symbol alone, refuses another scanner's signal with `IN_PROCESS`, without a stored row and with a
  200 answer, against the schema comment that `signals` is an "Immutable log of EVERY incoming webhook signal" (schema
  L36; P03-S014).
- The re-queue route cannot tell a retry from a new alert in the same slot, and queues the current price and trigger time
  under the earlier id, while the row keeps the first values (P03-S012; with A03 R-08).
- Every `IntegrityError` from the INSERT is answered `DUPLICATE` (P03-S011).
- Claims kept after an exception inside the `IntegrityError` handler (P03-S034; KNOWN DEFECT, provisional, with the four
  conditions stated for the AUDIT to confirm), and after an exception outside any `try` between the claim and the
  INSERT, for example a symbol carrying an unpaired surrogate (P03-S070).
- A release by symbol can remove another signal's claim; with no heartbeat wired the claim lasts one to two minutes
  (P03-S032, P03-S033; P01-S079).
- Nothing re-reads `QUEUE_FULL` or `QUEUED` rows; only a sender's retry within the expiry age recovers a `QUEUE_FULL`
  signal; queued items lost at a restart are refused on retry (P03-S015, P03-S040).
- The limiter: one bucket for `/health` and `/webhook`; one token per request whatever the symbols; no hard cap on the
  map; a refill of 0 cannot be configured (P03-S020 to P03-S024).
- The request threshold is checked once per request, not atomically with the puts; the depth measured is the
  dispatcher's hand-off buffer, not the work waiting for workers (P03-S038, P03-S044, P03-S047).
- A capacity of 0 or less, accepted by the schema, would refuse every intraday request (P03-S036).
- The dashboard and the pre-flight read queue values from port-8080 surfaces that carry no live queue value (P03-S046;
  A15 and A20 own those readers); `round()` against `int()` for the same threshold (P03-S047).
- No log line and no alert for the request-level 503; the warning at 180 is a header only (P03-S037, P03-S042).
- `webhook_audit.ts` is the time of writing, while the schema comment says "when request arrived"; every `/webhook`
  answer waits for the audit write (P03-S050, P03-S051).
- The census "acted" count for the receiver counts every audited POST of the day, not accepted signals, as the
  registry's `acted_means` "a POST audited" says; the census is taken before the receiver is stopped (P03-S053).
- The EOD heartbeat can fail silently (missing relative path, store error), and its store is not closed on an exception
  (P03-S056; A03 D-08).

## 10. UNKNOWN / NOT ESTABLISHED

P03-S062. UNKNOWN / NOT ESTABLISHED: every runtime fact for this part: whether any `IN_PROCESS`, `DUPLICATE`,
`QUEUE_FULL`, `STORE_ERROR`, 429 or request-level 503 occurred; the queue depths reached; how long claims were held;
whether the sweeper evicted a claim; whether the exception route of P03-S034 or the release interleaving of P03-S033
occurred; whether any `QUEUE_FULL` row was ever re-queued (no production log, database or journal is admitted).

P03-S063. UNKNOWN / NOT ESTABLISHED: the effective values of `webhook.dedup_window_seconds`, the per-IP settings,
`signal_queue.*` and `signal_processor.worker_count` and `drain_poll_sec` (only the repository file values are known;
P01-S110).

P03-S064. UNKNOWN / NOT ESTABLISHED: the installed versions of Python and cachetools on the legacy machines; the pin is
`cachetools==7.1.1`, Python is not pinned; the Python 3.15.2 documentation and the CPython 3.12 source were read.

P03-S065. UNKNOWN / NOT ESTABLISHED: whether Chartink retries, on which statuses, after what delay and with the same body;
the address or addresses its requests come from; how it treats slow answers (P02-S072).

P03-S066. UNKNOWN / NOT ESTABLISHED: the network path in front of port 5000 and so the address the limiter and the audit
see (P01-S075, P01-S114).

P03-S067. UNKNOWN / NOT ESTABLISHED: whether the heartbeat helper's relative default path names the trading database in
production (working directory; A03 D-08 and D-09; A17).

P03-S068. UNKNOWN / NOT ESTABLISHED in this part (owned by P04 and P05): any processor-side recovery of `QUEUED` or
`QUEUE_FULL` rows at boot; who releases the receiver's claim for re-queued and handed-off signals; how long
`_warm_zones` can hold the dispatcher.

P03-S069. UNKNOWN / NOT ESTABLISHED: the database lock waits actually met by the receiver's writes (the store's
30-second wait, P03-S051; A03 P-12 records the same unknown for the processor's writes).

## 11. Draft questions about intent for Rama

Neutral questions about what was intended; no answer is proposed.
- Q-P03-01. Was a signal from a second scanner for a symbol already being processed meant to be dropped without a stored
  row, or to be recorded or held? (P03-S014)
- Q-P03-02. What duplicate window was intended: a fixed time after the first signal, a fixed five-minute slot of the
  trigger time, or both? Was "minute precision" (WR7) still intended after FIX-131? (P03-S013, P03-S017)
- Q-P03-03. Was a new alert in the same five-minute slot as an earlier `QUEUE_FULL` signal meant to revive the earlier
  signal with the new price, or to be treated as a new signal or as a duplicate? (P03-S012)
- Q-P03-04. Was a `QUEUE_FULL` signal meant to be processed only if the sender retried, or was the system meant to
  recover it itself? (P03-S040)
- Q-P03-05. Was the per-IP limit meant to count `/health` calls in the same bucket as webhook posts, and to count requests
  rather than symbols? (P03-S020, P03-S023)
- Q-P03-06. What was the 503 queue threshold meant to protect: the number of signals waiting to be processed, or the
  hand-off to the dispatcher? (P03-S044, P03-S047)
- Q-P03-07. Was `webhook_audit.ts` meant to be the arrival time of the request? (P03-S050)
- Q-P03-08. The census registry says the receiver's count means "a POST audited" (HISTORICAL, P03-S053). Was the census
  meant to be taken before the receiver stops taking requests, so that later requests of the day are not counted?
  (P03-S053)
- Q-P03-09. Was a request-level 503 for the queue threshold meant to be logged or alerted by the receiver? (P03-S037)

## 12. Where the direction's questions are answered

| Direction question | Where in P03 | Main owner part |
|---|---|---|
| 1 to 8 Ingress, server, scanners, reachability, authentication, A02-13, validation | not in P03 | P01, P02, P07 |
| 9 Responses and side effects | P03-S025, P03-S026, P03-S037, P03-S039, P03-S042 (the limiter, threshold and queue answers only) | P02 |
| 10 Deduplication | P03-S001 to P03-S018; P03-S034 and P03-S070 (claims kept after an exception) | P03 |
| 11 Throttling (receiver side) | P03-S019 to P03-S028 | P03; P06 for the entry throttle |
| 12 Limits reached, missing or corrupt state, contention, restart, exceptions | P03-S016, P03-S021, P03-S024 to P03-S027, P03-S029 to P03-S035, P03-S039, P03-S051, P03-S056, P03-S070 | P03 |
| 13 Queue threshold and capacity against A02 | P03-S036 to P03-S038, P03-S044 to P03-S048 | P03 |
| 14 Concurrency, duplicate, lost or reordered signals (receiver side) | P03-S014, P03-S032 to P03-S034, P03-S038, P03-S041, P03-S057 to P03-S061, P03-S070 | P03; P04 for the processor |
| 15 Path through the processor | P03-S031, P03-S043, P03-S044 (interface only) | P04 |
| 16 Queue type, capacity, producers, backpressure, ordering, overflow (put side) | P03-S036 to P03-S044 | P03; P04 for the get side |
| 17 Expiry | P03-S015 R6 (its effect on retries only) | P04 |
| 18 Alias normalisation | P03-S002 (its effect on the keys only) | P05 |
| 19 Fields across handoffs | P03-S012 (the re-queue route) | P04, P05 |
| 20 Event creation and persistence | P03-S039, P03-S055 (the receiver's writes on these routes) | P05, P11 |
| 21 Wiring and callbacks | P03-S031 (the release callback), P03-S043 | P01, P04 |
| 22 A06 lifecycle against A01's | not in P03 (P01-S095 to P01-S108) | P01 |
| 23 Storage boundaries | P03-S049 to P03-S056 | P03, P11 |
| 24 A04 rate-limiter boundary | P03-S031 (the `rate_limiter` argument not passed; interface only) | P04, P05 |
| 25 Handoffs to A07 | not in P03 | P05 |
| 26 to 28 Whole-topic audit, matches, unknowns | sections 8 to 11 | AUDIT |

## 13. Check log

Checked by a separate read-only helper on 17-Nov-2026 against `970aabf` (filtered `git show`, `git grep` with the four
mandatory exclusions, `git log` and `git blame` with hashes and dates only), the project records under
the project repository (branch main, read-only) and the external pages of sections 1.4 and 1.6, each re-opened.
No legacy file was run, imported, built or tested; no endpoint was contacted; no credential, account, overlay or token
file was opened; no identifier was reproduced; G-19 is not touched.

**Statements checked:** 69 (P03-S001 to P03-S069). Correct without change: 49. Corrected: 20. Withdrawn: 0. Added: 1
(P03-S070).

| ID | What changed | Why |
|---|---|---|
| Header | Status line set to "checked and corrected by a separate helper" | the check procedure |
| Section 1.6 | added: the sources, records and pages read in the check | method record |
| P03-S002 | on an alias miss the symbol is the `stocks` element split and stripped at L670 (case unchanged), not "exactly as received"; L670 cited | imprecise fact |
| P03-S013 | the summary's "refused for at least one window" qualified: not when the key was removed on `QUEUE_FULL` or `STORE_ERROR` | precision (P03-S006) |
| P03-S014 | L730 to L734 cited; the batch is 503 if another symbol is `QUEUE_FULL` or `STORE_ERROR` | precision |
| P03-S024 | HISTORICAL class docstring L75 to L76 ("can't grow unbounded") recorded beside the code | intent text on the same point, recorded neutrally |
| P03-S025 | "the key is the address of the TCP peer" had no authoritative source (P01-S075 says the page does not state it); now cited to waitress 3.0.2 tagged source (`server.py`, `channel.py`, `task.py`: `REMOTE_ADDR` from `channel.addr[0]`, the accepted address) and Werkzeug source (`remote_addr` from `REMOTE_ADDR`); Werkzeug unpinned, version UNKNOWN | external fact without a cited source (the sourcing and labelling rules) |
| P03-S028 | commit `84cee3e` (17-Jul-2026) named for `/health` behind the limiter | precision |
| P03-S031 | enclosing functions named: `_process_one` (L867), `admit_prepared` (L1646), `reject_prepared` (L1706) | precision |
| P03-S034 | KNOWN DEFECT (provisional) kept and brought to the rule: FACT range L934 to L1068 and the absence of any outer `try`/`finally` stated; external context extended (SQLite result codes for reads; CPython mapping of BUSY, LOCKED, IOERR, FULL); failing condition kept and made concrete; effect adds that the later symbols of the batch are not processed; `ShutDown` "Added in version 3.13" with the Python version UNKNOWN; "theoretical" and "realistic" replaced by neutral wording; "This is against the comment ..." (a judgement against intent) replaced by HISTORICAL quotations, adding the docstring L1078 to L1080; the four conditions of the project's KNOWN DEFECT rule (A01 AUDIT section 1.6) stated, (a) and (b) holding by language semantics, (c) and (d) as INTERPRETATION for the AUDIT to confirm | KNOWN DEFECT rule (the sourcing and labelling rules; A01 AUDIT section 1.6); STUDY does not judge against intent |
| P03-S036 | conclusion qualified by a `backpressure_pct` of 0 or more (also unvalidated) | the arithmetic depends on it |
| P03-S038 | one request alone can pass 240 and reach 300; the processor's re-queues add depth with no threshold check; K-11's owners corrected (A02 keys, A20 pre-flight, A06 receiver; handoff row A20), replacing "A20 owns K-11" | completeness; owner misstated |
| P03-S042 | the answers carrying neither header listed in full (4xx, shutting-down 503 L490, 500 L528, EOD L788 and L804) | precision |
| P03-S046 | the facts the INTERPRETATION rests on cited: runtime-metric keys (L274 to L279, `_bump_metric` keys), the dashboard's health URL (`metrics_client.py` L42 to L43; `gui_config.yaml` L42 to L43; effective value UNKNOWN) | unstated basis |
| P03-S048 | K-11 owners as in P03-S038; statement references P03-S038 and P03-S046 | owner misstated |
| P03-S053 | `_shutdown` L1599 cited; the `covered-existing` state sourced to `config/expected_managers.yaml` L149 to L154, with HISTORICAL `acted_means` "a POST audited"; FACT that the census runs before `webhook_receiver.stop()` (L1684 to L1688); INTERPRETATION corrected: every POST that wrote an audit row; requests arriving before `stop()` and the shutting-down 503s after the census are also uncounted | missing source; incomplete interpretation |
| P03-S054 | A03 evidence file named (`evidence/A03_SQL_OUTSIDE_STORE_SCRIPTS_2026-11-09.md`) | precision |
| P03-S055 | `STORE_ERROR` is for INSERT exceptions other than `IntegrityError`; the P-12 link corrected: P-12 concerns the processor's writes under the fund manager's lock, its A06 side (lock scope) is P04's and P05's; the receiver's waits are the same 30-second store wait (P03-S051) | imprecise fact; inherited item mis-mapped |
| P03-S056 | "each EOD alert" limited to alerts passing the body checks (L757 to L774); the receiver's `except` (L830 to L834) catches an import failure at L825 and logs it at WARNING | imprecise; the earlier text implied no case reaches the WARNING |
| P03-S057 | the allocator's thread (`admit_prepared`, `reject_prepared`) added; waitress "Design" page (3.0.2) quoted directly | completeness; official source required by the brief (item 6) |
| P03-S061 | a row for P03-S070 added | consequence of the addition |
| P03-S069 | the unknown tied to the store's 30-second wait; P-12 cited only as the processor-side counterpart | inherited item mis-mapped |
| Section 8 | P-12 row: "A06 side in this part" corrected (not this part's; P04, P05) | inherited item mis-mapped; ID, owners and classification unchanged |
| Section 9 | the P03-S034 point notes the four conditions and adds P03-S070; the census point adds the registry text and the census-before-stop order | consequence of the corrections |
| Section 11 | Q-P03-08 reworded: the registry already states the meaning ("a POST audited"); the question asks about the census timing | the earlier question was answered by a HISTORICAL source |
| Section 12 | P03-S070 added to questions 10, 12 and 14; P03-S034 to question 10 | completeness |

**Statement added:** P03-S070 (section 4.3): the lines L934 to L962, between the claim and the `try`, run outside any
handler, so an exception there also keeps the claims; one source identified: `fp_raw.encode()` at L954 raises
`UnicodeEncodeError` for a symbol carrying an unpaired surrogate, which Python's `json` accepts (Python `json` and
`codecs` pages, 3.15.2, read 17-Nov-2026). INTERPRETATION; not classified; whether it occurred is UNKNOWN.

**Brief coverage (P03.md items 1 to 6 and direction questions 10, 11, 12, 13, 14, 16, 23):** each item is covered
(items 1 to 6 in sections 2 to 7); every listed question has a row in section 12 with its statements. The A02 handoffs
of the A06 entry were reviewed for this part: K-12 is the only one that bears on it (T-07 concerns a strategy field, P04
and P05; K-13 has no consumer, P04); K-11, K-38 and K-50 are A02 rows naming A06 and are recorded. Of the A03 handoffs,
D-08 and R-08 bear on this part, P-12 does not (section 8). The A01 handoffs reviewed (section 1.2) bear on P01, not on
this part.

**Not verified, and why:** `core.ids.new_signal_id` was not examined (outside this part; P03-S011, P03-S070); the
cachetools documentation page for 7.1.1 is not retrievable, so the tagged 7.1.1 source and the 8.0.0 documentation are
used (P03-S005); the Werkzeug source read is the main branch, Werkzeug being unpinned (P03-S025); the receiver lines L260
to L339 were not re-read (no P03 statement cites them); tests were read for names and stated expectations only, never
run (P03-S018, P03-S028); every runtime fact stays UNKNOWN / NOT ESTABLISHED (section 10).
