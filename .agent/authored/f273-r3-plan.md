# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 3 books round 2's verdict and the resolutions of R-0812, R-0396,
R-0445 and R-0736, registers R-0983, R-0984 and R-0985, lands DECISION
F273 D3, and builds T003's last clause (R-0645) and T016: the run state
renders its value with a 3.12 CI column (R-0984), the manifest reads the
ledger through its canonical reader (R-0985), and both evidence producers
emit tombstones the strict schema accepts (R-0839, R-0983).

## Next Steps

1. T002: the guards that cannot fail and the harness that reddens for its
   own reasons.
2. T004 to T015, one module group per round where the budget allows.
3. The findings the Acceptance names by id.
4. Closure; R-0803's resolution reads the closure suite's transcript,
   R-0807's the closure self-use run's ledger rows against its calls, and
   R-0984's the 3.12 column of the closure pull request's hosted CI.
