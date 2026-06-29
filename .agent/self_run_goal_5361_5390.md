# Job: Review Scope Packet + Test Gate + Final Verifier v1

Steps 5361-5390

Previous runs proved Remedy can develop, review, and apply its own code. This run adds a token-saving review layer, a missing-tests gate, and a deterministic final verifier.

## Task 1: Implement Review Scope Packet

Create a review scope packet generator that produces `review_scope_packet.json` (and optional `review_scope_packet.md`) for every task review and the final job review.

The packet must contain:
- `changed_files`: list of files modified by the builder
- `changed_line_ranges`: per-file list of `{start, end}` line ranges from the diff
- `symbols_touched`: per-file list of functions/classes/methods touched, when detectable from the diff (best-effort; mark "detection_unavailable" if not parseable)
- `risk_tags`: per-file risk classification (e.g. "safety_critical", "orchestration", "test_only", "config", "new_file")
- `relevant_test_files`: per changed file, which test files are likely relevant (by naming convention or import analysis)
- `evidence_refs`: relative paths to safe.diff, review.json, repair_loop.json, token_accounting.json
- `prompt_hashes`: sha256 hashes of builder and reviewer prompts (from prompt_trace)
- `reviewer_target_files`: which files the reviewer actually needs to inspect
- `estimated_review_tokens`: estimated token cost for the focused review
- `broad_review_needed`: bool — true if the change touches safety-critical paths or cross-cutting concerns

Location: `scripts/build_review_scope_packet.py`

CLI: `python3 scripts/build_review_scope_packet.py --evidence-dir <path> --task <task_id>`
For job-level: `python3 scripts/build_review_scope_packet.py --evidence-dir <path> --job-level`

