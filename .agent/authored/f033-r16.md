# F033 — Hunk-level diff approval · ROUND 16 · PARTIAL APPLY STATE BECOMES TELLABLE

SESSION 4 of feature F033. Round 16, rounds so far 16.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R16`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline. Take a slice as the bytes
   from the end of its `<<<SLICE` marker line up to and INCLUDING the newline
   that ends its last content line.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON AND THE TYPESCRIPT ARE A SPEC, NOT A SLICE. You write the code and
   the tests from the description. Names, signatures and the behaviours the SPEC
   fixes are binding; structure, comment wording and test names are yours. If the
   SPEC is impossible, STOP and say so rather than inventing past it.
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
    satisfy the SPEC's INTENT around it, and declare the disagreement.
12. NO `npm`, NO `npx`, NO vitest run is ordered this round, and none is needed:
    the TypeScript change is pinned by a PYTHON contract test that reads the
    source, which is this repository's own established way to guard `apps/ui/src`.

## Base

BASE is `1329ef45fbd1f4e189991ffc2ce4a8b2853c1b6a`, the round 15 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 15 PASSED and C2 books that verdict, resolves R-0744 and registers R-0745.

R-0744 IS FIXED AND THE PROOF IS THE COLOUR CHANGE: reverting the fix to the raw
argument inside the reviewer's own disposable worktree goes RED at 2 failed,
naming the two tests that name a job by short prefix and by uppercase UUID —
where at `fa963c4e` applying the same fix left all eleven tests GREEN. YOUR
DEVIATION D1 WAS ALSO VERIFIED BY COLOUR rather than by reading it: making the
hunk 409 reuse the decision wording goes RED at exactly
`test_every_exposed_command_reaches_the_answer_its_effect_gives`, so the edit you
were forced into really does pin the two 409s apart. The block claimed nothing
else in that file would change and it was wrong; that is the reviewer's prose
slip, recorded at C3, and your edit widened the guard rather than weakening it.

R-0745 IS NEW AND THE REVIEWER RAISED IT WITH A MEASUREMENT NO GATE ORDERED. The
door's import guard reads DIRECT imports only, so the reviewer walked the
TRANSITIVE closure of the door methods' own imports at BASE and at `1329ef45`. At
BASE no member of `FORBIDDEN_MODULES` was reachable at all. At `1329ef45`
`subprocess` is, through `packages/orchestration/evidence_index.py`, which imports
it at module level for the `_git` and `_git_raw` helpers that
`resolve_job_evidence_dir` never calls. THE REAL APPLIERS ARE ABSENT AT BOTH, so
DECISION F033 D4's own claim holds and this is not a D4 violation; what moved is
the P3 shell-capability boundary, and it moved because the door started importing
that module. It is Low and the fix is small.

NOW THIS ROUND'S WORK: R-0738, which T003 has owned since round 1.

WHAT IS WRONG, re-measured at BASE. `_task_truth_maps` in
`packages/orchestration/ui_server.py` folds a task's changes to one apply label
with a MEMBERSHIP test — `if "applied" in apply_states` — so a task holding eight
changes of which ONE applied reports `applied`, indistinguishable from a task all
eight of which applied. Three lines above it, in the same loop and over the same
list, the PROOF fold uses an AGREEMENT test and reserves a distinct `incomplete`
state for the mixed case. One fold models partial truth and the fold beside it
does not.

WHY IT IS F033's: hunk-level approval makes the mixed case the NORMAL case, so
this fold moves from understating a rare state to misreporting the state this
feature exists to produce.

THE TWO HALVES MUST MOVE TOGETHER, and the reviewer measured why. The single
consumer of that map is the dashboard task payload's `apply_status` at
`ui_server.py`, and it reaches the UI as `RemedyTaskItem.applyStatus`.
`apps/ui/src/components/detail/DetailPopover.tsx`'s `applyStatus` helper maps
exactly `applied`, `reverted` and `not_applied` to labels and ENDS IN
`return UNKNOWN;`. So a new value emitted by the fold ALONE would render as
"Unknown" — replacing a confident wrong answer with an uninformative one, which
is not a repair. The fold and the label land in ONE commit.

R-0738 STAYS OPEN AT THE END OF THIS ROUND, and the block says so rather than
letting a `Landed:` line imply otherwise. Its resolution condition names THREE
surfaces — the viewer badge, the task-node glyph and the report line — and this
round delivers the TRUTH plus the detail-popover label. Write NO `Landed:` line
for it. The next round takes the remaining surfaces, and the plan says so.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 15 verdict, the R-0744 resolution and the R-0745 registration
  into `.agent/live_review.md`
- C3 one dated prose slip into `.agent/prose_slips.md`
- C4 the agreement fold and the detail-popover label — ONE commit, because the
  fold alone renders the new state as "Unknown"
- C5 the tests for both halves
- C6 the handback

You write NO `Done:` paragraph — `Done:` is the reviewer's word — and NO
`Landed:` line at all this round, for the reason stated above.

## Change set — these paths and nothing else

    .agent/authored/f033-r16.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/ui_server.py
    apps/ui/src/components/detail/DetailPopover.tsx
    tests/ui_server/test_dashboard_cockpit_truth.py
    tests/ui_contracts/test_apply_state_partial.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r16.md` and
