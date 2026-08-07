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
  index + test pins. Four commits, each gated — PASS.
- R2 (SPLIT, LARGE, current): persist R-0207 and fix it in
  planner_reviewer_prompt.md, then dry-run the protocol's own Phase 0
  probe and record the raw transcript.
- R3 (planned): the PR round. No STATUS line, no evidence job, no zip
  (D7) — the PR is the end of the build and merges at the next work
  item's Open PR Gate.

## Findings
- R-0207 (reviewer authoring, Low): the R1 block ordered a "each
  applied FROM string now occurs 0x" proof for ALL three FROM→TO
  receipts, but r1-5 and r1-7 are APPEND-shaped — their TO contains
  the FROM verbatim, so 0x is unattainable by construction. The
  worker refused to fabricate the count and substituted a sound
  proof (FROM 1x plus each TO-only addition 1x), which the reviewer
  accepts. The defect is the reviewer's instruction, not the work.
  Fix: write the two proof shapes into
  docs/agents/planner_reviewer_prompt.md §4 item 9, so the rule
  lives on disk instead of in reviewer session memory (the A1 trap
  §0 names).
- Next free ID: R-0208.

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
  (breaks the ROADMAP.md Part C grammar and the 250-item ledger
  pins). Reversible by any later relay.
- D8 (R-0207 fix route): amend planner_reviewer_prompt.md rather than
  the worker conventions, because the defect is in what the REVIEWER
  orders. Alternatives: a note in reviewer_conventions.md (read less
  often at authoring time), or leaving it as a live_review entry
  (dies with the branch). Reversible by reverting one hunk.

## Verdicts
- R1: PASS (2026-08-07). Range df39c3fa..54a99c8e, five commits, all
  tabled in the handoff. Transport, PRIMARY proof: all eleven
  receipts cmp 0 against the reviewer's scratchpad originals — no
  digest fallback needed — and the seven full-file applications
  (live_review, plan, context, candidates, self_drive_protocol.md,
  SKILL.md, build-remedy-self.md) cmp 0 against their receipts. The
  three FROM→TO applications were read as diffs, not counted: each
  is exactly the authored TO and touches nothing else. The test
  append is a pure end-of-file addition, no existing line changed.
  Path set is exactly the instructed one; nothing under packages/,
  apps/ or scripts/, and no STATUS.md edit. Open PR Gate executed
  correctly (#184 merged, branch deleted, `gh pr list` now empty).
  Reviewer verification, independent re-runs at this HEAD:
  tests/test_agent_tooling.py 10 passed 1 skipped · tests/docs/ 293
  passed · tests/ui_server/test_dashboard_contract.py 70 passed ·
  tests/orchestration/test_test_runner.py 51 passed ·
  tests/regression/test_resource_safety.py 21 passed ·
  tests/cli/test_golden_path.py 42 passed — every count equal to the
  worker's report, all exit 0. Mutation red-proof (disposable git
  worktree at HEAD, removed and pruned before this verdict; primary
  checkout `git status --porcelain` empty): renaming guardrail G2 in
  the protocol turned test_self_drive_protocol_states_its_guardrails
  red, so the pin catches a dropped guardrail rather than merely
  passing. The protocol's own Phase 0 was exercised by the reviewer:
  `remedy plan status` and `remedy plan next` both exit 0 and report
  F103, and every file path the protocol and skill name exists. Tier
  that ran: round gate + canary. No full-suite claim is made.
  LAST_REVIEWED_SHA = 54a99c8e.
- R2: PENDING — awaiting the worker handback.
