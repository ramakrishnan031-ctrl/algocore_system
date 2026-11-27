"""ISB writer: consistency check of the legacy-half file (reads Markdown only; writes nothing)."""
import re, sys, pathlib
F = pathlib.Path('/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md')
D = pathlib.Path('/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT')
t = F.read_text(encoding='utf-8')
lines = t.splitlines()

def row_ids(prefix):
    ids = []
    for l in lines:
        m = re.match(r'^\| (%s-\d+)(?: \(new\))? \|' % prefix, l)
        if m:
            ids.append(m.group(1))
    return ids

for pre, lo, hi in (('IS', 501, 618), ('IC', 501, 513), ('CD', 501, 528)):
    ids = row_ids(pre)
    nums = [int(x.split('-')[1]) for x in ids]
    exp = list(range(lo, hi + 1))
    dup = sorted({n for n in nums if nums.count(n) > 1})
    print(pre, 'rows:', len(ids), 'expected', len(exp), 'missing', sorted(set(exp) - set(nums)), 'extra', sorted(set(nums) - set(exp)), 'dups', dup, 'ordered', nums == exp)

# references to IC/CD/IS numbers must exist
defined = set(row_ids('IS')) | set(row_ids('IC')) | set(row_ids('CD'))
refs = set(re.findall(r'\b((?:IS|IC|CD)-\d{3})\b', t))
print('undefined refs:', sorted(r for r in refs if r not in defined))
# IC/CD defined but never referenced from a row other than their own
for x in sorted(set(row_ids('IC')) | set(row_ids('CD'))):
    n = len(re.findall(r'\b%s\b' % re.escape(x), t))
    if n < 2:
        print('defined but not cross-referenced:', x)

# part statements exist
parts = {
    'P01': 'A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md',
    'P02': 'A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md',
    'P03': 'A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md',
    'P04': 'A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md',
    'P05': 'A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md',
    'P06': 'A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md',
    'P07': 'A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md',
}
ptext = {k: (D / 'evidence' / v).read_text(encoding='utf-8') for k, v in parts.items()}
missing = []
# expand ranges "Pnn-Saaa to Pnn-Sbbb"
for a, b in re.findall(r'(P0\d-S\d{3}) to (P0\d-S\d{3})', t):
    pa, sa = a.split('-S'); pb, sb = b.split('-S')
    if pa == pb:
        for n in range(int(sa), int(sb) + 1):
            sid = '%s-S%03d' % (pa, n)
            if not re.search(r'\b%s\b' % sid, ptext[pa]):
                missing.append(sid + ' (in range)')
for sid in sorted(set(re.findall(r'\b(P0\d-S\d{3})\b', t))):
    p = sid[:3]
    if not re.search(r'(^|\W)- %s |\| %s \|' % (sid, sid), ptext[p], re.M):
        missing.append(sid)
print('part statements not found as statements:', missing)

study = (D / 'A08_STUDY_2026-11-26.md').read_text(encoding='utf-8')
for kind in ('AP', 'U', 'Q'):
    for x in sorted(set(re.findall(r'\b(A08-%s-\d{2})\b' % kind, t))):
        if ('**%s**' % x) not in study:
            print('STUDY item not defined:', x)
# expand AP ranges
for a, b in re.findall(r'(A08-AP-\d{2}) to (A08-AP-\d{2})', t):
    for n in range(int(a[-2:]), int(b[-2:]) + 1):
        x = 'A08-AP-%02d' % n
        if ('**%s**' % x) not in study:
            print('STUDY item (range) not defined:', x)
print('ISB-R:', sorted(set(re.findall(r'\*\*(ISB-R\d)\*\*', t))))
# quotation length check (double-quoted strings over 14 words)
for i, l in enumerate(lines, 1):
    for q in re.findall(r'"([^"]{10,})"', l):
        w = len(q.split())
        if w >= 15:
            print('long quote L%d (%d words): %s' % (i, w, q[:90]))
