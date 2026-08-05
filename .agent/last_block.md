You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
10 flawless self-runs, round R13: CLOSURE per
docs/roadmap/STATUS_closure_protocol.md (v4) — read it and follow it
exactly; this block orders the steps and carries the authored texts.
Any precondition or zip failure -> STOP per Failure honesty (the
feature does NOT close; record the raw error in the handoff). Save
THIS ENTIRE block verbatim to .agent/last_block.md as its OWN FIRST
commit (R-0198). You are on feature/f075-self-run-gauntlet at
8bc1305a. NEVER force-push (R-0195); commits < 500 lines except where
a single authored artifact is inseparable — declare, never rewrite.

PHASE 0 — THE BLOCK
 Commit 0: chore(f075): save the R13 closure block. Touches ONLY
 .agent/last_block.md. Push.

PHASE 1 — PERSIST THE R12 GATE VERDICT (own commit)
 1. Save the five AUTHORED TEXT payloads below to
    .agent/authored/f075-r13-<n>.md (bytes between BEGIN/END
    markers, exclusive, incl. final newline; payload lines at
    column 0). Verify each sha256sum against its BEGIN-marker hash.
    Mismatch -> STOP, report raw sums, apply nothing (the r12-2
    precedent: diagnose from the saved bytes, never guess).
 2. Apply f075-r13-1 -> .agent/live_review.md (the FROM line occurs
    once; the TO embeds it — copy from the SAVED file, never
    retype; the two-space indentation of the FROM/TO lines inside
    the payload is part of the bytes).
 3. Commit 1: chore(f075): persist the R12 gate verdict. Gate:
    python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0.
    Push.

PHASE 2 — BUILT STATE (precondition 4, own commit)
 1. Append the BYTES of f075-r13-2 to the END of
    docs/roadmap/features/T1_F075.md (starts with a blank line;
    simple byte-append). Verify: bytes occur exactly once, the file
    ENDS with them, prior content intact as prefix.
 2. Commit 2: docs(f075): record the accepted Built State. This is
    the LAST content commit — its head is the intended accepted
    HEAD.
 3. Gates (docs/roadmap touched): python3 -m pytest tests/docs/ -q
    AND python3 -m pytest tests/cli/test_golden_path.py -q -> both
    exit 0. Push.

PHASE 3 — PRECONDITIONS
 remedy integrity check --json -> passed true; git status
 --porcelain empty; branch pushed. .agent/candidates.md still
 carries its F071-era content at this point (the new candidate set
 lands in the closure commit, PHASE 6) — assert, do not edit yet.

PHASE 4 — EVIDENCE JOB (fresh id, feature-scoped, NOT committed)
 Producer: packages.orchestration.job_evidence.
 create_manual_completion_bundle(review_feature_id="f075", ...),
 base 563b15b4 (the FULL 40-char sha), head = accepted HEAD
 (commit 2). Build the evidence dir OUTSIDE the repo (session
 scratch) — NEVER committed; the durable pointer is package +
 SHA-256 + job id in the STATUS line. Pitfalls, all asserted at
 authoring time (protocol §1): real node ids from --collect-only
 with len(node_ids) == passed per run; test_files are FILES
 (expand tests/docs/); run_id matches ^vr-\d{4,}$; full-length
 base_commit; output_hash OMITTED so the producer derives it; NO
 node id as an absolute path, NO slash inside a bracketed param
 id. Run coordinator validation over the produced bytes BEFORE any
 zip; a rejection -> record raw blocking_reasons in the handoff,
 fix at the cause, delete the rejected dir, rebuild.

