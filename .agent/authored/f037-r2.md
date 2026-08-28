STEP R2 / F037 — RENDERED DIFF VIEWER
Goal:        BOOK R1 AND AMEND THE SPEC THE INVENTORY CONTRADICTED. R1 measured
             two assumptions in `docs/roadmap/features/T5_F037.md` that the
             source does not meet: the contract's `binary` file status exists
             in no vocabulary this repository has, and there is NO per-attempt
             diff for the endpoint's attempt parameter to key on. Under
             `docs/agents/planner_reviewer_prompt.md` §4 item 7 a wrong spec is
             a finding routed to planning, so this round writes the R1 verdict,
             registers the finding R1 surfaced, records the reviewer's own
             authoring slip, and lands the DECISIONS and the feature-file
             amendments they rule. The design MOVES on disk this round so that
             T001 is planned against a spec the source can meet.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the record — the R1 gate, finding `R-0715`, the
             reviewer's slip and both DECISIONS · C3 the feature-file
             amendments · C4 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f037-r2.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `docs/roadmap/features/T5_F037.md`, `.agent/handoff.md`. This list
             bounds what you WRITE INTO THE REPOSITORY. It does NOT bound what
             you DO: G8 orders a push. NOTHING under `apps/`, `packages/` or
             `tests/` is written, and under `docs/` ONLY
             `docs/roadmap/features/T5_F037.md`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f037-r2.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f037-r2.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A SLICE begins at the line AFTER `<<<SLICE NAME` and ends at
    the line BEFORE `<<<END NAME`; its TEXT is its content lines joined with a
    newline plus ONE trailing newline, and that is the ONLY definition of a
    slice's bytes used anywhere in this block. If a slice contradicts something
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations — a corrected slice destroys the transport proof.
 3. EVERY EOF APPEND IN THIS ROUND IS THE SAME OPERATION: the target file's
    bytes as they stood before the commit, plus exactly ONE newline, plus the
    slice's TEXT as constraint 2 defines it. That is the operation for
    `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md` and
    `docs/roadmap/features/T5_F037.md`. No other separator is added and none is
    removed.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. The record moves
    BEFORE the feature file: C2 carries every ledger and decision append and C3
    carries the spec. Every sentence in PLANF037R2 that describes THIS round's
    own landed change depends on that order, and this constraint is what fixes
    it. `.agent/plan.md` is advanced at C1, the FIRST substantive commit, as
    `docs/agents/planner_reviewer_prompt.md` §3 item 23 requires of any round
    that touches the finding ledger.
 5. NOTHING IS EDITED OUT OF ANY APPEND-ONLY RECORD. `.agent/live_review.md` is
    append-only from its `## Findings` heading down, `.agent/prose_slips.md` and
    `.agent/decisions.md` are append-only entire. No existing finding
    paragraph, no `Done:` line, no existing `Gate:` paragraph and no existing
    DECISION is rewritten, deleted or renumbered. This round RESOLVES nothing.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id, never author a `Done:` line and never
    write a DECISION. If you find a defect, report it in the handback under
    Deviations and let the reviewer rule on it.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
 8. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. Run no
    `npm`, `npx`, `node` or `vite`, and build nothing. The primary checkout
    reads `git status --porcelain` 0 lines at every commit.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
10. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `69f6478c` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
11. THE REPLACEMENT PAIR IS CLASSIFIED BY A MECHANICAL CONTAINMENT TEST THE
    REVIEWER RAN, and the output is printed here. DFROM/DTO —
    `TO contains FROM: true`, so APPEND-SHAPED. It therefore carries the §4.9
    APPEND obligation — FROM exactly 1x in the target BEFORE the edit, and each
    TO-ONLY line exactly 1x among the lines C3's diff ADDS — and NO FROM-zero
    count is ordered or attainable for it. Everything else this round applies
    is an EOF append under constraint 3, not a pair.
12. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F037 and that R2 is the round. The handback has NO LENGTH CAP — operator
    amendment amend0827 rule 3 withdrew every tier — so do not declare, measure
    or apologise for its length. It is VALID when its mandated sections are
    present, and DROPPING one is the finding the cap used to stand in for.

