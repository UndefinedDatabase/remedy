# Handback — F151 round 6

## Session

SESSION 1 of feature F151 · round 6 · rounds so far 6.

Context self-assessment: both prepared top-level digests (`block.md`, `digests.txt`) and all
eleven prepared files under `.remedy-wt/f151-r6/prep/` were checked against `digests.txt` before
use, the block was read in full before any edit, and R-1439 and R-1440 were each repaired exactly
as their REPAIR sentences in the prepared ledger state, with the new logic smoke-tested against
hand-built fixtures before the gates ran.

Fortschritt: ~85 % (T001 to T003 and the docs landed · the closure open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical; `.agent/authored/f151-r6.md` confirmed equal to `block.md` by `wc -l` (87) and `sha256sum`; staged and committed alone |
| C2 | done | three prepared docs paths copied and proved byte-identical; staged and committed alone |
| C3 | done | `import_guard_violations` now also flags an `ImportFrom` whose module joined to an imported name is forbidden; two new tests and the module docstring's sentence updated; committed alone |
| C4 | done | a monkeypatched no-capability adapter drives `_cmd_worker_show`'s text output to `  Capabilities: none`; committed alone |
| C5 | done | this handback |
| R-1439 | done | repaired in C3, `a360ad6e4` |
| R-1440 | done | repaired in C4, `5c47b4a5d` |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C5` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3758 passed, 2 skipped in 33.18s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `ruff check tests/contracts tests/cli/test_worker.py` → `All checks passed!` |
| Gate 4 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 5 | done | `open_finding_ids` → `13` |
| Push | done | `git push origin feature/f151-worker-adapter-contract`, run once after this commit |

## Range

Review of `79592512a`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `4bf835fc0` F151 R6 C1: book round 5, resolve R-1438, register R-1439 and R-1440, the slip, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r6.md` | +87/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/live_review.md` | +8/-0 | round 5's VERDICT FAIL gate entry booked; `Done:` line for R-1438 appended; R-1439 and R-1440 registered |
| `.agent/plan.md` | +6/-6 | rewritten: current step R-1439/R-1440's repairs and the docs page, next step the closure sequence |
| `.agent/prose_slips.md` | +1/-0 | the round 5 prose slip appended (R-1438's I/O literal contradiction and the reviewer's amendment) |

### `b160a2f2d` F151 R6 C2: the worker adapter contract's docs page and its index rows

| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v1.md` | +80/-0 (new) | the contract's docs page: ownership, the typed contract, the conformance kit, the reference adapter, the registry/`adapter_ref` link, and the import guard |
| `docs/README.md` | +2/-0 | two index rows added for the new page (the quick-find table and the specifications list) |
| `docs/system/architecture.md` | +9/-0 | `adapter_ref` added to the worker spec field table; an "Adapter contract v2" section links to the new page |

### `a360ad6e4` F151 R6 C3: the import guard reads a name imported from the adapters' parent

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_adapter_import_guard.py` | +16/-1 | `import_guard_violations` also flags an `ImportFrom` whose `module` joined by a dot to an imported name is forbidden; two tests added (`from packages.providers import adapters` reported once, `from packages.providers import claude_planner` not reported); the module's top docstring sentence on what the guard fails on extended to name the joined-name case |

### `5c47b4a5d` F151 R6 C4: the worker show line for an adapter that declares nothing

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_worker.py` | +24/-0 | a test that monkeypatches `packages.providers.adapters.adapter_registry.resolve_worker_adapter` to answer an adapter whose `AdapterCapabilities` are all false, then asserts `_cmd_worker_show`'s text output carries `  Capabilities: none` |

### This commit (C5) — handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, after this commit.
- No pull request was opened (the block orders none). No worktree was added or removed by this
  worker. No merge, no rebase, no amend, no stash, no provider call.

## Verification

Interpreter: the repository's configured Python 3. All five gates were run once each, after C4
and before C5, per the block.

Gate 1 — `git -C <repo> status --porcelain` → empty (no output). `python3
.remedy-wt/f151-r6/prep/verify.py .` → every line `True`: all four commits single-parent and under
500 insertions (102, 91, 16, 24), each carries an `F151 R6 Cn` subject, on
`feature/f151-worker-adapter-contract`; C1's four paths exact and byte-equal to their `c1-*`
snapshots; C2's three paths exact and byte-equal to their `c2-*` snapshots; C3 and C4's one path
each exact and hold no machine path; `C5` read `absent` (not yet committed at gate time); the
saved block equals `block.md`; the ledger holds no `Landed:`/`Done:` line for R-1439 or R-1440;
`LLMWorker` occurs nowhere under `packages`, `apps` or `tests`; last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r6/prep/run_selection.py . .remedy-wt/f151-r6-worker/selection-output.txt`
→ `paths 84`, `exit 0`, `3758 passed, 2 skipped in 33.18s`; the two SKIPPED lines printed verbatim:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract
file) and `tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set). No
FAILED, no ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m ruff check tests/contracts tests/cli/test_worker.py` → `All checks passed!`.

Gate 4 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all
`pass` (`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict FAIL`,
`plan_consistency` `unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0,
relevant=0`, `repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`,
`high_blockers_open` `no open blocker/high findings`).

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `13`.

## Authored-text proofs

C1's four paths and C2's three paths are reviewer-authored or reviewer-produced text applied this
round. Each was copied from its prepared `c1-*`/`c2-*` file under `.remedy-wt/f151-r6/prep/` by a
dedicated `python3` script under `.remedy-wt/f151-r6-worker/`, which compared source and
destination bytes immediately after each copy; all seven pairs read equal. `block.md` itself
(saved as `.agent/authored/f151-r6.md`) was separately confirmed equal to the prepared `block.md`
by its sha256 (given in the prompt, checked before any file was used), again by `wc -l` (87) and
`sha256sum` directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`tests/contracts/test_adapter_import_guard.py` (C3) and `tests/cli/test_worker.py` (C4) are NOT
reviewer-authored text — they were written by this worker from the block's instructions and
R-1439/R-1440's REPAIR sentences — so no disk-to-disk comparison applies to them; their own
correctness is the gate and self-review-loop checks recorded above.

## Findings landed

Landed: R-1439 — `import_guard_violations` in `tests/contracts/test_adapter_import_guard.py` now
also flags an `ImportFrom` whose module joined by a dot to an imported name is forbidden, with a
fixture reporting `from packages.providers import adapters` once and `from packages.providers
import claude_planner` never, `a360ad6e4`.

Landed: R-1440 — a test in `tests/cli/test_worker.py` monkeypatches the registry's
`resolve_worker_adapter` to answer an adapter with every capability false and asserts
`_cmd_worker_show`'s text output carries `  Capabilities: none`, `5c47b4a5d`.

## Deviations & assumptions

The block's C3 instruction "Update the module docstring's sentence on what is read" was read as
the file's top-of-file module docstring (the literal Python module docstring), not the
`import_guard_violations` function's own docstring, since only the module docstring is named that
way anywhere in this repository's own usage; the top docstring's sentence on what import the guard
fails on was extended to name the joined-name case, and the function's own docstring was left
unchanged.

Before committing C4, this worker ran `python3 -B -m pytest tests/cli/test_worker.py -q -k
TestWorkerShowAdapterLinkage` once as a self-review check on the new test alone; this is not one
of the block's five named gates, ran sequentially (never alongside another test command), and did
not set `REMEDY_TEST_MAX_WORKERS`.

No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two
test commands ran at the same time. No merge, no rebase, no amend, no stash, no provider call. No
file outside the paths the block names per commit was touched; no production file changed this
round — C3 and C4 touch only `tests/`. `git branch --show-current` was run as a standalone command,
never joined to another, before every commit, and read `feature/f151-worker-adapter-contract`
every time.

## For the operator, in plain sentences

This round first booked the previous round's review result and its closed-out item, then recorded
two new small follow-up items the reviewer had found. The round's main work was twofold. First, it
added a page of documentation describing how Remedy's worker programs connect to the code that
actually runs them, and linked that page from the two places a reader would look for it. Second, it
closed the two follow-up items: a safety check that stops certain code from reaching into a
provider's internals directly was taught to notice one more way that could happen, and the
command that reports on a worker now has a test proving it prints the word "none" when a worker
declares no special abilities, rather than leaving that line unchecked. The round ran its own
selection of tests chosen for this change, not the project's whole test collection, and that
selection, the style check and the project's own health check all came back clean.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 6's verdict in the next round's first commit.
4. The closure sequence: the integration gate and the self-use run.

Operator questions open: 0. Open findings: 13, gate 5 printed.
