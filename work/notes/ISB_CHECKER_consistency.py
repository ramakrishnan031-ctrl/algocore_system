"""ISB checker: consistency check of the checked file (reads Markdown only; writes nothing)."""
import re, pathlib
F = pathlib.Path('/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md')
D = pathlib.Path('/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT')
t = F.read_text(encoding='utf-8'); lines = t.splitlines()
def row_ids(prefix):
    out = []
    for l in lines:
        m = re.match(r'^\| (%s-\d+)(?: \([^)|]*\))? \|' % prefix, l)
        if m: out.append(m.group(1))
    return out
for pre, lo, hi in (('IS', 501, 625), ('IC', 501, 515), ('CD', 501, 529)):
    ids = row_ids(pre); nums = [int(x.split('-')[1]) for x in ids]; exp = list(range(lo, hi + 1))
    print(pre, len(ids), 'missing', sorted(set(exp) - set(nums)), 'extra', sorted(set(nums) - set(exp)), 'dups', sorted({n for n in nums if nums.count(n) > 1}), 'ordered', nums == exp)
defined = set(row_ids('IS')) | set(row_ids('IC')) | set(row_ids('CD'))
refs = set(re.findall(r'\b((?:IS|IC|CD)-\d{3})\b', t))
print('undefined refs:', sorted(r for r in refs if r not in defined and int(r.split('-')[1]) >= 501))
for x in sorted(set(row_ids('IC')) | set(row_ids('CD'))):
    if len(re.findall(r'\b%s\b' % re.escape(x), t)) < 2: print('not cross-referenced:', x)
parts = {'P01': 'A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md', 'P02': 'A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md',
         'P03': 'A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md', 'P04': 'A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md',
         'P05': 'A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md', 'P06': 'A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_2026-11-26.md',
         'P07': 'A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md'}
pt = {k: (D / 'evidence' / v).read_text(encoding='utf-8') for k, v in parts.items()}
miss = []
for a, b in re.findall(r'(P0\d-S\d{3}) to (P0\d-S\d{3})', t):
    pa, sa = a.split('-S'); pb, sb = b.split('-S')
    for n in range(int(sa), int(sb) + 1):
        sid = '%s-S%03d' % (pa, n)
        if not re.search(r'(^|\W)- %s |\| %s \|' % (sid, sid), pt[pa], re.M): miss.append(sid + '(range)')
for sid in sorted(set(re.findall(r'\b(P0\d-S\d{3})\b', t))):
    if not re.search(r'(^|\W)- %s |\| %s \|' % (sid, sid), pt[sid[:3]], re.M): miss.append(sid)
print('part statements not found:', miss)
study = (D / 'A08_STUDY_2026-11-26.md').read_text(encoding='utf-8')
bad = [x for x in sorted(set(re.findall(r'\b(A08-(?:AP|U|Q)-\d{2})\b', t))) if ('**%s**' % x) not in study]
for a, b in re.findall(r'(A08-AP-\d{2}) to (A08-AP-\d{2})', t):
    bad += ['A08-AP-%02d' % n for n in range(int(a[-2:]), int(b[-2:]) + 1) if ('**A08-AP-%02d**' % n) not in study]
print('STUDY items not defined:', bad)
print('ISB-R:', sorted(set(re.findall(r'\*\*(ISB-R\d)\*\*', t))))
for i, l in enumerate(lines, 1):
    for q in re.findall(r'"([^"]{10,})"', l):
        w = len([x for x in q.split() if re.search(r'\w', x)])
        if w >= 15: print('long quote? L%d (%d words): %s' % (i, w, q[:100]))
