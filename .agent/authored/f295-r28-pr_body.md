## What

F295 — Machine client contract v1. A program can now drive Remedy from an order to its proof
through the command line's JSON answers alone, with no cockpit, no HTTP transport and nobody at a
terminal. This is the first step of Luna gate A: Luna's runner writes an order file, starts
Remedy, polls one digest, answers the decisions a run raises, approves the apply and reads the
proof.

- **T001, order files.** `remedy do order.md` reads the order from a Markdown file when the
  argument is one path without whitespace ending in `.md`. An optional header names the project,
  the contract, the cost cap and constraints; a flag wins over the header. A missing, unreadable,
  empty or malformed file, and an order file with no cost cap, are refused with exit 2 before any
  step. The mission records the file's path and the sha256 of the bytes read (D2, D3).
- **T002, the digest.** Every `remedy status --json` answer carries a `client` object, version 1:
  every project's missions and jobs with their state, measured cost and its basis, evidence
  references and whether they wait for their apply; every open decision with its question,
  default, options and age; the cost of the day per project; and whether a supervisor answers
  (D4 to D7). Every value is read from the records.
- **T003, decisions without a terminal.** A run with `--yes --no-ui --json` on a pipe never reads
  stdin, and the builder's and reviewer's child processes read end of file (D8). A budget stop
  raises a decision answered `extend`, with the raised limits, or `abandon`, which cancels the job
  for good (D11, D12); a budget-stopped job refuses to resume until it is answered (D9) and then
  resumes with its own builder and reviewer (D13). `remedy patch hunks --json` reads hunk
  decisions (D14), and `remedy change proof` lists the job's applies (D15).
- **T004, the contract page and the gate test.** `docs/system/machine-client-contract-v1.md` names
  the order file and the commands, flags, JSON keys and exit codes of the whole path.
  `tests/cli/test_machine_client_contract.py` drives the path end to end with the fake providers
  and a stdin that fails the test on any read, and holds the page's tables equal to what it uses
  (D16, D17).
- **The hardening stage (SLOW MODE).** A fresh auditor checked 31 statements of the feature file;
  28 had a test that failed under a mutation at once, one cannot be tested because it describes
  something never built, and two were reported as gaps. One was real and is repaired by a test
  (R-1154); the other was refuted. The reviewer also found and repaired a follow-up question that
  stayed open after an `extend` (R-1155, D19). A repeat audit found no gap (D18).

## Why

Luna already watches Remedy's build loop through a status export and a mailbox. To use Remedy's
product the same way she needs an order she can write as a file, one digest she can read every
minute, decisions she can answer, and an apply that waits for the operator's approval. Before this
branch, `remedy do` took only text, no single read gave the state of every job and open decision,
and nothing proved that an unattended run never waits on stdin. The strategy is
`docs/roadmap/design/luna-control-plane-v1.md`.

## Key decisions (in `.agent/decisions.md`)

- D1: four slices in the feature file's order.
- D2, D3: the order file's format and its record on the mission.
- D4 to D7: the digest's shape and readers.
- D8 to D14: unattended runs, the budget decision and its answers, resume, hunk decisions.
- D15: `remedy change proof` lists job applies.
- D16, D17: the gate test and the contract page.
- D18, D19: the acceptance audit and its repairs.
- D20: the closure's one full suite was run again, because another program switched the checkout
  to `main` during the last 14 seconds of the first run.

## How to review / test

- Read `docs/roadmap/features/T12_F295.md`'s Built State first; it names every piece and its
  DECISION. Then the contract page `docs/system/machine-client-contract-v1.md`.
- `python3 -m pytest -q tests/cli/test_machine_client_contract.py tests/cli/test_do_order_file.py tests/orchestration/test_client_digest.py tests/orchestration/test_budget_decision.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f295-closure-suite.txt`: `21479 passed, 22
  skipped`, exit 0, HEAD unchanged during the run, 1165.39 CPU seconds.

