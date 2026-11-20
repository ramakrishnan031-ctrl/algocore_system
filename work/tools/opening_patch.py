import re, shutil, os
R='doc/00_PROJECT_CONTROL/04_PROJECT_REGISTERS/'
TCR=R+'TOPIC_COMPLETION_REGISTER_2026-11-04.md'; DR=R+'DECISION_REGISTER_2026-11-04.md'
FOLDER='doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION'
def rep(s,a,b):
    assert s.count(a)==1,(a[:80],s.count(a)); return s.replace(a,b)

P1=("(P1) A07 studies in full the five V3 playbook gate functions in `screening/hard_gate.py` (`gate_rr`, `gate_htf`, `gate_extreme`, `gate_confirm` and `gate_pullback`): their inputs, calculations, thresholds, units, missing-data and error behaviour and the returned `GateVerdict`; A18 owns their call sites, when its chain calls them and how it consumes the verdicts, and A07 does not audit A18's chain; `gate_rr`'s arithmetic and output are recorded faithfully, the entry, stop, target, risk and R:R decisions staying A09's and the production of S&R inputs A08's")
P2=("(P2) A07 studies `screening/entry_gate.py` fully (start and rehydration, add, polling, release, persistence calls, the callback contract and failure behaviour), traces the callback through A01's `main.py` wiring to A06's `SignalProcessor.continue_from_gate`, records that function's inputs, outputs, status and decision contract and its handoff to A09 at the interface, and studies the A07-owned `strategy_will_trade` logic invoked on the resume path, including its call at `signals/signal_processor.py` L2062; A07 does not audit the internal orchestration of `continue_from_gate`, which stays A06's, the A01, A06 and A09 portions are recorded at their interfaces only, and A06's records are not edited")
P3=("(P3) the comparison of the screening components with the actual Chartink scanner conditions (Open Issues Register, A05-25) is made when Rama supplies the conditions (screenshots or an export), and A07 proceeds meanwhile; the material, once supplied, is external evidence, admitted to the Source Inventory only on Rama's decision (Document 05, section 11.1; D-12); Claude does not contact Chartink or retrieve scanner or account data; if the conditions are not supplied, the comparison is recorded as UNKNOWN / NOT ESTABLISHED, and no scanner condition is inferred from names, URLs, comments or memory")
METHOD=("read-only helpers on both repositories, at most two at a time, the next pair started only after both helpers of the current pair have completed and their final hand-back notifications have arrived (a progress log or partial output is not completion), with saved progress and backups to the temporary branch `wip/a07-fieldwork`, scanned for identifiers before every push and never merged into `main`; Rama is consulted before any helper is started; no legacy file is run, imported or tested, and no broker, scanner, webhook or other endpoint is contacted")

