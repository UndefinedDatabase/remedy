# Live Review — F111 Diff-only repair

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f111-diff-only-repair. Next free ID: R-0298.

## Findings

Twenty-two findings carry forward from F107, all OPEN, none above Medium,
each accepted as a risk at the F107 closure. Every entry below is compacted
to its substance; the full text of all of them lives in
`.agent/live_review.md` at commit 3c017c4e, merged to main as 4e0b762e,
which is the archive of record.

- R-0221 (Low, from F103 via F104 and F105):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` runs a real `npm install` and
  `npm run build` mid-suite, refreshing `apps/ui/dist` mtimes and costing
  every integration gate phantom base-only failures through
  `_frontend_is_stale()`. Routed to the F252 flake class. OPEN.
- R-0239 (Low, from F105): a reviewer-authored gate citation named a path
  that does not exist. The worker ran the real path and declared the
  correction, so nothing was skipped; kept as the citation-accuracy record.
  OPEN.
- R-0247 (Low, from F105): a reviewer-authored finding cited a line count of
  101 where the file was 100. Same class as R-0239. OPEN.
- R-0262 (Low, from F105): `plan_job_llm` composes its prompt OUTSIDE the
  `try` that turns a provider failure into a renderable result, so a raising
  composer escapes the function. OPEN.
- R-0265 (Medium, from F105): a provider that reports usage but no cache
  field leaves a measured-looking `0` the token ledger cannot distinguish
  from a real zero. The fix belongs to the actuals producer. OPEN.
- R-0266 (Medium, from F105): the token ledger's `role` is a hardcoded
  `builder` in production data, so a per-role split of production rows is one
  bucket. Producer change. OPEN.
- R-0268 (Low, from F105): a `.agent/STOP` file carries no provenance —
  nothing distinguishes an operator stop from any other writer. Belongs to
  the self-drive protocol. OPEN.
- R-0270 (Medium, F107 R1): `scripts/make_review_zip.sh` sweeps the work tree
  with `find` and never consults `.gitignore`, so the review zip packages the
  gitignored scratch tree `.remedy-wt/` — 1091 of 3646 members at one
  measured build, a prior feature's whole evidence bundle included. OPEN.
- R-0272 (Low, F107 R5): a reviewer-authored contract named an
  `ImportNeighbors.files` field that does not exist — the real neighbour
  tuple is `resolved`. The worker implemented the correct one. OPEN.
- R-0274 (Low, F107 R7): the R7 block contradicted itself about which commit
  carries a `Landed:` line, and asked for a commit's own SHA inside that
  commit. The worker applied the safe reading and disclosed both. OPEN.
- R-0280 (Medium, F107 R10): the R10 block contradicted itself about which
  commit carries two `docs/README.md` pairs; the losing reading would have
  committed three commits on a RED docs suite. The worker took the safe one.
  OPEN.
- R-0282 (Low, F107 R11): the R11 block said "exactly these nine paths" over
  a list of eight. Reviewer arithmetic, paid for with a declared deviation.
  OPEN.
- R-0284 (Low, F107 R11): two line citations in the R11 block were wrong.
  Citation-accuracy class. OPEN.
- R-0285 (Low, F107 R12): the R12 block's zero-gate on `^Landed:` made the
  protocol's own marker unwritable in the one round that landed a fix. The
  rule: such a zero-gate is safe only in a round that lands no fix. OPEN.
- R-0286 (Medium, F107 R13 integration gate): the full suite is RED at the
  merge base with five ids — every `[reviewer]` parametrization in
  `tests/orchestration/test_role_conventions.py` — because
  `docs/agents/reviewer_conventions.md` estimates 954 tokens against the
  800-token cap declared in `packages/orchestration/role_conventions.py`, so
  composing the segment raises `PromptSegmentError` before any assertion
  runs. Pre-existing, not branch-introduced; expect the same five at this
  feature's gate. OPEN.
- R-0287 (Low, F107 R13): `docs/agents/planner_reviewer_prompt.md` §4.4
  routes every severity decision to "the canonical scale in
  review_protocol.md", but no `docs/agents/review_protocol.md` exists on
  disk, so every severity here is assigned from precedent. OPEN.
- R-0289 (Medium, F107 R16): the R16 block ordered its ONLY push at its last
  commit; the session died after C4 and twelve commits sat on local disk
  alone. Rule, forward-looking and applied throughout this feature: a round
  pushes after EVERY commit. OPEN.
- R-0290 (Medium, F107 R18): not one of the six Phase 0 probe commands in
  `docs/agents/self_drive_protocol.md` can see a feature branch that is not
  checked out, and a completed-but-unclosed feature has by design no open PR
  — so Rule A5 can re-claim a feature already deep on a branch. Fix: Phase 0
  gains a `feature/*` branch sweep and Phase 1 a pending-feature rule that
  outranks A5. This session ran that sweep by hand before claiming F111.
  OPEN.
- R-0294 (Low, F107 R19): the R18 block was emitted without the §3
  pre-emission checklist run on its final bytes — 407 lines against the cap
  of 400, plus a self-counting zero-gate. Registered against the reviewer
  role. OPEN.
- R-0295 (Medium, F107 R21): `scripts/make_review_zip.sh:218-259` collects
  with a hardcoded `find` prune list that predates the `.remedy-wt/` scratch
  convention, and the post-publication scan at `:509` then rejects the
  package for the `/.data/` and `/.git/` components it just published —
  closure blocked by construction, and a leak surface for any scratch holding
  a `.env` or a log. The durable fix is one prune entry, owned by a
  follow-up. OPEN.
- R-0296 (Low, F107 R21, flake class):
  `tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome`
  is load-sensitive and fails intermittently under `-n auto`; two runs of the
  same head disagreed. Routed to F252. OPEN.
- R-0297 (Low, F107 R22): the R21 block made a filesystem path OUTSIDE the
  repository load-bearing without probing it first — every path outside
  `/home/decodeux/Repos/remedy` is denied by this environment — and the round
  lost its second half. The filesystem twin of §3 checklist item 5. OPEN.

## Steps
R1 claim, state reset and carry-forward · R2 the repair-path DECISION plus
T001 hunk selection · T002 response schema, fence pre-check and
apply-with-conflict fallback · T003 wiring, mode and token evidence ·
integration gate · closure.

## Round gates

### R1 — PASS (2026-08-13)
Reviewed by the main session over d956be2f..b0ab8e09, base 4e0b762e. Every
number below was produced by the reviewer re-running the command, not read
off the handback. `python3 -m pytest tests/docs/ -q` exit 0, 294 passed.
`python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, 42 passed.
Transport: the PRIMARY cmp proof holds, no digest fallback was needed —
`.remedy-wt/f111r1/BLOCK` and `.agent/authored/f111-r1-1.md` are
byte-identical at sha256 348f4541705097eb..., and `.agent/live_review.md`,
`.agent/plan.md` and `.agent/context.md` are byte-identical to their
scratchpad originals LR, PLAN and CTX. Scope: `git diff --name-only
main...HEAD` lists exactly the seven ordered paths and nothing else. STATUS:
claim commit b1017248 reads `1 1`; the `[~]` line occurs 1x and the `[ ]`
line 0x. No `Done:` and no `Landed:` line was written this round, and no
marker line leaked into live_review, plan, context, handoff or STATUS.
Per-commit insertions 319/293/1/96/30/27/50, each under the 500 cap. Tree
clean; remote comparison `0 0`. No finding: next free ID stays R-0298.

## Decisions

### DECISION F111 D1 — where the diff channel attaches (2026-08-13)
Chosen: F111's prompt side and response side attach to two DIFFERENT existing
seams, because no single seam carries both today.
- Response side (T002): `packages/orchestration/builder_bridge.py`. Its
  `bridge_builder_output_to_repo` already parses a `BuilderOutput` into a
  `StructuredPatch` (stage 1, `parse_builder_patch`) and lands it through
  `apply_structured_patch` (stage 3) — the fenced, snapshot-backed applicator
  whose `_apply_hunks` is already strict and already returns None on any
  context mismatch. The versioned unified-diff response schema, the fence
  pre-check and the conflict fallback belong there, where a model response is
  ALREADY treated as a patch.
- Prompt side (T001): the repair context built by
  `packages/orchestration/repair_context.py` and fed to the next `build_fn`
  call by `builder_bridge.run_bounded_repair_loop`.
- OUT of scope, deliberately: `packages/orchestration/pingpong_loop.py`. Its
  builder is an agentic CLI that edits the staging tree itself; `BuilderOutput`
  carries no patch field on that path and no applicator is invoked there.
  Giving it a diff-shaped response would mean inventing a new provider
  contract and changing applicator semantics — both barred by the feature
  file's Do not touch.
Alternatives considered. (a) Put both sides in `pingpong_loop`: rejected, it
has no response-side patch seam at all, so T002 would have nothing to attach
to. (b) Build a second applicator for the diff path: rejected outright, the
feature file names the existing applicator as the ONLY way changes land.
(c) Defer F111 until ping-pong grows a patch contract: rejected, the
measurable win the feature asks for is reachable today on the bridge path.
How to reverse: delete this DECISION and the amendment it adds to
docs/roadmap/features/T2_F111.md, then re-scope T002 to the preferred seam.
No code depends on it yet.

### R2 — PASS (2026-08-13)
Reviewed by the main session over f71ebc06..5d8d8c56. Every number below the
reviewer produced by re-running the command, not by reading the handback.
`python3 -m pytest tests/orchestration/test_diff_repair.py -q` exit 0, 18
passed. `python3 -m pytest tests/docs/ -q` exit 0, 294 passed. `python3 -m
pytest tests/cli/test_golden_path.py -q` exit 0, 42 passed. The mutation
red-proof was RE-RUN INDEPENDENTLY by the reviewer in its own disposable
worktree: removing the `max(1, ...)` clamp turns exactly two tests red,
`TestMarginClamping::test_start_of_file_clamps_to_line_1` and
`TestMarginClamping::test_margin_wider_than_file_yields_whole_file`, at
2 failed / 16 passed — matching the worker's report. That worktree was
removed and pruned; `git worktree list` shows only the primary checkout and
`git status --porcelain` is empty. Transport: primary cmp proof, no digest
fallback — `.remedy-wt/f111r2/BLOCK` and `.agent/authored/f111-r2-1.md` are
byte-identical at sha256 85e49d42..., `.agent/plan.md` matches its original,
and both appends sit verbatim at their targets' tails. Append purity proved
by numstat: `51 0` for live_review, `17 0` for the feature file. Scope:
exactly the eight ordered paths. `packages/orchestration/diff_repair.py`
imports only `__future__`, `collections.abc`, `dataclasses` and `pathlib`,
holds no `@@` and neither parses nor applies a diff — the reuse constraint
held. Two Low findings registered below; neither blocks the round.

- R-0298 (Low, F111 R2, reviewer-side authoring defect): step 0 of the R2
  block ordered the worker to "verify all four scratch digests", while the
  block's slice table states digests for only three — LRG, FF and PLAN. The
  fourth entry, BLOCK, is defined as "this entire step block, byte for byte"
  and cannot carry its own digest by construction: a file cannot state the
  hash of bytes that include the statement itself. The worker verified 3 of
  3, pinned BLOCK by the C1 `cmp` instead, and DECLARED the gap rather than
  inventing a fourth number — the wanted behaviour, and the reason this cost
  the round nothing. Same unmeetable-by-construction class as R-0282 and
  R-0285. Forward-looking fix, applied from R3 on: the slice table names how
  many digests it STATES, then BLOCK separately as pinned by the C1 cmp, and
  step 0 counts only the stated ones — the count is whatever that round has,
  never a number carried over from another round. OPEN.
- R-0299 (Low, F111 R2, spec gap in T001): `select_repair_hunks` reports the
  reason `no_ranges` for two different situations. One is a path whose range
  list is genuinely empty (`diff_repair.py:120-122`). The other is a path
  whose ranges ALL clamp away because they point outside the file:
  `_expand_and_merge_ranges` drops every span at `diff_repair.py:85-86` when
  `start > end`, and the caller then reports `no_ranges` at `:129`. The
  second case is a different and load-bearing signal — line numbers past EOF
  mean the ranges came from a diff that no longer matches the file on disk,
  which is exactly the staleness a repair round must not swallow silently.
  This feature's omissions record exists to name what was left out AND why,
  so two causes sharing one reason buys a wrong answer in a later debugging
  session. NOT a worker defect: the eight clauses the R2 block specified did
  not cover the out-of-bounds case, and the worker chose the conservative
  reading and declared it in the handback. Fix ordered in R3: a distinct
  `out_of_bounds` reason with its own test. OPEN.

Landed: R-0299 — a range naming lines the file does not have is now omitted as `out_of_bounds` instead of `no_ranges`, with three new tests; commit "feat(f111): report out of bounds ranges distinctly".

### R3 — PASS (2026-08-13)
Reviewed by the main session over 1bf62e2f..4717ce8c. Re-run by the reviewer,
not read off the handback: `python3 -m pytest
tests/orchestration/test_diff_repair.py -q` exit 0, 21 passed (18 before this
round); `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, 42
passed. The mutation red-proof was RE-RUN INDEPENDENTLY by the reviewer in
its own disposable worktree: reverting the call-site reason to a bare
`no_ranges` turns exactly two tests red,
`TestOutOfBounds::test_range_past_eof_is_out_of_bounds` and
`TestOutOfBounds::test_out_of_bounds_path_does_not_block_present_one`, at
2 failed / 19 passed — matching the worker's report. That worktree was
removed and pruned; `git worktree list` shows only the primary checkout.
Transport: primary cmp proof, no digest fallback — `.remedy-wt/f111r3/BLOCK`
and `.agent/authored/f111-r3-1.md` byte-identical at sha256 a5088325...,
`.agent/last_block.md` equal to both, `.agent/plan.md` equal to its original,
and the 51-line findings slice sits verbatim inside `.agent/live_review.md`.
Append purity by numstat: `51 0` for the findings commit, `2 0` for the
Landed line. Scope: exactly the seven ordered paths. The findings-first
ordering held — C3 persisted R-0298 and R-0299 BEFORE any code commit.
Markers: 24 `- R-0` entries, exactly 1 `Landed:`, 0 `Done:`, and the Landed
line names its commit by SUBJECT rather than by a SHA it could not contain
(R-0274). The fix is minimal: `_expand_and_merge_ranges` is unchanged and the
discrimination happens at the call site. Deviation ACCEPTED: C7 took three
commits because the first handoff came in at 62 lines against its own 60-line
cap; the worker trimmed forward rather than force-pushing — the correct order
of preferences — and declared it. One finding registered below.

- R-0300 (Low, F111 R3, uncovered behaviour change, self-declared by the
  worker in its handback): the R-0299 fix also changes what a range against a
  ZERO-LINE file reports. `_expand_and_merge_ranges` clamps `end` to
  `min(line_count, ...)`, which is 0 for an empty file, while `start` is at
  least 1 — so every span is dropped, and the new call-site discrimination at
  `packages/orchestration/diff_repair.py:136-141` then reports
  `out_of_bounds` where the pre-fix code reported `no_ranges`. The new reading
  is the correct one under the round's own definition (lines were named and
  none of them exist in that file), so nothing on disk is wrong. It is
  registered because it is a SECOND behaviour change beyond the past-EOF case
  the round was ordered to make, and no test pins it — an unpinned behaviour
  is one refactor away from silently reverting. The worker found it in its own
  diff and declared it rather than leaving it for a reader, which is the
  behaviour these rounds are supposed to produce. Fix, one test: an empty file
  with a non-empty range reports `out_of_bounds`. OPEN.
