── STEP T002e — F085 — R59 ───────────────────────────────────────────────────

Goal: build the `runtime-server` seam. Amendment F085 D8 rules `runtime-server` a row of its own
that must hold NO wall timeout, and R58's handback left open whether such a policy exists yet. It
does not: at 79f79f27 `packages/orchestration/exec_guard.py` carries no `runtime_server` symbol at
all. This round adds it. The seam is POLICY-ONLY, exactly like `dod-app`: `run_guarded` supervises
a child to COMPLETION and a server never completes, so the three call sites keep their own `Popen`
and take `plan_child_spawn`. This round also records the R58 PASS and registers R-0559 against the
R58 block's own gate text.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 promote the R-0559 counter-measure into the §3 checklist · C3 record the R58 PASS and register
R-0559 · C4 add the policy and its test · C5 handback. That list runs past C0a, C0b, C1, C2, C3, C4
to C5, so it holds more than five commits and the handback carries the ≤100-line allowance rather
than the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R58 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO REWRITE PAIRS ARE PLAN13 AND
CHECK; ITS END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD27, SEAMCODE AND TESTCODE —
listed rather than counted, per §3 checklist item 11. Each append slice CARRIES ITS OWN LEADING BLANK
LINES: that is the R-0558 counter-measure applied rather than restated, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape
that was reasoned about.

## Change

C1 applies PLAN13F→PLAN13T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can
keep a stale label. C2 applies CHECKF→CHECKT to `docs/agents/planner_reviewer_prompt.md`, adding
item 24 at the END of the §3 checklist, ahead of the "Why this is on disk" paragraph that closes
it. C3 appends RECORD27 to the END of `.agent/live_review.md`. C4 appends SEAMCODE to the END of
`packages/orchestration/exec_guard.py` and TESTCODE to the END of
`tests/orchestration/test_exec_guard.py`, in ONE commit, because a policy whose test does not land
with it is exactly the shape this feature's own gates exist to catch.

