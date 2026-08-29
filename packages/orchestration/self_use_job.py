"""F257 — carrying a curated self-use item onto the REAL job path.

:mod:`packages.orchestration.self_use_queue` is the read side of the self-use
track: it answers WHICH maintenance job Remedy runs on itself next.  This module
is the step that makes that answer matter — it renders a queue item to a job
file on disk and plans it through the job path Remedy already has,
:func:`packages.orchestration.pingpong_job.plan_job_from_file`, so the queue
stops being data nobody runs.

It is a SEPARATE module rather than a growth of the loader on purpose.  The
loader's read-only property is what DECISION F257 D2 turns on, and a module that
writes files is not the place to keep proving that a module writes none.

Public API::

    SelfUseJobError: asked to render or plan with no pending queue item, asked
        to render an id that is not a single file name, or asked to write
        outside the destination directory
    write_self_use_job_file(entry, dest_dir) -> Path
    plan_self_use_item(entry, dest_dir, repo_path=".") -> tuple[Path, object]
    plan_next_self_use_item(dest_dir, repo_path=".", queue_path=None)
        -> tuple[SelfUseQueueEntry, Path, object]

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT RUN A JOB HERE.  Planning is the read-only
    half — it parses text into a :class:`JobPlan` and touches no target repo —
    and running is ``do job-run``, which carries its own approval gate.  Keeping
    the two apart is what lets this module be called freely.
  * Remedy deliberately does not PROMOTE a job here.  Promotion stays behind the
    ``--approve`` barrier in :mod:`packages.orchestration.job_promote`, which
    never auto-promotes; a self-use job earns no shortcut through it for being
    Remedy's own maintenance.
  * REMEDY DELIBERATELY DOES NOT MARK A QUEUE ITEM CONSUMED.  This module owns
    no queue writer, exactly as the loader owns none.  Consumption is an edit
    the CLOSURE ROUND makes, which DECISION F257 D2 rules, because a run that
    can check itself off is not a gate.
  * Remedy deliberately resolves no data root here.  Every destination is the
    CALLER'S, which keeps this module out of
    ``tests/test_data_paths.py::TestSingleReaderInvariant``'s way and lets every
    test point it at ``tmp_path``.
"""

from __future__ import annotations

from pathlib import Path

from packages.orchestration.pingpong_job import plan_job_from_file
from packages.orchestration.self_use_queue import SelfUseQueueEntry, next_self_use_item


class SelfUseJobError(RuntimeError):
    """Asked to render or plan a self-use job the module refuses to carry out.

    Three refusals wear this one error: the queue has no pending item, an
    ``entry.id`` that is not a single file name, and a destination that would
    fall outside the caller's ``dest_dir``.

    Raised rather than answered with ``None``: "the track is exhausted" is a
    state a caller must handle deliberately — a human has to curate more items —
    and a ``None`` flowing onward would surface as a failure somewhere later and
    less obvious.
    """


