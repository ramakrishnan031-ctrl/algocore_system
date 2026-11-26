# P06 checker coverage test (reads the part and git show text; nothing from legacy code is imported or run).
import re, subprocess
G = ["git", "-C", "/home/claude/repos/legacy"]
part = open("/home/claude/a08/parts/A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md", encoding="utf-8").read()
def show(p): return subprocess.run(G + ["show", "970aabf:" + p], capture_output=True, text=True, check=True).stdout.split("\n")
# 1. fields: one table row each
L = show("core/config_loader.py")
fields = [re.match(r"^    ([a-z_0-9]+):", l).group(1) for l in L[1162:1223] if re.match(r"^    [a-z_0-9]+:", l)]
miss = [f for f in fields + ["structure_exit_enabled"] if not re.search(r"^\| P06-S\d{3} \| `" + f + r"`", part, re.M)]
print(f"1. fields: {len(fields)} + structure_exit_enabled; rows missing: {miss or 'none'}")
# 2. main.py A08 lines: cited directly or inside a cited range anywhere in the part (main.py citations)
M = show("main.py")
pat = re.compile(r"sr_detector|_sr_cfg|_v1_on|_v2_on|_struct_exit|zone_warmer|retest_monitor|_retest_diverter|_v2_zone_cache|OhlcFetcher|ohlc_fetchers|_sr_fetch_fn|_md_kite|_onem_fetcher|_retest_params|_structure_fetcher|_v2_knobs|_v2_scoring|_wl_knobs|_wl_scoring|_wl_fetcher|_regime_fetcher|_v3_fetcher|build_zone_knobs|build_scoring_params|_build_market_data_kite|_make_sr_fetch_fn|StructureExitManager|structure_exit_manager|RetestParams|RetestDiverter|RetestMonitor|ZoneCache|ZoneWarmer|_a4\b")
lines = [i + 1 for i, l in enumerate(M) if pat.search(l) and not l.strip().startswith("#")]
cited = set()
for a, b in re.findall(r"L(\d{3,4})(?: to L(\d{3,4}))?", part):
    a = int(a); b = int(b) if b else a
    if b - a < 600: cited.update(range(a, b + 1))
unc = [n for n in lines if n not in cited]
print(f"2. main.py lines with an A08 name (code lines): {len(lines)}; not inside any cited line or range: {unc or 'none'}")
for n in unc: print(f"   L{n}: {M[n-1].strip()[:110]}")
# 3. branch conditions of the wiring and the shutdown
br = [i + 1 for i, l in enumerate(M) if (2085 <= i + 1 <= 2192 or 3417 <= i + 1 <= 3840 or 1599 <= i + 1 <= 1831 or 3860 <= i + 1 <= 3975)
      and re.match(r"\s*(if |elif |else:|try:|except |return |finally:)", l)]
ub = [n for n in br if n not in cited]
print(f"3. branch/try/return lines in main L2085-L2192, L1599-L1831, L3417-L3840, L3860-L3975: {len(br)}; not cited: {len(ub)}")
for n in ub: print(f"   L{n}: {M[n-1].strip()[:110]}")
# 4. consumer files: each named in section 7
sec7 = part[part.index("## 7. Consolidated"):part.index("## 8. Inventory")]
cons = ["signals/signal_processor.py","orders/structure_exit_manager.py","orders/eod_squareoff.py","orders/order_placer.py","orders/full_entry_engine.py",
        "orders/order_protocol_limit.py","orders/order_protocol_co.py","regime/engine.py","v3_chain/runner.py","v3_chain/pb01_runner.py",
        "v3_chain/watchlist_capture.py","v3_chain/pb01_entry.py","v3_chain/truncate.py","screening/hard_gate.py","reports/daily_trade_review.py",
        "core/candle_math.py","core/daily_stats.py","scripts/forward_shadow_record.py","core/state_store.py","core/schema.sql","core/migrations.py",
        "scripts/eod_cleanup.py","reports/signal_status.py","ops_dashboard/backend/readers/db_reader.py","config/expected_managers.yaml",
        "core/effect_telemetry.py","core/evidence_contract.py","core/evidence_artefact_manifest.txt","core/config_auditor.py",
        "ops_dashboard/backend/services/audit.py","config_view.py","system_logs.py","config/cron_registry.yaml","deploy/cron/trading-system.cron",
        "utils/cron_heartbeat.py","utils/holiday_guard.py","scripts/check_cron_drift.py","core/time_authority.py"]
print("4. consumer files not named in section 7:", [c for c in cons if c not in sec7] or "none")
# 2b/3b. stricter: only citations that are main.py's (sections 4 to 6, whose lines are all main.py's, and explicit "`main.py` L..." runs elsewhere)
s46 = part[part.index("## 4. `main.py` wiring"):part.index("## 7. Consolidated")]
strict = set()
def add(txt):
    for a, b in re.findall(r"L(\d{3,4})(?: to L(\d{3,4}))?", txt):
        a = int(a); b = int(b) if b else a
        if b - a < 600: strict.update(range(a, b + 1))
add(s46)
for m in re.finditer(r"`main\.py`[^.;|]*", part):
    add(m.group(0))
unc2 = [n for n in lines if n not in strict]
print(f"2b. strict: A08-named main.py code lines not in a main.py citation: {unc2 or 'none'}")
for n in unc2: print(f"   L{n}: {M[n-1].strip()[:110]}")
br2 = [n for n in br if 1599 <= n <= 1831 or 3417 <= n <= 3840]
ub2 = [n for n in br2 if n not in strict]
print(f"3b. strict: branch/try/return lines in _shutdown and the S&R wiring region: {len(br2)}; not in a main.py citation: {ub2 or 'none'}")
for n in ub2: print(f"   L{n}: {M[n-1].strip()[:110]}")
