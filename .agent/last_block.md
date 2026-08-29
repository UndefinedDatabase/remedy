# STEP 21 — F033 Hunk-level diff approval (SESSION 6, round 21 of a 25-round soft limit)

Goal: the rejected hunks of an attempt reach the NEXT builder prompt as a
steering-rank segment, with the operator's reason surviving composition BYTE FOR
BYTE. This is the acceptance property the feature file calls "rejection reasons
verbatim in the next trace".

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r21.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN21.
4. C2: append slice RECORD21 to `.agent/live_review.md` — this books the round 20
   PASS that `.agent/handoff.md` has carried since `b5a29a74`, per operator
   amendment amend0827 rule 1. It buys no round of its own; this round is
   happening anyway.
5. C3: append slice SLIPS21 to `.agent/prose_slips.md` — the two reviewer prose
   slips the same handoff carries.
6. C4: SPEC A against `packages/orchestration/pingpong_loop.py`.
7. C5: the new test file `tests/orchestration/test_builder_prompt_hunk_rejections.py`.
8. C6: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r21.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_builder_prompt_hunk_rejections.py
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `98ce168e`, which is this
round's base. They are stated here so the worker does not rediscover them.

- `packages/orchestration/hunk_repair_findings.py` has NO caller. Its
  `render_rejection_findings` is TOTAL: it returns `""` for `None`, for a
  ledger with no `entries`, and for a ledger holding only approvals.
- Importing it pulls exactly `packages.orchestration.hunk_approval`,
  `packages.orchestration.hunk_ledger` and itself. `pingpong_loop` is NOT in
  that closure, so the import SPEC A1 orders creates no cycle.
- `compose_builder_prompt` builds a `specs` list, joins each spec's parts with
  `"\n"`, passes the joined texts through `_drop_one_newline_per_segment_boundary`,
  registers them and composes. `builder_repair` and `builder_directive` are both
  rank `STEERING`, so their ORDER is registration order, and the directive is
  registered last.
- `_drop_one_newline_per_segment_boundary` drops the EARLIER segment's trailing
  newline. `render_rejection_findings` always ends its non-empty output with a
  STRUCTURAL newline — the empty string its per-entry loop appends last — so the
  byte that boundary consumes is never a byte of an operator's reason. The
  reviewer confirmed this at `98ce168e` against a reason carrying leading
  spaces, an interior blank line, a tab indent, a `#` first character and
  trailing spaces: it survived composition unchanged.
- `tests/orchestration/test_builder_prompt_golden.py` asserts an EXACT segment
  name tuple for the `full` shape and `len(ordered) == len(texts)` against a
  fixed `_PRE_MIGRATION_ORDER`. A segment registered unconditionally would
  appear in all four shapes and turn that suite RED. That is why SPEC A3's
  guard is load-bearing and why G6(i) can find it.
- `packages/orchestration/hunk_decision_record.py` builds the ledger and
  deliberately persists NOTHING. There is therefore no route from a stored
  decision to the run loop yet, which is why SPEC A5 leaves the call site alone
  and why the plan gives that its own round.

## SPEC A — `packages/orchestration/pingpong_loop.py`

Described, not sliced: this is production code and the worker writes it.

A1. Add, beside the module's other `packages.orchestration` imports:
`from packages.orchestration.hunk_repair_findings import render_rejection_findings`

A2. `compose_builder_prompt` gains a KEYWORD-ONLY parameter, last in its
signature, defaulting to `None`: `hunk_ledger: Any = None`. Document it as one
attempt's `HunkDecisionLedger`, or `None` when the round has no recorded hunk
decision. If `Any` is not already imported in this module, import it.

A3. Between the `builder_repair` append and the `builder_directive` append,
render once and register only on a non-empty result, at rank `STEERING`, under
the segment name `builder_hunk_rejections`, with the rendered text as the
spec's single part.

A4. THERE IS EXACTLY ONE GUARD, and it is the emptiness test on the rendered
text. Do NOT add a second `hunk_ledger is not None` test beside it.
`render_rejection_findings` is total and answers `""` for `None`, so a second
layer would make the first unobservable and G6(i) would redden nothing. This is
the defect the R20 prose slip in slice SLIPS21 records, and this clause is it
being applied rather than repeated.

A5. DELIBERATE ABSENCES, each documented in the code where a reader would search
for it, in the repository's "Remedy deliberately does not X because Y" idiom:
  (i) the run-loop call site that composes the builder prompt is NOT changed
      this round, so nothing yet SUPPLIES a ledger in production; the round that
      locates the supply follows this one.
  (ii) the rendered text is NOT capped, unlike `safe_diff` at `_REPAIR_DIFF_CAP`.
      A cap truncates, and truncating an operator's words is precisely what the
      verbatim rule forbids.

