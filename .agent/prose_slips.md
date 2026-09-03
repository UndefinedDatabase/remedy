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

2026-08-29 · F257 R5 · The block's S2 asserted that `Path("..").name` is the empty string and that a single-component comparison would therefore refuse `..` unaided; it is `".."`, the worker measured it, and the explicit `entry.id in (".", "..")` arm it added is what makes the shipped check correct.
2026-08-29 · F257 R5 · Constraint 8's own summarising sentence — "one newline, then the slice, then one newline" — would leave every appended file ending in two newlines; the clauses around it are right, the worker followed those, and every append since round 3 has reconstructed byte-exactly.

2026-08-29 · F257 R10 · The block's G6(D) asked for the three ids from the negative control to appear "among the passing ones" while its own C3 step 3 ordered the third of those tests renamed, so the two clauses could not both hold literally; the worker reported that id under its post-rename name and declared the disagreement, which is the required behaviour.

2026-08-29 · F033 R1 · DECISION F033 D1 states that F256 moved `apps/ui/src/components/diff/DiffView.tsx` by "192 added lines" and `apps/ui/src/components/diff/DiffFileSidebar.tsx` by 45, but 192 and 45 are the `--stat` CHANGED-line totals; the added columns measured by `git diff --numstat 32cde54e..bd8d9529` are 172 and 27, the CSS figure of 63 is right, and the ruling's substance — that F256 rewrote F033's own surface and the parked inventory is stale on it — is untouched by the correction.

2026-08-29 · F033 R1 · The block's G6 called its list "the four state readers' full contract" while enumerating five tokens, which reads as a miscount although four READERS holding five TOKENS is consistent; the carried constraint inside `.agent/context.md` separately lists only four tokens for that file, omitting the `pytest`-or-`resource` token `tests/regression/test_resource_safety.py` asserts, and the next context rewrite should add it.

2026-08-29 · F033 R5 · The block's G3(c) ordered "the C2 blob plus one newline plus the Landed line, byte for byte" and "that commit's diff must ADD exactly one line" in the same gate, and the two cannot both hold, because the C2 blob already ends in a newline so the byte formula necessarily adds a blank separator and git reports two insertions; the worker followed the byte formula, matched the eleven pre-existing blank-separated `Landed:` lines, and declared the contradiction.

2026-08-29 · F033 R5 · The block's G5 ordered "zero changed lines that are not inside a comment or docstring" over `git diff BASE C3`, a range that also contains four `.agent/**` state files from C0a through C2, so the clause was unmeetable as written over the range it named; the worker proved the property over the two production files it was plainly meant for and reported the range's other paths openly.

2026-08-29 · F033 R6 · The block's SPEC §4 said a rejection entry in none of the three accepted spellings "is a `REFUSAL_MISSING_REASON`" while its own §3 fixed `UNKNOWN_HUNK` strictly earlier in the refusal order, so the two clauses are readable against each other; the worker took §4 as naming the fault class rather than overriding the order, shipped the order §3 fixed, and declared the tension.

2026-08-29 · F033 R8 · The block's "TWO CONSTRAINTS" paragraph said a synthesised patch "must set `target_paths` … or it fails validation", and `unsafe_path_issues(())` returns `[]`, so an unset `target_paths` would not in fact fail validation; every measured fact beside it was true and only the inferred consequence overshot, which the worker re-derived and declared.

2026-08-29 · F033 R8 · The block's G6 ordered the sha256 of "the target file" before and after the conflict call, in the singular, while a rollback can only be demonstrated with TWO files — a single-file conflict never reaches the applier's writer, so equal digests would prove ordering rather than restoration; the worker built the two-file fixture the property needs and reported both digests.

2026-08-29 · F033 R9 · The block's transport gate G2 ordered the sha256 of the C0a blob against the reviewer's scratch original and both readings reproduced, but the reviewer's own first re-derivation of the record append was short by one byte because its slice extractor consumed the newline ending the last content line; the committed append was correct all along and the corrected extractor reproduced 1471135 plus one newline plus 5939 exactly.

2026-08-29 · F033 R10 · The reviewer's own first re-derivation of the first appended paragraph's SPAN gave 1481911..1486856 where the worker reported 1481911..1486878, and the worker was right: the reviewer measured `len()` on a DECODED string while the offset is a BYTE offset, and this record's em-dashes and ellipses make the byte count 22 larger; both readings put the ordered control inside the paragraph, so the proof itself was unaffected.

2026-08-29 · F033 R10 · The block's G6(a) ordered the surviving clause "``landed`` is EMPTY whenever ``applied`` is false" reported as present, and the reviewer's own probe expected it exactly once while the file legitimately carries it twice — the module docstring gained the same sentence in round 9 — so the expectation rather than the file was wrong, and nothing the block ordered depended on the number.

2026-08-29 · F033 R11 · The block's SPEC §1 asked the recorder's persist-nothing paragraph to say it "leaves `save_job` to the door" while its own G6(b) ordered that token to read 0 in the same module, so the two could not both be satisfied literally; the worker read the gate as load-bearing, kept the paragraph's meaning by naming `escalation.answer_task_decision` and `_dispatch_decision_resolve` instead, and declared it, which is the required behaviour and is now stated as convention 11 of the next block.

