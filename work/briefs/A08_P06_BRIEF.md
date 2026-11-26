# A08 STUDY — Part P06 brief (writer): configuration keys, wiring and every consumer interface

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P06-S001` onwards.
Output file: `/home/claude/a08/parts/A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/P06_WRITER_PROGRESS.md`.
Context parts (checked; cite by statement ID, do not edit): P01 to P05 and P07 in `/home/claude/a08/parts/`. P06 is the
cross-cutting part: it records configuration and interfaces once, citing the parts for behaviour; it does not
re-describe the A08 objects' internals.

## Scope

1. Configuration (D-41 P3; A02 owns the files): every key of the `sr_detector:` block (`config/system_config.yaml`
   L508 to L545) and `structure_exit_enabled` (L634): for each key — committed value and its comment; the
   `SRDetectorConfig` field (`core/config_loader.py` L1153 onwards), its dataclass default and any validation; every
   reader at the baseline (file, function, lines; A08 objects and other topics' code); units; the fallback each reader
   uses if the attribute is absent (cite P01/P02/P03/P04 where they already record it); keys with no reader; readers of
   keys that do not exist in the block. Effective/deployed values: UNKNOWN / NOT ESTABLISHED (Document 06, section
   4.2). Any `*.local.yaml` overlay mechanism: record only that the loader merges such files and where (A02's); never
   open one.
2. Wiring in `main.py` (A01's file; interface only): L3421 to L3427 (the switches), L3480 to L3508 (the shared fetch
   closure and the V1 detector), L3515 to L3523, L3549 to L3572, L3575 to L3610, L3673 to L3693, L3728 to L3732 (PB-01
   fetcher; the inventory's L3717 to L3718 are imports), L3765 to L3802, L3804 to L3830, the shutdown L1599 onwards and
   L4267 to L4268: for each, what is constructed, under which switch, with which configuration values, the
   construction order, what happens if construction fails, and what is started/stopped and in which order. Produce a
   table "switch combination → A08 objects constructed/started" from the code (committed values marked).
3. Every consumer interface (A08 inventory section 2, as corrected by P01/P02/P03: `_sr_observe` call sites L1550,
   L2296, L2588): signal processor (A06's file), `orders/structure_exit_manager.py` (A11), `orders/eod_squareoff.py`
   (A12), the MARKET entry sites (A10), `regime/engine.py` and `v3_chain/*` (A18), `screening/hard_gate.py` `gate_htf`
   (A07; P01-S135), `reports/daily_trade_review.py` `_fmt_zone` (A15; P01-S136), the `Candle` type importers, the
   store and schema (A03), tests (A19, stated expectations only). For each: the call, the contract passed, the gating
   flag, what the consumer receives, and the owner topic — one consolidated table, citing the parts. Find any consumer
   not yet listed by `git grep` over the whole repository (exclusions applied) for every public A08 name.
4. The A08 inventory corrections found so far (for Claude's inventory revision; record as facts with lines): section
   2.1 `_sr_observe` call sites (L1550, L2296, L2588); section 2.2 PB-01 fetcher lines (construction L3728 to L3732);
   and any other inventory line you find wrong.

## Inherited items

Answer A08's side of every item whose PRIMARY part is P06 in P07 section 7 (final: A01 C13, C37, B-11; A02 K-21, K-25,
K-26; A03 U-24; A06 PQ-09 — P07-S107 notes no A08 code was found for K-25, K-26, U-24: confirm and record "no A08 side
found" or the side you find), and record P06's side where P06 is SECONDARY. Also confirm, as facts, the three rows
H-44, U-59, U-60 recorded unassigned in P03-S192 and say which part's code they touch (Claude decides their
assignment). Never change any item's classification, treatment or status.

## Intent sources

The configuration comments; `docs/SYSTEM_MAP.md`, `PATHS.md` (P01-S129: `sr_detector.enabled: false` there vs `true`
in the YAML), `README.md` and other legacy documents describing the S&R switches and wiring; git history of the
`sr_detector:` block and of the `main.py` wiring lines (HISTORICAL).

## Sections (after section 1, Method)

2. The configuration block: key-by-key table (value, comment, field, default, validation, readers, units)
3. Keys without readers, readers without keys, and default disagreements across layers (citing the parts)
4. `main.py` wiring: construction, switches, order, failure handling
5. Start and shutdown order of the A08 objects
6. Switch combinations and the A08 objects they produce (table)
7. Consolidated consumer-interface table (all topics)
8. Inventory corrections (facts)
9. Inherited items: P06's primary items, then its secondary items; the rows H-44, U-59, U-60
10. Stated intent: comments, documents, history
11. Points for the AUDIT
12. UNKNOWN / NOT ESTABLISHED items
13. Questions about intent for Rama
14. Cross-references
