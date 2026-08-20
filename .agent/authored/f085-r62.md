── STEP record round — F085 — R62 ────────────────────────────────────────────

Goal: record the R61 PASS and leave the branch on a clean edge for the last call-site migration.
This round writes NO code. It exists because a round cannot record a verdict on itself
(docs/agents/planner_reviewer_prompt.md §4.13), so R61's gate entry is owed by the round after it,
and the reviewer's session is ending at its stated round cap under self-drive guardrail G7 rather
than starting a migration round it cannot also review. R63 does `apps/cli/commands/runtime_cmd.py`
with a full block of its own.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 record the R61 PASS · C3 handback. That list runs past C0a, C0b, C1, C2 to C3, so it holds
five commits or fewer and the handback keeps the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R61 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO REWRITE PAIR IS PLAN16; ITS
END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD30 — listed rather than counted, per §3
checklist item 11. The append slice CARRIES ITS OWN LEADING BLANK LINE, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape
that was reasoned about.

## Change

C1 applies PLAN16F→PLAN16T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep
a stale label. C2 appends RECORD30 to the END of `.agent/live_review.md`.

Change set, named rather than counted: `.agent/authored/f085-r62.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. Nothing else. NO `.py` path is in
that set, so no lint gate and no red control is ordered — there is no code this round could break.
No `docs/roadmap/**` path is in it either, so the §3 docs tier does NOT trigger and no `tests/docs/`
gate is ordered. `apps/cli/commands/runtime_cmd.py` is NOT in it; it is R63's. That path and the two
migrated at R61 — `packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` —
were each resolved on disk at a05669a5 with `git ls-tree` before this block was emitted, per §3
checklist item 24, and all three exist.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r62.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders NO destructive check, so `git worktree list` is one line at
   round start, throughout, and at the end — do not create a worktree.
3. PAIR SHAPES. The reviewer ran the containment test at emission against that file's blob at
   a05669a5 and prints its own output here per checklist item 15: PLAN16F→PLAN16T
   `TO contains FROM: false`. PLAN16 is therefore a REWRITE and owes the FROM 0x / TO 1x reading
   over its post-commit file. Its FROM occurs EXACTLY 1x in `.agent/plan.md` at a05669a5 — the
   reviewer measured it.
4. RECORD30 HAS NO FROM. It is appended at the END of `.agent/live_review.md`. Its obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for it and do not report a FROM count.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record. Only C0a and C0b may precede it. This
   round writes to the finding ledger, so §3 checklist item 23 binds it.
6. Every sentence in RECORD30 that states a reading of a file THIS BLOCK also edits names the SHA it
   was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD30 is reviewer text. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD30 to reconcile it with
   anything you measure. A disagreement between RECORD30 and your own reading is a finding to REPORT
   in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. Registered stays 174, done stays 28, landed
   stays 0, open stays 146, and the next free id stays R-0560. RECORD30 is a `Gate:` paragraph and
   carries no `- R-` registration line and no `Done:` line, which is why the arithmetic must not
   move; G6 exists to prove it did not.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and reports them in G2. The worker re-measures all three from the
   committed `.agent/authored/f085-r62.md` and reports them; a mismatch is a finding against this
   block, not against the worker.
10. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line at round start and at the end, with
NO worktree created in between.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r62.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each, measured on every copy. Also report the block's TOTAL, PROSE and
RECORD30 line counts read from that committed file, against the 490 / 400 / 140 figures in
constraint 9. The reviewer holds its own original and runs the disk-to-disk comparison against it
itself; do not name or read any path outside the repository's tracked tree.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN16F→PLAN16T is a REWRITE: report its FROM 0x and its TO exactly 1x over the post-commit blob,
   and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the post-commit blob
   BYTE-EXACTLY.
 - For RECORD30 report the ordered-equality readings constraint 4 names: pre-commit blob is a
   byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the post-commit blob byte
   for byte, and the commit's ADDED lines are exactly the slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
both base readings below itself, in the primary checkout, at a05669a5. This round changes no code,
so each expected reading is the base reading UNCHANGED.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites, and that is the whole reason this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 44 lines mechanically by applying the pair to that file's blob at a05669a5.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
a05669a5 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558. At HEAD the reading must be IDENTICAL — 174 / 28 / 0, 146 open, same two maxima — and all
three symmetric differences must be EMPTY, because constraint 8 rules this round registers and
resolves nothing. Next free id R-0560. Report all three symmetric differences, the duplicate-id
count and the count of resolutions naming an unregistered id, at both SHAs.

G7 HYGIENE. `git diff --name-only a05669a5..HEAD` measured BEFORE C3 holds exactly the change set
above minus `.agent/handoff.md`, which C3 writes, and nothing else — and in particular holds NO
`.py` path at all, and neither `apps/cli/commands/runtime_cmd.py`, whose migration is R63's, nor
either of the two paths R61 migrated. Those three paths were resolved on disk at a05669a5 with
`git ls-tree a05669a5 -- <path>`, one call per path, and all three exist; re-run those three calls
and report each result, per §3 checklist item 24. Report per-commit insertions for every commit
BEFORE C3 — C3 cannot measure itself, so its own insertions go in the round report — and confirm
none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a
second oversize commit is a STOP under constraint 10, never a declaration. Confirm every commit is
single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA a05669a5, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2 and
C3, the real G1-G7 results with exit codes, the open-findings count and the next expected action.
The Bundle above holds five commits or fewer, so the ≤60-line cap applies; if the mandated content
genuinely does not fit, name the DECISION D15 stated cause and the specific mandated content behind
the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~98 % (T001 gebaut · R13-R61 PASS · T002a-T002d KOMPLETT · T002e — die
`runtime-server`-Policy gebaut, die beiden App-Call-Sites migriert und mit einem
Kind-Environment-Test gepinnt, `apps/cli/commands/runtime_cmd.py` offen · T003 offen) — Schätzung,
gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R63, which migrates the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, whose
child is the Remedy supervisor rather than a project application; its declared keys are
`REMEDY_DATA_DIR`, `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT`, and that round must also
decide whether the supervisor still needs `PYTHONPATH` and `VIRTUAL_ENV` beyond what
`RUNTIME_SERVER_ENV_ALLOWLIST` already carries, because the CLI spawns it as `python -m` from the
Remedy checkout. TWO: R62 carries no verdict of its own, because the round that records a verdict
cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R63 carries it. THREE: a
standalone closing line stating the open findings count and the next free id as its own sentence.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol
requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN16F
## Current Step
R61, this round: the two APP-spawning `runtime-server` call sites — `packages/runtimes/dev_server.py`
and `packages/runtimes/runtime_supervisor.py` — take `plan_child_spawn`, so a project's application
inherits the allowlist plus `PORT` and the spec's own keys and nothing else. A test reads the
environment from inside the running child. The R60 PASS is recorded in the same round.

## Next Steps
1. Migrate the LAST call site, `apps/cli/commands/runtime_cmd.py`, whose child is the Remedy
   supervisor rather than a project application. Its declared keys are `REMEDY_DATA_DIR`,
   `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT`: the supervisor resolves its runtime
   directory through `projects_dir()`, the boundary suite passes the log cap to the CLI, and the
   supervisor reads the port with `os.environ[...]` and dies without it.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN16F

BEGIN-PLAN16T
## Current Step
R62, this round: a RECORD round that writes no code. It records the R61 PASS, which the round
after a verdict always owes because a round cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13). The two app-spawning call sites migrated at R61
are verified and unchanged; the third has not been touched.

## Next Steps
1. Migrate the LAST call site, `apps/cli/commands/runtime_cmd.py`, whose child is the Remedy
   supervisor rather than a project application. Its declared keys are `REMEDY_DATA_DIR`,
   `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT`; settle before editing whether the
   supervisor also needs `PYTHONPATH` and `VIRTUAL_ENV`, since the CLI spawns it as `python -m`
   from the Remedy checkout rather than the project's.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN16T

BEGIN-RECORD30

Gate: R62 — the R61 entry. R61 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer over
5b9f935b..a05669a5, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared and one stated assumption about when a base reading
was taken, which the reviewer's own independent base reading corroborates. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest
fallback: the reviewer's original, the committed `.agent/authored/f085-r61.md` and the committed
`.agent/last_block.md` at a05669a5, and both of those working copies as they stand at a05669a5, are
all five byte-EQUAL at sha256
bb18ff7d5cdb461883a2e3b35fa6e137f178bbf759362d312904c91cd5b80eab, 30129 B, 484 lines, 32 marker
lines. THE SHAPES HELD, and the two classes were measured apart, one reading per pair. The five
REWRITES each end FROM 0x with TO exactly 1x — PLAN16's predecessor PLAN15 at 70c6c741, numstat
`9 10`, and SITE2B, SITE3B, BOUNDA and BOUNDB at 63c9fd46. The two APPEND-shaped pairs, SITE2A and
SITE3A at 63c9fd46, end FROM 1x and TO 1x, and no zero count was owed or reported for either. For
all seven, re-applying the extracted pairs in order to the pre-commit blob reproduces the
post-commit blob BYTE-EXACTLY, per path. The two FROM-less appends satisfy ORDERED EQUALITY on every
clause: RECORD29 at 603e39f7 and TESTCODE at 9727c5e3 each have the pre-commit blob as a byte-exact
PREFIX, the slice as an exact SUFFIX, `pre + slice` equal to the post-commit blob byte for byte, and
the commit's ADDED lines equal to the slice's lines IN ORDER — 36 and 49 lines, numstat `36 0` and
`49 0`. Marker LINES at a05669a5 are 0 in all six edited files. BOTH LINT HALVES WERE ALREADY RED AT
THE BASE, so both were compared as rule-code MULTISETS rather than demanded green, and both are
UNCHANGED: `ruff check` over the four paths gives `{I001: 1}` at 5b9f935b and `{I001: 1}` at
a05669a5, and `ruff check --preview` gives `{E303: 1, I001: 1}` at both — no new code and no second
instance, so neither migration introduced a lint finding. THE SUITES WERE RE-RUN, NOT READ, in the
primary checkout with the block's exact command lines, each exit 0: `tests/runtimes/` `252 passed`
against a base of `251 passed` with no skips at either, which is the base plus exactly the one test
C4 added; the guard suite `36 passed`, unchanged, so the seam this round CONSUMES was not altered;
the four state readers `160 passed`, unchanged; the canary `42 passed`. THE PLAN CONTRACT HELD at
70c6c741: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 44 being the figure that block projected. THE ARITHMETIC DID NOT MOVE, as constraint 8 of
that block required: 174 registered / 28 done / 0 landed and 146 open at 5b9f935b, the same three
numbers and the same 146 at a05669a5, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 resolutions naming an unregistered id at
both SHAs. HYGIENE IS CLEAN: the path set over 5b9f935b..9727c5e3 is exactly the eight the change set
named and holds `apps/cli/commands/runtime_cmd.py` not at all; per-commit INSERTIONS are 484, 397, 9,
36, 46, 49 and 54 for the handback commit, none over 500; all seven commits are single-parent. THE
BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 484, PROSE 269 and RECORD29 36,
agreeing with that block's own figures and under 490 / 400 / 140. TWO CLAIMS NO GATE COVERED WERE
CHECKED RATHER THAN ACCEPTED, both by the reviewer before the block was emitted and both inside a
disposable worktree since removed, with the primary checkout's `git status --porcelain` empty
immediately after each. FIRST, the block's own slices were applied to a throwaway tree and its gates
run there, which is how the boundary test
`test_the_readiness_failure_returns_the_line_the_child_really_printed` was found to go RED at exit 3
under the migration alone — it handed its application a marker path through the PARENT environment —
and that is why C3 carries its adaptation in the same commit instead of leaving a knowingly red
commit on the branch. SECOND, the red control: reverting ONLY `env=spawn_plan.env` to `env=env` in
`packages/runtimes/dev_server.py` makes the new test FAIL on exactly its
`ANTHROPIC_API_KEY not in child_env` assertion, with the imported module path printed from inside
the same invocation to prove the worktree copy was the one under test. So the test pins the scrub
rather than passing for an unrelated reason. NOTHING FAILED and this round registers no finding.
END-RECORD30
