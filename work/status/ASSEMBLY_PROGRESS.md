# A08 STUDY assembly progress (helper H15, assembler)

Output: out/A08_STUDY_2026-11-26.md (IST date of assembly).
Inputs: the seven checked parts in parts/ (not edited); the A08 inventory Revision 1 (read only); notes/RAMA_DECISIONS_A08_STUDY.md;
notes/CLAUDE_ASSIGNMENT_DECISIONS.md; status/AGENTS_REGISTER_STUDY.md; Decision Register D-41; Topic Completion Register entry A08.
Consolidated numbering: A08-AP-nn (points for the AUDIT), A08-U-nn (UNKNOWN items), A08-Q-nn (questions); the topic prefix keeps
them apart from P07's own AP-01 to AP-06.

| Time (IST) | Section done | Next step | Notes |
|---|---|---|---|
| 2026-11-26 18:39 | start: briefs, A07 STUDY model (skim), D-41, TCR entry A08, inventory Rev 1, decision notes and helper register read; skeleton (header and all section headings) created | read P07, then P01 -> section 3 | none |
| 2026-11-26 18:42 | section 3 (P01, calculation core) written | read P02 (index + full key sections) -> section 4 | P07 read in full; P01 read in full; notes/ASSEMBLY_NOTES.md started |
| 2026-11-26 18:44 | section 4 (P02, fetch, zone builder, cache, warmer) written | read P03 -> section 5 | P02 index + sections 3.8, 7, 9, 11-14 read in full; notes updated |
| 2026-11-26 18:46 | section 5 (P03, V1 observer, flags, row, backfill) written | read P04 -> section 6 | P03 index + sections 10, 12-15, check log read; notes updated |
| 2026-11-26 18:48 | section 6 (P04, V2 retest path and continue_from_retest handoff) written | read P05 -> section 7 | P04 index + sections 9, 11, 13-16, selected statements, check log read; notes updated |
| 2026-11-26 18:49 | section 7 (P05, spot-check and export scripts) written | read P06 -> sections 8, 9, 11 | P05 index + sections 8, 10-13 read; notes updated |
| 2026-11-26 18:51 | sections 8 (configuration) and 9 (wiring, start/shutdown, switch rows) written | section 11 (consumers), then 10 | P06 sections 1-14 read (tables in full); notes updated |
| 2026-11-26 18:53 | sections 11 (consumers) and 10 (cross-part summary table) written | section 12 (intent sources), then 13 | P06 section 7 table carried; section 10 from the parts' summaries |
| 2026-11-26 18:54 | section 12 (intent sources against the code) written | section 13 (inherited items: 48, 16 OIR, 16 records, N1-N6, 43+5 and PQ-06) | built from P01 s9, P02 s10, P03 s11, P04 s12, P05 s4/7/9, P06 s10 |
| 2026-11-26 18:58 | section 13 intro, 13.1 and 13.2 (the 48 items) written | 13.3 to 13.6 | AFR cells of 43+5 records and PQ-06 read by notes/ASSEMBLY_afr.py (read-only; an addition beyond the parts, for the hand-back) |
| 2026-11-26 19:00 | sections 13.3 (16 OIR), 13.4 (16 records, flagged), 13.5 (N1-N6), 13.6 (5 + 43 + PQ-06; Claude's assignment decisions, flagged) written | section 14 (boundaries by owner topic) | register cells copied from AFR (read-only reader) |
| 2026-11-26 19:02 | section 14 (boundaries by owner topic A01-A20; wording note; citation differences) written | section 15 (consolidated AP list and UNKNOWN list): extract all AP/U items to notes first | — |
| 2026-11-26 19:05 | section 15.1 part 1 written (A08-AP-01 to A08-AP-50: P01, P02, P03 points with merges AP-28, AP-31, AP-34, AP-44, AP-47, AP-48) | 15.1 part 2 (P04 to P07 points: A08-AP-51 to A08-AP-92) | consolidation plan: 104 points -> 92 entries; 61 unknowns -> 40; 27 R IDs -> 25 questions + 1 withdrawn |
| 2026-11-26 19:06 | section 15.1 complete (A08-AP-01 to A08-AP-92) | 15.2 (UNKNOWN items A08-U-01 to A08-U-40) | — |
| 2026-11-26 19:08 | section 15.2 written (A08-U-01 to A08-U-40; 8 merged entries hold 29 items) | section 16 (questions A08-Q-01 to A08-Q-25; P06-R1 withdrawn) | references to U and Q numbers fixed |
| 2026-11-26 19:09 | section 16 written (A08-Q-01 to A08-Q-25; P06-R1 withdrawn listed) | section 17 (evidence index), then 1 and 2, then header | — |
| 2026-11-26 19:09 | section 17 (evidence index) written | section 2 (in brief), then section 1 and the header | part counts verified by script: 1,152 statements |
| 2026-11-26 19:11 | section 2 (A08 in brief) written | section 1 (1.1 to 1.10) and the header fields | — |
