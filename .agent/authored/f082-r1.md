── STEP R1/7 — F082 Self-benchmark (claim and sweep) ─────────────────
Goal:        Claim F082, reset the live-review record carrying the F077 open
             set forward, and register the review-zip packaging finding that
             had no disk vehicle on the F077 branch.
Bundle:      A0 gate confirmation · A1 branch · C0 save this block · C1 the
             record reset, findings persisted FIRST · C2 the claim, plan,
             context and candidates · C3 handback.
Change:      docs/roadmap/STATUS.md (exactly one line), .agent/live_review.md,
             .agent/plan.md, .agent/context.md, .agent/candidates.md,
             .agent/authored/f082-r1.md, .agent/last_block.md,
             .agent/handoff.md. NOTHING under packages/, apps/ or tests/.
             No new file outside .agent/authored/.
Constraints: Findings persist FIRST, in their own commit, before anything else
             (planner_reviewer_prompt.md §4 item 4). Never write a `Done:` or
             `Landed:` paragraph of your own. Every authored slice is applied
             disk-to-disk out of the COMMITTED block file, never retyped.
             Push after every commit. Never merge, never force-push, never
             work on main.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── A0 — Open PR Gate: ALREADY EXECUTED, confirm only ─────────────────
The planner ran the Open PR Gate at this session's Phase 1 and merged PR #200
(feature/f077-autonomy-watchdog → main) before authoring this block. Do NOT
merge anything. Confirm and record the raw output of:
  gh pr list --state open --json number,headRefName,baseRefName,isDraft
EXPECT `[]`. Also record `git rev-parse main`; EXPECT
668d40f7ca691ba25e5293157651ddca853bbd4f, the merge commit of PR #200.
If either differs — any open PR at all, a different main head — STOP, write
the handoff and hand back. Do not create the branch.

── A1 — the branch ───────────────────────────────────────────────────
  git checkout -b feature/f082-self-benchmark
Record `git merge-base main HEAD`.

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original of this block is on disk at
`.remedy-wt/f082-r1-scratchpad.md`. Do not retype either target file.

This block is well over 250 lines, so saving it to both targets in ONE commit
would insert roughly twice that and break the 500-insertion cap by
construction (AGENTS.md Commit Discipline; findings R-0381 and R-0399).
Split it:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r1.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R1 claim-and-sweep block verbatim`

C0b. Copy the COMMITTED `.agent/authored/f082-r1.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE; it is
     the verbatim rewrite of a single `.agent/**` state file and is exempt
     from the churn reading under DECISION F104 D1.
     Subject: `chore(f082): mirror the R1 block into last_block`

── C1 — the record reset, findings FIRST ─────────────────────────────
File: `.agent/live_review.md`. FULL REPLACEMENT, built mechanically:

  part 1 = the LIVE-REVIEW-HEAD slice below, extracted from the COMMITTED
           `.agent/authored/f082-r1.md` between its own markers;
  part 2 = the THIRTY-TWO findings still open in the F077 record, carried
           VERBATIM, extracted by id from the PRE-RESET `.agent/live_review.md`
           and never retyped.

The carried ids, in this order:
R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374,
R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0385,
R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395, R-0396,
R-0397, R-0399, R-0400, R-0401, R-0402.

A carried finding is the whole paragraph that begins `- R-XXXX — ` up to (not
including) the next blank line. Join part 1 and part 2 so that exactly one
blank line separates each carried paragraph from the next. Write the extractor
as a script in `.remedy-wt/`; do not hand-edit the paragraphs.

Why the carry: DECISION F057 D1 in `.agent/decisions.md` and finding R-0362 —
a reset that drops open findings makes Rule A2 unenforceable by erasing its
input. The BEGIN/END marker lines themselves never reach the target file.

--- BEGIN SLICE LIVE-REVIEW-HEAD ---
# Live Review — F082 Self-benchmark

> Round-by-round review record for the F082 branch, reset at the feature claim.
> The F077 record closed with PR #200, merged 2026-08-14; that branch's closing
> verdict lives in its handoff and in the PR, per
> docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids continue the
> monotonic R-XXXX series across the reset. Next free id: R-0404.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The thirty-two findings
> open when the F077 record closed are reproduced verbatim at the end of this
> file, extracted by id out of the previous record and never retyped.

## Steps
R1 claim F082, reset this record carrying the F077 open set forward, and
register the review-zip packaging finding R-0403 → R2 the T001 inventory: what
the gauntlet harness already provides, which pieces the bench must reuse rather
than copy, and where the record schema and the history file belong, each
answered with a file-and-symbol citation → R3 T001 the factoring plus the five
frozen orders and the record schema → R4 T002 history append, trend computation
and the regression rules with improving, flat and degrading goldens → R5 T003
the CLI, model-context recording and a fake-provider bench run end to end →
R6 the integration gate → R7 closure.

