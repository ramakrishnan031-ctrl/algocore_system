"""CZ (A08 AUDIT part CZ) scratch: re-states, by hand, the expressions read at the
baseline 970aabf in sr_detector/pivots.py, zones.py and confluence.py, and
recomputes the worked examples the CZ records rely on. It imports NOTHING from
the legacy clone (standard library only) and reads no legacy file. Working
material (D-17), not kept as a record.
"""
import math
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from itertools import product

C = namedtuple("C", "ts high low volume")
P = namedtuple("P", "price ts kind bar_index")
Z = namedtuple("Z", "band_low band_high kind touches timeframe last_touch_ts")


def center(z):
    return (z.band_low + z.band_high) / 2.0


# pivots.py L37 to L55 (re-stated)
def find_swing_pivots(candles, left, right):
    n = len(candles)
    out = []
    if left < 1 or right < 1 or n < (left + right + 1):
        return out
    for i in range(left, n - right):
        c = candles[i]
        window = candles[i - left: i + right + 1]
        others = [w for j, w in enumerate(window) if (i - left + j) != i]
        if all(c.high >= w.high for w in window) and any(c.high > w.high for w in others):
            out.append(P(c.high, c.ts, "HIGH", i))
        if all(c.low <= w.low for w in window) and any(c.low < w.low for w in others):
            out.append(P(c.low, c.ts, "LOW", i))
    return out


# zones.py L43 to L75 (re-stated)
def cluster_zones(pivots, cluster_pct, timeframe):
    zones = []
    for kind, zk in (("HIGH", "RESISTANCE"), ("LOW", "SUPPORT")):
        same = sorted((p for p in pivots if p.kind == kind), key=lambda p: p.price)
        if not same:
            continue
        cl = [same[0]]
        for p in same[1:]:
            bh = max(x.price for x in cl)
            tol = bh * (cluster_pct / 100.0)
            if p.price <= bh + tol:
                cl.append(p)
            else:
                zones.append(zfc(cl, zk, timeframe))
                cl = [p]
        zones.append(zfc(cl, zk, timeframe))
    return zones


def zfc(cl, kind, tf):
    prices = [p.price for p in cl]
    return Z(min(prices), max(prices), kind, len(cl), tf, max((p.ts for p in cl), default=None))


# confluence.py L80 to L101 (re-stated); returns groups and the tolerances used
def merge(zones_by_tf, kind, merge_pct):
    flat = []
    for tz in zones_by_tf.values():
        flat.extend(z for z in tz if z.kind == kind)
    flat.sort(key=center)
    groups, tols = [], []
    for z in flat:
        if not groups:
            groups.append([z])
            continue
        cur = groups[-1]
        cc = sum(center(x) for x in cur) / len(cur)
        tol = cc * (merge_pct / 100.0)
        tols.append((round(cc, 6), round(tol, 6), round(abs(center(z) - cc), 6)))
        if abs(center(z) - cc) <= tol:
            cur.append(z)
        else:
            groups.append([z])
    return groups, tols


# confluence.py L180 to L192 (re-stated)
def has_round(low, high):
    c = (low + high) / 2.0
    if c <= 0:
        return False
    mag = 10.0 ** math.floor(math.log10(c))
    for step in (mag, mag / 2.0):
        if step <= 0:
            continue
        k = math.ceil(low / step - 1e-9)
        if k * step <= high + 1e-9:
            return True
    return False


def step_of(c):
    return (10.0 ** math.floor(math.log10(c))) / 2.0


# confluence.py L162 to L167 (re-stated), committed thresholds
def bucket(score, distinct, ntf, t_high=5.0, t_med=3.0):
    if score >= t_high and distinct >= 2 and ntf >= 2:
        return "HIGH"
    if score >= t_med:
        return "MEDIUM"
    return "LOW"


def score_shape(T, ntf, vol, prior, rnd, r, w=(1.0, 1.0, 1.0, 1.0, 0.5, 0.5), cap=4):
    """confluence.py L119 to L147 re-stated over a group 'shape'."""
    w_swing, w_volume, w_multi, w_prior, w_round, w_rec = w
    ev = []
    s = w_swing * min(T, cap)
    if s > 0:
        ev.append(("swing_pivots", s))
    m = w_multi * ntf
    if m > 0:
        ev.append(("multi_tf", m))
    if vol:
        ev.append(("volume_node", w_volume))
    if prior:
        ev.append(("prior_day_level", w_prior))
    if rnd:
        ev.append(("round_number", w_round))
    if r > 0 and w_rec > 0:
        ev.append(("recency", w_rec * r))
    sc = sum(c for _, c in ev)
    return sc, len(ev), bucket(sc, len(ev), ntf)


