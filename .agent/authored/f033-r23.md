# STEP 23 — F033 Hunk-level diff approval (SESSION 6, round 23 of a 25-round soft limit)

Goal: close the gap between a decision ALREADY RECORDED on a job and the next
builder prompt. A reader selects the task's latest decision from `job.metadata`,
`run_pingpong` forwards the rebuilt ledger, and the operator's rejection reason
is proved to reach the REAL loop's composed prompt.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r23.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN23.
4. C2: append slice RECORD23 to `.agent/live_review.md`. It books the round 22
   PASS and RESOLVES R-0747. Per amend0827 rule 1 neither buys a round of its
   own; this round is happening anyway.
5. C3: SPEC A — `load_hunk_ledger_for_task` in
   `packages/orchestration/hunk_decision_record.py`.
6. C4: SPEC B — `run_pingpong` takes and forwards `hunk_ledger`, in
   `packages/orchestration/pingpong_loop.py`.
7. C5: SPEC C — the tests, appended to two existing files.
8. C6: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r23.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/hunk_decision_record.py
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_hunk_decision_record.py
    tests/orchestration/test_builder_prompt_hunk_rejections.py
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `d0c86c2d`, this round's base.

- `hunk_decision_record.py` writes one record per attempt under
  `job.metadata["hunk_decisions"]`, keyed `f"{task_id}:{attempt}"` by the
  private `_attempt_key`. Each record carries exactly `task_id`, `attempt`,
  `decided_at` and `hunks`.
- `_LEDGER_ROWS_KEY` in that module is the literal `"hunks"`, and its own
  comment says it is deliberately the SAME name `export_hunk_ledger` writes
  under, re-stated because the name is private in `hunk_ledger`. A stored
  record therefore ALREADY has the shape `import_hunk_ledger` reads, and SPEC A
  passes the record straight in rather than re-wrapping its rows.
- That module imports `HunkDecisionLedger`, `build_hunk_ledger` and
  `export_hunk_ledger` from `hunk_ledger` in ONE block, so SPEC A's import adds
  a name to an existing block and no new module dependency at all.
- `open(` and `save_job` both occur ZERO times in that module. The F033 R11
  gate entry records that as the property DECISION F033 D4 leans on, and SPEC A
  must preserve it — which is why it takes a METADATA MAPPING and never a job
  id or a path.
- `run_pingpong` is defined at line 2556 and composes the builder prompt at
  line 2939 into a local named `builder_composed`. `datetime` is already
  imported in `hunk_decision_record.py`.
- `result.prompt_traces` is a list on the loop's result, appended at line 2975
  with `build_trace_entry(..., composed_prompt=builder_composed, ...)`, and
  `prompt_trace.py` derives `segment_manifest` from that composed prompt as a
  list of dicts each carrying a `name`. So a test CAN observe which segments the
  real loop composed, and that is how SPEC C3 proves the end to end.
- `run_pingpong` is driven in `tests/orchestration/test_pingpong.py` as
  `run_pingpong("Fix README", str(demo_repo), builder_name="fake",
  reviewer_name="fake")`. SPEC C3 reuses that shape and that fixture rather than
  inventing a harness.

## SPEC A — `packages/orchestration/hunk_decision_record.py`

Described, not sliced.

A1. Add `import_hunk_ledger` to the EXISTING
`from packages.orchestration.hunk_ledger import (...)` block, in the order ruff's
isort rules want. Do not add a second import statement.

A2. Add one public function taking a METADATA MAPPING and a task id and
returning a `HunkDecisionLedger`: the decision most recently recorded for that
task, rebuilt. Name it so it greps to itself and says what it reads.

A3. SELECTION, stated as ONE rule the docstring gives in full: among the records
whose `task_id` equals the given task id coerced to text, the winner is the one
with the greatest `decided_at` that `datetime.fromisoformat` parses; a record
whose `decided_at` does not parse can never beat one that does; and if none
parses, or several tie, the LAST in the mapping's iteration order wins, which
for a record loaded from JSON is insertion order. Nothing here sorts the ids.

A4. Rebuild by handing the winning record STRAIGHT to `import_hunk_ledger`. Say
in the docstring that this works because `_LEDGER_ROWS_KEY` and the export root
key are deliberately the same name, and that the module's existing comment on
that constant is where the deliberateness is recorded. Do NOT re-implement the
row walk — one inverse, not two.

