# A08 AUDIT — PART CHECKER brief (one checker per part; a different helper from the writer)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` (governs), `/home/claude/a08/briefs/A08_AUDIT_COMMON_BRIEF.md` and
`/home/claude/a08/briefs/A08_AUDIT_PART_BRIEF.md`. You check one AUDIT part (named in your start message):
`/home/claude/a08/parts/A08_AUDIT_PART_<PREFIX>_<date>.md`. Progress log: `/home/claude/a08/status/AUDIT_<PREFIX>_CHECKER_PROGRESS.md`.

1. Copy the writer's file to `/home/claude/a08/check/<file>.writer_original` before editing.
2. Re-check EVERY record against its sources: the code lines at `970aabf` (`git show`), the STUDY statements, the
   intent-sources rows (IS/IC/CD/RS numbers say what is cited), the earlier records. Every field present (AUDIT COMMON
   brief, section 3).
3. Results: MATCH / ISSUE / UNKNOWN applied by the rule (a lack of intent evidence alone is not an ISSUE; runtime
   questions are UNKNOWN; an item with a MATCH part and an ISSUE part is ISSUE). KNOWN DEFECT only under the four
   conditions, each condition's status stated, provisional; re-test every KNOWN DEFECT given or considered.
   Classifications honest (FACT / INTERPRETATION / HISTORICAL; no runtime claim without evidence).
4. Allocation coverage BY SCRIPT: every row of `/home/claude/a08/notes/AUDIT_ALLOCATION.md` with this part's prefix has
   exactly one disposition in section 2; inherited items' IDs, owners, classifications, treatments and statuses quoted
   unchanged; "cited to part X" reasons valid under the ownership rule.
5. Remove verdicts beyond the evidence, treatment options, V2 design, Audit Findings / Open Issues Register text and any
   security-rule breach. D-41 P1 to P5 exactly.
6. Totals re-counted by script; questions neutral, no preselected answers, no re-asked history questions.
7. Correct in place; log every change (record, before -> after, reason, source); a result change is logged with its
   full reason. New records continue the sequence; never renumber; a withdrawn record keeps its ID with a note.
   Update the header Revision history; append `## Check log` (section 10).
8. Scan 0 hits; placeholders; mask identifier-shaped tokens in notes.

Save, log (read the IST clock) and back up after every section or ~10 records
(`bash /home/claude/a08_tools/backup.sh "<PREFIX> checker section <n>"`). Hand back: file name, records checked, result
changes (with IDs), corrections by kind, KNOWN DEFECT re-tests, coverage result, totals, residual doubts.
