── STEP closure — F105 R51 (CLOSURE) ─────────────────────────
Goal:        Record the R50 gate, register DECISION D16, then CLOSE F105 —
             the STATUS `[x]` line and the README capability sync in ONE
             final commit, the closure PR created, NOTHING merged.
Bundle:      C1 save block · C2 mirror · C3 the R50 gate entry, the closure
             entry and D16 · C4 the closure commit (STATUS, README,
             candidates, plan, handoff) · C5 push and open the PR.
Change:      .agent/authored/f105-r51-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/decisions.md,
             docs/roadmap/STATUS.md, README.md, .agent/candidates.md,
             .agent/plan.md, .agent/handoff.md. NOTHING else. No production
             code, no test module, no feature file, no docs/ page. The
             review zip is NOT rebuilt — see C3's closure entry for why.
Constraints: No merge of ANY pull request, #189 above all: it is open from a
             non-`feature/*` branch, so the AGENTS.md Open PR Gate is
             stop-and-report and only the operator resolves it. Do not
             comment on it, do not modify it. No `main`, no force-push, no
             branch deletion. The C4 closure commit is the LAST commit on
             the branch. Touch no STATUS line but F105's.
Done when:   STATUS carries the authored `[x] F105` line byte for byte,
             README agrees with the ledger, the PR exists and is UNMERGED,
             and every gate below has a real exit code.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1 — write this ENTIRE block to `.agent/authored/f105-r51-1.md` byte for
  byte, commit it ALONE.

C2 — `cp` it over `.agent/last_block.md`, commit alone, `cmp` silent.

C3 — .agent/live_review.md and .agent/decisions.md, ONE commit.

  PAIR_GATE targets `.agent/live_review.md` and is APPEND-shaped: the TO
  CONTAINS the FROM verbatim as its first line. Do not run a whole-file
  "FROM 0x" proof on it — that is unattainable by construction here. The
  obligation is FROM exactly 1x in the file after the edit, plus each
  TO-ONLY added line exactly 1x AMONG THE LINES THIS COMMIT'S OWN DIFF ADDS.

<<<PAIR_GATE_FROM>>>
  resolve it. F105 stays `[~]`.
<<<END_PAIR_GATE_FROM>>>

<<<PAIR_GATE_TO>>>
  resolve it. F105 stays `[~]`.
- Reviewer gate on R50 (2026-08-12): PASS. Range `5786967b..470fb776` = five
  commits touching exactly the five `.agent/` paths the block named — no
  production code, no test module, no docs, no STATUS.md, no README.md.
  Insertions per commit 202, 181, 93, 170 and 1, each far under 500.
  Transport by the PRIMARY shape, because the reviewer's original survived on
  disk: `.remedy-wt/f105-r50-1.block.md`, the committed
  `.agent/authored/f105-r50-1.md` and `.agent/last_block.md` all three hash to
  `8686cf90d6a60f52b4665d7024f944496930257a295e33355b752f1437b642fd`
  at 202 lines, and both `cmp` runs are silent.
  PAIR_DONE measured as a REWRITE rather than asserted: the TO does not
  contain the FROM, the `Landed:` line reads 1x before and 0x after, and
  every TO-only line occurs exactly 1x among the 93 lines the C3 diff adds.
  Stray reconcile over that same commit: 93 added, 1 removed, 0 stray.
  Every scoped gate was RE-RUN by the reviewer instead of read from the
  handback: `python3 -m pytest tests/docs/ -q` returns 294 passed, the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c '^<<<'` is 0 in all three state files, `## Steps` is exactly 1,
  `git status --porcelain` is empty and `git worktree list` shows the primary
  checkout alone.
  The closure artifacts were checked as artifacts, never as claims. The
  package `remedy-review-20260812-092055-READY_FOR_REVIEW.zip` hashes to the
  recorded `23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840`,
  `zipfile.testzip()` returns None over its 3646 members, its manifest reads
  `package_status: READY_FOR_REVIEW` with `committed_review_subject`
  cfda4245..b928a0c6 and `source_root_containment: PASS`, and neither the zip
  nor the evidence directory is tracked — the zip is ignored at
  `.gitignore` line 223.
  Both declared deviations are ACCEPTED. C6's two attempts are the honest
  record of a producer pitfall found and repaired at authoring time with the
  production scrubber, on the same producer; C7b is the self-reference limit
  this branch has already accepted twice, since a gate row counting
  insertions per commit cannot count the commit that writes it.
  `LAST_REVIEWED_SHA` advances 5786967b -> 470fb776.
