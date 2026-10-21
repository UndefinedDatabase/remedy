# Handback — F141 round 4: a dependency change or a deletion asks through a decision

## Session

SESSION 1 of feature F141 · round 4 · rounds so far 4

Context self-assessment: this worker verified every prepared digest, wrote the two predicates and
the decision path exactly to the block's given signatures, prefixes and sentences, kept
`job_apply.py` at its pinned 2541 lines with only the two named lines changed, wrote the tests from
the block's given behaviours, repaired a structure-ratchet violation gate 3 caught before finishing,
ran all six gates, and the context was far from exhausted.

Fortschritt: ~55 % (T001 and the read, write, commit, push, dependency and deletion seams landed ·
cost and network seams and T003 open) — Schätzung

## Range

Review of `d7648d91c`..`HEAD` on `feature/f141-permission-matrix` (base: round 3's handback).

## Commits

### 61446735e F141 R4 C1: book round 3, resolve R-1396, register R-1397 and R-1398, DECISION F141 D4
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r4.md` | +178/-0 | new: the block of this round |
| `.agent/decisions.md` | +10/-0 | DECISION F141 D4 |
| `.agent/live_review.md` | +8/-0 | round 3 booked, R-1396 resolved, R-1397 and R-1398 registered |
| `.agent/plan.md` | +9/-10 | re-headed for round 4 |

### a2ed8f9cc F141 R4 C2: a dependency change or a deletion asks through a decision (DECISION F141 D4)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/apply_permissions.py` | +189/-13 | new: `DEPENDENCY_MANIFEST_NAMES`, `is_dependency_manifest`, `MIGRATIONS_FOLDER`, `is_migration_path`, `PERMISSION_DECISION_TASK_ID`/`PERMISSION_APPROVE`/`PERMISSION_DECLINE`, and the decision path, split across `_discovered_actions`, `_decision_outcome` and `apply_permission_refusals` so no function crosses the structure ratchet's 100-line limit (a mid-round repair — see Deviations) |
| `packages/orchestration/job_apply.py` | +2/-2 | `_flag_refusals`'s two returns now pass `planned` and `found`/`[]` to `apply_permission_refusals` — file stays 2541 lines |

### b9ba080eb F141 R4 C3: tests of the predicates, the decision path, R-1397 and R-1398
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_apply_permissions.py` | +319/-11 | (j)-(k) the two predicates; (l)-(r) the decision path on stand-in objects (one raises, repeats idempotently, previews, is answered approve/decline, is pinned past `ask`, a migration path, R-1397's grant suppression); (s) a real git branch that deletes a tracked file, through the real `_flag_refusals` (see Deviations for why not the full `apply_job`); (t)-(u) R-1398's `do_push_mission` tests; the existing (a)-(f) call sites updated to the new four-argument signature, no assertion changed |

Exception (self-reference), per `docs/agents/handback_template.md`: this commit, which writes
`.agent/handoff.md`, is not tabled here — its own diff never appears in this file.

## External actions

None. The push after this commit: result in the worker's final reply to the operator (the handoff
cannot hold the result of the commit that writes it). No PR was opened, per this round's
instruction. No provider call, no rotation, no worktree, no merge.

## Verification

Preconditions: `block.md` (178 lines, sha256 matched), `verify.py`, `run_selection.py`,
`selection.txt` and `digests.txt` each matched the prompt's own sha256 before use; the four
`c1-*` files then matched `digests.txt` before being byte-copied.

1. `git status --porcelain` (before C1): empty. After C3 and before C4:
   `python3 .remedy-wt/f141-r4/prep/verify.py .`: every line `True`, `absent	C4`, last line
   `ALL True`.
2. `python3 -m ruff check` over every Python file C2 and C3 touched
   (`apply_permissions.py`, `job_apply.py`, `test_apply_permissions.py`): `All checks passed!`.
3. `python3 .remedy-wt/f141-r4/prep/run_selection.py . .remedy-wt/f141-r4-worker/selection-output.txt`:
   `paths 90`, `exit 0`, `4310 passed, 2 skipped in 80.92s (0:01:20)`, no FAILED or ERROR line, no
   `process(es) behind` line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252),
   `tests/test_install_smoke.py:175` (install smoke is opt-in).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check
   `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346,
   R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve as before this round.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
   `89`.
6. `git show --numstat --format=%h HEAD~1 -- packages/orchestration/job_apply.py`: `2	2`.

Structure measurement: `packages/orchestration/job_apply.py` read 2541 lines before C1 and reads
2541 lines after C2, and neither of its two edited lines changed the file's length.
`tests/test_structure_ratchet.py` caught, on the first run of gate 3, a 133-line
`apply_permission_refusals` with no ledger row; it was split into `_discovered_actions` and
`_decision_outcome` (pure extraction, no behaviour change — all 24 tests of
`test_apply_permissions.py` passed unchanged before and after) and the whole selection, including
`tests/test_structure_ratchet.py`, was re-run green. `docs/system/structure-ledger-v1.md` was not
touched.

## Authored-text proofs

C1: each of the four prepared files (`c1-.agent__authored__f141-r4.md`, `c1-.agent__decisions.md`,
`c1-.agent__live_review.md`, `c1-.agent__plan.md`) is a byte copy, proven by a Python sha256
equality at copy time (all `True`) and again by `verify.py`'s own byte comparison (all `True`).
Every prepared digest was checked before use and every one matched.

C2, C3: none applied. The block gave the exact function signatures, every refusal's prefix rule and
every WHY comment's substance by its literal text, and the test behaviours by their given
sentences — there was no prepared `.agent/authored/` file to byte-copy against for these commits,
only the block's own prose, checked by hand against it while writing.

## Deviations & assumptions

- Structure-ratchet repair folded back into C2: gate 3's first run (over the three commits as
  first written) failed on `tests/test_structure_ratchet.py`, naming a 133-line
  `apply_permission_refusals` with no ledger row. The worker first fixed this as a separate
  commit, then found the block's own `verify.py` requires the round's commits between the base and
  HEAD to count exactly as many as the `F141 R4 Cn:`-tagged ones — a fourth, differently-named
  commit could never satisfy that count. Nothing from this round had been pushed yet, so the
  worker used `git reset --soft` back to C1 (no `git commit --amend`, no `git rebase`, both still
  avoided) and re-committed C2 and C3 once each, C2 now carrying the split function from the
  start. `verify.py` and the full selection both passed green afterward. Recorded because it is a
  real departure from a clean first pass through the block's commit sequence, even though the
  final three commits land in the block's given order with the block's given paths.
