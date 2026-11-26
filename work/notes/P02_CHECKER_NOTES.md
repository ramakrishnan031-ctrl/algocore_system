# P02 checker scratch notes (H7)

## Findings so far (to apply)
- S071: "no method calls another method of the class while holding it" is wrong: symbols_due_for_rewarm (L56) and evict_expired (L60) call _age_sec under the lock; _age_sec takes no lock. Correct wording.
- S054 (a): "two to four values" - re-derive; exact arithmetic gives exactly three ({b1, b1+M/2, b1+M}); check FP edge cases by own model script.
- S084: retry claim needs precision: only when the re-warm gives no interval at all; limiter not reached on token failure or None handle.
- S008: __future__ import not listed (minor); aliases _date/_time.
