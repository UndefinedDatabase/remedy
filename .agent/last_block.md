── STEP T003 / round 49 — F275 ───────────────────────────────
Goal:        Repair R-0876, the defect round 48's widen landed: two production sites wrap
             a value that can be `None` in `str(...)`, so an artifact that belongs to no
             task records the string `"None"` instead of the absence
             `packages/core/models.py` documents. Guard both with tests that go red
             without the fix.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r49.md`
             C0b  mirror it into `.agent/last_block.md` from the committed blob
             C1   slice PLAN49 — whole-file replacement of `.agent/plan.md`
             C2   slices RECORD49, FIND49 and SLIPS49 — the round 48 FAIL verdict, the
                  registration of `R-0876`, and one dated reviewer slip
             C3   THE REPAIR — pairs PAIR49A and PAIR49B, then code appends GUARD49A and
                  GUARD49B
             C4   slice LANDED49 — the `Landed: R-0876` line, appended after the fix
             C5   the handback, rewriting `.agent/handoff.md`

Change:      EXACTLY these paths and nothing else.
             `.agent/authored/f275-r49.md`  (new) · `.agent/last_block.md` ·
             `.agent/plan.md` · `.agent/live_review.md` · `.agent/prose_slips.md` ·
             `packages/orchestration/do_run.py` ·
             `packages/orchestration/test_failure_artifact.py` ·
             `tests/orchestration/test_do_run.py` ·
             `tests/orchestration/test_test_failure_repair.py` · `.agent/handoff.md`
             NO path under `apps/`, `docs/` or `scripts/` moves this round, and
             `.agent/decisions.md` is NOT touched — this round makes no new decision, it
             repairs a defect an existing one caused.

Constraints:
 1. Apply every slice BYTE FOR BYTE; extract each mechanically from the COMMITTED blob of
    `.agent/authored/f275-r49.md` by its `BEGIN-<name> ` / `END-<name> ` marker-line
    PREFIX. Never retype, reflow or edit one. A slice that looks wrong is applied as given
    and DECLARED.
 2. The commit order C0a, C0b, C1, C2, C3, C4, C5 is FIXED — none merged, none reordered.
    C4 comes AFTER C3 because a `Landed:` line may only be written once the fix it
    describes is committed.
 3. EVERY length is `len(<bytes>)` from `read_bytes()` or a `git show` byte stream, never
    `len()` over a decoded `str`.
 4. The four appends — RECORD49, FIND49, SLIPS49, LANDED49 — are `old_bytes +
    slice_bytes` in Python. Each owns its leading blank line. All pre-blobs end in a
    newline; add none. GUARD49A and GUARD49B are CODE appends and obey the same rule.
 5. This round REGISTERS `R-0876` and RESOLVES nothing. Write the `Landed: R-0876` line at
    C4 and NO `Done:` paragraph — only reviewer-authored text sets a resolution, and the
    reviewer authors it at the next gate. The open set goes 86 at the base to 87 at C4.
 6. The two pairs are REWRITES, established by the containment test rather than by eye:
    for each, the test's own output reads `TO contains FROM: false`, so the FROM-zero
    count applies and G6 orders it.
 7. Destructive verification — the red proof in G7 — runs ONLY inside a disposable
    `git worktree` under the gitignored `.remedy-wt/`, removed and pruned before the
    handback. The primary checkout satisfies `git status --porcelain` == empty at every
    commit.
 8. Re-read `.agent/STOP` FROM DISK before the first commit and report what you found.

Done when:   the gates below, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
             one line per gate in the handback, EVERY reading taken at C4 or earlier.
             Report the number of gates YOU ran; this block states none.

 G1  TRANSPORT, at C0b. sha256 over the bytes of `.agent/authored/f275-r49.md` equals the
     digest the delegation message states — this block carries marker lines for its SLICES
     only and no BEGIN marker of its own. `.agent/last_block.md` is written from
     `git cat-file blob <C0a-sha>:<that path>` and never retyped. Report both byte counts
     and both digests, and state the chain the proof walked. Claim nothing about the bytes
     emitted into your prompt.

 G2  THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to slice PLAN49: both byte counts, both
     sha256 digests, the line count against the AGENTS.md cap of 50, `^## Goal$` exactly 1x
     and `^## Next Steps$` exactly 1x.

 G3  THE RECORD AND THE SLIPS, at C2, then the record again at C4. Read every pre and post
     blob with `git show <sha>:<path>` INTO MEMORY — never write a non-current revision
     over a tracked file.
     (i)  `.agent/live_review.md` ← RECORD49 then FIND49, applied in that order inside C2,
          pre at C1 and post at C2, all three readings:
          (a) reader A: pre_bytes + RECORD49 + FIND49 == post_bytes, `identical: True`.
          (b) reader B, structural: N is the number of blank-line-separated paragraphs your
              script COUNTS across the two slices — never a number this block asserts — and
              the LAST N blank-line units of the post blob equal those N paragraphs IN
              ORDER, stripped.
          (c) negative control: flip ONE byte inside the FIRST appended paragraph of the
              IN-MEMORY copy; reader A rejects AND reader B rejects, each re-run against
              the ORIGINAL slices.
     (ii) `.agent/prose_slips.md` ← SLIPS49, pre at C1 and post at C2, reading (a) alone.
     (iii) `.agent/live_review.md` ← LANDED49, pre at C3 and post at C4, reading (a) alone.

 G4  THE TWO PAIRS, at C3, against COMMITTED blobs. For EACH pair report: the containment
     test's own output, which reads `TO contains FROM: false`; the FROM count in the base
     blob `70d6c8e6`, which is 1; the FROM count in the C3 blob, which must be 0; and the
     TO count in the C3 blob, which must be 1. Then REBUILD the C3 blob from the base blob
     by applying that pair alone and report byte-identity.

 G5  THE TWO GUARDS, at C3, as CODE APPENDS and therefore by ORDERED EQUALITY, not by a
     per-line count — a code slice repeats blank lines and closing brackets structurally,
     so multiplicity is unattainable by construction. For EACH of
     `tests/orchestration/test_do_run.py` ← GUARD49A and
     `tests/orchestration/test_test_failure_repair.py` ← GUARD49B, all three:
     the base blob at `70d6c8e6` is a byte-exact PREFIX of the C3 blob; the slice is a
     byte-exact SUFFIX of the C3 blob; and the lines that C3's diff ADDS for that path are
     exactly the slice's lines IN ORDER.

 G6  THE REPAIR WORKS AND NOTHING NEAR IT MOVED, at C3.
     (a) `git rev-parse C3:packages` must equal `1f1a040413f8045a9e53ec8dece733ddb1d0c0ac`
         and `git rev-parse C3:tests` must equal
         `b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee`. At the base `70d6c8e6` the same two
         read `18aadcb1ca69b2aa25a14044750bbe2e0883d2d0` and
         `67b33dc0be4345b55badd92b1af6b1af105cfffd`. These are the reviewer's own
         measurement of this repair applied to a clean checkout; a digest that differs
         means your tree is not the tree that was measured, so report it and stop.
     (b) `git diff --numstat 70d6c8e6..C3` reads exactly four rows: 1/1 `do_run.py`,
         1/1 `test_failure_artifact.py`, 21/0 `test_do_run.py`, 26/0
         `test_test_failure_repair.py`. Report every row you measured.
     (c) The SCOPED round gate, in the primary checkout at C3:
         `python3 -m pytest tests/orchestration/test_do_run.py
         tests/orchestration/test_test_failure_repair.py
         tests/orchestration/test_repair_loop_v1.py tests/cli/test_repair_runtime.py
         tests/orchestration/test_ci_budgets.py -q`
         and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both
         last lines and both exit codes. `test_ci_budgets.py` is in the selection because
         this round edits production expressions and that test freezes the ruff count at 26.

 G7  THE RED PROOF, at C3, in a disposable worktree under `.remedy-wt/` detached at C3,
     never `cd`-ed into: every command as `subprocess.run([...], cwd=<abs worktree>)`,
     under `python3 -B`, `__pycache__` purged before every run, the imported module's path
     PRINTED before any result is believed. The selection for every run is
     `tests/orchestration/test_do_run.py::TestSystemArtifactKeepsTaskIdAbsent` AND
     `tests/orchestration/test_test_failure_repair.py::TestSystemArtifactKeepsTaskIdAbsent`.
     TWO mutations, because there are two fixes and one mutation cannot prove both:
       1. CONTROL, unmutated — report the exit code and the last line.
       2. M1 — in `packages/orchestration/do_run.py`, revert PAIR49A's TO to its FROM.
          Count the TO string in THAT FILE first and report the count; it must be 1.
          Report the exit code, the last line and the FAILED node ids.
       3. REVERT, proved by sha256 against a digest recorded BEFORE the mutation.
       4. M2 — the same for PAIR49B in
          `packages/orchestration/test_failure_artifact.py`.
       5. REVERT, proved the same way.
       6. CONTROL again, green.
     THE TWO NODE-ID SETS MUST BE DISJOINT and you report both sets: M1 reddens the
     `test_do_run.py` guard and M2 the `test_test_failure_repair.py` guard. If they are
     not disjoint, do not adjust anything — report it. Then remove and prune the worktree
     and report that `git worktree list` reads ONE entry.

 G8  NOTHING ELSE MOVED, at C4. `.agent/STOP` ABSENT from disk, re-read and not
     remembered. `git status --porcelain` EMPTY, as the literal string. Over
     `70d6c8e6`..C4 the changed-path set equals the Change list MINUS `.agent/handoff.md`,
     which C5 writes after C4: report MISSING and EXTRA as lists, both `[]`. ZERO paths
     under `apps/`, `docs/` or `scripts/`, and `.agent/decisions.md` ABSENT from the set.
     THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md`: distinct `^- R-\d+ — `
     minus distinct `^Done: R-\d+ — ` reads 104 − 18 = 86 at the base and must read
     105 − 18 = 87 at C4. Report the ids registered — `['R-0876']` — and resolved — `[]`.
     Then `^Landed: R-0876 ` 0 at C3 and exactly 1 at C4, and `^Done: R-0876 ` 0 at C4.
     Report each of C0a..C4's own insertion count against the F104 D1 cap of 500, derived
     ONCE from `git show --numstat <sha>` and used both here and in the `+/-` column of the
     handback's `## Commits` table.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 19 of F275,
             round 49, the item-status table with every ordered item exactly once, the
             deviations, and one sentence of context self-assessment.
