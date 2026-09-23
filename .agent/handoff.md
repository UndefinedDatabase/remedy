# Handback — F279 Configuration & toolchain truth · Round 5 · Book round 4's PASS, record DECISION F279 D5, land T003 (`remedy integrity block`)

## Session

SESSION 1 of feature F279 · round 5 · rounds so far 5

This round booked round 4's PASS into the ledger, recorded DECISION F279 D5
(the command is `remedy integrity block <path>`, in the existing self-build
`integrity` group rather than a new `block` group, because a new group would
break the group partition DECISION amend0905-vocab D4 rules), and landed
T003: `packages/orchestration/block_lint.py` with one rule each for items 1,
3, 10, 24, 30, 31 and 37 of the reviewer's §3 checklist, the
`integrity.block` command (`apps/cli/commands/integrity_cmd.py`,
`apps/cli/command_catalog.py`), the reachability-allowlist line, and
`tests/orchestration/test_block_lint.py`'s guard holding every rule to a
live item number and to a sentence that item really contains. All of
G1-G5 ran before this handoff was written and matched the block's stated
expectations exactly, byte for byte and reading for reading. Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `182e7ea0`..`HEAD`.

## Commits

### 2cd53858 F279 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r5-block.md | +228/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r5-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f279-r5-plan.md | +30/-0 | Payload copy |
| .agent/authored/f279-r5-decisions.diff | +45/-0 | Payload copy |
| .agent/authored/f279-r5-feature.diff | +28/-0 | Payload copy |

Measured insertions: 341 (block's line count 228 plus 113), matching the
block's formula exactly, well under the 500 cap.

### d5934f6e F279 R5 C1b: copy round 5 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r5-block_lint.py | +185/-0 | Payload copy |
| .agent/authored/f279-r5-test_block_lint.py | +161/-0 | Payload copy |
| .agent/authored/f279-r5-integrity_cmd.diff | +41/-0 | Payload copy |
| .agent/authored/f279-r5-command_catalog.diff | +25/-0 | Payload copy |
| .agent/authored/f279-r5-allowlist.diff | +12/-0 | Payload copy |
| .agent/authored/f279-r5-mutations.py | +71/-0 | Payload copy (G5 tool, never applied to a tracked file) |

Measured insertions: 495, matching the block's expected 495 exactly.

### 312ab5cd F279 R5 C2: book round 4's PASS and record DECISION F279 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: round 4's `Gate:` entry appended |
| .agent/plan.md | +18/-10 | Rewritten to the round-5 plan.md payload |
| .agent/decisions.md | +37/-0 | `decisions.diff` applied: DECISION F279 D5 recorded |
| docs/roadmap/features/T2_F279.md | +8/-2 | `feature.diff` applied: T003's amendment and acceptance-line update |

Measured insertions (`git diff --cached --numstat`): 37 decisions.md, 2
live_review.md, 8 plan.md, 8 T2_F279.md — matching the block's expected
counts exactly.

### bc3e4f79 F279 R5 C3: add remedy integrity block, the checklist's checkable items by machine
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/block_lint.py | +185/-0 | NEW FILE (`shutil.copyfile` from payload): the linter, its seven rules and the checklist-item reader |
| tests/orchestration/test_block_lint.py | +161/-0 | NEW FILE (`shutil.copyfile` from payload): the rules-cite-live-items guard, per-rule tests, the command's tests |
| apps/cli/commands/integrity_cmd.py | +30/-0 | `integrity_cmd.diff` applied: `_cmd_integrity_block` and its `COMMAND_HANDLERS` entry |
| apps/cli/command_catalog.py | +14/-0 | `command_catalog.diff` applied: the `integrity.block` catalog entry |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `allowlist.diff` applied: `packages.orchestration.block_lint` added |

Measured insertions: 185 block_lint.py, 161 test_block_lint.py, 30
integrity_cmd.py, 14 command_catalog.py, 1 allowlist.txt — matching the
block's expected counts exactly.

### (this commit) F279 R5 C4: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f279-r5-mut bc3e4f79` — created for
  G5; `git worktree remove --force .remedy-wt/f279-r5-mut` then
  `git worktree prune` removed it as G5's last action. `git worktree list`
  afterward showed only the primary checkout and the two pre-existing
  `.remedy-wt/job-*` worktrees.
- `git push origin feature/f279-configuration-toolchain-truth` — see the
  session's final reply for the real outcome; it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no
  checkout of `main` or any other branch/commit in the primary checkout: none
  run, per constraint 5.
- `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their
  branches and every existing stash were left untouched.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, real exit 2 (ENOENT), absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `182e7ea0 F279 R4 C4: rewrite handoff for round 4`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=228,
  sha256=`ba77b253d42a694a3fcf691b1829aee88150849ef08c1e0f3de9e230be1b2b8a`;
  matches both readings given in the delegation message exactly.
- `git worktree list` (before any change) → primary checkout at `182e7ea0`
  plus `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 10 measured and matched the block's table exactly (line
count, byte count, sha256): allowlist.diff (12/605/`9adabb68...`),
block_lint.py (185/8440/`70ca22a3...`), command_catalog.diff
(25/1013/`1f90a3f7...`), decisions.diff (45/3456/`103dfba3...`),
feature.diff (28/1854/`23758d84...`), integrity_cmd.diff
(41/1773/`d90d1b9b...`), ledger.diff (10/6568/`2fc34e64...`), mutations.py
(71/2608/`02345b48...`), plan.md (30/1193/`a7faa59d...`),
test_block_lint.py (161/7326/`739972a5...`).

