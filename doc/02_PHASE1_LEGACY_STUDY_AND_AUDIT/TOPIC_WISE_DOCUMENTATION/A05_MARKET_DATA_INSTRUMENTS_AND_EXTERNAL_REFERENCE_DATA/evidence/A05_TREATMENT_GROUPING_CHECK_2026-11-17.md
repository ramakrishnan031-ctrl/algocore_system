# A05 evidence: the program check of the treatment grouping

**Status:** APPROVED — evidence for the A05 RECONCILED TOPIC RECORD, approved by Rama on 2026-11-17 with the A05 topic package (Decision Register, D-35)
**Date:** 2026-11-17
**Revision history:** First version, 2026-11-17. Approved by Rama on 2026-11-17 with the A05 topic package (Decision Register, D-35): status marked APPROVED; content unchanged.
**Purpose and scope:** Records the program check of the grouping of A05's 89 ISSUEs into the 19 treatment groups of the treatment round of 17-Nov-2026 (Document 04, section 4, step 8), which ChatGPT's re-check of the treatment-round file asked to be kept in the topic's final evidence package. It shows that each ISSUE is in exactly one group, that no UNKNOWN / NOT ESTABLISHED or MATCH item is in a group, that each ISSUE row of the register names its own group with the status AGREED, and the choices Rama adopted. It decides nothing and changes no finding, treatment or count; the Audit Findings Register governs.
**Source:** the Audit Findings Register (`doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/AUDIT_FINDINGS_REGISTER_2026-11-06.md`), its A05 section ("A05 treatment decisions" and "A05 findings"), as committed at `6a089d3` (the treatment round was committed at `b44857d`; `6a089d3` changed only the Topic Completion Register). The check read the committed register text with `git show` and parsed it with a script of the main session's own (not kept, D-17); no legacy file was read or run.
**Related documents:** the A05 RECONCILED TOPIC RECORD (section 18.3); the A05 AUDIT (`A05_AUDIT_2026-11-15.md`); the Open Issues Register (A05 entries) and the Topic Completion Register (entry A05).

## 1. Method

The script took the 19 group bullets of "A05 treatment decisions" (each bullet's declared count, its listed findings and Rama's recorded choice) and the 113 rows of "A05 findings" (each row's classification, treatment cell and status cell), and tested the conditions in section 2. A test passes only if it holds for every group and row. The same conditions were tested before the treatment round was put to Rama, on the working grouping (89 findings, 24 UNKNOWN, 19 groups); the result below is from the committed register.

## 2. Results

| Test | Result | Detail |
|---|---|---|
| Groups present | PASS | 19 groups (TG1, TG2, TG3, TG4, TG5, TG6, TG7, TG8, TG9, TG10, TG11, TG12, TG13, TG14, TG15, TG16, TG17, TG18, TG19) |
| Declared counts equal listed findings | PASS | declared total 89 |
| Findings listed in the groups | PASS | 89 listed |
| No finding in two groups | PASS | 0 duplicates |
| Every ISSUE row is in a group | PASS | 89 ISSUE rows; missing: none |
| No UNKNOWN / NOT ESTABLISHED item in a group | PASS | 24 UNKNOWN rows; in a group: none |
| No MATCH item or unlisted ID in a group | PASS | IDs not among the 113 rows: none |
| Each ISSUE row names its own group, status AGREED | PASS | mismatches: none |
| UNKNOWN rows untreated | PASS | mismatches: none |
| Rama's choices: 16 B and 3 A | PASS | B 16, A 3 (TG3, TG7, TG18) |

Rows of the A05 section: 113 (89 ISSUE, 24 UNKNOWN / NOT ESTABLISHED; MATCH items have no row).

## 3. Group membership

| Group | Findings | Members | Rama's choice (ChatGPT's suggested choice) |
|---|---|---|---|
| TG1 | 6 | LF-01, LF-02, LF-03, LF-05, LF-08, LF-09 | B — ACCEPT WITH QUALIFICATION |
| TG2 | 4 | LF-04, LF-10, LF-11, LF-12 | B — ACCEPT WITH QUALIFICATION |
| TG3 | 3 | LF-13, LF-14, LF-15 | A — ACCEPT |
| TG4 | 3 | CA-01, CA-02, CA-03 | B — ACCEPT WITH QUALIFICATION |
| TG5 | 3 | CA-04, HA-03, DC-03 | B — ACCEPT WITH QUALIFICATION |
| TG6 | 3 | CA-05, CA-06, CA-11 | B — ACCEPT WITH QUALIFICATION |
| TG7 | 3 | CA-07, CA-08, CA-10 | A — ACCEPT |
| TG8 | 3 | LF-17, CA-09, XC-06 | B — ACCEPT WITH QUALIFICATION |
| TG9 | 3 | CM-06, CM-08, CM-10 | B — ACCEPT WITH QUALIFICATION |
| TG10 | 5 | HA-01, HA-02, HA-06, HA-07, HA-08 | B — ACCEPT WITH QUALIFICATION |
| TG11 | 4 | IN-01, IN-02, IN-03, IR-08 | B — ACCEPT WITH QUALIFICATION |
| TG12 | 5 | IN-04, IN-05, CA-12, IN-07, IN-08 | B — ACCEPT WITH QUALIFICATION |
| TG13 | 4 | IR-01, IN-06, IR-10, IR-13 | B — ACCEPT WITH QUALIFICATION |
| TG14 | 6 | IR-03, IR-04, IR-05, IR-06, IR-07, IR-11 | B — ACCEPT WITH QUALIFICATION |
| TG15 | 7 | DC-01, DC-02, DC-04, DC-05, DC-06, DC-08, DC-10 | B — ACCEPT WITH QUALIFICATION |
| TG16 | 5 | FB-01, FB-02, FB-03, FB-04, FB-05 | B — ACCEPT WITH QUALIFICATION |
| TG17 | 4 | XC-02, XC-03, XC-04, XC-05 | B — ACCEPT WITH QUALIFICATION |
| TG18 | 13 | LF-18, CA-14, CM-01, CM-02, CM-03, CM-09, HA-09, IN-11, IR-02, IR-12, DC-07, FB-06, XC-07 | A — ACCEPT |
| TG19 | 5 | LF-16, CA-15, CM-04, XC-01, XC-14 | B — ACCEPT WITH QUALIFICATION |

ISSUEs by AUDIT part: LF 16, CA 14, CM 8, HA 7, IN 9, IR 12, DC 9, FB 6, XC 8 (total 89).
