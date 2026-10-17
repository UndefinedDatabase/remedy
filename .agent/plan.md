# Plan — scale correctness (operator order 2026-10-17, audit remedy_scale_audit_2026-10-17.md)

## Goal
Minimal correct work for small orders, reliable work for medium ones, controlled decomposition for
risky or multi-repo ones. A focused change of the lane decision, plan normalization and the
verification/cost policy; no new orchestrator. Branch feature/scale-correctness-routing.
`.agent/STOP` kept; no unattended loop, no real model call, no merge, no install.

## Current Step
Phase 1/2 code is in: exact path resolution (root vs docs README), test files as a requested
deliverable, layout-independent order parts, artifact-filter bypass closed, check-only second job
deleted, risk and hold routing, study staleness. Open: aggregate order budget (Phase 3), the call-count
baseline and the scale matrix with disposable repositories (Phase 0/4), docs, closing gates.

## Next Steps
- Aggregate order budget across the jobs of a walk + planning calls counted; tests incl. resume.
- Fake-provider call-count harness; baseline vs new table; scale matrix (fixtures versioned).
- docs/ (do guide), decisions.md, handoff, PR (no merge).
- One full local gate run at the end; propose the real Pi/Ollama calibration (needs approval).

## Risks
- Existing tests that assumed the check-only second job were rewritten to name two deliverables.
- Risk words are a small fixed vocabulary (EN/DE); a documentation target is exempt by design.