2026-08-29 · F033 R11 · The handback reported the recorder's AST import list as 8 entries where the reviewer's own extractor counts 11 `(module, name)` pairs; both readings agree on the property the gate exists for — every entry standard library or one of the three allowed modules, with all five forbidden names absent — and the difference is only whether dotted names or import statements were counted.

2026-08-29 · F033 R12 · The block's Bundle line for C3 read "one dated line into `.agent/prose_slips.md`" while its own SLIPSF033R12 slice carried TWO dated paragraphs and G5 ordered the count without fixing it; the worker applied both byte for byte under convention 1 and declared the disagreement, which is the required behaviour, and the R12 append reconstructs exactly.

2026-08-29 · F033 R12 · The round 11 verdict recorded the recorder's AST import set as eleven names and this round's is twelve, which reads as drift and is not: `Mapping` was added for the `attempt_view: Mapping[str, Any]` annotation, it is standard library, and the property the gate exists for — every entry stdlib or one of the three allowed modules, all five forbidden names absent — is unchanged.

2026-08-29 · F033 R13 · The block's G6 was headed "THE CODE AGAINST THE SPEC at C4" while its clause (a) ordered `ruff` over `tests/orchestration/test_evidence_index.py`, whose edit the same block's Bundle placed at C5, so at C4 that path still held its BASE content; the worker read the gate as load-bearing, ran it at C4 and again over the C5 tree, reported both as exit 0 and declared the disagreement, which is the required behaviour and left nothing wrong on disk.

2026-08-29 · F033 R15 · The block's "Why this round exists" enumerated the equality-shaped guards over the write door as `UI_EXPOSED_COMMANDS`, `DOOR_METHODS`, `ALLOWED_IMPORTS` and `FORBIDDEN_MODULES`, and its SPEC then said nothing else in `tests/ui_server/test_command_channel.py` would change; a fifth guard, `TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives`, iterates the exposed set and hard-branched every non-`job.stop` id to one 409 message, so the worker had to widen it to a per-id map and declared the disagreement, which is the required behaviour — the reviewer confirmed by mutation that the widened form pins the two 409 messages apart and weakens nothing.

2026-08-29 · F033 R16 · The block's `ui_server.py` SPEC ordered the fold's WHY comment to QUOTE the membership test `if "applied" in apply_states` while its contract-test SPEC ordered an assertion that no membership test remains, so a text search would have been answered by the reviewer's own ordered comment — pre-emission checklist item 2's shape reaching a TEST rather than a done-when; the worker resolved it with an AST predicate that is strictly stronger, declared the disagreement, and the reviewer's mutation confirms the predicate discriminates.

2026-08-29 · F033 R16 · The block's bundle ended at C6, the handback commit, and said nothing about where the PUSH outcome is recorded, so the worker added a C7 to carry the real outcome instead of committing a promise; nothing on disk is wrong and the change set was not exceeded, and a future block should name the commit the push outcome lands in rather than leaving the worker to invent one.

2026-08-29 · F033 R17 · The block's SPEC B ordered `.checkPartial` to keep "the same white glyph colour" as `.checkDone` AND said "no raw hex colour is introduced", while the rule it ordered copied carries `color: #fff`, so the two clauses could not both be met literally; the worker applied the first, declared the disagreement, and the reviewer measured that the file's DISTINCT hex colour values are unchanged by the round, so the intended property held and only the wording was wrong — a clause about a VALUE SET should say so instead of saying "no raw hex".

2026-08-29 · F033 R17 · The block named C7 as the commit the push outcome lands in, which repaired round 16's slip, and then said nothing about whether C7 is ITSELF pushed, so C7's text predicted it would stay local and AGENTS.md Push Discipline falsified that prediction the moment the worker obeyed it; the worker spent a declared C8 correcting one sentence, and a block that names a post-push commit must also say what happens to that commit — the same slip one level down.

2026-08-29 · F033 R18 · The block's SPEC A4 ordered the moved fold to guard `ImportError` beside `AttributeError` and `TypeError` "so a malformed chain degrades exactly as it does today", but the new function performs no import — the old one did, which is why the guard was there — so one member of the ordered tuple is unreachable by construction; the worker applied it as written and declared it, and a spec that carries a guard across a move should re-derive which of its clauses the move keeps alive.

2026-08-29 · F033 R18 · The block's SPEC B3 claimed that after the move "the four apply labels are literals in `proof_chain.py` and in no other production module", which is true of the APPLY labels and false of a literal search for the string, because `_metrics_proof_from_chain` in `ui_server.py` sets a proof-metrics `state = "partial"` that has nothing to do with the fold; no gate ordered that count so nothing was unmeetable, and the lesson is the standing one that a sweep claim is only as wide as the search that measured it.

2026-08-29 · F033 R19 · The block's SPEC C1 ordered one docstring line and called it "the whole fix" while its SPEC C2 ordered a guard asserting that EVERY public module-level function is named in that list, and the two could not both hold, because `packages/orchestration/proof_chain.py` had six public functions and not five; the root cause is that the reviewer counted the module's public functions from the very docstring list it was accusing of being incomplete, instead of walking the module — a census taken from the accused, which is how finding R-0746 also landed with a wrong numeral, corrected in its resolution rather than by a rewrite.

