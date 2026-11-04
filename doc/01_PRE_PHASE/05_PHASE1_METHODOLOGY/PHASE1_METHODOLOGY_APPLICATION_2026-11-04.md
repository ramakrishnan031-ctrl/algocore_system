# Preparation for Applying Document 08 in Phase 1

**Status:** DRAFT — Pre-Phase working record, for ChatGPT review
**Date:** 2026-11-04
**Revision history:** First version, 2026-11-04: first draft of Pre-Phase Deliverable 5, under ChatGPT's Pre-Phase instructions of 04-Nov-2026, section 9 (Decision Register, D-16, D-20 and D-22). Corrected, 2026-11-04, after ChatGPT's review of Pre-Phase checkpoint 4, section D: the Open Issues Register kept to the scope of Document 10, section 6 (sections 2, 6 and 7); the recommended topic-sequencing rule, OPEN FOR RAMA (sections 1 and 10); study prerequisites distinguished from code imports (section 2); the evidence package (section 4); conflicting intent sources (section 5); unresolved issues kept visible (section 8); references updated to ChatGPT's proposed index.
**Purpose and scope:** How Document 08, which remains the governing Phase 1 methodology, is to be applied to the topics of the Master System Investigation Index: their order, depth and deliverables (Document 02, section 2; D-16). This is a plan only. It applies Document 08 to no module, gives no module-level investigation instructions, conducts no trial audit and changes no foundation document.
**Basis and labels:** Each point either applies a rule of a governing document, cited beside it, or is a working method marked PROPOSED, for ChatGPT's review and Rama's approval at the Pre-Phase → Phase 1 gate. Where a point and a governing document differ, the document decides. Other labels follow Document 04, section 6. The plan draws on the Source Inventory (SRC-nn), the whole-system overview, the operational workflows, and ChatGPT's proposed Master System Investigation Index of 04-Nov-2026 (PROPOSED; Rama approves the index at the gate).

## 1. Grouping and order of the topics

- The Master System Investigation Index sets the topics and, for each, its scope, components and paths, coverage items, dependencies and order (Document 10, section 1; D-16). ChatGPT proposed its content on 04-Nov-2026: topics A01 to A19 in order positions P1 to P9, and synthesis deliverables S1 to S5. Claude keeps the file, and Rama approves the index at the gate (Document 05, section 11.1; D-13); until then, its topics are PROPOSED.
- Phase 1 runs topic by topic, in the index's order (Document 02, section 3). RECOMMENDATION (ChatGPT; Claude agrees), OPEN FOR RAMA, to be decided before Phase 1: topics run strictly in sequence. The next topic's study does not begin until the previous topic's package has completed ChatGPT's review and Rama has approved it, or has rejected it and the required rework is complete. Basis: "topic by topic" (Document 02, section 3), the 13 steps of Document 04, section 4, and D-11; it avoids overlapping evidence and unresolved handoffs. It also matches the working rule of Rama's earlier project recorded in Document 05, section 11.2 (each matter finalised or explicitly left open, then the next topic), which is not yet confirmed for this project.
- The proposed order (INTERPRETATION of the dependency map and the workflows): the foundation first, because every area imports `core/` (orchestration, configuration, storage); then the broker and market data; then the trade path in pipeline order (signal intake → screening and trade decision → S&R → sizing, risk and capital → order processing → position management and exits → end of day and reconciliation); then the controls around it (kill switch and recovery, alerts, reports and monitoring); then the schedule and deployment; then the V3 and shadow extensions; then testing.
- Each component or path has one owning topic; the other topics cite the owner and record their own boundary handoffs (Document 04, section 5.2; the proposal's index rule 1). Rama may adjust the granularity at the gate, keeping coverage items 1 to 24 and the single-owner rule (the proposal's index controls).
- Five coverage items of Document 08, section 3 are built across the topics as synthesis deliverables, not module topics (the proposal's S1 to S5): the repository and complete file map (item 2), re-based on the baseline; known issues and historical findings (item 22), during the topics; the complete end-to-end walkthrough (item 21), after them; legacy lessons and V2 inputs (item 23), at the end of Phase 1; and the master manual index (item 24), kept throughout.

## 2. Cross-topic flows and dependencies

- Flows that cross topics are traced end to end; an issue found at a boundary is recorded against the topic that owns it and cross-referenced from the others, without a duplicate register entry (Document 04, section 5.2).
- The index's prerequisites are the study order: the order in which a reliable investigation can be made. They are not code dependencies; the import graph is separate evidence (the proposal's index rule 2). Some imports run against the study order: for example, `core/` also imports `orders/`, `alerts/`, `strategies/`, `sr_detector/` and `utils/` (an OPEN QUESTION for Phase 1).
- PROPOSED: each topic records its boundary handoffs at the STORAGE / HANDOFF → NEXT CONSUMER steps of the chain of Document 08, section 4, naming the topic on the other side. The topic that owns the step where a decision is taken traces it in full; the other topics cite that trace and do not repeat it.
- A boundary with a topic not yet studied stays a clearly labelled pending boundary question (OPEN QUESTION) in the topic's own record (Document 04, sections 8 and 10), and is checked when that topic is reached. It goes to the Open Issues Register only if it becomes an unresolved issue of a Phase 1 topic that needs tracking (section 7).
- PROPOSED: where code depends both ways across a boundary, the earlier topic in the study order records the boundary and the later topic completes it.
- The end-to-end walkthrough (S2, item 21) joins the boundary records into whole flows, following the eight workflows of Deliverable 3.

