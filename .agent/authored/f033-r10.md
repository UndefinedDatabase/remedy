# F033 — Hunk-level diff approval · ROUND 10 · THE HUNK-DECISION LEDGER

SESSION 3 of feature F033. Round 10, rounds so far 10.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R10`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the code and the tests from the
   description. Names, signatures and the behaviours the SPEC fixes are binding;
   structure, comment wording and test names are yours. If the SPEC is
   impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.

## Base

BASE is `cee20b37`, the round 9 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs.

## Why this round exists

Round 9 PASSED. The reviewer re-executed all eight gates at `cee20b37` from
scripts of its own and reproduced every ordered reading, then ran two probes and
one mutation the block never ordered. That verdict, the resolution of R-0740 and
one new finding are booked by C2; none of them buys a round of its own.

YOU FOUND SOMETHING THE BLOCK GOT WRONG AND YOU WERE RIGHT ABOUT BOTH HALVES OF
IT. The R9 block's leave-alone clause named "`hunk_apply.py`'s `_blocked_ids`
docstring" for the hit at line 82 of the base file; that hit is in
`HunkApplyOutcome`'s docstring, and `_blocked_ids` carries none of the five
grepped strings. And calling it "about a DIFFERENT property" does not hold: it
asserts the same absolute the round retired. You followed the SPEC and left it,
which is the required behaviour. It is R-0741 below and C4 repairs it.

THIS ROUND'S REAL WORK IS THE LEDGER. Rounds 6 through 9 decide whether a
selection is coherent, which bytes it means, how it lands and how a failure to
land is told truthfully. What none of them produces is the RECORD of what the
operator decided and what became of it — the thing
`docs/roadmap/features/T5_F033.md` calls "the ledger of hunk decisions in
evidence" and the thing T003's viewer badges, node glyph and report line all
read. It lands as a pure module, the fourth of this feature's siblings.

TWO AXES, NOT ONE, AND THAT IS THE WHOLE POINT. A hunk carries a DECISION —
approved, rejected or pending — and separately a LANDING — did those bytes reach
the branch. They come apart in exactly the state this feature exists to render
honestly: an approved hunk whose apply failed is still APPROVED and did NOT
land, and collapsing the two would make a failed apply indistinguishable from a
rejection. The reviewer read `hunk_approval.HunkDecision` and
`hunk_apply.HunkApplyOutcome` at `cee20b37` and neither carries the pair.

THE ORDER PROBLEM, read at `cee20b37`: `HunkDecision` gives `approved` in the
order the operator gave, `rejected` in the order the operator gave and `pending`
in the known set's order, and it does NOT carry the attempt's full hunk list. A
viewer renders hunks in the DIFF's order, and "5 of 8" needs the 8. So the
builder takes `known_hunk_ids` as its first argument rather than recovering an
order it was never given.

WHY THE LEDGER MAY NOT IMPORT `hunk_apply`: that module imports
`packages.orchestration.source_apply`, the first entry of `FORBIDDEN_MODULES` in
`tests/ui_server/test_command_channel.py`. The ledger is what the write door will
write, so it must be importable from anywhere without dragging the applier
behind it. It therefore takes PLAIN VALUES — a bool and a list of ids — where a
`HunkApplyOutcome` would have been the obvious argument. That is a deliberate
absence and G6 measures it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 9 verdict, the R-0740 resolution and the R-0741 registration
- C3 one dated line into `.agent/prose_slips.md`
- C4 the R-0741 repair in `packages/orchestration/hunk_apply.py`
- C5 the ledger module
- C6 its tests
- C7 the `Landed: R-0741` line into `.agent/live_review.md`
- C8 the handback

C5 and C6 are SEPARATE COMMITS for the reason round 8 gave and round 9 confirmed:
a module and the suite that pins it are two logical steps, and this feature's test
files have twice landed near the 500-insertion cap on their own. You write NO
`Done:` paragraph — `Done:` is the reviewer's word.

## Change set — these paths and nothing else

    .agent/authored/f033-r10.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_apply.py
    packages/orchestration/hunk_ledger.py
    tests/orchestration/test_hunk_ledger.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r10.md`,
