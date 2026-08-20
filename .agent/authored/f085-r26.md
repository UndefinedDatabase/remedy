── STEP T002b continued — F085 — R26 ─────────────────────────────────────────

Goal: record the R25 PASS, then continue T002b by moving `autorun.py`'s three
`test`-class sites off their bare `subprocess.run` and onto the shared seam
`run_guarded_test_command`. Mechanism changes; observable outcome does not.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R25 · C2 migrate the three sites · C3 plan · C4 handback.

## Why this round exists — read before C2

T002b migrated `test_runner.run_tests_local` at R24 and left the rest of the
`test` class on bare spawns. `autorun.py` holds three of them: one in
`_run_fixture_builder` and two in `_run_repair_loop_fixture`. They are the next
sites because they share the migrated shape exactly — an argv list, a `timeout`,
a `cwd`, no `shell` — and because real children already drive them in the suite,
so the migration is verifiable rather than merely plausible.

The reviewer measured the three sites before authoring this block, and two facts
decide its shape:

- Every read of the returned object across all three sites is `.returncode` —
  checked with an AST walk over both enclosing functions, not by eye. The seam
  returns BYTES streams where the old call passed `text=True`, and because no
  site reads `stdout` or `stderr`, that difference is unobservable here. This is
  why the pairs below drop `capture_output=True, text=True` rather than trying to
  preserve them: the seam always captures, and it has no `text` parameter.
- `subprocess` stays imported in `_run_fixture_builder`, because its `except
  subprocess.TimeoutExpired` clause still needs the name, and the seam still
  raises exactly that exception on a wall trip. In `_run_repair_loop_fixture` the
  two migrated calls are that function's ONLY uses of `subprocess`, so IMP2
  removes the import. Leaving it would turn ruff F401 red.

Neither fixture path catches `TimeoutExpired` around the repair-loop calls today,
and neither did before: an uncaught wall trip stays uncaught. That is preserved
behaviour, not an oversight, and no slice below changes it.

## Change

C2 — `packages/orchestration/autorun.py`, one commit, exactly the pairs below and
nothing else in the file. Each FROM was confirmed to occur EXACTLY ONCE in the
file at this base. Containment was tested mechanically, one reading per pair, and
every reading came back the same way — no TO contains its FROM verbatim:
IMP1 REWRITE · SITE1 REWRITE · IMP2 REWRITE · SITE2 REWRITE · SITE3 REWRITE ·
PLANF/PLANT REWRITE. IMP1 is called out because it is the shape most often
mistaken for an append: it keeps its anchor line and still inserts a blank line
above it, so the FROM does not survive intact.

Do NOT touch `exec_guard.py`. Its PARTIAL COVERAGE note already says the test
class is PARTIALLY migrated and deliberately writes no count, so this round
leaves that note TRUE and editing it would only re-introduce the staleness R-0516
was raised about. The reviewer also swept `autorun.py`'s own module docstring and
its autonomy-level list: neither states anything this round falsifies, so C2
edits no prose in that file beyond the comment SITE1T carries.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r26.md` by its marker pair. Never retype a
   slice, and never apply one from this prompt directly. Marker lines
   (`BEGIN-…`/`END-…`) never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
3. `git status --porcelain` is empty at round start and after every commit. Any
   destructive check runs ONLY in a disposable `git worktree` under
   `.remedy-wt/`, removed and pruned before the handback.
4. C1's RECORD1 is an APPEND to `.agent/live_review.md`: the pre-commit file
   stays a byte-exact prefix, and exactly one blank line separates it from the
   slice. Do not reflow, re-wrap or re-indent RECORD1.
5. Nothing outside the declared change set is touched. This round registers no
   finding and resolves none, so the finding arithmetic must come out FLAT.
6. If any gate below comes out red, or any FROM does not match at exactly one
   place, STOP: write the handback naming the exact command, its exit code and
   its output, and do not improvise a repair.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 2;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` is one line at the handback.

