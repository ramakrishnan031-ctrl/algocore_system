# A06 evidence: signal-event creation, persistence and the handoff to A07

**Status:** APPROVED — evidence for the A06 STUDY, approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37)
**Date:** 2026-11-17
**Revision history:** Revision 1, 2026-11-18: P05-S031 reading (b) reworded after ChatGPT's STUDY review finding M-01 (the called logic stays with A07, A01 and A09; the line stays open). First version, 2026-11-17: written by a read-only helper as STUDY part P05, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude. Approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37): status marked APPROVED; content unchanged.
**Purpose and scope:** When a signal event is created and persisted (receiver and processor); the `signals` table writes, status values, updates through the pipeline, transaction boundaries and failure cases; the evidence recorder P1/P2/P3 capture (A06 side); the exact handoff point to A07 and the contract passed; an interface-only map of every later call-out from `signals/signal_processor.py` (including the late-bound setters and `continue_from_gate` / `continue_from_retest`); the A04 rate-limiter boundary (`try_acquire`). Rama's decision A applies: the logic after the handoff is mapped, not audited (STUDY part P05).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only, through `git show`)

- `signals/signal_processor.py` (2,703 lines): the function list in whole (`ast.parse` of the text, nothing run);
  read in full L1 to L1830, L1895 to L2070, L2095 to L2140, L2230 to L2412, L2436 to L2456, L2536 to L2682; the other
  lines through the search hits of section 1.3.
