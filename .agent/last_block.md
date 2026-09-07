── STEP T002 (the UI states round 8 never reached) — F272 ─
Goal:        Give `blocked` and `stopped` — the two `RunState` members round 8
             added — their place in the cockpit's two digest modules, so the
             card can classify and name a blocked or stopped job instead of
             calling it unreadable; and rule the placement as DECISION F272 D8.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 10
             verdict, finding R-0821 and three prose slips · C3 DECISION F272
             D8 · C4 the two modules · C5 the Landed line · C6 the handback.
Change:      EXACTLY the paths listed under "The change set" and nothing else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line one run of 2 — both measured, not recalled.

## What the reviewer MEASURED before ordering this (§3 item 34)

Round 10 PASSED and every one of its gates was re-run by me. While gating it I
found a defect that is NOT round 10's and that no round of this feature has been
able to see. Every reading below was taken BY ME, at `1bfb1cd9` unless another
commit is named.

- TWO TESTS ARE RED ON THIS BRANCH AND HAVE BEEN SINCE ROUND 8.
  `tests/ui_contracts/` reads EXIT 1 at `2 failed, 807 passed, 4 skipped`:
  `test_digest_card_copy.py::TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map`
  and
  `test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule`.
- THE CAUSE IS THIS FEATURE'S OWN ROUND 8, and I bisected it rather than
  inferring it. In a disposable worktree at `b5cde726`, the commit round 8
  built on, those two files read EXIT 0 at `52 passed`. In a second worktree at
  `027bdc2c` they read `2 failed, 50 passed`, and they read the same 2 failures
  in the primary checkout now. Round 8 widened `RunState` with `BLOCKED` and
  `STOPPED`; both tests parse the members out of `packages/core/models.py` and
  require each one to appear in a TypeScript module, and neither module was
  given the two new words. Both worktrees were removed by exact path and pruned.
- WHAT IS ACTUALLY BROKEN, read from the two modules.
  `apps/ui/src/api/digestVisibility.ts` partitions the states into
  `NOT_YET_STARTED_STATES = ["pending", "planned"]`, `IN_FLIGHT_STATES =
  ["running"]` and `SETTLED_STATES = ["paused", "completed", "failed",
  "cancelled"]` — seven words, and `blocked` and `stopped` are in none of them,
  so `digestStateClass` returns `"unknown"` for both.
  `apps/ui/src/api/digestCardCopy.ts` has `DIGEST_STATE_LABELS` at line 61 with
  those same seven keys, so `digestStateLabel("blocked")` returns the
  `UNREADABLE_STATE_LABEL`, `"State not recorded"`.
- SO THE COCKPIT MISREPRESENTS EXACTLY THE TWO STATES THIS FEATURE ADDED. A job
  the orchestrator has BLOCKED, or one the operator has STOPPED, reaches the
  hero card as a state it cannot read. That is a product effect and not only a
  red test, which is why it earns an id rather than a prose slip.
- THE TWO MODULES ARE NOT THE SAME KIND OF LIST, and the block must not treat
  them alike. `DIGEST_CTA_RULE_IDS` in the same copy module already carries
  `"stopped-by-operator"` and `"blocked-failed"`; those are RULE IDS from
  `recommended_next_action`, a different vocabulary, and the module's own
  comment at line 58 names that confusion as the trap. Do not reuse them as
  state keys and do not touch that tuple.
