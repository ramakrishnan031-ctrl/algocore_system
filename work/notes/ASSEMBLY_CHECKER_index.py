# H16 (assembly checker): build an index of every part statement / AP / U / R / X ID with its label and full text.
# Read-only on the parts; writes only notes/ASSEMBLY_CHECKER_index.json. Run with python3 -I.
import re, json
W = '/home/claude/a08'
PARTS = {'P01': 'A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md',
         'P02': 'A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md',
         'P03': 'A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md',
         'P04': 'A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md',
         'P05': 'A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md',
         'P06': 'A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md',
         'P07': 'A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md'}
START = re.compile(r'^(?:- |\| )?\**(P0[1-7]-(?:S\d{3}|AP\d+|U\d+|R\d+|X\d+))\**(?=[ .|:—-])')
P7AP = re.compile(r'^- \*\*(AP-\d\d)\.')
idx = {}
for p, fn in PARTS.items():
    lines = open(f'{W}/parts/{fn}', encoding='utf-8').read().split('\n')
    # stop at the check log: statements are defined before it
    cur = None
    blank_seen = False
    sec = ''
    for n, l in enumerate(lines, 1):
        if l.startswith('## Check log'):
            sec = 'CHECKLOG'
        if l.startswith('#'):
            if sec != 'CHECKLOG':
                sec = l.strip('# ').strip()
            cur = None
            continue
        if sec == 'CHECKLOG':
            continue
        m = START.match(l)
        m7 = P7AP.match(l) if p == 'P07' else None
        if m or m7:
            i = m.group(1) if m else 'P07 ' + m7.group(1)
            rest = l[m.end():] if m else l[m7.end():]
            lab = rest.strip(' .|*—-')
            labm = re.match(r'((?:FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|OPEN QUESTION|WITHDRAWN)'
                            r'(?:[ ,;]+(?:and |or )?(?:FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|OPEN QUESTION|current external context))*)', lab)
            label = labm.group(1) if labm else ''
            if i in idx:
                idx[i]['dup'] = idx[i].get('dup', 0) + 1
                cur = None
                continue
            idx[i] = {'part': p, 'line': n, 'label': label, 'text': l, 'sec': sec}
            cur = i
            blank_seen = False
        elif cur and l.strip() and (l.startswith('|') or l.startswith('  ') or not blank_seen):
            # continuation: lines directly after the statement, or a table / indented block after a blank line
            idx[cur]['text'] += '\n' + l
            blank_seen = False if not l.startswith('|') and not l.startswith('  ') else blank_seen
        elif not l.strip():
            blank_seen = True
            continue
        else:
            cur = None
        if l.strip(): blank_seen = False
json.dump(idx, open(f'{W}/notes/ASSEMBLY_CHECKER_index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
c = Counter((v['part'], re.sub(r'\d+', '', k.split('-', 1)[1]) if not k.startswith('P07 ') else 'AP') for k, v in idx.items())
for k in sorted(c): print(k, c[k])
print('total', len(idx), 'dups', {k: v['dup'] for k, v in idx.items() if 'dup' in v})
nolab = [k for k, v in idx.items() if not v['label'] and '-S' in k]
print('S without parsed label:', len(nolab), nolab[:40])