A6. `_build_builder_prompt` gains the same keyword-only parameter and forwards
it unchanged. Its behaviour is otherwise untouched: it still returns
`compose_builder_prompt(...).text`.

## SPEC B — `tests/orchestration/test_builder_prompt_hunk_rejections.py`

New file. It must reference the rendered vocabulary through the NAMES
`hunk_repair_findings` exports — `REJECTION_FINDINGS_HEADING`,
`REJECTION_FINDINGS_ENTRY_PREFIX`, `REJECTION_FINDINGS_REASON_INTRO` — and never
by retyping their spelling, which is the convention that module's own docstring
states. Cover at least:

B1. THE ACCEPTANCE PROPERTY. A reason carrying leading spaces, an interior blank
line, a tab indent, a line whose first character is `#`, and trailing spaces
appears as an EXACT SUBSTRING of `compose_builder_prompt(...).text`. Assert the
substring, not a normalised form.

B2. A reason whose final character is a newline keeps that newline in the
composed text — the boundary helper consumes the renderer's structural newline
and not the operator's.

B3. With no rejection in the ledger, and with `hunk_ledger` left at its default,
the composed manifest holds NO `builder_hunk_rejections` entry and the composed
text is byte-equal to the same call without the parameter.

B4. When the segment IS present, `builder_directive` is still the LAST manifest
entry, and `builder_hunk_rejections` sits after `builder_repair` when findings
are also supplied.

B5. The manifest ranks stay non-decreasing with the segment present.

B6. A malformed ledger — one without `entries`, and one whose entry lacks
`reason` — composes without raising and registers no rejections segment.

B7. `_build_builder_prompt` forwards the parameter: its text equals
`compose_builder_prompt(...).text` for a ledger with a rejection.

## Slice PLAN21 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file. PLAN21's own body contains `##` headings, which is why the
markers exist.

<<<BEGIN PLAN21
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
| that renderer reaches the builder prompt as a segment | open | this round |
| the run loop SUPPLIES a ledger, and the two-round end-to-end | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. This round wires `render_rejection_findings` into `compose_builder_prompt` as
   a STEERING-rank segment and proves the verbatim property survives
   composition. It changes no call site, so nothing supplies a ledger yet.
2. Then the supply: `packages/orchestration/hunk_decision_record.py` builds the
   ledger and persists nothing, so the round after this one must first locate
   where a recorded decision is stored before it can reach the run loop. That
   round also carries the two-round end-to-end the Acceptance asks for.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- Five rounds of headroom remain against the 25-round soft limit and steps 2, 3
  and 4 above are four rounds of work. Session 6 may owe the scope report.
<<<END PLAN21

## Slice RECORD21 — appended to `.agent/live_review.md`

One paragraph. The slice is every byte between the markers, exclusive.

