## What

F304 — Machine client contract v1.1, part two: what a client can rely on. F298 made the contract
data; this feature makes the paths a program actually walks through the command line work as the
contract says, and writes each one into `docs/system/machine-client-contract-v1.md` and the
interface `remedy client interface --json` prints.

- **T002, the project's own repository.** An order that names a project runs in that project's
  registered repository wherever the client stands; an order whose project has no repository
  (`project_has_no_repo`, exit 3) or whose `--repo` belongs to another project
  (`repo_not_in_project`, exit 2) is refused before any step. `remedy project register --repo
  <path>` registers a repository for a client and leaves its working copy clean.
- **T003, honest refusals and declining.** An approved apply that did not land answers
  `"ok": false` with one token per cause and exits non-zero; the preview keeps exit 0.
  `remedy job decline <job> --reason <text>` records the operator's decline, after which the job,
  like a job of an abandoned mission, waits for nothing.
- **T004, several jobs and the same order twice.** One order file runs in one mission at a time
  (`order_already_running`, exit 2, naming the mission) unless `--new-mission`. `remedy job run`
  answers `"ok": false` and exit 1 for a run that ended blocked, failed or stopped by its budget
  (R-1184). The second gate test, `tests/cli/test_machine_client_paths.py`, drives an apply merged
  with its history and pushed to a local bare upstream, an order of two jobs, an order started
  twice, an order naming its project and a declined result, through the command line alone.
- **T005, the approval card.** Each completed job in the digest carries its changed files, its
  tasks, its mission's blocking criteria, whether a check ran, and a recommendation word and a
  risk word derived from recorded facts by rules the page states; no word comes from a model.
- **T006, tokens and calls.** Each job carries its provider calls and its tokens by kind beside
  its cost, and each project's day its tokens; an order may be capped by any one job budget, and
  the page says what the call and token budgets count.
- **T007, a small digest.** The digest lists every job that still needs something and the 20 ended
  jobs that ended last, names the window and how many it left out, and `remedy status
  --all-ended-jobs` widens it; with 1,000 settled jobs it stays under 65,536 bytes. A small change
  to an existing repository needs no contract template of its own.

## Why

The universe workspace's client, Luna, could not complete one real order against F295's page: the
page promised too little, and three things Remedy did were wrong for a program. F253's HTTP API
calls the same functions, so the command line is where they are repaired.

## Key decisions (in `.agent/decisions.md`)

- D1: F298's slice order and claim measurement carried.
- D2, D3: an order runs in its project's registered repository; registering one for a client.
- D4, D5: one refusal token per cause of an apply that did not land; declining a result.
- D6 to D8: one mission per order file; the second gate test; `remedy job run` refuses a run that
  did not finish (R-1184).
- D9: the operator confirmed F298's early split.
- D10 to D12: the approval card, its blocking criteria and its two words.
- D13 to D15: calls and tokens by kind; any one job budget caps an order; what the budgets count.
- D16, D17: the digest's window; no template for a small change.

## How to review / test

- Read `docs/roadmap/features/T12_F304.md`'s Built State first, then the sections of
  `docs/system/machine-client-contract-v1.md` it names.
- `python3 -m pytest -q tests/cli/test_machine_client_paths.py tests/cli/test_machine_client_contract.py tests/cli/test_client_interface.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f304-closure-suite.txt`: `21810 passed, 22
  skipped`, exit 0, 1126.33 CPU seconds, 3.9 percent more than F298's closure.

