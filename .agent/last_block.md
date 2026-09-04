═══════════════════════════════════════════════════════════════
── STEP CLOSURE COMMIT + PR / ROUND 18 — F114 Cost preview per command (FINAL ROUND) ──

FEATURE F114 — Cost preview per command (Tier 3) — SESSION 4, ROUND 18 (closing round)

Goal
  Book round 17's PASS verdict into the ledger (RECORD17 — evidence
  bundle + review zip, algorithm steps 1-2 complete) and record one
  reviewer-authoring slip (SLIPF114R18), then execute the closure
  commit itself (STATUS `[x]` flip + README capability sync +
  self_use_queue `consumed_by` edit, all in ONE commit per
  docs/roadmap/STATUS_closure_protocol.md algorithm step 5) and open
  the pull request. This is F114's FINAL round — do not merge the PR.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r18.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD17 to .agent/live_review.md (append), SLIPF114R18 to
      .agent/prose_slips.md (append), and PLAN18 to .agent/plan.md
      (whole-file replacement)
  C2  THE CLOSURE COMMIT: apply the STATUS pair to
      docs/roadmap/STATUS.md, all three README pairs to README.md, and
      the QUEUE pair to scripts/self_use_queue.json — ALL FIVE PAIRS IN
      THIS ONE COMMIT (a prior feature's closure round split the STATUS
      flip from the README numeral updates across two commits and
      shipped a red `tests/docs/` in between — see constraint 10)
  then push, run the docs gate (must be green — see Done-when G6),
      then `gh pr create` (see "The pull request" section)
  C3  rewrite .agent/handoff.md — the FINAL handback (feature-done
      banner)

Change set — EXACTLY these paths and nothing else
  .agent/authored/f114-r18.md (new, C0a) — .agent/last_block.md (C0b) —
  .agent/live_review.md (C1) — .agent/prose_slips.md (C1) —
  .agent/plan.md (C1) — docs/roadmap/STATUS.md (C2) — README.md (C2) —
  scripts/self_use_queue.json (C2) — .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD17, SLIPF114R18, PLAN18) is applied
     BYTE FOR BYTE: extract by delimiter index from the COMMITTED
     .agent/authored/f114-r18.md — marker lines EXCLUDED.
  2. C1 is the first substantive commit of the round.
  3. RECORD17 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. SLIPF114R18 appends to
     .agent/prose_slips.md as EXACTLY TWO newline bytes (one blank
     line) followed by the slice — this file's own separator
     convention differs from live_review.md's, confirmed by the
     existing file: it holds 113 occurrences of a double-newline
     between its dated entries. PLAN18 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD17, SLIPF114R18 and PLAN18 all carry NO
     trailing newline of their own.
  5. Read .agent/STOP from disk before the first commit, again before
     C2, and again before C3. If it exists at any of these, finish the
     commit in hand, write the handback, and stop — do not create a PR.
  6. Every pair below is APPEND-shaped or REWRITE-shaped as labelled;
     verify the labelled containment reading yourself before applying
     (does TO contain FROM verbatim?) and report what you found beside
     what was labelled.
  7. Apply pairs via `str.replace(FROM, TO, 1)` on each named file.
     Before each apply, confirm FROM occurs EXACTLY ONCE in that file.
  8. THE OPEN SET, per docs/agents/planner_reviewer_prompt.md §3 item
     10's canonical line-count formula: report the registered/Done/open
     counts BEFORE C1 and AFTER C1, confirming both UNCHANGED (354
     registered, 76 Done lines, 278 open) — this round registers no
     finding id and resolves none.
  9. Precondition 6's closure paragraph: this round's RECORD17 (already
     landed) and RECORD16 both name that closure precondition 6 was
     satisfied in rounds 12-13 (SU-008 generated and run to the normal
     approval gate; its findings were evidence added to already-open
     `R-0784`, no new id minted). No new self-use action is needed this
     round beyond the `consumed_by` edit in the QUEUE pair below.
  10. THE CLOSURE COMMIT IS ONE COMMIT, NOT TWO. A prior feature's
      closure round (F112 R30) flipped STATUS.md to `[x]` in one commit
      without updating README's two DERIVED numerals (the "N of 266"
      count and the Tier 3 table's Done cell) in the same commit, and
      `tests/docs/` went red until a follow-up repair commit. All five
      pairs below (STATUS, the two README numeral pairs, the README
      paragraph pair, and the QUEUE pair) land together in C2.
  11. This round does not touch packages/, apps/, or tests/.

