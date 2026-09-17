# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 17. C1 books round 16's independently-reviewed PASS and adds DECISION
F281 D6. C2 lands `packages/orchestration/dead_command_check.py`
(`dead_command_ids`, a four-signal reference check: an AST-detected argv-list
pair, the spaced form, the dotted `command_id`, and the handler's own
referenced names) and wires it into `remedy doctor core` as an always-shown
`dead commands:` section plus a `dead_command_scan` hard check; two new
tests pin the section's presence in both render modes and the algorithm
itself is pinned in its own new test file, which also asserts the real
catalog reads empty. One line added to the import-reachability allowlist.
After this round: `remedy doctor core` lists dead commands as a section and
the section reads empty on the shipped catalog, clearing that Acceptance
line; F271 (later) owns the closure-precondition wiring and the
fixture-based red-proof.

## Next Steps

1. Remaining Acceptance items: R-0805 (`ui status` dead-session pruning),
   R-0809 (one id-error-message shape for mission/job/run), R-0895 (README
   quickstart) and R-0934 (advertised-flag scanner skips a quoted argument)
   are all OPEN. R-0895 runs last (orchestrator brief: it quotes the
   finished catalog). Session 3 begins at this round; continuing is allowed
   while context comfortably suffices (amend0905-throughput's 6-to-8 target).

## Risks

- None carried from round 16: DECISION F281 D6 resolves the design question
  PLAN16 flagged, measured non-vacuous by this round's mutation red-proof.
