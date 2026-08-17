── STEP T002b — F085 — R28 ───────────────────────────────────────────────────

Goal: record the R27 PASS, resolve R-0517, and take
`test_execution_service._run_isolated_process` onto the F085 seam's CHILD half —
`exec_guard.plan_child_spawn` — so its child is spawned under the policy's
rlimits, cwd and environment while every parent-side duty stays where it is.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R27 and resolve R-0517 · C2 plan · C3 the migration and its proof · C4 handback.

## Why this round exists — read before C1

R27 passed every gate it ordered; the reviewer re-ran all of them over
369d94a3..07b1ba25 and each reading reproduces. R-0517's fix was R27's own
handback, which now carries the Phase-1-rule-1 sentence on disk, so this round
authors the resolution the protocol reserves for the reviewer.

The production half takes the site the plan named last for T002b.
`_run_isolated_process` cannot use `run_guarded_test_command`: that seam buffers
both streams to bytes and returns a `CompletedProcess`, while this function
writes the child's output straight into a file handle and returns a four-tuple
its callers unpack positionally. What it CAN take is the child half —
`plan_child_spawn` resolves a policy into cwd, environment and the `preexec_fn`
that applies the rlimits — which is the split `ChildSpawnPlan` exists for and
which `stream_evidence.run_streamed_command` already consumes the same way.

R-0202 IS NOT RESOLVED HERE AND MUST NOT BE READ AS RESOLVED. That finding names
this site as one of the two that drop `REMEDY_UI_NO_AUTO_BUILD`. The migration
keeps `env` exactly as the caller built it, so the variable is dropped after this
round for the same reason and by the same code as before it. The mechanism moves;
the environment does not.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R27 gate entry, then the R-0517 resolution, then the R-0518
registration, as one slice.

C2 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. The FROM spans the whole
`## Current Step` and `## Next Steps` region so the numbered list is rewritten by
the pair itself rather than left half-edited.

C3 — one commit over `packages/orchestration/test_execution_service.py` and
`tests/orchestration/test_test_execution_service.py`, carrying the S1-S5 pairs.
S1 imports the seam, S2 is the migration, S3 and S4 import what the new test
needs, and S5 adds that test. Code and proof land together: a migration whose
proof arrives in a later commit is a migration nobody gated.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r28.md` by its marker pair. Never retype a
   slice, and never apply one from the delegating prompt. Marker lines never
   reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test rather than
   read by eye, one reading per pair: PLANF→PLANT REWRITE · S1 REWRITE ·
   S2 REWRITE · S3 REWRITE · S4 REWRITE · S5 APPEND-SHAPED, because S5's TO keeps
   its anchor line `    def test_no_shell_true(self):` verbatim. S5 therefore
   takes the added-lines proof of G6 and never a whole-file "FROM 0x" count.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. The
   red proof of G8 runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/`, which is removed and pruned before the handback. Use absolute
   paths: a `cd` into a worktree persists across commands and makes later
   readings describe the wrong tree.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round resolves
   R-0517 and no other finding, and registers R-0518 and no other finding.
7. If any gate comes out red, or a FROM does not match at exactly one place,
   STOP: write the handback naming the exact command, its exit code and its
   output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read both edited source files and confirm
   that no sentence this round put on disk was falsified by a later commit of
   the same round, and that no slice quotes another file's current wording as a
   claim. Report the check by naming what was re-read.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r28.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and
region digests over the line ranges 1-100, 101-200 and 201-end. Do not compute
any of those numbers by hand; measure them.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count
marker LINES, never the substring, because `APPEND-shaped` already appears in
that file's prose and a substring count reports it. Report `git show --numstat`
for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 07b1ba25 and at HEAD. The reviewer's base reading
is 132 registered / 14 done / 0 landed, 118 open, max R-0517; at HEAD it must be
133 / 15 / 0, still 118 open, max R-0518. One id arrives and one id is resolved,
so the open count is flat while both sets move — do not read a flat open count as
a sign that nothing changed. Report the registered symmetric difference (it must
hold exactly R-0518), the done symmetric difference (it must hold exactly
R-0517), the landed symmetric difference (empty), the count of duplicate ids, the
count of resolutions naming an unregistered id, the maximum id and the next free
id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numerals its `## Next
Steps` list parses to rather than a count of them.

