"""F016 — Flight-Plan task-granularity normalization.

v1 is a HEURISTIC on plan-intrinsic signals only: the token band the planner
guessed, the number of acceptance criteria, and token overlap between
``files_hint`` entries. Remedy has no per-task-class cost history yet, so
nothing here is data-driven and this module does not pretend to be (P6):
every band it assigns to a generated task is labeled in the transformation
record as heuristically reassigned.

Purity: this module performs no I/O — no filesystem, no network, no
environment reads. Thresholds arrive as a :class:`GranularityConfig` that the
caller builds from the resolved Remedy config.

Nothing is ever rewritten silently: every split, merge, abort, and
unsplittable task produces a :class:`Transformation` entry that plan
rendering shows to the human who approves the plan. The "aborted" kind
covers both refusals — a merge that dependency safety rejected, and a
whole normalization that failed revalidation — and its reason says which.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.schemas.models import FlightPlan, PlannedTask

#: Token bands in ascending size order (mirrors schemas.models.TokenBand).
_BAND_ORDER: tuple[str, ...] = ("S", "M", "L", "XL")

#: Band assigned to every child produced by a split — heuristic, not measured.
_SPLIT_CHILD_BAND = "M"

_TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class GranularityConfig:
    """Thresholds for normalization. Built by the caller from Remedy config.

    ``split_band`` is the band at (and above) which a task is split; the
    default "XL" therefore splits only XL tasks.
    """

    enabled: bool = True
    split_band: str = "XL"
    max_acceptance: int = 3
    merge_group_size: int = 3

    def __post_init__(self) -> None:
        if self.split_band not in _BAND_ORDER:
            raise ValueError(
                f"planning.granularity.split_band must be one of "
                f"{', '.join(_BAND_ORDER)} (got {self.split_band!r})")


@dataclass(frozen=True)
class Transformation:
    """One recorded change to the plan's task list."""

    #: "split" | "merge" | "aborted" | "unsplittable_flag"
    kind: str
    source_ids: list[str]
    result_ids: list[str]
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source_ids": list(self.source_ids),
            "result_ids": list(self.result_ids),
            "reason": self.reason,
        }


@dataclass(frozen=True)
class NormalizationResult:
    """A (possibly) normalized plan plus the record of what changed."""

    plan: FlightPlan
    transformations: list[Transformation]

    def as_dicts(self) -> list[dict[str, Any]]:
        return [t.as_dict() for t in self.transformations]


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------

def _band_rank(band: str) -> int:
    return _BAND_ORDER.index(band)


def _tokens(text: str) -> frozenset[str]:
    """Lowercase alphanumeric tokens of a free-text string."""
    return frozenset(t for t in _TOKEN_SPLIT_RE.split(text.lower()) if t)


def _path_tokens(path: str) -> frozenset[str]:
    """Tokens of a file path, with the final extension dropped.

    The extension is dropped so that two unrelated Python files do not look
    related merely because both end in ``.py``.
    """
    base = path.rsplit(".", 1)[0] if "." in path.rsplit("/", 1)[-1] else path
    return _tokens(base)


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

@dataclass
class _Cluster:
    """A group of acceptance criteria that point at the same files."""

    acceptance: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


def _split_triggers(task: PlannedTask, cfg: GranularityConfig) -> list[str]:
    """Return the human-readable reasons this task qualifies for splitting."""
    triggers: list[str] = []
    if _band_rank(task.est_tokens_band) >= _band_rank(cfg.split_band):
        triggers.append(
            f"band {task.est_tokens_band} at/above split band {cfg.split_band}")
    if len(task.acceptance) > cfg.max_acceptance:
        triggers.append(
            f"acceptance count {len(task.acceptance)} > {cfg.max_acceptance}")
    return triggers