2026-08-29 · F033 R19 · The block's G2 said to "extract its applied region from its target file" without naming the COMMIT the region is read at, and this round legitimately appended a `Landed:` line to `.agent/live_review.md` after the slice, so the slice stopped being the file's suffix at the branch tip while remaining exactly the suffix at the commit that applied it; the worker read each region at its own commit and declared the ambiguity, and an append gate should name the commit it is measured at whenever the same round writes to that file twice.

2026-08-29 · F033 R19 · The block's SPEC A2 told the worker to "build the chain the same way the rest of this module reaches evidence" without naming the two imports that takes — `resolve_data_root` and `load_run_events` — so the worker had to find them and declared the gap; a SPEC that points at a pattern rather than naming the calls leaves the worker to rediscover what the reviewer already read.

2026-08-29 · F033 R20 · The block's SPEC A6 ordered totality on all inputs, a re-stated coercion guard AND empty-string-on-unreadable without saying which of those is THE guard, so the obvious reading produces two overlapping defensive layers and the block's own G6(iii) would have reddened nothing — a mutation defeated by redundancy rather than by a missing test; the worker made the structural guard singular, confined the coercion guard to the id, and proved both are measured by disjoint tests, and a SPEC ordering defence in depth must name which layer its red-proof is aimed at.

2026-08-29 · F033 R20 · The session-close handoff stated the open set's movement twice — "259 to 257" for the round and "258 to 257" for the session — without either sentence naming the range it spanned, so the worker applying it reasonably read them as one quantity contradicting itself and proposed a correction that was itself false; both numerals were right, R-0746's mid-session registration is the difference between them, and a numeral about a MOVING quantity must name the two commits it is measured between or it invites a wrong repair.

2026-08-29 · F033 R23 · The block's G3 ordered the record append reconstructed from a base of 1588184 bytes, which is `.agent/live_review.md` at round 22's C2 and not at `d0c86c2d`, because that round's own C3 appended a 156-byte `Landed:` line AFTER the reading was taken; the worker measured the true 1588340, applied the append form unchanged and declared it, and a base numeral for a file the PREVIOUS round wrote TWICE must be read at the round's actual base commit rather than at the commit whose gate first measured it.

2026-08-29 · F033 R24 · The block's G5 ordered an absence swept "across `packages/`, `apps/`, `tests/` and `docs/`" and a plain recursive grep run that way also reads gitignored build artifacts, so the gate went red against a stale `__pycache__` object compiled from the pre-repair source while `git grep` over tracked content was already clean; the worker removed that one file by exact path, re-ran the gate unmodified and declared it, and an absence gate must be worded and run over TRACKED CONTENT, because such a gate can be red while the source property holds and green while it does not.
2026-08-29 · F040 R1 · The reviewer's PLAN1 slice marked "the seam inventory" as `done` in the Current Step table applied at C1, five commits before C6 wrote that inventory; the row was true when the round ended and false for the length of the round, and the block fixed the commit order without naming it in the slice, which is what §3 item 20's R-0524 carve-out asks for.

2026-08-29 · F040 R2 · The reviewer's DECISION F040 D3 paragraph states "THIS IS THE THIRD FEATURE FILE CARRYING THAT TYPO" from two precedent mentions it had grepped rather than from a count of the files; the round's own G5 sweep measured thirteen others still carrying it, so F040 was the fourteenth, and the numeral is the recollection §3 item 16 forbids standing beside a measurement.

2026-08-29 · F040 R2 · The reviewer's SPEC for C7 ordered "APPEND a new test class" and in the same paragraph "follow its fixture and naming conventions" over `tests/orchestration/test_decision_inbox.py`, which holds twenty module-level functions and no class at all, so the two halves of one instruction could not both be obeyed and the worker had to choose and declare.

2026-08-29 · F040 R2 · The reviewer's G4 required `.agent/prose_slips.md` to grow by exactly one line, which FORBADE the blank separator every other entry in that file carries, so the F040 R1 entry landed without one; the landed line is not rewritten and this round's append restores the convention going forward.

2026-08-30 · F258 R9 · The round's own block explicitly ordered two negative controls for its G3 append check (a byte flip inside each of two appended slices, in a disposable worktree), and the worker's handback skipped both while incorrectly stating the block ordered only the positive checks; the reviewer supplied both negative controls independently at the next gate and both behaved correctly, so the landed bytes were never wrong — only the worker's own account of what it had verified was, and a handback's claim about what a block ordered is exactly the kind of claim that should be read against the block's own text rather than trusted.

2026-08-30 — F106 R2's own gate G6 asserted `BuilderOutput.prepared_input`/`ReviewerOutput.prepared_input` would differ between a `resume=`-bearing call and a plain one; measurement at C3 showed every field equal including `prepared_input`, because `FakeProvider.build`/`review` do not thread `resume` into `prepare_call_input`'s options this round (correctly — T001a is additive-only). Reviewer-prose inaccuracy, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R8 · Round 8's own `.agent/plan.md`/`.agent/handoff.md` stated SESSION 2, carried forward unchanged from round 7's handback; round 7's SESSION 2 (rounds 5-7) had already ended when this new session began (a fresh session with no memory of round 7's authoring), so round 8 should have read SESSION 3 — this feature's first missed session-number increment. Corrected starting at round 9; nothing on disk under packages/apps/tests/docs is wrong, so no R-id (amend0827-process-diet rule 2).

