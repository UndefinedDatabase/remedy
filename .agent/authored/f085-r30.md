── STEP T002b group 1 — F085 — R30 ───────────────────────────────────────────

Goal: record the R29 PASS, resolve R-0519, and move the two byte-identical
post-test spawns — `job_promote._run_post_test` and
`pingpong_promote._run_post_test` — onto the shared `test`-class seam, each with
a test that pins the migration.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R29 and resolve R-0519 · C2 the migration and its tests · C3 plan · C4 handback.

## Why this round exists — read before C1

R29 passed every gate it ordered; the reviewer re-ran all of them over
b0d09db4..f99a8fe2 and every reading reproduces. R-0519's counter-measure landed
in that same round, so this round resolves it rather than carrying it.

The two sites this round migrates are ONE shape, not two: over the regions the
pairs replace, `job_promote.py` and `pingpong_promote.py` are byte-identical —
same `shlex`-split argv, same `timeout_sec`, same `cwd=str(target)`, same
concatenation of the two streams into the `str` summary the caller reads. That is
why one pair serves both files.

The seam hands back BYTES — `run_guarded_test_command` returns
`CompletedProcess[bytes]` — so the migration has two coupled halves: the spawn
moves onto the guard AND the stream concatenation gains a decode. A change that
does only one half raises `AttributeError: 'str' object has no attribute
'decode'`, which is what G6's red proof produces on purpose.

`pingpong_loop._run_test_command` is the same shape with `staging` in place of
`target` and is deliberately NOT in this round: adding it pushed the block over
the 400-line cap of docs/agents/planner_reviewer_prompt.md §3 item 1. It leads
the plan's remainder list instead.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R29 gate entry and then the R-0519 resolution, as one slice.

C2 — one commit. SPAWNF→SPAWNT and OUTF→OUTT are each applied to
`job_promote.py` AND to `pingpong_promote.py`, matching at exactly one place in
each; the pairs are narrowed to the lines that actually change, so the untouched
`except` arms are not carried through the block. Each file also takes its own
IMPORT pair, because their import blocks differ — `job_promote.py` already
imports from `packages.orchestration`, `pingpong_promote.py` does not. TESTJP and
TESTPP append one node each to the test file named after the source it covers.

C3 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. The FROM spans the whole
`## Current Step` and `## Next Steps` region so the numbered list is rewritten by
the pair itself and no stale label survives on its tail.

Change set, named rather than counted: `packages/orchestration/job_promote.py`,
`packages/orchestration/pingpong_promote.py`,
`tests/orchestration/test_job_promote.py`,
`tests/orchestration/test_pingpong_promote.py`, `.agent/authored/f085-r30.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
`.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r30.md` by its marker pair. Never retype a
   slice, never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test, one
   reading per pair: SPAWNF→SPAWNT REWRITE · OUTF→OUTT REWRITE · IMPF1→IMPT1
   APPEND-SHAPED · IMPF2→IMPT2 APPEND-SHAPED · PLANF→PLANT REWRITE. The two
   append-shaped import pairs therefore take the added-lines proof of G5 and
   never a whole-file "FROM 0x" count. TESTJP and TESTPP are appends to the end
   of their files and have no FROM at all.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. G6's
   red proof is destructive, so it runs ONLY inside a disposable worktree under
   `.remedy-wt/`, which is removed and pruned before C3; `git worktree list` is
   one line at the handback.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round resolves R-0519
   and registers nothing, so the registered set must come out unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in
   the file it is applied to, STOP: write the handback naming the exact command,
   its exit code and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same
   round, and that no slice quotes another file's current wording as a claim.
   Name what was re-read.
9. TESTJP and TESTPP append to files that already end in a test body. Append each
   to the file's existing bytes with exactly the blank lines the slice itself
   carries; do not insert or delete a separating newline of your own.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r30.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and
region digests over the line ranges 1-100, 101-200, 201-300 and 301-end. Do not
compute any of those numbers by hand; measure them.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count
marker LINES, never the substring, because `APPEND-shaped` and the quoted regex
both already appear in that file's prose and a substring count reports them.
Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base f99a8fe2 and at HEAD. The reviewer's base reading
is 134 registered / 15 done / 0 landed, 119 open, max R-0519; at HEAD it must be
134 / 16 / 0 with 118 open and max still R-0519. Report the registered symmetric
difference (it must be EMPTY), the done symmetric difference (it must hold
exactly R-0519), the landed symmetric difference (empty), the count of duplicate
ids, the count of resolutions naming an unregistered id, the maximum id and the
next free id.

G5 MIGRATION PAIRS, measured at HEAD after C2. SPAWNF and OUTF each occur 0 times
in `job_promote.py` and 0 times in `pingpong_promote.py`, and SPAWNT and OUTT each
occur exactly once in each file. For each IMPORT pair, which is append-shaped,
report that its TO
occurs exactly once in its file and that the line
`from packages.orchestration.exec_guard import run_guarded_test_command` occurs
exactly once among the lines C2's diff ADDS to that file. Report that each of the
two test files gained the line
`def test_job_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):`
respectively
`def test_pingpong_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):`
exactly once among the lines C2's diff ADDS to it. Report that 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` reached any of the four files, and `git show --numstat`
for C2.