Requirements:
- Use safe relative paths only (no absolute local paths)
- Work on incomplete evidence (mark missing data as "absent")
- Do not include raw prompt text, raw diffs, or secrets
- Line range detection from unified diff format
- Symbol detection best-effort using simple heuristics (def/class lines in Python)
- Risk tagging based on file path patterns (packages/orchestration/* = orchestration, tests/* = test_only, etc.)

Acceptance:
- File exists at `scripts/build_review_scope_packet.py`
- CLI callable with --evidence-dir and --task
- Output is valid JSON
- Contains all required fields
- No absolute paths
- No raw prompts/secrets
- Works on incomplete evidence

## Task 2: Token-saving reviewer prompts

Update the reviewer prompt template so the reviewer receives focused context from the Review Scope Packet instead of broad file tree / README context.

The reviewer prompt should include:
- Task goal (from the task specification)
- Changed files list
- Changed line ranges per file
- Risk summary from the scope packet
- Focused diff or hunk references (the actual diff content the reviewer should inspect)
- Relevant test outputs (if tests ran)
- Explicit instruction: "Review only the changed files and their immediate context. Do not review unrelated files unless the risk summary indicates cross-cutting concerns."

The reviewer should NOT receive by default:
- Full file tree listing (unless broad_review_needed=true)
- Full README content
- Unrelated file contents

Find the reviewer prompt construction in `packages/orchestration/pingpong_loop.py` (look for the reviewer prompt builder, likely near `_build_reviewer_prompt` or similar). Modify it to use the scope packet when available, falling back to the existing behavior when no packet exists.

Requirements:
- Backward compatible: if no scope packet exists, use existing prompt format
- When scope packet exists, build a focused prompt
- Never remove information that the reviewer needs for safety assessment
- If `broad_review_needed=true` in the packet, include the broader context
- Log when focused mode is used vs. fallback mode

Acceptance:
- Reviewer prompt uses scope packet when available
- Fallback to existing format when no packet
- Focused prompt is measurably shorter (fewer estimated tokens)
- No loss of safety-critical review context
- Log message indicates which mode was used

## Task 3: Missing-tests gate

If a task changes code files (not just tests, docs, or config) and no test command ran during the task, Remedy must not silently mark the task or final job as clean.

Required behavior:
- After each task completes, check if code was changed AND tests were not run
- If so, mark the task as `verification_required` (not `staged_review_passed`)
- The final audit must be `NEEDS_TESTS` or `NEEDS_REVIEW`, not `READY_FOR_APPROVAL`
- Add a field `missing_test_coverage` to the task report listing which changed code files have no corresponding test execution
- Add a field `test_gate_status` to the final audit: "all_tested", "tests_missing", or "tests_not_applicable"

What counts as "code changed":
- Any file under `packages/`, `apps/`, `scripts/` that is NOT a test file
- Excludes: files under `tests/`, `docs/`, config files (pyproject.toml, .gitignore, etc.)

What counts as "tests ran":
- `test_passed` is not None in the task report
- OR test output files exist in the task evidence

Do NOT:
- Block the entire job flow — the job should complete, but with `NEEDS_TESTS` status
- Auto-generate or auto-run tests — just flag the gap
- Prevent the human from explicitly accepting the risk

Acceptance:
- Code change without tests → `NEEDS_TESTS` in final audit
- Code change with tests → `READY_FOR_APPROVAL` (if everything else passes)
- Test-only or doc-only change → no test gate triggered
- `missing_test_coverage` field present in task report
- `test_gate_status` field present in final audit
- Human can still approve via `--approve` even with `NEEDS_TESTS`

## Task 4: Final Verifier Gate

Add a deterministic final verifier that runs before the human approve decision.

Create: `scripts/build_final_verifier_report.py`

CLI: `python3 scripts/build_final_verifier_report.py --evidence-dir <path>`

It must read:
- `job_flow.json`
- `self_run_observability_index.json` (if present)
- `review_scope_packet.json` (if present, per-task or job-level)
- `command_transcript.json`
- `target_guard.json`
- `final_review_test_results.json` (if present)
- `task_runs/*/review.json` and `task_runs/*/repair_loop.json`
- `task_runs/*/token_accounting.json`

It must output: `final_verifier_report.json`

With fields:
- `verdict`: one of "PASS", "PASS_WITH_RISKS", "NEEDS_TESTS", "NEEDS_REPAIR", "BLOCKED"
- `changed_files`: list with line ranges if available
- `unresolved_findings`: list of findings not resolved by repair
- `test_status`: { "ran": bool, "passed": bool, "test_gate": "all_tested"|"tests_missing"|"tests_not_applicable" }
- `token_summary`: { "total_estimated": int, "builder_calls": int, "reviewer_calls": int, "repair_rounds": int }
- `safety_status`: { "target_mutated": bool, "target_content_mutated": bool, "guard_transcript_agree": bool }
- `evidence_completeness`: { "complete": bool, "missing_artifacts": list }
- `recommended_next_action`: string describing what the human should do next
- `verdict_reasons`: list of strings explaining why this verdict was chosen

Verdict logic:
- PASS: all tasks reviewed pass, tests ran and passed, no unresolved findings, evidence complete, guard/transcript agree
- PASS_WITH_RISKS: all tasks pass but tests not run OR minor evidence gaps
- NEEDS_TESTS: code changed without test coverage
- NEEDS_REPAIR: unresolved findings from reviewer
- BLOCKED: target mutation detected, guard/transcript disagree on content mutation, or critical evidence missing

Integrate into `do job-flow`: after observability index generation, run the final verifier. Store the result in evidence and reference it from `job_flow.json` via `final_verifier_status` and `final_verifier_ref` fields. Best-effort: failure must not crash the job flow.

Acceptance:
- File exists at `scripts/build_final_verifier_report.py`
- CLI callable with --evidence-dir
- Output is valid JSON with all required fields
- Verdict logic is deterministic and documented
- Integrated into do job-flow (best-effort, never crashes)
- `final_verifier_status` and `final_verifier_ref` in job_flow.json
- Works on incomplete evidence
- No absolute paths in output

## Task 5: Focused tests

Add focused tests for all new features.

Tests needed:
- Review scope packet generation from complete evidence
- Review scope packet with incomplete evidence (absent markers)
- No absolute paths in scope packet
- No raw prompts in scope packet
- Changed line ranges extracted correctly from unified diff
- Symbol detection finds Python def/class lines
- Risk tagging matches expected patterns (orchestration files, test files, etc.)
- Reviewer prompt uses scope packet when available (shorter than fallback)
- Reviewer prompt falls back when no scope packet
- Missing-tests gate: code change without tests → NEEDS_TESTS
- Missing-tests gate: test-only change → no gate triggered
- Missing-tests gate: code change with tests → passes gate
- Final verifier: all pass → PASS verdict
- Final verifier: unresolved findings → NEEDS_REPAIR verdict
- Final verifier: no tests → NEEDS_TESTS or PASS_WITH_RISKS
- Final verifier: target mutation → BLOCKED
- Final verifier: works on incomplete evidence

Acceptance:
- At least 15 focused tests
- All pass
- No flaky tests
- Tests cover all four features
