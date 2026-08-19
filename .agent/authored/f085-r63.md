── STEP T002e final call site — F085 — R63 ───────────────────────────────────

Goal: migrate the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, onto
`plan_child_spawn`, so the Remedy supervisor the CLI launches inherits the allowlist plus the three
`REMEDY_*` keys it declares and nothing else — and pin that handover with a test that goes red when
the scrub is reverted. The R62 PASS is recorded in the same round, because a round cannot record a
verdict on itself (docs/agents/planner_reviewer_prompt.md §4.13). This closes T002e.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 record the R62 PASS · C3 migrate the call site · C4 add the pin · C5 handback. That list runs
past C0a, C0b, C1, C2, C3, C4 to C5, so it holds MORE than five commits and the handback takes the
≤100-line cap AGENTS.md allows when a per-commit table needs it.

CONVENTION, binding on every count here, carried verbatim in force from the R62 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO REWRITE PAIRS ARE PLAN17 AND
SITE4; ITS END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD31 AND TESTCLI — listed rather
than counted, per §3 checklist item 11. Each append slice CARRIES ITS OWN LEADING BLANK LINES, so
the separation its target's convention requires is a property of bytes that were measured and never
of a join shape that was reasoned about.

## Change

C1 applies PLAN17F→PLAN17T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep
a stale label. C2 appends RECORD31 to the END of `.agent/live_review.md`. C3 applies SITE4F→SITE4T
to `apps/cli/commands/runtime_cmd.py`, inside `_serve_supervisor`. C4 appends TESTCLI to the END of
`tests/cli/test_runtime_cmd.py`.

