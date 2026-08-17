── STEP T002b seam capability — F085 — R39 ───────────────────────────────────

Goal: record the R38 PASS, register R-0530, and implement DECISION F085 D3 — an
`extra_env` overlay on the `test`-class seam, so a call site can SET a variable the
parent does not have. No call site is migrated; R40 does that.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R38
and register R-0530 · C2 the seam overlay and its tests · C3 the plan · C4 handback.

## Change

C1 appends RECORD7 to `.agent/live_review.md` and nothing else. C2 applies four pairs to
`packages/orchestration/exec_guard.py` plus one append to
`tests/orchestration/test_exec_guard.py`, in one commit — the code DECISION F085 D3
authorises, which C2 of R38 put on disk at 275a294e. C3 applies the `.agent/plan.md`
pair.

Change set, named rather than counted: `.agent/authored/f085-r39.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/plan.md` and `.agent/handoff.md`.
Nothing else. No file under `docs/` changes, so no `tests/docs/` gate is ordered.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r39.md` by its marker pair. Never retype one, never apply one
   from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair — SEAMA→SEAMB, SEAMC→SEAMD, SEAME→SEAMF,
   SEAMG→SEAMH and PLANF7→PLANT7 each read `TO contains FROM: false`, so each is a
   REWRITE and each is owed the FROM 0x / TO 1x reading. Each FROM was measured to occur
   exactly 1x in its target at cbcb5c23. RECORD7 and SEAMTESTS are appends, carry no
   FROM, and are owed the §4.9 append obligation instead.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists, finish
   the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. Any red
   proof you run on your own initiative goes in a disposable worktree under
   `.remedy-wt/`, removed and pruned before the handback; the primary checkout is never
   mutated for a check.
5. C1 and C2's test-file half are APPENDS: each pre-commit file stays a byte-exact
   prefix and neither is reflowed, re-wrapped or re-indented. RECORD7 is joined by one
   blank line. SEAMTESTS is joined so that EXACTLY two blank lines separate the test
   file's last existing line from SEAMTESTS's first line; the slice itself starts at
   `@pytest.mark.subprocess` and those blank lines are your join, not part of the slice.
6. Nothing outside the declared change set is touched. This round registers R-0530 and
   resolves nothing, so the open count moves from 120 to 121.
7. If any gate comes out red, or a FROM does not match at exactly one place in its
   target, STOP: write the handback naming the exact command, its exit code and its
   output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every file this round edited and confirm no
   sentence this round put on disk was falsified by a later commit of the same round,
   and that no slice quotes another file's current wording as a claim. Name what was
   re-read and report the measurement, not a restatement of this sentence. Give special
   attention to any sentence quantifying over commits or files: R-0530 is that shape,
   and it landed one round ago inside the paragraph registering its own class.
9. Do not "repair" any landed text. The sentence R-0530 registers stays in commit
   3b915e3c; the registration IS the correction — the R-0521 principle.
10. `extra_env` adds no exception to `FORBIDDEN_ENV_KEYS`, whose floor lives in
    `scrub_child_env` and is not touched by any slice in this block. If any authored
    line appears to lower that floor, STOP under constraint 7.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status
--porcelain` empty at round start and after every commit; `git worktree list` one line
at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r39.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r39.md` — disk-to-disk, not a digest fallback. Report
the sha256, byte count, line count, marker-line count and region digests over lines
1-100, 101-200, 201-300 and 301-end, each taken with trailing newlines included, and
report the byte count of each region so an EMPTY region is visible as empty. Measure
every one of those; compute none by hand.

G3 APPEND SHAPE for C1 on `.agent/live_review.md`: the pre-commit blob is a byte-exact
PREFIX of the post-commit file; the remainder is exactly one blank line plus RECORD7;
RECORD7 is an exact suffix; its first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because the quoted regex already appears in that file's
prose. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md`
at base cbcb5c23 and at HEAD, from `^- R-\d{4} — `, `^Done: R-\d{4} — ` and
`^Landed: R-\d{4}`. The reviewer's base reading is 144 / 24 / 0, 120 open, max
registered R-0529, max resolved R-0527; at HEAD it must be 145 / 24 / 0, 121 open, max
registered R-0530, max resolved R-0527. Report the registered symmetric difference
(exactly R-0530), the done and landed symmetric differences (both empty), the
duplicate-id count, the count of resolutions naming an unregistered id, the maximum id,
and the next free id, which moves from R-0530 to R-0531.

