"""P03 checker coverage script (read-only).

(a) every class, function and method of screening/secondary_screener.py at the
    baseline appears in at least one P03 statement (owner marks per ADDENDUM 3);
(b) the assigned focused questions Q6, Q7, Q10, Q11, Q13 are answered with
    their verbatim wording (checked against A07_FOCUSED_QUESTIONS.md);
(c) the 14 inherited items of P03's row (P01-S074) each have a statement;
plus numbering (P03-S001..max, no gaps, each ID once) and the leading label.

The legacy file is read with `git show` and parsed with `ast.parse` only
(nothing is imported or run). Usage:
  python3 -I -B p03chk_coverage.py <part_file> <questions_file> <out_file>
"""
import ast
import re
import subprocess
import sys

LEGACY = "/home/claude/repos/legacy"
BASE = "970aabf"
SRC = "screening/secondary_screener.py"

OWNER = {  # ADDENDUM 3: content owned elsewhere; P03 needs a call-level statement
    "_build_market_data": "P04 (content); P03 call level",
    "_screen_v3_enforce": "P05 (internals); P03 routes at call level",
    "_log_v3_shadow_compare": "P05 (internals); P03 call level",
}
ITEMS = ["C20", "T-14", "H-16", "P-02", "P-11", "Q-22", "RD-12", "PR-23",
         "WA-06", "WA-07", "PQ-02", "PQ-15", "EV-02", "EV-19"]
QUESTIONS = ["6", "7", "10", "11", "13"]
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL",
          "OPEN QUESTION")


def defs_of_source():
    text = subprocess.run(["git", "-C", LEGACY, "show", f"{BASE}:{SRC}"],
                          capture_output=True, text=True, check=True).stdout
    tree = ast.parse(text)
    out = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            out.append(("class", node.name, node.lineno, None))
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out.append(("method", sub.name, sub.lineno, node.name))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(("function", node.name, node.lineno, None))
    return out


def statements(part_text):
    """Map statement ID -> full text of its line (bullet or table row)."""
    st = {}
    starts = []
    for line in part_text.splitlines():
        m = re.match(r"^(?:- |\| )(P03-S\d{3})\b(.*)$", line)
        if m:
            sid = m.group(1)
            starts.append(sid)
            st.setdefault(sid, "")
            st[sid] += m.group(2) + "\n"
    return st, starts


def section_of(part_text, sid):
    sec = None
    for line in part_text.splitlines():
        h = re.match(r"^## (\d+)\.", line)
        if h:
            sec = int(h.group(1))
        if re.match(rf"^(?:- |\| ){sid}\b", line):
            return sec
    return None


def main():
    part_file, q_file, out_file = sys.argv[1:4]
    part = open(part_file, encoding="utf-8").read()
    # the checker's own "Check log" section lists corrections by ID; it is not part of the statements
    if "\n## Check log" in part:
        part = part.split("\n## Check log", 1)[0]
    qtext = open(q_file, encoding="utf-8").read()
    st, starts = statements(part)
    lines = []
    ok = True

    # Numbering
    nums = sorted(int(s[5:]) for s in st)
    expected = list(range(1, max(nums) + 1))
    dup = sorted({s for s in starts if starts.count(s) > 1})
    gaps = sorted(set(expected) - set(nums))
    lines.append(f"NUMBERING: {len(st)} statements, P03-S001 to P03-S{max(nums):03d}; "
                 f"gaps {gaps or 'none'}; duplicated starts {dup or 'none'}")
    if gaps or dup:
        ok = False

    # Labels
    bad = []
    for sid, body in st.items():
        b = body.lstrip(" |")
        if not any(b.startswith(lab) for lab in LABELS):
            bad.append(sid)
    lines.append(f"LEADING LABEL: {'all statements start with an allowed label' if not bad else 'MISSING in ' + ', '.join(bad)}")
    if bad:
        ok = False
    withdrawn = [s for s, b in st.items() if "WITHDRAWN" in b]
    added = [s for s, b in st.items()
             if re.match(r"^\s*\|?\s*(FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|OPEN QUESTION) \(added in the check", b)]
    lines.append(f"WITHDRAWN: {withdrawn or 'none'}; ADDED IN THE CHECK: {', '.join(sorted(added)) or 'none'}")

    # (a) definitions
    lines.append("")
    lines.append("(a) DEFINITIONS OF screening/secondary_screener.py AT 970aabf (ast.parse; nothing imported or run)")
    for kind, name, lineno, parent in defs_of_source():
        if name == "__init__":
            pats = [r"`SecondaryScreener\.__init__`", r"\bconstructor\b"]
        else:
            pats = [rf"`{re.escape(name)}`", rf"`{re.escape(name)}\(", rf"\b{re.escape(name)}\b"]
        hits = sorted(s for s, b in st.items() if any(re.search(p, b) for p in pats))
        label = f"{kind} {parent + '.' if parent else ''}{name} (L{lineno})"
        owner = OWNER.get(name, "P03")
        status = "COVERED" if hits else "NOT COVERED"
        if not hits:
            ok = False
        shown = ", ".join(hits[:12]) + (f" (+{len(hits) - 12} more)" if len(hits) > 12 else "")
        lines.append(f"  {status}: {label}; owner {owner}; statements {shown or '-'}")

    # (b) questions
    lines.append("")
    lines.append("(b) ASSIGNED FOCUSED QUESTIONS (verbatim wording from the questions file)")
    qmap = {}
    for m in re.finditer(r"^(\d+)\. (.+)$", qtext, re.M):
        qmap[m.group(1)] = m.group(2).strip()
    for q in QUESTIONS:
        full = qmap.get(q)
        hits = sorted(s for s, b in st.items() if re.search(rf"\(Q{q}\b", b))
        sec14 = [s for s in hits if section_of(part, s) == 14]
        # verbatim check: each sentence of the question must appear in some section-14 answer
        parts_ = [p.strip() + "?" for p in full.split("?") if p.strip()]
        verb = all(any(p in st[s] for s in sec14) for p in parts_)
        unk = any("UNKNOWN / NOT ESTABLISHED" in st[s] for s in sec14)
        status = "ANSWERED" if sec14 and verb else "NOT ANSWERED"
        if status != "ANSWERED":
            ok = False
        lines.append(f"  Q{q}: {status}; answer statements {', '.join(sec14) or '-'}; "
                     f"verbatim wording present: {verb}; question parts: {len(parts_)}; "
                     f"UNKNOWN in answer: {unk}; other statements citing Q{q}: "
                     f"{', '.join(s for s in hits if s not in sec14) or '-'}")

    # (c) inherited items
    lines.append("")
    lines.append("(c) INHERITED ITEMS OF P03'S ROW (P01-S074): 14")
    found = 0
    for it in ITEMS:
        hits = sorted(s for s, b in st.items()
                      if section_of(part, s) == 13 and re.search(rf"\b{re.escape(it)}\b", b))
        others = sorted(s for s, b in st.items()
                        if section_of(part, s) != 13 and re.search(rf"\b{re.escape(it)}\b", b))
        if hits:
            found += 1
        else:
            ok = False
        lines.append(f"  {'CROSS-REFERENCED' if hits else 'MISSING'}: {it}; section 13 row {', '.join(hits) or '-'}; "
                     f"also cited in {', '.join(others) or '-'}")
    lines.append(f"  items with a section 13 statement: {found} of {len(ITEMS)}")

    lines.append("")
    lines.append("RESULT: " + ("PASS" if ok else "FAIL"))
    open(out_file, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
