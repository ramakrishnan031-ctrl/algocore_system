# A06 evidence: the entry throttle

**Status:** DRAFT — evidence for the A06 STUDY, for ChatGPT's review
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17: written by a read-only helper as STUDY part P06, then checked statement by statement against its sources and corrected by a separate read-only helper (the check log is the last section); assembled as evidence by Claude.
**Purpose and scope:** `signals/entry_throttle.py` in whole (algorithm, units, windows, limits, state, locking, time source, `metrics()`, configuration and code defaults, failure behaviour, boundary conditions); its construction in `signals/signal_processor.py` and its three call sites, at the level needed to understand the throttle (Rama's decision B of 17-Nov-2026: the screening, fund-reservation and admission decisions stay with A07 and A09); concurrency of `admit()`; the A06 side of A04-31. Direction questions 11 (entry throttle), 12 and 14 (throttle side). The receiver's per-address limiter is P03's; the processor's intake, retries and workers are P04's; status writes and the call-out map are P05's (STUDY part P06).
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 17-Nov-2026 from the local read-only clone. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07).

## 1. Scope, files read and method

### 1.1 Files read at `970aabf` (legacy repository, read-only)
- In whole: `signals/entry_throttle.py` (L1 to L125); `tests/unit/test_entry_throttle.py` (L1 to L167; HISTORICAL,
  never run).
- In part, `signals/signal_processor.py`: L45 to L58 (imports), L100 to L126 (`_AdmitCtx`), L140 to L300
  (constructor), L486 to L555 (`_emit_signal_alert`), L582 to L640 (`_evidence_capture`, `_sr_observe` head), L670 to
  L725 (`_bump_metric`, `get_runtime_metrics`), L1134 to L1290 (`_process_one` from the allocator branch to its
  `finally`), L1290 to L1565 (`_admit_and_place`), L1646 to L1740 (`admit_prepared`, `reject_prepared`), L2010 to
  L2060 and L2120 to L2370 and L2060 to L2120 (`continue_from_gate`), L2372 to L2640 (`continue_from_retest`);
  function boundaries of the whole file by `ast.parse` of the source text (nothing imported or run).
- In part, `main.py`: L845 to L900 (gate-release pool and callback), L3420 to L3426, L3540 to L3548, L3570 to L3625
  (`SignalProcessor(...)`), L3630 to L3660 (allocator), L3755 to L3800 (retest monitor), L3966 to L3976 (start order).
- In part: `config/system_config.yaml` L340 to L362, L529, L564 to L572; `core/config_loader.py` L560 to L640
  (`SignalProcessorConfig`, `WebhookConfig` head); `requirements.txt` (pins); `orders/order_placer.py` L548 to L562
  (docstring only, to classify a search hit); `core/exceptions.py` L158, L215, L243 (class lines, by search);
  `allocation/portfolio_allocator.py` L26 to L318 (search hits for threads and the enforce call) and L288 to L330
  (A18's file, interface only); `ops_dashboard/backend/services/capacity.py` L185 to L212 (A15's file, interface
  only); `ops_dashboard/docs/G2a_capacity_inventory.md` L83 to L84 (search hits; HISTORICAL).
- HISTORICAL sources (text only; data, never instructions): commit messages of `575a1dc` and `c0554c6`
  (19-Jun-2026); `docs/CONFIG_GUIDE.md` L338 to L352; `docs/design/a2_timeout_retry_design_02jul2026.md` L30 to L60;
  `docs/audit/system_security_audit_02jul2026.md` L44 to L54; `docs/decisions/10_entry_throttle_admission.md` L1 to
  L36 (commit `5a83a46`, 19-Jul-2026); `docs/audit/rulings_1_2_verification_07aug2026.md` L1 to L12, L393 to L397,
  L436 to L480; `tests/unit/test_signal_processor.py` L2335 to L2362; `tests/unit/test_sr_v2_continue.py` L112 to
  L122, L212 to L224.