def _cluster_acceptance(
    acceptance: list[str], files_hint: list[str],
) -> list[_Cluster]:
    """Greedily group acceptance items by shared files_hint entries.

    An acceptance item claims every files_hint entry whose path tokens
    overlap its own tokens, and then joins the first existing cluster that
    already claims one of those files. An item that matches no files_hint
    entry always starts its own cluster — no shared tokens means one child
    per acceptance item.

    Grouping keys are whole files, not raw tokens: two unrelated files under
    ``src/`` share the token "src" and would otherwise always look related.

    Cluster order is creation order, so the result is deterministic.
    """
    file_tokens = [(f, _path_tokens(f)) for f in files_hint]
    clusters: list[_Cluster] = []

    for item in acceptance:
        item_tokens = _tokens(item)
        matched = [f for f, ft in file_tokens if ft & item_tokens]

        target: _Cluster | None = None
        for cluster in clusters:
            if any(f in cluster.files for f in matched):
                target = cluster
                break

        if target is None:
            clusters.append(_Cluster(acceptance=[item], files=list(matched)))
            continue

        target.acceptance.append(item)
        for f in matched:
            if f not in target.files:
                target.files.append(f)

    return clusters


def _child_ids(parent_id: str, count: int, used: set[str]) -> list[str]:
    """Deterministic, collision-free ids for a parent's split children."""
    ids: list[str] = []
    for n in range(count):
        candidate = (
            f"{parent_id}{chr(ord('a') + n)}" if n < 26
            else f"{parent_id}s{n + 1}"
        )
        while candidate in used:
            candidate += "x"
        used.add(candidate)
        ids.append(candidate)
    return ids


def _split_task(
    task: PlannedTask, clusters: list[_Cluster], used_ids: set[str],
) -> list[PlannedTask]:
    """Build the chained children of a split task."""
    ids = _child_ids(task.id, len(clusters), used_ids)
    children: list[PlannedTask] = []
    for n, (cid, cluster) in enumerate(zip(ids, clusters, strict=True)):
        children.append(PlannedTask(
            id=cid,
            title=f"{task.title} ({n + 1}/{len(clusters)})",
            goal=task.goal,
            acceptance=list(cluster.acceptance),
            # First child inherits the parent's dependencies; the rest chain.
            depends_on=list(task.depends_on) if n == 0 else [ids[n - 1]],
            est_tokens_band=_SPLIT_CHILD_BAND,
            # A cluster that matched no files_hint entry keeps the parent's
            # full hint: an over-broad hint is less harmful than none.
            files_hint=list(cluster.files) if cluster.files
            else list(task.files_hint),
        ))
    return children


def split_one_task(
    task: PlannedTask, used_ids: set[str] | None = None,
) -> list[PlannedTask] | None:
    """Split ONE already-dispatched task into acceptance-clustered children,
    or None when it cannot usefully split.

    This is the public seam plan-time normalization never needed: F016's own
    entry point is :func:`normalize_plan`, which decides FOR ITSELF (via
    ``_split_triggers``) whether a task is oversized. A caller here has
    already made that call for its own reason — F112's ``cannot_fit``
    outcome, for instance — and wants exactly the clustering
    ``_apply_splits`` already proved out, without re-deciding the
    band/acceptance-count trigger. Returns None for the same "cannot
    usefully split" case ``_apply_splits`` flags as ``unsplittable_flag``:
    fewer than 2 acceptance clusters, where a split would produce one child
    carrying everything the parent already carried.
    """
    clusters = _cluster_acceptance(task.acceptance, task.files_hint)
    if len(clusters) < 2:
        return None
    ids = used_ids if used_ids is not None else {task.id}
    return _split_task(task, clusters, ids)


def _rewire(task: PlannedTask, mapping: dict[str, str]) -> PlannedTask:
    """Point dependencies at replacement ids, preserving order."""
    if not any(dep in mapping for dep in task.depends_on):
        return task
    deps: list[str] = []
    for dep in task.depends_on:
        new_dep = mapping.get(dep, dep)
        if new_dep not in deps:
            deps.append(new_dep)
    return task.model_copy(update={"depends_on": deps})