Done when:
 G1. HYGIENE, THE BASE AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     C0a, which must be `69f6478c6c18b7957f3e244b9f121e372f22a99d`, and
     `git branch --show-current`, which must be
     `feature/f037-rendered-diff-viewer`. Report `git status --porcelain` as a
     LINE COUNT after each of C0a, C0b, C1, C2 and C3, each 0. C4's own reading
     belongs in no file this round writes, because C4 is the commit that writes
     the handback; take it and report it in your completion report instead.
     Report `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f037-r2.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C3 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF037R2 under the
     newline-INCLUDED convention of constraint 2. Run the negative control
     against the slice MINUS its trailing newline and report FALSE. Then report
     the contract readings: `^## Goal$` 1, `^## Next Steps$` 1, a match for
     `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER 50.
 G5. THE THREE RECORD APPENDS, AT C2. Apply RECORDR2 to `.agent/live_review.md`,
     SLIPR2 to `.agent/prose_slips.md` and DECR2 to `.agent/decisions.md`, each
     by the single operation constraint 3 defines. For EACH of the three, read
     the baseline with `git show 89b96df7:<path>` so no tracked file is ever
     overwritten to obtain one, and prove the result TWO WAYS. Reader (a),
     RECONSTRUCTION: baseline bytes plus one newline plus the slice text is
     BYTE-EQUAL to the file at C2, and the baseline is a byte PREFIX of it;
     report the arithmetic as `<baseline> + 1 + <slice> = <post>` in bytes.
     Reader (b), STRUCTURE: split the file at C2 on blank lines, count N as the
     number of blank-line units the SLICE itself holds — N is a number YOUR
     script counts from the slice, never one this block asserts — and report
     that the LAST N units of the file equal the slice's N units IN ORDER.
     NEGATIVE CONTROL for each of the three: flip ONE byte at a byte offset you
     assert and report to lie inside the FIRST appended paragraph, and report
     that BOTH readers reject. Then report, for `.agent/live_review.md` before
     and after C2, the line-anchored counts of `^- R-\d+ — `,
     `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: R\d+ — ` and
     `^Gate: F\d+ R\d+ — `; the reviewer measured 275, 24, 1, 19 and 71 at the
     base, and after C2 they must read 276, 24, 1, 19 and 72. Report the
     finding ids ADDED as a SET, which must be exactly `R-0715`, the resolved
     ids ADDED and REMOVED and the finding ids REMOVED as SETS, all three
     EMPTY, whether all ids are DISTINCT, the maximum id after C2, which is
     `R-0715`, and the open set after C2, which is 252. Report the count of
     `^## DECISION ` in `.agent/decisions.md` before and after C2, and the
     literal strings `## DECISION F037 D1 ` and `## DECISION F037 D2 `, each 0
     before and EXACTLY 1 after.
 G6. THE FEATURE FILE, AT C3. Apply the DFROM/DTO pair, then append AMENDF037
     by the operation of constraint 3. Report, for
     `docs/roadmap/features/T5_F037.md`: DFROM occurs EXACTLY 1x BEFORE the
     edit; after C3, DFROM occurs 1x and DTO occurs EXACTLY 1x, which is the
     APPEND-shaped obligation constraint 11 assigns this pair and the reason no
     FROM-zero count is ordered. Report that each of the TO-ONLY lines of DTO —
     the lines of DTO that are not lines of DFROM — occurs EXACTLY 1x among the
     lines C3's diff ADDS to that file. Prove the append by RECONSTRUCTION as
     in G5 reader (a), against the baseline `git show d4aef1db:<path>` with the
     DFROM/DTO pair applied to it in memory first, and report the byte
     arithmetic. Report `^## Design amendments$` 0 before and EXACTLY 1 after,
     and `^## Do not touch$` 1 both before and after.
 G7. THE DOCS GATE AND THE CANARY, run AFTER C3 and BEFORE C4. This round's
     change set includes `docs/roadmap/**`, so `.agent/context.md`'s standing
     constraint binds: run, as ONE pytest process and never two at once,
     `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py
     tests/cli/test_golden_path.py -q` from the repository root. Report the
     REAL exit code, the summary line VERBATIM, and the COUNT of lines matching
     `^FAILED`. PROVE YOUR `^FAILED` EXTRACTOR IS NOT BLIND by running it over
     a string you know contains such a line and reporting that it matched. The
     reviewer measured `367 passed` at a REAL exit 0 with zero `^FAILED` lines
     at the round base. IF YOUR RUN IS RED, report the failing node ids
     VERBATIM and hand back.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only 69f6478c..C3` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C4
     writes — and report both residues EMPTY. Report `git diff --stat
     69f6478c..C3` restricted to `apps/`, `packages/`, `tests/` and `docs/` —
     the last WHOLE — and confirm the first three EMPTY and the fourth holding
     `docs/roadmap/features/T5_F037.md` alone. Report each commit's insertions
     from `git diff --numstat` for C0a through C3, confirm each single-parent
     and under 500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
     `.agent/decisions.md` and `docs/roadmap/features/T5_F037.md` at their
     commits, against a CONTROL over the C0a blob which is not 0. Report `git
     ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, and `git branch
     --list "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C4, run `git push origin feature/f037-rendered-diff-viewer`. ITS
     OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C4 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: the `## Session` section constraint 12 orders, feature and
             round, branch, the round base SHA `69f6478c`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item, ONE LINE PER GATE for G1
             through G8 with its real exit code, the open-findings count after
             this round, and the next expected action. C4 cannot table its own
             numstat — write `self` in that cell, as `R-0149` requires, and put
             C4's own numbers nowhere.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF037R2
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 onward.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and — from this round — the design amendments that reconcile it
with the source.