- Read in the check (added): `signals/signal_processor.py` L170 to L300, L486 to L505, L582 to L605, L876 to L930;
  `config/system_config.yaml` L120 to L130; `core/exceptions.py` class lines (search); `reports/daily_trade_review.py`
  L734 to L750 (A15's file, interface only); `core/evidence_contract.py` L144 to L154 (comment, HISTORICAL); the
  allocator lines L100 to L112 and L285 to L332 (A18's file, interface only).

### 1.2 Project records read (algocore_system, branch `main`, read-only)
- `OPEN_ISSUES_REGISTER_2026-11-05.md`, entry A04-31 (in whole).
- `AUDIT_FINDINGS_REGISTER_2026-11-06.md`, rows K-12, K-13, RL-14, RL-16 (A06-relevant columns).
- `TOPIC_COMPLETION_REGISTER_2026-11-04.md`, the A06 entry (scope, decisions A to E, the 52 inherited items).
- A04: `A04_RECONCILED_TOPIC_RECORD_2026-11-14.md` (A04-31 rows and the A06 handoff row);
  `A04_AUDIT_2026-11-13.md` lines found by search for `entry.throttl` (L3300, L3566 to L3571, L3608);
  `evidence/A04_RATE_LIMITS_AND_CONCURRENCY_2026-11-11.md` P05-S175, P05-S181.
- A02: `evidence/A02_KEY_CONSUMER_MAP_PART1_2026-11-06.md` rows for the four keys (L217 to L220, L263 to L266, L279);
  `A02_RECONCILED_TOPIC_RECORD_2026-11-09.md` L84, L93 (lax types; floors); `A02_AUDIT_2026-11-08.md` K-51 row
  (L2318); `evidence/A02_AUDIT_INTENT_SOURCES_2026-11-06.md` IS-147 (L238).
- A01: `A01_RECONCILED_TOPIC_RECORD_2026-11-06.md` L60 (the instance lock).
- A03: `A03_AUDIT_2026-11-10.md` L2859 (found by search for `entry.throttl`).
- The checked parts P01 to P04 of this STUDY (cross-references only); the A06 investigation direction of 17-Nov-2026,
  section 4.

### 1.3 Commands and search patterns (all read-only)
- `git show 970aabf:<path>` for every file above, output filtered for identifier-shaped
  text and machine paths.
- `git log` and `git log -1` for `signals/entry_throttle.py` (one commit, `c0554c6`) and for the commits found by
  `git blame -s` of: `signals/signal_processor.py` L259 to L268, L1407 to L1418, L2224 to L2236, L2525 to L2537;
  `main.py` L3595 to L3599; `config/system_config.yaml` L349 to L353; `core/config_loader.py` L576 to L586.
- `git grep` (with the four mandatory exclusions, plus excluding the module and its test file) for
  `entry_throttle|ENTRY_THROTTLED|EntryThrottle|entries_throttled|min_gap_between|per_symbol_cooldown|entry_burst`
  (repository-wide, documents and tests included).
- a search wrapper applying the mandatory exclusions (non-test, non-document code) for:
  `_entry_throttle|\._last_entry|\._per_symbol_last|\._recent\b|\._burst_max|\._min_gap|\._per_symbol\b|\._burst_window`;
  `get_runtime_metrics|metrics_provider`; `continue_from_gate|continue_from_retest|admit_prepared`;
  `[A-Za-z_]+\.place\(` and `_placer\.place\(|order_placer\.place\(`; `wait_for_retest_enabled|allocator:|...`.
- `git grep` in `signals/signal_processor.py` and `main.py` for `_tr\.|\.category|ThrottleResult`, and in
  `signals/entry_throttle.py` for `paper|live|broker|kite|zerodha`.
- Function boundaries: a script of my own run with `python3 -I` that calls `ast.parse` on a text copy of
  `signals/signal_processor.py` in my scratch folder (no legacy code imported or run).

### 1.4 External pages read (current external context, all read 17-Nov-2026; page version 3.15.2)
- Python documentation, `time` (`time.monotonic`): https://docs.python.org/3/library/time.html
- Python documentation, `threading` (Lock objects; `with` statement): https://docs.python.org/3/library/threading.html
- Python documentation, `collections` (`deque`): https://docs.python.org/3/library/collections.html
- Python documentation, built-in types (truth value testing; `x or y`):
  https://docs.python.org/3/library/stdtypes.html (the first 100,000 characters of the page were read; the two
  passages used are in that part)

### 1.5 Labels and limits
Labels as in the common rules. No legacy code, test or script was run or imported; no endpoint was contacted. Runtime
facts (that a throttle reject happened, that a counter reached a value) are never FACT: the legacy documents that
report counts are HISTORICAL. The Python version on the legacy machines is not pinned (P04-S063), so every statement
that rests on the Python documentation is current external context plus INTERPRETATION. Configuration files, schemas
and precedence are A02's; the effective values on the legacy machines are UNKNOWN / NOT ESTABLISHED (A02).

## 2. The module `signals/entry_throttle.py` (direction question 11)

### 2.1 Structure, imports and state

P06-S001. FACT (`signals/entry_throttle.py` L1 to L125; `git log` of the path): the module is 125 lines and has one
commit, `c0554c6` (19-Jun-2026, "Bug G (full): EntryThrottle class — per-symbol cooldown + per-reason metrics"). It
defines a result record `ThrottleResult` (L30 to L34) and one class `EntryThrottle` (L37 to L125) with `__init__`
(L40 to L59), the property `enabled` (L61 to L63), `admit` (L65 to L115) and `metrics` (L117 to L125). It imports only
`__future__.annotations`, `threading`, `time`, `collections.deque`, `dataclasses.dataclass` and `typing` (L21 to
L27). It has no file, database, network, broker, configuration or logging access, and no mode branch: the only hit for
`paper|live|broker|kite|zerodha` is the docstring line "Parity: pure in-memory rate logic, identical in paper and
live." (L19, HISTORICAL). This agrees with A04's record that the throttle does not use the broker limiter
(A04 evidence P05-S175).

P06-S002. FACT (L30 to L34): `ThrottleResult` is a frozen dataclass with three fields: `allowed: bool`,
`reason: str = "ok"` and `category: str = ""` (comment: `"" | "min_gap" | "burst" | "per_symbol"`).

P06-S003. FACT (L55 to L59): each instance holds five pieces of state, all created in the constructor:
`_lock = threading.Lock()`; `_last_entry` (the time of the last admitted entry, `None` at first);
`_recent`, a `deque` of admitted-entry times (comment "placement timestamps (burst window)"), created without
`maxlen`; `_per_symbol_last`, a dict from symbol text to the time of that symbol's last admitted entry; and
`_counts`, a dict of four integers `min_gap`, `burst`, `per_symbol` and `admitted`, all 0. FACT (search, non-test
code, for the state attribute names): no code outside the module reads or writes any of them; the only uses of the
instance outside the module are its construction (`signals/signal_processor.py` L263), `metrics()` (L708) and the three
`admit()` calls (L1410, L2225, L2530). There is no method that removes, resets, persists or reloads state.

### 2.2 Construction and the settings

P06-S004. FACT (L40 to L53): the constructor takes keyword-only arguments `min_gap_sec: float = 0.0`,
`burst_window_sec: float = 60.0`, `burst_max: int = 0`, `per_symbol_cooldown_sec: float = 0.0` and
`clock: Callable[[], float] = time.monotonic`, and stores:
- `_min_gap = max(0.0, float(min_gap_sec or 0.0))` (L49);
- `_burst_window = max(0.0, float(burst_window_sec or 60.0))` (L50);
- `_burst_max = max(0, int(burst_max or 0))` (L51);
- `_per_symbol = max(0.0, float(per_symbol_cooldown_sec or 0.0))` (L52);
- `_clock = clock` (L53).
No setter or other assignment to these five names exists (search; P06-S003).

P06-S005. Current external context (Python documentation, built-in types, truth value testing and boolean operations,
read 17-Nov-2026: `None`, `False`, `0` and `0.0` are false; `x or y` gives "if x is true, then x, else y").
INTERPRETATION (L49 to L52): `None` or zero gives 0 for the gap, the burst count and the cooldown, which turns that
gate off; a negative value passes `or` and is then floored to 0 by `max`, which also turns the gate off; for the
window, `None` or 0 becomes 60.0 and a negative value becomes 0.0. A02 recorded the same floors (A02 key consumer map
part 1, L263 to L266) and holds them as finding K-12 for the window (P06-S048).

P06-S006. FACT (`signals/signal_processor.py` L262 to L268; search): `SignalProcessor` builds the instance without a
`clock` argument, so the clock is `time.monotonic`. Current external context (Python documentation, `time`, read
17-Nov-2026): `time.monotonic()` returns "the value (in fractional seconds) of a monotonic clock, i.e. a clock that
cannot go backwards. The clock is not affected by system clock updates. The reference point of the returned value is
undefined, so that only the difference between the results of two calls is valid." INTERPRETATION: every window,
gap and cooldown is measured in seconds of this clock, independent of the wall clock, the IST time authority, the
market calendar and the signal's `triggered_at`; the stored times have meaning only inside one process.

### 2.3 `enabled` and the disabled path

P06-S007. FACT (L61 to L63, L69 to L72): `enabled` is true when at least one of `_min_gap > 0`, `_burst_max > 0` or
`_per_symbol > 0` holds; the window alone does not enable anything. When `enabled` is false, `admit()` takes the lock
only to add 1 to `_counts["admitted"]` and returns `ThrottleResult(True, "ok", "")`; it reads no clock and records no
time, symbol or entry. The `enabled` test itself (L69) reads the three settings without the lock; they never change
after construction (P06-S004).

### 2.4 The `admit(symbol)` algorithm

P06-S008. FACT (L65 to L115): when enabled, the whole of the decision runs inside one `with self._lock:` block
(L74 to L115). It reads `now = self._clock()` once (L75) and then tests three gates in this fixed order, returning at
the first that blocks:
1. Global minimum gap (L77 to L83): only if `_min_gap > 0` and `_last_entry is not None`: `gap = now - _last_entry`;
   if `gap < _min_gap`, it adds 1 to `_counts["min_gap"]` and returns
   `ThrottleResult(False, f"min_gap {gap:.1f}s < {self._min_gap:.0f}s", "min_gap")`.
2. Global burst (L85 to L95): only if `_burst_max > 0`: `cutoff = now - _burst_window`; it removes from the left of
   `_recent` every time `< cutoff` (L88 to L89); if `len(_recent) >= _burst_max`, it adds 1 to `_counts["burst"]` and
   returns `allowed=False` with reason `"burst <n> >= <max>/<window>s"` and category `"burst"`.
3. Per-symbol cooldown (L97 to L107): only if `_per_symbol > 0` and `symbol` is truthy: if
   `_per_symbol_last.get(symbol)` is not `None` and `now - last < _per_symbol`, it adds 1 to `_counts["per_symbol"]`
   and returns `allowed=False` with reason `"per_symbol <symbol> <elapsed>s < <cooldown>s"` and category
   `"per_symbol"`.
If no gate blocks (L109 to L115), it records the entry: `_last_entry = now`, `_recent.append(now)`, and, if `symbol` is
truthy, `_per_symbol_last[symbol] = now`; it adds 1 to `_counts["admitted"]` and returns
`ThrottleResult(True, "ok", "")`.

P06-S009. FACT (L78 to L113): a blocked call records nothing (no time, no symbol); only an admitted call changes
`_last_entry`, `_recent` and `_per_symbol_last`. Exactly one counter is increased per call: the blocking gate's, or
`admitted`. INTERPRETATION: a burst of rejected attempts does not extend any gap, window or cooldown; the next attempt
is measured from the last admitted entry only. The precedence matches the docstring's "evaluated global-first (global
takes precedence)" (L4 to L5, HISTORICAL) and the test `test_global_takes_precedence_over_per_symbol`
(`tests/unit/test_entry_throttle.py` L102 to L108, HISTORICAL).

P06-S010. FACT (L109 to L113; `signals/signal_processor.py` L1410, L2225, L2530): the time recorded is the time of the
`admit()` call. The module calls this "the placement" (L66 to L67, L109 comment "admit — record the placement",
HISTORICAL), but the module itself has no knowledge of whether an order is later placed; what follows an admit at the
call sites is in section 4.6.

### 2.5 Units, windows and boundary conditions

P06-S011. FACT and INTERPRETATION (L77 to L113; P06-S006): units are seconds of the monotonic clock for the gap, the
window and the cooldown, and a count of admitted entries for the burst limit. The boundaries, by the comparison
operators:
- the gap test is strict (`gap < _min_gap`): an attempt exactly `_min_gap` seconds after the last admitted entry
  passes;
- the window is closed at its old end: entries are removed only when strictly older than `now - _burst_window`
  (`< cutoff`), so an entry exactly `_burst_window` seconds old still counts; the limit test is `>=`, so the
  `_burst_max`-th entry in the window is the last admitted;
