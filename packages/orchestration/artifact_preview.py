"""Artifact preview — the roots a job's artifacts live under, and the traversal gate
between a requested name and a file the cockpit reads (F041 T001, DECISION F041 D1).

``artifact_root`` derives a job's staging workspace and evidence directory from the
data-root class registry (never from a job record — a recorded path is input, not
authority). ``resolve_artifact_path`` is the ONE gate a requested relative name passes
through before a byte of it is read: it refuses an absolute path, a ``..`` part, a
backslash, a NUL, and any symlink that resolves outside its root. ``artifacts_view``
answers the whole view the ``artifacts`` endpoint of ``ui_server.py`` serves: the
README rendered and sanitized by :mod:`packages.orchestration.artifact_markdown`, and
the screenshot list under ``captures/`` in the evidence directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from packages.orchestration.artifact_markdown import render_markdown
from packages.orchestration.data_paths import data_class_dir, job_evidence_dir
from packages.orchestration.staging_workspace import STAGING_DATA_CLASS, staging_dir_name

#: The two roots a README or a screenshot may resolve under, in README precedence
#: order: the staging workspace (the job's own copy of the target repo) wins over the
#: job's evidence directory.
ROOT_WORKSPACE = "workspace"
ROOT_EVIDENCE = "evidence"
ARTIFACT_ROOTS = (ROOT_WORKSPACE, ROOT_EVIDENCE)

README_NAME = "README.md"
CAPTURES_DIRNAME = "captures"

#: Screenshot suffixes the cockpit will show, to their content type. SVG is
#: deliberately absent — an SVG can carry script, and this view never runs one
#: through a sanitizer of its own.
IMAGE_CONTENT_TYPES = {
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

#: The screenshot list is capped so a job with a runaway capture loop cannot hand the
#: cockpit an unbounded response.
MAX_LISTED_IMAGES = 200


def artifact_root(job_id: str, root: str, data_root: Path | None = None) -> Path | None:
    """The directory ROOT names for JOB_ID, or None for an unknown name or an absent
    directory. DERIVED from the data-root class registry, never read from a record."""
    if root == ROOT_WORKSPACE:
        candidate = data_class_dir(STAGING_DATA_CLASS, data_root) / staging_dir_name(job_id)
    elif root == ROOT_EVIDENCE:
        candidate = job_evidence_dir(job_id, data_root)
    else:
        return None
    return candidate if candidate.is_dir() else None


def resolve_artifact_path(base: Path, relative: str) -> Path | None:
    """The file RELATIVE names under BASE, or None when it escapes BASE or is absent.

    Refused outright, before any resolution: an empty name, a name holding a
    backslash or a NUL, an absolute `PurePosixPath`, or one with a `..` part. What
    remains is resolved (following symlinks) and refused unless it both stays inside
    BASE and names an existing FILE — a directory, a symlink escaping BASE, or a
    symlinked directory whose target escapes BASE, all resolve to None.
    """
    if not relative or "\\" in relative or "\x00" in relative:
        return None
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    root = base.resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        return None
    return candidate


def _readme_view(job_id: str, data_root: Path | None) -> tuple[dict | None, str]:
    for root_name in ARTIFACT_ROOTS:
        root = artifact_root(job_id, root_name, data_root)
        if root is None:
            continue
        path = resolve_artifact_path(root, README_NAME)
        if path is None:
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            return None, "the README could not be read"
        rendered = render_markdown(raw.decode("utf-8", errors="replace"))
        return {
            "root": root_name,
            "path": README_NAME,
            "html": rendered.html,
            "truncated": rendered.truncated,
            "source_bytes": rendered.source_bytes,
        }, ""
    return None, ""


def _images_view(job_id: str, data_root: Path | None) -> list[dict]:
    evidence_root = artifact_root(job_id, ROOT_EVIDENCE, data_root)
    if evidence_root is None:
        return []
    captures_dir = evidence_root / CAPTURES_DIRNAME
    if not captures_dir.is_dir():
        return []
    images: list[dict] = []
    for entry in sorted(captures_dir.iterdir(), key=lambda p: p.name):
        content_type = IMAGE_CONTENT_TYPES.get(entry.suffix.lower())
        if content_type is None:
            continue
        relative = f"{CAPTURES_DIRNAME}/{entry.name}"
        resolved = resolve_artifact_path(evidence_root, relative)
        if resolved is None:
            continue
        images.append({
            "root": ROOT_EVIDENCE,
            "path": relative,
            "bytes": resolved.stat().st_size,
            "content_type": content_type,
        })
        if len(images) >= MAX_LISTED_IMAGES:
            break
    return images


def artifacts_view(job_id: str, data_root: Path | None = None) -> dict:
    """The whole artifacts view for JOB_ID: `readme`, `images`, `error`. READ-ONLY."""
    readme, error = _readme_view(job_id, data_root)
    return {"readme": readme, "images": _images_view(job_id, data_root), "error": error}


#: The file route's own size cap (F041 T001, DECISION F041 D2): a served body is capped
#: at 10 MiB so a body is never streamed unbounded through the localhost server.
FILE_MAX_BYTES = 10_485_760

#: The README is served as plain text, never as a type a browser might sniff or render
#: (DECISION F041 D2, clause 2) — "open full file" means the raw source, not a page.
README_CONTENT_TYPE = "text/plain; charset=utf-8"


@dataclass(frozen=True)
class ArtifactFile:
    """One file route answer (F041 T001, DECISION F041 D2): bytes on success, or a
    refusal whose `content_type` and `body` are always empty."""

    status: int
    content_type: str
    body: bytes
    error: str


def _refused_artifact_file(status: int, error: str) -> ArtifactFile:
    return ArtifactFile(status=status, content_type="", body=b"", error=error)


def read_artifact_file(
    job_id: str, root: str, relative: str, data_root: Path | None = None,
) -> ArtifactFile:
    """The bytes RELATIVE names under ROOT for JOB_ID (F041 T001, DECISION F041 D2).

    Exactly two names are servable: `README_NAME` from either root, served as
    `README_CONTENT_TYPE`, and one `captures/<name>` file directly under the evidence
    root whose lowercased suffix is in `IMAGE_CONTENT_TYPES`, served as that type —
    "exactly" means `relative` equals `f"{CAPTURES_DIRNAME}/{PurePosixPath(relative).name}"`,
    so no `.`, `..`, empty or extra segment passes. Any other request answers 400
    `"invalid artifact request"` before a byte of disk is touched. The root is then found
    with `artifact_root` and the name with `resolve_artifact_path`; either `None` answers
    404 `"artifact not found"`. A file whose size is over `FILE_MAX_BYTES` answers 413
    `"artifact too large"`; an `OSError` reading it answers 404. Otherwise 200 with the
    bytes and an empty error. Every refusal carries an empty `content_type` and body.
    """
    if root not in ARTIFACT_ROOTS:
        return _refused_artifact_file(400, "invalid artifact request")
    if relative == README_NAME:
        content_type = README_CONTENT_TYPE
    else:
        name = PurePosixPath(relative).name
        suffix_type = IMAGE_CONTENT_TYPES.get(PurePosixPath(relative).suffix.lower())
        if (root == ROOT_EVIDENCE
                and relative == f"{CAPTURES_DIRNAME}/{name}"
                and suffix_type is not None):
            content_type = suffix_type
        else:
            return _refused_artifact_file(400, "invalid artifact request")

    base = artifact_root(job_id, root, data_root)
    if base is None:
        return _refused_artifact_file(404, "artifact not found")
    path = resolve_artifact_path(base, relative)
    if path is None:
        return _refused_artifact_file(404, "artifact not found")
    try:
        if path.stat().st_size > FILE_MAX_BYTES:
            return _refused_artifact_file(413, "artifact too large")
        body = path.read_bytes()
    except OSError:
        return _refused_artifact_file(404, "artifact not found")
    return ArtifactFile(status=200, content_type=content_type, body=body, error="")
