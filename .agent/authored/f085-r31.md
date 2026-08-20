── STEP T002b group 2 — F085 — R31 ───────────────────────────────────────────

Goal: record the R30 PASS, register R-0520 against the reviewer's own R29 gate
entry, and move `pingpong_loop._run_test_command` — the last site of the shape
R30 migrated — onto the shared `test`-class seam, with a test that pins it.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R30 and register R-0520 · C2 the migration and its test · C3 plan · C4 handback.

## Why this round exists — read before C1

R30 passed. The reviewer re-ran every gate it ordered over f99a8fe2..d4fe1674 —
the transport digest, the append shape, the arithmetic, the pair counts, the
round gate, ruff, the state readers, the canary and the hygiene readings — and
each reproduces. The red proof was re-run independently in the reviewer's own
disposable worktree and produced the two failing nodes G6 named.

R30's handback reported one thing it was right not to repair: a present-tense
sentence in the R29 gate entry says `job_promote.py` and `pingpong_promote.py`
"reference neither symbol", which C2 of that same round made false. The worker
could not touch it — constraint 1 forbids altering a slice, constraint 6 forbids
widening scope — so it reported it instead, which is the correct move and is why
this round registers R-0520 rather than treating the report as the fix.

`pingpong_loop._run_test_command` is the same shape R30 migrated, with `staging`
in place of `target`. It was held back from R30 only because including it pushed
that block over the 400-line cap of docs/agents/planner_reviewer_prompt.md §3
item 1.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R30 gate entry and then the R-0520 registration, as one slice.

C2 — one commit. SPAWNF→SPAWNT, OUTF→OUTT and IMPF→IMPT are applied to
`pingpong_loop.py`, each matching at exactly one place; TESTPL appends one node
to `tests/orchestration/test_pingpong.py`, the test file that already covers that
module.

C3 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. The FROM spans the whole
`## Current Step` and `## Next Steps` region so the numbered list is rewritten by
the pair itself and no stale label survives on its tail.

Change set, named rather than counted: `packages/orchestration/pingpong_loop.py`,
`tests/orchestration/test_pingpong.py`, `.agent/authored/f085-r31.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
`.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r31.md` by its marker pair. Never retype a
   slice, never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test, one
   reading per pair: SPAWNF→SPAWNT REWRITE · OUTF→OUTT REWRITE · IMPF→IMPT
   APPEND-SHAPED · PLANF→PLANT REWRITE. The append-shaped import pair therefore
   takes the added-lines proof of G5 and never a whole-file "FROM 0x" count.
   TESTPL is an append to the end of its file and has no FROM at all.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. G6's
   red proof is destructive, so it runs ONLY inside a disposable worktree under
   `.remedy-wt/`, which is removed and pruned before C3; `git worktree list` is
   one line at the handback.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round registers
   R-0520 and resolves nothing, so the done set must come out unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in
   the file it is applied to, STOP: write the handback naming the exact command,
   its exit code and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same
   round, and that no slice quotes another file's current wording as a claim.
   Name what was re-read. R-0520's own text is written to survive C2 — it names
   the commit its readings belong to — so check it rather than assuming it.
9. TESTPL appends to a file that already ends in a test body. Append it with
   exactly the blank lines the slice itself carries; do not insert or delete a
   separating newline of your own.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r31.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and
region digests over the line ranges 1-100, 101-200 and 201-end. Do not compute
any of those numbers by hand; measure them.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count
marker LINES, never the substring, because `APPEND-shaped` and the quoted regex
both already appear in that file's prose and a substring count reports them.
Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base d4fe1674 and at HEAD. The reviewer's base reading
is 134 registered / 16 done / 0 landed, 118 open, max R-0519; at HEAD it must be
135 / 16 / 0 with 119 open and max R-0520. Report the registered symmetric
difference (it must hold exactly R-0520), the done and landed symmetric
differences (both empty), the count of duplicate ids, the count of resolutions
naming an unregistered id, the maximum id and the next free id.

G5 MIGRATION PAIRS, measured at HEAD after C2. SPAWNF and OUTF each occur 0 times
in `pingpong_loop.py`, and SPAWNT and OUTT each occur exactly once. IMPT, which is
append-shaped, occurs exactly once, and the line
`from packages.orchestration.exec_guard import run_guarded_test_command` occurs
exactly once among the lines C2's diff ADDS to that file. Report that
`tests/orchestration/test_pingpong.py` gained the line
`def test_pingpong_loop_test_command_runs_on_the_guarded_seam(tmp_path, monkeypatch):`
exactly once among the lines C2's diff ADDS to it, that 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` reached either file, and `git show --numstat` for C2.

