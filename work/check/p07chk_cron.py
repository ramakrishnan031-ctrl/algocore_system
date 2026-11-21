"""P07 checker helper: list cron_registry.yaml job declarations between 15:00 and 23:59 and
the cron officer's own entry. Reads the YAML text from stdin (piped from
`git show 970aabf:config/cron_registry.yaml`); never imports or runs legacy code."""
import sys
import yaml

data = yaml.safe_load(sys.stdin.read())
jobs = data.get("jobs", data)
rows = []
for name, j in jobs.items():
    if not isinstance(j, dict):
        continue
    sched = str(j.get("schedule", ""))
    expr = str(j.get("cron_expression", ""))
    parts = expr.split()
    hh = mm = None
    if len(parts) == 5 and parts[0].isdigit() and parts[1].isdigit():
        mm, hh = int(parts[0]), int(parts[1])
    rows.append((hh if hh is not None else 99, mm if mm is not None else 99, name, sched,
                 expr, j.get("enabled"), j.get("market_day_only")))
for hh, mm, name, sched, expr, en, mdo in sorted(rows):
    if (hh == 15 and mm >= 30) or (hh == 16 and mm <= 30) or name in ("cron_officer_brief", "cron_officer_eod", "system_manager_eod", "gemini_premarket_brief") or "cron_officer" in name:
        print(f"{hh:02d}:{mm:02d} {name:32s} schedule={sched!r} expr={expr!r} enabled={en} market_day_only={mdo}")
