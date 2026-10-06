# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 1, round 6, the session's last: book round 5's verdict, and land the digest's open
decisions as DECISION F295 D5 rules them — every open decision of every job with its question,
documented default, options, bundled questions and age.

## Next Steps
1. T002, last part: each job's measured cost with its basis and its evidence references, and each
   project's cost of the day, in the digest; and the digest's read cost measured.
2. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui
   --json` on a pipe never reads stdin.
3. T004: `docs/system/machine-client-contract-v1.md`, which also writes down the order file's
   format, and the gate test.
4. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1138 and R-1139 (Low) stay open, owned by F297; F295 owns no open finding.
- The digest reads every job file and every job's events on each call; its cost is measured
  before T002 closes.
