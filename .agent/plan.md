# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 18. C1 books round 17's PASS (one LOW finding, R-0956: a dropped
trailing newline in `.agent/decisions.md`, fixed in this same commit) and
resolves R-0934. C2 replaces
`tests/cli/test_advertised_commands.py`'s regex-only command-line-end
detection with `_command_line_end`, which skips over a quoted argument
(`"<goal>"`) instead of stopping the scan at its opening quote, so a flag
advertised after a quoted goal is now caught; one new regression test.
After this round: R-0805, R-0809 and R-0895 remain open on the Acceptance
list.

## Next Steps

1. R-0809 (one id-error-message shape for mission/job/run) is LARGE:
   research this session found FOUR current wordings across 20+ call sites
   (`brain.py` alone has 11), a job-id resolver already shared
   (`resolve_job_id`/`lookup_job_id` in `packages/orchestration/data_paths.py`)
   but a run-id and mission-id resolver that are NOT, and 9+ tests asserting
   the current wordings that will need updating. This does not fit one
   round; the round that claims it starts by measuring the exact call-site
   and test count fresh, then scopes a shared-helper design (probably one
   round per id kind: job, run, mission) before touching any call site.
2. R-0805 (`ui status` dead-session pruning, `ui status --all` showing the
   last ten with end time) needs a design pass on the session-state model
   before implementation — do not rush a heuristic.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 3 continues (round 18); continuing is allowed while context
   comfortably suffices (amend0905-throughput's 6-to-8 target).

## Risks

- R-0809's true scope was undermeasured before this session's research; do
  not let a future round default to a single mechanical sweep across all
  call sites without first scoping run-id and mission-id resolution, which
  currently have no shared helper the way job-id does.