- Item 3 of C3 (the history apply whose job branch deletes a tracked file) does not go through the
  full real `apply_job`, as the block's wording literally asks. Constructing that exact case —
  `apply_job`, `--commit-with-history`, a job branch that deletes a file tracked before the job —
  was tried three ways (the deleted file left out of every task's own manifest; added to a task's
  manifest; added together with `--skip-blocked`) and each one hit a different, pre-existing,
  unrelated gate of `_apply_from_workspace` first — a coverage check, a blocked-path check, and a
  skip-check `--commit-with-history` itself refuses to combine with `--skip-blocked` — confirmed by
  running each variant, not only reasoned about. Reaching the block's exact scenario through
  `apply_job` would need a change to one of those gates, and `job_apply.py` stays at 2541 lines
  this round with only the two lines the block names changed. The test instead calls the real,
  unmodified `_flag_refusals` directly, against a real git repository and a real job branch built
  by git plumbing (no working-tree or index write), which still exercises the new
  destructive-via-history-diff code, the real `_history_git` and the real decision-raising path
  end to end — just without the three unrelated gates this round does not touch. The test's own
  docstring carries this same explanation.
- The Session line adds `· rounds so far 4`, which the block's quoted text for this field does not
  give verbatim, to meet `docs/agents/handback_template.md`'s mandatory field (counting this
  round), matching round 3's handback precedent.
- `_decision_question`'s and `_decision_outcome`'s exact variable and helper names, and the split
  of `apply_permission_refusals` into `_discovered_actions` and `_decision_outcome`, are the
  worker's own structuring of the block's given behaviour — the block gave the sentences and the
  order of discovery, not a required internal shape, and the repair above constrained it further.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 4's verdict in the next round's first commit.
4. Round 5: the cost and network seams.

Operator questions open: 3.
Open findings: 89 (R-1397 and R-1398 owned by F141, repaired in C2 and C3).

The operator should read this round as finishing the write-up of what it means for Remedy to touch
a project's dependency file or delete one of its files during an apply. Until now, the permission
table could only say "ask" for those two things with no way for an approved apply to actually get
past the question other than raising the autonomy level for everything. Now a single approved
instance of either one raises one clear question with two answers, approve or decline, and the
apply stays refused and tells you exactly how to answer it until you do; declining, or leaving it
open, never lets the apply through, and approving it unblocks only that one instance, never a
standing change to policy. Nothing about commits, pushes or ordinary file writes changed. The whole
relevant test collection ran and passed. Three questions from before this feature still wait for
you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `61446735e` |
| C2 | done | `a2ed8f9cc` (repaired in place before C3, see Deviations) |
| C3 | done | `b9ba080eb` |
| C4 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 4310 passed, 2 skipped |
| Gate 4 | done | fail_count 1, the twelve findings; 89 open |
| Gate 5 | done | 89 |
| Gate 6 | done | `2	2` |
