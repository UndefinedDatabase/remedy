# F295 Machine client contract v1 — Acceptance audit (amend0930b-slow-cap hardening stage)

I read only `docs/roadmap/features/T12_F295.md`, `AGENTS.md`, `docs/system/machine-client-contract-v1.md`, the repository's source/test/docs files, `git log`/`git diff 9a8431ea9..d0ca96e49 -- packages apps tests docs`, and `git merge-base d0ca96e49 main` (confirmed `9a8431ea9`). I did not read `.agent/handoff.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, anything under `.agent/authored/`, or any `.remedy-wt/f295-r*` folder.

All mutations ran in one disposable worktree, `/home/decodeux/Repos/remedy/.remedy-wt/f295-audit-wt`, created detached at `d0ca96e49` and removed as the last step. Every pytest run was `python3 -B -m pytest -q -n auto -p no:cacheprovider <one node id>`, via a scratch driver script under `/home/decodeux/Repos/remedy/.remedy-wt/f295-audit/run.py`; no full suite and no directory-level selection ran, and no two runs ran at once. The primary checkout `/home/decodeux/Repos/remedy` stayed clean (`git status --porcelain` empty) before, during and after.

**Total claims audited: 31. Proven at once: 28. Gaps: 2. Measurement-only: 1.**

## Claim 1 (Goal & Done) — writes an order file, starts Remedy
Test: `tests/cli/test_do_order_file.py::test_an_order_file_with_a_cost_cap_plans_and_runs_its_order`. Mutation (`packages/orchestration/order_file.py::order_argument_names_file`): `return stripped.lower().endswith(".md")` → `return False`. Red: `AssertionError: assert 'Write a CONTRIBUTING.md' in '# Mission Plan\n...'`. Green: `1 passed in 2.90s`. Reaches the user: yes (in-process `apps.cli.grouped.main`). **PROVEN.**

## Claim 2 (Goal & Done) — polls one machine-readable digest
Test: `tests/orchestration/test_client_digest.py::test_build_client_digest_on_an_empty_data_root_equals_the_version_1_frame`. Mutation (`client_digest.py`): `CLIENT_DIGEST_VERSION = 1` → `2`. Red: `Differing items: {'version': 2} != {'version': 1}`. Green: `1 passed in 0.78s`. Reaches the user: no (unit-level). **PROVEN.**

## Claim 3 (Goal & Done) — answers the decisions a run raises
Test: `tests/cli/test_decision_cmd.py::TestABudgetDecisionAnsweredThroughTheCommandLine::test_extend_records_the_answer_and_the_job_runs_to_its_end`. Mutation (`budget_decision.py`): dropped `.append(record)` so the answer is computed but never recorded. Red: `assert not [{'created_at': ..., 'id': 'budget:budget_...'}]`. Green: `1 passed in 3.56s`. Reaches the user: yes, via `apps.cli.grouped.main`. **PROVEN.**

## Claim 4 (Goal & Done) — approves the apply
Test: the full gate test `tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`. Mutation (`job_apply.py`): `result.status = "applied"` → `"done"`. Red: `assert 'done' == 'applied'`. Green: `1 passed in 3.84s`. Reaches the user: yes. **PROVEN.**

## Claim 5 (Goal & Done) — reads the proof
Same gate test. Mutation (`proof_chain.py`): `job_applies = tuple(...)` → `job_applies = ()`. Red: `assert [] == ['135ee7f5341e483f']` at the `change proof` step. Green: `1 passed in 4.01s`. Reaches the user: yes. **PROVEN.**

## Claim 6 (Goal & Done) — through the command line's JSON envelope alone
Same gate test. Mutation (`apps/cli/json_envelope.py::_write`): added a stray `print("notice: envelope follows", file=stream)` before the JSON line. Red: `AssertionError: ... printed no single JSON envelope ...` (json.loads failed). Green: `1 passed in 4.40s`. Reaches the user: yes. **PROVEN.**

## Claim 7 (Goal & Done) — no cockpit
Mutation (`do_sequence.py::_step_ui`): `if ctx.no_ui:` → `if False:` (defeats the `--no-ui` skip). Result: `tests/cli/test_do_order_file.py::test_an_order_file_with_a_cost_cap_plans_and_runs_its_order` **stayed GREEN** (`1 passed in 6.26s`), and pytest reported verbatim: `remedy tests: the run left 1 process(es) behind, now ended (F293 T003): pid 2818793: /usr/bin/python3 -m apps.cli.grouped ui start 5ec28d8557574629 --port 0 --info-file ...`. A real cockpit server process was spawned and no test assertion noticed. The gate test also stayed green under the same mutation (its run stops on budget before reaching the `ui` step). **GAP.**

