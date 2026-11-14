# A05 STUDY part P02: The pinned kiteconnect 5.1.0 library: the ticker and the client methods A05 uses

**Status:** WORKING DRAFT (helper output; not a project record)
**Baseline:** trading-system-prod-snapshot, branch main, commit 970aabf3c78d777d9d34549e021f7c8e756c7bdb
**Scope:** the published `kiteconnect` 5.1.0 distribution, read as text only (never installed, imported, built or run): its provenance and the legacy pin (section 2); `kiteconnect/ticker.py` in whole (section 3); the `kiteconnect/connect.py` methods that A05 code calls, with `exceptions.py` (section 4); the current Kite Connect v3 documentation pages that bear on those library facts (section 5); a mapping of every A05 call site and the feed's `KiteTicker` use to the library facts (section 6). Library side only: what the legacy callers do with the results belongs to the other A05 parts (P01 feed, P06 historical closure, P07 instrument refresh, P08 daily candles) and to A04 (client construction, rate limiter).
**Prepared:** 14-Nov-2026 (IST), read-only helper for part P02.

## 1. Scope, files read and method

P02-S001. FACT (COMMON_RULES section 2; the direction for this part): every statement below that carries the qualifier "(published kiteconnect 5.1.0 source, <file> L<a> to L<b>)" is a fact about the text of the PUBLISHED 5.1.0 distribution only. It does not establish which package was installed on the legacy machine, what the broker's server sent in the legacy period, or that production ever exercised a path. Twisted and autobahn (the WebSocket and event-loop libraries that `ticker.py` builds on) were not downloaded: what their code does is UNKNOWN / NOT ESTABLISHED, and this part records only what kiteconnect's own source does with them (imports, calls, arguments). `requests`, `six`, `python-dateutil` and `urllib3` were not downloaded either; where a statement depends on how one of them behaves, it is labelled INTERPRETATION with that basis stated, or UNKNOWN / NOT ESTABLISHED.

P02-S002. INTERPRETATION (method; COMMON_RULES section 4): a library code fact is labelled FACT. What a library docstring or comment says is labelled HISTORICAL (a statement of intent inside the source, not proof of behaviour), with the same library qualifier.

**Files read in whole:**
- `/home/claude/a05_ext/kiteconnect_5.1.0_src/kiteconnect/ticker.py` (863 lines).
- `/home/claude/a05_ext/kiteconnect_5.1.0_src/kiteconnect/connect.py` (956 lines; every line read; sections 4.2 to 4.8 cite the methods A05 code calls).
- `/home/claude/a05_ext/kiteconnect_5.1.0_src/kiteconnect/exceptions.py` (80 lines), `__init__.py` (115 lines), `__version__.py` (8 lines; one e-mail line not reproduced).
- `kiteconnect-5.1.0.dist-info/` files `RECORD`, `WHEEL`, `top_level.txt`; `METADATA` (all lines except the two e-mail-bearing lines, which were filtered out and are not reproduced).
- `/home/claude/a05/notes/kiteconnect_5.1.0_provenance.txt`; `/home/claude/a05_ext/pypi_kiteconnect_5.1.0.json` (parsed as data with `python3 -I`).
- Legacy, at `970aabf`: `requirements.txt` (15 lines); `requirements-dev.txt` (27 lines).

**Files read in part (legacy, at `970aabf`, with `git show`, output filtered for identifiers):**
- `data/live_feed.py` L1 to L215, L262 to L600 (the `KiteTicker` call sites and callbacks; P01 owns the file).
- `main.py` L372 to L445 (`_build_kite_client`, `_build_market_data_kite`, `_make_sr_fetch_fn`); L473 to L556 (`_make_paper_quote_provider`, identified as paper-only and not traced); L2920 to L2950 (the feed's construction); L3478 to L3535 (the historical closure's wiring, as boundary evidence only).
- `scripts/fetch_daily_candles.py` L1 to L120, L160 to L300.
- `scripts/refresh_instruments.py` L150 to L215, L285 to L320, L370 to L446.
- `config/system_config.yaml` L736 to L752 (the `live_feed` block, as call-site context only; A02 and P09 own configuration).
- Boundary evidence only (A08 owns these): `sr_detector/fetch.py` L28 to L48, L110 to L137; `sr_detector/models.py` L34 to L43. `core/time_authority.py` L55 to L60, L94 to L101.
- Import lines only: `scripts/fetch_fno_ban.py`, `scripts/find_symbol_aliases.py`, `core/instrument_cache.py`, `core/candle_math.py`, `data/candle_store.py`.