2026-08-30 · F106 R9 · The block's constraint 5 predicted `Gate: F106 R8 — ` would read exactly 1x after C2's append; the worker measured 2x and the reviewer independently confirmed it — RECORD9's own G4 paragraph quotes the phrase a second time while describing what it measured, and this is a PRE-EXISTING, systemic property of this ledger's format (RECORD8 already read `Gate: F106 R7 — ` 2x before round 9 touched the file, `git show`-confirmed), not a defect this round introduced. A gate over a RECORD paragraph's own header must read "≥1x, exactly 1x counting only the header line" rather than a bare "1x", because every such paragraph's own G4 description quotes the previous round's header by name. Reviewer-prose inaccuracy, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R9 · The block's constraint 14 said each hoisted block carries "one added comment line"; the worker measured the added comment as one coherent note spanning 3 physical lines, not 1, and declared the discrepancy while confirming the SUBSTANCE (condition and session-id extraction logic byte-identical, only position moved) held exactly as stated. "Line" should have read "comment" or "note" — a wording imprecision, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R12 · The block's constraint 3 stated the record-append arithmetic as `base + 1 + RECORD12 + 1 + R-0759` (single-newline separators), assuming the base file already ended in a trailing newline — the pattern every earlier F106 round happened to hit. Round 11's own RECORD11 has no trailing newline (verified: last byte is `.`), so this round's real base does not end in `\n`, and the correct two-paragraph append needs `\n\n` before each new paragraph (base + 2 + 4516 + 2 + 2591 = 1864466, not the block's stated 1864464); the worker measured the real base directly, applied `\n\n` separators, and verified 801 blank-line units with the last two byte-equal to RECORD12 and R-0759 in order. Reviewer-prose arithmetic error, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R12 · G6 of round 12's block named "240 passed" for a stated "broadened suite" of seven files excluding `test_builder_prompt_golden.py` (which the same gate already counted separately at 28); the real seven-file combined count is 212, and 212 + 28 = 240 exactly — the 240 was the EIGHT-file combined total, mislabeled as the exclusive seven-file one. The worker measured 212 directly, flagged the mismatch, and reported the arithmetic that resolves it rather than silently substituting either number. Reviewer-prose labeling error, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R13 · The block's constraint 3 stated the record-append arithmetic as "base + 2 + 5004 + 2 + 1243 = base + 6249" — a self-inconsistent sum, since 2+5004+2+1243 = 6251, not 6249, a plain addition slip. The worker performed the operation exactly as described (measured base 1864466 bytes, `\n\n` separators, RECORD13 and Done: R-0759 hash-verified against the block's own stated hashes) and reported the correct real total, 1870717, rather than either the block's wrong figure or a silently "corrected" one. Reviewer-prose arithmetic error, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R14 · The round's own block (constraint 5) described PAIR2's and PAIR4's inline comments in `packages/orchestration/pingpong_loop.py` as "six-line" and "eight-line" respectively; both are independently measured at exactly 5 physical lines each in the real committed file. Reviewer-prose wording imprecision, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-08-30 · F106 R14 · The worker's own completion report stated the C6 handoff commit's insertions as 131/116; independently re-measured via `git diff --numstat c740b8f8^..c740b8f8` as 65/50 — the file itself was correct, only the worker's stated number was off. Worker completion-report slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).


