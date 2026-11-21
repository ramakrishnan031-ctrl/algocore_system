#!/usr/bin/env python3
"""P05 checker coverage script (read-only; run with python3 -I -B).

(a) every function, method and class (nested functions included) and every module-level
    constant of screening/quality_scorer.py and screening/hard_gate.py at 970aabf, and
    SecondaryScreener._screen_v3_enforce and _log_v3_shadow_compare, named in at least one
    P05 statement (list each with the statement IDs);
(b) focused questions Q8, Q9 (for scoring and the gates) and Q17: the answer statement
    quotes the question's full wording exactly, and a keyword probe of each element of the
    wording over the answer and the statements it cites (the checker judges by reading);
(c) the six inherited items of P05's row of P01-S074 cross-referenced in section 12;
(d) numbering S001..Smax without gaps or duplicates, one leading label per statement;
    the Points, UNKNOWN items and questions numbered without gaps.
Legacy text is read with `git show` and parsed with `ast`; nothing is imported or run.
"""
import ast
import re
import subprocess
import sys

REPO = "/home/claude/repos/legacy"
PART = "/home/claude/a07/parts/A07_QUALITY_SCORER_HARD_GATE_AND_V3_PLAYBOOK_GATES_2026-11-21.md"
QFILE = "/home/claude/a07/briefs/A07_FOCUSED_QUESTIONS.md"
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")


def git_show(path):
    return subprocess.run(["git", "-C", REPO, "show", f"970aabf:{path}"],
                          check=True, capture_output=True, text=True).stdout


