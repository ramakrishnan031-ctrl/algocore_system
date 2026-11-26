# P06 checker work notes (helper H14) — change list for the check log

Scripts (P06 checker; read-only; nothing imported from legacy code):
- notes/P06_CHECKER_fields.py — re-derives the 45 `SRDetectorConfig` fields, defaults and the 34 committed keys from `git show 970aabf` text. Result: 45 fields; 34 keys; only `enabled` differs; 11 fields not in the file; no YAML key that is not a field.
- notes/P06_CHECKER_stmt.py — prints a cited statement from a part file (reads workspace parts only).
- 7d4970a comparison: `git show` of both commits into a temp dir, `diff` of the sr_detector and structure_exit YAML blocks, `SRDetectorConfig`, `StructureExitConfig`, `_shutdown` (L1599-L1837 both), the wiring region (7d4970a L3376-L3797 vs base L3417-L3839) and the `_shutdown(...)` call: only difference one added line `evidence=evidence_recorder,` at base L3622; preceding hunks +33, +1, +7 = shift 41.

## Changes (ID | before -> after | reason | source)

| ID | Before | After | Reason | Source |
|---|---|---|---|---|
| P06-S003 | (e) "... thirteen modules, P06-S115" | "... P06-S124" | wrong cross-reference (S115 is the dashboard row; the test re-run is S124) | part text |
| P06-S006 | added line not located; shift not stated | adds base L3622 inside the call L3575-L3623; hunks 33+1+7 = 41; `_shutdown` L1599-L1837 at both; `StructureExitConfig`, helpers L393-L438, `_shutdown(...)` call identical | precision; verified by diff | git show 7d4970a / 970aabf |
| P06-S007 | dashboard overlay "not opened or traced"; `.gitignore` L8 | merge located: `ops_dashboard/backend/app.py` `load_gui_config` L153-L168 (deep-merge L162-L167); `.gitignore` L9 (comment L8) | the brief asks where any overlay is merged; L8 is the comment, L9 the entry | git show 970aabf:ops_dashboard/backend/app.py, .gitignore |
| P06-S010 | "the detector's `_attr` is the same" | adds `sr_detector/detector.py` L320 to L321 | location | git show detector.py |
| P06-S017 | Parts "P01-S055; P02-S133" | "P01-S052, P01-S055; P02-S133" | P01-S052 is where the /100 is recorded | P01 |
| P06-S018 | Parts "P01-S069" | "P01-S069, P01-S072" | P01-S072 records the merge rule | P01 |
| P06-S019 | Parts "P01-S069, P01-AP09" | adds P01-S083 | P01-S083 records `_level_in_band` | P01 |
| P06-S045 | `_strong_close` L133 to L137 | L130 to L137 | the function starts at L130 | retest_confirm.py |
| P06-S057 | export "reads two, sets four in a copy" | reads one directly (`lookback_days` L165), sets four (L152-L155), passes the copy to `build_sr_detector` (L159-L163) | only `sr_cfg.lookback_days` is read directly (grep of `sr_cfg`) | sr_level_export.py |
| P06-S061 | "the two that reach a decision of the V1 flags are weak_breakout_frac and retest_sl_buffer_pct" | lists weak_breakout_frac (WEAK_BREAKOUT), breakout_avg_window (avg-volume window, detector L242 -> NO_VOLUME_CONFIRMATION flags L174), retest_sl_buffer_pct (proposed stop), max_zones_logged, max_queue, and the six zone/scoring knobs | incomplete: breakout_avg_window also reaches a flag decision | detector.py L97, L242, L253-L254; flags.py L164-L185 |
| P06-S062 | — | adds the detector's `DETECTOR_VERSION` "snr-v1" (detector.py L51, L64), not passed by build_sr_detector | completeness beside the diverter's version | detector.py |
| P06-S068 | A02 AUDIT L254 to L264 | L254 to L266 | L-04 ends at L266 (Rama line) | A02 AUDIT |
| P06-S069 | INTERPRETATION "pydantic v2 lax mode ... stored as floats" (no external source) | current external context: Pydantic "Conversion Table" (int accepted for float in strict and lax; stored type not stated -> not established); INTERPRETATION that no A08 result depends on it, with each receiver's cast line | external-behaviour claim needed an authoritative source; the stored type is not stated there | pydantic.dev conversion table, read 26-Nov-2026; fetch.py L48, zone_cache.py L31, zone_warmer.py L51, retest_monitor.py L64 |
| P06-S074 | processor row "(L3574 to L3612; always)" | "(L3574 to L3623, the call L3575 to L3623; always)" | the call closes at L3623 (L3622 is the 7d4970a-added line) | main.py L3575-L3623 |
| P06-S080 | "between the V2 infrastructure block and the A18 and V2 retest blocks" | "after the V1, regime and V2 infrastructure blocks and before the allocator, V3 chain, PB-01 and V2 retest blocks" | the regime block (A18) precedes the processor | main.py L3514, L3575, L3625 |