G5 THE SEAM at HEAD after C2, in `packages/orchestration/exec_guard.py`: each of the
four FROM texts occurs 0x and each of the four TO texts 1x; the guard's floor is
untouched, measured as the line `    keep = set(allowlist) - FORBIDDEN_ENV_KEYS`
occurring exactly 1x and `def scrub_child_env` through its `return` being byte-identical
to the same span at cbcb5c23; 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` reached either file. For SEAMTESTS report the §4.9 append
obligation: every line SEAMTESTS contains occurs exactly once AMONG THE LINES C2'S DIFF
ADDS to `tests/orchestration/test_exec_guard.py`. Report `git show --numstat` for C2,
and after C3 the FROM 0x / TO 1x reading for the plan pair plus `.agent/plan.md`'s line
count against the 50-line cap.

G6 SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518), each as
its exact command line, each exit 0. Every base reading below was taken by the reviewer
at cbcb5c23:
- `python3 -m pytest tests/orchestration/test_exec_guard.py -q` — base `24 passed`;
  at HEAD it must be `27 passed`, the three cases SEAMTESTS adds.
- `python3 -m pytest tests/orchestration/test_mission_state.py
  tests/orchestration/test_job_promote.py tests/orchestration/test_pingpong.py
  tests/orchestration/test_pingpong_promote.py -q` — the seam's consumers, base
  `262 passed`. C2 is additive with a `None` default, so HEAD must also be
  `262 passed`; any other number is a STOP under constraint 7, not a number to report.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — base `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules`
  absent IS finding R-0518 and means the command ran in a worktree; re-run it in the
  primary checkout.
- `python3 -m ruff check packages/orchestration/exec_guard.py
  tests/orchestration/test_exec_guard.py` — base `All checks passed!`. Run the SAME
  command over the SAME two paths at `origin/main` as well and report both, so a
  pre-existing error cannot be read as a new one. Repository-wide `ruff check` is RED on
  main and is NOT a gate (R-0364).
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G7 HYGIENE. `git diff --name-only cbcb5c23..HEAD` measured BEFORE C4 holds exactly the
change set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report
per-commit insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own
insertions go in the round report — and confirm none exceeds 500. Confirm every commit
has exactly one parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA cbcb5c23, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real G1-G7 results with exit codes, the
open-findings count and the next expected action. In `## Authored-text proofs` report
each pair under the shape constraint 2 assigns it, and never report a FROM-zero count
for an append. Repeat this Fortschritt line verbatim:
Fortschritt: ~76 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R38
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R40
migrierbar · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

