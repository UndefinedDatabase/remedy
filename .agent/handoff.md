# Handoff — F254 R5 (R4 findings persisted, dead-model warning in `doctor core`)
Feature T2_F254 · Round R5 · SPLIT · branch `feature/f254-model-alias-table`.
Length: 131 lines, 71 over the 60 target (measured with `wc -l`, not estimated). Cause: the
mandated tables (changed files, pair counts under two shapes, 14-row verification table,
item status) plus the doctor output this block required VERBATIM. No section dropped. This
overage IS finding R-0214; the measurement is reported, not trimmed away, as asked.

## Commits (range 2504a560..HEAD)
- `fd601931` docs(f254): persist the R4 verdict, finding R-0214 and decisions D12 and D13
  — `.agent/` paths ONLY, 410 lines, precedes all code. Pushed with commit 2.
- `885c64f0` feat(f254): warn in doctor core when a model id is on the dead list
  — 289 lines, under the 500 limit. `git push` exit 0 (2504a560..885c64f0).
- commit 3 `chore(f254): rewrite handoff for the R5 handback` — SHA self-referential
  (this file is its only content); it is the branch tip at handback. Declared, not guessed.

## Changed files — GENERATED from `git diff --numstat 2504a560..HEAD` (R-0210, not retyped)
| File | + | - |
|---|---|---|
| .agent/authored/f254-r5-1.md | 163 | 0 |
| .agent/authored/f254-r5-2.md | 69 | 0 |
| .agent/authored/f254-r5-3.md | 23 | 0 |
| .agent/candidates.md | 14 | 3 |
| .agent/live_review.md | 100 | 10 |
| .agent/plan.md | 14 | 14 |
| apps/cli/commands/worker_facade_cmd.py | 109 | 0 |
| tests/cli/test_worker_facade_cmd.py | 180 | 0 |
(Row 8 is 180 not 176: a four-quote docstring opener in one new test was rewritten to a
normal one during self-review, before commit 2. No behaviour change.)

## Transport proofs — PRIMARY
`cp` from the reviewer's scratchpad, never retyped. All three `cmp` against the original: exit 0.
| Receipt | cmp | sha256 |
|---|---|---|
| f254-r5-1.md | 0 | f6d134c86eb3d61c79019b32484c17cd11d8890f1bda54b2ae8c076a41d4df62 |
| f254-r5-2.md | 0 | 89e49c907285969ac4b376c16f94fec8e147d9f9aa2cd1e365d88c583cdc38e4 |
| f254-r5-3.md | 0 | dad4bc73d25213ae16b000f4362237250988860b864179b512e3771d033e5270 |
`cp .agent/authored/f254-r5-3.md .agent/candidates.md` then `cmp` → exit 0 (full-file copy).

## Pair counts — reported UNDER EACH PAIR'S OWN SHAPE
f254-r5-1 → .agent/live_review.md (4 pairs). Every FROM verified 1x BEFORE any edit.
| Pair | Shape | FROM before | FROM after | TO after | TO-ONLY after |
|---|---|---|---|---|---|
| 1 | REWRITE | 1x | 0x | 1x | n/a |
| 2 | REWRITE | 1x | 0x | 1x | n/a |
| 3 | APPEND | 1x | 1x (by construction) | 1x | 1x |
| 4 | REWRITE | 1x | 0x | 1x | n/a |
f254-r5-2 → .agent/plan.md (3 pairs), all REWRITE: FROM 1x before, 0x after, TO 1x after.
Structure after: live_review.md has `## Steps`/`## Findings`/`## Decisions`/`## Verdicts`
1x each; plan.md has `## Goal` + `## Next Steps` 1x each and is 46 lines (<50).

## `remedy doctor core` — real run against the real repo, both forms, exit 0
`--json`: `ready` = **true**, `blockers` = **[]**, `warnings` = 2 entries, both
`dead_builtin_model`, with the same detail strings shown verbatim below. New check
`dead_model_list` = ok true, detail "2 shipped + 0 configured dead ids". Plain form:
```
Core Product Spine: READY
  [OK] worker_facade: COMMAND_HANDLERS available
  [OK] command_catalog: 325 commands, 57 groups
  [OK] run_contract: ContractAction available
  [OK] mission_facade: run_mission_loop available
  [OK] self_repair_proposal: list_self_repair_proposals available
  [OK] review_bundle: build_review_bundle available
  [OK] config: get_config available
  [OK] approval_policy: evaluate_execution_approval_policy available
  [OK] fast_test_lane: scripts/remedy_test_fast.sh
  [OK] full_test_lane: scripts/remedy_test_full.sh
  [OK] dead_model_list: 2 shipped + 0 configured dead ids
  warnings (advisory — these do not affect READY):
  [WARN] dead_builtin_model: claude-opus-4-20250514 is a BUILT-IN default, reached through alias claude-flagship in packages/orchestration/model_aliases.py. Fix: repoint alias claude-flagship to a live id. Remedy calls this id dead only because the shipped list scripts/dead_models.json says so — that list is operator-maintained data, no provider was queried, so the verdict is exactly as current as the data. Recorded reason: A May-2025 dated id, and the built-in default behind the claude-flagship alias in packages/orchestration/model_aliases.py. docs/roadmap/features/T2_F254.md ('How it fits') records it as several generations stale as of Aug 2026. No replacement id is named here because nothing in this repository states one: choosing the successor is F232's job (the model upgrade playbook). No replacement id is recorded.
  [WARN] dead_builtin_model: claude-sonnet-4-20250514 is a BUILT-IN default, reached through alias claude-workhorse in packages/orchestration/model_aliases.py. Fix: repoint alias claude-workhorse to a live id. Remedy calls this id dead only because the shipped list scripts/dead_models.json says so — that list is operator-maintained data, no provider was queried, so the verdict is exactly as current as the data. Recorded reason: A May-2025 dated id, and the built-in default behind the claude-workhorse alias in packages/orchestration/model_aliases.py. docs/roadmap/features/T2_F254.md ('How it fits') records it as several generations stale as of Aug 2026. No replacement id is named here because nothing in this repository states one: choosing the successor is F232's job (the model upgrade playbook). No replacement id is recorded.
```
This matches the block's expectation (two shipped dead ids warn, `ready` stays true). No
config warning fires: `ollama.model` resolves to `qwen3-coder-next` and `orchestrator.model`
to None, neither of which is on the list.

