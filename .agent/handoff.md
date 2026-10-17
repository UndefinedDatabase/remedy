# Handoff — exec-1017c: cancellation ends the lifecycle (overnight reliability campaign 2026-10-17/18)

Session 1 of exec-1017c. Branch `feature/order-cancel` from PR 360's head `9b172a16c`; worktree
`.remedy-wt/order-cancel`. **Merge order: PR 360 first, then this PR.** Not merged, not deployed;
`.agent/STOP`, the supervisor and the live checkout (main, editable install) untouched. Outside the
roadmap queue: F078 stays next. Decisions exec-1017c D1–D10; findings R-1338–R-1344.

## Findings and status
| Item | Status | Reason |
|---|---|---|
| R-1338 no order cancel | done | D3: `remedy client cancel-order`, `POST /api/v1/orders/{order}/cancel` |
| R-1339 abandoned work actionable / hidden | done | D1, D2, D10: `remedy job abandon`, terminal `cancelled`; hiding rule deleted |
| R-1340 waiting story reads planning | done | D5: `queued` + `after_job`, `stopped`/`resume`, orphaned wait reason |
| R-1341 lane "one thing" / reaches past files | done | D6 |
| R-1342 named file left unchanged passes | done | D6: `named_files_unchanged`; matrix v4 row |
| R-1343 sandbox refusal reads as failed test | deviated | DoD path done (D7); loop `--test-command` path open |
| R-1344 Pi loads AGENTS.md into every turn | done | D9: `--no-context-files`, bounded agent file |
| P1-5 efficiency | deviated | measured and analysed (D9); no prompt/tool change without a real run |
| P1-6 verification by project type | done | probed: py/js/package found; go/rust/root-monorepo `not_run` with config hint (by design) |
| P1-8 progress + review reports | done | order `phase`/`cancel`; reports record cancel and later runs (D8) |
| P1-9 historical memory | skipped | nothing reaches the model (goal, file_tree, readme); no evidence which lesson helps |
| P1-10 test audit | done | `test_claude_cli_no_changes` order dependence fixed; 299 nodes run alone: only it was red |
| Real Pi/Ollama calibration | skipped | no authorized model budget |

## Calibration proposal (needs an authorized real run; fake providers cannot measure it)
Measured on the lab jobs: builder 85–92 % of tokens (15,544 / 40,764 / 33,090 input over 4 / 8 / 7
turns), about 5,000 input tokens per turn, Remedy's own prompts about 1,800 tokens, `cacheRead` 0.
The normalize builder made `read` ×3, `ls`, `bash` ×3 although its files were shown. Candidates,
each A/B on the three lab orders: (1) bounded tasks with all named files shown get tools
`edit,write,bash` only; (2) the builder is told the project tests run after it (the DoD runs them).
Expected effect only where measured; `--no-context-files` (D9) changes nothing for remedy-lab.

## Verification
- Owner and neighbour selections green during the work (cancel 19, guards ~1,300, neighbours 1,399).
- Full local gate: first run on `9376b9ce2` was red on 7 nodes (deleted id `job.cancel`, reachability
  allowlist, `_cmd_job_run` row, context.md headings, golden-path run now honestly blocked); all
  repaired in `ac3c18b88`. The final gate's command, tree and result are in the PR body.

## Next
Operator: review and merge PR 360, then this PR; restart `remedy serve` to load the code. Universe:
use `POST /api/v1/orders/{order}/cancel`, `phase`, story `queued`/`resume`, `POST .../abandon`.
