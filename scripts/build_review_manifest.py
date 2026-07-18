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
        canonical_provenance_sha256 as _canon_provenance_sha256,
        parse_safe_diff_paths as _canon_parse_safe_diff_paths,
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


def _dirty_files() -> list[str]:
    # ``-u`` lists untracked files individually. Without it git collapses an
    # untracked directory to ``dir/``, which can never match a covered file and
    # would wrongly report the whole directory as uncovered.
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "-u"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            return []
        return [line.strip() for line in r.stdout.strip().split("\n")
                if line.strip()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def _has_untracked_files() -> bool:
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            return False
        return any(line.startswith("??") for line in r.stdout.strip().split("\n")
                   if line.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _has_commits() -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and len(r.stdout.strip()) >= 7
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _classify_review_subject(
    branch: str, commit: str, dirty: list[str],
    has_untracked: bool, has_commits_val: bool,
) -> dict:
    is_main = branch in ("main", "master")
    is_dirty = len(dirty) > 0

    if not has_commits_val:
        kind = "unknown"
        summary = "No commits — fresh git init or degraded metadata"
    elif is_main and not is_dirty:
        kind = "clean_commit"
        summary = f"Clean main at {commit[:12]}"
    elif is_main and is_dirty:
        kind = "dirty_working_tree"
        summary = f"Dirty working tree on main ({len(dirty)} changed file(s))"
    elif not is_main and not is_dirty:
        kind = "feature_branch"
        summary = f"Feature branch {branch} at {commit[:12]}"
    else:
        kind = "dirty_working_tree"
        summary = f"Dirty feature branch {branch} ({len(dirty)} changed file(s))"

    return {
        "kind": kind,
        "branch": branch,
        "commit": commit,
        "dirty_files": dirty,
        "dirty_file_count_total": len(dirty),
        "dirty_files_truncated": False,
        "has_untracked_files": has_untracked,
        "has_commits": has_commits_val,
        "degraded_metadata": not has_commits_val,
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


def _scan_task_runs(evidence_dir: str) -> list[dict]:
    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    if not os.path.isdir(task_runs_dir):
        return []
    result = []
    for entry in sorted(os.listdir(task_runs_dir)):
        task_path = os.path.join(task_runs_dir, entry)
        if not os.path.isdir(task_path):
            continue
        mrp_path = os.path.join(task_path, "manual_repair_provenance.json")
        is_manual = os.path.isfile(mrp_path)
        info: dict = {
            "task": entry,
            "prompt_trace": _check(os.path.join(task_path, "prompt_trace.jsonl")),
            "prompt_trace_summary": _check(os.path.join(task_path, "prompt_trace_summary.json")),
            "review": _check(os.path.join(task_path, "review.json")),
            "repair_loop": _check(os.path.join(task_path, "repair_loop.json")),
            "token_accounting": _check(os.path.join(task_path, "token_accounting.json")),
            "provider_evidence": _check(os.path.join(task_path, "provider_evidence.json")),
            "manual_repair_provenance": _check(mrp_path),
            "is_manual_repair": is_manual,
        }
        result.append(info)
    return result


def _load_json(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _read_job_id(evidence_dir: str) -> str:
    """Job ID from provider-flow evidence, else from the bundle manifest.

    ``job_flow.json`` is intentionally absent for an operator-attested manual
    completion, so falling back to ``manifest.json`` is what keeps the shared
    manifest from reporting an empty Job ID for a perfectly valid bundle.
    """
    jf = _load_json(os.path.join(evidence_dir, "job_flow.json"))
    job_id = str(jf.get("job_id") or "")
    if job_id:
        return job_id
    mf = _load_json(os.path.join(evidence_dir, "manifest.json"))
    job_id = str(mf.get("job_id") or "")
    if job_id:
        return job_id
    fjr = _load_json(os.path.join(evidence_dir, "final_job_review.json"))
    return str(fjr.get("job_id") or "")


def _read_final_audit(evidence_dir: str) -> dict:
    """Final audit from provider-flow evidence, else the manual-completion verdict.

    No provider observability artifact is fabricated: for a manual completion the
    status comes from the verifier/review artifacts that actually exist.
    """
    jf = _load_json(os.path.join(evidence_dir, "job_flow.json"))
    audit = jf.get("final_audit")
    if isinstance(audit, dict) and audit:
        return audit

    fv = _load_json(os.path.join(evidence_dir, "final_verifier_report.json"))
    status = str(fv.get("verdict") or "")
    source = "final_verifier_report.json"
    if not status:
        fjr = _load_json(os.path.join(evidence_dir, "final_job_review.json"))
        status = str(fjr.get("verdict") or "")
        source = "final_job_review.json"
    if not status:
        return {}
    return {
        "status": status,
        "source": source,
        "missing_observability_artifacts": [],
    }


def _read_trace_sources(evidence_dir: str) -> list[str]:
    sf = os.path.join(evidence_dir, "agent_run_trace_summary.json")
    if not os.path.isfile(sf):
        return []
    try:
        with open(sf) as f:
            data = json.load(f)
        return data.get("trace_sources", [])
    except (json.JSONDecodeError, OSError):
        return []


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


def _mc_read_json(evidence_dir: str, rel: str) -> dict:
    """Read a JSON object from the evidence dir, or {} if absent/invalid."""
    path = os.path.join(evidence_dir, rel)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _mc_task_dirs(evidence_dir: str) -> list[str]:
    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    if not os.path.isdir(task_runs_dir):
        return []
    return [
        e for e in sorted(os.listdir(task_runs_dir))
        if os.path.isdir(os.path.join(task_runs_dir, e))
    ]


def _mc_norm(p: str) -> str:
    p = str(p or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    if p.startswith(("a/", "b/")):
        p = p[2:]
    return p


def _is_sha256(v) -> bool:
    return isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v.lower())


def _all_task_runs_manual(evidence_dir: str) -> bool:
    """True when every task_run has a valid manual_repair_provenance."""
    task_dirs = _mc_task_dirs(evidence_dir)
    if not task_dirs:
        return False
    for entry in task_dirs:
        mrp = _mc_read_json(evidence_dir, os.path.join("task_runs", entry, "manual_repair_provenance.json"))
        if not (mrp.get("manual_operator_repair") is True and mrp.get("no_provider_calls") is True):
            return False
    return True


def _is_manual_completion(evidence_dir: str) -> bool:
    """A manual-only completion candidate: the final job review declares the
    manual completion mode AND every task run carries manual provenance. No
    bespoke root artifact — detection rides existing artifacts only."""
    fjr = _mc_read_json(evidence_dir, "final_job_review.json")
    if fjr.get("completion_mode") != "manual_operator_repair":
        return False
    return _all_task_runs_manual(evidence_dir)


def _verify_review_subject_records(evidence_dir: str, subject: dict, base: str) -> list:
    """F4 (round 16): the packager RECOMPUTES the whole review subject and holds the artifact to it.

    The final package trusted `review_subject.json` — the Evidence job's own account of what it
    was a review of. A forged tombstone hash, a rewritten rename origin, or a status flipped from
    `added` to `modified` therefore travelled straight into a READY package: the one artifact that
    says WHAT is under review was the one artifact nobody recomputed.

    So the subject is resolved again here, from the recorded base, and compared record by record:
    path, old_path, status, base_sha256, current_sha256 and file kind.
    """
    errors: list = []
    try:
        from packages.orchestration.review_subject import (
            resolve_review_subject, validate_review_subject_schema,
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
    chain = _mc_read_json(evidence_dir, "review_commit_chain.json")
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


def _verify_commit_patches(evidence_dir: str, actual: list) -> list:
    """F7 (round 16): exactly one canonical patch artifact per commit, recomputed here.

    The chain recorded `patch_sha256` and shipped nothing to hash it against, so the one field
    that says what a commit DID was the one field a ZIP-only reviewer could not check. The
    packager now recomputes the bytes from the repository, holds the packaged file to them, and
    refuses a missing, extra or tampered patch.
    """
    import hashlib as _h

    errors: list = []
    try:
        from packages.orchestration.review_subject import (
            COMMIT_PATCH_DIRNAME, commit_patch_bytes, commit_patch_filename,
        )
    except Exception as exc:
        return [f"cannot verify commit patches: {str(exc)[:120]}"]

    pdir = os.path.join(evidence_dir, COMMIT_PATCH_DIRNAME)
    if not actual:
        return errors
    if not os.path.isdir(pdir):
        return [f"the packaged evidence carries no {COMMIT_PATCH_DIRNAME}/ for its "
                f"{len(actual)} commit(s)"]

    expected_names = set()
    for c in actual:
        name = commit_patch_filename(c.commit)
        expected_names.add(name)
        p = os.path.join(pdir, name)
        if not os.path.isfile(p):
            errors.append(f"commit {c.commit[:12]} has no packaged patch artifact")
            continue
        with open(p, "rb") as fh:
            packaged = fh.read()
        want = commit_patch_bytes(".", c.commit)
        if packaged != want:
            errors.append(
                f"packaged patch for commit {c.commit[:12]} is not the repository's patch bytes")
        got = _h.sha256(packaged).hexdigest()
        if got != c.patch_sha256:
            errors.append(
                f"packaged patch for commit {c.commit[:12]} hashes to {got[:12]}, but the chain "
                f"records {c.patch_sha256[:12]}")

    present = {n for n in os.listdir(pdir) if n.endswith(".patch")}
    for extra in sorted(present - expected_names):
        errors.append(f"{COMMIT_PATCH_DIRNAME}/ carries {extra!r}, which no chain commit names")
    if len(present) != len(actual):
        errors.append(
            f"{COMMIT_PATCH_DIRNAME}/ holds {len(present)} patch file(s) for {len(actual)} "
            f"commit(s)")
    return errors


def _verify_commit_chain(evidence_dir: str, per_task_union: set) -> list:
    """Round 15 (F7): the packaged commit history is recomputed, not narrated.

    The operator's handoff used to say "there were six commits" in prose. A reader could not check
    that, could not tell whether an unrelated commit had been swept in, and could not tell whether
    the packaged history actually ends at the reviewed HEAD. So the chain is an artifact, and this
    recomputes it from the repository and holds the artifact to it.
    """
    errors: list = []
    chain = _mc_read_json(evidence_dir, "review_commit_chain.json")
    subject = _mc_read_json(evidence_dir, "review_subject.json")
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

    errors.extend(_verify_commit_patches(evidence_dir, actual))
    errors.extend(_verify_review_subject_records(evidence_dir, subject, base))

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
    evidence_dir: str, tid: str, mrp: dict, proof: dict, fjr: dict,
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

    safe_diff_path = os.path.join(evidence_dir, "task_runs", tid, "safe.diff")
    try:
        with open(safe_diff_path, encoding="utf-8") as f:
            safe_content = f.read()
    except OSError:
        return [f"{tid}: safe.diff unreadable"]

    # 8: empty / whitespace-only safe.diff is rejected.
    if not safe_content.strip():
        errors.append(f"{tid}: safe.diff is empty")

    untracked = mrp.get("untracked_file_hashes") or []
    tracked_sha = str(mrp.get("tracked_diff_sha256") or "")

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
    rsp = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "review_scope_packet.json"))
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


def validate_manual_completion(evidence_dir: str) -> list[str]:
    """Strictly and independently validate a manual-only completion candidate.

    Returns a list of human-readable errors; empty means authoritative. Every
    condition below is checked independently so any single tampering (a flag, a
    call count, a task id, a changed-file set, the changed-file union, a root
    test exit code / failure count, a content-proof hash, the job id, a
    provenance hash, or task overlap) invalidates the candidate.
    """
    errors: list[str] = []
    manifest = _mc_read_json(evidence_dir, "manifest.json")
    fjr = _mc_read_json(evidence_dir, "final_job_review.json")
    proof = _mc_read_json(evidence_dir, "current_change_content_proof.json")
    fv = _mc_read_json(evidence_dir, "final_verifier_report.json")
    cp = _mc_read_json(evidence_dir, "change_provenance_gate.json")
    vt = _mc_read_json(evidence_dir, "verification_tests.json")

    package_job_id = str(manifest.get("job_id") or "")
    planned_task_ids = [str(t) for t in (manifest.get("task_ids") or [])]
    task_dirs = _mc_task_dirs(evidence_dir)

    # 14 + planned-task coverage: package job id must equal the completion job id
    # and every planned task must have exactly one task run.
    fjr_job_id = str(fjr.get("job_id") or "")
    if not package_job_id:
        errors.append("manifest.json: job_id is empty")
    if fjr_job_id != package_job_id:
        errors.append(f"job_id mismatch: manifest={package_job_id!r} final_job_review={fjr_job_id!r}")
    if planned_task_ids and sorted(task_dirs) != sorted(planned_task_ids):
        errors.append(f"task runs {sorted(task_dirs)} != planned tasks {sorted(planned_task_ids)}")

    # completion facts on the existing final job review
    if fjr.get("completion_mode") != "manual_operator_repair":
        errors.append("final_job_review.completion_mode != manual_operator_repair")
    if fjr.get("human_final_reviewer_required") is not True:
        errors.append("final_job_review.human_final_reviewer_required is not true")
    if fjr.get("completion_provider_call_count", -1) != 0:
        errors.append("final_job_review.completion_provider_call_count != 0")

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
        # provider_call_count may be null (unknown) but must be present.
        if "provider_call_count" not in s:
            errors.append(f"linked job {s.get('job_id')!r} summary missing provider_call_count")
        if not s.get("status"):
            errors.append(f"linked job {s.get('job_id')!r} summary missing status")

    # per-task attestation validity + union of changed files
    per_task_union: set[str] = set()
    overlap_owner: dict[str, str] = {}
    for tid in task_dirs:
        rv = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "review.json"))
        pe = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "provider_evidence.json"))
        mrp = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "manual_repair_provenance.json"))
        safe_diff = os.path.join(evidence_dir, "task_runs", tid, "safe.diff")

        if str(rv.get("final_verdict") or rv.get("verdict") or "") != "operator_attested":
            errors.append(f"{tid}: review verdict is not operator_attested")
        if rv.get("human_final_reviewer_required") is not True:
            errors.append(f"{tid}: review.human_final_reviewer_required is not true")

        if pe.get("execution_mode") != "manual_operator_repair":
            errors.append(f"{tid}: provider_evidence.execution_mode != manual_operator_repair")
        if pe.get("provider_call_count", -1) != 0:
            errors.append(f"{tid}: provider_evidence.provider_call_count != 0")
        if pe.get("actual_provider_available") is True:
            errors.append(f"{tid}: provider_evidence claims provider availability (provider-backed PASS)")

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
        if not os.path.isfile(safe_diff):
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
        errors.extend(_verify_task_provenance_integrity(evidence_dir, tid, mrp, proof, fjr))

        # ---- Finding 5: a task manifest may not claim evidence unavailable
        #      without an explicit effective operator-attested completion state.
        tm = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "manifest.json"))
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
    errors.extend(_verify_commit_chain(evidence_dir, per_task_union))

    # 8: root verification must exist, exit 0, >=1 passed, 0 failed.
    if not vt:
        errors.append("verification_tests.json missing")
    else:
        if vt.get("exit_code", -1) != 0:
            errors.append(f"root verification exit_code != 0 ({vt.get('exit_code')})")
        if int(vt.get("passed", 0) or 0) < 1:
            errors.append("root verification passed < 1")
        if int(vt.get("failed", 0) or 0) != 0:
            errors.append(f"root verification failed != 0 ({vt.get('failed')})")

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


