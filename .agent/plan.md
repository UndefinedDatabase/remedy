# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: aff20fa3 (R17 PASS, plus the state-only
close-out commits). Next free finding ID: R-0338. Open findings: 11 —
R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334,
R-0336, R-0337. No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003d gave the command its docs page:
`docs/guides/cost-report-user-guide-v0.md` explains the half-open period,
the `unmeasured` word, the attribution line, the prior-period sentence and
the json keys, states that per-role has one bucket and per-task-class has
no source, and is registered in the `docs/README.md` index in this same
PR. Its example report is the T002 golden byte for byte, so the guide
cannot drift from the renderer without a red gate.

## Next Steps
1. Integration gate (docs/agents/integration_gate.md) — the full suite
   with `-n auto`, R-0322's five pre-existing reds expected.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line committed last, then the PR.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit —
  and now the guide's example too.
- The `remedy` binary is refused in this session's sandbox, so CLI wiring
  is proven through the suite and never through a pasted `--help`.

Fortschritt: 96 % (T001 ✅ · T002 ✅ · T003 ✅ — Integration-Gate + Closure
offen) — Schätzung
