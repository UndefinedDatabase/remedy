## What and why

F269 gives a mission one **contract**: its acceptance criteria, each compiled to a check by F061's DoD compiler. A mission is not done while a blocking criterion is red. Four templates are the contract's floor. Amendments and a remainder proposal complete it (`docs/roadmap/features/T2_F269.md`, DECISION amend0905-vocab D9).

- **Record and views.** `packages/orchestration/mission_contract.py` owns a validated `contract_v1` body on the mission. `remedy mission contract <id>` and `remedy job contract <id>` render it; the job view is the job's slice (D2, D3).
- **Compiler and gate.** Criteria are compiled by `dod_compiler.compile_dod`. Each job's DoD carries its slice, and its gate result sets the criteria. The loop's achieve move is refused while a blocking criterion is not met. `run_job` now runs F061's gate before the worktree goes (D4, D6).
- **Templates.** `docs/contracts/{website,api-service,cli-tool,python-library}.md` are proposed from the order or forced with `remedy do --contract <name>`. Planner criteria are added, never replacing a template criterion (D1).
- **Hygiene.** The three blocking hygiene criteria are checked by `python3 -m packages.orchestration.contract_hygiene`. A build round rejects an unreferenced or replaced added file, naming the path (D5).
- **Repository binding.** The contract binds a job to its repository and grants it. `remedy job attach-repo` and `remedy job permit` are deleted (D7).
- **Amendments.** An amendment applies from the next round and is acknowledged in the mission's ledger (D8).
- **Remainder.** At budget end with blockers open, a one-word `yes` starts a follow-up mission that carries them as one amendment (D9, D10).

## How to review

Read `docs/roadmap/features/T2_F269.md` (Built State), then DECISIONs F269 D1 to D10 in `.agent/decisions.md`, then `packages/orchestration/mission_contract.py` and its tests. Every round's block, verdict and gate output are in `.agent/authored/f269-r*` and `.agent/live_review.md`.

## Verdict and state

- Live review: **PASS_WITH_RISKS**. The risks are named in the round 11 gate entry:
  - finding R-0972 is open (Low, owner F273): the self-use defect describer is blind to a budget stop;
  - three Acceptance bullets hold in a DECISION's reading (D9 (2), D5 (6), D8 (2));
  - operator questions Q4 and Q5 stand as executed recommendations.
- Integration gate: the full suite ran once and read `1 failed, 17950 passed, 23 skipped`. The one node, an untimed `subprocess.run` F269 added, was repaired in round 11 and proved red-to-green.
- Evidence job `f269r11e1001`. Package `remedy-review-20260918-190009-READY_FOR_REVIEW.zip`, SHA-256 `bf0a454507933ee7848b83825eb599b07fb4eed0d44de84270d03acd91149172`, accepted HEAD `2a7f22c443350195a08b366abd17a5c3b3a4d1f3`.
- Self-use item SU-020 consumed. Its run stopped at its provider-call budget (R-0972).
- Findings: R-0971 raised and resolved inside the feature; R-0972 open, owner F273. Operator questions open: 5.

## Changed files (main code)

| Area | Files |
|---|---|
| Contract | `packages/orchestration/mission_contract.py`, `contract_templates.py`, `contract_hygiene.py` (new) |
| Wiring | `orchestrator_loop.py`, `pingpong_job.py`, `pingpong_loop.py`, `do_sequence.py`, `mission_compiler.py`, `mission_state.py`, `mission_dossier.py`, `ui_server.py` |
| CLI | `apps/cli/commands/contract_cmd.py` (new), catalog and `do`, `mission achieve`, `decision` doors; `job attach-repo` and `job permit` deleted |
| Templates | `docs/contracts/*.md` |
| Tests | `tests/orchestration/test_mission_contract.py`, `test_mission_gate.py`, `test_contract_templates.py`, `test_contract_hygiene.py`, `test_pingpong_job_dod_gate.py`, `tests/cli/test_contract_cmd.py`, and others |

## Runtime actuals

12 rounds over 2 sessions, planner/reviewer and workers on Claude Opus 5. Wall clock, tokens and cost: not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
