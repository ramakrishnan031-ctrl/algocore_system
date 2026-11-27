"""ISB writer: shorten quotations of 15 words or more in the legacy-half file (my own file only)."""
import pathlib
F = pathlib.Path('/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md')
t = F.read_text(encoding='utf-8')
R = [
 ('pivots come "in bar order (a bar may yield both a HIGH and a LOW pivot only in degenerate single-bar windows; normally one or neither)" (CD-502)',
  'pivots come "in bar order", and a bar yields both a HIGH and a LOW pivot "only in degenerate single-bar windows" (CD-502)'),
 ('"Confidence is NEVER a single method — it is a weighted sum of independent votes", with the evidence kept',
  'confidence is "NEVER a single method", "a weighted sum of independent votes", with the evidence kept'),
 ('SR-F3: an "Intra-session cache keyed by (symbol, interval) with a TTL, so a re-signalling symbol is not re-fetched" (CD-509); SR-F4: "Every failure path (no token, fetch raises, empty result) returns None for that TF; nothing propagates into the pipeline" (CD-508)',
  'SR-F3: an "Intra-session cache keyed by (symbol, interval) with a TTL", so that a re-signalling symbol is not re-fetched (CD-509); SR-F4: "Every failure path (no token, fetch raises, empty result)" returns `None` for that timeframe, and "nothing propagates into the pipeline" (CD-508)'),
 ('"The SINGLE zone-building path, shared by the V1 detector (async observer) and the V2 ZoneWarmer"',
  '"The SINGLE zone-building path", shared by the V1 detector and the V2 warmer'),
 ('are "Reference levels for the manual-marking validation export; they do NOT gate capital in this step"',
  'are "Reference levels for the manual-marking validation export" that "do NOT gate capital in this step"'),
 ('"a miss / expired entry returns None and the caller falls through to normal placement"',
  'a miss or an expired entry returns `None` and "the caller falls through to normal placement"'),
 ('so that "the cache is hot by the time (or soon after) the pipeline reaches the divert check"',
  'so that the cache is "hot by the time (or soon after) the pipeline reaches the divert check"'),
 ('"Only TERMINAL trades are finalised; a still-open trade is left NULL so a later run picks it up" (CD-515, CD-517)',
  '"Only TERMINAL trades are finalised", and a still-open trade "is left NULL so a later run picks it up" (CD-515, CD-517)'),
 ('the guard "FAILS OPEN (weekday fallback on any calendar error) so a trading day is never skipped"; "The guard is here and not in main() so a manual/ad-hoc run on a non-trading day is never blocked" (CD-516)',
  'the guard "FAILS OPEN" (a weekday fallback on any calendar error) "so a trading day is never skipped"; it is outside `main()` "so a manual/ad-hoc run on a non-trading day is never blocked" (CD-516)'),
 ('the backfill "was authored 27-Jun but never registered in the cron framework, so outcomes stayed NULL until run by hand"',
  'the backfill "was authored 27-Jun but never registered in the cron framework", so "outcomes stayed NULL until run by hand"'),
 ('`_strong_close`: "LONG wants the close in the UPPER frac of the 1m range, SHORT in the LOWER frac" (IC-503)',
  '`_strong_close`: "LONG wants the close in the UPPER frac of the 1m range", a short in the lower (IC-503)'),
 ('"Restart-safe like EntryGate: persists to retest_state, rehydrates on boot, deletes the row atomically on release" (CD-520)',
  '"Restart-safe like EntryGate": it persists to `retest_state`, rehydrates on boot and "deletes the row atomically on release" (CD-520)'),
 ('"Release the parking row first (so it can\'t be re-evaluated), then resume the pipeline. No capital was held → nothing to release."',
  '"Release the parking row first (so it can\'t be re-evaluated)", then resume the pipeline; "No capital was held → nothing to release"'),
 ('"a later bookkeeping exception must NOT fall through to placement (that is the double-order path)"',
  'a later bookkeeping exception "must NOT fall through to placement (that is the double-order path)"'),
 ('the monitor "rehydrates from it on boot and deletes the row atomically on release (confirm / reject / EOD)" (CD-520)',
  'the monitor rehydrates from it on boot and "deletes the row atomically on release (confirm / reject / EOD)" (CD-520)'),
 ('and "places a MARKET entry with a STRUCTURE SL below the reclaimed zone + an R:R-preserving TGT" (IC-502)',
  'and places "a MARKET entry with a STRUCTURE SL below the reclaimed zone" and "an R:R-preserving TGT" (IC-502)'),
 ('"the two resume-path dispatch sites are production-unreachable and deliberately uncounted; their awakening surfaces at the gate units"',
  'the two resume-path dispatch sites are "production-unreachable and deliberately uncounted", their awakening surfacing "at the gate units"'),
 ('"The diverter is late-bound into signal_processor; the monitor is rehydrated from retest_state and started; both daemons stop in _shutdown. eod clears parked candidates at square-off. Dormant when off."',
  'the diverter is "late-bound into signal_processor", the monitor "rehydrated from retest_state and started"; "both daemons stop in _shutdown"; the square-off "clears parked candidates"; "Dormant when off"'),
 ('"clear parked WAIT_FOR_RETEST candidates (in-memory + retest_state) so none survive into the next session (mirrors FIX-046 for the gate)" (CD-520)',
  'clear the parked candidates, in memory and in `retest_state`, "so none survive into the next session (mirrors FIX-046 for the gate)" (CD-520)'),
 ('"Run ONCE against a known-split stock on the VM (needs a live token); note the result in SYSTEM_MAP"',
  '"Run ONCE against a known-split stock on the VM", with a live token, and "note the result in SYSTEM_MAP"'),
 ('wires "a READ-ONLY market-data kite + OhlcFetcher + detector (anchors enabled), one as-of the requested date\'s session close" (CD-524)',
  'wires "a READ-ONLY market-data kite + OhlcFetcher + detector (anchors enabled)", one per request, as of the requested date\'s close (CD-524)'),
 ('"When disabled (the default) the detector is not even constructed (main.py passes sr_detector=None) → zero pipeline change"',
  '"When disabled (the default) the detector is not even constructed", "zero pipeline change"'),
 ('"SE2 -- HIGH-confidence zones only (min_zone_confidence). No valid zone → DO NOTHING (leave the current SL)"; "SE3 -- Break = a 1-MINUTE candle CLOSE beyond the band (+ optional strong close)"; the exit will "reuse Phase A\'s pure strong-close predicate", keeping "the break-confirmation byte-identical to the entry-side confirm (only the is_long polarity flips for the exit side)"',
  'SE2: "HIGH-confidence zones only"; "No valid zone → DO NOTHING (leave the current SL)"; SE3: a break is "a 1-MINUTE candle CLOSE beyond the band", with an optional strong close; the exit will "reuse Phase A\'s pure strong-close predicate", "byte-identical to the entry-side confirm", "only the is_long polarity flips"'),
 ('"S&R consumption must stay a synchronous cache read — a hot-path fetch would perturb latency"',
  '"S&R consumption must stay a synchronous cache read", as a hot-path fetch "would perturb latency"'),
 ('are "**PARTIAL** — only when the detector logged the signal (shadow); `N/A — no data` otherwise"',
  'are "**PARTIAL**", "only when the detector logged the signal (shadow)", `N/A` otherwise'),
 ('"They share the 0.2 default by design (parallel knobs) but each owns its own value and may be tuned apart; this is deliberate parallelism"',
  '"They share the 0.2 default by design (parallel knobs)", but each owns its value and "may be tuned apart; this is deliberate parallelism"'),
]
for old, new in R:
    n = t.count(old)
    assert n >= 1, ('NOT FOUND', old[:80])
    t = t.replace(old, new)
    print(n, 'x', old[:60])
F.write_text(t, encoding='utf-8')
print('done')
