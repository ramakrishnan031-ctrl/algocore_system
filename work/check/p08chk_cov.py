"""P08 checker coverage script (read-only; reads the P08 part file, the focused questions
file and the peer part files under /home/claude/a07/; writes no file; no legacy code).
Run: python3 -I -B /home/claude/a07/check/p08chk_cov.py
Checks: (1) numbering and labels; (2) every configuration key, strategy field, path,
option and environment input read by A07 code (the checker's inventory, P08-S075) has a
statement, with the statement IDs listed; (3) Q9's full wording is quoted and answered;
(4) the nine inherited items of P08's row of P01-S074 and A02 AUDIT L1320 are
cross-referenced; (5) every cited peer statement ID (P02 to P07, ranges expanded) exists.
"""
import re
from pathlib import Path

PARTS = Path("/home/claude/a07/parts")
P08 = PARTS / "A07_CONFIGURATION_KEYS_AND_EFFECTIVE_VALUES_2026-11-21.md"
FQ = Path("/home/claude/a07/briefs/A07_FOCUSED_QUESTIONS.md")
PEERS = {
    "P02": "A07_STRATEGY_CONTROL_TAXONOMY_AND_DIRECTION_REGISTRY_2026-11-21.md",
    "P03": "A07_SECONDARY_SCREENER_ORCHESTRATION_AND_RESULT_2026-11-21.md",
    "P04": "A07_STEP_EXECUTOR_AND_THE_TEN_STEPS_2026-11-21.md",
    "P05": "A07_QUALITY_SCORER_HARD_GATE_AND_V3_PLAYBOOK_GATES_2026-11-21.md",
    "P06": "A07_ENTRY_GATE_AND_RESUME_CONTRACT_2026-11-21.md",
    "P07": "A07_STRATEGY_SCRIPTS_2026-11-21.md",
}
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")

