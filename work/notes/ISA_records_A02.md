#### A02 K-02 (L1834; headings found 1) ##### K-02 — Trading-hour values held as literals and in the dashboard's own copy
  L1838 - **Intended behaviour and source:** LOCKED-YAML P1 L222: "All times sourced from core/market_windows.py — single source of truth, no hardcoded times anywhere else. Configurable via config/system_config.yaml"; FRULES 1.4 ("No hardcoded ... settings"); YAML header L5 (2026-04-17); YAML L104 (2026-04-21) `market_close` "cutoff for EOD-window checks"; CFG-GUIDE L199 to L204. Copies documented as deliberate at their sites: `ops_dashboard/backend/config/gui_config.yaml` L61 "Market clock (DUPLICATED from config/system_config.yaml trading_hours)" (2026-07-03); `screening/step_executor.py` L30 to L35 (constant for old tests; production injects the configured open); `scripts/liveness_probe.py` L85 to L100 (25-Jul-2026: the 16:00 bound is "CONSERVATIVE rather than exact ... Do NOT resync this to 17:35"). No later source replaces P1 as a whole.
  L1842 - **Result and classification:** ISSUE; FACT (copies and literals against P1 and FRULES 1.4; three of them deliberate by their own comments, so sources conflict). Not a KNOWN DEFECT: condition (a) fails (no code consults the keys at these sites).
  L1844 - **Owner:** A02 (the keys); A01 (`main.py` L994); A06 (gap window); A15 (dashboard, control tower, watchman, execution analytics, liveness probe); A08 (`sr_level_export.py`); A19 (t2 script).
  L1846 - **Rama:** not needed to classify.
#### A02 K-21 (L2100; headings found 1) ##### K-21 — The `_pct` suffix means a fraction in some keys and a percentage in others
  L2104 - **Intended behaviour and source:** YAML L366 to L371 and loader L654 to L660 (10-Sep-2026): `limit_aggressive_pct` "is a FRACTION ... These are NOT — hence '_percent', not '_pct'" (a stated convention: `_pct` a fraction, `_percent` a percentage); against: `broker_costs.yaml` L9 to L10 (2026-04-17) "All _pct fields are PERCENTAGES" (file-local) and CFG-GUIDE L666 to L667; each key's own comment states its unit (for example YAML L514 "within this %", L585 "this×LEVEL").
  L2108 - **Result and classification:** ISSUE; FACT (names against a stated convention); Weakness. Not a KNOWN DEFECT.
  L2110 - **Owner:** A02 (key names); the consumers' owners for unit handling (A08, A11, A10, A12, A18, A04).
  L2112 - **Rama:** not needed to classify; needed for treatment (which convention is meant file-wide).
#### A02 K-22 (L2114; headings found 1) ##### K-22 — The SL-buffer keys: a misnamed path and an untied duplicate
  L2118 - **Intended behaviour and source:** YAML L540 (2026-06-27) "structure SL beyond the broken level by this %"; loader L1211 ("structure SL = band_low − this%"); loader L1182 (2026-06-27, no comment); YAML L635 (2026-06-27) "SL-to-structure buffer ... — match Phase A".
  L2122 - **Result and classification:** ISSUE; FACT. Not a KNOWN DEFECT.
  L2124 - **Owner:** A02; A08 (detector, flags, retest); A06 (signal processor); A11 (structure exit).
  L2126 - **Rama:** not needed.
#### A02 K-23 (L2128; headings found 1) ##### K-23 — `sr_detector.max_queue` does not govern the ZoneWarmer's queue
  L2132 - **Intended behaviour and source:** loader L1195 to L1196 ("worker / logging", 2026-06-27). Whether the key should govern the warmer: not established. FRULES 1.4 (no hardcoded settings).
  L2136 - **Result and classification:** ISSUE; FACT: the warmer's queue size is a hardcoded constructor value beside a configurable key of the same name (a schema field absent from the file), against FRULES 1.4 (no hardcoded settings); whether the key itself was meant to govern the warmer is not established. Not a KNOWN DEFECT (condition (a) fails).
  L2138 - **Owner:** A02; A08.
  L2140 - **Rama:** not needed.
