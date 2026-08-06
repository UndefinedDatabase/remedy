"""Machine-readable mirror of the human roadmap (F080 T001/T002).

ONE-WAY MIRROR — the rule this module exists to keep. It READS
``docs/roadmap/ROADMAP.md``, ``docs/roadmap/features/*.md`` and
``docs/roadmap/STATUS.md`` and writes a generated JSON index under the
Remedy data root (``REMEDY_DATA_DIR``). It NEVER writes back into the
markdown, never checks a checkbox, and the generated index is never
committed: it is rebuilt on every read path, so there is no staleness
state to manage and it cannot drift into a second source of truth.
STATUS.md stays human-owned (ROADMAP.md Part A rule A4) — Remedy reads
it and may PROPOSE a diff, the merge is a human act.

Grammar is the only hard failure: a feature file or STATUS line that
breaks the documented conventions raises :class:`RoadmapGrammarError`
with ``<file>:<line>: <what>`` violations, so fixing is mechanical.
Consistency findings (STATUS entry without a file, file absent from
STATUS, dependency reference to an unknown id) are REPORTED, never
fatal.

Public API::

    build_index(repo_root=None) -> RoadmapIndex
    build_and_write_index(repo_root=None) -> tuple[RoadmapIndex, Path]
    check_consistency(files, entries) -> list[dict]
    roadmap_index_path(data_root=None) -> Path
    active_feature(index) -> RoadmapFeature | None
    next_feature(index) -> RoadmapFeature | None
    proposed_feature(index) -> tuple[RoadmapFeature | None, str]
    RoadmapGrammarError, GrammarViolation, RoadmapFeature, RoadmapIndex
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------------------

#: STATUS.md checkbox glyphs (ROADMAP.md Part C) mapped to index states.
STATUS_GLYPHS: dict[str, str] = {
    " ": "todo",
    "~": "in_progress",
    "x": "done",
    "!": "blocked",
}

#: Feature-file title line: ``# T1_F080 — Machine-readable roadmap mirror``.
_TITLE_RE = re.compile(r"^# T(\d{1,2})_F(\d{3}) — (\S.*)$")
#: Feature-file name: ``T1_F080.md``.
_FILENAME_RE = re.compile(r"^T(\d{1,2})_F(\d{3})\.md$")
#: The bold dependency line opens with the tier: ``**Tier 1 · Depends on: …**``.
_DEPENDENCY_OPEN_RE = re.compile(r"^\*\*Tier (\d{1,2})\b")
#: STATUS.md feature line: ``- [x] F001 — Adaptive provider timeouts (PR #123)``.
_STATUS_LINE_RE = re.compile(r"^- \[(.)\] F(\d{3}) — (\S.*)$")
#: STATUS.md tier heading: ``## Tier 1 — Self-Build Bootstrap``.
_TIER_HEADING_RE = re.compile(r"^## Tier (\d{1,2}) — (\S.*)$")
#: ROADMAP.md Part G milestone row: ``| M2 | "It builds itself" | Tier 1 | … |``.
_MILESTONE_ROW_RE = re.compile(r"^\|\s*(M\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$")
#: Any feature reference inside prose (``F070``, ``F031/F032``).
_FEATURE_REF_RE = re.compile(r"\bF(\d{3})\b")
#: How many lines the bold dependency block may wrap over before it counts
#: as unterminated. Five is the widest real block (T12_F253); 12 is slack.
_DEPENDENCY_MAX_LINES = 12


class RoadmapGrammarError(Exception):
    """Raised when the roadmap markdown breaks its documented grammar.

    Carries every violation found in one pass so a fix round is mechanical
    instead of one-error-at-a-time.
    """

    def __init__(self, violations: list[GrammarViolation]) -> None:
        self.violations = list(violations)
        body = "\n".join(str(v) for v in self.violations)
        super().__init__(f"{len(self.violations)} roadmap grammar violation(s):\n{body}")


@dataclass(frozen=True)
class GrammarViolation:
    """One grammar violation, rendered as ``<file>:<line>: <what>``."""

    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}"

    def as_dict(self) -> dict:
        return {"file": self.file, "line": self.line, "message": self.message}


@dataclass(frozen=True)
class RoadmapFeature:
    """One feature as the mirror sees it. ``status`` comes from STATUS.md."""

    id: str
    tier: int
    title: str
    depends_on: tuple[str, ...]
    blocks: tuple[str, ...]
    status: str
    file: str
    status_line: int = 0
    status_note: str = ""
    milestone: str = ""

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "tier": self.tier,
            "title": self.title,
            "depends_on": list(self.depends_on),
            "blocks": list(self.blocks),
            "status": self.status,
            "file": self.file,
            "status_line": self.status_line,
            "status_note": self.status_note,
            "milestone": self.milestone,
        }


@dataclass(frozen=True)
class RoadmapIndex:
    """The generated mirror: features, milestones, STATUS order, findings."""

    features: tuple[RoadmapFeature, ...]
    milestones: tuple[dict, ...]
    order: tuple[str, ...]
    inconsistencies: tuple[dict, ...] = ()
    repo_root: str = ""

    def by_id(self, feature_id: str) -> RoadmapFeature | None:
        for feature in self.features:
            if feature.id == feature_id:
                return feature
        return None

    def ordered_features(self) -> list[RoadmapFeature]:
        """Features in STATUS execution order; unscheduled ones last."""
        index = {fid: n for n, fid in enumerate(self.order)}
        return sorted(self.features, key=lambda f: (index.get(f.id, len(index)), f.id))

    def as_dict(self) -> dict:
        return {
            "schema": "roadmap_index/v1",
            "repo_root": self.repo_root,
            "features": [f.as_dict() for f in self.features],
            "milestones": [dict(m) for m in self.milestones],
            "order": list(self.order),
            "inconsistencies": [dict(c) for c in self.inconsistencies],
        }


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------


def resolve_repo_root(repo_root: Path | str | None = None) -> Path:
    """Repo root to mirror. Default: the repository this file lives in."""
    if repo_root is not None:
        return Path(repo_root)
    return Path(__file__).resolve().parents[2]


def roadmap_markdown_path(repo_root: Path) -> Path | None:
    """Locate ROADMAP.md. ``docs/roadmap/`` is this repo's actual home."""
    for candidate in (repo_root / "docs" / "roadmap" / "ROADMAP.md", repo_root / "docs" / "ROADMAP.md"):
        if candidate.is_file():
            return candidate
    return None