2026-09-02 · F108 R7 · The reviewer's own step block's G8 clause quoted a stale base SHA (`76982f2f`, round 5's tip, carried over from round 6's own G8 text) instead of round 7's actual base (`e7ef578f`); the worker ran both the literal and the semantically-correct command and declared the discrepancy, confirming the change set was exactly the 8 declared paths. Reviewer-prose citation drift, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-02 · F108 R12 · The round's own handback (`.agent/handoff.md`, committed at `4733812a`) stated commit `1faeed0c`'s `tests/orchestration/test_artifact_summaries.py` change as `+5/-3`; independently re-measured via `git show --numstat 1faeed0c -- tests/orchestration/test_artifact_summaries.py` as 3 insertions, 5 deletions — the two figures were swapped. The file's own diff (three names merged into the first import block, the second `from ... import (...)` block's five lines removed) and every gate result (ruff, pytest, ledger counts) were unaffected. Worker completion-report slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R1 · The reviewer's own step block ordered gate G8 to report the insertion count of "each commit from C0a through C5 — six numbers", while the same block's Bundle enumerates C0a, C0b, C1, C2, C3, C4 and C5, which is seven; the worker applied the clause as written per constraint 1, reported all seven counts and declared the contradiction. The checklist item this breaks is §3 item 32 — a clause naming a KIND of the block's own parts states no COUNT of that kind — and the block's arithmetic was right while only the adjective was wrong. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R1 · The reviewer's own step block defined gate G4(a)'s byte arithmetic as "2015028 + 2 + S, where S is the byte length of SLICE RECORD as saved to scratch" without saying whether S included the trailing newline a POSIX text extractor appends, while the same block's constraint 4 required the appended file to end WITHOUT one; the worker resolved the ambiguity correctly in favour of constraint 4 (S = 3285, not 3286), landed the correct bytes and declared the discrepancy so a reviewer recomputing S from the raw slice would not read it as a mismatch. Reviewer-prose ambiguity between two clauses of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R2 · The reviewer's own step block contradicted itself between two clauses: constraint 4 ruled that "Nothing already in either file is edited, reordered or deleted" for commits C4 and C5, while SPEC A's final paragraph ordered the `session_sent_index.py` module docstring reworded and three names added to its Public API list, which is an edit of existing lines in exactly one of those files. The worker resolved it correctly in favour of the specific instruction over the general one, applied the docstring change as SPEC A ordered, and declared the contradiction rather than silently choosing; the resulting commit carried 90 insertions against 2 deletions, the two deletions being precisely the old docstring bullet. Reviewer-prose contradiction between two clauses of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R6 · The reviewer's own step block ordered gate G4 to prove that the line-level opcodes between the pre-commit and post-commit blobs of `packages/orchestration/pingpong_loop.py` and the test file were `equal` and `insert` ONLY, with no `replace`, while SPEC G and constraint 6 of that same block explicitly ordered three SINGLE-LINE import statements to be EXTENDED — and extending a one-line statement can only ever surface as a `replace` at line granularity, so the clause was unmeetable for every possible execution of the round it was written for. The worker applied the SPEC as ordered, measured the opcodes, reported a delete count of 0 in both files with every `replace` quoted and matched to a named import extension, and declared the contradiction instead of narrowing the SPEC to fit the gate. The checklist neighbours are §3 item 18, which reads an ordered recipe against the property it must establish, and §3 item 8, which reads a gate's expected VALUE against the code — neither was run against the block's own two halves here. Reviewer-prose contradiction between a gate and a SPEC of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R7 · The reviewer's own step block ordered gate G5 mutation B to pass `session_sent_index.sent_hashes(builder_resume_ref or "")` unconditionally at the builder call site and required the non-resume chain case to go red, but `SessionSentIndex.record_call` refuses a call whose session id is empty, so `sent_hashes("")` is permanently `frozenset()` and an empty container composes byte-identical bytes to `None` — the ordered mutation was an EQUIVALENT MUTANT and no run of it could ever have produced the demanded colour. The checklist item this breaks is §3 item 5, which permits a mutation red-proof only where the mutated branch is reachable by the tests meant to redden, and the reviewer had in fact measured the `frozenset()` equivalence itself during the pre-emission dry run without connecting it to the mutation it invalidated. The worker diagnosed the equivalence inside the mutated worktree, reported the green honestly instead of reporting a colour, and ran a substitute discriminator of the same intent using a session key the index can hold, which reddened exactly the intended case. Reviewer-prose defect in a gate, nothing wrong on disk and the intended property still discriminated; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R18 · The reviewer's own `R-0783` finding text called itself "THE SIXTH SITE" of the stale-prose class while its own enumeration omitted `R-0782`, making the true count SEVEN; corrected in the round 18 gate entry rather than here, because this file stopped being written after round 7. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R18 · The reviewer's own step block gate G6 required a marker string to "resolve in the modules named", where that string is defined in ONE module and reaches the other by import, so the clause was unmeetable for the second module. Reviewer-prose defect in a gate, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R18 · The reviewer's own step block gate G3(d) named a base two rounds earlier than G3(a) named, so the ledger delta that clause ordered spanned two rounds instead of one. Reviewer-prose citation drift between two clauses of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R17 · The reviewer's own step block constraint 6 sent a running suite's log to a path INSIDE the measured repository on an over-wide reading of `R-0176`, which the worker corrected by measuring that `worktree_identity()` cannot see a gitignored file. Reviewer-prose over-wide constraint, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R17 · The reviewer's own step block implied `REMEDY_UI_NO_AUTO_BUILD` for the whole integration gate, where `docs/agents/integration_gate.md` scopes that variable to the BASE run alone. Reviewer-prose over-wide constraint, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R20 · The reviewer's own step block asserted the review zip would land in the repository root, where the packager archives it OUTSIDE the repository. Reviewer-prose defect in a stated location, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R21 · The reviewer's own closure block named `.agent/plan.md` in the path set its commit C3 had to touch while the same block's bundle assigned the single authored plan slice to C1, leaving C3 no plan diff to make; the worker declined both routes to a green gate, reported the gate PARTIAL and landed four paths. This is the `R-0527` class, and the checklist neighbour is section 3 item 35. Reviewer-prose contradiction between a constraint and a bundle of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R21 · The reviewer's own closure block gate G6 ordered the literal U+2014 count in `scripts/self_use_queue.json` compared before and after the edit as the discriminator against a `json.dumps` round trip, and that count is 0 on both sides because `R-0785`'s damage had already escaped every such character on disk, so the reading cannot distinguish a correct text edit from the round trip it was written to catch; the worker declared it vacuous and supplied three non-vacuous readings. The checklist item is section 3 item 27, and the underlying on-disk defect stays registered as `R-0785` with no second id minted, per section 3 item 30. Reviewer-prose defect in a gate, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R1 · The reviewer's own pre-emission count of the round 1 block projected 397 lines and the block as emitted and committed is 398, measured on the committed `.agent/authored/f110-r1.md`; the §3 item 1 cap of 400 was met either way and no gate consumed the projected figure. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R1 · The reviewer's own step block admitted two readings of "the slice" for the SLIPS1 append — constraint 3 required `.agent/prose_slips.md` to keep ending without a newline while gate G5(b) asked the file's final bytes to equal the extracted slice, which is 3383 bytes with the newline terminating its last line and 3382 without — and only the 3382 reading satisfies both; the worker took it, reported both numbers and declared the ambiguity instead of choosing silently. Reviewer-prose ambiguity between two clauses of one block, nothing wrong on disk and the intended bytes landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R1 · The worker's completion report gave commit `bbfbb83b`'s insertion count as 594, which is `.agent/handoff.md`'s line count rather than the `+` column; `git show --numstat` reads 485 insertions against 376 deletions, and the figure never entered any committed file because the block had already routed that commit's numbers to the next gate. This is the §3 item 28 class. Worker completion-report slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R2 · The reviewer's own pre-emission count of the round 2 block projected 262 lines while the block as committed is 263, measured on `.agent/authored/f110-r2.md` — the same off-by-one as the round 1 projection of 397 against a committed 398, and from the same cause: the projection SUMS per-slice line counts plus hand-counted marker and blank lines instead of counting assembled bytes. The §3 item 1 cap of 400 was met with room in both rounds and no gate consumed the projected figure. THE COUNTER-MEASURE RECORDED HERE IS THE ONE ACTUALLY AVAILABLE, because the obvious one is not: assembling a block of this size in a single pass to count it exceeds the reviewer's own tooling limit, so from round 3 on every block's gate G1 additionally reports `wc -l` of the COMMITTED authored file, which turns the projection into a measurement the round itself checks rather than a number the reviewer is trusted on. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R3 · The reviewer's own step block contradicted itself between two clauses: SPEC CODE (b) explicitly permitted removing a `get_config` import that became unused, while gate G5 required the production change to be "the new function, its docstring entry, and the two model arguments - nothing else". The worker removed the two genuinely dead imports as the SPEC directed, reported the resulting counts, and declared the conflict instead of silently choosing; the reviewer confirmed both files still import and that `grep get_config` returns nothing in either. The checklist neighbour is §3 item 35, which requires a block's prose and its enumeration to be read against each other. Reviewer-prose contradiction between a SPEC and a gate of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R3 · The reviewer's pre-emission line projection was wrong for the third consecutive round — 233 stated against a committed 236 — but this is the first round in which the ROUND caught it rather than the reviewer noticing afterwards, because the `wc -l` clause SLIPS3 instituted ran as gate G1 and reported the real count beside the projection. Recorded as evidence that the counter-measure works and should stay, not as a fresh defect. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R4 · The worker's own open-set script read 65 resolved and 282 open against `.agent/live_review.md`, where rounds 2 and 3 had stated 69 and 278; the reviewer recomputed under five independent readings — strict and loose registration matches, strict and loose `Done:` matches, and the first-R-id-per-`Done:`-line reading F109 round 20 pinned as canonical — and all five agree on 347 registered, 69 resolved across 71 `Done:` lines and 278 open, with every resolved id also registered and no non-standard `Done:` line in the file. The stated figure was right and the worker's script carries a defect its report does not expose. It cost nothing, because the worker reported the DELTA it could reproduce (zero movement between base and head) and declined to overwrite a figure it could not — which is the honest form of a disagreement and the behaviour to keep. Worker measurement slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R6 · The reviewer's G4 second reader was worded to compare the file's trailing blank-line units against the RAW slice's paragraphs, but constraint 4 of the same block orders the target's newline convention to win, so `.agent/decisions.md` legitimately carries one trailing newline the slice does not and the reading returned False on the eighth of eight paragraphs while the byte-equality proof beside it was exact and total. Reviewer gate-wording slip, nothing wrong on disk; the worker reported BOTH readings rather than choosing the green one, which is the behaviour to keep. No R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R6 · The reviewer's G6 discriminator demanded that each mutation "leave the OTHER mutations' cases GREEN", which no round could satisfy: four of that file's cases assert over an override map breaking every rule at once, so they belong to no single mutation and redden under several by construction. The property that actually discriminates, and that the reviewer measured pairwise at `a62d4920`, is that each mutation reddens exactly its own rule's parameter of `test_the_message_names_every_violated_rule` plus its own dedicated fixtures, and reddens no other mutation's dedicated fixtures. Reviewer gate-wording slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R7 · THREE CLAUSES OF THE ROUND 7 BLOCK SHARED ONE ROOT CAUSE: the reviewer derived them from a probe that widened the report-order tuple with dummy names and never exercised the promotion CHECK the same round ordered built. SPEC (o) therefore predicted six red guards where twelve go red; constraint 7's "a caller supplying no evidence map gets round 6's answers unchanged" is unmeetable for any map demoting a seeded class, since every orchestration and fixture-safety class is seeded at the top tier and any demotion of one is also a promotion; and G5's permitted-deletion regions omitted the validator docstring and the builder's call line that SPEC (g) and (h) necessarily change. The worker declared all three, chose correctly on each, and widened rather than weakened every affected test. THE LESSON: a pre-emission probe must exercise the BEHAVIOUR the round ships, not only the SHAPE of the constant that names it — a tuple widened with dummy names cannot show what a real check does. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R8 · Constraint 4 of the round 8 block stated `.agent/prose_slips.md` as 53575 bytes at `4cfcb464` where the file really held 54853 — the reviewer re-derived the figure by arithmetic from an earlier round's base instead of re-measuring it at the round's own base. The stated newline convention was correct and G4 gated that file by byte equality rather than by arithmetic, so the append landed exact and nothing on disk was wrong; the worker applied the constraint as written and declared the discrepancy, which is what constraint 1 asks for. THE LESSON: a byte figure quoted for one round's base is RE-MEASURED at the next round's base, never carried forward or re-derived in the reviewer's head. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R9 · The round 9 block's SPEC (f) ordered the `role_config.py` Public API list to gain "a line for RoleConfig's new field and one for resolve_role_config's new parameter" — two — while the same block's SPEC (d) ordered a NEW PUBLIC FUNCTION into that module, so three were owed. The worker added the third, named it in deviation D2 and was right to. The reviewer enumerated the API additions from the two SPEC items that mentioned the docstring rather than from the round's whole set of new public names. THE LESSON: when a block enumerates what a docstring's Public API list must gain, derive that list from every public name the round ships, not from the SPEC items that happen to mention the docstring. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R9 · BOTH the worker's and the reviewer's red-proof harnesses mis-parsed pytest's own output in the same round, in different ways: the worker's compared summary lines INCLUDING the elapsed time and so reported a false "back to control" mismatch (its deviation D4), and the reviewer's took the FIRST whitespace-separated token of each "FAILED ..." line as the node id, collecting the literal string "FAILED" for every failure and producing a red-set intersection analysis that was an artifact of the parser rather than a measurement. Both were caught before anything landed — the worker re-ran the whole gate, and the reviewer printed one raw failing line and re-ran. THE LESSON: a harness that derives a SET from tool output prints one RAW line of that output beside its parsed result before any conclusion is drawn from it; a parsed set that is never checked against the bytes it came from is a measurement in appearance only. Reviewer and worker tooling slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R10 · The reviewer's checklist item 34 sweep for the round 10 block read the guards on every test file that IMPORTS or COUNTS over the two edited production files, and missed `tests/orchestration/test_orchestrator_model_routing.py`, which does neither — it patches `packages.orchestration.config.get_config` with a stub that REFUSES any key but `orchestrator.model`, and so broke when `resolve_role_config` gained a second, legitimate config read. The reviewer's own DECISION D4 measurement had even listed `role_config.py`'s `resolve_orchestrator_model` among the call sites, so the file was one hop from being read. Registered as `R-0787` because the branch tip went red; recorded here as the AUTHORING lesson the id does not carry. THE LESSON: item 34's "read the tests that already guard that file" extends to tests that STUB A DEPENDENCY of an edited function — a monkeypatched double is a guard on the call path even though it names neither the edited file nor its symbols, and `rg -l '<basename>' tests/` cannot find it. Search for the patched TARGET (`get_config`, `resolve_role_config`) as well as for the edited file's own name. Reviewer block-authoring slip; no second R-id spent for the lesson (amend0827-process-diet rule 2).

2026-09-03 · F110 R11 · The round 11 handback reported the open-finding set as "278 open over 349 registered and 71 resolved", computing it as 349 minus 71 — LINE counts rather than sets of unique ids. `.agent/live_review.md` carries TWO `Done:` paragraphs each for `R-0721` and `R-0725`, so the unique resolved count is 69 and the open set after that round's two registrations is 280, not 278. The block's own Handback clause asked for the derivation "every '^- R-\d+ — ' paragraph minus every '^Done: R-\d+ — ' line" and thereby invited the line-count reading, so the wording is the reviewer's to answer for. Nothing on disk is wrong: the ledger is append-only, both duplicate resolutions are landed history that must not be rewritten, and checklist item 10 requires every block to recompute the set mechanically rather than carry a number forward. THE LESSON: an open-set derivation is stated as a set difference over UNIQUE IDS, and any block that orders the count says "unique" in the order — a ledger that has ever resolved one id twice makes the line-count reading silently wrong, and this one has. Reviewer block-wording slip; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R12 · The round 12 block's G6 told the worker to parse a pytest failure id as "the SECOND whitespace-separated token" of a `FAILED ...` line. That is wrong for any PARAMETRIZED id whose parameter contains a space — `FAILED path::Class::test[a wrong-typed field-entry2]` truncates to `path::Class::test[a` — so the worker's first harness run produced a truncated red set and a disjointness reading it could not trust. It discarded that run, corrected the parse to take everything after the first space, re-ran the whole gate and printed both readings side by side, which is exactly the behaviour the round 9 slip asked for. The irony is on the record deliberately: the same block's G6 also carried the round 9 lesson about printing a raw line beside a parsed set, and it was that instruction which caught the reviewer's own bad rule. THE LESSON: a node id is EVERYTHING AFTER THE FIRST SPACE of a `FAILED ` line, never a whitespace-token index, because pytest parameter ids may contain spaces; and a block that orders a parse states the rule in terms of the delimiter, not the token number. Reviewer block-wording slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R13 · The round 13 block set its constraint 9 ("a sentence this round makes stale INSIDE the change set is repaired in the commit that falsifies it") against its constraint 7 and its gate G5 ("model_routing.py is edited for its MODULE DOCSTRING ONLY and any deletion outside that docstring is a STOP"), and the sentence the round falsified sits in a FUNCTION docstring — so the two clauses could not both be obeyed and the worker was correct to declare the conflict and repair nothing. Registered as R-0789 because the false sentences are on disk in production code. THE LESSON: a permitted-deletion region is scoped to the SMALLEST region that still contains every sentence the round can falsify, and a block that names "the module docstring" must first grep the file for the other prose its own change makes false — a deliberate-absence note lives wherever the absence was, and this feature has now written such notes in three files.

2026-09-03 · F110 R13 · The block's gate G2 ordered "cmp the PLAN13 extraction against `.agent/plan.md` — exit 0" while its own constraint 4 states that the TARGET's convention adds one trailing newline the slice does not carry, so a literal cmp of the raw extraction cannot exit 0 and the two clauses disagree. Every round from 8 onward has carried this same wording and every worker has resolved it the same correct way, but this round's worker was the first to say so, running BOTH comparisons and reporting both exit codes rather than silently picking the green one. THE LESSON: state the gate as "cmp the slice PLUS the target's trailing newline", so the ordered command and the stated convention agree on the page instead of relying on the worker to reconcile them. Applied in this round's own G2.

2026-09-03 · F110 R14 · The round 14 block sent the worker into `remedy-review-r9-scratch/` — the REVIEWER's own scratch directory — without reserving a namespace for the worker's files, so the worker created its own `probe14.py` over the reviewer's file of that name and then correctly removed it by exact path, exactly as the no-delete-by-glob rule asks. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` was wrong and no gate depended on the lost file, which the reviewer simply rewrote under a different name; the worker declared the removal in its handback, which is how it was traced at all rather than guessed at. THE LESSON: a block that names a shared scratch directory gives the worker its own prefix for anything it creates there, because a reviewer's pre-emission probe and a worker's gate script converge on the same obvious filename, and the reviewer's copy is the one that vanishes silently.

2026-09-03 · F110 R15 (reviewer) · Polling a background pytest run's captured-output file for byte-growth was read as a liveness signal — three samples 90-180s apart showed the file frozen near 99% and were reported mid-round as "the base run appears hung." The run had, in fact, either already finished or was progressing normally behind a buffer that had not yet flushed; the worker's own investigation (fresh completion timestamps, a matching wall-clock reading between the run's meta file and pytest's self-report, an ordinary tail with tracebacks, zero live processes) found no hang and took no corrective action. THE LESSON: a captured log's byte count is evidence of I/O buffering, not of process liveness; check the run's own completion artifacts (a written end-timestamp, the process table) before reporting a stall, rather than sampling a log file's size. Reviewer-prose false alarm, nothing wrong on disk, no process was harmed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F112 R2 · The reviewer's own PLAN2 slice left its END marker boundary ambiguous, and the worker's marker-delimited extraction dropped `.agent/plan.md`'s final trailing newline as a result (45 lines, content otherwise byte-identical to the reviewer's scratch copy); the same ambiguity dropped the trailing newline of the whole committed `.agent/authored/f112-r2.md` file after its last marker line, with zero effect on any slice's content. Neither is wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F112 R4 · G3's literal append formula `content_bytes + b"\n\n" + RECORD3_bytes`, applied verbatim as instructed, produced three consecutive newlines before RECORD3's `Gate:` line instead of the two-newline (one blank line) shape every other entry in `.agent/live_review.md` carries, because `content_bytes` (measured 2250826 bytes, matching the block's own pinned figure) already ended in its own single trailing newline before the append; the second-reader split-on-`\n\n` check therefore reads the last unit as one leading newline plus RECORD3 rather than exact byte equality to RECORD3, while the pinned byte-count arithmetic (pre-size 2250826, RECORD3 1739 bytes with zero internal newlines, post-size 2252567) matches exactly as specified. Applied as written per instruction, not silently corrected; nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F112 R5 · G4's literal append formula `content_bytes + b"\n\n" + RECORD4_bytes`, applied verbatim as instructed, again produced three consecutive newlines before RECORD4's `Gate:` line instead of the two-newline (one blank line) shape every other entry in `.agent/live_review.md` carries, for the same reason as round 4: `content_bytes` (measured 2252567 bytes, matching the block's own pinned figure) already ended in its own single trailing newline before the append. The pinned byte-count arithmetic (pre-size 2252567, RECORD4 2300 bytes with zero internal newlines, post-size 2254869) matches exactly as specified. Applied as written per instruction, not silently corrected, per round 4's own precedent; nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong; no R-id spent (amend0827-process-diet rule 2).
2026-09-04 · F112 R14 (reviewer) · The round 14 block inherited the SESSION label "SESSION 4" verbatim from round 13's handback instead of incrementing it — planner_reviewer_prompt.md §1 step 3 states a fresh bootstrap's session number is the carried value plus one, and this /build-remedy-self invocation was a fresh bootstrap, not a continuation of the session that produced round 13. THE LESSON: before authoring the first block of any invocation, check whether THIS bootstrap is a continuation or a fresh start, and bump the SESSION NUMBER on a fresh start rather than copying the prior handback's value forward; round 15 corrects the label to SESSION 5. Reviewer-prose tracking slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
