# F033 — Hunk-level diff approval · ROUND 11 · WHAT THE DOOR'S EFFECT IS

SESSION 3 of feature F033. Round 11, rounds so far 11.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R11`.
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
10. Byte OFFSETS and byte SPANS are measured on BYTES, never on a decoded string:
    this record is full of em-dashes and ellipses, and a character count of the
    same paragraph is smaller than its byte count.

## Base

BASE is `97861cdf`, the round 10 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs.

## Why this round exists

Round 10 PASSED. The reviewer re-executed all eight gates at `97861cdf` from its
own scripts, reproduced every ordered reading, ran all four ordered mutations
with its own anchors and added two of its own. Your unordered commit `bd3bdcb1`
was RIGHT and the reviewer confirmed why: with the refusal stated twice, a
single-anchor mutation of one site could not reach a test, so the ordered colour
would have come back green for a reason that said nothing about the tests. That
verdict, the resolution of R-0741 and one new finding are booked by C2.

ONE OF THE REVIEWER'S OWN UNORDERED MUTATIONS CAME BACK GREEN, and it is
R-0742 below. Your deviation 3 declared a DELIBERATE DIVERGENCE from
`hunk_approval._entries` — `None` yields NO rows here, where the sibling yields
one — and gave the reason in the docstring. Reverting that divergence in the
reviewer's worktree left all 28 tests passing, so the rule is stated and
unpinned. C5 pins it.

THIS ROUND SETTLES WHAT THE WRITE DOOR ACTUALLY DOES, and builds the one thing
it will call. The plan has carried "needs the door's effect ruled" for three
rounds. DECISION F033 D4 in the record slice rules it, and the reasoning is
below so you can check the decision rather than take it.

THE MEASUREMENTS THE DECISION RESTS ON, all taken by the reviewer at `97861cdf`:

- `tests/ui_server/test_command_channel.py`'s `TestCommandDoorImportGuard`
  docstring states the contract as "the write door ENQUEUES, it never applies",
  and its `FORBIDDEN_MODULES` holds `packages.orchestration.source_apply`,
  `patch_apply`, `diff_repair_apply`, `job_fulfillment`, `exec_guard`,
  `workspace`, `secure_fs`, `subprocess` and `shutil`.
- `packages/orchestration/hunk_apply.py` imports
  `packages.orchestration.source_apply`. The guard's `_door_imports` walks the
  AST of the named methods and collects DIRECT imports only, so a door importing
  `hunk_apply` would PASS `test_the_door_imports_nothing_from_a_forbidden_module`
  while running the applier inside the HTTP handler. The guard would be defeated
  by name rather than by substance.
- `apply_approved_hunks` requires `repo_path`, `job`, `intent_id` and `data_dir`,
  and `apply_structured_patch` refuses without an APPROVED patch intent. The door
  has no intent to hand it.
- Both ids the door already dispatches RECORD rather than apply: `job.stop` calls
  `safe_points.request_stop`, whose signal a later runner consumes, and
  `decision.resolve` calls `escalation.answer_task_decision` then
  `storage.save_job`.
- `packages/orchestration/hunk_ledger.py` already carries
  `HUNK_LANDING_UNATTEMPTED` for exactly this state — a decision recorded before
  any apply has run.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 10 verdict, the R-0741 resolution, the R-0742 registration and
  DECISION F033 D4, into `.agent/live_review.md`
- C3 two dated lines into `.agent/prose_slips.md`
- C4 the R-0742 test in `tests/orchestration/test_hunk_ledger.py`
- C5 the recorder module
- C6 its tests
- C7 the `Landed: R-0742` line into `.agent/live_review.md`
- C8 the handback

C5 and C6 are SEPARATE COMMITS for the reason rounds 8, 9 and 10 all gave.

## Change set — these paths and nothing else

    .agent/authored/f033-r11.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    tests/orchestration/test_hunk_ledger.py
    packages/orchestration/hunk_decision_record.py
    tests/orchestration/test_hunk_decision_record.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r11.md`,