- R51 CLOSURE (2026-08-12): F105 closes as PASS_WITH_RISKS — ACCEPTED.
  The five closure preconditions were re-verified by the reviewer at HEAD
  470fb776, not carried forward from an earlier round. Every step has a PASS
  round and the seven open findings are exactly the documented Low/Medium
  residual set recorded above. The full suite, run by the reviewer itself,
  returns `16462 passed, 19 skipped in 132.94s` at exit 0 with zero failures.
  `python3 -m apps.cli.grouped integrity check --json` returns
  `"passed": true` with 5 of 5 checks passing, `relevant_untracked` at 0 and
  `high_blockers_open` clean. The feature file's Built State already
  describes T001-T004 as built. The tree is clean and HEAD equals
  `origin/feature/f105-cache-optimal-prompt-ordering`.
  The review zip is deliberately NOT rebuilt for this round. Every commit
  between the accepted HEAD b928a0c6 and the closure commit changes `.agent/`
  state only, and the closure commit's own STATUS and README edits follow the
  READY zip by construction, exactly as the protocol's build order requires.
  This is the F104 R9 shape, ratified there in the same words.
  This is the LAST round of the branch, so by construction it records no gate
  on itself (planner_reviewer_prompt.md §4.13). Its verdict lives in
  `.agent/handoff.md`, the completion report and the pull request, and that
  absence is the terminator rather than a missing gate.
  One closure CANDIDATE was raised and spends no R-id: the review zip
  packages the gitignored `.remedy-wt/` scratch tree. It is written to
  `.agent/candidates.md` under the disk-vehicle rule, so the next feature's
  first reviewed round registers or resolves it. The next free finding ID
  stays R-0270.
<<<END_PAIR_GATE_TO>>>

  PAIR_DEC targets `.agent/decisions.md` and is APPEND-shaped in the same
  way: the TO contains the FROM as its first line. The FROM is the CURRENT
  LAST NON-EMPTY LINE of `.agent/decisions.md`. Read that file's tail first,
  confirm the FROM matches it exactly, and if it does NOT match, STOP, do not
  guess, and report the real last line in the handback. If the file ends
  with a trailing blank line, append after it and keep the file's existing
  final-newline convention.

<<<PAIR_DEC_TO_APPEND>>>

## DECISION F105 D16 (2026-08-12) — the Open PR Gate does not block a
## closure PR

Chosen: PR #189 (`docs/amend0810-clerical` -> `main`) is stop-and-report and
stays untouched — not merged, not commented on, not modified — because it
does not originate from a `feature/*` branch. It does NOT block creating the
F105 closure pull request. The AGENTS.md Open PR Gate fires "before creating
a new feature branch or starting a new unrelated task"; closing F105 is
neither, it is the completion of the branch already in hand. The closure
protocol already leaves the closure PR unmerged until the next feature's
start, where the gate will see both PRs and correctly stop-and-report.

Alternatives considered. (a) Wait for the operator before closing: rejected —
from 2026-08-13 the operator reaches this machine only over SSH from a phone
(docs/agents/self_drive_protocol.md), so a finished feature would stall
indefinitely on an action the operator must take for #189 either way, and
every later session would re-derive F105's state from scratch. (b) Merge #189
to clear the gate: FORBIDDEN — a non-`feature/*` PR is stop-and-report and
merging it is outside any agent's authority here.

