You are the worker for F079 R1 (SPLIT round, LARGE). Reviewer gates the
handback; you never write verdicts and never merge feature work.
Authority: AGENTS.md. Spec: docs/roadmap/features/T1_F079.md (read it
fully). If any verification below goes red: STOP at that point per
AGENTS.md If-Blocked, commit what is green, hand back with the raw
failure — do not continue into the next slice.

── STEP claim+T001/3 — F079 ─────────────────────────────────
Goal:        Merge PR #180, claim F079, register/resolve the four
             closure candidates, measure R-0199, inspect reuse
             surfaces, build T001 (handoff schema + composer +
             idempotence + unit tests).
Bundle:      0 preflight · 1 Open PR Gate · 2 branch · 3 state commits
             (authored texts) · 4 docs gates · 5 R-0199 measured
             diagnosis · 6 reuse inspection · 7 T001 · 8 handback
Change:      .agent/** state files, docs/roadmap/STATUS.md (one line),
             docs/roadmap/features/T3_F106.md (append), NEW
             packages/orchestration/handoff.py, NEW
             tests/orchestration/test_handoff.py. Nothing else.
Constraints: Do-not-touch per T1_F079.md (no automatic context-pressure
             detection, no cross-machine transport, no memory features
             beyond composition). Reuse is mandated: dossier renderer,
             checkpoint verification, recall harness — a new
             implementation of an existing piece is a reject. Commits
             < 500 lines each. Primary checkout porcelain-empty at
             handback.
Done when:   All verifications below exit 0, in order.
Handback:    Completion report + rewrite .agent/handoff.md (see 8).
──────────────────────────────────────────────────────────────

0. PREFLIGHT
   git status --porcelain   → must be empty (you are on
   feature/amend0805-v3). If not empty: STOP, hand back.

1. OPEN PR GATE
   Merge PR #180 per the AGENTS.md Open PR Gate procedure. Then:
   git checkout main && git pull

2. BRANCH
   git checkout -b feature/f079-context-handoffs

3. STATE COMMITS
   Five authored texts follow at the bottom of this prompt, each
   delimited by BEGIN/END marker lines. The authored bytes are
   everything BETWEEN the marker lines, including the final newline;
   the marker lines themselves are never part of the content.
   For each text f079-r1-N:
   a. Save the bytes to .agent/authored/f079-r1-N.md
   b. Verify: sha256sum .agent/authored/f079-r1-N.md must equal the
      sha256 in its BEGIN marker. On ANY mismatch: STOP, hand back
      naming the block and both hashes — apply nothing.
   COMMIT 1 (own commit, before any application): the six files
   .agent/authored/f079-r1-{1,2,3,4,5,6}.md plus this entire prompt
   saved verbatim to .agent/last_block.md.
   Then apply, verbatim from the verified authored files:
   c. f079-r1-1: in docs/roadmap/STATUS.md replace the FROM line with
      the TO line (exactly one occurrence; the file's only F079 line).
   d. f079-r1-2 → replaces .agent/live_review.md entirely.
   e. f079-r1-3 → replaces .agent/candidates.md entirely.
   f. f079-r1-4 → APPEND to docs/roadmap/features/T3_F106.md (file
      currently ends after the "Do not touch" section; the authored
      text begins with a blank line — append as-is to the end).
   g. f079-r1-5 → replaces .agent/plan.md entirely.
   h. f079-r1-6 → replaces .agent/context.md entirely.
   COMMIT 2: exactly these six applied files, message
   "chore(f079): claim F079 + candidate sweep (R-0200..R-0202, R-0199
   diagnosis ordered)".

4. DOCS-ROUND GATES (change set touches docs/roadmap/**)
   python3 -m pytest tests/docs/ -q          → exit 0
   python3 -m pytest tests/cli/test_golden_path.py -q   → exit 0
   Record command, exit code and tail for both. Red → STOP.

5. R-0199 MEASURED DIAGNOSIS (read-only; no code change, no fix)
   Hypothesis to test: gauntlet_runner.data_root_digest
   (packages/orchestration/gauntlet_runner.py:91) full-scans the
   operator's real data root on every call, ~20+ calls per campaign.
   a. Read the call sites: count how many data_root_digest calls one
      campaign of 10 runs performs; note file:line of each site.
   b. Resolve the EXACT root the gauntlet passes (read the resolution
      code path; do not guess).
   c. Measure that root: file count and total bytes (e.g.
      `find <root> -type f | wc -l` and `du -sb <root>`).
   d. Time ONE data_root_digest(<root>) call with time.perf_counter
      via a throwaway script OUTSIDE the repo (scratch/tmp, deleted
      afterwards). HARD CAP: if the call has not returned after 15
      minutes, kill it and record "aborted at 15 min" — the timeout
      is itself the measurement.
   e. Record ALL raw numbers (counts, bytes, seconds, call-site
      table) in the handback under "R-0199 diagnosis". Compute
      bytes-scanned-per-campaign = total bytes x call count and state
      whether it is consistent with the observed ~872 GB. NO fix in
      this round — the reviewer orders the fix in R2 from your
      numbers.

6. REUSE INSPECTION (read-only)
   Produce a table in the handback naming, with file:line, the exact
   pieces T001–T003 must reuse:
   - the dossier renderer entry point(s) in
     packages/orchestration/mission_dossier.py and where dossier
     evidence is written (the evidence-area path scheme),
   - the checkpoint reference + verification API in
     packages/orchestration/checkpoints.py (what T002 will call),
   - the recall harness used by the dossier tests (locate it under
     tests/, name the fixture mission it uses),
   - where open decisions live (decision_queue.py surface) and where
     "next intent" can be read from mission state.
   No code changes in this slice.

7. T001 — schema + composer + idempotence + unit tests
   New module packages/orchestration/handoff.py:
   - HANDOFF_SCHEMA_VERSION = 1; build_handoff(mission_id) -> Path.
   - Compose handoff.json: schema_version, mission_id, dossier text
     (via the EXISTING renderer from slice 6), checkpoint reference +
     worktree head, open decisions with ids, next intent, provenance
     timestamps, and an explicit `gaps` list — any missing source
     renders as a named gap entry, never invented content.
   - Also render handoff.md: fixed section order, dossier first.
   - Both files land in the mission's evidence area, same path scheme
     the dossier uses.
   - IDEMPOTENT PER STATE: same mission state → byte-identical output
     (content-hash test). Therefore NO wall-clock reads in content:
     provenance timestamps are those of the SOURCE artifacts. Repeat
     builds on unchanged state must not create duplicates; changed
     state accumulates a new handoff deterministically (newest
     resolvable by the accumulation scheme — consumption itself is
     T002, not now).
   - PURE ARTIFACT: building mutates no mission/job/queue state —
     test asserts a state snapshot before == after.
   - Secrets: apply the existing manifest redaction denylist to any
     config values included.
   - Zero-progress mission is a valid handoff (goal + empty sections
     as explicit gaps).
   Tests in tests/orchestration/test_handoff.py covering: idempotence
   hash equality; missing-source → named gap; zero-progress validity;
   no-mutation snapshot; redaction applied; schema_version present.
   In the handback, name every reused piece per slice 6.
   Commit in small commits (< 500 lines each).
   VERIFY: python3 -m pytest tests/orchestration/test_handoff.py -q
   → exit 0. Red → STOP per If-Blocked.

8. HANDBACK
   Re-run the canary: python3 -m pytest tests/cli/test_golden_path.py
   -q → exit 0. Confirm git status --porcelain empty after the final
   commit. Push the branch (no PR — closure creates the PR later).
   Rewrite .agent/handoff.md (commit it as the last commit) with:
   - changed-files table per commit (path, +/-, reason),
   - raw transcripts: every verification command, exit code, output
     tail,
   - "R-0199 diagnosis" section with the slice-5 numbers,
   - the slice-6 reuse table,
   - reused-pieces list for T001,
   - item status per slice (done / stopped-at with the red output).
   No verdict, no merge, no STATUS edits beyond the authored claim.

AUTHORED TEXTS

<<<BEGIN AUTHORED f079-r1-1
sha256=29cbd4ef7c1a7bf2e7d043c6d0bf63dd95eb47a84ed25e68d89a69a70240c59b>>>
FROM:
- [ ] F079 — Context handoffs
TO:
- [~] F079 — Context handoffs
<<<END AUTHORED f079-r1-1>>>

<<<BEGIN AUTHORED f079-r1-2
sha256=0015ab62fc7342b8d0d35a78c258d133e08df3efaabaf431931e33416d313617>>>
# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. The F075 candidate
sweep (4 entries) is registered/resolved in R1 per
docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate findings").

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#180) + STATUS claim + candidate
  sweep + R-0199 measured diagnosis + reuse inspection + T001 (schema
  + composer + idempotence + unit tests). Awaiting handback.
- R2 (planned): T002 triggers + loop consumption + reference
  verification; R-0199 fix order once the diagnosis numbers are in.
- R3 (planned): T003 boundary recall eval + threshold. Then the
  integration gate round, then closure (its own round, never bundled).

## Findings
- R-0199 (harness perf, Medium — carried from F075, ID spent there):
  the attempt-03 campaign read ~872 GB while writing ~2 MB.
  Hypothesis, unverified: gauntlet_runner.data_root_digest full-scans
  the operator's real data root before and after every run. Operator
  priority HIGH. R1 orders the MEASURED diagnosis (raw numbers in the
  handback); the fix order follows in R2 on those numbers.
- R-0200 (process/gate-tooling, Medium) 2026-08-06, registered from
  candidates: F070 was accepted with a specified execution step
  unbuilt — its zero-provider closure evidence never proved the
  specified verb was CALLED. The reviewer-practice half is landed
  (docs/agents/reviewer_conventions.md, specified-route-exercised
  rule, amend0805-v3). The gate-tooling half (closure evidence proves
  a specified verb actually ran) stays OPEN here. DECISION: deferred —
  no build inside F079 scope (alternatives considered: build it now —
  rejected as scope creep; drop it — rejected, the F070 gap was real).
  Reversal: any later relay may order the build; if unbuilt at F079
  closure it rolls to candidates per protocol.
- R-0201 (roadmap routing) 2026-08-06, resolved from candidates: the
  move schema has no resume kind — a paused job's only forward path is
  re-dispatch, and a job that ended max_cycles_reached cannot be
  continued (F075 R5/R6 evidence). DECISION: routed to F106 — a scope
  note is appended to docs/roadmap/features/T3_F106.md in this round
  (alternative considered: F045 — rejected, loops are declarative
  config, not continuation of interrupted state). Reversal: move or
  reword the note in any later round. Resolved by routing.
- R-0202 (gate tooling, Low) 2026-08-06, registered from candidates:
  the mid-run UI rebuild recurred in the F075 R12 base gate despite
  REMEDY_UI_NO_AUTO_BUILD=1 (same class as R-0169, F069 R2); suspect a
  spawned server/build path not honoring the env var.
  docs/agents/integration_gate.md already carries the operational
  mitigation (dist hash check + per-id attribution). DECISION:
  deferred, OPEN — the env-var hunt is its own ordered round when
  prioritized; rolls to candidates at closure if unbuilt.
- Next free ID: R-0203.

## Verdicts
- (none yet — R1 handback awaited)
<<<END AUTHORED f079-r1-2>>>

<<<BEGIN AUTHORED f079-r1-3
sha256=9ddaa844de7b6a29f19c08b2001dcd85c703045798a79f61117e9a41b486ce35>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(empty — the four F075 candidates were registered/resolved in F079 R1
on 2026-08-06: R-0200 registered (F070 gate-tooling half, deferred) ·
R-0201 resolved by routing to T3_F106.md · R-0199 measured diagnosis
ordered in R1 · R-0202 registered (UI-rebuild env-var class,
deferred). Ledger of record: .agent/live_review.md.)
<<<END AUTHORED f079-r1-3>>>

<<<BEGIN AUTHORED f079-r1-4
sha256=54fee0eff5e98f3f333b8e42a1b8d4343ec824d029a741b0e9966325fb8dc640>>>

## Scope note (F075 candidate routing, 2026-08-06)
The orchestrator move schema has no `resume` kind: a paused job's only
forward path is re-dispatch, and a job that ended `max_cycles_reached`
cannot be continued (F075 R5/R6 evidence, routed from
.agent/candidates.md by F079 R1 as R-0201). When F106 is claimed,
treat "resume a job/mission from its persisted state" as in-scope
territory alongside provider-session resume — the two halves of the
same promise that an interruption is not a restart.
<<<END AUTHORED f079-r1-4>>>

<<<BEGIN AUTHORED f079-r1-5
sha256=51c15db676f1c3aaeb4ea71c3f088aaed4469ef6f0a3e09e564d59926a3338b5>>>
# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs (from main after PR #180 merged
at the Open PR Gate)

## Goal
Session and context-window boundaries stop losing knowledge:
build_handoff composes dossier + checkpoint reference + open decisions
+ next intent into handoff.json + rendered handoff.md (idempotent,
pure artifact — producing it changes no state); triggers + loop
consumption with reference verification; measured recall eval on a
fixture mission. Spec: docs/roadmap/features/T1_F079.md.

## Current Step
R1: candidate sweep persisted in live_review; R-0199 measured
diagnosis (raw numbers to handoff); reuse inspection
(mission_dossier renderer, checkpoints verification, recall harness);
T001 schema + composer + idempotence + unit tests.

## Next Steps
- T002: triggers (explicit CLI + loop-terminates-for-limits/stop) +
  loop consumption + stale-reference refusal + tests
- T003: boundary recall eval on a fake-provider mission + threshold
- R-0199 fix order once the diagnosis numbers are in
- Integration gate round, then closure (its own round)

## Risks
- Reuse is mandated: dossier renderer, checkpoint verification, recall
  harness — new implementations of existing pieces are rejects.
- Do not touch: automatic context-pressure detection, cross-machine
  transport, memory features beyond composition.
- Idempotence vs timestamps: provenance timestamps come from SOURCE
  artifacts, never wall clock — same state must hash identical.
<<<END AUTHORED f079-r1-5>>>

<<<BEGIN AUTHORED f079-r1-6
sha256=51862540c4c6d7359cc5c3468ab2dd68557f8af564b0dfb2bb3905cd4514fce8>>>
# Context — F079 Context handoffs (in progress)

## Active Branch
feature/f079-context-handoffs — claimed from main after the Open PR
Gate merged PR #180 (amend0805-v3).

## Scope
F079 (Context handoffs, Tier 1): handoff artifact composition
(dossier, checkpoint reference, open decisions, next intent) with
explicit + loop triggers, loop consumption with reference
verification, and a measured recall eval on a fixture mission. R1 also
carries the F075 candidate sweep and the R-0199 measured diagnosis.

## Constraints
- Round gates stay scoped pytest commands; the full-suite
  pytest -n auto run belongs to the integration gate, where the
  resource-safety rules of tests/regression apply.
- Building a handoff mutates nothing; missing sources render as
  explicit gaps, never invented content.

## Steps
R1: Open PR Gate + claim + candidate sweep + R-0199 diagnosis + reuse
inspection + T001. Then T002, T003, integration gate, closure.
<<<END AUTHORED f079-r1-6>>>
