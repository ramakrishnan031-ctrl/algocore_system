# P10 helper (read-only): for a test file at the baseline, print its docstring head and, for every line naming A07
# code, the enclosing def/class with its line. Tests are read as text only; nothing is imported or run.
import re, subprocess, sys
P = re.compile(r'strategies\.control|strategies\.taxonomy|strategy_direction|screening\.|strategy_will_trade|compute_strategy_metrics|strategy_registry_officer|strategy_status|EntryGate|SecondaryScreener|StepExecutor|QualityScorer|HardGate|hard_gate')
for f in sys.argv[2:]:
    L = subprocess.run(['git','-C','/home/claude/repos/legacy','show',f'970aabf:{f}'],capture_output=True,text=True).stdout.splitlines()
    print(f'=== {f}')
    head = [l for l in L[:int(sys.argv[1])] if l.strip()]
    for l in head: print('   | ' + l.strip()[:150])
    cur = None; seen = set()
    for i, l in enumerate(L, 1):
        m = re.match(r'\s*(async )?def (\w+)|\s*class (\w+)', l)
        if m: cur = (i, m.group(2) or m.group(3))
        if P.search(l):
            key = cur
            print(f'   L{i} [{cur[1] if cur else "-"}@L{cur[0] if cur else 0}] {l.strip()[:140]}')
