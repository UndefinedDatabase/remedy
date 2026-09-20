
## DECISION F276 D1 (2026-09-20, reviewer, round 1) — the data root's classes are DATA in `data_paths`, `data` is an advanced group, and the partition test's ruled count moves from thirty to thirty-one
CONTEXT: T001 of `docs/roadmap/features/T2_F276.md` orders `EPHEMERAL_CLASSES` and `DURABLE_CLASSES`
"both declared as data", an architecture test that reds on an unclassified child, and a read-only
`remedy data usage`. Two things the feature file does not settle had to be: where the new command's
group sits in the CLI surface, and what happens to `tests/cli/test_cli_ux.py::TestGroupDefIntegrity::test_catalog_partition_matches_d4`,
which asserts `len(GROUPS) == 30` for the partition DECISION amend0905-vocab D4 names. A research
helper inventoried the data root at `6daeb66e` by scanning `packages/`, `apps/` and `scripts/` and by
calling every `*_dir()` helper; the reviewer re-applied that work in its own worktree and re-ran it.
CHOSEN: (1) five ephemeral classes — `job_workspaces`, `workspaces`, `runs`, `job_logs` and the
`review_staging.*` prefix class — and fifteen durable ones, each entry a frozen `DataRootClass`
naming its owning module and its reclaim rule, with `classify_data_child` and `data_class_dir` as the
only readers; the eleven class-named `*_dir()` helpers resolve through `data_class_dir`, so an
unregistered name raises instead of composing a path. (2) The feature file's "ping-pong runs" and
"task jobs" get NO entry: no code creates either today — ping-pong results live in `runs/` and
`task_jobs/` was retired by DECISION F260 D-A — and a legacy `task_jobs/` on an operator disk reports
as `unclassified`, which is the honest answer and the one `data usage` prints. (3) The `data` group is
`user_facing=False`: it is advanced, reachable through `--all-commands`, and it does NOT enter
`VISIBLE_GROUP_ORDER`, which D4 and DECISION amend0911-feedback D1 pin at sixteen visible groups plus
two reserved slots. That pin is untouched; only the catalog's total moves, and the partition test's
docstring says which group the thirty-first is and that it was added after D4 was ruled.
ALTERNATIVES: a visible `data` group, rejected because it would edit the pinned visible order for a
command an operator runs when disk runs out, not daily; leaving the helpers spelling their own
literals beside the registry, rejected because two spellings of one name is what the registry exists
to end; asking the operator to re-rule D4 before building, rejected under amend0917-throughput (5) —
the recommendation is executed and stays reversible.
REVERSE: delete the `data` GroupDef and the `data.usage` entry from `apps/cli/command_catalog.py`,
restore `assert len(GROUPS) == 30` and the `_INTERNAL_GROUPS` set in `tests/cli/test_cli_ux.py`,
delete `apps/cli/commands/data_cmd.py`, `packages/orchestration/data_footprint.py`,
`tests/test_data_root_classes.py`, `tests/orchestration/test_data_footprint.py` and
`tests/cli/test_data_cmd.py` with their two allowlist lines, restore `packages/orchestration/data_paths.py`
from `43d14817`, and delete this paragraph.

## DECISION F276 D2 (2026-09-20, reviewer, round 1) — F276's first round repairs the test that reddens hosted CI on `main`, although the repair is nobody's planned scope
CONTEXT: pull request 260 merged F273's closure into `main` at this session's Open PR Gate as
`43d14817`. Its hosted run 35470120934 on `6daeb66e` had failed BOTH columns on one node,
`tests/cli/test_study_cmd.py::TestStudyCommandReachability::test_study_run_dispatch_e2e`, which is
green in the primary checkout and absent from F273's committed closure-suite transcript. The cause,
measured this round, is R-1001: the node asserts that a probe contacted the loopback host the test
supplies, and that probe cannot exist without the optional `ollama` extra that hosted CI does not
install. Under amend0911-feedback rule A the finding would default to F282, the next findings-paydown
feature, and `main` would stay red until F282 runs.
CHOSEN: F276 registers R-1001 in its first commit and repairs it in the next one, in the same round,
and owns it. The repair guards the assertion with `importlib.util.find_spec("ollama") is not None`
and leaves everything else standing, including the fake host that is what actually bounds the
subprocess away from a real model. A red column on `main` is read by every later feature's closure
evidence, so carrying it is more expensive than a nine-line test edit that four runs proved.
ALTERNATIVES: adding `ollama` to the `dev` extra so hosted CI installs it, rejected because it arms a
real provider import across every CI job to fix one assertion; deleting the assertion, rejected as a
weakened test; leaving it to F282 with the column red meanwhile, rejected for the reason above.
REVERSE: restore `tests/cli/test_study_cmd.py` from `43d14817`, and delete this paragraph.
