# A08 evidence: the V2 retest path (divert, parking, confirmation, monitor) and its resume handoff
**Status:** DRAFT — evidence for the A08 STUDY
**Date:** 2026-11-26
**Revision history:** First version, 2026-11-26.
**Purpose and scope:** Part P04 of the A08 STUDY fieldwork. It records in full what the V2 retest mechanism ("SNR-V2", Phase A) does at the baseline: `sr_detector/retest_confirm.py` (`_is_long`, `RetestParams`, `RetestResult`, the five state names, `evaluate`, `_strong_close`) and `screening/retest_monitor.py` (`ParkedCandidate`, `RetestMonitor` with `start`, `stop`, `register`, `clear_all`, `rehydrate`, the poll loop, `_evaluate`, `_release`, `_fetch_recent_1m` and the row conversions, and `RetestDiverter` with `maybe_divert`, `_matching_zone` and `_log_divert_audit`), A08's use of the `retest_state` table at the interface, the end-of-day clear and the shutdown stop. Decision Register D-41 is applied: P1 (A08 owns the V2 retest mechanism and studies it in full; for `SignalProcessor.continue_from_retest`, A06's function, only the A08-specific handoff and values are recorded: what the monitor passes in, the retest-derived values that reach it (the zone band, the structure-stop buffer, the MARKET entry type) and what A08 receives back; its internal orchestration is A06's and is not audited, and the A09 and A10 decisions it reaches are named at the interface only; the PB-01 watchlist's retest is A18's and is recorded only as a distinct mechanism that reuses A08 functions), P3 (every call site in another topic's file at the interface only) and P4 (inherited items: A08's side only; no ID, owner, classification, treatment or status changed). `ZoneCache` and `ZoneWarmer` are cited from part P02 and the zone objects from part P01, not re-described. No V2 design is proposed.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, read on 2026-11-26 from the local read-only clone with git show/grep/log/blame. Nothing was written or run; no endpoint was contacted; the four credential-holding file patterns were excluded from every search; no credential, account identifier or machine path is reproduced.

## 1. Method, sources and boundaries

## 2. The files: identity, declared purpose, and the three distinct "retest" mechanisms in the code

## 3. `retest_confirm`: parameters, states and `evaluate`

## 4. `RetestDiverter`: the divert decision and its zone lookup

## 5. `ParkedCandidate` and `retest_state`

## 6. `RetestMonitor`: lifecycle, poll loop, confirmation, rejection, persistence

## 7. Restart, end of day and shutdown (`rehydrate`, `clear_all`, `stop`)

## 8. The `continue_from_retest` handoff (D-41 P1: inputs, retest-derived values, what comes back; call-outs named only)

## 9. Threads, locks, clocks and failure behaviour (summary)

## 10. Call sites in other topics' files (interface only)

## 11. Inherited items: P04's primary items, then its secondary items

## 12. Stated intent: docstrings, comments, tests, documents, history

## 13. Points for the AUDIT

## 14. UNKNOWN / NOT ESTABLISHED items

## 15. Questions about intent for Rama

## 16. Cross-references to other parts and topics
