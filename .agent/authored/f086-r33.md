── STEP R33 — F086 Release capability ─────────────────────────
Goal:        Record R32's verdict, resolve R-0598 now that the branch's own CI
             run is green, and register R-0599 against the pair-shape reading
             the R32 block declared. No source file changes in this round.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0599, resolve R-0598 and record R32 ·
             C3 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f086-r33.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. No source
             file, no test and no document changes this round. These paths are
             PRESENT at 665c45df and must stay untouched: `hatch_build.py`,
             `tests/test_packaging_smoke.py`, `docs/system/release-capability-v1.md`,
             `docs/roadmap/STATUS.md`, `README.md`, `pyproject.toml`,
             `.agent/context.md`, `.agent/candidates.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f086-r33.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f086-r33.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL to
   each other; the reviewer stated its expected digest when it delegated, and
   that digest cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. PLAN33 is a WHOLE-FILE replacement of
   `.agent/plan.md`, and FIND0599, DONE0598 and RECORD32 are an APPEND to
   `.agent/live_review.md`. The reviewer ran the containment test over this
   block's own extracted slices before emission and it reported no pair to
   classify, so no FROM-count and no FROM-zero count is ordered anywhere below.
   That test running as code is itself the counter-measure R-0599 names.
4. THE LEDGER APPEND IS BLANK-SEPARATED. The three slices are appended in the
   order FIND0599, DONE0598, RECORD32, each preceded by exactly one blank line
   (R-0578). Nothing already in that file is rewritten, reordered or deleted —
   including the entries R-0599 reports as wrong, which are corrected by the
   dated entry this round appends and never by an edit.
5. YOU NEVER WRITE A `Done:` PARAGRAPH OF YOUR OWN. DONE0598 is reviewer-authored
   text and is applied verbatim like any other slice. You add no second one.
6. THE PULL REQUEST IS NOT MERGED and not touched. #207 already exists for this
   branch; C3 is followed by `git push` only, which updates it. Do not run
   `gh pr merge`, `gh pr create`, `gh pr edit` or any force push. Its merge
   belongs to the next feature's Open PR Gate, which is not this round.
7. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
8. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.

<<<SLICE PLAN33
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and its CI check is GREEN at 665c45df, run 32405232165 — the first
green run this branch has had. It merges at the next feature's Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R33: record R32's verdict, resolve R-0598 — the editable-target exemption, which
the branch's own CI run now proves in the environment that found the defect — and
register R-0599 against the pair-shape reading the R32 block declared. State
files only; no source file, test or document changes.

## Next Steps
1. THE REVIEWER GATES R33. If R33 ends the branch its verdict has no on-disk gate
   entry by construction, and that absence is the terminator rather than a missing
   gate (docs/agents/planner_reviewer_prompt.md section 4 item 13).
2. THE OPEN PR GATE MERGES #207 at the start of the next feature, per AGENTS.md —
   not in this round. The operator may merge it manually at any time instead.
3. F086 STAYS `[x]` IN THE LEDGER. Neither R-0598 nor R-0599 falsifies the
   closure's own claim — a shipped wheel is still refused without UI assets, and
   the accepted evidence names the commit it was taken at — so each correction is
   a dated ledger entry, never a rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- THE GREEN RUN IS A CI RUN, not a wheel install. It proves the dev install and
  the suite, which is what R-0598 broke, and it proves neither risk above.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
<<<END PLAN33

<<<SLICE FIND0599
- R-0599 — Medium — THE R32 BLOCK DECLARED A PAIR SHAPE ITS OWN CONTAINMENT TEST CONTRADICTS, AND THE HANDBACK THEN REPORTED THE UNATTAINABLE COUNT THAT MISLABEL ORDERS. Constraint 3 of the R32 block, saved at `84f30a06`, records one containment reading per pair "quoted here as the test printed it" and gives DOCPAIR as `TO contains FROM: False`, deriving REWRITE from it. DOCTO opens with DOCFROM verbatim — the sentence ending "which DECISION F086 D1 part (b) forbids." — and continues from there, so the test prints True and the pair is APPEND-shaped. Constraint 3 therefore obliged the worker to prove "FROM 1x at dcf351c6 and 0x after" for a FROM the applied file necessarily still carries, and the R32 handback at `665c45df` reports exactly that, grouping DOCPAIR with HOOKPAIR and IMPORTPAIR as rewrites reading "FROM 1x at the pre-commit blob and 0x after". Re-measured by the reviewer at `2be0fbbf`: DOCFROM occurs 1x in `hatch_build.py` AFTER the commit, so that clause is false where it names DOCPAIR while staying true for the other two, whose FROM really does reach 0. Nothing on disk is wrong. The reviewer rebuilt the file independently and `hatch_build.py` at `2be0fbbf` equals its `dcf351c6` blob with DOCPAIR, FNPAIR and HOOKPAIR each applied once and nothing else changed, at sha256 912fe336c0bb4ddcad6e758c22bf887785b5fb1d742f90b1119772e0a3e12d3b over 109 lines. The defect is in the proof text, which is the permanent record. This is the R-0508 and R-0522 class recurring under the very checklist item written for it: item 15 requires the containment test to be RUN and its OUTPUT quoted, and a block that quotes an output the test never produced is indistinguishable on the page from one that measured — the reader cannot tell them apart, which is what makes the rule unenforceable by reading. The counter-measure is mechanical and belongs to the reviewer rather than to any worker: extract the block's own slices programmatically and run the containment test over them in the SAME script that counts the block's lines before emission, so every shape word in the constraints is a value that script printed. R32's own round is the demonstration that the manual form fails while being obeyed, because its constraint 3 asserts the method in the sentence that gets the reading wrong.
<<<END FIND0599

<<<SLICE DONE0598
Done: R-0598 — the editable build target is exempted, and the environment that found the defect is the environment that proves the fix. `hatch_build.py` at `2be0fbbf` gains `build_target_ships_ui_assets`, which answers False only for the target named `editable`, and `RemedyBuildHook.initialize` returns before both packaging rules when it does; `tests/test_packaging_smoke.py` at the same commit gains the `TestEditableBuildsAreNotGuarded` cases, and the reviewer measured that selection rise from 9 passed at `dcf351c6` to 14 at `665c45df`. The closing proof is not a local one. Run 32402941541 against `dcf351c6` died in the workflow's own `pip install -e ".[dev]"` step with `error: metadata-generation-failed` and executed no test at all; run 32405232165 against `665c45df` is the same workflow with the same first step and it is GREEN, so the failure this finding names cannot survive at that commit. The reviewer additionally reverted the two exemption lines inside a disposable worktree at `2be0fbbf`, counting each of them 1x in that file first, and re-ran `python3 -m pytest tests/test_packaging_smoke.py -q -rf`: exit 1 at `1 failed, 10 passed`, naming only `TestEditableBuildsAreNotGuarded::test_an_editable_build_is_allowed_without_built_assets` and failing with the guard's own `ValueError` about `apps/ui/dist/index.html`. The new cases therefore GUARD the fix rather than merely accompanying it, which is the property a resolution has to carry and a passing suite alone never shows.
<<<END DONE0598

<<<SLICE RECORD32
Gate: R33 — the R32 entry. R32 PASSED, and the one finding it earns — R-0599, registered above — is against its proof TEXT and never against anything on disk. Every gate the R32 block ordered was RE-EXECUTED by the reviewer over `dcf351c6..665c45df` rather than read from the handback, and each holds as written except G8's DOCPAIR clause. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f086-r32.md`, the committed `.agent/authored/f086-r32.md` at `84f30a06` and the committed `.agent/last_block.md` at `3d98f5ce` are byte-EQUAL at sha256 840ef1f78d0f9965fe290ff33870c29ac0c51ce336d9c7d601cc9de68ee83464 over 21582 B and 327 lines, the digest the reviewer stated before delegating. THE STATE FILES LANDED AS AUTHORED: `.agent/plan.md` at `6623ae48` byte-equals PLAN32 at sha256 12fc87d55848b7ecfe5f752fdaf274d153751594cd8119079b39e68f17cf6b0c over 42 lines, under the AGENTS.md cap; the pre-C2 blob of `.agent/live_review.md` is a byte-exact PREFIX of the blob at `761683af` whose remainder is a blank line, R-0598, a blank line and the R32 entry, at sha256 cb8296645c09a32caae6335978c921d410b031f2b490001e61c030e46415273d with both blank separators present; the registered set goes 180 to 181 gaining exactly `R-0598`, the resolved set is unchanged at 6, and no `Landed:` line exists at either end. THE TWO SCANS THE CHECKLIST ADDED BOTH RAN AND ONE OF THEM PROVED ITSELF: unquoted `\bHEAD\b` reads 0 over the lines `761683af` ADDS, and the same extractor over `fd166295`'s added lines to the same file reads 3, so the gate is not vacuous; `Gate: R` headers go 29 to 30, the only duplicated key is unchanged and is exactly `Gate: R19 — the R18 entry`, and `Gate: R32 — the R31 entry.` occurs once, sits last, and is followed by text beginning `R31 ` once its leading space is stripped. THE APPLIED BYTES ARE RIGHT WHEREVER THE PROOF TEXT IS NOT: per FILE, `hatch_build.py` at `2be0fbbf` equals its `dcf351c6` blob with DOCPAIR, FNPAIR and HOOKPAIR each applied once at sha256 912fe336c0bb4ddcad6e758c22bf887785b5fb1d742f90b1119772e0a3e12d3b over 109 lines, `tests/test_packaging_smoke.py` equals its blob with IMPORTPAIR applied once plus TESTAPPEND appended at sha256 7da20674a48a32a29f8ae0e657ce461096ae8f8047b832f02bea96cf701a0d8c over 115 lines, and `docs/system/release-capability-v1.md` at `df12d573` equals its `2be0fbbf` blob with ISTPAIR applied once; the code append satisfies section 4.9 ordered equality, its diff adding exactly IMPORTTO's lines followed by TESTAPPEND's, IN ORDER. THE ROUND GATE WAS RE-RUN SERIALLY IN THE PRIMARY CHECKOUT: the packaging selection exit 0 at `14 passed`, rising from the 9 measured at `dcf351c6` by exactly the cases C3 adds; the four-file state-reader selection exit 0 at `160 passed`; `tests/docs/` exit 0 at `295 passed`; the canary exit 0 at `42 passed`; and `python3 -m ruff check hatch_build.py tests/test_packaging_smoke.py` under the repository's own configuration exit 0 at `All checks passed!`. THE RANGE IS WHAT THE HANDBACK DECLARES: eight paths over seven single-parent commits, every `+/-` cell byte-identical to `git diff --numstat`, a maximum insertion column of 327 under the 500 cap, every `git reflog` entry of the round reading `commit:`, each of the ten paths the Change section named as untouched present at `dcf351c6` and absent from the range, and zero marker lines in any target. WHAT R31'S GATES COULD NOT SEE, R32 SETTLED: run 32405232165 against `665c45df` is GREEN — the first green CI run this branch has had — so the amend0820-gate-autonomy work order that R32 opened is discharged, and the pull request's remaining risks are the two the closure line already names.
<<<END RECORD32

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f086-release-capability; `git status --porcelain`
   EMPTY after every commit and at the handback; `git worktree list` reports the
   primary checkout alone, because this round creates none. No reading is taken
   by overwriting a file in the primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f086-r33.md`, of `.agent/authored/f086-r33.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
   Constraint 2 names where the expected digest came from.
