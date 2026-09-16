# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280, and the feature file's Built State says what was reached.

## Current Step

ROUND 26 OPENS THE CLOSURE SEQUENCE. It books round 25's PASS and records DECISION F261 D26,
runs the integration gate of `docs/agents/integration_gate.md` on the branch and at the fork
point with its evidence under `.agent/gate_f261_r26/`, and generates the self-use item and runs
it to the approval gate without applying it, with its evidence under `.agent/selfuse_f261/`.

## Next Steps

1. CLOSURE ROUND A: book round 26's verdict and whatever the self-use run returned, rotate the
   ledger as its own commit, and from a clean tree at that commit run the evidence job, the
   integrity check and a fresh review package.
2. CLOSURE ROUND B: the STATUS `[x]` line, the README sync and the self-use item's
   `consumed_by` in one commit, then the pull request, which is not merged in that session.
3. F280, which Rule A5 proposes once F261 is merged.

## Risks

- 125 findings are open by distinct id; three are High, R-0803, R-0804 and R-0807, none of them
  F261's. Seven that F261 owned belong to F280 by DECISION F261 D25.
- F261 closes with the Goal & Done sentence not met, and says so in its Built State; the
  operator may reverse the split through operator question Q3.
- THE SELF-USE RUN NEEDS THE LOCAL MODEL SERVER and creates one `remedy/job-*` branch.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step runs through the scripts and modules it calls.
