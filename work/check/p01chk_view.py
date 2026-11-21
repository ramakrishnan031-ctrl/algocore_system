# P01 checker's read-only viewer (prints record lines through the identifier mask; writes nothing)
import re, sys
D='/home/claude/algocore_system/doc/'
T=D+'02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/'
R=D+'00_PROJECT_CONTROL/04_PROJECT_REGISTERS/'
F={'TCR':R+'TOPIC_COMPLETION_REGISTER_2026-11-04.md','AFR':R+'AUDIT_FINDINGS_REGISTER_2026-11-06.md',
'OIR':R+'OPEN_ISSUES_REGISTER_2026-11-05.md','DR':R+'DECISION_REGISTER_2026-11-04.md',
'A01R':T+'A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/A01_RECONCILED_TOPIC_RECORD_2026-11-06.md',
'A01A':T+'A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/A01_AUDIT_2026-11-05.md',
'A02R':T+'A02_CONFIGURATION_AND_EFFECTIVE_SETTINGS/A02_RECONCILED_TOPIC_RECORD_2026-11-09.md',
'A02A':T+'A02_CONFIGURATION_AND_EFFECTIVE_SETTINGS/A02_AUDIT_2026-11-08.md',
'A03R':T+'A03_DATABASE_PERSISTENCE_MIGRATIONS_AND_BACKUPS/A03_RECONCILED_TOPIC_RECORD_2026-11-11.md',
'A03A':T+'A03_DATABASE_PERSISTENCE_MIGRATIONS_AND_BACKUPS/A03_AUDIT_2026-11-10.md',
'A04R':T+'A04_BROKER_INTERFACE_AUTHENTICATION_AND_BROKER_STATE/A04_RECONCILED_TOPIC_RECORD_2026-11-14.md',
'A04A':T+'A04_BROKER_INTERFACE_AUTHENTICATION_AND_BROKER_STATE/A04_AUDIT_2026-11-13.md',
'A05R':T+'A05_MARKET_DATA_INSTRUMENTS_AND_EXTERNAL_REFERENCE_DATA/A05_RECONCILED_TOPIC_RECORD_2026-11-17.md',
'A05A':T+'A05_MARKET_DATA_INSTRUMENTS_AND_EXTERNAL_REFERENCE_DATA/A05_AUDIT_2026-11-15.md',
'A06R':T+'A06_SIGNAL_INTAKE_AND_WEBHOOK_LIFECYCLE/A06_RECONCILED_TOPIC_RECORD_2026-11-20.md',
'A06A':T+'A06_SIGNAL_INTAKE_AND_WEBHOOK_LIFECYCLE/A06_AUDIT_2026-11-18.md',
'INV':T+'A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/evidence/A07_SOURCE_FILE_INVENTORY_2026-11-20.md'}
pats=[r"(?<![A-Za-z0-9])[A-Za-z]{2,4}\d{3,6}(?![0-9A-Za-z])",r"\b(?:\d{1,3}\.){3}\d{1,3}\b",r"[\w.+-]+@[\w-]+\.[\w.]+",r"(/home/\w+|/Users/\w+)"]
ALLOW=re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$')
def mask(s):
    for p in pats: s=re.sub(p,lambda m: m.group(0) if ALLOW.match(m.group(0).upper()) else '[M]',s)
    return s
def lines(k): return open(F[k],encoding='utf-8').read().split('\n')
if __name__=='__main__':
    # usage: view.py KEY a[-b] [width] ; or KEY /regex/ [width]
    k=sys.argv[1]; spec=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 600
    L=lines(k)
    if spec.startswith('/'):
        rx=re.compile(spec.strip('/'))
        for i,l in enumerate(L,1):
            if rx.search(l): print(f"{i}: {mask(l)[:w]}")
    else:
        for part in spec.split(','):
            a,_,b=part.partition('-'); a=int(a); b=int(b or a)
            for i in range(a,b+1): print(f"{i}: {mask(L[i-1])[:w]}")
