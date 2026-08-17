── STEP T002c second half, seam — F085 — R52 ─────────────────────────────────

Goal: add the `dod-app` seam to `packages/orchestration/exec_guard.py` — the policy the DoD's
application harness will run under — and record the R51 PASS together with finding R-0554. The
seam takes NO wall timeout and NO output cap, the two columns separating `dod-app` from every
bounded class in T2_F085's table, because its only future caller `_run_app_once` already owns its
own deadline, stops the process family in a `finally`, and writes the app's output to a file
rather than to a pipe.

THE CALLER ARRIVES AT R53, NOT HERE, and that is the point of the split. The reviewer sized the
undivided round at 506 lines against the 490-line TOTAL cap DECISION F085 D6 rules, so the round
was split at the module boundary rather than trimmed below the evidence it owes. This round adds a
seam and the test that holds it; R53 migrates `_run_app_once` onto it in
`packages/orchestration/dod_runners.py`, which is the same shape T002a and T002b already used —
`run_guarded_test_command` existed for a round before its sites moved.

`packages/orchestration/exec_guard.py`'s own PARTIAL COVERAGE note is deliberately NOT touched
this round. It says the DoD app harness still spawns unsupervised, and that stays TRUE until R53
migrates the call site; rewriting it here would put a claim on disk a round ahead of the change
that makes it true. R53 carries that rewrite.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R51 and register R-0554 · C3 append the seam · C4 append the test ·
C5 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line. A slice is the bytes strictly between its marker lines. Two append
shapes appear below and they differ: RECORD20 is PROSE joined to its target by exactly one blank
line, while SEAM2 and TESTSGUARD2 are CODE slices CARRYING their own leading blank lines, so for
those two the post-commit file is `pre + slice` with NO joiner byte.

## Change

C1 applies PLAN6F→PLAN6T to `.agent/plan.md` and C2 appends RECORD20 to `.agent/live_review.md`.
C3 appends SEAM2 to `packages/orchestration/exec_guard.py`. C4 appends TESTSGUARD2 to
`tests/orchestration/test_exec_guard.py`. C3 and C4 are separate commits over separate paths, so
each append proof has a pre-commit blob its own commit did not also rewrite.

Change set, named rather than counted: `.agent/authored/f085-r52.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/handoff.md`. Nothing else — in particular
`packages/orchestration/dod_runners.py` is NOT in this round's change set. No `docs/roadmap/**`
path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered;
`.py` files ARE in it, so a lint gate is, and G4 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r52.md` by its marker pair. Never retype one, never apply one from the
   prompt, never reflow one to a different wrap, and never add, rename or reorder a test the
   slices define. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit. This round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line throughout.
3. PAIR SHAPES. This round has exactly ONE pair. The reviewer ran the containment test on it at
   emission against `.agent/plan.md`'s blob at 67475107 and prints that test's own output here per
   checklist item 15: PLAN6F→PLAN6T `TO contains FROM: false`. It is therefore a REWRITE and owes
   the FROM 0x / TO 1x reading over its whole post-commit file. PLAN6F spans the `## Current Step`
   section AND the WHOLE `## Next Steps` list rather than a prefix of either, because its TO drops
   the completed item and so changes that list's arity (checklist item 17). PLAN6F occurs EXACTLY
   1x in its target at 67475107 — the reviewer measured it — so it is not ambiguous. RECORD20,
   SEAM2 and TESTSGUARD2 are APPENDS carrying no FROM, so no containment reading is owed for them.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both code commits. Only
   C0a and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23
   binds it. RECORD20's registration of R-0554 states that C1 of THIS round retires the clause it
   names, which it may do under checklist item 20 as R-0524 carves it out — a claim about the
   round's OWN landed change names the block constraint fixing the commit order rather than a SHA
   that cannot exist when the slice is written. This is that constraint.
5. Every sentence in RECORD20 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD20 lands, which is why the SHA and never the
   present tense carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested PLAN6F against every
   later-applied text at emission and got NO hits, so G3's FROM-0x reading stays attainable
   (checklist item 2, whose failure mode is a TO that quotes retired text on purpose).
