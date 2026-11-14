# A05 — STUDY: Market data, instruments and external reference data

**Status:** DRAFT — the STUDY of topic A05 (Document 04, section 4, step 4), for ChatGPT's review (step 5)
**Date:** [DATE]
**Revision history:** First version, [DATE].
**Purpose and scope:** The factual study of how the legacy system obtains and normalises market data and reference data: the live feed and its tick intake; the construction of live one-minute candles; the candle calculations of `core/candle_math.py`; historical candle access from the trading process; the instrument cache and the instrument master it loads; the refresh of the instrument master from its external sources and the alias tool; the daily candles script and the F&O ban-list script; the configuration they read; the producers and consumers of every market-data artefact and the storage handoffs; the 33 items that earlier topics handed to A05; and the market-data claims of the existing technical records, checked against the code, at the fixed study baseline. It records what the code does; it does not compare the code with intended behaviour, which is the AUDIT's work.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read from the local read-only clone on [DATES]; nothing in it was written or run. The published `kiteconnect` 5.1.0 wheel, read as data only (Rama's decision G of 14-Nov-2026; provenance in the evidence file listed in section 20).
**Related documents:** Documents 04, 06, 07, 08 and 10; the Master System Investigation Index (entry A05, coverage item 4, Appendix A); the Decision Register, D-07, D-12, D-17, D-21, D-23 to D-25, D-28 and D-30 to D-33; ChatGPT's A05 investigation direction of 14-Nov-2026 and its corrected direction of the same day (not kept as files, D-17); the A01 to A04 RECONCILED TOPIC RECORDS; the Open Issues Register; the A05 evidence files listed in section 20.

## 1. Purpose, scope, exclusions and fixed baseline

### 1.1 Purpose

This STUDY establishes, from the code at the fixed baseline, how the legacy system acquires, normalises, stores and hands on market data, instrument data and external reference data (Document 08, section 3, coverage item 4). It answers the questions of ChatGPT's A05 investigation direction, as corrected on 14-Nov-2026 (section 1.9), and records A05's side of the 33 items that the closed topics handed to it (section 16).

### 1.2 Scope and paths

The A05 paths of the Master System Investigation Index (entry A05 and Appendix A): `data/live_feed.py`, `data/candle_store.py`, `core/instrument_cache.py`, `core/candle_math.py` (the candle construction and calculation boundary), the historical-data integration call sites in `main.py`, and four scripts, `scripts/fetch_daily_candles.py`, `scripts/fetch_fno_ban.py`, `scripts/find_symbol_aliases.py` and `scripts/refresh_instruments.py`. Their sizes, Git objects and histories are in the source file inventory (evidence, `A05_SOURCE_FILE_INVENTORY_2026-11-14.md`).

Boundaries decided by Rama on 14-Nov-2026 on ChatGPT's recommendations, without any change to the index (the Topic Completion Register, entry A05):

- `core/candle_math.py` (decision B): A05 studies its functions, their inputs, outputs, candle contract, calculations, edge cases and actual callers; A08 and A18 keep the use and technical meaning of their own calculations. That `resample()` has no non-test caller is a code fact; no intent or production use is inferred from it.
- Historical candle access (decision C): A05 studies the `main.py` historical-data call, the client and limiter boundary, the returned data contract and the timestamps; `sr_detector/fetch.py` and `sr_detector/models.py` are read only as boundary evidence for the row-to-Candle contract (A08 keeps them).
- The other `historical_data` scripts (decision D) stay with their owners; A05 records the boundary only.
- A03 U-25 (decision E) is carried as an A08-owned pointer only.
- The 33 inherited items (decision A) keep their original owners, IDs, classifications, statuses and treatments; A05 records its own side only (section 16).

### 1.3 Exclusions

