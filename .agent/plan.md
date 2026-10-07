# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 4, round 17: book round 16's PASS, register R-1152, and repair it under DECISION F295
D15 — `remedy change proof <job> --json` lists the job's applies through `remedy job apply` under
`job_applies`, never as verified, so the client's last read names what the apply wrote.

## Next Steps
1. T004: `docs/system/machine-client-contract-v1.md` and the gate test. Measured at `89ad24d76`
   with `.remedy-wt/f295-r17/probe2.py`: `remedy do <file> --json --no-ui --yes --deadline
   <past>` stops on the budget and raises `budget:<id>`, answered `extend`; `remedy job run`
   completes the job; `remedy job apply --approve` lands it. The hunk view of a `remedy do` job
   needs `remedy job evidence <job>` first; the page names that step.
2. The SLOW MODE hardening stage (amend0930b-slow-cap), then the closure sequence.

## Risks
- R-1152 (Medium, F295's) is repaired this round; its resolution is booked after review.
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- Eleven local branches `remedy/<16 hex>` with prunable worktree entries, made on 2026-10-07 at
  `c2b9a817f` and `4ae5d4d33` while F295's round 13 and 14 tests ran, remain in this repository;
  the hardening stage measures the cause.
