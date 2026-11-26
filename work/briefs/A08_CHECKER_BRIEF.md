# A08 STUDY — CHECKER brief (one checker per part; a different helper from the writer)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` (it governs) and the writer's part brief
`/home/claude/a08/briefs/A08_<Pxx>_BRIEF.md`. You check one part file: `/home/claude/a08/parts/<file>` (named in your
start message). Progress log: `/home/claude/a08/status/<Pxx>_CHECKER_PROGRESS.md`.

## Task

1. Before editing, copy the writer's file to `/home/claude/a08/check/<file>.writer_original` (keep it unchanged).
2. Check EVERY statement, one by one, against its cited source at the baseline (`git show 970aabf:<path>` with line
   numbers) or the cited algocore record: line numbers, names, values, counts, quoted text, label. Re-derive counts and
   lists by script where possible.
3. Correct the part file in place: fix wrong lines/values; re-label a statement whose label is wrong (e.g. FACT that is
   really INTERPRETATION or UNKNOWN; anything stating runtime behaviour without evidence -> UNKNOWN / NOT
   ESTABLISHED); withdraw an unsupported statement (keep its ID, "WITHDRAWN: reason"); add missing statements with new
   IDs continuing after the writer's last ID (never renumber). Remove any V2 design content, any verdict the evidence
   does not support, any KNOWN DEFECT label, and any security-rule breach.
4. Coverage test BY SCRIPT: list every `def`/`class` (and, for scripts, every argparse option and every external call)
   in the part's files at the baseline and confirm each is covered by at least one statement; list every branch-heavy
   function and confirm its branches are described. For P07: confirm by script that all 48 items, all 16 open issues
   and all prose notes are present and each assigned to a part. Record the script and its result in the check log.
5. Check the part brief's sections are all present and the "Points for the AUDIT", "UNKNOWN" and "Questions" sections
   are complete and neutral.
6. Run `python3 -I /home/claude/a08_tools/scan.py <file>` (0 hits) and check no absolute path (use the placeholders).
7. Update the header's Revision history: "Checked and corrected in place by the Pxx checker, <date> (n statements
   corrected, n re-labelled, n withdrawn, n added; see the final section 'Check log')."
8. Append `## Check log`: method; coverage scripts and results; a table of every change (statement ID, before ->
   after, reason, source); statements verified without change (count); residual doubts.

Save and back up after every section of the file you check (COMMON brief, section 6), e.g. every 25 statements. When
complete, hand back: file name, statements checked, counts of corrections/re-labels/withdrawals/additions, coverage
result, scan result, residual doubts.
