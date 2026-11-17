# A06 evidence: the webhook receiver: server, routes, request handling and lifecycle

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P01, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude.
**Purpose and scope:** `signals/webhook_receiver.py` in whole for structure (every class, method, constant and module-level object; the Flask app; every route; the request flow from receipt to response; the parse of the body into an internal signal; the WR4 and WR4b scan-name check; the EOD routing to the capture worker, payload and contract only; the sweeper thread; `stop()`); the waitress server and its thread in `main.py` L3979 to L4054; the receiver's construction (`main.py` L3402 to L3415) and its shutdown (`main.py` L1681 to L1690, L1719, L1751); A01's recorded lifecycle facts, receiver side; the waitress and Flask behaviour these depend on (official documentation, current external context); other non-test callers of the receiver and its app; the A19 scripts that post to it (HISTORICAL only). Authentication and validation detail is P02's; deduplication, throttling, in-flight control, the queue put and `webhook_audit` are P03's; the processor is P04's and P05's; Chartink configuration and the scanner checks are P07's. This part cross-references them where the flow passes them (STUDY part P01).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07). The loopback and all-interfaces addresses are written `<LOOPBACK>` and `<ALL_INTERFACES>`.

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)
In whole:
- `signals/webhook_receiver.py` (1,207 lines; read L1 to L1207, every printed line passed through an identifier filter;
  structure taken with Python `ast.parse` of the source text, which executes nothing).
- `scripts/test_webhook.py` (13 lines; A19, HISTORICAL only).
- `scripts/load_test_signals.py` (332 lines; A19, HISTORICAL only; L1 to L140 read line by line, L140 to L332 scanned
  for its server, scenarios and assertions).
- `requirements.txt` (15 lines).

In part (line ranges):
- `main.py` L1595 to L1725 (`_shutdown`, receiver and processor stop), L1725 to L1835 (scanned: Flask comment, store
  close), L3395 to L3420 (queue and receiver construction), L3477 to L3478 (watchlist flag), L3570 to L3640 (processor
  construction, for the receiver callbacks passed or not passed), L3700 to L3768 (PB-01 watchlist wiring and
  `set_eod_capture`), L3970 to L4075 (processor start, waitress thread, post-start self-check), L4200 to L4270
  (interactive banner, effect-telemetry registration, runtime wait, `_shutdown` call).
- `signals/signal_processor.py` L140 to L225 (constructor signature: `in_flight_release_fn`, `in_flight_heartbeat_fn`),
  and the `heartbeat` grep hits L172, L219, L661 to L673, L899, L1023, L1129, L1346, L1382.
- `core/config_loader.py` L192 to L215 (`SignalQueueConfig`), L617 to L650 (`WebhookConfig`), L1987 to L2200 (scanned
  for the `SystemConfig` fields `signal_queue` L1991, `excluded_symbols` L1993, `webhook` L2002), L2347 to L2395
  (`ScannerEntry`, `ScanWebhookMapConfig`, `ChartinkScannersConfig`), L2420 to L2470 (`AppConfig`, file registry,
  `load_all`) (A02 schemas, read at the boundary only).
- `config/system_config.yaml` L120 to L135 (`signal_queue`, `excluded_symbols`), L322 to L345 (`webhook`), L619 to L622
  (`watchlist`) (A02 file, read at the boundary only).
- `config/expected_managers.yaml` L147 to L156 (the `webhook_receiver` entry; text only).
- `config/scan_webhook_map.yaml` L1 to L84, every line except the `chartink_url` value lines (P07 owns the file's
  study; no URL value was read into this part).
- `deploy/install_vm_services.sh` L30 to L50 (A17; interface only).

### 1.2 Project records read (algocore_system, branch main, read-only)
- `A01_RECONCILED_TOPIC_RECORD_2026-11-06.md` sections 3, 4.2 and 15 (A06 row); `A01_AUDIT_2026-11-05.md` rows and
  entries C13, C15, C18, C20, C28, C32, C37, B-28, B-32, B-07, W-24, M-20, M-37, M-43, IS-9.14 (summary rows, detail
  entries where present, and the section 8 handoff table).
- The A06 investigation direction (17-Nov-2026), questions 1 to 28, and the A06 first fieldwork checkpoint
  (17-Nov-2026), as working inputs only.

### 1.3 Commands and search patterns (all read-only)
- `git -C <legacy clone> show 970aabf:<path>` for every file above; output filtered for identifier-shaped text and
  machine paths.
- `git ... grep -n -E` at `970aabf` with the four mandatory exclusion pathspecs (or the helper `the search wrapper`), patterns:
  `update_heartbeat|release_in_flight|in_flight_release|set_eod_capture|_eod_capture|webhook_receiver\b|WebhookReceiver`;
  `update_heartbeat` (whole repository, tests included, as HISTORICAL); `heartbeat` in `signals/signal_processor.py`
  and `main.py`; `webhook_receiver|webhook_thread|wh_cfg|WebhookReceiver|check_webhook_endpoint` in `main.py`;
  `excepthook`; `webhook_receiver\.app|\.app\.run\(|test_client\(`;
  `/webhook/|:5000|localhost:5000|<LOOPBACK>:5000|bind_port`.
- `git ... log` (hash, date, subject only) for `signals/webhook_receiver.py`, `scripts/load_test_signals.py`,
  `scripts/test_webhook.py`; `git ... log -S in_flight_heartbeat` and `-S update_heartbeat` (whole history, and
  `-- main.py`); `git ... show --stat a826dfe` (subject, body and file list used; the command's output also showed an
  identifier-bearing author line, not reproduced); `git ... grep -n -E "^\s*raise\b"` and
  `"app\.config|ProxyFix|wsgi_app|before_request|after_request"` in `signals/webhook_receiver.py`;
  `the search wrapper 'kill-switch"|hard-kill"|route\('`; `git ... grep "body\[|body\.get\("` in the receiver.
- Python `ast.parse` of `signals/webhook_receiver.py` source text (class, function and module-level assignment line
  ranges). No legacy file was imported, executed, built or tested; no endpoint, URL, scanner or broker was contacted.

### 1.4 External pages read (current external context, read 17-Nov-2026)
- waitress, "Arguments to waitress.serve" (page states waitress 3.0.2):
  https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html
- waitress documentation index (3.0.2): https://docs.pylonsproject.org/projects/waitress/en/latest/
- waitress "Design": https://docs.pylonsproject.org/projects/waitress/en/latest/design.html
- waitress "Usage": https://docs.pylonsproject.org/projects/waitress/en/latest/usage.html
- waitress "API": https://docs.pylonsproject.org/projects/waitress/en/latest/api.html
- waitress "Using Behind a Reverse Proxy": https://docs.pylonsproject.org/projects/waitress/en/latest/reverse-proxy.html
- Flask 3.1.x "Configuration Handling": https://flask.palletsprojects.com/config/
- Flask 3.1.x "Handling Application Errors": https://flask.palletsprojects.com/errorhandling/
- Flask 3.1.x "Uploading Files" (MAX_CONTENT_LENGTH): https://flask.palletsprojects.com/patterns/fileuploads/
- Werkzeug 3.1.x "Dealing with Request Data": https://werkzeug.palletsprojects.com/request_data/
- Werkzeug 3.1.x "WSGI Helpers" (`get_input_stream`, `LimitedStream`): https://werkzeug.palletsprojects.com/en/stable/wsgi/
- Python `threading` documentation source (3.13 or later): https://docs.python.org/3/_sources/library/threading.rst.txt
- Not reachable (permission not granted; not used): the waitress source file `src/waitress/__init__.py` at tag v3.0.2 on
  raw.githubusercontent.com. What it would have settled is listed in section 11.
- Added in the check (read 17-Nov-2026): Flask 3.1.x "Quickstart" (HTTP Methods: automatic HEAD and OPTIONS; Variable
  Rules: the default `string` converter): https://flask.palletsprojects.com/quickstart/ . Every page listed above
  except the waitress documentation index was re-opened in the check and the quoted text confirmed (the version 3.0.2
  is also stated by the "Arguments" page).
- Tried in the check, not retrievable (not used): pydantic's `pydantic/main.py` on GitHub (the `BaseModel.__getattr__`
  behaviour for P01-S011); the raw file was refused by the site and the rendered page did not reach the method.

### 1.5 Labels and limits
- Labels follow the sourcing and labelling rules. Every runtime fact (that a request arrived, a thread ran, a row was written) is
  UNKNOWN / NOT ESTABLISHED: no production log, database or journal is admitted.
- The installed versions of Flask, Werkzeug and waitress on the legacy machines are UNKNOWN / NOT ESTABLISHED;
  `requirements.txt` pins `flask==3.1.3` (L10) and `waitress==3.0.2` (L12) and does not pin Werkzeug (section 7).
- Security: the WR4b docstring (`signals/webhook_receiver.py` L112 to L128) carries account identifiers; it is described
  by its logic only and nothing from it is reproduced. The webhook secret is named by its variable only
  (`WEBHOOK_SECRET`). No credential, account, overlay or token file was opened.

## 2. Module structure of `signals/webhook_receiver.py`

P01-S001. FACT (`signals/webhook_receiver.py` L1 to L1207; `git log` at `970aabf`): the file has 1,207 lines and 31
commits, the last `3b15bbf` (09-Sep-2026, "WR4b -- strip a leading account-tag prefix before the scan_name check"). The
first is `bcf03b5` (17-Apr-2026).