# (token searched in statement text, description). Tokens are matched literally.
KEYS = [
    # system_config.yaml / SystemConfig
    ("`trade_type`", "system trade_type"), ("`force_intraday_only`", "system force_intraday_only"),
    ("`delivery_enabled`", "system delivery_enabled (brief; no A07 reader)"),
    ("`mis_filter.enabled`", "mis_filter.enabled"), ("`mis_filter.shadow`", "mis_filter.shadow"),
    ("`mis_filter.ttl_days`", "mis_filter.ttl_days"), ("`product_map`", "product_map"),
    ("`entry_gate.circuit_proximity_reject_enabled`", "entry_gate.circuit_proximity_reject_enabled"),
    ("`slippage_buffer`", "entry_gate.slippage_buffer (no A07 reader)"),
    ("`max_entry_slippage_pct`", "entry_gate.max_entry_slippage_pct (no A07 reader)"),
    ("`entry_gate.max_spread_pct`", "entry_gate.max_spread_pct (no reader by name)"),
    ("`min_depth_qty`", "entry_gate.min_depth_qty (no reader by name)"),
    ("`liquidity_check_enabled`", "entry_gate.liquidity_check_enabled (no reader by name)"),
    ("`min_effective_rr`", "entry_gate.min_effective_rr (no A07 reader)"),
    ("`min_pending_rr`", "entry_gate.min_pending_rr (no A07 reader)"),
    ("`slippage_control`", "entry_gate.slippage_control (no A07 reader)"),
    ("`trading_hours.market_open`", "trading_hours.market_open"), ("`special_sessions`", "special_sessions"),
    ("`v3_chain", "v3_chain keys (no A07 reader; gate keys via A18)"),
    ("`rr_floor`", "v3_chain.rr_floor (gate argument)"),
    ("`hold_buffer_atr_mult`", "v3_chain.hold_buffer_atr_mult (gate argument)"),
    # scoring_weights.yaml / ScoringConfig
    ("`steps.", "scoring.steps.* weights"), ("`min_pass_score`", "scoring.min_pass_score"),
    ("`high_score_threshold`", "scoring.high_score_threshold"),
    ("`medium_score_threshold`", "scoring.medium_score_threshold"),
    ("`v3_hardgate_mode`", "scoring.v3_hardgate_mode"), ("`v3_gate_steps`", "scoring.v3_gate_steps"),
    ("`v3_freshness_max_sec`", "scoring.v3_freshness_max_sec"),
    ("`v3_min_pass_score`", "scoring.v3_min_pass_score"),
    ("`v3_high_score_threshold`", "scoring.v3_high_score_threshold"),
    ("`v3_medium_score_threshold`", "scoring.v3_medium_score_threshold"),
    ("model_fields", "scoring steps' field names (scorer constructor)"),
    # strategy fields
    ("`intent`", "strategy intent"), ("`enabled`", "strategy enabled"), ("`direction`", "strategy direction"),
    ("`name`", "strategy name"), ("`min_score`", "strategy min_score"),
    ("`min_volume_surge`", "strategy min_volume_surge"), ("`min_adr_pct`", "strategy min_adr_pct"),
    ("`max_spread_pct`", "strategy max_spread_pct"), ("`pipeline`", "strategy pipeline"),
    ("`horizon`", "strategy horizon"), ("`v3_playbook`", "strategy v3_playbook"),
    ("`entry_start_time`", "strategy entry_start_time"), ("`entry_end_time`", "strategy entry_end_time"),
    ("`sl_pct`", "strategy sl_pct"), ("`tgt_risk_reward`", "strategy tgt_risk_reward"),
    ("`pullback_wait_enabled`", "strategy pullback_wait_enabled (brief; A06 reader only)"),
    ("`pullback_wait_tolerance_pct`", "strategy pullback_wait_tolerance_pct (brief; no reader)"),
    ("`pullback_wait_timeout_sec`", "strategy pullback_wait_timeout_sec (brief; no reader)"),
    ("`order_protocol`", "strategy order_protocol (brief; no A07 reader)"),
    ("`active_days`", "strategy active_days (no A07 reader)"),
    # paths, registry, options, environment, constructor values
    ("`config_dir`", "config_dir parameters"), ("`DEFAULT_SEED_PATH`", "registry seed path constant"),
    ("`DEFAULT_STATE_PATH`", "registry state path constant"),
    ("`DEFAULT_REGISTRY_PATH`", "registry alias constant"),
    ("config/strategy_direction_registry.yaml", "registry seed file"),
    ("`--config`", "metrics --config"), ("`--db`", "metrics --db"), ("`--date`", "metrics --date"),
    ("`--lookback`", "metrics --lookback"), ("`--dry-run`", "scripts --dry-run"),
    ("`--config-dir`", "officer/cron --config-dir"), ("`--db-path`", "officer --db-path"),
    ("`--registry`", "officer --registry"), ("`TRADING_MODE`", "env TRADING_MODE"),
    ("`load_dotenv", "officer load_dotenv(.env)"), ("`primary_account_tag`", "officer account tag (accounts file named only)"),
    ("`step_timeout_sec`", "executor step timeout (no key)"), ("`poll_interval_sec`", "gate poll interval (no key)"),
    ("`worker_count`", "gate worker count (no key)"), ("market_windows.market_open", "executor market_open argument"),
]
INHERITED = [("A01 C11", "L810"), ("A02 V-06", "L693"), ("A02 T-14", "L1156"), ("A02 T-20", "L1240"),
             ("A02 F-11", "L1521"), ("A02 K-05", "L1876"), ("A02 K-27", "L2184"),
             ("A04 OA-22", "L2367"), ("A04 CG-05", "L4784")]


