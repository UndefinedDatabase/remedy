# STEP 22 — F033 Hunk-level diff approval (SESSION 6, round 22 of a 25-round soft limit)

Goal: repair the false clause round 21 left in `pingpong_loop.py`, and ship the
inverse of `export_hunk_ledger` so a decision already STORED on a job can be
rebuilt into the ledger the rejection renderer consumes.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r22.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN22.
4. C2: append slice RECORD22 to `.agent/live_review.md`. It books the round 21
   PASS and REGISTERS finding R-0747. Per operator amendment amend0827 rule 1
   neither buys a round of its own; this round is happening anyway.
5. C3: SPEC A — repair R-0747 in `packages/orchestration/pingpong_loop.py`, and
   in the SAME commit append the `Landed: R-0747` line described in SPEC A3.
6. C4: SPEC B — `import_hunk_ledger` in `packages/orchestration/hunk_ledger.py`.
7. C5: SPEC C — append the tests to `tests/orchestration/test_hunk_ledger.py`.
8. C6: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r22.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_loop.py
    packages/orchestration/hunk_ledger.py
    tests/orchestration/test_hunk_ledger.py
    .agent/handoff.md

`.agent/prose_slips.md` is deliberately NOT in the change set. The reviewer error
this round repairs damaged state on disk under `packages/`, so under operator
amendment amend0827 rule 2 it spends an ID and is not a slip, and rule 2 forbids
booking one defect in both places.

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `0bcae480`, this round's base.

- `packages/orchestration/hunk_decision_record.py` line 226 reads
  `records = job.metadata.setdefault(HUNK_DECISIONS_METADATA_KEY, {})` and line
  227 assigns `records[attempt_key] = exported`. `HUNK_DECISIONS_METADATA_KEY`
  is the literal `"hunk_decisions"`. So the module DOES write the record onto
  the job object.
- `packages/orchestration/ui_server.py` line 3940 calls `save_job(job)` in
  `_dispatch_approve_hunks`, whose own docstring says the door "RECORDS and
  PERSISTS it". `apps/cli/commands/patch.py` reaches the same recorder.
- Therefore a recorded decision IS durable, and round 21's claim that there is
  "no route from a stored decision to the loop" is FALSE. That is R-0747.
- The stored shape is `job.metadata["hunk_decisions"][attempt_key]`, a mapping
  with keys `task_id`, `attempt`, `decided_at` and `hunks`, where `hunks` is the
  list `export_hunk_ledger` produces: one object per entry with exactly the keys
  `id`, `state`, `reason` and `landing`, all plain strings.
- `render_rejection_findings` reads `entry.hunk_id`, `entry.state` and
  `entry.reason` off objects. The stored rows are MAPPINGS keyed `id`, not
  `hunk_id`, so nothing today can feed stored rows to the renderer. That gap,
  and not the absence of storage, is what the next round needs closed — which is
  why this round ships the inverse rather than a call site.
- `run_pingpong` takes `job_id` and `task_id` among its parameters, so the job
  is reachable from the loop. Wiring that is NOT this round.
- `tests/orchestration/test_hunk_ledger.py` exists at 298 lines and already
  imports and exercises `export_hunk_ledger`. The new tests append to it,
  because this repository names a test file after the source it covers.

## SPEC A — the R-0747 repair in `packages/orchestration/pingpong_loop.py`

Described, not sliced.

A1. In `compose_builder_prompt`'s docstring, the paragraph beginning "Remedy
deliberately does NOT supply this parameter from the run loop yet" currently
ends with a clause asserting that `hunk_decision_record.py` "builds the ledger
and persists NOTHING, so there is as yet no route from a stored decision to the
loop". REPLACE that false reason. Keep the true half — the call site is
unchanged and `hunk_ledger` is therefore always `None` in production.

A2. The replacement states, in the module's own idiom, ONLY what the reviewer
measured at `0bcae480` and what stays true after this round: a recorded decision
IS stored, on `job.metadata` under the key `hunk_decisions`, keyed by attempt and
made durable by `save_job` at the write door; what is missing is the wiring at
the call site, which is its own round. Do NOT restate the byte offsets or line
numbers above — name the module and the key, which survive an edit, rather than
a line number, which does not.

A3. In the SAME commit, append to `.agent/live_review.md` exactly one line:

    Landed: R-0747 — the false no-stored-decision clause is replaced by the measured storage route, packages/orchestration/pingpong_loop.py, C3 of round 22.

