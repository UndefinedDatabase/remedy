# F033 — Hunk-level diff approval · ROUND 12 · THE RECORDER LEARNS THE VIEWER'S ENVELOPE

SESSION 3 of feature F033. Round 12, rounds so far 12.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R12`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline. Take a slice as the bytes
   from the end of its `<<<SLICE` marker line up to and INCLUDING the newline
   that ends its last content line.
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
10. Byte OFFSETS and byte SPANS are measured on BYTES, never on a decoded string.
11. IF A GATE AND A SPEC PARAGRAPH DISAGREE, the GATE is load-bearing: satisfy it,
    satisfy the SPEC's INTENT around it, and declare the disagreement. Round 11
    hit exactly this and resolved it correctly.

## Base

BASE is `624818e6`, the round 11 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs.

## Why this round exists

Round 11 PASSED. The reviewer re-executed all eight gates at `624818e6` from its
own scripts, reproduced every reading, ran all four ordered mutations with its
own anchors and added one of its own, which also went red. DECISION F033 D4 is
measured rather than asserted: the recorder's import list holds no applicator and
no storage, and all ten do-not-touch paths are byte-identical, so the door really
is untouched. That verdict and the resolution of R-0742 are booked by C2.

YOU WERE RIGHT ABOUT THE `save_job` COLLISION. The block's SPEC §1 asked the
persist-nothing paragraph to say "leaves `save_job` to the door" while G6(b)
ordered that token to read 0 in the module — a zero-gate over a string the
block's own SPEC asked to be written into the file it counts. You read the gate
as load-bearing, kept the paragraph's meaning by naming
`escalation.answer_task_decision` and `_dispatch_decision_resolve` instead, and
declared it. That is a reviewer-prose defect that damaged nothing on disk; it is
a dated line in `.agent/prose_slips.md` at C3 and convention 11 above now states
the rule you applied.

WHAT THE REVIEWER FOUND WHILE READING THE GROUND FOR THE WRITE DOOR, and it
re-sequences the rest of this feature. Measured at `624818e6`:

- `apps/cli/grouped.py` builds its argparse parsers FROM `GROUPS` and
  `get_commands_for_group`, and dispatches by `command_id` through
  `apps.cli.commands.collect_all_handlers`. A catalog entry with no handler is
  reachable in help and answers `Error: no handler for <id>`.
- The reviewer counted it rather than assuming: `CATALOG` holds 340 entries,
  `collect_all_handlers()` holds 340 handlers, and the number of catalog entries
  WITHOUT a handler is ZERO. No test asserts that invariant, and it has
  nevertheless never been broken.
- `UI_EXPOSED_COMMANDS` is a SUBSET of `CATALOG` and
  `TestUiExposedCommands.test_every_member_resolves_through_get_command` requires
  `get_command(id)` to resolve, so the door CANNOT expose an id that has no
  catalog entry, and the catalog entry should not land without its handler.

So the door is not the next round: the CLI command is, and the door follows it.
Both are blocked on one seam this round fixes.

THE SEAM. `record_hunk_decision` takes `attempt_diff_text` and parses it with
`parse_unified_diff_to_view`. But the thing that actually HAS an attempt's diff
is `packages/orchestration/diff_view_source.py`'s `build_diff_view(evidence_dir,
task_id)`, which returns an ENVELOPE that has already been parsed, already
carries `truncated`, and already reads the artifact under its own byte ceiling.
A caller holding that envelope has nothing to hand `record_hunk_decision` but the
raw text again — and re-reading and re-parsing would put a second copy of the
ceiling and the truncation rule beside the first, free to drift. Measured at
`624818e6`: `build_diff_view(None)` returns keys `available`, `files`, `reason`,
`scope`, `source`, `task_id`, `task_run_ids`, `truncated` and `version`, with
`available` False, `reason` `evidence_dir_unavailable` and `files` empty, while
`parse_unified_diff_to_view` returns `files`, `truncated` and `version` and has
NO `available` key at all.

THE REFUSAL THAT ABSENCE NEEDS. An envelope with `available` False has EMPTY
`files`, so every approved id would be unknown and `decide_hunk_approval` would
answer `unknown_hunk` — blaming the OPERATOR for an artifact that is not there.
That is the wrong answer to the wrong question, so this round mints one refusal
for it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 11 verdict and the R-0742 resolution into `.agent/live_review.md`
- C3 one dated line into `.agent/prose_slips.md`
- C4 the view entry point in `packages/orchestration/hunk_decision_record.py`
- C5 its tests in `tests/orchestration/test_hunk_decision_record.py`
- C6 the handback

You write NO `Done:` paragraph — `Done:` is the reviewer's word. This round
registers no finding, so there is no `Landed:` line and no `Landed:` commit.

## Change set — these paths and nothing else

    .agent/authored/f033-r12.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_decision_record.py
    tests/orchestration/test_hunk_decision_record.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r12.md`. This round
