# Handback — F141 round 5: BLOCKED after C4, gate 3 reds outside the round's named paths

## Session

SESSION 1 of feature F141 · round 5 · rounds so far 5

Context self-assessment: this worker verified every prepared digest, wrote the cost-prompt and
networked-child seams and the prompt's own approval kind exactly to the block's given signatures,
prefixes and sentences, kept `job.py` at 2483 lines and `exec_guard.py` at exactly 1000, wrote the
tests from the block's given behaviours including R-1399's through the real `apply_job` and
`_flag_refusals` paths, then found gate 3 red on a test outside every file the block named for this
round and stopped rather than invent an unauthorized repair commit.

Fortschritt: ~65 % (T001 and every seam landed in code and in C1-C4 · gate 3 unconfirmed because of
the out-of-scope regression below · T003 open) — Schätzung

## Range

Review of `092343da4`..`HEAD` on `feature/f141-permission-matrix` (base: round 4's handback).

## Commits

### 4d6583e0e F141 R5 C1: book round 4, resolve R-1397 and R-1398, register R-1399, DECISION F141 D5
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r5.md` | +154/-0 | new: the block of this round |
| `.agent/decisions.md` | +10/-0 | DECISION F141 D5 |
| `.agent/live_review.md` | +8/-0 | round 4 booked, R-1397 and R-1398 resolved, R-1399 registered |
| `.agent/plan.md` | +10/-9 | re-headed for round 5 |

### 4d568a510 F141 R5 C2: the cost prompt asks the permission matrix (DECISION F141 D5)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/permission_matrix.py` | +7/-2 | `APPROVAL_KIND_PROMPT`, `InstanceApproval` accepts it, `_approved_by` answers for it |
| `apps/cli/cost_preview_confirm.py` | +34/-1 | `confirm_cost_preview` gains `job_id`/`yes_flag`, asks `require_permission("expensive", ...)` on `yes` and on a confirmed prompt, docstring paragraph naming DECISION F141 D5 |
| `apps/cli/commands/job.py` | +2/-2 | `_cmd_job_run_cycles`'s two existing lines widened in place (`yes_flag=...`, `job_id=job_id_str`); file unchanged at 2483 lines |
| `apps/cli/commands/job_rerun_cmd.py` | +1/-1 | its call passes `job_id=job_id` |

### cb0f8b939 F141 R5 C3: a child that keeps the network asks the permission matrix (DECISION F141 D5 (3))
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +10/-10 | `plan_child_spawn` asks `require_permission("external_call", ...)` for a child that keeps the network; the three given lines reflowed to positional args (121 chars over the 120 limit with the keyword spelling — see Deviations); docstring rewrapped to 120 columns, same words and paragraph breaks, three lines shorter; file stays exactly 1000 lines |

### ccbfb7d45 F141 R5 C4: tests of the cost and network seams, and R-1399
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_cost_preview_confirm.py` | +121/-0 | the flag grant at L2 (`--yes` and `--unattended`), the prompt grant naming the command, the declined/cheap/missing-terminal no-grant cases, the L5 allow-and-still-prompts case |
| `tests/orchestration/test_exec_guard.py` | +35/-0 | `plan_child_spawn` asks `external_call` once when the policy keeps the network, never when it denies it, and raises on a `deny` cell put in with `monkeypatch.setitem` |
| `tests/orchestration/test_permission_matrix.py` | +27/-0 | the prompt kind is accepted and its allow-sentence names the command |
| `tests/orchestration/test_apply_permissions.py` | +61/-0 | R-1399 through the real paths: a plain and a `--commit` approved apply of a `pyproject.toml`-writing job both block `apply_failed` naming `(dependency_change, L2) = ask` and the new decision; `_flag_refusals` at the late call over a dirty tracked target refuses and grants nothing |

## External actions

None yet. No push was made — gate 3 is red and this handback's own commit has not landed; the push
after it, if authorized, is the next round's first action. No PR was opened, per this round's
instruction.

## Verification

Preconditions: `block.md` (154 lines, sha256 `12f6aa4f...de0004f` matched), `verify.py`,
`run_selection.py`, `selection.txt` and `digests.txt` each matched the prompt's own sha256 before
use; the four `c1-*` files then matched `digests.txt` before being byte-copied, and the copies were
proven byte-equal by sha256 at copy time.

1. `git status --porcelain` (before C1): empty. After C4: `python3 .remedy-wt/f141-r5/prep/verify.py .`
   — every line `True`, `absent	C5`, last line `ALL True`.
2. `python3 -m ruff check` over every Python file C2, C3 and C4 touched (`permission_matrix.py`,
   `cost_preview_confirm.py`, `job.py`, `job_rerun_cmd.py`, `exec_guard.py`, and the four test
   files): `All checks passed!`.
3. **RED.** `python3 .remedy-wt/f141-r5/prep/run_selection.py . .remedy-wt/f141-r5-worker/selection-output.txt`:
   `paths 95`, `exit 1`, `1 failed, 4539 passed, 2 skipped in 86.19s (0:01:26)`. The one failure:
   `tests/orchestration/test_long_run_executor.py::TestJobRunCommand::
   test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended` —
   `TypeError: ...fake_confirm() got an unexpected keyword argument 'yes_flag'`, raised from
   `job.py:1248` calling `confirm_cost_preview(... yes_flag="--yes" if yes else "--unattended", ...)`
   against the test's own strict-signature stand-in
   (`def fake_confirm(estimate, *, confirm_above_usd, yes, command_name, json_output=False):`).
   No other FAILED/ERROR line; no `process(es) behind` line. SKIPPED:
   `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175`
   (install smoke is opt-in).
4. `python3 -m apps.cli.main integrity check --json`: `fail_count` 1, the one failing check
   `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346,
   R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve as before this round.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
   `88`.
6. `wc -l packages/orchestration/exec_guard.py apps/cli/commands/job.py`: `1000` and `2483`.

## Authored-text proofs

C1: each of the four prepared files (`c1-.agent__authored__f141-r5.md`, `c1-.agent__decisions.md`,
`c1-.agent__live_review.md`, `c1-.agent__plan.md`) is a byte copy, proven by a Python sha256
equality at copy time (all `EQUAL`) and again by `verify.py`'s own byte comparison (all `True`).
Every prepared digest was checked before use and every one matched.

C2, C3, C4: none applied. The block gave the exact signatures, the matrix's own three new lines,
the docstring's words and paragraph breaks, and the tests' behaviours by its literal prose; there
was no prepared `.agent/authored/` file to byte-copy against for these commits.

## Deviations & assumptions

- **C3's three given lines, reflowed.** The block's literal third line —
  `require_permission("external_call", PermissionRequest(level=pinned_job_level(None), subject="a
  networked child"))` at 8-space indent — measures 121 characters, one over ruff's 120-character
  limit, so the block's own clause ("reflowed only if ruff's 120-character limit requires it, and
  then keeping three lines") applies. Reflowed to positional arguments —
  `PermissionRequest(pinned_job_level(None), "a networked child")`, matching the dataclass's own
  `level, subject, job_id=None, approval=None` field order — which reaches 107 characters and keeps
  the three lines ruff would otherwise want to break across more than three. No semantic change:
  `job_id` and `approval` still default to `None`, exactly as the keyword spelling left them.
- **GATE 3 RED, no repair commit made.** `job.py`'s call of `confirm_cost_preview` gained the
  keyword `yes_flag` exactly as DECISION F141 D5 (2) and the block's C2 item 3 order, and this is
  the only caller the block names. `tests/orchestration/test_long_run_executor.py` carries a second,
  independent caller of the same production function (`_cmd_job_run_cycles` via the CLI command
  module) whose own test replaces `confirm_cost_preview` with a strict-signature `fake_confirm` that
  does not accept the new keyword; the block's Bundle section does not list this file, and this
  worker's own pre-commit check of C2 (ruff, the structure ratchet, and the files the block names)
  did not catch it — a gap in this worker's own process, not only the block's. The constraint "If a
  gate goes red after a commit, repair it in a NEW commit only if the block names one; otherwise
  stop and report" names no repair commit for this file, so none was made: no reset, no amend, no
  rebase, and no new commit outside the block's four. The fix, read from the one failure, is narrow:
  give `fake_confirm` the same `job_id=None, yes_flag="--yes"` keywords (or `**_kw`) the real
  signature now carries; no assertion in that test changes. This is recorded here rather than
  guessed at in a repair, per the Commit Gate's "no existing assertion changes" rule and this
  round's own instruction not to invent an unauthorized commit.
- **C5 does not carry the block's prescribed success content.** The block's own C5 section
  specifies `Fortschritt: ~65 % (T001 and every seam landed · T003 open)`, a `Next` section naming
  only forward steps, and `Open findings: 88 (R-1399 owned by F141, repaired in C4)` — all written
  for a round whose six gates are green. Gate 3 is red. This handback instead states the true,
  blocked status: C1-C4 are committed, the code and the tests described by the block are written
  and self-consistent, and the one red gate is outside this round's own changes. `Fortschritt` is
  kept at `~65 %` (it is accurate: T001 and every seam ARE landed in the code and in C1-C4; what is
  missing is gate 3's confirmation, not a seam), but `Next` opens with the repair gate 3 needs
  before C5-as-success and the push can happen, and no push is reported because none was made.
- Per this round's own instruction, mutation red-proofs were not run, the full suite was not run
  beyond the one selection run (gate 3), `REMEDY_TEST_MAX_WORKERS` was not set, and no two test
  commands ran at the same time.
- **C5 also carries `.agent/plan.md`, not only `.agent/handoff.md`.** The block's C5 path is
  `.agent/handoff.md` alone. `AGENTS.md`'s own "State Update Triggers" make `.agent/plan.md` MUST be
  updated "when a blocker is encountered" and before every commit, and `AGENTS.md` wins any conflict
  with a prepared block. Gate 3's red is exactly that blocker, so this commit also rewrites
  `plan.md`'s Current Step, Next Steps and Risks to state it, rather than leave the plan reading a
  round that finished clean.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. The repair gate 3 needs: widen `fake_confirm` in `test_long_run_executor.py` to accept `job_id`
   and `yes_flag`, re-run gate 3, and only then this round's C5-as-success and the push.
4. Book round 5's verdict in the next round's first commit.
5. Round 6: the rendered table, the guards and a fixture per level (T003).

Operator questions open: 3.
Open findings: 88 (R-1399 owned by F141, repaired in C4).

The operator should read this round as code-complete but not yet confirmed: the cost prompt and a
networked child now both ask the same permission table the rest of the feature already asks, each
with its own clear answer for who approved it, and the tests of both are written and pass on their
own. The one thing standing between this and a normal green handback is a single other test
elsewhere in the project that stands in for this prompt with a narrower shape than the prompt now
has, and that one stand-in needs one more keyword added to it before the whole project's test
collection is shown green again. Nothing about commits, pushes or ordinary file writes changed.
Three questions from before this feature still wait for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `4d6583e0e` |
| C2 | done | `4d568a510` |
| C3 | done | `cb0f8b939` |
| C4 | done | `ccbfb7d45` |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | deviated | ran RED: `test_long_run_executor.py`'s `fake_confirm` rejects `yes_flag`; no repair commit authorized by the block |
| Gate 4 | done | fail_count 1, the twelve findings; 88 open |
| Gate 5 | done | 88 |
| Gate 6 | done | `1000` and `2483` |
| C5 | deviated | written as a blocked handback, not the block's prescribed success content (see Deviations) |
| Push | skipped | blocked by gate 3; not attempted |