`tests/ui_contracts/test_apply_state_partial.py`. This round does NOT touch
`packages/orchestration/proof_chain.py`,
`packages/orchestration/hunk_decision_record.py`,
`packages/orchestration/hunk_ledger.py`,
`packages/orchestration/evidence_index.py`, `apps/cli/command_catalog.py`,
`apps/cli/commands/patch.py`, `apps/cli/grouped.py`,
`tests/ui_server/test_command_channel.py`,
`tests/ui_server/test_command_dispatch.py`, `apps/ui/src/api/types.ts`,
`apps/ui/src/api/remedyApi.ts` or `docs/roadmap/STATUS.md`. `.agent/context.md`
is deliberately NOT touched.

## SPEC — `packages/orchestration/ui_server.py`

An EDIT that REPLACES the apply fold inside `_task_truth_maps` and changes
NOTHING else in the file. The proof fold three lines above it is UNTOUCHED and
G6 measures that.

The apply fold becomes an AGREEMENT test with a distinct mixed state, taking the
same shape as its proof-fold neighbour. Over
`apply_states = [getattr(c, "apply_state", "") for c in changes]`:

1. every state equal to `"applied"` → `"applied"`;
2. else every state equal to `"reverted"` → `"reverted"`;
3. else NO state equal to `"applied"` and NONE equal to `"reverted"` →
   `"not_applied"`. This arm deliberately also absorbs the empty string the
   `getattr` default can produce, exactly as the old `else` did — a change whose
   `apply_state` attribute is missing is not evidence that anything was applied.
4. else → `"partial"`.

THE THREE OLD ANSWERS ARE PRESERVED EXACTLY where they were right, and G6 proves
it by exercise: all-applied still reads `applied`, all-reverted still reads
`reverted`, all-not_applied still reads `not_applied`. ONLY the mixed case moves,
from a membership-driven `applied` to `partial`. Say that in a comment, and name
finding R-0738 and the proof fold beside it as the shape being copied.

`grouped` never holds an empty list, because it is built by `setdefault(...).append(...)`,
so arm 1 cannot be vacuously true. State that in the comment rather than adding a
guard for a case the construction excludes.

The `apply_status` default at the dashboard payload — `task_apply_map.get(tid, ...)`
— is UNCHANGED. A task absent from the map is a different question from a task
whose changes disagree.

## SPEC — `apps/ui/src/components/detail/DetailPopover.tsx`

An EDIT that ADDS ONE branch to the `applyStatus` helper and changes nothing
else. `"partial"` maps to a label that reads as PARTIAL to an operator and is
distinct from all three existing labels and from `UNKNOWN`. Keep the file's
existing branch idiom exactly — one `if` per value, in the order the backend can
emit them.