A5. TOTAL: never raises on any input at all — `None` metadata, a non-mapping,
no decisions key, a non-mapping decisions value, a record that is not a mapping,
a record missing any key. Anything unreadable yields an EMPTY ledger, never a
partial one. THE STRUCTURAL GUARD IS SINGULAR; do not nest a second one inside
it, or the red-proof aimed at it reddens nothing. Say which guard each red-proof
is aimed at, as `import_hunk_ledger` already does.

A6. An EMPTY ledger is also the honest answer for "this task has no recorded
decision", and that is NOT an error. Say so: the caller cannot distinguish the
two, deliberately, because both mean the same thing to a prompt — there is
nothing to quote.

A7. DELIBERATE ABSENCE, documented in the idiom: this function performs NO
storage I/O. It takes the mapping a caller already holds, so DECISION F033 D4's
property — this module drags no storage write behind it — is preserved, and a
reader looking for a job load here should stop at that paragraph.

A8. Add the new name to the module docstring's `Public API::` block in the SAME
commit. R-0746 is on this branch's record because that was once forgotten.

## SPEC B — `packages/orchestration/pingpong_loop.py`

B1. `run_pingpong` gains a KEYWORD-ONLY parameter `hunk_ledger: Any = None`,
documented as one attempt's ledger for the task about to be built, or `None`.

B2. Forward it at the `compose_builder_prompt` call that assigns
`builder_composed`. Change nothing else about that call.

B3. REFRESH the paragraph in `compose_builder_prompt`'s docstring that begins
"Remedy deliberately does NOT supply this parameter from the run loop yet". As
of C4 that sentence is stale: `run_pingpong` DOES take and forward the value.
Rewrite it to state what is then true — the loop forwards a ledger it is GIVEN,
`packages/orchestration/hunk_decision_record.py` is where a stored decision is
read from `job.metadata`, and what no round has wired yet is the JOB-level
caller in `packages/orchestration/pingpong_job.py`, which holds the job. Keep
naming modules rather than line numbers.

B4. Do NOT change `pingpong_job.py` or `do_cmd.py`. Both are outside the change
set. Wiring the job-level caller is the next round, and this round exists to
make that round's data route already proved.

## SPEC C — the tests

APPEND ONLY to both files. Do not edit, reorder or reflow one existing line: in
each, the pre-commit blob must be a byte-exact PREFIX of the post-commit file.
The obligation for a code append is ORDERED EQUALITY, never a per-line count.

C1. In `tests/orchestration/test_hunk_decision_record.py`, cover SPEC A: the
latest decision wins over an earlier one for the same task; a different task's
record is not returned; an unparseable `decided_at` loses to a parseable one;
with none parseable the last in insertion order wins; an absent task yields an
empty ledger; and every malformed input A5 names yields an empty ledger and
raises nothing, parametrized rather than written out one test per input.

C2. In the same file, prove the rebuild is faithful: a decision RECORDED through
`record_hunk_decision_from_view` and then read back by the new function yields a
ledger equal to the `ledger` field of the `HunkDecisionRecord` that recording
returned. Build the job with whatever fake or fixture that file already uses for
its existing recording tests; do not invent a second one.

C3. In `tests/orchestration/test_builder_prompt_hunk_rejections.py`, THE
ACCEPTANCE TEST, and it is the point of this round. Drive the REAL loop:
`run_pingpong` with `builder_name="fake"`, `reviewer_name="fake"` and a demo
repo built the way `tests/orchestration/test_pingpong.py`'s `demo_repo` fixture
builds one, with `REMEDY_DATA_DIR` redirected to `tmp_path` by `monkeypatch` the
way its `isolate_data_root` fixture does — the sandbox denies every shell form
of setting that variable, so it is set in-process or not at all. Pass a
`hunk_ledger` holding one rejection whose reason carries leading spaces, an
interior blank line and a tab.

The chain has THREE links and the block states all three, because the reviewer
measured at `d0c86c2d` that the trace carries a segment manifest but NO prompt
text, so a test asserting the reason directly off the trace cannot be written:
  (a) some `result.prompt_traces` entry has a `segment_manifest` row whose
      `name` is `builder_hunk_rejections` — the real loop composed the segment;
  (b) composing directly with the SAME ledger and recovering that segment's text
      by its manifest span, the reason is an EXACT SUBSTRING of it;
  (c) the sha256 on the row from (a) EQUALS the sha256 of the text from (b),
      which is what ties the loop's actual bytes to the text (b) inspected.
