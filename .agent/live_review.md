# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. The F075 candidate
sweep (4 entries) was registered/resolved in R1 per
docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate findings").

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#180) + STATUS claim + candidate
  sweep + R-0199 measured diagnosis + reuse inspection + T001 —
  PASS, see Verdicts.
- R2 (SPLIT, LARGE, current): R-0199 fix (metadata-manifest digest)
  + T002 (triggers + loop consumption + reference verification)
  + T003 (boundary recall eval + threshold). Awaiting handback.
- R3 (planned): integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md — its own
  round, never bundled.

## Findings
- R-0199 (harness perf, Medium — carried from F075, ID spent there):
  diagnosis MEASURED in the F079 R1 handback, mechanism confirmed —
  two production call sites (gauntlet_runner.py:461 before, :533
  after, always), root resolves to the operator's real .data
  (143.66 GB / 2,495,115 files at measurement), one content-hash call
  = 394.8 s, 20 calls per 10-order campaign ≈ 2.9 TB read / ~2.2 h
  pure hashing; job_workspaces holds 99.80 % of the bytes; the
  attempt-03 ~872 GB observation is consistent with the mechanism at
  that date's root size. FIX ORDERED in R2: data_root_digest becomes
  a metadata-manifest digest (relpath, size, mtime_ns — no content
  reads), per-run call frequency and evidence field names retained.
  DECISION (alternatives considered: campaign-level frequency —
  rejected, loses per-run attribution; scoping the root past
  job_workspaces — rejected, that subtree is exactly where a
  violation would land; keeping content hashing — rejected, 6x the
  wall clock for a threat model of accidental writes). Reversal: any
  later relay may reinstate content hashing.
- R-0200 (process/gate-tooling, Medium): F070 verb-called gate half.
  Deferred, OPEN — unchanged from R1; rolls to candidates at closure
  if unbuilt.
- R-0201 (roadmap routing): resolved by routing in R1 — scope note
  landed in docs/roadmap/features/T3_F106.md. Resolved.
- R-0202 (gate tooling, Low): mid-run UI rebuild env-var class.
  Deferred, OPEN — unchanged from R1; rolls to candidates at closure
  if unbuilt.
- R-0203 (design, Low) 2026-08-06, reviewer-registered at the R1
  review: handoff.py's `root` parameter reaches mission/dossier/output
  paths, but the job-side sources (checkpoints, storage, run events)
  resolve the env-rooted data root — consistent only when both point
  at the same place (the tests pin this via REMEDY_DATA_DIR). Matches
  the existing env-rooted API shape; not a defect today. Disposition:
  constraint carried into the T002 order (consumption resolves ALL
  sources through one root discipline and documents it); closes with
  T002.
- Next free ID: R-0204.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-06). Range 38854f60..79621fc0
  (6 commits, all tabled). Transport: f079-r1-1..6 cmp 0 against the
  reviewer's scratchpad originals (primary proof); every applied
  state file byte-equals its authored text; the STATUS claim and the
  T3_F106 append verified in place. Reviewer re-ran the gates
  personally: tests/docs 293 passed, canary 42 passed, test_handoff
  23 passed — all exit 0; porcelain empty; `git worktree list` =
  primary only. handoff.py and test_handoff.py read in full:
  composition only — dossier renderer, checkpoint loader, decision
  queue, event/job loaders and both redactors reused, every reuse
  claim spot-checked at its file:line; pure artifact pinned by the
  snapshot test; idempotence pinned incl. the derived-decision
  wall-clock fix the worker found and killed in-slice; gaps named,
  zero-progress valid, redaction pinned to run_manifest's denylist.
  R-0199 diagnosis accepted: both call sites and the root-resolution
  path verified in source by the reviewer; the size/time numbers
  accepted from the worker's raw transcript — a reviewer re-scan was
  deliberately skipped (the scan is itself the R-0199 cost) and the
  operator declined it at relay, consistent with that discipline.
  The COMMIT-1 split deviation is accepted (contents and order
  unchanged, < 500-line rule honoured — same class as the R-0198
  ruling). Verification tier: round gate + canary + docs gate.
  LAST_REVIEWED_SHA = 79621fc0.
