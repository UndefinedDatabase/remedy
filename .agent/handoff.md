# Handback — F264 Steering channel · Round 4 · A STEERING MESSAGE IS CONSUMED AT THE NEXT ROUND'S SAFE POINT, EXACTLY ONCE

## Session

SESSION 1 of feature F264 · round 4 · rounds so far 4

This round booked round 3's PASS into `.agent/live_review.md`, recorded
DECISION F264 D4 (the consumption point, marker, event and prompt
segment), and landed T002: `run_pingpong` now reads pending steering
messages as its own step directly after each round's first safe point —
never through `stop_check`, which also fires inside a call — consumes
each exactly once through a sealed, create-once marker naming its task
and round, writes a `steering_message_consumed` event, and carries every
consumed message verbatim in the builder prompt's new `builder_steering`
segment. `tests/orchestration/test_steering.py` gained two new test
classes and `tests/orchestration/test_steering_consumption.py` is a new
acceptance file comparing round 2's prompt with and without a message
sent while round 1's call was in flight. A large majority of this
session's working-context budget remained at handback.

## Range

Review of `889c556b`..`HEAD`.

## Commits

### 4fcaf619 F264 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r4-block.md | +226/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f264-r4-plan.md | +31/-0 | Payload copy |
| .agent/authored/f264-r4-records.diff | +51/-0 | Payload copy |

Measured insertions by `git show --numstat`: 308 (226+82), matching the
block's stated formula "this block's line count plus 82" exactly. Under
the 500 cap.

### 3fc2fd96 F264 R4 C1b: copy round 4 product diff and mutation tool into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r4-mutations.py | +73/-0 | Payload copy (G5 red-proof tool) |
| .agent/authored/f264-r4-product.diff | +235/-0 | Payload copy |

Measured insertions: 308, matching the block's expected number exactly.
Under the 500 cap.

### be313874 F264 R4 C1c: copy round 4 test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r4-test_steering_consumption.py | +121/-0 | Payload copy |
| .agent/authored/f264-r4-tests.diff | +77/-0 | Payload copy |

Measured insertions: 198, matching the block's expected number exactly.
Under the 500 cap.

### 50ef5486 F264 R4 C2: book round 3's PASS, record DECISION F264 D4 and advance the plan

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +33/-0 | `records.diff` applied — DECISION F264 D4 |
| .agent/live_review.md | +2/-0 | `records.diff` applied — the `Gate: F264 R3 —` entry |
| .agent/plan.md | +9/-8 | Rewritten to round 4's `plan.md` payload (via `shutil.copyfile`) |

Measured insertions by `git show --numstat`: 33 decisions.md, 2
live_review.md, 9 plan.md — matching the block's expected numbers
exactly. Under the 500 cap.

### be8454f5 F264 R4 C3: consume steering at the top of each round and carry it in the prompt

| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | +1/-0 | `product.diff` applied |
| packages/orchestration/event_names.py | +1/-0 | `product.diff` applied — `steering_message_consumed` event name |
| packages/orchestration/pingpong_loop.py | +32/-0 | `product.diff` applied — consumption at the round's first safe point |
| packages/orchestration/steering.py | +118/-4 | `product.diff` applied — marker, consumption and `builder_steering` segment |

Measured insertions by `git show --numstat`: 1 humanizeCatalog.ts, 1
event_names.py, 32 pingpong_loop.py, 118 steering.py — matching the
block's expected numbers exactly. Under the 500 cap.

### 5c173e7f F264 R4 C4: prove a mid-call message waits for the next round and steers it

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_steering.py | +69/-0 | `tests.diff` applied — two new test classes |
| tests/orchestration/test_steering_consumption.py | +121/-0 | New file, payload copy — the acceptance fixture |

Measured insertions: 69 test_steering.py, 121
test_steering_consumption.py — matching the block's expected numbers
exactly. Under the 500 cap.

### (uncommitted at handback time) F264 R4 C5: rewrite handoff for round 4

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f264-r4-mut 5c173e7f` for G5 —
  real exit 0; removed afterward with `git worktree remove --force
  .remedy-wt/f264-r4-mut` — real exit 0 — and `git worktree prune` — real
  exit 0. `git worktree list` afterward: primary checkout plus the
  reviewer's `.remedy-wt/f264-r4-dry`, `.remedy-wt/f264-r4-sim`, and the
  four pre-existing `.remedy-wt/job-*` worktrees — nothing else, matching
  constraint 6.
- No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.
- `git push origin feature/f264-steering-channel` — ordered after C5; its
  real outcome is reported in the worker's final reply, not in this
  committed file (it has not run yet when this file is written and
  committed as part of C5).

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256 measured
against the block's PAYLOADS table — all six rows matched exactly. The
block itself: 226 lines (newline count), 15774 bytes, sha256
`039ca2b52bc1c111a2c110df3067bfb5bb872b8cb5d0bf7cea926d85733c979f`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f264-r4-*` blob read with `git show
<commit>:<path>` compared byte-for-byte against its
`.remedy-wt/f264-r4-payloads/` (or block) source: all seven pairs
byte-identical = True.

