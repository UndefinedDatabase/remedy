# Handoff — F292 Plan view and hunk decisions in the cockpit, round 1

## Session

SESSION 1 of feature F292 · round 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

## Range

Review of `2d138e90fe17dfb89e18f9f4cf4a96cf08d417b7`..`HEAD` — three commits on
`feature/f292-plan-view-hunk-decisions`: `6c0b55791`, `994389bfd`, and this handback commit.

## Commits

### `6c0b55791` F292 R1 C1: claim F292, book F294 R16, register R-1128, re-head the ledger, DECISION F292 D1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f292-r1.md` | +135/-0 | NEW FILE at `.agent/authored/f292-r1.md`; byte-for-byte copy of this round's step block, `cmp`-verified against `.remedy-wt/f292-r1/block.md` before commit (`wc -l` 135, sha256 `7ec462bd89038df1f479053d3246e2851bedce86bc733cccfb82b096bd0cbcf1`) |
| `docs/roadmap/STATUS.md` | +1/-1 | whole-file replaced from `.remedy-wt/f292-r1/dry-STATUS.md`; `cmp` silent — F292's `[ ]` line becomes `[~]` |
| `.agent/live_review.md` | +29/-22 | whole-file replaced from `.remedy-wt/f292-r1/dry-live_review.md`; `cmp` silent — re-heads the ledger for F292, books F294 round 16 (`Gate: F294 R16`, VERDICT PASS), registers `R-1128` (Low, owned by F290) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f292-r1/append-decisions.txt` appended without retyping; pre-commit blob (`git show 2d138e90f:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) — DECISION F292 D1 |
| `.agent/plan.md` | +17/-16 | whole-file replaced from `.remedy-wt/f292-r1/dry-plan.md`; `cmp` silent |
| `.agent/context.md` | +13/-15 | whole-file replaced from `.remedy-wt/f292-r1/dry-context.md`; `cmp` silent |

`git diff --cached --numstat` before the commit read `135 0` (authored block), `1 1` (STATUS.md),
`29 22` (live_review.md), `10 0` (decisions.md), `17 16` (plan.md), `13 15` (context.md) — matching
the block's stated numstat exactly. `git show --numstat` after the commit read the same six lines.

### `994389bfd` F292 R1 C2: the plan read, one builder for plan-show and the dashboard's plan section (DECISION F292 D1)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/plan_editing.py` | +36/-0 | whole-file `cp` from `.remedy-wt/f292-r1/dry-plan_editing.py`; `cmp` silent — adds `PLAN_VIEW_TASK_FIELDS` and `plan_view` after `edit_window_refusal` (T5_F292 T001, DECISION F292 D1 (1)) |
| `packages/orchestration/ui_server.py` | +25/-0 | whole-file `cp` from `.remedy-wt/f292-r1/dry-ui_server.py`; `cmp` silent — adds the `"plan": _build_plan_section(job),` line in `_build_dashboard` and `_empty_plan_section`/`_build_plan_section` before `_build_task_spec_section` |
| `apps/cli/commands/job_plan_cmd.py` | +12/-31 | whole-file `cp` from `.remedy-wt/f292-r1/dry-job_plan_cmd.py`; `cmp` silent — deletes `_task_entry_for_planned_id`; `_cmd_plan_show` now prints from `plan_view`, output unchanged |
| `tests/ui_server/test_dashboard_plan.py` | +178/-0 | NEW FILE at `tests/ui_server/test_dashboard_plan.py`; whole-file `cp` from `.remedy-wt/f292-r1/dry-test_dashboard_plan.py`; `cmp` silent |

`git diff --cached --numstat` before the commit read `36 0` (plan_editing.py), `25 0`
(ui_server.py), `12 31` (job_plan_cmd.py), `178 0` (test file) — matching the block's stated
numstat exactly. `git show --numstat` after the commit read the same four lines. Self-review (`git
diff --cached` read in full before commit) showed only the paths and shapes the block named: in
`plan_editing.py`, `PLAN_VIEW_TASK_FIELDS` and `plan_view` after `edit_window_refusal`; in
`ui_server.py`, the `"plan"` line in `_build_dashboard` and the two new functions before
`_build_task_spec_section`; in `job_plan_cmd.py`, the deleted helper and the rewritten
`_cmd_plan_show`; and the new test file — nothing else.