- VITEST IS REACHABLE AND IS CURRENTLY GREEN.
  `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
  runs `npx vitest run` over the whole UI suite, and it passed inside my own
  `tests/orchestration/` run. Three vitest files import these modules:
  `digestVisibility.test.ts`, `digestCardCopy.test.ts` and
  `digestEndToEnd.test.ts`. That pytest node is the route this workflow uses to
  reach vitest; no bare `npx` invocation is ordered.
- THE BASE READINGS THIS ROUND GATES AGAINST, each run by me at `1bfb1cd9`:
  `tests/ui_contracts/` EXIT 1 at 2 failed / 807 passed / 4 skipped;
  `tests/orchestration/` EXIT 0 at 12847 passed / 10 skipped; `tests/docs/`
  EXIT 0 at 303; canary EXIT 0 at 42.
- THE APPEND TARGETS, measured at `1bfb1cd9`: `.agent/live_review.md` 1118077
  bytes / 701 units, registrations 304, resolutions 247, open BY DISTINCT ID 57,
  `^Gate: ` 32; `.agent/prose_slips.md` 136942 bytes / 174 units;
  `docs/roadmap/features/T2_F272.md` 30008 bytes / 63 units, headings D1 to D7.
  Each file's terminal byte is exactly one newline.

## What the OPEN SET binds on this block (§3 item 34, last clause)

"BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, same words, in the
Handback section. R-0819's shadow-property clause — DECLINED AS NOT APPLICABLE,
no `run_dir`/`runs_dir` gate here, still owed by T003/T004. R-0820's clause, that
a gate must not be computed from the same predicate as the change set — APPLIED:
G4 below is the repository's own pre-existing tests, which were written against
`packages/core/models.py` and not against anything this block defines.

## The change set

C2: `.agent/live_review.md`, `.agent/prose_slips.md`.
C3: `docs/roadmap/features/T2_F272.md`.
C4: `apps/ui/src/api/digestVisibility.ts`, `apps/ui/src/api/digestCardCopy.ts`.
C5: `.agent/live_review.md`.
C0a/C0b/C1/C6: `.agent/authored/f272-r11.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/handoff.md`.

No `.py` file changes this round. If a vitest file under `apps/ui/src/api/`
must change to keep G5 green, that is INSIDE this change set — report it with
the reason. Nothing else is.

## C4 — the two modules, a SPEC and not a slice

`digestVisibility.ts`: add `"blocked"` and `"stopped"` to `SETTLED_STATES`, per
DECISION F272 D8 below. Update the comments that count the partition — the
block comment above `SETTLED_STATES` calling `paused` "the most report-worthy
rest of the four", and the one above `digestStateClass` saying "The seven
members of `RunState`" — so no sentence states a figure its own body contradicts.
Prefer naming the set to counting it (§3 item 16); where a count must stay, make
it the measured one.

`digestCardCopy.ts`: add two entries to `DIGEST_STATE_LABELS`, `"blocked"` and
`"stopped"`. The labels are OPERATOR-FACING COPY and must survive `scrubUiText`
and §17: a short capitalised phrase in the voice of the seven already there
("Waiting to start", "Paused", "Cancelled"). Use `"Blocked"` and `"Stopped"`
unless the copy audit in `tests/ui_contracts/test_digest_card_copy.py` refuses
them, in which case report what it refused and what you used.

`tests/ui_contracts/` IS NOT IN THIS CHANGE SET AND IS NOT EDITED. It is this
round's gate, and a round does not edit its own gate. Its comments still say
"six of the seven digest states"; that staleness is real and is left standing on
purpose rather than repaired by the round it would be grading. If a test there
cannot pass without being changed, STOP and hand off — that is a finding about
this block, not a licence to edit the gate.

DO NOT touch `DIGEST_CTA_RULE_IDS`, `UNREADABLE_STATE_LABEL`, the CTA rules, or
any `.py` file. The unknown-state fallback stays exactly as it is: it is the
honest answer for a word the client really has never heard of, and this round
removes two words from that category rather than removing the category.

## Constraints

1. NO SLICE IS EDITED — apply the authored texts byte for byte between their
   markers; if one looks wrong, apply it anyway and say so. C4 is a SPEC: write
   that TypeScript yourself.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, nothing reordered; C1 is the
   first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, the slice
   being the marker-delimited lines each with its terminating newline, and the
   post-image ending in exactly one `\n`. PLAN CONVENTION: `.agent/plan.md` is
   REPLACED by exactly the PLANF272R11 slice.
5. Behaviour changes: exactly two states stop being unreadable. No other state,
   label, rule id, threshold or fallback changes.
6. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
   C5 is the ONE exception the rules make: a single `Landed:` line, worded
   below, and nothing else.
7. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never the primary checkout (protocol G5); remove
   and prune it before the handback, BY EXACT PATH and never by glob. A fresh
   worktree has no `apps/ui/node_modules`, so any vitest run inside one needs
   that directory restored with `shutil.copytree(..., symlinks=True)` — the
   argument, not the default, per R-0591.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before
   C6, and table all three; if it appears, finish only the half-written commit,
   then hand off (protocol G6).
9. `python3 -B` for every run; report each gate's REAL exit code, "green" as a
   word being a finding.

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r11.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2 and C5.** Readers (a) to (d) over `.agent/live_review.md`
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
(d) COUNTS before → after C2: `^- R-\d{4} — ` distinct ids 304 → 305; `^Done:
R-\d{4} — ` distinct 247 → 247; open set BY DISTINCT ID 57 → 58; `^Gate: ` 32 →
33; `^Gate: F272 R10 ` 0 → 1; `^- R-0821 — ` 0 → 1. Then AFTER C5, report
`^Landed: R-0821 ` 0 → 1 and confirm `^Done: R-0821 ` is still 0.

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3.** The plan: `.agent/plan.md`
equals the PLANF272R11 slice bytes exactly; report the equality, both byte
lengths, the line count against the AGENTS.md cap of 50, and that `## Goal` and
`## Next Steps` are present. The feature file: readers (a) and (b) of G2's
wording, no negative control (gate budget); plus the count YOU measure of
`^### DECISION F272 D\d+ ` lines and the D-number each names, in order.

