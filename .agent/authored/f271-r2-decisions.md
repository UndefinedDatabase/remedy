
## DECISION F271 D2 (2026-09-19, reviewer, round 2) — the orphan-module test, its entry-point rule, and how the unreached modules are resolved
CONTEXT: `docs/roadmap/features/T2_F271.md` Design (c) orders `tests/test_no_orphan_modules.py`: an
AST pass over `packages`, `apps` and `scripts` that fails on any module with zero non-test
importers, excluding `__init__.py`, the documented reserved namespaces and an `ALLOWED_UNWIRED`
tuple with a one-line reason per entry, listed in `ARCHITECTURE_FILES` and registered in the
`budgets` CI stage; and it orders the nine modules it measured resolved, wired or deleted. A
research helper's first scan at `a4f79a94`, counting only imports, found 41 modules with no
importer outside `tests/`, most of them scripts that a tracked shell file or workflow runs by path
or files of a fixture project. Its prototype at `c798fd2d`, with the rule below, finds 19: of the nine, `builder_eval.py` is already gone
(D1) and eight remain, plus `autonomy_loop.py`, `event_schemas.py`, `hunk_apply.py`,
`role_conventions.py`, `self_use_generator.py`, `self_use_runner.py`, `apps/cli/main.py`,
`packages/contracts/interfaces.py`, `scripts/remedy_agent_tooling_doctor.py`,
`scripts/rotate_live_review.py` and `scripts/self_run_gauntlet.py`.
CHOSEN: (1) REACH. A module is reached by a static import in a non-test file under the three trees
or at the repository root (relative imports resolved, `from pkg import mod` reaching the
submodule, every name reaching its ancestor packages, a script's bare `import x` also reaching
`scripts.x`), by `importlib.import_module` with a literal, by a script path literal inside
`scripts/`, or by the ENTRY-POINT rule: its repository path or dotted name appears in
`pyproject.toml`, in a `*.sh` at the root or under `scripts/`, or in a workflow under `.github/`,
and a `x.py` token in a `.sh` reaches the `x.py` beside it. The walk reads the filesystem and
skips caches, `node_modules`, virtualenvs, `dist`, `build` and `.remedy-wt`. (2) EXEMPT: every
`__init__.py`, and the reserved namespace `scripts/gauntlet_sample_project/`, a fixture project.
(3) TESTS: no unlisted orphan; every `ALLOWED_UNWIRED` entry is a live orphan, so the list only
shrinks; every entry carries a one-line reason; and a synthetic tree under `tmp_path` that
plants one orphan and exercises every reaching form yields exactly its two orphans — the
scanner's red proof, standing. (4) DELETED in this round, each with the test file that exists
only for it: `diagnostic_comparison.py`, `task_plan_evidence.py` and
`execution_config_evidence.py`. What stays in the repository after the deletion, by design: two
pins in `tests/docs/test_docs_consistency.py` that quote the historical text of
`docs/roadmap/features/T0_F012.md`, and the negative assertion in
`tests/orchestration/test_job_evidence.py` that keeps a hardcoded verification list out of
`job_evidence.py`. (5) ALLOWED, with the reason the test file carries: the other 16, among them
the five of the nine that are neither deleted by D1 nor by (4) — `feature_mission_adapter.py`
(F080's adapter, whose consumer is F248's loop), `patch_revert.py` (finding R-0982, owned by this
feature), `ci_budgets.py` (the ceilings the `budgets` stage's test compares), `bench_run.py`
(F082's on-demand run) and `self_use_findings.py` (run by hand under closure precondition 6) —
and `role_conventions.py` (finding R-0981). An entry
naming a finding leaves the list when that finding is resolved. (6) `MEASURED_MAX_WALL_S["budgets"]`
in `tests/orchestration/test_ci_stages.py` is left at its recorded 1.32 s. The prototype measured
the stage at about 3.1 s with the new file, and the budget rule still gives 300 s, so the budget
itself does not change.
ALTERNATIVES: an import-only scan, rejected because it flags the scripts that shell files and
workflows run by path; deleting every module that has no importer, rejected because hand-run
closure tools and modules kept by earlier DECISIONs (F275 D18, F033 D4) would go with them, and
the Design's "wired or deleted" is then met by an allowance that has to state its reason and fails
when that reason stops being true; walking `git ls-files`, rejected because the planted-orphan
check would then need a commit to be seen.
REVERSE: delete `tests/test_no_orphan_modules.py` and its two registrations, restore the three
deleted modules and their tests from `c798fd2d`, and delete this paragraph.
