# Handoff — F292 Plan view and hunk decisions in the cockpit, round 6

## Session

SESSION 1 of feature F292 · round 6

Context self-assessment: the reviewer's context is comfortable; the session continues.

## Range

Review of `8e77c28e9`..`HEAD` — five commits on `feature/f292-plan-view-hunk-decisions`:
`dcbe625cf`, `ec62f0219`, `5369bb38d`, `f94d5c2ae`, `2dad1fdc5`, and this handback commit.

## Commits

### `dcbe625cf` F292 R6 C1: book round 5, record DECISION F292 D6, save the round 6 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f292-r6.md` | +146/-0 | NEW FILE at `.agent/authored/f292-r6.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f292-r6/block.md` before commit (`wc -l` 146, sha256 `fc3e5fef086bd29cb88cfb6bace560ac5e4668f27c913b36deba05ff32d3c443`) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f292-r6/append-decisions.txt` appended without retyping; pre-commit blob (`git show 8e77c28e9:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) — DECISION F292 D6 |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f292-r6/append-live_review.txt` appended without retyping; pre-commit blob plus the append bytes verified byte-equal to the new file (`True`) — books round 5's `Gate: F292 R5` entry (VERDICT PASS) |
| `.agent/plan.md` | +9/-8 | whole-file replaced from `.remedy-wt/f292-r6/dry/.agent/plan.md`; byte comparison equal |

`git diff --cached --numstat` before the commit read `146 0` (authored block), `10 0`
(decisions.md), `2 0` (live_review.md), `9 8` (plan.md) — matching the block's stated numstat
exactly. `git show --numstat` after the commit read the same four lines.

### `ec62f0219` F292 R6 C2: the read of the hunk decision recorded for the attempt a diff shows (DECISION F292 D6)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/hunk_decision_record.py` | +29/-0 | whole-file copy from `.remedy-wt/f292-r6/dry/`; byte comparison equal — `recorded_hunk_decision` appended after `load_latest_hunk_ledger_from_metadata`, plus its Public API line |
| `packages/orchestration/ui_server.py` | +41/-0 | whole-file copy; byte comparison equal — `_hunk_decisions_for_view`, `_build_hunk_decisions_json`, `_build_task_run_hunk_decisions_json` after `_build_task_run_diff_json`, the `"hunk-decisions"` dispatch entry, and the task-run structural route after the task-run diff route |

`git diff --cached --numstat` before the commit read `29 0`, `41 0` — matching the block's stated
numstat exactly. `git show --numstat` after the commit read the same two lines. Self-review
(`git diff --cached` read in full before commit) showed only the Public API line and
`recorded_hunk_decision` appended in the first file, and in the second exactly the three new
functions, the `"hunk-decisions"` handler, and the structural route after the task-run diff
route — nothing else, matching the block's self-review instruction exactly; the base had not
moved.

### `5369bb38d` F292 R6 C3: tests for the recorded-decision routes and their walk

| Path | +/- | Reason |
|---|---|---|
| `tests/ui_server/test_hunk_decisions_route.py` | +160/-0 | NEW FILE; byte copy from `.remedy-wt/f292-r6/dry/`; byte comparison equal |
| `tests/ui_server/test_command_channel.py` | +1/-0 | whole-file copy; byte comparison equal — the walk gains `/api/jobs/<id>/task-runs/T001/hunk-decisions` after the task-run diff path |

`git diff --cached --numstat` before the commit read `160 0`, `1 0` — matching the block's stated
numstat exactly. `git show --numstat` after the commit read the same two lines.

### `f94d5c2ae` F292 R6 C4: the hunk controls' decoder, loader, rules and send (DECISION F292 D6)

| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/hunkDecisions.ts` | +59/-0 | NEW FILE; byte copy from `.remedy-wt/f292-r6/dry/`; byte comparison equal — `readHunkDecisions`, `hunkDecisionsPath` |
| `apps/ui/src/api/hunkDecisionView.ts` | +88/-0 | NEW FILE; byte copy; byte comparison equal — the hunk controls' rules |
| `apps/ui/src/api/hunkDecisionSend.ts` | +116/-0 | NEW FILE; byte copy; byte comparison equal — the send and its wording |
| `apps/ui/src/api/remedyApi.ts` | +17/-0 | whole-file copy; byte comparison equal — `loadHunkDecisions`, importing `hunkDecisionsPath`/`readHunkDecisions`/`HunkDecisions` |

`git diff --cached --numstat` before the commit read `59 0`, `88 0`, `116 0`, `17 0` — matching the
block's stated numstat exactly (280 insertions total, under the 500-line cap). `git show
--numstat` after the commit read the same four lines.

### `2dad1fdc5` F292 R6 C5: tests for the hunk controls' modules and their contract

| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/hunkDecisions.test.ts` | +43/-0 | NEW FILE; byte copy; byte comparison equal |
| `apps/ui/src/api/hunkDecisionView.test.ts` | +100/-0 | NEW FILE; byte copy; byte comparison equal |
| `apps/ui/src/api/hunkDecisionSend.test.ts` | +91/-0 | NEW FILE; byte copy; byte comparison equal |
| `apps/ui/src/api/remedyApi.test.ts` | +20/-1 | whole-file copy; byte comparison equal — imports and uses `loadHunkDecisions` |
| `tests/ui_contracts/test_hunk_decision_contract.py` | +91/-0 | NEW FILE; byte copy; byte comparison equal |

