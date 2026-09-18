
## Built State (F268, 2026-09-18)

What exists on disk at the close of F268; every DECISION named lives in `.agent/decisions.md`.

**T001 — the sequence as data.** `packages/orchestration/do_sequence.py` holds `DO_SEQUENCE =
("init", "study", "plan", "shape", "run", "ui", "apply")` and `walk_do_sequence`, which walks it
over a `DoContext` (DECISIONs F268 D1 to D4). `init` registers an unregistered git repository or
selects `--project`'s; `study` runs once on a non-empty, never-studied repository and records
`studied_at` and `studied_head`; `plan` creates the mission and its plan; `shape` plans the jobs
linked to the mission; `run` runs the first job; `ui` opens the cockpit detached through
`launch_do_cockpit` unless `--no-ui`; `apply` stops before apply unless `--apply`.
`tests/cli/test_do_sequence_cli.py` holds a test per step boundary on the fake provider.

**T002 — shape and deliverables.** `resolve_do_shape` reads the planner's outlines (two or more
are milestones) and lets `--force-job` or `--force-mission` override it (DECISION F268 D5).
`packages/orchestration/task_deliverables.py` gives every task the deliverable it produces;
`validate_deliverable_plan` rejects a plan holding a task without one, and
`deterministic_job_plans` plans one task per deliverable within the granularity ceilings
(DECISION F268 D6; `tests/orchestration/test_task_deliverables.py`).

**T003 — halts.** `--step-by-step` halts between steps through `do_step_by_step_halt`, reading
Enter or `q` with no model call in flight; `--plan-only` ends the walk after shape (DECISION
F268 D8).

**T004 — cockpit and apply.** The ui step opens the cockpit detached; `--apply` applies the job
that ran; `--contract`, `--commit`, `--commit-auto`, `--commit-with-history` and `--push` exit 2
naming the feature that brings them (DECISION F268 D9). A walk of two or more jobs runs job 1 and
names each waiting job with the commands that continue it (DECISION F268 D12).

**T005 — the quick start.** `remedy --help` and the README carry five numbered lines that each
exit 0 as printed on a fixture repository (DECISIONs F268 D14 and D15;
`tests/cli/test_quick_start.py`).

**One route, one flag list.** Every `remedy do`, with or without the word `run`, walks the
sequence; the autorun branch, its four flags and the `do` v1 flow of
`packages/orchestration/do_run.py` are deleted, and `do` honours `--project`, the budget flags and
`--builder-model`, `--reviewer-model` and `--planner-model` (DECISIONs F268 D16 and D17;
`tests/cli/test_do_flags.py`). `--planner-provider` is not created (operator question Q3).

**Cost and evidence.** `do` mirrors each job run into the F103 ledger and prints the measured
tokens per role and cost; the builder's context per task and round reaches
`context_strategy.json` (DECISION F268 D11). `export_job_evidence` writes `job_flow.json`, the
agent run trace and its summary and `command_transcript.json` from the job's own records, so a
fake-provider `do` job's package passes the review-package check (DECISION F268 D13;
`tests/cli/test_do_evidence_package.py`).

**Findings.** R-0808, R-0811, R-0897, R-0933, R-0968 and R-0969 were resolved inside the feature.
R-0892 stays open for its `.claude/skills/remedy-evidence-review/SKILL.md` half, which the
session's permission system refused to write (operator question Q2), and R-0807 for its F260 half.
