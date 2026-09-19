
## Built State (F271, 2026-09-19)

What exists on disk at the close of F271; every DECISION named lives in `.agent/decisions.md`.
The rule "Replacing is deleting" sits under AGENTS.md's Scope Control section, not under Core
Workflow as the DECISIONs section above says.

**T001 — ownership and reach.** `GroupDef` in `apps/cli/command_catalog.py` carries `feature`, the
owning feature id, and `reach`, one of the seven values of `Reach`: golden-path, job-path,
mission-path, self-use, teacher, cockpit and self-build. Both are defaulted, so a group missing
either is refused by `TestGroupOwnership` in `tests/test_command_catalog.py`, not by an import
error; the test also refuses a feature id with no line in `docs/roadmap/STATUS.md`. Every group of
the catalog is annotated; the owner rule and the table are DECISION F271 D1 (3).

**Design (c) — no orphan modules.** `tests/test_no_orphan_modules.py`, in `ARCHITECTURE_FILES` and
the `budgets` CI stage, fails on any module under `packages/`, `apps/` or `scripts/` that has no
importer outside `tests/` and that no entry point names. It counts a script run by path from
`pyproject.toml`, a shell file or a workflow as reached. An `ALLOWED_UNWIRED` entry states its
reason and fails once its module is gone or reached, so the list can only shrink. A synthetic tree
keeps the scanner's red proof standing (DECISION F271 D2). Of the nine modules the Design
measured, four are deleted with their tests — `builder_eval.py` with
`scripts/remedy_builder_eval.sh` (DECISIONs amend0911-feedback D6 and F271 D1),
`diagnostic_comparison.py`, `task_plan_evidence.py` and `execution_config_evidence.py` (D2).
`patch_revert.py`, which the `patch.revert` command no longer used, is deleted under D3 as finding
R-0982. The other four are allowed with their reasons, as are the modules the Design did not name.

**T002 — the closure precondition and the dead-command section.** Precondition 7 of
`docs/roadmap/STATUS_closure_protocol.md` requires the reachability test and the orphan-module
test green in the closure transcript. A line a feature adds to either list is named in its feature
file, and the precondition cites the AGENTS.md rule. The `doctor core` dead-command section F281
built is proved by `TestDoctorCoreDeadCommands` in `tests/cli/test_worker_facade_cmd.py`, which
plants a command nothing references and sees it listed in the JSON and text output (DECISION F271
D3).

**Findings.** R-0893 is resolved: `agent_run_trace.py` has a production importer,
`packages/orchestration/job_evidence.py`, on the `do` path. R-0982 was raised and resolved inside
the feature. R-0980 (a smoke-script section requires an event no product path emits) and R-0981
(the role conventions segment is registered by no prompt builder) were found here and are owned by
F273. No finding owned by F271 stays open.
