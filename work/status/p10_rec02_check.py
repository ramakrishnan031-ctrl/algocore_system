# P10 helper (read-only): check the line anchors of the A07 entries of the legacy technical record 02 against the
# baseline 970aabf. Prints, per entry and field, each anchor and the baseline line content (masked). No legacy code is run.
import re, subprocess, sys
sys.path.insert(0, '/home/claude/a07/status')
REC = '/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/02_REPOSITORY_AND_FILE_MAP.md'
ENTRIES = [('core/strategy_direction.py',513,528),('screening/__init__.py',798,811),('screening/entry_gate.py',812,829),
 ('screening/hard_gate.py',830,846),('screening/quality_scorer.py',847,863),('screening/secondary_screener.py',883,902),
 ('screening/step_executor.py',903,919),('strategies/__init__.py',990,1003),('strategies/control.py',1004,1020),
 ('strategies/taxonomy.py',1056,1072),('scripts/compute_strategy_metrics.py',2841,2859),
 ('scripts/strategy_registry_officer.py',3398,3416),('scripts/strategy_status.py',3417,3433)]
rec = open(REC, encoding='utf-8').read().splitlines()
def mask(s):
    s = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", '<IP>', s)
    s = re.sub(r"(/home/\w+|/Users/\w+)", '<PATH>', s)
    return s
only = sys.argv[1] if len(sys.argv) > 1 else None
mode = sys.argv[2] if len(sys.argv) > 2 else 'sym'
for path, a, b in ENTRIES:
    if only and only not in path: continue
    src = subprocess.run(['git','-C','/home/claude/repos/legacy','show',f'970aabf:{path}'],capture_output=True,text=True).stdout.splitlines()
    print(f'===== {path} (record L{a}-L{b}); baseline lines {len(src)}')
    for rl in range(a, b+1):
        line = rec[rl-1]
        m = re.match(r'- \*\*(.+?):\*\*', line)
        field = m.group(1) if m else ('header' if rl < a+4 else 'purpose')
        if mode == 'sym' and field in ('Key symbols','Config keys read','DB tables'):
            for name, n in re.findall(r'`([^`]+)` \(L(\d+)\)', line):
                n = int(n); tok = name.split('.')[-1]
                txt = src[n-1] if 0 < n <= len(src) else '<NO LINE>'
                ok = tok in txt
                print(f'  [{field}] L{rl} {name} @L{n}: {"OK " if ok else "MISS"} | {mask(txt.strip())[:150]}')
        elif mode == 'nums' and field not in ('Key symbols','Config keys read','DB tables','Imported by (0)'):
            # every bare number or range in parentheses / after 'line(s)' / 'at'
            for mm in re.finditer(r'(?:\(|lines? |at |, )(\d{1,3})(?:[-–](\d{1,3}))?(?=[),; ])', line):
                n1 = int(mm.group(1)); n2 = int(mm.group(2)) if mm.group(2) else n1
                if n1 > len(src) or n1 == 0: continue
                ctx = line[max(0, mm.start()-70):mm.start()].replace('\n',' ')
                print(f'  [{field}] L{rl} ...{ctx[-70:]} -> {n1}{"-"+str(n2) if n2!=n1 else ""}')
                for n in range(n1, min(n2, n1+3)+1):
                    print(f'        {n}: {mask(src[n-1].strip())[:140]}')
