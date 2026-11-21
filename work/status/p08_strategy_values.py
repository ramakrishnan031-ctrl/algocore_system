"""P08 helper (read-only): print, for each of the 16 strategy files at the baseline,
the line number and value of each strategy field that A07 code reads (and the fields the
P08 brief names). Reads `git show 970aabf:<path>` output only; parses YAML text with
yaml.safe_load (data only); imports and runs no legacy code; writes no file.
Run: python3 -I -B /home/claude/a07/status/p08_strategy_values.py
"""
import collections
import subprocess
import yaml

REPO = "/home/claude/repos/legacy"
BASE = "970aabf"
FIELDS = [
    "name", "direction", "intent", "enabled", "order_protocol", "pipeline", "horizon",
    "min_score", "min_volume_surge", "min_adr_pct", "max_spread_pct",
    "pullback_wait_enabled", "pullback_wait_tolerance_pct", "pullback_wait_timeout_sec",
    "entry_start_time", "entry_end_time", "sl_pct", "tgt_risk_reward", "v3_playbook",
]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True,
                          capture_output=True, text=True).stdout


def main():
    names = [p for p in git("ls-tree", "--name-only", BASE, "config/strategies/").split()
             if p.endswith(".yaml") and not p.endswith(".local.yaml")]
    dist = collections.defaultdict(collections.Counter)
    for path in names:
        text = git("show", f"{BASE}:{path}")
        data = yaml.safe_load(text)
        lines = text.splitlines()
        out = []
        for f in FIELDS:
            ln = next((i + 1 for i, l in enumerate(lines)
                       if l.startswith(f + ":")), None)
            val = data.get(f, "<absent>") if isinstance(data, dict) else "<not a mapping>"
            dist[f][repr(val)] += 1
            out.append(f"{f}={val!r}@L{ln}")
        top_keys = sorted(data.keys()) if isinstance(data, dict) else []
        print(path.split("/")[-1], "|", "; ".join(out), "| keys:", len(top_keys))
    print("\nDISTRIBUTION over", len(names), "files")
    for f in FIELDS:
        print(f, dict(dist[f]))


if __name__ == "__main__":
    main()
