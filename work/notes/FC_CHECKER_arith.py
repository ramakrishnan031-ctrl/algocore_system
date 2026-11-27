# FC checker's independent re-derivation (A08 AUDIT part FC). Re-states expressions read at the baseline 970aabf;
# imports nothing from the legacy clone; reads no file; writes nothing. Run with: python3 -I <this file>
#
# Expressions re-stated (read at 970aabf):
#   sr_detector/zone_cache.py  L47  get():  miss if age > ttl ;  L54-L56 due for re-warm if age >= ttl - margin
#   sr_detector/zone_cache.py  L37  warmed_at = now at put()
#   sr_detector/fetch.py       L144-L146 stale if age > ttl ; L127-L128, L151 store only a non-empty list, at store time
#   sr_detector/zone_warmer.py L104-L119 loop: q.get(timeout=idle) -> Empty -> rescan (L108, L121-L124) -> enqueue
#                              L113-L115 pending.discard then warm; L132-L135 fetch miss -> no put, warmed_at unchanged
#   main.py                    L428-L437 closure: rate_limiter.acquire("historical") once per call, then historical_data
#   broker/rate_limiter.py     L58-L74 bucket starts full (capacity=burst), refills rate_per_sec x elapsed, capped;
#                              L204-L233 acquire polls (<= 0.1 s sleeps) until a token is available
# Committed values: config/system_config.yaml L512 (cache_ttl_sec 1800), L537 (zone_cache_ttl_sec 1800),
#   L538 (zone_rewarm_margin_sec 300), L510 (3 intervals); zone_warmer.py L41 (idle_sleep_sec 2.0);
#   config/broker_limits.yaml L17-L19 (historical burst 2, rate_per_sec 2).
import math

F_TTL, Z_TTL, MARGIN, IDLE, N_INT = 1800.0, 1800.0, 300.0, 2.0, 3
BURST, RATE, POLL = 2.0, 2.0, 0.1
CUTOFF = Z_TTL - MARGIN

print("== A. normal re-warm cycle for one symbol (fresh fetch at t=0; idle scans every 2.0 s; calls instant) ==")
t, fetched_at, warmed_at = 0.0, 0.0, 0.0
fresh_times = [0.0]
max_candle_age_served = 0.0
log = []
scan = 0.0
while t < 6 * 3600:
    scan += IDLE                                   # idle scans every IDLE s (queue otherwise empty)
    if scan - warmed_at >= CUTOFF:                 # due (zone_cache L56)
        # just before this re-warm, get() serves the set if its age <= Z_TTL (L47): candles' age then:
        if scan - warmed_at <= Z_TTL:
            max_candle_age_served = max(max_candle_age_served, scan - fetched_at)
        cached = not ((scan - fetched_at) > F_TTL)  # fetch.py L145
        if not cached:
            fetched_at = scan
            fresh_times.append(scan)
        log.append((scan, "fetcher cache" if cached else "fresh fetch", scan - fetched_at))
        warmed_at = scan                           # put() after scoring (zone_cache L37)
    t = scan
for row in log[:6]:
    print(f"  re-warm at t={row[0]:7.0f} s: {row[1]:13s}; candles behind the new set {row[2]:6.0f} s old")
kinds = [r[1] for r in log]
alt = all(kinds[i] != kinds[i + 1] for i in range(len(kinds) - 1))
print(f"  re-warms in 6 h: {len(log)}; alternate cached/fresh throughout: {alt}; "
      f"fresh fetches per hour: {(len(fresh_times) - 1) / 6:.2f} -> broker calls per hour: {N_INT * (len(fresh_times) - 1) / 6:.2f}")
print(f"  oldest candles behind a set that get() still serves (normal cycle): about {max_candle_age_served:.0f} s "
      f"(set age reported about {CUTOFF:.0f} s)")
print(f"  extreme: set put at its fetcher list's TTL ({F_TTL:.0f} s old candles), served until its own TTL: "
      f"{F_TTL + Z_TTL:.0f} s")


def failing_rate(k_symbols, d, horizon=600.0):
    """k stored symbols whose every interval call fails (or is empty) after taking a token; each call lasts d s."""
    tokens, last = BURST, 0.0
    now, calls = 0.0, 0

    def refill(at):
        nonlocal tokens, last
        tokens = min(BURST, tokens + (at - last) * RATE)
        last = at

    while now < horizon:
        now += IDLE                                  # q.get(timeout=2.0) -> Empty -> rescan -> enqueue k symbols
        for _ in range(k_symbols):                   # worker takes them back to back
            for _ in range(N_INT):                   # fetch_timeframes: one _fetch_one per interval, each misses
                refill(now)
                while tokens < 1.0:                  # acquire polls in <= 0.1 s steps (rate_limiter L225-L237)
                    now += min(POLL, (1.0 - tokens) / RATE)
                    refill(now)
                tokens -= 1.0
                calls += 1
                now += d                             # the failed/empty broker call
    return calls / now


print("== B. a stored symbol whose re-warm gets no data: historical calls per second (committed bucket 2/s) ==")
for d in (0.0, 0.05, 0.1, 0.25, 0.5):
    r1 = failing_rate(1, d)
    print(f"  one symbol, call time {d:4.2f} s: {r1:.3f} per s = {100 * r1 / RATE:5.1f} % of 2/s")
print(f"  upper bound if the bucket's own wait is left out: {N_INT / IDLE:.2f} per s = {100 * N_INT / IDLE / RATE:.0f} %")
for k in (2, 3, 5, 10):
    rk = failing_rate(k, 0.0)
    print(f"  {k} such symbols, instant calls: {rk:.3f} per s = {100 * rk / RATE:5.1f} % of 2/s")