## Current Step
R2 books the R1 verdict, registers `R-0715`, records the reviewer's authoring
slip, and lands the DECISIONS the R1 inventory forced together with the
feature-file amendments they rule. The inventory measured that no vocabulary in
this repository carries a `binary` file status and that no per-attempt diff
exists anywhere, so the spec is amended on disk before T001 is planned against
it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the record, the finding, the slip, both DECISIONS | ordered | record first |
| C3 the feature-file amendments | ordered | the spec moves on disk |
| C4 the handback | ordered | |

## Next Steps
1. T001: the unified-to-JSON parser as a NEW module with its corpus tests, then
   the read endpoint, planned against the amended spec.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low. It is a stale count in a test docstring, turns
  nothing red, and belongs to whoever next edits that file.
- The amended spec drops the endpoint's attempt parameter for v1. If a later
  feature makes per-attempt diffs real, DECISION F037 D2 names how to reverse
  that.
<<<END PLANF037R2

<<<SLICE RECORDR2
Gate: F037 R1 — the F037 claim-and-inventory round, and the first entry of this record. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `69f6478c`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `906b7ee592aed02e7161797030d5adfc2906390f7367feae446f55fe2b2e1231` over 32631 bytes and 458 lines, equal across the reviewer's gitignored scratch original, the committed `.agent/authored/f037-r1.md` blob and the committed `.agent/last_block.md` blob, the two committed paths being ONE git blob, `2da50bdba5ca4a632eac5e5255fc0bdf34a7c2df`; that chain covers the original, the saved copy and the mirror, and claims nothing about any prompt's bytes. EXTRACTION FROM THE COMMITTED BLOB REPRODUCES THE BLOCK'S ARITHMETIC: 7 slices at 47, 55, 26, 27, 1, 1 and 1 content lines, CONTENT 158 against TOTAL 458, so PROSE is 300 and both caps hold. THE PLAN AND THE CONTEXT ARE BYTE-EQUAL to their slices with the trailing-newline negative controls `False`, the plan at 47 lines. THE LEDGER RESET IS PROVED BY WHOLE-FILE RECONSTRUCTION AND THE FINDINGS REGION IS UNTOUCHED: the region from `## Findings` to the end of the pre-commit blob is byte-identical at 1124868 bytes and sha256 `abc8bdb4f682d04bc84d56ca0eda9d23dc17c32cb5987fab8e3d91c932a7f528` at both points, the header pair moved `1`→`0` and `0`→`1`, and the counters read 275, 24, 1, 19 and 70→71 with the open set unmoved at 251 and the maximum id `R-0714`. THE STATUS CLAIM IS EXACTLY ONE LINE: `^- \[ \] ` 196→195, `^- \[x\] ` 59 unchanged, `^- \[~\] ` 0→1, the total `^- \[` unchanged at 255, and the single active line is F037. THE TWO SUITES WERE RE-RUN BY THE REVIEWER at a real exit 0 with zero `^FAILED` lines: `325 passed` over `tests/docs/` with `tests/orchestration/test_roadmap_index.py`, and `620 passed` over the four state readers with the canary. THE INVENTORY IS THE ROUND'S SUBSTANCE AND IT WAS SPOT-CHECKED RATHER THAN TRUSTED: the reviewer re-read `packages/orchestration/repair_loop_v2.py`, `packages/orchestration/pingpong_evidence.py` and `packages/orchestration/job_evidence.py` at the citations the inventory gives and all three resolve exactly as written. THE ROUND'S ONE DECLARED DEVIATION IS THE REVIEWER'S, NOT THE WORKER'S, and it is recorded in `.agent/prose_slips.md`: G5 ordered the reconstruction as the LTO slice "plus two newlines", while constraint 2 defines a slice's text as already carrying one trailing newline, so the two readings differ by a byte and cannot both hold. The worker measured both, applied the plain pair replacement, and declared the contradiction instead of correcting a slice — which is exactly what constraint 2 asks for. The reviewer confirms the landed bytes are the correct ones: the applied file equals the pair replacement plus one newline plus the gate slice, byte for byte. TWO SPEC CONTRADICTIONS THE INVENTORY MEASURED ARE RULED THIS ROUND rather than left to be rediscovered at T001, as DECISIONS F037 D1 and D2 and as amendments A1 and A2 of `docs/roadmap/features/T5_F037.md`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0715 — Low, A TEST DOCSTRING COUNTS THE SERVED JOB ENDPOINTS AND THE SERVER HAS CARRIED ONE MORE SINCE F031 LANDED. Raised by the reviewer at the F037 R1 gate; the worker found and named the mismatch under the standing staleness gate and correctly minted no id, because its block ordered none. `tests/ui_server/test_command_channel.py`, in the docstring of `_do_get_route_facts`, reads "The thirteen job endpoints live in a dict literal inside `do_GET`", and the `handlers` dict literal in `packages/orchestration/ui_server.py::do_GET` holds FOURTEEN keys. THE SENTENCE WAS TRUE WHEN IT WAS WRITTEN AND WENT STALE UNDER A LATER FEATURE, which is why it is registered rather than blamed: measured by the reviewer, the dict held thirteen keys at `aa2b9048`, the commit that wrote the docstring, and thirteen still at `a164317b`; the fourteenth key, `"decisions"`, was added by `ce462ecc` when F031 exposed the decision inbox as a read endpoint, and nothing swept the prose that counted the old set. LOW AND NOT MEDIUM because the gate it sits in is NOT blind: the same docstring says the list is "derived rather than transcribed", and the test really does walk `do_GET` by AST, so a fourteenth endpoint entered that walk for free and the suite is green at `69f6478c` — the count is wrong only in the prose a reader searches by. THIS IS NOT A DUPLICATE OF `R-0644`, and the neighbour is named so a later reader does not re-litigate it: R-0644 is a REVIEWER-AUTHORED DECISION paragraph in `.agent/decisions.md` whose route arithmetic was wrong AT THE MOMENT IT WAS WRITTEN, and it explicitly records that the `handlers` dict "yields thirteen, which is right" as measured at `a164317b`. That entry is therefore correct about the same dict at its own commit, and this finding is the SEPARATE fact that the dict has since grown; resolving one does not resolve the other. Nor is it `R-0427`, which is a stale claim in a module docstring under `packages/`, a different file and a different claim. COUNTER-MEASURE: delete the numeral rather than update it. The docstring's own next clause — "adding one puts it in the walk for free" — is the property that matters and is the one a reader needs, so "The job endpoints live in a dict literal inside `do_GET`" carries the whole meaning and cannot go stale again, which is the counter-measure `docs/agents/planner_reviewer_prompt.md` §3 item 16 states for exactly this shape. OPEN.
<<<END RECORDR2

