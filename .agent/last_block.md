OUTCOME: pending
── STEP R4b — F252 CLOSURE, corrected ordering (R-0154) ─────────────
Goal:        Finish closure: preconditions, evidence job, fresh
             review zip, then ONE final commit = README sync +
             STATUS [x] + final .agent state, grep proofs, PR.
Bundle:      Slice 0 persist · Slice A preconditions · Slice B
             evidence + zip · Slice C final commit + PR.
Change:      .agent state, README.md + docs/roadmap/STATUS.md (both
             ONLY in the final commit), evidence dir (committed
             AFTER the READY zip). Nothing else.
Constraints: AGENTS.md; STATUS_closure_protocol.md v3 EXACTLY. Zip
             failure = closure BLOCKER (raw error, hand back).
             Authored texts: save verbatim, sha256-verify BEFORE
             commit; mismatch = STOP + refusal record in
             .agent/last_block.md, apply nothing. The saved STATUS
             template .agent/authored/f252-r4-4.md must re-verify to
             79db25a571adeb91cdc4f460654d0630ba2355393bbe8662898c5cd244be5782
             before substitution; substitute ONLY the four
             <PLACEHOLDERS>, provenance line per value in the
             handback. Worker never writes ## Verdicts. The PR is
             NOT merged this session.
Done when:   Protocol steps 1–5 complete, zip import check green,
             combined final commit green on the docs gate, STATUS
             grep proof, PR open.
Handback:    Per template, including: raw `remedy integrity check
             --json`, evidence job id, zip filename + SHA-256 from
             the script output, accepted HEAD, the applied STATUS
             line verbatim + grep -cF proofs (new=1, old=0), PR
             number, and the post-commit `pytest tests/docs/ -q`
             transcript.

PROCEDURE

Slice 0 — persist (one commit)
1. last_block.md guard: line 1 "OUTCOME: pending", THIS block
   verbatim; final state "OUTCOME: executed" at round end.
2. Save f252-r4b-1 and f252-r4b-2 below VERBATIM to
   .agent/authored/, sha256-verify. Apply: r4b-1 FULL REPLACE
   .agent/live_review.md (cmp 0), r4b-2 FULL REPLACE .agent/plan.md
   (cmp 0). Gate: python3 -m pytest tests/docs/ -q → 292 passed +
   canary 42 passed. Commit: "chore(f252): persist the R4 stop
   verdict + R-0154 resolution". Push.

Slice A — preconditions (no commit)
3. remedy integrity check --json → verdict PASS required (record
   raw). git status --porcelain → empty. Branch pushed. Any failure
   → STOP, hand back (protocol Failure honesty).

Slice B — evidence job + zip (protocol steps 1–2)
4. Evidence job: final feature-scoped run, fresh job id, canonical
   producer create_manual_completion_bundle(
   review_feature_id="f252", …), complete verification_runs
   (sha256-hex output_hash, valid totals, full-length base_commit
   7baff1d<full sha>). Do NOT commit the evidence dir yet.
5. Zip: bash scripts/make_review_zip.sh --evidence-dir <step-4
   dir>. Verify committed_review_subject spans 7baff1d..HEAD (HEAD
   = the Slice 0 commit or later) and the import check passes.
   Record filename + SHA-256 from the script output. THEN commit
   the evidence dir: "chore(f252): commit closure evidence (after
   READY zip)". Push.
6. accepted HEAD for the STATUS line = the zip manifest's
   committed_review_subject.head_commit (full SHA). Record it.

Slice C — final commit + PR (protocol steps 4–5, R-0154 ordering)
7. In ONE commit, the last on the branch (Rule A4):
   a. README.md, three edits, nothing else: "24 of 252 registered
      items accepted. In progress: F252 (standing-red paydown)." →
      "25 of 252 registered items accepted. Next: F050 (DAG
      scheduling)." · Tier-1 row Done 8 → 9 · append "F252
      standing-red paydown" to the "Accepted in Tier 1 so far:"
      block.
   b. docs/roadmap/STATUS.md: replace the line "- [~] F252 —
      Standing-red paydown (154 ids, 13 classes)" with the r4-4
      template line after substituting <JOB_ID> (step 4),
      <ZIP_FILENAME> (step 5), <ZIP_SHA256> (step 5), <HEAD_SHA>
      (step 6). Touch no other line.
   c. Final .agent state: last_block.md OUTCOME → executed;
      handoff.md rewrite (the handback).
   Pre-commit gate on the staged state: python3 -m pytest
   tests/docs/ -q → 292 passed (README and STATUS now agree) +
   canary 42 passed. grep -cF applied STATUS line = 1, old line
   = 0. Commit: "chore(f252): close F252 — STATUS [x] + README
   sync". Push.