P01-S002. HISTORICAL (L1 to L36, module docstring): it describes the module as the "Flask-based HTTP entry point for
Chartink scanner webhooks" and lists locked decisions WR1 to WR17, among them WR2 ("Flask, single file; POST
/webhook/<scanner_name> + GET /health"), WR3 (constructor arguments), WR4 (payload fields `stocks`, `trigger_prices`,
`triggered_at`, `scan_name`), WR5 (response codes 200/400/401/403/404/503/500), WR11 ("each Flask request in its own
thread"), WR12 (`stop()` for graceful shutdown), WR13 ("webhook_audit row per POST regardless of outcome") and WR16
(screening, strategy lookup and order placement out of scope). A docstring is not proof of behaviour.

P01-S003. FACT (L37 to L57): imports are the standard-library modules `hashlib`, `hmac` (as `_hmac`), `json`, `queue`,
`re`, `sqlite3`, `threading`, `time`, `datetime`/`timedelta`, `pathlib.Path` and `typing`; third-party `yaml`,
`cachetools.TTLCache` and `flask` (`Flask`, `request`, `jsonify`); and four names from three project modules:
`core.ids.new_signal_id`, `core.time_authority.ist_timezone` and `now_ist`, and `core.account_registry.primary_account_tag`
(AR12, as the docstring at L121 names it). One more import is made at call time, inside `_record_eod_heartbeat`:
`utils.cron_heartbeat.record_heartbeat` (L825; P01-S056). The module does not import `core.exceptions` and raises no
project exception class (A01 M-20 side; section 9).

P01-S004. FACT (`ast.parse` of the source text): the module-level objects are one constant, one helper class, one
helper function and the receiver class. There is no module-level Flask app; each `WebhookReceiver` instance builds its
own app (L249).

| Object | Lines | What it is |
|---|---|---|
| `_RETRYABLE_STATUSES` | L66 | `frozenset({"QUEUE_FULL", "STORE_ERROR"})`: the per-symbol statuses that turn a batch answer into 503 (L733 to L734) |
| `_PerIpRateLimiter` | L69 to L108 | per-source-IP token bucket; methods `__init__` L79 to L84, `allow` L86 to L100, `_evict_idle` L102 to L108 (P03) |
| `_strip_account_prefix` | L111 to L138 | WR4b helper: strips a leading account-tag prefix from a normalised scan name (section 4.4) |
| `WebhookReceiver` | L141 to L1207 | the receiver class (methods below) |

P01-S005. FACT (`ast.parse`; call sites by `grep`): the `WebhookReceiver` methods, their lines and their callers.

| Method | Lines | Role | Called from |
|---|---|---|---|
| `__init__` | L152 to L252 | builds state, starts the sweeper, loads aliases, builds dedup cache, limiter and Flask app | `main.py` L3407 |
| `_load_symbol_aliases` | L258 to L292 | reads `config/symbol_aliases.yaml` once | L227 |
| `_authenticate` | L298 to L354 | the single auth decision (P02) | L387 (`/health`), L547 (`/webhook`) |
| `_register_routes` | L360 to L413 | registers `health` (L365 to L404), `webhook` (L407 to L408) and the 500 handler `internal_error` (L411 to L413) | L252 |
| `_cast_numeric_fields` | L419 to L471 | casts top-level numeric fields of the body (P02) | L600 |
| `_handle_webhook` | L477 to L534 | outer handler of `POST /webhook/<scanner_name>`: shutdown gate, per-IP limit, call, audit | L408 |
| `_process_request` | L536 to L745 | auth, scanner lookup, EOD branch, kill switch, backpressure, window, parse, per-symbol loop, response | L511 |
| `_handle_eod` | L751 to L804 | EOD route to the capture worker | L564 |
| `_record_eod_heartbeat` | L806 to L834 | one `pb01_capture` heartbeat per EOD alert (P03/P11 for storage) | L786, L801 |
| `_parse_eod_triggered_at` | L836 to L851 | EOD `triggered_at` parse | L767 |
| `_sanitize_payload_for_storage` | L857 to L886 | redacts the secret from the stored body copy (P02) | L688 |
| `_process_signal` | L892 to L1072 | per-symbol checks, claims, `signals` INSERT, queue put (P03) | L719 |
| `_claim_in_flight` | L1074 to L1091 | atomic in-flight claim (P03) | L934 |
| `_release_in_flight` | L1093 to L1096 | internal release (P03) | L944, L1000, L1014, L1031, L1067 |
| `release_in_flight` | L1102 to L1108 | public release for the processor (P03, P04) | `main.py` L3612 (passed as `in_flight_release_fn`) |
| `update_heartbeat` | L1110 to L1120 | refreshes an in-flight entry's `heartbeat_at` | no non-test caller (P01-S077) |
| `_write_audit` | L1126 to L1154 | one `webhook_audit` INSERT (P03) | L487, L497, L531 |
| `set_eod_capture` | L1156 to L1160 | late-binds the EOD capture worker | `main.py` L3747 |
| `stop` | L1166 to L1176 | sets the shutdown and sweeper-stop events | `main.py` L1686 |
| `_run_sweeper` | L1182 to L1207 | the in-flight sweeper loop | thread target, L217 to L220 |

P01-S006. HISTORICAL (L142 to L150, class docstring): it shows the receiver being served with
`receiver.app.run(host=config.webhook.bind_host, port=config.webhook.bind_port)`. INTERPRETATION: this usage text is
older than the server `main.py` actually starts, which is waitress `serve` (L3987 to L4000; section 5); the docstring
also names `config.webhook`, whereas the receiver itself falls back to `config.system.webhook` (P01-S011).

P01-S007. HISTORICAL against FACT (L16 against L380, L504): the WR5 list of response codes does not include 429,
which both routes return when the per-IP limiter refuses a request (P02 and P03 give the full status table).

P01-S117. FACT (added in the check; `git log 7d4970a..970aabf` per path and `git diff 7d4970a 970aabf` filtered for
changed lines): after the last recorded deployment (`686df1c` and `7d4970a`, both 02-Sep-2026; Decision Register D-21)
`signals/webhook_receiver.py` changed in one commit only, `3b15bbf` (WR4b; P01-S050); `requirements.txt`,
`scripts/load_test_signals.py`, `scripts/test_webhook.py`, `config/scan_webhook_map.yaml` and
`config/symbol_aliases.yaml` did not change; `main.py` changed in three commits (`1955ae1`, `8d27fdb`, `ea0e506`, all
10-Sep-2026), and none of its 42 added lines (none removed) contains `webhook`, `waitress`, `_shutdown(`,
`set_eod_capture`, `in_flight` or `signal_queue`; `config/system_config.yaml` (`5455ced`, 03-Sep-2026; `5f75c9b`,
10-Sep-2026) and `core/config_loader.py` (`5f75c9b`) changed in no line naming the `webhook`, `signal_queue`,
`excluded_symbols` or `watchlist` settings. INTERPRETATION: apart from WR4b, the receiver, its server wiring and its
repository settings at the baseline are the same as at the last recorded deployment. UNKNOWN / NOT ESTABLISHED: whether
production ran any commit after `7d4970a`.

## 3. Construction: `main.py` call site and the receiver's constructor

### 3.1 The call site (A01 owns `main.py`; the A06 side only)

P01-S008. FACT (`main.py` L3402 to L3404): the signal queue is built just before the receiver as
`queue.Queue(maxsize=app_config.system.signal_queue.capacity)`. The repository file sets `signal_queue.capacity: 300`
(`config/system_config.yaml` L125; A02 file; the effective value is UNKNOWN / NOT ESTABLISHED). The queue's behaviour
is P03's (put side) and P04's (get side).

P01-S009. FACT (`main.py` L3406 to L3415): the receiver is built with seven keyword arguments: `signal_queue` (the
queue above), `state_store=store`, `config=app_config`, `market_windows=market_windows`, `kill_switch=kill_switch`,
`logger=get_logger("webhook_receiver")` and `secret_token=os.environ.get("WEBHOOK_SECRET")`. The call runs to L3415
(the brief's L3413 ends one argument early; `secret_token` is at L3414). `eod_capture` is not passed, so it takes its
default `None` (L161). The comment at L3406 gives the reason for the order: "Create webhook_receiver first so we can
wire in_flight_release to signal_processor".

P01-S010. FACT (`main.py` L3407; indentation): the construction is a plain statement in the body of `_main_locked`,
with no local `try`. INTERPRETATION: an exception raised by the constructor (for example P01-S013's `ValueError`) ends
the start through A01's startup-failure path; that path is A01's (A01 RECONCILED TOPIC RECORD section 3).

### 3.2 The constructor, in execution order (L152 to L252)

P01-S011. FACT (L171 to L176; `core/config_loader.py` L2420 to L2434 and L2002): the constructor looks for the
`webhook` settings first at `config.webhook` and, if that is `None`, at `config.system.webhook`. `AppConfig`, the object
`main.py` passes, declares no `webhook` field (L2420 to L2434); `SystemConfig` declares `webhook: WebhookConfig`
(L2002). INTERPRETATION: in the `main.py` path the settings come from `config.system.webhook`, provided the
configuration object raises `AttributeError` for an undeclared name, which is the only case in which Python's
`getattr(..., None)` returns its default. HISTORICAL (L168 to L170, comment): "production passes AppConfig (has .system
.webhook.require_hmac)"; a comment is not proof. `requirements.txt` L7 pins `pydantic==2.13.0`. Current external context (pydantic's published source
at tag v2.13.0, `pydantic/main.py`, `BaseModel.__getattr__`, read 17-Nov-2026 by P08 and again at assembly): for a name
that is not a private attribute, not an extra field and not a class attribute it ends by raising `AttributeError`.
INTERPRETATION (as P08-S006 and P08-S071 record): `AppConfig` declares no `webhook` field and forbids extras
(`core/config_loader.py` L2420 to L2434), so under pydantic 2.13.0 `getattr(config, "webhook", None)` returns `None` and
the receiver takes `config.system.webhook` (L173 to L175); the installed pydantic version is UNKNOWN / NOT ESTABLISHED
(A02 owns the object). The same resolved object supplies `require_hmac` (L176), `dedup_window_seconds` (L233) and the
per-IP limiter settings (L241 to L244).

P01-S012. FACT (L176): `require_hmac` is read with `getattr(_webhook_cfg, "require_hmac", False)`; absent means
`False`. The repository file sets `require_hmac: false` (`config/system_config.yaml` L336; effective value UNKNOWN).

P01-S013. FACT (L177 to L182): if `require_hmac` is true and `secret_token` is empty, the constructor raises
`ValueError`. The authentication consequences are P02's.

P01-S014. FACT (L184 to L200): the constructor keeps references to the queue (`_queue`), the store (`_store`), the
configuration (`_config`), the market windows (`_mw`), the kill switch (`_ks`), the logger (`_log`), the secret
(`_secret`), the EOD capture worker (`_eod_capture`, `None` from `main.py`) and `_require_hmac`.

P01-S015. FACT (L206 to L208): in-flight state is a dict `_in_flight` (symbol to `acquired_at` and `heartbeat_at`
monotonic times), a `threading.Lock` and a timeout `_in_flight_timeout_sec = 60.0`. The 60 s is a literal in the code;
no configuration key sets it.

P01-S016. FACT (L213): `_shutting_down` is a `threading.Event`, initially clear; only `stop()` sets it (L1172).

P01-S017. FACT (L216 to L220): the constructor creates a second event, `_sweeper_stop`, and a thread named
`in_flight_sweeper` with target `_run_sweeper` and `daemon=True`, and starts it at L220. The sweeper therefore runs from
the moment `main.py` L3407 constructs the receiver (A01 C13, P01-S095).

P01-S018. FACT (L227; L258 to L292): after the sweeper has started, the constructor loads the alias map once from the
relative path `config/symbol_aliases.yaml`. A missing file logs a WARNING and gives an empty map (L266 to L271); any
exception while reading or converting logs an ERROR and gives an empty map (L287 to L292); otherwise every key and value
with a true value on both sides is converted with `str(...).upper()` (L277 to L281) and the count is logged at INFO.
INTERPRETATION: the relative path is resolved against the process working directory, whereas the configuration loader
takes a directory argument (`core/config_loader.py` L2457); the working directory of the production process is UNKNOWN /
NOT ESTABLISHED (A17's unit). The map is never reloaded during the process's life (no other assignment to
`_alias_map` in the file). How the map is applied is in P01-S039 and P01-S052; normalisation across handoffs is P04's;
A05 owns the alias tool and A02 the file (A05 IR-10, IR-13).

P01-S019. FACT (L232 to L238): the dedup window is `int(dedup_window_seconds)` with default 300 on a missing key or a
conversion error, floored at 60 (`max(60, ...)`), and a `TTLCache(maxsize=10000, ttl=<window>)` with its own lock is
built. Detail is P03's.

P01-S020. FACT (L241 to L247): if `per_ip_rate_limit_enabled` (default true) the constructor builds
`_PerIpRateLimiter(per_ip_burst or 60, per_ip_refill_per_sec or 5.0)`, otherwise `_ip_limiter = None`. The repository
file sets `true`, 60 and 5.0 (`config/system_config.yaml` L340 to L342). Detail is P03's.

P01-S021. FACT (L249 to L252): the constructor builds `self.app = Flask(__name__)`, sets `TESTING = False` and
`MAX_CONTENT_LENGTH = 1 * 1024 * 1024` (1,048,576 bytes; comment "FIX-077: 1MB hard limit prevents OOM") and calls
`_register_routes()`. No other Flask configuration key is set in the file (no `DEBUG`, no `PROPAGATE_EXCEPTIONS`, no
proxy middleware).

P01-S022. INTERPRETATION (L220 against L227 to L252): the sweeper is started before the rest of the construction. The
later steps are guarded (L273 to L292, L232 to L235) or read schema-validated values (`core/config_loader.py` L626 to
L642), so a failure after L220 is unlikely; if one occurred, the daemon sweeper would keep running in a process whose
start is failing. Recorded for completeness; no runtime evidence.

### 3.3 Late binding of the EOD capture worker (Rama's decision D: routing and contract only)

P01-S023. FACT (`main.py` L3477 to L3478, L3712 to L3755; `config/system_config.yaml` L619 to L620): the PB-01 capture
worker is built only when `system.watchlist.enabled` is true (repository file: `enabled: true`; effective value UNKNOWN).
Then `main.py` builds a `WatchlistCaptureWorker` (L3734 to L3737), calls `webhook_receiver.set_eod_capture(...)` at
L3747, and only afterwards starts the worker (L3748) and the entry stage (L3749). When the flag is false nothing is
built and the receiver keeps `_eod_capture = None` (L3756 to L3763).

P01-S024. FACT (L1156 to L1160): `set_eod_capture` only assigns `self._eod_capture`; it takes no lock and does no
check. FACT (`main.py` L3752 to L3755): if any statement in the wiring block raises, the `except` sets the local
`pb01_capture_worker` and `pb01_entry_stage` to `None` but does not call `set_eod_capture(None)`. INTERPRETATION: if
L3748 or L3749 raised after L3747, the receiver would keep a reference to a worker that `main.py` no longer tracks and
that `_shutdown` is then not asked to stop (it is passed `pb01_capture_worker=None`). This is the receiver side of A01
C37 ("partial wiring after an optional-feature failure"; the capture worker's ownership is A18's). No runtime evidence.

## 4. Routes and the request flow from receipt to response

### 4.1 The routes

P01-S025. FACT (L364, L406, L410): `_register_routes` registers exactly two routes and one error handler on the
instance's app.

| Route | Methods | Handler | Lines |
|---|---|---|---|
| `/health` | GET | `health()` (inner function) | L364 to L404 |
| `/webhook/<scanner_name>` | POST | `webhook(scanner_name)`, which returns `receiver._handle_webhook(scanner_name)` | L406 to L408 |
| error handler for 500 | (any) | `internal_error(exc)`: CRITICAL log, JSON `{"error": "Internal server error"}`, 500 | L410 to L413 |

P01-S026. FACT (`the search wrapper 'kill-switch"|hard-kill"|route\('` at `970aabf`, non-test code): the receiver's app has no other
route. The only other `route(` declarations outside the operations dashboard are in `scripts/healthcheck_server.py`
(L69, L133, L263; a separate server on port 8080, A15 and A01) and `scripts/test_webhook.py` (L7; A19). This is the
receiver side of A01 IS-9.14: no `POST /kill-switch` or `POST /hard-kill` route exists on the receiver at the baseline.

P01-S027. INTERPRETATION, current external context (Flask 3.1.x "Handling Application Errors", read 17-Nov-2026: "If a
route receives an unallowed request method, a '405 Method Not Allowed' ... will be raised"; HTTP exceptions without a
registered handler "show a generic message about their code"): a POST to `/health`, a GET to `/webhook/<name>` or any
unregistered path is answered by Flask's routing with 405 or 404 and a generic error page, because the file registers
no 404 or 405 handler. Such requests never enter `_handle_webhook`, so they write no `webhook_audit` row and are not
counted by the per-IP limiter. The automatic HEAD and OPTIONS methods are in P01-S118 (settled in the check).

P01-S028. FACT (L406 to L408): the route declares no converter for `<scanner_name>`; the handler receives it as a
string and passes it unchanged to `_handle_webhook`. The path segment is never lower-cased or otherwise normalised
before the scanner lookup (L553). Current external context (Flask 3.1.x "Quickstart", Variable Rules, read
17-Nov-2026: `string` "(default) accepts any text without a slash") and INTERPRETATION: a path with a further slash
after `/webhook/` does not match the route and is answered by Flask's routing (P01-S027), not by the receiver.

P01-S118. INTERPRETATION, current external context (added in the check; Flask 3.1.x "Quickstart", HTTP Methods, read
17-Nov-2026: "If `GET` is present, Flask automatically adds support for the `HEAD` method ... Likewise, `OPTIONS` is
automatically implemented for you"; the file sets no `provide_automatic_options` and no `methods` other than those at
L364 and L406): `/health` also answers HEAD, which runs the `health()` view (limiter, then authentication, with the
same status as a GET; Flask handles HEAD "according to the HTTP RFC", which INTERPRETATION means no body), and both routes answer OPTIONS from Flask itself, without entering the receiver's code: an OPTIONS
request is not limited, not authenticated and writes no `webhook_audit` row. The installed Flask version is UNKNOWN
(the pin is 3.1.3, P01-S085).

### 4.2 `POST /webhook/<scanner_name>`: the outer handler `_handle_webhook` (L477 to L534)

P01-S029. FACT (L478 to L481): the handler first records a monotonic start time, takes
`source_ip = request.remote_addr or "unknown"`, reads the whole body with `request.get_data()` and takes its length.
The body is read before the shutdown check (L485) and before the per-IP limiter (L495), and outside the `try` that
starts at L510.

P01-S119. FACT (added in the check; `git grep -n -E "request\.|content_type|mimetype|get_json|\.form\b"` in the
receiver): the receiver reads only four things from the Flask `request`: `remote_addr` (L376, L479), `get_data()`
(L480), the `X-Webhook-Signature` header (L333) and the `token` query parameter (L334). It never reads the
Content-Type, `request.form`, `request.json` or `request.get_json()` (the `get_json` at L515 is called on its own
response object); the raw bytes go to `json.loads` (L587, L758) whatever type the sender declares. UNKNOWN / NOT
ESTABLISHED: what `get_data()` returns for a form-encoded or multipart body (the Werkzeug 3.1.x "Dealing with Request
Data" page, read 17-Nov-2026, describes form parsing on access of `form`, `files` or `stream` without settling this
case). The payload format Chartink sends is P07's; validation is P02's.

P01-S030. INTERPRETATION, current external context (Flask 3.1.x "Configuration Handling", MAX_CONTENT_LENGTH: "If this
limit is exceeded, a 413 RequestEntityTooLarge error is raised"; Werkzeug 3.1.x "WSGI Helpers", `get_input_stream`: a
Content-Length over the limit raises `RequestEntityTooLarge`, and a stream without Content-Length is limited only when
the server sets `wsgi.input_terminated`, otherwise an empty stream is returned; read 17-Nov-2026): a request whose
declared length exceeds 1,048,576 bytes (P01-S021) fails at L480. Because L480 is outside the `try`/`finally` of L510
to L534, the 413 leaves the view, Flask answers with its generic 413 page (no handler for 413 is registered), no
`webhook_audit` row is written and the limiter is not consulted. A body sent without Content-Length would be limited or
read as empty depending on whether waitress 3.0.2 sets `wsgi.input_terminated`, which was not established (section 11).
Werkzeug 3.1.x "Dealing with Request Data" (read 17-Nov-2026) adds that "clients may show a 'connection reset' failure
instead of the 413 error".

P01-S031. FACT (L485 to L490): while `_shutting_down` is set, every request gets a `webhook_audit` row (code 503, 0
accepted, 0 rejected) and the answer `{"error": "Service shutting down; retry later"}` with status 503.

P01-S032. FACT (L495 to L504): if the limiter exists and refuses `source_ip`, the handler writes a `webhook_audit` row
(429), logs a WARNING and answers `{"error": "Rate limit exceeded; slow down"}` with 429. The limiter itself is P03's.

P01-S033. FACT (L506 to L534): otherwise the handler calls `_process_request(scanner_name, raw_body)` inside a `try`.
It takes the status from the returned tuple (every return in `_process_request` and `_handle_eod` is a
`(response, status)` tuple, so the default 200 for a non-tuple at L512 is never used). For a 200 only, it reads
`accepted` and `rejected` back from the response JSON (L514 to L517); for any other status the counts stay 0. For a 400
it logs the first 1,000 bytes of the raw body at WARNING (L519 to L523; the storage sanitiser of L688 applies only to the
stored copy, P02). Any exception from `_process_request` is logged at CRITICAL and answered with
`{"error": "Internal server error"}` and 500 (L525 to L528). The `finally` writes one `webhook_audit` row with the
status, the two counts and the duration (L529 to L534; P03 for the write).

### 4.3 `_process_request` (L536 to L745): the order of checks and the parse into an internal signal

P01-S034. FACT (L536 to L745): the checks run in this fixed order; the first failure answers and ends the request.

| Step | Lines | Check or action | Failure answer |
|---|---|---|---|
| 1 | L547 to L549 | `_authenticate(raw_body)` (P02) | 401, `{"error": <reason>}` |
| 2 | L552 to L554 | `scanner_name` is a key of `config.scan_webhook_map.scanners` | 404, `{"error": "Unknown scanner: '<name>'"}` |
| 3 | L562 to L564 | the entry's `scanner_type` is `"eod"` (default `"intraday"`) | goes to `_handle_eod` (section 4.5) |
| 4 | L567 to L568 | kill switch present and active | 403, `{"error": "Kill switch active; signals rejected"}` |
| 5 | L571 to L578 | queue size `>= int(capacity * backpressure_pct)` (P03) | 503 with `X-Queue-Depth` |
| 6 | L581 to L583 | `market_windows.is_entry_allowed(now_ist())` | 403, `{"error": "Outside entry window"}` |
| 7 | L586 to L593 | `json.loads(raw_body)` | 400, `{"error": "Malformed JSON: ..."}` (WARNING with first 500 raw bytes) |
| 8 | L595 to L596 | body is a JSON object | 400 |
| 9 | L600 to L606 | `_cast_numeric_fields(body)` (P02) | 400, `{"error": "Invalid payload: ..."}` |
| 10 | L609 to L615 | `stocks`, `trigger_prices`, `triggered_at` present | 400, `Missing required field` |
| 11 | L620 to L633 | WR4 and WR4b scan-name check (section 4.4) | 400 |
| 12 | L637 to L662 | `triggered_at` parse, three formats, IST attached (P02) | 400, `Invalid triggered_at ...` |
| 13 | L665 to L674 | `stocks` and `trigger_prices` are strings; split on commas and stripped; equal counts | 400 |
| 14 | L677 to L679 | `received_at = now_ist()`, `today_iso`, `expiry_sec = signal_queue.expiry_sec` | none |
| 15 | L688 to L690 | sanitised copy of the body for storage (P02) | none |
| 16 | L696 to L728 | per symbol: alias, excluded-symbol check, `_process_signal` | per-symbol status |
| 17 | L733 to L745 | batch answer | 503 if any status is retryable, else 200 |

P01-S035. FACT (L552 to L554): the scanner lookup is an exact dictionary-key test on the path segment, before the EOD
branch, the kill switch and the window. The repository map holds 16 keys, 15 without `scanner_type` and one
(`pb01_breakout_retest`) with `scanner_type: eod` (`config/scan_webhook_map.yaml` L16 to L84; P07 studies the file).

P01-S036. FACT (L562 to L564, L567 to L583): the EOD branch is taken before the kill-switch, backpressure and
entry-window checks, so an EOD alert is not subject to any of them. For intraday scanners the window check uses a fresh
`now_ist()` (L581) and `MarketWindows.is_entry_allowed` (A01's class; A01 B-36 records that the class leaves the IST
contract of `now` to its callers and that every non-test caller found passes `now_ist()` or a value from it, a MATCH;
the receiver's call at L581-L582 is of that kind).

P01-S037. FACT (L567 to L606): the body is parsed only after authentication, the scanner lookup, the kill switch,
backpressure and the window. INTERPRETATION: a malformed body sent while the kill switch is active, the queue is over its
threshold or the window is closed is answered 403 or 503, not 400.

P01-S038. FACT (L586 to L745, L892 to L1072): there is no signal class or object at the receiver. The parse produces
local values: the path segment `scanner_name`, the `symbols` and `price_strs` lists, the IST-aware `triggered_at`,
`received_at`, `today_iso`, `expiry_sec` and the sanitised `stored_payload`. Body fields other than `stocks`,
`trigger_prices`, `triggered_at` and `scan_name` are not read after the numeric cast: on the intraday path the only
reads of body values are L620, L637, L665 and L666 (`grep "body\[|body\.get\("`; L604 and L613 log only the key
names; the EOD path's reads are L767 and L771), so the cast fields (`price`, `entry_price`, `trigger_price`,
`sl_pct`, `target_pct`, `qty`) are converted and then unused. Per symbol, `_process_signal` creates the `signal_id`, the
fingerprint, the `signals` row and the queue item (P01-S041, P01-S042).

P01-S039. FACT (L701 to L706): the alias lookup is `self._alias_map.get(raw_symbol.upper(), raw_symbol)`: the raw
symbol is upper-cased for the lookup only. On a hit the symbol becomes the mapped value (upper-cased at load, L278); on a
miss the raw symbol is kept exactly as received, without upper-casing. A DEBUG line is logged when the alias changed the
symbol. INTERPRETATION: a lower-case symbol that is not in the map continues in lower case to the excluded check, the
in-flight claim, the dedup key, the `signals` row and the queue item.

P01-S040. FACT (L709 to L717): after the alias, the symbol is compared case-insensitively with
`config.system.excluded_symbols` (default `[]`; repository list at `config/system_config.yaml` L131 onwards); a match is
answered per symbol with `REJECTED_EXCLUDED_SYMBOL`, counted as rejected, logged at DEBUG, and writes no `signals` row.
The list is re-read and re-upper-cased for every symbol. Validation detail is P02's.

P01-S041. FACT (L892 to L1072): `_process_signal` applies, in order: an empty symbol gives `INVALID_SYMBOL` (L905 to
L906); a price that is not a float or is not above 0 gives `INVALID_PRICE` (L909 to L914); an age `now_ist() -
triggered_at` above `expiry_sec` gives `EXPIRED` (L919 to L926); a failed in-flight claim gives `IN_PROCESS` (L934 to
L935); a hit in the TTL dedup cache gives `DUPLICATE` (L940 to L947); then it computes the fingerprint (L952 to L954)
and a new `signal_id` (L957), inserts a `signals` row with status `QUEUED` (L963 to L980), handles an `IntegrityError`
(re-queue of a `QUEUE_FULL` row, or `DUPLICATE`; L981 to L1015) and any other store error (`STORE_ERROR`; L1016 to
L1044), puts the item on the queue without blocking (L1047 to L1049), handles `queue.Full` (`QUEUE_FULL`; L1050 to
L1068) and returns `ACCEPTED` with the `signal_id` (L1072). The checks and their side effects are P02's (symbol, price),
P03's (claims, dedup, store, queue) and P04's (expiry on both sides).

P01-S042. FACT (L1047; L993): the item put on the queue, and so the receiver-to-processor contract, is the 5-tuple
`(signal_id, scanner_name, symbol, price, triggered_at)`: the new or re-used signal id, the path segment (not the
strategy), the symbol after the alias, the price as a float and the IST-aware `triggered_at` as parsed. P04 studies the
consumer side.

P01-S043. FACT (L966 to L979): the `signals` INSERT writes the path segment into both the `scanner` and the `strategy`
columns; the receiver does not look up the strategy that `scan_webhook_map` assigns (WR16, L28). FACT
(`config/scan_webhook_map.yaml` L17 to L84): in the repository file every key equals its `strategy` value.
INTERPRETATION: the two values coincide while that holds. The storage side is P03's and P11's; the processor's own
lookup is P04's.

P01-S044. FACT (L733 to L745): the batch answer is 503 if any per-symbol status is `QUEUE_FULL` or `STORE_ERROR`
(`_RETRYABLE_STATUSES`), otherwise 200, with the JSON body `{"accepted": n, "rejected": m, "results": [...]}` (each
result holds `symbol` and `status`, and `signal_id` when accepted), the header `X-Queue-Depth: <size>/<capacity>`, and
`X-Queue-Warning: high` when the depth is at or above `int(capacity * warning_pct)`. INTERPRETATION (L514 to L517
against L734): for a 503 batch the audit row records 0 accepted and 0 rejected, even if some symbols in that batch were
accepted and queued.

P01-S045. FACT (L670 to L671, L905 to L906; L774): the intraday split keeps empty elements, so a trailing or doubled
comma yields an empty symbol answered `INVALID_SYMBOL` (and an empty price string, which would be `INVALID_PRICE` if the
symbol were present). The EOD split drops empty elements (L774).

P01-S046. FACT (L581, L645, L677, L919): one intraday request reads the clock three times: `now` for the window check and
for the date given to a time-only `triggered_at` (L581, L645), `received_at` for the stored times and `expires_at`
(L677, L958 to L961), and a fresh `now` inside `_process_signal` for each symbol's age test (L919). Expiry is P04's.

### 4.4 The scan-name check (WR4) and the account-prefix strip (WR4b)

P01-S047. FACT (L620 to L633): `scan_name` is optional. If it is present and not `None`, it is normalised with
`.lower().replace(" ", "_")`, passed through `_strip_account_prefix`, and compared for exact equality with the path
segment. A mismatch logs a WARNING (body value, normalised value, value after the strip, path) and answers 400
`{"error": "scan_name in body does not match scanner_name path param"}`. When `scan_name` is absent the request
continues with the path segment alone.

P01-S048. FACT (L622): the normalisation lower-cases and replaces each space with one underscore; it does not strip,
and it does not change hyphens, tabs or other characters. INTERPRETATION: a value with a trailing space or a doubled
space produces an extra underscore and is answered 400; a `scan_name` that is not a string (a number, for example) has
no `.lower()`, raises `AttributeError`, and is answered 500 by the `except` at L525 rather than 400. Recorded as a code
fact; intent is for the AUDIT.

P01-S049. FACT (L111 to L138, L626): `_strip_account_prefix` reads the tag as
`(primary_account_tag() or "").strip().lower()` on every call. If the tag is empty or equals `"unknown"` the value is
returned unchanged. Otherwise, for the separators `-` and `_` in that order, a value that starts with `<tag><sep>`
loses that prefix and the remainder is returned; only the first matching prefix is removed. The remainder must still
equal the path segment exactly (L627). INTERPRETATION: because spaces have already become underscores, an alert name
whose tag is followed by a space is also stripped (by the `_` separator).

P01-S050. HISTORICAL (L112 to L128, docstring; commit `3b15bbf`, 09-Sep-2026): the docstring gives the reason for WR4b
(alert names are per account on a shared Chartink login, so on the testing machine they carry an account prefix while
the webhook path does not, and WR4 then answered 400 to every signal there), states that the tag comes from the account
file through AR12 and is not hard-coded, states that the strip is a no-op on production, and insists on "PREFIX ONLY".
The identifiers in the docstring are not reproduced. Whether production alert names carried any prefix is UNKNOWN /
NOT ESTABLISHED. `3b15bbf` is later than the last recorded deployment (`686df1c` and `7d4970a`, both 02-Sep-2026;
Decision Register D-21), so whether production
ran WR4b is UNKNOWN / NOT ESTABLISHED (P01-S117).

P01-S051. FACT (A01 AUDIT M-37 and M-43, receiver side): the receiver depends on AR12 `primary_account_tag` for a
validation step; A01 recorded that AR12 caches its first result, including its "UNKNOWN" fallback, for the life of the
process, and reads the account file at a path fixed relative to its module, independent of `--config`
(`core/account_registry.py` L273 to L318, as A01 recorded it). FACT (L130 to L133): the receiver treats the lower-cased
fallback `"unknown"` as no tag. INTERPRETATION: if the first AR12 call in a process returned the fallback, WR4b stays a
no-op for that process and a prefixed `scan_name` is answered 400. A01's IDs are kept.

### 4.5 The EOD route to the capture worker (Rama's decision D: routing and payload only)

P01-S052. FACT (L564, L751 to L792): `_handle_eod` is reached after authentication (L547) and the scanner lookup (L553)
only. It parses the body as JSON (400 on failure), requires a JSON object (400) and the fields `stocks`,
`trigger_prices` and `triggered_at` (400; `trigger_prices` is required but never read), parses `triggered_at` with
`_parse_eod_triggered_at` (formats `%Y-%m-%d %H:%M:%S`, `%Y-%m-%d`, `%I:%M %p`, `%H:%M`; time-only values take today's IST
date; IST is attached to naive values; 400 `Invalid triggered_at` on failure; L836 to L851), requires `stocks` to be a
string (400), splits it on commas, strips and drops empty elements (L774), and applies the same alias rule as the
intraday path (L792, as in P01-S039). It does not apply the numeric cast, the scan-name check, the kill switch, the
backpressure check, the entry window, the excluded-symbol list, expiry, in-flight claims, deduplication, the `signals`
INSERT or the queue.

P01-S053. FACT (L778 to L788): when `_eod_capture` is `None`, the receiver logs a WARNING ("watchlist disabled ...
fail-safe miss"), records an EOD heartbeat with `status="FAILED"` and `functional_status="DISABLED"`, and answers 200
`{"accepted": 0, "captured": 0, "detail": "watchlist disabled"}`.

P01-S054. FACT (L790 to L800): otherwise, for each symbol, it calls
`self._eod_capture.submit(scanner_name=<path segment>, symbol=<symbol after alias>, triggered_at=<IST-aware datetime>)`.
A truthy return counts as captured; an exception from `submit` is logged at ERROR for that symbol and the loop
continues. This keyword call is the whole contract the receiver passes to the worker; the worker
(`v3_chain/watchlist_capture.py`) is A18's.

P01-S055. FACT (L801 to L804; L514 to L517): after the loop the receiver logs at INFO, records an EOD heartbeat
(`status="SUCCESS"`, `functional_status="EMPTY_NO_DATA"` when nothing was captured, else `None`) and answers 200
`{"accepted": <number of symbols>, "captured": <number captured>}`. INTERPRETATION: once the body parses, the EOD answer
is always 200, whatever the worker did; the audit row then records `accepted` as the number of symbols and `rejected`
as 0 (the body has no `rejected` key).

P01-S056. FACT (L806 to L834): `_record_eod_heartbeat` imports `utils.cron_heartbeat.record_heartbeat` at call time and
calls `record_heartbeat("pb01_capture", status=..., functional_status=..., message="scanner=<name> symbols=<n>
queued=<m>")`; every exception is swallowed, with a best-effort WARNING. HISTORICAL (L812 to L817): the docstring says
the count is of symbols queued for capture, not captured. The storage behind `record_heartbeat` is A03's; the write is
recorded by P03 and P11.

P01-S057. FACT (L751 to L804): the EOD route keeps no receiver-side record of earlier EOD alerts, so a repeated alert
is submitted again; any deduplication is the worker's (A18). The shutdown gate (L485) and the per-IP limiter (L495)
apply to EOD requests, because they run in `_handle_webhook` before `_process_request`.

### 4.6 `GET /health` (L364 to L404)

P01-S058. FACT (L376 to L404): `/health` takes `source_ip` from `request.remote_addr`, applies the same per-IP limiter
(429 `{"error": "rate limit exceeded"}`), then `_authenticate(b"")` (401 `{"error": "authentication required"}`, the
granular reason discarded; P02), then answers 200 with `status`, `kill_switch_active`, `queue_size`,
`queue_capacity` (from `config.system.signal_queue.capacity`) and `queue_depth`. It does not check `_shutting_down` and
writes no `webhook_audit` row. INTERPRETATION: `/health` keeps answering 200 after `stop()` has been called, while
`/webhook` answers 503.

P01-S059. FACT (`main.py` L4004 to L4005; A01 AUDIT C28): the boot self-check calls
`http://<LOOPBACK>:<bind_port>/health` through `check_webhook_endpoint`, which counts a 2xx or a 401 as reachable
(`utils/startup_checks.py` L789 to L809, as A01 recorded it). FACT (L330 to L354, L387 to L393): with a secret
configured, a request to `/health` without a valid signature or token is answered 401. INTERPRETATION: the self-check
shows that something answers on the port, not that the receiver's authentication passes.

### 4.7 The 500 handler

P01-S060. FACT (L250, L410 to L413) and current external context (Flask 3.1.x "Handling Application Errors" and
"Configuration Handling", read 17-Nov-2026: a handler registered for 500 "will be passed uncaught exceptions"; in debug
mode the 500 handler is not used; `TESTING` and `DEBUG` default to false and `PROPAGATE_EXCEPTIONS` is implicitly true
only if one of them is enabled): with `TESTING = False` and no `DEBUG` setting in the file, an exception that escapes a
view reaches `internal_error`, which logs CRITICAL and answers JSON 500. INTERPRETATION: on the `/webhook` route this
covers only L478 to L504 (the `try` at L510 catches everything from `_process_request`); on `/health` it covers the whole
handler (for example a kill-switch or queue call that raises). A 413 or other HTTP exception is not a 500 and gets
Flask's generic page (P01-S027, P01-S030). Current external context (same Flask page, read 17-Nov-2026: "As of Flask
1.1.0, this error handler will always be passed an instance of `InternalServerError`, not the original unhandled
error. The original error is available as `e.original_exception`") and INTERPRETATION (L412): the CRITICAL line
formats the `InternalServerError` it receives, so it carries Flask's generic 500 text, not the original exception's
message; the handler does not read `original_exception`.

## 5. The server: waitress in the thread "webhook-server" (`main.py` L3979 to L4054)

P01-S061. FACT (`main.py` L3979): the server settings are read directly as `wh_cfg = app_config.system.webhook` (not
through the receiver's fallback of P01-S011).

P01-S062. HISTORICAL (`main.py` L3980 to L3981): the comment says FIX-081 removed the port-conflict check because the
instance lock "already binds a persistent socket lock". A01 B-32 recorded that the lock binds a different port, so the
webhook port is not pre-checked (A01's ID kept; section 9).

P01-S063. HISTORICAL (`main.py` L3983 to L3986): the comment says waitress replaced Flask's development server because
it "drops connections under burst load (Chartink can fan out 50+ signals in a sub-second window)".

P01-S064. FACT (`main.py` L3987 to L4000): `main.py` imports `serve` from waitress at that point (a lazy import inside
`_main_locked`) and starts a `threading.Thread` with `target=_waitress_serve`, `args=(webhook_receiver.app,)`,
`kwargs={"host": wh_cfg.bind_host, "port": wh_cfg.bind_port, "threads": 8, "connection_limit": 100}`,
`name="webhook-server"` and `daemon=True`; the thread is started at L4000. These four are the only waitress arguments
passed. `threads` and `connection_limit` are literals in `main.py`, not configuration keys.

P01-S065. FACT (`config/system_config.yaml` L327 to L335; `core/config_loader.py` L619 to L620): the repository file
sets `bind_host: "<ALL_INTERFACES>"` (all IPv4 interfaces) and `bind_port: 5000`; the effective values are UNKNOWN / NOT
ESTABLISHED. In the schema both fields are required and have no default; the comments there ("default
\"<LOOPBACK>\"", "default 5000") describe defaults the schema does not implement (HISTORICAL comment against FACT).

P01-S066. HISTORICAL against FACT (`config/system_config.yaml` L328 to L336): the comment on `bind_host` says the
all-interfaces bind "relies on require_hmac=true plus firewall/security-group restrictions"; the same file sets
`require_hmac: false` (L336), with the comment that Chartink cannot sign payloads and the `?token=` route is used. The
comment and the value disagree; authentication is P02's and A02-13's.

P01-S067. FACT and current external context (waitress "Arguments to waitress.serve", page for waitress 3.0.2, the
pinned version; read 17-Nov-2026): `threads` is "The number of threads used to process application logic" (default 4;
`main.py` passes 8); `connection_limit` means "Stop creating new channels if too many are already active" (default 100;
`main.py` passes 100, the default). Every other argument takes its documented default, among them `channel_timeout`
120 s ("Maximum seconds to leave an inactive connection open"), `max_request_header_size` 262,144 bytes,
`max_request_body_size` 1,073,741,824 bytes, `expose_tracebacks` False ("Set to True to expose tracebacks of unhandled
exceptions to client"), `backlog` 1024, `trusted_proxy` None, `clear_untrusted_proxy_headers` True (changed to True in
3.0.0) and `ident` "waitress" (the `Server:` header).

P01-S068. INTERPRETATION, current external context (waitress "Design", read 17-Nov-2026: I/O "is always done
asynchronously ... in the main thread"; "The thread dispatcher maintains a fixed pool of worker threads"; "When all
worker threads are in use, scheduled tasks will wait in a queue"): in this process the waitress I/O loop runs in the
thread that called `serve`, which is "webhook-server", and the receiver's Flask code runs on a fixed pool of eight
waitress worker threads. At most eight requests execute receiver code at the same time; further complete requests wait
for a free worker. HISTORICAL WR11 ("each Flask request in its own thread", L23) describes one thread per request; the
server actually used shares a fixed pool. Concurrency consequences are P03's.

P01-S069. FACT (`main.py` grep `webhook_thread`: L3988, L4000 only) and INTERPRETATION, current external context
(waitress "Usage": "Press Ctrl-C (or Ctrl-Break on Windows) to exit the server", no programmatic stop described;
Python `threading`: "Daemon threads are abruptly stopped at shutdown"; read 17-Nov-2026): `main.py` keeps only the
thread object, never refers to it after L4000, and holds no server object; the receiver holds no reference to the
server. Nothing in the repository stops the server; it ends when the process exits.

P01-S070. INTERPRETATION, current external context (Python `threading`: an exception from `run()` goes to
`threading.excepthook`, which prints it on `sys.stderr`; read 17-Nov-2026): no `excepthook` is set anywhere in the
non-test repository (`the search wrapper 'excepthook'`: no hit). If `serve` raised in the "webhook-server" thread (for example
because the port is taken), the traceback would go to stderr and the thread would end; `main.py` would learn of it only
through the self-check two seconds later (P01-S071). Where and how waitress 3.0.2 reports a bind failure was not read in
its source (section 11).

P01-S071. FACT (`main.py` L4002 to L4054): after a fixed `time.sleep(2)` the boot calls
`check_webhook_endpoint("http://<LOOPBACK>:<bind_port>/health", _http_fetch, _log)`. If it reports not reachable,
`main.py` logs CRITICAL ("DEGRADED: entries cannot arrive ...") and writes a critical sentinel (title "Webhook endpoint
unreachable at boot -- DEGRADED, still running"); a sentinel failure is logged at ERROR; the boot continues. A01 C28
recorded this: MATCH for the 2 s settle and the degrade; ISSUE (minor) for the `detail` read that is always `None` and
for no detection after boot (A01's ID kept). The receiver side is P01-S059.

P01-S072. FACT (`main.py` L3407, L3974 to L4000): the receiver object, and its sweeper, exist from L3407; the server
starts at L4000, after `signal_processor.start()` (L3974) and the starts of the entry gate, the target manager and the
target retry manager (L3975 to L3977). INTERPRETATION: between L3407 and L4000 no HTTP request can reach the receiver,
because nothing serves its app yet. The steps L3987 to L4000 are not inside a `try` (A01 C15; a failure of the lazy
import at L3987, for example, would end the start after workers have started; the consequence is A01's).

P01-S073. FACT (`main.py` L3612, L3747, L3990, L4210 to L4213, L4238, L4262): inside the process the receiver is
reachable only through: its app, passed to waitress (L3990); its bound method `release_in_flight`, passed to the
processor (L3612); the `set_eod_capture` call (L3747); and the object passed to `_shutdown` (L4262). The interactive
banner prints the configured port (L4210 to L4213), and effect telemetry registers the name `"webhook_receiver"` as
"covered-existing (webhook_audit)" (L4238).

P01-S074. FACT, interface only (`deploy/install_vm_services.sh` L33 to L45; A17): the install script inserts an
iptables rule accepting TCP port 5000 and its comment says the webhook listener has been bound to all interfaces on port
5000 "since commit 2d1e580". Whether the script ran, and the network path between Chartink and the port (the
configuration comment at L329 to L330 mentions "ngrok/external"), are UNKNOWN / NOT ESTABLISHED.

P01-S075. INTERPRETATION, current external context (waitress "Using Behind a Reverse Proxy": waitress sets
`REMOTE_ADDR` from trusted proxy headers only when `trusted_proxy` is configured; `trusted_proxy` defaults to None;
read 17-Nov-2026): `main.py` configures no trusted proxy and the receiver adds no proxy middleware, so
`request.remote_addr` (used for the limiter key and the audit's `source_ip`, L376, L479) is not derived from forwarding
headers. The page does not state what `REMOTE_ADDR` holds without a trusted proxy; if a tunnel or reverse proxy sat in
front of the port, whether the address seen would be the proxy's is UNKNOWN / NOT ESTABLISHED. The limiter is P03's.

## 6. Threads the receiver owns, `stop()` and shutdown

### 6.1 The in-flight sweeper

P01-S076. FACT (L1182 to L1207) and current external context (Python `threading`, `Event.wait`: returns True when the
flag is set, False when the timeout expires; read 17-Nov-2026): the sweeper loops
`while not self._sweeper_stop.wait(timeout=60.0)`. Its first pass is 60 s after construction and the passes are 60 s
apart (plus the pass's own time). Each pass takes the in-flight lock, collects every entry whose
`now - heartbeat_at` exceeds `_in_flight_timeout_sec` (60.0 s), deletes them, releases the lock and then logs one
CRITICAL line per evicted symbol: "in_flight_sweeper: evicted STALLED symbol ... signal_processor worker likely crashed
or deadlocked". The loop has no exception handling. INTERPRETATION: an exception inside a pass would end the thread
(reported through `threading.excepthook` on stderr) and nothing restarts it.

P01-S077. FACT (whole-repository `grep update_heartbeat`; `main.py` L3575 to L3623; `signals/signal_processor.py` L172,
L219, L664 to L673; `git log -S`): `update_heartbeat` (L1110 to L1120) has no caller outside the tests
(`tests/unit/test_webhook_receiver.py` L1448 to L1488) and one audit document. The processor accepts an
`in_flight_heartbeat_fn` (default `None`) and calls its `_heartbeat` helper at five checkpoints (L899, L1023, L1129,
L1346, L1382), but the helper does nothing when the callback is `None` (L669). `main.py` passes
`in_flight_release_fn=webhook_receiver.release_in_flight` (L3612) and does not pass `in_flight_heartbeat_fn`. No commit
in the history of `main.py` ever added or removed `in_flight_heartbeat` or `update_heartbeat` (`git log -S`, no hit).

P01-S078. HISTORICAL (commit `a826dfe`, 12-May-2026, "fix: FIX-011 heartbeat + test timestamp fix"): the message lists
"Wire heartbeat callback from WebhookReceiver to SignalProcessor"; the commit changed `signals/signal_processor.py`,
`signals/webhook_receiver.py` and `tests/unit/test_webhook_receiver.py` only, not `main.py`. HISTORICAL (L203 to L205,
L1184 to L1187): the comments say a claim that keeps heartbeating is not evicted ("A lock that has been held for 400s
but continues heartbeating is NOT evicted").

P01-S079. INTERPRETATION (P01-S076, P01-S077): with no heartbeat callback wired in `main.py`, `heartbeat_at` stays
equal to `acquired_at` for every claim, so the sweeper evicts every in-flight claim that is more than 60 s old when a pass
runs, whether or not a worker is still processing it, and logs it as STALLED at CRITICAL. A claim is otherwise released
by the receiver's reject paths or by the processor's release calls (`signals/signal_processor.py` L456 to L458, L1267
to L1271, L1699 to L1703, L1733 to L1737; P03 and P04). After such an eviction a second signal for the same symbol can
pass the in-flight claim while the first is still being processed (it may still be stopped by the dedup layers, P03).
How long claims were held in production is UNKNOWN / NOT ESTABLISHED.

P01-S080. FACT (L1166 to L1176): `stop()` sets `_shutting_down` and `_sweeper_stop` and logs one INFO line ("new
requests will return 503"). It does not join the sweeper, does not stop or signal the waitress server, does not wait for
requests in progress, and does not release in-flight claims. Calling it twice only sets the events again.
INTERPRETATION (`Event.wait` semantics): the sweeper leaves its loop as soon as its current wait returns, after finishing
any pass in progress.

### 6.2 `main.py` shutdown (A01 owns `_shutdown`; the A06 side)

P01-S081. FACT (`main.py` L1629 to L1692): `_shutdown` first sets `_shutdown_event` (L1629), drains a hard-kill flatten
if one is running (L1643 to L1656), emits the effect census, which counts the day's `webhook_audit` rows (L1662 to L1675;
P03), and may invalidate the token (L1678 to L1679). Then, under the comment "H-16: stop webhook_receiver FIRST so new
webhooks return 503. In-flight requests drain naturally; signal_processor stop below still works on queued items"
(L1681 to L1683), it calls `webhook_receiver.stop()` inside a `try` that logs any error (L1684 to L1688) and immediately
calls `signal_proc.stop()` (L1689 to L1692). The receiver is the first subsystem stopped, not the first step of
`_shutdown`.

P01-S082. FACT (`main.py` L1718 to L1729): the PB-01 entry stage and capture worker are stopped later, under the comment
"After webhook_receiver.stop() above, so no new EOD alert can be captured" (L1719). INTERPRETATION: the `_shutting_down`
gate (L485) answers new EOD requests with 503; an EOD request already past L485 may still call `submit` on a worker that
is being stopped; the worker's behaviour is A18's.

P01-S083. FACT (`main.py` L1751, L1816, L1828): the comment at L1751 says "Flask has no clean stop (daemon thread dies
on process exit)"; the store is checkpointed at L1816 and closed at L1828. INTERPRETATION: after `stop()` the server
keeps accepting connections until the process ends; each new `/webhook` request still tries to write a `webhook_audit`
row (L487); if the store raises after `close()`, that write fails inside `_write_audit` and is logged at ERROR (L1153
to L1154), and the 503 answer is still returned. How the store behaves after `close()` is A03's (UNKNOWN here). `/health` keeps answering 200 (P01-S058).

P01-S084. INTERPRETATION (P01-S080, P01-S081; Python `threading`: "Daemon threads are abruptly stopped at shutdown",
read 17-Nov-2026): nothing waits for requests in progress, although the comments say they "drain naturally" (L211 to
L212; `main.py` L1682). A request that had passed L485 before `stop()` continues in its waitress worker thread while
`signal_proc.stop()` and the rest of `_shutdown` run. It may insert a `signals` row and put an item on the queue after
the processor has begun stopping (what happens to queued items at stop is P04's), or meet a closed store, or be cut
off when the process exits. Whether any request was in progress at any real shutdown is UNKNOWN / NOT ESTABLISHED.

## 7. Library versions and the waitress and Flask behaviour relied on

P01-S085. FACT (`requirements.txt` L6, L10 to L12): the runtime pins are `pyyaml==6.0.3`, `flask==3.1.3` ("WR2: webhook
HTTP server"), `cachetools==7.1.1` ("FIX-036: TTLCache for webhook deduplication") and `waitress==3.0.2` ("production
WSGI server ... replaces app.run"). Werkzeug, which supplies Flask's request parsing and HTTP exceptions, is not pinned
in `requirements.txt`, and `requirements-dev.txt` has no Flask, Werkzeug or waitress line. The versions installed on the
legacy machines are UNKNOWN / NOT ESTABLISHED (A01 W-24 recorded the waitress pin).

P01-S086. INTERPRETATION, current external context (read 17-Nov-2026): summary of the documented behaviour used in this part. Each row
is an INTERPRETATION of what it implies for the legacy code, with the statement that applies it.

| Point | Source and version the page documents | Implication for the receiver | Used in |
|---|---|---|---|
| Worker pool of `threads` threads; I/O in the serving thread; busy pool queues tasks | waitress Arguments and Design (3.0.2, the pin) | eight concurrent receiver executions at most; more requests wait | P01-S067, P01-S068 |
| `connection_limit` 100; `channel_timeout` 120 s; `backlog` 1024 | waitress Arguments (3.0.2) | the connection limit passed equals the default | P01-S067 |
| `max_request_body_size` 1 GiB, `max_request_header_size` 256 KiB (defaults) | waitress Arguments (3.0.2) | the server-level body limit is far above the app's 1 MiB | P01-S067, P01-S087 |
| `expose_tracebacks` False (default) | waitress Arguments (3.0.2) | waitress does not send tracebacks to clients | P01-S067 |
| `trusted_proxy` None; proxy headers used only for a trusted proxy | waitress Arguments, Reverse Proxy (3.0.2) | `remote_addr` is not taken from forwarding headers | P01-S075 |
| No programmatic stop documented for `serve` | waitress Usage, API (3.0.2) | the server runs until the process ends | P01-S069 |
| `MAX_CONTENT_LENGTH` exceeded raises 413 `RequestEntityTooLarge` | Flask Configuration (3.1.x; pin 3.1.3); Werkzeug WSGI Helpers (3.1.x; unpinned) | an over-1 MiB declared body fails at L480, before the audit `try` | P01-S030 |
| No Content-Length: limited only if the server sets `wsgi.input_terminated`, else empty stream | Werkzeug WSGI Helpers, Flask Configuration (3.1.x) | outcome depends on waitress, not established | P01-S030 |
| 405 for an unallowed method; generic pages for unhandled HTTP exceptions | Flask Handling Application Errors (3.1.x) | wrong-method and unknown-path requests bypass the receiver's code and audit | P01-S027 |
| HEAD added automatically when GET is present; OPTIONS implemented automatically (added in the check) | Flask Quickstart, HTTP Methods (3.1.x) | HEAD `/health` runs the health view; OPTIONS on either route bypasses the receiver's code and audit | P01-S118 |
| Default `string` converter accepts any text without a slash (added in the check) | Flask Quickstart, Variable Rules (3.1.x) | a further slash in the path does not reach the receiver | P01-S028 |
| A 500 handler receives uncaught exceptions unless debug or testing propagates them; it is passed an `InternalServerError` (since Flask 1.1.0) | Flask Handling Application Errors, Configuration (3.1.x) | `internal_error` answers escapes from views; its log line carries the generic 500 text | P01-S060 |
| Daemon threads stopped abruptly at exit; `excepthook` prints to stderr; `Event.wait` return value | Python `threading` (3.13 or later) | server and sweeper end with the process; a crash in either is visible only on stderr | P01-S069, P01-S070, P01-S076 |

P01-S087. INTERPRETATION (P01-S086 rows 3 and 7): the receiver therefore sits behind two body limits, Flask's 1 MiB in
the app (P01-S021) and waitress's default 1 GiB in the server; for a request that declares its length, the app limit is
the one reached first.

P01-S088. UNKNOWN / NOT ESTABLISHED (sources not reached): the exact response waitress 3.0.2 sends when a body exceeds
its own limit or when the application itself fails to answer, whether it sets `wsgi.input_terminated`, and how it
reports a bind failure; these would need the waitress source at tag v3.0.2, which could not be fetched (section 1.4).

## 8. Who else uses the receiver or its app; the A19 scripts

P01-S089. FACT (`the search wrapper` for `WebhookReceiver`, `webhook_receiver`, `release_in_flight`, `update_heartbeat`,
`set_eod_capture`, `_eod_capture`; non-test code): only `main.py` imports `WebhookReceiver` (L92) and uses the object:
construction (L3407), the bound method passed to the processor (L3612), `set_eod_capture` (L3747), the app given to
waitress (L3990), the object given to `_shutdown` (L4262) and `stop()` (L1686). The processor calls the injected
release callback (`signals/signal_processor.py` L456 to L458, L1267 to L1271, L1699 to L1703, L1733 to L1737; P04) and
names `receiver.release_in_flight` in its docstring example (L148).

P01-S090. FACT (the searches of section 1.3): the other non-test mentions are names or text only:
`signals/signal_processor.py` L43 (module docstring: the processor "Does not manage the HTTP server or receive signals"); `config/expected_managers.yaml` L149
to L154 (class path; `ctor: "main.py:2892"`; effect point "webhook_audit day-count (WR13 finally,
webhook_receiver.py:498-503)"); `core/effect_telemetry.py` L259 (the census name); `core/evidence_artefact_manifest.txt`
L93; `core/exceptions.py` L354 (a docstring naming the receiver as a raiser of `SignalError`); `core/schema.sql` L52 and
L576 (comments); `core/config_validator.py` L14 (docstring); `ops_dashboard/backend/services/system_logs.py` L77 (a
logger-name group); `ops_dashboard/backend/readers/db_reader.py` L1417 (renders `webhook_audit` rows as
"POST /webhook/..."; A15); `reports/daily_trade_review.py` L711 (comment). HISTORICAL against FACT: at the baseline the
constructor call is at `main.py` L3407, not L2892 (the same stale reference, "ctor main:~2892", is in the `main.py`
comment at L4238), and `webhook_receiver.py` L498 to L503 are the per-IP-limit audit
write and warning, while the WR13 `finally` write is at L529 to L534 (stale line references; P10 records documents).

P01-S091. FACT (`the search wrapper '/webhook/|:5000|localhost:5000|<LOOPBACK>:5000|bind_port'`): the HTTP clients of the receiver
in the non-test repository are the boot self-check (`main.py` L4004 to L4005, loopback `/health`), the pre-flight check
`scripts/preflight/checks/signals.py` (L7, L17: a loopback `/health` URL on port 5000; A20, interface only) and the A19
load-test script (P01-S093). `utils/startup_checks.py` L793 only mentions the URL in a docstring.

P01-S092. HISTORICAL (`scripts/test_webhook.py` L1 to L13; A19; commit `56e79a9`, 04-May-2026): the script is not a
client of the receiver. It is a separate stand-in Flask app that answers GET and POST `/health` on all interfaces, port
5000, with `{"status": "ok", "port": 5000, "test_mode": True}`; its docstring says it "bypasses holiday guard for
connectivity testing". It records an expectation that something answers `/health` on port 5000; unlike the receiver's
`/health` it has no limiter and no authentication. Evidence of stated expectation only.

P01-S093. HISTORICAL (`scripts/load_test_signals.py`; A19; FIX-151, commit `37e6698`, 03-Jun-2026): the script posts
JSON to `<target>/webhook/<scanner>` (default target `http://localhost:5000`), adding `?token=<value>` when a token
argument is given (L95 to L106). Each payload has one symbol in `stocks`, `trigger_prices` as a string, `triggered_at`
as the current IST time in `%Y-%m-%d %H:%M:%S`, `scan_name` equal to the path name, and an extra `scan_url` field (L85
to L92). It records `X-Queue-Depth` and `X-Queue-Warning` (L118 to L119). Scenarios: burst 100 signals in 10 s,
sustained 250 over 5 min, overflow 200 in 5 s with 40 workers (L146 to L153). Assertions: burst at least 50 of 100
answered 200 and a p95 latency of at most 5,000 ms; sustained at least 80 % answered 200; overflow at least one 503
(L235 to L256). The docstring says it "Starts a mock webhook server internally (or targets a running instance)" (L6 to
L7); FACT: the file contains no server code (its imports, L32 to L49, are standard-library HTTP-client and thread-pool
modules and two project helpers, `core.logger` and `core.time_authority`; no server library).

P01-S094. INTERPRETATION (P01-S093 against L86 to L100, L495 to L504, P01-S020; `d922007`, 02-Jul-2026, "per-IP
rate limit"): the script predates the per-IP limiter. With the repository values (burst 60, refill 5 per second), from
one source address the overflow scenario (200 requests in 5 s) can pass the limiter only about 85 times (60 plus about
25 refilled); the remaining 115 or so would be answered 429 before the backpressure check that produces 503 (P03), so
its expected 503 would need the queue already at its threshold. The burst scenario (100 in 10 s) stays within 60 plus
about 50 and is not limited. Its stated expectations describe the receiver as it was before 02-Jul-2026. Its payloads
pass WR4, because `scan_name` equals the path.

## 9. A01's recorded lifecycle facts and the inherited items, receiver side

A01's IDs, classifications and owners are unchanged; this section records only what A06 verified at the lines. P09
quotes each inherited item in full.

P01-S095. FACT, verifying A01 C13 (A01 RECONCILED TOPIC RECORD section 3 and 4.2: "the MIS threads and the webhook
sweeper (L3355 to L3407) even before the last fail-fast guards (L3436 to L3465)"): the sweeper thread is started at
L220, inside the constructor that `main.py` L3407 calls (P01-S017), so it runs before the guards at L3436 to L3465, the
startup reconcile (L3880 to L3899) and the server start (L4000). INTERPRETATION: until L4000 its dict is empty, because
no request can claim a symbol before the server serves the app (P01-S072); its early start therefore has no effect on
signals. A01 C13 names A06 for "the sweeper".

P01-S096. FACT, verifying A01's lifecycle statement (section 3: "It then starts the webhook server, the health server
and three helper threads"): the server thread starts at L4000 after the processor and the other workers (L3974 to
L3977) and before the health server (L4074) (P01-S072).

P01-S097. FACT, verifying A01's statement (section 4.2: "the webhook and health servers ... are never stopped"): the
receiver's `stop()` only sets two events (P01-S080) and nothing holds or stops the waitress server (P01-S069).

P01-S098. FACT, A01 C15 receiver side: the server start (`main.py` L3987 to L4000) is outside any `try` (P01-S072).

P01-S099. FACT, A01 C20 receiver side ("the shutdown order is a documentation mismatch"; A01 AUDIT section 8 hands "the
processor and gate behaviour at stop" to A06 and A07): the receiver is stopped before the processor (`main.py` L1684 to L1692), while at start the
processor starts before the server (L3974, L4000); the receiver's `stop()` does not stop the server that started last
(P01-S080, P01-S081).

P01-S100. FACT, A01 C28 receiver side (A06 for "the webhook server's lifecycle"): the self-check probes `/health`, which
answers 401 to an unauthenticated probe when a secret is configured, and the check counts 401 as reachable (P01-S059);
there is no liveness check of the server after boot (A01).

P01-S101. INTERPRETATION, A01 B-32 receiver side (A06 for "the webhook server's bind-failure handling (C28)"): a bind
failure would surface only as a traceback on stderr from the "webhook-server" thread and, two seconds later, as the
self-check's DEGRADED sentinel, unless another listener on the port answers 2xx or 401 (P01-S070, P01-S071). The
waitress bind behaviour itself is UNKNOWN (P01-S088).

P01-S102. INTERPRETATION, current external context, A01 W-24 receiver side (A01: UNKNOWN / NOT ESTABLISHED, "the evidence lies outside
the admitted repository"): the waitress 3.0.2 documentation now read states a fixed pool of `threads` worker threads
(eight here) and I/O in the serving thread (P01-S068). The daemon flag of waitress's own worker threads and their
behaviour at process exit are not stated in the pages read, so A01's UNKNOWN stands for that part.

P01-S103. INTERPRETATION, A01 C18 receiver side (A06 for the processor's join and executor wait): the receiver's
`stop()` waits for nothing, so it adds no time to the shutdown (P01-S080); the processor's waits are P04's.

P01-S104. FACT, A01 C37 receiver side (A01 AUDIT section 8 hands "the PB-01 capture worker's ownership" to A18 and
A06): P01-S024 (the receiver keeps
the worker set at L3747 if L3748 or L3749 then fails).

P01-S105. FACT, A01 M-37 and M-43 receiver side: P01-S049 to P01-S051 (WR4b's dependence on AR12 and its handling of
the fallback).

P01-S106. FACT, A01 IS-9.14 receiver side: P01-S026 (no kill routes on the receiver at the baseline).

P01-S107. FACT, A01 M-20 receiver side (`core/exceptions.py` L139, L350 to L373, as A01 recorded; `grep "raise"`): the
receiver imports no project exception class (L37 to L57) and its only `raise` is the `ValueError` at L178; the docstring
at `core/exceptions.py` L354 naming the receiver as a raiser of `SignalError` does not match the code (HISTORICAL against
FACT).

P01-S108. INTERPRETATION (A01 AUDIT section 8 handoff table): the other A01 items handed to A06 (C14, C32, S-44, B-36,
B-28, B-07, M-13, M-19) are not receiver-lifecycle items: B-36 is touched only by the window call (P01-S036); the
scanner checks (B-07, S-44, C32) are P07's; the processor items (M-13) are P04's and P05's; B-28 concerns the
non-daemon flatten worker and gate-release tasks at exit; M-19 concerns custom exception classes outside
`core/exceptions.py`, and the receiver defines none (P01-S107). M-43's lazy-import part concerns
`core/instrument_cache.py` (A05); its A06 part, the WR4b coupling, is P01-S105. P09 records all of them.

## 10. Points the AUDIT may examine (neutral)

These are pointers only; no issue is counted or judged here.
- The in-flight heartbeat is not connected in `main.py`, so the sweeper evicts any claim older than 60 s and reports it
  as STALLED, against the FIX-011 comments and the commit message that say the callback was wired (P01-S076 to
  P01-S079).
- WR13 ("webhook_audit row per POST regardless of outcome") against requests that write no audit row: an over-limit
  body failing at L480, wrong-method and unknown-path requests, automatic OPTIONS answers, and every `/health` call
  (P01-S027, P01-S030, P01-S058, P01-S118); and the audit counts of a 503 batch (0 and 0) and of an EOD alert
  (P01-S044, P01-S055).
- The 500 handler's CRITICAL line carries Flask's generic `InternalServerError` text, not the original exception
  (P01-S060).
- The body is parsed as JSON whatever Content-Type is declared (P01-S119; P02).
- Shutdown: the server is never stopped; requests in progress are not awaited although comments say they drain; `/health`
  keeps answering 200; a request in progress can still write and enqueue while the processor stops and the store closes
  (P01-S080 to P01-S084).
- The order of checks: the body is parsed after the kill-switch, backpressure and window checks; EOD alerts bypass the
  kill switch, the window and backpressure (P01-S036, P01-S037, P01-S052).
- The scan-name check: spaces-only normalisation, a non-string value answered 500, WR4b's reliance on AR12 and its cached
  fallback, and WR4b's commit after the last recorded deployment (P01-S047 to P01-S051).
- An alias miss keeps the received case, which then flows into the claim, dedup key, row and queue item (P01-S039; with
  P04).
- The `signals.strategy` column receives the scanner name (P01-S043).
- Empty elements are kept on the intraday path and dropped on the EOD path (P01-S045).
- A fixed pool of eight waitress threads against WR11's "own thread"; `threads` and `connection_limit` are code
  literals (P01-S064, P01-S068).
- The all-interfaces bind comment that relies on `require_hmac: true`, beside `require_hmac: false` (P01-S066; P02,
  A02-13).
- Schema comments that state defaults the schema does not implement (P01-S065).
- Stale texts: the class docstring's `app.run`, WR5's code list without 429, the stale line references in
  `config/expected_managers.yaml`, and the `SignalError` docstring (P01-S006, P01-S007, P01-S090, P01-S107).
- The EOD worker kept by the receiver after a partial wiring failure (P01-S024; A01 C37).
- Numeric fields cast and then never used (P01-S038).
- The boot self-check counts 401 as reachable (P01-S059; A01 C28).
- The A19 load-test expectations predate the per-IP limiter; its docstring describes a mock server the file lacks
  (P01-S093, P01-S094).
- The source address used by the limiter and the audit when a tunnel or proxy is in front (P01-S075; P03).
- The alias file is read from a path relative to the working directory, once per process (P01-S018).
- The sweeper has no exception handling and is never restarted (P01-S076).
- Observed in passing for P04 and P05 (A04 handoff, direction question 24): the processor construction at `main.py`
  L3575 to L3623 passes no `rate_limiter` argument, whose default is `None` (`signals/signal_processor.py` L189). FACT
  at those lines; the A04 `try_acquire` question is not studied in P01.

## 11. UNKNOWN / NOT ESTABLISHED

P01-S109. UNKNOWN / NOT ESTABLISHED: every runtime fact about the receiver: whether any request reached it, which
routes and statuses occurred, whether the server bound its port at each boot, whether the self-check ever reported
DEGRADED, whether the sweeper ever evicted a claim, how long claims were held, and whether any request was in progress
at a shutdown (no production log, database or journal is admitted).

P01-S110. UNKNOWN / NOT ESTABLISHED: the effective values of `webhook.bind_host`, `bind_port`, `require_hmac`,
`dedup_window_seconds` and the per-IP settings, `signal_queue.*`, `excluded_symbols` and `watchlist.enabled` (only the
repository file values are known; overlays are not read).

P01-S111. UNKNOWN / NOT ESTABLISHED: the installed versions of Python, Flask, Werkzeug (unpinned), waitress and
cachetools on the legacy machines.

P01-S112. UNKNOWN / NOT ESTABLISHED (waitress source at tag v3.0.2 not reachable): waitress's own answer to a body over
`max_request_body_size`, whether it sets `wsgi.input_terminated`, how it reports a bind failure, the daemon flag and exit
behaviour of its worker threads, and what `REMOTE_ADDR` holds without a trusted proxy.

P01-S113. UNKNOWN / NOT ESTABLISHED: the installed pydantic version on the legacy machines. Under the pinned
`pydantic==2.13.0` (`requirements.txt` L7) the configuration object raises `AttributeError` for the undeclared `webhook`
attribute, as its published source shows (P01-S011, as corrected at assembly; P08-S006, P08-S071). The automatic HEAD and OPTIONS question was settled in the check from the Flask
3.1.x documentation (P01-S118); the patch release 3.1.3 itself was not separately checked.

P01-S114. UNKNOWN / NOT ESTABLISHED: the working directory of the production process (the alias file path, P01-S018);
the network path between Chartink and port 5000 (tunnel, proxy, firewall, security group) and whether the install
script ran (P01-S074, P01-S075).

P01-S115. UNKNOWN / NOT ESTABLISHED: whether production ran `3b15bbf` (WR4b; later than the last recorded deployment
`7d4970a`), and whether production alert names carried any prefix (P01-S050).

P01-S116. UNKNOWN / NOT ESTABLISHED: the store's behaviour after `close()` for a late audit write (A03's; P01-S083).

## 12. Draft questions about intent for Rama

Neutral questions about what was intended; no answer is proposed.
- Q-P01-01. Was the FIX-011 heartbeat meant to be connected in `main.py`, so that a signal still being processed keeps
  its in-flight claim beyond 60 s? (P01-S077 to P01-S079)
- Q-P01-02. Was every request reaching the webhook port meant to leave a `webhook_audit` row, including oversized,
  wrong-method and unknown-path requests and `/health` calls? (P01-S027, P01-S030, P01-S058)
- Q-P01-03. At shutdown, was the webhook server meant to stop accepting connections, and were requests already in
  progress meant to finish before the processor and the store stopped? (P01-S080 to P01-S084)
- Q-P01-04. Was `/health` meant to keep answering 200 after the receiver's `stop()`? (P01-S058)
- Q-P01-05. Was an EOD alert meant to be accepted while the kill switch is active, outside the entry window and with the
  queue above its threshold? (P01-S036, P01-S052)
- Q-P01-06. Which `scan_name` forms was the body check meant to accept (spaces only, or other separators and
  surrounding spaces; non-text values)? (P01-S047, P01-S048)
- Q-P01-07. Was the `signals.strategy` column meant to hold the scanner name or the strategy that the scanner map
  assigns? (P01-S043)
- Q-P01-08. Were the eight server threads and the connection limit of 100 meant to be fixed in code rather than set in
  configuration? (P01-S064)
- Q-P01-09. Does Rama recall how Chartink's requests reached port 5000 in production (directly, through a tunnel or
  through a reverse proxy)? (P01-S074, P01-S075)

## 13. Where the direction's questions are answered

| Direction question | Where in P01 | Main owner part |
|---|---|---|
| 1 Sources, routes, methods, payload formats (receiver side) | P01-S025 to P01-S028, P01-S034, P01-S035, P01-S038, P01-S047, P01-S052, P01-S118, P01-S119 | P01; P07 for configuration and Chartink |
| 2 Receipt, parse, conversion to an internal signal; every branch | P01-S029 to P01-S046, P01-S052 to P01-S057, P01-S119 | P01 |
| 3 Bind address, port, route, server and thread model, lifecycle, exposure | P01-S008 to P01-S024, P01-S061 to P01-S075, P01-S076, P01-S080 to P01-S084, P01-S117 (changes after the last recorded deployment) | P01 |
| 4 Scanner configuration, names, strategy and symbol mapping against the payload (receiver side) | P01-S035, P01-S039, P01-S043, P01-S047 to P01-S051 | P07 |
| 5 Scanner reachability checks | P01-S091 (interface only) | P07 |
| 6 Authentication | P01-S011 to P01-S013, P01-S034 step 1, P01-S058 (pointers) | P02 |
| 7 A02-13 | P01-S066 (pointer) | P02 |
| 8 Payload validation | P01-S030, P01-S034, P01-S038, P01-S040, P01-S045, P01-S048 (flow only) | P02 |
| 9 Responses and side effects | P01-S027, P01-S030 to P01-S034, P01-S044, P01-S053, P01-S055, P01-S058, P01-S060 (flow only) | P02 |
| 10 Deduplication | P01-S041 (pointer) | P03 |
| 11 Throttling | P01-S020, P01-S032 (pointers) | P03, P06 |
| 12 Limits, missing state, restart, exceptions | P01-S033, P01-S060, P01-S076, P01-S079 | P03 |
| 13 Queue threshold and capacity against A02 | P01-S008, P01-S034 step 5 (pointers) | P03 |
| 14 Concurrency, duplicate, lost or reordered signals | P01-S068, P01-S079, P01-S084 | P03, P04 |
| 15 to 19 Processor intake, queue, expiry, normalisation, field survival | P01-S039, P01-S042, P01-S043, P01-S046 (receiver side of the handoff) | P04 |
| 20 Event creation and persistence | P01-S041, P01-S043 (pointers) | P05, P11 |
| 21 Wiring, injection, callbacks, start and stop order (receiver side) | P01-S008 to P01-S024, P01-S061, P01-S064, P01-S072, P01-S073, P01-S077, P01-S081 to P01-S083 | P01; P04 for the processor |
| 22 A06 lifecycle against A01's | P01-S095 to P01-S108 | P01 |
| 23 Storage boundaries | P01-S031 to P01-S033, P01-S056, P01-S083 (write points only) | P03, P11 |
| 24 A04 rate-limiter boundary | section 10, last point (observed in passing only) | P04, P05 |
| 25 Handoffs to A07 | P01-S042 (the queue contract only) | P05 |
| 26 to 28 Whole-topic audit, matches, unknowns | sections 10 and 11 | AUDIT |

## 14. Check log

Check by a separate read-only helper, 17-Nov-2026 (IST). The pre-check text is kept at
the work area (not committed, D-17).

### 14.1 What was checked
- All 116 original statements (P01-S001 to P01-S116), the tables in sections 2, 4.3 and 7, and sections 10 to 13.
- Legacy sources re-read at `970aabf` with `git show` (output filtered for identifier-shaped text and machine paths):
  `signals/webhook_receiver.py` L1 to L1207 (structure re-taken with `ast.parse` of the source text: every class and
  method line range in P01-S004 and P01-S005 matches); `main.py` L88 to L95, L1595 to L1834, L2193, L3395 to L3420,
  L3474 to L3480, L3570 to L3630, L3700 to L3770, L3965 to L4078, L4200 to L4275; `signals/signal_processor.py` L144 to
  L150, L170 to L221, L456 to L458, L658 to L675 and the `_heartbeat`/release call lines; `core/config_loader.py`
  L612 to L652, L1985 to L2005, L2415 to L2462; `config/system_config.yaml` L118 to L136, L320 to L346, L616 to L623;
  `config/scan_webhook_map.yaml` (key and `strategy`/`scanner_type` lines only; no URL line read); `requirements.txt`;
  `requirements-dev.txt` (grep only); `scripts/test_webhook.py`; `scripts/load_test_signals.py` L1 to L332;
  `deploy/install_vm_services.sh` L30 to L50; `utils/startup_checks.py` L785 to L812; `core/schema.sql` L570 to L602;
  the name-only lines of P01-S090.
- Searches re-run with the mandatory exclusions (`the search wrapper` or explicit pathspecs): the receiver-name search of P01-S089;
  `update_heartbeat|in_flight_heartbeat` (whole repository, tests included); `excepthook`; `kill-switch"|hard-kill"|route\(`;
  `/webhook/|:5000|localhost:5000|<LOOPBACK>:5000|bind_port`; in the receiver: Flask configuration and hook names,
  `raise`, `body\[|body\.get\(`, `request\.` and Content-Type names, `provide_automatic_options|methods=`.
- History: `git log` of the receiver (31 commits; first `bcf03b5`, last `3b15bbf`); `git log -1` of `d922007`, `37e6698`,
  `56e79a9`, `a826dfe`, `3b15bbf`, `7d4970a`, `2d1e580`; `git show --stat a826dfe` (subject, body and file list; an
  identifier-bearing author line was not reproduced); `git log -S` for `in_flight_heartbeat` and `update_heartbeat` in
  `main.py` (no hit); `git log` and `git diff` from `7d4970a` to `970aabf` for the receiver, `main.py`, the configuration
  files and the A19 scripts (P01-S117).
- Project records (algocore_system, main): A01 RECONCILED TOPIC RECORD sections 3, 4.2 and 15; A01 AUDIT entries C13,
  C15, C20, C28, C37, B-32, B-36, M-20, M-37, W-24, summary rows of C14, C32, B-28, B-07, S-44, M-13, M-19, M-43 and the
  section 8 handoff table; A01 intent-source entry IS-9.14; Decision Register D-21.
- External pages: every page in section 1.4 except the waitress documentation index was re-opened on 17-Nov-2026 and
  each quoted sentence confirmed; Flask "Quickstart" was added. The waitress "Arguments" page also carries a stale
  warning that the `clear_untrusted_proxy_headers` default is False; the documented default and the 3.0.0 change note
  say True, as P01-S067 records.

### 14.2 Changes
Result: 116 statements checked; 97 correct as written; 19 corrected (P01-S003, S007, S011, S027, S028, S030, S036,
S038, S050, S060, S083, S086, S090, S093, S094, S099, S104, S108, S113); none withdrawn; 3 added (P01-S117 to
P01-S119). No label had to change: no runtime claim was found labelled FACT. Section-level edits are listed after the
statements.

| ID | What changed | Why |
|---|---|---|
| P01-S003 | "three project helpers" became four names from three project modules; the call-time import at L825 added | imprecise count; the lazy import was missing from the import list |
| P01-S007 | line reference L16 to L17 became L16 | WR5 is at L16; L17 is WR6 |
| P01-S011 | added the HISTORICAL comment L168 to L170 and the pydantic pin (`requirements.txt` L7); recorded the failed source lookup | completeness; the sourcing and labelling rules (the external point stays UNKNOWN) |
| P01-S027 | the "not looked up" sentence on HEAD and OPTIONS replaced by a pointer to P01-S118 | settled in the check from the Flask documentation |
| P01-S028 | added the default `string` converter rule (no slash) with its Flask source | completeness of the route behaviour; external fact now cited |
| P01-S030 | added the Werkzeug note that clients may see a connection reset instead of 413 | the page was listed in section 1.4 but used by no statement |
| P01-S036 | B-36 restated as A01 recorded it (the class leaves the IST contract to callers; every caller meets it; MATCH) | the original wording narrowed A01's record |
| P01-S038 | "the only reads of the body" limited to the intraday path; key-name logging at L604 and L613 and the EOD reads L767, L771 noted | precision |
| P01-S050 | the last recorded deployment given as `686df1c` and `7d4970a` with D-21; pointer to P01-S117 | D-21 names both commits |
| P01-S060 | added Flask's rule that a 500 handler receives an `InternalServerError`, and its consequence for the CRITICAL log line | external behaviour that changes what the log records; looked up and cited |
| P01-S083 | the failing late audit write made conditional on the store raising after `close()` | the store's behaviour after close is A03's and UNKNOWN; the original asserted the failure |
| P01-S086 | table rows added for automatic HEAD/OPTIONS, the default converter and the `InternalServerError` rule | consistency with P01-S028, P01-S060, P01-S118 |
| P01-S090 | citation "same search" became the searches of section 1.3; added `signals/signal_processor.py` L43 and the stale "ctor main:~2892" comment at `main.py` L4238 | the listed hits come from the wider section 1.3 patterns; two name-only mentions were missing |
| P01-S093 | added the burst p95 latency assertion (L242 to L243); "client-side only" imports restated (standard-library client modules and two project helpers) | omission; imprecise description |
| P01-S094 | quantified: about 85 of 200 overflow requests pass the limiter, about 115 get 429; the burst scenario is not limited | "most of the excess" was imprecise; the arithmetic follows L86 to L100 and the file values |
| P01-S099 | A01's handoff quoted as to A06 and A07 | A01 section 8 names both topics |
| P01-S104 | A01's handoff quoted as to A18 and A06 | A01 section 8 names both topics |
| P01-S108 | "M-43's lazy-import part" removed from the A06 list (it concerns `core/instrument_cache.py`, A05); B-28 and M-19 explained | boundary: the lazy import is not an A06 item |
| P01-S113 | the HEAD/OPTIONS part removed (settled by P01-S118); pydantic pin added | settled in the check |
| Header | Status line changed as the check brief requires | check brief, step 4 |
| Section 1.4 | Flask Quickstart added; the failed pydantic lookup recorded; re-opening of all pages noted | sources used by the check |
| Section 10 | WR13 point extended with OPTIONS; two neutral points added (500 log text; Content-Type not read) | follow the new statements |
| Section 13 | rows 1, 2 and 3 extended with P01-S117 to P01-S119 | question coverage |


### 14.3 Statements added
- P01-S117 (section 2): changes after the last recorded deployment, receiver side (only `3b15bbf`; no receiver line in
  the later `main.py` and configuration commits).
- P01-S118 (section 4.1): automatic HEAD and OPTIONS on the two routes and what they bypass.
- P01-S119 (section 4.2): the four request attributes the receiver reads; no Content-Type check.

### 14.4 Could not verify
- Whether a pydantic 2.13.0 model raises `AttributeError` for an undeclared attribute (P01-S011, P01-S113): the
  published source could not be retrieved; it stays UNKNOWN / NOT ESTABLISHED.
- The waitress 3.0.2 source points of P01-S088 and P01-S112 (its own body-limit answer, `wsgi.input_terminated`, bind
  failure reporting, worker-thread daemon flag, `REMOTE_ADDR` without a trusted proxy): the documentation pages do not
  state them; still UNKNOWN.
- What `get_data()` returns for a form-encoded or multipart body (P01-S119): not settled by the Werkzeug page read.
- No rule conflict arose. No identifier, credential value, URL token or machine path was written; G-19 is not touched.

### 14.5 Corrected at assembly
- Corrected at assembly: P01-S011 the pydantic point changed from UNKNOWN to the settled reading (under pydantic 2.13.0 `getattr(config, "webhook", None)` returns `None`, so the receiver takes `config.system.webhook`), citing P08-S006 and P08-S071; why: P08's check read pydantic's published source at tag v2.13.0 (`BaseModel.__getattr__` ends by raising `AttributeError`), re-read at assembly on 17-Nov-2026, and the receiver L171 to L175 and `core/config_loader.py` L2420 to L2434 (`extra="forbid"`, no `webhook` field) were verified at `970aabf`. The installed version stays UNKNOWN. (17-Nov-2026 20:45 IST)
- Corrected at assembly: P01-S113 restated to keep only the installed-version unknown; why: follows the P01-S011 correction. The 14.4 bullet on pydantic is superseded by this correction. (17-Nov-2026 20:45 IST)

- Corrected at assembly by Claude (17-Nov-2026), after the independent check of the assembled STUDY: P01-S117: "44 added or removed lines" -> "42 added lines (none removed)" (`git diff --numstat 7d4970a 970aabf -- main.py` gives 42 / 0; 44 counted the diff header lines).