<<<SLICE SLIPR2
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
<<<END SLIPR2

<<<SLICE DECR2
## DECISION F037 D1 (2026-08-28) — `binary` is a VIEWER status this feature defines, and `review_subject`'s vocabulary is deliberately not widened

CONTEXT. `docs/roadmap/features/T5_F037.md` specifies a JSON contract whose
`status` field is one of `modified|added|deleted|renamed|binary`. The F037 R1
inventory measured that no vocabulary in this repository carries `binary` as a
status. `packages/orchestration/review_subject.py` defines seven — `added`,
`modified`, `deleted`, `renamed`, `copied`, `type_changed` and `dirty` — mapped
one-for-one from the `git diff --name-status` letters `A M D R C T`. Binary-ness
is not among them because git does not report it as a status letter: a binary
file comes back `M` or `A` exactly like a text file, and its binary-ness is a
property of the CONTENT, discovered when the diff body reads `Binary files …
differ`. Where this repository does handle binary today it handles it as a
REFUSAL rather than a status, in four separate places the inventory names:
a blocker in `provider_trust.py`, an omission reason in `diff_repair.py`, a
refusal in `source_apply.py` and a rendered placeholder in `pingpong_loop.py`.

CHOSEN. F037's parser emits the contract's five-value `status` as its OWN
viewer-facing vocabulary, deriving `binary` from the diff body's binary marker
and the other four from the git status letter. `review_subject.py` is NOT
touched, and its seven-value vocabulary keeps its one-for-one relationship with
the git letters.