- the cooldown test is strict (`elapsed < _per_symbol`);
- the very first admitted entry of the process meets no gap test (`_last_entry is None`) and no cooldown entry;
- `symbol` of `None` or `""` skips the per-symbol gate and is not recorded; the two global gates still apply;
- the per-symbol key is the exact symbol text (a dict key): no case folding, stripping, prefix or suffix handling is
  done here. At the fused-path call site the text is the receiver's post-alias symbol, kept in its received case on an
  alias miss (P04-S045, P04-S046); at the other two sites it comes from the `WatchEntry` and the parked candidate
  (section 4).

P06-S012. FACT (L57, L86 to L89, L109 to L113): `_recent` is pruned only inside the burst gate, that is only when
`_burst_max > 0`, but an admitted entry is appended to it whenever the throttle is enabled. `_per_symbol_last` is never
pruned, and is written on every admit with a truthy symbol, whether or not the cooldown is on. INTERPRETATION: with
the burst gate on, `_recent` holds at most `_burst_max` times after any admit (an admit happens only when fewer remain
after pruning); with the burst gate off and another gate on, `_recent` grows by one per admitted entry for the life of
the process (the deque has no `maxlen`; Python documentation, `collections`, read 17-Nov-2026: "If maxlen is not
specified or is None, deques may grow to an arbitrary length"); `_per_symbol_last` grows by one key per distinct
symbol text admitted. At the repository's file values the burst gate is on (P06-S021).

P06-S013. INTERPRETATION (L83, L94 to L95, L106 to L107): the reason text formats the configured gap, window and
cooldown with no decimals (`:.0f`), the measured gap of the `min_gap` gate with one decimal (`:.1f`, L83) and the
measured elapsed time of the `per_symbol` gate with no decimals (`:.0f`, L106); a fractional setting is shown rounded
in the reason, while the comparison uses the unrounded value. [corrected in the check: the per-symbol elapsed format
added]

### 2.6 How the gates combine at the file values

P06-S014. INTERPRETATION (arithmetic on P06-S008 and P06-S011, at the repository file values gap 20 s, window 60 s,
burst 3, cooldown 300 s, `config/system_config.yaml` L350 to L353): because only admitted entries are recorded and the
gap gate is tested first, any two admitted entries are at least 20 s apart. Four admitted entries therefore span at
least 60 s. The burst gate can block the fourth only if the first is still counted, which needs it to be at most 60 s
old: together these leave only the exact case in which the four times are exactly 20.0 s apart (the fourth attempt
exactly 60.0 s after the first). In every other case the gap gate either blocks first or the oldest entry has left the
window. At these values the burst gate is therefore, by the arithmetic, almost never the gate that blocks. HISTORICAL
(`docs/decisions/10_entry_throttle_admission.md` L12): a legacy document reports "Of 139 throttles, 132 are that one
gate (7 per-symbol, 0 burst)"; that is a report, not proof of what ran.

P06-S015. INTERPRETATION (same values): the cooldown can block only an attempt that the gap gate lets through, that is
one at least 20 s after the last admitted entry of any symbol and less than 300 s after the last admitted entry of the
same symbol text. The cooldown runs from one admitted entry to the next attempt for that symbol; the class has no
input from fills, exits or position state (P06-S003). HISTORICAL (`docs/audit/rulings_1_2_verification_07aug2026.md`
L438 to L475): a legacy verification of 07-Aug-2026 reached the same reading ("it measures PREVIOUS ENTRY → NEW
ENTRY. There is no exit hook anywhere in the class").

P06-S016. HISTORICAL (`tests/unit/test_entry_throttle.py` L134 to L148): the test of the 19-Jun burst replays five
attempts one second apart with gap 20, window 60, burst 3 and cooldown 300 and expects one admit; its last step, an
attempt 1 s after the third admitted entry, is commented "4th in 60s -> burst" and asserts only `not allowed`.
INTERPRETATION (P06-S008): by the code, that attempt is blocked by the gap gate (category `min_gap`), not by the
burst gate; the assertion does not check the category.

### 2.7 `metrics()`

P06-S017. FACT (L117 to L125): `metrics()` takes the lock and returns a new dict of four integers:
`entries_throttled_min_gap`, `entries_throttled_burst`, `entries_throttled_per_symbol` and `entries_admitted`, copied
from `_counts`. The counts start at 0 at construction and are never reset (P06-S003): they are cumulative for the life
of the instance. FACT (`signals/signal_processor.py` L706 to L710; `main.py` L4076): `get_runtime_metrics()` merges
them into its result inside `try: ... except Exception: pass`, and `main.py` passes `get_runtime_metrics` to the health
server as `metrics_provider` (the `/metrics` composition is recorded in P03-S046 and P04-S065; the endpoint is A15's).
The four keys do not collide with the processor's own keys (`signals_processed`, `entries_placed`,
`entries_throttled`, `entries_rejected`, L274 to L279).

### 2.8 Failure behaviour inside the module

P06-S018. FACT (L40 to L125): the module has no `try`, no logging and no error return. Current external context
(Python documentation, `threading`, read 17-Nov-2026: a lock used in a `with` statement is equivalent to
`acquire()` then `try: ... finally: release()`). INTERPRETATION: (a) at construction, a value that `float()` or
`int()` cannot convert raises out of `EntryThrottle(...)` and so out of the `SignalProcessor` constructor; the schema
types the four keys before they reach it (section 3; A02); (b) inside `admit()` and `metrics()` an exception, if one
occurred, would propagate to the caller with the lock released; the code in the block is arithmetic, deque and dict
operations on a string key and the clock call, so no ordinary input raises there; (c) the lock is a plain `Lock`;
`admit()` and `metrics()` do not call each other or any other locked code, so the same thread never re-acquires it.
How an escaped exception is handled at the call sites is P06-S034.

### 2.9 Records and history

P06-S019. HISTORICAL (commit `575a1dc`, 19-Jun-2026, "FIX-190 (Bug G): entry throttle — prevent burst placement"):
"The 19-Jun incident placed 5 entries in ~5s from a Chartink spike, contributing to the cap race + cascade blast
radius." It added an inline `_throttle_admit()` "(thread-safe, called right before placement so only PLACED entries
count)" that "rejects a too-soon/burst entry and releases its reservation so the slot frees for a later signal", with
schema defaults OFF and "system_config sets 20s / 3-per-60s". HISTORICAL (commit `c0554c6`, the same day): it replaced
the inline function with `EntryThrottle`, "ATOMIC admit(symbol) (check-AND-record under one lock — deliberately not a
split check/record, which would have a TOCTOU burst race)", added the 300 s per-symbol cooldown ("no re-entry of the
SAME symbol within 5 min (stops rapid same-symbol churn)") and the per-reason metrics, and stated "both place sites
call admit(symbol)" and "Activates next restart". Whether and when it was deployed is UNKNOWN / NOT ESTABLISHED.

P06-S020. HISTORICAL (module docstring L1 to L20): the stated purpose is to prevent "entry bursts (the 19-Jun
10:00:24-28 incident: 5 entries in ~5s)"; gate 1 is "minimum seconds between any two PLACED entries", gate 2 "at most
`burst_max` placed entries per rolling `burst_window`", gate 3 "no re-entry of the SAME symbol within
`per_symbol_cooldown` seconds (stops rapid same-symbol churn, e.g. enter X 10:00 → exit 10:02 → re-fire 10:03 →
wait)". HISTORICAL (`docs/CONFIG_GUIDE.md` L341 to L349): the guide gives the same values and says "Throttled signals
are **dropped**, not queued." HISTORICAL (`tests/unit/test_entry_throttle.py` L1 to L167): 13 tests with a fake
clock cover each gate, the window reset, the cooldown (same symbol, other symbol, expiry), precedence, the disabled
case, the counters and a 50-thread race expecting exactly `burst_max` admits; none was run in this study.

## 3. Configuration: keys, schema, wiring and defaults (A02 owns the files and the schema)

P06-S021. FACT (`config/system_config.yaml` L344 to L353; `git blame` and `git log -L` of L349 to L353): the
`signal_processor` section holds, under the comment "FIX-190 (Bug G): entry throttle — prevents the 19-Jun
5-entries-in-5s burst." (L349), `min_gap_between_entries_sec: 20` (L350, ">=20s between any two PLACED entries
(global)"), `entry_burst_window_sec: 60` (L351, "rolling burst window (global)"), `entry_burst_max: 3` (L352, "max 3
placed entries per 60s (0 = off)") and `per_symbol_cooldown_sec: 300` (L353, "no re-entry of same symbol within 5
min"). The 20, 60 and 3 come from commit `575a1dc` and the 300 from `c0554c6` (both 19-Jun-2026); the lines have not
changed since except for comment text in `c0554c6`. The effective files on the legacy machines are UNKNOWN / NOT
ESTABLISHED (A02).

