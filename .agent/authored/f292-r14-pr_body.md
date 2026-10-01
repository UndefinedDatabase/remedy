## What and why

F292 lets the cockpit do seven things that Remedy's write door already accepted but no screen
offered. The first six are the edits of a plan that waits for approval: edit a task, delete it, move
it, merge tasks, split a task, and change, remove or add its checks. The seventh is deciding a
change piece by piece, approving each changed piece of code or rejecting it with a reason. Before
this feature these seven stood in the command palette as disabled entries, because each needed a
form the cockpit did not have.

- **The plan view.** The right panel's Plan button opens the stored plan of the job: its version,
  whether it is approved, and every planned task with the tasks it waits for and the checks it must
  pass. One builder serves this answer to both `remedy job plan-show --json` and the dashboard, so
  the two always agree (DECISION F292 D1, D2).
- **The six plan edits.** While the plan is open for editing, every edit is sent against the version
  the view shows. An accepted edit names the new version and the cockpit reads the plan again at
  once; an edit against a plan that changed in the meantime, and every other refusal with a reason,
  is told in plain words; and the forms refuse beforehand what the planner would refuse (D3, D4, D5).
- **Hunk decisions.** The decision already recorded for a change is served at
  `/api/jobs/<id>/hunk-decisions` and per task run (D6). Below the change view, one row per changed
  piece offers Approve, Reject with a reason, and Undecided, starts from that record, and records the
  whole decision exactly as `remedy patch approve-hunks` does (D7).
- **The palette.** Its seven form entries now open these views, and no entry stands disabled for
  being a form (D8). `tests/ui_server/test_plan_view_live.py` drives both views through the real UI
  server and write door in headless Chrome and reads the stored results back from disk.

## Key decisions

- D1 to D8 build the feature; D9 records the hardening stage (SLOW MODE): a fresh auditor tried to
  break each of the nine statements of the feature file and every one had a test that turned red,
  three of them through the command line or a real browser. No gap was found.
- D10: the closure's self-use item, `SU-042`, ran to its approval gate, but Remedy's builder changed
  no file and its reviewer still passed the task. That is the defect finding R-1117 already records,
  so it was booked as R-1117's recurrence with new evidence, nothing of the item was landed, and the
  item is consumed by F292.
- D11: the README's Tier 5 row now reads 38 of 38. Its total had been one short since F292 was
  registered (finding R-1125, which stays open for the test it asks for).

## How to review

1. `docs/roadmap/features/T5_F292.md`, its Built State section first.
2. The server side: `packages/orchestration/plan_editing.py` (`plan_view`),
   `packages/orchestration/hunk_decision_record.py` and the two routes in
   `packages/orchestration/ui_server.py`.
3. The cockpit: `apps/ui/src/components/plan/`, `apps/ui/src/api/planEditSend.ts`,
   `apps/ui/src/components/diff/HunkDecisionPanel.tsx`, and the palette's
   `apps/ui/src/api/paletteCommands.ts`.
4. The end-to-end test `tests/ui_server/test_plan_view_live.py`.
5. The review record: `.agent/live_review.md` (one `Gate: F292 R<n>` entry per round),
   `.agent/f292_acceptance_audit.md`, and `.agent/authored/f292-closure-suite.txt`.

## Changed files outside `.agent/` (fork point `2d138e90f` to the accepted head)

