#!/usr/bin/env python3
"""P04 checker coverage script (read-only; run with python3 -I -B).

(a) every function, method and class of screening/step_executor.py at 970aabf, and
    SecondaryScreener._build_market_data, named in at least one P04 statement;
(b) focused questions Q8, Q9 (for the ten steps) and Q13 (for the executor): the
    statements in the sections that answer them, and a keyword probe of each element
    of the question's full wording (the checker judges the result by reading);
(c) the eight inherited items of P04's row of P01-S074;
(d) numbering S001..Smax without gaps, one leading label per statement.
Legacy text is read with `git show` and parsed with `ast`; nothing is imported or run.
"""
import ast
import re
import subprocess
import sys

REPO = "/home/claude/repos/legacy"
PART = "/home/claude/a07/parts/A07_STEP_EXECUTOR_AND_THE_TEN_STEPS_2026-11-21.md"
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")


def git_show(path):
    return subprocess.run(["git", "-C", REPO, "show", f"970aabf:{path}"],
                          check=True, capture_output=True, text=True).stdout


def defs(src):
    out = []
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            out.append(("class", node.name, node.lineno))
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out.append(("method", f"{node.name}.{sub.name}", sub.lineno))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(("function", node.name, node.lineno))
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.append(("constant", t.id, node.lineno))
    return out


def statements(text):
    """Map statement ID -> (section heading, full text incl. following table rows)."""
    st, order, cur, sec, top = {}, [], None, "", ""
    for line in text.splitlines():
        if line.startswith("## "):
            top = line.strip("# ").strip()
            sec = top
            cur = None
            continue
        if line.startswith("### "):
            sec = top + " / " + line.strip("# ").strip()
            cur = None
            continue
        m = re.match(r"^- (P04-S\d{3}) (.*)$", line)
        if m:
            cur = m.group(1)
            order.append(cur)
            st[cur] = [sec, m.group(2)]
            continue
        if cur and line.strip():
            st[cur][1] += "\n" + line
    return st, order


def main():
    text = open(PART, encoding="utf-8").read()
    body = text.split("\n## Check log", 1)[0]
    st, order = statements(body)
    print(f"statements found: {len(order)}")

    # (d) numbering and labels
    nums = [int(s[5:]) for s in order]
    gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
    dups = sorted({n for n in nums if nums.count(n) > 1})
    added = []
    for s_ in order:
        m_ = re.match(r"^[A-Z /]+\(([^)]*)\)", st[s_][1])
        if m_ and "added in the check" in m_.group(1):
            added.append(s_)
    out_of_place = [order[i] for i in range(1, len(order)) if nums[i] < nums[i - 1]]
    print(f"(d) numbering: S001..S{max(nums):03d}; gaps={gaps}; duplicates={dups}; "
          f"statements after a higher number (added at the end of their section): {out_of_place}; "
          f"statements whose label note says 'added in the check': {added}")
    bad = []
    for sid in order:
        t = st[sid][1]
        if t.startswith("WITHDRAWN"):
            continue
        if not any(t.startswith(lb) for lb in LABELS):
            bad.append(sid)
    print(f"(d) statements without a leading label: {bad}")

    # (a) definitions
    print("\n(a) definitions of screening/step_executor.py and _build_market_data")
    se = defs(git_show("screening/step_executor.py"))
    sc = [d for d in defs(git_show("screening/secondary_screener.py"))
          if d[1] == "SecondaryScreener._build_market_data"]
    missing = []
    for kind, name, line in se + sc:
        short = name.split(".")[-1]
        pat = re.compile(r"`" + re.escape(short) + r"`|\b" + re.escape(short) + r"\(")
        ids = [s for s in order if pat.search(st[s][1])]
        print(f"  {kind:8s} {name} (L{line}): {len(ids)} statements: {', '.join(ids) if ids else 'NONE'}")
        if not ids:
            missing.append(name)
    print(f"(a) not named in any statement: {missing if missing else 'none'}")

    # (b) focused questions
    print("\n(b) focused questions (sections whose heading names the question)")
    for q in ("Q8", "Q9", "Q13"):
        ids = [s for s in order if re.search(r"\b" + q + r"\b", st[s][0].split(" / ")[0])]
        print(f"  {q}: sections -> {sorted({st[s][0][:60] for s in ids})}; statements {ids[0] if ids else '-'}..{ids[-1] if ids else '-'} ({len(ids)})")
    probes = {
        "Q8 hard gate / immediate reject": r"hard (gate|reject)|rejects? the signal",
        "Q8 scores / rankings": r"\bscore",
        "Q8 advance or defer": r"advance|defer|park",
        "Q8 names, comments vs semantics": r"names, comments|docstring",
        "Q9 thresholds": r"threshold",
        "Q9 units": r"\bUnits?\b|unit of|percentage",
        "Q9 formulae": r"formula|`[a-z_]+ = \(",
        "Q9 weights": r"\bweights?\b",
        "Q9 score aggregation": r"weighted sum|aggregation|total",
        "Q9 rounding": r"round",
        "Q9 boundary conditions": r"Boundar|`>=`|`<=`|strict",
        "Q9 configured to effective": r"effective|committed|file value",
        "Q13 missing": r"missing",
        "Q13 malformed": r"malformed",
        "Q13 stale": r"stale",
        "Q13 contradictory": r"contradictory|crossed",
        "Q13 exceptions": r"exception",
        "Q13 unavailable market/context data": r"unavailable|SKIPPED_QUOTE_UNAVAILABLE",
        "Q13 database failures": r"database",
        "Q13 partial writes": r"partial write",
        "Q13 surfaced/swallowed/logged/retried/converted": r"surfaced|swallowed|retried",
    }
    for k, rx in probes.items():
        sect = "Q8" if k.startswith("Q8") else ("Q9" if k.startswith("Q9") else "Q13")
        # sections whose top heading names the question (7 and 9 for Q8; 7 and 8 for Q9; 10 for Q13)
        pool = [s for s in order if re.search(r"\b" + sect + r"\b", st[s][0].split(" / ")[0])]
        ids = [s for s in pool if re.search(rx, st[s][1], re.I)]
        print(f"  {k}: {', '.join(ids) if ids else 'NONE'}")

    # (c) inherited items
    print("\n(c) inherited items of P04's row of P01-S074")
    for item in ("T-20", "RD-12", "CM-07", "CM-22", "WA-06", "PQ-02", "PQ-08", "ET-06"):
        ids = [s for s in order if re.search(r"\b" + re.escape(item) + r"\b", st[s][1])]
        sec11 = [s for s in ids if st[s][0].startswith("11.")]
        print(f"  {item}: section 11 -> {', '.join(sec11) if sec11 else 'NONE'}; all -> {len(ids)}")


if __name__ == "__main__":
    sys.exit(main())