Put the one-line WHY above the helper, in the file's own comment voice: a task
whose changes disagree is a real state that this feature makes normal, and
rendering it as "Applied" or as "Unknown" both tell the operator something untrue.

Do NOT touch `apps/ui/src/api/types.ts` or `apps/ui/src/api/remedyApi.ts`:
`applyStatus` is already typed `string | undefined` and `remedyApi.ts` passes the
backend value through unexamined, so no new field and no type change is needed.
The reviewer measured that; if you find otherwise, STOP and say so.

## SPEC — `tests/ui_server/test_dashboard_cockpit_truth.py`

An EDIT that ADDS. Every existing test stays untouched and must still pass —
that is the proof the three preserved answers really are preserved.

Before writing, READ the existing `_task_truth_maps` tests in this file and
follow their idiom for building a proof chain; do not invent a second one.

Add tests, each pinning ONE property: a task whose changes are ALL `applied`
still reads `applied`; ALL `reverted` still reads `reverted`; ALL `not_applied`
still reads `not_applied`; a MIXED task — some `applied`, some `not_applied` —
reads `partial` AND NOT `applied`, which is the discriminator for the whole
finding; a task with one `applied` and one `reverted` also reads `partial`; and a
change whose `apply_state` attribute is missing does not by itself produce
`applied`. Assert the value that is EXPECTED, not merely that it differs.

## SPEC — `tests/ui_contracts/test_apply_state_partial.py`

A NEW FILE. Before writing it, READ two existing files under `tests/ui_contracts/`
and follow their idiom for locating and reading a source file under
`apps/ui/src`; do not invent a third.

It pins the TWO ENDS of the seam against each other, which is the only thing that
makes the pair honest:

- `packages/orchestration/ui_server.py` really can emit `"partial"` from the apply
  fold — assert against the source, not against a recollection;
- `apps/ui/src/components/detail/DetailPopover.tsx` really maps `"partial"` to a
  label, and that label is NOT the `UNKNOWN` fallback and is distinct from the
  labels for `applied`, `reverted` and `not_applied`;
- every apply value the backend fold can emit has a branch in that helper. Derive
  the emitted set from the SOURCE of the fold rather than restating it, so the
  test fails when a future value is added on one side only. If deriving it
  mechanically is not possible, say so in a comment and pin the four values
  explicitly — but try the derivation first.

Strip comments before asserting a token is present, per this repository's
existing contract-test practice: a token a comment MENTIONS is not a token the
code USES.

## The slices

<<<SLICE PLANF033R16
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

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
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | done | rounds 14, 15 |
| the write door's exposure and dispatch | done | round 15 |
| T003 partial apply truth, and its first surface | open | this round, R-0738 |
| T003 the node glyph and the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0745, the door's transitive import closure | open | with the next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0738's truth half: the apply fold in `ui_server._task_truth_maps` becomes an
   AGREEMENT test with a distinct `partial` state, taking the shape of the proof
   fold three lines above it, and the detail popover gains the matching label in
   the SAME commit — the fold alone would render the new state as "Unknown".
   R-0738 STAYS OPEN: its resolution names three surfaces and this reaches one.
2. Then the remaining two surfaces R-0738 names — the task-node glyph and the
   report line — and only then is R-0738 resolvable.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof the feature file calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The apply fold has one consumer but three downstream surfaces; a value added on
  one side only renders as "Unknown", which is why the contract test pins both ends.
<<<END PLANF033R16

