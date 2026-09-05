STEP CLOSURE PART 3 / F259 — Vocabulary & concept model v1 — round 10 of session 1
BRANCH feature/f259-vocabulary, head aba15f08 at the time this block was written.

Goal
  Close F259. Book the round-9 verdict, then make the ONE closure commit that
  flips the ledger, syncs the README, consumes the self-use item and rewrites the
  handback — Rule A4's last commit on the branch — and open the pull request.
  The pull request is NOT merged in this session; it merges at the next feature's
  Open PR Gate, and that gap is the operator's manual-review window.

  Every value in the STATUS line below was MEASURED by the reviewer, not
  reported: the package digest was recomputed from the file on disk
  (22 510 711 bytes), `zipfile.testzip()` returned None over its 3877 members,
  and the manifest's `committed_review_subject` was read out of
  `.review_zip_manifest.json` inside the package — base
  259617949461c993f1b8dabcf659e6a73110b162, head
  efd2a4fb04bb82b8ee87b812327a7c3f9776853a, `base_is_ancestor` true, 61 commits,
  `ready_gate_matrix.ok` true with no blocking reasons, `package_status`
  READY_FOR_REVIEW.

Finding R-0797 binds the README edit, harder than in round 6
  `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
  scans each `Accepted in Tier N so far:` block for `F\d{3}` tokens and asserts
  every one is `- [x]` in `docs/roadmap/STATUS.md`. This round ADDS a token to
  that block, which is the exact operation R-0797 was. Two things make it safe
  and both are gated: the token added is F259 itself, and the SAME commit flips
  F259 to `[x]`, so no committed state has them disagreeing (R-0154); and the
  authored entry names NO OTHER feature id — the reviewer checked its bytes for
  `F\d{3}` before emission and found only the leading F259. Do not add one.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r10.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R10 (whole rewrite)
  C2  .agent/live_review.md: append `"\n" + GATE_R9 + "\n"`
  C3  THE CLOSURE COMMIT — one commit, exactly these paths:
        docs/roadmap/STATUS.md   the STATUS pair
        README.md                the three README pairs
        scripts/self_use_queue.json  the one `consumed_by` edit
        .agent/handoff.md        the final handback
      This is the LAST commit on the branch (Rule A4). Nothing follows it.
  then push, then create the pull request (see "The pull request" below).

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r10.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md (C2) —
  docs/roadmap/STATUS.md, README.md, scripts/self_use_queue.json,
  .agent/handoff.md (C3)

Delivery
  The block is at `.remedy-wt/f259-r10-block.md`, gitignored scratch. C0a COPIES
  it to .agent/authored/f259-r10.md, C0b to .agent/last_block.md. Slices are
  extracted from the COMMITTED authored file by marker extraction in Python.

The five pairs of C3
  Each is applied with `str.replace(FROM, TO, 1)` after confirming the FROM
  occurs EXACTLY ONCE. The reviewer ran the containment test on all five before
  emission; every one printed `TO contains FROM: false`, so ALL FIVE ARE
  REWRITES and the obligation for each is FROM 0x and TO 1x afterwards — never
  an append's count.
    STATUSPAIR   docs/roadmap/STATUS.md — `[~]` becomes the accepted `[x]` line
    ACCPAIR      README.md — the Tier 2 accepted list gains F259; the previous
                 entry's closing `).` becomes `),`
    COUNTPAIR    README.md — 72 accepted becomes 73
    TIERPAIR     README.md — the Tier 2 table's Done column, 15 becomes 16
    QUEUEPAIR    scripts/self_use_queue.json — SU-010's `consumed_by` gains
                 `F259`. Apply it as a TEXT replacement, never by loading and
                 re-dumping the JSON: the file stores em dashes as `—`
                 escapes and a round-trip through `json.dump` would rewrite
                 every one of them, which is the open finding R-0785. The
                 reviewer measured `"consumed_by": ""` at exactly one occurrence
                 in the file, SU-010's, because it is the only unconsumed entry.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. Apply a slice you believe wrong verbatim and declare
     it in the handback.
  2. C3 IS ONE COMMIT AND IT IS THE LAST ON THE BRANCH. The STATUS flip and the
     README sync may never be in different commits (R-0154): no committed state
     of this repository may have README and STATUS disagreeing about what is
     accepted.
  3. Read `.agent/STOP` from disk before C0a and before C3.
  4. NEWLINE CONVENTIONS: PLANF259R10 replaces `.agent/plan.md` whole with
     exactly one trailing newline; the record append is as described;
     `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` each
     still end with exactly one newline after their edits.
  5. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, `${PIPESTATUS[0]}`,
     a `$` anchor inside a `grep -c` pattern, brace-with-quote literals in a
     heredoc, and a non-ASCII character in a Python bytes literal. Re-express in
     Python and report the Python you ran beside its output, with any refusal
     quoted verbatim. `ruff check` and the built `remedy` CLI are denied; use
     `python3 -m apps.cli.grouped <...>` where a remedy subcommand is needed.
  6. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path, no secret-like string — the evidence-packaging metadata scanner
     rejects such subjects. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  7. AGENTS.md binds you in full. Never `--force`, never a history rewrite,
     never a branch deletion, and NEVER `gh pr merge` — the merge belongs to the
     next feature's Open PR Gate and is the operator's review window.
  8. If ANY gate below comes back wrong, do NOT create the pull request. Commit
     what is sound, report the failure, and stop; the reviewer decides.

The pull request — after C3 is pushed
  Write the PR body to a scratch file under the gitignored `.remedy-wt/` and run
    gh pr create --title "F259: vocabulary and concept model v1" --base main --head feature/f259-vocabulary --body-file <file>
  The body carries: what changed and why; the key decisions (DECISION F259 D3,
  and the §3 checklist consolidation that merged item 32 into item 16 and retired
  the number); how to review; the changed-files table; the latest live-review
  verdict; the open-findings count; and the runtime actuals below. Report the PR
  number and URL in your final message. NEVER `gh pr merge`.
  The PR number cannot be inside `.agent/handoff.md`, because C3 writes that file
  and C3 is the last commit (Rule A4) — this is the R-0449 shape and the block
  accepts it rather than ordering an impossible value: the number lives in your
  final message and in the pull request itself, and `gh pr list` recovers it.

Runtime actuals for the PR body (observed; `not-measured` beats a guess)
  Rounds: 10 delegated rounds, all PASS at the reviewer's gate, one session.
  Wall clock: not-measured as a total; the integration gate's two full-suite runs
  were 134.50s (branch) and 161.68s (base), and the self-use job ran 107.8s.
  Models/tokens/cost: not-measured — no provider ledger was consulted for this
  feature, and the only model calls were the self-use job's own, inside its
  `max_provider_calls=6` / `max_cost_usd=0.5` budget.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Gates G1 through G7 run at or before C3; G8 covers the push and the PR
and is reported in your final message as well as in the PR.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r10-block.md .agent/authored/f259-r10.md .agent/last_block.md`
     — one digest, three times.
  G2 THE RECORD APPEND. The pre-append bytes of `.agent/live_review.md` are a
     byte-exact PREFIX of the post-append bytes, the remainder equals exactly
     `"\n" + GATE_R9 + "\n"`, and `grep -c '^Gate: R9 — '` goes 0 → 1. Report the
     byte lengths.
  G3 THE FIVE PAIRS. For EACH: the FROM count before (1), the printed containment
     reading with the label derived from it on the same line, the FROM count after
     (0) and the TO count after (1). Then the whole-file reconstruction for each
     of the three files: the post-commit bytes equal the pre-commit bytes with
     exactly its pairs applied and nothing else — three booleans.
  G4 THE LEDGER AND THE README AGREE — R-0154 and R-0797 together. After C3,
     from the COMMITTED state, report:
       `grep -c '^- \[x\] F' docs/roadmap/STATUS.md`            expect 73
       `grep -c '^- \[~\] F' docs/roadmap/STATUS.md`            expect 0
       the F259 STATUS line, in full, verbatim
       the accepted-per-tier counts, Tier 2 expect 16
       the README's `N of 271 registered items accepted` numeral, expect 73
       the README Tier 2 table row, expect Done 16
     Then the R-0797 sweep, which is the point: extract EVERY
     `Accepted in Tier N so far:` block from `README.md`, collect EVERY `F\d{3}`
     token in them, and report the FULL sorted list with, for each, whether
     `docs/roadmap/STATUS.md` carries it as `- [x]`. Every one must be `[x]`, F259
     among them, and the list is reported in full and never as a count alone.
  G5 THE SELF-USE ITEM IS CONSUMED — closure precondition 6. Report SU-010's
     `consumed_by` value after C3 (expect `F259`); the count of entries in
     `scripts/self_use_queue.json` with an empty `consumed_by` (expect 0); the
     total entry count (expect 10); and the boolean that the file's bytes differ
     from their pre-commit state ONLY by the QUEUEPAIR replacement. Also report
     the count of the literal two characters `\u` followed by `2014` in the file
     before and after — they must be EQUAL, which is what proves no JSON
     round-trip reformatted the file (open finding R-0785).
  G6 THE SUITES, RUN SERIALLY, at C3. Each a real run with its passed count and
     exit code. The reviewer measured at aba15f08:
       python3 -m pytest tests/docs/ -q                                 expect 303
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q   expect 30
       python3 -m pytest tests/ui_server/ -q                            expect 515
       python3 -m pytest tests/orchestration/test_test_runner.py -q     expect 52
       python3 -m pytest tests/regression/test_resource_safety.py -q    expect 21
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q  expect 16
       python3 -m pytest tests/cli/test_golden_path.py -q               expect 42
       python3 -m pytest tests/orchestration/test_self_use_generator.py -q  report the number
     The last is added because this round consumes a queue entry. `tests/docs/`
     is the one that would catch a README/STATUS disagreement, so run it AFTER C3
     is committed, not before. A different count is reported as the number it is,
     with failing node ids verbatim.
  G7 THE CLOSURE PRECONDITIONS RESTATED AGAINST THE FINAL STATE.
     `python3 -m apps.cli.grouped integrity check --json` — report `passed` and
     `fail_count`. `git status --porcelain` — empty. The open-findings count,
     computed as `^- R-\d{4} — ` lines minus `^Done: R-\d{4} — ` lines in
     `.agent/live_review.md` — report the number. And confirm
     `.agent/candidates.md` is unchanged by this round, since no candidate was
     raised.
  G8 STRUCTURE, THE PUSH AND THE PULL REQUEST. Every commit single-parent;
     `git diff --numstat <parent> <commit>` for EACH commit C0a through C3
     reported cell by cell; each commit's insertion count against the 500 cap;
     `git ls-files .remedy-wt` returns nothing; the push result; that C3 is the
     branch tip and NOTHING follows it; the PR number, its URL, that it is not a
     draft, that its base is `main` and its head is `feature/f259-vocabulary`,
     and that it is NOT merged. Report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

