"""
Patch Intent v1 for Remedy.

A PatchIntent is a structured proposal for a change to an existing file in the
user's target repository.  In this version, intents are created and verified but
NEVER applied — they are read-only proposals stored in the Remedy-owned workspace.

Lifecycle:
  1. derive_patch_intents()     — produces a PatchIntentSet from a builder artifact
  2. verify_patch_intent_set()  — validates path safety and non-empty intent strings
  3. materialize_patch_intents()— writes a JSON file into the workspace (or no-op if empty)
  4. generate_dry_run_preview() — reads target file (read-only) and produces a
                                  human-readable preview; no writes to repo (Step 11)

Key constraints:
  - No repo files are modified by any function in this module.
  - repo_overwrite remains reserved and unused.
  - target_path is always relative, has no traversal, and must end in .md (v1).
  - Derivation is conservative: task_type keyword match only; no raw LLM paths accepted.
  - An empty PatchIntentSet is valid and expected for most task types.
  - Dry-run reads repo files with read_text only; no open() for writing, no os calls.
  - generate_dry_run_preview resolves both repo_root and the target path and asserts
    the target is inside repo_root before any read; raises RuntimeError if not.
  - truncate_preview(text) caps text at _MAX_PREVIEW_CHARS; CLI calls this before
    storing the combined preview in artifact metadata.
  - Risk levels are explicit constants (RISK_LOW/MEDIUM/HIGH/UNKNOWN) collected in
    RISK_LEVELS.  PatchDryRunResult.risk_level is validated against RISK_LEVELS in
    __post_init__ — an invalid value raises ValueError immediately at construction
    time rather than propagating silently.
  - RISK_UNKNOWN is intentionally conservative.  Future approval/autonomy modes must
    not treat it as equivalent to RISK_LOW — see classify_risk docstring.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from packages.core.models import Artifact
    from packages.orchestration.workspace import LocalWorkspaceRuntime, MaterializedFile


# ---------------------------------------------------------------------------
# Risk level constants (Step 12.5)
# ---------------------------------------------------------------------------

RISK_LOW: str = "low"
RISK_MEDIUM: str = "medium"
RISK_HIGH: str = "high"
RISK_UNKNOWN: str = "unknown"

# All valid risk level values.  PatchDryRunResult.risk_level is validated against
# this frozenset in __post_init__ — construction fails fast on invalid values.
#
# Step 13 note: RISK_UNKNOWN must be treated conservatively by any future
# approval/autonomy mode.  It means risk cannot be determined without repository
# context (preview-only action) or the action string is not recognised.
# Do NOT equate RISK_UNKNOWN with RISK_LOW.
RISK_LEVELS: frozenset[str] = frozenset({RISK_LOW, RISK_MEDIUM, RISK_HIGH, RISK_UNKNOWN})


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class PatchIntent(BaseModel):
    """A single structured proposal for a change to an existing repo file.

    This is a proposal only — nothing is written to or modified in the repo.

    target_path:     repo-relative path of the file that would be changed (e.g. README.md).
                     Must be relative, traversal-free, and end in .md (v1).
    intent:          human-readable description of what would change.
    rationale:       optional rationale for why the change is proposed.
    expected_effect: optional description of the observable outcome after applying.
    safety_notes:    list of notes about what was checked or deferred.
    """

    target_path: str
    intent: str
    rationale: str | None = None
    expected_effect: str | None = None
    safety_notes: list[str] = Field(default_factory=list)


class PatchIntentSet(BaseModel):
    """Collection of patch intents derived from one task execution artifact.

    task_id:     UUID of the task that produced the source artifact.
    artifact_id: UUID of the source artifact.
    intents:     ordered list of PatchIntent proposals; may be empty.
    """

    task_id: UUID
    artifact_id: UUID
    intents: list[PatchIntent] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Path-safe keyword table for derivation
# ---------------------------------------------------------------------------

# Conservative mapping from task_type keyword to a repo-relative target path.
# Mirrors _REPO_PATH_RULES in repo_applicator.py — same ordering, same semantics.
# Only documentation-like targets are eligible; source code is never targeted.
# {safe_type} is substituted with the sanitized task_type at derivation time.
#
# KEEP IN SYNC with _REPO_PATH_RULES in repo_applicator.py — enforced by TestKeywordSync in tests/test_patch_intent.py.
_INTENT_RULES: list[tuple[str, str]] = [
    ("readme",         "README.md"),
    # docs/remedy/ — evaluated before the plain "doc" catch-all
    ("plan",           "docs/remedy/{safe_type}.md"),
    ("spec",           "docs/remedy/{safe_type}.md"),
    ("requirement",    "docs/remedy/{safe_type}.md"),
    ("acceptance",     "docs/remedy/{safe_type}.md"),
    ("analysis",       "docs/remedy/{safe_type}.md"),
    # docs/ — "documentation" before "doc" (substring ordering)
    ("changelog",      "docs/{safe_type}.md"),
    ("architecture",   "docs/{safe_type}.md"),
    ("design",         "docs/{safe_type}.md"),
    ("guide",          "docs/{safe_type}.md"),
    ("documentation",  "docs/{safe_type}.md"),
    ("doc",            "docs/{safe_type}.md"),
]

_SAFE_PATH_RE = re.compile(r"[^a-zA-Z0-9_-]")
_MAX_PATH_COMPONENT_LENGTH = 48


def _sanitize_path_component(value: str) -> str:
    """Sanitize a string for safe use as a single path component.

    Same logic as task_runner._sanitize_path_component — kept local to avoid
    importing a private helper across modules.
    """
    sanitized = _SAFE_PATH_RE.sub("_", value)
    sanitized = sanitized[:_MAX_PATH_COMPONENT_LENGTH].strip("_")
    return sanitized or "unknown"


def _derive_target_path(task_type: str) -> str | None:
    """Return a safe repo-relative path for the task_type, or None if no match."""
    lower = task_type.lower()
    safe_type = _sanitize_path_component(task_type)
    for keyword, template in _INTENT_RULES:
        if keyword in lower:
            return template.format(safe_type=safe_type)
    return None


# ---------------------------------------------------------------------------
# Derivation
# ---------------------------------------------------------------------------


def derive_patch_intents(artifact: "Artifact", task_type: str) -> PatchIntentSet:
    """Derive a PatchIntentSet from a builder artifact and its task type.

    Uses the conservative keyword table (_INTENT_RULES) to map task_type to a
    documentation-like target path.  If the task type does not match any keyword,
    the returned PatchIntentSet has an empty intents list (which is valid).

    No raw LLM strings are used to construct target paths.

    Args:
        artifact:  the task execution artifact produced by the builder.
        task_type: the task_type string from artifact metadata.

    Returns:
        A PatchIntentSet — possibly with zero intents.

    Raises:
        RuntimeError: if artifact.task_id or artifact.id is None (invariant violation
                      — this function must only be called with task-owned artifacts).
    """
    if artifact.task_id is None:
        raise RuntimeError(
            "derive_patch_intents: artifact.task_id is None. "
            "Patch intents must be derived from task-owned artifacts only."
        )
    if artifact.id is None:
        raise RuntimeError(
            "derive_patch_intents: artifact.id is None. "
            "Artifact must have a valid id before patch intents are derived."
        )

    target = _derive_target_path(task_type)
    intents: list[PatchIntent] = []

    if target is not None:
        summary = artifact.metadata.get("summary", "")
        intents.append(
            PatchIntent(
                target_path=target,
                intent=summary or f"Proposed change for task type '{task_type}'",
                safety_notes=[
                    "derived from task_type keyword match",
                    "not applied to repository — proposal only",
                ],
            )
        )

    return PatchIntentSet(
        task_id=artifact.task_id,
        artifact_id=artifact.id,
        intents=intents,
    )


# ---------------------------------------------------------------------------
# Verifier
# ---------------------------------------------------------------------------


def verify_patch_intent_set(pis: PatchIntentSet) -> list[str]:
    """Validate a PatchIntentSet for structural safety.

    Returns a list of error strings.  An empty list means the set is valid.
    An empty intents list is always valid — no errors.

    Checks per intent:
      - target_path is non-empty
      - target_path is relative (does not start with '/')
      - target_path has no traversal ('..') in any component
      - target_path ends with '.md' (documentation-like paths only in v1)
      - intent is non-empty
    """
    errors: list[str] = []
    for i, intent in enumerate(pis.intents):
        p = intent.target_path
        tag = f"intent[{i}]"
        if not p:
            errors.append(f"{tag}.target_path is empty")
            continue
        if "\x00" in p:
            errors.append(f"{tag}.target_path contains a null byte, which is not allowed")
            continue
        if p.startswith("/"):
            errors.append(f"{tag}.target_path {p!r}: absolute paths are not allowed")
        if ".." in p.split("/"):
            errors.append(f"{tag}.target_path {p!r}: path traversal ('..') is not allowed")
        if not p.endswith(".md"):
            errors.append(
                f"{tag}.target_path {p!r}: only .md documentation paths are allowed in v1"
            )
        if not intent.intent:
            errors.append(f"{tag}.intent is empty")
    return errors


# ---------------------------------------------------------------------------
# Materialization
# ---------------------------------------------------------------------------


def materialize_patch_intents(
    pis: PatchIntentSet,
    runtime: "LocalWorkspaceRuntime",
    task_index: int,
    task_type: str,
) -> "MaterializedFile | None":
    """Write a PatchIntentSet as a JSON file inside the workspace.

    Path: patch_intents/{index:03d}_{safe_type}_{short_task_id}.json

    Returns None if pis.intents is empty (no file is written).
    The caller is responsible for recording the file path in artifact metadata.

    Args:
        pis:        the PatchIntentSet to serialize.
        runtime:    the workspace runtime to write into.
        task_index: 0-based position of the task in job.tasks (for filename ordering).
        task_type:  the task_type string (sanitized for the filename).
    """
    if not pis.intents:
        return None

    safe_type = _sanitize_path_component(task_type)
    short_id = pis.task_id.hex[:8]
    relative_path = f"patch_intents/{task_index:03d}_{safe_type}_{short_id}.json"
    content = pis.model_dump_json(indent=2)
    return runtime.write(relative_path, content)


# ---------------------------------------------------------------------------
# Dry-run preview and explanation layer (Step 11)
# ---------------------------------------------------------------------------


# Known section headers in the builder artifact content format.
# Kept local to avoid importing private helpers from task_runner.
_ARTIFACT_SECTION_HEADERS: frozenset[str] = frozenset(
    {"Summary:", "Proposed Changes:", "Notes:", "Risks:"}
)

# Maximum characters kept for the summary field in an explanation.
_MAX_SUMMARY_CHARS = 120
# Maximum lines of existing file content shown as context in a preview.
_MAX_CONTEXT_LINES = 4
# Maximum proposed-change lines shown in a single preview block.
_MAX_PROPOSED_LINES = 10
# Hard cap on the combined diff_preview string stored in artifact metadata.
_MAX_PREVIEW_CHARS = 2000


def truncate_preview(text: str) -> str:
    """Truncate a combined diff-preview string to at most _MAX_PREVIEW_CHARS characters.

    Callers (e.g. the CLI) use this before storing the combined preview in artifact
    metadata.  Centralising the cap here keeps callers free of the internal constant.
    """
    return text[:_MAX_PREVIEW_CHARS]


def classify_risk(action: str) -> str:
    """Classify the risk level of a proposed change based on its action.

    Risk levels:
      "low"     — new file (create): no existing content is at risk.
      "medium"  — modify existing file: existing content could change.
      "high"    — overwrite existing file (reserved; placeholder for a future
                  action type that would unconditionally replace file content).
      "unknown" — action is "preview-only" (no repository attached; risk
                  cannot be determined without knowing whether the file exists)
                  or the action string is not recognised.

    This function is non-blocking and has no side effects.
    Callers MUST NOT equate RISK_UNKNOWN with RISK_LOW — see module docstring.
    """
    if action == "create":
        return RISK_LOW
    if action == "modify":
        return RISK_MEDIUM
    if action == "overwrite":  # reserved — not yet produced by any code path
        return RISK_HIGH
    # "preview-only" (no repo attached) and any unrecognised action both return
    # RISK_UNKNOWN.  Risk cannot be determined without repository context.
    return RISK_UNKNOWN


@dataclass
class PatchDryRunResult:
    """Dry-run preview for a single PatchIntent.

    Transient — not persisted directly; compact representations are stored
    in artifact metadata by the CLI.

    target_path:  the repo-relative path that would be targeted.
    action:       "create" | "modify" | "preview-only" (no repo attached).
    risk_level:   "low" | "medium" | "high" | "unknown" — from classify_risk().
    reason:       short human-readable reason (e.g. "task type 'write_readme'").
    summary:      truncated intent text from the PatchIntent.
    diff_preview: human-readable preview block — NOT a real patch; read-only.
    """

    target_path: str
    action: str
    risk_level: str
    reason: str
    summary: str
    diff_preview: str

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(
                f"PatchDryRunResult.risk_level {self.risk_level!r} is not a valid risk "
                f"level.  Valid values: {sorted(RISK_LEVELS)}"
            )


def _extract_proposed_lines(artifact_content: str) -> list[str]:
    """Extract plain-text lines from the 'Proposed Changes:' section.

    Same section-boundary logic as task_runner._extract_proposed_changes,
    kept local to avoid cross-module private-helper imports.
    Returns stripped lines (leading '  - ' prefix removed).
    """
    lines: list[str] = []
    in_section = False
    for line in artifact_content.splitlines():
        if line == "Proposed Changes:":
            in_section = True
        elif line in _ARTIFACT_SECTION_HEADERS:
            in_section = False
        elif in_section and line.startswith("  - "):
            lines.append(line[4:])  # strip "  - " → plain text
    return lines


def _build_preview_block(
    target_path: str,
    action: str,
    proposed_lines: list[str],
    existing_lines: list[str] | None,
) -> str:
    """Build a compact, human-readable preview block for one intent.

    Not a real patch format — clearly labeled as a proposal preview.
    No filesystem writes; only reads the already-fetched existing_lines.
    """
    parts: list[str] = []

    if action == "preview-only":
        parts.append(f"[preview-only — no repository attached]")
        parts.append(f"would target: {target_path}")
    elif action == "create":
        parts.append(f"+++ {target_path}  (new file — does not exist yet)")
    else:  # modify
        parts.append(f"--- {target_path}  (existing file)")
        if existing_lines:
            context = existing_lines[:_MAX_CONTEXT_LINES]
            parts.extend(f"    {ln}" for ln in context)
            remainder = len(existing_lines) - _MAX_CONTEXT_LINES
            if remainder > 0:
                parts.append(f"    ... ({remainder} more line(s))")

    if proposed_lines:
        label = "proposed:" if action == "preview-only" else "proposed additions:"
        if action == "create":
            label = "proposed content:"
        parts.append(label)
        shown = proposed_lines[:_MAX_PROPOSED_LINES]
        parts.extend(f"  + {ln}" for ln in shown)
        remainder = len(proposed_lines) - _MAX_PROPOSED_LINES
        if remainder > 0:
            parts.append(f"  ... ({remainder} more)")
    else:
        parts.append("  (no proposed-change lines found in artifact)")

    return "\n".join(parts)


def generate_dry_run_preview(
    pis: PatchIntentSet,
    artifact_content: str,
    task_type: str,
    repo_root: Path | None = None,
) -> list[PatchDryRunResult]:
    """Generate a dry-run preview for each intent in pis.

    Reads existing target files from repo_root (read-only) when provided.
    No files are created, modified, or deleted.

    Args:
        pis:             the PatchIntentSet to preview.
        artifact_content: raw content string of the builder artifact
                          (used to extract proposed-change lines).
        task_type:       the task_type string (for the human-readable reason).
        repo_root:       absolute path to the attached target repository, or
                         None if no repository is attached.

    Returns:
        One PatchDryRunResult per intent in pis.intents.
        Returns an empty list if pis.intents is empty.
    """
    if not pis.intents:
        return []

    proposed_lines = _extract_proposed_lines(artifact_content)
    reason = f"task type '{task_type}'"
    results: list[PatchDryRunResult] = []

    for intent in pis.intents:
        summary = intent.intent[:_MAX_SUMMARY_CHARS]

        if repo_root is None:
            action = "preview-only"
            existing_lines: list[str] | None = None
        else:
            # Boundary check — defence in depth even though verify_patch_intent_set
            # already rejects traversal in path components.  Resolving both sides
            # catches symlink escapes and any edge-case path that slips through.
            resolved_root = repo_root.resolve()
            target_file = (repo_root / intent.target_path).resolve()
            if not target_file.is_relative_to(resolved_root):
                raise RuntimeError(
                    f"generate_dry_run_preview: target path {intent.target_path!r} "
                    f"resolves to {str(target_file)!r} which is outside repo_root "
                    f"{str(resolved_root)!r}.  Path traversal is not allowed."
                )
            if target_file.exists():
                action = "modify"
                existing_lines = target_file.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            else:
                action = "create"
                existing_lines = None

        diff_preview = _build_preview_block(
            intent.target_path, action, proposed_lines, existing_lines
        )
        results.append(
            PatchDryRunResult(
                target_path=intent.target_path,
                action=action,
                risk_level=classify_risk(action),
                reason=reason,
                summary=summary,
                diff_preview=diff_preview,
            )
        )

    return results


def format_dry_run_explanations(results: list[PatchDryRunResult]) -> str:
    """Format dry-run results as a human-readable block for CLI output.

    Returns an empty string if results is empty.
    Each result is rendered as a labeled block showing file, action, reason,
    and a truncated summary of the proposed change.
    """
    if not results:
        return ""

    blocks: list[str] = []
    for r in results:
        lines = [
            "Planned change:",
            f"  file   : {r.target_path}",
            f"  action : {r.action}",
            f"  risk   : {r.risk_level}",
            f"  reason : {r.reason}",
            f"  summary: {r.summary}",
        ]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
