# A06 evidence: configuration read by A06

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P08, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude.
**Purpose and scope:** Every configuration key, code setting and environment-variable NAME that A06 code reads (the webhook receiver, the signal processor up to the A07 handoff, the entry throttle, the Appendix A script `scripts/preflight_scanner_check.py`, and the A06 call sites in `main.py`): where each key is defined and its committed value, the schema field (A02's), the reader (file and line), the code default when the key is absent, and the keys that nothing reads; the later processor reads at the interface only (Rama's decision A of 17-Nov-2026); the cross-check against A02's handoffs to A06 (T-02, T-07, T-12, T-14, F-11, K-02, K-04, K-05, K-09, K-12, K-13, K-22, K-49, X-01) and the open issues A02-03 and A02-13; the `config/expected_managers.yaml` entries for `signal_processor` and `webhook_receiver` as declarations. Direction questions 13 (values) and 26 (configuration as an intent source, recorded only). A02 owns the configuration files, the schema and precedence; A06 records where its settings are read and applied. The checked parts P01 to P06 are cited by statement ID and not repeated. `970aabf` below means the baseline commit (STUDY part P08).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)
- In whole: `scripts/preflight_scanner_check.py` (L1 to L235); `config/scan_webhook_map.yaml` (L1 to L84; the
  `chartink_url` values masked on screen and not reproduced); `config/chartink_scanners.yaml` (L1 to L32; URLs masked,
  not reproduced); `requirements.txt` (L1 to L15).
- In part, `config/system_config.yaml`: L20 to L50 (`trading_hours`), L110 to L160 (`signal_queue`,
  `excluded_symbols`, `force_intraday_only`, `trade_type`, `delivery_enabled`), L320 to L380 (`webhook`,
  `signal_processor`), L505 to L542 (`sr_detector`), L563 to L576 (`portfolio_allocator`, `v3_chain`), L740 to L753
  (`scanner_check_delay_sec`). A02's file, read at the boundary.
