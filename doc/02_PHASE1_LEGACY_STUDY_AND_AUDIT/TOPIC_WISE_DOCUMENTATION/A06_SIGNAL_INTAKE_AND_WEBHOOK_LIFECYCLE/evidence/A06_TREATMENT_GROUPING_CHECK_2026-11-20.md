# A06 evidence: the program check of the treatment grouping

**Status:** APPROVED — evidence for the A06 RECONCILED TOPIC RECORD, approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37)
**Date:** 2026-11-20
**Revision history:** First version, 2026-11-20. Approved by Rama on 2026-11-20 with the A06 topic package (Decision Register, D-37): status marked APPROVED; content unchanged.
**Purpose and scope:** Records the program check of the grouping of A06's 84 ISSUEs into the 16 treatment groups of the treatment round of 19-Nov-2026 (Document 04, section 4, step 8), which the treatment-round proposal said would be kept with the topic's final evidence package and which ChatGPT's review of the proposal checked independently. It shows that each ISSUE is in exactly one group, that no UNKNOWN / NOT ESTABLISHED or MATCH item is in a group, that each ISSUE row of the register names its own group with the status AGREED, and the choices Rama adopted. It decides nothing and changes no finding, treatment or count; the Audit Findings Register governs.
**Source:** the Audit Findings Register (`doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md`), its A06 section ("A06 treatment decisions" and "A06 findings"), as committed at `fbae332` (the treatment round). The check read the committed register text with `git show` and parsed it with a script of the main session's own (not kept, D-17); no legacy file was read or run.
**Related documents:** the A06 RECONCILED TOPIC RECORD (section 18.3); the A06 AUDIT (`A06_AUDIT_2026-11-18.md`); the Open Issues Register (A06 entries) and the Topic Completion Register (entry A06).

## 1. Method

The script took the 16 group bullets of "A06 treatment decisions" (each bullet's declared count, its listed findings and Rama's recorded choice) and the 98 rows of "A06 findings" (each row's classification, treatment cell and status cell), and tested the conditions in section 2. A test passes only if it holds for every group and row. Before the treatment round was put to Rama, the membership and count conditions were tested on the working grouping (84 findings, none twice, none missing, no UNKNOWN / NOT ESTABLISHED or MATCH item in a group), as the treatment-round proposal records, and ChatGPT's review of the proposal repeated that check independently; the result below is from the committed register.

## 2. Results

| Test | Result | Detail |
|---|---|---|
| Groups present | PASS | 16 groups (TG1, TG2, TG3, TG4, TG5, TG6, TG7, TG8, TG9, TG10, TG11, TG12, TG13, TG14, TG15, TG16) |
| Declared counts equal listed findings | PASS | declared total 84 |
| Findings listed in the groups | PASS | 84 listed |
| No finding in two groups | PASS | 0 duplicates |
| Every ISSUE row is in a group | PASS | 84 ISSUE rows; missing: none |
| No UNKNOWN / NOT ESTABLISHED item in a group | PASS | 14 UNKNOWN rows; in a group: none |
| No MATCH item or unlisted ID in a group | PASS | IDs not among the 98 rows: none |
| Each ISSUE row names its own group, status AGREED | PASS | mismatches: none |
| UNKNOWN rows untreated | PASS | mismatches: none |
| Rama's choices: 10 B and 6 A | PASS | B 10, A 6 (TG2, TG4, TG5, TG6, TG9, TG11) |

Rows of the A06 section: 98 (84 ISSUE, among them PQ-07, a provisional KNOWN DEFECT, and 14 UNKNOWN / NOT ESTABLISHED; MATCH items have no row). An ISSUE row's treatment cell reads "A06 treatment group TGn (AGREED, 19-Nov-2026)" and its status "AGREED"; an UNKNOWN row's treatment cell reads "None (UNKNOWN / NOT ESTABLISHED items receive no treatment)" and its status "UNKNOWN / NOT ESTABLISHED (no treatment)".

## 3. Group membership

| Group | Findings | Members | Rama's choice (ChatGPT's suggested choice) |
|---|---|---|---|
| TG1 | 7 | WI-12, WI-13, WI-14, WI-16, WA-06, WA-07, WI-10 | B — ACCEPT WITH QUALIFICATION |
| TG2 | 5 | WA-01, WA-03, WA-04, WA-05, WA-08 | A — ACCEPT |
| TG3 | 4 | WI-05, WI-06, WI-08, WI-09 | B — ACCEPT WITH QUALIFICATION |
| TG4 | 8 | WI-01, WI-11, WD-01, WD-02, WD-03, WD-06, WD-07, WD-08 | A — ACCEPT |
| TG5 | 7 | WD-04, WD-05, WD-09, WD-10, WD-11, WD-12, WD-13 | A — ACCEPT |
| TG6 | 4 | PQ-01, PQ-06, EV-11, WI-07 | A — ACCEPT |
| TG7 | 3 | WI-03, PQ-02, EV-08 | B — ACCEPT WITH QUALIFICATION |
| TG8 | 2 | WA-10, PQ-03 | B — ACCEPT WITH QUALIFICATION |
| TG9 | 4 | EV-01, EV-02, EV-07, XA-01 | A — ACCEPT |
| TG10 | 4 | EV-03, EV-04, EV-05, EV-06 | B — ACCEPT WITH QUALIFICATION |
| TG11 | 3 | PQ-04, PQ-05, ET-02 | A — ACCEPT |
| TG12 | 4 | ET-01, ET-03, ET-04, ET-05 | B — ACCEPT WITH QUALIFICATION |
| TG13 | 5 | WI-02, WI-18, WD-14, WD-15, EV-09 | B — ACCEPT WITH QUALIFICATION |
| TG14 | 4 | WI-04, WI-17, PQ-07, EV-10 | B — ACCEPT WITH QUALIFICATION |
| TG15 | 11 | CK-01, CK-02, CK-03, CK-04, CK-05, CK-06, CK-07, CK-08, CK-09, CK-10, CK-19 | B — ACCEPT WITH QUALIFICATION |
| TG16 | 9 | WI-15, WI-19, WI-20, WI-21, WI-25, PQ-08, ET-08, XA-02, XA-03 | B — ACCEPT WITH QUALIFICATION |

## 4. What this check does not show

It does not check the wording of the recommendations, qualifications or safeguards (ChatGPT reviewed them, and the register quotes them in full), and it does not re-examine any classification: it tests membership, counts, the treatment and status cells and the recorded choices only.
