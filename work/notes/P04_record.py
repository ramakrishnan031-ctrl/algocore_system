"""P04 writer helper: print one AUDIT record of an algocore_system Markdown file, from its heading
line to the next heading, with wrapped field lines joined. Reads Markdown only; imports nothing
from the legacy system. Usage: python3 -I P04_record.py <file> <heading line number> [max chars per field]"""
import sys

path, start = sys.argv[1], int(sys.argv[2])
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
with open(path, encoding="utf-8") as fh:
    lines = fh.read().split("\n")
out = [lines[start - 1]]
i = start
while i < len(lines):
    ln = lines[i]
    if ln.startswith("#"):
        break
    if ln.startswith("- **") or ln.startswith("|") or not out[-1].strip():
        out.append(ln)
    elif ln.strip() == "":
        out.append("")
    else:
        out[-1] = out[-1] + " " + ln.strip()
    i += 1
print(f"[{path.split('/')[-1]} L{start} to L{i}]")
for o in out:
    print(o[:limit])