`packages/orchestration/hunk_decision_record.py` and
`tests/orchestration/test_hunk_decision_record.py`. This round does NOT touch
`packages/orchestration/hunk_ledger.py`,
`packages/orchestration/hunk_apply.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/source_apply.py`,
`packages/orchestration/diff_parser.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`tests/ui_server/test_command_channel.py` or `docs/roadmap/STATUS.md`. THE DOOR
IS PROVABLY UNCHANGED THIS ROUND and G8 measures that: the decision is ruled and
the thing it will call is built, and the wiring is the NEXT round, which is how
DECISION F009 D17 split this same door before.
`.agent/context.md` is deliberately NOT touched.

## SPEC — the R-0742 test in `tests/orchestration/test_hunk_ledger.py`

An EDIT that ADDS. Every existing test stays untouched. Add ONE test pinning the
divergence the module's `_entries` docstring declares: `build_hunk_ledger(None,
decision)` returns a ledger with ZERO entries, and — this is the half that makes
it a discriminator rather than a restatement — a ledger built from a
non-``None`` unusable value, such as an integer, returns exactly ONE entry whose
`hunk_id` is that value as text. Without the second half the test passes under an
`_entries` that returns `[]` for everything. Name it for the property. Extend the
module docstring's property list with it, in the file's existing style.

## SPEC — `packages/orchestration/hunk_decision_record.py`

A NEW module: the seam between an operator's hunk decision and the job it is
recorded on. It is what DECISION F033 D4 rules the write door will call.

### 1. What it is, and the two things it deliberately is not

It takes an attempt's diff text and an operator's decision, validates the
decision, builds the ledger, and PUTS THAT LEDGER ON THE JOB. It APPLIES
NOTHING: it does not import `packages.orchestration.hunk_apply`,
`packages.orchestration.source_apply` or any other applicator, and it never
touches a repository. Write that as a DELIBERATE ABSENCE naming the guard in
`tests/ui_server/test_command_channel.py` it exists to satisfy in substance.

It also SAVES NOTHING. It MUTATES `job.metadata` and returns; persisting is the
caller's, exactly as `escalation.answer_task_decision` leaves `save_job` to the
door — `packages/orchestration/ui_server.py`'s `_dispatch_decision_resolve` says
so in as many words at `97861cdf`. So this module imports no storage either, and
a reader who came looking for the write should stop at that paragraph.

Imports: the standard library, `packages.orchestration.diff_parser`,
`packages.orchestration.hunk_approval` and `packages.orchestration.hunk_ledger`.
Nothing else.

### 2. The metadata shape

    #: The key on ``job.metadata`` under which every hunk decision is recorded.
    HUNK_DECISIONS_METADATA_KEY = "hunk_decisions"

Its value is a dict mapping an ATTEMPT KEY to one exported record. The attempt
key is `f"{task_id}:{attempt}"` after both have been coerced to text, and a
SECOND decision on the SAME key REPLACES the first rather than appending — an
operator may revise a decision while the landing is still `unattempted`, and two
records for one attempt would leave the viewer choosing between them. State that
rule in a comment; it is a test.

Each record is JSON-safe and carries exactly the keys `task_id`, `attempt`,
`decided_at` and `hunks`, where `hunks` is `export_hunk_ledger(ledger)["hunks"]`
— the ledger's own rows, unwrapped, so the shape is not doubled.

### 3. The refusals

    HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW = "untrustworthy_view"

The ONE refusal this module mints of its own. When
`parse_unified_diff_to_view(attempt_diff_text)["truncated"]` is true, the known
id set is INCOMPLETE, so every hunk the parser never showed would be recorded as
`pending` — a positive claim that the operator left it undecided, when in truth
nobody was ever shown it. Refuse instead. `packages/orchestration/hunk_subset_diff.py`
refuses the same shape as `SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW` for the neighbouring
reason, and this constant is spelled to match it deliberately; say so.

Every OTHER refusal is `decide_hunk_approval`'s and is returned UNCHANGED, code,
message and offending ids intact. This module mints no second vocabulary for
faults that already have one.

### 4. The entry point

    record_hunk_decision(
        job: Any,
        *,
        task_id: Any,
        attempt: Any,
        attempt_diff_text: str,
        approved: Iterable[str],
        rejected: Iterable[Any],
        now: datetime,
    ) -> HunkDecisionRecord | HunkApprovalRefusal

with

    @dataclass(frozen=True)
    class HunkDecisionRecord:
        attempt_key: str
        ledger: HunkDecisionLedger
        exported: dict

Steps, in order, and each is a test:

1. Parse `attempt_diff_text`. If the view is truncated, return a
   `HunkApprovalRefusal` carrying `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW`, a
   sentence saying why, and an EMPTY `hunk_ids` tuple — no single id is at
   fault. NOTHING IS WRITTEN to `job.metadata` in that case, and a test pins that
   by comparing the metadata before and after.
2. Otherwise the known ids are every hunk id of every file, in the view's own
   order. Say in a comment that this is the DIFF's order and that the ledger
   walks it.
3. Call `decide_hunk_approval(known_ids, approved, rejected)`. A
   `HunkApprovalRefusal` is returned UNCHANGED and, again, NOTHING IS WRITTEN.
4. Build the ledger with `build_hunk_ledger(known_ids, decision)` — with
   `apply_attempted` LEFT AT ITS DEFAULT, so every entry is `unattempted`. That
   is the whole point of the decision below: recording a decision is not
   applying it. Never pass `applied` or `landed_hunk_ids` from here; a comment
   says a later apply is what revises those, not this call.
5. Write the record under the attempt key, creating
   `job.metadata[HUNK_DECISIONS_METADATA_KEY]` if absent and REPLACING any
   record already under that key. `decided_at` is `now.isoformat()`.
6. Return the `HunkDecisionRecord`.

TOTALITY IS NOT CLAIMED HERE and the module must not pretend to it. Its two pure
dependencies are total, but this one reads `job.metadata`, and a `job` whose
metadata is not a dict, or whose attribute access raises, is a real programming
error a caller must see. Say so in the docstring, in the idiom
`packages/orchestration/hunk_apply.py` uses for the same admission. A non-string
`task_id` or `attempt` is NOT that class and is coerced to text.

## SPEC — `tests/orchestration/test_hunk_decision_record.py`

A NEW file. Build real diffs with `difflib.unified_diff` the way
`tests/orchestration/test_hunk_apply.py` does, and build a `Job` the way it
builds one; do not import across test files. Cover at least: a clean decision
writes one record under the right attempt key with every entry `unattempted`; the
`hunks` rows carry the ledger's own four keys and the diff's order; a rejection's
reason survives verbatim into the record; a second decision on the SAME attempt
key REPLACES the first and leaves the dict one entry long; a decision on a
DIFFERENT attempt key leaves the first record standing; a truncated view refuses
with `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` and writes NOTHING; a decision
refusal from `decide_hunk_approval` is returned unchanged and writes NOTHING;
a job whose metadata already holds unrelated keys keeps them; and the whole
exported record survives `json.dumps` without a custom encoder.

## The slices

<<<SLICE PLANF033R11
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
| T001 stable ids, viewer v2, consolidation | done | closed round 5 |
| the approval decision core | done | round 6 |
| the approved subset diff | done | round 7 |
| landing the subset all-or-nothing | done | round 8 |
| the failed-rollback truth | done | round 9, R-0740 |
| the hunk-decision ledger | done | round 10, R-0741 |
| what the door's effect IS, and the recorder | open | this round, DECISION F033 D4 |
| the write door itself | open | next, needs three guards widened together |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Rule the door's effect and build what it calls. DECISION F033 D4: the door
   RECORDS a hunk decision and never applies it, because `hunk_apply` imports
   `source_apply` and a door importing the seam would defeat the P3 import guard
   by name rather than by substance. `record_hunk_decision` is that effect, and
   R-0742 pins the ledger divergence round 10 declared but left untested.
2. Then the door itself, in ONE commit per widened guard plus its dispatch:
   `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` is pinned at exactly
   two ids by `TestUiExposedCommands`; `DOOR_METHODS` and `ALLOWED_IMPORTS` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards; and
   `packages.orchestration.hunk_apply` joins `FORBIDDEN_MODULES` so the mistake
   D4 forbids cannot be made silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report's "partially approved (5/8 hunks)" line derived from the ledger, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- Exposure without dispatch answers 501, so the catalog entry and the dispatch
  belong to one round.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R11

<<<SLICE RECORDF033R11
Gate: F033 R10 — THE HUNK-DECISION LEDGER. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `97861cdf` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 34128 bytes at sha256 `dc3caa08…3f1368`, BYTE-IDENTICAL to the reviewer's own pre-emission original, with ONE blob id `e04eaf4f` at C0b. THE RECORD APPEND at `c50b5ccf` reconstructs 1481910 plus one newline plus 9582 to 1491493, the committed blob exactly, base a byte PREFIX, the file ending in one newline, N COUNTED at 3 and the LAST THREE blank-line units equal to the slice's paragraphs IN ORDER; the reviewer placed THREE negative controls inside the FIRST appended paragraph — at its start, its middle and three bytes from its end — and BOTH readers rejected all three. THE LEDGER moved exactly where the block allowed: registered 301 to 302 with the ADDED id exactly `R-0741`, `Done:` 45 lines over 43 distinct to 46 over 44 with the ADDED resolved id exactly `R-0740`, `Landed:` 13 to 13 to 14 with the added id exactly `R-0741` and the `Landed: R-0740` line still present beside its new `Done:` paragraph, `Gate:` 126 to 127 with `^Gate: F033 R9 — ` exactly 1, and the open set 258 UNMOVED at all three commits because one id was registered and one resolved in the same commit. THE PROSE FILES landed byte-exactly: `.agent/plan.md` at 2494 bytes over 46 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 20761 plus one newline plus 451 to 21213. THE R-0741 REPAIR AT `f042e0a3` IS COMMENT ONLY, proved by the reviewer independently: the docstring-blanked `ast.dump` of `packages/orchestration/hunk_apply.py` is EQUAL across the change, with a control changing one executable literal REJECTED, and the retired reason reads 0 after. THE LEDGER MODULE AGAINST THE SPEC: `ruff check` exits 0 at "All checks passed!"; the AST import set is exactly `__future__.annotations`, `collections.abc.Iterable`, `collections.abc.Mapping`, `dataclasses.dataclass`, `typing.Any` and `packages.orchestration.hunk_approval.HunkDecision`, with `hunk_apply`, `source_apply`, `hunk_subset_diff` and `diff_parser` all ABSENT — so the claim that the write door may import this module without dragging the applier behind it is MEASURED rather than asserted; `open(`, `import os`, `import subprocess`, `import logging` and `Path` all read 0; the six vocabulary constants carry exactly `approved`, `rejected`, `pending`, `landed`, `not_landed` and `unattempted`; and the signature and both field lists match the ordered shape. THE FOUR ORDERED MUTATIONS WERE REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `97861cdf`, the import first proved to resolve to the worktree's own copy, each anchor asserted UNIQUE before replacement and the module restored byte-identically after: the UNMUTATED CONTROL is a real exit 0 at 28 passed; honouring `landed_hunk_ids` while `applied` is false is exit 1 at 1 failed naming `test_a_failed_apply_does_not_honour_the_landed_ids_it_was_handed`; ignoring `apply_attempted` is exit 1 at 1 failed naming `test_an_unattempted_apply_overrides_every_other_landing_argument`; emitting in the decision's order is exit 1 at 3 failed; and stripping the rejection reason is exit 1 at 1 failed naming the verbatim test. Each reddens exactly the tests that name its property. THE REVIEWER THEN RAN TWO MUTATIONS THE BLOCK NEVER ORDERED. Swapping the approved-before-rejected check order came back GREEN, which CONFIRMS the module's own comment that the order is unobservable through the supported path rather than contradicting it. Reverting the `_entries(None)` divergence ALSO came back green, and that one is R-0742 below. THE UNORDERED COMMIT `bd3bdcb1` WAS CORRECT AND THE REVIEWER CONFIRMED ITS REASONING BY MEASUREMENT: with the landing refusal stated at two sites, a single-anchor mutation of either leaves the other enforcing the rule, so the ordered colour could only have come back green for a reason saying nothing about the tests; the worker removed the duplicate, put the rule at one site, declined to amend the earlier commit because amending is a history rewrite, and declared all of it. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: the new `test_hunk_ledger.py` 28, `test_hunk_approval.py` 30, `test_hunk_apply.py` 11, `test_hunk_subset_diff.py` 17, `test_resource_safety.py` 21 and the canary `test_golden_path.py` 42. THE STRUCTURE: ten single-parent commits over BASE..C7 of 436, 308, 15, 6, 2, 6, 303, 14, 285 and 2 insertions, every one under 500, with the handback a further 292; the range's path set EQUALS the declared change set in BOTH directions; residue 0 in all four targets against a 5 and 6 control; `git ls-files .remedy-wt` 0; and all nine do-not-touch paths byte-identical by blob id.

Done: R-0741 — RESOLVED at `f042e0a3`, verified by the reviewer reading the diff and then proving the confinement mechanically rather than by eye. `HunkApplyOutcome`'s docstring no longer gives "there is no partial landing to distinguish it from" as the reason `landed` is empty on failure — that phrase reads 0 in the file after the change. It now says what is true: not that a partial state on disk is impossible, but that this module learns WHICH hunks landed only from a SUCCESSFUL apply and so has no per-hunk answer to give on failure, and it points at `_failure_lead_sentence` as where a partial state IS reported. The surviving first clause, that `landed` is EMPTY whenever `applied` is false, is untouched, so no caller's reading of the field changed. THE REPAIR IS PROVABLY PROSE: the docstring-blanked `ast.dump` of the module is EQUAL either side of the commit, against a negative control that changes one executable literal and is REJECTED — an equality that cannot fail proves nothing, so the control is what makes this reading evidence. The finding's FIX clause asked for exactly this reason and this pointer, and both are there. THE BINDING CLAUSE R-0741 CARRIED FORWARD is NOT discharged by this resolution and binds the next block that orders a grep-derived leave-alone set: name each hit by FILE AND LINE and by the SYMBOL that encloses it, resolved at the base SHA, and state per hit why it is left alone.

- R-0742 — Low, A DELIBERATE BEHAVIOURAL DIVERGENCE FROM A SIBLING MODULE IS STATED IN A DOCSTRING AND PINNED BY NOTHING. Raised by the reviewer at the F033 R10 gate, by running a mutation the block never ordered, and measured at `97861cdf`. THE STATE ON DISK: `packages/orchestration/hunk_ledger.py`'s `_entries` returns `[]` for `None` where `packages/orchestration/hunk_approval.py`'s `_entries` returns one entry, and its docstring calls this "ONE DELIBERATE DIVERGENCE", giving the reason — a validator reports the strange value it was handed, but a ledger would render it as a ROW, and a fabricated hunk called "None" in the operator's record is worse than an empty record. That reasoning is correct and the reviewer confirmed the effect by calling the shipped function: `build_hunk_ledger(None, decision)` returns zero rows while `'x'`, `7` and a bare `object()` each return exactly one row carrying that value as text. THE PROBLEM IS THAT NOTHING PINS IT. Deleting the two-line `None` guard in the reviewer's own disposable worktree left the suite at 28 passed, exit 0 — so the divergence survives only as long as the next reader believes the comment. The ordered totality test cannot see it: it requires a `HunkDecisionLedger` back and no raise, and both hold whether `None` yields zero rows or one fabricated one. WHY LOW: no behaviour is wrong today and the shipped rule is the right one; the exposure is that a later refactor aligning the two `_entries` "for consistency" would silently start writing a hunk called "None" into an operator's record, and every gate in this feature would stay green. It is not lower because this is a record a human reads to decide what was approved. FIX: one test asserting `build_hunk_ledger(None, decision)` has zero entries AND that a non-`None` unusable value still yields exactly one entry naming it — the second half is what stops the test passing under an `_entries` that returns `[]` for everything. This is the R-0671 class, an honesty rule a module states and no test pins, on a different file.

DECISION F033 D4 — THE WRITE DOOR RECORDS A HUNK DECISION AND NEVER APPLIES ONE, AND THE APPLY STAYS ON THE JOB BRANCH WHERE AN APPROVED INTENT EXISTS. THE SITUATION. `docs/roadmap/features/T5_F033.md` gives T002 "command + validation + subset apply atomicity + hunk ledger", and the plan carried "the write-door command and its exposure" for three rounds with the effect unruled. THE MEASUREMENTS, taken by the reviewer at `97861cdf` by reading each file rather than by grep alone. `TestCommandDoorImportGuard` in `tests/ui_server/test_command_channel.py` states the contract as "the write door ENQUEUES, it never applies" and its `FORBIDDEN_MODULES` holds `packages.orchestration.source_apply` first. `packages/orchestration/hunk_apply.py` imports that module, and the guard's `_door_imports` collects DIRECT imports from the AST of the named methods only — so a door importing `hunk_apply` would PASS `test_the_door_imports_nothing_from_a_forbidden_module` while running the applier inside an HTTP handler. `apply_approved_hunks` additionally requires an `intent_id` naming an APPROVED patch intent, which the door does not have. Both ids the door already dispatches record rather than apply: `job.stop` leaves a signal a later runner consumes, and `decision.resolve` answers a decision and saves the job. CHOSEN: `approve_hunks` at the door VALIDATES the decision, BUILDS the hunk ledger with every landing `unattempted`, and RECORDS it on the job; the apply runs later, on the job branch, where the intent exists. `packages/orchestration/hunk_decision_record.py` is that effect and this round builds it; the wiring is the next round. ALTERNATIVE 1, let the door import `hunk_apply` and apply inline, REJECTED: it defeats the P3 guard by naming a module the forbidden list has not caught up to, which is worse than an honest violation because the suite stays green; it puts a repository write inside a request handler; and it needs an approved intent the door cannot produce. ALTERNATIVE 2, widen `FORBIDDEN_MODULES` and route the apply through a service the door may import, REJECTED as an alternative and ADOPTED as a hardening: a service seam that ends in the applier is Alternative 1 with one more file in it, but adding `packages.orchestration.hunk_apply` to `FORBIDDEN_MODULES` stops the mistake being made silently later, and the next round does that in the same commit as the dispatch. ALTERNATIVE 3, expose the id now and let it answer 501 until a later round dispatches it, REJECTED: DECISION F009 D22 keeps that 501 as an UNREACHABLE guard, and exposing an undispatched id converts a guard into live behaviour for no gain. WHY THIS IS THE REVIEWER'S CALL AND NOT A QUESTION: docs/agents/planner_reviewer_prompt.md §4 item 7 routes a wrong or missing spec to planning as a loud, persisted, reversible DECISION carried in the block, never as a question to the operator. HOW TO REVERSE: delete this paragraph and give the door `apply_approved_hunks` directly; `packages/orchestration/hunk_decision_record.py` has no other caller until the next round wires it, so nothing else depends on this ruling today.
<<<END RECORDF033R11

<<<SLICE SLIPSF033R11
2026-08-29 · F033 R10 · The reviewer's own first re-derivation of the first appended paragraph's SPAN gave 1481911..1486856 where the worker reported 1481911..1486878, and the worker was right: the reviewer measured `len()` on a DECODED string while the offset is a BYTE offset, and this record's em-dashes and ellipses make the byte count 22 larger; both readings put the ordered control inside the paragraph, so the proof itself was unaffected.

2026-08-29 · F033 R10 · The block's G6(a) ordered the surviving clause "``landed`` is EMPTY whenever ``applied`` is false" reported as present, and the reviewer's own probe expected it exactly once while the file legitimately carries it twice — the module docstring gained the same sentence in round 9 — so the expectation rather than the file was wrong, and nothing the block ordered depended on the number.
<<<END SLIPSF033R11

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C7, so the handback at C8 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C8,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r11.md` and of `.remedy-wt/f033-r11-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r11.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1493203 bytes, plus one newline plus RECORDF033R11 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R11 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2 and C7.** At BASE, at C2 and at C7 count `^- R-\d+ — `
  with distinct ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the open set at all
  three. Ordered: registered 302 to 303 at C2 with the ADDED id exactly `R-0742`,
  UNMOVED at C7; `Done:` 46 to 47 lines and 44 to 45 distinct at C2 with the
  ADDED resolved id exactly `R-0741`, UNMOVED at C7 — you author no `Done:`
  paragraph of your own; `Landed:` 14 UNMOVED at C2 and 14 to 15 at C7, the added
  line matching `^Landed: R-0742 — `; `Gate:` 127 to 128 at C2 with
  `^Gate: F033 R10 — ` exactly 1, UNMOVED at C7; `DECISION F033 D` 3 to 4 at C2
  with `^DECISION F033 D4 — ` exactly 1; the open set 258 UNMOVED at C2 — one
  registered and one resolved in the same commit — and UNMOVED at C7. C7
  additionally keeps the C2 blob as a byte PREFIX.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R11 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  21213 bytes, plus one newline plus SLIPSF033R11, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching
  `^2026-\d\d-\d\d · F033 R10 · ` at BASE and at C3, and the count of lines
  beginning `- R-` in the whole file at C3, which must be 0.
- **G6 THE CODE AGAINST THE SPEC.** (a) `ruff check` over
  `packages/orchestration/hunk_decision_record.py`,
  `tests/orchestration/test_hunk_decision_record.py` and
  `tests/orchestration/test_hunk_ledger.py` exits 0 — report the summary line.
  (b) By AST, report the recorder's FULL import list; every entry must be
  standard library or one of `packages.orchestration.diff_parser`,
  `packages.orchestration.hunk_approval` and `packages.orchestration.hunk_ledger`,
  and `hunk_apply`, `source_apply`, `storage`, `subprocess` and `shutil` must
  each be ABSENT — this is DECISION F033 D4 measured rather than asserted.
  Report also the counts of `open(` and `save_job` in its text: each 0.
  (c) Report `HUNK_DECISIONS_METADATA_KEY` and
  `HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW` with their values. (d) Report the
  extracted signature of `record_hunk_decision` and the field list of
  `HunkDecisionRecord`, matching §4. (e) Exercise the SHIPPED function once
  directly, not through the tests: build a two-hunk diff, record a decision
  approving one hunk, and print the resulting `job.metadata` entry as
  `json.dumps` output — every entry's `landing` must read `unattempted`, and
  report that `json.dumps` needed no custom encoder.
- **G7 THE MUTATION RED-PROOFS at C6.** In a DISPOSABLE `git worktree` at C6,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROL over BOTH
  `tests/orchestration/test_hunk_decision_record.py` and
  `tests/orchestration/test_hunk_ledger.py` — REAL exit 0, report both counts.
  Then, one at a time, reverting fully between each, asserting the anchor is
  UNIQUE in the file you are editing before replacing it, and reporting the REAL
  exit code, the failure count and the NAME of each failing test:
  (i) in the recorder, pass `apply_attempted=True` and `applied=True` to
      `build_hunk_ledger`;
  (ii) in the recorder, write the record under `task_id` alone instead of the
      composed attempt key;
  (iii) in the recorder, skip the truncated-view refusal and record anyway;
  (iv) in `packages/orchestration/hunk_ledger.py`, delete the `None` guard in
      `_entries` so it returns one row again — this is R-0742's own red-proof and
      it MUST now go red, where it came back green at BASE.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: the new
  `tests/orchestration/test_hunk_decision_record.py`,
  `tests/orchestration/test_hunk_ledger.py` (28 at BASE),
  `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/orchestration/test_hunk_apply.py` (11 at BASE),
  `tests/orchestration/test_diff_parser.py`,
  `tests/ui_server/test_command_channel.py`,
  `tests/regression/test_resource_safety.py` (21 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C7`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C8's own numbers are NOT ordered
  here. Report the range's path set against the change set in BOTH directions.
  Count `<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_decision_record.py` and
  `tests/orchestration/test_hunk_decision_record.py`: each 0, against
  `.agent/authored/f033-r11.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C7, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 3,
round 11, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Quote `record_hunk_decision`'s final signature, the two constants
with their values, the `json.dumps` output G6(e) asks for, and the test names you
wrote with the property each pins. No length cap. Write no verdict on your own
work.
