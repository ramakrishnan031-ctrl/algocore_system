# A02 evidence: The configuration loader: schema, load flow, defaults and errors

**Status:** APPROVED — evidence for the A02 STUDY, approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31)
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06. Approved by Rama on 2026-11-09 with the A02 topic package (Decision Register, D-31): status marked APPROVED; content unchanged.
**Purpose and scope:** This file records what `core/config_loader.py` does: its module map, the full schema of its 65 models field by field (types, defaults, enforced constraints and presence in the baseline files), the `load_all` load flow, the code defaults that apply at the baseline, error behaviour, precedence, caching, callers, the post-deployment commit `5f75c9b`, and the configuration-side facts for the A01 handoffs C10a, C10b, C35, C12, M-24, M-19, M-20 and C7d/S-11. It supports the A02 STUDY sections on the central loader and schema, load and error behaviour, defaults and precedence, consumers, and the A01 handoffs.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

## About this file

- **File studied:** `core/config_loader.py`, 2,516 lines, git blob `8635bca77531515561ee48cf92677883a5e30782`, SHA-256 of the content `4e4f0d5c1acee0eb1f3216c69c8fe8be4d89b61d867c9a9a3576f173edcfbece`; last changed by `5f75c9b` (2026-09-10), the only commit to this file after the last recorded deployment (`7d4970a`, 2026-09-02; A02 source inventory section 2).
- **Method:** FACT: `git rev-parse HEAD` returned the baseline commit and `git status --short` was empty before work began. All 2,516 lines read; an AST inventory of the file (source read with `git show`, never imported): 65 classes, 458 annotated fields, 97 decorated validators, 116 `raise ValueError`, 1 `raise ConfigMissingError`, 2 `raise ConfigSchemaError`; a static key and type comparison of the eight baseline YAML files against those field lists (`yaml.safe_load` of `git show` text; value validators were evaluated by hand only where stated); PyYAML 6.0.3 probes on synthetic text only (the pinned version, `requirements.txt` L6); pydantic probes on synthetic models only, with pydantic 2.13.5 (the pin is `pydantic==2.13.0`, `requirements.txt` L7), so pydantic behaviour is labelled INTERPRETATION; `git grep` for callers; `git show`, `git blame` and `git log` for history. No legacy code, test or script was imported or run. Every line reference is to the baseline commit and to `core/config_loader.py` unless another file is named.
- **Labels:** FACT (what the code or file shows at the cited lines); INTERPRETATION (reasoned reading, including Python, PyYAML and pydantic semantics); HISTORICAL (comments, docstrings, commit messages); UNKNOWN / NOT ESTABLISHED (anything about what actually ran); OPEN QUESTION. A YAML value is "the file value at the baseline", never proof that it was in force. Unlabelled table rows are FACT.
- **Security:** no credential value, address, identifier or secret URL part is reproduced. Environment-variable NAMES held in configuration are given, as key names.

## 1. Module map

### 1.1 Top-level statements other than classes

| Lines | Item | Kind | Role | Runs at import? |
|---|---|---|---|---|
| L1 to L41 | module docstring | docstring | HISTORICAL design notes CL1 to CL6 and the file list (see 1.4) | yes (string only) |
| L42 | `from __future__ import annotations` | import | all annotations stay strings; pydantic resolves them when each model class is built (INTERPRETATION) | yes |
| L44 | `import hashlib` | import | SHA-256 of each file (L2491) | yes |
| L45 | `from datetime import date as _date` | import | holiday dates (L2398 to L2408) and the holiday-file year (L2449) | yes |
| L46 | `from datetime import time as _dt_time` | import | `SERVICE_WINDOW_END_MAX` (L83) and the watchlist HH:MM checks (L1556, L1565) | yes |
| L47 | `from pathlib import Path` | import | the `load_all` default argument and path joins | yes |
| L49 | `import yaml` | import | `yaml.safe_load` (L2494), `yaml.YAMLError` (L2495) | yes |
| L50 | `from typing import Literal, Optional` | import | field types | yes |
| L52 | `from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator` | import | schema machinery; `ValidationError` caught at L2508 | yes |
| L54 | `from core.exceptions import ConfigMissingError, ConfigSchemaError` | import | the two exceptions `load_all` raises | yes (imports `core/exceptions.py`, stdlib-only by its docstring L15) |
| L83 | `SERVICE_WINDOW_END_MAX = _dt_time(18, 15)` | public constant | exclusive upper bound for `trading_hours.service_window_end` (L180); imported by `main.py` L57 and bound to `SERVICE_START_CUTOFF` (`main.py` L2001) | yes |
| L229 | `ABSOLUTE_MAX_LEVERAGE: float = 20.0` | public constant | hard ceiling for `capital.leverage_safety.max_allowed` (L283 to L288); no non-test importer (grep) | yes |
| L232 | `_DELIVERY_PINNED_LEVERAGE: float = 1.0` | private constant | `leverage_map.DELIVERY` must equal it (L320) | yes |
| L235 to L247 | `_validate_finite_leverage(v, key)` | private function | rejects NaN and +/-inf for leverage fields | definition only |
| L86 to L2434 | 65 `BaseModel` classes | classes | the schema (table 1.2; field detail in section 2) | class bodies run at import (see 1.3) |
| L2441 to L2450 | `_CONFIG_FILES` | private constant (tuple of 8 `(AppConfig key, file name, schema class)`) | the registry `load_all` iterates (L2480) | **yes, including `_date.today()` at L2449** |
| L2457 to L2516 | `load_all(config_dir: Path = Path("config")) -> AppConfig` | public function | the only loader entry point (section 3) | definition only; the default `Path("config")` is created once at import |

FACT: the module has no other public function, no `__all__`, no `if __name__ == "__main__"` block, no module-level cache, and no exception class (section 9.6).

### 1.2 Classes (65; all `BaseModel`, all `model_config = ConfigDict(extra="forbid")`)

| Class | Lines | Represents | Fields | Validators |
|---|---|---|---|---|
| `TradingHoursConfig` | L86 to L189 | `system_config.yaml: trading_hours` | 11 | 2 |
| `SignalQueueConfig` | L192 to L197 | `system_config.yaml: signal_queue` | 4 | 0 |
| `ClockSkewProbeConfig` | L200 to L211 | `system_config.yaml: clock.probe` | 2 | 1 |
| `ClockConfig` | L214 to L220 | `system_config.yaml: clock` | 5 | 0 |
| `LeverageSafetyConfig` | L250 to L289 | `system_config.yaml: capital.leverage_safety` | 2 | 2 |
| `LeverageMapConfig` | L292 to L327 | `system_config.yaml: capital.leverage_map` | 4 | 2 |
| `CapitalConfig` | L330 to L409 | `system_config.yaml: capital` | 9 | 5 |
| `OrderMonitorConfig` | L412 to L429 | `system_config.yaml: order_monitor` | 2 | 2 |
| `MisFilterConfig` | L432 to L450 | `system_config.yaml: mis_filter` | 3 | 1 |
| `PositionSizingTierConfig` | L453 to L457 | `system_config.yaml: position_sizing.tier_multipliers` | 3 | 0 |
| `PositionSizingConfig` | L460 to L561 | `system_config.yaml: position_sizing` | 16 | 7 |
| `SignalProcessorConfig` | L564 to L614 | `system_config.yaml: signal_processor` | 9 | 4 |
| `WebhookConfig` | L617 to L642 | `system_config.yaml: webhook` | 7 | 2 |
| `EodSquareoffConfig` | L645 to L731 | `system_config.yaml: eod_squareoff` | 8 | 6 |
| `KillSwitchConfig` | L734 to L744 | `system_config.yaml: kill_switch` | 2 | 1 |
| `RiskConfig` | L747 to L881 | `system_config.yaml: risk` | 14 | 6 |
| `SmtpConfig` | L884 to L949 | `system_config.yaml: alerts.smtp` | 9 | 4 |
| `EmailFallbackConfig` | L952 to L968 | `system_config.yaml: alerts.email_fallback` | 7 | 1 |
| `TelegramChannelConfig` | L971 to L975 | `system_config.yaml: alerts.telegram.channels[]` | 3 | 0 |
| `TelegramConfig` | L978 to L1003 | `system_config.yaml: alerts.telegram` | 10 | 1 |
| `OrderReconcilerConfig` | L1006 to L1097 | `system_config.yaml: order_reconciler` | 7 | 6 |
| `AlertsConfig` | L1100 to L1123 | `system_config.yaml: alerts` | 13 | 1 |
| `LoggingConfig` | L1126 to L1136 | `system_config.yaml: logging` | 1 | 1 |
| `ShadowTrackerConfig` | L1139 to L1150 | `system_config.yaml: shadow_tracker` | 3 | 1 |
| `SRDetectorConfig` | L1153 to L1255 | `system_config.yaml: sr_detector` | 45 | 3 |
| `RegimeConfig` | L1258 to L1301 | `system_config.yaml: regime` | 17 | 2 |
| `PortfolioAllocatorConfig` | L1304 to L1381 | `system_config.yaml: portfolio_allocator` | 7 | 5 |
| `V3ChainConfig` | L1384 to L1513 | `system_config.yaml: v3_chain` | 42 | 3 |
| `WatchlistConfig` | L1516 to L1574 | `system_config.yaml: watchlist` | 10 | 2 |
| `StructureExitConfig` | L1577 to L1607 | `system_config.yaml: structure_exit` | 6 | 2 |
| `PaperConfig` | L1610 to L1668 | `system_config.yaml: paper` | 4 | 3 |
| `SmartTgtConfig` | L1671 to L1701 | `system_config.yaml: smart_tgt` | 5 | 1 |
| `SlippageTier` | L1704 to L1710 | `system_config.yaml: entry_gate.slippage_control.tiers[]` | 2 | 0 |
| `SlippageOverridesConfig` | L1713 to L1746 | `system_config.yaml: entry_gate.slippage_control.overrides` | 4 | 1 |
| `SlippageControlConfig` | L1749 to L1784 | `system_config.yaml: entry_gate.slippage_control` | 9 | 1 |
| `EntryGateConfig` | L1787 to L1813 | `system_config.yaml: entry_gate` | 9 | 0 |
| `LiveFeedConfig` | L1816 to L1821 | `system_config.yaml: live_feed` | 3 | 0 |
| `FnoBanConfig` | L1824 to L1835 | `system_config.yaml: fno_ban` | 2 | 0 |
| `StrategyCircuitBreakerConfig` | L1838 to L1844 | `system_config.yaml: strategy_circuit_breaker` | 4 | 0 |
| `CircuitBreakerConfig` | L1847 to L1862 | `system_config.yaml: circuit_breaker` | 3 | 0 |
| `DriftHandlerConfig` | L1865 to L1918 | `system_config.yaml: drift_handler` | 4 | 3 |
| `BrokerConfig` | L1921 to L1927 | `system_config.yaml: broker` | 4 | 0 |
| `TgtRetryConfig` | L1930 to L1961 | `system_config.yaml: tgt_retry` | 4 | 3 |
| `EodReconcileConfig` | L1964 to L1973 | `system_config.yaml: eod_reconcile` | 2 | 0 |
| `EodCleanupConfig` | L1976 to L1984 | `system_config.yaml: eod_cleanup` | 1 | 0 |
| `SystemConfig` | L1987 to L2086 | `system_config.yaml` (top level) | 42 | 2 |
| `FuturesRatesConfig` | L2094 to L2098 | `broker_costs.yaml: zerodha.futures` | 2 | 0 |
| `OptionsBuyRatesConfig` | L2101 to L2105 | `broker_costs.yaml: zerodha.options_buy` | 2 | 0 |
| `OptionsSellRatesConfig` | L2108 to L2112 | `broker_costs.yaml: zerodha.options_sell` | 2 | 0 |
| `ZerodhaRatesConfig` | L2115 to L2128 | `broker_costs.yaml: zerodha` | 12 | 0 |
| `BrokerCostsConfig` | L2131 to L2168 | `broker_costs.yaml` (top level) | 1 | 1 |
| `TokenBucketConfig` | L2176 to L2179 | `broker_limits.yaml: order`; `broker_limits.yaml: quote`; `broker_limits.yaml: historical`; `broker_limits.yaml: margins` | 2 | 0 |
| `TimeoutsConfig` | L2182 to L2185 | `broker_limits.yaml: timeouts` | 2 | 0 |
| `RateLimitBackoffConfig` | L2188 to L2242 | `broker_limits.yaml: rate_limit_backoff` | 5 | 4 |
| `BrokerLimitsConfig` | L2245 to L2256 | `broker_limits.yaml` (top level) | 7 | 0 |
| `SlippageTierConfig` | L2264 to L2266 | `slippage_model.yaml: tiers.<key>` | 1 | 0 |
| `SlippageConfig` | L2269 to L2272 | `slippage_model.yaml` (top level) | 2 | 0 |
| `ScoringStepsConfig` | L2280 to L2292 | `scoring_weights.yaml: steps` | 10 | 0 |
| `ScoringConfig` | L2295 to L2339 | `scoring_weights.yaml` (top level) | 10 | 2 |
| `ScannerEntry` | L2347 to L2371 | `scan_webhook_map.yaml: scanners.<key>` | 3 | 2 |
| `ScanWebhookMapConfig` | L2374 to L2377 | `scan_webhook_map.yaml` (top level) | 1 | 0 |
| `ChartinkScannersConfig` | L2385 to L2388 | `chartink_scanners.yaml` (top level) | 1 | 0 |
| `HolidayEntry` | L2395 to L2408 | `nse_holidays_<year>.yaml: holidays[]` | 2 | 1 |
| `NseHolidaysConfig` | L2411 to L2413 | `nse_holidays_<year>.yaml` (top level) | 1 | 0 |
| `AppConfig` | L2420 to L2434 | container returned by `load_all` (L2516); not a YAML section | 9 | 0 |

"Validators" counts functions decorated with `field_validator` or `model_validator`; the `Literal` type of `signal_processor.atr_fallback_mode` (L572) and `Field(ge=1)` of `eod_cleanup.signal_retention_days` (L1984) are further constraints not counted there.

### 1.3 Code that runs at import time

| Lines | What runs | Effect |
|---|---|---|
| L42 to L54 | the imports | loads PyYAML, pydantic and `core/exceptions.py`; nothing else from the repository |
| L83, L229, L232 | constants | none beyond the values |
| L86 to L2434 | 65 class bodies | INTERPRETATION: pydantic builds a validator for each class (CPU only, no I/O) |
| L1114, L1989, L2022, L2023, L2024, L2025 | default instances `EmailFallbackConfig()`, `BrokerConfig()`, `CircuitBreakerConfig()`, `StrategyCircuitBreakerConfig()`, `LiveFeedConfig()`, `FnoBanConfig()` in class bodies | six model instances are constructed while the module is imported; their classes have no model validators, so nothing beyond default construction runs (INTERPRETATION: pydantic does not run field validators on defaults, `validate_default` is not set) |
| L2441 to L2450 | `_CONFIG_FILES` tuple | **L2449 calls `_date.today()` once**: the holiday file name `nse_holidays_<year>.yaml` is fixed for the life of the process at the first import (section 9.1) |
| L2457 | `def load_all(config_dir: Path = Path("config"))` | the default `Path("config")` object is created once; it is relative and resolved against the process working directory at each call (INTERPRETATION) |

FACT: no environment variable, file, network or clock other than L2449's `date.today()` is read at import. FACT (grep): the module contains no `os.environ` read outside `SmtpConfig.resolved_password` (L939 to L948) and no `open(`.

Lazy imports, executed only during validation or on a method call: `core.mis_squareoff_timing` (L122 to L124, inside `TradingHoursConfig._validate_mis_squareoff_timing`); `datetime.time` (L156); `os` (L939, inside `SmtpConfig.resolved_password`); `logging` and `core.config_auditor.audit_system_config` (L2071 to L2072, inside `SystemConfig._cross_field_sanity_checks`).

### 1.4 The module docstring against the code (HISTORICAL against FACT)

