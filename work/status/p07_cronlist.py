import sys, re, yaml
data = yaml.safe_load(sys.stdin.read())
jobs = data.get("jobs", data)
def walk(d):
    for k, v in d.items():
        if isinstance(v, dict) and "schedule" in v:
            yield k, v
        elif isinstance(v, dict):
            yield from walk(v)
for name, j in walk(jobs):
    s = str(j.get("schedule", ""))
    m = re.match(r"(\d{1,2}):(\d{2})", s)
    if m and 15 <= int(m.group(1)) <= 18:
        print(f"{s:20s} {name:32s} enabled={j.get('enabled')} market_day_only={j.get('market_day_only')}")