Change set, named rather than counted: `.agent/authored/f085-r59.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
`packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py`,
`.agent/handoff.md`. Nothing else. No `docs/roadmap/**` path is in that set, so the §3 docs tier
does NOT trigger and no `tests/docs/` gate is ordered; `docs/agents/**` is outside what
`tests/docs/` reads. The three call sites — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — are NOT in it:
this round builds the seam, R60 migrates onto it, and those three paths are what R-0559 exists to
correct. Each of the three was resolved on disk at 79f79f27 with `git ls-tree` before this block
was emitted, which is the counter-measure C2 promotes, applied to this block's own text.

WHY THE SEAM SHIPS NO RUN WRAPPER. Every other class in T2_F085's table has a
`run_guarded_<class>_command` returning a `CompletedProcess`. `runtime-server` gets none, and that
absence IS the design: `run_guarded` buffers both streams and waits for the child to exit, while
all three sites spawn with `start_new_session=True` and then supervise for the life of the service
— two through a `LogPump` carrying its own `max_bytes`, one straight to `DEVNULL`. The policy
therefore sets `output_cap_bytes=None` for the reason `dod_app_exec_policy` already records about
its own row, and the absence is stated in the docstring, which is where AGENTS.md's Code
Discoverability section says a deliberate absence belongs.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r59.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round DOES order a destructive check (G9), which runs ONLY in a
   disposable `git worktree` under `.remedy-wt/` and is removed before the handback, so
   `git worktree list` is one line at round start and again at the end.
3. PAIR SHAPES. The reviewer ran the containment test on each REWRITE pair at emission against that
   file's blob at 79f79f27 and prints its own output here per checklist item 15, one reading per
   pair: PLAN13F→PLAN13T `TO contains FROM: false`; CHECKF→CHECKT `TO contains FROM: true`.
   PLAN13 is therefore a REWRITE and owes the FROM 0x / TO 1x reading over its post-commit file.
   CHECKT CONTAINS ITS FROM, so it is an APPEND-shaped pair and the FROM-0x reading is UNATTAINABLE
   for it by construction: it owes FROM exactly 1x and TO exactly 1x, and NO zero count. Both FROMs
   occur EXACTLY 1x in their target at 79f79f27 — the reviewer measured both.
4. THE THREE APPENDS HAVE NO FROM. RECORD27, SEAMCODE and TESTCODE are appended at the END of their
   target. Their obligation is ORDERED EQUALITY per §4.9 as R-0531 narrows it, which is what a code
   append owes instead of a per-line count: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for them and do not report a FROM count.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the checklist, the record and the seam. Only C0a and
   C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. C2 PRECEDES C3, and that order is what makes RECORD27 honest: RECORD27 states that item 24 is in
   the checklist, and this constraint is the ordering requirement checklist item 24 of R-0524's
   carve-out asks for in place of a SHA that cannot exist when the slice is written.
7. Every sentence in RECORD27 that states a reading of a file THIS BLOCK also edits names the SHA it
   was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD27 is reviewer text and carries both the R58
   gate record and the R-0559 registration; do not add a `Landed:` line, do not add a `Done:`
   paragraph of your own, and do not edit RECORD27 to reconcile it with anything you measure. A
   disagreement between RECORD27 and your own reading is a finding to REPORT in the handback, never
   to fix.
9. THIS ROUND REGISTERS R-0559 AND RESOLVES NOTHING. Registered goes 173 → 174, done stays 28,
   landed stays 0, open goes 145 → 146, and the next free id becomes R-0560.
10. THE SEAM IS ADDITIVE AND NOTHING EXISTING MOVES. Do not edit `run_guarded`, `plan_child_spawn`,
   `scrub_child_env`, any existing policy or any existing test. SEAMCODE and TESTCODE are appended
   whole; no line above them changes. In particular do NOT add a
   `run_guarded_runtime_server_command`: its absence is the design and the docstring says so.
11. DO NOT REFORMAT EITHER TARGET AND DO NOT RUN `ruff --fix`. Both `.py` files this round edits are
   preview-CLEAN at 79f79f27 — the reviewer measured `python3 -m ruff check --preview` exit 0 with
   zero findings on each — so G5 is ordered in the STRONG form, exit 0 at HEAD, and no multiset
   narrowing is needed or permitted.
12. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission: TOTAL 447, PROSE 243, RECORD27 65. The worker re-measures all three
   from the committed `.agent/authored/f085-r59.md` and reports them; a mismatch is a finding
   against this block, not against the worker.
13. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line at round start and at the end, with
the G9 worktree created and removed in between.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r59.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r59.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN13F→PLAN13T is a REWRITE: report its FROM 0x and its TO exactly 1x over the post-commit blob.
 - CHECKF→CHECKT is APPEND-shaped: report its FROM exactly 1x and its TO exactly 1x over the
   post-commit blob, and report NO zero count for it.
 - For BOTH pairs, re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - For RECORD27, SEAMCODE and TESTCODE report the ordered-equality readings constraint 4 names:
   pre-commit blob is a byte-exact PREFIX, the slice is an exact SUFFIX, and the commit's ADDED
   lines are exactly the slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at 79f79f27.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` — base `35 passed`. This round
   adds exactly one test and deletes none, so REPORT the number and state whether it is 36.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites. Expected reading 160, unchanged, because this round adds no
   test to that set.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 LINT, over the SAME two `.py` paths, with the repository's own `pyproject.toml` and NEVER
`--isolated` (R-0463). Both commands at HEAD, each exit 0:
 - `python3 -m ruff check packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — `All checks passed!`.
 - `python3 -m ruff check --preview packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — `All checks passed!`. This is the STRONG form and it is
   ordered because the reviewer measured BOTH paths preview-clean at 79f79f27, exit 0 with zero
   findings each. A single preview finding at HEAD is a red gate under constraint 13 — it means a
   slice failed to carry the blank lines its target's convention wants, which is what R-0558 was
   registered for.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 45 lines mechanically by applying the pair to that file's blob at 79f79f27.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
79f79f27 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 173 / 28 / 0, 145 open, max registered R-0558, max resolved
R-0558. At HEAD the reading must be 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558: the registered symmetric difference is exactly R-0559 with direction ADDED, and the done and
landed symmetric differences are both EMPTY. Next free id R-0560. Report all three symmetric
differences with their direction, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 79f79f27..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds NONE of
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
`packages/runtimes/runtime_supervisor.py`, whose migration is R60's. Those three paths were resolved
on disk at 79f79f27 with `git ls-tree 79f79f27 -- <path>`, one call per path, and all three exist;
re-run those three calls and report each result, because a forbidding clause over a path that does
not resolve forbids nothing and that is precisely R-0559. Report per-commit insertions for every
commit BEFORE C5 — C5 cannot measure itself, so its own insertions go in the round report — and
confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85,
so a second oversize commit is a STOP under constraint 13, never a declaration. Confirm every commit
is single-parent.

G9 RED CONTROL, the proof the new test has teeth, run ONLY in a disposable worktree created from
HEAD under `.remedy-wt/` and removed before the handback. In that worktree, and NEVER in the primary
checkout, change `wall_timeout_seconds=None,` to `wall_timeout_seconds=30.0,` at the LAST occurrence
of that string in `packages/orchestration/exec_guard.py`. Target it by LAST occurrence and not by
the enclosing name: the string occurs TWICE after C4, once in `dod_app_exec_policy` and once in
`runtime_server_exec_policy`, and because SEAMCODE is appended at end of file the last is always the
one this gate means. Mutate that one alone, then run
`python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q`. ORDERED RESULT: the run is RED
and `test_the_runtime_server_policy_holds_no_clock_and_no_cap` is among the failures. Report the
exit code and the failing test names verbatim from the `-rf` summary — do NOT report a predicted
pass count. Then remove the worktree and confirm `git worktree list` is one line and
`git status --porcelain` is empty in the primary checkout.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 79f79f27, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3,
C4 and C5, the real G1-G9 results with exit codes, the open-findings count and the next expected
action. The Bundle above names seven commits, which is more than five, so the ≤100-line allowance
applies; if the mandated content genuinely does not fit even that, name the DECISION D15 stated
cause and the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~97 % (T001 gebaut · R13-R58 PASS · T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT ·
T002d KOMPLETT · T002e — die `runtime-server`-Policy gebaut, die drei Call-Sites offen · T003 offen)
— Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R60, which migrates the three `runtime-server` call sites — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — onto
`runtime_server_exec_policy` via `plan_child_spawn`, each keeping its own `Popen` and its own
supervision. TWO: R60 also carries the R59 verdict, because the round that records a verdict cannot
record one on itself (docs/agents/planner_reviewer_prompt.md §4.13). THREE: a standalone closing
line stating the open findings count and the next free id as its own sentence. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every
handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN13F
## Current Step
R58, this round: T002d's second half. The two `runtime-build` call sites in
`_auto_build_frontend` (`packages/orchestration/ui_server.py`) move onto
`run_guarded_runtime_build_command` with `check=True`, reached as a module attribute so a test
can patch it, and one new test pins that no bare `subprocess.run` survives in that function.
The R57 PASS and the resolution of R-0558 are recorded in the same round.

## Next Steps
1. The three `runtime-server` sites (`runtime_cmd.py`, `dev_server.py`,
   `runtime_supervisor.py`) — `Popen`-shaped, and taking NO wall timeout, because a clock
   would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN13F

BEGIN-PLAN13T
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
END-PLAN13T

BEGIN-CHECKF
  Why this is on disk and not a habit: item 2 has recurred six times across
END-CHECKF

BEGIN-CHECKT
  24. **Every path a gate NAMES is resolved on disk before the gate is ordered.** Finding R-0559.
      A gate that names a path — in a command, in a baseline reading, or in an ABSENCE clause such
      as "the round's path set holds neither X nor Y" — has each of those paths checked with
      `git ls-tree <base> -- <path>` at the base it names, and a path that does not resolve is
      corrected, or dropped with the correction stated inline. Item 21 binds the paths a baseline
      COMMAND runs over, where a missing path makes the tool exit and produce no reading at all;
      this one binds the paths a gate merely MENTIONS, where nothing exits and nothing is reported
      — the absence clause is satisfied by every possible round, so it forbids nothing while
      reading on the page exactly like a guard. The R58 instance: G8 forbade the round's path set
      to hold `packages/orchestration/runtime_cmd.py`, `packages/orchestration/dev_server.py` or
      `packages/orchestration/runtime_supervisor.py`, and all three of those files really live
      under `apps/cli/commands/` and `packages/runtimes/`, so the clause held trivially, protected
      nothing, and carried the wrong paths on into `.agent/handoff.md` — the map AGENTS.md's
      Session Resume tells the next session to read.
  Why this is on disk and not a habit: item 2 has recurred six times across
END-CHECKT

BEGIN-RECORD27

Gate: R59 — the R58 entry. R58 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
b2bb3809..79f79f27, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL,
disk-to-disk with no digest fallback: `.remedy-wt/f085-r58.md`, the committed
`.agent/authored/f085-r58.md` and the committed `.agent/last_block.md` at 79f79f27, and both of those
working copies as they stand at 79f79f27, are all five byte-EQUAL at sha256
6d46cb294da82694650390a40f65c57cc886dd9885d3e1302a638270e193bd77, 29671 B, 436 lines, 24 marker
lines, which is the digest the reviewer emitted. THE SHAPES HELD. All six pairs give
`TO contains FROM: false`, the FROM 1x in the pre-commit blob and 0x after with the TO exactly 1x,
and for all four (commit, path) pairs re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY: `.agent/plan.md` at 240934ad numstat `8 9`,
`.agent/live_review.md` at 728469ac numstat `53 1`, and at 35db0c2f
`packages/orchestration/ui_server.py` numstat `13 6` with the three pairs applied in order and
`tests/ui_server/test_dashboard_contract.py` numstat `35 0`. Marker LINES at 79f79f27 are 0 in every
one of those four files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with the block's
exact command lines, each exit 0: the dashboard contract `71 passed`, which is the 71 the block
ordered the worker to confirm rather than assume; responsive `92 passed`; the guard suite
`35 passed`; the four state readers `160 passed`; the canary `42 passed`. BOTH LINT HALVES HELD:
plain `ruff check` over the two paths is exit 0 `All checks passed!`, and the NARROWED PREVIEW
multiset comparison the R57 resolution mandated reproduces per path — `ui_server.py` `E306` x3 at
both b2bb3809 and 79f79f27, `test_dashboard_contract.py` `E226` x1 / `E303` x11 / `W391` x1 at both
— identical multisets, so no slice added a blank-line defect. THE PLAN CONTRACT HELD at 240934ad: 43
lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 43
being the figure that block projected. THE ARITHMETIC MOVED EXACTLY AS ORDERED: 173 / 27 / 1 and 146
open at b2bb3809, 173 / 28 / 0 and 145 open at 79f79f27, the registered symmetric difference EMPTY,
the done symmetric difference exactly `{R-0558}` ADDED and the landed symmetric difference exactly
`{R-0558}` REMOVED, with 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs.
HYGIENE IS CLEAN: the path set over b2bb3809..35db0c2f is exactly the six the change set named and
holds no `packages/orchestration/exec_guard.py`; per-commit INSERTIONS are 436, 366, 8, 53, 48 and
104 for the handback commit, none over 500; all six commits are single-parent. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 436, PROSE 267 and RECORD26T 53, agreeing with that
block, and the handback's self-claim of 135 lines measures 135. THE RED CONTROL WAS RE-RUN BY THE
REVIEWER, in a disposable worktree since removed: with BUILDT reverted to BUILDF at the
`npm run build` site alone, `python3 -m pytest tests/ui_server/test_dashboard_contract.py -rf -q` is
EXIT 1 with exactly one failure, `test_auto_build_npm_commands_run_through_the_guard`, on
`assert bare_run.call_count == 0` reading `1 == 0` — the worker's reading reproduced line for line.
THE ONE CLAIM NO ORDERED GATE COVERS WAS CHECKED RATHER THAN ACCEPTED, since every test in the round
MOCKS the seam and none exercises the real child: at 79f79f27 the real `npm run build` in `apps/ui`
returns rc 0 with 355 bytes of stdout and 0 of stderr THROUGH the seam and rc 0 with 355 and 0 bare,
so the narrowed `runtime-build` environment allowlist really does carry a working npm build, and
constraint 9's behaviour-preservation claim is measured rather than asserted. The exception contract
was read at 79f79f27 and holds: `_completed_process_from_guarded` raises `subprocess.TimeoutExpired`
on a wall trip, `run_guarded` lets `Popen` raise `FileNotFoundError` before any translation, and
`check=True` raises `subprocess.CalledProcessError`, so all three names in the two surviving `except`
tuples stay reachable.

- R-0559 — Medium — the R58 block's G8 ordered an absence reading over three paths that do not exist
in this repository. It named `packages/orchestration/runtime_cmd.py`,
`packages/orchestration/dev_server.py` and `packages/orchestration/runtime_supervisor.py` and
required the round's path set to hold none of them. The three real files are
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
`packages/runtimes/runtime_supervisor.py`, each resolved on disk at 79f79f27. A gate that forbids
touching a path which cannot appear forbids nothing, so the protection G8 claimed over the NEXT
round's files was never in force — the vacuous-gate class of R-0438 and R-0532, arriving through a
path that was never resolved rather than through a base that lacks it. R58 still PASSES: G8's other
half enumerated the round's path set POSITIVELY and exhaustively, and that reading is what actually
held the change set to six paths, so nothing wrong landed. The cost is that the same three wrong
paths reached `.agent/handoff.md` at 79f79f27, which is the map the next session reads, and the next
round is exactly the round those paths matter for. COUNTER-MEASURE: item 24 of the §3 checklist in
`docs/agents/planner_reviewer_prompt.md`, which constraint 6 of the R59 block fixes as landing in
the commit BEFORE this record — every path a gate NAMES is resolved with `git ls-tree` at the base
the gate names before the block is emitted. The rule is promoted into the checklist rather than left
in this paragraph, because a standing rule written as finding prose binds nothing and recurs
(R-0452, R-0454).
END-RECORD27

BEGIN-SEAMCODE


# ---------------------------------------------------------------------------
# The `runtime-server` seam (F085 T002e) — the long-lived application servers,
# which take the CHILD half ALONE for the reason `dod_app_exec_policy` states:
# each of the three call sites is already a supervisor owning its own readiness
# probe, its own log handling and its own stop path.
# ---------------------------------------------------------------------------


#: WHY: the environment a `runtime-server` child may inherit. The MEMBERS are the
#: `test`-class values and the NAME stays deliberately separate, for the reason
#: `DOD_APP_ENV_ALLOWLIST` states: T2_F085's policy table rules `runtime-server` as
#: its own row, so widening one row stays a one-line edit here.
RUNTIME_SERVER_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST


def runtime_server_exec_policy(
    *,
    cwd: str | None,
    env: Mapping[str, str] | None = None,
    declared_env_keys: Sequence[str] = (),
) -> ExecGuardPolicy:
    """The stage-1 policy every `runtime-server` child runs under.

    `wall_timeout_seconds` is None because Amendment F085 D8 rules this row must
    not hold a clock: a wall deadline would kill a served application mid-request,
    which is the whole reason the row was split off from `runtime-build`.

    `output_cap_bytes` is None for the reason `dod_app_exec_policy` records about
    its own row, and not as an omission of T2_F085's column: the cap is enforced
    WHILE READING a pipe, and all three call sites read their own — two through a
    `LogPump` carrying its own `max_bytes`, one sending the child to `DEVNULL`. A
    cap here would have to hold a pipe this policy never sees. T003's limitations
    document says so rather than letting the column imply a bound that is absent.

    `cpu_seconds`, `address_space_bytes` and `open_files` are None for the reasons
    `managed_builder_execution._builder_exec_policy` already settled for the
    builder class, not restated here so the two cannot drift apart.

    `env` is the CALLER's already-resolved environment and becomes the scrub
    SOURCE, because every one of the three sites builds one before it spawns;
    `declared_env_keys` names the keys it adds on top of the parent's. Those keys
    JOIN the allowlist, so `scrub_child_env` keeps them while `FORBIDDEN_ENV_KEYS`
    stays the floor beneath both.

    Remedy deliberately ships no `run_guarded_runtime_server_command`: `run_guarded`
    buffers both streams and waits for the child to EXIT, and a server never exits
    on its own, so the callers keep their own `Popen` and take `plan_child_spawn`.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=None,
        output_cap_bytes=None,
        cwd=cwd,
        core_file_bytes=0,
        env=dict(env) if env is not None else None,
        env_allowlist=RUNTIME_SERVER_ENV_ALLOWLIST + tuple(sorted(declared_env_keys)),
    )
END-SEAMCODE

BEGIN-TESTCODE


def test_the_runtime_server_policy_holds_no_clock_and_no_cap():
    """The two columns Amendment F085 D8 separates `runtime-server` by.

    Both are PARENT-side and all three call sites keep their own `Popen`, so None
    here is the row the table rules rather than an omission. The declared keys are
    asserted to JOIN the allowlist rather than replace it, and `FORBIDDEN_ENV_KEYS`
    is asserted to survive a caller that names one.
    """
    policy = exec_guard.runtime_server_exec_policy(
        cwd="/tmp/runtime-server-cwd",
        env={"PATH": "/usr/bin", "REMEDY_RUNTIME_PORT": "7331",
             "ANTHROPIC_API_KEY": "leak"},
        declared_env_keys=("REMEDY_RUNTIME_PORT", "ANTHROPIC_API_KEY"),
    )

    assert policy.wall_timeout_seconds is None
    assert policy.output_cap_bytes is None
    assert policy.cwd == "/tmp/runtime-server-cwd"
    assert policy.core_file_bytes == 0
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None
    assert set(exec_guard.RUNTIME_SERVER_ENV_ALLOWLIST) <= set(policy.env_allowlist)
    assert "REMEDY_RUNTIME_PORT" in policy.env_allowlist

    child_env = exec_guard.plan_child_spawn(policy).env
    assert child_env["REMEDY_RUNTIME_PORT"] == "7331"
    assert child_env["PATH"] == "/usr/bin"
    assert "ANTHROPIC_API_KEY" not in child_env
END-TESTCODE
