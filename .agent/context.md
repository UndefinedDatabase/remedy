# Context — F107 Context compiler v2

## Active Branch
feature/f107-context-compiler-v2, cut from main at 2e4142c3 after PR #191
was merged at the Open PR Gate. F107 is claimed `[~]` under Rule A5 as the
first `[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use, Tier 2).

## Scope
In: packages/orchestration/context_compiler.py — import-neighbor graphs
(Python via ast, TS/JS via a documented line-level import scanner),
signature extractors, the tiered selector (the tier table of
docs/roadmap/features/T2_F107.md is the contract), budget demotion,
omitted_context.json, segment integration and the `remedy job context`
debugging view. Tests under tests/orchestration/test_context_compiler.py.

Out, per the feature file's Do-not-touch: prompt composition (the segment
registry owns it), retrieval/embedding approaches, repo-map features.
No TS parser dependency — reject any diff adding one; the line scanner is
an honestly documented heuristic.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/,
  and production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable
  git worktree, so resource safety stays intact and no background pytest
  process is ever left running.
- Dynamic imports and string-based requires are invisible to v1 — a
  documented limitation with the files_hint escape hatch (A9 defaults in
  the feature file).

## Steps
R1 claim, candidate sweep and state reset → R2 T001 import-neighbor
graphs → T002 signature extractors → T003 tiered selector + budget
demotion + omissions writer → T004 segment integration + CLI view +
end-to-end fixture → integration gate → closure.
