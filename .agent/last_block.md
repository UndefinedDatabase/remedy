# F033 — Hunk-level diff approval · ROUND 9 · THE FAILED-ROLLBACK TRUTH

SESSION 3 of feature F033. Round 9, rounds so far 9.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R9`.
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

BASE is `0ce3b71a52f229551be7a8bbafb0f405f80d6b8f`, the session-2 close commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 8 passed every gate and the reviewer re-ran all eight itself, including a
fourth mutation the block never ordered. Its verdict has been sitting in
`.agent/handoff.md` since the close of session 2 and is booked into the record by
C2 below, together with one finding raised at that gate. Under operator amendment
amend0827 rule 1 neither buys a round of its own: they ride in the first commits
of this round, which is happening anyway.

THE FINDING IS THIS ROUND'S WORK. `packages/orchestration/hunk_apply.py` builds
its failure message from a FIXED sentence — "No approved hunk was applied; the
repository is unchanged. " — followed by the applier's errors. That sentence is
unconditional. But `_rollback_from_snapshot` in
`packages/orchestration/source_apply.py` appends `rollback_failed:snapshot_not_found`
when the snapshot cannot be loaded, and `rollback_incomplete (N file(s)): …` when
a restore raises `OSError`, and both land in the same `result.errors`. So in
exactly the state where the repository IS changed, the operator is told it is
unchanged, with the contradicting evidence concatenated after the claim.

THE REVIEWER DEMONSTRATED THIS RATHER THAN INFERRING IT, in a disposable worktree
at `0ce3b71a`: with the two-file conflict fixture the suite already builds and
`source_apply.load_snapshot` returning None, the returned message read "No
approved hunk was applied; the repository is unchanged. g.txt: diff hunks did not
apply cleanly; rollback_failed:snapshot_not_found" while `f.txt`'s sha256 on disk
differed from its value before the call. The tree really was changed and the
sentence really did deny it.

WHAT THE REVIEWER READ IN THE CONTROL FLOW AT `0ce3b71a`, and the SPEC depends on
it: `load_snapshot` is imported at module level in `source_apply.py` and is called
in exactly two places — inside `_rollback_from_snapshot`, and in the durable
apply-record block guarded by `if result.success`. On a FAILING apply that second
call is never reached, so substituting `load_snapshot` reaches the rollback and
nothing else. `create_snapshot` and `verify_snapshot` are separate names and are
untouched by that substitution, so the snapshot is still really taken and really
verified before any file is written.

R-0739 CARRIED A CLAUSE BINDING ON THE NEXT BLOCK THAT LANDS A SEAM CHANGE: name,
in the block, the files whose COMMENTS assert the fact the change falsifies, and
grep for the CLAIM rather than read the diff. Discharged here. The reviewer
grepped `nothing-applied`, `falls back to nothing`, `no partial landing`,
`repository is unchanged` and `byte-identical` across the five modules and suites
of this seam at `0ce3b71a`; the hits that assert the falsified absolute are named
in SPEC §2 below, and the two hits in `hunk_subset_diff.py` and at
`hunk_apply.py`'s `_blocked_ids` docstring are about a DIFFERENT property and are
deliberately left alone.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 8 verdict and the R-0740 registration into `.agent/live_review.md`
- C3 two dated lines into `.agent/prose_slips.md`
- C4 the R-0740 repair in `packages/orchestration/hunk_apply.py`
- C5 its tests in `tests/orchestration/test_hunk_apply.py`
- C6 the `Landed: R-0740` line into `.agent/live_review.md`
- C7 the handback

C4 and C5 are SEPARATE COMMITS: the repair and the tests that pin it are two
logical steps, and C6 cannot exist before C4 and C5 have landed the thing it
reports. You write NO `Done:` paragraph — `Done:` is the reviewer's word, and a
worker-authored one is a finding however honestly it is hedged.

## Change set — these paths and nothing else

    .agent/authored/f033-r9.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/hunk_apply.py
    tests/orchestration/test_hunk_apply.py
    .agent/handoff.md

The first is a NEW FILE. This round does NOT touch
`packages/orchestration/source_apply.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/hunk_identity.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`tests/ui_server/test_command_channel.py` or `docs/roadmap/STATUS.md`.
`.agent/context.md` is deliberately NOT touched: the branch, the scope and the
constraints it records are all unchanged by this round.

## SPEC — `packages/orchestration/hunk_apply.py`

An EDIT to an existing module. Everything not named below stays byte-identical.

### 1. The failure sentence becomes DERIVED instead of asserted

