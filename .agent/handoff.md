# Handback — F306 round 6: book round 5, then `run_job`'s configuration resolution becomes a function of its own

## Session

SESSION 2 of feature F306 · round 6 · rounds so far 6

Context self-assessment: this round cut the resolution block out of a 1559-line function with a
fixed reference to check equivalence against, so the move went through on the first attempt with
no stop condition triggered and the only departure from the block's literal wording was a lint-
driven import-statement split, explained below.

Fortschritt: ~75 % (T001 to T004, T006, T007 and run_job's step (2) landed · T005 carried · T008
open) — Schätzung

## Range

Review of `baf42eea2`..`b9ca27564`

## Commits

### 47d0f091c F306 R6 C1: book round 5 and the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r6.md` | +136/-0 | NEW FILE, byte copy of `block.md` (136 lines, sha256 `eeb5b5d1f36e2f0e77d62f591a49206dba4c7fc18838733878997904d53efe41`) |
| `.agent/live_review.md` | +2/-0 | round 5's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/plan.md` | +8/-7 | replaced by `dry-plan.md` |

### b9ca27564 F306 R6 C2: run_job's configuration resolution becomes a function of its own (structure step, T008 prerequisite)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/execution_config.py` | +164/-4 | `default_role_provider_name`, `_resolve_cfg` moved in verbatim with their WHY comment; new `_resolve_invocation_controls` (the F3 comment, nested `_resolve_inv`, its five calls) and new public `resolve_job_execution_config`, which `run_job` used to compute inline; module docstring widened to name all six exports |
| `packages/orchestration/pingpong_job.py` | +42/-141 | the two moved functions deleted; `run_job`'s inline resolution block (`ec = job.execution_config` through the `ExecutionConfig(...)` construction) replaced by one call to `resolve_job_execution_config` plus a rebind of the 14 locals `run_job` reads later, read from the returned record; three names imported back, two of them (`_resolve_cfg`, `default_role_provider_name`) via `name as name` because, unlike round 5's three names, neither has a live caller left inside this module |
| `docs/system/structure-ledger-v1.md` | +8/-6 | `run_job` row 1559→1486, its bullet's step (2) sentence; `pingpong_job.py` file row 5498→5399 |
| `tests/test_structure_ratchet.py` | +2/-2 | `MAX_FUNCTION_LINES` 30731→30658 (same 73); `MAX_FILE_LINES` 73890→73791 (same 99) |

### (this commit) F306 R6 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` read `[]` — no open PR,
  no Open PR Gate action needed.
- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8`
  — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block does not ask for one. No worktree added or removed. No `gh pr merge` or
  `gh pr edit`.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read
`feature/f306-findings-paydown-v8`; `git rev-parse HEAD` read
`baf42eea221a600ca38b73759ee4569fb0d92e60`; `git status --porcelain` was clean.

Every prepared-file digest matched before use (all seven files in the prep directory): `block.md`
(`eeb5b5d1f36e2f0e77d62f591a49206dba4c7fc18838733878997904d53efe41`, 136 lines),
`append-live_review.txt` (`9841d51aaf12af6c7709babfc093cc5eb503cadfcc45410b50cc0aa7db92fd8b`),
`dry-plan.md` (`8565c019fb8350a0dcb4db0fd625c4241fb537a92aad301b3a21392eb2bd6524`), `verify.py`
(`1f7dfcdc73baa82ca1f3a1233d9317547b1429c1043e635e62fd4622834c1d45`), `run_selection.py`
(`cddebcc9b29665c95a90fb1b93184e421e0348d110823ea328a6ff2b003d712e`), `selection.txt`
(`c5d9aea7c44efaec34c9703656d3707cfb4eabf2b032fd73d9319fdc60203022`), `check_extract.py`
(`158225a8a8880ef621509b139a154ddeb2fc520c6caf4008ecdc2fdf1f48cf4b`).

C1: before commit, `git diff --cached --numstat` read exactly `136 0
.agent/authored/f306-r6.md`, `2 0 .agent/live_review.md`, `8 7 .agent/plan.md` — matching the
block's specification exactly (`2 0` for the ledger, `8 7` for the plan, the block file at its
`wc -l` of 136). `cmp` of the authored copy against `block.md` printed nothing.

C2: before commit, `git diff --cached --stat` read `4 files changed, 216 insertions(+), 153
deletions(-)`, under the 500-insertion cap. Self-review ran over `git diff --cached` before the
commit: the `pingpong_job.py` diff showed only the planned block removal/replacement and the
import-statement change; the new module's diff showed only the moved bodies plus the two new
functions, byte-for-byte on the moved parts. Searched `run_job`'s own source (lines 2457–3942 by
`ast`) for every local the moved block used to bind (`ec`, `builder_src`, `bm_src`, `be_src`,
`rm_src`, `re_src`, `rp_src`, `rpm_src`, `rpe_src`, `test_cmd_src`, `write_mode_src`,
`max_rounds_src`, `_ts`, `_tp`, `_moc`, `_se`, `_mt`, their `_src` pairs, `_resolve_inv`,
`builder_effort`, `reviewer_effort`, `repair_provider_name`, `repair_model`, `repair_effort`):
none is read after the replaced block except as the call's own keyword arguments — confirming the
block's claim that only the named 14 locals are read later. `python3 -m ruff check` on the four
changed Python/text files found two `F401` (unused-import) errors on first run —
`_resolve_cfg` and `default_role_provider_name` plain-imported but never called inside
`pingpong_job.py` any more — fixed by switching those two imports to the `name as name`
self-re-export idiom this codebase already uses for re-export-only names (e.g.
`run_manifest.py`'s imports from `job_input_definition.py` and `workspace_identity.py`); ruff's own
`--fix` then split them into their own import statements, matching that precedent exactly. Second
run: `All checks passed!`. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f306-r6/prep/check_extract.py`
run directly beforehand, after the fix: `ALL True`, including the 2006-combination equivalence
check against the reference function built from the pre-round block. `tests/test_structure_ratchet.py`
run directly beforehand: 5 passed. No leftover process after any run.

