── STEP R23 / F105 — gate R22, close the unsatisfiable-red-proof gap ────────
Goal:        Put the R22 gate on disk; register R-0251 and R-0252 and fix both
             in the same round; leave migration-order step 6 to a fresh
             session with the ground already proved.
Bundle:      C1a save block · C1b mirror · C2 live_review (next free ID, the two
             findings, the R22 gate) · C3 the process fix — §3 checklist item 5
             + DECISION F105 D10 · C4 R-0251's pin · C5 plan.md + handoff.md
Change:      exactly these paths, nothing else —
             `.agent/authored/f105-r23-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`, `docs/agents/planner_reviewer_prompt.md`,
             `tests/orchestration/test_builder_prompt_golden.py`.
Constraints: No production file changes. Do NOT touch
             `packages/orchestration/pingpong_loop.py` — R-0251's fix is a test
             that pins existing behaviour, never an edit to the behaviour. Do
             not touch `_build_reviewer_prompt` (that is step 6). Do not edit
             AGENTS.md or `docs/roadmap/ROADMAP.md`. This round's change set
             includes `docs/`, so the docs-round gate applies (Done when D).
Handback:    completion report + rewrite `.agent/handoff.md`. This is the
             SESSION TERMINATOR: its own gate is owed to the next session's
             reviewer, per docs/agents/planner_reviewer_prompt.md §4.13. Say so
             in the handoff and do NOT open a repair round to close it.
──────────────────────────────────────────────────────────────────────────────

## Commit order

### C1a — save the block, ALONE
Save this block verbatim to `.agent/authored/f105-r23-1.md`, nothing else.
    git commit -m "chore(f105): save the R23 block verbatim"

### C1b — mirror to last_block
`cp .agent/authored/f105-r23-1.md .agent/last_block.md`, commit alone.
    git commit -m "chore(f105): mirror the R23 block to last_block"

### C2 — live_review: findings persist FIRST
Apply PAIR_A, PAIR_B, PAIR_C to `.agent/live_review.md`. One commit.
    git commit -m "chore(f105): record the R22 gate and register R-0251 and R-0252"

### C3 — the process fix for R-0252
Apply PAIR_D to `docs/agents/planner_reviewer_prompt.md` and PAIR_E to
`.agent/decisions.md`. One commit — the rule and the DECISION that installs it
belong together.
    git commit -m "chore(f105): extend the pre-emission checklist to red-proofs"

### C4 — the pin for R-0251
Add the pin described under "C4 spec" to
`tests/orchestration/test_builder_prompt_golden.py`. One commit.
    git commit -m "test(f105): pin the segment-boundary fallback branch"

### C5 — plan and handoff
Apply PAIR_F to `.agent/plan.md` (full replacement). Rewrite `.agent/handoff.md`.
    git commit -m "chore(f105): update the plan and close the session with R23"

Then `git push -u origin feature/f105-cache-optimal-prompt-ordering`.

## C4 spec — pin the fallback branch (R-0251)

`_drop_one_newline_per_segment_boundary` in
`packages/orchestration/pingpong_loop.py` has three branches. Two are exercised
by every existing test; the third — "else if the NEXT segment's text starts with
a newline, drop that leading newline instead" — is UNREACHABLE for today's ten
segments, so it ships unproven. The reviewer confirmed this directly: replacing
that branch's body with a `raise` leaves 433 tests green across the golden, the
three pingpong suites, `test_scope_plan.py` and `test_task_input.py`.

The fix is a pin, NOT a deletion. The branch handles a legal case that no
segment happens to produce today; deleting it would turn a future segment whose
text opens with a newline from "composes correctly" into "raises". Import the
helper directly and call it with synthetic lists — it takes a plain
`list[str]` and returns one, so no prompt fixture is needed:

1. The trailing branch: `["a\n", "b"]` -> `["a", "b"]`.
2. The fallback branch, the one nothing reached: `["a", "\nb"]` -> `["a", "b"]`.
   Assert on BOTH elements — that the first is untouched is half the property.
3. The illegal boundary: `["a", "b"]` raises `PromptSegmentError`, with
   `pytest.raises` matching on the message.
4. A three-segment list mixing branches 1 and 2 at its two boundaries, to pin
   that the choice is made per boundary and not once for the whole list.
5. The last element is never trimmed: `["a\n", "b\n"]` -> `["a", "b\n"]`.

Put them in one class in `tests/orchestration/test_builder_prompt_golden.py`
with a docstring naming R-0251 and saying in one line WHY a directly-called
helper needs its own test: the composed prompts cannot reach the branch, so no
prompt-level golden can ever cover it.

## Done when (run every command; record REAL exit codes and real output)

