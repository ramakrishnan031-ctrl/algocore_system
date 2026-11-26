"""A08 inventory Revision 1: apply the corrections found by the STUDY parts (P06 section 8, P06-S122 to S135 and
S187, S188, as checked). Idempotent, anchored to exact text; fails on any missing anchor."""
import sys, pathlib
P = pathlib.Path("/home/claude/algocore_system/doc/02_PHASE1_LEGACY_STUDY_AND_AUDIT/TOPIC_WISE_DOCUMENTATION/"
                 "A08_TECHNICAL_ANALYSIS_SR_AND_RETEST_CONTEXT/evidence/A08_SOURCE_FILE_INVENTORY_2026-11-26.md")
t = P.read_text(encoding="utf-8")

def sub(old, new, label):
    global t
    if new in t:
        return
    n = t.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL ({label}): {n}")
    t = t.replace(old, new)

sub("**Revision history:** First version, 2026-11-26.",
    "**Revision history:** First version, 2026-11-26. Revision 1, 2026-11-26: line references and omissions corrected "
    "from the checked A08 STUDY parts (part P06, section 8, statements P06-S122 to P06-S135, P06-S187 and P06-S188; "
    "parts P01 to P05 as cited there); every corrected cell names its source statement. No path, size, hash or count of "
    "section 1's table changed (P06-S136).", "history")

sub("`sr_level_export.py` `flatten_analysis` (L62), `export_levels` (L104), `_make_real_analyze_fn` (L127), `main` (L178).",
    "`sr_level_export.py` `flatten_analysis` (L62), `export_levels` (L104), `_make_real_analyze_fn` (L127), `main` (L178). "
    "Also at column 0 (Revision 1; P06-S188): `zone_builder.py` `_attr` (L24); `detector.py` `_attr` (L320), `_iso` (L324), "
    "`_json` (L328); `scripts/sr_corp_action_spotcheck.py` `_build_kite` (L33), `_token_for` (L45); "
    "`scripts/sr_detector_backfill.py` `_is_terminal` (L30), `_win_loss` (L34); `scripts/sr_level_export.py` `_row` (L46), "
    "`rows_to_csv` (L94).", "toplevel")

sub("| L186 to L188; L229 to L231 | constructor parameters and fields:",
    "| L186 to L188; L229 to L232 | constructor parameters and fields:", "2.1 fields")
sub("calls `SRDetector.observe` (L655); called at L1550, after the order reached placement |",
    "calls `SRDetector.observe` (L655); called at L1550 (`_admit_and_place`), L2296 (`continue_from_gate`) and L2588 "
    "(`continue_from_retest`), each after the `PROCESSED` write (P06-S122; P01-S032; P03-S101) |", "2.1 observe")
sub("| L1042 to L1043 | `RetestDiverter.enabled` and `maybe_divert` on the FCFS path |",
    "| L1042 to L1049; L1056 | `RetestDiverter.enabled` and `maybe_divert` on the FCFS path; the parked return at L1056 "
    "(P06-S126; P04-S117) |", "2.1 divert")

sub("| L3717 to L3718 | an `OhlcFetcher` and the zone knobs reused by the PB-01 watchlist (A18) |",
    "| L3712 to L3763 | the PB-01 block (A18): imports L3717 to L3718, the zone knobs L3723 to L3724, an `OhlcFetcher` "
    "L3728 to L3732, reused by the PB-01 watchlist (P06-S123; P02-X08) |", "2.2 pb01")
sub("| L3804 to L3830 | `StructureExitManager` (A11) with the zone cache, when `_struct_exit_on` |",
    "| L3804 to L3837 | `StructureExitManager` (A11) with the zone cache, when `_struct_exit_on`: the warmer start L3816, "
    "construction L3817 to L3831, `start()` L3832, `except` L3835 to L3837 (P06-S127) |", "2.2 sem")
sub("| L4267 to L4268 | `zone_warmer` and `retest_monitor` passed to `_shutdown` |",
    "| L4266 to L4269 | `sr_detector` (L4266), `zone_warmer` and `retest_monitor` (L4267 to L4268) and "
    "`structure_exit_manager` (L4269) passed to `_shutdown` (P06-S128) |\n"
    "| L393 to L438 | the closure's helpers `_build_market_data_kite` (L393 to L418) and `_make_sr_fetch_fn` (L421 to L438), "
    "used by the fetch of every A08 object (P06-S129) |\n"
    "| L3428 to L3443 | the structure-exit guard before the S&R blocks (P06-S129) |\n"
    "| L3524, L3563, L3683, L3733, L3778 | the five `register_constructed(\"ohlc_fetchers\")` calls (P06-S129) |", "2.2 shutdown+")

sub("| `orders/order_placer.py`, `orders/order_protocol_limit.py`, `orders/full_entry_engine.py` (A10) | L888, L1355; L183, L207; L85 | `entry_order_type` \"MARKET\" for the retest-confirm entry |",
    "| `orders/order_placer.py`, `orders/order_protocol_limit.py`, `orders/full_entry_engine.py`, `orders/order_protocol_co.py` (A10) | L888, L1345 to L1356; L183, L206 to L219; L85, L93 to L119; L103 | `entry_order_type` \"MARKET\" for the retest-confirm entry (`order_protocol_co.py` takes and ignores it) (P06-S130; P04-S121) |", "2.3 a10")
