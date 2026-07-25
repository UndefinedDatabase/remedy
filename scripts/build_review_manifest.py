#!/usr/bin/env python3
"""Build a valid JSON review zip manifest.

Called by make_review_zip.sh. Produces always-valid JSON regardless of
git state, file paths, or evidence dir contents.

Usage:
    python3 scripts/build_review_manifest.py [--evidence-dir <path>] [--output <path>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# Shared canonical provenance-hash implementation — the validator and the
# attestation writer MUST use the same code so they cannot drift apart.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
try:
    from packages.orchestration.repair_attest import (
        build_safe_diff_text as _canon_safe_diff_text,
    )
    from packages.orchestration.repair_attest import (
        canonical_provenance_sha256 as _canon_provenance_sha256,
    )
    from packages.orchestration.repair_attest import (
        parse_safe_diff_paths as _canon_parse_safe_diff_paths,
    )
    from packages.orchestration.repair_attest import (
        sha256_text as _canon_sha256_text,
    )
    _CANON_AVAILABLE = True
except Exception:  # pragma: no cover - defensive; canonical impl must exist
    _CANON_AVAILABLE = False


def _git(cmd: list[str]) -> str:
    try:
        r = subprocess.run(
            ["git"] + cmd,
            capture_output=True, text=True, timeout=10,
        )
        return r.stdout.strip().split("\n")[0] if r.returncode == 0 else "unknown"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "unknown"


def _check(path: str) -> str:
    return "present" if os.path.isfile(path) else "absent"


def _strict_json_loads(raw):
    """F5 (round 25/26): the ONE strict decoder for every trusted gate/evidence read — imported from
    the single shared ``packages.common.strict_json`` implementation, so duplicate keys (at any
    depth), NaN/Infinity and invalid UTF-8 are refused identically here and in the archive builder.
    The import is dependency-free so the standalone manifest builder stays importable in minimal
    environments."""
    from packages.common.strict_json import strict_loads
    return strict_loads(raw, where="gate/evidence artifact")


class _EvidenceView:
    """F6 (round 24): a read-only Evidence accessor over an IMMUTABLE ``rel_path -> bytes`` map.

    Once this view is built — from the coordinator's Source snapshot, or by reading a directory
    exactly once — NO Evidence fact in the Root Manifest is ever re-read from the staging
    filesystem: every gate, proof, provenance and task-run fact comes from these exact bytes, so a
    file that changes on disk between the snapshot and the manifest cannot be interpreted from one
    read and packaged from another. Repository/Git facts are resolved separately from the repo.
    """

    def __init__(self, files, mtimes=None):
        self._files = {self._norm(k): v for k, v in dict(files).items()}
        self._mtimes = {self._norm(k): v for k, v in dict(mtimes or {}).items()}
        self._dirs: set[str] = {""}
        for k in self._files:
            parts = k.split("/")
            for i in range(1, len(parts)):
                self._dirs.add("/".join(parts[:i]))

    @staticmethod
    def _norm(rel: str) -> str:
        return str(rel or "").replace(os.sep, "/").replace("\\", "/").strip("/")

    def isfile(self, rel: str) -> bool:
        return self._norm(rel) in self._files

    def isdir(self, rel: str) -> bool:
        return self._norm(rel) in self._dirs

    def listdir(self, rel: str):
        base = self._norm(rel)
        prefix = (base + "/") if base else ""
        names: set[str] = set()
        for k in list(self._files) + list(self._dirs):
            if k.startswith(prefix) and k != base:
                rest = k[len(prefix):]
                if rest:
                    names.add(rest.split("/")[0])
        return sorted(names)

    def read_bytes(self, rel: str):
        return self._files.get(self._norm(rel))

    def read_text(self, rel: str):
        b = self._files.get(self._norm(rel))
        return None if b is None else b.decode("utf-8", errors="surrogateescape")

    def read_json(self, rel: str) -> dict:
        """A JSON object from the view, or {} if absent/invalid/non-object/duplicate-keyed (the
        shared tolerant read used by _mc_read_json / _read_evidence_gate)."""
        b = self._files.get(self._norm(rel))
        if b is None:
            return {}
        try:
            data = _strict_json_loads(b)                # F5 (round 25): duplicate keys rejected
        except Exception:
            return {}
        return data if isinstance(data, dict) else {}

    def read_json_strict(self, rel: str):
        """None if absent; a DUPLICATE-KEY-REJECTING strict decode otherwise (F5, round 25) — a
        corrupt or ambiguous gate (``"verdict": "BLOCKED", "verdict": "PASS"``) RAISES and so BLOCKS
        rather than silently collapsing to the stdlib's last-wins value."""
        b = self._files.get(self._norm(rel))
        if b is None:
            return None
        return _strict_json_loads(b)

    def status(self, rel: str) -> str:
        return "present" if self.isfile(rel) else "absent"

    def mtime_iso(self, rel: str) -> str:
        return self._mtimes.get(self._norm(rel), "")

    def gate_loader(self):
        return self.read_json_strict


def _view_from_dir(evidence_dir: str) -> _EvidenceView:
    """F6 (round 25) / F4 (round 26): read an evidence directory ONCE into an immutable byte map
    through the shared ANCHORED, O_NOFOLLOW ``secure_fs`` primitives — never ``os.walk``/``open`` by
    name. A symlink (dir or file), FIFO, socket or device is NEVER followed or read; every regular
    member is opened ``O_NOFOLLOW``, identity-checked and stably read, and CHARGED against the shared
    acquisition budget so an over-count/over-byte tree BLOCKS (raises) rather than being silently
    truncated. The coordinator uses ``_view_from_snapshot``."""
    import stat as _stat

    from packages.common import secure_fs
    from packages.common.acquisition_budget import AcquisitionBudget

    files: dict[str, bytes] = {}
    mtimes: dict[str, str] = {}
    budget = AcquisitionBudget()
    try:
        root_fd = secure_fs.anchor_root(evidence_dir, noun="evidence dir", create=False)
    except Exception:
        return _EvidenceView({})

    def _collect(dir_fd: int, relbase: str) -> None:
        for name in secure_fs.list_dir_names(dir_fd):
            try:
                st = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
            except OSError:
                continue
            rel = f"{relbase}/{name}" if relbase else name
            if _stat.S_ISLNK(st.st_mode):
                continue                                # never follow a symlink — no outside bytes
            if _stat.S_ISDIR(st.st_mode):
                try:
                    sub = secure_fs.open_verified_dir(name, dir_fd=dir_fd, noun="evidence dir")
                except Exception:
                    continue
                try:
                    _collect(sub, rel)
                finally:
                    os.close(sub)
            elif _stat.S_ISREG(st.st_mode):
                # Charge FIRST from the no-follow lstat size — an over-limit tree BLOCKS here rather
                # than being read and then silently skipped.
                budget.charge(rel, st.st_size)
                try:
                    vf = secure_fs.read_verified_file_at(
                        dir_fd, name, expected_kind="regular",
                        max_bytes=st.st_size + 1, noun="evidence file")
                except Exception:
                    continue                            # symlink swap / torn — refuse, never read
                files[rel] = vf.data
                mtimes[rel] = datetime.fromtimestamp(
                    st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            # FIFO / socket / device → skipped, never read

    try:
        _collect(root_fd, "")
    finally:
        os.close(root_fd)
    return _EvidenceView(files, mtimes)


def _view_from_snapshot(snapshot, current_prefix: str) -> _EvidenceView:
    """Build the Evidence view from the coordinator's immutable Source snapshot
    (``dict[archive_path, SnapshotMember]``): the SAME bytes the ZIP packages, keyed by the path
    relative to ``current_prefix``. No staging-filesystem read happens here or downstream."""
    prefix = current_prefix.replace(os.sep, "/").strip("/") + "/"
    files: dict[str, bytes] = {}
    for arc, member in snapshot.items():
        arc_n = str(arc).replace(os.sep, "/").strip("/")
        if arc_n.startswith(prefix):
            files[arc_n[len(prefix):]] = member.data
    return _EvidenceView(files)


def _as_view(ev):
    """Accept an already-built ``_EvidenceView`` OR a directory path (str/os.PathLike). A path is
    read ONCE into an immutable view — this is the only place the standalone helpers touch the FS,
    and the coordinator always passes a snapshot-backed view so it never reaches this branch."""
    if ev is None or isinstance(ev, _EvidenceView):
        return ev
    return _view_from_dir(os.fspath(ev)) if os.path.isdir(os.fspath(ev)) else _EvidenceView({})


SOURCE_ROOT_TOKEN = "[source_root]"
EXTERNAL_EVIDENCE_TOKEN = "[external_evidence]"


def _shareable_path(path: str, source_root: str) -> str:
    """Render a filesystem path so it carries no machine-specific root.

    The review manifest is shared with external reviewers, so it must never
    disclose ``/home/<user>``, ``/Users/<user>``, ``/tmp/...`` or any other
    private absolute prefix. Paths inside the repository become
    ``[source_root]/<relative>``; anything outside collapses to its basename
    under ``[external_evidence]``.
    """
    if not path:
        return ""
    root = os.path.realpath(source_root) if source_root else ""
    resolved = os.path.realpath(path)
    if root and (resolved == root):
        return SOURCE_ROOT_TOKEN
    if root and resolved.startswith(root + os.sep):
        rel = os.path.relpath(resolved, root).replace(os.sep, "/")
        return f"{SOURCE_ROOT_TOKEN}/{rel}"
    return f"{EXTERNAL_EVIDENCE_TOKEN}/{os.path.basename(resolved.rstrip(os.sep))}"


def _probe_publication_capability(source_root: str) -> dict:
    """Round 40 F5: probe and bind publication capability into the root manifest."""
    try:
        from packages.orchestration.safe_publish import probe_anonymous_publication_capability
        status = probe_anonymous_publication_capability(source_root)
    except Exception:
        status = "PROBE_ERROR"
    return {
        "status": status,
        "primitive": "linkat" if status == "SUPPORTED" else "none",
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _parse_status_z(raw: str, strict: bool = False) -> list[tuple[str, str]]:
    """Parse ``git status --porcelain=v1 -z`` into ``(XY, path)`` records.

    F4 (round 29): the NUL-delimited format preserves BOTH status columns and needs no quoted-path
    decoding, so the leading status character is never mistaken for part of the path and a path with
    spaces/unicode/quotes survives verbatim. A rename/copy record (``R``/``C``) is followed by a
    separate NUL field carrying the ORIGIN path; the record's own path is the NEW path.

    F5 (round 32): with ``strict``, a primary record that is not ``XY<space>PATH`` (two status columns,
    a space, then a non-empty path) is MALFORMED and raises ``ValueError`` — a corrupt snapshot blocks
    rather than being read as a partial/clean tree.
    """
    records: list[tuple[str, str]] = []
    parts = raw.split("\0")
    i = 0
    while i < len(parts):
        entry = parts[i]
        if not entry:
            i += 1
            continue
        if strict and (len(entry) < 4 or entry[2] != " "):
            raise ValueError(f"malformed porcelain record {entry[:12]!r}")
        xy = entry[:2]
        path = entry[3:] if len(entry) >= 3 else ""       # skip 'XY ' — never strip the status
        if xy[:1] in ("R", "C") and i + 1 < len(parts):
            i += 1                                         # consume the origin field
        if path:
            records.append((xy, path))
        i += 1
    return records


#: F5 (round 32): git-status is acquired ONCE, as a typed immutable snapshot. Only ``OK`` may mean a
#: clean tree; ``FAILED``/``TIMED_OUT``/``UNAVAILABLE``/``MALFORMED`` block READY and are recorded with
#: a bounded diagnostic — a git failure can never fall open to "clean".
def _git_status_snapshot() -> dict:
    """Run ``git status --porcelain=v1 -z -u`` exactly once and return
    ``{status, records, diagnostic}``. ``records`` is the parsed ``(XY, path)`` list only when
    ``status == "OK"``; every failure mode is distinguished and never silently becomes an empty list.
    """
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "-u"],
            capture_output=True, text=True, timeout=10,
        )
    except FileNotFoundError:
        return {"status": "UNAVAILABLE", "records": [], "diagnostic": "git executable not found"}
    except subprocess.TimeoutExpired:
        return {"status": "TIMED_OUT", "records": [], "diagnostic": "git status timed out"}
    except Exception as exc:                               # pragma: no cover - defensive
        return {"status": "FAILED", "records": [], "diagnostic": f"{type(exc).__name__}: {str(exc)[:120]}"}
    if r.returncode != 0:
        return {"status": "FAILED", "records": [],
                "diagnostic": f"git status exit {r.returncode}: {(r.stderr or '')[:120]}"}
    try:
        records = _parse_status_z(r.stdout, strict=True)
    except ValueError as exc:
        return {"status": "MALFORMED", "records": [], "diagnostic": str(exc)[:120]}
    return {"status": "OK", "records": records, "diagnostic": ""}


def _git_status_records() -> list[tuple[str, str]]:
    # Back-compat accessor: the records of the single snapshot (empty on any non-OK status).
    return _git_status_snapshot()["records"]


def _dirty_files() -> list[str]:
    # Back-compat: an OK snapshot's records rebuilt as ``XY PATH``; a failed snapshot yields no records
    # (callers that need the fail-closed status use ``_git_status_snapshot`` directly).
    return [f"{xy} {path}" for xy, path in _git_status_records()]


def _has_untracked_files() -> bool:
    return any(xy == "??" for xy, _ in _git_status_snapshot()["records"])


def _has_commits() -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and len(r.stdout.strip()) >= 7
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _dirty_line_path(line: str) -> str:
    """The exact repository-relative path from an ``XY PATH`` record.

    F4 (round 29): the path is everything after the two status columns and the single separating
    space — column 3 onward. The leading status character must NOT be dropped, and the path is never
    ``.strip()``ed (a path may legitimately contain leading/trailing spaces). A legacy newline-format
    rename ``old -> new`` still resolves to the new path.
    """
    body = line[3:] if len(line) >= 3 else line
    if " -> " in body:
        body = body.split(" -> ", 1)[1]
    return body


#: The ONLY shapes a repository-ROOT path may take to be a packaging output: the root manifest, or a
#: ``remedy-review-<YYYYMMDD>-<HHMMSS>[-<STATUS>].zip`` (with an optional ``.sha256`` sidecar). This is
#: a floor, not the authority — the authority is exact membership in the invocation's DERIVED set.
_GENERATED_OUTPUT_RE = re.compile(r"^remedy-review-\d{8}-\d{6}(-[A-Z][A-Z_]*)?\.zip(\.sha256)?$")


def _eligible_generated_output(path: str) -> bool:
    """F3 (round 29): a path may be treated as a self-generated packaging output ONLY when it is a
    repository-ROOT path (no directory component) whose name is a packaging-output shape. A caller
    that declares an arbitrary SOURCE path (``scripts/security_fix.py``) — or a root source lookalike
    — can therefore never have it dispositioned out of the dirty subject, no matter what set it
    supplies."""
    p = str(path or "").replace("\\", "/").strip().strip('"')
    if not p or "/" in p:
        return False
    return p == ".review_zip_manifest.json" or bool(_GENERATED_OUTPUT_RE.fullmatch(p))


def _normalize_generated(paths) -> frozenset:
    """The repository-ROOT-relative paths the CURRENT packaging invocation generates, normalized to
    the same form ``_dirty_line_path`` yields (forward slashes, trimmed, unquoted) and filtered to
    the eligible packaging-output shapes — an ineligible declared path is dropped, never trusted."""
    out = set()
    for p in (paths or ()):
        s = str(p or "").replace("\\", "/").strip().strip('"')
        if s and _eligible_generated_output(s):
            out.add(s)
    return frozenset(out)


def _classify_review_subject(
    branch: str, commit: str, dirty: list[str],
    has_untracked: bool, has_commits_val: bool,
    generated_outputs=frozenset(), git_status: str = "OK",
) -> dict:
    is_main = branch in ("main", "master")
    # F3 (round 28): a working-tree change is a self-generated packaging output ONLY when its path is
    # a member of the EXACT set of outputs THIS packaging invocation generates (passed down from
    # make_review_zip.sh: the current run's root manifest and its own ZIP name). Round 27 matched an
    # invocation-independent filename GRAMMAR, so an arbitrary leftover/forged root ZIP from another
    # run (``remedy-review-20200101-000000-READY_FOR_REVIEW.zip``, ``...-EVIL.zip``) was silently
    # dispositioned out of the dirty subject — hiding a real changed file. Now only exact membership
    # in the current invocation's own output set classifies; everything else is a dirty source file.
    gen = _normalize_generated(generated_outputs)
    packaging_outputs = sorted({_dirty_line_path(x) for x in dirty
                                if _dirty_line_path(x) in gen})
    dirty_source = [x for x in dirty if _dirty_line_path(x) not in gen]
    is_dirty = len(dirty_source) > 0

    if git_status != "OK":
        # F5 (round 32): a git-status acquisition that is not OK cannot be reported as clean; the tree
        # state is unknown and the package must block.
        kind = "git_status_unavailable"
        summary = f"git status is {git_status} — the working-tree state cannot be trusted"
    elif not has_commits_val:
        kind = "unknown"
        summary = "No commits — fresh git init or degraded metadata"
    elif is_main and not is_dirty:
        kind = "clean_commit"
        summary = f"Clean main at {commit[:12]}"
    elif is_main and is_dirty:
        kind = "dirty_working_tree"
        summary = f"Dirty working tree on main ({len(dirty_source)} changed file(s))"
    elif not is_main and not is_dirty:
        kind = "feature_branch"
        summary = f"Feature branch {branch} at {commit[:12]}"
    else:
        kind = "dirty_working_tree"
        summary = f"Dirty feature branch {branch} ({len(dirty_source)} changed file(s))"

    return {
        "kind": kind,
        "branch": branch,
        "commit": commit,
        "dirty_files": dirty_source,
        "dirty_file_count_total": len(dirty_source),
        "dirty_files_truncated": False,
        "packaging_generated_outputs": packaging_outputs,
        "has_untracked_files": has_untracked,
        "has_commits": has_commits_val,
        "degraded_metadata": (not has_commits_val) or git_status != "OK",
        "git_status": git_status,
        "human_summary": summary,
    }


def _extract_review_state() -> dict:
    lr_path = ".agent/live_review.md"
    plan_path = ".agent/plan.md"

    verdict = "absent"
    open_findings: list[str] = []
    builder_handoff_present = False

    if os.path.isfile(lr_path):
        try:
            with open(lr_path) as f:
                full_content = f.read()
            blocks = re.split(r"\n---\n+(?=# Live Review)", full_content)
            content = blocks[0] if blocks else full_content

            verdict_match = re.search(
                r"##\s+Verdict\s+\(reviewer-owned\)\s*\n\s*\*?\*?([A-Z_]+)\*?\*?",
                content,
            )
            if verdict_match:
                verdict = verdict_match.group(1).strip("*").strip()
            elif "pending" in content[:500].lower():
                verdict = "PENDING"

            for m in re.finditer(
                r"###\s+(R-\d+)\s+.*?\n.*?(?=\n###|\n---|\Z)",
                content, re.DOTALL,
            ):
                block = m.group(0)
                finding_id = m.group(1)
                if "**Resolved" not in block and "resolved" not in block.lower()[:200]:
                    open_findings.append(finding_id)

            builder_handoff_present = "## Builder Handoff" in content
        except OSError:
            pass

    plan_step_range = ""
    plan_goal_present = False
    if os.path.isfile(plan_path):
        try:
            with open(plan_path) as f:
                plan_content = f.read()
            step_match = re.search(r"Steps?\s+(\d+\s*[-–]\s*\d+)", plan_content)
            if step_match:
                plan_step_range = step_match.group(1).replace("–", "-").strip()
            plan_goal_present = "## Goal" in plan_content
        except OSError:
            pass

    review_ready = (
        verdict == "PASS"
        and len(open_findings) == 0
        and builder_handoff_present
    )

    return {
        "latest_live_review_verdict": verdict,
        "open_findings": open_findings,
        "builder_handoff_present": builder_handoff_present,
        "review_ready": review_ready,
        "review_state_source": lr_path if os.path.isfile(lr_path) else "missing",
        "plan_step_range": plan_step_range,
        "plan_goal_present": plan_goal_present,
    }


def _scan_task_runs(ev) -> list[dict]:
    ev = _as_view(ev)
    if not ev.isdir("task_runs"):
        return []
    result = []
    for entry in ev.listdir("task_runs"):
        td = f"task_runs/{entry}"
        if not ev.isdir(td):
            continue
        info: dict = {
            "task": entry,
            "prompt_trace": ev.status(f"{td}/prompt_trace.jsonl"),
            "prompt_trace_summary": ev.status(f"{td}/prompt_trace_summary.json"),
            "review": ev.status(f"{td}/review.json"),
            "repair_loop": ev.status(f"{td}/repair_loop.json"),
            "token_accounting": ev.status(f"{td}/token_accounting.json"),
            "provider_evidence": ev.status(f"{td}/provider_evidence.json"),
            "manual_repair_provenance": ev.status(f"{td}/manual_repair_provenance.json"),
            "is_manual_repair": ev.isfile(f"{td}/manual_repair_provenance.json"),
        }
        result.append(info)
    return result


