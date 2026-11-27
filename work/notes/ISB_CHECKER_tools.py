"""ISB checker helper (read-only). Runs only `git show`, `git blame`, `git log`, `git grep` against the legacy clone
at the baseline; imports no legacy code; writes no file. Output masked for identifier-shaped text.

Usage (python3 -I):
  show  <path|SHORT> [a b]          numbered lines a..b, blame commit (10) + date per line
  dates <path|SHORT> a-b [...]      introducing commits (full hash) and dates per range
  msg   <commit> [...]              commit messages (trailers dropped)
  grep  <pattern> [paths...]        git grep -n -I -i -E with the four exclusions
  row   <ROW-ID> [...]              quote locator + date check for one row of the checked file
  rows  <prefix> <a> <b>            same for a range, e.g. rows IS 501 511
"""
import re, subprocess, sys, pathlib
REPO = '/home/claude/repos/legacy'
BASE = '970aabf3c78d777d9d34549e021f7c8e756c7bdb'
EXCL = [':(exclude)config/accounts.csv', ':(exclude,glob)**/.env*', ':(exclude,glob)**/*.local.yaml',
        ':(exclude,glob)**/*token*.json']
FORBID = re.compile(r'(^|/)(config/accounts\.csv|\.env[^/]*|[^/]*\.local\.yaml|[^/]*token[^/]*\.json)$')
F = pathlib.Path('/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md')
ALLOW = re.compile(r'^(SHA|AES|ISO|RFC|UTF|MD|PEP|ATR|EMA|RSI|ADX|VWAP|SMA|HTTP|FIX)\d+$')
MASKS = [
    (re.compile(r"(?<![A-Za-z0-9])[A-Z]{2,4}\d{3,6}(?![0-9A-Za-z])"), '<ID?>'),
    (re.compile(r"(?<![A-Za-z0-9])[a-z]{2,4}\d{3,6}(?![0-9A-Za-z])"), '<id?>'),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), '<IP?>'),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), '<EMAIL?>'),
    (re.compile(r"(/home/\w+|/Users/\w+|[A-Za-z]:\\\\)"), '<HOMEPATH?>'),
]
SHORT = {
    'INIT': 'sr_detector/__init__.py', 'MODELS': 'sr_detector/models.py', 'PIVOTS': 'sr_detector/pivots.py',
    'ZONES': 'sr_detector/zones.py', 'CONFL': 'sr_detector/confluence.py', 'FLAGS': 'sr_detector/flags.py',
    'DETECT': 'sr_detector/detector.py', 'FETCH': 'sr_detector/fetch.py', 'ZBUILD': 'sr_detector/zone_builder.py',
    'ZCACHE': 'sr_detector/zone_cache.py', 'ZWARM': 'sr_detector/zone_warmer.py', 'RCONF': 'sr_detector/retest_confirm.py',
    'RMON': 'screening/retest_monitor.py', 'SPOT': 'scripts/sr_corp_action_spotcheck.py',
    'BACKFILL': 'scripts/sr_detector_backfill.py', 'EXPORT': 'scripts/sr_level_export.py', 'MAIN': 'main.py',
    'PROC': 'signals/signal_processor.py', 'SYSCFG': 'config/system_config.yaml', 'CFGLOADER': 'core/config_loader.py',
    'AUDITOR': 'core/config_auditor.py', 'EXPECTED': 'config/expected_managers.yaml', 'CRONREG': 'config/cron_registry.yaml',
    'SCHEMA': 'core/schema.sql', 'STORE': 'core/state_store.py', 'EOD': 'orders/eod_squareoff.py',
    'SEXIT': 'orders/structure_exit_manager.py', 'PB01ENTRY': 'v3_chain/pb01_entry.py', 'PATHS': 'PATHS.md',
    'SMAP': 'docs/SYSTEM_MAP.md', 'README': 'README.md', 'CLARIF': 'docs/chatgpt_project_clarification.md',
    'IA': 'docs/audit/integrity_audit_2026.md', 'AUD-05JUL': 'docs/audit/audit_05jul2026.md',
    'FSA-04JUL': 'docs/audit/full_system_audit_04july2026.md', 'V3P0': 'docs/v3/V3_PHASE0_INVESTIGATION_GAP_ANALYSIS.md',
    'V3S5': 'docs/v3/V3_STEP5_RISK_SIZING_GAPMAP.md', 'V3S7': 'docs/v3/V3_STEP7_ENTRY_ENGINE_GAPMAP.md',
    'V3S8': 'docs/v3/V3_STEP8_TRADE_MGMT_GAPMAP.md', 'V3S10': 'docs/v3/V3_STEP10_PIPELINE_PLUMBING_PLAN.md',
    'PREC14': 'docs/audit/pending_reconciliation_14jul2026.md', 'BATCH16': 'docs/audit/batch_classification_16jul2026.md',
    'MP28': 'docs/MASTER_PENDING_28-Jul-2026.txt', 'MP30': 'docs/MASTER_PENDING_30-Jul-2026.md',
    'MP01': 'docs/MASTER_PENDING_01-Aug-2026.md', 'DRP0': 'docs/audit/daily_report_redesign_phase0_data_audit_30jun2026.md',
    'EVC': 'docs/audit/effect_verification_contract_01aug2026.md', 'EPB': 'docs/audit/effect_telemetry_phaseB_build_01aug2026.md',
    'DBDP': 'docs/audit/deploy_behaviour_delta_prediction_14jul2026.md', 'STOPPROC': 'docs/audit/STOP_PROCEDURE_05-Aug-2026.md',
    'REPCON': 'docs/report_data_contract.md',
}


