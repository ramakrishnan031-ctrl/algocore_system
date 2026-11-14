# A05 STUDY fieldwork progress (working note; not a project record)

Started: 14-Nov-2026 12:59 IST, after ChatGPT verified the opening commit ea8e89d (PUSH VERIFIED).
Method: read-only helpers, at most two at a time (decision F); each part drafted by one helper, then checked and
corrected statement by statement by a separate helper; backups to wip/a05-fieldwork after each section
(Rama's standing go-ahead for backup pushes, 14-Nov-2026).

| Part | Subject | Draft | Check |
|---|---|---|---|
| P01 | Live feed and tick intake (data/live_feed.py; main.py feed wiring) | done 13:27 IST (146 statements) | done 13:56 IST (151 statements; 40 corrected, 5 added) |
| P02 | Pinned kiteconnect 5.1.0 library (ticker; client methods A05 uses) | done 13:24 IST (98 statements) | done 13:50 IST (100 statements; 38 corrected, 2 added) |
| P03 | Candle store and live candles (data/candle_store.py; dispatcher; consumers) | done 14:25 IST (125 statements) | running |
| P04 | core/candle_math.py functions, contracts, callers | done 14:28 IST (101 statements) | running |
| P05 | Instrument cache (core/instrument_cache.py; preload; consumers) | - | - |
| P06 | Historical candle access (main.py closure; limiter bucket; A08 boundary) | - | - |
| P07 | Instrument refresh and alias tool (refresh_instruments.py; find_symbol_aliases.py) | - | - |
| P08 | Daily candles and F&O ban scripts (fetch_daily_candles.py; fetch_fno_ban.py) | - | - |
| P09 | Configuration keys A05 reads (A02 crosswalk) | - | - |
| P10 | The 33 inherited handoffs and the 5 open issues naming A05 | - | - |
| P11 | The five existing technical records checked against the code | - | - |
| P12 | Producers, readers and writers of every A05 artefact; duplication | - | - |

Order: pairs (P01,P02) (checks P01,P02) (P03,P04) (checks) (P05,P06) (checks) (P07,P08) (checks) (P09,P10) (checks)
(P11,P12) (checks); then the STUDY and evidence files are assembled and checked independently.
Resume rule: a part whose file exists continues from the first section not marked done in status/<part>.status.