G2 TRANSPORT. After C0b, the committed `.agent/authored/f085-r26.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and three
region digests over the line ranges 1-60, 61-140 and 141-end, so a split write
would be visible rather than merely unlikely.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once in the commit's added lines;
0 marker lines land in the file; the HEAD blob equals the working copy. Report
`git show --numstat` for that path and commit.

G4 ARITHMETIC, FLAT. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 5b02cff9 and at HEAD. The reviewer's base reading
is 131 registered / 14 done / 0 landed, 117 open. Both readings must be identical
— a `Gate:` line registers nothing. Report both symmetric differences (each must
be empty), the count of duplicate ids, the count of resolutions naming an
unregistered id, the maximum id and the next free id.

G5 THE MIGRATION, MEASURED ON THE FILE. In `packages/orchestration/autorun.py` at
HEAD: `subprocess.run(` occurs 0 times, having occurred 3 times at base; each FROM
text below occurs 0 times; each TO text below occurs exactly once;
`run_guarded_test_command` occurs once per migrated call site plus once per import
that C2 adds. Report `import subprocess` still present in `_run_fixture_builder`
and absent from `_run_repair_loop_fixture`. Report the file's sha256 and byte count.

G6 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numerals its `## Next
Steps` list parses to rather than a count of them.

G7 THE ROUND GATE, run after C2:
`python3 -m pytest tests/orchestration/test_autorun.py
tests/test_cli_execution_loop_closure.py tests/regression/test_named_bugs.py -q`
exits 0. The reviewer's base reading is `140 passed, 6 skipped`. Report the counts
as a READING, and report whether the migration moved them. These three files were
chosen deliberately: the first drives `_run_fixture_builder` with a real child,
the second drives BOTH repair-loop sites with real children — once expecting a
pass and once expecting a failing suite — and the third reads `autorun.py` as
SOURCE and asserts `shell=True` never appears in it, which the seam must not
re-introduce.

G8 REACHABILITY PROBE, run in a disposable worktree at HEAD and NOT in the primary
checkout. Make `run_guarded_test_command` raise on entry — edit its body in
`exec_guard.py` inside the worktree — then run G7's exact command line there.
REPORT what happens: how many nodes fail, whether the injected error appears in
the output, and the exact tail. No colour is ordered and none is predicted; the
reading itself is the evidence that C2's code is on a path the suite really
executes.

G9 NEIGHBOURS AND LINT. `python3 -m pytest tests/orchestration/test_exec_guard.py
-q` exits 0, base reading `24 passed`. The four state readers, because this round
rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0, base reading `158 passed`; that suite spawns wrapper processes under
flock and is timing-sensitive, so report its count as a READING. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`. LINT: `python3 -m ruff check packages/orchestration/autorun.py`
exits 0. No docs gate: nothing under `docs/` changes.

G10 COMMIT HYGIENE. `git diff --name-only 5b02cff9..HEAD` measured BEFORE C4 holds
exactly these paths and nothing else, named rather than counted:
`.agent/authored/f085-r26.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`packages/orchestration/autorun.py`, `.agent/plan.md`. Report per-commit insertions
for every commit BEFORE C4 — C4 cannot measure itself, so report its own insertions
in the round report instead — and confirm none exceeds 500. Confirm every commit has
exactly one parent and that `git reflog -12` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G10
with exit codes, the open-findings count, and the next expected action. Repeat the
Fortschritt line verbatim from this block:
Fortschritt: ~80 % (T001 gebaut · R13-R25 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.
Then `git push -u origin feature/f085-sandbox-hardening`. Create no PR and merge
nothing.

BEGIN-RECORD1
Gate: R25 — PASS, the paydown round that recorded R24 and retired the stale
no-callers claim from the guard's own fixture file. All nine ordered gates were
re-run by the reviewer over 3d1821bf..5b02cff9 and every one reproduces the
handback's reading. TRANSPORT IS PROVEN DISK-TO-DISK UNDER THE §4.9 DIGEST
FALLBACK, WHICH THIS ENTRY STATES RATHER THAN HIDES: this session did not author
R25's block, so no reviewer-side pre-delegation original exists to compare
against, and the proof is instead that the committed `.agent/authored/f085-r25.md`
is byte-EQUAL to the committed `.agent/last_block.md` and to both working copies
at sha256 4abce714f82e9a6b2baad095c02c6f0aecebfd009ce4a8883531c908b8971262,
18089 B, 296 lines, with the region digests 07199a30, cad21f6b and 3de16b95 all
reproducing, and that every applied slice re-derives from that committed file by
its marker pair. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 and again for C3 the
pre-commit blob is a byte-exact PREFIX of the post-commit file and the remainder
is exactly one blank line plus the slice, at numstat 67/0 and 12/0. THE ARITHMETIC
MOVES ONLY WHERE R-0516 MOVES IT: 130 / 13 / 0 with 117 open at base, 131 / 13 / 0
with 118 open after C1, and 131 / 14 / 0 with 117 open at HEAD; both symmetric
differences are exactly the set holding R-0516; no duplicate id, no resolution
naming an unregistered id, max R-0516 and next free R-0517. THE FALSE SENTENCE IS
OFF DISK AND ITS REPLACEMENT RESOLVES: DOCF occurs 0 times at HEAD and DOCT
exactly once, the file's first line is byte-unchanged from base, sha256
ee200a92041190027a59efc08a835dd2827dc951de57eb7e35cf158957d2d04c at 21388 B — and
the reviewer followed the new pointer rather than trusting it, finding the PARTIAL
COVERAGE note exactly once in `exec_guard.py`, saying what DOCT attributes to it
and writing no count, so the replacement cannot go stale the way the sentence it
replaced did. THE GATES WERE RE-RUN, NOT READ: the edited suite exited 0 with
`24 passed` and the docstring edit did NOT move that base, the four state readers
gave `158 passed`, the canary `42 passed`, and ruff over the changed `.py`
`All checks passed!`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the changed-path set is the declared one, per-commit insertions are 296,
217, 67, 6, 12 and 7 with the handback's own 56 measured after it existed and none
over 500, seven commits form a single-parent chain, and the reflog holds nothing
but `commit:` entries. The handback is 100 lines — exactly the ceiling its seven
per-commit tables engage under DECISION D15, so it sits AT the cap rather than
over it. No block condition is met.
END-RECORD1

BEGIN-IMP1F
        import subprocess
        import sys as _sys
        try:
END-IMP1F

BEGIN-IMP1T
        import subprocess
        import sys as _sys

        from packages.orchestration.exec_guard import run_guarded_test_command
        try:
END-IMP1T

BEGIN-SITE1F
            proc = subprocess.run(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q", "--tb=short", "--no-header"],
                capture_output=True, text=True, timeout=30,
                cwd=str(repo),
            )
END-SITE1F

BEGIN-SITE1T
            # Guarded since F085 T002b: rlimits, an env allowlist and the guard's
            # own deadline replace the bare spawn. Only `returncode` is read here,
            # so the seam's bytes streams change nothing this site observes.
            proc = run_guarded_test_command(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q", "--tb=short", "--no-header"],
                timeout_sec=30,
                cwd=str(repo),
            )
END-SITE1T

BEGIN-IMP2F
    import subprocess
    import sys as _sys

    from packages.orchestration.permissions import Capability, set_permission
END-IMP2F

BEGIN-IMP2T
    import sys as _sys

    from packages.orchestration.exec_guard import run_guarded_test_command
    from packages.orchestration.permissions import Capability, set_permission
END-IMP2T

BEGIN-SITE2F
        proc = subprocess.run(
            [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
             "--tb=short", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
END-SITE2F

BEGIN-SITE2T
        proc = run_guarded_test_command(
            [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
             "--tb=short", "--no-header"],
            timeout_sec=30, cwd=str(repo),
        )
END-SITE2T

BEGIN-SITE3F
            proc2 = subprocess.run(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
                 "--tb=short", "--no-header"],
                capture_output=True, text=True, timeout=30, cwd=str(repo),
            )
END-SITE3F

BEGIN-SITE3T
            proc2 = run_guarded_test_command(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
                 "--tb=short", "--no-header"],
                timeout_sec=30, cwd=str(repo),
            )
END-SITE3T

BEGIN-PLANF
## Current Step
R25, this round: record the R24 PASS, register R-0516 — a stale claim the R24
block left standing in a file it was itself editing — and retire that claim in the
same round. The session's declared cap of two authored rounds is reached here, not
a blocker.

## Next Steps
1. T002b continued — the remaining `test`-class sites, starting with the three in
   `autorun.py`, which share the migrated shape exactly, and ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R26, this round: record the R25 PASS and continue T002b by moving `autorun.py`'s
three `test`-class sites onto `run_guarded_test_command`. Every one of them reads
only `returncode`, so the seam's bytes streams change nothing they observe, and
real children already drive both fixture paths in the suite the round gate re-runs.

## Next Steps
1. T002b continued — the `test`-class sites still on a bare spawn, ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT
