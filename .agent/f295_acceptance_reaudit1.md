# F295 Machine client contract v1 — Repeated acceptance audit 1 (amend0930b-slow-cap rule (3))

I read only `docs/roadmap/features/T12_F295.md`, `docs/system/machine-client-contract-v1.md`, `AGENTS.md`, and the repository itself: source, tests, docs, `git log`, and `git -C /home/decodeux/Repos/remedy diff d0ca96e49 7179a592d -- packages apps tests docs`. I did not read `.agent/handoff.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/f295_acceptance_audit.md`, anything under `.agent/authored/`, or any other `.remedy-wt/f295-*` folder. All mutations ran in one disposable worktree, `/home/decodeux/Repos/remedy/.remedy-wt/f295-reaudit1-wt`, detached at base commit `7179a592d` (tip of `feature/f295-machine-client-contract-v1`); it has since been removed. Every pytest run used the mandated shape `python3 -B -m pytest -q -n auto -p no:cacheprovider <file::node_id>`; no full suite and no directory-wide run was ever issued. The primary checkout `/home/decodeux/Repos/remedy` stayed clean (`git status --porcelain` empty before and after). No run printed "the run left ... process(es) behind." `git branch --list "remedy/*"` was identical before and after (31 pre-existing job/scratch branches, none appeared or disappeared).

Statements audited: 5. Proven: 5. Gaps: 0.

## S1 — `--no-ui` opens no cockpit

> `remedy do` run as the machine client runs it (`--no-ui`) opens no cockpit.

**Test node id:** `tests/cli/test_do_sequence_cli.py::test_with_no_ui_the_cockpit_launcher_is_never_called_and_the_ui_step_says_so`

**Mutation 1** — `packages/orchestration/do_sequence.py`, `_step_ui` (line 1153): `if ctx.no_ui:` → `if False and ctx.no_ui:`. RED: `AssertionError: assert ['93ed19786e0846fb'] == []` (launcher called). GREEN after revert: `1 passed in 3.08s`.

**Mutation 2** — `apps/cli/commands/do_cmd.py`, `COMMAND_HANDLERS["do.run"]`: `no_ui=bool(getattr(args, "no_ui", False)),` → `no_ui=False,`. RED: `AssertionError: assert ['2258f5d05aa44bec'] == []`. GREEN after revert: `1 passed in 2.85s`.

**Reaches the user: yes** — test drives `from apps.cli.grouped import main`, exactly as a terminal invocation.

**Verdict: PROVEN.**

## S2 — An extend answers the remainder decision its own stop raised

> "... answers the decisions a run raises ..." — including that once a budget stop is answered, no question raised by that same stop is left open whose premise the answer ended.

**Test node ids:** `tests/orchestration/test_mission_contract.py::TestAnExtendAnswersTheRemainder` (5 unit tests); `tests/cli/test_do_sequence_cli.py::test_an_extend_answers_the_remainder_and_says_so_in_its_text`; `tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`.

**Mutation 1** — `packages/orchestration/mission_contract.py`, `answer_contract_remainder_on_extend`: inserted `return []` right after the `mission is None` guard. RED: `3 failed, 2 passed` (the 2 that still pass expect `[]` anyway — "no mission" and "already answered"). GREEN after revert: `5 passed in 0.99s`.

**Mutation 2** — `apps/cli/commands/decision.py` (line 653): `closed = answer_contract_remainder_on_extend(job_id, decision_id)` → call it but discard the result, `closed = []`. RED (CLI text): the "Remainder decision ... answered no" line missing. RED (full gate test): `AssertionError: assert [] == ['td:c5959dac']` on `answered["closed_decisions"]`. GREEN after revert: `1 passed in 4.07s`.

**Reaches the user: yes** — mutation 2's red-proof is the full gate test via `apps.cli.grouped.main`.

**Probes:**
- `abandon` instead of `extend`: CLI probe (`probe_abandon.py`, `python3 -m apps.cli.grouped ... --json` subprocess, scratch `REMEDY_DATA_DIR`) against the unmutated worktree. Result: `outcome abandoned`, `closed_decisions key present: False`, remainder decision **still open** after abandon, job state `cancelled`. This is correct by design, not a gap: only `extend` ends the remainder's premise (job runs on); `abandon` cancels the job, so the "start a follow-up mission?" question stays live. `decision.py`'s `abandoned` branch returns before ever calling `answer_contract_remainder_on_extend`.
- A second budget stop: CLI probe (`probe_second_stop.py`) tried extending with a deadline still in the past — correctly refused (`error: budget_limit_not_raised`, no `closed_decisions`), leaving the original open decision untouched. A genuine second stop with fresh ids is directly proven at the function level by `test_a_later_budget_stop_raises_a_fresh_remainder`, re-read and re-run here (passing). No stale-id leak found through the CLI layer.

**Verdict: PROVEN.**

## S3 — The digest lists every open decision, and no decision that is no longer open

> "the section lists every open decision across jobs with its question and default" — and lists no decision that is no longer open.