G6 CODE PAIRS. At HEAD, in the file each pair targets: S1F, S2F, S3F and S4F each
occur 0 times and S1T, S2T, S3T and S4T each exactly once. S5 is append-shaped,
so instead report that the lines C3's diff ADDS contain
`    def test_child_half_of_the_exec_policy_reaches_the_child(self, tmp_path):`
exactly once, and that `    def test_no_shell_true(self):` still occurs exactly
once in the whole file.

G7 ROUND GATE. `python3 -m pytest tests/orchestration/test_test_execution_service.py
tests/cli/test_test_run_runtime.py tests/cli/test_truncation_metadata.py -q`
exits 0. The reviewer measured `97 passed` at base 07b1ba25 with the same command
line, and this round adds exactly one test. Report the reading rather than
matching it.

G8 RED PROOF, in a disposable worktree at HEAD under `.remedy-wt/` and nowhere
else. Delete the single line `                preexec_fn=plan.preexec_fn,` from
`packages/orchestration/test_execution_service.py`, then run
`python3 -m pytest tests/orchestration/test_test_execution_service.py::TestRunIsolatedProcess::test_child_half_of_the_exec_policy_reaches_the_child -q`
and report its exit code and its last output line. Then restore the file and
report the same command's exit code again. The reviewer ran this exact recipe
before ordering it: the node went red without the line and green with it. A
disagreeing reading is a finding, not something to repair.

G9 RUFF. `python3 -m ruff check packages/orchestration/test_execution_service.py
tests/orchestration/test_test_execution_service.py` exits 0. The reviewer
measured `All checks passed!` for that command line at base 07b1ba25, so a new
error is this round's and not a pre-existing one. The repository-wide `ruff
check` is RED on main and is NOT a gate.

G10 STATE READERS AND CANARY, because this round rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`158 passed` — that suite spawns wrapper processes under flock, so report the
count as a READING and never as a target.

RUN THIS ONE IN THE PRIMARY CHECKOUT AND NEVER INSIDE THE G8 WORKTREE. It carries
`TestVitestFrontendTestFoundation::test_vitest_passes`, which shells out to `npx
vitest run` against `apps/ui`, and `apps/ui/node_modules` is gitignored
(`.gitignore:221`) so no fresh worktree has it. The reviewer measured both sides:
green in the primary checkout, red in a cold worktree with `[UNRESOLVED_IMPORT]
Could not resolve 'vitest/config'`. That is R-0518, which this round's own C1
registers and which this round does NOT fix. A red naming that node with
`apps/ui/node_modules` absent IS that finding; any other red is a STOP under
constraint 7. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits
0, base reading `42 passed`. No docs gate: nothing under `docs/` changes.

G11 COMMIT HYGIENE. `git diff --name-only 07b1ba25..HEAD` measured BEFORE C4
holds exactly these paths and nothing else, named rather than counted:
`.agent/authored/f085-r28.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `packages/orchestration/test_execution_service.py`,
`tests/orchestration/test_test_execution_service.py`. Report per-commit
insertions for every commit BEFORE C4 — C4 cannot measure itself, so report its
own insertions in the round report instead — and confirm none exceeds 500.
Confirm every commit has exactly one parent and that `git reflog -12` holds only
`commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G11
with exit codes, the open-findings count, and the next expected action. Repeat
this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R27 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` + `test_execution_service` migriert · T002b
Restprüfung, T002c-d, T003 offen) — Schätzung.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). It MUST also state that R-0202 is NOT
resolved by this round, that R28's own verdict is NOT a §4.13 terminator because
this branch continues, and that the next reviewed round records R28's gate entry
in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. Create no PR and merge
nothing.

