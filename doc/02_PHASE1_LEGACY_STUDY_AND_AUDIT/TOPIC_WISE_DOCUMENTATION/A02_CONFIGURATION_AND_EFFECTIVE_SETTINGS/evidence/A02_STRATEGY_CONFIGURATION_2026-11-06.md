# A02 evidence: Strategy configuration: schema, loading, conformance of the strategy files, and the A07 handoff

**Status:** APPROVED — evidence for the A02 STUDY, approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31)
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06. Corrected, 2026-11-08: after the independent check of the A02 STUDY against the code (two line references). Approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31): status marked APPROVED; content unchanged.
**Purpose and scope:** This file records the strategy schema (`strategies/schema.py`), the strategy loader (`strategies/loader.py`) and the non-test callers and direct readers of the strategy files found with `git grep`, a static conformance check of the 16 strategy YAML files against the schema, the readers of `config/strategy_direction_registry.yaml` and `config/scoring_weights.yaml`, and the strategy fields read by consumers, as a handoff to A07. It supports the A02 STUDY sections on the strategy schema and loading, the conformance of the strategy files, and the A07 handoff.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

- Reading: files were read with `git show` and searched with `git grep` and `git ls-tree`. The strategy files and the other YAML files were parsed from their text with `yaml.safe_load` and with a duplicate-key-detecting `SafeLoader` subclass; the field list of `StrategyConfig` was read from the source text with `ast`. No legacy module was imported or run.
- "Local test" below means a test of synthetic inputs outside the clone, with PyYAML 6.0.3 (the version pinned at `requirements.txt` L6), pydantic 2.13.5 (pinned: 2.13.0, `requirements.txt` L7) and Python 3.13.18. The Python version in production is UNKNOWN / NOT ESTABLISHED.
- Labels: FACT, INTERPRETATION, HISTORICAL, UNKNOWN / NOT ESTABLISHED, OPEN QUESTION. A YAML value is "the file value at the baseline", never proof that it was in force.

---

## 1. Module maps

### 1.1 `strategies/schema.py` (375 lines)

| Lines | Symbol | Role (FACT unless marked) |
|---|---|---|
| L1 to L8 | module docstring | "Pydantic schema for strategy YAML files (S3-S8)"; layer 2; "Locked decisions: S1-S8" (HISTORICAL) |
| L10 to L20 | imports | `datetime.time`, `Path`, `List`, `yaml`, pydantic `BaseModel`, `ConfigDict`, `field_validator`, `model_validator`, `ValidationError`; `core.exceptions.ConfigSchemaError` |
| L24 | `_VALID_DIRECTIONS` | {LONG, SHORT} |
| L25 | `_VALID_INTENTS` | {INTRADAY, DELIVERY} |
| L26 | `_VALID_PROTOCOLS` | {CO_PLUS_TGT, LIMIT_TRIPLE} |
| L27 to L31 | comment | taxonomy is "metadata + display only; NO routing/execution" (INTERPRETATION of intent; HISTORICAL comment) |
| L32 | `_VALID_PIPELINES` | {INTRADAY, DELIVERY} |
| L33 | `_VALID_HORIZONS` | {SAME_DAY, NEXT_DAY, BTST, SWING} |
| L34 | `_VALID_ENTRY_METHODS` | {MARKET, LIMIT} |
| L35 | `_VALID_SL_METHODS` | {FIXED_PCT, ATR} |
| L36 | `_VALID_TGT_METHODS` | {FIXED_PCT, RISK_REWARD, ATR} |
| L37 | `_VALID_DAYS` | {MON, TUE, WED, THU, FRI} |
| L42 to L345 | `class StrategyConfig(BaseModel)` | the strategy schema |
| L50 | `model_config = ConfigDict(extra="forbid")` | unknown keys rejected; nothing else configured (no `frozen`, no `validate_assignment`, no `strict`) |
| L53 to L139 | 41 annotated fields | see section 2 |
| L143 to L150 | `_val_direction` | field validator, `direction` |
| L152 to L159 | `_val_intent` | `intent` |
| L161 to L168 | `_val_order_protocol` | `order_protocol` |
| L170 to L177 | `_val_pipeline` | `pipeline` |
| L179 to L186 | `_val_horizon` | `horizon` |
| L188 to L195 | `_val_entry_method` | `entry_method` |
| L197 to L204 | `_val_sl_method` | `sl_method` |
| L206 to L213 | `_val_tgt_method` | `tgt_method` |
| L215 to L220 | `_val_sl_bounds` | `sl_min_pct`, `sl_max_pct` |
| L222 to L227 | `_val_atr_multipliers` | `sl_atr_multiplier`, `tgt_atr_multiplier` |
| L229 to L234 | `_val_tgt_risk_reward` | `tgt_risk_reward` |
| L236 to L242 | `_val_trail_pcts` | `smart_tgt_trail_trigger_pct`, `smart_tgt_trail_step_pct`, `pullback_wait_tolerance_pct` |
| L244 to L249 | `_val_entry_offset` | `entry_offset_pct` |
| L251 to L256 | `_val_threshold_pcts` | `min_adr_pct`, `max_spread_pct` |
| L258 to L263 | `_val_min_score` | `min_score` |
| L265 to L270 | `_val_min_volume_surge` | `min_volume_surge` |
| L272 to L277 | `_val_pullback_timeout` | `pullback_wait_timeout_sec` |
| L279 to L284 | `_val_lot_size` | `lot_size` |
| L286 to L296 | `_val_active_days` | `active_days` |
| L300 to L345 | `_val_cross_fields` | `model_validator(mode="after")`, cross-field rules (section 2.3) |
| L350 to L375 | `validate_strategy(yaml_path) -> StrategyConfig` | reads, parses and validates ONE file; the only file reader in this module (section 3.1) |

### 1.2 `strategies/loader.py` (213 lines)

| Lines | Symbol | Role (FACT unless marked) |
|---|---|---|
| L1 to L8 | module docstring | "Strategy YAML loader (S9-S11)" (HISTORICAL) |
| L10 to L20 | imports | `logging`, `Path`, typing, `yaml`, pydantic `ValidationError`, `ConfigMissingError`, `ConfigSchemaError`, `StrategyConfig`, `validate_strategy` |
| L22 | `_log = logging.getLogger("strategies.loader")` | module logger |
| L25 to L37 | comment block | HISTORICAL (18-Jul-2026): why `scan_strategy_errors` exists (missing-`direction` alert) |
| L39 to L67 | `_describe_config_error(exc)` | renders one failure as text; uses pydantic `.errors()` from `exc.__cause__` when it is a `ValidationError` (`missing` → "missing required field", `extra_forbidden` → "unknown field … not permitted", others → "loc: msg" with the "Value error, " prefix removed); else `str(exc)` |
| L70 to L88 | `scan_strategy_errors(strategies_dir)` | validates every `*.yaml`, collects `(filename, reason)` for each failure, never raises |
| L91 to L213 | `class StrategyLoader` | load-once loader with lookup |
| L97 to L98 | `__init__` | `self._strategies = {}` |
| L102 to L156 | `load_all_strategies(strategies_dir, scan_webhook_map_path=None, force_intraday_only=False)` | fail-fast load of all files; returns `{name: StrategyConfig}` (section 3.2) |
| L158 to L165 | `get_strategy(name)` | lookup; `ConfigMissingError` if absent. FACT (git grep): no non-test caller |
| L169 to L213 | `_validate_scan_webhook_map(map_path, strategies)` | S10 cross-check: every `scanners[*].strategy` must be a loaded name (section 3.3) |