The authored slices

<<<BEGIN RECORD17>>>
Gate: F114 R17 — the round 17 entry, algorithm steps 1-2 of `docs/roadmap/STATUS_closure_protocol.md`: the evidence bundle and the review zip. VERDICT PASS, over the range `eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0..af075516d058e24a9ee19e54c4014a444341fc97` (commits C0a `4a14e6d91acae13cd764edcaa6dd0f31112176f6`, C0b `fef49778925ebb537629535462c77f4dfb00cf8b`, C1 `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6` — three real content commits — plus handback commit `af075516d058e24a9ee19e54c4014a444341fc97`), independently re-verified by the reviewer. TRANSPORT HELD: `sha256sum .agent/authored/f114-r17.md .agent/last_block.md` both print `58b921c822ad80e9c134267525791d7c9b2f2ed3b2c8ff79f27e5d423b44c2a1`, reproduced directly. G4 THE LEDGER APPEND (RECORD16) HELD BYTE-EXACT: base 2405496 bytes (no trailing newline), RECORD16 measured 3273 bytes with zero internal newlines, base + 1 + 3273 = 2408770 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD16 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PLAN HELD BYTE-EXACT: PLAN17 extracted from the committed authored file compares equal to `.agent/plan.md` (35 lines by `wc -l`; `## Goal`/`## Next Steps` each exactly once). THE EVIDENCE BUNDLE HELD, REPRODUCED INDEPENDENTLY: evidence job `f114-closure` produced all five verification runs green at exactly the ordered counts — `tests/orchestration/test_cost_preview.py` 19, `tests/cli/test_cost_preview_confirm.py` 12, `tests/cli/test_cost_preview.py` 5, `tests/test_command_catalog.py::TestCatalogExpensive` 4, `tests/docs/test_docs_consistency.py` 295 — zero failed/skipped/deselected everywhere, `len(node_ids) == selected` for every run, every `output_hash` matching sha256 of its own `stdout_summary`, all eight closed-schema gate files present, and the template's own computed HEAD equal to C1's full sha. THE REVIEW ZIP HELD, REPRODUCED INDEPENDENTLY BY THE REVIEWER OVER THE FILE ON DISK: `remedy-review-20260904-185732-READY_FOR_REVIEW.zip` at `/home/decodeux/Repos/remedy-history/zips/`, size 22113384 bytes, sha256 `8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810` — matching the worker's own reported digest exactly; its `.review_zip_manifest.json` reads `package_status` READY_FOR_REVIEW with `ready_gate_matrix.ok` true and EMPTY `blocking_reasons`, `committed_review_subject.head_commit` equal to C1's full sha, and `committed_review_subject.base_commit` equal to `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88`. THE RED CONTROL WAS OPENED, NOT TAKEN ON REPORT: the deliberately mutated copy packaged `remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip`, independently re-opened by the reviewer, reading `package_status` BLOCKED_EVIDENCE with exactly the three blocking reasons the handback quotes — the node-id count mismatch, the local-absolute-path node id, and the unconfirmable VerificationTests total — proving the pipeline distinguishes a poisoned bundle from the real one. PRECONDITION 3 HELD, RE-CONFIRMED A SECOND TIME: `python3 -m apps.cli.grouped integrity check --json` unchanged from round 16's own reading. THE STRUCTURE HELD: `git status --porcelain` empty, the three commits before the handback single-parent, all insertions under 500, `.remedy-wt` and `remedy-job-evidence` both absent from the tracked tree, and `docs/roadmap/STATUS.md`/`README.md`/`scripts/self_use_queue.json` all absent from the range, exactly as this round's own scope required. ONE DISCREPANCY IS DECLARED AND RESOLVED, NOT A DEFECT ON DISK: this round's own constraint 7 asked for the open-findings count under the DISTINCT-id formula `len(set(registered) - set(resolved))` while quoting the expected value `278`, which is round 16's own LINE-COUNT-formula figure; the two formulas disagree because two ids, `R-0721` and `R-0725`, each carry TWO `Done:` lines from a "resolved in part" / "fully resolved" pair, so the line-count subtraction (354 − 76 = 278) and the distinct-id subtraction (354 − 74 = 280) differ by exactly 2. `docs/agents/planner_reviewer_prompt.md` §3 item 10 defines the open-finding set by the LINE-COUNT formula in as many words ("every registered paragraph minus every `Done:` line"), so 278 remains THE canonical open-findings count this project's checklist recognizes; the worker reported both readings rather than silently reconciling them, exactly as constraint 1 requires, and the mismatch is the REVIEWER's own authoring error in restating a distinct-id formula it did not re-derive against — recorded as a dated line in `.agent/prose_slips.md` this round (SLIPF114R18), no R-id spent, per amend0827-process-diet rule 2. Open findings, canonical count: 354 registered minus 76 `Done:` lines equals 278 open, unchanged this round; `.agent/candidates.md` remains EMPTY. ALL SIX CLOSURE PRECONDITIONS FOR F114 CONTINUE TO HOLD, and algorithm steps 1 and 2 of `docs/roadmap/STATUS_closure_protocol.md` are now complete: `Evidence job f114-closure`, package `remedy-review-20260904-185732-READY_FOR_REVIEW.zip`, SHA-256 `8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810`, archived at `/home/decodeux/Repos/remedy-history/zips`, accepted HEAD `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`. The next and final round is the closure commit itself (STATUS line, README sync, the `consumed_by` edit) and the pull request.
<<<END RECORD17>>>

