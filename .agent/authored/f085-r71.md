── STEP T003 repair — the defeated no-shell test — F085 — R71 ────────────────

Goal: repair the one BLOCKER R70's integration gate found, register it and the parity defect that
gate also surfaced, and record the R70 PASS. F085 moved a spawn and a test that pinned the old spawn
site was silently defeated by the move; this round follows that test to the new seam. No production
file is touched — the property the test pins already holds in the source, and it is the MEASUREMENT
that is broken.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 register R-0564 and R-0565 and record the R70 PASS · C3 repair the test · C4 the `Landed:` line ·
C5 handback.

CONVENTION, binding on every count here, carried verbatim in force from the R70 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN25 AND NOSHELL. ITS ONE
END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD40 — listed rather than counted, per §3
checklist item 11. RECORD40 CARRIES ITS OWN LEADING BLANK LINES, so the separation its target's
convention requires is a property of bytes that were measured and never of a join shape that was
reasoned about.

## Change

C1 applies PLAN25F→PLAN25T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD40 to the END of `.agent/live_review.md`. C3 applies NOSHELLF→NOSHELLT to
`tests/test_command_discovery.py`, replacing exactly one test method body and nothing else. C4 appends
the single `Landed:` line NOSHELLLANDED to the END of `.agent/live_review.md`.

