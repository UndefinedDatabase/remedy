# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
`LAST_REVIEWED_SHA` is 9c80cf59 — R48 was GATED PASS and that record sits in
`.agent/live_review.md`.
T001, T002, T003 and T004 are ALL DONE. The build is feature-complete; what
remains is closure.
The INTEGRATION GATE ran this round (`docs/agents/integration_gate.md`,
evidence in `.agent/gate_f105_r49/`). Real result: the branch suite is
16462 passed, 19 skipped, 0 failed, exit 0, 99 s. The base suite at merge base
cfda4245, with UI artifact parity restored by copy and verified by content
hash, is 16298 passed, 19 skipped, 7 failed, exit 1, 144 s. BRANCH-ONLY
failures: ZERO — no blocker exists. BASE-ONLY: seven, every one of them
`tests/ui_server/test_live_state.py::TestUIServerIntegration`, every one
attributed to the known R-0221 mtime-staleness class by three kinds of direct
evidence and passing on a serial re-run at the base. The base worktree was
created on the throwaway branch `tmp/base-gate`, then removed, pruned and the
branch deleted.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266, R-0268 and the
newly registered R-0269 — eight. R-0269 is the only one with a fix LANDED this
round (the note now states what the directional prefix guard cannot catch); it
stays OPEN until the reviewer authors its `Done:` text. The next free finding
ID is R-0270.

## Next Steps
1. Closure per `docs/roadmap/STATUS_closure_protocol.md`: the evidence job, a
   FRESH review zip, the STATUS line and the closure PR.
2. PR #189 (`docs/amend0810-clerical` -> `main`), which the OPERATOR must
   resolve before F105's closure PR is cut.

## Risks
- PR #189 is open and is NOT from a `feature/*` branch, so the Open PR Gate
  makes it stop-and-report. It blocks no work here, but it blocks closure.
- R-0221 stays open. It cost this gate seven phantom base-only failures, as
  predicted; it will cost the same at any future gate until it is fixed.
- R-0262, R-0265, R-0266 and R-0268 stay OPEN and out of scope for F105 by
  design; R-0268 belongs to the self-drive protocol, not prompt composition.
