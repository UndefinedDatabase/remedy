# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: b047aa38 (R18 PASS WITH RISKS). Next free
finding ID: R-0339. Open findings: 12 — R-0320, R-0322, R-0323, R-0324,
R-0327, R-0328, R-0331, R-0333, R-0334, R-0336, R-0337, R-0338. No PR exists
and closure has not started. `.agent/STOP` is on disk.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 is complete, docs included. `docs/guides/cost-report-user-guide-v0.md`
explains the half-open period, the `unmeasured` word, the attribution
line, the prior-period sentence and the json keys, and is registered in
the `docs/README.md` index. Its example report is the T002 golden byte for
byte. ONE sentence in it is false and is registered as R-0338: the
role-limit note belongs to `remedy stats cache`, not `remedy stats cost`.

## Next Steps
1. Repair R-0338 FIRST — one sentence in the guide, plus the plainer fact
   that `stats report` does not print the note itself.
2. Integration gate (docs/agents/integration_gate.md), full suite
   `-n auto`, R-0322's five pre-existing reds expected.
3. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line committed last, then the PR.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the guide's example in the same commit.
- The `remedy` binary is refused in this session's sandbox, so CLI wiring
  is proven through the suite and never through a pasted `--help`.

Fortschritt: 96 % (T001 ✅ · T002 ✅ · T003 ✅ — R-0338-Repair,
Integration-Gate und Closure offen) — Schätzung