`packages/orchestration/hunk_ledger.py` and
`tests/orchestration/test_hunk_ledger.py`. This round does NOT touch
`packages/orchestration/source_apply.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/hunk_identity.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`tests/ui_server/test_command_channel.py`,
`tests/orchestration/test_hunk_apply.py` or `docs/roadmap/STATUS.md`.
`.agent/context.md` is deliberately NOT touched: branch, scope and constraints
are unchanged.

## SPEC — the R-0741 repair in `packages/orchestration/hunk_apply.py`

COMMENT TEXT ONLY. `HunkApplyOutcome`'s docstring opens with

    ``landed`` is EMPTY whenever ``applied`` is false — a caller must not have to check two
    fields to learn that nothing landed, because there is no partial landing to distinguish it
    from.

The first clause is TRUE and stays. The reason is what is false, for the reason
the module docstring already states after round 9: when the applier's own
rollback does not finish there IS a partial state on disk. Give this sentence
the same real reason its neighbour now has — this module learns WHICH hunks
landed only from a SUCCESSFUL apply, so on failure it has no per-hunk answer to
give — and point at `_failure_lead_sentence` as where a partial state IS
reported. Every other sentence of that docstring is untouched, and NO EXECUTABLE
LINE CHANGES anywhere in the file: G6(a) proves that by AST.

## SPEC — `packages/orchestration/hunk_ledger.py`

A NEW module, the fourth pure sibling. Follow the idiom of
`packages/orchestration/hunk_approval.py` and
`packages/orchestration/decision_evidence.py`: a `Public API::` block closing the
module docstring, module-level constants with `#:` comments, frozen dataclasses,
and a DELIBERATE ABSENCE paragraph naming where a reader should go instead.

### 1. What it is and what it deliberately is not

It turns one decision plus what became of it into the durable, ordered record of
every hunk in an attempt. It decides nothing, applies nothing, reads no diff,
opens no path, runs no subprocess and keeps no state. It imports the STANDARD
LIBRARY and `packages.orchestration.hunk_approval` and NOTHING ELSE — in
particular NOT `hunk_apply`, for the reason stated above, which belongs in the
docstring as a deliberate absence a reader can act on.

It is TOTAL: every public name NEVER raises, on any input at all. Restate
`hunk_approval`'s `_total_text` guard rather than importing it — that name is
private there and this module follows the same rule its siblings do.

### 2. The vocabularies

Two closed sets, each constant carrying its own `#:` comment:

- DECISION: `HUNK_STATE_APPROVED` = `"approved"`, `HUNK_STATE_REJECTED` =
  `"rejected"`, `HUNK_STATE_PENDING` = `"pending"`. These are the viewer's three
  badges, named in the feature file's Partial-state-truth bullet.
- LANDING: `HUNK_LANDING_LANDED` = `"landed"`, `HUNK_LANDING_NOT_LANDED` =
  `"not_landed"`, `HUNK_LANDING_UNATTEMPTED` = `"unattempted"`. `unattempted`
  is NOT a synonym for `not_landed` and the distinction is load-bearing: it
  separates "we tried and it did not land" from "no apply has run", which is what
  a viewer must not conflate before the operator has pressed anything.

### 3. The types

    @dataclass(frozen=True)
    class HunkLedgerEntry:
        hunk_id: str
        state: str      # one of the three HUNK_STATE_* values
        reason: str     # the operator's reason, VERBATIM; "" unless rejected
        landing: str    # one of the three HUNK_LANDING_* values

    @dataclass(frozen=True)
    class HunkDecisionLedger:
        entries: tuple[HunkLedgerEntry, ...]

`HunkDecisionLedger` deliberately holds NO counts. "5 of 8" is derived from
`entries` by whoever renders it, because two derivations of one number drift
apart — the same reason `HunkDecision.pending` is computed once in
`hunk_approval` rather than by each caller. Say so in the docstring.