## Claim 8 (Goal & Done) — no HTTP transport
**MEASUREMENT-ONLY.** The feature file's own "Do not touch" and "Why this exists" sections defer the HTTP API to F253 ("why the HTTP API (F253) comes later"). No HTTP code exists in this path to mutate, and no test can pin the absence of a subsystem never built.

## Claim 9 (Goal & Done) — no question on stdin
Mutation A (`exec_guard.py`): `stdin=subprocess.DEVNULL` → `stdin=None`. Test: `tests/orchestration/test_exec_guard.py::test_a_guarded_child_reads_end_of_file_while_the_callers_stdin_is_an_open_pipe`. Red: hung until wall timeout, `assert 'wall_timeout' == 'None 0'` (21.21s). Green: `1 passed in 1.00s`. Mutation B (`apps/cli/cost_preview_confirm.py`): `if not _stdin_is_a_tty():` → `if False:`. Test: `tests/cli/test_cost_preview_confirm.py::test_on_an_open_pipe_the_confirmation_answers_without_reading_stdin`. Red: `subprocess.TimeoutExpired: ... timed out after 60 seconds`. Green: `2 passed in 1.02s`. Both tests spawn a real subprocess of the repo's interpreter; `tests/cli/test_do_flags.py::test_an_unattended_do_on_an_open_pipe_finishes_without_reading_stdin` additionally proves the whole claim via a real `python3 -m apps.cli.main` subprocess (read, not re-mutated). **PROVEN.**

## Claim 10 (Goal & Done) — one test drives the whole path through `apps.cli.grouped.main`
Same test/mutations as Claims 4–6. **PROVEN** (not re-run).

## Claim 11 (Goal & Done) — contract page names every command/flag/key/exit code/file the path uses
Same as Acceptance Claims 27–29. **PROVEN** (not re-run here).

## Claim 12 (Acceptance) — readable `.md` path plans and runs
Same as Claim 1. **PROVEN.**

## Claim 13 (Acceptance) — missing path exits 2 before any step, naming the path
Test: `test_a_missing_md_path_exits_2_with_order_file_not_found_and_no_missions_dir`. Mutation: `"order_file_not_found"` → `"order_file_unreadable"` on `FileNotFoundError`. Red: `assert 'order_file_unreadable' == 'order_file_not_found'`. Green: `1 passed in 0.99s`. **PROVEN.**

## Claim 14 (Acceptance) — empty path (whitespace-only body) exits 2
Test: `test_an_order_empty_after_its_header_exits_2_with_order_file_empty`. Mutation: disabled the `order_file_empty` raise. Red: `assert 'invalid_argument' == 'order_file_empty'`. Green: `1 passed in 0.87s`. **PROVEN.**

## Claim 15 (Acceptance) — unreadable path exits 2
Test: `test_a_directory_named_order_md_exits_2_with_order_file_unreadable`. Mutation: `"order_file_unreadable"` → `"order_file_not_found"` on generic `OSError`. Red: `assert 'order_file_not_found' == 'order_file_unreadable'`. Green: `1 passed in 0.82s`. Separately confirmed without mutation: `chmod 0o000` also yields `order_file_unreadable` via the same `except OSError` branch. **PROVEN.**

## Claim 16 (Acceptance) — no cost cap and no `--max-cost-usd` exits 2, naming the rule
Test: `test_an_order_file_without_a_cost_cap_or_flag_exits_2_naming_max_cost_usd`. Mutation (`do_cmd.py`): disabled the cost-cap check. Red: `Failed: DID NOT RAISE <class 'SystemExit'>`. Green: `1 passed in 0.91s`. **PROVEN.**

