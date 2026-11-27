# FC writer scratch script (A08 AUDIT part FC). Re-states expressions read at the baseline 970aabf;
# imports nothing from the legacy clone; reads no file; writes nothing. Run with: python3 -I <this file>
import math

print("== 1. round_number_levels, re-stated from sr_detector/zone_builder.py L130 to L140 ==")
def rnl(price):
    if price is None or price <= 0:
        return ()
    magnitude = 10.0 ** math.floor(math.log10(price))
    levels = set()
    for step in (magnitude, magnitude / 2.0):
        if step <= 0:
            continue
        below = math.floor(price / step) * step
        levels.add(round(below, 6))
        levels.add(round(below + step, 6))
    return tuple(sorted(levels))

for p in (523.0, 500.0, 0.3, 1.0, 99.99):
    print(p, rnl(p))
for p in (float("nan"), float("inf")):
    try:
        print(p, rnl(p))
    except Exception as e:
        print(p, "raises", type(e).__name__, e)
print("nan <= 0:", float("nan") <= 0, "; math.log10(nan):", math.log10(float("nan")))

print("== 2. ages: fetcher TTL (cache_ttl_sec), zone TTL (zone_cache_ttl_sec), margin (zone_rewarm_margin_sec) ==")
# Committed values (config/system_config.yaml L512, L537, L538); expressions: fetch.py L144 to L146 (age > ttl
# means stale), zone_cache.py L47 (age > ttl is a miss), L54 to L56 (due when age >= ttl - margin).
F_TTL, Z_TTL, MARGIN = 1800.0, 1800.0, 300.0
cutoff = Z_TTL - MARGIN
print("re-warm due at zone age >=", cutoff)
# Cycle with no queue delay: t=0 fresh fetch; each re-warm at warmed_at + cutoff.
t, fetched_at, warmed_at = 0.0, 0.0, 0.0
for i in range(6):
    t = warmed_at + cutoff                       # re-warm instant
    fetcher_age = t - fetched_at
    served_from_fetcher_cache = not (fetcher_age > F_TTL)
    if not served_from_fetcher_cache:
        fetched_at = t                           # fresh broker fetch
    warmed_at = t                                # put() resets warmed_at
    print(f"re-warm {i+1} at t={t:.0f}: fetcher age {fetcher_age:.0f} -> "
          f"{'cached candles' if served_from_fetcher_cache else 'fresh fetch'}; candles now {t - fetched_at:.0f} s old")
# Oldest candles behind a ZoneSet that get() still serves, just before the next re-warm:
print("max candle age seen by get() in the cycle (just before a re-warm):", cutoff + cutoff, "s; zone age reported:", cutoff)
print("extreme (re-warm delayed to expiry; fetcher list served at its TTL):", F_TTL + Z_TTL, "s")

print("== 3. calls per symbol in the committed-value cycle ==")
intervals = 3                                    # knobs.intervals, committed ["day","60minute","30minute"]
period = 2 * cutoff                              # one fresh fetch every second re-warm
print(f"one fresh fetch of {intervals} intervals every {period:.0f} s -> {intervals * 3600 / period:.1f} historical calls per hour per symbol (no queue delay)")
print("historical bucket (config/broker_limits.yaml L17 to L19): burst 2, 2 per second (committed)")

print("== 4. a failed re-warm: re-queued at every idle scan (zone_warmer.py L106 to L108, L121 to L124) ==")
IDLE = 2.0                                       # idle_sleep_sec default, zone_warmer.py L41
print(f"one attempt per {IDLE} s plus the failed fetch's own time; up to {intervals} acquire('historical') per attempt")
