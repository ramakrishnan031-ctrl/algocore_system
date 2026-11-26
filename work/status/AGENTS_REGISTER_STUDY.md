# A08 STUDY — helper register

| Helper | Part | Role | Model / effort | Started (IST) | Final hand-back (IST) | Status |
|---|---|---|---|---|---|---|
| H1 | P07 | writer (handoffs; runs first) | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 13:02 | 26-Nov-2026 13:26 | COMPLETE (115 statements; 6 AUDIT points; assignment table P07-S105) |
| H2 | P01 | writer (calculation core) | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 13:02 | 26-Nov-2026 13:23 | COMPLETE (132 statements; 17 AUDIT points; backup ceb66fb) |
| H3 | P07 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 13:31 | 26-Nov-2026 14:04 | COMPLETE (115 checked; 23 corrected, 1 re-labelled, 26 added -> 141; 16 Owner-field records assigned; backup 0677158) |
| H4 | P01 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 13:31 | 26-Nov-2026 14:02 | COMPLETE (132 checked; 33 corrected, 12 re-labelled, 8 added -> 140; backup d618f26) |
| H5 | P02 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 14:24 | 26-Nov-2026 15:07 | COMPLETE (157 statements; 16 AUDIT points; backup ecd10a1) |
| H6 | P03 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 14:24 | 26-Nov-2026 15:13 | COMPLETE (214 statements; 16 AUDIT points; backup 2aa596d) |
| H7 | P02 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 15:14 | 26-Nov-2026 15:55 | COMPLETE (157 checked; 44 corrected, 1 re-labelled, 3 added -> 160; AP17 added; backup 88c9292) |
| H8 | P03 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 15:14 | 26-Nov-2026 15:49 | COMPLETE (214 checked; 36 corrected, 4 re-labelled, 3 added -> 217; backup 616d386) |
| H9 | P04 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 15:56 | 26-Nov-2026 16:41 | COMPLETE (182 statements; 21 AUDIT points; backup 6754933) |
| H10 | P05 | writer | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 15:56 | 26-Nov-2026 16:36 | COMPLETE (121 statements; 17 AUDIT points; progress-log times corrected by the writer) |
| H11 | P04 | checker | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 16:44 | 26-Nov-2026 16:53 | COMPLETE (182 checked; 3 corrected, 1 added -> 183; AP13, AP15 reworded; backup b53adb4) |
| H12 | P05 | checker | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 16:44 | 26-Nov-2026 16:57 | COMPLETE (121 checked; 18 corrected, 1 added -> 122; AP10 corrected; backup 4d5f467) |
| H13 | P06 | writer | Opus 5.5 / High (Rama, 26-Nov) | 26-Nov-2026 17:00 | 26-Nov-2026 17:24 | COMPLETE (186 statements; 10 AUDIT points; 14 inventory corrections; 43 unnamed records found; backup 966b77e) |
| H14 | P06 | checker | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 17:26 | 26-Nov-2026 18:13 | COMPLETE (186 checked; 53 corrected, 3 added -> 189; 47 of 48 records with part pointers; PQ-06 found) |
| H15 | STUDY | assembler | Opus 5.5 / Max (Rama, 26-Nov) | 26-Nov-2026 18:36 | — | RUNNING |

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
- Rows H-44, U-59, U-60 (P03-S192): unassigned; P06 brief asks P06 to confirm the code they touch; Claude to decide assignment at assembly.
- A03 AUDIT H-11 cites retest_monitor.py L415 for the divert's ts; baseline L414 (P03-X08 d). Record only in A08; do not change A03.
- A01 C40 and A02 K-32 touch A08's scripts but do not name A08 (P05-AP17): not assigned; decide at assembly / flag for ChatGPT.
- Inventory section 7 omits tests/unit/test_sr_v2_market_path.py (P04-X08). Correct in the inventory revision.
