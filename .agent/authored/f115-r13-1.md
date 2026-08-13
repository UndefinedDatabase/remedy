── STEP R13 — F115 · session close-out ────────────────────────────────────────
Goal:        Put R12's verdict and the round's last finding on disk, then hand
             the session off at its stated round cap with the record complete.

Bundle:      C1a save this block · C1b mirror it · C2 findings and verdict text
             (own commit, FIRST) · C3 plan + handoff.

Change:      Exactly these paths: .agent/authored/f115-r13-1.md (new),
             .agent/last_block.md, .agent/live_review.md, .agent/plan.md,
             .agent/handoff.md. No code, no tests, no docs/.

── C2 — .agent/live_review.md, OWN COMMIT, FIRST ──────────────────────────────
APPEND both texts below to the END of the file, in this order, each separated
from its neighbour and from the current last line by one blank line. The file
currently ends with the R-0332 entry's "own gate. Fixed in R12, which opens
that module for the goldens anyway. OPEN." line.

Done: R-0332 — RESOLVED at the R12 gate. Verified against the code and a live probe, not the report: `_same_question` now compares `(ledger_path, ledger_exists)` as well as `(since, job_id)`, and the reviewer re-ran the probe class itself — deleting the whole ledger guard in a disposable worktree fails exactly `test_a_pair_from_two_different_ledgers_is_refused_by_both_renderers` and nothing else, so the test catches the regression rather than passing alongside it. The docstring now states WHY the None/None case is not a hole: `merge_cost_reports` deliberately clears `ledger_path` for a cross-project total, so two merged reports compare equal to each other and to nothing else. The R12 round as a whole is PASS. The reviewer re-ran every gate itself: cmp exit 0 with sha256 a3106079f0a10af038120b60380b35c46ceac247c8e66dbb90de15fde38560ca over both copies, `wc -lc` 276 19049, the live-review counts 0/5/13/1, ruff `All checks passed!` and the import exit 0, `15 passed` and `99 passed` and canary `42 passed` (156 in one run), `wc -l .agent/plan.md` 43, an empty porcelain, 0/0 against origin, and 35 changed paths with no `.remedy-wt/**` among them. Determinism was re-established independently rather than accepted: the fifteen tests were re-run under two separate `--basetemp` roots and passed both times, so the golden bytes do not depend on where the fixture ledger was built. A THIRD probe, of the reviewer's own choosing and not ordered by the block, settled the question a golden pair actually has to answer — whether it binds the ledger or only the renderer: inserting `report.rows = []` into `query_segment_shares` turns BOTH goldens red, so the pair tests the query-to-renderer seam end to end and is not a snapshot of the formatter alone. One ordered-but-absent detail, deliberately NOT registered as a finding: the block offered a `Landed: R-0332` marker if the fix outran its review, and none was written. The marker exists so a session dying between a fix and its gate leaves an unambiguous disk state, and here the reviewer-authored R-0332 entry already said "Fixed in R12" in the same file, so the marker would have restated a fact the record already carried. The worker's one unordered edit is likewise correct and was declared: C4 made the test module's docstring claim "this module reads no ledger" false, and scoping that sentence to the property tests was better than preserving a false claim to keep a diff narrow.

- R-0333 — Low — reviewer red-proof arithmetic, self-registered, second of the
  over-prediction sibling class after R-0328. R12's gate (j) ordered the
  `_share_percent` mutation with the words "Both golden byte-comparisons MUST
  fail." Only the markdown one can. `cost_report_json` renders no percentage at
  all — the share cell is a markdown-only presentation computed over raw ints,
  and the json carries `tokens_estimated` unformatted — so `_share_percent` is
  unreachable from the json path and its golden cannot move when the format
  string does. Measured by the reviewer at the R12 gate: `grep -c '%'` over
  `tests/orchestration/fixtures/cost_report/golden/cost_report.json` prints 0,
  and the re-run mutation gives `2 failed, 13 passed` —
  `test_the_share_column_uses_the_attributed_total_as_its_denominator` and
  `test_the_golden_markdown_matches_the_fixture_ledger`, not the json golden.
  The worker measured both, reported the real numbers, declared the deviation
  and adjusted nothing to reach the ordered count — the correct behaviour, and
  the round paid one declared deviation for a reviewer's arithmetic again.
  Checklist item 5 governs a red-proof's REACHABILITY and item 8 the VALUE a
  gate asserts; this class is the blast RADIUS, and the standing counter-measure
  is the one item 5 already names — order the PROBE, not the colour, whenever
  the mutated branch's reach is not obvious. Here it was not obvious for a
  reason worth recording: the two goldens are rendered from ONE pair of reports
  by two functions that do not share a formatting path, so "the golden pair"
  reads as one artifact and behaves as two. Seventh instance of the
  reviewer-arithmetic family overall, after R-0282, R-0321, R-0323, R-0324,
  R-0327, R-0328 and R-0331. No on-disk fix: the block is committed verbatim by
  design and R12's verdict stands as PASS. OPEN.

