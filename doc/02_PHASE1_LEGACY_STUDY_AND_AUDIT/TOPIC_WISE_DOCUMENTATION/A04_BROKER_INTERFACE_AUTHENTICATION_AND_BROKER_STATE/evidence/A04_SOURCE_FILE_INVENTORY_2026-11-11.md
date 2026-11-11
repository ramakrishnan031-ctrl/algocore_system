# A04 evidence: the A04 source files at the study baseline

**Status:** DRAFT — evidence for the A04 STUDY, for ChatGPT's review
**Date:** 2026-11-11
**Revision history:** First version, 2026-11-11.
**Purpose and scope:** Identifies the A04 paths of the Master System Investigation Index (entry A04; Appendix A for the three scripts) at the study baseline: size, Git object, SHA-256 and history of the eighteen tracked paths; the related paths that other topics own, which A04 reads at the boundary only; and the A04 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY's inventory sections.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 11-Nov-2026 from the local read-only clone with `git show`, `git rev-parse`, `git ls-tree`, `git log` and `git diff`. Nothing in the clone was written or run. No credential, token or account value is reproduced (Document 08, section 11; D-07).

## 1. The files

The A04 paths are the twelve files under `broker/` that the index names (`zerodha_adapter.py`, `rate_limiter.py`, `order_monitor.py`, `order_state_machine.py`, `token_monitor.py`, `auth_recovery.py`, `product_resolver.py`, `cost_calculator.py`, `slippage_engine.py`, `clock_skew_probe.py`, `position_helpers.py` and `angelone_adapter.py`); `deploy/token_watcher.sh` (the whole file; A13 cites its restart contract), `deploy/zerodha_morning.bat` and `deploy/zerodha_morning.ps1`; and the three scripts that Appendix A assigns to A04 (`scripts/auto_refresh_token.py`, `scripts/copy_token_to_vm.bat` and `scripts/zerodha_login.py`). FACT: all eighteen paths exist at the baseline, and the clone's working tree was clean and at the baseline.

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `broker/zerodha_adapter.py` | 2520 | 115374 | 100644 | `0c85d2d254aa5015bf98072ec5abf88c88cce133` | `395d0d67f03c569ed800a81fa5eb8fca54fd017d15a572f178606c3c70f6d4b3` | 37 | 8f9afe0, 2026-09-10 |
| `broker/rate_limiter.py` | 272 | 12393 | 100644 | `b2f688e7ed84cae02a87e9733a7c177ade944a13` | `52c981fbfe32722fa2869abfa8affb3175764c4af9418d328f72c6cee4f93513` | 4 | 2ad9a31, 2026-05-18 |
| `broker/order_monitor.py` | 1351 | 61408 | 100644 | `c4f4aaa564f1dc342aa31265cc155191a71e5916` | `ee8f59ee15cfced69995f68aab2afe5ded91fd150ddc5f954aad123884796dd7` | 23 | 132e571, 2026-08-01 |
| `broker/order_state_machine.py` | 231 | 10261 | 100644 | `f79418d8072c0e6b722473ecde69af995026b121` | `023c598bde02b2ed4cadbf623214e75ec854bc44474a15f083a27b89bc8e0f52` | 7 | b52ef90, 2026-05-18 |
| `broker/token_monitor.py` | 235 | 9733 | 100644 | `15102f2431e32f3900545a1094406313b919e07d` | `76f40ea25d59ecc22820fe5b00a2bcbfb8ccccd794e46526cd3a166443fe94f3` | 3 | e965589, 2026-07-06 |
| `broker/auth_recovery.py` | 98 | 3896 | 100644 | `d610cee16a1dee20ff6faee71db351e985418048` | `c9d97cd0a881e94b1770543a159979e75003c2663917d8717b782c7c3dc2ac0b` | 1 | 7126034, 2026-06-20 |
| `broker/product_resolver.py` | 175 | 7759 | 100644 | `9db0d6fb7fd7ce11aa2689eecb1d9db7a5b8b575` | `ff37a2d0cf32f5465f4d09bd92a82594a5af2e02173e65ff825457b96fa3ee69` | 2 | d12fe15, 2026-05-18 |
| `broker/cost_calculator.py` | 353 | 15635 | 100644 | `0191b2bb9dad453291306d2d63b3dd663cfa56c2` | `0ab28020e731ef821d8cef3cb2c02da2dc7dbfec50188655cd360df6e2b194f9` | 6 | 1f4509e, 2026-07-17 |
| `broker/slippage_engine.py` | 186 | 7890 | 100644 | `66c7c2bec957af864b4ba93477f5558c5bffc302` | `d9b3bf8a32ae501a82837c83d6c307610db9d9a3530b470401b0d54016095bdf` | 5 | 7f93c2f, 2026-06-16 |
| `broker/clock_skew_probe.py` | 141 | 5620 | 100644 | `749d3905a15f35987fd7c00b4f1b94dbdbfddbfe` | `81684d2f2e01dc2980d5102304d010dc358c5722b5ecfd5303748307ec146e5a` | 1 | a401f81, 2026-04-19 |
| `broker/position_helpers.py` | 101 | 4530 | 100644 | `0e9646da6036f47e63fecf2105308a94d6a413e7` | `3d14f7217d59fa02e2fc7f1d239a2c96ada938b3d03e0ca72b413dac7544497f` | 3 | 7662ace, 2026-08-04 |
| `broker/angelone_adapter.py` | 79 | 2417 | 100644 | `b040ecd19212397612bc8d33b6954693cfbd4116` | `feab4f44869180b30a9f7a21a62017f52474f1682364861eb658ab12533c5aa2` | 1 | 38fa4e9, 2026-05-31 |
| `deploy/token_watcher.sh` | 191 | 7904 | 100644 | `000a3769a2df12292478b197baec1b1c5f16d4cf` | `48f5ddd498d1678139f3b4a12b48bf3063a78866c4f13b80435b414736086a1a` | 6 | 0f722f7, 2026-06-19 |
| `deploy/zerodha_morning.bat` | 93 | 2967 | 100644 | `b5ee09e29b59b9f9ddc614821412bb3c3d2f14a4` | `0cc405928ac3bb19c5b5d152d5164f065edb8076a6fc13c46775a2145159dd1b` | 3 | 4a89cdb, 2026-06-09 |
| `deploy/zerodha_morning.ps1` | 103 | 3588 | 100644 | `0ccce295b989511bf54f49604ee1e524319db686` | `21fd93c0939f1d5c4a0febfa8e96e690232f570ffd42629bd82577c1e0d8acee` | 1 | a9ccaef, 2026-05-31 |
| `scripts/auto_refresh_token.py` | 420 | 18652 | 100644 | `57c71f49d142b5fec7af787d30bd75caa286fa5a` | `08e93229b492602d3926f1dd1958bc6ae3ab4a2fb9c3cbee1395c22ccb6847c8` | 3 | 09ea725, 2026-07-17 |
| `scripts/copy_token_to_vm.bat` | 47 | 1567 | 100644 | `aa32c9268593198d0ccbd6c70f23031e10cc1ef6` | `9bf8efe37085970090a89a13ffeba300d55355811954a2bd4069197ec8d0b706` | 5 | 2f8d35c, 2026-06-18 |
| `scripts/zerodha_login.py` | 288 | 10600 | 100644 | `ff6e8745e5877b33f4d445d0686f67866aea857e` | `06626bb0bb458bb4577667270d85f5807e68585f4848751c02b3da63388748d6` | 4 | dd4f3f4, 2026-07-08 |