**G4 THE TWO RED TESTS GO GREEN, AND THE GATE CAN STILL FAIL, at C4.**
(i) `python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly` EXIT 0. Base at
`1bfb1cd9` is EXIT 1 at 2 failed / 807 passed / 4 skipped, so report the new
counts against those three numbers; passed must rise by exactly 2 and skipped
must stay 4.
(ii) THE RED CONTROL, in a disposable worktree at the commit C4 creates: remove
the single `"blocked"` entry from `SETTLED_STATES` in `digestVisibility.ts` —
count that exact byte string in that file first, where it must be 1 (§3 item 25)
— and require `test_job_digest_card_contract.py` to go EXIT 1 naming `blocked`.
Restore, confirm the file is byte-identical, and re-run to EXIT 0. A gate that
cannot fail is not a gate.
(iii) THE READING THE TESTS DO NOT MAKE: in that same worktree, print the value
`digestStateLabel` returns for `"blocked"` and for `"stopped"` by parsing
`DIGEST_STATE_LABELS` out of the module, and confirm neither is
`UNREADABLE_STATE_LABEL`. The suite proves the keys EXIST; this proves what a
reader of the card actually sees.

**G5 VITEST, at C4, through this repository's own pytest route.**
`python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly`
EXIT 0, in the PRIMARY CHECKOUT, which is the only tree carrying
`apps/ui/node_modules`. Report the summary line. This node runs `npx vitest run`
over the whole UI suite, so it is the gate on all three `.test.ts` files that
import the modules C4 edits. If it goes red, report the failing vitest specs
verbatim before changing anything, and fix only files inside the change set.

**G6 THE SUITES, run SERIALLY, each its own invocation.** `tests/docs/` and the
canary `tests/cli/test_golden_path.py`. Both EXIT 0; report each exit code and
summary line. Base at `1bfb1cd9`: 303 and 42. `tests/orchestration/` and
`tests/cli/` are NOT ordered in full: no `.py` file changes this round, and G5
already runs the one orchestration node this change can reach. State that
reasoning in the handback rather than reporting a suite you did not run.

**G7 LINT AND INTEGRITY, at C4.** No `.py` file changes, so `ruff` has an EMPTY
ordered file set — say so plainly rather than reporting a pass. `npm run lint`
is NEVER ordered in this repository. `python3 -m apps.cli.grouped integrity
check --json`: EXIT 0, `"passed": true`, `"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C6 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming every worktree you
created and confirming its removal by exact path. Per commit C0a through C5 —
NOT C6, which cannot count its own insertions (§3 item 14) — the insertion count
from `git diff --numstat <parent> <commit>`, each single-parent and under the
F104 D1 cap of 500; those same numbers fill the handback's `## Commits` `+/-`
column, so report both readings side by side and confirm each row cell by cell
(§3 item 28). Marker sweep: the number YOU measure of `<<<BEGIN `/`<<<END `
lines in every written non-block file, zero in each. The three `.agent/STOP`
readings as a table.

