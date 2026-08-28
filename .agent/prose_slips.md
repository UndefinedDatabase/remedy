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

- 2026-08-28 · F032 R17 · The block's BASE paragraph wrote the base commit as
  `c1e208334cd8c7c0cef0a0ae3e5a1e63a4dc65d5` after measuring only the leading
  eight characters, so thirty-two of the forty were invented and the string
  names no git object; the real tip was
  `c1e20833405fc3a5a8f3b50729046578dbc97329`. The worker resolved the intent
  from the short form the gates quote, ran against the real tip and declared
  the discrepancy. Nothing on disk under `packages/`, `apps/`, `tests/` or
  `docs/` was wrong, so no id was spent. Measure a SHA in full or write only
  the short form that was measured.

- 2026-08-28 · F032 R18 · The LEDGER18 slice was headed `Gate: F032 R16 and R17
  — `, a shape the record's own `^Gate: F\d+ R\d+ — ` pattern cannot match, so
  the entry for those two rounds adds no gate key and the count stood still at
  69 across the commit that wrote it. The reviewer's own pre-emission checklist
  requires a slice joining a repeating record format to be compared
  MECHANICALLY against the headers it joins, and that comparison was not run;
  the block's own gate reported the standing count and the worker declared it.
  The landed entry is not rewritten — the R19 entry carries the dated
  correction that indexes it. One round, one key: where an entry covers two,
  give it the later round's key and name the earlier one in the body.

- 2026-08-28 · F037 R1 · The block's G5 ordered the ledger reconstruction as
  the LTO slice "plus two newlines plus everything from `## Findings`", while
  constraint 2 of the same block defines a slice's text as its content lines
  joined plus ONE trailing newline — so the two clauses describe byte strings
  one newline apart and cannot both hold, and only the content-joined reading
  matches the file. The worker measured both readings, applied the plain
  FROM/TO replacement plus one newline plus the appended slice, and declared
  the contradiction rather than correcting a slice. Nothing landed wrong on
  disk. Where a gate restates an operation the constraints already define,
  NAME the constraint instead of paraphrasing its bytes.

- 2026-08-28 · F037 R2 · The block's G5 ordered every append baseline read with
  `git show 89b96df7:<path>`, naming R1's C1 instead of the round base — a
  commit at which `.agent/live_review.md` predates R1's own header reset and
  F032 R19 gate append by 4148 bytes and one gate key. Obeying it literally
  would have deleted landed text from an append-only record, which the same
  block's constraint 5 forbids, so the block contradicted itself and the worker
  had to resolve it. Nothing landed wrong: the worker measured all three
  baselines against the base first, used the correct pre-commit tip and
  declared the deviation. A baseline SHA is COPIED FROM THE COMMIT THE APPEND
  BUILDS ON, never carried over from the previous round's block, and where the
  worker makes that commit itself the gate names it by ROLE — "the commit you
  are about to build on" — rather than by a SHA the reviewer guessed.
