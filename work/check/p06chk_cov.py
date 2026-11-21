"""P06 checker coverage script (read-only).

(a) every class, function and method of screening/entry_gate.py at the baseline (AST of the `git show` text; legacy
    code is never imported or run) appears in at least one P06 statement; the interface records of
    continue_from_gate (D-39 P2) are present;
(b) the assigned focused questions Q12, Q10, Q11 are answered (statement present, carrying the question's full wording);
(c) the 17 inherited items of P06's row in P01-S074 are cross-referenced;
plus: statement numbering S001..S129 without gaps or duplicates, every cited P06 ID defined, the fixed entry-gate
wording present word for word, and the files cited outside the gate's interface set.
Run: python3 -I -B /home/claude/a07/check/p06chk_cov.py
"""
import ast
import re
import subprocess
import sys

PART = "/home/claude/a07/parts/A07_ENTRY_GATE_AND_RESUME_CONTRACT_2026-11-21.md"
QFILE = "/home/claude/a07/briefs/A07_FOCUSED_QUESTIONS.md"
COMMON = "/home/claude/a07/briefs/A07_COMMON_BRIEF.md"
REPO = "/home/claude/repos/legacy"

text = open(PART, encoding="utf-8").read()
# cut off the checker's own section, if present, so that it cannot satisfy the coverage
body = text.split("\n## Check log")[0]

# statements: list items and table rows that start with an ID
stmt = {}
for line in body.split("\n"):
    m = re.match(r"^(?:- |\| )(P06-(?:S\d{3}|AP\d{2}|U\d{2}|R\d))\b", line)
    if m:
        stmt.setdefault(m.group(1), []).append(line)

ok = True
def fail(msg):
    global ok
    ok = False
    print("FAIL:", msg)

# numbering
s_ids = sorted(int(k[5:]) for k in stmt if k.startswith("P06-S"))
dups = [k for k, v in stmt.items() if len(v) > 1]
print(f"statements S: {len(s_ids)} (min S{min(s_ids):03d}, max S{max(s_ids):03d}); "
      f"AP: {sum(k.startswith('P06-AP') for k in stmt)}; U: {sum(k.startswith('P06-U') for k in stmt)}; "
      f"R: {sum(k.startswith('P06-R') for k in stmt)}")
missing = sorted(set(range(1, max(s_ids) + 1)) - set(s_ids))
if missing:
    fail(f"gaps: {missing}")
if dups:
    fail(f"duplicates: {dups}")
cited = set(re.findall(r"P06-(?:S\d{3}|AP\d{2}|U\d{2}|R\d)\b", body))
undef = sorted(c for c in cited if c not in stmt)
if undef:
    fail(f"cited but not defined: {undef}")
else:
    print(f"cited P06 IDs: {len(cited)}, all defined")

# (a) definitions of the gate file
src = subprocess.run(["git", "-C", REPO, "show", "970aabf:screening/entry_gate.py"],
                     capture_output=True, text=True, check=True).stdout
tree = ast.parse(src)
defs = []
for node in tree.body:
    if isinstance(node, ast.ClassDef):
        defs.append(("class", node.name, node.lineno, node.end_lineno))
        for sub in node.body:
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defs.append(("method", f"{node.name}.{sub.name}", sub.lineno, sub.end_lineno))
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        defs.append(("function", node.name, node.lineno, node.end_lineno))
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                defs.append(("constant", t.id, node.lineno, node.end_lineno))
print(f"\n(a) definitions in screening/entry_gate.py: {len(defs)}")
for kind, name, a, b in defs:
    short = name.split(".")[-1]
    pat = re.compile(r"`" + re.escape(short) + r"(?:\(|`|\.|\b)")
    hits = [k for k, lines in stmt.items() if any(pat.search(l) for l in lines)]
    hits_s = [h for h in hits if h.startswith("P06-S")]
    if short == "__init__":   # the constructor is recorded as "constructor"
        hits_s = [k for k, lines in stmt.items() if k.startswith("P06-S") and any("constructor" in l and "L108" in l for l in lines)]
    status = "OK" if hits_s else "MISSING"
    if not hits_s:
        fail(f"{name} not named in any statement")
    print(f"  {kind:8s} {name:40s} L{a}-L{b}: {status} {', '.join(sorted(hits_s)[:12])}{' ...' if len(hits_s) > 12 else ''}")