G3 PLAN. `.agent/plan.md` at C1 byte-equals PLAN33; report its sha256 and line
   count, that the count is under 50, and that `## Goal`, `## Next Steps` and
   `F086` all occur in it.
G4 LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
   PREFIX of the post-C2 blob, and the remainder is a blank line, FIND0599, a
   blank line, DONE0598, a blank line and RECORD32 — report the remainder's
   sha256 and line count, and that EVERY one of those blank separators is
   present. Report it twice, by two INDEPENDENT extractions that must agree: the
   byte-level remainder above, and a paragraph-level split of the post-C2 blob
   whose last paragraphs are those three slices in that order (R-0572, R-0578).
G5 LEDGER SETS. With `^- R-\d+ — ` as registered and `^Done: R-\d+ — ` as
   resolved, report both counts plus open and `Landed:` at 665c45df and at C2.
   The reviewer measured 181 registered, 6 resolved, 175 open and 0 `Landed:` at
   665c45df. The registered set must gain EXACTLY `R-0599` and lose none, the
   resolved set must gain EXACTLY `R-0598` and lose none, and open must therefore
   read 175 at BOTH ends — report that number rather than assuming it.
G6 ITEM-20 SCAN. Over C2's ADDED lines only, delete backtick-quoted spans first,
   then report the count of `\bHEAD\b` — it must be 0. Run the SAME extractor
   over `fd166295`'s added lines to that file as a RED CONTROL and report that
   count too; a control that does not read above 0 makes the gate worthless.
