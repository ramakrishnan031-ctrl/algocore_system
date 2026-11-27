# ISB checker (A4) — working change list (scratch; becomes the Check log)

Format: row — before -> after — reason — source re-read.

## C1 (section 1) — verified, corrections deferred to their rows
- 1.1: both clones re-checked at start (27-Nov-2026 13:51 IST): legacy 970aabf3c78d777d9d34549e021f7c8e756c7bdb, clean; algocore_system 20e267d4997986107324f4f1385c96dc89b8b1bf, main, clean.
- 1.2 verified: STUDY section 12 L559 to L604 (writer L603: last content line; kept); P01 s9 S120..S132 + S138..S140; P02 s10 S142..S158 (S158 out of order inside); P03 s11 S193..S214; P04 s12 S161..S182; P05 s4/s7/s9; P06 s10 S179..S186: all present.
- 1.2 verified: 637 docstring+comment lines (ast clean=False + tokenize: 453 docstring, 184 comment; union 637).
- 1.2 verified: eight commits touch the 16 files (git log 970aabf -- <16 paths>): dea336ae, 55c93d3c, 9f56b077, 02357130, 536172cf, b3a5c949, 09ea7254, 132e571e.
- 1.2 verified: document search 465 lines / 80 documents (53 audit, 7 v3, 5 design, 2 web_claude, 6 single others + SMAP, PATHS, README, UNPUSHED_LEDGER, 3 MP).
- 1.2 verified: code/config pattern search 25 files; AGENTS.md, GEMINI.md, docs/locked_decisions.yaml: 0 matches.
- 1.2 verified: SRDetectorConfig starts L1153 (next class L1258); StructureExitConfig L1577 (docstring L1578); cron L90 comment, L91 job line (machine paths; not reproduced).
- section 5 "docs/locked_decisions.yaml (April 2026)": file created 2026-04-17 (bcf03b51...), last changed 2026-07-22 (245569ad...) -> correct in section 5.
- Not searched by the writer (completeness, C13): tracked documents outside docs/ (DEPLOYMENT.md, ops_dashboard/docs, deploy/, tasks/, reports/, core/*.txt) and code folders regime/, v3_chain/ (other than pb01_entry.py), screening/hard_gate.py, scripts/* (other than the three), reports/, ops_dashboard/.

## C2 (section 2.1)
- IS-502 — "the backfill and the spot check "(VM/live)"" -> "the backfill script, and the spot check "(VM/live)" (the parenthesis follows the spot check only)" — the message reads "EOD outcome backfill scripts/sr_detector_backfill.py; corp-action spot-check scripts/sr_corp_action_spotcheck.py (VM/live)."; the writer's wording attached "(VM/live)" to the backfill too (IC-509 records the backfill as DB-only) — commit dea336ae message.
- IS-507 — source "L226, ..., L281" -> "L226 to L227, ..., L277 and L281"; "Permanently stored" is the L277 heading (L281 is the list item "S&R detector results"); L226 was cited but not described -> added "the processor has "`continue_from_gate`/`continue_from_retest` resumption paths"" (L226 to L227) — CLARIF L226 to L227, L277 to L281.
- IS-511 — added FACT: the two July accounts differ (one core import against none); package imports core.time_authority since dea336ae (INIT L50), core.effect_telemetry (DETECT L27), core.candle_math (ZBUILD L16) — git grep of imports at 970aabf.
- Verified unchanged: IS-501, IS-503 to IS-506, IS-508 to IS-510 (quotes located at the cited lines; dates by blame; spec-label search re-run over the whole repository: no other "spec X" label; 8116b74 resolves to 8116b747b14729dbfaa20855b9b504eae2f02c2c).
