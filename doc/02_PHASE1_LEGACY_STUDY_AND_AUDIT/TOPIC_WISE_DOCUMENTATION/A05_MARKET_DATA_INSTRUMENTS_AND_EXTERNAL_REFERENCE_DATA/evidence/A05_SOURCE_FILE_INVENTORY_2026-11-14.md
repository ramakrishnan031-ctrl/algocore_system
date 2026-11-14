# A05 evidence: the A05 source files at the study baseline

**Status:** DRAFT — evidence for the A05 STUDY, for ChatGPT's review
**Date:** 2026-11-14
**Revision history:** First version, 2026-11-14.
**Purpose and scope:** Identifies the A05 paths of the Master System Investigation Index (entry A05; Appendix A for the four scripts) at the study baseline: size, Git object, SHA-256 and history of the nine paths; the A05 call sites in `main.py`, which A01 owns as a file (index rule 8); the declared invocations of the four scripts, as declarations only; the related paths that other topics own, which A05 reads at the boundary only (Rama's decisions B, C and D of 14-Nov-2026); and the A05 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY's inventory sections.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 14-Nov-2026 from the local read-only clone with `git show`, `git ls-tree`, `git log` and `git diff`. Nothing in the clone was written or run. No credential, token, account identifier or machine path is reproduced (Document 08, section 11; D-07); where a declaration carries an account argument, it is written as `<ACCOUNT_ID>`.

## 1. The files

The A05 paths are `data/live_feed.py`, `data/candle_store.py`, `core/instrument_cache.py` and `core/candle_math.py`; the historical-data integration call sites in `main.py` (section 2); and the four scripts that Appendix A assigns to A05 (`scripts/fetch_daily_candles.py`, `scripts/fetch_fno_ban.py`, `scripts/find_symbol_aliases.py` and `scripts/refresh_instruments.py`). FACT: all nine paths exist at the baseline, and the clone's working tree was clean and at the baseline.

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date. `main.py` is listed for identification only: A05 studies its call sites, not the file (index rule 8).

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `data/live_feed.py` | 790 | 34774 | 100644 | `10ebd00ee728c449c6df4dcc5e576a92f3361e10` | `92873573d0c8a253368beb7f34382e54cd3cb82228b7c1755bd6eaa650003acd` | 17 | 37336bc, 2026-08-09 |
| `data/candle_store.py` | 368 | 15247 | 100644 | `f44a831760e62c9d34d4ffc6d420434b0acebf4c` | `5d9278bfe1395b140d1ca110f2a5fa4a27c11b3fea82e4b2bca98dd664b996b0` | 8 | beb8278, 2026-07-06 |
| `core/instrument_cache.py` | 297 | 12293 | 100644 | `2bff50f7657fd9600e99d3663791e4d134f01d08` | `a4ead5941f082b92903d6c96802daae0af52a1f4094206a66c8500f750e53fda` | 2 | f08b485, 2026-05-17 |
| `core/candle_math.py` | 456 | 21275 | 100644 | `57e69c5973ae29a04633bce90537448c7b3778f0` | `6de3e05d1dc0a74e9e1da52b28fe6f18869dcb2cac7950c569c88d784976d3e5` | 2 | 3c85512, 2026-07-13 |
| `main.py` (A05 call sites only) | 4293 | 208758 | 100644 | `445fb0d8237a6d535ed00e5eb968c8176efd74f3` | `151e87f38d93f08acc76f38aa03308f0777b55991a83fefee3e842c4d4ef3b42` | 148 | ea0e506, 2026-09-10 |
| `scripts/fetch_daily_candles.py` | 346 | 13950 | 100644 | `4a149615dc48ad1342f5b406d4728728631dd7c8` | `9f6a41dfb85a88815eb4a9ccb1027adaf2f6ff874e8ce5dfcae4bec87da724f8` | 13 | b6df768, 2026-09-09 |
| `scripts/fetch_fno_ban.py` | 378 | 14028 | 100644 | `8416cd9c71b17b2cb949b559ed6321156f1622fe` | `28cb1aa942bd2a7621bc007c5555d270ca8010f33c5e171a1996e182e6ed030b` | 6 | 5057425, 2026-06-22 |
| `scripts/find_symbol_aliases.py` | 109 | 3657 | 100644 | `24258c1ef2a157b267b5bd2ee7ee144d15cc3c03` | `b05140a3cff701ceea5e7486ac2b7f46d065b4a12af58a1207f88d5b6922ba71` | 1 | 4fcf984, 2026-05-07 |
| `scripts/refresh_instruments.py` | 446 | 17598 | 100644 | `2002a24b1e7dbf1ae585df220272739dc1aba6fd` | `6556858b17851e8b4e379605edb5bda4ef64559db81b3d91e08d9c665dcff823` | 5 | c3c1242, 2026-06-21 |

## 2. The A05 call sites in `main.py`

FACT, at the baseline (line numbers of `main.py` at `970aabf`). The STUDY traces each one; this table only locates them.

| Lines | What is there |
|---|---|
| L64 | `from core.instrument_cache import InstrumentCache` |
| L393 to L419 | `_build_market_data_kite`: the handle used for read-only historical data (A01 B-11) |
| L421 to L438 | `_make_sr_fetch_fn`: the only `historical_data` call in `main.py` (L432), after `rate_limiter.acquire("historical")` (L431); returns an empty list when there is no handle (L429 to L430) |
| L1788, L1792 | shutdown: `live_feed.disconnect()`, `candle_store.stop()` |
| L2441 | `InstrumentCache.load(config_dir / "instruments.csv")`, in the instrument-master pre-load (A01 C9) |
| L2518 | the instrument cache wired into the adapter (FIX-181 comment) |
| L2908 | sector lookup through the instrument cache |
| L2927 | `LiveFeedManager(` construction |
| L2940 | `CandleStore(` construction |
| L2964, L2971 | `_tick_dispatcher` and `live_feed.register_callback(_tick_dispatcher)` |
| L2992 to L2993 | `live_feed.set_on_reconnect_callback(...)` (candle store and smart target reconnect marks) |
| L3223 | the known-symbol set built from `instrument_cache.all_rows()` |
| L3479 to L3487 | the historical fetch closure built when any of six features is enabled |
| L3494, L3519, L3559, L3678, L3728, L3774 | its consumers: `build_sr_detector` and five `OhlcFetcher` instances (A08, A11 and A18 own their use) |
| L3921 to L3947 | start order: `candle_store.start()` before `live_feed.connect()` (L3947) |

## 3. Declared invocations of the four scripts

These are declarations in the repository, not evidence that a job was installed, ran or completed (Document 06, section 4.2; index rule 12). A16 owns the schedule declarations; A05 owns the scripts' functional logic.

| Script | `deploy/cron/trading-system.cron` | `config/cron_registry.yaml` | Appendix A |
|---|---|---|---|
| `scripts/fetch_fno_ban.py` | L67: `35 8 * * 1-5` | L279 to L280: 08:35 Mon-Fri | cron: 08:35 Mon-Fri |
| `scripts/refresh_instruments.py` | L73: `0 9 * * 1-5` | L307 to L308: 09:00 Mon-Fri, with an `--account <ACCOUNT_ID>` argument | cron: 09:00 Mon-Fri |
| `scripts/fetch_daily_candles.py` | L82: `40 15 * * 1-5` | L360 to L361: 15:40 Mon-Fri | cron: 15:40 Mon-Fri |
| `scripts/find_symbol_aliases.py` | not named | not named | — |

FACT: `config/instruments.csv`, the file `refresh_instruments.py` writes and `InstrumentCache.load` reads, is not tracked; `.gitignore` L35 to L40 states that it is regenerated on the VM daily by `refresh_instruments.py`. UNKNOWN / NOT ESTABLISHED: its deployed content.

## 4. Related paths that other topics own

These paths are read at the boundary only, for the A05 side of a flow; their owners investigate them (index rule 1; Rama's decisions B, C and D of 14-Nov-2026). Owners are as the index states.

| Path | Bytes | Owner (index) | Why A05 reads it |
|---|---|---|---|
| `data/__init__.py` | 0 | S1 (empty package marker) | package context only |
| `config/reference_data/` (18 tracked files), `config/index_universe.yaml`, `config/symbol_aliases.yaml`, `config/system_config.yaml` | 209571 (folder); 1688; 393; 55901 | A02 (`config/`) | the inputs and settings A05 code reads; `symbol_aliases.yaml` is the alias tool's target (its consumer is A06) |
| `sr_detector/fetch.py`, `sr_detector/models.py` | 6709; 8872 | A08 | boundary evidence for the historical row-to-Candle contract only (decision C) |
| `scripts/forward_shadow_record.py`; `scripts/gemini_data_integrity_check.py`, `scripts/reconstruct_excursions.py`; `scripts/sr_corp_action_spotcheck.py` | 15232; 13008, 24912; 3560 | A18; A15; A08 | other `historical_data` callers: boundary only (decision D) |
| `core/daily_stats.py` | 3446 | A15 | a `core/candle_math.py` importer (decision B) |
| `orders/order_placer.py` | 219497 | A10 | the only non-test caller of `live_feed.subscribe` (exit-retry path) |
| `reports/daily_report.py` | 84776 | A15 | reader of the candle CSV that `fetch_daily_candles.py` writes |
| `scripts/preflight/checks/broker.py` | 16992 | A20 | launches `refresh_instruments.py` as a pre-flight fix |
| `deploy/cron/trading-system.cron`, `config/cron_registry.yaml` | 15842; 27116 | A16 | the declared invocations (section 3) |
| `requirements.txt` | 1343 | A17 | the `kiteconnect` pin (L8: `kiteconnect==5.1.0`) |
| `.gitignore` | 2632 | historical source (index rule 11) | the untracked `config/instruments.csv` (section 3) |
| `tests/` (feed, candle, instrument and script tests) | — | A19 | intent and behaviour evidence only, never proof of runtime behaviour |
| legacy documents under `docs/` | — | evidence (HISTORICAL; index rule 11) | intent sources for the AUDIT |

The pinned `kiteconnect` 5.1.0 distribution, read from PyPI as data only under Rama's decision G of 14-Nov-2026, is external context for library-implementation facts; its provenance is recorded in the STUDY's evidence, not here.

## 5. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21); the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): two of the nine paths changed after `7d4970a`; the other seven are identical at both commits.

| A05 path | Lines added / removed (`7d4970a` to the baseline) | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `scripts/fetch_daily_candles.py` | 3 / 2 | `b6df768` (2026-09-09 12:47): "fix(scripts): resolve the broker api_key env var per account, not by literal name" |
| `main.py` | 42 / 0 | `1955ae1` (2026-09-10 15:36), `8d27fdb` (2026-09-10 19:07), `ea0e506` (2026-09-10 20:42); the added lines (L3248 to L3280, L3297, L3369 to L3375, L3622 at the baseline) wire the evidence recorder and a units comment; none is an A05 call site of section 2 |

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether the `fetch_daily_candles.py` change was ever in force.
