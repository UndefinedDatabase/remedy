# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 6 books round 5's PASS and DECISION F278 D5, makes the secret detector
in `run_manifest.py` fail closed, and marks every blind handler in
`job_evidence.py`, `run_manifest.py` and `scripts/build_review_manifest.py`
with a noqa reason, one file per commit, comment text only.

## Next Steps

1. T003, the next marking group: the job, pingpong, apply, runtime and
   snapshot modules, each handler narrowed or given a reason.
2. T003, the last marking group, in whose final commit BLE001 joins `select`
   and the ratchet test freezes the count of excused handlers.
3. The closure sequence.

## Risks

A reason drafted by a research agent is only as good as its reading; the
reviewer checks the ones that could hide a defect against the code.
