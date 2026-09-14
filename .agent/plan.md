# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 101 IS THE FLIP ROUND, per operator amendment amend0914-f275-sprint. One bookkeeping
commit books the round 100 verdict, registers as `R-0884` the structured acceptance form that
DECISION F275 D22 left to the flip, and records DECISION F275 D75, under which the eleven thin
sites of DECISION F275 D48 are re-checked by their own witnesses before the flip. The next
commit is THE FLIP: the transform in the primary checkout, then every committed overlay carrier
of rounds 90 to 100 in round and part order, staged and landed as ONE declared-oversize commit.
The full suite then runs once in the primary checkout and its transcript is committed. The
overlay method of DECISION F275 D64 is retired from the flip commit onward.

## Next Steps

1. BRIDGE ROUNDS on the real tree, one residue group each, every one strictly shrinking the
   bad-node set of the committed transcript before it with no node newly bad: production code
   that hands a `JobPlan` a `JobBudgets` model where the record holds its serialized dict; the
   classic-shaped tests of routed handlers in `tests/test_data_paths.py`; what is left of the
   classic runner under `job resume`, whose kill-and-resume fixture still builds a classic job;
   the job digest's stored goldens; and the rows `ruff check` gains from the transform — until
   a round's transcript reads exit 0.
2. THE CLASSIC STORE, with the which-store branches and adapters the flip leaves unreached.
3. THE CLOSURE SEQUENCE.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE BRANCH IS RED FROM THE FLIP COMMIT until a bridge round's transcript reads exit 0, and
  hosted CI on the branch is expected to be red in that span, per amend0914 rule 3.
- THE BRIDGE IS BOUNDED at eight rounds after the flip commit: a ninth writes an operator
  question and stops, and a round that adds a bad node is FAIL.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open, and 89 once `R-0884` is registered. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