## Changed files (outside `.agent/`, fork point `4eda924c5` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 15 | 2 |
| `apps/cli/client_interface.py` | 69 | 15 |
| `apps/cli/command_catalog.py` | 46 | 1 |
| `apps/cli/commands/do_cmd.py` | 197 | 18 |
| `apps/cli/commands/project.py` | 39 | 0 |
| `apps/cli/commands/status_cmd.py` | 8 | 2 |
| `apps/ui/src/api/ownership.ts` | 1 | 0 |
| `docs/agents/planner_reviewer_prompt.md` | 28 | 0 |
| `docs/guides/exit-codes.md` | 4 | 0 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T12_F304.md` | 36 | 0 |
| `docs/system/machine-client-contract-v1.md` | 147 | 26 |
| `packages/orchestration/client_digest.py` | 247 | 23 |
| `packages/orchestration/job_apply.py` | 130 | 6 |
| `packages/orchestration/mission_state.py` | 23 | 0 |
| `packages/orchestration/order_file.py` | 25 | 19 |
| `packages/orchestration/ownership.py` | 24 | 1 |
| `packages/orchestration/ownership_phrases.py` | 3 | 0 |
| `packages/orchestration/token_ledger.py` | 20 | 0 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_client_interface.py` | 27 | 4 |
| `tests/cli/test_do_flags.py` | 3 | 2 |
| `tests/cli/test_do_order_file.py` | 252 | 1 |
| `tests/cli/test_do_project_repo.py` | 174 | 0 |
| `tests/cli/test_do_sequence_cli.py` | 5 | 4 |
| `tests/cli/test_job_apply_refusals.py` | 232 | 0 |
| `tests/cli/test_job_decline.py` | 121 | 0 |
| `tests/cli/test_job_run_end_states.py` | 100 | 0 |
| `tests/cli/test_machine_client_paths.py` | 183 | 0 |
| `tests/cli/test_project_register.py` | 102 | 0 |
| `tests/cli/test_status_cmd.py` | 145 | 0 |
| `tests/orchestration/fixtures/ownership/golden/sentences.txt` | 1 | 0 |
| `tests/orchestration/test_client_digest.py` | 490 | 4 |
| `tests/orchestration/test_f018_authority_integration.py` | 13 | 8 |
| `tests/orchestration/test_job_apply.py` | 9 | 5 |
| `tests/orchestration/test_job_apply_commit.py` | 9 | 4 |
| `tests/orchestration/test_job_apply_history.py` | 3 | 2 |
| `tests/orchestration/test_job_task_runner.py` | 50 | 47 |
| `tests/orchestration/test_job_worktree_handoff.py` | 7 | 3 |
| `tests/orchestration/test_mission_state.py` | 29 | 0 |
| `tests/orchestration/test_order_file.py` | 23 | 0 |
| `tests/orchestration/test_ownership_ledger.py` | 25 | 0 |
| `tests/orchestration/test_ownership_phrases.py` | 10 | 6 |
| `tests/orchestration/test_token_ledger.py` | 27 | 0 |
| `tests/ui_server/test_task_edit_e2e_live.py` | 3 | 1 |
| `tests/ui_server/test_task_veto_e2e_live.py` | 6 | 2 |

## Verdict and evidence

- Latest live review verdict: PASS (round 23); F304 accepted PASS_WITH_RISKS, the risks being the
  open findings below.
- The hardening stage (SLOW MODE): a fresh auditor split the Goal & Done sentence and the
  Acceptance lines into forty claims; thirty-eight had a test that a mutation turned red at once,
  and the one gap, covering two claims of the second gate test (R-1185), was repaired and audited
  again with no gap left.
- Evidence job `f304r23e1001`, package `remedy-review-20261008-124310-READY_FOR_REVIEW.zip`,
  SHA-256 `d30f2486853690405637598957c25cabac8bd65f0455c66385bb014df5207945`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `95f3421e7`.
- Resolved on this branch: R-1183 to R-1186.
- Open findings: 11, all owned by F297, Findings paydown v7, all carried from earlier features:
  R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and
  R-1176 (Low).

## Runtime actuals

- Rounds: 24, in 5 sessions, on 2026-10-08. Every round passed review.
- Models: the workers' commit trailers name Claude Sonnet 5.5 and Claude Sonnet 5; the fifth
  session's reviewer ran on Claude Opus 5.5. The closure's self-use job SU-049 ran on `claude-cli` / `claude-sonnet-4-6`: 4
  provider calls, 11,763 tokens, a measured $1.63 against a $6.00 budget, completed with the
  reviewer's verdict pass after one repair round, never applied.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: two, in rounds 20 and 21; the first found R-1186, the second was green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
