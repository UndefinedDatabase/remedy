STEP INTEGRATION GATE / ROUND 11 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 11

Goal
  Book round 10's PASS verdict into the ledger (RECORD10), record one
  reviewer gate-text lesson from round 10 in .agent/prose_slips.md, and
  run the INTEGRATION GATE (docs/agents/integration_gate.md steps 1-5)
  before F114's closure: a branch run, a base run at the merge-base with
  UI parity restored in a disposable worktree on a throwaway branch,
  every branch-only failure attributed, every base-only failure
  attributed, evidence saved under .agent/gate_f114_r11/. The worker
  measures; only the reviewer issues the gate verdict at the next round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r11.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD10 to .agent/live_review.md (append), PROSESLIP10 to
      .agent/prose_slips.md (append), and PLAN11 to .agent/plan.md
      (whole-file replacement)
  C2  run the integration gate (docs/agents/integration_gate.md steps
      1-5) per constraints 5-11 below; save all nine evidence files
      under .agent/gate_f114_r11/
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r11.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/prose_slips.md (C1) -
  .agent/plan.md (C1) - .agent/gate_f114_r11/*.txt (nine new files, C2)
  - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD10, PROSESLIP10, PLAN11) is applied
     BYTE FOR BYTE: extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r11.md - marker lines EXCLUDED - and write it
     with a script, never by retyping. If a slice looks wrong, apply it
     as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD10 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PROSESLIP10 appends to
     .agent/prose_slips.md the SAME way: one newline byte, then the
     slice, with NO trailing newline of its own - this deliberately
     changes that file's own end-of-file from "ends with a trailing
     newline" (its state before this round) to "does not", which is
     intentional and stated here explicitly, not an accident to
     correct. PLAN11 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD10, PROSESLIP10 and PLAN11 all carry NO
     trailing newline of their own.
  5. C2 executes docs/agents/integration_gate.md steps 1-5 EXACTLY, with
     these round-specific parameters:
       - base commit: confirm with `git merge-base main HEAD` (expected
         a1b5d4bb455550f082da7d6c4c80fd968d6e1a88 - the commit where PR
         234 merged into main, matching .agent/plan.md's own stated cut
         point) - if the measured merge-base differs from this expected
         value, STOP and declare the discrepancy rather than proceeding
         on an assumption.
       - base worktree: create ON A THROWAWAY BRANCH, never detached
         (the self-dogfood branch guard refuses a detached HEAD by
         design - DECISION D3, F053 R2):
           git worktree add -b tmp/f114-r11-base .remedy-wt/f114-r11-base <base-sha>
       - evidence directory: .agent/gate_f114_r11/, with exactly these
         nine files, `.txt` extension only (never `.log` - .gitignore
         drops *.log silently and the review-zip guard rejects any
         \.log$ member): gate_summary.txt, branch_run_tail.txt,
         base_run_tail.txt, branch_failed.txt, base_failed.txt,
         branch_only.txt, fixed_by_branch.txt, attribution.txt,
         parity_mtime.txt. Match the SHAPE of the most recent precedent,
         .agent/gate_f112_r19/gate_summary.txt, for gate_summary.txt's
         own structure (STEP 1 through STEP 5, TEST-COUNT DELTA,
         CLEANUP, GATE OUTCOME sections).
  6. UI PARITY (integration_gate.md step 3, before the base run): copy
     the PRIMARY checkout's apps/ui/node_modules and apps/ui/dist into
     the base worktree with shutil.copytree(..., symlinks=True) (never
     a plain copy, never a whole-directory symlink - copytree's own
     default symlinks=False would dereference the npm bin shims,
     R-0591); set REMEDY_UI_NO_AUTO_BUILD=1 for the base run IN-PROCESS
     (shell env assignment is denied in this sandbox - invoke pytest as
     a library call with the env var set in that same process, or via
     python's os.environ before the call); re-stamp every file under the
     base worktree's apps/ui/dist to the current time after the copy
     (git worktree add stamps newer than copytree preserves source
     mtimes, R-0736) and re-measure that the frontend is-stale check
     reads False afterward inside the base worktree; record every dist
     file's mtime immediately before and immediately after the base run
     in parity_mtime.txt - PARITY VOIDS if any mtime falls inside the
     run window, and an accompanying content-hash reading may sit beside
     that but never replace it (R-0444).
  7. Run logs are captured OUTSIDE the repo worktree while each suite
     runs (a scratch path such as /tmp or a path outside the repo tree)
     and copied into .agent/gate_f114_r11/ only after each run exits
     (R-0176 - an in-repo-growing log changes the worktree digest
     mid-run and can produce false failures in identity-checking tests).
  8. `comm` may be unavailable through this sandbox's guard for piped
     forms (R-0590 precedent) - if so, compute branch_only.txt and
     fixed_by_branch.txt as a Python set difference instead and state
     which method was used in gate_summary.txt.
  9. ATTRIBUTION (integration_gate.md step 4), for EVERY id in
     branch_only.txt: a serial re-run of the exact node id with xdist
     disabled (plain `pytest <node-id>`, no `-n auto`).
       - serial-pass => XDIST-FLAKE class (F135/F052): record it in
         attribution.txt, not a blocker.
       - serial-fail => reproduce at the base worktree before blaming
         the feature.
       - a reproducible branch-only failure coupled to F114's own
         changed files is a BLOCKER. Check coupling against
         `git diff --name-only <base-sha>..HEAD -- packages/ apps/` (the
         real changed-file list, not an assumption). On a genuine
         BLOCKER: STOP this round right there - do not attempt a repair,
         do NOT clean up the worktree yet if evidence still needs it,
         write the handback naming exactly which id(s), the full
         evidence, and that a separate reviewer-gated repair round is
         needed before closure can proceed. That STOP handback replaces
         the normal C3 handback shape - still write it, still push, but
         say plainly that this is a STOP, not a normal round-complete
         handback.
  10. ATTRIBUTION, for every id in fixed_by_branch.txt (base-only
      failures): attribute EVERY one by direct evidence too
      (integration_gate.md step 3's unconditional-attribution
      requirement) - an unattributed base-only id counts as a genuine
      base failure and is named as such in gate_summary.txt, never
      silently assumed away or omitted.
  11. gate_summary.txt's closing section is MEASURED, not a verdict:
      follow the shape of .agent/gate_f112_r19/gate_summary.txt's own
      "GATE OUTCOME (measured, not a verdict)" section - name the counts
      and the classification, and end it stating that the verdict
      belongs to the reviewer. Do not write the word "PASS" as your own
      conclusion anywhere in this round's files.
  12. CLEANUP (only if no BLOCKER per constraint 9 halted the round
      first): remove the base worktree by its exact path
      (`git worktree remove --force .remedy-wt/f114-r11-base`),
      `git worktree prune`, delete the tmp branch
      (`git branch -D tmp/f114-r11-base`) - confirm all three with
      `git worktree list` and `git branch --list 'tmp/*'` showing
      neither the worktree nor the branch, before C3.
  13. This round does NOT modify anything under packages/, apps/, or
      tests/ - the integration gate reads and measures, it does not
      repair. A genuine BLOCKER is handled per constraint 9 (stop, do
      not repair in this round).
  14. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  15. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - closure (if
      the gate comes back clean) is its own later round per
      docs/roadmap/STATUS_closure_protocol.md.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r11.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD10). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2382446, no trailing newline). RECORD10 has ZERO
     internal newlines - report its own byte length (expect 3363).
     Report base + 1 + 3363 and whether it equals the post-C1 file's
     byte length (expect 2385810). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD10. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD10's own text,
     confirm the second reader REJECTS it.
  G3 THE PROSE SLIP APPEND (PROSESLIP10). Base size of
     .agent/prose_slips.md immediately BEFORE C1: report byte length and
     trailing-newline status (expect 69169, ends WITH a trailing
     newline). PROSESLIP10 has ZERO internal newlines - report its own
     byte length (expect 720). Report base + 1 + 720 and whether it
     equals the post-C1 file's byte length (expect 69890), and confirm
     the post-C1 file now ends WITHOUT a trailing newline (per
     constraint 3, a deliberate change). Second reader: post-C1 file's
     bytes from `base` to end equal exactly "\n" + PROSESLIP10.
  G4 THE PLAN. Extract PLAN11 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 43 (PLAN11 has 44 logical lines but no trailing newline, so wc -l - which counts \n bytes - reads one less; same class as round 10's own recorded lesson), must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G5 THE GATE EVIDENCE. `ls .agent/gate_f114_r11/` names exactly the
     nine files constraint 5 lists, nothing else. Report each file's
     byte length. Print gate_summary.txt in full inside the handback.
  G6 THE CLEANUP AND THE TREE (skip if constraint 9's BLOCKER path was
     taken - say so explicitly instead).
       git worktree list                 -> no f114-r11-base entry
       git branch --list 'tmp/*'         -> empty
       git status --porcelain            -> empty, checked immediately before C3 staged
       git ls-files .remedy-wt           -> empty
  G7 THE COMMITS AND THE SWEEP. Per-commit numstat cross-check
     (`git show --numstat`) for C0a, C0b, C1 (three paths:
     .agent/live_review.md, .agent/prose_slips.md, .agent/plan.md) and
     C2 (the nine new files under .agent/gate_f114_r11/) against this
     handback's own Commits table - report every cell and confirm it
     matches. C3's own numbers go to neither the table nor a round
     report, per the template's self-reference exception. Staleness
     sweep: one entry per file this round touched (NOT stale / stale +
     why), plus a statement that no NEW stale sentence was found outside
     the change set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are three: RECORD10, PROSESLIP10 and PLAN11.

<<<BEGIN RECORD10>>>
Gate: F114 R10 — the round 10 entry, adds docs/guides/cost-preview-user-guide-v0.md (T003 continued: the docs item) and registers it in docs/README.md's Quick-Find Table and Guides section; no production code or test changes. VERDICT PASS, over the range `91e4ad641da9668f43959043075fc7c2056f2e9b..a2a24339f2c322521e798857eb825b6b4a9d1652` (commits C0a `ab68a38535cbde084eebd9c8cd27dde205704bde`, C0b `fc141a634878e5dc086c8d39023abab7f6b5ec3c`, C1 `bb3bc3f8ff782437fed9635d9c87c999ed41994b`, C2 `a2a24339f2c322521e798857eb825b6b4a9d1652` — four real content commits — plus handback commit `9e04b4379ce5342656831a51cd99492d0f211d9f`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r10.md .agent/last_block.md` both print `fc00c33f38b4c17083c476110e1a520fb21b90bf3f7cc32ca4e8e69f08636dee`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2379181 bytes (no trailing newline), RECORD9 3264 bytes, base + 1 + 3264 = 2382446, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD9 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN10 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (39 lines by `wc -l`, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. The block's own gate text had predicted 40 for `wc -l` where the real, correct reading is 39 (PLAN10 carries no trailing newline, so `wc -l` counts one fewer than its logical line count) — a reviewer gate-text slip with nothing wrong on disk, recorded in `.agent/prose_slips.md` rather than spending an R-id (amend0827-process-diet rule 2). G4 THE NEW FILE HELD: `docs/guides/cost-preview-user-guide-v0.md` `cmp`s exit 0 against the extracted GUIDE slice (3666 bytes, its own trailing newline kept), reproduced independently. G5 THE README PAIRS HELD: both QUICKFIND and GUIDESROW FROM strings occurred exactly once in `docs/README.md` before C2, both applied via `str.replace(FROM, TO, 1)`, both TO-contains-FROM checks true, and `git show --numstat` on C2 read `2	0	docs/README.md` and `88	0	docs/guides/cost-preview-user-guide-v0.md` — reproduced independently. G6 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all six counts unchanged from round 9 exactly as expected for a docs-only round: `tests/docs/` 295, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42. G7 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no scratch worktree was created or needed this round (no production code changed), all four pre-handback commits' numstat cells matched the handback's own Commits table cell for cell, reproduced independently. ONE DEVIATION WAS DECLARED by the worker (the wc -l prediction above, correctly reported as measured rather than assumed) and the reviewer found no others. No finding is registered; nothing is wrong on disk. `docs/guides/cost-preview-user-guide-v0.md` is now the first user-facing documentation of F114's cost-preview behavior. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD10>>>

<<<BEGIN PROSESLIP10>>>
2026-09-04 · F114 R10 (reviewer) · The round 10 block's G3 gate text predicted `wc -l .agent/plan.md` would read 40, matching PLAN10's own logical line count, but the file carries no trailing newline (constraint 4), so `wc -l` — which counts `\n` bytes — correctly read 39; the worker reported the real measured value rather than the block's predicted one, exactly as constraint 1 requires. THE LESSON: a `wc -l` gate over a no-trailing-newline slice is stated as "one less than the slice's own line count", not as the line count itself, so the block's own prediction matches what the tool will actually print. Reviewer-authored gate-text slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSESLIP10>>>

<<<BEGIN PLAN11>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 11 runs the INTEGRATION GATE (docs/agents/integration_gate.md,
steps 1-5) before closure: branch run vs. a base run at the merge-base
`a1b5d4bb455550f082da7d6c4c80fd968d6e1a88` (PR 234's merge into main),
UI parity restored in a disposable worktree on a throwaway branch,
every branch-only failure attributed, evidence saved under
`.agent/gate_f114_r11/`. The worker measures; only the reviewer issues
the gate verdict at the next round.

## Next Steps

- If the gate is clean (no unattributed branch-only failure): author
  the closure sequence per STATUS_closure_protocol.md - evidence job,
  fresh review zip, the STATUS line, the PR. T003's core scope (mark,
  golden tests, docs) is complete; marking further commands
  `is_expensive` and real cost bands for `job.run` are named as
  explicit future work in the guide and the feature file, not blockers.
- If a branch-only failure is a genuine BLOCKER coupled to F114 code:
  that repair is its own reviewer-gated round before closure proceeds.
- Session note: round 11, session 3 - 2nd delegated round this session,
  at the 4-5 default.

## Risks

- The integration gate is the round most likely to surface xdist-flake
  noise (F135/F052 class) unrelated to F114; every branch-only id gets
  a serial re-run and a stated attribution, never an assumed one.
- UI parity (apps/ui/node_modules, apps/ui/dist) must be restored
  correctly in the base worktree or false base-only failures mask real
  ones (R-0736 mtime lesson) - the block states the exact copytree and
  re-stamp procedure rather than leaving it to be improvised.
<<<END PLAN11>>>