# ---------- Topic Completion Register ----------
s=open(TCR).read()
entry=f"""## A07 — Strategies, screening, filtering and trade decision

| Field | Entry |
|---|---|
| Topic ID | A07 |
| Topic name | Strategies, screening, filtering and trade decision |
| Scope | Strategy selection and controls, secondary screening, hard gates, quality scoring, entry gates, step execution, rejection and acceptance outcomes, and the decision handoff: `strategies/control.py` and `strategies/taxonomy.py` (`strategies/schema.py` and `strategies/loader.py` are A02's), `screening/secondary_screener.py`, `screening/hard_gate.py`, `screening/quality_scorer.py`, `screening/entry_gate.py` and `screening/step_executor.py`, `core/strategy_direction.py`, `strategies/__init__.py` and `screening/__init__.py` (package initialisation and exports; provisional, see S1), the relevant `regime/` and `v3_chain/` integration call sites, and three scripts, `scripts/compute_strategy_metrics.py`, `scripts/strategy_registry_officer.py` and `scripts/strategy_status.py` (Master System Investigation Index, entry A07 and Appendix A). Document 08, section 3, coverage items 5 (strategy definition and use) and 6. Study baseline: trading-system-prod-snapshot at `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (D-21). Boundary: A07 owns the decision to accept, reject or advance a signal; A08 owns the technical-analysis and S&R calculations; A09 owns the entry, R:R, risk and capital decisions, and may cite the capital and governor handoff of `scripts/compute_strategy_metrics.py` (index, entry A07). The start line (Decision Register, D-38): A07's investigation of the processing flow starts at the screening call (`signals/signal_processor.py` L998 at the baseline), and A07 covers the strategy-control logic of `strategy_will_trade(...)`, called before it (L959); the strategy lookup and the processor's orchestration up to the screening call stay on A06's side (PQ-14 stays an A06 MATCH); the strategy's own entry window is A01's and the strategy governor A09's. Boundaries, as Rama decided on 20-Nov-2026 on ChatGPT's recommendations, without any change to the index (Decision Register, D-39): {P1}; {P2}; {P3}. A01's handoffs to A07 (the A01 RECONCILED TOPIC RECORD, section 15) are C11, C14, C15, C20, B-28 and B-08. A02's handoffs to A07 (the A02 RECONCILED TOPIC RECORD, section 15.2) are V-06, V-23, T-14, T-20, F-11, K-05 and K-27. A03's handoffs to A07 (the A03 RECONCILED TOPIC RECORD, section 15.2) are D-05, D-09, H-16, H-17, H-50, P-02, P-11, Q-11, Q-12, Q-22, Q-45, U-24, U-25 and E-08. A04's handoffs to A07 (the A04 RECONCILED TOPIC RECORD, section 15.2) are OA-22, RD-12, RL-11, PR-23 and CG-05. A05's handoffs to A07 (the A05 RECONCILED TOPIC RECORD, section 15.2) are CM-07, CM-22, FB-01, FB-02, FB-07 and FB-14. A06's handoffs to A07 (the A06 RECONCILED TOPIC RECORD, section 15.2) are WA-06, WA-07, PQ-02, PQ-08, PQ-13, PQ-14, PQ-15, EV-02, EV-11, EV-19, ET-06, ET-13 and XA-11. Each of the 51 keeps its original owners, ID, classification, status and treatment; A07 records its own side only. |
| Phase | Phase 1 (authorised by Rama, D-27) |
| Status | IN PROGRESS, since 2026-11-20: opened on ChatGPT's A07 investigation direction of 20-Nov-2026 (Document 04, section 4, step 1), issued after A06 closed and Rama approved the start of A07 the same day ("A07 is approved"; D-23); ChatGPT's review of Claude's first fieldwork checkpoint passed it with qualifications the same day, with its recommendations on the boundary points P1 to P3 and on the working method, and Rama decided them (Decision Register, D-39): "A07 studies all five (Recommended)", "ChatGPT's narrower version (Recommended)", "Later; proceed now (Recommended)" and "Approve method (Recommended)": {METHOD}; the STUDY stage. |
| STUDY | Not started. The topic folder `A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION` (D-28) holds the first evidence file, `evidence/A07_SOURCE_FILE_INVENTORY_2026-11-20.md`, DRAFT. |
| AUDIT | Not started (step 6). |
| RECONCILED TOPIC RECORD | Not started (step 10). |
| Issues raised with Rama | None yet. |
| Open issues | None yet for A07. The open issues of earlier topics that mention A07 (A02-03, A03-10, A03-11, A03-36, A03-37, A05-01, A05-25, A06-02, A06-08 and A06-12) stay in the Open Issues Register under their topics, with their IDs and statuses unchanged; A06-08 was decided by Rama on 20-Nov-2026 (D-38). |
| Reviewer | ChatGPT (Document 04, section 4, steps 5, 7 and 12). |
| Approval | None yet. Rama approves or rejects the topic document and package (Document 07, section 6.3). |
| Publication reference | Topic folder: `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/A07_STRATEGIES_SCREENING_FILTERING_AND_TRADE_DECISION/`. |
| Closure date | Not closed. |

## Topics not yet opened

A08 to A17, A20, A18 and A19, in that order"""
s=rep(s,"## Topics not yet opened\n\nA07 to A17, A20, A18 and A19, in that order",entry)
old="A06 stays CLOSED; no other field changed."
s=rep(s,old,old+" Seventy-third version, 2026-11-20: topic A07 opened on ChatGPT's A07 investigation direction of 20-Nov-2026, after Rama approved the start of A07, ChatGPT's review of Claude's first fieldwork checkpoint and Rama's decisions on it (D-39: the boundary points P1 to P3; the working method); A07 IN PROGRESS.")
open(TCR,'w').write(s)