## 3. Bounding each topic's study and audit

- At its opening, each topic records the eight steps of Document 04, section 3, including what it includes and excludes; material scope ambiguity is referred to Rama.
- PROPOSED: the scope is stated so that it can be checked: the owned modules and paths (from the index), the entry points, the flows covered, the configuration keys and environment variables (by key) and the database tables.
- The study traces inputs, logic, validations, outputs, storage and handoffs, and records the unknowns (Document 04, section 4, step 4), along the chain of Document 08, section 4, with the important calculations documented as Document 08, section 5 requires.
- The audit covers every area and flow of the same scope, on every route (normal, rejection, error, retry, restart and mode branches), and looks for every kind of issue (Document 04, sections 5.2 and 5.3; Document 08, section 6, steps 3 and 4). It is not limited to configuration settings or to one example.
- Live only: paper-mode workflows are excluded, and shared code is examined only where necessary to establish actual Live behaviour (Document 08, section 2).
- Each topic studies the baseline `970aabf3c78d777d9d34549e021f7c8e756c7bdb` and notes where its code changed after the last recorded deployment (`686df1c` and `7d4970a`, 02-Sep-2026); whether production ran those later commits is UNKNOWN / NOT ESTABLISHED (D-21).
- Nothing in the legacy system is corrected, run or revived, and legacy behaviour is never silently corrected in the documentation (Document 04, section 5.5; Document 08, sections 1 and 7).

## 4. Collecting and citing evidence

- Claude studies the local read-only clone at the baseline (Document 04, section 4, step 2; Document 06, section 3).
- Each finding records, where supported, the exact file path, the commit studied, the function or class, the line reference and the other items of Document 04, section 7 and Document 08, section 4.
- For each item, every place where the code reads, sets or overrides it is found by searching for its name, not only by following the obvious caller (Document 08, section 6, step 2).
- Evidence priority follows Document 06, section 4.1: the actual code first; documentation, configuration files and comments are compared with the code, never taken in its place.
- PROPOSED: sources are cited by path and by their Source Inventory reference; every file of the legacy repository falls under SRC-10. Admitting, removing or reclassifying a source is Rama's decision (Document 05, section 11.1; D-12).
- Credentials are recorded by existence, type and location category only, never by value; the production repository's public exposure is not raised as an issue (Document 08, section 11), and no credential-leak issue or investigation is opened before Phase 1 is complete (D-07).
- PROPOSED: the evidence package cites, for each finding, the exact admitted source and commit, and keeps only the evidence needed to substantiate the findings: no large source extracts, and no credential value. It sits with the topic document in the topic's subfolder of `doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/` (Document 07, section 3). Instructions, follow-ups and intermediate reviews are not kept (D-17).