The handback, inside C3 — rewrite .agent/handoff.md whole
  No length cap. It is the last state this branch leaves behind, so it carries:
  feature, round and SESSION NUMBER — SESSION 1 of F259, round 10, rounds so far
  10, and the feature CLOSED; the commit range for this round and the accepted
  HEAD `efd2a4fb04bb82b8ee87b812327a7c3f9776853a`; the evidence job id, package
  filename, SHA-256 and package path exactly as they appear in the STATUS line;
  a `## Commits` table with the `+/-` numbers G8 printed for C0a through C3; the
  AGENTS.md item-status table, one row per bundle item; one line per gate G1
  through G7 with its real reading, plus what G8 could measure before the commit;
  the deviations; ONE sentence of context self-assessment; the open-findings
  count; and the next expected action — the operator's review window, then the
  next feature's Open PR Gate merging this pull request. Say plainly that the
  pull request number is NOT in this file and why (Rule A4 makes C3 the last
  commit; the number is in the round's final message and recoverable with
  `gh pr list`). Repeat this line verbatim in its state block:
  `100 % (T001–T004 ✅ · Integration Gate ✅ · Closure ✅ — F259 geschlossen, PR offen) — Schätzung`

<<<BEGIN PLANF259R10>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 9
PASSED the reviewer's gate. Round 7 was the integration gate — the full suite
green on the branch and at the merge base, zero branch-only and zero base-only
failures. Rounds 8 and 9 were closure parts 1 and 2; the package is built and
READY_FOR_REVIEW.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 10 is CLOSURE PART 3 — the last round. One commit flips the STATUS line to
accepted, syncs the README's counters and its Tier 2 accepted list, marks the
self-use item consumed and rewrites the handback; it is the last commit on the
branch. Then the pull request is opened and left UNMERGED, which is the
operator's review window.

