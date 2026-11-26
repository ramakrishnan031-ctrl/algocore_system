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
