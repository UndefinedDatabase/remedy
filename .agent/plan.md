# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R66 is a record round and touches no file outside `.agent/`. It writes the R65
verdict — the integration gate PASSED, with an EMPTY branch-only set and an
EMPTY base-only set, both full-suite runs re-run by the reviewer itself — and it
corrects one factual error the R65 handback carried. It is the LAST round of its
session: its handback is the session terminator. No finding is resolved and none
is registered, no production code and no decision this round.

## Next Steps
1. Closure per `docs/roadmap/STATUS_closure_protocol.md`, whose first step is
   the evidence bundle and the review zip.

## Risks
- A SESSION LINE IS NOT DERIVABLE BY THE WORKER THAT WRITES IT. A worker runs
  ONE round and cannot see a session boundary, so a block ordering that line
  must SUPPLY the round list; R65's block did not, its worker reconstructed the
  window from branch history, declared the assumption, and got it wrong by two
  rounds. The repair is in the block, not in the worker.
- THE PARITY CLAIM OF THE R65 GATE IS VOID AND STAYS VOID. A rebuild ran inside
  the base run window and the evidence says so; it costs nothing only because
  the base-only set is empty, so no id was owed an attribution.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `033484f6`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
