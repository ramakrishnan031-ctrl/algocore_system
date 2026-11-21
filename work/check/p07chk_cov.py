"""P07 checker coverage script.

(a) every function, method and class of the three P07 scripts appears in at least one statement;
(b) every focused question assigned to P07 (Q18 to Q21) has the statements that P07-S097 lists, and
    each listed statement exists;
(c) every inherited item and handoff point of P07's row (P01-S074) and of ADDENDUM 1 and 2 is
    cross-referenced in the section 7 table and in at least one statement;
(d) numbering: P07-S001 to the highest number, each once, no gap; every statement starts with a label.

The legacy files are read as TEXT with `git show` and parsed with `ast.parse` only; nothing is
imported or run. Run: python3 -I -B p07chk_cov.py
"""
import ast
import re
import subprocess

REPO = "/home/claude/repos/legacy"
BASE = "970aabf"
PART = "/home/claude/a07/parts/A07_STRATEGY_SCRIPTS_2026-11-21.md"
SCRIPTS = {
    "scripts/compute_strategy_metrics.py": ("2", "3"),
    "scripts/strategy_registry_officer.py": ("4",),
    "scripts/strategy_status.py": ("5",),
}
LABELS = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")
COMMON_WORDS = {"run", "main"}


def git_show(path):
    return subprocess.run(["git", "-C", REPO, "show", f"{BASE}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def defs(src):
    tree = ast.parse(src)
    out = []

    def walk(node, prefix):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                kind = "class" if isinstance(ch, ast.ClassDef) else (
                    "method" if prefix and prefix[-1][0] == "class" else
                    ("nested function" if prefix else "function"))
                out.append((kind, ".".join(p[1] for p in prefix + [("", ch.name)] if p[1]), ch.name, ch.lineno))
                walk(ch, prefix + [("class" if isinstance(ch, ast.ClassDef) else "def", ch.name)])
            else:
                walk(ch, prefix)
    walk(tree, [])
    return out


def statements(text):
    blocks, cur_id, cur_sec, cur = {}, None, None, []
    sec_of = {}
    for line in text.splitlines():
        m_sec = re.match(r"^##+ (\d+)(?:\.\d+)?\.? ", line)
        if m_sec:
            if cur_id:
                blocks[cur_id] = "\n".join(cur)
            cur_id, cur = None, []
            cur_sec = m_sec.group(1)
            continue
        m = re.match(r"^- (P07-S\d{3}) ", line)
        if m:
            if cur_id:
                blocks[cur_id] = "\n".join(cur)
            cur_id, cur = m.group(1), [line]
            sec_of[cur_id] = cur_sec
            continue
        if re.match(r"^- P07-(AP|U|R)\d", line) or line.startswith("## "):
            if cur_id:
                blocks[cur_id] = "\n".join(cur)
            cur_id, cur = None, []
            continue
        if cur_id:
            cur.append(line)
    if cur_id:
        blocks[cur_id] = "\n".join(cur)
    return blocks, sec_of


def mentions(block, name, path):
    if name in COMMON_WORDS:
        pat = re.compile(r"`%s`|`%s\(|\b%s\(" % (name, name, name))
    else:
        pat = re.compile(r"(?<![\w.])%s(?![\w])" % re.escape(name))
    return bool(pat.search(block))


def main():
    text = open(PART, encoding="utf-8").read()
    blocks, sec_of = statements(text)
    ok = True
    print("(a) functions, methods and classes")
    for path, secs in SCRIPTS.items():
        src = git_show(path)
        short = path.split("/")[-1]
        for kind, qual, name, line in defs(src):
            ids = [sid for sid, b in blocks.items()
                   if (mentions(b, name, path) or ("." in qual and qual in b))
                   and (sec_of.get(sid) in secs or short in b)]
            status = "PASS" if ids else "FAIL"
            ok &= bool(ids)
            print(f"  {status} {short} {kind} {qual} L{line} -> {', '.join(sorted(ids)) or 'NONE'}")
    print("(b) focused questions (from P07-S097)")
    s097 = blocks.get("P07-S097", "")
    for q, nxt in (("Q18", "Q19"), ("Q19", "Q20"), ("Q20", "Q21"), ("Q21", None)):
        seg = s097.split(q + " —", 1)[1] if (q + " —") in s097 else ""
        if nxt and (nxt + " —") in seg:
            seg = seg.split(nxt + " —", 1)[0]
        refs = set()
        for a, b in re.findall(r"P07-S(\d{3})(?: to P07-S(\d{3}))?", seg):
            lo = int(a); hi = int(b) if b else lo
            refs.update(f"P07-S{n:03d}" for n in range(lo, hi + 1))
        missing = sorted(r for r in refs if r not in blocks)
        status = "PASS" if refs and not missing else "FAIL"
        ok &= status == "PASS"
        print(f"  {status} {q}: {len(refs)} statements cited, missing {missing}")
    print("(c) inherited items and handoff points (P01-S074 row P07; ADDENDUM 1 and 2)")
    sec7 = text.split("## 7. ", 1)[1].split("## 8. ", 1)[0]
    items = {
        "A02 K-05": r"K-05", "A03 D-05": r"D-05", "A03 D-09": r"D-09", "A03 E-08": r"E-08",
        "PAPER_ONLY demotion (P01-S072 item 1)": r"PAPER_ONLY demotion",
        "A02 AUDIT L540 (P01-S126 item 1)": r"A02 AUDIT L540",
        "A02 AUDIT L1320 (P01-S126 item 2)": r"A02 AUDIT L1320",
    }
    for label, pat in items.items():
        in7 = bool(re.search(pat, sec7))
        stmts = sorted(sid for sid, b in blocks.items() if re.search(pat, b) and sec_of.get(sid) != "7")
        status = "PASS" if in7 and stmts else "FAIL"
        ok &= status == "PASS"
        print(f"  {status} {label}: section 7 table {'yes' if in7 else 'NO'}; statements {', '.join(stmts)}")
    print("(d) numbering and labels")
    nums = sorted(int(s[5:]) for s in blocks)
    ids_all = re.findall(r"^- (P07-S\d{3}) ", text, flags=re.M)
    dup = sorted({i for i in ids_all if ids_all.count(i) > 1})
    gap = [n for n in range(1, nums[-1] + 1) if n not in nums]
    print(f"  {'PASS' if not dup and not gap else 'FAIL'} P07-S001 to P07-S{nums[-1]:03d}: {len(nums)} statements, duplicates {dup}, gaps {gap}")
    ok &= not dup and not gap
    bad = []
    for sid, b in blocks.items():
        first = b.split(" ", 2)[2] if b.count(" ") >= 2 else ""
        if not first.startswith(LABELS):
            bad.append(sid)
    print(f"  {'PASS' if not bad else 'FAIL'} every statement starts with a label (no label: {bad})")
    ok &= not bad
    counts = {}
    for sid, b in blocks.items():
        first = b.split(" ", 2)[2]
        for lab in LABELS:
            if first.startswith(lab):
                counts[lab] = counts.get(lab, 0) + 1
                break
    print("  first labels:", ", ".join(f"{k} {v}" for k, v in counts.items()))
    print("RESULT:", "ALL PASS" if ok else "SOME FAIL")


if __name__ == "__main__":
    main()
