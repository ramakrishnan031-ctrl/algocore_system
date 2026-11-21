# P10 helper (read-only): for legacy documents with A07 token hits, print dates, hit count and the first hit lines,
# masked. Usage: p10_doc_scan.py <start> <end> [maxlines] [width]. Reads p10_doc_hits.txt. Nothing is run.
import re, subprocess, sys
PAT = r'strategy_will_trade|strategies/control|strategies\.control|STRATEGY_CONTROL|taxonomy|secondary_screener|SecondaryScreener|ScreeningResult|hard_gate|HardGate|v3_hardgate|gate_rr|gate_htf|gate_extreme|gate_confirm|gate_pullback|quality_scorer|QualityScorer|min_pass_score|scoring_weights|entry_gate|EntryGate|gate_state|pullback_wait|GATE_WAITING|GATE_RELEASED|step_executor|StepExecutor|step_timeout|strategy_direction|direction_registry|build_direction_map|compute_strategy_metrics|strategy_metrics|PAPER_ONLY|strategy_registry_officer|strategy_status|force_intraday_only|trade_type|mis_filter|screener|Screener|screening/'
masks = [re.compile(r"(?<![A-Za-z0-9])[A-Za-z]{2,4}\d{3,6}(?![0-9A-Za-z])"), re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
         re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), re.compile(r"(/home/\w+|/Users/\w+|[A-Za-z]:\\)")]
ALLOW = re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$', re.I)
def mask(s):
    for i, rx in enumerate(masks):
        s = rx.sub(lambda m: m.group(0) if (i == 0 and ALLOW.match(m.group(0))) else '<M>', s)
    return s
rows = [l.rsplit(':', 1) for l in open('/home/claude/a07/status/p10_doc_hits.txt').read().split('\n') if l]
a, b = int(sys.argv[1]), int(sys.argv[2]); k = int(sys.argv[3]) if len(sys.argv) > 3 else 3; w = int(sys.argv[4]) if len(sys.argv) > 4 else 150
G = ['git', '-C', '/home/claude/repos/legacy']
for i, (f, n) in enumerate(rows[a-1:b], a):
    dates = subprocess.run(G + ['log', '--format=%ad', '--date=short', '970aabf', '--', f], capture_output=True, text=True).stdout.split()
    txt = subprocess.run(G + ['show', f'970aabf:{f}'], capture_output=True, text=True).stdout.splitlines()
    hits = [(j, l) for j, l in enumerate(txt, 1) if re.search(PAT, l)]
    print(f'#{i} {f} | {n} hits | {len(txt)} lines | commits {len(dates)} first {dates[-1] if dates else "?"} last {dates[0] if dates else "?"}')
    for j, l in hits[:k]: print(f'   L{j}: {mask(l.strip())[:w]}')
