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
- R1 (SPLIT, LARGE, current): Open PR Gate (#184) + candidate sweep +
  closure-protocol amendment + protocol doc + skill + command + docs
  index + test pins. Four commits, each with its own gate.
- R2 (planned): review + repair + the docs/agent-tooling gates, then
  the S4 rehearsal decision (F254 through the skill).

## Findings
- 0 open findings carried in. Next free ID: R-0207.
- Closure candidate from F080 R4 (.agent/candidates.md): RESOLVED
  inline as DECISION D5 — no R-id spent, per
  docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
  findings") and docs/agents/planner_reviewer_prompt.md §4 item 7.

## Decisions
- D5 (candidate sweep): the F080 candidate — a bundle verification
  record can never carry a full-suite node-id list — is resolved by
  writing the working shape into
  docs/roadmap/STATUS_closure_protocol.md as producer pitfall (d),
  and .agent/candidates.md is emptied in the SAME commit.
  Alternatives considered: registering it as R-0207 and carrying it
  open (keeps the ledger busy for a documentation edit already fully
  understood), or dropping it (loses the precedent, which is exactly
  the F056 failure the disk vehicle exists to prevent). Reversible by
  reverting one hunk.
- D6 (round-type conflict): planner_reviewer_prompt.md §3 makes SPLIT
  mandatory for production code and forbids self-certified merges,
  while the self-drive requirement removes the human relay. Chosen:
  the two ROLES survive inside one session — the main session plans
  and reviews and never edits a work-tree file, and every write goes
  through a delegated worker subagent, one per round. What §3
  protects is reviewer independence from the writer, not the
  operator's keyboard. Alternatives considered: one undivided actor
  that self-certifies (rejected — it is precisely the prohibited
  shape), or keeping SPLIT and having the operator relay from a phone
  (rejected — it is the constraint that started this work).
  Reversible: the skill's delegation clause is one paragraph.
- D7 (work-item selection): S1+S2 runs BEFORE F103, and claims no
  STATUS line. Rule A5 names F103 as the next roadmap feature and that
  is unchanged; the self-drive track is infrastructure with a hard
  operator date (2026-08-12) that F103 does not have, and
  .agent/plan.md plus .agent/selfdrive_package.md already sequence it
  first. Alternatives considered: claiming F103 now and building the
  skill afterwards (misses the date with no buffer), or inventing a
  STATUS entry for the skill (breaks the ROADMAP.md Part C grammar and
  the 250-item ledger pins). Reversible by any later relay.

## Verdicts
- R1: PENDING — awaiting the worker handback.
