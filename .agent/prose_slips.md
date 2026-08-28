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

- 2026-08-28 · F037 R12 · The resolution `Done: R-0721 — RESOLVED IN PART`
  removes that id from the open set the pre-emission checklist derives
  mechanically — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — while half of the finding, the unbounded artifact read in
  `diff_view_source.py`, is still open on disk. The remaining half survives in
  prose only, in the handback and in the plan's Next Steps. A partial
  resolution is invisible to the one arithmetic the checklist runs, so a round
  that resolves half of a finding says so in the resolution AND leaves the
  remainder somewhere the count can see it.

- 2026-08-28 · F037 R15 · The R15 block declared that the round's TypeScript
  could not be type-checked here and ordered no gate for it, and the worker
  reported the same in its deviations after `tsc --noEmit` was refused from its
  shell. Both are wrong about the environment rather than about the code:
  `tests/ui_server/test_dashboard_contract.py` runs the repository's LOCAL
  `apps/ui/node_modules/.bin/tsc --noEmit` from pytest and skips only when that
  binary is absent, and the reviewer measured it at `68680786` as exit 0 with
  the new module on disk. This is the second time in two rounds that a tool was
  called unavailable after being refused from ONE caller, the first being the
  vitest runner that `R-0724` records: before writing that a tool cannot run
  here, grep `tests/` for a node that already runs it.

- 2026-08-28 · F037 R21 · The R20 block contradicted itself and one of its
  asides was inexact: constraint 10 stated that NO TypeScript mutation red-proof
  was ordered while G6 ordered two, and the claim that the `Gate: F037 R16`
  entry records why every vitest route is blind is not what that entry says. The
  worker declared both and routed around neither, and nothing landed wrong on
  disk. DECISION F037 D10 settles the underlying question by measurement: the
  red-proofs were orderable all along, and successive blocks said otherwise
  because each inherited the sentence instead of re-running it.

2026-08-28 · F256 R1 · The PLANF256R1 slice's Current Step table read `the per-line highlight model | done` at C1, where the slice lands and the model does not yet exist; it became true at C3 within the same round. The worker applied it byte for byte per constraint 1 and declared it.
2026-08-28 · F256 R1 · The block listed `.agent/handoff.md` in its change set while fixing G8's range to end at C3, which cannot reach the commit that writes the handback; the worker reported both readings rather than the convenient one.
2026-08-28 · F256 R1 · The G4 reader (b) counted N as 7 blank-line units where the DECF256R1 slice holds 6 paragraphs plus an empty trailing unit; the comparison still covered the whole appended region, so the obligation of §3 item 36 was met.

2026-08-28 · F256 R2 · The reviewer's R1 fuzz probe used a 32-bit LCG evaluated in floating point, so its low bits degenerated and its language and character coverage were narrower than the R1 entry's wording implies; re-measured with a xorshift generator at F256 R2, the property held over 4452 distinct lines. The correction is appended to the record in the R2 entry.

2026-08-28 · F256 R3 · The block's prose ordered `.agent/decisions.md`'s append "separated by exactly one blank line" while its gate G4(a) ordered `base + newline + slice`, and that file's blob already ended with a blank line; the two are unsatisfiable together, the worker obeyed the gate and declared it, so D2's heading is preceded by two blank lines.
2026-08-28 · F256 R3 · The block's G9 marker sweep expected 0 in "every non-authored target", which cannot hold for `.agent/last_block.md` because C0b and G2 require that file to be the identical blob to the authored control; the worker reported 4 and declared it.

2026-08-28 · F256 R7 · The block's G7 mutation (ii) quoted its anchor inside a four-space-indented code block, so the line it displayed carried eight leading spaces where `apps/ui/src/api/diffViewModel.ts` carries four; the worker asserted uniqueness on the correct four-space form, applied it and declared the difference, so nothing on disk was affected.

2026-08-28 · F257 R1 · The block's G4 reconstruction formula read "base + newline + DECF257D1 + newline + DECF257D2" while the same block's slice-convention paragraph required one BLANK LINE before each appended slice and a trailing newline; the two clauses disagreed, the worker followed the convention, and `.agent/decisions.md` is byte-correct on disk.

2026-08-28 · F257 R1 · The block's G7 structure gate ran over a range ending at C2 while its change set named `.agent/handoff.md`, which C3 writes, so the changeset-minus-range residue could never be empty; the worker reported the residue and declared it rather than dropping the path.

2026-08-28 · F257 R2 · The block's G5 ordered the open set as "the registrations minus the resolutions" without saying whether resolutions are counted by line or by distinct id; the two differ by two because `R-0721` and `R-0725` each carry a partial and a remainder `Done:` paragraph, so the worker honestly reported 249 where the correct figure is 251.

2026-08-29 · F257 R3 · The handback's G3 reported `.agent/plan.md` at C1 as 1591 bytes where the blob is 1593, and its G4 gave the first appended paragraph's span as 1378358..1378622 where the reviewer's script measures 1378358..1378625; both equality claims the two numbers decorate are correct and reproduced, so nothing on disk is wrong.

2026-08-29 · F257 R4 · The block's PLANF257R5 predecessor marked the consumption-point item `done` in the plan applied at C1, three commits before C4 made it true; the worker applied it verbatim under constraint 1 and declared it, which is the required behaviour.
2026-08-29 · F257 R4 · The block's FINDF257R4 called the R-0733 fix "four lines long" where the shipped guard is an `if` and a three-line `raise`; the estimate was written before the code existed and nothing on disk depended on it.
