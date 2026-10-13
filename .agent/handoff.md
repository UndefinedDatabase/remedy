# Handback — F306 round 4: book round 3 and DECISION F306 D2, then T006 (the job-input definition's first step out of `run_manifest.py`)

## Session

SESSION 1 of feature F306 · round 4 · rounds so far 4

Context self-assessment: C1 was mechanical bookkeeping (prepared-bytes copies, verified digest by
digest). C2 required working out, per the block's own stay/move rule, which of the sixteen named
candidates could actually move: the constants, `_h`, `_redacted_command_identity`,
`build_job_input_definition` and the three byte/hash helpers moved cleanly, but
`validate_job_input_definition` calls `_is_hex64`, `_safe_component`, `VALID_ISOLATION_MODES`,
`_contains_secret` and `_contains_local_path` — shared helpers every other validator on
`run_manifest.py` uses too, two of them replaced directly on that module by name in three test
files — so it had to stay, and `decode_job_input_definition_v1` had to stay with it, since its only
call is to `validate_job_input_definition`. This reading departs from the block's Step 4 text, which
assumed both would move; Step 4's own trailing clause ("name what stayed if anything did") is the
escape hatch this round uses. Every gate passed clean on the first run with no amendment needed.

Fortschritt: ~55 % (T001 to T004 and T006 landed · T005 carried · T007 and T008 open) — Schätzung

## Range

Review of `9b56e0825`..`f778c4a09`

## Commits

