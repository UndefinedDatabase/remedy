# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001, T002 and T003 are DONE: the record flip landed in
round 101 and the classic store was deleted in round 104.

## Current Step

ROUND 105 REPAIRS `R-0887` AND `R-0888`, the two regressions the flip left that the suite did
not see. The one dashboard builder emits `prompt_trace` from `_build_prompt_trace` over the
job's evidence directory, so the cockpit's prompt trace lens shows each task's prompts again;
the reviewer's context names a job by its `job_title`, a test failure artifact carries the
job's `job_id`, and the verify-first refusals quote a task's `title`. Each repair has a test
that fails without it. The full suite runs once and must read exit 0.

## Next Steps

1. THE CLOSURE SEQUENCE of `docs/roadmap/STATUS_closure_protocol.md`: the integration gate
   with its full-suite runs, the evidence job and a fresh review package, the re-assignment of
   every open finding this feature does not resolve, the §3 checklist consolidation, the
   ledger rotation, and the STATUS line with its pins, then the pull request.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step is run through the scripts and modules it calls.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 91 by distinct id at this round's base, with `R-0809`, `R-0880`, `R-0883`,
  `R-0884`, `R-0887` and `R-0888` open. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
