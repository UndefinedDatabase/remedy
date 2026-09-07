── STEP T002 (the cockpit states, landed) — F272 ─
Goal:        Land the C4 round 11 measured and correctly refused to commit: free
             the one guard whose arity pin blocks it, then give `blocked` and
             `stopped` their place in the two digest modules, so R-0821's fix is
             on disk rather than only claimed.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 11
             verdict, the R-0821 correction and two prose slips · C3 DECISION
             F272 D9 · C4 the guard · C5 the two modules · C6 the Landed line ·
             C7 the handback.
Change:      EXACTLY the paths listed under "The change set" and nothing else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line one run of 2 — both measured, not recalled.

## What the reviewer MEASURED before ordering this (§3 item 34)

Round 11 PASSED. It landed C0a through C3 exactly as ordered and then STOPPED at
C4, under the clause this block's predecessor wrote for exactly that case, having
measured five ways that `tests/ui_contracts/` could not reach EXIT 0 with C4
applied. It escalated the one ruling it was not permitted to make. That ruling is
DECISION F272 D9 below, and this round is the rest of the work.

Every reading below was taken BY ME at `fcde1983`.

- THE BLOCKER IS REAL AND I REPRODUCE IT.
  `tests/ui_contracts/test_digest_hero_card.py:230`, inside
  `TestNoRuleHasASecondHome` at line 224, reads `assert len(phrases) == 7` over
  `digest_state_phrases()`, which parses `DIGEST_STATE_LABELS` out of
  `digestCardCopy.ts`. C5 puts two entries in that map, so the parse returns 9
  and the equality fails. No choice of labels avoids it: any two entries make it
  9. This is R-0821's own defect class — a hard-coded seven that goes stale the
  moment the enum widens — one layer further out, and invisible until the fix
  lands.
- THE GUARD WAS NEVER MEANT TO PIN THE ARITY, and its own text proves it. Its
  failure message reads "the parse found only {phrases}; a reader that returns
  almost nothing would make the loop below vacuous" — that describes a FLOOR.
  The real assertion is the next one, `restated == []`.
- THE REPOSITORY'S OWN CONVENTION FOR THIS GUARD IS A FLOOR, and this line is
  the outlier. The same vacuity guard, with the same wording, appears twice more
  in the same suite: `tests/ui_contracts/test_digest_card_copy.py:433` and
  `tests/ui_contracts/test_job_digest_card_contract.py:531`, and BOTH read
  `>= 7`. Those two are precisely the tests R-0821 is about, and they are green
  on a widened enum for exactly the reason this one is not. The other `== 7`
  assertions in the suite — `test_graph_architecture.py:395` and `:560`,
  `test_ux_quality.py:525` — are over zoom levels, a genuinely fixed arity, and
  are none of this round's business.
