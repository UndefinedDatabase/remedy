# Handback — F151 round 3

## Session

SESSION 1 of feature F151 · round 3 · rounds so far 3.

Context self-assessment: every prepared file under `.remedy-wt/f151-r3/prep/` was checked against
`digests.txt`'s sha256 (itself checked against the value given in the prompt) before use, the block,
DECISION F151 D2, DECISION F151 D3 and the three findings were read in full before any code was
written, and the repair — the public `adapter_transport_violations`, the whole-MRO walk, the
`FailureClass`-attribute exemption, and one isolated test per kit check — was written from D3's text
directly rather than recalled.

Fortschritt: ~55 % (T001 and T002 landed, T002's repair in review · T003 open) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical, `.agent/authored/f151-r3.md` confirmed equal to `block.md` by `wc -l` (113) and `sha256sum`, staged and committed alone |
| C2 | done | `packages/contracts/adapter_conformance_kit.py` repaired per DECISION F151 D3; committed alone, under the 500-insertion cap, so no split was needed |
| C3 | done | `tests/contracts/test_adapter_conformance_kit.py` rewritten so every `_BROKEN_CASES` entry carries `(dimension, toy, samples, fragment)`; committed alone, under the 500-insertion cap, so no split was needed |
| R-1435 | done | the kit's transport dimension no longer fails an adapter naming `FailureClass.PROVIDER_TIMEOUT` |
| R-1436 | done | the transport dimension now reads every class of the adapter's MRO, not only its own |
| R-1437 | done | every surviving kit check now has its own isolated broken case or direct parametrized test |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C4` read `absent`, last line `ALL True` |
| Gate 2 | done | `run_selection.py` → exit 0, `3307 passed, 2 skipped in 27.46s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 3 | done | `ruff check` → `All checks passed!`; `mypy` → `Success: no issues found in 2 source files` |
| Gate 4 | done | `integrity check --json` → `fail_count` 0, six checks all `pass` |
| Gate 5 | done | `open_finding_ids` → `14` |
| C4 | done | this handback written and committed |
| Push | done | `git push origin feature/f151-worker-adapter-contract` |

## Range

Review of `23b0268fa`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `276f30c90` F151 R3 C1: book round 2, register R-1435 to R-1437, DECISION F151 D3, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r3.md` | +113/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/decisions.md` | +10/-0 | DECISION F151 D3 appended: the whole-MRO transport read, the `FailureClass` exemption, `adapter_transport_violations` |
| `.agent/live_review.md` | +8/-0 | round 2's VERDICT FAIL gate entry booked, R-1435, R-1436 and R-1437 registered |
| `.agent/plan.md` | +2/-3 | rewritten: current step the T002 repair, next step T003 and the closure |

### `6ba76e91d` F151 R3 C2: the transport dimension over the class chain with the failure class exempt

| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_conformance_kit.py` | +20/-5 | `_transport_source_failures` renamed to the public `adapter_transport_violations`, an `Attribute` read off the bare name `FailureClass` exempted from the forbidden-word check, and `_check_transport` rewritten to walk `type(adapter).__mro__`, skipping `object`, `WorkerAdapter` and any class `inspect.getsource` cannot read, prefixing each violation with the class's `__qualname__` |

### `1a93a951f` F151 R3 C3: one test per check of the kit

| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_adapter_conformance_kit.py` | +427/-35 | the two conforming toys now return the `FailureClass` member directly; every `_BROKEN_CASES` entry carries `(dimension, toy, samples, fragment)` and the test asserts both the exact dimension set and a kit-text fragment; one new broken case or custom samples set added per previously-unguarded capabilities, invocation, stream, usage and errors check; the two whole-class transport toys retired in favor of direct parametrized proofs of `adapter_transport_violations` over every forbidden word (as an attribute, an arg, a function name) and every module root (as a name, an import, a from-import), the `FailureClass` exemption and its lookalike, a subclass/base-class case proving the MRO walk, and the two run-level properties (the not-a-`WorkerAdapter` answer in dimension order; capabilities failures before transport failures for one doubly-broken toy) |

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, after this commit.
- No pull request was opened (the block orders none). No worktree was added or removed by this worker.
  No merge, no rebase, no amend. No provider call.

## Verification

Interpreter: the repository's configured Python 3. All five gates were run once each, after C3 and
before C4, per the block.

Gate 1 — `git status --porcelain` → empty. `python3 .remedy-wt/f151-r3/prep/verify.py .` → every line
`True`: all three commits single-parent and under 500 insertions (133, 20, 427), each carries an
`F151 R3 Cn` subject, C3 is not split, on `feature/f151-worker-adapter-contract`, C1's four paths exact
and byte-equal to their `c1-*` snapshots, C2's and C3's paths exact and hold no machine path; `C4` read
`absent` (not yet committed at gate time); the ledger holds no `Landed:`/`Done:` line for R-1435 to
R-1437; last line `ALL True`.

Gate 2 — `python3 .remedy-wt/f151-r3/prep/run_selection.py . .remedy-wt/f151-r3-worker/selection-output.txt`
→ `paths 81`, `exit 0`, `3307 passed, 2 skipped in 27.46s`; the two SKIPPED lines printed verbatim:
`tests/test_install_smoke.py:175` (install smoke is opt-in, no network access set) and
`tests/test_agent_tooling.py:43` (D12 quarantine, F252, a deliberately deleted reviewer contract file).
No FAILED, no ERROR, no `process(es) behind` line.

Gate 3 — `python3 -m ruff check packages/contracts tests/contracts` → `All checks passed!`.
`python3 -m mypy packages/contracts/adapter_contract.py packages/contracts/adapter_conformance_kit.py`
→ `Success: no issues found in 2 source files`.

Gate 4 — `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, six checks all `pass`
(`handler_import` `handlers=197`, `live_review_verdict` `last Gate verdict FAIL`, `plan_consistency`
`unchecked=0, context_complete=False`, `relevant_untracked` `untracked=0, relevant=0`,
`repo_root_hygiene` `no reviewer scratch, evidence dir or archive at the root`, `high_blockers_open`
`no open blocker/high findings`).

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
→ `14`.

## Authored-text proofs

C1's four paths are reviewer-authored or reviewer-produced text applied this round. Each was copied
from its prepared `c1-*` file under `.remedy-wt/f151-r3/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r3-worker/` (`c1_copy.py`), which hashed source and destination with sha256
immediately after the copy; all four pairs read equal. `block.md` itself (saved as
`.agent/authored/f151-r3.md`) was separately confirmed equal to the prepared `block.md` by its sha256
(given in the prompt, checked before any file was used) and again by `wc -l` (113) and `sha256sum`
directly against `block.md`, and a third time by `verify.py`'s own check for that path.
`packages/contracts/adapter_conformance_kit.py` and its test file (C2, C3) are NOT reviewer-authored
text — they were written by this worker from DECISION F151 D3's prose — so no disk-to-disk comparison
applies to them; their own correctness is the gate and self-review-loop checks recorded above.

## Findings landed

Landed: R-1435 — the two conforming toys' `classify_error` return `FailureClass.PROVIDER_TIMEOUT`
directly and `test_conforming_cli_toy_is_fully_conformant`/`test_conforming_http_toy_is_fully_conformant`
prove that attribute no longer fails the transport dimension, `6ba76e91d`.

Landed: R-1436 — `_check_transport` walks every class in `type(adapter).__mro__` that source can be
read for, except `object` and `WorkerAdapter`, so a retry loop inherited from a base class now fails
the dimension too, `6ba76e91d`.

Landed: R-1437 — every surviving kit check now holds its own broken case or direct parametrized test
asserting both the exact dimension and a fragment of that check's own detail text, `1a93a951f`.

## Deviations & assumptions

`_BrokenCapabilitiesWrongTypeToy` returns a dict only on its first `capabilities()` call and a real
`AdapterCapabilities` on every later call: every other dimension's check also calls `capabilities()`,
and a dict returned unconditionally crashes `_check_stream`'s `caps.streaming` read before the stream
dimension's own checks can run, which is not an "exactly its own check" failure. Isolating the broken
answer to the one call the capabilities dimension itself inspects keeps the case targeted, matching
the block's own pattern for the usage-dimension wrong-type cases (an `expected_usage` set equal to the
broken answer, so only the type check fires).

The two whole-class transport toys from round 2 (`_BrokenTransportLoopsOverAttemptsToy`,
`_BrokenTransportNamesSubprocessToy`) are retired rather than kept alongside the new cases: the block
excludes "the transport word and module lists" from the per-check addition it orders, routing that
coverage instead to direct parametrized tests of `adapter_transport_violations` (bullet 4), and a
subclass/base-class case for the MRO property (bullet 5). The retired toys' two properties are not
lost — the base-class case's own base method spells a forbidden word as a plain `Name` (the one
word-check variant bullet 4 does not parametrize directly), and the module-root `Import` case is
covered by the new direct parametrized import test — so removing the old pair trades whole-class,
multi-check proofs for the narrower, per-check ones R-1437 asks for, with no check left unguarded.

No mutation red-proof was run. No full suite was run; the selection gate ran pytest once. No two test
commands ran at the same time. No merge, no rebase, no amend, no stash, no provider call. No file
outside the paths the block names per commit was touched. `git branch --show-current` was run as a
standalone command, never joined to another, before every commit, and read
`feature/f151-worker-adapter-contract` every time.

## For the operator, in plain sentences

This round repaired the conformance kit the previous round's review found wanting in three ways. The
check that looks for retry and timeout machinery inside an adapter's own code was wrongly flagging the
one enum value every adapter must be able to name for a timeout, so a correctly written adapter could
never fully pass; that check now carves out exactly that one reading and nothing else. The same check
only ever looked at an adapter's own class body, so a retry loop quietly inherited from a shared base
class would slip through; it now walks the adapter's whole class lineage instead. Finally, a large
share of the kit's individual checks had no test of their own, so a check could be deleted entirely
and nothing would notice; every one of those checks now has a dedicated case proving it fires, and
proving it fires for the right reason rather than merely in the right general area. The round ran its
own selection of tests chosen for this change, not the project's whole test collection, and that
selection, the two style checks and the project's own health check all came back clean.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. The Open PR Gate, run at the start of the next session before any new branch.
3. Book round 3's verdict in the next round's first commit.
4. T003: the reference adapter, the import guard, the registry linkage.

Operator questions open: 0. Open findings: 14, gate 5 printed (`R-1246`, `R-1281`, `R-1326`, `R-1351`,
`R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427`, `R-1428`, `R-1435`, `R-1436` and `R-1437`).
