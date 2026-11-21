"""P08 checker helper (read-only, independent of the writer's script).
For each of the 16 strategy files at the baseline: parse the YAML text from
`git show 970aabf:<path>` with yaml.safe_load (data only), and print, per field,
the value distribution, the files where the field is absent, and per-value file lists.
Imports and runs no legacy code; writes no file.
Run: python3 -I -B /home/claude/a07/check/p08chk_strat.py
"""
import collections
import subprocess
import yaml

REPO = "/home/claude/repos/legacy"
BASE = "970aabf"
A07_READ = ["intent", "enabled", "direction", "name", "min_score", "min_volume_surge",
            "min_adr_pct", "max_spread_pct", "pipeline", "horizon", "v3_playbook",
            "entry_start_time", "entry_end_time", "sl_pct", "tgt_risk_reward"]
OTHER = ["order_protocol", "pullback_wait_enabled", "pullback_wait_tolerance_pct",
         "pullback_wait_timeout_sec", "active_days", "sl_method"]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True,
                          capture_output=True, text=True).stdout


def main():
    paths = [p for p in git("ls-tree", "--name-only", BASE, "config/strategies/").split()
             if p.endswith(".yaml")]
    print("files:", len(paths))
    data = {}
    lines = {}
    for p in paths:
        t = git("show", f"{BASE}:{p}")
        data[p.split("/")[-1][:-5]] = yaml.safe_load(t)
        lines[p.split("/")[-1][:-5]] = t.splitlines()
    for f in A07_READ + OTHER:
        absent = [n for n, d in data.items() if f not in d]
        byval = collections.defaultdict(list)
        for n, d in data.items():
            if f in d:
                byval[repr(d[f])].append(n)
        tag = "A07-read" if f in A07_READ else "other"
        print(f"\n[{tag}] {f}: absent in {len(absent)} {absent if absent else ''}")
        for v, ns in sorted(byval.items(), key=lambda kv: -len(kv[1])):
            if len(byval) == 1 or f in ("min_volume_surge", "sl_pct", "horizon", "direction",
                                         "intent", "enabled", "order_protocol",
                                         "pullback_wait_enabled", "entry_end_time", "v3_playbook"):
                print(f"   {v}: {len(ns)} {sorted(ns)}")
            else:
                print(f"   {v}: {len(ns)}")
    # name equals stem?
    mism = [n for n, d in data.items() if d.get("name") != n]
    print("\nname != file stem:", mism)
    # pipeline == intent?
    pi = [n for n, d in data.items() if d.get("pipeline") != d.get("intent")]
    print("pipeline != intent:", pi)
    # SHORT + enabled
    se = sorted(n for n, d in data.items() if d.get("direction") == "SHORT" and d.get("enabled") is True)
    print("SHORT and enabled true:", len(se), se)
    # line numbers of specific fields in specific files
    for n, f in (("pb01_breakout_retest", "enabled"), ("pb01_breakout_retest", "v3_playbook"),
                 ("pb01_breakout_retest", "entry_end_time")):
        ln = [i + 1 for i, l in enumerate(lines[n]) if l.startswith(f + ":")]
        print(f"{n}.{f} at lines {ln}")


if __name__ == "__main__":
    main()
