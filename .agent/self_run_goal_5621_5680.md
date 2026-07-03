# Steps 5621-5680: Run Freshness + Artifact Contract + Commit Execution Gate v1

## Product goal

Add fresh evidence gate, artifact contract gate, runtime integration gate,
commit execution gate, change provenance gate, token truth per-call roles,
final verifier integration for all new gates, and review zip freshness check.

## Hard constraints

- Do NOT fake provider token usage.
- Do NOT reuse old evidence as proof.
- Do NOT auto-push or auto-merge.
- Do NOT change review zip filename behavior.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures.
- Do NOT label estimated tokens as exact/actual.
- Do NOT copy estimated values into `actual_*` fields.

---

## Task 1: Verify fresh evidence gate

### Files allowed

- `packages/orchestration/fresh_evidence_gate.py` (read)
- `tests/orchestration/test_fresh_evidence_gate.py` (read)

### Acceptance

- `fresh_evidence_gate.py` exists and compiles
- `build_fresh_evidence_gate` blocks when job_id mismatches
- `build_fresh_evidence_gate` blocks when step range is empty
- `build_fresh_evidence_gate` blocks when step range mismatches
- Output includes evidence_freshness, evidence_validity, evidence_authoritative
- Test file has at least 8 tests
- All tests pass

## Task 2: Verify artifact contract gate

### Files allowed

- `packages/orchestration/artifact_contract_gate.py` (read)
- `tests/orchestration/test_artifact_contract_gate.py` (read)

### Acceptance

- `artifact_contract_gate.py` exists and compiles
- CORE_ARTIFACTS includes fresh_evidence_gate.json, runtime_integration_gate.json, change_provenance_gate.json, final_verifier_report.json
- `build_artifact_contract_gate` blocks when required artifact missing
- `build_artifact_contract_gate` blocks when fv_referenced_missing contains critical items
- Test file has at least 9 tests
- All tests pass

## Task 3: Verify runtime integration gate

### Files allowed

- `packages/orchestration/runtime_integration_gate.py` (read)
- `tests/orchestration/test_runtime_integration_gate.py` (read)

### Acceptance

- `runtime_integration_gate.py` exists and compiles
- `check_call_exists` skips comments and def lines
- `build_runtime_integration_gate` blocks when call_exists fails
- Test file has at least 10 tests
- All tests pass

## Task 4: Verify commit execution gate

### Files allowed

- `packages/orchestration/commit_execution_gate.py` (read)
- `tests/orchestration/test_commit_execution_gate.py` (read)

### Acceptance

- `commit_execution_gate.py` exists and compiles
- Empty verdict causes BLOCKED (not silently pass)
- change_provenance_verdict parameter exists and BLOCKED causes BLOCKED
- FORBIDDEN_FILE_PATTERNS includes `_[!_]*.py`
- Test file has at least 11 tests
- All tests pass

## Task 5: Verify token truth per-call roles

### Files allowed

- `packages/orchestration/token_truth.py` (read)
- `tests/orchestration/test_token_truth.py` (read)

### Acceptance

- Per-task records include `role` field (builder/reviewer/repair)
- Per-task records include `actual_tokens` dict (None when unavailable)
- Estimated values never in actual_* fields
- Test file has at least 9 tests
- All tests pass

## Task 6: Verify final verifier integration

### Files allowed

- `packages/orchestration/final_verifier.py` (read)
- `tests/orchestration/test_final_verifier.py` (read)

### Acceptance

- Final verifier reads fresh_evidence_gate, artifact_contract_gate, runtime_integration_gate, change_provenance_gate, commit_execution_gate
- BLOCKED gate causes final verifier verdict BLOCKED
- Gate values exposed as non-null in output when gate files exist
- Test file covers all 5 gate readings plus none test
- All tests pass

## Task 7: Verify change provenance gate

### Files allowed

- `packages/orchestration/change_provenance_gate.py` (read)
- `tests/orchestration/test_change_provenance_gate.py` (read)

### Acceptance

- `change_provenance_gate.py` exists and compiles
- `build_change_provenance_gate` returns PASS when all dirty files covered by evidence
- `build_change_provenance_gate` returns BLOCKED when dirty source files have no evidence proof
- `build_change_provenance_gate` returns PASS_WITH_RISKS when no source changes
- Excluded patterns filter out evidence dirs, caches, transcripts
- Test file has at least 6 tests
- All tests pass

## Task 8: Verify job evidence writes all gates

### Files allowed

- `packages/orchestration/job_evidence.py` (read)
- `tests/orchestration/test_job_evidence.py` (read)

### Acceptance

- job_evidence.py calls write_fresh_evidence_gate
- job_evidence.py calls write_artifact_contract_gate
- job_evidence.py calls write_runtime_integration_gate
- job_evidence.py calls write_change_provenance_gate
- job_evidence.py calls write_commit_execution_gate
- job_evidence.py calls write_final_verifier_report (twice: draft + refresh)
- fresh_evidence_gate receives non-empty step range from _derive_step_range
- All tests pass
