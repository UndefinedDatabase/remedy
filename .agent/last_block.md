You are the worker for F079 R5 (SPLIT round): CLOSURE PART 2 — the
closure commit and the PR, per docs/roadmap/STATUS_closure_protocol.md
algorithm steps 4–6. R4 verdict: PASS; the package is
READY_FOR_REVIEW. The PR is NOT merged — it merges at the next
feature's Open PR Gate. If any verification goes red: STOP per
AGENTS.md If-Blocked and hand back the raw output.

── STEP closure-2/2 — F079 ──────────────────────────────────
Goal:        Apply the authored STATUS [x] line + README sync +
             candidate re-emit + final .agent state in ONE closure
             commit, push, create the PR.
Bundle:      1 authored saves · 2 closure commit · 3 gates ·
             4 push + PR · 5 handback
Change:      docs/roadmap/STATUS.md (one line), README.md (two
             lines), .agent/** — NOTHING else (R-0154 exact paths).
Constraints: The closure commit is the LAST commit on the branch
             (Rule A4). STATUS and README move in the SAME commit.
             The evidence dir and the zips stay uncommitted
             (gitignored).
Done when:   Docs gate + canary green at the closure commit, grep
             proofs recorded, PR created.
Handback:    Completion report + rewrite .agent/handoff.md (inside
             the closure commit, see 5).
──────────────────────────────────────────────────────────────

1. AUTHORED SAVES
   Six authored texts follow at the bottom, delimited by BEGIN/END
   markers. Authored bytes = everything BETWEEN the marker lines,
   including the final newline; markers are never content.
   Save to .agent/authored/f079-r5-{1..6}.md; verify each with
   sha256sum against its BEGIN-marker hash. Mismatch → STOP, hand
   back naming block and both hashes; apply nothing.
   COMMIT A: the six authored files PLUS this entire prompt saved
   verbatim to .agent/last_block.md. (If that commit exceeds 500
   changed lines, split the last_block save into its own commit —
   R-0198 rule; both orderings are approved.)

2. CLOSURE COMMIT (one commit, exact paths)
   Apply, verbatim from the verified authored files:
   a. f079-r5-1: in docs/roadmap/STATUS.md replace the FROM line
      with the TO line (exactly one occurrence).
   b. f079-r5-2: in README.md apply EDIT 1 (FROM→TO) and EDIT 2
      (FROM→TO), each exactly one occurrence.
   c. f079-r5-3 → replaces .agent/candidates.md entirely.
   d. f079-r5-4 → replaces .agent/live_review.md entirely.
   e. f079-r5-5 → replaces .agent/plan.md entirely.
   f. f079-r5-6 → replaces .agent/context.md entirely.
   g. Rewrite .agent/handoff.md as the R5 handback (see 5 for
      required content — write it now, before committing).
   COMMIT B (the closure commit): exactly docs/roadmap/STATUS.md,
   README.md, .agent/candidates.md, .agent/live_review.md,
   .agent/plan.md, .agent/context.md, .agent/handoff.md. Message:
   "chore(f079): close F079 — STATUS [x] + README sync"

3. GATES (docs round — roadmap touched)
   python3 -m pytest tests/docs/ -q          → exit 0
   python3 -m pytest tests/cli/test_golden_path.py -q → exit 0
   git status --porcelain                    → empty
   GREP PROOFS (record raw output in the handback message):
   grep -F "accepted HEAD abc33f79aac937d3504dddef7a72bdb22d4aa2d1" docs/roadmap/STATUS.md
   grep -F "SHA-256 f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec"
docs/roadmap/STATUS.md
   grep -F "37 of 254 registered items accepted" README.md
   grep -c "^- " .agent/candidates.md        → 3
   Red or missing → STOP (the closure commit exists; do NOT amend —
   hand back and the reviewer orders the repair).

4. PUSH + PR
   git push. Then create the PR per the AGENTS.md PR workflow
   (gh pr create, base main, head feature/f079-context-handoffs).
   Title: "F079 — Context handoffs (T001–T003, closure)"
   Body (compose from the disk state, not from memory):
   - What/why: T1_F079.md Goal & Done + the Built State section.
   - Key decisions: two-relay closure (STATUS quotes the package);
     R-0199 metadata-manifest digest DECISION (alternatives named in
     live_review R2 finding); drift-wording extraction ruling;
     first-zip BLOCKED_EVIDENCE diagnosis (privacy validator
     correct, per-file scoped runs precedent).
   - How to review: read .agent/live_review.md verdicts R1–R4; the
     gate evidence in .agent/gate_f079_r3/; the package
     remedy-review-20260806-203747-READY_FOR_REVIEW.zip (SHA-256
     f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec).
   - Changed-files summary per round (from the four handbacks in
     .agent/handoff.md git history).
   - Latest verdict: R4 PASS; full suite green at the R3 gate.
   - Open findings: 2 deferred (R-0200 gate tooling, R-0202 UI
     rebuild class) + 1 flake id — all re-emitted in
     .agent/candidates.md for the next feature's first round.
   - Runtime actuals (observed): 5 reviewer-gated rounds on
     2026-08-06; full-suite wall ~141 s branch / ~132 s base;
     tokens/cost not-measured (zero-provider closure).
   Record the PR number and URL. DO NOT merge.

5. HANDBACK (.agent/handoff.md, inside the closure commit)
   - The four STATUS values verbatim (job id, package, SHA-256,
     accepted HEAD) and the PR number placeholder note ("PR created
     after this commit; number in the completion report").
   - Changed-files table for commits A and B.
   - The grep-proof commands listed in 3 (their raw outputs go in
     the completion REPORT, since the handoff commits first).
   - Item status per bundle item.
   The completion report (chat) carries: both gate tails, the grep
   outputs, the PR number + URL, and final `git log --oneline -3`.

AUTHORED TEXTS

<<<BEGIN AUTHORED f079-r5-1
sha256=6ae1a2d014f8ffad8c72e9cb121cf83906950d191895194f310c2f7daa8c36a7>>>
FROM:
- [~] F079 — Context handoffs
TO:
- [x] F079 — Context handoffs (T001–T003 complete; accepted 2026-08-06 · live review PASS
— ACCEPTED · Evidence job a7f0791c4d6b2e58 · package
remedy-review-20260806-203747-READY_FOR_REVIEW.zip · SHA-256
f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec · accepted HEAD
abc33f79aac937d3504dddef7a72bdb22d4aa2d1)
<<<END AUTHORED f079-r5-1>>>

<<<BEGIN AUTHORED f079-r5-2
sha256=33fa335d51fd8951b2f553e1e5f7299155e5357b4f30065df941abd74c4a88d9>>>
EDIT 1 FROM:
36 of 254 registered items accepted. Next: F079 (Context handoffs).
EDIT 1 TO:
37 of 254 registered items accepted. Next: F080 (Machine-readable roadmap mirror &
STATUS.md).
EDIT 2 FROM:
| 1 | Self-Build Bootstrap | 20 | 22 |
EDIT 2 TO:
| 1 | Self-Build Bootstrap | 21 | 22 |
<<<END AUTHORED f079-r5-2>>>

<<<BEGIN AUTHORED f079-r5-3
sha256=9e92118597c3faea2182a1d195d5c080a21e99df01ad25e06d17b6328503f293>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- R-0200 (registered in F079, deferred unbuilt): closure evidence
  cannot yet prove a specified verb was actually CALLED — the
  gate-tooling half of the F070 acceptance gap. The reviewer-practice
  half is landed (docs/agents/reviewer_conventions.md,
  specified-route-exercised rule). Any build order should cite that
  rule. Source: F075 R4 diagnosis → F079 R1 registration → deferred
  through F079 closure · 2026-08-06.
- R-0202 (registered in F079, deferred unbuilt): the mid-run UI
  rebuild class — REMEDY_UI_NO_AUTO_BUILD=1 was once ignored by a
  spawned server/build path (R-0169, F069 R2; recurred F075 R12).
  Did NOT recur in the F079 R3 gate (dist hashes identical on both
  sides), but one clean gate is not the env-var hunt; the mechanism
  is still unexplained. integration_gate.md carries the operational
  mitigation. Source: F075 R12 gate → F079 R1 registration ·
  2026-08-06.
- xdist flake, single id: tests/orchestration/
  test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogical
  Identity::test_different_execution_identities_same_logical_hash
  failed once in the reviewer's parallel full-suite run at F079 R3,
  passed serially (file: 11/11) and the file is untouched by F079
  (0 commits in range). F135 flaky-detector territory; 1 id, far
  under the 10-id flake-debt threshold. Source: F079 R3 gate,
  reviewer run · 2026-08-06.
<<<END AUTHORED f079-r5-3>>>

<<<BEGIN AUTHORED f079-r5-4
sha256=c32b1668387d74f8d6d4e86c55a6d3e5b013061c0f5cbc02e26cc059c9293571>>>
# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. T001–T003 built,
verified, gated; evidence job + fresh zip produced in R4; R5 is the
closure commit + PR. FEATURE COMPLETE at R5.

## Steps
- R1 (SPLIT, LARGE): claim + candidate sweep + R-0199 diagnosis +
  reuse inspection + T001 — PASS.
- R2 (SPLIT, LARGE): R-0199 fix + T002 + T003 — PASS.
- R3 (SPLIT): INTEGRATION GATE — PASS, FULL SUITE GREEN.
- R4 (SPLIT): closure part 1 — Built State, preconditions, evidence
  job a7f0791c4d6b2e58, fresh zip READY_FOR_REVIEW — PASS, see
  Verdicts.
- R5 (SPLIT, current): closure part 2 — authored STATUS [x] + README
  sync + candidate re-emit + closure commit + PR. The PR merges at
  the next feature's Open PR Gate.

## Findings
- R-0199 (harness perf, Medium — carried from F075): FIXED in R2.
  Done: R-0199
- R-0200 (process/gate-tooling, Medium): deferred unbuilt — re-emitted
  to .agent/candidates.md in the closure commit.
- R-0201 (roadmap routing): resolved by routing in R1 (T3_F106.md).
  Resolved.
- R-0202 (gate tooling, Low): deferred unbuilt — re-emitted to
  .agent/candidates.md in the closure commit.
- R-0203 (design, Low): FIXED in R2. Done: R-0203
- Next free ID: R-0204.

## Verdicts
- R1: PASS (2026-08-06). Range 38854f60..79621fc0. Full text in this
  file's git history (commit b3a0291e).
- R2: PASS (2026-08-06). Range 79621fc0..0938884f. Full text in this
  file's git history (commit 561e401b).
- R3: PASS — INTEGRATION GATE PASS, FULL SUITE GREEN (2026-08-06).
  Range 0938884f..a11d1f74. Full text in this file's git history
  (commit cc03063c).
- R4: PASS (SPLIT, 2026-08-06). Range a11d1f74..20e2a06a (5 commits,
  all tabled). Transport: f079-r4-1/2/3 cmp 0 against the reviewer's
  scratchpad originals; live_review and plan byte-equal their
  authored texts; the Built State append verified in place. Reviewer
  verification, independent: the zip's sha256 recomputed on disk
  equals the printed hash; zipfile.testzip() None over all 2031
  members; .review_zip_manifest.json read directly — base
  38854f6034f1abff6f2c1e85e4d21752d33d66b6, head
  abc33f79aac937d3504dddef7a72bdb22d4aa2d1 (exactly the required
  span), package_status READY_FOR_REVIEW, validation
  is_valid_current_run true with zero errors, final_verifier and
  token_truth both VERIFIED_EQUAL; `remedy integrity check --json`
  re-run by the reviewer: passed=true, 0 failed, 5 checks. Docs gate
  293 and canary 42 accepted from raw transcripts at the content
  HEAD. The FIRST zip attempt (BLOCKED_EVIDENCE) was recorded with
  its diagnosed cause — the packaging privacy validator correctly
  rejecting 605 parametrized full-suite node ids that literally
  contain secret-like strings and absolute paths; the full-suite
  numbers stay in the committed .agent/gate_f079_r3/ evidence —
  deviation ACCEPTED: correct validator behaviour, honest recording,
  per-file scoped verification_runs match the closure precedent.
  PASS_WITH_RISKS is the operator-attested manual-completion profile
  (commit_execution_gate NEEDS_HUMAN_APPROVAL by design; every other
  gate PASS; missing_evidence empty). Closure preconditions 1–5 all
  hold. LAST_REVIEWED_SHA = 20e2a06a.
<<<END AUTHORED f079-r5-4>>>

<<<BEGIN AUTHORED f079-r5-5
sha256=c6a703cc16533ab87432ef47812feec491b5f9fa14a029ce6e251806c9549a79>>>
# Plan — F079 Context handoffs (closed)

Branch: feature/f079-context-handoffs — closure PR open, merges at
the next feature's Open PR Gate.

## Goal
F079 is complete and accepted: handoff composer (idempotent, pure
artifact), explicit CLI + loop boundary triggers, consumption with
reference verification and one shared drift wording, measured
boundary recall (100 % open items, report archived), R-0199
metadata-manifest digest fix (34.6 s vs 394.8 s). Evidence job
a7f0791c4d6b2e58; package
remedy-review-20260806-203747-READY_FOR_REVIEW.zip; accepted HEAD
abc33f79aac937d3504dddef7a72bdb22d4aa2d1.

## Next Steps
- Next session: F080 (Machine-readable roadmap mirror & STATUS.md)
  per Rule A5, fresh window. Its first paste block runs the Open PR
  Gate (merges the F079 closure PR).
- .agent/candidates.md carries three entries (R-0200, R-0202, one
  xdist-flake id) — block condition at the F080 claim until its
  first reviewed round registers or resolves each.

## Risks
- ADR-0001 (CYCLE_SAFETY_CAP) still awaits a human; the pinned
  assertions hold it at 1.
- Round gates stay scoped pytest commands (resource-safety rules of
  tests/regression apply to full runs).
<<<END AUTHORED f079-r5-5>>>

<<<BEGIN AUTHORED f079-r5-6
sha256=c7efa5aa380b3dfeaf46cd99711d05aad79c4807ab75fbb53b522fa48645dbad>>>
# Context — F079 closed; next feature not yet claimed

## Active Branch
feature/f079-context-handoffs — F079 closure PR open, NOT merged. The
next feature (F080, Machine-readable roadmap mirror & STATUS.md)
starts from main AFTER the Open PR Gate merges this PR.

## Scope
F079 is complete and accepted: handoff composer (idempotent, pure
artifact), `remedy mission handoff` + loop boundary triggers,
consumption with checkpoint-reference verification and the shared
worktree-drift wording, measured boundary recall (100 % of open
items), and the R-0199 metadata-manifest digest fix. Built State is
recorded in docs/roadmap/features/T1_F079.md; STATUS.md carries the
[x] line with the evidence job, package and accepted HEAD.

## Constraints
- Nothing further ships on this branch. The closure commit is the
  last commit (Rule A4); do not append to it.
- .agent/candidates.md is non-empty by design and blocks the next
  feature claim until its first reviewed round registers or resolves
  each entry.
- Round gates stay scoped pytest commands; the full-suite
  pytest -n auto run belongs to the integration gate, where the
  resource-safety rules of tests/regression apply.
- ADR-0001 stays PROPOSED; CYCLE_SAFETY_CAP stays 1 until a human
  applies it.

## Steps
R1–R2 build (PASS) → R3 integration gate PASS (full suite green) →
R4 evidence job + fresh zip → R5 closure commit + PR (this commit) →
next: F080 in a fresh session.
<<<END AUTHORED f079-r5-6>>>