Reverse this decision by closing the F105 pull request; the branch and every
commit on it survive untouched.

Operator note, not a blocker: PR #189 and this branch both modify
`docs/agents/reviewer_conventions.md`, so whichever merges second may need a
conflict resolution.
<<<END_PAIR_DEC_TO_APPEND>>>

C4 — the CLOSURE COMMIT. ONE commit, and it is the LAST commit on the
  branch. It touches exactly: `docs/roadmap/STATUS.md`, `README.md`,
  `.agent/candidates.md`, `.agent/plan.md`, `.agent/handoff.md`.

  PAIR_STATUS targets `docs/roadmap/STATUS.md` and is a REWRITE. Replace the
  single line; touch no other line in the file.

<<<PAIR_STATUS_FROM>>>
- [~] F105 — Cache-optimal prompt ordering
<<<END_PAIR_STATUS_FROM>>>

<<<PAIR_STATUS_TO>>>
- [x] F105 — Cache-optimal prompt ordering (T001–T004 complete; accepted 2026-08-12 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f105-closure · package remedy-review-20260812-092055-READY_FOR_REVIEW.zip · SHA-256 23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840 · accepted HEAD b928a0c691dc0a2b86c149a5e732ea07ac03176e)
<<<END_PAIR_STATUS_TO>>>

  PAIR_RM_COUNT targets `README.md` and is a REWRITE of one line.

<<<PAIR_RM_COUNT_FROM>>>
41 of 255 registered items accepted. Next: F105 (Cache-optimal prompt ordering).
<<<END_PAIR_RM_COUNT_FROM>>>

<<<PAIR_RM_COUNT_TO>>>
42 of 255 registered items accepted. Next: F107 (Context compiler v2).
<<<END_PAIR_RM_COUNT_TO>>>

  PAIR_RM_TIER targets `README.md` and is a REWRITE of one table row.

<<<PAIR_RM_TIER_FROM>>>
| 2 | Minimal Self-Build Runtime | 3 | 14 |
<<<END_PAIR_RM_TIER_FROM>>>

<<<PAIR_RM_TIER_TO>>>
| 2 | Minimal Self-Build Runtime | 4 | 14 |
<<<END_PAIR_RM_TIER_TO>>>

  PAIR_RM_LIST targets `README.md` and is a REWRITE of two lines into three.
  It adds F104 alongside F105. That is NOT scope creep and NOT a silent
  correction: F104 is `[x]` in the ledger and on `main`, the Tier-2 table row
  already counts it as done, and only this prose list omitted it. The
  cross-check pin only verifies that README-listed features ARE accepted, so
  the omission stayed green. Since this commit exists precisely to stop
  README and STATUS disagreeing (R-0154), leaving a known-wrong list while
  editing that very list would be dishonest. Declare it in the handback and
  the PR description.

<<<PAIR_RM_LIST_FROM>>>
F254 model alias table & dead-model doctor check,
F103 token ledger (SQLite).
<<<END_PAIR_RM_LIST_FROM>>>

<<<PAIR_RM_LIST_TO>>>
F254 model alias table & dead-model doctor check,
F103 token ledger (SQLite), F104 hard budget enforcement,
F105 cache-optimal prompt ordering.
<<<END_PAIR_RM_LIST_TO>>>

  CANDIDATES — replace `.agent/candidates.md` ENTIRELY with this text.

