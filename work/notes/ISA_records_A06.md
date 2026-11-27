#### A06 WA-06 (L1974; headings found 1) ##### WA-06 — `triggered_at` is read as IST, as the sources say; a time-only text is dated with the day of receipt even when it is later than the moment of receipt, and no check refuses a time ahead of the receiver's clo
  L1980 - **Intended behaviour and source (all HISTORICAL, except the external page):** (1) M19 WR4, L42 (IS-39;
  L2009 - **Result and classification:** ISSUE, with MATCH parts and an UNKNOWN part. FACT; HISTORICAL; INTERPRETATION;
  L2018 - **Owner:** A06 (receiver); part PQ for the processor's age check and the expiry order.
  L2021 - **Rama:** STUDY question 10: its first half (IST) is answered by the sources at their dates; its second half (were
#### A06 WA-07 (L2024; headings found 1) ##### WA-07 — Trigger prices "nan" and "inf" pass the positive-price check, which has no finiteness, upper-bound or tick test; a symbol is refused only when empty, although WR10 names "empty/malformed"; no instrument che
  L2029 - **Intended behaviour and source (HISTORICAL):** M19 WR10, L103 to L104 (IS-46; 17-Apr-2026): `INVALID_SYMBOL`
  L2057 - **Result and classification:** ISSUE, with MATCH parts. FACT; HISTORICAL; INTERPRETATION; current external context.
  L2068 - **Owner:** A06 (the receiver's checks); A03 (storage of a NaN or infinite value); A07 to A10 (later use of the
  L2072 - **Rama:** STUDY question 9 (were trigger prices meant to be finite positive numbers?) stays a draft question; it is
#### A06 WD-10 (L2937; headings found 1) ##### WD-10 — The 503 threshold fires at 240 as P15 states, but it measures only the dispatcher's hand-off buffer: work waiting for the five workers sits in an unbounded executor queue that back-pressure never sees
  L2942 - **Intended behaviour and source:** P15, `docs/locked_decisions.yaml` L352 to L355 (2026-04-17): "Default queue
  L2968 - **Result and classification:** ISSUE. FACT; INTERPRETATION; HISTORICAL. MATCH part: the refusal point (240) and its
  L2976 - **Owner:** A06 (receiver threshold; processor dispatcher and executor, part PQ).
  L2979 - **Rama:** not needed to classify; STUDY question 18 asks what the capacity was meant to protect (OPEN FOR RAMA).
#### A06 WD-16 (L3175; headings found 1) ##### WD-16 — UNKNOWN: the runtime facts of duplicates, limits, claims and back-pressure; Chartink's retries and source addresses; the dispatcher's lag
  L3180 - **Intended behaviour and source:** not applicable (the question is what happened, not what was meant). The design
  L3202 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. No production log, database or journal is admitted
  L3205 - **Owner:** A06; A08 (the zone warmer); A17 (installed versions, working directory).
  L3208 - **Rama:** STUDY question 51 (part CK's: the alerts' unique or duplicate setting) bears on (2); no classification
#### A06 PQ-09 (L3946; headings found 1) ##### PQ-09 — UNKNOWN: the runtime and environment facts of the processor's intake (alerts sent, clock, versions, effective settings, backlogs, call durations)
  L3951 - **Intended behaviour and source:** not applicable (the question is what happened or what was installed).
  L3975 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. No production log, database, journal or deployed
  L3978 - **Owner:** A06; A14 (the notifier); A01 and A04 (the clock and its skew checks); A17 (installed versions); A08 (the
  L3981 - **Rama:** not needed.
#### A06 EV-11 (L4709; headings found 1) ##### EV-11 — The four other entry points into the processor run outside its executor: uncounted, not awaited by `stop()`, with no guard against a second resumption; their bypass of the age check, screening and claim rel
  L4715 - **Intended behaviour and source:** (1) The gate docstring L2011 to L2026 (lines 2026-04-17 and 2026-05-14): Steps 1
  L4750 - **Result and classification:** ISSUE (latent), with MATCH parts. FACT; INTERPRETATION; HISTORICAL. MATCH parts: the
  L4758 - **Owner:** A06 (the entry points and `stop()`); A07 (the gate and its rehydration); A08 (the retest monitor); A18
  L4762 - **Rama:** not needed to classify.
#### A06 EV-01 (L4254; headings found 1) ##### EV-01 — Status writes are unconditional: a later write replaces the stored status and reason, so a final status can be overwritten; no time and no trail of changes is kept, against P16 and SP9
  L4260 - **Intended behaviour and source:** (1) P16, `docs/locked_decisions.yaml` L362 (2026-04-17): "Every signal_id
  L4291 - **Result and classification:** ISSUE. FACT; INTERPRETATION; HISTORICAL. ISSUE parts: (a) P16 and SP9 ask for the
  L4302 - **Owner:** A06 (the status sequence and the overwrites); A03 (the method and the missing time column, P-02); A07 and
  L4306 - **Rama:** not needed to classify; STUDY question 29 asks which was meant (OPEN FOR RAMA).
#### A06 ET-07 (L5166; headings found 1) ##### ET-07 — UNKNOWN: the runtime and environment facts of the throttle (effective values, deployment, restarts and processes, lock order, a `place()` that declines without raising, refusals and retries that occurred, t
  L5170 - **Intended behaviour and source:** as in ET-01 to ET-06 and the match records; the legacy documents that report counts (DEC10 L12 to L13, L23; the 07-Aug document §8) are runtime claims, HISTORICAL.
  L5174 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. Settling evidence: the legacy period's `signals` rows (status and reason), the processor's log lines (`rejected at ENTRY_THROTTLED`, FIX-069 warnings), the deployed configuration, the service journal and the installed Python version; none is admitted evidence (STUDY section 1.6).
  L5176 - **Owner:** A06; A02 (effective values); A01 and A17 (processes, restarts, deployment); A10 (item 5); A07, A08, A18 (item 7).
  L5178 - **Rama:** not needed.
#### A06 XA-02 (L6358; headings found 1) ##### XA-02 — The five existing technical records against the code: no A06 claim differs, but three record statements describe the receiver and the processor otherwise than the code (construction "Flask object only", a s
  L6366 - **Intended behaviour and source:** the records are descriptions, dated 18-Sep-2026, of a worktree at `e7bf477` with
  L6398 - **Result and classification:** ISSUE (minor), with a MATCH part. FACT; HISTORICAL; INTERPRETATION (the coverage
  L6402 - **Owner:** A06 (the records' A06 claims); A01 (R03-07's boot side, R3-79); the records' own maintenance is outside
  L6407 - **Rama:** not needed.
#### A06 EV-08 (L4597; headings found 1) ##### EV-08 — A stop leaves rows `PROCESSING`, `PASSED`, `RESERVED` or parked; only earlier-day `PROCESSING` rows are swept, nothing re-reads rows at start-up and such rows are never deleted
  L4602 - **Intended behaviour and source:** (1) P16 (IS-98): every id "gets a final status before the system 'forgets' it";
  L4624 - **Result and classification:** ISSUE. FACT; INTERPRETATION; HISTORICAL. Against source (1) and the aim source (2)
  L4629 - **Owner:** A06 (the statuses the pipeline leaves); A12 (the cleanup and its docstring); A03 (retention); A09, A10 and
  L4633 - **Rama:** not needed to classify; STUDY question 37 bears on treatment (OPEN FOR RAMA).
#### A06 EV-13 (L4817; headings found 1) ##### EV-13 — UNKNOWN: whether the processor was meant to call A04's limiter; the FIX-007 pre-check has never been wired by `main.py`, and if wired it would spend a second `order` token per entry (A04 RL-18's A06 side)
  L4822 - **Intended behaviour and source:** (1) The FIX-007 comment L415 to L417 (`31075d0`, 2026-05-12): "non-blocking
  L4844 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. FACT (the wiring); INTERPRETATION; HISTORICAL. Whether the
  L4849 - **Owner:** A06 (the pre-check and the processor's wiring contract); A01 (`main.py`'s wiring); A04 (the limiter;
  L4853 - **Rama:** needed: STUDY question 24 (OPEN FOR RAMA), whether the pre-check was meant to be wired and active.
#### A06 ET-06 (L5152; headings found 1) ##### ET-06 — UNKNOWN: which of several near-simultaneous approvals the throttle admits is decided by who takes its lock first, after risk approval and reservation, not by receipt order, `triggered_at` or score; the one 
  L5156 - **Intended behaviour and source (all HISTORICAL):** (1) DEC10 L1 to L9 (2026-07-19, `5a83a46`): "Status: OPEN — Rama's call", between Option A, "leave arrival-order admission as-is: a global 20-second `min_gap` between placed entries, first-come-first-served, evaluated after risk approval", Option B (change the parameters) and Option C (the V3 ranked-admission batching window); L28: "The purpose the 20s `min_gap` was set to serve" is "not re-derived here" (IS-115; RS-06, the documents' attribution of a pending call); `docs/decisions/00_INDEX.md` L20 and L26 still list it "OPEN" at the baseline, and no later decision was found (IS-159). (2) SMAP L268 (line 2026-07-12; IS-93): the V3 allocator plan describes the present first-come-first-served admission as the design it is to replace. (3) The 19-Jul report behind DEC10 (IS-172; RS-14): the throttle's selection is by "Time/arrival-density", "quality-neutral", and the decisions it bears on "are Rama's". (4) SYSCFG L565 (committed `allocator_mode: "shadow"`; A18's, interface only; IS-203, added in the cross-part check): shadow leaves live admission "BYTE-IDENTICAL"; enforce is gated on shadow sessions, a regret review "+ Rama + an off-market cutover" (an attribution of a pending gate, not Rama's recorded intent).
  L5160 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. FACT; INTERPRETATION; HISTORICAL; OPEN QUESTION. The intent is not established: the one legacy record that poses the question (DEC10) leaves it "OPEN — Rama's call" at the baseline, and no answer of Rama is recorded (no Open Issues Register entry covers it). The code shows no defect against a stated intent: it implements the "first-come-first-served, evaluated after risk approval" admission that DEC10 and SMAP L268 describe; the undefined order among waiting threads is a property of the lock that no source addresses. A lack of intent evidence alone is not an ISSUE.
  L5162 - **Owner:** A06 (the throttle's admission order); A07 and A09 (the admission decisions before it, decision B); A18 (the allocator's ranked admission, interface only).
  L5164 - **Rama:** needed: OPEN FOR RAMA (STUDY question 43: which approval was meant to be admitted, and whether the legacy decision DEC10 was ever taken and where it is recorded).
#### A06 EV-14 (L4855; headings found 1) ##### EV-14 — UNKNOWN: the runtime facts of event creation, persistence and the handoff
  L4870 - **Result and classification:** UNKNOWN / NOT ESTABLISHED. No production log, database, journal or deployed
  L4872 - **Owner:** A06; A17 (deployment and versions); A02 (effective values); A03 (stored rows).
  L4874 - **Rama:** not needed to classify.
#### A06 XA-05 (L6491; headings found 1) ##### XA-05 — UNKNOWN: the runtime and other-owner facts on which part XA's items depend
  L6496 - **Intended behaviour and source:** not applicable.
  L6514 - **Result and classification:** UNKNOWN / NOT ESTABLISHED.
  L6516 - **Owner:** A06 (its reads and writes); A02 (configuration in force); A03 (migrations); A15, A16, A18 (readers and
  L6520 - **Rama:** not needed.
#### A06 PQ-06 (L3768; headings found 1) ##### PQ-06 — Exceptions raised outside the worker's `try` blocks end in discarded futures, unlogged, with no status and no claim release; a dispatcher that ended would not be noticed or restarted, and nothing reads `is_
  L3774 - **Intended behaviour and source (all HISTORICAL):** (1) M20 SP12, L167 to L172 (2026-04-17): "Unexpected exception
  L3806 - **Result and classification:** ISSUE (latent), with a MATCH part. FACT; HISTORICAL; INTERPRETATION; current external
  L3820 - **Owner:** A06 (the processor); A14 (no alert path for a dead dispatcher).
  L3825 - **Rama:** not needed to classify.
