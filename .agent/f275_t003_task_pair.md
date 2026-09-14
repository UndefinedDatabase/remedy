# F275 T003 — the second type pair, `Task` against `TaskEntry`

## 1. Banner

Measured at base `6537ece6`, by IMPORTING the two shipped record classes
rather than reading their source, and by `ast` over the tracked `.py` files.

NO LINE under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in
F275 round 40, the round that wrote this file. Its whole change set is under
`.agent/`: this is a MEASUREMENT of the flip ahead, not a step of it.

`Job.tasks` is `list[Task]` and `JobPlan.tasks` is `list[TaskEntry]`, so a
consumer moved from the classic record to the unified one moves BOTH types.
DECISION F275 D22 is the ruling drawn from the figures below.

## 2. The instrument

Run from the repository root as `python3 -B .remedy-wt/r40_task_pair.py`.

The tool is written to the
gitignored `.remedy-wt/` scratch, never to a repository root, because
`ruff check .` would collect a file left there; its source is embedded here
verbatim so the measurement is reproducible from this artefact alone.

```python
"""F275 T003 — the SECOND type pair, measured: `Task` against `TaskEntry`.

`Job.tasks` is `list[Task]` and `JobPlan.tasks` is `list[TaskEntry]`, so a
consumer moved from the classic record to the unified one moves both types. This
reads the two shipped classes rather than their source, then counts the `Task`
type sites the flip must carry, then asks whether the fields with no counterpart
are READ anywhere — which is what decides whether the flip owes a finding under
operator amendment amend0908-f275-finish rule 4.
"""
import ast
import collections
import dataclasses
import subprocess

from packages.core.models import Task
from packages.orchestration.pingpong_job import TaskEntry

ORPHANS = ("budget", "output_artifact_ids", "acceptance_checks")


def annotation_names(node, depth=0):
    out = set()
    if node is None or depth > 3:
        return out
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            try:
                out |= annotation_names(ast.parse(n.value, mode="eval").body, depth + 1)
            except SyntaxError:
                pass
    return out


def params(n):
    a = n.args
    return (list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)
            + [x for x in (a.vararg, a.kwarg) if x is not None])


def main():
    task_fields = dict(Task.model_fields)
    entry_fields = {f.name: f for f in dataclasses.fields(TaskEntry)}
    print("Task fields:", len(task_fields))
    for name, f in task_fields.items():
        print(f"    {name} :: {f.annotation}")
    print("TaskEntry fields:", len(entry_fields))
    for name, f in entry_fields.items():
        print(f"    {name} :: {f.type}")
    shared = sorted(set(task_fields) & set(entry_fields))
    print("shared names:", shared)
    print("Task-only names:", sorted(set(task_fields) - set(entry_fields)))

    files = subprocess.run(["git", "ls-files", "*.py"],
                           capture_output=True, text=True).stdout.split()
    kinds = collections.Counter()
    lines = set()
    reads = collections.defaultdict(list)
    for path in files:
        try:
            tree = ast.parse(open(path, "rb").read(), filename=path)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id == "Task":
                kinds["constructions"] += 1
                lines.add((path, n.lineno))
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                if any(a.name.split(".")[-1] == "Task" for a in n.names):
                    kinds["imports"] += 1
                    lines.add((path, n.lineno))
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in params(n):
                    if "Task" in annotation_names(arg.annotation):
                        kinds["annotations"] += 1
                        lines.add((path, arg.lineno))
                if "Task" in annotation_names(n.returns):
                    kinds["annotations"] += 1
                    lines.add((path, n.lineno))
            elif isinstance(n, ast.AnnAssign) and "Task" in annotation_names(n.annotation):
                kinds["annotations"] += 1
                lines.add((path, n.lineno))
            if isinstance(n, ast.Attribute) and n.attr in ORPHANS:
                recv = n.value.id if isinstance(n.value, ast.Name) else None
                reads[n.attr].append((path, n.lineno, recv))

    hit = {p for p, _ in lines}
    prod = {p for p in hit if not p.startswith("tests/")}
    print("Task type sites:", dict(kinds))
    print(f"distinct changed lines {len(lines)} in {len(hit)} files,"
          f" production {len(prod)}, test {len(hit) - len(prod)}")
    for f in ORPHANS:
        h = reads[f]
        p = [x for x in h if not x[0].startswith("tests/")]
        t = [x for x in h if x[2] and "task" in x[2].lower()]
        print(f"{f}: {len(h)} attribute reads, {len(p)} production,"
              f" {len(t)} on a receiver named *task*")
        for x in sorted(set(t)):
            print(f"    {x[0]}:{x[1]}  receiver {x[2]}")


if __name__ == "__main__":
    main()
```

## 3. The two record shapes

`Task` declares 7 fields; `TaskEntry` declares 23.

### `Task` — 7 fields

| Field | Annotation |
|---|---|
| `id` | `<class 'uuid.UUID'>` |
| `description` | `<class 'str'>` |
| `inputs` | `dict[str, typing.Any]` |
| `acceptance_checks` | `list[packages.core.models.AcceptanceCheck]` |
| `budget` | `<class 'packages.core.models.Budget'>` |
| `status` | `<enum 'RunState'>` |
| `output_artifact_ids` | `list[uuid.UUID]` |

### `TaskEntry` — 23 fields