Package export: `strategies/__init__.py` L3 to L6 re-exports `StrategyConfig`, `validate_strategy`, `StrategyLoader` (not `scan_strategy_errors`). Owner of `__init__.py`: A07 (provisional, index S1).

---

## 2. The strategy schema (`StrategyConfig`)

### 2.1 Fields (41; FACT from the source, extracted with `ast`)

"Required" = no default, so a missing key fails validation. "Type only" = no value constraint beyond the pydantic type.

| # | Field | Line | Type | Required / default | Constraint actually enforced (lines) |
|---|---|---|---|---|---|
| 1 | `name` | L53 | str | required | type only |
| 2 | `display_name` | L54 | str | required | type only |
| 3 | `description` | L55 | str | required | type only |
| 4 | `direction` | L58 | str | required | in {LONG, SHORT} (L143 to L150) |
| 5 | `intent` | L59 | str | required | in {INTRADAY, DELIVERY} (L152 to L159) |
| 6 | `order_protocol` | L60 | str | required | in {CO_PLUS_TGT, LIMIT_TRIPLE} (L161 to L168) |
| 7 | `pipeline` | L69 | str | required | in {INTRADAY, DELIVERY} (L170 to L177) |
| 8 | `horizon` | L70 | str | required | in {SAME_DAY, NEXT_DAY, BTST, SWING} (L179 to L186) |
| 9 | `enabled` | L78 | bool | default `True` | type only |
| 10 | `entry_method` | L81 | str | required | in {MARKET, LIMIT} (L188 to L195) |
| 11 | `entry_offset_pct` | L82 | float | `0.0` | 0 <= v < 1 (L244 to L249) |
| 12 | `sl_method` | L85 | str | required | in {FIXED_PCT, ATR} (L197 to L204) |
| 13 | `sl_pct` | L86 | float | `0.0` | no field validator; only when `sl_method=FIXED_PCT`: > 0 and `sl_min_pct` <= v <= `sl_max_pct` (L303 to L312) |
| 14 | `sl_atr_multiplier` | L87 | float | `1.5` | > 0 (L222 to L227) |
| 15 | `sl_min_pct` | L88 | float | `0.003` | 0 < v < 1 (L215 to L220); <= `sl_max_pct` (L315 to L319) |
| 16 | `sl_max_pct` | L89 | float | `0.05` | 0 < v < 1 (L215 to L220) |
| 17 | `sl_gap_buffer_pct` | L90 | float | `0.0` | type only |
| 18 | `tgt_method` | L93 | str | required | in {FIXED_PCT, RISK_REWARD, ATR} (L206 to L213) |
| 19 | `tgt_pct` | L94 | float | `0.0` | only when `tgt_method=FIXED_PCT`: > 0 (L322 to L326); no upper bound |
| 20 | `tgt_risk_reward` | L95 | float | `2.0` | > 0 (L229 to L234) |
| 21 | `tgt_atr_multiplier` | L96 | float | `2.5` | > 0 (L222 to L227) |
| 22 | `smart_tgt_enabled` | L99 | bool | required | type only |
| 23 | `smart_tgt_trail_trigger_pct` | L100 | float | `0.005` | 0 < v < 1 (L236 to L242) |
| 24 | `smart_tgt_trail_step_pct` | L101 | float | `0.003` | 0 < v < 1 (L236 to L242) |
| 25 | `trailing_sl_enabled` | L105 | bool | `False` | type only |
| 26 | `trailing_sl_breakeven_trigger_pct` | L106 | float | `60.0` | type only |
| 27 | `trailing_sl_partial_lock_trigger_pct` | L107 | float | `80.0` | type only |
| 28 | `trailing_sl_partial_lock_sl_pct` | L108 | float | `40.0` | type only |
| 29 | `pullback_wait_enabled` | L111 | bool | required | type only |
| 30 | `pullback_wait_tolerance_pct` | L112 | float | `0.005` | 0 < v < 1 (L236 to L242) |
| 31 | `pullback_wait_timeout_sec` | L113 | int | `180` | >= 1 (L272 to L277) |
| 32 | `min_score` | L116 | int | `0` | >= 0 (L258 to L263); comment L116 "0 = use global from scoring_weights.yaml" |
| 33 | `min_volume_surge` | L117 | float | `1.3` | > 0 (L265 to L270) |
| 34 | `min_adr_pct` | L118 | float | `0.005` | >= 0 (L251 to L256) |
| 35 | `max_spread_pct` | L119 | float | `0.005` | >= 0 (L251 to L256) |
| 36 | `lot_size` | L126 | int | `1` | >= 1 (L279 to L284) |
| 37 | `max_concurrent_positions` | L127 | int | `2` | type only (0 or negative not rejected) |
| 38 | `v3_playbook` | L134 | bool | `False` | type only |
| 39 | `entry_start_time` | L137 | str | `"10:00"` | cross-field only (L329 to L343) |
| 40 | `entry_end_time` | L138 | str | `"15:00"` | cross-field only (L329 to L343) |
| 41 | `active_days` | L139 | List[str] | `["MON","TUE","WED","THU","FRI"]` | non-empty and a subset of MON to FRI (L286 to L296) |

Totals (FACT): 41 fields; 13 required (`name`, `display_name`, `description`, `direction`, `intent`, `order_protocol`, `pipeline`, `horizon`, `entry_method`, `sl_method`, `tgt_method`, `smart_tgt_enabled`, `pullback_wait_enabled`); 28 with defaults; 13 fields are "type only" (rows 1 to 3, 9, 17, 22, 25 to 29, 37, 38); 2 more are checked only conditionally (`sl_pct`, `tgt_pct`).

HISTORICAL comments in the class: L122 to L125 say per-strategy `max_risk_pct` was deleted (BUILD 1, 24-Jun) and removed from all YAMLs; L129 to L133 say `v3_playbook` default False keeps "the 15 existing strategies" unchanged; L72 to L77 say `enabled` defaults True so adding the field changed nothing.

### 2.2 Type handling (INTERPRETATION of pydantic v2 lax mode; confirmed by local test on a synthetic model)

| Input | Result |
|---|---|
| int or `None` into a `str` field | rejected (`string_type`) |
| `2.5` into an `int` field | rejected (`int_from_float`); `2.0` and `"3"` accepted |
| `"yes"`, `"off"` into a `bool` field | accepted as True / False |
| `True` into a `float` field | accepted as 1.0 |
| unknown key | rejected (`extra_forbidden`) because of `extra="forbid"` (L50) |
| YAML 1.1 unquoted time `10:00` | PyYAML gives int 600 (sexagesimal) → would be rejected by the `str` type; unquoted `09:25` gives the string "09:25" (local test). All 16 files quote their times (section 5). |

