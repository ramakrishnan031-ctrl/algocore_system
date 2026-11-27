# ISB writer plan (working note; not evidence)

IC rows (conflicts between legacy sources):
- IC-501 V1 switch: "default OFF/false" texts vs committed true / "stays true" (A08-AP-48)
- IC-502 V2 long-only texts vs symmetric texts (A08-AP-56)
- IC-503 strong-close wording "UPPER frac / strong 60%" vs "directional close position >= this" (A08-AP-55)
- IC-504 zone cache/warmer construction: retest switch only vs either switch (A08-AP-33)
- IC-505 zone cache reader sides: "Phase A reads resistance; Phase B will read support" vs both sides (A08-AP-33)
- IC-506 two structure-stop buffers: "match Phase A" vs "may be tuned apart; deliberate parallelism" (A08-AP-44; Q-23)
- IC-507 V1 flags and confidence: "only HIGH would ever drive a flag" vs LOW_CONFIDENCE flag table (A08-AP-38) NEW
- IC-508 sr_detector_results population: "One row per PLACED candidate" vs V2 divert audit rows (A08-AP-39, AP-43)
- IC-509 export "like sr_detector_backfill" live token vs backfill DB-only (A08-AP-77)
- IC-510 fetcher count x4 vs x5 (both omit V1 detector's) (A08-AP-83)
- IC-511 V3 plan synchronous ZoneCache read vs Step 10a async (boundary A18)
- IC-512 flag list PATHS L418 (no SELLING_INTO_SUPPORT) vs FLAGS docstring (A08-AP-38)
- IC-513 config review "decide whether a signal exists" vs "never rejects" (INTERPRETATION)

CD rows (only the code contradicts):
- CD-501 confidence meaning / >=2 method types (AP-01)
- CD-502 SR-P1 plateau / degenerate (AP-02)
- CD-503 SR-C1 across TFs (AP-03)
- CD-504 band never a single line (AP-04)
- CD-505 round number magnitude (AP-11)
- CD-506 models "Pure data"; Candidate "_emit_signal_alert" (AP-16)
- CD-507 fetched_at_monotonic (AP-19)
- CD-508 never raises / nothing propagates (AP-20)
- CD-509 within the session / intra-session (AP-22)
- CD-510 re-warm before expiry (AP-23)
- CD-511 warm returns True if zones cached (AP-25)
- CD-512 "the OhlcFetcher records a fetch_failed row" (AP-21)
- CD-513 seam "BOTH ... two paths" vs three call sites (AP-48)
- CD-514 flag table + config L517 (AP-38)
- CD-515 "a later run picks it up" (AP-40)
- CD-516 manual run never blocked (AP-41)
- CD-517 only TERMINAL / observer fires post-placement (AP-43)
- CD-518 store comment actual_* absent (AP-46)
- CD-519 restart-safe never mis-advances (AP-58)
- CD-520 release atomically incl. EOD; none survive into next session (AP-52, AP-59)
- CD-521 dedup overlap invariant (AP-53)
- CD-522 sizing_inputs / timeout_at (AP-57)
- CD-523 spot check ratio near split factor (AP-78)
- CD-524 export read-only market-data kite / working export (AP-69, AP-72)
- CD-525 export other texts (None analysis, never persists, detector per date, reference price) (AP-74, AP-77)
- CD-526 confidence class: swings never drive the R:R gate (AP-14)

ISB-R questions:
- ISB-R1 (IC-507) which flags meant for lower-confidence zones
- ISB-R2 (IC-508) the table holding V2 rows; backfill treatment
- ISB-R3 specs A..K existence
- ISB-R4 confirm "Deliberate trade-off (Rama)" quotation (for Claude/ChatGPT to decide)
Additions: Q-23 (IC-506 test comment), Q-19 (EOD comment + PB-01 analog), Q-04 (DETECT L186-L187), Q-14 (runbook not tracked; roadmap), Q-18 (A11 reuses _strong_close), Q-20 (docstring ratio)
- CD-527 V3P0 L13/L121 'None are in main' vs history (8116b74 contains V2 commits)
