# P01 checker working notes (H4) — scratch, not a deliverable

## Verified against the baseline (git show 970aabf, nl -ba), no change needed (running list)
- S007 blobs/sizes/lines/commits/7d4970a identity; S008 line numbers; S010 fixed-string search (`time.` only models.py L25);
  no try/except/raise in the four files; S011 docstring quotes; S014 to S016 code; S019 fetch.py L121 to L136 and the
  WARNING text; forward_shadow_record L211 to L215; two non-test from_kite callers only; S020 candle_math L427; S022
  bar_index only L56, L49, L53 (whole tree); S023 to S028 code; S025 (.width hits are spreadsheet columns); S030 to
  S037 code and call sites; S038 to S044 pivots; S050 to S052, S057, S059 to S061, S063, S067, S068, S070, S071, S074 to
  S076, S080, S083, S084, S088 code; S069 table values (zone_builder L54 to L65, loader L1172 to L1194, YAML L515 to
  L527); S093 detector L253 to L254, loader L1197; flags L122/L133/L135; retest_monitor L384 to L390, L400/L404/L410,
  L295 to L296; SEM L270/L277; watchlist_capture L199 to L218, L232 to L236; S102 to S118 call sites; S124 to S127
  test lines; S128 to S132 documents and history.

## Corrections planned
- S009: add `annotations` (__future__) for the three algorithm files; `field` unused is a direct read (FACT).
- S010: "only time input" -> the only clock / reference-time input (candle and pivot ts are data labels).
- S012: "stdlib only" literal vs the intra-package import of sr_detector.models: nuance.
- S029: zone_builder dict is L215 to L223 in build_swings_payload (L207 to L224), not L213 to L221.
- S036: _validate_timeframes is L1243 to L1255 (not L1250).
- S047: basis for "every caller passes an int": build_zone_knobs int() L43; pivot_n_by_tf typed dict[str, int] (loader
  L1169), not cast in L44.
- S054: "the four files do not add one themselves" is not exact: _level_in_band and contains widen for their test; the
  stored band is never widened.
- S055: -inf LOW pivot -> own zone at the bottom (mirror of +inf at the top).
- S055/S069: validators run L1225 to L1255 (class L1153 to L1255).
- S062: clamp also catches floating-point rounding when mid is at/near hi ("only" too strong) - check numerically.
- S064/S097: NaN -> ValueError; +inf high / -inf low -> ValueError (NaN via inf/inf); +inf low / -inf high (invalid
  bars) -> OverflowError, or [] when hi <= lo. "raises ValueError for any NaN or infinite" too broad.
- S064: NaN bucket as peak (bucket 0) -> no nodes at all.
- S072/S073: zero mean centre -> tolerance 0 (equal centres still merge), not negative.
- S078: also needs touch_cap >= 1.
- S086/S097: "infinite centre" -> +inf (a -inf centre is non-positive -> False).
- S090: neutral wording instead of "correct"/"right".
- S092: zones_by_tf order changes only member order inside a group; no ScoredZone field changes.
- S094 (a): same zones; same scores only for the same ConfluenceContext (prior_day_levels uses daily[-2]).
- S098: zero vs negative prices (zero: tolerance 0, equal prices still join/merge).
- S100: single candle gives one node only with positive volume.
- S108 to S117 table rows: no labels -> add a Label column.
- S119: export as_of naive 15:30 (sr_level_export L158, L161).
- S125: test zones at L98 to L115 contain 100.0 -> round vote by code reading; MEDIUM test comment omits it (5.5).
- AP05: "wrong neighbours" -> neutral; add gate_htf consumer. AP08 wording. AP15 "so a MATCH candidate" -> remove
  (classification hint). R1 "In the legacy system ... was marked" -> "the legacy code rated".
- S004: add page titles; check each external claim against the pages.

## Additions planned (new IDs from P01-S133)
- gate_htf (screening/hard_gate.py L297 to L336, A07) reads highs[-1]/[-2] of V3 pivot lists in output order;
  docstring L311 to L313 "chronological price lists (e.g. from find_swing_pivots)"; V3 runner L203 to L205, L212 to
  L214; pb01_runner L150 to L154.
- sr_detector/__init__.py L20, L22 re-exports Candidate; signal_processor L640 imports it from the package.
- reports/daily_trade_review.py _fmt_zone L234 to L249 (A15) reads stored zone JSON keys.
- export script naive as_of (L158, L161) -> recency tz branch.
- HISTORICAL: daily_report_redesign_phase0_data_audit_30jun2026.md L100, L165 (commit 01e07b7f..., 2026-07-01):
  "29 rows, all outcome-backfilled"; relevant to U05/U06.
- HISTORICAL: ma2_ms3_md1_25jul2026.md L262 to L267 and SYSTEM_MAP L85: historical volume is per-interval (delta);
  relevant to S014.
