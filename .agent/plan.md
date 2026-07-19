# Plan — Steps 13161-13360 — F012 hardening round 28 (COHERENCE + INVOCATION-BINDING CLOSURE)

## Round 28 binding decision

Reviewed `remedy-review-20260719-124709-READY_FOR_REVIEW.zip`
(SHA `7a452c42...d898d1`, Evidence job `a3d937ec1835eb93`, linked prior `ebe675ec74f20c1a`,
Base `7fa4466`, HEAD `8c32724`). Verdict FINDINGS; F012 `[~]`. Final F012 hardening round.

Four reproduced contract defects, each repaired in its own non-overlapping scope:

1. **Token-status projection coherence** — one shared projection mapping requires every overlapping
   field of token_measurement / its actual_summary / top-level token_actual_summary to EQUAL the
   authoritative token_status; a disagreement blocks; the low/null summary carries no projection.
   Scope: `_token_projection_problems` + its call in the FV branch of `_gate_semantic_problems`.
2. **Producer-derived VerificationTests** — exact `job_evidence._run_verifications` contract: repeated
   commands legitimate (unique run ids stay mandatory), top-level command == `" && ".join(run
   commands)`, exit_code == 0 iff every run exited 0, timestamp a real tz-aware ISO-8601 datetime.
   Scope: `validate_verification_tests` + `_valid_utc_datetime`.
3. **Invocation-bound packaging-output identity** — only the EXACT set of outputs the current
   packaging invocation generates (passed from make_review_zip.sh through both builders) classifies;
   the invocation-independent grammar is removed. Scope: `_classify_review_subject` + the CLI plumbing.
4. **Malformed nested Evidence validates, never crashes** — validate the minimal closed shape before
   reading nested fields; a wrong inner type appends a validation error, never an AttributeError.
   Scope: `_job_flow_shape_problems` + the job_flow block of `validate_evidence_candidate`.

Plus one isolated maintenance item (separate commit): the stream-export ZIP fixture is repaired for
the current pipeline (copies every helper, models an internally consistent git-backed job).

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network; no Fable; no
subagents; no Docker; no new dependency. Manual operator work only. Small local commits, never amend/
squash Round 27. Do not push, PR, merge, or begin F017. Fresh Evidence linked `a3d937ec1835eb93`; one
READY_FOR_REVIEW ZIP; then stop. Preserve every accepted F012 behavior. This is the final F012
hardening round — after it, generic hardening is follow-up maintenance (see the F012 closure section
of `docs/roadmap/features/T0_F012.md`).
