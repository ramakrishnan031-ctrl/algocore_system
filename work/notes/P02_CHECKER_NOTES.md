# P02 checker scratch notes (H7)

## Corrections to apply (status: [ ] to do, [x] done)
Section 1
- [ ] S005: add (b) GIL sentence (threading page, CPython implementation detail); (d) subtraction rule ("Subtraction of a datetime from a datetime is defined only if both operands are naive, or if both are aware. If one is aware and the other is naive, TypeError is raised."), now(): "Return the current local date and time"; "If optional argument tz is None or not specified, this is like today()"; "Subsequent calls to datetime.now() may return the same instant depending on the precision of the underlying clock"; today(): "functionally equivalent to now(), but without a tz parameter". Checker re-read note.
- [ ] NEW S160 (after S005): pydantic model_copy: "Updates are _not_ applied recursively, and no validation is performed on updated values." (latest docs; pinned pydantic==2.13.0, requirements.txt L7).
Section 2
- [ ] S007: "read at `970aabf` only" -> "read at the baseline only".
- [ ] S008: add `from __future__ import annotations` (fetch L23, zone_builder L9, zone_cache L12, zone_warmer L18); aliases `date as _date`, `time as _time` (L13).
Section 3
- [ ] S019: int(inf float) -> OverflowError.
- [ ] S023: exact `_IST_OFFSET`/`_IST` lines.
- [ ] S026: session_vwap sums bars with positive volume (L149 to L155).
- [ ] S029: correct the docs basis (now(tz) "current local date and time" converted to tz; "like today()" only when tz is None).
- [ ] S031: negative TTL serves after a backward clock step larger than |TTL|.
- [ ] S035/S036: other outside-try raises (unhashable key/interval L140; non-iterable intervals L64), no non-test caller passes them; OverflowError.
- [ ] S038: ValueError raised at rate_limiter L170 (in _get_bucket).
- [ ] S040: row 1 add candidate.ts condition (detector L218 to L219); row 2 thread "market-regime" (regime/runner.py L50); row 7 its own closure and limiter (sr_level_export L143 to L145).
- [ ] S041: clarify anchor-interval window wording.
- [ ] S042 (c): model_copy citation -> pydantic docs (S160) + argparse no choices (L182); A02 L-45 records the copy and no validation on assignment.
Section 4
- [ ] S054 (a): exactly three values in exact arithmetic (b, b+M/2, b+M); fewer only below 0.00001 by rounding.
- [ ] S060: reference None when intended entry is falsy (zero or missing).
Section 5
- [ ] S071: _age_sec is called under the lock by symbols_due_for_rewarm and evict_expired; it takes no lock.
Section 6
- [ ] S079: BaseException not caught; on the L98 path after L92 the symbol stays in _pending.
- [ ] S080: lock hold = membership test + insertion, or one removal; PQ-11 MATCH row L3988 and handoff row L4010; GIL note.
- [ ] S084: retry only when the re-warm gives no interval at all; limiter not reached on token failure or None handle.
- [ ] NEW S159 (after S081): enqueue sources only _warm_zones and the re-warm scan; readers never enqueue; consequence for structure exit (positions with no signal in process life).
- [ ] S089: _shutdown sets _shutdown_event first (main.py L1628 to L1629), the limiter's event (L116, L2348): limiter waits already aborted at L1744; only an in-flight broker call outlasts the join.
Section 7
- [ ] S091: regime thread "market-regime".
- [ ] S094: rows: int(token) OverflowError; _cache_get naive/aware; "worker in a broker call at stop".
Section 8
- [ ] S095: hits also include the imports beside each construction.
- [ ] S096: prior_day_levels: confluence.py L39, L133 are the field name.
Section 9
- [ ] S101: six OhlcFetcher( call sites, seven constructions; export over its own closure.
- [ ] S108: PB-01 phrase (TTL 0).
- [ ] S113: PQ-11 MATCH row L3988 + handoff row L4010.
- [ ] S117: add retest_confirm.py L13, L84 (P04's).
- [ ] S122..S128: AFR classification / treatment / status verbatim (treatment OPEN; SX-07 treatment "None (UNKNOWN / NOT ESTABLISHED items receive no treatment)"; CM-07, HA-05, SX-07 full classifications).
- [ ] S126: export's own closure.
- [ ] S133: P01-S052 for /100.
Section 10
- [ ] S146: re-warms before expiry and, when a re-warm is delayed or gets no data, after it.
- [ ] S148: L3725-3727 comment states TTL 0 for the 5-min poll, inputs memoized; not about keeping windows apart.
- [ ] S149: "before its TTL expiry" describes when a re-warm first becomes due; scan returns expired entries too.
- [ ] S153: test_structure_exit_manager L55 (ZoneSet), L61 (ZoneCache double), used L182.
- [ ] S154: search scope: all tracked *.md/*.txt; 18 documents matched; 16 others mention in passing only.
- [ ] S155: label HISTORICAL and INTERPRETATION; "one window length per interval".
- [ ] NEW S158 (10.3): config/expected_managers.yaml registry (HISTORICAL): L4, L351 to L358, L386; commits 297b587cca40d79d6b1d3bb531e7118f9da91dc8, a5c3704d901c188659599405fce1d400ebf9b780, 0197923ecb4954fc3ef1b17acac507fc191c9508.
Section 11-14
- [ ] AP01: balance with HA-06's (d) reasoning; PB-01 TTL-0 comment; export's --interval (argparse no choices; S160).
- [ ] AP06: retry precision.
- [ ] AP16: add registry note.
- [ ] NEW AP17: zone cache filled only from signal arrivals and re-warms (S159).
- [ ] U01: registry declaration note.
- [ ] R1, R3, R4, R5: present tense / code behaviour, both switches off in the committed file.
- [ ] X07: A15 registry; A11 enqueue point.
- [ ] Header revision history; Check log.
