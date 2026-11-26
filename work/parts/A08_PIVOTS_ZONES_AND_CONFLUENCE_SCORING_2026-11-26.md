# A08 evidence: pivots, zones and confluence scoring (the calculation core)
**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26.
**Purpose and scope:** Part P01 of the A08 STUDY fieldwork. It records in full what the four calculation-core files of the S&R detector do at the baseline: `sr_detector/models.py` (the value objects, `Candle.from_kite` and the module constants), `sr_detector/pivots.py` (`find_swing_pivots`), `sr_detector/zones.py` (`cluster_zones`, `_zone_from_cluster`, `volume_profile_nodes`) and `sr_detector/confluence.py` (`ConfluenceContext`, `ScoringParams`, `score_zones` and its helpers): every function, branch, guard, unit, ordering assumption and numeric edge case. It records the callers of these functions at the interface only (Rama's decision P3 of 26-Nov-2026, Decision Register D-41): the internal logic of `zone_builder.py`, `detector.py`, `flags.py`, `retest_confirm.py`, `zone_cache.py`, `zone_warmer.py` and `screening/retest_monitor.py` belongs to the other A08 parts, and the logic of callers in other topics' files (A05's `core/candle_math.py`, A15's `core/daily_stats.py`, A18's `regime/`, `v3_chain/` and `scripts/forward_shadow_record.py`, A06's `signals/signal_processor.py`, A11's `orders/structure_exit_manager.py`) stays with their owners (index rules 1 and 8). Inherited items are catalogued by part P07; facts that bear on A05's handoffs about `Candle.from_kite` and unsorted rows are recorded plainly in sections 3, 4 and 7. No V2 design. It decides nothing.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-26 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced.

## 1. Method, sources and boundaries

## 2. The four files, their identity and declared purpose

## 3. The data model (`models.py`) and `Candle.from_kite`

## 4. Swing pivots (`pivots.py`)

## 5. Zone clustering and volume-profile nodes (`zones.py`)

## 6. Confluence scoring and merging across timeframes (`confluence.py`)

## 7. Input-order, data-quality and numeric edge cases across the four files (summary)

## 8. Callers and the contracts passed (interface only)

## 9. Stated intent: docstrings, comments, tests, legacy documents, history

## 10. Points for the AUDIT

## 11. UNKNOWN / NOT ESTABLISHED items

## 12. Questions about intent for Rama

## 13. Cross-references to other parts and topics