<<<BEGIN SLIPF114R18>>>
2026-09-04 · F114 R18 (reviewer) · Round 17's own constraint 7 asked for the open-findings count under the distinct-id formula `len(set(registered) - set(resolved))` while quoting the expected value `278`, which is the LINE-COUNT formula's figure (`docs/agents/planner_reviewer_prompt.md` §3 item 10's canonical definition: "every registered paragraph minus every `Done:` line"); the two formulas disagree by exactly 2 because `R-0721` and `R-0725` each carry two `Done:` lines from a resolved-in-part/fully-resolved pair, giving 354−76=278 under the line formula and 354−74=280 under the distinct-id formula. THE LESSON: when a gate borrows a DIFFERENT round's formula wording (here, an F257 closure round's ledger-movement check), its own quoted expected NUMBER is re-derived under THAT exact formula rather than copied from the canonical count computed a different way — item 10's line-count formula remains the project's official open-findings count. Reviewer-authored gate-text slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPF114R18>>>

<<<BEGIN PLAN18>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 18 books round 17's PASS verdict (RECORD17 — the evidence bundle
and review zip, algorithm steps 1-2) and records one reviewer-authoring
slip (SLIPF114R18), then runs the closure commit itself: the `[x]` flip
on docs/roadmap/STATUS.md, the README capability sync, and
`scripts/self_use_queue.json`'s `consumed_by=F114` edit on SU-008 — one
commit, per docs/roadmap/STATUS_closure_protocol.md algorithm step 5.
The pull request follows in this same round.

## Next Steps

None — F114 closes with this round's pull request. The next session
claims the next feature per Rule A5.

## Risks

- The README's derived numerals (the accepted count and the Tier 3
  Done cell) move mechanically the moment STATUS.md flips to `[x]`;
  both are re-derived and edited in the SAME commit as the flip, per
  F112 R30's own lesson (a closure commit that skipped this went red
  on `tests/docs/` and needed a repair commit).
<<<END PLAN18>>>

The closure pairs

PAIR 1 — STATUS (REWRITE: TO does not contain FROM), file
docs/roadmap/STATUS.md:

<<<BEGIN STATUS_FROM>>>
- [~] F114 — Cost preview per command
<<<END STATUS_FROM>>>

<<<BEGIN STATUS_TO>>>
- [x] F114 — Cost preview per command (T001–T003 complete; accepted 2026-09-04 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f114-closure · package remedy-review-20260904-185732-READY_FOR_REVIEW.zip · SHA-256 8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6)
<<<END STATUS_TO>>>

PAIR 2 — README accepted-count (REWRITE), file README.md:

<<<BEGIN README_COUNT_FROM>>>
70 of 266 registered items accepted.
<<<END README_COUNT_FROM>>>

<<<BEGIN README_COUNT_TO>>>
71 of 266 registered items accepted.
<<<END README_COUNT_TO>>>