## The slices

<<<BEGIN PLANF272R11>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 10 PASSED;
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

Repair R-0821, the two cockpit modules round 8's `RunState` widening never
reached. `blocked` and `stopped` are in no partition of `digestVisibility.ts`
and have no key in `digestCardCopy.ts`, so the hero card calls both "State not
recorded" and two `tests/ui_contracts/` tests have been red on this branch since
round 8. This round gives them their place and rules it as DECISION F272 D8.

## Next Steps

1. Move three of the `state` collapse: retype `JobPlan.state` to `RunState` and
   make the six `JOB_*` constants `RunState` members, with `.value` at every
   boundary leaving the record. The rendering guard round 10 shipped in
   `tests/orchestration/test_job_state_field.py` is what that move must keep
   green, and D7's probe is the method for finding its site set.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A `RunState` member added without a matching cockpit entry is invisible to
  every gate this feature has run so far; `tests/ui_contracts/` is the suite
  that sees it and it belongs in the gate list of any round touching the enum.
<<<END PLANF272R11>>>

<<<BEGIN RECORDR11>>>
Gate: F272 R10 — the F272 round 10 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `027bdc2c`..`1bfb1cd9`, nine commits, every one single-parent, in exactly the bundle's ordered sequence C0a through C7 with nothing added, dropped or reordered. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r10-block.md` was written and hashed BEFORE delegation, and it, the committed `.agent/authored/f272-r10.md` and the committed `.agent/last_block.md` are all 32692 bytes at 400 lines and all hash to `e0aea48b27d07b255fa7c18c7ad1abbbd5bfa4893ac04dafd14d7daaad8d2a13`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte under the reviewer's own readers: 1109691 to 1118077, pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, reader (b) accepting with N counted at 2 from the slice's own paragraphs and units 699 to 701; registrations 303 to 304, resolutions 247 unchanged, open set BY DISTINCT ID 56 to 57, `^Gate: ` 31 to 32, `^Gate: F272 R9 ` 0 to 1 and `^- R-0820 — ` 0 to 1 — every count exactly as ordered. G3 THE PLAN is 2173 bytes byte-equal to its slice at 43 lines against the cap of 50, and THE FEATURE FILE appended 27130 to 30008 with reader (b) accepting at N counted 6 and units 57 to 63, its headings reading D1 through D7 in order. G4 THE RENAME, re-measured by the reviewer by importing the SHIPPED `/home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py`: `state` is in `__dataclass_fields__` and `status` is NOT; `_export_job` on a blocked job emits key `"status"` valued `'blocked'` and NO `"state"` key; `_import_job({'job_id':…,'status':'blocked'})` returns `state == 'blocked'`; the JSON round trip preserves it; `type(...)` is `str`, `isinstance(..., RunState)` is FALSE, and the f-string renders the plain word `blocked` — so the stored key did not move, old records still load, and nothing was retyped. THE PRODUCTION DIFF IS A CORRECT RENAME AND ITS DISCRIMINATION IS EXACT WHERE IT IS HARDEST: `task.status` and `t.status` are untouched throughout `pingpong_job.py`, `job.worktree_cleanup_status` is untouched, `core_job.state.value` in the adapter is untouched, and in `test_pingpong_integration.py` the stand-in `FakeJob.status` moved while `FakeTask.status` and `FakePromo.status` beside it did not. THE TWO SITES ROUND 9 PROVED UNREACHABLE ARE BOTH FIXED: `packages/orchestration/self_use_findings.py:51`, production code no static name rule could see, and `_CoreJobAdapter` in `apps/cli/commands/job_stop_cmd.py`, whose `__slots__` entry and assignment moved together with all six of its consumers while the external JSON key `"job_status"` was preserved. G6 THE SUITES, re-run serially by the reviewer: `tests/orchestration/` EXIT 0 at 12847 passed and 10 skipped in 721.47s — a rise of EXACTLY 9 over the reviewer's own `027bdc2c` reading of 12838, which is the 9 tests C6 adds and nothing else, with skips unchanged at 10 — `tests/cli/` EXIT 0 at 1537 passed in 305.58s exactly matching base, `tests/docs/` EXIT 0 at 303, the canary EXIT 0 at 42, and the new `tests/orchestration/test_job_state_field.py` EXIT 0 at 9 passed. G7's ruff EXIT 1 IS UPHELD AS PRE-EXISTING AND CORRECTLY NOT FIXED: the single `I001` in `tests/orchestration/test_predictive_budget.py` reproduces identically when the reviewer lints the `027bdc2c` blob through `ruff check --stdin-filename`, which is R-0594's non-writing route, so the diagnostic predates this round and repairing it would have been a change outside the change set. G8 THE TREE: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, thirteen worktree entries being the primary and the twelve pre-existing `remedy/job-*`, and the marker sweep 0 in all five written non-block files. THE INVENTORY IS GENUINE CONVERGENCE EVIDENCE, not a prediction: `.agent/f272_state_rename_inventory.md` tables seven probe runs with their real exit codes INCLUDING the failed intermediate states — the raising run that logged 40 sites, the run whose empty log beside 14 failures in `test_final_audit_evidence.py` is what an unfound STAND-IN looks like, and the final raising run at EXIT 0 with an EMPTY site log — and its 14375 convergence reading plus C6's 9 tests reconciles exactly with the 14384 of G4. THE WORKER'S ELEVEN DEVIATIONS ARE ACCEPTED. Three are judgement calls that improved the round: the forwarding probe mode, declared as an accelerator with every claim resting on the raising run; instrumenting `__init__`, without which a property cannot see `JobPlan(status=…)`; and probing the REST of `tests/` beyond the two ordered suites, which is the only reason `tests/test_do_job_flow.py` — outside every suite this block's gates order — was found at all, and which the reviewer confirms EXIT 0 at 178 passed. Deviation 6 is UPHELD AND IS THE REVIEWER'S SLIP, NOT THE WORKER'S: G4(i) ordered the residual site log EMPTY, and the one entry it holds is C6's own `assert not hasattr(JobPlan(), "status")` reading the gate's own instrument — an assertion stronger than the block specified and worth keeping, so the gate was over-strict by exactly the improvement it provoked. Deviation 8 is upheld as reported and is registered beside this entry as R-0821; the worker minted no id for it, which constraint 6 required and which was right.