#### A02 K-24 (L2142; headings found 1) ##### K-24 — Cross-section reuse, and a lookback key that does not set the fetch its comment names
  L2146 - **Intended behaviour and source:** YAML L624 and loader L1539 (2026-07-13): "how far back to fetch daily candles to compute LEVEL (calendar days)"; YAML L512 (2026-06-27) "intra-session (symbol, interval) re-fetch suppression" (sr_detector's own fetches); YAML L612 and L615 (2026-07-12): the V3 worker "reuses the sr_detector rate-limited closure" with its "own OhlcFetcher cache TTL (distinct from sr_detector.cache_ttl_sec)"; `main.py` L3725 to L3727 ("ONE fetcher over the shared closure: lookback covers the structural fetch; cache_ttl=0 keeps the entry stage's 5-min poll FRESH").
  L2150 - **Result and classification:** ISSUE; FACT (the key against its own comment); the regime TTL reuse has no stated intent (INTERPRETATION). Not a KNOWN DEFECT: condition (a) fails.
  L2152 - **Owner:** A02; A18 (watchlist, regime); A08 (fetcher).
  L2154 - **Rama:** not needed.
#### A02 K-25 (L2156; headings found 1) ##### K-25 — `regime.index_symbol` is stored and never read
  L2160 - **Intended behaviour and source:** YAML L549 (2026-07-12) "spot index (NOT in the instrument cache → fetched by index_token via the existing OHLC closure)"; loader docstring L1263 to L1265. The intended use of the symbol itself: not established.
  L2164 - **Result and classification:** ISSUE; FACT (minor). Not a KNOWN DEFECT.
  L2166 - **Owner:** A02; A18.
  L2168 - **Rama:** not needed.
#### A02 K-26 (L2170; headings found 1) ##### K-26 — `watchlist.entry_tf` (replaced by a literal) and `watchlist.playbook_scanner` (no reader)
  L2174 - **Intended behaviour and source:** YAML L621 "the eod scanner this watchlist owns", L628 "retest timeframe (built via candle_math.resample)" (2026-07-13); loader L1533 to L1535 ("binds the eod route → the playbook ... the scanner-name the capture worker owns") and L1544. HISTORICAL: IA-2026 L3729, L3754 to L3756 (orphans).
  L2178 - **Result and classification:** ISSUE; FACT. Not a KNOWN DEFECT: condition (a) fails.
  L2180 - **Owner:** A02; A18.
  L2182 - **Rama:** not needed.
#### A02 L-08 (L310; headings found 1) ##### L-08 — Failures that leave `load_all` outside the two documented classes
  L314 - **Intended behaviour and source:** CL2: "Any failure raises ConfigMissingError ... or ConfigSchemaError ... immediately"; `load_all` docstring L2473 to L2475 (2026-04-17).
  L318 - **Result and classification:** ISSUE. INTERPRETATION. KNOWN DEFECT considered and not given: (a) holds (the wrapping handlers); (b) holds (they cannot catch these classes); (c) holds for an unreadable file; (d) fails: the outcome is still a failed load with no partial configuration and, in `main.py`, the same exit 5, which CL2's "startup failure" covers.
  L320 - **Owner:** A02.
  L322 - **Rama:** not needed.
#### A02 L-12 (L366; headings found 1) ##### L-12 — Constraints stated in comments, decisions or instructions that the schema does not enforce
  L370 - **Intended behaviour and source:** as listed in the detail table (each with its path, lines and date).
  L374 - **Result and classification:** ISSUE. FACT.
  L376 - **Owner:** A02.
  L378 - **Rama:** not needed.
#### A02 K-32 (L2254; headings found 1) ##### K-32 — `broker_limits.yaml`: the 429 sequence and the connect timeout are never read; the read timeout reaches one client
  L2258 - **Intended behaviour and source:** file header L5 (2026-04-17) "On 429 from broker, apply backoff_sequence_sec then soft_kill (G7)", L25 and L29 ("4th step is soft_kill -- handled in code, not here"); LOCKED-YAML G7 L135 to L138 ("4-step backoff on 429: 1s/5s/30s/soft_kill") and RL4 L1068 to L1078; loader L2190 to L2192 (2026-04-19: `rate_limit_backoff` is "Distinct from backoff_sequence_sec (G7), which is the soft-kill escalation ladder for sustained rate-limit failure") and L2251; CFG-GUIDE L241 to L247; L31 to L33 and loader L2184 to L2185 (ZA12 timeouts).
  L2262 - **Result and classification:** ISSUE; FACT. Not a KNOWN DEFECT: condition (a) fails. A01 C36b records `connect_sec` at `main.py`; A02 adds the sequence key and the scope of `read_sec`.
  L2264 - **Owner:** A02; A04; A01 (`main.py` L385); script owners (A12, A05, A18, A20, A19, A15).
  L2266 - **Rama:** not needed.
