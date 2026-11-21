import re, sys, pathlib
p = pathlib.Path("/home/claude/a07/parts/A07_ENTRY_GATE_AND_RESUME_CONTRACT_2026-11-21.md")
t = p.read_text(encoding="utf-8")
defs = re.findall(r"^(?:- |\| )P06-S(\d{3}) ", t, flags=re.M)
nums = [int(x) for x in defs]
print("defined:", len(nums), "min", min(nums), "max", max(nums))
dups = sorted({n for n in nums if nums.count(n) > 1})
gaps = [n for n in range(1, max(nums) + 1) if n not in nums]
print("duplicates:", dups, "gaps:", gaps)
cited = {int(x) for x in re.findall(r"P06-S(\d{3})", t)}
print("cited but undefined:", sorted(cited - set(nums)))
aps = re.findall(r"^- (P06-AP\d\d) ", t, flags=re.M)
us = re.findall(r"^- (P06-U\d\d) ", t, flags=re.M)
rs = re.findall(r"^- (P06-R\d) ", t, flags=re.M)
print("APs", len(aps), "Us", len(us), "Rs", len(rs))
for ref in set(re.findall(r"P06-(AP\d\d|U\d\d|R\d)", t)):
    if f"- P06-{ref} " not in t:
        print("undefined ref:", ref)
# table cell counts
bad = 0
for i, line in enumerate(t.splitlines(), 1):
    if line.startswith("|"):
        cells = line.count("|") - line.count("\\|")
        # header separators and rows of a table must agree with the previous header
    pass
tables = []
cur = None
for i, line in enumerate(t.splitlines(), 1):
    if line.startswith("|"):
        n = len(re.findall(r"(?<!\\)\|", line.replace("`|`", "")))
        if cur is None:
            cur = (i, n)
        elif n != cur[1]:
            print("table cell mismatch at line", i, n, "expected", cur[1]); bad += 1
    else:
        cur = None
print("table problems:", bad)
labels = ("FACT", "UNKNOWN / NOT ESTABLISHED", "INTERPRETATION", "HISTORICAL", "OPEN QUESTION")
for m in re.finditer(r"^- P06-S(\d{3}) (.*)$", t, flags=re.M):
    if not m.group(2).startswith(labels):
        print("label missing:", m.group(1))
for m in re.finditer(r"^\| P06-S(\d{3}) ([^|]*)\|", t, flags=re.M):
    if not m.group(2).startswith(labels):
        print("label missing (table):", m.group(1))