## Verification — real runs, real exit codes, nothing adjusted to match
| Command | Result | Exit |
|---|---|---|
| pytest tests/cli/test_worker_facade_cmd.py -q | 59 passed | 0 |
| pytest tests/cli/test_product_spine.py -q | 72 passed | 0 |
| pytest tests/cli/test_command_catalog.py -q | 23 passed | 0 |
| pytest tests/orchestration/test_development_artifact_boundary.py -q | 18 passed | 0 |
| pytest tests/orchestration/test_dead_model_list.py -q | 23 passed | 0 |
| pytest tests/orchestration/test_model_aliases.py -q | 21 passed | 0 |
| pytest tests/cli/test_cli_ux.py -q | 57 passed | 0 |
| pytest tests/ui_server/test_dashboard_contract.py -q | 70 passed | 0 |
| pytest tests/orchestration/test_test_runner.py -q | 51 passed | 0 |
| pytest tests/regression/test_resource_safety.py -q | 21 passed | 0 |
| pytest tests/cli/test_golden_path.py -q | 42 passed | 0 |
| ruff check apps/cli/commands/worker_facade_cmd.py | All checks passed | 0 |
| ruff check tests/cli/test_worker_facade_cmd.py | All checks passed | 0 |
| git status --porcelain (at handback, before commit 3) | empty | 0 |

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts persisted first | done | commit fd601931, `.agent/` paths only |
| B doctor check | done | hard check + warnings, `ready`/`blockers` untouched |
| C tests | done | 10 new tests in the existing file, +10 → 59 |
| D commit / push / handoff | done | 2 pushed; commit 3 is this file |

## Deviations, assumptions, observations
1. RED GATE HIT AND FIXED BEFORE COMMIT 2 — report this to the reviewer as a real event:
   `test_development_artifact_boundary.py` failed 3/18 on first run because my `_warn`
   docstring cited `.agent/live_review.md`, and `worker_facade_cmd` is in that test's
   `_PRODUCT_MODULES` list (shipped code must not name a development artifact). Fixed by
   citing `docs/roadmap/features/T2_F254.md` instead. No test assertion was edited.
2. No existing doctor test went red from the new `warnings` key — the suite does not pin
   the exact key set, so the STOP clause in the step block was never triggered.
3. ASSUMPTION (not mandated): a `.model` key sitting at its built-in default that is dead
   would produce BOTH a `dead_builtin_model` and a `dead_configured_model` warning. Both
   statements are true about distinct origins, and the block asked for every `.model` key
   read through the normal accessor with no source filter, so no `ConfigSource` filtering
   was added. Today no such overlap exists.
4. ASSUMPTION (not mandated): if the comparison itself fails (config or alias table
   unreadable) a `dead_model_comparison` WARNING is emitted rather than crashing the
   doctor or skipping silently — non-silent, and still never touches `ready`.
5. OBSERVATION: each warning embeds the entry's full `reason` verbatim, so a detail runs
   ~700 characters. Fine in JSON, a wall in the text form. Flagged for the reviewer's
   judgement; nothing was truncated, because truncation would drop the provenance clause.
6. Scope held: only the nine instructed paths changed. No `docs/`, `scripts/`, `packages/`
   or `.claude/` edit; no catalog, flag or subcommand added. No worktree, no force-push,
   no PR, `main` untouched.

## Findings & next action
Open findings: 0. R-0214 registered and closed in the same commit (filed as a candidate);
next free ID R-0215. `.agent/candidates.md` now holds 1 entry — a block condition at the
next feature claim, by design (DECISION D12).
Next expected action: reviewer reads `git diff 2504a560..HEAD` bottom-up, re-runs the 11
suites, `ruff` and both `remedy doctor core` forms, and issues the R5 verdict. R6 is the
repo-scan test plus the `docs/` write-up the alias module and dead-model list owe.