sub("| `regime/engine.py` (A18) | L50 | `find_swing_pivots` |",
    "| `regime/engine.py` (A18) | L50; L193 to L194; L108, L117 to L118, L321 to L323 | `find_swing_pivots` (import and call); the injected fetcher through `_fetch` (P06-S131) |", "2.3 regime")
sub("| `v3_chain/runner.py`, `v3_chain/pb01_runner.py`, `v3_chain/watchlist_capture.py` (A18) | L32 to L34; L37 to L39; L205 | `CONF_ANCHOR_ONLY`, `find_swing_pivots`, `scored_zones_from_candles`, `split_zones` |",
    "| `v3_chain/runner.py`, `v3_chain/pb01_runner.py`, `v3_chain/watchlist_capture.py` (A18) | L32 to L34; L37 to L39; L205 | `CONF_ANCHOR_ONLY`, `find_swing_pivots`, `scored_zones_from_candles`, `split_zones`; the runners and the capture also call the fetcher (`fetch_timeframes`) (P06-S131) |\n"
    "| `v3_chain/pb01_entry.py` (A18) | L279 to L280, L289 to L291, L308 | the shared PB-01 `OhlcFetcher`, without importing A08 (P06-S131) |\n"
    "| `v3_chain/truncate.py` (A18) | L54 to L68, L71 onwards (L92) | reads the `ts` of the fetched A08 `Candle` objects; called by the V3 runner, the PB-01 runner and the entry stage (P06-S187) |", "2.3 v3")
sub("| `core/state_store.py` (A03) | L1992 to L2020; L3017 onwards | the `sr_detector_results` writes, the backfill reads and updates; the `retest_state` writes (`insert_retest_state` L3026, `update_retest_state` L3041) |",
    "| `core/state_store.py` (A03) | L1979 to L2024; L3026 to L3072; L1408 to L1426 | the `sr_detector_results` methods (writes, the backfill reads and updates); the `retest_state` methods (`insert_retest_state` L3026, `update_retest_state` L3041); `update_signal_status` (P06-S133) |", "2.3 store")
sub("| `core/schema.sql`, `core/migrations.py` (A03) | L1247 to L1294; L1303 to L1336; L82, L131 | the `sr_detector_results` table (schema v37) and the `retest_state` table (v38) |",
    "| `core/schema.sql`, `core/migrations.py` (A03) | L1247 to L1300; L1303 to L1340; L81 to L83, L131 to L132 | the `sr_detector_results` table and indexes (schema v37) and the `retest_state` table and indexes (v38; rebuild entry L132) (P06-S133) |\n"
    "| other readers of A08 code or of A08's stored output (owners as the index states) | — | `screening/hard_gate.py` `gate_htf` (A07); `reports/daily_trade_review.py`, `reports/signal_status.py`, `core/effect_telemetry.py` with `config/expected_managers.yaml`, `core/evidence_contract.py` and its manifest (A15); `scripts/eod_cleanup.py` (A12); `ops_dashboard/backend/readers/db_reader.py` and the `ops_dashboard` label maps; `core/config_auditor.py` (A02); `core/time_authority.py` as the clock (P06-S132; the STUDY's consumer table) |", "2.3 schema+")
sub("| `orders/structure_exit_manager.py` (A11) | L70; L102 to L130; L203 to L208 | imports `retest_confirm._strong_close`; reads the `ZoneCache` for the structure stop |",
    "| `orders/structure_exit_manager.py` (A11) | L70; L102 to L130; L203 to L208; L256 to L277, L281 to L296 (`_strong_close` at L290, L293) | imports `retest_confirm._strong_close`; reads the `ZoneCache` and the zones' fields for the structure stop (P06-S135) |", "2.3 sem")

sub("`structure_exit_enabled: false` (L634) sits in the structure-exit block, read by `main.py` L3427.",
    "`structure_exit_enabled: false` (L634) sits in the structure-exit block, read by `main.py` L3427, by "
    "`core/config_auditor.py` L224 (rule A4, run at `main.py` L3437 to L3439) and by `orders/structure_exit_manager.py` "
    "L127 to L129 (P06-S134).", "4 readers")

sub("A test states an expectation under its own conditions; it is never evidence of production behaviour, and none was run.",
    "A test states an expectation under its own conditions; it is never evidence of production behaviour, and none was run. "
    "Revision 1 (P06-S124): the search does not match `tests/unit/test_config_auditor.py`, which tests rule A4 on "
    "`structure_exit_enabled` (L87 to L132), or `tests/unit/test_sr_v2_market_path.py`, the SNR-V2 MARKET-route test, "
    "which names no A08 code (P04-X08); no file under `tests/` outside the 26 imports A08 code.", "7")

P.write_text(t, encoding="utf-8")
print("OK")