## Claim 17 (Acceptance) — whitespace argument stays text even naming a `.md` file
Test: `test_text_holding_whitespace_or_no_dot_md_suffix_is_not_a_file[fix the heading in README.md]` (the Acceptance line's own example). Mutation: disabled the whitespace check. Red: `assert True is False`. Green: `4 passed in 1.05s`. **PROVEN.**

## Claim 18 (Acceptance) — only a single whitespace-free `.md` path is read as a file
Mutation: `.lower()` dropped from the suffix check. Test: `test_a_single_dot_md_path_in_any_case_with_outer_whitespace_names_a_file[ORDER.MD]`. Red: `assert False is True`. Green: `4 passed in 0.74s`. **PROVEN.**

## Claim 19 (Acceptance) — digest carries a version field
Same as Claim 2. **PROVEN.**

## Claim 20 (Acceptance) — decisions list with question and default
Test: `test_a_task_decision_with_a_default_is_listed_as_the_whole_d5_object`. Mutation: `"default": safe_default or None` → `"default": None`. Red: dict diff on `'default'`. Green: `1 passed in 0.62s`. **PROVEN.**

## Claim 21 (Acceptance) — job waiting for apply listed as such
Test: `tests/cli/test_status_cmd.py::test_a_full_do_without_apply_completes_the_job_and_it_awaits_apply`. Mutation: `waits_for_apply = plan.state == JOB_COMPLETED and not job_apply_landed(job_id)` → `False`. Red: `assert False is True`. Green: `1 passed in 2.90s`. **PROVEN.**

## Claim 22 (Acceptance) — section says whether a supervisor answers
Test: `test_a_listening_socket_makes_supervisor_answers_true_closing_it_makes_it_false`. Mutation: `socket_answers(serve_paths().socket)` → `False`. Red: `assert False is True` with a real UNIX socket bound. Green: `1 passed in 1.08s`. **PROVEN.**

## Claim 23 (Acceptance) — every decision kind answerable with `--json`, recorded as the cockpit's own door records it
Budget: same as Claim 3. Hunk: test `tests/cli/test_patch_cmd.py::TestTheHunksCommandIsTheReadSide::test_it_reads_back_the_decision_approve_hunks_recorded`; mutation (`hunk_decision_record.py`): removed `records[attempt_key] = exported` while still returning success. Red: `assert '' == '2026-10-07T...431370+00:00'`. Green: `1 passed in 1.16s`. Confirmed (by reading `ui_server.py:4132`) that the CLI and the cockpit's own route share `record_hunk_decision_from_view`. Task/plan/proposal/veto kinds verified by reading `test_decision_cmd.py`'s dispatcher classes (not independently mutated — same core modules). **PROVEN.**

## Claim 24 (Acceptance) — `--yes --no-ui --json` on a non-TTY pipe never reads stdin
Same as Claim 9. **PROVEN.**

## Claim 25 (Acceptance) — contract page exists
Via `test_the_contract_page_carries_the_gate_tests_order_file`, which would raise `FileNotFoundError` if the page were absent; Claim 27 shows red/green for a content change. **PROVEN.**

## Claim 26 (Acceptance) — contract page is indexed
Mutation (`docs/README.md`): removed both lines linking `machine-client-contract-v1.md` (Quick-Find Table row and catalog row with description). Result: `tests/orchestration/test_doc_staleness.py::TestAgainstTheRealTree::test_the_real_tree_does_not_raise_and_every_claim_names_an_existing_document` **stayed GREEN** (`1 passed in 0.80s`). Confirmed via `git show 4b1fab0f1 --stat`: the commit that added the page touched only `docs/README.md` and the page itself, no test file. **GAP.**

## Claim 27 (Acceptance) — page names every command/flag/key/exit code/file the gate test uses
Test: `test_the_contract_page_names_exactly_what_the_gate_test_uses[flags]` (parametrized identically over commands/flags/keys/exit codes). For `file`: `test_the_contract_page_carries_the_gate_tests_order_file`; mutation: `max-cost-usd: 1` → `2` in the page's embedded order-file block. Red: text-containment assertion failed. Green: `1 passed in 0.88s`. Caveat: the `file` dimension is proven one-directionally only (one file in play, no table to check the reverse). **PROVEN** with that caveat noted (not a gap — the Acceptance text is satisfied as written).

## Claim 28 (Acceptance) — test fails when the page names a flag/key the test does not use
Mutation: added a bogus `--dry-run` row to the Flags table. Red: `assert ['--dry-run'] == []`. Green: `4 passed in 1.01s`. **PROVEN.**

## Claim 29 (Acceptance) — or the test uses one the page does not name
Mutation: removed the `--approve` row from the Flags table. Red: `assert ['--approve'] == []`. Green: `4 passed in 0.84s`. **PROVEN.**

## Claim 30 (Acceptance) — the gate test runs green, end to end, through the command line alone
Same as Claims 4–6. **PROVEN** (not re-run).

## Claim 31 — `PATH_SECTION_HEADING` scope confirmation
Read, not independently mutated; subsumed by Claim 27's mechanism. **PROVEN** (not an independent 32nd proof).

## Gaps

1. **No cockpit (Goal & Done).** `remedy do --no-ui` opening no cockpit has no guarding test. Defeating the `--no-ui` skip in `_step_ui` (`packages/orchestration/do_sequence.py`) left an existing test green while actually spawning a real `apps.cli.grouped ui start` child process, caught only by pytest's own leak detector. Smallest fix: one assertion that the `"ui"` step is `"skipped"` with `"--no-ui given"`, or a `launch_do_cockpit` tripwire proving it is never called under `--no-ui` (the pattern already exists for the with-UI case in `test_do_sequence_cli.py`).

2. **Contract page's docs index registration (Acceptance).** "is indexed" has no guarding test. Removing both of `docs/README.md`'s links to the page left the real-tree doc-staleness test green, and the commit that added the page touched no test. Smallest fix: a rule in `tests/orchestration/test_doc_staleness.py` (or a narrow dedicated test) that every `docs/system/*.md`/`docs/guides/*.md` page has an inbound link from `docs/README.md`, run against the real tree.

## Leak measurement

Before the first test run: `git branch --list "remedy/*"` listed 32 branches; `git worktree list` listed 22 entries (11 real `.remedy-wt/job-*` worktrees plus 11 `/tmp/pytest-of-decodeux/...` leftovers, all pre-existing). After the last test run (before removing my own worktree): identical 32 branches, identical 22 entries plus exactly one new entry — my own `/home/decodeux/Repos/remedy/.remedy-wt/f295-audit-wt` (detached at `d0ca96e49`). No branch and no worktree other than my own appeared during this audit. The one leak event (Gap 1) was a child *process*, not a branch/worktree, and pytest's own cleanup reported it ended on its own.

## Final `git worktree list`

```
/home/decodeux/Repos/remedy                                                                                                                           d0ca96e49 [feature/f295-machine-client-contract-v1]
/home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013                                                                                           218eaabd6 [remedy/job-034ab8c2d9fa4013]
/home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d                                                                                           09441a92a [remedy/job-129b3ad7206d4f8d]
/home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb                                                                                           218eaabd6 [remedy/job-1fe227733cbf41eb]
/home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928                                                                                           aab638e21 [remedy/job-6a38b3203cca4928]
/home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363                                                                                           e4fa7d06f [remedy/job-d0f70d9d45dd4363]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831                                                                                           cc8696a37 [remedy/job-e7268925db3a4831]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86                                                                                           03d435e59 [remedy/job-e7a145761bf04f86]
/home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15                                                                                           3f36bd811 [remedy/job-f03587d31f444b15]
/home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc                                                                                           3f36bd811 [remedy/job-f196d785124e48bc]
/home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0                                                                                           68c833e6c [remedy/job-fd57a5d1dfe245b0]
/tmp/pytest-of-decodeux/pytest-30246/.../.remedy-wt/50755aa8c0484c14   c2b9a817f [remedy/50755aa8c0484c14] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/57e6581477dd4f10   4ae5d4d33 [remedy/57e6581477dd4f10] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/e335c1f4a3ad438b   4ae5d4d33 [remedy/e335c1f4a3ad438b] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/813f1746c820462c   4ae5d4d33 [remedy/813f1746c820462c] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/a9cafea770cf4d1f   4ae5d4d33 [remedy/a9cafea770cf4d1f] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/c7955c02353a40f3   4ae5d4d33 [remedy/c7955c02353a40f3] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/cf414216490f48bc   4ae5d4d33 [remedy/cf414216490f48bc] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/bb666e9a683b4810   4ae5d4d33 [remedy/bb666e9a683b4810] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/02250b2c16aa40b1   4ae5d4d33 [remedy/02250b2c16aa40b1] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/4fcdf52ee5e645f1   4ae5d4d33 [remedy/4fcdf52ee5e645f1] prunable
/tmp/pytest-of-decodeux/pytest-30268/.../.remedy-wt/7d2c9fbf9c1a4036   4ae5d4d33 [remedy/7d2c9fbf9c1a4036] prunable
```

All entries above pre-date this audit. My own `.remedy-wt/f295-audit-wt` worktree has been removed and no longer appears.
