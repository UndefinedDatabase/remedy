# F033 — Hunk-level diff approval · ROUND 6 · OPENING T002

SESSION 2 of feature F033. Round 6, rounds so far 6.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R6`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the module and its tests from the
   description. Names, signatures, refusal codes, the refusal ORDER and the
   behaviours the SPEC fixes are binding; structure, comment wording and test
   names are yours. If the SPEC is impossible, STOP and say so rather than
   inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.

## Base

BASE is `cb49a3ea39659dbc270dfd36ea296171cf6dc439`, the round 5 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 5 passed every gate; the reviewer re-ran all eight itself, reproduced every
reading, and additionally proved the comment-only property by its own
canonicalisation with negative controls. T001 is closed. Its verdict, and the
resolution of R-0739, are in the record slice below.

Round 5's handback also inventoried the T002 seam, and the reviewer spot-checked
its load-bearing claims: the grep for any approved/rejected hunk vocabulary
matches ZERO files across `packages/`, `apps/` and `tests/`;
`apply_structured_patch` takes no subset of anything; and
`packages.orchestration.source_apply` is the FIRST entry of `FORBIDDEN_MODULES`
in `TestCommandDoorImportGuard`, so the write door may never import the applier.
T002 therefore cannot be one commit, and its first piece is the piece that needs
no door and no applier at all.

THIS ROUND BUILDS THAT PIECE: the pure decision core. Given the hunk ids an
attempt's diff really carries, and an operator's approved and rejected sets, it
either returns the decision — approved, rejected with reasons, and the pending
remainder — or it refuses with a named code and the offending ids. It touches no
file system, no door, no applier and no storage, and it is the thing every later
T002 commit validates against.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 5 verdict and `Done: R-0739` into `.agent/live_review.md`
- C3 the two reviewer prose slips into `.agent/prose_slips.md`
- C4 the decision core and its tests, together
- C5 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r6.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_approval.py
    tests/orchestration/test_hunk_approval.py
    .agent/handoff.md

The last two are NEW FILES. This round does NOT touch
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`packages/orchestration/source_apply.py`,
`packages/orchestration/hunk_identity.py`, `packages/orchestration/diff_parser.py`
or `docs/roadmap/STATUS.md`.

## SPEC — `packages/orchestration/hunk_approval.py`

A NEW module. `docs/roadmap/features/T5_F033.md` names
`tests/orchestration/test_hunk_approval.py` as this feature's suggested test
path, so the module takes the matching name per AGENTS.md's discoverability
convention (`test_x.py` ↔ `x.py`).

### 1. What it is, and what it deliberately is not

It decides ONE thing: whether an operator's approved and rejected hunk sets are a
coherent decision over the hunks an attempt's diff actually carries. It does NOT
apply anything, does not read a diff, does not know what a hunk's CONTENT is, and
does not touch the file system, a subprocess, the network, logging or any global
mutable state. Standard library only. A reader who arrives wanting the apply
mechanics wants `packages/orchestration/source_apply.py`; one who wants where a
hunk id COMES FROM wants `packages/orchestration/hunk_identity.py`. Write that
deliberate absence into the module docstring, in the idiom those two modules use.

Every public function is TOTAL: it NEVER raises, on any input at all, including a
non-iterable, `None`, a non-string id or an object whose `__str__` is broken.
Totality is not politeness — this runs while rendering an approval screen, and a
validator that throws on a strange id takes down the screen that exists to show
the operator what is strange. `hunk_identity.py` states the same rule and its
`_total_text` helper is the shape to follow.

### 2. The types

- `HunkRejection`, a frozen dataclass: `hunk_id: str`, `reason: str`.
- `HunkDecision`, a frozen dataclass: `approved: tuple[str, ...]`,
  `rejected: tuple[HunkRejection, ...]`, `pending: tuple[str, ...]`.
- `HunkApprovalRefusal`, a frozen dataclass: `code: str`, `message: str`,
  `hunk_ids: tuple[str, ...]` — the offending ids, and empty when none is.

`pending` is the ids the attempt carries that the operator decided NEITHER way,
IN THE ORDER THE KNOWN SET GAVE THEM. It is computed here rather than by a
caller because the feature's report line — "partially approved (5/8 hunks)" —
and T003's viewer badges both need it, and two derivations of one number drift.
An undecided hunk is a legitimate state, not an error: `docs/roadmap/features/T5_F033.md`
rules that new hunks in a later round render PENDING with no inherited decision.

### 3. The refusal codes, and the ORDER they are checked in

Module-level string constants, each with its own name, so a caller matches on a
name and never on a message: `REFUSAL_EMPTY_DECISION` (`"empty_decision"`),
`REFUSAL_DUPLICATE_HUNK` (`"duplicate_hunk"`), `REFUSAL_OVERLAPPING_SETS`
(`"overlapping_sets"`), `REFUSAL_UNKNOWN_HUNK` (`"unknown_hunk"`),
`REFUSAL_MISSING_REASON` (`"missing_reason"`).

They are checked in exactly that order and the FIRST one that trips is returned.
The order is part of the contract and a test pins it with an input that trips two
at once, because an unpinned order is one a later refactor changes silently.
Reason for this particular order: a decision that names nothing at all is not a
malformed decision but an absent one; a set that contradicts ITSELF is reported
before one that contradicts the DIFF; and a missing reason is last because it is
the only fault an operator repairs by typing rather than by re-selecting.

### 4. The entry point

    decide_hunk_approval(
        known_hunk_ids: Iterable[str],
        approved: Iterable[str],
        rejected: Iterable[HunkRejection | tuple[str, str] | Mapping[str, str]],
    ) -> HunkDecision | HunkApprovalRefusal

`rejected` accepts all three spellings because the wire form is a mapping
(`{"id": ..., "reason": ...}` — the feature file writes `rejected[{id, reason}]`),
the test form is a tuple and the internal form is the dataclass; normalise once,
here, so no caller has to. A rejection entry that is none of the three — a bare
string, `None` — is a `REFUSAL_MISSING_REASON` naming that entry's id as far as
one can be recovered, never an exception.

Rules, in the order of §3:
- EMPTY_DECISION when approved and rejected are both empty.
- DUPLICATE_HUNK when an id appears more than once WITHIN approved, or more than
  once WITHIN rejected.
- OVERLAPPING_SETS when an id appears in BOTH.
- UNKNOWN_HUNK when an id in either set is not in `known_hunk_ids`.
- MISSING_REASON when a rejection's reason is empty or only whitespace.

`hunk_ids` on the refusal carries every offending id, DEDUPLICATED and in first-
appearance order, so an operator sees all of them at once rather than one per
round-trip. `message` is one human sentence and is never parsed by anything.

On success: `approved` in the order given, `rejected` normalised to
`HunkRejection` in the order given with reasons kept VERBATIM — leading and
trailing whitespace included, because T003 quotes a rejection reason verbatim
into the next repair prompt and this is not the layer that reformats it — and
`pending` as §2 defines it.

An id is compared as text. Coerce with the same totality guard `hunk_identity.py`
uses, so a non-string id becomes text rather than an exception.

## SPEC — `tests/orchestration/test_hunk_approval.py`

A NEW file. Cover, at least: each of the five refusal codes on its own; the
ORDER, with one input that trips two codes and an assertion that the earlier one
is returned; a clean mixed decision with the right approved, rejected and pending
tuples; pending EMPTY when every known hunk is decided; a full-rejection round
with an empty approved set accepted as VALID, which the feature file's edge cases
require; a reason preserved VERBATIM including its surrounding whitespace; all
three `rejected` spellings producing the same decision; the offending-id list
DEDUPLICATED and in first-appearance order; and TOTALITY — `None`, a
non-iterable, a non-string id and an object whose `__str__` raises all return a
value rather than raising.

Name each test for the property it pins, not for the function it calls.

## The slices

<<<SLICE PLANF033R6
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 2 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5, DECISION F033 D3 |
| the approval decision core and its tests | done | this round |
| the all-or-nothing subset apply | open | next, on `source_apply.py` |
| the write-door command and its exposure | open | needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The subset apply: land ONLY the approved hunks, all-or-nothing, with a
   conflict inside the approved set falling back to nothing-applied and naming
   the hunk. Built on `packages/orchestration/source_apply.py`, whose
   `apply_structured_patch` takes no subset today.
2. Then the write door: `approve_hunks` reaches the applier through a service
   seam, never by importing it — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`.