def _read_evidence_gate(evidence_dir: str, filename: str) -> dict:
    """Read a gate JSON from the evidence dir, or {} if absent."""
    path = os.path.join(evidence_dir, filename)
    if os.path.isfile(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _read_fresh_evidence_gate(evidence_dir: str) -> dict:
    return _read_evidence_gate(evidence_dir, "fresh_evidence_gate.json")


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
_SUPPORTED_GATE_VERSIONS = frozenset({"1.0.0"})
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
        "checks", "checks_passed", "checks_total", "issues", "schema_version", "verdict"}),
    "manifest_integrity.json": frozenset({"failures", "notes", "ok", "schema_version"}),
    "postmortem_integrity.json": frozenset({"failures", "ok", "schema_version"}),
    "commit_execution_gate.json": frozenset({
        "blocked_gates", "gate_checks", "issues", "non_pass_gates", "promote_ready",
        "schema_version", "verdict"}),
}
_RUNTIME_CHECK_FIELDS = frozenset({"check_id", "check_type", "file_missing", "found", "pattern",
                                   "source_file"})
_RUNTIME_CHECK_TYPES = frozenset({"call_exists"})
#: The FV's OWN commit-readiness view (distinct from the packaged commit gate's verdict); a
#: pre-acceptance package must never claim it is auto-promotable.
_FV_COMMIT_NOT_READY = frozenset({"BLOCKED", "NEEDS_HUMAN_APPROVAL", "NEEDS_APPROVAL",
                                  "NEEDS_REPAIR", "NEEDS_TESTS"})


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