<<<SLICE RECORDF033R16
Gate: F033 R15 — THE WRITE DOOR, AND R-0744. THE ROUND PASSED. Every gate was re-executed by the reviewer at `1329ef45` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 32348 bytes at sha256 `92c6e6c8…de170`, EQUAL to the reviewer's own scratchpad original, with ONE blob id across `.agent/authored/f033-r15.md` and `.agent/last_block.md` at C0b. THE RECORD APPEND at `bd83cedb` reconstructs 1526301 plus one newline plus 7431 to 1533733, the committed blob exactly, base a byte PREFIX, N COUNTED at 3, the last three blank-line units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1528162 — proved to lie inside the FIRST appended paragraph, spanning 1526302 to 1530022 — rejected by BOTH readers. THE LEDGER walked at three commits: registered 304 to 305 with the ADDED id exactly `R-0744`; `Done:` 48 lines over 46 distinct to 49 over 47 with the ADDED resolved id exactly `R-0743` and the `Landed: R-0743` line STILL PRESENT beside its new `Done:` paragraph; `Landed:` 16 at BASE and C2 and 17 at C3 with `^Landed: R-0744 — ` exactly 1; `Gate:` 131 to 132 with `^Gate: F033 R14 — ` exactly 1; `DECISION F033 D` 4 UNMOVED; and the open set 258 at ALL THREE, one id added and one resolved. THE PLAN is byte-EQUAL to its slice at 2422 bytes over 45 lines. THE R-0744 FIX is on disk at `54b569cb`: `resolve_job_evidence_dir(str(job_id))` occurs once and the raw-argument form zero times. THE DOOR'S GUARDS: the reviewer re-ran `_door_imports` ITSELF over the C4 source with the C4 `DOOR_METHODS` and collected 23 pairs, the set difference against `ALLOWED_IMPORTS` EMPTY IN BOTH DIRECTIONS and the intersection with `FORBIDDEN_MODULES` empty; every name in `DOOR_METHODS` answers to a real `_RemedyHandler` method, so the guard scans what it claims to; `UI_EXPOSED_COMMANDS` gains exactly `patch.approve-hunks`; and `FORBIDDEN_MODULES` gains exactly `packages.orchestration.hunk_apply`, which nothing imports and which is the point. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `e24d3b44` with its OWN anchors, each asserted UNIQUE, the import proved to resolve inside the worktree and every file restored byte-identically: controls 13, 12 and 106 at REAL exit 0; reverting the R-0744 fix is exit 1 at 2 failed naming BOTH discriminating tests; dropping `save_job` from the door is exit 1 at 2 failed; and removing the id from the exposed set is exit 1 at 6 failed. THE REVIEWER ALSO RAN A MUTATION THE BLOCK NEVER ORDERED, to test the worker's own declared deviation D1 rather than take it on trust: making the hunk 409 reuse the decision message goes RED at exactly `test_every_exposed_command_reaches_the_answer_its_effect_gives`, so the widened test really does pin the two 409s apart and the edit STRENGTHENED the guard. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: `test_patch_cmd.py` 13, `test_command_dispatch.py` 12, `test_command_channel.py` 106, `test_command_catalog.py` 18, `test_evidence_index.py` 33, `test_hunk_decision_record.py` 15 and the canary 42, with `ruff` over all six touched files exiting 0. THE STRUCTURE: seven single-parent commits of 439, 291, 17, 6, 80, 157 and 189 insertions, every one under 500; the path set EQUALS the declared change set in BOTH directions; and ALL TWELVE do-not-touch paths byte-identical by blob id. THE WORKER DECLARED FOUR DEVIATIONS AND EVERY ONE IS HONEST; D1 is a defect in the REVIEWER's block, which enumerated four equality-shaped guards over the door where there are five, and it is recorded as a prose slip rather than an id because the worker's repair left nothing wrong on disk.

Done: R-0744 — RESOLVED at `54b569cb`, verified by the reviewer running the mutation the finding's FIX clause asked for rather than by reading the diff. `_cmd_approve_hunks` now calls `evidence_index.resolve_job_evidence_dir(str(job_id))` with the `UUID` that `resolve_job_id` returned, so the canonical lowercase hyphenated form reaches the index whatever the operator typed; the raw-argument form occurs zero times in that file at that commit. THE PROOF IS THE COLOUR CHANGE, and it is sharper than a pass: at `fa963c4e` the reviewer APPLIED this fix inside a disposable worktree and all eleven tests stayed GREEN, so the suite was blind to the defect; at `e24d3b44` REVERTING it goes RED at exit 1 and 2 failed, naming `test_a_short_hex_prefix_records_exactly_as_the_full_id_does` and `test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does`. Two tests that did not exist now discriminate the two id forms, and they assert the RECORDED state rather than the exit code, so a handler that recorded under the wrong key would still fail them. The defect was the reviewer's own SPEC and the round 14 worker was right to apply it literally and declare the consequence; this resolution reaches that one call site and claims nothing about any other handler in the file.

