── STEP R2 — F086 Release capability (REPAIR of R1) ──────────

Goal:
Repair the R1 carry. Thirty-nine multi-line findings were truncated to their
headline when `.agent/live_review.md` was reset, destroying 52917 characters of
the permanent finding record. Register that defect and the gate defect that let
it pass, restore every truncated paragraph verbatim from the pre-reset blob, and
prove the restoration with a check that demonstrably fails on the corrupt state.
No production code, no packaging work.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r2.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN2 slice, whole file
  C2  findings persist FIRST: append R0572 then R0573 to
      `.agent/live_review.md`
  C3  the repair: restore the truncated finding paragraphs
  C4  append the DONE1 slice to `.agent/live_review.md`
  C5  rewrite `.agent/handoff.md` (the handback)

C2 precedes C3 because docs/agents/planner_reviewer_prompt.md §4 item 4 requires
authored findings to reach disk in their own commit BEFORE any repair, so a
session that dies mid-round loses the fix and never the finding. C1 precedes both
because §3 pre-emission item 23 requires the plan to advance before any commit
that touches the finding ledger.

Base:
This round starts from `25f7a5af`, the tip of `feature/f086-release-capability`
and the R1 handback commit. The pre-reset record this round restores FROM is the
blob at `76661dc1`, R1's own base. Both SHAs already exist; every range gate
below names `25f7a5af`. Stay on the existing branch — do NOT create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN2, R0572, R0573 and DONE1. Every slice's bytes end with a
single trailing newline, and PLAN2 is the COMPLETE file including that newline.

Append convention:
R0572, R0573 and DONE1 are EOF-APPENDS into `.agent/live_review.md`, defined as
pure concatenation: the existing file content, then the slice bytes exactly as
extracted. Each slice's own leading blank line is INSIDE the slice, so nothing is
prepended and nothing is stripped. No FROM/TO pair exists anywhere in this block.

──────────────────────────────────────────────────────────────

The defect being repaired, measured by the reviewer:

At `25f7a5af`, 152 finding ids are carried in `.agent/live_review.md`. Of the 152
paragraphs they name in the pre-reset blob at `76661dc1`, 113 occupy a single
physical line and 39 span several. All 113 single-line paragraphs are byte-equal
at `25f7a5af`. All 39 multi-line paragraphs are truncated to their FIRST PHYSICAL
LINE — the mismatched set and the multi-line set are the same set, and every
truncated paragraph at `25f7a5af` equals exactly the first physical line of its
original. `OPEN.` is not a universal closing here — 86 of the 152 carried
paragraphs end that way in the pre-reset blob and 75 do after the carry — so the
eleven repaired paragraphs whose original closes with it lost that marker along
with the body. Restoring them adds 589 lines: 628 full paragraph lines replace
the 39 present now.