- R-0821 — Medium, ROUND 8 WIDENED `RunState` WITHOUT GIVING THE TWO NEW MEMBERS A PLACE IN THE COCKPIT, SO THE HERO CARD CANNOT NAME OR CLASSIFY A BLOCKED OR STOPPED JOB AND TWO TESTS HAVE BEEN RED ON THIS BRANCH FOR THREE ROUNDS. Raised by the reviewer while gating round 10; the round 10 worker independently reported the two failures as red at base and correctly minted no id. MEASURED BY THE REVIEWER BY BISECTION, not inferred: in a disposable worktree at `b5cde726`, the commit round 8 built on, `tests/ui_contracts/test_digest_card_copy.py` and `test_job_digest_card_contract.py` read EXIT 0 at 52 passed; in a second worktree at `027bdc2c` the same two files read 2 failed and 50 passed; and `tests/ui_contracts/` in the primary checkout at `1bfb1cd9` reads EXIT 1 at 2 failed, 807 passed and 4 skipped. Both worktrees were removed by exact path and pruned. THE FAILING TESTS ARE `TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map` and `TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule`; each parses the `RunState` members out of `packages/core/models.py` with `ast` and asserts that every member value appears in a named TypeScript module, so both went red the moment round 8 added `BLOCKED` and `STOPPED` to that enum. THE PRODUCT EFFECT, read from the two modules at `1bfb1cd9` and not from the test names: `apps/ui/src/api/digestVisibility.ts` partitions states into `NOT_YET_STARTED_STATES = ["pending", "planned"]`, `IN_FLIGHT_STATES = ["running"]` and `SETTLED_STATES = ["paused", "completed", "failed", "cancelled"]`, so `digestStateClass` answers `"unknown"` for `blocked` and for `stopped`; and `DIGEST_STATE_LABELS` at `apps/ui/src/api/digestCardCopy.ts:61` carries those same seven keys, so `digestStateLabel` answers `UNREADABLE_STATE_LABEL`, the string `"State not recorded"`. A job the orchestrator BLOCKED and a job the operator STOPPED are therefore shown to the operator as a state the cockpit cannot read — the two states this feature exists to make first-class. That is wrong state on disk under `apps/` and `tests/`, which is what operator amendment amend0827-process-diet rule 2 spends an id on. WHY NO ROUND SAW IT: the gate lists of rounds 8, 9 and 10 name `tests/orchestration/`, `tests/docs/`, `tests/cli/` and the canary, and `tests/ui_contracts/` is in none of them, so the suite that watches the Python-to-TypeScript seam was never reachable by any gate while the enum it watches was being widened. The reviewer wrote all three of those gate lists. Searched before minting per §3 item 30 by grepping `.agent/live_review.md` for `digestVisibility`, `digestCardCopy`, `RunState`, `ui_contracts` and `run_state_values`; R-0661 is the nearest neighbour and does not cover this — it is about undefined CSS custom properties in a stylesheet, a different file class, a different seam and a different mechanism — and no open finding describes the enum-to-cockpit gap. FIX, LANDED BY THIS ROUND: `blocked` and `stopped` join `SETTLED_STATES` and gain `DIGEST_STATE_LABELS` entries, ruled as DECISION F272 D8. THE COUNTER-MEASURE, BINDING ON EVERY LATER BLOCK OF THIS FEATURE THAT CHANGES `RunState`, THE `JOB_*` CONSTANTS OR ANY STATE VOCABULARY — move three of the `state` collapse is exactly such a round, so this is owed rather than historical: the block's gate list NAMES `tests/ui_contracts/` alongside the Python suites, because that is the only suite in this repository that reads the enum against the cockpit, and a vocabulary change with no gate on that seam is a change nothing can see. OPEN.
<<<END RECORDR11>>>

