# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001, T002 and T003 are DONE, the feature file's Built
State is current, and the integration gate passed in round 106.

## Current Step

ROUND 107 IS THE SELF-USE PRECONDITION AND THE FINDING RE-ASSIGNMENT. It books round 106's
verdict and the integration gate's, re-assigns the 22 open findings this feature raised and did
not resolve to the findings-paydown feature F273, records that the §3 checklist consolidation
pass merges nothing, and generates the tier-1 self-use item, runs it to the approval gate under
the configured real provider without applying it, and commits the run's evidence under
`.agent/selfuse_f275/`.

## Next Steps

1. CLOSURE ROUND A: register every defect string the self-use run returned, rotate the ledger,
   run the evidence job and build a fresh review package from a clean tree at the accepted head.
2. CLOSURE ROUND B: the STATUS line, the README sync and the self-use item's `consumed_by` in one
   commit, then the pull request.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE SELF-USE RUN NEEDS THE LOCAL MODEL SERVER: role config resolves builder and reviewer to
  a local `ollama` model, and the runner refuses to run on the fake provider.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step is run through the scripts and modules it calls.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- The open set is 89 by distinct id, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open.
  Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