def _scan_gate_metadata(gate, name: str) -> list[str]:
    """F5 (round 24): no trusted gate may carry a secret, a local absolute path or a control
    character in ANY textual field — scan every string value recursively with the shared scanners."""
    from packages.orchestration.run_manifest import _contains_local_path, _contains_secret
    problems: list[str] = []

    def _walk(value, path):
        if isinstance(value, str):
            if _contains_secret(value):
                problems.append(f"{name} field {path} carries a secret")
            elif _contains_local_path(value):
                problems.append(f"{name} field {path} carries a local absolute path")
            elif any(ord(c) < 32 and c not in "\t\n\r" for c in value):
                problems.append(f"{name} field {path} carries a control character")
        elif isinstance(value, dict):
            for k, v in value.items():
                _walk(v, f"{path}.{k}")
        elif isinstance(value, list):
            for i, v in enumerate(value):
                _walk(v, f"{path}[{i}]")

    _walk(gate, name.replace(".json", ""))
    return problems


def _gate_closed_schema_problems(name: str, gate: dict) -> list[str]:
    """F1 (round 24): version-closed + closed allowed-field set + metadata safety."""
    problems: list[str] = []
    if _gget(gate, "schema_version") not in _SUPPORTED_GATE_VERSIONS:
        problems.append(f"{name} schema_version {gate.get('schema_version')!r} is not supported "
                        f"{sorted(_SUPPORTED_GATE_VERSIONS)}")
    allowed = _GATE_ALLOWED_FIELDS.get(name)
    if allowed is not None:
        extra = set(gate) - allowed
        if extra:
            problems.append(f"{name} has unknown field(s) {sorted(extra)} (schema is closed)")
    problems.extend(_scan_gate_metadata(gate, name))
    return problems