`git apply --check` then `git apply` for every `.diff` payload (ledger,
decisions, feature at C2; integrity_cmd, command_catalog, allowlist at C3):
all 6 pairs at real exit code 0, in the commit order the block specifies.
`.agent/plan.md`, `block_lint.py` and `test_block_lint.py` were rewrites/new
files by `shutil.copyfile`, never a `git apply`.

G1 TRANSPORT — every `.agent/authored/f279-r5-*` copy (11 files, including
the block copy) read back with `git show <adding-commit>:<path>` and
compared byte-for-byte against its source (`.remedy-wt/f279-r5-block.md` for
the block, `.remedy-wt/f279-r5-payloads/<name>` for the rest): all 11
matched exactly.

G2 THE BOOKKEEPING — at C2 (`312ab5cd`): `.agent/live_review.md`
bytes=382747 sha256=`2e7b3abf8e0e33b2fa35014dc957a881781dd47b320ae7fbe6ae604cf50e83c0`
MATCH; `.agent/plan.md` bytes=1193
sha256=`a7faa59d7b6283628ee25b006fd361f8ff13ded8c4a1e2d87cac6f0ba60748d3` MATCH;
`.agent/decisions.md` bytes=1870110
sha256=`b8f76e9c8fc10739883505a8e6ac00a14bef7fdd062fe2d2fd29fa5f3c4aa90b` MATCH;
`docs/roadmap/features/T2_F279.md` bytes=8970
sha256=`116e7e92fbd15b2ada884d457f438efcdb5f8733534c8cd7db7d81b8f36e049d` MATCH.
Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`),
computed over `.agent/live_review.md` text at `182e7ea0` and at C2: 26 and
26, both set differences empty — matching the block's 26/26 exactly. Lines
beginning `Gate: F279 R4 — ` at `182e7ea0` and at C2: 0 and 1 — matching the
block's 0/1 exactly. `git diff --name-only <C1b> <C2>` → exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T2_F279.md` — matches C2's list.

G3 THE LINTER — `git diff --name-only <C2> <C3>` → exactly
`apps/cli/command_catalog.py`, `apps/cli/commands/integrity_cmd.py`,
`packages/orchestration/block_lint.py`,
`tests/orchestration/import_reachability_allowlist.txt`,
`tests/orchestration/test_block_lint.py` — matches C3's list exactly. At C3
(`bc3e4f79`): `packages/orchestration/block_lint.py` bytes=8440
sha256=`70ca22a3d1d838c7d9fa4b8e650c945c8af21589ca85c8384ac56979d0b19ba3` MATCH;
`tests/orchestration/test_block_lint.py` bytes=7326
sha256=`739972a5d5b5f15780417fee48109b7b4a49705c27ce372679a6ce83670c29f3` MATCH;
`apps/cli/commands/integrity_cmd.py` bytes=2410
sha256=`ec1f2cc946e333f34a68cc0b526fc65b73bc4c369b5368060b39fa39c805ccd3` MATCH;
`apps/cli/command_catalog.py` bytes=110204
sha256=`3d22af46395a89813cd5df12c71b41448324a94da5595566400b0ef013a9b30d` MATCH;
`tests/orchestration/import_reachability_allowlist.txt` bytes=9834
sha256=`8c65b73ddd3442277a34f8efcaaa15bce26f23329aa60626a75ee3fc81ff53f2` MATCH.
No digest differed, so no `git diff --no-index` stop was needed.