def _apply_splits(
    tasks: list[PlannedTask], cfg: GranularityConfig,
) -> tuple[list[PlannedTask], list[Transformation]]:
    """Split oversized tasks in plan order. Returns (tasks, records)."""
    used_ids = {t.id for t in tasks}
    out: list[PlannedTask] = []
    records: list[Transformation] = []
    replacements: dict[str, str] = {}

    for task in tasks:
        triggers = _split_triggers(task, cfg)
        if not triggers:
            out.append(task)
            continue

        trigger_text = " + ".join(triggers)
        clusters = _cluster_acceptance(task.acceptance, task.files_hint)
        if len(clusters) < 2:
            detail = (
                "single acceptance criterion"
                if len(task.acceptance) == 1
                else "acceptance criteria cluster into one files_hint group"
            )
            records.append(Transformation(
                kind="unsplittable_flag",
                source_ids=[task.id],
                result_ids=[task.id],
                reason=(
                    f"not split ({trigger_text}): {detail} — left oversized, "
                    f"review risk flagged for the approver"),
            ))
            out.append(task)
            continue

        children = _split_task(task, clusters, used_ids)
        out.extend(children)
        # Everything that depended on the parent now depends on the chain end.
        replacements[task.id] = children[-1].id
        records.append(Transformation(
            kind="split",
            source_ids=[task.id],
            result_ids=[c.id for c in children],
            reason=(
                f"split ({trigger_text}) into {len(children)} acceptance "
                f"clusters; children band {_SPLIT_CHILD_BAND} assigned "
                f"heuristically (no cost history — F016 v1)"),
        ))

    if replacements:
        out = [_rewire(t, replacements) for t in out]
    return out, records


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

#: Band a task must have to be a merge candidate.
_MERGE_BAND = "S"


def _is_merge_candidate(task: PlannedTask, cfg: GranularityConfig) -> bool:
    return (
        task.est_tokens_band == _MERGE_BAND
        and len(task.acceptance) <= cfg.max_acceptance
    )


def _task_file_tokens(task: PlannedTask) -> frozenset[str]:
    tokens: frozenset[str] = frozenset()
    for f in task.files_hint:
        tokens |= _path_tokens(f)
    return tokens


def _merge_runs(
    tasks: list[PlannedTask], cfg: GranularityConfig,
) -> list[list[int]]:
    """Maximal runs of consecutive merge candidates with overlapping files.

    Adjacency is decided pairwise: a candidate extends the current run only
    if it shares at least one files_hint token with its predecessor. A
    candidate without files_hint therefore never joins a run.
    """
    runs: list[list[int]] = []
    current: list[int] = []
    for i, task in enumerate(tasks):
        if not _is_merge_candidate(task, cfg):
            if len(current) > 1:
                runs.append(current)
            current = []
            continue
        if current and (
            _task_file_tokens(tasks[current[-1]]) & _task_file_tokens(task)
        ):
            current.append(i)
            continue
        if len(current) > 1:
            runs.append(current)
        current = [i]
    if len(current) > 1:
        runs.append(current)
    return runs


def _closure(
    start: set[str], edges: dict[str, list[str]], exclude: set[str],
) -> set[str]:
    """Transitive closure over an id->ids edge map, minus *exclude*."""
    seen: set[str] = set()
    stack = list(start)
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(edges.get(node, ()))
    return seen - exclude


def _merge_blocker(
    group: list[PlannedTask], tasks: list[PlannedTask],
) -> str | None:
    """Return why this group must not merge, or None if it is safe."""
    member_ids = {t.id for t in group}
    last_id = group[-1].id

    outside = [t for t in tasks if t.id not in member_ids]
    for task in outside:
        for dep in task.depends_on:
            if dep in member_ids and dep != last_id:
                return (
                    f"task {task.id} depends on {dep}, which is not the last "
                    f"member of the group")

    # Contracting the group into one node must not close a dependency loop:
    # an outside task that the group depends on must not also depend on the
    # group.
    dep_edges = {t.id: list(t.depends_on) for t in tasks}
    dependent_edges: dict[str, list[str]] = {t.id: [] for t in tasks}
    for task in tasks:
        for dep in task.depends_on:
            dependent_edges.setdefault(dep, []).append(task.id)

    group_deps = {
        dep for t in group for dep in t.depends_on if dep not in member_ids}
    group_dependents = {
        t.id for t in outside
        if any(dep in member_ids for dep in t.depends_on)}

    ancestors = _closure(group_deps, dep_edges, member_ids)
    descendants = _closure(group_dependents, dependent_edges, member_ids)
    overlap = sorted(ancestors & descendants)
    if overlap:
        return f"merging would create a dependency cycle via {overlap[0]}"
    return None


