OUTCOME: pending

# Received block — operator override 2026-07-31 (single-session micro-round)

Read docs/agents/planner_reviewer_prompt.md and act accordingly, with
this operator override: at the current feature boundary, run ONE small
micro-round (chore branch, authored texts per fidelity protocol, full
evidence discipline, standing operator approval for same-session
merge). Sequence: (0) if a closure PR waits, Open PR Gate first per
protocol — skip if none; (1) this round, including the normal
register-or-resolve pass over any carried closure CANDIDATES;
(2) merge on PASS; (3) continue per STATUS.md to whatever Rule A5
selects next.
Gate: tests/docs/ + canary. Expected ledger effect: R-0160 RESOLVED.

Item 1 — Named round types: production code never merges
self-certified. File: docs/agents/planner_reviewer_prompt.md (the
section governing rounds/blocks). Presence check: any rule naming
round types or restricting single-session execution. If absent, add,
tagged "operator ruling 2026-07-31, paydown0731 precedent": SPLIT
(default, mandatory for packages/, apps/, any production code path,
all feature work; production code never merges self-certified) vs
SINGLE-SESSION MICRO-ROUND (change set limited to docs/, tests/,
.agent/**, roadmap files; full fidelity ritual + evidence discipline
unchanged; labeled; standing approval covers only this type).
Retroactive note: paydown0731 ratified as founding precedent EXCEPT
its production-code commit (R-0159 guard fix class) — that kind
requires SPLIT from now on.

Item 2 — Symmetrize the worktree-only mutation rule (R-0160).
Files: planner_reviewer_prompt.md §4 item 10 + split_workflow.md
worker bootstrap bullet. If reviewer-only, amend both, tagged
"R-0160 fix, operator ruling 2026-07-31": destructive verification
only in disposable worktrees for EVERY role; primary checkout
porcelain-empty at every handback and every verdict. Then RESOLVE
R-0160 with the doc commit as evidence (honest-conduct note
preserved).

Item 3 — Relay semantics: "no questions" never means "no relays".
File: planner_reviewer_prompt.md §2 at the never-ask rule. If absent,
add one sentence, tagged "operator ruling 2026-07-31": never-ask bars
questions/menus/tasks at the operator — it does NOT reduce required
relays, and no directive phrase licenses collapsing SPLIT into
single-session; round type governed solely by Item 1's change-set
rule.

Constraints: token caps respected; AGENTS.md wins on conflict;
handback per template; every applied string in sha256-stamped blocks;
if ALL presence checks already satisfied and R-0160 resolved, skip
round, note in one line, proceed to step (3). No questions to the
operator at any point.
