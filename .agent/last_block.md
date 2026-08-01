OUTCOME: executed — F061 CLOSED. Built State appended, preconditions green
(integrity passed=true, tree clean, branch pushed), Evidence job
c5185517fa2443bf, package remedy-review-20260801-190945-READY_FOR_REVIEW.zip
SHA-256 486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8,
STATUS [x] + README synced in one commit, PR opened and NOT merged.
Deviation: accepted HEAD is 8dc6086c (one extra content commit — the first
evidence bundle was rejected for path-shaped node ids; fixed at the source and
rebuilt). See .agent/handoff.md for raw transcripts and seven A9 deviations.

You are the WORKER for F061 — Definition-of-Done compiler (Tier 1), round R4:
  CLOSURE per docs/roadmap/STATUS_closure_protocol.md (v4) — read it and follow
  it exactly; this block orders the steps and carries the authored texts. Any
  precondition or zip failure → STOP per Failure honesty (the feature does NOT
  close; record the raw error in the handoff). Save THIS ENTIRE block verbatim
  to .agent/last_block.md first (append OUTCOME at handback).

  PHASE 1 — PERSIST THE R3 VERDICT (first commit)
  1. Save the four AUTHORED TEXT payloads below to
     .agent/authored/f061-r4-<n>.md (bytes between BEGIN/END markers,
     exclusive, including the final newline). Verify each sha256sum against
     its BEGIN-marker hash. Mismatch → STOP, report raw output, apply nothing.
  2. Apply f061-r4-1 → .agent/live_review.md by copy (cmp → 0).
  3. Commit 1: chore(f061): persist the R3 integration-gate verdict
     (.agent/authored/* + live_review + last_block; plan/context stay as-is —
     their Next Steps already name closure.)

  PHASE 2 — BUILT STATE (precondition 4, own commit)
  1. Append the BYTES of f061-r4-2 to the END of
     docs/roadmap/features/T1_F061.md (the authored text begins with a blank
     line; simple byte-append, no editing). Verify: the authored bytes occur
     in the file exactly once and the file ENDS with them.
  2. Commit 2: docs(f061): record the accepted Built State in the feature file
  3. Gate: python3 -m pytest tests/docs/ -q
           python3 -m pytest tests/cli/test_golden_path.py -q

  PHASE 3 — PRECONDITIONS
     remedy integrity check --json        → passed=true (record raw JSON)
     git status --porcelain               → empty
     git push -u origin feature/f061-dod-compiler
     Any failure → STOP.

  PHASE 4 — EVIDENCE JOB (feature-scoped)
     packages.orchestration.job_evidence.create_manual_completion_bundle(
     review_feature_id="f061", ...) — the full closed-schema gate set.
     Producer pitfalls (F051/F052 + F056's OWN failed first zip — avoid at
     authoring time, do not discover at zip time):
     - test_files lists SORTED, files only (expand directories);
     - output_hash = sha256 over the STORED 2000-char stdout_summary, not the
       untruncated log;
     - real node ids via --collect-only, len(node_ids) == selected;
     - VerificationTests run_id matches ^vr-\d{4,}$;
     - full-length base_commit SHA.
     Record: Evidence job <job_id>.

  PHASE 5 — REVIEW ZIP (mandatory, fresh; failure = closure BLOCKER)
     Tree clean, branch pushed, THEN:
     bash scripts/make_review_zip.sh --evidence-dir <the phase-4 evidence dir>
     Require: READY_FOR_REVIEW · is_valid_current_run true · validation_errors
     [] · ready_gate_matrix ok=true · zip import check passes ·
     committed_review_subject spans BASE(1869d89a)..accepted HEAD (= commit 2).
     Record package filename + SHA-256. A failed attempt is recorded in the
     handoff with its raw validation_errors BEFORE any retry; a rebuilt zip
     only after the failed one and its evidence dir are deleted.

  PHASE 6 — CLOSURE COMMIT + PR (last content commit, Rule A4 + R-0154)
  1. f061-r4-3: fill the four placeholders — <EVIDENCE_JOB_ID>,
     <ZIP_FILENAME>, <ZIP_SHA256>, <ACCEPTED_HEAD> (= the full sha of commit
     2, the reviewed head the zip covers) — then replace the FROM line in
     docs/roadmap/STATUS.md with the filled TO line. Grep proof required:
     substituting the four values back to their placeholders must yield bytes
     identical to the authored file's TO line; the FROM line is gone; no
     other STATUS line touched.
  2. f061-r4-4: apply EDIT 1 and EDIT 2 to README.md — SAME commit as the
     STATUS edit (R-0154 pin). Verify both FROM lines gone, both TO lines
     present exactly once.
  3. Rewrite .agent/handoff.md (completion report incl. all raw transcripts,
     authored-text proofs, deviations) + last_block OUTCOME — same commit.
     Commit 3: chore(f061): close F061 — STATUS [x] + README sync
     This commit touches exactly: docs/roadmap/STATUS.md, README.md, .agent/.
  4. Gate: python3 -m pytest tests/docs/ -q
           python3 -m pytest tests/cli/test_golden_path.py -q
  5. git push, then gh pr create --base main. PR description: what/why, key
     decisions (DoDDraft honesty split, one-seam gate, dod_draft_v1
     non-registration, structured_base extraction), how to review,
     changed-files table, latest verdict (R3 FULL SUITE GREEN, both sides
     clean), open findings 0 (R-0164/R-0165 resolved), runtime actuals:
     4 rounds R1–R4 on 2026-08-01, tokens/cost not-measured. Honest boundary
     line: DoD compilation is not yet wired into job creation (F062/F069/F070
     scope). Record the PR number. DO NOT MERGE — the PR merges at the next
     feature's Open PR Gate.

  Handback: completion report + the rewritten .agent/handoff.md as ordered in
  Phase 6. The reviewer then verifies closure and ends the session.
  ──────────────────────────────────────────────────────────────

  ----- BEGIN AUTHORED f061-r4-1 sha256=1d12e62d274729984399ec5050b594c1be42f2dca56075a4505f277a23edec10 -----
  # Live Review — F061 Definition-of-Done compiler (Tier 1)

  Branch: feature/f061-dod-compiler
  Scope: user intent + Flight Plan compile into a machine-checkable DoD
  (versioned schema; checks with blocking flags); runners execute checks
  with per-check evidence; the job-end gate holds a job open on a red
  blocking check. Compiler is an LLM step with intake/plan discipline:
  schema-enforced, parse-retried, honest deterministic fallback labeled
  compiled=false.

  ## Steps
  - R1 (LARGE): T001 schema + compiler + fallback + fixtures +
    traceability, T002 runners red+green per kind — PASS.
  - R2 (LARGE): R-0164 fix, T003 runtime_flow runner + T004 job-end
    gate + report matrix + `remedy job dod` + end-to-end — PASS.
  - R3: R-0165 fix, dod_v1 SCHEMA_REGISTRY registration, integration
    gate per docs/agents/integration_gate.md — PASS.
  - R4: closure per docs/roadmap/STATUS_closure_protocol.md v4:
    Built State → preconditions → evidence job → fresh review zip →
    closure commit (STATUS [x] + README sync + final .agent state) →
    PR (merge deferred to the next feature's Open PR Gate).

  ## Findings
  - Resolved: R-0164 (hardening, Low) 2026-08-01: flag-shaped first
    tokens (pytest selector, lint/build tool, custom_cmd argv[0])
    passed compile-time validation. Fixed: _reject_flag_shaped on the
    three fields + negative tests. Done: R-0164 (commit af5c39d7).
  - Resolved: R-0165 (hardening, Low) 2026-08-01: the runtime_flow v1
    vocabulary was runner-enforced only; the schema accepted any step
    with a non-empty action. Fixed: _validate_flow_step (action ==
    "open", path starts with "/", closed key set, typed expectations,
    index-named messages); the runner guard stays as defence for DoDs
    stored before the rule, proven via legacy_flow/model_construct.
    Done: R-0165 (commit d5604c51).
  - Next free ID: R-0166.

  ## Verdicts
  - R1: PASS (SPLIT round, 2026-08-01). Range 1869d89a..785f8cbd.
    Scoped 89 + docs 293 + canary 42, all reviewer-run, exit 0;
    transport cmp 0 disk-to-disk (all four texts, scratchpad
    originals); A9 deviations 1–10 accepted; R-0164 registered.
    LAST_REVIEWED_SHA = 785f8cbd.
  - R2: PASS (SPLIT round, 2026-08-01). Range 785f8cbd..ef60758b.
    Reviewer re-ran: scoped 140 + adjacent 177, exit 0. Seam audited
    in situ: RunState.COMPLETED reachable only through the gate-guarded
    branch; hold routes through the existing blocked machinery; no-DoD
    returns None (additive). End-to-end drives the real
    run_job_fulfill (hold, release, matrix, timeline event).
    Deviations 1–11 accepted; R-0164 verified fixed; R-0165
    registered. LAST_REVIEWED_SHA = ef60758b.
  - R3: PASS — INTEGRATION GATE PASS (reviewer, 2026-08-01). Range
    ef60758b..f6a05214. Branch full suite: worker 14900 passed / 19
    skipped exit 0 @ aebc3c11; the reviewer's OWN run at HEAD 14900
    passed / 19 skipped, exit 0 in 138s. Base @ merge base 1869d89a in
    a throwaway worktree on a throwaway branch (parity restored by
    COPYING apps/ui/node_modules + apps/ui/dist,
    REMEDY_UI_NO_AUTO_BUILD=1): 14744 passed / 19 skipped, exit 0 —
    fully green, so comm -13 AND comm -23 are both EMPTY; nothing to
    attribute on either side. Count delta +156 = F061's own tests.
    Flake debt 0 (threshold >10 not met). R-0165 verified fixed in the
    diff and marked Done; dod_v1 registered with the structured_base
    extraction accepted (cycle proven with the raw ImportError, both
    in-package alternatives shown failing, re-exports keep every
    existing import working, verified from all four entry points);
    dod_draft_v1 deliberately NOT registered — the registry resolves
    tags readers encounter, and no reader ever loads a draft; the
    absence is pinned by test. Deviations 1–6 accepted, incl. the
    pre-existing dag_schedule.py ruff error left alone (reproduced at
    base) and the legacy_flow test adjustment (the only way to reach
    the runner's surviving guard post-R-0165). Transport: all three
    texts cmp 0 disk-to-disk; live_review differs by exactly the
    ordered Done line. Gate worktree removed + pruned, tmp branch
    deleted, `git worktree list` proof recorded. Only this round
    carries the full-suite claim: FULL SUITE GREEN.
    LAST_REVIEWED_SHA = f6a05214.
  ----- END AUTHORED f061-r4-1 -----

  ----- BEGIN AUTHORED f061-r4-2 sha256=c3a5bd8da1cb98c31ce26d6811c3b66a770c128fa6cb78c5e50d8d601c186165 -----

  ## Built State (accepted 2026-08-01, F061 closure)
  - **Schema** (`packages/orchestration/dod_schema.py`): `DoD` (`dod_v1`,
    registered in `SCHEMA_REGISTRY`) and the provider-facing `DoDDraft`
    (`dod_draft_v1`, deliberately unregistered — no reader ever resolves
    it; absence pinned by test). Honesty is structural: the draft cannot
    carry `source` or claim `compiled`; `compiled` must equal
    `origin == "provider"`. Compile-time validation refuses detectable
    nonsense: empty/flag-shaped selectors and tools, empty argv, cwd
    escapes, unknown keys, and (R-0165) the closed runtime_flow v1 step
    vocabulary (`open` + path + typed expectations).
  - **Compiler** (`dod_compiler.py`): three merged sources — provider
    checks via `run_structured_call` (one parse retry), one generated
    check per uncovered plan acceptance line (grouped by selector), and
    the `register_standard_check_provider` seam (F062 plugs in here).
    The traceability rule (verbatim, tested against this file): every
    plan acceptance line traceable to a check id. No provider → a
    deterministic DoD from the acceptance lines, labeled
    `compiled=false`; every fallback route tested.
  - **Runners** (`dod_runners.py`): pytest/lint/build/custom_cmd as
    single processes under the shared executable allowlist and worktree
    fence, each proven red and green; `runtime_flow` (T003) drives the
    F007 harness — resolve spec, start in its own session, readiness
    probe, declarative steps, stop-process-tree in a `finally`; a
    surviving process is red. Named red reasons throughout; a missing
    tool is red `tool_unavailable`, never a pass; a kind without a
    runner raises `UnsupportedCheckKindError`.
  - **Gate** (`dod_gate.py` + ONE seam in
    `job_fulfillment.run_job_fulfill`): on the terminal-green path, any
    red BLOCKING check holds the job open through the existing blocked
    machinery (`dod_blocking_red:` blocker); non-blocking reds are
    reported, never gating; an unreadable stored DoD fails closed. A job
    with no stored DoD is not gated (additive; `dod_released=None`).
    End-to-end proven on the real fulfillment path: hold, then release
    after the fix on the same job. DoD + gate result live in the job's
    evidence area (`dod.json`, `dod_result.json`), never the user repo.
  - **Surface**: report section "Definition of Done" with the check
    matrix (absent source renders `not recorded`); `remedy job dod <id>`
    prints the matrix read-only.
  - **Boundaries (honest)**: nothing calls `compile_dod` at real job
    creation yet — F062 registers the product-smoke standard check and
    F069/F070 wire compilation into the mission/orchestrator flow; the
    flow vocabulary is v1 (`open` only) by design.
  ----- END AUTHORED f061-r4-2 -----

  ----- BEGIN AUTHORED f061-r4-3 sha256=45212872599183cb674e4d2795395a0761e0d71b57361cca4cbbb9fbbbed152d -----
  FROM (exact line, occurs once in docs/roadmap/STATUS.md, replace once):
  - [~] F061 — Definition-of-Done compiler
  TO (fill the four <PLACEHOLDERS> with real values, then apply):
  - [x] F061 — Definition-of-Done compiler (T001–T004 complete; accepted 2026-08-01 · live review PASS —
  ACCEPTED · Evidence job <EVIDENCE_JOB_ID> · package <ZIP_FILENAME> · SHA-256 <ZIP_SHA256> · accepted HEAD
  <ACCEPTED_HEAD>)
  ----- END AUTHORED f061-r4-3 -----

  ----- BEGIN AUTHORED f061-r4-4 sha256=0dbdb6eed0f24a458c3beaf33fc182fadf5d8fdb25579d11bdf7f9811d3f3876 -----
  EDIT 1 FROM (exact line, occurs once in README.md):
  30 of 252 registered items accepted. Next: F061 (Definition-of-Done compiler).
  EDIT 1 TO:
  31 of 252 registered items accepted. Next: F062 (Product smoke as the closing gate).
  EDIT 2 FROM (exact line, occurs once in README.md):
  | 1 | Self-Build Bootstrap | 14 | 22 |
  EDIT 2 TO:
  | 1 | Self-Build Bootstrap | 15 | 22 |
  ----- END AUTHORED f061-r4-4 -----