<<<CANDIDATES_FULL>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- The review zip packages the gitignored scratch tree `.remedy-wt/` · source
  feature: F105 · date: 2026-08-12 — measured by the reviewer at the R50 gate
  against `remedy-review-20260812-092055-READY_FOR_REVIEW.zip`: 1091 of its
  3646 members come from `.remedy-wt/`. `scripts/make_review_zip.sh` prunes
  `.git`, `.data`, caches and ROOT-LEVEL `remedy-job-evidence-*` directories,
  but it sweeps the working tree with `find` and never consults `.gitignore`.
  Three measured consequences. (1) A PRIOR feature's complete evidence bundle
  ships inside the package — 114 members under
  `.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure/` —
  which is exactly what the root-level exclusion exists to prevent; nesting
  one level deeper evades it. (2) The current bundle is packaged twice: 339
  authoritative members under `evidence/current/` plus 334 raw copies under
  `.remedy-wt/f105_closure_evidence/`. (3) 244 packaged scratch members
  contain the literal local path `/home/decodeux`, while the manifest reports
  `external_paths_detected: []` — the local-path scanner reads evidence
  fields, not packaged tree members, so the same class of leak that packaged
  the FIRST R50 zip attempt as BLOCKED_EVIDENCE rides undetected in the
  second. The package itself remains valid and authoritative:
  `package_status` is READY_FOR_REVIEW, `packaged_evidence_job_id` is
  `f105-closure`, and `review_subject_evidence_alignment` is PASS — which is
  why this is a candidate and not a closure blocker. It is neither F105's
  code nor F105's scope: `.remedy-wt/` exists only because self-drive scratch
  cannot be written to `/tmp` on this machine, so the fix belongs to
  `scripts/make_review_zip.sh` and docs/agents/self_drive_protocol.md
  together.
<<<END_CANDIDATES_FULL>>>

  PLAN — rewrite `.agent/plan.md` completely, UNDER 50 lines, keeping a
  `## Goal` heading and a `## Next Steps` heading (the `.agent` contract
  tests assert both). Compose the text yourself; it must state, accurately:
  F105 is CLOSED, `[x]` in STATUS.md, accepted 2026-08-12 as PASS_WITH_RISKS;
  the accepted HEAD b928a0c6, the package name and its SHA-256, evidence job
  `f105-closure`; that the reviewer re-ran the full suite itself
  (16462 passed, 19 skipped, 0 failed) and the integrity check (5 of 5);
  T001-T004 all done; seven residual Low/Medium risks open (R-0221, R-0239,
  R-0247, R-0262, R-0268 Low; R-0265, R-0266 Medium) and next free ID R-0270;
  one closure candidate in `.agent/candidates.md`; DECISION D16. Next Steps:
  the closure PR is UNMERGED by design and merges at the next feature's start
  via the Open PR Gate, the operator may merge manually at any time, the
  operator still owns PR #189, and the next feature by Rule A5 is F107.

  HANDOFF — rewrite `.agent/handoff.md` completely. Target under 60 lines; if
  the MANDATED content genuinely does not fit, go over and carry a
  "Deviations, declared (DECISION D15)" line naming the real line count and
  the specific mandated content that caused it. Never drop a section to meet
  the cap. It must carry: feature and round; branch; this round's commit
  SHAs; a changed-files table; an item-status table covering C1 through C5
  with `done` / `skipped` / `deviated` and a reason for anything not `done`;
  the gate table below with REAL exit codes, never the word "green"; the open
  findings count (7) and the next free ID (R-0270); the closure values
  (accepted HEAD, evidence job, package name, SHA-256); the PR number and the
  fact that it is UNMERGED; the statement that PR #189 was not touched; and
  the next expected action.

C5 — push and open the PR. `git push`, then `gh pr create` with this title
  and this body, byte for byte.

<<<PR_TITLE>>>
F105 — Cache-optimal prompt ordering (closure)
<<<END_PR_TITLE>>>

<<<PR_BODY>>>
## What changed

Every prompt in Remedy now composes from REGISTERED SEGMENTS ordered by
stability — system and conventions first, task and steering last — instead of
from hand-written string concatenation. Prompt CONTENT is unchanged; only the
ordering and the bookkeeping are new.

