You are the WORKER for F103 R8 (SPLIT round): CLOSURE PART 2 — the STATUS `[~]`->`[x]` line, the README capability sync in the SAME commit, the final `.agent` state, and the PR. Per docs/roadmap/STATUS_closure_protocol.md algorithm steps 4-6.

Read from disk before acting: AGENTS.md (highest authority), docs/roadmap/STATUS_closure_protocol.md, .agent/plan.md, .agent/live_review.md, .agent/handoff.md.

R7 verdict is PASS. LAST_REVIEWED_SHA `09d7ab2d`. Accepted head for the package: `65e1eec2`. Open findings 0.

You are the ONLY writer. The reviewer is read-only and re-runs every verification itself. Never force-push. Never work on main. `git add -A` is forbidden — stage exact paths.

CRITICAL — DO NOT MERGE. Create the PR and stop. This session does not merge the PR it creates (closure protocol step 6). Do not run `gh pr merge`. Do not delete any branch.

── STEP closure-2/2 — F103 ────────────────────────────────────
Goal:        Flip the roadmap ledger to accepted, sync the README in
             the same commit, land the final state, and open the PR.
Bundle:      1 save the block · 2 apply the six authored texts ·
             3 gates · 4 the closure commit (LAST on the branch) ·
             5 push + PR · 6 handback
Change:      `.agent/**`, README.md and docs/roadmap/STATUS.md ONLY.
             No source, no tests, no feature file, no other doc.
Constraints: The STATUS edit is the LAST commit on the branch
             (Rule A4). README and STATUS may never disagree in any
             committed state, so they land TOGETHER (R-0154).
Done when:   Docs gate and canary green, tree clean, branch pushed,
             PR created and NOT merged.
Handback:    Completion report + rewrite .agent/handoff.md (in the
             closure commit itself) — see 6.
───────────────────────────────────────────────────────────────

1. SAVE THE BLOCK (own commit, first)
   Save this entire prompt verbatim to `.agent/last_block.md`.
   COMMIT 1: exactly that file, message
   "chore(f103): save the R8 closure block".

2. APPLY THE SIX AUTHORED TEXTS
   Six authored texts follow at the bottom, delimited by BEGIN/END
   markers. The authored bytes are everything BETWEEN the marker
   lines, including the final newline; the marker lines are never
   content.
   Save them to `.agent/authored/f103-r8-1.md` through
   `.agent/authored/f103-r8-6.md` and verify each with `sha256sum`
   against its BEGIN-marker hash. Any mismatch → STOP, hand back
   naming the block and BOTH hashes; apply nothing.
   Then apply, all in the working tree (do not commit yet):
   a. f103-r8-1 → `docs/roadmap/STATUS.md`. ONE pair, a REWRITE. The
      FROM is the whole F103 line and occurs exactly 1x. Report FROM
      1x / TO 0x before, FROM 0x / TO 1x after. Touch no other line:
      `wc -l docs/roadmap/STATUS.md` must be identical before and
      after, and `grep -c '^- \[~\]' docs/roadmap/STATUS.md` must go
      from 1 to 0.
   b. f103-r8-2 → `README.md`. THREE pairs, all REWRITES. Each FROM
      occurs exactly 1x. Report the before/after counts for all three.
   c. f103-r8-3 → `.agent/live_review.md`. TWO pairs, both REWRITES.
      Each FROM occurs exactly 1x. Report the before/after counts.
   d. f103-r8-4 → `.agent/plan.md`, COMPLETE replacement by
      `cp .agent/authored/f103-r8-4.md .agent/plan.md`, then
      `cmp` the two and record the exit code.
   e. f103-r8-5 → `.agent/candidates.md`, COMPLETE replacement by
      `cp`, then `cmp` and record the exit code. This file keeps
      R-0221 and ADDS the commit-size counting candidate. It must
      NOT be emptied — both entries are the next feature's
      claim-time block condition.
   f. f103-r8-6 is the PR body. It is saved and committed, but it is
      NOT applied to any tracked file — it is used verbatim in 5.