Change set, named rather than counted: `.agent/authored/f085-r63.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `apps/cli/commands/runtime_cmd.py`,
`tests/cli/test_runtime_cmd.py`, `.agent/handoff.md`. Nothing else. NO `docs/roadmap/**` path is in
that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered. TWO `.py` paths
ARE in it, so a lint gate IS ordered and a red control IS ordered. `packages/runtimes/dev_server.py`
and `packages/runtimes/runtime_supervisor.py`, the two sites R61 migrated, are NOT in the set and
this round must not touch them. All four paths named in this paragraph — the two edited `.py` files
and those two — were resolved on disk at cbe1b3e5 with `git ls-tree`, one call per path, before this
block was emitted, per §3 checklist item 24, and all four exist.

WHY the declared keys are these three, settled by reading before this block was written, which is
the question the R62 handback left open. `PYTHONPATH` and `VIRTUAL_ENV` are ALREADY members of
`RUNTIME_SERVER_ENV_ALLOWLIST` — it is `TEST_COMMAND_ENV_ALLOWLIST` by assignment, and both keys
appear in that tuple in `packages/orchestration/exec_guard.py` at cbe1b3e5 — so the `python -m`
import from the Remedy checkout needs NOTHING declared on top of the allowlist and this block
declares neither. The three keys that ARE declared are the supervisor's own control variables:
`REMEDY_RUNTIME_PORT`, which the supervisor reads with `os.environ[...]` and dies without;
`REMEDY_RUNTIME_LOG_MAX`, which it reads with `os.environ.get`; and `REMEDY_DATA_DIR`, which it
resolves `projects_dir()` through. None of the three is a `FORBIDDEN_ENV_KEYS` member, so the floor
does not take them back.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r63.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   cbe1b3e5 and prints its own output here per checklist item 15, one reading per pair:
   PLAN17F→PLAN17T `TO contains FROM: false`; SITE4F→SITE4T `TO contains FROM: false`. BOTH are
   therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file. Each
   FROM occurs EXACTLY 1x in its target at cbe1b3e5 — the reviewer measured both.
4. RECORD31 AND TESTCLI HAVE NO FROM. Each is appended at the END of its target. Their obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for either and do not report a FROM
   count. TESTCLI is CODE, so the per-line "each TO-ONLY addition exactly 1x" count of §4.9 does NOT
   bind it and must not be reported — ordered equality replaces it, which is why R-0531 exists.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both code commits. Only C0a
   and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. Every sentence in RECORD31 that states a reading of a file names the SHA it was read at in the
   same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to
   EVERY reading in the clause, not only the first. RECORD31 states readings of R62's range only,
   all of which are prior state, so every SHA it names already exists when it is written.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD31 is reviewer text. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD31 to reconcile it with
   anything you measure. A disagreement between RECORD31 and your own reading is a finding to REPORT
   in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. The reviewer re-executed every R62 gate and
   found nothing to register. Registered stays 174, done stays 28, landed stays 0, open stays 146,
   and the next free id stays R-0560. RECORD31 is a `Gate:` paragraph and carries no `- R-`
   registration line and no `Done:` line, which is why the arithmetic must not move; G6 proves it.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and reports them in G2. The worker re-measures all three from the
   committed `.agent/authored/f085-r63.md` and reports them; a mismatch is a finding against this
   block, not against the worker.
10. C3 AND C4 ARE SEPARATE COMMITS and land in that order. C3 alone leaves the suite green — the
   reviewer verified that in a disposable worktree at cbe1b3e5 — so neither commit is knowingly red.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. This round DOES order a destructive check (G8), so
`git worktree list` is one line at round start, one line again at the end, and the worktree G8
creates is removed and pruned before the handback is written.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r63.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each, measured on every copy. Also report the block's TOTAL, PROSE and
RECORD31 line counts read from that committed file, against the 490 / 400 / 140 figures in
constraint 9. Do not name or read any path outside the repository's tracked tree.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN17F→PLAN17T is a REWRITE over `.agent/plan.md` at C1: report its FROM 0x and its TO exactly
   1x over the post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must
   reproduce the post-commit blob BYTE-EXACTLY.
 - SITE4F→SITE4T is a REWRITE over `apps/cli/commands/runtime_cmd.py` at C3: the same three
   readings, measured over that file's own pre- and post-commit blobs.
 - For RECORD31 at C2 and TESTCLI at C4 report the ordered-equality readings constraint 4 names:
   pre-commit blob is a byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the
   post-commit blob byte for byte, and that commit's ADDED lines are exactly the slice's lines IN
   ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0. Report each run's
passed count; the counts are reported, never predicted, and only the exit code is ordered. The
reviewer took every base reading below itself, in the primary checkout, at cbe1b3e5.
 - `python3 -m pytest tests/runtimes/ tests/cli/test_runtime_cmd.py
   tests/orchestration/test_exec_guard.py -q -rf` — base `304 passed`, no skips. C4 adds exactly one
   test to `tests/cli/test_runtime_cmd.py`, whose own base is `16 passed`.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites, and that is the whole reason this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 39 lines mechanically by applying the pair to that file's blob at cbe1b3e5.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
cbe1b3e5 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558. At HEAD the reading must be IDENTICAL — 174 / 28 / 0, 146 open, same two maxima — and all
three symmetric differences must be EMPTY, because constraint 8 rules this round registers and
resolves nothing. Next free id R-0560. Report all three symmetric differences, the duplicate-id
count and the count of resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the two `.py` paths this round edits, run from the repository root with the
repository's OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green at
the base, so both are ordered GREEN rather than compared as multisets; the reviewer executed both at
cbe1b3e5 itself, per R-0364, and both printed `All checks passed!`.
 - `python3 -m ruff check apps/cli/commands/runtime_cmd.py tests/cli/test_runtime_cmd.py` — exit 0.
 - `python3 -m ruff check --preview apps/cli/commands/runtime_cmd.py
   tests/cli/test_runtime_cmd.py` — exit 0. The preview half is ordered separately because ruff is
   preview-blind to the E301-E306 class that a code append most plausibly breaks (R-0500, R-0558).

G8 RED CONTROL, the ONLY destructive check this round, and ONLY inside a disposable `git worktree`
at HEAD under §4.10 — never in the primary checkout. In that worktree revert EXACTLY ONE thing: the
single line `            cwd=spawn_plan.cwd, env=spawn_plan.env,` back to
`            cwd=str(source_root), env=env,`, changing nothing else, and re-run
`python3 -m pytest tests/cli/test_runtime_cmd.py -q -rf`. The run must FAIL, and the failure must be
`test_a_secret_parent_variable_never_reaches_the_supervisor` failing on its
`assert "ANTHROPIC_API_KEY" not in env` line, with the other tests in that file still passing.
Report the failing test's full name and the asserted line. The reviewer ran this control itself at
emission and saw exactly that, and separately ran the un-reverted test 10 times, all 10 green, so
the colour is ordered rather than probed (the stability rule the F085 R6 lesson fixed). Then remove
and prune the worktree and confirm `git status --porcelain` empty in the primary checkout.

G9 HYGIENE. `git diff --name-only cbe1b3e5..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds neither
`packages/runtimes/dev_server.py` nor `packages/runtimes/runtime_supervisor.py`. Those two paths and
the two `.py` paths this round edits were each resolved on disk at cbe1b3e5 with
`git ls-tree cbe1b3e5 -- <path>`, one call per path, and all four exist; re-run those four calls and
report each result, per §3 checklist item 24. Report per-commit insertions for every commit BEFORE
C5 — C5 cannot measure itself, so its own insertions go in the round report — and confirm none
exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second
oversize commit is a STOP under constraint 11, never a declaration. Confirm every commit is
single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA cbe1b3e5, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3,
C4 and C5, the real G1-G9 results with exit codes, the open-findings count and the next expected
action. The Bundle above holds more than five commits, so the ≤100-line cap applies; if the mandated
content genuinely does not fit even there, name the DECISION D15 stated cause and the specific
mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R62 PASS · T002a-T002d KOMPLETT · T002e KOMPLETT — die
`runtime-server`-Policy gebaut und ALLE drei Call-Sites migriert, die letzte mit einem
Popen-Seam-Test gepinnt, der ohne den Scrub rot wird · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: T002e is COMPLETE
— all three `runtime-server` call sites now take `plan_child_spawn` — so the next round is R64,
which starts T003: the network posture, the limitations document and its README link. That document
must state what the CHILD-half migrations do NOT bound, naming both cases the R62 plan already
recorded: an app log written to a file takes no guard output cap, and a build behind an HTTP proxy
does not run under the guard at all, because the proxy variables are `FORBIDDEN_ENV_KEYS` members
and the floor is not a row's to lift. TWO: R63 carries no verdict of its own, because the round that
records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R64
carries it. THREE: a standalone closing line stating the open findings count and the next free id as
its own sentence. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive
protocol requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN17F
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
END-PLAN17F

BEGIN-PLAN17T
## Current Step
R63, this round: the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, takes
`plan_child_spawn`, so the Remedy supervisor the CLI launches inherits the allowlist plus the
three `REMEDY_*` keys it declares and nothing else. A test pins that handover at the `Popen`
seam, which is the only place it can be observed. The R62 PASS is recorded in the same round.

## Next Steps
1. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
2. Then the integration gate, then closure.
END-PLAN17T

BEGIN-SITE4F
    env = dict(os.environ)
    env["REMEDY_RUNTIME_PORT"] = str(port)
    source_root = Path(__file__).resolve().parents[3]      # the Remedy checkout

    try:
        proc = subprocess.Popen(          # noqa: S603 - argv, never a shell
            [_sys.executable, "-m", "packages.runtimes.runtime_supervisor",
             "--repo", str(root), "--spec", str(spec_file), "--handshake", str(hs),
             "--instance", instance_id],
            cwd=str(source_root), env=env,
END-SITE4F

BEGIN-SITE4T
    env = dict(os.environ)
    env["REMEDY_RUNTIME_PORT"] = str(port)
    source_root = Path(__file__).resolve().parents[3]      # the Remedy checkout
    # F085 T002e: the CHILD half of the `runtime-server` policy, the LAST of the three
    # call sites. This child is the Remedy supervisor itself, not a project application,
    # so the keys it declares are its OWN `REMEDY_RUNTIME_*` control variables plus the
    # data root it resolves `projects_dir()` through. `PYTHONPATH` and `VIRTUAL_ENV` are
    # already `RUNTIME_SERVER_ENV_ALLOWLIST` members, so the `python -m` import from the
    # Remedy checkout needs nothing declared on top.
    from packages.orchestration.exec_guard import (
        plan_child_spawn,
        runtime_server_exec_policy,
    )
    spawn_plan = plan_child_spawn(runtime_server_exec_policy(
        cwd=str(source_root),
        env=env,
        declared_env_keys=("REMEDY_DATA_DIR", "REMEDY_RUNTIME_LOG_MAX",
                           "REMEDY_RUNTIME_PORT"),
    ))

    try:
        proc = subprocess.Popen(          # noqa: S603 - argv, never a shell
            [_sys.executable, "-m", "packages.runtimes.runtime_supervisor",
             "--repo", str(root), "--spec", str(spec_file), "--handshake", str(hs),
             "--instance", instance_id],
            cwd=spawn_plan.cwd, env=spawn_plan.env,
            preexec_fn=spawn_plan.preexec_fn,  # rlimits between fork and exec
END-SITE4T

BEGIN-TESTCLI


class TestTheSupervisorEnvironmentIsScrubbed:
    """F085 T002e — what the supervisor child really inherits from the CLI.

    The supervisor is spawned to DEVNULL and dumps no environment of its own, so
    the handover can only be observed at the `Popen` call. The recorder DELEGATES
    to the real one, so the runtime still comes up and these assertions describe a
    spawn that actually served rather than a call that was intercepted.
    """

    def test_a_secret_parent_variable_never_reaches_the_supervisor(
            self, tmp_path, capsys, monkeypatch):
        import subprocess

        seen: dict = {}
        real_popen = subprocess.Popen

        def recording_popen(argv, **kwargs):
            if any("runtime_supervisor" in str(a) for a in argv):
                seen.update(kwargs)
            return real_popen(argv, **kwargs)

        monkeypatch.setattr(subprocess, "Popen", recording_popen)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-must-not-travel")
        monkeypatch.setenv("REMEDY_UNDECLARED_MARKER", "must-not-travel")

        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        out = json.loads(capsys.readouterr().out)
        try:
            assert out["ok"] is True                        # it really served
            env = seen["env"]
            assert "ANTHROPIC_API_KEY" not in env           # the guard's floor held
            assert "REMEDY_UNDECLARED_MARKER" not in env    # the allowlist bound
            assert "PATH" in env                            # the allowlist held
            assert env["REMEDY_RUNTIME_PORT"] == str(out["port"])
            assert env["REMEDY_DATA_DIR"] == str(tmp_path / "remedy_data")
            assert seen["preexec_fn"] is not None            # rlimits between fork and exec
        finally:
            runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
            capsys.readouterr()
END-TESTCLI

BEGIN-RECORD31

Gate: R63 — the R62 entry. R62 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer over
a05669a5..cbe1b3e5, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk
with no digest fallback, though NOT against a reviewer scratchpad original: R62 was authored by an
earlier session and this one holds no original of it, so the comparison ran across the six copies
that do exist — the committed `.agent/authored/f085-r62.md` at 37114518 and at cbe1b3e5, the
committed `.agent/last_block.md` at aa9b94e8 and at cbe1b3e5, and both working copies as they stand
at cbe1b3e5 — all six byte-EQUAL at sha256
ad6827dc70e67bd8d007666fa379345ea4c318b9a62ac58baa19ceb10a4ead50, 19619 B, 256 lines, 6 marker
lines. What binds that block's CONTENT is the shape proof rather than the digest, and it held. THE
SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN16F→PLAN16T is a
REWRITE — its containment test reads `TO contains FROM: false` — and over `.agent/plan.md` at
3d754312 it ends FROM 0x with TO exactly 1x, its FROM having occurred exactly 1x in that file at
aa9b94e8, and re-applying the extracted pair to the pre-commit blob reproduces the post-commit blob
BYTE-EXACTLY. RECORD30, which has no FROM, satisfies ORDERED EQUALITY on every clause over
`.agent/live_review.md` at 5cced41e: the pre-commit blob at 3d754312 is a byte-exact PREFIX, the
slice is an exact SUFFIX, `pre + slice` equals the post-commit blob byte for byte, and that commit's
ADDED lines equal the slice's lines IN ORDER, 50 and 50, numstat `50 0`. Marker LINES at cbe1b3e5
are 0 in `.agent/plan.md`, in `.agent/live_review.md` and in `.agent/handoff.md`. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with that block's exact command lines, each exit 0: the
four state readers `160 passed` against a base of `160 passed`, and the canary `42 passed` against a
base of `42 passed`, both unchanged because that round changed no code. THE PLAN CONTRACT HELD at
cbe1b3e5: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 44 being the figure that block projected. THE ARITHMETIC DID NOT MOVE, as constraint 8 of
that block required: 174 registered / 28 done / 0 landed and 146 open at a05669a5, the same three
numbers and the same 146 at cbe1b3e5, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 resolutions naming an unregistered id at
both SHAs. HYGIENE IS CLEAN: the path set over a05669a5..cbe1b3e5 is exactly the five the change set
named, holds no `.py` path at all, and holds `apps/cli/commands/runtime_cmd.py` not at all;
per-commit INSERTIONS are 256, 166, 7, 50 and 30 for the handback commit, none over 500; all five
commits are single-parent; and `.agent/handoff.md` at cbe1b3e5 is 60 lines, within its own cap, with
the ordered Fortschritt line present verbatim. THE BLOCK'S OWN SIZE re-measured from the committed
file at cbe1b3e5 gives TOTAL 256, PROSE 172 counting its 6 marker lines and RECORD30 50, agreeing
with that block's own figures and under 490 / 400 / 140. ONE CLAIM NO GATE COVERED WAS CHECKED
RATHER THAN ACCEPTED: the R62 handback's open question, whether the supervisor needs `PYTHONPATH`
and `VIRTUAL_ENV` declared, was settled by reading `packages/orchestration/exec_guard.py` at
cbe1b3e5, where both keys are already members of the tuple `RUNTIME_SERVER_ENV_ALLOWLIST` is
assigned from, so R63 declares neither. NOTHING FAILED and this round registers no finding.
END-RECORD31