Link (c) is what makes this an end to end rather than two separate claims. The
reviewer measured that it holds: that segment's digest depends ONLY on the
ledger and not on any other argument to `compose_builder_prompt`, confirmed at
`d0c86c2d` across two compositions differing in goal, context, round number,
staged state, scope contract, task body, test result and findings, which both
produced the identical 123-character segment. Do not assert the 123; it is the
reviewer's reading of one fixture, and yours will differ with your reason.

C4. A round with NO hunk ledger composes no such segment: the same
`run_pingpong` call without the parameter yields traces whose manifests hold no
`builder_hunk_rejections` row. This is the negative half of C3 and it is what
makes C3 discriminating.

## Slice PLAN23 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file. PLAN23's own body contains `##` headings, which is why the
markers exist.

<<<BEGIN PLAN23
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
| R-0747, and the inverse of the ledger export | done | round 22 |
| the stored decision is selected and reaches the real loop | open | this round |
| the JOB-level caller in `pingpong_job.py` supplies it | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. This round adds the reader that selects a task's latest recorded decision
   from `job.metadata`, gives `run_pingpong` the parameter it forwards, and
   proves through the REAL loop that a rejection reason reaches the composed
   prompt's segment manifest.
2. Then the last wiring step: `packages/orchestration/pingpong_job.py` holds the
   job at its `run_pingpong` call, so it reads the decision and passes it. That
   is the only remaining hop, and it is deliberately its own round because it
   touches the job runner.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- Steps 2, 3 and 4 plus the two closure rounds exceed what the 25-round soft
  limit leaves. The scope report amend0827 rule 6 requires is now expected, and
  the session-6 handoff carries the proposal.
<<<END PLAN23

## Slice RECORD23 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated. The slice is every byte between the
markers, exclusive.

<<<BEGIN RECORD23
Gate: F033 R22 — THE REVIEWER'S OWN FALSE CLAUSE REPAIRED, AND THE LEDGER EXPORT GAINS ITS INVERSE. THE ROUND PASSED. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the reviewer reached at `d0c86c2d`. All eight gates were re-executed by the reviewer from scripts of its own and every ordered reading reproduced. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r22.md` against the reviewer's own pre-emission original was SILENT, as was the same comparison against `.agent/last_block.md`; the worker copied the file with `shutil.copyfile` rather than retyping it, so one end of that comparison is the emitted artefact itself. THE PLAN is byte-EQUAL to slice PLAN22 at 2577 bytes over 46 lines, under the 50-line cap, holding `## Goal` and the substring `Steps`. THE RECORD APPEND at `61d2ffe7` reconstructs 1580194 plus one newline plus 7989 to 1588184, base a byte PREFIX, slice an exact SUFFIX, the separator a newline, N COUNTED at 2 by the reviewer's own script, the last two blank-line units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1581426 — an offset the reviewer chose independently of the worker's 1582658, both inside the FIRST appended paragraph's span 1580195 to 1585120 — REJECTED by both readers, each of which accepted the unflipped bytes. THE LEDGER walked at three revisions: registered 307 to 308 with the ADDED id exactly `R-0747`; `Done:` 52 lines over 50 distinct UNMOVED at all three; `Landed:` 18 to 19 with `^Landed: R-0747 — ` exactly 1 at C3 and 0 before it; `^Gate: F033 R21 — ` 0 before and exactly 1 after; and the open set 257 to 258. THE ZERO-GATE HELD: `persists NOTHING` occurs 0 times in `packages/orchestration/pingpong_loop.py` at C5, and the reviewer confirmed the gate was not self-satisfying — the string appears in slice RECORD22, which lands in `.agent/live_review.md` and never in the file the gate counts. THE REPAIR IS TRUE, checked clause by clause against the source rather than against the block: the module writes the exported ledger to `job.metadata` under `hunk_decisions` keyed by attempt, `save_job` at the write door makes it durable, and what is missing is the wiring — every one of those verified at `d0c86c2d`. THE NEW FUNCTION MATCHES ITS SPEC: `import_hunk_ledger` is module-level and unprefixed, sits directly after `export_hunk_ledger`, is named in the `Public API::` block, reuses `_EXPORT_ROOT_KEY` and `_EXPORT_ENTRY_KEYS` rather than restating either spelling, documents the `id`-to-`hunk_id` rename as its whole reason for existing, and names which of its two guards each red-proof is aimed at — the counter-measure the R20 prose slip asked for, applied. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at C5 with its OWN anchors, each asserted UNIQUE, the file restored and proved byte-identical by sha256 after each: the unmutated control is a REAL exit 0 at 44 passed; dropping the reason on rebuild is exit 1 at exactly 3 failed, naming the round-trip, the byte-for-byte reason and the renderer tests; removing the structural guard entirely is exit 1 at 9 failed, every one a case of `test_no_malformed_input_makes_the_import_raise`, so the guard is genuinely reachable and the gate's permitted answer of "this reddened nothing" did not arise; and normalising an unknown state to pending is exit 1 at exactly 1 failed. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the four hunk suites 106 together, the two builder-prompt suites 35 together, and the canary 42, with `python3 -m ruff check` exiting 0 over all three changed files. THE STRUCTURE: eight single-parent commits over `0bcae480`..`d0c86c2d` of 314, 234, 12, 4, 11, 48, 146 and 200 insertions, every one under 500, the last being the handback commit the block could not gate and which the reviewer measured here; the path set to C5 EQUALS the declared change set in BOTH directions; and the append to `tests/orchestration/test_hunk_ledger.py` satisfies ORDERED EQUALITY — the pre-commit blob is a byte PREFIX and the 146 lines that commit's diff ADDS are exactly the appended suffix IN ORDER. THE WORKER DECLARED SEVEN DEVIATIONS AND EVERY ONE IS HONEST, two of them improving on the order: it added a seventh test the block never asked for, which discriminates the structural guard from the coercion guard where nothing else did, and it declined to name `import_hunk_ledger` in SPEC A's repaired paragraph because C3 lands before C4 and the reference would have dangled — a correct reading of its own commit sequence. ONE OBSERVATION THAT IS NOT A FINDING: after C4 that repaired paragraph says the unbuilt step is "reading that key for the current attempt and rebuilding a ledger from its rows", and round 22 shipped a function that does the second half. The sentence remains TRUE as written, because the STEP is an action no code path performs and a function nobody calls is a tool rather than a step; but it is one round from becoming misleading, so the R23 block orders that paragraph refreshed as part of the round that gives the loop its parameter.

