# Live Review — F070 Orchestrator loop inside Remedy (Tier 1)

Branch: feature/f070-orchestrator-loop
Scope: the external orchestrator's working style internalized as
Remedy's own loop: per mission iteration, assemble context (dossier
first, cache-stable prefix), one schema-validated OrchestratorMove
from the configured orchestrator-role model, execute through
EXISTING verbs only (A6), evaluate job terminal state + milestone
DoD, update mission state and dossier, append an auditable ledger
entry with cost actuals. The move schema has NO kind that creates
missions or edits goals; stop requests and answered decisions are
read every iteration. Era fixture corpus detection (R-0141/43/45,
R-0144, R-0146, R-0147, R-0148 classes) is an acceptance criterion.

## Steps
- R1 (SPLIT, LARGE bundle): Open PR Gate (#175) + claim + verb map
  + T001 + T002 — PASS, see Verdicts.
- R2 (SPLIT, LARGE): persist verdict + findings (own commit); fix
  R-0170 with tests; docs amendments (handback-cap DECISION,
  R-0169 integration-gate hardening); THEN T003 e2e fixture
  mission (three jobs, one escalated decision, to achieved) + CLI
  `remedy mission run` / `remedy mission ledger`; THEN the
  integration gate per docs/agents/integration_gate.md (hardened
  form), evidence under .agent/gate_f070_r2/ (.txt names) —
  per-slice verification, stop at first red. No closure work.
- Next: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0169 (gate tooling, Low) 2026-08-03, carried from F069's
  closure candidate: REMEDY_UI_NO_AUTO_BUILD=1 did not prevent a
  UI auto-build inside the F069 R2 gate base worktree (dist/
  rewritten mid-run, .agent/gate_f069_r2/attribution.md evidence
  2); same incident: *.log evidence names are gitignored AND
  zip-guard-rejected (9/12 files landed until renamed .txt). Fix:
  the two integration_gate.md amendments authored as f070-r2-4
  (dist/ hash parity verification; .txt evidence names) — applied
  in R2's docs slice.
  Done: R-0169
- R-0170 (behavior, Low) 2026-08-03: evaluate_move checks a
  declare_mission_achieved claim only against OPEN milestones. A
  mission with NO compiled plan has milestone_ids() == (), so
  open_ones is empty and the claim EXECUTES: reviewer reproduced —
  plan-less active mission + scripted achieved move -> status
  "achieved" in one iteration, zero evidence. Inconsistent with
  all_milestones_done(), which requires bool(ids). Fix: refuse
  the achieved claim when milestone_ids(mission) is empty ("no
  compiled plan — nothing evidences the goal"); pin with tests: a
  plan-less achieved claim is refused with a recorded reason, and
  a second refusal escalates, never executes.
  Done: R-0170
- R-0171 (accounting, Low) 2026-08-03: the R1 handback commit
  b053516a also modified .agent/decisions.md (+5/-2, the
  backup-branch deletion note) but its grouped table lists only
  handoff.md — the omission shape the new era corpus itself flags
  (R-0141/R-0143 class, miniature scale). Also: the prose proof
  line cites digest "0db64fea…" for candidates.md where the real
  digest is 0db64faa… (transcription slip; the sha256 block above
  it is correct — reviewer cmp confirmed byte-identity). Fix: the
  R2 handoff carries a correction row for b053516a; every future
  table lists every touched file, bookkeeping included.
- Next free ID: R-0172.

## Verdicts
- R1: PASS (SPLIT, LARGE bundle, 2026-08-03). Range
  afbe2639..b053516a (16 commits, all tabled; the final-commit
  omission -> R-0171). Reviewer re-ran: orchestration 9439 passed
  / 7 skipped, canary 42, docs 293, loop+era targeted 138 — all
  exit 0, matching the handback's numbers. Transport: cmp 0
  disk-to-disk against the reviewer's scratchpad originals for
  all four authored texts; applied state files byte-identical;
  STATUS claim FROM 1->0, TO 0->1. The declared rebuild
  (deviation 6, force-push) was INDEPENDENTLY re-verified: the
  pre-rebuild tip 08b77ba2 survives in the local object store and
  `git diff 08b77ba2 2b28f15a` is EMPTY — byte-identical trees;
  every commit in the rebuilt range is <=471 changed lines.
  Deviations 1-8 accepted: CLI deferral (permitted by the order);
  the dossier-SEAM reading of A6 (F071 unbuilt, stand-in labeled
  and tested); the --yes extraction verified faithful in the
  diff; the orchestrator role addition with the renamed pinned
  tuple (declared, defaults unchanged); two T001 tests tightened
  not weakened; the handoff-cap collision routed to a DECISION
  (template amendment f070-r2-3, applied in R2); ledger-based
  milestone attribution (recorded, job creation untouched).
  R-0170 registered and REPRODUCED by the reviewer; R-0171
  registered. LAST_REVIEWED_SHA = b053516a.