def statements(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^- (P08-(?:S\d{3}|AP\d{2}|U\d{2}|R\d))\b", line)
        if m:
            cur = m.group(1)
            out[cur] = line
        elif line.startswith("#"):
            cur = None
        elif cur and (line.startswith("|") or line.startswith("  ")):
            out[cur] += "\n" + line
    return out


def peer_ids(text):
    ids = set(re.findall(r"P0[2-7]-(?:S\d{3}|AP\d+|U\d+)", text))
    for a, b in re.findall(r"(P0[2-7]-S\d{3}) to (P0[2-7]-S\d{3})", text):
        if a[:3] == b[:3]:
            ids |= {f"{a[:3]}-S{n:03d}" for n in range(int(a[-3:]), int(b[-3:]) + 1)}
    return ids


def main():
    text = P08.read_text(encoding="utf-8")
    body = text.split("\n## Check log")[0]
    st = statements(body)
    # (1) numbering and labels
    s_nums = sorted(int(k[5:]) for k in st if k.startswith("P08-S"))
    ap = sorted(int(k[6:]) for k in st if k.startswith("P08-AP"))
    u = sorted(int(k[5:]) for k in st if k.startswith("P08-U"))
    r = sorted(int(k[5:]) for k in st if k.startswith("P08-R"))
    print("(1) statements S:", len(s_nums), "range", s_nums[0], "-", s_nums[-1],
          "gaps:", sorted(set(range(1, s_nums[-1] + 1)) - set(s_nums)))
    print("    AP:", len(ap), "gaps:", sorted(set(range(1, ap[-1] + 1)) - set(ap)),
          "| U:", len(u), "| R:", len(r))
    dup = [k for k in st if body.count(f"- {k} ") + body.count(f"- {k}\n") > 1]
    print("    duplicate statement starts:", dup)
    bad = []
    for k, v in st.items():
        if k.startswith("P08-S"):
            rest = v.split(k, 1)[1].lstrip()
            if not rest.startswith(LABELS):
                bad.append(k)
    print("    S statements without a leading label:", bad)
    added = sorted(k for k, v in st.items() if "added in the check" in v.split("\n")[0][:140])
    print("    statements marked 'added in the check' at their head:", added)
    # (2) key coverage
    print("\n(2) key coverage (token -> statement IDs)")
    missing = []
    for tok, desc in KEYS:
        ids = sorted(k for k, v in st.items() if tok in v and k.startswith("P08-S"))
        if not ids:
            missing.append(desc)
        print(f"    {'PASS' if ids else 'FAIL'} {desc}: {', '.join(ids[:12])}{' ...' if len(ids) > 12 else ''}")
    print("    keys without a statement:", missing)
    # (3) Q9
    fq = FQ.read_text(encoding="utf-8")
    q9 = re.search(r"^9\. (.+)$", fq, re.M).group(1).strip()
    s073 = st.get("P08-S073", "")
    print("\n(3) Q9 full wording quoted in P08-S073:", q9 in s073,
          "| answer parts (1)-(5) present:", all(f"({i})" in s073 for i in range(1, 6)))
    # (4) inherited items
    print("\n(4) inherited items (section 10) and ADDENDUM 2")
    sec10 = body.split("## 10.")[1].split("## 11.")[0]
    st10 = statements("## x\n" + sec10)
    for item, line in INHERITED:
        ids = [k for k, v in st10.items() if v.split("(", 1)[-1].startswith(item) and line in v]
        print(f"    {'PASS' if ids else 'FAIL'} {item} ({line}): {ids}")
    print("    A02 AUDIT L1320 cited in:", sorted(k for k, v in st.items() if "L1320" in v))
    # (5) peer IDs
    print("\n(5) cited peer statement IDs")
    ids = peer_ids(body)
    for p, f in PEERS.items():
        ptext = (PARTS / f).read_text(encoding="utf-8")
        have = set(re.findall(r"^\s*-\s*\**(P0[2-7]-(?:S\d{3}|AP\d+|U\d+))", ptext, re.M))
        mine = sorted(i for i in ids if i.startswith(p))
        miss = [i for i in mine if i not in have]
        print(f"    {p}: {len(mine)} cited; missing in {p}'s file: {miss}")


if __name__ == "__main__":
    main()