7. Nothing outside the declared change set is touched. This round REGISTERS R-0554 and resolves
   nothing, so the registered count rises by one, the done count is unchanged and the open count
   rises from 141 to 142; the next free id becomes R-0555. `.agent/plan.md` after C1 is 44 lines,
   which the reviewer projected mechanically by applying the pair to that file's blob at 67475107.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never
   widen the change set to route around a red.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 373, PROSE 205, RECORD20 55. The worker
   re-measures all three from the committed `.agent/authored/f085-r52.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. THE REVIEWER ALREADY RAN THIS ROUND'S RED CONTROL, at 67475107, in a disposable worktree it
   removed afterwards, with these exact slice bytes applied by the extraction ordered above.
   Giving the seam a `wall_timeout_seconds` of 30.0 instead of None, and an `output_cap_bytes` of
   1024 instead of None, each failed the new policy test on the assertion naming that column. DO
   NOT repeat it: it is recorded here so this round needs no worktree, and G2 plus G3 are what
   carry that reading onto the worker's own commits.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty
at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r52.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r52.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The ONE REWRITE of constraint 3: in `.agent/plan.md` after C1, PLAN6F occurs 0x and PLAN6T
   exactly 1x. Report both counts and `git show --numstat` for that path and commit.
 - C2 / RECORD20 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies in its PROSE form: every non-empty line the slice
   contains occurs exactly once among the lines C2's diff adds TO THAT PATH.
 - C3 / SEAM2 and C4 / TESTSGUARD2 are CODE APPENDS, so §4.9 as R-0531 narrows it orders ORDERED
   EQUALITY rather than a per-line count: for each, the pre-commit blob is a byte-exact PREFIX of
   the post-commit file, the slice is an exact SUFFIX, the post-commit file equals `pre + slice`
   with no joiner byte, the lines that commit's diff adds TO THAT PATH are exactly the slice's
   lines IN ORDER, and 0 marker LINES reach the file. Report `git show --numstat` for each path.

G4 LINT, the repository's own configuration and never `--isolated`, exit 0:
`python3 -m ruff check packages/orchestration/exec_guard.py
tests/orchestration/test_exec_guard.py` — base reading at 67475107, taken by the reviewer with
this exact command line: `All checks passed!`, exit 0.

G5 CODE SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_dod_runners.py
tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf` — the
file this round edits plus the two modules whose behaviour the seam must leave untouched. Base at
67475107, taken by the reviewer in the primary checkout: `150 passed`. TESTSGUARD2 adds one test
and nothing else changes, so a green run reads `151 passed`; REPORT the number this run prints.

G6 STATE READERS, primary checkout, exit 0: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
ordered because C1 rewrites `.agent/plan.md`, which two of them assert on. Base at 67475107:
`159 passed`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base at 67475107
`42 passed`. REPORT both numbers.

