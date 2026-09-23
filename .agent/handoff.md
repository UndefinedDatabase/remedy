# Handback — F263 Human-change absorption (absorb) · Round 6 · Book round 5's PASS, record DECISION F263 D6, land T003's apply half — PASS, end of session 1

## Session

SESSION 1 of feature F263 · round 6 · rounds so far 6

This round ends session 1 of F263. It booked round 5's PASS into the
ledger with DECISION F263 D6 (C2), then landed T003's apply half in one
commit (C3): `apply_job` now absorbs a hand edit before a single file is
copied — the drift block that stood on `job.target_guard.target_mutated`
is gone, replaced by `HC.absorb_job(job, detected_by="apply")` followed by
`HC.recorded_human_changes(job.job_id)`; the resulting path set is
threaded through `_apply_from_workspace` as `human_changed`, and when the
baseline-clean check fails on a path in that set the apply is blocked with
`human_change_conflict: <path> ... changed by hand since the job's last
known state and changed by the job too; the apply stops rather than
overwrite either side (DECISION D-E of T2_F263.md)`. With C3, every slice
of F263 — T001, T002 and T003 — has landed. G1 through G5 all ran and
every reading matched the block's stated expectation, including the
old-behaviour red proof (`old_apply`, `job_apply.py` restored to its
`5fd8b648` bytes, 5 failed) and the existing test
`TestDryRunTargetMutation` in `tests/orchestration/test_job_apply.py`,
renamed by product.diff to
`test_a_recorded_target_mutation_no_longer_blocks_by_itself` and now
asserting the flag alone refuses nothing (DECISION F263 D6 (4)). The
pytest count read in G4 (571 passed, 0 skipped) reflects the block's own
ordered command, which includes `tests/cli/test_golden_path.py`, unlike
the reviewer's disposable-worktree dry run which explicitly excluded it
and read 527 passed, 2 skipped — no failures either way, reported as read
per the block's own instruction and the identical pattern at rounds 3, 4
and 5. Context self-assessment: a large majority of the session's working
context budget remained at handback.

## Range

Review of `5fd8b648`..`HEAD`.

## Commits

### f14bf413 F263 R6 C1a: copy round 6 block, bookkeeping payloads and red-proof tool

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r6-block.md | +191/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f263-r6-ledger.md | +2/-0 | Payload copy |
| .agent/authored/f263-r6-decisions.md | +34/-0 | Payload copy |
| .agent/authored/f263-r6-plan.md | +30/-0 | Payload copy |
| .agent/authored/f263-r6-mutations.py | +80/-0 | Payload copy (G5 tool) |

Measured insertions by `git show --numstat f14bf413`: 337 (191+2+34+30+80),
matching the block's stated formula "this block's line count plus 146"
(191 + 146 = 337) exactly. Under the 500 cap.

### 41d3a8d6 F263 R6 C1b: copy round 6 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r6-product.diff | +128/-0 | Payload copy |
| .agent/authored/f263-r6-test_human_change_at_apply.py | +156/-0 | Payload copy |

Measured insertions by `git show --numstat 41d3a8d6`: 284 (128+156),
matching the block's expected 284 exactly.

### 44e6426c F263 R6 C2: book round 5's PASS and DECISION F263 D6

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +34/-0 | Append of decisions.md payload (DECISION F263 D6) |
| .agent/live_review.md | +2/-0 | Append of ledger.md payload (round 5's PASS entry) |
| .agent/plan.md | +10/-10 | Rewritten to the round-6 `plan.md` payload |

Measured insertions by `git show --numstat 44e6426c`: `34 0
.agent/decisions.md`, `2 0 .agent/live_review.md`, `10 10 .agent/plan.md`
— matching the block's expected 34, 2, 10 exactly.

### 8e131568 F263 R6 C3: absorb before every apply and name a hand edit the job also changed

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/human_change.py | +15/-0 | `git apply` of product.diff — new `recorded_human_changes(job_id, root=None)` helper reading every intact human-change record's paths |
| packages/orchestration/job_apply.py | +30/-4 | `git apply` of product.diff — the drift block on `target_guard.target_mutated` deleted; `HC.absorb_job` runs before file copy; `human_changed` threaded into `_apply_from_workspace`; a baseline-clean failure on a human-changed path is reported as `human_change_conflict` |
| tests/orchestration/test_human_change_at_apply.py | +156/-0 | New file, copied whole from test_human_change_at_apply.py payload |
| tests/orchestration/test_job_apply.py | +6/-2 | `git apply` of product.diff — `TestDryRunTargetMutation` renamed and repinned: the flag alone refuses nothing |

Measured insertions by `git show --numstat 8e131568`: 15, 30, 156, 6 —
matching the block's expected 15/30/156/6 exactly (207 total insertions,
6 deletions). `git apply --check` then `git apply` for product.diff: real
exit 0, 0. New test file `git add`ed before commit.