P06-S022. FACT (`core/config_loader.py` L564 to L614): `SignalProcessorConfig` (`extra="forbid"`) declares
`min_gap_between_entries_sec: float = 0.0` (L581), `entry_burst_window_sec: float = 60.0` (L582),
`entry_burst_max: int = 0` (L583) and `per_symbol_cooldown_sec: float = 0.0` (L586), with the comment "All default
OFF so existing configs/tests are unaffected; system_config enables them." (L577 to L578, HISTORICAL). The class's
four validators cover `worker_count`, `drain_poll_sec`, `pipeline_timeout_sec` and `tgt_min_pct` (L588 to L614);
none covers a throttle key, so any value of the declared type, negative values included, reaches `EntryThrottle`
(A02 key consumer map part 1, L279; A02 RECONCILED TOPIC RECORD L84 records that the loader enforces types in lax
mode). The floors that then apply are in P06-S005.

P06-S023. FACT (`main.py` L3574, L3595 to L3599): `main.py` passes the four values as
`getattr(sp_cfg, "min_gap_between_entries_sec", 0.0)`, `getattr(sp_cfg, "entry_burst_window_sec", 60.0)`,
`getattr(sp_cfg, "entry_burst_max", 0)` and `getattr(sp_cfg, "per_symbol_cooldown_sec", 0.0)`, where
`sp_cfg = app_config.system.signal_processor`. INTERPRETATION (P06-S022): `sp_cfg` is a `SignalProcessorConfig`, whose
four fields always exist (with their defaults when the keys are absent), so the `getattr` defaults are never used; A02
recorded the same ("the `getattr` defaults at `main.py` L3596 to L3599 never apply", A02 AUDIT K-51 row, L2318).

P06-S024. FACT (`core/config_loader.py` L581 to L586; `main.py` L3596 to L3599; `signals/signal_processor.py` L179 to
L182; `signals/entry_throttle.py` L43 to L46): the code defaults are the same at all four layers: gap 0.0, window
60.0, burst 0 and cooldown 0.0. INTERPRETATION (P06-S007): if the four keys were removed from the file, the schema
defaults would apply and the throttle would be disabled, admitting every entry; at the file values all three gates are
on. A02 counted the three gate keys among the 13 loader defaults that differ from the file values (A02 key consumer
map part 1, L326).

P06-S025. FACT (search for the four key names, non-test code): in the trading process the keys are read only by the
schema and passed only at `main.py` L3596 to L3599; the throttle has no other source of settings and no reload. FACT,
interface only (`ops_dashboard/backend/services/capacity.py` L197 to L208, A15's file): the operations dashboard reads
the same four keys from configuration for display, and its "Entry Burst" row counts ENTRY orders in the database over
the window ("DB-derived"), not the throttle's in-memory admits. Its logic is A15's.

## 4. Construction in the processor and the three call sites (Rama's decision B)

### 4.1 Construction and scope of one instance

P06-S026. FACT (`signals/signal_processor.py` L179 to L182, L259 to L268): the constructor takes
`min_gap_between_entries_sec`, `entry_burst_window_sec`, `entry_burst_max` and `per_symbol_cooldown_sec` and, after
the FIX-018 counter and before the runtime metrics, imports `EntryThrottle` locally (L262) and builds
`self._entry_throttle = EntryThrottle(min_gap_sec=..., burst_window_sec=..., burst_max=...,
per_symbol_cooldown_sec=...)` (L263 to L268), passing the four values unchanged. HISTORICAL (L259 to L261): "entry
throttle — global min-gap + burst + per-symbol cooldown, atomic check-and-record (prevents the 19-Jun burst AND rapid
same-symbol re-entry)". FACT (`main.py` L3575; P04-S001): `main.py` builds one `SignalProcessor`. FACT (A01 RECONCILED
TOPIC RECORD L60): the process holds an instance lock (a file lock plus a loopback bind). INTERPRETATION: there is one
throttle per trading process, shared by every caller in it (section 5); nothing shares its state with another process.
Whether more than one trading process ran at once (for example one per account) is outside A06 (A01, A17); at runtime
it is UNKNOWN / NOT ESTABLISHED.

### 4.2 Call site 1: `_admit_and_place` (L1407 to L1418)

P06-S027. FACT (L1277 to L1418; owners of each step named for the interface only): in `_admit_and_place` the call
`_tr = self._entry_throttle.admit(symbol)` (L1410) comes after, in execution order: the FIX-018 in-flight increment
(L1302 to L1305); inside `self._fm.portfolio_lock` the per-strategy cap, the one-trade-per-symbol-direction check, risk
approval and the capital reservation, and the status `RESERVED` (L1307 to L1344; A09); the early return when there is
no order placer, which releases the reservation as `"no_order_placer"` and writes `PROCESSED_NO_PLACER` without
consulting the throttle (L1351 to L1363); the target derivation (L1368); the `INTRADAY SIGNAL` alert
(`_emit_signal_alert`, L1371 to L1380; A14); the late kill-switch check (L1389 to L1396) and the shutdown check (L1398
to L1405), each of which releases the reservation and raises before the throttle. After a successful admit, the next
statements are the effect-telemetry count, the `P1_ACCEPT` evidence capture and `self._placer.place(...)` (L1420 to
L1460; A10).

P06-S028. FACT (L1411 to L1418): when `_tr.allowed` is false, the site releases the reservation, if one is held, with
`self._fm.release(ac.reservation_id, "entry_throttled")` and clears `ac.reservation_id`; calls
`self._bump_metric("entries_throttled")`; and raises `_PipelineReject("ENTRY_THROTTLED", f"Entry throttled:
{_tr.reason}")`. HISTORICAL (L1407 to L1409): "space out placed entries to prevent a burst (the 5-entries-in-5s 19-Jun
spike). Released reservation on reject so the slot frees for a later signal." INTERPRETATION: the release call at
L1413 is not inside a `try`; if it raised, the exception would leave `_admit_and_place` in place of the reject, with
`ac.reservation_id` still set and `entries_throttled` not counted, and would be handled as in P06-S034. The release
itself is A09's.

