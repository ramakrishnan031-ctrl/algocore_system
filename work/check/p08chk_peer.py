"""P08 checker helper: print the text of peer statements (P02 to P07) cited in the P08 file,
including the IDs inside "Pxx-Snnn to Pxx-Smmm" ranges, so each citation can be compared.
Reads only files under /home/claude/a07/parts/. Writes no file.
Run: python3 -I -B /home/claude/a07/check/p08chk_peer.py <part prefix e.g. P02> [maxchars]
"""
import re
import sys
from pathlib import Path

PARTS = Path("/home/claude/a07/parts")
P08 = PARTS / "A07_CONFIGURATION_KEYS_AND_EFFECTIVE_VALUES_2026-11-21.md"
FILES = {
    "P02": "A07_STRATEGY_CONTROL_TAXONOMY_AND_DIRECTION_REGISTRY_2026-11-21.md",
    "P03": "A07_SECONDARY_SCREENER_ORCHESTRATION_AND_RESULT_2026-11-21.md",
    "P04": "A07_STEP_EXECUTOR_AND_THE_TEN_STEPS_2026-11-21.md",
    "P05": "A07_QUALITY_SCORER_HARD_GATE_AND_V3_PLAYBOOK_GATES_2026-11-21.md",
    "P06": "A07_ENTRY_GATE_AND_RESUME_CONTRACT_2026-11-21.md",
    "P07": "A07_STRATEGY_SCRIPTS_2026-11-21.md",
}


def cited(text):
    ids = set(re.findall(r"P0[2-7]-(?:S\d{3}|AP\d+|U\d+)", text))
    for a, b in re.findall(r"(P0[2-7]-S\d{3}) to (P0[2-7]-S\d{3})", text):
        if a[:3] == b[:3]:
            for n in range(int(a[-3:]), int(b[-3:]) + 1):
                ids.add(f"{a[:3]}-S{n:03d}")
    return ids


def statements(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*(?:-\s*|\|\s*)?\**(P0[2-7]-(?:S\d{3}|AP\d+|U\d+))\**[\s.:—-]", line)
        if m and m.group(1) not in out:
            out[m.group(1)] = line.strip()
    return out


def main():
    part = sys.argv[1]
    maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    ids = sorted(i for i in cited(P08.read_text(encoding="utf-8")) if i.startswith(part))
    st = statements(PARTS / FILES[part])
    missing = [i for i in ids if i not in st]
    print(f"{part}: {len(ids)} cited (with ranges); missing in file: {missing}")
    for i in ids:
        if i in st:
            print(f"\n## {i}: {st[i][:maxc]}")


if __name__ == "__main__":
    main()