Add, beside the three existing failure-code constants, a module-level tuple of
the prefixes `source_apply._rollback_from_snapshot` puts in `ApplyResult.errors`
when the restore it attempted did not finish. They are exactly
`rollback_failed:` and `rollback_incomplete ` — note the trailing space on the
second, which is what keeps the prefix off any longer word. RESTATE them here
rather than importing: they are that function's private message vocabulary, and
importing a private name to read a message would couple this seam to the
applier's WORDING instead of to its BEHAVIOUR. Say that in the comment above
them, and name `packages/orchestration/source_apply.py` as where they come from.

Add a private predicate `_rollback_did_not_finish` — one argument, the applier's
`errors` list, returning whether ANY error starts with ANY of those prefixes —
and a private function `_failure_lead_sentence`, same one argument, returning the
failure message's LEADING SENTENCE chosen by that predicate. Those two names are
FIXED because G6 calls them by name; everything else about their shape is yours.

- predicate false → exactly `"No approved hunk was applied; the repository is
  unchanged. "`, the text that ships today, byte for byte including the trailing
  space.
- predicate true → a sentence that (a) still says no approved hunk was applied,
  (b) says the ROLLBACK did not finish, and (c) says the repository MAY still
  hold part of the change. It must NOT contain the substring
  `the repository is unchanged`. The reviewer's own wording, which you may use
  verbatim or improve: `"No approved hunk was applied, and the rollback did not
  finish, so the repository may still hold part of the change — inspect it before
  re-diffing. "`, trailing space included.

The failure return then uses that function in place of the fixed string. The
`"; ".join(result.errors) if result.errors else "The applier reported failure."`
tail is UNCHANGED, and so is everything else about that return: `applied` false,
`landed` empty, `blocked` from `_blocked_ids`, and `code` still
`HUNK_APPLY_CONFLICT`. THE CODE DELIBERATELY DOES NOT CHANGE and no fourth code
is added — `conflict` is correct in this case, nothing machine-readable is wrong,
and a new code would make every existing caller's match incomplete for a state
that is a strictly worse version of the one it already handles. Write that
absence into the comment, in the idiom this module already uses for its
deliberate absences.

The files are NOT re-named in the new sentence: `rollback_incomplete (N file(s)):
a; b` already names them and is concatenated after it. Say so in a comment, so
the next reader does not add a second naming that could drift from the first.

### 2. The comments that assert the absolute the fix retires

Repair each, keeping its WHY intact and stating the new truth in the present
tense. These are the grep hits named above:

- The module docstring's atomicity paragraph says a conflict inside the approved
  set "already falls back to nothing-applied". True only when the rollback
  finishes. Keep the point it is making — that the atomicity is INHERITED and a
  second rollback written here would be a second answer to one question — and
  state the exception: when the applier reports its own rollback did not finish,
  the fallback did not complete either, and this module's job is then to SAY so
  rather than to repair it.
- The same paragraph's closing sentence, "``landed`` is EMPTY whenever
  ``applied`` is false, because there is no partial landing for a caller to
  report". The first clause stays TRUE and stays. The reason is what is now
  wrong: there can be a partial state on disk. Give the real reason — this module
  learns which hunks landed only from a SUCCESSFUL apply, so on failure it has no
  per-hunk answer to give, and the message is where a partial state is reported.
- `tests/orchestration/test_hunk_apply.py`'s module docstring lists the
  properties in order and calls the conflict case "leaves every file
  BYTE-IDENTICAL, which is this round's reason to exist". That property is still
  pinned and still true of a rollback that finishes. Extend the list with the
  properties C5 adds, and scope the byte-identical claim to the rollback that
  completed. Do this in C5, with the tests, not in C4.

## SPEC — `tests/orchestration/test_hunk_apply.py`

An EDIT. The eight existing tests stay, unchanged. The helpers `_repo_with`,
`_tree_digests`, `_approved_job` and `_conflict_scenario` already do everything
these tests need — reuse them and add none.

Add the tests listed below. The first is the property; the others are its
discriminators, and without them the first passes under a predicate that simply
returns true always.

1. A ROLLBACK THAT COULD NOT RUN IS NOT REPORTED AS AN UNCHANGED REPOSITORY.
   Take `_conflict_scenario`, hash the tree with `_tree_digests`, then
   `monkeypatch.setattr` on `packages.orchestration.source_apply`'s
   `load_snapshot` so it returns None, and call `apply_approved_hunks` with the
   permissioned job. Assert ALL of: `applied` is false; `code` is
   `HUNK_APPLY_CONFLICT`; the message does NOT contain `the repository is
   unchanged`; the message DOES carry `rollback_failed:snapshot_not_found`
   through from the applier; AND — this is the assertion that makes the test
   about the world rather than about wording — the tree digests AFTER the call
   DIFFER from the ones before, with `f.txt` named as the file that differs and
   `g.txt` as one that does not. A message assertion with no disk assertion
   beside it would pass just as well if the sentence were still a lie.