# interface records of continue_from_gate (D-39 P2)
print("\n(a2) interface records of continue_from_gate")
need = {
    "signature (L2010)": r"continue_from_gate\(self, entry: object, release_ltp",
    "only non-test caller (_gate_release_worker, main.py L873)": r"_gate_release_worker`? \(L873\)|`_gate_release_worker` \(L873\)",
    "inputs read from the entry (L2027 to L2099)": r"`signal_id`, `symbol` \(L2027 to L2028\)",
    "return value None": r"returns `None` on every route",
    "statuses written": r"`PROCESSING` \(L2034\), `RESERVED` \(L2171\), `PROCESSED_NO_PLACER` \(L2186\)",
    "decision order at call level": r"the order is A06's and is recorded here at the call level only",
    "strategy_will_trade at L2062 cross-referenced to P02": r"strategy control at L2062; logic in part P02",
    "failure contract": r"failure contract at the interface",
    "handoff to A09 and A10": r"handoff to A09 and A10, interface only",
    "no guard against second resumption": r"no guard against a second resumption",
}
for label, pat in need.items():
    hits = [k for k, lines in stmt.items() if any(re.search(pat, l) for l in lines)]
    print(f"  {label:60s}: {'OK ' + ', '.join(sorted(hits)) if hits else 'MISSING'}")
    if not hits:
        fail(f"interface record missing: {label}")

# (b) questions
print("\n(b) assigned focused questions")
qtext = open(QFILE, encoding="utf-8").read()
for q, sid in (("12", "P06-S126"), ("10", "P06-S127"), ("11", "P06-S128")):
    m = re.search(r"^" + q + r"\. (.+)$", qtext, re.M)
    full = m.group(1).strip()
    line = " ".join(stmt.get(sid, []))
    has_q = full in line
    print(f"  Q{q}: {sid} present={sid in stmt}; full wording quoted={has_q}")
    if not (sid in stmt and has_q):
        fail(f"Q{q} answer or wording missing")

# fixed wording
common = open(COMMON, encoding="utf-8").read()
m = re.search(r"- Entry-gate wording \(fixed\): (.+?)\n\n", common, re.S)
fixed = " ".join(m.group(1).split())
flat = " ".join(body.split())
n_fixed = flat.count(fixed)
print(f"\nfixed entry-gate wording, word for word: {n_fixed} occurrence(s)")
for k, lines in stmt.items():
    if fixed in " ".join(" ".join(lines).split()):
        print(f"  in {k}")
if n_fixed < 1:
    fail("fixed wording not found word for word")

# (c) inherited items
print("\n(c) inherited items of P06's row (P01-S074)")
items = ["A01 C14", "A01 C15", "A01 C20", "A01 B-28", "A02 T-14", "A03 H-50", "A03 P-02", "A03 P-11",
         "A03 Q-11", "A03 Q-12", "A03 Q-45", "A04 RD-12", "A04 RL-11", "A06 WA-07", "A06 PQ-13", "A06 EV-11",
         "A06 ET-13"]
found = 0
for it in items:
    hits = [k for k, lines in stmt.items() if k.startswith("P06-S") and any(f"| {it} (P01-S" in l for l in lines)]
    print(f"  {it:10s}: {', '.join(hits) if hits else 'MISSING'}")
    if hits:
        found += 1
    else:
        fail(f"inherited item {it} not cross-referenced")
print(f"  {found} of {len(items)} items cross-referenced")

# files cited outside the gate's interface set (for the boundary review; listing only)
allowed = {"screening/entry_gate.py", "main.py", "signals/signal_processor.py", "core/state_store.py",
           "core/schema.sql", "orders/eod_squareoff.py", "broker/zerodha_adapter.py", "broker/rate_limiter.py",
           "core/effect_telemetry.py", "core/time_authority.py", "strategies/schema.py", "core/config_loader.py",
           "config/expected_managers.yaml"}
paths = sorted(set(re.findall(r"`((?:[a-z_]+/)+[a-z_0-9]+\.(?:py|sql|yaml|txt|md))`", body)))
outside = [p for p in paths if p not in allowed]
print("\nfiles cited outside the gate's interface set (boundary review):")
for p in outside:
    print("  ", p)

print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