3. GATES (run against the working tree, before the closure commit)
   Both must exit 0:
     python3 -m pytest tests/docs/ -q
     python3 -m pytest tests/cli/test_golden_path.py -q
   The docs gate is the pin that proves README and STATUS agree; a
   red gate here means the ledger edit is wrong. Red → STOP and hand
   back the raw output. Also run and record:
     python3 -m apps.cli.grouped integrity check --json

4. THE CLOSURE COMMIT (LAST on the branch)
   Write the new `.agent/handoff.md` (see 6) FIRST, then make ONE
   commit staging exactly these paths and nothing else:
     docs/roadmap/STATUS.md
     README.md
     .agent/live_review.md
     .agent/plan.md
     .agent/candidates.md
     .agent/handoff.md
     .agent/authored/f103-r8-1.md .. .agent/authored/f103-r8-6.md
   Message subject exactly:
     docs(f103): accept F103 in the roadmap ledger and sync the readme
   Body: what was accepted, the evidence job / package / SHA-256 /
   accepted HEAD, that README is synced in the SAME commit so no
   committed state has the two disagreeing (R-0154), that the PR is
   not merged by this session, and that `.agent/candidates.md`
   carries two entries as the next feature's claim-time block
   condition. End the message with the trailer
   `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
   Commit subjects must not contain leading-slash tokens, absolute
   paths or secret-like strings — the evidence metadata scanner
   rejects them.
   Then verify: `git status --porcelain` empty, and
   `git log --oneline -1` is this commit.

5. PUSH AND PR
   `git push`.
   Then create the PR — and do NOT merge it:
     gh pr create --base main --head feature/f103-token-ledger \
       --title "F103 — Token ledger (SQLite)" \
       --body-file .agent/authored/f103-r8-6.md
   Record the PR number and URL. Then run
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   and record the raw output: it must show exactly this one PR, not a
   draft, `feature/f103-token-ledger` -> `main`.
   Do NOT run `gh pr merge`. Do NOT delete the branch.

6. HANDBACK — `.agent/handoff.md`, rewritten inside the closure commit
   It carries:
   - feature + round, branch, the per-commit changed-files table for
     both commits (a commit cannot table its own SHA — table the
     closure commit by role);
   - transport proofs: the six sha256 verifications, the before/after
     pair counts for STATUS (1), README (3) and live_review (2), and
     the two `cmp` exit codes for plan.md and candidates.md;
   - the verification table with REAL exit codes: docs gate, canary,
     integrity check, final `git status --porcelain`;
   - the STATUS line proof: `wc -l` identical before/after and the
     `[~]` count going 1 -> 0;
   - the closure values as accepted: Evidence job `f103-closure`,
     package `remedy-review-20260808-210612-READY_FOR_REVIEW.zip`,
     SHA-256 `8e967d78e57fa97641365b4baa91ca884f6322bc855f678d1daeb146c9dd38ad`,
     accepted HEAD `65e1eec25e61c1d0fe78539adeb890d3426cb605`;
   - the PR number and URL, and the explicit statement that it was
     NOT merged;
   - the item-status table (AGENTS.md), bundle items 1-6 exactly
     once each, with `done` / `skipped` / `deviated` and a reason;
   - open findings **0**, and the note that `.agent/candidates.md`
     carries TWO entries which are the next feature's claim-time
     block condition;
   - next expected action: the next feature (F104, Rule A5) in a
     FRESH session, whose Open PR Gate merges this PR.
   - any deviation, DECLARED. The stated-cause overage clause
     applies: never drop a mandated section to meet the line cap.

AUTHORED TEXTS

<<<BEGIN AUTHORED f103-r8-1
sha256=713a7e26a6ba9114898b2ea6aab301984c610023d30b2543ae86aa4b10e09d6f>>>
PAIR 1 — REWRITE
FROM:
- [~] F103 — Token ledger (SQLite)
TO:
- [x] F103 — Token ledger (SQLite) (T001–T003 complete; accepted 2026-08-08 · live review PASS — ACCEPTED · Evidence job f103-closure · package remedy-review-20260808-210612-READY_FOR_REVIEW.zip · SHA-256 8e967d78e57fa97641365b4baa91ca884f6322bc855f678d1daeb146c9dd38ad · accepted HEAD 65e1eec25e61c1d0fe78539adeb890d3426cb605)
<<<END AUTHORED f103-r8-1>>>

<<<BEGIN AUTHORED f103-r8-2
sha256=d71606371fb801fda081d265d7c053d384d3bcead0a9a71e365e64cf098c2b3c>>>
PAIR 1 — REWRITE
FROM:
39 of 255 registered items accepted. Next: F103 (Token ledger (SQLite)).
TO:
40 of 255 registered items accepted. Next: F104 (Hard budget enforcement).

PAIR 2 — REWRITE
FROM:
| 2 | Minimal Self-Build Runtime | 1 | 14 |
TO:
| 2 | Minimal Self-Build Runtime | 2 | 14 |

PAIR 3 — REWRITE
FROM:
Accepted in Tier 2 so far:
F254 model alias table & dead-model doctor check.
TO:
Accepted in Tier 2 so far:
F254 model alias table & dead-model doctor check,
F103 token ledger (SQLite).
<<<END AUTHORED f103-r8-2>>>

<<<BEGIN AUTHORED f103-r8-3
sha256=00be41a5fe574cb96d6e244e7a0b01319581ff36147c6d2de0c07036175fd62d>>>
PAIR 1 — REWRITE
FROM:
  those values exist (F079 R4/R5 and F254 R11/R12 precedent).
TO:
  those values exist (F079 R4/R5 and F254 R11/R12 precedent) — PASS.

PAIR 2 — REWRITE
FROM:
- R7: in flight — closure part 1. Awaiting the handback with the
  evidence job id, the package filename, its SHA-256 and the content
  HEAD the zip records as the accepted head.
- R8: pending — closure part 2.
TO:
- R7 (closure part 1) — **PASS**. Reviewed `f69990a1..09d7ab2d`
  bottom-up across five commits. The change set is exactly the
  mandated two-path family — `.agent/**` and
  `docs/roadmap/features/T2_F103.md` — with STATUS.md, README.md,
  every source file and every test file untouched, so no part of the
  closure claim was smuggled in early. Transport is proved
  disk-to-disk against the REVIEWER'S OWN scratchpad originals rather
  than by the digest fallback: `cmp` of each of the three
  `.agent/authored/f103-r7-*.md` files against its original returned
  **exit 0 x3**. Both `live_review.md` pairs are genuine REWRITES —
  the reviewer re-parsed the FROM and TO strings out of the committed
  receipt and confirmed neither TO contains its FROM — and after the
  edit each is FROM **0x** / TO **1x**. `.agent/plan.md` equals its
  authored file (`cmp` exit 0). The Built State landing is a PURE
  APPEND, proved twice over: 5263 B before + 4376 B authored = 9639 B
  after, `tail -c 4376` byte-identical to the authored file, and
  `git diff` +69/-0.
  The load-bearing claim is the one this round existed to make, and
  the reviewer made it on its OWN run: `python3 -m pytest -n auto -q`
  → **16131 passed, 19 skipped in 112.64s, exit 0**, matching the
  handback exactly. The +10 delta against the R5 gate's 16121 is
  VERIFIED rather than asserted: `test_token_ledger.py` collected
  **72** tests at the gate head `af91d57b` and collects **82** now, so
  the entire full-suite delta is R6's live-mirror tests and nothing
  else moved. R6's production code is therefore covered by full-suite
  evidence — the debt the R6 verdict recorded is paid.
  The package was checked by the reviewer, not read from the
  handback: disk `sha256sum` == `8e967d78…d38ad`; `zipfile.testzip()`
  reports no corrupt member across 2211 members; the packaged
  `.review_zip_manifest.json` records `package_status=
  READY_FOR_REVIEW`, `committed_review_subject` spanning
  `c1c0fbcb…a05d..65e1eec2…b605` with `base_is_ancestor=true`, 39
  commits and 51 files, `ready_gate_matrix.ok=true` with
  `blocking_reasons: []`, an alignment verdict of PASS with zero hash
  mismatches and zero uncovered source or test files, and
  `final_verifier_reproducible=true` (`VERIFIED_EQUAL`). All eight
  closed-schema gates are on disk, so this is a real bundle and not a
  lone runtime gate. Every named packaging pitfall was checked
  individually and met: `run_id` `vr-0001`/`vr-0002`, bare 64-hex
  `output_hash`, `test_files` that are files, and
  `len(node_ids) == selected` on both runs — and the ids are REAL,
  not merely well-shaped: the reviewer re-collected both suites and
  the 115 recorded ids are exactly the 115 collected ids, zero extra
  and zero missing, which is the F080 BLOCKED_EVIDENCE class closed
  by evidence. `test_status.passed=115` equals 82+33, so the
  fail-closed VerificationTests confirmation in
  `build_review_manifest` is satisfied rather than bypassed. The
  evidence dir is untracked and ignored and contributes ZERO files to
  the review subject.
  Reviewer-run verification: the full suite as above, `tests/docs/`
  **294 passed**, canary **42 passed**, `integrity check --json`
  `"passed": true` across 5/5 checks with `relevant_untracked` 0,
  `git status --porcelain` empty, branch in sync with origin, and
  `gh pr list --state open` still `[]`. Verification tier: CLOSURE
  CONFIRMATION — the second and last of this feature's two full-suite
  runs. No block condition.
  Declared deviations accepted: the 106-line handoff states its cause
  and drops no mandated section. One observation the reviewer records
  rather than hides: commit `68bd9f3f` is +308/-277 = **585 changed
  lines**, over 500 by the churn reading of AGENTS.md Commit
  Discipline though under it by the insertions reading every prior
  verdict in this repository has used. It is a single-file verbatim
  save of the reviewer's own step block and is inseparable by
  construction. Accepted under the insertions reading; the ambiguity
  itself goes to `.agent/candidates.md` as a closure candidate rather
  than spending an R-id (STATUS_closure_protocol.md,
  "Closure-candidate findings").
  LAST_REVIEWED_SHA = `09d7ab2d`.
- R8: in flight — closure part 2. The STATUS `[~]`->`[x]` line and the
  README capability sync land in the SAME commit, last on the branch,
  then the PR — which this session does NOT merge.
<<<END AUTHORED f103-r8-3>>>

<<<BEGIN AUTHORED f103-r8-4
sha256=c4e6084bf42e93bb2098d870532e0cf0820f31f9191b35bf68b1ddc321061533>>>
# Plan — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger. R1-R7 all PASSed; LAST_REVIEWED_SHA
09d7ab2d. Open findings 0; next free ID R-0222. Accepted head for the
package: 65e1eec2. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.

## Goal
F103 is built, gated and packaged: token and cost actuals are queryable,
a real job mirrors its finalized task runs into the per-project SQLite
ledger, and `remedy stats cost` answers per-job, per-role and per-period
questions with every figure naming its basis. What remains is the ledger
edit itself — flipping docs/roadmap/STATUS.md from `[~]` to `[x]` with
the README capability sync in the SAME commit, so no committed state has
the two disagreeing (R-0154), and opening the PR.

## Current Step
R8 — closure part 2: apply the reviewer-authored STATUS `[x]` line and
the three README pairs in ONE commit that also carries the final
`.agent` state, LAST on the branch (Rule A4), touching exactly
docs/roadmap/STATUS.md, README.md and `.agent/**`. Then push and
`gh pr create`. The PR is NOT merged by the session that creates it: it
merges at the next feature's Open PR Gate, which is the operator's
manual-review window.

## Next Steps
- The feature-done banner, and the session ends. The operator may
  review and merge the PR manually at any time.
- Next feature by Rule A5: F104 — Hard budget enforcement. Its first
  reviewed round MUST register or resolve every entry in
  `.agent/candidates.md` and empty the file; a non-empty candidates
  file at claim time is itself a block condition.

## Risks
- The README may claim only what is merged and verified. It is synced
  in the same commit as the STATUS line for exactly that reason, and
  `tests/docs/` is the pin that proves the two agree — the docs-round
  gate must run before the commit stands.
- `.agent/candidates.md` carries TWO entries after this round: R-0221
  and the AGENTS.md commit-size counting ambiguity. Neither is F103's
  to fix and neither may be silently dropped.
- No force-push, no branch deletion, no merge this session.
<<<END AUTHORED f103-r8-4>>>

<<<BEGIN AUTHORED f103-r8-5
sha256=6ecf1e5498428ccdaa0b1df24f18579654e61de32d0813f6f1a886714152ec87>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- R-0221 (Low): `TestAutoBuildBehavior::test_auto_build_runs_by_default` in `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD` and runs a real `npm install` + `npm run build` in whatever checkout it runs in, refreshing `apps/ui/dist` mtimes mid-suite. Costs every integration gate seven phantom base-only failures via the mtime comparison in `_frontend_is_stale()` (`ui_server.py:2748`). · source feature F103 (found at the R5 gate; the code is not F103's) · 2026-08-08
- Commit-size counting is undefined (Low): AGENTS.md Commit Discipline says "If a diff exceeds 500 lines, stop and split before committing" without stating whether the count is INSERTIONS or insertions+deletions. F103 R7's commit `68bd9f3f` is +308/-277 = 585 changed lines — over the cap by the churn reading, under it by the insertions reading. This is not an edge case: every round's `.agent/last_block.md` and `.agent/handoff.md` save is a full-file rewrite, so the churn reading is unmeetable by construction for a verbatim single-file state save, while every verdict in this repository so far has silently used the insertions reading. Fix: state the counting rule in AGENTS.md and say whether a verbatim single-file state rewrite is exempt. · source feature F103 (raised at the R7 closure review; the rule is not F103's) · 2026-08-08
<<<END AUTHORED f103-r8-5>>>

<<<BEGIN AUTHORED f103-r8-6
sha256=53fef3259d02e94472d9e9386350c7e495902f2b3f1b4d251ee2ac270b017cec>>>
## What changed

F103 makes token and cost actuals QUERYABLE. Every finalized task run
lands as a row in a per-project SQLite ledger at
`<data_root>/projects/<uuid>/ledger.sqlite`, and `remedy stats cost`
answers per-job, per-role and per-period questions from it. This is the
first and so far only use of SQLite in Remedy; the module docstring says
so where a reader would search for it.

- **T001** `packages/orchestration/token_ledger.py`: schema version 1 in
  a `meta` row, numbered migrations, WAL, the `calls` table keyed by
  `call_id` with the three covering indexes, and `record_call` — which
  NEVER fails the run: any failure returns False and counts a miss.
- **T002** the call site at the actuals seam plus `backfill_ledger`
  (idempotent by `call_id`) and `verify_ledger`, which compares row
  CONTENT rather than presence and reports field-level `drifted_rows`.
- **T003** `apps/cli/commands/stats_ledger_cmd.py`: `stats cost`,
  `stats backfill-ledger` and `stats verify-ledger` in the existing
  `stats` group, human and `--json`, every figure labelled with its
  basis.
- **R6** arms the mirror at the task-run evidence seam in
  `job_evidence.py`, so a REAL job yields rows with nobody passing a
  `ledger_*` argument by hand.

## Why

The files stay the source of truth; the database is a mirror. A ledger
write may fail without failing the run precisely because every row
restates something a file already says. Actuals capture already existed
file-based — what it could not do is answer a question.

## Key decisions

- **D16 — row granularity.** A row is one FINALIZED TASK RUN, keyed
  `"<job_id>:<task_id>"`, not one HTTP request. No per-request record
  exists on disk, and synthesising one would fabricate ids, timestamps
  and a usage split no file records (the F075 lesson). Remedy
  deliberately does not do that.
- **D17 — closure moved from R6 to R7** so R6 could arm the live
  mirror. Closing before that would have claimed a capability that was
  wired and switched off (finding R-0220).
- **P6 holds in code, not prose.** There is no `COALESCE` in the
  queries, so a sum over all-unmeasured rows stays NULL and never
  renders as a measured zero. Counts use `COUNT`, because 0 is their
  honest empty value. Reads use `mode=rw` + `PRAGMA query_only=1` so a
  read never creates a database nor litters `-wal`/`-shm` sidecars.

## How to review

    python3 -m pytest tests/orchestration/test_token_ledger.py tests/cli/test_stats_cost.py -q   # 115 passed
    python3 -m pytest tests/docs/ -q                                                             # 294 passed
    python3 -m pytest tests/cli/test_golden_path.py -q                                           # 42 passed (canary)
    python3 -m pytest -n auto -q                                                                 # 16131 passed, 19 skipped

Package: `remedy-review-20260808-210612-READY_FOR_REVIEW.zip`,
SHA-256 `8e967d78e57fa97641365b4baa91ca884f6322bc855f678d1daeb146c9dd38ad`,
Evidence job `f103-closure`, accepted HEAD `65e1eec2`.

## Changed files (source, tests and docs; `.agent/**` state omitted)

| Path | What |
|------|------|
| `packages/orchestration/token_ledger.py` | new — schema, writer, backfill, reconcile, cost queries |
| `packages/orchestration/job_evidence.py` | live mirror armed at the task-run evidence seam |
| `packages/orchestration/pingpong_evidence.py` | the ledger hook at the actuals seam |
| `apps/cli/commands/stats_ledger_cmd.py` | new — the three stats commands |
| `apps/cli/command_catalog.py` | registers `stats.cost`, `stats.backfill-ledger`, `stats.verify-ledger` |
| `apps/cli/commands/__init__.py` | wires the new handler module |
| `tests/orchestration/test_token_ledger.py` | new — 82 tests |
| `tests/cli/test_stats_cost.py` | new — 33 tests |
| `tests/cli/test_failure_cmd.py` | declared: exact-contents assertion on the `stats` group weakened to membership |
| `docs/roadmap/features/T2_F103.md` | D16 amendment + Built State |
| `docs/roadmap/STATUS.md` | `[~]` -> `[x]` |
| `README.md` | capability sync, same commit as STATUS (R-0154) |
| `AGENTS.md` | D15 stated-cause handoff-overage clause (own commit, R1) |

## Verdict and findings

Live review **PASS** across R1–R8, every round reviewer-gated with the
reviewer re-running the verification itself. **0 open findings.**
R-0218 (perceptible-slowdown criterion) closed against a measured
**+1.386 ms per finalized task run**, independently reproduced by the
reviewer at +1.395 ms. R-0219 (presence-vs-content reconcile) and
R-0220 (mirror never switched on) closed, both mutation red-proofed in
disposable worktrees. R-0221 (a UI auto-build test that defeats its own
env var) is NOT this feature's code and is carried in
`.agent/candidates.md` as the next feature's claim-time block
condition, together with an AGENTS.md commit-size counting ambiguity
raised at the closure review.

## Runtime actuals (observed)

- Rounds: **8** (R1–R8), all PASS; closure split across R7/R8 because
  the STATUS line quotes values that only exist after the package.
- Models: planner/reviewer and every delegated worker ran on Claude
  Opus 5 (1M context).
- Full suite: **112.64 s** wall clock at the accepted head; scoped
  ledger + stats suites 6.05 s.
- Total feature wall clock: **not-measured** — the build spans several
  sessions and no clock was recorded end to end. A guess would be worse
  than the gap.
- Tokens and cost: **not-measured**. No provider exposed measured usage
  for this build, which the final verifier records as
  `token_measurement_confidence: low`, `actual_call_count: 0`. That is
  precisely the gap this feature closes for every provider that DOES
  report.

## Merge

This PR is deliberately NOT merged by the session that created it. It
merges at the next feature's Open PR Gate — the operator's
manual-review window — or manually by the operator at any time.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
<<<END AUTHORED f103-r8-6>>>
