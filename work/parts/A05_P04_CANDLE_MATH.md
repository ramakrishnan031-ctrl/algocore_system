# A05 STUDY part P04: `core/candle_math.py` — functions, candle contract, calculations and callers

**Status:** WORKING DRAFT (helper output; not a project record)

**Baseline:** trading-system-prod-snapshot, branch main, commit 970aabf3c78d777d9d34549e021f7c8e756c7bdb

**Scope:** `core/candle_math.py` in whole (L1 to L456): module header and imports, the `Candle` type it expects and the attributes it reads, its constants, and every function and class (`true_range_series`, `atr`, `session_vwap`, `ema_series`, `ema`, `adx` with its inner `_wilder`, `rsi`, `SessionBounds`, `ResampleResult` with `partial_last`, `resample` with `_bounds_for`): signatures, defaults, formulas as implemented, short-input and edge handling, rounding, units, ordering, gaps, time zone and session bounds. Every non-test importer and call site (arguments passed, and the type and origin of the candles passed in, stopping at the boundary). The two `resample` comments outside the module. The tests of the module (HISTORICAL). Other implementations of the same calculations in non-test code (neutral facts). The A04 CG-27 tick-size point, and the A05 boundary with A08, A15 and A18 under Rama's decision B of 14-Nov-2026: A05 records implementation and boundary facts; A08 and A18 keep the use and technical meaning of their own calculations. Live only.

## 1. Scope, files read and method