### (this commit) F263 R6 C4: rewrite handoff for round 6, the end of session 1

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f263-r6-mut 8e131568` (at C3) for
  G5: real exit 0.
- `git worktree remove --force .remedy-wt/f263-r6-mut`: real exit 0.
  `git worktree prune`: real exit 0.
- No `gh pr create`, no merge, no branch deletion — none ordered, none
  taken.
- `git push origin feature/f263-human-change-absorption` after C4 — real
  outcome reported in the worker's final reply (G6 readings cannot live
  in this committed file per the block).

## Verification

**G1 — transport**: every payload's lines/bytes/sha256 measured against
the block's PAYLOADS table: all six rows matched exactly (ledger.md
2/1944, decisions.md 34/2618, plan.md 30/1162, mutations.py 80/3086,
product.diff 128/6349, test_human_change_at_apply.py 156/6714 — sha256
digests all equal to the table). Every committed `.agent/authored/f263-r6-*`
blob read with `git show <commit>:<path>` compared byte-for-byte against
its `.remedy-wt/` source: all seven pairs (the block plus the six
payloads) byte-identical = True, sha256 equal to the table in every case.

**G2 — the booking**: pre-C2 `.agent/live_review.md` (381945 bytes) +
ledger.md payload (1944 bytes) = 383889 bytes, matching `git show
44e6426c:.agent/live_review.md` sha256
`3dac4145b65da0ca21f3a01ebd6076a2b160d0efceea5ad044035f2f310bff8a`
exactly. Pre-C2 `.agent/decisions.md` (1888999 bytes) + decisions.md
payload (2618 bytes) = 1891617 bytes, matching sha256
`babb8bf798b0243eea3b1ceba616465881161a1dad1e17d0b5d36f6267e26e7f`
exactly. `.agent/plan.md` at C2 equals plan.md payload: 1162 bytes, sha256
`aa2b56a82505783e5e542575fad30c40e9aeda653cfff3be4ff0657951330f23` — all
three match the block's reviewer-simulated table exactly. Open finding
ids via `scripts/rotate_live_review.py`'s `open_finding_ids(text)` read
against `.agent/live_review.md`: at base `5fd8b648`, count 28 (distinct
28); at C2 `44e6426c`, count 28 (distinct 28); both set differences
empty — matching the block's reading of 28, 28, both empty exactly.

**G3 — the product bytes**: at C3 (`8e131568`), `git show 8e131568:<path>`
for all four paths in the block's table — bytes and sha256 both matched
exactly:

| path | bytes | sha256 | match |
|---|---|---|---|
| packages/orchestration/job_apply.py | 104131 | 4fc9af0b4437308fce72ce95882f64f950d56b678dc0fd8fafa9085060bfc1f5 | True |
| packages/orchestration/human_change.py | 14217 | 887b418a9e0c7742746aa537933d1dcc45f6fcef0087398c6cc439a0cbc5d60b | True |
| tests/orchestration/test_job_apply.py | 93177 | 03ed1c5eddcaefd9c0be31c80824e0076a3ca38fca737649dff44afca2261d9e | True |
| tests/orchestration/test_human_change_at_apply.py | 6714 | 968665d74ef7d81543a1c37a97cfa0ea69ff222a0f5b07c345b1f09388970731 | True |

All four pairs equal the block's table.

**G4 — the tests and the lint, ALL PASSING**: in the primary checkout at
C3, SERIALLY: `python3 -m pytest -q -p no:cacheprovider` over the block's
exact 21-path selection (including `tests/cli/test_golden_path.py`, which
the block's own G4 command orders here, unlike the reviewer's disposable-
worktree dry run which explicitly excluded it) → `571 passed in 427.83s`,
real exit 0 (`PIPESTATUS[0]`). The reviewer's own run (without the golden
path, in a disposable worktree) read `527 passed, 2 skipped` at exit 0; my
run read 0 skipped and 44 more passing tests — the golden path's own tests
plus this primary checkout's environment account for the delta; no
failures either way, so this is reported as read, not treated as a red
gate (the block orders "report what you read", as it did at rounds 3, 4
and 5 for the identical pattern). Then `python3 -m ruff check .` over the
WHOLE repository from its root: `All checks passed!`, real exit 0.
`python3 -m apps.cli.main integrity check --json`: all five checks
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) `pass`, `fail_count: 0`,
`ok: true`, `passed: true`, real exit 0.

**G5 — the red proofs, all matching**: `git worktree add --detach
.remedy-wt/f263-r6-mut 8e131568` real exit 0; `python3 -B
.remedy-wt/f263-r6-payloads/mutations.py .remedy-wt/f263-r6-mut 5fd8b648`,
real exit 0 overall: `control_before` `94 passed` exit 0; `old_apply`
(`job_apply.py` restored to its `5fd8b648` bytes) 5 failed exit 1, naming
`TestTheSecondDemoCase::test_a_hand_edit_after_the_run_is_absorbed_and_kept_by_the_apply`,
`TestAHandEditTheJobMeetsStopsTheApply::test_after_the_run_it_is_refused_and_named`,
`TestAHandEditTheJobMeetsStopsTheApply::test_during_the_run_it_is_refused_and_named_too`,
`TestAFailedAbsorptionStopsTheApply::test_the_apply_is_refused_with_the_reason_and_copies_nothing`,
`TestDryRunTargetMutation::test_a_recorded_target_mutation_no_longer_blocks_by_itself`
— the OLD behaviour, restored byte-identical True; `m1_apply_absorbs_nothing`
3 failed exit 1; `m2_conflicts_not_named` 2 failed exit 1;
`m3_a_failed_absorption_does_not_block` 1 failed exit 1;
`m4_the_drift_block_back` 1 failed exit 1;
`m5_unverified_records_counted` 1 failed exit 1; `control_after` `94
passed` exit 0; every `restored byte-identical` line `True` (7 of 7) —
matching the block's table of 5(old)/3/2/1/1/1 exactly. Then `git
worktree remove --force .remedy-wt/f263-r6-mut` (real exit 0), `git
worktree prune` (real exit 0); `git worktree list` after: primary
checkout at `8e131568` plus the three `.remedy-wt/job-*` worktrees only
(`09441a92`, `cc8696a3`, `03d435e5`) — no new worktree or branch left
behind (R-0940).

## Authored-text proofs

- `.agent/authored/f263-r6-block.md` (C1a) == `.remedy-wt/f263-r6-block.md`: byte-identical True (sha256 `ee0452ad648b1514160d5967ea803910772222b3f3f54e12891efd3bd19160c9`, 191 lines).
- `.agent/authored/f263-r6-ledger.md` (C1a) == `.remedy-wt/f263-r6-payloads/ledger.md`: byte-identical True (1944 bytes).
- `.agent/authored/f263-r6-decisions.md` (C1a) == `.remedy-wt/f263-r6-payloads/decisions.md`: byte-identical True (2618 bytes).
- `.agent/authored/f263-r6-plan.md` (C1a) == `.remedy-wt/f263-r6-payloads/plan.md`: byte-identical True (1162 bytes).
- `.agent/authored/f263-r6-mutations.py` (C1a) == `.remedy-wt/f263-r6-payloads/mutations.py`: byte-identical True (3086 bytes).
- `.agent/authored/f263-r6-product.diff` (C1b) == `.remedy-wt/f263-r6-payloads/product.diff`: byte-identical True (6349 bytes).
- `.agent/authored/f263-r6-test_human_change_at_apply.py` (C1b) == `.remedy-wt/f263-r6-payloads/test_human_change_at_apply.py`: byte-identical True (6714 bytes).
- APPLIED text: `product.diff` was `git apply --check`ed (exit 0) then
  `git apply`ed (exit 0) unedited, never retyped; G3's post-apply sha256
  match against the block's table is the disk-to-disk proof that the
  applied bytes equal the payload's bytes. `test_human_change_at_apply.py`
  was copied whole via `shutil.copyfile` to its landing path, then read
  back at C3 in G3 — byte-identical to its payload.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 337 insertions, matches block formula (191+146) |
| C1b | done | 284 insertions, matches block exactly |
| C2 | done | 34/2/10 insertions, matches block exactly; G2 fully passed |
| C3 | done | 15/30/156/6 insertions, matches block exactly; G3 fully passed |
| C4 | done | this handback |
| G1 | done | all readings match |
| G2 | done | all readings match; open-set 28 at base and at C2, both differences empty |
| G3 | done | all readings match |
| G4 | done | pytest 571 passed, exit 0 (deviation from reviewer's 527/2-skipped explained, not a red gate); ruff `All checks passed!` exit 0; integrity check all-pass exit 0 |
| G5 | done | mutations.py: old_apply 5 failed (OLD behaviour), m1-m5 3/2/1/1/1 failures exit 1, controls 94 passed exit 0, all 7 restores byte-identical |
| T003 apply half | done | apply-time absorption before file copy, drift block deleted, hand-edit conflicts named; landed at C3; proved by G3 (bytes) and G5 (red proofs including the old-behaviour proof) |
| T003 (T001-T003 complete) | done | with C3, every slice of F263 has landed |

## Deviations & assumptions

None from the block's ordered commit sequence: bytes verified before use,
the five-commit bundle landed in order C1a-C1b-C2-C3-C4, no payload was
edited or retyped, G1 through G5 all ran and every reading matched the
block's stated expectation. One reported-not-treated-as-deviation note:
G4's pytest count read `571 passed` (0 skipped) against the reviewer's
disposable-worktree reading of `527 passed, 2 skipped` — expected, since
the block's own G4 command includes `tests/cli/test_golden_path.py` while
the reviewer explicitly ran "WITHOUT the golden path"; no failures in
either reading, and the block itself says "report what you read" rather
than asserting the reviewer's count would recur (the identical pattern
occurred at rounds 3, 4 and 5). No other worktree, branch or stash was
touched. This round ends session 1 of F263.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR Gate (no
pull request is open for this branch), then the review of round 6 by
session 2's reviewer, then the closure sequence's first round — the Built
State in `docs/roadmap/features/T2_F263.md`, the closure's self-use item,
and the feature's one full-suite run. Open findings count: 28. Operator-
questions count: 0.
