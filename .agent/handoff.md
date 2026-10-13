# Handback — F306 round 5: book round 4, then T007 (ExecutionConfig and its two serializers out of `pingpong_job.py`)

## Session

SESSION 1 of feature F306 · round 5 · rounds so far 5

Context self-assessment: this round was a clean mechanical move — all three named candidates
(`ExecutionConfig`, `_export_execution_config`, `_import_execution_config`) had no external
dependency on `pingpong_job` and no test replacing any of them there, so the move went through on
the first attempt with no stop condition triggered and no amendment needed.

Fortschritt: ~65 % (T001 to T004, T006 and T007 landed · T005 carried · T008 open) — Schätzung

## Range

Review of `5491194ae`..`d0d1d655e`

## Commits

### 54afe3ee4 F306 R5 C1: book round 4 and the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r5.md` | +114/-0 | NEW FILE, byte copy of `block.md` (114 lines, sha256 `6275d58eee96767adc2ed30d808a7c12198cb32e3edea4682df05dc968ff2155`) |
| `.agent/live_review.md` | +2/-0 | round 4's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/plan.md` | +7/-8 | replaced by `dry-plan.md` |

### d0d1d655e F306 R5 C2: ExecutionConfig and its two serializers move to a module of their own (R-1235, T007)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/execution_config.py` | +143/-0 | NEW FILE: `ExecutionConfig`, `_export_execution_config`, `_import_execution_config`, every body byte-for-byte, plus a one-paragraph module docstring and the two imports (`dataclass`, `Any`) they need |
| `packages/orchestration/pingpong_job.py` | +5/-133 | the moved class and two functions removed; one import block brings the three names back by name (all three still have a live caller inside this module, so no `name as name` alias is needed) |
| `tests/cli/test_client_interface.py` | +2/-1 | the one assertion in `test_the_job_run_answer_trees_name_exactly_what_their_code_builds` that reads `_export_execution_config`'s returned keys now reads `packages/orchestration/execution_config.py` instead of `pingpong_job.py`; nothing else in the file changed |
| `docs/system/structure-ledger-v1.md` | +3/-2 | `pingpong_job.py` row 5626→5498; the ledger bullet gains its Step (1) sentence, naming the new module |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 74018→73890 (same 128-line fall) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.execution_config` added in its sorted place (the guard asked for it: the new module is reachable through `pingpong_job.py`) |

### (this commit) F306 R5 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8` — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block does not ask for one.
- No worktree added or removed. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` read `[]` — no open PR, no Open PR Gate action needed. No `gh pr merge` or `gh pr edit`.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read `feature/f306-findings-paydown-v8`; `git rev-parse HEAD` read `5491194aee1ab3fe3872343ffb39a385d98b08a4`; `git status --porcelain` was clean.

Every prepared-file digest matched before use: `block.md` (`6275d58eee96767adc2ed30d808a7c12198cb32e3edea4682df05dc968ff2155`, 114 lines), `append-live_review.txt` (`080e0488334ed915f982b763a0cca882670e7ca90457899b2d4bb905ee02ac0f`), `dry-plan.md` (`ce20d07c39ca382a332fdc959844edc63fdad41615bf95a6fd8bd939c16b574a`), `verify.py` (`355678d7e6625e717df8c9cf6b3669905034c38ffd4545b15f2b90e78bb24767`), `run_selection.py` (`cddebcc9b29665c95a90fb1b93184e421e0348d110823ea328a6ff2b003d712e`), `selection.txt` (`4c3264118df6aad565fe58cefdca8b32195be604324cba976ece142ada363ece`), `check_reexport.py` (`128071ec6b8f8a8520e39fcaefe3fa09697ced195cba3fe1c39df0bbd9ad8cc9`).

C1: before commit, `git diff --cached --numstat` read exactly `114 0 .agent/authored/f306-r5.md`, `2 0 .agent/live_review.md`, `7 8 .agent/plan.md` — matching the block's specification exactly. `cmp` of the authored copy against `block.md` printed nothing.

C2: before commit, `git diff --cached --stat` read `6 files changed, 155 insertions(+), 137 deletions(-)`, under the 500-insertion cap. Self-review ran over `git diff --cached` before the commit: the `pingpong_job.py` diff showed only the planned class/function removal plus the one import block added; the new module's diff showed only the moved bodies, a docstring and the two stdlib imports (`dataclass`, `Any`) they need; no unrelated line moved. Searched `tests/` in every spelling (`ExecutionConfig`, `_export_execution_config`, `_import_execution_config`) beforehand: every reference imports from or reads `pingpong_job`, none replaces any of the three there. `python3 -m ruff check` on the four named files passed on the first try, no `--fix` round needed. `tests/test_structure_ratchet.py` and `tests/orchestration/test_import_reachability.py` run directly beforehand: the reachability test red once (the new module unlisted), green after the allowlist line was added; 8 passed after. `tests/cli/test_client_interface.py` run directly beforehand: 77 passed. No leftover process after any run.

**Gate run (against C2, the only one — no amendment needed):**
- Gate 1: `git status --porcelain` empty; `verify.py` →
  ```
  found True F306 R5 C1: 54afe3ee4877755c4d9a7850e943feffb1eef668
  C1 parent is the base True
  equal at F306 R5 C1: True .agent/live_review.md
  equal at F306 R5 C1: True .agent/plan.md
  equal at F306 R5 C1: True .agent/authored/f306-r5.md
  F306 R5 C1: names exactly its paths True []
  ALL True
  ```
- Gate 2: `python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/execution_config.py tests/cli/test_client_interface.py tests/test_structure_ratchet.py` → `All checks passed!`.
- Gate 3: `run_selection.py` → exit 0:
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  88 paths
  4349 passed, 3 skipped in 70.95s (0:01:10)
  exit 0
  ```
  No FAILED/ERROR line, no "process(es) behind" line.
