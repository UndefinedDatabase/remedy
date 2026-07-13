# Plan — Steps 6621-6660 — F007 external acceptance closure

## Goal
Record the external acceptance of F007 in the execution-order truth, the feature document,
the top-level README and the operator state. Documentation and operator state only — the
accepted implementation and tests are frozen.

## Current Step
**Branch `feature/f007-supervisor-portability` (uncommitted, from main `dbd27e5`).
Closure documented; packaging the closure Evidence. NOT committed, pushed or merged.**

## External verdict — PASS_WITH_RISKS — ACCEPTED (2026-07-13)
- Accepted package `remedy-review-20260713-115439-READY_FOR_REVIEW.zip`
  (sha256 `4df642850249b8e1d2763400311aced43a712fd0523e79e4c6c169d5c0b263a9`),
  Evidence job `2e820a4dbf9842cf`, history jobs `eb2b76fd1aba4668`, `809b9b5743694abf`.
- 7/7 content proofs matched; bundle integrity, subject/Evidence alignment, fresh Evidence,
  change provenance, artifact contract and runtime integration all PASS.
- Portability 99 passed; CLI process boundary 15 passed; **both files in one pytest
  invocation: 114 passed in 525.44s**, all with normal final summaries.
- No `/tmp/pytest-*` runtime supervisor or application survived any complete run; a
  deliberately failing probe proved the registered cleanup still runs after an assertion
  failure.
- Disclosed environment limitation only: the review ZIP excludes `apps/ui/node_modules`, so
  the external host ran 2 apps/ui tests and skipped 5 with the explicit missing-Vite
  blocker. All 7 pass on the operator environment; production code is byte-identical.
- **Zero open findings. Zero remaining product or test blockers.**

## Closure performed
1. `docs/roadmap/STATUS.md` — F007 `[~]` → **`[x]`**, keeping PR #127 / merge `7733a1d` /
   follow-up `d0a08a1` and adding the accepted ZIP, Evidence job `2e820a4dbf9842cf`, the
   verdict and the acceptance date. F010 remains the first unchecked feature after F007.
2. `docs/roadmap/features/T0_F007.md` — status accepted/done; the binding Done criterion and
   every honest boundary preserved (single runtime, no watchdog, no F008, no F146, no
   multi-service Compose).
3. `README.md` — F001–F007 shown as the accepted foundation; the "not accepted yet" and
   "unaccepted" claims removed; the real remaining limitations (no watchdog, no multi-service
   runtimes, resolved-path project identity) kept.
4. `tests/docs/test_docs_consistency.py` — pins the new truth (F007 `[x]` with its Evidence
   job and verdict, F010 still `[ ]`, README no longer calling F007 pending).
5. Operator state (`.agent/context.md`, `.agent/plan.md`, `.agent/live_review.md`) records the
   acceptance. The live review now uses the format the review manifest really parses —
   `## Verdict (reviewer-owned)` with a bold `**PASS_WITH_RISKS**` token, plus a
   `## Builder Handoff` section (see the parser audit below).

## Frozen
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py`, `tests/cli/test_runtime_cmd.py`,
`tests/runtimes/runtime_cleanup.py`, `tests/runtimes/test_runtime_cli_process_boundary.py`,
`tests/runtimes/test_supervisor_portability.py` — sha256 verified unchanged before and after
this run. Every accepted protection stands untouched; the 114-test subprocess proof was not
rerun because none of its files changed.

## Boundaries
F010 is next and was **not started**. F008, F009 and F146 untouched. No provider calls.

## Live-review parser audit (why integrity passed while the ZIP said `absent`)

Two consumers read `.agent/live_review.md`, with different strictness:

- `packages/orchestration/integrity_gate.py::_check_live_review_verdict` is LENIENT: it
  takes the first non-empty line after ANY `## Verdict` heading. The closure file used
  `## Verdict` + the verdict on the next line, so `remedy integrity check` reported the
  verdict as present and passing.
- `scripts/build_review_manifest.py::_extract_review_state` is STRICT: it requires the
  reviewer-owned heading and a bold token —
  `##\s+Verdict\s+\(reviewer-owned\)\s*\n\s*\*?\*?([A-Z_]+)` — plus a
  `## Builder Handoff` section. Neither was present, so the packaged manifest honestly
  recorded `latest_live_review_verdict: "absent"` and `builder_handoff_present: false`.

Both parsers were behaving as written; the LIVE REVIEW was in the wrong format. The repair
is therefore the file, not the parsers — no parser was weakened, and `PASS_WITH_RISKS` was
not redefined as `PASS`. `review_ready` stays `false` because a human sign-off is still
required. `tests/orchestration/test_final_audit_evidence.py` now pins the manifest contract
so this cannot regress silently. Unifying the two parsers is a real (small) inconsistency,
but it is out of scope for a closure repair and no defect in either parser was found.

## Evidence package — closure-metadata repair
- Manual repair job `386faa53c8444451`, each scope attested with
  `--linked-prior-job-id 74c3ccfc36974aff` (the previous closure job, which itself links the
  accepted implementation job `2e820a4dbf9842cf`). 0 provider calls.
- Verification: `pytest -q tests/orchestration/test_final_audit_evidence.py
  tests/docs/test_docs_consistency.py tests/cli/test_command_catalog.py
  tests/cli/test_cli_ux.py` → **132 passed**.
- Review state before packaging: `latest_live_review_verdict = PASS_WITH_RISKS`,
  `open_findings = []`, `builder_handoff_present = true`, `review_ready = false`.
- Export: `.data/evidence_exports/386faa53c8444451` — fresh_evidence PASS,
  artifact_contract PASS, change_provenance PASS, runtime_integration PASS,
  final_verifier PASS_WITH_RISKS, final_job_review PASS,
  commit_execution NEEDS_HUMAN_APPROVAL, 12 content proofs.
- ZIP: `remedy-review-20260713-203151-READY_FOR_REVIEW.zip`
  (sha256 `56cb61e19496d26d6cc71106fd46a2c04db341c5133c5e4dedb2c19f5f9119ec`); its manifest
  reports `latest_live_review_verdict: "PASS_WITH_RISKS"`, not `absent`.

## Evidence package — previous closure (superseded metadata)
- Manual closure job `74c3ccfc36974aff`, each scope attested with
  `--linked-prior-job-id 2e820a4dbf9842cf` (the accepted F007 job), 0 provider calls,
  11 content proofs.
- Export: `.data/evidence_exports/74c3ccfc36974aff` — fresh_evidence PASS,
  artifact_contract PASS, change_provenance PASS, runtime_integration PASS,
  final_verifier PASS_WITH_RISKS, final_job_review PASS,
  commit_execution NEEDS_HUMAN_APPROVAL.
- ZIP: `remedy-review-20260713-123434-READY_FOR_REVIEW.zip`
  (sha256 `f8ecbecfa2bea090a03929353b67b1cb1effc1cb741b4392ce73d81771d9bf7a`).
- Verification: `pytest -q tests/docs/test_docs_consistency.py tests/cli/test_command_catalog.py
  tests/cli/test_cli_ux.py` → **95 passed**.

## Next
**Awaiting the human commit decision.** The branch stays uncommitted, unpushed and
unmerged.