| Docstring statement | Code at the baseline |
|---|---|
| L10 to L13 "AppConfig ... holding all 8 sub-configs" | FACT: `AppConfig` has 8 sub-configs plus `file_hashes` (L2426 to L2434) |
| L14 to L15 CL2 "Atomic load. All 8 files must parse + validate. Any failure raises immediately. No partial AppConfig ever returned." | FACT: matches L2480 to L2516; the loop stops at the first failure |
| L16 to L17 CL3 "Every Pydantic model uses extra=\"forbid\"" | FACT: all 65 classes (AST) |
| L18 to L19 CL4 SHA-256 per file in `file_hashes` | FACT: L2490 to L2491 |
| L20 to L21 CL5 "No env-var interpolation, no includes. yaml.safe_load() only." | FACT: `yaml.safe_load` only (L2494); no interpolation code |
| L22 to L23 CL6 "Split into core/config_schemas/ if file exceeds 600 lines" | FACT: the file has 2,516 lines; no `core/config_schemas/` exists (not split) |
| L33 `nse_holidays_2026.yaml → NseHolidaysConfig` | FACT: the code builds the name from the year at import (L2449; since `c303e04`, 2026-06-13) |
| L37 "Does not read .env files or expand environment variables" | FACT for loading; `SmtpConfig.resolved_password` (L935 to L949) reads one variable when called |
| L39 "Does not fill in defaults for missing keys (CL3: extra=\"forbid\", all required)" | FACT: contradicted; many fields have defaults (section 2), and 38 key occurrences are absent from the baseline files and take the code default: 23 keys of `system_config.yaml` and `scanner_type` in 15 of the 16 `scan_webhook_map.yaml` entries, that is 24 distinct schema keys (section 3.5) |
| `requirements.txt` L7 comment "CL3: strict schema validation (extra=\"forbid\")" | FACT: no `ConfigDict` sets `strict=True`; INTERPRETATION: pydantic runs in its default lax (coercing) mode (section 4) |

## 2. The schema

### 2.1 General rules that apply to every model

| Rule | Where | Label |
|---|---|---|
| Unknown keys are rejected at every model level: `ConfigDict(extra="forbid")` on all 65 classes. | each class's `model_config` line (table 1.2) | FACT |
| Fields typed as a mapping accept ANY keys: `special_sessions` (L1992), `product_map` (L1995), `sr_detector.pivot_n_by_tf` (L1169), the three `v3_chain.regime_pref_*` maps (L1460 to L1465), the three `slippage_control.overrides.by_*` maps (L1732 to L1734), `slippage_model.yaml` `tiers` (L2271), both `scanners` maps (L2377, L2388). `extra="forbid"` does not apply to the keys of these maps. | cited lines | FACT (declarations); INTERPRETATION (pydantic semantics) |
| No `ConfigDict` sets `strict`, `validate_default`, `validate_assignment`, `frozen` or `allow_inf_nan`. So: inputs are coerced in lax mode; defaults are not passed through field validators; a loaded model can be changed by assignment without validation; float fields accept NaN and infinity unless a validator refuses them. | table 1.2 | FACT (absence); INTERPRETATION (pydantic 2 defaults) |
| A field with a type but no default is required; `Optional[X]` with no default is required but accepts `null`. | per field | INTERPRETATION (pydantic 2) |
| `field_validator` without a mode runs after type coercion; `HolidayEntry.date` is the only `mode="before"` validator (L2401). `model_validator(mode="after")` runs after all fields of that model validated, and only if they all validated; several "after" validators on one model run in definition order. | per class | INTERPRETATION (pydantic 2) |
| A `ValueError` raised in a validator, including a subclass such as `ConfigContradictionError`, becomes a pydantic validation error (`type` "value_error", message "Value error, <text>"). An `AssertionError` is converted too (`type` "assertion_error"), but this module contains no `assert` statement. Other exception types, for example `TypeError`, are not converted and propagate. | 114 `raise ValueError` in validators and 1 in the private function they call (section 9.6); no `assert` statement (grep) | FACT (raises, no `assert`); INTERPRETATION (pydantic) |
| Cross-file validation: none. `AppConfig` (L2420 to L2434) has no validator, and `load_all` validates each file on its own. Example: `scan_webhook_map.yaml` strategy names and `chartink_scanners.yaml` URLs are not compared here. | L2420 to L2434, L2480 to L2514 | FACT |

### 2.2 The eight files and their root models

| `AppConfig` key | File (L2441 to L2450) | Root model | Required top-level keys | Defaulted top-level keys |
|---|---|---|---|---|
| `system` | `system_config.yaml` | `SystemConfig` (L1987) | 20 | 22 |
| `broker_costs` | `broker_costs.yaml` | `BrokerCostsConfig` (L2131) | 1 (`zerodha`) | 0 |
| `broker_limits` | `broker_limits.yaml` | `BrokerLimitsConfig` (L2245) | 6 | 1 (`rate_limit_backoff`) |
| `slippage` | `slippage_model.yaml` | `SlippageConfig` (L2269) | 2 | 0 |
| `scoring` | `scoring_weights.yaml` | `ScoringConfig` (L2295) | 4 | 6 |
| `scan_webhook_map` | `scan_webhook_map.yaml` | `ScanWebhookMapConfig` (L2374) | 1 (`scanners`) | 0 |
| `chartink_scanners` | `chartink_scanners.yaml` | `ChartinkScannersConfig` (L2385) | 1 (`scanners`) | 0 |
| `nse_holidays` | `nse_holidays_{date.today().year}.yaml` | `NseHolidaysConfig` (L2411) | 1 (`holidays`) | 0 |

FACT (AST): across all 65 models, 169 of the 458 fields have no default (9 of them are `AppConfig`'s); 289 have a code default.

FACT (static check, section 3.5): at the baseline every one of the eight files (with `nse_holidays_2026.yaml` for the holiday entry) has no unknown key, no missing required key and no value of a plainly wrong YAML type for its field. This is a key and type comparison only; it does not prove that every validator passes (validators evaluated by hand are named where used).

### 2.3 Field tables, one per model

Each table lists every field: line, declared type, default ("REQUIRED" if none), the constraints the code actually enforces (with lines; "none" means only the type check applies), and whether the key is present in the baseline file. "mis L…" means `core/mis_squareoff_timing.py` (owner A12), cited only for what the schema delegates to it.

#### TradingHoursConfig (L86 to L189)

- YAML: `system_config.yaml: trading_hours`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `entry_start` | L88 | `str` | REQUIRED | `_hhmm` parse L158 to L160 (split on ':' into exactly 2 parts, `int()` each, `time()` range); chain L168: market_open <= entry_start < entry_end | present |
| `entry_end` | L89 | `str` | REQUIRED | chain L168: entry_start < entry_end <= eod_entry_cutoff; also strict HH:MM and entry_end < CHECK_1 via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) L118, L150 | present |
| `eod_entry_cutoff` | L90 | `str` | REQUIRED | chain L168: entry_end <= eod_entry_cutoff <= eod_squareoff_time | present |
| `eod_squareoff_time` | L91 | `str` | REQUIRED | chain L168: eod_entry_cutoff <= eod_squareoff_time <= market_close; also strict HH:MM and cutoff < eod_squareoff_time via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) L119, L150 | present |
| `market_open` | L92 | `str` | `"09:15"` | chain L168: market_open <= entry_start | present |
| `market_close` | L93 | `str` | `"15:30"` | chain L168: eod_squareoff_time <= market_close; L180: market_close <= service_window_end | present |
| `service_window_end` | L98 | `str` | `"16:00"` | L179 to L188: market_close <= service_window_end < `SERVICE_WINDOW_END_MAX` (18:15, L83) | present |
| `mis_squareoff_cutoff` | L104 | `str` | `"15:12"` | strict HH:MM (str; 2 digit-only parts after strip; 0-23, 0-59; mis L40 to L56); CHECK_2 < cutoff < eod_squareoff_time (mis L150); via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) | present |
| `mis_squareoff_first_offset` | L105 | `str` | `"5m"` | strict `<N>m`, N > 0 (mis L59 to L75); first > second (mis L140 to L144); entry_end < CHECK_1 = cutoff - first (mis L147, L150); via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) | present |
| `mis_squareoff_second_offset` | L106 | `str` | `"2m"` | strict `<N>m`, N > 0; CHECK_1 < CHECK_2 = cutoff - second < cutoff (mis L148, L150); via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) | present |
| `mis_squareoff_margin_sec` | L107 | `int` | `20` | int by the pydantic type (INTERPRETATION: a YAML `true` or `false` is coerced to 1 or 0 before the model validator runs, so the bool test in mis L121 to L124 is not reached from YAML; both values are then rejected by the margin floor, since 1 and 0 are below 5); margin_sec >= poll_interval_sec, where the schema passes the LITERAL `poll_interval_sec=5` (L131; mis L129 to L138); via `_validate_mis_squareoff_timing` L109 to L137 -> `MisSquareoffTiming.build` (`core/mis_squareoff_timing.py`) | present |

#### SignalQueueConfig (L192 to L197)

- YAML: `system_config.yaml: signal_queue`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `capacity` | L194 | `int` | REQUIRED | none | present |
| `backpressure_pct` | L195 | `float` | REQUIRED | none | present |
| `expiry_sec` | L196 | `int` | REQUIRED | none | present |
| `warning_pct` | L197 | `float` | `0.60` | none | present |

#### ClockSkewProbeConfig (L200 to L211)

- YAML: `system_config.yaml: clock.probe`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "BL-21: periodic broker clock skew probe driver."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L203 | `bool` | `True` | none | present |
| `probe_interval_sec` | L204 | `int` | `60` | > 0 (L206 to L211) | present |

#### ClockConfig (L214 to L220)

- YAML: `system_config.yaml: clock`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `warn_skew_sec` | L216 | `float` | REQUIRED | none (no ordering among the four tiers) | present |
| `alert_skew_sec` | L217 | `float` | REQUIRED | none | present |
| `halt_skew_sec` | L218 | `float` | REQUIRED | none | present |
| `startup_max_skew_sec` | L219 | `float` | REQUIRED | none | present |
| `probe` | L220 | `ClockSkewProbeConfig` | `Field(default_factory=ClockSkewProbeConfig)` | nested model | present |

#### LeverageSafetyConfig (L250 to L289)

- YAML: `system_config.yaml: capital.leverage_safety`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "GOVERNANCE block -- deliberate, reviewed, rarely touched."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `min_allowed` | L262 | `float` | REQUIRED | finite (L265 to L268 -> `_validate_finite_leverage` L235 to L247: rejects NaN and +/-inf); >= 1.0 (L272 to L277) | present |
| `max_allowed` | L263 | `float` | REQUIRED | finite (as above); >= min_allowed (L278 to L282); <= `ABSOLUTE_MAX_LEVERAGE` 20.0 (L283 to L288, L229) | present |

#### LeverageMapConfig (L292 to L327)

- YAML: `system_config.yaml: capital.leverage_map`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "OPERATIONAL block -- the per-intent multiplier actually applied."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `INTRADAY` | L307 | `float` | REQUIRED | finite (L312 to L315); within [leverage_safety.min_allowed, leverage_safety.max_allowed] (CapitalConfig L389 to L409) | present |
| `COVER_ORDER` | L308 | `float` | REQUIRED | finite (L312 to L315); within [leverage_safety.min_allowed, leverage_safety.max_allowed] (CapitalConfig L389 to L409) | present |
| `DELIVERY` | L309 | `float` | REQUIRED | finite (L312 to L315); within [leverage_safety.min_allowed, leverage_safety.max_allowed] (CapitalConfig L389 to L409); exactly 1.0 (L317 to L327, `_DELIVERY_PINNED_LEVERAGE` L232) | present |
| `BRACKET_ORDER` | L310 | `float` | REQUIRED | finite (L312 to L315); within [leverage_safety.min_allowed, leverage_safety.max_allowed] (CapitalConfig L389 to L409) | present |

#### CapitalConfig (L330 to L409)

- YAML: `system_config.yaml: capital`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 5.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `intraday_bucket_pct` | L332 | `float` | REQUIRED | 0 < v < 1 (L382 to L387); no check that the two buckets sum to 1 | present |
| `positional_bucket_pct` | L333 | `float` | REQUIRED | 0 < v < 1 (L382 to L387) | present |
| `conditional_allocation_enabled` | L340 | `bool` | `False` | none | present |
| `slm_margin_buffer_pct` | L345 | `float` | `0.05` | none | present |
| `sl_limit_offset_pct` | L346 | `float` | `0.005` | rejects v < 0 or v >= 0.10 (L357 to L363) | present |
| `gtt_sl_limit_offset_pct` | L350 | `float` | `0.03` | 0 < v < 0.20 (L365 to L372) | present |
| `emergency_exit_buffer_pct` | L351 | `float` | `0.01` | rejects v < 0 or v >= 0.10 (L374 to L380) | present |
| `leverage_map` | L352 | `LeverageMapConfig` | REQUIRED | nested model; cross-checked against leverage_safety (L389 to L409) | present |
| `leverage_safety` | L355 | `LeverageSafetyConfig` | REQUIRED | nested model (self-validating) | present |

#### OrderMonitorConfig (L412 to L429)

- YAML: `system_config.yaml: order_monitor`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `poll_interval_sec` | L414 | `int` | REQUIRED | >= 1 (L417 to L422) | present |
| `fill_timeout_sec` | L415 | `int` | REQUIRED | >= 5 (L424 to L429) | present |

#### MisFilterConfig (L432 to L450)

- YAML: `system_config.yaml: mis_filter`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "MIS Learned Blocklist — source-free pre-drop of MIS-blocked symbols."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L441 | `bool` | `False` | none | present |
| `shadow` | L442 | `bool` | `True` | none | present |
| `ttl_days` | L443 | `int` | `1` | >= 1 (L445 to L450) | present |

#### PositionSizingTierConfig (L453 to L457)

- YAML: `system_config.yaml: position_sizing.tier_multipliers`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `HIGH` | L455 | `float` | REQUIRED | none | present |
| `MEDIUM` | L456 | `float` | REQUIRED | none | present |
| `LOW` | L457 | `float` | REQUIRED | none | present |

#### PositionSizingConfig (L460 to L561)

- YAML: `system_config.yaml: position_sizing`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 7.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `risk_per_trade_pct` | L462 | `float` | REQUIRED | 0 < v < 1 (L515 to L520) | present |
| `max_concentration_pct` | L463 | `float` | REQUIRED | 0 < v <= 1 (L522 to L527) | present |
| `min_qty_threshold` | L464 | `int` | REQUIRED | >= 1 (L529 to L534) | present |
| `lot_skew_rejection_threshold` | L465 | `float` | REQUIRED | 0 < v <= 1 (L536 to L541) | present |
| `min_tick_size` | L466 | `float` | REQUIRED | none | present |
| `max_single_order_qty` | L467 | `int` | REQUIRED | none | present |
| `max_position_value_pct` | L474 | `float` | REQUIRED | 0 < v <= 1 (L543 to L549) | present |
| `tier_multipliers` | L475 | `PositionSizingTierConfig` | REQUIRED | nested model | present |
| `dynamic_by_winrate` | L476 | `bool` | `True` | none | present |
| `min_multiplier` | L477 | `float` | `0.5` | none (no ordering with max_multiplier) | present |
| `max_multiplier` | L478 | `float` | `2.0` | none | present |
| `enabled` | L479 | `bool` | `True` | when false, flat_value_rs must be non-null and > 0 (L551 to L561) | present |
| `flat_value_rs` | L480 | `Optional[float]` | `None` | checked only when enabled is false (L551 to L561) | absent: default applies |
| `delivery_risk_per_trade_pct` | L497 | `Optional[float]` | REQUIRED (nullable: no default) | null rejected with a reason (L501 to L510); 0 < v <= 1 (L511 to L512) | present |
| `delivery_max_concentration_pct` | L498 | `Optional[float]` | REQUIRED (nullable: no default) | null rejected with a reason (L501 to L510); 0 < v <= 1 (L511 to L512) | present |
| `delivery_max_position_value_pct` | L499 | `Optional[float]` | REQUIRED (nullable: no default) | null rejected with a reason (L501 to L510); 0 < v <= 1 (L511 to L512) | present |

#### SignalProcessorConfig (L564 to L614)