def _read_job_id(ev: _EvidenceView) -> str:
    """Job ID from provider-flow evidence, else from the bundle manifest.

    ``job_flow.json`` is intentionally absent for an operator-attested manual
    completion, so falling back to ``manifest.json`` is what keeps the shared
    manifest from reporting an empty Job ID for a perfectly valid bundle.
    """
    ev = _as_view(ev)
    job_id = str(ev.read_json("job_flow.json").get("job_id") or "")
    if job_id:
        return job_id
    job_id = str(ev.read_json("manifest.json").get("job_id") or "")
    if job_id:
        return job_id
    return str(ev.read_json("final_job_review.json").get("job_id") or "")


def _read_final_audit(ev: _EvidenceView) -> dict:
    """Final audit from provider-flow evidence, else the manual-completion verdict.

    No provider observability artifact is fabricated: for a manual completion the
    status comes from the verifier/review artifacts that actually exist.
    """
    ev = _as_view(ev)
    audit = ev.read_json("job_flow.json").get("final_audit")
    if isinstance(audit, dict) and audit:
        return audit

    fv = ev.read_json("final_verifier_report.json")
    status = str(fv.get("verdict") or "")
    source = "final_verifier_report.json"
    if not status:
        status = str(ev.read_json("final_job_review.json").get("verdict") or "")
        source = "final_job_review.json"
    if not status:
        return {}
    return {
        "status": status,
        "source": source,
        "missing_observability_artifacts": [],
    }


def _read_trace_sources(ev) -> list[str]:
    ev = _as_view(ev)
    data = ev.read_json("agent_run_trace_summary.json")
    return data.get("trace_sources", []) if isinstance(data, dict) else []


REQUIRED_ROOT_ARTIFACTS = [
    "job_flow.json",
    "manifest.json",
    "agent_run_trace.jsonl",
    "agent_run_trace_summary.json",
    "prompt_trace_summary.json",
    "command_transcript.json",
]

REQUIRED_TASK_ARTIFACTS = [
    "prompt_trace.jsonl",
    "prompt_trace_summary.json",
    "review.json",
    "repair_loop.json",
    "token_accounting.json",
    "provider_evidence.json",
]

MANUAL_REPAIR_EXEMPT_ARTIFACTS = frozenset({
    "prompt_trace.jsonl",
    "prompt_trace_summary.json",
    "provider_evidence.json",
    "repair_loop.json",
})

# Provider-flow-only root artifacts that a deterministic manual-only completion
# legitimately does not produce. They are marked not-applicable — never
# fabricated — when a valid operator-attested completion contract is present.
MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS = frozenset({
    "job_flow.json",
    "agent_run_trace.jsonl",
    "agent_run_trace_summary.json",
    "command_transcript.json",
})


def _mc_read_json(ev: _EvidenceView, rel: str) -> dict:
    """Read a JSON object from the Evidence view, or {} if absent/invalid."""
    return ev.read_json(rel)


# F2 (round 29): the complete pre-consumption shape contract for manual-completion Evidence. Every
# trust-bearing collection/record field consumed by validate_manual_completion and its _verify_*
# helpers is validated ONCE, up front, before any iteration or ``.get`` chain — a wrong inner type
# appends a bounded ``<artifact>: <field> is not a <kind>`` error and normalizes to a safe empty, so
# no downstream code operates on an unvalidated collection and no AttributeError/TypeError escapes.
_MC_LIST = "list"           #: a JSON array
_MC_DICT = "dict"           #: a JSON object
_MC_LISTDICT = "listdict"   #: an array whose every element is an object
_MC_DICTLIST = "dictlist"   #: an object whose every value is an array

#: keyed by artifact BASENAME (task artifacts share the basename of their root counterpart).
_MC_SHAPES: dict[str, dict[str, str]] = {
    "manifest.json": {"task_ids": _MC_LIST},
    "final_job_review.json": {
        "linked_prior_job_ids": _MC_LIST, "linked_prior_job_summaries": _MC_LISTDICT,
        "per_task_changed_files": _MC_DICTLIST, "actual_changed_files": _MC_LIST,
        "expected_changed_files": _MC_LIST},
    "current_change_content_proof.json": {"file_hashes": _MC_DICT, "tombstones": _MC_DICT},
    "final_verifier_report.json": {
        "authoritative_changed_files": _MC_LIST, "test_status": _MC_DICT,
        "review_subject_uncovered_files": _MC_LIST, "content_hash_mismatches": _MC_LIST},
    "change_provenance_gate.json": {
        "covered_files": _MC_LIST, "hash_mismatches": _MC_LIST, "uncovered_files": _MC_LIST},
    "manual_repair_provenance.json": {
        "changed_files": _MC_LIST, "task_scoped_files": _MC_LIST,
        "untracked_file_hashes": _MC_LISTDICT},
    "review_scope_packet.json": {"changed_files": _MC_LIST},
    "review_commit_chain.json": {"commits": _MC_LISTDICT},
    "review_subject.json": {"commits": _MC_LISTDICT, "files": _MC_LISTDICT},
}


def _mc_coerce(errors: list, artifact: str, field: str, value, kind: str):
    if kind == _MC_LIST:
        if not isinstance(value, list):
            errors.append(f"{artifact}: {field} is not a list"); return []
        return value
    if kind == _MC_DICT:
        if not isinstance(value, dict):
            errors.append(f"{artifact}: {field} is not an object"); return {}
        return value
    if kind == _MC_LISTDICT:
        if not isinstance(value, list):
            errors.append(f"{artifact}: {field} is not a list"); return []
        clean = []
        for i, el in enumerate(value):
            if isinstance(el, dict):
                clean.append(el)
            else:
                errors.append(f"{artifact}: {field}[{i}] is not an object")
        return clean
    if kind == _MC_DICTLIST:
        if not isinstance(value, dict):
            errors.append(f"{artifact}: {field} is not an object"); return {}
        out = {}
        for k, v in value.items():
            if isinstance(v, list):
                out[str(k)] = v
            else:
                errors.append(f"{artifact}: {field}[{k!r}] is not a list"); out[str(k)] = []
        return out
    return value


def _read_mc(ev: _EvidenceView, rel: str, errors: list) -> dict:
    """Read a manual-completion artifact and normalize every consumed structured field to its
    validated type, appending an error (which invalidates the candidate) for any wrong type."""
    data = _mc_read_json(ev, rel)
    spec = _MC_SHAPES.get(rel.rsplit("/", 1)[-1], {})
    for field, kind in spec.items():
        if field in data:
            data[field] = _mc_coerce(errors, rel, field, data[field], kind)
    return data


def _mc_task_dirs(ev: _EvidenceView) -> list[str]:
    if not ev.isdir("task_runs"):
        return []
    return [e for e in ev.listdir("task_runs") if ev.isdir(f"task_runs/{e}")]


def _mc_norm(p: str) -> str:
    p = str(p or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    if p.startswith(("a/", "b/")):
        p = p[2:]
    return p


def _is_sha256(v) -> bool:
    return isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v.lower())


def _all_task_runs_manual(ev: _EvidenceView) -> bool:
    """True when every task_run has a valid manual_repair_provenance."""
    task_dirs = _mc_task_dirs(ev)
    if not task_dirs:
        return False
    for entry in task_dirs:
        mrp = _mc_read_json(ev, f"task_runs/{entry}/manual_repair_provenance.json")
        if not (mrp.get("manual_operator_repair") is True and mrp.get("no_provider_calls") is True):
            return False
    return True


def _has_any_manual_claim(ev) -> bool:
    """Round 40 F1: detect ANY manual-completion claim anywhere in the bundle.

    If any authoritative artifact claims manual_operator_repair, operator_attested_complete,
    or manual completion, the entire bundle must satisfy the canonical manual-completion
    contract. A bundle cannot masquerade as non-manual when any part claims manual."""
    ev = _as_view(ev)
    fjr = _mc_read_json(ev, "final_job_review.json")
    if fjr.get("completion_mode") == "manual_operator_repair":
        return True
    for tid in _mc_task_dirs(ev):
        tm = _mc_read_json(ev, f"task_runs/{tid}/manifest.json")
        if tm.get("completion_mode") == "manual_operator_repair":
            return True
        if tm.get("effective_status") == "operator_attested_complete":
            return True
        pe = _mc_read_json(ev, f"task_runs/{tid}/provider_evidence.json")
        if pe.get("execution_mode") == "manual_operator_repair":
            return True
    fv = _mc_read_json(ev, "final_verifier_report.json")
    if fv.get("manual_completion") is True:
        return True
    ec = _mc_read_json(ev, "execution_config.json")
    if ec.get("builder_model") == "operator" and ec.get("reviewer_model") == "operator":
        return True
    return False


def _is_manual_completion(ev) -> bool:
    """A manual-only completion candidate: the final job review declares the
    manual completion mode AND every task run carries manual provenance. No
    bespoke root artifact — detection rides existing artifacts only."""
    ev = _as_view(ev)
    fjr = _mc_read_json(ev, "final_job_review.json")
    if fjr.get("completion_mode") != "manual_operator_repair":
        return False
    return _all_task_runs_manual(ev)


def _verify_review_subject_records(ev: _EvidenceView, subject: dict, base: str) -> list:
    """F4 (round 16): the packager RECOMPUTES the whole review subject and holds the artifact to it.

    The final package trusted `review_subject.json` — the Evidence job's own account of what it
    was a review of. A forged tombstone hash, a rewritten rename origin, or a status flipped from
    `added` to `modified` therefore travelled straight into a READY package: the one artifact that
    says WHAT is under review was the one artifact nobody recomputed.

    So the subject is resolved again here, from the recorded base, and compared record by record:
    path, old_path, status, base_sha256, current_sha256 and file kind.
    """
    ev = _as_view(ev)
    errors: list = []
    try:
        from packages.orchestration.review_subject import (
            resolve_review_subject,
            validate_review_subject_schema,
            validate_subject_path_kinds,
        )
    except Exception as exc:
        return [f"cannot recompute the review subject: {str(exc)[:120]}"]

    # F7 (round 17): the artifact must be an EXACT schema before it is trusted — unknown top-level
    # or file fields, a wrong subject_v, a forged/missing link_target, or an unsafe path all block.
    # A packager that ignores unknown fields would ship an injected `secret`/`path` field untouched.
    errors.extend(validate_review_subject_schema(subject))
    # The embedded commit list must equal the commit chain's — a forged commits[] here cannot
    # disagree with the recomputed chain.
    chain = _read_mc(ev, "review_commit_chain.json", errors)
    subj_commits = [str(c.get("commit") or "") for c in (subject.get("commits") or [])]
    chain_commits = [str(c.get("commit") or "") for c in (chain.get("commits") or [])]
    if subj_commits != chain_commits:
        errors.append("review_subject.commits does not equal review_commit_chain.commits")
    for cf in ("base_commit", "head_commit"):
        if str(subject.get(cf) or "") != str(chain.get(cf) or ""):
            errors.append(f"review_subject.json {cf} disagrees with review_commit_chain.json")

    try:
        # The base is the one the package DECLARES; passing it explicitly is the whole point of
        # F6 — the packager may run from anywhere.
        recomputed = resolve_review_subject(".", base)
    except Exception as exc:
        return [f"cannot recompute the review subject: {str(exc)[:160]}"]

    errors.extend(validate_subject_path_kinds(recomputed, "."))

    def _key(rec: dict) -> tuple:
        # F5 (round 18): the COMPLETE ReviewFileV1 record — every field, so a forged link_target,
        # base_kind, base_mode or current_mode cannot survive recomputation. The round-17 key
        # omitted exactly those four, so a symlink retyped as a regular file (with matching
        # path/status/hash) passed.
        return (
            _mc_norm(str(rec.get("path") or "")),
            str(rec.get("status") or ""),
            "" if rec.get("old_path") in (None, "") else _mc_norm(str(rec.get("old_path"))),
            "" if rec.get("base_sha256") in (None, "") else str(rec.get("base_sha256")),
            "" if rec.get("current_sha256") in (None, "") else str(rec.get("current_sha256")),
            str(rec.get("kind") or "regular"),
            "" if rec.get("link_target") is None else str(rec.get("link_target")),
            "" if rec.get("base_kind") is None else str(rec.get("base_kind")),
            str(rec.get("base_mode") or ""),
            str(rec.get("current_mode") or ""),
        )

    # F3 (round 23): the packaging build writes its own artifacts into the repo root
    # (`.review_zip_manifest.json`, a `remedy-review-*` output). Those are build outputs, never a
    # source change, so they must not pollute the review-subject recomputation the coordinator runs
    # AFTER the manifest exists. (The ArchivePlan classifies them EXCLUDE_SAFE_CONTEXT.)
    def _is_build_output(rec: dict) -> bool:
        p = _mc_norm(str(rec.get("path") or ""))
        base = p.rsplit("/", 1)[-1]
        return base == ".review_zip_manifest.json" or base.startswith("remedy-review-")

    recorded = sorted(_key(f) for f in (subject.get("files") or [])
                      if not _is_build_output(f))
    fresh = sorted(_key(f.to_json()) for f in recomputed.files
                   if not _is_build_output(f.to_json()))
    if recorded != fresh:
        only_rec = [r for r in recorded if r not in fresh]
        only_new = [r for r in fresh if r not in recorded]
        if only_rec:
            errors.append(
                f"review_subject.json records file facts the repository does not confirm: "
                f"{only_rec[:3]}")
        if only_new:
            errors.append(
                f"the repository shows file facts review_subject.json does not record: "
                f"{only_new[:3]}")
    return errors


def _verify_commit_patches(ev: _EvidenceView, actual: list) -> list:
    """F7 (round 16): exactly one canonical patch artifact per commit, recomputed here.

    The chain recorded `patch_sha256` and shipped nothing to hash it against, so the one field
    that says what a commit DID was the one field a ZIP-only reviewer could not check. The
    packager now recomputes the bytes from the repository, holds the packaged file to them, and
    refuses a missing, extra or tampered patch.
    """
    import hashlib as _h

    ev = _as_view(ev)
    errors: list = []
    try:
        from packages.orchestration.review_subject import (
            COMMIT_PATCH_DIRNAME,
            commit_patch_bytes,
            commit_patch_filename,
        )
    except Exception as exc:
        return [f"cannot verify commit patches: {str(exc)[:120]}"]

    if not actual:
        return errors
    if not ev.isdir(COMMIT_PATCH_DIRNAME):
        return [f"the packaged evidence carries no {COMMIT_PATCH_DIRNAME}/ for its "
                f"{len(actual)} commit(s)"]

    expected_names = set()
    for c in actual:
        name = commit_patch_filename(c.commit)
        expected_names.add(name)
        packaged = ev.read_bytes(f"{COMMIT_PATCH_DIRNAME}/{name}")
        if packaged is None:
            errors.append(f"commit {c.commit[:12]} has no packaged patch artifact")
            continue
        want = commit_patch_bytes(".", c.commit)
        if packaged != want:
            errors.append(
                f"packaged patch for commit {c.commit[:12]} is not the repository's patch bytes")
        got = _h.sha256(packaged).hexdigest()
        if got != c.patch_sha256:
            errors.append(
                f"packaged patch for commit {c.commit[:12]} hashes to {got[:12]}, but the chain "
                f"records {c.patch_sha256[:12]}")

    present = {n for n in ev.listdir(COMMIT_PATCH_DIRNAME) if n.endswith(".patch")}
    for extra in sorted(present - expected_names):
        errors.append(f"{COMMIT_PATCH_DIRNAME}/ carries {extra!r}, which no chain commit names")
    if len(present) != len(actual):
        errors.append(
            f"{COMMIT_PATCH_DIRNAME}/ holds {len(present)} patch file(s) for {len(actual)} "
            f"commit(s)")
    return errors


def _verify_commit_chain(ev: _EvidenceView, per_task_union: set) -> list:
    """Round 15 (F7): the packaged commit history is recomputed, not narrated.

    The operator's handoff used to say "there were six commits" in prose. A reader could not check
    that, could not tell whether an unrelated commit had been swept in, and could not tell whether
    the packaged history actually ends at the reviewed HEAD. So the chain is an artifact, and this
    recomputes it from the repository and holds the artifact to it.
    """
    ev = _as_view(ev)
    errors: list = []
    chain = _read_mc(ev, "review_commit_chain.json", errors)
    subject = _read_mc(ev, "review_subject.json", errors)
    if not chain and not subject:
        return errors                     # no declared base: the legacy dirty-tree subject
    base = str(chain.get("base_commit") or "")
    head = str(chain.get("head_commit") or "")
    if not base:
        return errors                     # nothing was declared; nothing to verify

    if subject:
        if str(subject.get("base_commit") or "") != base:
            errors.append("review_commit_chain base_commit disagrees with review_subject")
        if str(subject.get("head_commit") or "") != head:
            errors.append("review_commit_chain head_commit disagrees with review_subject")
        if subject.get("base_is_ancestor") is not True:
            errors.append("review_subject does not record the base as an ancestor of HEAD")

    try:
        from packages.orchestration.review_subject import resolve_commit_chain
        actual = resolve_commit_chain(".", base, head)
    except Exception as exc:                       # unreadable repo/base: say so, never assume
        errors.append(f"cannot recompute the commit chain: {str(exc)[:160]}")
        return errors

    recorded = chain.get("commits") or []
    if len(recorded) != len(actual):
        errors.append(
            f"review_commit_chain records {len(recorded)} commit(s); the repository's "
            f"{base[:12]}..{head[:12]} ancestry path has {len(actual)}")
        return errors
    # F3 (round 16): EVERY recorded field is recomputed. The chain used to compare only
    # commit/tree/patch_sha256/parents, so `subject` and `changed_files` — the two fields a human
    # reader actually reads — were narrative that nothing checked. Reproduced: subject rewritten
    # to "FORGED SUBJECT" and changed_files replaced with ["fake.py"], and verification returned
    # no problems at all.
    if int(chain.get("chain_v") or 0) != 1:
        errors.append(
            f"review_commit_chain declares an unsupported chain_v {chain.get('chain_v')!r} "
            f"(this build reads 1)")
    for rec, act in zip(recorded, actual):
        for field in ("commit", "tree", "patch_sha256", "subject"):
            if str(rec.get(field) or "") != getattr(act, field):
                errors.append(
                    f"review_commit_chain commit {str(rec.get('commit'))[:12]} {field} does not "
                    f"match the repository")
        if [str(x) for x in (rec.get("parents") or [])] != list(act.parents):
            errors.append(
                f"review_commit_chain commit {act.commit[:12]} parents do not match")
        rec_files = [str(x) for x in (rec.get("changed_files") or [])]
        if rec_files != sorted(rec_files):
            errors.append(
                f"review_commit_chain commit {act.commit[:12]} changed_files is not canonically "
                f"sorted")
        if len(set(rec_files)) != len(rec_files):
            errors.append(
                f"review_commit_chain commit {act.commit[:12]} changed_files repeats a path")
        if rec_files != list(act.changed_files):
            errors.append(
                f"review_commit_chain commit {act.commit[:12]} changed_files does not match the "
                f"repository")
    if actual and actual[-1].commit != head:
        errors.append("the packaged commit chain does not end at the review head")
    if actual and base not in actual[0].parents:
        errors.append("the packaged commit chain does not start after the declared base")

    errors.extend(_verify_commit_patches(ev, actual))
    errors.extend(_verify_review_subject_records(ev, subject, base))

    # Every COMMITTED file in the review subject must be explained by one of these commits: the
    # subject cannot claim a committed change that no packaged commit made.
    #
    # The check is deliberately one-directional. The commit union is legitimately a SUPERSET
    # whenever a file is changed and then REVERTED inside the range: the commits touched it, the
    # net base..HEAD delta does not contain it, and that is honest history rather than "work the
    # review does not account for". Requiring equality flagged exactly that case.
    from packages.orchestration.final_verifier import _is_source_for_alignment

    union_committed = {_mc_norm(f) for c in actual for f in c.changed_files}
    subject_files = {_mc_norm(f.get("path", "")) for f in (subject.get("files") or [])
                     if f.get("status") != "dirty"}
    unexplained = sorted({f for f in subject_files if _is_source_for_alignment(f)}
                         - union_committed)
    if unexplained:
        errors.append(
            f"the review subject claims committed changes no packaged commit made: {unexplained}")
    return errors