P06-S029. FACT (L1179 to L1276, L1646 to L1704; `main.py` L3633 to L3660; `config/system_config.yaml` L564 to L566):
`_admit_and_place` has two callers. (1) `_process_one`'s fused path (L1179 to L1191), used when the allocator is off,
in shadow mode, in enforce mode for an out-of-scope strategy, or when the allocator routing raises an exception other
than `_PipelineReject`, which is logged and ignored (L1147 to L1173). Its handler for the throttle reject
(L1193 to L1231): logs INFO "rejected at ENTRY_THROTTLED", skips `entries_rejected` (L1199: "throttle drops are
already counted under entries_throttled"), writes `update_signal_status(signal_id, "REJECTED_ENTRY_THROTTLED",
rej.reason)` (L1201; the status write is P05's, the storage A03's), calls `_evidence_capture("P2_REJECT", ...)` with
`rejected_step` `ENTRY_THROTTLED` (L1202 to L1211; a no-op when no evidence recorder is wired, L595 to L597; the same
applies to the `P2_REJECT` calls of the other handlers below), finds no reservation left to release, and adds 1 to
`_stats["rejected"]["ENTRY_THROTTLED"]` (L1218 to L1220); its `finally` decrements the FIX-018 counter and releases the
receiver's in-flight claim for the symbol (L1248 to L1271; P04-S057). (2) `admit_prepared` (L1646 to L1704), the
allocator's enforce-mode entry, wired by `main.py` as `enforce_admit_fn` (L3644) only when `allocator_mode` is not
`"off"` (L3633); its handler (L1661 to L1680) writes the same status and evidence and counts the reject, without the
INFO line and without the metric skip (the handler bumps no runtime metric; the site's own `entries_throttled` bump,
L1415, applies on both paths), and its `finally` releases the claim unless
re-queued (L1692 to L1703). The file sets `allocator_mode: "shadow"` and `enforce_scope: "v3_only"` (L565 to L566);
HISTORICAL (L566 comment): "none exist yet → enforce governs nothing even if flipped". The allocator is A18's.
[corrected in the check: the allocator-error fall-through (L1171 to L1172) added to the fused-path conditions; the
evidence call described as a call that does nothing without a recorder]

### 4.3 Call site 2: `continue_from_gate` (L2224 to L2233)

P06-S030. FACT (L2010 to L2369; `main.py` L865 to L887): `continue_from_gate(entry, release_ltp)` takes
`symbol = entry.symbol` from the `WatchEntry` (L2028). The admit at L2225 comes after the status `PROCESSING`, the
last-mile kill-switch, window and shadow-inning checks, the strategy lookup and controls, sizing, the FIX-018
increment, the reservation inside `portfolio_lock` with status `RESERVED` (L2133 to L2171), the no-placer return
(L2174 to L2189), the `INTRADAY SIGNAL` alert with score `None` (L2191 to L2201) and the FIX-165e kill-switch and
shutdown checks (L2203 to L2222). On a block the site releases the reservation as `"entry_throttled"`, bumps
`entries_throttled` and raises `ENTRY_THROTTLED` (L2226 to L2233); the handler (L2309 to L2338) logs, skips
`entries_rejected`, writes `REJECTED_ENTRY_THROTTLED` with the reason, emits `P2_REJECT` and counts the reject; its
`finally` (L2357 to L2369) decrements the FIX-018 counter and does not call the receiver's release (docstring L2018 to
L2019: "in_flight tracking is NOT released here -- the EntryGate already manages it", HISTORICAL). The caller is
`main.py`'s `_gate_release_worker`, run on a two-thread pool `gate-release` (L865 to L867) when the gate reports
`PRICE_HIT` (L879 to L887). HISTORICAL (L2236 to L2238): "This path is DORMANT today: nothing calls EntryGate.add(), so
only gate_state rows rehydrated at boot can reach it." Whether it ran in production is UNKNOWN / NOT ESTABLISHED; the
entry gate is A07's.

### 4.4 Call site 3: `continue_from_retest` (L2530 to L2536)

P06-S031. FACT (L2375 to L2640; `main.py` L3423, L3765 to L3797; `config/system_config.yaml` L529):
`continue_from_retest(parked)` takes `symbol = parked.symbol` (L2386). The admit at L2530 follows the same pattern:
status `PROCESSING`, last-mile checks, strategy lookup and controls, the structure stop and its check, sizing and
the target (L2393 to L2467), FIX-018 increment, reservation with status `RESERVED`
(L2469 to L2501) [line corrected in the check: the increment block starts at L2469], no-placer return (L2503 to L2512), the alert (L2514 to L2517), the late kill-switch and shutdown
checks (L2519 to L2528). On a block it releases the reservation as `"entry_throttled"`, bumps `entries_throttled` and
raises `ENTRY_THROTTLED` (L2531 to L2536); the handler (L2594 to L2614) writes `REJECTED_ENTRY_THROTTLED`, emits
`P2_REJECT` and counts it; the `finally` (L2630 to L2640) does not call the receiver's release. Its caller is the
`RetestMonitor`'s `on_confirm` (`main.py` L3784 to L3788), built and started only when `wait_for_retest_enabled` is true
and the zone warmer and cache exist (L3769); the file sets `wait_for_retest_enabled: false` (L529). HISTORICAL
(docstring L2381 to L2382: "Called from RetestMonitor's poll thread on CONFIRMED"; L2539 to L2540: "DORMANT today
(wait_for_retest_enabled: false)"). INTERPRETATION: at the file value this site cannot be reached, because the monitor
is not built. The retest logic is A08's and A18's.

P06-S054. (added in the check) HISTORICAL (`tests/unit/test_sr_v2_continue.py` L116 to L117, L217 to L223; never
run): a test of the retest path replaces the throttle with a stub whose `admit` returns `allowed=False` and expects,
for `continue_from_retest`, one reservation, one release, no `place()` call and a `REJECTED_ENTRY_THROTTLED` status
("throttle rejects AFTER reserve"). This agrees with the code order recorded in P06-S031 and P06-S035; it is not
proof of what ran.

### 4.5 Completeness and what the caller learns

P06-S032. FACT (search for `[A-Za-z_]+\.place\(` in non-test, non-document code; the other hits are text, not calls:
`orders/order_placer.py` L558 (docstring), `capital/risk_engine.py` L624, `signals/signal_processor.py` L34 and L116
(comments) and `config/expected_managers.yaml` L61 (a YAML string)): the only placement calls are
`signals/signal_processor.py` L1446, L2251 and L2553, and each is preceded in its function by exactly one
`admit(symbol)` (L1410, L2225, L2530). Between the admit and the call there is, on the fused path, the effect-telemetry
count (`self._fx_dispatch.inc()`, L1423) and the `P1_ACCEPT` evidence capture (L1427 to L1445); on the gate and retest
paths only the `P1_ACCEPT` evidence capture (L2241 to L2250, L2543 to L2552), because the effect-telemetry handle
"counts the _process_one dispatch only" (L213 to L216, HISTORICAL comment). INTERPRETATION: every entry the processor
sends to the order placer has passed the throttle immediately before, and the throttle is the last gate before
placement on all three paths. [corrected in the check: the effect-telemetry count is on the fused path only; the
non-call search hits named]
HISTORICAL (`docs/audit/rulings_1_2_verification_07aug2026.md` L472 to L475): a legacy verification states the same
at an earlier commit.

P06-S033. FACT (search for `_tr\.|\.category|ThrottleResult` in `signals/signal_processor.py` and `main.py`): the call
sites use only `allowed` and `reason`; `category` is never read. The structured status is the single value
`REJECTED_ENTRY_THROTTLED` for all three gates; which gate blocked is visible only as the first word of the stored
reason text (`"Entry throttled: min_gap ..."`, `"... burst ..."`, `"... per_symbol ..."`) and in the per-gate counters
of `metrics()`. HISTORICAL (`docs/decisions/10_entry_throttle_admission.md` L23): a legacy decision file of
19-Jul-2026 makes the same observation ("recorded only in the free-text `rejection_reason`").

P06-S053. (added in the check) FACT, interface only (`reports/daily_trade_review.py` L734 to L744, A15's file;
search of non-test, non-document code for `ENTRY_THROTTLED`): besides the processor, the only code that names the
throttle's status text is the daily trade review (code that reads every `REJECTED_*` status without naming this one
is not covered by the search), which places any signal whose status contains `ENTRY_THROTTLED` in its
`"CAPITAL_CHECK"` stage, together with the sizing, position-count, daily-trade, loss and strategy-cap rejects; it
cannot tell the three gates apart (P06-S033). HISTORICAL (`core/evidence_contract.py` L146 to L150, comment): the
evidence contract notes that a reject "past sizing (the admission caps, the risk rungs, ENTRY_THROTTLED)" had "a
fully sized order" that the `P2_REJECT` record does not capture. The report's logic is A15's.

### 4.6 What an admit means

P06-S034. FACT (L1410 to L1538, L1193 to L1246; L2225 to L2288, L2340 to L2355; L2530 to L2581, L2616 to L2628): the
throttle records the entry when `admit()` returns allowed, before `place()` is called. What then happens is decided at
the call site, and the throttle is never told: `place()` returns (status `PROCESSED`, `entries_placed`); it raises
`BrokerTimeoutError` (status `TIMEOUT`, reservation kept for recovery); in `_admit_and_place` (both of its callers) it
raises `BrokerRateLimitError` (re-queue, at most three times, or `PLACEMENT_FAILED`; P04-S052), while on the gate and
retest paths that exception, a `BrokerError` subclass (`core/exceptions.py` L158, L243), is re-raised and gives
`PLACEMENT_FAILED` (L2283 to L2286, L2578 to L2581); or it raises another exception (`PLACEMENT_FAILED`). An exception
from `admit()` itself, or from the site's own release call (P06-S028), would reach the generic handler of the calling
function (L1233 to L1246, L1681 to L1691, L2340 to L2355, L2616 to L2628), which writes `PLACEMENT_FAILED` and
releases the reservation as `"placement_failed"`. INTERPRETATION: (a) the gap, window and cooldown run from the admit
in every one of these outcomes, including those in which no order reached the broker; what the configuration and the
docstring call "PLACED entries" (P06-S020, P06-S021) is, in the code, "entries admitted immediately before a placement
attempt"; whether `place()` can decline an entry without raising is A10's; (b) `entries_admitted` therefore counts
admits, not placements, and can exceed `entries_placed`; (c) an exception at the throttle step leads to no placement
(fail-closed).

P06-S035. FACT (L1302 to L1344, L1371 to L1380, L1410; L2133 to L2201, L2225; L2470 to L2517, L2530): at all three
sites the reservation, the `RESERVED` status and the `INTRADAY SIGNAL` alert come before the admit. INTERPRETATION: a
throttled signal has held a reservation and counted in the FIX-018 in-flight figure while risk approval ran (A09), has
been announced by an `INTRADAY SIGNAL` alert when a notifier is wired (A14), and ends as `RESERVED` then
`REJECTED_ENTRY_THROTTLED`; between its reservation and its admit, other signals see that reservation in the capital
and position checks (their effect is A09's). A03 recorded the release after a reservation for this status from the
storage side (A03 AUDIT, L2859).

### 4.7 The FIX-069 retry and the throttle

P06-S036. FACT (L1486 to L1532; P04-S052) and A04's record (Audit Findings Register RL-16: the limiter raises
`BrokerRateLimitError` after waiting up to 30 s): in `_admit_and_place`, a `BrokerRateLimitError` from `place()` makes
the worker put the signal straight back on the queue (with `retry_count` + 1, up to three retries); the retry runs the
whole intake and A07 path again (P04-S052), including the age check against the original `triggered_at` (L914 to
L921; P04-S037), and only if it passes every step again does it reach `admit(symbol)` a second time, with the same
symbol text. Its first attempt was admitted and recorded (P06-S034). INTERPRETATION (P06-S008, P06-S011, at the file
values): the retry is admitted only if at least 20 s have passed since the last admitted entry of any symbol and at
least 300 s since the first attempt's own admit; a retry that reaches the throttle sooner is blocked (by `min_gap` if
under 20 s have passed since the last admitted entry of any symbol, otherwise by `per_symbol`, or, in the exact
equality case of P06-S014, by `burst`), ends `REJECTED_ENTRY_THROTTLED` with its reservation released, and is not
retried again. The time limits that also apply to the retry before the throttle are in P06-S052. [corrected in the
check: the retry reaches the throttle only if it passes the intake and A07 steps again; the burst exact case added] HISTORICAL (`docs/design/a2_timeout_retry_design_02jul2026.md` L43 to
L48; `docs/audit/system_security_audit_02jul2026.md` L50): legacy documents of 02-Jul-2026 describe the same effect
for the then-combined timeout and rate-limit retry ("The near-immediate retry is rejected as `ENTRY_THROTTLED`. **This
is a rate-limiter, not an idempotency guard.**"). FACT (L1464 to L1484; HISTORICAL test
`tests/unit/test_signal_processor.py` L2347 to L2362): at the baseline the timeout branch no longer re-queues, so the
effect concerns the rate-limit retry only; the test at L2335 to L2344 still expects the rate-limit path to re-queue
("retry preserved"). Whether a `BrokerRateLimitError` ever occurred in production, and how long a retry took to reach
the throttle, are UNKNOWN / NOT ESTABLISHED.

P06-S052. (added in the check) FACT (`signals/signal_processor.py` L914 to L921, L1486 to L1525; search of the file
for `_signal_expiry_sec|deadline|pipeline_timeout|age_sec`; `config/system_config.yaml` L127; P04-S036, P04-S052;
Audit Findings Register K-13): the only time limit in the processor between a FIX-069 retry's intake and its admit is
the age check, which compares `now_ist()` with the retry's original `triggered_at` against `signal_expiry_sec`
(repository value 600 s, read from `signal_queue.expiry_sec`); the re-put has no delay, and
`signal_processor.pipeline_timeout_sec` has no consumer (A02 K-13). INTERPRETATION (P06-S036, at the file values):
a retry is admitted by the throttle only if its admit comes at least 300 s after its own first admit, while its age
check at intake, measured from the original trigger time, must still be at most 600 s; that requires the retry to
wait in the queue or in its steps for most of the cooldown. A retry that comes back quickly, as the immediate re-put
allows, is refused at the throttle (P06-S036), and a retry taken from the queue more than 600 s after the trigger is
rejected `EXPIRED` before it reaches the throttle. Whether either happened in production is UNKNOWN / NOT
ESTABLISHED. The age check uses the IST wall clock and the throttle the monotonic clock (P06-S006); the two are
compared here only as elapsed seconds.

## 5. Concurrency: callers of `admit()` at the same time (direction question 14, throttle side)

P06-S037. FACT (sections 4.2 to 4.4; `main.py` L865 to L887, L3784 to L3797, L3633 to L3660;
`allocation/portfolio_allocator.py` L105 to L109 and L318, A18's file, interface only): the one throttle instance is
reached from these threads: (1) the processor's worker threads (five at the file value, P04-S003) through
`_process_one` and `_admit_and_place`; (2) the two `gate-release` pool threads through `continue_from_gate`; (3) the
`RetestMonitor`'s thread through `continue_from_retest`, only when the monitor is built (P06-S031: not at the file
value); (4) the allocator's own thread, which calls `admit_prepared` and so `_admit_and_place`, only in enforce mode
(not at the file value, P06-S029). `metrics()` is called from the health server's request handling through
`get_runtime_metrics` (A15). All of them use the same `_lock`.

P06-S038. Current external context (Python documentation, `threading`, Lock objects, read 17-Nov-2026: "When the
state is locked, `acquire()` blocks until a call to `release()` in another thread changes it to unlocked"; "When more
than one thread is blocked in `acquire()` waiting for the state to turn to unlocked, only one thread proceeds when a
`release()` call resets the state to unlocked; which one of the waiting threads proceeds is not defined, and may vary
across implementations."). INTERPRETATION (P06-S008): (a) the read of state, the three tests and the record of an
admit happen under one lock, so two callers cannot both pass the gates against the same state: of several
near-simultaneous attempts, the first to take the lock is admitted and the rest are tested against its record (at the
file values they are blocked by the 20 s gap). This is the design the docstring states (L13 to L17, HISTORICAL) and
the 50-thread test expects (`tests/unit/test_entry_throttle.py` L151 to L167, HISTORICAL). (b) The clock is read
inside the lock, so the recorded times are in lock order and, by the monotonic clock (P06-S006), never decrease.
(c) The caller that acquires the lock first is admitted. Which caller that is depends on when each reaches the lock,
and so on how long each one's earlier steps took (screening, quotes, sizing, the wait for `portfolio_lock`), not on
receipt order at the receiver, on `triggered_at` or on score; among callers already blocked on the lock, which one
proceeds "is not defined, and may vary across implementations" (the documentation quoted above). [corrected in the
check: the earlier text asserted an order "in practice" that the documentation does not give] HISTORICAL
(`docs/decisions/10_entry_throttle_admission.md` L7, L14): the legacy decision file calls the outcome
"first-come-first-served, evaluated after risk approval".

P06-S039. FACT (L1307 to L1344 then L1410; L2138 to L2171 then L2225; L2474 to L2501 then L2530; module L74 to L115;
`allocation/portfolio_allocator.py` L290 to L318, A18's file, interface only): on the fused, gate and retest paths
`admit()` is called after the function's own `portfolio_lock` block has ended, with no other lock held; on the
allocator's enforce path the allocator holds `portfolio_lock` (an `RLock`, per its docstring L290 to L292) for the whole
ranked batch and calls `admit_prepared` inside it (L302 to L318), so there `admit()` runs with `portfolio_lock` held.
`admit()` itself takes no other lock while holding the throttle's lock. INTERPRETATION: the only lock order involving
the throttle is `portfolio_lock` then the throttle's lock (enforce mode only, not at the file value, P06-S029); no code
takes them in the other order, so the throttle cannot take part in a deadlock; the work under its lock has no I/O and,
with the burst gate on, removes at most a few entries, so a waiting caller waits briefly; there is no timeout on the
wait (Python documentation, `threading`: the default `acquire()` blocks until the lock is unlocked).

P06-S040. INTERPRETATION (P06-S028 to P06-S036; P04-S057; P03): the throttle neither queues nor reorders: a blocked
signal ends `REJECTED_ENTRY_THROTTLED` and is not retried by the processor (HISTORICAL, `docs/CONFIG_GUIDE.md` L349:
"Throttled signals are **dropped**, not queued"); on the fused path the receiver's in-flight claim is then released,
so a later webhook for the symbol can be accepted again, subject to the receiver's dedup (P03). The per-symbol
cooldown blocks a second admit for the same symbol text within 300 s (at the file value), whichever signal or path it
comes from, including a FIX-069 retry of the same signal (P06-S036). Two texts for one instrument (an alias miss, a
different case, a suffix) are separate keys (P06-S011). Per-signal duplicate protection is not the throttle's design:
it has no signal identifier.

P06-S041. INTERPRETATION (P06-S014, P06-S038): in an opening burst of approved signals at the file values, the
throttle admits one entry per 20 s of the monotonic clock; each blocked signal has already been reserved (P06-S035).
Within 20 s after an admit, every attempt, from any of the five workers or any path, is blocked by the gap gate,
because it is tested first (P06-S008); the burst gate and the cooldown therefore play no part inside one 20 s gap; the
gap gate decides. [corrected in the check: the basis is the gate order; the receiver's per-symbol claim (P03,
P04-S058) is not needed for this reading and can itself be broken, P04-S058]
Whether such bursts occurred, and how often, is UNKNOWN / NOT ESTABLISHED (legacy documents report counts, HISTORICAL:
`docs/decisions/10_entry_throttle_admission.md` L12 to L13, L23).

## 6. Limits reached, missing state, contention, restart and exceptions (direction question 12, throttle side)

P06-S042. INTERPRETATION (summary of P06-S028 to P06-S035): when a limit is reached the entry is refused at once,
never delayed: the reservation is released as `"entry_throttled"`, `entries_throttled` and the gate's own counter are
increased, the status becomes `REJECTED_ENTRY_THROTTLED` with the gate in the reason text, a `P2_REJECT` evidence
record is passed to the recorder when one is wired (P06-S029), and the signal is finished; the `INTRADAY SIGNAL` alert
call has already been made, which sends an alert only when a notifier is wired (L499 to L500; P06-S035). [corrected in
the check: the evidence record and the alert made conditional on their wiring, as the code is]

P06-S043. FACT (L40 to L59; P06-S003): the throttle has no stored state to be missing or corrupt: it starts empty in
the constructor and is never loaded. The only "missing" case is missing settings: absent keys give the schema
defaults and a disabled throttle that admits every entry (P06-S024); negative values give the same for the gap, burst
and cooldown, and a zero window becomes 60 s (P06-S005). INTERPRETATION: this is the throttle's only open (admit-all)
condition, and it is a configuration state, not an error path.

P06-S044. INTERPRETATION (P06-S003, P06-S006, P06-S017): on a process restart every recorded time and every counter
is lost: the first entry after the restart meets no gap, window or cooldown from entries made before it, and the
`/metrics` throttle counters start again from 0. There is no daily reset either; the state and counters last for the
life of the process. HISTORICAL (`ops_dashboard/docs/G2a_capacity_inventory.md` L84, A15's document): "in-memory
throttle state (not persisted)". How often, and when in the day, the process was restarted is A01's and A16's; at
runtime it is UNKNOWN / NOT ESTABLISHED.

P06-S045. INTERPRETATION (P06-S018, P06-S034, P06-S039): a contended lock makes the caller wait until it is free, with
no timeout and no error. An exception inside `admit()` (not expected for ordinary input) or from the site's release
call leads to `PLACEMENT_FAILED` and no placement: closed. The throttle has no fail-open path on error.

## 7. Inherited items and records touched by this part (A06 side only)

P06-S046. FACT (`OPEN_ISSUES_REGISTER_2026-11-05.md`, entry A04-31), quoted as recorded: "Which broker limits were the
bucket values meant to respect (per second only, or also per minute or per day for orders), and is there a record of
the broker's published limits they came from?" Owner: "Rama answers; Claude records. Topic: A04 (A06 for the entry
throttle)." Status: "History: OPEN QUESTION (Rama answered OPEN on 13-Nov-2026). Treatment: none recorded (a
history-only question: no new-system input was asked and Rama added none)." Next action: "None in the intent
discussion. RL-14 stays UNKNOWN / NOT ESTABLISHED and receives no treatment; the history stays OPEN and is carried
forward (Document 05, sections 11.2 and 11.3)." This part changes none of it.

P06-S047. FACT and INTERPRETATION, the A06 side of A04-31 (P06-S001, P06-S019 to P06-S022): (a) FACT: the throttle is
not one of the bucket values the question asks about: it uses no broker limiter and counts admitted entries (attempts to
place an entry), not broker requests; INTERPRETATION (P06-S026): it is per process [label split in the check]; (b) FACT (the module, its two commits `575a1dc` and
`c0554c6`, the schema comment L576 to L586 and the file comment L349 to L353): none of these names a broker limit or a
published broker figure; the purpose they state is the 19-Jun burst ("5 entries in ~5s from a Chartink spike,
contributing to the cap race + cascade blast radius", HISTORICAL) and same-symbol churn; (c) INTERPRETATION
(arithmetic at the file values, P06-S014): at most one admit per 20 s and three per 60 s per process, a ceiling on
placement attempts; how many broker requests each placement makes is A10's and A04's. Nothing found here answers the
history question; it stays OPEN with its owner A04.

P06-S048. FACT (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`, row K-12; `signals/entry_throttle.py` L50): K-12 (A02's
finding "Consumer-side floors and fallbacks replace values that the loader accepts", ISSUE, treatment AGREED on
09-Nov-2026, batch T5 group G3) includes `signal_processor.entry_burst_window_sec`. The A06 side is confirmed at the
baseline: a window of 0 becomes 60 s and a negative window becomes 0 s (P06-S005); at the file value 60 nothing
changes. ID, owner, classification and treatment are unchanged.