- **T001 — the registry.** `packages/orchestration/prompt_segments.py`:
  `PromptSegmentRegistry` collects named segments and rejects duplicates,
  `SegmentStabilityRank` is the documented 0-5 scale, and
  `compose_prompt_segments` sorts by `(rank, registration index)` so
  composition is deterministic rather than dependent on iteration order. It
  returns a `ComposedPrompt(text, manifest)` whose rows carry name, rank,
  sha256, chars and estimated tokens.
- **T002 — the conventions loaders.** `role_conventions.py` loads
  `docs/agents/worker_conventions.md` and `docs/agents/reviewer_conventions.md`
  VERBATIM and registers each as the `CONVENTIONS`-ranked segment. Remedy
  deliberately provides no writer for either document: those rules change
  through a reviewed diff of the documents themselves.
- **T003 — six builders migrated**, each in its own commit under its own
  content-equality golden: intake, flight plan, mission, orchestrator (prompt
  and system prompt), builder and reviewer.
- **T004 — the measurement.** `remedy stats cache` is a read-only view over
  ledger rows that already exist, with a `--json` mode. It renders
  `unmeasured` when nobody reported the inputs and `undefined` when they were
  reported as zero — never a `0` standing in for either.

## Why

Cache-optimal ordering is only worth anything if it is provable. The manifest
reaches evidence through `PromptTraceEntry.segment_manifest`, derived from the
composed prompt at ONE seam, so a manifest can never describe a different
prompt than the one that was sent.

## Key decisions

- **D1** — segments join with a plain blank line and nothing else.
- **D16** — the AGENTS.md Open PR Gate fires before a NEW branch or a new
  task, so open PR #189 (`docs/amend0810-clerical`, not a `feature/*` branch,
  therefore stop-and-report) does not block this closure PR. #189 was not
  merged, commented on or modified.
- The README capability sync also adds **F104**, which was accepted and on
  `main` but missing from the Tier-2 prose list while the Tier-2 table row
  already counted it. Declared, not silent.

## How to review

- `python3 -m pytest -n auto -q` — full suite.
- `python3 -m pytest tests/orchestration/test_prompt_segments.py tests/orchestration/test_role_conventions.py tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_prompt_trace.py -q`
- The six prompt goldens under `tests/orchestration/`.
- `docs/system/cache-optimal-prompt-ordering-v1.md` carries the measured
  before/after cacheable-prefix table and the command that reproduces it.

## Verdict and evidence

Latest live review: **PASS_WITH_RISKS — ACCEPTED** (R50 gated PASS; R51 is the
closing round and by construction records no gate on itself).

The reviewer re-ran verification itself rather than reading the handback:
full suite `16462 passed, 19 skipped in 132.94s`, exit 0, zero failures;
`integrity check --json` `"passed": true`, 5 of 5 checks.

- Evidence job `f105-closure`
- Package `remedy-review-20260812-092055-READY_FOR_REVIEW.zip`
- SHA-256 `23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840`
- Accepted HEAD `b928a0c691dc0a2b86c149a5e732ea07ac03176e`

## Open findings: 7

All Low or Medium, all documented, none inside F105's change set, no High
open: R-0221, R-0239, R-0247, R-0262, R-0268 (Low); R-0265, R-0266 (Medium).
One closure candidate is recorded in `.agent/candidates.md`: the review zip
packages the gitignored `.remedy-wt/` scratch tree (1091 of 3646 members),
which the next feature's first reviewed round must register or resolve.

## Changed files

104 files across 278 commits, 2026-08-09 to 2026-08-12. 35 of them are
outside `.agent/`:

| Area | Files |
|---|---|
| production | `packages/orchestration/` prompt_segments, role_conventions, prompt_trace, intake, flight_plan, mission_compiler, orchestrator_loop, pingpong_loop, gauntlet_runner; `apps/cli/` command_catalog, do_cmd, mission_cmd, stats_ledger_cmd |
| tests | 15 modules under `tests/orchestration/` and `tests/cli/` |
| docs | `docs/system/cache-optimal-prompt-ordering-v1.md`, `docs/README.md`, `docs/agents/planner_reviewer_prompt.md`, `docs/agents/worker_conventions.md`, `docs/agents/reviewer_conventions.md`, `docs/roadmap/features/T2_F105.md`, `docs/roadmap/STATUS.md`, `README.md` |

