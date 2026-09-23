# Handback — F263 Human-change absorption (absorb) · Round 1 · Claim, re-head, DECISION D1, and T001's foundation

## Session

SESSION 1 of feature F263 · round 1 · rounds so far 1

This round cut `feature/f263-human-change-absorption` from `main` at
`54a23101` (PR 267's merge commit), claimed F263, re-headed the live
review record, recorded DECISION F263 D1 (the human change record's
shape), and landed the first half of T001:
`packages/orchestration/human_change.py`, the target checkout's last
known state recorded on every git job behind its own checkpoint ref, and
the certified human change record written before any re-base, with the
tests and their red proofs. No re-base ships this round. Context
self-assessment: roughly two-thirds of the session's working context
budget remained at handback.

## Range

Review of `54a23101`..`HEAD`.

## Commits

### 22e95530 F263 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r1-block.md | +242/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f263-r1-status.diff | +13/-0 | Payload copy |
| .agent/authored/f263-r1-rehead.diff | +50/-0 | Payload copy |
| .agent/authored/f263-r1-plan.md | +34/-0 | Payload copy |
| .agent/authored/f263-r1-context.md | +45/-0 | Payload copy |
| .agent/authored/f263-r1-decisions.diff | +50/-0 | Payload copy |

Measured insertions: 434 (242 + 13 + 50 + 34 + 45 + 50), matching the
block's stated formula "this block's line count plus 192" (242 + 192 =
434) exactly, per `git show --numstat 22e95530` and `git commit`'s own
report `6 files changed, 434 insertions(+)`. Under the 500 cap.

### e6f912ce F263 R1 C1b: copy round 1 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r1-product.diff | +106/-0 | Payload copy |
| .agent/authored/f263-r1-human_change.py | +255/-0 | Payload copy |
| .agent/authored/f263-r1-mutations.py | +84/-0 | Payload copy |

Measured insertions by `git show --numstat e6f912ce`: 445 (106 + 255 +
84), matching the block's expected 445 exactly.

### a47aa8ef F263 R1 C1c: copy round 1 test payload into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r1-test_human_change.py | +206/-0 | Payload copy |

Measured insertions by `git show --numstat a47aa8ef`: 206, matching the
block's expected 206 exactly.

### 958f7ec2 F263 R1 C2: claim F263 and re-head the live review record

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +17/-18 | `git apply` of rehead.diff |
| docs/roadmap/STATUS.md | +1/-1 | `git apply` of status.diff — F263's line becomes `[~]` (claimed) |
| .agent/plan.md | +21/-14 | Rewritten to the round-1 `plan.md` payload |
| .agent/context.md | +15/-17 | Rewritten to the round-1 `context.md` payload |

Measured insertions by `git show --numstat 958f7ec2`: `15 17
.agent/context.md`, `17 18 .agent/live_review.md`, `21 14 .agent/plan.md`,
`1 1 docs/roadmap/STATUS.md` — matching the block's expected 15, 17, 21, 1
exactly.

### 66078e11 F263 R1 C3: record DECISION F263 D1, the human change record's shape

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +42/-0 | `git apply` of decisions.diff |

Measured insertions by `git show --numstat 66078e11`: 42, matching the
block's expected 42 exactly.

