# Plan — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger · claimed `[~]` in
docs/roadmap/STATUS.md. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R6 PASSed; LAST_REVIEWED_SHA 7f32dae9. Open findings 0; next free
ID R-0222. R-0221 is carried in `.agent/candidates.md`. No PR exists.

## Goal
Close F103 per docs/roadmap/STATUS_closure_protocol.md. The substance
is built and gated: T001 schema plus the never-fail writer, T002 the
call site with backfill and a content-comparing reconcile, T003 the
cost aggregation with `remedy stats cost`, `backfill-ledger` and
`verify-ledger`, the R5 integration gate, and R6's live mirror at the
task-run evidence seam so a real job yields rows. Closure records what
was built on the feature file and packages the accepted head.

## Current Step
R7 — closure part 1: the Built State section on
docs/roadmap/features/T2_F103.md (a CONTENT commit, before the zip),
the closure preconditions, the LOAD-BEARING full-suite confirmation
run, the evidence job through `create_manual_completion_bundle` with
`review_feature_id="f103"` into a gitignored dir outside the review
subject, and a FRESH review zip from that clean content head. The
handback carries the job id, the package filename, its SHA-256 and the
content HEAD; the reviewer authors the STATUS line from those values
and never from a guess.

## Next Steps
- R8 — closure part 2: apply the authored STATUS `[~]`->`[x]` line and
  the README ledger sync in the SAME commit (R-0154), keep R-0221 in
  `.agent/candidates.md` as the next feature's block condition, write
  the final `.agent` state, commit LAST on the branch (Rule A4), push,
  `gh pr create`. That PR merges at the next feature's Open PR Gate,
  which is the operator's manual-review window.

## Risks
- The full-suite confirmation is LOAD-BEARING, not a formality: R6
  landed production code AFTER the R5 gate, so it is the only
  full-suite evidence over the live-mirror wiring. A regression there
  is a normal repair round, never a closure workaround.
- Packaging pitfalls named in the protocol must be met at authoring
  time: sha256-hex output_hash, FULL-length base_commit, real node ids
  with `len(node_ids) == selected`, `test_files` are files and never
  directories, `run_id` matching `^vr-\d{4,}$`, and NEVER a full-suite
  node-id list.
- The evidence dir stays OUTSIDE the review subject and is never
  committed — a committed one packages BLOCKED_EVIDENCE.
- A failing zip build is a closure BLOCKER: stop, hand back the raw
  error, do not work around it.
