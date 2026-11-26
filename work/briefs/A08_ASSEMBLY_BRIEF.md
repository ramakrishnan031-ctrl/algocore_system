# A08 STUDY — ASSEMBLY brief (one assembler; then an independent assembly checker)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs (sources, boundaries, security, labels, saving,
backup). You assemble the A08 STUDY from the seven checked evidence parts. You add no new fieldwork except where a part
is silent and a fact is needed for the synthesis; any such addition is cited to the code with lines and listed in your
hand-back.

Output: `/home/claude/a08/out/A08_STUDY_<YYYY-MM-DD>.md` (IST date of assembly).
Progress log: `/home/claude/a08/status/ASSEMBLY_PROGRESS.md`. Save, log and back up after every section.

## Inputs (checked; cite by statement ID; do not edit them)

In `/home/claude/a08/parts/`: P01 `A08_PIVOTS_ZONES_AND_CONFLUENCE_SCORING_2026-11-26.md`; P02
`A08_CANDLE_FETCH_ZONE_BUILDER_CACHE_AND_WARMER_2026-11-26.md`; P03 `A08_V1_OBSERVER_FLAGS_RESULTS_AND_BACKFILL_2026-11-26.md`;
P04 `A08_V2_RETEST_PATH_AND_RESUME_HANDOFF_2026-11-26.md`; P05 `A08_SPOTCHECK_AND_EXPORT_SCRIPTS_2026-11-26.md`; P06
`A08_CONFIGURATION_WIRING_AND_CONSUMER_INTERFACES_<date>.md`; P07 `A08_PRIOR_TOPIC_HANDOFFS_2026-11-26.md`; the A08
inventory (committed DRAFT, plus Claude's revision notes in `/home/claude/a08/notes/INVENTORY_REVISION_NOTES.md` if
present); Rama's working decisions `/home/claude/a08/notes/RAMA_DECISIONS_A08_STUDY.md`; Claude's assignment decisions
`/home/claude/a08/notes/CLAUDE_ASSIGNMENT_DECISIONS.md` (if present); ChatGPT's A08 investigation direction (its
requirements are summarised in Decision Register D-41's Evidence field and in the Topic Completion Register entry A08;
the direction's section 4 lists: A.1 inventory; A.2 S&R data path; A.3 retest monitoring; A.4 the three scripts; A.5
configuration; A.6 concurrency, retries, errors, missing data, restart; A.7 interfaces to A07, A09, A11; B the AUDIT
checks; section 5 the A05 handoffs incl. HA-06, unsorted rows, `Candle.from_kite`, the corporate-action check, L139 vs
L141).

Model: the approved A07 STUDY
`/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/A07_STUDY_2026-11-22.md`
— follow its header fields, its section pattern and its citation style ("P04-S070", "P02-AP11").

## Header

```
# A08 — STUDY: Technical analysis, S&R and retest context

**Status:** DRAFT — the STUDY of topic A08 (Document 04, section 4, step 4); not yet reviewed by ChatGPT
**Date:** <date>
**Revision history:** First version, <date>.
**Purpose and scope:** ...
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 26-Nov-2026 ... ; current external context as named in section 1.5.
**Related documents:** Documents 04, 05, 06, 07, 08 and 10; the Master System Investigation Index (entry A08 and Appendix A); the Decision Register, D-07, D-12, D-17, D-21, D-23 to D-25, D-28, D-30 to D-33, D-35, D-37, D-40 and D-41 (the A08 boundary decisions P1 to P5 and the working method); ChatGPT's A08 investigation direction (dated 25-Nov-2026, approved by Rama 26-Nov-2026) and Claude's first A08 checkpoint and ChatGPT's reviews (not kept as files, D-17); the A01 to A07 RECONCILED TOPIC RECORDS and AUDITs; the Topic Completion Register (entry A08); the Open Issues Register; the Audit Findings Register; the A08 evidence files listed in section 17.
```

## Sections

