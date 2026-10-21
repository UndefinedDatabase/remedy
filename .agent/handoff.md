# Handback — F141 round 1: claim, book F078 R11, the seam inventory, DECISION F141 D1, Q23 and T001

## Session

SESSION 1 of feature F141 · round 1 · rounds so far 1

Context self-assessment: this worker verified every prepared digest, copied the eight prepared files, wrote the matrix module and its tests from the block's given sentences, ran all six gates, and the context was far from exhausted.

Fortschritt: ~20 % (claim, inventory and T001 landed · the seams and T003 open) — Schätzung

## Range

Review of `43e470560`..`HEAD` on `feature/f141-permission-matrix` (base: `main` at `43e470560`, the merge commit of pull request 373).

## Commits

### c42cc0c15 F141 R1 C1: claim F141, book F078 R11, the seam inventory, DECISION F141 D1 and Q23
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r1.md` | +220/-0 | new: the block of this round |
| `.agent/context.md` | +11/-12 | re-headed for F141 |
| `.agent/decisions.md` | +32/-0 | DECISION F141 D1 |
| `.agent/f141_inventory.md` | +114/-0 | new: the T001 seam inventory |
| `.agent/live_review.md` | +17/-24 | re-headed for F141; F078 R11 booked |
| `.agent/operator_questions.md` | +27/-0 | Q23 |
| `.agent/plan.md` | +19/-13 | re-headed for F141 |
| `docs/roadmap/STATUS.md` | +1/-1 | F141 `[ ]` to `[~]` |

### 4365a8b25 F141 R1 C2: the push switch and the permission matrix with its one check (T001)
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | +1/-0 | regenerated: the new `REMEDY_AUTONOMY_ALLOW_PUSH` row |
| `packages/orchestration/config_keys_autonomy.py` | +12/-0 | the `autonomy.allow_push` key |
| `packages/orchestration/permission_matrix.py` | +318/-0 | new: the matrix, its check, the grants record |
| `tests/test_no_orphan_modules.py` | +2/-0 | `ALLOWED_UNWIRED` entry for the new module |

### cc5ec51d9 F141 R1 C3: a test per cell and per answer of the permission matrix
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_permission_matrix.py` | +407/-0 | new: a test per cell and per answer |

Exception (self-reference), per `docs/agents/handback_template.md`: this commit, which writes
`.agent/handoff.md`, is not tabled here — its own diff never appears in this file.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` at session start: `[]` (no open pull request; the Open PR Gate passed without a merge).
- The push after this commit: result in the worker's final reply (the handoff cannot hold the result of the commit that writes it).
- No provider call, no rotation, no worktree, no merge, no pull request created.

## Verification

Preconditions: `git rev-parse HEAD` read `43e4705604bd33707db741bd1d5ec9679fc9df89` on `main`, clean `git status --porcelain`, before any write. `gh pr list --state open ...` read `[]`. Every prepared digest (`block.md` 220 lines, and `verify.py`, `run_selection.py`, `selection.txt`, `digests.txt`, each by its own sha256) matched the prompt before use; the eight `c1-*` files then matched `digests.txt` before being copied.

1. `git status --porcelain` (before C4): empty. `python3 .remedy-wt/f141-r1/prep/verify.py .`: every line `True`, `absent	C4`, last line `ALL True`.
2. `python3 -m ruff check packages/orchestration/config_keys_autonomy.py packages/orchestration/permission_matrix.py tests/test_no_orphan_modules.py tests/orchestration/test_permission_matrix.py`: `All checks passed!`.
3. `python3 .remedy-wt/f141-r1/prep/run_selection.py . .remedy-wt/f141-r1-worker/selection-output.txt`: `paths 77`, `exit 0`, `3584 passed, 2 skipped in 43.14s`, no FAILED or ERROR line, no `process(es) behind` line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (install smoke is opt-in).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve as before this round.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`: `87`.
6. `python3 -c "from packages.orchestration.permission_matrix import PermissionRequest as P, require_permission as r; print(r('dependency_change', P(level='L2', subject='probe')))"`: outcome `ask`, reason `"Autonomy level L2 asks before Remedy may change your project's dependencies ((dependency_change, L2) = ask): approve this instance, or raise the level to L4 with its decision record."`, naming `L4`.

## Authored-text proofs

C1: each of the eight prepared files (`c1-.agent__authored__f141-r1.md`, `c1-.agent__context.md`, `c1-.agent__decisions.md`, `c1-.agent__f141_inventory.md`, `c1-.agent__live_review.md`, `c1-.agent__operator_questions.md`, `c1-.agent__plan.md`, `c1-docs__roadmap__STATUS.md`) is a byte copy, proven by a Python sha256 equality at copy time (all `True`) and again by `verify.py`'s own byte comparison (all `True`). Every prepared digest was checked before use and every one matched.

C2, C3: none applied. The block gave the exact sentences of the new config key's description, the module's docstring and WHY comments, and every refusal and reason string by its literal text — there was no prepared `.agent/authored/` file to byte-copy against, only the block's own prose, checked by hand against it while writing.

## Deviations & assumptions

None.

## For the operator, in plain sentences

Remedy is starting work on a new table that says, for each level of how much it may do on its own, what the work it starts may then actually do: read your files, write a result into them, commit, push, change a dependency, delete something, spend above your cost limit, or reach the network. This round decided the table itself, asked you a question about it, and wrote the one piece of code that will answer every later check against it, together with a test for every square of the table. Nothing in your project behaves differently yet, because nothing calls the new check so far; that starts in the next few rounds, one group of actions at a time. The whole relevant test collection ran and passed. A question about the table waits for you, already answered with this session's recommendation, alongside two older questions from before this feature.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 1's verdict in the next round's first commit.
4. Round 2: the pinned level and the read seam.

Operator questions open: 3.
Open findings: 87.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f141-permission-matrix` at `43e470560` |
| C1 | done | `c42cc0c15` |
| C2 | done | `4365a8b25` |
| C3 | done | `cc5ec51d9` |
| C4 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3584 passed, 2 skipped |
| Gate 4 | done | fail_count 1, the twelve findings; 87 open |
| Gate 5 | done | 87 |
| Gate 6 | done | outcome ask, naming L4 |