Field validators are the default "after" kind, so they run on the coerced value. Defaults are not re-validated (pydantic default `validate_default=False`); every default satisfies its own rule, so this has no effect at the baseline (INTERPRETATION). The model is not frozen (L50), so loaded objects can be modified after load (INTERPRETATION); FACT (git grep): no non-test code assigns to a strategy config attribute.

### 2.3 Cross-field rules (`_val_cross_fields`, L300 to L345)

| # | Rule | Lines |
|---|---|---|
| X1 | if `sl_method == "FIXED_PCT"`: `sl_pct > 0` | L303 to L307 |
| X2 | if `sl_method == "FIXED_PCT"`: `sl_min_pct <= sl_pct <= sl_max_pct` | L308 to L312 |
| X3 | always `sl_min_pct <= sl_max_pct` | L315 to L319 |
| X4 | if `tgt_method == "FIXED_PCT"`: `tgt_pct > 0` | L322 to L326 |
| X5 | both times split on ":" into exactly two ints and form a valid `datetime.time`; otherwise "Invalid entry_start_time or entry_end_time format; expected HH:MM" (catches `ValueError`, `AttributeError`) | L329 to L337 |
| X6 | `entry_start_time < entry_end_time` | L339 to L343 |

INTERPRETATION of X5: "9:5" is accepted (H:M with one digit), "10:00:00" and "24:00" are rejected; the format is not strictly HH:MM.

No cross-field rule exists (FACT, by absence in L300 to L345) for: `sl_method=ATR` or `tgt_method=ATR/RISK_REWARD` (no extra requirement), `intent` vs `order_protocol`, `intent` vs `pipeline`, `pipeline` vs `horizon`, `direction` vs the `_long`/`_short` name suffix, `name` vs the file name, `entry_method=MARKET` vs `entry_offset_pct`, `trailing_sl_*` vs `order_protocol`, `smart_tgt_*` vs `order_protocol`, `v3_playbook` vs `enabled`, or the per-strategy window vs the global trading hours.

### 2.4 Unknown-key policy

FACT: `extra="forbid"` (L50). Any key not in the 41 fields makes validation fail; `validate_strategy` turns that into `ConfigSchemaError` (L372 to L375) and `_describe_config_error` names it "unknown field … not permitted" (loader L57 to L58).

### 2.5 Differences by strategy type

FACT: the schema has no type-specific branch. The only conditional rules key on `sl_method` and `tgt_method` (X1, X2, X4). `direction`, `intent`, `order_protocol`, `pipeline`, `horizon` are independent enums; long/short, intraday/delivery, positional and V3-playbook strategies all use the same 41 fields and the same rules. HISTORICAL: L62 to L68 say `pipeline`/`horizon` are "Deliberately INERT — no routing, execution, capital-split, or config change" and "pipeline is INDEPENDENT of intent". The differences that exist are file values (section 5).

---

## 3. Loading

### 3.1 `validate_strategy(yaml_path)` (schema.py L350 to L375)

| Step | Behaviour | Lines | Label |
|---|---|---|---|
| open | `open(yaml_path, "r", encoding="utf-8")` | L353 | FACT |
| parse | `yaml.safe_load(fh)` | L354 | FACT |
| file missing | `FileNotFoundError` → `ConfigSchemaError("Strategy YAML not found: …")` (not `ConfigMissingError`; raised without `from`) | L355 to L358 | FACT |
| YAML syntax | `yaml.YAMLError` → `ConfigSchemaError("Invalid YAML syntax in …")` (without `from`) | L359 to L362 | FACT |
| not a mapping (incl. empty file → `None`) | `ConfigSchemaError("Strategy YAML must be a mapping, got …")` | L364 to L368 | FACT; empty → None is local test |
| validate | `StrategyConfig(**raw)` | L371 | FACT |
| schema failure | `ValidationError` → `ConfigSchemaError(...) from exc` (the only branch that sets `__cause__`) | L372 to L375 | FACT |
| non-UTF-8 bytes | Python's decoder raises `UnicodeDecodeError` (a `ValueError`) from inside `safe_load`; it is not caught by L355 or L359, so it escapes raw, not as `ConfigSchemaError` | L353 to L362 | INTERPRETATION (local test) |
| UTF-8 BOM | tolerated: PyYAML skips a leading BOM | — | INTERPRETATION (local test) |
| other `OSError` (directory named `*.yaml`, permission) | `IsADirectoryError` / `PermissionError` escape raw (only `FileNotFoundError` is caught) | L355 | INTERPRETATION (local test) |
| non-string top-level key (e.g. a key YAML reads as bool or int) | `StrategyConfig(**raw)` raises `TypeError: keywords must be strings`, not caught (only `ValidationError` is) | L370 to L375 | INTERPRETATION (local test of `dict(**{True: 1})`) |
| duplicate keys | PyYAML `safe_load` keeps the last value silently | L354 | INTERPRETATION (local test); none of the 16 files has one (section 5) |

### 3.2 `StrategyLoader.load_all_strategies` (loader.py L102 to L156)

| Aspect | Behaviour | Lines | Label |
|---|---|---|---|
| discovery | `sorted(strategies_dir.glob("*.yaml"))`: one flat directory, not recursive, suffix `.yaml` only | L128 | FACT |
| file selection edge cases | `.yml` and `.YAML` ignored; `pathlib` also matches dot-files and directories whose name ends `.yaml` (shown on Python 3.13; other versions not tested); case-sensitive on Linux | L128 | INTERPRETATION (local test; production Python version UNKNOWN) |
| ordering | sorted `Path` order (string order of the path) | L128 | FACT / INTERPRETATION of `Path` ordering |
| no files / missing directory | `ConfigSchemaError("No strategy YAML files found in …")`; a missing directory globs to nothing, so it gives the same error | L129 to L132 | FACT; missing-dir globbing is local test |
| per-file | `validate_strategy(yaml_path)`; no try, so the first failure propagates and nothing is returned ("no partial loads", docstring L111) | L134 to L136 | FACT |
| state on failure | `self._strategies` is assigned only at L155, so a failed load leaves the previous (initially empty) dict | L155 | INTERPRETATION |
| `force_intraday_only` | when true and `cfg.intent != "INTRADAY"`: one INFO log ("keeps declared intent … DORMANT at the entry gate"); the object is not changed | L142 to L148 | FACT |
| HISTORICAL | docstring L114 to L124: the old "Bug-D" rewrite DELIVERY → INTRADAY at load was removed (Option A, 10-Jul-2026); the parameter is kept for callers and the log | L114 to L124, L137 to L141 | HISTORICAL |
| enabled / disabled | not consulted: disabled strategies are loaded and returned (`pb01_breakout_retest`, `enabled: false`, is in the dict). Gating is in `strategies/control.py` L76 to L82 (A07) | L134 to L149 | FACT |
| defaults | applied by pydantic for absent keys (section 2.1) | — | FACT |
| key | `strategies[cfg.name] = cfg`: keyed by the `name` field, not the file name; a second file with the same `name` silently replaces the first (sort order decides) | L149 | FACT (code); INTERPRETATION (effect) |
| S10 | `_validate_scan_webhook_map` only when `scan_webhook_map_path is not None` | L152 to L153 | FACT |
| caching | per instance only (`self._strategies`, L155); no module cache; "loaded ONCE; no hot reload" (class docstring L94). Each caller builds a new `StrategyLoader` and re-reads the files | L94, L98, L155 | FACT |
| return | the same dict object that is stored on the instance (L155 to L156), values are mutable `StrategyConfig` | L155 to L156 | FACT / INTERPRETATION |
| error type | `ConfigSchemaError` for schema/YAML/missing-file/no-files; raw `UnicodeDecodeError`, `OSError`, `TypeError` for the cases in 3.1; `ConfigMissingError`/`ConfigSchemaError` from S10 | — | FACT / INTERPRETATION |

