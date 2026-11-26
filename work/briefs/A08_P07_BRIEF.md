# A08 STUDY — Part P07 brief (writer): the inherited items and the open issues that name A08

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first; it governs. Statement IDs: `P07-S001` onwards.
Output file: `/home/claude/a08/parts/A08_PRIOR_TOPIC_HANDOFFS_<YYYY-MM-DD>.md` (IST date of writing).
Progress log: `/home/claude/a08/status/P07_WRITER_PROGRESS.md`.

P07 runs FIRST (paired with P01) so that parts P02 to P06 receive an exact list of the items they must answer. It is
the A08 counterpart of A07's part P01 (`.../A07_.../evidence/A07_PRIOR_TOPIC_HANDOFFS_2026-11-21.md` — read it as the
model for structure and depth).

## Scope (D-41, P4)

A. The 48 items handed to A08 by the approved A01 to A07 records (each record's section 15.2):
   - A01: C13, C37, C38a, B-11, C38b (A01 record L304 says "C38b, probably (to confirm)"; D-41 / index Appendix A give
     `scripts/sr_level_export.py` to A08)
   - A02: K-02, K-21, K-22, K-23, K-24, K-25, K-26
   - A03: D-05, H-11, P-02, P-11, Q-11, Q-17, Q-29, U-24, U-25
   - A04: CL-11, CL-15, RL-05, RL-06
   - A05: CM-05, CM-10, CM-15, HA-01, HA-04, HA-06, HA-07, HA-08, HA-09, IN-02, XC-03
   - A06: WA-06, WA-07, WD-10, WD-16, PQ-09, PQ-11, EV-11, EV-23
   - A07: SL-06, SL-30, EG-01, XS-12
   Confirm the list by script against each record's section 15.2 table row `| A08 | ... |` and report any difference.
B. The 16 Open Issues Register entries that name A08: A03-10, A04-05, A04-28, A05-01, A05-02, A05-17, A05-18, A05-25,
   A05-27, A05-28, A05-29, A05-32, A05-35, A05-37, A05-38, A05-54 (confirm by script: every `### A0n-nn` section of
   `OPEN_ISSUES_REGISTER_2026-11-05.md` whose text contains the word A08).
C. The non-ID handoff notes in the records' section 15.2 prose that name A08 (e.g. A03: "the S&R shadow database";
   A05: the fetchers' cache key and wall-clock age — KNOWN DEFECT considered and not given at the boundary —, the
   unsorted fetched rows, `Candle.from_kite`'s conversions, the corporate-action check, `sr_level_export.py` stopping
   at L139 before A01 C38b's recorded L141; A06: "whether the dispatcher's zone warming can block"; A07 record section
   15.2 point 2: the retest path's owner, now decided by D-41 P1). Find them all by script.
D. The retest-ownership wording difference: A06 AUDIT PQ-13 ("A18's retest path"), A07 parts SL and EG ("A08 and
   A18") against D-41 P1. Record the facts only; nothing is changed.

## For each item (one row or block per item; statements P07-Snnn)

- ID, source topic, source file and exact location (the AUDIT record row; the register entry);
- the source's result/classification (MATCH / ISSUE / UNKNOWN; KNOWN DEFECT if any), its treatment and status from
  the Audit Findings Register (topic section) or Open Issues Register — copied exactly, unchanged;
- what the source says about A08's side (short paraphrase; any quotation under 15 words);
- the A08 question it raises (neutral; what A08 must establish);
- the A08 code location(s) at the baseline where the answer lies (FACT: path and lines you found with git grep/show;
  you may confirm that the code exists and where, but do NOT write the A08 finding — the assigned part does that);
- the assigned part(s): P01 calculation core (models, pivots, zones, confluence); P02 `fetch.py`, `zone_builder.py`,
  `zone_cache.py`, `zone_warmer.py`; P03 `detector.py`, `flags.py`, `__init__.py`, the `sr_detector_results` writes,
  `scripts/sr_detector_backfill.py`; P04 `retest_confirm.py`, `screening/retest_monitor.py`, the
  `continue_from_retest` interface, `retest_state`, the end-of-day clear; P05 `scripts/sr_corp_action_spotcheck.py`,
  `scripts/sr_level_export.py`; P06 configuration keys, `main.py` wiring and every consumer interface.
- A04-05 / CL-11 (the token file): security rules apply — record only the A08 interface (whether and where A08 code
  or scripts use the broker client); never read, derive, check or discuss any credential value, validity or exposure.

## Sections to write (after section 1, Method)

2. How the list was confirmed (scripts used, counts; differences if any)
3. The 48 inherited items, by source topic (A01 to A07)
4. The 16 open issues that name A08
5. The non-ID handoff notes
6. The retest-ownership wording (facts only; D-41 P1)
7. Assignment table: part -> item IDs (every item in exactly one primary part; secondary parts where relevant), with a
   count per part and a script-checked total (48 items + 16 issues + notes)
8. Points for the AUDIT (only where the source records themselves differ from each other, e.g. L139 vs L141; no A08
   findings)
9. UNKNOWN / NOT ESTABLISHED items
10. Questions about intent for Rama (only if an item cannot be understood without Rama)
11. Cross-references

Do not reopen, reclassify, re-treat or re-word any earlier topic's item; do not edit any record.