- YAML: `system_config.yaml: signal_processor`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 4.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `worker_count` | L566 | `int` | REQUIRED | 1 <= v <= 50 (L588 to L593) | present |
| `drain_poll_sec` | L567 | `float` | REQUIRED | rejects v <= 0 (L595 to L600) | present |
| `pipeline_timeout_sec` | L568 | `int` | REQUIRED | >= 1 (L602 to L607) | present |
| `atr_fallback_mode` | L572 | `Literal["WARN", "HALT"]` | `"WARN"` | type `Literal["WARN", "HALT"]` (L572) | absent: default applies |
| `tgt_min_pct` | L575 | `float` | `0.003` | 0 < v < 1 (L609 to L614) | present |
| `min_gap_between_entries_sec` | L581 | `float` | `0.0` | none | present |
| `entry_burst_window_sec` | L582 | `float` | `60.0` | none | present |
| `entry_burst_max` | L583 | `int` | `0` | none | present |
| `per_symbol_cooldown_sec` | L586 | `float` | `0.0` | none | present |

#### WebhookConfig (L617 to L642)

- YAML: `system_config.yaml: webhook`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `bind_host` | L619 | `str` | REQUIRED | none | present |
| `bind_port` | L620 | `int` | REQUIRED | none (no port-range check) | present |
| `require_hmac` | L621 | `bool` | REQUIRED | none | present |
| `dedup_window_seconds` | L622 | `int` | `300` | none | present |
| `per_ip_rate_limit_enabled` | L626 | `bool` | `True` | none | present |
| `per_ip_burst` | L627 | `int` | `60` | >= 1 (L630 to L635) | present |
| `per_ip_refill_per_sec` | L628 | `float` | `5.0` | rejects v < 0 (L637 to L642) | present |

#### EodSquareoffConfig (L645 to L731)

- YAML: `system_config.yaml: eod_squareoff`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 6.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `inter_order_delay_ms` | L647 | `int` | REQUIRED | 0 <= v <= 5000 (L669 to L674) | present |
| `poll_interval_sec` | L648 | `int` | REQUIRED | >= 1 (L676 to L681); not cross-checked with trading_hours.mis_squareoff_margin_sec (the MIS check uses the literal 5, L131) | present |
| `auto_resume_kill_switch` | L649 | `bool` | REQUIRED | none | present |
| `exit_protocol` | L651 | `str` | `"MARKET"` | in {MARKET, LIMIT_THEN_MARKET} (L683 to L689) | present |
| `limit_aggressive_pct` | L652 | `float` | `0.01` | 0 < v <= 0.10 (L691 to L698) | present |
| `limit_grace_sec` | L653 | `float` | `120.0` | 0 <= v <= 300 (L700 to L707) | present |
| `mis_pass_1_market_protection_percent` | L666 | `float` | `1.5` | 0.1 <= v <= 10.0, a PERCENT (L709 to L731; added by 5f75c9b) | present |
| `mis_pass_2_market_protection_percent` | L667 | `float` | `2.5` | 0.1 <= v <= 10.0, a PERCENT (L709 to L731; added by 5f75c9b) | present |

#### KillSwitchConfig (L734 to L744)

- YAML: `system_config.yaml: kill_switch`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `api_failure_threshold` | L736 | `int` | REQUIRED | >= 1 (L739 to L744) | present |
| `enable_auto_trip` | L737 | `bool` | REQUIRED | none | present |

#### RiskConfig (L747 to L881)

- YAML: `system_config.yaml: risk`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 6.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `max_open_positions` | L749 | `int` | REQUIRED | >= 1 (L824 to L829) | present |
| `max_daily_trades` | L750 | `int` | REQUIRED | >= 1 (L824 to L829) | present |
| `max_open_delivery_positions` | L776 | `Optional[int]` | REQUIRED (nullable: no default) | null rejected with a reason (L831 to L843); >= 1 (L844 to L845) | present |
| `max_daily_delivery_trades` | L777 | `Optional[int]` | REQUIRED (nullable: no default) | null rejected with a reason (L831 to L843); >= 1 (L844 to L845) | present |
| `one_trade_per_symbol_direction_per_day` | L784 | `bool` | `False` | none | present |
| `max_sector_exposure_pct` | L785 | `float` | REQUIRED | 0 < v <= 1 (L848 to L853) | present |
| `max_consecutive_losses` | L786 | `int` | REQUIRED | >= 1 (L824 to L829) | present |
| `daily_loss_limit_pct` | L787 | `float` | REQUIRED | 0 < v <= 1 (L848 to L853) | present |
| `delivery_max_sector_exposure_pct` | L799 | `Optional[float]` | REQUIRED (nullable: no default) | null rejected with a reason (L855 to L864); 0 < v <= 1 (L865 to L866) | present |
| `delivery_daily_loss_limit_pct` | L800 | `Optional[float]` | REQUIRED (nullable: no default) | null rejected with a reason (L855 to L864); 0 < v <= 1 (L865 to L866) | present |
| `daily_loss_include_unrealized` | L806 | `bool` | `False` | none | present |
| `price_drift_threshold` | L807 | `float` | `0.005` | none | present |
| `sector_cap_mode` | L815 | `str` | `"observe"` | in {observe, enforce} (L869 to L874) | present |
| `sector_unknown_alert_pct` | L816 | `float` | `0.20` | 0 <= v <= 1 (L876 to L881) | present |

#### SmtpConfig (L884 to L949)

- YAML: `system_config.yaml: alerts.smtp`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 4.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `host` | L886 | `str` | REQUIRED | none | present |
| `port` | L887 | `int` | REQUIRED | 1 <= v <= 65535 (L902 to L907) | present |
| `use_tls` | L888 | `bool` | REQUIRED | none | present |
| `username` | L889 | `str` | REQUIRED | none | present |
| `password` | L890 | `str` | `""` | plaintext fallback; at least one of password / password_env non-empty (L923 to L933) | absent: default applies |
| `password_env` | L894 | `str` | `""` | name of an environment variable; at least one of password / password_env non-empty (L923 to L933); the variable is read only when `resolved_password()` is called (L935 to L949) | present |
| `from_address` | L898 | `str` | REQUIRED | none (no address-format check) | present |
| `to_addresses` | L899 | `list[str]` | REQUIRED | non-empty list (L916 to L921); no address-format check | present |
| `timeout_sec` | L900 | `int` | REQUIRED | >= 1 (L909 to L914) | present |

#### EmailFallbackConfig (L952 to L968)

- YAML: `system_config.yaml: alerts.email_fallback`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "FIX-132 Item 10: email fallback when Telegram fails for CRITICAL alerts."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L955 | `bool` | `False` | none | present |
| `smtp_host` | L956 | `str` | `"smtp.gmail.com"` | none | present |
| `smtp_port` | L957 | `int` | `587` | 1 <= v <= 65535 (L963 to L968) | present |
| `from_addr_env` | L958 | `str` | `"ALERT_EMAIL_USER"` | none (variable name) | present |
| `password_env` | L959 | `str` | `"ALERT_EMAIL_PASSWORD"` | none (variable name) | present |
| `to_addr_env` | L960 | `str` | `"ALERT_EMAIL_TO"` | none (variable name) | present |
| `use_tls` | L961 | `bool` | `True` | none | present |

#### TelegramChannelConfig (L971 to L975)

- YAML: `system_config.yaml: alerts.telegram.channels[]`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `chat_id_env` | L973 | `str` | REQUIRED | none (variable name) | present in 2 of 2 instances |
| `label` | L974 | `str` | REQUIRED | none | present in 2 of 2 instances |
| `enabled` | L975 | `bool` | `False` | none | present in 2 of 2 instances |

#### TelegramConfig (L978 to L1003)

- YAML: `system_config.yaml: alerts.telegram`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L980 | `bool` | `True` | none | present |
| `bot_token_env` | L981 | `str` | `"TELEGRAM_BOT_TOKEN"` | none (variable name; empty string accepted) | present |
| `telegram_alerts_in_paper_mode` | L982 | `bool` | `True` | none (paper-mode behaviour: out of scope) | present |
| `channels` | L983 | `list[TelegramChannelConfig]` | REQUIRED | non-empty list (L998 to L1003) | present |
| `personal_chat_id_env` | L984 | `str` | `""` | none (variable name) | present |
| `whitelist_only` | L985 | `bool` | `True` | none | present |
| `max_retries` | L986 | `int` | `3` | none | present |
| `retry_backoff_seconds` | L987 | `float` | `2.0` | none | present |
| `rate_limit_per_minute` | L988 | `int` | `20` | none | present |
| `send_deadline_seconds` | L996 | `Optional[float]` | `8.0` | none (null allowed = unbounded, per comment L992) | present |

#### OrderReconcilerConfig (L1006 to L1097)

- YAML: `system_config.yaml: order_reconciler`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 6.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `poll_interval_sec` | L1008 | `int` | REQUIRED | >= 1 (L1054 to L1059) | present |
| `capital_drift_tolerance` | L1009 | `float` | REQUIRED | rejects v < 0.0 (L1068 to L1073) | present |
| `capital_drift_tolerance_pct` | L1014 | `float` | `0.0` | none | present |
| `human_order_margin_tolerance` | L1019 | `float` | `5000.0` | rejects v < 0.0 (L1075 to L1080) | present |
| `capital_drift_alert_interval_sec` | L1026 | `float` | `1800.0` | rejects v < 1.0 (L1082 to L1087) | present |
| `stuck_exiting_timeout_minutes` | L1035 | `int` | `30` | >= 1 (L1061 to L1066) | present |
| `check1_mid_fill_defer_sec` | L1052 | `float` | `0.0` | rejects v < 0.0 (L1089 to L1097) | present |

#### AlertsConfig (L1100 to L1123)

- YAML: `system_config.yaml: alerts`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `failed_alerts_log_path` | L1102 | `str` | REQUIRED | none | present |
| `sentinel_dir` | L1103 | `str` | REQUIRED | none | present |
| `watcher_max_attempts` | L1104 | `int` | REQUIRED | >= 1 (L1118 to L1123) | present |
| `alert_digest_threshold` | L1105 | `int` | `3` | none | present |
| `watcher_lock_path` | L1106 | `str` | REQUIRED | none | present |
| `watcher_log_path` | L1107 | `str` | REQUIRED | none | present |
| `watcher_interval_sec` | L1108 | `int` | `60` | none | absent: default applies |
| `watcher_heartbeat_path` | L1109 | `Optional[str]` | `None` | none | absent: default applies |
| `respawn_restart_delta_threshold` | L1112 | `int` | `3` | none | absent: default applies |
| `respawn_rate_per_hour_threshold` | L1113 | `float` | `6.0` | none | absent: default applies |
| `email_fallback` | L1114 | `EmailFallbackConfig` | `EmailFallbackConfig()` | nested model (default is an instance built at class definition, L1114) | present |
| `telegram` | L1115 | `TelegramConfig` | REQUIRED | nested model | present |
| `smtp` | L1116 | `SmtpConfig` | REQUIRED | nested model | present |

#### LoggingConfig (L1126 to L1136)

- YAML: `system_config.yaml: logging`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "FIX-099: Logging subsystem configuration."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `min_free_disk_gb` | L1129 | `float` | REQUIRED | rejects v < 0.1 (L1131 to L1136) | present |

#### ShadowTrackerConfig (L1139 to L1150)

- YAML: `system_config.yaml: shadow_tracker`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1141 | `bool` | REQUIRED | none | present |
| `max_innings` | L1142 | `int` | REQUIRED | 1 <= v <= 5 (L1145 to L1150) | present |
| `alert_per_inning` | L1143 | `bool` | REQUIRED | none | present |

#### SRDetectorConfig (L1153 to L1255)

- YAML: `system_config.yaml: sr_detector`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 3. Docstring: "SNR-DETECTOR-V1 — shadow support/resistance detector config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1163 | `bool` | `False` | none | present |
| `timeframes` | L1164 | `list[str]` | `Field(default_factory=lambda: ["day", "60minute", "30minute"])` | non-empty; each in {day, 60minute, 30minute, 15minute, 5minute} (L1243 to L1255) | present |
| `lookback_days` | L1165 | `int` | `180` | none | present |
| `cache_ttl_sec` | L1166 | `float` | `1800.0` | none | present |
| `default_pivot_n` | L1168 | `int` | `5` | none | present |
| `pivot_n_by_tf` | L1169 | `dict[str, int]` | `Field(default_factory=dict)` | none (any keys, int values) | absent: default applies |
| `cluster_pct` | L1171 | `float` | `0.5` | none | present |
| `merge_pct` | L1172 | `float` | `0.4` | none | present |
| `band_buffer_pct` | L1173 | `float` | `0.1` | none | present |
| `volume_bins` | L1175 | `int` | `24` | none | absent: default applies |
| `volume_node_frac` | L1176 | `float` | `0.7` | none | absent: default applies |
| `breakout_avg_window` | L1178 | `int` | `20` | none | absent: default applies |
| `entry_proximity_pct` | L1179 | `float` | `1.0` | none | present |
| `volume_surge_mult` | L1180 | `float` | `1.5` | none | present |
| `weak_breakout_frac` | L1181 | `float` | `0.25` | none | absent: default applies |
| `retest_sl_buffer_pct` | L1182 | `float` | `0.3` | none | absent: default applies |
| `w_swing` | L1184 | `float` | `1.0` | none | present |
| `w_volume` | L1185 | `float` | `1.0` | none | present |
| `w_multi_tf` | L1186 | `float` | `1.0` | none | present |
| `w_prior_day` | L1187 | `float` | `1.0` | none | present |
| `w_round` | L1188 | `float` | `0.5` | none | present |
| `w_recency` | L1189 | `float` | `0.5` | none | present |
| `t_high` | L1190 | `float` | `5.0` | none | present |
| `t_med` | L1191 | `float` | `3.0` | none | present |
| `touch_cap` | L1192 | `int` | `4` | none | absent: default applies |
| `recency_window_days` | L1193 | `float` | `90.0` | none | absent: default applies |
| `recency_min_factor` | L1194 | `float` | `0.0` | none | absent: default applies |
| `max_queue` | L1196 | `int` | `256` | none | absent: default applies |
| `max_zones_logged` | L1197 | `int` | `12` | none | absent: default applies |
| `wait_for_retest_enabled` | L1200 | `bool` | `False` | none | present |
| `near_zone_buffer_pct` | L1201 | `float` | `0.3` | none | present |
| `require_confidence` | L1202 | `str` | `"HIGH"` | in {HIGH, MEDIUM, LOW} (L1236 to L1241) | present |
| `retest_timeout_sec` | L1203 | `float` | `1800.0` | none | present |
| `retest_max_away_pct` | L1204 | `float` | `1.0` | none | present |
| `confirm_strong_close_frac` | L1205 | `float` | `0.6` | none | present |
| `breakout_margin_pct` | L1206 | `float` | `0.0` | none | present |
| `onem_lookback_days` | L1207 | `int` | `2` | none | present |
| `zone_cache_ttl_sec` | L1208 | `float` | `1800.0` | none | present |
| `zone_rewarm_margin_sec` | L1209 | `float` | `300.0` | none | present |
| `retest_poll_interval_sec` | L1210 | `float` | `20.0` | none | present |
| `sl_buffer_pct` | L1211 | `float` | `0.2` | none | present |
| `intraday_anchors_enabled` | L1220 | `bool` | `False` | none | present |
| `anchor_intraday_interval` | L1221 | `str` | `"5minute"` | in {5minute, 15minute, 30minute} (L1225 to L1234) | present |
| `anchor_lookback_days` | L1222 | `int` | `1` | none | present |
| `orb_window_minutes` | L1223 | `int` | `15` | none | present |

#### RegimeConfig (L1258 to L1301)