P06-S049. FACT (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`, row RL-14; `A04_AUDIT_2026-11-13.md` L3566 to L3571): A04's
RL-14 (UNKNOWN / NOT ESTABLISHED; owner "A04 (A06 for the entry throttle)") records that "the entry throttle (at least
20 s between placed entries, at most 3 in 60 s, a 300 s per-symbol cooldown at `config/system_config.yaml` L350 to
L353) limits entries, not broker requests". The A06 side agrees with the baseline code (P06-S008, P06-S021, P06-S047):
RL-14 is unchanged.

P06-S050. FACT (`AUDIT_FINDINGS_REGISTER_2026-11-06.md`, row RL-16; A04 RECONCILED TOPIC RECORD, A06 handoff row
L412): RL-16 (A04's limiter wait bound of 30 s) is handed to A06 among others. Its A06 side for the retry comment is
P04-S052; the throttle side is P06-S036: after the limiter's wait and a re-queue, the retry meets the throttle's gap
and cooldown measured from its own first admit. RL-16 is unchanged.

P06-S051. HISTORICAL (legacy documents; data, not proof of what ran, and not statements of Rama recorded by this
project): (a) `docs/decisions/10_entry_throttle_admission.md` (19-Jul-2026), status "OPEN — Rama's call", sets out
arrival-order admission against changed parameters or ranked admission; A02 holds it among its intent sources (IS-147,
"entry-throttle admission (RS-18)"); (b) `docs/audit/rulings_1_2_verification_07aug2026.md` L395 (OPEN-2) says that the
300 s cooldown "contradicts the ruling's wording", quoting a ruling attributed to Rama that a symbol "immediately
becomes eligible again", and asks whether "immediately" governs throttles too; (c) the 02-Jul-2026 design and audit
documents describe the throttle as masking a duplicate retry (P06-S036). These are intent sources for the AUDIT; this
part does not weigh them.

## 8. Points the AUDIT may examine (neutral)

1. The record point: the stated intent counts "PLACED entries" (commit `575a1dc`: "called right before placement so
   only PLACED entries count"; docstring L7 to L8; file comments L350, L352; `docs/CONFIG_GUIDE.md` L343 to L344),
   while the code records every admit before `place()`, whatever its outcome (P06-S010, P06-S034).
2. The FIX-069 rate-limit retry meets the throttle measured from its own first admit (P06-S036; the time limits that
   also apply to it, P06-S052). The AUDIT may examine
   it under the A01 AUDIT's four-condition rule: a retry mechanism exists and its comments say it retries (conditions
   (a) and (c) appear to hold); whether the block is certain depends on the settings and the time to reach the
   throttle (condition (b)); the intent sources differ (FIX-069's "Max 3 retries" and the test "retry preserved"
   against the 02-Jul-2026 documents' account of the throttle masking a duplicate) (condition (d)). No classification
   is given here.
3. At the file values the burst gate can block only in an exact-equality case, so in effect the gap gate and the
   cooldown do the work (P06-S014, P06-S041).
4. The reservation, the `RESERVED` status and the `INTRADAY SIGNAL` alert all come before the throttle on all three
   paths (P06-S027, P06-S030, P06-S031, P06-S035).
5. The gate that blocked is kept only in free text and in process-life counters; `category` is never read
   (P06-S033, P06-S017); the daily trade review groups the status with other capital-check rejects (P06-S053).
6. Which of several simultaneous approvals is admitted is decided by lock order after risk approval and reservation,
   not by arrival at the receiver, `triggered_at` or score (P06-S038); a legacy decision on this was recorded as OPEN
   (P06-S051).
7. The cooldown runs from entry to entry and knows nothing of exits (P06-S015); a legacy document records a ruling
   whose wording it may not match (P06-S051).
8. The per-symbol key is the exact symbol text; different texts for one instrument are separate keys (P06-S011).
9. State and counters are in memory only: lost on restart, never reset daily (P06-S044); one throttle per process
   (P06-S026).
10. With the burst gate off and another gate on, `_recent` grows without bound for the life of the process
    (P06-S012); not at the file values.
11. No validators on the four keys: a negative value silently turns a gate off; a zero window becomes 60 s; absent
    keys disable the throttle (P06-S005, P06-S022, P06-S024; A02 K-12).
12. The release at the throttle site is not inside a `try` (P06-S028).
13. A test comment names the burst gate where the code's blocking gate is the gap gate (P06-S016).
14. `entries_admitted` counts admits, not placements, beside `entries_placed` in the same `/metrics` answer
    (P06-S017, P06-S034).

## 9. UNKNOWN / NOT ESTABLISHED

1. The effective values of the four keys on the legacy machines (A02); only the repository file values are known
   (P06-S021).
2. Whether and when commits `575a1dc` and `c0554c6` (and the later call-site commits `9f56b07` and `536172c`) were
   deployed, and whether any throttle refusal happened in production; the counts in legacy documents are HISTORICAL
   (P06-S014, P06-S019, P06-S041).
3. The Python version on the legacy machines (P04-S063); the lock, clock and deque behaviour used here is that of the
   current documentation (P06-S006, P06-S012, P06-S038).
4. Whether the gate-release path and the retest path were ever reached in production (P06-S030, P06-S031), and whether
   the allocator ran in enforce mode (P06-S029).
5. Whether a `BrokerRateLimitError` ever reached the FIX-069 retry, and how long a retry took to reach the throttle
   (P06-S036, P06-S052).
6. How often and when the trading process was restarted, and whether more than one trading process ran at once
   (P06-S026, P06-S044).
7. Whether `place()` can decline an entry without raising, which would leave an admit with no order (A10; P06-S034).
8. The order in which waiting callers actually acquired the lock at runtime (P06-S038).

## 10. Draft questions about intent for Rama

1. Was the entry throttle meant to count an entry when it is cleared for placement, or only once an order has been
   sent to the broker (or filled)?
2. When a placement is retried after a client-side rate-limit error (FIX-069), was the retry meant to be subject to
   the throttle's 20-second gap and 300-second same-symbol cooldown, measured from its own first attempt?
3. Was the same-symbol cooldown meant to run from the previous entry, or from the exit of the previous position?
4. When several approved signals reach the throttle together, which one was meant to be admitted?
5. Was the `INTRADAY SIGNAL` alert meant to be sent for a signal that the throttle then refuses?
6. Was the throttle's memory of recent entries meant to survive a restart of the trading process?
7. Was the gate that refused an entry (gap, burst or same-symbol) meant to be recorded as a separate field of the
   signal record?

## 11. Where the direction's questions are answered

| Direction question (section 4) | Statements in this part | Other parts |
|---|---|---|
| 1 to 10 | not in this part | P01, P02, P03, P07 |
| 11 Throttling (entry throttle): algorithm, units, windows, bursts, defaults, locking, race behaviour | P06-S001 to P06-S025, P06-S038 to P06-S039 | P03 (receiver's per-address limiter) |
| 12 Limits reached, missing or corrupt state, lock contention, restart, exceptions; fail-open or fail-closed (throttle side) | P06-S018, P06-S028, P06-S034, P06-S042 to P06-S045 | P03, P04 |
| 13 Queue threshold and capacity | not in this part | P03, P04 |
| 14 Concurrency boundaries; duplicate, lost or reordered signals (throttle side) | P06-S026, P06-S036 to P06-S041, P06-S052 | P03, P04 |
| 15 to 19 | not in this part (the throttle is after the handoff to A07) | P04, P05 |
| 20 Event persistence (throttle-reject status write, interface only) | P06-S029 to P06-S031; the status's reader in the daily review, P06-S053 | P05 |
| 21, 22 Wiring and lifecycle (throttle construction only) | P06-S023, P06-S026 | P01, P04 |
| 23 Storage boundaries | not in this part (status writes are P05's) | P03, P05 |
| 24 A04 rate-limiter boundary (throttle side only) | P06-S036, P06-S046 to P06-S050 | P05 |
| 25 Handoffs to A07 | not in this part (the three sites lie after the handoff; P06-S027) | P05 |
| 26 Intended-behaviour sources (throttle) | P06-S019, P06-S020, P06-S022, P06-S051, P06-S053 (comment), P06-S054 (test) | all parts |
| 27, 28 Whole-topic audit, matches and unknowns | sections 8 and 9 | AUDIT |

## 12. Check log

Check pass by a separate read-only helper, 17-Nov-2026 (IST). Draft copy kept at
`parts/drafts/A06_P06_ENTRY_THROTTLE_DRAFT.md`. Every statement was re-read against its cited source: the legacy lines
at `970aabf` with `git show`, `git grep`, `git blame` and `git log` (output filtered for identifier-shaped text); the
project records under `algocore_system` (`main`, `11a9a8a`); the four Python documentation pages, re-opened on
17-Nov-2026 (page version 3.15.2), whose quoted passages were confirmed word for word.

**Statements checked:** 51 (P06-S001 to P06-S051). Correct as written: 42. Corrected: 9. Withdrawn: 0.
Added: 3 (P06-S052 to P06-S054).

| ID | What changed | Why |
|---|---|---|
| P06-S013 | Added that the per-symbol gate's measured elapsed time is formatted with no decimals (L106) | The statement named only the gap's one-decimal format; the per-symbol format differs |
| P06-S029 | Added the allocator-error fall-through (L1171 to L1172) to the fused-path conditions; the `P2_REJECT` evidence described as a call that does nothing without a recorder (L595 to L597) | Completeness and precision against the code |
| P06-S031 | Reservation range L2470 changed to L2469 | The FIX-018 increment block starts at L2469 |
| P06-S032 | Effect-telemetry count placed on the fused path only (L1423); gate and retest paths have only the `P1_ACCEPT` capture between admit and place; the non-call search hits named | The statement said the count was on all three paths; L213 to L216 and L2235 to L2251, L2538 to L2553 show otherwise |
| P06-S036 | The retry reaches `admit` only if it passes the intake and A07 steps again, including the age check against the original `triggered_at`; the burst exact-equality case added; pointer to P06-S052 | The statement said the retry reaches `admit` unconditionally |
| P06-S038 | Part (c) rewritten: the first caller to acquire the lock is admitted; among waiting callers the order "is not defined" | The draft asserted an order "in practice" that the cited documentation does not give (no raw assumptions) |
| P06-S041 | Basis changed to the gate order (P06-S008); the reference to the receiver's claim removed as a basis | The conclusion follows from the gate order alone; the claim can itself be broken (P04-S058) |
| P06-S042 | Evidence record and `INTRADAY SIGNAL` alert made conditional on their wiring (L499 to L500, L595 to L597) | The draft stated both unconditionally |
| P06-S047 | "Per process" relabelled INTERPRETATION (from P06-S026) | It rests on reasoning, not directly on a cited line |

Also updated to follow the changes (no statement content changed): section 1.1 (sources read in the check), section 8
points 2 and 5, section 9 item 5, and the rows for questions 14, 20 and 26 of section 11.

**Statements added (each verified):**
- P06-S052: the only time limit between a FIX-069 retry's intake and its admit is the age check against the original
  trigger time (600 s at the file value); with the 300 s cooldown, a retry is admitted only if it waits for most of
  the cooldown; a quick retry is refused at the throttle, a late one rejected `EXPIRED`.
- P06-S053: interface: the daily trade review (A15) puts any status containing `ENTRY_THROTTLED` in its
  `CAPITAL_CHECK` stage; an evidence-contract comment notes the throttled order was fully sized (HISTORICAL).
- P06-S054: HISTORICAL test of the retest path: a throttle refusal after reservation releases it, places nothing and
  writes `REJECTED_ENTRY_THROTTLED`.

**Completeness against the brief:** item 1 (module in whole) covered by P06-S001 to P06-S025; item 2 (construction,
three call sites, return value, release `"entry_throttled"`) by P06-S026 to P06-S036, P06-S052 to P06-S054; item 3
(concurrency, with the Python documentation) by P06-S037 to P06-S041; item 4 (A04-31, A06 side) by
P06-S046 and P06-S047. Direction questions 11, 12 and 14 are answered in the section 11 table. The brief's construction lines
"L261 to L263" are, at `970aabf`, the comment L259 to L261, the import L262 and the call L263 to L268 (P06-S026); the
three call sites are at the brief's lines.

**Could not verify / not done:** nothing within scope was left unverified. Runtime facts (deployment, refusals,
counter values, lock order, retries) stay UNKNOWN / NOT ESTABLISHED by rule. No legacy code, test or script was run or
imported; no endpoint was contacted; no repository was edited. A07, A09, A10, A15 and A18 logic was read only at the
interface.
