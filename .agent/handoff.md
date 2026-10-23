# Handback — F151 round 2

## Session

SESSION 1 of feature F151 · round 2 · rounds so far 2.

Context self-assessment: every prepared file this round (`block.md` and the seven other files
under `.remedy-wt/f151-r2/prep/` that `digests.txt` lists) was checked against `digests.txt`'s sha256
before use, and `digests.txt`'s own sha256 was checked against the value given in the prompt, both
with a `python3` script under `.remedy-wt/f151-r2-worker/`; the whole block, DECISION F151 D2,
`.agent/f151_inventory.md`, `docs/agents/handback_template.md`, `packages/contracts/interfaces.py`,
the named `stream_evidence.py` lines, `token_actuals.py`, `failure_postmortem.py` and both named
tests were read in full before any code was written; every dataclass, the protocol and the kit's
seven dimension checks were written from DECISION F151 D2's text directly, never recalled; and every
gate reading below was produced by running the thing.

Fortschritt: ~45 % (T001 and T002 landed · T003 open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical, `.agent/authored/f151-r2.md` confirmed equal to `block.md` by `wc -l` (153) and `sha256sum`, staged and committed alone |
| C2 | done | `packages/contracts/adapter_contract.py` and its test file written from DECISION F151 D2 (3); `_GUARDED_PACKAGES` gained `packages/contracts`; committed alone |
| C3a | done | split from C3 (declared below): `packages/contracts/adapter_conformance_kit.py` and the `ALLOWED_UNWIRED` entry, committed alone |
| C3b | done | split from C3: `tests/contracts/test_adapter_conformance_kit.py` — the conforming CLI/HTTP toys and one broken toy per dimension — committed alone |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C4` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3237 passed, 2 skipped in 35.52s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `ruff check` → `All checks passed!`; `mypy` → `Success: no issues found in 2 source files` |
| Gate 4 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 5 | done | `open_finding_ids` → `11` |
| C4 | done | this handback written and committed |
| Push | done | `git push origin feature/f151-worker-adapter-contract` succeeded on the first attempt, no HTTP 500 |

## Range

Review of `ebea24422`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `2fa2a9a57` F151 R2 C1: book round 1, DECISION F151 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r2.md` | +153/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/decisions.md` | +10/-0 | DECISION F151 D2 appended: the contract's names, the ownership table, the protocol, the kit, the proof |
| `.agent/live_review.md` | +2/-0 | round 1's VERDICT PASS gate entry booked |
| `.agent/plan.md` | +6/-6 | rewritten: current step T002, next steps T003 and closure |

### `c17439e36` F151 R2 C2: the adapter contract

| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_contract.py` | +145/-0 (new) | `ADAPTER_ROLES`, `STREAM_EVENT_TYPES`, `ADAPTER_ERROR_CLASSES`, the five frozen dataclasses, `AdapterInvocation`, and the `WorkerAdapter` protocol (D2 (3)) |
| `tests/contracts/__init__.py` | +0/-0 (new) | empty package marker |
| `tests/contracts/test_adapter_contract.py` | +131/-0 (new) | one test per promise: frozen dataclasses, no `timeout` field, `STREAM_EVENT_TYPES` read from `vars()`, the five error classes, the two roles, a conforming/incomplete class against `WorkerAdapter` |
| `tests/test_no_interactive_guard.py` | +1/-0 | `packages/contracts` appended to `_GUARDED_PACKAGES` |

### `c600ecedd` F151 R2 C3a: the conformance kit module and orphan entry

| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_conformance_kit.py` | +349/-0 (new) | `CONFORMANCE_DIMENSIONS`, `ConformanceFailure`, `ErrorSample`, `AdapterSamples`, `CANONICAL_PROMPT_PARTS`, the seven dimension checks, `check_conformance_dimension`, `run_adapter_conformance` |
| `tests/test_no_orphan_modules.py` | +3/-0 | `ALLOWED_UNWIRED` entry for the kit, in path order, with its one-line reason |

### `94819193c` F151 R2 C3b: the conformance kit's conforming and broken toys

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_adapter_conformance_kit.py` | +295/-0 (new) | a conforming CLI toy and a conforming HTTP toy, both reading `()` from `run_adapter_conformance`; ten broken-toy variants (two each for `invocation`, `stream` and `transport`, one each for the other four), each failing exactly its own dimension; the missing-timeout-sample case; `check_conformance_dimension`'s `ValueError`; `CONFORMANCE_DIMENSIONS`'s exact tuple |

## External actions

- `git push origin feature/f151-worker-adapter-contract` → run once, after this commit, succeeded on
  the first attempt; no HTTP 500, no retry needed.
- No pull request was opened (the block orders none). No worktree was added or removed by this worker.
  No merge, no rebase, no amend. No provider call.

## Verification

Interpreter: the repository's configured Python 3. All five gates were run once each, after C3b and
before C4, per the block.

Gate 1 — `git status --porcelain` → empty. `python3 .remedy-wt/f151-r2/prep/verify.py .` → every line
`True`: all four commits single-parent and under 500 insertions (171, 277, 352, 295), each carries an
`F151 R2 Cn` subject, only C3 is split (C3a/C3b, at most once), on `feature/f151-worker-adapter-contract`,
C1's four paths exact and byte-equal to their `c1-*` snapshots, C2's and C3's paths exact and hold no
machine path; `C4` read `absent` (not yet committed at gate time); last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r2/prep/run_selection.py . .remedy-wt/f151-r2-worker/selection-output.txt`
→ `paths 81`, `exit 0`, `3237 passed, 2 skipped in 35.52s`; the two SKIPPED lines printed verbatim:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract file)
and `tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set). No FAILED, no
ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m ruff check packages/contracts/adapter_contract.py
packages/contracts/adapter_conformance_kit.py tests/contracts tests/test_no_interactive_guard.py
tests/test_no_orphan_modules.py` → `All checks passed!`. `python3 -m mypy
packages/contracts/adapter_contract.py packages/contracts/adapter_conformance_kit.py` → `Success: no
issues found in 2 source files`.

Gate 4 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all `pass`
(`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict PASS`, `plan_consistency`
`unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0, relevant=0`,
`repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`, `high_blockers_open`
`no open blocker/high findings`).

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `11`.

## Authored-text proofs

C1's four paths are reviewer-authored or reviewer-produced text applied this round. Each was copied
from its prepared `c1-*` file under `.remedy-wt/f151-r2/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r2-worker/` (`c1_copy.py`), which hashed source and destination with sha256
immediately after the copy; all four pairs read equal. `block.md` itself (saved as
`.agent/authored/f151-r2.md`) was separately confirmed equal to the prepared `block.md` by its sha256
(given in the prompt, checked before any file was used) and again by `wc -l` (153) and `sha256sum`
directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`packages/contracts/adapter_contract.py`, `packages/contracts/adapter_conformance_kit.py` and their
tests (C2, C3a, C3b) are NOT reviewer-authored text — they were written by this worker from DECISION
F151 D2's prose — so no disk-to-disk comparison applies to them; their own correctness is the gate and
self-review-loop checks recorded above.

## Deviations & assumptions

C3 was split into C3a (the module plus the orphan-list entry) and C3b (the test file) because the
single commit would have reached 647 insertions, over the 500-insertion cap; the split is declared
here as the block allows, and `verify.py`'s "only C3 is split, at most once" check passed.

`HttpInvocation`'s field order is `method, url, body, headers=()` rather than DECISION F151 D2's
prose order `method, url, headers=(), body`: a dataclass cannot place a field without a default
(`body`) after one that has a default (`headers`), so the order was adjusted for validity while
keeping every field's name, type and default exactly as specified; the module carries a one-line
comment at the dataclass naming this.

The two conforming toys' `classify_error` return `FailureClass("provider_timeout")` rather than
`FailureClass.PROVIDER_TIMEOUT`: the `transport` dimension flags any `Attribute` whose lower-cased
text contains `timeout`, which the enum member's own name does, so spelling it as an attribute inside
an adapter class would make every real adapter that correctly classifies a timeout fail its own
`transport` check. Constructing the same member by its string value avoids the attribute node
entirely (the string lives in an `ast.Constant`, which the transport scan does not inspect) while
returning the identical `FailureClass.PROVIDER_TIMEOUT` member. A comment at the first use in
`tests/contracts/test_adapter_conformance_kit.py` names this. `_check_isolation` carries one
`# type: ignore[func-returns-value]` with a one-line reason: the protocol types `isolation()` as
always returning `None`, and the check exists precisely to catch a broken implementation that
violates that statically-declared promise at runtime.

