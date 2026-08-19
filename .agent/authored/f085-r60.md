── STEP record round — F085 — R60 ────────────────────────────────────────────

Goal: record the R59 PASS and leave the branch on a clean edge for the call-site migration. This
round writes NO code. It exists because a round cannot record a verdict on itself
(docs/agents/planner_reviewer_prompt.md §4.13), so R59's gate entry is owed by the round after it,
and the reviewer's session is ending at its stated round cap under self-drive guardrail G7 rather
than starting a design round it cannot also review. R61 does the three `runtime-server` call sites
with a full block of its own.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 record the R59 PASS · C3 handback. That list runs past C0a, C0b, C1, C2 to C3, so it holds
five commits or fewer and the handback keeps the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R59 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO REWRITE PAIR IS PLAN14; ITS
END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD28 — listed rather than counted, per §3
checklist item 11. The append slice CARRIES ITS OWN LEADING BLANK LINE, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape
that was reasoned about.

## Change

C1 applies PLAN14F→PLAN14T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep
a stale label. C2 appends RECORD28 to the END of `.agent/live_review.md`.

Change set, named rather than counted: `.agent/authored/f085-r60.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. Nothing else. NO `.py` path is in
that set, so no lint gate and no red control is ordered — there is no code this round could break.
No `docs/roadmap/**` path is in it either, so the §3 docs tier does NOT trigger and no `tests/docs/`
gate is ordered. The three call sites — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — are NOT in it;
they are R61's. Each of the three was resolved on disk at d91d2ffa with `git ls-tree` before this
block was emitted, per §3 checklist item 24, which R59 promoted and which this block therefore owes.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r60.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders NO destructive check, so `git worktree list` is one line at
   round start, throughout, and at the end — do not create a worktree.
3. PAIR SHAPES. The reviewer ran the containment test at emission against that file's blob at
   d91d2ffa and prints its own output here per checklist item 15: PLAN14F→PLAN14T
   `TO contains FROM: false`. PLAN14 is therefore a REWRITE and owes the FROM 0x / TO 1x reading
   over its post-commit file. Its FROM occurs EXACTLY 1x in `.agent/plan.md` at d91d2ffa — the
   reviewer measured it.
4. RECORD28 HAS NO FROM. It is appended at the END of `.agent/live_review.md`. Its obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for it and do not report a FROM count.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record. Only C0a and C0b may precede it. This
   round writes to the finding ledger, so §3 checklist item 23 binds it.
6. Every sentence in RECORD28 that states a reading of a file THIS BLOCK also edits names the SHA it
   was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD28 is reviewer text. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD28 to reconcile it with
   anything you measure. A disagreement between RECORD28 and your own reading is a finding to REPORT
   in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. Registered stays 174, done stays 28, landed
   stays 0, open stays 146, and the next free id stays R-0560. RECORD28 is a `Gate:` paragraph and
   carries no `- R-` registration line and no `Done:` line, which is why the arithmetic must not
   move; G7 exists to prove it did not.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission: TOTAL 253, PROSE 170, RECORD28 47. The worker re-measures all three from
   the committed `.agent/authored/f085-r60.md` and reports them; a mismatch is a finding against
   this block, not against the worker.
10. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line at round start and at the end, with
NO worktree created in between.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r60.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r60.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN14F→PLAN14T is a REWRITE: report its FROM 0x and its TO exactly 1x over the post-commit blob,
   and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the post-commit blob
   BYTE-EXACTLY.
 - For RECORD28 report the ordered-equality readings constraint 4 names: pre-commit blob is a
   byte-exact PREFIX, the slice is an exact SUFFIX, and the commit's ADDED lines are exactly the
   slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at d91d2ffa. This round changes no code,
so each expected reading is the base reading UNCHANGED.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites, and that is the whole reason this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 45 lines mechanically by applying the pair to that file's blob at d91d2ffa.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
d91d2ffa and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558. At HEAD the reading must be IDENTICAL — 174 / 28 / 0, 146 open, same two maxima — and all
three symmetric differences must be EMPTY, because constraint 8 rules this round registers and
resolves nothing. Next free id R-0560. Report all three symmetric differences, the duplicate-id
count and the count of resolutions naming an unregistered id, at both SHAs.

G7 HYGIENE. `git diff --name-only d91d2ffa..HEAD` measured BEFORE C3 holds exactly the change set
above minus `.agent/handoff.md`, which C3 writes, and nothing else — and in particular holds NONE of
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
`packages/runtimes/runtime_supervisor.py`, whose migration is R61's, and no `.py` path at all.
Those three paths were resolved on disk at d91d2ffa with `git ls-tree d91d2ffa -- <path>`, one call
per path, and all three exist; re-run those three calls and report each result, per §3 checklist
item 24. Report per-commit insertions for every commit BEFORE C3 — C3 cannot measure itself, so its
own insertions go in the round report — and confirm none exceeds 500. This branch spent the
AGENTS.md declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under
constraint 10, never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA d91d2ffa, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2 and
C3, the real G1-G7 results with exit codes, the open-findings count and the next expected action.
The Bundle above holds five commits or fewer, so the ≤60-line cap applies; if the mandated content
genuinely does not fit, name the DECISION D15 stated cause and the specific mandated content behind
the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~97 % (T001 gebaut · R13-R59 PASS · T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT ·
T002d KOMPLETT · T002e — die `runtime-server`-Policy gebaut und verifiziert, die drei Call-Sites
offen · T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R61, which migrates the three `runtime-server` call sites — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — onto
`runtime_server_exec_policy` via `plan_child_spawn`, each keeping its own `Popen` and its own
supervision; that round's first task is to settle, per site, which keys its child needs on top of
`RUNTIME_SERVER_ENV_ALLOWLIST`, because `apps/cli/commands/runtime_cmd.py` at d91d2ffa builds its
child environment as `dict(os.environ)` plus `REMEDY_RUNTIME_PORT` and a scrub would drop whatever
else that child reads. TWO: R60 carries no verdict of its own, because the round that records a
verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R61 carries it.
THREE: a standalone closing line stating the open findings count and the next free id as its own
sentence. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive
protocol requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN14F
## Current Step
R59, this round: T002e. `runtime_server_exec_policy` and `RUNTIME_SERVER_ENV_ALLOWLIST` are added
to `packages/orchestration/exec_guard.py` — the row Amendment F085 D8 rules must hold NO wall
timeout — together with the test that pins both absent columns and the environment scrub. The seam
is POLICY-ONLY: the three call sites keep their own `Popen` and take `plan_child_spawn`. The R58
PASS is recorded and R-0559 registered in the same round.

## Next Steps
1. Migrate the three `runtime-server` call sites onto the policy:
   `apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
   `packages/runtimes/runtime_supervisor.py`. Each keeps its own `Popen` and its own
   supervision; what changes is the `cwd`, `env` and `preexec_fn` it spawns with, which come
   from `plan_child_spawn`.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN14F

BEGIN-PLAN14T
## Current Step
R60, this round: a RECORD round that writes no code. It records the R59 PASS, which the round
after a verdict always owes because a round cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13). The `runtime-server` policy built at R59 is
verified and unchanged; nothing consumes it yet.

## Next Steps
1. Migrate the three `runtime-server` call sites onto the policy:
   `apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
   `packages/runtimes/runtime_supervisor.py`. Each keeps its own `Popen` and its own
   supervision; what changes is the `cwd`, `env` and `preexec_fn` it spawns with, which come
   from `plan_child_spawn`. Settle per site which keys its child needs on top of
   `RUNTIME_SERVER_ENV_ALLOWLIST` BEFORE editing: a scrub that drops one breaks a server.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN14T

BEGIN-RECORD28

Gate: R60 — the R59 entry. R59 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
79f79f27..d91d2ffa, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: `.remedy-wt/f085-r59.md`,
the committed `.agent/authored/f085-r59.md` and the committed `.agent/last_block.md` at d91d2ffa, and
both of those working copies as they stand at d91d2ffa, are all five byte-EQUAL at sha256
8df06395327c5573a708a055a05eaf9b0d0d02b5103ba823908f1e13abbc1fed, 31513 B, 447 lines, 14 marker
lines, which is the digest the reviewer emitted. THE SHAPES HELD, and the two classes were measured
apart. PLAN13F→PLAN13T at 0279b57e is a REWRITE: `TO contains FROM: false`, FROM 1x before and 0x
after, TO exactly 1x, numstat `10 8`. CHECKF→CHECKT at b5b76e3c is APPEND-shaped: `TO contains FROM:
true`, FROM 1x and TO 1x after, no zero count owed or reported, numstat `14 0`. For BOTH,
re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob
BYTE-EXACTLY. The three FROM-less appends satisfy ORDERED EQUALITY on every clause: for RECORD28's
predecessor RECORD27 at 307b4456, and for SEAMCODE and TESTCODE at b2104539, the pre-commit blob is
a byte-exact PREFIX, the slice an exact SUFFIX, `pre + slice` equals the post-commit blob byte for
byte, and each commit's ADDED lines equal that slice's lines IN ORDER — 65, 58 and 31 lines, numstat
`65 0`, `58 0` and `31 0`. Marker LINES at d91d2ffa are 0 in all five edited files. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with the block's exact command lines, each exit 0: the
guard suite `36 passed`, which is the 36 the block ordered the worker to confirm rather than assume;
the four state readers `160 passed`, unchanged as ordered; the canary `42 passed`. BOTH LINT HALVES
HELD IN THE STRONG FORM over the two `.py` paths: `ruff check` exit 0 `All checks passed!` and
`ruff check --preview` exit 0 `All checks passed!`, which is the direct evidence that SEAMCODE and
TESTCODE carried their own leading blank lines — the R-0558 counter-measure holding as bytes rather
than as reasoning. THE PLAN CONTRACT HELD at 0279b57e: 45 lines against the 50-line cap with
`## Goal`, `## Next Steps` and a roadmap F-id present, 45 being the figure that block projected.
THE ARITHMETIC MOVED EXACTLY AS ORDERED: 173 / 28 / 0 and 145 open at 79f79f27, 174 / 28 / 0 and 146
open at d91d2ffa, the registered symmetric difference exactly `{R-0559}` ADDED with the done and
landed symmetric differences both EMPTY, and 0 duplicate ids and 0 resolutions naming an
unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over 79f79f27..b2104539 is exactly the
seven the change set named and holds none of the three R61 call sites; per-commit INSERTIONS are
447, 368, 10, 14, 65, 89 and 91 for the handback commit, none over 500; all seven commits are
single-parent. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 447, PROSE 243
and RECORD27 65, agreeing with that block. CHECKLIST ITEM 24 WAS APPLIED TO THE BLOCK THAT REGISTERED
IT: all three R61 call sites resolve at 79f79f27 — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — so the R-0559
defect did not recur in the round that named it. THE RED CONTROL WAS RE-RUN BY THE REVIEWER, in a
disposable worktree since removed: `wall_timeout_seconds=None,` occurs 2x after C4 and mutating the
LAST occurrence alone to `30.0` gives EXIT 1 with exactly one failure,
`test_the_runtime_server_policy_holds_no_clock_and_no_cap`. THE CLAIM NO ORDERED GATE COVERS WAS
CHECKED RATHER THAN ACCEPTED, because the new test asserts on the policy dataclass and never spawns:
at d91d2ffa the reviewer built the policy with a declared key and a forbidden key both present, took
`plan_child_spawn`, and spawned a real child with the returned `cwd`, `env` and `preexec_fn`. The
child exited 0, reported its cwd as the pinned directory, received `REMEDY_RUNTIME_PORT`, did NOT
receive `ANTHROPIC_API_KEY`, and read `RLIMIT_CORE` as `(0, 0)` — so the rlimit really is applied
between fork and exec and the scrub really is enforced, on the one path the suite exercises only by
proxy. NOTHING FAILED and this round registers no finding.
END-RECORD28
