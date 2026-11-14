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
