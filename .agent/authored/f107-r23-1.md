── STEP R23/23 — F107 Context compiler v2 — CLOSURE ─────────────
Goal:        Close F107. Record the R20, R21 and R22 gates and the closure
             verdict, apply the reviewer-authored STATUS `[x]` line with the
             README capability sync in the SAME commit, and open the PR. The PR
             is NOT merged in this session.
Bundle:      C1 save block · C2 mirror · C3 gates and closure verdict persist
             FIRST · C4 the closure commit · C5 the PR.
Change:      `.agent/authored/f107-r23-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `docs/roadmap/STATUS.md` · `README.md` ·
             `.agent/plan.md` · `.agent/handoff.md`. SEVEN paths, nothing else.
             No production code, no tests, no feature file.
Constraints: AGENTS.md in full. Rule A4: the STATUS edit is the LAST commit on
             the branch, and README ships in that same commit (R-0154) so the
             ledger cross-check never sees them disagree. Insertions per commit
             under 500. Push after every commit. Never merge the PR. Never
             force-push. Nothing is deleted.
Done when:   gates A-H below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content, per AGENTS.md DECISION D15), carrying the PR number and
             URL, the closure values, and the open-findings count.

C1 — the block was handed to you as `.remedy-wt/f107-r23-1.block.md`. Copy it,
do not retype it: `cp .remedy-wt/f107-r23-1.block.md .agent/authored/f107-r23-1.md`,
then `cmp` the two (silent, exit 0). Record `wc -l` and `sha256sum`. Commit
alone, then push:
  chore(f107): save the R23 step block verbatim

C2 — `cp .agent/authored/f107-r23-1.md .agent/last_block.md`, then `cmp` the
two (silent, exit 0). Commit alone, then push:
  chore(f107): mirror the R23 block into last block

C3 — GATES AND CLOSURE VERDICT PERSIST FIRST (planner_reviewer_prompt.md §4.4)
No finding is registered this round: the header line stays at R-0298.

PAIR_LRG is an APPEND: the TO's first line IS the FROM, the last line of the
R19 gate entry. The three new gate entries go directly beneath it.
<<<BEGIN PAIR_LRG_FROM>>>
  `LAST_REVIEWED_SHA` advances 6e1970c4 -> 65723390.
<<<END PAIR_LRG_FROM>>>
<<<BEGIN PAIR_LRG_TO>>>
  `LAST_REVIEWED_SHA` advances 6e1970c4 -> 65723390.
- Reviewer gate on R20 (2026-08-12): PASS on the three commits it made; its C6
  was blocked and its C7 correctly skipped. Range `65723390..ca8e36ab` = three
  commits over three `.agent/` paths, 242/0, 188/325 and 53/0. Transport by the
  PRIMARY shape: `.remedy-wt/f107-r20-1.block.md` and the saved copy are
  byte-identical, as are the saved copy and `.agent/last_block.md`, and both
  authored payloads were searched for as whole strings in the target and occur
  exactly 1x each. `^Done:` is 13 and `^Landed:` 0. The round stopped at the
  review-zip build, which published a package and then rejected it, exit 1: the
  worker recorded the raw error, refused to delete anything to make it pass and
  refused to write a plan asserting a rebuild that had not happened. That
  refusal is the correct behaviour and cost the round nothing but time. The
  reviewer re-ran closure precondition 2 independently and got a DIFFERENT
  result from the handback — six failures against five — which is registered as
  R-0296 rather than rounded to the expected number. Precondition 3 re-confirmed
  by the worker: integrity `passed: true`, 5 of 5 checks, untracked 0.
  `LAST_REVIEWED_SHA` advances 65723390 -> ca8e36ab.
- Reviewer gate on R21 (2026-08-12): PASS on the four commits it made; C5 and
  C6 blocked. Range `ca8e36ab..56ee7dc1` = four commits over four `.agent/`
  paths, 275/0, 219/186, 50/1 and 29/0. Both payload pairs verified verbatim in
  their targets, the D3 anchor adjacency holds, `^<<<` is 0 across the four
  state files. The round could not run because the block named a path outside
  the repository and the permission layer denies every such path; the worker
  proved it was the path rather than the command with a probe directory, then
  declined both the override flag and a subagent detour. That is the second
  consecutive worker to stop clean at a wall instead of routing around one, and
  it is the behaviour these rules exist to produce. The defect is the
  reviewer's and is registered as R-0297.
  `LAST_REVIEWED_SHA` advances ca8e36ab -> 56ee7dc1.
- Reviewer gate on R22 (2026-08-12): PASS, and the package exists. Range
  `56ee7dc1..9aacd70d` = five commits over the six `.agent/` paths the Change
  line names, 251/0, 149/173, 21/1, 35/0 and the C6 pair, each far under 500.
  Transport primary and silent both ways. Payloads verbatim: PAIR_HDR_TO,
  PAIR_LRF_TO and the D3a append each occur exactly 1x in their target,
  `.agent/plan.md` equals PAYLOAD_PLAN byte for byte, and `^## DECISION F107
  D3 ` is still 1 — the original decision was amended in the open, not
  rewritten. The package was verified by this reviewer opening it rather than
  by reading the handback: `sha256sum` returns
  4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d, matching
  the worker's value; the archive holds 4096 members of which 0 match the
  packager's own rejection regex, 0 match its local-path leak regex and 0 come
  from `.remedy-wt/.cache`, which proves the D3a prune held; and the manifest's
  committed_review_subject reads base 2e4142c3 with head b823dff9. All four
  archived items survive under `.remedy-wt/.cache/f107-archive/` — nothing was
  deleted to make a package build. Gate F's wording that the package head must
  equal the round's final HEAD was the reviewer's error and the worker was right
  to flag it: the closure protocol builds the zip before the final state commit
  BY DESIGN, so the accepted HEAD is the manifest's head and this is exactly the
  shape every prior closure has.
  `LAST_REVIEWED_SHA` advances 56ee7dc1 -> 9aacd70d.
<<<END PAIR_LRG_TO>>>

PAIR_CLOSE is an APPEND at the END of the file: the TO's first line IS the
FROM, the current last line of `.agent/live_review.md`.
<<<BEGIN PAIR_CLOSE_FROM>>>
signatures. Open findings 20 -> 19.
<<<END PAIR_CLOSE_FROM>>>
<<<BEGIN PAIR_CLOSE_TO>>>
signatures. Open findings 20 -> 19.

## Closure verdict — F107 Context compiler v2 (2026-08-12)

PASS_WITH_RISKS. The DONE sentence is met and proved: a fixture task's context
shrinks measurably against whole-files while the fake provider still reaches
`staged_review_passed`, with the reported length pinned to the exact bytes the
compiler produces so a run that bypassed compilation cannot pass by being
smaller for an unrelated reason, and every candidate path is accounted for in
`included` or in an omissions record naming one of five reasons.

Preconditions, each checked against the disk rather than a summary. (1) Every
step has a PASS round; 35 findings registered, 13 resolved, 22 open, NONE above
Medium, each carried below as a documented risk. (2) Full suite re-confirmed
after the R16 integration gate: `5 failed, 16537 passed, 19 skipped` in the
worker's run and `6 failed, 16536 passed, 19 skipped` in the reviewer's own
re-run of the same head — both recorded, never collapsed, the difference being
R-0296. (3) `integrity check` passes, 5 of 5, untracked 0. (4) Built State is
current in the feature file. (5) Tree clean, branch pushed.

Risks accepted, all Medium or Low: R-0286, the five pre-existing `[reviewer]`
role-convention failures that predate this branch and fail identically on it;
R-0296, a load-sensitive smoke test that passes alone and belongs to F252's
flake paydown; R-0295, the packager publishing local scratch before rejecting
its own package, whose one-line durable fix belongs to a follow-up that owns
`scripts/make_review_zip.sh`; R-0290 and R-0297, two reviewer-side protocol
defects whose fixes edit `docs/agents/` and so sit outside this feature's change
set; R-0291's two Design deferrals, recorded as DECISION F107 D1; and fifteen
older Low and Medium items carried from F103, F104, F105 and this feature's
earlier rounds. No risk touches the DONE sentence, and none is a defect in the
code this feature ships.

Evidence job f107-closure, verdict PASS_WITH_RISKS over 416 passing tests in
four recorded runs. Package
remedy-review-20260812-235227-READY_FOR_REVIEW.zip, SHA-256
4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d, accepted HEAD
b823dff9b4711ec3cc3505b496589cd02e219fc4, verified open by the reviewer at 4096
members with zero unsafe entries. This round's own gate has no entry above it
by construction (§4.13): it lives in the handoff and the PR.
<<<END PAIR_CLOSE_TO>>>
Commit, then push:
  chore(f107): record the R20 to R22 gates and the closure verdict

C4 — THE CLOSURE COMMIT. STATUS, README, plan and handoff in ONE commit, and it
is the LAST commit on this branch (Rule A4, R-0154). Four replacement pairs,
each unique in its file.

PAIR_STATUS is a REWRITE. In `docs/roadmap/STATUS.md` replace the one line:
<<<BEGIN PAIR_STATUS_FROM>>>
- [~] F107 — Context compiler v2
<<<END PAIR_STATUS_FROM>>>
<<<BEGIN PAIR_STATUS_TO>>>
- [x] F107 — Context compiler v2 (T001–T004 complete; accepted 2026-08-12 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f107-closure · package remedy-review-20260812-235227-READY_FOR_REVIEW.zip · SHA-256 4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d · accepted HEAD b823dff9b4711ec3cc3505b496589cd02e219fc4)
<<<END PAIR_STATUS_TO>>>

PAIR_RM1 is a REWRITE. In `README.md` replace the one line:
<<<BEGIN PAIR_RM1_FROM>>>
42 of 255 registered items accepted. Next: F107 (Context compiler v2).
<<<END PAIR_RM1_FROM>>>
<<<BEGIN PAIR_RM1_TO>>>
43 of 255 registered items accepted. Next: F111 (Diff-only repair).
<<<END PAIR_RM1_TO>>>

PAIR_RM2 is a REWRITE. In `README.md` replace the one line:
<<<BEGIN PAIR_RM2_FROM>>>
| 2 | Minimal Self-Build Runtime | 4 | 14 |
<<<END PAIR_RM2_FROM>>>
<<<BEGIN PAIR_RM2_TO>>>
| 2 | Minimal Self-Build Runtime | 5 | 14 |
<<<END PAIR_RM2_TO>>>

PAIR_RM3 is a REWRITE. In `README.md` replace the one line:
<<<BEGIN PAIR_RM3_FROM>>>
F105 cache-optimal prompt ordering.
<<<END PAIR_RM3_FROM>>>
<<<BEGIN PAIR_RM3_TO>>>
F105 cache-optimal prompt ordering, F107 context compiler v2.
<<<END PAIR_RM3_TO>>>

Then replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2 — CLOSED

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0298. Last reviewed SHA 9aacd70d (R22 PASS).

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE, and closed at PASS_WITH_RISKS: the fixture task's context
shrinks measurably against whole-files, the fake provider still solves it, and
the omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R23 — closure. The R20, R21 and R22 gates and the closure verdict are recorded,
`docs/roadmap/STATUS.md` carries the `[x]` line with the README capability sync
in the same commit, and the PR is open. 22 findings remain open, none above
Medium, each named as an accepted risk in the closure verdict.

## Next Steps
1. The PR is NOT merged by this session. It merges at the next feature's start
   via the AGENTS.md Open PR Gate — that gap is the operator's manual-review
   window, and the operator may merge manually at any time instead.
2. The next session claims the next feature under Rule A5: F111 Diff-only
   repair, the first `[ ]` line of docs/roadmap/STATUS.md.
3. Owed follow-ups, all registered: R-0295 the packager prune, R-0296 the flake
   routed to F252, R-0290 and R-0297 the two self-drive protocol gaps.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with feature, round, branch,
the C1-C4 SHAs, a changed-files table, the C1-C5 item-status table, the REAL
results of gates A-H, the closure values, the open-findings count and the PR
number. The state block repeats the operator brief's Fortschritt line verbatim:
  Fortschritt: 100 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · Evidence + Zip ✅ · STATUS [x] ✅ · PR offen, ungemergt) — Schätzung
Commit all of C4 TOGETHER, then push:
  docs(f107): close F107 in the status ledger and sync the readme

C5 — the PR. Create it, do NOT merge it, do not mark it draft:
  gh pr create --base main --head feature/f107-context-compiler-v2
Title:
  F107 Context compiler v2 — tiered selection, budget demotion, omissions record
The description carries, per AGENTS.md and STATUS_closure_protocol.md step 5:
what changed and why; the key decisions (F107 D1 the two Design deferrals, D2
the fifth omission reason, D3 and D3a the scratch archive); how to review
(the scoped suites and the canary, named with their commands); a changed-files
table for `2e4142c3..HEAD`; the latest verdict PASS_WITH_RISKS with the risk
list; the open-findings count 22 with none above Medium; and runtime actuals —
23 rounds, evidence job f107-closure, package
remedy-review-20260812-235227-READY_FOR_REVIEW.zip, wall clock and token cost
`not-measured` for the rounds before this session rather than guessed. Record
the PR number and URL. Then STOP: this session does not merge.

GATES — run every one, record the real output and the real exit code
A transport: `cmp` scratch against `.agent/authored/f107-r23-1.md` (silent,
  exit 0), its `wc -l` and `sha256sum`, and the C2 `cmp` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400.
C pairs after C3, in `.agent/live_review.md`: `Reviewer gate on R20`,
  `Reviewer gate on R21`, `Reviewer gate on R22` and `^## Closure verdict` are
  each 1; `^Done:` is still 13; `^Landed:` is 0; `^> Branch:.*Next free ID:
  R-0298` is 1. Both pairs are APPEND-shaped: each FROM stays exactly 1x and
  every non-blank TO-ONLY line occurs exactly 1x among the lines C3's own diff
  adds. Report `git show --numstat <C3> -- .agent/live_review.md` and the count
  of added lines in no TO body (must be 0).
D closure commit: `grep -c -F -- '- [x] F107 —' docs/roadmap/STATUS.md` is 1
  and `- [~] F107` is 0; `grep -c '^43 of 255 registered items accepted'
  README.md` is 1 and the `42 of 255` line is 0; the tier-2 row reads `| 5 |`;
  `grep -c -F 'F107 context compiler v2.' README.md` is 1. Prove STATUS and
  README moved in the SAME commit: `git show --name-only <C4>` lists both.
E ledger pins, the docs-round gate (this round touches docs/roadmap/**):
  `python3 -m pytest tests/docs/ -q` — exit code and pass count. The README
  accepted-count pin and the STATUS cross-check live here, so a mismatch
  between the two files turns this red.
F canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
G marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/handoff.md`, `docs/roadmap/STATUS.md` and
  `README.md`.
H tree, push, scope and PR: `git status --porcelain` empty, `git worktree list`
  the primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only 9aacd70d..HEAD` lists exactly the seven paths the
  Change line names, insertions per commit each under 500, and `gh pr list
  --state open` now returns EXACTLY ONE PR — this one, not a draft, from
  `feature/f107-context-compiler-v2` into `main`. Report its number and URL.
── END OF BLOCK ─────────────
