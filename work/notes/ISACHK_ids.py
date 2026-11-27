"""ISA checker: read-only ID and quotation-length check of the ISA file (writes nothing)."""
import re, pathlib, collections
F = pathlib.Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md").read_text(encoding="utf-8")
lines = F.split("\n")
# section of each line
sec = []
cur = "0"
for l in lines:
    m = re.match(r"^#{2,3} (\d+(?:\.\d+)?)", l)
    if m: cur = m.group(1)
    sec.append(cur)
defs = collections.defaultdict(list)
for i, l in enumerate(lines):
    m = re.match(r"^\| (IS-\d{3}|IC-\d{3}|RS-\d{2})( |,)", l)
    if m: defs[m.group(1)].append((i + 1, sec[i]))
for pref, n, w in (("IS", 98, 3), ("IC", 6, 3), ("RS", 29, 2)):
    want = [f"{pref}-{k:0{w}d}" for k in range(1, n + 1)]
    missing = [x for x in want if x not in defs]
    extra = sorted(k for k in defs if k.startswith(pref + "-") and k not in want)
    multi = {x: defs[x] for x in want if len(defs.get(x, [])) > 1}
    print(pref, "defined", sum(1 for x in want if x in defs), "of", n, "| missing", missing, "| extra", extra)
    for x, v in multi.items():
        print("   defined more than once:", x, v)
# references to own IDs (not preceded by a topic prefix like "A05 IS-64")
bad = []
for i, l in enumerate(lines):
    for m in re.finditer(r"(?<![A-Za-z0-9-])(IS-\d{2,3}|IC-\d{2,3}|RS-\d{2})(?!\d)", l):
        pre = l[max(0, m.start() - 12):m.start()]
        if re.search(r"A0\d(?: [A-Z]{2,4})? $", pre) or re.search(r"A0\d's $", pre) or re.search(r"A0\d (IS|IC|RS)-\d+, $", pre):
            continue
        tok = m.group(1)
        if re.fullmatch(r"IS-\d{3}|IC-\d{3}|RS-\d{2}", tok) and tok not in defs:
            bad.append((i + 1, tok, l[max(0, m.start() - 50):m.end() + 10]))
print("references to undefined own IDs:", len(bad))
for b in bad[:40]: print("  ", b)
# quotation length: fragments between straight double quotes with 15 or more words
longq = []
for i, l in enumerate(lines):
    for q in re.findall(r'"([^"]+)"', l):
        words = len(q.split())
        if words >= 15:
            longq.append((i + 1, words, q[:120]))
print("quoted fragments of 15 or more words:", len(longq))
for x in longq: print("  ", x)