G6 THE MIGRATION IS REAL, PROVED BY BREAKING IT. Round gate first, in the PRIMARY
checkout: `python3 -m pytest tests/orchestration/test_pingpong.py -q -rf` exits 0.
The reviewer measured that command at base d4fe1674 as `33 passed` — report the
HEAD count as a READING and never as a target.
Then the RED PROOF, in a disposable worktree at HEAD under `.remedy-wt/` and
NEVER in the primary checkout: in `pingpong_loop.py` replace the five-line
`run_guarded_test_command(` call with a bare
`subprocess.run(argv, capture_output=True, text=True, timeout=timeout_sec, cwd=str(staging))`
and LEAVE the decode line as this block wrote it, then run
`python3 -m pytest tests/orchestration/test_pingpong.py -q -rf`. It must FAIL with
`test_pingpong_loop_test_command_runs_on_the_guarded_seam` among the failures.
Report the failing node names and the exception text the run prints. Delete the
worktree, then remove and prune it before C3.

G7 LINT AND STATE READERS. `python3 -m ruff check packages/orchestration/pingpong_loop.py
tests/orchestration/test_pingpong.py` with the repository's own configuration and
no `--isolated` exits 0. Then, because this round also rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`158 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518
records why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes`
with `apps/ui/node_modules` absent IS that finding rather than a regression. Any
other red is a STOP under constraint 7. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`. No docs gate: nothing under `docs/` changes.

G8 COMMIT HYGIENE. `git diff --name-only d4fe1674..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which
C4 writes, and nothing else. Report per-commit insertions for every commit BEFORE
C4 — C4 cannot measure itself, so report its own insertions in the round report
instead — and confirm none exceeds 500. Confirm every commit has exactly one
parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA d4fe1674, a per-commit changed-files table, the
item-status table covering C0a, C0b, C1, C2, C3 and C4, the real verification
results for G1-G8 with exit codes, the open-findings count, and the next expected
action. Repeat this Fortschritt line verbatim:
Fortschritt: ~67 % (T001 gebaut · R13-R30 PASS · T002a KOMPLETT · T002b 8 von 12
Sites auf dem Seam, 4 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). It MUST also state that R-0520 is OPEN
and awaits the next reviewed round's authored resolution, that R31's own verdict
is NOT a §4.13 terminator because this branch continues, and that the next
reviewed round records R31's gate entry in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD1
Gate: R30 — PASS, the round that moved `job_promote._run_post_test` and
`pingpong_promote._run_post_test` onto the shared `test`-class seam. Every ordered
gate was re-run by the reviewer over f99a8fe2..d4fe1674 and each one reproduces
the handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL,
not only against a digest: the scratch file the block was authored into, the
committed `.agent/authored/f085-r30.md`, the committed `.agent/last_block.md` and
both working copies are all five byte-EQUAL at sha256
fd9117aad06382747a59995dbeef4d32d75e14f3f7e3d19af7bc5499dc93b0a2, 21347 B, 399
lines, 26 marker lines, region digests 9e5478bc, 97f12afd, c6bb8ee5 and d3cf7d6b.
THE APPEND COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of
the post-commit file, the remainder is exactly one blank line plus RECORD1 at
numstat 58/0, RECORD1's first line occurs once among the 58 lines that commit
adds, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits
ten times in that file's prose. THE ARITHMETIC MOVED IN THE DONE SET ALONE: 134
registered / 16 done / 0 landed at d4fe1674 against 134 / 15 / 0 at f99a8fe2, 119
open falling to 118, registered symmetric difference empty, done symmetric
difference exactly R-0519, landed empty, no duplicate id, no resolution naming an
unregistered id, max R-0519 and next free R-0520. THE PAIRS LANDED WHERE THEY WERE
AIMED: at d4fe1674 SPAWNF and OUTF each occur 0 times in both migrated files while
SPAWNT and OUTT each occur once, IMPT1 occurs once in `job_promote.py` and IMPT2
once in `pingpong_promote.py`, the guard import occurs once among the lines C2 adds
to each source, each new test def occurs once among the lines C2 adds to its test
file, and 0 marker lines reached any of the four. PLANF is gone and PLANT occurs
once, in a 46-line plan under the 50-line cap. THE PROOF IS A REAL COUPLING AND THE
REVIEWER BROKE IT INDEPENDENTLY: at d4fe1674 the round gate exits 0 at `146 passed`
against the `144 passed` the reviewer measured at f99a8fe2 before the block was
written, and in the reviewer's own disposable worktree at d4fe1674, with the
guarded call replaced by a bare `subprocess.run` and the decode left standing, the
run exits 1 with `2 failed, 73 passed` — `TestApprovePostTest::test_post_apply_test_runs`
and `test_job_promote_post_test_runs_on_the_guarded_seam`, both
`AttributeError: 'str' object has no attribute 'decode'`. The first of those two is
the behaviour-equality golden this feature's Acceptance asks for: it spawns a REAL
child through the migrated function, so its staying green under the guard is the
evidence that well-behaved commands behave identically. THE GATES WERE RE-RUN, NOT
READ: ruff over the four changed files `All checks passed!`, the four state readers
`158 passed` and the canary `42 passed`, each as its exact ordered command line in
the primary checkout. COMMIT HYGIENE IS CLEAN: the path set is the nine declared
paths, per-commit insertions are 399, 317, 58, 69 and 12 with the handback's own
100 measured after it existed and none over 500, all six commits are single-parent,
and the reflog holds only `commit:` entries. The 150-line handback declares its own
overage against the 100-line cap and names the mandated content that caused it. No
block condition is met, and the worker deviated from nothing it was ordered to do.

