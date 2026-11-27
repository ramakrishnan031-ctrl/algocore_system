"""CZ checker (helper A7) — independent re-statement of the expressions read at 970aabf in
sr_detector/pivots.py L37-L55, zones.py L43-L116, confluence.py L80-L211 and models.py L36-L43,
written afresh by the checker (not copied from the writer's script). Imports nothing from the
legacy clone; standard library only. Working material (D-17), not a record.
"""
import math
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


class Bar:
    def __init__(self, ts, high, low, volume=1):
        self.ts, self.high, self.low, self.volume = ts, high, low, volume


class Pv:
    def __init__(self, price, ts, kind, i):
        self.price, self.ts, self.kind, self.i = price, ts, kind, i


class Zn:
    def __init__(self, lo, hi, kind, touches, tf, last=None):
        self.band_low, self.band_high, self.kind, self.touches, self.timeframe, self.last_touch_ts = lo, hi, kind, touches, tf, last

    @property
    def center(self):
        return (self.band_low + self.band_high) / 2.0


def pivots(c, left, right):  # pivots.py L37-L55
    n = len(c)
    out = []
    if left < 1 or right < 1 or n < left + right + 1:
        return out
    for i in range(left, n - right):
        x = c[i]
        win = c[i - left:i + right + 1]
        oth = [w for j, w in enumerate(win) if (i - left + j) != i]
        if all(x.high >= w.high for w in win) and any(x.high > w.high for w in oth):
            out.append(Pv(x.high, x.ts, "HIGH", i))
        if all(x.low <= w.low for w in win) and any(x.low < w.low for w in oth):
            out.append(Pv(x.low, x.ts, "LOW", i))
    return out


def clusters(pv, cluster_pct, tf):  # zones.py L43-L75
    zs = []
    for k, zk in (("HIGH", "RESISTANCE"), ("LOW", "SUPPORT")):
        s = sorted((p for p in pv if p.kind == k), key=lambda p: p.price)
        if not s:
            continue
        cl = [s[0]]
        for p in s[1:]:
            bh = max(q.price for q in cl)
            if p.price <= bh + bh * (cluster_pct / 100.0):
                cl.append(p)
            else:
                zs.append(Zn(min(q.price for q in cl), max(q.price for q in cl), zk, len(cl), tf,
                             max((q.ts for q in cl), default=None)))
                cl = [p]
        zs.append(Zn(min(q.price for q in cl), max(q.price for q in cl), zk, len(cl), tf,
                     max((q.ts for q in cl), default=None)))
    return zs


def vprofile(c, bins=24, node_frac=0.7):  # zones.py L91-L116
    if not c or bins < 1:
        return []
    lo = min(x.low for x in c)
    hi = max(x.high for x in c)
    if hi <= lo:
        return []
    width = (hi - lo) / bins
    b = [0.0] * bins
    for x in c:
        mid = (x.high + x.low) / 2.0
        idx = int((mid - lo) / width)
        idx = min(idx, bins - 1)
        idx = max(idx, 0)
        b[idx] += float(x.volume)
    peak = max(b)
    if peak <= 0:
        return []
    return [lo + (i + 0.5) * width for i, v in enumerate(b) if v >= node_frac * peak]


def merge(zbt, kind, merge_pct):  # confluence.py L84-L101
    flat = []
    for zl in zbt.values():
        flat.extend(z for z in zl if z.kind == kind)
    flat.sort(key=lambda z: z.center)
    groups, trace = [], []
    for z in flat:
        if not groups:
            groups.append([z])
            continue
        cur = groups[-1]
        cc = sum(x.center for x in cur) / len(cur)
        tol = cc * (merge_pct / 100.0)
        trace.append((z.timeframe, round(z.center, 4), round(cc, 4), round(tol, 4), round(abs(z.center - cc), 4)))
        if abs(z.center - cc) <= tol:
            cur.append(z)
        else:
            groups.append([z])
    return groups, trace


def in_band(levels, lo, hi, buf):  # confluence.py L170-L177
    if not levels:
        return False
    pad = ((lo + hi) / 2.0) * (buf / 100.0)
    return any((lo - pad) <= v <= (hi + pad) for v in levels)


def rnd(lo, hi):  # confluence.py L180-L192
    c = (lo + hi) / 2.0
    if c <= 0:
        return False
    m = 10.0 ** math.floor(math.log10(c))
    for st in (m, m / 2.0):
        if st <= 0:
            continue
        k = math.ceil(lo / st - 1e-9)
        if k * st <= hi + 1e-9:
            return True
    return False