──────────────────────────────────────────────────────────────

WHAT THE REVIEWER ALREADY MEASURED. This repair was applied to a clean checkout at
`70d6c8e6` and run. The two guards were written FIRST and run against the UNFIXED code,
where both go red on `assert 'None' is None` — the defect stated in the assertion's own
words. With the fix the selection in G6(c) reads `175 passed` at exit 0 and the canary
`42 passed` at exit 0, and `ruff check .` reports 26, the frozen ceiling.

────────── SLICES ──────────
The authored texts follow, in the order their commits apply them: PLAN49, RECORD49, FIND49,
SLIPS49, PAIR49A, PAIR49B, GUARD49A, GUARD49B, LANDED49. Each is delimited by its own
`BEGIN-`/`END-` marker lines; the marker lines are NOT part of any slice and never reach a
target file. Every rule line in this block's frame is a run of U+2500 BOX DRAWINGS LIGHT
HORIZONTAL, and no rule LENGTH is load-bearing: markers are matched by prefix and the frame
carries no appliable bytes.

Slice shapes, mechanically. PLAN49 is a WHOLE-FILE REPLACEMENT. RECORD49, FIND49, SLIPS49
and LANDED49 are prose APPENDS applied as `old_bytes + slice_bytes`. GUARD49A and GUARD49B
are CODE APPENDS, proved by ordered equality under G5. PAIR49A and PAIR49B are the round's
only FROM→TO pairs and both are REWRITES by the containment test quoted in constraint 6;
each pair's FROM and TO are given as their own slices so that neither is ever retyped.