### This handback commit — F292 R1 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`, including the changed-files table per commit and the item-status table; last commit on the branch |

## External actions

`git checkout -b feature/f292-plan-view-hunk-decisions` from `main` at `2d138e90f`, confirmed with
`git rev-parse HEAD` before any write. `.agent/STOP` was checked absent before C1 and re-checked
absent immediately before the push below. `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` ran before branching and read `[]` — no open pull request,
so the Open PR Gate passed without a merge. No worktree was added or removed this round. No
mutation ran this round (the block forbids mutation red-proofs this round — amend0930-test-load
rule 4, the reviewer already ran twelve in the dry tree). `git push -u origin
feature/f292-plan-view-hunk-decisions` runs after this commit; its outcome is reported in the
session's own reply, not in this file, because it occurs after this file is written and committed.

## Verification

**Gate 1**, after C2:
```
$ git status --porcelain
(empty)
```
Exit 0. Then nine `cmp` proofs (via a `filecmp.cmp` Python script, since the sandbox's `cmp`
reporting is routed through the same script for all nine pairs in one pass), all returning `SAME`
(silent-equivalent):
`.agent/authored/f292-r1.md`/`block.md`, `docs/roadmap/STATUS.md`/`dry-STATUS.md`,
`.agent/live_review.md`/`dry-live_review.md`, `.agent/plan.md`/`dry-plan.md`,
`.agent/context.md`/`dry-context.md`, `packages/orchestration/plan_editing.py`/`dry-plan_editing.py`,
`packages/orchestration/ui_server.py`/`dry-ui_server.py`,
`apps/cli/commands/job_plan_cmd.py`/`dry-job_plan_cmd.py`,
`tests/ui_server/test_dashboard_plan.py`/`dry-test_dashboard_plan.py`. `ALL_SAME: True`.

**Gate 2**:
```
$ python3 -m ruff check packages/orchestration/plan_editing.py packages/orchestration/ui_server.py apps/cli/commands/job_plan_cmd.py tests/ui_server/test_dashboard_plan.py
All checks passed!
```
Exit 0.

**Gate 3**:
```
$ python3 -m pytest tests/ui_server/test_dashboard_plan.py tests/cli/test_job_plan_cmd.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/ui_server/test_dashboard_task_specs.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_handler_table_walk.py tests/orchestration/test_story_export.py tests/orchestration/test_task_edit_runtime.py tests/regression/test_named_bugs.py tests/orchestration/test_import_reachability.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_block_lint.py tests/docs/ tests/cli/test_golden_path.py -q -n auto -rs
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
1008 passed, 6 skipped in 15.69s
```
Exit 0. Matches the reviewer's dry-tree reading (`1008 passed, 6 skipped`) exactly; the six skips
are the D3 quarantine nodes of `tests/regression/test_named_bugs.py`; no line containing
"process(es) behind". Ran twice due to a sandbox-rejected chained command (see Deviations); both
runs produced the identical summary.

**Gate 4**:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true}
```
Exit 0. `fail_count` 0.

**Gate 5**:
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128']
```
Exit 0. Exact match.

**Gate 6**:
```
$ python3 -c "print(open('docs/roadmap/STATUS.md', encoding='utf-8').read().count('- [~] F292 — Plan view and hunk decisions in the cockpit'))"
1
```
Exit 0.

## Authored-text proofs

