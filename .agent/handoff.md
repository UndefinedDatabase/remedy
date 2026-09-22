# Handback — F278 Durable writes & loud failures · Round 5 · Book round 4, T003's first slice

## Session

SESSION 1 of feature F278 · round 5 · rounds so far 5

This round booked round 4's PASS and DECISION F278 D4 into the durable ledger
files, then landed T003's first slice in one product commit:
`packages/orchestration/stream_evidence.py`'s blind exception handlers are
narrowed to the exception each call expects (`OSError` for signalling/closing
an already-gone process, `subprocess.TimeoutExpired` for a wait) or recorded
as a degradation; the stream artifact gains a `degradations` field in
`StreamCaptureResult.to_dict` and as `stream_degraded` events in
`run_events.jsonl`; the one remaining broad handler around the caller-supplied
`on_cap` callback keeps `except Exception` with a `# noqa: BLE001` reason. A
new `TestDegradations` class in `tests/orchestration/test_stream_evidence.py`
covers a clean capture, the on_cap failure path, the after-capture append
path and a real subprocess run with a monkeypatched failing `stderr.close()`.
All five gates (G1–G5) ran clean and matched the reviewer's dry-run readings
exactly (transport, booking, product bytes/BLE001 count, tests, and the four
red-proof mutations). Context self-assessment: a comfortable majority of the
working budget remains at handback.

## Range

Review of `924f7dd6`..`HEAD`.

## Commits

### 94a7443e F278 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r5-block.md | +186/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r5-decisions.md | +36/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r5-ledger.md | +2/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r5-plan.md | +29/-0 | Bookkeeping copy of the plan.md rewrite payload |

Measured insertions: 253 (block 186 + 67 payload lines), under the 500 cap;
matches the block's expected value exactly.

### 0deb8e47 F278 R5 C1b: copy round 5 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r5-mutations.py | +56/-0 | Bookkeeping copy of the G5 mutation-tool payload |
| .agent/authored/f278-r5-stream.diff | +275/-0 | Bookkeeping copy of the stream degradations diff |

Measured insertions: 331 (56+275), matches the block's expected value exactly.

### 77e9177d F278 R5 C2: book round 4's PASS and DECISION F278 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +36/-0 | `decisions.md` appended by byte concatenation |
| .agent/live_review.md | +2/-0 | `ledger.md` appended by byte concatenation |
| .agent/plan.md | +11/-11 | Rewritten to plan.md payload for round 5 |

Measured insertions: 49 (36+2+11), matches the block's expected value exactly.
Deletions: 11, all from the plan.md rewrite.

### 1bea8ec1 F278 R5 C3: record stream capture degradations and narrow its handlers
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/stream_evidence.py | +61/-22 | `_stop_process_tree`'s handlers narrowed to `OSError`/`TimeoutExpired`; `StreamCaptureResult` gains `degradations`; `run_streamed_command` records a failed stderr drain, stdout close, process reap or stderr close as a degradation once the capture is done; `capture_stream_evidence`'s `on_cap` handler records and emits a `stream_degraded` event, keeping `except Exception` with a noqa reason |
| tests/orchestration/test_stream_evidence.py | +78/-0 | New `TestDegradations` class: clean capture, on_cap failure, after-capture append, and a real subprocess run with a failing `stderr.close()` |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 139 (61+78), matches the block's expected value exactly.

