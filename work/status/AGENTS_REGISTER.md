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
| 3 | P04 | writer | (held locally) | 21-Nov-2026 09:54 | RUNNING |