# THE RENDERED BYTES ARE THE CURATED BYTES: no templating, no substitution, no
# reformatting.  The queue stores job-file TEXT precisely so the thing that runs
# is the thing an operator curated and a reviewer read; a renderer that edited it
# on the way out would make the reviewed text and the executed text two
# different artifacts, and only one of them would ever have been looked at.
def write_self_use_job_file(entry: SelfUseQueueEntry, dest_dir: Path) -> Path:
    """Write ``entry.job_markdown`` verbatim to ``dest_dir/<id>.md`` and answer the path.

    ``dest_dir`` is created when absent.  The destination is the CALLER'S and is
    never derived here — this module resolves no data root.

    Raises:
        SelfUseJobError: ``entry.id`` is not a single path component, or it
            would place the file outside ``dest_dir``.  The message names the
            offending id.
    """
    dest_dir = Path(dest_dir)
    # R-0735 — THE ID MUST BE ONE PATH COMPONENT, AND THIS IS CHECKED FIRST.
    # ``Path.resolve()`` NORMALISES ``..`` away, so the containment check below
    # cannot see an id like ``x/../SU-001``: its resolved parent genuinely is
    # ``dest_dir``, the guard passes, and ``write_text`` then leaks a raw
    # ``FileNotFoundError`` because ``dest_dir/x`` was never created.  Comparing
    # ``Path(id).name`` with the id itself refuses that, and with it ``sub/dir``,
    # ``../../escaped`` and an absolute id.  ``.`` fails it too, because
    # ``Path(".").name`` is the empty string — but ``Path("..").name`` is ``".."``
    # and NOT empty, measured here, so the one directory id the name comparison
    # cannot catch is named outright beside it.
    #
    # THE TWO CHECKS ANSWER DIFFERENT QUESTIONS AND NEITHER IS REDUNDANT: this
    # one asks "is this id one file name?", the resolved comparison below asks
    # "does that file land inside the caller's directory?".  A name comparison
    # cannot see a destination reached through a symlink, and a resolved
    # comparison cannot see a component that normalises itself away.
    if Path(entry.id).name != entry.id or entry.id in (".", ".."):
        raise SelfUseJobError(
            f"self-use item id {entry.id!r} is not a single file name: "
            f"a job file is named <id>.md inside the destination directory"
        )
    candidate = dest_dir / f"{entry.id}.md"
    # CONTAINMENT IS CHECKED ON RESOLVED PATHS, NOT ON THE CHARACTERS OF THE ID.
    # Comparing the candidate's resolved parent with the resolved ``dest_dir``
    # also catches an ABSOLUTE id and a symlinked escape, which a character
    # filter would not; and the character route is not available anyway, because
    # ``tests/test_path_utils.py::TestSingleImplementationInvariant`` reserves
    # path-sanitising regexes and length constants to
    # :mod:`packages.orchestration.path_utils`.
    #
    # IT REFUSES RATHER THAN SANITISES.  The contract is that the file is named
    # ``<id>.md``; a sanitiser would quietly make the written name differ from
    # the id the caller asked for — the same silent divergence the verbatim-bytes
    # rule above exists to prevent — and raising is what this module already does
    # for its other failures.
    #
    # WORTH A GUARD EVEN THOUGH THE LOADER VALIDATES: ``load_self_use_queue``
    # refuses any id but ``^SU-\d{3}$``, so the SHIPPED path cannot reach this.
    # But ``write_self_use_job_file`` and :func:`plan_self_use_item` are PUBLIC
    # exports taking a caller-built :class:`SelfUseQueueEntry`, and that frozen
    # dataclass validates nothing — the guard is what makes the public function
    # safe on its own terms rather than only as far as today's callers behave.
    if candidate.resolve().parent != dest_dir.resolve():
        raise SelfUseJobError(
            f"self-use item id {entry.id!r} would write outside {dest_dir}: "
            f"a job file is named <id>.md inside the destination directory"
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    candidate.write_text(entry.job_markdown, encoding="utf-8")
    return candidate


# The seam where the curated queue meets the job path Remedy already has: one
# render, then the EXISTING parser, so the queue never grows a second format.
def plan_self_use_item(
    entry: SelfUseQueueEntry,
    dest_dir: Path,
    repo_path: str = ".",
) -> tuple[Path, object]:
    """Render one queue item and plan it. Answers ``(job_file_path, JobPlan)``.

    Plans only.  Running the job is ``do job-run`` behind the normal approval
    gate, and this function deliberately stops short of it.
    """
    path = write_self_use_job_file(entry, dest_dir)
    return path, plan_job_from_file(str(path), repo_path)


# The whole track in one call — the entry point a caller wants when the question
# is "what does Remedy do to itself next?" rather than "plan this exact item".
def plan_next_self_use_item(
    dest_dir: Path,
    repo_path: str = ".",
    queue_path: Path | None = None,
) -> tuple[SelfUseQueueEntry, Path, object]:
    """Plan the queue's next PENDING item. Answers ``(entry, job_file_path, JobPlan)``.

    Raises:
        SelfUseJobError: the queue holds no pending item — the track is
            exhausted and a human must curate more.  The message names the
            queue path, because "which queue?" is the first question a reader
            has once an operator has pointed the loader elsewhere.
    """
    entry = next_self_use_item(queue_path)
    if entry is None:
        raise SelfUseJobError(
            f"no pending self-use item in {queue_path or 'the shipped queue'}: "
            f"the track is exhausted and needs curation"
        )
    path, plan = plan_self_use_item(entry, dest_dir, repo_path)
    return entry, path, plan
