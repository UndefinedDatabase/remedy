# Live Review — Process-Hardening v1 (chore round)

Branch: chore/process-hardening-v1
LAST_REVIEWED_SHA: 89c4ef0 (branch base; round 1 under repair)
Finding IDs continue monotonically from R-0147. The F046 ledger is
archived in git history; this file is per-round working state.

## Findings

- R-0148 · Medium · round 1 (89c4ef0..ac97215)
  docs/README.md:171-172 — the integration_gate.md row of the Agent
  Conventions table is split across two physical lines ("…referenced by
  paste" / "blocks) |"), breaking the markdown table row. Root cause:
  transport hard-wrap in the relay of authored text phv1-r1-10; the
  worker correctly saved and applied verbatim and reported the suspected
  error (no worker fault). Fix: replace BOTH physical lines with the
  authored single row in .agent/authored/phv1-r2-2.md; the wrapped
  two-line form must no longer appear anywhere in docs/README.md.
  Resolved only by reviewer text.

- R-0149 · Medium · round 1 — routed to planning (spec conflict)
  The mandatory per-commit tables of docs/agents/handback_template.md
  collide with the AGENTS.md ≤60-line handoff cap on any round with
  more than ~5 commits (round 1 handoff: 106 lines, deviation
  documented). No in-round fix: AGENTS.md changes need operator
  approval; options are in the operator brief, ruling pending. Not a
  merge blocker.

## Verdicts

- Round 1 (89c4ef0..ac97215): FAIL — R-0148 (broken index table row)
  blocks the merge. All ten authored texts verified as applied from the
  committed .agent/authored/ files (reviewer re-ran the proof script:
  10/10 OK, exit 0); canary re-run by the reviewer: 42 passed; all
  anchors and the tier-3 replacement verified in the real diff. The
  handback followed the new template (first live test); the line-cap
  collision is recorded as R-0149. LAST_REVIEWED_SHA stays 89c4ef0.
