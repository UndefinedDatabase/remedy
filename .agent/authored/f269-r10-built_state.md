
## Built State (F269, 2026-09-18)

What exists on disk at the close of F269; every DECISION named lives in `.agent/decisions.md`.

**T001 — record and renderers.** `packages/orchestration/mission_contract.py` owns the mission's
contract: one `contract_v1` body with `template`, `criteria[]` (`id`, `text`, `blocking`,
`origin` in `template`, `planner`, `amendment`, `milestones`, `check`, `status`, `evidence_ref`)
and `amendments[]`, validated on read and on write and refused with the rule named (DECISION F269
D2). The orchestrator's dispatch records the milestone a job serves, a job's slice is the
whole-mission criteria plus its milestone's, and `remedy mission contract <id>` and `remedy job
contract <id>` render both views read-only with `--json` from `apps/cli/commands/contract_cmd.py`
(DECISION F269 D3; `tests/cli/test_contract_cmd.py`).

**T002 — compiler and mission gate.** Each criterion's check is compiled by F061's
`dod_compiler.compile_dod`; `plan_mission` writes one planner criterion per milestone and keeps
every criterion of another origin; each dispatched job's stored DoD carries its slice, its gate
result sets the slice criteria `met` or `unmet`, and `evaluate_move` refuses
`declare_mission_achieved` while a blocking criterion is not met (DECISION F269 D4). Whole-mission
checks enter a job's DoD non-blocking, and `run_job` runs `dod_gate.run_job_gate` before the job's
worktree goes, so a `remedy do` job is gated too (DECISION F269 D6). `remedy mission achieve`
stays the operator's override and prints the unmet blocking criteria (operator question Q4). No
module evaluates a DoD check itself; `tests/orchestration/test_mission_gate.py`.

**T003 — the four templates.** `docs/contracts/{website,api-service,cli-tool,python-library}.md`,
each with its proposal phrases, criteria and one fixture order, are read and compiled by
`packages/orchestration/contract_templates.py`; the proposal is a deterministic phrase match,
`remedy do --contract <name>` forces a template and a name that is none exits 2 before any step,
and the planner's criteria are added after the template's, never replacing one (DECISION F269 D1;
`tests/orchestration/test_contract_templates.py`, `tests/cli/test_do_sequence_cli.py`).

**Hygiene.** Every template carries three blocking hygiene criteria checked by
`python3 -m packages.orchestration.contract_hygiene <unreferenced|replaced|stubs>` as `custom_cmd`
checks, and every build round runs the `unreferenced` and `replaced` rules over the files the job
added, turning a `pass` into `needs_repair` with the path in the finding; the reviewer's system
text carries the matching sentence (DECISION F269 D5; `tests/orchestration/test_contract_hygiene.py`,
`tests/orchestration/test_pingpong.py`).

**Repository binding and grants.** A job of a mission with a contract gets `target_repo` and the
grants `repo_test_run`, `repo_generated_write` and `repo_revert` from the contract at dispatch and
in `do`'s shape step; `remedy job attach-repo` and `remedy job permit` are deleted and listed in
`TestDeletedCommands` (DECISION F269 D7; operator question Q5).

**T004 — amendments.** `amend_mission_contract` adds one compiled `amendment` criterion and one
entry `{id, text, received_at, applies_from, criteria, understood, acknowledged_in}` applying from
the mission's next round; every job dispatched from that round carries its check, and the loop
acknowledges each due amendment in the mission's ledger before the round's move (DECISION F269 D8;
`tests/orchestration/test_orchestrator_loop.py`). No command sends an amendment: F264 owns the
channel.

**T005 — the remainder proposal.** At `run_mission`'s iteration limit, or when a `do` job stops at
its budget, with blocking criteria open, `raise_contract_remainder_decision` puts one decision in
the inbox naming every blocker and carrying the prefilled follow-up order; a `yes` at the CLI or
the cockpit starts the follow-up mission through `start_remainder_follow_up_mission`, whose
contract carries the blockers as `amendment` criteria under one entry `A001`, so planning it keeps
them (DECISIONs F269 D9 and D10).

**Findings.** R-0971 was raised and resolved inside the feature. No finding owned by F269 stays
open.