The cause is this reviewer's own R1 wording, not worker error. R1's C2 item d
said "a finding paragraph is a line matching `^- R-\d+ — `", which literally
DEFINES the paragraph as the line, and the worker applied it literally. R1's G4
then compared HEAD against the base using, in its own words, "the same two
regexes named in C2", so the identical line-based extractor ran on both sides and
reported 152 of 152 equal — a self-consistent proof of nothing. Both defects are
registered below; the second is why this block's restoration gate carries a
NEGATIVE CONTROL rather than only a required reading.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `25f7a5af`, that
   `git branch --show-current` is `feature/f086-release-capability`, that
   `git status --porcelain` is EMPTY and that `.agent/STOP` is absent. If any
   differs, stop and hand off. Do NOT create a branch and do NOT run the Open PR
   Gate: this round continues an existing branch.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r2.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r2.md`; copy that file rather than retyping it (`cp` may be
   denied — `shutil.copyfile` is an acceptable substitute; the gate names the
   byte property, not the tool). Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r2.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN2 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the R0572 slice, then the R0573 slice, to
   `.agent/live_review.md` under the append convention. Commit alone. Nothing
   else in that file changes in this commit.

5. C3 — the repair, one commit, `.agent/live_review.md` only.
   Define the extraction ONCE and use it on both sides:
     Split a file's text on runs of one or more blank lines into BLOCKS. A
     finding paragraph is any BLOCK whose FIRST line matches `^- R-\d+ — `. The
     paragraph is that ENTIRE block — every line of it, including every
     continuation line — and NEVER merely its first line. Its id is read from
     its first line. A resolution line is a line matching `^Done: (R-\d+) — `.
   Then:
   a. Read the blob at `76661dc1` and build the pre-reset paragraph map by id.
      The carried set is every id registered there with no resolution line
      anywhere in that blob.
   b. Read `.agent/live_review.md` at HEAD and build the same map.
   c. The repair set is every carried id whose HEAD paragraph is NOT byte-equal
      to its pre-reset paragraph. The reviewer measured this set as 39 ids at
      `25f7a5af`, the first three being R-0502, R-0503 and R-0504 and the last
      three R-0567, R-0568 and R-0569. Report the set your own run produces and
      flag any difference rather than editing to match.
   d. For each id in the repair set, the HEAD file contains its truncated text
      as a whole line. The reviewer verified at `25f7a5af` that each of those 39
      truncated lines occurs EXACTLY ONCE in that file, so an exact whole-line
      match identifies it unambiguously. Assert that count is 1 for each id
      before replacing, and stop and declare if any is not.
   e. Replace each such line, in place, with the FULL pre-reset paragraph for
      that id, byte for byte. Change nothing else: the header, R-0570, R-0571,
      R-0572, R-0573 and all 113 intact paragraphs are untouched, and no blank
      line is added or removed anywhere.

6. C4 — append the DONE1 slice to `.agent/live_review.md` under the append
   convention. Commit alone. DONE1 states what C3 landed, so it MUST be
   committed strictly after C3; constraint 9 below fixes that order.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~1 % (F086 beansprucht · R1 repariert · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table, every
   gate reading below with its real exit code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. No production code, no test file, and no `docs/` file is touched this round.
   `docs/roadmap/STATUS.md` is already claimed and does NOT change again.
4. Destructive or red-proof verification runs only inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout, which
   satisfies `git status --porcelain` == empty at the handback.
5. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch, and do not create one. Do not create the PR this round.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.
8. The restored paragraphs are restored, never rewritten. Not one byte of a
   pre-reset paragraph may be reflowed, re-wrapped, corrected or shortened, and
   a paragraph that reads oddly stays exactly as it was: this file is the
   permanent record and overwriting landed text is worse than a dated wrong
   sentence (docs/agents/planner_reviewer_prompt.md §3 item 20).
9. ORDERING: C3 is committed strictly before C4, and the restoration gate G5
   below is executed AFTER C3 and BEFORE C4 is committed. DONE1 asserts what
   that gate showed, so this ordering is what makes its text true; it is stated
   here rather than as a SHA because the commit DONE1 describes does not exist
   when DONE1 is authored (§3 item 19 and finding R-0524).

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent. Branch is still
    `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r2.md`, the committed `.agent/authored/f086-r2.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN2 slice as extracted from
    the COMMITTED `.agent/authored/f086-r2.md`, contains `## Goal`,
    `## Next Steps` and a match of `\bF\d{3}\b`, and is under 50 lines. Report
    its sha256 and line count.
G4  `.agent/live_review.md` at HEAD, using the C3 extraction: report registered,
    resolved, `Landed:`, duplicate ids, and resolutions naming an unregistered
    id. REQUIRED as SET comparisons against `25f7a5af`, reporting both sides
    rather than predicting either: registered at HEAD equals registered at
    `25f7a5af` plus exactly `R-0572` and `R-0573`; resolved at HEAD is exactly
    `R-0572`; open at HEAD equals open at `25f7a5af` plus exactly `R-0573`.
    Report the max id and the next free id.
G5  THE RESTORATION GATE, and its negative control — run BOTH halves with ONE
    script, using the C3 extraction, and report both numbers:
    a. REQUIRED: for the carried set, every id's paragraph at HEAD is byte-equal
       to its paragraph in the blob at `76661dc1`. Report compared and equal;
       they must agree, and the reviewer measured the carried set as 152.
    b. NEGATIVE CONTROL, read-only, no checkout: run the SAME comparison with
       the blob at `25f7a5af` in place of HEAD. It MUST report fewer equal than
       compared — the reviewer measured 113 equal of 152 there. A run in which
       half b also reports full equality means the check cannot tell the corrupt
       state from the repaired one and is worthless; report that and hand back
       rather than proceeding.
    Half b is what R1's G4 lacked, which is why R-0573 exists.
G6  Total restored volume: the sum over the carried set of paragraph lengths in
    characters at HEAD equals the sum at `76661dc1`. Report both sums and their
    difference, which must be 0. The reviewer measured the shortfall at
    `25f7a5af` as 52917 characters.