def status_markdown_path(repo_root: Path) -> Path:
    return repo_root / "docs" / "roadmap" / "STATUS.md"


def features_dir(repo_root: Path) -> Path:
    return repo_root / "docs" / "roadmap" / "features"


def roadmap_index_path(data_root: Path | None = None) -> Path:
    """Where the generated index is written — under the data root, never the repo."""
    if data_root is None:
        from packages.orchestration.data_paths import resolve_data_root

        data_root = resolve_data_root()
    return Path(data_root) / "roadmap" / "index.json"


# ---------------------------------------------------------------------------
# Feature files
# ---------------------------------------------------------------------------


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _split_dependency_segments(block: str) -> list[str]:
    """Split the bold dependency line into its ``·``-separated segments."""
    body = block.strip()
    if body.startswith("**"):
        body = body[2:]
    if body.endswith("**"):
        body = body[:-2]
    return [seg.strip() for seg in body.split("·")]


def _refs_after(segments: list[str], label: str) -> tuple[str, ...]:
    """Feature ids referenced in the segment introduced by ``label``."""
    ids: list[str] = []
    for segment in segments:
        if not segment.startswith(label):
            continue
        for ref in _FEATURE_REF_RE.findall(segment):
            fid = f"F{ref}"
            if fid not in ids:
                ids.append(fid)
    return tuple(ids)


