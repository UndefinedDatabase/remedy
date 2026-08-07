# Live Review — S1+S2 Self-drive skill (infrastructure track, not a roadmap feature)

Branch: feature/selfdrive-skill
Scope: the one-session build discipline the operator needs from
2026-08-13 (SSH from a phone; starting Claude Code and invoking ONE
skill is the only touchpoint). Deliverables: the protocol doc
docs/agents/self_drive_protocol.md, the skill
.claude/skills/remedy-self-drive/SKILL.md, the command
.claude/commands/build-remedy-self.md, docs-index registration and the
pins in tests/test_agent_tooling.py. Source of the requirement:
.agent/selfdrive_package.md (S1+S2), operator-relayed 2026-08-06.
No STATUS.md line is claimed — STATUS is the roadmap ledger and this
work is not a roadmap feature (DECISION D7).

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#184) + candidate sweep +
  closure-protocol pitfall (d) + protocol doc + skill + command + docs
  index + test pins — PASS.
- R2 (SPLIT, LARGE): persist R-0207, fix it in §4 item 9, dry-run the
  protocol's own Phase 0 probe — PASS.
- R3 (SPLIT, current): persist R-0208 and R-0209, fix both, then the
  PR. No STATUS line, no evidence job, no zip (D7); the PR merges at
  the next work item's Open PR Gate.

## Findings
- R-0207 (reviewer authoring, Low): the R1 block ordered a "FROM
  occurs 0x" proof for all three FROM→TO receipts, but two were
  APPEND-shaped, where 0x is unattainable by construction. Fixed in
  R2: docs/agents/planner_reviewer_prompt.md §4 item 9 now names both
  proof shapes. Done: R-0207.
- R-0208 (reviewer authoring, Low): DECISION D7 below calls the
  roadmap ledger "the 250-item ledger". The disk says 255 —
  255 files in docs/roadmap/features/, 255 STATUS entries, and
  tests/docs/test_docs_consistency.py TOTAL_FEATURES = 255. The
  decision itself is unaffected (the pins reject an invented line at
  either count), but a wrong number persisted in a decision record is
  exactly the class this project polices. Fix: correct the number in
  D7.
  Done: R-0208 — D7 now reads 255-item.
- R-0209 (stale doc claim, Low): two PRIMARY_DOCS understate the
  ledger. AGENTS.md says the target plan is "ROADMAP.md + 250 feature
  detail files"; docs/README.md calls ROADMAP.md "the full
  250-feature" plan. Both predate F251-F255. The 150-file claim has a
  pin in tests/docs (TestPrimaryDocsAreHonest) and the 250 claim has
  none, which is why it survived. Fix: correct both texts AND add the
  pin in the SAME commit (planner_reviewer_prompt.md §3, R-0151).
  README.md line 89 ("Roadmap (250 features + registered items)") is
  a DIFFERENT and still-true statement — F001-F250 plus the five
  later registered items — and is deliberately not touched.
  Done: R-0209 — both texts corrected and pinned in one commit.
- Next free ID: R-0210.

## Decisions
- D5 (candidate sweep): the F080 candidate — a bundle verification
  record can never carry a full-suite node-id list — was resolved by
  writing the working shape into
  docs/roadmap/STATUS_closure_protocol.md as producer pitfall (d);
  .agent/candidates.md was emptied in the SAME commit. Alternatives
  considered: registering it as an R-id and carrying it open, or
  dropping it (the F056 failure the disk vehicle exists to prevent).
  Reversible by reverting one hunk. APPLIED in R1 (12e151df).
- D6 (round-type conflict): planner_reviewer_prompt.md §3 makes SPLIT
  mandatory for production code and forbids self-certified merges,
  while the self-drive requirement removes the human relay. Chosen:
  the two ROLES survive inside one session — the main session plans
  and reviews and never edits a work-tree file, and every write goes
  through a delegated worker subagent, one per round. What §3
  protects is reviewer independence from the writer, not the
  operator's keyboard. Alternatives considered: one undivided actor
  that self-certifies (the prohibited shape), or keeping SPLIT with a
  phone relay (the constraint that started this work). Reversible:
  the delegation clause is one paragraph.