G6 THE MIGRATION IS REAL, PROVED BY BREAKING IT. Round gate first, in the PRIMARY
checkout: `python3 -m pytest tests/orchestration/test_job_promote.py
tests/orchestration/test_pingpong_promote.py -q -rf` exits 0. The reviewer
measured that command at base f99a8fe2 as `144 passed` and, with this block's own
slices applied in a disposable worktree, as `146 passed` — report the HEAD count
as a READING and never as a target. The behaviour-equality golden the feature
file asks for is `TestApprovePostTest::test_post_apply_test_runs`, which spawns a
REAL child through the migrated function; the new node does not.
Then the RED PROOF, in a disposable worktree at HEAD under `.remedy-wt/` and
NEVER in the primary checkout: in `job_promote.py` replace the five-line
`run_guarded_test_command(` call with a bare
`subprocess.run(argv, capture_output=True, text=True, timeout=timeout_sec, cwd=str(target))`
and LEAVE the decode line as this block wrote it, then run
`python3 -m pytest tests/orchestration/test_job_promote.py -q -rf`. It must FAIL
with both `test_job_promote_post_test_runs_on_the_guarded_seam` and
`TestApprovePostTest::test_post_apply_test_runs` among the failures. Report the
failing node names and the exception text the run prints. Delete the worktree,
then remove and prune it before C3.

G7 LINT AND STATE READERS. `python3 -m ruff check` over the four non-`.agent`
files C2 changes, as one command line with the repository's own configuration and
no `--isolated`, exits 0. Then, because this round also rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`158 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518
records why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes`
with `apps/ui/node_modules` absent IS that finding rather than a regression. Any
other red is a STOP under constraint 7. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`. No docs gate: nothing under `docs/` changes.

G8 COMMIT HYGIENE. `git diff --name-only f99a8fe2..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which
C4 writes, and nothing else. Report per-commit insertions for every commit BEFORE
C4 — C4 cannot measure itself, so report its own insertions in the round report
instead — and confirm none exceeds 500. Confirm every commit has exactly one
parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA f99a8fe2, a per-commit changed-files table, the
item-status table covering C0a, C0b, C1, C2, C3 and C4, the real verification
results for G1-G8 with exit codes, the open-findings count, and the next expected
action. Repeat this Fortschritt line verbatim:
Fortschritt: ~63 % (T001 gebaut · R13-R29 PASS · T002a KOMPLETT · T002b 7 von 12
Sites auf dem Seam, 5 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). It MUST also state that R30's own
verdict is NOT a §4.13 terminator because this branch continues, and that the
next reviewed round records R30's gate entry in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD1
Gate: R29 — PASS, the state-only round that recorded the R28 PASS, registered
R-0519 and put the T002b migration state into the inventory of record. Every
ordered gate was re-run by the reviewer over b0d09db4..f99a8fe2 and each one
reproduces the handback's reading. TRANSPORT: the committed
`.agent/authored/f085-r29.md`, the committed `.agent/last_block.md` and both
working copies are all four byte-EQUAL at sha256
5c93aff876b168aada846b99dcf9ff927df3f41f3329b55a7f40d353422dd813, 18160 B, 306
lines, 10 marker lines at 157, 226, 228, 244, 246, 262, 264, 276, 278 and 306,
region digests c40e6be2, 23d988e4 and 70c142ae. No scratchpad original from that
authoring session survived into this one, so the proof is disk-to-disk over the
committed artifacts under the self-drive protocol's cmp rule; stated, not
implied. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at numstat
69/0, RECORD1's first line occurs once among the 69 lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits nine times
in that file's prose. THE ARITHMETIC MOVED IN ONE SET ONLY: 134 registered / 15
done / 0 landed at HEAD against 133 / 15 / 0 at base, 118 open rising to 119,
registered symmetric difference exactly R-0519, done and landed symmetric
differences both empty, no duplicate id, no resolution naming an unregistered id,
max R-0519 and next free R-0520. THE PAIRS LANDED WHERE THEY WERE AIMED: PLANF
occurs 0 times at HEAD and PLANT exactly once, `## Goal` and `## Risks` are
byte-identical to their base bytes, `.agent/plan.md` is 42 lines under the
50-line cap, and its `## Next Steps` parses to 1, 2, 3. INVF occurs once and INVT
once, INVT contains INVF verbatim so the pair really is append-shaped, and
`Migration state, measured at R29:` occurs once among the 16 lines C3 adds. THE
MEASUREMENT THE ROUND EXISTS TO RECORD IS TRUE OF THE SOURCE, NOT ONLY OF THE
PROSE: the reviewer re-derived it per file rather than trusting the paragraph.
`autorun.py` references `run_guarded_test_command` five times, `test_runner.py`
three times and `test_execution_service.py` references `plan_child_spawn` three
times, so those three files carry the five sites called ON THE SEAM;
`builder_bridge.py`, `ci_run.py`, `integrity_gate.py`, `job_promote.py`,
`mission_state.py`, `pingpong_loop.py` and `pingpong_promote.py` reference
neither symbol. Five on the seam, seven not, as the inventory paragraph and
R-0519 both state. THE GATES WERE RE-RUN, NOT READ: the four state
readers exited 0 at `158 passed` and the canary exited 0 at `42 passed`, each as
its exact ordered command line in the primary checkout. COMMIT HYGIENE IS CLEAN:
the path set before the handback is the five declared paths, per-commit
insertions are 306, 212, 69, 8 and 16 with the handback's own 99 measured after
it existed and none over 500, the range is a single-parent chain, and the reflog
holds only `commit:` entries. One reported number differs and neither reading is
wrong: the handback gives `## Goal` as 729 B where a heading-inclusive slice
measures 730 B, a section-boundary convention that leaves the ordered property —
byte-identical to base — reproducing either way. The 131-line handback declares
its own overage against the 100-line cap and names the mandated content that
caused it. No block condition is met.

