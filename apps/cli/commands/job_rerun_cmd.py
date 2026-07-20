"""`remedy job rerun <id> --check-manifest` — F012 drift verification (hardened).

Re-executes nothing. Loads the run-input manifest a job episode recorded, freshly rebuilds
the manifest the CURRENT environment WOULD produce (current target HEAD/tree, current
config/env/models, current Remedy identity), diffs the two, and reports drift split into
blocking and informational — with an honest coverage state.

Exit codes:
* 0 — verification COMPLETE and no blocking drift (same inputs, fully verified);
* 4 — confirmed blocking drift;
* 5 — no blocking drift found, but per-call input coverage is INCOMPLETE (check-only mode
      cannot reconstruct assembled prompts without a worktree replay — F140), so "same
      inputs" could not be fully verified;
* 3 — unknown job; 2 — usage; 1 — missing/corrupt required manifest.

The honesty rule is printed on every check:

    Inputs are reproducible and verified; LLM outputs are recorded, not promised.
"""
from __future__ import annotations

import json as _json
import sys

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_UNKNOWN_JOB = 3
EXIT_BLOCKING_DRIFT = 4
EXIT_INCOMPLETE_COVERAGE = 5

HONESTY = ("Inputs are reproducible and verified; LLM outputs are recorded, "
           "not promised.")
CHECK_ONLY = "Manifest check only — this command did not re-execute the job."
INCOMPLETE = "Input equality could not be fully verified."


def _cmd_job_rerun(job_id: str, *, check_manifest: bool = False,
                   json_output: bool = False) -> None:
    from packages.orchestration.pingpong_job import job_evidence_dir, load_job_plan
    from packages.orchestration.run_manifest import (
        build_current_candidate,
        diff_manifests,
        load_latest_manifest_for_cli,
    )
    from packages.orchestration.safe_points import StopControlError, validate_job_id

    job_id = (job_id or "").strip()
    try:
        validate_job_id(job_id)
    except StopControlError as exc:
        _fail(EXIT_USAGE, "invalid_job_id", str(exc), json_output)

    if not check_manifest:
        _fail(EXIT_USAGE, "check_manifest_required",
              "remedy job rerun currently supports only --check-manifest "
              "(it does not re-execute a job)", json_output)

    job = load_job_plan(job_id)
    if job is None:
        _fail(EXIT_UNKNOWN_JOB, "job_not_found", f"job not found: {job_id}", json_output)

    ev = job_evidence_dir(job_id)
    # F10: load the CANONICAL latest episode through the ANCHORED, typed loader — NO name-based
    # `Path.is_file()` precheck. A tree with no F012 manifest at all is a legacy/uncovered job
    # (`no_manifest`); a tree with manifest artifacts whose chain is partial/corrupt is an
    # INTEGRITY ERROR (exit 1), never mistaken for a missing manifest, drift (4) or incomplete
    # coverage (5).
    load = load_latest_manifest_for_cli(ev, job_id=job_id)
    if load.kind == "no_manifest":
        _fail(EXIT_ERROR, "no_manifest",
              f"job {job_id} has no run manifest (was it completed or stopped under F012?)",
              json_output)
    if load.kind == "integrity_error":
        _fail(EXIT_ERROR, "manifest_integrity", load.detail, json_output)
    reference = load.manifest

    candidate = build_current_candidate(reference, job)
    diff = diff_manifests(reference, candidate)

    blocking = diff["blocking"]
    complete = diff["verification_complete"]
    if blocking:
        exit_code = EXIT_BLOCKING_DRIFT
    elif complete:
        exit_code = EXIT_OK
    else:
        exit_code = EXIT_INCOMPLETE_COVERAGE

    if json_output:
        print(_json.dumps({
            "job_id": job_id,
            "check_only": True,
            "honesty": HONESTY,
            "episode_id": reference.episode_id,
            "same_inputs": diff["same_inputs"],
            "verification_complete": complete,
            "logical_input_match": diff["logical_input_match"],
            "reference_logical_input_sha256": reference.logical_input_sha256(),
            "candidate_logical_input_sha256": candidate.logical_input_sha256(),
            "blocking": blocking,
            "informational": diff["informational"],
            "coverage": diff["coverage"],
            "warnings": diff.get("warnings", []),
        }, indent=2))
        raise SystemExit(exit_code)

    print(f"Run manifest check — job {job_id} (episode {reference.episode_id})")
    print(CHECK_ONLY)
    print(HONESTY)
    print()
    print(f"Blocking drift ({len(blocking)})")
    if blocking:
        for e in blocking:
            print(f"  {e['field']} [{e['category']}]: "
                  f"{_show(e['reference'])} -> {_show(e['candidate'])}")
    else:
        print("  none — the recorded blocking inputs match the current would-be inputs")
    info = diff["informational"]
    print(f"Informational drift ({len(info)})")
    for e in info:
        print(f"  {e['field']} [{e['category']}]: "
              f"{_show(e['reference'])} -> {_show(e['candidate'])}")
    cov = diff["coverage"]
    # F9 (round 12): TWO dimensions, named separately. "Every call compared" and "every material
    # input known" are different claims, and an operator needs to see WHICH one is short.
    call_status = cov.get("call_status", "complete" if complete else "incomplete")
    input_status = cov.get("input_status", "complete")
    if not complete:
        print("Coverage: INCOMPLETE")
        print(f"  call inputs:     {str(call_status).upper()}")
        if call_status != "complete":
            print(f"    {cov.get('reason', 'per-call inputs not reconstructed')}")
        print(f"  material inputs: {str(input_status).upper()}")
        for prob in (cov.get("input_problems") or [])[:5]:
            print(f"    {prob}")
    else:
        print("Coverage: COMPLETE (call inputs and material inputs)")
    print()
    if blocking:
        print("Result: BLOCKING DRIFT — the current inputs are not the recorded inputs.")
    elif complete:
        print("Result: same inputs (fully verified).")
    else:
        print(f"Result: {INCOMPLETE}")
    raise SystemExit(exit_code)


def _show(value) -> str:
    if value is None:
        return "(not available)"
    text = str(value)
    return text if len(text) <= 80 else text[:77] + "..."


def _fail(code: int, error: str, message: str, json_output: bool) -> None:
    if json_output:
        print(_json.dumps({"ok": False, "error": error, "message": message}, indent=2))
    else:
        print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


COMMAND_HANDLERS = {
    "job.rerun": lambda args: _cmd_job_rerun(
        getattr(args, "job_id", "") or "",
        check_manifest=bool(getattr(args, "check_manifest", False)),
        json_output=bool(getattr(args, "json", False)),
    ),
}