- YAML: `system_config.yaml: regime`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "V3 03.02 — index-level Market Regime engine config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1269 | `bool` | `False` | none | present |
| `index_symbol` | L1270 | `str` | `"NIFTY 50"` | none | present |
| `index_token` | L1271 | `int` | `256265` | none | present |
| `daily_lookback_days` | L1272 | `int` | `400` | none | present |
| `intraday_interval` | L1273 | `str` | `"5minute"` | in {5minute, 15minute, 30minute} (L1287 to L1295) | present |
| `intraday_lookback_days` | L1274 | `int` | `1` | none | present |
| `ema_fast` | L1275 | `int` | `50` | ema_fast < ema_slow (L1297 to L1301) | present |
| `ema_slow` | L1276 | `int` | `200` | ema_fast < ema_slow (L1297 to L1301) | present |
| `slope_lookback` | L1277 | `int` | `5` | none | absent: default applies |
| `adx_period` | L1278 | `int` | `14` | none | present |
| `adx_trend_threshold` | L1279 | `float` | `25.0` | none | present |
| `atr_period` | L1280 | `int` | `14` | none | present |
| `vol_high_ratio` | L1281 | `float` | `1.3` | none | present |
| `vol_low_ratio` | L1282 | `float` | `0.7` | none | present |
| `trend_day_range_atr_mult` | L1283 | `float` | `1.5` | none | present |
| `swing_pivot_n` | L1284 | `int` | `3` | none | absent: default applies |
| `compute_interval_sec` | L1285 | `float` | `60.0` | none | present |

#### PortfolioAllocatorConfig (L1304 to L1381)

- YAML: `system_config.yaml: portfolio_allocator`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 5. Docstring: "V3 03.05 — Portfolio Allocator (ranked batch admission) config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `allocator_mode` | L1325 | `str` | `"off"` | in {off, shadow, enforce} (L1341 to L1346) | present |
| `enforce_scope` | L1326 | `str` | `"v3_only"` | in {v3_only, all} (L1348 to L1353) | present |
| `candle_interval_seconds` | L1329 | `float` | `60.0` | rejects v <= 0 (L1375 to L1376) | present |
| `drain_tail_seconds` | L1330 | `float` | `2.0` | 0 < v < candle_interval_seconds (L1377 to L1380) | present |
| `max_portfolio_deployment_pct` | L1334 | `Optional[float]` | `None` | null, or 0 < v <= 1 (L1355 to L1362) | present |
| `long_short_skew_max` | L1337 | `Optional[float]` | `None` | null, or 0.5 < v <= 1 (L1364 to L1371) | present |
| `regret_log_path` | L1339 | `str` | `"data_store/allocator/regret.jsonl"` | none | present |

#### V3ChainConfig (L1384 to L1513)

- YAML: `system_config.yaml: v3_chain`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 3. Docstring: "V3 Step 10 — the V3 DECISION CHAIN (enrichment + generic gates + 3-layer score"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `v3_chain_mode` | L1405 | `str` | `"off"` | in {off, shadow} (L1484 to L1491) | present |
| `atr30_period` | L1408 | `int` | `14` | rejects v <= 0 (L1502 to L1503) | present |
| `rr_floor` | L1409 | `float` | `2.0` | rejects v <= 0 (L1504 to L1505) | present |
| `sl_buffer_atr_mult` | L1410 | `float` | `0.20` | none | present |
| `htf_ema_period` | L1411 | `int` | `20` | none | present |
| `htf_swing_pivot_n` | L1412 | `int` | `3` | none | present |
| `confirm_min_body_frac` | L1416 | `float` | `0.50` | none | present |
| `confirm_volume_mult` | L1417 | `float` | `1.20` | none | present |
| `baseline_candles_per_session` | L1418 | `int` | `75` | none | present |
| `pullback_proximity_pct` | L1419 | `float` | `0.005` | none | present |
| `pullback_proximity_atr_mult` | L1420 | `float` | `0.50` | none | present |
| `hold_buffer_atr_mult` | L1421 | `float` | `0.20` | none | present |
| `retest_quality_atr_span` | L1423 | `float` | `0.75` | none | present |
| `level_touches_cap` | L1424 | `int` | `5` | none | present |
| `w_retest_quality` | L1428 | `float` | `15.0` | none | present |
| `w_confirmation_strength` | L1429 | `float` | `15.0` | none | present |
| `w_level_significance` | L1430 | `float` | `10.0` | none | present |
| `w_regime_preference` | L1432 | `float` | `8.0` | none | present |
| `w_sr_target_quality` | L1433 | `float` | `8.0` | none | present |
| `w_htf_alignment` | L1434 | `float` | `8.0` | none | present |
| `w_sector_strength` | L1435 | `float` | `8.0` | none | present |
| `w_momentum_position` | L1436 | `float` | `8.0` | none | present |
| `exec_budget` | L1439 | `float` | `20.0` | rejects v <= 0 (L1506 to L1507) | present |
| `w_exec_volume_surge` | L1440 | `float` | `15.0` | none | present |
| `w_exec_atr` | L1441 | `float` | `10.0` | none | present |
| `w_exec_time_of_day` | L1442 | `float` | `5.0` | none | present |
| `w_exec_spread` | L1443 | `float` | `5.0` | none | present |
| `confluence_combine` | L1449 | `str` | `"mean"` | in {mean, max} (L1493 to L1498) | present |
| `sr_target_quality_high` | L1452 | `float` | `1.0` | none | present |
| `sr_target_quality_medium` | L1453 | `float` | `0.6` | none | present |
| `sr_target_quality_low` | L1454 | `float` | `0.3` | none | present |
| `regime_pref_direction` | L1460 | `dict[str, float]` | `Field( default_factory=lambda: {"BULL": 1.0, "SIDEWAYS": 0.5, "BEAR": 0.0})` | none (any keys) | absent: default applies |
| `regime_pref_day_type` | L1462 | `dict[str, float]` | `Field( default_factory=lambda: {"TREND_DAY": 1.0, "UNDETERMINED": 0.5, "RANGE_DAY": 0.4})` | none (any keys) | absent: default applies |
| `regime_pref_volatility` | L1464 | `dict[str, float]` | `Field( default_factory=lambda: {"HIGH": 0.85, "NORMAL": 1.0, "LOW": 1.0})` | none (any keys) | absent: default applies |
| `min_pass_score` | L1470 | `int` | `60` | high > medium > min_pass (L1508 to L1512) | present |
| `medium_score_threshold` | L1471 | `int` | `65` | high > medium > min_pass (L1508 to L1512) | present |
| `high_score_threshold` | L1472 | `int` | `80` | high > medium > min_pass (L1508 to L1512) | present |
| `structure_intervals` | L1477 | `list[str]` | `Field( default_factory=lambda: ["day", "60minute", "30minute"])` | none | present |
| `fetch_lookback_days` | L1479 | `int` | `180` | none | present |
| `fetch_cache_ttl_sec` | L1480 | `float` | `1800.0` | none | present |
| `max_queue` | L1481 | `int` | `512` | none | present |
| `would_be_log_path` | L1482 | `str` | `"data_store/v3/would_be.jsonl"` | none | present |

#### WatchlistConfig (L1516 to L1574)

- YAML: `system_config.yaml: watchlist`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "V3 Step 10b — the PB-01 OVERNIGHT WATCHLIST + next-morning entry stage config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1531 | `bool` | `False` | none | present |
| `playbook_scanner` | L1535 | `str` | `"pb01_breakout_retest"` | none | present |
| `level_lookback_sessions` | L1538 | `int` | `20` | rejects v <= 0 (L1568 to L1569) | present |
| `capture_fetch_lookback_days` | L1539 | `int` | `60` | none | present |
| `entry_start` | L1542 | `str` | `"09:20"` | HH:MM parse (L1551 to L1559); entry_start < entry_end (L1563 to L1567) | present |
| `entry_end` | L1543 | `str` | `"11:00"` | HH:MM parse (L1551 to L1559); entry_start < entry_end (L1563 to L1567) | present |
| `entry_tf` | L1544 | `str` | `"5minute"` | none | present |
| `gap_guard_pct` | L1545 | `float` | `0.03` | 0 < v < 1 (L1570 to L1571) | present |
| `poll_interval_sec` | L1546 | `float` | `20.0` | rejects v <= 0 (L1572 to L1573) | present |
| `would_be_log_path` | L1549 | `str` | `"data_store/v3/pb01_would_be.jsonl"` | none | present |

#### StructureExitConfig (L1577 to L1607)

- YAML: `system_config.yaml: structure_exit`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "SNR-V2 Phase B — structure-aware exit (trail SL to structure + confirmed-break"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `structure_exit_enabled` | L1588 | `bool` | `False` | none | present |
| `sl_buffer_pct` | L1589 | `float` | `0.2` | none | present |
| `break_buffer_pct` | L1590 | `float` | `0.0` | none | present |
| `require_strong_close` | L1591 | `bool` | `True` | none | present |
| `break_strong_close_frac` | L1592 | `float` | `0.6` | 0 <= v <= 1 (L1602 to L1607) | present |
| `min_zone_confidence` | L1593 | `str` | `"HIGH"` | in {HIGH, MEDIUM, LOW} (L1595 to L1600) | present |

#### PaperConfig (L1610 to L1668)

- YAML: `system_config.yaml: paper`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 3. Docstring: "H-20 / ZA16a: paper-mode fill synthesis settings."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `auto_fill_delay_sec` | L1632 | `float` | `0.5` | rejects v < 0 or v > 10.0 (L1637 to L1646) | present |
| `ltp_gating_enabled` | L1633 | `bool` | `False` | none | present |
| `ltp_gating_max_wait_sec` | L1634 | `float` | `60.0` | rejects v < 0 or v > 25200 (L1648 to L1657) | present |
| `ltp_gating_poll_sec` | L1635 | `float` | `0.5` | rejects v <= 0 or v > 30 (L1659 to L1668) | present |

#### SmartTgtConfig (L1671 to L1701)

- YAML: `system_config.yaml: smart_tgt`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "BL-7b: deployment-wide defaults for SmartTgtManager trailing behavior."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1687 | `bool` | REQUIRED | none | present |
| `trigger_pct` | L1688 | `float` | REQUIRED | 0 < v < 1 (L1693 to L1701) | present |
| `step_pct` | L1689 | `float` | REQUIRED | 0 < v < 1 (L1693 to L1701) | present |
| `volume_dependent_trails` | L1690 | `bool` | REQUIRED | none | present |
| `max_modify_failures` | L1691 | `int` | `3` | none | present |

#### SlippageTier (L1704 to L1710)

- YAML: `system_config.yaml: entry_gate.slippage_control.tiers[]`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "One price band of the tiered entry-slippage guard. `price < max_price`"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `max_price` | L1709 | `float` | REQUIRED | none | present in 4 of 4 instances |
| `max_slippage_rs` | L1710 | `float` | REQUIRED | none | present in 4 of 4 instances |

#### SlippageOverridesConfig (L1713 to L1746)

- YAML: `system_config.yaml: entry_gate.slippage_control.overrides`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "Phase 3a — MANUAL override hierarchy for the sl_fraction entry-slippage"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1731 | `bool` | `True` | none | present |
| `by_price_band` | L1732 | `dict[str, float]` | `Field(default_factory=dict)` | each value coerced to `float` by the type, then 0.0 < v <= 1.0 (L1736 to L1746); INTERPRETATION: the bool test at L1740 cannot fire on the load path, because pydantic has already coerced the value, so a YAML `true` loads as 1.0 and a YAML `false` (0.0) fails only the range; keys not checked here | present |
| `by_strategy` | L1733 | `dict[str, float]` | `Field(default_factory=dict)` | each value coerced to `float` by the type, then 0.0 < v <= 1.0 (L1736 to L1746); INTERPRETATION: the bool test at L1740 cannot fire on the load path, because pydantic has already coerced the value, so a YAML `true` loads as 1.0 and a YAML `false` (0.0) fails only the range; keys not checked here | present |
| `by_symbol` | L1734 | `dict[str, float]` | `Field(default_factory=dict)` | each value coerced to `float` by the type, then 0.0 < v <= 1.0 (L1736 to L1746); INTERPRETATION: the bool test at L1740 cannot fire on the load path, because pydantic has already coerced the value, so a YAML `true` loads as 1.0 and a YAML `false` (0.0) fails only the range; keys not checked here | present |

#### SlippageControlConfig (L1749 to L1784)

- YAML: `system_config.yaml: entry_gate.slippage_control`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "Entry-slippage abort tolerance — calibratable without code changes. The"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1765 | `bool` | `False` | none | present |
| `mode` | L1766 | `str` | `"sl_fraction"` | in {sl_fraction, flat_tiers, pct} (L1777 to L1784) | present |
| `max_slippage_fraction` | L1767 | `float` | `0.22` | none (contrast: overrides are range-checked) | present |
| `absolute_cap_rs` | L1768 | `float` | `5.0` | none | present |
| `tiers` | L1769 | `list[SlippageTier]` | `Field(default_factory=list)` | none (no ordering or non-empty check) | present |
| `default_max_slippage_rs` | L1770 | `float` | `2.0` | none | present |
| `also_apply_pct_check` | L1771 | `bool` | `True` | none | present |
| `hard_max_slippage_rs` | L1772 | `float` | `10.0` | none | present |
| `overrides` | L1773 | `SlippageOverridesConfig` | `Field( # Phase 3a: per symbol/strategy/band fraction default_factory=SlippageOverridesConfig )` | nested model | present |

#### EntryGateConfig (L1787 to L1813)

- YAML: `system_config.yaml: entry_gate`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-025: EntryGate slippage protection config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `slippage_buffer` | L1803 | `float` | REQUIRED | none | present |
| `max_entry_slippage_pct` | L1804 | `float` | `1.0` | none | present |
| `max_spread_pct` | L1805 | `float` | `0.5` | none | present |
| `min_depth_qty` | L1806 | `int` | `500` | none | present |
| `liquidity_check_enabled` | L1807 | `bool` | `True` | none | present |
| `min_effective_rr` | L1808 | `float` | `1.0` | none | present |
| `min_pending_rr` | L1809 | `float` | `0.0` | none | present |
| `circuit_proximity_reject_enabled` | L1810 | `bool` | `True` | none | present |
| `slippage_control` | L1811 | `SlippageControlConfig` | `Field( # entry-slippage abort (sl_fraction/flat_tiers/pct) default_factory=SlippageControlConfig )` | nested model | present |

#### LiveFeedConfig (L1816 to L1821)

- YAML: `system_config.yaml: live_feed`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-134 Item 37: WebSocket reconnect hardening config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `max_reconnect_attempts` | L1819 | `int` | `10` | none | present |
| `reconnect_backoff_base_seconds` | L1820 | `int` | `1` | none | present |
| `reconnect_backoff_max_seconds` | L1821 | `int` | `30` | none | present |

#### FnoBanConfig (L1824 to L1835)

- YAML: `system_config.yaml: fno_ban`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-136 Item 44 + 22-Jun-2026 endpoint fix: F&O ban list fetch config."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `url` | L1834 | `str` | `"https://nsearchives.nseindia.com/content/fo/fo_secban.csv"` | none | present |
| `fail_closed` | L1835 | `bool` | `False` | none | present |

#### StrategyCircuitBreakerConfig (L1838 to L1844)

- YAML: `system_config.yaml: strategy_circuit_breaker`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-130 (Item 6): Intraday strategy circuit breaker settings."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1841 | `bool` | `True` | none | present |
| `loss_multiplier` | L1842 | `float` | `2.0` | none | present |
| `cutoff_time` | L1843 | `str` | `"12:00"` | none (no HH:MM check) | present |
| `lookback_days` | L1844 | `int` | `10` | none | present |

#### CircuitBreakerConfig (L1847 to L1862)

- YAML: `system_config.yaml: circuit_breaker`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-128 (Fix C): Position-level circuit breaker settings."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `partial_fill_timeout_minutes` | L1860 | `int` | `5` | none | present |
| `force_close_time` | L1861 | `str` | `"15:15"` | none (no HH:MM check) | present |
| `max_api_failures` | L1862 | `int` | `3` | none | present |

#### DriftHandlerConfig (L1865 to L1918)

