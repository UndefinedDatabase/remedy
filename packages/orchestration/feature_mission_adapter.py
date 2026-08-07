"""F080 T003 — compile a roadmap feature file into a PREPARED mission.

The adapter is the work-intake path of the self-build loop: `remedy plan
next` names a feature file, and this module turns that file into the
records the normal mission machinery already understands — nothing more.

    "How it fits" / "Context"  -> mission context input (JobIntake)
    "Task slicing"             -> plan structure seed (FlightPlan tasks
                                  and the milestone draft)
    "Acceptance"               -> DoD compiler input (acceptance lines)
    "Do not touch"             -> fences

PREPARES, NEVER EXECUTES — the guarantee this module exists to hold, and
the one an acceptance criterion pins: compiling starts no job, creates no
run, spawns no process, and writes nothing outside the data root. The
result carries ``approval_required=True`` and ``started=False`` and then
waits for the STANDARD human approval path; there is no code here that
starts anything, and that absence is the feature. Remedy deliberately
does not auto-approve a prepared mission — see docs/agents/ for why the
merge and the approval stay human acts (A4).

There is no second markdown parser here. The header grammar (title line,
bold dependency line, ids, tiers) belongs to
:mod:`packages.orchestration.roadmap_index`, and a file that breaks it
raises :class:`~packages.orchestration.roadmap_index.RoadmapGrammarError`
before any section is read — the adapter refuses to compile a broken
file. What this module adds is only the SECTION split of the body, which
is not part of that grammar.

Every seeded part records the heading and line it came from
(:attr:`PreparedMission.sources`), so a reader can trace any element of
the draft back to the sentence in the feature file that produced it.

Public API::

    prepare_feature_mission(feature, repo_root=None) -> PreparedMission
    write_prepared_mission(prepared, data_root=None) -> Path
    prepared_mission_path(feature_id, data_root=None) -> Path
    dod_compiler_input(prepared) -> tuple[dict, FlightPlan]
    read_feature_sections(text) -> list[FeatureSection]
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.mission_plan_schema import (
    MAX_MISSION_MILESTONES,
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
)
from packages.orchestration.roadmap_index import (
    RoadmapFeature,
    build_index,
    features_dir,
    resolve_repo_root,
)
from packages.orchestration.schemas.models import (
    FLIGHT_PLAN_SCHEMA_V,
    JOB_INTAKE_SCHEMA_V,
    FlightPlan,
    JobIntake,
    PlannedTask,
)

#: Which heading feeds which part of the draft. Matched case-insensitively
#: against the heading text up to the first "(" — the feature files carry
#: parenthesised qualifiers ("## How it fits (inspect current shape first)")
#: that say nothing about the section's role.
SECTION_ROLES: dict[str, tuple[str, ...]] = {
    "context": ("how it fits", "context", "goal & done", "goal and done", "built state"),
    "plan": ("task slicing",),
    "acceptance": ("acceptance", "acceptance & tests", "acceptance and tests"),
    "fences": ("do not touch", "non-goals", "out of scope", "risks / anti-goals"),
}

#: The goal sentence of the feature comes from this heading when present.
_GOAL_HEADINGS = ("goal & done", "goal and done")

#: A task-slicing id, in either shape the feature files use: the bullet
#: form ``- **T001** …`` and the prose form ``T001 … T002 …``.
_SLICE_BULLET_RE = re.compile(r"^- \*\*(T\d{3})\*\*\s*(.*)$")
_SLICE_INLINE_RE = re.compile(r"\b(T\d{3})\b")

#: Path-like tokens inside a do-not-touch line become deny globs: either a
#: path under a real top-level directory of this repo, or a bare filename
#: with a source extension. Deliberately narrow — "Estimation/calibration" is
#: prose, not a path, and a fence invented from prose would fence nothing.
#: Prose that names no path stays prose (``fence_notes``), reported as a fence
#: a human still has to translate rather than silently dropped.
_PATH_TOKEN_RE = re.compile(
    r"(?:docs|tests|apps|packages|scripts|schemas|\.agent|\.github)/[\w./*-]+"
    r"|\b[\w-]+\.(?:py|md|json|toml|ya?ml|sh|ts|tsx|sql)\b")

#: The "Suggested tests:" tail of a Do-not-touch section names where proof
#: SHOULD live — the opposite of a fence. Never harvested as a deny glob.
_SUGGESTED_TESTS_RE = re.compile(r"suggested tests?:", re.IGNORECASE)

#: Estimation is not this module's job; the bands are placeholders the human
#: approval step can correct, and they are labeled that way in the record.
_DEFAULT_BAND = "M"


@dataclass(frozen=True)
class FeatureSection:
    """One ``## …`` section of a feature file, with its 1-based heading line."""

    heading: str
    line: int
    body: str

    @property
    def key(self) -> str:
        """Heading text lowered and stripped of its parenthesised qualifier."""
        return self.heading.split("(")[0].strip().lower()

    def role(self) -> str:
        for role, headings in SECTION_ROLES.items():
            if self.key in headings:
                return role
        return ""


