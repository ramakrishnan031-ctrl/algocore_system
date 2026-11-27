# A08 AUDIT — PART brief (writer), for parts CZ, FC, VO, RT, SC and XW

Read first, in full: `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` (governs), `/home/claude/a08/briefs/A08_AUDIT_COMMON_BRIEF.md`
(AUDIT rules: results, KNOWN DEFECT rule, record fields, "never" list), and the model, the approved A07 AUDIT
(`.../A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/A07_AUDIT_2026-11-24.md`, section 1.5 to 1.7 and one part,
e.g. section 10, part EG).
Your part is named in your start message. Statement IDs: `<PREFIX>-01` onwards (two digits; three if over 99). ISSUE and
UNKNOWN records and records observations are numbered first (section .3), MATCH records after them (section .4); an
item added later continues the sequence; never renumber.
Output: `/home/claude/a08/parts/A08_AUDIT_PART_<PREFIX>_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/AUDIT_<PREFIX>_WRITER_PROGRESS.md`.

## Inputs

- The A08 STUDY (`20e267d`) and its evidence part for your area; the intended-behaviour sources, both halves as
  checked: `/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md` (IS-001…, IC-001…, RS-…,
  ISA-Q…) and `/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_2026-11-27.md` (IS-501…, IC-501…, CD-501…,
  ISB-R…). Cite them by number. A source you need that is not in either file: cite it by path, lines and date, and list
  it in section .9 (numbered later in the cross-part check).
- Your allocation: every row of `/home/claude/a08/notes/AUDIT_ALLOCATION.md` whose Part is your prefix. Every allocated
  item gets exactly one disposition in section .2 (the record that answers it, or "cited to part <X>" with the reason
  under the ownership rule below). Items allocated to other parts may be cited, never counted.
- Ownership rule between parts: where one behaviour appears in two parts, the part that owns the mechanism counts it
  and the other cites it. If you find that an allocated item's mechanism is really in another part, record it as
  "cited to part <X>" in section .2 and say so in your hand-back (Claude decides).

| Part | Files studied in full (baseline `970aabf`) | STUDY sections | STUDY evidence part |
|---|---|---|---|
| CZ | `sr_detector/models.py`, `pivots.py`, `zones.py`, `confluence.py` | 3 (and 10, 12 where they bear) | P01 |
| FC | `sr_detector/fetch.py`, `zone_builder.py`, `zone_cache.py`, `zone_warmer.py` | 4, 10 | P02 |
| VO | `sr_detector/__init__.py`, `detector.py`, `flags.py`; `scripts/sr_detector_backfill.py`; the `sr_detector_results` interface | 5, 10 | P03 |
| RT | `sr_detector/retest_confirm.py`, `screening/retest_monitor.py`; the `retest_state` interface; the `continue_from_retest` handoff (D-41 P1: A08-specific handoff and values only; A06's orchestration not audited) | 6, 10 | P04 |
| SC | `scripts/sr_corp_action_spotcheck.py`, `scripts/sr_level_export.py` (SECURITY: broker client at the interface only; never run) | 7 | P05 |
| XW | configuration (`sr_detector:` block, `structure_exit_enabled`), `main.py` wiring and shutdown (interface), every consumer interface, documents and tests as stated expectations, the inherited items and listed records allocated to XW, cross-topic boundaries | 1, 8, 9, 11, 12, 13, 14 | P06, P07 |

## Sections (n = your part's section number in the assembled AUDIT; write them as 1 to 10 here)

1. Scope and method (files, lines re-read, external sources with URL and date read, scripts used — none importing
   legacy code)
2. Dispositions of the allocated items: 2.1 A08-AP points; 2.2 A08-U items; 2.3 A08-Q questions; 2.4 inherited items
   (IDs, owners, classifications, treatments and statuses quoted unchanged from STUDY section 13); 2.5 Open Issues
   Register entries; 2.6 Owner-field records, listed records and notes. Each row: item, disposition (record ID or
   "cited to part X"), one-line reason.
3. Issue and UNKNOWN records (blocks with every field of the AUDIT COMMON brief, section 3), records observations among
   them (marked, not counted)
4. Match records (table rows with the same information in short form)
5. Handoffs to other topics (what another topic must examine; owner per the index)
6. Totals (by script: MATCH / ISSUE / UNKNOWN; records observations separately; KNOWN DEFECT considered / given)
7. Could not establish
8. Questions about intent for Rama (draft, plain, no preselected answers; never re-ask A01-10's history, the 16 OIR
   entries' history, or A07's RS-23; say when a question adds to a STUDY A08-Q or an ISA-Q / ISB-R)
9. Sources cited beyond the intent-sources file (path, lines, date, what it says)
10. (left for the checker) Check log

## Rules specific to the AUDIT parts

- Re-read every code line you rely on at `970aabf`; a STUDY statement is a pointer, never proof.
- Each ISSUE states its issue category (Document 04, section 5.3) and the intent source; where intent is not
  established, name the demonstrated defect or weakness; otherwise UNKNOWN.
- KNOWN DEFECT: only under the four-condition rule; state which conditions hold and which fails; provisional. Where
  you consider it and do not give it, say "KNOWN DEFECT considered and not given" with the failing condition.
- A08's own items only: an earlier topic's item keeps its record; A08 writes its own record of A08's side and
  cross-references the earlier item without changing it (e.g. HA-06: A05's classification stays A05's).
- D-41 P1 to P5 exactly; P1 for `continue_from_retest`.
- No treatment options, no V2 design, no runtime claims without evidence, no Audit Findings / Open Issues Register text.
- Arithmetic re-computed only by scripts that re-state the expressions read at the baseline and import nothing legacy.
