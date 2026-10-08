# F298 acceptance audit (amend0930b-slow-cap hardening stage)

Commit audited: `854097e88d95d30808f3aa24482fa651668ccf96` (branch `feature/f298-machine-client-contract-v1-1`).
Feature file: `docs/roadmap/features/T12_F298.md`.

## What was read, and what was not

Read: the feature file; the amend0930b-slow-cap paragraph of `docs/agents/self_drive_protocol.md` (rule 2);
`apps/cli/client_interface.py`; `tests/cli/test_client_interface.py`; `tests/cli/test_machine_client_contract.py`
(F295's gate test); `packages/orchestration/client_digest.py`, `apps/cli/commands/status_cmd.py`,
`apps/cli/commands/patch.py`, `packages/orchestration/mission_state.py` (only the lines mutated);
`docs/system/machine-client-contract-v1.md` (the generated section and its edges).
Not read: `.agent/handoff.md`, `.agent/live_review*.md`, `.agent/plan.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/authored/`, any other `.remedy-wt/f298-*` folder.

## How the mutations ran

- Worktree: `/home/decodeux/Repos/remedy/.remedy-wt/f298-audit-wt`, detached at the audited commit.
- Scripts (in `/home/decodeux/Repos/remedy/.remedy-wt/f298-audit/`): `h.py` (harness), `run1.py` (m01 to m06),
  `run2.py` (m07 to m14), `run3.py` (m15), `run4.py` (m16), `show.py`, `gatecmds.py`. Per-proof raw results are
  `out/<name>.json`.
- Command for every test run, cwd = the worktree: `python3 -B -m pytest -q -p no:cacheprovider <ids>`. One run at a
  time, no `-n`, no full suite. CLI proofs: `python3 -B -m apps.cli.main client interface --json` and
  `python3 -B -m apps.cli.main status --json` (data root `.remedy-wt/f298-audit/data`), cwd = the worktree.
- Each proof: worktree status empty, (CLI unmutated), tests unmutated (control, exit 0), the mutation, (CLI mutated),
  one second pause, tests again (exit 1), `git -C <worktree> checkout -- .`, then `git status --porcelain` read back.
  The status after restore was empty after all 16 proofs (recorded as `status_after_restore` in each result file).

## Claims and proofs

Test file `I` = `tests/cli/test_client_interface.py`, `G` = `tests/cli/test_machine_client_contract.py`.
Production file `CI` = `apps/cli/client_interface.py`.

| # | Claim | Test | Mutation (production file, exact change) | Control | Mutated | Verdict |
|---|---|---|---|---|---|---|
| 1 | G&D: the contract document is generated from the code (a change in the catalog shows in it) | `I::test_each_operation_is_its_catalog_entry_in_the_declared_order` | m13: `CI` `"description": entry.description,` -> `"description": "",` | 1 passed | 1 failed; CLI: `job.apply` description `Review and apply job workspace changes to target r...` unmutated, empty mutated | PROVED (CLI) |
| 2 | G&D: the document names every operation | `I::test_every_operation_declares_its_refusal_tokens`, `I::test_every_declared_answer_is_a_sorted_list_of_payload_keys`, `I::test_each_operation_is_its_catalog_entry_in_the_declared_order` | m01: `CI` drop `"mission.abandon",` from `CLIENT_OPERATION_IDS`. Also m15: drop `job.evidence` from the ids, token and answer-key tables and regenerate the page | m01 3 passed; m15 65 passed | m01 2 failed, 1 passed; m15 4 failed, 59 passed. CLI: `client interface --json` lists 14 operations unmutated, 13 mutated | PROVED (CLI) |
| 3 | G&D: the document names every operation's fields: its arguments, and whether each takes a value | `I::test_a_switch_takes_no_value_and_a_collected_option_repeats`, `I::test_each_operation_is_its_catalog_entry_in_the_declared_order` | m02: `CI` `"takes_value": action.nargs != 0,` -> `"takes_value": True,` | 2 passed | 2 failed. CLI: `job.apply` `--approve` `takes_value` false unmutated, true mutated | PROVED (CLI) |
| 4 | G&D: the document names every operation's answer keys (top level) | `I::test_declared_answer_keys_equal_the_keys_the_handler_reaches[status.run]` | m07: `apps/cli/commands/status_cmd.py` `"stops_pending": stops_pending,` -> `"stops_pending_x": stops_pending,` | 1 passed | 1 failed. CLI: `status --json` top keys carry `stops_pending` unmutated, `stops_pending_x` mutated | PROVED (CLI) |
| 5 | G&D: the document names the keys below the top level of the answers | `I::test_the_mission_answer_trees_name_exactly_what_their_code_builds` | m16: `packages/orchestration/mission_state.py` `MissionOrder.to_json` gains key `"audit_extra": 1` | 1 passed | 1 failed | PROVED |
| 6 | G&D: the document names the digest's keys | `I::test_the_digest_tree_names_exactly_the_keys_the_digest_code_writes` | m08: `packages/orchestration/client_digest.py` adds `"audit_extra_key": 1,` to the returned dict | 1 passed | 1 failed. CLI: `status --json` `client` keys gain `audit_extra_key` | PROVED (CLI) |
| 7 | G&D: the document names every job state word | `I::test_the_vocabularies_are_the_products_own` | m05: `CI` `[state.value for state in RunState]` -> `[...][:-1]` | 1 passed | 1 failed. CLI: `job_states` has 9 words unmutated (last `stopped`), 8 mutated | PROVED (CLI) |
| 8 | G&D: the document names every mission status word | `I::test_the_vocabularies_are_the_products_own` | m06: `CI` `list(MISSION_STATUSES)` -> `list(MISSION_STATUSES)[:-1]` | 1 passed | 1 failed. CLI: `mission_statuses` loses `abandoned` | PROVED (CLI) |
| 9 | G&D: the document names every refusal token | `I::test_declared_tokens_equal_the_tokens_the_handler_reaches[patch.approve]` and `[patch.reject]` | m03: `apps/cli/commands/patch.py` every `"patch_intent_not_found"` -> `"patch_intent_missing"` | 2 passed | 2 failed | PROVED |
| 10 | G&D: the document names every exit code | `I::test_the_vocabularies_are_the_products_own`, `I::test_the_pages_generated_section_is_the_interface_rendered` | m04: `CI` `for meaning in CLI_EXIT_CODES` -> `for meaning in CLI_EXIT_CODES[:-1]` | 2 passed | 2 failed. CLI: `exit_codes` has 5 entries unmutated, 4 mutated | PROVED (CLI) |
| 11 | Acc: a test fails when the code returns a key the document does not name (written as a dict literal) | `I::test_the_digest_tree_names_exactly_the_keys_the_digest_code_writes` | m08 (same as claim 6) | 1 passed | 1 failed | PROVED (CLI) |
| 12 | Acc: the same, for a key the code adds by other means than a literal (`**dict(...)`), seen in a real run | `I::test_a_real_runs_digest_returns_only_keys_the_tree_names` (with the static test) | m10: `client_digest.py` `return {` gains `**dict(audit_dynamic_key=1),` | 2 passed | 1 failed, 1 passed (the static test stays green; the real-run test fails). CLI: `status --json` `client` keys gain `audit_dynamic_key` | PROVED (CLI) |
| 13 | Acc: a test fails when the document names a key the code does not return | `I::test_the_digest_tree_names_exactly_the_keys_the_digest_code_writes`, `I::test_the_pages_generated_section_is_the_interface_rendered` | m09: `CI` `DIGEST_KEY_TREE` gains `"audit_phantom_key": {}` | 2 passed | 2 failed | PROVED |
| 14 | Acc: the Markdown page is the document's rendering | `I::test_the_pages_generated_section_is_the_interface_rendered`, `I::test_the_pages_generated_section_reads_back_as_the_interface` | m11: edit the committed page, `Mission statuses: ...`, drop `abandoned`. m12: `CI` `_yes` returns `"Yes"/"No"` | m11 2 passed; m12 2 passed | m11 2 failed; m12 1 failed, 1 passed (the rendered-equals test fails) | PROVED |
| 15 | Acc: F295's gate test is green (its path works) | `G::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line` | m14: `client_digest.py` `CLIENT_DIGEST_VERSION = 1` -> `2` | 1 passed | 1 failed (`assert 2 == 1`, line 133) | PROVED |
| 16 | Acc: F295's gate test and its path are unchanged | none | not mutable: it is a claim about history | not applicable | not applicable | GAP |

Counts note: 16 rows because the Acceptance line about keys is two claims (rows 11 and 13) and row 12 is the
dynamic-key variant of row 11. Rows 1 to 10 are the Goal & Done sentence split into its separate claims.

## Moved, not audited

The Built State says F298 keeps two Acceptance lines (keys, and F295's gate test) and one Goal & Done claim (the
generated document). Moved to F304 and not audited:

1. Acceptance: an order with `project: b`, started in repository A or in no repository, changes only b's registered repository or is refused before any step.
2. Acceptance: a blocked apply under `--approve --json` exits non-zero with `"ok": false` and a listed token.
3. Acceptance: a declined job reads `waits_for_apply` false, is not in `awaiting_apply`, and its decision is in the ownership record.
4. Acceptance: the second gate test is green through the command line alone, with a stdin that fails on any read.
5. Acceptance: the digest names calls and tokens by kind, and an order capped only by provider calls or total tokens is accepted and stopped at its cap.
6. Acceptance: with 1,000 settled jobs the default digest stays under a fixed size and names the count it left out.
7. Acceptance: a second `remedy do` of an order file a running mission records exits 2 before any step.
8. Goal & Done: the second gate test (an order in the named project's repository, an apply that commits and pushes, a declined result, an order of more than one job, an order started twice).

(Also out of this audit by the same split: T002 to T007 of the task slicing.)

## Gaps

1. Claim 16, "F295's gate test and its path are unchanged": no test can hold a test file's own history, so only a
   green gate test (claim 15) guards the path. Measured at the audit: `git diff 77493e0f91 854097e88 --
   tests/cli/test_machine_client_contract.py` is empty (77493e0f91 is the merge base with `main`), and no commit
   in that range touched `do_cmd.py`, `status_cmd.py` or `client_digest.py`. The hand-written part of the page
   changed at lines 3 to 7 (a note added); the rest of the diff is the appended generated section. So the claim is
   true of the product today, but nothing fails if a later change edits the gate test to match a changed path.
   It is a gap by rule 2 only because there is no test; it is a review-time fact.

Observations that are not gaps:
- The static digest test is blind to a key added by `**dict(...)`; the real-run test (claim 12) catches it. Both are needed.
- `CLIENT_OPERATION_IDS` has no anchor outside the code and the tests that name operations: the gate test's commands
  (`change proof`, `decision resolve`, `do`, `job apply`, `job run`, `status`) are all in the interface today
  (measured with `gatecmds.py`; `remedy do` and `remedy status` are the aliases of `do run` and `status run`), but no
  test compares them. Dropping an existing operation fails tests (m15); adding a new client command to the gate test
  without the interface would not.
- Claim 14: changing only the case of the page's yes/no words stays green in the read-back test, red in the
  rendered-equals test.

## Counts

- Claims audited: 16.
- With a proving test at once: 15 (rows 1 to 15; each went red under its mutation and green without it).
- Proofs through the command line: 10 rows (1, 2, 3, 4, 6, 7, 8, 10, 11, 12), where `client interface --json` or `status --json` printed different output unmutated and mutated.
- Gaps: 1 (row 16).
- Mutation proofs run: 16 (m01 to m16), all restored with an empty `git status --porcelain`.