@dataclass(frozen=True)
class TaskSlice:
    """One ``T00n`` slice of the feature's Task-slicing section."""

    id: str
    text: str


@dataclass(frozen=True)
class PreparedMission:
    """A mission draft awaiting the standard human approval. Starts nothing."""

    feature_id: str
    tier: int
    title: str
    feature_file: str
    goal: str
    intake: JobIntake
    plan: FlightPlan
    mission_plan: MissionPlan
    fence_notes: tuple[str, ...]
    fence_globs: tuple[str, ...]
    dod_seed: tuple[str, ...]
    sources: dict[str, dict] = field(default_factory=dict)
    #: Both constants, and both asserted by the tests: a prepared mission is
    #: not an approved one, and preparing is not starting.
    approval_required: bool = True
    started: bool = False

    def as_dict(self) -> dict:
        return {
            "schema": "prepared_feature_mission/v1",
            "feature_id": self.feature_id,
            "tier": self.tier,
            "title": self.title,
            "feature_file": self.feature_file,
            "goal": self.goal,
            "intake": self.intake.model_dump(),
            "plan": self.plan.model_dump(),
            "mission_plan": self.mission_plan.model_dump(),
            "fence_notes": list(self.fence_notes),
            "fence_globs": list(self.fence_globs),
            "dod_seed": list(self.dod_seed),
            "sources": {k: dict(v) for k, v in self.sources.items()},
            "approval_required": self.approval_required,
            "started": self.started,
        }


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def read_feature_sections(text: str) -> list[FeatureSection]:
    """Split a feature file body into its ``## …`` sections, in file order."""
    sections: list[FeatureSection] = []
    heading = ""
    start = 0
    body: list[str] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if line.startswith("## "):
            if heading:
                sections.append(FeatureSection(heading, start, "\n".join(body).strip()))
            heading, start, body = line[3:].strip(), number, []
            continue
        if heading:
            body.append(line)
    if heading:
        sections.append(FeatureSection(heading, start, "\n".join(body).strip()))
    return sections


def _sections_for(sections: list[FeatureSection], role: str) -> list[FeatureSection]:
    return [s for s in sections if s.role() == role]


def _first_section(sections: list[FeatureSection], headings: tuple[str, ...]) -> FeatureSection | None:
    for section in sections:
        if section.key in headings:
            return section
    return None


def _bullet_lines(body: str) -> list[str]:
    """Bullet items of a section, each rejoined across its wrapped lines."""
    items: list[str] = []
    for line in body.split("\n"):
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif items and line.strip():
            items[-1] += " " + line.strip()
    return [i for i in items if i]


def _sentences(body: str) -> list[str]:
    flat = " ".join(part.strip() for part in body.split("\n") if part.strip())
    return [s.strip() for s in re.split(r"(?<=[.!?]) +", flat) if s.strip()]


# ---------------------------------------------------------------------------
# Section -> draft part
# ---------------------------------------------------------------------------