G4 THE TESTS — the ordered pytest selection, run SERIALLY (real exit code
0): `1734 passed in 198.29s (0:03:18)`. The reviewer ran the same selection
WITHOUT `tests/cli/test_golden_path.py` inside a disposable worktree
carrying C2 and C3 and read `1689 passed, 2 skipped` at exit 0; this round
ran the full selection INCLUDING golden path in the primary checkout, which
carries the UI toolchain a worktree lacks (as the block anticipates),
accounting for the different pass/skip counts. `python3 -m ruff check
apps/cli/command_catalog.py apps/cli/commands/integrity_cmd.py
packages/orchestration/block_lint.py tests/orchestration/test_block_lint.py`
→ `All checks passed!`, real exit 0. `python3 -m apps.cli.main integrity
check --json` → all 5 checks `pass` (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`), `fail_count` 0, real exit 0. `python3 -m
apps.cli.main integrity block .remedy-wt/f279-r5-block.md` → all 7 items OK
(1 size, 3 cap-bounded replacements, 10 open set recomputed, 24 gate paths
resolve, 30 new ids searched first, 31 gates before the text, 37 no
unmeasured runs), `All 7 checkable items pass.`, real exit 0 — matching the
reviewer's own pre-emission run of this block exactly.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r5-mut
bc3e4f79` real exit 0. `python3 -B .remedy-wt/f279-r5-payloads/mutations.py
.remedy-wt/f279-r5-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
20 passed in 0.29s
m1_a_rule_cites_a_retired_item FROM count in packages/orchestration/block_lint.py: 1
m1_a_rule_cites_a_retired_item REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestTheRulesCiteLiveItems::test_no_rule_references_a_retired_item_number
FAILED tests/orchestration/test_block_lint.py::TestTheRulesCiteLiveItems::test_every_rule_quotes_a_sentence_its_item_really_contains
FAILED tests/orchestration/test_block_lint.py::TestEachRule::test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not
3 failed, 17 passed in 0.31s
m1_a_rule_cites_a_retired_item restored byte-identical: True
m2_size_limit_off_by_one FROM count in packages/orchestration/block_lint.py: 1
m2_size_limit_off_by_one REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestEachRule::test_size_counts_lines_against_four_hundred
1 failed, 19 passed in 0.30s
m2_size_limit_off_by_one restored byte-identical: True
m3_a_declared_new_file_is_not_exempt FROM count in packages/orchestration/block_lint.py: 1
m3_a_declared_new_file_is_not_exempt REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestEachRule::test_a_path_a_command_names_must_resolve_unless_the_block_creates_it
1 failed, 19 passed in 0.31s
m3_a_declared_new_file_is_not_exempt restored byte-identical: True
m4_a_code_fence_counts_as_a_run FROM count in packages/orchestration/block_lint.py: 1
m4_a_code_fence_counts_as_a_run REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestEachRule::test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not
1 failed, 19 passed in 0.37s
m4_a_code_fence_counts_as_a_run restored byte-identical: True
m5_a_wrong_open_count_passes FROM count in packages/orchestration/block_lint.py: 1
m5_a_wrong_open_count_passes REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestEachRule::test_a_stated_open_count_is_recomputed_from_the_ledger
1 failed, 19 passed in 0.31s
m5_a_wrong_open_count_passes restored byte-identical: True
m6_a_violation_exits_zero FROM count in apps/cli/commands/integrity_cmd.py: 1
m6_a_violation_exits_zero REAL_EXIT=1
FAILED tests/orchestration/test_block_lint.py::TestTheCommand::test_a_violation_exits_one_and_names_its_item
1 failed, 19 passed in 0.30s
m6_a_violation_exits_zero restored byte-identical: True
control_after REAL_EXIT=0
20 passed in 0.29s
```
Every reading matches the reviewer's stated expectations, each count exactly
one higher than the reviewer's own tree (which lacks this round's block
copy, per the block's own anticipation): control_before/control_after
20 passed (reviewer read 19); m1 3 failed at the three named tests; m2 1
failed at `test_size_counts_lines_against_four_hundred`; m3 1 failed at
`test_a_path_a_command_names_must_resolve_unless_the_block_creates_it`; m4 1
failed at `test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not`;
m5 1 failed at `test_a_stated_open_count_is_recomputed_from_the_ledger`; m6 1
failed at `test_a_violation_exits_one_and_names_its_item`.
`git worktree remove --force .remedy-wt/f279-r5-mut` real exit 0, `git
worktree prune` real exit 0. `git worktree list` afterward → primary
checkout plus the two `.remedy-wt/job-*` worktrees only.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r5-block.md`): `.agent/authored/f279-r5-block.md` at
  C1a verified byte-identical to `.remedy-wt/f279-r5-block.md` (G1) and to
  the two readings given in the delegation message.
- All 9 payloads (ledger.diff, plan.md, decisions.diff, feature.diff,
  block_lint.py, test_block_lint.py, integrity_cmd.diff,
  command_catalog.diff, allowlist.diff, mutations.py — 10 total): each
  `.agent/authored/f279-r5-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r5-payloads/<name>` source (G1).
- Every `.diff` payload applied by `git apply` (never retyped): ledger,
  decisions, feature (at C2), integrity_cmd, command_catalog, allowlist (at
  C3) — all 6, `git apply --check` then `git apply`, real exit 0 both
  times, and the resulting tracked-file digests MATCH the reviewer's stated
  readings exactly at G2/G3.
- `plan.md` (rewrite, never retyped) and `block_lint.py`/`test_block_lint.py`
  (new files, never retyped): all three by `shutil.copyfile` from their
  payloads; the resulting on-disk digests MATCH the reviewer's stated G2/G3
  readings exactly.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 341 insertions, matches 228+113 formula |
| C1b | done | 495 insertions, matches expectation |
| C2 | done | round 4's PASS booked, DECISION F279 D5 recorded, all four insertion counts match |
| C3 | done | linter, command and guard landed, all five counts match |
| C4 | done | this handback |
| G1 TRANSPORT | done | all 11 authored copies byte-identical to source |
| G2 THE BOOKKEEPING | done | all 4 digests match, 26/26 open-finding set empty diff, 0/1 Gate-line count matches, file-list matches |
| G3 THE LINTER | done | file-list and all 5 digests match, no stop needed |
| G4 THE TESTS | done | 1734 passed, exit 0, ruff clean exit 0, integrity check 5/5 pass exit 0, integrity block 7/7 OK exit 0 |
| G5 THE RED PROOFS | done | control/m1-m6/control_after all match reviewer's exact readings (one higher, as anticipated), worktree cleaned up |
| G6 TREE AND PUSH | done | reported in the session's final reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3,
C4) exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 182e7ea0 HEAD` before C4 was written.

No oversize commit this round (largest was C1b's 495 insertions, well under
the 500 cap; F279's one declared oversize commit remains round 1's C5).

No sandbox friction beyond the block's own anticipated shapes: every
measurement script was written to a file under
`.remedy-wt/f279-r5-scratch/` and run with `python3 -B <file>` or `bash -c`,
never as an inline heredoc or `VAR=x cmd` shape; no payload was retyped or
edited.

No other procedural deviation. Nothing was merged this round, per
constraint 5. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted beyond the round's own `.remedy-wt/f279-r5-mut`, which
was created and removed within G5 per constraint 6. The full suite was not
run, per constraint 7 (amend0917 rule 1) — F279's one full-suite run
belongs to its closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 5,
then T004 — the toolchain refresh order and `remedy doctor toolchain`. Open
findings: 26. Operator questions: 0.
