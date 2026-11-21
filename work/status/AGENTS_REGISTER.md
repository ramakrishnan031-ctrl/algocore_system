# A07 helper register (for resuming after an interruption or the usage limit)

Each row: pair, part, role, agent ID (held in a local file outside the backup; used to resume the helper in this session), start time (IST), state. A helper whose state is
not DONE is resumed from its own progress log and file; it never starts again from scratch. The next pair starts
only after both helpers of the current pair have handed back (final notification received).

| Pair | Part | Role | Agent ID | Started (IST) | State |
|---|---|---|---|---|---|
| 1 | P01 | writer | (held locally) | 21-Nov-2026 09:06 | DONE (hand-back 09:32) |
| 1 | P02 | writer | (held locally) | 21-Nov-2026 09:06 | DONE (hand-back 09:29; disclosed: two temporary /tmp files of strategy names, deleted) |
| 2 | P01 | checker | (held locally) | 21-Nov-2026 09:33 | DONE (hand-back 09:52) |
| 2 | P02 | checker | (held locally) | 21-Nov-2026 09:33 | DONE (hand-back 09:52) |
| 3 | P03 | writer | (held locally) | 21-Nov-2026 09:54 | DONE (hand-back 10:21; one backup briefly blocked by a scan hit in the P04 file, retried after P04 fixed it) |
| 3 | P04 | writer | (held locally) | 21-Nov-2026 09:54 | DONE (hand-back 10:23; one backup blocked by a short legacy commit hash, rewritten in full) |
| 4 | P03 | checker | (held locally) | 21-Nov-2026 10:24 | DONE (hand-back 10:43) |
| 4 | P04 | checker | (held locally) | 21-Nov-2026 10:24 | DONE (hand-back 10:45; disclosed: one redirect outside the work folder, denied by the permission system, no file created) |
| 5 | P05 | writer | (held locally) | 21-Nov-2026 10:46 | DONE (hand-back 11:13) |
| 5 | P06 | writer | (held locally) | 21-Nov-2026 10:46 | DONE (hand-back 11:09) |
| 6 | P05 | checker | (held locally) | 21-Nov-2026 11:14 | DONE (hand-back 11:38) |
| 6 | P06 | checker | (held locally) | 21-Nov-2026 11:14 | DONE |
| 7 | P07 | writer | (held locally) | 21-Nov-2026 11:38 | DONE (hand-back 12:04) |
| 7 | P08 | writer | (held locally) | 21-Nov-2026 11:38 | DONE (hand-back 12:05) |
| 8 | P07 | checker | (held locally) | 21-Nov-2026 12:05 | DONE |
| 8 | P08 | checker | (held locally) | 21-Nov-2026 12:05 | DONE (hand-back 12:30) |
| 9 | P09 | writer | (held locally) | 21-Nov-2026 12:31 | RUNNING |
| 9 | P10 | writer | (held locally) | 21-Nov-2026 12:31 | RUNNING |