BEGIN-RECORD1
Gate: R27 — PASS, the round that recorded R26 and registered the reviewer's own
omission. Every ordered gate was re-run by the reviewer over 369d94a3..07b1ba25
and each one reproduces the handback's reading. TRANSPORT IS EXACT IN ALL FOUR
PLACES: the committed `.agent/authored/f085-r27.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
ce7ffcc42df494a9c21e733f410e6d8f48d394bc16239a0be71191232cdeafdd, 14103 B, 229
lines, 6 marker lines, region digests dfea0906, 85061d65 and b03dbb55. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD2 at numstat
61/0, RECORD2's first line occurs once among the lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits five times —
all of it `APPEND-shaped` prose older than that round, which is the exact
distinction the gate exists to force. THE ARITHMETIC MOVED BY THE ONE ID IT WAS
ORDERED TO MOVE BY: 131 registered / 14 done / 0 landed with 117 open at base and
132 / 14 / 0 with 118 open at HEAD, registered symmetric difference exactly
R-0517, done and landed symmetric differences empty, no duplicate id, no
resolution naming an unregistered id, max R-0517 and next free R-0518. THE PLAN
PAIR IS A REWRITE AND ONLY THE ORDERED REGION MOVED: PLANF2 occurs 0 times at HEAD
and PLANT2 once, `## Goal` and `## Risks` are byte-identical to their base bytes,
the file is 254757ce2fbc3267ebdda74003373bf987e83371927bb6384a1a50caf470b46c at
2370 B and 41 lines, and its `## Next Steps` list parses to 1, 2, 3. THE GATES
WERE RE-RUN, NOT READ: the four state readers exited 0 with `158 passed` and the
canary exited 0 with `42 passed`, each as its exact ordered command line, and no
ruff gate was skipped by oversight because the change set holds no `.py` file.
COMMIT HYGIENE IS CLEAN: the path set measured before the handback commit is the
four declared `.agent/` paths and the handback adds only itself, per-commit
insertions are 229, 168, 61 and 4 with the handback's own 80 measured after it
existed and none over 500, the range is a single-parent chain, and the reflog
holds only `commit:` entries. The handback is 123 lines against the 60 its
per-commit tables carry; the overage is declared, names its own measured length
and names the mandated content that caused it, which DECISION D15 permits and
which no dropped section was traded for. No block condition is met.

Done: R-0517 — resolved. The pointer is back on disk, and the block that dropped
it is the block that restored it. R27's Handback section named the
Phase-1-rule-1 sentence among the handback's mandated contents, and the handback
it produced carries it: `.agent/handoff.md` at 07b1ba25 states in its `## Next`
section that the next session's first action is re-reading `.agent/STOP` from
disk BEFORE the Open PR Gate, and the reviewer read that from the file rather
than from the worker's report. The finding closes on the PROPERTY and not on a
sentence: what is required is that a handoff naming the next session's first
action names the sentinel check first, and that every later block's Handback
section carries the requirement forward — this round's block does. No checklist
item is added, because docs/agents/self_drive_protocol.md §Phase 2 already binds
it and a second copy would be a second source of truth.

