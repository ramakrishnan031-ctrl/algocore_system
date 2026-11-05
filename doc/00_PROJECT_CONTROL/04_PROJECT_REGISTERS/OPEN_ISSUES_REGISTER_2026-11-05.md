# Open Issues Register

**Status:** DRAFT — for ChatGPT review
**Date:** 2026-11-05
**Revision history:** First version, 2026-11-05: the register created at A01's issue discussion (Document 04, section 4, step 8), with the 24 entries of the A01 AUDIT's section 10(b); batch 1 (A01-01 to A01-04) raised with Rama on 05-Nov-2026 and his answers recorded for his confirmation.
**Purpose and scope:** The project's Open Issues Register (Document 10, section 6): the issues of the Phase 1 topics that need Rama's intent or decision, each with the ten fields of Document 10, section 6. It is separate from the foundation's open items (Document 10, section 11). Claude maintains it and ChatGPT reviews it; Rama decides each issue's treatment, or leaves it OPEN (Document 05, section 11.1). It is updated with each topic package and immediately after Rama decides an issue's treatment (Document 05, section 11.1, update timing 6). An unresolved issue stays here, visible, until it is resolved or Rama decides its treatment (Document 05, section 11.3).

## How entries are recorded

- **Issue ID:** `<TOPIC_ID>-NN`. A01's numbers follow the order of the A01 AUDIT's section 10(b). Each heading keeps the AUDIT's own issue IDs and the STUDY's R numbers, so that every entry can be traced to its AUDIT record.
- **Three kinds of statement are kept apart** in each entry's Resolution field:
  1. FACT / HISTORICAL: what the legacy repository establishes, taken from the AUDIT and its evidence file, and never changed to agree with an answer;
  2. Rama's statement about the legacy system: how it was operated, or what it was meant to do (an intent source under Document 04, section 5.1, with its date);
  3. Rama's treatment for the new system: input to the Phase 2 proposal (Document 04, section 5.5). It is not an approved V2 design decision, and no legacy behaviour becomes a V2 requirement automatically.
- **Recommendations** by ChatGPT or Claude are labelled as such and stay PROPOSED until Rama decides them (Document 05, section 3).
- **Status** uses the labels of Document 05, section 3: OPEN QUESTION (OPEN FOR RAMA), for a question not yet answered; UNDER DISCUSSION, for an entry raised with Rama whose recorded answers await his confirmation of the read-back; AGREED, for a treatment that Rama has confirmed. A part of a question that Rama leaves open is shown OPEN. No entry is marked CLOSED without Rama's explicit decision of its treatment (Document 05, sections 8 and 11.3).
- **Where Rama's words are recorded:** the discussion itself is not kept (Document 07, section 3, retention rule), so each entry quotes the words that decide it.
- **Sensitive values:** none. Credentials, tokens and account identifiers are named by type only.

## A01 — System orchestration, startup, runtime and shutdown