### e60c496d F263 R1 C4: record the target's last known state and certify human changes

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/human_change.py | +255/-0 | New module, copied whole then `git add`ed |
| packages/orchestration/pingpong_job.py | +12/-0 | `git apply` of product.diff — `JobPlan.target_last_known`, export/import, and the capture call in `_create_job_workspace` |
| packages/orchestration/worktrees.py | +12/-3 | `git apply` of product.diff — `write_tree` body moved into new `write_tree_at(path)` so a non-worktree target can be measured |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `git apply` of product.diff — registers the new module (an untracked/unlisted module fails `integrity check`'s `relevant_untracked`) |

Measured insertions by `git show --numstat e60c496d`: `255 0
packages/orchestration/human_change.py`, `12 0
packages/orchestration/pingpong_job.py`, `12 3
packages/orchestration/worktrees.py`, `1 0
tests/orchestration/import_reachability_allowlist.txt` — matching the
block's expected 255, 12, 12, 1 exactly.

### 26c3c8ac F263 R1 C5: test the human change record and the job's last known state

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_human_change.py | +206/-0 | New test file, copied whole then `git add`ed |

Measured insertions by `git show --numstat 26c3c8ac`: 206, matching the
block's expected 206 exactly.

### (this commit) F263 R1 C6: rewrite handoff for round 1

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git checkout -b feature/f263-human-change-absorption` from `main` at
  `54a23101` — created, no pull (Open PR Gate already ran before this
  round; `main` was already at the merge commit).
- `git worktree add --detach .remedy-wt/f263-r1-mut 26c3c8ac` for G5 —
  created.
- `git worktree remove --force .remedy-wt/f263-r1-mut` then `git worktree
  prune` after G5 — removed; `git worktree list` afterward showed only
  the primary checkout and the three `.remedy-wt/job-*` worktrees
  constraint 6 names.
- `git push -u origin feature/f263-human-change-absorption` after C6 —
  real outcome reported in the worker's final reply (G6 readings cannot
  live in this committed file per the block).
- No `gh pr create` — the block orders none; the branch opens its pull
  request at F263's closure.

## Verification

**G1 — transport**: every payload's lines/bytes/sha256 measured against
the block's PAYLOADS table: all nine rows matched exactly (status.diff
13/527, rehead.diff 50/5681, plan.md 34/1463, context.md 45/2166,
decisions.diff 50/3839, product.diff 106/5611, human_change.py 255/9853,
test_human_change.py 206/9046, mutations.py 84/3191 — sha256 digests all
equal to the table). Every committed `.agent/authored/f263-r1-*` blob
read with `git show <commit>:<path>` compared byte-for-byte against its
`.remedy-wt/` source: all ten pairs (the block plus the nine payloads)
byte-identical = True.

**G2 — the bookkeeping**: at C2, `git show 958f7ec2:<path>` sha256 for
`.agent/live_review.md` (371115 bytes), `docs/roadmap/STATUS.md` (47565
bytes), `.agent/plan.md` (1463 bytes) and `.agent/context.md` (2166
bytes), and at C3 `.agent/decisions.md` (1878109 bytes) — all five
byte counts and sha256 digests matched the block's G2 table exactly. Open
finding ids via `scripts/rotate_live_review.py`'s `open_finding_ids` over
the file TEXT: 28 at `54a23101`, 28 at C2, `base - c2 = []`, `c2 - base =
[]` — both differences empty, matching the reviewer's reading of 28 and
28. F263's STATUS line at C2 read in full: `- [~] F263 — Human-change
absorption (absorb)`. `git diff --name-only a47aa8ef 958f7ec2` named
exactly `.agent/context.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md`; `git diff --name-only 958f7ec2 66078e11` named
exactly `.agent/decisions.md` — both matching C2's and C3's path lists.

**G3 — the product**: at C5, `git show 26c3c8ac:<path>` sha256 for
`packages/orchestration/human_change.py` (9853 bytes),
`packages/orchestration/worktrees.py` (31800 bytes),
`packages/orchestration/pingpong_job.py` (195753 bytes),
`tests/orchestration/import_reachability_allowlist.txt` (9903 bytes) and
`tests/orchestration/test_human_change.py` (9046 bytes) — all five byte
counts and sha256 digests matched the block's G3 table exactly.
`git diff --name-only 66078e11 e60c496d` named exactly
`packages/orchestration/human_change.py`,
`packages/orchestration/pingpong_job.py`,
`packages/orchestration/worktrees.py`,
`tests/orchestration/import_reachability_allowlist.txt`;
`git diff --name-only e60c496d 26c3c8ac` named exactly
`tests/orchestration/test_human_change.py` — both matching C4's and C5's
path lists.

**G4 — the tests**, in the primary checkout at C5, serially:
`python3 -m pytest -q -p no:cacheprovider` over the block's 19-file
selection (including the golden path) → `737 passed in 248.04s`, real
exit 0 (`${PIPESTATUS[0]}` read via the pipeline). The reviewer's
disposable-worktree run (without the golden path) read `693 passed, 2
skipped`; the primary checkout carries the UI toolchain a worktree lacks,
so those 2 skips passed here instead, and the golden path file added its
own passing tests on top — no failures, no unexpected skips. Then
`python3 -m ruff check packages/orchestration/human_change.py
packages/orchestration/worktrees.py packages/orchestration/pingpong_job.py
tests/orchestration/test_human_change.py` → `All checks passed!`, real
exit 0. Then `python3 -m apps.cli.main integrity check --json` → all five
checks (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) `pass`, `fail_count: 0`,
`ok: true`, `passed: true`, real exit 0.

**G5 — the red proofs**: `git worktree add --detach .remedy-wt/f263-r1-mut
26c3c8ac` then `python3 -B .remedy-wt/f263-r1-payloads/mutations.py
.remedy-wt/f263-r1-mut`, whole output:
`control_before` `17 passed in 1.68s` exit 0;
`m1_rebase_before_the_record` FROM count 1, `2 failed, 15 passed in
1.65s` exit 1 (`test_the_record_is_on_disk_before_the_rebase_runs`,
`test_a_failed_rebase_leaves_the_record_and_the_hand_edit`), restored
byte-identical True;
`m2_untracked_files_not_captured` FROM count 1, `5 failed, 12 passed in
1.72s` exit 1, restored byte-identical True;
`m3_noise_counted_as_content` FROM count 1, `1 failed, 16 passed in
1.50s` exit 1, restored byte-identical True;
`m4_diff_digest_unchecked` FROM count 1, `1 failed, 16 passed in 1.65s`
exit 1, restored byte-identical True;
`m5_seal_unchecked` FROM count 1, `1 failed, 16 passed in 1.67s` exit 1,
restored byte-identical True;
`m6_record_rewritten` FROM count 1, `1 failed, 16 passed in 1.63s` exit
1, restored byte-identical True;
`m7_job_records_no_state` FROM count 1, `2 failed, 15 passed in 1.70s`
exit 1, restored byte-identical True;
`m8_import_drops_the_state` FROM count 1, `1 failed, 16 passed in 2.01s`
exit 1, restored byte-identical True;
`control_after` `17 passed in 1.94s` exit 0 — every reading exactly
matches the reviewer's simulated readings (m1: 2 failed; m2: 5 failed;
m3–m6, m8: 1 failed each; m7: 2 failed; both controls 17 passed).
`git worktree remove --force .remedy-wt/f263-r1-mut` then `git worktree
prune`, both exit 0; `git worktree list` afterward showed only the
primary checkout plus the three `.remedy-wt/job-*` worktrees.

## Authored-text proofs

- `.agent/authored/f263-r1-block.md` (C1a) == `.remedy-wt/f263-r1-block.md`: byte-identical True.
- `.agent/authored/f263-r1-status.diff` (C1a) == `.remedy-wt/f263-r1-payloads/status.diff`: byte-identical True.
- `.agent/authored/f263-r1-rehead.diff` (C1a) == `.remedy-wt/f263-r1-payloads/rehead.diff`: byte-identical True.
- `.agent/authored/f263-r1-plan.md` (C1a) == `.remedy-wt/f263-r1-payloads/plan.md`: byte-identical True.
- `.agent/authored/f263-r1-context.md` (C1a) == `.remedy-wt/f263-r1-payloads/context.md`: byte-identical True.
- `.agent/authored/f263-r1-decisions.diff` (C1a) == `.remedy-wt/f263-r1-payloads/decisions.diff`: byte-identical True.
- `.agent/authored/f263-r1-product.diff` (C1b) == `.remedy-wt/f263-r1-payloads/product.diff`: byte-identical True.
- `.agent/authored/f263-r1-human_change.py` (C1b) == `.remedy-wt/f263-r1-payloads/human_change.py`: byte-identical True.
- `.agent/authored/f263-r1-mutations.py` (C1b) == `.remedy-wt/f263-r1-payloads/mutations.py`: byte-identical True.
- `.agent/authored/f263-r1-test_human_change.py` (C1c) == `.remedy-wt/f263-r1-payloads/test_human_change.py`: byte-identical True.
- APPLIED text: `packages/orchestration/human_change.py` as committed at
  C4 (`git show e60c496d:packages/orchestration/human_change.py`)
  compared byte-for-byte to the committed `.agent/authored/f263-r1-human_change.py`
  blob and to the source payload: sha256 `09a885ea94200cae771cf754d4ac4d50d3fb5e8b4d2f2c233a59de0c470ce8aa` all three, equal.
- APPLIED text: `tests/orchestration/test_human_change.py` as committed at
  C5 compared byte-for-byte to the committed
  `.agent/authored/f263-r1-test_human_change.py` blob and to the source
  payload: sha256 `e51f21d1d4664e4e45f6eb5ffe895fd7734a8070cdab58b16ceabad57c464ebd`
  all three, equal.
- APPLIED text: `rehead.diff`, `status.diff`, `decisions.diff` and
  `product.diff` were each `git apply --check`ed (exit 0) then `git
  apply`ed (exit 0) unedited, never retyped; G2 and G3's post-apply
  sha256 matches against the reviewer's simulated readings are the
  disk-to-disk proof that the applied bytes equal the payload's bytes.

## Deviations & assumptions

None. The round followed C1a, C1b, C1c, C2, C3, C4, C5 in the block's
exact order, gates G1 through G5 all ran and all passed before C6 was
written, and no payload was edited or retyped.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
1, then T001's second half — the human change record joining the job's
exported evidence and its verification, so a package carries it like any
other artifact. Open findings count: 28, none of them owned by F263.
Operator-questions count: 0.