The `## Next` section MUST state that the next session's FIRST action is Phase 1 rule 1
— re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list
--state open --json number,headRefName,baseRefName,isDraft`); that R39's own verdict is
NOT a §4.13 terminator because this branch continues; and that the next reviewed round
records R39's gate entry. It MUST also carry this note verbatim:

  R40 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through `extra_env`. It still owes its own DECISION on where the stage output
  goes: at cbcb5c23 `_run_via_subprocess` streams straight to the console and returns
  only the returncode, while the seam CAPTURES both streams, so the migration changes
  observable behaviour rather than preserving it and that decision is the round's own
  work. `packages/orchestration/builder_bridge.py` follows it, and R41 or later takes
  T002c-d.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-SEAMA
    output_cap_bytes: int = TEST_COMMAND_OUTPUT_CAP_BYTES,
    extra_env_keys: Sequence[str] = (),
) -> ExecGuardPolicy:
END-SEAMA

BEGIN-SEAMB
    output_cap_bytes: int = TEST_COMMAND_OUTPUT_CAP_BYTES,
    extra_env_keys: Sequence[str] = (),
    extra_env: Mapping[str, str] | None = None,
) -> ExecGuardPolicy:
END-SEAMB

BEGIN-SEAMC
    names it there instead of widening the shared allowlist for everyone.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=output_cap_bytes,
        cwd=cwd,
        core_file_bytes=0,
        env=None,
        env_allowlist=TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys),
    )
END-SEAMC

BEGIN-SEAMD
    names it there instead of widening the shared allowlist for everyone.

    `extra_env` SETS variables the parent need not have, which `extra_env_keys`
    cannot do: that knob names keys to pass THROUGH, so a key absent from
    `os.environ` arrives absent. Both `test`-class call sites still on a bare
    spawn overlay one variable onto a copy of `os.environ` and would lose that
    value silently on this seam without this knob. The overlay becomes the scrub
    SOURCE and its keys join the allowlist, so `scrub_child_env` still applies
    `FORBIDDEN_ENV_KEYS` as the floor: an `extra_env` naming a forbidden key does
    not reach the child.
    """
    overlay = dict(extra_env or {})
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=output_cap_bytes,
        cwd=cwd,
        core_file_bytes=0,
        env={**os.environ, **overlay} if overlay else None,
        env_allowlist=(
            TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys) + tuple(sorted(overlay))
        ),
    )
END-SEAMD

BEGIN-SEAME
    cwd: str | None,
    extra_env_keys: Sequence[str] = (),
) -> subprocess.CompletedProcess[bytes]:
END-SEAME

BEGIN-SEAMF
    cwd: str | None,
    extra_env_keys: Sequence[str] = (),
    extra_env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
END-SEAMF

BEGIN-SEAMG
    guarded = run_guarded(cmd, test_command_exec_policy(
        timeout_sec, cwd, extra_env_keys=extra_env_keys))
END-SEAMG

BEGIN-SEAMH
    guarded = run_guarded(cmd, test_command_exec_policy(
        timeout_sec, cwd, extra_env_keys=extra_env_keys, extra_env=extra_env))
END-SEAMH

BEGIN-SEAMTESTS
@pytest.mark.subprocess
def test_extra_env_sets_a_value_the_parent_does_not_have(monkeypatch):
    """The SET knob, which `extra_env_keys` cannot provide.

    `extra_env_keys` names keys to pass THROUGH, so a key the parent lacks arrives
    absent. The remaining `test`-class sites SET a value instead, which is why the
    two knobs are separate rather than one.
    """
    monkeypatch.delenv("REMEDY_PROBE_BUDGET", raising=False)

    passed_through = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env_keys=("REMEDY_PROBE_BUDGET",),
    )
    set_by_overlay = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env={"REMEDY_PROBE_BUDGET": "4242"},
    )

    assert "REMEDY_PROBE_BUDGET" not in _dumped(passed_through)
    assert _dumped(set_by_overlay)["REMEDY_PROBE_BUDGET"] == "4242"


@pytest.mark.subprocess
def test_extra_env_cannot_smuggle_a_forbidden_key_past_the_floor():
    """`FORBIDDEN_ENV_KEYS` is the guard's floor and not a caller's to lower."""
    result = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env={"ANTHROPIC_API_KEY": "sk-should-never-appear"},
    )

    assert "ANTHROPIC_API_KEY" not in _dumped(result)
    assert b"sk-should-never-appear" not in result.stdout


def test_extra_env_adds_to_the_allowlisted_environment_rather_than_replacing_it(monkeypatch):
    """The overlay ADDS; what the allowlist already carries still reaches the child."""
    monkeypatch.setenv("REMEDY_UI_NO_AUTO_BUILD", "1")

    policy = exec_guard.test_command_exec_policy(
        60, None, extra_env={"REMEDY_PROBE_BUDGET": "7"}
    )
    child_env = exec_guard.plan_child_spawn(policy).env

    assert child_env["REMEDY_PROBE_BUDGET"] == "7"
    assert child_env["REMEDY_UI_NO_AUTO_BUILD"] == "1"
    assert "PATH" in child_env
END-SEAMTESTS

BEGIN-RECORD7
Gate: R39 — the R38 entry. R38 PASSED. Every ordered gate was re-run by the reviewer over
c3201976..cbcb5c23 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the
committed `.agent/authored/f085-r38.md`, the committed `.agent/last_block.md` at b9d5050b
and both working copies are all five byte-EQUAL at sha256
5fa4d096e45014a54d93d7f27efe176adc4c85a1f10ebdcf6a649c6620cb5090, 18154 B, 284 lines, 12
marker lines — and that digest is the one the reviewer measured BEFORE emission, so the
block the worker applied is the block the reviewer wrote. BOTH APPENDS HELD THEIR SHAPE:
3b915e3c's pre-commit blob 397527 B is a byte-exact PREFIX of the 402603 B post-commit
file with remainder one blank line plus RECORD6, numstat 65/0; 275a294e's 356103 B is a
prefix of 358646 B with remainder one blank line plus DEC6, numstat 38/0; each slice is an
exact suffix, each first line occurs once among that commit's added lines, and 0 marker
lines reached either file. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 142 / 24 / 0
at c3201976 against 144 / 24 / 0 at cbcb5c23, 118 open against 120, registered symmetric
difference exactly R-0528 and R-0529, done and landed symmetric differences empty, no
duplicate id, no resolution naming an unregistered id, next free R-0530. THE PLAN PAIRS
WERE APPLIED VERBATIM: the reviewer rebuilt the file mechanically — the pre-commit blob
with each FROM replaced once by its TO equals the post-commit blob byte for byte — and
`.agent/plan.md` is 45 lines against its 50-line cap with `## Goal` and `## Next Steps`
intact. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed` and the
canary `42 passed`, each as its exact ordered command line in the primary checkout, each
exit 0. HYGIENE IS CLEAN: the path set is the six declared paths, per-commit insertions
are 284, 249, 65, 49 and the handback's own 48, none over 500, all five commits are
single-parent, the reflog holds only `commit:` entries, and origin and local agree at
cbcb5c23.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R38's worker measured a
sentence of the reviewer's own RECORD6 against the repository, found it false, declared it
in the handback, and changed nothing. That is the fourth consecutive round in which the
constraint-8 report produced the round's finding, and the third in which the false
sentence was one the reviewer wrote about its own text.

- R-0530 — Low, A CORRECTION INTRODUCED THE UNIVERSAL IT WAS WRITTEN TO REMOVE. RECORD6's
R-0528 paragraph, applied at commit 3b915e3c, states that `.agent/last_block.md` "hashes
208ad9d3 at 483975b3 and c8efc5c0 at 857ca31a and every commit after it". Measured: that
file hashes 208ad9d3 at 483975b3, c8efc5c0 at 857ca31a and c3201976, and 5fa4d096 at
b9d5050b and cbcb5c23. The clause "and every commit after it" is therefore false from
b9d5050b — R38's own C0b — onward, and because C0b PRECEDES C1 the sentence was already
false at the moment it landed. The two readings it actually took are correct; only the
quantifier is wrong. What makes this worth an id rather than a shrug is its provenance:
the clause was ADDED by the reviewer, in the last edit before emission, specifically to
satisfy the R-0525 rule that a reference to `.agent/last_block.md` name the SHA holding
the text it means — and naming two SHAs correctly, then generalising past them, is the
R-0526 universal-quantifier shape reappearing inside the paragraph that registers its own
class. Checklist item 11 already forbids exactly this and the block's own constraint 8
already ordered the measurement that caught it, so nothing new is owed to the checklist:
what is owed is the habit of running that measurement over sentences quantifying across
COMMITS, which no pair-shape or path check reaches. Found by the worker under constraint 8
and registered by the reviewer.
END-RECORD7

BEGIN-PLANF7
## Current Step
R38, this round: record the R37 PASS, register R-0528 and R-0529, and give the
`test`-class seam an `extra_env` overlay so a call site can SET a variable — the one
capability both remaining T002b sites need. No call site is migrated.
END-PLANF7

BEGIN-PLANT7
## Current Step
R39, this round: record the R38 PASS, register R-0530, and implement DECISION F085 D3 —
the `extra_env` overlay on the `test`-class seam, with the tests pinning the set, the
`FORBIDDEN_ENV_KEYS` floor and the untouched allowlist. No call site is migrated.
END-PLANT7