3. Then the hunk-decision ledger in evidence, which T003's report line reads.

## Risks
- The door's import guard is an EQUALITY guard, so any new import is widened in
  the SAME commit that adds it, or the branch tip ships red.
- `packages/orchestration/repo_applicator.py` applies nothing by design, so the
  subset seam is new work rather than a parameter on something existing.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R6

<<<SLICE RECORDF033R6
Gate: F033 R5 — CLOSING T001. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `cb49a3ea` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 27281 bytes at sha256 `02e77e6f…c809b6` and matches the reviewer's own pre-emission original byte for byte, which is the one round in this feature where that comparison was available rather than inferred; the C0b `.agent/last_block.md` blob is identical to it. THE RECORD APPEND at `935c3cf7` reconstructs 1446287 plus one newline plus 8354 to 1454642, the committed blob exactly, base a byte PREFIX, N counted at 3, the last three blank-line units equal to the slice's paragraphs IN ORDER, and a byte flipped at offset 1446488 — inside the FIRST appended paragraph, which spans 1446288 to 1449890 — rejected by BOTH readers. THE SECOND APPEND at `8c594ef1` keeps C2 as a byte prefix and adds exactly one content line matching `^Landed: R-0739 — `. THE LEDGER moved exactly where the block allowed: registered 299 to 300 with the ADDED id exactly `R-0739`, `Done:` 44 over 42 UNMOVED, `Landed:` 11 to 12, `Gate:` 121 to 122, the open set 257 to 258, and `^Gate: F033 R4 — ` 0 at the base and 1 after. THE STALENESS REPAIR: all six ordered needles read 1 at the base and 0 at C3, and both survivors read 1. THE COMMENT-ONLY PROPERTY WAS PROVED BY THE REVIEWER INDEPENDENTLY, not accepted from the handback: the docstring-blanked `ast.dump` of `packages/orchestration/hunk_identity.py` is EQUAL across the change with a `HUNK_ID_LENGTH` 16-to-17 control REJECTED, and `apps/ui/src/api/diffViewModel.ts` stripped through the repository's own `strip_ts_comments` is equal at 13233 characters both sides with an overscan 8-to-9 control REJECTED. THE FEATURE-FILE APPEND at `d1faf70e` is 5057 plus 1301 equals 6358 byte for byte, base a prefix, `^## Amendments$` exactly 1. THE PLAN landed byte-EQUAL at 40 lines. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: `tests/orchestration/test_hunk_identity.py` 10, `tests/orchestration/test_diff_parser.py` 50, `tests/ui_contracts/` 664 passed with 4 skipped, `tests/docs/` 295, the canary `tests/cli/test_golden_path.py` 42, `npx tsc --noEmit` 0 and vitest 95. NO MUTATION RED-PROOF WAS ORDERED OR RUN, and that is correct rather than a gap: C3 changed comment text only, so no mutated branch is reachable by any test and a colour ordered here could only have come back green. THE STRUCTURE: seven single-parent commits of 340, 259, 16, 6, 23, 23 and 2 insertions, all under 500, the path set matching the change set in BOTH directions with `.agent/handoff.md` the sole expected absence, residue 0 in every target against a control of 5 and 6, `git ls-files .remedy-wt` 0, and `diff_parser.py`, `diff_repair.py`, `diffViewModel.test.ts` and `docs/roadmap/STATUS.md` all byte-identical across the round. THE WORKER DECLARED TWO DEFECTS IN THE REVIEWER'S OWN BLOCK AND WAS RIGHT ABOUT BOTH; neither damaged anything on disk, so under operator amendment amend0827 rule 2 they spend no id and buy no correction round, and they are the two dated lines this round's C3 puts in `.agent/prose_slips.md`.