def _parse_feature_file(path: Path, repo_root: Path) -> tuple[dict | None, list[GrammarViolation]]:
    """Parse one feature detail file. Returns (parsed, violations)."""
    rel = _relative(path, repo_root)
    violations: list[GrammarViolation] = []
    lines = path.read_text(encoding="utf-8").split("\n")

    name_match = _FILENAME_RE.match(path.name)
    if name_match is None:
        violations.append(GrammarViolation(rel, 1, f"feature file name must be T<tier>_F<id>.md, got {path.name!r}"))

    title_match = _TITLE_RE.match(lines[0]) if lines else None
    if title_match is None:
        violations.append(GrammarViolation(
            rel, 1, "missing title line: expected '# T<tier>_F<id> — <title>'"))
        return None, violations

    tier = int(title_match.group(1))
    feature_id = f"F{title_match.group(2)}"
    title = title_match.group(3).strip()

    if name_match is not None and (int(name_match.group(1)), f"F{name_match.group(2)}") != (tier, feature_id):
        violations.append(GrammarViolation(
            rel, 1, f"title line {feature_id} (tier {tier}) does not match file name {path.name!r}"))

    if len(lines) < 2 or _DEPENDENCY_OPEN_RE.match(lines[1]) is None:
        violations.append(GrammarViolation(
            rel, 2, "malformed dependency line: expected '**Tier <n> · Depends on: … · Blocks/used by: …**'"))
        return None, violations

    header_tier = int(_DEPENDENCY_OPEN_RE.match(lines[1]).group(1))
    if header_tier != tier:
        violations.append(GrammarViolation(
            rel, 2, f"dependency line says tier {header_tier}, title line says tier {tier}"))

    block = lines[1]
    last = 1
    while not block.rstrip().endswith("**"):
        last += 1
        if last >= len(lines) or last - 1 >= _DEPENDENCY_MAX_LINES:
            violations.append(GrammarViolation(
                rel, 2, "malformed dependency line: bold block is not closed with '**'"))
            return None, violations
        block += " " + lines[last]

    segments = _split_dependency_segments(block)
    if not any(s.startswith("Depends on:") or s.startswith("Blocks/used by:") for s in segments):
        violations.append(GrammarViolation(
            rel, 2, "malformed dependency line: no 'Depends on:' or 'Blocks/used by:' segment"))
        return None, violations

    parsed = {
        "id": feature_id,
        "tier": tier,
        "title": title,
        "depends_on": _refs_after(segments, "Depends on:"),
        "blocks": _refs_after(segments, "Blocks/used by:"),
        "file": rel,
    }
    return parsed, violations


def _parse_feature_files(repo_root: Path) -> tuple[dict[str, dict], list[GrammarViolation]]:
    """Parse every feature detail file. Duplicate ids are a hard grammar error."""
    parsed: dict[str, dict] = {}
    violations: list[GrammarViolation] = []
    directory = features_dir(repo_root)
    if not directory.is_dir():
        return parsed, violations
    for path in sorted(directory.glob("*.md")):
        feature, file_violations = _parse_feature_file(path, repo_root)
        violations.extend(file_violations)
        if feature is None:
            continue
        seen = parsed.get(feature["id"])
        if seen is not None:
            violations.append(GrammarViolation(
                feature["file"], 1,
                f"duplicate feature id {feature['id']} — already defined in {seen['file']}"))
            continue
        parsed[feature["id"]] = feature
    return parsed, violations


# ---------------------------------------------------------------------------
# STATUS.md
# ---------------------------------------------------------------------------