## 5. Identifying intended behaviour

- For each item, intended behaviour is taken from every source that states or implies it (Document 04, section 5.1): configuration (YAML, JSON, CSV, and environment variables named by key), documents (manuals, the legacy technical records, README files), comments and docstrings, function and variable names, log and alert texts, earlier records, and Rama's statement of how he intended the system to work.
- PROPOSED: in the admitted sources, these are found in `config/` (SRC-15) and the keys of `.env.example` (SRC-35); the comments, docstrings, names, and log and alert texts of the topic's own code; the legacy project's own documents (SRC-19, SRC-30 and SRC-36 to SRC-39), as HISTORICAL; the five existing technical records (SRC-40 to SRC-44); and Rama's dated statements.
- The five existing technical records rest on the testing copy, so their statements are checked against the production code at the baseline (D-21). A statement found wrong is corrected in the topic document, with its evidence, and the record stays unchanged (Document 08, section 9).
- Each intended behaviour is recorded with its source (Document 04, section 5.4). PROPOSED: where sources of intent conflict, each is recorded separately with its source and the conflict is referred to Rama; neither AI chooses the governing intent.
- Questions about Rama's intent are listed together for him (Document 08, section 6, step 1); his answers are recorded with their date (Document 04, section 5.4).
- Where no source states the intent, the code is still audited for defects of its own (Document 04, section 5.1).

## 6. Handling UNKNOWN / NOT ESTABLISHED

- Both legacy VMs were terminated, and no backup of their databases, logs or crontab is known (Document 06, section 4.2; SRC-50). Runtime behaviour not supported by surviving evidence is UNKNOWN / NOT ESTABLISHED and is never invented (Document 06, section 4.2).
- A schedule, job or value found in the repository or in a document is not evidence that it ran or was in force; where only runtime evidence could decide a point, the audit records UNKNOWN / NOT ESTABLISHED (Document 08, section 6, step 5, and section 10).
- Surviving external evidence that Rama supplies is entered in the Source Inventory with its origin and cited as external evidence (Document 06, section 4.2). None has been supplied as of 04-Nov-2026; Rama reports that Telegram and email contain routine production-system alerts only (SRC-51).
- Every UNKNOWN is recorded in the topic's study or audit record, whether or not it enters a register (Document 04, sections 4, step 4, and 5.4). PROPOSED: each states why it is unknown and what evidence would settle it.
- An UNKNOWN is not, by itself, an Open Issues Register entry; it enters that register only as part of an unresolved issue of a Phase 1 topic (section 7). It is not converted into an assumption, closed or discarded (Document 05, section 8), and missing facts are not reconstructed from memory or guesswork (Document 04, section 8).

## 7. Carrying findings and open questions between topics

- Demonstrated issues and findings are entered in the Audit Findings Register (Document 10, section 7; Document 08, section 6, step 7).
- An issue is entered in the Open Issues Register (Document 10, section 6) when it is an issue of a Phase 1 topic that remains unresolved, needs Rama's treatment, or needs an owned next action. It stays there, and in the topic document, until resolved (Document 05, sections 8 and 11.3).
- A boundary issue is entered once, against the owning topic, and cross-referenced from the other topic; register entries are not duplicated.
- Each topic's opening reviews the earlier findings and open issues (Document 04, section 3, step 6); open issues are carried into the next topic where relevant, and into Phase 2 (Document 04, section 12; Document 05, section 11.3).
- PROPOSED: a later topic cites an earlier finding by its register identifier and does not copy it. A later fact that changes an earlier finding is recorded as a change to that finding, with its evidence (Document 05, section 11.1, timing rule 5).
- The registers are updated at the times set in Document 05, section 11.1. The Topic Completion Register (Document 10, section 3) shows each topic's status (Document 10, section 4).
- The agreed treatment of an issue is input to Phase 2. It does not decide the new design and does not change the legacy system (Document 08, section 12).