<<<BEGIN SLIPSR11>>>
2026-09-07 · F272 R10 block, gate G4(i) (reviewer) · G4(i) ordered the residual probe's site log to be EMPTY, while C6 item 1 of the same block ordered a test asserting that `status` is no longer a field. The worker wrote that assertion in its strongest form, `assert not hasattr(JobPlan(), "status")`, which under the residual probe READS the raising property the gate installs and so logs one site — making the ordered emptiness unreachable by exactly the improvement the block asked for. This is §3 item 2's self-counting-gate family reaching a SPEC rather than a slice: item 2 forbids a must-be-0 gate over a string a TO slice writes into the same file, and says nothing about a must-be-empty gate over a log that the block's own ordered TEST causes an entry in. A residual-instrument gate excludes the test that asserts the instrument's absence, or scopes the emptiness to sites outside the pin file. The worker declared it rather than deleting the assertion, which was the right call and is why nothing on disk is wrong.

2026-09-07 · F272 R10 block, gate G7 (reviewer) · G7 ordered `ruff check` EXIT 0 over exactly the `.py` files the round changed, and one of those files, `tests/orchestration/test_predictive_budget.py`, already carried an `I001` at the round's own base. The gate was therefore unmeetable without an edit outside the change set. It could not have been pre-run at base in the usual way either, because DECISION F272 D7 makes the change set a MEASURED quantity that does not exist at authoring time — which is the general lesson: when a block's file set is determined by the round's own measurement, a lint gate over "the files this round changed" is worded as EXIT 0 OR every diagnostic proven pre-existing by linting the base blob through `ruff check --stdin-filename`, the non-writing route R-0594 requires. The worker took exactly that route unprompted and proved the diagnostic pre-existing.

2026-09-07 · F272 R10 handoff, Session line (reviewer) · The round 10 delegation told the worker `SESSION 4 of feature F272`, and the worker wrote that faithfully into `.agent/handoff.md`. It is wrong by one: round 9's session ended with its own handoff, and round 10 ran in a new session, so round 10 was SESSION 5. The reviewer carried the number forward from the previous handoff instead of incrementing it at the Phase 0 probe. Nothing on disk depends on it — `.agent/handoff.md` is rewritten every round and F272's soft limit of 12 sessions and 40 rounds is far away either way — but the session count exists to make that limit auditable, so the round 11 handoff states SESSION 6 and this line is the correction of record for round 10.
<<<END SLIPSR11>>>

