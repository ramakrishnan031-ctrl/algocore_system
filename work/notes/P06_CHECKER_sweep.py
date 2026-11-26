# P06 checker: independent sweep of the seven approved AUDIT files (algocore, read-only) for records and table rows
# that touch A08 code, tables, switches or keys without naming A08. Names come from the 16 A08 files at 970aabf
# (git show text; nothing imported). Prints one line per record/row: topic, ID, kind, lines, hits.
import re, sys, glob, os, subprocess, json
ROOT = "/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION"
G = ["git", "-C", "/home/claude/repos/legacy"]
files16 = ["sr_detector/" + m for m in ["__init__.py","confluence.py","detector.py","fetch.py","flags.py","models.py","pivots.py","retest_confirm.py","zone_builder.py","zone_cache.py","zone_warmer.py","zones.py"]] + ["screening/retest_monitor.py","scripts/sr_corp_action_spotcheck.py","scripts/sr_detector_backfill.py","scripts/sr_level_export.py"]
top = set()
for m in files16:
    for ln in subprocess.run(G + ["show", "970aabf:" + m], capture_output=True, text=True).stdout.split("\n"):
        q = re.match(r"^(?:class|def) ([A-Za-z_][A-Za-z0-9_]*)", ln) or re.match(r"^([A-Z][A-Z0-9_]{3,})\s*[:=]", ln)
        if q: top.add(q.group(1))
# drop names that are common words or generic helpers shared with other files
generic = {"main","_attr","_SENTINEL","REJECT","CONFIRMED","evaluate","Zone","Candle","Pivot","_iso","_json","_row","_is_long",
           "backfill","ROOT","DB_PATH","COLUMNS","TOKEN_PATH","_bucket","_nearest","_cron_main","_build_kite","_is_terminal",
           "_win_loss","Candidate","IN_PROGRESS_STATES","WAIT_BREAKOUT","WAIT_RETEST","WAIT_CONFIRM","TF_ROLE","rows_to_csv"}
names = sorted(top - generic)
code = names + ["sr_detector", "retest_monitor", "sr_corp_action_spotcheck", "sr_detector_backfill", "sr_level_export",
        "sr_detector_results", "retest_state", "REJECTED_RETEST_DUP", "_sr_observe", "_warm_zones", "maybe_divert",
        "set_retest_diverter", "set_retest_monitor", "_make_sr_fetch_fn", "_build_market_data_kite", "fetch_timeframes",
        "fetch_interval", "fetch_by_token", "from_kite", r"`Candle`", r"Candle\.", "sr-detector", "sr-zone-warmer", "sr-retest-monitor"]
keys = ["wait_for_retest", "structure_exit_enabled", "intraday_anchors", "near_zone_buffer_pct", "require_confidence",
        "retest_timeout_sec", "retest_max_away_pct", "confirm_strong_close_frac", "breakout_margin_pct", "onem_lookback_days",
        "zone_cache_ttl_sec", "zone_rewarm_margin_sec", "retest_poll_interval_sec", "retest_sl_buffer_pct",
        "anchor_intraday_interval", "anchor_lookback_days", "orb_window_minutes", r"sr_detector\.enabled", "RETEST_"]
words = [r"S&R", r"support/resistance", r"support and resistance", r"\bSNR-", r"\bretest"]
pc = re.compile("|".join(re.escape(n) if not n.startswith(("`", "Candle\\.")) else n for n in code))
pk = re.compile("|".join(keys))
pw = re.compile("|".join(words), re.I)
head = re.compile(r"^#{3,6} ([A-Z]{1,3}-?\d+[a-z]?)(?: \([^)]*\))? — ")
row = re.compile(r"^\| *\**`?([A-Z]{1,3}-\d+[a-z]?|C\d+[a-z]?)`?\** *(?:\([^)]*\))? *\|")
out = []
for f in sorted(glob.glob(ROOT + "/A0[1-7]_*/A0[1-7]_AUDIT_*.md")):
    t = os.path.basename(f)[:3]
    L = open(f, encoding="utf-8").read().split("\n")
    for i, l in enumerate(L):
        m = head.match(l)
        if m:
            j = i + 1
            while j < len(L) and not L[j].startswith("#"): j += 1
            body = "\n".join(L[i:j]); kind = "REC"; span = f"L{i+1}-L{j}"
        else:
            m = row.match(l)
            if not m: continue
            body = l; kind = "ROW"; span = f"L{i+1}"
        if "A08" in body: continue
        hc = sorted(set(x.group(0) for x in pc.finditer(body)))
        hk = sorted(set(x.group(0) for x in pk.finditer(body)))
        hw = sorted(set(x.group(0).lower() for x in pw.finditer(body)))
        if hc or hk or hw:
            out.append({"t": t, "id": m.group(1), "kind": kind, "span": span, "code": hc, "keys": hk, "words": hw})
json.dump(out, open("/home/claude/a08/notes/P06_CHECKER_sweep_out.json", "w"), indent=0)
for o in out:
    print(f"{o['t']}\t{o['id']}\t{o['kind']}\t{o['span']}\tC={','.join(o['code'])}\tK={','.join(o['keys'])}\tW={','.join(o['words'])}")
