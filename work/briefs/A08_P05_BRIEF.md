# A08 STUDY — Part P05 brief (writer): the corporate-action spot-check and the level-export scripts

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P05-S001` onwards.
Output file: `/home/claude/a08/parts/A08_SPOTCHECK_AND_EXPORT_SCRIPTS_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/P05_WRITER_PROGRESS.md`.
Context parts (checked; cite by statement ID, do not edit): P01, P02, P03 and P07 in `/home/claude/a08/parts/`.

## SECURITY (re-read COMMON brief section 3 before starting)

Both scripts construct or use a broker client. Record ONLY the interface: which module/function constructs the client,
which configuration or file LOCATIONS and variable NAMES it reads (names as configuration only), and which client
methods it calls. Never open, read, derive, check or discuss any credential value, its validity, history or exposure;
never open `config/accounts.csv`, `.env*`, `*.local.yaml`, `*token*.json`. Items A04 CL-11, CL-15, A04-05, CL-12 and
AU-05 are recorded at the interface only. Never run either script.

## Scope (study in full)

- `scripts/sr_corp_action_spotcheck.py` (102 lines): `_build_kite`, `_token_for`, `main` — purpose (the docstring's
  corporate-action/split-adjustment check), arguments, inputs (symbols, dates, the instrument lookup), the broker calls
  made (interface), what it compares and prints/writes, exit codes, failure behaviour, the manual command line in its
  docstring (L18; describe it, do not copy any machine path); whether any record of a run, or of its result, exists in
  the repository (git grep in docs/records; HISTORICAL if found; otherwise UNKNOWN). For the external fact of how Kite
  Connect historical candles treat corporate actions, cite the official Kite Connect documentation (date read) as
  current external context only.
- `scripts/sr_level_export.py` (203 lines): `flatten_analysis`, `rows_to_csv`, `export_levels`,
  `_make_real_analyze_fn`, `main` — arguments, inputs, the analysis function it builds (imports from `main` at L137,
  `load_all(str(ROOT / "config"))` at L139, `InstrumentCache(str(...))` at L141 — read the signatures of `load_all`
  and `InstrumentCache.__init__` at the baseline and establish BY READING THE CODE ONLY which line would fail first and
  with what exception, or whether that cannot be established without running it (then UNKNOWN); A01 C38b records L141,
  A02 and A05 record L139 — record the facts, do not reclassify), the clock it uses (P01-S137: a naive 15:30), the CSV
  columns, output location, failure behaviour; its relation to `intraday_anchors_enabled` (`config/system_config.yaml`
  L542 comment) and `docs/SYSTEM_MAP.md` L233.
- Declared invocations: neither script has a schedule (A08 inventory section 3); record any other reference by git grep.

## Inherited items

Answer A08's side of every item, open issue and Owner-field record whose PRIMARY part is P05 in P07 section 7 (final:
7 items — A01 C38b, A02 K-02, A04 CL-11, CL-15, RL-06, A05 HA-07, XC-03 —, 4 open issues A04-05, A04-28, A05-32,
A05-54, records CL-12 and AU-05), and record P05's side where P05 is SECONDARY (including N2's corporate-action check
and the export script's L139). Never change any item's classification, treatment or status.

## Intent sources

Docstrings/comments; tests as stated expectations (`tests/unit/test_sr_level_export.py` and others by git grep);
legacy documents; git history (HISTORICAL).

## Sections (after section 1, Method)

2. The two scripts: identity and declared purpose
3. `sr_corp_action_spotcheck.py`: inputs, broker interface (security rules), comparison, output, failures
4. Whether a spot-check run or result is recorded anywhere (facts; HISTORICAL or UNKNOWN)
5. `sr_level_export.py`: the analysis function and where it stops (L137, L139, L141 — by reading only)
6. `sr_level_export.py`: export, columns, clock, output, failures
7. Declared invocations and references
8. Inherited items: P05's primary items, then its secondary items
9. Stated intent: docstrings, comments, tests, documents, history
10. Points for the AUDIT
11. UNKNOWN / NOT ESTABLISHED items
12. Questions about intent for Rama
13. Cross-references
