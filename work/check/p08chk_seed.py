"""P08 checker helper (read-only): compare the committed direction-registry seed
`config/strategy_direction_registry.yaml` with the `direction` field of the 16 strategy
files at the baseline. Parses `git show` text with yaml.safe_load; imports and runs no
legacy code; writes no file.
Run: python3 -I -B /home/claude/a07/check/p08chk_seed.py
"""
import collections
import subprocess
import yaml

REPO = "/home/claude/repos/legacy"
BASE = "970aabf"


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True,
                          capture_output=True, text=True).stdout


def main():
    seed = yaml.safe_load(git("show", f"{BASE}:config/strategy_direction_registry.yaml"))
    rows = seed.get("strategies", {})
    print("seed top-level keys:", sorted(seed))
    print("seed rows:", len(rows))
    print("registration_status:", dict(collections.Counter(r.get("registration_status") for r in rows.values())))
    print("health:", dict(collections.Counter(r.get("health") for r in rows.values())))
    print("row keys:", sorted({k for r in rows.values() for k in r}))
    files = [p for p in git("ls-tree", "--name-only", BASE, "config/strategies/").split()
             if p.endswith(".yaml")]
    decl = {}
    for p in files:
        d = yaml.safe_load(git("show", f"{BASE}:{p}"))
        decl[d["name"]] = d["direction"]
    print("names equal:", set(decl) == set(rows))
    print("direction mismatches:", sorted(n for n in decl if rows.get(n, {}).get("direction") != decl[n]))
    print("source_yaml mismatches:", sorted(n for n, r in rows.items()
                                            if r.get("evidence", {}).get("source_yaml") != f"config/strategies/{n}.yaml"))
    print("first_seen values:", dict(collections.Counter(r.get("first_seen") for r in rows.values())))
    print("last change:", git("log", "-1", "--format=%H %ad", "--date=short", BASE, "--",
                              "config/strategy_direction_registry.yaml").strip())


if __name__ == "__main__":
    main()
