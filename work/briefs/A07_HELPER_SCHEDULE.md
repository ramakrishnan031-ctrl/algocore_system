# A07 STUDY: helper schedule (D-39 method)

At most two helpers at a time. A pair starts only after BOTH helpers of the previous pair have handed back
(the final notification of the COMMON brief section 6 received; a finished progress log does not count). Rama is asked before the first helper.

| Pair | Helper 1 | Helper 2 |
|---|---|---|
| 1 | P01 writer | P02 writer |
| 2 | P01 checker | P02 checker |
| 3 | P03 writer | P04 writer |
| 4 | P03 checker | P04 checker |
| 5 | P05 writer | P06 writer |
| 6 | P05 checker | P06 checker |
| 7 | P07 writer | P08 writer |
| 8 | P07 checker | P08 checker |
| 9 | P09 writer | P10 writer |
| 10 | P09 checker | P10 checker |
| 11 | STUDY assembly (one helper) | — |
| 12 | Independent check of the assembled STUDY (one helper) | — |

Then Claude: final review, validator, identifier scan, Rama's go-ahead, commit as DRAFT, ChatGPT's STUDY review.
Backups: Claude prepares the settings file /home/claude/a07_backup.conf and the separate backup clone /home/claude/a07_backup and creates the temporary branch
wip/a07-fieldwork from main just before pair 1, after Rama authorises it, and reports to Rama before pair 1 the verified repository URL, the branch name,
the branch's base commit and the clean initial state; helpers only run backup.sh (COMMON brief
section 2); the branch is never merged into main.
Every helper reads: A07_COMMON_BRIEF.md, A07_FOCUSED_QUESTIONS.md, its part in A07_PART_BRIEFS.md, and (checkers)
A07_CHECKER_BRIEF.md.
