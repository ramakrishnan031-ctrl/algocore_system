# A08 evidence: candle fetch, zone building, zone cache and zone warmer
**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26.
**Purpose and scope:** Part P02 of the A08 STUDY fieldwork. (to be completed)
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-26 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced.

## 1. Method, sources and boundaries

## 2. The four files: identity and declared purpose

## 3. `OhlcFetcher`: windows, cache, conversion, ordering, errors

## 4. `zone_builder`: knobs, parameters, prior-day levels, anchors, split, payloads

## 5. `ZoneCache`

## 6. `ZoneWarmer`: queue, worker, re-warm, blocking, shutdown

## 7. Threads, locks, clocks and failure behaviour across the four files (summary)

## 8. Callers and readers (interface only)

## 9. Inherited items: P02's primary items, then its secondary items

## 10. Stated intent: docstrings, comments, tests, documents, history

## 11. Points for the AUDIT

## 12. UNKNOWN / NOT ESTABLISHED items

## 13. Questions about intent for Rama

## 14. Cross-references
