# A07 helper register (for resuming after an interruption or the usage limit)

Each row: pair, part, role, agent ID (to resume with SendMessage), start time (IST), state. A helper whose state is
not DONE is resumed from its own progress log and file; it never starts again from scratch. The next pair starts
only after both helpers of the current pair have handed back (final notification received).

| Pair | Part | Role | Agent ID | Started (IST) | State |
|---|---|---|---|---|---|
| 1 | P01 | writer | a87416f1927c615d1 | 21-Nov-2026 09:06 | RUNNING |
| 1 | P02 | writer | a1f344048b055b337 | 21-Nov-2026 09:06 | RUNNING |
