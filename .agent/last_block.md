You are the worker for F079 R4 (SPLIT round): CLOSURE PART 1 —
evidence job + fresh review zip per
docs/roadmap/STATUS_closure_protocol.md. R3 verdict: PASS, integration
gate passed, full suite green. Read the protocol file before acting.
The STATUS [x] line is NOT written this round — the reviewer authors
it from the values your handback reports, and part 2 applies it.
If anything below goes red: STOP per AGENTS.md If-Blocked, hand back
with the raw output. A failing zip build is a closure BLOCKER.

── STEP closure-1/2 — F079 ──────────────────────────────────
Goal:        Persist the R3 gate verdict, land the Built State
             section, satisfy the closure preconditions, produce the
             evidence job and the fresh review zip.
Bundle:      1 state commits · 2 Built State · 3 preconditions ·
             4 evidence job · 5 review zip · 6 handback
Change:      .agent/** state files and
             docs/roadmap/features/T1_F079.md (append) ONLY. No
             STATUS.md, no README.md, no source, no tests.
Constraints: Evidence dir lives in session scratch OUTSIDE the repo
             and is NEVER committed (a committed dir turns the
             package BLOCKED_EVIDENCE — F147 attempt-2). Commits
             < 500 lines each; the last_block save rides alone.
Done when:   Integrity check PASS, bundle complete, zip import check
             green, package + SHA-256 recorded.
Handback:    Completion report + rewrite .agent/handoff.md (see 6).
──────────────────────────────────────────────────────────────

1. STATE COMMITS (persist FIRST)
   Three authored texts follow at the bottom, delimited by BEGIN/END
   markers. Authored bytes = everything BETWEEN the marker lines,
   including the final newline; markers are never content.
   a. COMMIT A: this entire prompt saved verbatim to
      .agent/last_block.md (own commit).
   b. Save to .agent/authored/f079-r4-{1,2,3}.md; verify each with
      sha256sum against its BEGIN-marker hash. Mismatch → STOP, hand
      back naming block and both hashes; apply nothing.
      COMMIT B: the three authored files.
   c. Apply: f079-r4-1 replaces .agent/live_review.md entirely;
      f079-r4-2 replaces .agent/plan.md entirely. COMMIT C: exactly
      these two files, message
      "chore(f079): persist R3 gate PASS (full suite green) +
      closure plan".

2. BUILT STATE (content commit — precondition 4)
   Apply f079-r4-3 as an APPEND to
   docs/roadmap/features/T1_F079.md (the file currently ends after
   the "Do not touch" section; the authored text begins with a blank
   line — append as-is). COMMIT D: exactly this file, message
   "docs(f079): Built State — composer, triggers, consumption,
   recall eval, R-0199 fix".
   GATES (docs round): python3 -m pytest tests/docs/ -q → exit 0;
   python3 -m pytest tests/cli/test_golden_path.py -q → exit 0.
   Red → STOP.

3. PRECONDITIONS (protocol head)
   a. remedy integrity check --json → record the RAW output; must be
      PASS. Not PASS → STOP, hand back the output.
   b. git status --porcelain → empty; no relevant untracked files.
   c. git push (branch up to date; the zip records committed state).

4. EVIDENCE JOB (protocol algorithm step 1)
   Produce the final evidence bundle with the canonical producer:
   packages.orchestration.job_evidence.create_manual_completion_bundle
   with review_feature_id="f079", writing into a NEW evidence dir
   under the session scratchpad (outside the repo). Honor the named
   producer pitfalls from the protocol, at authoring time:
   - verification_runs: sha256-hex output_hash, valid
     VerificationTests totals, FULL-length base_commit (38854f60's
     full sha via `git rev-parse 38854f60`);
   - (a) non-empty test node ids with len(node_ids) == selected —
     take real ids from `pytest --collect-only -q`;
   - (b) test_files are FILES, never directories;
   - (c) run_id matches ^vr-\d{4,}$.
   Feed it the real gate numbers (R3: branch 15853 passed/19
   skipped; base 15805 passed/19 skipped; canary 42) — never
   invented totals. Record the job id.

5. REVIEW ZIP (protocol algorithm step 2 — MANDATORY, fresh)
   From the clean tree at the content HEAD (after COMMIT D):
   bash scripts/make_review_zip.sh --evidence-dir <the dir from 4>
   Verify: committed_review_subject spans <full sha of 38854f60>..
   <current HEAD> and the zip import check passes. Record the
   printed package filename and SHA-256 EXACTLY (they go verbatim
   into the STATUS line). Zip failure → STOP, hand back the raw
   error; do not retry blind.

6. HANDBACK
   Canary already ran in 2; re-run if any commit followed it. Final
   git status --porcelain → empty. Rewrite .agent/handoff.md (last
   commit) with:
   - changed-files table per commit,
   - raw transcripts: docs gate, canary, integrity check --json
     output, the producer invocation + its stdout, the zip build
     tail (package + SHA-256 + import check),
   - the four values the reviewer needs VERBATIM on one line each:
     evidence job id · package filename · SHA-256 · content HEAD
     (full sha at handback, before the handoff commit — state both
     if the handoff commit moves HEAD),
   - item status. NO STATUS edit, NO README edit, NO PR — part 2.

AUTHORED TEXTS

<<<BEGIN AUTHORED f079-r4-1
sha256=f883c986a24ba50a45bf6a060ce3631b860bf425de4e423792d469cc79619447>>>
# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. T001–T003 built and
verified; integration gate PASSED. Closure runs in two relays because
the STATUS line quotes the evidence job, package and hash — the
reviewer can only author it after they exist.

## Steps
- R1 (SPLIT, LARGE): claim + candidate sweep + R-0199 diagnosis +
  reuse inspection + T001 — PASS, see Verdicts.
- R2 (SPLIT, LARGE): R-0199 fix + T002 + T003 — PASS, see Verdicts.
- R3 (SPLIT): INTEGRATION GATE — PASS, FULL SUITE GREEN, see
  Verdicts.
- R4 (SPLIT, current): closure part 1 — Built State section, closure
  preconditions, evidence job, fresh review zip. Awaiting handback
  with job id, package and SHA-256.
- R5: closure part 2 — authored STATUS [x] + README sync + candidate
  re-emit + closure commit + PR, per
  docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0199 (harness perf, Medium — carried from F075): FIXED in R2
  (metadata-manifest digest, 34.611 s vs 394.8 s baseline, consumer
  audit verified). Done: R-0199
- R-0200 (process/gate-tooling, Medium): F070 verb-called gate half.
  Deferred, OPEN — re-emits to .agent/candidates.md at closure.
- R-0201 (roadmap routing): resolved by routing in R1 (T3_F106.md).
  Resolved.
- R-0202 (gate tooling, Low): mid-run UI rebuild env-var class.
  Deferred, OPEN — did NOT recur in the R3 gate (dist hashes
  identical on both sides); one clean gate is not the env-var hunt;
  re-emits to .agent/candidates.md at closure.
- R-0203 (design, Low): root discipline at the consumption seam.
  FIXED in R2. Done: R-0203
- Next free ID: R-0204.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-06). Range 38854f60..79621fc0.
  Full text in this file's git history (commit b3a0291e).
- R2: PASS (SPLIT, LARGE, 2026-08-06). Range 79621fc0..0938884f.
  Full text in this file's git history (commit 561e401b).
- R3: PASS — INTEGRATION GATE PASS (SPLIT, 2026-08-06). Range
  0938884f..a11d1f74 (6 commits, all tabled; no source or test file
  touched). Transport: f079-r3-1/2 cmp 0 against the reviewer's
  scratchpad originals; both applied state files byte-equal their
  authored texts. Gate evidence audited in .agent/gate_f079_r3/:
  raw logs (branch 15853 passed / 19 skipped, 141 s; base @
  38854f60 15805 passed / 19 skipped, 132 s; both exit 0), failed
  lists EMPTY on both sides, comm -13 and comm -23 EMPTY,
  ids_base_only EMPTY, and the 48 branch-only ids reconcile exactly
  (15853-15805 = 15872-15824 = 48): 39 test_handoff.py ids (file
  absent at the merge base — 0 commits, re-verified by the
  reviewer), 5 TestHandoffCommand ids, 4 digest-test ids — all
  attributed to the three new-test commits. Step-3 dist hashes
  identical before/after on both sides: the R-0202 class did NOT
  recur and the parity claim stands. The reviewer re-ran the FULL
  SUITE personally at HEAD: 1 failed / 15852 passed — the single id
  (test_run_manifest_logical_identity.py::TestTwoRealRunsShare
  LogicalIdentity::test_different_execution_identities_same_
  logical_hash) re-run serially passed (file: 11 passed), and the
  file is untouched in 38854f60..HEAD (0 commits) — xdist-flake
  class per integration_gate.md step 4: recorded, not a blocker;
  1 id, far under the 10-id flake-debt threshold; goes to closure
  candidates for the flake ledger. Canary 42 re-run by the
  reviewer; porcelain empty; primary worktree only, base worktree
  removed and pruned. Only this round carries the claim: FULL SUITE
  GREEN. GATE VERDICT: PASS. LAST_REVIEWED_SHA = a11d1f74.
<<<END AUTHORED f079-r4-1>>>

<<<BEGIN AUTHORED f079-r4-2
sha256=16bce73d69dd46de382cb45cddb877b7d5880546ead651b95f5603d354154d62>>>
# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Close F079 per docs/roadmap/STATUS_closure_protocol.md. Substance is
done and gated: T001 composer, T002 triggers + consumption + reference
verification, T003 measured boundary recall (100 % open items),
R-0199 fixed, integration gate PASS (full suite green, both sides,
all 48 differing ids attributed).

## Current Step
R4 — closure part 1: Built State section into T1_F079.md (content
commit, before the zip), closure preconditions (integrity check,
clean tree), evidence job via create_manual_completion_bundle
(review_feature_id=f079), fresh review zip from the clean content
HEAD. Handback carries job id, package filename, SHA-256 and the
content HEAD — the reviewer authors the STATUS line from them.

## Next Steps
- R5 — closure part 2: apply the authored STATUS [x] line + README
  ledger sync (same commit), re-emit R-0200/R-0202 + the R3 flake
  observation to .agent/candidates.md, final .agent state, closure
  commit (STATUS.md + README.md + .agent/** only), push, PR. The PR
  merges at the next feature's Open PR Gate.

## Risks
- Packaging pitfalls are known and named in the protocol: sha256
  output_hash, full-length base_commit, real node ids with
  len == selected, test_files are files, run_id matches ^vr-\d{4,}$.
- The evidence dir stays OUTSIDE the repo (session scratch, never
  committed) — a committed dir turns the package BLOCKED_EVIDENCE.
- A failing zip build is a closure BLOCKER: stop, hand back raw.
<<<END AUTHORED f079-r4-2>>>

<<<BEGIN AUTHORED f079-r4-3
sha256=ae6e99fe3784cd20e2cea3e9d4e3c70fca59c5582dccf8ada47691072a82894b>>>

## Built State (accepted 2026-08-06, R1–R3)

Built and reviewed on branch feature/f079-context-handoffs:

- **Composer** (packages/orchestration/handoff.py, T001):
  HANDOFF_SCHEMA_VERSION = 1; build_handoff(mission_id) composes
  handoff_v<N>.json plus the rendered handoff_v<N>.md (fixed section
  order, dossier first) into the mission's evidence area
  (mission_state.mission_evidence_dir — the dossier's own path
  scheme and _v<N> accumulation precedent). Idempotent per state: no
  wall-clock reads in content, a repeat build on unchanged state
  returns the existing file, changed state accumulates the next
  version. Missing sources are NAMED gaps (GAP_* constants), never
  invented content; a zero-progress mission is a valid handoff.
  Redaction reuses run_manifest.is_secret_key and stream_evidence's
  redactors. Building is a pure artifact — pinned by a
  before/after-snapshot test.
- **Triggers** (T002): explicit `remedy mission handoff <id>`
  (command_catalog `mission.handoff` + mission_cmd handler,
  supports --json) and the loop boundary:
  orchestrator_loop.build_boundary_handoff runs at
  TERMINAL_ITERATION_LIMIT and TERMINAL_STOPPED; a build failure
  lands in MissionRunResult.handoff_error and nowhere else — the
  terminal is never masked.
- **Consumption** (T002): handoff_resume_seed seeds iteration one of
  a resumed mission (SECTION_HANDOFF, first iteration only); the
  newest readable handoff wins and is logged; an unknown
  schema_version refuses (HandoffSchemaVersionError); the checkpoint
  reference is verified with the checkpoint feature's own rules, and
  a moved worktree refuses with checkpoints.worktree_drift_message —
  extracted in this feature so `remedy job resume` and handoff
  consumption share ONE wording. Root discipline documented
  (R-0203; handoff_root_conflict names a mission-root/data-root
  split). Automatic in-flight context-pressure detection is
  deliberately unbuilt and documented in the module docstring.
- **Recall eval** (T003): run_boundary_recall_eval reuses the
  dossier's run_recall_harness, RECALL_FIXTURE_FACTS and
  recall_report verbatim, forces a real boundary and measures the
  seed alone; threshold RECALL_THRESHOLD_OPEN_ITEMS = 1.0, inherited
  from the dossier's open/resolved asymmetry; the report is archived
  as handoff_recall_eval.md beside the handoffs it measures.
  Measured: 100 % open recall on the fixture facts.
- **R-0199** (carried from F075, fixed here):
  gauntlet_runner.data_root_digest hashes a sorted metadata manifest
  (relpath, size, mtime_ns), value prefixed `meta-sha256:`; measured
  34.611 s per call against the 394.8 s content-hash baseline,
  content bytes read per call ~143.66 GB -> ~0; per-run frequency
  and evidence field names unchanged.
- **Tests**: tests/orchestration/test_handoff.py (39),
  digest tests in tests/orchestration/test_gauntlet_runner.py (4),
  TestHandoffCommand in tests/cli/test_mission_cmd.py (5).
  Integration gate (R3): branch 15853 passed / base 15805 passed,
  zero failures on both sides, all 48 differing ids attributed to
  the three new-test commits; dist hashes unchanged (R-0202 did not
  recur).
<<<END AUTHORED f079-r4-3>>>