A. `sha256sum .agent/authored/f105-r23-1.md .agent/last_block.md` equal;
   `cmp` on the pair exits 0.
B. `wc -l .agent/authored/f105-r23-1.md` — report the number.
C. Application, per target file:
   `grep -c '^- R-0251 ' .agent/live_review.md` -> 1
   `grep -c '^- R-0252 ' .agent/live_review.md` -> 1
   `grep -c '^- Reviewer gate on R22 ' .agent/live_review.md` -> 1
   `sed -n '8p' .agent/live_review.md` -> ends `Next free ID: R-0253.`
   `grep -c '^## DECISION F105 D10 ' .agent/decisions.md` -> 1
   `grep -c 'Reachable red-proofs only' docs/agents/planner_reviewer_prompt.md` -> 1
   `grep -c '^===BEGIN\|^===END' .agent/live_review.md .agent/decisions.md .agent/plan.md docs/agents/planner_reviewer_prompt.md` -> 0 for all four
   `wc -l .agent/plan.md` -> must be < 50. Report the number.
D. Docs-round gate (this round touches `docs/`):
   `python3 -m pytest tests/docs/ -q` (baseline 294)
   `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` (baseline 70)
E. Round gate + canary:
   `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`
   (baseline 16; report the new number)
   `python3 -m pytest tests/cli/test_golden_path.py -q` (baseline 42)
F. Red-proof, in a DISPOSABLE `git worktree` at HEAD, never the primary
   checkout. ONE mutation, reverted afterwards: in
   `_drop_one_newline_per_segment_boundary`, delete the `elif` fallback branch
   so its case falls through to the `raise`. The C4 pin's fallback-branch test
   and its mixed-boundary test MUST go RED; report which tests failed and their
   real message. This mutation IS reachable by construction — the pin calls the
   helper directly with a list the composed prompts cannot produce, which is
   the whole point of R-0251's fix. Then `git worktree remove`,
   `git worktree prune`, and show `git worktree list` as the primary alone.
G. `git status --porcelain` empty after C5; `git log --numstat b35d9d56..HEAD` —
   report the `+` column per commit, each under 500.

## PAIR shapes, declared at authoring time

| Pair | Target | Shape |
|---|---|---|
| A | live_review | REWRITE — the TO changes the ID on the same line |
| B | live_review | APPEND — TO contains FROM verbatim as its prefix |
| C | live_review | APPEND — TO contains FROM verbatim as its prefix |
| D | planner_reviewer_prompt | APPEND — TO contains FROM verbatim as its prefix |
| E | decisions | APPEND — TO contains FROM verbatim as its prefix |
| F | plan | full replacement, byte-for-byte equal to the slice |

REWRITE proof: FROM 0x after, TO 1x after. APPEND proof: FROM exactly 1x after,
each TO-ONLY line at least 1x. Every state/docs commit also reports its stray
count — added lines tracing to no authored TO slice — which must be 0.

===BEGIN PAIR_A_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0251.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0253.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
  checklist in that file's §3, installed as DECISION F105 D8 in the same round
  as this entry, so the next reviewer runs the checks off disk instead of
  remembering them. Fixed and resolved in this same round; the NEXT session's
  gate verifies the rule is on disk and reads as intended.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
  checklist in that file's §3, installed as DECISION F105 D8 in the same round
  as this entry, so the next reviewer runs the checks off disk instead of
  remembering them. Fixed and resolved in this same round; the NEXT session's
  gate verifies the rule is on disk and reads as intended.
- R-0251 (Low, F105 R22): the fallback branch of
  `_drop_one_newline_per_segment_boundary` in
  `packages/orchestration/pingpong_loop.py` ships unproven. The helper has three
  branches; composition reaches two of them. The third — drop the NEXT segment's
  leading newline when the earlier one has no trailing newline to give — is
  unreachable for today's ten segments, because every non-last segment's raw
  text already ends with a newline. Proven by the reviewer at b35d9d56 in a
  disposable worktree: replacing that branch's body with a `raise` leaves 433
  tests green across the golden, the three pingpong suites, `test_scope_plan.py`
  and `test_task_input.py`. The worker declared exactly this as R22 deviation 1
  rather than reporting the ordered mutation as red, which is the behaviour the
  gate exists to reward. Fix: pin the helper directly with synthetic lists — not
  delete the branch, which handles a legal case a future segment may produce.
  Done: R-0251 — RESOLVED at R23. The helper now carries its own test class,
  called directly with lists the composed prompts cannot produce: the trailing
  branch, the fallback branch, the illegal boundary's `PromptSegmentError`, a
  mixed three-segment list, and the untouched last element. Re-proved by the
  reviewer's own red-proof at gate F, where deleting the `elif` turns the
  fallback and mixed-boundary tests RED where before the pin it turned nothing.
