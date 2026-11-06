# A01 evidence: the A01 source files at the study baseline

**Status:** APPROVED — evidence for the A01 STUDY, approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30)
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04. Approved by Rama on 2026-11-06 with the A01 topic package (Decision Register, D-30): status marked APPROVED; content unchanged.
**Purpose and scope:** Identifies the fifteen A01 paths of the Master System Investigation Index (entry A01; Appendix A for the two scripts) at the study baseline: size, Git object, SHA-256 and history, and the A01 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY, sections 3 and 13.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 04-Nov-2026 from the local read-only clone with `git show`, `git rev-parse`, `git ls-tree`, `git log` and `git diff`. Nothing in the clone was written or run.

## 1. The files

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. All fifteen paths exist at the baseline, and the clone's working tree was clean and at the baseline.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `main.py` | 4293 | 208758 | 100644 | `445fb0d8237a6d535ed00e5eb968c8176efd74f3` | `151e87f38d93f08acc76f38aa03308f0777b55991a83fefee3e842c4d4ef3b42` | 148 | ea0e506, 2026-09-10 |
| `utils/startup_checks.py` | 1692 | 68854 | 100644 | `61ff67676d8230640a2aafb6bd6d75d7a185fbb6` | `416f2d2ec8895ef3eff7b3ab228ead489b4d5826a8293d9a41a66fc1b84b7f02` | 19 | e393b3f, 2026-07-17 |
| `utils/instance_lock.py` | 257 | 10006 | 100644 | `f73345ed4f2fd3ad749a4a4180b45f4387fd0e20` | `b5b1269a66ac3d8dba9ba3356ba960288083ade5d97cbd9e2760178de049e806` | 4 | 65cd7df, 2026-07-17 |
| `utils/holiday_guard.py` | 131 | 4445 | 100644 | `688679256362ffbabf0811af4bce17683832850e` | `4aa127f1e4842c53abc89a0ebfaf9be158350b957b83ba69d9b9362cc0329224` | 4 | 7f93c2f, 2026-06-16 |
| `utils/__init__.py` | 1 | 47 | 100644 | `438c72609e7a1cba62a59d2b8dc4810257ff8f3b` | `cee24671157f19ba4e33ee06c2f6a1dbe93d7301b4258ab128de5ff4e4186c1b` | 1 | bcf03b5, 2026-04-17 |
| `core/time_authority.py` | 395 | 16646 | 100644 | `a29c4f0795b182fea0a2c9297d22075f6a3e6924` | `178bd9fc902d3c474b76a8d7ef9901b0c31159726d4e94c3cf16566ab6a4afd7` | 3 | 618222e, 2026-07-14 |
| `core/market_windows.py` | 333 | 13938 | 100644 | `25625e8cd109c935d014ad357cd6726c75737157` | `3fcbec13d3afc6e30fbaf5908d8e11c30a32996ef5f05763af088ca9678c6a85` | 9 | 7f93c2f, 2026-06-16 |
| `core/events.py` | 365 | 15023 | 100644 | `6511bc40fe74413ff5498a5b90cd47fae34dff82` | `24d144cb3517c9e7afd9fb075747c96a928c8891f1ca6a193282bb097a3a3b9c` | 8 | dfdeec2, 2026-05-19 |
| `core/ids.py` | 124 | 5731 | 100644 | `5e8b17bdd97f7ed37d7b4229e18353cb62ecd2ff` | `c1aa69c80e133541c780bcfad330d96d7b1ba7ea685bdd30a0156422fc193bcf` | 2 | 9ddb632, 2026-05-17 |
| `core/exceptions.py` | 422 | 18013 | 100644 | `1eeac584208493425bef34c4d80b1f78413342e5` | `b8e72ea84f57fab8a4cda21cf333ae9cda271e1349f5a5c3ad989ca18fc2cca5` | 6 | 8812026, 2026-06-23 |
| `core/constants.py` | 42 | 2175 | 100644 | `e99bd77650d98b3257d2c85d702f48ab60f2caf4` | `85cf981f8b728c17a06c41a75622b1ebb7c3f7981211fdfead0dc16ca3119053` | 3 | 07c7fc0, 2026-08-02 |
| `core/account_registry.py` | 360 | 17125 | 100644 | `d2bdc836cc9a04a99d4d179dba4f46e78213c84c` | `14ac701a837e416ff853ffaa9bf94553c92428ec22bd9cfd7a30bafeee777653` | 6 | 42c07f3, 2026-09-09 |
| `core/__init__.py` | 1 | 37 | 100644 | `cfb176a4b18e37df00d23ad457947379fa9793cf` | `39a7897749c14f0aa2f3784e82d105f82ebaf324ace7303d2b208e0219a4951b` | 1 | 1ad8026, 2026-05-13 |
| `scripts/check_tz.sh` | 50 | 2417 | 100755 | `64afd9e7c4fb75b1eaee38d9be78fd1d5d63ff78` | `940d77217a55ad2f310aed0048e4588415839ef3f39d8f634dfa120fb3b7f557` | 1 | 3114326, 2026-06-29 |
| `scripts/ist_now.sh` | 39 | 1761 | 100755 | `32a5d192bb1fd6ba4bcc24b6f429ae1a2ff5a42f` | `4c9dd677367b9c3d98e6180ba705f8988eceea9bf56d13ba27ce137b9d959d8f` | 1 | 3114326, 2026-06-29 |

