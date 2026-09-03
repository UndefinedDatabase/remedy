── STEP F110 R19 — THE CLOSURE COMMIT (final round of this feature) ──
Round 19 · SESSION 7 of F110 · base `acd89a6f` (F110 R18 C4)

Goal:
  Book round 18's PASS verdict as the `Gate: F110 R18` ledger entry, then
  perform the closure commit per docs/roadmap/STATUS_closure_protocol.md:
  the authored STATUS `[x]` line and the README capability paragraph in
  ONE commit, `SU-006`'s `consumed_by` set to `F110`, then open the pull
  request. This is the LAST round of F110 — do not create a round 20.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r19.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN19 to `.agent/plan.md` (whole-file replacement)
  C2   append RECORD19 to `.agent/live_review.md`
  C3   apply STATUS_PAIR to `docs/roadmap/STATUS.md` AND README_PAIR to
       `README.md` — BOTH in this ONE commit (R-0154 precedent: STATUS
       line and README sync land together)
  C4   apply QUEUE_PAIR to `scripts/self_use_queue.json`
  C5   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r19.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `docs/roadmap/STATUS.md`
  `README.md`
  `scripts/self_use_queue.json`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/`, `docs/roadmap/features/`,
  `.agent/decisions.md`, `.agent/prose_slips.md` or `.agent/candidates.md`
  is touched by this round's own commits. This round mints NO finding id.

Constraints:
  1. `.agent/STOP` is read FROM DISK before the first commit and again
     before C5. If it exists at either reading: finish the commit in
     hand, write the handback, push, and stop — do NOT create the PR.
  2. Transport is PROMPT-EMBEDDED (the reviewer is 100% read-only and
     holds no scratch original). Copy the bytes between BEGIN BLOCK / END
     BLOCK (excluding sentinels) verbatim into `.agent/authored/f110-r19.md`.
  3. Extract every slice from the COMMITTED `.agent/authored/f110-r19.md`
     by its markers — never from this prompt directly, never retyped.
  4. `.agent/plan.md` at C1 is REPLACED IN FULL by PLAN19. Report `wc -l`
     (under 50) and sha256.
  5. `.agent/live_review.md` at C2: base at `acd89a6f` measured 2241475
     bytes ending WITHOUT a trailing newline. RECORD19 is 2974 bytes, one
     paragraph, zero internal newlines. The committed file must be
     EXACTLY 2241475 + 2 + 2974 = 2244451 bytes, base an exact PREFIX.
     Report the arithmetic and prefix confirmation directly.
  6. `docs/roadmap/STATUS.md` at C3: STATUS_PAIR is a REWRITE (not an
     append — the reviewer verified TO does NOT simply contain FROM as a
     substring, since new text is inserted mid-line). STATUS_PAIR_FROM
     occurs exactly ONCE in the base file (the `- [~] F110` line);
     replace it with STATUS_PAIR_TO. Report the FROM count in the base
     (must be 1) and confirm the applied line matches STATUS_PAIR_TO
     byte-for-byte.
  7. `README.md` at C3 (same commit as STATUS.md): README_PAIR is also a
     REWRITE for the same reason. README_PAIR_FROM occurs exactly ONCE in
     the base file; replace it with README_PAIR_TO, which inserts the new
     F110 capability paragraph between the F109 paragraph and "Accepted
     in Tier 5 so far:". Report the FROM count (must be 1).
  8. `scripts/self_use_queue.json` at C4: QUEUE_PAIR_FROM
     (`"consumed_by": "",`) occurs exactly ONCE in the entire file — this
     is SU-006's own field, since every other item's `consumed_by` is
     already non-empty. Report the FROM count (must be 1) and confirm the
     file is still valid JSON after the edit (`json.load` it).
  9. Do NOT run `ruff`, `npm`, or any formatter — no `.py` file under
     `packages/`/`apps/`/`tests/` is touched this round.
 10. After C5, push, THEN create the pull request with `gh pr create`
     (base `main`, head `feature/f110-model-routing-by-task-class`) using
     the title and body given below under PR_CONTENT. Do NOT merge it —
     report only the PR number and URL `gh pr create` returns. Do NOT run
     `gh pr merge` under any circumstance this round.

Done when — each gate run and reported as ONE LINE in the handback with
its real exit code, at a commit STRICTLY EARLIER than C5:

G1 TRANSPORT — sha256sum of `.agent/authored/f110-r19.md` and
   `.agent/last_block.md` — must match. Report `wc -l`.

G2 THE PLAN — `wc -l .agent/plan.md` under 50; sha256; `grep -c '^## Goal$'`
   and `grep -c '^## Next Steps$'` each 1.

G3 THE LEDGER APPEND — the arithmetic from constraint 5, reproduced
   directly; `grep -c '^Gate: F110 R18'` 0 before C2, 1 after; confirm no
   new `^- R-` or `^Done: R-` line (identical counts before/after).

G4 STATUS AND README — the values from constraints 6 and 7: FROM counts,
   applied-text confirmation for STATUS.md, FROM count for README.md.
   Report `git diff --stat` for C3 shows exactly these two paths.

G5 THE QUEUE — the value from constraint 8: FROM count, JSON validity
   after edit, and confirm `json.load(...)["items"]` still has the SAME
   number of items as before (no item added or removed, only one field
   changed on one item).

G6 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C5 — EMPTY.
   `git diff --stat acd89a6f..<C4-sha> -- packages/ apps/ tests/
   docs/roadmap/features/ .agent/decisions.md .agent/prose_slips.md
   .agent/candidates.md` — must be EMPTY.
   PER-COMMIT INSERTIONS, the `+` column only, for C0a, C0b, C1, C2, C3
   and C4, reported cell by cell against the handback's own `## Commits`
   table and each confirmed under 500 (C0b may be a whole-file rewrite).