### 3.3 `_validate_scan_webhook_map` (loader.py L169 to L213)

| Step | Behaviour | Lines |
|---|---|---|
| open | `encoding="utf-8"`, `yaml.safe_load` | L176 to L177 |
| missing file | `ConfigMissingError` | L178 to L181 |
| YAML error | `ConfigSchemaError` | L182 to L185 |
| root not a dict | returns silently (no error) | L187 to L188 |
| `scanners` not a dict | returns silently | L190 to L192 |
| entry | dict → `entry.get("strategy")`; otherwise the entry itself is the strategy name (old format) | L194 to L200 |
| no strategy | `ConfigSchemaError` | L202 to L206 |
| unknown strategy | `ConfigMissingError` | L208 to L213 |
| direction | forward only (map → YAML); a YAML with no scanner is not reported | L194 to L213 |

FACT (git grep `scan_webhook_map_path`): only `tests/unit/test_pb01_registration.py` L34 and `tests/unit/test_strategies.py` L364, L392 pass it; no production caller does. HISTORICAL: `docs/audit/audit_05jul2026.md` L446 and `docs/audit/integrity_audit_2026.md` L62 already describe S10 as unwired. Static simulation at the baseline (file values only): `config/scan_webhook_map.yaml` has 16 scanners: 15 entries have the keys `chartink_url` and `strategy`, and 1 entry (`pb01_breakout_retest`) also has `scanner_type` (URL values not reproduced); every referenced strategy has a YAML and every YAML is referenced by exactly one scanner, so S10 would pass on the files.

### 3.4 `scan_strategy_errors` (loader.py L70 to L88)

FACT: same glob and sort as the loader (L83); calls `validate_strategy` per file (L85); `except Exception` (L86) turns any failure into `(yaml_path.name, _describe_config_error(exc))` (L87); returns the list (L88). INTERPRETATION: a missing or empty directory returns `[]` (glob yields nothing), so the "No strategy YAML files found" failure produces no entry; non-schema failures (non-UTF-8, bad syntax, missing file) give `str(exc)` because only the schema branch sets `__cause__` (schema.py L375; loader L48 to L49).

### 3.5 What a non-UTF-8 strategy file does at each reader (INTERPRETATION from the code plus the local library test)

| Reader | Lines | Outcome |
|---|---|---|
| `validate_strategy` | schema.py L353 to L362 | raw `UnicodeDecodeError` |
| `load_all_strategies` | loader.py L136 | propagates; nothing loaded |
| `check_strategy_configs` | utils/startup_checks.py L1288 to L1291 | caught (`Exception`) → records the blocking `invalid_strategy_configs` in the runner's list (L1616 to L1618); the boot never reaches the point where that list is acted on (below) |
| `check_temp_config_values` | utils/startup_checks.py L1477 to L1487 (called at L1644) | reads every `config/strategies/*.yaml` with `read_text(encoding="utf-8")` (L1481) and catches only `OSError` (L1486), so the `UnicodeDecodeError` propagates out of the function and out of `run_all_startup_checks`, which has no try and calls it after `check_strategy_configs` (L1616) |
| `scan_strategy_errors` | loader.py L86 to L87 | caught → reason is the codec message (when called; at boot it is not reached for this case, below) |
| `main.py` load | L3159 to L3162 | would propagate; not reached, because the boot has already ended at L2451 (below) |
| `build_direction_map`, `build_taxonomy_map` | core/strategy_direction.py L67 to L68; strategies/taxonomy.py L36 to L37 | file skipped silently |
| `strategy_status.build_status_rows` | scripts/strategy_status.py L66 to L74 | "config error" row |
| dashboard `get_strategies` | ops_dashboard/backend/readers/config_reader.py L61 to L65 | catches only `OSError`, `yaml.YAMLError` → the error escapes `get_strategies` |
| `daily_report._build_strategy_min_scores`, `system_manager._enabled_strategy_names` | reports/daily_report.py L324 to L333; scripts/system_manager.py L510 to L514 | file skipped silently |

Boot outcome for a non-UTF-8 strategy file (INTERPRETATION from the code path; the same reading as A01 AUDIT S-39, which records this case as a KNOWN DEFECT sub-case). `run_all_startup_checks` is called at `main.py` L2451 without a try. The `UnicodeDecodeError` from step 14, `check_temp_config_values` (`utils/startup_checks.py` L1644), leaves the runner and `_main_locked`, and the guard gives exit 2, "unexpected_error" (`main.py` L4291 to L4293). No report is returned, so the blocking `invalid_strategy_configs` recorded by step 10 is never acted on: the abort path at L2484 to L2502 (the `scan_strategy_errors` alert and `return 3`) is not reached, and there is no alert and no exit 3. `load_all` does not read the strategy files, so nothing stops such a file earlier (A01 AUDIT S-39).

---

## 4. Callers (git grep, non-test; `tests/` and `ops_dashboard/tests/` excluded)

### 4.1 Through `StrategyLoader.load_all_strategies`

| # | Caller | Lines | Arguments passed | Use of result / errors | Owner |
|---|---|---|---|---|---|
| C1 | `utils/startup_checks.py` `check_strategy_configs` | L1266 to L1293 (load L1283 to L1284) | `strategies_dir` only: no `force_intraday_only` (default False), no `scan_webhook_map_path` | checks the directory exists first (L1276 to L1280: CRITICAL log, error string, return); result discarded; INFO "OK" on success; `except Exception` → CRITICAL log + error string (L1288 to L1291); returns the list. L1272 imports `StrategyConfig`, which the function never uses. Called by `run_all_startup_checks` L1615 to L1618 → blocking failure `invalid_strategy_configs` | A01 |
| C2 | `main.py` boot | L3157 to L3162 | `strategies_dir`, `force_intraday_only=app_config.system.force_intraday_only`; no `scan_webhook_map_path` | the live strategy set; no try around it (A01 S-30). Used at: L3164 to L3187 (boot summary via `strategy_will_trade`), L3216 to L3228 (slippage-override typo check, `set(strategies.keys())` L3224), L3437 to L3439 and L3459 to L3461 (`audit_config(..., strategies=strategies, groups="A")`, codes A4 and A5), L3584 (`SignalProcessor(strategies=strategies)`), L4148 to L4150 (`strategy_intent_fn` → `.intent`) | A01 (call site); consumers A06, A07, A09, A12 |
| C3 | `ops/control_tower/aggregator.py` `read_config` | L141 to L167 (load L154 to L158) | dir + `force_intraday_only=app.system.force_intraday_only` | passed to `audit_app_config` L161; any exception → `strategies = None` silently (L159 to L160) | A15 |
| C4 | `scripts/preflight/checks/config_sanity.py` `_build_report` | L22 to L49 (load L35 to L42) | dir + `force_intraday_only=app_config.system.force_intraday_only` | passed to `audit_app_config`; exception → `None` (L41 to L42); memoised in `ctx.extra` (L48) | A20 |
| C5 | `scripts/preflight/checks/config_integrity.py` `StrategyConfigsValidCheck.run` | L146 to L158 (load L154 to L155) | dir only | exception → CRITICAL fail "strategy config invalid"; pass "all N strategy configs valid" | A20 |
| C6 | same file `LongStrategiesEnabledCheck.run` | L161 to L182 (load L172 to L173) | dir only | reads `.direction`; WARN if any LONG; exception → WARN | A20 |
| C7 | `scripts/replay_signals.py` `run_replay` | L187 to L188 | dir only | offline replay | A19 |