Change set, named rather than counted: `.agent/authored/f085-r71.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `tests/test_command_discovery.py`, `.agent/handoff.md`.
Nothing else. NO `docs/**` path is in that set, so no docs suite is ordered and Rule A4 is untouched.
ONE `.py` path is in it, so a lint gate IS ordered, over that path. NO file under `packages/` or
`apps/` is touched: the defect is in the TEST, not in the source it measures, and widening this round
into production code would be scope drift. Every path named in a gate below was resolved with
`git ls-tree 6a04b37b`, one call per path, before emission, per checklist item 24, and all of them
exist; `.agent/authored/f085-r71.md` is the one path no gate reads at the base, because C0a creates it.

WHAT BROKE AND WHY THE FIX GOES WHERE IT DOES. `tests/test_command_discovery.py` section M pins "no
shell=True in the execution path". Its `run_tests_local` case patched the name `subprocess.run` and
asserted `mock_run.called`. F085 T002b changed `run_tests_local` to call
`exec_guard.run_guarded_test_command` instead, and the guard spawns with `subprocess.Popen`, so the
patched name is never reached and the assertion fails on a property that is in fact still true. The
branch never touched that test file — the reviewer measured `git diff --stat a5a70621..6a04b37b --
tests/test_command_discovery.py` as EMPTY — so this is a test defeated by a move, not a test that was
edited wrong. The repair patches `subprocess.Popen` with a spy that DELEGATES to the real `Popen` and
asserts over every recorded spawn. That seam is strictly better than the old one: `subprocess.run` is
itself implemented on top of `Popen`, so the new assertion holds wherever the spawn is written and
cannot be defeated by moving it again — the reviewer confirmed this by mutation, below.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r71.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   6a04b37b and prints its own output here per checklist item 15, one reading per pair:
   PLAN25F→PLAN25T `TO contains FROM: false`; NOSHELLF→NOSHELLT `TO contains FROM: false`. Both are
   therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file. Each
   FROM occurs EXACTLY 1x in its target at 6a04b37b — the reviewer measured both.
4. RECORD40 AND NOSHELLLANDED HAVE NO FROM. Do not invent one for either and do not report a FROM
   count for either. Each is appended at the END of `.agent/live_review.md` in its own commit and owes
   the ORDERED EQUALITY of §4.9 as R-0531 narrows it: pre-commit blob a byte-exact PREFIX, slice an
   exact SUFFIX, and that commit's ADDED lines exactly the slice's lines IN ORDER.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the repair. Only C0a and C0b
   may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. NOTHING IN `.agent/live_review.md` THAT ALREADY EXISTS AT 6a04b37b IS EDITED, MOVED OR DELETED, and
   nothing already in `tests/test_command_discovery.py` at 6a04b37b is edited, moved or deleted EXCEPT
   the NOSHELLF bytes the pair replaces. No other test is renamed, retitled or removed, and no test is
   deleted to make a suite green.
7. Every sentence in RECORD40 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first.
8. THE ONE PIECE OF LEDGER TEXT YOU AUTHOR THIS ROUND IS THE `Landed:` LINE IN C4, AND ITS BYTES ARE
   GIVEN TO YOU AS NOSHELLLANDED — apply it verbatim like any other slice. Beyond it you author no
   ledger text: RECORD40 is reviewer text, and you do not add a `Done:` paragraph and do not edit
   RECORD40 to reconcile it with anything you measure. `Done:` is reserved for reviewer text and the
   resolution of R-0564 is written NEXT round, after the reviewer has verified this repair
   (docs/agents/planner_reviewer_prompt.md §4 item 4). A disagreement between RECORD40 and your own
   reading is a finding to REPORT in the handback, never to fix.
9. THIS ROUND REGISTERS TWO AND RESOLVES NONE. Registered moves 178 → 180, done stays 31, landed moves
   0 → 1, open moves 147 → 148, and the next free id becomes R-0566. RECORD40 carries exactly two
   `- R-` registration lines and no `Done:` line; NOSHELLLANDED is the single `Landed:` line. G6 proves
   all of it.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as its correction section fixes the ruled figure:
   490 lines TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three on the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r71.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, never delete or skip a
   test to make a suite green, and never widen the change set to route around a red. In particular, if
   the repaired test does not pass, do NOT adjust it and do NOT touch `packages/`.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors and real children that bind ports, so two concurrent
   runs redden each other on tests neither touched. The repaired test itself performs a REAL spawn — it
   runs pytest inside a temporary repository — which is why it is still bound by this constraint.
13. THE RED CONTROLS RUN ONLY INSIDE A DISPOSABLE `git worktree` AND NEVER IN THE PRIMARY CHECKOUT
   (G5 of docs/agents/self_drive_protocol.md). Create it, mutate there, read each colour, revert
   between the two controls, remove the worktree, and confirm `git worktree list` is one line at the
   end. The primary checkout must satisfy `git status --porcelain` empty at every commit.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. G8 creates and removes ONE disposable worktree; `git worktree
list` is one line at round start and one line at the end, and no worktree exists at any commit.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r71.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD40 line counts read
from that committed file, against constraint 10's 490 / 400 / 140, where PROSE is TOTAL minus the
slice lines.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN25F→PLAN25T is a REWRITE over `.agent/plan.md` at C1: report FROM 0x and TO exactly 1x over the
   post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - RECORD40 at C2 over `.agent/live_review.md`: report the ordered-equality readings constraint 4
   names — PREFIX, SUFFIX, `pre + slice` equal byte for byte, and that commit's ADDED lines exactly the
   slice's lines IN ORDER.
 - NOSHELLF→NOSHELLT is a REWRITE over `tests/test_command_discovery.py` at C3: report FROM 1x
   pre-commit and 0x post-commit with TO exactly 1x post-commit, and re-applying the extracted FROM→TO
   to the pre-commit blob must reproduce the post-commit blob BYTE-EXACTLY. Do NOT report an ADDED-line
   count for it: this is CODE and a rewrite, so §4.9's per-line prose count is not its obligation
   (R-0531).
 - NOSHELLLANDED at C4 over `.agent/live_review.md`: the same ordered-equality readings as RECORD40,
   measured against C4's own pre-commit blob and not against C2's.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0. Count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 12. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took every base reading below itself, in the primary checkout, at
6a04b37b.
 - `python3 -m pytest tests/test_command_discovery.py -q -rf` — the file C3 repairs. Its base reading
   at 6a04b37b is `1 failed, 91 passed`, EXIT 1: this gate is RED at the base BY DESIGN, because that
   single failure is the BLOCKER this round exists to repair. Exit 0 here is therefore a real move and
   not an already-green reading.
 - `python3 -m pytest tests/test_command_discovery.py -q -rf -k "TestNoShellTrue"` — the class holding
   the repaired test. Report how many were selected and how many passed.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` — base `44 passed`. The repair
   asserts over the guard's own spawn, so this file is re-run to show the repair moved nothing in it.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; these read `.agent/plan.md` and `.agent/live_review.md`, which C1, C2 and C4
   write.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 39 lines by applying the pair to that blob at 6a04b37b — two more than the round
before, because PLAN25T's `## Current Step` runs a line longer and its `## Next Steps` list carries one
item more than PLAN25F's.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
6a04b37b and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 178 / 31 / 0, 147 open, max registered R-0563, max resolved R-0563. At
HEAD the reading must be 180 / 31 / 1, 148 open, max registered R-0565 and max resolved still R-0563,
because constraint 9 rules this round registers two and resolves none. The registered symmetric
difference must be EXACTLY `{R-0564, R-0565}`, the landed symmetric difference EXACTLY `{R-0564}`, and
the done symmetric difference EMPTY. Next free id R-0566. Report all three symmetric differences, the
duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the one `.py` path this round edits, run from the repository root with the repository's
OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green at the base, so
both are ordered GREEN rather than compared as multisets; the reviewer executed both at 6a04b37b
itself, per R-0364, and both printed `All checks passed!`.
 - `python3 -m ruff check tests/test_command_discovery.py` — exit 0.
 - `python3 -m ruff check --preview tests/test_command_discovery.py` — exit 0. The preview half is
   ordered separately because ruff is preview-blind to the E301-E306 class (R-0500, R-0558).

G8 THE RED CONTROLS, run ONLY in a disposable worktree per constraint 13 and only AFTER C3 is
committed. The repaired test asserts an ABSENCE — no shell — which is the shape most likely to pass
for the wrong reason, so BOTH of its live assertions are proved reachable. The reviewer ran both of
these itself at 6a04b37b with the repair applied, and reports its own readings beside each.
 - Create the worktree from HEAD: `git worktree add --detach .remedy-wt/redctl-r71 HEAD`.
 - CONTROL (i), the shell assertion. In THAT worktree only, in
   `packages/orchestration/exec_guard.py`, insert the line `        shell=True,` immediately after the
   line `        argv,` that belongs to the `subprocess.Popen(` call — locate it by the three-line byte
   string `    proc = subprocess.Popen(` followed by `        argv,` followed by
   `        stdout=subprocess.PIPE,`. Count that three-line string in that file first and report the
   count, which must be 1 (§3 checklist item 25). Run
   `python3 -m pytest tests/test_command_discovery.py -q -rf -k "no_shell_true"` there: it must go RED.
   Report exit code, failed count and the assertion text. The reviewer's own reading was EXIT 1,
   `1 failed`, failing on `assert not call_kwargs.get("shell", False)` with `shell: True` present in
   the recorded kwargs. THEN REVERT that inserted line before control (ii).
 - CONTROL (ii), the non-vacuity guard. In THAT worktree only, in
   `packages/orchestration/test_runner.py`, replace the five-line call
   `        proc = run_guarded_test_command(` / `            argv,` /
   `            timeout_sec=timeout_sec,` / `            cwd=str(repo_root),` / `        )` with the
   single line `        proc = subprocess.CompletedProcess(argv, 0, b"", b"")` so that
   `run_tests_local` returns without spawning at all. Count that five-line string first and report the
   count, which must be 1. Run the same pytest command there: it must go RED. The reviewer's own
   reading was EXIT 1, `1 failed`, failing on `assert spawns` with the recorded list EMPTY.
 - Remove the worktree with `git worktree remove --force .remedy-wt/redctl-r71` and report that
   `git worktree list` is one line again and `git status --porcelain` in the primary checkout is empty.
 - Do NOT commit either mutation anywhere. If either control comes out GREEN, that is a STOP under
   constraint 11: report it and do not touch the repaired test.

G9 HYGIENE. `git diff --name-only 6a04b37b..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds no path
under `packages/`, `apps/`, `docs/` or `scripts/`, and exactly one path under `tests/`. Report the
list. Report per-commit insertions for every commit BEFORE C5 — C5 cannot measure itself, so its own
go in the round report — and confirm none exceeds 500. This branch spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint 11,
never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
6a04b37b, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3, C4
and C5, the real G1-G9 results with exit codes, the open-findings count and the next expected action.
The Bundle above holds more than five commits, so the ≤100-line cap AGENTS.md allows when a per-commit
table needs it applies; drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~100 % der Bauarbeit; das Integration Gate lief und hat GENAU EINEN echten Regress
gefunden — ein Test, der die alte Spawn-Stelle festnagelte, wurde durch die Migration entwertet und
ist hier auf die neue Naht nachgezogen, mit zwei Rot-Kontrollen. R70 PASS. Offen bleiben der zweite
Gate-Lauf und die Closure. Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R72 re-runs the
INTEGRATION GATE per docs/agents/integration_gate.md, because a repair after a gate invalidates that
gate's comparison; closure per docs/roadmap/STATUS_closure_protocol.md follows it. TWO: R71 carries no
verdict of its own, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4 item 13); R72 carries it, and R72 also writes the
reviewer-authored `Done: R-0564` that replaces this round's `Landed:` line. THREE: a standalone
closing line stating the open findings count and the next free id. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every
handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN25F
## Current Step
R70, this round: the INTEGRATION GATE, the first of the two full-suite runs this feature owes.
The branch suite and a merge-base suite run sequentially under restored parity, every branch-only
failure is attributed by direct evidence, and the comparison is REPORTED rather than predicted.
R69 PASSED: the denied fetch is now measured against a really listening server, with its control
in the same test body. No source file, no test and no document is touched this round.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN25F

BEGIN-PLAN25T
## Current Step
R71, this round: the repair the integration gate demanded. R70 PASSED and its gate found exactly
one real branch-only regression — `test_run_tests_local_no_shell_true` pinned a spawn site that
F085 T002b moved, so it failed on a property that still holds. The test is pulled to the new seam
and its two assertions are proved reachable by mutation. Registered as R-0564; the parity-digest
blindness the same gate surfaced is registered as R-0565. No production file is touched.

## Next Steps
1. Re-run the integration gate per docs/agents/integration_gate.md: a repair landed after a gate
   invalidates that gate's comparison, so the branch-versus-base reading is taken again.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the
   STATUS line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN25T

BEGIN-NOSHELLF
    def test_run_tests_local_no_shell_true(self, tmp_path):
        """run_tests_local must never pass shell=True to subprocess.run."""
        from unittest.mock import patch

        from packages.orchestration.test_runner import run_tests_local

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[project]\n")
        (repo / "tests").mkdir()
        job = _make_job()
        job.metadata["target_repo"] = str(repo)

        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=0,
            stdout=b"1 passed\n", stderr=b"",
        )
        with patch("subprocess.run", return_value=proc) as mock_run:
            run_tests_local(job, tmp_path)

        assert mock_run.called
        call_kwargs = mock_run.call_args.kwargs
        assert not call_kwargs.get("shell", False), "shell=True must never be used"
END-NOSHELLF

BEGIN-NOSHELLT
    def test_run_tests_local_no_shell_true(self, tmp_path):
        """run_tests_local must never spawn through a shell.

        F085 T002b moved the spawn rather than removing it: `run_tests_local` no
        longer calls `subprocess.run` at all, it calls
        `exec_guard.run_guarded_test_command`, which spawns with
        `subprocess.Popen`. The property this test exists to pin is unchanged —
        no shell, and argv passed as a list — so the test follows the spawn to
        its new seam instead of asserting against a call site that no longer
        runs. The spy DELEGATES to the real `Popen` rather than replacing it:
        the guard reads the child's pid, waits on it and pumps its streams, so a
        mock returning no real process would measure the mock and not the spawn.
        """
        from unittest.mock import patch

        from packages.orchestration.test_runner import run_tests_local

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[project]\n")
        (repo / "tests").mkdir()
        job = _make_job()
        job.metadata["target_repo"] = str(repo)

        real_popen = subprocess.Popen
        spawns = []

        def _record_then_really_spawn(*args, **kwargs):
            spawns.append((args, kwargs))
            return real_popen(*args, **kwargs)

        with patch("subprocess.Popen", side_effect=_record_then_really_spawn):
            run_tests_local(job, tmp_path)

        assert spawns, "run_tests_local must reach a real spawn"
        for call_args, call_kwargs in spawns:
            assert not call_kwargs.get("shell", False), "shell=True must never be used"
            argv = call_kwargs.get("args", call_args[0] if call_args else None)
            assert isinstance(argv, list), f"argv must be a list, got {type(argv)}"
END-NOSHELLT

BEGIN-RECORD40

Gate: R71 — the R70 entry. R70 PASSED as a round, and the INTEGRATION GATE IT RAN RETURNED A BLOCKER,
which are two different statements and both are true. The round is a PASS because every gate its block
ordered was executed and reported honestly and because the worker STOPPED at the blocker instead of
repairing it, which is what docs/agents/integration_gate.md step 4 requires; the gate is a BLOCKER
because a branch-only failure reproduces serially, does not reproduce at the merge base, and is
coupled to code this feature changed. Every gate reading below was re-taken by the reviewer over
126b70ae..6a04b37b rather than read from the handback, except `git status --porcelain` after each
intermediate commit and the absence of `.agent/STOP` at the two points R70's constraint 2 names, which
are unobservable once a round has ended and are accepted on the worker's report. TRANSPORT HELD,
disk-to-disk with the reviewer's OWN pre-emission original in the comparison and no digest fallback:
that original, the committed `.agent/authored/f085-r70.md`, the committed `.agent/last_block.md` at
6a04b37b and both working copies at 6a04b37b are all five byte-EQUAL at sha256
31f928b9466a6d46a22ed4be1da815f545419861ac9341f12a03cdff414442f3, 24310 B, 308 lines, 6 marker lines;
TOTAL 308 against the 490 cap, PROSE 232 against 400, RECORD38 54 against 140. THE SHAPES HELD:
PLAN24F→PLAN24T over `.agent/plan.md` at cdbcfb16 reads `TO contains FROM: false`, FROM 1x pre-commit
and 0x post-commit with TO exactly 1x post-commit, and re-applied reproduces the post-commit blob
BYTE-EXACTLY; RECORD38 over `.agent/live_review.md` at d2e65482 satisfies ORDERED EQUALITY on every
clause — PREFIX, SUFFIX, `pre + slice` equal byte for byte, ADDED lines equal to the slice's lines IN
ORDER, 54 and 54. Marker LINES at 6a04b37b are 0 in both edited files. THE PLAN CONTRACT HELD at
cdbcfb16: 37 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present. THE ARITHMETIC STOOD STILL AS THAT BLOCK'S CONSTRAINT 9 REQUIRED: 178 registered / 31 done /
0 landed and 147 open at both 126b70ae and 6a04b37b, all three symmetric differences EMPTY, and 0
duplicate ids and 0 orphan resolutions at both SHAs. THE CANARY WAS RE-RUN, NOT READ, in the primary
checkout: exit 0, `42 passed`. THE HYGIENE READING HELD: the range touches 15 paths, every one of them
under `.agent/`, none under `packages/`, `apps/`, `docs/`, `scripts/` or `tests/` and none ending
`.log`, over six single-parent commits inserting 308, 228, 7, 54, 262 and 112 lines, none over 500.

- R-0564 — High — a test that pinned a security-relevant property was silently defeated by this
feature's own migration, and no round gate could see it. `tests/test_command_discovery.py` section M
exists to pin "no shell=True in the execution path"; its `run_tests_local` case patched the name
`subprocess.run` and asserted `mock_run.called`. F085 T002b changed `run_tests_local` to call
`exec_guard.run_guarded_test_command`, which spawns with `subprocess.Popen` at
`packages/orchestration/exec_guard.py`, so the patched name is never reached, `mock_run.called` is
False, and the assertion fails at 6a04b37b on a property that is in fact still true of the source. The
reviewer reproduced it serially in the primary checkout at 6a04b37b — EXIT 1, `1 failed in 0.41s`,
`assert mock_run.called` — and confirmed the same id passes at the merge base a5a70621, where
`packages/orchestration/test_runner.py` still called `subprocess.run`. `git diff --stat
a5a70621..6a04b37b -- tests/test_command_discovery.py` is EMPTY: the branch never touched the failing
test, so the behaviour under test moved and the measurement did not follow it. High, not Medium,
because for the whole span between the migration and R70 this test was reporting on a call site that
no longer ran: had the guard passed `shell=True`, nothing in the suite would have said so, and every
round gate F085 ordered stayed green throughout — the R-0220 class, a green gate over a feature the
gate does not reach. COUNTER-MEASURE: when a round moves a spawn, a call or any other seam out of a
module, grep the suite for tests that patch the OLD name over that module — `rg -l '<old.name>' tests/`
followed by reading each `patch(` in what it returns — and pull each one to the new seam in the SAME
round that moves the seam. R70's gate is the only thing that caught this one, and a gate that runs
twice per feature is too coarse a net to be the first line. OPEN.

- R-0565 — Medium — the integration gate's own parity check is blind to the change it is meant to
detect. docs/agents/integration_gate.md orders `apps/ui/dist` hashed before and after the base run,
and a changed hash to void the parity claim; but the artifact's staleness is decided by MTIME, not by
content — `packages/orchestration/ui_server.py` treats the frontend as stale when any file under
`apps/ui/src` is newer than `apps/ui/dist/index.html` — and a rebuild that reproduces byte-identical
output leaves the digest equal while moving the mtime. R70's own evidence records exactly that at
6a04b37b: `.agent/gate_f085_r70/base_parity.txt` reports DIST_SHA256_BEFORE equal to DIST_SHA256_AFTER
and, beside it, mtimes showing `apps/ui/dist` was rewritten inside both checkouts mid-run, which is
also why the eight base-only ids failed. So the digest test reported parity intact over a run in which
the artifact was in fact rebuilt twice. Medium, not High, because that round did not rely on the
parity claim alone — every base-only id was additionally attributed per id by direct evidence, which
is the alternative integration_gate.md itself allows — and not Low, because the next gate that leans
on the digest alone will believe a parity claim that was never tested. COUNTER-MEASURE: the parity
reading records the artifact's MTIME alongside its sha256, and a moved mtime voids the claim exactly
as a changed digest does. The R70 worker measured this and declared it rather than fixing it, under
that block's constraint 9, which is why it is registered here. OPEN.
END-RECORD40

BEGIN-NOSHELLLANDED

Landed: R-0564 — the defeated no-shell test now spies on `subprocess.Popen`, delegating to the real
spawn, and asserts over every recorded spawn that no `shell=True` is present and that argv is a list;
`tests/test_command_discovery.py` only, in this round's C3.
END-NOSHELLLANDED