1. Purpose, scope, exclusions and fixed baseline — 1.1 Purpose; 1.2 Scope and paths (D-41 P1 to P5); 1.3 Exclusions;
   1.4 Fixed baseline; 1.5 Method (parts, writers and checkers, models and effort as recorded in the helper register and
   Rama's working decisions; external sources with dates); 1.6 Runtime evidence limit; 1.7 Labels; 1.8 Changes after
   the last recorded deployment (none: inventory section 6); 1.9 Where the direction's requirements are answered (a
   table: direction item -> STUDY section -> part statements); 1.10 Security restriction (verbatim rules; how CL-11,
   CL-15, CL-12, AU-05, A04-05 were handled).
2. A08 in brief (one page: the three S&R mechanisms — V1 observer, V2 retest path, zone supply to the structure exit —
   and the scripts; what is on/off at the committed values; the headline facts, without verdicts).
3. The calculation core: data model, pivots, zones, confluence scoring (P01)
4. Candle fetch, zone building, zone cache and warmer (P02)
5. The V1 observer, flags, the `sr_detector_results` row and the end-of-day backfill (P03)
6. The V2 retest path and the `continue_from_retest` handoff (P04; D-41 P1 boundary stated)
7. The corporate-action spot-check and the level-export script (P05)
8. Configuration read by A08: committed values, defaults across layers, effective values UNKNOWN (P06; P01/P02/P04)
9. Wiring, start and shutdown; switch combinations (P06)
10. Clocks, threads, locks, retries, failure, missing/invalid data and restart behaviour across A08 (summary table
    citing the parts)
11. Consumers: the technical context supplied to entry, risk and exit decisions and to other topics (P06 consolidated
    table; D-41 P3)
12. Documents, legacy records and tests against the code; intent sources and their conflicts
13. Inherited items: 13.1 the records as handed over; 13.2 the 48 items; 13.3 the 16 open issues; 13.4 the 16 Owner-field
    records (Rama's decision of 26-Nov-2026 — flagged for ChatGPT's STUDY review); 13.5 the prose notes N1 to N6; 13.6
    records that touch A08 code without naming A08 (P05-AP17, P03-S192, P06 sweep) and Claude's assignment decisions.
    One row per item: ID, source, classification/treatment/status (copied, unchanged), A08 side in one or two sentences,
    part statements. Never reclassify.
14. Cross-topic boundaries and handoffs (D-41; by owner topic A01 to A20; the retest-ownership wording note, P07 section
    6 and P04 N6; earlier-record citation differences found — noted only, nothing changed)
15. Points the AUDIT may examine, and what cannot be established — 15.1 Points for the AUDIT: consolidate every part's
    AP items into one de-duplicated, numbered list (AP-01 ...), each with the part AP IDs it merges, the facts and
    sources, and the comparison it invites; no verdicts, no classifications, no KNOWN DEFECT label; 15.2 UNKNOWN / NOT
    ESTABLISHED items consolidated, each with the evidence that would settle it.
16. Draft questions about intent for Rama (consolidated from the parts' R items; plain; no preselected answers).
17. Evidence index — 17.1 the A08 paths at the baseline (from the inventory, corrected); 17.2 the evidence files (the
    inventory and the seven parts, with their final file names, statement counts and a SHA-256 placeholder "computed at
    commit").

## Rules

- Every statement in sections 2 to 16 cites at least one part statement, AP/U/R ID, record or code line.
- Keep labels: a synthesis sentence that combines FACTs stays FACT only if every part is FACT; otherwise
  INTERPRETATION with its basis.
- Where parts disagree, say so and cite both; do not resolve silently (checkers' corrected text governs over writers').
- Preserve every AUDIT point and every UNKNOWN item from every part (coverage test by script at the end: every part
  AP/U/R ID appears in sections 15 or 16).
- No V2 design. Security rules verbatim. Placeholders, no absolute paths. Scan 0 hits.
- Hand back: file name, line count, section list, counts (consolidated AUDIT points, UNKNOWN items, questions), the
  coverage-test result, additions beyond the parts, residual doubts.