On the A01 observation (C1 vs C2): FACT: at the baseline `force_intraday_only` changes only the INFO log at loader L142 to L148, so C1 and C2 return equal content from the same files. They read the files at two different moments (C1 inside `run_all_startup_checks`, called at main.py L2451; C2 at L3159). File value at the baseline: `config/system_config.yaml` L142 `force_intraday_only: false`, so with file values the log would not fire (UNKNOWN / NOT ESTABLISHED what was in force).

### 4.2 Through `scan_strategy_errors`

| Caller | Lines | Behaviour | Owner |
|---|---|---|---|
| `main.py` abort path | L2484 to L2502 (call L2496) | only when `report.ok` is false AND `"invalid_strategy_configs"` is in `report.blocking_failures`; non-empty list → `_alert_invalid_strategy_configs` (defined L288) at L2497 to L2498; any exception logged (L2499 to L2500); then `store.close()` and `return 3` (L2501 to L2502). The `--dry-run` branch (L2476 to L2482) returns before this, with no alert | A01 (path); A14 (alert) |

INTERPRETATION: a missing or empty strategies directory makes C1 fail but `scan_strategy_errors` returns `[]`, so `_alert_invalid_strategy_configs` is not called for those two cases (L2497). For a non-UTF-8 strategy file this path is not reached at all: the boot ends at L2451 with exit 2 (section 3.5; A01 AUDIT S-39).

### 4.3 Through `validate_strategy` directly (each file validated on its own)

| Caller | Lines | What it reads | Failure handling | Owner |
|---|---|---|---|---|
| `core/strategy_direction.py` `build_direction_map` | L52 to L71 | `cfg.name`, `cfg.direction` | skip file (L67 to L68) | A07 |
| `core/strategy_direction.py` `canonical_direction` | L74 to L79 | rebuilds the whole map on every call | as above | A07 |
| ↳ `orders/eod_squareoff.py` | L695 to L696 | `build_direction_map("config")` (relative path) | exception → `{}` (L697 to L699) | A12 |
| ↳ `scripts/strategy_registry_officer.py` `run` | L230 | `build_direction_map(config_dir)` | — | A07 |
| `strategies/taxonomy.py` `build_taxonomy_map` | L23 to L38 | `cfg.name`, `cfg.pipeline`, `cfg.horizon` | skip file (L36 to L37) | A07 |
| ↳ `reports/daily_report.py` | L1518 to L1519 | `build_taxonomy_map(config_dir)` | — | A15 |
| `scripts/strategy_status.py` `build_status_rows` | L56 to L109 (validate L67) | `name`, `intent`, `enabled`, `entry_start_time`, `entry_end_time`, `sl_pct`, `tgt_risk_reward`, `direction`, `pipeline`, `horizon`, `v3_playbook` (skips V3 playbooks, L81 to L82) | "config error" row keyed by `path.stem` (L68 to L74) | A07 |

### 4.4 Direct raw readers that bypass the schema (`yaml.safe_load` of the strategy files, or their raw text)

| Reader | Lines | Keys read (own defaults) | Failure handling | Owner |
|---|---|---|---|---|
| `reports/daily_report.py` `_build_strategy_min_scores` | L313 to L334 | `name`, `min_score` (default 0; `>0` else the global from `scoring_weights.yaml`) | `except Exception: pass` | A15 |
| `scripts/system_manager.py` `_enabled_strategy_names` | L502 to L519 | `enabled` (default True), `name` | skip file | A15 |
| `ops_dashboard/backend/readers/config_reader.py` `get_strategies` | L56 to L89 | `name` (else file stem), `display_name`, `enabled` (default True), `direction`, `intent`, `order_protocol`, `max_concurrent_positions` (default 2), `entry_start_time`, `entry_end_time`, `tgt_risk_reward` (no default) | skips on `OSError`/`yaml.YAMLError` only | A15 (used by `api/trading.py` L247, `services/config_view.py` L134, `services/controls.py` L221, `services/operations.py` L33, `services/strategy_meta.py` L72, `services/strategy_tower.py` L95) |
| `utils/startup_checks.py` `check_temp_config_values` | L1465 to L1501 (glob L1477, read L1481) | no keys: reads the raw text of every `config/strategies/*.yaml` (and of every top-level `config/*.yaml`) and counts "# TEMP" markers (L1482); no YAML parse, no schema | `OSError` → skip file (L1486 to L1487); any other error, for example `UnicodeDecodeError`, propagates (section 3.5); markers give a warning only (L1644 to L1646) | A01 |

### 4.5 Other

| Item | Lines | Note | Owner |
|---|---|---|---|
| `core/config_auditor.py` | A4 L222 to L238; A5 L266 to L297; A3 L304 to L319; G5 L745 to L760 | receives the loaded dict from C2, C3, C4; reads `enabled`, `trailing_sl_enabled`, `entry_start_time`, `entry_end_time`, and `intent`/`enabled` via `strategy_will_trade` | A02 |
| `core/config_loader.py` | `_CONFIG_FILES` L2441 to L2450 | the central loader covers 8 files; `config/strategies/*.yaml` is not among them, so the strategy files are not in `AppConfig.file_hashes` (L2491) | A02 |
| `core/config_snapshotter.py` | — | FACT (git grep): no "strateg" string in the file; HISTORICAL: `reports/daily_trade_review.py` L1156 and L1300 say per-strategy config is not snapshotted | A02 / A15 |
| `utils/startup_checks.py` `_REQUIRED_CONFIG_FILES_STATIC` | L833 to L843 | lists no strategy file; the directory is checked only in C1 | A01 |

---

## 5. Conformance of the 16 strategy YAML files (static; file values at the baseline)

`git ls-tree` of `config/strategies/`: exactly 16 entries, all `.yaml`. Each was parsed from its text with `yaml.safe_load` and compared with the schema as read (section 2), not by importing it.