- YAML: `system_config.yaml: drift_handler`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 3. Docstring: "BL-2: CapitalDriftHandler escalation thresholds (absolute rupee values)."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `log_only_threshold_rs` | L1884 | `float` | `250.0` | rejects v <= 0 (L1889 to L1895); log_only < soft_kill < hard_kill (L1906 to L1918) | present |
| `soft_kill_threshold_rs` | L1885 | `float` | `1_000.0` | rejects v <= 0 (L1889 to L1895); log_only < soft_kill < hard_kill (L1906 to L1918) | present |
| `hard_kill_threshold_rs` | L1886 | `float` | `2_500.0` | rejects v <= 0 (L1889 to L1895); log_only < soft_kill < hard_kill (L1906 to L1918) | present |
| `consecutive_cycles_before_escalate` | L1887 | `int` | `3` | >= 1 (L1897 to L1904) | present |

#### BrokerConfig (L1921 to L1927)

- YAML: `system_config.yaml: broker`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-133 Item 28/29: multi-broker + multi-account support."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `primary` | L1924 | `str` | `"zerodha"` | none | present |
| `fallback` | L1925 | `str` | `"angelone"` | none | present |
| `fallback_enabled` | L1926 | `bool` | `False` | none | present |
| `multi_account_mode` | L1927 | `bool` | `False` | none | present |

#### TgtRetryConfig (L1930 to L1961)

- YAML: `system_config.yaml: tgt_retry`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 3. Docstring: "Task (2026-06-19): standalone TGT retry. A LIMIT_TRIPLE trade whose SL is"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `enabled` | L1937 | `bool` | `True` | none | present |
| `poll_interval_sec` | L1938 | `int` | `30` | >= 1 (L1942 to L1947) | present |
| `max_attempts` | L1939 | `int` | `5` | >= 1 (L1949 to L1954) | present |
| `backoff_base_sec` | L1940 | `int` | `30` | >= 1 (L1956 to L1961) | present |

#### EodReconcileConfig (L1964 to L1973)

- YAML: `system_config.yaml: eod_reconcile`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "P1 (02-Jul): broker-authoritative EOD reconcile (scripts/eod_broker_reconcile.py)."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `authoritative` | L1972 | `bool` | `False` | none | present |
| `pnl_tolerance` | L1973 | `float` | `100.0` | none | present |

#### EodCleanupConfig (L1976 to L1984)

- YAML: `system_config.yaml: eod_cleanup`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "EOD hygiene prune (scripts/eod_cleanup.py step 4). `signal_retention_days` = keep-window"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `signal_retention_days` | L1984 | `int` | `Field(default=90, ge=1)` | `Field(ge=1)` (L1984) | present |

#### SystemConfig (L1987 to L2086)

- YAML: `system_config.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `broker` | L1989 | `BrokerConfig` | `BrokerConfig()` | nested model (default is an instance built at class definition) | present |
| `trading_hours` | L1990 | `TradingHoursConfig` | REQUIRED | nested model | present |
| `signal_queue` | L1991 | `SignalQueueConfig` | REQUIRED | nested model | present |
| `special_sessions` | L1992 | `dict[str, dict[str, str]]` or `None` (a union) | `None` | none beyond the type: any string keys, inner mapping of any string keys to string values (no date, key-set or HH:MM check) | present (value `null`) |
| `excluded_symbols` | L1993 | `list[str]` | `[]` | none | present |
| `mis_filter` | L1994 | `MisFilterConfig` | `Field(default_factory=MisFilterConfig)` | nested model | present |
| `product_map` | L1995 | `dict[str, dict[str, str]]` | REQUIRED | none beyond the type (any broker keys, any intent keys, any string values, empty string accepted) | present |
| `clock` | L1996 | `ClockConfig` | REQUIRED | nested model | present |
| `order_monitor` | L1997 | `OrderMonitorConfig` | REQUIRED | nested model | present |
| `capital` | L1998 | `CapitalConfig` | REQUIRED | nested model | present |
| `position_sizing` | L1999 | `PositionSizingConfig` | REQUIRED | nested model | present |
| `risk` | L2000 | `RiskConfig` | REQUIRED | nested model | present |
| `kill_switch` | L2001 | `KillSwitchConfig` | REQUIRED | nested model | present |
| `webhook` | L2002 | `WebhookConfig` | REQUIRED | nested model | present |
| `signal_processor` | L2003 | `SignalProcessorConfig` | REQUIRED | nested model | present |
| `eod_squareoff` | L2004 | `EodSquareoffConfig` | REQUIRED | nested model | present |
| `alerts` | L2005 | `AlertsConfig` | REQUIRED | nested model | present |
| `logging` | L2006 | `LoggingConfig` | REQUIRED | nested model | present |
| `order_reconciler` | L2007 | `OrderReconcilerConfig` | REQUIRED | nested model | present |
| `eod_reconcile` | L2008 | `EodReconcileConfig` | `Field(default_factory=EodReconcileConfig)` | nested model | present |
| `eod_cleanup` | L2009 | `EodCleanupConfig` | `Field(default_factory=EodCleanupConfig)` | nested model | present |
| `tgt_retry` | L2010 | `TgtRetryConfig` | `Field(default_factory=TgtRetryConfig)` | nested model | present |
| `shadow_tracker` | L2011 | `ShadowTrackerConfig` | REQUIRED | nested model | present |
| `sr_detector` | L2012 | `SRDetectorConfig` | `Field(default_factory=SRDetectorConfig)` | nested model | present |
| `regime` | L2013 | `RegimeConfig` | `Field(default_factory=RegimeConfig)` | nested model | present |
| `portfolio_allocator` | L2014 | `PortfolioAllocatorConfig` | `Field(default_factory=PortfolioAllocatorConfig)` | nested model | present |
| `v3_chain` | L2015 | `V3ChainConfig` | `Field(default_factory=V3ChainConfig)` | nested model | present |
| `watchlist` | L2016 | `WatchlistConfig` | `Field(default_factory=WatchlistConfig)` | nested model | present |
| `structure_exit` | L2017 | `StructureExitConfig` | `Field(default_factory=StructureExitConfig)` | nested model | present |
| `smart_tgt` | L2018 | `SmartTgtConfig` | REQUIRED | nested model | present |
| `entry_gate` | L2019 | `EntryGateConfig` | REQUIRED | nested model | present |
| `paper` | L2020 | `PaperConfig` | REQUIRED | nested model | present |
| `drift_handler` | L2021 | `DriftHandlerConfig` | REQUIRED | nested model | present |
| `circuit_breaker` | L2022 | `CircuitBreakerConfig` | `CircuitBreakerConfig()` | nested model (default is an instance built at class definition) | present |
| `strategy_circuit_breaker` | L2023 | `StrategyCircuitBreakerConfig` | `StrategyCircuitBreakerConfig()` | nested model (default is an instance built at class definition) | present |
| `live_feed` | L2024 | `LiveFeedConfig` | `LiveFeedConfig()` | nested model (default is an instance built at class definition) | present |
| `fno_ban` | L2025 | `FnoBanConfig` | `FnoBanConfig()` | nested model (default is an instance built at class definition) | present |
| `scanner_check_delay_sec` | L2026 | `float` | `5.0` | none | present |
| `slippage_bands` | L2027 | `list[str]` | `Field( # price bands for trade_slippage_log.price_band (v31) default_factory=lambda: ["0-100", "100-200", "200-300", "300-500", "500-1000", "1000+"] )` | none (no format check) | present |
| `force_intraday_only` | L2030 | `bool` | `True` | none at field level; at load, rejected if true while `trade_type` is `DELIVERY` (auditor rule A1, a BLOCK, `core/config_auditor.py` L196 to L203, raised by `raise_if_blocked()` at L2080) | present |
| `delivery_enabled` | L2037 | `bool` | `False` | none; not read during `load_all`: the startup audit (L2075, groups ACG, no strategies) skips the only rule that reads it, A5 (`core/config_auditor.py` L266 to L297, which runs only `if strategies:`); A5 runs in `main.py` L3459 to L3460 and in the pre-flight, outside this module | present |
| `trade_type` | L2044 | `str` | `"INTRADAY"` | in {INTRADAY, DELIVERY, BOTH} (L2046 to L2054); rejected at load if `force_intraday_only` is true and `trade_type` is `DELIVERY` (rule A1, `core/config_auditor.py` L196 to L203, raised by L2080) | present |

#### FuturesRatesConfig (L2094 to L2098)

- YAML: `broker_costs.yaml: zerodha.futures`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-027: Futures-specific rates."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `stt_pct` | L2097 | `float` | REQUIRED | none | present |
| `stamp_duty_buy_pct` | L2098 | `float` | REQUIRED | none | present |

#### OptionsBuyRatesConfig (L2101 to L2105)

- YAML: `broker_costs.yaml: zerodha.options_buy`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-027: Options buy-side rates."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `stt_pct` | L2104 | `float` | REQUIRED | none | present |
| `stamp_duty_pct` | L2105 | `float` | REQUIRED | none | present |

#### OptionsSellRatesConfig (L2108 to L2112)

- YAML: `broker_costs.yaml: zerodha.options_sell`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "FIX-027: Options sell-side rates."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `stt_pct` | L2111 | `float` | REQUIRED | none | present |
| `stamp_duty_pct` | L2112 | `float` | REQUIRED | none | present |

#### ZerodhaRatesConfig (L2115 to L2128)

- YAML: `broker_costs.yaml: zerodha`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `brokerage_flat_intraday` | L2117 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159); not both brokerage fields 0 (L2161 to L2165) | present |
| `brokerage_pct_intraday` | L2118 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159); not both brokerage fields 0 (L2161 to L2165) | present |
| `stt_sell_pct` | L2119 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `stt_cnc_pct` | L2120 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `exchange_txn_pct` | L2121 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `gst_pct` | L2122 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159); != 0 (L2166 to L2167) | present |
| `sebi_pct` | L2123 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `stamp_duty_mis_buy_pct` | L2124 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `stamp_duty_cnc_buy_pct` | L2125 | `float` | REQUIRED | >= 0 (BrokerCostsConfig L2140 to L2159) | present |
| `futures` | L2126 | `FuturesRatesConfig` | REQUIRED | nested model (rates not range-checked) | present |
| `options_buy` | L2127 | `OptionsBuyRatesConfig` | REQUIRED | nested model (rates not range-checked) | present |
| `options_sell` | L2128 | `OptionsSellRatesConfig` | REQUIRED | nested model (rates not range-checked) | present |

#### BrokerCostsConfig (L2131 to L2168)

- YAML: `broker_costs.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "FIX-131 Item 25: All rate fields must be explicitly defined in YAML."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `zerodha` | L2138 | `ZerodhaRatesConfig` | REQUIRED | nested model; model validator L2140 to L2168 | present |

#### TokenBucketConfig (L2176 to L2179)

- YAML: `broker_limits.yaml: order`; `broker_limits.yaml: quote`; `broker_limits.yaml: historical`; `broker_limits.yaml: margins`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `burst` | L2178 | `int` | REQUIRED | none | present in 4 of 4 instances |
| `rate_per_sec` | L2179 | `int` | REQUIRED | none | present in 4 of 4 instances |

#### TimeoutsConfig (L2182 to L2185)

- YAML: `broker_limits.yaml: timeouts`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `connect_sec` | L2184 | `int` | REQUIRED | none | present |
| `read_sec` | L2185 | `int` | REQUIRED | none | present |

#### RateLimitBackoffConfig (L2188 to L2242)

- YAML: `broker_limits.yaml: rate_limit_backoff`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 4. Docstring: "BL-6: exponential backoff applied to rate_limiter.penalize() when the"

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `initial_delay_sec` | L2203 | `float` | `0.2` | rejects v < 0 (L2209 to L2214); max_delay_sec >= initial_delay_sec (L2235 to L2242) | present |
| `max_delay_sec` | L2204 | `float` | `5.0` | rejects v < 0 (L2209 to L2214); >= initial_delay_sec (L2235 to L2242) | present |
| `max_placer_retries` | L2205 | `int` | `3` | rejects v < 0 (L2226 to L2233) | present |
| `multiplier` | L2206 | `float` | `2.0` | rejects v < 1.0 (L2216 to L2224) | present |
| `jitter_sec` | L2207 | `float` | `0.05` | rejects v < 0 (L2209 to L2214) | present |

#### BrokerLimitsConfig (L2245 to L2256)

- YAML: `broker_limits.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `order` | L2247 | `TokenBucketConfig` | REQUIRED | nested model | present |
| `quote` | L2248 | `TokenBucketConfig` | REQUIRED | nested model | present |
| `historical` | L2249 | `TokenBucketConfig` | REQUIRED | nested model | present |
| `margins` | L2250 | `TokenBucketConfig` | REQUIRED | nested model | present |
| `backoff_sequence_sec` | L2251 | `list[int]` | REQUIRED | none (no non-empty, positivity or ordering check) | present |
| `timeouts` | L2252 | `TimeoutsConfig` | REQUIRED | nested model | present |
| `rate_limit_backoff` | L2254 | `RateLimitBackoffConfig` | `Field( default_factory=RateLimitBackoffConfig )` | nested model | present |

#### SlippageTierConfig (L2264 to L2266)

- YAML: `slippage_model.yaml: tiers.<key>`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `slippage_bps` | L2266 | `int` | REQUIRED | none | present in 3 of 3 instances |

#### SlippageConfig (L2269 to L2272)

- YAML: `slippage_model.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `tiers` | L2271 | `dict[str, SlippageTierConfig]` | REQUIRED | none (empty mapping accepted) | present |
| `default_tier` | L2272 | `str` | REQUIRED | none (not checked against `tiers` keys) | present |

#### ScoringStepsConfig (L2280 to L2292)

- YAML: `scoring_weights.yaml: steps`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "One integer weight per screener step. All 10 required (P9b)."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `volume_surge` | L2283 | `int` | REQUIRED | none | present |
| `vwap_position` | L2284 | `int` | REQUIRED | none | present |
| `atr_filter` | L2285 | `int` | REQUIRED | none | present |
| `rsi_range` | L2286 | `int` | REQUIRED | none | present |
| `price_action` | L2287 | `int` | REQUIRED | none | present |
| `sector_strength` | L2288 | `int` | REQUIRED | none | present |
| `time_of_day` | L2289 | `int` | REQUIRED | none | present |
| `spread_check` | L2290 | `int` | REQUIRED | none | present |
| `circuit_check` | L2291 | `int` | REQUIRED | none | present |
| `signal_age` | L2292 | `int` | REQUIRED | none | present |

#### ScoringConfig (L2295 to L2339)

- YAML: `scoring_weights.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `steps` | L2297 | `ScoringStepsConfig` | REQUIRED | nested model | present |
| `min_pass_score` | L2298 | `int` | REQUIRED | high > medium > min_pass (L2326 to L2333) | present |
| `high_score_threshold` | L2304 | `int` | REQUIRED | high > medium > min_pass (L2326 to L2333) | present |
| `medium_score_threshold` | L2305 | `int` | REQUIRED | high > medium > min_pass (L2326 to L2333) | present |
| `v3_hardgate_mode` | L2312 | `str` | `"off"` | in {off, shadow, enforce} (L2319 to L2324) | present |
| `v3_gate_steps` | L2313 | `list[str]` | `Field(default_factory=lambda: ["circuit_check", "signal_age"])` | none (not checked against step names) | present |
| `v3_freshness_max_sec` | L2314 | `float` | `60.0` | none | present |
| `v3_min_pass_score` | L2315 | `int` | `50` | v3 high > v3 medium > v3 min_pass (L2334 to L2338) | present |
| `v3_high_score_threshold` | L2316 | `int` | `75` | v3 high > v3 medium > v3 min_pass (L2334 to L2338) | present |
| `v3_medium_score_threshold` | L2317 | `int` | `56` | v3 high > v3 medium > v3 min_pass (L2334 to L2338) | present |

#### ScannerEntry (L2347 to L2371)

- YAML: `scan_webhook_map.yaml: scanners.<key>`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 2. Docstring: "One scanner → strategy mapping entry (S14 format)."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `strategy` | L2350 | `str` | REQUIRED | none (not checked against strategy files in this module) | present in 16 of 16 instances |
| `chartink_url` | L2351 | `str` | REQUIRED | must start with http:// or https:// (L2359 to L2364) | present in 16 of 16 instances |
| `scanner_type` | L2357 | `str` | `"intraday"` | in {intraday, eod} (L2366 to L2371) | present in 1 of 16 instances |