### C4 (this commit) F278 R5 C4: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r5-mut 1bea8ec1` — real exit 0.
- `python3 .remedy-wt/f278-r5-payloads/mutations.py .remedy-wt/f278-r5-mut` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r5-mut` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, exit 2, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `924f7dd6 F278 R4 C6: rewrite handoff for round 4`.
- Block bytes (R-0954): measured lines=186, sha256=`09db3e27f1b741a33dcfd4e6c07c98849a9f2e2adf7e2bb75589d1bf2afc9c53`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 5 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (36/2721), ledger.md (2/2939), mutations.py (56/2283), plan.md (29/1058), stream.diff (275/11131). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r5-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 6 copies (block.md + 5 payloads) matched exactly (block.md against `.remedy-wt/f278-r5-block.md`, the other 5 against their `.remedy-wt/f278-r5-payloads/` originals).

G2 THE BOOKING — at C2 (`77e9177d`), the byte counts matched `924f7dd6` bytes plus each payload's bytes by strict concatenation (live_review.md: 433010+2939=435949; decisions.md: 1847094+2721=1849815; plan.md rewritten to 1058), and the sha256 read with `git show 77e9177d:<path>` matched the reviewer's dry-run reading for all three files:
- `.agent/live_review.md`: bytes=435949, sha256=`68313ce3e282ef331c07614bdde29bf4a2abb07483491bd17c4014b54b1ff1fa` — MATCH
- `.agent/decisions.md`: bytes=1849815, sha256=`c77fde5f327391bf0aada4372f53172a7f07164cef3349369eff150892b99e1c` — MATCH
- `.agent/plan.md`: bytes=1058, sha256=`54e1accca56d2146515fe4e2bafdb716691a91fe58d47c6da52c77dff116f58b` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `924f7dd6` count=26; at C2 (`77e9177d`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

Note: `git commit`'s own summary line for C2 read "67 insertions(+), 29 deletions(-)" (a rename/rewrite-detection artifact of the commit-summary diff algorithm against the 1.8MB `.agent/decisions.md` and `.agent/live_review.md` files); the authoritative reading per the block's own instruction (item 8: "each commit's insertion count ... as `git show --numstat` gives it") is `git show --numstat 77e9177d`, which read 36+2+11=49 insertions, 11 deletions — exactly the block's expected value. Reported here per the block's deviation-reporting instinct even though the numbers ultimately match; see Deviations & assumptions.

G3 THE PRODUCT BYTES — at C3 (`1bea8ec1`), sha256 of each file read with `git show 1bea8ec1:<path>`, both MATCH:
- `packages/orchestration/stream_evidence.py`: bytes=36246, sha256=`d284904286486579a191928993996a5c15dc004816dc46285e42c23ebf6eaca4`
- `tests/orchestration/test_stream_evidence.py`: bytes=19788, sha256=`98278280ec8842641cee78b6b1f4e27affd0c0d09de0544586a2f9eb46b3d4c2`

`python3 -m ruff check --select BLE001 packages/orchestration/stream_evidence.py` → `All checks passed!`, real exit 0. (At `924f7dd6` the same command read `Found 11 errors.`, per the reviewer's own measurement — not re-run this round since the block states it as the reviewer's prior reading.)

G4 THE TESTS — command (the block's own, in the primary checkout at C3, WITH `tests/cli/test_golden_path.py` as the block's own command lists it):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_stream_evidence.py tests/orchestration/test_stream_evidence_integration.py tests/orchestration/test_stream_export_e2e.py tests/orchestration/test_event_names.py tests/orchestration/test_event_name_coupling.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `279 passed in 186.64s (0:03:06)`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, WITHOUT the golden path, in a disposable worktree carrying C2 and C3, read `236 passed, 1 skipped` at exit 0; this run's command includes `tests/cli/test_golden_path.py` as the block states it, giving a higher pass count and no reported skip — consistent with the block's own framing ("report what you read").

`python3 -m ruff check` over both files of the G3 table → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency` with `unchecked=0, context_complete=False`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open`). Real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r5-mut 1bea8ec1` real exit 0. `python3 .remedy-wt/f278-r5-payloads/mutations.py .remedy-wt/f278-r5-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
4 passed in 0.26s
m1_on_cap_not_recorded FROM count in file: 1
m1_on_cap_not_recorded REAL_EXIT=1
FAILED tests/orchestration/test_stream_evidence.py::TestDegradations::test_a_failing_cap_callback_is_recorded_in_the_result_and_the_events
1 failed, 3 passed in 0.25s
m1_on_cap_not_recorded restored byte-identical: True
m2_stderr_close_not_recorded FROM count in file: 1
m2_stderr_close_not_recorded REAL_EXIT=1
FAILED tests/orchestration/test_stream_evidence.py::TestDegradations::test_a_failing_stderr_close_reaches_the_run_artifact
1 failed, 3 passed in 0.25s
m2_stderr_close_not_recorded restored byte-identical: True
m3_run_degradations_not_appended FROM count in file: 1
m3_run_degradations_not_appended REAL_EXIT=1
FAILED tests/orchestration/test_stream_evidence.py::TestDegradations::test_a_failing_stderr_close_reaches_the_run_artifact
1 failed, 3 passed in 0.25s
m3_run_degradations_not_appended restored byte-identical: True
m4_to_dict_drops_degradations FROM count in file: 1
m4_to_dict_drops_degradations REAL_EXIT=1
FAILED tests/orchestration/test_stream_evidence.py::TestDegradations::test_a_clean_capture_records_no_degradation
FAILED tests/orchestration/test_stream_evidence.py::TestDegradations::test_a_failing_cap_callback_is_recorded_in_the_result_and_the_events
2 failed, 2 passed in 0.25s
m4_to_dict_drops_degradations restored byte-identical: True
control_after REAL_EXIT=0
4 passed in 0.23s
```
Every reading matches the reviewer's stated expectations exactly: control_before `4 passed`/exit 0; m1 `1 failed, 3 passed`/exit 1 at `test_a_failing_cap_callback_is_recorded_in_the_result_and_the_events`; m2 and m3 each `1 failed, 3 passed`/exit 1 at `test_a_failing_stderr_close_reaches_the_run_artifact`; m4 `2 failed, 2 passed`/exit 1 at `test_a_clean_capture_records_no_degradation` and the on_cap test; control_after `4 passed`/exit 0; every `restored byte-identical` line `True`.