| Field | Annotation |
|---|---|
| `task_id` | `str` |
| `source_heading_number` | `int` |
| `title` | `str` |
| `task_class` | `str` |
| `inputs` | `dict` |
| `files_hint` | `list` |
| `body` | `str` |
| `acceptance` | `str` |
| `status` | `str` |
| `run_id` | `str` |
| `final_status` | `str` |
| `safe_diff_files` | `list[str]` |
| `test_passed` | `bool \| None` |
| `reviewer_verdict` | `str` |
| `repair_rounds_used` | `int` |
| `repair_rounds_allowed` | `int` |
| `error` | `str` |
| `apply_manifest` | `ApplyManifest \| None` |
| `proof_summary` | `TaskProofSummary \| None` |
| `task_start_tree` | `str` |
| `task_start_tree_ref` | `str` |
| `task_start_recorded_at` | `str` |
| `task_attempt_state` | `str` |

SHARED NAMES — 2: `inputs`, `status`.

`Task`-ONLY NAMES — 5: `acceptance_checks`, `budget`, `description`, `id`, `output_artifact_ids`.

## 4. The `Task` type sites the flip must carry

| Kind | Count |
|---|---|
| constructions | 246 |
| imports | 142 |
| annotations | 40 |

DISTINCT CHANGED LINES 427 in 111 files — 15 production,
96 test. These are lines DECISION F275 D21's union does not contain,
because that union was computed over `Job` alone.

## 5. The orphan fields

The three `Task` fields with no counterpart of the same meaning on
`TaskEntry`. Every list below is COMPLETE and is never truncated.

### `budget`

45 attribute reads, 24 production, 0 on a receiver named `*task*`.

No read anywhere is on a receiver named `*task*`.

### `output_artifact_ids`

58 attribute reads, 15 production, 35 on a receiver named `*task*`.

The 35 reads on a `*task*` receiver, in full:

- `apps/cli/commands/job.py:538  receiver _task_obj_for_log`
- `apps/cli/commands/job.py:539  receiver _task_obj_for_log`
- `apps/cli/commands/job.py:577  receiver task_obj`
- `apps/cli/commands/job.py:578  receiver task_obj`
- `apps/cli/commands/job.py:604  receiver pi_task_obj`
- `apps/cli/commands/job.py:605  receiver pi_task_obj`
- `packages/orchestration/brain_detail.py:368  receiver task`
- `packages/orchestration/task_runner.py:248  receiver task`
- `packages/orchestration/task_runner.py:351  receiver task`
- `packages/orchestration/task_runner.py:357  receiver task`
- `packages/orchestration/task_runner.py:362  receiver task`
- `packages/orchestration/task_runner.py:460  receiver task_obj`
- `packages/orchestration/task_runner.py:465  receiver task_obj`
- `packages/orchestration/verifier.py:172  receiver task`
- `packages/orchestration/verifier.py:184  receiver task`
- `tests/test_cli_main.py:329  receiver task`
- `tests/test_cli_main.py:428  receiver task`
- `tests/test_cli_main.py:502  receiver reloaded_task`
- `tests/test_cli_main.py:560  receiver task`
- `tests/test_imports.py:55  receiver task`
- `tests/test_run_log_cli.py:304  receiver task`
- `tests/test_run_log_cli.py:444  receiver task`
- `tests/test_run_log_cli.py:564  receiver task`
- `tests/test_run_log_cli.py:652  receiver task`
- `tests/test_run_log_cli.py:768  receiver task`
- `tests/test_task_runner.py:225  receiver task`
- `tests/test_task_runner.py:226  receiver task`
- `tests/test_verifier.py:132  receiver task`
- `tests/test_verifier.py:155  receiver task`
- `tests/test_verifier.py:180  receiver task`
- `tests/test_verifier.py:209  receiver task`
- `tests/test_verifier.py:240  receiver task`
- `tests/test_verifier.py:271  receiver task`
- `tests/test_verifier.py:455  receiver task`
- `tests/test_verifier.py:510  receiver task`

### `acceptance_checks`

5 attribute reads, 3 production, 1 on a receiver named `*task*`.

The 1 read on a `*task*` receiver, in full:

- `tests/orchestration/test_flight_plan.py:113  receiver task`

## 6. Figures

`measured` is this file's own run; `reviewer` is the figure the round 40
block states as measured at the same base.

| Figure | measured | reviewer | verdict |
|---|---|---|---|
| `Task` fields | 7 | 7 | same |
| `TaskEntry` fields | 23 | 23 | same |
| shared names (count) | 2 | 2 | same |
| shared names (list) | inputs, status | inputs, status | same |
| `Task`-only names (count) | 5 | 5 | same |
| `Task`-only names (list) | acceptance_checks, budget, description, id, output_artifact_ids | acceptance_checks, budget, description, id, output_artifact_ids | same |
| `Task` type sites — constructions | 246 | 246 | same |
| `Task` type sites — imports | 142 | 142 | same |
| `Task` type sites — annotations | 40 | 40 | same |
| distinct changed lines | 427 | 427 | same |
| files | 111 | 111 | same |
| production files | 15 | 15 | same |
| test files | 96 | 96 | same |
| `budget` attribute reads | 45 | 45 | same |
| `budget` production | 24 | 24 | same |
| `budget` on a `*task*` receiver | 0 | 0 | same |
| `output_artifact_ids` attribute reads | 58 | 58 | same |
| `output_artifact_ids` production | 15 | 15 | same |
| `output_artifact_ids` on a `*task*` receiver | 35 | 35 | same |
| `acceptance_checks` attribute reads | 5 | 5 | same |
| `acceptance_checks` production | 3 | 3 | same |
| `acceptance_checks` on a `*task*` receiver | 1 | 1 | same |