Done: R-0739 — RESOLVED at `d96988c8`, verified by the reviewer reading both files as a diff and then proving the property mechanically rather than by eye. The four false claims in `packages/orchestration/hunk_identity.py` and the two in `apps/ui/src/api/diffViewModel.ts` all read 1 at `7434f546` and 0 after, while the two sentences that had to SURVIVE — `Nothing here depends on the id's SHAPE` in the client and `DELIBERATE ABSENCE` in the module — each still read exactly 1. The replacement text is TRUE where the old text was false, and the reviewer checked each claim against the thing it describes rather than against the block: `diff_parser.py` really does call `hunk_identity` for every hunk id it emits, its docstring really does now say those ids "are CONTENT-DERIVED and carry no position at all", `DIFF_VIEW_VERSION` really is 2, and `RepairHunk` really does select spans of current source and name no hunk. NOTHING EXECUTABLE MOVED: the docstring-blanked AST of the Python module is equal across the change and its negative control is rejected, and the comment-stripped TypeScript is equal at 13233 characters with its own control rejected — so the repair is provably confined to prose, which is also why no suite could ever have caught the original defect. The finding's FIX clause asked for the wiring stated in the present tense with each comment's WHY intact, and both survive: the module still opens on why a positional name cannot keep an approval's promise, and the client still says nothing there depends on the id's shape. The BINDING clause R-0739 carried forward — that a block landing a seam change must NAME the files whose comments assert the fact the change falsifies, and grep for the CLAIM rather than read the diff — is not discharged by this resolution and binds the next such block.
<<<END RECORDF033R6

<<<SLICE SLIPSF033R6