def _parse_status(repo_root: Path) -> tuple[list[dict], list[GrammarViolation]]:
    """Parse STATUS.md in file order — the execution-order truth (Rule A5)."""
    path = status_markdown_path(repo_root)
    rel = _relative(path, repo_root)
    entries: list[dict] = []
    violations: list[GrammarViolation] = []
    if not path.is_file():
        return entries, violations

    in_fence = False
    tier = 0
    seen: dict[str, int] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = _TIER_HEADING_RE.match(line)
        if heading is not None:
            tier = int(heading.group(1))
            continue
        if not line.startswith("- "):
            continue
        match = _STATUS_LINE_RE.match(line)
        if match is None:
            violations.append(GrammarViolation(
                rel, number, "status line without checkbox grammar: expected '- [<glyph>] F<id> — <title>'"))
            continue
        glyph, digits, rest = match.group(1), match.group(2), match.group(3)
        if glyph not in STATUS_GLYPHS:
            violations.append(GrammarViolation(
                rel, number,
                f"unknown status glyph {glyph!r} — expected one of {sorted(STATUS_GLYPHS)}"))
            continue
        feature_id = f"F{digits}"
        if feature_id in seen:
            violations.append(GrammarViolation(
                rel, number, f"duplicate feature id {feature_id} — already listed on line {seen[feature_id]}"))
            continue
        seen[feature_id] = number
        title, _, note = rest.partition(" (")
        entries.append({
            "id": feature_id,
            "tier": tier,
            "title": title.strip(),
            "status": STATUS_GLYPHS[glyph],
            "line": number,
            "note": note.rstrip(")").strip(),
        })
    return entries, violations


# ---------------------------------------------------------------------------
# ROADMAP.md milestones
# ---------------------------------------------------------------------------


def _parse_milestones(repo_root: Path) -> list[dict]:
    """Milestones from ROADMAP.md Part G. Absent roadmap = no milestones."""
    path = roadmap_markdown_path(repo_root)
    if path is None:
        return []
    milestones: list[dict] = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        match = _MILESTONE_ROW_RE.match(line)
        if match is None:
            continue
        name = match.group(2).strip().strip('"')
        features = match.group(3).strip()
        milestones.append({
            "id": match.group(1),
            "name": name,
            "features": features,
            "tiers": [int(t) for t in re.findall(r"Tier\s*(\d{1,2})", features)]
                     + [int(t) for t in re.findall(r"\+\s*(\d{1,2})", features)],
            "proof": match.group(4).strip(),
        })
    return milestones


def _milestone_for_tier(milestones: list[dict], tier: int) -> str:
    for milestone in milestones:
        if tier in milestone["tiers"]:
            return milestone["id"]
    return ""


# ---------------------------------------------------------------------------
# Consistency checks (T002) — reported, never fatal
# ---------------------------------------------------------------------------

#: The three check classes. Grammar stays the only hard failure: these are
#: findings a human decides about, not reasons to refuse to read the roadmap.
CONSISTENCY_KINDS = ("status_without_file", "file_without_status", "unknown_dependency")


def check_consistency(files: dict[str, dict], entries: list[dict]) -> list[dict]:
    """Report roadmap inconsistencies as ``{kind, id, detail}`` records.

    * ``status_without_file`` — a STATUS line whose feature file is missing.
    * ``file_without_status`` — a feature file absent from STATUS; per the
      STATUS rules it is simply not scheduled, which is worth saying out loud.
    * ``unknown_dependency`` — a dependency or blocks reference to an id that
      exists in neither STATUS nor the feature files.
    """
    findings: list[dict] = []
    status_ids = {entry["id"] for entry in entries}
    known = status_ids | set(files)

    for entry in entries:
        if entry["id"] not in files:
            findings.append({
                "kind": "status_without_file",
                "id": entry["id"],
                "detail": f"listed in STATUS.md:{entry['line']} but no feature file defines it",
            })

    for feature_id, parsed in sorted(files.items()):
        if feature_id not in status_ids:
            findings.append({
                "kind": "file_without_status",
                "id": feature_id,
                "detail": f"{parsed['file']} is not listed in STATUS.md — treated as not scheduled",
            })

    for feature_id, parsed in sorted(files.items()):
        for label, refs in (("depends_on", parsed["depends_on"]), ("blocks", parsed["blocks"])):
            for ref in refs:
                if ref in known:
                    continue
                findings.append({
                    "kind": "unknown_dependency",
                    "id": feature_id,
                    "detail": f"{label} references unknown id {ref} ({parsed['file']}:2)",
                })
    return findings


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