def mask(s):
    for rx, rep in MASKS:
        def f(m):
            t = m.group(0)
            if rep in ('<ID?>', '<id?>') and ALLOW.match(t.upper()):
                return t
            if rep == '<IP?>' and t in ('0.0.0.0', '127.0.0.1'):
                return t
            return rep
        s = rx.sub(f, s)
    return s


def git(*args):
    return subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True).stdout


def resolve(p):
    p = SHORT.get(p, p)
    if FORBID.search(p):
        sys.exit('refused: forbidden path pattern')
    return p


_tc = {}


def text(path):
    path = resolve(path)
    if path not in _tc:
        _tc[path] = git('show', f'{BASE}:{path}')
    return _tc[path]


_dc = {}


def cdate(h):
    if h not in _dc:
        out = git('log', '-1', '--format=%H %as', h).split()
        _dc[h] = out[1] if len(out) > 1 else '?'
    return _dc[h]


_bc = {}


def blame_map(path):
    path = resolve(path)
    if path not in _bc:
        out = git('blame', '-s', '-l', BASE, '--', path)
        m = {}
        for line in out.splitlines():
            parts = line.split(None, 2)
            if len(parts) < 2:
                continue
            h = parts[0].lstrip('^')
            mm = re.match(r'(\d+)\)', parts[1])
            if mm:
                m[int(mm.group(1))] = h
        _bc[path] = m
    return _bc[path]


def cmd_show(path, a=None, b=None):
    lines = text(path).splitlines()
    bm = blame_map(path)
    a = int(a) if a else 1
    b = int(b) if b else len(lines)
    for i in range(a, min(b, len(lines)) + 1):
        h = bm.get(i, '?')
        print(f'{i:5d} [{h[:10]} {cdate(h) if h != "?" else "?"}] {mask(lines[i-1])}')


def range_commits(path, a, b):
    bm = blame_map(path)
    c = {}
    for i in range(a, b + 1):
        h = bm.get(i)
        if h:
            c.setdefault(h, []).append(i)
    return c


def cmd_dates(path, *specs):
    for spec in specs:
        a, _, b = spec.partition('-')
        a = int(a); b = int(b or a)
        print(f'{path} L{a} to L{b}:')
        for h, ls in sorted(range_commits(path, a, b).items(), key=lambda kv: cdate(kv[0])):
            print(f'   {h} {cdate(h)}  {len(ls)} lines  (L{ls[0]}..L{ls[-1]})')


def cmd_msg(*commits):
    for c in commits:
        out = git('log', '-1', '--format=%H %as%n%B', c)
        keep = [l for l in out.splitlines() if not re.match(r'^(Co-Authored-By|Signed-off-by|Claude-Session|Generated with)', l, re.I)]
        print(mask('\n'.join(keep)))
        print('-' * 60)


def cmd_grep(pattern, *paths):
    args = ['grep', '-n', '-I', '-i', '-E', pattern, BASE, '--'] + (list(paths) if paths else ['.']) + EXCL
    for line in git(*args).splitlines():
        print(mask(line.replace(BASE + ':', '', 1)))


# ---------- row checking ----------
TOK = re.compile(r'(?P<short>\b(?:%s)\b)|`(?P<bt>[\w./-]+\.(?:py|md|yaml|txt|sql|cron))`|(?P<commit>\b[0-9a-f]{40}\b)'
                 r'|(?P<rng>\bL(?P<a>\d+)(?: to L(?P<b>\d+))?)' % '|'.join(re.escape(k) for k in sorted(SHORT, key=len, reverse=True)))


def parse_cites(cell):
    """Return list of (path, a, b) and commit hashes, in order of appearance."""
    cur = None
    cites, commits = [], []
    for m in TOK.finditer(cell):
        if m.group('short'):
            cur = SHORT[m.group('short')]
        elif m.group('bt'):
            p = m.group('bt')
            if '/' not in p:
                cand = 'tests/unit/' + p
                if text(cand):
                    p = cand
            cur = p
        elif m.group('commit'):
            commits.append(m.group('commit'))
        elif m.group('rng') and cur:
            a = int(m.group('a')); b = int(m.group('b') or a)
            cites.append((cur, a, b))
    return cites, commits


def norm_line(l):
    l = l.strip()
    l = re.sub(r'^(?:#+|--+|//+|"""|\'\'\'|>+)\s?', '', l)
    l = l.replace('"""', ' ')
    return l


def norm(s):
    s = s.replace('`', '').replace('**', '')
    return re.sub(r'\s+', ' ', s).strip()


