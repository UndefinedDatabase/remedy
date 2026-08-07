## What changed

Adds the one-session build discipline ("self-drive") the operator needs
from 2026-08-13, when this machine is reachable only over SSH from a
phone and starting Claude Code plus invoking ONE skill has to be the
whole touchpoint.

- `docs/agents/self_drive_protocol.md` (new) — the protocol: role model,
  Phase 0 state probe, Phase 1 decide, the round loop, guardrails G1-G8,
  and how a session ends.
- `.claude/skills/remedy-self-drive/SKILL.md` and
  `.claude/commands/build-remedy-self.md` (new) — the two entry points,
  both thin pointers at the protocol rather than second sources of
  truth.
- `docs/README.md`, `.claude/README.md` — index and contents
  registration.
- `tests/test_agent_tooling.py` — three pins: the entry points exist and
  point at the protocol, the protocol still states each guardrail, and
  the protocol is registered in the docs index.
- `docs/roadmap/STATUS_closure_protocol.md` — producer pitfall (d): a
  bundle verification record can never carry a full-suite node-id list
  (the F080 R4 closure candidate, now swept from
  `.agent/candidates.md`).
- `docs/agents/planner_reviewer_prompt.md` — §4 item 9 now names both
  FROM-TO proof shapes, rewrite and append (R-0207).
- `AGENTS.md`, `docs/README.md`, `tests/docs/test_docs_consistency.py` —
  the roadmap ledger is 255, not 250; corrected and pinned in one commit
  (R-0209).

## Why

Relaying paste blocks between two windows stops being possible on
2026-08-13. The relay therefore moves into the session — but everything
the relay was protecting stays: evidence-first review, the block
conditions, PR-only merges.

## Key decisions

- **D6 — the roles survive inside one session.** The main session plans
  and reviews and never edits a work-tree file; every write goes through
  a delegated worker subagent, one per round. `planner_reviewer_prompt.md`
  §3 protects reviewer independence from the writer, not the operator's
  keyboard, so delegation satisfies it without a human relay. A round
  where one actor both wrote and certified is void by the protocol's own
  text.
- **D7 — no STATUS line.** This is infrastructure, not a roadmap
  feature. `STATUS.md` stays the roadmap ledger and Rule A5 still names
  F103 next. Consequently there is no evidence job and no review zip:
  this PR is the end of the build.
- **D9 — the stale-count fix is scoped.** `AGENTS.md` and
  `docs/README.md` were wrong and are fixed and pinned. `README.md` line
  89 ("250 features + registered items") is a different, still-true
  statement and is deliberately untouched, which is why the pin names
  documents instead of matching a pattern across all of them.

## How to review

1. Read `docs/agents/self_drive_protocol.md` first — everything else
   points at it.
2. The guardrails are load-bearing; the pin that protects them was
   red-proofed in a disposable worktree (renaming G2 turns
   `test_self_drive_protocol_states_its_guardrails` red). The new
   ledger-count pin was red-proofed the same way (reverting both counts
   to 250 turns `test_no_doc_understates_the_feature_count` red, and
   nothing else).
3. Gates, per round: `python3 -m pytest tests/docs/ -q`,
   `tests/test_agent_tooling.py`, `tests/ui_server/test_dashboard_contract.py`,
   `tests/orchestration/test_test_runner.py`,
   `tests/regression/test_resource_safety.py`, and the canary
   `tests/cli/test_golden_path.py`. All green at every round, re-run
   independently by the reviewer.
4. Phase 0 of the shipped protocol was executed end to end in R2: six
   commands exit 0, all nine named paths exist. The raw transcript is in
   the R2 handoff.

## Status

- R1, R2 and R3 all PASS. The build is complete and reviewed.
- Open findings: 0. R-0207, R-0208, R-0209 and R-0210 all Done; next
  free ID R-0211.
- Rounds: 5 — R4's first attempt was stopped by a truncated reviewer
  receipt and reported rather than guessed; nothing was written from
  reconstructed text. Tokens and cost: not-measured — no provider run
  was executed on this branch.
- Not merged here by design: this PR merges at the next work item's Open
  PR Gate, which is the operator's manual-review window.

## What is NOT proven yet

Phases 1 and 2 of the protocol have never run for real. The acceptance
test is the S4 rehearsal — F254 built end to end through the skill with
the operator present — and it has not happened. Nothing in this PR
claims otherwise.