- R-0520 — Low, A REVIEWER-AUTHORED GATE ENTRY MADE A PRESENT-TENSE CLAIM ABOUT
SOURCE FILES THE SAME BLOCK THEN CHANGED. The R29 gate entry applied at commit
9668bec4 lists seven modules and states that they "reference neither symbol",
meaning `run_guarded_test_command` and `plan_child_spawn`. That reading was taken
at f99a8fe2 and is true there. C2 of the SAME round, commit 10fe9a14, put
`job_promote.py` and `pingpong_promote.py` on the seam, and at d4fe1674 each of
those two files references `run_guarded_test_command` twice — so two of the seven
names in that sentence are wrong for every commit from 10fe9a14 onward, in a file
that is the permanent record. The defect is the reviewer's, not the worker's: R30's
handback found it under constraint 8 and reported it instead of editing a slice it
was forbidden to alter or a file outside its change set, which is exactly the
behaviour constraint 8 exists to produce. Low because nothing executable depends on
the sentence, no gate can go red over it, and the paragraph it sits in opens by
naming the range b0d09db4..f99a8fe2 that scopes it. It is registered rather than
quietly corrected because this is the R-0417 staleness class recurring in the one
place the standing gate does not reach — the reviewer's own authored prose, written
before the commit that falsifies it exists. The counter-measure is a rule, not an
edit: a slice that states a fact about a file the SAME block modifies names the
commit its reading was taken at, in the sentence itself, rather than relying on a
range named in a neighbouring sentence. Rewriting the landed text is NOT proposed —
appending a correction is how this record stays honest, and a later round may do
that; overwriting history in `.agent/live_review.md` is worse than a dated wrong
sentence. OPEN.
END-RECORD1

BEGIN-SPAWNF
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(staging),
        )
END-SPAWNF

BEGIN-SPAWNT
        # Guarded since F085 T002b: rlimits, an env allowlist, a pinned cwd and the
        # guard's own wall deadline replace the bare spawn. The observable outcome is
        # unchanged — same returncode, same TimeoutExpired, same FileNotFoundError —
        # except that the guard hands back BYTES, which the decode below turns into
        # the str this function has always returned.
        proc = run_guarded_test_command(
            argv,
            timeout_sec=timeout_sec,
            cwd=str(staging),
        )
END-SPAWNT

BEGIN-OUTF
    output = (proc.stdout or "") + (proc.stderr or "")
END-OUTF

BEGIN-OUTT
    output = (proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode("utf-8", "replace")
END-OUTT

BEGIN-IMPF
from packages.orchestration.pingpong_provider import (
END-IMPF

BEGIN-IMPT
from packages.orchestration.exec_guard import run_guarded_test_command
from packages.orchestration.pingpong_provider import (
END-IMPT

BEGIN-TESTPL


# F085 T002b — pingpong_loop._run_test_command on the shared `test`-class seam


def test_pingpong_loop_test_command_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import pingpong_loop

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(pingpong_loop, "run_guarded_test_command", _fake_guarded)
    passed, summary = pingpong_loop._run_test_command("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary
END-TESTPL

BEGIN-PLANF
## Current Step
R30, this round: record the R29 PASS, resolve R-0519, and move the two
byte-identical post-test spawns of `job_promote.py` and `pingpong_promote.py`
onto `run_guarded_test_command`, each with a test that pins the spawn and the
bytes-to-str decode the seam makes necessary.

## Next Steps
1. T002b remainder — the `test`-class sites still on a bare spawn.
   `pingpong_loop.py`:3537 first: it is the same shape as the pair just migrated,
   with `staging` in place of `target`, so it takes the same pair with one word
   changed. Then the four that each differ: `builder_bridge.py`:220 adds
   `PYTHONDONTWRITEBYTECODE` to a full `os.environ`, `ci_run.py`:79 streams to the
   console instead of capturing and passes no timeout, `integrity_gate.py`:283
   passes no cwd at all, and `mission_state.py`:833 spawns inside a default
   `runner` closure. One or two per order, never as one group.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.

END-PLANF

BEGIN-PLANT
## Current Step
R31, this round: record the R30 PASS, register R-0520 against the reviewer's own
R29 gate entry, and move `pingpong_loop._run_test_command` onto
`run_guarded_test_command` — the last site of the shape R30 migrated.

## Next Steps
1. T002b remainder — the four `test`-class sites still on a bare spawn, each
   differing from the shape already migrated: `builder_bridge.py`:220 adds
   `PYTHONDONTWRITEBYTECODE` to a full `os.environ`, `ci_run.py`:79 streams to the
   console instead of capturing and passes no timeout, `integrity_gate.py`:283
   passes no cwd at all, and `mission_state.py`:833 spawns inside a default
   `runner` closure. One or two per order, never as one group.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.

END-PLANT
