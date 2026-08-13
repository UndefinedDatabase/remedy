# Live Review — F111 Diff-only repair

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f111-diff-only-repair. The next free finding ID is not
> tracked in this header: `.agent/plan.md` holds it and is rewritten each round.

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

Done: R-0299 — the `out_of_bounds` reason ships and is pinned. Verified at the R3 gate above: `_expand_and_merge_ranges` is unchanged, the discrimination happens at the call site, and the reviewer's own mutation red-proof in a disposable worktree turned exactly the two `TestOutOfBounds` tests red when the reason was reverted to a bare `no_ranges`. RESOLVED.

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

### R4 — PASS (2026-08-13)
Reviewed by the main session over 4717ce8c..c9064b17, a state-only round. Every
gate was RE-RUN by the reviewer rather than read off the handback: `python3 -m
pytest tests/orchestration/test_diff_repair.py -q` exit 0, 21 passed; `python3
-m pytest tests/cli/test_golden_path.py -q` exit 0, 42 passed; `python3 -m
pytest tests/orchestration/test_test_runner.py -q -k 'plan_md or context_md'`
exit 0, 3 passed and 48 deselected. Transport: PRIMARY cmp proof, no digest
fallback — the scratch originals survived the session boundary, so
`.remedy-wt/f111r4/BLOCK` and `.agent/authored/f111-r4-1.md` are byte-identical
at sha256 70625e3e..., `.agent/last_block.md` equals both, `.agent/plan.md`
equals its original, and the LRG slice (sha256 9892593c..., matching the digest
the block stated) is byte-identical to the last 43 lines of
`.agent/live_review.md`. Append purity by numstat: `43 0` for C3, delete column
0. Scope: exactly the five ordered paths — no code, no test, no doc. Markers:
25 `- R-0`, exactly 1 `Landed:`, 0 `Done:`, 1 `### R3 — PASS`. Caps:
`.agent/plan.md` 40 lines, `.agent/handoff.md` 60 lines, per-commit insertions
174/127/43/19/38, each under 500. `git status --porcelain` empty and
`git worktree list` a single entry at the verdict; remote comparison `0 0`.
Two findings are registered below. Both are against the reviewer's OWN earlier
planning text, and both were found by reading the code that text named — which
is what the round the plan ordered ("settle this by reading code, never by
assuming") was for.

- R-0301 (Medium, F111 R2, planning defect — a spec name that resolves to
  nothing): DECISION F111 D1, written into `docs/roadmap/features/T2_F111.md`
  under "Built State", names the bounded repair loop
  `packages/orchestration/builder_bridge.py` (`run_bounded_repair_loop`). No
  such symbol exists anywhere in the repository:
  `grep -rn "run_bounded_repair_loop" packages/ apps/ tests/` returns no hits.
  The real function is `run_builder_bridge_loop`
  (`packages/orchestration/builder_bridge.py:264`), whose own docstring reads
  "Run bounded repair loop: build -> bridge -> test -> repair -> rebuild" — so
  D1 chose the RIGHT seam and recorded the WRONG name for it. AGENTS.md "Code
  Discoverability Conventions" requires that a name grep to its own definition;
  a spec name with zero hits sends the next worker looking for code that is not
  there, and the whole point of writing the seam into the feature file was to
  spare that search. Fix ordered this round as DECISION F111 D2: the feature
  file carries the real name. OPEN.

- R-0302 (Medium, F111 R4, planning defect — a hypothesis the named code
  disproves): `.agent/plan.md` Next Steps 1 proposed that T001's line ranges
  come from `review_scope._parse_diff` applied to "the diff of the
  `source_patch_applied` event", and told the next round to confirm that the
  event carries a diff. It does not.
  `packages/orchestration/source_apply.py:355-362` emits `source_patch_applied`
  with exactly `apply_id`, `snapshot_id`, `snapshot_verified`, `success`,
  `files_modified`, `files_created` and `error_count` — no diff text and no
  line numbers — and `build_repair_context` reads only the file LISTS back out
  of it (`packages/orchestration/repair_context.py:56-72`). The ranges must
  come from the patch that was applied, which the loop already holds in memory:
  `run_builder_bridge_loop` keeps every cycle's `bridge_result`
  (`packages/orchestration/builder_bridge.py:325`), and
  `BridgeResult.parse_result.patch` is a `StructuredPatch` whose
  `unified_diffs` entries carry per-path diff text
  (`packages/orchestration/structured_patch.py:37-56`). This is registered as a
  finding instead of being re-planned quietly because a written plan step was
  disproved by the code it pointed at, and the next reader deserves the reason
  on disk. Fix ordered this round as DECISION F111 D3. OPEN.

Done: R-0300 — a zero-line file whose range names lines it does not have now reports `out_of_bounds`, pinned by `TestEmptyFileRanges::test_empty_file_with_a_non_empty_range_is_out_of_bounds`. Verified at the R5 gate: the reviewer re-ran the file at 30 passed and read the test, which asserts the reason, the empty hunk tuple and `total_chars == 0`. RESOLVED.
Done: R-0301 — `docs/roadmap/features/T2_F111.md` now names `run_builder_bridge_loop`, the symbol that exists. Verified at the R5 gate by the reviewer's own greps over that file: `run_bounded_repair_loop` 0x, `run_builder_bridge_loop` 2x, and `grep -rn` over packages/ apps/ tests/ resolves the new name to `packages/orchestration/builder_bridge.py:264`. RESOLVED.
Done: R-0302 — the range source is `changed_line_ranges_from_patch`, which reads the applied `StructuredPatch` through the single shared parser `review_scope.parse_diff_line_ranges` rather than the diffless `source_patch_applied` event, and DECISION F111 D3 records why on disk. Verified at the R5 gate: nine new tests, the reviewer's independent mutation red-proof, and the expected range values confirmed against the real `_parse_diff` before the block was emitted. RESOLVED.

### R5 — PASS (2026-08-13)
Reviewed by the main session over c9064b17..d0952432. Every number was produced
by the reviewer re-running the command, never read off the handback:
`python3 -m pytest tests/orchestration/test_diff_repair.py
tests/orchestration/test_review_scope.py -q` exit 0, 62 passed (30 + 32, 21 + 32
before); `python3 -m pytest tests/docs/ -q` exit 0, 294 passed (docs-round gate,
this round touched docs/roadmap/**); `python3 -m pytest
tests/cli/test_golden_path.py -q` exit 0, 42 passed (canary); `python3 -m ruff
check` over the three touched files exit 0. The MUTATION RED-PROOF was re-run
INDEPENDENTLY by the reviewer in its own disposable worktree: deleting the two
`for file_op in patch.file_ops:` lines from `changed_line_ranges_from_patch`
turns exactly `test_file_ops_paths_carry_no_lines` and
`test_a_file_ops_path_is_reported_as_no_ranges_by_selection` red at 2 failed /
28 passed — the worker's numbers reproduce. That worktree was removed and
pruned; `git worktree list` shows only the primary checkout. Transport: PRIMARY
cmp proof, no digest fallback — `.remedy-wt/f111r6` aside, `.remedy-wt/f111r5/BLOCK`,
`.agent/authored/f111-r5-1.md` and `.agent/last_block.md` are byte-identical,
and all five content slices occur EXACTLY ONCE in their target files by
`str.count` against the originals. Append purity by numstat: `59 0` for the
findings commit, `1 1` for the R-0299 resolution, `3 0` for the landed lines.
Scope: exactly the nine ordered paths — no production file outside
`diff_repair.py` and `review_scope.py` was touched, and `builder_bridge.py`,
`repair_context.py`, `source_apply.py` and `pingpong_loop.py` are unchanged as
ordered. Markers before this round's own commits: 27 `- R-0`, 3 `Landed:`, 1
`Done:`, 1 `### R4 — PASS`. Caps: `.agent/plan.md` 47 lines; per-commit
insertions 200/185/59/1/164/20/3/26, each under 500. `git status --porcelain`
empty and remote comparison `0 0` at the verdict.

Deviation ACCEPTED, not a precedent: `.agent/handoff.md` came in at 78 lines
against the 60-line cap, with a DECISION D15 "Deviations, declared" line naming
the measured count and the mandated content that caused it — a nine-row commit
table, a nine-row changed-files table, an eight-gate verification table and a
nine-row item-status table. No section was dropped and there is no padding, so
the overage is the block's own doing: a nine-commit round cannot report itself
in sixty lines. The worker also corrected its own first draft when `wc -l` gave
78 against an estimated 74, which is the right order of operations.

The round's honesty is worth recording: `.agent/plan.md` and the handoff BOTH
state that T001 now has its selector and its range source and STILL HAS NO CALL
SITE, so a green suite here is not a working feature. That is the R-0220 class
disclosed by the round itself rather than found at a gate.

- R-0303 (Low, F111 R5, reviewer-side authoring defect): the R5 block gated the
  landed-marker commit with `git show --numstat` exactly `3 0`, which forbids
  the blank separator line this file uses everywhere else, so the three
  `Landed:` lines landed flush against the last line of the R-0302 paragraph
  and render as part of that list item. Same class as R-0285: an exact-count
  gate that makes the correct formatting unwritable in the one commit that
  needs it. The worker applied the block as written and flagged it in the
  handback instead of quietly improving it, which is the behaviour these rounds
  are supposed to produce. Fixed in this round's resolution commit, which
  rewrites those three lines with the separator restored. OPEN.

- R-0304 (Low, F111 R4 and R5, reviewer-side omission):
  docs/agents/planner_reviewer_prompt.md section 3 requires the handoff's state
  block to repeat the operator brief's "Fortschritt" line verbatim, estimate
  label included, so the progress estimate always exists on disk and not only
  in the chat brief. Neither the R4 block nor the R5 block ordered that line,
  and neither handoff carries one. The R4 gate passed without catching it, so
  this is registered at the round where it was noticed rather than backdated.
  Fix: every future block's handback item names the Fortschritt line as
  mandated content. OPEN.

### R6 — PASS (2026-08-13)
Reviewed by the main session over d0952432..b1e5cc7e, a state-only round. Every
gate was re-run by the reviewer, not read off the handback: `python3 -m pytest
tests/orchestration/test_diff_repair.py tests/orchestration/test_test_runner.py
-q` exit 0, 81 passed (30 unchanged plus 51); `python3 -m pytest
tests/cli/test_golden_path.py -q` exit 0, 42 passed (canary). Transport:
PRIMARY cmp proof, no digest fallback — `.remedy-wt/f111r7` aside,
`.remedy-wt/f111r6/BLOCK`, `.agent/authored/f111-r6-1.md` and
`.agent/last_block.md` are byte-identical, and both content slices occur
EXACTLY ONCE in `.agent/live_review.md` by `str.count` against the originals.
Append purity by numstat: `63 0` for the findings commit and `4 3` for the
resolution commit, the delete column matching the three `Landed:` lines that
became `Done:` text. Markers: 29 `- R-0`, 4 `Done:`, 0 `Landed:` (exit 1, the
pass), 1 `### R5 — PASS`. Caps: `.agent/plan.md` 46 lines; per-commit
insertions 116/94/63/4/21/59, each under 500. `git status --porcelain` empty,
`git worktree list` one entry, remote comparison `0 0`. Scope: exactly the five
ordered paths, no production, test or docs file touched.

Deviation ACCEPTED: C5 kept two Risks entries where the block said "the two
existing Risks entries" and `.agent/plan.md` in fact carried THREE. The worker
kept the two durable ones and dropped the stale third — the note saying the R4
`source_patch_applied` hypothesis "is deleted here", which R-0302's resolution
retires — and declared the deviation rather than guessing silently. That is the
correct call on the merits; the arithmetic error is the reviewer's and is
registered as R-0305 below.

- R-0305 (Low, F111 R6, reviewer-side arithmetic in an authored block): the R6
  step block instructed "Keep the two existing Risks entries" against a
  `.agent/plan.md` whose Risks section held three bullets. A worker told to
  keep two of three must either drop one on its own judgement or stop, and this
  one dropped the correct bullet and declared it — but the block put it in that
  position for no reason. Same class as R-0282 (a block naming nine paths over
  a list of eight): counts inside authored blocks are asserted from memory
  instead of measured against the file the block is about. The rule that
  follows: any count an authored block states about an EXISTING file is read
  off that file at authoring time, the way section 3 checklist item 6 already
  requires for zero-gates. OPEN.

- R-0306 (Low, F111 R6, incomplete handoff): the R6 handback declared C5
  `deviated` with its reason, but `.agent/handoff.md` records C5 as plain
  `done` with an empty Reason cell, so the deviation exists only in the chat
  handback and not on disk. AGENTS.md "Completion Report — Item-Status Table"
  requires the status values `done`, `skipped` and `deviated` with reasons, and
  docs/agents/planner_reviewer_prompt.md section 4.8 makes the handoff the only
  return channel — an outcome absent from it is a finding by construction. The
  round itself is unaffected: the deviation was disclosed, reviewed and
  accepted at this gate, and this entry is what puts it on disk. Fix: the
  item-status table in the handoff carries the same status the handback
  declares, always. OPEN.

### R7 — PASS (2026-08-13)
Reviewed by the main session of the next self-drive session over
b1e5cc7e..023e8d9d, a state-only round. Section 4.13 does not apply here: a
new session CAN gate the round that closed the previous one, and this entry is
that gate. Every command was re-run by the reviewer, never read off the
handback. Transport: PRIMARY cmp proof, no digest fallback —
`.remedy-wt/f111r7/BLOCK` and `.agent/authored/f111-r7-1.md` are
byte-identical, that file and `.agent/last_block.md` are byte-identical,
`sha256sum .remedy-wt/f111r7/LRG` reproduces the stated digest ending
d49c182, and a `str.count` of that slice against `.agent/live_review.md`
prints 1. Append purity by numstat: `50 0` for the findings commit and `2 2`
for the plan pair. Markers on the final file: 31 `- R-0`, 4 `Done:`, 0
`Landed:` (exit 1, the pass), 1 `### R6 — PASS`. Plan: the retired id 0x
(exit 1, the pass), `Next free finding ID: R-0307` 1x, `Open findings: 27`
1x, 46 lines. Handoff: 76 lines carrying the DECISION D15 stated-cause line
that names 76, and 1 `^Fortschritt: ` line. Tests: `python3 -m pytest
tests/orchestration/test_test_runner.py -q -k 'plan_md or context_md'` exit 0,
3 passed 48 deselected; `python3 -m pytest tests/cli/test_golden_path.py
tests/orchestration/test_diff_repair.py -q` exit 0, 72 passed — the 42 canary
plus the 30 T001 tests, unchanged, as a round that touches no code requires.
Hygiene: `git status --porcelain` empty, `git worktree list` one entry,
per-commit insertions 109/71/50/2/45 each under 500, `git rev-list
--left-right --count origin/feature/f111-diff-only-repair...HEAD` prints
`0 0`. Scope: exactly the five ordered paths; no production, test or docs
file was touched.

- R-0307 (Low, F111 R7, stale live-looking header): the header of
  `.agent/live_review.md` names a next-free finding id that the body has long
  overtaken — the findings below it run past it by four — so the file's own
  header contradicts its body, and a reader who trusts it would reuse ids
  already allocated. It was true when the file was reset and nothing updates
  it, which is the R-0228 class: a line that positively CLAIMS a live value it
  does not track. The fix is not to refresh the number, because the next round
  would stale it again, but to stop the header carrying a counter at all —
  `.agent/plan.md` already holds it and is rewritten every round. OPEN.

Done: R-0307 — the header no longer names a next-free finding id; it points at
`.agent/plan.md`, which is rewritten every round and is the one place the
counter lives. Verified at the R8 gate: `sed -n '8,9p'` matches the authored
two-line replacement byte for byte, and the retired line is the single
deletion in commit ea0d63b3's `4 1` numstat. Resolved.

### R8 — PASS (2026-08-13)
Reviewed by the main session over 023e8d9d..456a25e9. Every ordered gate was
re-run by the reviewer, and the new module was additionally probed live, never
read off the handback. Transport: PRIMARY cmp proof, no digest fallback —
`.remedy-wt/f111r8/BLOCK`, `.agent/authored/f111-r8-1.md` and
`.agent/last_block.md` are byte-identical, `.remedy-wt/f111r8/PLAN` and
`.agent/plan.md` are byte-identical, and a `str.count` of the appended slice
against `.agent/live_review.md` prints 1. Append purity by numstat: `36 0` for
the gate commit and `4 1` for the header pair, the single deletion being the
retired counter line and nothing else. Markers on the final file: 32 `- R-0`,
4 `Done:`, 1 `Landed:`, 1 `### R7 — PASS`. Caps: the plan is 48 lines and
carries `## Goal` and `## Next Steps`; the step block is 356 lines, under the
DECISION F105 D5 limit of 400; per-commit insertions 356/341/36/4/50/439/111,
each under 500. Tests: `python3 -m pytest
tests/orchestration/test_diff_repair_response.py
tests/orchestration/test_diff_repair.py tests/cli/test_golden_path.py -q` exit
0, 95 passed — 23 new, the 30 T001 tests unchanged, 42 canary; `python3 -m
pytest tests/orchestration/test_source_apply.py
tests/orchestration/test_source_apply_transaction.py
tests/orchestration/test_fence_e2e.py tests/test_path_utils.py
tests/test_data_paths.py -q` exit 0, 225 passed — the 174 behaviour pin the
reviewer measured BEFORE the round, unchanged, plus the 51 repo-wide guards
that rglob every `packages/**/*.py` and therefore already reach the new module.
Reviewer's own probe, beyond the ordered gates: a two-file diff declared with
one path returned exactly `diff touches undeclared path: src/b.py`; a ghost
declaration returned exactly `declared path not touched by the diff:
src/ghost.py`; `precheck_diff_repair_fences` denied `remedy.toml` with reason
`denied:builtin:project config file`, and denied a path lying outside a job
allow glob. The C5 reuse is real, not nominal: the three path-safety message
strings moved into `unsafe_path_issues` unchanged and `validate_structured_patch`
now calls it. Hygiene: `git status --porcelain` empty, `git worktree list` one
entry, remote comparison `0 0`. Scope: exactly the eight ordered paths.

Deviation ACCEPTED: C4's `Landed:` line names `commit C4 of R8` instead of its
own short sha. A commit cannot carry its own sha without amending, the block
named that fallback explicitly, and the handoff's item-status table declares
C4 `deviated` with that reason — finding R-0306 repaired on its first occasion
after being registered.

- R-0308 (Low, F111 R8, unreachable defensive branch): `parse_diff_repair_response`
  returns `not_an_object` for a decoded value that is not a dict, and that
  branch cannot execute today: `extract_json_object` only ever returns text
  starting with `{`, so a successful `json.loads` always yields a dict. The
  worker disclosed it rather than writing a test that could not pass honestly,
  which is DECISION F105 D10 working as designed. Registered so the branch is
  never later mistaken for tested behaviour. It stays for now — it becomes
  reachable the moment `extract_json_object` learns to return array text — and
  the decision to keep or delete it belongs to the closure round, not to a
  repair. OPEN.

### R9 — PASS (2026-08-13)
Reviewed by the main session over 456a25e9..33f408b2. Every ordered gate was
re-run by the reviewer, and the new split was probed live against the real
applier rather than read off the handback. Transport: PRIMARY cmp proof, no
digest fallback — `.remedy-wt/f111r9/BLOCK`, `.agent/authored/f111-r9-1.md`
and `.agent/last_block.md` are byte-identical, `.remedy-wt/f111r9/PLAN` and
`.agent/plan.md` are byte-identical, and `str.count` of both the LRG and the
DONE slice against `.agent/live_review.md` prints 1. Numstat purity: `50 0`
for the gate append and `5 1` for the R-0307 resolution, the single deletion
being the retired `Landed:` line. Markers: 33 `- R-0`, 5 `Done:`, 0 `Landed:`
(exit 1, the pass), 1 `### R8 — PASS`. Caps: the block is 330 lines, under the
DECISION F105 D5 limit of 400; per-commit insertions 330/262/50/5/139/110/93,
each under 500. Tests: `python3 -m pytest
tests/orchestration/test_review_scope.py
tests/orchestration/test_diff_repair_response.py
tests/orchestration/test_diff_repair.py tests/cli/test_golden_path.py -q` exit
0, 138 passed — 39 (32 before, 7 new), 27 (23 before, 4 new), 30 unchanged, 42
canary; `python3 -m pytest tests/orchestration/test_final_verifier.py
tests/orchestration/test_reviewer_prompt_scope.py
tests/orchestration/test_pingpong.py tests/test_path_utils.py
tests/test_data_paths.py -q` exit 0, 197 passed — the 146 `_parse_diff`
consumer pin the reviewer measured BEFORE the round, unchanged, plus the 51
repo-wide guards. Hygiene: `git status --porcelain` empty, `git worktree list`
one entry, remote comparison `0 0`. Scope: exactly the nine ordered paths.

Deviation ACCEPTED: C7 applied a 47-line PLAN slice where the block said 46.
The worker applied the authored bytes verbatim and declared the mismatch
rather than reflowing text to hit a number, which is the correct call — the
error is the reviewer's and is registered as R-0309 below.

- R-0309 (Low, F111 R9, reviewer-side arithmetic in an authored block): the R9
  block stated its PLAN slice was 46 lines and gated `wc -l` on that number;
  the slice is 47 lines. Third instance of the class after R-0282 and R-0305,
  and the second in three rounds, so the rule R-0305 stated is not being
  applied: any count an authored block asserts about a file — including a file
  the block itself carries — is MEASURED before emission, never recalled. The
  reviewer cannot measure its own not-yet-written slice with a shell, so the
  standing fix is different in kind: gate authored slices on `cmp` against the
  applied file, which proves byte identity, and never on a line count, which
  proves nothing the `cmp` does not already prove. OPEN.

- R-0310 (Low, F111 R9, cosmetic residue in a correct function):
  `split_diff_by_path` drops preamble before the FIRST `---` line, so in a
  git-style multi-file diff the `diff --git` and `index` lines introducing
  file N+1 stay at the TAIL of file N's section. The worker disclosed this
  instead of writing a test that would have to pass dishonestly. The reviewer
  proved the residue harmless: `_apply_hunks` breaks its hunk body on any line
  starting with `diff `, and its outer loop skips every line that is not a
  hunk header, so both sections of a two-file git diff applied to the right
  content in a live probe. Kept for v1 as a cosmetic wart, not a correctness
  defect; a section is still a standalone applicable diff. OPEN.

- R-0311 (High, F111 R9, pre-existing silent file corruption in the
  applicator): `source_apply._apply_hunks` collects each addition WITH its
  position, then throws those positions away and inserts every added line at
  `insert_at = orig_start + offset` — the start of the hunk. Any hunk whose
  additions are not on its first line therefore writes them to the wrong
  place. On the repository's own test input, `original = "alpha\nbeta\ngamma\n"`
  with `@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n`, the function returns
  `alpha\ngamma\nBETA\n` where the diff says `alpha\nBETA\ngamma\n`. The
  existing guard `TestHunkValidation::test_correct_context_applies` passes only
  because it asserts `"BETA" in result` and never checks order, which is how
  this survived. Every `intent_kind="unified_diff"` patch in Remedy lands
  through this function, and F111's Done criterion is literally that no repair
  path can silently corrupt a file, so the diff channel cannot ship over it.
  Fixed in R10 per DECISION F111 D4. OPEN.

### DECISION F111 D4 (2026-08-13) — the applier order fix is in scope
Chosen: repair `_apply_hunks` inside F111, in R10, scoped to hunk application
order and nothing else. Alternatives considered: (a) route it to a new feature
and ship F111's diff channel over a corrupting applier — rejected, because the
feature's own Done criterion forbids exactly that; (b) work around it in
`diff_repair_response` — rejected, because it would be a second applier, which
this feature has refused twice already. The feature file's Do-not-touch names
"applicator semantics", and an off-by-one in where a line lands is not a
semantic of the applicator, it is a defect in it: the all-or-nothing contract,
the fence preflight, the snapshot gate and the rollback path are untouched by
this fix. Reverse by reverting R10's C4 commit; the tests it adds name the
behaviour precisely enough that a reverter knows what they are giving up.