- In part, `core/config_loader.py` (A02's): L1 to L60 (module docstring), L185 to L200 (`SignalQueueConfig`), L560 to
  L645 (`SignalProcessorConfig`, `WebhookConfig`), L1180 to L1183 and L1209 to L1212 (`SRDetectorConfig`, two fields),
  L1985 to L2048 (`SystemConfig`, first fields), L2340 to L2440 (`ScannerEntry`, `ScanWebhookMapConfig`,
  `ChartinkScannersConfig`, `AppConfig`).
- In part, `signals/webhook_receiver.py`: L1 to L70, L69 to L100 (`_PerIpRateLimiter`), L138 to L300 (class docstring,
  constructor, `_load_symbol_aliases`), L395 to L400 (`/health`), L494 to L585 (`_handle_webhook` tail,
  `_process_request` head), L676 to L722 (per-symbol loop head), L1189 to L1195 (sweeper); plus a search of the whole
  file for configuration, `getattr` and environment reads.
- In part, `signals/signal_processor.py`: L45 to L125 (imports, constants), L150 to L300 (constructor), L300 to L1006
  (search for literals and configuration reads; L930 to L1006 read in full), L1026 to L1031, L1096 to L1101, L1224 to
  L1225, L1414 to L1426, L1493, L1799 to L1848, L1874 to L1892, L1909 to L1953, L2075 to L2080, L2438 to L2441; plus a
  search of the whole file for strategy-attribute and setting reads.
- `signals/entry_throttle.py`: searched for configuration and environment reads (none); its keys are P06's.
- In part, `main.py`: L826 to L860 (`_build_strategy_governor`), L2316 to L2332 (`MarketWindows`), L3395 to L3420
  (queue and receiver), L3421 (`_sr_cfg`), L3570 to L3625 (processor), L3979 to L4006 (server and self-check), L4208 to
  L4213 (banner), L4225 to L4250 (effect-telemetry registration); search for `WEBHOOK_SECRET`, `load_dotenv`,
  `effect_telemetry`.
- In part, A01's and other topics' files at the interface only: `utils/startup_checks.py` L652 to L700, L748 to L782,
  L1585 to L1600 (A01); `core/market_windows.py` L143 to L151 and a search for `entry_start` and `special` (A01);
  `core/effect_telemetry.py` L1 to L70, L120 to L215 and a search (A15 per the index entry A15 Paths; the census is
  A01's, P03-S053); `capital/risk_engine.py`, a search for `_one_trade_per_symbol_direction` (A09);
  `deploy/systemd/trading-system.service`, a search for `Environment`, `WorkingDirectory`, `ExecStart` (A17); the 16
  strategy files under `config/strategies/`, a search for `sl_method`, `tgt_method`, `sl_gap_buffer_pct` (A02's files).
- `config/expected_managers.yaml`: L1 to L66, L140 to L160, L370 to L386 (text only; HISTORICAL declarations).
- HISTORICAL text only (data, never instructions): `core/config_validator.py` L1 to L30 (docstring);
  `docs/CONFIG_GUIDE.md` L336 to L375 (last commit `d2426d2`, 28-Jul-2026); `git log` of
  `config/expected_managers.yaml` and `git blame` of its L57 to L64 and L149 to L156.
- Not opened (security rules): `config/accounts.csv`, any `.env*` file, any `*.local.yaml`, any `*token*.json`; local
  overlays and effective settings.

### 1.2 Project records read (algocore_system, branch `main`, read-only)
- `A02_AUDIT_2026-11-08.md`: the records T-02 (L988 to L1000), T-07 (L1058 to L1072), T-12 (L1128 to L1140), T-14
  (L1156 to L1170), F-11 (L1521 to L1534), K-02 (L1834 to L1848), K-04 (L1862 to L1874), K-05 (L1876 to L1890), K-09
  (L1932 to L1945), K-11 (L1960 to L1972), K-12 (L1974 to L1986), K-13 (L1988 to L2000), K-22 (L2114 to L2126), X-01
  (L2411 to L2426); the rows K-49, K-50, K-51 (L2316 to L2318); the handoff tables (L1300 to L1316, L1769, L2350 to
  L2384); section 10 (L2427 to L2445); section 11 (L2446 to L2462).
- `A02_RECONCILED_TOPIC_RECORD_2026-11-09.md`: L198 to L204, L241 to L258, L284, L297, L335 to L355, L385, L394,
  L443, L452 (search hits for the 16 IDs).
- `A02_STUDY_2026-11-06.md` L247, L255, L373 to L378, L763; `evidence/A02_KEY_CONSUMER_MAP_PART1_2026-11-06.md` L73 to
  L86, L288 to L326; `evidence/A02_KEY_CONSUMER_MAP_PART2_2026-11-06.md` L459 to L463, L668;
  `evidence/A02_STRATEGY_CONFIGURATION_2026-11-06.md` L442 to L456.
- `OPEN_ISSUES_REGISTER_2026-11-05.md`: entries A02-03 (L481 to L495) and A02-13 (L601 to L615).
- `AUDIT_FINDINGS_REGISTER_2026-11-06.md`: the rows of the 14 A02 items (L255 to L331, by search).
- `TOPIC_COMPLETION_REGISTER_2026-11-04.md`: the A06 entry (L103 to L116).
- The checked parts P01 to P06 of this STUDY (cross-references only); the A06 investigation direction of 17-Nov-2026,
  sections 2, 4 and 5.

### 1.3 Commands and search patterns (all read-only)
- `git show 970aabf:<path>` for every file above, output filtered for identifier-shaped
  text, machine paths and (for the two scanner files) URLs.
- a search wrapper applying the mandatory exclusions (non-test, non-document code, with the four exclusions) for:
  `signal_queue|backpressure_pct|warning_pct|expiry_sec|excluded_symbols|dedup_window_seconds|per_ip_(rate_limit_enabled|burst|refill_per_sec)|require_hmac|bind_host|bind_port|scanner_check_delay_sec|drain_poll_sec|pipeline_timeout_sec|worker_count|tgt_min_pct|min_gap_between_entries_sec|entry_burst_(window_sec|max)|per_symbol_cooldown_sec`;
  `WEBHOOK_SECRET|webhook_secret`; `expected_managers`.
- `git show` piped to `grep -n -E` on the four A06 files for
  `_config\b|_config\.|config\.|cfg\b|cfg\.|getattr\(|os\.environ|getenv|environ\[|\.yaml|\.get\("` and module-level
  upper-case names; on `signals/signal_processor.py` for `strategy_obj\.[a-z_]+|strategy\.[a-z_]+` and the
  setting names; on `main.py` for `register_constructed|effect_telemetry|load_dotenv|dotenv|wh_cfg *=|_sr_cfg *=`.
- `git grep -n -E` with the four exclusions in `config/strategies/`, `config/system_config.yaml`,
  `capital/risk_engine.py`, `core/config_loader.py`, `config/preflight.yaml`, `config/cron_registry.yaml`,
  `config/security.yaml` for the strategy method keys, `atr_fallback_mode`, `_one_trade_per_symbol_direction` and
  `scanner|webhook|signal_queue|preflight_scanner`.
- `git log --format='%h %ad %s' --date=short 970aabf -- config/expected_managers.yaml`; `git log --diff-filter=A` of
  that file and of `core/effect_telemetry.py`; `git blame -s -L` of the registry's entries; `git blame -L 567,567` of
  `config/system_config.yaml` and `git log -1` of the commit found (`536172c`).
- Added in the check (read-only): `git show 297b587:main.py`, `git show 297b587:signals/signal_processor.py` and
  `git show 297b587:signals/webhook_receiver.py` at the lines the registry names (P08-S036, P08-S037); the helper
  `the search wrapper` for `dotenv`, `scan_webhook_map`, `scanner_type|chartink_url|chartink_scanners`, `scanner_check_delay_sec`,
  `WEBHOOK_SECRET` and `_one_trade_per_symbol_direction`; `git log -L127,127:config/system_config.yaml`;
  `git grep` of the strategy method keys in `config/strategies/` (values counted).
- Python `ast` was not needed; nothing was imported, executed or run.

### 1.4 External pages read
- Pydantic documentation, "Models" (https://pydantic.dev/docs/validation/latest/concepts/models/, reached by the
  redirect from docs.pydantic.dev; read 17-Nov-2026): "`name` wasn't set when `user` was initialized, so the default
  value was used."; "'forbid': Providing extra data is not permitted." The page does not state its version (re-opened
  in the check, 17-Nov-2026: it is the "Latest (stable)" build and carries "New in v2.14" notes, so it documents a later
  release than the pin); the repository pins `pydantic==2.13.0` (`requirements.txt` L7); the installed version on the
  legacy machines is UNKNOWN / NOT ESTABLISHED.
- Pydantic documentation, "Fields" (same site, read 17-Nov-2026): no sentence on omitted fields that adds to the
  "Models" page; not cited further.
- Pydantic documentation, "Validation Errors" (https://pydantic.dev/docs/validation/dev/errors/validation_errors/, the
  development version of the pages; read 17-Nov-2026): `missing`: "This error is raised when there are required fields
  missing from the input value"; `extra_forbidden`: "This error is raised when the input value contains extra fields,
  but `model_config['extra'] == 'forbid'`".
- Added in the check (read 17-Nov-2026): pydantic's published source at the tag of the pin,
  https://raw.githubusercontent.com/pydantic/pydantic/v2.13.0/pydantic/main.py, `BaseModel.__getattr__`: after the
  private-attribute branch, the `__pydantic_extra__` branch and the `hasattr(self.__class__, item)` branch it ends with
  `raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')`. Python documentation,
  "Built-in Functions", `getattr` (https://docs.python.org/3/library/functions.html): "If the named attribute does not
  exist, default is returned if provided, otherwise AttributeError is raised."; "Data model", `object.__getattr__`
  (https://docs.python.org/3/reference/datamodel.html): "Called when the default attribute access fails with an
  AttributeError". Used in P08-S006 and P08-S071.
- No Chartink, scanner, webhook or legacy endpoint was contacted.

## 2. Where A06's configuration comes from

P08-S001. FACT (`main.py` L3407 to L3415, L3574 to L3623; `signals/signal_processor.py` L155 to L198): `main.py` passes
the whole `AppConfig` to the receiver (`config=app_config`, L3410) and the secret as `secret_token=
os.environ.get("WEBHOOK_SECRET")` (L3414; P01-S009, P02-S009). The processor receives no configuration object: its
constructor has no `config` parameter, and `main.py` passes individual values taken from `app_config.system` (through
`sp_cfg = app_config.system.signal_processor`, L3574), `app_config.scan_webhook_map.scanners` (L3585) and other
objects built from configuration (P04-S001, P04-S002). The entry throttle receives four numbers from the processor's
constructor (L263 to L268; P06).

P08-S002. FACT (`core/config_loader.py` L2420 to L2434; L1987 to L2026; L2347 to L2388): the A06 keys loaded by
`load_all` sit in three of the eight files of `AppConfig`: `system_config.yaml` (model `SystemConfig`: the sections
`signal_queue`, `webhook`, `signal_processor`, the list `excluded_symbols` and the scalar `scanner_check_delay_sec`),
`scan_webhook_map.yaml` (`ScanWebhookMapConfig`, one mapping `scanners` of `ScannerEntry`) and `chartink_scanners.yaml`
(`ChartinkScannersConfig`, one mapping `scanners` of name to URL text). Every model named here declares
`model_config = ConfigDict(extra="forbid")` (L193, L565, L618, L1988, L2349, L2376, L2387, L2425). Current external
context (pydantic "Models" and "Validation Errors", read 17-Nov-2026): with `extra='forbid'` "Providing extra data is not
permitted"; the `missing` error "is raised when there are required fields missing from the input value".
INTERPRETATION: a misspelt A06 key in these files, or a deleted required one, makes validation fail rather than being
ignored; the load-failure path is A01's and A02's.

P08-S003. HISTORICAL against FACT (`core/config_loader.py` L35 to L40, docstring; L194 to L197, L572 to L586, L622 to
L628, L1993, L2026, L2357; A02 STUDY L763, item 4): the loader's docstring says it "Does not fill in defaults for
missing keys (CL3: extra="forbid", all required)" (L39). Fourteen A06 fields have code defaults: eleven in the
three sections (`warning_pct`; `dedup_window_seconds` and the three per-IP keys; `atr_fallback_mode`, `tgt_min_pct`
and the four entry-throttle keys) and three more (`excluded_symbols` and `scanner_check_delay_sec` of `SystemConfig`,
`scanner_type` of `ScannerEntry`). A02 recorded the general point (289 fields with defaults; A02 AUDIT L-04, L254 to
L260); the A06 fields are listed in section 3.

P08-S004. FACT (sources other than `AppConfig` read by A06 code or for A06 objects):
- (a) the process environment variable named `WEBHOOK_SECRET`, read once by `main.py` L3414 for the receiver (P02-S009;
  section 5.1);
- (b) `config/symbol_aliases.yaml`, read directly by the receiver's constructor from the relative path
  `Path("config/symbol_aliases.yaml")` (`signals/webhook_receiver.py` L227, L258 to L292; P01-S018, P04-S047);
- (c) the account file, read through A01's `core.account_registry.primary_account_tag` for the receiver's WR4b
  scan-name prefix strip (`signals/webhook_receiver.py` L57, L111 to L138; P01-S049, P01-S051); named only, not opened;
- (d) `config/expected_managers.yaml`, read by `core/effect_telemetry.py` (L63, L129 to L142) for the processor's
  `handle("signal_processor")` (`signals/signal_processor.py` L55, L217) and `main.py`'s registration of
  `"webhook_receiver"` (L4238 to L4240) (section 7);
- (e) the strategy files, loaded by `StrategyLoader` in `main.py` L3157 to L3162 and passed as `strategies` (P04-S007);
  the processor reads their fields (section 4.4);
- (f) the Appendix A script's own command-line options (`scripts/preflight_scanner_check.py` L34 to L57; section 4.3).

P08-S005. FACT (`deploy/systemd/trading-system.service` L10, L13, L18; A17's file, interface only; `main.py`, search
for `load_dotenv|dotenv`: no hit): the declared service unit sets the working directory to the project directory and
names an environment file (the project's `.env` file; type and location only, not opened) with `EnvironmentFile=`;
`main.py` itself does not load a `.env` file, and no module outside `scripts/` does (search for `dotenv`, added in the
check: the only loaders are scripts). HISTORICAL (`requirements.txt` L14): `python-dotenv` is pinned with the comment
"runtime .env loading (SU19)"; a comment is not proof. INTERPRETATION: under the declared unit, `WEBHOOK_SECRET` would reach the
process environment from that file, and the relative paths of (b) and (d) resolve against the project directory (A02
F-11 made the same reading). A unit file is a declaration, not proof of how any process was started (UNKNOWN / NOT
ESTABLISHED).

P08-S006. INTERPRETATION, with current external context (pydantic "Models", read 17-Nov-2026: "`name` wasn't set when
`user` was initialized, so the default value was used"): a field that has a default is present on the loaded model
whether or not its key is in the file. So under `main.py`'s wiring the `getattr(..., <default>)` fallbacks that A06 code
applies to declared fields of `SystemConfig`, `SignalQueueConfig`, `WebhookConfig` and `SignalProcessorConfig`
(sections 3.1 to 3.5) never supply the value: the schema default does when the key is absent. The fallbacks matter only
for objects that are not these models (for example test doubles, HISTORICAL comment `signals/webhook_receiver.py` L168
to L170). For the receiver's five `webhook` reads this holds provided its lookup reaches
`config.system.webhook` (P01-S011). Current external context (read 17-Nov-2026, in the check; section 1.4): in
pydantic's published source at tag v2.13.0 (the version `requirements.txt` L7 pins), `BaseModel.__getattr__` ends by
raising `AttributeError` for a name that is not a private attribute, not an extra field and not a class attribute;
Python's `getattr` returns its default when the attribute "does not exist", and `__getattr__` is "Called when the
default attribute access fails". INTERPRETATION: `AppConfig` declares no `webhook` field and forbids extras
(`core/config_loader.py` L2420 to L2434), so under pydantic 2.13.0 `getattr(config, "webhook", None)` (receiver L171)
returns `None` and the receiver takes `config.system.webhook` (L173 to L175); the installed pydantic version is UNKNOWN /
NOT ESTABLISHED. P01-S011 recorded this point as UNKNOWN because the source could not then be retrieved; it was aligned
at assembly (P01 check log, section 14.5; P08-S071). P06-S023 made the same reading for the four throttle keys.

## 3. `config/system_config.yaml` keys read by A06 code

All values below are the committed values of the repository file at `970aabf` (A02's file). The effective values on
the legacy machines (local overlays, any edited copy) are UNKNOWN / NOT ESTABLISHED for every key (A02). "Code default
at the reader" is the value the reading line would use if the attribute were missing; P08-S006 explains why, under
`main.py`'s wiring, such a fallback on a declared field never supplies the value. File comments are HISTORICAL.

### 3.1 `signal_queue` (L124 to L128; `SignalQueueConfig` L192 to L197; required section, L1991)

P08-S007. FACT (lines as cited; `core/config_loader.py` L192 to L197):

| Key | File line, value, comment (HISTORICAL) | Schema field | A06 reader(s) | Code default at the reader | Statements |
|---|---|---|---|---|---|
| `capacity` | L125, `300`, "Max signals in queue before HTTP 503 (P15)" | L194 `int`, required, no validator | `main.py` L3402 to L3404 (`queue.Queue(maxsize=...)`); receiver L537, L571 (base of the request threshold), L397 (`/health` display) | none (plain attribute read) | P01-S008, P03-S036, P03-S045 |
| `backpressure_pct` | L126, `0.80`, "503 threshold = capacity * backpressure_pct (P15)" | L195 `float`, required, no validator | receiver L573: `int(capacity * sq_cfg.backpressure_pct)` | none | P03-S037, P03-S047 |
| `expiry_sec` | L127, `600`, "WR6: 10 min - Chartink triggered_at is scan time, not delivery time" | L196 `int`, required, no validator; field comment "(default 60)" | receiver L679, then `_process_signal` L925 (`age_sec > expiry_sec` gives `EXPIRED`) and L960 (`expires_at = received_at + expiry_sec`); `main.py` L3614 to processor L175, L222, L917 | receiver: none; processor constructor `60` (L175), always overridden by `main.py` | P02-S058, P02-S075, P04-S005, P04-S036, P04-S037 |
| `warning_pct` | L128, `0.60`, "FIX-134 Item 35: X-Queue-Warning header above 60% fill" | L197 `float`, default `0.60`, no validator | receiver L574: `int(capacity * getattr(sq_cfg, "warning_pct", 0.60))` | `0.60` | P03-S042 |

P08-S008. INTERPRETATION (P08-S007; `main.py` L3403; receiver L537, L571; the same reasoning as P04-S036 for
`expiry_sec`): the queue's hard limit is fixed from `capacity` when `main.py` builds the queue, while the receiver reads
`capacity`, `backpressure_pct`, `warning_pct` and `expiry_sec` from its configuration object on every request. The two
use one value as long as the object is not replaced in a running process (whether that can happen is A02's). At the
file values: hard limit 300, request refusal at a depth of 240, warning header at 180, expiry 600 s (P03-S037,
P03-S042). The meanings of the same settings at their other consumers (dashboard, pre-flight) are P03-S045 to P03-S047
(direction question 13).

### 3.2 `excluded_symbols` (L130 to L136; `SystemConfig` L1993)

P08-S009. FACT (`config/system_config.yaml` L130 to L136; `core/config_loader.py` L1993; `signals/webhook_receiver.py`
L708 to L717): the file lists five symbols (comment L130, "FIX-C: Symbol exclusion list (rejected at webhook edge with
DEBUG log only)", HISTORICAL; L132's entry carries the comment "Exclude list from live observation"). The schema field
is `list[str] = []`. The receiver reads it per symbol as `getattr(self._config.system, "excluded_symbols", [])` (L709)
and compares `symbol.upper()` with the upper-cased entries after the alias step (L710); a match gives the per-symbol
status `REJECTED_EXCLUDED_SYMBOL` with no row and no queue item (P02-S060). The end-of-day route does not apply the list
(P02-S060). Outside A06, `reports/daily_report.py` reads the raw YAML (L140 to L161; A15; A02 K-04). A02 recorded that
the loader default `[]` differs from the file value, so deleting the key would empty the list without an error (key
consumer map part 1, L86 and L326).

### 3.3 `webhook` (L327 to L342; `WebhookConfig` L617 to L642; required section, L2002)

P08-S010. FACT (lines as cited; `core/config_loader.py` L617 to L642):

| Key | File line, value, comment (HISTORICAL) | Schema field | A06 reader(s) | Code default at the reader | Statements |
|---|---|---|---|---|---|
| `bind_host` | L328, an all-interfaces address (value not reproduced); comment L328 to L334 (premise "require_hmac=true plus firewall/security-group restrictions") | L619 `str`, required, no validator; field comment names a loopback default the schema does not implement | `main.py` L3979 (`wh_cfg = app_config.system.webhook`), L3992 (waitress `host`) | none | P01-S061, P01-S064, P01-S065, P01-S066 |
| `bind_port` | L335, `5000`, "port to listen on" | L620 `int`, required, no validator; field comment "default 5000" | `main.py` L3993 (waitress `port`), L4004 (boot self-check URL, loopback `/health`), L4210 (interactive banner) | none | P01-S059, P01-S073 |
| `require_hmac` | L336, `false`, "Chartink cannot sign payloads; use ?token= auth (WEBHOOK_SECRET required in BOTH modes as of C-2 02-Jul)" | L621 `bool`, required | receiver L171 to L176 (`bool(getattr(_webhook_cfg, "require_hmac", False))`), L177 to L182 (construction guard), L200 (kept), L343 (request time) | `False` | P01-S011 to P01-S013, P02-S014 to P02-S017 |
| `dedup_window_seconds` | L337, `300`, "FIX-131 Item 17: 5-min fingerprint bucket (was 60s/1-min)" | L622 `int`, default `300`, no bound | receiver L232 to L236 (`int(getattr(..., 300))`; `TypeError` or `ValueError` gives 300; then `max(60, ...)`), L237 (cache TTL), L952 (fingerprint slot) | `300`, floored at 60 | P01-S019, P03-S003 |
| `per_ip_rate_limit_enabled` | L340, `true` (comment L338 to L339) | L626 `bool`, default `True` | receiver L241 (`bool(getattr(..., True))`) | `True` | P03-S021 |
| `per_ip_burst` | L341, `60` | L627 `int`, default `60`, validator `>= 1` (L630 to L635) | receiver L243 (`int(getattr(..., 60) or 60)`); limiter L80 (`float(max(1, int(burst)))`) | `60` | P03-S020, P03-S021 |
| `per_ip_refill_per_sec` | L342, `5.0` | L628 `float`, default `5.0`, validator `>= 0` (L637 to L642) | receiver L244 (`float(getattr(..., 5.0) or 5.0)`); limiter L81 (`max(0.0, ...)`) | `5.0`; a configured `0.0` also becomes `5.0` | P03-S021 (A02 K-12) |

P08-S011. FACT (P08-S010; `signals/webhook_receiver.py` L171 to L247; `main.py` L3979 to L3995): all seven `webhook`
keys have a reader. The receiver reads its five once, in its constructor, so they are fixed for the receiver's life;
`main.py` reads the two server keys when it starts the server (L3979, L3992 to L3993) and reads `bind_port` again for
the boot self-check URL (L4004) and, in interactive mode only, for the banner (L4210). `WebhookConfig` has no secret field (L617 to
L628): the webhook secret is not a configuration key (P02-S009). HISTORICAL (`core/config_loader.py` L20 to L21, CL5):
"Values needing env vars go in .env, read by consumer modules." INTERPRETATION (validator L630 to L635): because the
schema rejects a burst below 1, the receiver's `or 60` for a zero burst cannot be reached from a loaded file; the
refill fallback can (A02 K-12; P03-S021).

### 3.4 `signal_processor` (L344 to L353; `SignalProcessorConfig` L564 to L614; required section, L2003)

P08-S012. FACT (lines as cited; `core/config_loader.py` L564 to L614; `main.py` L3574, L3590 to L3599):

| Key | File line, value, comment (HISTORICAL) | Schema field | Reader (`main.py` argument, then `signals/signal_processor.py`) | Code default (constructor) | Statements |
|---|---|---|---|---|---|
| `worker_count` | L345, `5`, "ThreadPoolExecutor workers (1-50)" | L566 `int`, required, 1 to 50 (L588 to L593) | `main.py` L3590; L173, L220 (`max(1, worker_count)`), L311 (`ThreadPoolExecutor(max_workers=...)`) | `5`, overridden | P04-S003, P04-S010 |
| `drain_poll_sec` | L346, `0.1`, "queue poll interval when empty" | L567 `float`, required, `> 0` (L595 to L600) | `main.py` L3591; L174, L221, L385 (`get(timeout=...)`) | `0.1`, overridden | P04-S013, P04-S014 |
| `pipeline_timeout_sec` | L347, `30`, "hard per-signal processing deadline" | L568 `int`, required, `>= 1` (L602 to L607) | none: not passed by `main.py`, no constructor parameter | none | P04-S004 (A02 K-13) |
| `tgt_min_pct` | L348, `0.003`, "BL-16: reject signal if target distance < 0.3% of entry" | L575 `float`, default `0.003`, `0 < v < 1` (L609 to L614) | `main.py` L3594; L178, L225, L1945 (inside `_derive_target`, after the handoff; A09 per P05-S036 row 15) | `0.003`, overridden | P04-S003 |
| `min_gap_between_entries_sec` | L350, `20` | L581 `float`, default `0.0`, no validator | `main.py` L3596 (`getattr(sp_cfg, ..., 0.0)`); L179, L264; `EntryThrottle` L49 | `0.0` | P06-S021 to P06-S024 |
| `entry_burst_window_sec` | L351, `60` | L582 `float`, default `60.0`, no validator | `main.py` L3597 (`getattr`, `60.0`); L180, L265; `EntryThrottle` L50 | `60.0` | P06-S021 to P06-S024 |
| `entry_burst_max` | L352, `3`, "(0 = off)" | L583 `int`, default `0`, no validator | `main.py` L3598 (`getattr`, `0`); L181, L266; `EntryThrottle` L51 | `0` | P06-S021 to P06-S024 |
| `per_symbol_cooldown_sec` | L353, `300` | L586 `float`, default `0.0`, no validator | `main.py` L3599 (`getattr`, `0.0`); L182, L267; `EntryThrottle` L52 | `0.0` | P06-S021 to P06-S024 |
| `atr_fallback_mode` (not in the file) | absent | L572 `Literal["WARN", "HALT"]`, default `"WARN"` | `main.py` L3593; L177, L224, L1803 and L1914 (inside `_derive_prices` and `_derive_target`, after the handoff; A09 per P05-S036 rows 1 and 15) | `"WARN"` | P04-S003, P05-S013 |

P08-S013. FACT (P08-S012; P04-S033; P05-S036): of the eight keys in this section of the file, two govern A06's
intake itself (`worker_count`, the worker pool; `drain_poll_sec`, the dispatcher's poll); the four throttle keys act at
the throttle's three admission call sites (P06; Rama's decision B); `tgt_min_pct` acts after the handoff;
`pipeline_timeout_sec` has no reader. The schema field `atr_fallback_mode`, absent from the file, also acts after the
handoff. This agrees with A02's row K-51 ("6 matching"; `pipeline_timeout_sec` ISSUE K-13, `entry_burst_window_sec`
ISSUE K-12; A02 AUDIT L2318).

### 3.5 `scanner_check_delay_sec` (L752 to L753; `SystemConfig` L2026)

P08-S014. FACT (`config/system_config.yaml` L752 to L753; `core/config_loader.py` L2026; `utils/startup_checks.py`
L652 to L678, L1587 to L1597, A01's file, interface only; `scripts/preflight_scanner_check.py` L208 to L214): the file
sets `5.0` (comment "FIX-D: Scanner connectivity check settings"; "Delay before scanner checks (network stabilization
at startup)", HISTORICAL); the schema field is `float = 5.0`. The only code that uses the value is A01's
`run_all_startup_checks` (the dashboard's configuration view names the key only to place it in a display category,
`ops_dashboard/backend/services/config_view.py` L35 and L259; A15), which reads `getattr(app_config.system, "scanner_check_delay_sec", 0.0)` (L1591) and passes it as `delay_sec` to
`check_scanner_connectivity` (L1592 to L1595), which sleeps for it when it is above 0 (L676 to L678); the whole step is
skipped on a COLD start (L1589). No A06 file reads the key. The Appendix A script calls the same function without
`delay_sec` (L208 to L214), so the function's own default `0.0` (L658) applies there and the key has no effect on the
script. INTERPRETATION (P08-S006): the `getattr` default `0.0` never applies under `main.py`; A02 recorded the
disagreement between 5.0 and 0.0 (key consumer map part 2, L463 and L668; STUDY L378).

### 3.6 Other `system_config.yaml` keys that reach A06 objects (interface only)

P08-S015. FACT (lines as cited; owners from the Master System Investigation Index as the earlier parts recorded them):

| Key or section (file line, value) | Path into A06 code | Where A06 code uses it | Owner of the logic | Statements |
|---|---|---|---|---|
| `trading_hours.entry_start` (L28, `"10:00"`), `entry_end` (L47, `"15:00"`) and the other trading-hour keys, with the holiday file and `special_sessions` | `main.py` L2317 to L2329 build `MarketWindows` | receiver L582 (`is_entry_allowed(now)`); processor L911 (`is_entry_allowed`) and L977 (`is_entry_allowed_for_strategy`, which also reads the strategy's `entry_start_time` and `entry_end_time`); `core/market_windows.py` L143 to L150: `entry_start <= t < entry_end` on a non-holiday | A01 (`MarketWindows`); A02 (keys) | P02-S043, P04-S028, P04-S032 |
| `trade_type` (L149, `BOTH`); `force_intraday_only` (L142, `false`) | `main.py` L3620 to L3621; constructor L193 to L194 (defaults `"INTRADAY"` and `False`), L237 to L238 | `strategy_will_trade(strategy_obj, trade_type=..., force_intraday_only=...)` at L959 to L962, before screening | A07 (`strategies/control.py`) | P04-S032; A02 K-05 |
| `strategy_circuit_breaker` (section) | `main.py` L846 to L860 (`_build_strategy_governor`), L3618; constructor L191, L235 | `self._strategy_governor.check(strategy_name, now.time())` at L985 to L990, before screening | A09 | P04-S032 |
| `sr_detector.sl_buffer_pct` (L540, `0.2`) | `main.py` L3421 (`_sr_cfg`), L3610 (`retest_sl_buffer_pct=_sr_cfg.sl_buffer_pct`); constructor L188 (default `0.2`), L232 | L2438 to L2441, in `continue_from_retest` only (after the handoff; the callback of A08's `RetestMonitor`) | after the handoff (P04-S042: A07's and A18's paths; P05-S044 maps it) | P05-S041, P05-S044; A02 K-22 |
| `watchlist.enabled` | `main.py` L3477 to L3478, L3747 (`set_eod_capture`) | whether an end-of-day scanner alert has a capture worker | A18 | P01-S023 |
| `sr_detector.enabled` (L509), `sr_detector.wait_for_retest_enabled` (L529), `portfolio_allocator.allocator_mode` (L565), `v3_chain.v3_chain_mode` (L574) | `main.py` construction and late binding | which collaborators the processor holds | A08, A18 | P05-S038, P05-S040, P05-S041 |
| `risk.one_trade_per_symbol_direction_per_day` | `RiskEngine` keeps `_one_trade_per_symbol_direction` (`capital/risk_engine.py`, search) | processor L834 reads the private attribute with `getattr(..., False)`, inside `_enforce_one_trade_per_symbol_direction` (called at L1312, after the handoff) | A09 | P05-S036 row 11; A02 K-49 |
| `position_sizing` performance-weight keys | not passed (`perf_weights` stays `{}`) | L1120, L2116, L2458: `.get(name, 1.0)` (after the handoff) | A09 | P04-S002; A02 K-09 |

P08-S016. INTERPRETATION (P04-S002; P08-S012; P08-S015): every processor constructor parameter that carries a
configuration value is passed by `main.py`, except `perf_weights`; so the constructor defaults `60` (expiry), `5`,
`0.1`, `"WARN"`, `0.003`, the four throttle defaults, `0.2`, `"INTRADAY"` and `False` never apply in the `main.py` path.
Where a constructor default differs from the schema default (`force_intraday_only`: constructor `False`, schema `True`,
`core/config_loader.py` L2030; `signal_expiry_sec`: constructor `60`, schema required), the difference matters only to
other callers of the constructor (tests, scripts).

### 3.7 The same setting at each layer

P08-S017. FACT (P08-S007 to P08-S016): the value of each A06 setting at each layer that holds one ("req." = required
schema field without a default; "—" = the layer does not hold a value):

| Setting | File | Schema default | `main.py` | Constructor default | Consumer fallback or floor |
|---|---|---|---|---|---|
| `signal_queue.expiry_sec` | 600 | req. (comment "default 60") | passed | 60 (processor) | — |
| `signal_queue.warning_pct` | 0.60 | 0.60 | — | — | `getattr` 0.60 |
| `excluded_symbols` | 5 entries | `[]` | — | — | `getattr` `[]` |
| `webhook.require_hmac` | false | req. | — | — | `getattr` False |
| `webhook.dedup_window_seconds` | 300 | 300 | — | — | `getattr` 300; error 300; floor 60 |
| `webhook.per_ip_rate_limit_enabled` | true | True | — | — | `getattr` True |
| `webhook.per_ip_burst` | 60 | 60 (>= 1) | — | — (the limiter's `burst` parameter has no default, L79) | `getattr` 60; `or 60`; limiter floor `max(1, int(...))` (L80) |
| `webhook.per_ip_refill_per_sec` | 5.0 | 5.0 (>= 0) | — | — (no default, L79) | `getattr` 5.0; `or 5.0`; limiter floor `max(0.0, ...)` (L81) |
| `webhook.bind_host`, `bind_port` | all-interfaces address, 5000 | req. (comments name defaults) | read | — | — |
| `signal_processor.worker_count` | 5 | req. (1 to 50) | passed | 5 | `max(1, ...)` |
| `signal_processor.drain_poll_sec` | 0.1 | req. (> 0) | passed | 0.1 | — |
| `signal_processor.tgt_min_pct` | 0.003 | 0.003 | passed | 0.003 | — |
| entry-throttle gap, window, burst, cooldown | 20, 60, 3, 300 | 0.0, 60.0, 0, 0.0 | `getattr` 0.0, 60.0, 0, 0.0 | 0.0, 60.0, 0, 0.0 (processor and `EntryThrottle`) | `or` and `max` floors (P06-S005) |
| `signal_processor.atr_fallback_mode` | absent | "WARN" | passed | "WARN" | — |
| `trade_type` | BOTH | "INTRADAY" | passed | "INTRADAY" | — |
| `force_intraday_only` | false | True | passed | False | — |
| `sr_detector.sl_buffer_pct` (as `retest_sl_buffer_pct`) | 0.2 | 0.2 | passed | 0.2 | — |
| `scanner_check_delay_sec` | 5.0 | 5.0 | — (A01 reads it: `getattr` 0.0) | function default 0.0 | — |

P08-S018. INTERPRETATION (P08-S017; P08-S006): at the file values no layer's default is used for any A06 setting,
because every key is present (except `atr_fallback_mode`, whose schema default `"WARN"` applies). If a key were deleted,
the schema default would apply: for `excluded_symbols` an empty list, for the four throttle keys a throttle that admits
every entry (P06-S024), for `trade_type` and `force_intraday_only` the values `"INTRADAY"` and `True` (their effect is
A07's). A required key that is deleted makes validation fail (P08-S002).

## 4. Other configuration files and sources read by A06 code

### 4.1 `config/scan_webhook_map.yaml` (A02's file; `ScanWebhookMapConfig`, `ScannerEntry`)

P08-S019. FACT (`config/scan_webhook_map.yaml` L16 to L84; `core/config_loader.py` L2347 to L2377): `scanners` holds
16 entries; each has `strategy` and `chartink_url`; only `pb01_breakout_retest` (L81 to L84) adds `scanner_type: eod`.
In every entry the scanner key and the strategy name are the same text. The schema requires `strategy: str` and
`chartink_url: str` (validator: must start with `http://` or `https://`, L2359 to L2364) and gives `scanner_type` the
default `"intraday"`, allowing only `intraday` or `eod` (L2357, L2366 to L2371). The URL values are not reproduced
(P07 studies both scanner files in whole).

P08-S020. FACT (search `chartink_scanners|chartink_url|scanner_type` in non-test, non-document code; reader lines as
cited): who reads each part of an entry:

| Part of the entry | A06 readers | Other readers (interface only) | Statements |
|---|---|---|---|
| the scanner key | receiver L552 to L554 (path segment must be a key, else 404), L562 (`known_scanners.get`); processor L933 (`self._scan_webhook_map.get(scanner_name)`), L573 (`_evidence_strategy_for`) | `utils/startup_checks.py` L687 (iterates the entries; A01's function, also used by the Appendix A script) | P01-S035, P02-S044, P04-S030 |
| `strategy` | processor L939 to L942 (dict key or attribute); L576 to L577 (evidence) | the dashboard's raw readers (`ops_dashboard/backend/readers/config_reader.py` L92 to L99 and L281; A15); `strategies/loader.py` `_validate_scan_webhook_map` L169 to L210, reached only when a map path is passed (L152 to L153; A02 T-02: not requested outside tests) | P04-S030, P04-S035 |
| `chartink_url` | none in `signals/` | `utils/startup_checks.py` L764 to L776 (`_resolve_url`; A01's), reached through A01's start-up check (`main.py` L2458 to L2459; `utils/startup_checks.py` L1592 to L1595) and through the Appendix A script; the dashboard (`config_reader.py` L281 to L286; `services/scanner_attribution.py` L664 to L674; A15) | section 4.3 |
| `scanner_type` | receiver L563 (`getattr(_entry, "scanner_type", "intraday") == "eod"`); the processor never reads it | none | P01-S035, P04-S031 |

P08-S021. FACT (`signals/signal_processor.py` L207 to L208; `signals/webhook_receiver.py` L552; P04-S009, P04-S031):
the processor keeps a shallow copy of `scanners` taken at construction; the receiver reads the mapping from its
configuration object on every request. HISTORICAL (`config/scan_webhook_map.yaml` L3 to L6, header): "Validated at
startup (P17, S10): every strategy name must have a corresponding YAML file in config/strategies/. Duplicate scanner
names -> CRITICAL startup failure." A02 T-02 recorded that neither check runs outside tests (section 8, T-02).
HISTORICAL (L78): "Routing key MUST equal the /webhook/<scanner_name> URL path Rama pastes into Chartink." This agrees
with the receiver's exact key test (P02-S044).

### 4.2 `config/chartink_scanners.yaml` (A02's file; `ChartinkScannersConfig`)

P08-S022. FACT (`config/chartink_scanners.yaml` L15 to L32; `core/config_loader.py` L2385 to L2388;
`utils/startup_checks.py` L680 to L681, L756 to L761, L764 to L776, A01's file, interface only): the file maps the same
16 scanner names to URL texts (schema `dict[str, str]`). It is read by `_get_chartink_dict` and used by `_resolve_url`
only as the last fallback, when an entry has no `chartink_url` attribute and is neither a string nor a dict with that
key (L775 to L776). No A06 file reads it; the Appendix A script passes `app_config.chartink_scanners` through
(`scripts/preflight_scanner_check.py` L208 to L210).

P08-S023. INTERPRETATION (P08-S019, P08-S022; current external context, pydantic "Validation Errors", read
17-Nov-2026: the `missing` error "is raised when there are required fields missing from the input value"): every
entry that `load_all` builds is a `ScannerEntry`, which always has the required `chartink_url`, so `hasattr(entry,
"chartink_url")` (L767) is true for every entry and the fallback to `chartink_scanners.yaml` is not reached in the
startup check or in the Appendix A script. The file's URLs are therefore loaded and validated as text but not used by
the reachability check. HISTORICAL against FACT (`config/chartink_scanners.yaml` L3 to L5, header): "scripts/preflight_
scanner_check.py sends an HTTP HEAD request to each URL and fails CRITICAL if any is unreachable at startup"; the script
uses `requests.get` (L101) and returns exit code 1 (L225 to L231); the start-up check appends the warning
`scanner_unreachable` (`utils/startup_checks.py` L1596 to L1597). HISTORICAL (L12 to L13): "URLs are placeholders.
Replace with actual Chartink screener URLs once scanners are configured and active in Chartink." Whether the two files'
URLs agree is P07's.

### 4.3 The Appendix A script's own settings (`scripts/preflight_scanner_check.py`)

P08-S024. FACT (`scripts/preflight_scanner_check.py` L34 to L57, L64 to L75, L161, L176 to L214): the script's
settings are three command-line options, four module constants and its logging set-up; it reads no environment
variable (search for `os.environ|getenv`: no hit):

| Setting | Line | Value or default | Use |
|---|---|---|---|
| `--config` | L39 to L44 | `"config"` (a path relative to the working directory) | checked to be a directory (L184 to L187, else exit 1); `load_all(config_dir)` (L197; any load error gives exit 1, L198 to L200) |
| `--timeout` | L50 to L56 | `10` (seconds, `int`) | `timeout_override` of the fetcher (L206) and `timeout_sec` of the check (L213) |
| `--verbose` | L45 to L49 | off | prints up to 200 characters of each captured response (L154 to L166) |
| `_HEADERS` | L64 | a fixed `User-Agent` text | every request (L101) |
| `_SNIPPET_LEN` | L65 | `300` | characters of each response kept (L102) |
| `_PREFLIGHT_RETRIES` | L74 | `2` (up to three attempts) | network errors and 5xx answers are retried; 4xx is not (L99 to L117) |
| `_PREFLIGHT_RETRY_BACKOFF_SEC` | L75 | `1.0` | sleep between attempts (L108, L115) |
| logging | L176 to L180 | level WARNING to standard error | |

Configuration keys read through `load_all`: the entries of `scan_webhook_map.scanners` (key and `chartink_url`, through
A01's `check_scanner_connectivity`) and `chartink_scanners.scanners` (passed, fallback only, P08-S023). The script does
not pass `delay_sec`, so `scanner_check_delay_sec` has no effect on it (P08-S014). What the check does and does not
check is P07's.

### 4.4 The strategy files (A02's files; `StrategyConfig`)

P08-S025. FACT (`signals/signal_processor.py` L933 to L1004; `core/market_windows.py` L152 to L175, A01's file;
`strategies/control.py`, A07's file, whose reads of `intent` and `enabled` at L76 to L77 A02 recorded in
`evidence/A02_STRATEGY_CONFIGURATION_2026-11-06.md` L444 to L445): up to the
screening call the processor's own code reads, from the strategy object found through the map: its presence in
`self._strategies` (L948); `entry_start_time` and `entry_end_time` (only in the reject text, L981; the window check
itself reads them inside `MarketWindows.is_entry_allowed_for_strategy`); `direction` and `intent` (passed to the
screener, L1000 to L1001). It hands the whole object to `strategy_will_trade` (L959 to L962; A07) and to the screener
(`strategy=strategy_obj`, L1002; A07). A02 recorded the same field-to-line map (`evidence/A02_STRATEGY_CONFIGURATION_
2026-11-06.md` L442 to L456).

P08-S026. FACT (processor search for `strategy_obj\.[a-z_]+|strategy\.[a-z_]+`; interface only, Rama's decision A;
owners from P05-S036): after the screening call the processor's code reads further strategy fields: `name` (L1120,
L2116, L2458, as the performance-weight key; logs L1830, L1890); `direction` (L1034, L1045, L1379, L1558, L1775, L1910);
`intent` (L1047, L1117, L1316, L1329, L1452, L1560, L1593, L1641 and the two resume paths); `entry_method` and
`entry_offset_pct` (L1779 to L1796); `sl_method`, `sl_pct`, `sl_min_pct`, `sl_max_pct` (L1801 to L1867);
`sl_gap_buffer_pct` (L1877, `getattr` default 0.0, used as a percent at L1883); `tgt_method`, `tgt_pct`,
`tgt_risk_reward` (L1911 to L1932; `tgt_risk_reward` also L1459, L2265, L2560); `pullback_wait_enabled` (L1082);
`lot_size` (L1119, L2115, L2457); `max_concurrent_positions` (L760, `getattr` default 2); `v3_playbook` (L1603). The
price derivation, sizing and caps that use them are A09's (code in A06's file; P05-S036 rows 1, 4, 10, 15).

P08-S027. FACT (`git grep` of `sl_method:`, `tgt_method:`, `sl_gap_buffer_pct:` in `config/strategies/`; 16 files):
every strategy file sets `sl_method: "FIXED_PCT"` and `tgt_method: "RISK_REWARD"`; four set `sl_gap_buffer_pct: 0.3`
(comment "FIX-130: widen SL 0.3% during 09:15-09:30 gap-risk window", HISTORICAL); the three positional files carry the
comment "ATR not yet implemented; using FIXED_PCT until ATR data available" (HISTORICAL). No file sets an ATR method,
and `config/system_config.yaml` has no `atr_fallback_mode` line.

### 4.5 `config/symbol_aliases.yaml` and the account file

P08-S028. FACT (P01-S018, P04-S047, P04-S048; `signals/webhook_receiver.py` L227, L258 to L292): the alias file is read
once, in the receiver's constructor, from a path relative to the working directory, not through `load_all` and not from
the `--config` directory; a missing or unreadable file gives an empty map. The file holds two entries (P04-S048). The
alias file and the alias tool are A02's and A05's (P04-S048 cites the A05 record); the consumer in the receiver is
A06's (direction question 18: "Do not take ownership of A05's instrument cache or alias tool").

P08-S029. FACT (P01-S049, P01-S051; `signals/webhook_receiver.py` L57, L111 to L138, L620 to L626): the receiver's
WR4b step calls A01's `primary_account_tag()` (L129) on every intraday request that reaches the WR4 step with a
`scan_name` in its body; that function reads the account file at a
path fixed relative to its module and caches its first result (A01 M-37 and M-43, as P01-S051 records). The account
file is named here as a configuration source only; it was not opened and no value is reproduced.

## 5. Environment-variable names and fixed code settings

### 5.1 Environment variables

P08-S030. FACT (search for `os\.environ|getenv|environ\[` in the four A06 files: no hit; `main.py` L3414; L219 to L232;
P02-S009, P02-S011): no A06 file reads an environment variable. The only environment-variable NAME read for an A06
component is `WEBHOOK_SECRET`, which `main.py` reads once with `os.environ.get("WEBHOOK_SECRET")` (L3414; `None` when
unset) and passes as the receiver's `secret_token`. The same name is one of the four names returned by
`required_startup_secrets` (L227 to L232), which A01's startup check treats as blocking when unset or empty
(P02-S011). It also appears in the name lists of `scripts/preflight/checks/config_integrity.py` L30 and
`scripts/premarket_healthcheck.py` L50 (other topics' scripts; names only, interface only). No value is examined or
reproduced (security rules). Flask settings that the documentation ties to environment variables are recorded in
P02-S073 (no code sets `DEBUG` or `PROPAGATE_EXCEPTIONS`).

P08-S031. INTERPRETATION (P08-S030; `signals/webhook_receiver.py` L177 to L182, L330 to L331; P02-S015): because the
receiver reads `require_hmac` from the configuration but the secret from the environment, the two settings that
together decide authentication come from different sources: the file (A02) and the process environment (A01 and A17).
With the file value `require_hmac: false` and a secret present, both the signature and the token routes are open
(P02-S016); with no secret, the receiver itself would accept every request (P02-S015 (a)), which the blocking startup
check is there to prevent (P02-S011).

### 5.2 Fixed settings in the code (not configurable)

P08-S032. FACT (lines as cited): settings held as literals in A06 code or at A06 call sites in `main.py`; none has a
configuration key:

| Setting | Where | Value | Statements |
|---|---|---|---|
| in-flight claim timeout | `signals/webhook_receiver.py` L208 | `60.0` s | P01-S015 |
| sweeper interval | L1189 (`_sweeper_stop.wait(timeout=60.0)`) | `60.0` s | P01-S076 |
| dedup cache size | L237 (`TTLCache(maxsize=10000, ...)`) | 10,000 keys | P01-S019, P03-S004 |
| dedup window floor | L236 (`max(60, ...)`) | 60 s | P03-S003 |
| request body limit | L251 (`MAX_CONTENT_LENGTH`) | 1,048,576 bytes | P01-S021, P02-S063 |
| per-IP map size | L79 (`max_ips: int = 8192`; not passed) | 8,192 addresses | P03-S020 |
| raw body in logs | L522, L591 | first 1,000 and 500 characters | P02-S034 |
| retryable statuses | L66 (`_RETRYABLE_STATUSES`) | `QUEUE_FULL`, `STORE_ERROR` | P01-S004 |
| server threads and connection limit | `main.py` L3994 to L3995 | 8 and 100 | P01-S064, P01-S067 |
| boot self-check | `main.py` L4003 to L4005 | 2 s sleep; loopback `/health` on `bind_port` | P01-S059 |
| dispatcher join at stop | `signals/signal_processor.py` L336 | 10.0 s | P04-S017 |
| re-put timeout (pre-check and FIX-069) | L426, L1520 | 1.0 s | P04-S053, P03-S043 |
| FIX-069 retry limit | L1493 (`retry_count >= 3`) | 3 | P04-S052 |
| expired-alert spacing | L1224 | more than 60.0 s | P04-S043 |
| gap window for `sl_gap_buffer_pct` | L1745 to L1746 | 09:15 to 09:30 (after the handoff) | A02 K-02; section 8 |
| strategy cap default | L760 (`getattr(strategy_obj, "max_concurrent_positions", 2)`) | 2 (after the handoff) | P05-S036 row 10 |
| entry-throttle internals | `signals/entry_throttle.py` | as P06 records (clock, floors) | P06-S005 |
| Appendix A script constants | `scripts/preflight_scanner_check.py` L64 to L75 | P08-S024 | P08-S024 |

HISTORICAL (`core/config_validator.py` L9 to L14, docstring): the module's "Problem Statement (2026-04-28 paper
testing)" names "signal_expiry_sec: config=600, code default=60" and "in_flight_release_fn: defaulted to None instead of
mandatory injection" as examples of hard-coded defaults that bypass configuration; A02 recorded that the validator is
never fed (A02 V-01, STUDY question 10). At `970aabf` `main.py` passes both (L3612, L3614).

## 6. Keys that nothing reads, and fallbacks that do not apply

P08-S033. FACT (P08-S007 to P08-S029): within A06's configuration surface:
- `signal_processor.pipeline_timeout_sec` (L347) has no reader anywhere in non-test code (P04-S004; A02 K-13).
- `chartink_scanners.yaml` is loaded and passed, but its URLs are used only as a fallback that loaded entries never
  reach (P08-S022, P08-S023, INTERPRETATION).
- `scan_webhook_map` `chartink_url` is read by no A06 runtime code; only A01's reachability check (and so the Appendix
  A script) and the dashboard read it (P08-S020).
- `scan_webhook_map` `scanner_type` is read by the receiver only; within A06 code `strategy` is read by the processor
  only (the dashboard and the strategy loader's S10 check read it outside A06; P08-S020).
- `scanner_check_delay_sec` is read by A01's start-up check only; it has no effect on the Appendix A script (P08-S014).
- `webhook.bind_host` and `bind_port` appear in the receiver only in its class docstring (L148 to L149, HISTORICAL
  usage example with `app.run`); the server is waitress, started by `main.py` (P01-S064).
- `sr_detector.retest_sl_buffer_pct` (schema field L1182, default 0.3, absent from the file) is not what the processor
  receives: its parameter `retest_sl_buffer_pct` is fed from `sr_detector.sl_buffer_pct` (P08-S015; A02 K-22).
- `delivery_enabled` (L155) and the `position_sizing` performance-weight keys are not passed to the processor (A02 K-05,
  K-09).
- Every `getattr` fallback on a declared schema field in A06 code (`require_hmac`, `dedup_window_seconds`, the three
  per-IP keys, `warning_pct`, `excluded_symbols`) and in `main.py`'s A06 arguments (the four throttle keys), and every
  processor constructor default for a passed value, is unused under `main.py` (P08-S006, P08-S016, INTERPRETATION).

P08-S034. FACT (search of `signals/webhook_receiver.py` and `main.py` L3402 to L3415): the receiver's in-flight
timeout, sweeper interval, cache size and body limit (P08-S032) are not configurable, while the dedup window that the
cache's time-to-live follows is (P08-S010). INTERPRETATION: the dedup window can be set from 60 s upwards, but the
claim timeout and the sweeper interval stay at 60 s whatever the window (their interplay is P01-S079 and P03-S032).

## 7. `config/expected_managers.yaml`: the declared effect points (HISTORICAL declarations)

P08-S035. HISTORICAL (`config/expected_managers.yaml` L1 to L27; `git log`: `a5c3704` 01-Aug-2026 "docs(telemetry):
ledger #1 Phase A -- freeze the effect-verification contract + expected-manager registry (NO CODE)", `4959111`
01-Aug-2026, `0197923` 04-Aug-2026): the header calls the file "the single source of truth (C2/C6)", "Frozen 01-Aug-2026
against deployed code 297b587", says it is "NOT part of the system_config.yaml schema" and "Consumer:
core/effect_telemetry (Phase B — NOT YET BUILT; until then this file is the frozen contract artifact)". FACT (`core/
effect_telemetry.py` L63, L129 to L142, L152 to L215, L219 to L307; `main.py` L1662 to L1673, L4225 to L4246): at
`970aabf` the consumer exists: it loads the file from the relative path `config/expected_managers.yaml` and uses only
the fields `managers`, `name`, `state`, `modes` and `reason` (search for `.get("...")`); `main.py` calls
`assert_composition` at the end of boot and `emit_census` at shutdown. FACT (`git log --diff-filter=A`): the registry
was added by `a5c3704` (01-Aug-2026, 21:27 IST) and `core/effect_telemetry.py` by `132e571` (01-Aug-2026, 23:31 IST,
"feat(telemetry): ledger #1 Phase B -- effect-verification counters, ..."). INTERPRETATION: the header's "NOT YET BUILT"
was written before the consumer was added the same evening and no longer describes the code; the fields `class`, `ctor`,
`effect_point`, `acted_means` and `note` are read by no code and are text only.

P08-S036. HISTORICAL (`config/expected_managers.yaml` L57 to L63; `git blame`: every line from `a5c3704`): the
`signal_processor` entry declares `class: signals.signal_processor.SignalProcessor`, `ctor: "main.py:3058"`, `state:
expected-active`, `effect_point: "signals/signal_processor.py:1230 _process_one dispatch to order_placer.place()"`,
`acted_means: "an approved entry dispatched to placement"` and a note that the resume sites ":1995/:2272" are
excluded. FACT (`signals/signal_processor.py` L55, L217, L1410 to L1446, L1230; `main.py` L3575): at `970aabf` the
constructor call is at `main.py` L3575; the counter handle is taken once in the processor's constructor
(`self._fx_dispatch = _effect_handle("signal_processor")`, L217) and incremented at L1423, between the throttle's
`admit` (L1410) and `place()` (L1446) on the FCFS path only (P06-S032); L1230 is the `except Exception: pass` of the
expired-signal alert. FACT (added in the check; `git show 297b587:<path>`, read-only): at the frozen commit `297b587`
named in the header (L4, L27), `main.py` L3058 is the `SignalProcessor(` constructor call and
`signals/signal_processor.py` L1230 is `self._placer.place(`, so the entry's line references are those of `297b587`,
not of the baseline. INTERPRETATION: the declared effect point lies after the A07 handoff (it counts dispatches to placement, not intake), so it
is not an A06 intake measure.

P08-S037. HISTORICAL (`config/expected_managers.yaml` L149 to L154; every line from `a5c3704`): the `webhook_receiver`
entry declares `class: signals.webhook_receiver.WebhookReceiver`, `ctor: "main.py:2892"`, `state: covered-existing`,
`effect_point: "webhook_audit day-count (WR13 finally, webhook_receiver.py:498-503) — NO new counter"` and
`acted_means: "a POST audited"`. FACT (`main.py` L3407, L4238 to L4240, L1662 to L1673; `signals/webhook_receiver.py`
L494 to L504, L529 to L534; `core/effect_telemetry.py` L257 to L267): at `970aabf` the constructor call is at `main.py`
L3407; `main.py` registers the name with `register_constructed("webhook_receiver")` (no counter); the census line for a
`covered-existing` entry is the day's `SELECT COUNT(*) FROM webhook_audit WHERE date = ?` (P03-S053); the receiver's
L498 to L503 are the audit write and log line of the 429 path, and the `finally` audit write ("WR13 finally") is at
L529 to L534. FACT (added in the check; `git show 297b587:<path>`): at `297b587`, `main.py` L2892 is the
`WebhookReceiver(` constructor call and `signals/webhook_receiver.py` L498 to L503 are the `finally:` block with the
audit write, so the references are the frozen commit's (P01-S090 noted the constructor line). INTERPRETATION: the
declaration agrees with the census code that the count is of audited POSTs, not of accepted
signals (P03-S053).

P08-S038. INTERPRETATION (`core/effect_telemetry.py` L1 to L42, docstring "OBSERVATIONAL ONLY"; L152 to L215): the
registry changes no A06 behaviour. Its effects are the boot composition assertion, which in live mode logs a CRITICAL
line and sends an alert on a mismatch and continues (L207 to L215) and in paper or development mode raises (paper-only;
not traced), and the census lines written at shutdown (L219 to L307). Whether any census or composition line was ever
produced is UNKNOWN / NOT ESTABLISHED.

## 8. Cross-check against the A02 records (A06 side only)

Each item keeps its A02 ID, owners, classification, status and treatment (Topic Completion Register, A06 entry). The
first statement of each pair quotes the A02 record (HISTORICAL, record); the second states what A06's code shows. Where
the A06-side code lies after the A07 handoff it is recorded at the interface only (Rama's decision A), because A02
handed it to A06; the logic stays with the owners P05-S036 names.

### 8.1 T-02

P08-S039. HISTORICAL (record; `A02_AUDIT_2026-11-08.md` L988, L1308, quoted): title "The S10 cross-check is never
requested, while the map's header and the decisions say it runs at startup"; handoff to A01 and A06: "P17 (b)
map-to-strategy and (d) duplicate scanner names are not checked at startup (`utils/startup_checks.py`;
`scripts/preflight_scanner_check.py`); runtime rejection `UNKNOWN_STRATEGY` at `signals/signal_processor.py` L948 to
L953". Classification as recorded: "ISSUE / FACT"; KNOWN DEFECT "considered and not given".

P08-S040. FACT (A06 side; `scripts/preflight_scanner_check.py` L184 to L214; P04-S007, P04-S030, P04-S031): the
Appendix A script does three things with configuration: it checks the directory, calls `load_all` and calls the
reachability check; it compares no map entry with the strategy files and has no duplicate-key check. At runtime a
map entry whose strategy is not loaded is rejected per signal as `UNKNOWN_STRATEGY` (L948 to L953; P04-S030), the only
one of the three `UNKNOWN_STRATEGY` branches reachable under `main.py`'s wiring (P04-S031). At the baseline files every
map strategy has a strategy file (P04-S031; A02 T-02). A02's reading of duplicate keys in the map file (the last entry
kept, an INTERPRETATION from PyYAML) is A02's and is not re-examined here.

### 8.2 T-07

P08-S041. HISTORICAL (record; L1058, L1310, quoted): title "The `*_pct` unit convention differs inside the schema";
handoff to A06: "`sl_gap_buffer_pct` divided by 100 (L1877 to L1883) and whether it can act before the 10:00 floor";
the AUDIT's own wording: "INTERPRETATION, for A06 to confirm: the buffer applies only between 09:15 and 09:30, while the
global entry floor `trading_hours.entry_start` is 10:00 (file value, `config/system_config.yaml` L28), so at the
baseline file values it may never act." Classification: "ISSUE / FACT (the two conventions) and INTERPRETATION
(effect)".

P08-S042. FACT (A06 side only: the key's read site and the call-site contract, at the interface, Rama's decision A;
`signals/signal_processor.py` L910 to L912, L1026 to L1030, L1096 to L1100, L1745 to L1746, L1877, L1881, L1883;
`core/market_windows.py` L143 to L150, A01's file; search: `_derive_prices(` is called only at L1028 and L1098; corrected
in the check): the strategy key `sl_gap_buffer_pct` is read only inside `_derive_prices`, with
`getattr(strategy, "sl_gap_buffer_pct", 0.0)` (L1877); that method lies after the A07 handoff and its price rule is
A09's (P05-S036 row 1: "A09 (price decisions; code in A06's file)"). At the read site the value is taken as a percent
(`gap_buffer / 100.0`, L1883), which is the unit point A02 recorded in T-07, and the time it is tested against is
bounded by the class literals `_GAP_WINDOW_START` 09:15 and `_GAP_WINDOW_END` 09:30 (L1745 to L1746, compared at
L1881). The contract A06 passes: both call sites pass `now_time=now.time()`, where `now` is the worker's `now_ist()`
of L910, which L911 has already required to pass `is_entry_allowed(now)`, that is a non-holiday time with
`entry_start <= now.time() < entry_end`, `entry_start` being the configured `trading_hours.entry_start` (no
special-session override in that method). INTERPRETATION (contract only): every `now_time` the two call sites pass is
at or after the configured `entry_start` (10:00 at the file value, `config/system_config.yaml` L28), so at the file
values it never lies between 09:15 and 09:30; this agrees with A02's T-07 reading as far as the A06-side contract goes.
How the buffer moves the stop, and the confirmation of the effect inside the price rule, are A09's (P05-S036 row 1)
and are not audited here (P08-S074). HISTORICAL (`config/system_config.yaml` L28 to L39, comments): the 10:00 value is
called a "[LAUNCH-PHASE]" floor over the per-strategy windows, to be relaxed later.

### 8.3 T-12 and the open issue A02-03

P08-S043. HISTORICAL (record; L1128, L1310, quoted): title "The schema accepts ATR methods that the consumer does not
implement"; handoff to A06: "the ATR branches and their fallbacks (L1801 to L1846, L1913 to L1940)"; the AUDIT's
reading "INTERPRETATION from the consumer (A06 to confirm): such a strategy's signals are rejected (`ZERO_SL`, L1825 to
L1835) or, for the target, fall back to a zero distance that the BL-16 guard rejects; with
`signal_processor.atr_fallback_mode` set to `HALT` they are rejected as `REJECTED_NO_ATR_DATA`". Classification:
"ISSUE / INTERPRETATION". Open issue A02-03 (`OPEN_ISSUES_REGISTER_2026-11-05.md` L481 to L495, quoted): question
"Do S6's ATR stop-loss and target methods remain the intent for the three positional (DELIVERY) strategies, which the
files set to a fixed 2 % stop and a 1.5 R target?"; owner "Rama decides; Claude records. Topic: A02 (files and
headers); A06 for the ATR branches."; status "History: OPEN QUESTION (Rama answered OPEN on 08-Nov-2026). Treatment:
AGREED in part (08-Nov-2026: Rama's new-system input, confirmed in the read-back as an accurately recorded Phase 2
input); OPEN QUESTION in part (its design details, left for Phase 2). Not an approved V2 design decision."

P08-S044. FACT (A06 side only: configuration and interface, Rama's decision A; `core/config_loader.py` L572;
`main.py` L3593; `signals/signal_processor.py` L177, L224, L1801 to L1803, L1911 to L1914; P08-S012; corrected in the
check): `signal_processor.atr_fallback_mode` (schema `Literal["WARN", "HALT"]`, default `"WARN"`) is absent from the
file, so the loaded value is the schema default `"WARN"`; `main.py` passes it to the processor (L3593; constructor
L177, kept at L224). The processor reads it only at L1803 and L1914, each reached only when the strategy's
`sl_method` (L1801 to L1802) or `tgt_method` (L1911 to L1913) is `"ATR"`; both reads lie inside `_derive_prices` and
`_derive_target`, after the A07 handoff, owned by A09 (P05-S036 rows 1 and 15). FACT (P08-S027; the three positional
files L10, L21, L22, L29): no strategy file sets either method to ATR; the three positional (DELIVERY) files set
`sl_pct: 0.02` and `tgt_risk_reward: 1.5` with the comment "ATR not yet implemented; using FIXED_PCT until ATR data
available" (HISTORICAL). INTERPRETATION (configuration only): at the committed files the branches that read
`atr_fallback_mode` are not selected, so the setting has no effect at the baseline files; this agrees with A02's "no
file uses ATR, so latent". What the ATR branches and their fallbacks do (A02's reading of `ZERO_SL`, the BL-16 guard
and `REJECTED_NO_ATR_DATA`) is the logic of the price derivation, owned by A09, and is not audited here (P08-S074); the
form of the HALT reject label is recorded in P05-S013. A02-03's owner field names "A06 for the ATR branches"; A06
records the configuration and interface side above. A02-03's history stays OPEN; Rama's Phase 2 input recorded there
is not evidence of legacy intent and is not used here.

### 8.4 T-14

P08-S045. HISTORICAL (record; L1156, L1310, quoted): title "Strategy fields that are configured and that nothing reads
(A02's part of the A07 handoff)"; handoff to A06: "strategy fields read: `direction`, `intent`, `name`, `entry_method`,
`entry_offset_pct`, `sl_*`, `tgt_*`, `pullback_wait_enabled` (L1082), `lot_size`, `max_concurrent_positions` (L760,
`getattr` default 2), `v3_playbook` (L1603)". Classification: "ISSUE / FACT for A02's part".

P08-S046. FACT (A06 side; P08-S025, P08-S026; search of the three `signals/` files for `sl_atr_multiplier`,
`tgt_atr_multiplier`, `smart_tgt_enabled`, `smart_tgt_trail`, `pullback_wait_tolerance_pct`,
`pullback_wait_timeout_sec`, `active_days`, `order_protocol`, `trailing_sl`: no hit): the processor reads the fields
A02 listed, at the lines of P08-S026; up to the screening call it reads only the strategy's presence, its entry times
(through `MarketWindows`), `direction` and `intent` (P08-S025). None of the fields that A02 found unread is read by
any A06 file.

### 8.5 F-11

P08-S047. HISTORICAL (record; L1521, L1769, quoted): title "`main.py --config` overrides the configuration directory
only for some readers"; handoff row: "Readers in the trading process that ignore `--config`:
`signals/webhook_receiver.py` L265; `core/effect_telemetry.py` L63; `orders/eod_squareoff.py` L696;
`core/strategy_direction.py` L43 to L44; `core/account_registry.py::_read_primary_row` L308 to L310." Classification:
"ISSUE. FACT; INTERPRETATION for the latency."

P08-S048. FACT (A06 side; search of the four A06 files for `Path\(|open\(|\.yaml|\.csv|\.json`): the only file that A06
code opens itself is the alias file, at the relative path of `signals/webhook_receiver.py` L265 (P08-S028). The
processor does not read the expected-manager registry itself (its `handle("signal_processor")` creates a counter and
reads no file, `core/effect_telemetry.py` L102 to L114); the registry is read by the boot assertion and the census
(P08-S035). The account file is read by A01's `primary_account_tag` (P08-S029). The Appendix A script has its own
`--config` option, default `"config"` relative to the working directory, and passes it to `load_all` (P08-S024).
INTERPRETATION: under `main.py --config <other directory>` the receiver would take its aliases from the working
directory's `config/` while `load_all` reads the other directory, as A02 recorded; under the declared unit both are the
project's `config/` (P08-S005).

### 8.6 K-02

P08-S049. HISTORICAL (record; L1834, L2353, quoted): title "Trading-hour values held as literals and in the dashboard's
own copy"; the A06 part of the handoff: "the time literals at ... `signal_processor.py` L1745 to L1746". Classification:
"ISSUE; FACT".

P08-S050. FACT (A06 side; search of the four A06 files for `time\([0-9]|"[0-9]{2}:[0-9]{2}"|_GAP_WINDOW`): the only
clock-time literals in A06 files are `_GAP_WINDOW_START = time(9, 15)` and `_GAP_WINDOW_END = time(9, 30)` (L1745 to
L1746), used only at L1881 for the gap buffer (P08-S042). The receiver and the processor take every other trading-hour
decision through `MarketWindows`, which `main.py` builds from `trading_hours` (P08-S015).

### 8.7 K-04

P08-S051. HISTORICAL (record; L1862, L2355, quoted): title "`excluded_symbols` is read two ways"; handoff to A06 and
A15: "whether excluded symbols are stored as signals; the report's case-sensitive count". Classification: "ISSUE; FACT
(two readers, two matching rules); INTERPRETATION for the effect."

P08-S052. FACT (A06 side; P02-S060; `signals/webhook_receiver.py` L708 to L719): a symbol matched by the list is not
stored: the check runs after the alias step and before `_process_signal`, which is where the `signals` row is
inserted, so a matched symbol gets only the response status `REJECTED_EXCLUDED_SYMBOL` and no row and no queue item.
INTERPRETATION: the daily report's count of stored signals whose symbol is in the list cannot include signals
rejected by this check; which stored rows it does count is A15's.

### 8.8 K-05

P08-S053. HISTORICAL (record; L1876, L2356, quoted): title "The three delivery-gate flags are read with different
predicates and defaults"; owners include "A06 and A07 (strategy control)"; the actual-code-path list includes "L3620 to
L3621 (`SignalProcessor`, without `delivery_enabled`)" and "constructor defaults ... `SignalProcessor` L193 to L194".
Classification: "ISSUE; FACT (different predicates and defaults); INTERPRETATION for the effect."

P08-S054. FACT (A06 side; P08-S015, P08-S016): the processor receives `trade_type` and `force_intraday_only` from
`main.py` (L3620 to L3621) and not `delivery_enabled`; its constructor defaults are `"INTRADAY"` and `False`, the second
differing from the schema default `True`; it stores them (L237 to L238, `force_intraday_only` through `bool()`) and
passes both to `strategy_will_trade` at L959 to L962 before
screening (and at L2063 to L2064 and L2412 to L2413 on the resume paths). The predicate is A07's.

### 8.9 K-09

P08-S055. HISTORICAL (record; L1932, L2360, quoted): title "`dynamic_by_winrate`, `min_multiplier` and
`max_multiplier` have no behavioural effect"; the A06 part: "`signals/signal_processor.py` L192, L236, L1120, L2116,
L2458 (`.get(name, 1.0)`)". Classification: "ISSUE; FACT."

P08-S056. FACT (A06 side; P04-S002; `signals/signal_processor.py` L192, L236, L1120, L2116, L2458): `main.py` does not
pass `perf_weights`, so the processor holds `{}` and every `.get(strategy_obj.name, 1.0)` gives 1.0; all three reads lie
after the handoff (sizing, A09).

### 8.10 K-12

P08-S057. HISTORICAL (record; L1974, L2362, quoted): title "Consumer-side floors and fallbacks replace values that the
loader accepts"; the A06 lines: "`signals/webhook_receiver.py` L233 to L236 (`max(60, …)`), L243 to L244 (`or 60`,
`or 5.0`); `signals/entry_throttle.py` L49 to L52 ...". Classification: "ISSUE; INTERPRETATION (latent)."

P08-S058. FACT (A06 side): recorded in P03-S003 and P03-S021 (receiver: the window floor of 60 governing both dedup
layers; a refill of 0.0 becoming 5.0, so a burst-only limit cannot be configured) and in P06-S005 and P06-S048
(throttle floors). P08-S011 adds that the receiver's `or 60` for a zero burst cannot be reached from a loaded file,
because the schema rejects a burst below 1. At the file values no value is changed (P08-S017).

### 8.11 K-13

P08-S059. HISTORICAL (record; L1988, L2363, quoted): title "`signal_processor.pipeline_timeout_sec` has no consumer";
handoff to A06: "whether any per-signal deadline exists". Classification: "ISSUE; FACT."

P08-S060. FACT (A06 side; P04-S004, P06-S052, P05-S015): the processor has no per-signal deadline in its intake or
worker code; the only time limit applied to a queued signal before the handoff is the age check against
`signal_queue.expiry_sec` (P04-S037). The status `TIMEOUT` that the processor writes belongs to a broker timeout at
placement (`BrokerTimeoutError`, after the handoff; P05-S015, P05-S036 row 21), not to a pipeline deadline.

### 8.12 K-22

P08-S061. HISTORICAL (record; L2114, L2371, quoted): title "The SL-buffer keys: a misnamed path and an untied
duplicate"; the A06 part: "`main.py` L3610 (`retest_sl_buffer_pct=_sr_cfg.sl_buffer_pct`) →
`signals/signal_processor.py` L2438 to L2441". Classification: "ISSUE; FACT."

P08-S062. FACT (A06 side; P08-S015; `signals/signal_processor.py` L188, L232, L2436 to L2442): the processor's
`retest_sl_buffer_pct` is `sr_detector.sl_buffer_pct` (0.2), read only in `continue_from_retest` (L2438 to L2441, taken
as a percent: divided by 100), a resume path after the A07 handoff whose logic is not studied here (P04-S042: A07's and
A18's paths; P05-S044 maps it); the schema field `sr_detector.retest_sl_buffer_pct` (default 0.3) does not reach the
processor. At the committed `wait_for_retest_enabled: false` no diverter is set and the path is not reached
(P05-S041, INTERPRETATION).

### 8.13 K-49

P08-S063. HISTORICAL (record; `A02_AUDIT_2026-11-08.md` L2316 and L2382, quoted): a MATCH row for the `risk` section,
noting that "`one_trade_per_symbol_direction_per_day` reaches the signal processor through a private attribute
(`signal_processor.py` L834, handoff A06)"; handoff: "`signal_processor.py` L834 reads a private risk-engine attribute
with a default".

P08-S064. FACT (A06 side, interface only; `signals/signal_processor.py` L802 to L835, L1312 to L1313, L2142, L2478;
`capital/risk_engine.py` L180, L203; `main.py` L2901; `config/system_config.yaml` L302): L834 reads
`getattr(self._risk, "_one_trade_per_symbol_direction", False)` inside `_enforce_one_trade_per_symbol_direction`,
which the FCFS path calls at L1312 (and the two resume paths at L2142 and L2478), after the handoff; the risk engine
sets the attribute from its constructor argument `one_trade_per_symbol_direction_per_day` (L180, L203), which
`main.py` passes from `risk_cfg` (L2901); the file sets `true` (L302). INTERPRETATION: with a real `RiskEngine` the
default `False` is not used; it would apply only to a risk object without the attribute, in which case the method
returns at once (L834 to L835). The rule itself is A09's (P05-S036 row 11) and is not studied here.

### 8.14 X-01 and the open issue A02-13

P08-S065. HISTORICAL (record; L2411, quoted): X-01 "The `webhook.bind_host` comment still rests the all-interfaces bind
on `require_hmac=true`, which the file sets false"; "How the token check constrained the receiver is A06's.";
classification "ISSUE / FACT". Open issue A02-13 (`OPEN_ISSUES_REGISTER_2026-11-05.md` L601 to L615): the question, the
OPEN history ("Keep all five OPEN") and the treatment "AGREED, with X-01 (batch T5, group G4, 09-Nov-2026)" are quoted
in P02-S036 to P02-S039.

P08-S066. FACT (A06 side): recorded in P02-S040 (the code facts at the file values) and P02-S041 (the intent sources as
they stand), with P02-S042: the code facts do not answer what Rama intended; A02-13's history stays OPEN. P08-S031 adds
the configuration-side fact that `require_hmac` comes from the file and the secret from the environment.

### 8.15 Boundary note (added in the check)

P08-S074. FACT (records: `A02_AUDIT_2026-11-08.md` L1064 (T-07: "for A06 to confirm"), L1134 (T-12: "A06 to
confirm"), L1310 (handoff row T-07, T-12, T-14 to A06), L1349 (section 7.7, "Could not establish": "Whether
`sl_gap_buffer_pct` can act while the global entry floor is 10:00 (A06 to confirm, T-07)"); `OPEN_ISSUES_REGISTER_2026-11-05.md` A02-03 owner field ("A06
for the ATR branches"); `TOPIC_COMPLETION_REGISTER_2026-11-04.md` L109, Rama's decision A of 17-Nov-2026; P05-S036
rows 1 and 15): A02 handed to A06 the confirmation of effects that lie inside `_derive_prices` and `_derive_target`,
which run after the A07 handoff; Rama's later decision A has A06 map those call-outs at the interface only, and P05
names A09 as the owner of the price decisions (code in A06's file). This part therefore records only the A06-side
configuration facts and call-site contracts for T-07 and T-12 (P08-S042, P08-S044) and for K-22 and K-49 (P08-S062,
P08-S064). The items keep their IDs, owners, classifications, statuses and treatments (Topic Completion Register,
A06 entry). OPEN QUESTION for the coordinator, to put to Rama if needed: whether the effect readings that A02 asked
A06 to confirm (T-07, T-12) are confirmed by A09 when that topic is studied, or recorded in A06 at the interface level
used here.

## 9. Configuration as an intent source (direction question 26; recorded only)

P08-S067. HISTORICAL against FACT (sources as cited; no classification, which is the AUDIT's): what the configuration
texts say about A06 behaviour, beside what the code does. "Agrees" and "differs" describe the wording only.

| Text (HISTORICAL) | What it says | Code fact | Wording | Statements |
|---|---|---|---|---|
| `system_config.yaml` L125 | `capacity`: "Max signals in queue before HTTP 503 (P15)" | request-level 503 from a depth of `int(300 * 0.80) = 240`; per-symbol `QUEUE_FULL` (batch 503) at the hard limit 300 | differs in part: two 503 points, neither is "before" 300 alone | P03-S037, P03-S039 |
| L126 | "503 threshold = capacity * backpressure_pct (P15)" | `qsize() >= int(capacity * backpressure_pct)` | agrees (with `int()` truncation) | P03-S037, P03-S047 |
| L127 | `expiry_sec`: "WR6: 10 min - Chartink triggered_at is scan time, not delivery time" | 600 s, measured from `triggered_at` at both stages | agrees on the value; the meaning of the age is P04-S039 | P02-S058, P04-S039 |
| `config_loader.py` L196 | "reject signal older than this many seconds (default 60)" | required field, no default; the processor constructor's default is 60 | differs | P04-S005 |
| L128 | "X-Queue-Warning header above 60% fill" | at or above `int(capacity * 0.60)` | agrees except "above" against "at or above" | P03-S042 |
| L130 | "rejected at webhook edge with DEBUG log only" | as stated, intraday route only | agrees | P02-S060 |
| L328 to L334 | the all-interfaces bind "relies on require_hmac=true plus firewall/security-group restrictions" | `require_hmac: false` (L336) | differs (X-01; history OPEN, A02-13) | P02-S040, P02-S041 |
| L336 | "Chartink cannot sign payloads; use ?token= auth (WEBHOOK_SECRET required in BOTH modes as of C-2 02-Jul)" | token route open when no `sha256=` header; the secret is a blocking start-up requirement | agrees (the paper side is paper-only, not traced) | P02-S011, P02-S016 |
| L337 | "5-min fingerprint bucket (was 60s/1-min)" | 300-second slot and a 300-second cache TTL | agrees | P03-S003, P03-S017 |
| L338 to L339 | "Burst-tolerant for Chartink's open-bell burst (~40 signals from one IP); caps sustained flooding -> 429" | 60 tokens, 5 per second, one token per request whatever the number of symbols; 429 when empty | the code counts requests, the comment signals; Chartink's burst size is UNKNOWN / NOT ESTABLISHED | P03-S020, P03-S021 |
| L345, L346 | "ThreadPoolExecutor workers (1-50)"; "queue poll interval when empty" | validator 1 to 50; `get(timeout=drain_poll_sec)` | agrees | P04-S003, P04-S013 |
| L347 | `pipeline_timeout_sec`: "hard per-signal processing deadline" | no reader | differs (A02 K-13) | P04-S004 |
| L348 | "BL-16: reject signal if target distance < 0.3% of entry" | read at L1945 inside `_derive_target`, after the handoff | not compared here: the logic is A09's (P05-S036 row 15; Rama's decision A) | P08-S012 |
| L349 to L353 | the entry-throttle comments | compared in P06 | — | P06-S021 |
| L753 | "Delay before scanner checks (network stabilization at startup)" | used by A01's start-up check only; not by the Appendix A script | agrees for the start-up check | P08-S014 |
| L567 (`portfolio_allocator.candle_interval_seconds`; `git blame`: `536172c`, 12-Jul-2026) | "short vs the 60s signal expiry" | `expiry_sec` is 600 (since `2e8448c`, 28-Apr-2026, P04-S005) | differs (a comment in another section naming A06's expiry, written after the change to 600; the processor's resume texts say the same, P04-S042) | P04-S005, P04-S042 |
| `config_loader.py` L619, L620 | defaults for `bind_host` (loopback) and `bind_port` (5000) | both required | differs | P01-S065 |
| `config_loader.py` L35 to L40 | "Does not fill in defaults for missing keys" | fourteen A06 fields have defaults | differs | P08-S003 |
| `scan_webhook_map.yaml` L3 to L6 | validated at start-up; duplicate names a CRITICAL start-up failure | neither check runs outside tests | differs (A02 T-02) | P08-S021, P08-S040 |
| `chartink_scanners.yaml` L3 to L5 | the script "sends an HTTP HEAD request" and "fails CRITICAL" | `requests.get`; the script exits 1, the start-up check adds a warning; the file's URLs are not reached | differs | P08-S023 |
| `docs/CONFIG_GUIDE.md` L355, L359 to L363 (last commit `d2426d2`, 28-Jul-2026) | `pipeline_timeout_sec` "hard deadline per signal"; "identical signals within 5 min are de-duplicated"; "queue returns HTTP 503 above 80% full; `expiry_sec: 600` drops signals older than 10 min" | no deadline; fixed 300-second slots plus a 300-second cache; 503 at or above 240; age above 600 s rejected | differs on the deadline; "above 80%" against "at or above"; the dedup wording is a summary of P03's two layers | P03-S003, P03-S017, P04-S004 |
| `config/expected_managers.yaml` L57 to L63, L149 to L154 | the declared effect points | the counter and census as found | line references stale; meaning agrees | P08-S036, P08-S037 |

P08-S068. HISTORICAL (A02 AUDIT L389, L418, L419 and L1964, quoted as A02 recorded them; citation completed in the
check): the module instruction WR14 (`module_19_webhook_receiver.txt`, 2026-04-17) gave "backpressure_pct ...
validated 0-1" and the defaults "default 1000", "default 0.80", "default 60" (L389, L418), and for the server keys
"require_hmac ... default true in production" (L419), while P15 (LOCKED-YAML L352 to L358) gave "Default queue
capacity raised to 300" (L418) and "Backpressure (HTTP 503) still fires at 80% capacity = 240" (K-11, L1964); A02
recorded that the two sources disagree on the capacity. A06 adds no reading of these documents; they are listed here as configuration intent sources for the AUDIT.

## 10. Points the AUDIT may examine (neutral)

- Settings that decide one behaviour come from different sources: `require_hmac` from the file, the secret from the
  environment (P08-S031); the dedup window is configurable while the claim timeout and sweeper interval are fixed at
  60 s (P08-S034).
- Defaults held at up to five layers for one setting, with differences between layers (P08-S017): for example the
  expiry (file 600, schema required with a comment of 60, constructor 60) and `force_intraday_only` (file false, schema
  True, constructor False); none applies at the file values (P08-S018).
- Keys or files that govern nothing in A06: `pipeline_timeout_sec`; the URLs of `chartink_scanners.yaml`;
  `scanner_check_delay_sec` for the Appendix A script (P08-S033, P08-S014, P08-S023).
- Configuration comments and documents that differ from the code (P08-S067), including a comment in another section
  that names a 60-second signal expiry.
- The expected-manager registry's stale line references and "NOT YET BUILT" header (P08-S035 to P08-S037).
- The A06 sides of the A02 handoffs as recorded in section 8, in particular the `now_time` contract that keeps the gap
  buffer's 09:15 to 09:30 window out of reach at the file's 10:00 entry start (P08-S042) and the
  `atr_fallback_mode` setting that no committed strategy file reaches (P08-S044); the effects inside the price rule are
  A09's (P08-S074).
- The receiver reads the queue settings live from its configuration object while the queue's limit and the
  processor's values are fixed at construction (P08-S008, P08-S021).

## 11. UNKNOWN / NOT ESTABLISHED

- P08-S069. UNKNOWN / NOT ESTABLISHED: the effective value of every key in this part on the legacy machines (local
  overlays and edited copies are not in the repository and were not read); whether `WEBHOOK_SECRET` was set, and how
  the process environment was populated at any start (the unit file is a declaration, P08-S005).
- P08-S070. UNKNOWN / NOT ESTABLISHED: the installed pydantic, Flask, waitress and Python versions (the repository pins
  pydantic 2.13.0, Flask 3.1.3 and waitress 3.0.2 and no Python version; P01-S085, P04-S063); P08-S006 and P08-S023
  rest on the current pydantic documentation.
- P08-S071. UNKNOWN / NOT ESTABLISHED (corrected in the check): the installed pydantic version, on which the reading
  that `getattr(config, "webhook", None)` on `AppConfig` returns `None` depends; against pydantic's published source at
  the pinned tag v2.13.0 it does (P08-S006, current external context). P01-S011 recorded the point as UNKNOWN
  because the source could not then be retrieved; it was aligned at assembly (P01 check log, section 14.5).
- P08-S072. UNKNOWN / NOT ESTABLISHED: whether `main.py` was ever started with `--config` pointing elsewhere (A02 F-11);
  whether the Appendix A script was ever run, with which options, and with what result; whether any effect census or
  composition line was produced.
- P08-S073. UNKNOWN / NOT ESTABLISHED: the size of Chartink's open-bell burst named in the per-IP comment (P08-S067).

## 12. Draft questions about intent for Rama

These ask what was intended in the legacy system; none proposes an answer. A02-03 and A02-13 already hold the ATR and
the bind questions (history OPEN) and are not repeated.

- Q-P08-01. Was `signal_processor.pipeline_timeout_sec` (30, "hard per-signal processing deadline") meant to be
  enforced by the signal processor, or was it kept as a placeholder? (P08-S012, P08-S060; A02 K-13 holds the finding.)
- Q-P08-02. Was `config/chartink_scanners.yaml` meant to be the source of the URLs the scanner check uses, or only a
  fallback behind `scan_webhook_map.yaml`'s `chartink_url`? (P08-S022, P08-S023.)
- Q-P08-03. Was `scanner_check_delay_sec` meant to apply to the operator's Appendix A script as well as to the start-up
  check? (P08-S014.)
- Q-P08-04. The comment at `config/system_config.yaml` L567 (commit `536172c`, 12-Jul-2026) speaks of "the 60s signal
  expiry", although `expiry_sec` had been 600 since 28-Apr-2026 (P04-S005): when the allocator's window was set, was a
  60-second signal life the intended basis, or was the 600-second expiry the intended value? (P08-S067.)

## 13. Where the direction's questions are answered

| Direction question (section 4) | Statements in this part | Main owner part |
|---|---|---|
| 1 sources, scanner map, URL handling | P08-S019 to P08-S023 (keys and readers only) | P01, P07 |
| 4 scanner names, strategy and symbol mapping, keys and defaults | P08-S019 to P08-S021, P08-S025, P08-S028 | P01, P04, P07 |
| 5 reachability checks | P08-S022 to P08-S024 (configuration side only) | P07 |
| 6 authentication configuration keys and defaults | P08-S010, P08-S011, P08-S030, P08-S031 | P02 |
| 7 A02-13 | P08-S065, P08-S066 (pointer) | P02 |
| 10, 11 dedup and throttle settings | P08-S010, P08-S012, P08-S017, P08-S034, P08-S057, P08-S058 | P03, P06 |
| 13 queue threshold and capacity values | P08-S007, P08-S008, P08-S017 | P03 (P03-S045 to P03-S047) |
| 16 worker settings | P08-S012, P08-S013 | P04 |
| 17 expiry setting | P08-S007, P08-S016, P08-S017 | P04 |
| 18 alias file | P08-S028 | P04 |
| 21 `main.py` wiring of settings | P08-S001, P08-S004, P08-S015, P08-S016 | P01, P04 |
| 26 configuration as an intent source | P08-S067, P08-S068, P08-S035 to P08-S037 | AUDIT |
| 27, 28 issues, matches, unknowns | sections 10 and 11; section 8, with the boundary note P08-S074 | AUDIT |
| 3 bind address and port (keys only; added in the check) | P08-S010, P08-S011 | P01 |
| 2, 8, 9, 12, 14, 15, 19, 20, 22 to 25 | not in P08 | P01 to P06 |

## 14. Check log

Checked by a separate read-only helper on 17-Nov-2026 against `970aabf` (`git show`, `git grep`, `git log`, `git blame`
only; `git show 297b587` for the registry's line references), the project records under `algocore_system` (branch
`main`) and the external pages listed in section 1.4 (re-opened). Nothing was imported, executed or run; no endpoint
was contacted; no identifier, value or machine path was copied.

**Statements checked:** 73 (P08-S001 to P08-S073), each against its cited source. Result: 50 correct as written; 23
corrected; 0 withdrawn; 1 added (P08-S074). All 98 cross-referenced statement IDs of P01 to P07 exist in the current
part files (their content was relied on as checked there; spot-checked: P01-S011, P01-S049, P01-S051, P01-S090,
P02-S060, P02-S073, P03-S045 to P03-S047, P04-S031, P04-S042, P04-S048, P05-S013, P05-S015, P05-S036, P05-S041,
P05-S044, P06-S023, P06-S024, P06-S032, P06-S052).

| ID | What changed | Why |
|---|---|---|
| Section 1.4 | the "Models" page noted as the "Latest (stable)" build with "New in v2.14" notes; pydantic's v2.13.0 source and two Python pages added | precision; the sourcing and labelling rules |
| Section 1.3 | the commands added in the check listed | method record |
| P08-S003 | count corrected: fourteen A06 fields have code defaults (eleven in the three sections plus `excluded_symbols`, `scanner_check_delay_sec`, `scanner_type`); docstring line L39 and A02 L-04 lines added | the draft's "eleven ... plus" was ambiguous and P08-S067 repeated "eleven" |
| P08-S005 | added: no module outside `scripts/` loads `.env`; HISTORICAL `requirements.txt` L14 comment | completeness |
| P08-S006 | P01-S011's open point settled against pydantic's published source at the pinned tag v2.13.0 and the Python documentation (current external context; INTERPRETATION; installed version UNKNOWN) | the sourcing and labelling rules (look it up) |
| P08-S011 | `bind_port` is read again at `main.py` L4004 (self-check URL) and L4210 (interactive banner), not "once" | source |
| P08-S014 | "the only reader" narrowed: the only code using the value is A01's check; the dashboard's configuration view names the key for display (A15) | search hit |
| P08-S017 | per-IP rows: the limiter has no constructor default (L79); its floors (L80, L81) moved to the fallback column | column misuse |
| P08-S020 | `chartink_url` also reached through A01's start-up check (`main.py` L2458 to L2459); `strategy` row: the dashboard reader L92 to L99 and the loader's S10 check added | completeness of the reader list |
| P08-S025 | the `strategies/control.py` reads cited from A02's strategy evidence file (L444 to L445), not from T-14 | wrong source |
| P08-S029 | WR4b reached only by intraday requests that get to the WR4 step with a body `scan_name` (L620 to L626) | precision |
| P08-S033 | `strategy` read by the processor only "within A06 code" | contradicted P08-S020 |
| P08-S036 | stale-line reading upgraded to FACT (`git show 297b587`: `main.py` L3058, processor L1230 = `place()`) | verifiable |
| P08-S037 | same (`main.py` L2892; receiver L498 to L503 = `finally` audit write at `297b587`) | verifiable |
| P08-S041, P08-S043, P08-S045 | handoff-row citation L1308 corrected to L1310 (L1308 is T-02's row) | wrong line |
| P08-S042 | cut back to the A06 side: the key's read site and unit (L1877, L1883), the window literals and the `now_time` contract of the two call sites; the effect inside the price rule named as A09's and not audited; "confirms" replaced by "agrees ... as far as the A06-side contract goes"; HISTORICAL launch-phase comment (`config/system_config.yaml` L28 to L39) added | boundary breach (Rama's decision A; check brief) |
| P08-S044 | cut back to the A06 side: the `atr_fallback_mode` schema, its absence from the file, its wiring and its two read sites with the ATR conditions that reach them; the `ZERO_SL`, BL-16 and HALT branch tracing removed and named as A09's logic; P05-S013 kept as a pointer | boundary breach (Rama's decision A; check brief) |
| P08-S054 | "unchanged" replaced by the stored values (L237 to L238, `bool()`) | precision |
| P08-S062 | the retest path named as after the handoff, logic not studied (P04-S042, P05-S044); reduced to the read site and unit; the not-reached reading labelled INTERPRETATION | boundary; label |
| P08-S064 | file value (L302), risk-engine lines (L180, L203), `main.py` L2901 and the resume call sites (L2142, L2478) added; the default's effect stated at the read site only; the rule named A09's | completeness; boundary |
| P08-S067 | row L348: "agrees" withdrawn (A09's logic, not compared); row `config_loader.py` L35 to L40: "fourteen"; CONFIG_GUIDE row: "above 80%" against "at or above" | boundary; count; precision |
| P08-S068 | citations completed (L389, L418, L419; the P15 "still fires ... 240" quote is K-11's, L1964); WR14's "require_hmac ... default true in production" (L419) added | wrong citation; completeness (question 26) |
| P08-S071 | narrowed to the installed pydantic version (the getattr point settled against the pinned source, P08-S006) | follows P08-S006 |
| Section 10 | the gap-buffer and ATR point reworded to the A06-side contract and setting; effects named as A09's | boundary |
| Section 13 | question 3 (keys only) added; P08-S074 added to questions 27 and 28 | completeness |

**Statements added:** P08-S074 (section 8.15): the boundary note for T-07, T-12, K-22 and K-49 under Rama's decision
A, with an OPEN QUESTION for the coordinator on who confirms A02's effect readings (A09 when studied, or A06 at the
interface level used here).

**Boundary check (Rama's decision A):** after the corrections, every A02 handoff that reaches into
`signals/signal_processor.py` after the A07 handoff (T-07, T-12, T-14, K-09, K-22, K-49) is recorded by its read site,
the contract passed and the receiving owner (A09; A07 and A18 for the resume paths), without auditing the logic. The
strategy-field map of P08-S026 is a list of read sites (A02's T-14 handoff) and is kept.

**Completeness against the brief:** item 1 (every key, setting and environment-variable name with definition, value,
reader, default, unused keys): covered by sections 2 to 6; the reader lists of the receiver (all `config` reads
listed by search) and of the throttle (none) were re-run. Item 2 (the 14 handoffs and A02-03, A02-13): all present in
section 8. Item 3 (`config/expected_managers.yaml`): section 7. Direction questions 13 and 26 are answered (P08-S007,
P08-S008, P08-S017 with P03-S045 to P03-S047; P08-S067, P08-S068, P08-S035 to P08-S037); A02's K-11 (the pre-flight's
own threshold), not in A02's handoff list to A06, is covered for question 13 by P03-S045 to P03-S047.

**Could not verify:** the content of the other parts' statements beyond the spot checks listed above (relied on as
checked there); the installed library versions (UNKNOWN; P08-S070); the A02 RECONCILED TOPIC RECORD lines of section
1.2, which no statement cites.

### Corrected at assembly
- Corrected at assembly: P08-S006 and P08-S071 the note "alignment is for the coordinator" replaced by a note that P01-S011 was aligned at assembly; why: P01-S011 and P01-S113 were corrected at assembly to the reading P08-S006 records (P01 check log, section 14.5). No fact of P08 changed. (17-Nov-2026 20:57 IST)
