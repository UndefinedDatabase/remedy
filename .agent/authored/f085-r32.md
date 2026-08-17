── STEP T002b group 3 — F085 — R32 ───────────────────────────────────────────

Goal: record the R31 PASS, resolve R-0520 by promoting its counter-measure into
the pre-emission checklist, and move `integrity_gate._check_collect_only` — the
`test`-class site that pins no cwd — onto the shared seam, with a node that pins
it.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1
promote the checklist item · C2 record R31 and resolve R-0520 · C3 the migration
and its test · C4 plan · C5 handback.

## Why this round exists — read before C1

R31 passed. The reviewer re-ran every gate it ordered over d4fe1674..HEAD and each
reproduces the handback's value; the red proof was re-run independently in the
reviewer's own disposable worktree and produced the failing node G6 named.

R-0520 states a rule and lives in finding prose, where it binds nothing — the
R-0452/R-0454 class, and the branch has already promoted three such rules into
`docs/agents/planner_reviewer_prompt.md` §3. C1 performs the promotion and C2
records the resolution AFTERWARDS, so the resolving sentence is true on the disk
it lands on. That ordering is R-0520's own rule applied to itself.

`integrity_gate._check_collect_only` differs from every site migrated so far by
passing NO cwd: it resolves `scripts/remedy_pytest.sh` relative to the process
working directory, so this seam is entered with `cwd=None` and the pin the feature
adds elsewhere is deliberately NOT added here. The module's other
`subprocess.run` — the `git ls-files` call in `_check_relevant_untracked` — is a
different command class and is NOT touched, which is why the `subprocess` import
stays. No test executes this function today, so C3 brings the node that pins the
seam and the round also runs it FOR REAL, because a mocked node cannot show that
the guard's allowlist still lets a real collection succeed.

## Change

C1 — `docs/agents/planner_reviewer_prompt.md`, one commit, the ITEM20F→ITEM20T
pair. The FROM is the checklist's closing paragraph opener, so the new item lands
after item 19 and before that paragraph.

C2 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R31 gate entry and then the R-0520 resolution, as one slice.

C3 — one commit. IGIMPF→IGIMPT, IGSPAWNF→IGSPAWNT and IGERRF→IGERRT are applied
to `packages/orchestration/integrity_gate.py`, each matching at exactly one
place; TESTIG appends one node to `tests/orchestration/test_integrity_gate.py`,
the test file that already covers that module.

C4 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. It spans the Current
Step and list item 1, the only lines that change; items 2 and 3 keep their labels
untouched because the list's arity does not change.

