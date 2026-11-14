# A05 STUDY fieldwork progress (working note; not a project record)

Started: 14-Nov-2026 12:59 IST, after ChatGPT verified the opening commit ea8e89d (PUSH VERIFIED).
Method: read-only helpers, at most two at a time (decision F); each part drafted by one helper, then checked and
corrected statement by statement by a separate helper; backups to wip/a05-fieldwork after each section
(Rama's standing go-ahead for backup pushes, 14-Nov-2026).

| Part | Subject | Draft | Check |
|---|---|---|---|
| P01 | Live feed and tick intake (data/live_feed.py; main.py feed wiring) | done 13:27 IST (146 statements) | done 13:56 IST (151 statements; 40 corrected, 5 added) |
| P02 | Pinned kiteconnect 5.1.0 library (ticker; client methods A05 uses) | done 13:24 IST (98 statements) | done 13:50 IST (100 statements; 38 corrected, 2 added) |
| P03 | Candle store and live candles (data/candle_store.py; dispatcher; consumers) | done 14:25 IST (125 statements) | done 14:58 IST (128 statements; 34 corrected, 3 added) |
| P04 | core/candle_math.py functions, contracts, callers | done 14:28 IST (101 statements) | done 15:00 IST (103 statements; 37 corrected, 2 added) |
| P05 | Instrument cache (core/instrument_cache.py; preload; consumers) | done 15:35 IST (117 statements) | running |
| P06 | Historical candle access (main.py closure; limiter bucket; A08 boundary) | done 15:26 IST (82 statements) | running |
| P07 | Instrument refresh and alias tool (refresh_instruments.py; find_symbol_aliases.py) | - | - |
| P08 | Daily candles and F&O ban scripts (fetch_daily_candles.py; fetch_fno_ban.py) | - | - |
| P09 | Configuration keys A05 reads (A02 crosswalk) | - | - |
| P10 | The 33 inherited handoffs and the 5 open issues naming A05 | - | - |
| P11 | The five existing technical records checked against the code | - | - |
| P12 | Producers, readers and writers of every A05 artefact; duplication | - | - |

Order: pairs (P01,P02) (checks P01,P02) (P03,P04) (checks) (P05,P06) (checks) (P07,P08) (checks) (P09,P10) (checks)
(P11,P12) (checks); then the STUDY and evidence files are assembled and checked independently.
Resume rule: a part whose file exists continues from the first section not marked done in status/<part>.status.

## Assembly notes (to settle when the STUDY is assembled)
- P04-S102 says scripts/sr_level_export.py reaches session_vwap; P06-S061 (and A01 C38b) show the script fails before any
  fetch (L139 TypeError; A01 recorded L141). Verify at the baseline and reconcile in P04's evidence (assembly correction).
- P04 check log: a docstring/filter mismatch in core/daily_stats.py L28-L29 vs L58 is outside A05's scope: route to A15
  as a boundary note (not a finding).
- P01 Q4 and P04 Q2 for Rama may duplicate A02 records (IC-40/K-30; K-26): drop or cross-reference at assembly.
- Verified by Claude (15:50 IST): scripts/sr_level_export.py L139 `load_all(str(ROOT / "config"))` -> core/config_loader.py
  L2457 load_all, L2481 `path = config_dir / filename` -> TypeError (str / str) before L141; L143 builds the handle with
  kite_client=None (None). P04-S102 to be qualified at assembly: the route exists in code but the script stops at L139.
