# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 13 books round 12's PASS verdict (RECORD12 - the self-use
GENERATION step, SU-008 appended) then performs closure precondition
6's RUN step: `run_next_self_use_item()` unflagged, real local
`ollama` provider, default small budget, against SU-008 (the R-0418
paragraph). Evidence (job id, provider, final status,
`describe_self_use_run_defects()` output) saved under
`.agent/selfuse_f114/`. No `consumed_by` edit yet - that is the
closure commit's own edit. No new R-id is minted this round; the
reviewer analyzes and narrates the defect-registration obligation
against the open ledger when booking THIS round's own verdict next
round (the same split F110 R16 / F112 R21 used).

## Next Steps

- Round 14: book round 13 (RECORD13, with the R-0784 evidence-addition
  narration), author T3_F114.md's Built State section (precondition
  4), run `remedy integrity check --json` (precondition 3).
- Then the closure commit: evidence job, fresh review zip, STATUS
  line, README sync, `consumed_by=F114`, the PR.
- Session note: round 13, session 3 - 4th delegated round, at the 4-5
  default; likely the session's last round before a scope check.

## Risks

- The run is a real, budget-capped LLM call against local `ollama`
  (`max_cost_usd=0.50`, `max_provider_calls=6`) - bounded, expected to
  end BLOCKED at the approval gate (the correct, safe outcome for a
  reviewer-practice finding no builder can fix in code), matching
  every prior run against R-0418 (SU-005/006/007).