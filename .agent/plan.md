# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D27.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
CLOSURE 3 OF 3. The RECORD ROUND passed every gate its block ordered and this
round writes that verdict. It registers ONE new finding, `R-0709`, for a defect
the open set does not hold: a block ordered its handback to put a ruling request
to the operator, which `docs/agents/planner_reviewer_prompt.md` §2 forbids, and
the session ended with nothing closed. It records DECISION F031 D27, which rules
closure precondition 2 met on the evidence and carries `R-0708` as a documented
open Medium risk. Then it flips the STATUS line to `[x]` with the README sync in
the SAME commit and opens the pull request, which is NOT merged this session.

## Next Steps
1. MERGE THE CLOSURE PULL REQUEST at the next feature's start, through the
   AGENTS.md Open PR Gate. It is not merged in the session that creates it; the
   gap is the operator's manual-review window.

## Risks
- `R-0708` IS CARRIED OPEN AND IS NOT AN F031 DEFECT. Closure precondition 2
  measured four GREEN and one RED in five runs at the reviewed head. The red is
  a fixed five-second server-start budget in `tests/ui_server/test_live_state.py`
  losing a CPU race under `-n auto`; the same test passes SOLO at exit 0 in
  0.32s. DECISION F031 D27 rules the precondition met and routes the repair to a
  follow-up, because `tests/ui_server/` is outside F031's change set.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects.
- THE CLOSURE PACKAGE IS NOT ON DISK. It was built and verified at CLOSURE 2 and
  its five values are carried unchanged; `.gitignore` excludes the archive and
  the durable pointer is the STATUS line. This is registered as a closure
  candidate rather than a finding.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 after this
  round, which mints `R-0709` and resolves nothing.
