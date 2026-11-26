# Assembly working notes (H15; scratch, not evidence)

## Part facts
- P01: 140 statements (S001-S140), 17 AP (AP01-AP17), 10 U (U01-U10), 4 R (R1-R4), 8 X. Checker H4 (Opus 5.5 Max). Writer H2 (Opus 5.5 High).
- P07: 141 statements (S001-S141), 6 AP (AP-01..AP-06 in sec 8), U = statements S109, S110, S111, S141, S112, S113 (sec 9); R none (S114). Writer H1 High; checker H3 Max.

## Section 13 pointers (item -> A08 side statements)
- P01 (X01): CM-05 -> P01-S021,S045,S046,S094,S095,S126; CM-10 -> P01-S017,S018,S097,S098; HA-04 -> P01-S048,S096; HA-08 -> P01-S014,S018,S099; HA-10 -> P01-S014,S138,U10; HA-15 -> P01-S015,S016,S019,S021; HA-09 -> P01-S013; B-41 -> P01-S004,S133,U09. HA-03 (record) P01 secondary: Candle.ts docstring P01-S014,S016,S058.
- P07 lists: 48 items P07-S018..S065; 16 OIR P07-S070..S085; 16 Owner-field records P07-S125..S140; notes N1-N6 P07-S088..S093; 5.3 rows P07-S095 (22 rows incl. H-44,U-59,U-60); P07-S096 other rows.

## Section 10 (threads/clocks/failure) pointers
- P01: no clock/IO/log (S010); exceptions uncaught (S097); recency clock None -> full (S091); tz stripping (S090); data quality S094-S101.

## Section 12 (intent sources) pointers
- P01: S120 (locked decisions vs code), S121, S122 (docstrings differ), S123 (config comments), S124-S127, S140 (tests), S128-S130, S138, S139 (legacy docs), S131-S132 (history).

## Section 14 (boundaries) pointers
- P01 X08: A01 S118, S137; A07 gate_htf S135; A15 daily_trade_review S136; A06 as_of S137, Candidate S032/S115; A02 keys S055,S065,S069,S123,S129; A05 candle_math S020,S112; A11 S116; A15 daily_stats S113; A18 S108-S111,S114,S135,S137, AP05, AP14; A19 S124-S127,S140.

## P02 (160 statements S001-S160; 17 AP; 11 U; 5 R (R1-R5); 8 X). Writer H5 Max; checker H7 Max.
- Sec 13 primary items: C38a S101; K-23 S102; K-24 S103; RL-05 S104; CM-05 S105; CM-15 S106; HA-01 S107; HA-06 S108; HA-09 S109; IN-02 S110; WD-10 S111; WD-16 S112; PQ-11 S113.
- OIR primary: A05-01 S114; A05-02 S115; A05-25 S116; A05-27 S117; A05-28 S118; A05-35 S119; A05-37 S120; A05-38 S121.
- Owner-field records primary: RL-11 S122; CM-07 S123; CM-11 S124; HA-05 S125; HA-10 S126; IN-09 S127; SX-07 S128.
- Notes: N2 S129 (cache key/age + unsorted rows); N3 S130.
- Secondary: C13 S131; B-11 S132; K-21 S133; K-22 S134; CM-10 S135; HA-04 S136; PQ-09 S137; A05-17 S138; A05-29 S139; HA-03 S140.
- Sec 10: threads S091 table; locks S092; clocks S093; failure table S094; shutdown S088/S089; enqueue S079/S080.
- Sec 12: S142-S149 docstrings/comments vs code; S150-S153 tests; S154, S158 docs (PATHS.md L386, L392, L409; SYSTEM_MAP; expected_managers.yaml); S155-S157 history.
- Sec 14 (X07): A01 closure/constructions/warmer start/_shutdown; A02 keys K-23, K-24; A04 limiter RL-05, RL-11; A05 session_vwap, instrument cache; A06 _warm_zones WD-10, WD-16, PQ-11; A07 SX-07; A11 structure exit ZoneCache.get never enqueues S159/AP17; A12 eod clears retest monitor not zone cache; A15 telemetry S099, registry S158; A16/A17 process lifetime, clock sync; A18 regime/V3/PB-01 fetchers; A19 tests.
- X08: inventory 2.2 PB-01 fetcher lines L3728-L3732 (now corrected in inventory Rev 1).

## P03 (217 statements S001-S217; 16 AP; 10 U; 5 R; 8 X). Writer H6 Max; checker H8 Max. Post-check correction by Claude: S157.
- Sec 13 primary: D-05 S164; Q-17 S165; Q-29 S166; U-25 S167; HA-04 S168; EV-23 S169; XS-12 S170; A03-10 S171; A05-29 S172; D-09 S173; U-05 S174; N1 S175.
- Secondary: C13 S176; K-21 S177; K-22 S178; K-23 S179; H-11 S180; CM-15 S181; HA-06 S182; HA-07 S183; HA-08 S184; A05-32 S185; CM-07 S186; CM-11 S187; HA-05 S188; SX-07 S189; RP-12 S190; N5 S191.
- 5.3 rows H-44, U-59, U-60: S192 (facts S095, S118, S120, S128/S129/S134).
- Sec 10: stop leaves S033/S216; worker before placement S036; observe S037-S040; exceptions S055; as-of S057; clock NULL created_at S092; shared resources S105-S107,S217; backfill date S116/S125; failure S126; guard S128-S131.
- Sec 12: S193-S197 docstrings; S198-S202 tests; S203-S207 docs; S208-S214 history.
- Sec 14 (X07): A01 wiring/clock/holiday S035,S155,S157; A02 config + registry S154,S098, AP13; A03 store/schema/locking S087,S089,S106,S152,S153; A04 limiter/client S105; A05 instrument cache S217; A06 seam, EV-23, TIMEOUT S101,S102,S143-S147,S169,S215; A10 trade rows/recovery S121,S215, AP11; A12 prune S097,S160; A15 report/telemetry/logging S096,S098,S156,S159,S217; A16 guard/registry/cron S128,S133,S134,S157,S158, AP07, AP08; A18 activation D-41 P2, PB-01 retest S077; A19 tests S139,S140,S162,S198-S202.
- X08 (d): A03 H-11 cites retest_monitor L415; baseline L414 (recorded only).
