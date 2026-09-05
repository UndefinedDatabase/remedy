# Plan — amend0905-vocab-rebuild (operator planning amendment)

Branch: feature/amend0905-vocab-rebuild, cut from `main` after PR #237
(amend0905-throughput) merged; STATUS.md had 0 `[~]` lines and
`remedy plan next` proposed F259 at the cut.

## Goal

Write down the operator's 2026-09-05 vocabulary rulings (DECISION
amend0905-vocab D1–D12 in `.agent/decisions.md`) and make the vocabulary
rebuild the very next work: rewrite T2_F259.md / T2_F260.md / T2_F261.md
completely, register F268–F271 with ledger atomicity (STATUS lines,
TOTAL_FEATURES 267 → 271, README counter), reorder STATUS.md per D12,
sweep every feature file for the retired vocabulary (open files edited by
the replacement table, `[x]` files get a dated vocabulary note only), add
the "Replacing is deleting" rule to AGENTS.md. PLANNING ONLY: no product
code, no command or module rename, no module deletion.

## Current Step

Commit sequence of the single amendment round: (1) decisions D1–D12 ·
(2) this plan · (3) F259 rewrite · (4) F260 rewrite · (5) F261 rewrite ·
(6) registrations F268–F271 + pin + README in one commit · (7) STATUS
layout (D12 order, F260/F263 titles) · (8) feature-file sweep, ~15 files
per commit · (9) README / docs index / closure protocol / docs/agents
sweep · (10) AGENTS.md rule · (11) ruling conflicts as findings in
live_review.md · (12) handoff rewrite. Then push, PR, hosted run GREEN,
checks read, merge (two separate commands), verify on main.

## Next Steps

- Operator starts remedy-loop-feature; Rule A5 proposes F259.
- F259 → F260 → F261 → F266 → F268 → F269 → F270 → F271 → F263 → F264 →
  F265 in that order (D12).

## Risks

- The ruling table applies `promote → apply` by SENSE (job-result verb
  only); the kept senses are listed in the live_review finding so a later
  reader does not re-sweep them.
- README counter is measured on disk (72 accepted), not the operator's
  recalled 71 — recorded as a conflict finding.
- Two modules of the F260 deletion list do not exist under those names
  (`provider_trust_gate.py`, `local_advisor.py`); F260's file names the
  on-disk modules and the finding records the mismatch.
