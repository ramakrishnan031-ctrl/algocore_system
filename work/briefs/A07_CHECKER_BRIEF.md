# A07 STUDY helpers: CHECKER BRIEF (read the COMMON brief and the writer's part brief first)

You check one part file written by another helper. You did not write it. The write permissions and the backup rule
of the COMMON brief section 2 apply to you unchanged.

1. Check EVERY statement against its cited source at the baseline (`git show 970aabf:<path>` with the cited lines,
   or the cited record). For each statement decide: CONFIRMED, CORRECTED (state what changed), RE-LABELLED (for
   example FACT -> INTERPRETATION), or WITHDRAWN (keep the number, "WITHDRAWN: reason").
2. Correct the file in place. Keep statement numbers; add new statements only at the end of the relevant section
   with the next free number, marked "(added in the check)".
3. Coverage test by script: confirm (a) every function, method and class of the part's files appears in at least
   one statement (list each with the statement IDs); (b) every focused question the part brief assigns (wording in
   `/home/claude/a07/briefs/A07_FOCUSED_QUESTIONS.md`) is answered or marked UNKNOWN / NOT ESTABLISHED with the gap,
   checked independently against the question's full wording
   (for P09, Q22's paths each verified against the cited P02 to P08 statements and source lines); (c) every inherited item the P01 table assigns to this part is cross-referenced
   (for P01 itself: all 51 and all 10 entries are present, and counts by topic are 6, 7, 14, 5, 6, 13).
4. Security pass: run `python3 -I /home/claude/a07_tools/scan.py <file>`; no account identifier, IP, e-mail,
   machine path or secret; the four excluded file patterns never opened; credential variables by name only.
5. Label pass: no judgement words in statements; potential issues sit in "Points for the AUDIT" as neutral
   questions; runtime claims without evidence are UNKNOWN / NOT ESTABLISHED.
6. Add the final section "Check log": counts (statements checked, confirmed, corrected, re-labelled, withdrawn,
   added), the coverage-script output, the scan result, and each correction as "Pxx-Snnn: old -> new (source)".
7. Save after each section of the part you finish checking; progress log `/home/claude/a07/status/<PART>_checker.log`;
   run the backup after each section (COMMON brief section 5). Hand back as the COMMON brief section 6 says.
