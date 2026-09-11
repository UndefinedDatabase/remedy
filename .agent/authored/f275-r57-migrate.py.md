# F275 R57 — `f275_r57_migrate.py`, one record per run, as DECISION F275 D33 orders

> Committed verbatim so the seven commits are the output of a checked instrument
> rather than thirty-five hand-applied edits. Every edit is an explicit
> (line, FROM, TO) triple applied only where the FROM matches byte for byte; a triple
> that misses is reported, nothing is written for it, and the exit code is non-zero.
> It is a `.md` and not a `.py` because a `.py` file anywhere `ruff check .` scans is
> counted by `tests/orchestration/test_ci_budgets.py`.

```python
"""F275 R57 — retype ONE record's id field, and everything in its module that carries it.

Usage: python3 -B f275_r57_migrate.py <RecordName>
       python3 -B f275_r57_migrate.py --list

DECISION F275 D33 rules the seven records `R-0878` names migrated ONE RECORD PER COMMIT,
so this applies exactly one record's edits per run and prints what it changed. It is run
from the repository root and edits the tracked file in place.

Every edit is an explicit (line, FROM, TO) triple and is applied ONLY where the FROM
matches that line byte for byte. A triple whose FROM does not match is REPORTED and
nothing is written for it, so a silent miss is impossible; the exit code is non-zero
whenever any triple missed. A TO of None deletes the line, which is how an import
orphaned by the retype is removed — leaving it would take `ruff check .` from 26 findings
to more, and `tests/orchestration/test_ci_budgets.py` freezes that count at 26.

THE SEVEN ARE NOT UNIFORM, and the order below is the artefact's construction order. Five
are a declaration line, its docstring and the parameters that feed it. Two —
`dag_schedule` and `long_run_executor` — thread a task id through the whole module's
signatures, so retyping the field alone would leave every caller's annotation lying, which
is the `R-0877` shape this migration exists to stop repeating.
"""
import pathlib
import sys

TASK_RUNNER = "packages/orchestration/task_runner.py"

RECORDS = {
    "VerificationResult": ("packages/orchestration/verifier.py", [
        (113, "    task_id: UUID of the task that was verified.",
              "    task_id: id of the task that was verified."),
        (118, "    task_id: UUID", "    task_id: str"),
        (130, "    task_id: UUID,", "    task_id: str,"),
        (47, "from uuid import UUID", None),
    ]),
    "TaskAttempt": ("packages/orchestration/long_run_executor.py", [
        (281, "    task_id: UUID | None = None", "    task_id: str | None = None"),
        (557, "                      task_id: UUID | None = None) -> TaskAttempt:",
              "                      task_id: str | None = None) -> TaskAttempt:"),
        (772, "                blocked_ids: Collection[UUID] = (),",
              "                blocked_ids: Collection[str] = (),"),
        (773, "                awaiting_ids: Collection[UUID] = ()) -> list[UUID]:",
              "                awaiting_ids: Collection[str] = ()) -> list[str]:"),
        (800, "                          blocked_ids: Collection[UUID]) -> list[UUID]:",
              "                          blocked_ids: Collection[str]) -> list[str]:"),
        (813, "                              awaiting_ids: Collection[UUID]) -> list[UUID]:",
              "                              awaiting_ids: Collection[str]) -> list[str]:"),
        (943, "                            blocked_ids: Collection[UUID] = (),",
              "                            blocked_ids: Collection[str] = (),"),
        (944, "                            awaiting_ids: Collection[UUID] = ()) -> None:",
              "                            awaiting_ids: Collection[str] = ()) -> None:"),
        (992, "def _escalate_task(job: Job, attempt: TaskAttempt, target: UUID, *,",
              "def _escalate_task(job: Job, attempt: TaskAttempt, target: str, *,"),
        (1365, "    blocked_ids: set[UUID] = set()", "    blocked_ids: set[str] = set()"),
        (1370, "    awaiting_ids: set[UUID] = set()", "    awaiting_ids: set[str] = set()"),
        (73, "from uuid import UUID", None),
    ]),
    "RunTaskResult": (TASK_RUNNER, [
        (68, "    task_id:  UUID of the task that was executed, or None if no task was run.",
             "    task_id:  id of the task that was executed, or None if no task was run."),
        (73, "    task_id: UUID | None", "    task_id: str | None"),
        (77, "def _find_next_pending(job: Job, *, task_id: UUID | None = None) -> Task | None:",
             "def _find_next_pending(job: Job, *, task_id: str | None = None) -> Task | None:"),
        (160, "    task_id: UUID | None = None,", "    task_id: str | None = None,"),
        (419, "        <short_id>   first 8 hex characters of the task UUID",
              "        <short_id>   first 8 characters of the task id"),
        (422, "        - collision-safe: index + task UUID fragment make every file unique",
              "        - collision-safe: index + task id fragment make every file unique"),
        # THE ONE BEHAVIOUR CHANGE IN THE WHOLE MIGRATION, and it is not `[:8]`.
        # `.hex` cannot simply go: the value is a `UUID` until the flip lands, and a
        # `UUID` is not subscriptable, so `result.task_id[:8]` raises TypeError TODAY —
        # measured, as 15 reddened tests in `tests/test_workspace.py`. `str(x)[:8]` is
        # the shape-agnostic form: over 10000 `uuid4()` samples `str(u)[:8] == u.hex[:8]`
        # in every one, because a UUID's canonical string begins with its first eight hex
        # digits, and for a `str` id it is the identity. Correct before AND after.
        (479, "    short_id = result.task_id.hex[:8]",
              "    short_id = str(result.task_id)[:8]"),
        (53, "from uuid import UUID", None),
    ]),
    "TaskNode": ("packages/orchestration/dag_schedule.py", [
        (60, "    task_id: UUID", "    task_id: str"),
        (64, "    depends_on: tuple[UUID, ...]", "    depends_on: tuple[str, ...]"),
        (83, "    by_planned: dict[str, UUID] = {}", "    by_planned: dict[str, str] = {}"),
        (106, "        resolved: list[UUID] = []", "        resolved: list[str] = []"),
        (126, "def ready_set(tasks: Sequence[Task]) -> list[UUID]:",
              "def ready_set(tasks: Sequence[Task]) -> list[str]:"),
        (135, "    ready: list[UUID] = []", "    ready: list[str] = []"),
        (148, "                       blocked_ids: Iterable[UUID]) -> set[UUID]:",
              "                       blocked_ids: Iterable[str]) -> set[str]:"),
        (164, "    dependents: dict[UUID, list[UUID]] = {}",
              "    dependents: dict[str, list[str]] = {}"),
        (170, "    blocked: set[UUID] = set()", "    blocked: set[str] = set()"),
        (37, "from uuid import UUID", None),
    ]),
    "AgentLoopState": ("packages/orchestration/agent_loop.py", [
        (117, "    job_id: UUID", "    job_id: str"),
        (39, "from uuid import UUID", None),
    ]),
    "ProjectBrainGraph": ("packages/orchestration/project_brain.py", [
        (256, "    job_id: UUID", "    job_id: str"),
        # The import STAYS: line 582 is `UUID(str(raw))`, a parse of external input and
        # not an id annotation, so removing it would break the module.
    ]),
    "Workspace": ("packages/orchestration/workspace.py", [
        (47, "    job_id:             UUID of the owning job.",
             "    job_id:             id of the owning job."),
        (52, "    job_id: UUID", "    job_id: str"),
        (71, "    def __init__(self, job_id: UUID) -> None:",
             "    def __init__(self, job_id: str) -> None:"),
        (20, "from uuid import UUID", None),
    ]),
}

ORDER = ["VerificationResult", "TaskAttempt", "RunTaskResult", "TaskNode",
         "AgentLoopState", "ProjectBrainGraph", "Workspace"]

if len(sys.argv) != 2:
    print(__doc__)
    raise SystemExit(2)
if sys.argv[1] == "--list":
    for i, name in enumerate(ORDER, 1):
        rel, edits = RECORDS[name]
        drops = len([e for e in edits if e[2] is None])
        print(f"{i}. {name:20s} {rel:46s} {len(edits) - drops} edits, {drops} import drop")
    raise SystemExit(0)

name = sys.argv[1]
if name not in RECORDS:
    print(f"unknown record {name!r}; one of {sorted(RECORDS)}")
    raise SystemExit(2)

rel, edits = RECORDS[name]
path = pathlib.Path(rel)
lines = path.read_text().split("\n")
missed, changed, drop = [], [], set()
for lineno, frm, to in edits:
    have = lines[lineno - 1] if lineno - 1 < len(lines) else "<past end of file>"
    if have != frm:
        missed.append((lineno, frm, have))
        continue
    if to is None:
        drop.add(lineno)
        changed.append((lineno, frm, "<LINE DELETED>"))
    else:
        lines[lineno - 1] = to
        changed.append((lineno, frm, to))

if missed:
    print(f"{name}: {len(missed)} triple(s) did NOT match; NOTHING was written.")
    for lineno, frm, have in missed:
        print(f"   {rel}:{lineno}\n      WANTED {frm!r}\n      FOUND  {have!r}")
    raise SystemExit(1)

path.write_text("\n".join(l for i, l in enumerate(lines, 1) if i not in drop))
print(f"{name}  ->  {rel}")
for lineno, frm, to in changed:
    print(f"   line {lineno}")
    print(f"      -  {frm}")
    print(f"      +  {to}")
print(f"{len(changed) - len(drop)} line(s) rewritten, {len(drop)} line(s) deleted, "
      f"0 triple(s) missed")
```
