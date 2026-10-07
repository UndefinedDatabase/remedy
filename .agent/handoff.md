# Handoff — F298 session 1, round 2: T001's first part, the machine client interface and `remedy client interface`

## Session

SESSION 1 of feature F298 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~8 % (claim · T001 first part landed · T001 rest and T002 to T007 open) — Schätzung

## Range

Review of `0deb416e6c59748acb006b213ac7385ec3bb9e78`..HEAD (HEAD is C4 below).

## Commits

### e22496735 F298 R2 C1: book round 1, two prose slips, DECISION F298 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f298-r2.md` | 131/0 (new) | byte copy of the reviewer's `block.md` (131 lines, sha256 `b7456bd6a12dd3a04cb826d54bf1e41fc576db0404a4e5da356249392011f74b`) |
| `.agent/decisions.md` | 10/0 | base blob at `0deb416e6` followed by `append-decisions.txt` (DECISION F298 D2) |
| `.agent/live_review.md` | 2/0 | base blob at `0deb416e6` followed by `append-live_review.txt` (books round 1's PASS) |
| `.agent/plan.md` | 16/13 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 2/0 | base blob at `0deb416e6` followed by `append-prose_slips.txt` (two prose slips) |

### 29d8a9f70 F298 R2 C2: the machine client interface read from the code, and remedy client interface (T001, DECISION F298 D2)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 102/0 (new) | byte copy of `dry-client_interface.py`: `build_client_interface()`, reading the catalog, exit codes, job states, mission statuses, contract templates and budget kinds |
| `apps/cli/commands/client_cmd.py` | 41/0 (new) | byte copy of `dry-client_cmd.py`: `client.interface` handler, text and `--json` |
| `apps/cli/commands/__init__.py` | 2/1 | byte copy of `dry-commands_init.py`: imports and registers `client_cmd` |
| `apps/cli/command_catalog.py` | 13/0 | byte copy of `dry-command_catalog.py`: the `client` advanced group and the `client.interface` command entry |
| `tests/cli/test_client_interface.py` | 102/0 (new) | byte copy of `dry-test_client_interface.py`: the interface's tests, including the live-reading and KeyError-on-gap tests |
| `tests/cli/test_cli_ux.py` | 5/4 | byte copy of `dry-test_cli_ux.py`: `client` added to `_INTERNAL_GROUPS` and the D4 group-count assertion raised from 34 to 35 |
| `tests/orchestration/import_reachability_allowlist.txt` | 2/0 | byte copy of `dry-import_reachability_allowlist.txt`: `apps.cli.client_interface` and `apps.cli.commands.client_cmd` added |

### b9ea95f29 F298 R2 C3: the machine client page and the docs index name remedy client interface

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 11/0 | byte copy of `dry-machine-client-contract-v1.md`: the new "The interface as data" section naming `remedy client interface --json` |
| `docs/README.md` | 1/1 | byte copy of `dry-docs_README.md`: the page's index row grows the clause naming `remedy client interface` |

### F298 R2 C4: handback (self-reference exception: the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f298-machine-client-contract-v1-1`: outcome, including whether an HTTP
  500 retry was needed, is in the worker's final reply (write-once rule; not known when this file
  is written).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run before any write:
  empty list, so the Open PR Gate passed with no action needed.
- No merge, no branch switch, no new branch, no force-push, no pull, no pull request opened.

## Verification

0. Before any write: `block.md` and every `append-*` and `dry-*` file named in the prompt matched
   its sha256 digest (14 of 14, Python `hashlib.sha256` over the bytes); `block.md` is 131 lines,
   matching its stated line count. `git rev-parse HEAD` read
   `0deb416e6c59748acb006b213ac7385ec3bb9e78`, equal to `origin/feature/f298-machine-client-contract-v1-1`;
   `git branch --show-current` read `feature/f298-machine-client-contract-v1-1`; `git status --porcelain`
   empty. `gh pr list --state open ...` returned `[]`.
1. `git branch --show-current` read `feature/f298-machine-client-contract-v1-1` before every commit
   below.
