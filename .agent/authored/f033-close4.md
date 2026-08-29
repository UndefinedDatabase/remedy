# F033 — SESSION 4 CLOSE · apply the reviewer's round 16 verdict

You are the WORKER for the closing action of SESSION 4. AGENTS.md is the highest
authority and binds you in full. This is NOT a round: it ships no code, and its
whole purpose is to put the reviewer's round 16 verdict on disk, where operator
amendment amend0827-process-diet rule 1 makes a committed and pushed
`.agent/handoff.md` a durable carrier for it.

## Base

BASE is `c7dc3cc07ffb000da337cba2390c6bcb85b36ee7`, the round 16 push-outcome
commit, on branch `feature/f033-hunk-approval-v2`. Confirm with
`git rev-parse HEAD` before you start and STOP if it differs.

## What to do

ONE commit. Replace `.agent/handoff.md` ENTIRELY with the HANDOFFCLOSE4 slice
below, byte for byte — it is a whole-file slice ending in exactly one trailing
newline. Do not edit it, do not reflow it, do not add to it. Save the block first
to `.agent/authored/f033-close4.md` by copying
`.remedy-wt/f033-close4-block.md` with `shutil.copyfile`, and commit both paths
together.

Take the slice from the COMMITTED blob you just saved, never by retyping.

## Change set — these paths and nothing else

    .agent/authored/f033-close4.md
    .agent/last_block.md
    .agent/handoff.md

## Done when

Run every one and report the REAL exit code and the actual numbers.

- **G1 HYGIENE.** `.agent/STOP` read from disk before you start and again after
  the commit, absent both times. `git status --porcelain` empty after the commit.
  Branch `feature/f033-hunk-approval-v2`. No force-push, no rewrite, no branch
  deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of the committed
  `.agent/authored/f033-close4.md` and of `.remedy-wt/f033-close4-block.md`, and
  whether they are EQUAL. Then report that the committed
  `.agent/authored/f033-close4.md` and `.agent/last_block.md` print ONE blob id.
- **G3 THE HANDOFF.** The committed `.agent/handoff.md` is byte-EQUAL to the
  HANDOFFCLOSE4 slice — report its byte length, its line count, and the equality.
  Report that it ends in exactly one newline.
- **G4 THE LEDGER IS UNTOUCHED.** `.agent/live_review.md` is byte-identical at
  BASE and at your commit, by blob id, and so are `.agent/plan.md` and
  `.agent/prose_slips.md`. This action books nothing: the next round does that.
- **G5 THE CANARY.** `pytest tests/cli/test_golden_path.py -q` — report the REAL
  exit code and count. 42 at BASE.
- **G6 STRUCTURE.** Your commit has exactly ONE parent and is under 500
  INSERTIONS — report the number. Report its path set against the change set in
  BOTH directions. `git ls-files .remedy-wt` must read 0.

Then push: `git push -u origin feature/f033-hunk-approval-v2`, and report the
command and its outcome.

Do NOT create a pull request. F033 is not closed — T003 is open — and
docs/agents/planner_reviewer_prompt.md §5 rules that the PR is created in the
CLOSURE sequence and merged at the NEXT feature's start.

## The slice

<<<SLICE HANDOFFCLOSE4
# Handback — F033 · SESSION 4 CLOSE · rounds 13 through 16

> Written by the REVIEWER at the close of session 4 and applied by a worker,
> because the reviewer writes no work-tree file itself. It carries the round 16
> verdict and two reviewer prose slips. Operator amendment amend0827 rule 1: a
> verdict committed and pushed HERE is persisted, and is booked into
> `.agent/live_review.md` in the FIRST COMMIT of the next round that is happening
> anyway — never in a round of its own.

## Session

SESSION 4 of feature F033 · rounds 13, 14, 15 and 16 delegated · rounds so far 16.
The NEXT session is SESSION 5 of 7 against the amend0827 rule 6 soft limit.
The soft limit is NOT reached: 16 rounds of 25, 4 sessions of 7.

## Fortschritt

~88 % (T001 and T002 complete: identity · decision · subset · apply ·
failed-rollback truth · ledger · recorder · envelope seam · one evidence-directory
rule · the CLI command · the write door. T003 open: the partial apply truth landed
with its first surface; the node glyph, the report line and the rejection-to-repair
injection remain) — Schätzung.

## Range

`d526dfb5`..`c7dc3cc07ffb000da337cba2390c6bcb85b36ee7` on branch
`feature/f033-hunk-approval-v2`, pushed; `origin/feature/f033-hunk-approval-v2`
is at the same commit. 21 files, 3876 insertions and 509 deletions over the
session. Every round was gated by the reviewer, which re-ran each round's own
gates from scripts of its own, reproduced every ordered reading, and re-ran every
mutation with its own anchors in its own disposable worktree before writing a
verdict.

