# Handback — F033 · SESSION 2 CLOSE · rounds 5 through 8

> Written by the REVIEWER at the close of session 2 and applied by a worker,
> because the reviewer writes no work-tree file itself. It carries the round 8
> verdict, one finding awaiting registration and two reviewer prose slips.
> Operator amendment amend0827 rule 1: a verdict committed and pushed HERE is
> persisted, and is booked into `.agent/live_review.md` in the FIRST COMMIT of
> the next round that is happening anyway — never in a round of its own.

## Session

SESSION 2 of feature F033 · rounds 5, 6, 7 and 8 delegated · rounds so far 8.
The NEXT session is SESSION 3 of 7 against the amend0827 rule 6 soft limit.
The soft limit is NOT reached: 8 rounds of 25, 2 sessions of 7.

## Range

`7434f54632e75e9d1e86044d8edc7f96c0ef0ae6`..`a2248b7b257efcff4505a2ab3daa71dcd95531c0`
on branch `feature/f033-hunk-approval-v2`. Every round was gated by the reviewer,
which re-ran each round's own gates from scripts of its own and reproduced every
ordered reading before writing a verdict.

## Verdicts

| Round | Subject | Verdict | Ledger entry |
|-------|---------|---------|--------------|
| 5 | closing T001 · staleness repair · DECISION F033 D3 | PASS | `Gate: F033 R5` at `f3a8b0ed` |
| 6 | the approval decision core | PASS | `Gate: F033 R6` at `d887643a` |
| 7 | the approved subset diff | PASS | `Gate: F033 R7` at `6dcbc15e` |
| 8 | landing the subset all-or-nothing | PASS | NOT YET BOOKED — see below |

## Round 8 verdict — PASS, and it is not yet in the ledger

The next round books it. All eight gates were re-executed by the reviewer at
`a2248b7b` and every ordered reading reproduced. TRANSPORT: the C0a blob is 23191
bytes at sha256 `18bc25bd…65061ab3`, byte-identical to the reviewer's own
pre-emission original, ONE blob id at C0b. THE RECORD APPEND at `6dcbc15e`
reconstructs 1466257 plus one newline plus 4877 to 1471135, the committed blob
exactly, base a byte PREFIX, N counted at 1, the last unit equal to the slice's
paragraph, and a byte flipped at offset 1466758 inside that paragraph rejected by
BOTH readers. THE LEDGER: registered 300, `Done:` 45 over 43, `Landed:` 12 and the
open set 257 ALL UNMOVED, `Gate:` 124 to 125, `^Gate: F033 R7 — ` exactly 1. THE
MODULE: `ruff` exits 0; the AST import set holds `hunk_subset_diff`,
`source_apply` and `structured_patch` and NEITHER `permissions` NOR
`approval_queue`, so the "no second permission boundary" claim is measured; the
three codes carry exactly `subset_refused`, `conflict` and `nothing_to_apply`;
and `apply_approved_hunks` and `HunkApplyOutcome` match the ordered signature and
field list. THE MUTATIONS were reproduced in the reviewer's own disposable
worktree at `ee4fbaeb`, the import first proved to resolve inside it: the
UNMUTATED CONTROL is a real exit 0 at 8 passed, reporting success on a failed
apply is exit 1 at 4 failed, calling the applier after a refusal is exit 1 at 1
failed, and flattening the blocked-id attribution is exit 1 at 1 failed. THE
REVIEWER THEN RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED — filling `landed`
with the selected ids on the FAILURE path — and it went RED at 3 failed, so the
"`landed` is empty whenever `applied` is false" contract is genuinely pinned and
not merely written. THE SUITES were re-run SERIALLY, every REAL exit 0:
`test_hunk_apply.py` 8, `test_source_apply.py` 34, `test_hunk_subset_diff.py` 17,
`test_hunk_approval.py` 30, `test_resource_safety.py` 21 and the canary 42. THE
STRUCTURE: six single-parent commits of 341, 223, 16, 2, 207 and 294 insertions,
all under 500, the path set matching in BOTH directions with `.agent/handoff.md`
the sole expected absence, residue 0 in every target, `git ls-files .remedy-wt` 0,
and all seven do-not-touch paths byte-identical across the round. THE WORKER
CORRECTED THE REVIEWER AND WAS RIGHT: the block asserted the synthesised patch
"must set `target_paths` … or it fails validation", and `unsafe_path_issues(())`
returns `[]`, which the reviewer re-ran itself — so the consequence overshot the
measurement. Setting `target_paths` is still correct and was done.

## Awaiting registration — R-0740, drafted here, not yet in the ledger