2. A ROLLBACK THAT FINISHED STILL SAYS THE REPOSITORY IS UNCHANGED. The same
   `_conflict_scenario` with NO monkeypatch: the message contains `the repository
   is unchanged`, and the tree digests are EQUAL before and after.
3. A FAILURE THAT NEVER REACHED A FILE STILL SAYS THE REPOSITORY IS UNCHANGED.
   Use `_approved_job(allow_write=False)` on the same fixture: the applier
   refuses on the capability before touching anything, no rollback vocabulary
   appears, the message contains `the repository is unchanged`, and the tree
   digests are EQUAL before and after.

Name each test for the property it pins, in the file's existing style.

## The slices

<<<SLICE PLANF033R9
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
| landing the subset all-or-nothing | done | round 8, on `source_apply.py` |
| the seam tells the truth about a failed rollback | open | this round, R-0740 |
| the hunk-decision ledger in evidence | open | |
| the write-door command and its exposure | open | needs the door's effect ruled |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Repair R-0740: the apply seam's failure sentence is DERIVED from the
   applier's errors, so a rollback that did not finish is never reported as an
   unchanged repository, and the comments asserting the old absolute go with it.
2. Then the hunk-decision ledger — approved, rejected and pending hunks with the
   rejection reasons kept VERBATIM. It moves ahead of the write door because it
   is what the door's effect writes.
