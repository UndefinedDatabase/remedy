# Context — paydown-0801 micro-round (post-F061, pre-F062)

## Active Branch
`feature/paydown-0801`
Base commit: main after PR #172 merge (F061, Open PR Gate 2026-08-01)

## Steps (round map)
R1 (single-session micro-round): closure-candidate disk vehicle
(.agent/candidates.md) + settle the two dropped F056 candidates as
DECISIONs. Then merge on PASS; next feature per Rule A5 is F062.

## Scope
docs/roadmap/STATUS_closure_protocol.md,
docs/agents/planner_reviewer_prompt.md,
docs/agents/handback_template.md, and `.agent/` state (authored
texts, candidates.md, decisions.md, plan/handoff/last_block).
Nothing beyond; no production code.

## Gates (round verification, pytest)
python3 -m pytest tests/docs/ -q            docs-round gate
python3 -m pytest tests/cli/test_golden_path.py -q  canary
Resource safety: everything runs through these pytest wrappers; no
unbounded subprocess fan-out from gate tooling.

## Constraints
- Round type: SINGLE-SESSION MICRO-ROUND (planner_reviewer_prompt.md
  §3) — change set limited to docs/, tests/, .agent/**, roadmap
  files; full fidelity ritual applies (scratchpad originals, sha256,
  cmp disk-to-disk).
- Authored texts under .agent/authored/ are applied by copy and
  sha256-verified before use; never hand-edited.
- Commits stay under 500-line diffs (AGENTS.md).
- context.md satisfies its FULL test reader list: a "Steps" section,
  "## Active Branch" with a feature/ slug, a roadmap F-id, and this
  pytest/resource line (R-0162; reader rule in
  planner_reviewer_prompt.md §4 item 11).

## Do not touch
Production code (packages/, apps/). docs/roadmap/ROADMAP.md and
docs/roadmap/STATUS.md this round. Feature files. Evidence tooling.
