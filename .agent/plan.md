# Plan — F057 Rate-limit-aware scheduler (CLOSED)

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. F057 is
closed `[x]` in docs/roadmap/STATUS.md as of 2026-08-14, verdict
PASS_WITH_RISKS. Next free finding id: R-0380. Open findings, recomputed from
`.agent/live_review.md` and not carried over from the previous plan: R-0361,
R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376,
R-0377, R-0378, R-0379 — fourteen, three Medium and eleven Low, none High,
every one carried as a documented accepted risk. R-0365, R-0366, R-0370,
R-0372 and R-0373 are resolved. `.agent/live_review.md` is the source of truth
for this ledger; this file is a mirror of it and nothing else.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today. Shipped as
T001 signal normalization, T002 the governor and its acquire semantics, and
T003 the pingpong seam plus the two report surfaces.

## Current Step
None. R14 closed the feature: the R13 verdict is on the record, the evidence
job and a fresh review zip were built, and the STATUS and README edits landed
as the last commit on the branch. The closure PR is open and unmerged.

## Next Steps
1. Nothing on this branch. The closure PR is NOT merged in this session; it
   merges at the next feature's start via the AGENTS.md Open PR Gate, which is
   the operator's manual-review window.
2. The next session's FIRST action is Phase 1 rule 1 of
   docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk —
   BEFORE rule 2's Open PR Gate.
3. `.agent/candidates.md` is non-empty. The next feature's first reviewed
   round registers its entry with the next free id or resolves it inline as a
   §4.7 DECISION, and empties the file in that same round.
4. Rule A5 then proposes F077 — Autonomy watchdog, the first `[ ]` in STATUS
   order.

## Risks
- Fourteen open findings is the largest carry this feature has held, and every
  one of them is a reviewer gate defect rather than a product defect. They
  close as documented Medium/Low risks; the integrity check reports no open
  blocker/high findings.
- A reviewer rate limit reaches the governor only when its error carries the
  `provider_error:` prefix, because `ReviewerOutput.verdict` defaults to
  `"blocked"`. R-0378 tracks that this coupling is undocumented in the code.

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrationsgate ✅ · Closure ✅) — gemessen