G7 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each of
the three booleans. G6 covers the first three through their tests; this gate covers the cap.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
67475107 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 168 / 27 / 0, 141 open, max registered R-0553, max resolved
R-0532. At HEAD the registered count must read 169, the done count must be UNCHANGED at 27 and the
landed count UNCHANGED at 0; the registered symmetric difference must be exactly R-0554 while the
done and landed symmetric differences are EMPTY, because this round registers that one id and
resolves nothing; 142 open, next free id R-0555. Report the three symmetric differences, the
duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only 67475107..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular does NOT
hold `packages/orchestration/dod_runners.py`. Report per-commit insertions for every commit BEFORE
C5 — C5 cannot measure itself, so its own insertions go in the round report — and confirm none
exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second
oversize commit is a STOP under constraint 8, never a declaration. Confirm every commit has
exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 67475107, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4 and C5, the real G1-G9 results with exit codes, the open-findings count and the next
expected action. Six commits, so the ≤100-line allowance applies; beyond it, name the DECISION D15
stated cause and the mandated content behind the overage.
Repeat this Fortschritt line verbatim:
Fortschritt: ~88 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R51 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c erste Hälfte gebaut, Naht für die zweite in dieser Runde
gebaut, `_run_app_once` wird an R53 migriert · T002d entsperrt durch Amendment F085 D8, noch nicht
gebaut · T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round
is R53, which migrates `_run_app_once` in `packages/orchestration/dod_runners.py` onto the seam
this round adds, taking the CHILD half alone through `plan_child_spawn`, and rewrites the
`exec_guard` PARTIAL COVERAGE note in the same round because that note only becomes false when the
call site moves. T002d follows under the DECISION F085 D8 split, then T003, the integration gate
and closure. TWO: R52's own verdict is NOT on disk as a gate entry, because the round that records
a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that
absence is the terminator, not a missing gate, and R53 must not open a repair round to close it;
R52's verdict, when the reviewer issues it, is recorded by R53's OWN record slice. THREE: a
standalone closing line stating the open findings count and the next free id as its own sentence,
not only inside a gate transcript. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`,
because the self-drive protocol requires every handoff that names the next session's first action
to name that rule ahead of the Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN6F
## Current Step
R51, this round: T002c's first half. `_run_process_check` moves onto a new `dod-process` seam in
`packages/orchestration/exec_guard.py` that keeps the check's wall timeout and its cwd pin and
replaces the `env=os.environ.copy()` copy with an allowlist; four tests ship with it. The R50
PASS is recorded in the same round.

## Next Steps
1. T002c — `_run_app_once` in `packages/orchestration/dod_runners.py` under the dod-app policy:
   no wall timeout and network allowed, because it starts the app harness and probes it over
   HTTP. It takes the CHILD half alone through `plan_child_spawn`, since it owns its own
   parent-side deadline and writes the app's output to a file rather than to a pipe.
2. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, once three uses show its shape.
3. T003 — network posture, the limitations document, its README link. Then the integration gate,
   then closure.
END-PLAN6F

BEGIN-PLAN6T
## Current Step
R52, this round: the `dod-app` seam alone, in `packages/orchestration/exec_guard.py`. It takes no
wall timeout and no output cap — both are parent-side, and its caller owns its own deadline and
writes the app's output to a file. One test ships with it. Its caller migrates at R53, so the
module's PARTIAL COVERAGE note is untouched here and stays true. The R51 PASS is recorded in the
same round, with finding R-0554.

## Next Steps
1. T002c — migrate `_run_app_once` in `packages/orchestration/dod_runners.py` onto that seam,
   taking the CHILD half alone through `plan_child_spawn`, and rewrite the `exec_guard` coverage
   note in the same round, because only the call site's move makes that note false.
2. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, once three uses show its shape.
3. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.
END-PLAN6T

BEGIN-SEAM2


# ---------------------------------------------------------------------------
# The `dod-app` seam (F085 T002c) — the DoD's own application harness, which
# takes the CHILD half ALONE, because `_run_app_once` is already a supervisor.
# ---------------------------------------------------------------------------


#: WHY: the environment the DoD's application harness may inherit. The MEMBERS are
#: the `test`-class values and the NAME is deliberately separate, for the reason
#: `DOD_PROCESS_ENV_ALLOWLIST` states: T2_F085's policy table rules `dod-app` as its
#: own row, so widening one row stays a one-line edit here.
DOD_APP_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST


def dod_app_exec_policy(
    *,
    cwd: str | None,
    env: Mapping[str, str] | None = None,
    declared_env_keys: Sequence[str] = (),
) -> ExecGuardPolicy:
    """The stage-1 policy the DoD's application harness runs under.

    `wall_timeout_seconds` and `output_cap_bytes` are BOTH None, and that is the
    row T2_F085's table gives `dod-app` rather than an omission: the caller takes
    the CHILD half alone, owns its own deadline, stops the process family in a
    `finally`, and writes the app's output to a file rather than to a pipe. A
    second deadline would fight the first, and an output cap is enforced WHILE
    READING a pipe this guard never holds. Remedy deliberately does not bound that
    file here; T003's limitations document says so rather than letting the table's
    column imply a bound that is absent.

    `cpu_seconds`, `address_space_bytes` and `open_files` are None for the reasons
    `managed_builder_execution._builder_exec_policy` already settled for the
    builder class, not restated here so the two cannot drift apart.

    `env` is the CALLER's already-resolved environment and becomes the scrub
    SOURCE; `declared_env_keys` names the keys it adds on top of the parent's —
    for the coming caller, the project's runtime configuration plus `PORT`. Those
    keys JOIN the allowlist, so `scrub_child_env` keeps them while
    `FORBIDDEN_ENV_KEYS` stays the floor beneath both.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=None,
        output_cap_bytes=None,
        cwd=cwd,
        core_file_bytes=0,
        env=dict(env) if env is not None else None,
        env_allowlist=DOD_APP_ENV_ALLOWLIST + tuple(sorted(declared_env_keys)),
    )
END-SEAM2

BEGIN-TESTSGUARD2


def test_the_dod_app_policy_takes_neither_a_wall_timeout_nor_an_output_cap():
    """The two columns separating `dod-app` from every bounded class in T2_F085.

    Both are PARENT-side, and this policy's caller takes the CHILD half alone, so
    None here is the row the table rules rather than an omission. The declared
    keys are asserted to JOIN the allowlist rather than replace it, and
    `FORBIDDEN_ENV_KEYS` is asserted to survive a caller that names one.
    """
    policy = exec_guard.dod_app_exec_policy(
        cwd="/tmp/dod-app-cwd",
        env={"PATH": "/usr/bin", "PORT": "5173", "AWS_SECRET_ACCESS_KEY": "leak"},
        declared_env_keys=("PORT", "AWS_SECRET_ACCESS_KEY"),
    )

    assert policy.wall_timeout_seconds is None
    assert policy.output_cap_bytes is None
    assert policy.cwd == "/tmp/dod-app-cwd"
    assert policy.core_file_bytes == 0
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None
    assert set(exec_guard.DOD_APP_ENV_ALLOWLIST) <= set(policy.env_allowlist)
    assert "PORT" in policy.env_allowlist

    child_env = exec_guard.plan_child_spawn(policy).env
    assert child_env["PORT"] == "5173"
    assert child_env["PATH"] == "/usr/bin"
    assert "AWS_SECRET_ACCESS_KEY" not in child_env
END-TESTSGUARD2

BEGIN-RECORD20
Gate: R52 — the R51 entry. R51 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 3a64b65e..67475107, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r51.md`, the committed `.agent/authored/f085-r51.md` at
44a1fbde, the committed `.agent/last_block.md` at aa38f8c7 and both working copies as they stand
at 67475107 are all five byte-EQUAL at sha256
12c6771bf04c38f94be460b4beb48ed93ea5b37709ce1f70711f89a093703abc, 29295 B, 489 lines, 28 marker
lines — every figure measured on every copy. THE SHAPES HELD, each measured separately from slices
the reviewer extracted programmatically from the committed block by marker pair. THE FIVE REWRITES
each give `TO contains FROM: false` as that block declared, each FROM occurred exactly 1x in its
own pre-commit blob and 0x in its post-commit file with its TO exactly 1x: PLAN5F→PLAN5T in
`.agent/plan.md` at 051b4082 numstat `13 11`, HDRF→HDRT in
`packages/orchestration/exec_guard.py` at ff93b13a numstat `5 3`, and DOCF→DOCT, IMPF→IMPT and
SITEF→SITET in `packages/orchestration/dod_runners.py` at 44460d56 numstat `13 6`. THE PROSE
APPEND held for RECORD19 on `.agent/live_review.md` at 73489620: byte-exact prefix, a remainder of
exactly one blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 37 slice
lines — 0 empty — occurring exactly once among the 38 lines that commit adds, numstat `38 0`. THE
THREE CODE APPENDS held under the ORDERED EQUALITY §4.9 owes them since R-0531 — SEAM at fcfb2a0f
numstat `77 0`, TESTSDOD at 43cd292a numstat `52 0`, TESTSGUARD at 43cd292a numstat `22 0`: each
post-commit file equals `pre + slice` with NO joiner byte, each commit's added lines are exactly
that slice's lines IN ORDER, and 0 marker LINES reached any of the three. THE SUITES AND THE LINT
GATE WERE RE-RUN, NOT READ, in the primary checkout with the block's exact command lines, each
exit 0: the code suite `150 passed` against a base of 147, the four state readers `159 passed`
against 159, the canary `42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT
HELD at 051b4082: 43 lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap
F-id present. THE ARITHMETIC STOOD STILL AS ORDERED: 168 / 27 / 0 at both 3a64b65e and 67475107,
141 open at both, all three symmetric differences EMPTY, no duplicate id and no resolution naming
an unregistered id at either SHA. HYGIENE IS CLEAN: over the eight commits of 3a64b65e..67475107
that precede the handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1
fixes for the cap, are 489, 425, 13, 38, 5, 77, 13 and 74, and the handback commit adds 55; none
over 500; that range's path set measured before the handback is exactly the eight ordered paths
and nothing else; all nine commits are single-parent; the tree is clean and `git worktree list` is
one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 489, PROSE 226 and
RECORD19 37, agreeing with that block. THE TWO RED CONTROLS THAT BLOCK RECORDED WERE NOT TAKEN ON
TRUST: the reviewer re-ran both in a disposable worktree at 67475107 and removed it. Reverting
SITET to SITEF failed both new `dod_runners` tests and printed `AWS_SECRET_ACCESS_KEY` in the leak
test's own failure message; replacing the seam's `wall_timeout_seconds` with None failed the new
policy test AND the pre-existing `test_a_timeout_is_red_not_a_hang`, so the behaviour-equality
golden that block named really does hold the migration in place.

- R-0554 — `.agent/plan.md` claimed FOUR tests for a round that shipped THREE. Low. The R51 block
authored PLAN5T with the clause "four tests ship with it", and the round it described shipped
three: TESTSDOD defined two tests and TESTSGUARD one, which is also what the code suite measured
as `150 passed` against a base of 147. This is the class checklist item 16 names after R-0537 and
R-0543 — a sentence that quantifies what follows it, drifting because the numeral is the half
nobody re-reads — and it is the third instance of that class, in the same file R-0543 arrived in.
It is LOW and not Medium because no GATE ordered or reported the number: every gate R51 ordered is
reproducible and this reviewer reproduced all nine, so the miscount misled a reader of the plan
and never a verdict. The worker is not at fault; it applied the reviewer's slice byte-verbatim,
which is what constraint 1 required of it. C1 of the round carrying this registration retires the
clause as a side effect — PLAN6F spans the `## Current Step` section holding it and PLAN6T
describes R52 instead — so this finding is expected to be RESOLVED at the R52 gate rather than
repaired by a round of its own; `.agent/plan.md` states the CURRENT step and never a history, so
no appending correction under R-0520 is owed to it. Found and registered by the reviewer while
gating R51.
END-RECORD20
