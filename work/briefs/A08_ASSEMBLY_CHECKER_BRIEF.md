# A08 STUDY — ASSEMBLY CHECKER brief (independent; a different helper from the assembler)

Read `/home/claude/a08/briefs/A08_COMMON_BRIEF.md` (governs) and `/home/claude/a08/briefs/A08_ASSEMBLY_BRIEF.md` (what the
assembler was asked to do). You check the assembled STUDY `/home/claude/a08/out/A08_STUDY_<date>.md` (named in your start
message) against the seven checked parts in `/home/claude/a08/parts/`, the inventory Revision 1, the algocore records and,
where a synthesis sentence states a code fact, the baseline code (`git show 970aabf:<path>`).
Progress log: `/home/claude/a08/status/ASSEMBLY_CHECKER_PROGRESS.md`.

## Task

1. Copy the assembled file to `/home/claude/a08/check/<file>.assembler_original` before editing.
2. Faithfulness: every sentence in sections 2 to 16 must be supported by the part statements it cites (or the record /
   code line). Check every citation resolves and says what the sentence says; check no part fact is distorted, no label
   upgraded (INTERPRETATION or UNKNOWN presented as FACT), no verdict, KNOWN DEFECT label or V2 design added.
3. Completeness by script: every part AP, U and R ID appears in sections 15 or 16; every one of the 48 inherited items,
   16 open issues, 16 Owner-field records, notes N1 to N6, the 43 + 5 listed records and A06 PQ-06 appears in section
   13 with classification/treatment/status copied word for word from the Audit Findings Register / Open Issues Register;
   every direction requirement (assembly brief) is mapped in section 1.9 to sections and statements that answer it.
4. Consistency: section 2 (in brief) and section 15 agree with the body; counts stated anywhere are re-counted by
   script; D-41 boundaries are stated correctly (P1 wording on `continue_from_retest`); Rama's coverage decisions and
   Claude's assignment decisions are flagged for ChatGPT.
5. Correct in place; log every change (location, before -> after, reason, source); never renumber consolidated IDs
   after they are cited (withdrawn ones keep their number).
6. Scan 0 hits; no absolute paths; header Revision history updated ("Checked and corrected in place by the assembly
   checker, <date> ..."); append `## Check log` at the end of the file.

Save, log (read the IST clock for every time you write) and back up after every section you check
(`bash /home/claude/a08_tools/backup.sh "assembly checker section <n>"`). Hand back: file name, lines, counts of
corrections by kind, the completeness scripts and results, residual doubts.
