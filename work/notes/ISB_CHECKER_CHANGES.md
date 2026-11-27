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

## C3 (section 2.2)
- IS-514 — quote ""≥2 distinct method-types"" -> "">=2 distinct method-types"" — CONFL L20 reads ">=2 distinct method-types contribute"; no source has "≥2 distinct method-types" (SYSCFG L526 has "≥2 method-types", the commit ">=2 method-types") — CONFL L20 re-read.
- Verified unchanged: IS-512, IS-513, IS-515 to IS-524 (quotes located; blame dates; "visual-review" search re-run: only SYSCFG L519, CFGLOADER L1159, CONFL L47 for S&R, GUI hits otherwise; "only HIGH would ever drive a flag" and the test_config_loader comment confirmed absent from the STUDY and its parts).
- Residual (records observation for Claude, not changed): the STUDY's A08-AP-01 also quotes "≥2 distinct method-types", which matches no source exactly.

## C4 (section 2.3)
- IS-530 — source "(its live sentences; the paper branch named by line only)" -> "(L395, L397 and L401 to L402 quoted; the paper branch's token-file description, L397 to L400, named by line only)" — the row quotes "for market data only (parity)" and "fails safe → fetch_failed rows" from L401 to L402, which are not live-only sentences — MAIN L394 to L403.
- IS-541 — source "EXPECTED L351 to L358 and L386" -> "EXPECTED L4, L351 to L358 and L386"; "EVC ... L271" -> "EVC ... L270 to L271"; date cell adjusted (L4 a5c3704d...; L270 4959111a...) — the quotation "Frozen 01-Aug-2026 against deployed code 297b587" is EXPECTED L4 (blame a5c3704d...); "corrected ×4→×5" starts on EVC L270 — EXPECTED L1 to L8, EVC L266 to L272.
- IC-510 — "(EVC L271)" -> "(EVC L270 to L271)" — same reason.
- Verified unchanged: IS-525 to IS-529, IS-531 to IS-540 (FETCH, MAIN L3414 to L3512, L3540 to L3573, L3680 to L3690, L3720 to L3736, L3762 to L3838, L1690 to L1746, ZBUILD, ZCACHE, ZWARM, PROC L183 to L234, L354 to L390, SMAP L230, L243, L252, PATHS L207, L209, L383 to L397, L399 to L412, IA L383, L801 re-read; ZCACHE evict_expired/size/clear: no caller).
- New conflict found (to add in C10 as IC-514): MAIN L3417 to L3418 "built ONCE if EITHER the V1 observer or the V2 WAIT_FOR_RETEST feature is enabled" vs the later comments L3424 to L3425, L3466 to L3467, L3470 to L3471, L3474 to L3476 (structure exit, regime, V3 chain, watchlist share the closure); code L3480 six switches (P02-S148; A05 HA-09).

## C5 (section 2.4)
- IS-559 — source "w2 ... L76 to L82" -> "L74 to L82" — the quotations "CANNOT degrade live trading" and "on a different endpoint bucket than trading" are at L74 to L76 (same commit ce9e4d32...) — w2 doc L72 to L83.
- IS-560 — added "(FACT: at the baseline that call is only the fallback when the `now_ist` default raises, BACKFILL L108 to L112; P03-S125)" — the audits' "naive datetime.now() derives the trade date" is accurate only for the fallback branch — BACKFILL L105 to L112.
- Verified unchanged: IS-542 to IS-558, IS-561 (DETECT, PROC L614 to L660, MAIN L3489 to L3508 and L1693 to L1694, FLAGS in full, SCHEMA L1246 to L1292, STORE L1963 to L1977, BACKFILL in full, commit 09ea7254 and a47efca1 messages, CRONREG L405 to L425, SMAP L226 to L237, L589, L630, L1228, PATHS L217, L247, L414 to L425, PREC14 L137, L204, L244, BATCH16 L172, MP28 L355 to L359, MP30 L317, MP01 L1815, DRP0 L100, L165, L181, L235, the 15-Jul and 25-Jul audits, IA L806, EVC L83, L138, EXPECTED L116 to L124, STOPPROC L288 to L294). SYSCFG has no `retest_sl_buffer_pct` key (grep).