- D7 (work-item selection): S1+S2 runs BEFORE F103 and claims no
  STATUS line. Rule A5 still names F103 as the next roadmap feature.
  Alternatives considered: claiming F103 first (misses the
  2026-08-12 date with no buffer), or inventing a STATUS entry
  (breaks the ROADMAP.md Part C grammar and the 255-item ledger
  pins). Reversible by any later relay.
- D8 (R-0207 fix route): amend planner_reviewer_prompt.md rather than
  the worker conventions, because the defect is in what the REVIEWER
  orders. Alternatives: a note in reviewer_conventions.md (read less
  often at authoring time), or leaving it as a live_review entry
  (dies with the branch). Reversible by reverting one hunk.
- D9 (R-0209 scope): fix the two documents that are wrong and pin
  them, and leave README.md line 89 alone because it is right.
  Alternatives considered: a regex pin over all PRIMARY_DOCS like the
  150 pin (it matches README.md line 89 and would force a false
  repair), or routing the whole class to T2_F083 (leaves two
  PRIMARY_DOCS lying while the fix costs one word each). The
  historical snapshot docs/ui/design_reference/
  FINAL_DESIGN_REFERENCE_SUMMARY.md also says 250; it describes what
  was verified on its own date and stays untouched. Reversible by
  reverting one hunk.

## Verdicts
- R1: PASS (2026-08-07). Range df39c3fa..54a99c8e. Transport, PRIMARY
  proof: eleven receipts cmp 0 against the reviewer's scratchpad
  originals; seven full-file applications cmp 0. Reviewer re-ran all
  six gates and matched every count. Mutation red-proof in a
  disposable worktree: renaming guardrail G2 turns
  test_self_drive_protocol_states_its_guardrails red. Full text in
  this file's git history (commit f043cf9c).
- R2: PASS (2026-08-07). Range 54a99c8e..151733e1, three commits, all
  tabled. Transport, PRIMARY proof: all five receipts cmp 0 against
  the reviewer's scratchpad originals — no digest fallback. r2-4 and
  r2-5 cmp 0 against .agent/plan.md and .agent/context.md. The
  two-step live_review application was verified by RECONSTRUCTION,
  not by counting: applying r2-3's FROM→TO to the r2-1 original
  reproduces the on-disk .agent/live_review.md byte for byte, and
  r2-3's FROM occurs exactly 1x in the base. The
  planner_reviewer_prompt.md hunk is exactly the authored TO, placed
  inside item 9 ahead of item 10, +10/-0. The worker correctly
  reported append-shape proofs and claimed no 0x count — the R-0207
  rule was in force the same round it landed. Ordering respected:
  the fix commit precedes the Done flip within it. Reviewer
  verification, independent re-runs at this HEAD: tests/docs/ 293
  passed · tests/ui_server/test_dashboard_contract.py 70 passed ·
  tests/orchestration/test_test_runner.py 51 passed ·
  tests/regression/test_resource_safety.py 21 passed ·
  tests/test_agent_tooling.py 10 passed 1 skipped ·
  tests/cli/test_golden_path.py 42 passed — every count equal to the
  worker's report, all exit 0. Part D delivered what it owed: Phase 0
  of the shipped protocol executes end to end, six commands exit 0
  and all nine named paths exist; the reviewer re-ran `remedy plan
  status` and `remedy plan next` independently with the same result.
  The handoff exceeded the 60-line cap and said so with its cause —
  the round itself ordered the full raw transcript into it; accepted,
  sections compressed and none dropped. The worker also surfaced the
  250/255 discrepancy instead of quietly matching the surrounding
  text, which is what raised R-0208 and R-0209. Primary checkout
  clean, no worktree, no force-push, no PR. Tier that ran: round gate
  + canary. No full-suite claim is made. LAST_REVIEWED_SHA =
  151733e1.
- R3: PENDING — awaiting the worker handback.