def defs(src, only=None):
    """(kind, qualified name, bare name, line) for classes, functions, methods, nested
    functions and module-level constants."""
    out = []
    tree = ast.parse(src)

    def walk_fn(fn, prefix):
        for sub in ast.walk(fn):
            if sub is fn:
                continue
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out.append(("nested function", f"{prefix}.{sub.name}", sub.name, sub.lineno))

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if only and node.name != only[0]:
                continue
            if not only:
                out.append(("class", node.name, node.name, node.lineno))
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if only and sub.name not in only[1]:
                        continue
                    out.append(("method", f"{node.name}.{sub.name}", sub.name, sub.lineno))
                    walk_fn(sub, f"{node.name}.{sub.name}")
        elif only:
            continue
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(("function", node.name, node.name, node.lineno))
            walk_fn(node, node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.append(("constant", t.id, t.id, node.lineno))
    return out


def statements(text):
    """Map statement ID -> (section, text incl. following table rows). Section-12
    statements are table rows beginning '| P05-Snnn'."""
    st, order, cur, sec, top = {}, [], None, "", ""
    for line in text.splitlines():
        if line.startswith("## "):
            top = line.strip("# ").strip()
            sec, cur = top, None
            continue
        if line.startswith("### "):
            sec, cur = top + " / " + line.strip("# ").strip(), None
            continue
        m = re.match(r"^- (P05-S\d{3}) (.*)$", line) or re.match(r"^\| (P05-S\d{3}) (.*)$", line)
        if m:
            cur = m.group(1)
            order.append(cur)
            st[cur] = [sec, m.group(2)]
            continue
        if re.match(r"^- (P05-AP\d{2}|P05-U\d{2}|P05-R\d)", line) or line.startswith("## Check log"):
            cur = None
            continue
        if cur and line.strip():
            st[cur][1] += "\n" + line
    return st, order


def main():
    text = open(PART, encoding="utf-8").read()
    body = text.split("\n## Check log")[0]
    st, order = statements(body)
    ok = True
    out = []

    # (d) numbering and labels
    nums = [int(s[5:]) for s in order]
    dup = sorted({n for n in nums if nums.count(n) > 1})
    gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
    out.append(f"(d) statements: {len(order)} (P05-S001 to P05-S{max(nums):03d}); duplicates: {dup or 'none'}; gaps: {gaps or 'none'}")
    bad = [s for s in order if not any(st[s][1].lstrip("*").startswith(l) for l in LABELS)]
    out.append(f"(d) statements whose text does not begin with an allowed label: {bad or 'none'}")
    for kind, pat in (("Points for the AUDIT", r"^- (P05-AP(\d{2}))"), ("UNKNOWN items", r"^- (P05-U(\d{2}))"),
                      ("questions for Rama", r"^- (P05-R(\d))")):
        ids = [int(m.group(2)) for m in re.finditer(pat, body, re.M)]
        g = sorted(set(range(1, max(ids) + 1)) - set(ids))
        d = sorted({i for i in ids if ids.count(i) > 1})
        out.append(f"(d) {kind}: {len(ids)} (1 to {max(ids)}); gaps: {g or 'none'}; duplicates: {d or 'none'}")
        ok &= not g and not d
    ok &= not dup and not gaps and not bad

    # (a) definitions
    targets = []
    for path in ("screening/quality_scorer.py", "screening/hard_gate.py"):
        for d in defs(git_show(path)):
            targets.append((path,) + d)
    for d in defs(git_show("screening/secondary_screener.py"),
                  only=("SecondaryScreener", {"_screen_v3_enforce", "_log_v3_shadow_compare"})):
        targets.append(("screening/secondary_screener.py",) + d)
    # explicit patterns for bare method names that are generic words
    special = {
        "QualityScorer.__init__": [r"QualityScorer\.__init__"],
        "QualityScorer.score": [r"`score\(\)`", r"QualityScorer\.score", r"\.score\("],
        "HardGate.__init__": [r"HardGate\.__init__"],
        "HardGate.evaluate": [r"`evaluate\(", r"HardGate\.evaluate", r"\.evaluate\("],
        "circuit_proximity_reason._pos_num": [r"`_pos_num"],
    }
    out.append("(a) definitions (path, kind, name, baseline line -> statement IDs):")
    missing = []
    for path, kind, qual, bare, line in targets:
        pats = special.get(qual, [re.escape(f"`{bare}") + r"[`(]", r"\b" + re.escape(bare) + r"\b"])
        hits = [s for s in order if any(re.search(p, st[s][1]) for p in pats)]
        out.append(f"    {path} {kind} {qual} L{line}: {len(hits)} -> {', '.join(h[4:] for h in hits[:12])}{' ...' if len(hits) > 12 else ''}")
        if not hits:
            missing.append(qual)
    out.append(f"(a) definitions: {len(targets)}; not named in any statement: {missing or 'none'}")
    ok &= not missing

    # (b) focused questions
    qtext = open(QFILE, encoding="utf-8").read()
    # the question line, not the section heading "8. FOCUSED INVESTIGATION QUESTIONS"
    qs = {n: [m.group(1).strip() for m in re.finditer(rf"^{n}\. (.*)$", qtext, re.M) if "?" in m.group(1)][0]
          for n in (8, 9, 17)}
    answers = {8: "P05-S113", 9: "P05-S114", 17: "P05-S115"}
    elements = {
        8: ["hard gate", "score", "advance", "defer", "names", "comments"],
        9: ["threshold", "unit", "formula", "weight", "aggregat", "rounding", "boundar", "configured", "effective", "as declared"],
        17: ["regime/", "v3_chain/", "read back", "A07's integration", "A18's internal logic"],
    }
    for n, sid in answers.items():
        a = st[sid][1]
        quoted = qs[n] in a
        cited = sorted(set(re.findall(r"P05-S\d{3}", a)) - {sid})
        pool = a + "".join(st[c][1] for c in cited if c in st)
        probe = {e: (e.lower() in pool.lower()) for e in elements[n]}
        out.append(f"(b) Q{n} answered in {sid}: full wording quoted exactly: {quoted}; statements cited: {len(cited)}; element probe: {probe}")
        ok &= quoted and all(probe.values())

    # (c) inherited items
    sec12 = body.split("## 12.")[1].split("## 13.")[0]
    items = {"T-20": "P01-S026", "K-27": "P01-S029", "RD-12": "P01-S047",
             "WA-06": "P01-S059", "WA-07": "P01-S060", "PQ-08": "P01-S062"}
    for item, p01 in items.items():
        rows = [l for l in sec12.splitlines() if l.startswith("| P05-S") and item in l and p01 in l]
        out.append(f"(c) {item} ({p01}): {'cross-referenced in ' + rows[0][2:11] if rows else 'MISSING'}")
        ok &= bool(rows)

    out.append("RESULT: " + ("PASS" if ok else "FAIL"))
    print("\n".join(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
