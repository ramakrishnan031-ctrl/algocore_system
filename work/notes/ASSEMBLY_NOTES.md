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