## Runtime actuals

51 rounds over 4 days (2026-08-09 to 2026-08-12), 278 commits. Models and
token/cost figures: `not-measured` — the ledger's `role` column is a
hardcoded `builder` in production data (open finding R-0266), so no honest
per-role split of this branch's own spend exists.

## Merge

Do NOT merge as part of this session. Per the closure protocol this PR merges
at the next feature's start via the Open PR Gate; that gap is the operator's
manual-review window. The operator may merge manually at any time. Note that
PR #189 also modifies `docs/agents/reviewer_conventions.md`, so whichever of
the two merges second may need a conflict resolution.
<<<END_PR_BODY>>>

  Do NOT merge the PR. Do NOT approve it. Record its number.

Gates — run every one, record REAL exit codes, never the word "green"
  A  Transport, one-session shape. `wc -l` and `sha256sum`
     `.agent/authored/f105-r51-1.md`, and `cmp` it against
     `.agent/last_block.md` — silent. State plainly in the handback that no
     reviewer scratchpad original exists in a one-session self-drive build,
     because the reviewer writes nothing, so this gate proves C1 == C2 and
     the reviewer's own read of the committed file is the transport proof.
  B  `wc -l .agent/authored/f105-r51-1.md` against the cap of 400.
  C  PAIR_GATE and PAIR_DEC are APPEND-shaped. For each: prove the TO
     CONTAINS the FROM verbatim, the FROM occurs exactly 1x in the target
     file after the edit, and each TO-ONLY added line occurs exactly 1x
     AMONG THE LINES THAT COMMIT'S OWN DIFF ADDS.
  D  Stray reconcile for C3, per file: every ADDED line appears in
     `.agent/authored/f105-r51-1.md`. Report added, removed and stray counts.
  E  `grep -c '^<<<'` over `.agent/live_review.md`, `.agent/decisions.md`,
     `.agent/candidates.md`, `.agent/plan.md`, `.agent/handoff.md`,
     `docs/roadmap/STATUS.md` and `README.md` — all 0. `grep -c` exits 1 when
     the pattern is absent and absence IS the pass condition; record the
     counts, not the exit code alone.
  F  `grep -c '^## Steps' .agent/live_review.md` — exactly 1. This round adds
     no new `##` heading to that file.
  G  STATUS: `grep -c '^- \[x\] F105 — ' docs/roadmap/STATUS.md` is 1,
     `grep -c '^- \[~\]' docs/roadmap/STATUS.md` is 0, and
     `git diff --numstat` for STATUS.md in the C4 commit is exactly
     `1	1`. Then prove the applied line is byte-identical to PAIR_STATUS_TO
     by `grep -c -F` on the authored file's own copy of it.
  H  README: each of the three FROM texts occurs 0x after the edit and each
     of the three TO texts occurs 1x. Then
     `python3 -m pytest tests/docs/ -q` — this round changes README.md and
     docs/roadmap/**, so the docs gate is mandatory alongside the canary.
  I  Canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J  `git status --porcelain` empty, `git worktree list` shows the primary
     checkout ALONE, and `git rev-parse HEAD` equals
     `git rev-parse origin/feature/f105-cache-optimal-prompt-ordering`
     after the push.
  K  Insertions per commit under 500. `git diff --name-only 470fb776..HEAD`
     is exactly the eight paths this block names — no production code, no
     tests, no feature file, no other docs page.
  L  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     shows PR #189 still open and untouched PLUS the new closure PR. Nothing
     was merged. Record the raw JSON.

If any gate comes back red, or anything in this block contradicts what you
find on disk: STOP, do not guess, do not widen scope to route around it,
commit whatever valid portion already stands, and say so plainly in the
handback with the raw error. A round that stops honestly is a success.