── C3 — state ────────────────────────────────────────────────────────────────
Rewrite `.agent/plan.md` (under 50 lines, keep "## Goal" and "## Next Steps").
It must record: last reviewed SHA a228feb9 (R12 PASS); next free finding ID
R-0334; open findings 8 — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328,
R-0331, R-0333; R-0329, R-0330 and R-0332 resolved at their gates; no PR and
closure not started; T001 and T002 both DONE, with the renderer, the golden
pair and the query all on disk; Next Steps 1 = T003, the `remedy stats report`
CLI with `--until`, the prior-period comparison, the json schema and the docs
page the new user-visible behaviour needs, plus making
`stats_ledger_cmd.UNMEASURED` an import of `COST_UNMEASURED_LABEL` so the
concept keeps one spelling; then the integration gate, then closure. End with
the Fortschritt line below, verbatim.

Rewrite `.agent/handoff.md` per AGENTS.md with the mandated tables and real
values (item-status table, commit table, changed-files table, gate values,
open-findings count, next expected action). It must state plainly that the
SESSION ENDED AT ITS STATED ROUND CAP of three rounds (R11, R12, R13) with the
handoff written, which guardrail G7 of `docs/agents/self_drive_protocol.md`
defines as a SUCCESS and not a failure; that R11 and R12 were both reviewed and
both PASS, with R13's own verdict living only here and in the completion report
by construction (`docs/agents/planner_reviewer_prompt.md` §4 item 13 — the last
round of a branch has no on-disk gate entry, and that absence is the terminator,
not a missing gate); and that the next session resumes at T003 on this same
branch, since no PR exists and the Open PR Gate therefore has nothing to merge.
Repeat this line verbatim as the last line of BOTH files:
Fortschritt: 80 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung

Constraints:
 - C2 is its own commit and comes first.
 - Append only in C2: do not edit, re-wrap or renumber any existing line of
   `.agent/live_review.md`.
 - Write no `Done:` paragraph of your own; C2's text is reviewer-authored and
   complete.
 - No code, no test, no docs/ file is touched this round.

Done when — run every command and record its REAL output and exit code:
 (a) cmp .agent/authored/f115-r13-1.md .agent/last_block.md  → exit 0; report
     sha256sum of both and `wc -lc` of one.
 (b) In .agent/live_review.md after C2:
       grep -c '^Done:'     → 6   (five before this round, plus R-0332)
       grep -c '^- R-0'     → 14  (thirteen before, plus R-0333)
       grep -c '^## Steps'  → 1
       grep -c '^Landed:'   → 0
     and, scoped to that commit's ADDED lines only
     (`git show <sha> -- .agent/live_review.md | grep '^+'`), each of
     `^+Done: R-0332` and `^+- R-0333` appears exactly 1x.
     Also confirm the commit's diff shows ZERO deleted lines for that file
     (`git show --numstat <sha> -- .agent/live_review.md`).
 (c) python3 -m pytest tests/cli/test_golden_path.py -q   → 42 passed (canary).
 (d) python3 -m pytest tests/orchestration/test_cost_report.py -q → 15 passed,
     unmoved by a state-only round.
 (e) wc -l .agent/plan.md                                  → under 50
 (f) git status --porcelain                                → empty
 (g) git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD
                                                           → 0  0
 (h) git diff --name-only 0d6c97aa..HEAD | wc -l  → report the number and
     confirm no `.remedy-wt/**` path is among them.

Handback:    completion report with the item-status table + rewrite
             .agent/handoff.md.
──────────────────────────────────────────────────────────────────────────────