<<<BEGIN RECORD21
Gate: F033 R20 — REJECTED HUNKS AS VERBATIM REPAIR FINDINGS. THE ROUND PASSED. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the session-5 reviewer reached and committed to `.agent/handoff.md` at `b5a29a74`; it is written into this record by the first commits of the next round rather than by a round of its own, and every reading below is that reviewer's, taken at `203689cf`. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r20.md` against the reviewer's own scratchpad original, SILENT. That chain walks the saved copy, its mirror and the working copy — three artefacts that are all the worker's own output — so it establishes SELF-CONSISTENCY and is not a claim about the emitted bytes. Each slice region was read AT THE COMMIT THAT APPLIED IT and is byte-EQUAL to its original: PLAN20 at `69084af5` at 2570 bytes over 46 lines, RECORD20 at `d9db68ef` at 10101 bytes, SLIPS20 at `688cf561` at 1622 bytes. THE RECORD APPEND reconstructs 1565456 plus one newline plus 10101 to 1575558, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 3 over 713 blank-line units, and a negative control at byte 1568181 — proved to lie inside the FIRST appended paragraph, spanning 1565457 to 1570905 — REJECTED by both readers run independently, each of which accepted the unflipped file. THE LEDGER: registered 307 UNMOVED; `Done:` 50 lines over 48 distinct to 52 over 50 with the ADDED ids exactly `R-0738` and `R-0746`; `Landed:` 18 UNMOVED with the `Landed: R-0746` line still standing beside its new `Done:` paragraph, which is this branch's append-only precedent; `^Gate: F033 R19 — ` 0 before and exactly 1 after; distinct `DECISION F033 D` ids 5 UNMOVED; and the open set 259 to 257, the first fall this feature has recorded. That numeral spans the ROUND, measured between `d4a21259` and `b5a29a74`; the SESSION's own movement is 258 to 257 between `5f0273d8` and `b5a29a74`, and R-0746's mid-session registration is the whole difference between the two. THE MODULE IS PURE AS ORDERED and its docstring documents both deliberate absences — it renders nothing that was approved, and it had no caller at `203689cf`. THE VERBATIM RULE HOLDS WHERE IT MATTERS: `entry.reason` is appended raw, never stripped, wrapped, escaped or indented, and is deliberately NOT put through the coercion guard, because rendering the string "None" where an operator's words belong would put words in their mouth. THE MUTATIONS were re-run by the reviewer in its own disposable worktree with its OWN anchors, each asserted UNIQUE, the file restored and PROVED byte-identical against the committed blob: unmutated control 17 passed at REAL exit 0; dropping the reason exit 1 at 8 failed; rendering non-rejected entries exit 1 at 3 failed; removing the STRUCTURAL guard exit 1 at 5 failed. THE REVIEWER ALSO RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED, to settle the worker's deviation D4 rather than take it on trust: removing ONLY the coercion guard `_total_text`, leaving the structural guard intact, reddens EXACTLY ONE test, `test_an_id_whose_str_raises_returns_rather_than_raises`, which is precisely the one the structural mutation left green. The two guards are measured by DISJOINT tests, 5 and 1 covering all six totality assertions, and the worker's design decision is confirmed correct. D4 IS A DEFECT IN THE REVIEWER'S OWN BLOCK: its SPEC A6 ordered totality on all inputs, a re-stated coercion guard AND empty-string-on-unreadable without saying which of those is THE guard, so gate G6(iii) as written would have reddened nothing. The worker resolved it correctly and declared it; it is recorded as a prose slip, spends no id, and the counter-measure is applied in the R21 block's SPEC A4. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the new file 17, the hunk ledger 29, hunk approval 30, `test_named_bugs.py` 64 passed and 6 skipped, `test_resource_safety.py` 21, and the canary 42, with `ruff` exiting 0 over both new files. THE STRUCTURE: nine single-parent commits over `d4a21259`..`203689cf` of 344, 238, 20, 6, 6, 130, 294, 294 and 17 insertions, every one under 500; the path set over the WHOLE range EQUALS the declared change set in BOTH directions; and all sixteen do-not-touch paths blob-identical at both ends. The remaining eight deviations were honest and need no action, and D3 deserves a note for its honesty rather than any fault: the worker used `git worktree remove --force` and stated it had NOT first tried without the flag, so it could not claim the flag was necessary, which is the correct way to report an unmeasured choice.
<<<END RECORD21

## Slice SLIPS21 — appended to `.agent/prose_slips.md`

Two paragraphs, separated by one blank line. The slice is every byte between the
markers, exclusive.

<<<BEGIN SLIPS21
2026-08-29 · F033 R20 · The block's SPEC A6 ordered totality on all inputs, a re-stated coercion guard AND empty-string-on-unreadable without saying which of those is THE guard, so the obvious reading produces two overlapping defensive layers and the block's own G6(iii) would have reddened nothing — a mutation defeated by redundancy rather than by a missing test; the worker made the structural guard singular, confined the coercion guard to the id, and proved both are measured by disjoint tests, and a SPEC ordering defence in depth must name which layer its red-proof is aimed at.

2026-08-29 · F033 R20 · The session-close handoff stated the open set's movement twice — "259 to 257" for the round and "258 to 257" for the session — without either sentence naming the range it spanned, so the worker applying it reasonably read them as one quantity contradicting itself and proposed a correction that was itself false; both numerals were right, R-0746's mid-session registration is the difference between them, and a numeral about a MOVING quantity must name the two commits it is measured between or it invites a wrong repair.
<<<END SLIPS21

## Constraints

1. Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it as written
   and declare the problem in the handback; never silently repair it.
2. PLAN21 is a FULL REWRITE of `.agent/plan.md`. RECORD21 and SLIPS21 are
   APPENDS: the existing file is a byte PREFIX of the result. Measured by the
   reviewer at `98ce168e`, both target files end with a newline, so each append
   is one blank-line separator then the slice.
3. Touch no path outside the change set. In particular do not touch
   `.agent/context.md`, `.agent/decisions.md` or any file under `docs/`.
4. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, and process substitution. Use one command per call, `git -C`,
   `python3 -c` or a heredoc for anything counting or hashing, and
   `python3 -m ruff` rather than the bare executable.
5. A gate's REAL exit code is captured as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`
   with NO PIPE in it. The reviewer measured at `98ce168e` that
   `false 2>&1 | tail -1; echo $?` reports 0, so a piped form is a gate that
   cannot fail and its reading is not evidence.
6. Destructive verification runs ONLY in a disposable `git worktree`. The
   primary checkout satisfies `git status --porcelain` empty at the handback.
   Purge `__pycache__` and run `python3 -B` inside that worktree.
7. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
8. G1 through G8 all run at C5, which is BEFORE the handback commit C6, so C6
   can quote every one of them. C6's own insertion count is not gated here —
   it cannot exist while C6 is being written; the reviewer measures it.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r21.md`. One reading.

G2 THE PROSE FILES. `.agent/plan.md` is byte-EQUAL to PLAN21 and is under 50
lines, and it still contains `## Goal` and the substring `Steps`, which
`tests/ui_server/test_dashboard_contract.py::test_plan_md_references_current_steps`
asserts. `.agent/prose_slips.md` reconstructs 29663 plus one newline plus the
byte length of SLIPS21 to its committed size; report all three numbers.

G3 THE RECORD APPEND into `.agent/live_review.md`. Reconstruct 1575558 plus one
newline plus the byte length of RECORD21 to the committed size. Prove the
pre-commit blob is a byte PREFIX and the slice an exact SUFFIX. COUNT N, the
slice's blank-line paragraphs, in the script — do not take it from this block —
and compare the file's LAST N blank-line units against the slice's paragraphs IN
ORDER. Then flip one byte inside the FIRST appended paragraph, report the byte
offset and prove it lies in that paragraph's span, and show BOTH readers reject
the flipped file while both accept the unflipped one.

G4 THE LEDGER, before and after C2: registered `^- R-\d+ — ` 307 distinct
UNMOVED; `^Done: R-\d+ — ` 52 lines over 50 distinct UNMOVED; `^Landed: ` 18
lines over 15 distinct UNMOVED; `^Gate: F033 R20 — ` 0 before and exactly 1
after; the open set, distinct registered minus distinct resolved, 257 UNMOVED.

G5 THE CODE AGAINST THE SPEC, at C5. `python3 -m ruff check` exits 0 over both
changed files. By AST and not by grep, show that `compose_builder_prompt` and
`_build_builder_prompt` each carry a KEYWORD-ONLY parameter named `hunk_ledger`
defaulting to `None`, and that the module imports `render_rejection_findings`.
Show `builder_hunk_rejections` is registered at rank `STEERING`.

G6 MUTATION RED-PROOFS, in a disposable worktree at C5, `python3 -B`, with
`__pycache__` purged. Run the UNMUTATED CONTROL FIRST and report its REAL exit
code and pass count beside every mutation. Each anchor is a byte string you have
shown occurs EXACTLY ONCE in `packages/orchestration/pingpong_loop.py`; report
that count. Restore the file after each and prove it byte-identical to the
committed blob. Selection for each run: the new test file plus
`tests/orchestration/test_builder_prompt_golden.py`.
  (i) remove SPEC A3's emptiness guard so the segment registers unconditionally
      — `test_builder_prompt_golden.py` must go RED.
  (ii) register the rejections spec AFTER the `builder_directive` spec instead of
      before it — the new test file must go RED.
  (iii) register `rejection_text.strip()` instead of `rejection_text` — the new
      test file must go RED.
Report the failing test NAMES, not only counts.

G7 THE SUITES, SERIALLY, in the PRIMARY checkout at C5, each with its REAL exit
code and pass count: the new test file; `test_builder_prompt_golden.py`;
`test_prompt_cache_prefix.py`; `test_hunk_repair_findings.py`;
`test_pingpong_cli.py`; `test_repair_loop.py`; and the canary
`python3 -m pytest tests/cli/test_golden_path.py -q`.

G8 STRUCTURE. `git status --porcelain` EMPTY. For every commit from C0a through
C5, report insertions from `git diff --numstat` and show each is under 500. Show
the path set over `98ce168e`..C5 equals the change set above minus
`.agent/handoff.md`, in BOTH directions.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
feature and round, SESSION 6 of F033, the branch, the commit SHAs, a
changed-files table, one line per gate G1 through G8 with its REAL exit code, the
open-findings count, every deviation, and the next expected action. It has no
length cap. If any gate is RED, do not repair on your own initiative: report it
and stop.
