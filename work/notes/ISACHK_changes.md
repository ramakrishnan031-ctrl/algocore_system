# ISA checker: change log (scratch; copied into the file's Check log at the end)

Format: row | before -> after | reason | source (algocore_system at 20e267d unless stated)

## Section 1 (header, 1.1 to 1.4): checked
- Clone checks re-run 27-Nov-2026 13:50 IST: legacy 970aabf clean; algocore 20e267d clean.
- git diff --stat 52cc811 20e267d: only TCR (6 lines) outside the A08 folder: confirmed. e0439f2..52cc811: DR, TCR, A08 inventory: confirmed.
- Line counts confirmed: MSII 375, DR 583, TCR 162, OIR 4,255 (261 entry headings), AFR 1,449, SRCINV 113, the five technical records 4,298.
- DR entry ranges confirmed (D-07 L93-105, D-12 L163-175, D-17 L233-245, D-21 L289-301, D-23 L317-329, D-24 L331-343, D-25 L345-357, D-28 L387-399, D-36 L499-512, D-39 L541-553, D-40 L555-567, D-41 L569-583); approval dates D-30 06-Nov, D-31 09-Nov, D-32 11-Nov, D-33 14-Nov, D-35 17-Nov, D-37 20-Nov, D-40 25-Nov confirmed.
- DR search claim (hits only in D-21, D-36, D-39, D-40, D-41) confirmed; MSII search: one further hit L309 (A12's backfill script, word match only): no change.
- STUDY counts confirmed: 92 AP (15.1), 40 U (15.2), 25 Q (16); STUDY L3 and TCR L150/L151 quotations exact.
- Missing source found: D-38 (DR L527-539; the brief lists D-38 to D-41): added as IS-096 (section 2.1) and to the header and 1.2 lists.

## Section 2.1 (IS-001 to IS-018; IS-096 added): checked
- All quotations of IS-001 to IS-018 located at the cited lines (MSII L12-L23, L36, L96, L114, L119-L123, L132, L146-L150, L159, L186, L195, L218, L222, L231, L251; DR D-21, D-36, D-39, D-40, D-41; TCR L141-L158; DOC04 L62-L100; DOC06 L60-L69; DOC08 L31, L73-L84, L92, L139, L145, L157; SRCINV L24, L75, L104, L105, L111; WSO, OPW, PMA lines; R01, R02, R03, R03A, RMI lines; STUDY L3, L28, L81-L100, L700, L736-L745, L1024-L1026; RTR A08 rows; A07 RTR L533; AFR L16-L22; P07-S012, S014, S016, S067, S068, S097, S098).
- IS-010 | Rationale (L297): Rama said the repositories differ "in the S&R change and configuration settings" -> the Rationale's words given as the register's, with his own words of L299 ("S&R Change and Config settings") | a register paraphrase was quoted after "Rama said" (attributions to Rama exact) | DR L297, L299
- IS-013 | "the retest monitor parks a candidate ..." -> `RetestDiverter.maybe_divert` parks a candidate ..., `RetestMonitor` then polls (the record's retest-monitor entry) | R02 L868 names the diverter as the parker | R02 L868
- IS-013 | FACT "no A08 part checks these records' A08 statements against the baseline" -> no A08 part cites these records or checks them record by record; P03-S137 and P03-S175 answer note N1 (the records' S&R shadow database) at the A08 side | search of STUDY and evidence re-run: no citation of the five records; P03-S137/S175 address N1, which derives from the records via A03 RTR L199 | P03 L217, L267
- IS-016 | "(1) FACT / HISTORICAL", "(2) ...", "(3) Rama's treatment for the new system" (L11 to L14) -> the register's own numbering 1 to 3 with exact wording; note that entries write (3) "Rama's new-system input" | misquotation: L11-L14 number the kinds "1." to "3."; "(3) Rama's treatment for the new system" occurs nowhere | OIR L11-L14, L884
- IS-016 | "the Status cell of all 16 is one text" -> "the summary-table Status cell of all 16" | P07-S068 states it for the summary rows; each entry's own Status field is longer and dated | P07-S068; OIR L883
- IS-096 ADDED | D-38 (L527-L539; Exact decision L534; Rama approval L537; A07 RTR L164) | completeness: the writer's brief names D-38 to D-41; D-38 is a boundary decision whose "every other interface keeps the owner" rule covers A08's processor call sites; no A08 file cites it | DR L527-L539; A07 RTR L164; P04-S036
- Header and section 1.2: D-38 added to the Decision Register lists.
