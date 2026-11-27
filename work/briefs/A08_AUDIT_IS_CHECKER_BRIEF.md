# A08 AUDIT — CHECKER brief for the intended-behaviour sources (one checker per half; not the writer)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md`, `/home/claude/a08/briefs/A08_AUDIT_COMMON_BRIEF.md` and the
writer's brief (`A08_AUDIT_IS_PROJECT_BRIEF.md` or `A08_AUDIT_IS_LEGACY_BRIEF.md`). You check one half (named in your
start message). Progress log: `/home/claude/a08/status/<ISA|ISB>_CHECKER_PROGRESS.md`.

1. Copy the writer's file to `/home/claude/a08/check/<file>.writer_original` before editing.
2. Re-open EVERY row's source (project record at algocore_system `20e267d`, or legacy source at `970aabf` with `git
   show`, `git log`, `git grep`): path, section/lines, date, what it says, label (project-record statements FACT where
   they state record content; legacy sources HISTORICAL; attributions to Rama exact), the areas it bears on. Quotations
   under 15 words and exact.
3. Check every IC row (both sides cited correctly; none chosen; no verdict) and every CD row (the code lines really
   differ from the source, re-read at the baseline; no verdict). Check the questions: neutral; no preselected answer;
   no repeat of a history question Rama directed to stay OPEN (A01-10, the 16 entries naming A08, RS-23 of A07) or of the
   STUDY's A08-Q-01 to A08-Q-25 (an addition to one of those must say so).
4. Completeness: search for sources the writer missed (project half: every A01 to A07 record and register row that
   names A08, its paths or public names; legacy half: re-run the writer's search patterns and add obvious missing ones);
   add rows with new numbers continuing the writer's sequence; never renumber.
5. Correct in place; log every change (row, before -> after, reason, source). Update the header Revision history
   ("Checked and corrected in place by the <ISA|ISB> checker, <date> ..."); append `## Check log`.
6. Scan 0 hits; no absolute paths; no credential, account identifier or machine path reproduced.

Save, log (read the IST clock for every time you write) and back up after every section
(`bash /home/claude/a08_tools/backup.sh "<ISA|ISB> checker section <n>"`). Hand back: file name, rows checked, counts of
corrections / re-labels / withdrawals / additions, completeness searches and results, residual doubts.
