# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Close F079 per docs/roadmap/STATUS_closure_protocol.md. Substance is
done and gated: T001 composer, T002 triggers + consumption + reference
verification, T003 measured boundary recall (100 % open items),
R-0199 fixed, integration gate PASS (full suite green, both sides,
all 48 differing ids attributed).

## Current Step
R4 — closure part 1: Built State section into T1_F079.md (content
commit, before the zip), closure preconditions (integrity check,
clean tree), evidence job via create_manual_completion_bundle
(review_feature_id=f079), fresh review zip from the clean content
HEAD. Handback carries job id, package filename, SHA-256 and the
content HEAD — the reviewer authors the STATUS line from them.

## Next Steps
- R5 — closure part 2: apply the authored STATUS [x] line + README
  ledger sync (same commit), re-emit R-0200/R-0202 + the R3 flake
  observation to .agent/candidates.md, final .agent state, closure
  commit (STATUS.md + README.md + .agent/** only), push, PR. The PR
  merges at the next feature's Open PR Gate.

## Risks
- Packaging pitfalls are known and named in the protocol: sha256
  output_hash, full-length base_commit, real node ids with
  len == selected, test_files are files, run_id matches ^vr-\d{4,}$.
- The evidence dir stays OUTSIDE the repo (session scratch, never
  committed) — a committed dir turns the package BLOCKED_EVIDENCE.
- A failing zip build is a closure BLOCKER: stop, hand back raw.
