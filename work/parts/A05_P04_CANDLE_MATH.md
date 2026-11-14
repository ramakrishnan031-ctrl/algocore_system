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

P04-S010. HISTORICAL (L28 to L31): "Wiring : NONE yet (V3 Step 1 is build + unit-test only). Nothing in the live trading / scoring / sizing / S&R path consumes these functions; later modules (03.01 S&R, 03.02 Regime, 03.06 Sizing) wire them in and own the config defaults." FACT (section 10; `git blame -s`): at `970aabf` six non-test modules import functions of this module. The header (L1 to L32) blames to commit `536172c` (2026-07-12), the same commit that added the imports in `regime/engine.py` L26 and L28 and in `sr_detector/zone_builder.py` L16; no later commit changed the header. Whether any importing path ran in production is UNKNOWN / NOT ESTABLISHED.

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

## 3. True range and ATR: `true_range_series` and `atr`

P04-S018. FACT (L54 to L80): `true_range_series(candles: Sequence["Candle"]) -> List[float]`. For each candle, in input order, it takes `high = float(c.high)` and `low = float(c.low)` (L72 to L73). For the first candle, `TR_0 = high - low` (L74 to L75). For every later candle, `TR_t = max(high_t - low_t, |high_t - close_(t-1)|, |low_t - close_(t-1)|)` (L76 to L77), where `close_(t-1)` is `float(close)` of the previous element of the input (L79). It returns a list of the same length as the input, and `[]` for an empty input (L69, L80). It does not sort, does not read `ts`, and does not check order, duplicates or gaps.

P04-S019. HISTORICAL (L61 to L62, docstring): the first value is "a degenerate "range", not a true range — atr() excludes it". HISTORICAL (L66 to L67): "Candles are processed in the given order and never re-sorted (caller supplies chronological order)."

P04-S020. INTERPRETATION (Python semantics, L72 to L79): the "previous close" is the previous list element, whatever time separates the two candles; a missing bar, a session break or a day break is not detected. The first value is negative if a candle has `high < low`; every later value is non-negative, because two of the three terms are absolute values. A `None` in `high`, `low` or `close` raises `TypeError` (from `float(None)`); a numeric string is converted silently by `float`.

P04-S021. FACT (L83 to L113): `atr(candles, period, method=ATR_WILDER) -> Optional[float]`. It raises `ValueError` when `period` is not an `int`, is a `bool`, or is not positive (L108 to L109), and when `method` is not exactly `"wilder"` or `"sma"` (L110 to L113; a case-sensitive comparison). `period` has no default.

P04-S022. FACT (L114 to L118): when `len(candles) < period + 1` it returns `None` (L114 to L115). Otherwise it computes `true_range_series(candles)` and drops the first value: `real = trs[1:]` (L117 to L118), so `len(real) = len(candles) - 1 >= period`.

P04-S023. FACT (L121 to L123): `method="sma"` returns `sum(real[-period:]) / period`, the plain mean of the last `period` true ranges.

P04-S024. FACT (L125 to L129): `method="wilder"` (the default) seeds `ATR = sum(real[:period]) / period` (the mean of the first `period` true ranges, L126), then for each later true range applies `ATR = (ATR * (period - 1) + TR) / period` (L127 to L128), and returns the final value (L129). HISTORICAL (L96 to L98): "Seed = mean of the first ``period`` prev-close true ranges; then ``ATR_t = (ATR_{t-1} * (period - 1) + TR_t) / period``." The docstring and the code agree.

P04-S025. FACT (L117 to L129): the result is a Python `float` at full precision; nothing is rounded. INTERPRETATION (the formula): it is in the price units of the candles (a mean of price differences). The `"sma"` value depends only on the last `period + 1` candles. The `"wilder"` value depends on every candle passed, because the seed is taken at the start of the input and each later candle enters the recursion; the same instrument and period give different values for different lookback lengths or start dates, and the effect of the seed decays geometrically by `(period - 1) / period` per later candle.

P04-S026. INTERPRETATION (Python semantics, L114): `len(candles)` requires a sized sequence; a generator raises `TypeError`. A non-numeric value raises in `true_range_series` (P04-S020). Nothing in `atr` catches an exception; error handling is the caller's (section 10).

## 4. Volume-weighted average price: `session_vwap`

P04-S027. FACT (L136 to L158): `session_vwap(candles) -> Optional[float]`. For each candle it takes `v = float(c.volume)` (L150) and skips the candle when `v <= 0.0` (L151 to L152). Otherwise it adds `typical * v` to a numerator and `v` to a denominator, with `typical = (float(high) + float(low) + float(close)) / 3.0` (L153 to L155). It returns `None` when the total volume is not positive (L156 to L157), which covers an empty input and an input whose volumes are all zero or negative; otherwise it returns `numerator / denominator` (L158). Formula: VWAP = Σ(((high + low + close) / 3) × volume) / Σ(volume), over the candles with positive volume.

P04-S028. FACT (L149 to L158): the function reads no `ts` and no `open`, and filters nothing by date or time; the word "session" in its name is not enforced by the code. HISTORICAL (L142 to L144, docstring): "The caller scopes `candles` to the intended session/window (e.g. today's in-session bars) — this function is a pure reducer over whatever it is given". The one non-test caller scopes the candles itself (section 10, call 9).