- R-0252 (Medium, F105 R22, reviewer-authored defect): DECISION F105 D8's
  pre-emission checklist does not cover the red-proofs a block ORDERS. R22's
  gate F ordered a mutation — delete the fallback branch, expect red — against
  a branch no test can reach, so the gate was unsatisfiable exactly as R-0250's
  four were. That is the SIXTH instance of the class across F104 and F105, and
  the first the freshly installed checklist did not catch: its four items read
  the block's own bytes, and reachability is a property of the CODE the block
  points at. The cost is the same as every earlier instance — a round spends a
  declared deviation proving a reviewer mistake. Fix: a fifth checklist item in
  docs/agents/planner_reviewer_prompt.md §3, installed as DECISION F105 D10 in
  the same round as this entry. Fixed and resolved in this same round; the NEXT
  session's gate verifies the rule is on disk and reads as intended.
===END PAIR_B_TO===

===BEGIN PAIR_C_FROM===
  R-0250's own resolution asked the next gate to verify the rule reached disk
  and reads as intended. It did: docs/agents/planner_reviewer_prompt.md §3 now
  carries the four-item pre-emission checklist, and this round's block was
  written against it — item 1 caught the size before emission and item 2 was run
  against every zero-gate in Done-when C.
  `LAST_REVIEWED_SHA` advances 9cb128d7 -> 54049e6b.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
  R-0250's own resolution asked the next gate to verify the rule reached disk
  and reads as intended. It did: docs/agents/planner_reviewer_prompt.md §3 now
  carries the four-item pre-emission checklist, and this round's block was
  written against it — item 1 caught the size before emission and item 2 was run
  against every zero-gate in Done-when C.
  `LAST_REVIEWED_SHA` advances 9cb128d7 -> 54049e6b.
