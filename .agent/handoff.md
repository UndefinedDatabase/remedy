# Handback — F151 round 4

## Session

SESSION 1 of feature F151 · round 4 · rounds so far 4.

Context self-assessment: every prepared file under `.remedy-wt/f151-r4/prep/` was checked against
`digests.txt`'s sha256 (itself checked against the value given in the prompt) before use, the block,
DECISION F151 D2 and DECISION F151 D4 (the prepared decisions file's last entry) were read in full
before any code was written, and the reference adapter was built as a thin wrapper over
`build_claude_cli_args`, `parse_cli_result_detailed`, `redact_stream_payload`/`normalize_stream_object`
and the shared error predicates `_classify_error_text` asks — never a re-implementation of any of them.

Fortschritt: ~65 % (T001, T002 and the reference adapter landed · the import guard, the linkage and the
docs open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical, `.agent/authored/f151-r4.md` confirmed equal to `block.md` by `wc -l` (128) and `sha256sum`, staged and committed alone |
| C2 | done | `tests/contracts/test_adapter_conformance_kit.py` gained two literal-value pin tests and the six `adapter_transport_violations` parametrized tests now parametrize over this file's own module constants instead of the kit's; committed alone, under the 500-insertion cap, so no split was needed |
| C3 | done | `packages/providers/adapters/__init__.py` (new) and `packages/providers/adapters/claude_cli_reference.py` (new) add `ClaudeCliReferenceAdapter` and `classify_claude_cli_error`; `tests/test_no_orphan_modules.py` gained the adapter's `ALLOWED_UNWIRED` line in path order; committed alone, under the 500-insertion cap, so no split was needed |
| C4 | done | `tests/contracts/test_claude_cli_reference.py` (new) holds the kit run, the invocation/stream/usage/error goldens; committed alone, under the 500-insertion cap, so no split was needed |
| R-1437 | done | `_FORBIDDEN_NAME_SUBSTRINGS` and `_FORBIDDEN_MODULE_ROOTS` are now pinned against literal module constants of the test file, and the six parametrized transport tests parametrize over those constants, not the kit's — a word or module root dropped from the kit's own lists can no longer silently drop its own test along with it |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C5` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3360 passed, 2 skipped in 34.50s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `ruff check` → `All checks passed!`; `mypy` → `Success: no issues found in 6 source files` |
| Gate 4 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 5 | done | `open_finding_ids` → `12` |
| Push | done | `git push origin feature/f151-worker-adapter-contract` |

## Range

Review of `03a7847a6`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `6d7ff2d26` F151 R4 C1: book round 3, resolve R-1435 and R-1436, DECISION F151 D4, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r4.md` | +128/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/decisions.md` | +10/-0 | DECISION F151 D4 appended: the reference adapter wraps today's claude-cli functions unchanged, its goldens compare against those functions, the loop is not rewired |
| `.agent/live_review.md` | +6/-0 | round 3's VERDICT FAIL gate entry booked; `Done:` lines for R-1435 and R-1436 appended |
| `.agent/plan.md` | +4/-4 | rewritten: current step the reference adapter and its goldens, next step T003's second half and the closure |

### `76682ae14` F151 R4 C2: pin the kit's forbidden words and module roots

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_adapter_conformance_kit.py` | +30/-6 | two module constants `_EXPECTED_FORBIDDEN_NAME_SUBSTRINGS` and `_EXPECTED_FORBIDDEN_MODULE_ROOTS` added, each pinned to its literal value by a new test against the kit's own `_FORBIDDEN_NAME_SUBSTRINGS`/`_FORBIDDEN_MODULE_ROOTS`; the six `adapter_transport_violations` parametrized tests now parametrize over the new module constants instead of the kit's own, so a word or module root dropped from the kit cannot silently drop its own test |

### `7a9d161d0` F151 R4 C3: the claude-cli reference adapter

| Path | +/- | Reason |
|---|---|---|
| `packages/providers/adapters/__init__.py` | +5/-0 (new) | package docstring: concrete worker adapters live here, orchestration never imports them |
| `packages/providers/adapters/claude_cli_reference.py` | +146/-0 (new) | `ClaudeCliReferenceAdapter` (every `WorkerAdapter` member per D4 (1) to (6)) and the module-level `classify_claude_cli_error` `classify_error` delegates to; both wrap existing claude-cli functions, re-implementing none |
| `tests/test_no_orphan_modules.py` | +3/-0 | `ALLOWED_UNWIRED` gains the adapter's line, in path order, naming T003's next round as the remover |

### `98e97e217` F151 R4 C4: the reference adapter's goldens and its kit run

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_claude_cli_reference.py` | +292/-0 (new) | every adapter built with `config={}`; the kit run for a streaming and a non-streaming adapter; invocation goldens over role/model/schema/resume and a two-part-prompt join; stream goldens over every recorded fixture against `capture_stream_evidence`'s own normalized events, plus the secrets-canary leak check and the non-streaming empty-tuple case; usage goldens over every recorded result line carrying a usage object, plus the `is_error`/empty-string/non-JSON-string None cases; error goldens over every distinct `ClaudeCliProvider` raise message (placeholders replaced by a number) plus a missing binary, a refused connection, a `malformed_output:` message and an unmatched text under both an exit code and none; `adapter_id` checked against `ROLE_PROVIDER_NAMES` |

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, after this commit.
- No pull request was opened (the block orders none). No worktree was added or removed by this worker.
  No merge, no rebase, no amend. No provider call.

## Verification

Interpreter: the repository's configured Python 3. All five gates were run once each, after C4 and
before C5, per the block.

Gate 1 — `git status --porcelain` → empty. `python3 .remedy-wt/f151-r4/prep/verify.py .` → every line
`True`: all four commits single-parent and under 500 insertions (148, 30, 154, 292), each carries an
`F151 R4 Cn` subject, no split occurred on C3 or C4 (the block allows at most one each), on
`feature/f151-worker-adapter-contract`, C1's four paths exact and byte-equal to their `c1-*` snapshots,
C2's, C3's and C4's paths exact and hold no machine path; `C5` read `absent` (not yet committed at gate
time); the ledger holds no `Landed:`/`Done:` line for R-1437; last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r4/prep/run_selection.py . .remedy-wt/f151-r4-worker/selection-output.txt`
→ `paths 81`, `exit 0`, `3360 passed, 2 skipped in 34.50s`; the two SKIPPED lines printed verbatim:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract file)
and `tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set). No FAILED, no
ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m ruff check packages/contracts packages/providers/adapters tests/contracts tests/test_no_orphan_modules.py`
→ `All checks passed!`. `python3 -m mypy packages/contracts packages/providers/adapters` → `Success: no
issues found in 6 source files`.

Gate 4 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all `pass`
(`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict FAIL`, `plan_consistency`
`unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0, relevant=0`,
`repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`, `high_blockers_open`
`no open blocker/high findings`).

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `12`.

## Authored-text proofs

C1's four paths are reviewer-authored or reviewer-produced text applied this round. Each was copied
from its prepared `c1-*` file under `.remedy-wt/f151-r4/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r4-worker/` (`c1_copy.py`), which hashed source and destination with sha256
immediately after the copy; all four pairs read equal. `block.md` itself (saved as
`.agent/authored/f151-r4.md`) was separately confirmed equal to the prepared `block.md` by its sha256
(given in the prompt, checked before any file was used) and again by `wc -l` (128) and `sha256sum`
directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`tests/contracts/test_adapter_conformance_kit.py` (C2), `packages/providers/adapters/__init__.py`,
`packages/providers/adapters/claude_cli_reference.py`, `tests/test_no_orphan_modules.py` (C3), and
`tests/contracts/test_claude_cli_reference.py` (C4) are NOT reviewer-authored text — they were written
by this worker from the block and DECISION F151 D4's prose — so no disk-to-disk comparison applies to
them; their own correctness is the gate and self-review-loop checks recorded above.

## Findings landed

Landed: R-1437 — `_FORBIDDEN_NAME_SUBSTRINGS` and `_FORBIDDEN_MODULE_ROOTS` are pinned against literal
module constants of the test file (`_EXPECTED_FORBIDDEN_NAME_SUBSTRINGS`,
`_EXPECTED_FORBIDDEN_MODULE_ROOTS`), and the six `adapter_transport_violations` parametrized tests now
parametrize over those constants rather than the kit's own two lists, `76682ae14`.

## Deviations & assumptions

The stream-golden comparison (`tests/contracts/test_claude_cli_reference.py`) strips five keys from
`capture_stream_evidence`'s own written events before comparing them to `map_stream`'s output, not only
the three the block names (`raw_line_number`, `raw_byte_offset`, `raw_byte_length`): `schema_version`
and `seq` are also added only by the capture's own `_emit` helper and are never produced by
`normalize_stream_object`, which is the one function DECISION F151 D4 (3) names `map_stream` as built
from. Measured directly: `map_stream`'s output equals the captured events with exactly these five keys
removed, for every one of the five recorded fixtures, with no other difference.

Every placeholder in a `ClaudeCliProvider` raise message (a byte count, an exit code, a free-text
stderr tail, a result subtype, a detail string) is replaced by the literal number `1`, per the block's
own instruction to place "a number" there; the eight distinct message patterns were found by grepping
every `raise` statement inside the `ClaudeCliProvider` class body (lines 881-1556 of
`packages/orchestration/pingpong_provider.py`) and de-duplicating the two raise sites that share the
literal pattern `claude CLI exited {n}: {text}` (`_CliNonZeroExit` and `_StreamNonZeroExit`) and the
three that share `claude CLI timed out after {n}s`.

The kit-run samples (`test_streaming_adapter_passes_every_kit_dimension`,
`test_non_streaming_adapter_passes_every_kit_dimension`) draw their stream lines and usage line from
the recorded `basic_session.jsonl` fixture, as the block asks; their `error_samples` use representative
claude-cli-shaped text rather than text drawn from a fixture file, because none of the five recorded
stream fixtures carries a raw CLI error string — they are `stream-json` event lines, not error
messages. The dedicated error-goldens section separately proves every real `ClaudeCliProvider` message.

No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two test
commands ran at the same time. No merge, no rebase, no amend, no stash, no provider call. No file
outside the paths the block names per commit was touched; in particular no file under
`packages/orchestration/` changed. `git branch --show-current` was run as a standalone command, never
joined to another, before every commit, and read `feature/f151-worker-adapter-contract` every time.

## For the operator, in plain sentences

This round first booked the previous round's review verdict and closed out its last two open items, so
the kit's list of forbidden words and module names can no longer silently lose one of its own tests if
a future change trims that list. It then built the first concrete adapter for the new contract: a
wrapper around the command-building, output-parsing, stream-redaction and error-classifying logic the
local Claude command line already uses today, written so it calls those existing pieces rather than
reimplementing any of them. A large set of comparison tests then checked that wrapper's behavior
against the real functions it wraps, across every recorded sample conversation and every error message
the underlying provider is known to produce, and all of them agreed. The new adapter is not yet wired
into the system that runs real work; that connection, along with removing an older unused interface it
replaces and updating its documentation, is deliberately left for the next piece of work. The round ran
its own selection of tests chosen for this change, not the project's whole test collection, and that
selection, the two style checks and the project's own health check all came back clean.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 4's verdict in the next round's first commit.
4. T003's second half: the import guard, the registry linkage, the deletion of `LLMWorker`, the docs.

Operator questions open: 0. Open findings: 12, gate 5 printed.
