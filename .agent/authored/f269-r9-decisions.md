
## DECISION F269 D10 (2026-09-18, reviewer, round 9) — a follow-up mission carries its remainder as one amendment, amending D9 (3)
CONTEXT: finding R-0971: DECISION F269 D9 (3) kept each carried blocker's origin, and planning the
follow-up, which the answer door names as the next step, replaces every `planner` criterion
(DECISION F269 D4 (2)), so the carried remainder is lost. DECISION F269 D8 gives the contract
exactly one origin for a criterion the operator added after the plan: `amendment`, which
`write_planner_criteria` keeps with its id, and an amendment entry that records what was
understood and from which round it applies.
CHOSEN: the follow-up mission's contract carries the blockers as origin `amendment`, renumbered
from `C001` with their text, blocking and check as D9 (3) orders, and ONE amendment entry `A001`:
its text the prefilled order, `received_at` the answer's time, `applies_from` 1, `criteria` every
carried id, `understood` "carries the criteria mission <id> left unmet: <old ids> as <new ids>",
`acknowledged_in` null — so the follow-up's first loop round acknowledges it in its ledger as any
amendment. Everything else in D9 stands.
ALTERNATIVES: keeping carried `planner` criteria in `write_planner_criteria`, rejected because a
re-plan must be able to replace the planner's own criteria; a fourth origin, rejected because the
operator's "yes" is exactly an amendment. REVERSE: restore D9 (3)'s origin rule, which re-opens
R-0971, and delete this paragraph.