## 2. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02, 22:48 IST) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02, 23:42 IST) (D-21). `686df1c` is an ancestor of `7d4970a`, and the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): two of the fifteen A01 paths changed after `7d4970a`, by additions only; the other thirteen are identical at both commits.

| Commit | Date (IST) | Subject, as recorded in the commit | A01 file | Lines added (net) |
|---|---|---|---|---|
| `42c07f3` | 2026-09-09 12:46 | feat(registry): AR12/AR12b -- resolve the account tag and credential env names from accounts.csv | `core/account_registry.py` | 115 |
| `1955ae1` | 2026-09-10 15:36 | feat(mis-squareoff): protected MARKET per pass, and the PASS_2 residual gate | `main.py` | 7 |
| `8d27fdb` | 2026-09-10 19:07 | feat(evidence): CHECKPOINT -- wire P1, all five P2 reject paths, and P3 | `main.py` | 15 |
| `ea0e506` | 2026-09-10 20:42 | fix(evidence): CHECKPOINT -- the sentinel reaches the real alert officer, and the observer cannot stop the boot | `main.py` | 28 added, 8 removed |

Where the net change sits at the baseline:

- `main.py`, 42 lines added (no line removed overall), in `_main_locked`: L3248 to L3280, which builds the forward-evidence recorder (`core.evidence_contract.EvidenceRecorder`, owned by A15) and, if that fails, sets it to `None`, logs an error and sends a CRITICAL notification, and startup continues; L3297 and L3622, which pass that recorder to the secondary screener (`SecondaryScreener(...)`, L3281 to L3298; A07) and to the signal processor (`SignalProcessor(...)`, L3575 to L3623; A06); L3369 to L3375, which pass two market-protection percentages from configuration to the MIS auto square-off (`MisAutoSquareoff(...)`, L3359 to L3379; A12).
- `core/account_registry.py`, 115 lines added: L35 (an import) and L247 to L360, the module-level functions `primary_account_tag` (L277), `_read_primary_row` (L302), `reset_primary_account_tag_cache` (L321), `primary_api_key_env` (L347), `primary_api_secret_env` (L352) and `primary_api_key` (L357).

FACT (`git grep` at the baseline): 23 other files name those new functions (22 production Python files and one test file), and all 23 also changed after `7d4970a`. Across the whole repository, 51 files changed between `7d4970a` and the baseline.

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a` (D-21; Document 06, section 4.2).
