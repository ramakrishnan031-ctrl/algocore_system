# A02 evidence: the A02 source files at the study baseline

**Status:** DRAFT — evidence for the A02 STUDY, for ChatGPT's review
**Date:** 2026-11-06
**Revision history:** First version, 2026-11-06.
**Purpose and scope:** Identifies the A02 paths of the Master System Investigation Index (entry A02; Appendix A for the script) at the study baseline: size, Git object, SHA-256 and history, and the A02 changes made after the last recorded deployment (Decision Register, D-21). It supports the STUDY's inventory sections.
**Source:** trading-system-prod-snapshot, branch `main`, commit `970aabf3c78d777d9d34549e021f7c8e756c7bdb` (Source Inventory, SRC-10), read on 06-Nov-2026 from the local read-only clone with `git show`, `git ls-tree`, `git log` and `git diff`. Nothing in the clone was written or run.

## 1. The files

The A02 paths are every YAML and CSV file under `config/` except `config/cron_registry.yaml` (A16's), the four `core/config_*.py` modules, `strategies/schema.py`, `strategies/loader.py`, `.env.example` and `scripts/revert_temp_config.py` (index entry A02 and Appendix A). FACT: at the baseline `config/` holds 51 tracked files, all YAML or CSV; with `config/cron_registry.yaml` excluded, 50 are A02's, and with the eight other paths the A02 set is 58 paths. All exist at the baseline, and the clone's working tree was clean and at the baseline.

Lines and bytes are those of the file at the baseline. "Commits" counts the commits in the repository's history that touch the path, up to the baseline. For `.env.example` only the file's identity is recorded here; its key names are recorded in the STUDY and no value is reproduced anywhere.

| Path | Lines | Bytes | Mode | Git blob (SHA-1) | SHA-256 | Commits | Last change |
|---|---|---|---|---|---|---|---|
| `config/accounts.csv` | 6 | 704 | 100644 | `e2cceb6665678e1648d8c52c59e57107487bd43b` | `b012e1ac707b62ecfd3318b58b1522916dbf1fff46efb0f497d91b00e707b1a5` | 6 | 13eb727, 2026-06-12 |
| `config/accounts_multi_example.csv` | 4 | 467 | 100644 | `05e71a28cf21de8926af287941b51abe063a0492` | `778199fdca483ccaa7252a1585cfb98f7d980b31d4bacc7c4f44226558a16f77` | 1 | 38fa4e9, 2026-05-31 |
| `config/broker_costs.yaml` | 35 | 1895 | 100644 | `99320ecfd0e238a76f8f96748f81474d5e38640c` | `7cf2bc40534e8abf4386062385bab480e77b08ff3569e23b55ff1590abc6fd34` | 2 | 5dc8563, 2026-05-14 |
| `config/broker_limits.yaml` | 40 | 1361 | 100644 | `ad05dd83fb2b7d6480b6e226c57693d2fdaaa1ab` | `e660b15089435d1164ec15b0900df4289e158a0eb3be33d33d0dab1b9066c145` | 3 | 316b335, 2026-04-19 |
| `config/chartink_scanners.yaml` | 32 | 1795 | 100644 | `de82a8269c2c913e027dad5bd3a92c59222d8eaa` | `514454c2744180f9c27820cb59d5e44e6657921837ac5681d567ccb19020dcfe` | 2 | 5a71fb6, 2026-07-13 |
| `config/expected_managers.yaml` | 386 | 22155 | 100644 | `ff4d65d5f9b5a5ddfcc8cac7b812c770da555a3c` | `5c1977bdc30164a8712155a50d04ddaa09aa77058faa9805769c8753d57b0f0d` | 3 | 0197923, 2026-08-04 |
| `config/index_universe.yaml` | 28 | 1688 | 100644 | `416d1eb723c555573dc12f71a78c7bd17afde6ed` | `27c74fcf1c02adc661d4230e276c74b2470c9d09cc0bb41793717dc3130e8921` | 1 | 4e2df39, 2026-07-17 |
| `config/nse_holidays_2026.yaml` | 47 | 1390 | 100644 | `128643594c4206151d3901d8f85d6d68f67e8105` | `efebaaea6f2e413b8f34dba731098cfc3e595002edfe22c3f2f05418adaabc4e` | 1 | bcf03b5, 2026-04-17 |
| `config/preflight.yaml` | 38 | 2108 | 100644 | `b56ea0d468ae1ccd80232d577c1dcc6417dbd83e` | `d2f9951b36ffc73273fe728fa31faa97bb47cbe2efe9269e5cab69b0955d25a7` | 1 | e45f6b2, 2026-08-10 |
| `config/reference_data/index_members/fno_symbols.csv` | 207 | 1669 | 100644 | `f2d29cefeaa24bb222e3257b94d39fb90a0d685d` | `ce68c30b39bb823519b050b38136ce0e723e6058e5d88b1e0f7358beb36b895f` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty100.csv` | 101 | 806 | 100644 | `6eeb957d5c08c82a57b785985e429a4fe3a03392` | `465ef2ca10fbc1a196aba879b9295c55586bf0da9e82096f362447863332970d` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty50.csv` | 51 | 415 | 100644 | `cfeeddd65ef75d117cec01c0dd6b1e9b88f0b068` | `4beaea49925866c967d2fc3930376eb1c071d3878441b9486d86ad081120b471` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_auto.csv` | 16 | 138 | 100644 | `b5f274b45f14bc8731d2e823eeb77e7609fe8717` | `18555d4cbd0c6fffd72655a19521eb625044e2f0613233b9a7c3153fb25d3cd7` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_bank.csv` | 15 | 129 | 100644 | `4b254a5e6a3936f8f7b2db0e79280e1298b62be9` | `0b67f1aaf431be0fa21f16c2697d9ab602d42bf9cc9814501064d41cbd897f3c` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_fin_services.csv` | 21 | 179 | 100644 | `cf9d9b8070d569cd3e44f6e9476158358572d129` | `2c7b453eff3fe43aaab1157b19df8307a1f31fdca2f60ea5100e53c7ffb3c36f` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_fmcg.csv` | 16 | 125 | 100644 | `f3b55396a16117ca3de60ec5d40b0aff0cdcfe05` | `686023546f81320e693e40733a02b8f15813108ccbc71c9d720668ce8f78d625` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_healthcare.csv` | 21 | 184 | 100644 | `882c1e5e68b08c90117ee74f08fcdd7d4501401b` | `4417e31df64e9c2dc222c12fc2f2fa5b4908051356212965bae4a03a6580b6f8` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_it.csv` | 11 | 72 | 100644 | `53b7006fd2dfae876b7791f1264d3b663436f6d2` | `6757a678dfc8454923f768f2a6ad7630018919f3b04717b05f8fb46b6e7a9c7d` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_metal.csv` | 16 | 132 | 100644 | `3f7d4e1c6fff4f6deec256fa469680d222bfa180` | `d8e74762f2df08c73db8736eb20b043a30f73494145750cd3242cb5ece1e865e` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_midcap_select.csv` | 26 | 224 | 100644 | `0e4c293c7b73f83fc55f27a47a07526bae2e0a7c` | `3e5c500e12e5ddfe1e006bf0bfef0356ae0802cd7e5f660d980e393ccce66241` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_next50.csv` | 51 | 398 | 100644 | `d34ccf3d21b0175ef677f9e7416c6244d9c75810` | `85831070c0c8ae2df71b32dafac21ee92401f3812494ccf02ec810ce1c7dd86e` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_oil_gas.csv` | 16 | 106 | 100644 | `698d85c344b93c11e059f0f64cf731cb2636735b` | `a902693122f3ae17ad9e0fdb5c2a6e417f8f70a76cdbe967bbb362dcb057b01a` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_pharma.csv` | 21 | 187 | 100644 | `d2975627cb89c1207ac0bdce3fe3be35f8c7fc8d` | `4063de3f328d351f8f64ec95ef5422d3c5d52c0bc19bc20788d906a2b0b186de` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_private_bank.csv` | 11 | 105 | 100644 | `90c4ff5abc2c49eccb5530157208db88da99dbf2` | `86f2ce1502e66c2954d18b2821cca4a139dd3b07f7cc89e89b2f0bdb89b6acfd` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_psu_bank.csv` | 13 | 96 | 100644 | `29600f535bfb7c05646b8ff913f2ee9c723cc00d` | `d046c0994040955c1b288c4fbe08973e14e9c0ffbc0c4c2b172899467f2f900c` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/index_members/nifty_realty.csv` | 11 | 92 | 100644 | `e496ec7b9d696a1762d21a06d2bb6b8b87022a55` | `91f617c4286398255464dddf19e8cdfa93f869de954e026a3cd4fad4d5798f40` | 1 | bcf03b5, 2026-04-17 |
| `config/reference_data/security_master_file.csv` | 2802 | 204514 | 100644 | `2794185899f777cb0fe3a757b1e8967e2a7d65fb` | `464d85ea45c2c8ce7aaf90c2704795cc28f86b508869f94ad43270db385019ba` | 1 | bcf03b5, 2026-04-17 |
| `config/scan_webhook_map.yaml` | 84 | 3067 | 100644 | `54dd98d75f276f9b82027707702df2ee619b11f7` | `8393ef08e16b9dce39bc287bc408f730131498f669a195f54c90aaa393b1aed0` | 2 | 5a71fb6, 2026-07-13 |
| `config/scoring_weights.yaml` | 44 | 2610 | 100644 | `e9d6ede4c02d5766acb450e84b1acba78102d89d` | `6a0bd4817243be35039846dcf5b017190764d5d509ad7263d68b2a9e1b98b76b` | 10 | c1ad82e, 2026-07-12 |
| `config/security.yaml` | 155 | 9651 | 100644 | `db5a28676274e252c7749f3f306bad7ef3597132` | `8059ea108941cb39bce169b4c23808ecd5d307f5c4b605cbba9a5c44f9a9f7e5` | 10 | e6ade32, 2026-07-26 |
| `config/slippage_model.yaml` | 17 | 605 | 100644 | `b5459a4ef307729503b97d070d1ef633cb4a495f` | `1b325c65998339a3925225d58d0c92c100a31fcc7bc8afd324099d1aff00a48e` | 1 | bcf03b5, 2026-04-17 |
| `config/strategies/first_pullback_long.yaml` | 54 | 1121 | 100644 | `bba1441d7cc33e295d738397238d751a7d5c06bf` | `df2aefdff8f2649c56b21914dc5c85470755bfe15499aafb792a9afd13fd5257` | 11 | 5a71fb6, 2026-07-13 |
| `config/strategies/first_pullback_short.yaml` | 54 | 1127 | 100644 | `d946da39a9c53a105b43573b6121d6784ec8f65c` | `a92b8fa5ad0e11b56f7085f7bbfe88e7e05c9cd3a48cd8559d372fde5abdd54e` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategies/gap_fade_long.yaml` | 56 | 1285 | 100644 | `6e0c95d5191d0cf2788f9d81c2f26a74ec6fdb6a` | `9b3a85dafa49ac4ad9ea175f036f5610811fced6d12899884d28cb1fcd8b0a1c` | 15 | 5a71fb6, 2026-07-13 |
| `config/strategies/gap_fade_short.yaml` | 55 | 1211 | 100644 | `a78b93440fe5c18522ff5796f72b5dad7aaf9505` | `a9b7ea7756f6da905416406fcb8e33d183c1099d7a8dede907ccb76c83498223` | 11 | 5a71fb6, 2026-07-13 |
| `config/strategies/gap_go_long.yaml` | 56 | 1265 | 100644 | `6e6656fbc6ed80f9dd749bb4837562a3e0dfdb65` | `189d9cbe8ff56f53d61b9dd3c2ac4aa9ff2e1c354f6088d292eba2b90518670f` | 12 | 5a71fb6, 2026-07-13 |
| `config/strategies/gap_go_short.yaml` | 56 | 1259 | 100644 | `7e53d31871d6efb65a6d452ed70c25fb0c444442` | `863dba5eb9410f3e08b9701ced09781495fe18a3ea08fd53c601d64b469e0119` | 12 | 5a71fb6, 2026-07-13 |
| `config/strategies/open_high_breakdown_short.yaml` | 55 | 1228 | 100644 | `96b354653687a2f36d450688552e5cd906372dcd` | `008506c249e20b83c1de7dbc1eb41d199d45eb692f8bc6589b656ba1f7e54cd4` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategies/open_low_breakout_long.yaml` | 54 | 1150 | 100644 | `48012d053f3335e45feec688d3a157961469f5cb` | `8869b671076f119dbc5bfcd34551924eca9b1b1459858b1b2ee1a21412d7f8a3` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategies/pb01_breakout_retest.yaml` | 79 | 3051 | 100644 | `eedf5cac5ed5132665160a1aac9cce30cf4a38ed` | `bcf9244cbbba2b21bf5701af26e48e1de0eb629312d9c02c5caefe8fa6474929` | 1 | 5a71fb6, 2026-07-13 |
| `config/strategies/positional_momentum_long.yaml` | 55 | 1310 | 100644 | `7a46596fac63e73dc56949da04212b8d6dffa002` | `299cda0ad004aeb93a8f75d36fb8fd49af0bb11325d022f089101d1d9078eb09` | 14 | 5a71fb6, 2026-07-13 |
| `config/strategies/positional_sector_rotation.yaml` | 55 | 1315 | 100644 | `b110bd594203692317aa68b3c60915d4224e2a20` | `db2b4a4771e97d0beddd995e7d58fbf65fb173e19265f4d4bdc5043b21af9732` | 14 | 5a71fb6, 2026-07-13 |
| `config/strategies/positional_swing_long.yaml` | 55 | 1291 | 100644 | `597193f8076a8c7b3d9c1234e55e09ee8502696f` | `07049dc7d176f279371d01bef9158f1595278f97ea33a3fe675a6ccc969276b3` | 14 | 5a71fb6, 2026-07-13 |
| `config/strategies/range_breakout_long.yaml` | 55 | 1220 | 100644 | `ddee444cade6dd2d911de428a70130647ceb2770` | `d34e6323f419febb29286301f8ca455e4b6d745c14d618e717dafd5271ebf713` | 11 | 5a71fb6, 2026-07-13 |
| `config/strategies/range_breakout_short.yaml` | 54 | 1140 | 100644 | `2f99b1dd5f155bb458b0ddfe3e50366f5892f3ca` | `de11663af31acdeae80c0eb7709b2f5e199df19f7e00005312a1c8c1f999ebea` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategies/vwap_bounce_long.yaml` | 54 | 1109 | 100644 | `e279719f9e5d75b545cb1f89011cee0ced78d63b` | `c6f0333ccf1afdddd96bae128c054965469582528d7148b5c189220f884b30b8` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategies/vwap_rejection_short.yaml` | 54 | 1133 | 100644 | `a62177d49e35bba977750f22c9eaf64bf440c0d3` | `41e854f6b31ce484108275a2e13467e97c02c3f4ffaede01d121adb4b05c64aa` | 10 | 5a71fb6, 2026-07-13 |
| `config/strategy_direction_registry.yaml` | 154 | 5745 | 100644 | `b03f4ed0c90043840f339fc9b5dac6cca93bf736` | `a260a786ef55f3e6ce42bcb473bd577d378490a32563286a8d025f8fe6cc0974` | 1 | 26885bb, 2026-07-18 |
| `config/symbol_aliases.yaml` | 10 | 393 | 100644 | `09f1ff37a59ae464dc249be3bb32fe8efca76668` | `79591ae6daa8b39071d1d8bf268c3edb9e107b341561310a437f63e086be1c46` | 2 | 435b3a2, 2026-05-07 |
| `config/system_config.yaml` | 753 | 55901 | 100644 | `bf742ae5c81c60614370361998e6a102a1064ff7` | `819efd387ac983118e41ed4ca03b4636a38c60f64300e9b9500d6c50fe525b32` | 124 | 5f75c9b, 2026-09-10 |
| `core/config_loader.py` | 2516 | 127242 | 100644 | `8635bca77531515561ee48cf92677883a5e30782` | `4e4f0d5c1acee0eb1f3216c69c8fe8be4d89b61d867c9a9a3576f173edcfbece` | 88 | 5f75c9b, 2026-09-10 |
| `core/config_validator.py` | 274 | 9514 | 100644 | `8581e82973f158589e74432d1bb41e415bc82ec0` | `877d308b4a4e14b293b842d5b959e2b1dbe374b5e5b11259cb5bd1d7dc81927e` | 1 | 419c430, 2026-05-02 |
| `core/config_auditor.py` | 858 | 45055 | 100644 | `054d58298b58cd74f40d1b899022a89983247eea` | `0af364c1f2e35b95b49a8961fc1ccf47bbae95487cdcb92e6a28da0221671904` | 10 | 076fe57, 2026-08-23 |
| `core/config_snapshotter.py` | 217 | 10293 | 100644 | `3bb8ce1de7ce2f6d6a096b0195e3ff41b39d6973` | `b012f65a2939df8a173f950b9fc85739210d8e075d471c43f780a388553f8e10` | 3 | 4c495d0, 2026-08-22 |
| `strategies/schema.py` | 375 | 14263 | 100644 | `22530161a5ee5a24bd85a7701b45269b3f2bacdb` | `fbd38cdb178cd5f6cb73ffeec06f11df1d9a320e0a3e35010e6205dfb5a6d1c8` | 12 | 5a71fb6, 2026-07-13 |
| `strategies/loader.py` | 213 | 9811 | 100644 | `99e83b192021297a3df472840728b88123c7b891` | `f565b82c51b29a57794cbff86cd90abafaa23060186008fdb818c5c34395be99` | 4 | 34fd6a5, 2026-07-18 |
| `.env.example` | 50 | 1979 | 100644 | `d9a910411265046e4d9df153cb09a67d6e7f624d` | `1141095a95af94c8ffdeaf544af01f2239bcbba3ed8d9193f7b03dc4eac0cad8` | 4 | 7bc3367, 2026-07-02 |
| `scripts/revert_temp_config.py` | 237 | 7828 | 100644 | `576c4c0b07f3dbffd1208fd2a4d1c78bb064503d` | `2a976412aac04e032992033f593821973e79dd7653887866c2b27c9748bf9a2b` | 2 | c69f1fd, 2026-06-24 |

## 2. Changes after the last recorded deployment

The last recorded deployment is commits `686df1c847d415958c4df406b77503bb45975749` (2026-09-02) and `7d4970a26991fd40774023f5293a00556228e14b` (2026-09-02) (D-21); the baseline is 32 commits after `7d4970a`.

FACT (`git diff 7d4970a 970aabf`): two of the 58 A02 paths changed after `7d4970a`; the other 56 are identical at both commits.

| A02 file | Lines added / removed | Commits after `7d4970a`, as recorded in the commit (date, IST) |
|---|---|---|
| `config/system_config.yaml` | 39 / 4 | `5455ced` (2026-09-03 22:32): "fix(mis-squareoff): STOP A -- finish before the broker acts, and never leave a position naked (schedule + F2 settle window + F1 restore)"; `5f75c9b` (2026-09-10 15:36): "feat(config): MIS squareoff protected-MARKET bands, PASS_1 1.5 / PASS_2 2.5" |
| `core/config_loader.py` | 38 / 0 | `5f75c9b` (2026-09-10 15:36): as above |

UNKNOWN / NOT ESTABLISHED: whether production ran any commit after `7d4970a`, so whether these values and this code were ever in force.
