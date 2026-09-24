# Handback — F264 Steering channel · Round 3 · THE COCKPIT'S STEERING INPUT GOES LIVE: `steeringSend.ts`, the input and its card

## Session

SESSION 1 of feature F264 · round 3 · rounds so far 3

This round booked round 2's PASS into `.agent/live_review.md`, recorded
DECISION F264 D3 (the cockpit's steering input) and two dated
`prose_slips.md` lines, and put the cockpit's steering input live:
`apps/ui/src/api/steeringSend.ts` builds, sends and describes a
`chat.send` through the decision inbox's existing path, nonce and submit
modules; `ChatInput` holds the typed text and announces what became of
each message; `ActivityFeedCard` renders one composer in both branches,
live only for an addressed job that can still run, with two named
disabled reasons otherwise. The design reference's `assumption_log.md`
gained three entries (all DECISION F264 D3), and
`test_brain_stream_ring.py`'s guard class was rewritten to match the now-
live input. A large majority of this session's working-context budget
remained at handback.

## Range

Review of `61e6dd70`..`HEAD`.

## Commits

### c1eee45c F264 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r3-block.md | +251/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f264-r3-plan.md | +30/-0 | Payload copy |
| .agent/authored/f264-r3-records.diff | +57/-0 | Payload copy |

Measured insertions by `git show --numstat`: 338 (251+87), matching the
block's stated formula "this block's line count plus 87" exactly. Under
the 500 cap.

### 1859169e F264 R3 C1b: copy round 3 product diff and mutation tool into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r3-product.diff | +319/-0 | Payload copy |
| .agent/authored/f264-r3-mutations.py | +95/-0 | Payload copy (G5 red-proof tool) |

Measured insertions: 414, matching the block's expected number exactly.
Under the 500 cap.

### 2c3c8a2e F264 R3 C1c: copy round 3 module and test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r3-steeringSend.ts | +182/-0 | Payload copy |
| .agent/authored/f264-r3-steeringSend.test.ts | +179/-0 | Payload copy |
| .agent/authored/f264-r3-test_steering_send_contract.py | +64/-0 | Payload copy |

Measured insertions: 425, matching the block's expected number exactly.
Under the 500 cap.

### 5411ea95 F264 R3 C2: book round 2's PASS, record DECISION F264 D3 and advance the plan

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +29/-0 | `records.diff` applied — DECISION F264 D3 |
| .agent/live_review.md | +2/-0 | `records.diff` applied — the `Gate: F264 R2 —` entry |
| .agent/prose_slips.md | +2/-0 | `records.diff` applied — two dated prose-slip lines |
| .agent/plan.md | +7/-9 | Rewritten to round 3's `plan.md` payload (via `shutil.copyfile`) |

Measured insertions by `git show --numstat`: 29 decisions.md, 2
live_review.md, 7 plan.md, 2 prose_slips.md — matching the block's
expected numbers exactly. Under the 500 cap.

### b54208cb F264 R3 C3: put the cockpit's steering input live in the activity card

| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/steeringSend.ts | +182/-0 | New file, `steeringSend.ts` payload copy |
| apps/ui/src/components/panels/ActivityFeedCard.tsx | +27/-8 | `product.diff` applied |
| apps/ui/src/components/panels/ChatInput.tsx | +59/-23 | `product.diff` applied |
| apps/ui/src/components/panels/RightLivePanel.module.css | +12/-0 | `product.diff` applied |
| apps/ui/src/components/panels/RightLivePanel.tsx | +1/-1 | `product.diff` applied |
| docs/ui/design_reference/assumption_log.md | +5/-1 | `product.diff` applied — three new assumption-log rows |
| tests/ui_contracts/test_brain_stream_ring.py | +23/-21 | `product.diff` applied — the guard class rewritten for the now-live input |

Measured insertions by `git show --numstat`: 182 steeringSend.ts, 27
ActivityFeedCard.tsx, 59 ChatInput.tsx, 12 RightLivePanel.module.css, 1
RightLivePanel.tsx, 5 assumption_log.md, 23 test_brain_stream_ring.py —
matching the block's expected numbers exactly. Under the 500 cap.

### 2f3409fd F264 R3 C4: test the steering sender and pin its rules to the server's

| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/steeringSend.test.ts | +179/-0 | New file, `steeringSend.test.ts` payload copy |
| tests/ui_contracts/test_steering_send_contract.py | +64/-0 | New file, `test_steering_send_contract.py` payload copy |

Measured insertions: 179 steeringSend.test.ts, 64
test_steering_send_contract.py — matching the block's expected numbers
exactly. Under the 500 cap.

### (uncommitted at handback time) F264 R3 C5: rewrite handoff for round 3

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f264-r3-mut 2f3409fd` for G5 —
  real exit 0; removed afterward with `git worktree remove --force
  .remedy-wt/f264-r3-mut` — real exit 0 — and `git worktree prune` — real
  exit 0. `git worktree list` afterward: primary checkout plus the
  reviewer's `.remedy-wt/f264-r3-dry`, `.remedy-wt/f264-r3-sim`, and the
  four pre-existing `.remedy-wt/job-*` worktrees — nothing else, matching
  constraint 6.
- No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.
- `git push origin feature/f264-steering-channel` — ordered after C5; its
  real outcome is reported in the worker's final reply, not in this
  committed file (it has not run yet when this file is written and
  committed as part of C5).

## Verification

**G1 — transport**: each of the seven payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all seven rows matched
exactly. The block itself: 251 lines (newline count), 17375 bytes,
sha256
`f23c077076bc02266f85aca01d3be79523d1ff7bfbe0a2c708c34fafe020f518`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f264-r3-*` blob read with `git show
<commit>:<path>` compared byte-for-byte against its
`.remedy-wt/f264-r3-payloads/` (or block) source: all eight pairs
byte-identical = True.

**G2 — the records**: at C2 (`5411ea95`), `.agent/live_review.md` 313792
bytes, sha256
`fbfd98d1184dbf030c4d8d18f0fd2f8715812b7e8b15ad9b5e53ae59274dbd44`;
`.agent/decisions.md` 1945107 bytes, sha256
`a5871a9e5673d0e9f418017f7c39f563e9a87c95f9f8cd9312335ef0b0d8c019`;
`.agent/prose_slips.md` 365777 bytes, sha256
`ce66ed20b98c517d2f30c08b6fe5e455e06107133c62c463ab3479a2b0a94207`;
`.agent/plan.md` 1088 bytes, sha256
`b25f57bbfbfc1218e250f443ca50a10f5ff71eaf327e0a22cbe6f84f0ef95a78` — all
four equal to the block's table exactly. Among the lines C2's diff adds
to `.agent/live_review.md`, exactly 1 begins `Gate: F264 R2 — `, matching
the reviewer's reading. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 3 at
`61e6dd70` (`R-0499`, `R-0950`, `R-1008`), 3 at C2 (`5411ea95`), same
three ids; both set differences (`base - head`, `head - base`) empty —
matching the block's reading of 3 and 3 exactly. `git diff --name-only
2c3c8a2e 5411ea95`: exactly `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md` — the four record paths C2
writes.

**G3 — the product**: at C4 (`2f3409fd`), each of the nine files read
with `git show 2f3409fd:<path>` equal to the reviewer's simulated
reading — all nine byte counts and sha256 digests matched exactly
(`steeringSend.ts`, `ActivityFeedCard.tsx`, `ChatInput.tsx`,
`RightLivePanel.module.css`, `RightLivePanel.tsx`, `assumption_log.md`,
`test_brain_stream_ring.py`, `steeringSend.test.ts`,
`test_steering_send_contract.py`). `git diff --name-only 5411ea95
b54208cb`: exactly the seven paths C3 lists. `git diff --name-only
b54208cb 2f3409fd`: exactly the two paths C4 lists.

**G4 — the tests**: in the primary checkout at C4, the ordered pytest
selection: `1363 passed, 4 skipped in 82.54s`, real exit 0. All four
`SKIPPED` lines are the pre-existing D3-quarantine skips in
`test_graph_architecture.py` (×2) and `test_ux_quality.py` (×2) — F252
legacy-UI quarantine, unrelated to this round. The four toolchain nodes
the block names (the two in `test_ui_lint.py`, the `tsc --noEmit` node in
`test_dashboard_contract.py`, and the vitest node in
`test_test_runner.py`) all PASSED — none appears in the `-rs` summary.
The reviewer's sim (without golden path, inside a worktree lacking the UI
toolchain) read `1316 passed, 9 skipped`; the primary checkout's run here
includes the golden-path file the reviewer's selection excluded and
carries the UI toolchain a worktree lacks, exactly as the block
anticipates, so the higher pass count and the four resolved toolchain
skips are consistent with that note. `python3 -m ruff check` over the two
named test files: `All checks passed!`, real exit 0. `python3 -m
apps.cli.main integrity check --json`, real exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=149", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

**G5 — the red proofs**: `python3 -B .remedy-wt/f264-r3-payloads/mutations.py
.remedy-wt/f264-r3-mut` against the detached worktree at C4, real exit 0
overall, matching the reviewer's readings on every mutation exactly:
control_before vitest `17 passed` exit 0, pytest `74 passed` exit 0; u1
(every job state open) vitest `2 failed` exit 1, pytest exit 0; u2 (limit
counted in UTF-16 units) vitest `1 failed` exit 1, pytest exit 0; u3
(untrimmed message sent) vitest `1 failed` exit 1, pytest exit 0; u4
(ended job's refusal not named) vitest `1 failed` exit 1, pytest exit 0;
u5 (request built with no job or token) vitest `1 failed` exit 1, pytest
exit 0; p1 (refused message's text cleared) pytest `1 failed` exit 1,
vitest exit 0; p2 (browser's limit drifted from the server's) pytest `1
failed` exit 1, vitest exit 0; p3 (card never closes the input) pytest `1
failed` exit 1, vitest exit 0; control_after as control_before; every
`restored byte-identical` line True.

**G6**: reported in the worker's final reply only, per the block (not in
this committed handback).

## Authored-text proofs

- `.agent/authored/f264-r3-block.md` (C1a) ==
  `.remedy-wt/f264-r3-block.md`: byte-identical True (17375 bytes, 251
  lines, sha256
  `f23c077076bc02266f85aca01d3be79523d1ff7bfbe0a2c708c34fafe020f518`).
- `.agent/authored/f264-r3-plan.md`, `-records.diff` (C1a) == their
  `.remedy-wt/f264-r3-payloads/` sources: byte-identical True, both.
- `.agent/authored/f264-r3-product.diff`, `-mutations.py` (C1b) == their
  payload sources: byte-identical True, both.
- `.agent/authored/f264-r3-steeringSend.ts`, `-steeringSend.test.ts`,
  `-test_steering_send_contract.py` (C1c) == their payload sources:
  byte-identical True, all three.
- `records.diff` was applied at C2 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both real
  exit 0.
- `.agent/plan.md` at C2 == its payload source verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  reading above and the payload table).
- `steeringSend.ts` was copied to `apps/ui/src/api/steeringSend.ts` at C3
  via `shutil.copyfile` — byte-identical to its payload source (confirmed
  by the G3 sha256 reading above).
- `product.diff` was applied at C3 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both real
  exit 0.
- `steeringSend.test.ts` and `test_steering_send_contract.py` were copied
  at C4 via `shutil.copyfile` — byte-identical to their payload sources
  (confirmed by the G3 sha256 readings above).
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied via `git apply` reading the
  payload file directly.

## Assumption-log entries this round

Three rows, all in `product.diff`, all dated 2026-09-24, all attributed
to DECISION F264 D3, landed in `docs/ui/design_reference/assumption_log.md`
at C3 (`b54208cb`):

1. `ActivityFeedCard.tsx` — the reference says the input stays disabled
   until steering exists; shipped instead is a live input for a job that
   can still run, disabled with a named reason otherwise (no job link, or
   an ended job).
2. `ChatInput.tsx` — the reference does not say what the operator sees
   after sending; shipped instead is one line under the input, announced
   to screen readers, using the decision inbox's outcome colours, with the
   typed text cleared only after the job accepts the message.
3. `RightLivePanel.module.css` — the reference names a `--remedy-focus`
   outer ring that is not defined in the shipped tokens sheet; shipped
   instead is the same `--remedy-blue-strong` ring the stylesheet's other
   focus states already use.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 338 insertions, matches block formula (251+87) exactly |
| C1b | done | 414 insertions, matches block exactly |
| C1c | done | 425 insertions, matches block exactly |
| C2 | done | 29/2/2/7 insertions by `git show --numstat`, matches block exactly |
| C3 | done | 182/27/59/12/1/5/23 insertions, matches block exactly |
| C4 | done | 179/64 insertions, matches block exactly |
| C5 | done | this handback commits with it |
| Push | done | ordered after C5; real outcome in the final reply |
| G1 | done | all seven payload readings match; all eight authored copies byte-identical |
| G2 | done | all four sha256/byte readings match; 1 `Gate: F264 R2 — ` line added; open-set 3 at both 61e6dd70 and C2, both differences empty; name-only diff matches |
| G3 | done | all nine C4 files byte/sha match; both name-only diffs (C2..C3, C3..C4) match |
| G4 | done | 1363 passed, 4 skipped, exit 0; the four named toolchain nodes all pass, not skip; ruff all checks passed exit 0; integrity check all six pass, fail_count 0, handlers=149 |
| G5 | done | control_before/after plus u1-u5/p1-p3 all match the reviewer's readings exactly; every restore byte-identical |
| G6 | done | readings reported in the final reply only, per the block |

## Deviations & assumptions

None. Every measured number matched the block's stated expectation
exactly, and the commit sequence landed in the block's exact order
C1a-C1b-C1c-C2-C3-C4-C5. No gate went red. No payload was edited or
retyped; every copy used `shutil.copyfile` and every diff was applied via
`git apply` reading the payload file directly. This round is SESSION 1 of
F264, its third round. No pull request is opened this round (constraint
5): the branch opens one at F264's closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
3, then T002 — consumption at the run's next safe point, with a red proof
that a mid-call message waits. Open findings count: 3. Operator-questions
count: 0.
