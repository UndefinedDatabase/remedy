# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 16 books round 15's verdict and three resolutions, registers R-0991,
lands DECISION F273 D16, and builds the repair-loop deletion (R-0918,
R-0923, R-0924, R-0925, R-0926) with the helper-aware catalog contract
(R-0991), the handled refusal of `job evidence` (R-0912) and the two
worker-step rules of the self-drive protocol (R-0940, R-0954).

## Next Steps

1. R-0914: delete the operator-attestation writer and the export overlay
   that only it fed, keeping everything the closure evidence producer
   reaches.
2. The worker queue (R-0927 with R-0928), without raising the coupling
   ceiling.
3. R-0977 with the `__pycache__` handoff-coverage defect it exposes.
4. A measured owner for every other open id, then closure; R-0803's
   resolution reads the closure suite's transcript, R-0807's the closure
   self-use run's ledger rows against its calls, R-0984's the 3.12 column
   of the closure pull request's hosted CI, R-0892 waits on the operator's
   skill-page write, and R-0662 waits for the checklist consolidation pass.
