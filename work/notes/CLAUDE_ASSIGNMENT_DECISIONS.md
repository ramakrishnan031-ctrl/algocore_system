# Claude's assignment decisions for the A08 STUDY assembly (working note; for ChatGPT's STUDY review)

- Rows H-44, U-59, U-60 (P03-S192; P06 section 9) and records A01 C40, A02 K-32 (P05-AP17; P06 section 9): treated as
  records that touch A08 code without naming A08, listed in STUDY section 13.6 with their A08 facts by part statement
  (H-44: P03 and P04; U-59, U-60: P03; C40, K-32: P05), on the same footing as the 43 records of P06-S175/S176 (Rama's
  decision of 26-Nov-2026: "List with A08 facts"). Not added to the 48 handed items; not reclassified.
- HA-03 primary part P04 (P07 checker's choice, matching A05-17 and A05-18) is kept.
- A06 PQ-06 (found by the P06 checker, P06-S189): touches A08's zone warmer without naming A08; treated like the 43
  (listed with A08 facts: P02-S080, P02-S098, P06-S094), under Rama's decision of 26-Nov-2026 "List with A08 facts".
- P06-R1 withdrawn by the P06 checker (repeats A01-10's history question, which Rama directed to stay OPEN): accepted.
- P06-R5 overlaps A07-Q19 and A07-29: the assembly keeps it, with the overlap noted, for Rama to see in context.
- Post-check corrections by Claude: P03-S157 (line ranges assigned to the right files) and P04-S126 (UNKNOWN clause
  added); each logged at the end of its part file.
- Post-check correction by Claude: P06-S051 and P06-S066 (the divert's structure stop goes only to the audit row's proposed_retest_sl; P04-S042), logged at the end of P06.

# AUDIT ownership decisions (Claude, 27-Nov-2026; for the cross-part check and ChatGPT's AUDIT review)
- CZ-13 (the detector's cap of 12 logged zones per kind; slice in `detector.py`) and CZ-12 (the confidence class read by
  no consumer) stay COUNTED in part CZ, because the allocated items (A08-AP-12 and the core's confidence class) are CZ's
  and no item allocated elsewhere covers them; parts VO, RT and SC CITE them and do not count them again.
- Split items (A08-AP-05, AP-06, AP-07, AP-13, AP-16): CZ counts the core's side only; FC counts the fetcher's /
  zone builder's side (A05 CM-05, A05-27, A05-28; AP-25); VO counts the PATHS.md L417 point (AP-48).
