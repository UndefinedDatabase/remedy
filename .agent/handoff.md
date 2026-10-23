# Handback — F151 round 5

## Session

SESSION 1 of feature F151 · round 5 · rounds so far 5.

Context self-assessment: every prepared file under `.remedy-wt/f151-r5/prep/` was checked against
`digests.txt`'s sha256 (itself checked against the value the prompt gave) before use, the block and
DECISION F151 D5 (the prepared decisions file's last entry) were read in full before any code was
written; a genuine contradiction in C2's literal text was found and reported rather than silently
worked around, and C2 through C6 proceeded only after the reviewer's amendment confirmed and
corrected it.

Fortschritt: ~80 % (T001 to T003 code landed · the docs page and the closure open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical, `.agent/authored/f151-r5.md` confirmed equal to `block.md` by `wc -l` (125) and `sha256sum`, staged and committed alone |
| C2 | done | corrected per the reviewer's amendment (see Deviations); ten direct tests added for R-1438's numbered mutations, plus a whole-record capabilities golden and a config/`--safe-mode` golden; committed alone |
| C3a | done | `adapter_ref` linkage, `adapter_registry.py` (new), `remedy worker show`'s two adapter lines, the `ALLOWED_UNWIRED` line removed, the reachability allowlist regenerated from a measured closure diff; committed alone |
| C3b | done | the linkage's tests across the three named paths; committed alone |
| C4 | done | `tests/contracts/test_adapter_import_guard.py` (new): the checker, the two-tree walk, the violation fixture, the clean fixture; committed alone |
| C5 | done | `LLMWorker` and its now-unused imports deleted from `packages/contracts/interfaces.py`; the two naming tests in `tests/test_imports.py` trimmed, their other assertions kept; `LLMWorker` occurs nowhere under `packages`, `apps` or `tests` |
| R-1438 | done | ten mutations of `ClaudeCliReferenceAdapter` each now hold their own direct test, `86bd3db16` |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C6` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3409 passed, 2 skipped in 43.57s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `ruff check` → `All checks passed!`; `mypy` → `Success: no issues found in 8 source files` |
| Gate 4 | done | `worker show claude_code` → exit 0, two adapter lines; `--json` → exit 0, `adapter_ref` `claude-cli` |
| Gate 5 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 6 | done | `open_finding_ids` → `12` |
| Push | done | `git push origin feature/f151-worker-adapter-contract` |

## Range

Review of `384c8fb58`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `925a83dd5` F151 R5 C1: book round 4, resolve R-1437, register R-1438, DECISION F151 D5, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r5.md` | +125/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/decisions.md` | +10/-0 | DECISION F151 D5 appended: the `adapter_ref` linkage, the registry, `remedy worker show` as the product path, the import guard, `LLMWorker` deleted |
| `.agent/live_review.md` | +6/-0 | round 4's VERDICT FAIL gate entry booked; `Done:` line for R-1437 and the R-1438 registration appended |
| `.agent/plan.md` | +3/-4 | rewritten: current step R-1438's tests and T003's second half under D5, next step the docs page/architecture section/README index |

### `86bd3db16` F151 R5 C2: the reference adapter's unguarded promises

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_claude_cli_reference.py` | +70/-1 | ten direct tests, one per R-1438 numbered mutation: the `malformed_output:`-before-shared-predicates ordering (1), an I/O-predicate text folding to unknown rather than the I/O class (2, literal corrected per the reviewer's amendment), exit code 0 never counting as non-zero (3), the whole `AdapterCapabilities` record compared against D4 (6) for both streaming flags (4-8), a `claude_cli.customizations` configuration reaching `build_claude_cli_args` unchanged with `--safe-mode` absent (9), and an `is_error` envelope with a `usage` object added still mapping to `None` (10) |

### `9850e1b5f` F151 R5 C3a: the adapter_ref linkage, the adapter registry, and worker show

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/worker_adapters.py` | +12/-0 | `adapter_ref: str = ""` field (additive); `claude_code`'s record sets it to `claude-cli`; the export writes it for every record; the summary prints `Adapter: <ref>` under a record that has one; the v1/v2 relationship paragraph added to the module docstring |
| `packages/contracts/adapter_contract.py` | +5/-0 | the same v1/v2 relationship paragraph added to this module's docstring, so a search for `adapter_ref` finds both |
| `packages/providers/adapters/adapter_registry.py` | +26/-0 (new) | `WORKER_ADAPTERS_BY_REF` and `resolve_worker_adapter(adapter_ref) -> WorkerAdapter \| None`, each with its WHY comment |
| `apps/cli/commands/worker.py` | +19/-7 | `_cmd_worker_show` imports the registry inside the function, resolves the record's reference, and prints `Adapter: <ref>`/`Capabilities: <flags-or-none>` when an adapter answers; restructured the `if json_output: ... else: ...` into an early return so the new lines sit at one indent level |
| `tests/test_no_orphan_modules.py` | +0/-3 | the reference adapter's `ALLOWED_UNWIRED` line deleted — it is now reached through the registry |
| `tests/orchestration/import_reachability_allowlist.txt` | +3/-0 | three newly reachable modules added, computed from a closure diff (see "Allowlist lines added" below) |

### `d137e549f` F151 R5 C3b: the linkage's tests

| Path | +/- | Reason |
|---|---|---|
| `tests/test_worker_adapters.py` | +19/-0 | only `claude_code` carries a non-empty `adapter_ref` (and it is `claude-cli`); the export carries `adapter_ref` for every record; the summary prints `Adapter: claude-cli` exactly once |
| `tests/cli/test_worker.py` | +25/-0 | `worker show claude_code` text output carries `Adapter: claude-cli` and `Capabilities: json_schema, session_resume, streaming, tool_use`; `worker show ollama` carries neither line; the JSON answer's record carries `adapter_ref` |
| `tests/contracts/test_adapter_registry.py` | +24/-0 (new) | every non-empty reference resolves to an adapter whose `adapter_id` equals it and which passes `isinstance(..., WorkerAdapter)`; `resolve_worker_adapter("")` and `resolve_worker_adapter("no-such")` are both `None` |

### `7c94dcc12` F151 R5 C4: the import guard and its violation fixture

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_adapter_import_guard.py` | +78/-0 (new) | `import_guard_violations(source)` (the per-file checker), `walk_guarded_trees(root)` (the two-tree walk reporting `path:line`); an assertion the live walk finds none; a violation fixture (a function-body import of the reference adapter) reports exactly one; a clean fixture importing `packages.contracts.adapter_contract` reports none |

### `491575b6b` F151 R5 C5: delete LLMWorker, which WorkerAdapter replaces

| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/interfaces.py` | +1/-24 | `LLMWorker` deleted along with its now-unused `AsyncIterator`, `Artifact` and `TaskEntry` imports (kept `JobPlan`, still used by two other protocols) |
| `tests/test_imports.py` | +2/-4 | `LLMWorker` dropped from `test_contracts_interfaces_import` and `test_interfaces_are_protocols`; their other assertions (`MemoryGateway`, `RuntimeProvider`) kept |

## Allowlist lines added (C3a, `tests/orchestration/import_reachability_allowlist.txt`)

Computed by diffing `reachable_closure()` before and after C3a's code edits (452 → 455 modules), via a
`python3` script under `.remedy-wt/f151-r5-worker/`, never typed by hand:

- `packages.contracts.adapter_contract`
- `packages.providers.adapters.adapter_registry`
- `packages.providers.adapters.claude_cli_reference`

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, after this commit.
- No pull request was opened (the block orders none). No worktree was added or removed by this worker.
  No merge, no rebase, no amend. No provider call.

## Verification

Interpreter: the repository's configured Python 3. All six gates were run once each, after C5 and
before C6, per the block.

Gate 1 — `git -C <repo> status --porcelain` → empty. `python3 .remedy-wt/f151-r5/prep/verify.py .` →
every line `True`: all six commits single-parent and under 500 insertions (144, 70, 65, 68, 78, 3),
each carries an `F151 R5 Cn` subject, C3 is exactly C3a and C3b, on
`feature/f151-worker-adapter-contract`, C1's four paths exact and byte-equal to their `c1-*` snapshots,
C2 through C5's paths exact and hold no machine path; `C6` read `absent` (not yet committed at gate
time); the saved block equals `block.md`; the ledger holds no `Landed:`/`Done:` line for R-1438;
`LLMWorker` occurs nowhere under `packages`, `apps` or `tests`; last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r5/prep/run_selection.py . .remedy-wt/f151-r5-worker/selection-output.txt`
→ `paths 83`, `exit 0`, `3409 passed, 2 skipped in 43.57s`; the two SKIPPED lines printed verbatim:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract file)
and `tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set). No FAILED, no
ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m ruff check packages/contracts packages/providers/adapters packages/orchestration/worker_adapters.py apps/cli/commands/worker.py tests/contracts tests/test_worker_adapters.py tests/cli/test_worker.py tests/test_imports.py tests/test_no_orphan_modules.py`
→ `All checks passed!`. `python3 -m mypy packages/contracts packages/providers/adapters packages/orchestration/worker_adapters.py`
→ `Success: no issues found in 8 source files`.

Gate 4 — `python3 -m apps.cli.main worker show claude_code` → exit 0, prints `Adapter: claude-cli` and
`Capabilities: json_schema, session_resume, streaming, tool_use`. `python3 -m apps.cli.main worker show
claude_code --json` → exit 0, `"adapter_ref": "claude-cli"` in the one record.

Gate 5 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all `pass`
(`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict FAIL`, `plan_consistency`
`unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0, relevant=0`,
`repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`, `high_blockers_open`
`no open blocker/high findings`).

Gate 6 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `12`.

## Authored-text proofs

C1's four paths are reviewer-authored or reviewer-produced text applied this round. Each was copied
from its prepared `c1-*` file under `.remedy-wt/f151-r5/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r5-worker/` (`do_c1_copy.py`), which hashed source and destination with sha256
immediately after the copy; all four pairs read equal. `block.md` itself (saved as
`.agent/authored/f151-r5.md`) was separately confirmed equal to the prepared `block.md` by its sha256
(given in the prompt, checked before any file was used) and again by `wc -l` (125) and `sha256sum`
directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`tests/contracts/test_claude_cli_reference.py` (C2), the C3a/C3b/C4/C5 paths are NOT reviewer-authored
text — they were written by this worker from the block and DECISION F151 D5's prose — so no
disk-to-disk comparison applies to them; their own correctness is the gate and self-review-loop checks
recorded above.

## Findings landed

Landed: R-1438 — ten direct tests added to `tests/contracts/test_claude_cli_reference.py`, one per
R-1438's numbered mutation (items 2's literal corrected per the reviewer's amendment below), `86bd3db16`.

## Deviations & assumptions

Reviewer amendment: C2's I/O literal replaced, because broken pipe is read first by the connection
predicate.

Before writing C2, this worker computed `classify_claude_cli_error("write failed: broken pipe", None)`
against the unmodified reference adapter and found it returns `FailureClass.PROVIDER_UNAVAILABLE`, not
`FailureClass.UNKNOWN` as the block's C2 text and R-1438's own REPAIR sentence required — "broken pipe"
is a marker in both `is_provider_connection_error` and `is_io_failure_error`, and the connection
predicate is checked first in `_classify_error_text`, so that literal can never reach the I/O class at
all. This is a contradiction the block's own text introduced (not a defect reachable from inside C2's
test-only path), so the worker stopped before writing C2 and reported it rather than silently
substituting a different literal. The reviewer confirmed the diagnosis and amended the block to
`"write failed: no space left on device"` (measured by the reviewer at `925a83dd5`: `_classify_error_text`
reads `FailureClass.IO_FAILURE` for it, `classify_claude_cli_error` folds it to `FailureClass.UNKNOWN`),
with the instruction to leave R-1438's landed ledger text unchanged (append-only) and record this
amendment here. No other departure from the block's ordered commit sequence occurred: C1, C2, C3a, C3b,
C4, C5 and C6 landed in that order, each alone, each under the 500-insertion cap.

The reachability allowlist's three new lines were inserted at their correct alphabetical position
within the existing file (`packages.contracts.adapter_contract` between the `packages.common.*` and
`packages.core.models` runs; the two `packages.providers.adapters.*` lines before
`packages.providers.claude_planner.provider`), rather than appended as a trailing block — the file is
otherwise sorted aside from one pre-existing out-of-order block from an earlier round, and inserting in
sorted position reads as the more literal match for the block's "in the file's sorted order" instruction.

`apps/cli/commands/worker.py`'s `_cmd_worker_show` was restructured from `if json_output: ... else:
...` to an early `return` after the JSON branch, so the new adapter-line logic sits at the function's
top indent level rather than nested inside an `else`; behavior is unchanged (`fail()` is `NoReturn`, so
the `match is None` branch already never fell through).

No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two test
commands ran at the same time; `REMEDY_TEST_MAX_WORKERS` was not set. No merge, no rebase, no amend, no
stash, no provider call. No file outside the paths the block names per commit was touched; in
particular only `worker_adapters.py` changed under `packages/orchestration/`. `git branch --show-current`
was run as a standalone command, never joined to another, before every commit, and read
`feature/f151-worker-adapter-contract` every time.

## For the operator, in plain sentences

This round first booked the previous round's review verdict and its two closed-out findings, then
added a set of direct tests that pin down ten small edge cases in the reference adapter's error and
capability handling so none of them can quietly regress. One of the example inputs specified for those
tests turned out to classify differently than expected once actually measured against the real code, so
work paused and the discrepancy was reported before any test was written against it; the example was
then corrected and the round continued. The bulk of the work links the earlier worker-list entries to
their executable adapters: a new lookup table resolves a stable reference name to the adapter that
implements it, the worker-information command now reports which adapter a worker is linked to and what
it can do, and a guard was added that keeps the orchestration and contract layers from reaching into a
concrete adapter's code directly. Finally, an older, never-implemented interface that the new adapter
contract fully replaces was removed, along with the handful of test lines that only existed to prove it
could be imported. The round ran its own selection of tests chosen for this change, not the project's
whole test collection, and that selection, the two style checks and the project's own health check all
came back clean.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 5's verdict in the next round's first commit.
4. The docs page for the contract, the architecture page's worker section, and the README index.

Operator questions open: 0. Open findings: 12, gate 6 printed.