# ---------- Decision Register ----------
d=open(DR).read()
d39=f"""## D-39 — A07 boundary decisions P1 to P3 and the A07 working method

| Field | Entry |
|---|---|
| Decision ID | D-39 |
| Date | 2026-11-20 |
| Subject | The A07 topic boundaries (points P1 to P3) and the A07 working method, decided on ChatGPT's review of Claude's first A07 fieldwork checkpoint, without any change to the Master System Investigation Index |
| Exact decision | {P1}. {P2[0].upper()+P2[1:]}. {P3[0].upper()+P3[1:]}. Working method (D-36's method for A06, applied to A07 by this decision): {METHOD}. |
| Rationale | ChatGPT's review of the checkpoint, 20-Nov-2026: PASS WITH QUALIFICATIONS. It recommended option A for P1 (the index assigns `screening/hard_gate.py` to A07, and the owner of a named file studies the file, index rule 1); a narrowed version of Claude's option A for P2, so that A07's own entry gate and strategy-control logic are fully investigated while the processor's orchestration stays with its owner (index rule 1; D-36; D-38); option A for P3, conditional on Rama supplying the conditions, without holding up the rest of the topic; and the method, with strict application of the A06 lesson on helper overlap (D-37). Its qualification on the entry-gate wording (`EntryGate.add()` has no non-test caller at the baseline; `EntryGate.start()` rehydrates any persisted `gate_state` rows and can release them; whether such rows existed in production is UNKNOWN / NOT ESTABLISHED) is applied in the A07 records. |
| Evidence | ChatGPT's A07 investigation direction of 20-Nov-2026, Claude's first A07 fieldwork checkpoint and ChatGPT's review of it, all 20-Nov-2026 (not kept as files, D-17); the Topic Completion Register, entry A07; `evidence/A07_SOURCE_FILE_INVENTORY_2026-11-20.md` in the A07 topic folder. |
| Rama approval | Rama's selections in the Claude chat on 2026-11-20: "Approve method (Recommended)"; "A07 studies all five (Recommended)"; "ChatGPT's narrower version (Recommended)"; "Later; proceed now (Recommended)". |
| Affected documents | The A07 topic folder; the Topic Completion Register, entry A07; the Source Inventory, if the Chartink scanner conditions are supplied and Rama admits them. |
| Status | APPROVED. |

**Related documents:**"""
d=rep(d,"**Related documents:**",d39)
old="Twentieth version, 2026-11-20: decision D-38 (the A06-to-A07 hand-over line, A06-08: reading (b)), Rama's decision of 20-Nov-2026."
d=rep(d,old,old+" Twenty-first version, 2026-11-20: decision D-39 (the A07 boundary decisions P1 to P3 and the A07 working method), Rama's decisions of 20-Nov-2026.")
open(DR,'w').write(d)

# ---------- evidence file ----------
os.makedirs(FOLDER+'/evidence',exist_ok=True)
shutil.copy('/home/claude/a07/evidence/A07_SOURCE_FILE_INVENTORY_2026-11-20.md',FOLDER+'/evidence/')
print('applied')
