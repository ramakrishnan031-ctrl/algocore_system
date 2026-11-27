"""VO writer's check script (working material, not kept: D-17).

Runs only `git show 970aabf:<path>` against the legacy clone and parses the TEXT;
imports nothing from the legacy clone; writes nothing; runs no SQL.
Also re-states a few expressions read at the baseline, on literal values only.
"""
import ast
import json
import math
import re
import subprocess
from datetime import datetime, timedelta, timezone

CLONE = "/home/claude/repos/legacy"


def show(path):
    return subprocess.run(["git", "-C", CLONE, "show", f"970aabf:{path}"],
                          capture_output=True, text=True, check=True).stdout.splitlines()


def lines(path, a, b):
    src = show(path)
    return "\n".join(src[a - 1:b])


# 1. The 24 insert columns against the two A08 writers' row keys (text only).
cols_txt = lines("core/state_store.py", 1970, 1977)
cols = re.findall(r'"([a-z_]+)"', cols_txt)
det_txt = lines("sr_detector/detector.py", 269, 294)
det_keys = re.findall(r'^\s*"([a-z_]+)":', det_txt, flags=re.M)
div_txt = lines("screening/retest_monitor.py", 413, 431)
div_keys = re.findall(r'"([a-z_]+)":', div_txt)
print("1. _SR_INSERT_COLS:", len(cols), "| detector keys:", len(det_keys),
      "| divert keys:", len(div_keys))
print("   detector == cols (content and order):", det_keys == cols)
print("   divert == cols (content and order):", div_keys == cols)

# 2. Re-state _breakout_flags (flags.py L159 to L175) for the long side.
def breakout_long(band_low, band_high, last_close, last_high, last_vol, avg_vol,
                  frac=0.25, mult=1.5):
    width = max(band_high - band_low, 1e-9)
    cleared = last_close > band_high
    poke_fail = last_high > band_high and last_close <= band_high
    weak = cleared and (last_close - band_high) < frac * width
    any_breakout = cleared or poke_fail
    out = []
    if weak or poke_fail:
        out.append("WEAK_BREAKOUT")
    if any_breakout and avg_vol > 0 and last_vol < mult * avg_vol:
        out.append("NO_VOLUME_CONFIRMATION")
    return out

# a lone candle: _breakout_context (detector.py L242 to L243) gives avg = its own volume
print("2a. lone candle, volume 1000, close far above a zone:",
      breakout_long(100, 101, 150, 151, 1000, float(1000)))
# a zone far below the entry, ordinary volume (0.9 x average)
print("2b. zone 100-101, close 150, volume 0.9x avg:",
      breakout_long(100, 101, 150, 151, 900, 1000))
# zero average volume
print("2c. zero average:", breakout_long(100, 101, 150, 151, 0, 0.0))
# zero-width zone: weak needs clearance < 0.25 * 1e-9
print("2d. zero-width zone 100-100, close 100.0000000001:",
      breakout_long(100, 100, 100.0000000001, 100.0000000001, 5000, 1000))

# 3. Re-state _nearest / _is_into_zone (flags.py L114 to L122, L138 to L146) on an
#    example: a nearer LOW resistance and a farther HIGH one that also holds the entry
#    within its one-sided pad.
zones = [  # (band_low, band_high, confidence)
    (100.0, 100.2, "LOW"),
    (100.6, 101.0, "HIGH"),
]
entry = 100.1
def center(z):
    return (z[0] + z[1]) / 2.0
preferred = [z for z in zones if z[1] >= entry]
pool = preferred or zones
nearest = min(pool, key=lambda z: abs(center(z) - entry))
def into_long(e, z, pct=1.0):
    pad = center(z) * (pct / 100.0)
    return (z[0] - pad) <= e <= z[1]
print("3. nearest:", nearest, "| into nearest:", into_long(entry, nearest),
      "| into the HIGH zone:", into_long(entry, zones[1]))
# fallback: no resistance at or above the entry
zones2 = [(90.0, 91.0, "HIGH"), (95.0, 95.5, "LOW")]
e2 = 100.0
pref2 = [z for z in zones2 if z[1] >= e2]
near2 = min(pref2 or zones2, key=lambda z: abs(center(z) - e2))
print("   fallback nearest resistance:", near2, "dist % =",
      round((center(near2) - e2) / e2 * 100.0, 4))

# 4. Plain expressions (Python semantics; local interpreter, not production).
nan, inf = float("nan"), float("inf")
print("4. bool(nan):", bool(nan), "| bool(inf):", bool(inf), "| nan <= 0:", nan <= 0,
      "| -inf <= 0:", -inf <= 0)
for p in (nan, inf):
    try:
        math.floor(math.log10(p))
        print("   floor(log10(%r)) no raise" % p)
    except Exception as exc:
        print("   floor(log10(%r)) raises %s: %s" % (p, type(exc).__name__, exc))
print("   json.dumps(nan, compact):", json.dumps(nan, separators=(",", ":")),
      "| json.dumps(inf):", json.dumps(inf))
print("   json.loads('NaN') is nan-like:", math.isnan(json.loads("NaN")))

# 5. IST stamps and their UTC dates (a re-statement of the offset arithmetic that
#    SQLite date() applies by its documentation as P03-S005 (f) records; no SQL run).
IST = timezone(timedelta(hours=5, minutes=30), name="IST")
for hh, mm in ((5, 29), (5, 30), (9, 15), (15, 30), (23, 59)):
    t = datetime(2026, 7, 1, hh, mm, tzinfo=IST)
    print("5. IST %02d:%02d -> UTC date %s (IST date %s)" %
          (hh, mm, t.astimezone(timezone.utc).date(), t.date()))
print("   isoformat aware:", datetime(2026, 7, 1, 10, 0, 0, 123456, tzinfo=IST).isoformat())
print("   isoformat naive:", datetime(2026, 7, 1, 10, 0, 0, 123456).isoformat())
# text ordering of the two forms written in the same table (the A15 report orders by text)
a = datetime(2026, 7, 1, 10, 0, 0, 123456).isoformat()          # divert, naive
b = datetime(2026, 7, 1, 10, 5, 0, 7, tzinfo=IST).isoformat()  # observer, aware
print("   text order naive-earlier < aware-later:", a < b)

# 6. The proposal stop (flags.py L180) with the two buffers on one zone.
band_low = 500.0
print("6. V1 stop (0.3):", round(band_low * (1 - 0.3 / 100.0), 6),
      "| V2-formula stop (0.2):", round(band_low * (1 - 0.2 / 100.0), 6))

# 7. _breakout_context window slice (detector.py L242) for small/odd windows.
lst = list(range(10))
for w in (20, 0, -1):
    print("7. window %d -> slice" % w, lst[-(w + 1):-1])