ALTERNATIVES CONSIDERED. (a) Widen `review_subject.STATUS_*` with `binary`:
rejected because it would break the property that makes that vocabulary
checkable — every constant maps to a letter git actually emits — and because
the inventory found equality guards pinning that set, which such a change would
turn red for no gain to any existing reader. (b) Drop `binary` from F037's
contract: rejected because the feature file's Acceptance requires binary
placeholders to render, and a viewer that cannot say "this file is binary" must
either lie or show an empty diff. (c) Carry a separate `is_binary` boolean
beside a four-value status: rejected as a third vocabulary for one fact, when
the contract already specifies a single field and F033 will version it anyway.

CONSEQUENCE. The two vocabularies are deliberately different and that
difference is documented where a reader searches for it — amendment A1 of
`docs/roadmap/features/T5_F037.md` says so in the feature file, and the parser
module's header will say so at T001. `copied`, `type_changed` and `dirty` are
NOT rendered by the viewer's v1 and the JSON version field is what F033 uses to
widen the set.

REVERSE by deleting amendment A1 from `docs/roadmap/features/T5_F037.md` and
this decision; the contract in the Design section above A1 is then the spec
again, unamended.

## DECISION F037 D2 (2026-08-28) — the read endpoint keys on task run and job, and the attempt parameter is dropped from v1

CONTEXT. `docs/roadmap/features/T5_F037.md` specifies the diff endpoint as
"a read endpoint per task/attempt" and its edge-case section says "the endpoint
takes an attempt parameter". The F037 R1 inventory measured that NO per-attempt
diff exists anywhere in this repository. Diffs are persisted at exactly two
scopes: `task_runs/<task_id>/safe.diff` per TASK RUN, and `workspace.diff` per
JOB, both under a job's evidence directory. The module that owns repair
attempts, `packages/orchestration/repair_loop_v2.py`, does not merely lack a
diff — it FORBIDS one in its records, listing diffs among the raw content its
schema excludes and carrying `"diff --git"` in its raw-marker rejection tuple.
`self_dogfood_execution.py` persists an attempt record and a request text, and
no diff file. The nearest per-attempt artifact, `patch_intent_diff_preview`, is
documented in its own source as "NOT a real patch; read-only" and is stripped
from review bundles and named on three separate redaction lists.

CHOSEN. The v1 endpoint takes a TASK RUN and falls back to the JOB scope, and
carries NO attempt parameter. The feature file's attempt clause is amended to
record why, and the JSON contract's version field is the seam through which a
later feature adds the parameter if per-attempt diffs ever become real.

