# Live Review — F069 Mission compiler (Tier 1)

Branch: feature/f069-mission-compiler
Scope: a long prose goal compiles into a versioned MissionPlan —
ordered milestones with a milestone DAG, each carrying a compiled
DoD reference (via the F061 compiler, no second mechanism, A6) and
draft job outlines that are explicitly NOT runnable; deterministic
one-milestone fallback without a provider; CLI plan/recompile with
version retention and in-progress refusal. Compiling creates no
jobs, starts nothing, touches no worktree.

## Steps
- R1 (SPLIT, LARGE bundle, operator LARGE-mode 2026-08-02): claim +
  T001 schema + milestone-DAG validation + compiler + deterministic
  fallback + three long-goal fixtures with golden milestone
  structures; THEN T002 per-milestone DoD hand-off + persistence on
  the mission record + mission_plan.md rendering + the no-autostart
  guarantee (negative test: compile leaves zero jobs); THEN T003
  CLI `remedy mission plan <id>` + recompile versioning +
  in-progress refusal — per-slice verification, stop-on-red.
- R2 (LARGE): persist the R1 verdict + R-0168 (own commit); fix
  R-0168; scoped re-verification; THEN the integration gate per
  docs/agents/integration_gate.md — stop-on-red.
- Next: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0168 (behavior, Low) 2026-08-02: MissionPlanDraft caps
  milestones (12) but not jobs_draft per milestone, and DraftJob
  accepts empty or blank title/goal. milestone_flight_plan builds
  len(jobs_draft)+1 tasks, so more than 24 draft outlines — or a
  blank goal (acceptance [""]) — fail the FlightPlan validators
  INSIDE attach_milestone_dods, outside the compile-time
  parse-retry net: plan_mission raises ValueError and the CLI
  shows a traceback instead of a parse-class refusal. Fix:
  validate at the draft — cap jobs_draft (named constant, 8 per
  milestone) and require title/goal non-empty after strip — so a
  bad provider draft fails inside run_structured_call (one retry,
  then the honest deterministic fallback); name the cap in the
  provider prompt's rules; pin with tests: an over-cap draft and
  a blank-goal draft both end in the deterministic fallback with
  a hint, never a traceback.
  Done: R-0168 (commit b70009cb).
- Next free ID: R-0169.

## Verdicts
- R1: PASS (SPLIT, LARGE bundle, 2026-08-02). Range
  53ac3efa..83ddb4cb (12 commits, all tabled). Reviewer re-ran:
  compiler 90 + state 81 + CLI 66 (237 combined) + canary 42 +
  docs 293 + dashboard contract 70 — all exit 0; the handback's
  160/156 totals reconcile as mid-round states. Transport cmp 0
  disk-to-disk, both texts, scratchpad originals; STATUS claim
  FROM 1→0, TO 0→1. Spot-checks: porcelain empty; primary
  worktree only; stash@{0} intact and unconsumed (deviation 6
  verified); PR #174 gate-merge landed (53ac3efa); the fixtures'
  goldens carry coherent 4/3/2-milestone DAGs with dod_refs.
  Deviations 1–5 accepted: named tag exemption widened to 2
  (bound 15); per-MISSION in-progress rule (the record lacks
  milestone attribution, Do-not-touch honored) — DECISION in
  .agent/decisions.md; additive mission_plan field, no schema
  bump; DoD via the ephemeral milestone_flight_plan VIEW, never
  persisted or scheduled (A6 held); two self-caught defects fixed
  with tests. R-0168 registered (unbounded jobs_draft / blank
  draft fields, Low). LAST_REVIEWED_SHA = 83ddb4cb.
- R2: PASS — INTEGRATION GATE PASS (LARGE round, 2026-08-03). Range
  83ddb4cb..d2a4bb75 (5 commits, all tabled). Reviewer re-ran:
  compiler+schemas 151 + canary 42, exit 0; OWN full suite at HEAD
  15094 passed / 19 skipped, exit 0 — matching the branch evidence
  in .agent/gate_f069_r2/; base 8 failed / 14968 passed (worker
  raw); comm -13 EMPTY (0 branch-only); comm -23 = 8 ids, all
  test_live_state.py::TestUIServerIntegration, attributed to the
  environment class on three direct evidences (base stderr "React
  UI not built"; dist rewritten mid-run; pass-at-base re-run
  42/42, exit 0) — flake debt 0. R-0168 verified fixed in situ
  (cap at draft validation, blank refusal, prompt names the cap;
  red-proof at pre-fix HEAD in a throwaway worktree, R-0160) —
  Done stands. Transport: digest fallback per
  planner_reviewer_prompt.md §4.9 (scratchpad originals
  unavailable at review time; the committed authored file's
  recomputed sha256 equals the BEGIN digest 7f9538b8…dbc7ef7d) —
  stated so the evidence chain stays honest. Deviations 1–3
  accepted. Worktrees removed + pruned, tmp branch deleted,
  primary only. Only this round carries the full-suite claim:
  FULL SUITE GREEN. LAST_REVIEWED_SHA = d2a4bb75.
