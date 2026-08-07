Target: .agent/live_review.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: REWRITE — FROM and TO are disjoint, so the proof is FROM 0x and
TO 1x after the edit.
Apply this AFTER all four pairs of selfdrive-r5-1.md are on disk.

FROM
<<<FROM
- R3: PENDING — awaiting the worker handback.
FROM>>>

TO
<<<TO
- R3: PASS (2026-08-07). Range 151733e1..96bee72c, three commits, all
  tabled. Transport, PRIMARY proof: all eight receipts cmp 0 against
  the reviewer's scratchpad originals — no digest fallback; r3-6 and
  r3-7 cmp 0 against .agent/plan.md and .agent/context.md. The
  four-step live_review application was verified by RECONSTRUCTION,
  not by counting: applying r3-5's three pairs in order to the r3-1
  original reproduces the on-disk file byte for byte, each FROM
  unique at its turn. The AGENTS.md and docs/README.md hunks are
  +1/-1 each and exactly the authored TO; the markdown hard break on
  AGENTS.md:588 survived, which is what the substring-scoped pair was
  designed to protect. The new pin sits inside
  TestPrimaryDocsAreHonest between the 150 pin and the ledger test.
  Ordering: findings landed in b59bde9f, every fix and both Done
  lines in 11659b95 — no Done line was ever true ahead of its fix,
  and the count change and its pin share one commit (R-0151). PR #185
  open, isDraft false, mergedAt null; its body is byte-identical to
  receipt r3-8 but for one trailing newline GitHub adds. Reviewer
  re-runs: tests/docs/ 294 (293 before the pin, +1 — it landed) ·
  dashboard contract 70 · test_test_runner 51 · resource safety 21 ·
  test_agent_tooling 10 passed 1 skipped · golden path 42 — every
  count equal to the worker's report, all exit 0. Mutation red-proof
  in a disposable worktree, removed and pruned before this verdict,
  primary checkout clean: reverting both counts to 250 turns
  test_no_doc_understates_the_feature_count red and nothing else.
  Zero deviations reported, none found. Tier: round gate + canary; no
  full-suite claim is made anywhere in this feature.
  LAST_REVIEWED_SHA = 96bee72c.
- R4 first attempt: PASS ON THE EXECUTED WORK, round blocked
  (2026-08-07). Range 96bee72c..bca5492e. The reviewer's live-review
  receipt arrived truncated and the worker STOPPED at PART A: it
  reported the expected and the arrived digest, wrote no substitute
  text, committed no live_review/plan/context change, and refused to
  publish the prepared PR body because that body would have claimed a
  verdict the repo did not record. Reviewer verification:
  .agent/authored/selfdrive-r4-1.md does not exist in the repo; r4-2,
  r4-3 and r4-4 are cmp 0 against the reviewer's originals;
  live_review, plan and context are untouched at their R3 content;
  PR #185 unchanged. Gates re-run at that HEAD: dashboard contract 70
  · test_test_runner 51 · resource safety 21 · tests/docs/ 294 ·
  golden path 42, all exit 0. One finding raised, R-0210. Cause and
  remedy: a 126-line single-file receipt is a fragile payload, so the
  replacement was authored as small edits against the file already on
  disk, split across two independently verified receipts — §4 item 12,
  re-emit corrected bytes, never the same bytes.
- R4: the build is COMPLETE once this round's edits are committed. The
  next work is the S4 rehearsal in a fresh session.
TO>>>
