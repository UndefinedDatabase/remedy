# Handback — F141 round 3: the apply's write, commit and push, and `remedy do`'s push, ask the matrix

## Session

SESSION 1 of feature F141 · round 3 · rounds so far 3

Context self-assessment: this worker verified every prepared digest, wrote the new module and the
two in-place seams exactly to the block's given signatures and sentences, wrote the tests from the
block's given behaviours, ran all six gates, and the context was far from exhausted.

Fortschritt: ~45 % (T001, the read seam and the apply's write, commit and push landed · dependency,
deletion, cost and network seams and T003 open) — Schätzung

## Range

Review of `10905b495`..`HEAD` on `feature/f141-permission-matrix` (base: round 2's handback).

## Commits

### ffe941dad F141 R3 C1: book round 2, resolve R-1395, register R-1396, DECISION F141 D3, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r3.md` | +175/-0 | new: the block of this round |
| `.agent/decisions.md` | +10/-0 | DECISION F141 D3 |
| `.agent/live_review.md` | +6/-0 | round 2 booked, R-1395 resolved, R-1396 registered |
| `.agent/plan.md` | +9/-12 | re-headed for round 3 |
| `.agent/prose_slips.md` | +1/-0 | round 2's `try:` span slip |

### 742b9e81c F141 R3 C2: the apply's write, commit and push ask the permission matrix (DECISION F141 D3)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/apply_permissions.py` | +93/-0 | new: `apply_permission_refusals`, `push_permission_refusals`, `grant_push_permission`, `WRITE_PERMISSION_REFUSED` |
| `packages/orchestration/job_apply.py` | +4/-4 | one sorted import; `_flag_refusals`'s two returns now add the matrix's refusals; `_push_landed_commit`'s tuple assignment joined into one line — file stays 2541 lines |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.apply_permissions`, now reachable from `job_apply.py` |

### 7cbf535ad F141 R3 C3: remedy do's push asks the permission matrix (DECISION F141 D3 (4))
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_apply.py` | +12/-1 | `do_mission_push_refusals` adds `push_permission_refusals` after the upstreams', before the mission's; `do_push_mission` grants each repository's push before pushing it, naming the sentence and failing the step on a refusal |

### b4b626473 F141 R3 C4: tests of the apply's and remedy do's permission seams, and R-1396
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_apply_permissions.py` | +228/-0 | new: (a)-(f) on stand-in objects, (g)-(i) through the real `apply_job` / `do_mission_push_refusals` paths |
| `tests/orchestration/test_builder_context.py` | +20/-0 | R-1396: a job pinned at `L4` with only its `read` cell denied refuses `run_pingpong`, citing `L4` |

Exception (self-reference), per `docs/agents/handback_template.md`: this commit, which writes
`.agent/handoff.md`, is not tabled here — its own diff never appears in this file.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` at session start: `[]` (no open pull request; the Open PR Gate passed without a merge).
- The push after this commit: result in the worker's final reply (the handoff cannot hold the result of the commit that writes it).
- No provider call, no rotation, no worktree, no merge, no pull request created.

## Verification

Preconditions: every prepared digest (`block.md` 175 lines, and `verify.py`, `run_selection.py`,
`selection.txt`, `digests.txt`, each by its own sha256) matched the prompt before use; the five
`c1-*` files then matched `digests.txt` before being byte-copied.

1. `git status --porcelain` (before C5): empty. `python3 .remedy-wt/f141-r3/prep/verify.py .`: every line `True`, `absent	C5`, last line `ALL True`.
2. `python3 -m ruff check` over every Python file C2, C3 and C4 touched (`apply_permissions.py`, `job_apply.py`, `do_apply.py`, `test_apply_permissions.py`, `test_builder_context.py`): `All checks passed!`.
3. `python3 .remedy-wt/f141-r3/prep/run_selection.py . .remedy-wt/f141-r3-worker/selection-output.txt`: `paths 88`, `exit 0`, `4180 passed, 2 skipped in 67.96s (0:01:07)`, no FAILED or ERROR line, no `process(es) behind` line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (install smoke is opt-in).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve as before this round.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`: `88`.
6. `git show --numstat --format=%h HEAD~2` restricted to `job_apply.py`: `4	4`.

Structure measurement: `packages/orchestration/job_apply.py` read 2541 lines before C1 and reads
2541 lines after C2; neither function the structure ledger lists for it (`_apply_from_workspace`,
`apply_job`, `summarize_job_apply`) changed size, and `docs/system/structure-ledger-v1.md` was not
touched.

## Authored-text proofs

C1: each of the five prepared files (`c1-.agent__authored__f141-r3.md`, `c1-.agent__decisions.md`,
`c1-.agent__live_review.md`, `c1-.agent__plan.md`, `c1-.agent__prose_slips.md`) is a byte copy,
proven by a Python sha256 equality at copy time (all `True`) and again by `verify.py`'s own byte
comparison (all `True`). Every prepared digest was checked before use and every one matched.

C2, C3, C4: none applied. The block gave the exact function signatures, every refusal's prefix
rule and every WHY comment's substance by its literal text, and the test behaviours by their given
sentences — there was no prepared `.agent/authored/` file to byte-copy against for these commits,
only the block's own prose, checked by hand against it while writing.

## Deviations & assumptions

- Working order: the worker wrote and ruff-checked the C2, C3 and C4 code in the working tree
  before staging and committing C1, instead of committing C1 first as the block's C1 paragraph
  implies ("confirm ... git status --porcelain is empty first"). By the time C1 was staged, the
  tree also carried the unstaged C2/C3/C4 edits, so that literal precondition did not hold. This
  changed nothing about what each commit contains: C1 was staged and committed with exactly its
  five ordered paths, verified by sha256 and `git diff --cached --numstat` before the commit, and
  C2 through C4 followed in the block's order with their own ordered paths. Recorded because it is
  a real departure from the block's stated sequence, even though every commit's content and order
  landed exactly as ordered (finding R-0485's rule).
- The Session line adds `· rounds so far 3`, which the block's quoted text omits, to meet
  `docs/agents/handback_template.md`'s mandatory field (counting this round); the block's own
  quoted substring is unchanged within it.
- `do_push_mission`'s refusal sentence on a denied grant is the worker's own wording (the block
  only ordered that a sentence it answers stops the walk, becomes the push record's error, and
  fails the step naming it): `f"{denied}{before}{named}"`, `before` naming any repository already
  pushed, `named` the open/unchecked criteria sentence already built for this push, matching the
  shape of the existing failed-push branch two lines below it. No test exercises this exact branch;
  the block's own C4 list names no test for it, and the normal case (the push switch on, a flag or
  key approval given) returns `""` and was exercised by (g), (h), (i) and the untouched `remedy do`
  push tests already in the selection.

## For the operator, in plain sentences

This round connects the apply of a job's reviewed work, and the one push a full run of several
jobs makes at the end, to the permission table this feature is building. Before any file is
written, a commit is made or anything is pushed, the apply now asks whether the level that job was
allowed to run at permits each of those three things; a level that forbids one of them stops the
apply cold, the same way a refusal from any of the apply's existing checks already did, so nothing
new can be denied twice. A level that only asks is granted once, right before the thing it covers
happens, with the command flag that approved it recorded as the reason. The single run's own push,
at the very end of several jobs, now asks the same question once per repository it pushes, and a
missing approval there stops the remaining pushes instead of letting them through silently. A gap
left open at the end of last round, where nothing proved that a job's own allowed level, rather than
the default one, actually reached the check that decides whether its work may even be read, is
closed and tested. The whole relevant test collection ran and passed. Three questions from before
this feature still wait for you.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 3's verdict in the next round's first commit.
4. Round 4: the dependency and deletion predicates and their seams.

Operator questions open: 3.
Open findings: 88 (R-1396 owned by F141, repaired in C4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `ffe941dad` |
| C2 | done | `742b9e81c` |
| C3 | done | `7cbf535ad` |
| C4 | done | `b4b626473` |
| C5 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 4180 passed, 2 skipped |
| Gate 4 | done | fail_count 1, the twelve findings; 88 open |
| Gate 5 | done | 88 |
| Gate 6 | done | `4	4` |
