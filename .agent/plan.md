# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 5: book round 4's verdict and R-1141's resolution, and land the digest's frame as
DECISION F295 D4 rules it — a `client` object in `remedy status --json` with projects, missions,
jobs, the jobs that wait for apply and whether the supervisor answers.

## Next Steps
1. T002, second half: the digest's open decisions with question, default and age, each job's cost
   with its basis and its evidence references, and each project's cost of the day.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138 and R-1139 (Low) stay open, owned by F297; F295 owns no open finding.
- The digest reads every job file on each call; its cost is measured before T002 closes.