does NOT touch `packages/orchestration/hunk_ledger.py`,
`packages/orchestration/hunk_apply.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/source_apply.py`,
`packages/orchestration/diff_parser.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`apps/cli/commands/patch.py`, `tests/ui_server/test_command_channel.py` or
`docs/roadmap/STATUS.md`. THE DOOR AND THE CATALOG ARE PROVABLY UNCHANGED and G8
measures it. `.agent/context.md` is deliberately NOT touched.

## SPEC — `packages/orchestration/hunk_decision_record.py`

An EDIT that ADDS one entry point and RE-ROUTES the existing one through it.
Every public name that exists today keeps its name, its signature and its
behaviour; G6 measures both halves of that.

### 1. The new refusal

    #: The attempt has no diff to decide over ...
    HUNK_RECORD_REFUSAL_NO_DIFF = "no_diff_available"

Mint it beside the existing refusal constant, with the same comment idiom. WHY
it must exist rather than letting the decision core answer: an envelope whose
`available` is False carries an EMPTY `files` list, so every approved id would be
absent from the known set and `decide_hunk_approval` would answer
`REFUSAL_UNKNOWN_HUNK` — telling the operator their ids are wrong when the truth
is that the artifact is missing. Write that reasoning into the comment; it is
the same reasoning `hunk_subset_diff.py` gives for deciding untrustworthiness
BEFORE absence.

### 2. The view entry point

    record_hunk_decision_from_view(
        job: Any,
        *,
        task_id: Any,
        attempt: Any,
        attempt_view: Mapping[str, Any],
        approved: Iterable[str],
        rejected: Iterable[Any],
        now: datetime,
    ) -> HunkDecisionRecord | HunkApprovalRefusal

This becomes the ONE implementation. Its steps, in order, and each is a test:

1. AVAILABILITY. Read `attempt_view.get("available", True)`. Falsy → return a
   `HunkApprovalRefusal` carrying `HUNK_RECORD_REFUSAL_NO_DIFF`, a sentence that
   QUOTES the envelope's own `reason` value so the operator learns which absence
   it was, and an EMPTY `hunk_ids` tuple. NOTHING is written to `job.metadata`.
   THE DEFAULT IS `True` AND THE REASON IS LOAD-BEARING: `build_diff_view`
   carries an availability axis because an artifact can be missing, and
   `parse_unified_diff_to_view` carries none because text that exists IS
   available. A caller handing a raw parse must not be refused for a key that
   parser never emits. State that in a comment.
2. TRUSTWORTHINESS. `attempt_view["truncated"]` truthy → the existing
   `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` refusal, unchanged in code, message
   and emptiness, and again NOTHING is written. It is checked AFTER availability
   because an unavailable envelope is not truncated, it is absent.
3. From there the body is exactly what `record_hunk_decision` does today: the
   known ids in the view's own order, `decide_hunk_approval`, its refusals
   returned UNCHANGED with nothing written, `build_hunk_ledger` with
   `apply_attempted` LEFT AT ITS DEFAULT, and the record written under the
   composed attempt key, replacing any record already there.

`attempt_view["files"]` and `attempt_view["truncated"]` are read by SUBSCRIPT,
not by `.get`: a mapping without them is not a view, and defaulting one would
record an empty decision over a caller's mistake. `available` is the ONE key read
with a default, for the reason step 1 gives. Say so.

### 3. The text entry point becomes a wrapper

`record_hunk_decision` keeps its exact signature and its exact behaviour and
becomes: parse `attempt_diff_text` with `parse_unified_diff_to_view`, then
delegate to `record_hunk_decision_from_view` with every other argument passed
through UNCHANGED. It must hold no second copy of the truncation rule, the known-id
derivation, the ledger call or the metadata write — ONE implementation, two doors,
which is the whole reason this round exists. Its docstring says which of the two
it is and points at the other.

Add both names to the module docstring's `Public API::` block, and add one
paragraph saying WHY there are two doors: the viewer already parsed the artifact
under its own ceiling, and re-parsing text a caller already has as an envelope
would put a second copy of that ceiling beside the first.

## SPEC — `tests/orchestration/test_hunk_decision_record.py`

An EDIT that ADDS. Every existing test stays untouched and must still pass —
that is the proof the text entry point's behaviour did not move.

Add tests for: an envelope with `available` False refuses with
`HUNK_RECORD_REFUSAL_NO_DIFF`, QUOTES the envelope's `reason` in its message, and
writes NOTHING; an envelope with `available` False AND `truncated` True gets the
NO_DIFF code, not the untrustworthy one, because availability is decided first; a
view with NO `available` key at all is treated as available and records normally,
which is the raw-parser case and the discriminator that stops the default being
flipped; a truncated envelope still refuses as untrustworthy; a clean envelope
records exactly what the text entry point records for the same diff — build the
record BOTH ways, on two jobs, and assert the two exported dicts are EQUAL apart
from nothing at all; and a real `build_diff_view` envelope shape, constructed by
hand with the nine keys the reviewer measured, records normally.

Extend the module docstring's property list with what you added, in the file's
existing style.

## The slices

<<<SLICE PLANF033R12
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
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | open | this round |
| the CLI command and its handler | open | next |
| the write door's exposure and dispatch | open | after the CLI command |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The recorder takes the VIEWER'S ENVELOPE, not only diff text.
   `diff_view_source.build_diff_view` holds an attempt's diff already parsed and
   already read under its own byte ceiling; re-parsing text a caller has as an
   envelope would put a second copy of that ceiling beside the first. One
   implementation, two doors, plus the refusal an ABSENT artifact needs so the
   operator is not told their ids are wrong.
2. Then the CLI command and its handler TOGETHER. Measured at `624818e6`:
   `CATALOG` holds 340 entries and `collect_all_handlers()` 340 handlers, so
   entries without a handler number ZERO — no test asserts it, nothing has broken
   it, and `apps/cli/grouped.py` builds its parsers from the catalog, so a
   handlerless entry is reachable in help and answers `Error: no handler`. It
   lands in the `patch` group beside `patch.approve` and `patch.apply`.
3. Then the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the catalog pinned
   at exactly two ids by `TestUiExposedCommands`, so exposure needs step 2 first.
   `DOOR_METHODS` and `ALLOWED_IMPORTS` are EQUALITY guards widened in the same
   commit as the dispatch, and `packages.orchestration.hunk_apply` joins
   `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden mistake cannot be made
   silently later.
4. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit. R-0738 is T003's to repair.
<<<END PLANF033R12

<<<SLICE RECORDF033R12
Gate: F033 R11 — WHAT THE DOOR'S EFFECT IS. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `624818e6` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 36001 bytes at sha256 `7b42b486…56303`, BYTE-IDENTICAL to the reviewer's own pre-emission original, with ONE blob id `282dcf69` at C0b. THE RECORD APPEND at `d48b4850` reconstructs 1493203 plus one newline plus 11438 to 1504642, the committed blob exactly, base a byte PREFIX, the file ending in one newline, N COUNTED at 4 and the LAST FOUR blank-line units equal to the slice's paragraphs IN ORDER; the reviewer computed the FIRST appended paragraph's BYTE span as 1493204 to 1498026 — the same span the worker reported, the convention-10 correction having removed last round's character-versus-byte disagreement — and placed THREE negative controls inside it, at its start, its middle and two bytes from its end, all three rejected by BOTH readers. THE LEDGER moved exactly where the block allowed: registered 302 to 303 with the ADDED id exactly `R-0742`, `Done:` 46 lines over 44 distinct to 47 over 45 with the ADDED resolved id exactly `R-0741`, `Landed:` 14 to 14 to 15 with the added id exactly `R-0742` and the `Landed: R-0741` line still standing beside its `Done:` paragraph, `Gate:` 127 to 128 with `^Gate: F033 R10 — ` exactly 1, `DECISION F033 D` 3 to 4 with `^DECISION F033 D4 — ` exactly 1, and the open set 258 UNMOVED at all three commits. THE PROSE FILES landed byte-exactly: `.agent/plan.md` at 2472 bytes over 47 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 21213 plus one newline plus 865 to 22079. DECISION F033 D4 IS MEASURED RATHER THAN ASSERTED, which is the point of this round: `ruff check` exits 0 at "All checks passed!"; the recorder's AST import set is eleven names, every one of them standard library or from `packages.orchestration.diff_parser`, `packages.orchestration.hunk_approval` or `packages.orchestration.hunk_ledger`, with `hunk_apply`, `source_apply`, `storage`, `subprocess` and `shutil` ALL ABSENT and `open(` and `save_job` both reading 0 — so the module the write door will import drags neither the applier nor a storage write behind it; the two constants carry exactly `hunk_decisions` and `untrustworthy_view`; and the signature and field list match the ordered shape. THE FOUR ORDERED MUTATIONS WERE REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `624818e6`, the import first proved to resolve to the worktree's own copy, each anchor asserted UNIQUE in the file being edited before replacement and both targets restored byte-identically afterwards: the UNMUTATED CONTROL over both suites is a real exit 0 at 38 passed; building the ledger as attempted-and-applied is exit 1 at 1 failed naming the unattempted test; writing the record under `task_id` alone is exit 1 at 4 failed; skipping the truncated-view refusal is exit 1 at 1 failed; and DELETING THE `None` GUARD in `hunk_ledger._entries` — R-0742's own red-proof — is exit 1 at 1 failed naming `test_a_none_known_set_yields_no_rows_where_another_unusable_value_yields_one`, RED where the identical mutation came back GREEN at the previous round's base, which is exactly what a resolution of that finding had to demonstrate. THE REVIEWER THEN RAN A FIFTH MUTATION THE BLOCK NEVER ORDERED — writing the record even when `decide_hunk_approval` refused — and it went RED at 1 failed naming the returns-unchanged-and-writes-nothing test, so "a refused decision writes nothing" is genuinely pinned and not merely stated. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: the new `test_hunk_decision_record.py` 9, `test_hunk_ledger.py` 29, `test_hunk_approval.py` and `test_hunk_apply.py` 41 together, `test_diff_parser.py` 50, `tests/ui_server/test_command_channel.py` 106 and the canary `test_golden_path.py` 42. THE STRUCTURE: nine single-parent commits over BASE..C7 of 442, 309, 20, 8, 4, 14, 176, 248 and 2 insertions, every one under 500, with the handback a further 271; the range's path set EQUALS the declared change set in BOTH directions; residue 0 in all four targets against a 5 and 6 control; `git ls-files .remedy-wt` 0; and ALL TEN do-not-touch paths byte-identical by blob id, so the claim that the door is untouched this round is a measurement. THE WORKER FOUND A COLLISION IN THE REVIEWER'S OWN BLOCK AND RESOLVED IT THE RIGHT WAY: SPEC §1 asked the persist-nothing paragraph to say "leaves `save_job` to the door" while G6(b) ordered that token to read 0 in the same file — a zero-gate over a string the block's own SPEC asked to be written into the file it counts, which is checklist item 2's shape exactly. It read the gate as load-bearing, kept the paragraph's meaning by naming `escalation.answer_task_decision` and `_dispatch_decision_resolve` instead of spelling the identifier, and declared it. Nothing on disk is wrong, so under operator amendment amend0827 rule 2 it spends no id and buys no correction round.

