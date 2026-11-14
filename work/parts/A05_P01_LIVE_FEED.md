# A05 STUDY part P01: The live feed and tick intake

**Status:** WORKING DRAFT (helper output; not a project record)

**Baseline:** trading-system-prod-snapshot, branch main, commit 970aabf3c78d777d9d34549e021f7c8e756c7bdb

**Scope:** `data/live_feed.py` in whole (L1 to L790); the feed wiring in `main.py` only (credential-variable names, construction, tick dispatcher, reconnect callback, start order, shutdown, other readers); every other non-test user of the feed object; the configuration keys the feed uses or could use; the pinned `kiteconnect` 5.1.0 interface points that `LiveFeedManager` calls (library internals: see P02); feed tests and legacy feed documents (HISTORICAL); the A05 side of inherited handoffs A01 C37, B-36, W-24, C14, C15; A04 CL-09, CL-27; A02 K-30. Live only.

## 1. Scope, files read and method

P01-S001. FACT (method): every legacy statement below cites path and line(s) at baseline `970aabf`. The local clone's HEAD equals `970aabf` (checked with `git rev-parse HEAD`), so the helper `gg.sh` (which greps HEAD) reads the baseline. Legacy files were read only with `git show 970aabf:<path>` (copied to the P01 scratch folder for line-numbered reading), `git grep -n -E ... 970aabf` with the mandatory exclusion pathspecs, and `git log` (hashes and dates only). Nothing legacy was run, imported, built or tested. No broker, API or network call was made.

P01-S002. FACT (files read in whole): `data/live_feed.py` L1 to L790.

P01-S003. FACT (files read in part): `main.py` L40, L66, L70, L657 to L684, L1599 to L1612, L1770 to L1800, L2193 (function head), L2318 to L2330, L2520 to L2584, L2900 to L3010, L3060 to L3082, L3910 to L3960, L4050 to L4086, L4240 to L4293; `orders/order_placer.py` L582, L652 to L653, L1107, L1201, L2825 (function head), L2905 to L2913, L3330 to L3340, L3361 to L3424, L3431 to L3460, L4041; `orders/shadow_tracker.py` L17, L108, L123, L139, L221 to L249; `core/state_store.py` L285 to L312; `core/market_windows.py` L128 to L152; `core/time_authority.py` L55 to L60, L94 to L101; `core/config_loader.py` L1816 to L1821, L2018 to L2028; `config/system_config.yaml` L736 to L753; `config/expected_managers.yaml` L200 to L222; `capital/kill_switch.py` L563, L618 to L632; `scripts/healthcheck_server.py` L100 to L125; `scripts/preflight/checks/engine.py` L1 to L40; `ops_dashboard/backend/services/capacity.py` L120 to L130, L290 to L300. Pinned library (text only): `/home/claude/a05_ext/kiteconnect_5.1.0_src/kiteconnect/ticker.py` L1 to L28, L40 to L66, L138 to L160, L204 to L215, L375 to L470, L472 to L491, L496 to L700; `__version__.py` L5. Further reads for tests, documents and project records are listed in the sections that use them.

P01-S004. FACT (search patterns used, all with the mandatory exclusions): `live_feed|LiveFeedManager|_ticker_thread_id|tick_age_seconds|reconnect_count`; `_live_feed\b|live_feed\.[a-z_]+|checkpoint\(`; `max_reconnect_attempts|reconnect_backoff_(base|max)_seconds|tick_stale_threshold|watchdog_check_interval|subscription_batch_size|reconnect_delay_sec`; `system\.live_feed|cfg\.live_feed|config\.live_feed`; `_add_to_exit_retry\(|_on_ltp_tick_for_retry`; `class MarketWindows|def is_market_open|def is_entry_allowed`; `def soft_kill`; in `main.py` only: `live_feed|LiveFeedManager|_tick_dispatcher|tick_age_seconds|reconnect_count|set_notifier|is_connected\(|access_token|api_key`.

P01-S005. FACT (method, library): the pinned library statements are about the PUBLISHED `kiteconnect` 5.1.0 source only (`__version__.py` L5 reads "5.1.0"). They do not establish which package ran on the legacy machine. Twisted and autobahn source were not available: their behaviour is UNKNOWN / NOT ESTABLISHED. The library's packet parsing, reconnect algorithm and threading are P02's work; this part writes "library behaviour: see P02" for them.

P01-S006. FACT (method, history): `data/live_feed.py` was last changed at `970aabf` by commit `37336bc` (2026-08-09); `git log` lists 17 commits touching the file up to the baseline. Commit history is context only.