def _verify_task_provenance_integrity(
    ev: _EvidenceView, tid: str, mrp: dict, proof: dict, fjr: dict,
) -> list[str]:
    """Finding 1: recompute and verify every provenance hash for one task.

    Nothing is trusted at face value: the safe.diff content is re-hashed, the
    provenance and tracked-diff hashes are recomputed from the recorded inputs
    via the SHARED canonical implementation, the safe.diff paths must match every
    changed-file view, and each untracked entry is cross-checked against the
    current content proof.
    """
    errors: list[str] = []
    if not _CANON_AVAILABLE:
        return [f"{tid}: canonical provenance-hash implementation unavailable"]

    safe_content = ev.read_text(f"task_runs/{tid}/safe.diff")
    if safe_content is None:
        return [f"{tid}: safe.diff unreadable"]

    # 8: empty / whitespace-only safe.diff is rejected.
    if not safe_content.strip():
        errors.append(f"{tid}: safe.diff is empty")

    untracked = mrp.get("untracked_file_hashes") or []
    tracked_sha = str(mrp.get("tracked_diff_sha256") or "")

    # F2 (round 29): each untracked entry is a record consumed by the canonical provenance producer
    # (which subscripts uf['path']/['sha256']/['size_bytes']). Validate the record fields BEFORE that
    # producer runs, so a well-typed list carrying a malformed entry is a bounded validation error,
    # never a KeyError from inside repair_attest.
    bad_untracked = False
    for i, uf in enumerate(untracked):
        if not isinstance(uf.get("path"), str) or not uf.get("path"):
            errors.append(f"{tid}: untracked_file_hashes[{i}].path is not a non-empty string")
            bad_untracked = True
        if not isinstance(uf.get("sha256"), str):
            errors.append(f"{tid}: untracked_file_hashes[{i}].sha256 is not a string")
            bad_untracked = True
        if not isinstance(uf.get("size_bytes"), int) or isinstance(uf.get("size_bytes"), bool):
            errors.append(f"{tid}: untracked_file_hashes[{i}].size_bytes is not an integer")
            bad_untracked = True
    if bad_untracked:
        return errors                                      # do not feed malformed records to the producer

    # 1: the emitted safe.diff must hash to the recorded safe_diff_sha256.
    actual_safe_sha = _canon_sha256_text(safe_content)
    if actual_safe_sha != str(mrp.get("safe_diff_sha256") or ""):
        errors.append(f"{tid}: safe_diff_sha256 mismatch (safe.diff modified)")

    # 4/2: provenance hash recomputed from tracked-diff hash + untracked entries.
    recomputed_prov = _canon_provenance_sha256(tracked_sha, untracked)
    if recomputed_prov != str(mrp.get("provenance_sha256") or ""):
        errors.append(f"{tid}: provenance_sha256 does not match recomputed value")
    if recomputed_prov != str(mrp.get("diff_sha256") or ""):
        errors.append(f"{tid}: diff_sha256 does not match recomputed provenance")

    # 2: tracked_diff_sha256 must equal the hash of the tracked portion of
    #    safe.diff (safe.diff = tracked_diff + untracked headers).
    suffix = _canon_safe_diff_text("", untracked)
    if suffix and safe_content.endswith(suffix):
        tracked_portion = safe_content[: len(safe_content) - len(suffix)]
    elif not suffix:
        tracked_portion = safe_content
    else:
        tracked_portion = None
        errors.append(f"{tid}: safe.diff untracked headers do not match provenance")
    if tracked_portion is not None:
        if _canon_sha256_text(tracked_portion) != tracked_sha:
            errors.append(f"{tid}: tracked_diff_sha256 does not match safe.diff content")

    # 5/6: exact path equality across every changed-file view.
    diff_paths = set(_canon_parse_safe_diff_paths(safe_content))
    changed = {_mc_norm(f) for f in (mrp.get("changed_files") or [])}
    scoped = {_mc_norm(f) for f in (mrp.get("task_scoped_files") or [])}
    rsp = _read_mc(ev, f"task_runs/{tid}/review_scope_packet.json", errors)
    rsp_files = {_mc_norm(f) for f in (rsp.get("changed_files") or [])}
    fjr_task = {_mc_norm(f) for f in ((fjr.get("per_task_changed_files") or {}).get(tid) or [])}
    diff_paths_n = {_mc_norm(f) for f in diff_paths}
    for label, s in (
        ("provenance.changed_files", changed),
        ("provenance.task_scoped_files", scoped),
        ("review_scope.changed_files", rsp_files),
        ("final_job_review.per_task_changed_files", fjr_task),
    ):
        if s != diff_paths_n:
            errors.append(
                f"{tid}: safe.diff paths != {label} "
                f"(only_in_diff={sorted(diff_paths_n - s)} only_in_view={sorted(s - diff_paths_n)})"
            )

    # 7: each untracked entry — unique path, valid sha matching the content
    #    proof, non-negative size, path within the task changed set.
    proof_hashes = proof.get("file_hashes") or {}
    proof_norm = {_mc_norm(k): v for k, v in proof_hashes.items()}
    seen_paths: set[str] = set()
    for uf in untracked:
        p = _mc_norm(uf.get("path", ""))
        sha = uf.get("sha256", "")
        size = uf.get("size_bytes", -1)
        if p in seen_paths:
            errors.append(f"{tid}: untracked path {p!r} appears more than once")
        seen_paths.add(p)
        if not _is_sha256(sha):
            errors.append(f"{tid}: untracked {p!r} has an invalid sha256")
        elif p in proof_norm and proof_norm[p] != sha:
            errors.append(f"{tid}: untracked {p!r} sha256 disagrees with content proof")
        if not isinstance(size, int) or size < 0:
            errors.append(f"{tid}: untracked {p!r} has a negative/invalid size")
        if p not in changed:
            errors.append(f"{tid}: untracked {p!r} is not in the task changed set")

    return errors


def validate_manual_completion(ev) -> list[str]:
    """Strictly and independently validate a manual-only completion candidate.

    Returns a list of human-readable errors; empty means authoritative. Every
    condition below is checked independently so any single tampering (a flag, a
    call count, a task id, a changed-file set, the changed-file union, a root
    test exit code / failure count, a content-proof hash, the job id, a
    provenance hash, or task overlap) invalidates the candidate.
    """
    ev = _as_view(ev)
    errors: list[str] = []
    manifest = _read_mc(ev, "manifest.json", errors)
    fjr = _read_mc(ev, "final_job_review.json", errors)
    proof = _read_mc(ev, "current_change_content_proof.json", errors)
    fv = _read_mc(ev, "final_verifier_report.json", errors)
    cp = _read_mc(ev, "change_provenance_gate.json", errors)
    vt = _mc_read_json(ev, "verification_tests.json")

    package_job_id = str(manifest.get("job_id") or "")
    planned_task_ids = [str(t) for t in (manifest.get("task_ids") or [])]
    task_dirs = _mc_task_dirs(ev)

    # 14 + planned-task coverage: package job id must equal the completion job id
    # and every planned task must have exactly one task run.
    fjr_job_id = str(fjr.get("job_id") or "")
    if not package_job_id:
        errors.append("manifest.json: job_id is empty")
    if fjr_job_id != package_job_id:
        errors.append(f"job_id mismatch: manifest={package_job_id!r} final_job_review={fjr_job_id!r}")
    if planned_task_ids and sorted(task_dirs) != sorted(planned_task_ids):
        errors.append(f"task runs {sorted(task_dirs)} != planned tasks {sorted(planned_task_ids)}")

    # F3 (round 31): manifest.task_count is a real integer (never bool) equal to len(task_ids), and the
    # planned task ids equal the actual task directories (bound above) and the final review's ids.
    tc = manifest.get("task_count")
    if not (isinstance(tc, int) and not isinstance(tc, bool)):
        errors.append("manifest.json: task_count is not an integer")
    elif tc != len(planned_task_ids):
        errors.append(f"manifest.json: task_count {tc} != len(task_ids) {len(planned_task_ids)}")
    fjr_ptcf = fjr.get("per_task_changed_files")
    if isinstance(fjr_ptcf, dict) and sorted(str(k) for k in fjr_ptcf) != sorted(planned_task_ids):
        errors.append("final_job_review.per_task_changed_files task ids != manifest task_ids")

    # completion facts on the existing final job review
    if fjr.get("completion_mode") != "manual_operator_repair":
        errors.append("final_job_review.completion_mode != manual_operator_repair")
    if fjr.get("human_final_reviewer_required") is not True:
        errors.append("final_job_review.human_final_reviewer_required is not true")
    # F3 (round 31): completion_provider_call_count is a real integer 0 (a boolean False is not 0).
    _cpcc = fjr.get("completion_provider_call_count")
    if not (isinstance(_cpcc, int) and not isinstance(_cpcc, bool)) or _cpcc != 0:
        errors.append("final_job_review.completion_provider_call_count is not integer 0")

    # Finding 7: the linked prior-job summaries must match the linked ids exactly
    # (an honest historical record, never a fabricated call count).
    linked_ids = [str(x) for x in (fjr.get("linked_prior_job_ids") or [])]
    summaries = fjr.get("linked_prior_job_summaries") or []
    summary_ids = [str(s.get("job_id")) for s in summaries if isinstance(s, dict)]
    if sorted(summary_ids) != sorted(linked_ids):
        errors.append(
            f"linked_prior_job_summaries ids {sorted(summary_ids)} != "
            f"linked_prior_job_ids {sorted(linked_ids)}"
        )
    for s in summaries:
        if not isinstance(s, dict):
            continue
        # F3 (round 32): provider_call_count may be null (unknown) but, when present, must be a real
        # integer — a string "0" (or a boolean) is a forged/untyped historical count and blocks.
        if "provider_call_count" not in s:
            errors.append(f"linked job {s.get('job_id')!r} summary missing provider_call_count")
        else:
            _pcc = s.get("provider_call_count")
            if _pcc is not None and not (isinstance(_pcc, int) and not isinstance(_pcc, bool)):
                errors.append(
                    f"linked job {s.get('job_id')!r} summary provider_call_count is not an integer/null")
        if not s.get("status") or not isinstance(s.get("status"), str):
            errors.append(f"linked job {s.get('job_id')!r} summary status is not a nonempty string")

    # per-task attestation validity + union of changed files
    per_task_union: set[str] = set()
    overlap_owner: dict[str, str] = {}
    for tid in task_dirs:
        rv = _read_mc(ev, f"task_runs/{tid}/review.json", errors)
        pe = _read_mc(ev, f"task_runs/{tid}/provider_evidence.json", errors)
        mrp = _read_mc(ev, f"task_runs/{tid}/manual_repair_provenance.json", errors)
        safe_diff_rel = f"task_runs/{tid}/safe.diff"

        if str(rv.get("final_verdict") or rv.get("verdict") or "") != "operator_attested":
            errors.append(f"{tid}: review verdict is not operator_attested")
        if rv.get("human_final_reviewer_required") is not True:
            errors.append(f"{tid}: review.human_final_reviewer_required is not true")

        if pe.get("execution_mode") != "manual_operator_repair":
            errors.append(f"{tid}: provider_evidence.execution_mode != manual_operator_repair")
        # F3 (round 31): provider/completion call counts are real integer 0 (a boolean is not 0), the
        # actual/prompt-trace availability flags are exactly False (not the string "false" or 999).
        for _pf in ("provider_call_count", "completion_provider_call_count"):
            if _pf in pe:
                _v = pe.get(_pf)
                if not (isinstance(_v, int) and not isinstance(_v, bool)) or _v != 0:
                    errors.append(f"{tid}: provider_evidence.{_pf} is not integer 0")
        if pe.get("actual_provider_available") is not False:
            errors.append(f"{tid}: provider_evidence.actual_provider_available is not false")
        if pe.get("prompt_trace_available") is not False:
            errors.append(f"{tid}: provider_evidence.prompt_trace_available is not false")
        _ta = _read_mc(ev, f"task_runs/{tid}/token_accounting.json", errors)
        if _ta.get("kind") != "manual" or _ta.get("reason") != "manual":
            errors.append(f"{tid}: token_accounting kind/reason are not both 'manual'")
        _tacc = _ta.get("provider_call_count")
        if not (isinstance(_tacc, int) and not isinstance(_tacc, bool)) or _tacc != 0:
            errors.append(f"{tid}: token_accounting.provider_call_count is not integer 0")

        if mrp.get("manual_operator_repair") is not True:
            errors.append(f"{tid}: provenance manual_operator_repair is not true")
        if mrp.get("no_provider_calls") is not True:
            errors.append(f"{tid}: provenance no_provider_calls is not true")
        if str(mrp.get("job_id") or "") != package_job_id:
            errors.append(f"{tid}: provenance job_id != package job id")
        if str(mrp.get("task_id") or "") != tid:
            errors.append(f"{tid}: provenance task_id mismatch")
        if not str(mrp.get("note") or "").strip():
            errors.append(f"{tid}: provenance note is empty")
        for hf in ("provenance_sha256", "diff_sha256", "tracked_diff_sha256"):
            if not _is_sha256(mrp.get(hf)):
                errors.append(f"{tid}: provenance {hf} is not a valid sha256")
        if not ev.isfile(safe_diff_rel):
            errors.append(f"{tid}: safe.diff missing")

        changed = [_mc_norm(f) for f in (mrp.get("changed_files") or [])]
        if not changed:
            errors.append(f"{tid}: provenance changed_files is empty")
        for f in changed:
            if f in overlap_owner:
                errors.append(f"file {f!r} owned by both {overlap_owner[f]} and {tid} (overlap)")
            else:
                overlap_owner[f] = tid
            per_task_union.add(f)

        # ---- Finding 1: actually RECOMPUTE and verify every provenance hash,
        #      the safe.diff content, its paths, and the untracked entries. ----
        errors.extend(_verify_task_provenance_integrity(ev, tid, mrp, proof, fjr))

        # ---- Finding 5: a task manifest may not claim evidence unavailable
        #      without an explicit effective operator-attested completion state.
        tm = _read_mc(ev, f"task_runs/{tid}/manifest.json", errors)
        if (tm.get("evidence_available") is not True
                and tm.get("effective_status") != "operator_attested_complete"):
            errors.append(
                f"{tid}: task manifest shows evidence unavailable without an "
                "effective operator-attested completion state"
            )

    # 7: union must exactly equal every authoritative changed-file view.
    fjr_actual = {_mc_norm(f) for f in (fjr.get("actual_changed_files") or [])}
    fjr_expected = {_mc_norm(f) for f in (fjr.get("expected_changed_files") or [])}
    # Round 15 (F4): a DELETED path is proven by its tombstone (its base_sha256), not by a
    # current hash it cannot have. Counting only file_hashes would report a real, proven
    # part of the change as an uncovered file.
    proof_files = {_mc_norm(f) for f in (proof.get("file_hashes") or {})}
    proof_files |= {_mc_norm(f) for f in (proof.get("tombstones") or {})}
    fv_auth = {_mc_norm(f) for f in (fv.get("authoritative_changed_files") or [])}
    cp_covered = {_mc_norm(f) for f in (cp.get("covered_files") or [])}
    for label, s in (
        ("final_job_review.actual_changed_files", fjr_actual),
        ("final_job_review.expected_changed_files", fjr_expected),
        ("current_change_content_proof.file_hashes", proof_files),
        ("final_verifier.authoritative_changed_files", fv_auth),
        ("change_provenance.covered_files", cp_covered),
    ):
        if s != per_task_union:
            errors.append(
                f"changed-file union mismatch vs {label}: "
                f"only_in_union={sorted(per_task_union - s)} only_in_{label.split('.')[0]}={sorted(s - per_task_union)}"
            )

    # 7b: the packaged commit chain is recomputed and verified against the review subject.
    errors.extend(_verify_commit_chain(ev, per_task_union))

    # 8 (round 26, F3): root verification is STRICTLY validated, fail-closed and NO int() coercion —
    # a string "9999" passed count, a missing record, or a runs/total mismatch all block.
    vt_problems, _ = validate_verification_tests(vt if vt else None)
    errors.extend(vt_problems)

    # F2 (round 31): token_truth.json is trust-bearing (the final verifier derives the entire
    # token_status from it). When claimed present it must be a valid, nonempty, coherent object;
    # empty/whitespace/malformed/wrong-root/enum-violating token truth blocks.
    if ev.isfile("token_truth.json"):
        try:
            from packages.orchestration.token_authority import validate_token_truth
            tt_raw = ev.read_json_strict("token_truth.json")
        except Exception as exc:
            errors.append(f"token_truth.json is not valid strict JSON: {str(exc)[:120]}")
        else:
            errors.extend(validate_token_truth(tt_raw))

    # FVR manual-completion coherence: when the bundle is manual the FVR must agree.
    if fv.get("manual_completion") is not True:
        errors.append("final_verifier_report.manual_completion is not true for a manual bundle")
    if fv.get("human_final_reviewer_required") is not True:
        errors.append("final_verifier_report.human_final_reviewer_required is not true for a manual bundle")
    fv_oat = fv.get("operator_attested_tasks") or []
    if sorted(str(t) for t in fv_oat) != sorted(task_dirs):
        errors.append(
            f"final_verifier_report.operator_attested_tasks {sorted(str(t) for t in fv_oat)} "
            f"!= task dirs {sorted(task_dirs)}")

    # 9-12: alignment / uncovered / hash mismatches / missing proofs (final verifier + gates).
    if fv.get("file_set_alignment_status") not in ("PASS", "PASS_WITH_RISKS"):
        errors.append(f"file_set_alignment_status={fv.get('file_set_alignment_status')}")
    if fv.get("review_subject_uncovered_files"):
        errors.append(f"uncovered files: {fv.get('review_subject_uncovered_files')}")
    if fv.get("content_hash_mismatches"):
        errors.append(f"final verifier content hash mismatches: {fv.get('content_hash_mismatches')}")
    if cp.get("hash_mismatches"):
        errors.append(f"change provenance hash mismatches: {cp.get('hash_mismatches')}")
    if cp.get("uncovered_files"):
        errors.append(f"change provenance uncovered files: {cp.get('uncovered_files')}")
    if not proof_files:
        errors.append("current_change_content_proof.json has no file hashes (missing proofs)")

    return errors


def _read_evidence_gate(ev: _EvidenceView, filename: str) -> dict:
    """Read a gate JSON from the Evidence view, or {} if absent/invalid."""
    return ev.read_json(filename)


def _read_fresh_evidence_gate(ev: _EvidenceView) -> dict:
    return _read_evidence_gate(ev, "fresh_evidence_gate.json")


#: F1 (round 22): the EXACT READY gate matrix. READY_FOR_REVIEW is possible only when EVERY required
#: gate passes, decoded from exactly the packaged bytes. commit_execution_gate=NEEDS_HUMAN_APPROVAL
#: is expected and nonblocking. A missing/invalid/unknown/blocking/contradictory gate BLOCKS.
_VERDICT_GATES = {
    "final_verifier_report.json": {"PASS", "PASS_WITH_RISKS"},
    "fresh_evidence_gate.json": {"PASS"},
    "artifact_contract_gate.json": {"PASS"},
    "change_provenance_gate.json": {"PASS"},
    "runtime_integration_gate.json": {"PASS"},
}
_OK_GATES = ("manifest_integrity.json", "postmortem_integrity.json")
_COMMIT_GATE = "commit_execution_gate.json"
_ALL_READY_GATES = tuple(_VERDICT_GATES) + _OK_GATES + (_COMMIT_GATE,)

#: F1 (round 23): every READY gate's schema is version-closed.
_SUPPORTED_GATE_VERSIONS = frozenset({"1.0.0", "1.1.0"})
_MISSING = object()