### 5.1 Structure and conformance

Abbreviations for schema keys absent from a file (pydantic default then applies): **T4** = `trailing_sl_enabled`, `trailing_sl_breakeven_trigger_pct`, `trailing_sl_partial_lock_trigger_pct`, `trailing_sl_partial_lock_sl_pct`; **V** = `v3_playbook`; **G** = `sl_gap_buffer_pct`.

| File | Keys | Unknown keys | Missing required | Absent schema keys | Violations | enabled | direction | intent / pipeline / horizon | order_protocol | pullback_wait | smart_tgt | Window |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| first_pullback_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |
| first_pullback_short | 35 | 0 | 0 | T4, V, G | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |
| gap_fade_long | 36 | 0 | 0 | T4, V | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| gap_fade_short | 36 | 0 | 0 | T4, V | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| gap_go_long | 36 | 0 | 0 | T4, V | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| gap_go_short | 36 | 0 | 0 | T4, V | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| open_high_breakdown_short | 35 | 0 | 0 | T4, V, G | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |
| open_low_breakout_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |
| pb01_breakout_retest | 36 | 0 | 0 | T4, G | 0 | **false** | LONG | INTRADAY / INTRADAY / NEXT_DAY | CO_PLUS_TGT | false | true | 09:25-11:00 |
| positional_momentum_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | DELIVERY / DELIVERY / SWING | LIMIT_TRIPLE | false | false | 09:25-15:00 |
| positional_sector_rotation | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | DELIVERY / DELIVERY / SWING | LIMIT_TRIPLE | false | false | 09:25-15:00 |
| positional_swing_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | DELIVERY / DELIVERY / SWING | LIMIT_TRIPLE | false | false | 09:25-15:00 |
| range_breakout_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| range_breakout_short | 35 | 0 | 0 | T4, V, G | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | false | true | 09:25-15:00 |
| vwap_bounce_long | 35 | 0 | 0 | T4, V, G | 0 | true | LONG | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |
| vwap_rejection_short | 35 | 0 | 0 | T4, V, G | 0 | true | SHORT | INTRADAY / INTRADAY / SAME_DAY | CO_PLUS_TGT | true | true | 09:25-15:00 |

Common to all 16 (FACT): `entry_method: LIMIT`, `sl_method: FIXED_PCT`, `tgt_method: RISK_REWARD`, `tgt_pct: 0.0`, `min_score: 0`, `lot_size: 1`, `active_days` MON to FRI; both times are quoted strings; every file is valid UTF-8, has no BOM, uses LF line ends, is a mapping, has no duplicate key; `name` equals the file stem; the 16 names are unique. Non-ASCII characters: only `pb01_breakout_retest.yaml` (3, all in comments: L2, L4, L70).

### 5.2 Numeric file values

| File | sl_pct | sl_min / sl_max | sl_atr_mult | sl_gap_buffer | tgt_rr | tgt_atr_mult | entry_offset | min_vol_surge | max_conc_pos |
|---|---|---|---|---|---|---|---|---|---|
| first_pullback_long | 0.015 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.3 | 2 |
| first_pullback_short | 0.015 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.3 | 2 |
| gap_fade_long | 0.01 | 0.003 / 0.05 | 1.5 | 0.3 | 1.5 | 2.5 | 0.001 | 1.3 | 3 |
| gap_fade_short | 0.01 | 0.003 / 0.05 | 1.5 | 0.3 | 1.5 | 2.5 | 0.001 | 1.3 | 3 |
| gap_go_long | 0.012 | 0.003 / 0.05 | 1.5 | 0.3 | 1.5 | 2.5 | 0.001 | 2.0 | 3 |
| gap_go_short | 0.012 | 0.003 / 0.05 | 1.5 | 0.3 | 1.5 | 2.5 | 0.001 | 2.0 | 3 |
| open_high_breakdown_short | 0.01 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.3 | 2 |
| open_low_breakout_long | 0.01 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.3 | 2 |
| pb01_breakout_retest | 0.01 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.3 | 2 |
| positional_momentum_long | 0.02 | 0.005 / 0.08 | 2.0 | (absent) | 1.5 | 3.0 | 0.002 | 1.5 | 2 |
| positional_sector_rotation | 0.02 | 0.005 / 0.08 | 2.0 | (absent) | 1.5 | 3.0 | 0.002 | 1.3 | 2 |
| positional_swing_long | 0.02 | 0.005 / 0.08 | 2.0 | (absent) | 1.5 | 3.0 | 0.002 | 1.2 | 2 |
| range_breakout_long | 0.01 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.8 | 2 |
| range_breakout_short | 0.01 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.8 | 2 |
| vwap_bounce_long | 0.008 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.5 | 2 |
| vwap_rejection_short | 0.008 | 0.003 / 0.05 | 1.5 | (absent) | 1.5 | 2.5 | 0.001 | 1.5 | 2 |

The six LONG/SHORT pairs (first_pullback, gap_fade, gap_go, open_low/open_high, range_breakout, vwap_bounce/vwap_rejection) are identical apart from `name`, `display_name`, `description`, `direction` (FACT, own comparison). The four `sl_gap_buffer_pct: 0.3` lines carry the comment "widen SL 0.3% during 09:15-09:30 gap-risk window" (e.g. `gap_go_long.yaml` L26). The three positional files carry `sl_method: "FIXED_PCT"    # ATR not yet implemented; using FIXED_PCT until ATR data available` (e.g. `positional_swing_long.yaml` L21).

### 5.3 Totals

| Measure | Count |
|---|---|
| Files | 16 |
| Parse / encoding problems | 0 |
| Unknown keys | 0 |
| Missing required keys | 0 |
| Constraint violations (field and cross-field rules) | 0 (all 16 would pass the schema as read) |
| Top-level keys per file | 35 (11 files), 36 (5 files) |
| Files omitting T4 | 16 |
| Files omitting `v3_playbook` | 15 |
| Files omitting `sl_gap_buffer_pct` | 12 |
| enabled true / false | 15 / 1 (`pb01_breakout_retest`) |
| direction LONG / SHORT | 10 / 6 |
| intent INTRADAY / DELIVERY | 13 / 3 (`pipeline` equals `intent` in all 16) |
| horizon SAME_DAY / NEXT_DAY / SWING / BTST | 12 / 1 / 3 / 0 |
| order_protocol CO_PLUS_TGT / LIMIT_TRIPLE | 13 (all INTRADAY) / 3 (all DELIVERY) |
| pullback_wait_enabled true / false | 6 / 10 |
| smart_tgt_enabled true / false | 13 / 3 |
| v3_playbook true | 1 (`pb01_breakout_retest`) |
| Names without a `_long`/`_short` suffix | 2 (`pb01_breakout_retest`, `positional_sector_rotation`; both LONG) |

### 5.4 File values against the locked decisions (HISTORICAL intent, `docs/locked_decisions.yaml` L2606 to L2791)