def parse_task_slices(body: str) -> list[TaskSlice]:
    """Read the Task-slicing section in either shape the feature files use."""
    slices: list[TaskSlice] = []
    for item in _bullet_lines(body):
        match = _SLICE_BULLET_RE.match(f"- {item}")
        if match is not None:
            slices.append(TaskSlice(match.group(1), match.group(2).strip()))
    if slices:
        return slices

    flat = " ".join(part.strip() for part in body.split("\n") if part.strip())
    marks = list(_SLICE_INLINE_RE.finditer(flat))
    for n, mark in enumerate(marks):
        end = marks[n + 1].start() if n + 1 < len(marks) else len(flat)
        text = flat[mark.end():end].strip(" .")
        slices.append(TaskSlice(mark.group(1), text))
    return slices


def acceptance_seed(sections: list[FeatureSection]) -> tuple[list[str], FeatureSection | None]:
    """Acceptance lines for the DoD compiler, with the section they came from.

    Falls back to the Goal & Done section's sentences when a feature file
    carries no acceptance section — recorded in ``sources`` as that fallback,
    never presented as an acceptance section that does not exist.
    """
    for section in _sections_for(sections, "acceptance"):
        lines = _bullet_lines(section.body) or _sentences(section.body)
        if lines:
            return lines, section
    goal_section = _first_section(sections, _GOAL_HEADINGS)
    if goal_section is not None:
        done = [s for s in _sentences(goal_section.body) if "DONE" in s or "done when" in s.lower()]
        if done:
            return done, goal_section
    return [], None


def fence_seed(sections: list[FeatureSection]) -> tuple[list[str], list[str], FeatureSection | None]:
    """Fences from the Do-not-touch family: prose notes and derived deny globs."""
    notes: list[str] = []
    globs: list[str] = []
    first: FeatureSection | None = None
    for section in _sections_for(sections, "fences"):
        first = first or section
        items = _bullet_lines(section.body) or _sentences(section.body)
        for item in items:
            if _SUGGESTED_TESTS_RE.search(item):
                # Names where proof should live, not what must not be touched.
                continue
            notes.append(item)
            globs.extend(_PATH_TOKEN_RE.findall(item))
    ordered_globs = list(dict.fromkeys(globs))
    return notes, ordered_globs, first


def context_seed(sections: list[FeatureSection]) -> tuple[list[str], list[FeatureSection]]:
    """Context refs for the intake: one ref per context-bearing section."""
    used = _sections_for(sections, "context")
    return [f"{s.heading} (line {s.line})" for s in used], used


# ---------------------------------------------------------------------------
# Prepare
# ---------------------------------------------------------------------------


def _feature_of(repo_root: Path, feature: str) -> RoadmapFeature:
    """Resolve a feature id or path against the (grammar-validated) index."""
    index = build_index(repo_root)
    wanted = feature.strip()
    match = re.search(r"F\d{3}", Path(wanted).name if "/" in wanted else wanted)
    if match is None:
        raise ValueError(f"cannot read a feature id out of {feature!r}")
    found = index.by_id(match.group(0))
    if found is None or not found.file:
        raise ValueError(f"{match.group(0)} has no feature file in {repo_root}")
    return found


def _milestone_goal(slice_: TaskSlice, feature: RoadmapFeature) -> str:
    """Outcome phrasing for a slice.

    The slice text is a task list by nature ("parser + tests"), which the
    milestone schema rightly refuses. Wrapping it in an outcome sentence keeps
    every real feature file compilable without editing what it says.
    """
    text = slice_.text.strip().rstrip(".")
    if not text:
        return f"{slice_.id} of {feature.id} is complete as specified in the feature file"
    return f"{slice_.id} of {feature.id} is complete: {text}"