- Reviewer gate on R22 (2026-08-10, same session): PASS. Range
  `54049e6b..HEAD` at b35d9d56, SIX commits, NINE path rows over eight paths,
  exactly the block's declared change set. Insertions per `git log --numstat`:
  376, 306, 32, 102, 392, 71 — each under 500.
  Transport was proved disk to disk, not by retype: the reviewer's authored
  original and the committed `.agent/authored/f105-r22-1.md` are byte-identical
  under `cmp`, and all three of original, authored copy and `.agent/last_block.md`
  hash to `8f5fc0c8bf8bdb67…`.
  The production claim was checked WITHOUT using the worker's numbers. Before
  the block was authored the reviewer had already proved the decomposition
  reproduces the pre-migration render BYTE FOR BYTE in pre-migration order over
  all 64 combinations of the six optional arguments, so the round was ordered
  against a spec known to be satisfiable — the R-0250 discipline applied
  forward for the first time. After the round the golden was re-read and re-run:
  16 tests, four fixture shapes, and the four frozen renders are `repr()` of the
  real 54049e6b output rather than retyped prompt text. `compose_prompt_segments`
  sorts by `(rank, registration index)`, and the worker registers in rank order,
  so the manifest's ten names and the ranks `(0,2,3,3,3,3,4,4,5,5)` are pinned
  exactly, not merely as a monotonic sequence.
  Gates re-run by the reviewer with real exit codes: golden plus segments
  41 passed — 16 + 25, where 25 is the pre-round 22 plus D9's three pins; the
  five caller suites 417 passed, unchanged from the pre-round baseline, so the
  migration added no test to them and removed none; canary 42 passed.
  TWO mutation red-proofs of the REVIEWER's own choosing, distinct from the
  worker's, ran in a disposable worktree at HEAD. M3 dropped the bare `"\n"`
  from `builder_context`'s parts: all 16 golden tests went RED, so the golden
  really does pin bytes and not only shape. M4b changed `builder_staged_diff`'s
  rank from JOB_CONTEXT to DOSSIER, which leaves every segment's TEXT identical
  and the ranks still non-decreasing: exactly one test failed,
  `test_the_full_shape_registers_the_ten_segments_in_rank_order`, so the golden
  pins the rank ASSIGNMENT and not just its monotonicity. Both reverted, the
  worktree removed and pruned, `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  Application was re-measured rather than accepted: pairs A and B APPEND with
  FROM 1x and TO 1x, PAIR_C's slice and `.agent/plan.md` byte-identical at
  sha256 `45b21911…`, `.agent/plan.md` 45 lines against the cap of 50, zero
  BEGIN/END markers in all three targets, and stray added lines recomputed from
  the authored TO slices against the real diffs: 32 added and 0 stray at C2, 42
  added and 0 stray at C3.
  Both declared deviations ACCEPTED, and deviation 1 is charged to the
  reviewer, not the worker: gate F's M2 ordered a mutation against an
  unreachable branch. It is registered as R-0251 and R-0252 rather than held
  against R22. Deviation 2 is the round working as intended — gate H asked for a
  measured number, the number contradicted the block's guess, and the worker
  reported the measurement instead of the guess.
  `LAST_REVIEWED_SHA` advances 54049e6b -> b35d9d56.
===END PAIR_C_TO===

===BEGIN PAIR_D_FROM===
  Why this is on disk and not a habit: item 2 has recurred five times across
  F104 and F105, and R20 hit all four items in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
  5. **Reachable red-proofs only.** A block may order a mutation red-proof only
     when the mutated branch is REACHABLE by the tests that are supposed to go
     red. Items 1-4 read the block's own bytes; this one reads the code the
     block points at, which is why it is a separate check and not a sub-point.
     When reachability is not obvious, order the PROBE instead of the colour:
     "replace the branch body with a raise and report whether any test fails".
     A worker who reports an ordered mutation as green is telling the truth
     about dead code, and it costs that round a declared deviation to prove a
     reviewer mistake (finding R-0252, DECISION F105 D10).
  Why this is on disk and not a habit: item 2 has recurred five times across
  F104 and F105, and R20 hit all four items in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
===END PAIR_D_TO===

===BEGIN PAIR_E_FROM===
Reverse this decision by deleting this entry; the pin test in
`tests/orchestration/test_prompt_segments.py` stays useful either way.
===END PAIR_E_FROM===

===BEGIN PAIR_E_TO===
Reverse this decision by deleting this entry; the pin test in
`tests/orchestration/test_prompt_segments.py` stays useful either way.

## DECISION F105 D10 — red-proofs are ordered only where they can go red (2026-08-10)

Context: finding R-0252. R22's gate F ordered a mutation red-proof against a
branch of `_drop_one_newline_per_segment_boundary` that no composed prompt can
reach, so the mutation could only ever come back green. The worker ran it,
reported green, probed the branch over all 64 optional-argument combinations to
show WHY, and declared it. Nothing was damaged; a round again spent a declared
deviation proving a reviewer mistake, and this is the sixth instance of the
unsatisfiable-gate class across F104 and F105.

What makes it worth its own decision rather than a note under D8 is that D8's
four items cannot catch it. They are checks on the block's own bytes — count
the lines, check a zero-gate against the block's own TO slices, count a
replacement against its file's cap, test whether a TO contains its FROM. All
four are answerable by reading the block alone. Reachability is a property of
the CODE the block points at, so it is a different kind of check and belongs as
its own item.

D10 — §3's checklist gains a fifth item: order a mutation red-proof only where
the mutated branch is reachable by the tests meant to go red, and when that is
not obvious, order the PROBE ("replace the branch with a raise, report whether
anything fails") rather than asserting the colour. The probe is strictly more
informative than a guess: it returns the same evidence whether the branch is
live or dead, and it cannot produce a gate the worker has to declare its way
out of.

The alternative — drop the red-proof when reachability is uncertain — was
rejected. Red-proofs are the only thing separating a test that pins behaviour
from a test that merely runs, and F105's own R-0229 was found exactly this way.
Fewer red-proofs is the wrong direction; better-aimed ones is the right one.

Scope: reviewer-authored blocks, as with D8. It adds no obligation to workers
and changes no verification tier.

Reverse this decision by deleting this entry and §3 checklist item 5.
===END PAIR_E_TO===

===BEGIN PAIR_F===
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). Migration-order steps 1-5 are COMPLETE and GATED, each with its own
golden; `LAST_REVIEWED_SHA` is b35d9d56. R23 is the session terminator: it
records the R22 gate, registers and fixes R-0251 and R-0252, and starts no
migration. Open findings: R-0221, R-0239, R-0246, R-0247. No PR; one is
created at CLOSURE.

## Next Steps
- R24 gates R23 (state, docs and one test file — a red-proof IS owed, on the
  new pin), then takes migration-order step 6,
  `pingpong_loop.py::_build_reviewer_prompt`, last of the six.
- Step 6 gets a FRESH session on purpose. Before authoring its block, prove the
  decomposition byte-exact in pre-migration order over every combination of its
  optional arguments, as R22 did for step 5 — that proof is what made step 5
  land without a repair round. Its two mutually exclusive branches and its
  three reviewer-role strings (base, effective, parse-retry) all reach
  evidence.
- ONE later round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The builder prompt's cacheable prefix now dies 24 characters into
  `builder_staged_state` (R22 gate H measured 467). T004's before/after number
  should quote that, not the rank order alone.
===END PAIR_F===