| Decision | Statement (HISTORICAL) | Baseline (FACT) |
|---|---|---|
| S2 (L2615 to L2622), S12 (L2745 to L2755) | 15 files, names locked | 16 files; `pb01_breakout_retest` added (its header L2 to L21: "REGISTRATION STUB — SHADOW / NON-TRADING") |
| S3 (L2624 to L2646) | field list; time defaults 09:30 / 13:30; `max_risk_pct` | schema defaults 10:00 / 15:00 (L137 to L138); `max_risk_pct` deleted (L122 to L125); later fields not in S3: `pipeline`, `horizon`, `enabled`, `sl_gap_buffer_pct`, T4, `max_concurrent_positions`, `v3_playbook` |
| S4 (L2648 to L2664) | "Percentage float fields: > 0, < 1" | `sl_gap_buffer_pct` and the three `trailing_sl_*_pct` have no rule; `entry_offset_pct`, `min_adr_pct`, `max_spread_pct` allow 0 |
| S5 (L2666 to L2674) | every YAML declares all fields; "No reliance on Pydantic defaults" | every file omits 5 or 6 schema keys; the schema docstring L46 says the same but does not enforce it (28 defaults) |
| S6 (L2676 to L2688) | positional: `sl_method` ATR, `tgt_method` ATR, `entry_end_time` 14:30 | FIXED_PCT, RISK_REWARD, 15:00 in all three |
| S7 (L2690 to L2698) | SHORT mirrors LONG | identical pairs (5.2) |
| S8 (L2700 to L2708) | callers get `ConfigSchemaError` "for uniformity" | holds for missing file, syntax, non-mapping, schema; not for the raw errors in 3.1 (INTERPRETATION) |
| S9 (L2710 to L2722) | `load_all_strategies(strategies_dir, scan_webhook_map_path=None)` | plus `force_intraday_only` (L106) |
| S10 (L2724 to L2733) | cross-validation when the map path is given | no production caller gives it (3.3) |
| S13 (L2757 to L2769) | intraday R:R 2.0; gap_go 2.5; gap_fade 1.5; first_pullback `sl_pct` 0.015; vwap 0.008; pullback wait true except gap_go, gap_fade, range_breakout | `tgt_risk_reward` 1.5 in all 16; `sl_pct` as stated except gap_go 0.012; pullback-wait pattern as stated |

---

## 6. `config/strategy_direction_registry.yaml` and `config/scoring_weights.yaml`

### 6.1 `config/strategy_direction_registry.yaml` (154 lines; 1 commit, 26885bb, 2026-07-18)

Structure (keys only): `strategies` → 16 entries keyed by strategy name, each with `direction`, `registration_status`, `health`, `first_seen`, `evidence` {`scanner`, `source_yaml`}. FACT (static): the 16 names equal the 16 YAML names; each `direction` equals the YAML `direction`; each `evidence.source_yaml` is `config/strategies/<name>.yaml` and each `evidence.scanner` equals the name. Header comment L1 to L25 (HISTORICAL): seeded 2026-07-17, "auto-maintained by scripts/strategy_registry_officer.py", mirrors `StrategyConfig.direction`, "nothing reads direction FROM here to place a trade".

| Reader / writer | Lines | How | Required? / fallback | Owner |
|---|---|---|---|---|
| `core/strategy_direction.py` `_read_registry` | L84 to L95 | direct `yaml.safe_load` (utf-8) of `strategies`; missing or unreadable → `None`; any exception → `None` | — | A07 |
| `core/strategy_direction.py` `load_registry(path=DEFAULT_STATE_PATH, seed_path=None)` | L98 to L121 | reads the runtime STATE file `data_store/strategy_direction_registry.yaml` (L44); the tracked SEED `config/strategy_direction_registry.yaml` (L43) is read only when the state file is missing/unreadable and a `seed_path` is given | optional; neither → `{}` | A07 |
| `core/strategy_direction.py` `save_registry` | L124 to L136 | writes STATE only (atomic temp + rename); docstring: "Writes STATE, never the tracked seed" | — | A07 |
| `scripts/strategy_registry_officer.py` `main` / `run` | L276 to L287; L230 to L231 | state path `data_store/...` (L281 to L282), `seed_path = config_dir / "strategy_direction_registry.yaml"` (L283); `load_registry(registry_path, seed_path=seed_path)` (L231) | seed is the first-run fallback | A07 (cron entry: A16) |
| `scripts/preflight/checks/config_integrity.py` `ConfigYamlValidCheck` | L75 to L93 (glob L85) | parses every top-level `config/*.yaml` for syntax only, so this file too | CRITICAL fail on parse error | A20 |
| `utils/startup_checks.py` `check_temp_config_values` | L1465 to L1501 (glob L1477, read L1481) | reads the raw text of every top-level `config/*.yaml`, so this file too, and counts "# TEMP" markers; no parse | `OSError` → skip file; warning only (L1644 to L1646) | A01 |

