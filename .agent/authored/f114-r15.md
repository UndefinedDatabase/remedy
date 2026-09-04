STEP SESSION CLOSE / ROUND 15 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 15

Goal
  Book round 14's PASS verdict into the ledger (RECORD14 - Built State
  authored, closure precondition 4 satisfied), then end SESSION 3 with
  a proper session-ending handback per self_drive_protocol.md's
  "Ending a session" section. Pure bookkeeping round, permitted only
  inside the closure sequence (amend0827 rule 1's exception). No code
  changes.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r15.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD14 to .agent/live_review.md (append) and PLAN15 to
      .agent/plan.md (whole-file replacement)
  C2  rewrite .agent/handoff.md - the SESSION-ENDING handback (see
      constraint 5 below for its required shape)

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r15.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  .agent/handoff.md (C2)

Constraints
  1. Every authored slice (RECORD14, PLAN15) is applied BYTE FOR BYTE:
     extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r15.md - marker lines EXCLUDED - and write it
     with a script, never by retyping. If a slice looks wrong, apply it
     as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD14 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PLAN15 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD14 and PLAN15 both carry NO trailing
     newline of their own.
  5. C2's handback is a SESSION-ENDING handback, per
     self_drive_protocol.md's "Ending a session" section. It states, at
     minimum: feature F114 and round 15; SESSION NUMBER 3 of the
     running feature, now ENDING; branch name; the full commit SHA
     history of THIS SESSION (rounds 10 through 15, every commit,
     grouped by round); a summary changed-files table for the whole
     session (which real files changed, aggregated); real verification
     results (state that round 11's integration gate was the full-suite
     confirmation, GATE CLEAN - 19601/19554 passed, 0 branch-only, 0
     unattributed base-only failures); the OPEN FINDINGS COUNT,
     computed MECHANICALLY at this exact commit (every
     '^- R-\\d+ — ' paragraph in .agent/live_review.md minus every
     '^Done: R-\\d+ — ' line in it - report the real numbers, not a
     recollection); and the NEXT EXPECTED ACTION stated explicitly:
     "SESSION 4 opens with `remedy integrity check --json`
     (closure precondition 3, not yet run), then the closure commit
     itself (evidence job, fresh review zip, STATUS line, README sync,
     scripts/self_use_queue.json's consumed_by=F114 edit, the PR) per
     docs/roadmap/STATUS_closure_protocol.md's algorithm." State
     plainly that closure preconditions 4 and 6 are SATISFIED, 1 and 2
     hold, 5 holds now, and only 3 plus the closure commit itself
     remain.
  6. This round does not touch packages/, apps/, or tests/ - only
     .agent/** changes.
  7. Read .agent/STOP from disk before the first commit and again
     before C2. If it exists, finish the commit in hand, write the
     handback, and stop.
  8. Self-review loop before every commit (git diff --stat, git diff).
     Push after C2. No pull request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r15.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD14). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2398958, no trailing newline). RECORD14 has ZERO
     internal newlines - report its own byte length (expect 3923).
     Report base + 1 + 3923 and whether it equals the post-C1 file's
     byte length (expect 2402882). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD14. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD14's own text,
     confirm the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN15 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 37 (PLAN15 has 38 logical lines but no trailing newline), must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE TREE AND THE SWEEP.
       git status --porcelain            -> empty, checked immediately before C2 staged
       git diff --stat <this round's own starting HEAD>..HEAD -- packages/ apps/ tests/  -> empty
     Per-commit numstat cross-check (`git show --numstat`) for C0a,
     C0b and C1 (two paths) against this handback's own Commits table -
     report every cell and confirm it matches. Report the mechanically
     computed open-findings count (per constraint 5) directly from the
     grep commands stated there.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are two: RECORD14 and PLAN15.

<<<BEGIN RECORD14>>>
Gate: F114 R14 — the round 14 entry, closure precondition 4's Built State section, no code changes. VERDICT PASS, over the range `fdfe587574be7af3625dcb219a99233508d561c9..e8fe6d7d4bc94e001407e37a4555a337cf0575f8` (commits C0a `dfbf425e84116b99ef117b48a91bcc6cce5032f6`, C0b `14f6d8a22a5774abd165ef320a10cc94e2b34735`, C1 `598f2ccdb73d64e62685d70a8bbfbff45bd55ffb`, C2 `e8fe6d7d4bc94e001407e37a4555a337cf0575f8` — four real content commits — plus handback commit `1d0627fa50c63062af56987bd2f369241ad25d80`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r14.md .agent/last_block.md` both print `bb040642421ea504a1e52c7afbe163e5d8ebf0f2834e6598e4f67d72f3679d54`, reproduced directly. G2 THE LEDGER APPEND (RECORD13) HELD BYTE-EXACT: base 2393966 bytes (no trailing newline), RECORD13 measured 4991 bytes with zero internal newlines, base + 1 + 4991 = 2398958 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD13 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PLAN HELD BYTE-EXACT: PLAN14 extracted from the committed authored file compares equal to `.agent/plan.md` (40 lines by `wc -l`; `## Goal`/`## Next Steps` each exactly once). G4 THE BUILT STATE PAIR HELD: the FROM line occurred exactly once in `docs/roadmap/features/T3_F114.md` before C2, the applied TO contains that FROM verbatim, and the post-C2 file measures 6744 bytes ending with a trailing newline — exactly matching the reviewer's own prediction, reproduced independently. THE SECTION'S OWN CLAIMS WERE CHECKED AGAINST DISK, NOT ONLY ITS SHAPE: every symbol it names — `token_economy.tokens_to_cost_usd`, `cost_preview.CostBandEstimate`/`estimate_cost_band`/`resolve_confirm_above_usd`/`ESTIMATE_UNAVAILABLE`, `cost_preview_confirm.render_estimate_line`/`confirm_cost_preview`/`EXIT_USAGE` — resolves in the named file at the named line, and every file it lists (`docs/guides/cost-preview-user-guide-v0.md`, all four named test files) exists on disk, reproduced independently by the reviewer. ONE HARMLESS LABELING SLIP IS DECLARED: the block's own G4 prose named an intermediate '3412-byte BUILTSTATE slice' meaning the appended content alone, while the worker's own extraction measured the FULL TO text (FROM plus separator plus BUILTSTATE) at 3474 bytes — both readings are consistent arithmetic over the SAME bytes read two different ways, and the one number that actually gates the round (the post-C2 file length, 6744) matched exactly either way; nothing on disk is wrong, only the block's own descriptive noun for which span '3412' named. G5 THE DOCS GATES HELD, REPRODUCED INDEPENDENTLY: `tests/docs/` 295, `test_roadmap_index.py` 30. G6 THE SUITES HELD, REPRODUCED INDEPENDENTLY, ALL FIVE COUNTS IDENTICAL TO ROUND 9/10's OWN BASELINE: `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42. G7 HELD: `git status --porcelain` and `git diff --stat fdfe5875..e8fe6d7d -- packages/ apps/ tests/` are both empty, reproduced independently; every commit's numstat cells match the handback's own Commits table cell for cell. THREE DEVIATIONS ARE DECLARED (a denied `cmp` tool substituted with an equivalent Python byte-equality read; the labeling slip above; a read-only spot-check of file existence rather than re-deriving every prose claim, per constraint 1's apply-verbatim rule) — none is a defect on disk. Closure preconditions 4 (Built State, this round) and 6 (self-use, round 13) are both now SATISFIED for F114; precondition 3 (`remedy integrity check --json`) is still owed, and the closure commit itself (evidence job, review zip, STATUS line, README sync, `consumed_by=F114`, the PR) has not started. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD14>>>

<<<BEGIN PLAN15>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 15 books round 14's PASS verdict (RECORD14 - Built State
authored, precondition 4 satisfied) and ends SESSION 3 here, per
amend0827 rule 6's own 4-5-round default (this session ran 5: rounds
10-14). Pure bookkeeping, permitted only inside the closure sequence
(amend0827 rule 1's exception). No code changes.

## Next Steps

- SESSION 4 opens with `remedy integrity check --json` (precondition
  3, not yet run).
- Then the closure commit itself: evidence job, fresh review zip,
  STATUS line, README sync, `scripts/self_use_queue.json`'s
  `consumed_by=F114` edit, the PR (STATUS_closure_protocol.md
  algorithm) - likely its own session or two, per F112's own
  precedent (rounds 20/21/22/29/30/31).
- Preconditions 4 and 6 are SATISFIED; precondition 1 (every step
  PASS) and precondition 2 (integration gate clean, round 11) both
  hold; precondition 5 (clean tree, pushed) holds now.

## Risks

- None new this round. The closure commit is the highest-stakes
  remaining work (STATUS/README edits, a real PR) and deserves a
  fresh session's full context rather than a tired continuation.
<<<END PLAN15>>>