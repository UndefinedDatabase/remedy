── STEP T002c second half, migration — F085 — R53 ────────────────────────────

Goal: migrate the harness spawn in `_run_app_once` (`packages/orchestration/dod_runners.py`) onto
the `dod-app` seam R52 added, taking the CHILD half ALONE through `plan_child_spawn`, rewrite the
`exec_guard` PARTIAL COVERAGE note in the same round because only this call site's move makes that
note false, and record the R52 PASS together with findings R-0555 and R-0556. The gap this closes
is `env=spec.resolved_env(port)`, which is `dict(os.environ)` plus the project's own overrides and
so hands a project-authored application the whole parent environment. T002c is COMPLETE at the end
of this round.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R52 and register R-0555 and R-0556 · C3 rewrite the exec_guard
coverage note · C4 migrate the call site · C5 append the test · C6 handback.

CONVENTION, binding on every count here. A line count is the `splitlines` reading — a trailing
newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE
INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE: extract it as everything after the
`BEGIN-` line's own newline up to and including the newline immediately before the `END-` line, so
that `pre + slice` is already a newline-terminated file and NO joiner and NO terminator byte is
ever added. This sentence is the R-0556 counter-measure and it is what makes G3's code-append
equality readable exactly one way. TESTSDOD2 is a CODE slice CARRYING its own leading blank lines,
so for it the post-commit file is `pre + slice` with nothing between them; RECORD21 is PROSE
joined to its target by exactly one blank line.

## Change

C1 applies PLAN7F→PLAN7T to `.agent/plan.md` and C2 appends RECORD21 to `.agent/live_review.md`.
C3 applies HDRF2→HDRT2 to `packages/orchestration/exec_guard.py`, that module's own PARTIAL
COVERAGE note: it currently says the DoD app harness still spawns unsupervised, and C4 makes that
false. C4 applies DOCF2→DOCT2, IMPF2→IMPT2 and SITEF2→SITET2 to
`packages/orchestration/dod_runners.py`: the module docstring's subprocess-discipline paragraph,
the import, and the call site. All three are rewrites, so one commit carries them with no append
proof. C5 appends TESTSDOD2 to `tests/orchestration/test_dod_runners.py`, whose pre-commit blob no
commit of this round has rewritten.