BEGIN-PLAN49 ─────────────────────────────────────────────────
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 49 repairs `R-0876`, which round 48's id-shape widen landed and its worker declared.
The generator wrapped two construction keywords in `str(...)` whose value can be `None`, so
an artifact produced by orchestration rather than by a task recorded the string `"None"`
instead of the absence `packages/core/models.py` documents — a truthy value no lookup
matches. Both sites move the `str(...)` inside the conditional's true branch, and both gain
a test that goes red without the fix on `assert 'None' is None`. The round 48 FAIL verdict
is booked here.

## Next Steps

1. RE-RUN THE FLIP DRY RUN against a tree whose id shape is one spelling, and re-classify
   the residue `.agent/f275_t003_flip_residue.md` records at 2714 failures. The 256
   hexadecimal-UUID and 369 model-validation failures should be gone; what remains is the
   transform rules section 3 of that artefact enumerates.
2. THE FLIP, still as the one declared-oversize commit AGENTS.md permits per feature,
   declared with its inseparability reason before review.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 stands at 49 rounds and 19 sessions against the operator's soft limit of 60 rounds
  and 20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1, which also forbids the split-and-close default here.
- A mechanical wrap applied to a construction keyword is only safe where the value cannot
  be `None`. `R-0876` is that class; the flip's own transform wraps nothing, but its
  `**`-splat rule will face the same question.