Write NO `Done:` paragraph. `Done:` is reserved for reviewer-authored text, and a
worker-authored one is a finding however honestly it is hedged. The reviewer
replaces this `Landed:` line with an authored resolution at the next gate.

## SPEC B — `import_hunk_ledger` in `packages/orchestration/hunk_ledger.py`

B1. Add one public function, the INVERSE of `export_hunk_ledger`, taking the
exported mapping and returning a `HunkDecisionLedger`. Place it directly after
`export_hunk_ledger` so the pair reads together, and add its name to the module
docstring's `Public API::` block in the SAME commit — R-0746 is on this branch's
record precisely because a public function was added and that list was not.

B2. It reads the rows under the existing root key, and per row the existing four
entry keys, reusing `_EXPORT_ROOT_KEY` and `_EXPORT_ENTRY_KEYS` rather than
restating either spelling. A row's `id` becomes the entry's `hunk_id`; that
rename is the whole reason a caller cannot hand stored rows straight to a
renderer, so state it in the docstring.

B3. TOTAL, like every public name in this module: it NEVER raises, on any input
at all — `None`, a non-mapping, a mapping with no rows key, a non-iterable rows
value, a row that is not a mapping, a row missing any key.

B4. THE STRUCTURAL GUARD IS SINGULAR AND LOAD-BEARING. Anything unreadable
yields an EMPTY ledger, never a partially built one, for the reason
`hunk_repair_findings.render_rejection_findings` already gives for returning the
empty string: a half-built result's missing half is invisible to whoever reads it
next. Do NOT add a second defensive layer inside that guard — a redundant inner
layer makes the outer one unobservable and G6(ii) would then redden nothing.
`_total_text` remains the SEPARATE coercion guard and covers the four field
values, exactly as `export_hunk_ledger` already uses it; say in the docstring
which of the two each red-proof is aimed at.

B5. ROUND-TRIP. For any ledger `build_hunk_ledger` produces,
`import_hunk_ledger(export_hunk_ledger(ledger))` equals that ledger. Both
dataclasses are frozen, so equality is structural and the test asserts `==`
directly rather than field by field.

B6. Remedy deliberately does NOT validate that `state` is one of the three
`HUNK_STATE_*` values or that `landing` is one of the three `HUNK_LANDING_*`
values. Document this where a reader would search for it. Importing is not the
layer that decides whether a decision is coherent — `hunk_approval.py` is — and a
row carrying an unknown state is reproduced as it was stored so the fault stays
visible instead of being silently normalised into a valid-looking one.

## SPEC C — tests appended to `tests/orchestration/test_hunk_ledger.py`

APPEND ONLY. Do not edit, reorder or reflow one existing line: the pre-commit
blob must be a byte-exact PREFIX of the post-commit file. Add the new import to
the existing import block only if that block is inside the appended region;
otherwise import inside the new tests. Cover at least:

C1. The round-trip of B5, over a ledger holding an approved, a rejected and a
pending entry, asserting `==` on the whole ledger.
C2. A rejected entry's reason survives the round trip BYTE FOR BYTE, using a
reason with leading spaces, an interior blank line, a tab and a trailing newline.
C3. `render_rejection_findings(import_hunk_ledger(stored_rows))` reproduces that
reason verbatim — the property that makes the stored form usable at all.
C4. Totality: each of the malformed inputs B3 names returns an empty ledger and
raises nothing. Parametrize; do not write one test per input by hand.
C5. Order is preserved: three entries import in the order they were exported.
C6. B6's absence: a row whose `state` is an unknown string imports with that
string intact rather than being normalised or dropped.

## Slice PLAN22 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file. PLAN22's own body contains `##` headings, which is why the
markers exist.

<<<BEGIN PLAN22
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 6 of this feature.

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
| one evidence-directory resolver, the CLI door, the write door | done | 13-15 |
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| rejections rendered verbatim as repair findings | done | round 20 |
| that renderer reaches the builder prompt as a segment | done | round 21 |
| R-0747, and the inverse of the ledger export | open | this round |
| the loop SUPPLIES a stored ledger, and the two-round end-to-end | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. This round repairs R-0747 and ships `import_hunk_ledger`, the inverse of
   `export_hunk_ledger`. A decision IS stored — on `job.metadata` under
   `hunk_decisions`, persisted by `save_job` at the write door — but its rows
   are mappings keyed `id`, so nothing could rebuild a ledger from them.