- R-0745 — Low, THE DOOR'S IMPORT GUARD READS DIRECT IMPORTS ONLY, AND THE DOOR'S TRANSITIVE CLOSURE NOW REACHES `subprocess` WHERE AT THE PREVIOUS COMMIT IT REACHED NO FORBIDDEN MODULE AT ALL. Raised by the reviewer at the F033 R15 gate by a measurement no gate ordered. `TestCommandDoorImportGuard._door_imports` in `tests/ui_server/test_command_channel.py` walks the door methods' own AST and collects DIRECT imports, which is what lets it be an equality guard at all; `FORBIDDEN_MODULES` then forbids a set that includes `subprocess` and `shutil` under the comment "the applicators and the shell/filesystem writers the P3 contract exists to keep out of an HTTP handler". MEASURED by walking the module-level import graph from the door methods' own imports, at `fa963c4e` and at `1329ef45`: at the first, NO member of `FORBIDDEN_MODULES` is reachable at all; at the second, `subprocess` is, through `packages/orchestration/evidence_index.py`, which imports it at module level for the `_git` and `_git_raw` helpers, and the door began importing that module this round for `resolve_job_evidence_dir` — which never calls either helper. THE REAL APPLIERS ARE ABSENT AT BOTH COMMITS — `hunk_apply`, `source_apply`, `patch_apply`, `diff_repair_apply`, `job_fulfillment`, `exec_guard`, `workspace` and `secure_fs` are all unreachable — so DECISION F033 D4's own claim that the door drags no applier behind it HOLDS, and this finding does not contradict it. What moved is the shell-capability half of the same boundary. WHY LOW: nothing is wrong on disk, no door method can shell out, and `resolve_job_evidence_dir` is a pure filesystem read; the defect is that a guard whose stated purpose is keeping shell writers out of an HTTP handler cannot see the reach it now has, so a later edit inside `evidence_index` could hand the door shell capability with no guard firing. FIX, either half of which discharges it: move the `subprocess` import in `packages/orchestration/evidence_index.py` from module level into the two helpers that use it, which restores the base property exactly; or add to `TestCommandDoorImportGuard` a test that walks the transitive module-level closure from the door's own imports and asserts the intersection with `FORBIDDEN_MODULES`, recording whatever set is then accepted. The second is the more durable of the two because it measures the property rather than one instance of it, and the reviewer recommends it; the first is a one-line change and may be taken as well.
<<<END RECORDF033R16

<<<SLICE SLIPSF033R16
2026-08-29 · F033 R15 · The block's "Why this round exists" enumerated the equality-shaped guards over the write door as `UI_EXPOSED_COMMANDS`, `DOOR_METHODS`, `ALLOWED_IMPORTS` and `FORBIDDEN_MODULES`, and its SPEC then said nothing else in `tests/ui_server/test_command_channel.py` would change; a fifth guard, `TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives`, iterates the exposed set and hard-branched every non-`job.stop` id to one 409 message, so the worker had to widen it to a per-id map and declared the disagreement, which is the required behaviour — the reviewer confirmed by mutation that the widened form pins the two 409 messages apart and weakens nothing.
<<<END SLIPSF033R16

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them; C6's own numbers are NOT
ordered here.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r16.md` and of `.remedy-wt/f033-r16-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r16.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1535259 bytes, plus one newline plus RECORDF033R16 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R16 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the open set at
  both. Ordered: registered 305 to 306 with the ADDED id exactly `R-0745`;
  `Done:` 49 lines over 47 distinct to 50 over 48 with the ADDED resolved id
  exactly `R-0744`, and the `Landed: R-0744` line STILL PRESENT beside its new
  `Done:` paragraph; `Landed:` 17 UNMOVED at BOTH — this round writes no
  `Landed:` line at all; `Gate:` 132 to 133 with `^Gate: F033 R15 — ` exactly 1;
  `DECISION F033 D` 4 UNMOVED; and the open set 258 at BOTH. Report that
  equality explicitly rather than inferring it, and report that `^- R-0738 — `
  is still 1 and `^Done: R-0738 — ` still 0 at C2 — this round does NOT resolve it.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R16 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  24266 bytes, plus one newline plus SLIPSF033R16, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching
  `^2026-\d\d-\d\d · F033 R15 · ` at BASE, which must be 0, and at C3, and the
  count of lines beginning `- R-` in the whole file at C3, which must be 0.
