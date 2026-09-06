STEP T002/5 — F260 · ROUND 12 · THE TEST SIDE OF THE ONE SPELLING
(§3 item 37: every rule line below is exactly sixty-two U+2500 characters, and
no other line of this block's frame is a run of a repeated character.)

Goal:
  Round 11 moved every `_pingpong_runs_dir` reference onto the `data_paths`
  pair, and left fourteen HAND-SPELLED `"pingpong_runs"` path components in
  seven test files untouched, because they never named the deleted helper. Those
  are the test-side twin of finding R-0814: a path built by hand does not follow
  its writer, so each one is a test that will silently keep pointing at the old
  directory when DECISION F260 D1's move happens. Move them onto the pair.

Base: `2ad2d1534ff53a202dc6965909391849b2dd2ca0` (`2ad2d153`). Every reading
quoted in this block was taken by the reviewer at that commit.

Bundle:
  C0a  Save this block verbatim as `.agent/authored/f260-r12.md`.
  C0b  Mirror it into `.agent/last_block.md`.
  C1   `.agent/plan.md` ← the PLAN slice, whole-file replacement.
  C2   `.agent/live_review.md` ← append GATE_R11.
  C3   `.agent/prose_slips.md` ← append the four SLIP lines.
  C4   THE SWEEP — see the SPEC below.
  C5   Handback: rewrite `.agent/handoff.md`.

Change set — nothing outside these paths:
  .agent/authored/f260-r12.md           (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  tests/orchestration/test_failure_wiring.py
  tests/orchestration/test_failure_postmortem.py
  tests/orchestration/test_evidence_bundle.py
  tests/orchestration/test_manual_completion_bundle.py
  tests/orchestration/test_pingpong_cli.py
  tests/orchestration/test_job_stop_integration.py
  tests/cli/test_task_input.py

──────────────────────────────────────────────────────────────
MEASURED AT THE BASE — the complete site list, do not re-derive it

The quoted token `"pingpong_runs"` — either quote style — occurs SEVENTEEN times
in NINE tracked files under `packages/`, `apps/` and `tests/`. Two of those files
are NOT swept and the reason is given, so the remaining fourteen sites in seven
files are this round's whole change:

  KEPT — `packages/orchestration/data_paths.py:216` (one site). This is the
    definition. The string has to live somewhere and this is where.
  KEPT — `tests/test_data_paths.py:406` and `:407` (two sites). This is the
    contract test round 11 added, and a test that pins a layout must spell the
    layout it pins — the same reason round 9's `task_jobs` assertion spells its
    own forbidden component.
  SWEPT — the fourteen below:
    tests/orchestration/test_failure_wiring.py:351, 359, 623, 631
    tests/orchestration/test_pingpong_cli.py:281, 283
    tests/orchestration/test_job_stop_integration.py:248, 250
    tests/orchestration/test_evidence_bundle.py:201, 209
    tests/cli/test_task_input.py:146, 155
    tests/orchestration/test_failure_postmortem.py:687
    tests/orchestration/test_manual_completion_bundle.py:142

DO NOT TOUCH `tests/orchestration/test_failure_postmortem.py` LINES 669, 688 AND
689. They contain the substring `pingpong_runs` inside STRING LITERALS that
assert REDACTION OUTPUT — `"/home/user/.data/pingpong_runs/r1/postmortem.json"`
and `"[runtime-data]/pingpong_runs/r1/postmortem.json"`. Those are assertions
about text a function PRINTS, not path construction, and an accessor cannot
produce them. They are invisible to the quoted-token reading above, which is why
the count is fourteen and not seventeen; the reviewer read them before excluding
them. Line 687 in the same file IS a construction and IS swept.

──────────────────────────────────────────────────────────────
SPEC FOR C4 — described, not sliced; you write the code

Replace each hand-built path with the `data_paths` accessor that produces it.
Every site's root is visible in its own line; use the accessor's `root`
parameter rather than re-deriving a root:

  - A site rooted at the DATA ROOT (`resolve_data_root() / "pingpong_runs" ...`
    or `isolate_data_root / "pingpong_runs" ...`) becomes `pingpong_runs_dir()`
    or `pingpong_run_dir(<run id>)` where a run id follows.
  - A site rooted at an EXPLICIT directory (`tmp_path / "data" / "pingpong_runs"`,
    `data_dir / "pingpong_runs"`, `data_root / "pingpong_runs"`,
    `demo_repo / ".data" / "pingpong_runs"`) becomes
    `pingpong_runs_dir(<that root>)` or `pingpong_run_dir(<run id>, <that root>)`.
    Pass the root explicitly; do NOT assume it equals the data root, and do not
    change which directory any test reads.
  - Where a site already ends in `/ <run id>`, prefer `pingpong_run_dir(...)`
    over `pingpong_runs_dir(...) / <run id>`, because the hand-built join is the
    same shape this round exists to remove.

BEHAVIOUR MUST NOT CHANGE. Each edited line must resolve to the SAME path it
resolved to before. Where you are unsure a root is equal, print both paths in a
scratch probe and compare them before committing rather than reasoning about it.

Add the import each file needs, following that file's existing convention
(module-level or function-local — check which, per file, and do not introduce a
second convention into a file that has one).

Re-grep every line number above before editing. They were read at `2ad2d153`
and this round's own commits move them (§3 item 9).

──────────────────────────────────────────────────────────────
CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice or a gate looks wrong,
    apply it as given and DECLARE the defect. Never repair a slice, and never
    reshape code to make a gate go green. Round 11 declared ten deviations and
    nine were upheld; that is the handback working as intended.
 2. Change-set discipline: no path outside the list above. The list bounds
    WRITES, not reads or worktrees.
 3. `.agent/plan.md` stays under 50 lines; the PLAN slice was measured against
    that cap before emission.
 4. THIS ROUND HAS EXACTLY TWO `.agent/` APPENDS — `.agent/live_review.md` and
    `.agent/prose_slips.md` — and no other file is appended to. Both end with
    exactly ONE newline at `2ad2d153`, measured: 918017 bytes and 108734 bytes.
    Derive each recipe from its own target's terminal byte. (Round 11's
    constraint 4 said "both" while three files were appended to, which the
    worker had to catch; this one states the set and the count together so the
    claim is checkable.)
 5. Slice shapes, classified before emission and stated per target: GATE_R11 is
    an APPEND at end of `.agent/live_review.md`; SLIP9 through SLIP12 are an
    APPEND at end of `.agent/prose_slips.md`; PLAN is a whole-file REWRITE of
    `.agent/plan.md`. No pair in this block has a FROM, so no containment test
    applies and no FROM-zero count is ordered anywhere.
 6. `git status --porcelain` is EMPTY at the handback. Destructive checks run
    only in a disposable `git worktree` (self-drive protocol G5).
 7. AGENTS.md throughout: self-review loop before every commit, 500-insertion
    cap counting INSERTIONS only, push after committing, no force push, no work
    on `main`, no merge, no pull request.

──────────────────────────────────────────────────────────────
DONE WHEN — eight gates, each RUN and its real exit code recorded

G1 TRANSPORT — one digest. `sha256sum .agent/authored/f260-r12.md` equals the
   digest named in the delegation that carried this block, and the same digest
   over `.agent/last_block.md`. One reading, not a chain.

G2 THE RECORD. (a) EXACT IMAGE: the post-image at C2 EQUALS
   `pre + b"\n" + GATE_R11 + b"\n"` byte for byte, where `pre` is the file at
   `2ad2d153`; state the measured length. (b) STRUCTURAL: split on `"\n\n"`; the
   last unit with the terminating newline stripped equals GATE_R11; units run
   431 → 432. (c) NEGATIVE CONTROL: flip ONE byte inside the appended paragraph
   and confirm readings (a) AND (b) both reject it, then restore and confirm
   both accept. (d) After C2: `^Gate: ` headers 21, all distinct; registrations
   299 over 299 distinct ids; `^Done: ` 5 lines over 3 distinct ids; the open
   set is 296 BY DISTINCT ID.

G3 THE SLIPS. The post-image EQUALS `pre + b"\n" + SLIP9 + b"\n\n" + SLIP10 +
   b"\n\n" + SLIP11 + b"\n\n" + SLIP12 + b"\n"` byte for byte; blank-line units
   run 139 → 143, a rise of exactly FOUR, one per slip.

G4 THE PLAN. `.agent/plan.md` equals the PLAN slice plus exactly one trailing
   newline, byte for byte, and its line count is under 50.

G5 THE HAND-SPELLED PATHS ARE GONE.
   (a) The QUOTED TOKEN `"pingpong_runs"` (or `'pingpong_runs'`) occurs, over
       every TRACKED `.py` file under `packages/`, `apps/` and `tests/`, in
       EXACTLY THREE places: `packages/orchestration/data_paths.py` once and
       `tests/test_data_paths.py` twice. Report the full `file:line` list rather
       than only the total. Measured at the base: SEVENTEEN sites in NINE files,
       so this gate can fail, and the two surviving files are named rather than
       counted to zero — a zero would be unmeetable, which is the mistake round
       9's G5(c) and round 11's G5(c) each made in a different direction.
   (b) NON-VACUITY, PER FILE: in each of the seven swept files, AST references
       resolving to `pingpong_run_dir` or `pingpong_runs_dir` are NON-ZERO.
       Report the count per file. At the base every one of the seven is ZERO, so
       the reading really distinguishes before from after.
   (c) NO BEHAVIOUR CHANGE: `git diff --numstat` over C4 shows, for every one of
       the seven files, insertions and deletions that are both non-zero and
       within two of each other — a sweep that replaces a spelling neither adds
       nor removes test logic. Report the seven rows. If any row is further
       apart than that, say which and why; do not adjust the code to fit.

G6 THE SUITES, run SERIALLY, each exit code recorded separately, never piped —
   capture each run to a file under `.remedy-wt/` and read the capture, because
   a pipe reports the pipe's exit code and not pytest's:
     `pytest tests/orchestration/ -q -p no:randomly`
     `pytest tests/cli/ -q -p no:randomly`   (carries the canary)
     `pytest tests/test_data_paths.py -q -p no:randomly`
   The reviewer ran all three at the base: `tests/orchestration/` is 12805
   passed and 10 skipped at exit 0, `tests/test_data_paths.py` is 48 passed, and
   `tests/cli/` carries `test_golden_path.py`. Report each passed count. Also
   run `python3 -m apps.cli.grouped integrity check --json` and record `passed`,
   `fail_count` and the check count.

G7 THE MUTATION RED-PROOF, and it is the proof this round is worth a round.
   In a disposable `git worktree` at the C4 commit, `python3 -B`, modules
   confirmed to resolve from THAT worktree:
   (i)   UNMUTATED CONTROL FIRST over the seven swept files: exit code AND
         passed count, per the whole selection.
   (ii)  Change `data_paths.pingpong_runs_dir` to return
         `(root if root is not None else resolve_data_root()) / "pingpong_runs_MUTATED"`.
         Tests in the swept files must now FAIL — because they read the accessor
         rather than a hand-spelled string. Report HOW MANY failed and name at
         least one node id per swept file that fails, or say plainly which swept
         file produced no failure and why.
   (iii) Restore, confirm the control is green again and that `git diff` in that
         worktree is empty.
   A file whose tests do NOT redden under (ii) is still hand-spelling its path
   somewhere the token reading missed; that is a finding about this round, and
   reporting it is worth more than a green gate.
   Name the revert target by PATH and verify the bytes you replace occur EXACTLY
   ONCE in that file before editing (§3 item 25).

G8 LINT AND CLEAN TREE. `python3 -m ruff check` over exactly the seven swept
   files exits 0 — file-scoped on purpose, because `ruff check tests/` is RED at
   the base with pre-existing errors that are not this feature's. Then
   `git status --porcelain` and `git ls-files .remedy-wt` are both EMPTY.

──────────────────────────────────────────────────────────────
HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, `SESSION 3 of feature F260`, branch, commit SHAs, the changed-files table
with its `+/-` column from `git diff --numstat` and never re-derived by eye (§3
item 28), ONE LINE PER GATE with its real exit code, the open-findings count BY
DISTINCT ID, the item-status table, the next expected action, and every
deviation — including any place this block is wrong. No length cap.

──────────────────────────────────────────────────────────────
AUTHORED SLICES

A slice is the bytes of the lines strictly BETWEEN its BEGIN and END marker
lines, joined by `"\n"`, carrying NO trailing newline. The marker lines are
never part of any slice and never reach any file.

<<<BEGIN GATE_R11>>>
Gate: R11 — the F260 R11 entry. R11 GAVE THE PING-PONG RUN STORE ONE SPELLING IN `data_paths` AND DELETED `pingpong_loop._pingpong_runs_dir`, AND RECORDED DECISION F260 D5. VERDICT PASS. Range 2cedf98c..2ad2d153, ten commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; largest insertion count 399, a single `.agent/**` state write, and largest code commit 97, both far under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT: one digest `e2dc8680811953e9119c64eaabd552bdfe5285bafef7bba74b5644a84b777fac` across the reviewer's scratch original, the saved copy at `.agent/authored/f260-r11.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is not a claim about bytes emitted into a prompt. THE RECORD: 912232 to 918017 bytes by exact-image equality, blank-line units 430 to 431, the last unit equal to the slice byte for byte, twenty `Gate:` headers, registrations 299 over 299 DISTINCT ids, `Done:` 5 lines over THREE distinct ids, open set 296 BY DISTINCT ID. THE SLIPS: 105750 to 108734 by the same reading, units 137 to 139. THE DECISION LANDED AS AN INSERTION AND IS PROVED AS ONE: `docs/roadmap/features/T2_F260.md` satisfies `pre[:off] + inserted + pre[off:] == post` byte for byte at `off` 15662 with 3022 bytes inserted, so nothing outside the insertion point moved; `^### DECISION F260 D` matches SIX times with D0, D1, D2, D3, D4 and D5 each exactly once; the D5 heading sits at byte 15663, after D4 at 13191 and before `## Design` at 18684, which is the placement the block ordered; and the file still ends with exactly one newline. THE HELPER IS GONE: `hasattr(pingpong_loop, "_pingpong_runs_dir")` is False, and by an AST reading covering `Name`, `Attribute`, `alias` AND `FunctionDef` over 1030 tracked Python files the name resolves ZERO times, against a non-vacuity control of 138 for `pingpong_run_dir` and 13 for `pingpong_runs_dir`. THE VALUE IS PRESERVED and both new functions honour a `root` argument set to a different directory from the environment root. THE SUITES, re-run serially by the reviewer at the branch tip, all exit 0: `tests/orchestration/` at 12805 passed and 10 skipped in 738 seconds, `tests/test_data_paths.py` at 48, and `tests/test_data_paths.py` with the canary and `tests/docs/` together at 393; `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks; and RUFF over exactly the twenty-nine changed paths under `packages/`, `apps/` and `tests/` exits 0. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY in the reviewer's own disposable worktree at `2be351cc`, control exit 0 at 48 passed: making `pingpong_run_dir` ignore its `root` argument reddens exactly `test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir`, and reviving `_pingpong_runs_dir` in `pingpong_loop` as an UNCALLED `def` reddens exactly `test_pingpong_loop_has_no_runs_dir_helper_at_all`; `git diff` was empty after each restore and the control was green again. NINE OF THE WORKER'S TEN DEVIATIONS ARE UPHELD AND ONE IS DECLINED. Upheld and worth the record: G5(c) as written was UNMEETABLE, because it required the literal `pingpong_runs` to occur only in `data_paths.py` while the new identifier `pingpong_runs_dir` CONTAINS that substring, so every importer is a hit by construction — round 9 wrote an unmeetable ZERO and round 11 an unmeetable ONE, the same defect at two different numbers; the property that actually holds, and that the reviewer confirmed, is that the QUOTED TOKEN `"pingpong_runs"` occurs exactly once under `packages/` and `apps/`, at `data_paths.py:216`. The block's Bundle assigned SPEC (4) no commit slot, so the two ordered guard tests had nowhere to land and the worker created `2be351cc` for them. The block's "measured for you" offsets 13104 and 15565 were CHARACTER offsets presented as BYTE offsets, the real values being 13191 and 15662, which the reviewer re-measured both ways to confirm. And constraint 4 said "both `.agent/` appends" over a round that appended to THREE files, the third being `.agent/decisions.md`, which ends with NO trailing newline and so needed a different recipe than the two the constraint named. DECLINED, with the measurement: the worker read the GATE_R10 slice's sentence "THE SUITES, re-run serially by the reviewer, all exit 0 at 59, 1537 and 203" as describing `tests/test_data_paths.py` and `tests/orchestration/`, and reported the numerals as wrong. They are correct. That sentence names no files, it sits inside the R10 gate record, and it reports the three suite groups the ROUND-10 block's G6 ordered — `tests/test_data_paths.py` with `tests/cli/test_patch_cmd.py` at 59, `tests/cli/` at 1537, and the three-file group at 203 — every one of which the reviewer measured itself during the round-10 review. The numerals the worker compared them against belong to ROUND 11's G6, which names different suites. No correction is owed to the record. THE WORKER'S OWN COUNTS MATCHED THE BLOCK'S CHECKLISTS EXACTLY at 39 production references across seven modules and 97 test references across twenty files, per file, and it flagged that the delegation prose said "roughly 95" while the block's own list summed to 97 — the list being the half that is executed, per §3 item 35.
<<<END GATE_R11>>>

<<<BEGIN SLIP9>>>
2026-09-06 · F260 R11 (reviewer) · Gate G5(c) of the round-11 block required the literal `pingpong_runs` to occur under `packages/`, `apps/` and `tests/` ONLY inside `packages/orchestration/data_paths.py`, and no round could satisfy it: the identifier the same block introduces, `pingpong_runs_dir`, CONTAINS that substring, so every module importing the new accessor is a hit by construction — 51 raw hits across 13 files at the round's own tip. The block even carried the reasoning that would have caught it, noting in the gate itself that a zero would be unmeetable "because `data_paths` is where the string now lives", and then set the bound to one file instead of asking about the right token. THE LESSON: a substring gate over an identifier family is not a gate over the STRING CONSTANT it was written for; name the token — the quoted `"pingpong_runs"` — or the gate measures the vocabulary rather than the spelling. The property that holds, measured by the worker and reproduced by the reviewer, is that the quoted token occurs EXACTLY ONCE under `packages/` and `apps/`, at `data_paths.py:216`. This is the third gate of this shape in three rounds: round 9's G5(c) asserted an unmeetable ZERO, round 11's an unmeetable ONE. Reviewer-authored unmeetable gate clause; the round's real property holds and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP9>>>

<<<BEGIN SLIP10>>>
2026-09-06 · F260 R11 (reviewer) · The round-11 block's Bundle listed C5 as SPEC (1) and (2) and C6 as SPEC (3), and gave SPEC (4) — two new guard tests the block ordered in full, with their names, their readings and their non-vacuity controls — NO COMMIT SLOT AT ALL. The worker landed them as an extra commit `2be351cc` and declared it. THE LESSON is §3 item 35 exactly, and it is the second time this session that a block's prose has promised what its enumeration did not hold: the Bundle is the half that is EXECUTED, because a worker commits by it, so every SPEC section is resolved against the Bundle item by item before emission and anything the prose orders that the list does not carry is added to the list. The counter-measure is mechanical and takes one reading — enumerate the SPEC sections, enumerate the Bundle's commits, and check that each of the former is named by one of the latter. Reviewer-authored prose/enumeration mismatch, caught and repaired by the worker inside the round; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP10>>>

<<<BEGIN SLIP11>>>
2026-09-06 · F260 R11 (reviewer) · Gate G4(b) of the round-11 block offered the worker two offsets "measured at the base for you" — 13104 for the D4 heading and 15565 for `## Design` — and ordered an insertion proof stated in BYTES. Those two numbers are CHARACTER offsets. The reviewer's pre-emission checker read the feature file with `Path.read_text()` and used `str.index`, and `docs/roadmap/features/T2_F260.md` carries em dashes and other multi-byte characters, so the byte offsets are 13191 and 15662 — the worker's correct `off` of 15662 would have looked out of range against the range the block supplied. The worker measured both and declared the discrepancy; the reviewer re-measured with `bytes.index` and confirms every figure. THE LESSON: an offset is only a number until its UNIT is named, and a proof stated in bytes must be prepared in bytes — read the file with `read_bytes()` and index the bytes whenever the value will be handed to someone as a byte offset. §3 item 12 already requires a dry run to use the gate's exact command; this is the same rule one level down, at the gate's exact TYPE. Reviewer-authored unit error in a gate's supplied constants; the insertion itself is correct and proved by whole-file identity, and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP11>>>

<<<BEGIN SLIP12>>>
2026-09-06 · F260 R11 (reviewer) · Constraint 4 of the round-11 block opened "Both `.agent` appends target files ending with exactly ONE newline at `2cedf98c`" and named `.agent/live_review.md` and `.agent/prose_slips.md`, while the same block's own Bundle appended to a THIRD file: `.agent/decisions.md`, which the block's C4 ordered the DECISION_D5 text appended to. That file ends with NO trailing newline at 836338 bytes, so the recipe the constraint supplied was wrong for it, and the worker had to derive a different one and say so. THE LESSON is the append rule this repository already carries — an append recipe is a function of ITS OWN target's terminal byte and is derived per target, never generalised across a set — arriving through the word "both", which is a COUNT of the block's own parts and therefore §3 item 11's forbidden shape: a convention paragraph names its units and states no count of them. Had the constraint listed the three files instead of counting two, the missing recipe would have been visible while the block was being written. Reviewer-authored miscount in a convention paragraph; the worker derived the correct recipe and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP12>>>

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 11 are reviewed and 2 to 11 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, and the run store has one spelling.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE TEST SIDE OF THE ONE SPELLING. Round 11 moved every `_pingpong_runs_dir`
reference onto `data_paths.pingpong_runs_dir` / `pingpong_run_dir` and left
fourteen hand-spelled `"pingpong_runs"` path components in seven test files,
which never named the deleted helper and so were invisible to that sweep. They
are the test-side twin of R-0814 — a path built by hand does not follow its
writer — and this round moves them onto the pair.

## Next Steps

- THE RUN MOVE, which needs its own session: `pingpong_runs_dir` and
  `pingpong_run_dir` collapse into `runs_dir` and `run_dir`, AND the run LOG at
  `<data_root>/runs/<job_id>/` must move to the run id in the SAME commit, or
  `timeline.load_run_events` reads one directory keyed two ways — DECISION F260
  D0 measured that collision. It needs a fresh reading of `run_log.py` and
  `timeline.py`, which no round so far has touched.
- The unified record's own fields, and the Mission extension (order, contract,
  mission plan, job refs), which is the rest of T002.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- `<data_root>/runs/` is keyed by JOB id today and D1 keys it by RUN id. Every
  reader of the old shape moves in the same commit as its writer.
- `<data_root>/jobs/` holds both `<uuid>.json` files and `<16hex>/` directories.
  Any new reader of that directory must make the same file/directory
  distinction the two matchers make.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLAN>>>

──────────────────────────────────────────────────────────────