Change set, named rather than counted: `.agent/authored/f085-r53.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`packages/orchestration/dod_runners.py`, `tests/orchestration/test_dod_runners.py`,
`.agent/handoff.md`. Nothing else — `tests/orchestration/test_exec_guard.py` is NOT in this
round's change set, because R52 already landed the seam's own test. No `docs/roadmap/**` path is
in that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered; `.py`
files ARE in it, so a lint gate is, and G4 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r53.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one to a different wrap, and never add, rename or
   reorder a test the slices define. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C6; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit. This round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on each pair separately at emission against
   that file's blob at 3bafcc1e, and prints each pair's own output here per checklist item 15,
   none generalised to another: PLAN7F→PLAN7T `TO contains FROM: false`; HDRF2→HDRT2
   `TO contains FROM: false`; DOCF2→DOCT2 `TO contains FROM: false`; IMPF2→IMPT2
   `TO contains FROM: false`; SITEF2→SITET2 `TO contains FROM: false`. All five are therefore
   REWRITES and each owes the FROM 0x / TO 1x reading over its whole post-commit file. PLAN7F
   spans the `## Current Step` section AND the WHOLE `## Next Steps` list rather than a prefix of
   either, because its TO drops the completed item and so changes that list's arity (checklist
   item 17). RECORD21 and TESTSDOD2 are APPENDS carrying no FROM, so no containment reading is
   owed for either. Each of the five FROM texts occurs EXACTLY 1x in its target at 3bafcc1e — the
   reviewer measured all five — so none is ambiguous.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of every code commit. Only
   C0a and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23
   binds it.
5. Every sentence in RECORD21 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD21 lands, which is why the SHA and never the
   present tense carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested each of the five FROM texts
   against every later-applied text at emission and got NO hits, so each G3 FROM-0x reading stays
   attainable (checklist item 2, whose failure mode is a TO that quotes retired text on purpose).
7. Nothing outside the declared change set is touched. This round REGISTERS R-0555 and R-0556 and
   resolves nothing, so the registered count rises by two, the done count is unchanged and the
   open count rises from 142 to 144; the next free id becomes R-0557. `.agent/plan.md` after C1 is
   42 lines, which the reviewer projected mechanically by applying the pair to that file's blob at
   3bafcc1e.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never
   widen the change set to route around a red.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 429, PROSE 231, RECORD21 62. The worker
   re-measures all three from the committed `.agent/authored/f085-r53.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. THE REVIEWER ALREADY RAN THIS ROUND'S RED CONTROL, at 3bafcc1e, in a disposable worktree it
   removed afterwards, with these exact slice bytes applied by the extraction ordered above.
   Reverting SITET2 to SITEF2 failed the new `dod_runners` test, and its own failure message
   printed `AWS_SECRET_ACCESS_KEY` as the child had received it. Bytecode caching was disabled for
   that run, because two same-length mutations written inside one second otherwise reuse a stale
   `.pyc` and the second probe silently reprints the first one's assertion — the blind-probe class
   checklist item 12 names. DO NOT repeat the control: it is recorded here so this round needs no
   worktree, and G2 plus G3 are what carry that reading onto the worker's own commits.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty
at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r53.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r53.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The five REWRITES of constraint 3: in each post-commit file the FROM occurs 0x and the TO
   exactly 1x. Report both counts and `git show --numstat` per path per commit.
 - C2 / RECORD21 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies in its PROSE form: every non-empty line the slice
   contains occurs exactly once among the lines C2's diff adds TO THAT PATH.
 - C5 / TESTSDOD2 is a CODE APPEND, so §4.9 as R-0531 narrows it orders ORDERED EQUALITY rather
   than a per-line count: the pre-commit blob is a byte-exact PREFIX of the post-commit file, the
   slice is an exact SUFFIX, the post-commit file equals `pre + slice` with NO byte between them
   and none appended after — the CONVENTION above makes the slice newline-terminated already — the
   lines that commit's diff adds TO THAT PATH are exactly the slice's lines IN ORDER, and 0 marker
   LINES reach the file. Report `git show --numstat` for that path.

G4 LINT, the repository's own configuration and never `--isolated`, exit 0:
`python3 -m ruff check packages/orchestration/exec_guard.py
packages/orchestration/dod_runners.py tests/orchestration/test_dod_runners.py` — base reading at
3bafcc1e, taken by the reviewer with this exact command line: `All checks passed!`, exit 0.
`pyproject.toml` enables the `I` rules, so IMPT2's multi-name `exec_guard` import block is checked
for sorting by this gate, not by eye.

G5 CODE SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_dod_runners.py
tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf` — the
file this round edits plus the two modules whose behaviour the migration must leave untouched.
Base at 3bafcc1e, taken by the reviewer in the primary checkout: `151 passed`. TESTSDOD2 adds one
test, so a green run reads `152 passed`; REPORT the number this run prints.

G6 STATE READERS, primary checkout, exit 0: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
ordered because C1 rewrites `.agent/plan.md`, which two of them assert on. Base at 3bafcc1e:
`159 passed`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base at 3bafcc1e
`42 passed`. REPORT both numbers.

G7 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each of
the three booleans. G6 covers the first three through their tests; this gate covers the cap.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
3bafcc1e and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 169 / 27 / 0, 142 open, max registered R-0554, max resolved
R-0532. At HEAD the registered count must read 171, the done count must be UNCHANGED at 27 and the
landed count UNCHANGED at 0; the registered symmetric difference must be exactly R-0555 and R-0556
while the done and landed symmetric differences are EMPTY, because this round registers those two
ids and resolves nothing; 144 open, next free id R-0557. Report the three symmetric differences,
the duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only 3bafcc1e..HEAD` measured BEFORE C6 holds exactly the change set
above minus `.agent/handoff.md`, which C6 writes, and nothing else — and in particular does NOT
hold `tests/orchestration/test_exec_guard.py`. Report per-commit insertions for every commit
BEFORE C6 — C6 cannot measure itself, so its own insertions go in the round report — and confirm
none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a
second oversize commit is a STOP under constraint 8, never a declaration. Confirm every commit has
exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 3bafcc1e, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4, C5 and C6, the real G1-G9 results with exit codes, the open-findings count and the next
expected action. This round's Bundle names seven commits, which is more than five, so the
≤100-line allowance applies; beyond it, name the DECISION D15 stated cause and the mandated
content behind the overage.
Repeat this Fortschritt line verbatim:
Fortschritt: ~91 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R52 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT in dieser Runde · T002d entsperrt durch
Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round
is R54, which implements T002d under the DECISION F085 D8 split — `runtime-server` takes no wall
timeout and `runtime-build` keeps the one it already has; that round also extracts the guard-result
translation the `test` and `dod-process` seams each carry, now that three uses show its shape.
Then T003, the integration gate and closure. TWO: R53's own verdict is NOT on disk as a gate
entry, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing
gate, and R54 must not open a repair round to close it; R53's verdict, when the reviewer issues
it, is recorded by R54's OWN record slice. THREE: a standalone closing line stating the open
findings count and the next free id as its own sentence, not only inside a gate transcript.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of the
Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN7F
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
END-PLAN7F

BEGIN-PLAN7T
## Current Step
R53, this round: T002c's migration, which COMPLETES T002c. `_run_app_once` in
`packages/orchestration/dod_runners.py` takes the CHILD half alone through `plan_child_spawn`
under the `dod-app` seam R52 landed, so the whole-parent-environment copy it passed becomes an
allowlist. The `exec_guard` PARTIAL COVERAGE note is rewritten in the same round, because only
this call site's move makes it false. One test ships with it. The R52 PASS is recorded in the same
round, with findings R-0555 and R-0556.

## Next Steps
1. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, now that three uses show its shape.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.
END-PLAN7T

BEGIN-HDRF2
  through `run_guarded_test_command`; and since T002c the DoD's bounded process
  checks run through `run_guarded_dod_process_command`, while the DoD app
  harness and the runtime, git and packaging classes still spawn unsupervised.
  No count is written here on purpose: it changes with every migration round,
  and the caller grep is the honest answer.
END-HDRF2

BEGIN-HDRT2
  through `run_guarded_test_command`; and since T002c the DoD class is migrated
  whole — its bounded checks through `run_guarded_dod_process_command`, and its
  application harness through the CHILD half of `dod_app_exec_policy` — while
  the runtime, git and packaging classes still spawn unsupervised. No count is
  written here on purpose: it changes with every migration round, and the caller
  grep is the honest answer.
END-HDRT2

BEGIN-DOCF2
Since F085 T002c the single-process kinds spawn through
``exec_guard.run_guarded_dod_process_command``, so the environment is no longer
inherited as-is: a child receives only allowlisted keys, never a secret-like
variable. The harness spawn in ``_run_app_once`` is still bare — it is the
second half of T002c, under the ``dod-app`` policy.
END-DOCF2

BEGIN-DOCT2
Since F085 T002c no kind here spawns bare. The single-process kinds go through
``exec_guard.run_guarded_dod_process_command``, and the harness spawn in
``_run_app_once`` takes the CHILD half of ``exec_guard.dod_app_exec_policy``, so
the environment is no longer inherited as-is: a child receives only allowlisted
keys plus the keys the project's own runtime configuration declares, never a
secret-like variable. What the CHILD half does NOT carry is the parent-side
pair — no wall timeout and no output cap — because ``_run_app_once`` owns its
own deadline and writes the app's output to a file rather than to a pipe.
END-DOCT2

BEGIN-IMPF2
from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.exec_guard import run_guarded_dod_process_command
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
END-IMPF2

BEGIN-IMPT2
from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.exec_guard import (
    dod_app_exec_policy,
    plan_child_spawn,
    run_guarded_dod_process_command,
)
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
END-IMPT2

BEGIN-SITEF2
                proc = subprocess.Popen(  # noqa: S603 - argv list, never a shell
                    argv, cwd=spec.cwd, env=spec.resolved_env(port),
                    stdout=handle, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    # Its own session, so the family can be killed whole without
                    # this process signalling itself — the supervisor's rule.
                    start_new_session=True,
                )
END-SITEF2

BEGIN-SITET2
                # The guard owns the CHILD half of this spawn since F085 T002c:
                # the rlimits, the cwd pin and an allowlisted environment,
                # resolved between fork and exec. The PARENT half stays HERE —
                # this function owns its own `deadline`, stops the family in a
                # `finally`, and writes the app's output to a file rather than
                # to a pipe — so the policy carries no wall timeout and no
                # output cap, and a second deadline never fights this one.
                plan = plan_child_spawn(dod_app_exec_policy(
                    cwd=spec.cwd,
                    env=spec.resolved_env(port),
                    declared_env_keys=tuple(spec.env) + ("PORT",),
                ))
                proc = subprocess.Popen(  # noqa: S603 - argv list, never a shell
                    argv, cwd=plan.cwd, env=plan.env,
                    preexec_fn=plan.preexec_fn,
                    stdout=handle, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    # Its own session, so the family can be killed whole without
                    # this process signalling itself — the supervisor's rule.
                    start_new_session=True,
                )
END-SITET2

BEGIN-TESTSDOD2


class TestTheDodAppSeam:
    """The harness spawn takes the CHILD half of the `dod-app` policy.

    `Popen` is captured and made to fail before exec, so no application starts
    and no process survives this test: `_run_app_once` documents that path as
    `REASON_APP_START_FAILED`, and what is judged here is the spawn the function
    was given rather than the red evidence that path then produces.
    """

    def test_the_harness_spawn_takes_the_child_half_of_the_dod_app_policy(
            self, tmp_path: Path, monkeypatch):
        from packages.orchestration import dod_runners

        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "f085-must-not-leak")
        monkeypatch.setenv("F085_NOT_ALLOWLISTED", "f085-must-not-leak")
        root = tmp_worktree(tmp_path / "app")
        write_runtime_config(root, cmd=[sys.executable, "flow_app.py"],
                             env={"F085_DECLARED": "kept"})
        seen: dict = {}

        def _capture(argv, **kwargs):
            seen.update(argv=list(argv), kwargs=kwargs)
            raise OSError("captured before exec")

        monkeypatch.setattr(dod_runners.subprocess, "Popen", _capture)
        ev = run_check(
            flow({"action": "open", "path": "/health", "expect_status": 200}),
            root, timeout_sec=60)

        child_env = seen["kwargs"]["env"]
        assert "AWS_SECRET_ACCESS_KEY" not in child_env
        assert "F085_NOT_ALLOWLISTED" not in child_env
        assert "PATH" in child_env
        assert child_env["F085_DECLARED"] == "kept"
        assert child_env["PORT"].isdigit()
        assert Path(seen["kwargs"]["cwd"]).resolve() == root.resolve()
        assert callable(seen["kwargs"]["preexec_fn"])
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_APP_START_FAILED
END-TESTSDOD2

BEGIN-RECORD21
Gate: R53 — the R52 entry. R52 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 67475107..3bafcc1e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r52.md`, the committed `.agent/authored/f085-r52.md` at
a7896384, the committed `.agent/last_block.md` at 216fe178 and both working copies as they stand
at 3bafcc1e are all five byte-EQUAL at sha256
dbb09a909d14afe36d188f834eba2698f195ac502d2372f92e0f89d5bda554b8, 25680 B, 373 lines, 10 marker
lines, and that digest is the one the R52 block itself carried — every figure measured on every
copy. THE SHAPES HELD. The single REWRITE PLAN6F→PLAN6T in `.agent/plan.md` at 511736d6 gives
`TO contains FROM: false`, its FROM occurred 1x in the pre-commit blob and 0x after with its TO
exactly 1x, numstat `11 10`. THE PROSE APPEND RECORD20 on `.agent/live_review.md` at 23a7ec30:
byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix, 0 marker
LINES, and each of its 54 non-empty slice lines occurring exactly once among the 56 lines that
commit adds, numstat `56 0`. THE TWO CODE APPENDS held under ORDERED EQUALITY — SEAM2 at d5b1c8f6
numstat `50 0` and TESTSGUARD2 at 610fd945 numstat `30 0`: each post-commit file equals
`pre + slice` with NO byte between them, each commit's added lines are exactly that slice's lines
IN ORDER, and 0 marker LINES reached either. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ,
in the primary checkout with the block's exact command lines, each exit 0: the code suite
`151 passed` against a base of 150, the four state readers `159 passed` against 159, the canary
`42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at 511736d6: 44
lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 44 is
the figure that block projected. THE ARITHMETIC MOVED AS ORDERED: 169 / 27 / 0 at 3bafcc1e against
168 / 27 / 0 at 67475107, 142 open against 141, the registered symmetric difference exactly
R-0554, done and landed symmetric differences EMPTY, no duplicate id and no resolution naming an
unregistered id at either SHA. HYGIENE IS CLEAN: over the six commits of 67475107..3bafcc1e that
precede the handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes
for the cap, are 373, 255, 11, 56, 50 and 30, and the handback commit adds 38; none over 500; that
range's path set measured before the handback is exactly the six ordered paths and does NOT hold
`packages/orchestration/dod_runners.py`, which that round's change set excluded; all seven commits
are single-parent; the tree is clean and `git worktree list` is one line. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 373, PROSE 205 and RECORD20 55, agreeing with that
block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds: it states 86 lines and measures 86,
inside the ≤100 allowance a seven-commit round carries.

- R-0555 — the R52 block's Handback section said "Six commits" over a Bundle naming seven. Low.
That block's Bundle names C0a, C0b, C1, C2, C3, C4 and C5, and its Handback section then wrote
"Six commits, so the ≤100-line allowance applies". This is checklist item 16's class as R-0537 and
R-0543 widened it — a sentence that quantifies what follows it, drifting because the numeral is
the half nobody re-reads — arriving in the reviewer's own block one round after R-0554 registered
the same class against `.agent/plan.md`. It is LOW because the allowance it computes is identical
either way: the threshold is more than five commits and both readings clear it, so no gate and no
cap moved. The worker read the Bundle rather than the sentence, wrote "Seven commits" in the
handback, and flagged the contradiction instead of silently following either half — which is the
behaviour the block wants. Found by the worker, registered by the reviewer while gating R52.

- R-0556 — a block's slice convention did not say whether a slice INCLUDES its terminating
newline, so the worker's extraction and the block's definition disagreed. Low. The R52 block's
CONVENTION said only that "a slice is the bytes strictly between its marker lines" and that a
trailing newline is not an extra line. Under the reading that a slice ends with the newline
terminating its last content line, `post == pre + slice` holds exactly for SEAM2 at d5b1c8f6 and
TESTSGUARD2 at 610fd945, which is what the reviewer measured at 3bafcc1e; under an extraction that
joins the inner lines WITHOUT a trailing newline it does not, and the worker therefore appended one
and declared an assumption for it. BOTH ROUTES PRODUCED IDENTICAL BYTES ON DISK, so nothing landed
wrong and G4 stayed green either way; what the gap cost was a declared assumption on a round that
did nothing wrong, and it put into the handback the absolute claim that `post == pre + slice` does
not hold at fcfb2a0f, which is false under the block's own convention and true only under the
worker's unstated one. This is the newline class the reviewer's own notes already carry — one
newline shifts both slice counts and pair shape — recurring because the convention sentence stated
the units without pinning the boundary. THE COUNTER-MEASURE IS IN THE R53 BLOCK'S OWN CONVENTION
paragraph, which states newline-inclusion explicitly and says that no joiner and no terminator byte
is ever added; that is the block carrying this registration. Found by the worker's declared
assumption, registered by the reviewer while gating R52.
END-RECORD21
