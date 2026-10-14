# Plan — amend1014b-pi-default-repeatable-do

## Goal
Operator amendment amend1014b (2026-10-15), closing PR #339 on `feature/do-golden-path`:
Pi (JSON mode, local Ollama `muse-glimmer:latest`) is the default builder/reviewer/repair harness,
and a dirty working tree is the captured baseline so `remedy do ... --apply` then
`... --commit-auto` run back to back. D1 to D7, tests 1 to 18, real acceptance A to E.

## Current Step
Production code in place and trial-verified (A, B, C ran against the real model):
`pi_provider.py`, `dirty_baseline.py`, role defaults, seeding, apply from the baseline commit,
`target_changed_during_run`, empty-diff pass rejection, health chain. Old tests updated.
Next: commit slices, then the 18 mandated tests.

## Next Steps
1. Commit slices (provider+wiring / baseline+apply / loop guard+health) with tests.
2. Mandated tests 1 to 18 (fake `pi` executable for subprocess contract).
3. Docs (quickstart, do guide, docs/README), dated decision, PR #339 title and body.
4. Real acceptance A to E recorded; closure gate once; handoff.

## Review Strategy
PR #339 has no review comments on any of the three channels (checked 2026-10-15).

## Risks
- Structure ratchet (`run_pingpong`, `_cmd_do` must not grow): the loop edit is net negative.
- `.agent/STOP` is untracked and must stay untouched; F078 branch untouched.
