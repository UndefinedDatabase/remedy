# Handoff — amend0827 process diet · operator collection order · terminal state

## Session
SESSION 1 of order amend0827 · round 1 · rounds so far 1. Not a feature, so
no STATUS line is claimed and the 25-round / 7-session soft limit does not
bind; this section is written because rule 6 of this very order makes it
mandatory from 2026-08-27, and an order that exempts itself from its own
first handback is not a rule.

## Range
Review of `f4eae1d4`..HEAD, `f4eae1d4` being the merge commit of pull
request #215 which closed F031. HEAD is C7, the commit that writes this file.

## Commits
### 68f52760 C0 docs(agent): open the amend0827 process-diet order
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +33/-23 | scope, assumptions, four standing constraints carried forward |
| .agent/plan.md | +35/-33 | goal and item table for this order |

### 2c2ea885 C1 docs(agents): amend0827 rules 1, 2, 3 and 6 in AGENTS.md
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +32/-0 | new standing file, rule 2; two slips from the F031 closure |
| AGENTS.md | +66/-13 | handoff cap withdrawn, prose_slips registered, carrier rule, session number |

### dab1347d C2 docs(agents): sweep the withdrawn handback cap out of the two remaining docs
| Path | +/- | Reason |
|---|---|---|
| docs/agents/handback_template.md | +30/-20 | all three tiers withdrawn; write-once rule kept |
| docs/agents/split_workflow.md | +8/-4 | the 60/100 pair removed from the handoff description |

### 01518381 C3 docs(agents): amend0827 rules 1 through 6 in the planner/reviewer prompt
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +107/-5 | all six rules at their §1, §3 and §4 homes |

### 2fc22841 C4 docs(agents): amend0827 rules 1, 4, 5 and 6 in the self-drive protocol
| Path | +/- | Reason |
|---|---|---|
| docs/agents/self_drive_protocol.md | +58/-4 | round loop, G7 and session end |

### 2e9d37a1 C5 docs(agent): work off the four F031 closure candidates and book rule 3's findings
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +72/-0 | DECISION amend0827 D1 and D2 appended |
| .agent/live_review.md | +10/-0 | four Done: bookings and the disposition note appended |
| .agent/candidates.md | +11/-70 | EMPTIED; block condition lifted |
| docs/roadmap/STATUS_closure_protocol.md | +35/-2 | D1's package path, D2's carrier commit, rule 1's closure exception |

### a3764d13 C6 docs(agents): carry the session number where rule 6 says every handback carries it
| Path | +/- | Reason |
|---|---|---|
| docs/agents/handback_template.md | +14/-0 | mandatory `## Session` section |
| docs/agents/planner_reviewer_prompt.md | +6/-1 | operator brief Feature row |

### C7 docs(agent): close the amend0827 order in the state files — self, per R-0149
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | self | item table to done |
| .agent/handoff.md | self | this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| Part 0(a) merge PR #215 | done | conflict resolved, CI green, merged as `f4eae1d4` |
| Part 0(b) four candidates worked off | done | no id spent; file EMPTY |
| Part 1 round measurement | done | reported to the operator; no disk artifact ordered |
| Rule 1 verdict booking | done | AGENTS.md, §4 item 6, self-drive Phase 2, closure exception |
| Rule 2 two-class findings | done | AGENTS.md section, prose_slips.md, §4 item 4 |
| Rule 3 cap reform | done | four files swept; four findings booked |
| Rule 4 checklist freeze | done | §3 header, self-drive session end; list measured at 37 |
| Rule 5 gate budget | done | §3 gate-budget bullet, self-drive Phase 2 |
| Rule 6 session budget | done | §3, §1, G7, session end, template, operator brief |
| push and PR | pending | this file is committed first |

## External actions
- `gh pr list` before the branch: exactly PR #215, `feature/*` → `main`, not a
  draft, `mergeable: CONFLICTING`, `statusCheckRollup` EMPTY. Reported to the
  operator, who ruled option 1.
- Conflict resolved on `feature/f031-decision-inbox` as merge commit `40ed12ba`;
  pushed; the first CI run PR #215 ever had, `33076078540`, completed `success`.
- `gh pr merge 215 --merge --delete-branch` exit 0 → `f4eae1d4` on `main`;
  `gh pr list --state open` then `[]`.