- The open set is 87 by distinct id once this round registers `R-0876`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN49 ───────────────────────────────────────────────────

BEGIN-RECORD49 ───────────────────────────────────────────────

Gate: F275 R48 — the F275 round 48 entry. VERDICT FAIL, and the fault is the REVIEWER'S, not the round's. Written by the planner and reviewer of session 19 after reading the committed range `05631ba3`..`70d6c8e6` and RE-DERIVING EVERY ONE of the round's eight gates INDEPENDENTLY against the committed blobs. EVERY GATE THE BLOCK ORDERED IS GREEN ON THE REVIEWER'S OWN MEASUREMENT, and the round still fails, because a round PASS requires the diff to be clean and this diff carries two wrong lines. THE DEFECT, registered here as `R-0876`: slice WIDEN48 wraps every construction keyword it rewrites in `str(...)` unconditionally, and at two production sites the wrapped expression can evaluate to `None` — `packages/orchestration/do_run.py` writes `task_id=str(job.tasks[0].id if job.tasks else None)` and `packages/orchestration/test_failure_artifact.py` writes `task_id=str(UUID(failure.task_id) if failure.task_id else None)`. `packages/core/models.py` documents the convention both violate in its own docstring — `task_id = None` means the artifact came from orchestration rather than from a Task — so the widen turns a documented ABSENCE into the truthy string `"None"`, which `artifact_index.task_artifacts_by_kind` can never match. No test covers either branch, which is why every ordered gate stayed green. THE WORKER FOUND IT, DECLARED IT AND DID NOT EDIT IT, which is exactly right: constraint 1 forbids editing a slice, the worker applied the generator as ordered, proved its tree byte-identical to the tree the reviewer measured, and raised the two sites for a ruling as the first substantive paragraph of its handback. THE REST OF THE ROUND IS CORRECT AND THE REVIEWER RE-DERIVED ALL OF IT. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the saved copy, its mirror and the reviewer's surviving original are one blob at 34051 bytes and sha256 `47750c3be1aab6831d8eaec0f9fa19685065cbf3e12901b474d3bf5183e82e14`. G2: `.agent/plan.md` byte-identical to PLAN48 at 2600 bytes over 45 lines. G3 and G4: all three appends reconstruct exactly — `.agent/live_review.md` 888735 to 892396, `.agent/prose_slips.md` 239271 to 240453 and `.agent/decisions.md` 1080309 to 1085053 — with reader B true at N counted from each slice, N being 1 and 7, and both negative controls rejected by BOTH readers with the flipped byte inside the FIRST appended paragraph. G5: the open set is 86 BY DISTINCT ID at the base and at C4, nothing registered and nothing resolved, and `^- R-0876 — ` reads 0 at both — the gate anchored on the registration form precisely because the bare token occurs in that round's own ledger prose. G6 IS THE GATE THE ROUND EXISTS FOR AND BOTH HALVES HOLD: importing the shipped classes gives `Artifact.task_id` as `str | None` and `PatchIntentSet.task_id` as `<class 'str'>`, and BOTH SUBTREE DIGESTS EQUAL THE REVIEWER'S OWN REPLAY OF THE TWO GENERATORS FROM A CLEAN CHECKOUT — `packages` at `18aadcb1ca69b2aa25a14044750bbe2e0883d2d0` and `tests` at `67b33dc0be4345b55badd92b1af6b1af105cfffd` — which fixes every byte of both directories rather than a list of paths that could drift. The reviewer re-ran the scoped selection itself at `480 passed, 2 skipped` and the canary at `42 passed`, both exit 0. G7's red proof was re-run by the reviewer in its own disposable worktree at C3: control `52 passed` at exit 0, M1 reverting the single `str(task_id)` in `artifact_index.py` reads `2 failed, 50 passed` at exit 1 over two named node ids, the revert is byte-exact by sha256, the control is green again, and the PRIMARY checkout's porcelain read empty throughout. G8: 58 changed paths, ZERO under `apps/`, `docs/` or `scripts/`, and insertions 425, 238, 20, 4, 132 and 14. THE WORK IS KEPT — the widen itself is right and the id shape is now one spelling across all four fields the flip feeds — and round 49 repairs the two lines and guards both.
END-RECORD49 ─────────────────────────────────────────────────