## 2. Related paths that other topics own

These paths are read at the boundary only, for the A04 side of a flow; their owners investigate them (index rule 1). Owners are as the index states.

| Path | Bytes | Owner (index) | Why A04 reads it |
|---|---|---|---|
| `broker/__init__.py` | 39 | not listed in the index (one line, a package comment) | package context only; recorded for S1, which completes the repository map; no ownership change is proposed |
| `config/broker_costs.yaml`, `config/broker_limits.yaml` | 1895; 1361 | A02 (`config/`) | the broker cost and limit values whose consumers A04 traces |
| `deploy/systemd/token-watcher.service` | 491 | A17 (`deploy/` systemd units) | the unit that starts `deploy/token_watcher.sh` |
| `scripts/preflight/checks/broker.py` | 16992 | A20 | the pre-flight broker-connectivity check, a caller of the broker interface |
| `scripts/eod_broker_reconcile.py` | 22502 | A12 | a caller of the broker reads |
| `tests/` (broker, token and adapter tests, for example `tests/integration/sim_kite.py`) | — | A19 | intent and behaviour evidence only, never proof of runtime behaviour |
| legacy documents (for example `docs/web_claude/01_module_instructions/module_13_zerodha_adapter.txt`, `docs/broker_integration_audit_2026-06-02.md`) | — | evidence (HISTORICAL; index rule 11) | intent sources for the AUDIT |

Other callers of the broker interface, outside A04's paths, are identified in the STUDY's call-site map and cross-referenced to their owners.

## 3. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21); the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): one of the eighteen A04 paths changed after `7d4970a`; the other seventeen are identical at both commits.

| A04 file | Lines added / removed (`7d4970a` to the baseline) | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `broker/zerodha_adapter.py` | 64 / 2 | `8f9afe0` (2026-09-10 15:36): "feat(adapter): market_protection at the single kite.place_order chokepoint" |

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether this change was ever in force.