G7  Body restoration, two readings, because `OPEN.` is NOT a universal closing
    in this record and a gate demanding it of every paragraph is unreachable:
    a. Every id in the repair set spans MORE THAN ONE physical line at HEAD.
       Report the count; it must equal the size of your repair set. The reviewer
       measured 0 of 39 multi-line at `25f7a5af` and 39 of 39 in the blob at
       `76661dc1`.
    b. The number of carried paragraphs whose text ends with `OPEN.` is the SAME
       at HEAD as in the blob at `76661dc1`. The reviewer measured 86 there and
       75 at `25f7a5af`; the difference is the 11 repaired paragraphs whose
       original closes that way.
G8  `.agent/live_review.md` at HEAD contains the substring `Steps`, and `<<<`
    occurs 0x in it.
G9  R-0570 and R-0571 at HEAD are byte-equal to the R0570 and R0571 slices in
    the COMMITTED `.agent/authored/f086-r1.md`, and the header of the file is
    unchanged from `25f7a5af`. The repair must not have disturbed them.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN THIS IN THE PRIMARY CHECKOUT, not in a worktree: the reviewer
    measured `160 passed`, exit 0, in the primary checkout at `25f7a5af`, and
    the SAME command in a fresh worktree is red on
    `TestVitestFrontendTestFoundation::test_vitest_passes`, which spawns
    `npx vitest run` and cannot resolve `apps/ui/node_modules` because that path
    is gitignored and therefore absent from every fresh worktree by
    construction. That red is the known R-0480 mechanism and not a base red.
G11 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at `25f7a5af`.
    `tests/docs/` and `tests/orchestration/test_roadmap_index.py` are NOT gated
    this round: no path under `docs/` changes, and the reviewer measured both
    green at `25f7a5af` — 295 passed and 30 passed — before ordering this block.
G12 `git diff --name-only 25f7a5af..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f086-r2.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`.
    Report the real list and flag any difference rather than editing to match.
G13 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2, C3 and C4. C3 exceeds 500 by construction, restoring 628 lines
    of record, and is EXEMPT under AGENTS.md DECISION F104 D1 as the verbatim
    rewrite of a SINGLE `.agent/**` state file; report its number and name the
    exemption. No other commit may exceed 500. C5's own insertion count cannot
    exist while C5's text is being written, so it is reported in your FINAL
    MESSAGE and not in any committed file.
