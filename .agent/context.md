# Context — amend0827 process diet

## Active Branch
feature/amend0827-process-diet, cut from `main` at `f4eae1d4`, the merge
commit of pull request #215 which closed F031.

## Scope
The six process rules of operator collection order amend0827, and the four
`.agent/candidates.md` entries the F031 closure left behind. This is not
feature work and claims no STATUS line. No file under `packages/` or
`apps/` is touched, and no test is added, changed or deleted.

## Do not touch
The block caps themselves (490 total / 400 prose / `.agent/plan.md` under
50) — rule 3 keeps them deliberately. The mutation red-proof obligation for
production code — rule 5 keeps it in full. The append-only property of
`.agent/live_review.md` and `.agent/decisions.md`.

## Assumptions
- The operator prompt carries the authorization for all six rules and for
  every candidate disposition; none of them is a question to the operator.
- The rules bind from their amendment date forward. Landed findings are
  NOT rewritten: the record is append-only, so rule 2 reclassifies nothing
  that already has a number.
- `.agent/prose_slips.md` is runtime state, not documentation, so it is
  registered in AGENTS.md under Runtime State Management and not in
  `docs/README.md`.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not F031's and not
this order's, and deleting them with the rest of a rewrite is what cost an
earlier round a red CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.

This order's own constraints:

- `tests/test_agent_tooling.py` pins six substrings in
  `docs/agents/self_drive_protocol.md` by text ("Open PR Gate", "Never
  force-push", ".agent/STOP", "worker subagent", "git worktree",
  "handoff"). An amendment there keeps all six.
- `tests/docs/test_docs_consistency.py` resolves every markdown link in
  AGENTS.md against disk, so a new path is named in backticks or its file
  exists in the same commit.