#: F1 (round 24): the CLOSED allowed-field set of every READY gate — an unknown field blocks.
_GATE_ALLOWED_FIELDS = {
    "final_verifier_report.json": frozenset({
        "also_needs_repair", "artifact_contract_gate", "authoritative_changed_files",
        "change_provenance", "change_provenance_gate", "change_source_mismatches", "changed_files",
        "changed_line_ranges", "commit_execution_gate", "content_hash_mismatches",
        "evidence_completeness", "execution_mode_blocked", "execution_mode_by_task",
        "execution_mode_findings", "file_set_alignment_status", "final_job_review_blocked",
        "final_job_review_findings", "final_job_review_verdict", "fresh_evidence_gate",
        "human_final_reviewer_required", "invocation_args_warnings", "manifest_integrity_blocked",
        "manual_completion", "missing_evidence", "missing_tests_gate", "model_mismatch_blocked",
        "model_mismatch_warnings", "model_needs_repair", "operator_attested_tasks",
        "postmortem_failures", "postmortem_integrity_blocked", "recommended_action",
        "report_badges", "review_subject_uncovered_files", "runtime_integration_gate",
        "schema_version", "scratch_file_guard", "spec_compliance", "sticky_binding_by_task",
        "sticky_binding_warnings", "test_status", "token_actual_summary", "token_cost_has_critical",
        "token_cost_policy_present", "token_cost_risk_findings", "token_measurement",
        "token_measurement_confidence", "token_measurement_note", "token_status",
        "unresolved_findings", "verdict"}),
    "fresh_evidence_gate.json": frozenset({
        "current_job_id", "current_step_range", "evidence_authoritative", "evidence_freshness",
        "evidence_job_id", "evidence_validity", "issues", "job_id_match", "live_review_match",
        "live_review_step_range", "plan_match", "plan_step_range", "schema_version", "verdict"}),
    "artifact_contract_gate.json": frozenset({
        "critical_fv_missing", "evidence_job_id", "fv_referenced_missing", "issues", "job_id_fresh",
        "missing_required", "optional_artifacts", "required_artifacts", "schema_version",
        "stream_artifacts", "verdict", "worktree_artifacts"}),
    "change_provenance_gate.json": frozenset({
        "content_hash_verified", "covered_files", "current_hashes", "current_job_id", "dirty_files",
        "evidence_covered_files", "evidence_hashes", "evidence_sources", "excluded_files",
        "hash_mismatches", "issues", "schema_version", "source_files", "stale_apply_proofs",
        "uncovered_files", "verdict"}),
    "runtime_integration_gate.json": frozenset({
        "checks", "checks_passed", "checks_total", "feature_id", "issues", "schema_version",
        "verdict"}),
    "manifest_integrity.json": frozenset({"failures", "notes", "ok", "schema_version"}),
    "postmortem_integrity.json": frozenset({"failures", "ok", "schema_version"}),
    "commit_execution_gate.json": frozenset({
        "blocked_gates", "gate_checks", "issues", "non_pass_gates", "promote_ready",
        "schema_version", "verdict"}),
}
_RUNTIME_STATIC_CHECK_FIELDS = frozenset({"check_id", "check_type", "file_missing", "found",
                                          "pattern", "source_file"})
_RUNTIME_BINDING_REQUIRED_FIELDS = frozenset({"check_id", "check_type", "test_file", "min_passed",
                                               "found"})
_RUNTIME_BINDING_OPTIONAL_FIELDS = frozenset({"bound_run", "critical_node_ids"})
_RUNTIME_BOUND_RUN_REQUIRED = frozenset({"run_id", "command", "exit_code", "passed", "failed",
                                          "skipped", "selected", "node_ids", "output_hash",
                                          "head_sha"})
_RUNTIME_BOUND_RUN_OPTIONAL = frozenset({"deselected", "duration_seconds"})
_RUNTIME_CHECK_TYPES = frozenset({"call_exists", "test_execution_binding"})
#: The FV's OWN commit-readiness view (distinct from the packaged commit gate's verdict); a
#: pre-acceptance package must never claim it is auto-promotable.
_FV_COMMIT_NOT_READY = frozenset({"BLOCKED", "NEEDS_HUMAN_APPROVAL", "NEEDS_APPROVAL",
                                  "NEEDS_REPAIR", "NEEDS_TESTS"})

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")
_MAX_KEY_LEN = 256
#: F3 (round 25): a KEY whose NAME looks like a credential is refused even without a value — the
#: shared value scanner only flags `key=value`/PEM payloads, but a map keyed by `aws_secret_access_key`
#: is itself a leak. Gate map keys are only file paths / task ids / artifact / gate names, so a
#: credential-shaped key is never legitimate.
_CREDENTIAL_KEY_RE = re.compile(
    r"(secret|password|passwd|api[_-]?key|access[_-]?key|private[_-]?key|credential|"
    r"auth[_-]?token|bearer|aws_secret)", re.IGNORECASE)


# ---- F1/F3 (round 25): typed RECURSIVE gate schemas — an unknown NESTED field, a wrong element
# type, or a dynamic-map key that violates its grammar all BLOCK. Value SEMANTICS (equality with a
# PASS gate) stay in _gate_semantic_problems; this layer pins STRUCTURE + dynamic-key safety. ----
class _Node:
    """Base schema node. Subclasses type a trusted value EXACTLY — there is no accept-anything node
    (F1, round 26): every scalar, list element, nested object and dynamic-map value is typed."""
    def check(self, v, path, name):
        return []


class _Scalar(_Node):
    def __init__(self, py, label):
        self.py, self.label = py, label

    def check(self, v, path, name):
        # bool is an int/float subclass — reject it unless bool is explicitly acceptable.
        allows_bool = self.py is bool or (isinstance(self.py, tuple) and bool in self.py)
        if isinstance(v, bool) and not allows_bool:
            return [f"{name} {path} is a bool, expected {self.label}"]
        return [] if isinstance(v, self.py) else [f"{name} {path} is not {self.label}"]


class _Obj(_Node):
    """A closed object: unknown field blocks; every REQUIRED field must be present; optional fields
    are explicitly documented; each present field is typed (F2, round 26)."""
    def __init__(self, fields, *, optional=frozenset()):
        self.fields = fields
        self.optional = frozenset(optional)
        self.required = frozenset(fields) - self.optional

    def check(self, v, path, name):
        if not isinstance(v, dict):
            return [f"{name} {path} is not an object"]
        problems = []
        extra = set(v) - set(self.fields)
        if extra:
            problems.append(f"{name} {path} has unknown field(s) {sorted(extra)} (schema is closed)")
        missing = self.required - set(v)
        if missing:
            problems.append(f"{name} {path} is missing required field(s) {sorted(missing)}")
        for k, node in self.fields.items():
            if k in v:
                problems.extend(node.check(v[k], f"{path}.{k}" if path else k, name))
        return problems


class _Map(_Node):
    """A dynamic-key map: every KEY must satisfy its typed grammar; every value its node."""
    def __init__(self, key_kind, value):
        self.key_kind, self.value = key_kind, value

    def check(self, v, path, name):
        if not isinstance(v, dict):
            return [f"{name} {path} is not an object"]
        problems = []
        for k, val in v.items():
            if not _valid_dynamic_key(self.key_kind, k):
                problems.append(f"{name} {path} key {k!r} violates the {self.key_kind} grammar")
            problems.extend(self.value.check(val, f"{path}[{k!r}]", name))
        return problems


class _Arr(_Node):
    def __init__(self, elem):
        self.elem = elem

    def check(self, v, path, name):
        if not isinstance(v, list):
            return [f"{name} {path} is not a list"]
        problems = []
        for i, e in enumerate(v):
            problems.extend(self.elem.check(e, f"{path}[{i}]", name))
        return problems


class _Nullable(_Node):
    """A value that is EITHER JSON null OR the wrapped node — the explicit nullable union that
    replaces every ANY on a field the producer may legitimately emit as null (F1, round 26)."""
    def __init__(self, node):
        self.node = node

    def check(self, v, path, name):
        return [] if v is None else self.node.check(v, path, name)


class _OneOf(_Node):
    """A value that must satisfy AT LEAST ONE of the alternative nodes — no catch-all."""
    def __init__(self, *nodes):
        self.nodes = nodes

    def check(self, v, path, name):
        for node in self.nodes:
            if not node.check(v, path, name):
                return []
        return [f"{name} {path} matches none of the allowed shapes"]


BOOL = _Scalar(bool, "a bool")
INT = _Scalar(int, "an integer")
STR = _Scalar(str, "a string")
NUM = _Scalar((int, float), "a number")
_NINT, _NSTR, _NBOOL, _NNUM = _Nullable(INT), _Nullable(STR), _Nullable(BOOL), _Nullable(NUM)
_NSTRLIST = _Nullable(_Arr(STR))
#: An exact closed placeholder for a finding/warning list element: a message string OR an empty
#: structured record (a READY package requires these lists empty, and a populated arbitrary object
#: is refused — F1 round 26 removed the ANY catch-all here).
_FINDING = _OneOf(STR, _Obj({}))
#: The exact content-hash-mismatch record shape.
_HASH_MISMATCH = _Obj({"file": STR, "expected": STR, "actual": STR})
_MODELS = _Obj({"builder": _NSTR, "reviewer": _NSTR})


def _valid_dynamic_key(kind: str, key) -> bool:
    if not isinstance(key, str) or not key or len(key) > _MAX_KEY_LEN:
        return False
    if kind == "task_id":
        return bool(_SAFE_TASK_ID_RE.fullmatch(key))
    if kind == "gate_name":
        return key in _COMMIT_CHECK_TO_GATE
    if kind in ("repo_path", "artifact_name"):
        return _safe_rel_path(key)
    return True                                            # generic str key (still metadata-scanned)


#: F1/F2 (round 26): the token blocks are TWO distinct exact shapes (token_status carries the
#: estimate/trace fields; token_measurement carries measurement_note + actual_summary).
_TOKEN_STATUS = _Obj({
    "actual_available": _NBOOL, "actual_call_count": INT, "actual_completion_tokens": _NINT,
    "actual_coverage_complete": BOOL, "actual_missing_reasons": _NSTRLIST,
    "actual_model_verified": BOOL, "actual_models": _MODELS, "actual_prompt_tokens": _NINT,
    "actual_total_tokens": _NINT, "builder_estimated_total": INT, "cli_version": _NSTR,
    "configured_models": _MODELS, "cost_call_count": INT, "cost_coverage_complete": BOOL,
    "cost_coverage_reason": _NSTR, "estimated_completion_tokens": INT, "estimated_prompt_tokens": INT,
    "estimated_total_tokens": INT, "measurement_confidence": STR, "measurement_source": STR,
    "missing_reason": _NSTR, "prompt_trace_count": INT, "provider_call_count": INT,
    "repair_estimated_total": INT, "reviewer_estimated_total": INT, "total_cost_usd": _NNUM})
#: F1 (round 27): the EXACT real ``actual_summary`` shape emitted by
#: final_verifier._token_measurement_summary for high/mixed confidence. Every field the producer
#: builds is required; each is typed by the token_status field it copies (mostly nullable). Reused
#: for both token_measurement.actual_summary AND the top-level token_actual_summary — a null is
#: accepted where the producer legitimately emits null (low/unavailable confidence), and an unknown
#: field or wrong scalar type still blocks.
_ACTUAL_TOKEN_SUMMARY = _Obj({
    "measurement_confidence": STR, "measurement_source": STR,
    "actual_prompt_tokens": _NINT, "actual_completion_tokens": _NINT, "actual_total_tokens": _NINT,
    "total_cost_usd": _NNUM, "cost_call_count": INT, "cost_coverage_complete": BOOL,
    "cost_coverage_reason": _NSTR, "provider_call_count": INT, "actual_call_count": INT,
    "actual_coverage_complete": BOOL, "actual_missing_reasons": _NSTRLIST, "cli_version": _NSTR,
    "configured_models": _MODELS, "actual_models": _MODELS, "actual_model_verified": BOOL})
_TOKEN_MEASUREMENT = _Obj({
    "actual_call_count": INT, "actual_coverage_complete": BOOL, "actual_missing_reasons": _NSTRLIST,
    "actual_model_verified": BOOL, "actual_models": _MODELS,
    "actual_summary": _Nullable(_ACTUAL_TOKEN_SUMMARY),
    "cli_version": _NSTR, "configured_models": _MODELS, "cost_call_count": INT,
    "cost_coverage_complete": BOOL, "cost_coverage_reason": _NSTR, "measurement_confidence": STR,
    "measurement_note": _Nullable(STR), "measurement_source": STR, "provider_call_count": INT,
    "total_cost_usd": _NNUM})

def _token_producer_problems(name: str, gate: dict) -> list[str]:
    """F1 (round 29): the token_measurement block and its top-level projections must be REPRODUCIBLE
    from token_status by the ONE shared producer. Round 28 kept a hand-duplicated projection-field
    list, so a derived field the list did not name (measurement_note, actual_summary presence) could
    drift: high confidence with a null summary, low confidence with a fabricated summary, or an
    arbitrary matching note all passed. Now the gate rebuilds the expected block with the real
    producer and requires exact deep equality — no field list to drift."""
    ts = gate.get("token_status")
    tm = gate.get("token_measurement")
    if not isinstance(ts, dict) or not isinstance(tm, dict):
        return []                                          # a non-object is caught by the schema
    try:
        from packages.orchestration.token_measurement import token_measurement_summary
    except Exception as exc:                               # pragma: no cover - import guard
        return [f"{name}: cannot reconstruct token_measurement: {str(exc)[:120]}"]
    expected = token_measurement_summary(ts)
    problems: list[str] = []
    if tm != expected:
        problems.append(
            f"{name} token_measurement is not reproducible from token_status via the producer "
            f"(expected measurement_note/actual_summary and every copied field to match)")
    # The top-level projections must equal the SAME producer output, so a forged top-level view
    # cannot differ from the nested block or from what the producer would derive.
    if gate.get("token_measurement_confidence") != expected["measurement_confidence"]:
        problems.append(f"{name} token_measurement_confidence != producer measurement_confidence")
    if gate.get("token_measurement_note") != expected["measurement_note"]:
        problems.append(f"{name} token_measurement_note != producer measurement_note")
    if gate.get("token_actual_summary") != expected["actual_summary"]:
        problems.append(f"{name} token_actual_summary != producer actual_summary")
    return problems


_STREAM_SECTION = _Obj({
    "applicable": BOOL, "verdict": STR, "tasks_with_stream_evidence": _Arr(STR),
    "artifacts_verified": INT, "artifacts_present": INT,
    "missing_stream_artifact_listing": _Arr(_FINDING), "missing_stream_artifacts": _Arr(_FINDING),
    "missing_stream_artifact_metadata": _Arr(_FINDING),
    "stream_artifact_hash_mismatches": _Arr(_FINDING), "stream_artifact_size_mismatches": _Arr(_FINDING),
    "unexpected_stream_artifacts": _Arr(_FINDING), "duplicate_stream_artifact_refs": _Arr(_FINDING),
    "unsafe_stream_artifact_refs": _Arr(_FINDING)})
_WORKTREE_SECTION = _Obj({
    "applicable": BOOL, "verdict": STR, "job_level_handoff": BOOL, "handoff_coverage_verdict": STR,
    "handoff_coverage_issues": _Arr(_FINDING), "missing_job_handoff": _Arr(_FINDING),
    "worktree_tasks": _Arr(_FINDING), "diffs_verified": INT, "missing_result_diffs": _Arr(_FINDING),
    "missing_result_diff_references": _Arr(_FINDING), "result_diff_hash_mismatches": _Arr(_FINDING),
    "result_diff_size_mismatches": _Arr(_FINDING), "unreferenced_result_diffs": _Arr(_FINDING),
    "unsafe_result_diff_refs": _Arr(_FINDING)})

#: F1/F2 (round 26): the COMPLETE recursive schema for every gate — fully typed (no ANY), with
#: required fields enforced. Derived from the real producer's emitted shape.
_GATE_SCHEMA = {
    "final_verifier_report.json": _Obj({
        "schema_version": STR, "verdict": STR, "also_needs_repair": BOOL,
        "artifact_contract_gate": STR, "change_provenance_gate": STR, "fresh_evidence_gate": STR,
        "runtime_integration_gate": STR, "commit_execution_gate": STR, "change_provenance": STR,
        "spec_compliance": STR, "scratch_file_guard": STR, "missing_tests_gate": STR,
        "file_set_alignment_status": STR, "final_job_review_verdict": STR, "recommended_action": STR,
        "authoritative_changed_files": _Arr(STR), "changed_files": _Arr(STR),
        "changed_line_ranges": _Map("repo_path", _Arr(_Arr(INT))),
        "change_source_mismatches": _Arr(_FINDING), "content_hash_mismatches": _Arr(_HASH_MISMATCH),
        "review_subject_uncovered_files": _Arr(STR), "postmortem_failures": _Arr(_FINDING),
        "unresolved_findings": _Arr(_FINDING), "missing_evidence": _Arr(STR),
        "execution_mode_findings": _Arr(_FINDING), "final_job_review_findings": _Arr(_FINDING),
        "invocation_args_warnings": _Arr(STR), "model_mismatch_warnings": _Arr(STR),
        "sticky_binding_warnings": _Arr(_FINDING), "token_cost_risk_findings": _Arr(_FINDING),
        "report_badges": _Arr(STR), "operator_attested_tasks": _Arr(STR),
        "test_status": _Obj({"ran": BOOL, "passed": INT, "failed": INT}),
        "evidence_completeness": _Obj({
            "review_scope_packet": BOOL, "spec_compliance_check": BOOL, "missing_tests_gate": BOOL,
            "scratch_file_guard": BOOL, "token_truth": BOOL, "safe_diff": BOOL, "review_json": BOOL,
            "tests_txt": BOOL}),
        "execution_mode_by_task": _Map("task_id", STR),
        "sticky_binding_by_task": _Map("task_id", BOOL),
        "manual_completion": BOOL, "human_final_reviewer_required": BOOL,
        "postmortem_integrity_blocked": BOOL, "manifest_integrity_blocked": BOOL,
        "final_job_review_blocked": BOOL, "execution_mode_blocked": BOOL,
        "model_mismatch_blocked": BOOL, "model_needs_repair": BOOL,
        "token_cost_has_critical": BOOL, "token_cost_policy_present": BOOL,
        "token_status": _TOKEN_STATUS, "token_measurement": _TOKEN_MEASUREMENT,
        "token_measurement_confidence": STR, "token_measurement_note": _Nullable(STR),
        "token_actual_summary": _Nullable(_ACTUAL_TOKEN_SUMMARY)}),
    "fresh_evidence_gate.json": _Obj({
        "schema_version": STR, "verdict": STR, "evidence_job_id": STR, "current_job_id": STR,
        "current_step_range": STR, "live_review_step_range": STR, "plan_step_range": STR,
        "job_id_match": BOOL, "live_review_match": BOOL, "plan_match": BOOL,
        "evidence_authoritative": BOOL,
        "evidence_freshness": _Obj({"is_fresh": BOOL, "job_id_match": BOOL, "step_range_match": BOOL}),
        "evidence_validity": _Obj({"is_valid_current_run": BOOL, "has_job_id": BOOL,
                                   "has_manifest": BOOL}),
        "issues": _Arr(STR)}),
    "artifact_contract_gate.json": _Obj({
        "schema_version": STR, "verdict": STR, "evidence_job_id": STR, "job_id_fresh": BOOL,
        "required_artifacts": _Map("artifact_name", BOOL),
        "optional_artifacts": _Map("artifact_name", BOOL),
        "missing_required": _Arr(STR), "fv_referenced_missing": _Arr(STR),
        "critical_fv_missing": _Arr(STR), "issues": _Arr(STR),
        "stream_artifacts": _STREAM_SECTION, "worktree_artifacts": _WORKTREE_SECTION}),
    "change_provenance_gate.json": _Obj({
        "schema_version": STR, "verdict": STR, "current_job_id": STR,
        "covered_files": _Arr(STR), "source_files": _Arr(STR), "excluded_files": _Arr(STR),
        "evidence_covered_files": _Arr(STR), "evidence_sources": _Arr(STR), "dirty_files": _Arr(STR),
        "uncovered_files": _Arr(STR), "stale_apply_proofs": _Arr(_FINDING),
        "hash_mismatches": _Arr(_HASH_MISMATCH),
        "issues": _Arr(STR), "current_hashes": _Map("repo_path", STR),
        "evidence_hashes": _Map("repo_path", STR), "content_hash_verified": BOOL}),
    "runtime_integration_gate.json": _Obj({
        "schema_version": STR, "verdict": STR, "checks": _Arr(_OneOf(
            _Obj({"check_id": STR, "check_type": STR, "file_missing": BOOL, "found": BOOL,
                  "pattern": STR, "source_file": STR}),
            _Obj({"check_id": STR, "check_type": STR, "test_file": STR, "min_passed": INT,
                  "found": BOOL, "bound_run": _Obj({
                      "run_id": STR, "command": STR, "exit_code": INT, "passed": INT, "failed": INT,
                      "skipped": INT, "selected": INT, "node_ids": _Arr(STR),
                      "output_hash": STR, "head_sha": STR},
                      optional={"deselected", "duration_seconds"}),
                  "critical_node_ids": _Arr(STR)},
                 optional={"bound_run", "critical_node_ids"}),
        )), "checks_total": INT, "checks_passed": INT, "issues": _Arr(STR),
        "feature_id": STR},
        optional={"feature_id"}),
    "manifest_integrity.json": _Obj({
        "schema_version": STR, "ok": BOOL, "failures": _Arr(_FINDING), "notes": _Arr(STR)}),
    "postmortem_integrity.json": _Obj({
        "schema_version": STR, "ok": BOOL, "failures": _Arr(_FINDING)}),
    "commit_execution_gate.json": _Obj({
        "schema_version": STR, "verdict": STR, "gate_checks": _Map("gate_name", STR),
        "blocked_gates": _Arr(STR), "non_pass_gates": _Arr(STR), "promote_ready": BOOL,
        "issues": _Arr(STR)}),
}