- **G6 THE FOLD AND THE LABEL at C4.** (a) `ruff check` over
  `packages/orchestration/ui_server.py` and the two touched test paths exits 0 —
  report the summary line. (b) EXERCISE the shipped `_task_truth_maps` DIRECTLY,
  not through the tests, over hand-built change objects, and report the label it
  returns for each of: all `applied`; all `reverted`; all `not_applied`; three
  `applied` and five `not_applied`; one `applied` and one `reverted`; and one
  whose `apply_state` attribute is ABSENT beside one `applied`. The first three
  must read `applied`, `reverted` and `not_applied` — UNCHANGED from BASE, and
  report the BASE reading for the same six inputs beside the C4 reading. The
  fourth and fifth must read `partial`. (c) Report the PROOF fold's source lines
  at BASE and at C4 and confirm they are byte-identical — only the apply fold
  moves. (d) Report the set of literal apply labels the C4 fold can assign, and
  the set of values `DetailPopover.tsx`'s `applyStatus` helper branches on at
  C4, and their difference IN BOTH DIRECTIONS, which must be empty. (e) Report
  the label the helper returns for `"partial"` and confirm it differs from the
  `UNKNOWN` fallback and from the other three labels.
- **G7 THE MUTATION RED-PROOFS at C5.** In a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROLS — REAL
  exit 0 with counts — over `tests/ui_server/test_dashboard_cockpit_truth.py`
  (33 at BASE) and `tests/ui_contracts/test_apply_state_partial.py`. Then, one
  at a time, reverting fully between each, asserting the anchor is UNIQUE inside
  the named FILE before replacing it, and reporting the REAL exit code, the
  failure count and the NAME of each failing test:
  (i) in `packages/orchestration/ui_server.py`, restore the MEMBERSHIP test —
      `if "applied" in apply_states` — as the first arm of the apply fold;
  (ii) in `packages/orchestration/ui_server.py`, make the mixed arm return
      `"applied"` instead of `"partial"`;
  (iii) in `apps/ui/src/components/detail/DetailPopover.tsx`, delete the
      `"partial"` branch so the helper falls through to `UNKNOWN`.
  Each MUST go RED. Mutation (iii) proves the CONTRACT test really reads the
  TypeScript; if it comes back GREEN the contract test is not doing its job —
  report that plainly and do NOT adjust anything to force a red. Remove the
  worktree BY EXACT PATH, then `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/ui_server/test_dashboard_cockpit_truth.py`
  (33 at BASE), `tests/ui_contracts/test_apply_state_partial.py`,
  `tests/ui_contracts/` as a whole, `tests/ui_server/test_command_channel.py`
  (106 at BASE), `tests/cli/test_patch_cmd.py` (13 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C5`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. Report the range's path set against
  the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/ui_server.py` and
  `apps/ui/src/components/detail/DetailPopover.tsx`: each 0, against
  `.agent/authored/f033-r16.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C5, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 4,
round 16, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Write external actions as command plus outcome. Quote the shipped
apply fold in full, the six readings from G6(b) side by side with their BASE
readings, the label the helper returns for `"partial"`, and the test names you
wrote with the property each pins.

Carry SESSION 4 forward and name the next session's first actions in this order:
read `.agent/STOP` from disk, then run the Open PR Gate, then book this round's
verdict, then the plan's step 2 — the two surfaces R-0738 still names. No length
cap. Write no verdict on your own work.