<<<BEGIN DECISIONR11>>>
### DECISION F272 D8 (2026-09-07, F272 round 11) — `blocked` and `stopped` are SETTLED states in the cockpit, and a state vocabulary change is not finished until the cockpit can name it

CONTEXT. Round 8 widened `RunState` with `BLOCKED` and `STOPPED` so the job
lifecycle field could be retyped onto it. Neither word was given a place in
`apps/ui/src/api/digestVisibility.ts` or `apps/ui/src/api/digestCardCopy.ts`, so
`digestStateClass` answers `"unknown"` for both and `digestStateLabel` answers
`"State not recorded"`. Two `tests/ui_contracts/` tests went red at that moment
and stayed red through rounds 8, 9 and 10, because no round's gate list named
that suite. Finding R-0821 carries the bisection and the readings.

CHOSEN. BOTH JOIN `SETTLED_STATES`, and both gain a plain label. A blocked job
and a stopped job have COME TO REST AND HAVE SOMETHING TO REPORT, which is the
property that tuple names and the reason `paused` already sits there rather than
with `running`. Neither is in flight: a blocked job is not working and a stopped
job has been halted at a safe point by the operator. Neither is
not-yet-started: both have run. The card should therefore show them on settled
grounds, which is precisely when an operator most needs to see them.

WHY NOT A FOURTH CLASS. A `needs-attention` partition beside the three would be
the more expressive model and is rejected here: `digestStateClass` feeds a
three-way rule with an honest fourth answer for the unreadable, every consumer
of it is written against those four, and widening the partition is a cockpit
design change that F272 has no mandate for. The states are settled; whether the
card should shout about some settled states more than others is a question for
whoever owns the hero card's priority rule, and it is not answered by putting a
state in the wrong bucket.

NOT CHANGED BY THIS RULING: `UNREADABLE_STATE_LABEL` and the unknown class stay
exactly as they are — they are the honest answer for a word the client really
has never heard of, and this ruling removes two words from that category rather
than removing the category. `DIGEST_CTA_RULE_IDS` is untouched: its
`stopped-by-operator` and `blocked-failed` entries are RULE ids from
`recommended_next_action`, a different vocabulary that the copy module's own
comment already names as a trap for exactly this confusion.

THE GENERAL RULE THIS SETTLES, which is the half worth more than the two entries:
a change to a state vocabulary is not finished when the Python suite is green.
`tests/ui_contracts/` is the only suite that reads `RunState` against the
cockpit, so any round changing that enum, the `JOB_*` constants or any state
spelling names that suite in its gate list. Move three of the `state` collapse
is the next such round.

REVERSE by removing the two entries from each module; the two tests go red again
and the cockpit returns to calling both states unreadable.
<<<END DECISIONR11>>>

## C5 — the Landed line, a SPEC and not a slice

APPEND to `.agent/live_review.md`, as its own commit AFTER C4, exactly one line
of the form the rules fix — `Landed: R-0821 — ` followed by one sentence naming
what changed and the commit C4 created. Nothing else, no `Done:` paragraph, no
second line. The reviewer replaces it with the authored resolution at the next
gate; a surviving `Landed:` line is an unreviewed fix, which is what it should
look like.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 6 of feature F272 · round 11` — the round 10 handoff says SESSION 4 and
is wrong by one for the reason the third prose slip records; this round's number
is 6 and is stated here so the count is auditable again. Then the one-sentence
context self-assessment amend0905-throughput requires, branch, the range, a
per-commit changed-files table with real `+/-`, the item-status table covering
C0a through C6 with every item present exactly once, one line per gate G1 to G8
with its real exit code, the G4 red-control readings, the authored-text proof
table, deviations and the next expected action. No length cap. Per the fix clause
OPEN in the record and binding on the next block that orders a handback: any
commit beyond the ordered sequence receives its OWN `## Commits` row and its OWN
item-status row, and the Deviations section says so in those same words rather
than beside a clause that denies it.