- R-0740 — Medium, THE APPLY SEAM TELLS AN OPERATOR THE REPOSITORY IS UNCHANGED
IN THE ONE CASE WHERE IT MAY NOT BE. Raised by the reviewer at the F033 R8 gate
by reading `_rollback_from_snapshot` rather than by any gate, and measured at
`a2248b7b`. THE STATE ON DISK: `packages/orchestration/hunk_apply.py`'s failure
return builds its message as the fixed sentence "No approved hunk was applied;
the repository is unchanged. " followed by `"; ".join(result.errors)`. That
sentence is UNCONDITIONAL. But `_rollback_from_snapshot` in
`packages/orchestration/source_apply.py` appends
`"rollback_failed:snapshot_not_found"` when the snapshot cannot be loaded, and
`"rollback_incomplete (N file(s)): …"` when a restore raises `OSError`, and both
land in that same `result.errors`. So in exactly the state where the repository
IS changed — a partial apply whose rollback did not complete — the operator is
told it is unchanged, with the contradicting evidence concatenated after the
claim. WHY MEDIUM RATHER THAN LOW: F033's own Acceptance requires that "every
partial state renders truthfully in viewer and report", and a half-rolled-back
worktree is precisely the partial state this feature exists to render honestly;
the sentence is also the one an operator acts on when deciding whether to
re-diff or to inspect the tree by hand. It is not Higher because `code` is
correct in that case, nothing machine-readable is wrong, and no data is lost.
FIX: derive the sentence from the errors rather than asserting it — when any
error matches the rollback vocabulary, say that the rollback did not complete
and name the files, and reserve "the repository is unchanged" for the case where
it is known. A test for it needs the rollback to fail, which is reachable by
removing the snapshot directory between the apply and the rollback. NOT A GATE
FAILURE of round 8: the block never ordered this message examined, and the
worker wrote exactly what the SPEC described.

## Reviewer prose slips — for `.agent/prose_slips.md`, no id, no round of their own

2026-08-29 · F033 R8 · The block's "TWO CONSTRAINTS" paragraph said a synthesised
patch "must set `target_paths` … or it fails validation", and
`unsafe_path_issues(())` returns `[]`, so an unset `target_paths` would not in
fact fail validation; every measured fact beside it was true and only the
inferred consequence overshot, which the worker re-derived and declared.

2026-08-29 · F033 R8 · The block's G6 ordered the sha256 of "the target file"
before and after the conflict call, in the singular, while a rollback can only be
demonstrated with TWO files — a single-file conflict never reaches the applier's
writer, so equal digests would prove ordering rather than restoration; the worker
built the two-file fixture the property needs and reported both digests.

## What this session built

T001 closed and T002 carried from nothing to a landed, all-or-nothing subset
apply. Four new production modules and suites, every one of them mutation-proved:

| Path | What it decides | Tests |
|------|-----------------|-------|
| `packages/orchestration/hunk_approval.py` | whether a selection is coherent | 30 |
| `packages/orchestration/hunk_subset_diff.py` | WHICH BYTES the selection means | 17 |
| `packages/orchestration/hunk_apply.py` | landing them, all or nothing | 8 |
| `packages/orchestration/hunk_identity.py` | (round 2) the one hunk id | 10 |

DECISION F033 D3 discharged T001's "shared-helper consolidation with diff-repair"
as VACUOUS — `diff_repair.py` holds no hunk identity, its `RepairHunk` selects
spans of current source and names no hunk, and `diff_parser.py` is the only
caller of the shared identity. Recorded as amendment A1 of
`docs/roadmap/features/T5_F033.md`.

## Next expected action — SESSION 3, in this order

1. Read `.agent/STOP` from disk. If it exists, hand off and end (Phase 1 rule 1
   before rule 2 — finding R-0347).
2. Run the Open PR Gate. There was no open PR at the close of session 2.
3. The next round's FIRST commit books, into `.agent/live_review.md`, the round 8
   verdict above and the registration of R-0740, and its second commit appends
   the two prose slips. Neither buys a round of its own.
4. Then the round's real work, which is the plan's step 1: the WRITE DOOR.
   `approve_hunks` becomes UI-exposed and dispatched. The door may NOT import
   the applier — `packages.orchestration.source_apply` is the first entry of
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py` — so the
   command reaches `apply_approved_hunks` through a service seam, and
   `TestCommandDoorImportGuard`'s `ALLOWED_IMPORTS` is an EQUALITY guard that
   must be widened in the SAME commit that adds the import, together with the
   decision that widens it. `UI_EXPOSED_COMMANDS` in
   `apps/cli/command_catalog.py` is pinned at exactly two ids by
   `TestUiExposedCommands`, and exposure without dispatch answers 501.

## Verification of THIS commit

None ordered beyond the reviewer's own: this commit rewrites `.agent/handoff.md`
and nothing else. The worker applying it runs the canary
`pytest tests/cli/test_golden_path.py -q` and reports its REAL exit code, checks
`.agent/STOP` before and after, and leaves `git status --porcelain` empty.
