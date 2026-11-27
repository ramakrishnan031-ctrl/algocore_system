# A08 AUDIT fieldwork — COMMON brief for every AUDIT helper (in addition to the STUDY COMMON brief)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` first: its sources, boundaries (D-41 P1 to P5), VERBATIM SECURITY
RULES, labels, evidence rules, saving/progress/backup rules and placeholders all apply unchanged. This brief adds the
AUDIT rules. Model throughout: the approved A07 AUDIT
`/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/A07_AUDIT_2026-11-24.md`
(sections 1.5 to 1.7 especially) and its intent-sources file
`.../A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/evidence/A07_AUDIT_INTENT_SOURCES_2026-11-24.md`.

## 1. Inputs

- The A08 STUDY at GitHub main `20e267d`:
  `/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/A08_STUDY_2026-11-26.md`
  and its eight evidence files in that folder's `evidence/` (cite STUDY sections, A08-AP-nn, A08-U-nn, A08-Q-nn, and
  part statements Pnn-Snnn). The STUDY describes; the AUDIT re-reads every code line it relies on at the baseline
  `970aabf` and never takes a STUDY statement as proof without re-reading the cited lines.
- Document 04, sections 5.1 to 5.4 and section 6 (`doc/00_PROJECT_CONTROL/01_PROJECT_FOUNDATION/04_...md`); Document 06,
  section 4.2; Document 08.
- Decision Register D-41 (boundaries) — preserve P1 to P5 exactly; Rama's working decisions
  `/home/claude/a08/notes/RAMA_DECISIONS_A08_STUDY.md` (incl. the AUDIT points of 27-Nov-2026).

## 2. Results and classifications (as the A07 AUDIT, section 1.6, unchanged)

- MATCH: the code does what the sources intend.
- ISSUE: a difference from intended behaviour; a conflict between sources that the code resolves one way; or, where
  intent is not established, a defect or weakness that the code itself demonstrates, of a kind listed in Document 04,
  section 5.3, the basis named. A lack of intent evidence alone does not make an ISSUE. An item with a MATCH part and an
  ISSUE part counts as ISSUE.
- UNKNOWN / NOT ESTABLISHED: the answer needs runtime evidence that does not survive, or intent is not established and
  the code demonstrates no such defect.
- Records observations: a true discrepancy in a project record or in the STUDY; not counted; no record changed.
- Classifications: FACT, INTERPRETATION, HISTORICAL, KNOWN DEFECT (provisional), OPEN QUESTION, UNKNOWN / NOT
  ESTABLISHED; anything Rama must decide is marked OPEN FOR RAMA.
- KNOWN DEFECT rule (A01 AUDIT, section 1.6, unchanged): (a) the code implements a mechanism for the case; (b) by the
  language or library semantics that mechanism fails for certain whenever the case occurs; (c) the case is one the code
  or an intent source says it handles, and it can arise under the documented set-up; (d) the outcome contradicts every
  intent source found. A record that gives or considers KNOWN DEFECT states which conditions hold and which fails. Every
  KNOWN DEFECT is provisional. A prior topic's classification keeps that topic's record (e.g. A05 HA-06's "KNOWN DEFECT
  considered and not given" stays A05's; A08 records its own item for the A08 side).
- Severity words only with their basis. No treatment options (T1/T2/T3) in the AUDIT: treatments come at step 8.

## 3. Record fields (Document 04, section 5.4; as the A07 AUDIT, section 1.6)

Area and flow; issue category (Document 04, section 5.3); intended behaviour and its source (IS, IC, CD or RS number of
the A08 intent-sources file, or path and lines with date, or "not established"); actual code path (file, function,
lines at the baseline); actual behaviour and effective value (committed value; deployed value UNKNOWN); evidence (STUDY
statement IDs and code lines); result and classification; severity/impact only with basis; owner topic; cross-reference
to the allocated STUDY items (A08-AP/U/Q) and any inherited item; OPEN FOR RAMA where Rama's intent or decision is
needed. ISSUE and UNKNOWN items as blocks; MATCH items as table rows.

## 4. Never

- Never update or propose text for the Audit Findings Register or the Open Issues Register; never change any earlier
  topic's record, ID, classification, treatment or status; never re-ask an earlier topic's history question (e.g. A01-10,
  RS-23); never repair, tune or design.
- Never state that a feature ran in production on code evidence alone.
- Never use the Decision Register entry D-42 (it does not exist yet).