Change set, named rather than counted: `docs/agents/planner_reviewer_prompt.md`,
`packages/orchestration/integrity_gate.py`,
`tests/orchestration/test_integrity_gate.py`, `.agent/authored/f085-r32.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
`.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r32.md` by its marker pair. Never retype a
   slice, never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test, one
   reading per pair: ITEM20F→ITEM20T APPEND-SHAPED · IGIMPF→IGIMPT APPEND-SHAPED ·
   IGSPAWNF→IGSPAWNT REWRITE · IGERRF→IGERRT REWRITE · PLANF→PLANT REWRITE. The
   two append-shaped pairs therefore take the added-lines proof of G5 and G6 and
   never a whole-file "FROM 0x" count. TESTIG is an append to the end of its file
   and has no FROM at all.
3. Re-read `.agent/STOP` from disk before C0a and again before C5. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. G7's
   red proof is destructive, so it runs ONLY inside a disposable worktree under
   `.remedy-wt/`, which is removed and pruned before C4; `git worktree list` is
   one line at the handback.
5. C2 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round resolves R-0520
   and registers nothing, so the registered set must come out unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in
   the file it is applied to, STOP: write the handback naming the exact command,
   its exit code and its output, and do not improvise a repair.
8. STALENESS, standing: after C4 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same
   round, and that no slice quotes another file's current wording as a claim.
   Name what was re-read. RECORD1 states that the promoted rule is checklist item
   20; C1 puts it there and precedes C2, so check that ordering held rather than
   assuming it.
9. TESTIG appends to a file that already ends in a test body. Append it with
   exactly the blank lines the slice itself carries; do not insert or delete a
   separating newline of your own.
10. The commit order C1 before C2 is load-bearing, not cosmetic: it is what makes
    RECORD1's claim about the checklist true when it is written. Do not reorder.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r32.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and
region digests over the line ranges 1-100, 101-200 and 201-end. Do not compute
any of those numbers by hand; measure them.

G3 APPEND SHAPE for C2. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count
marker LINES, never the substring, because `APPEND-shaped` and the quoted regex
both already appear in that file's prose and a substring count reports them.
Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 16234fbf and at HEAD, taking registered from
`^- R-\d{4} — `, done from `^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`.
The reviewer's base reading is 135 registered / 16 done / 0 landed, 119 open, max
registered R-0520 and max resolved R-0519; at HEAD it must be 135 / 17 / 0 with 118
open and both maxima R-0520. Report the registered symmetric difference (it must be
EMPTY), the done symmetric difference (it must hold exactly R-0520), the landed
symmetric difference (empty), the count of duplicate ids, the count of resolutions
naming an unregistered id, the maximum id and the next free id, which is R-0521 at
both ends because this round registers nothing.

G5 THE CHECKLIST ITEM LANDED, measured at HEAD after C1. In
`docs/agents/planner_reviewer_prompt.md` the line
`  20. **A slice states a fact about a file the same block edits only with the commit`
occurs exactly once, the closing paragraph opener
`  Why this is on disk and not a habit: item 2 has recurred six times across`
occurs exactly once, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the
file. Report the first line of ITEM20T once among the lines C1's diff ADDS, and
`git show --numstat` for C1.

G6 MIGRATION PAIRS, measured at HEAD after C3. IGSPAWNF and IGERRF each occur 0
times in `packages/orchestration/integrity_gate.py`, and IGSPAWNT and IGERRT each
occur exactly once. IGIMPT, which is append-shaped, occurs exactly once, and the
line `from packages.orchestration.exec_guard import run_guarded_test_command`
occurs exactly once among the lines C3's diff ADDS to that file. Report that
`import subprocess` still occurs exactly once in that file — the `git ls-files`
call still needs it — that
`tests/orchestration/test_integrity_gate.py` gained the line
`def test_collect_only_runs_on_the_guarded_seam(monkeypatch):`
exactly once among the lines C3's diff ADDS to it, that 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` reached either file, and `git show --numstat` for C3.

G7 THE MIGRATION IS REAL, PROVED TWICE — once by running it, once by breaking it.
Round gate first, in the PRIMARY checkout:
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q -rf` exits 0. The
reviewer measured that command at base 16234fbf as `15 passed` — report the HEAD
count as a READING and never as a target.
Then the BEHAVIOUR-EQUALITY reading, in the PRIMARY checkout. Run, from the
repository root:
`python3 -c "from packages.orchestration.integrity_gate import _check_collect_only as c; r=c(); print(r.name, r.status, r.message)"`
The reviewer measured the UNMIGRATED function at base 16234fbf as
`collect_only IntegrityStatus.PASS pytest collection passed`, and measured the
guarded call it is being moved onto as returncode 0 over the same command line.
Report what the migrated function prints, as a reading; a `FAIL` or `SKIP` here is
a STOP under constraint 7, because it would mean the allowlist starves collection.
Then the RED PROOF, in a disposable worktree at HEAD under `.remedy-wt/` and
NEVER in the primary checkout: in `integrity_gate.py` replace the guarded call
with the bare
`result = subprocess.run(["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"], capture_output=True, text=True, timeout=120)`
leaving the import and the decode branch as this block wrote them, then run
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q -rf`. It must
FAIL with `test_collect_only_runs_on_the_guarded_seam` among the failures. Report
the failing node names and the exception text the run prints. Remove and prune the
worktree before C4.