P04-S029. INTERPRETATION (the formula): the value is a typical-price approximation per bar, weighted by bar volume; it is not the exchange's average traded price. A candle with a negative volume is skipped, not rejected. Nothing is rounded; the result is in the candles' price units. A `None` volume raises `TypeError` (from `float(None)`, L150); a `None` price raises only on a candle with positive volume, because the prices of a skipped candle are not read (L151 to L153).

## 5. Exponential moving average: `ema_series` and `ema`

P04-S030. FACT (L165 to L181): `ema_series(values: Sequence[float], period: int) -> List[float]` takes plain numbers, not candles. It raises `ValueError` for a `period` that is not an `int`, is a `bool`, or is not positive (L171 to L172). It converts every value with `float` (L173) and returns `[]` when there are fewer values than `period` (L174 to L175). Otherwise: smoothing factor `k = 2 / (period + 1)` (L176); seed = `sum(vals[:period]) / period`, the simple mean of the first `period` values (L177); then, for each later value `v`, `EMA_t = v × k + EMA_(t-1) × (1 - k)` (L178 to L180). The list has `len(values) - period + 1` elements; its first element belongs to input index `period - 1`.

P04-S031. FACT (L184 to L188): `ema(values, period) -> Optional[float]` returns the last element of `ema_series(values, period)`, or `None` when that list is empty. It has the same validation (through `ema_series`) and no default period.

P04-S032. INTERPRETATION (Python semantics, L173): `values` can be any iterable of numbers or numeric strings; `None` raises `TypeError`. As with the Wilder ATR (P04-S025), the result depends on the whole input, because the seed is taken at the start; the seed's weight decays by `(1 - k)` per later value. Nothing is rounded. Every non-test caller passes candle closes (section 10).

## 6. Average directional index: `adx` and its inner `_wilder`

P04-S033. FACT (L191 to L202): `adx(candles, period: int = 14) -> Optional[float]`. It raises `ValueError` for an invalid `period` (same rule as `atr`, L198 to L199) and returns `None` when `len(candles) < 2 × period + 1` (L200 to L202). HISTORICAL (L192 to L194): "Requires at least ``2*period + 1`` candles so the DX series is long enough to seed + smooth the ADX."

P04-S034. FACT (L204 to L217): for each candle `i` from the second onwards, with `prev` the previous list element: `up = high_i - high_(i-1)` and `dn = low_(i-1) - low_i` (L209 to L210); `+DM_i = up` if `up > dn` and `up > 0`, else `0.0` (L211); `-DM_i = dn` if `dn > up` and `dn > 0`, else `0.0` (L212); `TR_i = max(high_i - low_i, |high_i - close_(i-1)|, |low_i - close_(i-1)|)` (L213 to L217). Each of the three lists has `len(candles) - 1` elements. When `up` equals `dn`, both directional movements are `0.0` (strict comparisons).

P04-S035. HISTORICAL (L194 to L195): "Uses true_range_series for TR (reuse, no duplication)." FACT (L213 to L217; the only call of `true_range_series` in the module is at L117, inside `atr`): `adx` does not call `true_range_series`; it computes the true range inline. INTERPRETATION (comparison of L77 with L213 to L217): the inline expression is the same formula as `true_range_series` uses for every candle after the first, so `adx`'s true ranges equal `true_range_series(candles)[1:]`; the difference is in the reuse claim only.

P04-S036. FACT (L219 to L227): the inner `_wilder(x)` returns a running Wilder total, not an average: `S_0 = sum(x[:period])` (L220 to L221), then `S_t = S_(t-1) - S_(t-1) / period + x_t` for each later element (L222 to L224); it returns `len(x) - period + 1` values. It is applied to `+DM`, `-DM` and `TR` (L227). INTERPRETATION (algebra): dividing by `period` gives the average-form recursion `A_t = A_(t-1) × (period - 1) / period + x_t / period`, so the ratios formed next are the same as with Wilder averages.

P04-S037. FACT (L228 to L236): for each triple of smoothed values: if the smoothed `TR <= 0.0`, `DX = 0.0` (L230 to L232); otherwise `+DI = 100 × S(+DM) / S(TR)`, `-DI = 100 × S(-DM) / S(TR)` (L233 to L234), and `DX = 100 × |+DI - -DI| / (+DI + -DI)` when the sum is positive, else `0.0` (L235 to L236).

P04-S038. FACT (L238 to L243): if fewer than `period` DX values exist it returns `None` (L238 to L239); otherwise `ADX` is seeded with the mean of the first `period` DX values (L240) and smoothed with `ADX = (ADX × (period - 1) + DX) / period` over the remaining DX values (L241 to L242); the final value is returned (L243), unrounded. INTERPRETATION (arithmetic on P04-S033, P04-S034, P04-S036): with `n >= 2 × period + 1` candles there are `n - period >= period + 1` DX values, so the check at L238 cannot be true when it is reached; with exactly `2 × period + 1` candles one smoothing step follows the seed.

P04-S039. INTERPRETATION (the formula): each DX lies between 0 and 100 because both directional movements are non-negative, so the ADX, a weighted mean of DX values, lies between 0 and 100; it is dimensionless. Like the Wilder ATR, it depends on every candle passed (P04-S025). A run of candles with zero range gives smoothed `TR = 0` and `DX = 0.0` (L230 to L232), not an error.