P04-S001. FACT (method): every legacy statement below cites path and line(s) at baseline `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (written `970aabf` from here on). The local clone's HEAD equals `970aabf` (checked with `git rev-parse HEAD`). Legacy files were read only with `git show 970aabf:<path>` (copied to this part's scratch folder for line-numbered reading), `git grep -n -E ... 970aabf` with the mandatory exclusion pathspecs, and `git log` (hashes and dates only). Nothing legacy was run, imported, built or tested. No broker, API or network call was made.

P04-S002. FACT (method): the formulas and edge cases below are read from the source text. Statements about what an expression does with particular values (for example `float(None)`, an empty list, mixed naive and aware datetimes) are INTERPRETATION from Python semantics, with the basis stated; no legacy code and no re-implementation of it was executed.

P04-S003. FACT (files read in whole): `core/candle_math.py` L1 to L456 (Git blob `57e69c5973ae29a04633bce90537448c7b3778f0`, 21275 bytes, as in the A05 source file inventory, evidence `A05_SOURCE_FILE_INVENTORY_2026-11-14.md` section 1); `sr_detector/models.py` L1 to L207 (boundary evidence only: the `Candle` type).

P04-S004. FACT (files read in part, at the boundary only): to be completed as the caller sections are written (section 11 lists each caller's lines).

P04-S005. FACT (search patterns used, all with the mandatory exclusions): repository-wide `candle_math` (non-test, non-document, and again including tests and documents); non-test `\b(true_range_series|session_vwap|ema_series|ResampleResult|partial_last|partial_bucket_starts|empty_bucket_starts|ATR_WILDER|ATR_SMA|DAILY_TF|SessionBounds)\b` and `\bresample`; in the six importing files, `\b(_?atr|_?adx|rsi|ema|ema_series|true_range_series|session_vwap)\(` and the same names as whole words (to catch a function passed without a call); in `core/candle_math.py`, `tick|round|decimal|precision|tz|zone|IST|09:15|15:30` (case-insensitive). Further patterns are listed in the sections that use them.

P04-S006. FACT (project records read, read-only): the Master System Investigation Index, entries A05, A08, A15 and A18 and Appendix A (owners of `scripts/`); the A05 source file inventory (evidence `A05_SOURCE_FILE_INVENTORY_2026-11-14.md`, sections 1, 4 and 5); the A04 AUDIT of 2026-11-13, the CG-27 match record and section 14.5 (handoffs to A05).

## 2. The module: header, imports, the `Candle` contract, constants and history

P04-S007. HISTORICAL (`core/candle_math.py` L1 to L7, the header comment): "Domain-agnostic, PURE candle math for the V3 Shared-Engine "Common Utilities" substrate", with "Two genuinely-new helpers that did not exist anywhere before (Phase-0 gap): (1) True Range series + ATR (Wilder / SMA) from OHLC candles. (2) Timeframe RESAMPLE (base bars -> higher timeframe)."

P04-S008. HISTORICAL (L9 to L16): the header says the functions are "Pure functions over the SHARED OHLCV `Candle` value object (sr_detector.models.Candle — the single candle type in the codebase; NO parallel type is defined here)", with "No I/O, no globals, no clock, no broker, no config read, no mode branch — deterministic and identical in paper and live by construction", and that session boundaries for `resample` are injected by the caller ("derive them from core.market_windows") so that the module "never hardcodes 09:15".

P04-S009. HISTORICAL (L17 to L20): "Inputs : Sequences of Candle (chronologically ordered); an ATR period; a target timeframe + session bounds for resample." "Outputs : float | None (atr), list[float] (true_range_series), ResampleResult (resample)." FACT (L136, L165, L184, L191, L250): the module also defines `session_vwap`, `ema_series`, `ema`, `adx` and `rsi`, which the header's purpose, inputs and outputs lines do not name.

P04-S010. HISTORICAL (L28 to L31): "Wiring : NONE yet (V3 Step 1 is build + unit-test only). Nothing in the live trading / scoring / sizing / S&R path consumes these functions; later modules (03.01 S&R, 03.02 Regime, 03.06 Sizing) wire them in and own the config defaults." FACT (section 10; `git blame -s`): at `970aabf` six non-test modules import functions of this module; the header lines L1 to L245 come from commit `536172c` (2026-07-12), the same commit that added the imports in `regime/engine.py` L26 and L28 and in `sr_detector/zone_builder.py` L16. The header was not changed afterwards (L1 to L32 blame to `536172c`). Whether any importing path ran in production is UNKNOWN / NOT ESTABLISHED.

P04-S011. FACT (L33 to L42): the imports are `from __future__ import annotations`; `dataclass`; `date` (as `_date`), `datetime`, `time`, `timedelta`; and the typing names `TYPE_CHECKING`, `Callable`, `List`, `Optional`, `Sequence`, `Tuple`, `Union`. `Candle` is imported from `sr_detector.models` only inside `if TYPE_CHECKING:` (L39 to L42). INTERPRETATION (Python semantics: `typing.TYPE_CHECKING` is false at run time, and with postponed evaluation of annotations the `"Candle"` annotations are never evaluated): at run time the module imports only standard-library names. The only run-time reference to the `sr_detector` package is the function-local `from sr_detector.models import Candle` inside `resample` (L376), executed on each call of `resample`.

P04-S012. FACT (L33 to L42, L376; the case-insensitive search of section 1): the module imports no `math`, `decimal`, logging, configuration, clock or broker module. It writes no log line, holds no mutable module-level state, reads no tick size, applies no rounding and performs no time-zone conversion. Its module-level names are the eight functions, the dataclass `ResampleResult`, the constants `ATR_WILDER`, `ATR_SMA` and `DAILY_TF`, and the type alias `SessionBounds`.

P04-S013. FACT (`sr_detector/models.py` L23 to L43; A08's file, read as boundary evidence): the `Candle` type is a frozen dataclass with six fields, `ts: datetime`, `open: float`, `high: float`, `low: float`, `close: float` and `volume: int`. HISTORICAL (L25, its docstring): "One OHLCV bar. ts is timezone-aware (or naive IST) datetime." FACT (L33 to L43): `Candle.from_kite(row)` sets `ts=row["date"]` unchanged, `open`, `high`, `low` and `close` with `float(...)`, and `volume=int(row.get("volume") or 0)`. INTERPRETATION (dataclass semantics): the field annotations are not enforced at run time, so a `Candle` holds whatever values its constructor is given; `from_kite` converts the prices and the volume but not the timestamp.

P04-S014. FACT (L54 to L456): the attributes each function reads.

| Function | Attributes read from each input object | Notes |
|---|---|---|
| `true_range_series` | `high`, `low`, `close` (L72, L73, L79) | |
| `atr` | none directly; through `true_range_series` (L117) | |
| `session_vwap` | `volume`, `high`, `low`, `close` (L150, L153) | |
| `ema_series`, `ema` | none: they take plain numbers (L165, L173, L184) | callers pass closes |
| `adx` | `high`, `low`, `close` (L209 to L217) | |
| `rsi` | `close` (L271) | |
| `resample` | `ts`, `high`, `low`, `close`, `open`, `volume` (L394, L412 to L414) | constructs `Candle(ts=..., open=..., high=..., low=..., close=..., volume=...)` (L427) |

The timestamp attribute is `ts`; only `resample` reads it, and only `resample` reads `open`.

P04-S015. INTERPRETATION (Python attribute access; P04-S011, P04-S014): no function checks the type of the objects it receives; any object with the attributes in P04-S014 is accepted. FACT (`data/candle_store.py` L24 to L36; part P03's subject, read for the interface only): the live candle record `CandleData` has the same six attribute names (`open`, `high`, `low`, `close`, `volume`, `ts`) plus `instrument_token`, `symbol`, `interval_sec` and `is_synthetic`. HISTORICAL (L34, a field comment): `ts` is the "IST candle close time (from clock thread)"; (L36): `is_synthetic` is "True for flat carry-forward candles". FACT (P04-S014): no function of the module reads `is_synthetic` or `interval_sec`. Whether any caller passes `CandleData` objects: section 10 (none does).

P04-S016. FACT (constants): `ATR_WILDER = "wilder"` (L50); `ATR_SMA = "sma"` (L51); `DAILY_TF = "day"` (L298); `SessionBounds` (L303 to L306) is either a `(time, time)` tuple or a callable from a date to such a tuple. The module defines no session time. `atr`, `ema_series` and `ema` have no default period; `adx` and `rsi` have `period: int = 14` (L191, L250). HISTORICAL (L92 to L93, `atr`'s docstring): "no default period is baked in here; any default belongs in config, at the wiring site." FACT (the non-test search of section 1): `DAILY_TF` is not used anywhere after its definition; `resample` tests `target_tf` against the literal tuple `("day", "daily")` (L378).

P04-S017. FACT (`git log` and `git blame -s` at `970aabf`): two commits touch the file, `536172c` (2026-07-12; lines L1 to L245 and L293 to L456) and `3c85512` (2026-07-13; lines L246 to L292, the `rsi` block). HISTORICAL (commit subjects): "feat(v3): shared engine 03.01-03.09 + portfolio allocator — all default-OFF (byte-identical)"; "feat(m-s4): rsi() helper + Q3 sizing & Q2.5 expectancy autopsy reports". FACT (`git diff --stat 7d4970a 970aabf -- core/candle_math.py sr_detector/models.py`, empty; agrees with the A05 source file inventory, section 5): both files are identical at the last recorded deployment commit `7d4970a` and at the baseline. UNKNOWN / NOT ESTABLISHED: whether production ever ran this file.