G14 `git log --format=%p 25f7a5af..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.

The two pytest gates run SERIALLY, never two at once: concurrent pytest
processes in this repository produce false reds through port-bound supervisors
(finding R-0518 class), and a false red costs the round.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push the branch with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN2>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1, the merge
commit of PR #206. `.agent/live_review.md` is the source of truth for the open
set, for the next free finding id and for the round map; this file repeats none
of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R2, this round: repair the R1 carry. R1 reset the live-review record and
truncated every multi-line finding paragraph to its headline; this round
registers that defect and the gate defect that let it pass, restores the lost
paragraphs verbatim from the pre-reset blob, and proves the restoration with a
check that is required to fail on the corrupt state. No production code.

## Next Steps
1. R3 — the packaging-shape inventory in `.agent/f086_inventory.md`, MEASURED
   from a real `python -m build` rather than read off the metadata: what the
   built wheel actually contains, whether the UI assets are in it, how the serve
   command resolves that directory, and where a version string could be
   single-sourced from. The reviewer read four starting facts at 76661dc1 —
   `pyproject.toml` declares `version = "0.1.0"` literally, its wheel target
   lists `packages = ["packages", "apps"]` with no package-data rule,
   `apps/cli` defines no `--version` flag, and `ui_server._get_frontend_dist`
   resolves `apps/ui/dist` by walking three parents up from its own `__file__`.
   R3 confirms or refutes each rather than inheriting it.

## Risks
- The finding record is the repository's own memory, and a carry that loses part
  of it is invisible to every existing gate: the four state readers, the docs
  suite and the canary were all green over the truncated file. Until a paragraph
  integrity check exists somewhere durable, every future reset carries the same
  risk.
- `packages = ["packages", "apps"]` collects `apps/ui` wholesale, and
  `apps/ui/node_modules` lives under that path. Whether a built wheel already
  carries that tree is a MEASUREMENT R3 must take.
- Building a wheel spawns npm. That spawn is exactly what F085's guard now
  bounds, so a packaging round that bypasses the seam would silently undo
  stage-1 containment.
<<<END PLAN2>>>

<<<SLICE R0572>>>

- R-0572 — High, THE FEATURE-CLAIM CARRY TRUNCATED EVERY MULTI-LINE FINDING TO ITS HEADLINE, DESTROYING 52917 CHARACTERS OF THE PERMANENT RECORD, AND EVERY GATE THE ROUND RAN WAS GREEN OVER IT. Raised by the reviewer at the R1 gate. Measured at `25f7a5af` against the pre-reset blob at `76661dc1`: 152 finding ids are carried; in the pre-reset record 113 of those paragraphs occupy a single physical line and 39 span several; all 113 single-line paragraphs are byte-equal after the carry and all 39 multi-line paragraphs are not. The mismatched set and the multi-line set are the SAME set, and each truncated paragraph equals exactly the first physical line of its original — so the loss is not corruption but a systematic first-line-only extraction. Of the 39, the eleven whose original closes with `OPEN.` no longer do, because that marker sits at the end of the body that was dropped: `OPEN.` is not a universal closing in this record, and of the 152 carried paragraphs 86 end that way in the pre-reset blob against 75 after the carry. The cause is the reviewer's own R1 wording and not worker error: R1's C2 item d defined the unit as "a finding paragraph is a line matching `^- R-\d+ — `", which literally makes the paragraph the line, and the worker applied it literally and reported honestly under it. What makes this High rather than Medium is not the recoverability — every paragraph survives in the blob at `76661dc1` and this round restores all 39 — but that nothing in the repository could notice: `tests/docs/`, `tests/orchestration/test_roadmap_index.py`, the four `.agent` state readers and the golden-path canary were re-run by the reviewer over the truncated file and returned 295, 30, 160 and 42 passed, all green, because no test reads a finding paragraph's integrity. A defect that destroys the review record while every gate reports success is the exact shape this record exists to prevent. COUNTER-MEASURE, applied in the R2 block that carries this finding: the extraction is defined once, as the whole blank-line-delimited block and never its first line, and the restoration gate carries a negative control that must go red on the corrupt state. The DURABLE counter-measure — a paragraph-integrity check that survives this session — edits the test suite or the integrity gate, neither of which F086 owns, so it routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.
<<<END R0572>>>

<<<SLICE R0573>>>

- R-0573 — Medium, A TRANSPORT GATE RE-USED THE VERY EXTRACTOR IT WAS MEANT TO CHECK, SO IT COULD NOT FAIL. Raised by the reviewer at the R1 gate, alongside R-0572, and registered separately because the two have different fixes: R-0572 is a lost record and R-0573 is a gate that certified the loss. R1's G4 ordered "for each carried id, compare the paragraph at HEAD against the paragraph extracted from the blob at `76661dc1`", and specified the method as "the same two regexes named in C2" — the identical line-based extractor that had produced the truncation. Running one broken extractor on both sides of an equality yields agreement no matter what the files contain, so the gate reported 152 of 152 equal over a file in which 39 paragraphs had lost their bodies, and the worker's handback repeated that reading in good faith. The reviewer measured the true value independently at `25f7a5af` with a block-based extraction: 113 of 152 equal. This is the R-0364 and R-0438 family — a gate whose expected value the reviewer never computed from an independent producer — arriving through METHOD RE-USE rather than through an unreachable colour or a missing path, and it is the reason a green G4 in the R1 handback is not evidence of anything. COUNTER-MEASURE, binding this reviewer from R2 on and visible in the R2 block rather than only in this prose: an equality gate over transported text names an extraction INDEPENDENT of the one that produced the text, and carries a NEGATIVE CONTROL — a state the check is required to REJECT, reported alongside the required reading — so a run in which both halves agree is itself the failure signal. R2's G5 half b is that control. Promoting this rule into the pre-emission checklist at docs/agents/planner_reviewer_prompt.md §3 is what would bind future sessions, and that file is not owned by F086, so the promotion routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490; until it lands, this counter-measure binds only by being written here, which finding R-0452 already showed is weaker than the checklist. OPEN.
<<<END R0573>>>

<<<SLICE DONE1>>>

Done: R-0572 — the truncated finding paragraphs were restored verbatim from the pre-reset blob at `76661dc1`, by an extraction that takes the ENTIRE blank-line-delimited block and never its first line. Not one byte of a restored paragraph was reflowed or rewritten, per constraint 8 of this round's block. The restoration was proved before this text was committed — constraint 9 of that block fixes the gate to run after the repair commit and before this one — by a check carrying its own negative control: every carried id's paragraph byte-equals its pre-reset original at HEAD, while the SAME comparison against the R1 tip `25f7a5af` reports strictly fewer equal than compared, so the check demonstrably distinguishes the repaired record from the corrupt one instead of passing vacuously. The total character volume of the carried set matches the pre-reset record exactly, every restored paragraph is multi-line again, and the count of carried paragraphs closing with `OPEN.` matches the pre-reset record rather than being asserted of all of them. R-0573, the gate defect that allowed the loss, stays OPEN: its durable fix is a checklist edit outside this feature's ownership.
<<<END DONE1>>>