PAIR 3 — README Tier 3 table row (REWRITE), file README.md:

<<<BEGIN README_TIER3_FROM>>>
| 3 | Full Token Economy & Autonomy | 5 | 26 |
<<<END README_TIER3_FROM>>>

<<<BEGIN README_TIER3_TO>>>
| 3 | Full Token Economy & Autonomy | 6 | 26 |
<<<END README_TIER3_TO>>>

PAIR 4 — README F114 capability paragraph (APPEND: TO contains FROM
verbatim), file README.md. This FROM string is the boundary between
F112's paragraph and the Tier 5 heading; the paragraph is inserted
between them, so this is an APPEND even though the TO is much longer
than the FROM:

<<<BEGIN README_PARA_FROM>>>
ones).

Accepted in Tier 5 so far:
<<<END README_PARA_FROM>>>

<<<BEGIN README_PARA_TO>>>
ones).

F114 cost preview per command (`remedy job run` — the one command wired to
it so far — prints an upfront cost-band estimate with its basis before an
expensive run starts and requires confirmation above a configured
threshold in attended mode; `--yes` and `--unattended` both skip the
prompt with an audited line, and a non-tty pipe with neither flag exits
with the estimate and the `--yes` hint rather than hanging. Real cost
bands for `job.run` are not calibrated yet, so its own estimate reads
`ESTIMATE_UNAVAILABLE` today — still confirmed, never silently skipped).

Accepted in Tier 5 so far:
<<<END README_PARA_TO>>>

PAIR 5 — self_use_queue.json consumed_by (REWRITE), file
scripts/self_use_queue.json. This exact string occurs exactly once in
the file (SU-008's own line; every other item already carries a
non-empty consumed_by):

<<<BEGIN QUEUE_FROM>>>
"consumed_by": "",
<<<END QUEUE_FROM>>>

<<<BEGIN QUEUE_TO>>>
"consumed_by": "F114",
<<<END QUEUE_TO>>>

The pull request

After C2 is pushed and the docs gate (G6 below) is green, run:

  gh pr create --title "F114: Cost preview per command" --base main --head feature/f114-cost-preview-per-command --body "$(cat <<'PRBODY'
## Summary
- Commands that will spend real money now show an upfront cost-band
  estimate with its basis and require confirmation above a configured
  threshold in attended mode; unattended runs rely on `--yes`/
  `--unattended`, not prompts. `remedy job run` is the first (and so
  far only) command wired to it.
- Shared estimator: `packages/orchestration/token_economy.tokens_to_cost_usd`
  (extracted, no behavior change) + `packages/orchestration/cost_preview.py`
  (`CostBandEstimate`, `estimate_cost_band`, `ESTIMATE_UNAVAILABLE`,
  `resolve_confirm_above_usd`). Shared CLI helper:
  `apps/cli/cost_preview_confirm.py`. Wired at
  `apps/cli/commands/job.py` / `apps/cli/command_catalog.py`
  (`is_expensive=True` on `job.run`).
- An unrecognised class, an unpriced config, or a negative
  `repeat_count` always answers `ESTIMATE_UNAVAILABLE` (never a
  fabricated number), and an unavailable estimate is treated as
  expensive rather than skipped.

## Key decisions
- `--yes`/`--unattended` print an audited line and proceed; a non-tty
  stdin with neither exits 2 with the estimate and the `--yes` hint,
  rather than hanging on `input()`.
- Real cost bands for `job.run` are not calibrated yet (deliberately
  out of scope, per `docs/roadmap/features/T3_F114.md` Do-not-touch on
  calibration/F074); its estimate is honestly `ESTIMATE_UNAVAILABLE`
  today, still confirmed.

## How to review
- `docs/roadmap/features/T3_F114.md` Built State section names every
  shipped symbol and test file.
- `docs/guides/cost-preview-user-guide-v0.md` is the user-facing guide.
- Full round-by-round record: `.agent/live_review.md`, `Gate: F114 R1`
  through `R18`.

## Verification
- Integration gate (round 11): full suite clean at the merge-base with
  `main` — 19601 passed / 23 skipped / 0 failed on branch, 19554 / 23 /
  0 on base, no attribution needed.
