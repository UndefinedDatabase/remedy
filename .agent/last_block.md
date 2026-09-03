── STEP R20/1 — F110 (repair round) ────────────────────────
Goal: Fix the two doc-consistency test failures that turned PR #233's
CI red, caused by R19's STATUS/README bundle never re-deriving the two
counts its own additions moved.

Bundle:
1. Save this whole block verbatim.
2. Apply PLAN20 (full replacement) to .agent/plan.md.
3. Apply README_COUNT_PAIR and README_TIER3_PAIR to README.md, one commit.
4. Append RECORD20 to .agent/live_review.md.
5. Rewrite .agent/handoff.md (handback).

Change: .agent/authored/f110-r20.md (new), .agent/last_block.md (mirror),
.agent/plan.md (full replace), README.md (two in-place rewrites),
.agent/live_review.md (append), .agent/handoff.md (rewrite). No other
path.

Constraints:
- Do not touch any file under packages/, apps/, tests/, or
  docs/roadmap/features/.
- Both README pairs are REWRITES (TO does not contain FROM) — apply as
  literal string replacement, each FROM must occur exactly once in the
  base README.md before your edit.
- Commit order: C0a (save authored block verbatim to
  .agent/authored/f110-r20.md) → C0b (mirror committed authored file to
  .agent/last_block.md, byte-identical) → C1 (PLAN20 to .agent/plan.md)
  → C2 (both README pairs, one commit) → C3 (RECORD20 appended to
  .agent/live_review.md — append means: read the current file, then
  write two newline characters, then RECORD20's exact bytes, with
  nothing else changed; the file must end WITHOUT a trailing newline,
  matching its current convention) → C4 (handback: rewrite
  .agent/handoff.md, commit).
- Before C2, run: python3 -m pytest tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger -q
  and confirm it reproduces the same two AssertionErrors CI reported
  (68 vs 69; Tier 3 Done=3 vs 4). Report the exact output.
- After C2, re-run the same pytest command and confirm both tests PASS.
  Report the exact output.
- AGENTS.md self-review loop (git diff --stat, git diff) before every
  commit — no exceptions.
- git push -u origin feature/f110-model-routing-by-task-class after C4.
- Do not run `gh pr merge`. Do not create a worktree. Do not touch main.

Done when:
- Both pytest tests above pass after C2, real exit code 0, output
  quoted in the handback.
- git diff --stat over the full round's range, scoped to packages/,
  apps/, tests/, docs/roadmap/features/, is EMPTY.
- git status --porcelain is EMPTY after C4.
- .agent/plan.md is under 50 lines, exactly one `## Goal`, exactly one
  `## Next Steps`.
- .agent/live_review.md's new byte length equals its pre-C3 byte length
  plus 2 (two newlines) plus RECORD20's UTF-8 byte length (2129), and
  the file still ends without a trailing newline; report all three
  numbers.
- The branch is pushed.

Handback: completion report (AGENTS.md handback fields) + rewrite
.agent/handoff.md naming: SESSION 8 of feature F110, round 20 (repair),
branch, commit SHAs, changed-files table, the real pytest output before
and after C2, git diff --stat scope check result, live_review.md byte
arithmetic, next expected action = "the reviewer re-verifies and, if
green, re-checks PR #233's CI and merges at the Open PR Gate."
──────────────────────────────────────────────────────────────

PLAN20 (full replacement of .agent/plan.md):
<<<PLAN20_START>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, PR #233 open into `main`
since F110 R19 (session 7). F110 is CLOSED as a build feature; this round
is a REPAIR round against the still-open PR, triggered by CI going red.

## Goal

Fix the two doc-consistency failures CI reported on PR #233: R19's C3
(`86bc9444`) authored the new STATUS `[x] F110` line and README capability
paragraph but never re-derived the two counts those additions moved, so
`tests/docs/test_docs_consistency.py` failed
`test_the_readme_accepted_count_equals_the_status_count` (68 vs 69) and
`test_the_readme_tier_table_done_column_matches_the_ledger` (Tier 3
Done=3 vs ledger 4).

## Current Step

Round 20 (repair). Rewrite README.md's accepted-count line and Tier 3
Done cell to match the real STATUS.md ledger, register and resolve
finding R-0790 for the omission, push, and confirm CI goes green.

## Next Steps

Once CI is green on PR #233, the Open PR Gate merges it (AGENTS.md):
`gh pr merge 233 --merge --delete-branch`, then `git checkout main` and
`git pull --ff-only`. No further F110 rounds are planned after the
merge — the next session claims the next STATUS `[ ]` feature.

## Risks

- `R-0767` and `R-0784` stay OPEN; both predate F110, documented in the
  Built State section, not F110 defects.
<<<PLAN20_END>>>

README_COUNT_PAIR:
FROM: "68 of 266 registered items accepted."
TO:   "69 of 266 registered items accepted."

README_TIER3_PAIR:
FROM: "| 3 | Full Token Economy & Autonomy | 3 | 26 |"
TO:   "| 3 | Full Token Economy & Autonomy | 4 | 26 |"

RECORD20 (append to .agent/live_review.md, exactly as C3 above describes):
<<<RECORD20_START>>>
Gate: F110 R20 — the round 20 entry. VERDICT PASS, over this round's own commit sequence (base e6e413ad, F110 R19's closure handback). THE ROUND REPAIRED A CI-RED LEFT BY R19: R19's C3 (86bc9444) authored the STATUS `[x] F110` line and the README capability paragraph but never re-derived the two counts those additions moved, so PR #233's `ci` check failed tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count (README claimed 68 accepted; docs/roadmap/STATUS.md carries 69 `- [x] F\d{3} — ` lines) and test_the_readme_tier_table_done_column_matches_the_ledger (README's Tier 3 Done cell read 3; the ledger derives 4 from F106/F108/F109/F110 all resolving to tier 3 via their feature files). THE REVIEWER REPRODUCED BOTH FAILURES LOCALLY BEFORE AUTHORING THIS ROUND, MATCHING CI'S OWN TWO ASSERTIONERRORS EXACTLY, and confirmed both FROM strings this round replaces occurred exactly once each in the base README.md. THE FIX IS TWO REWRITE PAIRS IN README.md ONLY: `68 of 266 registered items accepted.` to `69 of 266 registered items accepted.`, and `| 3 | Full Token Economy & Autonomy | 3 | 26 |` to `| 3 | Full Token Economy & Autonomy | 4 | 26 |` — neither TO contains its FROM (the changed digit sits mid-string in both), so both are REWRITES, not appends. FINDING R-0790 IS REGISTERED AND RESOLVED IN THE SAME ROUND: the open set was searched first per §3 item 30 and held no existing entry for this defect class; root cause is that R19's STATUS_PAIR/README_PAIR bundle carried no done-when asserting the two derived counts, so nothing caught the omission before it reached CI. THE GATE WAS RE-RUN AFTER THIS ROUND'S OWN README-FIX COMMIT (the commit immediately preceding this ledger entry in the sequence) AND WENT GREEN: both named tests pass at exit 0, reproduced directly against the committed README.md. THE TREE AND THE SWEEP HELD: this round's change set is README.md plus its own `.agent/**` state files only — no path under packages/, apps/, tests/ or docs/roadmap/features/ was touched. Done: R-0790 — the same round that registered it.<<<RECORD20_END>>>
