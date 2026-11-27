import pathlib
p=pathlib.Path("/home/claude/a08/evidence/A08_AUDIT_INTENT_SOURCES_PROJECT_HALF_2026-11-27.md")
t=p.read_text(encoding="utf-8")
S=[
('A01-10 ("Was starting the MIS units and the optional workers before the last guards and the reconcile ... deliberate?"):',
 'A01-10 (whether starting the MIS units and the optional workers "before the last guards and the reconcile" was deliberate):'),
('"live reuses the adapter\'s client; the closure is rate-limited (the `historical` bucket) and returns an empty list without a handle";',
 '"live reuses the adapter\'s client", and the closure "is rate-limited (the `historical` bucket)" and returns an empty list without a handle;'),
('Owner "A02 (key names); the consumers\' owners for unit handling (A08, A11, A10, A12, A18, A04)" (L2110)',
 'Owner A02 for the key names and "the consumers\' owners for unit handling", A08 among them (L2110)'),
('"whether the warmer was enabled (built only with the V2 S&R or structure-exit flags ...) stays UNKNOWN";',
 'whether the warmer was enabled, built only with the V2 S&R or structure-exit flags, "stays UNKNOWN";'),
('"test presence or a test result does not prove production runtime behaviour. Tests are evidence of the tested claim only, at the stated commit and conditions" (L231);',
 '"test presence or a test result does not prove production runtime behaviour", and tests "are evidence of the tested claim only, at the stated commit and conditions" (L231);'),
('the closure "paces through the `historical` bucket and returns `[]` without a client; the fetcher fails safe on an error, a token-lookup error and an empty answer; fake rows have naive dates, newest first" (A05 IS-75)',
 'the closure "paces through the `historical` bucket and returns `[]` without a client", the fetcher "fails safe on an error, a token-lookup error and an empty answer", and the fake rows "have naive dates, newest first" (A05 IS-75)'),
('The register records X as "his statement about how the system was run, not as an answer to A05-07 or A05-08", which "does not settle either question, and nothing is inferred from it",',
 'The register records X as "his statement about how the system was run", "not as an answer to A05-07 or A05-08", which "does not settle either question, and nothing is inferred from it",'),
('the audit "covers the entire system, every area and every flow, not one setting or one example";',
 'the audit "covers the entire system, every area and every flow", "not one setting or one example";'),
('"is carried forward as an OPEN QUESTION to the topics named; A07\'s records and the approved records of other topics are unchanged";',
 '"is carried forward as an OPEN QUESTION to the topics named", and "A07\'s records and the approved records of other topics are unchanged";'),
('"His operational background of 15-Nov-2026 (recorded as his statement about how the system was run, not as an answer to A05-07 or A05-08)":',
 '"His operational background of 15-Nov-2026", "recorded as his statement about how the system was run", "not as an answer to A05-07 or A05-08":'),
('the system\'s secondary filtration "appears to calculate or evaluate some of the same indicators again, which is duplicate work";',
 'the system\'s secondary filtration "appears to calculate or evaluate some of the same indicators again", "which is duplicate work";'),
('clarified as "\'created by mistake\' means without my knowledge coding agent created it by its own assumption"',
 'clarified as "\'created by mistake\' means without my knowledge" and "coding agent created it by its own assumption"'),
('history OPEN; "For every history question, my answer is OPEN. For every new-system proposal presented in this batch, I accept ChatGPT\'s suggestion as a Phase 2 input.";',
 'history OPEN; "For every history question, my answer is OPEN."; "For every new-system proposal presented in this batch", "I accept ChatGPT\'s suggestion as a Phase 2 input.";'),
('his reply records "History: C — OPEN" and "directs that neither Claude\'s evidence lean (weakly B) nor ChatGPT\'s recommendation be turned into his historical answer";',
 'his reply records "History: C — OPEN" and directs that neither Claude\'s evidence lean "(weakly B)" nor ChatGPT\'s recommendation "be turned into his historical answer";'),
('the record\'s account, not his verbatim words: "both routes were used: configuration files were at first changed locally and then pushed to the VM, and later also changed directly on the VM";',
 'the record\'s account, not his verbatim words: "both routes were used", configuration files "were at first changed locally and then pushed to the VM" and later "also changed directly on the VM";'),
('the A08 side "interface only (security rules)", the spot check building its own client from the broker session token file alone;',
 'the A08 side "interface only (security rules)": the spot check builds its own client from the broker session token file alone;'),
]
for a,b in S:
    c=t.count(a)
    if c!=1: print("COUNT",c,"::",a[:90]); continue
    t=t.replace(a,b)
p.write_text(t,encoding="utf-8"); print("batch 3 applied")