### 4. The entry point

    build_hunk_ledger(
        known_hunk_ids: Iterable[str],
        decision: HunkDecision,
        *,
        applied: bool = False,
        landed_hunk_ids: Iterable[str] = (),
        apply_attempted: bool = False,
    ) -> HunkDecisionLedger

Rules, and each is a test:

1. ONE ENTRY PER KNOWN HUNK, in `known_hunk_ids` order, repeats removed keeping
   FIRST-appearance order. Ids are compared AS TEXT, exactly as
   `hunk_approval` compares them.
2. STATE: `approved` if the id is in `decision.approved`; `rejected` if it is
   among `decision.rejected`'s `hunk_id` values; otherwise `pending`. An id in
   BOTH cannot occur — `decide_hunk_approval` refuses that decision before it
   can be built — but check approved FIRST anyway and say in a comment why the
   order is stated rather than left to chance.
3. REASON: the matching rejection's `reason`, VERBATIM including surrounding
   whitespace, for a rejected hunk; the empty string for every other state. This
   is what T003 quotes into the next repair prompt, so it is not reformatted
   here.
4. LANDING, and this is the rule the round turns on:
   - `apply_attempted` false → EVERY entry is `unattempted`, whatever the other
     arguments say.
   - `apply_attempted` true and `applied` FALSE → every entry is `not_landed`
     for an approved hunk and `unattempted` for a rejected or pending one, and
     `landed_hunk_ids` IS IGNORED ENTIRELY. A caller that passes ids alongside
     `applied=False` is contradicting `HunkApplyOutcome`'s own contract, and this
     module refuses to mint a landing from it rather than trusting the caller.
     Write that as a deliberate refusal in a comment.
   - `apply_attempted` true and `applied` TRUE → an approved hunk is `landed`
     when its id is in `landed_hunk_ids` and `not_landed` otherwise; a rejected
     or pending hunk is `unattempted`, because it was never submitted.
5. A hunk id that `decision` names but `known_hunk_ids` does not is DROPPED, not
   appended: the ledger is the record of THIS ATTEMPT's hunks, and an id outside
   it has no row to render. `decide_hunk_approval` already refuses such a
   decision, so this is a guard rather than a path; say so.

    export_hunk_ledger(ledger: HunkDecisionLedger) -> dict

A JSON-safe dict, plain `str` and `list` throughout, one object per entry with
keys `id`, `state`, `reason` and `landing`, under a single top-level key
`hunks`. It adds nothing the entries do not already hold.

## SPEC — `tests/orchestration/test_hunk_ledger.py`

A NEW file. One test per PROPERTY, named for the property, in the style
`tests/orchestration/test_hunk_approval.py` uses. Build decisions by calling
`decide_hunk_approval` rather than by constructing `HunkDecision` by hand
wherever the case allows it, so the suite pins the two modules AGREEING rather
than the ledger's reading of a shape nothing produces.

Cover at least: the diff's order is the ledger's order — approve and reject in a
DIFFERENT order from `known_hunk_ids`, or the test cannot tell the two apart and
G7's mutation (iii) has nothing to bite on — and a repeated known id appears
once; each of the three states lands on the right hunk; a rejection's
reason arrives verbatim with its whitespace and every other reason is empty;
each of the three landing values in the case that produces it; the
`applied=False` refusal to honour `landed_hunk_ids`; the `apply_attempted=False`
override; a decision id outside `known_hunk_ids` dropped; `export_hunk_ledger`
round-tripping the entries with the four keys and nothing else; and TOTALITY —
`build_hunk_ledger` called with `None`, a non-iterable, a non-string id and an
object whose `__str__` raises, none of which may raise and each of which must
return a `HunkDecisionLedger`.

## The slices