G8 LINT AND STATE READERS. `python3 -m ruff check
packages/orchestration/integrity_gate.py tests/orchestration/test_integrity_gate.py`
with the repository's own configuration and no `--isolated` exits 0. Then, because
this round also rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`158 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518
records why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes`
with `apps/ui/node_modules` absent IS that finding rather than a regression. Any
other red is a STOP under constraint 7. Because a file under `docs/` changes:
`python3 -m pytest tests/docs/ -q` exits 0, base reading `295 passed`. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`.

G9 COMMIT HYGIENE. `git diff --name-only 16234fbf..HEAD` measured BEFORE C5 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which
C5 writes, and nothing else. Report per-commit insertions for every commit BEFORE
C5 — C5 cannot measure itself, so report its own insertions in the round report
instead — and confirm none exceeds 500. Confirm every commit has exactly one
parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA 16234fbf, a per-commit changed-files table, the
item-status table covering C0a, C0b, C1, C2, C3, C4 and C5, the real verification
results for G1-G9 with exit codes, the open-findings count, and the next expected
action. Repeat this Fortschritt line verbatim:
Fortschritt: ~70 % (T001 gebaut · R13-R31 PASS · T002a KOMPLETT · T002b 9 von 12
Sites auf dem Seam, 3 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). It MUST also state that R32's own
verdict is NOT a §4.13 terminator because this branch continues, and that the next
reviewed round records R32's gate entry in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-ITEM20F
  Why this is on disk and not a habit: item 2 has recurred six times across
END-ITEM20F

BEGIN-ITEM20T
  20. **A slice states a fact about a file the same block edits only with the commit
      it was read at.** Finding R-0520. An authored slice may assert a present-tense
      fact about a source file — "these modules reference neither symbol", "this
      function still spawns bare" — only when the sentence itself names the commit the
      reading was taken at, because a later commit of the SAME block may falsify it and
      the slice is by then unalterable: constraint 1 forbids editing a slice and the
      file it lands in is the permanent record. Item 9 re-measures a block's POINTERS
      at emission and item 19 governs a claim about a GATE's result; this one governs a
      claim about a file's CONTENT, which neither reaches, because the pointer resolves
      and no gate is involved — the sentence is simply true at the base and false at
      HEAD. The R29 instance: a gate entry listed seven modules as referencing neither
      symbol, and C2 of that same round put two of them on the seam, so five-sevenths
      of a sentence in `.agent/live_review.md` survives and two-sevenths do not. The
      counter-measure is the commit name, never a rewrite: appending a correction is
      how this record stays honest, and overwriting landed text is worse than a dated
      wrong sentence.
  Why this is on disk and not a habit: item 2 has recurred six times across
END-ITEM20T

BEGIN-RECORD1
Gate: R31 — PASS, the round that moved `pingpong_loop._run_test_command` onto the
shared `test`-class seam and registered R-0520. Every ordered gate was re-run by the
reviewer over d4fe1674..HEAD and each one reproduces the handback's reading.
TRANSPORT REPRODUCES IN REGIONS AND NOT ONLY IN TOTAL: the committed
`.agent/authored/f085-r31.md`, the committed `.agent/last_block.md` and both working
copies are all four byte-EQUAL at sha256
9023be74ce151bf00b833090c733fe9f77210a50519f4c14790f615adc6cf2a4, 20195 B, 352
lines, 20 marker lines, region digests def02d5c, afd442cb and b083f1bd. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at 5193 =
1 + 5192 bytes, numstat 67/0, RECORD1's first line occurs once among the 67 lines
that commit adds, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring
`END-` hits eleven times in that file's prose. THE ARITHMETIC MOVED IN THE
REGISTERED SET ALONE: 134 registered / 16 done / 0 landed at d4fe1674 against 135 /
16 / 0 at HEAD, 118 open rising to 119, registered symmetric difference exactly
R-0520, done and landed symmetric differences both empty, no duplicate id, no
resolution naming an unregistered id, max R-0520 and next free R-0521. THE PAIRS
LANDED WHERE THEY WERE AIMED: at HEAD SPAWNF and OUTF each occur 0 times in
`pingpong_loop.py` while SPAWNT and OUTT each occur once, IMPT occurs once, the guard
import occurs once among the nine lines C2 adds to that file, the new test def occurs
once among the twenty-five lines C2 adds to its test file, 0 marker lines reached
either, and every applied slice matches its committed original byte for byte — TESTPL
is an exact suffix of the test file and RECORD1 an exact suffix of the review record.
PLANF is gone and PLANT occurs once, in a 43-line plan under the 50-line cap. THE
PROOF IS A REAL COUPLING AND THE REVIEWER BROKE IT INDEPENDENTLY: at HEAD the round
gate exits 0 at `34 passed` against the `33 passed` the reviewer measured at
d4fe1674, and in the reviewer's own disposable worktree at 16234fbf, with the guarded
call replaced by a bare `subprocess.run` and the decode left standing, the run exits 1
with `1 failed, 33 passed` — `test_pingpong_loop_test_command_runs_on_the_guarded_seam`,
`AttributeError: 'str' object has no attribute 'decode'` at `pingpong_loop.py:3549`.
THE SEAM'S CONTRACT WAS READ RATHER THAN TRUSTED: `run_guarded_test_command` raises
`subprocess.TimeoutExpired` on a wall trip, deliberately does not catch
`FileNotFoundError`, and returns a negative returncode on a signal death — so both
`except` clauses and `passed = proc.returncode == 0` are unchanged. THE GATES WERE RE-RUN, NOT READ: ruff
over the two changed files `All checks passed!`, the four state readers `158 passed`
and the canary `42 passed`, each as its exact ordered command line in the primary
checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is the seven declared
paths, per-commit insertions are 352, 174, 67, 34, 5 and the handback's own 130, none
over 500, all six commits are single-parent, and the reflog holds only `commit:`
entries. STALENESS REPRODUCES: `builder_bridge.py`, `ci_run.py`, `integrity_gate.py` and
`mission_state.py` each show 0 references to `run_guarded_test_command` at HEAD, and
R-0520's own text survives C2 — `job_promote.py` and `pingpong_promote.py` reference
that symbol twice each at BOTH d4fe1674 and HEAD. The 162-line handback declares its own overage against the
100-line cap and names the mandated content that caused it. No block condition is met,
and the worker deviated from nothing it was ordered to do.

Done: R-0520 — Resolved at R32. The counter-measure the finding named is now
checklist item 20 of `docs/agents/planner_reviewer_prompt.md` §3, applied by the
commit that precedes this one in this round: a slice may assert a present-tense fact
about a source file only when the sentence names the commit its reading was taken at.
The finding asked for a rule rather than an edit, so the resolution is the promotion
and not a rewrite of the R29 sentence that exposed it. That sentence stays on disk,
wrong for two of its seven names from commit 10fe9a14 onward, because appending a
correction is how this record stays honest; this paragraph is that correction.
END-RECORD1

BEGIN-IGIMPF
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
END-IGIMPF

BEGIN-IGIMPT
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from packages.orchestration.exec_guard import run_guarded_test_command
END-IGIMPT

BEGIN-IGSPAWNF
        result = subprocess.run(
            ["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"],
            capture_output=True, text=True, timeout=120,
        )
END-IGSPAWNF

BEGIN-IGSPAWNT
        # Guarded since F085 T002b: rlimits, an env allowlist, a per-stream output cap
        # and the guard's own wall deadline replace the bare spawn. `cwd=None` is
        # deliberate and is the one pin this seam does NOT add here — the command
        # resolves `scripts/remedy_pytest.sh` relative to the process working
        # directory, so pinning it anywhere else would break collection. The guard
        # hands back BYTES, which the failure branch below decodes.
        result = run_guarded_test_command(
            ["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"],
            timeout_sec=120,
            cwd=None,
        )
END-IGSPAWNT

BEGIN-IGERRF
        return IntegrityCheck("collect_only", IntegrityStatus.FAIL,
                              f"collect-only failed: {result.stderr[:200]}")
END-IGERRF

BEGIN-IGERRT
        return IntegrityCheck("collect_only", IntegrityStatus.FAIL,
                              "collect-only failed: "
                              + (result.stderr or b"").decode("utf-8", "replace")[:200])
END-IGERRT

BEGIN-TESTIG


# F085 T002b — integrity_gate._check_collect_only on the shared `test`-class seam


def test_collect_only_runs_on_the_guarded_seam(monkeypatch):
    """The spawn goes through `run_guarded_test_command` with no cwd pin, and its BYTES decode."""
    import subprocess

    from packages.orchestration import integrity_gate

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 1, b"", b"boom-\xff-undecodable\n")

    monkeypatch.setattr(integrity_gate, "run_guarded_test_command", _fake_guarded)
    check = integrity_gate._check_collect_only()

    assert seen == {
        "cmd": ["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"],
        "timeout_sec": 120,
        "cwd": None,
    }
    assert check.status is integrity_gate.IntegrityStatus.FAIL
    assert "boom-" in check.message
    assert "undecodable" in check.message
END-TESTIG

BEGIN-PLANF
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
END-PLANF

BEGIN-PLANT
## Current Step
R32, this round: record the R31 PASS, resolve R-0520 by promoting its
counter-measure into the pre-emission checklist, and move
`integrity_gate._check_collect_only` onto `run_guarded_test_command` — the
`test`-class site that pins no cwd and keeps `cwd=None` deliberately.

## Next Steps
1. T002b remainder — the three `test`-class sites still on a bare spawn, each
   differing from the shapes already migrated: `builder_bridge.py` SETS
   `PYTHONDONTWRITEBYTECODE` on a full `os.environ` copy, which the seam cannot
   express today because `run_guarded_test_command` allowlists keys rather than
   setting values — that site needs the seam widened before it can move;
   `ci_run.py` streams to the console instead of capturing and passes no timeout;
   and `mission_state.py` spawns inside a default `runner` closure. One or two per
   order, never as one group.
END-PLANT