G7 THE PR — report the PR number, URL, base and head branch as `gh pr
   create` actually printed, and confirm with `gh pr view <n> --json
   state,isDraft,baseRefName,headRefName` that it is OPEN, NOT a draft,
   base `main`, head `feature/f110-model-routing-by-task-class`. Confirm
   `gh pr merge` was NEVER invoked this round.

Handback: rewrite `.agent/handoff.md` in full per
   docs/agents/handback_template.md — feature and round, SESSION 7 of
   F110, branch, base and head SHAs, the per-commit changed-files table
   with its `+/-` column, ONE line per gate above with its real exit
   code, the item-status table AGENTS.md mandates, the deviations, the
   open-findings count (278, UNCHANGED — no new id minted this round),
   the PR number and URL. State explicitly that this is F110's LAST
   round and the PR is UNMERGED, awaiting the Open PR Gate. It has NO
   length cap. Then push again after C5 if anything changed (the PR
   itself does not require a further push).

<<<BEGIN PLAN19>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 19 — THE CLOSURE COMMIT (final round of this feature). Round 18's
Built State section is booked (`Gate: F110 R18`, PASS); closure
precondition 4 is satisfied. This round books the authored STATUS `[x]`
line and the README capability paragraph in ONE commit, sets `SU-006`'s
`consumed_by` to `F110` in `scripts/self_use_queue.json`, and opens the
pull request. The PR is NOT merged this session — it merges at the next
feature's Open PR Gate, the operator's manual-review window.

## Next Steps

None — this is the feature's last round. The next session's Phase 0
finds an open, non-draft PR from this branch into `main` and merges it
at the Open PR Gate before claiming a new feature.

## Risks

- `R-0767` and `R-0784` stay OPEN; both predate F110 and are documented,
  not F110 defects — see the Built State section's own citations.
<<<END PLAN19>>>

