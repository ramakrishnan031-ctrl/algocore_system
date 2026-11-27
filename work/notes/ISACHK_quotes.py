"""ISA checker: read-only quotation locator. Reads the ISA file and the project records (Markdown only);
writes only its report to the notes folder. For every quoted fragment in each row, finds the files/lines of the
project records that contain it (exact after whitespace normalisation, or relaxed: backticks/asterisks dropped,
curly quotes straightened). Usage: python3 -I ISACHK_quotes.py [first_line last_line]"""
import re, sys, pathlib, collections

ROOT = pathlib.Path("/home/claude/algocore_system/doc")
F = pathlib.Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md")
EXTRA = [pathlib.Path("/home/claude/a08/notes/RAMA_DECISIONS_A08_STUDY.md")]
OUT = pathlib.Path("/home/claude/a08/notes/ISACHK_quotes_out.txt")

def short(p):
    s = str(p)
    if "RAMA_DECISIONS" in s: return "WNOTE"
    name = p.name
    m = re.match(r"(A0\d)_(AUDIT_INTENT_SOURCES|AUDIT|RECONCILED_TOPIC_RECORD|STUDY)_", name)
    if m:
        k = {"AUDIT_INTENT_SOURCES": "IS", "AUDIT": "AUDIT", "RECONCILED_TOPIC_RECORD": "RTR", "STUDY": "STUDY"}[m.group(2)]
        return f"{m.group(1)} {k}"
    tbl = {"MASTER_SYSTEM_INVESTIGATION_INDEX": "MSII", "DECISION_REGISTER": "DR", "TOPIC_COMPLETION": "TCR",
           "OPEN_ISSUES": "OIR", "AUDIT_FINDINGS": "AFR", "SOURCE_INVENTORY": "SRCINV", "WHOLE_SYSTEM": "WSO",
           "OPERATIONAL_WORKFLOWS": "OPW", "PHASE1_METHODOLOGY": "PMA", "01_SYSTEM_OVERVIEW": "R01",
           "02_REPOSITORY": "R02", "03_STARTUP": "R03", "03A_CRON": "R03A", "LEGACY_SYSTEM_MANUAL": "RMI",
           "A08_PIVOTS": "P01", "A08_CANDLE": "P02", "A08_V1_OBSERVER": "P03", "A08_V2_RETEST": "P04",
           "A08_SPOTCHECK": "P05", "A08_CONFIGURATION": "P06", "A08_PRIOR": "P07", "A08_SOURCE_FILE": "INV"}
    for k, v in tbl.items():
        if name.startswith(k) or k in name:
            return v
    m = re.match(r"(\d\d)_", name)
    if m and "FOUNDATION" in s: return "DOC" + m.group(1)
    if name.startswith("A08_STUDY"): return "STUDY"
    return name

files = sorted(ROOT.rglob("*.md")) + EXTRA
DOCS = {}
for p in files:
    try:
        DOCS[short(p)] = p.read_text(encoding="utf-8").split("\n")
    except Exception as e:
        print("skip", p, e)

def norm(s):
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()

def relax(s):
    s = norm(s)
    s = s.replace("`", "").replace("**", "").replace("*", "")
    return s

# per-file normalised lines (exact and relaxed)
NL = {k: [norm(l) for l in v] for k, v in DOCS.items()}
RL = {k: [relax(l) for l in v] for k, v in DOCS.items()}

import bisect
JOIN = {}
for k, v in DOCS.items():
    for mode, fn in (("exact", norm), ("relaxed", relax)):
        parts, starts, pos = [], [], 0
        for l in v:
            t = fn(l)
            starts.append(pos); parts.append(t); pos += len(t) + 1
        JOIN[(k, mode)] = (" ".join(parts), starts)

def find(frag):
    hits = []
    for k in DOCS:
        if k == "A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md":
            continue
        for mode, fn in (("exact", norm), ("relaxed", relax)):
            f = fn(frag)
            if not f: continue
            text, starts = JOIN[(k, mode)]
            got = False
            for m in re.finditer(re.escape(f), text):
                hits.append((k, bisect.bisect_right(starts, m.start()), mode)); got = True
            if got: break
    return hits

lines = F.read_text(encoding="utf-8").split("\n")
a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, len(lines))
out = []
nf_count = 0
for ln in range(a, b + 1):
    l = lines[ln - 1]
    m = re.match(r"^\| (IS-\d{3}|IC-\d{3}|RS-\d{2})[ ,]", l) or re.match(r"^\| (IS-\d{3}(?:, IS-\d{3})*) \|", l)
    rid = m.group(1) if m else ("Q" if "ISA-Q" in l else "-")
    # fragments between straight double quotes
    qs = re.findall(r'"([^"]+)"', l)
    if not qs:
        continue
    out.append(f"===== L{ln} {rid}: {len(qs)} quoted fragments")
    for q in qs:
        q2 = q.strip()
        if len(q2) < 6 or len(q2.split()) < 2 and len(q2) < 12:
            continue
        # split on ellipses: each part must be found
        parts = [p.strip(" ,;:") for p in re.split(r"\s*(?:\.\.\.|…)\s*", q2) if len(p.strip(" ,;:")) >= 4]
        for p in parts:
            h = find(p)
            words = len(p.split())
            if not h:
                nf_count += 1
                out.append(f"  NOT FOUND [{words}w]: {p[:160]}")
            else:
                locs = collections.OrderedDict()
                for k, i, kind in h:
                    locs.setdefault(k, []).append(f"L{i}{'' if kind == 'exact' else 'r'}")
                s = "; ".join(f"{k} {','.join(v[:6])}{'+' if len(v) > 6 else ''}" for k, v in list(locs.items())[:6])
                out.append(f"  ok [{words}w] {p[:90]} -> {s}")
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print("lines", a, b, "not found", nf_count, "report", OUT)