BEGIN-FIND49 ─────────────────────────────────────────────────

- R-0876 — Medium. A mechanical `str(...)` wrap applied to a construction keyword whose value can be `None` turns a documented ABSENCE into the string `"None"`. Landed at F275 round 48's C3 `2b395e02` by slice WIDEN48, which wraps every keyword it rewrites unconditionally because `ast` gives it no way to know whether the expression is nullable. TWO SITES, both production, both constructing an `Artifact`: `packages/orchestration/do_run.py` inside `_run_build_phase`, where a job with no tasks has no task to attribute the artifact to, and `packages/orchestration/test_failure_artifact.py` inside `persist_failure_artifact`, where `TestFailureArtifact.task_id` defaults to the empty string. `packages/core/models.py` states the convention in the `Artifact` docstring itself — `task_id = None` means the artifact was produced by orchestration or system logic and is not tied to a Task — and `packages/orchestration/artifact_index.py`'s `task_artifacts_by_kind` matches that field by equality, so a stored `"None"` is a truthy value no lookup will ever match and no reader expects. Measured at `2b395e02`: both sites read as described, and the repo-wide sweep for the pattern `task_id=str(<expr> if <cond> else None)` returns exactly these two. NOT CAUGHT BY ANY GATE THE ROUND ORDERED, and that is the honest part of the record: the subtree digests matched, the scoped suite read 480 passed and the canary 42 passed, because no test exercises either branch — the empty-task-list path and the empty-`task_id` path are both unreached by the suite. THE FIX: move the `str(...)` inside the conditional's true branch at both sites, so the false branch still yields `None`, and add a test at each that constructs the artifact through the real function on the absent branch and asserts `task_id is None`. Both tests must go red without their fix; the reviewer measured them doing so, on `assert 'None' is None`. THE RULE THIS LEAVES BEHIND, binding on the next block that orders a mechanical wrap: a generator that wraps an expression states what it assumes about that expression's NULLABILITY, and where it cannot know, the block sweeps for the conditional form before emission rather than after.
END-FIND49 ───────────────────────────────────────────────────

BEGIN-SLIPS49 ────────────────────────────────────────────────