2. C1: five byte-equality proofs all `True` (block copy; `.agent/live_review.md`,
   `.agent/decisions.md` and `.agent/prose_slips.md` each equal to their base blob at `0deb416e6`
   plus the matching `append-*.txt`; `.agent/plan.md` equal to `dry-plan.md`). Numstat before
   commit: `131 0` block copy, `2 0` live_review.md, `10 0` decisions.md, `2 0` prose_slips.md,
   `16 13` plan.md — matching the block exactly.
3. C2: seven byte-equality proofs, one per path against its `dry-*` file, all `True`. Numstat
   before commit: `102 0` client_interface.py, `41 0` client_cmd.py, `2 1` commands/__init__.py,
   `13 0` command_catalog.py, `102 0` test_client_interface.py, `5 4` test_cli_ux.py, `2 0`
   import_reachability_allowlist.txt — matching the block exactly. `git diff --cached` read as
   self-review before commit.
4. C3: two byte-equality proofs, both `True`. Numstat before commit: `11 0` the page, `1 1` the
   index — matching the block exactly.
5. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty. All 14 byte proofs
   of C1, C2 and C3 re-run after all three commits, all `True`.
6. **Gate 2**:
   `python3 -m pytest -q -rfEs tests/cli/test_client_interface.py tests/cli/test_cli_ux.py tests/orchestration/test_import_reachability.py tests/cli/test_exit_codes.py tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/test_help_renderer.py tests/test_grouped_cli.py tests/cli/test_advertised_commands.py tests/cli/test_list_commands_everywhere.py tests/cli/test_json_contract.py tests/cli/test_product_spine.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_doc_staleness.py tests/test_test_categories.py tests/test_remedy_smoke_script.py tests/ui_contracts/test_humanize_catalog.py tests/cli/test_machine_client_contract.py tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py --deselect tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes --deselect tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`
   — whole output: 28 lines of dots, 1988 dots total, no `F`, `E` or `s` character in any line,
   captured exit code `0` (`subprocess.run(...).returncode`), last line verbatim `1988 passed, 2
   deselected in 137.60s (0:02:17)`. Run once, as the round's one test selection.
7. **Gate 3**: `python3 -m ruff check apps/cli/client_interface.py apps/cli/commands/client_cmd.py
   apps/cli/commands/__init__.py apps/cli/command_catalog.py tests/cli/test_client_interface.py
   tests/cli/test_cli_ux.py` — captured exit code `0`, whole output `All checks passed!`.
8. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — captured exit code `0`:
   ```
   {"check_count": 6, "checks": [{"message": "handlers=176", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
   Six of six `pass`, `"fail_count": 0`.
9. **Gate 5**:
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — captured exit code `0`, whole output:
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`
   — an exact match to the block's expected list.
10. **Gate 6**: `python3 -m apps.cli.main client interface` — captured exit code `0`, whole output:
    ```
    Machine client interface 1.1
    Operations:
      remedy do run — Plan and run what you ask: study the repo, plan a mission of jobs and their tasks, run the first job, and stop before apply unless --apply.
      remedy status run — Show project status overview, across its repos and missions.
      remedy decision resolve — Resolve a decision (if backed by a resolvable record).
      remedy job run — Run pending job tasks sequentially through Builder/Reviewer/Repair.
      remedy job resume — Resume a job. Without --checkpoint: continue from the newest valid cycle checkpoint (F047) — a pending stop request is consumed first, worktree drift refuses, the plan-approval gate (approving the job's tasks) still applies. With --checkpoint <id>: resume from that safe event-replay checkpoint.
      remedy job apply — Review and apply job workspace changes to target repo, under its mission. Preview by default; --approve applies.
      remedy change proof — Show proof chain — why changes happened and verification status.
      remedy job evidence — Export a self-contained evidence bundle for an entire job (under its mission).
      remedy patch hunks — Show the hunks of a job's diff, or of one of its tasks, with their ids and the answer recorded for them.
      remedy patch approve-hunks — Record a hunk-level approve-or-reject answer over one of a job's tasks.
      remedy patch approve — Approve a patch intent for application.
      remedy patch reject — Reject a patch intent.
      remedy mission abandon — Mark a mission abandoned — the goal is dropped; its jobs and their run evidence stay.
      remedy client interface — Show what a program that drives Remedy can rely on: its commands, arguments, exit codes, state words, templates and budget kinds (read-only).
    Job states: pending, planned, running, paused, completed, failed, cancelled, blocked, stopped
    Mission statuses: active, paused, achieved, abandoned
    Contract templates: api-service, cli-tool, python-library, website
    Budget kinds: max_total_tokens, max_provider_calls, max_wall_clock_minutes, max_cost_usd, deadline, min_free_disk_bytes
    Exit codes: 0 ok, 1 failed, 2 usage, 3 not_ready, 4 environment
    A program reads the whole interface with: remedy client interface --json
    ```
    First line reads `Machine client interface 1.1`, matching the block.