ALTERNATIVES CONSIDERED. (a) Persist a diff per attempt: rejected on two
independent grounds — `evidence formats` is named in this feature's own
Do-not-touch, and writing diffs into attempt records would reverse a deliberate
redaction rule that three modules enforce, which is far outside a viewer's
scope. (b) Accept an `attempt` parameter and serve the task-run diff under it:
rejected as a false live indicator, which is a block condition under
`docs/agents/planner_reviewer_prompt.md` §4 item 5 — a parameter that does not
select anything is a lie the API tells every caller. (c) Block the feature until
per-attempt diffs exist: rejected because the viewer's whole value is readable
diffs and the two scopes that DO exist carry them.

CONSEQUENCE. The feature file's Acceptance is met without the attempt
parameter, and the absence is documented rather than silent — amendment A2 of
`docs/roadmap/features/T5_F037.md` states it where a reader would search for
it, per the deliberate-absence convention in `AGENTS.md`.

REVERSE by deleting amendment A2 from `docs/roadmap/features/T5_F037.md` and
this decision, restoring the attempt parameter to the endpoint spec.
<<<END DECR2

<<<SLICE DFROM
## Design (binding specifics)
<<<END DFROM

<<<SLICE DTO
## Design (binding specifics)
> Amended below — see "Design amendments" at the end of this file. Where an
> amendment conflicts with this section, the amendment wins.
<<<END DTO

<<<SLICE AMENDF037
## Design amendments

> Added 2026-08-28 at F037 R2, after the R1 source inventory
> (`.agent/f037_inventory.md`) measured assumptions in the Design, Task
> slicing and Edge-case sections above that the source does not meet. The
> sections above are left as written — this file records how the design MOVED,
> and the amendments below win where they conflict with it. Full reasoning,
> alternatives and reversal instructions: `.agent/decisions.md`, DECISION
> F037 D1 and D2.

**A1 — `binary` is a VIEWER status F037 defines, and `review_subject`'s
vocabulary is not widened (DECISION F037 D1).** No vocabulary in this
repository carries `binary` as a file status.
`packages/orchestration/review_subject.py` defines seven — `added`, `modified`,
`deleted`, `renamed`, `copied`, `type_changed`, `dirty` — mapped one-for-one
from the `git diff --name-status` letters, and git reports a binary file with
the same letter as a text file. Binary-ness is a property of the diff BODY, and
this repository treats it today as a refusal or an omission in four modules,
never as a status. F037's parser therefore emits the five-value `status` of the
contract above as its OWN viewer vocabulary, deriving `binary` from the diff
body's binary marker; `review_subject.py` is not touched. The viewer's v1 does
not render `copied`, `type_changed` or `dirty`, and the JSON version field is
how F033 widens the set.

**A2 — the endpoint keys on task run and job; there is no attempt parameter in
v1 (DECISION F037 D2).** "A read endpoint per task/attempt" and the edge-case
clause "the endpoint takes an attempt parameter" cannot be built: no
per-attempt diff exists. Diffs are persisted at exactly two scopes,
`task_runs/<task_id>/safe.diff` per task run and `workspace.diff` per job, both
under a job's evidence directory. The module owning repair attempts forbids
diffs in its records outright, and the nearest per-attempt artifact is
documented in its own source as not a real patch and is stripped from review
bundles. Serving the task-run diff under an `attempt` parameter would be a
false live indicator, so the parameter is dropped from v1 and the JSON version
field is the seam a later feature uses if per-attempt diffs become real.

**A3 — T001 builds a NEW parser module; the existing reader is not extended
(the R1 inventory, `.agent/f037_inventory.md`).** One structured unified-diff
reader exists, `packages/orchestration/review_scope.py`, and it discards every
field the contract needs: its hunk regex does not capture old line numbers, it
records no per-line kind because only added lines reach its output, it drops a
rename's old path, and it never sees a binary file at all. Its two consumers
state in their own source that they hold no parser, so widening it would change
what they read. The new module owns the contract, and `review_scope.py` is left
alone.
<<<END AMENDF037
