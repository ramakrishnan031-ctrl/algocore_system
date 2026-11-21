# P10 helper (read-only): for each bare line number cited in the non-symbol fields of an A07 entry of record 02,
# test whether an identifier from the record's phrase before the number appears on the cited baseline line(s) (+-1).
# Prints only the anchors with no identifier match, plus counts. Nothing from the legacy repository is run.
import re, subprocess, sys
REC = '/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/02_REPOSITORY_AND_FILE_MAP.md'
ENTRIES = [('core/strategy_direction.py',513,528),('screening/__init__.py',798,811),('screening/entry_gate.py',812,829),
 ('screening/hard_gate.py',830,846),('screening/quality_scorer.py',847,863),('screening/secondary_screener.py',883,902),
 ('screening/step_executor.py',903,919),('strategies/__init__.py',990,1003),('strategies/control.py',1004,1020),
 ('strategies/taxonomy.py',1056,1072),('scripts/compute_strategy_metrics.py',2841,2859),
 ('scripts/strategy_registry_officer.py',3398,3416),('scripts/strategy_status.py',3417,3433)]
rec = open(REC, encoding='utf-8').read().splitlines()
STOP = set('the and or of to a an in on at by is be it as for with from per via when not no its this that line lines L only one two else then'.split())
tot = miss = 0
show_all = len(sys.argv) > 1 and sys.argv[1] == 'all'
for path, a, b in ENTRIES:
    src = subprocess.run(['git','-C','/home/claude/repos/legacy','show',f'970aabf:{path}'],capture_output=True,text=True).stdout.splitlines()
    for rl in range(a, b+1):
        line = rec[rl-1]
        if re.match(r'- \*\*(Key symbols|Config keys read|DB tables|Log calls by level|Imported by|Imports locally|Third-party)', line): continue
        for mm in re.finditer(r'(?<![\w.:L])(\d{1,3})(?:[-–](\d{1,3}))?(?![\w.%])', line):
            n1 = int(mm.group(1)); n2 = int(mm.group(2)) if mm.group(2) else n1
            pre = line[max(0, mm.start()-60):mm.start()]
            if not re.search(r'(\(|line |lines |at |, |-)\s*$', pre) and not re.search(r'\((?:[\d, -]+)$', pre): continue
            if n1 == 0 or n1 > len(src) or n2 < n1: continue
            if re.search(r'(main\.py|signal_processor\.py|step_executor\'s|its line|\.py):?\s*$', pre): continue
            tot += 1
            words = [w for w in re.findall(r'[A-Za-z_][A-Za-z0-9_]{2,}', pre) if w.lower() not in STOP][-4:]
            window = ' '.join(src[max(0,n1-2):min(len(src), n2+1)])
            hit = any(w in window or w.lower() in window.lower() for w in words)
            if not hit or show_all:
                miss += (not hit)
                print(f'{path} rec L{rl}: ...{pre[-55:]}[{n1}{"-"+str(n2) if n2!=n1 else ""}] words={words}')
                for n in range(n1, min(n2, n1+2)+1): print(f'      {n}: {src[n-1].strip()[:130]}')
print(f'anchors tested {tot}; without identifier match {miss}')