| Path | +/- |
|---|---|
| `apps/cli/commands/job_plan_cmd.py` | +12/-31 |
| `apps/ui/src/RemedyApp.tsx` | +8/-2 |
| `apps/ui/src/api/hunkDecisionSend.test.ts` | +91/-0 |
| `apps/ui/src/api/hunkDecisionSend.ts` | +116/-0 |
| `apps/ui/src/api/hunkDecisionView.test.ts` | +100/-0 |
| `apps/ui/src/api/hunkDecisionView.ts` | +88/-0 |
| `apps/ui/src/api/hunkDecisions.test.ts` | +43/-0 |
| `apps/ui/src/api/hunkDecisions.ts` | +59/-0 |
| `apps/ui/src/api/paletteCommandState.test.ts` | +14/-7 |
| `apps/ui/src/api/paletteCommandState.ts` | +13/-9 |
| `apps/ui/src/api/paletteCommands.test.ts` | +16/-12 |
| `apps/ui/src/api/paletteCommands.ts` | +17/-17 |
| `apps/ui/src/api/planEditSend.test.ts` | +173/-0 |
| `apps/ui/src/api/planEditSend.ts` | +190/-0 |
| `apps/ui/src/api/planEditView.test.ts` | +192/-0 |
| `apps/ui/src/api/planEditView.ts` | +175/-0 |
| `apps/ui/src/api/planView.test.ts` | +101/-0 |
| `apps/ui/src/api/planView.ts` | +60/-0 |
| `apps/ui/src/api/remedyApi.test.ts` | +99/-1 |
| `apps/ui/src/api/remedyApi.ts` | +59/-1 |
| `apps/ui/src/api/types.ts` | +35/-1 |
| `apps/ui/src/components/diff/HunkDecisionPanel.module.css` | +75/-0 |
| `apps/ui/src/components/diff/HunkDecisionPanel.tsx` | +135/-0 |
| `apps/ui/src/components/diff/hunkDecisionPanelMarkup.test.ts` | +44/-0 |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +4/-1 |
| `apps/ui/src/components/plan/PlanCriteria.tsx` | +99/-0 |
| `apps/ui/src/components/plan/PlanMergeForm.tsx` | +59/-0 |
| `apps/ui/src/components/plan/PlanSplitForm.tsx` | +59/-0 |
| `apps/ui/src/components/plan/PlanTaskEditForm.tsx` | +69/-0 |
| `apps/ui/src/components/plan/PlanView.module.css` | +173/-0 |
| `apps/ui/src/components/plan/PlanView.tsx` | +199/-0 |
| `apps/ui/src/components/plan/planViewMarkup.test.ts` | +215/-0 |
| `apps/ui/src/components/shell/RemedyShell.tsx` | +31/-5 |
| `docs/agents/planner_reviewer_prompt.md` | +6/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T5_F292.md` | +47/-1 |
| `packages/orchestration/hunk_decision_record.py` | +29/-0 |
| `packages/orchestration/plan_editing.py` | +36/-0 |
| `packages/orchestration/ui_server.py` | +66/-0 |
| `scripts/self_use_queue.json` | +8/-0 |
| `tests/ui_contracts/test_hunk_decision_contract.py` | +115/-0 |
| `tests/ui_contracts/test_plan_view_contract.py` | +155/-0 |
| `tests/ui_server/test_command_channel.py` | +1/-0 |
| `tests/ui_server/test_dashboard_plan.py` | +178/-0 |
| `tests/ui_server/test_hunk_decisions_route.py` | +160/-0 |
| `tests/ui_server/test_plan_view_live.py` | +268/-0 |

After the accepted head, the closing commit flips F292's STATUS line, syncs `README.md` and sets
`SU-042`'s `consumed_by`; everything else after it is under `.agent/`.

## Verdict and evidence

- Latest live review verdict: PASS (round 13, the evidence round; the closing round's own verdict is
  booked in the next feature's first commit).
- The one full suite, on the tree that ships: `21186 passed, 22 skipped`, exit 0, no bad node and no
  leftover process, 863.01 CPU seconds, 0.3 percent less than F294's
  (`.agent/authored/f292-closure-suite.txt`).
- Evidence job `f292r13e1001`: 903 tests passed. Package
  `remedy-review-20261001-095015-READY_FOR_REVIEW.zip`, SHA-256
  `f178c7e8e63d3652480d7aa77bfe824c91bd0533d4d2fdb7549526c6fe7b8a9b`, archived in
  `/home/decodeux/Repos/remedy-history/zips`, accepted head
  `7b322964482026296eb5e9bf721517b9a8540d14`.
- Open findings: 5, none owned by F292: R-1117 (Medium), R-1125, R-1127, R-1128 and R-1129 (Low),
  all owned by F290, the next findings paydown.

## Runtime actuals

- 14 delegated rounds in 2 sessions, all on 2026-10-01, from 06:28 to about 10:00 local time.
- Planner and reviewer: Claude Opus 5.5; workers: one subagent per round. Tokens and cost of the
  sessions themselves: not measured.
- The self-use run: 4 provider calls, $0.79, 107 seconds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