def _gget(gate: dict, path: str):
    """Dotted lookup; returns _MISSING if any segment is absent."""
    cur = gate
    for seg in path.split("."):
        if not isinstance(cur, dict) or seg not in cur:
            return _MISSING
        cur = cur[seg]
    return cur


def _check_fields(gate: dict, name: str, spec) -> list[str]:
    """Each (dotted_path, expected) must be PRESENT and equal — absence or contradiction blocks."""
    problems: list[str] = []
    for path, expected in spec:
        v = _gget(gate, path)
        if v is _MISSING:
            problems.append(f"{name} is missing {path}")
        elif v != expected:
            problems.append(f"{name} {path}={v!r} contradicts a PASS gate (expected {expected!r})")
    return problems


def _unsafe_text(s: str) -> str | None:
    """Return a reason if a string carries a secret, a local absolute path or a control character."""
    from packages.orchestration.run_manifest import _contains_local_path, _contains_secret
    if _contains_secret(s):
        return "a secret"
    if _contains_local_path(s):
        return "a local absolute path"
    if any(ord(c) < 32 and c not in "\t\n\r" for c in s):
        return "a control character"
    return None


def _scan_gate_metadata(gate, name: str) -> list[str]:
    """F5 (round 24) / F3 (round 25): no trusted gate may carry a secret, a local absolute path or a
    control character in ANY textual field — scan every string value AND every dictionary KEY
    recursively, since an injected map key (e.g. a file-hash keyed by an absolute path) is just as
    dangerous as a value."""
    problems: list[str] = []

    def _walk(value, path):
        if isinstance(value, str):
            r = _unsafe_text(value)
            if r:
                problems.append(f"{name} field {path} carries {r}")
        elif isinstance(value, dict):
            for k, v in value.items():
                if isinstance(k, str):
                    r = _unsafe_text(k)
                    if r:
                        problems.append(f"{name} key {path}.{k!r} carries {r}")
                    elif _CREDENTIAL_KEY_RE.search(k):
                        problems.append(f"{name} key {path}.{k!r} is a credential-like key name")
                    elif len(k) > _MAX_KEY_LEN:
                        problems.append(f"{name} key {path}.{k!r} is implausibly long")
                _walk(v, f"{path}.{k}")
        elif isinstance(value, list):
            for i, v in enumerate(value):
                _walk(v, f"{path}[{i}]")

    _walk(gate, name.replace(".json", ""))
    return problems


def _gate_closed_schema_problems(name: str, gate: dict) -> list[str]:
    """F1 (round 24/25): version-closed + EXACT RECURSIVE typed schema (unknown nested field, wrong
    element type or unsafe dynamic-map key all block) + metadata key/value safety."""
    problems: list[str] = []
    if _gget(gate, "schema_version") not in _SUPPORTED_GATE_VERSIONS:
        problems.append(f"{name} schema_version {gate.get('schema_version')!r} is not supported "
                        f"{sorted(_SUPPORTED_GATE_VERSIONS)}")
    schema = _GATE_SCHEMA.get(name)
    if schema is not None:
        problems.extend(schema.check(gate, "", name))
    problems.extend(_scan_gate_metadata(gate, name))
    return problems


def _artifact_section_problems(gate: dict, name: str, section: str) -> list[str]:
    """F2 (round 25): an applicable stream/worktree section needs COMPLETE PASS semantics; a
    nonapplicable one needs the EXACT NOT_APPLICABLE shape (verdict NOT_APPLICABLE, every list
    empty, every count 0) — a nested BLOCKED verdict under a top-level PASS blocks."""
    s = gate.get(section)
    if not isinstance(s, dict):
        return [f"{name} {section} is not an object"]
    problems: list[str] = []
    applicable = s.get("applicable")
    if applicable is True:
        if s.get("verdict") != "PASS":
            problems.append(f"{name} {section} is applicable but verdict {s.get('verdict')!r} "
                            f"is not PASS")
        for k, v in s.items():
            if isinstance(v, list) and v and (k.startswith("missing") or k.startswith("unexpected")
                                              or k.startswith("unsafe") or k.startswith("unreferenced")
                                              or "mismatch" in k or "duplicate" in k or "issues" in k):
                problems.append(f"{name} {section}.{k} is nonempty ({v!r})")
    else:
        if applicable is not False:
            problems.append(f"{name} {section}.applicable={applicable!r} is not a bool")
        if s.get("verdict") != "NOT_APPLICABLE":
            problems.append(f"{name} {section} verdict {s.get('verdict')!r} != NOT_APPLICABLE")
        for k, v in s.items():
            if isinstance(v, list) and v:
                problems.append(f"{name} {section}.{k} is nonempty for a NOT_APPLICABLE section")
            elif isinstance(v, int) and not isinstance(v, bool) and v != 0:
                problems.append(f"{name} {section}.{k}={v} is nonzero for a NOT_APPLICABLE section")
    return problems


def _change_provenance_coherence(gate: dict, name: str, ctx: dict) -> list[str]:
    """F2 (round 25): the change-provenance set and hash maps must be internally coherent and equal
    the packaged ContentProof authority — the SAME authority the coordinator decodes. A manually
    emptied covered_files or an injected hash (with hash_mismatches=[]) blocks."""
    problems: list[str] = []
    covered = set(gate.get("covered_files") or [])
    source = set(gate.get("source_files") or [])
    excluded = set(gate.get("excluded_files") or [])
    ev_cov = set(gate.get("evidence_covered_files") or [])
    if not covered:
        problems.append(f"{name} covered_files is empty")
    if covered != (source - excluded):
        problems.append(f"{name} covered_files != source_files - excluded_files")
    if covered != ev_cov:
        problems.append(f"{name} covered_files != evidence_covered_files")
    cur = gate.get("current_hashes") if isinstance(gate.get("current_hashes"), dict) else {}
    evh = gate.get("evidence_hashes") if isinstance(gate.get("evidence_hashes"), dict) else {}
    if cur != evh:
        problems.append(f"{name} current_hashes != evidence_hashes")
    if ctx.get("proof_authority") is not None and covered != ctx["proof_authority"]:
        problems.append(f"{name} covered_files != ContentProof authority set")
    if ctx.get("proof_hashes") is not None and cur != ctx["proof_hashes"]:
        problems.append(f"{name} current_hashes != ContentProof file hashes")
    return problems


def _gate_semantic_problems(name: str, gate: dict, verdicts: dict, ctx: dict) -> list[str]:
    """F1/F2/F3 (round 24) + F2 (round 25): the gate's PASS label must be consistent with its
    COMPLETE internal body — every READY-incompatible field is checked — and (final_verifier) its
    embedded gate verdicts must equal the separately packaged gates. ``ctx`` carries the packaged
    ContentProof authority/hashes and the recorded verification total for cross-gate coherence."""
    problems = _gate_closed_schema_problems(name, gate)
    # F6 (round 31): the closed-schema pass MUST complete before any semantic operation. If a field is
    # the wrong type, the gate already blocks — the semantic layer (which does set()/sorted()/
    # membership/arith/.get chains) must NOT then run on the unvalidated value and raise. Return the
    # schema problems and stop; other gates are still evaluated independently by the caller.
    if problems:
        return problems

    if name == "final_verifier_report.json":
        problems.extend(_check_fields(gate, name, [
            ("also_needs_repair", False), ("unresolved_findings", []),
            ("test_status.ran", True), ("test_status.failed", 0), ("missing_tests_gate", "PASS"),
            ("change_source_mismatches", []), ("review_subject_uncovered_files", []),
            ("content_hash_mismatches", []), ("postmortem_failures", []),
            ("postmortem_integrity_blocked", False), ("manifest_integrity_blocked", False),
            # F2 (round 24): the remaining FV blocking fields.
            ("final_job_review_blocked", False), ("execution_mode_blocked", False),
            ("model_mismatch_blocked", False), ("model_needs_repair", False),
            ("missing_evidence", []), ("execution_mode_findings", []),
            ("final_job_review_findings", []),
            # F2 (round 25): the remaining READY-incompatible FV fields.
            ("spec_compliance", "PASS"), ("scratch_file_guard", "PASS"),
            ("change_provenance", "PASS"), ("file_set_alignment_status", "PASS"),
            ("token_cost_has_critical", False), ("token_cost_risk_findings", []),
            ("evidence_completeness.review_scope_packet", True),
            ("evidence_completeness.spec_compliance_check", True),
            ("evidence_completeness.missing_tests_gate", True),
            ("evidence_completeness.scratch_file_guard", True),
            ("evidence_completeness.token_truth", True),
            ("evidence_completeness.safe_diff", True),
            ("evidence_completeness.review_json", True),
            ("evidence_completeness.tests_txt", True)]))
        # F2 (round 25): test_status.passed is a nonnegative integer, coherent with the recorded
        # verification total (so a fabricated PASS count cannot disagree with what actually ran).
        tp = _gget(gate, "test_status.passed")
        if not isinstance(tp, int) or isinstance(tp, bool) or tp < 0:
            problems.append(f"{name} test_status.passed={tp!r} is not a nonnegative integer")
        elif ctx.get("vt_passed") is None:
            # F3 (round 26): fail-closed — a READY final_verifier cannot be confirmed without a
            # strictly-valid VerificationTests total to equal.
            problems.append(f"{name} test_status.passed cannot be confirmed: the VerificationTests "
                            f"total is missing or invalid")
        elif tp != ctx["vt_passed"]:
            problems.append(f"{name} test_status.passed={tp} != recorded verification total "
                            f"{ctx['vt_passed']}")
        # F2: the FV's embedded gate verdicts must EQUAL the separately packaged gate verdicts.
        for emb, gate_file in (("artifact_contract_gate", "artifact_contract_gate.json"),
                               ("change_provenance_gate", "change_provenance_gate.json"),
                               ("fresh_evidence_gate", "fresh_evidence_gate.json"),
                               ("runtime_integration_gate", "runtime_integration_gate.json")):
            ev = gate.get(emb)
            if gate_file in verdicts and ev != verdicts[gate_file]:
                problems.append(f"{name} embedded {emb}={ev!r} != packaged "
                                f"{verdicts[gate_file]!r}")
        # F2: the FV's commit-readiness view (distinct name/meaning from the packaged gate verdict)
        # must not claim an auto-promotable state for a pre-acceptance package.
        ce = gate.get("commit_execution_gate")
        if ce not in _FV_COMMIT_NOT_READY:
            problems.append(f"{name} commit_execution_gate={ce!r} is not a pre-acceptance "
                            f"not-ready state {sorted(_FV_COMMIT_NOT_READY)}")
        # F1 (round 29): the token_measurement block and its top-level projections must be exactly
        # REPRODUCIBLE from token_status by the ONE shared producer. This subsumes the round-27
        # top/nested equality and the round-28 field-list projection: an impossible confidence/summary
        # combination or a drifted note cannot pass, and there is no duplicated list to fall behind
        # the producer.
        problems.extend(_token_producer_problems(name, gate))
        return problems

    if name == "fresh_evidence_gate.json":
        problems.extend(_check_fields(gate, name, [
            ("evidence_authoritative", True), ("job_id_match", True), ("plan_match", True),
            ("live_review_match", True), ("evidence_validity.has_job_id", True),
            ("evidence_validity.has_manifest", True),
            ("evidence_validity.is_valid_current_run", True),
            ("evidence_freshness.is_fresh", True), ("evidence_freshness.job_id_match", True),
            ("evidence_freshness.step_range_match", True), ("issues", [])]))
        # F2 (round 25): the match Booleans cannot be true over UNEQUAL actual values — require the
        # actual ids/ranges to be equal, so a flipped id with job_id_match=true still blocks.
        if gate.get("current_job_id") != gate.get("evidence_job_id"):
            problems.append(f"{name} current_job_id != evidence_job_id "
                            f"({gate.get('current_job_id')!r} vs {gate.get('evidence_job_id')!r})")
        csr = gate.get("current_step_range")
        if csr != gate.get("live_review_step_range") or csr != gate.get("plan_step_range"):
            problems.append(f"{name} step ranges disagree (current={csr!r} "
                            f"live={gate.get('live_review_step_range')!r} "
                            f"plan={gate.get('plan_step_range')!r})")
        return problems

    if name == "artifact_contract_gate.json":
        from packages.orchestration.artifact_contract_gate import CORE_ARTIFACTS
        problems.extend(_check_fields(gate, name, [
            ("missing_required", []), ("fv_referenced_missing", []), ("critical_fv_missing", []),
            ("issues", []), ("job_id_fresh", True)]))
        req = gate.get("required_artifacts")
        if not isinstance(req, dict):
            problems.append(f"{name} required_artifacts is not an object")
        else:
            # F2 (round 25): the EXACT required-artifact key set from the producer's contract; an
            # empty or trimmed map (which trivially satisfies "all true") blocks.
            if set(req) != set(CORE_ARTIFACTS):
                problems.append(f"{name} required_artifacts keys {sorted(req)} != the contract "
                                f"{sorted(CORE_ARTIFACTS)}")
            for k, v in req.items():
                if v is not True:
                    problems.append(f"{name} required_artifacts[{k!r}]={v!r} is not true")
        problems.extend(_artifact_section_problems(gate, name, "stream_artifacts"))
        problems.extend(_artifact_section_problems(gate, name, "worktree_artifacts"))
        return problems

    if name == "change_provenance_gate.json":
        problems.extend(_check_fields(gate, name, [
            ("uncovered_files", []), ("content_hash_verified", True), ("hash_mismatches", []),
            ("stale_apply_proofs", []), ("issues", [])]))
        problems.extend(_change_provenance_coherence(gate, name, ctx))
        return problems

    if name == "runtime_integration_gate.json":
        problems.extend(_check_fields(gate, name, [("issues", [])]))
        checks = gate.get("checks")
        if not isinstance(checks, list):
            problems.append(f"{name} checks is not a list")
        else:
            if len(checks) == 0:
                problems.append(f"{name} checks_total is zero — gate cannot pass with no checks")
            ids: set = set()
            for i, c in enumerate(checks):
                if not isinstance(c, dict):
                    problems.append(f"{name} check[{i}] is not an object")
                    continue
                ct = c.get("check_type")
                if ct == "call_exists":
                    if set(c) != _RUNTIME_STATIC_CHECK_FIELDS:
                        problems.append(f"{name} checks[{i}] has unknown field(s) "
                                        f"{sorted(set(c) - _RUNTIME_STATIC_CHECK_FIELDS)} "
                                        f"(schema is closed)" if set(c) - _RUNTIME_STATIC_CHECK_FIELDS
                                        else f"{name} checks[{i}] is missing required field(s) "
                                        f"{sorted(_RUNTIME_STATIC_CHECK_FIELDS - set(c))}")
                        continue
                    if not _safe_rel_path(c.get("source_file")):
                        problems.append(f"{name} check {c.get('check_id')!r} source_file "
                                        f"is not a safe relative path")
                    if c.get("file_missing") is not False:
                        problems.append(f"{name} check {c.get('check_id')!r} file_missing is not false")
                elif ct == "test_execution_binding":
                    allowed = _RUNTIME_BINDING_REQUIRED_FIELDS | _RUNTIME_BINDING_OPTIONAL_FIELDS
                    extra = set(c) - allowed
                    missing = _RUNTIME_BINDING_REQUIRED_FIELDS - set(c)
                    if extra:
                        problems.append(f"{name} checks[{i}] has unknown field(s) {sorted(extra)}")
                        continue
                    if missing:
                        problems.append(f"{name} checks[{i}] is missing required field(s) "
                                        f"{sorted(missing)}")
                        continue
                    if not isinstance(c.get("test_file"), str) or not c["test_file"]:
                        problems.append(f"{name} check {c.get('check_id')!r} test_file is empty")
                    if not isinstance(c.get("min_passed"), int) or c.get("min_passed", 0) < 1:
                        problems.append(f"{name} check {c.get('check_id')!r} min_passed < 1")
                    br = c.get("bound_run")
                    if c.get("found") is True and br is not None:
                        if isinstance(br, dict):
                            br_extra = set(br) - _RUNTIME_BOUND_RUN_REQUIRED - _RUNTIME_BOUND_RUN_OPTIONAL
                            br_missing = _RUNTIME_BOUND_RUN_REQUIRED - set(br)
                            if br_extra:
                                problems.append(f"{name} checks[{i}].bound_run has unknown field(s) "
                                                f"{sorted(br_extra)}")
                            if br_missing:
                                problems.append(f"{name} checks[{i}].bound_run is missing field(s) "
                                                f"{sorted(br_missing)}")
                            if not br_extra and not br_missing:
                                if not isinstance(br.get("head_sha"), str) or not br["head_sha"]:
                                    problems.append(
                                        f"{name} checks[{i}].bound_run.head_sha is empty")
                                elif ctx.get("review_subject_head") and br["head_sha"] != ctx["review_subject_head"]:
                                    problems.append(
                                        f"{name} checks[{i}].bound_run.head_sha "
                                        f"{br['head_sha']!r} != Review Subject HEAD "
                                        f"{ctx['review_subject_head']!r}")
                                if not isinstance(br.get("output_hash"), str) or not br["output_hash"]:
                                    problems.append(
                                        f"{name} checks[{i}].bound_run.output_hash is empty")
                                elif not re.fullmatch(r"[0-9a-f]{64}", br["output_hash"]):
                                    problems.append(
                                        f"{name} checks[{i}].bound_run.output_hash is not sha256 hex")
                                _mp = c.get("min_passed", 1)
                                _bp = br.get("passed", 0)
                                if isinstance(_mp, int) and isinstance(_bp, int) and _bp < _mp:
                                    problems.append(
                                        f"{name} checks[{i}].bound_run.passed ({_bp}) < "
                                        f"min_passed ({_mp})")
                        else:
                            problems.append(f"{name} checks[{i}].bound_run is not an object")
                else:
                    problems.append(f"{name} check[{i}] check_type {ct!r} is not supported")
                    continue
                cid = c.get("check_id")
                if not isinstance(cid, str) or not cid:
                    problems.append(f"{name} check[{i}] check_id is empty")
                elif cid in ids:
                    problems.append(f"{name} duplicate check_id {cid!r}")
                else:
                    ids.add(cid)
                if c.get("found") is not True:
                    problems.append(f"{name} check {c.get('check_id')!r} found is not true")
            ct, cp = gate.get("checks_total"), gate.get("checks_passed")
            if not (ct == cp == len(checks)):
                problems.append(f"{name} checks_total/checks_passed/len(checks) disagree "
                                f"({ct}/{cp}/{len(checks)})")
        return problems

    if name in _OK_GATES:
        problems.extend(_check_fields(gate, name, [("failures", [])]))
        return problems

    return problems


def _safe_rel_path(p) -> bool:
    if not isinstance(p, str) or not p or p.startswith("/") or "\\" in p or "\0" in p:
        return False
    return not any(seg in ("", "..", ".") for seg in p.split("/"))


_VT_NAME = "verification_tests.json"
_VT_SUPPORTED_VERSIONS = frozenset({"1.0.0", "1.1.0"})
_VT_SUPPORTED_TYPES = frozenset({"explicit_commands"})
_VT_TOP_FIELDS = frozenset({"schema_version", "verification_type", "runs", "command", "exit_code",
                            "passed", "failed", "test_files", "timestamp"})
_VT_RUN_FIELDS_V10 = frozenset({"run_id", "command", "exit_code", "passed", "failed", "test_files",
                                "stdout_summary"})
_VT_RUN_FIELDS_V11 = frozenset({"run_id", "command", "exit_code", "passed", "failed", "test_files",
                                "stdout_summary", "head_sha", "output_hash", "selected",
                                "deselected", "skipped", "node_ids", "duration_seconds"})
_VT_RUN_FIELDS = _VT_RUN_FIELDS_V10
_VT_RUN_ID_RE = re.compile(r"^vr-\d{4,}$")
_VT_MAX_STDOUT = 4000


def _is_real_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _valid_utc_datetime(s) -> bool:
    """F2 (round 28): a real TIMEZONE-AWARE ISO-8601 DATETIME, matching the producer's
    ``datetime.now(timezone.utc).isoformat()``. A date-only value (``2026-07-19``) or a timezone-
    naive datetime is refused — both parse to a ``tzinfo``-less value, so requiring ``tzinfo`` rejects
    them; a ``Z``, ``+00:00`` or explicit offset is accepted."""
    if not isinstance(s, str) or not s.strip():
        return False
    try:
        dt = datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return dt.tzinfo is not None and dt.utcoffset() is not None