Not read by `core/config_loader.py` (central loader), and its content is not used by any live trading path (FACT, git grep `direction_registry`: only the two modules above plus comments; the two glob readers in the table read it only for syntax or for markers). HISTORICAL inconsistency: `config/cron_registry.yaml` L624 to L625 (A16's file) says the officer "writes config/strategy_direction_registry.yaml", while `core/strategy_direction.py` L31 to L44 and the officer L278 to L283 say production writes only `data_store/...`. Whether the state file existed in production is UNKNOWN / NOT ESTABLISHED.

### 6.2 `config/scoring_weights.yaml` (44 lines; 10 commits, last c1ad82e, 2026-07-12)

Structure (keys only): `steps` → `volume_surge`, `vwap_position`, `atr_filter`, `rsi_range`, `price_action`, `sector_strength`, `time_of_day`, `spread_check`, `circuit_check`, `signal_age`; top level also `min_pass_score`, `high_score_threshold`, `medium_score_threshold`, `v3_hardgate_mode`, `v3_gate_steps`, `v3_freshness_max_sec`, `v3_min_pass_score`, `v3_high_score_threshold`, `v3_medium_score_threshold`. Static: the keys match `ScoringConfig` / `ScoringStepsConfig` exactly (no unknown, none missing). The file has 51 non-ASCII bytes (comments), no BOM.

| Reader | Lines | How | Required? / fallback | Owner |
|---|---|---|---|---|
| `core/config_loader.py` `load_all` | `_CONFIG_FILES` L2446; loop L2480 to L2516; `ScoringStepsConfig` L2280 to L2292; `ScoringConfig` L2295 to L2339 (`v3_hardgate_mode` validator L2319 to L2324; threshold ordering L2326 to L2339) | central loader: reads bytes, SHA-256 into `file_hashes`, `yaml.safe_load(bytes)`, `ScoringConfig.model_validate`; `extra="forbid"`; all 10 steps and the three live thresholds required, v3 keys defaulted | required: missing → `ConfigMissingError` (L2483 to L2488); parse/schema → `ConfigSchemaError` | A02 |
| ↳ `main.py` | L3230 to L3233 (`QualityScorer(weights=app_config.scoring)`); L3245 (`HardGate(freshness_max_sec=app_config.scoring.v3_freshness_max_sec)`); L3296 (`SecondaryScreener(scoring_config=app_config.scoring)`) | consumers of the validated object | — | A01 (wiring); A07 (logic) |
| `core/config_auditor.py` `audit_app_config` | L836 (`_safe_load_yaml` L850 to L858); rules B4 L361 to L366 and B5 L371 to L382 (the six threshold keys) | raw re-read for regression guards | best-effort: failure → `None`, group skipped | A02 |
| `utils/startup_checks.py` | L833 to L843 | presence list only | missing → blocking (A01) | A01 |
| `utils/startup_checks.py` `check_temp_config_values` | L1465 to L1501 (glob L1477, read L1481) | raw text, utf-8, counts "# TEMP" markers; no parse | `OSError` → skip file; warning only (L1644 to L1646) | A01 |
| `scripts/preflight/checks/config_integrity.py` | `_BASE_CONFIG_FILES` L16 to L24; `ConfigYamlValidCheck` L85 | presence; syntax | — | A20 |
| `scripts/premarket_healthcheck.py` | L54 to L62 | presence list (deprecated predecessor) | — | A20 |
| `reports/daily_report.py` | L150 to L154 | direct `open()` without `encoding`, `min_pass_score` | default 60 (L141, L154); any error → `pass` | A15 |
| `ops_dashboard/backend/readers/config_reader.py` | `get_min_pass_score` L118 to L147 (path L130); `get_scoring_weights` L298 to L307 | direct read, utf-8 | missing/unreadable → system_config fallback or `None`; `{}` | A15 |
| `scripts/forward_shadow_record.py` | `_weights` L45 to L54; SHA L83 | direct read, utf-8, `steps` | none (raises) | A18 |
| `scripts/v3_hardgate_parity_recompute.py` | `_load_weights` L198 to L204 | direct `open()` without encoding | any error → `_DEFAULT_WEIGHTS` | A18 |
| `strategies/schema.py` | L116 (comment only) | `min_score` 0 means "use global from scoring_weights.yaml" | — | A02 |

Link to the strategy files (FACT): per-strategy `min_score` overrides the global threshold only when `> 0` (`screening/secondary_screener.py` L317 to L321; V3 path L501 to L505 via `rescale_min_score`). All 16 files have `min_score: 0`.

---

## 7. Handoff to A07: strategy fields read by consumers (call site and attribute only; logic not studied)

Live object = the `StrategyConfig` from C2. "No non-test reader found" = FACT from `git grep` of `.<field>` and `"<field>"` over non-test `*.py` (schema.py excluded).

| Field | Reader (call site) | Owner |
|---|---|---|
| `name` | signal_processor L1120, L2116, L2458 (`perf_weights` key), L1830, L1890 (logs); secondary_screener `getattr(strategy, "name")` in every `_persist` call (e.g. L163, L231, L369); strategy_direction L70; taxonomy L35 | A06, A07 |
| `direction` | signal_processor L1000, L1034, L1045, L1379, L1558, L1775, L1910; config_integrity L176; strategy_direction L69 to L70; strategy_status L100 | A06, A07, A20 |
| `intent` | strategies/control.py L76; signal_processor L1001, L1047, L1117, L1313 to L1329, L1452, L1560, L1593, L1641, L2113 to L2159, L2257, L2306, L2456 to L2492, L2556, L2592; main.py L4149; strategies/loader.py L142 (log only); strategy_status L91 | A07, A06, A12 |
| `enabled` | strategies/control.py L77; config_auditor L228; strategy_status L93; (raw) system_manager L515, dashboard config_reader L70 | A07, A02, A15 |
| `entry_start_time`, `entry_end_time` | core/market_windows.py `is_entry_allowed_for_strategy` L152 to L175 (parse L169 to L170), called from signal_processor L977, L2078, L2420; config_auditor L749 to L750 | A01, A06, A02 |
| `entry_method`, `entry_offset_pct` | signal_processor L1779 to L1796 | A06 / A09 |
| `sl_method`, `sl_pct`, `sl_min_pct`, `sl_max_pct` | signal_processor L1801, L1814, L1852 to L1867; shadow_tracker L825 to L840 | A06 / A09; A11 |
| `sl_gap_buffer_pct` | signal_processor L1877 (used as a percent: `/ 100.0` at L1883) | A06 / A09 |
| `tgt_method`, `tgt_pct`, `tgt_risk_reward` | signal_processor L1911, L1925, L1932; `tgt_risk_reward` also L1459, L2265, L2560 → order_placer; shadow_tracker L329 to L334, L844 to L855 | A06 / A09, A10, A11 |
| `pullback_wait_enabled` | signal_processor L1082 | A06 / A07 |
| `min_volume_surge`, `min_adr_pct`, `max_spread_pct` | secondary_screener L235 to L238, L461 to L464 (into the thresholds dict read by step_executor L255, L280, L394, which has its own fallbacks) | A07 |
| `min_score` | secondary_screener L317 to L321, L501 to L505 | A07 |
| `lot_size` | signal_processor L1119, L2115, L2457 (to the sizer) | A06 / A09 |
| `max_concurrent_positions` | signal_processor L760 (`getattr`, default 2) | A06 / A09 |
| `v3_playbook` | main.py L3648 (allocator `v3_scope_fn`); signal_processor L1603; strategy_status L81 | A18, A06, A07 |
| `trailing_sl_enabled`, T4 thresholds | order_placer L2175 to L2192, guarded by `getattr(fill_entry, "strategy_obj", None) is not None`; `_FillEntry.__slots__` (L498 to L503) has no `strategy_obj`; config_auditor L228 | A10 / A11 (OPEN QUESTION for them: can that guard ever be true?), A02 |
| `pipeline`, `horizon` | taxonomy L35; strategy_status L101 (display only) | A07 |
| `order_protocol` | no non-test reader of the strategy attribute found; `OrderPlacer.place` takes the protocol from `self._default_protocol` (L961), and main.py L3061 to L3087 does not pass `default_order_protocol`, whose default is "LIMIT_TRIPLE" (L572); raw dashboard read config_reader L79 | A10 (OPEN QUESTION for A10) |
| `display_name` | dashboard config_reader L69 (raw read); downstream, from the dict that `get_strategies` returns: `services/controls.py` L62 and L78, `services/strategy_meta.py` L75 | A15 |
| `sl_atr_multiplier`, `tgt_atr_multiplier` | no non-test reader found | A07 / A09 |
| `smart_tgt_enabled`, `smart_tgt_trail_trigger_pct`, `smart_tgt_trail_step_pct` | no non-test reader found; order_placer gets `smart_tgt_config=app_config.system.smart_tgt` (main.py L3072) | A11 |
| `pullback_wait_tolerance_pct`, `pullback_wait_timeout_sec` | no non-test reader found (named only in comments at screening/entry_gate.py L69 to L70; `WatchEntry` is built from DB rows at L209 to L218) | A07 |
| `active_days` | no non-test reader found | A07 / A01 |
| `description` | not established | — |

Note for A11: `orders/shadow_tracker.py` reads strategy fields only when constructed with `strategies` (L144, L327, L666); main.py L2946 to L2958 constructs it without that argument (FACT); effect at runtime UNKNOWN / NOT ESTABLISHED.