## Verdicts

| Round | Subject | Verdict | Ledger entry |
|-------|---------|---------|--------------|
| 13 | the shared evidence-directory resolver | PASS | `Gate: F033 R13` at `096b8539` |
| 14 | the CLI command and its handler | PASS WITH RISKS | `Gate: F033 R14` at `bd83cedb` |
| 15 | the write door, and R-0744 | PASS | `Gate: F033 R15` at `807f6f25` |
| 16 | partial apply state becomes tellable | PASS | NOT YET BOOKED — see below |

## Round 16 verdict — PASS, and it is not yet in the ledger

The next round books it. All eight gates were re-executed by the reviewer at
`c7dc3cc0` and every ordered reading reproduced. TRANSPORT: the C0a blob is 30868
bytes at sha256 `8fcdfcd2…df874d`, EQUAL to the reviewer's own scratchpad
original, with ONE blob id at C0b — a chain walking the saved copy, its mirror and
the working copy, which is what this workflow can measure and is not a claim about
the emitted bytes. THE RECORD APPEND at `807f6f25` reconstructs 1535259 plus one
newline plus 7464 to 1542724, the committed blob exactly, base a byte PREFIX, N
COUNTED at 3, the last three blank-line units equal to the slice's paragraphs IN
ORDER, and a negative control at byte 1537103 — proved to lie inside the FIRST
appended paragraph, spanning 1535260 to 1538947 — rejected by BOTH readers. THE
LEDGER: registered 305 to 306 with the ADDED id exactly `R-0745`; `Done:` 49 lines
over 47 distinct to 50 over 48 with the ADDED resolved id exactly `R-0744` and the
`Landed: R-0744` line still standing beside its new `Done:` paragraph; `Landed:`
17 UNMOVED, this round writing none; `Gate:` 132 to 133 with `^Gate: F033 R15 — `
exactly 1; `DECISION F033 D` 4 UNMOVED; the open set 258 at BOTH; and `- R-0738`
still registered with no `Done:` line, which is correct — this round ADVANCED that
finding and did not resolve it. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to
its slice at 2453 bytes over 44 lines, under the 50-line cap; `.agent/prose_slips.md`
reconstructs 24266 plus one newline plus 715 to 24982. THE FOLD: the shipped apply
fold agrees or says `partial`, and the reviewer traced every branch by hand,
including the two the SPEC did not name — a task whose every change carries the
`getattr` default reads `not_applied` exactly as before, and a task mixing
`reverted` with that default now reads `partial` where the old membership test said
`reverted`, which is the same defect and the same repair. The PROOF fold three
lines above is byte-identical. THE MUTATIONS were re-run by the reviewer in its own
disposable worktree at `c924eb41` with its OWN anchors, each asserted UNIQUE, the
import proved to resolve inside the worktree and every file restored
byte-identically: controls 39 and 13 at REAL exit 0; restoring the membership test
is exit 1 at 4 failed; making the mixed arm return `applied` is exit 1 at 5 failed;
and deleting the TSX `partial` branch is exit 1 at 4 failed — which proves the
PYTHON contract test really reads the TypeScript, with no vitest anywhere. THE
REVIEWER ALSO RAN A MUTATION THE BLOCK NEVER ORDERED, to test the contract test's
own headline claim rather than take it on trust: adding a FIFTH backend label the
popover cannot render reddens `test_the_two_sets_agree_in_both_directions`, so the
seam guard really is derived from the fold's AST and not restated. THE SUITES were
re-run SERIALLY in the primary checkout, every REAL exit 0: the cockpit 39, the new
contract 13, `tests/ui_contracts/` 677 passed and 4 skipped, `test_command_channel.py`
106, `test_patch_cmd.py` 13 and the canary 42, with `ruff` exiting 0. THE
STRUCTURE: seven single-parent commits over the range ending at C5, of 400, 272,
17, 6, 2, 21 and 396 insertions, every one under 500; the path set EQUALS the
declared change set in BOTH directions; and ALL TWELVE do-not-touch paths
byte-identical by blob id.

## The worker's six deviations — all honest, and two are the reviewer's own errors

D1 is a DEFECT IN THE REVIEWER'S BLOCK and the worker was right to declare it. The
`ui_server.py` SPEC ordered the fold's WHY comment to QUOTE the membership test it
replaced, and the contract-test SPEC ordered an assertion that the membership test
is absent — a "must be absent" gate over a string the same block ordered written
into the file it reads, which is pre-emission checklist item 2's shape arriving
through a TEST rather than through a done-when. The worker's AST predicate is
strictly stronger than the ordered text search and mutation (i) proves it
discriminates. Recorded as a prose slip below.