**Gate run (against C2, the only one — no amendment needed):**
- Gate 1: `git status --porcelain` empty; `verify.py` →
  ```
  found True F306 R6 C1: 47d0f091ce02b46fd50521103483a34f122446b7
  C1 parent is the base True
  equal at F306 R6 C1: True .agent/live_review.md
  equal at F306 R6 C1: True .agent/plan.md
  equal at F306 R6 C1: True .agent/authored/f306-r6.md
  F306 R6 C1: names exactly its paths True []
  ALL True
  ```
- Gate 2: `python3 -m ruff check packages/orchestration/pingpong_job.py packages/orchestration/execution_config.py tests/test_structure_ratchet.py` → `All checks passed!`.
- Gate 3: `run_selection.py` → exit 0:
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  107 paths
  5132 passed, 3 skipped in 109.36s (0:01:49)
  exit 0
  ```
  No FAILED/ERROR line, no "process(es) behind" line.
- Gate 4: `python3 -m apps.cli.main integrity check --json` → exit 0:
  ```
  {"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
  ```
- Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → `['R-1235', 'R-1246', 'R-1252']`.
- Gate 6: `check_extract.py` →
  ```
  default_role_provider_name defined in execution_config True
  default_role_provider_name re-exported as the same object True
  _resolve_cfg defined in execution_config True
  _resolve_cfg re-exported as the same object True
  resolve_job_execution_config defined in execution_config True
  resolve_job_execution_config re-exported as the same object True
  execution_config imports no pingpong_job True
  run_job no longer spells _resolve_cfg( True
  run_job no longer spells ExecutionConfig( True
  run_job no longer spells _resolve_inv True
  run_job no longer spells default_role_provider_name( True
  run_job calls resolve_job_execution_config True
  resolve_job_execution_config equals the old block on 2006 combinations True
  ALL True
  ```

## Authored-text proofs

- `.agent/authored/f306-r6.md` against `block.md`: byte-equal, 136 lines, sha256
  `eeb5b5d1f36e2f0e77d62f591a49206dba4c7fc18838733878997904d53efe41` (`cmp` printed nothing; Gate
  1's "equal at F306 R6 C1 True .agent/authored/f306-r6.md").
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).

No other reviewer-authored text applied this round: C2 is this session's own code (a structural
move the block ordered), proved by the gates above, by the unchanged test suite, and by
`check_extract.py`'s 2006-combination equivalence check against the reference function built from
the exact pre-round block, rather than by digest comparison to a prepared file.

## Deviations & assumptions

One deviation from the block's literal wording, in C2 only: the block asked that
`default_role_provider_name` and `_resolve_cfg` be imported back "in the existing
`from packages.orchestration.execution_config import (...)` statement." Added there as plain
names, `python3 -m ruff check` failed both with `F401` (imported but unused), because — unlike
round 5's three names, which all still had a live caller inside `pingpong_job.py` — neither
function is called anywhere in `pingpong_job.py` any more; `run_job` now calls
`resolve_job_execution_config` instead. Fixed by the `name as name` self-re-export idiom this
codebase already uses for exactly this situation (`run_manifest.py`'s imports of
`_h`, `_redacted_command_identity`, `_source_field`, `job_input_sha256` from
`job_input_definition.py`, and `_run_probe` from `workspace_identity.py`); ruff's own `--fix` then
split the two aliased imports into their own statements, which is the same shape that precedent
takes. The net effect — both names re-exported as the same objects, `pingpong_job.<name>` still
resolving — is unchanged; only the statement's grouping differs from the block's literal text, to
keep Gate 2 green. No extra commit beyond C1, C2, C3; no dropped one; no reordering. Every commit
carries `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` — the model this session actually
runs on.

## For the operator, in plain sentences

This round first recorded the previous round's acceptance and moved the working plan forward. It
then took the next step a finding's own text asks for on the job runner's own file: the long block
that worked out which setting value to use — an explicit one passed in, a previously saved one, or
a plain default — moved out of the huge function that runs a job and became a function of its own,
callable and checkable on its own terms. The function that runs a job now calls that new function
once and then reads back the fourteen answers it needs, so it behaves exactly as before. A machine
check compared the new function's answer against the old block's answer over thousands of
combinations of settings and found no difference. One small departure from the letter of this
round's instructions was needed to keep an automatic code-quality check satisfied, with no change
in what runs; it is written down above. One more step of this same repair remains open for a later
session, plus two older problems still carried forward by name. Nothing waits on the operator right
now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate.
3. Book round 6's verdict in the next round's first commit.
4. T008: R-1235's third step.

Operator questions open: 0.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `47d0f091c` |
| C2 | done | `b9ca27564` |
| C3 | done | this commit |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | `All checks passed!` (after one ruff-driven import-statement fix) |
| Gate 3 | passed | exit 0, `5132 passed, 3 skipped`, 107 paths, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | passed | six checks pass, `fail_count` 0 |
| Gate 5 | passed | `['R-1235', 'R-1246', 'R-1252']` |
| Gate 6 | passed | `ALL True`, including the 2006-combination equivalence check |
| Push | pending at write time | runs after this commit; result in the session's final reply |