def _vt_safe_files(tf, label, problems):
    """A test-file list: strings, safe normalized relative repo paths, sorted, no duplicates."""
    if not isinstance(tf, list) or not all(isinstance(x, str) for x in tf):
        problems.append(f"{_VT_NAME} {label} test_files is not a string list")
        return set()
    for p in tf:
        if not _safe_rel_path(p):
            problems.append(f"{_VT_NAME} {label} test_file {p!r} is not a safe relative path")
    if len(set(tf)) != len(tf):
        problems.append(f"{_VT_NAME} {label} test_files has duplicates")
    if tf != sorted(tf):
        problems.append(f"{_VT_NAME} {label} test_files is not sorted")
    return set(tf)


def validate_verification_tests(vt):
    """F3 (round 26) / F2 (round 27): STRICT, FAIL-CLOSED, FULLY TYPED ``VerificationTestsV1``,
    aligned to the ``job_evidence._run_verifications`` producer. Returns ``(problems, passed)``: an
    empty ``problems`` means the document is exactly a supported, coherent, all-passing record and
    ``passed`` is its authoritative total. No ``int(...)`` coercion; the command/timestamp/run_id/
    stdout_summary are typed; per-run and top counts are nonnegative real integers; test-file lists
    are safe, sorted, duplicate-free; run ids are unique (commands MAY repeat); the top-level
    command/exit_code are the producer-derived views of the runs; and every textual key/value is
    scanned for secrets/local paths/control characters."""
    if vt is None:
        return [f"{_VT_NAME} is missing"], None
    if not isinstance(vt, dict):
        return [f"{_VT_NAME} is not an object"], None
    problems: list[str] = []
    extra = set(vt) - _VT_TOP_FIELDS
    missing = _VT_TOP_FIELDS - set(vt)
    if extra:
        problems.append(f"{_VT_NAME} has unknown field(s) {sorted(extra)}")
    if missing:
        problems.append(f"{_VT_NAME} is missing field(s) {sorted(missing)}")
    if vt.get("schema_version") not in _VT_SUPPORTED_VERSIONS:
        problems.append(f"{_VT_NAME} schema_version {vt.get('schema_version')!r} unsupported")
    if vt.get("verification_type") not in _VT_SUPPORTED_TYPES:
        problems.append(f"{_VT_NAME} verification_type {vt.get('verification_type')!r} unsupported")
    if not isinstance(vt.get("command"), str) or not vt.get("command", "").strip():
        problems.append(f"{_VT_NAME} command is not a nonempty string")
    if not _valid_utc_datetime(vt.get("timestamp")):
        problems.append(f"{_VT_NAME} timestamp {vt.get('timestamp')!r} is not a timezone-aware "
                        f"ISO-8601 datetime")
    for f in ("exit_code", "passed", "failed"):
        if not _is_real_int(vt.get(f)):
            problems.append(f"{_VT_NAME} {f}={vt.get(f)!r} is not a real integer")
    if _is_real_int(vt.get("exit_code")) and vt["exit_code"] != 0:
        problems.append(f"{_VT_NAME} exit_code != 0 ({vt['exit_code']})")
    if _is_real_int(vt.get("failed")) and vt["failed"] != 0:
        problems.append(f"{_VT_NAME} failed != 0 ({vt['failed']})")
    if _is_real_int(vt.get("passed")) and vt["passed"] < 1:
        problems.append(f"{_VT_NAME} passed < 1 ({vt['passed']}) — no test proven")
    # F2 (round 27): every textual key AND value is secret/path/control safe, as for gates.
    problems.extend(_scan_gate_metadata(vt, _VT_NAME))
    runs = vt.get("runs")
    run_files: set = set()
    if not isinstance(runs, list) or not runs:
        problems.append(f"{_VT_NAME} runs is not a nonempty list")
    else:
        sum_p = sum_f = 0
        seen_ids: set = set()
        run_cmds: list = []
        run_exits: list = []
        _vt_ver = vt.get("schema_version", "1.0.0")
        _expected_run_fields = _VT_RUN_FIELDS_V11 if _vt_ver == "1.1.0" else _VT_RUN_FIELDS_V10
        for i, r in enumerate(runs):
            if not isinstance(r, dict) or set(r) != _expected_run_fields:
                problems.append(f"{_VT_NAME} runs[{i}] has the wrong field set")
                continue
            rid = r.get("run_id")
            if not isinstance(rid, str) or not rid.strip() or not _VT_RUN_ID_RE.fullmatch(rid):
                problems.append(f"{_VT_NAME} runs[{i}] run_id {rid!r} is empty or malformed")
            elif rid in seen_ids:
                problems.append(f"{_VT_NAME} duplicate run_id {rid!r}")
            else:
                seen_ids.add(rid)
            cmd = r.get("command")
            # F2 (round 28): a REPEATED command is legitimate (the producer emits two unique runs for
            # the same command) — distinguished by unique run_id. Command text is NOT required unique.
            if not isinstance(cmd, str) or not cmd.strip():
                problems.append(f"{_VT_NAME} runs[{i}] command is empty")
            else:
                run_cmds.append(cmd)
            if _is_real_int(r.get("exit_code")):
                run_exits.append(r["exit_code"])
            if not isinstance(r.get("stdout_summary"), str):
                problems.append(f"{_VT_NAME} runs[{i}] stdout_summary is not a string")
            elif len(r["stdout_summary"]) > _VT_MAX_STDOUT:
                problems.append(f"{_VT_NAME} runs[{i}] stdout_summary is implausibly long")
            for f in ("exit_code", "passed", "failed"):
                if not _is_real_int(r.get(f)):
                    problems.append(f"{_VT_NAME} runs[{i}].{f} is not a real integer")
            if _is_real_int(r.get("exit_code")) and r["exit_code"] != 0:
                problems.append(f"{_VT_NAME} runs[{i}] exit_code != 0")
            if _is_real_int(r.get("failed")) and r["failed"] != 0:
                problems.append(f"{_VT_NAME} runs[{i}] failed != 0")
            if _is_real_int(r.get("passed")) and r["passed"] < 0:
                problems.append(f"{_VT_NAME} runs[{i}] passed is negative ({r['passed']})")
            run_files |= _vt_safe_files(r.get("test_files"), f"runs[{i}]", problems)
            if _vt_ver == "1.1.0":
                if not isinstance(r.get("head_sha"), str) or not r["head_sha"]:
                    problems.append(f"{_VT_NAME} runs[{i}].head_sha is empty")
                if not isinstance(r.get("output_hash"), str) or not re.fullmatch(r"[0-9a-f]{64}", r.get("output_hash", "")):
                    problems.append(f"{_VT_NAME} runs[{i}].output_hash is not sha256 hex")
                for _nf in ("selected", "deselected", "skipped"):
                    if not _is_real_int(r.get(_nf)) or r.get(_nf, -1) < 0:
                        problems.append(f"{_VT_NAME} runs[{i}].{_nf} is not a non-negative integer")
                if not isinstance(r.get("node_ids"), list) or not all(isinstance(n, str) for n in r.get("node_ids", [])):
                    problems.append(f"{_VT_NAME} runs[{i}].node_ids is not a list of strings")
                if not isinstance(r.get("duration_seconds"), (int, float)) or isinstance(r.get("duration_seconds"), bool) or r.get("duration_seconds", -1) < 0:
                    problems.append(f"{_VT_NAME} runs[{i}].duration_seconds is not a non-negative number")
                if all(_is_real_int(r.get(f)) for f in ("selected", "passed", "failed", "skipped")):
                    _expected_sel = r["passed"] + r["failed"] + r["skipped"]
                    if r["selected"] != _expected_sel:
                        problems.append(f"{_VT_NAME} runs[{i}] selected ({r['selected']}) != "
                                        f"passed+failed+skipped ({_expected_sel})")
                if isinstance(r.get("node_ids"), list) and _is_real_int(r.get("selected")):
                    if len(r["node_ids"]) != r["selected"]:
                        problems.append(f"{_VT_NAME} runs[{i}] node_ids count ({len(r['node_ids'])}) != "
                                        f"selected ({r['selected']})")
                if (isinstance(r.get("output_hash"), str)
                        and re.fullmatch(r"[0-9a-f]{64}", r["output_hash"])
                        and isinstance(r.get("stdout_summary"), str)):
                    import hashlib as _hl
                    _expected_hash = _hl.sha256(r["stdout_summary"].encode()).hexdigest()
                    if r["output_hash"] != _expected_hash:
                        problems.append(f"{_VT_NAME} runs[{i}] output_hash does not match "
                                        f"sha256(stdout_summary)")
            if _is_real_int(r.get("passed")):
                sum_p += r["passed"]
            if _is_real_int(r.get("failed")):
                sum_f += r["failed"]
        if not problems:
            if sum_p != vt.get("passed"):
                problems.append(f"{_VT_NAME} passed {vt.get('passed')} != sum of runs {sum_p}")
            if sum_f != vt.get("failed"):
                problems.append(f"{_VT_NAME} failed {vt.get('failed')} != sum of runs {sum_f}")
            # F2 (round 28): the top-level fields are DERIVED from the runs by the exact producer
            # rule — command is the join, exit_code is 0 only when every run exited 0. A forged or
            # reordered top-level command no longer passes.
            derived_command = " && ".join(run_cmds)
            if vt.get("command") != derived_command:
                problems.append(f"{_VT_NAME} command is not the producer-derived join of the run "
                                f"commands")
            derived_exit = 0 if all(e == 0 for e in run_exits) else 1
            if vt.get("exit_code") != derived_exit:
                problems.append(f"{_VT_NAME} exit_code {vt.get('exit_code')!r} != the producer-"
                                f"derived {derived_exit}")
    tf_top = _vt_safe_files(vt.get("test_files"), "top-level", problems)
    if not problems and tf_top != run_files:
        problems.append(f"{_VT_NAME} test_files is not the union of the runs' test_files")
    return problems, (vt.get("passed") if not problems else None)


#: The commit gate's embedded gate_checks keys → the READY-matrix gate file whose verdict must match.
_COMMIT_CHECK_TO_GATE = {
    "final_verifier": "final_verifier_report.json",
    "fresh_evidence_gate": "fresh_evidence_gate.json",
    "artifact_contract_gate": "artifact_contract_gate.json",
    "change_provenance_gate": "change_provenance_gate.json",
    "runtime_integration_gate": "runtime_integration_gate.json",
}
#: The commit-gate writer's hard-block verdict set (build_commit_execution_gate); a gate whose check
#: is one of these appears in blocked_gates and yields a "gate 'x' is BLOCKED" issue.
_COMMIT_HARD_BLOCK = frozenset({"BLOCKED", "NEEDS_TESTS", "NEEDS_REPAIR", ""})


def _validate_commit_gate(gate, verdicts: dict) -> list[str]:
    """F4 (round 24): the commit_execution gate is CHECKED but nonblocking, and it must be an EXACT
    derived document: its gate_checks are exactly the five packaged gate verdicts, non_pass_gates is
    the derived set, blocked_gates is empty, promote_ready is false and the verdict is
    NEEDS_HUMAN_APPROVAL. A missing/invalid/extra/contradictory commit gate blocks Evidence
    integrity, though human approval itself is expected."""
    if gate is None:
        return [f"{_COMMIT_GATE} is missing"]
    if not isinstance(gate, dict):
        return [f"{_COMMIT_GATE} is not an object"]
    problems: list[str] = _gate_closed_schema_problems(_COMMIT_GATE, gate)
    if gate.get("verdict") != "NEEDS_HUMAN_APPROVAL":
        problems.append(f"{_COMMIT_GATE} verdict {gate.get('verdict')!r} != NEEDS_HUMAN_APPROVAL")
    if gate.get("promote_ready") is not False:
        problems.append(f"{_COMMIT_GATE} promote_ready {gate.get('promote_ready')!r} is not false")
    checks = gate.get("gate_checks")
    if not isinstance(checks, dict) or set(checks) != set(_COMMIT_CHECK_TO_GATE):
        problems.append(f"{_COMMIT_GATE} gate_checks keys must be exactly "
                        f"{sorted(_COMMIT_CHECK_TO_GATE)}")
    else:
        for k, gate_file in _COMMIT_CHECK_TO_GATE.items():
            if gate_file in verdicts and checks[k] != verdicts[gate_file]:
                problems.append(f"{_COMMIT_GATE} gate_checks[{k!r}]={checks[k]!r} != packaged "
                                f"{verdicts[gate_file]!r}")
        # F4 (round 25): blocked_gates, non_pass_gates AND issues are ALL exactly derived from
        # gate_checks by the SAME deterministic rule as the commit-gate writer — issue text is not a
        # second source of truth. Any drift (empty or unrelated issues) blocks.
        derived_blocked = sorted(k for k in checks if checks[k] in _COMMIT_HARD_BLOCK)
        derived_non_pass = sorted(k for k in checks if checks[k] != "PASS")
        derived_issues = [f"gate {k!r} is BLOCKED" for k in derived_blocked]
        derived_issues += [f"gate {k!r} is not PASS (verdict {checks[k]!r})"
                           for k in derived_non_pass if k not in derived_blocked]
        if sorted(gate.get("blocked_gates") or []) != derived_blocked:
            problems.append(f"{_COMMIT_GATE} blocked_gates {gate.get('blocked_gates')!r} != "
                            f"the derived {derived_blocked}")
        if sorted(gate.get("non_pass_gates") or []) != derived_non_pass:
            problems.append(f"{_COMMIT_GATE} non_pass_gates {gate.get('non_pass_gates')!r} != "
                            f"the derived {derived_non_pass}")
        if list(gate.get("issues") or []) != derived_issues:
            problems.append(f"{_COMMIT_GATE} issues {gate.get('issues')!r} != the exact derived "
                            f"{derived_issues}")
    return problems


def _safe_gate_semantics(name: str, gate, verdicts: dict, ctx: dict) -> list[str]:
    """F6 (round 31): a total wrapper — the semantic validators run on schema-validated values, but as
    defense in depth ANY unexpected exception becomes a bounded blocking reason so one malformed gate
    can never raise out of ``evaluate_ready_gate_matrix`` and hide the other gates' failures."""
    try:
        return _gate_semantic_problems(name, gate, verdicts, ctx)
    except Exception as exc:                               # pragma: no cover - defensive
        return [f"{name} could not be evaluated ({type(exc).__name__}); it is malformed and blocks"]


def evaluate_ready_gate_matrix(load_json) -> dict:
    """The ONE READY gate evaluation (round 22-24), used by the manifest AND re-run by the archive
    builder on the staged byte map. First pass records every gate's verdict label; second pass runs
    the closed-schema + complete semantic + embedded-equality validators (and the exact commit-gate
    derivation) with all verdicts available. ``load_json(name)`` returns the parsed gate dict,
    ``None`` if absent, and raises on invalid JSON. Returns {ok, gate_verdicts, blocking_reasons}."""
    verdicts: dict[str, str] = {}
    reasons: list[str] = []
    loaded: dict[str, object] = {}

    def _load(name):
        try:
            return load_json(name)
        except Exception as exc:                       # invalid JSON / unreadable
            reasons.append(f"{name} is not valid JSON: {exc}")
            return _MISSING

    # Pass 1 — record every gate's verdict/ok label.
    for name in _VERDICT_GATES:
        g = loaded[name] = _load(name)
        if g is _MISSING:
            verdicts[name] = "INVALID"
        elif g is None:
            verdicts[name] = "MISSING"
        elif isinstance(g, dict) and isinstance(g.get("verdict"), str):
            verdicts[name] = g["verdict"]
        else:
            verdicts[name] = "UNKNOWN"
    for name in _OK_GATES:
        g = loaded[name] = _load(name)
        if g is _MISSING:
            verdicts[name] = "INVALID"
        elif g is None:
            verdicts[name] = "MISSING"
        else:
            verdicts[name] = "ok=true" if (isinstance(g, dict) and g.get("ok") is True) \
                else f"ok={g.get('ok') if isinstance(g, dict) else g!r}"
    cg = loaded[_COMMIT_GATE] = _load(_COMMIT_GATE)
    verdicts[_COMMIT_GATE] = (cg.get("verdict") if isinstance(cg, dict) else "MISSING") \
        if cg not in (_MISSING, None) else ("INVALID" if cg is _MISSING else "MISSING")

    # F2 (round 25): the shared cross-gate context — the packaged ContentProof authority/hashes and
    # the recorded verification total — decoded from the SAME loader so no second authority model
    # exists. A missing/invalid proof leaves the cross-checks off (the coordinator refuses it
    # separately); a present proof binds change-provenance and the FV test total.
    ctx: dict = {"proof_authority": None, "proof_hashes": None, "vt_passed": None,
                 "review_subject_head": None}
    try:
        proof = load_json("current_change_content_proof.json")
        if isinstance(proof, dict):
            fh = proof.get("file_hashes") if isinstance(proof.get("file_hashes"), dict) else {}
            tomb = proof.get("tombstones") if isinstance(proof.get("tombstones"), dict) else {}
            ctx["proof_authority"] = set(fh) | set(tomb)
            ctx["proof_hashes"] = dict(fh)
    except Exception:
        pass                                           # a corrupt proof blocks in the coordinator
    try:
        _rs = load_json("review_subject.json")
        if isinstance(_rs, dict) and isinstance(_rs.get("head_commit"), str):
            ctx["review_subject_head"] = _rs["head_commit"]
    except Exception:
        pass
    # F3 (round 26): the VerificationTests are STRICTLY validated, fail-closed. A present-but-invalid
    # record blocks here; a valid record's ``passed`` is the authoritative total the FV must equal.
    vt_problems: list[str] = []
    try:
        vt_raw = load_json(_VT_NAME)
    except Exception as exc:
        vt_problems = [f"{_VT_NAME} is not valid JSON: {exc}"]
    else:
        # F6 (round 31): the strict VT validator runs on an untrusted value — a malformed record must
        # block, never raise out of the matrix.
        try:
            vt_problems, ctx["vt_passed"] = validate_verification_tests(vt_raw)
        except Exception as exc:                           # pragma: no cover - defensive
            vt_problems = [f"{_VT_NAME} could not be validated ({type(exc).__name__}); it is malformed"]
    ctx["vt_present"] = ctx.get("vt_passed") is not None

    # Pass 2 — validate.
    for name, allowed in _VERDICT_GATES.items():
        g = loaded[name]
        if g is _MISSING:
            continue                                   # JSON error already recorded
        if g is None:
            reasons.append(f"{name} is missing")
            continue
        if not isinstance(g, dict) or "verdict" not in g:
            reasons.append(f"{name} has no verdict (unknown schema)")
            continue
        # F6 (round 31): a non-string verdict (list/dict/...) is not a hashable membership candidate —
        # test the type before ``in allowed`` so a malformed verdict blocks instead of raising.
        if not isinstance(g.get("verdict"), str) or g.get("verdict") not in allowed:
            reasons.append(f"{name} verdict {g.get('verdict')!r} is not in {sorted(allowed)}")
            continue
        reasons.extend(_safe_gate_semantics(name, g, verdicts, ctx))
        # F3 (round 26): a present, valid final_verifier means a READY package is being evaluated —
        # its VerificationTests must be a strictly-valid, all-passing record.
        if name == "final_verifier_report.json":
            reasons.extend(vt_problems)

    for name in _OK_GATES:
        g = loaded[name]
        if g is _MISSING:
            continue
        if g is None:
            reasons.append(f"{name} is missing")
            continue
        if not (isinstance(g, dict) and g.get("ok") is True):
            reasons.append(f"{name} ok is {g.get('ok') if isinstance(g, dict) else g!r}, not true")
            continue
        reasons.extend(_safe_gate_semantics(name, g, verdicts, ctx))

    if cg is None:
        reasons.append(f"{_COMMIT_GATE} is missing")
    elif cg is not _MISSING:
        try:
            reasons.extend(_validate_commit_gate(cg, verdicts))
        except Exception as exc:                           # F6: never raise out of the matrix
            reasons.append(f"{_COMMIT_GATE} could not be evaluated ({type(exc).__name__}); it is "
                           f"malformed and blocks")

    return {"ok": not reasons, "gate_verdicts": verdicts, "blocking_reasons": reasons}


def _evidence_dir_gate_loader(ev: _EvidenceView):
    """A load_json for evaluate_ready_gate_matrix backed by the immutable Evidence view, raising on
    invalid JSON so a corrupt gate BLOCKS rather than silently passing."""
    return ev.gate_loader()


