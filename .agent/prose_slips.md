# Prose slips — reviewer inaccuracies without product effect

> Standing file, created by operator collection order amend0827
> (2026-08-27), rule 2. One line per slip: date, round, one sentence.
> No R-id, no severity, no recurrence bookkeeping, no correction round.
>
> WHAT BELONGS HERE: a reviewer-prose inaccuracy that left nothing wrong on
> disk under `packages/`, `apps/`, `tests/` or `docs/` — a miscounted line,
> a stale byte or digit, a block over its cap, a wording contradiction the
> worker declared and applied anyway.
>
> WHAT DOES NOT: a defect with product effect, and a load-bearing factual
> claim that landed false in the append-only record. Both keep their old
> route — an R-id in `.agent/live_review.md`, and for the record a single
> correction, at most one per defect.
>
> This file is APPENDED, never rewritten, and it is never a block condition:
> nothing here gates a claim, a closure or a round. It is read at
> consolidation (rule 4) and otherwise left alone.

## Slips

- 2026-08-27 · F031 R72 · A clause quoted from an OPEN finding's own body
  was reproduced into `.agent/decisions.md` and `.agent/plan.md` at closure
  after a later `Gate:` entry had already measured it false and narrowed
  it; a correction lands in the gate entry and never in the finding it
  corrects, so a body quote is re-measured against every later gate entry
  naming that finding.
- 2026-08-27 · F031 R72 · The package-absence closure candidate asserted a
  reach — "cannot be reopened from this machine" — that no command in that
  session established, the sandbox having refused every read outside the
  repository; the class already carries `R-0709`.

- 2026-08-27 · F032 R2 · An item-status row in the authored `.agent/plan.md`
  replacement wrapped across two source lines, so the markdown table rendered
  one ordered item as two rows; the worker applied it byte for byte and
  declared it, and the next round's plan rewrite clears it.

- 2026-08-28 · F032 R10 · The block's Done-when preamble put every gate at a
  commit strictly earlier than C6 while G1 asked for the `git status
  --porcelain` count after C6, so one clause of one gate was unmeetable by
  construction; the worker declared it and reported the reading outside the
  file, and the reviewer measured it at `91b00286` as 0.

- 2026-08-28 · F032 R15 · The block did not carry forward the clause the F032
  R12 gate entry had labelled binding on the next block ordering a handback —
  that a false numeral in `.agent/handoff.md` is repaired by a deviation line
  in the NEXT handback rather than by a commit of its own — so the worker,
  finding an unmeasured sentence in its own committed handback, spent a ninth
  commit repairing it and declared the write-once breach itself. Nothing on
  disk under `packages/`, `apps/`, `tests/` or `docs/` was wrong, so no id was
  spent; the clause is quoted in the R16 block instead.
