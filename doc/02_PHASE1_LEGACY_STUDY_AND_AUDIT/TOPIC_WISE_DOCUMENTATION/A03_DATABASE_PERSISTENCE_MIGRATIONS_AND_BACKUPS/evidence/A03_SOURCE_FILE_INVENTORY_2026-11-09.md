# A03 evidence: the A03 source files at the study baseline

**Status:** DRAFT — evidence for the A03 STUDY, for ChatGPT's review
**Date:** 2026-11-09
**Revision history:** First version, 2026-11-09.
**Purpose and scope:** Identifies the A03 paths of the Master System Investigation Index (entry A03; Appendix A for the six scripts) at the study baseline: size, Git object, SHA-256 and history of the eleven tracked paths; the two runtime persistence paths, which are not tracked; and the A03 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY's inventory sections.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 09-Nov-2026 from the local read-only clone with `git show`, `git rev-parse`, `git ls-tree`, `git log` and `git diff`. Nothing in the clone was written or run.

## 1. The files

The A03 paths are `core/state_store.py`, `core/schema.sql`, `core/analytics_schema.sql`, `core/db_connect.py` and `core/migrations.py`; the six scripts that Appendix A assigns to A03 (`scripts/backup_evidence.py`, `scripts/backup_restore_drill.py`, `scripts/backup_retention.py`, `scripts/db_retention.py`, `scripts/output_retention.py` and `scripts/wal_checkpoint.py`); and the `data_store/` and `logs/` persistence paths, which are runtime paths named in configuration, not tracked folders (section 2). FACT: all eleven tracked paths exist at the baseline, and the clone's working tree was clean and at the baseline.

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. "Last change" is the last of those commits, with its author date.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `core/state_store.py` | 3355 | 153466 | 100644 | `11866117801b9329773a1be605448faef3c96f8d` | `ec0825fca164278a828c5e3fed90d15cb7c73183f76f3c3342c6396aac6cd326` | 92 | 6f00b4d, 2026-08-28 |
| `core/schema.sql` | 1654 | 104053 | 100644 | `b46d7489f6ec5e31149dd68957f3b9e45270571e` | `9a393cc239a23ebb6faf2251d06b2df06513a540fc399ebc0659a68bdb2ae69a` | 45 | e39655a, 2026-08-23 |
| `core/analytics_schema.sql` | 90 | 5370 | 100644 | `57deb055f4db78d0c016505971a0ce4be040d7a2` | `ba50f59fcf42242ad0faefcf71396df522db09dfde2d64f54868b0111d4a6bbd` | 1 | f172171, 2026-06-14 |
| `core/db_connect.py` | 137 | 5265 | 100644 | `a0f776fef2caf56a1a2e533dfb2ffb436792b543` | `6697067cdbaa13f98c926fea7491ca7cae2d7c266df92e5cce70753e46fdb386` | 2 | d3499b9, 2026-07-15 |
| `core/migrations.py` | 444 | 21663 | 100644 | `cc39e811e48a9eec823c20b70d343278a6b33eef` | `c7bcd53ca10c4361f22cb80fff9dde54a86d00147161cd043fe9d9a4fa58e288` | 13 | 77b8b04, 2026-07-26 |
| `scripts/backup_evidence.py` | 143 | 6091 | 100644 | `031cbe80dc0758ec239bb2d6b30b33681ec4cb80` | `e7e0081dd0acb20b2495317a7af131fbb81e03bf6b5f9d338d4ebd81099018e8` | 2 | 4608b83, 2026-09-10 |
| `scripts/backup_restore_drill.py` | 377 | 11374 | 100644 | `fe12a5efcb8a8a5a6c72be00549b009fed8227a5` | `37ed7c2bdbe4cdb59790ba6b344b9dd96cd258b7953e64ab26c28fc80ecc7dfb` | 3 | f172171, 2026-06-14 |
| `scripts/backup_retention.py` | 310 | 13840 | 100644 | `1b541332c3ec0e8416ec6439eefeb23e3417df9b` | `5bb981b49843a5aefe31e2d01d4292ce190a7b87bce049d2b02303412537856a` | 2 | c42e329, 2026-07-24 |
| `scripts/db_retention.py` | 230 | 8564 | 100644 | `3de2dded7d813a3848dce555941f15ba5ac333f4` | `6363d59f5cf9bfad53d2e475e46357777ef90ce14f26b056498381996a574def` | 3 | 991f5c3, 2026-06-16 |
| `scripts/output_retention.py` | 315 | 13800 | 100644 | `e11baf33fb49e8abbafceb2e15dc94d1f5cb9f21` | `439c14954489e2b2859e45862aa5b6bfa1e45cb9c80f4cec5f4b46a2f995db60` | 4 | e1952e4, 2026-09-11 |
| `scripts/wal_checkpoint.py` | 70 | 2390 | 100644 | `3a6d603b7cf100a6b5273a6ee1120cb633dae016` | `2c6489e30e5512c3459c5bdf1d838b3b6a1a7a76f0d171f3733f60177601cd1c` | 3 | 09ea725, 2026-07-17 |

## 2. The runtime persistence paths

FACT: at the baseline no file is tracked under `data_store/` or `logs/` (`git ls-tree -r`), and neither is an entry of the repository's top-level tree. `.gitignore` lists `*.db`, `*.db-journal`, `*.db-shm`, `*.db-wal` and `data_store/` (L13 to L17) and `logs/` (L20); it is a legacy project file, read as HISTORICAL (index rule 11).

The paths that configuration and code actually give for these folders, and their writers and readers, are traced in the STUDY. What the folders held on either VM is UNKNOWN / NOT ESTABLISHED: the VMs' databases, logs and files do not survive (Source Inventory, SRC-50; Document 06, section 4.2).

## 3. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21); the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): two of the eleven tracked A03 paths changed after `7d4970a`; the other nine are identical at both commits. `scripts/backup_evidence.py` did not exist at `7d4970a`: it was created after it.

| A03 file | Lines added / removed (`7d4970a` to the baseline) | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `scripts/backup_evidence.py` | 143 / 0 (created) | `28ec9df` (2026-09-10 19:07): "feat(evidence): CHECKPOINT -- retention exclusion, backup script, cron entry", which created the file; `4608b83` (2026-09-10 21:00): "fix(backup): CHECKPOINT -- the evidence backup is append-only-safe and atomic, and says what it protects" |
| `scripts/output_retention.py` | 10 / 0 | `28ec9df` (2026-09-10 19:07): as above; `e1952e4` (2026-09-11 01:45): "docs(backup): CHECKPOINT -- the evidence backup is labelled SAME-DISK wherever it is described" |

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether this code was ever in force.