**Project records read (sections cited where used):** A01 RECONCILED TOPIC RECORD (W-24 entry) and A01 AUDIT (item W-24); A04 RECONCILED TOPIC RECORD (handoff row for A05) and A04 AUDIT (items CL-27 and RD-33).

**Commands and search patterns (all read-only):**
- `sha256sum` of the wheel and of each module; a `python3 -I` scratch script that recomputes the RECORD hashes and sizes; a `python3 -I` scratch script that parses the stored PyPI JSON. Scratch scripts are in `/home/claude/a05_tools/scratch/P02/`.
- `git -C /home/claude/repos/legacy show 970aabf:<path>`; `git log` (hashes, dates, subjects) on `requirements.txt`, including `git log -S'kiteconnect=='`.
- `git grep -n -E "KiteConnect\(|KiteTicker\(|historical_data\(|instruments\(|\.quote\(|\.ltp\(|\.ohlc\(" 970aabf -- data/live_feed.py data/candle_store.py core/instrument_cache.py core/candle_math.py scripts/fetch_daily_candles.py scripts/fetch_fno_ban.py scripts/find_symbol_aliases.py scripts/refresh_instruments.py main.py` with the four mandatory exclusion pathspecs.
- A wider sweep of the same files for `kiteconnect`, `set_access_token`, `.subscribe(`, `.unsubscribe(`, `.set_mode(`, `MODE_`, `.connect(`, `.close(`, `stop_retry`, the callback names, `reconnect_max`, `connect_timeout`, `threaded=`, any `kite*.<method>(` call, `.reqsession`, `set_session_expiry_hook` and the kiteconnect exception class names.
- `grep -n` inside the library source for: the bare word `reconnect`; `KEEPALIVE`, `sendPing`, `PING_INTERVAL`; `self.factory`; `reactor.`; `fromtimestamp`, `utc`, `tz`, `timezone`; `retry`, `429`, `sleep`, `rate`, `backoff`; `NetworkException`, `status_code`; `try:`, `except`, `raise`; `sendMessage`, `stopTrying`, `resetDelay`; `_message_code`, `EXCHANGE_MAP[`.
- WebFetch of current Kite Connect v3 documentation pages (section 5).

**Not done (by rule):** nothing in the library or the legacy repository was installed, imported, built, run or tested; no broker or API call was made; no credential, account, token or local-overlay file was opened.

## 2. Provenance of the library text and the legacy pin

P02-S003. FACT (`/home/claude/a05/notes/kiteconnect_5.1.0_provenance.txt`; re-verified with `sha256sum` on 14-Nov-2026, 13:00 IST): the artifact read is `kiteconnect-5.1.0-py3-none-any.whl`, 25214 bytes, SHA-256 `bcfd71703981675e191fbf4f3fe1e2c737edfaafe429ec6eb62c7f98fb27666c`. This equals the wheel's SHA-256 digest in the stored PyPI metadata (`pypi_kiteconnect_5.1.0.json`, release 5.1.0, `packagetype` `bdist_wheel`). It was obtained with `pip download --no-deps --only-binary=:all:` and extracted with Python `zipfile` into its own read-only directory (provenance note, "Method"); nothing was built or installed.

P02-S004. FACT (re-verified 14-Nov-2026, 13:00 IST): the extracted module files, their line counts and SHA-256 values are the same as in the provenance note. Each file's size and hash also match the wheel's own `kiteconnect-5.1.0.dist-info/RECORD` entries (recomputed by the scratch script `rec.py`).

| File | Lines | SHA-256 |
|---|---|---|
| `kiteconnect/__init__.py` | 115 | `a0e4c1273f432b3c2e5603fff2bb415b7353fdabb6c6367f5b39f5cb8d5f475a` |
| `kiteconnect/__version__.py` | 8 | `fb4420a4b89ddb344dc9ecd29bfebe7d24d3fa68dd511ede59006e0822739587` |
| `kiteconnect/connect.py` | 956 | `a4c221a1e3e67963fe1c97fcb103c75d5c6c2a95bc60a8b7a710fe724b3f565c` |
| `kiteconnect/exceptions.py` | 80 | `95028b5e9bad5b07ac87b8f4e5e3b6a36a7c4a001b220d26353748b694840cff` |
| `kiteconnect/ticker.py` | 863 | `5b491b554eb31f419ef8bdc93ae26672f1f6fd162eb6acefa83706eb29f6f87d` |

