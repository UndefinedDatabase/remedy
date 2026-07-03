---
description: Use for Remedy evidence pipeline, review zip, manifest building, and job evidence inspection. Covers make_review_zip.sh, build_review_manifest.py, job_flow.json, final_verifier, and token_truth.
---

# Remedy Evidence & Review Skill

## Evidence Pipeline
```
Job run → evidence dir (remedy-job-evidence-*/) → review zip → manifest.json
```

Evidence dirs are ephemeral build artifacts (gitignored). Review zips are also gitignored (`remedy-review-*`).

## Key Files
- `scripts/make_review_zip.sh` — builds review zip package (works with or without evidence dirs)
- `scripts/build_review_manifest.py` — generates JSON manifest
- `packages/orchestration/job_evidence.py` — evidence bundle builder
- `packages/orchestration/final_verifier.py` — final verification gate
- `packages/orchestration/token_truth.py` — actual vs estimated token tracking
- `packages/orchestration/fresh_evidence_gate.py` — fresh evidence commit gate
- `apps/cli/commands/do_cmd.py` — `_build_final_audit()` reads verifier report

## Evidence Dir Structure
```
remedy-job-evidence-{id}/
  job_flow.json              — main job record (job_id, final_audit, promote_ready)
  manifest.json              — evidence manifest
  agent_run_trace.jsonl      — raw trace
  agent_run_trace_summary.json
  prompt_trace_summary.json
  command_transcript.json
  final_verifier_report.json — verifier verdict
  token_truth.json           — actual/estimated token split
  scratch_file_guard.json    — scratch file check
  task_runs/
    T001/
      prompt_trace.jsonl
      prompt_trace_summary.json
      review.json
      repair_loop.json
      token_accounting.json
      provider_evidence.json
      missing_tests_gate.json
```

## Manifest Status Values
- `READY_FOR_REVIEW` — evidence valid, alignment OK, containment OK
- `NO_EVIDENCE` — no evidence dir found (zip still builds)
- `BLOCKED_EVIDENCE` — evidence incomplete or validation failed

## Verification Gates
- **final_verifier**: drives `final_audit.status` and `promote_ready` in job_flow.json
- **missing_tests_gate**: checks test execution (sandbox-blocked = NEEDS_TESTS, not PASS)
- **token_truth**: never cross-contaminates estimated into actual fields
- **scratch_file_guard**: checks for leftover scratch files
- **fresh_evidence_gate**: commit readiness gate

## Review Zip Building
```bash
bash scripts/make_review_zip.sh   # auto-selects latest evidence or builds without
```

## Inspecting Evidence
```bash
python3 -c "import json; print(json.dumps(json.load(open('remedy-job-evidence-xxx/job_flow.json')), indent=2))" | head -50
```

## Safety
- Evidence dirs are build artifacts — delete freely, they're gitignored
- Never fabricate evidence
- `promote_ready=false` when verifier says NEEDS_REPAIR or NEEDS_TESTS