- R-0518 — Medium, A GATED TEST NEEDS A GITIGNORED BUILD DIRECTORY, SO THE
STATE-READER GATE IS RED IN EXACTLY THE DISPOSABLE WORKTREE THIS PROTOCOL
MANDATES. `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
runs `npx vitest run` with `cwd=Path("apps/ui").resolve()`, and
`apps/ui/node_modules` is gitignored at `.gitignore:221`, so a fresh
`git worktree` never carries it. That node sits inside the four-file state-reader
suite every `.agent/`-rewriting round gates on, while
docs/agents/planner_reviewer_prompt.md §4 item 10 and the self-drive protocol's
G5 both require destructive verification to run in a disposable worktree. The two
rules meet in a red no change caused. MEASURED, not inferred: in the primary
checkout the node passed 3 of 3 standalone and the whole suite read `158 passed`
at exit 0 in 5 of 5 runs at base 07b1ba25; in a worktree created at the same
commit with no `apps/ui/node_modules` it failed 2 of 2 standalone with
`AssertionError: vitest failed: ... [UNRESOLVED_IMPORT] Could not resolve
'vitest/config'`. The first red the reviewer hit reported only a tail summary and
named no node, which is why `-rf` now stands in the ordered command line — a
reading ordered in a shape that cannot carry the evidence it exists to produce is
its own small defect, recorded here rather than in a separate id. Medium because
a red gate halts a round under the standing rule that a worker never repairs
around one, and this red is reachable by any round that follows the worktree
requirement. NOT fixed here: the repair belongs in the test — skip the node when
`apps/ui/node_modules` is absent — and `tests/orchestration/test_test_runner.py`
carries no skip of its own today, so the fix is a real edit to a gate file and
sits outside this round's change set. OPEN.
END-RECORD1

BEGIN-PLANF
## Current Step
R27, this round: record the R26 PASS and register R-0517 — the reviewer's own R26
block under-specified its Handback section, so that round's handoff dropped the
next-session pointer the self-drive protocol requires. The session's declared cap
of two authored rounds is reached here, not a blocker.

## Next Steps
1. T002b continued — the `test`-class sites still on a bare spawn, ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R28, this round: record the R27 PASS, resolve R-0517, and put
`test_execution_service._run_isolated_process` on the seam's CHILD half via
`plan_child_spawn`, keeping its own wait deadline, its process-group kill and its
file-backed streams where they are. R-0202 stays open: the environment the child
receives is unchanged by this round.

## Next Steps
1. T002b Restprüfung — re-derive the `test`-class site set from
   `.agent/f085_inventory.md` against amendment F085 D1's twelve, and name every
   site still on a bare spawn before T002b is called finished.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT

BEGIN-S1F
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.permissions import Capability, is_allowed
END-S1F

BEGIN-S1T
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.exec_guard import ExecGuardPolicy, plan_child_spawn
from packages.orchestration.permissions import Capability, is_allowed
END-S1T

BEGIN-S2F
    with open(output_file, "wb") as out_fh:
        try:
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
END-S2F

BEGIN-S2T
    # WHY: the CHILD half of the F085 execution policy — the rlimits, the cwd and the
    # environment `plan_child_spawn` resolves between fork and exec. The PARENT half
    # stays here: this function owns its own `proc.wait` deadline, its process-group
    # kill and its file-backed streams, so the policy carries no wall timeout and no
    # output cap and a second deadline never fights this one. `env` stays the
    # CALLER's: `_build_safe_env` already scrubbed it against the job's environment,
    # while the seam's own allowlist would rebuild it from `os.environ` and discard
    # that scrubbing. Remedy deliberately does not surface `plan.limits_unsupported`
    # here — this function's return tuple is read positionally by every caller.
    plan = plan_child_spawn(ExecGuardPolicy(cwd=cwd, env=env, core_file_bytes=0))

    with open(output_file, "wb") as out_fh:
        try:
            proc = subprocess.Popen(
                argv,
                cwd=plan.cwd,
                env=plan.env,
                preexec_fn=plan.preexec_fn,
                stdin=subprocess.DEVNULL,
END-S2T

BEGIN-S3F
import os
import sys
from dataclasses import asdict
END-S3F

BEGIN-S3T
import os
import resource
import sys
from dataclasses import asdict
END-S3T

BEGIN-S4F
from uuid import uuid4

from packages.orchestration.test_execution_service import (
END-S4F

BEGIN-S4T
from uuid import uuid4

import pytest

from packages.orchestration.test_execution_service import (
END-S4T

BEGIN-S5F
    def test_no_shell_true(self):
END-S5F

BEGIN-S5T
    def test_child_half_of_the_exec_policy_reaches_the_child(self, tmp_path):
        # The guard sets BOTH halves of RLIMIT_CORE to 0 while an unguarded child
        # inherits the parent's hard limit unchanged, so a child that reads (0, 0) is
        # evidence that `plan_child_spawn`'s `preexec_fn` really ran between fork and
        # exec. When the parent's own hard limit is already 0 there is nothing to
        # observe, and the test says so instead of passing vacuously.
        if resource.getrlimit(resource.RLIMIT_CORE)[1] == 0:
            pytest.skip("parent already has a zero RLIMIT_CORE hard limit")
        output = tmp_path / "out.txt"
        status, exit_code, _dur, _started = _run_isolated_process(
            [sys.executable, "-c",
             "import resource, sys; "
             "sys.exit(0 if resource.getrlimit(resource.RLIMIT_CORE) == (0, 0) else 1)"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=10.0,
        )
        assert status == "passed"
        assert exit_code == 0

    def test_no_shell_true(self):
END-S5T