def prepare_feature_mission(feature: str, repo_root: Path | str | None = None) -> PreparedMission:
    """Compile a feature detail file into a PREPARED mission draft.

    ``feature`` is a feature id (``F103``) or a path to its detail file.
    Raises RoadmapGrammarError if the roadmap markdown breaks its grammar —
    the adapter refuses to compile a file it cannot trust.

    Starts nothing: no job, no run, no process, no write. Persisting the draft
    is the separate, explicit :func:`write_prepared_mission` call.
    """
    root = resolve_repo_root(repo_root)
    found = _feature_of(root, feature)
    path = root / found.file
    if not path.is_file():  # pragma: no cover — build_index would have failed first
        path = features_dir(root) / Path(found.file).name
    sections = read_feature_sections(path.read_text(encoding="utf-8"))

    goal_section = _first_section(sections, _GOAL_HEADINGS)
    goal_text = " ".join(_sentences(goal_section.body)) if goal_section else found.title
    goal = f"{found.id} — {found.title}. {goal_text}".strip()

    context_refs, context_sections = context_seed(sections)
    acceptance, acceptance_section = acceptance_seed(sections)
    fence_notes, fence_globs, fence_section = fence_seed(sections)

    plan_section = _first_section(sections, ("task slicing",))
    slices = parse_task_slices(plan_section.body) if plan_section else []
    if not slices:
        slices = [TaskSlice("T001", found.title)]

    intake = JobIntake(
        schema_v=JOB_INTAKE_SCHEMA_V,
        goal=goal,
        context_refs=[f"{found.file}: {ref}" for ref in context_refs],
        constraints=list(fence_notes),
        acceptance_hints=list(acceptance),
        mission_candidate=True,
    )

    tasks = [
        PlannedTask(
            id=slice_.id,
            title=f"{found.id} {slice_.id}",
            goal=slice_.text or found.title,
            acceptance=list(acceptance) or [f"{found.file} acceptance section is met"],
            depends_on=[],
            est_tokens_band=_DEFAULT_BAND,
            files_hint=[found.file],
        )
        for slice_ in slices
    ]
    plan = FlightPlan(
        schema_v=FLIGHT_PLAN_SCHEMA_V,
        tasks=tasks,
        risks=[],
        fences={"deny": fence_globs} if fence_globs else None,
    )

    mission_plan = MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[
            Milestone(id=slice_.id, goal=_milestone_goal(slice_, found),
                      rationale=f"Task slicing of {found.file}")
            for slice_ in slices[:MAX_MISSION_MILESTONES]
        ],
        risks=[],
        assumptions=[
            f"Token bands are placeholders ({_DEFAULT_BAND}) — the feature file "
            f"estimates none; the approval step sets them.",
        ],
        compiled=False,
        origin="deterministic",
    )

    sources = {
        "goal": _source_of(goal_section),
        "context": {"headings": [s.heading for s in context_sections],
                    "lines": [s.line for s in context_sections]},
        "plan": _source_of(plan_section),
        "dod": _source_of(acceptance_section),
        "fences": _source_of(fence_section),
    }

    return PreparedMission(
        feature_id=found.id,
        tier=found.tier,
        title=found.title,
        feature_file=found.file,
        goal=goal,
        intake=intake,
        plan=plan,
        mission_plan=mission_plan,
        fence_notes=tuple(fence_notes),
        fence_globs=tuple(fence_globs),
        dod_seed=tuple(acceptance),
        sources=sources,
    )


def _source_of(section: FeatureSection | None) -> dict:
    if section is None:
        return {"heading": "", "line": 0}
    return {"heading": section.heading, "line": section.line}


# ---------------------------------------------------------------------------
# Persistence — under the data root, explicit, still not an execution
# ---------------------------------------------------------------------------


def prepared_mission_path(feature_id: str, data_root: Path | None = None) -> Path:
    """Where a prepared draft is written — under the data root, never the repo."""
    if data_root is None:
        from packages.orchestration.data_paths import resolve_data_root

        data_root = resolve_data_root()
    return Path(data_root) / "roadmap" / "missions" / f"{feature_id}.json"


def write_prepared_mission(prepared: PreparedMission, data_root: Path | None = None) -> Path:
    """Persist the draft as JSON. Writing a draft is not starting a mission."""
    path = prepared_mission_path(prepared.feature_id, data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(prepared.as_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def dod_compiler_input(prepared: PreparedMission) -> tuple[dict[str, Any], FlightPlan]:
    """The pair the F061 DoD compiler consumes: intake payload + flight plan.

    Handing this to ``compile_dod``/``deterministic_dod`` is the caller's
    explicit act; the adapter does not compile a DoD on its own, because that
    would put a provider call inside what is supposed to be a pure read.
    """
    return prepared.intake.model_dump(), prepared.plan