2026-09-11 · F275 R48 · DECISION F275 D28 attributes the four `tests/test_grouped_cli.py` failures that appeared under DECISION F275 D27's three-field scope to the assignment coupling between `Artifact.task_id` and `PatchIntentSet.task_id`, and says the widen order was the cause. The COUPLING is measured and the CHOSEN ruling rests on it independently — `patch_intent.py` builds `PatchIntentSet(task_id=artifact.task_id, ...)` at one site, which the reviewer read directly. The ATTRIBUTION of those four specific failures is not measured, and `tests/conftest.py` documents a different mechanism that produces exactly that symptom: a leaked `REMEDY_DATA_DIR` makes `save_job()` write to a stale temp root while the CLI subprocess resolves the real one, which its own docstring records as having turned every `test_grouped_cli.py` JSON test into "Job not found", order-dependently. The reviewer never isolated the two. D28's ruling stands because it rests on the assignment rather than on the failures, and its landed text is not rewritten; this line is the correction the append-only record takes. THE RULE THAT FOLLOWS: a decision may cite a failure set as CORROBORATION only when the alternative explanations the repository already documents have been excluded, or it says which reading it did not take.
END-SLIPS49 ──────────────────────────────────────────────────

BEGIN-PAIR49A_FROM ───────────────────────────────────────────
        task_id=str(job.tasks[0].id if job.tasks else None),
END-PAIR49A_FROM ─────────────────────────────────────────────

BEGIN-PAIR49A_TO ─────────────────────────────────────────────
        task_id=str(job.tasks[0].id) if job.tasks else None,
END-PAIR49A_TO ───────────────────────────────────────────────

BEGIN-PAIR49B_FROM ───────────────────────────────────────────
        task_id=str(UUID(failure.task_id) if failure.task_id else None),
END-PAIR49B_FROM ─────────────────────────────────────────────

BEGIN-PAIR49B_TO ─────────────────────────────────────────────
        task_id=str(UUID(failure.task_id)) if failure.task_id else None,
END-PAIR49B_TO ───────────────────────────────────────────────

BEGIN-GUARD49A ───────────────────────────────────────────────


class TestSystemArtifactKeepsTaskIdAbsent:
    """The same convention at the other site F275 round 48's id-shape widen reached.

    `_run_build_phase` attributes its artifact to the job's first task, and a job with no
    tasks has none to attribute it to — which the artifact records as an ABSENT `task_id`,
    not as the string "None".
    """

    def test_the_build_phase_on_a_task_less_job_leaves_task_id_absent(
        self, tmp_path, monkeypatch
    ):
        from packages.orchestration.do_run import _run_build_phase
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        job = Job(name="no-tasks")
        assert job.tasks == []
        artifact = _run_build_phase(job, "a goal", tmp_path, data_dir)
        assert artifact.task_id is None
END-GUARD49A ─────────────────────────────────────────────────

BEGIN-GUARD49B ───────────────────────────────────────────────


class TestSystemArtifactKeepsTaskIdAbsent:
    """A system-produced artifact carries `task_id = None`, never the string "None".

    `packages/core/models.py` states the convention every artifact lookup relies on:
    `task_id = None` means the artifact came from orchestration rather than from a Task,
    and `artifact_index.task_artifacts_by_kind` matches on equality. F275 round 48's
    id-shape widen wrapped the whole conditional in `str(...)`, which turned that absence
    into the truthy string `"None"` that no lookup matches and no reader expects.
    """

    def test_a_failure_without_a_task_leaves_task_id_absent(self, tmp_path):
        job, _task, _data_dir, old = _make_job(tmp_path)
        try:
            failure = TestFailureArtifact(
                artifact_id="temp",
                job_id=str(job.id),
                task_id="",
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            art = persist_failure_artifact(job, failure)
            assert art.task_id is None
        finally:
            _cleanup_env(old)
END-GUARD49B ─────────────────────────────────────────────────

BEGIN-LANDED49 ───────────────────────────────────────────────

Landed: R-0876 — both `str(...)` wraps moved inside their conditional's true branch, so an artifact that belongs to no task records `None` again, and each site gained a test that goes red without its fix; all in this round's C3. The reviewer's authored `Done:` is owed at the next gate.
END-LANDED49 ─────────────────────────────────────────────────