8. PR per AGENTS.md: title "F252 — Standing-red paydown (154 ids,
   13 classes)"; body: what/why, key decisions (D3/D12 quarantines,
   D4 live-coupled, D10 test-only, R-0154 ordering), how to review
   (four gates + determinism proof + zip), changed-files table,
   latest verdict R4 PASS (stopped-round) / R1–R3 PASS, open
   findings 0, runtime actuals: "5 rounds (R1–R4b), 2026-07-28 →
   2026-07-29, ~26 commits; tokens/cost not-measured". Do NOT
   merge.
9. Handback per template with everything under Handback above.

--- BEGIN f252-r4b-1 sha256=f91bd529d7e5310721b8d154cf11e2e64133e3804ee5d718eb4dc86e2137511f ---
# Live Review — F252 Standing-red paydown (154 ids, 13 classes)

Branch: feature/f252-standing-red-paydown
Scope: every catalogued standing-red id reaches an explicit terminal
state, class by class (catalog: .agent/f251_baseline/class_map.txt).

## Steps
- R1: claim + state reset + product-bug classes D8, D10, D11. Done.
- R2: R-0152 + all remaining classes; 143 fixed, 11 quarantined by
  decision; suite 14295 passed / 0 failed / 19 skipped. Done.
- R3: R-0153 + integration gate (zero branch-only failures) +
  three-run determinism proof (four counting the reviewer's). Done.
- R4: closure, first attempt — STOPPED at the README sync on the
  ordered condition; Slice 0 (verdict + Built State) stands. Done.
- R4b: closure resumed — preconditions, evidence job, zip, then ONE
  final commit carrying README sync + STATUS [x] + final .agent
  state; PR. In progress.

## Findings
- Done: R-0152 (minor): do-planning fallback to the intake-bound
  call_fn removed (R2).
- Done: R-0153 (nit): dead `unaccepted <= named` assertion removed
  from the README honesty pin (R3).
- Resolved: R-0154 (process, planning-routed): the R4 block ordered
  the README "Accepted in Tier 1" append (step 3) before the STATUS
  [x] edit (step 8), contradicting the R2-authored ledger
  cross-check pin — README and STATUS may never disagree in a
  committed state. The worker STOPped exactly as ordered, reverted
  cleanly, handed back with the raw failure. Resolution: R4b folds
  the README sync into the final STATUS commit; the pin stays
  untouched. Registered as a DECISION (option a; alternatives:
  narrow the pin — a test change inside closure, rejected; other
  orderings). Reversible by any later relay.

## Verdicts
- R1: PASS (reviewer, 2026-07-29). Range 7baff1d..cc247fa.
- R2: PASS (reviewer, 2026-07-29). Range cc247fa..fc3e843.
- R3: PASS (reviewer, 2026-07-29). Range fc3e843..2758396. Details
  for R1–R3 in this file's git history.
- R4 (stopped round): PASS on the executed scope (reviewer,
  2026-07-29). Range 2758396..d9a146a, 2 commits. All four authored
  proofs cmp 0 against the reviewer's originals (r4-4 one line, 222
  chars, placeholders intact); Built State append tail-cmp 0;
  README.md and STATUS.md byte-untouched on the branch (0-line
  diff); tree clean. Reviewer re-ran: tests/docs 292 passed, the
  ledger pin passes on the clean tree, canary 42 passed. The STOP
  was correct worker behavior on a reviewer authoring error
  (R-0154); OUTCOME: stopped + STOP RECORD is the prescribed
  disk trace. LAST_REVIEWED_SHA = d9a146a.
--- END f252-r4b-1 ---

--- BEGIN f252-r4b-2 sha256=d2d810d54f5b7fae4407d3d145956778363650691e56c956926e850efece5810 ---
# Plan — F252 Standing-red paydown

## Goal
All 154 catalogued standing-red ids reach an explicit terminal state
(root-cause fix, honest test update, or operator-decided retirement);
DONE when three consecutive full-suite runs produce identical failure
sets, empty except explicit quarantines (F251 rules unchanged).
Status: proven (R3 gate + determinism proof, reviewer-confirmed).

## Next Steps
- R4b: closure with the corrected ordering (R-0154): preconditions
  (integrity check), evidence job (feature_id=f252), fresh review
  zip, THEN one final commit = README sync + authored STATUS [x] +
  final .agent state (Rule A4), grep proofs, PR per AGENTS.md. The
  PR is NOT merged this session; it merges at the next feature's
  start via the Open PR Gate.
- After the R4b PASS: session ends; next feature per Rule A5 (F050)
  in a fresh window.
--- END f252-r4b-2 ---