### 14512f90f F306 R4 C1: book round 3, DECISION F306 D2, the slice list and the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r4.md` | +122/-0 | NEW FILE, byte copy of `block.md` (122 lines, sha256 `ac1dcd5ffc1d58fd4fe36a9aaee14df085e19e7fa875bc0691c54097b587f5e8`) |
| `.agent/live_review.md` | +2/-0 | round 3's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/decisions.md` | +12/-0 | DECISION F306 D2 appended, byte-identical to `append-decisions.txt` |
| `.agent/plan.md` | +10/-10 | replaced by `dry-plan.md` |
| `docs/roadmap/features/T2_F306.md` | +6/-4 | replaced by `dry-T2_F306.md` (T005 withdrawn, R-1235's step text updated) |

### f778c4a09 F306 R4 C2: the job-input definition, its field sets and its builder move to a module of their own (R-1235, T006)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_input_definition.py` | +167/-0 | NEW FILE: `_SECRET_TERMS`, `is_secret_key`, `_safe_scalar` (Redaction-section dependencies), `_h`, `_redacted_command_identity`, `build_job_input_definition`, `job_input_definition_bytes`, `job_input_definition_sha256`, `job_input_sha256`, and the field-set constants `JOB_INPUT_TOP_FIELDS`/`JOB_INPUT_TASK_FIELDS`/`JOB_INPUT_EXECUTION_STR_FIELDS`/`JOB_INPUT_EXECUTION_INT_FIELDS`/`JOB_INPUT_EXECUTION_BOOL_FIELDS`/`_JOB_INPUT_SOURCE_OF`/`_source_field`/`JOB_INPUT_EXECUTION_FIELDS` — every body byte-for-byte |
| `packages/orchestration/run_manifest.py` | +25/-148 | the moved bodies removed; one import block re-exports every moved name (`_h`, `_redacted_command_identity`, `_source_field` and `job_input_sha256` each on their own `name as name` statement, the only four ruff's unused-import rule needs the alias for, since nothing left in `run_manifest.py` still calls them directly); `validate_job_input_definition` and `decode_job_input_definition_v1` stay (see Deviations) |
| `docs/system/structure-ledger-v1.md` | +8/-2 | `run_manifest.py` row 6398→6275; the ledger bullet gains its Step (2) sentence, naming what moved and what stayed |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 74141→74018 (same 123-line fall) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.job_input_definition` added in its sorted place |

### (this commit) F306 R4 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8` — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block does not ask for one.
- No worktree added or removed. No `gh pr merge` or `gh pr edit`. No Open PR Gate check was run this round because the block's preconditions named the exact branch/HEAD to confirm instead; `None` beyond the push.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read `feature/f306-findings-paydown-v8`; `git rev-parse HEAD` read `9b56e08255046f705e0b1ce60bd2af5b3fe8e228`; `git status --porcelain` was clean.

Every prepared-file digest matched before use (all eight, plus `block.md` itself, 122 lines): `block.md` (`ac1dcd5ffc1d58fd4fe36a9aaee14df085e19e7fa875bc0691c54097b587f5e8`), `append-live_review.txt` (`6565f72ae2fdae7f510ecab0f8a7d951f695a4969b834d87aee6457c1f1e00f3`), `append-decisions.txt` (`11f97b6b3989d3d0ec33efedfda2d6dd3f2fae63195c5943023401938b4b78c1`), `dry-plan.md` (`3097f67313b436fdab7f2f125f3a24ef3338b51824f02d2cf85265298561b75d`), `dry-T2_F306.md` (`e5876e3058320653aa658a957e73dda1d5f2df817843a5e945467aac426de2ec`), `verify.py` (`4e9edb2e00fde19f09678da8ce8d2f832c1f10f33065a91ca7de4d92e38f6377`), `run_selection.py` (`cddebcc9b29665c95a90fb1b93184e421e0348d110823ea328a6ff2b003d712e`), `selection.txt` (`4e7952dbe929d2111dbb6eca7a397f2b0e62ea61dab87695e867d83e6b9dd5c8`), `check_reexport.py` (`70510bfebf7bb92ee54dbe66b3a0ce042c1d35757e1a4794588c5e626ce2138e`).

C1: before commit, `git diff --numstat` (post-commit, read back) matched exactly `2 0 .agent/live_review.md`, `12 0 .agent/decisions.md`, `10 10 .agent/plan.md`, `6 4 docs/roadmap/features/T2_F306.md`, `122 0 .agent/authored/f306-r4.md` — matching the block's specification exactly. `cmp` of the authored copy against `block.md` printed nothing.

C2: before commit, `git diff --cached --stat` read `5 files changed, 202 insertions(+), 151 deletions(-)`, under the 500-insertion cap. Self-review ran over `git diff --cached` before the commit: the `run_manifest.py` diff showed only the planned removals and the import block; the new module's diff showed only the moved bodies plus a docstring and the two stdlib imports (`hashlib`, `json`) they need; no unrelated line moved. `python3 -m ruff check` on the three named files passed on the first try, no `--fix` round needed. `tests/test_structure_ratchet.py` and `tests/orchestration/test_import_reachability.py` run directly beforehand: 8 passed. `tests/orchestration/test_job_input_definition_schema.py`, `test_job_input_definition_completeness.py`, `test_episode_snapshot_full_validity.py` and `test_run_manifest_strict_boundaries.py` run directly beforehand: 163 passed. `test_run_manifest_security.py`, `test_review_subject_strict_schema.py`, `test_review_gate_sensitive_metadata.py`, `test_failure_postmortem.py`, `test_run_manifest_ledger_identity_safety.py` and `test_stream_evidence.py` (the files that monkeypatch `_contains_secret`/`_contains_local_path` on `run_manifest`, to confirm the stay decision kept their patch semantics correct) run directly beforehand: 309 passed. No leftover process after any run.

**Gate run (against C2, the only one — no amendment needed):**
- Gate 1: `git status --porcelain` empty; `verify.py` →
  ```
  found True F306 R4 C1: 14512f90fd891b3b0195ed79e6e4c7a6e79c62c8
  C1 parent is the base True
  equal at F306 R4 C1: True .agent/live_review.md
  equal at F306 R4 C1: True .agent/decisions.md
  equal at F306 R4 C1: True .agent/plan.md
  equal at F306 R4 C1: True docs/roadmap/features/T2_F306.md
  equal at F306 R4 C1: True .agent/authored/f306-r4.md
  F306 R4 C1: names exactly its paths True []
  ALL True
  ```
- Gate 2: `python3 -m ruff check packages/orchestration/run_manifest.py packages/orchestration/job_input_definition.py tests/test_structure_ratchet.py` → `All checks passed!`.
- Gate 3: `run_selection.py` → exit 0:
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  133 paths
  4640 passed, 3 skipped in 70.78s (0:01:10)
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
  functions and classes: 9 ['_h', '_redacted_command_identity', '_safe_scalar', '_source_field', 'build_job_input_definition', 'is_secret_key', 'job_input_definition_bytes', 'job_input_definition_sha256', 'job_input_sha256']
  constants: 6 ['JOB_INPUT_EXECUTION_BOOL_FIELDS', 'JOB_INPUT_EXECUTION_FIELDS', 'JOB_INPUT_EXECUTION_INT_FIELDS', 'JOB_INPUT_EXECUTION_STR_FIELDS', 'JOB_INPUT_TASK_FIELDS', 'JOB_INPUT_TOP_FIELDS']
  re-exported as the same object: True []
  job_input_definition imports run_manifest: False
  ALL True
  ```

## Authored-text proofs

- `.agent/authored/f306-r4.md` against `block.md`: byte-equal, 122 lines, sha256 `ac1dcd5ffc1d58fd4fe36a9aaee14df085e19e7fa875bc0691c54097b587f5e8` (`cmp` printed nothing; Gate 1's "equal at F306 R4 C1 True .agent/authored/f306-r4.md").
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/decisions.md` against the base plus `append-decisions.txt`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).
- `docs/roadmap/features/T2_F306.md` against `dry-T2_F306.md`: byte-equal (Gate 1).

No other reviewer-authored text applied this round: C2 is this session's own code (a structural move DECISION F306 D2 ordered), proved by the gates above and by the unchanged test suite rather than by digest comparison to a prepared file.

## Deviations & assumptions

- **The moved list is fourteen of sixteen named candidates, not sixteen — `validate_job_input_definition` and `decode_job_input_definition_v1` stay.** The block's Step 4 instruction read as if both would move (it ordered the ledger row of `validate_job_input_definition` renamed to the new file), but Step 2's own stay rule — "a candidate that calls a name staying in `run_manifest` stays" — applies here first. `validate_job_input_definition`'s body calls `_is_hex64`, `_safe_component`, `VALID_ISOLATION_MODES`, `_contains_secret` and `_contains_local_path`, none of which is a named candidate; all five are either used by other, unrelated validators on `run_manifest.py` (`validate_run_manifest`, `validate_call_ledgers`, `validate_input_snapshot`, `validate_call_identity`, `validate_prepared_call_input`, `_is_safe_key`, among others) or, for `_contains_secret`/`_contains_local_path` specifically, directly replaced by `monkeypatch.setattr(run_manifest, "_contains_secret"/"_contains_local_path", ...)` in `tests/orchestration/test_run_manifest_security.py`, `test_review_gate_sensitive_metadata.py` and `test_review_subject_strict_schema.py`. Moving `validate_job_input_definition` would force `job_input_definition.py` to import these names from `run_manifest`, which gate 6 forbids. `decode_job_input_definition_v1`'s only call is to `validate_job_input_definition`, so it stays for the same reason, one level removed. Step 4's own trailing clause — "name what stayed if anything did" — is read as the escape hatch for exactly this outcome, and the ledger's `run_manifest.py` bullet, the C2 commit subject and this handback all state the actual outcome plainly rather than the Step 4 text's assumption. `_VALID_SOURCES` and `VALID_ISOLATION_MODES`, neither a named candidate, stay in place untouched alongside the function that reads them.
- **`_SECRET_TERMS` moved as an unnamed sub-dependency.** The block named `is_secret_key`/`_safe_scalar` as the two Redaction-section names that move "as dependencies" if a candidate needs them; `is_secret_key`'s own body needs `_SECRET_TERMS`, used nowhere else in `run_manifest.py` and patched by no test, so it moved with it rather than being left behind as an orphaned private constant.
- **Four re-exported names need the `name as name` form.** `_h`, `_redacted_command_identity`, `_source_field` and the function `job_input_sha256` (distinct from the `job_input_sha256` dataclass field, which is untouched) have no remaining caller inside `run_manifest.py` after the move — every caller was itself moved — so ruff's unused-import rule needs the self-referential alias on each to signal the intentional re-export, each on its own `from packages.orchestration.job_input_definition import (... as ...)` statement, matching the round 3 precedent for `_run_probe`.
- **Commit trailer model name.** Every commit carries `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` — the model this session actually runs on — per the standing operator instruction, not a fixed name typed into the block.
- No extra commit beyond C1, C2, C3; no dropped one; no reordering.

## For the operator, in plain sentences

This round first recorded the previous round's acceptance and a decision about which of the open
problems fit into one round of work and which do not. It then took the first step a finding's own
text asks for on the file that records what inputs a job's run actually used: the part that builds
the typed description of those inputs moved into a module of its own, with every existing caller
still finding it under its old name. Two of the originally-planned pieces — the rule set that checks
the shape of that description, and the reader that applies it to an untrusted record — turned out to
depend on this file's own shared checking helpers closely enough that moving them would have broken
the rule that the new module may never import from the old one, so both stayed in place instead,
with the reason written down. Every check this round ran — the structure-size rule, the
import-reachability guard, the full test selection, the health check and the re-export guard —
passed on the first attempt, with no repair round needed. One problem, a lost run record when a task
is split, is left for the next clean-up because its repair is too large for this one. Three more
steps remain open for later sessions. Nothing waits on the operator right now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate.
3. Book round 4's verdict in the next round's first commit.
4. T007: R-1235's second step.

Operator questions open: 0.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `14512f90f` |
| C2 | done | `f778c4a09` |
| C3 | done | this commit |
| Candidate: `_h` | moved | no staying-name call; re-exported `as _h` (otherwise unused on `run_manifest`) |
| Candidate: `_redacted_command_identity` | moved | no staying-name call; re-exported `as _redacted_command_identity` (otherwise unused on `run_manifest`) |
| Candidate: `build_job_input_definition` | moved | no staying-name call; still called from the staying `build_input_snapshot` |
| Candidate: `job_input_definition_bytes` | moved | no staying-name call; still called from staying validators |
| Candidate: `job_input_definition_sha256` | moved | no staying-name call; still called from staying validators and `build_run_manifest` |
| Candidate: `job_input_sha256` (function) | moved | no staying-name call left in `run_manifest.py`; re-exported `as job_input_sha256` (otherwise unused there; still imported directly by tests) |
| Candidate: `validate_job_input_definition` | stayed | calls `_is_hex64`, `_safe_component`, `VALID_ISOLATION_MODES`, `_contains_secret`, `_contains_local_path` — shared helpers every other validator on `run_manifest` uses, two of them test-patched directly there (see Deviations) |
| Candidate: `JOB_INPUT_TOP_FIELDS` | moved | read only inside the staying `validate_job_input_definition`, resolved via the back-import |
| Candidate: `JOB_INPUT_TASK_FIELDS` | moved | same as above |
| Candidate: `JOB_INPUT_EXECUTION_STR_FIELDS` | moved | same as above |
| Candidate: `JOB_INPUT_EXECUTION_INT_FIELDS` | moved | same as above |
| Candidate: `JOB_INPUT_EXECUTION_BOOL_FIELDS` | moved | same as above |
| Candidate: `_JOB_INPUT_SOURCE_OF` | moved | read only inside the moving `_source_field` |
| Candidate: `JOB_INPUT_EXECUTION_FIELDS` | moved | read only inside the staying `validate_job_input_definition`, resolved via the back-import |
| Candidate: `_source_field` | moved | no staying-name call; re-exported `as _source_field` (otherwise unused on `run_manifest`) |
| Candidate: `decode_job_input_definition_v1` | stayed | its only call is to the staying `validate_job_input_definition` (see Deviations) |
| Dependency: `is_secret_key` | moved | named by the block as a Redaction-section dependency; still called from staying code |
| Dependency: `_safe_scalar` | moved | named by the block as a Redaction-section dependency; still called from staying code |
| Dependency: `_SECRET_TERMS` | moved | unnamed sub-dependency of `is_secret_key`, used nowhere else and patched by no test (see Deviations) |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `4640 passed, 3 skipped`, 133 paths, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | passed | six checks pass, `fail_count` 0 |
| Gate 5 | passed | `['R-1235', 'R-1246', 'R-1252']` |
| Gate 6 | passed | `ALL True` |
| Push | pending at write time | runs after this commit; result in the session's final reply |