P02-S005. FACT (stored PyPI JSON, parsed by the scratch script `pypi.py`): release 5.1.0 has two files: the wheel (uploaded 2026-03-27T16:45:44Z) and `kiteconnect-5.1.0.tar.gz` (26281 bytes, SHA-256 `90f75c04c7225dabe8f307661f813eee78179aaa8cb8c27c8ee51a4dcf9b1f84`, uploaded 2026-03-27T16:45:45Z; not read). For both files the `provenance` field is null and `yanked` is false. No build-provenance attestation exists for either file, and none is claimed or implied here: the hash match shows only that the text read is the file PyPI serves for 5.1.0.

P02-S006. FACT (published kiteconnect 5.1.0 source, `kiteconnect-5.1.0.dist-info/METADATA` L2 to L3 and L24 to L32; `__version__.py` L1 and L5): name `kiteconnect`, version `5.1.0`. Declared dependencies: `service_identity>=18.1.0`, `requests>=2.18.4`, `six>=1.11.0`, `pyOpenSSL>=17.5.0`, `python-dateutil>=2.6.1`, `autobahn[twisted]==19.11.2`; `pdoc` only with the extra `doc`; `pywin32` only where `sys_platform == "win32"`. Twisted is not named: it is reached only through autobahn's `twisted` extra, so the wheel pins autobahn exactly but does not pin Twisted. Which Twisted versions autobahn 19.11.2's extra allows is in autobahn's own metadata, which was not read: UNKNOWN / NOT ESTABLISHED.

P02-S007. FACT (published kiteconnect 5.1.0 source, `WHEEL` L1 to L4): generator `setuptools (82.0.1)`, `Root-Is-Purelib: true`, tag `py3-none-any`. HISTORICAL (published kiteconnect 5.1.0 source, `METADATA` L16 to L18): the classifiers name Python 3.5, 3.6 and 3.7 only. FACT (stored PyPI JSON): `requires_python` is null, so the metadata sets no Python version limit.

P02-S008. FACT (`requirements.txt` L8 at `970aabf`, read with `git show`): `kiteconnect==5.1.0`, with the comment "Audit #11: pin; DO NOT upgrade without full regression test" (the comment itself is HISTORICAL). FACT (`requirements.txt` L1 to L15): there is no pin for autobahn, Twisted, `service_identity`, `pyOpenSSL`, `six` or `python-dateutil`; `requests==2.33.1` is pinned at L9. FACT (`requirements-dev.txt` L5, L26 to L27): it includes `-r requirements.txt` and adds only `pytest==9.0.3` and `pytest-cov==7.1.0`. FACT (`git ls-tree -r --name-only 970aabf`): no constraints file, lock file, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile` or Poetry file is tracked; the only other requirements file is `ops_dashboard/backend/requirements.txt`, whose L2 comment says kiteconnect must not appear there. FACT (case-insensitive `git grep` for `twisted|autobahn` over the whole tree at `970aabf`, with the mandatory exclusions): no tracked file names Twisted or autobahn.

P02-S009. HISTORICAL (`git log` on `requirements.txt`; `git log -S'kiteconnect=='`): the exact pin `kiteconnect==5.1.0` first appears in commit `7ed3a3b` (2026-04-22, "apply all 14 audit fixes"); the two earlier commits `bcf03b5` (2026-04-17) and `7ac61b3` (2026-04-18) had `kiteconnect>=4.2.0`. The comment on L8 read "Kite SDK API compat" up to `5dc8563` (2026-05-14) and reads "DO NOT upgrade without full regression test" from `e55cb59` (2026-05-31). The PyPI upload of 5.1.0 (2026-03-27) is earlier than the first pin.

P02-S010. INTERPRETATION (basis: P02-S006, P02-S008): the pin fixes the kiteconnect version that `pip install -r requirements.txt` asks for. It does not fix the versions of Twisted, autobahn's other dependencies, `six`, `python-dateutil`, `pyOpenSSL` or `service_identity` (autobahn itself is fixed at 19.11.2 by the wheel's own requirement). Which versions were actually installed on the legacy machine, and whether the installed kiteconnect was this wheel or a build from the sdist, are UNKNOWN / NOT ESTABLISHED: no installed-package listing survives in the repository (P02-S008).