- `signals/webhook_receiver.py`: L672 to L730, L888 to L935, L948 to L1075 (event creation only; the rest is P01 to
  P03's).
- At the boundary (other owners; only the methods, columns and lines A06 code uses): `core/state_store.py` L205 to
  L240, L506 to L548, L1400 to L1430 (A03); `core/schema.sql` L38 to L82 (A03); `core/ids.py` L40 to L60 (A01);
  `core/exceptions.py` class lines L158, L215, L243, L261, L284 (A01); `core/evidence_contract.py` L1 to L180, L296 to
  L340, L420 to L670 and its function list (A15); `screening/secondary_screener.py` L40 to L56, L123 to L150, L600 to
  L680 (A07); `screening/retest_monitor.py` L200 to L212, L340 to L376 (A08); `orders/order_manager.py` L700 to L735
  and `orders/order_placer.py` L1464 to L1478, L4400 to L4412 (A10); `capital/shadow_engine.py` L1 to L30, L95 to L110
  (A09); `scripts/eod_cleanup.py` L95 to L135 (outside A06); `config/system_config.yaml` lines found by search (L302,
  L509, L529, L565, L574; A02).
- `main.py` (A01's file; A06 call sites only): L850 to L895, L2378 to L2388, L2980 to L2987, L3240 to L3300, L3486 to
  L3500, L3540 to L3560, L3600 to L3622, L3624 to L3710, L3765 to L3805, L3836 to L3850, L4215 to L4235; and the
  `SignalProcessor(...)` call block at `31075d0`, `686df1c` and `970aabf` (searched for `rate_limiter`).

### 1.2 Project records and working inputs read (algocore_system, branch `main`, read-only)

- The working rules, the P05 brief and the A06 investigation direction (17-Nov-2026), section 4.
- Topic Completion Register, A06 entry; Decision Register, D-21; Open Issues Register, row A04-33.
- Master System Investigation Index: entries A01, A04, A06, A07, A08, A09, A10, A11, A13, A14, A15 and A18 (Paths and
  Boundary lines).
- A04 RECONCILED TOPIC RECORD sections 4.7, 6 (row 14), 15.2 and 22.2; A04 AUDIT rows RL-18 and the rate-limit rules
  row, and entries CS-03, CS-05, CS-08, RL-14 and RL-16.
- A03 RECONCILED TOPIC RECORD section 15.2; A03 AUDIT entries P-02, P-11, P-12, Q-11 and R-08.
- The checked parts P01 to P04 (statements cited by ID; their content is not repeated).

### 1.3 Commands and search patterns (all read-only)

`git show 970aabf:<path>`; `git grep -n -E` with the four exclusions (through the fieldwork's read-only search helper for
non-test code); `git blame -s -L` (hashes only); `git log --format='%h %ad %s' --date=short` with `-S` and ranges;
`ast.parse` of source text. Patterns: `update_signal_status\(`, `UPDATE signals|INSERT INTO signals|DELETE FROM
signals|FROM signals`, `_PipelineReject\(`, `_evidence_capture\(`, `EvidenceRecorder|evidence_recorder|"P1_ACCEPT"|
"P2_REJECT"|P3_[A-Z]+`, `'TRADED'|"TRADED"`, `set_shadow_engine|ShadowEngine\(`, `set_allocator|set_v3_chain|
set_retest_diverter|continue_from_gate|continue_from_retest|admit_prepared|reject_prepared`, `rate_limiter|
try_acquire|RateLimiter|\.acquire\(` (in `signals/` and the Appendix A script), `\brate_limiter\b` (in `main.py`),
`FIX-007`, `link_signal_trade\(`, `release_gate_state\(|release_retest_state\(`, `EntryGate.add`-style callers,
`ALTER TABLE signals`, `received_at|expires_at|fingerprint|webhook_payload|fetch_one|fetch_all` (in the processor),
`_active_workers`, `one_trade_per_symbol_direction`, the collaborator attributes (`self._fm.`, `self._risk.`, and so
on). The commits after the last recorded deployment were listed with `git log 7d4970a..970aabf` on the four files
concerned.

### 1.4 External pages read (current external context, read 17-Nov-2026)

- Python documentation, `sqlite3` (https://docs.python.org/3/library/sqlite3.html): `timeout`, `isolation_level`
  (`None`: "transactions are never implicitly opened"), `check_same_thread`.
- SQLite documentation, "BEGIN TRANSACTION" (https://www.sqlite.org/lang_transaction.html): `BEGIN IMMEDIATE`,
  `COMMIT`, implicit transactions.
- Added in the check (read 17-Nov-2026): Python documentation, `uuid` (https://docs.python.org/3/library/uuid.html):
  `UUID.hex`; Python documentation, `queue` (https://docs.python.org/3/library/queue.html): `put`, `put_nowait`;
  Python Language Reference, "The try statement" (https://docs.python.org/3/reference/compound_stmts.html). The two
  sources above were re-opened and their quotes confirmed.
The installed Python and SQLite versions are not pinned (P04-S063) and are UNKNOWN / NOT ESTABLISHED.

### 1.5 Labels and limits

Labels as in the working rules. No legacy file was run, imported or tested; no endpoint, scanner or broker was
contacted; no credential file, overlay or effective setting was opened; the evidence arm value and account files were
not read; G-19 is not cited. Security note: one `git show --stat` of a commit printed an identifier-bearing line (not
reproduced); filter replacements inside printed code (a hash-algorithm name, lint codes, a test-file name) were false
positives and are not quoted.

## 2. When the signal event is created (receiver side)

P05-S001. FACT (`signals/webhook_receiver.py` L676 to L679, L719 to L723, L892 to L902, L956 to L980, L1047 to L1049,
L1072; P01-S041, P02-S070, P03-S055): the signal event, in the only durable form A06 gives it, is one row of the
`signals` table. It is created by the receiver, on the request thread, inside `_process_signal`, after the per-symbol
checks (symbol, price, age, in-flight claim, TTL cache; P02, P03) and before the queue put. The receiver first takes
a new identifier `signal_id = new_signal_id()` (L957), then runs one INSERT in its own `with self._store.transaction()`
(L963 to L980), and only after that INSERT has committed does it build the queue item (L1047) and call `put_nowait`
(L1049). On the M-S2 re-accept route no row is created: an existing `QUEUE_FULL` row is reused with its `signal_id`
(L992 to L1013; P03-S012, P04-S064). No other A06 code path creates a `signals` row.

P05-S002. FACT (`core/ids.py` L38, L50 to L52; `signals/webhook_receiver.py` L957): the identifier is the text `sig_`
(`_PREFIX_SIGNAL`, L38) followed by `uuid.uuid4().hex`. Current external context (Python documentation, `uuid`,
https://docs.python.org/3/library/uuid.html, read 17-Nov-2026: `UUID.hex` is "The UUID as a 32-character lowercase
hexadecimal string"); INTERPRETATION: so the identifier is `sig_` plus 32 lower-case hexadecimal characters, as the
docstring L51 also says. It is created once per symbol that reaches the INSERT and is the key that every later write
and the queue item carry.

P05-S003. FACT (`signals/webhook_receiver.py` L958 to L961, L966 to L979, L677 to L679, L688 to L690; `core/schema.sql`
L42 to L79, A03's file, read at the boundary): the INSERT writes 12 of the table's 14 columns:

| Column | Value written | Source line |
|---|---|---|
| `signal_id` | the new `sig_` identifier | L957 |
| `symbol` | the symbol after the alias map (not upper-cased on an alias miss; P02-S059) | L701, L975 |
| `scanner` | the URL path segment `scanner_name` | L975 |
| `strategy` | the same path segment (P01-S043) | L975 |
| `triggered_at` | `triggered_at.isoformat()` (IST-aware as parsed; P02-S055) | L958 |
| `received_at` | `now_ist()` taken once per request, before the per-symbol loop, in ISO form | L677, L959 |
| `expires_at` | `received_at + expiry_sec` (`signal_queue.expiry_sec`), in ISO form | L679, L960 to L961 |
| `status` | the literal `QUEUED` | L977 |
| `fingerprint` | a hash of the scanner name, the symbol and the epoch bucket, joined by a vertical bar (P03) | L952 to L954 |
| `fingerprint_date` | `today_iso`, the date of `received_at` | L678 |
| `trigger_price` | the request price as a `float` | L910, L977 |
| `webhook_payload` | the sanitized raw body (P02 section 2.5; S-1B.1 comment L681 to L687) | L688 to L690, L978 |

The two columns not written are `rejection_reason` and `trade_id` (both nullable, so NULL at creation). No
`ALTER TABLE signals` exists anywhere in the repository (search), so the 14 columns of `core/schema.sql` are the whole
table at `970aabf`; it has no column for the time of a status change (A03 P-02, quoted in section 3). The `status`
CHECK (L60 to L70) admits a fixed list plus the prefix families `REJECTED*`, `DROPPED_*`, `SKIPPED_*`, `GATE_*` and
`RETEST_*`. INTERPRETATION: `received_at`,
`expires_at` and `fingerprint_date` are the same for every symbol of one request, because `received_at` is taken once
per request (L677).

P05-S004. Current external context (Python documentation, `sqlite3`, read 17-Nov-2026: `isolation_level=None`
"transactions are never implicitly opened"; `timeout`: "How many seconds the connection should wait before raising an
OperationalError when a table is locked"; SQLite documentation, `lang_transaction.html`, read 17-Nov-2026: "IMMEDIATE
causes the database connection to start a new write immediately, without waiting for a write statement. The BEGIN
IMMEDIATE might fail with SQLITE_BUSY if another write transaction is already active on another database connection").
FACT (`core/state_store.py` L107 to L113, L215 to L242, L506 to L543; A03's file, at the boundary): every store
connection is opened per thread with `isolation_level=None` and `timeout=30`, and each new connection also runs
`PRAGMA busy_timeout = 30000` (L112, comment "Wait up to 30s on a locked DB (FIX-006)"); `transaction()` runs
`BEGIN IMMEDIATE`, yields the cursor, then `COMMIT`; on any exception it tries `ROLLBACK` and re-raises. INTERPRETATION: the INSERT is committed
before the queue put, so a queued item always has a committed row behind it on the normal route; if the INSERT fails,
nothing is queued and the symbol is answered `STORE_ERROR` or, for an `IntegrityError`, routed as P03-S010 records.
The SQLite library version used is UNKNOWN / NOT ESTABLISHED (no pin; P04-S063 for Python).

P05-S005. INTERPRETATION (P05-S001, P05-S004; P04-S020; current external context, Python documentation, `queue`,
https://docs.python.org/3/library/queue.html, read 17-Nov-2026: `put_nowait(item)` is "Equivalent to
`put(item, block=False)`", which puts the item "if a free slot is immediately available, else raise the `Full`
exception"): between the INSERT's commit (end of the `with` block, L964 to L980) and the queue put (L1049)
the row is `QUEUED` with no queue item; if the process stops in that window the row stays `QUEUED` with no item and no
code re-reads it (P04-S020). If the put raises `queue.Full`, the row is set `QUEUE_FULL` in a second transaction (L1052
to L1057; P03-S055); if that UPDATE fails, the row stays `QUEUED` with no item, and the failure is logged at ERROR
(L1058 to L1059). Whether any of these occurred is UNKNOWN / NOT ESTABLISHED.

P05-S006. FACT (`signals/webhook_receiver.py` L1047 to L1049; P01-S042, P04-S024): the event that A06 hands on is not
the row but the in-memory 5-tuple `(signal_id, scanner_name, symbol, price, triggered_at)`; the row's other columns
(`received_at`, `expires_at`, `fingerprint`, `webhook_payload`) are not in the item and are not read back by the
processor (search of `signals/signal_processor.py` for `received_at`, `expires_at`, `fingerprint` and `webhook_payload`:
no hits). The processor never reads the `signals` table at all (search for `FROM signals` and `fetch_one`/`fetch_all`
on `signals` in the file: none; its only `fetch_one` reads `trades`, L761 to L767).

## 3. The `signals` status writes through the pipeline

### 3.1 The write method (A03's) as A06 code uses it

P05-S007. FACT (`core/state_store.py` L1408 to L1426; A03's file, read at the boundary): every processor write to
`signals` goes through `update_signal_status(signal_id, status, reason="", ts="")`, which runs one
`UPDATE signals SET status = ?, rejection_reason = ? WHERE signal_id = ?` in its own `transaction()` (P05-S004), with
`reason if reason else None`; `ts` is accepted and not stored (parameter comment L1413). There is no predicate on the
current status, and the method does not read `rowcount`. HISTORICAL (L1416 to L1420): "Called at every state change in
the processing pipeline so every signal_id has a terminal status + reason for audit purposes. No-op if signal_id does
not exist". HISTORICAL (processor docstring L21): "SP9 -- Signal status written to state_store at each state change".
A03 recorded the method side as P-02 (A03 AUDIT, "`update_signal_status` discards the status time stamp that SP9 and
P16 require"; Owner: "A03 (the method); A06 (the pipeline's status sequence and whether a final status can be
overwritten)"); this part records the A06 sequence; P-02's ID, owners and classification are unchanged.

P05-S008. FACT (search of `signals/signal_processor.py` for `update_signal_status`): the processor writes `signals`
only through that method, at 26 call sites, never with the `ts` argument, and it never writes `trade_id` or any other
column. INTERPRETATION (P05-S007): a write without a reason (`PROCESSING`, `RESERVED`, `PROCESSED`,
`PROCESSED_NO_PLACER`) sets `rejection_reason` to NULL, so it clears any reason stored by an earlier write; every write
replaces the stored status whatever it was.

### 3.2 The processor's writes, in pipeline order (FCFS path, `_process_one` and `_admit_and_place`)

P05-S009. FACT (lines as cited; `capital/fund_manager.py` is A09's, its lock is used at the interface only): the
status values the FCFS path writes, in order, with the reason, the place and whether the fund manager's
`portfolio_lock` is held:

| # | Line | Status written | Reason written | When | `portfolio_lock` held |
|---|---|---|---|---|---|
| 1 | L897 | `PROCESSING` | none (NULL) | first statement inside the worker's `try`, before any check | no |
| 2 | screener (A07) | `PASSED`, `REJECTED_<step>` or `SKIPPED_<reason>` | `rejected_step` or the status | inside `screen()` (P05-S012) | no |
| 3 | L1344 | `RESERVED` | none (NULL) | after `self._fm.reserve(...)` succeeded and `ac.reservation_id` was set (L1340) | yes (L1307 to L1344) |
| 4a | L1360 | `PROCESSED_NO_PLACER` | none (NULL) | `order_placer` is `None`, after the reservation is released (L1356) | no |
| 4b | L1480 to L1482 | `TIMEOUT` | `str(timeout_err)` | `place()` raised `BrokerTimeoutError` | no |
| 4c | L1543 | `PROCESSED` | none (NULL) | `place()` returned | no |
| R | L1201 | `REJECTED_<check>` | `rej.reason` | any `_PipelineReject` (section 3.4) | no (the handler runs after the `with` block has exited) |
| E | L1238 | `PLACEMENT_FAILED` | `str(exc)` | any other `Exception` in the `try` | no |
| W | L473 to L475 | `PLACEMENT_FAILED` | `unhandled: <exc>` | an `Exception` that leaves `_process_one` (P04-S025, P04-S055) | no |
| Q | L435 to L437 | `REJECTED` | `QUEUE_FULL` | FIX-007 branch only; never under `main.py` (P04-S053; section 9) | no |

FACT (L1486 to L1525): the FIX-069 re-queue (a `BrokerRateLimitError` with `retry_count < 3`) writes no status; the
row keeps `RESERVED` while the reservation is released (L1522 to L1524) and the item waits in the queue; the retry's
worker writes `PROCESSING` again (L897). FACT (L1042 to L1056): the retest divert writes nothing in the processor; the
parked status is written by A08's code (P05-S012).

P05-S010. FACT (L1307 to L1344; A03 P-12, quoted): write 3 is the only FCFS `signals` write made while
`portfolio_lock` is held (inside the lock the processor also reads the store, L761 and L855, and A09's `reserve()`
writes its own ledger, A03 P-11).
A03 recorded "three `update_signal_status` calls ... run lexically inside the lock" (L1307 to L1344, L2138 to L2171,
L2474 to L2501) and the 30-second store wait as P-12 ("UNKNOWN: store waits of up to 30 seconds while the fund
manager's re-entrant lock is held"; Owner: "A03 (lock wait); A06, A09 (lock scope)"). A06-side FACT: the three are the
`RESERVED` writes of the FCFS, gate and retest paths (L1344, L2171, L2501); each is the last statement inside the
`with` block, after `reserve()`. HISTORICAL (L1342 to L1343): "kept inside the lock so the SQL row appears atomically
with the reservation entry". A03 P-11 (quoted in P05-S021) records that the reservation's ledger row and the
`RESERVED` status are two transactions. P-12's classification is unchanged.

### 3.3 The other paths of the processor

P05-S011. FACT (lines as cited): the gate resume `continue_from_gate` writes `PROCESSING` (L2034), `RESERVED` inside
the lock (L2171), `PROCESSED_NO_PLACER` (L2186), `TIMEOUT` (L2278 to L2280), `PROCESSED` (L2290), `REJECTED_<check>`
(L2316 to L2318) and `PLACEMENT_FAILED` (L2345); the retest resume `continue_from_retest` writes `PROCESSING` (L2393),
`RESERVED` inside the lock (L2501), `PROCESSED_NO_PLACER` (L2509), `TIMEOUT` (L2573), `PROCESSED` (L2583),
`REJECTED_<check>` (L2598) and `PLACEMENT_FAILED` (L2620); the allocator's `admit_prepared` writes `REJECTED_<check>`
(L1662) and `PLACEMENT_FAILED` (L1683) around the shared `_admit_and_place` (whose writes are rows 3 to 4c), and
`reject_prepared` writes `REJECTED_<reason>` with reason `allocator pre-check: <reason>` (L1712 to L1713). Neither
resume path, nor `admit_prepared`, has a wrapper like `_process_one_safe`; their callers are in section 8.

### 3.4 Status values and the schema CHECK

P05-S012. FACT, interface only (`screening/secondary_screener.py` L604 to L620, A07's; `screening/entry_gate.py`
L312, L512, A07's; `screening/retest_monitor.py` L349, L373, L209, A08's; `core/state_store.py` L2982 to L2998,
L3049 to L3059, A03's; `orders/order_manager.py` L718 to L724 with its caller `orders/order_placer.py` L1028, A10's):
the other in-process writers of a signal's row after the receiver are: the screener (`update_signal_status` with
`result.status`, reason `result.rejected_step or result.status`, inside a `try` that logs and swallows a failure,
"DB failure is logged but never raised", L605 to L606); the entry gate (`GATE_WAITING`; the release through
`release_gate_state`); the retest diverter in the same file (`REJECTED_RETEST_DUP` for a symbol already parked, L349 to L351, and `RETEST_WAITING`, L373; the release through
`release_retest_state`); and the order manager's `link_signal_trade`, which sets `signals.trade_id` from the order
placer. Their status logic is their owners'. A03 R-08 (the receiver's re-queue flip) is P03's (P03-S012) and P04's
(P04-S064).

P05-S054. FACT (`screening/secondary_screener.py` L611, L615 to L620, A07's file, interface only; `core/state_store.py`
L1413, A03's; added in the check): the screener's call passes `ts=ts` (an IST ISO time taken at L611), which the store
method accepts and does not store (P05-S007); the processor's 26 calls pass no `ts` (P05-S008). HISTORICAL (A03 AUDIT,
P-02, "Actual behaviour and effective value"): "`ts` is accepted and unused, and no caller passes it (grep of the 32
calls)". INTERPRETATION: A03's wording "no caller passes it" does not match the screener's call; the effect recorded by
P-02 (no status time is stored) is unchanged. P-02's ID, owners and classification are not changed here; the point is
noted for the coordinator.

P05-S013. FACT (`signals/signal_processor.py` L94 to L100, L1201; the reject sites listed by a search for
`_PipelineReject(`; `core/schema.sql` L60 to L70): every processor reject is written as `REJECTED_` plus the check
label; the labels the processor raises itself are `KILL_SWITCH`, `OUTSIDE_ENTRY_WINDOW`, `EXPIRED`,
`SHADOW_INNING_ACTIVE`, `SHADOW_TRACKER_ERROR`, `UNKNOWN_STRATEGY`, `TRADE_TYPE` (the constant `CAUSE_TRADE_TYPE`,
L970), `STRATEGY_CONTROL`, `STRATEGY_CIRCUIT_BREAKER` (intake; P04-S035), and after the handoff `INVALID_DERIVED_PRICE`,
`ZERO_SL`, `REJECTED_NO_ATR_DATA` (L1805, L1916), `UNKNOWN_TGT_METHOD`, `TGT_DISTANCE_TOO_SMALL`,
`SIZING_BROKER_ERROR`, `STRATEGY_POSITION_LIMIT`, `SYMBOL_DIRECTION_DAILY_LIMIT`, `RISK_BROKER_ERROR`,
`RESERVE_BROKER_ERROR`, `RESERVE_FAILED`, `KILL_SWITCH_LATE`, `SHUTDOWN`, `ENTRY_THROTTLED` and `RETEST_BAD_STRUCTURE`
(retest only); two families come from collaborators: `SIZING_<sizing.constraint>` (A09's sizer, L1128) and
`<approval.failed_check>` (A09's risk engine, L1325). All fall under the CHECK's `GLOB 'REJECTED*'`.
INTERPRETATION: the label `REJECTED_NO_ATR_DATA` is written as `REJECTED_REJECTED_NO_ATR_DATA` (L1201 adds the prefix
again); it is raised only when an ATR method meets `atr_fallback_mode == "HALT"` (L1803 to L1806, L1913 to L1918),
whose code default is `"WARN"` (processor L177; `core/config_loader.py` L572, A02's; `main.py` L3593 passes
`sp_cfg.atr_fallback_mode`) and which the committed file does not set (search; P04-S003), so it is not reached at the
committed values.

P05-S014. FACT (search of non-test code for `'TRADED'` and `"TRADED"`): no code writes the status `TRADED`, although
the schema lists it (L63) and readers count it (for example `scripts/healthcheck_server.py` L172,
`reports/signal_status.py` L40, `reports/daily_report.py` L483, L711, L1558, `reports/daily_trade_review.py` L737; A15's,
interface only); the other non-test hits are a label in `reports/daily_trade_review.py` L847, a CSV header in
`scripts/generate_screened_stocks_csv.py` L209 and L294, a docstring example read in `core/state_store.py` L161 and a
parameter default of `capital/shadow_engine.py` L103; none writes a `signals` row (the non-test writers of `signals`
found by a search for `UPDATE signals` and `update_signal_status(` are the receiver, the processor, the screener, the
entry gate, the retest diverter and monitor, the order manager's `trade_id` link and `scripts/eod_cleanup.py`). The processor's success status
is `PROCESSED` (L1543, L2290, L2583) and the link to a trade is the `trade_id` column (P05-S012).
INTERPRETATION: a reader that counts `TRADED` rows finds none written by the code at `970aabf`; whether earlier code or
other processes wrote it is outside this part (A15 for the readers).

P05-S015. FACT (`core/schema.sql` L50, L60 to L70; search for each value as a quoted literal in non-test code): of the
CHECK's fixed values, those written by A06 code are `QUEUED`, `QUEUE_FULL` (receiver), `PROCESSING`, `RESERVED`,
`PROCESSED`, `PROCESSED_NO_PLACER`, `PLACEMENT_FAILED` and `TIMEOUT` (processor); the bare `REJECTED` of the unwired
FIX-007 branch and every `REJECTED_...` value fall under `GLOB 'REJECTED*'`. The receiver's per-symbol answers `DUPLICATE`, `EXPIRED`, `INVALID_SYMBOL`, `INVALID_PRICE` and
`IN_PROCESS` write no row (P02-S070); nor do `REJECTED_EXCLUDED_SYMBOL` (the request loop, `signals/webhook_receiver.py`
L708 to L717, before `_process_signal`) and `STORE_ERROR` (the INSERT failed and was rolled back, L1016 to L1044). HISTORICAL (L50): the column comment lists
"QUEUED/PASSED/PROCESSED/REJECTED*/GATE_*/DROPPED_*/SKIPPED_*" and does not name `PROCESSING`, `RESERVED` or
`TIMEOUT`, which the CHECK admits.

## 4. When persistence fails, and when the process stops between steps

### 4.1 A failing status write

P05-S016. FACT (L895 to L897, L1233 to L1246, L1248 to L1276, L465 to L477; the Python `try` semantics of P05-S053):
if the `PROCESSING` write (L897) raises,
no check runs; the exception is caught at L1233, which logs ERROR "Pipeline exception for ..." and writes
`PLACEMENT_FAILED` (L1238). If that write also raises, the exception leaves the handler; the `finally` still releases
the receiver's claim (L1267 to L1271), and `_process_one_safe` logs "Unhandled exception in pipeline" and tries
`PLACEMENT_FAILED` a third time, swallowing any error (L472 to L477). INTERPRETATION: when the store refuses writes,
the row keeps `QUEUED`; when only the first write fails (for example a lock wait that ends in `OperationalError` after
the 30 s of P05-S004), the row can read `PLACEMENT_FAILED` for a signal that never reached a check or the broker.

P05-S017. FACT (L1193 to L1231): in the reject handler the status write (L1201) is the first statement after the log
line and the metric; if it raises, the `P2_REJECT` capture, the reservation release (L1212 to L1217), the per-check
count and the `EXPIRED` alert are skipped; the `finally` runs; `_process_one_safe` then tries `PLACEMENT_FAILED`.
FACT (L1340, L1368, L1901 to L1953, L1389 to L1418): the rejects that can be raised while `ac.reservation_id` still
holds a reservation are the three target labels of `_derive_target` (L1368: `UNKNOWN_TGT_METHOD`,
`TGT_DISTANCE_TOO_SMALL`, `REJECTED_NO_ATR_DATA`); `KILL_SWITCH_LATE`, `SHUTDOWN` and `ENTRY_THROTTLED` release the
reservation themselves before they raise (L1393 to L1395, L1402 to L1404, L1412 to L1414), with calls not guarded by
any `try`; if such a release raises, the reject is not raised, the exception reaches the handler at L1233 with
`ac.reservation_id` still set, and that handler writes `PLACEMENT_FAILED` and calls a release again. INTERPRETATION: a
target reject whose status write fails leaves its reservation unreleased by the processor; what then happens to it,
and what a repeated release does, is A09's.

P05-S018. FACT (L1328 to L1344, L1188 to L1191, L1233 to L1243): if the `RESERVED` write (L1344) raises, the exception
leaves the `with portfolio_lock` block and `_admit_and_place`; `ac.reservation_id` was set at L1340, the `finally` at
L1188 copies it to `reservation_id`, and the handler at L1233 writes `PLACEMENT_FAILED` and calls
`self._fm.release(reservation_id, "placement_failed")`. FACT (L1238 to L1243): the handler's `PLACEMENT_FAILED`
write comes before that release; if the write raises (for example because the store is still refusing writes), the
release is skipped, the exception leaves the handler, and `_process_one_safe` (L467 to L477) tries only a status write,
not a release. INTERPRETATION: on the A06 side the reservation is released by the same worker only if the
`PLACEMENT_FAILED` write and the release both succeed; otherwise the processor leaves it held (A09 for what follows).
The window in which the ledger holds a reservation for a row not marked `RESERVED`, recorded by A03 P-11 point (3),
lasts at least until that release. The same order (status write, then release) holds in every generic handler that
releases (L1238 to L1243, L1683 to L1688, L2345 to L2352, L2620 to L2625).

P05-S019. FACT (L1446 to L1484, L1461, L1483, L1233 to L1243): when `place()` raises `BrokerTimeoutError`, the
handler calls `self._ks.record_api_failure(timeout_err)` (L1478 to L1479), writes `TIMEOUT` (L1480 to L1482) and only
then sets `ac.reservation_id = None` (L1483); `ac.reservation_id` still holds the reservation, because L1461 runs only
after `place()` returns. HISTORICAL (L1465 to L1477): "relinquish the reservation handle WITHOUT releasing it
(recovery owns it — SINGULAR ownership)". INTERPRETATION (P05-S053): if either the kill-switch call or the `TIMEOUT`
write raises, that exception, raised inside the `except BrokerTimeoutError` clause, is not handled by the sibling
clauses and reaches the handler at L1233 with the reservation still set, and that handler writes
`PLACEMENT_FAILED` and releases the reservation as `"placement_failed"`: the outcome the comment says must not happen.
The gate and retest paths have the same order (L2276 to L2281, L2571 to L2576). Whether it occurred is UNKNOWN / NOT
ESTABLISHED. The A04 side of the timeout chain is A04 CS-03 and CS-08 (section 10).

P05-S020. FACT (L1446 to L1463, L1540 to L1547, L1233 to L1246): if `place()` returns and the `PROCESSED` write
(L1543) raises, the handler at L1233 writes `PLACEMENT_FAILED` with the store error as reason (no reservation is then
held: L1461) and counts `PLACEMENT_FAILED` in `_stats`; the S&R observer (L1550) is not called; the `entries_placed`
metric was already counted (L1463). INTERPRETATION: the row can then read `PLACEMENT_FAILED` for an order that was
handed to the placer and not refused by it.

P05-S021. FACT, interface only (`screening/secondary_screener.py` L604 to L637, A07's): the screener's own status
write is inside a `try` that logs ERROR and continues; the processor then acts on the returned result (L1008 to
L1022). INTERPRETATION: if the screener's write fails, the row keeps `PROCESSING` while the worker continues (to
sizing on `PASSED`, or to the `finally` on a reject); a rejected signal can then stay `PROCESSING` in the table.
A03 P-11 (quoted; its ID, owners and classification unchanged): "(3) Signal reservation: the reservation's ledger row
and the RESERVED status are two transactions; a failure of the status UPDATE leaves a reservation for a signal not
marked RESERVED, and readers without the lock (other processes) can see one without the other, so "appears
atomically" holds only for holders of the lock." (Owner: "A03 (the per-call transaction boundary); ... A06
(reservation status)".)

### 4.2 A stop between steps

P05-S022. INTERPRETATION (P05-S009; P04-S019, P04-S020; FACT: no processor write is made in a transaction with any
other write): a hard stop leaves the row at the last status committed before it: `QUEUED` (queued, or in the
executor's work queue, not started), `PROCESSING` (started, before or during screening), the screener's `PASSED`
(screened, before sizing or the reservation), `RESERVED` (reserved, before or during placement), or a parked
`GATE_*`/`RETEST_*` status (A07, A08). FACT, interface only (`scripts/eod_cleanup.py` L105 to L127, outside A06):
the end-of-day cleanup sets `EXPIRED` only on rows still `PROCESSING` with an earlier `triggered_at` date; rows left
`QUEUED`, `PASSED` or `RESERVED` are not touched by it, and no start-up code re-reads `signals` rows (P04-S020). What
happens at a restart to a reservation or a broker order made before the stop is A09's, A10's and A12's.

P05-S023. INTERPRETATION (P05-S009 rows 3 to 4c; P04-S019): a stop during placement can leave a row `RESERVED` for a
signal whose order may have been sent; the processor writes nothing that marks "sent to the broker" before `place()`
returns (the `P1_ACCEPT` evidence record, P05-S026, is written to a file, not to `signals`). The trade-level status
(`PENDING`, `UNKNOWN_IN_FLIGHT`) is the order placer's (A10; A04 CS-05 and CS-08).

### 4.3 The reservation when `place()` raises

P05-S052. FACT (processor L1340, L1446 to L1461, L1533 to L1538, L1188 to L1191, L1239 to L1243; the gate and retest
paths L2251 to L2267, L2283 to L2288, L2346 to L2352 and L2553 to L2563, L2578 to L2581, L2621 to L2625;
`orders/order_placer.py` L1466 to L1475 and L4400 to L4404, A10's file, interface only): the processor clears its
reservation handle only after `place()` returns (L1461); when `place()` raises any exception other than
`BrokerTimeoutError` and a re-queued `BrokerRateLimitError`, the handle is still set and the processor's handler calls
`self._fm.release(reservation_id, "placement_failed")` after its `PLACEMENT_FAILED` write (skipped if that write
raises, P05-S018). The placer's own `BrokerError` handler calls
`_handle_placement_failure(trade_id, reservation_id, signal_id, exc, ...)`, whose docstring says it will "release
capital reservation", and then re-raises. INTERPRETATION: for such a `BrokerError`, both the placer and the processor
call a release for the same reservation; what a second release does is A09's (the fund manager) and whether the
placer's release runs in each case is A10's (A04 CS-05 records that `ValueError` and `RateLimitAbortedError` skip the
placer's failure path, so for those only the processor's release runs).

### 4.4 Language semantics used in sections 4.1 to 4.3 (added in the check)

P05-S053. Current external context (Python Language Reference, "The try statement",
https://docs.python.org/3/reference/compound_stmts.html, read 17-Nov-2026): "When an exception occurs in the `try`
suite, a search for an exception handler is started." "If `finally` is present, it specifies a 'cleanup' handler. The
`try` clause is executed, including any `except` and `else` clauses. If an exception occurs in any of the clauses and
is not handled, the exception is temporarily saved. The `finally` clause is executed. If there is a saved exception it
is re-raised at the end of the `finally` clause." INTERPRETATION (for P05-S016 to P05-S020, P05-S052): an exception
raised inside one of the processor's `except` clauses (a failing status write or release in a handler) is not handled
by the other `except` clauses of the same `try`; the `finally` of that `try` still runs, and the exception then passes
to the enclosing `try` (in `_process_one`, to `_process_one_safe`, L465 to L477). The installed Python version is
UNKNOWN / NOT ESTABLISHED (P04-S063).

## 5. The evidence recorder's P1, P2 and P3 capture (A06 side only)

P05-S024. FACT (Master System Investigation Index, entry A15, Paths: "`core/evidence_contract.py`;
`core/effect_telemetry.py`"; `main.py` L3248 to L3279, L3297, L3622): the recorder is A15's module; A06 holds only its
call sites in the processor. `main.py` builds one `EvidenceRecorder(Path(__file__).resolve().parent,
config_hashes=app_config.file_hashes, logger=..., critical_sink=notifier_critical_sink(notifier))` inside a `try`; if
the construction raises, `evidence_recorder = None`, an ERROR line is logged and a CRITICAL notification
"[EVIDENCE] RECORDER_NOT_BUILT" is attempted, and start-up continues. The same object is passed to the screener
(`evidence=`, L3297, "Batch 1: P3 capture") and to the processor (`evidence=`, L3622, "Batch 1: P1 + P2 capture");
`enabled` is not passed, so its default `True` applies (`core/evidence_contract.py` L439).

P05-S025. FACT (`git log` and `git blame` at `970aabf`): the recorder and its wiring come from commits of 10 and
11-Sep-2026: `d2aa35d` (the recorder), `8d27fdb` (wiring of P1, the P2 reject paths and P3; also the processor's
`evidence=` parameter, L197, L241), `ea0e506` (the guarded construction in `main.py`, L3257 to L3266), `d646347`,
`23d2be7` (the `reanchored` field), `853a3a1` (the FIX-007 `QUEUE_FULL` capture), `3fc1d2e` (P1 on the gate and
retest paths) and `056905b` (the required P2 identity; `_evidence_strategy_for`, L560 to L580); on the screener's side
(A07's file) `02d1e3f` moved the P3 capture outside the screener's DB `try` (P05-S027). All are later than
the last recorded deployment (`686df1c` and `7d4970a`, 02-Sep-2026; Decision Register D-21). Whether production ran
any of them is UNKNOWN / NOT ESTABLISHED; HISTORICAL: the message of `853a3a1` says "Batch 1: NOT deployed to either
VM" (P04-S053), and comments speak of reject figures from production: the processor's docstring "measured on
production, 4,168 of 48,934 P2 rejects" (L565 to L566) and the recorder's "MEASURED ... Production, 12-Jun..10-Sep:
48,934 P2 rejects" (`core/evidence_contract.py` L95 to L99); these describe a corpus counted by other means and are not
evidence that the recorder ran there.

P05-S026. FACT (`signals/signal_processor.py` L582 to L612, L1420 to L1445, L2235 to L2250, L2538 to L2552): `P1_ACCEPT`
is emitted once per placement dispatch, inside the `try` that calls `place()`, immediately before it: on the FCFS path
after the effect-telemetry counter `self._fx_dispatch.inc()` (L1423), and on the gate and retest paths without that
counter (their comment at L213 to L216 calls them "production-unreachable and deliberately uncounted"). The FCFS
payload carries `signal_id`, `symbol`, `strategy`, `triggered_at`, `status: "ACCEPTED"`, `score_total` (the
screener's `score`), `tier`, `step_results`, `step_statuses` and `market_data_snapshot`, `trigger_price`, `entry_price_final`,
`reanchored` (from `ac.reanchored`, set from the M-S1 re-anchor flag L1081, L1101, L1180), `sl_price`, `tgt_price`,
`qty`, `sizing_breakdown` and `binding_constraint`. The `ACCEPTED` value is written only to the evidence file; the
`signals` row is not changed at this point (it stays `RESERVED` until P05-S009 row 4b, 4c or E, or, on the FIX-069
re-queue, until the retry's `PROCESSING`). The gate and retest P1 payloads (L2241 to L2250, L2543 to L2552) carry no
`triggered_at`, no `score_total`, step or market-data fields, and `reanchored: None`.

P05-S027. FACT (L443 to L455, L1202 to L1211, L1663 to L1672, L1716 to L1727, L2319 to L2328, L2599 to L2606):
`P2_REJECT` is emitted after the reject's status write in six places: the unwired FIX-007 `QUEUE_FULL` branch, the
FCFS reject handler, `admit_prepared`'s reject handler, `reject_prepared`, and the gate and retest reject handlers.
Each carries `signal_id`, `symbol`, `strategy`, `trigger_price`, `status` (the same `REJECTED_...` value as the row),
`reject_reason` and `rejected_step`, and, except on the gate and retest paths, `triggered_at`. On the FCFS path the
strategy is resolved from the scanner name by `_evidence_strategy_for` (the same map lookup as Step 2), so a reject
raised before Step 2 still names a strategy. FACT (search for `_evidence_capture(` in the file): no evidence record is
emitted for `PLACEMENT_FAILED` (L1233, L1681, L2340, L2616, L473), `TIMEOUT`, `PROCESSED`, `PROCESSED_NO_PLACER`, the
FIX-069 re-queue or the retest divert; the processor emits no `P3_SCREEN`, which is the screener's (A07's site,
`screening/secondary_screener.py` L650 to L674, outside the screener's DB `try`).

P05-S028. FACT (`core/evidence_contract.py` L86 to L119, L302 to L332, L488 to L600, L602 to L627): each capture
becomes one JSON line with the required provenance fields (`contract_version` "1", `evidence_epoch` "E1",
`capture_point`, `arm`, `signal_id`, `ts`, `captured_at`, `code_fingerprint`, `config_hashes`), the 20 context
fields, a `record_status` (`COMPLETE`, `PARTIAL` or `FAILED`) and the lists of missing fields. The processor's
payloads pass no `ts`, so `ts` is the capture time (L535). The line is appended with `open(..., "a")`, `write`,
`flush` and `os.fsync` under the recorder's `_write_lock` (L445; `main.py` builds one recorder for the screener and the
processor, P05-S024, and the docstring L497 calls it "one process-wide lock"), on the calling worker thread (L592 to
L600), to
`<root>/data_store/evidence/signal_evidence_<ARM>_<YYYY-MM-DD>.jsonl` (L319 to L321), where `<root>` is the
directory of `main.py` (P05-S024) and `<ARM>` is the value returned by `core.account_registry.primary_account_tag()`
(L462 to L465; a per-account tag, not read here; `UNKNOWN_ARM` when it cannot be resolved, L589). Failures are
written to `evidence_failures_<ARM>_<date>.jsonl` beside it, counted, logged and, once a day, sent to the critical
sink (L629 to L668). HISTORICAL (L495 to L501): the docstring measures the append at "mean 2.18 ms, p99 3.1 ms, max
4.1 ms per record" on the development PC and calls whether this cost belongs on the decision path "an OPEN item for
review"; "The VMs' volumes are UNMEASURED".

P05-S029. FACT (L582 to L612; `core/evidence_contract.py` L488 to L508, L602 to L627): the processor's
`_evidence_capture` builds the payload inside its own `try` (the payload is passed as a callable), returns at once
when no recorder is held, and on any exception calls `note_failure` and logs ERROR "evidence capture failed at ...";
the recorder's own `capture` also catches every `Exception`. INTERPRETATION: under `main.py`'s wiring an evidence
failure cannot change a status, a reservation or a placement; the observable effects on the A06 path are the
synchronous file write before `place()` and in each reject handler, and the extra log lines. The evidence files are
not part of the `signals` table and nothing in A06 reads them; their readers are A15's.

## 6. The handoff to A07: where A06's intake ends and what is passed

P05-S030. FACT (`signals/signal_processor.py` L895 to L1006; Master System Investigation Index, entries A01, A07,
A09, A11, A13): inside one worker call of `_process_one`, the steps before screening run in this order, and each call
lands in the module of the owner shown:

| Lines | Step | Code called | Owner of the called logic |
|---|---|---|---|
| L897 | status `PROCESSING` | `StateStore.update_signal_status` | A06 (the write); A03 (the method) |
| L906 to L907 | kill switch | `KillSwitch.is_active("entry")` | A13 |
| L910 to L912 | global entry window | `MarketWindows.is_entry_allowed(now)` | A01 |
| L914 to L921 | signal age | none (inline arithmetic) | A06 (P04 section 5) |
| L928 | shadow-inning guard | `ShadowTracker.is_tracking(symbol)` (L1976 to L2008) | A11 (`orders/shadow_tracker.py`) |
| L933 to L953 | scanner-to-strategy lookup | the processor's copy of `scan_webhook_map.scanners` and `strategies` dicts | the processor's own code (P04-S030; the configuration is A02's); which topic owns this step depends on the handoff line (P05-S031) |
| L959 to L972 | strategy control | `strategy_will_trade` (`strategies/control.py`) | A07 |
| L977 to L982 | per-strategy entry window | `MarketWindows.is_entry_allowed_for_strategy(now, strategy_obj)` | A01 (with A07's strategy fields) |
| L985 to L990 | strategy circuit breaker | `StrategyGovernor.check(strategy_name, now.time())` | A09 |
| L997 to L1006 | secondary screening | `SecondaryScreener.screen(...)` | A07 |

INTERPRETATION: the code has no single "hand to A07" call. The first transfer of control into an A07 module is the
strategy-control call at L959; A07's screening starts at L998. Under reading (b) of P05-S031, A06's last intake step would be the strategy lookup that
ends at L953; under reading (a), A06's side ends at the dequeue and the start of `_process_one` (the age check, L914 to
L921, is the last check of the signal's own fields before the strategy lookup). The worker thread that ran
A06's intake runs A07's screening and every later step; ownership changes by the code called, not by thread or queue.

P05-S031. HISTORICAL (L4 to L8, L29 to L31, L35): the processor's docstring describes the order
"pre-flight -> strategy lookup -> secondary screen -> price derivation -> position sizing -> risk approval -> capital
reserve -> order placement -> status update", "SPW3 -- Pipeline: step2=strategy lookup via map; step3=secondary_screener"
and "SPW7 -- P18 compliance: screener writes PASSED/REJECTED; processor does not". FACT (project records, quoted
exactly): the Master System Investigation Index, entry A06, Boundary, reads "A06 ends at the accepted or queued signal
handed to A07; downstream trade-decision logic is A07's" (the Topic Completion Register's A06 entry repeats it); the
index's A07 Scope includes "strategy selection and controls, secondary screening, hard gates, quality scoring, entry
gates, step execution, rejection and acceptance outcomes, and the decision handoff", and its A07 Boundary reads "A07
owns the decision to accept, reject or advance a signal". The A06 investigation direction (17-Nov-2026, section 2,
headed "APPROVED INDEX ENTRY — A06") words the boundary as "A06 ends at the accepted or queued signal handed to A07.
Downstream strategy selection, screening and trade-decision logic belong to A07."; the words "strategy selection,
screening" are not in the index's A06 entry (a wording difference for the coordinator; the index governs).
INTERPRETATION: read against the code, these records admit two lines: (a) the dequeue and the start of `_process_one` (the "queued signal handed" on), which
would place the strategy lookup (L933 to L953, "strategy selection") on A07's side; or (b) the screening call at L998,
which P04 used as its working end (P04-S033), with the strategy lookup and the processor's orchestration up to that
call recorded on A06's intake side, while the logic called at the intervening interfaces stays with its owners
(strategy control and screening A07, the per-strategy entry window A01, the strategy governor A09).
Which line the STUDY adopts is OPEN QUESTION (boundary; for the coordinator and Rama under decision A); this part
records both and the contract at each (P05-S032, P05-S033).

P05-S032. FACT (L376 to L399, L876 to L887; P01-S042, P04-S024 to P04-S026): reading (a)'s contract is the queue item:
the receiver's 5-tuple `(signal_id, scanner_name, symbol, trigger_price, triggered_at)`, or the FIX-069 dict with the
same keys plus `retry_count`; positions and keys are named by `_SIGNAL_TUPLE_FIELDS` (L78). The types are `str`
(`sig_` plus 32 hexadecimal characters), `str` (the path segment), `str` (after strip and alias), `float` and
`datetime` (IST-aware as parsed, P02-S055). HISTORICAL (L874): the processor's docstring says "triggered_at: naive
datetime (IST)" (P04, section 10 point 14). The item carries no strategy, direction, intent, received time or payload.

P05-S033. FACT (L998 to L1004; `screening/secondary_screener.py` L42 to L54, L123 to L141, A07's file, interface
only): reading (b)'s contract is the call `self._screener.screen(signal_id, symbol, scanner_name, trigger_price,
triggered_at, direction=strategy_obj.direction, intent=strategy_obj.intent, strategy=strategy_obj, market_data=None)`.
The first five are the queue item's values unchanged (P04-S034); `direction` and `intent` come from the loaded
`StrategyConfig`; `strategy` is that object itself (A02's schema); `market_data` is always `None` from this call
site. The return is a frozen `ScreeningResult` with `passed`, `status` ("PASSED" | "REJECTED_<step>" |
"SKIPPED_<reason>"), `score`, `tier`, `rejected_step`, `step_results`, `step_statuses`, `error_steps`,
`latencies_ms` and `market_data_snapshot`. The screener writes the row's status itself (P05-S012). The processor then
reads `status` (`startswith("SKIPPED_")`, L1008), `passed` (L1015), `tier` (L1047, L1118), `score` (L1048, L1374,
L1553); for the P1 evidence `score`, `tier`, `step_results`, `step_statuses` and `market_data_snapshot` (L1430 to
L1434); for the V3 builder `score`, `tier`, `step_results` and `market_data_snapshot` (L1597 to L1600); and for the
allocator builder `score` and `tier` (L1641 to L1642).

P05-S034. FACT (L1008 to L1022): after `screen()` returns, control comes back to the processor: a `SKIPPED_` status or
`passed == False` ends the worker's run with a log line and the `finally` (claim release, statistics); a pass
continues to price derivation (L1028) and the later call-outs of section 7, still on the same worker thread.

P05-S035. FACT (L1028 to L1035, L1081 to L1106, L1182 to L1187, L1446 to L1460; P04-S034): how the fields change after
the screener (direction question 19, handoff side): `signal_id`, `symbol` and `strategy_name` pass unchanged to every
later call; `trigger_price` is replaced as the price basis by `entry_price` and `sl_price` from `_derive_prices`
(L1028 to L1030), and for a strategy with `pullback_wait_enabled` false and a quote available, by prices derived from
the live LTP (L1082 to L1101); the original `trigger_price` is still passed to the placer as `signal_trigger_price`
(L1457); the strategy's `direction` becomes `side` "BUY" or "SELL" (L1034 to L1035); `scanner_name`, `triggered_at`
and `retry_count` go to `_admit_and_place` (L1182 to L1187) but not to `place()` (L1446 to L1460), whose arguments are
`symbol`, `side`, `qty`, `entry_price`, `sl_price`, `intent`, `signal_id`, `reservation_id`, `strategy`, `tgt_price`,
`signal_trigger_price`, `sizing_breakdown` and `tgt_risk_reward`.

## 7. Map of the later call-outs from `signals/signal_processor.py` (interface only; Rama's decision A)

P05-S036. FACT (lines as cited; owners from the Master System Investigation Index, entries A04, A05, A07 to A11,
A13 to A15 and A18): every call the FCFS path makes after the screener returns, in order, with the contract passed and
the receiving owner. The logic behind each call is not studied here.

| # | Call site | Callee | Contract passed | What the processor uses | Receiving owner |
|---|---|---|---|---|---|
| 1 | L1028 to L1030; again L1098 to L1100 | `_derive_prices(price, strategy_obj, now_time=now.time())`, in this file | trigger price (or live LTP), `StrategyConfig`, time | `(entry_price, sl_price)`; raises `INVALID_DERIVED_PRICE`, `ZERO_SL`, `REJECTED_NO_ATR_DATA` | A09 (price decisions; code in A06's file) |
| 2 | L1042 to L1056 | `RetestDiverter.enabled`, `.maybe_divert(...)` (`screening/retest_monitor.py` L303) | `signal_id`, `symbol`, `side`, `direction`, `entry_price`, `sl_price`, `strategy_name`, `intent`, `tier`, `trigger_price`, `score` | `True` ends the run (parked or dropped as a duplicate) | A08 |
| 3 | L1082 to L1087 | `quote_fn([symbol])` = `broker_adapter.get_quote` (`main.py` L3616) | a one-element list | `quotes.get(symbol).last_price` | A04 (the adapter); A09 (the re-anchor decision) |
| 4 | L1112 to L1128 | `PositionSizer.calculate(...)` | `symbol`, `side`, `entry_price`, `sl_price`, `intent`, `tier`, `lot_size`, `perf_weight` (from `perf_weights`, empty under `main.py`) | `success`, `constraint`, `reason`, `qty`, `breakdown`, `margin_required` | A09 |
| 5 | L1124, L1321, L1334, L1479, L1491, L1535 | `KillSwitch.record_api_failure(exc)` | the broker exception | nothing | A13 |
| 6 | L1136 to L1143, L1578 to L1603 | `V3ChainRunner.observe(V3Signal(...))` | a `V3Signal` snapshot (identity, prices, live target, screener outputs, sector, `as_of`, `triggered_at`, `v3_playbook`) | nothing; errors logged and ignored | A18 |
| 7 | L1147 to L1172, L1619 to L1644 | `PortfolioAllocator.mode`, `.in_scope(strategy_obj)`, `.submit(ScoredCandidate)` (enforce), `.observe(ScoredCandidate)` (shadow) | a `ScoredCandidate` (`signal_id`, `symbol`, `strategy_name`, `side`, `intent`, `score`, `tier`, `margin_required`, `sector`, `triggered_epoch`, and for enforce an `AdmitPayload`) | enforce in scope: `handed_off = True`, return (the claim stays held) | A18 |
| 8 | L1302 to L1305 | the processor's `_in_flight_count` | incremented under `_in_flight_lock` | value passed to the risk engine (row 11) | A06 (the counter); A09 (its use) |
| 9 | L1307 to L1344 | `FundManager.portfolio_lock` | held across rows 10 to 13 and the `RESERVED` write | | A09 |
| 10 | L1311, L744 to L779 | `_enforce_strategy_position_cap`, in this file: `StateStore.fetch_one` on `trades` and `FundManager.count_live_reservations_for_strategy` | `strategy_name`, `max_concurrent_positions` (default 2) | raises `STRATEGY_POSITION_LIMIT` | A09 (admission rule; code in A06's file); A03 (the read) |
| 11 | L1312 to L1313, L802 to L864, L782 to L800 | `_enforce_one_trade_per_symbol_direction`, in this file: `RiskEngine._one_trade_per_symbol_direction` (a private attribute), `StateStore.count_executed_trades_today_for_symbol_direction`, `capital.fund_manager._INTRADAY_INTENTS` and `_POSITIONAL_INTENTS` | `symbol`, `side`, `intent` | raises `SYMBOL_DIRECTION_DAILY_LIMIT` | A09; A03 (the read) |
| 12 | L1315 to L1325 | `RiskEngine.approve(...)` | `symbol`, `side`, `intent`, `sizing`, `signal_id`, `processor_in_flight_count` | `approved`, `failed_check`, `reason` | A09 |
| 13 | L1328 to L1340 | `FundManager.reserve(...)` | `symbol`, `qty`, `entry_price`, `intent`, `signal_id`, `strategy=strategy_name` | `success`, `reservation_id`, `reason_if_failed` | A09 |
| 14 | L1215, L1241, L1356, L1394, L1403, L1413, L1523 | `FundManager.release(reservation_id, reason)` | reasons `rejected_<check in lower case>` (`rej.check.lower()`), `placement_failed`, `no_order_placer`, `kill_switch_after_pipeline`, `shutdown_before_placement`, `entry_throttled`, `requeued_transient_error` | nothing (a failure of L1215, L1241 or L1356 is caught and logged; L1394, L1403 and L1413 have no `try`, and L1523 sits in a `try` that catches only `queue.Full`) | A09 |
| 15 | L1368, L1901 to L1953 | `_derive_target(entry, sl, strategy_obj)`, in this file | prices and strategy | `tgt_price`; raises three target labels (P05-S017) | A09 (code in A06's file) |
| 16 | L1371 to L1380, L486 to L555 | `TelegramNotifier.send(severity="INFO", title=..., body=..., source_module="signal_processor")` | the INTRADAY SIGNAL text | nothing; errors logged | A14 |
| 17 | L1389 to L1405 | `KillSwitch.is_active("entry")`; the processor's own `_stop_event` | | raises `KILL_SWITCH_LATE` or `SHUTDOWN` after releasing the reservation | A13; A06 (the stop flag; P04-S019) |
| 18 | L1410 to L1418 | `EntryThrottle.admit(symbol)` | `symbol` | `allowed`, `reason`; raises `ENTRY_THROTTLED` | A06 (P06); admission decision A07/A09 (decision B) |
| 19 | L1423 | effect-telemetry handle `inc()` (`core/effect_telemetry.py`) | | | A15 |
| 20 | L1427 to L1445 | `EvidenceRecorder.capture("P1_ACCEPT", ...)` through `_evidence_capture` | section 5 | | A15 |
| 21 | L1446 to L1460 | `OrderPlacer.place(...)` | P05-S035's 13 keyword arguments | return ignored; exceptions mapped to `TIMEOUT` (L1464), FIX-069 re-queue (L1486), re-raise (L1533 to L1538) | A10 |
| 22 | L1550 to L1561, L614 to L658 | `sr_detector.observe(Candidate(...))` | `signal_id`, `symbol`, `strategy`, `direction`, `intended_entry`, `sl_price`, `tgt_price`, `qty`, `intent`, `mode`, `ts`, `score` | nothing; errors logged | A08 |
| 23 | L1201, L1202 to L1211 | status write and `P2_REJECT` on every reject (sections 3 and 5) | | | A03 (method); A15 (recorder) |

P05-S037. FACT (same file, other call-outs outside the FCFS order): `stop()` calls `self._screener.shutdown()` when
the screener has one (L342 to L344; A07); the dispatcher calls `ZoneWarmer.enqueue(symbol)` (L361 to L375; A08,
P04-S015); `get_runtime_metrics` (L683 to L738) reads `StateStore.count_trades_today` and
`count_settled_trades_today`, `FundManager.count_live_reservations`, the risk engine's private `_max_daily` and
`EntryThrottle.metrics()`, and is handed by `main.py` to the health server as `metrics_provider` (L4076;
`scripts/healthcheck_server.py` L251 to L253; A15); `_sector_for` (L1605 to L1617) calls the instrument cache's
`sector_for` or `get_sector` for the V3 and allocator builders only (A05). FACT (search): `bus` and `quality_scorer`
are stored (L201, L210) and never used again in the file; HISTORICAL (L145, L168): the scorer is "kept for
logging/metrics".

P05-S038. FACT (`config/system_config.yaml` L509, L529, L565, L574, A02's file; `main.py` L3422 to L3423,
L3473, L3490 to L3494, L3631 to L3651, L3672 to L3694, L3769 to L3793): at the committed values, `sr_detector.enabled:
true` (row 22 built), `wait_for_retest_enabled: false` (row 2: no diverter is set, P05-S041), `allocator_mode:
"shadow"` (row 7: built and late-bound, so the shadow `observe` branch runs; `enforce` would need a configuration
change) and `v3_chain_mode: "shadow"` (row 6: built and late-bound). Each construction is inside a `try` that falls
back to `None`. The effective values on the legacy machines are UNKNOWN / NOT ESTABLISHED (A02), and so is whether
these components ran (the index's A18 boundary: "actual activation is UNKNOWN until established by evidence").

P05-S039. HISTORICAL (Master System Investigation Index, entry A18, Paths): "the integration points in `signals/`,
`screening/`, `capital/` and `main.py` (the owners of those integration call sites remain A01, A06, A07 and A09)".
INTERPRETATION: rows 6 and 7, and the late-bound setters of section 8, are A06's integration call sites whose
receiving logic is A18's; rows 1, 10, 11 and 15 are code in A06's file whose decisions the index gives to A09
("A09 owns the price, sizing, risk and capital decisions"). The study of that code is left to A09 under decision A.

P05-S055. FACT (search of `signals/signal_processor.py` for `hard_gate`, `step_executor`, `self._scorer`, `PB-01`,
`pb01`, `watchlist`; `main.py` L3281 to L3298; added in the check): the processor makes no direct call to A07's hard
gate, quality scorer or step executor, nor to any PB-01 code (A18): `main.py` passes `step_executor`,
`quality_scorer=scorer` and `hard_gate` to the `SecondaryScreener` (L3282, L3283, L3295), so they are reached only
inside `screen()` (row (b) of P05-S033); the processor's own `quality_scorer` reference is stored and unused
(P05-S037), and its only other contact with the screener is `self._screener.shutdown()` at `stop()` (L342 to L344),
which its comment ties to "the screener's internal step_executor thread pool". The PB-01 end-of-day route runs through
the receiver (decision D; P01 and P03), not the processor. The entry gate is reached only through
`continue_from_gate` (P05-S043); the processor never adds to it.

P05-S056. FACT (L1221 to L1231, L664 to L673, L899, L1023, L1129, L1346, L1382; `main.py` L3575 to L3623; P04 section 5;
added in the check): two further call-outs on the FCFS path, not in the table of P05-S036: on an `EXPIRED` reject the
reject handler calls `self._notifier.send_warning(...)` at most once per 60 s of `time.monotonic()` (A14's notifier;
any error swallowed); and five `_heartbeat(symbol)` checkpoints call the receiver's heartbeat callback, which
`main.py` does not pass (`in_flight_heartbeat_fn` absent from L3575 to L3623), so each is a no-op (P04). The
`in_flight_release_fn` callback is the receiver's `release_in_flight` (`main.py` L3612), an A06-internal call
(P04, P03).

## 8. Late-bound setters and the other entry points into the processor

P05-S040. FACT (`signals/signal_processor.py` L356 to L359, L1568 to L1576; `main.py` L3650, L3660, L3693, L3700,
L3793; P04-S002): `set_allocator`, `set_v3_chain` and `set_retest_diverter` each assign one attribute
(`_allocator`, `_v3_chain`, `_retest_diverter`) with no lock and no other effect. `main.py` calls `set_allocator` and
`set_v3_chain` after building those components (and again with `None` in the `except` of a failed wiring) and
`set_retest_diverter` once; every call is earlier in the file than `signal_processor.start()` (L3974). The constructor
parameters `allocator` and `v3_chain` (L195 to L196) are not passed by `main.py`; there is no constructor parameter
for the diverter (L231 sets `None`).

P05-S041. FACT (`main.py` L3423, L3769 to L3802; `config/system_config.yaml` L529): `set_retest_diverter` is called
only when `wait_for_retest_enabled` is true and the zone warmer and zone cache were built (L3769), inside a `try`; the
committed value is `false`. INTERPRETATION: at the committed value `_retest_diverter` stays `None`, so the divert
(section 7 row 2) and `continue_from_retest` (P05-S044) are not reached; the effective value is UNKNOWN / NOT
ESTABLISHED.

P05-S042. FACT (search of every file at `970aabf`, tests and documents included, with the four exclusions; `git log
-S set_shadow_engine` over `signals/signal_processor.py`, `capital/shadow_engine.py` and `main.py`): no
`set_shadow_engine` method or call exists. The only occurrence is the docstring of `capital/shadow_engine.py` L14,
HISTORICAL: "Injected into signal_processor via set_shadow_engine()." (L13 to L15 also say it is "Called after live
pipeline completes"), added with the file by `25c4a77` (31-May-2026); the processor file has never contained the
name. FACT (search for `ShadowEngine(` and `shadow_engine` in non-test code): no non-test code builds or imports
`ShadowEngine`; one unit test builds it. INTERPRETATION: the injection the docstring describes is not implemented at
`970aabf`. The processor's `shadow_tracker` (A11's `orders/shadow_tracker.py`, the re-entry guard of P04-S029) is a
different component. `capital/shadow_engine.py` is A09's (index, entry A09, Paths).

P05-S043. FACT (`main.py` L865 to L893, L3839 to L3844, L3975; `screening/entry_gate.py` L156, L179, L209, L288,
A07's file, interface only; search for callers of `EntryGate.add`): `continue_from_gate(entry, release_ltp)` is called
only by `main.py`'s `_gate_release_worker`, which `_on_gate_release` submits to the module-level
`_gate_release_pool` (`ThreadPoolExecutor`, 2 workers, prefix "gate-release") when the gate releases an entry with
reason `PRICE_HIT`, passing `entry.extras.get("release_ltp")`; other reasons are logged "no action"; an exception that
escapes is logged at ERROR. No non-test code calls `EntryGate.add`; the gate's entries come only from
`rehydrate_from_gate_state`, which `entry_gate.start()` (`main.py` L3975) runs. HISTORICAL (processor L2236 to L2238):
"DORMANT today: nothing calls EntryGate.add(), so only gate_state rows rehydrated at boot can reach it". The contract
is a `WatchEntry` (`screening/entry_gate.py` L54) whose `signal_id`, `symbol`, `strategy_name`, `entry_price`,
`sl_price`, `tgt_price`, `direction`, `tier` and `trigger_price` the processor reads (L2027 to L2099, L2244, L2263),
plus `release_ltp`, passed to `place()` (L2262). The path writes the statuses of P05-S011, has no age check (P04),
no screening, no FIX-069 re-queue, no allocator or V3 hook and no release of a receiver claim (HISTORICAL L2018 to
L2019: "in_flight tracking is NOT released here -- the EntryGate already manages it").

P05-S044. FACT (`main.py` L3784 to L3788; `screening/retest_monitor.py` L27, L51, L181 to L190, A08's file,
interface only; processor L2375 to L2640): `continue_from_retest(parked)` is the `on_confirm` callback of the
`RetestMonitor`, called from the monitor's poll thread on a confirmed retest (HISTORICAL L2381 to L2382). The contract
is a `ParkedCandidate` (`signal_id`, `symbol`, `strategy`, `direction`, `zone_band_low`, `zone_band_high`, `tier`,
`trigger_price` and others). The path re-checks the kill switch, window, shadow guard, strategy control, per-strategy
window and governor, computes a structure SL from the zone band (L2436 to L2442) and an entry estimate from a live
quote (`_retest_entry_estimate`, L2642 to L2657), and places with `entry_order_type="MARKET"` (L2561); it has no age
check and releases no receiver claim (the FCFS `finally` released it when the signal was diverted, P04-S057).

P05-S045. FACT (`main.py` L3636 to L3651; `allocation/portfolio_allocator.py` L46 to L47, L294, A18's file,
interface only; processor L1646 to L1737): `admit_prepared(candidate)` and `reject_prepared(candidate, reason)` are
passed to the allocator as `enforce_admit_fn` and `enforce_reject_fn`. `admit_prepared` reads the `AdmitPayload`
(`scanner_name`, `strategy_obj`, `sizing`, `screen_result`, `entry_price`, `sl_price`, `trigger_price`,
`triggered_at`, `retry_count`, `now`), runs the shared `_admit_and_place` and returns `ac.placed`; its `finally`
releases the receiver claim unless re-queued. `reject_prepared` writes `REJECTED_<reason>`, emits `P2_REJECT`, counts
the reason and releases the claim. HISTORICAL (L1647 to L1650): "R5 migration scaffolding — consolidate with
_process_one when enforce is activated". HISTORICAL (`core/evidence_contract.py` L100 to L101, A15's file): "the
allocator has never run in enforce" (a comment; not evidence either way). INTERPRETATION (P05-S038): the allocator
calls them only in its enforce mode (A18's logic); the committed mode is `shadow`.

P05-S046. FACT (L405 to L480, L2010 to L2370, L2375 to L2640, L1646 to L1737; search for `_active_workers`): the
four entry points other than the dispatcher's `_process_one_safe` run on threads outside the processor's executor
(the gate-release pool, the retest monitor's poll thread, the allocator's worker) and are not counted in
`_active_workers` (changed only at L463 to L480). They share with the FCFS workers the processor's `_in_flight_count`
and `_stats` (each under its lock), the entry throttle, the fund manager's `portfolio_lock` and the store (each
thread with its own connection, P05-S004).

## 9. The A04 rate-limiter boundary (`try_acquire`)

P05-S047. HISTORICAL (A04 RECONCILED TOPIC RECORD, section 15.2, row A06): "RD-14, CS-03, CS-05, CS-08, RL-14, RL-16,
RL-18"; section 6, row 14: "REJECTED as issues or MATCH: the unwired `try_acquire` pre-check (A06's wiring), tokens
accruing during a freeze, concurrent misses of the margin cache, a limiter exception at the boot's first call, G7's
quote bucket replaced by the later 3/3 (RL-15, RL-17, RL-18, RL-19, RL-22)". The record that carries the pre-check is
RL-18 (A04 AUDIT, RL-18 row): "`try_acquire` (RL5) and its only caller (point 6)" ... "its only non-test caller, the
signal processor's pre-check, is never reached because `main.py` passes no limiter ... if wired, a successful
pre-check would itself spend an `order` token before `place_order` took another (A06's, section 5); the unwired code
is part CS's (P04-S338)"; result "MATCH; FACT (the A04 side)"; owner "A04; A06 (the caller)". RL-18's ID, owners,
classification and status are unchanged here.

P05-S048. FACT (search of `signals/` and `scripts/preflight_scanner_check.py` for `rate_limiter`, `try_acquire`,
`RateLimiter` and `.acquire(`): the only references to A04's limiter in A06 code are the processor's parameter
`rate_limiter=None` (L189), its storage (L233) and the pre-check `self._rate_limiter.try_acquire("order")` (L418 to
L419). The receiver's `_PerIpRateLimiter` (L69, L245) is the receiver's own per-IP bucket (P03 section 3), not A04's
limiter. FACT (`main.py` L2348, L2385, L2985, L3487, L3575 to L3623): `main.py` builds one `RateLimiter` and passes
it to the broker adapter, the smart-target manager and the S&R fetch closure, but not to `SignalProcessor` (this
confirms the note handed from P01; P04-S053). FACT (`git show` of `main.py` at `31075d0`, 12-May-2026, the FIX-007
commit; at `686df1c`, 02-Sep-2026; and at `970aabf`; `git log -S FIX-007 -- main.py`): the `SignalProcessor(...)`
call passes no `rate_limiter` at any of the three, and the label FIX-007 never appears in `main.py`'s history.

P05-S049. INTERPRETATION (P05-S048; A04 RECONCILED TOPIC RECORD section 4.7; A04 RL-16, summarised in section 10):
under `main.py` A06 code never calls A04's limiter; an entry's `order` token is taken only below `OrderPlacer.place()`
(A10), in the adapter (A04), on the worker thread, after the worker has left `portfolio_lock` (the `with` block ends
at L1344; `place()` is at L1446). FACT (`core/exceptions.py` L158, L215, L243, L261, L284, A01's file at the
boundary; processor L1464 to L1538): of the limiter's exceptions, a `BrokerRateLimitError` (a `BrokerError`) that
reaches the processor from `place()` takes the FIX-069 re-queue branch (L1486 to L1532); a
`BrokerRateLimit429Error` (a `BrokerError`, not a `BrokerRateLimitError`) takes the generic `BrokerError` branch,
which re-raises to `PLACEMENT_FAILED` (L1533 to L1536, L1233 to L1246); a `RateLimitAbortedError` (not a
`BrokerError`) is re-raised as any `Exception` (L1537 to L1538) to the same handler. Which of them the placer lets
through is A10's (A04 CS-05 records the placer's handlers).

P05-S050. INTERPRETATION (P04-S053, P04-S054; A04 RL-18; FACT: L405 to L465; the Python `queue` page of P05-S005,
whose `put` with a positive `timeout` "blocks at most *timeout* seconds and raises the Full exception if no free slot
was available within that time"): if a limiter were passed, the pre-check would run on the worker before
`_process_one`, outside every `try` of `_process_one` and before the `try` of `_process_one_safe` (L465); on success
it would spend an `order` token in addition to the adapter's; on failure it would try to re-put the item with
`put(signal_tuple, timeout=1.0)` (L426), blocking the worker for up to 1 s; if the put succeeds it returns with the
receiver claim kept; if the queue stays full it writes `REJECTED` with reason `QUEUE_FULL`, emits `P2_REJECT` and
releases the claim (L427 to L461). This part records the wiring fact only; whether the pre-check was meant to be active is a question
for Rama (section 13), already asked by P04 (P04 section 12, question 8).

## 10. Inherited items touched by this part (A06 side only; IDs, owners, classifications and statuses unchanged)

P05-S051. FACT (the A03 AUDIT and A04 AUDIT entries named; A03 and A04 RECONCILED TOPIC RECORDS, section 15.2): the
items handed to A06 that this part's sections touch, with the A06-side fact recorded here (the full record of each
item is P09's):

| Item | Recorded as (originating record) | A06-side fact in this part |
|---|---|---|
| A03 P-02 | ISSUE; Owner "A03 (the method); A06 (the pipeline's status sequence and whether a final status can be overwritten)" | P05-S007 to P05-S011: 26 processor writes, none conditional on the current status; reason-less writes clear the reason |
| A03 P-11 | ISSUE; Owner includes "A06 (reservation status)" | P05-S010, P05-S018, P05-S021: the reservation and `RESERVED` are separate transactions; on a failed `RESERVED` write the worker releases the reservation |
| A03 P-12 | UNKNOWN / NOT ESTABLISHED; Owner "A03 (lock wait); A06, A09 (lock scope)" | P05-S010: the three `RESERVED` writes are the only status writes inside `portfolio_lock` |
| A03 Q-11 | ISSUE; Owner includes "A06 (resumption guards)" | P05-S043, P05-S044: `continue_from_gate` and `continue_from_retest` write `PROCESSING` first, with no check of the current status or of an earlier resumption (L2034, L2393) |
| A03 R-08 | ISSUE; Owner "A06; A03" | not re-studied here (P03-S012, P04-S064) |
| A04 CS-03 | ISSUE; Owner includes "A06 ... for their handlers (boundary)" | P05-S009 rows 4b, E; P05-S019, P05-S049: the processor's handling of `BrokerTimeoutError`, `BrokerRateLimitError`, `BrokerRateLimit429Error` and other exceptions from `place()` |
| A04 CS-05 | ISSUE; "which reservation, if any, is then released is A06's and A09's to establish" | P05-S049: `ValueError` and `RateLimitAbortedError` from `place()` reach the handler at L1233, which releases `reservation_id` only if it is still set; it is set while `place()` runs (L1340, L1461), so that handler releases the reservation the placer received, provided its `PLACEMENT_FAILED` write succeeds first (P05-S018); for a `BrokerError` the placer also releases it (P05-S052) |
| A04 CS-08 | ISSUE; Owner includes "A06 (the reservation left to the recovery)" | P05-S019: on `TIMEOUT` the processor drops its handle without releasing (L1483), unless the kill-switch call or the status write raises first |
| A04 RL-14, RL-16 | UNKNOWN / NOT ESTABLISHED; ISSUE (minor) | RL-14's A06 side is the entry throttle (P06); RL-16: `place()` can hold the worker for up to the limiter's 30 s wait, outside `portfolio_lock` (P05-S049) |
| A04 RL-18 | MATCH; Owner "A04; A06 (the caller)" | section 9 |

FACT (A04 RECONCILED TOPIC RECORD, section 22.2): "A04-33's rule is also a scope input for A06 and A10, which decide
what is traded"; the only same-day re-entry rule in `signals/signal_processor.py` is row 11 of section 7 (A09's
decision; committed `one_trade_per_symbol_direction_per_day: true` under `risk:`, `config/system_config.yaml` L261,
L302); the entry throttle's per-symbol cooldown in A06's `signals/entry_throttle.py` is a time-spacing control (P06). The comparison is not made here
(P09; the AUDIT; Phase 2).

## 11. Points the AUDIT may examine (neutral)

1. The handoff to A07 is not one call: A06 intake, A13, A01, A11, A07 and A09 calls interleave before screening; the
   STUDY must state which line it adopts (P05-S030, P05-S031).
2. The receiver writes the scanner name as the row's `strategy`; the processor resolves the real strategy but never
   writes it to the row; the evidence records carry the resolved strategy (P05-S003, P05-S006, P05-S027; P01-S043).
3. No status write is conditional on the current status, and reason-less writes clear earlier reasons; the time of a
   status change is stored nowhere (P05-S007, P05-S008; A03 P-02).
4. A failing status write can leave a final status that misdescribes the signal: `PLACEMENT_FAILED` for a signal never
   checked (P05-S016) or for an order handed to the placer (P05-S020); `PROCESSING` after a screener reject
   (P05-S021); `QUEUED` with no queue item (P05-S005).
5. A failing reject write skips the reservation release for the three target rejects (P05-S017).
6. On a placement timeout, a failing kill-switch call or `TIMEOUT` write sends the reservation to the
   `PLACEMENT_FAILED` handler, which releases it, contrary to the comment's "do NOT release" (P05-S019).
7. The FIX-069 re-queue leaves the row `RESERVED` with no reservation until the retry starts (P05-S009).
8. No code writes `TRADED`, which the schema allows and several readers count (P05-S014).
9. `REJECTED_NO_ATR_DATA` would be stored as `REJECTED_REJECTED_NO_ATR_DATA` (P05-S013).
10. The schema's status comment omits `PROCESSING`, `RESERVED` and `TIMEOUT` (P05-S015).
11. A stop leaves rows `QUEUED`, `PASSED`, `RESERVED` or parked; only `PROCESSING` rows are swept, by an end-of-day
    script outside A06, and nothing re-reads them at start-up (P05-S022, P05-S023).
12. The evidence recorder adds a synchronous `fsync` on the worker before every placement and in every reject handler;
    its own docstring leaves that cost open; it records no `PLACEMENT_FAILED`, `TIMEOUT` or `PROCESSED` outcome; it is
    later than the last recorded deployment (P05-S025 to P05-S029).
13. `capital/shadow_engine.py` documents a `set_shadow_engine()` injection that does not exist (P05-S042).
14. `bus` and `quality_scorer` are required constructor arguments that the processor never uses (P05-S037).
15. The processor reads private attributes of the risk engine (`_one_trade_per_symbol_direction`, `_max_daily`) and
    private names of the fund-manager module (P05-S036 rows 11, P05-S037).
16. The gate and retest resumptions, and the allocator's admit and reject functions, run outside the executor, are not
    counted as active workers, have no safe wrapper, and (gate and retest) no age check, no screening and no claim
    release (P05-S043 to P05-S046).
17. The FIX-007 `try_acquire` pre-check has never been wired by `main.py` since it was added (P05-S048); A04 RL-18
    leaves the wiring question to A06.
18. A broker 429 and a client-side limit from `place()` take different processor branches (P05-S049).
19. When `place()` raises a `BrokerError`, the placer's failure path and the processor's handler both call a release for
    the same reservation (P05-S052).
20. In every generic handler the `PLACEMENT_FAILED` write precedes the reservation release, so a failing write (for
    example a store still refusing writes after a failed `RESERVED` write) skips the release; the safe wrapper retries
    only the status (P05-S018). The late-abort releases (`KILL_SWITCH_LATE`, `SHUTDOWN`, `ENTRY_THROTTLED`) are not
    guarded, so a failing release turns the reject into `PLACEMENT_FAILED` with a second release (P05-S017).
21. A03 P-02 states that no caller passes `ts`; the screener does (the effect, no stored status time, is unchanged)
    (P05-S054).
22. The A06 investigation direction words the index's A06 boundary with "strategy selection, screening", which the
    index entry itself does not contain (P05-S031).

## 12. UNKNOWN / NOT ESTABLISHED

- Whether any `signals` row was written, updated or left in any state described here in production; every runtime
  outcome of sections 2 to 4 (P05-S005, P05-S016 to P05-S023).
- Whether production ran the evidence-recorder commits of 10 and 11-Sep-2026, and whether any evidence file exists;
  the arm value and the evidence directory on the legacy machines (P05-S025, P05-S028).
- The effective values of `sr_detector.enabled`, `wait_for_retest_enabled`, `allocator_mode`, `v3_chain_mode`,
  `one_trade_per_symbol_direction_per_day` and `atr_fallback_mode`, and so which optional call-outs ran (P05-S013,
  P05-S038, P05-S041; A02).
- Whether any `gate_state` row existed at a start, so whether `continue_from_gate` ever ran (P05-S043).
- Whether the allocator ever ran in enforce mode; whether `admit_prepared` or `reject_prepared` were ever called
  (P05-S045).
- The installed Python and SQLite versions (P05-S004; P04-S063).
- Whether the timeout ordering of P05-S019 or the failed-write cases of P05-S016 to P05-S021 ever occurred.
- Whether any process other than the trading process wrote `TRADED` to `signals` (P05-S014).
- Whether a failed `PLACEMENT_FAILED` write ever left a reservation held by the processor, or a late-abort release ever
  failed (P05-S017, P05-S018).

## 13. Draft questions about intent for Rama

1. Was the `signals` row meant to record the strategy that the scanner map assigns, or the scanner name, in its
   `strategy` column?
2. Was a signal's final status meant to be protected from later overwrites, and was each status change meant to keep
   its time and reason (SP9 and P16 say so; the store's comment says the time is not stored)?
3. Which status was meant to mark a signal that became a trade: `PROCESSED`, `TRADED`, or the `trade_id` link?
4. When a status write fails, what was meant to happen to the signal: stop, retry the write, or continue?
5. Was the forward evidence recorder (Batch 1, September 2026) meant to run in production, with its per-record `fsync`
   on the decision path?
6. Was a shadow engine meant to be injected into the signal processor, as `capital/shadow_engine.py` says?
7. Was the FIX-007 `try_acquire` pre-check meant to be wired (already asked as P04 question 8; A04 RL-18)?
8. (Boundary, for the coordinator and Rama under decision A, not legacy intent) At which line should the STUDY place the
   A06-to-A07 handoff: the dequeue and start of `_process_one`, or the screening call at L998 (P05-S031; the index's
   A06 boundary names only "trade-decision logic", its A07 scope names "strategy selection and controls", and the
   direction's wording adds "strategy selection, screening")?

## 14. Where the direction's questions are answered

The brief assigns P05 direction questions 19 (handoff side), 20, 23 (`signals`), 24 and 25 (A06 investigation
direction, 17-Nov-2026, section 4).

| Direction question (section 4) | Where in P05 | Other parts |
|---|---|---|
| 19 How strategy identity, scanner identity, symbol, price, timestamp and other fields survive or change across each handoff (handoff side) | P05-S003, P05-S006, P05-S032, P05-S033, P05-S035 | P01-S042, P01-S043 (receiver); P04-S034 (to the screener) |
| 20 When a signal event is created and persisted; which fields are written; what happens if persistence fails or the process stops between steps | P05-S001 to P05-S023, P05-S052, P05-S053 | P03-S055 (receiver writes), P04-S019, P04-S020, P04-S064, P11 |
| 23 A03 storage boundary: `signals` reads and writes, transaction boundaries, error handling (the `signals` side) | P05-S004, P05-S006 to P05-S015, P05-S051, P05-S054 | P03 section 6 (receiver, `webhook_audit`, EOD heartbeat), P11 (producers, consumers, retention) |
| 24 The A04 rate-limiter boundary and the unwired `try_acquire` pre-check | P05-S047 to P05-S050 | P04-S053, P04-S054 |
| 25 All handoffs to A07; where A06's responsibility ends and A07's begins (the end line itself is recorded in both readings and left OPEN for Rama, P05-S031) | P05-S030 to P05-S034, P05-S036 to P05-S046, P05-S055, P05-S056 | P04-S033 |
| 15, 16, 21 (also touched) the path to A07, worker threads and the late-bound wiring | P05-S040 to P05-S046 | P04 |
| 26 to 28 (whole-topic audit inputs) | sections 11 to 13 | the AUDIT |


## 15. Check log

Checked by a separate read-only helper on 17-Nov-2026 against `970aabf` (every cited legacy line re-read with
`git show`), the project records under `algocore_system` (A03 AUDIT entries P-02, P-11, P-12, Q-11 and R-08; A04 AUDIT
entries CS-03, CS-05, CS-08, RL-14, RL-16 and the RL-18 row; A04 RECONCILED TOPIC RECORD sections 4.7, 6 row 14, 15.2
and 22.2; Decision Register D-21; Master System Investigation Index entries A01, A06, A07, A08, A09, A11, A13, A14,
A15 and A18; Topic Completion Register, A06 entry) and the external pages of section 1.4, re-opened on 17-Nov-2026.
The draft before the check is kept as `parts/drafts/A06_P05_EVENT_CREATION_AND_HANDOFF_DRAFT.md`.

- Statements checked: 52 (P05-S001 to P05-S052). Correct as written: 30. Corrected: 22. Withdrawn: 0. Added: 4
  (P05-S053 to P05-S056).
- The two candidate lines for the A06-to-A07 handoff (P05-S031) are kept as two readings; neither is adopted. The
  check corrected only the quotations that P05-S031 rests on.

| ID | What changed | Why |
|---|---|---|
| P05-S002 | Added `_PREFIX_SIGNAL` (L38) and the Python `uuid` page for "32 lower-case hexadecimal characters"; "accepted symbol" became "symbol that reaches the INSERT" | Library behaviour was stated without an authoritative source; the row is written before acceptance |
| P05-S004 | Added `PRAGMA busy_timeout = 30000` (`core/state_store.py` L107 to L113); range L215 to L242 | The second 30 s wait setting was omitted |
| P05-S005 | Added the Python `queue` page for `put_nowait`; the commit point stated as the end of the `with` block (L964 to L980) | Library behaviour uncited; imprecise line |
| P05-S010 | "the only FCFS write" became "the only FCFS `signals` write", noting the store reads and A09's ledger write inside the lock | Imprecise |
| P05-S013 | Cited where the `"WARN"` default is set (processor L177; `core/config_loader.py` L572; `main.py` L3593) | Source of the default not cited |
| P05-S014 | Replaced "the only other non-test hit" with the full list of non-test hits (readers, a label, a CSV header, a docstring example, a parameter default) and the list of non-test `signals` writers | Other non-test hits exist; the conclusion (no code writes `TRADED`) is unchanged |
| P05-S015 | Added `REJECTED_EXCLUDED_SYMBOL` (receiver L708 to L717) and `STORE_ERROR` (L1016 to L1044) to the answers that leave no row | Incomplete |
| P05-S016 | Basis now cites the Python `try` semantics (P05-S053) | Language semantics relied on without a source |
| P05-S017 | Added that the late-abort releases (L1394, L1403, L1413) are not guarded and what follows if one raises | Incomplete |
| P05-S018 | Added that the handler's `PLACEMENT_FAILED` write precedes the release, so a failing write skips the release, and that the same order holds in all four generic handlers; interpretation narrowed accordingly | The draft's "released by the same worker (if that release succeeds)" omitted a failing condition shown by the code |
| P05-S019 | Quotation corrected to the source's em dash; interpretation cites P05-S053 | Quotation fidelity; language semantics |
| P05-S025 | Added `02d1e3f` (P3 moved outside the screener's DB `try`); the production-figure comments quoted exactly with their locations | Commit list incomplete for the brief's range; a paraphrase was in quotation marks |
| P05-S026 | `score` corrected to the payload key `score_total`; the row's status after P1 completed (row E, FIX-069 re-queue); gate and retest P1 payload differences added | Wrong key name; incomplete |
| P05-S028 | "under one process-wide lock" became the recorder's `_write_lock` (L445), with the docstring's wording quoted; "UNMEASURED" quoted exactly | Precision |
| P05-S031 | The sentence quoted as the index's A06 Boundary is the A06 investigation direction's wording; replaced by the index's exact A06 Boundary, its A07 Scope and Boundary, and the direction's wording, labelled as such; label of the quotations FACT (project records); both readings kept | Misattributed quotation; the index's A06 entry does not contain "strategy selection, screening" |
| P05-S033 | Citation split by builder (P1 evidence, V3, allocator); L1553 added for `score` | L1641 to L1642 read only `score` and `tier` |
| P05-S036 | Row 14: release reason is `rejected_` plus the lower-cased check; the guard wording made exact (L1523 is in a `try` that catches only `queue.Full`) | Precision |
| P05-S045 | Added HISTORICAL comment `core/evidence_contract.py` L100 to L101 ("the allocator has never run in enforce") | Relevant intent-side text omitted |
| P05-S049 | "A04 RL-16, quoted in section 10" became "summarised" | RL-16 is not quoted there |
| P05-S050 | FIX-007 failure path made exact (put success keeps the claim; a full queue writes `REJECTED`/`QUEUE_FULL`, emits `P2_REJECT`, releases); the pre-check is also outside `_process_one_safe`'s `try`; Python `queue` page cited | Imprecise; library behaviour uncited |
| P05-S051 | CS-05 row: the release depends on the preceding `PLACEMENT_FAILED` write; A04-33 sentence names the file and the YAML parent key and mentions the entry throttle's per-symbol cooldown | Precision |
| P05-S052 | Added that the handler's release follows its status write (P05-S018) | Precision |
| Section 1.3 | A working-machine tool path replaced by "the fieldwork's read-only search helper" | No machine path in a record |
| Sections 1.4, 11 to 14 | External pages added in the check listed; AUDIT points 20 to 22, one UNKNOWN item, question 8's wording and the question table updated for the corrections and additions | Consistency with the corrected statements |

Statements added (each verified at `970aabf` or against the cited project record or page):

- P05-S053: the Python Language Reference on `try`, `except` and `finally`, the basis of P05-S016 to P05-S020 and
  P05-S052.
- P05-S054: the screener passes `ts=` to `update_signal_status`; A03 P-02's wording "no caller passes it" does not
  match (P-02 not reclassified).
- P05-S055: the processor makes no direct call to the hard gate, quality scorer, step executor or PB-01 code; they sit
  behind `screen()` or the receiver.
- P05-S056: the `EXPIRED` `send_warning` call-out (A14) and the five heartbeat no-ops, not in the call-out table.

Not verified, and why:

- The content of statements of P01 to P04 cited by ID was not re-checked here (those parts have their own checks).
- The A03 and A04 STUDY statements cited inside the quoted AUDIT entries (for example P04-S113 of A03) were not opened;
  only the AUDIT entries themselves were read. G-19 was not opened.
- Every runtime outcome stays UNKNOWN / NOT ESTABLISHED; the installed Python and SQLite versions are not pinned.
- Rule conflict: none found. Security: no identifier, value or machine path was copied; filter hits on screen were
  hash-algorithm names and lint codes (false positives, not reproduced).

- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P05-S030: the owner cell of the strategy lookup (L933 to L953) no longer assigns it to A06, which assumed reading (b) of P05-S031.
- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P05-S030: the sentence "A06's own last intake step is the strategy lookup" restated under both readings of P05-S031; the line stays OPEN FOR RAMA.
