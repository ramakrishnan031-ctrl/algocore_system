# A08 AUDIT — intended-behaviour sources, PROJECT-RECORDS half (writer)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` and `/home/claude/a08/briefs/A08_AUDIT_COMMON_BRIEF.md` first.
Output: `/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/ISA_WRITER_PROGRESS.md`. Model: the A07 intent-sources file (sections 1, 2, 3, 5,
7, 8; its rows IS-001 to IS-078, IC-001 to IC-012, RS-01 to RS-20).

## Scope

Every admitted PROJECT record that states or implies what A08's behaviour was intended to be, or what Rama said about
it: the approved Master System Investigation Index (entry A08, Appendix A, its rules); the approved A01 to A07 STUDY,
AUDIT and RECONCILED TOPIC RECORD files (statements about S&R, zones, pivots, retest, the V1 observer, the backfill, the
two scripts, the `sr_detector` configuration, `structure_exit`, the candle fetch for S&R); the registers (Decision
Register entries bearing on A08 incl. D-21, D-24, D-38 to D-41; Topic Completion Register A08; Audit Findings Register
and Open Issues Register rows that name A08 or its code — read only); the foundation rules that govern intent (Documents
04 section 5, 06 section 4.2, 08); and every statement attributed to Rama or to the operator in those records (RS rows).

## Rows

- IS-001 onwards: one row per source: short name, path and section/line, date, kind, label (FACT for what a project
  record says; HISTORICAL where it reports legacy intent), the A08 area(s) it bears on, and what it says (paraphrase;
  quotations under 15 words).
- RS-01 onwards: statements attributed to Rama or the operator (exact source; what it says; whether it is a decision,
  an answer or a reported practice).
- IC-001 onwards: conflicts between project sources on A08 intent (both sides cited; none chosen).
- ISA-Q1 onwards: questions about intent for Rama (draft; no preselected answers; never repeat an earlier topic's
  question whose history Rama directed to stay OPEN).

Areas: all areas; (a) calculation core — CZ; (b) candle fetch, zone builder, cache, warmer — FC; (c) V1 observer, flags,
results, backfill — VO; (d) V2 retest path and handoff — RT; (e) the two scripts — SC; (f) configuration, wiring,
consumers — XW; (g) tests (as recorded by earlier topics).

## Sections

1. Scope and method (1.1 clone checks: both HEADs; 1.2 what was read, with counts; 1.3 kinds, dates and labels; 1.4
   short names)
2. Sources by area (2.1 all areas; 2.2 to 2.8 areas (a) to (g))
3. Conflicts between sources (IC rows)
4. Statements attributed to Rama or to the operator (RS rows)
5. Could not establish
6. Questions about intent for Rama (ISA-Q rows)