## Findings

- R-0403 — Low — every review package carries the gitignored `.remedy-wt/` tree as file content, so more than half of each archive is scratch that the review subject itself excludes. Measured today from the two packages on disk: `remedy-review-20260814-085403-READY_FOR_REVIEW.zip` holds 2811 of 5373 entries under `.remedy-wt/` and F077's closure package `remedy-review-20260814-161744-READY_FOR_REVIEW.zip` holds 3096 of 5746 — 52.3% and 53.9%. Cause, read from the script rather than inferred: the file-collection `find` in `scripts/make_review_zip.sh` prunes an EXPLICIT directory list (`./.git`, `./.data`, `./.agent/Evidence`, `node_modules`, `dist`, `build`, the cache directories, plus the dynamically appended `remedy-job-evidence-*` entries) and `./.remedy-wt` is not among them — so being gitignored is NOT the criterion, `./.data` is excluded by being named, and `.remedy-wt/` is collected as ordinary repo files. That directory is Remedy's own job-worktree root by design (`docs/roadmap/features/T0_F006.md`, `git worktree add .remedy-wt/<job>`), it is gitignored at init by F081's `_ensure_ignore_entry` (`.gitignore:235`), and because `/tmp` writes are denied to this session class it is also where every round's gate and transport scratch lands — 731 entries at its top level as this finding is written. Nothing here is INVALID: both packages validated READY_FOR_REVIEW, and `committed_review_subject` is a git range, so gitignored files never enter the review subject and no reviewed byte is affected. The cost is that the operator's only remote window into a run is roughly twice the size it needs to be, over a link that since 2026-08-13 is a phone. The fix is one `-path './.remedy-wt' -o` line in that prune list, which edits `scripts/make_review_zip.sh` — a file F082 does not own, and AGENTS.md forbids mixing an unrelated fix into a feature branch — so it routes to a paydown branch exactly as R-0380 and R-0381 were routed. Registered here rather than through `.agent/candidates.md` because it was raised during F077's closure review, AFTER the closure commit had already written that carrier empty, and Rule A4 forbids a commit after the closure commit: the empty carrier at this claim is therefore not evidence that nothing was raised. OPEN.
--- END SLICE LIVE-REVIEW-HEAD ---

Commit C1 ALONE. Subject: `docs(f082): reset the live review record and register R-0403`

── C2 — the claim, plan, context, candidates ─────────────────────────
All four in ONE commit.
  Subject: `docs(f082): claim F082 and refresh the candidates carrier`

C2a. `docs/roadmap/STATUS.md`. REWRITE pair — FROM and TO are disjoint. The
FROM must match exactly once before the edit and zero times after; the TO
exactly once after.

>>> STATUS-FROM >>>
- [ ] F082 — Self-benchmark
<<< STATUS-FROM <<<

>>> STATUS-TO >>>
- [~] F082 — Self-benchmark
<<< STATUS-TO <<<

Touch no other STATUS line. README.md is NOT edited this round: its capability
counts change at closure, not at the claim.

C2b. `.agent/candidates.md`. FULL REPLACEMENT with the CANDIDATES slice.

--- BEGIN SLICE CANDIDATES ---
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(empty — the one candidate raised during F077's closure review, the review-zip
packaging of `.remedy-wt/`, had no disk vehicle on that branch because it was
raised after the closure commit, and is registered as finding R-0403 in
`.agent/live_review.md` on the F082 branch, 2026-08-14.)
--- END SLICE CANDIDATES ---

C2c. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0404. Open findings: thirty-three — the thirty-two carried from F077 plus
R-0403 registered this round. `.agent/live_review.md` is the source of truth for
that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R1 is done: F082 claimed, this record reset carrying the F077 open set forward,
R-0403 registered.

## Next Steps
1. R2 — the T001 inventory, read-only, no production edit: what the six
   gauntlet modules under `packages/orchestration/` and
   `scripts/self_run_gauntlet.py` already provide, which pieces the bench
   reuses versus copies, and where the record schema and the history file
   belong under the data root. Every answer carries a file-and-symbol
   citation, into `.agent/f082_inventory.md`.
2. R3 — T001 the factoring, the five frozen orders, the record schema and a
   dry run against recorded fixture evidence.
3. R4 — T002 history append, trend computation, regression rules and goldens.
4. R5 — T003 CLI, model-context recording and a fake-provider bench run.

## Risks
- The factoring in T001 is the feature file's own named risk: the gauntlet's
  seven test files must stay green UNMODIFIED, so R2 establishes what may move
  before anything moves.
- Thirty-three open findings is the largest carry any feature has started with.
--- END SLICE PLAN ---

