# Development Artifact Boundary v0

## What `.agent/live_review.md` is

A development-time coordination file used by Builder and Reviewer prompts during
Remedy's own development cycle. It tracks review findings, verdicts, and protocol
compliance for the current development block.

## What `.agent/live_review.md` is NOT

- NOT product runtime state
- NOT job/mission evidence or report truth
- NOT approval policy input
- NOT runtime decision input
- NOT user-facing product truth
- NOT canonical progress truth
- NOT core product readiness truth

Normal Remedy users never need to read, edit, or depend on this file.

## Allowed development uses

| Use | Relative Path | Classification |
|-----|--------|----------------|
| Parse review verdict for self-dogfood gates | `packages/orchestration/self_dogfood.py` | development self-test |
| Parse review findings for self-dogfood execution | `packages/orchestration/self_dogfood_execution.py` | development self-test |
| Orchestrator brain context | `packages/orchestration/orchestrator_brain.py` | development context |
| Integrity gate checks | `packages/orchestration/integrity_gate.py` | development process health |

## Disallowed product/runtime uses

The following modules must NOT depend on `.agent/live_review.md`:

- `worker_facade_cmd.py` — worker commands must use structured run/mission state

Guard tests enforce this boundary (see
`tests/orchestration/test_development_artifact_boundary.py`).

## Current legacy dependencies

All current `.agent/live_review.md` reads are in development/self-dogfood paths.
No product-facing operator command depends on it for core functionality.

`progress_cmd.py` READ it for developer convenience display, and it was classified
as a development command rather than a core product operator command. F275 deleted
that handler with the whole `progress` command group, and nothing product-facing
replaced it, so no command reads this file for display today.

## Planned migration path

1. Core operator commands (`worker`, `mission`, `approval`) already use structured state
2. The development command `progress` may continue reading `.agent/` files
3. Future blocks may migrate remaining self-dogfood paths to structured event ledger
4. No urgent migration needed — boundary is enforced for new product paths

---

## Product Truth Source Map

Product questions must be answered from structured Remedy state:

| Question | Structured Source | Relative Path |
|----------|------------------|--------|
| Mission status | Mission records | `mission_state.py` |
| Test status | Real test execution records | `real_test_execution.py` |
| Repair proposal status | Self-repair proposal records | `self_repair_proposals.py` |
| Proof status | Proof chain records | `file_provenance.py` |
| Config status | Config diagnostics | `config_diagnostics.py` |

These sources are structured JSON, persisted to `data_dir`, and testable without `.agent/`.
