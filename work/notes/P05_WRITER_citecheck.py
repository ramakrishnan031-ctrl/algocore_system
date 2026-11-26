import re, sys
P = '/home/claude/a08/parts/'
mine = open(P + 'A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md', encoding='utf-8').read()
ctx = {
 'P01': open(P + 'A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md', encoding='utf-8').read(),
 'P02': open(P + 'A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md', encoding='utf-8').read(),
 'P03': open(P + 'A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md', encoding='utf-8').read(),
 'P07': open(P + 'A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md', encoding='utf-8').read(),
}
# defined IDs in my file (bullet starts)
defs = re.findall(r'^- (P05-(?:S\d{3}|AP\d{2}|U\d{2}|R\d|X\d{2}))\b', mine, flags=re.M)
print('defined:', len(defs))
for kind in ('S', 'AP', 'U', 'R', 'X'):
    ids = [d for d in defs if re.match(r'P05-' + kind + r'\d', d)]
    nums = [int(re.sub(r'\D', '', d.split('-')[1])) for d in ids]
    ok = nums == list(range(1, len(nums) + 1))
    print(kind, len(ids), 'in order 1..n:', ok, '' if ok else nums)
dup = sorted({d for d in defs if defs.count(d) > 1})
print('duplicates:', dup)
# cited P05 ids exist
cited = set(re.findall(r'P05-(?:S\d{3}|AP\d{2}|U\d{2}|R\d|X\d{2})', mine))
missing = sorted(c for c in cited if c not in defs)
print('cited P05 ids missing a definition:', missing)
# cited ids of other parts exist (as a defined bullet / table statement in that part)
other = sorted(set(re.findall(r'\b(P0[1237]-(?:S\d{3}|AP\d{2}|U\d{2}|R\d|X\d{2}))\b', mine)))
bad = []
for o in other:
    part = o[:3]
    txt = ctx[part]
    if not re.search(r'(^- |^\| |^)' + re.escape(o) + r'\b', txt, flags=re.M) and not re.search(r'\b' + re.escape(o) + r' (FACT|HISTORICAL|INTERPRETATION|UNKNOWN)', txt):
        bad.append(o)
print('other-part ids cited:', len(other), 'not found as definitions:', bad)
# P07 AP-02 etc. (AP-xx form) cited
print('P07 AP forms cited:', sorted(set(re.findall(r'P07 AP-\d\d', mine))))