<<<SLICE PLANF033R10
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 3 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5, DECISION F033 D3 |
| the approval decision core | done | round 6, 30 cases |
| the approved subset diff | done | round 7, 17 cases |
| landing the subset all-or-nothing | done | round 8 |
| the seam tells the truth about a failed rollback | done | round 9, R-0740 |
| the hunk-decision ledger | open | this round, plus R-0741 |
| the write-door command and its exposure | open | needs the door's effect ruled |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The hunk-decision ledger: the ordered record of every hunk in an attempt on
   TWO axes — the operator's decision and whether those bytes landed — kept
   apart because an approved hunk whose apply failed is neither landed nor
   rejected. Pure, and deliberately unable to import the applier. R-0741 repairs
   the last comment still asserting the absolute round 9 retired.
2. Then the write door, opened by a DECISION that first rules what its effect IS.
   `packages.orchestration.hunk_apply` imports `source_apply`, the first entry of
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`, so a door
   importing the seam runs the applicator inside the HTTP handler and defeats the
   P3 contract by naming a module the list has not caught up to. The ledger is
   built to be what the door writes instead.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report's "partially approved (5/8 hunks)" line derived from the ledger, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- `UI_EXPOSED_COMMANDS` is pinned at exactly two ids by `TestUiExposedCommands`,
  and exposure without dispatch answers 501.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R10

<<<SLICE RECORDF033R10
Gate: F033 R9 — THE FAILED-ROLLBACK TRUTH. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `cee20b37` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 29545 bytes at sha256 `fd870c48…3796f01f` and is BYTE-IDENTICAL to the reviewer's own pre-emission original, which existed before this worker did — so the reading covers delivery and not merely the worker's self-consistency, which is the distinction R-0705 exists to force — and the C0b `.agent/authored/f033-r9.md` and `.agent/last_block.md` blobs are ONE blob id `eec2e4bc`. THE RECORD APPEND at `488149d2` reconstructs 1471135 plus one newline plus 5939 to 1477075, the committed blob exactly, base a byte PREFIX, the file ending in one newline, N COUNTED at 2 by the reviewer's own script, and the LAST TWO blank-line units equal to the slice's paragraphs IN ORDER; the reviewer placed TWO negative controls INSIDE the FIRST appended paragraph — whose span it computed at 1471136 to 1474163 — at offsets 1472656 and 1471139, and BOTH readers rejected BOTH. THE LEDGER moved exactly where the block allowed: registered 300 to 301 at C2 with the ADDED id exactly `R-0740` and UNMOVED at C6, `Done:` 45 lines over 43 distinct UNMOVED throughout with NO worker-authored resolution anywhere, `Landed:` 12 to 12 to 13 with the added id exactly `R-0740`, `Gate:` 125 to 126 with `^Gate: F033 R8 — ` exactly 1, and the open set 257 to 258 to 258, with the C2 blob a byte PREFIX of the C6 blob. THE PROSE FILES landed byte-exactly: `.agent/plan.md` at 2442 bytes over 45 lines, under the 50-line cap, EQUAL to its slice; `.agent/prose_slips.md` reconstructs 19985 plus one newline plus 775 to 20761 with the base a prefix. THE MODULE AGAINST THE SPEC: `ruff check` exits 0 at "All checks passed!"; the AST import set is UNCHANGED at 12 entries with NOTHING added and none of `permissions`, `approval_queue` or `repository_snapshot` present; the module-level string constants are still exactly `subset_refused`, `conflict` and `nothing_to_apply` with no fourth minted; and both the signature of `apply_approved_hunks` and the field list of `HunkApplyOutcome` are unchanged. THE SENTENCE WAS MEASURED BY CALLING IT, never by counting bytes: the false branch is byte-identical to the literal the base module hard-codes, trailing space included; both rollback prefixes select a different sentence carrying no occurrence of the retired claim. THE REVIEWER THEN RAN TWO PROBES THE BLOCK NEVER ORDERED — a plain `g.txt: diff hunks did not apply cleanly` error, which correctly KEEPS the old sentence, and a near-miss `rollback_incompleteXYZ`, which also keeps it — so the comment's claim that the trailing space is load-bearing is measured rather than asserted. THE MUTATIONS WERE REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `cee20b37`, the import first proved to resolve to the worktree's own copy, each anchor asserted UNIQUE before replacement and fully reverted after: the UNMUTATED CONTROL is a real exit 0 at 11 passed, forcing the predicate False is exit 1 at 1 failed naming exactly `test_a_rollback_that_could_not_run_is_not_reported_as_an_unchanged_repository`, and forcing it True is exit 1 at 2 failed naming exactly the two discriminators — so each mutation reddens precisely the tests that name its property and no other. THE REVIEWER THEN RAN TWO MUTATIONS THE BLOCK NEVER ORDERED: restoring the fixed sentence at the call site went RED at 1 failed on the same test, and DROPPING THE LOAD-BEARING TRAILING SPACE from the prefix tuple came back GREEN at 11 passed. That green is reported rather than repaired: the applier only ever emits `rollback_incomplete (N file(s)): `, so the space guards a string no producer in this repository writes, which makes it a defensive guard of the same class as the unreachable third limb recorded at the R7 gate — not a defect, and not worth a test that would pin a hypothetical. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, one pytest process at a time, every REAL exit 0: `test_hunk_apply.py` 11 against 8 at the base, `test_source_apply.py` 34, `test_hunk_subset_diff.py` 17, `test_hunk_approval.py` 30, `test_resource_safety.py` 21 and the canary `test_golden_path.py` 42. THE STRUCTURE: eight single-parent commits over BASE..C6 of 391, 275, 18, 4, 4, 59, 81 and 2 insertions, every one under 500, with the handback commit a further 2 insertions short of the cap at 351; the range's path set EQUALS the declared change set in BOTH directions with nothing touched that the block did not name; delimiter residue 0 in all four targets against a 5 and 6 control in the saved block; `git ls-files .remedy-wt` 0; the worktree list holding only the primary checkout; and all eight do-not-touch paths byte-identical across the round by blob id. THE WORKER FOUND A DEFECT IN THE REVIEWER'S OWN GREP AND WAS RIGHT ON BOTH HALVES OF IT, which is R-0741 below.

Done: R-0740 — RESOLVED at `de17f054` and pinned at `da551b48`, verified by the reviewer reading the diff and then measuring the property rather than accepting it. The failure message's leading sentence is now DERIVED: `_failure_lead_sentence` returns the retired absolute only when `_rollback_did_not_finish` reads no rollback vocabulary in the applier's errors, and otherwise a sentence saying the rollback did not finish and the repository may still hold part of the change. The reviewer called both functions directly at `cee20b37`: the false branch is byte-identical to the literal the base module hard-coded, trailing space included, so the correct case is unweakened; `rollback_failed:snapshot_not_found` and `rollback_incomplete (1 file(s)): a.txt` each select the other sentence, which carries no occurrence of the retired claim; and a plain `g.txt: diff hunks did not apply cleanly` correctly keeps the old one, which is the discrimination the finding's FIX clause asked for. THE FIX HOLDS ITS SHAPE: `code` is still `HUNK_APPLY_CONFLICT` with no fourth constant minted, the AST import set is unchanged at 12 entries, and the signature and field list are untouched — so no existing caller's match became incomplete, which is what the finding ruled it must not. THE TESTS PIN IT RATHER THAN DESCRIBING IT: `test_a_rollback_that_could_not_run_is_not_reported_as_an_unchanged_repository` asserts the message AND the disk, requiring `f.txt`'s digest to have MOVED and `g.txt`'s to have held, so it would fail if the sentence were true and the tree were not; and the two discriminators fail under a predicate that simply cries partial state for every failure, which the reviewer confirmed by forcing the predicate True and watching exactly those two go red. The finding's Acceptance link is discharged: a half-rolled-back worktree is now the one partial state this seam renders truthfully. WHAT THIS RESOLUTION DOES NOT COVER: the same absolute is still asserted in `HunkApplyOutcome`'s own docstring, which the block's leave-alone clause protected; that is R-0741 and not a reopening of this one, because R-0740 is about the MESSAGE an operator reads and R-0741 about a comment a maintainer reads.

- R-0741 — Low, THE LAST COMMENT STILL ASSERTING THE ABSOLUTE ROUND 9 RETIRED SURVIVED BECAUSE THE BLOCK'S OWN GREP MISNAMED IT. Raised by the WORKER as R9's declared deviation, confirmed by the reviewer at `cee20b37` by re-running the grep itself and reading the file. THE STATE ON DISK at `cee20b37`: `HunkApplyOutcome`'s docstring in `packages/orchestration/hunk_apply.py` reads "``landed`` is EMPTY whenever ``applied`` is false — a caller must not have to check two fields to learn that nothing landed, because there is no partial landing to distinguish it from". The first clause is true. The REASON is the same absolute R-0740 retired: when the applier's own rollback does not finish there IS a partial landing on disk, which is exactly why the module docstring's equivalent sentence was rewritten one paragraph earlier in the same round. HOW IT SURVIVED, and this is the part worth keeping: the R9 block ordered a grep for the CLAIM, ran it, and then MISNAMED one of its own hits — it attributed the line to "`_blocked_ids`'s docstring", which carries none of the five grepped strings, and it filed the hit under "about a DIFFERENT property", which is true of the `hunk_subset_diff.py` hit beside it and false of this one. The SPEC's "everything not named stays byte-identical" then made the mistake binding, and the worker correctly applied the SPEC and declared the disagreement rather than widening its own change set. WHY LOW: no behaviour is wrong, no test can see it, and the message an operator reads is already correct. It is not lower because this is the docstring of the type every caller of the seam reads to learn what `landed` means, and it currently gives a reason that the module docstring three screens above it explicitly contradicts — a reader who trusts it will conclude no partial state can exist. FIX: give the sentence the real reason its neighbour now carries — this module learns WHICH hunks landed only from a successful apply, so on failure it has no per-hunk answer — and point at `_failure_lead_sentence` as where a partial state IS reported. COMMENT TEXT ONLY; no executable line may move. BINDING ON THE NEXT BLOCK THAT ORDERS A GREP-DERIVED LEAVE-ALONE SET: name each hit by FILE AND LINE and by the SYMBOL that encloses it, resolved at the base SHA, and state per hit why it is left alone — a hit filed under a wrong symbol is a hit nobody re-reads.
<<<END RECORDF033R10

<<<SLICE SLIPSF033R10
2026-08-29 · F033 R9 · The block's transport gate G2 ordered the sha256 of the C0a blob against the reviewer's scratch original and both readings reproduced, but the reviewer's own first re-derivation of the record append was short by one byte because its slice extractor consumed the newline ending the last content line; the committed append was correct all along and the corrected extractor reproduced 1471135 plus one newline plus 5939 exactly.
<<<END SLIPSF033R10

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C7, so the handback at C8 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C8,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r10.md` and of `.remedy-wt/f033-r10-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r10.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1481910 bytes, plus one newline plus RECORDF033R10 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  Take the slice as the bytes from the end of the `<<<SLICE` marker line up to
  and INCLUDING the newline that ends its last content line. (b) let N be the
  paragraph count your script COUNTS in RECORDF033R10 — report it — and compare
  the LAST N blank-line units of the C2 blob against the slice's paragraphs IN
  ORDER. NEGATIVE CONTROL at an offset your script PROVES lies inside the FIRST
  appended paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2 and C7.** At BASE, at C2 and at C7 count `^- R-\d+ — `
  with distinct ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  and `^Gate: F\d+ R\d+ — `; report the open set at all three. Ordered:
  registered 301 to 302 at C2 with the ADDED id exactly `R-0741`, UNMOVED at C7;
  `Done:` 45 to 46 lines and 43 to 44 distinct at C2 with the ADDED resolved id
  exactly `R-0740`, UNMOVED at C7 — you author no `Done:` paragraph of your own;
  `Landed:` 13 UNMOVED at C2 and 13 to 14 at C7, the added line matching
  `^Landed: R-0741 — `, with the existing `Landed: R-0740` line still present
  beside its new `Done:` paragraph as this append-only record requires; `Gate:`
  126 to 127 at C2 with `^Gate: F033 R9 — ` exactly 1, UNMOVED at C7; the open
  set 258 UNMOVED at C2 — one registered and one resolved in the same commit —
  and UNMOVED at C7. C7 additionally keeps the C2 blob as a byte PREFIX.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R10 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  20761 bytes, plus one newline plus SLIPSF033R10, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching `^2026-\d\d-\d\d · F033 R9 · `
  at BASE and at C3, and the count of lines beginning `- R-` in the whole file at
  C3, which must be 0.
- **G6 THE CODE AGAINST THE SPEC.** (a) THE R-0741 REPAIR AT C4 IS COMMENT ONLY,
  proved by AST rather than by reading: parse `packages/orchestration/hunk_apply.py`
  at BASE and at C4, blank EVERY docstring in both trees, and report that
  `ast.dump` of the two is EQUAL — with a NEGATIVE CONTROL that changes one
  executable literal in the C4 tree and is REJECTED, because an equality that
  cannot fail proves nothing. Report also that the retired reason is gone and the
  surviving first clause is still present. (b) THE LEDGER MODULE AT C5: `ruff
  check` over it and its test file exits 0 — report the summary line. (c) By AST,
  report the module's FULL import list; every entry must be either standard
  library or `packages.orchestration.hunk_approval`, and `hunk_apply`,
  `source_apply`, `hunk_subset_diff` and `diff_parser` must each be ABSENT.
  Report also the counts of `open(`, `import os`, `import subprocess`,
  `import logging` and `Path` in its text: each 0. (d) Report each of the six
  vocabulary constants with its value, which must be exactly `approved`,
  `rejected`, `pending`, `landed`, `not_landed` and `unattempted`. (e) Report the
  extracted signature of `build_hunk_ledger` and the field lists of
  `HunkLedgerEntry` and `HunkDecisionLedger`, matching §3 and §4.
- **G7 TOTALITY AND THE MUTATION RED-PROOFS at C6.** First, in the primary
  checkout, exercise the SHIPPED function directly rather than through the
  tests: call `build_hunk_ledger` with `None` as `known_hunk_ids`, with a
  non-iterable, with a non-string id, with `decision=None`, and with an object
  whose `__str__` raises; report for EACH the `type()` of what came back, and
  report that NONE raised. Then, in a DISPOSABLE `git worktree` at C6, never in
  the primary checkout, with `python3 -B`, having first proved the import
  resolves to the WORKTREE's copy: the UNMUTATED CONTROL — REAL exit 0, report
  the count. Then, one at a time, reverting fully between each, asserting the
  anchor is UNIQUE in the worktree's own `packages/orchestration/hunk_ledger.py`
  before replacing it, and reporting the REAL exit code, the failure count and
  the NAME of each failing test:
  (i) honour `landed_hunk_ids` even when `applied` is False;
  (ii) ignore `apply_attempted` and treat it as always True;
  (iii) emit entries in the decision's order instead of `known_hunk_ids`' order;
  (iv) strip the rejection reason instead of carrying it verbatim.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red — a green mutation is a real finding about the
  tests and the reviewer wants it. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: the new `tests/orchestration/test_hunk_ledger.py`,
  `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/orchestration/test_hunk_apply.py` (11 at BASE),
  `tests/orchestration/test_hunk_subset_diff.py` (17 at BASE),
  `tests/regression/test_resource_safety.py` (21 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C7`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C8's own numbers are NOT ordered
  here; the reviewer measures C8 at the next gate. Report the range's path set
  against the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_ledger.py` and
  `tests/orchestration/test_hunk_ledger.py`: each 0, against
  `.agent/authored/f033-r10.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C7, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 3,
round 10, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Quote `build_hunk_ledger`'s final signature, the six vocabulary
constants with their values, the totality probe's `type()` results, and the test
names you wrote with the property each pins. No length cap. Write no verdict on
your own work.