D6 is the second. The block's bundle ended at C6, the handback commit, while the
push outcome can only exist after it; the worker added a C7 to record the real
outcome rather than commit a promise. Nothing on disk is wrong and the change set
was not exceeded — `.agent/handoff.md` is in it — but the block should have said
where the push outcome goes. Recorded as a prose slip below.

D2, D3, D4 and D5 are correct and need no action: the cockpit tests were added to
the existing class because its chain idiom is instance helpers; the control reads
39 because this round adds 6 to the 33 the block annotated AS A BASE reading; G8's
path comparison cannot see `.agent/handoff.md` from a range ending at C5, which is
checklist item 14's known shape; and no `Landed:` line was written because R-0738
is advanced rather than resolved, which is what the block ordered.

## Reviewer prose slips — for `.agent/prose_slips.md`, no id, no round of their own

2026-08-29 · F033 R16 · The block's `ui_server.py` SPEC ordered the fold's WHY
comment to QUOTE the membership test `if "applied" in apply_states` while its
contract-test SPEC ordered an assertion that no membership test remains, so a text
search would have been answered by the reviewer's own ordered comment — pre-emission
checklist item 2's shape reaching a TEST rather than a done-when; the worker
resolved it with an AST predicate that is strictly stronger, declared the
disagreement, and the reviewer's mutation (i) confirms the predicate discriminates.

2026-08-29 · F033 R16 · The block's bundle ended at C6, the handback commit, and
said nothing about where the PUSH outcome is recorded, so the worker added a C7 to
carry the real outcome instead of committing a promise; nothing on disk is wrong
and the change set was not exceeded, and a future block should name the commit the
push outcome lands in rather than leaving the worker to invent one.

## What this session built

| Path | What it decides | Tests |
|------|-----------------|-------|
| `packages/orchestration/evidence_index.py` | WHICH directory a job's diff is read out of — one rule for the viewer and both doors | 33 |
| `apps/cli/commands/patch.py` | the operator's CLI door: `remedy patch approve-hunks` | 13 |
| `apps/cli/command_catalog.py` | the command's catalog entry and its UI exposure | 18 |
| `packages/orchestration/ui_server.py` | the write door's dispatch, and the apply fold's partial truth | 12 + 39 |
| `apps/ui/src/components/detail/DetailPopover.tsx` | the partial state's operator label | 13 |

Findings R-0743 (Low) and R-0744 (Medium) were raised, repaired and resolved
within this session, each proved by a COLOUR CHANGE rather than by reading the
test. R-0745 (Low) was raised and is open. R-0738 (Medium) was ADVANCED and is
open. The open set is 258, exactly where this session opened, because two ids were
added and two resolved.

## Verification of THIS commit

The gates the closing block ordered: hygiene, transport, the handoff's byte
equality, the ledger's three files byte-identical, the canary, and the structure.

## Next expected action — SESSION 5, in this order

1. Read `.agent/STOP` from disk. If it exists, hand off and end (Phase 1 rule 1
   before rule 2 — finding R-0347).
2. Run the Open PR Gate. There was no open PR at the close of session 4, and this
   session created none: F033 is not closed, and §5 rules the PR into the closure
   sequence.
3. The next round's FIRST commits book, into `.agent/live_review.md`, the round 16
   verdict above, and append the two prose slips. Neither buys a round of its own.
4. Then the round's real work, which is the plan's step 2: THE TWO SURFACES R-0738
   STILL NAMES. THIS ROUND NEEDS ITS OWN GROUND-READING BUDGET, which is why
   session 4 ended here rather than starting it. Measured by the reviewer at
   `c7dc3cc0`: `applyStatus` is consumed by `DetailPopover.tsx` ALONE, so no node
   glyph reads apply state today at all; the task node's glyph is driven by
   `RemedyState` in `apps/ui/src/api/types.ts`, a CLOSED union of `done`,
   `current`, `pending`, `blocked` and `suggested` with no partial member, so a
   partial glyph means widening that union AND conforming to the design reference
   this feature file's banner makes binding, including `assets_spec.md` for any
   glyph treatment; and `packages/orchestration/run_report.py` holds NO reference
   to apply state whatsoever, so the report line is a new read rather than a
   changed one. Do not assume any of the three is a small edit.
5. Only AFTER R-0738 is resolvable on all three surfaces, T003's remaining half:
   rejection reasons quoted VERBATIM into the next repair prompt, with the trace
   proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
6. R-0745 is open and belongs with the next work that touches the door's imports;
   its FIX clause names two routes and recommends the transitive-closure test.
7. The closure sequence still owes `docs/` an operator-facing description of
   `remedy patch approve-hunks`. No round has been allowed a `docs/` path yet, and
   the plan carries it as an explicit item so it is not discovered at closure.
<<<END HANDOFFCLOSE4
