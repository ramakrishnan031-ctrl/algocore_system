import re, sys, pathlib, subprocess
try:
    COMMITS = set(h[:7] for h in subprocess.run(['git','-C','/home/claude/algocore_system','log','--all','--format=%H'],capture_output=True,text=True).stdout.split())
except Exception:
    COMMITS = set()
ALLOW = re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$')
pats = {"acct-id-shape": re.compile(r"(?<![A-Za-z0-9])[A-Z]{2,4}\d{3,6}(?![0-9A-Za-z])"),
        "acct-id-shape-lower": re.compile(r"(?<![A-Za-z0-9])[a-z]{2,4}\d{3,6}(?![0-9A-Za-z])"),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
        "home-path": re.compile(r"(/home/\w+|/Users/\w+|[A-Za-z]:\\\\)"),
        "session-link": re.compile(r"claude\.ai/(code|chat)/")}
ok_ip = {"0.0.0.0", "127.0.0.1"}
hits = 0
for root in sys.argv[1:]:
    rp = pathlib.Path(root)
    for p in ([rp] if rp.is_file() else rp.rglob("*")):
        if not p.is_file(): continue
        try: t = p.read_text(encoding="utf-8")
        except Exception: continue
        for n, line in enumerate(t.splitlines(), 1):
            for k, rx in pats.items():
                for m in rx.findall(line):
                    m = m if isinstance(m, str) else m[0]
                    if k in ("acct-id-shape", "acct-id-shape-lower") and (ALLOW.match(m.upper()) or m in COMMITS): continue
                    if k == "ipv4" and m in ok_ip: continue
                    if k == "home-path" and m.startswith("/home/claude"): continue
                    if k == "email" and (m.rpartition("@")[2] == "users.noreply.github.com" or (m.rpartition("@")[0] == "noreply" and m.rpartition("@")[2] == "anthropic.com")): continue
                    print(f"HIT {k}: {p}:{n}"); hits += 1
print(f"SCAN HITS: {hits}")
sys.exit(1 if hits else 0)