Done: R-0519 — RESOLVED at R29 by the counter-measure the finding itself named.
`.agent/f085_inventory.md` now carries `Migration state, measured at R29:`
directly beneath the `### test — 12` heading that defines the class, naming the
criterion for being on the seam, the files that satisfy it and the files that do
not — so the next estimate is derived from the file that fixes the denominator
instead of from the previous estimate. The overstated line is gone as well: R29's
handback carries `~60 %` with `T002b 5 von 12 Sites auf dem Seam, 7 offen` in
place of `~85 %`. The reviewer verified the correction against the SOURCE, per
the per-file reading in this round's gate entry above. Resolved rather than
carried, because the finding asked for a denominator on disk and it is on disk.
END-RECORD1

BEGIN-SPAWNF
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(target),
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
            cwd=str(target),
        )
END-SPAWNT

BEGIN-OUTF
    output = (proc.stdout or "") + (proc.stderr or "")
END-OUTF

BEGIN-OUTT
    output = (proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode("utf-8", "replace")
END-OUTT

BEGIN-IMPF1
from packages.orchestration.pingpong_evidence import (
END-IMPF1

BEGIN-IMPT1
from packages.orchestration.exec_guard import run_guarded_test_command
from packages.orchestration.pingpong_evidence import (
END-IMPT1

BEGIN-IMPF2
from uuid import uuid4
END-IMPF2

BEGIN-IMPT2
from uuid import uuid4

from packages.orchestration.exec_guard import run_guarded_test_command
END-IMPT2

BEGIN-TESTJP


# F085 T002b — job_promote._run_post_test on the shared `test`-class seam


def test_job_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import job_promote

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(job_promote, "run_guarded_test_command", _fake_guarded)
    passed, summary = job_promote._run_post_test("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary
END-TESTJP

BEGIN-TESTPP


# F085 T002b — pingpong_promote._run_post_test on the shared `test`-class seam


def test_pingpong_promote_post_test_runs_on_the_guarded_seam(tmp_path, monkeypatch):
    """The spawn goes through `run_guarded_test_command`, and its BYTES decode to str."""
    import subprocess

    from packages.orchestration import pingpong_promote

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 0, b"out-line\n", b"err-line\n")

    monkeypatch.setattr(pingpong_promote, "run_guarded_test_command", _fake_guarded)
    passed, summary = pingpong_promote._run_post_test("pytest -q", tmp_path, timeout_sec=17)

    assert passed is True
    assert seen == {"cmd": ["pytest", "-q"], "timeout_sec": 17, "cwd": str(tmp_path)}
    assert summary.startswith("exit=0")
    assert "out-line" in summary
    assert "err-line" in summary
END-TESTPP

BEGIN-PLANF
## Current Step
R29, this round: record the R28 PASS and register R-0519. The T002b Restprüfung
found five of the twelve `test`-class sites on the seam and seven still on a bare
spawn, which the previous Fortschritt overstated; the measurement lands in
`.agent/f085_inventory.md` beneath the class list that defines the set.

## Next Steps
1. T002b continued — the seven `test`-class sites still on a bare spawn:
   `builder_bridge.py`:220, `ci_run.py`:79, `integrity_gate.py`:283,
   `job_promote.py`:417, `mission_state.py`:833, `pingpong_loop.py`:3537 and
   `pingpong_promote.py`:326. Take them in small groups, one order per group.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.

END-PLANF

BEGIN-PLANT
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

END-PLANT