## Next Steps

- The operator reviews the package at their own pace.
- The next feature's session merges this pull request at its Open PR Gate, then
  claims the next unchecked line in the DECISION amend0905-vocab D12 order,
  which is F260 — one world: mission, job, run.

## Risks

- The README and the STATUS ledger must never disagree in any committed state,
  which is why one commit carries both. A split would leave a state where the
  README claims an acceptance the ledger does not.
- The pull request must not be merged in this session. Merging it here would
  close the operator's review window before it opened.
<<<END PLANF259R10>>>

<<<BEGIN GATE_R9>>>
Gate: R9 — the F259 R9 entry, CLOSURE PART 2. VERDICT PASS. Range 32808b5d..aba15f08, seven commits, all single-parent, pushed, no pull request; largest commit 303 insertions, so the AGENTS.md DECISION F104 D1 exemption was not needed for the rotation commit, which carried 8. The change set is exactly the ordered paths and the reviewer confirmed with `git diff --name-only` that `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are named nowhere in it — they belong to the single closure commit that must carry them together under R-0154. TRANSPORT: one digest `5ae765ed108327d52ed5b9e216a859a2186c9ef7b7b601ffae2ac66b18be8da0` across the scratch file, the saved copy and the mirror, equal to the reviewer's own pre-emission digest; a COPY chain per §3 item 37. THE FOUR LEDGER PARAGRAPHS LANDED BYTE-EXACTLY: `.agent/live_review.md` at 3a5f006f equals its parent plus exactly `"\n" + GATE_R8 + "\n\n" + FIND0813 + "\n\n" + REC0784 + "\n\n" + DONE0418 + "\n"` (848 281 to 859 557 bytes), and `.agent/prose_slips.md` equals its parent plus exactly `"\n\n" + SLIP9`, still ending with no newline. THE R-0813 REPAIR: `docs/agents/planner_reviewer_prompt.md` at a7c72f25 equals its parent with the single FROZENFIX replacement and nothing else; the paragraph now contains `measures against 36` exactly once and `the number the next consolidation measures against` zero times; and the per-item digest sweep the reviewer re-ran independently shows the checklist still at 36 items numbered 1 to 31 and 33 to 37 with ZERO item texts changed, which is what a repair confined to the frozen paragraph must look like. THE ROTATION HELD ITS INVARIANT, measured by the reviewer from the committed blobs on both sides: before, 300 registrations against 6 `Done:` lines; after, 298 against 4; open findings 294 on BOTH sides, which is the equality `scripts/rotate_live_review.py` guarantees and refuses on. The ledger fell from 859 557 to 851 727 bytes and the archive rose from 1 723 631 to 1 731 461; the resolved `R-0418` pair is now in the archive, one registration and one `Done:`, and is gone from the live ledger, which is the intended effect of resolving it. THE PACKAGE WAS VERIFIED BY THE REVIEWER FROM THE FILE ON DISK, not from the worker's report: `remedy-review-20260906-004320-READY_FOR_REVIEW.zip` in `/home/decodeux/Repos/remedy-history/zips`, 22 510 711 bytes, sha256 recomputed as `164f9513a4608030989590daf647d9a96a1c2c0b78f4fb469461966024fd56e3` — equal to the worker's value — `zipfile.testzip()` returning None over 3877 members with no `.log` member among them, and its `.review_zip_manifest.json` read out of the archive giving `committed_review_subject` base `259617949461c993f1b8dabcf659e6a73110b162`, head `efd2a4fb04bb82b8ee87b812327a7c3f9776853a`, `base_is_ancestor` true over 61 commits, `ready_gate_matrix.ok` true with an empty `blocking_reasons`, `package_status` READY_FOR_REVIEW, and the evidence job id `ace7fa4d9d782a7a` present. The evidence bundle's own final verdict is PASS_WITH_RISKS over 8 authority gates, and its one verification run records `tests/docs/` at 303 selected with 303 node ids and two sorted real file paths — the scoped shape closure algorithm step 1 requires, with no full-suite node-id list anywhere. SUITES, re-run by the reviewer: `tests/docs/` 303 and `tests/cli/test_golden_path.py` 42, both reproducing the worker's numbers. THE WORKER'S TWO HONESTY NOTES ARE ACCEPTED AS WRITTEN. `vt_passed` is ABSENT from this manifest rather than null, so a `None` read there means absent-key and not a rejected VerificationTests document — the record was accepted on its own merits and `ready_gate_matrix.ok` is true. The manifest's `dirty_file_count_total` reads 1 while `git status --porcelain` was empty and its own `git_status_snapshot.status` reads OK; the worker reported the discrepancy without explaining it, which is the correct disposition for a number it did not establish, and that block's verdict is PASS with zero issues. Neither is a finding: nothing false is claimed anywhere and no gate over production code is blind.
<<<END GATE_R9>>>

<<<BEGIN STATUSPAIR_FROM>>>
- [~] F259 — Vocabulary & concept model v1
<<<END STATUSPAIR_FROM>>>

<<<BEGIN STATUSPAIR_TO>>>
- [x] F259 — Vocabulary & concept model v1 (T001–T004 complete; accepted 2026-09-06 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job ace7fa4d9d782a7a · package remedy-review-20260906-004320-READY_FOR_REVIEW.zip · SHA-256 164f9513a4608030989590daf647d9a96a1c2c0b78f4fb469461966024fd56e3 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD efd2a4fb04bb82b8ee87b812327a7c3f9776853a)
<<<END STATUSPAIR_TO>>>

<<<BEGIN ACCPAIR_FROM>>>
the remaining nine belong to the follow-up feature the STATUS ledger
registers next).
<<<END ACCPAIR_FROM>>>

<<<BEGIN ACCPAIR_TO>>>
the remaining nine belong to the follow-up feature the STATUS ledger
registers next),
F259 vocabulary & concept model v1 (the binding page
`docs/system/vocabulary.md`: one row per word with its meaning, its code
spelling today and after the rename features, its CLI spelling and what it
is NOT; the do-not-confuse table; the concept diagram, byte-equal in this
README and pinned against the page by a test; and the rulings that decided
them, copied verbatim from the build record).
<<<END ACCPAIR_TO>>>

<<<BEGIN COUNTPAIR_FROM>>>
72 of 271 registered items accepted.
<<<END COUNTPAIR_FROM>>>

<<<BEGIN COUNTPAIR_TO>>>
73 of 271 registered items accepted.
<<<END COUNTPAIR_TO>>>

<<<BEGIN TIERPAIR_FROM>>>
| 2 | Minimal Self-Build Runtime | 15 | 24 |
<<<END TIERPAIR_FROM>>>

<<<BEGIN TIERPAIR_TO>>>
| 2 | Minimal Self-Build Runtime | 16 | 24 |
<<<END TIERPAIR_TO>>>

<<<BEGIN QUEUEPAIR_FROM>>>
      "consumed_by": ""
<<<END QUEUEPAIR_FROM>>>

<<<BEGIN QUEUEPAIR_TO>>>
      "consumed_by": "F259"
<<<END QUEUEPAIR_TO>>>