def regenerate_final_verifier(evidence_view) -> tuple[dict | None, str | None]:
    """F1 (round 30/31): the final verifier report is NOT a trusted staged input. Materialize the
    IMMUTABLE Evidence snapshot to a private temp dir and run the REAL current producer over exactly
    those bytes. Returns ``(report, problem)``: a dict report and ``None`` on success, or ``(None,
    reason)`` for a DISTINGUISHED failure — producer unavailable, import/runtime error, materialization
    failure, or a non-object return. A failure is NEVER translated into success; broad exceptions are
    reported, not swallowed into a pass."""
    import shutil as _shutil
    import tempfile as _tempfile

    if evidence_view is None:
        return None, "no Evidence view"
    files = getattr(evidence_view, "_files", None)
    if not files:
        return None, "the Evidence snapshot is empty"
    try:
        from packages.orchestration.final_verifier import build_final_verifier_report
    except ImportError as exc:
        return None, f"the final-verifier producer is unavailable: {str(exc)[:120]}"
    except Exception as exc:                               # any other import-time failure blocks
        return None, f"the final-verifier producer failed to import: {str(exc)[:120]}"
    if not callable(build_final_verifier_report):
        return None, "the final-verifier producer entry point is missing"
    tmp = None
    try:
        tmp = _tempfile.mkdtemp(prefix="remedy_fv_regen_")
        for rel, data in files.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p) or tmp, exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
    except Exception as exc:
        if tmp:
            _shutil.rmtree(tmp, ignore_errors=True)
        return None, f"could not materialize the Evidence snapshot: {str(exc)[:120]}"
    try:
        report = build_final_verifier_report(tmp)
    except Exception as exc:
        return None, f"the final-verifier producer raised {type(exc).__name__}: {str(exc)[:120]}"
    finally:
        _shutil.rmtree(tmp, ignore_errors=True)
    if not isinstance(report, dict):
        return None, f"the final-verifier producer returned a {type(report).__name__}, not an object"
    return report, None


def _final_verifier_reproducibility(evidence_view) -> dict:
    """F1 (round 31): a TRI-STATE reproducibility record — never a bare optimistic boolean. A report is
    authoritative ONLY when the producer ran successfully and exact equality was verified; an unchecked
    or failed regeneration is never reproducible.

    Returns ``{checked, reproducible, status, problems}`` where status is one of ``VERIFIED_EQUAL`` /
    ``VERIFIED_MISMATCH`` / ``NOT_CHECKED`` / ``PRODUCER_ERROR``. Only ``VERIFIED_EQUAL`` permits
    READY; every other Evidence-bearing state blocks with a bounded reason."""
    if evidence_view is None or not getattr(evidence_view, "_files", None):
        return {"checked": False, "reproducible": None, "status": "NOT_CHECKED", "problems": []}
    regenerated, problem = regenerate_final_verifier(evidence_view)
    if regenerated is None:
        return {"checked": True, "reproducible": False, "status": "PRODUCER_ERROR",
                "problems": [f"final_verifier_report.json could not be reproduced: {problem}"]}
    supplied = evidence_view.read_json("final_verifier_report.json")
    if not isinstance(supplied, dict) or not supplied:
        return {"checked": True, "reproducible": False, "status": "VERIFIED_MISMATCH",
                "problems": ["final_verifier_report.json is absent/unreadable; the staged Evidence "
                             "produces a report it does not carry"]}
    if supplied != regenerated:
        diffs = sorted(k for k in set(supplied) | set(regenerated)
                       if supplied.get(k) != regenerated.get(k))
        return {"checked": True, "reproducible": False, "status": "VERIFIED_MISMATCH",
                "problems": [f"final_verifier_report.json is not reproducible from the staged Evidence "
                             f"(the real producer disagrees at: {diffs[:8]})"]}
    return {"checked": True, "reproducible": True, "status": "VERIFIED_EQUAL", "problems": []}


def regenerate_token_truth(evidence_view) -> tuple[dict | None, str | None]:
    """F2 (round 32): the root ``token_truth.json`` is NOT authoritative by itself — it must be the
    exact aggregate of the per-task token_accounting/provider_evidence. Materialize the immutable
    snapshot and run the real ``token_truth.build_token_truth`` producer over it. Returns
    ``(canonical, problem)``; a distinguished failure yields ``(None, reason)`` and never a false
    success."""
    import shutil as _shutil
    import tempfile as _tempfile

    if evidence_view is None:
        return None, "no Evidence view"
    files = getattr(evidence_view, "_files", None)
    if not files:
        return None, "the Evidence snapshot is empty"
    try:
        from packages.orchestration.token_truth import build_token_truth
    except Exception as exc:
        return None, f"the token-truth producer is unavailable: {str(exc)[:120]}"
    tmp = None
    try:
        tmp = _tempfile.mkdtemp(prefix="remedy_tt_regen_")
        for rel, data in files.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p) or tmp, exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
    except Exception as exc:
        if tmp:
            _shutil.rmtree(tmp, ignore_errors=True)
        return None, f"could not materialize the Evidence snapshot: {str(exc)[:120]}"
    try:
        truth = build_token_truth(tmp)
    except Exception as exc:
        return None, f"the token-truth producer raised {type(exc).__name__}: {str(exc)[:120]}"
    finally:
        _shutil.rmtree(tmp, ignore_errors=True)
    if not isinstance(truth, dict):
        return None, f"the token-truth producer returned a {type(truth).__name__}, not an object"
    return truth, None


def _token_truth_authority(evidence_view) -> dict:
    """Require the packaged ``token_truth.json`` to EQUAL the canonical regeneration from task/provider
    Evidence, AND both canonical and supplied must individually pass ``validate_token_truth``. A forged
    root count/model that no task supports cannot survive. Returns ``{checked, equal, status, problems}``
    (``NOT_PRESENT`` when the bundle carries no token truth). Round 35 F4: VERIFIED_EQUAL requires BOTH
    outputs to be valid — an invalid canonical that equals an invalid supplied is PRODUCER_ERROR, and a
    valid canonical that does not equal an invalid supplied is MISMATCH."""
    if evidence_view is None or not getattr(evidence_view, "_files", None):
        return {"checked": False, "equal": None, "status": "NOT_CHECKED", "problems": []}
    if not evidence_view.isfile("token_truth.json"):
        return {"checked": False, "equal": None, "status": "NOT_PRESENT", "problems": []}
    canonical, problem = regenerate_token_truth(evidence_view)
    if canonical is None:
        return {"checked": True, "equal": False, "status": "PRODUCER_ERROR",
                "problems": [f"token_truth.json could not be regenerated: {problem}"]}
    # Round 35 F4: validate canonical output — the producer self-validates (round 35 F3), but
    # belt-and-suspenders: if the canonical is invalid, it's a PRODUCER_ERROR.
    try:
        from packages.orchestration.token_authority import validate_token_truth
        canonical_problems = validate_token_truth(canonical)
    except Exception as exc:
        return {"checked": True, "equal": False, "status": "PRODUCER_ERROR",
                "problems": [f"canonical token_truth validation failed: {str(exc)[:120]}"]}
    if canonical_problems:
        return {"checked": True, "equal": False, "status": "PRODUCER_ERROR",
                "problems": [f"canonical token_truth is invalid: {'; '.join(canonical_problems[:5])}"]}
    supplied = evidence_view.read_json("token_truth.json")
    if not isinstance(supplied, dict) or not supplied:
        return {"checked": True, "equal": False, "status": "MISMATCH",
                "problems": ["token_truth.json is absent/unreadable but the Evidence produces one"]}
    # Round 35 F4: validate supplied output — an invalid supplied cannot be VERIFIED_EQUAL.
    supplied_problems = validate_token_truth(supplied)
    if supplied_problems:
        return {"checked": True, "equal": False, "status": "MISMATCH",
                "problems": [f"supplied token_truth.json is invalid: "
                             f"{'; '.join(supplied_problems[:5])}"]}
    if supplied != canonical:
        diffs = sorted(k for k in set(supplied) | set(canonical)
                       if supplied.get(k) != canonical.get(k))
        return {"checked": True, "equal": False, "status": "MISMATCH",
                "problems": [f"token_truth.json is not the aggregate of the task/provider Evidence "
                             f"(the producer disagrees at: {diffs[:8]})"]}
    return {"checked": True, "equal": True, "status": "VERIFIED_EQUAL", "problems": []}


def _build_alignment(
    dirty_files: list[str], ev: _EvidenceView,
) -> dict:
    """Build review_subject/evidence alignment proof."""
    ev = _as_view(ev)
    _EXCLUDE_DIRS = {
        "remedy-job-evidence", "__pycache__", ".git", ".agent",
        "node_modules", ".data", ".mypy_cache", ".pytest_cache",
        ".venv", "venv", "dist", "build", "egg-info",
    }
    _EXCLUDE_SUBS = (
        "remedy-review-", "remedy-job-evidence", "run_transcript",
        ".coverage", "htmlcov/", ".review_zip_manifest",
    )
    _EXCLUDE_SUFFS = (
        ".pyc", ".pyo", ".egg", ".whl", ".zip", ".tar",
        ".gz", ".log", ".tmp",
    )

    def _is_source(raw: str) -> bool:
        path = raw.split()[-1] if raw.strip() else ""
        path = path.replace("\\", "/").strip()
        while path.startswith("./"):
            path = path[2:]
        if not path:
            return False
        parts = path.split("/")
        if any(p in _EXCLUDE_DIRS or p.lstrip(".") in _EXCLUDE_DIRS
               or p.endswith(".egg-info") for p in parts):
            return False
        if path.endswith(_EXCLUDE_SUFFS):
            return False
        if any(sub in path for sub in _EXCLUDE_SUBS):
            return False
        return True

    dirty_source_test = sorted({
        f.split()[-1] for f in dirty_files if _is_source(f)
    })

    cp_gate = _read_evidence_gate(ev, "change_provenance_gate.json")
    fv_report = _read_evidence_gate(ev, "final_verifier_report.json")
    ce_gate = _read_evidence_gate(ev, "commit_execution_gate.json")
    ac_gate = _read_evidence_gate(ev, "artifact_contract_gate.json")

    # F6 (round 31): the alignment view consumes gate lists — a malformed gate value (bool/int/dict)
    # must not raise here; coerce a non-list to empty so the manifest stays valid JSON (the gate matrix
    # blocks the malformed gate separately).
    def _as_list_field(d, key):
        v = d.get(key, []) if isinstance(d, dict) else []
        return v if isinstance(v, list) else []
    cp_covered = sorted(str(x) for x in _as_list_field(cp_gate, "covered_files"))
    fv_changed = sorted(str(x) for x in _as_list_field(fv_report, "authoritative_changed_files"))
    hash_mismatches = _as_list_field(cp_gate, "hash_mismatches")

    covered_set = set(cp_covered)
    fv_set = set(fv_changed)
    dirty_src_set = set(dirty_source_test)

    uncovered = sorted(dirty_src_set - covered_set)

    issues: list[str] = []
    if uncovered:
        issues.append(f"uncovered dirty source/test files: {uncovered}")
    if hash_mismatches:
        issues.append(
            f"content hash mismatches: {[m['file'] for m in hash_mismatches]}"
        )

    alignment_verdict = "PASS" if not issues else "BLOCKED"

    return {
        "dirty_file_count_total": len(dirty_files),
        "dirty_source_test_files": dirty_source_test,
        "intended_commit_files": fv_changed or cp_covered,
        "change_provenance_covered_files": cp_covered,
        "final_verifier_changed_files": fv_changed,
        "uncovered_source_test_files": uncovered,
        "hash_mismatches": hash_mismatches,
        "gate_verdicts": {
            "change_provenance_gate": cp_gate.get("verdict", ""),
            "final_verifier": fv_report.get("verdict", ""),
            "commit_execution_gate": ce_gate.get("verdict", ""),
            "artifact_contract_gate": ac_gate.get("verdict", ""),
        },
        "issues": issues,
        "verdict": alignment_verdict,
    }


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _job_flow_shape_problems(jf_data) -> list[str]:
    """F4 (round 28): the minimal CLOSED shape ``validate_evidence_candidate`` consumes from
    job_flow.json. A document that decodes to valid JSON but carries a wrong inner type (``final_audit``
    a list, ``target_guard`` a list, ...) must APPEND validation errors, never raise AttributeError/
    TypeError from a ``.get`` on a non-dict. Never raises.

    - root is a JSON object; ``job_id`` a non-empty string;
    - ``final_audit`` an object with a non-empty string ``status``;
    - ``final_audit.missing_observability_artifacts`` a list when present;
    - ``target_guard`` an object when present, with a Boolean ``mutated_target`` when present.
    """
    problems: list[str] = []
    if not isinstance(jf_data, dict):
        return ["job_flow.json: root is not a JSON object"]
    if not _nonempty_str(jf_data.get("job_id")):
        problems.append("job_flow.json: job_id is not a non-empty string")
    audit = jf_data.get("final_audit")
    if not isinstance(audit, dict):
        problems.append("job_flow.json: final_audit is not an object")
    else:
        if not _nonempty_str(audit.get("status")):
            problems.append("job_flow.json: final_audit.status is not a non-empty string")
        if "missing_observability_artifacts" in audit and not isinstance(
                audit["missing_observability_artifacts"], list):
            problems.append(
                "job_flow.json: final_audit.missing_observability_artifacts is not a list")
    tg = jf_data.get("target_guard")
    if tg is not None and not isinstance(tg, dict):
        problems.append("job_flow.json: target_guard is not an object")
    elif isinstance(tg, dict) and "mutated_target" in tg and not isinstance(
            tg["mutated_target"], bool):
        problems.append("job_flow.json: target_guard.mutated_target is not a boolean")
    return problems


def validate_evidence_candidate(ev, *, required_verification_suites=None) -> dict:
    ev = _as_view(ev)
    errors: list[str] = []
    missing_root: list[str] = []
    missing_task: dict[str, list[str]] = {}

    manual_completion = _is_manual_completion(ev)
    has_manual_claim = _has_any_manual_claim(ev)
    manual_completion_errors: list[str] = []
    not_applicable_root: list[str] = []

    if has_manual_claim and not manual_completion:
        errors.append(
            "mixed completion identity: some artifacts claim manual_operator_repair "
            "but the bundle does not satisfy the full manual-completion contract "
            "(final_job_review.completion_mode + all task manual_repair_provenance)")

    if manual_completion:
        manual_completion_errors = validate_manual_completion(ev)
        errors.extend(manual_completion_errors)

    for art in REQUIRED_ROOT_ARTIFACTS:
        if ev.isfile(art):
            continue
        if manual_completion and art in MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS:
            # A deterministic manual-only completion legitimately has no
            # provider-flow root artifact — mark not-applicable, never missing.
            not_applicable_root.append(art)
            continue
        missing_root.append(art)
        errors.append(f"missing root artifact: {art}")

    has_job_flow = ev.isfile("job_flow.json")
    job_id = ""
    final_audit_status = ""
    missing_obs: list[str] = []
    target_mutation_detected = False

    if manual_completion and not has_job_flow:
        # Derive identity/verdict from the existing final job review + final
        # verifier, without fabricating a provider job_flow.json.
        fjr = _mc_read_json(ev, "final_job_review.json")
        manifest_obj = _mc_read_json(ev, "manifest.json")
        job_id = str(fjr.get("job_id") or manifest_obj.get("job_id") or "")
        if not job_id:
            errors.append("manual completion: job_id could not be derived")
        fv = _read_evidence_gate(ev, "final_verifier_report.json")
        final_audit_status = str(fv.get("verdict", "") or "")
        if not final_audit_status:
            errors.append("final_verifier_report.json: verdict missing")

    if has_job_flow:
        raw = ev.read_bytes("job_flow.json")
        jf_data = None
        try:
            # F5 (round 27): job_flow.json is trust-bearing (job_id, final_audit.status) — decode it
            # strictly so a duplicate/contradictory key is refused, never last-wins.
            jf_data = _strict_json_loads(raw) if raw is not None else {}
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"job_flow.json: parse error: {exc}")
        if jf_data is not None:
            # F4 (round 28): validate the minimal closed shape BEFORE reading nested fields, so a
            # valid-JSON-but-wrong-inner-type document (final_audit a list, target_guard a list, ...)
            # appends errors instead of raising AttributeError from a .get on a non-dict.
            errors.extend(_job_flow_shape_problems(jf_data))
            if isinstance(jf_data, dict):
                jid = jf_data.get("job_id")
                job_id = jid if isinstance(jid, str) else ""
                audit = jf_data.get("final_audit")
                if isinstance(audit, dict):
                    st = audit.get("status")
                    final_audit_status = st if isinstance(st, str) else ""
                    mo = audit.get("missing_observability_artifacts")
                    if isinstance(mo, list) and mo:
                        missing_obs = mo
                        errors.append(
                            f"final_audit.missing_observability_artifacts: {missing_obs}")
                tg = jf_data.get("target_guard")
                if isinstance(tg, dict) and tg.get("mutated_target", False) is True:
                    target_mutation_detected = True
                    errors.append("target_guard indicates target mutation")

    task_run_count = 0
    manual_repair_tasks: list[str] = []
    if ev.isdir("task_runs"):
        for entry in ev.listdir("task_runs"):
            td = f"task_runs/{entry}"
            if not ev.isdir(td):
                continue
            task_run_count += 1
            mrp_rel = f"{td}/manual_repair_provenance.json"
            is_manual_repair = ev.isfile(mrp_rel)
            if is_manual_repair:
                raw = ev.read_bytes(mrp_rel)
                try:
                    # F5 (round 27): manual_repair_provenance is trust-bearing — decode strictly so a
                    # duplicate key cannot silently flip a provenance flag.
                    mrp = _strict_json_loads(raw) if raw is not None else None
                    if not (isinstance(mrp, dict) and mrp.get("manual_operator_repair") is True
                            and mrp.get("no_provider_calls") is True):
                        is_manual_repair = False
                        errors.append(
                            f"task_runs/{entry}: manual_repair_provenance.json invalid"
                        )
                except (json.JSONDecodeError, ValueError):
                    is_manual_repair = False
                    errors.append(
                        f"task_runs/{entry}: manual_repair_provenance.json unreadable"
                    )
            if is_manual_repair:
                manual_repair_tasks.append(entry)
            task_missing = []
            for art in REQUIRED_TASK_ARTIFACTS:
                if is_manual_repair and art in MANUAL_REPAIR_EXEMPT_ARTIFACTS:
                    continue
                if not ev.isfile(f"{td}/{art}"):
                    task_missing.append(art)
            if task_missing:
                missing_task[entry] = task_missing
                errors.append(
                    f"task_runs/{entry}: missing {task_missing}"
                )
    else:
        errors.append("no task_runs/ directory")

    if task_run_count == 0:
        errors.append("no task runs found")

    # Round 40 F4: verification completeness — when the caller supplies required suites,
    # the verification matrix must cover all of them.
    if required_verification_suites:
        vt_raw = _mc_read_json(ev, "verification_tests.json")
        if vt_raw:
            try:
                from packages.orchestration.verification_matrix import (
                    validate_verification_completeness,
                )
                vc_problems = validate_verification_completeness(
                    vt_raw, required_verification_suites)
                errors.extend(vc_problems)
            except ImportError:
                pass

    # Round 40 F4: diagnostic staleness — if diagnostic_broad_run.json is present,
    # its head_commit must match the review subject's HEAD.
    diag_raw = _mc_read_json(ev, "diagnostic_broad_run.json")
    if diag_raw:
        subj = _mc_read_json(ev, "review_subject.json")
        diag_head = str(diag_raw.get("head_commit") or "")
        subj_head = str(subj.get("head_commit") or "")
        if diag_head and subj_head and diag_head != subj_head:
            errors.append(
                f"diagnostic_broad_run.json references stale HEAD {diag_head[:12]}, "
                f"expected {subj_head[:12]}")

    def _root_status(art: str) -> str:
        if art in not_applicable_root:
            return "not_applicable_manual_completion"
        return "present" if art not in missing_root else "absent"

    is_valid = len(errors) == 0

    return {
        "is_valid_current_run": is_valid,
        "validation_errors": errors,
        "manual_completion": manual_completion,
        "manual_completion_errors": manual_completion_errors,
        "not_applicable_root_artifacts": not_applicable_root,
        "required_root_artifacts": {
            art: _root_status(art) for art in REQUIRED_ROOT_ARTIFACTS
        },
        "required_task_artifacts": missing_task,
        "task_run_count": task_run_count,
        "manual_repair_tasks": manual_repair_tasks,
        "job_id": job_id,
        "final_audit_status": final_audit_status,
        "missing_observability_artifacts": missing_obs,
        "target_mutation_detected": target_mutation_detected,
    }


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_bundle_integrity(
    ev,
    source_root: str,
) -> dict:
    ev = _as_view(ev)
    result: dict = {
        "current_content_hash_checked": False,
        "current_content_hash_mismatches": [],
        "current_content_hash_missing_proofs": [],
        "packaged_file_hashes": {},
        "verdict": "PASS",
    }

    if ev is None or not ev.isfile("current_change_content_proof.json"):
        return result

    # F2 (round 29): normalize the consumed collections through the shared shape validator so a
    # malformed file_hashes/tombstones/subject cannot reach the ``.items()``/iteration below as a
    # non-collection. A wrong type here is recorded (and blocks) by validate_manual_completion.
    proof = _read_mc(ev, "current_change_content_proof.json", [])

    file_hashes = proof.get("file_hashes", {})
    if not file_hashes:
        return result

    # F4 (round 17): the check is TYPED and NO-FOLLOW, driven by the ReviewSubject's own record of
    # what each path is. `os.path.isfile` + `open` follow symlinks, so an allowed contained symlink
    # was hashed as its TARGET's bytes (content from outside the packaged set) and a regular file
    # swapped for a symlink after the proof was written would still verify. Each path is inspected
    # with `lstat` and hashed by its declared kind: a regular file its own bytes, a symlink its
    # literal target text — never the target.
    import hashlib as _hashlib

    kinds: dict[str, str] = {}
    link_targets: dict[str, str] = {}
    subj = _read_mc(ev, "review_subject.json", [])
    for f in (subj.get("files") or []):
        kinds[_mc_norm(str(f.get("path", "")))] = str(f.get("kind") or "regular")
        if f.get("link_target") is not None:
            link_targets[_mc_norm(str(f.get("path", "")))] = str(f.get("link_target"))

    result["current_content_hash_checked"] = True
    mismatches: list = []
    missing_proofs: list = []
    packaged_hashes: dict = {}

    # F3 (round 18): read every proof path through the ANCHORED, atomically no-follow reader. The
    # old shape lstat'd `abs_path` then `open(abs_path)` by name — a regular file swapped to an
    # external symlink in that window would have been followed and the OUTSIDE hash reported PASS.
    # `read_verified_relative` re-lstats and opens with O_NOFOLLOW relative to a held root fd, so a
    # swap changes the inode and is refused, never read.
    from packages.common.secure_fs import SecureFsError, read_verified_relative

    for rel_path, expected_hash in file_hashes.items():
        declared_kind = kinds.get(_mc_norm(rel_path), "regular")
        try:
            vf = read_verified_relative(
                source_root, rel_path,
                expected_kind=("symlink" if declared_kind == "symlink" else "regular"),
                error_cls=SecureFsError, noun="proof file")
        except SecureFsError:
            # Absent, wrong kind, or swapped mid-read — either a missing proof or a refused race.
            declared_target = link_targets.get(_mc_norm(rel_path))
            missing_proofs.append(rel_path)
            continue

        if declared_kind == "symlink":
            target = vf.data.decode("utf-8", errors="surrogateescape")
            actual_hash = _hashlib.sha256(vf.data).hexdigest()
            declared_target = link_targets.get(_mc_norm(rel_path))
            if declared_target is not None and target != declared_target:
                mismatches.append({"file": rel_path, "expected": "link_target",
                                   "actual": "changed"})
                continue
        else:
            actual_hash = _hashlib.sha256(vf.data).hexdigest()

        packaged_hashes[rel_path] = actual_hash
        if actual_hash != expected_hash:
            mismatches.append({"file": rel_path, "expected": expected_hash,
                               "actual": actual_hash})

    result["current_content_hash_mismatches"] = mismatches
    result["current_content_hash_missing_proofs"] = missing_proofs
    result["packaged_file_hashes"] = packaged_hashes

    if mismatches or missing_proofs:
        result["verdict"] = "BLOCKED"

    return result