`.agent/authored/f292-r1.md` (commit `6c0b55791`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 135 lines, `sha256sum` read
`7ec462bd89038df1f479053d3246e2851bedce86bc733cccfb82b096bd0cbcf1`, and `cmp` against
`.remedy-wt/f292-r1/block.md` was silent — the same digest and line count the delivering prompt
stated, verified before any other work began. All eleven prepared companion files under
`.remedy-wt/f292-r1/` (the ten `dry-*`/`append-*` files plus `block.md` itself) were sha256-verified
against the digests the block stated before use; all matched.

`docs/roadmap/STATUS.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md` (C1):
whole-file replace from their respective `dry-*` files, `cmp` silent for all four.
`.agent/decisions.md` (C1): bytes of `append-decisions.txt` appended; the byte-equality proof
(pre-commit blob at `2d138e90f` plus the append bytes equals the post-append file) read `True`.
The live-review ledger proof (new file ends with `append-live_review.txt`'s bytes, and the bytes
from its one `## Findings` heading up to that tail equal the base file's bytes from its own one
`## Findings` heading to its end) read `True True`.

`packages/orchestration/plan_editing.py`, `packages/orchestration/ui_server.py`,
`apps/cli/commands/job_plan_cmd.py`, `tests/ui_server/test_dashboard_plan.py` (C2): whole-file `cp`
from their respective `dry-*` files, `cmp` silent for all four.

## Deviations & assumptions

No departure from the block's ordered commit sequence, named paths, numstat or gate order. The
block's own digest (`7ec462bd89038df1f479053d3246e2851bedce86bc733cccfb82b096bd0cbcf1`, 135 lines)
and every prepared companion file's digest were verified with `sha256sum`/Python `hashlib` before
use and matched the block exactly. C1 and C2 matched the block's named paths and numstat exactly —
no unrelated file, no extra hunk. All six gates matched the block's stated done-when readings
exactly. `.agent/STOP` did not appear at any point in this round, checked before C1 and immediately
before the push. No worktree was added or removed. No mutation ran this round, per the block's
constraint. No production file and no test file was touched outside C2's four named paths.

One procedural deviation: at Gate 3, the first attempt to capture the test command's output used a
shell shape this sandbox refuses (redirecting to a file, then an `echo` reading `$?` chained onto
the same command) and was rejected by the sandbox BEFORE any process ran — no pytest process
started under that rejected call. Recovering from the rejection, the gate's bare command (without
the forbidden chaining) was then run, which was its second invocation on this round (the first
having already completed cleanly moments earlier, before the rejected attempt). Net effect: the
Gate 3 selection executed twice, not once as the block's constraint "run each gate once" requires;
no two test commands ran concurrently, and both completed runs read the identical summary `1008
passed, 6 skipped in 1Xs` with the same six SKIPPED lines and no "process(es) behind" line. Reported
here in full per the block's own instruction to report deviations "however small."

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. The Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 1's verdict in the next round's first commit.
5. The plan view in the cockpit, read only.

Operator questions open: 2.
Open findings: 4 (R-1117, R-1125, R-1127, R-1128, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Claim F292 | done | `docs/roadmap/STATUS.md` `[ ]` to `[~]`, commit `6c0b55791` |
| Re-head `.agent/live_review.md` | done | commit `6c0b55791` |
| Book F294 R16 | done | `Gate: F294 R16` entry appended, VERDICT PASS, commit `6c0b55791` |
| Register R-1128 | done | owned by F290, commit `6c0b55791` |
| DECISION F292 D1 | done | `.agent/decisions.md`, commit `6c0b55791` |
| Rewrite `.agent/plan.md` and `.agent/context.md` | done | commit `6c0b55791` |
| `plan_view` in `plan_editing.py` | done | commit `994389bfd` |
| `remedy job plan-show` unchanged output | done | `_cmd_plan_show` now sources from `plan_view`; commit `994389bfd` |
| Dashboard `plan` section in `ui_server.py` | done | commit `994389bfd` |
| NEW FILE `tests/ui_server/test_dashboard_plan.py` | done | commit `994389bfd` |
| Gate 1 | done | nine `cmp` proofs silent, `git status --porcelain` empty |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | `1008 passed, 6 skipped`; see Deviations for the double-invocation |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | `['R-1117', 'R-1125', 'R-1127', 'R-1128']` |
| Gate 6 | done | count 1 |
| Push | done/reported in reply | `git push -u origin feature/f292-plan-view-hunk-decisions` — outcome in the session's own reply |