**Test node ids:** `tests/orchestration/test_client_digest.py::test_an_answered_task_decision_is_not_listed`; `tests/orchestration/test_client_digest.py::test_a_task_decision_with_a_default_is_listed_as_the_whole_d5_object`; `tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`.

**Mutation 1** — `packages/orchestration/client_digest.py` (line 224): `if decision.status == "open":` → `if True:`. RED (unit): `assert [{...}] == []`. RED (gate test): fails at `assert not [d for d in digest["decisions"] if d["job_id"] == job_id]` (closed remainder relisted). GREEN after revert: both `1 passed`.

**Mutation 2** — same file, `_decision_entry` (line 88): `safe_default = str(payload.get("safe_default", "") or "") if is_task_decision else ""` → `safe_default = ""`. RED: `'default': None` instead of `'8080'`. GREEN after revert: `1 passed in 1.00s`.

**Reaches the user: yes** — mutation 1's second red-proof is the full gate test via the CLI.

**Verdict: PROVEN.**

## S4 — The contract page names exactly what the gate test uses (JSON keys table)

> "names every command, flag, key, exit code and file the gate test uses; a test fails when the page names a flag or key the test does not use or the test uses one the page does not name" — JSON keys, both directions.

**Test node id:** `tests/cli/test_machine_client_contract.py::test_the_contract_page_names_exactly_what_the_gate_test_uses[keys]`

**Mutation A (page names something unused)** — `docs/system/machine-client-contract-v1.md`: added row `| \`bogus_extra_key\` | nowhere | ... |`. RED: `assert ['bogus_extra_key'] == []`. GREEN after revert: `1 passed in 0.91s`.

**Mutation B (test uses something unnamed)** — same file: deleted the `closed_decisions` row. RED: `assert ['closed_decisions'] == []`. GREEN after revert: `1 passed in 0.70s`; worktree confirmed byte-identical to base (`git status --porcelain` empty).

**Reaches the user: no (by design)** — a docs/test syntax-consistency check (`ast.parse` over the gate test compared against the markdown table), not a product run; this is the appropriate proof shape for this statement. S5 covers the CLI-path requirement.

**Verdict: PROVEN.**

## S5 — The gate test runs green, end to end, through the command line alone

**Test node id:** `tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line`

**Mutation** — `packages/orchestration/job_apply.py`, `apply_job`'s gate: `if dry_run or not approve:` → `if True:`. RED: step 5 (`job apply --approve`) always previews: `AssertionError: assert 'dry_run' == 'applied'`. GREEN after revert: `1 passed in 4.40s`.

This mutation plus every RED proof under S1–S3 (which all independently redden this same gate test, since it exercises `--no-ui`, the extend/remainder answer, and the post-run decisions list in one run) show it is a sensitive end-to-end guard, not one that stays green under mutation.

**Reaches the user: yes** — `_remedy()` drives `apps.cli.grouped.main` in-process with a stdin stand-in that fails the test on any read, across `do → status → decision resolve → job run → status → job apply --approve → change proof → status`.

**Verdict: PROVEN.**

## Gaps

None.

## Leak measurement

No statement's guarding test stayed green under its mutation; all 9 mutations (2×S1, 2×S2, 2×S3, 2×S4, 1×S5) turned their node id(s) red, and every revert turned them back green, confirmed byte-identical to base via `git status --porcelain` (empty) after each revert and again at the end. Two independent CLI probes (`abandon`; an extend that fails to clear the deadline) stress-tested S2 beyond its existing tests; neither surfaced a defect — both matched the documented, `extend`-only design of DECISION F295 D19.

## Worktree

```
/home/decodeux/Repos/remedy                                   7179a592d [feature/f295-machine-client-contract-v1]
/home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013    218eaabd6 [remedy/job-034ab8c2d9fa4013]
/home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d    09441a92a [remedy/job-129b3ad7206d4f8d]
/home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb    218eaabd6 [remedy/job-1fe227733cbf41eb]
/home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928    aab638e21 [remedy/job-6a38b3203cca4928]
/home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363    e4fa7d06f [remedy/job-d0f70d9d45dd4363]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831    cc8696a37 [remedy/job-e7268925db3a4831]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86    03d435e59 [remedy/job-e7a145761bf04f86]
/home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15    3f36bd811 [remedy/job-f03587d31f444b15]
/home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc    3f36bd811 [remedy/job-f196d785124e48bc]
/home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0    68c833e6c [remedy/job-fd57a5d1dfe245b0]
... (plus several /tmp/pytest-of-decodeux/... "prunable" worktrees, pre-existing test-harness artifacts unrelated to this audit)
```
`/home/decodeux/Repos/remedy/.remedy-wt/f295-reaudit1-wt` (this audit's own worktree) is **not** in the list — removed via `git worktree remove --force` as the last action.

Note: the harness refused to let me write `report.md` as a file (subagents must return findings as text), so this report exists only in this reply; the scratch helper scripts (`run_pytest.py`, `probe_abandon.py`, `probe_second_stop.py`) remain under `/home/decodeux/Repos/remedy/.remedy-wt/f295-reaudit1/`, which is gitignored.