11. **Gate 7** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` → `.agent/authored/f298-r2.md`: 131 lines, byte-equal (`True`), sha256
  `b7456bd6a12dd3a04cb826d54bf1e41fc576db0404a4e5da356249392011f74b`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal (`True`).
- base `.agent/live_review.md` blob at `0deb416e6` + `append-live_review.txt` →
  `.agent/live_review.md`: byte-equal (`True`).
- base `.agent/decisions.md` blob at `0deb416e6` + `append-decisions.txt` → `.agent/decisions.md`:
  byte-equal (`True`).
- base `.agent/prose_slips.md` blob at `0deb416e6` + `append-prose_slips.txt` →
  `.agent/prose_slips.md`: byte-equal (`True`).
- `dry-client_interface.py` → `apps/cli/client_interface.py`: byte-equal (`True`).
- `dry-client_cmd.py` → `apps/cli/commands/client_cmd.py`: byte-equal (`True`).
- `dry-commands_init.py` → `apps/cli/commands/__init__.py`: byte-equal (`True`).
- `dry-command_catalog.py` → `apps/cli/command_catalog.py`: byte-equal (`True`).
- `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: byte-equal (`True`).
- `dry-test_cli_ux.py` → `tests/cli/test_cli_ux.py`: byte-equal (`True`).
- `dry-import_reachability_allowlist.txt` →
  `tests/orchestration/import_reachability_allowlist.txt`: byte-equal (`True`).
- `dry-machine-client-contract-v1.md` → `docs/system/machine-client-contract-v1.md`: byte-equal
  (`True`).
- `dry-docs_README.md` → `docs/README.md`: byte-equal (`True`).

## Deviations & assumptions

None: C1, C2 and C3 follow the block's order with its subjects, with no file written outside the
named paths. No `cd`, nothing written under `/tmp`, no `-n`, no `REMEDY_TEST_MAX_WORKERS`; Gate 2
was the round's one test selection, run exactly once, with its exit code captured inside the
script that ran it. No mutation and no full suite were run (the reviewer ran them, per the
block). Every numstat the block named was checked before its commit and matched exactly.

## For the operator, in plain sentences

Remedy now has a command, `remedy client interface`, that prints what a program such as Luna's
runner can rely on when it drives Remedy — the commands it may use with their options and the
exit codes each can end with, what each exit code means, the possible states of a job and of a
mission, the templates a mission's acceptance criteria can start from, and the kinds of spending
limit; every part of it is read from Remedy's own code when the command runs, so it cannot fall
behind the code; the word "contract" is not used for it, because in Remedy that word means a
mission's acceptance criteria and nothing else; the answers of the commands, the refusal words
and the documentation page will be added to it in the next rounds.

## Round verdicts

Round 1's PASS is booked by this round's C1, in `.agent/live_review.md`. Round 2's verdict is the
reviewer's to give and book in the next round's first commit.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 2's verdict in the next round's first commit.
5. Then T001, next part: the answer and digest keys and the refusal tokens, held to the real
   commands.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 1, two prose slips, DECISION F298 D2, the plan | done | `e22496735` |
| C2: the machine client interface and `remedy client interface` | done | `29d8a9f70` |
| C3: the machine client page and the docs index | done | `b9ea95f29` |
| C4: handback | done | this commit |
| Gates 1 to 6 | done | all green, see Verification |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 7 | pending | reported in the worker's final reply |