def recf(last, now, window=90.0, minf=0.0):  # confluence.py L195-L211
    if last is None:
        return 0.0
    if now is None:
        return 1.0
    if (now.tzinfo is None) != (last.tzinfo is None):
        now = now.replace(tzinfo=None)
        last = last.replace(tzinfo=None)
    age = (now - last).total_seconds() / 86400.0
    if window <= 0:
        return 1.0
    return max(minf, min(1.0, 1.0 - age / window))


W = dict(w_swing=1.0, w_volume=1.0, w_multi_tf=1.0, w_prior_day=1.0, w_round=0.5, w_recency=0.5,
         t_high=5.0, t_med=3.0, touch_cap=4, band_buffer_pct=0.1, recency_min_factor=0.0)


def score_group(g, vnodes=(), prior=(), now=None, window=90.0, p=W):  # confluence.py L107-L167
    lo = min(z.band_low for z in g)
    hi = max(z.band_high for z in g)
    tfs = tuple(sorted({z.timeframe for z in g}))
    tt = sum(z.touches for z in g)
    last = max((z.last_touch_ts for z in g if z.last_touch_ts is not None), default=None)
    ev = []
    s = p["w_swing"] * min(tt, p["touch_cap"])
    if s > 0:
        ev.append(("swing_pivots", s))
    m = p["w_multi_tf"] * len(tfs)
    if m > 0:
        ev.append(("multi_tf", m))
    if in_band(vnodes, lo, hi, p["band_buffer_pct"]):
        ev.append(("volume_node", p["w_volume"]))
    if in_band(prior, lo, hi, p["band_buffer_pct"]):
        ev.append(("prior_day_level", p["w_prior_day"]))
    if rnd(lo, hi):
        ev.append(("round_number", p["w_round"]))
    r = recf(last, now, window, p["recency_min_factor"])
    if r > 0 and p["w_recency"] > 0:
        ev.append(("recency", p["w_recency"] * r))
    sc = sum(c for _, c in ev)
    dt = len(ev)
    if sc >= p["t_high"] and dt >= 2 and len(tfs) >= 2:
        b = "HIGH"
    elif sc >= p["t_med"]:
        b = "MEDIUM"
    else:
        b = "LOW"
    return sc, dt, b, [e[0] for e in ev]


def sh(T, ntf, vol=False, prior=False, rn=False, r=0.0):
    """score of an abstract group shape at the committed weights (confluence.py L119-L167)."""
    ev = [min(T, 4) * 1.0, ntf * 1.0]
    if vol:
        ev.append(1.0)
    if prior:
        ev.append(1.0)
    if rn:
        ev.append(0.5)
    if r > 0:
        ev.append(0.5 * r)
    sc = sum(ev)
    b = "HIGH" if (sc >= 5.0 and len(ev) >= 2 and ntf >= 2) else ("MEDIUM" if sc >= 3.0 else "LOW")
    return round(sc, 6), len(ev), b


def run(label, f):
    try:
        print(label, "->", f())
    except Exception as e:
        print(label, "-> raises", type(e).__name__)


