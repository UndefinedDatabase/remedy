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

- 2026-08-28 · F037 R4 · The block's G7 ordered a mutation that was VACUOUS BY
  CONSTRUCTION: it had `insert` opcodes mark the OLD side, and
  `difflib.SequenceMatcher.get_opcodes()` emits every `insert` with `i1 == i2`,
  so the resulting span is always zero-length and the module's own
  normalisation drops it. No corpus could have turned that mutation red. The
  worker ran it, reported the green plainly, diagnosed the cause and declined
  to substitute another mutation, which is the ordered behaviour. Nothing
  landed wrong on disk. A mutation is checked against the SHAPE OF THE DATA THE
  MUTATED BRANCH RECEIVES before it is ordered, not only against the branch
  being reachable — `docs/agents/planner_reviewer_prompt.md` §3 item 5 asks for
  the probe form where that is not obvious, and this is the case it was written
  for.

- 2026-08-28 · F037 R5 · G8 ordered `^Landed: R-` to read 2 after C4 while the
  same block's constraint 6 forbade deleting the third such line, which belongs
  to `R-0711`, so 3 was the only reachable value and the gate contradicted the
  block's own constraint; a count over a SHARED record file is derived from the
  base reading plus the lines the round's own constraints add, and pre-existing
  entries are counted rather than assumed away.

- 2026-08-28 · F037 R5 · SPEC S2 named the `add`-side `[]` as the assertion that
  fails when `delete` is dropped from the old-side opcode tuple, and the
  assertion that actually fails is the `del`-side span equality; a stated
  discriminator is RUN against the mutation it names before it is written down,
  because a fixture can be right while the sentence explaining it is wrong.

- 2026-08-28 · F037 R5 · SPEC S6 defined significant tokens as "the tokens that
  are not pure whitespace" and then glossed the both-empty case as lines made of
  "whitespace and punctuation", which that definition excludes; where a spec
  states a definition and a gloss beside it, the two are read against each other
  before emission and the gloss is deleted rather than left to be chosen between.

- 2026-08-28 · F037 R5 · SPEC S8 ordered a report that a `the fox jumps`
  replacement test still passes, and no such test existed in the corpus; a gate
  naming a test by its CONTENT is resolved against the file at the base commit,
  the same obligation `docs/agents/planner_reviewer_prompt.md` §3 item 24 places
  on a path a gate names.

- 2026-08-28 · F037 R7 · G5 worded append reader (a) as a length sum plus a
  byte-PREFIX check, and those two properties together cannot reject a byte
  flipped INSIDE the appended region — which is exactly the rejection the same
  gate's negative control ordered them to produce, so the control could have
  passed a corrupted append. The worker implemented the stronger byte IDENTITY
  `result == before + b"\n" + slice` and declared the substitution. An append
  reader is stated as the IDENTITY it must prove, never as an arithmetic a
  control can satisfy.

- 2026-08-28 · F037 R8 · The PLANF037R8 slice was authored at exactly 50 lines
  while the same block's G4 ordered `.agent/plan.md` strictly under 50, so the
  block contained two clauses no worker could satisfy together and the file sat
  one line over AGENTS.md's rule for a round. Checklist item 3 requires every
  authored full-replacement text to be counted against its own file's cap BEFORE
  emission; the count was carried over from an earlier round's slice instead of
  being re-measured after the last edit, which is the staleness shape the
  checklist already names. A cap is re-measured on the FINAL bytes of the slice
  that will land, never inherited from the slice it was adapted from.

- 2026-08-28 · F037 R11 · Finding `R-0721` states a parse cost of 0.363 s for a
  10k-line diff, and the figure is an artifact of the reviewer's own probe rather
  than a property of the parser: it was measured with `tracemalloc` active around
  the call. Measured clean afterwards, the same fixture parses in 0.101 s and the
  same fixture with `tracemalloc` running takes 0.262 s, so the instrumentation
  accounted for a factor of 2.6 and the different generated content of the probe
  for the rest. The R11 worker measured 0.105 s, reported the disagreement instead
  of transcribing the finding, and was right to. The finding's substance — linear
  cost, no ceiling — is unaffected and was re-confirmed. A timing figure that will
  be written into the append-only record is measured by the SAME instrument the
  round will use to check it, never through a profiler that is switched on for the
  memory reading beside it; a measurement's harness is part of the measurement.