- TWO STALE NUMERALS SIT IN THE SAME FILE, at line 128 ("The seven `RunState`
  label PHRASES") and line 225 ("None of the seven `RunState` phrases"). Both
  are §3 item 16's class and both go, because a count of a set the reader can
  count unaided is the half nobody re-reads.
- THE BASE READINGS THIS ROUND GATES AGAINST, each run by me at `fcde1983`:
  `tests/ui_contracts/` EXIT 1 at 2 failed / 807 passed / 4 skipped, the two
  failures being the pair R-0821 names; `tests/docs/` EXIT 0 at 303; the canary
  EXIT 0 at 42. `tests/orchestration/` was EXIT 0 at 12847 passed / 10 skipped
  at `1bfb1cd9`, and round 11 changed no `.py` file, so that reading stands.
- THE APPEND TARGETS at `fcde1983`: `.agent/live_review.md` 1127168 bytes / 703
  units, registrations 305, resolutions 247, open BY DISTINCT ID 58, `^Gate: `
  33, `^Landed: R-0821 ` 0; `.agent/prose_slips.md` 139621 bytes / 177 units;
  `docs/roadmap/features/T2_F272.md` 32918 bytes / 70 units, headings D1 to D8.
  Each file's terminal byte is exactly one newline.
- WHAT ROUND 11 LEFT OVERSTATED ON DISK, which C2 corrects by APPENDING and
  never by rewriting (§3 item 20). Round 11 applied its slices byte for byte as
  constraint 1 required, and three of them describe a C4 that did not land:
  R-0821's "FIX, LANDED BY THIS ROUND", the plan's Current Step, and DECISION
  F272 D8's REVERSE clause. The plan is replaced this round anyway; D8's ruling
  is unaffected because it rules a PLACEMENT and not a landing; and the record
  entry is append-only, so C2 appends the dated correction and the landed
  paragraph stays exactly as written.

## What the OPEN SET binds on this block (§3 item 34, last clause)

"BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, same words, in the
Handback section. R-0821's own clause, that a block changing a state vocabulary
NAMES `tests/ui_contracts/` in its gate list — APPLIED: G4 and G5 below are that
suite. R-0819's shadow-property clause — DECLINED AS NOT APPLICABLE, still owed
by T003/T004. R-0820's clause, that a gate must not be computed from the same
predicate as the change set — APPLIED: the gates are the repository's own
pre-existing tests, written against `packages/core/models.py`.

## The change set

C2: `.agent/live_review.md`, `.agent/prose_slips.md`.
C3: `docs/roadmap/features/T2_F272.md`.
C4: `tests/ui_contracts/test_digest_hero_card.py`.
C5: `apps/ui/src/api/digestVisibility.ts`, `apps/ui/src/api/digestCardCopy.ts`.
C6: `.agent/live_review.md`.
C0a/C0b/C1/C7: `.agent/authored/f272-r12.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/handoff.md`.

If a vitest file under `apps/ui/src/api/` must change to keep G6 green, that is
INSIDE this change set — report it with the reason. Nothing else is. In
particular no OTHER file under `tests/ui_contracts/` is touched: C4 frees ONE
assertion that DECISION F272 D9 rules on, and the rest of that suite stays the
gate it is.

## C4 — the guard, a SPEC and not a slice

In `tests/ui_contracts/test_digest_hero_card.py`, three edits and no others:

1. Line 230, `assert len(phrases) == 7` becomes `assert len(phrases) >= 7`,
   which is the spelling its two siblings already use for the same guard with
   the same message. Do NOT touch the message, and do NOT touch the assertion
   that follows it — `restated == []` is what the test is FOR and it is
   unchanged by this round.
2. The class docstring at line 225 loses its numeral: "None of the seven
   `RunState` phrases" names the set instead of counting it.
3. The `digest_state_phrases` docstring at line 128 loses its numeral the same
   way.

Do NOT touch `test_the_phrase_restatement_scan_can_see_a_restated_phrase`, the
discriminator that proves the scan can see a restated phrase even when one is
there. It is what keeps the loosened floor honest, and after C4 it is the only
thing standing between this guard and vacuity — so it must still pass, and G4
reports it BY NAME.

## C5 — the two modules, a SPEC and not a slice

`digestVisibility.ts`: add `"blocked"` and `"stopped"` to `SETTLED_STATES`, per
DECISION F272 D8. Update the comments that count the partition — the block
comment above `SETTLED_STATES` calling `paused` "the most report-worthy rest of
the four", and the one above `digestStateClass` saying "The seven members of
`RunState`" — so no sentence states a figure its own body contradicts. Prefer
naming the set to counting it.

`digestCardCopy.ts`: add `"blocked"` and `"stopped"` to `DIGEST_STATE_LABELS`.
Round 11 measured `"Blocked"` and `"Stopped"` against the copy audit and it
refused neither; use them unless the audit refuses them at this tree, in which
case report what it refused and what you used. Update the module's own "seven
`RunState` members" comment the same way.

DO NOT touch `DIGEST_CTA_RULE_IDS` — its `stopped-by-operator` and
`blocked-failed` entries are RULE ids from `recommended_next_action`, a
different vocabulary the module's own comment names as a trap for exactly this
confusion. DO NOT touch `UNREADABLE_STATE_LABEL` or the unknown class: this
round removes two words from that category, not the category.

## C6 — the Landed line, a SPEC and not a slice

APPEND to `.agent/live_review.md`, as its own commit AFTER C5, exactly one line
of the form the rules fix — `Landed: R-0821 — ` followed by one sentence naming
what changed and the commit C5 created. Nothing else, no `Done:` paragraph, no
second line. The reviewer replaces it with the authored resolution at the next
gate; a surviving `Landed:` line is an unreviewed fix, which is what it should
look like.

## Constraints

1. NO SLICE IS EDITED — apply the authored texts byte for byte between their
   markers; if one looks wrong, apply it anyway and say so. C4, C5 and C6 are a
   SPEC: write that code yourself.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, C7, nothing reordered; C1 is
   the first substantive commit (§3 item 23). C4 lands BEFORE C5 so that the
   guard is a floor before the map widens; the reverse order reddens the branch
   at an intermediate commit for no reason.
4. APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, the slice
   being the marker-delimited lines each with its terminating newline, and the
   post-image ending in exactly one `\n`. PLAN CONVENTION: `.agent/plan.md` is
   REPLACED by exactly the PLANF272R12 slice.
5. Behaviour changes: exactly two states stop being unreadable. No other state,
   label, rule id, threshold or fallback changes, and no assertion is weakened
   beyond the single floor DECISION F272 D9 rules on.
6. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
   C6 is the ONE exception the rules make: a single `Landed:` line.
7. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never the primary checkout (protocol G5); remove
   and prune it before the handback, BY EXACT PATH and never by glob. A fresh
   worktree has no `apps/ui/node_modules`, so any vitest run inside one needs
   that directory restored with `shutil.copytree(..., symlinks=True)` — the
   argument, not the default, per R-0591.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before
   C7, and table all three; if it appears, finish only the half-written commit,
   then hand off (protocol G6).
9. `python3 -B` for every run; report each gate's REAL exit code, "green" as a
   word being a finding.

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r12.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2 and C6.** Readers (a) to (d) over `.agent/live_review.md`
for C2, and (a) and (b) over `.agent/prose_slips.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and
never taken from this block: units before, after, delta; the last N units equal
the slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it first;
(a) and (b) must BOTH reject; restore and require both to accept and the
restored image to equal the disk image.
(d) COUNTS before → after C2: `^- R-\d{4} — ` distinct ids 305 → 305; `^Done:
R-\d{4} — ` distinct 247 → 247; open set BY DISTINCT ID 58 → 58; `^Gate: ` 33 →
34; `^Gate: F272 R11 ` 0 → 1 — the first three unchanged because this round
mints no id and resolves none. Then AFTER C6, report `^Landed: R-0821 ` 0 → 1
and confirm `^Done: R-0821 ` is still 0.

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3.** The plan: `.agent/plan.md`
equals the PLANF272R12 slice bytes exactly; report the equality, both byte
lengths, the line count against the AGENTS.md cap of 50, and that `## Goal` and
`## Next Steps` are present. The feature file: readers (a) and (b) of G2's
wording, no negative control (gate budget); plus the count YOU measure of
`^### DECISION F272 D\d+ ` lines and the D-number each names, in order.

**G4 THE GUARD IS STILL A GUARD, at C4.** The floor may not buy itself green.
(i) `python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly` at C4 must read
EXACTLY the base: EXIT 1, 2 failed, 807 passed, 4 skipped. C4 changes a bound
that 7 already satisfied, so a DIFFERENT count here means C4 did more than it
was ordered to.
(ii) `test_the_phrase_restatement_scan_can_see_a_restated_phrase` passes, named
explicitly with its own result — it is the discriminator that keeps the loosened
floor honest.
(iii) THE REAL ASSERTION STILL BITES, proved in a disposable worktree at the
commit C4 creates: `CARD` in that test module resolves to
`apps/ui/src/components/digest/DigestHeroCard.tsx`, which exists at `fcde1983`
at 5568 bytes — print the resolved path to confirm it, then add one line
restating a parsed phrase as a string literal there and require
`test_no_run_state_phrase_is_restated_as_a_literal` to go EXIT 1 naming that
phrase. Restore, confirm byte-identical, re-run EXIT 0. This is the proof that
loosening `==` to `>=` did not turn the test vacuous.

**G5 THE TWO RED TESTS GO GREEN, at C5.**
(i) `python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly` EXIT 0. Against
the base of 2 failed / 807 passed / 4 skipped, passed must rise by exactly 2 to
809, failed must be 0, skipped must stay 4. Report all three numbers.
(ii) THE RED CONTROL, in a disposable worktree at the commit C5 creates: remove
the single `"blocked"` entry from `SETTLED_STATES` in `digestVisibility.ts` —
count that exact byte string in that file first, where it must be 1 (§3 item 25)
— and require `test_job_digest_card_contract.py` to go EXIT 1 naming `blocked`.
Restore, confirm byte-identical, re-run EXIT 0.
(iii) WHAT A READER OF THE CARD SEES, which no test asserts: parse
`DIGEST_STATE_LABELS` out of the module and print the value for `"blocked"` and
for `"stopped"`, confirming neither is `UNREADABLE_STATE_LABEL`.

**G6 VITEST AND THE SUITES.**
`python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly`
EXIT 0 in the PRIMARY CHECKOUT, the only tree carrying `apps/ui/node_modules`;
this node runs `npx vitest run` over the whole UI suite and is the gate on all
three `.test.ts` files importing the modules C5 edits. If it goes red, report the
failing specs verbatim before changing anything. Then, serially, `tests/docs/`
and the canary `tests/cli/test_golden_path.py`, both EXIT 0 against a base of 303
and 42. `tests/orchestration/` and `tests/cli/` are NOT ordered in full: no `.py`
file outside `tests/ui_contracts/` changes this round. State that reasoning
rather than reporting a suite you did not run.

**G7 LINT AND INTEGRITY, at C5.** `python3 -m ruff check` over exactly the `.py`
files this round changed — that is `tests/ui_contracts/test_digest_hero_card.py`
and nothing else — in ONE invocation. EXIT 0, or every diagnostic proven
PRE-EXISTING by linting the `fcde1983` blob through
`ruff check --stdin-filename <path> -`, which is the non-writing route R-0594
requires; report which. `npm run lint` is NEVER ordered in this repository.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C7 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming every worktree you
created and confirming its removal by exact path. Per commit C0a through C6 —
NOT C7, which cannot count its own insertions (§3 item 14) — the insertion count
from `git diff --numstat <parent> <commit>`, each single-parent and under the
F104 D1 cap of 500; those same numbers fill the handback's `## Commits` `+/-`
column, so report both readings side by side and confirm each row cell by cell
(§3 item 28). Marker sweep: the number YOU measure of `<<<BEGIN `/`<<<END `
lines in every written non-block file, zero in each. The three `.agent/STOP`
readings as a table.

## The slices

<<<BEGIN PLANF272R12>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 11 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, and renamed
`JobPlan.status` to `state` at the 234 measured sites of DECISION F272 D7.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Land R-0821's fix. Round 11 ruled the placement as DECISION F272 D8 and then
measured that a third guard, an arity pin in
`tests/ui_contracts/test_digest_hero_card.py`, reddens the moment the label map
widens; DECISION F272 D9 rules that guard a FLOOR, as its two siblings already
are. This round frees the guard, then gives `blocked` and `stopped` their place
in `digestVisibility.ts` and `digestCardCopy.ts`.

## Next Steps

1. Move three of the `state` collapse: retype `JobPlan.state` to `RunState` and
   make the six `JOB_*` constants `RunState` members, with `.value` at every
   boundary leaving the record. The rendering guard round 10 shipped in
   `tests/orchestration/test_job_state_field.py` is what that move must keep
   green, D7's probe is the method for finding its site set, and R-0821's clause
   puts `tests/ui_contracts/` in that round's gate list.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A vacuity guard written as an equality pins an arity nobody meant to pin, and
  goes stale exactly when a vocabulary grows. Two more sit in this suite over
  zoom levels; both are genuine fixed arities and neither is F272's business.
<<<END PLANF272R12>>>

<<<BEGIN RECORDR12>>>
Gate: F272 R11 — the F272 round 11 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `1bfb1cd9`..`fcde1983`, six commits, every one single-parent, in the bundle's ordered sequence C0a, C0b, C1, C2, C3 and C6; the two ordered commits C4 and C5 are ABSENT and that absence is the round's substance and is upheld. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r11-block.md` was written and hashed BEFORE delegation, and it, the committed `.agent/authored/f272-r11.md` and the committed `.agent/last_block.md` are all 32960 bytes at 363 lines and all hash to `6575c005b2b8bfca32818ff20c24122921aa205a86858f310b3860f75be9d1d3`; per §3 item 37 that chain covers those three artefacts and is not a claim about emitted bytes. G2 THE RECORD reproduces byte for byte under the reviewer's own readers: `.agent/live_review.md` 1118077 to 1127168 and `.agent/prose_slips.md` 136942 to 139621, each pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE for both, reader (b) accepting at N counted 2 and 3 with units 701 to 703 and 174 to 177; registrations 304 to 305, resolutions 247 unchanged, open set BY DISTINCT ID 57 to 58, `^Gate: ` 32 to 33, `^Gate: F272 R10 ` 0 to 1, `^- R-0821 — ` 0 to 1, and `^Landed: R-0821 ` correctly still 0. G3 THE PLAN is 2187 bytes byte-equal to its slice at 42 lines against the cap of 50, and THE FEATURE FILE appended 30008 to 32918 with reader (b) accepting at N counted 7 and units 63 to 70, headings D1 through D8 in order. THE CHANGE SET IS EXACTLY THE FIVE `.agent/` PATHS AND THE FEATURE FILE: no `.py` and no `.ts` file was touched, which is what an honest stop at C4 looks like. THE REFUSAL IS CORRECT AND THE REVIEWER REPRODUCES ITS CAUSE: `tests/ui_contracts/test_digest_hero_card.py:230`, inside `TestNoRuleHasASecondHome` at line 224, reads `assert len(phrases) == 7` over `digest_state_phrases()`, which parses `DIGEST_STATE_LABELS` out of `digestCardCopy.ts` — so the two entries C5 adds make the parse return 9 and the equality fails, for any choice of labels whatever. The block ordered the worker to stop rather than edit `tests/ui_contracts/`, and it stopped. THE REVIEWER'S OWN READING GOES FURTHER THAN THE WORKER WAS PERMITTED TO: that line's failure message says "a reader that returns almost nothing would make the loop below vacuous", which describes a FLOOR and not an arity, and the SAME guard with the SAME message appears at `tests/ui_contracts/test_digest_card_copy.py:433` and `tests/ui_contracts/test_job_digest_card_contract.py:531` — both spelled `>= 7`, and both being exactly the tests R-0821 names. The equality is the outlier and DECISION F272 D9 rules it back to the convention. NO SECOND ID IS MINTED FOR IT, per §3 item 30: it is the same defect R-0821 already describes — a hard-coded seven that goes stale when the enum widens — reached one layer further out, so the evidence joins R-0821's fix rather than starting a second thing to resolve. THE WORKER'S FIVE-WAY MEASUREMENT IS ACCEPTED AS THE ROUND'S REAL PRODUCT: it isolated the copy half as the whole cause, confirmed the visibility half introduces no new red, ran vitest EXIT 0 at 52 passed in a worktree with C4 applied and `node_modules` restored by `copytree(symlinks=True)` as constraint 7 requires, and demonstrated the red control fires. Its labels `"Blocked"` and `"Stopped"` are ratified. Deviations 1, 3 and 4 are accepted as declared. DEVIATION 2 IS UPHELD AND IS THE REVIEWER'S SLIP: constraint 1 made the worker apply four slices byte for byte, and three of them describe a C4 that did not land — R-0821's "FIX, LANDED BY THIS ROUND", the plan's Current Step, and D8's REVERSE clause. The worker edited not one byte and declared all three, which is the only correct conduct available to it. The correction is the paragraph below and the landing is this round's C5; the landed text is NOT rewritten, per §3 item 20.

Correction: R-0821 — 2026-09-07, F272 round 12. The fix clause of R-0821, appended at `6373dc0e`, reads "FIX, LANDED BY THIS ROUND", and that was FALSE ON DISK from the moment it was written: the round that wrote it stopped at C4 without touching either module, for the reason the R11 gate entry above records. The clause was authored by the reviewer before the round ran and asserted a landing that the block's own STOP condition then correctly prevented — the §3 item 20 class, an authored slice stating a fact about its own round's change with no constraint able to guarantee it. R-0821's registration paragraph stands unrewritten because this record is append-only and a dated correction is how it stays honest. THE FIX ACTUALLY LANDS AT F272 ROUND 12, whose C4 frees the arity guard under DECISION F272 D9 and whose C5 adds `blocked` and `stopped` to `SETTLED_STATES` in `apps/ui/src/api/digestVisibility.ts` and to `DIGEST_STATE_LABELS` in `apps/ui/src/api/digestCardCopy.ts`; the `Landed: R-0821` line that round's C6 appends is the first honest on-disk statement that the fix exists, and the reviewer's `Done:` paragraph follows at the next gate. R-0821 stays OPEN until then, and its counter-measure — that a block changing a state vocabulary names `tests/ui_contracts/` in its gate list — is unaffected by this correction and is applied by round 12.
<<<END RECORDR12>>>

<<<BEGIN SLIPSR12>>>
2026-09-07 · F272 R11 block, the R-0821 slice (reviewer) · The finding slice C2 committed said "FIX, LANDED BY THIS ROUND" while the fix was ordered two commits later at C4, and the block's own STOP clause then stopped the round before it. A slice bound for the append-only record may state a fact about its own round's landing only when a block CONSTRAINT fixes the commit order in a way the worker cannot satisfy by accident — R-0524's carve-out — and a clause that a STOP condition can falsify is not that. Two forms are safe and this was neither: name the constraint, or word the fix as what the round ORDERS rather than what it achieved. The same block's plan slice and DECISION D8 REVERSE clause carried the same shape, so one authoring habit put three overstatements on disk in one round.

2026-09-07 · F272 R11 block, gate G4 (reviewer) · G4 ordered `tests/ui_contracts/` to EXIT 0 after C4, and the reviewer had run that suite at base and read its two failures — but read them as the two tests R-0821 names and never asked what ELSE in the suite reads `DIGEST_STATE_LABELS`. A third test, `test_digest_hero_card.py:230`, pins the map's arity at seven, so the ordered gate was unreachable by any C4 whatsoever. Running a gate at its base proves it can FAIL; it does not prove it can PASS, and a gate that orders a suite green after a widening is checked against every reader of the thing being widened — `rg -l DIGEST_STATE_LABELS tests/` answers it in one command, and would have.
<<<END SLIPSR12>>>

<<<BEGIN DECISIONR12>>>
### DECISION F272 D9 (2026-09-07, F272 round 12) — the run-state phrase guard in `test_digest_hero_card.py` is a FLOOR, as its two siblings already are; an equality there pinned an arity nobody meant to pin

CONTEXT. Round 11 ruled `blocked` and `stopped` into the cockpit as DECISION
F272 D8 and then could not land the change. `tests/ui_contracts/
test_digest_hero_card.py:230` reads `assert len(phrases) == 7` over
`digest_state_phrases()`, which parses `DIGEST_STATE_LABELS` out of
`digestCardCopy.ts`; the two entries D8 requires make that parse return 9, so the
equality fails for any choice of labels. The worker measured it five ways and
stopped rather than edit the suite that was gating it, which is what its block
ordered.

CHOSEN. THE ASSERTION BECOMES `>= 7`. Three readings settle it and none of them
is a preference. FIRST, the line's own failure message reads "a reader that
returns almost nothing would make the loop below vacuous" — it describes a
FLOOR, and a floor is what a vacuity guard is for. SECOND, the identical guard
with the identical message appears twice more in the same suite, at
`test_digest_card_copy.py:433` and `test_job_digest_card_contract.py:531`, and
both are spelled `>= 7`; those two are precisely the tests R-0821 is about, and
they survive a widened enum for exactly the reason this one does not. The
equality is the outlier, not the convention. THIRD, the assertion the test
EXISTS for is the next one, `restated == []`, and it is untouched — as is
`test_the_phrase_restatement_scan_can_see_a_restated_phrase`, the discriminator
that proves the scan sees a restated phrase when one is there. Loosening the
floor therefore removes an arity pin and removes no protection.

NO SECOND FINDING ID IS SPENT ON IT. This is R-0821's own defect — a hard-coded
seven that goes stale when the enum widens — one layer further out, so per §3
item 30 the evidence joins R-0821's fix instead of starting a second thing to
resolve. It was invisible until the fix landed, which is why round 11 and not
round 10 found it.

NOT CHANGED BY THIS RULING: the other `== 7` assertions in the suite, at
`test_graph_architecture.py:395` and `:560` and `test_ux_quality.py:525`, are
over zoom levels — a genuinely fixed arity, deliberately pinned, and none of
F272's business. This ruling reaches run-state vocabulary guards and nothing
else.

ALTERNATIVES CONSIDERED. Change the 7 to a 9 — rejected: it re-arms the same
trap one enum member later, and the guard was never meant to pin arity at all.
Leave the guard and abandon D8 — rejected: it leaves the cockpit unable to name
two states the orchestrator produces, which is the product defect R-0821 exists
for. Delete the vacuity guard entirely — rejected: without a floor the loop below
it passes over an empty parse, which is the exact failure the message names.

REVERSE by restoring the equality; D8's two entries then redden this test again
and the fix cannot land while it stands.
<<<END DECISIONR12>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 6 of feature F272 · round 12`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-`, the item-status table covering C0a through C7 with every
item present exactly once, one line per gate G1 to G8 with its real exit code,
G4's discriminator and restatement readings, G5's three numbers and its red
control, the authored-text proof table, deviations and the next expected action.
No length cap. Per the fix clause OPEN in the record and binding on the next
block that orders a handback: any commit beyond the ordered sequence receives its
OWN `## Commits` row and its OWN item-status row, and the Deviations section says
so in those same words rather than beside a clause that denies it.
