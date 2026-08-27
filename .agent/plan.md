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
CLOSURE 2 of 3. This round records the CLOSURE 1 verdict, then builds the two
artifacts closure cannot be authored without: a fresh feature-scoped evidence
bundle and a FRESH review zip built from a clean tree at the reviewed head. It
builds no product code. T001, T002 and T003 are complete, the integration gate
PASSED, and the Built State section landed last round, so closure preconditions
1 through 5 are all either met or re-confirmed by this round's own gates.

## Next Steps
1. CLOSURE 3 of 3 — the reviewer authors the STATUS line from the evidence job
   id, the package filename and the package SHA-256 this round produces; the
   worker commits it LAST with the README capability sync in the SAME commit,
   writes any candidates to `.agent/candidates.md`, and creates the PR. The PR
   is NOT merged in this session: the gap is the operator's review window.

## Risks
- A FAILING ZIP BUILD IS A CLOSURE BLOCKER, never a thing to work around. The
  feature does not close without the package, and a package built from a dirty
  tree is invalid.
- THE STATUS LINE CANNOT BE AUTHORED BEFORE THE PACKAGE EXISTS. Its evidence
  job id, filename and SHA-256 do not exist until this round produces them, so
  splitting closure across two rounds is forced by the record, not chosen.
- R-0693 IS RESOLVED and was the only open High this feature raised. R-0495 and
  R-0574 are inherited standing Highs from the already-closed F085 and F086,
  documented risks rather than F031 defects, and they rode through six prior
  closures on the same footing.
- R-0648 IS OPEN AND THIS ROUND'S G8 SHOWS IT: the `high_blockers_open` check
  cannot parse this ledger, so its PASS is a tool reading and not evidence
  about findings. The High question is answered by the record above, not by it.
- R-0403 IS OPEN AND THIS PACKAGE WILL SHOW IT: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F031 defect.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 and this round
  moves it by nothing.