PHASE 5 — REVIEW ZIP (mandatory, fresh, from the clean tree at
 accepted HEAD)
 git status clean + branch pushed, then:
 bash scripts/make_review_zip.sh --evidence-dir <path>
 Require: READY_FOR_REVIEW, review_subject_alignment PASS, evidence
 authoritative, committed_review_subject spans 563b15b4..accepted
 HEAD. Zip integrity (testzip) + import smoke over the PACKAGED
 sources (extract to tmp, import gauntlet_evaluator +
 gauntlet_orders + gauntlet_runner, confirm PASS_CRITERIA has 9
 members and GAUNTLET_ORDER_SET_VERSION == 4 there, remove tmp).
 Record package filename + SHA-256 (recompute independently).
 Failure -> STOP, raw error into the handoff, the feature does not
 close.

PHASE 6 — CLOSURE COMMIT + PR
 1. Apply f075-r13-3 -> docs/roadmap/STATUS.md with the four
    placeholders filled (evidence job id, zip filename, zip
    SHA-256, accepted HEAD = commit 2's full sha). The TO line is
    ONE line however it displays (the F071 wrap lesson).
 2. Apply BOTH f075-r13-4 edits -> README.md (same commit as
    STATUS — R-0154: README and STATUS never disagree in any
    committed state).
 3. Apply f075-r13-5 -> .agent/candidates.md (FULL replacement —
    the closure-candidate disk vehicle).
 4. Rewrite .agent/plan.md and .agent/context.md to their final
    F075-closed state (worker-authored, inside the allowed .agent/
    path set; KEEP the contract strings: plan "## Goal" +
    "## Next Steps" + an F-id; context "## Active Branch" +
    "feature/" + an F-id + "Steps" + the word "resource" or
    "pytest"; note F079 as next per Rule A5). Rewrite
    .agent/handoff.md per docs/agents/handback_template.md (all
    commits tabled; grep proof that every applied reviewer text is
    byte-identical to its authored file; the zip outcome recorded
    BEFORE handback). Update last_block OUTCOME.
 5. Commit 3 (the LAST commit, Rule A4) touches exactly
    docs/roadmap/STATUS.md, README.md and .agent/ state — nothing
    else. Gates (docs/roadmap touched): python3 -m pytest
    tests/docs/ -q AND the canary -> both exit 0. Push.
 6. gh pr create --base main (title: F075 — MILESTONE GATE: 10
    flawless self-runs; body: what/why — the gauntlet harness, the
    frozen order set + sample project, the nine campaign-earned
    product changes, the attempt history 0/10 -> 3/10 -> 10/10
    with matrices committed, ADR-0001 prepared NOT applied; key
    decisions R-0187/R-0188/R-0196/R-0197 pointers; how to review
    — start at .agent/gauntlet/attempt-03/matrix.md and
    docs/adr/0001-*; changed-files table; verdict PASS —
    INTEGRATION GATE FULL SUITE GREEN (15805/19, 0 branch-only);
    open findings 0 (R-0199 documented Medium risk, carried as a
    candidate); four closure candidates in .agent/candidates.md;
    runtime actuals: 13 rounds 2026-08-04..05, three live
    campaigns + seven --only re-proofs, tokens not-measured
    (ledger usage unreported by the local provider)). The PR is
    NOT merged — it merges at the next feature's Open PR Gate.
    Report the PR NUMBER in the completion report.
 Handback: completion report ending
 "F075 closure complete — PR #<n> open, awaiting the next Open PR
 Gate."

--- BEGIN f075-r13-1 sha256=67b700f9c7c98ecea146366fc760f029f08af3b36770d73ae95a6fa53854d1e0 ---
FROM (exact line, occurs once in .agent/live_review.md):
  LAST_REVIEWED_SHA = 05a15669.
TO:
  LAST_REVIEWED_SHA = 05a15669.
- R12: PASS — INTEGRATION GATE PASS (SPLIT, LARGE, 2026-08-05).
  Range 05a15669..8bc1305a (7 commits, all tabled). Transport:
  r12-1/2/3 cmp 0 against the reviewer's scratchpad originals AND
  against the applied files; the r12-2 corruption (ONE blank line
  dropped in transport) was caught by the sha256 check BEFORE
  anything was applied, isolated, restored, and re-verified — the
  R-0148 mechanism doing exactly its job; the archived block was
  corrected too (ba266dab). ADR-0001 verified: status PROPOSED,
  the diff applies cleanly and is NOT applied (CYCLE_SAFETY_CAP
  still 1 at source line 165, pinned by the new test until a
  human applies the ADR); the honest evidence-limit note (per-run
  cycle consumption unrecoverable, argued from the proven
  ceiling) accepted. INTEGRATION GATE: reviewer re-ran the FULL
  SUITE at HEAD personally: 15805 passed / 19 skipped, exit 0 in
  150s — matching the worker's branch run; base run raw records
  audited (6 failed / 15377 passed); comm -13 EMPTY (0
  branch-only), comm -23 = 6 ids, all
  test_live_state.py::TestUIServerIntegration, attributed to the
  known mid-run-UI-rebuild class on per-id direct evidence
  (identical dist content hash, mtimes inside the base run,
  serial re-run 16/16 green, no F075 commit touching apps/ui) —
  .agent/gate_f075_r12/attribution.txt. Flake debt: 6 base-only,
  under the 10-id escalation threshold; the recurring rebuild
  class goes to closure candidates. Worktree hygiene: the base
  gate worktree removed, pruned, branch deleted, primary only;
  porcelain empty. Only this round carries the full-suite claim:
  FULL SUITE GREEN. T003 complete — 10/10 stands, the ADR + diff
  are prepared. GATE VERDICT: PASS.
  LAST_REVIEWED_SHA = 8bc1305a.
--- END f075-r13-1 ---

--- BEGIN f075-r13-2 sha256=9c3e097e8794616caf00b8daefe35f702e8f3620ae00509ef56b67f747c53a72 ---

## Built State (accepted 2026-08-05, R1–R12)

Built and reviewed on branch feature/f075-self-run-gauntlet:

- **Harness** (packages/orchestration/): gauntlet_evidence
  (never-raising reader, R-0178/R-0183 honest numbers),
  gauntlet_evaluator (9 falsifiable criteria, era classes
  R-0141..R-0148 nameable, empty-set vacuous pass refused),
  gauntlet_matrix (deterministic md+json), gauntlet_orders
  (frozen set, manifest digests + set hash + template digest),
  gauntlet_injection (all four operator classes driveable,
  dispositions read off product facts), gauntlet_runner
  (per-run isolated data root + materialised sample-project
  workspace, real-root hash before/after, campaign-level crash
  containment). CLI scripts/self_run_gauntlet.py: --dry-run
  proof, --live campaign, --only, preflight refusals.
- **Order set v4** (scripts/gauntlet_orders/): ten missions,
  2x each kind, rationale + risk_probed + budget_rationale per
  order, all four injection classes exercised; frozen with the
  sample-project template (scripts/gauntlet_sample_project/,
  30-test green suite) under one set hash.
- **Product changes earned by the campaign** (each its own
  reviewed round): run_mission exception boundary with narrow
  retryable-class continuation and per-milestone streak
  escalation (R3/R11); transport/machine failure classes in
  failure_postmortem (R4); the loop executes what it dispatches
  via long_run_executor.run_cycles (R5); explicit
  experiment_max_cycles override — flag/config clamp untouched —
  and store_dod at dispatch + run_job_gate at production
  completion (R6); blocked-streak escalation (R7); released-gate
  dispatch guard (R8); refused-dispatch attribution fix (R9);
  released-gate context directive (R10); compiler milestone cap
  honoring the order's declared shape (R11).
- **The bar**: attempt 01 = 0/10, attempt 02 = 3/10, attempt 03
  = 10/10 FLAWLESS from ONE invocation — matrices KEPT under
  .agent/gauntlet/attempt-0{1,2,3}/. All four injections fired
  and settled retry_within_budget in attempt 03.
- **ADR-0001** (docs/adr/): raise CYCLE_SAFETY_CAP 1 -> 8,
  status PROPOSED, diff prepared and NOT applied, pinned by
  test until a human applies it.
- **Proof**: tests/orchestration/test_gauntlet_*.py +
  test_self_run_gauntlet.py (~470 across seven files), boundary
  and guard tests in test_orchestrator_loop.py, compiler-cap
  tests, executor-clamp pins. R12 integration gate: branch
  15805 passed / 19 skipped exit 0 (reviewer re-ran personally,
  identical); 0 branch-only failures; 6 base-only ids attributed
  to the known UI-rebuild class (.agent/gate_f075_r12/).

Honest boundary: the multi-cycle DEFAULT is still 1 everywhere —
ADR-0001 proposes the flip and a human applies it; the gauntlet's
experiment override is the only over-cap path and every use is
recorded in run evidence.
--- END f075-r13-2 ---

--- BEGIN f075-r13-3 sha256=b6ff64e8330e39dff83bff4898247a3903b3273caf05b53df2f499f03924f94b ---
FROM (exact line, occurs once in docs/roadmap/STATUS.md, replace once):
- [~] F075 — MILESTONE GATE: 10 flawless self-runs
TO (fill the four <PLACEHOLDERS> with real values, then apply):
- [x] F075 — MILESTONE GATE: 10 flawless self-runs (T001–T003 complete; accepted 2026-08-05 · live review PASS — ACCEPTED · Evidence job <EVIDENCE_JOB_ID> · package <ZIP_FILENAME> · SHA-256 <ZIP_SHA256> · accepted HEAD <ACCEPTED_HEAD>)
--- END f075-r13-3 ---

--- BEGIN f075-r13-4 sha256=91123541fd9bd7f634cdbc67ef3a50e43afafc40c2da7c982d24b991e7e2873d ---
EDIT 1 FROM (exact line, occurs once in README.md):
35 of 253 registered items accepted. Next: F075 (MILESTONE GATE: 10 flawless self-runs).
EDIT 1 TO:
36 of 253 registered items accepted. Next: F079 (Context handoffs).
EDIT 2 FROM (exact line, occurs once in README.md):
| 1 | Self-Build Bootstrap | 19 | 22 |
EDIT 2 TO:
| 1 | Self-Build Bootstrap | 20 | 22 |
--- END f075-r13-4 ---

--- BEGIN f075-r13-5 sha256=55af55f4d3a10d23ecbe54ee739d7619711e03a064957592a003dc0fffe2b030 ---
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- F070 was accepted with a specified execution step unbuilt (the
  multi-cycle executor call named in T1_F070.md Design): its
  zero-provider evidence never ran a job, so no test could notice.
  Review-practice/gate-tooling class: how closure evidence can
  prove a specified verb is actually CALLED, not merely present.
  Source: F075 R4 diagnosis · 2026-08-04.
- The move schema has no resume kind: a paused job's only forward
  path is re-dispatch, and a job that ended max_cycles_reached
  cannot be continued. Roadmap F045/F106 territory.
  Source: F075 R5/R6 · 2026-08-04.
- R-0199 (registered, deferred): the attempt-03 campaign read
  ~872 GB while writing ~2 MB. Reviewer hypothesis, unverified:
  gauntlet_runner.data_root_digest full-scans the operator's real
  data root before and after every run — cost scales with operator
  history. Needs a measured diagnosis + fix order (manifest-based
  digest or scoped root). Source: F075 R11 · 2026-08-05.
- The mid-run UI rebuild recurs: REMEDY_UI_NO_AUTO_BUILD=1 did not
  prevent a rebuild inside the R12 base gate run (6 base-only ids,
  identical dist content hash, mtimes inside the run) — the same
  class as the F069 R2 candidate. Suspect: a spawned server/build
  path not honoring the env var. Gate tooling, not F075 code.
  Source: F075 R12 gate · 2026-08-05.
--- END f075-r13-5 ---