#### ScanWebhookMapConfig (L2374 to L2377)

- YAML: `scan_webhook_map.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "Maps Chartink scanner names to ScannerEntry (strategy + chartink_url)."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `scanners` | L2377 | `dict[str, ScannerEntry]` | REQUIRED | none (empty mapping accepted) | present |

#### ChartinkScannersConfig (L2385 to L2388)

- YAML: `chartink_scanners.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "Canonical Chartink scanner URLs for pre-flight health check."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `scanners` | L2388 | `dict[str, str]` | REQUIRED | none (no URL check; empty mapping accepted) | present |

#### HolidayEntry (L2395 to L2408)

- YAML: `nse_holidays_<year>.yaml: holidays[]`. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 1. Docstring: "One NSE holiday entry with date and descriptive name."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `date` | L2398 | `_date` | REQUIRED | before-validator L2401 to L2408: str -> `date.fromisoformat`; a `date` instance passes; anything else ValueError | present in 15 of 15 instances |
| `name` | L2399 | `str` | REQUIRED | none | present in 15 of 15 instances |

#### NseHolidaysConfig (L2411 to L2413)

- YAML: `nse_holidays_<year>.yaml` (top level). Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0.

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `holidays` | L2413 | `list[HolidayEntry]` | REQUIRED | none (empty list accepted; no uniqueness, weekday or year check) | present |

#### AppConfig (L2420 to L2434)

- YAML: none; the container built by `load_all` at L2516. Extra-key policy: `ConfigDict(extra="forbid")` (forbid). Validators: 0. Docstring: "Holds all validated sub-configs and per-file SHA-256 hashes."

