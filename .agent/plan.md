# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001, T002 and T003 are DONE, and round 105 repaired the
last two regressions the flip left.

## Current Step

ROUND 106 OPENS THE CLOSURE SEQUENCE. It books round 105's verdict and resolves `R-0887` and
`R-0888`, gives `docs/roadmap/features/T2_F275.md` its Built State section, and runs the
integration gate of `docs/agents/integration_gate.md`: the full suite on the branch in the
primary checkout, the same suite at the merge base in a throwaway worktree, and the comparison
of the two failure sets, with its evidence under `.agent/gate_f275_r106/`.

## Next Steps

1. THE SELF-USE PRECONDITION of the closure protocol, the re-assignment of every open finding
   this feature raised and did not resolve to the findings-paydown feature F273, and the one §3
   checklist consolidation pass this feature owes.
2. CLOSURE ROUND A: the ledger rotation, the evidence job and a fresh review package built from
   a clean tree at the accepted head.
3. CLOSURE ROUND B: the STATUS line, the README sync and the consumed self-use item in one
   commit, then the pull request.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step is run through the scripts and modules it calls.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 91 by distinct id at this round's base and 89 once `R-0887` and `R-0888` are
  resolved, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