def _merge_group(group: list[PlannedTask]) -> PlannedTask:
    """Fuse a group of consecutive small tasks into one task."""
    member_ids = {t.id for t in group}
    deps: list[str] = []
    for task in group:
        for dep in task.depends_on:
            if dep not in member_ids and dep not in deps:
                deps.append(dep)
    files: list[str] = []
    for task in group:
        for f in task.files_hint:
            if f not in files:
                files.append(f)
    acceptance: list[str] = []
    for task in group:
        acceptance.extend(task.acceptance)
    rank = max(_band_rank(t.est_tokens_band) for t in group)
    return PlannedTask(
        id=group[0].id,
        title=" + ".join(t.title for t in group),
        goal="; ".join(t.goal for t in group),
        acceptance=acceptance,
        depends_on=deps,
        est_tokens_band=_BAND_ORDER[min(rank + 1, len(_BAND_ORDER) - 1)],
        files_hint=files,
    )


def _apply_merges(
    tasks: list[PlannedTask], cfg: GranularityConfig,
) -> tuple[list[PlannedTask], list[Transformation]]:
    """Merge runs of trivial neighbors. Returns (tasks, records)."""
    if cfg.merge_group_size < 2:
        return tasks, []

    # index -> merged task it belongs to; groups are chunked greedily
    # left-to-right, so a run longer than the cap leaves a remainder group.
    merged_at: dict[int, PlannedTask] = {}
    dropped: set[int] = set()
    records: list[Transformation] = []
    replacements: dict[str, str] = {}

    for run in _merge_runs(tasks, cfg):
        for start in range(0, len(run), cfg.merge_group_size):
            chunk = run[start:start + cfg.merge_group_size]
            if len(chunk) < 2:
                continue
            group = [tasks[i] for i in chunk]
            blocker = _merge_blocker(group, tasks)
            if blocker is not None:
                records.append(Transformation(
                    kind="aborted",
                    source_ids=[t.id for t in group],
                    result_ids=[t.id for t in group],
                    reason=f"merge skipped: {blocker}",
                ))
                continue
            merged = _merge_group(group)
            merged_at[chunk[0]] = merged
            dropped.update(chunk[1:])
            for t in group[1:]:
                replacements[t.id] = merged.id
            records.append(Transformation(
                kind="merge",
                source_ids=[t.id for t in group],
                result_ids=[merged.id],
                reason=(
                    f"merged {len(group)} consecutive {_MERGE_BAND}-band tasks "
                    f"sharing files_hint tokens; band "
                    f"{merged.est_tokens_band} assigned heuristically "
                    f"(no cost history — F016 v1)"),
            ))

    if not merged_at:
        return tasks, records

    out: list[PlannedTask] = []
    for i, task in enumerate(tasks):
        if i in dropped:
            continue
        out.append(merged_at.get(i, task))
    if replacements:
        out = [_rewire(t, replacements) for t in out]
    return out, records


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def normalize_plan(
    plan: FlightPlan, cfg: GranularityConfig,
) -> NormalizationResult:
    """Right-size a plan's tasks. Returns the plan to use plus the record.

    When normalization is disabled, or when the task list comes out
    unchanged, the ORIGINAL plan object is returned. A record entry can
    still be present in that case (a flagged unsplittable task, a merge that
    dependency safety refused).
    """
    if not cfg.enabled:
        return NormalizationResult(plan=plan, transformations=[])

    tasks, records = _apply_splits(list(plan.tasks), cfg)
    tasks, merge_records = _apply_merges(tasks, cfg)
    records += merge_records

    if tasks == list(plan.tasks):
        return NormalizationResult(plan=plan, transformations=records)

    data = plan.model_dump()
    data["tasks"] = [t.model_dump() for t in tasks]
    try:
        # Constructing the model IS the revalidation: FlightPlan's own
        # _validate_dag runs here. No validation logic is copied.
        new_plan = FlightPlan(**data)
    except Exception as exc:
        # Fail open to the plan the human is about to approve, never to a
        # broken one — and say so in the record.
        return NormalizationResult(
            plan=plan,
            transformations=[Transformation(
                kind="aborted",
                source_ids=[t.id for t in plan.tasks],
                result_ids=[t.id for t in plan.tasks],
                reason=(
                    f"normalization aborted, original plan kept: {exc}"),
            )],
        )
    return NormalizationResult(plan=new_plan, transformations=records)