def _gate_semantic_problems(name: str, gate: dict, verdicts: dict) -> list[str]:
    """F1/F2/F3 (round 24): the gate's PASS label must be consistent with its complete internal
    body, and (final_verifier) its embedded gate verdicts must equal the separately packaged
    gates."""
    problems = _gate_closed_schema_problems(name, gate)

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
            ("final_job_review_findings", [])]))
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
        return problems

    if name == "fresh_evidence_gate.json":
        problems.extend(_check_fields(gate, name, [
            ("evidence_authoritative", True), ("job_id_match", True), ("plan_match", True),
            ("live_review_match", True), ("evidence_validity.has_job_id", True),
            ("evidence_validity.has_manifest", True),
            ("evidence_validity.is_valid_current_run", True),
            ("evidence_freshness.is_fresh", True), ("evidence_freshness.job_id_match", True),
            ("evidence_freshness.step_range_match", True), ("issues", [])]))
        return problems

    if name == "artifact_contract_gate.json":
        problems.extend(_check_fields(gate, name, [
            ("missing_required", []), ("fv_referenced_missing", []), ("critical_fv_missing", []),
            ("issues", []), ("job_id_fresh", True)]))
        req = gate.get("required_artifacts")
        if not isinstance(req, dict):
            problems.append(f"{name} required_artifacts is not an object")
        else:
            for k, v in req.items():
                if v is not True:
                    problems.append(f"{name} required_artifacts[{k!r}]={v!r} is not true")
        return problems

    if name == "change_provenance_gate.json":
        problems.extend(_check_fields(gate, name, [
            ("uncovered_files", []), ("content_hash_verified", True), ("hash_mismatches", []),
            ("stale_apply_proofs", []), ("issues", [])]))
        return problems

    if name == "runtime_integration_gate.json":
        problems.extend(_check_fields(gate, name, [("issues", [])]))
        checks = gate.get("checks")
        if not isinstance(checks, list):
            problems.append(f"{name} checks is not a list")
        else:
            ids: set = set()
            for i, c in enumerate(checks):
                if not isinstance(c, dict) or set(c) != _RUNTIME_CHECK_FIELDS:
                    problems.append(f"{name} check[{i}] has the wrong field set")
                    continue
                cid = c.get("check_id")
                if not isinstance(cid, str) or not cid:
                    problems.append(f"{name} check[{i}] check_id is empty")
                elif cid in ids:
                    problems.append(f"{name} duplicate check_id {cid!r}")
                else:
                    ids.add(cid)
                if c.get("check_type") not in _RUNTIME_CHECK_TYPES:
                    problems.append(f"{name} check {cid!r} check_type {c.get('check_type')!r} "
                                    f"is not supported")
                if not _safe_rel_path(c.get("source_file")):
                    problems.append(f"{name} check {cid!r} source_file is not a safe relative path")
                if c.get("found") is not True:
                    problems.append(f"{name} check {cid!r} found is not true")
                if c.get("file_missing") is not False:
                    problems.append(f"{name} check {cid!r} file_missing is not false")
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