| Field | Line | Type | Default | Constraints enforced | Baseline file |
|---|---|---|---|---|---|
| `system` | L2426 | `SystemConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `broker_costs` | L2427 | `BrokerCostsConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `broker_limits` | L2428 | `BrokerLimitsConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `slippage` | L2429 | `SlippageConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `scoring` | L2430 | `ScoringConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `scan_webhook_map` | L2431 | `ScanWebhookMapConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `chartink_scanners` | L2432 | `ChartinkScannersConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `nse_holidays` | L2433 | `NseHolidaysConfig` | REQUIRED | nested model | n/a (built by load_all) |
| `file_hashes` | L2434 | `dict[str, str]` | REQUIRED | none (built by load_all, not read from YAML) | n/a (built by load_all) |

## 3. Load flow

### 3.1 Entry points

| Entry point | Lines | Role |
|---|---|---|
| `load_all(config_dir: Path = Path("config")) -> AppConfig` | L2457 to L2516 | FACT: the only loading function in the module. Reads, hashes, parses and validates the eight registered files and returns one `AppConfig`. |
| the model classes themselves | table 1.2 | FACT: public; consumers also construct some directly from code defaults, without any file: `V3ChainConfig()` (`main.py` L3722, if `getattr(app_config.system, "v3_chain", None)` at L3472 gave `None`; INTERPRETATION: after a successful `load_all` it never does, because the field has a default, L2015), `EodCleanupConfig()` (`scripts/eod_cleanup.py` L64, after a failed `load_all`), `RateLimitBackoffConfig()` (`broker/zerodha_adapter.py` L430, `orders/order_placer.py` L627, when no instance is passed). |
| `SmtpConfig.resolved_password()` | L935 to L949 | FACT: a method, not a loader; reads one environment variable when called (section 5). |

FACT: there is no reload function, no `load_one`/per-file loader, no cached accessor and no singleton (section 6).

### 3.2 `load_all`, step by step

| Step | Lines | What the code does | Label |
|---|---|---|---|
| 1. Directory | L2457, docstring L2466 to L2468 | Taken only from the argument. Default `Path("config")`, relative to the process working directory. The module reads no environment variable and no command line for it. | FACT |
| 1a. Directory at the main caller | `main.py` L192 to L195, L2099 | `--config PATH` ("Override config/ directory path"), else `Path("config")`. Other callers: section 7.1. | FACT |
| 2. State | L2477 to L2478 | Two local dicts: `validated` (AppConfig key -> model) and `hashes` (file name -> digest). | FACT |
| 3. Order | L2480, L2441 to L2450 | Fixed registry order: `system_config.yaml`, `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scoring_weights.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml`, `nse_holidays_<import year>.yaml`. | FACT |
| 4. Path | L2481 | `config_dir / filename`: the bare file name directly inside the directory; no subdirectory, glob, search path or include. | FACT. INTERPRETATION: a `str` argument raises `TypeError` here (`str / str`), see 7.1 `scripts/sr_level_export.py`. |
| 5. Presence | L2483 to L2488 | `if not path.is_file()`: raise `ConfigMissingError(f"Required config file not found: {filename}", file=filename, path=str(path))`. Every one of the eight entries is required; the registry has no optional flag. | FACT. INTERPRETATION: a directory or a broken symbolic link gives `False`; a parent directory without search permission makes `is_file()` itself raise `PermissionError`, unwrapped, not `ConfigMissingError` (CPython 3.13 `pathlib`, read locally; other versions may differ, and the production Python version is UNKNOWN / NOT ESTABLISHED). |
| 6. Read | L2490 | `path.read_bytes()`: the whole file as raw bytes. | FACT. INTERPRETATION: a read error (for example a permission error) propagates as the `OSError` subclass, not wrapped. |
| 7. Hash | L2491 | `hashlib.sha256(raw_bytes).hexdigest()` stored as `hashes[filename]`. Algorithm SHA-256; input the raw bytes exactly as on disk (no decoding, no newline or BOM normalisation, no canonical YAML form); output lowercase hex; key the bare file name (not the path, not the AppConfig key); insertion order = registry order; computed BEFORE parsing. | FACT (code). INTERPRETATION: a CRLF, BOM, comment or whitespace change alters the hash although the parsed values are the same. |
| 8. Parse | L2493 to L2500 | `yaml.safe_load(raw_bytes)`; any `yaml.YAMLError` becomes `ConfigSchemaError(f"YAML parse error in {filename}: {exc}", file=filename, path=str(path))` chained `from exc`. | FACT. Verified on synthetic text with PyYAML 6.0.3: bytes are decoded as UTF-8 (a UTF-8 or UTF-16 BOM is accepted); YAML 1.1 typing applies (section 4). |
| 9. Normalise | L2502 to L2504 | `None` (empty file or comments only) becomes `{}`. No other normalisation: no key case-folding, no environment expansion, no time parsing, no include. | FACT |
| 10. Validate | L2506 to L2514 | `schema_cls.model_validate(data)`; a pydantic `ValidationError` becomes `ConfigSchemaError("Schema validation failed for {filename}", file=filename, error_count=exc.error_count(), errors=exc.errors())` chained `from exc`. All validators run here, including two with side effects: the MIS timing check (lazy import, L122 to L137) and the configuration auditor with WARNING log lines (L2056 to L2086). | FACT |
| 11. Return | L2516 | `AppConfig(**validated, file_hashes=hashes)`, outside any `try`. | FACT. INTERPRETATION: the already-built sub-models are accepted as they are (pydantic 2 default `revalidate_instances="never"`); a `ValidationError` here would escape unwrapped, but cannot arise with the registry as written (its eight keys equal `AppConfig`'s eight model fields, L2442 to L2449 against L2426 to L2433). |

FACT: the loop stops at the first failing file. Files before it were read, hashed, parsed and validated, then discarded; files after it are not read. No partial `AppConfig` is returned (CL2, L14 to L15).

### 3.3 Validation order inside `system_config.yaml` (INTERPRETATION of pydantic 2)

1. Each field in declaration order (L1989 to L2044); nested models validate their own fields, then their own "after" model validators (for `trading_hours`: the MIS timing check L109 first, then the window-ordering check L139; for `capital`: the leverage check L389 after `leverage_map` and `leverage_safety` validated themselves).
2. `SystemConfig.trade_type`'s field validator (L2046 to L2054).
3. Only if every field of `SystemConfig` validated: `_cross_field_sanity_checks` (L2056 to L2086), which imports `core.config_auditor` (A02, another part), runs `audit_system_config(self)` with the startup groups `"ACG"` (`core/config_auditor.py` L811, L814 to L819), raises on any BLOCK (`raise_if_blocked` at L2080, `core/config_auditor.py` L142 to L146, a `ConfigContradictionError(ValueError)`) and only then, if nothing was blocked, logs every WARN with `logging.getLogger("config_sanity").warning("config_sanity: %s", ...)` (L2074, L2083 to L2084).

Consequence (INTERPRETATION): a file with any field-level error never reaches the auditor, so its BLOCK and WARN findings are not produced for that load. FACT: a load stopped by a BLOCK logs no WARN finding, because L2080 raises before the WARN loop (L2083 to L2084).

### 3.4 Normalisation and coercion this module applies

| What | Lines | Label |
|---|---|---|
| Empty document to `{}` | L2503 to L2504 | FACT |
| `HolidayEntry.date`: string to `date` with `date.fromisoformat`; a `date` object passes; anything else rejected | L2401 to L2408 | FACT |
| Leverage values returned as `float(v)` | L242, L247 | FACT |
| HH:MM strings are checked but kept as strings (the validators return `self` or `v` unchanged); consumers parse them again (`main.py` `_parse_hhmm` L613 to L616; A01 C11) | L158 to L189, L1551 to L1574 | FACT |
| Allowed-value sets are case-sensitive (for example `MARKET`, `observe`, `off`, `intraday`) | each `in {...}` validator | FACT |
| Lax type coercion by pydantic (numeric strings to numbers, whole floats to int, "true"/"yes"/1 and similar to bool; no number, bool or date to str) | none in this module; library default | INTERPRETATION |

### 3.5 Code defaults that apply at the baseline (keys absent from the files)

FACT (static key comparison): 38 key occurrences are absent from the baseline files, so the code default applies: 23 keys of `system_config.yaml` and `scanner_type` in 15 of the 16 entries of `scan_webhook_map.yaml`, that is 24 distinct schema keys. No unknown key and no missing required key was found. Whether the defaults were in force in production is UNKNOWN / NOT ESTABLISHED.

| Key (file: path) | Default (line) |
|---|---|
| `system_config.yaml: position_sizing.flat_value_rs` | `None` (L480) |
| `system_config.yaml: signal_processor.atr_fallback_mode` | `"WARN"` (L572) |
| `system_config.yaml: alerts.watcher_interval_sec` | `60` (L1108) |
| `system_config.yaml: alerts.watcher_heartbeat_path` | `None` (L1109) |
| `system_config.yaml: alerts.respawn_restart_delta_threshold` | `3` (L1112) |
| `system_config.yaml: alerts.respawn_rate_per_hour_threshold` | `6.0` (L1113) |
| `system_config.yaml: alerts.smtp.password` | `""` (L890) |
| `system_config.yaml: sr_detector.pivot_n_by_tf` | `{}` (L1169) |
| `system_config.yaml: sr_detector.volume_bins` | `24` (L1175) |
| `system_config.yaml: sr_detector.volume_node_frac` | `0.7` (L1176) |
| `system_config.yaml: sr_detector.breakout_avg_window` | `20` (L1178) |
| `system_config.yaml: sr_detector.weak_breakout_frac` | `0.25` (L1181) |
| `system_config.yaml: sr_detector.retest_sl_buffer_pct` | `0.3` (L1182) |
| `system_config.yaml: sr_detector.touch_cap` | `4` (L1192) |
| `system_config.yaml: sr_detector.recency_window_days` | `90.0` (L1193) |
| `system_config.yaml: sr_detector.recency_min_factor` | `0.0` (L1194) |
| `system_config.yaml: sr_detector.max_queue` | `256` (L1196) |
| `system_config.yaml: sr_detector.max_zones_logged` | `12` (L1197) |
| `system_config.yaml: regime.slope_lookback` | `5` (L1277) |
| `system_config.yaml: regime.swing_pivot_n` | `3` (L1284) |
| `system_config.yaml: v3_chain.regime_pref_direction` | `{"BULL": 1.0, "SIDEWAYS": 0.5, "BEAR": 0.0}` (L1460 to L1461) |
| `system_config.yaml: v3_chain.regime_pref_day_type` | `{"TREND_DAY": 1.0, "UNDETERMINED": 0.5, "RANGE_DAY": 0.4}` (L1462 to L1463) |
| `system_config.yaml: v3_chain.regime_pref_volatility` | `{"HIGH": 0.85, "NORMAL": 1.0, "LOW": 1.0}` (L1464 to L1465) |
| `scan_webhook_map.yaml: scanners.<name>.scanner_type`, 15 of the 16 entries (including the three `positional_*` scanners) | `"intraday"` (L2357) |

### 3.6 Further specific areas

| Area | Facts |
|---|---|
| Holiday file | Name `nse_holidays_{_date.today().year}.yaml`, the year taken from the host-local date at module import (L2449; section 9.1). Required like every registry entry (L2483 to L2488). Only that one file is loaded; no other year is read. Schema: `NseHolidaysConfig.holidays: list[HolidayEntry]` (L2413), each `{date, name}` (L2398 to L2399), `extra="forbid"`. Dates: an unquoted ISO date is already a `date` from PyYAML (verified), a quoted one is parsed with `date.fromisoformat` (L2404 to L2405). No check of uniqueness, weekday, or that the dates fall in the year of the file name; an empty list passes. Baseline: only `config/nse_holidays_2026.yaml` exists in `config/` (FACT, listing); 15 entries, all keys present (static check). |
| Special sessions | `special_sessions`, typed `dict[str, dict[str, str]]` or `None` (a union), default `None` (L1992); no validator anywhere in this module or in `core/config_auditor.py` (grep). Details and YAML typing: section 9.3. |
| Broker limits | `BrokerLimitsConfig` (L2245 to L2256): four required token buckets `order`, `quote`, `historical`, `margins` (`burst: int`, `rate_per_sec: int`, no range checks, L2176 to L2179), required `backoff_sequence_sec: list[int]` (no check), required `timeouts` (`connect_sec`, `read_sec`, no check), and `rate_limit_backoff` defaulted (L2254 to L2256) with five validated fields (L2188 to L2242). Baseline: all keys present. Consumer: `broker/rate_limiter.py` L40, L150 (A04). |
| Product map | `product_map: dict[str, dict[str, str]]`, REQUIRED (L1995), comment "broker -> {INTENT -> code} (PR8)"; no validation of broker names, intent names or codes; an empty string is accepted. File value at the baseline: one broker key with four intents, one of which (`BRACKET_ORDER`) maps to an empty string. Consumer: `broker/product_resolver.py` L52 to L67 (A04). |
| Accounts | FACT: `config_loader.py` has no accounts schema and does not read `config/accounts.csv`; `main.py` loads it through `core/account_registry.AccountRegistry.load` (L2359, L2414; A01). |
| Other `config/` content | FACT: not in `_CONFIG_FILES`, so never read, validated or hashed by `load_all`: `cron_registry.yaml` (A16), `security.yaml`, `preflight.yaml` (both say so in their own headers, L3 to L4), `expected_managers.yaml`, `index_universe.yaml`, `strategy_direction_registry.yaml`, `symbol_aliases.yaml`, `reference_data/`, `accounts.csv`, `accounts_multi_example.csv`, `strategies/` (read by `strategies/loader.py`, another A02 part). |
| `file_hashes` | Exactly the eight registry file names when `load_all` succeeds (L2491, L2516); a missing file cannot appear in it because absence raises first (L2483). The holiday key changes name with the import year. Nothing outside the registry is hashed. |

## 4. Error behaviour

| Condition | Where | Result | Exception class (defined at) | Message and context | Silently defaulted? |
|---|---|---|---|---|---|
| `config_dir` is a `str` | L2481 | INTERPRETATION: `TypeError` from `str / str`, unwrapped | built-in | Python's message | no |
| A registered file is absent (or not a regular file) | L2483 to L2488 | stops at the first such file in registry order | `ConfigMissingError` (`core/exceptions.py` L69; `ConfigError` L56; `TradingSystemError` L30) | "Required config file not found: <file>"; context `file`, `path` | no |
| File unreadable | L2490; L2483 | INTERPRETATION: `OSError` subclass from `read_bytes()`, unwrapped; a parent directory without search permission already raises `PermissionError` from `is_file()` at L2483 (CPython 3.13; version-dependent, see 3.2 step 5) | built-in | Python's message | no |
| Malformed YAML (syntax, tabs, multiple documents, Python tags) | L2493 to L2500 | wrapped | `ConfigSchemaError` (`core/exceptions.py` L64), `from` the PyYAML error | "YAML parse error in <file>: <PyYAML text>"; context `file`, `path`. INTERPRETATION: the PyYAML text quotes the problem line and position, so it can carry file content | no |
| Invalid encoding (non-UTF-8 bytes, NUL, non-printable) | L2494 | verified on synthetic text: PyYAML `ReaderError`, a `YAMLError`, so the row above applies | `ConfigSchemaError` | "unacceptable character ..." | no |
| UTF-8 or UTF-16 BOM | L2494 | verified: accepted, same data | none | none | n/a (the hash differs from a BOM-less copy) |
| Duplicate keys in one mapping | L2494 | verified (PyYAML 6.0.3): the last value wins, no error; the code has no duplicate check | none | none | **yes: silent** |
| Empty file or comments only | L2502 to L2504 | `{}` validated; all eight root schemas have at least one required key, so it fails | `ConfigSchemaError` | "Schema validation failed for <file>"; context `file`, `error_count`, `errors` (no `path`) | no |
| Top level is a list or scalar | L2507 | INTERPRETATION: pydantic rejects a non-mapping for a model | `ConfigSchemaError` | as above | no |
| Missing required key | L2507 | pydantic "Field required" at the key's location | `ConfigSchemaError`, **not** `ConfigMissingError` (whose docstring, `core/exceptions.py` L70, says "required config file or required config key") | as above | no |
| Missing defaulted key | L2507 | the code default is used | none | none | **yes: 38 key occurrences (24 distinct keys) at the baseline (3.5)** |
| Unknown key in a model | L2507 | `extra="forbid"`: "Extra inputs are not permitted" | `ConfigSchemaError` | as above | no |
| Unknown key inside a mapping-typed field (`product_map`, `special_sessions`, `tiers`, `scanners`, `pivot_n_by_tf`, `regime_pref_*`, overrides) | L2507 | accepted | none | none | **yes: accepted silently** |
| Wrong type | L2507 | INTERPRETATION: lax coercion where pydantic allows it (for example `"5"` to 5, `20.0` to 20, `"yes"` to True), otherwise a type error. YAML 1.1 typing (verified): unquoted `15:30` is the integer 930 and `18:15` is 1095 (base-60), while unquoted `09:15` stays a string; bare `off`/`on`/`yes`/`no` are booleans; unquoted ISO dates are `date` objects; `1e3` is a string. So an unquoted time whose hour does not start with 0 (for example `15:30`, or `9:15`, which is 555), or a bare `off` for a mode string, is rejected for a `str` field | `ConfigSchemaError` | pydantic message at the location | coerced silently where lax mode allows |
| Value outside a validator's rule | L2507 | `ValueError` in the validator becomes "Value error, <text>" | `ConfigSchemaError` | the validator's text (for example L169 to L177, L1742 to L1745) inside `errors` | no |
| `null` for the seven required-but-nullable delivery keys | L501 to L513, L831 to L846, L855 to L867 | rejected with a reason ("does NOT fall back to the global (intraday) value", "does NOT fall back to a built-in default") | `ConfigSchemaError` | as above | no |
| NaN or infinity (`.nan`, `.inf` are floats in YAML, verified) | L2507 | INTERPRETATION: accepted by a float field unless a validator refuses it. Refused for leverage explicitly (L235 to L247) and by rules written as "require in range" (for example `not (0 < v < 1)`). Passed by rules written as "reject if v < x" or "reject if v <= 0", for example L361, L378, L598, L640, L1071, L1078, L1085, L1095, L1134, L1375, L1504 to L1507, L1572, L2156, L2212, L2219, L2237; and by every float field with no validator | none | none | **yes, where not refused** |
| Empty values | L2507 | empty strings accepted by every `str` field without a rule (for example `bot_token_env`, a `product_map` code); empty lists refused only for `alerts.telegram.channels` (L998 to L1003), `alerts.smtp.to_addresses` (L916 to L921), `sr_detector.timeframes` (L1247 to L1248); empty mappings accepted (`scanners`, `tiers`, `holidays: []` as a list) | none | none | **yes, accepted** |
| A configuration contradiction (auditor BLOCK) | L2080 | `ConfigContradictionError(ValueError)` (`core/config_auditor.py` L68) wrapped by pydantic | `ConfigSchemaError` for `system_config.yaml` | BLOCK messages joined with a vertical-bar separator (`core/config_auditor.py` L146) | no |
| Invalid MIS timing | L125 to L136 | `MisSquareoffConfigError(ValueError)` (`core/mis_squareoff_timing.py` L36) caught and re-raised as a plain `ValueError(str(exc))` | `ConfigSchemaError` | the MIS module's message; INTERPRETATION: located at `trading_hours` (a model-level error) | no |
| An exception other than `ValueError`/`AssertionError` inside a validator (for example an `ImportError` from a lazy import, or a `TypeError` in auditor code) | L122, L2072, L2507 | INTERPRETATION: pydantic does not convert it; it is not caught by `except ValidationError` (L2508) and escapes `load_all` unwrapped | the original class | Python's message | no |
| Partially valid configuration | L2480 to L2516 | no partial result; the first failing file raises; within one file pydantic reports all field-level errors together (`error_count`), and model-level rules only once the fields pass (INTERPRETATION) | as above | as above | no |

Context content (INTERPRETATION, pydantic 2): `errors=exc.errors()` (L2513) is a list of dicts with `type`, `loc`, `msg`, `input` and, for value errors, `ctx`; the `input` entries carry the rejected values (for a model-level rule, the whole section). `main.py` renders only `loc` and `msg` (`_config_error_detail`, L2018 to L2040); other callers print `str(exc)` (section 7.1).

## 5. Precedence

| Source | What the code shows | Label |
|---|---|---|
| YAML file value against code default | A key present in the file wins; an absent key takes the model default (pydantic). No other layer exists inside `load_all`. | FACT (L2507); INTERPRETATION (pydantic) |
| Environment variables | `load_all` reads none and expands none (CL5, L20 to L21; no `os` import outside L939). Configuration holds variable NAMES (section 9.4) that consumers read later. The only read in this module: `SmtpConfig.resolved_password()` (L935 to L949): if `password_env` is non-empty, the variable's value is returned, and an empty or unset variable raises `ValueError` (no fall back to the plaintext `password`); if `password_env` is empty, the plaintext `password` is returned. | FACT |
| Command line | The module reads none. Callers choose only the directory (`main.py --config`, L192 to L195, L2099; scripts' `--config`/`--config-dir`). | FACT |
| Code constants over files | `leverage_map.DELIVERY` must equal 1.0 (L232, L317 to L327); `service_window_end` must be below `SERVICE_WINDOW_END_MAX` 18:15 (L83, L180), which also fixes `main.py`'s start cutoff (L2001); `leverage_safety.max_allowed` must not exceed 20.0 (L229, L283); the MIS check uses the literal poll interval 5 instead of the configured one (L131). | FACT |
| Consumer-side overrides after loading (call sites only; not investigated) | `main.py` L3722 `V3ChainConfig()` if the section were absent (INTERPRETATION: not reachable from a loaded `AppConfig`, since L2015 defaults it) (A01, A18); `scripts/sr_level_export.py` L152 to L155 `model_copy(update=...)` sets four `sr_detector` values: `enabled` and `intraday_anchors_enabled` to the literal `True` (L153), and `anchor_intraday_interval` and `orb_window_minutes` from `--interval` and `--orb-window` (L154; L182 to L183, passed at L190) (INTERPRETATION: `model_copy` does not validate the update) (A08); `scripts/fetch_fno_ban.py` L324 to L325 `--url` wins over `fno_ban.url`, and a failed load falls back to module defaults (L321 to L322) (A05); `scripts/alert_watcher.py` L814 to L815 `--interval` wins over `alerts.watcher_interval_sec` (A14); `scripts/eod_cleanup.py` L57 to L58 command-line retention wins, and a failed load uses `EodCleanupConfig().signal_retention_days` (L62 to L67) (A12); `scripts/liveness_probe.py` L295 to L296 and `scripts/cron_officer.py` L781 to L783 fall back to `data_store` when the load fails (A15, A16); A01 C36a: `main.py` L2979 constructs SmartTgt enabled regardless of `smart_tgt.enabled`. | FACT (lines); owners as named |

## 6. Caching and state

| Item | Lines | Facts |
|---|---|---|
| Module-level cache or singleton | none | FACT: none. Each `load_all` call re-reads, re-hashes, re-parses and re-validates all eight files and returns a new `AppConfig`. |
| Reload | none | FACT: no reload function; docstring L38 "load-once at startup". Each caller decides when to call. |
| Values fixed at import | L2449, L2457 | FACT: the holiday-file year (`_CONFIG_FILES` is built once); the default `Path("config")` object (relative, resolved per call). INTERPRETATION: a process that imports the module before a year change and calls `load_all` after it still asks for the earlier year's file. |
| Default instances | L1114, L1989, L2022 to L2025 | FACT: six model instances built at import as field defaults. INTERPRETATION: pydantic 2 copies unhashable defaults per instance, so these are not shared between loads (not executed). |
| Mutability | all `ConfigDict` | INTERPRETATION: models are not frozen and assignment is not validated, so a holder can change a loaded value in process without any check. FACT (grep of non-test code for assignments to `app_config.*` and `setattr` on configs): none found; one `model_copy` (`scripts/sr_level_export.py` L152). |
| Side effects of a load | L2071 to L2084, L122 | FACT: every `load_all` call in which `system_config.yaml` has no field-level error and no BLOCK logs the auditor's WARN findings on logger `config_sanity` (each process, each call; `raise_if_blocked()` at L2080 runs before the WARN loop at L2083 to L2084); a load imports `core.config_auditor` and `core.mis_squareoff_timing` on first use. INTERPRETATION: in a process with no logging configured, Python's last-resort handler writes those WARNING lines to stderr. |

## 7. Callers (non-test, `git grep` at the baseline)

### 7.1 `load_all`: 26 call sites in 21 files

| Caller | Line(s) | Argument | On failure (call site only) | Owner topic |
|---|---|---|---|---|
| `main.py` | L2198 (import L57) | `config_dir` (`--config` or `Path("config")`, L2099) | any exception: CRITICAL log with `_config_error_detail`, return 5 (L2199 to L2201) | A01 |
| `ops/control_tower/aggregator.py` | L145 (import L142) | `Path(config_dir)` | CRITICAL finding "config failed to load" (L146 to L152) | A15 |
| `scripts/alert_watcher.py` | L795, L797 (import L68) | `Path(args.config)` or default | print, return 1 (L798 to L800) | A14 |
| `scripts/compute_strategy_metrics.py` | L303 (import L32 as `load_config`) | `Path(args.config)` (L301) | return 1 | A07 |
| `scripts/cron_officer.py` | L781 | default | falls back to `<repo>/data_store` | A16 |
| `scripts/deploy_preflight.py` | L42 to L46 (code string run on the VM through `python -c`) | default | n/a (remote) | A17 |
| `scripts/eod_broker_reconcile.py` | L343 | default | error log "config load failed", return 1 (L352 to L354; the same `try` also covers the reads at L344 to L351) | A12 |
| `scripts/eod_cleanup.py` | L61 | default | model default retention (L62 to L67) | A12 |
| `scripts/fetch_fno_ban.py` | L318 | `Path("config")` | module defaults (L322) | A05 |
| `scripts/forward_shadow_record.py` | L116 | `ROOT / "config"` | warning `forward_shadow.broker_connect_failed`, continues without broker data and records the score and decision only (L123 to L125) | A18 |
| `scripts/liveness_probe.py` | L294 | default | `Path("data_store")` | A15 |
| `scripts/monitoring_canary.py` | L314, L340 | default | return 1 / caught | A15 |
| `scripts/preflight/checks/config_integrity.py` | L140 | `ctx.config_dir` | check failed "config validation failed" | A20 |
| `scripts/preflight/checks/config_sanity.py` | L33 | `ctx.config_dir` | caught (L46) | A20 |
| `scripts/preflight_scanner_check.py` | L197 | `Path(args.config)` (L184) | return 1 | A06 |
| `scripts/reconcile_pnl.py` | L329 (import L41 as `load_config`) | `Path(args.config)` (L327) | return 1 | A12 |
| `scripts/reconcile_positions.py` | L369 (import L39 as `load_config`) | `Path(args.config)` (L367) | return 1 | A12 |
| `scripts/sr_level_export.py` | L139 | **`str(ROOT / "config")`, a `str`** (INTERPRETATION: `TypeError` at L2481) | none at the call site | A08 |
| `scripts/system_manager.py` | L1318 | `args.config_dir` (`type=Path`, L1298) | return 1 | A15 |
| `scripts/t2_cnc_gtt_realtest.py` | L159 | `Path("config")` | none at the call site | A19 |
| `scripts/v3_shadow_soak_report.py` | L45, L108, L189, L317 | `_REPO / "config"` | none at the call sites | A18 |

Import timing (INTERPRETATION): `main.py` and `scripts/alert_watcher.py`, `scripts/compute_strategy_metrics.py`, `scripts/reconcile_pnl.py`, `scripts/reconcile_positions.py` import the module at their top level (year fixed at process start); the others import inside a function (year fixed at the first such call in that process). Importing any module that imports a model class at its top level (`broker/clock_skew_probe.py`, `broker/cost_calculator.py`, `broker/rate_limiter.py`, `broker/slippage_engine.py`, `broker/zerodha_adapter.py`, `orders/order_placer.py`, `orders/order_reconciler.py`; table 7.2) also imports this module and fixes the year at that moment.

### 7.2 Model classes, constants and the method

| Name | Importer / caller (line) | Use | Owner topic |
|---|---|---|---|
| `SERVICE_WINDOW_END_MAX` | `main.py` L57, L2001 | `SERVICE_START_CUTOFF = SERVICE_WINDOW_END_MAX` | A01 |
| `ABSOLUTE_MAX_LEVERAGE` | none in code (named in a `config/system_config.yaml` L217 comment) | n/a | A02 |
| `ClockSkewProbeConfig` | `broker/clock_skew_probe.py` L48, L60 | type of the injected config | A04 |
| `BrokerCostsConfig` | `broker/cost_calculator.py` L43, L109 | constructor argument | A04 |
| `BrokerLimitsConfig` | `broker/rate_limiter.py` L40, L150 | constructor argument | A04 |
| `SlippageConfig` | `broker/slippage_engine.py` L46, L56 | constructor argument | A04 |
| `RateLimitBackoffConfig` | `broker/zerodha_adapter.py` L122, L370, L429 to L430; `orders/order_placer.py` L228, L578, L626 to L627 | argument; default instance when none passed | A04; A10 |
| `SmartTgtConfig` | `orders/order_placer.py` L228, L576 | argument type | A10 |
| `OrderReconcilerConfig` | `orders/order_reconciler.py` L77, L297 | argument type | A12 |
| `DriftHandlerConfig` | `capital/drift_handler.py` L63 (under `TYPE_CHECKING`), L84 | annotation only | A09 |
| `ScoringConfig` | `screening/quality_scorer.py` L22 (under `TYPE_CHECKING`), L48 | annotation only | A07 |
| `V3ChainConfig` | `main.py` L3716, L3722 | default instance when the section is absent | A01 (wiring), A18 |
| `EodCleanupConfig` | `scripts/eod_cleanup.py` L63 to L64 | default value after a failed load | A12 |
| `SmtpConfig.resolved_password()` | `scripts/alert_watcher.py` L295, L582; `scripts/monitoring_canary.py` L85 | SMTP login password at send time | A14; A15 |
| `AppConfig.file_hashes` | `main.py` L2202, L2312, L3261, L4178; `utils/startup_checks.py` L595; `core/evidence_contract.py` L468; `ops_dashboard/backend/services/audit.py` L151 (treated as noise); `core/config_snapshotter.py` L134 to L135 (dumps the whole `AppConfig`, `file_hashes` included, into the hashed snapshot, as its docstring L122 to L128 says) | count log; JSON into the state store and evidence; hash comparison; inside the snapshot hash | A01; A15; A02 (`core/config_snapshotter.py`) |

Duck-typed consumers (receive a loaded section without importing the class; found by name in comments and signatures, not exhaustive): `allocation/portfolio_allocator.py` L39, `v3_chain/runner.py` L49, `v3_chain/pb01_entry.py` L82 to L83, `v3_chain/pb01_runner.py` L64 to L65, `v3_chain/watchlist_capture.py` L60 (A18); `orders/structure_exit_manager.py` L103 (A11); `capital/strategy_governor.py` L29 (A09); `signals/webhook_receiver.py` L156 (A06); `broker/product_resolver.py` L57 to L67 (A04); `core/config_auditor.py`, `core/config_validator.py` L146, `core/config_snapshotter.py` (A02, other parts); `utils/startup_checks.py` L749, L757, L888 (A01).

## 8. Post-deployment change: commit `5f75c9b`

- **HISTORICAL:** `5f75c9b`, 2026-09-10 15:36 IST, "feat(config): MIS squareoff protected-MARKET bands, PASS_1 1.5 / PASS_2 2.5"; 38 lines added, 0 removed in `core/config_loader.py`; 12 lines added in `config/system_config.yaml` (the two keys with values 1.5 and 2.5 and their comment, inside `eod_squareoff`). The message: the values are percentages, config load refuses anything outside [0.1, 10.0], and the bounds mirror "the adapter's chokepoint" (the preceding commit `8f9afe0`, same day, "feat(adapter): market_protection at the single kite.place_order chokepoint", A04).
- **FACT, what the lines add to `EodSquareoffConfig`:**

| Lines | Added |
|---|---|
| L654 to L665 | a comment block (its content HISTORICAL): the units are PERCENTAGES (1.5 means 1.5%), unlike `limit_aggressive_pct` (a fraction); the comment says the values were chosen by Rama on 10-Sep from a measured coverage table; "Historical adverse-excursion coverage is NOT a guaranteed fill" |
| L666 | `mis_pass_1_market_protection_percent: float = 1.5` |
| L667 | `mis_pass_2_market_protection_percent: float = 2.5` |
| L709 to L731 | `_validate_market_protection_percent` (one `field_validator` for both): rejects values outside `0.1 <= v <= 10.0` with a message naming the field and the percent-versus-fraction risk (L725 to L730); docstring L715 to L724 says the bound mirrors `broker/zerodha_adapter.py` "kept in both places deliberately" |

- **FACT:** both keys are present in the baseline `system_config.yaml` (static check). INTERPRETATION (hand evaluation): the file values 1.5 and 2.5 pass the validator.
- **UNKNOWN / NOT ESTABLISHED:** whether production ever ran this commit (it is after the last recorded deployment `7d4970a`).
- Consumers of the two keys are outside A02 (A12 MIS auto-square-off, A04 adapter); not traced.

## 9. A01 handoffs: configuration-side facts only

### 9.1 C10a — the holiday-file year fixed at import (L2449)

| Fact | Lines | Label |
|---|---|---|
| The holiday entry of `_CONFIG_FILES` is `("nse_holidays", f"nse_holidays_{_date.today().year}.yaml", NseHolidaysConfig)`, inside a module-level tuple. | L2441 to L2450, L2449 | FACT |
| The f-string is evaluated once, when the module is first imported in a process; `load_all` iterates the tuple (L2480) and never recomputes the name. | L2449, L2480 | FACT (code); INTERPRETATION (Python import semantics) |
| `date.today()` is the host-local date (the process's local time zone), not IST from `core.time_authority`; the module uses no `now_ist`/`time_authority` (grep). | L2449 | FACT (no IST source); INTERPRETATION (`date.today()` semantics) |
| HISTORICAL: introduced by `c303e04` (2026-06-13), "F30: nse_holidays filename uses dynamic year (_date.today().year) in config_loader + healthcheck"; the docstring L33 still names `nse_holidays_2026.yaml`. | blame L2449 | HISTORICAL |
| Other year derivations for the same file elsewhere (not A02's, cited for comparison only): `utils/startup_checks.py` L859 to L866 (UTC plus 05:30, A01); `scripts/preflight/checks/config_integrity.py` L35 to L36 (`config_files_for(year)`, A20); `scripts/security_monitor.py` L873 to L887 comment describing this line and a reminder for the next year's file (A17). | cited | FACT (lines) |
| Not established: the VM's time zone; whether any process imported the module on one side of a year change and loaded on the other. | — | UNKNOWN / NOT ESTABLISHED |

### 9.2 C10b — `load_all`'s holiday-file requirement and the year it uses

| Fact | Lines | Label |
|---|---|---|
| The holiday file is required exactly like the other seven: absent means `ConfigMissingError("Required config file not found: nse_holidays_<year>.yaml", file=..., path=...)`; there is no optional entry and no fallback year. | L2483 to L2488 | FACT |
| The year is the import-time host-local year (9.1). Only that one file is loaded; the next year's file is never read by `load_all`, so `AppConfig.nse_holidays` holds one file's entries only. | L2449, L2480 | FACT |
| Nothing checks that the entries' dates belong to the year in the file name, that they are unique, or that they are weekdays; `holidays: []` passes; a missing `holidays` key fails as "Field required" (`ConfigSchemaError`). | L2395 to L2413 | FACT (absence of checks); INTERPRETATION (pydantic) |
| Baseline: `config/nse_holidays_2026.yaml` is the only holiday file. With the baseline file set, a process that imports the module with a host-local date in 2027 or later gets `ConfigMissingError` from `load_all`; in `main.py` that is exit 5 (L2197 to L2201). | `config/` listing | FACT (file set); INTERPRETATION (consequence); `scripts/security_monitor.py` L873 to L880 records the same as "MEASURED" (HISTORICAL) |

### 9.3 C35 — the special-session schema

| Fact | Lines | Label |
|---|---|---|
| Declaration: `special_sessions`, typed `dict[str, dict[str, str]]` or `None` (a union), default `None`, comment "FIX-094: date -> {market_open, market_close, eod_squareoff_time}"; added by `4c99692` (2026-05-18). | L1992 | FACT |
| No validator: no `field_validator` names it, the two `SystemConfig` validators (L2046 to L2086) do not test it, and `core/config_auditor.py` does not mention it (grep). | — | FACT |
| What the type alone allows: any string keys (no date format), an inner mapping of any string keys to any string values (no check that `market_open`, `market_close`, `eod_squareoff_time` exist, that they are HH:MM, ordered, or compatible with `service_window_end`, the MIS cutoff or the holiday list). An empty mapping or `null` is accepted. | L1992 | FACT (declaration); INTERPRETATION (pydantic) |
| YAML typing: an unquoted key `2026-11-01:` is read by PyYAML as a `datetime.date` (verified on synthetic text). INTERPRETATION (pydantic 2 does not coerce a date to `str`): such a key is rejected, so `system_config.yaml` fails with `ConfigSchemaError` and `main.py` exits 5. Likewise an unquoted time such as `18:15` is the integer 1095 and is rejected as a value. Quoted keys and values pass the schema and are parsed only later by `main.py` `_load_special_sessions` (L446 to L470; A01). Not executed. | L1992 | INTERPRETATION |
| Baseline: the key `special_sessions:` is followed only by comment lines, so its value is `null` (verified by parsing the file); the commented example (`config/system_config.yaml` L118 to L122) has an unquoted date key and quoted times. | `config/system_config.yaml` L117 to L122 | FACT |

### 9.4 C12 — `bot_token_env` and the other credential-name fields

| Field | Lines | Default | Rule | File value at the baseline (names only) | Consumers (call sites) |
|---|---|---|---|---|---|
| `alerts.telegram.bot_token_env` | L981 (blame `bcf03b5`, 2026-04-17) | `"TELEGRAM_BOT_TOKEN"` | none (any string, empty accepted) | `TELEGRAM_BOT_TOKEN` (`config/system_config.yaml` L388), equal to the default | `main.py` L2629 `os.environ[tg_cfg.bot_token_env]` (A01) |
| `alerts.telegram.channels[].chat_id_env` | L973 | REQUIRED | none; the list must be non-empty (L998 to L1003) | `TELEGRAM_CHANNEL_PRIMARY` (L416), `TELEGRAM_CHANNEL_SECONDARY` (L419) | `main.py` L2622 (A01); `alerts/telegram_notifier.py` L622 (A14) |
| `alerts.telegram.personal_chat_id_env` | L984 | `""` | none | `TELEGRAM_PERSONAL_CHAT_ID` (L422) | none found in non-test code (grep) |
| `alerts.smtp.password_env` | L894 | `""` | password or password_env non-empty (L923 to L933) | `ALERT_SMTP_PASSWORD` (L459) | `SmtpConfig.resolved_password()` L935 to L949, called by `scripts/alert_watcher.py` L295, L582 (A14), `scripts/monitoring_canary.py` L85 (A15) |
| `alerts.smtp.password` (plaintext fallback) | L890 | `""` | as above | absent (default `""` applies) | via `resolved_password()` only when `password_env` is empty (L949) |
| `alerts.email_fallback.from_addr_env`, `.password_env`, `.to_addr_env` | L958 to L960 | `"ALERT_EMAIL_USER"`, `"ALERT_EMAIL_PASSWORD"`, `"ALERT_EMAIL_TO"` | none | equal to the defaults (L444 to L446) | `alerts/telegram_notifier.py` L805 to L807 (A14) |

Further FACTS: `config_loader.py` has no broker-credential field (no API key, secret or TOTP name: those are per account in `config/accounts.csv`, read by `core/account_registry.py`, A01) and no webhook-secret field (`WebhookConfig` has only `require_hmac`, L621). `load_all` never checks that a named variable exists (no environment read during load). Not established: which variables were set on the VM (UNKNOWN / NOT ESTABLISHED).

### 9.5 M-24 — `MisSquareoffConfigError` and the MIS timing validation with a literal poll interval

| Fact | Lines | Label |
|---|---|---|
| `MisSquareoffConfigError` is defined in `core/mis_squareoff_timing.py` L36 as `class MisSquareoffConfigError(ValueError)` (owner A12), outside the `core/exceptions.py` tree. `config_loader.py` neither defines nor raises it. | `core/mis_squareoff_timing.py` L36 | FACT |
| `TradingHoursConfig._validate_mis_squareoff_timing` imports it lazily (L122 to L124), calls `MisSquareoffTiming.build(...)` with the four `mis_squareoff_*` values (`cutoff`, `first_offset`, `second_offset`, `margin_sec`), `entry_end` and `eod_squareoff_time` (six `trading_hours` values) and the literal `poll_interval_sec=5` (L126 to L134), and converts the error: `except MisSquareoffConfigError as exc: raise ValueError(str(exc)) from exc` (L135 to L136). So at load time the class never leaves `load_all`: it becomes a pydantic error and then `ConfigSchemaError` (exit 5 in `main.py`). | L109 to L137 | FACT (code); INTERPRETATION (pydantic wrapping) |
| The literal `5` (blame `6f00b4d`, 2026-08-28) is used where the runtime uses the configured value: `main.py` L3329 to L3337 passes `app_config.system.eod_squareoff.poll_interval_sec` (L3334), and the notifier receives the same key (L3345). In `build`, the poll interval enters two rules only: positive integer (mis L125 to L128) and `margin_sec >= poll_interval_sec` (mis L129 to L138). | L131; `main.py` L3334, L3345 | FACT |
| No rule in this module or in `core/config_auditor.py` relates `eod_squareoff.poll_interval_sec` to `trading_hours.mis_squareoff_margin_sec`; `EodSquareoffConfig.poll_interval_sec` only requires `>= 1` (L676 to L681). INTERPRETATION: the load-time check equals the runtime check only when the configured poll interval is 5; a configured poll interval above the margin (for example 21 or more with the margin 20) passes `load_all` and fails at `main.py` L3329 with `MisSquareoffConfigError` (A01 M-24: exit 2). | L676 to L681; grep | FACT; INTERPRETATION |
| File values at the baseline: `eod_squareoff.poll_interval_sec: 5` (`config/system_config.yaml` L361), `mis_squareoff_margin_sec: 20` (L96), cutoff "15:09", offsets "6m"/"3m", `entry_end` "15:00", `eod_squareoff_time` "15:17". INTERPRETATION (hand evaluation): both the load-time and the runtime checks pass (15:00 < 15:03 < 15:06 < 15:09 < 15:17; 20 >= 5). | `config/system_config.yaml` L28 to L96, L361 | FACT (values); INTERPRETATION (evaluation) |
| HISTORICAL against FACT: the validator's docstring (L113 to L116) says "the schema and the runtime cannot disagree: there is ONE definition of the ordering invariant"; the poll input differs (literal against configured). The MIS module's message names the key `mis_squareoff.poll_interval_sec` (mis L127), which does not exist in the schema (the configured key is `eod_squareoff.poll_interval_sec`). | L113 to L116; mis L127 | HISTORICAL; FACT |

### 9.6 M-19 and M-20 — exception classes in `config_loader.py`

| Fact | Lines | Label |
|---|---|---|
| `config_loader.py` defines no exception class: all 65 classes subclass `BaseModel` (AST). | table 1.2 | FACT |
| It raises two classes, both from the central tree: `ConfigMissingError` (L2484) and `ConfigSchemaError` (L2496, L2509), defined in `core/exceptions.py` L69 and L64 as subclasses of `ConfigError` (L56), itself a subclass of `TradingSystemError` (L30). Both are raised, so neither is a "never raised" class for M-20. | L2484, L2496, L2509 | FACT |
| 116 `raise ValueError` in the module (AST). 115 are reached through validators: 114 in decorated validators and 1 in the private function `_validate_finite_leverage` (L244), which the validators at L268 and L315 call; inside `load_all` these never escape as `ValueError` (wrapped into `ConfigSchemaError`). The 116th is in `SmtpConfig.resolved_password()` (L943), a method, not a validator: it raises `ValueError` directly to its callers (L942 to L947), outside the load and outside the tree. | L244, L943 | FACT |
| Classes from elsewhere that pass through: `MisSquareoffConfigError(ValueError)` (`core/mis_squareoff_timing.py` L36, A12) and `ConfigContradictionError(ValueError)` (`core/config_auditor.py` L68, A02 other part), both outside the `TradingSystemError` tree and both wrapped during `load_all`. | L135 to L136, L2080 | FACT |
| Not raised by this module: the sub-root `ConfigError` itself and `ConfigValidationError` (`core/exceptions.py` L74; its docstring names `core/config_validator.py`, another A02 part). | — | FACT (grep of this file) |
| Not established here: whether other modules raise `ConfigMissingError` or `ConfigSchemaError` (A01 M-23 lists further raisers of `ConfigError` subclasses). | — | not in this part's scope |

### 9.7 Also asked of A02 by A01 (C7d, S-11): the hashed set

FACT: `file_hashes` holds exactly the eight registry file names after a successful load (L2491, L2516); a registry file cannot be missing from it without `load_all` raising first (L2483 to L2488); so no hashed file can disappear without failing the load, except that the holiday key's name changes with the import year (a year change replaces one key with another). Files outside the registry (section 3.6) are never hashed, so their change or removal is not represented in `file_hashes`. The digest is of raw bytes (L2491), so formatting-only edits change it.

## Could not establish (summary)

- Anything about what ran in production: the VM's time zone, the installed PyYAML and pydantic versions, which environment variables were set, whether any process crossed a year boundary, and whether `5f75c9b` was ever deployed (UNKNOWN / NOT ESTABLISHED).
- Pydantic behaviour at the pinned version 2.13.0 was not tested; the coercion, wrapping, ordering, NaN and date-key statements are INTERPRETATION from the library's documented semantics, checked against synthetic models of no legacy origin with pydantic 2.13.5.
- The baseline files were compared with the schema for keys and YAML types only; validators were evaluated by hand only for `trading_hours` (both validators), the MIS timing and the two market-protection percentages.