- Gate 4: `python3 -m apps.cli.main integrity check --json` → exit 0:
  ```
  {"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
  ```
- Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → `['R-1235', 'R-1246', 'R-1252']`.
- Gate 6: `check_reexport.py` →
  ```
  defined in execution_config: 3 ['ExecutionConfig', '_export_execution_config', '_import_execution_config']
  re-exported as the same object: True []
  execution_config imports pingpong_job: False
  holds the three names: True
  ALL True
  ```

## Authored-text proofs

- `.agent/authored/f306-r5.md` against `block.md`: byte-equal, 114 lines, sha256 `6275d58eee96767adc2ed30d808a7c12198cb32e3edea4682df05dc968ff2155` (`cmp` printed nothing; Gate 1's "equal at F306 R5 C1 True .agent/authored/f306-r5.md").
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).

No other reviewer-authored text applied this round: C2 is this session's own code (a structural move the block ordered), proved by the gates above and by the unchanged test suite rather than by digest comparison to a prepared file.

## Deviations & assumptions

None. All three named candidates moved cleanly: none is called from elsewhere in `pingpong_job.py`
only by name without being itself a mover (in fact all three keep a live caller inside
`pingpong_job.py`, so the back-import uses the same plain grouped form the last two rounds used for
their own still-called names, not the `name as name` re-export-only alias), the new module imports
nothing from `pingpong_job`, and no test replaces any of the three on `pingpong_job` directly — every
test reference reads `ExecutionConfig`/`_export_execution_config`/`_import_execution_config` from
`pingpong_job` by plain import, which the re-export keeps working. No extra commit beyond C1, C2,
C3; no dropped one; no reordering. Every commit carries `Co-Authored-By: Claude Sonnet 5
<noreply@anthropic.com>` — the model this session actually runs on.

## For the operator, in plain sentences

This round first recorded the previous round's acceptance and moved the working plan forward. It
then took the second step a finding's own text asks for on the job runner's own file: the durable
execution settings a job carries, along with the two small functions that turn them into plain data
and back, moved into a module of their own, with every existing caller still finding them under
their old name. One pointer inside a naming test that used to look at the old file now looks at the
new one, since that is the exact finding this step closes. Every check this round ran — the
structure-size rule, the import-reachability guard, the full test selection, the health check and
the re-export guard — passed, with one guard needing one small addition (a new module's name added
to an allowlist) before it went green. One more step of this same repair remains open for a later
session, plus two older problems still carried forward by name. Nothing waits on the operator right
now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate.
3. Book round 5's verdict in the next round's first commit.
4. T008: R-1235's third step.

Operator questions open: 0.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `54afe3ee4` |
| C2 | done | `d0d1d655e` |
| C3 | done | this commit |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `4349 passed, 3 skipped`, 88 paths, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | passed | six checks pass, `fail_count` 0 |
| Gate 5 | passed | `['R-1235', 'R-1246', 'R-1252']` |
| Gate 6 | passed | `ALL True` |
| Push | pending at write time | runs after this commit; result in the session's final reply |
