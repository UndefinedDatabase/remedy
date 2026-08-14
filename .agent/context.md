# Context — F082 Self-benchmark

## Active Branch
feature/f082-self-benchmark, cut from main after PR #200 merged. F082 is
claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: the capability bench built on the gauntlet harness — a runner module under
`packages/orchestration/`, the five frozen order files, the per-run record
schema, the append-only history under the data root, and the `stats bench` CLI
surface; plus `.agent/f082_inventory.md`, the read-only T001 inventory,
`.agent/**` round state and the one claimed STATUS line. The exact file set is
NOT fixed until R2 has inventoried the harness: the feature file requires
inspecting the current shape before building, and its orchestrator brief names
the T001 factoring as the risky part.

Out: the gauntlet's pass definition, routing decisions — this feature only
RECORDS model context — and visual judgment, which is the F082 feature file's
Do-not-touch list. The gauntlet's own seven test files stay green UNMODIFIED;
a change that needs one of them edited is a finding, not a fix.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F082 owns.
- The reviewer measures its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5), with 240 the
  preferred target so the block-save commit stays inside the 500-insertion
  limit (R-0381).
- The bench never runs implicitly — on demand only, an F082 acceptance rule.

## Steps
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory → R3 T001 factoring, the five
orders and the record schema → R4 T002 history, trend and regression rules → R5
T003 CLI, model context and a fake-provider run → R6 the integration gate → R7
closure.