#: The commit gate's embedded gate_checks keys → the READY-matrix gate file whose verdict must match.
_COMMIT_CHECK_TO_GATE = {
    "final_verifier": "final_verifier_report.json",
    "fresh_evidence_gate": "fresh_evidence_gate.json",
    "artifact_contract_gate": "artifact_contract_gate.json",
    "change_provenance_gate": "change_provenance_gate.json",
    "runtime_integration_gate": "runtime_integration_gate.json",
}


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
    if gate.get("blocked_gates") != []:
        problems.append(f"{_COMMIT_GATE} blocked_gates {gate.get('blocked_gates')!r} is nonempty")
    checks = gate.get("gate_checks")
    if not isinstance(checks, dict) or set(checks) != set(_COMMIT_CHECK_TO_GATE):
        problems.append(f"{_COMMIT_GATE} gate_checks keys must be exactly "
                        f"{sorted(_COMMIT_CHECK_TO_GATE)}")
    else:
        for k, gate_file in _COMMIT_CHECK_TO_GATE.items():
            if gate_file in verdicts and checks[k] != verdicts[gate_file]:
                problems.append(f"{_COMMIT_GATE} gate_checks[{k!r}]={checks[k]!r} != packaged "
                                f"{verdicts[gate_file]!r}")
        derived_non_pass = sorted(k for k in checks if checks[k] != "PASS")
        if sorted(gate.get("non_pass_gates") or []) != derived_non_pass:
            problems.append(f"{_COMMIT_GATE} non_pass_gates {gate.get('non_pass_gates')!r} != "
                            f"the derived {derived_non_pass}")
    return problems


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
        if g.get("verdict") not in allowed:
            reasons.append(f"{name} verdict {g.get('verdict')!r} is not in {sorted(allowed)}")
            continue
        reasons.extend(_gate_semantic_problems(name, g, verdicts))

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
        reasons.extend(_gate_semantic_problems(name, g, verdicts))

    if cg is not _MISSING:
        reasons.extend(_validate_commit_gate(cg, verdicts))

    return {"ok": not reasons, "gate_verdicts": verdicts, "blocking_reasons": reasons}