C2d. `.agent/context.md`. FULL REPLACEMENT with the CONTEXT slice.

--- BEGIN SLICE CONTEXT ---
# Context — F082 Self-benchmark

## Active Branch
feature/f082-self-benchmark, cut from main after PR #200 merged. F082 is
claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: the capability bench built on the gauntlet harness — a runner module under
`packages/orchestration/`, the five frozen order files, the per-run record
schema, the append-only history under the data root, and the `stats bench` CLI
surface; plus `.agent/f082_inventory.md`, the read-only T001 inventory,
`.agent/**` round state and the one claimed STATUS line. The exact file set is
NOT fixed until R2 has inventoried the harness: the feature file requires
inspecting the current shape before building, and its orchestrator brief names
the T001 factoring as the risky part.

Out: the gauntlet's pass definition, routing decisions — this feature only
RECORDS model context — and visual judgment, which is the F082 feature file's
Do-not-touch list. The gauntlet's own seven test files stay green UNMODIFIED;
a change that needs one of them edited is a finding, not a fix.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F082 owns.
- The reviewer measures its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5), with 240 the
  preferred target so the block-save commit stays inside the 500-insertion
  limit (R-0381).
- The bench never runs implicitly — on demand only, an F082 acceptance rule.

## Steps
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory → R3 T001 factoring, the five
orders and the record schema → R4 T002 history, trend and regression rules → R5
T003 CLI, model context and a fake-provider run → R6 the integration gate → R7
closure.
--- END SLICE CONTEXT ---

── C3 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, commit SHAs, per-commit changed-files table, the real
verification results below, open-findings count, next expected action. Under 60
lines, or carry a DECISION D15 stated-cause line naming the real count and the
mandated content that caused it. Commit and push.
  Subject: `chore(f082): handback R1`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line.
2.  `cmp` the scratchpad original against `.agent/authored/f082-r1.md`, and
    that file against `.agent/last_block.md` → both exit 0. Report the shared
    sha256 and the line count; it must be at or under 400. The planner
    measured it mechanically at emission and it passed; report the real
    number, whatever it is.
3.  A0's `gh pr list` output verbatim → `[]`. Report `git rev-parse main`.
4.  `git branch --show-current` → feature/f082-self-benchmark. Report
    `git merge-base main HEAD`.
5.  `grep -c "^- \[ \] F082 — Self-benchmark" docs/roadmap/STATUS.md` → 0.
    `grep -c "^- \[~\] F082 — Self-benchmark" docs/roadmap/STATUS.md` → 1.
    `grep -c "^- \[~\]" docs/roadmap/STATUS.md` → 1.
6.  Carry proof: compute one sha256 over the thirty-two carried paragraphs
    joined in the listed order, ONCE from the pre-reset record
    (`git show <pre-C1 SHA>:.agent/live_review.md`) and ONCE from the new
    `.agent/live_review.md`. The two hex digests must be EQUAL. Report the hex
    and the byte length. Do not report a `cmp` exit code for this — report the
    digests (R-0361).
7.  Open set recomputed mechanically from the new record — every
    `^- R-[0-9]\+ — ` paragraph minus every `^Done: R-[0-9]\+ — ` line. Expect
    exactly THIRTY-THREE; name every id. Report duplicates as none or name
    them. Report the max id and the next free id.
8.  `grep -c "^- " .agent/candidates.md` → 0.
    `grep -c "R-0403" .agent/candidates.md` → 1.
9.  `wc -l .agent/plan.md` → report it; must be under 50.
10. `python3 -m pytest tests/docs/ -q` → exit 0. The planner measured
    295 passed at main 668d40f7 today; report the real number, whatever it is.
11. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Planner baseline at
    that same commit today: 142 passed. Report the real number.
12. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0.
    Planner baseline today: 42 passed.
13. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open`
    message. The `remedy` entry point is denied to this session class, so the
    module form above is the one to run.
14. `git diff --stat <merge-base>..HEAD -- packages/ apps/ tests/` → EMPTY.
15. Report each commit's `git show --numstat <sha>` insertion total. If any
    commit exceeds 500 insertions, declare it in the handback with the reason
    (AGENTS.md Commit Discipline) — do not silently pass it.

Transport proof: state, for each of LIVE-REVIEW-HEAD, CANDIDATES, PLAN,
CONTEXT, STATUS-FROM and STATUS-TO, that it was extracted from the COMMITTED
`.agent/authored/f082-r1.md` and applied disk-to-disk, with the slice's sha256
and byte length, and the proof that the applied region equals it. Confirm that
no BEGIN/END marker line and no `>>>` pair line reached any target file. Scan
every file you touched for trailing whitespace and report the result.
