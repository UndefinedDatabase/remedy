# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions. Merge base COMPUTED this round, not
assumed: `git merge-base main HEAD` → cb3ef34fddbf0efa5799d8de93cb2d8e66566d20.
No PR open; nothing merged. Next free finding ID: R-0359. Open findings: 3 —
R-0350, R-0354, R-0358 — RECOMPUTED by the gate (b) command over
`.agent/live_review.md` (every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line). That matches what the block expected; no deviation.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
The integration gate ran; evidence in `.agent/gate_f045_r15/`. Branch run
`python3 -m pytest -n auto -q` → exit 1, 128 s, `5 failed, 16769 passed, 19
skipped`. Base run at the merge base, throwaway worktree on branch
`tmp/base-gate` → exit 1, 142 s, `11 failed, 16700 passed, 19 skipped`.
`comm -13` (BRANCH-ONLY) is EMPTY: F045 introduces no failure. `comm -23` held 6
`tests/ui_server/test_live_state.py::TestUIServerIntegration` ids, each
attributed to the environment class — their captured stderr is `ERROR: React UI
not built.` naming `apps/ui/dist`, each passes serially at the merge base, the
whole file passes there under `-n auto`, and a SECOND full base run on the same
commit reproduced none of them and produced a FAILED list byte-identical to the
branch's (`cmp` exit 0). The 5 failures common to both sides are pre-existing:
the `reviewer_conventions` prompt segment estimates 954 tokens against a cap of
800, and this branch never touches `docs/agents/reviewer_conventions.md`. The
gate VERDICT is the reviewer's, not this file's.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md. Its precondition 2
   ("full relevant suite green") meets those 5 pre-existing red ids, which F045
   did not cause and which no F045 round may fix; that call is the reviewer's.
2. The open findings R-0350, R-0354, R-0358, if closure does not absorb them.

## Risks
- The branch run rebuilt the PRIMARY checkout's `apps/ui/dist` mid-run (mtime
  1786668566, inside the branch-run window) — the R-0169 phenomenon.
- Schedule and event triggers are validated but INERT until the scheduler.
- `report_path` resolves through `jobs_dir()`, which reads REMEDY_DATA_DIR and
  honours no `root=`; report tests isolate through the environment (R-0351/2).
- This branch has carried no PR across several sessions; that call is the
  operator's, and this session did not make it either way.

Fortschritt: ~85 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrationsgate gelaufen) — Schätzung