def _evidence_dir_gate_loader(evidence_dir: str):
    """A load_json for evaluate_ready_gate_matrix that reads the (staged) evidence dir, raising on
    invalid JSON so a corrupt gate BLOCKS rather than silently passing."""
    def _load(name: str):
        path = os.path.join(evidence_dir, name)
        if not os.path.isfile(path):
            return None
        with open(path, "rb") as fh:
            return json.loads(fh.read())     # raises json.JSONDecodeError on invalid
    return _load


def _build_alignment(
    dirty_files: list[str], evidence_dir: str,
) -> dict:
    """Build review_subject/evidence alignment proof."""
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

    cp_gate = _read_evidence_gate(evidence_dir, "change_provenance_gate.json")
    fv_report = _read_evidence_gate(evidence_dir, "final_verifier_report.json")
    ce_gate = _read_evidence_gate(evidence_dir, "commit_execution_gate.json")
    ac_gate = _read_evidence_gate(evidence_dir, "artifact_contract_gate.json")

    cp_covered = sorted(cp_gate.get("covered_files", []))
    fv_changed = sorted(fv_report.get("authoritative_changed_files", []))
    hash_mismatches = cp_gate.get("hash_mismatches", [])

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


def validate_evidence_candidate(evidence_dir: str) -> dict:
    errors: list[str] = []
    missing_root: list[str] = []
    missing_task: dict[str, list[str]] = {}

    manual_completion = _is_manual_completion(evidence_dir)
    manual_completion_errors: list[str] = []
    not_applicable_root: list[str] = []

    if manual_completion:
        # Strict, independent validation of the manual-completion contract.
        # Any mismatch invalidates the candidate and blocks authoritativeness.
        manual_completion_errors = validate_manual_completion(evidence_dir)
        errors.extend(manual_completion_errors)

    for art in REQUIRED_ROOT_ARTIFACTS:
        if os.path.isfile(os.path.join(evidence_dir, art)):
            continue
        if manual_completion and art in MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS:
            # A deterministic manual-only completion legitimately has no
            # provider-flow root artifact — mark not-applicable, never missing.
            not_applicable_root.append(art)
            continue
        missing_root.append(art)
        errors.append(f"missing root artifact: {art}")

    jf_path = os.path.join(evidence_dir, "job_flow.json")
    job_id = ""
    final_audit_status = ""
    missing_obs: list[str] = []
    target_mutation_detected = False

    if manual_completion and not os.path.isfile(jf_path):
        # Derive identity/verdict from the existing final job review + final
        # verifier, without fabricating a provider job_flow.json.
        fjr = _mc_read_json(evidence_dir, "final_job_review.json")
        manifest_obj = _mc_read_json(evidence_dir, "manifest.json")
        job_id = str(fjr.get("job_id") or manifest_obj.get("job_id") or "")
        if not job_id:
            errors.append("manual completion: job_id could not be derived")
        fv = _read_evidence_gate(evidence_dir, "final_verifier_report.json")
        final_audit_status = str(fv.get("verdict", "") or "")
        if not final_audit_status:
            errors.append("final_verifier_report.json: verdict missing")

    if os.path.isfile(jf_path):
        try:
            with open(jf_path) as f:
                jf_data = json.load(f)
            job_id = jf_data.get("job_id", "")
            if not job_id:
                errors.append("job_flow.json: job_id is empty")
            audit = jf_data.get("final_audit", {})
            final_audit_status = audit.get("status", "")
            if not final_audit_status:
                errors.append("job_flow.json: final_audit.status missing")
            missing_obs = audit.get("missing_observability_artifacts", [])
            if missing_obs:
                errors.append(
                    f"final_audit.missing_observability_artifacts: {missing_obs}"
                )
            tg = jf_data.get("target_guard", {})
            if tg.get("mutated_target", False):
                target_mutation_detected = True
                errors.append("target_guard indicates target mutation")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"job_flow.json: parse error: {exc}")

    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    task_run_count = 0
    manual_repair_tasks: list[str] = []
    if os.path.isdir(task_runs_dir):
        for entry in sorted(os.listdir(task_runs_dir)):
            task_path = os.path.join(task_runs_dir, entry)
            if not os.path.isdir(task_path):
                continue
            task_run_count += 1
            mrp_path = os.path.join(task_path, "manual_repair_provenance.json")
            is_manual_repair = os.path.isfile(mrp_path)
            if is_manual_repair:
                try:
                    with open(mrp_path) as f:
                        mrp = json.load(f)
                    if not (isinstance(mrp, dict) and mrp.get("manual_operator_repair") is True
                            and mrp.get("no_provider_calls") is True):
                        is_manual_repair = False
                        errors.append(
                            f"task_runs/{entry}: manual_repair_provenance.json invalid"
                        )
                except (json.JSONDecodeError, OSError):
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
                if not os.path.isfile(os.path.join(task_path, art)):
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
    evidence_dir: str | None,
    source_root: str,
) -> dict:
    result: dict = {
        "current_content_hash_checked": False,
        "current_content_hash_mismatches": [],
        "current_content_hash_missing_proofs": [],
        "packaged_file_hashes": {},
        "verdict": "PASS",
    }

    if not evidence_dir or not os.path.isdir(evidence_dir):
        return result

    proof_path = os.path.join(
        evidence_dir, "current_change_content_proof.json"
    )
    if not os.path.isfile(proof_path):
        return result

    try:
        proof = json.loads(open(proof_path).read())
    except (json.JSONDecodeError, OSError):
        return result

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
    import stat as _stat

    kinds: dict[str, str] = {}
    link_targets: dict[str, str] = {}
    subj = _mc_read_json(evidence_dir, "review_subject.json") if evidence_dir else {}
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
) -> dict:
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _git(["rev-parse", "HEAD"])
    has_commits_val = _has_commits()
    dirty = _dirty_files()
    has_untracked = _has_untracked_files()

    review_subject = _classify_review_subject(
        branch, commit, dirty, has_untracked, has_commits_val,
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

    if evidence_dir and os.path.isdir(evidence_dir):
        for artifact_name in root_artifacts:
            root_artifacts[artifact_name] = _check(
                os.path.join(evidence_dir, artifact_name)
            )
        task_runs = _scan_task_runs(evidence_dir)
        job_id = _read_job_id(evidence_dir)
        audit = _read_final_audit(evidence_dir)
        trace_sources = _read_trace_sources(evidence_dir)

        validation = validate_evidence_candidate(evidence_dir)

        fresh_gate = _read_fresh_evidence_gate(evidence_dir)
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
    if evidence_dir and os.path.isdir(evidence_dir):
        alignment = _build_alignment(dirty, evidence_dir)
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

    if evidence_dir:
        ev_resolved = os.path.realpath(evidence_dir)
        if not contained(source_root, evidence_dir):
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
        gate_matrix = evaluate_ready_gate_matrix(_evidence_dir_gate_loader(evidence_dir))
        if not gate_matrix["ok"]:
            packaging_warnings.append(
                "gate matrix not satisfied: " + "; ".join(gate_matrix["blocking_reasons"][:4]))

    if evidence_valid and alignment_ok and containment_ok and gate_matrix["ok"]:
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
    if evidence_dir and os.path.isdir(evidence_dir):
        ev_mf_path = os.path.join(evidence_dir, "manifest.json")
        if os.path.isfile(ev_mf_path):
            try:
                ev_mf = json.loads(open(ev_mf_path).read())
                ev_manifest_task_count = ev_mf.get("task_count", 0)
                ev_manifest_task_ids = ev_mf.get("task_ids", [])
                ev_manifest_job_id = ev_mf.get("job_id", "")
                ev_manifest_mtime = datetime.fromtimestamp(
                    os.path.getmtime(ev_mf_path), tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
            except (json.JSONDecodeError, OSError):
                packaging_warnings.append(
                    "evidence manifest.json unreadable"
                )

    # Review-bundle integrity: compare packaged files against content proof
    bundle_integrity = _check_bundle_integrity(evidence_dir, source_root)
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

    _subject = _mc_read_json(evidence_dir, "review_subject.json") if evidence_dir else {}
    _chain = _mc_read_json(evidence_dir, "review_commit_chain.json") if evidence_dir else {}
    _proof_doc = _mc_read_json(evidence_dir, "current_change_content_proof.json") \
        if evidence_dir else {}

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
        "review_subject": review_subject,
        "review_state": review_state,
        "review_subject_evidence_alignment": alignment,
        "packaged_evidence_dir": (
            _shareable_path(evidence_dir, source_root) if evidence_dir else ""
        ),
        "packaged_evidence_job_id": ev_manifest_job_id,
        "packaged_evidence_manifest_task_count": ev_manifest_task_count,
        "packaged_evidence_manifest_task_ids": ev_manifest_task_ids,
        "packaged_evidence_modified_at": ev_manifest_mtime,
        "source_root": SOURCE_ROOT_TOKEN,
        "packaging_command_context": {
            "cwd": _shareable_path(cwd, source_root),
            "evidence_dir_arg": (
                _shareable_path(evidence_dir, source_root) if evidence_dir else ""
            ),
        },
        "source_root_containment": {
            "verdict": containment_verdict,
            "blockers": containment_blockers,
        },
        "external_paths_detected": external_paths,
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
    args = parser.parse_args()

    manifest = build_manifest(
        args.evidence_dir,
        selection_mode=args.selection_mode,
        selection_reason=args.selection_reason,
        candidate_count=args.candidate_count,
        selected_mtime=args.selected_mtime,
        rejected_candidate_count=args.rejected_candidate_count,
    )
    out = json.dumps(manifest, indent=2) + "\n"

    if args.output == "-":
        sys.stdout.write(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
