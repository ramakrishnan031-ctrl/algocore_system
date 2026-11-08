# A02 evidence: The configuration validator, auditor and snapshotter, and the boot configuration hash

**Status:** DRAFT — evidence for the A02 STUDY, for ChatGPT's review
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06. Corrected, 2026-11-08: after the independent check of the A02 STUDY against the code (the rows named in that check).
**Purpose and scope:** This file records what `core/config_validator.py`, `core/config_auditor.py` and `core/config_snapshotter.py` do at the baseline (rules, results, side effects and callers), the W0 configuration snapshot, the file hashes the boot uses to detect configuration changes, the paths by which secret values could be exposed, and the configuration-side facts for the A01 items C7d, S-11, S-24, W-17 and M-24. It supports the A02 STUDY sections on configuration validation, the configuration auditor, the configuration snapshot and change detection at boot, and the A01 handoff.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git grep`, `git log` and the standard library's `ast`, in scripts kept outside the clone; nothing in the clone was written or run. Statements about pydantic and PyYAML behaviour rest on the libraries' documented rules and on tests of synthetic inputs outside the clone (pydantic 2.13.5, against the pinned 2.13.0; PyYAML 6.0.3, the pinned version; `requirements.txt` L6 to L7); they are INTERPRETATION, and the versions installed on the VM are UNKNOWN / NOT ESTABLISHED.

- Reading: the three modules were read in full (274, 858 and 217 lines). The relevant parts of `core/config_loader.py`, `main.py`, `utils/startup_checks.py`, `core/mis_squareoff_timing.py`, `core/schema.sql` and the callers were read at the cited lines. Callers were found with `git grep`. YAML file text from `git show` was parsed with `yaml.safe_load`, and constructor signatures were read statically with `ast`. No legacy code was imported or run.
- Labels: FACT, INTERPRETATION, HISTORICAL, UNKNOWN / NOT ESTABLISHED, OPEN QUESTION. A YAML value is "the file value at the baseline". Nothing here says what ran in production: that is UNKNOWN / NOT ESTABLISHED throughout.
- Owner topics come from the Master System Investigation Index, section 3: `main.py`, `utils/startup_checks.py` and `core/exceptions.py` are A01's; `core/schema.sql`, `core/migrations.py` and `core/state_store.py` are A03's; `strategies/control.py` is A07's; `capital/*` is A09's; `orders/order_placer.py` is A10's; `core/mis_squareoff_timing.py` is A12's; `ops/`, `ops_dashboard/`, `reports/` and `core/evidence_artefact_manifest.txt` are A15's; `scripts/preflight/` is A20's; `tests/` is A19's.

---

## 1. Module maps

### 1.1 `core/config_validator.py` (274 lines; one commit, `419c430`, 2026-05-02, "feat: add ConfigValidator to prevent config drift": HISTORICAL)

| Item | Lines | Role |
|---|---|---|
| Module docstring | L1–L43 | States design CV1 to CV4 (HISTORICAL/claim): CV1 runtime tracking via `track`/`get`; CV2 mandatory injection; CV3 "Any untracked config key → ConfigValidationError → exit(1)"; CV4 static analysis "Not implemented in v1". The usage example at L37 is `config_validator.validate_all(app_config)`. |
| Imports | L44–L50 | `logging`, `dataclasses`, `typing`, `core.exceptions.ConfigValidationError` |
| `logger` | L52 | `logging.getLogger(__name__)` |
| `T` | L54 | TypeVar for `get` |
| `ConfigUsage` (dataclass) | L57–L65 | One key's record: `key`, `expected_value`, `actual_value`, `accessed`, `access_count`, `accessor_modules` |
| `ConfigValidator` | L68–L271 | Tracker. Docstring L72: "Thread-safe for read tracking (via get())". FACT: the module has no lock or `threading` import. |
| `__init__` | L76–L79 | `_tracked={}`, `_enabled=True`, `_validated=False` |
| `reset` / `disable` / `enable` | L81–L84 / L86–L88 / L90–L92 | For tests. FACT: no non-test caller (git grep). |
| `register_expected` | L94–L102 | Stores a fresh `ConfigUsage(key, expected_value)` and overwrites any earlier entry for the key |
| `get` | L104–L142 | Marks a key accessed. Logs WARNING `CONFIG_DRIFT` with the expected and actual values when they differ (L127–L131). Registers keys it has not seen as accessed (L132–L140). Returns the value. |
| `register_all_from_app_config` | L144–L183 | Walks the Pydantic models and registers every leaf (see section 2) |
| `get_usage_report` | L185–L219 | Builds the in-memory lists accessed, unaccessed and drift, with their counts |
| `validate_all` | L221–L271 | The gate (see section 2) |
| `config_validator` | L274 | Module-level singleton instance |

Import-time effects. FACT: the import creates the module logger and the singleton (`_enabled=True`). There is no I/O, no database access and no file access.

### 1.2 `core/config_auditor.py` (858 lines; 10 commits, from `eb373c4` on 2026-06-25, "BUILD 2: Config Sanity Auditor", to `076fe57` on 2026-08-23: HISTORICAL)

| Item | Lines | Role |
|---|---|---|
| Module docstring | L1–L33 | "ONE rule engine, two callers": STARTUP (config_loader's model validator, config-only groups, raises on BLOCK) and PRE-FLIGHT (`scripts/preflight/checks/config_sanity.py`, all groups, the 08:30 → 09:20 e-mail and Telegram report). "VALIDATE + ALERT only." Lists groups A to G. |
| Imports | L34–L38 | `enum`, `dataclasses`, `typing` only |
| `Severity` (Enum) | L45–L50 | PASS, INFO, WARN, BLOCK |
| `_SEV_RANK` | L53 | Ranks the severities 0 to 3 |
| `GROUP_TITLES`, `GROUP_ORDER` | L56–L64, L65 | A Contradictions; B Single-source integrity; C Capital-relative sanity; D Active overrides; E Launch-phase reminders; F Stale-default guard; G Cross-field sanity; `"ABCDEFG"` |
| `ConfigContradictionError(ValueError)` | L68–L72 | Raised by `raise_if_blocked`. It subclasses ValueError so that Pydantic wraps it (docstring). |
| `AuditFinding` (frozen dataclass) | L75–L85 | `group`, `code`, `severity`, `message`, `metrics`; `group_title` property |
| `ConfigAuditReport` (dataclass) | L88–L146 | Filters: `by_severity`, `blocks`, `warns`, `infos`, `for_group`, `worst_in_group` (L93–L115). `verdict` (L118–L124): BLOCK if any BLOCK, else WARN if any WARN, else PASS; INFO does not count. `actionable` = BLOCK + WARN (L126–L129). `one_line` shows up to 6 actionable items (L131–L140). `raise_if_blocked` joins every BLOCK message into one ConfigContradictionError (L142–L146). |
| `_LaunchParam`, `LAUNCH_PHASE_PARAMS` | L155–L159, L162–L169 | Group E registry: one row, `trading_hours.entry_start` |
| `_STALE_DEFAULT_GUARDS` | L175–L180 | Group F registry: `capital.position_sizer.PositionSizer.max_position_value_pct` against `position_sizing.max_position_value_pct`; `capital.fund_manager.FundManager.daily_loss_limit_pct` against `risk.daily_loss_limit_pct` |
| `_group_a_contradictions` | L187–L323 | Group A |
| `_group_b_single_source` | L326–L389 | Group B (needs the raw YAML) |
| `_SIZER_TIERED_QTY_HARD_CAP = 2.0` | L398 | Mirrors a literal in `capital/position_sizer.py` (comment L392–L397) |
| `_max_effective_multiplier` | L401–L413 | min(max positive tier weight × `max_multiplier`, 2.0) |
| `_group_c_capital_relative` | L416–L530 | Group C |
| `_group_d_active_overrides` | L533–L573 | Group D |
| `_group_e_launch_phase` | L576–L590 | Group E |
| `_group_f_stale_default` | L593–L669 | Group F (signature introspection) |
| `_group_g_cross_field` | L672–L765 | Group G |
| `audit` | L772–L803 | The rule engine (see section 3.2) |
| `STARTUP_GROUPS = "ACG"` | L811 | The startup subset |
| `audit_system_config` | L814–L818 | Startup entry: `audit(system, groups="ACG")` |
| `audit_app_config` | L821–L847 | Pre-flight entry: reads the raw YAML when `config_dir` is given |
| `_safe_load_yaml` | L850–L858 | Reads `config_dir/filename` as UTF-8 with `yaml.safe_load`. Returns None on any exception or when the result is not a dict. |

Import-time effects. FACT: only class and constant definitions; no I/O. The heavier imports are deferred into the functions: `strategies.control.strategy_will_trade` (L268, L306); `orders.order_placer.validate_slippage_overrides` (L568); `importlib.import_module` of `capital.position_sizer` and `capital.fund_manager` (L620, L626); `yaml` and `pathlib` (L852–L853). INTERPRETATION: running groups A, D or F imports those modules, with whatever import-time effects they have (A07, A10 and A09 own them).

### 1.3 `core/config_snapshotter.py` (217 lines; 3 commits: `01e07b7` 2026-07-01, `dbeba4a` 2026-07-16 "redact populated secrets ... (M-K5)", `4c495d0` 2026-08-22 "NI-6": HISTORICAL)

| Item | Lines | Role |
|---|---|---|
| Module docstring | L1–L32 | W0: persists the "FULL resolved runtime config" to `config_snapshots` at startup. Idempotent per `(snapshot_date, config_hash)`. Claim at L23–L27: "No secrets are logged (only the row id, the hash prefix, and the wrote/skipped decision)". |
| Imports | L33–L38 | `hashlib`, `json`, `logging`, `typing` |
| `_SECRET_KEY_MARKERS` | L49 | `("password", "secret", "token", "api_key", "apikey")` |
| `_REDACTED` | L50 | The marker string that replaces a redacted value |
| `_is_secret_key` | L53–L57 | Lower-cases the key. Returns False for keys ending in `_env`; otherwise True if any marker is a substring of the key. |
| `redact_secrets` | L60–L83 | Recursive over dicts and lists. Replaces a value only when its key is a secret key **and** the value is a **non-empty str** (L77). |
| `config_to_canonical_json` | L86–L99 | `json.dumps(redact_secrets(cfg), sort_keys=True, separators=(",", ":"), ensure_ascii=False)` |
| `hash_config_json` | L102–L104 | `sha256(config_json.encode("utf-8")).hexdigest()` |
| `_resolve_config_dict` | L107–L141 | Uses `app_config.model_dump(mode="json")` if the object has `model_dump`, passes a dict through, otherwise raises TypeError naming the type only. The NI-6 docstring (L115–L132, HISTORICAL) says `file_hashes` sits inside the dump, so a comment-only YAML edit changes `config_hash`. |
| `snapshot_config` | L148–L217 | The one entry point (see section 4). Docstring L168 holds an example broker account identifier (value not reproduced). |

Import-time effects. FACT: none beyond the definitions. There is no module-level logger: `logging.getLogger("config_snapshotter")` is created at call time when no logger is passed (L177).

---

## 2. `config_validator.py`: rules, `strict`, result, side effects, callers

### 2.1 What it registers (`register_all_from_app_config`, L144–L183)

| Rule | Lines | FACT |
|---|---|---|
| Sub-configs walked | L179–L183 | `system`, `broker_costs`, `broker_limits`, `slippage`, `scoring` |
| Sub-configs not walked | L179–L183 by omission; AppConfig fields `core/config_loader.py` L2426–L2434 | `scan_webhook_map`, `chartink_scanners`, `nse_holidays`, `file_hashes` |
| Nested Pydantic model | L163–L164 | Recursed with a dotted key |
| Dict field | L165–L171 | Each entry becomes `key.<dictkey>`. A model value is recursed; any other value, including a whole nested plain dict (for example `product_map`, `special_sessions`), is registered as one leaf. |
| List field | L172–L175 | Only Pydantic items are walked, keyed `key[i]`. Scalar lists (for example `excluded_symbols`, `slippage_bands`) are not registered at all. |
| Scalar or None | L176–L177 | Registered as the expected value |
| Disabled | L151–L152 | No-op when `_enabled` is False |

### 2.2 `validate_all(strict=False)` (L221–L271)

| Step | Lines | Outcome |
|---|---|---|
| Disabled | L232–L233 | Returns |
| Second call | L235–L237 | DEBUG "already called; skipping" and return |
| Unaccessed keys (registered, never `get()`) | L242–L255 | Message `CONFIG_UNACCESSED: N config keys never read: [first 10 key names]` plus "... and M more". `strict=True`: ERROR log, then raise `ConfigValidationError(..., unaccessed_keys=keys)` with every key name. `strict=False`: WARNING log only. |
| Drift (accessed and expected ≠ actual) | L257–L266 | ERROR `CONFIG_DRIFT_DETECTED`, then **raise `ConfigValidationError(..., drift_keys=...)` whatever `strict` is** |
| Success | L268–L271 | INFO `ConfigValidator: a/total keys accessed, 0 drift` |
| Return | — | None |

- Meaning of `strict`. FACT: it affects only the unaccessed-keys branch (L248–L255). Drift always raises.
- INTERPRETATION (Python call semantics): the docstring usage example `validate_all(app_config)` (L37) would bind `app_config` to `strict`, which would select strict mode: a truthy object there takes the raising branch (L248–L253).
- `ConfigValidationError` is `core/exceptions.py` L74–L85, a subclass of `ConfigError` (L56), which subclasses `TradingSystemError` (L30). It carries `SEVERITY="ERROR"` and context kwargs.
- Side effects. FACT: logging only, under logger `__name__` (INTERPRETATION: `core.config_validator`; `ops_dashboard/backend/services/system_logs.py` L92–L93, A15, groups that logger name under "System Monitor"). There are no alerts, no database writes and no files. Key names are logged; values are logged only by `get()`'s drift warning (L128–L131).

### 2.3 Callers (non-test; `git grep`)

| Caller | Line | Owner | What it does |
|---|---|---|---|
| `main.py` import | L60 | A01 | `from core.config_validator import config_validator` |
| `main.py` `_main_locked` | L2205 | A01 | `register_all_from_app_config(app_config)`, right after `load_all` (L2198) and its log line (L2202), and before StateStore. It also runs for `--status` and `--dry-run` boots. |
| `main.py` | L4164 | A01 | `validate_all(strict=False)`. Comment L4163: "CV3: ... non-strict for gradual rollout". |
| Any call of `get()` or `track()` | none outside tests | — | FACT (git grep): no non-test code calls `get()` on the singleton or on any instance. Tests call `get()` on their own `ConfigValidator()` instances (for example `tests/core/test_config_validator.py` L27, L48, L98, L152). The class has no `track` method at all; only the docstring names it (L17). |

When `validate_all` runs in the boot (FACT, `main.py`): after every subsystem is built and the EOD self-exit thread is armed (L4129–L4161), immediately before Phase 0h (the STARTUP system_event at L4167–L4173 and the second `_write_session` at L4174–L4180). `--status` (L2299–L2302), `--dry-run` (L2476–L2482) and every earlier failure return before it.

What `main.py` does with the result. FACT: the return value is ignored and there is no try/except around L4164. An exception would leave `_main_locked` (the `try/finally` at L2187–L2190 only releases the lock) and reach the guard at L4285–L4293: `except TradingSystemError` gives exit 1.

INTERPRETATION (from the grep). Because no non-test code calls `get()`, no key of the singleton is ever marked accessed. Every registered key is therefore "unaccessed" and the drift list is always empty (drift requires `accessed`, L204–L207; `accessed` is set only at L121 and L136). At baseline each boot reaching L4164 would log one WARNING `CONFIG_UNACCESSED` and one INFO "0/N keys accessed, 0 drift", and would not raise. The number N is UNKNOWN (it depends on the resolved models; nothing was run).

---

## 3. `config_auditor.py`: groups, codes, `groups=`, callers, gaps

### 3.1 Findings by group (severity as coded)

"Object" = the loaded `SystemConfig` (duck-typed `sc`); "raw" = the raw YAML dict; "strategies" = the dict of loaded strategy configs.

| Group | Code | Severity | Inspects | Condition | Lines |
|---|---|---|---|---|---|
| A | `A1_force_intraday_delivery` | BLOCK | object | `force_intraday_only` truthy and `trade_type == "DELIVERY"`; message contains "CONTRADICTORY CONFIG" | L196–L203 |
| A | `A2_trade_type_domain` | BLOCK | object | `trade_type` not in INTRADAY/DELIVERY/BOTH | L207–L213 |
| A | `A4_structure_exit_trailing_sl` | BLOCK | object + strategies | only if strategies are given; `structure_exit.structure_exit_enabled is True` and at least one strategy has `enabled` (default True) and `trailing_sl_enabled is True`; metrics list the names | L222–L239 |
| A | `A5_delivery_without_conditional_allocation` | BLOCK | object + strategies | only if strategies are given; `delivery_enabled` and not `capital.conditional_allocation_enabled`; at least one strategy will trade, and every strategy for which `strategy_will_trade(...).will_trade` holds has `Verdict.product == "DELIVERY"`; the message includes `capital.intraday_bucket_pct` as a percentage. **The whole block sits in `try/except Exception: pass`** (L267, L296–L297). | L266–L297 |
| A | `A3_zero_strategies_trade` | WARN | object + strategies | only if strategies are given **and no earlier group-A finding**; no strategy will trade; also `try/except Exception: pass` (L305, L318–L319) | L304–L319 |
| A | `A_ok` | PASS | — | no group-A finding | L321–L322 |
| B | (no finding at all) | — | raw | returns `[]` when `raw_system` is None: the raw read failed or the file is not a mapping (L850–L858), or `config_dir` was not given (L834–L836). The startup path does not run group B at all (`STARTUP_GROUPS = "ACG"`, L811). In pre-flight, an empty B list gives a PASS row titled "Single-source integrity" (`scripts/preflight/checks/config_sanity.py` L66–L80; `worst_in_group` L111–L115). | L334–L335 |
| B | `B1_daily_loss_limit_resurrected` | WARN | raw system | key `capital.daily_loss_limit` present | L341–L347 |
| B | `B2_max_position_value_rs_resurrected` | WARN | raw system | key `position_sizing.max_position_value_rs` present | L348–L353 |
| B | `B3_live_test_mode_resurrected` | WARN | raw system | any `risk.live_test*` key | L354–L360 |
| B | `B4_tier_multipliers_duplicated` | WARN | raw scoring | top-level `tier_multipliers` present | L361–L366 |
| B | `B5_scoring_threshold_ordering_live` / `_v3` | **BLOCK** | raw scoring | all three keys present and not `high > medium > min_pass` (live set and `v3_` set); the comment labels this "A9 (V3 03.04)" | L371–L382 |
| B | `B_ok` | PASS | — | none of the above | L384–L388 |
| C | `C1_daily_loss_pct_range` | WARN | object `risk.daily_loss_limit_pct` | not in (0, 0.10] | L426–L432 |
| C | `C2_position_cap_not_looser` | WARN | object `position_sizing` | `max_position_value_pct <= max_concentration_pct × _max_effective_multiplier` | L453–L466 |
| C | `C2d_delivery_position_cap_not_looser` | WARN | object | same ladder for `delivery_max_*` when both are not None | L479–L494 |
| C | `C3_risk_per_trade_range` | WARN | object | `risk_per_trade_pct` not in (0, 0.05] | L497–L502 |
| C | `C4_risk_exceeds_concentration` | WARN | object | `risk_per_trade_pct > max_concentration_pct` | L505–L511 |
| C | `C5_cumulative_risk_vs_daily_loss` | WARN | object | only when daily limit < 1.0; `risk_per_trade_pct × risk.max_open_positions > 2 × daily limit` | L515–L523 |
| C | `C_ok` | PASS | — | none | L525–L529 |
| D | `D_unavailable` | INFO | object | `sc.entry_gate.slippage_control.overrides` raises | L540–L544 |
| D | `D_none` | INFO | object | the `by_symbol`, `by_strategy` and `by_price_band` maps are all empty | L554–L557 |
| D | `D_active` | INFO | object | lists every non-empty map in the message, with its contents, and whether `enabled` is set | L558–L564 |
| D | `D_override_warn` | WARN | object + `known_symbols`/`known_strategies` | one per warning string returned by `orders.order_placer.validate_slippage_overrides` (A10); exceptions swallowed | L567–L572 |
| E | `E_trading_hours_entry_start` | INFO | object | always, from the `LAUNCH_PHASE_PARAMS` row; getter exceptions skip the row | L579–L587 |
| E | `E_none` | INFO | — | no rows produced | L588–L589 |
| F | `F_<Class>_<param>` (`F_PositionSizer_max_position_value_pct`, `F_FundManager_daily_loss_limit_pct`) | WARN | code signature + object | constructor default ≠ config value | L624–L644 |
| F | `F_<Class>_<param>_required` | PASS | code signature | the parameter has no default | L633–L635, L645–L651 |
| F | `F_<Class>_<param>_unresolved` | PASS | — | import, attribute or introspection failed ("this guard did NOT run") | L630–L632, L652–L657 |
| F | `F_ok` | PASS | — | no F WARN; names what was compared, or says nothing was | L658–L668 |
| G | `G1_entry_end_near_squareoff` | WARN | object `trading_hours` | `eod_squareoff_time − entry_end < 15` minutes | L684–L692 |
| G | `G2_leverage_INTRADAY` / `G2_leverage_COVER_ORDER` | WARN | object `capital.leverage_map` | value > 10 (DELIVERY and BRACKET_ORDER are not checked) | L695–L702 |
| G | `G3_min_tick_size` | WARN | object `position_sizing.min_tick_size` | < 0.01 | L705–L710 |
| G | `G5_window_<strategy>` | WARN | object + strategies | the strategy's `entry_start_time`/`entry_end_time` has **no** overlap with the global `entry_start`–`entry_end`; per-strategy exceptions skipped. There is no G4 code. | L745–L761 |
| G | `G_ok` | PASS | — | none | L763–L764 |

Group B and the schema. FACT: `ScoringConfig._validate_threshold_ordering` (`core/config_loader.py` L2326–L2339) already enforces both orderings, live and v3, at `load_all`. None of the B1 to B4 keys is a schema field, and the target models are `extra="forbid"` (`CapitalConfig` L331, `PositionSizingConfig` L461, `RiskConfig` L748, `ScoringConfig` L2296). Both group-B callers call `load_all` before the auditor (`scripts/preflight/checks/config_sanity.py` L33; `ops/control_tower/aggregator.py` L145), and the group-B docstring (L328–L332) states this design. INTERPRETATION: at the baseline schema, a file that would trigger any B finding fails `load_all` first, with `ConfigSchemaError`, so the auditor never runs. Group B can fire only when the raw and the validated values differ (for example quoted numbers, which B5 would compare as strings) or when the file changes between the two reads.

Static facts about group F at the baseline (AST of the signatures, nothing imported). `PositionSizer.__init__` (`capital/position_sizer.py` L135) has **no** default for `max_position_value_pct`, which gives the `_required` PASS. `FundManager.__init__` (`capital/fund_manager.py` L294) has default `0.03` for `daily_loss_limit_pct`. The file value of `risk.daily_loss_limit_pct` is 0.03 (`config/system_config.yaml` L316). INTERPRETATION: at the file values the F comparison would not WARN.

Exception handling. FACT: group C, G1 to G3, G5's global window parse (`_hhmm(th.entry_start)` and `_hhmm(th.entry_end)`, L746–L747, outside the per-strategy try at L751) and B5's comparison `hi > mid > lo` (L377) have no try/except around attribute access, time parsing (`_hhmm`, L676–L678) or comparison, so an exception there propagates out of `audit()`. Group E is guarded per row (L580–L583), so it does not propagate. Group A's A4 is unguarded; A5 and A3 swallow everything. The only deliberate raise is `raise_if_blocked`.

### 3.2 `audit()` and the `groups=` parameter (L772–L803)

- FACT: `groups` is a string. Each group runs if its capital letter is a substring (`"A" in groups` and so on, L789–L802). The run order is always A to G, whatever the order of the string; other characters are ignored; an empty string gives an empty report, verdict PASS.
- FACT: the docstring at L786 says "the startup path runs ACEG". The constant is `STARTUP_GROUPS = "ACG"` (L811), and the comment at L806–L810 says E is excluded.
- FACT: the `capital` parameter (L780, "reserved") is accepted and never used in the body (L788–L803).
- FACT: the auditor itself does no logging and writes no database rows or files. Its only deliberate raise is `raise_if_blocked`; the unguarded parts listed in 3.1 can still let an exception propagate out of `audit()`. Its only file reads are `_safe_load_yaml` of `system_config.yaml` and `scoring_weights.yaml` when `config_dir` is given (L834–L836).

### 3.3 Callers (non-test)

| Caller | Lines | Owner | Groups and context | What is done with the result |
|---|---|---|---|---|
| `core/config_loader.py` `SystemConfig._cross_field_sanity_checks` (model_validator "after") | L2056–L2086 (import L2072, call L2075) | A02 | `audit_system_config(self)` → "ACG", no strategies, no raw YAML | `raise_if_blocked()` (L2080). Each WARN is logged at WARNING via logger `config_sanity` (L2083–L2084). INFO and PASS are not logged. INTERPRETATION (Pydantic v2): the ValueError subclass is wrapped into a `ValidationError`, which `load_all` turns into `ConfigSchemaError("Schema validation failed for system_config.yaml", errors=...)` (L2506–L2514); `main.py` L2199–L2201 logs CRITICAL and returns **5**. It runs on every `load_all`, in every process that calls it (main, pre-flight, control tower). |
| `main.py` import | L58 | A01 | `from core.config_auditor import audit as audit_config` | — |
| `main.py` Q4(c) guard | L3436–L3443 | A01 (rule A02) | only if `structure_exit_enabled is True`; `audit_config(app_config.system, strategies=strategies, groups="A")` | keeps only the BLOCK findings with code `A4_structure_exit_trailing_sl`; CRITICAL log, `store.close()`, return **3** |
| `main.py` A5 guard | L3458–L3465 | A01 (rule A02) | only if `delivery_enabled is True`; same call | keeps only the code `A5_delivery_without_conditional_allocation`; CRITICAL log, `store.close()`, return **3**. Every other group-A finding of this strategy-aware run (for example an A3 WARN) is discarded, not logged. |
| `scripts/preflight/checks/config_sanity.py` `_build_report` | L22–L49 (call L43–L44) | A20 | `load_all(ctx.config_dir)`, `StrategyLoader().load_all_strategies(...)` (None on failure), `audit_app_config(app_config, config_dir=..., strategies=...)`, all groups; no `known_symbols` | memoised. Seven check rows A to G (L83–L133): BLOCK → `_failed`, WARN → `_warn`, else `_passed`; the detail is capped at 220 characters. Group A's criticality is CRITICAL, B, C, F and G are WARN, D and E are INFO. If `load_all` raises, every row reports "auditor unavailable: <Type>: <message>" (L46–L47, L63–L64). |
| `ops/control_tower/aggregator.py` `read_config` | L141–L167 (call L161) | A15 | the same pattern as pre-flight; no `known_symbols` | `report.actionable` becomes Findings (reason = message[:240], L162–L165); status critical, warn or ok |

Callers of `audit_app_config` from cron or other scripts. FACT: none other than the two above (git grep). How pre-flight and the control tower are scheduled is A16's and A20's.

INTERPRETATION. When a BLOCK stops `load_all`, the pre-flight and control-tower error text is the `ConfigSchemaError` message, which names only the file (`core/config_loader.py` L2509–L2510). The "CONTRADICTORY CONFIG" reason sits in the exception's `errors` context, which those two callers do not render.

### 3.4 What the auditor does not inspect that the loader loads

- AppConfig sub-configs. FACT: `audit` receives only `app_config.system` (L838–L839). `broker_costs`, `broker_limits`, `slippage`, `scoring` (only the **raw** `scoring_weights.yaml` in group B), `scan_webhook_map`, `chartink_scanners`, `nse_holidays` and `file_hashes` are not inspected.
- SystemConfig has 42 top-level fields (AST, `core/config_loader.py` L1987–L2086). The auditor reads 9 of them: `force_intraday_only`, `trade_type`, `delivery_enabled`, `structure_exit`, `capital` (`conditional_allocation_enabled`, `intraday_bucket_pct`, `leverage_map.INTRADAY` and `.COVER_ORDER`), `position_sizing` (concentration, position-value and delivery pairs, `risk_per_trade_pct`, `tier_multipliers`, `max_multiplier`, `min_tick_size`), `risk` (`daily_loss_limit_pct`, `max_open_positions`), `entry_gate.slippage_control.overrides` and `trading_hours` (`entry_start`, `entry_end`, `eod_squareoff_time`).
- The 33 SystemConfig sections it does not read: `broker`, `signal_queue`, `special_sessions`, `excluded_symbols`, `mis_filter`, `product_map`, `clock`, `order_monitor`, `kill_switch`, `webhook`, `signal_processor`, `eod_squareoff`, `alerts`, `logging`, `order_reconciler`, `eod_reconcile`, `eod_cleanup`, `tgt_retry`, `shadow_tracker`, `sr_detector`, `regime`, `portfolio_allocator`, `v3_chain`, `watchlist`, `smart_tgt`, `paper`, `drift_handler`, `circuit_breaker`, `strategy_circuit_breaker`, `live_feed`, `fno_ban`, `scanner_check_delay_sec`, `slippage_bands`.
- Parts of `trading_hours` it does not read: the `mis_squareoff_*` keys, `market_open`/`market_close`, `eod_entry_cutoff` and `service_window_end`. In particular it has no rule tying `eod_squareoff.poll_interval_sec` to `trading_hours.mis_squareoff_margin_sec` (FACT: no `mis_squareoff` text in `core/config_auditor.py`; see section 7, M-24).
- Strategies: only `enabled`, `trailing_sl_enabled`, `entry_start_time`/`entry_end_time` and whatever `strategy_will_trade` reads (A07).

---

## 4. `config_snapshotter.py`: the W0 snapshot

| Aspect | FACT (lines) |
|---|---|
| What is captured | `AppConfig.model_dump(mode="json")` (L134–L135): all 8 validated sub-configs, including schema-default fields (INTERPRETATION: `model_dump` includes defaulted fields; the loader has no `exclude=`, `SecretStr` or serializer, per a grep of `core/config_loader.py`), plus `file_hashes`. These are the effective, post-validation values of the loaded object, not the raw YAML. FACT: `main.py` was searched for assignments to `app_config...` and for `setattr`/`model_copy`; none was found, so the object snapshotted is the object loaded at L2198. |
| What is not captured | Strategies (AppConfig has no strategies field, L2426–L2434; `reports/daily_trade_review.py` L1156 and `ops_dashboard/backend/readers/config_reader.py` L10–L11 say the same), `accounts.csv`, and every other `config/` file outside the 8-file registry (section 5). Environment-variable values: only names are in the config. |
| Redaction | `redact_secrets` (L60–L83): the key contains, case-insensitively, `password`, `secret`, `token`, `api_key` or `apikey`, the key does not end in `_env`, **and** the value is a non-empty str. Non-string values (int, bool, list, dict) are never replaced; dicts and lists are recursed. Values under other keys pass through unchanged. |
| Canonicalisation | `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False)` (L98–L99). Dict keys are sorted at every level; **list order is preserved** (not sorted). Applied after redaction, so the stored string and the hash use the same redacted text. |
| Hash | SHA-256 hex of the canonical JSON encoded as UTF-8 (L102–L104) → `config_hash`. The config directory path does not take part; path-valued config fields do, because they are in the dump (for example `alerts.failed_alerts_log_path` and `alerts.sentinel_dir`, `core/config_loader.py` L1102–L1103, used at `main.py` L2631–L2632). `file_hashes` keys are bare file names (`core/config_loader.py` L2491). |
| Storage | SQLite table `config_snapshots` (`core/schema.sql` L1491–L1502, "TABLE 46", schema v41; A03): `snapshot_id` autoincrement, `snapshot_date`, `snapshot_ts`, `account_id`, `mode`, `trade_type`, `config_hash`, `config_json`; index on `snapshot_date`. **There is no UNIQUE constraint.** |
| Idempotency or "diff" | SELECT for a row with the same `(snapshot_date, config_hash)` (L189–L193). If one exists: INFO "identical snapshot already present ... skipped" and return None (L194–L200). If not: INSERT inside `store.transaction()` (L202–L211) and INFO "wrote config snapshot id=..." (L213–L216); returns the new id. The SELECT and the INSERT are two separate steps, not one transaction. `account_id` and `mode` are not part of the duplicate key. |
| How a difference is reported | The module compares nothing beyond the duplicate check: no field diff, no alert, no system_event. A changed config is just a new row. Diffs of consecutive rows are made by A15's consumers (for example `ops_dashboard/backend/readers/db_reader.py` L3324–L3349, which takes the range plus the row before it; `services/audit.py`, `services/trade_logs.py`). Report readers take the latest row of a date by `snapshot_ts DESC` (`reports/daily_trade_review.py` L349–L351, L1195–L1197, L1780–L1782; `db_reader.py` L629–L640). |
| Files added, removed, missing, unreadable or invalid | The module reads no files. A missing, unreadable or invalid registry file makes `load_all` fail first (`main.py` exit 5), so no snapshot is written; an unreadable or malformed holiday file ends the start earlier, at the holiday guard (`main.py` L2102, exit 2; A01 C10c). A comment-only or whitespace edit to a registry file changes `file_hashes` → `config_hash` → a new row (NI-6, L115–L132). A file outside the registry has no effect. The rename of the holiday file at a year change alters the `file_hashes` key, so the hash changes too (INTERPRETATION). |
| Errors | TypeError for an unsupported `app_config` type (L138–L141; the message holds only the type name). Database errors propagate to the caller. |
| Return | The new `snapshot_id`, or None |

INTERPRETATION (from L189–L200 and the consumers' `ORDER BY snapshot_ts DESC`). Take a same-day sequence of config A, then B, then A again. The third boot finds `(date, hash A)` and skips, so the latest row for the date stays B while A is loaded. In the same way, a same-day boot with an identical config but a different account or mode is skipped, and the row keeps the first boot's `account_id` and `mode`. Paper mode itself is out of scope.

### 4.1 Callers

| Caller | Lines | Owner | Detail |
|---|---|---|---|
| `main.py` import | L59 | A01 | `from core.config_snapshotter import snapshot_config` |
| `main.py` W0 | L2593–L2614 | A01 (call site) | `snapshot_config(store, app_config, snapshot_date=today_iso, snapshot_ts=time_authority.now_ist_iso(), account_id=selected_account.account_id, mode="PAPER"/"LIVE", trade_type=app_config.system.trade_type, logger=_log)` inside `try/except Exception` → ERROR "config_snapshotter: snapshot failed (non-fatal): %s" (L2613–L2614). It runs after the account and mode selection (L2528–L2582). It runs before Phase 0e subsystem construction (L2616 onwards), before the CONFIG_DIFF alert (L2656–L2675) and before the A4/A5 gates (L3436–L3465). `today_iso` is the IST date (L2255, L2266). |
| Other writers | none | — | FACT: no other non-test caller of `snapshot_config`, `redact_secrets`, `config_to_canonical_json` or `hash_config_json` (git grep) |
| Readers of the table (consumers) | `reports/daily_trade_review.py` L350, L1196, L1781, L2092; `ops_dashboard/backend/readers/db_reader.py` L631–L638, L1554–L1564, L3324–L3349, L3440, L4202; `ops_dashboard/backend/readers/config_reader.py` L33 and L231 (through `db_reader.latest_config_snapshot`); `services/audit.py`, `config_view.py`, `trade_logs.py`. Mention only: `scripts/output_retention.py` L71–L72 is a comment, with a HISTORICAL claim that the first row is dated 2026-07-02; it does not query the table. | A15 (A03 for the retention script) | Read only; internals not investigated |
| Schema and migration | `core/schema.sql` L1474–L1502; `core/migrations.py` L85–L86 | A03 | — |

---

## 5. The configuration hash used for change detection at boot (A02 side)

| Point | FACT (lines) |
|---|---|
| Hashed set | Exactly the 8 files of `_CONFIG_FILES` (`core/config_loader.py` L2441–L2450): `system_config.yaml`, `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scoring_weights.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml`, `nse_holidays_{year}.yaml` |
| Holiday-file year | `_date.today().year` evaluated **once, at module import** (L2449), from the host-local date. `check_config_files_present` uses the IST year (`utils/startup_checks.py` L859–L866). A01's C10a and C10b cover the date sources. |
| Hash method | `hashlib.sha256(path.read_bytes()).hexdigest()` on the **raw bytes**, computed before YAML parsing (L2490–L2491). The key is the bare file name. |
| Can a file drop out of the set without failing `load_all`? | **No, for the registry as coded.** Each registry file must pass `path.is_file()`, otherwise `ConfigMissingError` (L2483–L2488). The hash of every file is stored before its parse (L2491), and any parse or schema error raises (L2493–L2514). An `AppConfig` therefore always carries all 8 keys. The key set can change only (a) by a code change to `_CONFIG_FILES` or (b) at a year change, when `nse_holidays_<old>.yaml` is replaced by `nse_holidays_<new>.yaml`. No registry file is optional. |
| Files never hashed | 43 of the 51 tracked `config/` files: 16 `config/strategies/*.yaml`, 18 `config/reference_data/**` CSVs, `accounts.csv`, `accounts_multi_example.csv`, `cron_registry.yaml` (A16), `expected_managers.yaml`, `index_universe.yaml`, `preflight.yaml`, `security.yaml`, `strategy_direction_registry.yaml`, `symbol_aliases.yaml`. `instruments.csv` is required at startup (`utils/startup_checks.py` L841) but is not tracked in the tree and is not hashed. |
| Comparison (A01's code) | `check_config_hash` (`utils/startup_checks.py` L581–L634) compares against `session.last_config_hash` of the single row id=1 (`core/state_store.py` L2474–L2480), written as `json.dumps(app_config.file_hashes)` by `_write_session` (`main.py` L2308–L2314, L4174–L4180; L619–L633). `changed_files` = the **current** names whose hash differs from the stored one (L618–L622). |
| A file whose content changed | Listed. `main.py` L2656–L2675 then writes the CONFIG_DIFF system_event (details: file names only) and sends a Telegram WARN "Files: ...". A comment-only change counts, because the hash is over the raw bytes. |
| An added file | Only a new registry key can appear, for example the next year's holiday file. Its stored hash is missing (`None ≠ h`), so it is **listed as changed**. A new file elsewhere in `config/` is invisible. |
| A removed file | On disk, the boot fails at `load_all` (`main.py` L2198–L2201, exit 5) before the comparison at L2295, so no diff is made (the holiday guard before it tolerates a missing holiday file, `main.py` L2151–L2152; an unreadable or malformed one ends the start there with exit 2, A01 C10c). A key leaving the registry (the old-year holiday file) is **not listed** (L618–L622 iterates only the current set): this is A01's C7d. |
| An unreadable file | INTERPRETATION: an `OSError` from `read_bytes()` (L2490) is not caught by `load_all` (it catches only `yaml.YAMLError` and `ValidationError`); `main.py`'s `except Exception` at L2199 still gives exit 5. |
| An empty file | `safe_load` returns None → `{}` (L2502–L2504), then schema validation |
| The two hashes compared | CL4 `file_hashes` (raw bytes per file; compared with the last session only) is not the W0 `config_hash` (one SHA-256 over the redacted canonical JSON of the whole dump, `file_hashes` included; compared per date). |

---

## 6. Secret exposure paths (paths only; no value reproduced)

| Path | Assessment |
|---|---|
| `config_snapshots.config_json` (durable; travels with DB backups per the docstring L70–L72) | FACT: the full dump is stored. Secret values are not in AppConfig: the loader has no API-key field (grep), and tokens and passwords are referenced by env-var **names** (`bot_token_env` L981, `password_env` L894 and L959, `chat_id_env` L973). The live consumers read the values from the environment, for example `main.py` L2629 (`os.environ[tg_cfg.bot_token_env]`) and L3414 (`WEBHOOK_SECRET`). `SmtpConfig.password` (L890) defaults to `""`, and `system_config.yaml` has no `alerts.smtp.password` key at the baseline (YAML key scan), so it stays empty and is not redacted (only non-empty strings are). FACT (YAML scan, key paths only): stored **unredacted**, because no marker is in their key: `alerts.smtp.username`, `alerts.smtp.from_address`, `alerts.smtp.to_addresses[0]` (e-mail-address-shaped values), `webhook.bind_host` (an IP-literal value), 16 `scan_webhook_map.scanners.*.chartink_url` and 16 `chartink_scanners.scanners.*` URLs, `fno_ban.url`. Values not reproduced. FACT: `regime.index_token` matches the "token" marker but is an int, so it is never redacted (an instrument token, not a credential). INTERPRETATION: the substring rule would also redact any future non-empty string key containing "token" or "secret", and would miss a secret held under a non-matching key, inside a list of strings, inside a URL, or as a non-string value. |
| `config_snapshots.account_id` column and the snapshotter log line | FACT: `snapshot_config` logs at INFO the date, mode, **account_id**, trade_type, a 12-character hash prefix and the length (L183–L187). The skip and write lines log the date, the id and the hash prefix (L195–L199, L213–L216). The account identifier, a broker account identifier, goes to the boot log and the DB column. The docstring at L23–L27 says only "the row id, the hash prefix, and the wrote/skipped decision" are logged. Example identifiers sit in comments: `config_snapshotter.py` L168 and `core/schema.sql` L1495 (values not reproduced). |
| Snapshot failure message | `main.py` L2614 logs `%s` of the exception. INTERPRETATION: sqlite3 errors do not normally include bound parameter values, and `_resolve_config_dict`'s TypeError names only a type. No config content is expected. |
| CL4 hashes | Digests only; the CONFIG_DIFF event and the Telegram body carry file names (`main.py` L2660, L2668–L2672). No content. |
| Validator | FACT: `validate_all` logs and raises **key names** only (L244–L246, L250–L253, L259–L265). `get()` would log the expected and actual **values** at WARNING (L128–L131), but it has no caller. The in-memory `_tracked` map holds every registered value (including the empty SMTP password); it is never written out. |
| Auditor | FACT: messages and metrics embed config values (percentages, times, leverage, strategy names, the full slippage-override maps in `D_active`, scoring thresholds in B5). They go to the boot log (WARN lines from the loader, `core/config_loader.py` L2083–L2084; CRITICAL lines for A4 and A5 at `main.py` L3441 and L3463 and, for a load-time BLOCK, at `main.py` L2200), the pre-flight rows, e-mail and Telegram (A20, A14), and the control-tower findings (A15). None of the fields it reads is secret-named (section 3.4). The raw `system_config.yaml` dict that `_safe_load_yaml` reads is used only for key-presence checks. INTERPRETATION: no secret path. |
| Loader exceptions (adjacent, A02) | FACT: `ConfigSchemaError` keeps `errors=exc.errors()` in its context (L2513). `main.py` `_config_error_detail` renders only `loc` and `msg` (L2033–L2035). INTERPRETATION (Pydantic v2): each entry of `context['errors']` holds the untruncated `input`, which for `SystemConfig`'s model validator is the whole system-config mapping; only the string form of the chained `ValidationError` truncates its `input_value`s, so a traceback logged with `exc_info` (not done at L2200) would show truncated input values. INTERPRETATION (PyYAML): the "YAML parse error in {filename}: {exc}" message (L2496–L2499) includes PyYAML's problem mark, which can quote a fragment of the offending line, so YAML text near a syntax error could reach the CRITICAL boot line (L2200). |
| Boot log of the config path | `main.py` L2202 logs `config_dir` (A01). INTERPRETATION: an absolute path appears only if `--config` is given one; the tracked unit passes no `--config` (`deploy/systemd/trading-system.service` L18–L19), so the relative default is logged. |

---

## 7. A01 handoffs: config-side facts only

| A01 item | What it asks of A02 | Config-side facts | Not established |
|---|---|---|---|
| **C7d** (A01 AUDIT L722–L730; section 8 row) | Whether the hashed set (`AppConfig.file_hashes`) can lose a file without failing `load_all` | FACT: no. All 8 registry files are mandatory (`core/config_loader.py` L2480–L2488), and each is hashed before its parse (L2490–L2491). A missing file fails the boot at `main.py` L2198–L2201 (exit 5), before `check_config_hash` (L2295). The key set changes only by a code change to `_CONFIG_FILES` (L2441–L2450) or by the holiday-file year (L2449, import-time host-local date): the old-year key then disappears silently and the new-year key is listed as "changed" (`utils/startup_checks.py` L618–L622). INTERPRETATION: the removal path of C7d can occur at baseline only as this year rename, which still surfaces as a listed new file. | Whether a year rollover ever happened while the system was running: UNKNOWN |
| **S-11** (A01 AUDIT L1299–L1305; section 8 row) | The hashed set, and the W0 snapshot (L2602) | FACT: the hashed set is as above, raw bytes. W0 runs at `main.py` L2602–L2612, after the session write at L2308 and before the CONFIG_DIFF block at L2656. A boot that ends between L2308 and L2602 writes neither the event nor a snapshot. A boot that ends between L2602 and L2656 has written the snapshot but not the event. W0 rows are keyed per IST date and `config_hash`, and the hash includes `file_hashes`, so the first later boot that reaches L2602 records the changed config as a new row (unless that date already has the same hash). The snapshotter raises no alert and writes no system_event (L148–L217). INTERPRETATION: the change is preserved durably only as a new W0 row that A15's dashboard diff can show later; it is never a CONFIG_DIFF alert. If the failed boot and the next good boot fall on different dates, no row exists for the failed boot's date. | Whether such sequences happened: UNKNOWN |
| **S-24** (A01 AUDIT L511, L1985; section 8 row "placement only") | The W0 snapshot | FACT: what is captured, redaction, hash and idempotency are in section 4. Placement: after mode and account are final (L2528–L2582), before the A4/A5 exit-3 gates (L3436–L3465). INTERPRETATION: a boot that later exits 3 there has already written a snapshot row for a configuration that never reached trading. A01's note that "failed-startup have already returned" holds only for failures before L2602 is consistent with this. Failure is non-fatal (L2613–L2614). | — |
| **W-17** (A01 AUDIT L514, L1988; section 8 row) | `validate_all(strict=False)` | FACT: `strict=False` makes the **unaccessed** branch warn-only (L248–L255). The **drift** branch raises `ConfigValidationError` whatever `strict` is (L257–L266). A01's M-24 (L1678) records the drift raise as an exit-1 path; W-17 records "warn-only". FACT: drift needs `accessed=True`, set only in `get()` (L121, L136), and no non-test code calls `get()` (git grep; tests call it on their own instances). INTERPRETATION: at baseline the drift raise cannot occur, so the call is effectively warn-only (W-17 holds in effect), and M-24's `ConfigValidationError` exit-1 path is unreachable at baseline. Every registered key is reported unaccessed on each boot that reaches L4164. | The actual WARNING content and the key count N: UNKNOWN (nothing was run) |
| **M-24** (A01 AUDIT L1674–L1681; section 8 row) | A02's part: the MIS timing validation and `MisSquareoffConfigError` | FACT: `TradingHoursConfig._validate_mis_squareoff_timing` (`core/config_loader.py` L109–L137) calls `MisSquareoffTiming.build(...)` with **literal `poll_interval_sec=5`** (L131) and re-raises `MisSquareoffConfigError` as ValueError (L135–L136; at load this gives `ConfigSchemaError`, exit 5). The runtime build at `main.py` L3329–L3337 (and the notifier at L3343–L3345) passes `app_config.system.eod_squareoff.poll_interval_sec`. Schema: `EodSquareoffConfig.poll_interval_sec: int` (L648) with validator `>= 1` (L676–L681). In `build` (`core/mis_squareoff_timing.py` L103–L159, A12), the checks that depend on the poll interval are L125–L128 (positive int) and **L129–L138 (`margin_sec >= poll_interval_sec`)**. All other checks see identical inputs. `MisSquareoffConfigError` subclasses ValueError only (L36), outside `TradingSystemError`. No SystemConfig-level validator and no auditor rule ties `eod_squareoff.poll_interval_sec` to `trading_hours.mis_squareoff_margin_sec` (grep). File values: `mis_squareoff_margin_sec: 20` (`config/system_config.yaml` L96) and `eod_squareoff.poll_interval_sec: 5` (L361). INTERPRETATION: a configuration with `eod_squareoff.poll_interval_sec` greater than the margin passes `load_all` and raises at `main.py` L3329, giving exit 2 through the guard (L4291–L4293). At the file values (5 ≤ 20) both checks pass, so the path is latent, as A01 says. HISTORICAL: L131 dates from commit `6f00b4d` (2026-08-28, git blame). | Whether any deployed configuration had poll > margin: UNKNOWN |

Other A01 rows that name A02 (C10a, C10b, C12, C35, M-19/M-20) are outside the scope of this file and are not covered here.
