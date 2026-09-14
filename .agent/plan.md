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

THE FLIP ROUND, per operator amendment amend0914-f275-sprint. First commit books the round 100
verdict and any carried slips, exactly as before. Next commit is THE FLIP: in the primary
checkout, on the branch, run the transform as round 100's block ordered it, then apply every
committed overlay carrier under `.agent/authored/` (`f275-r<n>-overlay*.md`, ascending round and
part order, each `git apply --check` then `git apply`), then `git add -A` — ONE commit, the
operator's second declared-oversize grant for F275. Then one full-suite run in the primary
checkout, transcript committed to `.agent/authored/f275-r<n>-suite.txt`. Then the handback.

## Next Steps

1. BRIDGE ROUNDS: one residue group each, on the real tree — production code that hands a
   `JobPlan` a `JobBudgets` model where the record holds its serialized dict; the classic-shaped
   tests of routed handlers in `tests/test_data_paths.py`; what is left of the classic runner
   under `job resume`, whose kill-and-resume fixture still builds a classic job; and the job
   digest's stored goldens — each round strictly shrinking the committed bad-node set until a
   round reads exit 0.
2. THE CLASSIC STORE, with the which-store branches and adapters the flip leaves unreached.
3. THE CLOSURE SEQUENCE.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: test nodes still fail in the flipped tree, and a test that starts the
  command line from a directory outside that tree runs this checkout's code instead.
- THE BRIDGE IS BOUNDED: at most eight red rounds after the flip commit (amend0914 rule 3); a
  round that adds a bad node is FAIL.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