def build_index(repo_root: Path | str | None = None) -> RoadmapIndex:
    """Mirror the roadmap markdown into a structured index.

    Raises :class:`RoadmapGrammarError` if the markdown breaks its grammar.
    Consistency findings land in ``index.inconsistencies`` — reported, not raised.
    """
    root = resolve_repo_root(repo_root)
    files, violations = _parse_feature_files(root)
    entries, status_violations = _parse_status(root)
    violations.extend(status_violations)
    if violations:
        raise RoadmapGrammarError(violations)

    milestones = _parse_milestones(root)
    status_by_id = {entry["id"]: entry for entry in entries}

    features: list[RoadmapFeature] = []
    for feature_id, parsed in sorted(files.items()):
        entry = status_by_id.get(feature_id)
        features.append(RoadmapFeature(
            id=feature_id,
            tier=parsed["tier"],
            title=parsed["title"],
            depends_on=parsed["depends_on"],
            blocks=parsed["blocks"],
            status=entry["status"] if entry else "not_scheduled",
            file=parsed["file"],
            status_line=entry["line"] if entry else 0,
            status_note=entry["note"] if entry else "",
            milestone=_milestone_for_tier(milestones, parsed["tier"]),
        ))

    # STATUS entries with no feature file still belong in the execution order.
    for entry in entries:
        if entry["id"] in files:
            continue
        features.append(RoadmapFeature(
            id=entry["id"],
            tier=entry["tier"],
            title=entry["title"],
            depends_on=(),
            blocks=(),
            status=entry["status"],
            file="",
            status_line=entry["line"],
            status_note=entry["note"],
            milestone=_milestone_for_tier(milestones, entry["tier"]),
        ))

    index = RoadmapIndex(
        features=tuple(features),
        milestones=tuple(milestones),
        order=tuple(entry["id"] for entry in entries),
        inconsistencies=tuple(check_consistency(files, entries)),
        repo_root=str(root),
    )
    return index


def build_and_write_index(repo_root: Path | str | None = None,
                          data_root: Path | None = None) -> tuple[RoadmapIndex, Path]:
    """Build the index and write it under the data root. One-way mirror."""
    index = build_index(repo_root)
    path = write_index(index, data_root)
    return index, path


def write_index(index: RoadmapIndex, data_root: Path | None = None) -> Path:
    """Write the generated index as JSON under the data root. Never committed."""
    path = roadmap_index_path(data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index.as_dict(), indent=2) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Reading the order (STATUS Rule A5)
# ---------------------------------------------------------------------------


def active_feature(index: RoadmapIndex) -> RoadmapFeature | None:
    """The in-progress ``[~]`` feature, first in STATUS order, or None."""
    for feature in index.ordered_features():
        if feature.status == "in_progress":
            return feature
    return None


def next_feature(index: RoadmapIndex) -> RoadmapFeature | None:
    """The first unchecked ``[ ]`` feature in STATUS order, or None."""
    for feature in index.ordered_features():
        if feature.status == "todo":
            return feature
    return None


def proposed_feature(index: RoadmapIndex) -> tuple[RoadmapFeature | None, str]:
    """What Rule A5 points at: the active ``[~]`` line, else the first ``[ ]``.

    Returns (feature, reason) with reason ``in_progress``, ``next_unchecked``
    or ``none``. This PROPOSES — nothing here starts any work.
    """
    active = active_feature(index)
    if active is not None:
        return active, "in_progress"
    nxt = next_feature(index)
    if nxt is not None:
        return nxt, "next_unchecked"
    return None, "none"


def blocker_states(index: RoadmapIndex, feature: RoadmapFeature) -> list[dict]:
    """State of each id the feature depends on — unknown ids included."""
    states: list[dict] = []
    for dep in feature.depends_on:
        found = index.by_id(dep)
        states.append({
            "id": dep,
            "status": found.status if found is not None else "unknown",
            "title": found.title if found is not None else "",
        })
    return states