2. Then the supply: read that key in the run loop and pass the rebuilt ledger to
   `compose_builder_prompt`, which has taken the parameter since round 21. That
   step also carries the two-round end-to-end the Acceptance asks for.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- Steps 2, 3 and 4 are more rounds than the 25-round soft limit leaves. The
  scope report operator amendment amend0827 rule 6 requires is now likely.
<<<END PLAN22

## Slice RECORD22 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated. The slice is every byte between the
markers, exclusive.

<<<BEGIN RECORD22
Gate: F033 R21 — REJECTED HUNKS REACH THE BUILDER PROMPT AS A STEERING SEGMENT. THE ROUND PASSED, AND THE REVIEWER'S OWN BLOCK PUT ONE FALSE SENTENCE ON DISK, REGISTERED BELOW AS R-0747. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the reviewer reached at `0bcae480`; it is written into this record by the first commits of the next round rather than by a round of its own. All eight gates were re-executed by the reviewer from scripts of its own and every ordered reading reproduced. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r21.md` against the reviewer's own pre-emission original `.remedy-wt/f033-r21-block.md` was SILENT, as was the same comparison against `.agent/last_block.md`, and the source file's sha256 at review time is `105c5c4d…ad60432` over 21541 bytes, the digest the reviewer computed BEFORE delegating. This round's chain is stronger than the usual one and the difference is worth recording: the worker did not RETYPE the block, it copied the reviewer's own file with `shutil.copyfile`, so one end of the comparison is the emitted artefact itself rather than a third artefact of the worker's. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to slice PLAN21 at 2509 bytes over 45 lines, under the 50-line cap, holding `## Goal` and the substring `Steps` that `tests/ui_server/test_dashboard_contract.py::test_plan_md_references_current_steps` asserts; `.agent/prose_slips.md` reconstructs 29663 plus one newline plus 1143 to 30807. THE RECORD APPEND at `e0c9ce2d` reconstructs 1575558 plus one newline plus 4635 to 1580194, base a byte PREFIX, slice an exact SUFFIX, the separator byte a newline, N COUNTED at 1 by the reviewer's own script, and a negative control at byte 1577104 — an offset the reviewer chose independently of the worker's 1577876, both proved inside the FIRST appended paragraph's span 1575559 to 1580193 — REJECTED by both readers run independently, each of which accepted the unflipped bytes. THE LEDGER: registered 307 distinct UNMOVED; `Done:` 52 lines over 50 distinct UNMOVED; `Landed:` 18 lines over 15 distinct UNMOVED; `^Gate: F033 R20 — ` 0 before and exactly 1 after; and the open set 257 UNMOVED, exactly as ordered for a round resolving nothing. THE CODE AGAINST THE SPEC: `python3 -m ruff check` exits 0 over both changed files; by AST both `compose_builder_prompt` and `_build_builder_prompt` carry `hunk_ledger` as the LAST keyword-only parameter defaulting to `None`, the `render_rejection_findings` import resolves, and there are ZERO `Compare` nodes anywhere in the module with `hunk_ledger` as the left operand — which is how SPEC A4's single-guard rule is measured rather than asserted. THE MUTATIONS were re-run by the reviewer in its own disposable worktree with its OWN anchors, each asserted UNIQUE and the file restored and proved byte-identical to the committed blob after each: the unmutated control is a REAL exit 0 at 35 passed; removing the emptiness guard is exit 1 at 9 failed, reddening SIX golden tests including `test_the_full_shape_registers_the_ten_segments_in_rank_order` and three new-file tests; registering the segment after the directive instead of before it is exit 1 at 10 failed including both position tests; and stripping the rendered text is exit 1 at exactly 4 failed, every one a raw-substring test. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the new file 14, the golden 21, the cache prefix 16, the renderer 17, `test_pingpong_cli.py` 172, `test_repair_loop.py` 131 and the canary 42. THE STRUCTURE: eight single-parent commits over `98ce168e`..`0bcae480` of 300, 298, 13, 2, 4, 55, 338 and 474 insertions, every one under 500 — the last of those being the handback commit, which no gate of the block could reach and which the reviewer measured here instead, as checklist items 14 and 31 require; and the path set over the range to C5 EQUALS the declared change set in BOTH directions, the whole range adding only `.agent/handoff.md`. THE WORKER DECLARED SEVEN DEVIATIONS AND EVERY ONE IS HONEST. D1 is the best of them: the worker's own self-review caught a `:func:` cross-reference to `run_pingpong_loop` in its draft and corrected it to `run_pingpong` before committing, and the reviewer confirms by AST that `compose_builder_prompt`'s only callers are `_build_builder_prompt` and `run_pingpong` and that no function of the other name exists. D5 reports that mutation (i) reddened three tests beyond the six the block predicted, which the reviewer reproduced exactly — more red than ordered is a stronger result, and declaring it rather than folding it into "as expected" is the correct instinct. D4 answers the R20 handback's open question directly: `git worktree remove` was tried WITHOUT `--force` and succeeded, so the flag is not necessary for this workflow, and the reviewer independently removed its own worktree the same way.