3. Then the write door, opened by a DECISION that first rules what its effect IS.
   `packages.orchestration.hunk_apply` imports `source_apply`, the first entry of
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`, so a door
   importing the seam runs the applicator inside the HTTP handler and defeats the
   P3 contract by naming a module the list has not caught up to.
4. Then T003: rejection reasons quoted verbatim into the next repair prompt, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- The subset builder refuses rather than shrinking a diff silently, and every
  later caller must keep that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R9

<<<SLICE RECORDF033R9
Gate: F033 R8 — LANDING THE SUBSET ALL-OR-NOTHING. THE ROUND PASSED. All eight gates were re-executed by the reviewer at `a2248b7b` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 23191 bytes at sha256 `18bc25bd…65061ab3`, byte-identical to the reviewer's own pre-emission original, with ONE blob id at C0b. THE RECORD APPEND at `6dcbc15e` reconstructs 1466257 plus one newline plus 4877 to 1471135, the committed blob exactly, base a byte PREFIX, N counted at 1, the last unit equal to the slice's paragraph, and a byte flipped at offset 1466758 inside that paragraph rejected by BOTH readers. THE LEDGER: registered 300, `Done:` 45 over 43, `Landed:` 12 and the open set 257 ALL UNMOVED, `Gate:` 124 to 125, and `^Gate: F033 R7 — ` exactly 1. THE MODULE: `ruff` exits 0; the AST import set holds `hunk_subset_diff`, `source_apply` and `structured_patch` and NEITHER `permissions` NOR `approval_queue`, so the "no second permission boundary" claim is measured rather than asserted; the three codes carry exactly `subset_refused`, `conflict` and `nothing_to_apply`; and `apply_approved_hunks` and `HunkApplyOutcome` match the ordered signature and field list. THE MUTATIONS were reproduced in the reviewer's own disposable worktree at `ee4fbaeb`, the import first proved to resolve inside it: the UNMUTATED CONTROL is a real exit 0 at 8 passed, reporting success on a failed apply is exit 1 at 4 failed, calling the applier after a refusal is exit 1 at 1 failed, and flattening the blocked-id attribution is exit 1 at 1 failed. THE REVIEWER THEN RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED — filling `landed` with the selected ids on the FAILURE path — and it went RED at 3 failed, so the "`landed` is empty whenever `applied` is false" contract is genuinely pinned and not merely written. THE SUITES were re-run SERIALLY, every REAL exit 0: `test_hunk_apply.py` 8, `test_source_apply.py` 34, `test_hunk_subset_diff.py` 17, `test_hunk_approval.py` 30, `test_resource_safety.py` 21 and the canary 42. THE STRUCTURE: six single-parent commits of 341, 223, 16, 2, 207 and 294 insertions, all under 500, the path set matching in BOTH directions with `.agent/handoff.md` the sole expected absence, residue 0 in every target, `git ls-files .remedy-wt` 0, and all seven do-not-touch paths byte-identical across the round. THE WORKER CORRECTED THE REVIEWER AND WAS RIGHT: the block asserted that a synthesised patch "must set `target_paths` … or it fails validation", and `unsafe_path_issues(())` returns `[]`, which the reviewer re-ran itself — so the consequence overshot the measurement. Setting `target_paths` is still correct and was done. THE GATES SAW EVERYTHING THEY WERE POINTED AT AND ONE THING THEY WERE NOT POINTED AT WAS WRONG: reading `_rollback_from_snapshot` rather than any gate is what raised R-0740 below, and no gate this block ordered could have found it, because the block never ordered the failure MESSAGE examined and the worker wrote exactly what the SPEC described.

- R-0740 — Medium, THE APPLY SEAM TELLS AN OPERATOR THE REPOSITORY IS UNCHANGED IN THE ONE CASE WHERE IT MAY NOT BE. Raised by the reviewer at the F033 R8 gate by reading `_rollback_from_snapshot` rather than by any gate, measured at `a2248b7b`, and DEMONSTRATED by a run at `0ce3b71a` before this registration was written. THE STATE ON DISK at `a2248b7b`: `packages/orchestration/hunk_apply.py`'s failure return builds its message as the fixed sentence "No approved hunk was applied; the repository is unchanged. " followed by `"; ".join(result.errors)`. That sentence is UNCONDITIONAL. But `_rollback_from_snapshot` in `packages/orchestration/source_apply.py` appends `rollback_failed:snapshot_not_found` when the snapshot cannot be loaded, and `rollback_incomplete (N file(s)): …` when a restore raises `OSError`, and both land in that same `result.errors`. So in exactly the state where the repository IS changed — a partial apply whose rollback did not complete — the operator is told it is unchanged, with the contradicting evidence concatenated after the claim. THE DEMONSTRATION, run at `0ce3b71a` in a disposable worktree on the two-file conflict fixture the suite already builds, with `source_apply.load_snapshot` substituted to return None: the returned message read "No approved hunk was applied; the repository is unchanged. g.txt: diff hunks did not apply cleanly; rollback_failed:snapshot_not_found" while `f.txt`'s sha256 on disk differed from its value before the call and `g.txt`'s did not — so the tree really was part-changed and the sentence really did deny it. That substitution reaches the rollback and nothing else: `load_snapshot` is called in exactly two places in `source_apply.py` at that commit, and the second sits under `if result.success`, which a failing apply never reaches. WHY MEDIUM RATHER THAN LOW: `docs/roadmap/features/T5_F033.md`'s Acceptance requires that "every partial state renders truthfully in viewer and report", and a half-rolled-back worktree is precisely the partial state this feature exists to render honestly; the sentence is also the one an operator acts on when deciding whether to re-diff or to inspect the tree by hand. It is not Higher because `code` is correct in that case, nothing machine-readable is wrong, and no data is lost. FIX: derive the sentence from the errors rather than asserting it — when any error carries the applier's rollback vocabulary, say the rollback did not finish and that the repository may still hold part of the change, and reserve "the repository is unchanged" for the case where it is known. Keep `code` as `conflict`: a fourth code would make every existing caller's match incomplete for a state that is a strictly worse version of the one it already handles. NOT A GATE FAILURE of round 8: the block never ordered this message examined, and the worker wrote exactly what the SPEC described.
<<<END RECORDF033R9

<<<SLICE SLIPSF033R9
2026-08-29 · F033 R8 · The block's "TWO CONSTRAINTS" paragraph said a synthesised patch "must set `target_paths` … or it fails validation", and `unsafe_path_issues(())` returns `[]`, so an unset `target_paths` would not in fact fail validation; every measured fact beside it was true and only the inferred consequence overshot, which the worker re-derived and declared.

2026-08-29 · F033 R8 · The block's G6 ordered the sha256 of "the target file" before and after the conflict call, in the singular, while a rollback can only be demonstrated with TWO files — a single-file conflict never reaches the applier's writer, so equal digests would prove ordering rather than restoration; the worker built the two-file fixture the property needs and reported both digests.
<<<END SLIPSF033R9

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C6, so the handback at C7 can quote all of them.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C7,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r9.md` and of `.remedy-wt/f033-r9-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r9.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1471135 bytes, plus one newline plus RECORDF033R9 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R9 — report it
  — and compare the LAST N blank-line units of the C2 blob against the slice's
  paragraphs IN ORDER. NEGATIVE CONTROL at an offset your script PROVES lies
  inside the FIRST appended paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2 and C6.** At BASE, at C2 and at C6 count `^- R-\d+ — `
  with distinct ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  and `^Gate: F\d+ R\d+ — `; report the open set at all three. Ordered:
  registered 300 to 301 at C2 with the ADDED id exactly `R-0740` and UNMOVED at
  C6; `Done:` 45 lines over 43 distinct UNMOVED throughout — you write no
  `Done:` paragraph; `Landed:` 12 UNMOVED at C2 and 12 to 13 at C6, the added
  line matching `^Landed: R-0740 — `; `Gate:` 125 to 126 at C2 with
  `^Gate: F033 R8 — ` exactly 1, UNMOVED at C6; the open set 257 to 258 at C2
  and UNMOVED at C6. C6 additionally keeps the C2 blob as a byte PREFIX.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R9 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  19985 bytes, plus one newline plus SLIPSF033R9, byte for byte, with BASE a byte
  PREFIX; report the count of lines matching `^2026-\d\d-\d\d · F033 R8 · ` at
  BASE and at C3, and the count of lines beginning `- R-` in the whole file at
  C3, which must be 0.
- **G6 THE REPAIR AGAINST THE SPEC at C4.** Each as a measurement over
  `packages/orchestration/hunk_apply.py`. (a) `ruff check` exits 0 — report the
  summary line. (b) By AST, report the FULL import list; it must be UNCHANGED
  from BASE — this repair adds no import, and in particular adds none of
  `packages.orchestration.permissions`, `packages.orchestration.approval_queue`
  or `packages.orchestration.repository_snapshot`. (c) Report the three existing
  failure codes with their values, which must still be exactly `subset_refused`,
  `conflict` and `nothing_to_apply`, and report that no fourth module-level code
  constant was added. (d) Report the extracted signature of `apply_approved_hunks`
  and the field list of `HunkApplyOutcome`; both UNCHANGED from BASE. (e) THE
  SENTENCE ITSELF, measured by CALLING it rather than by counting bytes, because
  the module's own comments legitimately quote it: import the module and print
  `repr(_failure_lead_sentence([]))` and
  `repr(_failure_lead_sentence(["rollback_failed:snapshot_not_found"]))` and
  `repr(_failure_lead_sentence(["rollback_incomplete (1 file(s)): a.txt"]))`.
  The first must be byte-identical to the sentence the BASE module hard-codes,
  trailing space included; the second and third must each be a DIFFERENT string
  that does NOT contain `the repository is unchanged`. Print all three verbatim.
- **G7 THE BEHAVIOUR AND THE MUTATION RED-PROOFS at C5.** First, in the primary
  checkout, `python3 -B -m pytest tests/orchestration/test_hunk_apply.py -q` —
  REAL exit 0, report the count, which must exceed the 8 BASE gives. Then, for
  the failed-rollback test SPECIFICALLY and by name, report the sha256 of `f.txt`
  BEFORE the call and AFTER it and that they DIFFER, and the same two digests for
  `g.txt` and that they are EQUAL. Then, in a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy: the UNMUTATED CONTROL — REAL exit 0,
  report the count. Then, one at a time, reverting fully between each, asserting
  the anchor is UNIQUE in the worktree's own
  `packages/orchestration/hunk_apply.py` before replacing it, and reporting the
  REAL exit code, the failure count and the NAME of each failing test:
  (i) make `_rollback_did_not_finish` return False unconditionally;
  (ii) make `_rollback_did_not_finish` return True unconditionally.
  Each MUST go RED. If either comes back GREEN, report that plainly and do NOT
  adjust anything to force a red — a green mutation is a real finding about the
  tests and the reviewer wants it. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_hunk_apply.py`,
  `tests/orchestration/test_source_apply.py` (34 at BASE),
  `tests/orchestration/test_hunk_subset_diff.py` (17 at BASE),
  `tests/orchestration/test_hunk_approval.py` (30 at BASE),
  `tests/regression/test_resource_safety.py` (21 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C6`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. C7's own numbers are NOT ordered
  here; the reviewer measures C7 at the next gate. Report the range's path set
  against the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/hunk_apply.py` and
  `tests/orchestration/test_hunk_apply.py`: each 0, against
  `.agent/authored/f033-r9.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C6, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 3,
round 9, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Quote the two failure sentences the module now chooses between,
verbatim, the four sha256 digests G7 asks for, and the three test names you wrote
with the property each pins. No length cap. Write no verdict on your own work.