<<<BEGIN RECORD19>>>
Gate: F110 R18 — the round 18 entry. VERDICT PASS, over the range `2fe36572..acd89a6f`. THE ROUND BOOKED ROUND 17'S VERDICT AND GAVE THE FEATURE FILE ITS BUILT STATE SECTION, AND THE REVIEWER RE-DERIVED EVERY VALUE FROM DISK. TRANSPORT, digest-fallback per docs/agents/self_drive_protocol.md: `.agent/authored/f110-r18.md` and `.agent/last_block.md` are byte-identical, sha256 `52eb4f51244388d798b2f5fb4cee2c7afad3baf7610b9f402fa043b3d5c24eef` over 304 lines, reproduced by the reviewer directly against the committed blob. THE LEDGER APPEND HOLDS UNDER THE REVIEWER'S OWN ARITHMETIC: base at `2fe36572` measured 2238252 bytes ending without a trailing newline, RECORD18 measured 3221 bytes with zero internal newlines, and the committed file is exactly 2238252 + 2 + 3221 = 2241475 bytes, its first 2238252 bytes an exact PREFIX of the base, reproduced directly off disk. NO NEW `- R-` OR `Done:` LINE WAS ADDED this round either. THE FEATURE FILE HOLDS UNDER THE REVIEWER'S OWN CONTAINMENT AND BYTE CHECKS: both AS-BUILT correction pairs' FROM strings occurred exactly once in the base `docs/roadmap/features/T3_F110.md`, both TO strings were confirmed by the reviewer to literally CONTAIN their FROM as a prefix (a genuine APPEND at the paragraph level, correctly labelled), and the committed file ends with exactly one trailing newline at 10653 bytes, carrying exactly one `## Built State` heading, one `## Design` heading (unchanged) and two `AS BUILT` markers — all reproduced by the reviewer directly from the committed bytes, not from the handback's count. CLOSURE PRECONDITION 4 (the feature file's Built State section is current) IS THEREFORE SATISFIED. THE TREE AND THE SWEEP HELD: `git diff --stat 2fe36572..acd89a6f` over `packages/`, `apps/`, `tests/`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/candidates.md` and `scripts/self_use_queue.json` is EMPTY, reproduced directly; the branch is pushed at `acd89a6f` with no pull request open. ONE DEVIATION WAS DECLARED, CORRECTLY: the worker created seven transient scratch files under `.agent/` to perform byte-exact marker extraction from the committed authored block, deleted every one by exact path before staging C3, and the reviewer confirmed `git status --porcelain` was EMPTY immediately before C4 was staged and that none of the seven appears in any commit's changed-files list — the deviation cost nothing on disk and was declared rather than hidden. THE REVIEWER ALSO RE-CONFIRMED THIS ROUND, INDEPENDENTLY OF EITHER HANDBACK, THAT F110's OWN THREE SELF-RAISED FINDINGS ARE ALL RESOLVED — `Done: R-0787` (F110 R12, `cc32f16b`), `Done: R-0788` (F110 R12, `fdfc7e2c`), `Done: R-0789` (F110 R14, `d8a66340`) — and that the two open items this branch's own plan.md names as risks, `R-0767` and `R-0784`, both predate F110 (inherited from earlier features, documented, not F110 defects), which is the precondition-1 reading closure round 19 relies on. NO FINDING IS OWED BY THIS ROUND.
<<<END RECORD19>>>

<<<BEGIN STATUS_PAIR_FROM>>>
- [~] F110 — Model routing by task class
<<<END STATUS_PAIR_FROM>>>

<<<BEGIN STATUS_PAIR_TO>>>
- [x] F110 — Model routing by task class (T001–T003 complete; accepted 2026-09-03 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f110-closure · package remedy-review-20260903-181544-READY_FOR_REVIEW.zip · SHA-256 767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 953cade0f62b2687d7dafb5cf1e0b9631849b532)
<<<END STATUS_PAIR_TO>>>

<<<BEGIN README_PAIR_FROM>>>
mechanism is exercised by the suite and inert on real runs today).

Accepted in Tier 5 so far:
<<<END README_PAIR_FROM>>>

<<<BEGIN README_PAIR_TO>>>
mechanism is exercised by the suite and inert on real runs today).

F110 model routing by task class (every role Remedy resolves a runtime
configuration for now carries a declared task class; a single resolver
seam routes builder/reviewer/orchestrator/teacher/summary/test-worker/
design-worker calls to a cost tier — cheap, mid or top — with the
reason recorded alongside the routed call; the three policy hard rules
(reviewer never weaker than its paired worker, orchestrator/mission
calls always top tier, safety-relevant classes never below mid) are
enforced in code and refuse a violating override by name rather than
silently applying it; moving a class to a cheaper tier requires a
documented benchmark run, never a bare config edit).

Accepted in Tier 5 so far:
<<<END README_PAIR_TO>>>

<<<BEGIN QUEUE_PAIR_FROM>>>
"consumed_by": "",
<<<END QUEUE_PAIR_FROM>>>

<<<BEGIN QUEUE_PAIR_TO>>>
"consumed_by": "F110",
<<<END QUEUE_PAIR_TO>>>

<<<BEGIN PR_CONTENT>>>
TITLE: F110 — Model routing by task class

BODY:
## Summary
- Every role Remedy resolves a runtime configuration for now carries a declared task class (`packages/orchestration/model_routing.py`'s `TASK_CLASS_TIERS`, seeded from and synced against `docs/agents/model_routing_policy.md`).
- One shared resolver seam (`role_config.resolve_role_config`, via `RoleConfig.routed_call`) routes every one of the seven inventoried call sites to a cost tier (cheap/mid/top) with the reason recorded alongside the routed call.
- The three policy hard rules (reviewer never weaker than paired worker; orchestrator/mission calls always top tier; safety-relevant classes never below mid) are enforced in code as named checks and refuse a violating `remedy.toml` override by naming every rule it breaks (DECISION F110 D5), rather than raising and turning one typo into an outage.
- Moving a task class to a cheaper tier requires a documented benchmark run (`promotion_evidence_from_mapping`, `role_config.resolve_promotion_evidence`) — never a bare config edit.

## Test plan
- [x] `tests/orchestration/test_model_routing.py`, `test_role_config.py`, `test_orchestrator_model_routing.py`, `test_config.py`, `test_job_role_routing.py`, `test_job_task_runner.py` — 838 passed, 3 skipped (reviewer-verified independently, not just worker-reported)
- [x] Tier-3 integration gate (round 15) — PASS, both base-only failures attributed to the pre-existing XDIST-FLAKE class
- [x] `remedy integrity check` — PASS, 0 failures (reviewer re-ran independently)
- [x] Review zip — `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS` (package `remedy-review-20260903-181544-READY_FOR_REVIEW.zip`, SHA-256 `767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b`)
- [x] F257 self-use precondition — `SU-006` run for real against a local `ollama` provider through the shipped generator/runner, reached a normal approval-gate `blocked` outcome (not promoted); its defects added as evidence to the already-open `R-0784` rather than a new id

Built via docs/agents/self_drive_protocol.md (one-session planner/reviewer, no paste relay). NOT merged by this session — awaiting the Open PR Gate.
<<<END PR_CONTENT>>>
──────────────────────────────────────────────────────────────