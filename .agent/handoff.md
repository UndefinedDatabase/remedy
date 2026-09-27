# Handoff — F029, round 1

## Session

SESSION 1 of feature F029 · round 1 · rounds so far 1. Context remaining at
handback: comfortable — most of the round's context went to reading the
five source files the block named and drafting the module against S1–S6;
one repair loop was needed (G5's m1 mutation stayed green on the first
pass, fixed with one added test and a clean re-run), leaving ample context
had a further round been required this session.

## Range

Review of `b2863af4`..`HEAD` (`HEAD` is this handback's own commit, `F029
R1 C5`, on `feature/f029-subtree-rerun`).

## Commits

### c29a11694 F029 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r1-block.md | 342/0 | copy of this round's block |
| .agent/authored/f029-r1-context.md | 37/0 | copy of the context payload |
| .agent/authored/f029-r1-plan.md | 33/0 | copy of the plan payload |

Measured insertions: 412 (block's own line count 342 + 70), matching the
block's expectation exactly, under the 500-line cap.

### 97ef306b9 F029 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r1-claim.diff | 158/0 | copy of the claim diff payload |

Matches the block's expected insertions (158) exactly.

### a66c445bc F029 R1 C2: claim F029, re-head the live review record, book F028 R12, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 15/13 | rewrite from the context payload |
| .agent/decisions.md | 74/0 | DECISION F029 D1 appended |
| .agent/live_review.md | 24/21 | re-head (heading + intro paragraph + Steps) plus F028 R12's Gate entry appended |
| .agent/plan.md | 19/11 | rewrite from the plan payload |
| docs/roadmap/STATUS.md | 1/1 | F029's line `[ ]` → `[~]` |

Matches the block's expected numstat (15/13, 74/0, 24/21, 19/11, 1/1)
exactly. Applied via `git apply --check` (exit 0) then the real apply
(exit 0) of `claim.diff`, followed by the two payload rewrites.

### 4c55db2cd F029 R1 C3: reset a task's subtree to its state before the task as one proved commit
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 424/0 | new module: S1 constants/exceptions, S2 the subtree, S3 the walk, S4 the plan and refusal ladder, S5 the commit message, S6 the reset and its proof |
| tests/test_no_orphan_modules.py | 2/0 | `ALLOWED_UNWIRED` entry for the new, still-unwired module (T002 wires it) |

426 total insertions, under the 500-line cap; no split needed.

### 2f4be98b1 F029 R1 C4a: test the subtree reset (part 1 of what the block calls C4)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_subtree_rerun.py | 439/0 | new test file: S2–S6 coverage, 19 tests |

### d5b8fd0b9 F029 R1 C4b: add the mutation tool (part 2 of what the block calls C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r1-mutations.py | 156/0 | the G5 mutation (red-proof) tool |

C4a + C4b together are the block's single C4 ("the tests and the tool"),
split under constraint 2: 439 + 156 = 595 combined, over the 500-insertion
cap; each part alone is well under it.

### cbafa7b10 F029 R1 C4c: add the transitive-walk test G5's m1 mutation needs to catch it
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_subtree_rerun.py | 12/0 | one more `TestSubtreeIds` test: a dependent task (T4) listed BEFORE the dependencies it needs (T2, T3), which only a genuinely repeating walk resolves |

Added after G5's first run (at C4b) found mutation m1 ("S2 answers the
direct dependents only, with no transitive walk") stayed green — see
Deviations §2. Re-running G3/G4/G5 afterward at this commit is this
handback's canonical verification.

### F029 R1 C5: rewrite handoff for round 1 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- `git checkout -b feature/f029-subtree-rerun` from `main` at `b2863af4` —
  succeeded (Open PR Gate had already run before this round; `main` was
  already at the merge commit, so no pull).
- `git worktree add --detach .remedy-wt/f029-r1-mut d5b8fd0b9` (at C4b) for
  G5's first attempt — succeeded. `git worktree remove --force
  .remedy-wt/f029-r1-mut` then `git worktree prune` afterwards — both
  succeeded; `git worktree list | wc -l` read 61 before the add and 61
  after the remove.
- After C4c: `git worktree add --detach .remedy-wt/f029-r1-mut cbafa7b10`
  for G5's second attempt — succeeded. `git worktree remove --force
  .remedy-wt/f029-r1-mut` then `git worktree prune` afterwards — both
  succeeded; `git worktree list | wc -l` read 61 again.
- `git push -u origin feature/f029-subtree-rerun` after C5 — reported under
  G6 in this round's reply (run after this file is committed).
- No `gh pr create` (the block explicitly forbids it this round: the branch
  opens a pull request at F029's closure, not here), no `gh pr merge`, no
  checkout of `main` after the branch was cut, no branch deletion, no
  force-push, no `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `claim.diff`: 158 lines, 18109 bytes, sha256
  `5acca117cdc46dc66d71001b86e1cd9854334748b1156017f710326092beb13d`.
- `context.md`: 37 lines, 1569 bytes, sha256
  `c2ded9d16a6c91668c61b96cc6e5609be767d782263e183609fde54cbeb52c1b`.
- `plan.md`: 33 lines, 1208 bytes, sha256
  `259ad21a932f844e517a04f86d95ef04da23ebe2f349a1c1748a1290f193080d`.
- Block: 342 lines, sha256
  `bd1f5241306ee8a5e4a1355ef8ffb19b43c8d749901303f5770015bd865be3b1` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f029-r1-*` payload copy, read back with `git show
<commit>:<path>` from the commit that added it, compared byte-for-byte
(sha256) against its source: block/plan/context at `c29a11694`, claim.diff
at `97ef306b9` — all four MATCH (identical bytes and sha256 to the source).

### G2 — THE CLAIM
`git show a66c445bc:<path>`, bytes and sha256, each MATCHING the reviewer's
table exactly:
```
docs/roadmap/STATUS.md   bytes=55186    0b9fe9b1dd2eb6732d82cddaf83e483b8894ffd497576ba46de23b1246216775
.agent/live_review.md    bytes=307852   c63283daaf27049e3f19da677c9f6f6ef3ef5d7aaa58d2e2619fc890a09bfab3
.agent/decisions.md      bytes=2281119  2a107b591a6e9d10d0a259de0380b09fd7f96441ed93ba6c770cca5a8af65157
.agent/plan.md           bytes=1208     259ad21a932f844e517a04f86d95ef04da23ebe2f349a1c1748a1290f193080d
.agent/context.md        bytes=1569     c2ded9d16a6c91668c61b96cc6e5609be767d782263e183609fde54cbeb52c1b
```
All five MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text at `b2863af4` and at
`a66c445bc` (C2): `[]` both times — matching the reviewer's reading (empty
at both). At C2 the ledger has exactly one line reading `## Findings` and
exactly one reading `## Steps`; its last line begins `Gate: F028 R12 — the
F028 round 12 entry` — MATCH. F029's STATUS line at C2 reads in full `- [~]
F029 — Subtree rerun` — MATCH exactly. `git diff --name-only 97ef306b9
a66c445bc` names exactly: `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md` — the
table's five paths, no more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/subtree_rerun.py tests/orchestration/test_subtree_rerun.py tests/test_no_orphan_modules.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```
The whole refusal ladder of `plan_subtree_reset` (steps a–h) and the proof
block of `apply_subtree_reset`, quoted from `git show 4c55db2cd:packages/
orchestration/subtree_rerun.py` (this round's C3, unchanged by C4c which
only touched the test file):

```python
def plan_subtree_reset(job: JobPlan, root_task_id: str, worktree_path: str | Path) -> dict[str, Any]:
    """Read-only: the subtree, the walk and the target tree of a rerun from ``root_task_id``.

    Raises ``SubtreeRerunRefused`` from the first unsafe condition, in order:
    an unknown task, a copy-mode job, an uncommitted root task, a drifted or
    dirty worktree, a root commit not on the branch, a subtree task whose
    commit precedes the root's, and interleaving with work outside the
    subtree. Raises ``SubtreeRerunError`` when an EXACT reset's target tree
    disagrees with the tree before the root task — an invariant, never a user
    refusal.
    """
    subtree_ids = rerun_subtree_ids(job.tasks, root_task_id)          # a
    tasks_by_id = {t.task_id: t for t in job.tasks}
    root_task = tasks_by_id[root_task_id]

    if job.isolation_mode != "worktree":                              # b
        raise SubtreeRerunRefused(
            "not_worktree_mode",
            "the job ran in a copy of the repository, not on a job branch, "
            "so no task has a commit to go back to",
        )

    if not root_task.worktree_commit:                                 # c
        raise SubtreeRerunRefused(
            "task_not_committed",
            f"task {root_task_id} has no commit on the job branch yet, "
            f"so there is nothing to rerun",
        )

    live_head = W.head_at(worktree_path)
    if live_head != job.worktree_head:                                # d
        raise SubtreeRerunRefused(
            "worktree_drift",
            checkpoints.worktree_drift_message(job.worktree_head, live_head or "unknown"),
        )

    if not W.worktree_matches_head(worktree_path):                    # e
        listing = _join_listing(_status_paths(worktree_path))
        raise SubtreeRerunRefused(
            "worktree_dirty",
            f"the job worktree holds uncommitted changes to {listing}; "
            f"commit or discard them before a rerun",
        )

    root_commit = root_task.worktree_commit
    if not W.is_ancestor(worktree_path, root_commit, "HEAD"):         # f
        raise SubtreeRerunRefused(
            "commit_not_on_branch",
            f"task {root_task_id}'s commit {root_commit[:12]} is not on this job's branch",
        )

    base = W._git(worktree_path, "rev-parse", f"{root_commit}^").strip()
    commits = branch_commits_since(worktree_path, base)
    commit_shas = {c["sha"] for c in commits}

    for tid in subtree_ids:                                           # g
        task = tasks_by_id[tid]
        if task.worktree_commit and task.worktree_commit not in commit_shas:
            raise SubtreeRerunRefused(
                "subtree_order",
                f"task {tid} depends on {root_task_id} but its commit "
                f"{task.worktree_commit[:12]} is not after {root_task_id}'s on the job "
                f"branch; rerun from an earlier task",
            )

    subtree_id_set = set(subtree_ids)
    in_paths: set[str] = set()
    for commit in commits:
        if commit["task_id"] in subtree_id_set:
            in_paths.update(commit["paths"])

    interleaving: list[dict[str, Any]] = []
    for commit in commits:                                            # h
        if commit["task_id"] not in subtree_id_set:
            shared = sorted(set(commit["paths"]) & in_paths)
            if shared:
                name = commit["task_id"] or f"commit {commit['sha'][:12]}"
                interleaving.append({"by": name, "paths": shared})
    if interleaving:
        parts = "; ".join(f"{d['by']} changed {', '.join(d['paths'])}" for d in interleaving)
        raise SubtreeRerunRefused(
            "interleaved",
            f"rerunning {root_task_id} would also undo work outside its subtree: {parts}; "
            f"start the rerun at an earlier task whose subtree includes that work",
            facts={"interleaving": interleaving},
        )

    sorted_paths = sorted(in_paths)
    target_tree = _build_target_tree(worktree_path, base, sorted_paths)
    base_tree = W._git(worktree_path, "rev-parse", f"{base}^{{tree}}").strip()
    exact = all(commit["task_id"] in subtree_id_set for commit in commits)

    if exact and target_tree != base_tree:
        raise SubtreeRerunError(
            f"exact reset's target tree {target_tree} does not equal the tree before "
            f"{root_task_id}, {base_tree}",
        )
    ...
```

```python
def apply_subtree_reset(job: JobPlan, root_task_id: str, worktree_path: str | Path) -> dict[str, Any]:
    """Plan, then commit the reset — and prove it before handing the result back.
    ...
    """
    plan = plan_subtree_reset(job, root_task_id, worktree_path)

    branch = W._git(worktree_path, "rev-parse", "--abbrev-ref", "HEAD").strip()
    handle = W.WorktreeHandle(
        job_id=job.job_id, repo_path=job.repo_path, path=str(worktree_path), branch=branch,
    )
    restored = W.restore_tree(handle, plan["target_tree"])
    reset_commit = W.commit_job_worktree(str(worktree_path), build_rerun_commit_message(job, plan))
    reset_tree = W._git(worktree_path, "rev-parse", f"{reset_commit}^{{tree}}").strip()

    if reset_tree != plan["target_tree"]:
        raise SubtreeRerunError(
            f"tree_equals_target check failed: reset commit {reset_commit} has tree "
            f"{reset_tree}, expected {plan['target_tree']}",
        )

    for path in plan["paths"]:
        new_entry = _tree_entry(worktree_path, reset_commit, path)
        base_entry = _tree_entry(worktree_path, plan["base_commit"], path)
        if new_entry != base_entry:
            raise SubtreeRerunError(
                f"paths_equal check failed at {path!r}: reset commit entry {new_entry} "
                f"does not equal the entry before {root_task_id}, {base_entry}",
            )

    if plan["exact"] and reset_tree != plan["base_tree"]:
        raise SubtreeRerunError(
            f"tree_equals_base check failed: reset commit {reset_commit} has tree "
            f"{reset_tree}, expected {plan['base_tree']}",
        )
    ...
```

### G4 — THE TESTS
Final run, at C4c (this round's completed state):
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_subtree_rerun.py tests/orchestration/test_worktrees.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_veto.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
946 passed, 7 skipped in 90.41s (0:01:30)
REAL_EXIT=0
```
The reviewer's own baseline (same selection LESS `test_subtree_rerun.py`, at
`b2863af4` before any change) read `926 passed, 7 skipped` at exit 0. This
round's test file collects 20 nodes (`--collect-only -q` read `20 tests
collected`, after C4c's added test); 926 + 20 = 946, exactly this run's
total — no unexplained difference. The seven skips are the same F252
quarantines (6 in `test_named_bugs.py`, 1 in `test_agent_tooling.py`),
unchanged.

An earlier run at C4b (before C4c's added test) read `945 passed, 7
skipped` at exit 0, with the test file then collecting 19 nodes (926 + 19 =
945) — see Deviations §2.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
FIRST ATTEMPT, at C4b (`d5b8fd0b9`, before C4c existed): `git worktree add
--detach .remedy-wt/f029-r1-mut d5b8fd0b9` then `python3 -B
.agent/authored/f029-r1-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r1-mut`:
```
control (before): exit=0 failed=0 failing=[]
m1 S2 answers the direct dependents only, with no transitive walk: exit=0 failed=0 failing=[] caught=False
m2 .. m12: all caught=True (exit=1, failed>=1, real failing node ids)
control (after): exit=0 failed=0 failing=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
```
m1 stayed GREEN — reported as green, not papered over. Cause: the diamond
test's task order was already topologically sorted (dependencies always
precede their dependents in the list), so mutating the repeating `while` to
a single `if` still converges in one pass, because `included` is mutated
IN PLACE as the same pass scans forward past a just-added dependency. Fix:
added `test_transitive_walk_when_a_dependent_precedes_its_own_dependency_in_plan_order`
(C4c) — a dependent (T4) listed BEFORE the dependencies it needs (T2, T3),
which only a genuinely repeating walk resolves. `git worktree remove
--force .remedy-wt/f029-r1-mut` then `git worktree prune` — both exit 0;
`git worktree list | wc -l` read 61 afterwards.

SECOND ATTEMPT, at C4c (`cbafa7b10`, after the fix): `git worktree add
--detach .remedy-wt/f029-r1-mut cbafa7b10` then the same tool invocation,
whole output:
```
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f029-r1-mut
control (before): exit=0 failed=0 failing=[]
m1 S2 answers the direct dependents only, with no transitive walk: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestSubtreeIds::test_transitive_walk_when_a_dependent_precedes_its_own_dependency_in_plan_order'] caught=True
m2 S2 leaves the root out of the subtree: exit=1 failed=9 failing=[...9 nodes...] caught=True
m3 step d reads an unreadable live head ('') as matching: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestRefusalsAreSideEffectFree::test_worktree_drift_for_a_missing_worktree_path_names_unknown'] caught=True
m4 step e is skipped: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestRefusalsAreSideEffectFree::test_worktree_dirty_names_an_untracked_file'] caught=True
m5 a commit carrying no Remedy-Task trailer is classed IN the subtree: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestExactResetAndProof::test_interleaving_names_a_trailerless_commit_by_its_sha'] caught=True
m6 step h is skipped: exit=1 failed=2 failing=[...2 nodes...] caught=True
m7 a path base has no entry for is left in the target tree instead of removed: exit=1 failed=3 failing=[...3 nodes...] caught=True
m8 base is the root's commit itself instead of its first parent: exit=1 failed=7 failing=[...7 nodes...] caught=True
m9 S6 restores the worktree but makes no commit: exit=1 failed=4 failing=[...4 nodes...] caught=True
m10 step g is skipped: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestRefusalsAreSideEffectFree::test_subtree_order_for_a_dependent_commit_preceding_the_root'] caught=True
m11 exact is always True: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestExactResetAndProof::test_completed_elsewhere_task_outside_subtree_keeps_its_own_file'] caught=True
m12 S5 leaves out the Remedy-Rerun trailer: exit=1 failed=2 failing=[...2 nodes...] caught=True
control (after): exit=0 failed=0 failing=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 12 mutations red with at least one failing node each on this second
run. `git worktree remove --force .remedy-wt/f029-r1-mut` then `git
worktree prune`, both exit 0; `git worktree list | wc -l` read 61
afterwards, matching step 4's own reading both times.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f029-r1-block.md`, at `c29a11694`) vs
  `.remedy-wt/f029-r1/block.md`: byte-identical, sha256
  `bd1f5241306ee8a5e4a1355ef8ffb19b43c8d749901303f5770015bd865be3b1` both
  sides.
- `plan.md` copy (`.agent/authored/f029-r1-plan.md`, at `c29a11694`) vs
  `.remedy-wt/f029-r1-payloads/plan.md`: byte-identical, sha256
  `259ad21a932f844e517a04f86d95ef04da23ebe2f349a1c1748a1290f193080d` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `context.md` copy (`.agent/authored/f029-r1-context.md`, at `c29a11694`)
  vs `.remedy-wt/f029-r1-payloads/context.md`: byte-identical, sha256
  `c2ded9d16a6c91668c61b96cc6e5609be767d782263e183609fde54cbeb52c1b` both
  sides; used to rewrite `.agent/context.md` via `shutil.copyfile` at C2.
- `claim.diff` copy (`.agent/authored/f029-r1-claim.diff`, at `97ef306b9`)
  vs `.remedy-wt/f029-r1-payloads/claim.diff`: byte-identical, sha256
  `5acca117cdc46dc66d71001b86e1cd9854334748b1156017f710326092beb13d` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production module and its tests (`subtree_rerun.py`,
`test_subtree_rerun.py`) and the mutation tool (`f029-r1-mutations.py`) are
the WORKER's own authored code against the block's specification S1–S6, not
reviewer-authored text, so no fidelity comparison applies to them.

## Deviations & assumptions

1. C4 was split into C4a/C4b, departing from the block's literal
   single-commit-per-letter sequence. Justification: constraint 2's own
   500-insertion cap — the test file (439) plus the mutation tool (156)
   together are 595, over the cap combined — and constraint 2 explicitly
   names this exact split ("C4a and C4b") as the required response. Split
   by artifact: the test file in C4a, the mutation tool in C4b.
2. A THIRD commit, C4c, was added beyond the block's named C4/C4a/C4b:
   G5's first run (at C4b) found mutation m1 ("S2 answers the direct
   dependents only, with no transitive walk") stayed green — the diamond
   test's task list happened to be topologically sorted, so mutating the
   repeating `while changed:` loop to a single `if changed:` still
   converges, because `included` is mutated in place as the same forward
   pass scans past a just-added dependency. Constraint 4 explicitly
   provides for this: "a test this round itself wrote that is wrong may be
   corrected before C5, and the correction is declared" and G5's own text:
   "a mutation that stays green is reported as green, never papered over,
   and you then add the test that catches it in C4 before C5 and re-run
   the tool." C4c adds exactly one test — a dependent task listed BEFORE
   the dependencies it needs — and G3/G4/G5 were re-run in full afterward
   at the new HEAD; all readings in the Verification section above are
   from that final, post-C4c state except where the first G5 attempt is
   shown explicitly for the record.
3. The block gives exact, quotable wording for six of the eight refusal
   messages (a, b, c, d, e, h) but for two (f `commit_not_on_branch`, g
   `subtree_order`) says only what the message must NAME rather than its
   literal text. Assumption: composed prose meeting the stated naming
   requirement exactly (the task id and the first twelve characters of the
   relevant commit sha for `commit_not_on_branch`; the dependent task id,
   the root, its own commit's first twelve characters and the root's id
   again for `subtree_order`), verified against the block's own worked
   example in its test list ("subtree_order for a dependent whose commit
   precedes the root's").
4. `worktrees.is_ancestor` (step f) and `git rev-parse
   --abbrev-ref HEAD` (in `apply_subtree_reset`, to build the
   `WorktreeHandle`'s branch) are both called with `worktree_path` as the
   git repo argument, not `job.repo_path` — because `HEAD` must resolve to
   the JOB BRANCH's own tip (the worktree the rerun is being planned
   against), not the main checkout's `HEAD`. `job.repo_path` is used only
   where the specification names it directly (the `WorktreeHandle`'s
   `repo_path` field itself).
5. `plan_subtree_reset`'s `commit_not_on_branch` check and `git rev-parse
   <root_commit>^` (to compute `base`) assume the root task's commit
   always has a parent — true by construction, since every task commit
   lands strictly after the job's own base commit on the branch, and
   `task_not_committed` (step c) has already refused an uncommitted root
   before this point is reached. Not exercised as an edge case because the
   block's design (DECISION F029 D1) does not name a root-with-no-parent
   case.

No test went red unexpectedly beyond the one repair loop above (§2), no
reviewer payload was edited or retyped, and no gate was skipped.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | block named one commit "C4"; split into C4a/C4b under constraint 2's 500-line cap (see Deviations §1) |
| C4b | deviated | see C4a |
| C4c | deviated | additional commit beyond the block's named sequence, added to catch G5's m1 mutation which stayed green at C4b (see Deviations §2) |
| C5 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | run twice (at C4b pre-fix: 945 passed; at C4c post-fix: 946 passed), both exit 0, integrity clean both times |
| G5 | deviated | run twice: first attempt (at C4b) found m1 green, reported as green per constraint 4, not papered over; second attempt (at C4c, after adding the catching test) found all 12 mutations caught, restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 1,
then T002 — the rerun command behind the cost preview, the attempt counter
and the subtree's tasks returned to pending, earlier attempts' evidence
linked, and the model override recorded. Open findings (by
`open_finding_ids` at this round's head): 0. Operator questions open: 0.
