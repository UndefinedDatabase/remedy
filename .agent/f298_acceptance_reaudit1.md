# F298 acceptance re-audit 1 (amend0930b-slow-cap hardening stage)

Commit audited: `10b98bcb748e4edc149e6330cd2bb73c0311e8b8` (branch `feature/f298-machine-client-contract-v1-1`).

## What was read, and what was not

Read: the feature file `docs/roadmap/features/T12_F298.md` (grep of its gate-test lines), the first audit
`.agent/f298_acceptance_audit.md`, `tests/cli/test_machine_client_contract.py` (F295's gate test),
`tests/cli/test_client_interface.py` (its imports and its last two tests, lines 1507 to 1533),
`apps/cli/client_interface.py` (lines 48 to 66, `CLIENT_OPERATION_IDS`).
Not read: `.agent/handoff.md`, `.agent/live_review*.md`, `.agent/plan.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/authored/`, any other `.remedy-wt/f298-*` folder. My grep for the
protocol's "amend0930b-slow-cap — SLOW MODE IS THE HARDENING STAGE" heading found no exact match (the heading is
on line 557 of `docs/agents/self_drive_protocol.md` with other punctuation); I did not read the paragraph and worked
from the task text.

## How the mutations ran

- Worktree `/home/decodeux/Repos/remedy/.remedy-wt/f298-reaudit-wt`, detached at the audited commit.
- One script, `/home/decodeux/Repos/remedy/.remedy-wt/f298-reaudit/run.py`; raw results in `result.json` beside it.
- Test command, cwd = the worktree: `python3 -B -m pytest -q -p no:cacheprovider -rfE <ids>`. One run at a time, no `-n`, no full suite.
- Each proof: `git status --porcelain` empty, control run (exit 0), one mutation, (CLI), one second pause, run again (exit 1),
  `git -C <worktree> checkout -- .`, `git status --porcelain` read back. All three read back empty.
- Test ids: `I` = `tests/cli/test_client_interface.py`, `G` = `tests/cli/test_machine_client_contract.py`.
  The guarding tests are `I::test_f295s_gate_test_is_unchanged` (a sha256 of the gate test file against
  `F295_GATE_TEST_SHA256`) and `I::test_every_command_and_flag_the_gate_test_drives_is_in_the_interface`
  (reads the gate test's commands and flags with `_gate_names()` and compares them to `build_client_interface()`).
- Test sets run (control 7 passed in A and B2): A and B2 ran the 4 ids/7 cases `I::test_f295s_gate_test_is_unchanged`,
  `G::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`,
  `G::test_the_contract_page_names_exactly_what_the_gate_test_uses` (4 kinds), `G::test_the_contract_page_carries_the_gate_tests_order_file`
  (B2 swapped the gate test for `I::test_every_command_and_flag_the_gate_test_drives_is_in_the_interface`; its set was 1 + 1 + 4 + 1 = 7).

## Claims and proofs

| # | Claim | Test | Mutation (file, exact change) | Control | Mutated | Verdict |
|---|---|---|---|---|---|---|
| A | F295's gate test and its path are unchanged | `I::test_f295s_gate_test_is_unchanged` | `G`: append the two lines `\n# audit mutation: a comment line\n` at the end of the file (no code change) | 7 passed | 1 failed, 6 passed: only `test_f295s_gate_test_is_unchanged` failed (sha256 `46896f76...` against `e6f4d57b...`); the gate test itself and the page tests stayed green | PROVED |
| B1 | The document names every command the gate test drives (production side) | `I::test_every_command_and_flag_the_gate_test_drives_is_in_the_interface` | `apps/cli/client_interface.py`: delete the line `    "change.proof",` from `CLIENT_OPERATION_IDS` | 1 passed | 1 failed: `the gate test drives a command the interface lacks`, `['remedy change proof'] == []`. CLI: `python3 -B -m apps.cli.main client interface --json` lists 14 operations unmutated (including `remedy change proof`, `remedy do run`, `remedy status run`, `remedy decision resolve`, `remedy job run`, `remedy job apply`), 13 mutated, `remedy change proof` the one lost | PROVED (CLI) |
| B2 | The document names every command the gate test drives (test side: a command the gate test drives that the interface does not name) | `I::test_every_command_and_flag_the_gate_test_drives_is_in_the_interface` | `G`: in the body of the gate test, after the last line `assert job_id not in status["client"]["awaiting_apply"]`, add `_remedy(["job", "list"], repo, env)` (`remedy job list` is not an operation) | 7 passed | 3 failed, 4 passed: the failures are `I::test_every_command_and_flag_the_gate_test_drives_is_in_the_interface`, `I::test_f295s_gate_test_is_unchanged`, `G::test_the_contract_page_names_exactly_what_the_gate_test_uses[commands]` (`the gate test uses commands the page does not name`, `['remedy job list']`). The failure text of the interface test was not captured (only its name in the summary) | PROVED |

## Gaps

None. Two limits, not gaps:
1. Claim A is guarded by a pinned digest, not by a comparison with history: a deliberate edit of the gate test that also
   updates `F295_GATE_TEST_SHA256` in the same commit passes. The test's own message says so, and only review sees that
   the new digest is justified.
2. The flag half of B (`used["flags"] - declared`) was not mutated here; the task named a production mutation and a gate-test mutation, and I ran the command half of each.

## Counts

- Claims re-audited: 3 (A, B1, B2; B is two mutations).
- Proved: 3 (A: PROVED; B1: PROVED (CLI); B2: PROVED).
- Gaps: 0.
- Mutation proofs run: 3, all restored with an empty `git status --porcelain`.