Done: R-0742 — RESOLVED at `b80a56a1`, verified by the reviewer running the red-proof the finding's FIX clause asked for rather than by reading the test. `test_a_none_known_set_yields_no_rows_where_another_unusable_value_yields_one` now pins BOTH halves the finding required: that `build_hunk_ledger(None, decision)` yields ZERO rows, and that a non-`None` unusable value still yields exactly ONE row naming it — the second half being what stops the test passing under an `_entries` that returns `[]` for everything. THE PROOF IS THE COLOUR CHANGE, not the assertion text: deleting the two-line `None` guard in `packages/orchestration/hunk_ledger.py`'s `_entries` inside the reviewer's own disposable worktree came back GREEN at 28 passed when the finding was raised, and comes back RED at exit 1, 1 failed, naming exactly that test, at `624818e6`. A finding about an unpinned rule is resolved only by the mutation that used to pass and now fails, and that is the reading recorded here. The divergence itself is unchanged and still right: a validator reports the strange value it was handed, but a ledger would render it as a ROW, and a fabricated hunk called "None" in an operator's record is worse than an empty record. This resolution reaches the `hunk_ledger` instance only; the R-0671 class it belongs to — an honesty rule a module states and no test pins — is not discharged by it anywhere else in the repository.
<<<END RECORDF033R12

<<<SLICE SLIPSF033R12
2026-08-29 · F033 R11 · The block's SPEC §1 asked the recorder's persist-nothing paragraph to say it "leaves `save_job` to the door" while its own G6(b) ordered that token to read 0 in the same module, so the two could not both be satisfied literally; the worker read the gate as load-bearing, kept the paragraph's meaning by naming `escalation.answer_task_decision` and `_dispatch_decision_resolve` instead, and declared it, which is the required behaviour and is now stated as convention 11 of the next block.