`git worktree remove --force .remedy-wt/f278-r5-mut` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the mutation worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C4). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `c77fde...892b99e1c` == payload sha256 concatenated onto the `924f7dd6` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `68313c...4014b54b1ff1fa` == payload sha256 concatenated onto the `924f7dd6` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `54e1ac...d47dff116f58b` == payload sha256 exactly (G2). MATCH.
- `stream.diff` (applied): `.agent/authored/f278-r5-stream.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C3; resulting files' sha256 at C3 match the G3 table. MATCH.
- `mutations.py`: a TOOL run against the disposable mutation worktree, never applied to a tracked file. `.agent/authored/f278-r5-mutations.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r5-block.md`): `.agent/authored/f278-r5-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r5-block.md` (G1) and to the two readings given in the delegation message.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE PRODUCT BYTES | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | |
| G6 TREE AND PUSH | done | runs after C4; real readings reported in the session's final chat reply, not this file |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3, C4)
exactly, touched exactly the tracked path set the block names, ran no full
suite, and left `.remedy-wt/job-129b3ad7206d4f8d`, its branch, and every
existing stash untouched. One non-load-bearing prose note: `git commit`'s
own one-line summary for C2 read "67 insertions(+), 29 deletions(-)" against
the block's expected 49/11, a rewrite-detection artifact of that command's
own diff algorithm over the two multi-megabyte ledger files; `git show
--numstat 77e9177d`, the reading the block's item 8 actually orders, read
36+2+11=49 insertions and 11 deletions, matching the block exactly. No
finding: no product byte differs, both readings are logged above.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 5,
then T003's marking rounds: the remaining blind handlers, module group by
module group, each narrowed to the exception it expects or marked
`# noqa: BLE001 — <reason>`, with BLE001 joining `select` in `pyproject.toml`
only in the last marking commit once the count of unmarked sites is zero.
Open findings: 26. Operator questions: 0.