def corpus(path):
    lines = text(path).splitlines()
    pieces, starts = [], []
    pos = 0
    for i, l in enumerate(lines, 1):
        n = norm(norm_line(l))
        starts.append((pos, i))
        pieces.append(n)
        pos += len(n) + 1
    return ' '.join(pieces), starts


_cc = {}


def find(path, q):
    if path not in _cc:
        _cc[path] = corpus(path)
    s, starts = _cc[path]
    out = []
    qn = norm(q)
    segs = [x.strip() for x in re.split(r'\s*(?:\.\.\.|…)\s*', qn) if x.strip()]
    if not segs:
        return out
    start = 0
    while True:
        k = s.find(segs[0], start)
        if k < 0:
            break
        ok = True
        j = k + len(segs[0])
        for sg in segs[1:]:
            k2 = s.find(sg, j)
            if k2 < 0 or k2 - j > 800:
                ok = False
                break
            j = k2 + len(sg)
        if ok:
            ln = max(i for p, i in starts if p <= k)
            ln2 = max(i for p, i in starts if p <= j - 1)
            out.append((ln, ln2))
        start = k + 1
    return out


def msg_text(c):
    out = git('log', '-1', '--format=%B', c)
    return norm(out)


def quotes(cell):
    # straight double quotes; nested quotes give fragments
    return [q.strip() for q in re.findall(r'"([^"\n]{3,})"', cell) if len(q.strip()) >= 3]


def row_cells(rid):
    for l in F.read_text(encoding='utf-8').splitlines():
        if re.match(r'^\| %s(?: \(new\))? \|' % re.escape(rid), l):
            return [c.strip() for c in l.strip().strip('|').split(' | ')]
    return None


def check_row(rid, show_dates=True):
    cells = row_cells(rid)
    if not cells:
        print(rid, 'NOT FOUND'); return
    whole = ' | '.join(cells[1:])
    cites, commits = parse_cites(whole if not rid.startswith('IS') else cells[1] + ' | ' + cells[4])
    if rid.startswith('IS'):
        cites_src, commits_src = parse_cites(cells[1])
    else:
        cites_src, commits_src = cites, commits
    paths = []
    for p, a, b in cites:
        if p not in paths:
            paths.append(p)
    print('=' * 100)
    print(rid, '| cites:', '; '.join(f'{SHORT_INV.get(p, p)} L{a}-{b}' for p, a, b in cites_src), '| commits:', ' '.join(c[:10] for c in commits_src))
    qcells = cells[1:] if not rid.startswith('IS') else [cells[1], cells[4]]
    for q in quotes(' | '.join(qcells)):
        hits = []
        for p in paths:
            for a2, b2 in find(p, q):
                inr = any(pp == p and a <= a2 and b2 <= b for pp, a, b in cites)
                hits.append((p, a2, b2, inr))
        mhits = [c for c in commits if norm(q) in msg_text(c)] if commits else []
        if not hits and not mhits:
            # wider search: all short-name files
            wide = []
            for p in SHORT.values():
                if p in paths:
                    continue
                for a2, b2 in find(p, q):
                    wide.append((p, a2, b2))
            print(f'  NOTFOUND "{mask(q)[:110]}"' + (f'  (elsewhere: {[(SHORT_INV.get(p,p), a, b) for p, a, b in wide[:4]]})' if wide else ''))
        else:
            ok = any(h[3] for h in hits) or bool(mhits)
            tag = 'ok' if ok else 'OUT'
            locs = ', '.join(f'{SHORT_INV.get(p, p)}:{a2}' + (f'-{b2}' if b2 != a2 else '') + ('' if inr else '!') for p, a2, b2, inr in hits[:5])
            if mhits:
                locs += (', ' if locs else '') + 'msg ' + ' '.join(c[:8] for c in mhits)
            print(f'  {tag:3s} "{mask(q)[:90]}" -> {locs}')
    if show_dates and rid.startswith('IS'):
        listed = set(re.findall(r'\b[0-9a-f]{40}\b', cells[2]))
        found = {}
        for p, a, b in cites_src:
            for h, ls in range_commits(p, a, b).items():
                found.setdefault(h, []).append(f'{SHORT_INV.get(p, p)} L{ls[0]}..{ls[-1]}({len(ls)})')
        for h in sorted(found, key=cdate):
            print(f'  blame {h[:10]} {cdate(h)} {"listed" if h in listed else "NOT-LISTED"}: {"; ".join(found[h])[:150]}')
        for h in listed - set(found) - set(commits_src):
            print(f'  date-cell commit {h[:10]} {cdate(h)} not among blame of cited ranges')


SHORT_INV = {v: k for k, v in SHORT.items()}

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'show':
        cmd_show(*sys.argv[2:5])
    elif cmd == 'dates':
        cmd_dates(sys.argv[2], *sys.argv[3:])
    elif cmd == 'msg':
        cmd_msg(*sys.argv[2:])
    elif cmd == 'grep':
        cmd_grep(sys.argv[2], *sys.argv[3:])
    elif cmd == 'row':
        for r in sys.argv[2:]:
            check_row(r)
    elif cmd == 'rows':
        pre, a, b = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        for n in range(a, b + 1):
            check_row(f'{pre}-{n}')
