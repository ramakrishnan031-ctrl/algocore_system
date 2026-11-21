# P10 helper (read-only): compare record 02's "Imported by" and "Imports locally" lists for the 13 A07 entries with
# git grep at the baseline (static text search of import statements; the four exclusions applied). Nothing is run.
import re, subprocess
REC='/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/00_EXISTING_LEGACY_TECHNICAL_RECORDS/02_REPOSITORY_AND_FILE_MAP.md'
L=open(REC,encoding='utf-8').read().splitlines()
ENT={'core.strategy_direction':513,'screening':798,'screening.entry_gate':812,'screening.hard_gate':830,'screening.quality_scorer':847,
 'screening.secondary_screener':883,'screening.step_executor':903,'strategies':990,'strategies.control':1004,'strategies.taxonomy':1056,
 'scripts.compute_strategy_metrics':2841,'scripts.strategy_registry_officer':3398,'scripts.strategy_status':3417}
EX=[':(exclude)config/accounts.csv',':(exclude,glob)**/.env*',':(exclude,glob)**/*.local.yaml',':(exclude,glob)**/*token*.json']
def grep(p):
    r=subprocess.run(['git','-C','/home/claude/repos/legacy','grep','-l','-E',p,'970aabf','--','*.py']+EX,capture_output=True,text=True).stdout.split()
    return sorted(x.split(':',1)[1] for x in r)
def mod(path):
    m=path[:-3].replace('/','.')
    return m[:-9] if m.endswith('.__init__') else m
for name,start in ENT.items():
    blk=L[start-1:start+18]
    ib=next(x for x in blk if x.startswith('- **Imported by'))
    il=next((x for x in blk if x.startswith('- **Imports locally')),'')
    rec_ib=re.findall(r'`([^`]+)`',ib); more=re.search(r'\(\+(\d+)\)',ib)
    esc=re.escape(name)
    if name in ('screening','strategies'):
        pat=rf'^\s*(from {esc} import|import {esc}(\s|$|,))'
    else:
        parent,leaf=name.rsplit('.',1)
        pat=rf'^\s*(from {esc} import|import {esc}\b|from {re.escape(parent)} import .*\b{leaf}\b)'
    files=[f for f in grep(pat) if mod(f)!=name]
    got=sorted(set(mod(f) for f in files))
    recn=re.search(r'Imported by \((\d+)\)',ib).group(1)
    miss=[x for x in rec_ib if x not in got]; extra=[x for x in got if x not in rec_ib]
    print(f'== {name}: record count {recn} (+{more.group(1) if more else 0} not listed); baseline importers {len(got)}')
    if miss: print('   in record, not found at baseline:', miss)
    if extra and not more: print('   at baseline, not in record:', extra)
    if extra and more: print(f'   at baseline beyond the listed names ({len(extra)}; record says +{more.group(1)}):', extra)
    print('   record imports locally:', re.findall(r'`([^`]+)`',il))