## 8. Topic deliverables and evidence packages

- For each topic (Document 04, section 4; Document 08, section 8): the study; the separate technical audit, whose audit table records each item with the fields of Document 04, section 5.4, matches included (Document 08, section 6, step 6); the topic's issues as raised with Rama, each with its agreed treatment or OPEN status (Document 04, section 5.5); the reconciled topic document, which keeps distinct study and audit sections; and the evidence package. The topic document and its evidence form the topic package (Document 04, section 4, step 11).
- With each package, the Audit Findings Register and the Open Issues Register are updated, and the Topic Completion Register whenever the topic's status changes (Document 05, section 11.1).
- Unresolved issues stay visible in the topic document and in the registers, cross-referenced between the topics they touch (Document 05, section 11.3). Whether a topic can close with unresolved issues is OI-04, which stays OPEN (Document 05, section 11.2).
- Each document carries the document-control fields of Document 07, section 4 and a dated file name (Document 07, section 5).
- The names of the topic document types are OPEN (OI-07; Document 07, section 5). OI-04 and OI-07 are to be settled before Phase 1 (D-20); this plan does not settle them.

## 9. Where ChatGPT's review and Rama's approval come in

For each topic (Document 04, section 4, steps 1 to 13; Document 07, section 6.3; D-11):

1. ChatGPT prepares the investigation direction and focused questions (step 1).
2. Claude carries out the study; ChatGPT reviews and challenges it, and gaps return to Claude (steps 2 to 5).
3. Claude carries out the audit; ChatGPT reviews and challenges it (steps 6 and 7).
4. Every issue is raised with Rama, with ChatGPT's and Claude's recommendations; Rama decides its treatment or leaves it OPEN (step 8; Document 04, section 5.5).
5. The findings are reconciled into the topic document, and Claude prepares the topic package (steps 9 to 11).
6. ChatGPT reviews every file of the package and reports to Rama in short, plain English (step 12).
7. Rama approves or rejects the topic document and package; ChatGPT's review alone does not finalise it (step 13).
8. Claude marks the approved document APPROVED, commits it and updates the registers; ChatGPT verifies the commit (Document 07, section 6.3).
9. The topic closes when the checklist of Document 04, section 11 is met; closure with unresolved issues depends on OI-04.

Working drafts may be committed as DRAFT before approval: Claude runs the validator first and reports each commit to ChatGPT (Document 07, section 6.1).

## 10. Before Phase 1 can start

- Pre-Phase is complete, ChatGPT has reviewed it, and Rama has explicitly approved the Pre-Phase → Phase 1 transition (Document 02, section 6; Document 05, section 6). He approves the five Pre-Phase deliverables together at that gate, the Master System Investigation Index included (Document 02, section 2, step 5).
- Rama decides the topic-sequencing rule recommended in section 1.
- OI-04 and OI-07 are settled (D-20); for OI-07, ChatGPT proposes the names, or Claude recommends them if ChatGPT does not (Document 07, section 5). The labels carried forward ("Proposed document statuses:" in Document 07, section 4; "Suggested fields:" and "Proposed sequence:" in Document 10, sections 3 and 4) are corrected in the same revision (Document 05, section 10). That revision changes approved documents, so it follows Document 05, section 5.

**Related documents:** 02, 04, 05, 06, 07, 08 and 10; the Source Inventory; the whole-system overview; the operational workflows; Decision Register, D-07, D-11, D-12, D-13, D-16, D-17, D-20, D-21 and D-22.