**Source:** `A01_AUDIT_2026-11-05.md` (DRAFT, committed at `8ce3215`; passed by ChatGPT's review of 05-Nov-2026, Document 04, section 4, step 7), section 10(b), with the questions worded for Rama in its section 9, and its evidence file `evidence/A01_AUDIT_INTENT_SOURCES_2026-11-05.md`, both in `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A01_SYSTEM_ORCHESTRATION_STARTUP_RUNTIME_AND_SHUTDOWN/`. Section and record references below without a file name are to that AUDIT; line references without a path are to the legacy `main.py` at the baseline `970aabf` (D-21). 24 entries: 21 carry a STUDY R number (R4 is referenced by two of them, A01-02 and A01-04), and three have none (A01-21, A01-22 and A01-24). The ISSUEs of the AUDIT's section 10(a), established by evidence, are not entered here: their treatment for the new system is raised with Rama after these entries, and any that Rama leaves OPEN is added (Document 04, section 5.5).

**Discussion:** in batches of four. Batch 1 (A01-01 to A01-04) was raised on 05-Nov-2026; Rama answered the same day in a file prepared with ChatGPT, and his answers are recorded below for his confirmation (the read-back). Batches 2 to 6 follow, as planned in the table.

| Issue ID | AUDIT IDs | Raised with Rama | Status |
|---|---|---|---|
| A01-01 | C1 (R1) | 05-Nov-2026, batch 1 | UNDER DISCUSSION; treatment OPEN QUESTION |
| A01-02 | C2, the L2374 exit (IC-40; R4) | 05-Nov-2026, batch 1 | UNDER DISCUSSION |
| A01-03 | C2 part (ii) (R2) | 05-Nov-2026, batch 1 | UNDER DISCUSSION; historical exit code OPEN QUESTION |
| A01-04 | C4 (R4) | 05-Nov-2026, batch 1 | UNDER DISCUSSION |
| A01-05 | C5 (R5 part 3) | not yet (batch 2) | OPEN QUESTION |
| A01-06 | C6 (R6) | not yet (batch 2) | OPEN QUESTION |
| A01-07 | C7a (R7) | not yet (batch 2) | OPEN QUESTION |
| A01-08 | C8 (R8) | not yet (batch 2) | OPEN QUESTION |
| A01-09 | C10c, C11 (R9(a)) | not yet (batch 3) | OPEN QUESTION |
| A01-10 | C13 (R12) | not yet (batch 4) | OPEN QUESTION |
| A01-11 | C17 (R15, second half) | not yet (batch 4) | OPEN QUESTION |
| A01-12 | C22 (R16; handed off to A09) | not yet (batch 6) | OPEN QUESTION |
| A01-13 | C23 (R17, remaining part) | not yet (batch 6) | OPEN QUESTION |
| A01-14 | C25, W-04 (R13) | not yet (batch 4) | OPEN QUESTION |
| A01-15 | C30 (R21(b)) | not yet (batch 3) | OPEN QUESTION |
| A01-16 | C31 (R22 part 2) | not yet (batch 5) | OPEN QUESTION |
| A01-17 | C33 (R20) | not yet (batch 5) | OPEN QUESTION |
| A01-18 | C35 (R11) | not yet (batch 3) | OPEN QUESTION |
| A01-19 | C41 (R24) | not yet (batch 4) | OPEN QUESTION |
| A01-20 | B-41, C10a (R10) | not yet (batch 3) | OPEN QUESTION |
| A01-21 | B-26 (no STUDY R number) | not yet (batch 5) | OPEN QUESTION |
| A01-22 | S-44 (no STUDY R number) | not yet (batch 5) | OPEN QUESTION |
| A01-23 | S-56 (R23) | not yet (batch 6) | OPEN QUESTION |
| A01-24 | M-35 (no STUDY R number) | not yet (batch 6) | OPEN QUESTION |

### A01-01 — C1 (R1, narrowed; impact question)

| Field | Entry |
|---|---|
| Issue ID | A01-01 |
| Topic | A01 |
| Question or discrepancy | After May 2026, was `main.py --interactive` still used, for live trading or for the recovery steps in `docs/disaster_recovery.md`? Its planned use for the first paper days of April 2026 is already answered by the operations documents. |
| Evidence | FACT (C1, KNOWN DEFECT): `main.py --interactive` stops with `NameError` and exit 2 at L2534; the binding broke at commit `ab2c6d2` (05-May-2026). HISTORICAL: the operations documents of 18-Apr-2026 planned the interactive launch for the first paper days, with systemd taking over from the next day (RUNBOOK T5R02; PLAYBOOK T2R08 and T4R01; IS-1.19); `docs/disaster_recovery.md` (2026-08-02) prescribes it for recovery (L113, L134 to L136, L227); the boot record of 26-Aug-2026 shows a headless service start (`docs/audit/BOOT_PROOF_75e637c_26-Aug-2026.md` L115). Section 9, R1. |
| Impact | Bears on the defect's impact only; C1's classification rests on the code and the intent sources and does not depend on the answer (section 9, R1). |
| Owner | Rama (the answer and the treatment); Claude records them (A01). |
| Raised with Rama | 05-Nov-2026 (batch 1); answered the same day. |
| Next action | Rama confirms this record (Claude's read-back of 05-Nov-2026), and ChatGPT reviews it. The treatment for the new system is raised with the treatment of the AUDIT's section 10(a) findings, where C1 is also listed. |
| Status | UNDER DISCUSSION, awaiting Rama's confirmation. Treatment: OPEN QUESTION (not yet raised). |
| Resolution | (1) FACT / HISTORICAL: as in Evidence, unchanged. (2) Rama's statement (05-Nov-2026): "HEADLESS": the system was operated in headless mode, and interactive mode was not the operating method. The question asked about use after May 2026; the statement is recorded as given, and no date or recovery event is inferred from it. (3) Treatment for the new system: none stated yet. |

### A01-02 — C2, the L2374 exit (IC-40; with R4)

| Field | Entry |
|---|---|
| Issue ID | A01-02 |
| Topic | A01 |
| Question or discrepancy | At a live start, was a missing credential environment variable meant to give exit 5 (docstring, M41C) or exit 6 (code, FIX-163)? |
| Evidence | FACT (C2 part (iii); C12): an unset API-key variable raises `KeyError` at L2361, caught at L2371 to L2374 with a CRITICAL log line and exit 6. The sources conflict (IC-40): exit 5 in the module docstring L17 ("5 invalid args / config / missing env var"), in M41C SU10 (`consolidated_module_41_with_context.txt` L190 to L193: "If missing: print error with env var name, exit 5") and in M41C SU15 (L298); exit 6 in the code, in commit `7fc06ff` (HISTORICAL, 12-Jun-2026, FIX-163: "Falls back to exit code 6 (no restart) on missing token or credential") and in existing record 03 L174. Restart (C4; INTERPRETATION, systemd semantics; whether the declared unit was installed is UNKNOWN / NOT ESTABLISHED, B-40): under the declared unit exit 5 is not restarted since 23-Aug-2026 (commit `2f67bb8`), and the token watcher retries it up to 3 times an hour with a fresh token; exit 6 is restarted every 10 s. |
| Impact | Which code was meant decides whether the code's exit 6 departs from intent; with A01-04 it bears on how the service was to react. C2's other parts are classified without it. |
| Owner | Rama; Claude records it (A01). The restart treatment is A01-04's (C4). |
| Raised with Rama | 05-Nov-2026 (batch 1); answered the same day. |
| Next action | Rama confirms this record, including whether "exit 5" is his account of the original intent or his choice for the new system, and the count of four attempts (Claude's read-back of 05-Nov-2026); ChatGPT reviews it. |
| Status | UNDER DISCUSSION, awaiting Rama's confirmation. |
| Resolution | (1) FACT / HISTORICAL: as in Evidence; the conflict between the sources (IC-40) stays recorded, unchanged. (2) Rama's answer (05-Nov-2026): "OPTION B — EXIT 5 (invalid configuration)". Cross-check: it agrees with the docstring and M41C; FIX-163 chose exit 6, which its commit also describes as "no restart". (3) Treatment for the new system (Phase 2 input; not a V2 design decision), in the words of Rama's file: "Make the initial startup attempt. If the required credential/configuration check fails, retry at 10-second intervals for THREE ADDITIONAL RETRIES. This means FOUR ATTEMPTS IN TOTAL: one initial attempt plus three retries. If all four attempts fail, stop retrying. Trigger detailed severity-warning alerts through BOTH Telegram and email. Alerts should explain the failure, identify the failed startup check, state that the retry limit has been exhausted, and confirm that the service has stopped. Never include credential values, tokens, API keys, or other secrets in alerts." Rama's own words, which the file restates: "restart for every 10s for 3 times, then at the end of third time stop and trigger severity warning alerts (Telegram & Email) detailed". The legacy sources give exit 5 no retry (not restarted); no legacy source specified this policy. A recommendation on retries is recorded in A01-04. |

### A01-03 — C2 part (ii) (R2, narrowed)

| Field | Entry |
|---|---|
| Issue ID | A01-03 |
| Topic | A01 |
| Question or discrepancy | At a live start, was a missing or invalid `accounts.csv` meant to give exit 3 (the code written for it; IC13) or exit 5 (the exit list's entry for invalid configuration)? |
| Evidence | FACT (C2 part (ii), KNOWN DEFECT): at a live start a missing or unreadable `accounts.csv`, or a schema problem, ends the start with exit 1 (L4288 to L4290), because the pre-read at L2359 raises before the handler written for the case (L2420 to L2423, exit 3) is reached; in paper the same problems give exit 3; a short row gives exit 2 (M-33). The two sources that name the case conflict: 3 (the handler; IC13; records-check R3-40) against 5 (docstring L17, "5 invalid args / config"; SU15; Phase 0b's `return 5`, L2198 to L2201). FACT (C2, M-32, M-35; `core/account_registry.py` L6, L22, L27 to L28, L47 to L68): every live start, the headless service's included, reads the file and uses its primary row (L2360, L2545); each row holds the account identifier and the names of the environment variables that hold its credentials, not the credentials themselves (AR1, AR2; the module's docstring: it "does not store raw broker credentials"); `enabled` gates the interactive account selector (SU2; L1844); the registry's design is a single primary account, with multi-account trading deferred (AR9; IC6); the committed file has five rows, one of them primary (no identifier copied). |
| Impact | Decides which named code was meant; the code's exit 1 contradicts both named codes whatever the answer (KNOWN DEFECT). |
| Owner | Rama; Claude records it (A01). |
| Raised with Rama | 05-Nov-2026 (batch 1); answered the same day. |
| Next action | Rama confirms this record (Claude's read-back of 05-Nov-2026); ChatGPT reviews it. The historical exit code stays OPEN; if still unresolved, it is shown in the RECONCILED TOPIC RECORD and carried forward (Document 05, section 11.3). |
| Status | UNDER DISCUSSION, awaiting Rama's confirmation. The historical exit code (3 or 5): OPEN QUESTION. |
| Resolution | (1) FACT / HISTORICAL: as in Evidence, unchanged. (2) Rama's statement (05-Nov-2026) on the file's purpose: "The accounts.csv mechanism existed to allow selection of which Zerodha client code would be used when the system was started manually. The system has since moved to headless operation and is intended to operate using one configured Zerodha client code, rather than selecting among multiple client codes at manual startup." Cross-check: it agrees with the interactive account selector (SU2, SU4) and with the registry's single-primary design (AR9); the evidence adds that every live start, the headless one included, read the file for its primary row, and that the file held the names of the credential variables, not the credentials (Evidence). The historical exit code (3 or 5) is not answered: Rama's file keeps it OPEN unless the evidence settles it, and the evidence does not (the two named sources conflict). (3) Treatment for the new system (Phase 2 input; not a V2 design decision), in the words of Rama's file: "Do not retain an accounts.csv file for storing or selecting multiple client credentials. Use one configured Zerodha client code for the headless operating setup. Load required credentials from protected environment configuration, such as a local .env file. Do not store credentials in source control or expose them in reports, logs, evidence, or alerts." |

### A01-04 — C4 (R4, narrowed)

| Field | Entry |
|---|---|
| Issue ID | A01-04 |
| Topic | A01 |
| Question or discrepancy | Besides exit 6, were exit 9 and failures that repeat on every restart meant to be restarted automatically, and was the April start limit meant to remain? |
| Evidence | FACT, with INTERPRETATION for systemd's behaviour (C4; whether the declared unit was installed is UNKNOWN / NOT ESTABLISHED, B-40): the declared unit (`deploy/systemd/trading-system.service`, 2026-08-23: `Restart=on-failure`, `RestartSec=10`, `RestartPreventExitStatus=3 4 5`, no start limit) restarts exits 1, 2, 6 and 9 after 10 s without limit, so a failure that repeats on every restart loops: another program holding the lock port 5001, a database migration refused during market hours, a malformed holiday file or special session, a missing token file, a short `accounts.csv` row. Exit 9 is a broker other than Zerodha in `accounts.csv`. The token watcher (`deploy/token_watcher.sh`) caps crash restarts at 3 an hour (L13, L27, L168 to L177) but acts only on a failed or inactive unit, so it never sees the exits that systemd restarts. Exit 6 is answered by evidence: not meant to be restarted (section 9, R4). HISTORICAL: the April start limit (`StartLimitIntervalSec=300`, `StartLimitBurst=3`: STEP3 L104 to L108 and L372 to L375; STEP4A L16; commit `316b335`, 19-Apr-2026; CT-089 relied on it) was removed by commit `ccde039` (22-Apr-2026) together with a change to `Restart=always`, under a comment that the token watcher's gating would stop an always-restart loop from hammering with a stale token; commit `398dbae` (05-May-2026) returned to `Restart=on-failure` and removed that comment, without restoring the limit. For exit 9 and the repeating causes behind exits 1 and 2: no source. |
| Impact | Under the declared unit a repeating failure restarts every 10 s without end, each attempt re-running the early boot steps (C2 and C4, INTERPRETATION); the answer decides treatment, not the classification (section 9, R4). |
| Owner | Rama; Claude records it (A01). The unit file is A17's; the token watcher is A04's file, with its restart contract A13's (cross-referenced). |
| Raised with Rama | 05-Nov-2026 (batch 1); answered the same day. |
| Next action | Rama confirms this record, including whether Option A is his account of the original intent or his choice for the new system, and the count of four attempts (Claude's read-back of 05-Nov-2026); ChatGPT reviews it. |
| Status | UNDER DISCUSSION, awaiting Rama's confirmation. |
| Resolution | (1) FACT / HISTORICAL: as in Evidence, unchanged. (2) Rama's answer (05-Nov-2026), Option A: "NO — repeated failures should not restart indefinitely; retain a start limit." Cross-check: it agrees with the April start limit, CT-089's expectation and the token watcher's cap of 3 an hour; no surviving source intends unlimited restarts (the comment of 22-Apr-2026 was removed on 05-May-2026). It is not claimed that the legacy configuration had a four-attempt policy. (3) Treatment for the new system (Phase 2 input; not a V2 design decision), in the words of Rama's file: "One initial attempt plus three additional retries. 10 seconds between attempts. After four unsuccessful attempts in total, stop. Trigger detailed severity-warning alerts through Telegram and email. Do not continue an endless restart loop." Rama's own words: "Option A with same as C2 (R4): repeat 3 times start > stop & trigger alerts". Recommendation (PROPOSED; not decided by Rama): ChatGPT advised Rama on 05-Nov-2026 to "apply the retry limit consistently to failures classified as retryable. Permanent configuration errors should ideally be distinguished from temporary failures rather than repeatedly retried without purpose." Claude agrees: a missing credential, a broken holiday file or a wrong broker in the account file fails the same way ten seconds later, so retries help only with temporary causes, such as a broker connection that drops for a moment; for A01-02's case the alert, not the retries, brings the fix. The point is for the Phase 2 restart policy. |

### A01-05 to A01-24 — not yet raised

These twenty entries share five fields: Topic A01; Owner: Rama decides, and Claude records (A01, with the cross-topic owner where shown); Raised with Rama: not yet; Next action: raise them in the planned batch (Document 04, section 5.5); Status: OPEN QUESTION (OPEN FOR RAMA); Resolution: none yet. The other fields follow; the questions are those of the AUDIT's section 10(b), worded for Rama in its section 9.

| Issue ID | AUDIT IDs and question | Evidence | Impact | Batch |
|---|---|---|---|---|
| A01-05 | C5 (R5 part 3): Were `--status` and `--dry-run` meant to be usable while the service is running? | C5: both are refused at the instance lock beside the service (exit 1), and they are not read-only; that they were meant to be read-only and to stop on holidays is answered by evidence (MAIN16, MAIN17, SU6; R5 parts 1 and 2); no source addresses use beside the service. | Treatment; not needed to classify. | 2 |
| A01-06 | C6 (R6): Was the scanner check meant to run on the first start of the day, and were the repeated detection and hash checks meant as re-checks? | C6: the early session write makes the aggregate's second detection return CRASH on a normal first boot, so the scanner skip never fires and the second hash check cannot report a change; the sources conflict on the skip (IC-30: SC12 and the code comment, against CT-084 and the legacy review of 22-Jul-2026). | Treatment; not needed to classify (the boot latency is C32's). | 2 |
| A01-07 | C7a (R7): Was a crash after an earlier same-day clean stop meant to count as a crash? | C7a: any SHUTDOWN dated today, or a COMPLETE EOD row, gives WARM; SC4 step 5, the docstring and SPEC L606 to L611 state that rule, SPEC L884 to L890 implies a marker per run, and no source addresses the case. | C7a stays ISSUE with its intent not settled; treatment. | 2 |
| A01-08 | C8 (R8): Was a rejected token meant to be reported as a token problem with exit 6, and checked before the first broker call? | C8: the clock check, the boot's first broker call, runs before the token gate, and a broker rejection ends the start with exit 3 as `clock_skew`; that a broker failure blocks the start is answered by evidence (SC5); the order conflicts between sources (IC-17); no source addresses the label or exit 3 against exit 6. | Treatment. | 2 |
| A01-09 | C10c, C11 (R9(a), narrowed): When the holiday guard's own reading of the holiday file and the configured holiday list disagree, which was meant to win, and was a missing or broken holiday file meant to stop the boot or to let it continue? | C10c, C11: two readers with opposite failure policies; the guard's own parser is deliberate (fix3 L28 to L31, L70 to L73); `docs/audit/register_items_26jul2026.md` L59 to L62 left the policy conflict undecided. | Treatment. | 3 |
| A01-10 | C13 (R12): Was starting the MIS units and the optional workers before the last guards and the reconcile, and leaving them running after a failed start, deliberate? | C13, C14: MAIN8, MAIN10 and MAIN11 start every worker after the reconcile, and SPEC C.1 to C.7 after all validation; the later placements (27-Jun to 28-Aug-2026) carry no stated reason (CD-13). | Treatment. | 4 |
| A01-11 | C17 (R15, second half): Was the event-first rule meant to apply to the flatten's own broker calls during the grace? | C17: the shutdown event is set before the 15 s flatten drain, so a throttled flatten call can abort; the grace and its CRITICAL outcome are answered by evidence; no source addresses the interaction (IC-56). | Treatment; A13 is first to establish how the flatten loop treats `RateLimitAbortedError`. | 4 |
| A01-12 | C22 (R16; handoff to A09): Was a deposit after a pre-market start meant to be able to trip the drift kill ladder at 09:15? | C22: A01's part, the wiring, is a MATCH; the consequence is handed off to A09 and A13 (section 8); FIX-164's re-sync exists to pick up deposits and announces itself as INFO, while decision 11 (HISTORICAL, 28-Jul-2026) keeps the ladder without mentioning deposits (IC-51). | Needed by A09 to classify the handed-off consequence, which A09 owns. | 6 |
| A01-13 | C23 (R17, remaining part): Were the helper threads meant to follow special sessions, and was the pre-alert meant to list PARTIAL trades? | C23: fixed 14:45 and 09:15; the pre-alert omits PARTIAL trades; the DELIVERY listing and the fixed times are answered by evidence (ledger #9; P1, FRULES 1.4; IC-49, IC-50). | Treatment; the special-session part goes with A01-18. | 6 |
| A01-14 | C25, W-04 (R13, narrowed): Was a kill meant to stop the process, or to leave it running until the self-exit? | C25, W-04: no kill path stops the process; SPEC 4.6 and C.8 say a hard kill breaks the loop, while the later flatten design and documents describe a process that stays up without saying that it must (IC-48; not settled by the April operations documents or the dashboard's kill text). | Treatment; C25 and W-04 are classified ISSUE with the conflict recorded. | 4 |
| A01-15 | C30 (R21(b)): Were the NTP server and thresholds meant to be configurable, was "unreachable" meant to be a startup warning, and was the check meant to refuse above 5 seconds or above 30 seconds? | C30, S-42: the NTP check is hard-coded (2 s, 5 s, one public pool host) and blocks at 5 s (FIX-129 Item 27, "per spec") against G4's 30 s; R21(a), the unwired WARN and ALERT tiers, is answered by evidence. | Treatment. | 3 |
| A01-16 | C31 (R22 part 2): Was the lock meant to stop a hand-run copy beside the service despite `PrivateTmp`? | C31: under the declared `PrivateTmp` only the lock port, not the lock file, can refuse a hand-run copy beside the service; the documented design assumed the lock refuses it by itself; the April procedure stopped the service before a hand run, before any lock existed; R22 part 1 (a configurable port) is answered by evidence. | Treatment. | 5 |
| A01-17 | C33 (R20): Were the session-row literals `default` and `INTRADAY` intended? | C33: every write records the account as 'default' and the trade type as 'INTRADAY'; no source states the literals; the dashboard works around them and the daily report shows them (IC-37). | Treatment. | 5 |
| A01-18 | C35 (R11): How were weekend or evening special sessions meant to be traded? | C35: weekend special sessions stop at the holiday guard, evening sessions fall after the START cutoff, and the operator override that the holiday file mentions does not exist in the code; no source describes the procedure. | Treatment. | 3 |
| A01-19 | C41 (R24): Was the kill check meant to cover the second synchronous reconcile? | C41: no kill check follows the second pass inside `order_reconciler.start()`; MAIN10 and the other specifications each describe "the" startup reconcile (IC-47). | Needed to decide between an issue against intent and a design choice; can wait until A12 and A13 establish what the second pass can change. | 4 |
| A01-20 | B-41, C10a (R10, narrowed): Was the VM actually set to IST and kept in time by NTP? | B-41 (section 6.2, UNKNOWN / NOT ESTABLISHED), C10a: the holiday decision uses the host-local date; the intended set-up, IST and NTP, is answered by the documents (HISTORICAL). | Bears on exposure (C10a, C10g), not on classification. | 3 |
| A01-21 | B-26 (no STUDY R number): Was the first step at process start meant to be the logger (MAIN4), the holiday guard (SU6), or the lock (SPEC)? | B-26: logging starts after the holiday guard and the START window and before the lock; the sources conflict (IC-03). | Needed only to settle which first step was meant; treatment. | 5 |
| A01-22 | S-44 (no STUDY R number): Was a scanner outage at boot meant to be a warning (SC12) or CRITICAL (P17, SPEC C.1), with an alarm (the 27-Jul rule)? | S-44: a scanner outage at boot produces only log lines; the sources conflict (IC-31). | Treatment. | 5 |
| A01-23 | S-56 (R23): Was the TEMP-marker check meant to block above about Rs 25,000 of capital? | S-56: the check only warns and has no capital input; its docstring says it blocks above 25K "checked by caller", and the tracking note says "consider promoting" (IC-34). | Low at the baseline's file state (no markers); treatment. | 6 |
| A01-24 | M-35 (no STUDY R number): Was a primary account marked disabled meant to be refused, or traded by the headless service, and was at least one account meant to be enabled (IC5 against SU2, AR3 and the June test)? | M-35: `load()` requires exactly one primary row, but neither that it be enabled nor that any row be enabled; the sources conflict (IC-42). | Needed before M-35's final classification; latent with the committed file. | 6 |