`git diff --cached --numstat` before the commit read `43 0`, `100 0`, `91 0`, `20 1`, `91 0` —
matching the block's stated numstat exactly. `git show --numstat` after the commit read the same
five lines.

### This handback commit — F292 R6 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`, including the changed-files table per commit and the item-status table; last commit on the branch |

## External actions

`.agent/STOP` was checked absent before C1 (`ls` exit 2, not found) and re-checked absent
immediately before the push below. No `gh` command ran this round — the Open PR Gate is deferred
to the next round per this round's own `## Next`. No worktree was added or removed this round;
`git worktree list` was counted by a Python script (`len(result.stdout.splitlines())`), never by
eye, and reads **twelve** entries: the primary checkout, the pre-existing `.remedy-wt/f292-r1-dry`
worktree, and ten pre-existing `job-*` scratch worktrees — unchanged from round 5's script-counted
reading. No mutation and no render-harness execution ran this round, per the block's constraint
(amend0930-test-load rule 4; no render this round either, per the block's own Goal line). `git
push origin feature/f292-plan-view-hunk-decisions` runs after this commit; its outcome is reported
in the session's own reply, not in this file, because it occurs after this file is written and
committed.

## Verification

**Gate 1**, after C5:
```
$ git status --porcelain
(empty, exit 0)
```
Then a Python byte comparison of all sixteen table paths plus `.agent/authored/f292-r6.md`
against its prepared file — seventeen pairs, all `True`, `ALL_OK True`.

**Gate 2** (THE UI BUILD, before the selection):
```
$ python3 subprocess.run(["/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vite", "build"], cwd="/home/decodeux/Repos/remedy/apps/ui")
vite v6.4.2 building for production...
transforming...
✓ 2156 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                                  0.41 kB │ gzip:   0.28 kB
dist/assets/index-B-LhDP-c.css                  89.73 kB │ gzip:  15.32 kB
dist/assets/diffHighlightGrammars-o9XqnLhb.js    1.70 kB │ gzip:   0.79 kB
dist/assets/index-DDnsX-ZA.js                  802.22 kB │ gzip: 258.06 kB
✓ built in 2.37s
```
Exit 0. `git status --porcelain` re-checked immediately after: still empty (`apps/ui/dist` is
ignored).

**Gate 3**:
```
$ python3 -m ruff check packages/orchestration/hunk_decision_record.py packages/orchestration/ui_server.py tests/ui_server/test_hunk_decisions_route.py tests/ui_server/test_command_channel.py tests/ui_contracts/test_hunk_decision_contract.py
All checks passed!
```
Exit 0.

**Gate 4**:
```
$ python3 -m pytest tests/ui_contracts/ tests/ui_server/test_hunk_decisions_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_handler_table_walk.py tests/orchestration/test_hunk_decision_record.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/ui_server/test_dashboard_plan.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_live_state.py tests/regression/test_named_bugs.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_block_lint.py tests/docs/ tests/cli/test_golden_path.py -q -n auto -rs
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
2092 passed, 10 skipped in 18.60s
```
Exit 0. Matches the reviewer's dry-tree reading (`2092 passed, 10 skipped`) exactly; all ten skips
are D3 quarantine nodes; no line containing "process(es) behind"; ran exactly once, after the UI
build in gate 2 so no `React UI not built` failure was met. The selection included `tsc --noEmit`,
the whole vitest suite, eslint over `apps/ui/src`, and the canary `tests/cli/test_golden_path.py`.

**Gate 5**:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...all "pass"...], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0. `fail_count` 0.

**Gate 6**:
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129']
```
Exit 0. Exact match.

## Authored-text proofs

`.agent/authored/f292-r6.md` (commit `dcbe625cf`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 146 lines, `sha256sum` read
`fc3e5fef086bd29cb88cfb6bace560ac5e4668f27c913b36deba05ff32d3c443`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest. All prepared companion files under
`.remedy-wt/f292-r6/` (the sixteen `dry/` files, the two `append-*.txt` files, plus `block.md`
itself) were sha256-verified against the digests the block's table stated before any use; all
matched.

`.agent/decisions.md` (C1): bytes of `append-decisions.txt` appended; the byte-equality proof
(pre-commit blob at `8e77c28e9` plus the append bytes equals the post-append file, compared against
the prepared `dry/.agent/decisions.md`) read `True`.
`.agent/live_review.md` (C1): bytes of `append-live_review.txt` appended; the same proof read
`True`.
`.agent/plan.md` (C1): whole-file replace from `dry/.agent/plan.md`; byte comparison equal.

`packages/orchestration/hunk_decision_record.py`, `packages/orchestration/ui_server.py` (C2):
whole-file byte copy from their respective `dry/` files, byte comparison equal for both.

`tests/ui_server/test_hunk_decisions_route.py`, `tests/ui_server/test_command_channel.py` (C3):
whole-file byte copy from their respective `dry/` files, byte comparison equal for both.

`apps/ui/src/api/hunkDecisions.ts`, `hunkDecisionView.ts`, `hunkDecisionSend.ts`, `remedyApi.ts`
(C4): whole-file byte copy from their respective `dry/` files, byte comparison equal for all four.

`apps/ui/src/api/hunkDecisions.test.ts`, `hunkDecisionView.test.ts`, `hunkDecisionSend.test.ts`,
`remedyApi.test.ts`, `tests/ui_contracts/test_hunk_decision_contract.py` (C5): whole-file byte copy
from their respective `dry/` files, byte comparison equal for all five.

## Deviations & assumptions

None. No departure from the block's ordered commit sequence, named paths, numstat or gate order.
The block's own digest (`fc3e5fef086bd29cb88cfb6bace560ac5e4668f27c913b36deba05ff32d3c443`, 146
lines) and every prepared companion file's digest were verified with Python `hashlib` before use
and matched the block exactly. C1 through C5 matched the block's named paths and numstat exactly —
no unrelated file, no extra hunk. All six gates matched the block's stated done-when readings
exactly, each run once, in order, gate 2 (the UI build) before gate 4 (the selection) as ordered.
`.agent/STOP` did not appear at any point in this round, checked before C1 and immediately before
the push. No worktree was added or removed; the `git worktree list` count was read by script
(twelve), not by eye, agreeing with round 5's script-counted reading. No mutation and no render
harness ran this round, per the block's constraints — this round lands no screen. No production
file and no test file was touched outside C2's two, C3's two, C4's four and C5's five named paths.
No `gh` command ran, since the Open PR Gate is this round's own next-round action, not this
round's.

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. The Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 6's verdict in the next round's first commit.
5. The hunk controls panel beside the diff view.

Operator questions open: 2.
Open findings: 5 (R-1117, R-1125, R-1127, R-1128, R-1129, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 5's verdict (PASS) in `.agent/live_review.md` | done | commit `dcbe625cf` |
| Record DECISION F292 D6 in `.agent/decisions.md` | done | commit `dcbe625cf` |
| Advance `.agent/plan.md` | done | commit `dcbe625cf` |
| `recorded_hunk_decision` in `packages/orchestration/hunk_decision_record.py` | done | commit `ec62f0219` |
| `/api/jobs/<id>/hunk-decisions` and `/api/jobs/<id>/task-runs/<tid>/hunk-decisions` routes in `ui_server.py` | done | commit `ec62f0219` |
| NEW FILE `tests/ui_server/test_hunk_decisions_route.py` | done | commit `5369bb38d` |
| Walk's new path in `tests/ui_server/test_command_channel.py` | done | commit `5369bb38d` |
| NEW FILE `apps/ui/src/api/hunkDecisions.ts` | done | commit `f94d5c2ae` |
| NEW FILE `apps/ui/src/api/hunkDecisionView.ts` | done | commit `f94d5c2ae` |
| NEW FILE `apps/ui/src/api/hunkDecisionSend.ts` | done | commit `f94d5c2ae` |
| `loadHunkDecisions` in `apps/ui/src/api/remedyApi.ts` | done | commit `f94d5c2ae` |
| Tests for the four client modules | done | commit `2dad1fdc5` |
| NEW FILE `tests/ui_contracts/test_hunk_decision_contract.py` | done | commit `2dad1fdc5` |
| Gate 1 | done | `git status --porcelain` empty, 17/17 byte comparisons equal |
| Gate 2 (UI build) | done | `✓ built in 2.37s`, exit 0, `git status --porcelain` still empty |
| Gate 3 (ruff) | done | `All checks passed!` |
| Gate 4 (selection) | done | `2092 passed, 10 skipped` |
| Gate 5 (integrity) | done | `fail_count` 0 |
| Gate 6 (open finding ids) | done | `['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129']` |
| Push | done/reported in reply | `git push origin feature/f292-plan-view-hunk-decisions` — outcome in the session's own reply |