def build_manifest(
    evidence_dir: str | None = None,
    selection_mode: str = "",
    selection_reason: str = "",
    candidate_count: int = 0,
    selected_mtime: str = "",
    rejected_candidate_count: int = 0,
    generated_outputs=frozenset(),
) -> dict:
    """Standalone/CLI/test entry: read the evidence directory ONCE into an immutable byte-map view,
    then build the manifest from those bytes. The coordinator instead passes its Source snapshot to
    ``build_manifest_from_snapshot`` so it never re-reads the staging filesystem after the snapshot.
    """
    ev = (_view_from_dir(evidence_dir)
          if evidence_dir and os.path.isdir(evidence_dir) else None)
    return build_manifest_from_snapshot(
        ev, evidence_path=evidence_dir, selection_mode=selection_mode,
        selection_reason=selection_reason, candidate_count=candidate_count,
        selected_mtime=selected_mtime, rejected_candidate_count=rejected_candidate_count,
        generated_outputs=generated_outputs)


def build_manifest_from_snapshot(
    evidence_view: _EvidenceView | None = None,
    *,
    evidence_path: str | None = None,
    selection_mode: str = "",
    selection_reason: str = "",
    candidate_count: int = 0,
    selected_mtime: str = "",
    rejected_candidate_count: int = 0,
    generated_outputs=frozenset(),
) -> dict:
    """F6 (round 24): build the Root Manifest from the IMMUTABLE Evidence view (Source snapshot
    bytes), never from staging-filesystem re-reads. Repository/Git facts (branch, HEAD, dirty set,
    commit chain, patch bytes, containment) still come from the repo; ``evidence_path`` is used only
    for the path-level containment check, not to read any evidence content.

    F1 (round 31): whenever Evidence is present the final verifier report is ALWAYS regenerated from
    the staged bytes and checked for exact equality (standalone and coordinator alike), so no path
    can serialize an unchecked reproducibility claim."""
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _git(["rev-parse", "HEAD"])
    has_commits_val = _has_commits()
    # F5 (round 32): ONE immutable git-status snapshot — dirty and untracked derive from the same
    # acquisition, and a non-OK status blocks READY rather than falling open to "clean".
    git_snapshot = _git_status_snapshot()
    dirty = [f"{xy} {path}" for xy, path in git_snapshot["records"]]
    has_untracked = any(xy == "??" for xy, _ in git_snapshot["records"])

    review_subject = _classify_review_subject(
        branch, commit, dirty, has_untracked, has_commits_val,
        generated_outputs=generated_outputs, git_status=git_snapshot["status"],
    )

    root_artifacts = {
        "job_flow.json": "absent_no_evidence_dir",
        "agent_run_trace.jsonl": "absent_no_evidence_dir",
        "agent_run_trace_summary.json": "absent_no_evidence_dir",
        "prompt_trace_summary.json": "absent_no_evidence_dir",
        "manifest.json": "absent_no_evidence_dir",
        "command_transcript.json": "absent_no_evidence_dir",
    }
    task_runs: list[dict] = []
    current_evidence: dict = {}

    if evidence_view is not None:
        for artifact_name in root_artifacts:
            root_artifacts[artifact_name] = evidence_view.status(artifact_name)
        task_runs = _scan_task_runs(evidence_view)
        job_id = _read_job_id(evidence_view)
        audit = _read_final_audit(evidence_view)
        trace_sources = _read_trace_sources(evidence_view)

        validation = validate_evidence_candidate(evidence_view)

        fresh_gate = _read_fresh_evidence_gate(evidence_view)
        freshness_ok = bool(
            fresh_gate.get("evidence_freshness", {}).get("is_fresh", False)
        )
        validity_ok = validation["is_valid_current_run"]

        current_evidence = {
            "job_id": job_id,
            "evidence_freshness": {
                "is_fresh": freshness_ok,
                "evidence_validity": {"is_valid_current_run": validity_ok},
                "evidence_authoritative": freshness_ok and validity_ok,
            },
            "zip_prefix": "evidence/current",
            # F1 (round 21): the typed ArchivePlan and its EXPECTATION are packaged under
            # evidence/current/ by build_review_zip.py. Reference only members that actually exist,
            # by their deterministic in-archive paths — the round-20 rename retired the stale
            # `review_zip_verification.json`; the real member is `review_zip_expectation.json`.
            "review_archive": {
                "plan": "evidence/current/review_archive_plan.json",
                "expectation": "evidence/current/review_zip_expectation.json",
            },
            "validation": {
                "is_valid_current_run": validation["is_valid_current_run"],
                "validation_errors": validation["validation_errors"],
                "required_root_artifacts": validation[
                    "required_root_artifacts"
                ],
                "required_task_artifacts": validation[
                    "required_task_artifacts"
                ],
                "manual_repair_tasks": validation.get(
                    "manual_repair_tasks", []
                ),
                "selected_candidate_status": (
                    "valid" if validation["is_valid_current_run"]
                    else "incomplete"
                ),
                "selection_mode": selection_mode or "unknown",
                "selection_reason": selection_reason or "unknown",
                "selected_from_candidate_count": candidate_count,
                "rejected_candidate_count": rejected_candidate_count,
            },
            "selection_mode": selection_mode or "unknown",
            "selection_reason": selection_reason or "unknown",
            "selected_from_candidate_count": candidate_count,
            "selected_modified_time": selected_mtime or "",
            "root_artifacts": root_artifacts,
            "task_runs": task_runs,
            "trace_sources": trace_sources,
            "final_audit_status": audit.get("status", "unknown"),
            "missing_observability_artifacts": audit.get(
                "missing_observability_artifacts", []
            ),
        }

    review_state = _extract_review_state()

    alignment: dict | None = None
    if evidence_view is not None:
        alignment = _build_alignment(dirty, evidence_view)
        if alignment["verdict"] == "BLOCKED" and current_evidence:
            current_evidence["evidence_freshness"]["evidence_authoritative"] = False

    # Source-root containment check
    source_root = _git(["rev-parse", "--show-toplevel"]).strip()
    cwd = os.getcwd()
    containment_blockers: list[str] = []
    external_paths: list[str] = []

    # F9 (round 17): containment by PATH COMPONENTS, not a string prefix. A raw
    # `startswith(root)` accepts a sibling `/root/repo-evil` for root `/root/repo` — a different
    # directory whose name merely begins with the root's. `contained` uses os.path.commonpath and
    # resolves symlinks first, so a sibling, a different drive, or a symlinked descendant that
    # escapes the root is refused.
    from packages.orchestration.review_zip import contained

    if not contained(source_root, cwd):
        containment_blockers.append(
            f"packaging cwd {_shareable_path(cwd, source_root)} is outside source_root"
        )
        external_paths.append(_shareable_path(cwd, source_root))

    if evidence_path:
        ev_resolved = os.path.realpath(evidence_path)
        if not contained(source_root, evidence_path):
            containment_blockers.append(
                f"evidence_dir {_shareable_path(ev_resolved, source_root)} "
                "is outside source_root"
            )
            external_paths.append(_shareable_path(ev_resolved, source_root))

    containment_ok = len(containment_blockers) == 0
    containment_verdict = "PASS" if containment_ok else "BLOCKED"

    # Determine package status
    packaging_warnings: list[str] = []
    evidence_valid = bool(
        current_evidence
        and current_evidence.get("evidence_freshness", {}).get(
            "evidence_authoritative", False
        )
    )
    alignment_ok = alignment and alignment.get("verdict") != "BLOCKED"

    if not current_evidence:
        packaging_warnings.append("no evidence directory provided or found")
    if current_evidence and not evidence_valid:
        packaging_warnings.append("evidence is not authoritative")
    if alignment and not alignment_ok:
        packaging_warnings.append("review subject/evidence alignment is BLOCKED")
    if not containment_ok:
        packaging_warnings.extend(containment_blockers)

    # F1 (round 22): READY_FOR_REVIEW additionally requires the COMPLETE packaged gate verdict
    # matrix to pass, decoded from the (staged) gate bytes.
    gate_matrix = {"ok": True, "gate_verdicts": {}, "blocking_reasons": []}
    if current_evidence:
        gate_matrix = evaluate_ready_gate_matrix(_evidence_dir_gate_loader(evidence_view))
        if not gate_matrix["ok"]:
            packaging_warnings.append(
                "gate matrix not satisfied: " + "; ".join(gate_matrix["blocking_reasons"][:4]))

    # F1 (round 31): the packaged final_verifier_report.json must be REPRODUCIBLE — a fresh, SUCCESSFUL
    # run of the real producer over the exact staged Evidence bytes must equal it. This is ALWAYS
    # performed when Evidence is present (standalone and coordinator alike), so the manifest can never
    # claim reproducibility it did not verify; a producer failure is PRODUCER_ERROR, never success.
    fv_repro = {"checked": False, "reproducible": None, "status": "NOT_CHECKED", "problems": []}
    if current_evidence:
        fv_repro = _final_verifier_reproducibility(evidence_view)
        if fv_repro["status"] != "VERIFIED_EQUAL":
            packaging_warnings.extend(fv_repro["problems"])
    fv_reproducible = fv_repro["status"] == "VERIFIED_EQUAL"

    # READY requires VERIFIED_EQUAL whenever Evidence is present; an unchecked or failed regeneration
    # can never be READY_FOR_REVIEW.
    fv_ok_for_ready = (fv_repro["status"] == "VERIFIED_EQUAL") if current_evidence else True
    # F5 (round 32): a non-OK git-status snapshot blocks READY — the working-tree state is unknown.
    git_status_ok = git_snapshot["status"] == "OK"
    if not git_status_ok:
        packaging_warnings.append(
            f"git status is {git_snapshot['status']}: {git_snapshot['diagnostic']}")
    # F2 (round 32): the root token truth must be the exact aggregate of task/provider Evidence — a
    # forged root count/model that no task supports blocks even if the report reproduces it.
    tt_authority = {"checked": False, "equal": None, "status": "NOT_CHECKED", "problems": []}
    if current_evidence:
        tt_authority = _token_truth_authority(evidence_view)
        if tt_authority["status"] not in ("VERIFIED_EQUAL", "NOT_PRESENT"):
            packaging_warnings.extend(tt_authority["problems"])
    tt_ok_for_ready = tt_authority["status"] in ("VERIFIED_EQUAL", "NOT_PRESENT")
    if (evidence_valid and alignment_ok and containment_ok and gate_matrix["ok"]
            and fv_ok_for_ready and git_status_ok and tt_ok_for_ready):
        package_status = "READY_FOR_REVIEW"
    elif not current_evidence:
        package_status = "NO_EVIDENCE"
    else:
        package_status = "BLOCKED_EVIDENCE"

    # Packaging proof — record what was actually packaged
    ev_manifest_task_count = 0
    ev_manifest_task_ids: list[str] = []
    ev_manifest_job_id = ""
    ev_manifest_mtime = ""
    if evidence_view is not None and evidence_view.isfile("manifest.json"):
        raw = evidence_view.read_bytes("manifest.json")
        try:
            # F5 (round 27): the packaged manifest.json is trust-bearing (job_id, task ids) — strict.
            ev_mf = _strict_json_loads(raw) if raw is not None else {}
            if not isinstance(ev_mf, dict):
                raise ValueError("manifest.json is not an object")
            ev_manifest_task_count = ev_mf.get("task_count", 0)
            ev_manifest_task_ids = ev_mf.get("task_ids", [])
            ev_manifest_job_id = ev_mf.get("job_id", "")
            # F6 (round 24): the packaging-proof timestamp comes from the snapshot view's own frozen
            # record of the modified time, never a fresh stat of the staging filesystem.
            ev_manifest_mtime = evidence_view.mtime_iso("manifest.json")
        except (json.JSONDecodeError, ValueError):
            packaging_warnings.append(
                "evidence manifest.json unreadable"
            )

    # Review-bundle integrity: compare packaged files against content proof
    bundle_integrity = _check_bundle_integrity(evidence_view, source_root)
    if bundle_integrity["verdict"] == "BLOCKED":
        packaging_warnings.append("review bundle content hash mismatch or missing proofs")
        package_status = "BLOCKED_EVIDENCE"
    elif (
        package_status == "READY_FOR_REVIEW"
        and not bundle_integrity.get("current_content_hash_checked", False)
    ):
        # Evidence passed other checks but content hashes were not verified
        # (no proof file or no file_hashes). Mark as unverified so reviewers
        # know integrity was not confirmed.
        package_status = "READY_FOR_REVIEW_UNVERIFIED"
        packaging_warnings.append(
            "content hash verification was not performed; integrity unconfirmed"
        )

    _subject = _mc_read_json(evidence_view, "review_subject.json") if evidence_view else {}
    _chain = _mc_read_json(evidence_view, "review_commit_chain.json") if evidence_view else {}
    _proof_doc = _mc_read_json(evidence_view, "current_change_content_proof.json") \
        if evidence_view else {}

    manifest = {
        "bundle_kind": "remedy_review_zip",
        # The version stays 12: `committed_review_subject` below is ADDITIVE, so every existing
        # v12 reader keeps working unchanged. Bumping it would signal a breaking change that did
        # not happen — and would drag an already-broken, unrelated test file into this round's
        # attested set, where no authoritative command could honestly cover it.
        "bundle_version": 12,
        # Round 15: which base this is a review OF, and the machine-verifiable history that got
        # from there to HEAD. A deleted path is packaged as a TOMBSTONE — the ZIP cannot carry a
        # file that no longer exists, and pretending otherwise would be a missing-proof error for
        # a real, proven part of the change.
        #
        # Deliberately NOT named `review_subject`: that key already exists below with an older,
        # different meaning (branch/kind/dirty summary), and silently redefining it would break
        # every existing reader of that field.
        "committed_review_subject": {
            "base_commit": str(_subject.get("base_commit") or ""),
            "head_commit": str(_subject.get("head_commit") or ""),
            "base_is_ancestor": bool(_subject.get("base_is_ancestor") or False),
            "commit_count": len(_chain.get("commits") or []),
            "file_count": len(_subject.get("files") or []),
            "tombstones": sorted(_proof_doc.get("tombstones") or {}),
        },
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "review_package_created": True,
        "package_status": package_status,
        "ready_gate_matrix": gate_matrix,
        "final_verifier_reproducibility": fv_repro,
        "git_status_snapshot": {"status": git_snapshot["status"],
                                "diagnostic": git_snapshot["diagnostic"]},
        "token_truth_authority": {"status": tt_authority["status"],
                                  "problems": tt_authority["problems"][:4]},
        # Back-compat boolean: TRUE only for a verified-equal check. An unchecked/failed state is never
        # serialized true (the tri-state ``status`` carries the real meaning).
        "final_verifier_reproducible": fv_reproducible,
        "review_subject": review_subject,
        "review_state": review_state,
        "review_subject_evidence_alignment": alignment,
        "packaged_evidence_dir": (
            _shareable_path(evidence_path, source_root) if evidence_path else ""
        ),
        "packaged_evidence_job_id": ev_manifest_job_id,
        "packaged_evidence_manifest_task_count": ev_manifest_task_count,
        "packaged_evidence_manifest_task_ids": ev_manifest_task_ids,
        "packaged_evidence_modified_at": ev_manifest_mtime,
        "source_root": SOURCE_ROOT_TOKEN,
        "packaging_command_context": {
            "cwd": _shareable_path(cwd, source_root),
            "evidence_dir_arg": (
                _shareable_path(evidence_path, source_root) if evidence_path else ""
            ),
        },
        "source_root_containment": {
            "verdict": containment_verdict,
            "blockers": containment_blockers,
        },
        "external_paths_detected": external_paths,
        "publication_capability": _probe_publication_capability(source_root),
        "review_bundle_integrity": bundle_integrity,
        "packaging_warnings": packaging_warnings,
        "policy": (
            "Current-run evidence under evidence/current/. "
            "Stale evidence dirs excluded by default. "
            "Excludes .git, .data, node_modules, caches, build outputs, "
            "env files, private keys, logs, old archives."
        ),
        "agent_state": {
            ".agent/live_review.md": _check(".agent/live_review.md"),
            ".agent/plan.md": _check(".agent/plan.md"),
            ".agent/review_protocol.md": _check(".agent/review_protocol.md"),
        },
        "current_evidence": current_evidence if current_evidence else None,
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build review zip manifest")
    parser.add_argument("--evidence-dir", default=None)
    parser.add_argument("--selection-mode", default="")
    parser.add_argument("--selection-reason", default="")
    parser.add_argument("--candidate-count", type=int, default=0)
    parser.add_argument("--rejected-candidate-count", type=int, default=0)
    parser.add_argument("--selected-mtime", default="")
    parser.add_argument("--output", default=".review_zip_manifest.json")
    parser.add_argument(
        "--generated-output", action="append", default=[], dest="generated_outputs",
        help="an exact repo-root-relative path THIS packaging invocation generates (repeatable); "
             "only these are dispositioned as packaging outputs instead of dirty source changes")
    args = parser.parse_args()

    manifest = build_manifest(
        args.evidence_dir,
        selection_mode=args.selection_mode,
        selection_reason=args.selection_reason,
        candidate_count=args.candidate_count,
        selected_mtime=args.selected_mtime,
        rejected_candidate_count=args.rejected_candidate_count,
        generated_outputs=frozenset(args.generated_outputs),
    )
    out = json.dumps(manifest, indent=2) + "\n"

    if args.output == "-":
        sys.stdout.write(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