- No worktree was left behind, no force-push, no history rewrite.

## Verification
- Conflict resolution, `.agent/decisions.md`: base is a byte PREFIX of the
  result; the main delta (4972 B) and the branch delta (64490 B) each occur
  verbatim and contiguously; result == base + main delta + branch delta at
  622400 B; both seams `.\n` → `\n#`; keys 126/129/153 → 156 = 126 + 3 + 27,
  zero duplicates, zero lost.
- Local gates before the push of `40ed12ba`: canary + three state readers
  `131 passed`; `tests/ui_server/` `489 passed`; docs + roadmap index
  `325 passed`.
- C1: `tests/docs/` + roadmap index + canary `367 passed`.
- C2, C3, C6: `tests/docs/` + `tests/test_agent_tooling.py` + canary
  `347 passed, 1 skipped` at each.
- C4: same suite `347 passed, 1 skipped`; the six substrings
  `tests/test_agent_tooling.py` pins in the self-drive protocol all survive
  (Open PR Gate 2x, Never force-push 1x, .agent/STOP 3x, worker subagent 1x,
  git worktree 1x, handoff 12x).
- C5: `tests/docs/` + roadmap index + the four state readers + canary
  `456 passed`.
- Ledger movement at C5, measured against `HEAD~`: `^- R-\d+ — ` 270 unchanged,
  `^Done: R-\d+ — ` 17 → 21 adding exactly R-0430, R-0582, R-0676, R-0700,
  `^Landed: R-` 0, `^Gate: R\d+ — ` 19 unchanged, `^Gate: F\d+ R\d+ — ` 53
  unchanged, open set 253 → 249, no duplicate resolved id, and both appended
  files keep their pre-commit content as a byte prefix.
- §3 pre-emission checklist re-counted after every edit: 37 items, numbered
  1..37 with no gap — the number rule 4 freezes.
- §4 item numbering re-counted after the rule 1 insertion: 1..13, strictly
  increasing, no duplicate. Rule 1 was rewritten as a continuation of item 6
  precisely so `§4 item 7` keeps meaning what STATUS_closure_protocol.md and
  §1 of the same file say it means.

## Deviations & assumptions
- SINGLE-SESSION MICRO-ROUND, and the change set includes `AGENTS.md`, which
  that round type does not name among its allowed paths (docs/, tests/,
  .agent/**, roadmap files). The operator prompt authorizes the AGENTS.md
  amendments by name. No file under `packages/` or `apps/` is touched and no
  test is added, changed or deleted, so the production-code bar the type
  protects is not approached.
- RULE 3 REACHED FOUR FILES, NOT THE TWO THE ORDER NAMED. The withdrawn cap
  lived in AGENTS.md, `docs/agents/handback_template.md`,
  `docs/agents/split_workflow.md` and `docs/agents/planner_reviewer_prompt.md`.
  Leaving any of them would have left the rule alive where a worker actually
  reads it, so the sweep is wider than the order's file list and narrower than
  its intent by nothing.
- FINDING R-0700 IS PARTLY WRONG AND THE CORRECTION IS RECORDED RATHER THAN
  QUIETLY DROPPED. It calls the >10-commit 160-line tier "a tier AGENTS.md does
  not define"; the tier was defined in `docs/agents/handback_template.md`, a
  file AGENTS.md itself makes mandatory. The finding resolves either way under
  rule 3, but its Medium severity rested on a worker inventing a tier, and the
  worker was applying one. Recorded in the Done: text and beside the withdrawn
  tier in the template.
- The four rule-3 findings are booked RESOLVED BY AMENDMENT, not by repair, and
  each Done: text says so in those words. Nothing was fixed; a rule was
  withdrawn.
- PART 1 PRODUCED NO DISK ARTIFACT. The round classification was ordered as a
  report to the operator and delivered as one; it is not written into `.agent/`
  because no rule asks for it and an unbidden state file is the kind of
  bookkeeping this order exists to cut.

## Next
Push, open the pull request into `main`, watch the hosted run, and merge at the
Open PR Gate. `.agent/candidates.md` is EMPTY, so the next session may claim the
next feature per Rule A5 with no block condition standing.