2026-08-29 · F033 R11 · The handback reported the recorder's AST import list as 8 entries where the reviewer's own extractor counts 11 `(module, name)` pairs; both readings agree on the property the gate exists for — every entry standard library or one of the three allowed modules, with all five forbidden names absent — and the difference is only whether dotted names or import statements were counted.
<<<END SLIPSF033R12

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r12.md` and of `.remedy-wt/f033-r12-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r12.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1506343 bytes, plus one newline plus RECORDF033R12 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R12 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the open set at
  both. Ordered: registered 303 UNMOVED — this round registers NOTHING;
  `Done:` 47 to 48 lines and 45 to 46 distinct with the ADDED resolved id exactly
  `R-0742`; `Landed:` 15 UNMOVED, the `Landed: R-0742` line still present beside
  its new `Done:` paragraph as this append-only record requires; `Gate:` 128 to
  129 with `^Gate: F033 R11 — ` exactly 1; `DECISION F033 D` 4 UNMOVED; and the
  open set 258 to 257.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R12 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  22079 bytes, plus one newline plus SLIPSF033R12, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching
  `^2026-\d\d-\d\d · F033 R11 · ` at BASE and at C3, and the count of lines
  beginning `- R-` in the whole file at C3, which must be 0.
- **G6 THE CODE AGAINST THE SPEC at C4.** (a) `ruff check` over the module and
  its test file exits 0 — report the summary line. (b) By AST, report the
  module's FULL import list; every entry must be standard library or from
  `packages.orchestration.diff_parser`, `packages.orchestration.hunk_approval`
  or `packages.orchestration.hunk_ledger`, and `hunk_apply`, `source_apply`,
  `storage`, `subprocess` and `shutil` must each be ABSENT, with `open(` and
  `save_job` each reading 0 in its text — DECISION F033 D4 must survive this
  round unchanged. (c) Report the three module-level refusal-and-key constants
  with their values; `HUNK_DECISIONS_METADATA_KEY` and
  `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` must be UNCHANGED from BASE and
  `HUNK_RECORD_REFUSAL_NO_DIFF` must read `no_diff_available`. (d) Report the
  extracted signatures of BOTH `record_hunk_decision` and
  `record_hunk_decision_from_view`; the FIRST must be byte-identical to its
  signature at BASE. (e) THE WRAPPER HOLDS NO SECOND COPY: extract
  `record_hunk_decision`'s function body by AST and report it; it must contain a
  call to `record_hunk_decision_from_view` and must NOT contain the names
  `build_hunk_ledger`, `decide_hunk_approval`, `export_hunk_ledger` or
  `setdefault`. (f) Exercise BOTH shipped entry points once directly, not through
  the tests, on the SAME two-hunk diff and two separate jobs, and report that the
  two exported records are EQUAL.
- **G7 THE MUTATION RED-PROOFS at C5.** In a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROL over
  `tests/orchestration/test_hunk_decision_record.py` — REAL exit 0, report the
  count, which must exceed the 9 BASE gives. Then, one at a time, reverting fully
  between each, asserting the anchor is UNIQUE before replacing it, and reporting
  the REAL exit code, the failure count and the NAME of each failing test:
  (i) skip the availability refusal entirely;
  (ii) default `available` to False instead of True;
  (iii) check truncation BEFORE availability;
  (iv) write the record even when the availability refusal fires.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_hunk_decision_record.py`,
  `tests/orchestration/test_hunk_ledger.py` (29 at BASE),
  `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/orchestration/test_hunk_apply.py` (11 at BASE),
  `tests/orchestration/test_diff_view_source.py`,
  `tests/ui_server/test_command_channel.py` (106 at BASE),
  `tests/regression/test_resource_safety.py` (21 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C5`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C6's own numbers are NOT ordered
  here. Report the range's path set against the change set in BOTH directions.
  Count `<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_decision_record.py` and
  `tests/orchestration/test_hunk_decision_record.py`: each 0, against
  `.agent/authored/f033-r12.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C5, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 3,
round 12, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Quote both entry points' final signatures, the three constants with
their values, `record_hunk_decision`'s extracted body from G6(e), and the test
names you wrote with the property each pins.

THIS IS THE LAST DELEGATED ROUND OF SESSION 3. Say so in the handback, carry
SESSION 3 forward, and name the next session's first actions in this order:
read `.agent/STOP` from disk, then run the Open PR Gate, then book this round's
verdict, then the CLI command of the plan's step 2. No length cap. Write no
verdict on your own work.