- Paper-only branches (Document 08, section 2): marked "paper-only" where met, not traced.
- Other topics' paths: `main.py` as a file (A01); configuration sources, schemas and precedence (A02); database schemas, persistence, connections, storage format and write discipline (A03); the broker adapter, authentication and the broker-wide rate limiter (A04); the alias consumer (A06); technical-analysis use and `sr_detector/` (A08); the downstream consumers of ticks, candles and instrument data (A09, A10, A11, A18); data-quality telemetry and reports (A15); schedule declarations and the invocation map (A16); deployment and installed packages (A17); pre-flight checks (A20). For each, only the interface fact that A05's side needs is recorded.
- Runtime behaviour without surviving evidence (section 1.6).
- Credential values, tokens, account identifiers, environment and local-overlay values (D-07; section 1.10). A03 G-19 is cited by ID only.

### 1.4 Fixed baseline

trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Decision Register, D-21). The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` and `7d4970a26991fd40774023f5293a00556228e14b` (both 2026-09-02); the baseline is 32 commits after `7d4970a` (section 1.8).

### 1.5 Method

[METHOD: read-only clone and commands; twelve parts by read-only helpers, at most two at a time (decision F), each drafted by one helper and checked statement by statement and corrected by a separate helper; working drafts backed up to the temporary branch `wip/a05-fieldwork` after each section (Rama's standing go-ahead of 14-Nov-2026 for backup pushes; never merged into `main`); the published `kiteconnect` 5.1.0 wheel read as data only (decision G); current vendor documentation read as current external context only; the assembled STUDY checked independently against the evidence and the code.]

### 1.6 Runtime evidence limit

Both legacy machines were terminated, and no database, log, crontab, installed unit, environment file or `data_store/` file survives (reported by Rama, not independently verified; Document 06, section 4.2; Source Inventory, SRC-50). `config/instruments.csv`, the instrument master that the trading process loads, is not tracked in the repository (`.gitignore` L35 to L40). No tick, candle, ban-list row, refresh output or heartbeat of the legacy period is available. Every statement about what ran, what was received, what was built or what was written in production is therefore UNKNOWN / NOT ESTABLISHED, and a schedule, unit, import, test, docstring or comment is not taken as proof that a path ran.

### 1.7 Labels

FACT, UNKNOWN / NOT ESTABLISHED, INTERPRETATION, HISTORICAL, KNOWN DEFECT and OPEN QUESTION (Document 04, section 6). A statement drawn from the published `kiteconnect` 5.1.0 source is a FACT about that published source only: it does not establish which package was installed on the legacy machine, what the broker's server sent in the legacy period, or that production exercised a path. Current vendor documentation is labelled current external context, with the date it was read; it is not a fact about the legacy period.

### 1.8 Changes after the last recorded deployment (D-21)

FACT (`git diff 7d4970a 970aabf`): two of the nine A05 paths changed after `7d4970a`. `scripts/fetch_daily_candles.py` changed in `b6df768` (2026-09-09 12:47 IST, 3 lines added and 2 removed: the broker API-key environment variable resolved per account instead of by a literal name). `main.py` changed in three commits on 2026-09-10 (42 lines added), none at an A05 call site (the source file inventory, section 5). UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether the `fetch_daily_candles.py` change was ever in force.

### 1.9 Where the direction's questions are answered

[TABLE]

### 1.10 Security restriction

No credential, token, account identifier, environment or overlay value, personal name other than the Project Owner's, IP address, e-mail address, key fingerprint or absolute legacy machine path is written in this STUDY or its evidence (D-07; Document 08, section 11). Credential variables appear by name only, as configuration. Where a legacy line carries an account identifier (the usage line of `scripts/refresh_instruments.py`'s docstring, the `refresh_instruments` command in `config/cron_registry.yaml`, a version of `scripts/fetch_daily_candles.py` before `b6df768`), it is written as `<ACCOUNT_ID>` or not reproduced. A03 G-19 is cited by ID only. No credential or security issue, alert or register entry is made (D-07).