G7 ITEM-26 HEADER. Report how many lines begin `Gate: R` at 665c45df and at C2,
   which header keys occur more than once at each end, that
   `Gate: R33 — the R32 entry.` occurs 1x, that it is the LAST such header, and
   that the text following it begins `R32 ` once its leading space is stripped.
   The reviewer measured 30 headers at 665c45df, with exactly
   `Gate: R19 — the R18 entry` occurring more than once.
G8 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches no source file, so
   the four files that read that state live are the gate, plus the canary.
   Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q`
   The reviewer measured 160 passed and 42 passed at 665c45df.
G9 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 665c45df..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the eight paths the Change section names as untouched is PRESENT
   at 665c45df and absent from that range; that every commit in the range has one
   parent; that every `git reflog` entry of this round is `commit:`; and each
   commit's insertion column from `git diff --numstat`, every one under 500. Per
   checklist item 28 the same `+/-` cells appear in the handback's `## Commits`
   table and must be byte-identical to the tool's output there. C3's own cell
   cannot exist while C3 is being written, so it belongs to the round report.
G10 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2. Both
   counts must be 0.
G11 THE PUSH. After C3, `git push` and report its real output, then re-read
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   report it verbatim, stating that #207 is still OPEN and was not merged. Do NOT
   merge and do NOT wait on the CI run; the reviewer watches it. C3's own
   insertion count and the push cannot appear inside C3, so they belong in the
   round report, not in `.agent/handoff.md`.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, at most 60
             lines or a DECISION D15 stated-cause line naming the real count and
             the mandated content that caused it. It carries the item-status
             table for the C0a..C3 bundle, the `## Commits` table G9 pins, and
             one LINE per gate rather than its transcript (R-0582). The full
             transcripts go in the round report you return, never in the file.
──────────────────────────────────────────────────────────────