- Closure evidence bundle (round 17, job `f114-closure`): five scoped
  suites green — `test_cost_preview.py` 19, `test_cost_preview_confirm.py`
  12, `test_cost_preview.py` (CLI acceptance) 5,
  `TestCatalogExpensive` 4, `tests/docs/` 295 — all eight closed-schema
  gates present, review zip `PACKAGE_STATUS=READY_FOR_REVIEW`
  (SHA-256 `8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810`),
  red control confirmed `BLOCKED_EVIDENCE`.
- `remedy integrity check --json` (or the `apps.cli.grouped` module
  route): `passed: true`, `fail_count: 0`, no open Blocker/High
  findings.
- Latest live-review verdict: PASS_WITH_RISKS — ACCEPTED. Open findings
  ledger-wide: 278 (pre-existing project debt, none Blocker/High,
  nothing newly introduced by this feature).

## Runtime actuals
- 18 delegated rounds across 4 sessions (self-drive, one branch, no
  paste relay).
- Wall clock / token / cost totals: not-measured (this workflow's
  ledger does not track them per round).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
PRBODY
)"

  Report the PR number and URL. Do NOT run `gh pr merge` — this round
  never merges anything.

Done when — the gates. Run each, record the REAL exit code and the REAL
output.

  G1 HYGIENE. Read `.agent/STOP` before C0a, before C2, and before C3;
     report all three. Report `git status --porcelain | wc -l` after
     each of C0a, C0b, C1 and C2, where it must be 0 each time.
  G2 TRANSPORT. `sha256sum .agent/authored/f114-r18.md
     .agent/last_block.md` — one digest, twice.
  G3 THE TWO RECORD APPENDS AT C1, each reconstructed and each with its
     own negative control. (a) `.agent/live_review.md`: base size
     immediately before C1 (expect 2408770, no trailing newline),
     RECORD17's own byte length, base + 1 + RECORD17's length vs the
     post-C1 file's length, tail-slice equality, negative control
     rejection. (b) `.agent/prose_slips.md`: base size immediately
     before C1 (expect 71035, no trailing newline), SLIPF114R18's own
     byte length, base + 2 + SLIPF114R18's length (TWO newlines, per
     constraint 3) vs the post-C1 file's length, tail-slice equality,
     negative control rejection.
  G4 THE PLAN AT C1. `.agent/plan.md` equals PLAN18 byte for byte
     (report byte lengths of each side and the boolean); `wc -l`
     (expect under 50); `grep -c '^## Goal'` and `grep -c '^## Next
     Steps'` (each expect 1).
  G5 THE FIVE CLOSURE PAIRS AT C2. For each of PAIR 1-5: report the
     FROM count in its target file immediately BEFORE C2 (must be 1),
     apply it, then report whether "TO contains FROM" matches this
     pair's own label (REWRITE = false, APPEND = true). After all five
     are applied, report README.md's new accepted-count line and Tier
     3 table row exactly as they now read, and STATUS.md's new F114
     line exactly as it now reads.
  G6 THE DOCS GATES (this round touches docs/roadmap/STATUS.md, so
     gate both, per the standing .agent/context.md constraint):
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q
     Both MUST be green before `gh pr create` runs. Report both counts;
     expect 295 and 30 respectively — if either is red, STOP before
     creating the PR and report the failure instead.
  G7 THE FOUR STATE READERS AND THE CANARY (this round rewrites
     .agent/ state):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each count; expect 515 / 52 / 21 / 16 / 42, matching every
     earlier round's baseline this session.
  G8 THE TREE, THE COMMITS, THE SWEEP AND THE PR.
       git status --porcelain            -> empty, checked immediately
         before C3 staged
       git diff --stat <round's own starting HEAD>..HEAD -- packages/
         apps/ tests/  -> empty
     Per-commit numstat cross-check (`git show --numstat`) for C0a,
     C0b, C1 (three paths) and C2 (three paths) against this handback's
     own Commits table. Report the PR number, its URL, its base/head
     branches, and that it is NOT a draft and NOT merged. Re-run
     `python3 -m apps.cli.grouped integrity check --json` (or `remedy
     integrity check --json` if not denied) one final time and report
     `passed`/`fail_count`/`high_blockers_open` — expect unchanged from
     round 17.

──────────────────────────────────────────────────────────────
═══════════════════════════════════════════════════════════════