**G2 — the records**: at C2 (`50ef5486`), `.agent/live_review.md` 316339
bytes, sha256
`02e44b2e6f79bc99cedf4a794361b26a56dfa5f1ead9063a79b8c7101aae6f95`;
`.agent/decisions.md` 1948088 bytes, sha256
`c8b9d4ce7da60338e385c206fd5fc66b3bd1b163f57de56b2f54fe853ce1b7f8`;
`.agent/plan.md` 1238 bytes, sha256
`08b916e270dc80ba485c3eb59b77c95a7a641bf94dae556c127b9faacd079833` — all
three equal to the block's table exactly. Among the lines C2's diff adds
to `.agent/live_review.md`, exactly 1 begins `Gate: F264 R3 — `, matching
the reviewer's reading. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 3 at
`889c556b` (`R-0499`, `R-0950`, `R-1008`), 3 at C2 (`50ef5486`), same
three ids; both set differences (`base - head`, `head - base`) empty —
matching the block's reading of 3 and 3 exactly. `git diff --name-only
be313874 50ef5486`: exactly `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md` — the three record paths C2 writes.

**G3 — the product**: at C4 (`5c173e7f`), each of the six files read with
`git show 5c173e7f:<path>` equal to the reviewer's simulated reading —
all six byte counts and sha256 digests matched exactly
(`humanizeCatalog.ts`, `event_names.py`, `pingpong_loop.py`,
`steering.py`, `test_steering.py`, `test_steering_consumption.py`). `git
diff --name-only 50ef5486 be8454f5`: exactly the four paths C3 lists.
`git diff --name-only be8454f5 5c173e7f`: exactly the two paths C4 lists.

**G4 — the tests**: in the primary checkout at C4, the ordered pytest
selection: `770 passed in 102.99s`, real exit 0. The reviewer's sim (no
golden path, serially, inside a worktree lacking the UI toolchain) read
`726 passed, 2 skipped`; the primary checkout's run here includes the
golden-path file the reviewer's selection excluded and carries the UI
toolchain a worktree lacks, exactly as the block anticipates, so the
higher pass count and zero skips here are consistent with that note.
`python3 -m ruff check` over the five named product/test files: `All
checks passed!`, real exit 0. `python3 -m apps.cli.main integrity check
--json`, real exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=149", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

**G5 — the red proofs**: `python3 -B .remedy-wt/f264-r4-payloads/mutations.py
.remedy-wt/f264-r4-mut` against the detached worktree at C4, real exit 0
overall, matching the reviewer's readings on every mutation exactly:
control_before `37 passed` exit 0; m1 (the loop never reads steering) `4
failed` exit 1; m2 (the steering segment never registered) `3 failed`
exit 1; m3 (a message consumed again every round) `2 failed` exit 1; m4
(the consumption round recorded one early) `4 failed` exit 1; m5 (a
consumption marker's seal never checked) `1 failed` exit 1; m6 (only
newly consumed messages carried, so a correction is forgotten) `2 failed`
exit 1; control_after `37 passed` exit 0; every `restored byte-identical`
line True.

**G6**: reported in the worker's final reply only, per the block (not in
this committed handback).

## Authored-text proofs

- `.agent/authored/f264-r4-block.md` (C1a) ==
  `.remedy-wt/f264-r4-block.md`: byte-identical True (15774 bytes, 226
  lines, sha256
  `039ca2b52bc1c111a2c110df3067bfb5bb872b8cb5d0bf7cea926d85733c979f`).
- `.agent/authored/f264-r4-plan.md`, `-records.diff` (C1a) == their
  `.remedy-wt/f264-r4-payloads/` sources: byte-identical True, both.
- `.agent/authored/f264-r4-product.diff`, `-mutations.py` (C1b) == their
  payload sources: byte-identical True, both.
- `.agent/authored/f264-r4-tests.diff`,
  `-test_steering_consumption.py` (C1c) == their payload sources:
  byte-identical True, both.
- `records.diff` was applied at C2 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both real
  exit 0.
- `.agent/plan.md` at C2 == its payload source verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  reading above and the payload table).
- `product.diff` was applied at C3 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both real
  exit 0.
- `tests.diff` was applied at C4 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both real
  exit 0.
- `test_steering_consumption.py` was copied at C4 via `shutil.copyfile`
  — byte-identical to its payload source (confirmed by the G3 sha256
  reading above).
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied via `git apply` reading
  the payload file directly.

## Deviations & assumptions

None. Every measured number matched the block's stated expectation
exactly, and the commit sequence landed in the block's exact order
C1a-C1b-C1c-C2-C3-C4-C5. No gate went red. No payload was edited or
retyped; every copy used `shutil.copyfile` and every diff was applied via
`git apply` reading the payload file directly. This round is SESSION 1 of
F264, its fourth round. No pull request is opened this round (constraint
5): the branch opens one at F264's closure.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 308 insertions, matches block formula (226+82) exactly |
| C1b | done | 308 insertions, matches block exactly |
| C1c | done | 198 insertions, matches block exactly |
| C2 | done | 33/2/9 insertions by `git show --numstat`, matches block exactly |
| C3 | done | 1/1/32/118 insertions, matches block exactly |
| C4 | done | 69/121 insertions, matches block exactly |
| C5 | done | this handback commits with it |
| Push | done | ordered after C5; real outcome in the final reply |
| G1 | done | all six payload readings match; all seven authored copies byte-identical |
| G2 | done | all three sha256/byte readings match; 1 `Gate: F264 R3 — ` line added; open-set 3 at both 889c556b and C2, both differences empty; name-only diff matches |
| G3 | done | all six C4 files byte/sha match; both name-only diffs (C2..C3, C3..C4) match |
| G4 | done | 770 passed, exit 0; ruff all checks passed exit 0; integrity check all six pass, fail_count 0, handlers=149 |
| G5 | done | control_before/after plus m1-m6 all match the reviewer's readings exactly; every restore byte-identical |
| G6 | done | readings reported in the final reply only, per the block |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
4, then T002's mission half — a consumed message for a job that belongs
to a mission also amends the mission's contract. Open findings count: 3.
Operator-questions count: 0.
