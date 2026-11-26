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

## P04 (183 statements S001-S183; 21 AP; 11 U; 5 R; 8 X). Writer H9 Max; checker H11 High. Post-check correction by Claude: S126.
- Sec 13 primary: K-22 S131; H-11 S132; P-02 S133; P-11 S134; Q-11 S135; WA-06 S136; WA-07 S137; EV-11 S138; SL-06 S139; SL-30 S140; EG-01 S141.
- OIR primary: A05-17 S142; A05-18 S143. Records primary: Q-09 S144; HA-03 S145; EV-01 S146; ET-07 S147; RP-12 S148. N5 S149; N6 + wording S150.
- Secondary: C13 S151; C37 S152; K-21 S153; Q-17 S154; CM-05 S155; HA-04 S156; A05-29 S157; N1 S158. 5.3 rows: H-25,H-44,H-47,Q-46 S159; RP-13,RP-21 S160.
- Sec 10: threads S106; locks S107; interleavings S108; clocks S109/S110; directions S111; failure table S112; S113 summary; TypeError S070.
- Sec 12: S161-S170 docstrings/comments; S171-S175 tests; S176-S178 docs; S179-S182 history.
- Sec 14 (X07): A01 wiring/boot/shutdown S016,S035,S062,S080,S089,S091,S092,S114,S115; A02 keys/loader/registry S019,S034,S097,S125,S128; A03 store/table/CHECKs S053-S059,S122, AP17, AP21; A05 HA-03/HA-04/CM-05/A05-17/18/29; A06 divert call site/resumption/WA-06/WA-07/EV-01/EV-11/ET-07/upstream claim S036, sec 8, S136-S138,S146,S147, AP03; A07 SL-06,SL-30,EG-01,RP-12,RP-13,RP-21 S105,S139-S141,S148,S160; A09 S099,S102; A10 MARKET S100,S121, AP18; A11 _strong_close S017,S120; A12 eod clear/prune/recovery S059,S086-S088,S119,S123; A13 S102; A15 report/registry/evidence S060,S125,S126,S175; A18 PB-01 + wording S017,S127,S150, AP09, AP10; A19 tests S129,S171-S175, AP20.
- X08: (b) inventory sec 7 omits test_sr_v2_market_path.py (now in Rev 1); (c) records notes AP21; (d) AP01 bears on SL-06,SL-30,ET-07,EV-11,Q-11,C13.

## P05 (122 statements S001-S122; 17 AP; 7 U; 3 R; 8 X). Writer H10 Max; checker H12 High.
- Sec 13 primary: C38b S093; K-02 S094; CL-11 S095; CL-15 S096; RL-06 S097; HA-07 S098; XC-03 S099. OIR: A04-05 S100; A04-28 S101; A05-32 S102; A05-54 S103. Records: CL-12 S104; AU-05 S105.
- Secondary: D-05 S106; CM-15 S107; HA-09 S108; A05-02 S109; CM-07, HA-05, IN-09, SX-07 S110; N2 S111.
- 8.5 records found: A01 C40 S112; A02 K-32 S113 (Claude's assignment decision: listed in 13.6 with P05 facts).
- Sec 12: S114-S116 texts; S117-S119 tests; S120 docs; S121 history.
- Sec 14 (X07): A01 helpers/import effects C38b, C40; A02 load_all, keys K-02, K-32, L-45, L-47; A04 client/limiter CL-11, CL-12, CL-15, AU-05, RL-06, A04-05, A04-28; A05 instrument cache HA-07, HA-09, XC-03, CM-15, IN-09, A05-02, A05-32, A05-54; A15 registry; A16 no schedule; A19 test.

## P06 (189 statements S001-S189; 10 AP; 6 U; 5 R (R1 withdrawn); 8 X). Writer H13 High; checker H14 Max.
- Sec 13 primary: C13 S137; C37 S138; B-11 S139; K-21 S140; K-25 S141 (no A08 side); K-26 S142 (no A08 side); U-24 S143 (no A08 side); PQ-09 S144.
- Secondary table S146-S167: C38a S146; K-02 S147; K-22 S148; K-23 S149; K-24 S150; RL-05 S151; HA-06 S152; HA-09 S153; XC-03 S154; WA-06 S155; WA-07 S156; WD-10 S157; WD-16 S158; EV-23 S159; SL-06 S160; SL-30 S161; A05-01 + CM-07 S162; RL-11 S163; CM-11 S164; HA-05 S165; HA-10 S166; ET-07 S167.
- 9.3: H-44 S169 (P03-S095, P04-S045); U-59 S170 (P03-S118, S120, S192, S196); U-60 S171 (P03-S129, S133, S134, S138, S192); C40 S172 (P05-S049, S050, S112); K-32 S173 (P05-S021, S113).
- 9.4: S175 table 34 records (pointers in table); S176 9 records: A01 S-33 (P06-S072,S056); A02 L-12 (P06-S053,S009,AP07; P03-S025); A02 V-22 (P06-S072,S114); A02 L-33 (P06-S009,S011,S040,S052,S056,S065); A03 R-34 (P06-S056,S088,S074; P04-S120); A05 CA-16 (P06-U01,S056); A06 EV-14 (P06-U01,S011,S040); A06 XA-05 (P06-U01,S040,S051); A07 XS-08 (P06-S011,S057). S177/S178 not A08-touching lists. S189 PQ-06 (P02-S080,S098; P06-S094).
- Sec 11 consumer table S093-S118, S187 (v3_chain/truncate.py), S119 inputs, S120 sweep result.
- Sec 12: S179-S186.
- Inventory corrections S121-S136, S187, S188 (applied in inventory Rev 1).
