OUTCOME: (pending — update at handback)

You are the Remedy worker (Window 2) for feature F069 — Mission compiler,
  round R2 (SPLIT, LARGE): persist the R1 verdict + finding, fix R-0168,
  then the INTEGRATION GATE. AGENTS.md governs. Save THIS ENTIRE block
  verbatim to .agent/last_block.md FIRST (update its OUTCOME line at
  handback). STOP-ON-RED for the whole round: the first red verification →
  STOP per AGENTS.md If Blocked; commit the safe state, record the raw
  failing output in the handoff, hand back early. You are on
  feature/f069-mission-compiler at 83ddb4cb.

  PHASE 1 — PERSIST THE VERDICT + FINDING (FIRST ACTION, own commit)
   1. Save the AUTHORED TEXT payload below to .agent/authored/f069-r2-1.md
      — bytes between BEGIN/END markers, exclusive, including the final
      newline. Verify with sha256sum against the BEGIN-marker hash.
      Mismatch → STOP, report the raw sums, apply nothing.
   2. Apply its THREE edits to .agent/live_review.md (each FROM occurs
      exactly once; copy the TO text from the SAVED file, never retype).
   3. Update .agent/plan.md Current Step/Next Steps for R2 (keep the
      `## Goal` and `## Next Steps` headings — contract tests read them).
   4. Commit: chore(f069): persist the R1 verdict + R-0168. Gate: python3
      -m pytest tests/cli/test_golden_path.py -q → exit 0. Push.

  PHASE 2 — FIX R-0168 (packages/orchestration/mission_plan_schema.py)
   1. Named constant MAX_MILESTONE_DRAFT_JOBS = 8. MilestoneDraft
      validator: len(jobs_draft) <= 8, refusal message in the existing
      MissionPlanError style. DraftJob: title and goal must be non-empty
      after strip. Milestone inherits both (goldens max at 2 outlines —
      unaffected; the deterministic fallback carries 1 — unaffected).
   2. Name the cap in _MISSION_PROMPT_TEMPLATE's Rules (mission_compiler)
      so the provider is told, not just refused.
   3. Tests in tests/orchestration/test_mission_compiler.py: (a) a draft
      with 9 outlines on one milestone and (b) a draft with a blank job
      goal both fail draft validation, so compile_mission_plan ends in the
      deterministic fallback with a hint — never a traceback out of
      attach_milestone_dods/plan_mission; (c) validator unit tests (cap
      boundary 8 ok / 9 refused; blank title refused).
   4. Append to the R-0168 finding in .agent/live_review.md, same bullet:
      Done: R-0168 (commit <sha>).
   Done when: python3 -m pytest tests/orchestration/
   test_mission_compiler.py tests/orchestration/schemas/test_schemas.py -q
   → exit 0, AND python3 -m pytest tests/cli/test_golden_path.py -q →
   exit 0. Red → STOP rule. Commit(s) small, push.

  PHASE 3 — INTEGRATION GATE (docs/agents/integration_gate.md — read it
  and follow it EXACTLY; it owns the procedure, this block only scopes it)
   - Branch run + base run (throwaway worktree ON a tmp branch at the
     merge base; UI-artifact parity per the doc: COPY apps/ui/node_modules
     and apps/ui/dist, never symlink; REMEDY_UI_NO_AUTO_BUILD=1), comm in
     BOTH directions, attribution for EVERY branch-only id per the doc's
     classes. A reproducible branch-only failure coupled to feature code =
     BLOCKER: STOP, hand back — the fix is its own reviewer-gated round.
   - Evidence (raw tails, FAILED lists, exit codes, wall times, comm
     outputs, per-id attribution) committed under .agent/gate_f069_r2/
     (F062 precedent). Remove + prune the worktree and tmp branch; prove
     with git worktree list. The GATE VERDICT is the reviewer's — report
     evidence, claim no verdict.
   - Wall clock over ~5 min → note it for a perf pass (§3 tier 4).

  DO NOT TOUCH: execution, job creation, dossier maintenance, loop
  policy. No closure work of any kind this round (no STATUS edit, no zip,
  no PR). Primary checkout porcelain-clean at every point a command ends
  (R-0160).

  HANDBACK
   Push first. Completion report + rewrite .agent/handoff.md per
   docs/agents/handback_template.md: ALL commits tabled (grouped
   self-reference allowed, R-0149); raw transcripts (command, exit code,
   real output tail) for EVERY gate and both full-suite runs; sha256
   proof for the applied authored text; deviations & assumptions
   numbered. End with: "F069 R2 complete — awaiting the gate verdict."

  --- BEGIN f069-r2-1 sha256=7f9538b8156a57dccc29c2866bfaf365acfe62d684fc4b16cea8ed4edbc7ef7d ---
  EDIT 1 FROM (exact two lines, occur once in .agent/live_review.md):
  - Next: integration gate per docs/agents/integration_gate.md, then
    closure per docs/roadmap/STATUS_closure_protocol.md.
  EDIT 1 TO:
  - R2 (LARGE): persist the R1 verdict + R-0168 (own commit); fix
    R-0168; scoped re-verification; THEN the integration gate per
    docs/agents/integration_gate.md — stop-on-red.
  - Next: closure per docs/roadmap/STATUS_closure_protocol.md.
  EDIT 2 FROM (exact line, occurs once):
  - Next free ID: R-0168.
  EDIT 2 TO:
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
  - Next free ID: R-0169.
  EDIT 3 FROM (exact line, occurs once):
  - (pending R1 handback)
  EDIT 3 TO:
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
  --- END f069-r2-1 ---
