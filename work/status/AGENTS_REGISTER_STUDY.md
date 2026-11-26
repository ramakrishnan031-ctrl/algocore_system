# A08 STUDY — helper register

| Helper | Part | Role | Model / effort | Started (IST) | Final hand-back (IST) | Status |
|---|---|---|---|---|---|---|
| H1 | P07 | writer (handoffs; runs first) | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 13:02 | 26-Nov-2026 13:26 | COMPLETE (115 statements; 6 AUDIT points; assignment table P07-S105) |
| H2 | P01 | writer (calculation core) | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 13:02 | 26-Nov-2026 13:23 | COMPLETE (132 statements; 17 AUDIT points; backup ceb66fb) |
| H3 | P07 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 13:31 | 26-Nov-2026 14:04 | COMPLETE (115 checked; 23 corrected, 1 re-labelled, 26 added -> 141; 16 Owner-field records assigned; backup 0677158) |
| H4 | P01 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 13:31 | 26-Nov-2026 14:02 | COMPLETE (132 checked; 33 corrected, 12 re-labelled, 8 added -> 140; backup d618f26) |
| H5 | P02 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 14:24 | 26-Nov-2026 15:07 | COMPLETE (157 statements; 16 AUDIT points; backup ecd10a1) |
| H6 | P03 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 14:24 | — | RUNNING |

Planned order (at most two at a time; next pair only after both final hand-backs; Rama consulted before each start):
1. P07 writer + P01 writer
2. P07 checker + P01 checker
3. P02 writer + P03 writer (briefs include P07's assignments)
4. P02 checker + P03 checker
5. P04 writer + P05 writer
6. P04 checker + P05 checker
7. P06 writer, then P06 checker
8. Assembly helper, then independent assembly checker


Notes for later (Claude):
- Inventory section 2.1 lists only L1550 for `_sr_observe`; the baseline also has call sites L2296 and L2588 (P01-S032). Correct the DRAFT inventory in a revision before the STUDY commit.
- Inventory section 2.2 gives `main.py` L3717-L3718 for the PB-01 fetcher; those are import lines, the construction is L3728-L3732 (P02-X08). Correct in the inventory revision.
