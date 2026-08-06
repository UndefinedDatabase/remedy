You are the worker for F079 R2 (SPLIT round, LARGE). R1 verdict: PASS.
Reviewer gates the handback; you never write verdicts and never merge.
Authority: AGENTS.md. Spec: docs/roadmap/features/T1_F079.md. If any
verification below goes red: STOP at that point per AGENTS.md
If-Blocked, commit what is green, hand back with the raw failure — do
not continue into the next slice.

── STEP R-0199+T002+T003/3 — F079 ───────────────────────────
Goal:        Persist the R1 verdict, fix R-0199 (metadata-manifest
             digest), build T002 (triggers + loop consumption +
             reference verification) and T003 (boundary recall eval).
Bundle:      1 state commits · 2 R-0199 fix · 3 T002 · 4 T003 ·
             5 handback
Change:      .agent/** state files,
             packages/orchestration/gauntlet_runner.py (digest only),
             packages/orchestration/handoff.py, the CLI module that
             carries mission commands, orchestrator loop termination
             seam, tests. Nothing else.
Constraints: Do-not-touch per T1_F079.md. Reuse mandated: checkpoint
             verification, recall harness — new implementations of
             existing pieces are rejects. Commits < 500 lines each
             (the last_block save rides alone, R-0198 rule). Primary
             checkout porcelain-empty at handback. Mutation/red-proof
             checks, if any, only in a disposable git worktree.
Done when:   All verifications below exit 0, in order.
Handback:    Completion report + rewrite .agent/handoff.md (see 5).
──────────────────────────────────────────────────────────────

1. STATE COMMITS (persist FIRST, before any fix)
   Two authored texts follow at the bottom, delimited by BEGIN/END
   marker lines. Authored bytes = everything BETWEEN the marker
   lines, including the final newline; markers are never content.
   a. COMMIT A: this entire prompt saved verbatim to
      .agent/last_block.md (own commit).
   b. Save the bytes to .agent/authored/f079-r2-1.md and
      .agent/authored/f079-r2-2.md; verify each with sha256sum
      against the sha256 in its BEGIN marker. Mismatch → STOP, hand
      back naming the block and both hashes; apply nothing.
      COMMIT B: the two authored files.
   c. Apply: f079-r2-1 replaces .agent/live_review.md entirely;
      f079-r2-2 replaces .agent/plan.md entirely. COMMIT C: exactly
      these two files, message
      "chore(f079): persist R1 PASS verdict + R2 plan (R-0199 fix
      ordered, R-0203 registered)".

2. R-0199 FIX — data_root_digest becomes a metadata manifest
   File: packages/orchestration/gauntlet_runner.py, function
   data_root_digest (line ~91). The R1 diagnosis (handoff.md of R1)
   measured 394.8 s per call, ~2.9 TB read per campaign, with
   job_workspaces at 99.80 % of bytes.
   a. FIRST inspect every consumer of the digest value and the
      data_root_hash_before/after fields: rg through
      gauntlet_evaluator.py, gauntlet_evidence.py, gauntlet_matrix.py
      and tests/. List them in the handback. Field NAMES and per-run
      call frequency stay unchanged; only the digest definition
      changes.
   b. Reimplement: sha256 over the sorted manifest of
      "relpath\tsize\tmtime_ns" lines for every file under the root —
      NO content reads. Prefix the value "meta-sha256:" so an old
      content digest can never be compared equal to a new one.
      Docstring states the honest contract: detects add, remove,
      move, resize and mtime change; does NOT detect a content edit
      that forges identical size and mtime_ns — the isolation proof's
      threat model is accidental writes, not forgery. Cite R-0199.
   c. Unit tests (same test home the runner already uses): unchanged
      tree → stable digest across calls; add / remove / move /
      resize / mtime-touch → digest changes; value carries the
      meta-sha256: prefix.
   d. Time ONE call of the new digest on the real data root
      (throwaway script outside the repo, deleted after; the R1
      baseline was 394.8 s content / 66.8 s walk-only). Record the
      seconds in the handback — that number is the fix's proof.
   VERIFY: the runner's test file(s) you touched, e.g.
   python3 -m pytest tests/orchestration/test_self_run_gauntlet.py -q
   plus the digest tests → exit 0. Red → STOP.

3. T002 — triggers + loop consumption + reference verification
   a. Explicit trigger: `remedy mission handoff <mission-id>` —
      follow the EXISTING mission-command registration pattern in the
      CLI (locate it; name it in the handback). Calls build_handoff,
      prints the artifact path, exits nonzero with the
      MissionForHandoffNotFoundError message for an unknown mission.
   b. Loop trigger: when the orchestrator loop terminates for limits
      or stop, it builds a handoff — every pause becomes resumable.
      A handoff-build failure must NOT mask the terminal outcome:
      catch, record honestly (event/log surface the loop already
      has), terminate as before. Name the exact seam (file:line) in
      the handback.
   c. Consumption: the loop's context assembly accepts a handoff as
      the seed for iteration one of a RESUMED mission. Rules:
      newest valid handoff wins and which one is logged; unknown
      schema_version → refuse (HANDOFF_SCHEMA_VERSION consumers must
      not guess); before trusting the narrative, verify the
      checkpoint reference with the EXISTING checkpoint rules
      (checkpoints.py load path + resolve_live_worktree_head) — a
      stale worktree head refuses with the checkpoint feature's own
      message, never a new one. R-0203 constraint: resolve ALL
      sources through one root discipline; document it at the
      consumption seam.
   d. Automatic in-flight context-pressure detection stays unbuilt —
      note it in the module docstring where consumption lands (the
      feature file demands the documentation).
   Tests: extend tests/orchestration/test_handoff.py (+ a CLI test
   beside the existing mission-command tests): explicit trigger
   writes the artifact; loop-limit termination writes one; build
   failure does not change the terminal; resume seeds from newest
   valid; stale head refuses with the checkpoint message; unknown
   schema_version refuses.
   VERIFY: python3 -m pytest tests/orchestration/test_handoff.py -q
   and the CLI test file you touched → exit 0. Red → STOP.

4. T003 — the boundary recall eval (acceptance heart)
   Reuse the dossier's recall harness VERBATIM:
   mission_dossier.run_recall_harness + RECALL_FIXTURE_FACTS (10
   seeded facts) + recall_report — a new harness is a reject. Eval:
   fixture mission on the fake provider, seed the facts, force a
   boundary (build the handoff), resume in a fresh context FROM THE
   HANDOFF ALONE, assert the documented recall threshold on OPEN
   items (resolved items may compress — the dossier's own
   asymmetry; reuse its documented threshold and cite where it is
   documented). Archive the eval report into the mission's evidence
   area — that archived report is closure evidence.
   Tests: the eval runs in test_handoff.py (or its own test file
   beside it), asserts the threshold and the archived report's
   existence and content.
   VERIFY: python3 -m pytest tests/orchestration/test_handoff.py -q
   (full file) → exit 0. Red → STOP.

5. HANDBACK
   Canary: python3 -m pytest tests/cli/test_golden_path.py -q →
   exit 0. git status --porcelain → empty. Push the branch (no PR —
   closure creates it). Rewrite .agent/handoff.md (last commit) with:
   - changed-files table per commit (path, +/-, reason),
   - raw transcripts: every verification command, exit code, tail,
   - the R-0199 consumer list (2a) and the new-digest timing (2d),
   - the CLI pattern followed (3a) and the loop seam file:line (3b),
   - reused pieces named for T002/T003 (checkpoint rules, recall
     harness, threshold citation),
   - item status per slice (done / stopped-at with the red output).
   No verdict, no merge, no STATUS edits.

AUTHORED TEXTS

<<<BEGIN AUTHORED f079-r2-1
sha256=8077b273a9f909e51ca3c50f0ca3b7330428a1b44b1d3e7fc5cd7e0d5bf79cde>>>
# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. The F075 candidate
sweep (4 entries) was registered/resolved in R1 per
docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate findings").

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#180) + STATUS claim + candidate
  sweep + R-0199 measured diagnosis + reuse inspection + T001 —
  PASS, see Verdicts.
- R2 (SPLIT, LARGE, current): R-0199 fix (metadata-manifest digest)
  + T002 (triggers + loop consumption + reference verification)
  + T003 (boundary recall eval + threshold). Awaiting handback.
- R3 (planned): integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md — its own
  round, never bundled.

## Findings
- R-0199 (harness perf, Medium — carried from F075, ID spent there):
  diagnosis MEASURED in the F079 R1 handback, mechanism confirmed —
  two production call sites (gauntlet_runner.py:461 before, :533
  after, always), root resolves to the operator's real .data
  (143.66 GB / 2,495,115 files at measurement), one content-hash call
  = 394.8 s, 20 calls per 10-order campaign ≈ 2.9 TB read / ~2.2 h
  pure hashing; job_workspaces holds 99.80 % of the bytes; the
  attempt-03 ~872 GB observation is consistent with the mechanism at
  that date's root size. FIX ORDERED in R2: data_root_digest becomes
  a metadata-manifest digest (relpath, size, mtime_ns — no content
  reads), per-run call frequency and evidence field names retained.
  DECISION (alternatives considered: campaign-level frequency —
  rejected, loses per-run attribution; scoping the root past
  job_workspaces — rejected, that subtree is exactly where a
  violation would land; keeping content hashing — rejected, 6x the
  wall clock for a threat model of accidental writes). Reversal: any
  later relay may reinstate content hashing.
- R-0200 (process/gate-tooling, Medium): F070 verb-called gate half.
  Deferred, OPEN — unchanged from R1; rolls to candidates at closure
  if unbuilt.
- R-0201 (roadmap routing): resolved by routing in R1 — scope note
  landed in docs/roadmap/features/T3_F106.md. Resolved.
- R-0202 (gate tooling, Low): mid-run UI rebuild env-var class.
  Deferred, OPEN — unchanged from R1; rolls to candidates at closure
  if unbuilt.
- R-0203 (design, Low) 2026-08-06, reviewer-registered at the R1
  review: handoff.py's `root` parameter reaches mission/dossier/output
  paths, but the job-side sources (checkpoints, storage, run events)
  resolve the env-rooted data root — consistent only when both point
  at the same place (the tests pin this via REMEDY_DATA_DIR). Matches
  the existing env-rooted API shape; not a defect today. Disposition:
  constraint carried into the T002 order (consumption resolves ALL
  sources through one root discipline and documents it); closes with
  T002.
- Next free ID: R-0204.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-06). Range 38854f60..79621fc0
  (6 commits, all tabled). Transport: f079-r1-1..6 cmp 0 against the
  reviewer's scratchpad originals (primary proof); every applied
  state file byte-equals its authored text; the STATUS claim and the
  T3_F106 append verified in place. Reviewer re-ran the gates
  personally: tests/docs 293 passed, canary 42 passed, test_handoff
  23 passed — all exit 0; porcelain empty; `git worktree list` =
  primary only. handoff.py and test_handoff.py read in full:
  composition only — dossier renderer, checkpoint loader, decision
  queue, event/job loaders and both redactors reused, every reuse
  claim spot-checked at its file:line; pure artifact pinned by the
  snapshot test; idempotence pinned incl. the derived-decision
  wall-clock fix the worker found and killed in-slice; gaps named,
  zero-progress valid, redaction pinned to run_manifest's denylist.
  R-0199 diagnosis accepted: both call sites and the root-resolution
  path verified in source by the reviewer; the size/time numbers
  accepted from the worker's raw transcript — a reviewer re-scan was
  deliberately skipped (the scan is itself the R-0199 cost) and the
  operator declined it at relay, consistent with that discipline.
  The COMMIT-1 split deviation is accepted (contents and order
  unchanged, < 500-line rule honoured — same class as the R-0198
  ruling). Verification tier: round gate + canary + docs gate.
  LAST_REVIEWED_SHA = 79621fc0.
<<<END AUTHORED f079-r2-1>>>

<<<BEGIN AUTHORED f079-r2-2
sha256=d4c7bcd3d28c2278bd27cc8c9a65999f85eeffc407fbb586ed6d38fa5b4a8f4c>>>
# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Session and context-window boundaries stop losing knowledge:
build_handoff composes dossier + checkpoint reference + open decisions
+ next intent into handoff.json + rendered handoff.md (idempotent,
pure artifact — done in T001); triggers + loop consumption with
reference verification (T002); measured recall eval on a fixture
mission (T003). Spec: docs/roadmap/features/T1_F079.md.

## Current Step
R2: R-0199 fix (data_root_digest becomes a metadata-manifest digest;
per-run frequency and evidence field names retained), T002 triggers +
loop consumption + reference verification, T003 boundary recall eval
+ threshold assertion + archived eval report.

## Next Steps
- R3: integration gate per docs/agents/integration_gate.md
- R4: closure per docs/roadmap/STATUS_closure_protocol.md (own round)

## Risks
- R-0203 constraint: consumption resolves ALL sources through one
  root discipline; document it at the consumption seam.
- Evidence-shape care in the R-0199 fix: digest definition changes,
  call frequency and field names do not; gauntlet evaluator/test
  consumers must be inspected before the edit.
- Do-not-touch unchanged: no automatic context-pressure detection, no
  cross-machine transport, no memory features beyond composition.
<<<END AUTHORED f079-r2-2>>>