No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two test
commands ran at the same time. No merge, no rebase, no amend, no stash, no provider call. No file
outside the paths the block names per commit was touched. `git branch --show-current` was run as a
standalone command, never joined to another, before every commit, and read
`feature/f151-worker-adapter-contract` every time.

## For the operator, in plain sentences

This round gave the builder-and-reviewer call path its first typed contract: a small set of frozen
records describing what one backend can do, how a request to it is built, and how its raw output maps
back onto the shapes the rest of the system already understands, plus a reusable kit that proves any
future backend implementation honors that contract on every one of its seven faces before it is ever
wired into a real job. Nothing about how a job actually runs today changed; this is the interface the
next round's reference wrapper will sit behind. The kit's own test suite proves its honesty the direct
way: a correctly built toy backend passes every check, and ten separately broken variants each fail
only the one check their particular defect belongs to, never any other. The round ran its own selection
of tests chosen for this change, not the project's whole test collection, and that selection, the two
style checks and the project's own health check all came back clean.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 2's verdict in the next round's first commit.
4. T003: the reference adapter, the import guard, the registry linkage.

Operator questions open: 0. Open findings: 11, gate 5 printed (`R-1246`, `R-1281`, `R-1326`, `R-1351`,
`R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427` and `R-1428`, all owned by F314).