Done: R-0747 — RESOLVED at `72dcfd53`. The false clause is gone and the replacement is true. VERIFIED by the reviewer at `d0c86c2d`, reading each of its claims against the source rather than against the block that ordered it: `packages/orchestration/hunk_decision_record.py` line 226 writes `job.metadata.setdefault(HUNK_DECISIONS_METADATA_KEY, {})` and line 227 assigns the exported record under the attempt key, the constant is the literal `hunk_decisions`, and `packages/orchestration/ui_server.py` line 3940 calls `save_job(job)` inside `_dispatch_approve_hunks`. The paragraph now says the absence is in the WIRING and not in the data, which is the measured truth. The zero-gate confirms the retired wording is gone: `persists NOTHING` occurs 0 times in `packages/orchestration/pingpong_loop.py` at C5. `.agent/plan.md` no longer tells the next round to locate storage; PLAN22 replaced that step with reading the key, which the finding's own fix clause required for resolution. The `Landed: R-0747` line the worker wrote at C3 STANDS beside this paragraph and is not deleted — this record is append-only and that line is the honest trace of a fix that landed before its resolution was authored. THE LESSON IS THE REVIEWER'S AND IT IS RECORDED HERE RATHER THAN IN A SLIP, because it is the finding's own root cause: the reviewer read a module docstring saying it "imports no storage", inferred that nothing was stored, and wrote that inference into a block as a measurement without opening the function body or either door. A docstring is a claim about a file, not a measurement of it, and the distinction is exactly the one this record exists to keep.
<<<END RECORD23

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it as written
   and declare the problem in the handback; never silently repair it.
2. PLAN23 is a FULL REWRITE. RECORD23 is an APPEND: measured by the reviewer at
   `d0c86c2d`, `.agent/live_review.md` is 1588184 bytes and ends with a newline,
   so the append is one blank-line separator then the slice.
3. Do NOT delete or edit the `Landed: R-0747` line. This record is append-only;
   the `Done:` paragraph joins it rather than replacing it, which is this
   branch's established precedent.