## Changed files (outside `.agent/`, fork point `9a8431ea9` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 13 | 2 |
| `apps/cli/command_catalog.py` | 25 | 2 |
| `apps/cli/commands/decision.py` | 90 | 4 |
| `apps/cli/commands/do_cmd.py` | 49 | 1 |
| `apps/cli/commands/job.py` | 76 | 6 |
| `apps/cli/commands/patch.py` | 63 | 0 |
| `apps/cli/commands/status_cmd.py` | 2 | 0 |
| `docs/README.md` | 2 | 0 |
| `docs/agents/planner_reviewer_prompt.md` | 8 | 0 |
| `docs/guides/hunk-approval-user-guide-v1.md` | 11 | 1 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T12_F295.md` | 75 | 0 |
| `docs/system/machine-client-contract-v1.md` | 151 | 0 |
| `docs/system/proof-chain.md` | 11 | 0 |
| `packages/orchestration/budget_decision.py` | 209 | 0 |
| `packages/orchestration/budget_resolution.py` | 26 | 0 |
| `packages/orchestration/checkpoints.py` | 27 | 6 |
| `packages/orchestration/client_digest.py` | 241 | 0 |
| `packages/orchestration/decision_queue.py` | 66 | 3 |
| `packages/orchestration/do_sequence.py` | 15 | 1 |
| `packages/orchestration/exec_guard.py` | 3 | 0 |
| `packages/orchestration/job_apply.py` | 53 | 0 |
| `packages/orchestration/job_digest.py` | 14 | 5 |
| `packages/orchestration/mission_contract.py` | 48 | 0 |
| `packages/orchestration/order_file.py` | 189 | 0 |
| `packages/orchestration/pingpong_job.py` | 7 | 0 |
| `packages/orchestration/project_cockpit.py` | 31 | 20 |
| `packages/orchestration/proof_chain.py` | 28 | 0 |
| `packages/orchestration/stream_evidence.py` | 2 | 0 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_change_proof_cli.py` | 115 | 0 |
| `tests/cli/test_cost_preview_confirm.py` | 46 | 0 |
| `tests/cli/test_decision_cmd.py` | 181 | 1 |
| `tests/cli/test_do_flags.py` | 38 | 0 |
| `tests/cli/test_do_order_file.py` | 366 | 0 |
| `tests/cli/test_do_sequence_cli.py` | 112 | 0 |
| `tests/cli/test_exit_codes.py` | 7 | 0 |
| `tests/cli/test_job_refusal_envelope.py` | 1 | 0 |
| `tests/cli/test_machine_client_contract.py` | 283 | 0 |
| `tests/cli/test_patch_cmd.py` | 167 | 0 |
| `tests/cli/test_status_cmd.py` | 268 | 0 |
| `tests/orchestration/import_reachability_allowlist.txt` | 3 | 0 |
| `tests/orchestration/test_budget_decision.py` | 327 | 0 |
| `tests/orchestration/test_client_digest.py` | 481 | 0 |
| `tests/orchestration/test_do_sequence_order_digest.py` | 188 | 0 |
| `tests/orchestration/test_exec_guard.py` | 39 | 0 |
| `tests/orchestration/test_mission_contract.py` | 92 | 0 |
| `tests/orchestration/test_order_file.py` | 200 | 0 |
| `tests/orchestration/test_resume_cli.py` | 426 | 1 |
| `tests/orchestration/test_stream_evidence.py` | 39 | 0 |
| `tests/test_command_catalog.py` | 3 | 2 |

## Verdict and evidence

- Latest live review verdict: PASS (round 27); F295 accepted PASS_WITH_RISKS, the risks being the
  seven open Low findings below.
- Evidence job `f295r27e1001`, package `remedy-review-20261007-084539-READY_FOR_REVIEW.zip`,
  SHA-256 `f577772b647ff223cc2c4a22e4a13a4a1387880a5ed07939fa8704cf9defeea4`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `2ba602db4`.
- Resolved on this branch: R-1140 to R-1142, R-1144 to R-1148 and R-1150 to R-1155.
- Open findings: 7, all Low, all owned by F297, Findings paydown v7: R-1138 and R-1139 carried
  from F290; R-1143 and R-1149 raised here; R-1156 and R-1157 from the closure's self-use run (the
  toolchain refresh order's budget is too small for its five tasks, and it does not say where to
  read the newest Python version); and R-1158, the closure suite's 10 percent cost limit, which
  three runs of the same tests on one day showed to lie inside their normal spread.

## Runtime actuals

- Rounds: 28, in 7 sessions, on 2026-10-06 and 2026-10-07. F295 reached its soft limit of 25
  rounds and 7 sessions inside its closure sequence; nothing in scope was missing, so the closure
  is the self-consistent close and no split was proposed.
- Models: the workers' commit trailers name Claude Opus 5.5, Claude Sonnet 5 and Claude Sonnet
  5.5; the seventh session's reviewer ran on Claude Opus 5.5. The closure's self-use job SU-045
  ran on `claude-cli` / `claude-sonnet-4-6`: 12 provider calls, a measured $10.15, stopped at its
  $10.00 budget and applied nothing.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: two, both green; the first, in round 24, was not counted because another program
  switched the checkout during its last 14 seconds, and the second, in round 25, is the closure's
  run.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