def recency(last_touch, now, window=90.0, min_f=0.0):
    """confluence.py L195 to L211 re-stated."""
    if last_touch is None:
        return 0.0
    if now is None:
        return 1.0
    if (now.tzinfo is None) != (last_touch.tzinfo is None):
        now = now.replace(tzinfo=None)
        last_touch = last_touch.replace(tzinfo=None)
    age = (now - last_touch).total_seconds() / 86400.0
    if window <= 0:
        return 1.0
    f = 1.0 - (age / window)
    return max(min_f, min(1.0, f))


def main():
    t0 = datetime(2026, 6, 1, 9, 15)
    print("== 1 plateau, highs [1,2,5,5,2,1], n=2")
    cs = [C(t0 + timedelta(minutes=i), h, 0.0, 1) for i, h in enumerate([1, 2, 5, 5, 2, 1])]
    print([(p.bar_index, p.price) for p in find_swing_pivots(cs, 2, 2) if p.kind == "HIGH"])

    print("== 2 plateau at committed n=5: 13 bars, two equal tops at positions 6 and 7")
    hs = [1, 2, 3, 4, 5, 6, 9, 9, 6, 5, 4, 3, 2, 1]
    cs = [C(t0 + timedelta(minutes=i), h, 0.0, 1) for i, h in enumerate(hs)]
    piv = [p for p in find_swing_pivots(cs, 5, 5) if p.kind == "HIGH"]
    print([(p.bar_index, p.price) for p in piv], "-> touches in one zone:",
          [z.touches for z in cluster_zones(piv, 0.5, "day")])

    print("== 3 fully flat nine bars, n=2 (the unit test's case)")
    cs = [C(t0 + timedelta(minutes=i), 100, 99, 1) for i in range(9)]
    print(find_swing_pivots(cs, 2, 2))

    print("== 4 outside bar engulfing its window, n=2")
    hl = [(10, 9), (10.5, 9.5), (12, 8), (10.4, 9.4), (10.2, 9.2)]
    cs = [C(t0 + timedelta(minutes=i), h, l, 1) for i, (h, l) in enumerate(hl)]
    print([(p.bar_index, p.kind, p.price) for p in find_swing_pivots(cs, 2, 2)])

    print("== 5 chaining, cluster_pct 0.5")
    pv = [P(x, t0, "HIGH", i) for i, x in enumerate([100.0, 100.4, 100.8, 101.2, 101.6, 102.0])]
    print(cluster_zones(pv, 0.5, "day"))

    print("== 6 merge drift, merge_pct 0.4 (cluster_pct 0.5 keeps the two daily zones apart)")
    d = cluster_zones([P(100.0, t0, "HIGH", 0), P(100.55, t0, "HIGH", 1)], 0.5, "day")
    h = cluster_zones([P(100.35, t0, "HIGH", 0)], 0.5, "60minute")
    print("daily zones:", [(z.band_low, z.band_high) for z in d])
    g, tols = merge({"day": d, "60minute": h}, "RESISTANCE", 0.4)
    print("groups:", [[(z.timeframe, center(z)) for z in grp] for grp in g], "tols:", tols)
    print("   direct test of the two daily zones alone:", merge({"day": d}, "RESISTANCE", 0.4)[1])

    print("== 7 bucket map at committed weights (T=summed touches, ntf, vol, prior, round, r)")
    high_1tf = False
    rows = []
    for T, ntf, vol, prior, rnd, r in product(range(1, 7), (1, 2, 3), (0, 1), (0, 1), (0, 1), (0.0, 0.5, 1.0)):
        if T < ntf:
            continue   # each zone has at least one touch, so a k-TF group has T >= k
        sc, dt, b = score_shape(T, ntf, vol, prior, rnd, r)
        assert dt >= 2, "distinct types below 2"
        if ntf == 3:
            assert b == "HIGH", (T, ntf, vol, prior, rnd, r)
        if ntf == 1 and b == "HIGH":
            high_1tf = True
        if ntf == 2 and not (vol or prior or rnd) and r == 0.0:
            rows.append((T, sc, b))
    print("every 3-TF shape HIGH: yes; any 1-TF shape HIGH:", high_1tf)
    print("2-TF shapes with no external vote and no recency (T, score, bucket):", rows)
    print("2-TF, T=2, round and r=1.0:", score_shape(2, 2, 0, 0, 1, 1.0))
    print("2-TF, T=2, round and r=0.99:", score_shape(2, 2, 0, 0, 1, 0.99))
    print("1-TF lone pivot: none", score_shape(1, 1, 0, 0, 0, 0.0), "round", score_shape(1, 1, 0, 0, 1, 0.0),
          "round+r1", score_shape(1, 1, 0, 0, 1, 1.0), "vol", score_shape(1, 1, 1, 0, 0, 0.0))
    print("1-TF T=2:", score_shape(2, 1, 0, 0, 0, 0.0), "max 1-TF:", score_shape(6, 1, 1, 1, 1, 1.0))
    print("zero-weight volume vote counted:", score_shape(1, 1, 1, 0, 0, 0.0, w=(1.0, 0.0, 1.0, 1.0, 0.5, 0.5)))

    print("== 8 round-number rule")
    for c in (9.99, 10.01, 99.9, 100.1, 523.0, 990.0, 1001.0, 2500.0):
        print("   centre", c, "step", step_of(c), "step/price %.1f%%" % (100 * step_of(c) / c))
    for lo, hi in ((498, 502), (520, 521), (100.0, 100.0), (100.0, 100.2), (100.0, 100.5), (519.8, 520.2),
                   (101.0, 103.0), (97.0, 99.0), (98.0, 100.5), (100.0001, 100.0001)):
        print("   band", lo, hi, "->", has_round(lo, hi))

    print("== 9 test-band scores (lone 100.0, four touches 100.0-100.2, prior-day 100.0-100.5)")
    print("   lone:", score_shape(1, 1, 0, 0, has_round(100.0, 100.0), 0.0))
    print("   four touches:", score_shape(4, 1, 0, 0, has_round(100.0, 100.2), 0.0))
    print("   prior-day:", score_shape(2, 1, 0, 1, has_round(100.0, 100.5), 0.0))
    print("   HIGH test merged band 519.8-520.2:", score_shape(8, 2, 0, 0, has_round(519.8, 520.2), 0.0))

    print("== 10 recency")
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime(2026, 6, 8, 15, 30, tzinfo=ist)
    print("   7 days:", recency(now - timedelta(days=7), now), 0.5 * recency(now - timedelta(days=7), now))
    print("   now None:", recency(now - timedelta(days=80), None))
    print("   naive 15:30 vs aware label 10:00 same day:", recency(datetime(2026, 6, 8, 10, 0, tzinfo=ist),
                                                             datetime(2026, 6, 8, 15, 30)))
    print("   window 0:", recency(now - timedelta(days=80), now, window=0.0))
    print("   min factor 1.5:", recency(now - timedelta(days=1), now, min_f=1.5))
    print("   future touch (clamped):", recency(now + timedelta(hours=3), now))
    # rounding vs bucket boundary: smallest age that keeps 0.5*r >= 0.49995
    age_max_days = (1 - 0.49995 / 0.5) * 90.0
    print("   0.5*r within 0.00005 of 0.5 needs age <= %.5f days = %.1f minutes" % (age_max_days, age_max_days * 1440))
    for label, hours in (("30minute, 5 bars", 2.5), ("60minute, 5 bars", 5.0), ("5minute, 5 bars", 25 / 60.0)):
        r = recency(now - timedelta(hours=hours), now)
        print("   newest possible touch,", label, "-> r", round(r, 6), "contribution", round(0.5 * r, 6))
    s = 2 + 2 + 0.5 + 0.5 * 0.99992
    print("   example score 4.99996: bucket", bucket(s, 5, 2), "to_dict round ->", round(s, 4))

    print("== 11 semantics (plain expressions)")
    for expr in ("int(float('nan'))", "int(float('inf'))", "float(None)", "float('abc')", "int('12.5')",
                 "int('' or 0)", "int(None or 0)", "int(-3.7)", "math.floor(math.log10(float('nan')))",
                 "math.floor(math.log10(float('inf')))", "float('nan') <= 0", "max([float('nan'), 1.0])",
                 "max([1.0, float('nan')])", "round(2.675, 2)", "round(4.99996, 4)"):
        try:
            print("  ", expr, "->", repr(eval(expr)))
        except Exception as exc:
            print("  ", expr, "-> raises", type(exc).__name__)
    aw = datetime(2026, 6, 1, 9, 15, tzinfo=ist)
    nv = datetime(2026, 6, 1, 9, 15)
    for f, lab in ((lambda: max([aw, nv]), "max(aware, naive)"), (lambda: aw - nv, "aware - naive")):
        try:
            f()
            print("  ", lab, "-> no error")
        except Exception as exc:
            print("  ", lab, "-> raises", type(exc).__name__)


if __name__ == "__main__":
    main()