def main():
    t0 = datetime(2026, 6, 1, 9, 15)
    T = lambda i: t0 + timedelta(minutes=i)
    print("## CZ-01 bucket map (committed weights; T >= ntf)")
    all3 = all(sh(T_, 3, v, pr, rn, r)[2] == "HIGH" for T_ in range(3, 9) for v in (0, 1) for pr in (0, 1)
               for rn in (0, 1) for r in (0, 0.3, 1.0))
    any1 = any(sh(T_, 1, v, pr, rn, r)[2] == "HIGH" for T_ in range(1, 9) for v in (0, 1) for pr in (0, 1)
               for rn in (0, 1) for r in (0, 0.3, 1.0))
    print(" every 3-TF shape HIGH:", all3, "| any 1-TF HIGH:", any1, "| max 1-TF score:", sh(8, 1, 1, 1, 1, 1.0))
    print(" min 3-TF score:", sh(3, 3))
    print(" 2-TF T=2 nothing:", sh(2, 2), " T=3:", sh(3, 2), " T=2+vol:", sh(2, 2, vol=1), " T=2+prior:", sh(2, 2, prior=1))
    print(" 2-TF T=2 round r=1:", sh(2, 2, rn=1, r=1.0), " r=0.99:", sh(2, 2, rn=1, r=0.99))
    print(" distinct>=2 always (w>0, cap>=1):", all(sh(T_, n)[1] >= 2 for T_ in range(1, 9) for n in (1, 2, 3)))
    print(" unit-test HIGH case (day 520.0x5, 60m 519.8-520.2x3, empty ctx):",
          score_group([Zn(520.0, 520.0, "R", 5, "day"), Zn(519.8, 520.2, "R", 3, "60minute")], p=dict(W, band_buffer_pct=0.0)))

    print("## CZ-02 plateaus and outside bars")
    c = [Bar(T(i), h, 0.0) for i, h in enumerate([1, 2, 5, 5, 2, 1])]
    print(" [1,2,5,5,2,1] n=2 HIGH:", [(p.i, p.price) for p in pivots(c, 2, 2) if p.kind == "HIGH"])
    hs = [1, 2, 3, 4, 5, 6, 9, 9, 6, 5, 4, 3, 2, 1]
    c = [Bar(T(i), h, 0.0) for i, h in enumerate(hs)]
    pv = [p for p in pivots(c, 5, 5) if p.kind == "HIGH"]
    print(" two equal tops at 6,7 n=5:", [(p.i, p.price) for p in pv], "zones:", [(z.band_low, z.band_high, z.touches) for z in clusters(pv, 0.5, "day")])
    c = [Bar(T(i), 100, 99) for i in range(9)]
    print(" nine equal bars n=2:", pivots(c, 2, 2))
    c = [Bar(T(0), 10, 9), Bar(T(1), 10.5, 9.5), Bar(T(2), 12, 8), Bar(T(3), 10.4, 9.4), Bar(T(4), 10.2, 9.2)]
    print(" outside bar n=2:", [(p.i, p.kind, p.price) for p in pivots(c, 2, 2)])
    c = [Bar(T(i), 100, 99) for i in range(4)]
    print(" guard: 4 bars n=2 ->", pivots(c, 2, 2), "| left=0 ->", pivots([Bar(T(i), i, 0) for i in range(9)], 0, 2))
    # a flat top filling the whole window except one bar: 5 bars n=2, highs [9,9,9,9,8]?
    c = [Bar(T(i), h, 0.0) for i, h in enumerate([8, 9, 9, 9, 8])]
    print(" [8,9,9,9,8] n=2 HIGH:", [(p.i, p.price) for p in pivots(c, 2, 2) if p.kind == "HIGH"])
    c = [Bar(T(i), h, 0.0) for i, h in enumerate([9, 9, 9, 9, 9, 8])]
    print(" [9,9,9,9,9,8] n=2 HIGH:", [(p.i, p.price) for p in pivots(c, 2, 2) if p.kind == "HIGH"])

    print("## CZ-03 chaining and merge drift")
    pv = [Pv(100.0 + 0.4 * i, t0, "HIGH", i) for i in range(6)]
    z = clusters(pv, 0.5, "day")
    print(" chain 100.0..102.0 step 0.4:", [(round(q.band_low, 4), round(q.band_high, 4), q.touches) for q in z],
          "width % of low:", round(100 * (z[0].band_high - z[0].band_low) / z[0].band_low, 3))
    d = clusters([Pv(100.0, t0, "HIGH", 0), Pv(100.55, t0, "HIGH", 1)], 0.5, "day")
    h = clusters([Pv(100.35, t0, "HIGH", 0)], 0.5, "60minute")
    print(" daily zones:", [(q.band_low, q.band_high) for q in d])
    print(" daily alone merge trace:", merge({"day": d}, "RESISTANCE", 0.4)[1])
    g, tr = merge({"day": d, "60minute": h}, "RESISTANCE", 0.4)
    print(" with 60m 100.35: groups", [[(q.timeframe, q.center) for q in gg] for gg in g], "trace", tr)
    print(" group band:", (min(q.band_low for q in g[0]), max(q.band_high for q in g[0])))
    # bound: same-TF zones cannot join a group of only that TF's zones (positive prices)
    import random
    random.seed(7)
    bad = 0
    for _ in range(20000):
        base = random.uniform(1, 5000)
        prices = sorted(base * (1 + random.uniform(0, 0.08)) for _ in range(random.randint(2, 12)))
        zs = clusters([Pv(p, t0, "HIGH", i) for i, p in enumerate(prices)], 0.5, "day")
        gg, _ = merge({"day": zs}, "RESISTANCE", 0.4)
        if any(len(x) > 1 for x in gg):
            bad += 1
    print(" random same-TF-only groups with >1 zone (expect 0):", bad)

    print("## CZ-04 zero-width zones")
    print(" lone pivot 100.0:", score_group([Zn(100.0, 100.0, "R", 1, "day")]),
          "| lone 100.0001:", score_group([Zn(100.0001, 100.0001, "R", 1, "day")]))
    print(" lone 100.0 + now (full recency):", score_group([Zn(100.0, 100.0, "R", 1, "day", t0)], now=t0))
    print(" lone 101.3 + vol node 101.35:", score_group([Zn(101.3, 101.3, "R", 1, "day")], vnodes=(101.35,)))
    print(" lone 101.3 nothing:", score_group([Zn(101.3, 101.3, "R", 1, "day")]), "round(101.3)", rnd(101.3, 101.3))
    print(" lone 101.3 + now:", score_group([Zn(101.3, 101.3, "R", 1, "day", t0)], now=t0))

    print("## CZ-09 recency")
    now = datetime(2026, 6, 8, 15, 30, tzinfo=IST)
    print(" 7 days aware:", round(recf(now - timedelta(days=7), now), 4), round(0.5 * recf(now - timedelta(days=7), now), 4))
    print(" naive 15:30 vs aware 10:00 IST:", round(recf(datetime(2026, 6, 8, 10, 0, tzinfo=IST), datetime(2026, 6, 8, 15, 30)), 5))
    print(" now None:", recf(now - timedelta(days=89), None), "| window 0:", recf(now - timedelta(days=89), now, window=0.0),
          "| window -1:", recf(now - timedelta(days=89), now, window=-1.0))
    print(" future touch:", recf(now + timedelta(hours=2), now), "| minf 1.5:", recf(now - timedelta(days=1), now, minf=1.5))
    run(" aware IST vs aware UTC same instant", lambda: recf(datetime(2026, 6, 8, 10, 0, tzinfo=IST), datetime(2026, 6, 8, 4, 30, tzinfo=timezone.utc)))

    print("## CZ-10 prior-day test band unbuffered vs buffered")
    print(" level 100.2 in 100.0-100.5 buf 0:", in_band((100.2,), 100.0, 100.5, 0.0), "buf 0.1:", in_band((100.2,), 100.0, 100.5, 0.1))

    print("## CZ-11 zero / negative weights; minf > 1; bins")
    p0 = dict(W, w_volume=0.0)
    print(" lone pivot, zero-weight volume vote:", score_group([Zn(101.3, 101.3, "R", 1, "day")], vnodes=(101.3,), p=p0))
    pn = dict(W, w_volume=-1.0)
    print(" lone pivot, negative volume weight:", score_group([Zn(101.3, 101.3, "R", 1, "day")], vnodes=(101.3,), p=pn))
    print(" touch_cap 0:", score_group([Zn(101.3, 101.3, "R", 3, "day")], p=dict(W, touch_cap=0)))
    run(" bins 2.0", lambda: vprofile([Bar(T(0), 10, 9, 5), Bar(T(1), 11, 10, 5)], bins=2.0))
    print(" node_frac 0 nodes:", len(vprofile([Bar(T(0), 10, 9, 5), Bar(T(1), 11, 10, 5)], bins=4, node_frac=0.0)),
          "| node_frac 1.1:", vprofile([Bar(T(0), 10, 9, 5), Bar(T(1), 11, 10, 5)], bins=4, node_frac=1.1))
    print(" cluster_pct 0 joins equal only:", [(z.band_low, z.touches) for z in clusters([Pv(100, t0, "HIGH", 0), Pv(100, t0, "HIGH", 1), Pv(100.01, t0, "HIGH", 2)], 0.0, "d")])
    print(" cluster_pct -0.1 equal prices:", [(z.band_low, z.touches) for z in clusters([Pv(100, t0, "HIGH", 0), Pv(100, t0, "HIGH", 1)], -0.1, "d")])

    print("## CZ-14 (7) test band 100.0-100.2 four touches one TF, unbuffered, no now")
    print(" ", score_group([Zn(100.0, 100.2, "R", 4, "day")], p=dict(W, band_buffer_pct=0.0)))
    print(" prior-day test 100.0-100.5 two touches:", score_group([Zn(100.0, 100.5, "R", 2, "day")], prior=(100.2,), p=dict(W, band_buffer_pct=0.0)))
    print(" lone weak 100.0:", score_group([Zn(100.0, 100.0, "R", 1, "day")], p=dict(W, band_buffer_pct=0.0)))

    print("## CZ-19 round-number rule")
    for c_ in (9.99, 10.0, 99.9, 100.1, 523.0, 999.0, 1000.0, 1001.0, 9999.0):
        m = 10.0 ** math.floor(math.log10(c_))
        print("  centre", c_, "magnitude", m, "half", m / 2, "half/centre %.2f%%" % (100 * (m / 2) / c_))
    for lo, hi in ((498, 502), (520, 521), (100.0, 100.0), (100.0001, 100.0001), (519.8, 520.2), (100.0, 100.5)):
        print("  band", lo, hi, rnd(lo, hi))
    # does the magnitude step ever add a match beyond the half step (outside the 1e-9 allowance)?
    extra = 0
    import random
    random.seed(11)
    for _ in range(200000):
        lo = random.uniform(1, 20000)
        hi = lo + random.uniform(0, lo * 0.05)
        c_ = (lo + hi) / 2
        m = 10.0 ** math.floor(math.log10(c_))
        a = math.ceil(lo / m - 1e-9) * m <= hi + 1e-9
        b = math.ceil(lo / (m / 2) - 1e-9) * (m / 2) <= hi + 1e-9
        if a and not b:
            extra += 1
    print("  random bands where magnitude matches but half does not:", extra)

    print("## CZ-22 rounding vs threshold at committed weights")
    print("  r needed for 0.5r >= 0.49995:", 0.9999, "age <= minutes:", round(0.0001 * 90 * 1440, 2))
    for lab, mins in (("5minute x5", 25), ("30minute x5", 150), ("60minute x5", 300), ("day x5", 5 * 1440)):
        r = 1 - (mins / 1440) / 90
        print("  ", lab, "r=", round(r, 6), "0.5r=", round(0.5 * r, 6), "score 4.5+0.5r rounds to", round(4.5 + 0.5 * r, 4))

    print("## CZ-07 / CZ-08 semantics (plain expressions; no legacy code)")
    nan, inf = float("nan"), float("inf")
    run(" float(None)", lambda: float(None))
    run(" float('abc')", lambda: float("abc"))
    run(" float('nan')", lambda: float("nan"))
    run(" int(None or 0)", lambda: int(None or 0))
    run(" int(0.0 or 0)", lambda: int(0.0 or 0))
    run(" int('' or 0)", lambda: int("" or 0))
    run(" int(False or 0)", lambda: int(False or 0))
    run(" int(-3.7)", lambda: int(-3.7))
    run(" int(nan or 0)", lambda: int(nan or 0))
    run(" int(inf or 0)", lambda: int(inf or 0))
    c = [Bar(T(i), h, h - 1) for i, h in enumerate([10, 11, 12, 11, 10, 11, 12, 11, 10])]
    c[4] = Bar(T(4), nan, 9)
    print(" pivots with NaN high at 4 (n=2):", [(p.i, p.kind) for p in pivots(c, 2, 2)])
    c2 = [Bar(T(i), h, h - 1) for i, h in enumerate([10, 11, 12, 11, 10, 11, 12, 11, 10])]
    c2[6] = Bar(T(6), inf, 11)
    print(" pivots with +inf high at 6 (n=2):", [(p.i, p.kind, p.price) for p in pivots(c2, 2, 2)])
    run(" vprofile NaN high (not first)", lambda: vprofile(c))
    cc = [Bar(T(i), h, h - 1) for i, h in enumerate([10, 11, 12])]
    cc[0] = Bar(T(0), nan, 9)
    run(" vprofile NaN high first", lambda: vprofile(cc))
    run(" vprofile +inf high", lambda: vprofile(c2))
    c3 = [Bar(T(i), h, h - 1) for i, h in enumerate([10, 11, 12])]
    c3[1] = Bar(T(1), 11, -inf)
    run(" vprofile -inf low", lambda: vprofile(c3))
    c4 = [Bar(T(i), h, h - 1) for i, h in enumerate([10, 11, 12])]
    c4[1] = Bar(T(1), -inf, 10)
    run(" vprofile -inf high (inconsistent bar)", lambda: vprofile(c4))
    run(" rnd NaN centre", lambda: rnd(nan, nan))
    run(" rnd +inf centre", lambda: rnd(100.0, inf))
    run(" rnd -inf centre", lambda: rnd(-inf, 100.0))
    aw = datetime(2026, 6, 1, 9, 15, tzinfo=IST)
    nv = datetime(2026, 6, 1, 9, 20)
    run(" max(aware, naive) ts", lambda: max([aw, nv]))
    run(" clusters mixed ts", lambda: clusters([Pv(100, aw, "HIGH", 0), Pv(100.1, nv, "HIGH", 1)], 0.5, "d"))
    print(" in_band NaN level:", in_band((nan,), 99, 101, 0.1))


if __name__ == "__main__":
    main()