2026-08-29 · F033 R5 · The block's G3(c) ordered "the C2 blob plus one newline plus the Landed line, byte for byte" and "that commit's diff must ADD exactly one line" in the same gate, and the two cannot both hold, because the C2 blob already ends in a newline so the byte formula necessarily adds a blank separator and git reports two insertions; the worker followed the byte formula, matched the eleven pre-existing blank-separated `Landed:` lines, and declared the contradiction.

2026-08-29 · F033 R5 · The block's G5 ordered "zero changed lines that are not inside a comment or docstring" over `git diff BASE C3`, a range that also contains four `.agent/**` state files from C0a through C2, so the clause was unmeetable as written over the range it named; the worker proved the property over the two production files it was plainly meant for and reported the range's other paths openly.
<<<END SLIPSF033R6

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C4, so the handback at C5 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C5,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r6.md` and of `.remedy-wt/f033-r6-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r6.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1456716 bytes, plus one newline plus RECORDF033R6 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R6 — report it
  — and compare the LAST N blank-line units of the C2 blob against the slice's
  paragraphs IN ORDER. NEGATIVE CONTROL at an offset your script PROVES lies
  inside the FIRST appended paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. Ordered: registered 300
  UNMOVED — this round registers NOTHING — `Done:` 44 to 45 over 42 to 43 with
  the ADDED resolved id exactly `R-0739`, `Landed:` 12 UNMOVED, `Gate:` 122 to
  123, and the open set 258 to 257. `^Gate: F033 R5 — ` at C2 must read exactly
  1. The `Landed: R-0739` line STAYS: this record is append-only and a `Done:`
  paragraph sits beside its `Landed:` line rather than replacing it — measured at
  BASE, where 8 of the 9 distinct `Landed:` ids also carry a `Done:`.
- **G5 THE PROSE-SLIPS APPEND at C3.** The BASE blob of `.agent/prose_slips.md`,
  which must be 18681 bytes, plus SLIPSF033R6 equals the C3 blob byte for byte —
  the slice OPENS with a blank line, so no separator is added. BASE a byte
  PREFIX; result ending in exactly one newline; the lines that commit's diff ADDS
  are exactly the slice's lines IN ORDER. Report `^2026-08-29 · F033 R5 · ` at C3
  as exactly 2.
- **G6 THE MODULE AGAINST THE SPEC at C4.** Each as a measurement, over
  `packages/orchestration/hunk_approval.py`. (a) `ruff check` over both new files
  exits 0 — report its own summary line. (b) By AST, not by grep: the module's
  import statements name ONLY standard-library modules; report the full list you
  extracted. (c) The five refusal constants are module-level assignments and
  their values are exactly `empty_decision`, `duplicate_hunk`,
  `overlapping_sets`, `unknown_hunk`, `missing_reason`; report each name with its
  value. (d) TOTALITY, run as a real probe rather than asserted: call
  `decide_hunk_approval` with each of `None`, `object()`, an integer id, and an
  object whose `__str__` raises, in both the `approved` and the `rejected`
  position, and report that every call RETURNED and what type came back. (e) the
  module contains no `open(`, no `import os`, no `import subprocess`, no
  `import logging` and no `Path` — report each count as 0.
- **G7 THE MUTATION RED-PROOFS at C4.** In a DISPOSABLE `git worktree` at C4,
  never in the primary checkout, with `python3 -B` so no stale bytecode masks a
  mutation. FIRST the UNMUTATED CONTROL: `python3 -B -m pytest
  tests/orchestration/test_hunk_approval.py -q` must be a REAL exit 0 — report
  the count. Then, one at a time, reverting fully between each, assert the anchor
  is UNIQUE in the file before replacing it, and report the REAL exit code, the
  failure count and the NAME of each failing test:
  (i) make the OVERLAPPING_SETS check never trip;
  (ii) accept a whitespace-only rejection reason as a reason;
  (iii) make the UNKNOWN_HUNK check never trip.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red — a green mutation is a real finding about the
  tests and the reviewer wants it. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_hunk_approval.py` (new
  this round — report the count), `tests/orchestration/test_hunk_identity.py` (10
  at BASE), `tests/orchestration/test_diff_parser.py` (50 at BASE),
  `tests/regression/test_resource_safety.py`, `tests/test_no_interactive_guard.py`
  and the canary `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C4`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C5's own numbers are NOT ordered
  here; the reviewer measures C5 at the next gate. Report the range's path set
  against the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_approval.py` and
  `tests/orchestration/test_hunk_approval.py`: each 0, against
  `.agent/authored/f033-r6.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 2,
round 6, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts — one line
per gate with real numbers, the item-status table with every ordered item exactly
once, and your deviations. Quote `decide_hunk_approval`'s final signature and
list the test names you wrote with the property each pins. No length cap. Write
no verdict on your own work.