4. Both test edits are CODE APPENDS. The obligation is ORDERED EQUALITY — the
   pre-commit blob a byte-exact PREFIX, the commit's added lines exactly the
   appended lines IN ORDER — and never a per-line uniqueness count, which is
   unattainable for code by construction.
5. Touch no path outside the change set. In particular do NOT touch
   `packages/orchestration/pingpong_job.py`, `apps/cli/commands/do_cmd.py`,
   `.agent/prose_slips.md` or anything under `docs/`.
6. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`; use `python3 -m ruff`.
   REAL exit codes come from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO
   PIPE — a piped form reports the last stage's exit and cannot fail.
7. Destructive verification runs ONLY in a disposable `git worktree`, purged of
   `__pycache__`, under `python3 -B`. The primary checkout satisfies
   `git status --porcelain` empty at the handback.
8. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
9. G1 through G8 all run at C5, before the handback commit C6.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r23.md` and `cmp` it against
`.remedy-wt/f033-r23-block.md`. One reading.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN23, under 50 lines, holding
`## Goal` and the substring `Steps`. Report bytes and lines.

G3 THE RECORD APPEND, measured AT C2. Reconstruct 1588184 plus one newline plus
the byte length of RECORD23 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script rather than
taking it from this block, and compare the file's LAST N blank-line units
against the slice's paragraphs IN ORDER. Flip one byte inside the FIRST appended
paragraph, report the offset, prove it lies in that paragraph's span, and show
BOTH readers reject the flipped bytes and accept the unflipped ones.

G4 THE LEDGER, at `d0c86c2d` and at C2: registered `^- R-\d+ — ` 308 distinct
UNMOVED; `^Done: R-\d+ — ` 52 lines over 50 distinct going to 53 over 51 with
the ADDED resolved id exactly `R-0747`; `^Landed: ` 19 UNMOVED with
`^Landed: R-0747 — ` still exactly 1; `^Gate: F033 R22 — ` 0 before and exactly
1 after; and the open set 258 going to 257.

G5 THE CODE AGAINST THE SPEC, at C5. `python3 -m ruff check` exits 0 over all
four changed files. By AST: the new reader is defined at module level in
`hunk_decision_record.py` with no leading underscore and its name appears in
that module's `Public API::` block; `run_pingpong` carries `hunk_ledger` as a
keyword-only parameter defaulting to `None`; and `hunk_ledger` is passed at the
`compose_builder_prompt` call inside `run_pingpong`. Report `open(` and
`save_job` occurrence counts in `hunk_decision_record.py` — both must still be
0, which is DECISION F033 D4's standing property and SPEC A7's claim.

G6 MUTATION RED-PROOFS, in a disposable worktree at C5. Run the UNMUTATED
CONTROL FIRST over both changed test files and report its REAL exit code and
pass count beside every mutation. Each anchor is a byte string shown to occur
EXACTLY ONCE in the file it edits; report that count; restore and prove
byte-identical by sha256 after each.
  (i) make the selector return the FIRST matching record instead of the latest
      — C1's latest-wins test must go RED.
  (ii) remove SPEC A5's structural guard so a malformed input raises — the
      totality tests must go RED. If this reddens nothing, SAY SO: that is a
      real result about a guard no test reaches.
  (iii) stop forwarding `hunk_ledger` at the `compose_builder_prompt` call
      inside `run_pingpong` — the C3 acceptance test must go RED. This is the
      mutation that proves the end to end is really end to end.
Report the failing test NAMES, not only counts.

G7 THE SUITES, SERIALLY, in the PRIMARY checkout at C5, each with REAL exit code
and pass count: `test_hunk_decision_record.py`;
`test_builder_prompt_hunk_rejections.py`; `test_hunk_ledger.py`;
`test_hunk_repair_findings.py`; `test_builder_prompt_golden.py`;
`test_pingpong.py`; `test_pingpong_cli.py`; and the canary
`python3 -m pytest tests/cli/test_golden_path.py -q`.

G8 STRUCTURE. `git status --porcelain` EMPTY. For every commit from C0a through
C5 report insertions from `git diff --numstat` and show each under 500. Show the
path set over `d0c86c2d`..C5 equals the change set minus `.agent/handoff.md` in
BOTH directions. For BOTH appended test files show the pre-commit blob is a byte
PREFIX and the added lines are exactly the appended suffix IN ORDER.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 6 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle and SPEC item, every deviation, and the
next expected action. No length cap. If any gate is RED, do not repair on your
own initiative: report it and stop.