- R-0747 — Low, `packages/orchestration/pingpong_loop.py` DOCUMENTS A FALSE REASON FOR A TRUE ABSENCE: IT SAYS NO STORED HUNK DECISION EXISTS TO READ, AND ONE DOES. Raised by the reviewer at the F033 R21 gate, from a measurement no gate of that block ordered, and registered as an ID rather than a prose slip because the wrong state is on disk under `packages/` and the next reader meets it — the same reading that produced R-0746 on this branch. `compose_builder_prompt`'s docstring, landed at `06443151`, states that the run-loop call site is unfed because `packages/orchestration/hunk_decision_record.py` "builds the ledger and persists NOTHING, so there is as yet no route from a stored decision to the loop". The first half has a true and narrow meaning that the F033 R11 gate entry already measured — that MODULE performs no storage I/O, `open(` and `save_job` both reading 0 in it — and the second half does not follow from it and is false. MEASURED by the reviewer at `0bcae480`: `hunk_decision_record.py` line 226 reads `records = job.metadata.setdefault(HUNK_DECISIONS_METADATA_KEY, {})` and line 227 assigns `records[attempt_key] = exported`, with that key the literal `hunk_decisions`; `packages/orchestration/ui_server.py` line 3940 then calls `save_job(job)` inside `_dispatch_approve_hunks`, whose own docstring reads "this door RECORDS and PERSISTS it"; and `apps/cli/commands/patch.py` reaches the same recorder. A decision is therefore durable the moment either door returns. WHY LOW: no behaviour is wrong, no gate is blind, every test passes, and the ABSENCE the paragraph documents is real — the call site genuinely is unchanged and `hunk_ledger` genuinely is always `None` in production. The defect is confined to the stated REASON for that absence. WHY IT IS NOT HARMLESS: it is a positive false statement rather than an omission, it sits in the exact paragraph the next round must read, and `.agent/plan.md` repeated it as "the round after this one must first locate where a recorded decision is stored" — so the defect was on course to spend a round hunting for storage that already existed. THE FAULT IS THE REVIEWER'S, NOT THE WORKER'S: the R21 block asserted the same false consequence in its own "what the reviewer measured" section, and SPEC A5(i) ordered the absence documented with the reason left in the worker's wording, so the worker rendered faithfully what it was given. The reviewer read `hunk_decision_record.py`'s docstring, which truthfully says it imports no storage, and inferred that nothing was stored without reading the function body or either door — an inference presented as a measurement, which is the one move this record exists to catch. FIX: replace the false clause with the measured storage route, naming the module and the `hunk_decisions` key rather than a line number, and keep the true half about the call site. Resolved when the paragraph states only what a reader can verify, and when `.agent/plan.md`'s step for the following round names reading that key rather than locating storage.
<<<END RECORD22

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it as written
   and declare the problem in the handback; never silently repair it.
2. PLAN22 is a FULL REWRITE. RECORD22 is an APPEND: measured by the reviewer at
   `0bcae480`, `.agent/live_review.md` is 1580194 bytes and ends with a newline,
   so the append is one blank-line separator then the slice.
3. `.agent/live_review.md` is written by TWO commits this round — C2 appends
   RECORD22, C3 appends the single `Landed:` line of SPEC A3. G3's arithmetic is
   measured at C2 and G4's ledger readings at C3, and neither is stated over the
   final state, because that state does not exist when either is written.
4. The append to `tests/orchestration/test_hunk_ledger.py` is a CODE append, so
   the obligation is ORDERED EQUALITY and never a per-line count: the pre-commit
   blob is a byte-exact PREFIX, and the lines the commit's diff ADDS are exactly
   the appended lines IN ORDER. Code repeats blank lines and closing parentheses
   structurally, so a uniqueness count over added lines is unattainable here.
