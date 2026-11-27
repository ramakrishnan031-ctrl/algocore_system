# A08 AUDIT — intended-behaviour sources, LEGACY-SIDE half (writer)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` and `/home/claude/a08/briefs/A08_AUDIT_COMMON_BRIEF.md` first.
Output: `/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_LEGACY_HALF_<YYYY-MM-DD>.md` (IST date).
Progress log: `/home/claude/a08/status/ISB_WRITER_PROGRESS.md`. Model: the A07 intent-sources file (sections 1, 2, 3,
4, 7, 8; its rows IS-501 to IS-698, IC-501 to IC-540, CD-501 to CD-522).

## Scope

Every LEGACY-side source at the baseline `970aabf` that states or implies the intended behaviour of the sixteen A08
paths and of A08's interfaces: legacy documents (`docs/`, `PATHS.md`, `README.md`, design, decision, audit and
running-log documents, `docs/SYSTEM_MAP.md`, the integrity audit, MASTER_PENDING files), module docstrings and comments
in the A08 files, dated labels (FIX-, SNR-, M-S and similar), log and alert texts, names, configuration comments by key
name (`config/system_config.yaml` `sr_detector:` block L508 to L545 and `structure_exit` L634 onwards;
`config/expected_managers.yaml`; `config/cron_registry.yaml` L408 to L423), commit messages of the A08 files (full
hashes), and the tests that reference A08 code as stated expectations (A08 inventory section 7, Revision 1; never run).
Every legacy source is HISTORICAL. Find them with `git grep` (exclusions always) and `git log`; use the STUDY parts'
"Stated intent" sections (P01 section 9, P02 section 10, P03 section 11, P04 section 12, P05 section 9, P06 section 10)
as the starting list and re-open every source at the baseline.

## Rows

- IS-501 onwards: one row per source: short name, path and lines, date (commit or document date), kind, label
  (HISTORICAL), the A08 area(s), what it says (paraphrase; quotations under 15 words).
- IC-501 onwards: conflicts between legacy sources (both cited; none chosen).
- CD-501 onwards: statements that only the code contradicts (the source, the code lines that differ; no verdict).
- ISB-R1 onwards: questions about intent for Rama (draft; no preselected answers).

Areas: as the project half — all areas; (a) CZ; (b) FC; (c) VO; (d) RT; (e) SC; (f) XW; (g) tests.

## Sections

1. Scope and method (1.1 clone checks; 1.2 what was read, with counts and the search patterns used; 1.3 kinds, dates and
   labels; 1.4 short names)
2. Sources by area (2.1 all areas; 2.2 to 2.8 areas (a) to (g))
3. Conflicts between sources (IC rows)
4. Statements that only the code contradicts (CD rows)
5. Could not establish
6. Questions about intent for Rama (ISB-R rows)
