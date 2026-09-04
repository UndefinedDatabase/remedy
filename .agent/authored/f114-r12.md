STEP CLOSURE PRECONDITION 6 (GENERATION) / ROUND 12 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 12

Goal
  Book round 11's PASS verdict into the ledger (RECORD11 - the
  integration gate came back clean, F114's first "full suite green"
  claim) and one reviewer prose slip (PROSESLIP11), then perform ONLY
  the GENERATION half of closure precondition 6: the self-use queue
  currently holds no pending item (all seven existing entries are
  already consumed by earlier features), so
  packages.orchestration.self_use_generator.generate_and_append_if_empty()
  is called once, expected to append one new PENDING item. Running
  that item to the approval gate is round 13, not this one.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r12.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD11 to .agent/live_review.md (append), PROSESLIP11 to
      .agent/prose_slips.md (append), and PLAN12 to .agent/plan.md
      (whole-file replacement)
  C2  call generate_and_append_if_empty() per constraint 5 below
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r12.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/prose_slips.md (C1) -
  .agent/plan.md (C1) - scripts/self_use_queue.json (C2) -
  .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD11, PROSESLIP11, PLAN12) is applied
     BYTE FOR BYTE: extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r12.md - marker lines EXCLUDED - and write it
     with a script, never by retyping. If a slice looks wrong, apply it
     as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD11 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PROSESLIP11 appends to
     .agent/prose_slips.md the SAME way: one newline byte, then the
     slice, with NO trailing newline of its own. PLAN12 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD11, PROSESLIP11 and PLAN12 all carry NO
     trailing newline of their own.
  5. C2 IS A PURE PYTHON CALL - NO WORKTREE NEEDED:
       from packages.orchestration.self_use_queue import next_self_use_item, load_self_use_queue
       from packages.orchestration.self_use_generator import generate_and_append_if_empty
     BEFORE calling the generator, verify the precondition the block's
     own Goal states: next_self_use_item() must return None, and
     len(load_self_use_queue().items) must be 7. If EITHER check
     disagrees (a pending item already exists, or the count differs),
     STOP before calling generate_and_append_if_empty(), do NOT call
     it, and declare the discrepancy in the handback instead of
     proceeding on a stale assumption - someone else may have already
     advanced this step. Otherwise, call
     generate_and_append_if_empty() exactly once (no arguments - use
     the real, shipped queue and ledger paths) and report its full
     returned SelfUseQueueEntry (or None, if it answers that).
  6. The returned entry is EXPECTED to have id "SU-008", consumed_by
     "", and a provenance string naming "generated (self-use-generator
     tier 1, ledger scan, R-0418)" (matching SU-005/006/007's own
     provenance shape exactly) - report the REAL returned values
     verbatim; do not assume they match before checking, and declare
     any difference rather than silently reconciling it.
  7. This round does NOT run the generated item (no self_use_job or
     self_use_runner call of any kind) and does NOT set any
     consumed_by value anywhere - both are later rounds' work.
  8. scripts/self_use_queue.json's diff at C2 is EXPECTED to be a
     FULL-FILE rewrite (every line's byte position may shift, because
     json.dumps(..., ensure_ascii=True) re-escapes existing non-ASCII
     content such as em dashes) rather than a clean single-item
     append. This is the ALREADY-OPEN R-0785 finding's own known
     class - do NOT register a new finding for it, and say so plainly
     in the handback if the diff does show a full-file rewrite.
  9. This round does not touch packages/, apps/, or tests/ - only
     scripts/self_use_queue.json (a data file) and .agent/** change.
  10. Read .agent/STOP from disk before the first commit and again
      before C3. If it exists, finish the commit in hand, write the
      handback, and stop.
  11. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r12.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD11). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2385806, no trailing newline). RECORD11 has ZERO
     internal newlines - report its own byte length (expect 4403).
     Report base + 1 + 4403 and whether it equals the post-C1 file's
     byte length (expect 2390210). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD11. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD11's own text,
     confirm the second reader REJECTS it.
  G3 THE PROSE SLIP APPEND (PROSESLIP11). Base size of
     .agent/prose_slips.md immediately BEFORE C1: report byte length
     and trailing-newline status (expect 69890, no trailing newline).
     PROSESLIP11 has ZERO internal newlines - report its own byte
     length (expect 1144). Report base + 1 + 1144 and whether it
     equals the post-C1 file's byte length (expect 71035). Second
     reader: post-C1 file's bytes from `base` to end equal exactly
     "\n" + PROSESLIP11.
  G4 THE PLAN. Extract PLAN12 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 42 (PLAN12 has 43 logical lines but no trailing newline, so wc -l reads one less), must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G5 THE SELF-USE GENERATION. Report the precondition check from
     constraint 5 (next_self_use_item() result, item count) BEFORE the
     call; report the exact returned SelfUseQueueEntry (all fields) from
     generate_and_append_if_empty(); report load_self_use_queue().items
     count AFTER the call (expect 8); report whether the new entry
     matches constraint 6's expectation, field by field; report
     `git show --numstat <C2 sha> -- scripts/self_use_queue.json` and
     whether the diff is a full-file rewrite (most/all lines touched)
     or a clean append (only new lines added) - either is acceptable,
     just report which, per constraint 8.
  G6 THE TREE AND THE SWEEP.
       git status --porcelain            -> empty, checked immediately before C3 staged
       git diff --stat <base>..HEAD -- packages/ apps/ tests/  -> empty (report the exact base SHA used, this round's own starting HEAD)
     Per-commit numstat cross-check (`git show --numstat`) for C0a,
     C0b, C1 (three paths) and C2 (one path) against this handback's
     own Commits table - report every cell and confirm it matches.
     Staleness sweep: one entry per file this round touched (NOT stale
     / stale + why), plus a statement that no NEW stale sentence was
     found outside the change set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are three: RECORD11, PROSESLIP11 and PLAN12.

<<<BEGIN RECORD11>>>
Gate: F114 R11 — the round 11 entry, the INTEGRATION GATE (docs/agents/integration_gate.md steps 1-5) before closure, no production code touched. VERDICT PASS — GATE CLEAN, over the range `9e04b4379ce5342656831a51cd99492d0f211d9f..a4af43f9a6ed22d641cff132512fe844ae5d5fbc` (commits C0a `f553d3276ed3a05ee06ef43f5673c2294b278d7b`, C0b `dc65ab66aca42d1f42da892a2f30c106fedc0181`, C1 `6d20460dbd47c7e5e9e63ab81e17c68dbe3783c9`, C2 `a4af43f9a6ed22d641cff132512fe844ae5d5fbc` — four real content commits — plus handback commit `31aa76b79a8dd9eda17039c903cbff3fef1e06bc`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r11.md .agent/last_block.md` both print `b90f3cd34771cdb62c0da869d25fea9d211cde10dd403ae54a614eedbfeb9ba7`, reproduced directly. G2 THE LEDGER APPEND (RECORD10) HELD ON DISK, WITH ONE DECLARED CORRECTION TO THE REVIEWER'S OWN PRIOR ARITHMETIC: the round 11 block's own G2 text had pinned RECORD10 at 3363 bytes and the post-append total at 2385810, but the slice extracted from the committed authored file measures 3359 bytes and the real post-append file measures 2385806 — the reviewer's own pre-emission byte count was wrong by 4, not a transport or content defect; the worker correctly applied RECORD10 byte-for-byte as extracted rather than trusting the reviewer's stale numeral (the same class as F112 R21's own declared correction). Reproduced independently: base 2382446 bytes (no trailing newline), RECORD10 measured 3359 bytes with zero internal newlines, base + 1 + 3359 = 2385806 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD10 byte for byte, and RECORD10's own text (start and end) reads exactly as authored. G3 THE PROSE SLIP APPEND (PROSESLIP10) HELD BYTE-EXACT: base 69169 bytes (ends WITH a trailing newline), PROSESLIP10 measured 720 bytes with zero internal newlines, base + 1 + 720 = 69890 exactly matching the post-C1 file, which now ends WITHOUT a trailing newline exactly as the block's own constraint 3 stated. G4 THE PLAN HELD BYTE-EXACT: PLAN11 extracted from the committed authored file compares equal to `.agent/plan.md` (43 lines by `wc -l`, matching the block's own corrected prediction this time; `## Goal`/`## Next Steps` each exactly once). G5 THE GATE EVIDENCE HELD: all nine files named by constraint 5 exist under `.agent/gate_f114_r11/` and nothing else does; `gate_summary.txt` follows the `.agent/gate_f112_r19/` shape and ends with the required measured-not-a-verdict framing. THE GATE ITSELF READ CLEAN, REPRODUCED INDEPENDENTLY BY THE REVIEWER: the branch run (`python3 -m pytest -n auto -q` at this round's own HEAD) read 19601 passed, 23 skipped, 0 failed in the reviewer's own re-run, identical to the worker's own reading; the base run (merge-base `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88`, confirmed by `git merge-base main HEAD` matching the block's pinned expectation exactly, UI parity restored in a disposable worktree on throwaway branch `tmp/f114-r11-base`) read 19554 passed, 23 skipped, 0 failed; both `branch_only.txt` and `fixed_by_branch.txt` are empty, so no attribution target exists on either side and no BLOCKER is possible — the reviewer read the full raw evidence (`gate_summary.txt`, `attribution.txt`, `parity_mtime.txt`, both run tails) rather than a summary. UI parity held as an EVENT: no `apps/ui/dist` mtime fell inside the base run's own window, the content digest was identical before and after, and `_frontend_is_stale()` read False inside the base worktree immediately before the run. G6 THE CLEANUP AND THE TREE HELD: `git worktree list` and `git branch --list 'tmp/*'` show neither the base worktree nor its throwaway branch, `git status --porcelain` and `git ls-files .remedy-wt` are both empty, reproduced independently. G7 HELD: every commit's numstat cells match the handback's own Commits table cell for cell, reproduced independently. ONE DEVIATION IS DECLARED (the RECORD10 byte-count correction above, a reviewer-authoring slip with nothing wrong on disk, to be recorded in `.agent/prose_slips.md` at the next round); the reviewer found no others. This is F114's FIRST 'full suite green' claim, per planner_reviewer_prompt.md §4 item 6 — only an integration-gate round may make it. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD11>>>

<<<BEGIN PROSESLIP11>>>
2026-09-04 · F114 R11 (reviewer) · The round 11 block's G2 gate text predicted RECORD10 at 3363 bytes and the post-append `.agent/live_review.md` total at 2385810, but the real measured values are 3359 bytes and 2385806 — a 4-byte arithmetic slip in the reviewer's own re-transcription of RECORD10 between authoring round 10's ledger entry and re-quoting its byte count inside round 11's block, most likely from a differing count of the multi-byte em-dash characters across the two authoring passes. The worker applied the slice byte-for-byte as extracted from the committed authored file, exactly as constraint 1 requires, and correctly reported the real measured values rather than the block's stale prediction (the same class as F112 R21's own declared correction). THE LESSON: a byte count re-quoted for a SECOND gate, in a LATER round's block, is re-measured from the actual committed file at authoring time rather than copied from an earlier round's own prose — a value is only as fresh as the last time it was actually counted. Reviewer-authored gate-text slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSESLIP11>>>

<<<BEGIN PLAN12>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 12 books round 11's PASS verdict (RECORD11 - integration gate
clean, F114's first "full suite green" claim) and one reviewer prose
slip (PROSESLIP11), then does closure precondition 6's GENERATION step
only: the queue has no pending item, so `generate_and_append_if_empty()`
appends SU-008 (the R-0418 paragraph SU-005/006/007 already quoted) as
PENDING. No production code changes. Running SU-008 is round 13, per
the split F112 used at its own rounds 20/21.

## Next Steps

- Round 13: run SU-008 via `self_use_job`/`self_use_runner` to the
  approval gate (real local `ollama`, small budget); register
  `describe_self_use_run_defects`' output - expect it adds evidence to
  the ALREADY-OPEN `R-0784` (§3 item 30), not a new id.
- Author T3_F114.md's Built State section (precondition 4).
- `remedy integrity check --json` (precondition 3).
- Then the closure commit: evidence job, fresh review zip, STATUS
  line, README sync, `consumed_by=F114`, the PR. Likely its own
  session, per F112's closure spanning rounds 20/21/22/29/30/31.
- Session note: round 12, session 3 - 3rd delegated round, at the 4-5
  default.

## Risks

- `append_generated_item` rewrites the WHOLE queue file (`json.dumps`
  ensure_ascii) - the ALREADY-OPEN `R-0785` class; expect a full-file
  diff, not a clean append.
- Round 13's run is a real, budget-capped LLM call against local
  `ollama` - bounded, expected to end BLOCKED (the correct outcome).
<<<END PLAN12>>>