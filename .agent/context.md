# Context — F070 Orchestrator loop inside Remedy (Tier 1)

## Active Branch
`feature/f070-orchestrator-loop`
Base commit: main after PR #175 merge (F069 closure), `afbe2639`

## Steps (round map)
R1 (SPLIT, LARGE bundle): Open PR Gate (#175) + claim `[~]` + authored
state; then the verb map (inspection only, recorded in decisions.md);
then T001 — the OrchestratorMove schema, context assembly, the
`run_mission` skeleton and the ledger writer with fake-provider unit
tests; then T002 — evaluation wiring (job terminal + milestone DoD),
the dossier update call, and the era fixture corpus with one detection
test per finding class.
Next: T003 end-to-end two-milestone fixture mission — its own round.
Then: integration gate per docs/agents/integration_gate.md (R-0169 doc
hardening lands there). Then: closure — its own round.

## Scope
`packages/orchestration/**` (new `orchestrator_loop.py`, the move
schema, the ledger writer, the era fixture corpus),
`docs/agents/orchestrator_protocol.md` (the versioned protocol
document the orchestrator system prompt is generated from),
`tests/orchestration/test_orchestrator_loop.py` plus fixtures under
`tests/orchestration/fixtures/`, `docs/roadmap/STATUS.md` (claim line
only), and `.agent/` state. The CLI surface (`remedy mission run`,
`remedy mission ledger`) lands here or in T003 — the choice is
recorded in decisions.md. Nothing beyond.

## Gates (round verification, pytest)
python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q
                                                  T001 slice gate
python3 -m pytest tests/orchestration/ -q         T002 slice gate
python3 -m pytest tests/cli/test_golden_path.py -q    canary
python3 -m pytest tests/docs/ -q                      docs-round gate
Integration gate: full suite with pytest -n auto, branch AND base,
per docs/agents/integration_gate.md — a later round.
Resource safety: everything runs through these pytest wrappers; the
loop's tests use a fake provider only and start no real process, so
there is no subprocess fan-out to bound.

## Constraints
- A6: the loop is a POLICY layer. Intake/flight-plan generation, plan
  approval, the multi-cycle executor, DoD evaluation, reports,
  escalation and postmortems are CALLED, never reimplemented. The
  verb map in decisions.md is the reuse record.
- The move schema is validated through the EXISTING structured-call /
  schema-registry mechanism — no second validation path.
- Authority boundary is enforced by schema shape: no move kind creates
  missions or edits goals; an unknown kind is a parse-class failure.
- Context assembly puts the dossier FIRST (cache-stable prefix).
- Stop requests and answered decisions are read EVERY iteration; safe
  points are between iterations.
- One provider call per iteration, role "orchestrator", top-tier model
  via a CONFIG key only — no model-routing-policy change.
- Iteration limit comes from config with a conservative default;
  hitting it is a normal terminal with an honest status.
- The protocol document is versioned in-repo and never self-modified
  at runtime.
- A job proposed for an already-done milestone is refused with a
  recorded reason, re-prompted ONCE, then escalated through the
  existing escalation verb — never a silent loop.
- Reviewer-authored texts under .agent/authored/ are applied by copy
  and sha256-verified before use; never hand-edited.
- SPLIT round: production code merges only after reviewer PASS; the
  worker never writes Verdicts or Resolved lines.
- Commits stay under 500-line diffs (AGENTS.md).
- Mutation red-proofs only in a disposable git worktree (R-0160); the
  primary checkout is porcelain-clean at handback.
- context.md satisfies its FULL test reader list: a "Steps" section,
  "## Active Branch" with a feature/ slug, a roadmap F-id, and this
  pytest/resource line (R-0162; reader rule in
  planner_reviewer_prompt.md §4 item 11).

## Do not touch
New goal creation paths. Model routing policy (a config key only).
Self-modification of the protocol document at runtime. Harness /
process semantics. docs/roadmap/ROADMAP.md; STATUS entries other than
the F070 claim line.