5. Touch no path outside the change set. In particular do not touch
   `.agent/prose_slips.md`, `.agent/context.md` or anything under `docs/`.
6. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, and process substitution. Use one command per call, `git -C`,
   `python3 -c` or a script file under `.remedy-wt/`, and `python3 -m ruff`.
   A gate's REAL exit code is captured as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`
   with NO PIPE in it — a piped form reports the exit of the last pipeline
   stage and is a gate that cannot fail.
7. Destructive verification runs ONLY in a disposable `git worktree`, purged of
   `__pycache__` and run under `python3 -B`. The primary checkout satisfies
   `git status --porcelain` empty at the handback.
8. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
9. G1 through G8 all run at C5, before the handback commit C6, so C6 can quote
   every one. C6's own insertion count is not gated; the reviewer measures it.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r22.md`, and `cmp` it against `.remedy-wt/f033-r22-block.md`.
One reading.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN22, under 50 lines, still
holding `## Goal` and the substring `Steps`. Report bytes and lines.

G3 THE RECORD APPEND, measured AT C2. Reconstruct 1580194 plus one newline plus
the byte length of RECORD22 to the committed size at C2. Prove the pre-commit
blob a byte PREFIX and the slice an exact SUFFIX. COUNT N, the slice's
blank-line paragraphs, in the script rather than taking it from this block, and
compare the file's LAST N blank-line units against the slice's paragraphs IN
ORDER. Flip one byte inside the FIRST appended paragraph, report the offset and
prove it lies in that paragraph's span, and show BOTH readers reject the flipped
bytes while both accept the unflipped ones.

G4 THE LEDGER, read at `0bcae480`, at C2 and at C3: registered `^- R-\d+ — `
307 distinct going to 308 with the ADDED id exactly `R-0747`; `^Done: R-\d+ — `
52 lines over 50 distinct UNMOVED at all three; `^Landed: ` 18 going to 19 with
`^Landed: R-0747 — ` exactly 1 at C3 and 0 before it; `^Gate: F033 R21 — ` 0
before and exactly 1 after; and the open set 257 going to 258.

G5 THE CODE AGAINST THE SPEC, at C5. `python3 -m ruff check` exits 0 over all
three changed files. By AST: `import_hunk_ledger` is defined at module level in
`hunk_ledger.py` with no leading underscore; its name appears in the module
docstring's `Public API::` block; and `pingpong_loop.py` contains ZERO
occurrences of the string `persists NOTHING`. Show by RUNNING the shipped
function that `import_hunk_ledger(export_hunk_ledger(L)) == L` for a ledger
holding an approved, a rejected and a pending entry.

G6 MUTATION RED-PROOFS, in a disposable worktree at C5. Run the UNMUTATED
CONTROL FIRST over `tests/orchestration/test_hunk_ledger.py` and report its REAL
exit code and pass count beside every mutation. Each anchor is a byte string
shown to occur EXACTLY ONCE in the file it edits; report that count, and restore
the file and prove it byte-identical to the committed blob after each.
  (i) make the round trip lossy — drop the `reason` field when rebuilding an
      entry — and show the verbatim test goes RED.
  (ii) remove SPEC B4's structural guard so a malformed input raises instead of
      yielding an empty ledger; the totality tests must go RED. If this reddens
      nothing, SAY SO — that is a real result about a guard no test reaches, and
      it is the outcome this gate exists to detect.
  (iii) normalise an unknown `state` to `pending` on import; C6's test must go
      RED.
Report the failing test NAMES, not only counts.

G7 THE SUITES, SERIALLY, in the PRIMARY checkout at C5, each with its REAL exit
code and pass count: `test_hunk_ledger.py`; `test_hunk_repair_findings.py`;
`test_hunk_approval.py`; `test_hunk_decision_record.py`;
`test_builder_prompt_hunk_rejections.py`; `test_builder_prompt_golden.py`; and
the canary `python3 -m pytest tests/cli/test_golden_path.py -q`.

G8 STRUCTURE. `git status --porcelain` EMPTY. For every commit from C0a through
C5, report insertions from `git diff --numstat` and show each is under 500. Show
the path set over `0bcae480`..C5 equals the change set above minus
`.agent/handoff.md`, in BOTH directions.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 6 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle and SPEC item, every deviation, and the
next expected action. It has no length cap. If any gate is RED, do not repair on
your own initiative: report it and stop.
