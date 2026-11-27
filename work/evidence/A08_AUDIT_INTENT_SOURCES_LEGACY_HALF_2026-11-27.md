# A08 evidence: intended-behaviour sources for the A08 AUDIT — legacy-side half

**Status:** DRAFT — evidence for the A08 AUDIT (intended-behaviour sources, legacy-side half ISB); not yet checked
**Date:** 2026-11-27
**Revision history:** First version, 2026-11-27.
**Purpose and scope:** The legacy-side half of the inventory of intended-behaviour sources for the A08 AUDIT (technical analysis, S&R and retest context): every legacy source found at the baseline that states or implies the intended behaviour of the sixteen A08 paths and of A08's interfaces — legacy documents, module docstrings and comments in the A08 files, dated labels, log and alert texts, names, configuration comments by key name, wiring and call-site comments in other topics' files (cited for what they state about A08 only), commit messages and the tests that reference A08 code (stated expectations, never run) — by area: all areas; (a) the calculation core (CZ); (b) the candle fetch, the zone builder, the zone cache and the zone warmer (FC); (c) the V1 observer, its flags, the `sr_detector_results` row and the backfill (VO); (d) the V2 retest path and its `continue_from_retest` handoff (RT); (e) the two scripts, the corporate-action spot check and the level export (SC); (f) configuration, wiring and consumers (XW); (g) the tests. With the conflicts between legacy sources (IC-501 onward), the statements that only the code contradicts (CD-501 onward), what could not be established and the draft questions about intent for Rama (ISB-R1 onward). Boundaries as Decision Register D-41, P1 to P5, applied unchanged: other topics' files are cited for what they state about A08 only. It judges no code, decides nothing, answers nothing for Rama and contains no design for the new system.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-27 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced. Project records read (read-only) from algocore_system `main`, commit `20e267d4997986107324f4f1385c96dc89b8b1bf`.
**Counts:** (filled at completion)
**Factual baseline:** the A08 STUDY (`A08_STUDY_2026-11-26.md`, algocore_system commit `20e267d`, DRAFT) and its seven part evidence files and inventory, statement IDs Pnn-Snnn, points A08-AP-nn, unknown items A08-U-nn, draft questions A08-Q-nn.

## 1. Scope and method

### 1.1 Clone checks

### 1.2 What was read

### 1.3 Kinds, dates and labels

### 1.4 Short names

## 2. Sources by area

### 2.1 All areas

### 2.2 Area (a): the calculation core (CZ)

### 2.3 Area (b): the candle fetch, the zone builder, the zone cache and the zone warmer (FC)

### 2.4 Area (c): the V1 observer, its flags, the `sr_detector_results` row and the backfill (VO)

### 2.5 Area (d): the V2 retest path and the `continue_from_retest` handoff (RT)

### 2.6 Area (e): the corporate-action spot check and the level export (SC)

### 2.7 Area (f): configuration, wiring and consumers (XW)

### 2.8 Area (g): the tests, as stated expectations (A19's)

## 3. Conflicts between sources

## 4. Statements that only the code contradicts

## 5. Could not establish

## 6. Questions about intent for Rama
