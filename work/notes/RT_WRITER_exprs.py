# RT writer: plain-expression checks (current external context; work environment interpreter).
# Re-states expressions read at the baseline; imports NOTHING from the legacy clone; reads and writes no file.
import math
import sys
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone

print("python", sys.version.split()[0])
IST = timezone(timedelta(hours=5, minutes=30), name="IST")   # core/time_authority.py L58-L59, restated

# (1) screening/retest_monitor.py L368 + L171 restated: aware now minus naive added_at
aware_now = datetime.now(tz=IST)                 # now_ist() L99 restated
added_at = datetime.now(tz=IST).replace(tzinfo=None)   # L368 restated
try:
    (aware_now - added_at).total_seconds()
    print("(1) aware - naive: no error")
except TypeError as e:
    print("(1) aware - naive: TypeError:", e)

# (1b) the restored form: L239 writes naive isoformat; L251 fromisoformat
txt = added_at.replace(tzinfo=None).isoformat()
back = datetime.fromisoformat(txt)
print("(1b) restored tzinfo:", back.tzinfo)
try:
    (aware_now - back).total_seconds()
    print("(1b) aware - restored: no error")
except TypeError as e:
    print("(1b) aware - restored: TypeError:", e)

# (1c) naive minus naive (the tests' clock form) works
print("(1c) naive - naive seconds >= 0:", (datetime.now() - datetime.now().replace(microsecond=0)).total_seconds() >= 0)

# (1d) L231 restated: naive added_at + timedelta isoformat carries no offset
print("(1d) timeout_at text:", (added_at + timedelta(seconds=1800.0)).isoformat()[-6:], "(no offset)")

# (2) the one-minute fetcher's TTL test, sr_detector/fetch.py L144-L145 restated, TTL 0.0
ttl = 0.0
for age in (20.0, 0.0, -5.0):
    print("(2) age", age, "served:", not (age > ttl))

# (3) evaluate's timeout test L89 restated (strict)
for el in (1800.0, 1800.000001, float("nan")):
    print("(3) elapsed", el, "times out:", el > 1800.0)

# (4) _strong_close L133-L137 restated, LONG, frac 0.6
@dataclass(frozen=True)
class C:
    high: float
    low: float
    close: float

def strong(c, frac, is_long=True):
    rng = c.high - c.low
    if rng <= 0:
        return c.close >= c.high if is_long else c.close <= c.low
    pos = (c.close - c.low) / rng if is_long else (c.high - c.close) / rng
    return pos >= frac

print("(4) close at 40% of range, LONG:", strong(C(110.0, 100.0, 104.0), 0.6))
print("(4) close at 60% of range, LONG:", strong(C(110.0, 100.0, 106.0), 0.6))
print("(4) flat bar, LONG and SHORT:", strong(C(100.0, 100.0, 100.0), 0.6, True), strong(C(100.0, 100.0, 100.0), 0.6, False))

# (5) contains L107-L109 restated with NaN / inf entry
def contains(lo, hi, price, buf):
    pad = ((lo + hi) / 2.0) * (buf / 100.0)
    return (lo - pad) <= price <= (hi + pad)
print("(5) NaN entry contained:", contains(100.0, 101.0, float("nan"), 0.3), "inf:", contains(100.0, 101.0, float("inf"), 0.3))

# (6) L363 restated: float(trigger_price or 0.0)
print("(6) None ->", float(None or 0.0), " nan ->", float(float("nan") or 0.0), " 0 ->", float(0 or 0.0))

# (7) frozen dataclass replace leaves the original
@dataclass(frozen=True)
class P:
    state: str = "WAIT_BREAKOUT"
p = P(); q = replace(p, state="WAIT_RETEST")
print("(7) replace:", p.state, q.state)

# (8) direction tests: _is_long (L50-L51) vs exact (L399, L2435) for 'long'
d = "long"
print("(8) _is_long('long'):", str(d).strip().upper() in ("LONG", "BUY"), " exact:", d in ("LONG", "BUY"))
