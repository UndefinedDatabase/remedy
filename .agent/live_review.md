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

### R10 — PASS (2026-08-13)
Reviewed by the main session over 33f408b2..8644def9. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: PRIMARY cmp proof — `.agent/authored/f111-r10-1.md` and
`.agent/last_block.md` are byte-identical. Numstat purity: `80 0` for the gate
append and `2 0` for the `Landed:` line, both pure appends as ordered. Markers
on the final file: 36 registered ids, 5 resolutions, 1 landed marker, 1 R9 pass
heading, 1 D4 heading. The fix proved BY VALUE, not by colour:
`_apply_hunks('alpha\nbeta\ngamma\n', '@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n')`
printed `'alpha\nBETA\ngamma\n'` at exit 0. Tests, each re-run by the reviewer:
179 passed for the source-apply tier, 138 for the untouched modules plus the
golden-path canary, 225 for the applier's other consumers. Red-proof: in a
disposable worktree at HEAD with `source_apply.py` checked out from 33f408b2,
`pytest tests/orchestration/test_source_apply_transaction.py -q` exited 1 with
5 failed / 10 passed — exactly the five ids the handback named, and
`test_pure_deletion_hunk_removes_only_its_line` passes on the old code, as the
handback declared. Worktree removed and pruned; `git status --porcelain` empty,
`git worktree list` one entry. Scope: exactly the seven ordered paths.

Deviation ACCEPTED: C5's authored `Landed:` line says "six order tests added";
C4 adds five new tests and strengthens one existing assertion. The worker
applied the authored bytes verbatim and declared the mismatch instead of
reflowing text to match a number, which is the correct call — the error is the
reviewer's and is registered as R-0314 below.

Done: R-0311 — `_apply_hunks` no longer collects a hunk's additions and dumps
them at the hunk's start; it splices the hunk's new block over the exact
original range the hunk consumed, so an added line lands at its own position.
Proved by value at the R10 gate and pinned by five new order tests plus the
strengthened `test_correct_context_applies`, which now asserts the full result
string instead of a substring. Resolved. The header-side placement defect found
while gating this fix is a SEPARATE finding, R-0312 below, not a reopening.

- R-0312 (High, F111 R10, hunk-header off-by-one in the applicator, the same
  Done-criterion class as R-0311): `_apply_hunks` computes every hunk's 0-based
  start as `int(m.group(1)) - 1`. That is correct only for a hunk that consumes
  at least one original line. A unified-diff hunk whose OLD COUNT is 0 is a pure
  insertion, and its header names the line AFTER which the content goes, so its
  0-based index is the line number ITSELF. Confirmed against real `git diff
  -U0`, not from memory: inserting `X` between `a` and `b` in `a\nb\nc\n` emits
  `@@ -1,0 +2 @@`, prepending emits `@@ -0,0 +1 @@`, appending emits
  `@@ -3,0 +4 @@`. Measured on the R10 applier against `'a\nb\nc\n'`:
  `@@ -1,0 +2 @@\n+X\n` returned `'X\na\nb\nc\n'` where the diff says
  `'a\nX\nb\nc\n'`; `@@ -3,0 +4 @@\n+X\n` returned `'a\nb\nX\nc\n'` where the
  diff says `'a\nb\nc\nX\n'`; and `@@ -0,0 +1 @@\n+X\n` returned
  `'a\nb\nc\nX\n'` — `orig_start` is -1 there, so `result_lines[-1:-1]` inserts
  before the trailing element and a PREPEND silently becomes an APPEND. The
  same three values were measured on the PRE-R10 applier, so this is not an R10
  regression: it is the older half of the same defect, and R-0311's fix could
  not reach it because every test in that round used hunks with context. No
  validation fires on any of these inputs — a pure-insertion hunk has no context
  and no removal line to check — so the file is written wrong and reported as
  applied, which is exactly the failure this feature's Done criterion names.
  OPEN.

- R-0313 (Medium, F111 R10, acceptance narrowed by the body-walk rewrite):
  R10 changed a hunk-body line that is none of ` `, `+`, `-` from `pos += 1` to
  ignored. The block declared that for `\ No newline at end of file`, which is
  right, but it also covers a case the block did not name: a BLANK context line
  whose single leading space was stripped in transport arrives as `""`. The old
  applier consumed it as context; the new one ignores it, `old_len` runs one
  short, and the next `-` or context line then validates against the wrong
  original index and returns None. Measured both sides on this machine:
  `'a\n\nb\n'` with `@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n` returned `'a\n\nB\n'`
  before R10 and returns None after it. The direction is SAFE — an
  all-or-nothing rejection that falls back, never a corrupted file — so this is
  not a corruption finding. It matters because F111 exists to apply
  MODEL-generated diffs, and stripping the trailing space off a blank line is
  among the most common things a model or a transport does, so the diff channel
  will fall back on a class of otherwise-valid answers. The fix does NOT belong
  in `_apply_hunks`: `diff_text.split("\n")` also yields a trailing `""` for any
  diff ending in a newline, so treating `""` as context there would make the
  last hunk consume one original line too many — trading a safe rejection for a
  silent corruption. Normalise on the response side, where the diff's own line
  structure is known. Deferred to T002/T003 by decision, not fixed in R11. OPEN.

- R-0314 (Low, F111 R10, fourth instance of an unmeasured count in authored
  text): the R10 block's authored `Landed:` line asserted "six order tests
  added"; C4 adds five and strengthens one. R-0282, R-0305 and R-0309 are the
  same class. R-0309's standing fix — gate authored slices on `cmp`, never on a
  line count — was applied to R10's slices and worked; the count that broke was
  embedded in authored PROSE, which a `cmp` gate cannot catch by construction.
  Widened rule, applied from R11 onward: an authored text states a number about
  the change set only when that number is already measured on disk, and when it
  cannot be — because the change does not exist yet — the text names the thing
  without a count. OPEN.

### DECISION F111 D5 (2026-08-13) — the header off-by-one is in scope too
Chosen: fix R-0312 inside F111, in R11, scoped to the hunk-header start
computation and nothing else. This extends DECISION F111 D4 by the same
reasoning: the feature's Done criterion is that no repair path can silently
corrupt a file, and a pure-insertion hunk that lands its content at the wrong
index — or turns a prepend into an append — is that criterion failing, not an
"applicator semantic" the Do-not-touch list protects. Alternatives considered:
(a) ship the diff channel and file the header bug against a later feature —
rejected, it is the same defect class the round before this one just refused to
ship over; (b) reject every zero-old-count hunk instead of placing it correctly
— rejected, `-U0` diffs are the SMALLEST diffs a model can send and this feature
exists to make repairs smaller, so refusing them would defeat its purpose while
leaving the `@@ -0,0` splice-at-minus-one path reachable anyway. Reverse by
reverting R11's C4 commit; the tests it adds name the behaviour precisely enough
that a reverter knows what they are giving up.

### R11 — PASS (2026-08-13)
Reviewed by the main session over 8644def9..06e85a11. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: PRIMARY cmp proof — `.agent/authored/f111-r11-1.md` and
`.agent/last_block.md` are byte-identical. Numstat purity: `102 1` for the gate
commit, the single deletion being the retired R-0311 marker line the reviewer
replaced with authored text, and `2 0` for the new marker line. Markers on the
final file: 39 registered ids, 6 resolutions, 1 landed marker, 1 R10 pass
heading, 1 D5 heading. Scope: exactly the seven ordered paths, no more.

The fix proved BY VALUE, not by colour. Against `'a\nb\nc\n'`, the reviewer ran
the three zero-count headers real `git diff -U0` emits for an insert-in-middle,
a prepend and an append: `@@ -1,0 +2 @@`, `@@ -0,0 +1 @@` and `@@ -3,0 +4 @@`,
each with a single `+X` body. They now return `'a\nX\nb\nc\n'`, `'X\na\nb\nc\n'`
and `'a\nb\nc\nX\n'`. On the R10 applier the same three returned
`'X\na\nb\nc\n'`, `'a\nb\nc\nX\n'` and `'a\nb\nX\nc\n'` — every one placed
wrong, and the prepend silently appended. Both rejections were exercised
directly: `@@ -0,1 +0,2 @@\n+X\n` on `'a\nb\n'` returned `'a\nb\nX\n'` before
and returns None now, and `@@ -1,0 +2 @@\n a\n+X\n` on `'a\na\nb\n'` — chosen
because its context line still MATCHES at the shifted index, so only the new
contradiction check can reject it — returns None. R10's own fix still holds:
the `alpha/BETA/gamma` probe still prints `'alpha\nBETA\ngamma\n'`.

Tests, each re-run by the reviewer: 185 passed for the source-apply tier, 179
before the round plus the 6 new cases; 138 for the untouched modules plus the
golden-path canary, unchanged; 225 for the applier's other consumers,
unchanged, so the header change regressed no existing consumer. Red-proof: in a
disposable worktree at HEAD with `source_apply.py` checked out from 8644def9 —
which reverts exactly C4 and nothing else —
`pytest tests/orchestration/test_source_apply_transaction.py -q` exited 1 with
6 failed / 15 passed, the six failures being exactly the six tests C4 adds,
with every pre-existing test still passing on the old applier. Worktree removed
and pruned; `git status --porcelain` empty, `git worktree list` one entry,
`git rev-list --left-right --count` against the remote `0 0`. Caps: per-commit
insertions 355/266/102/71/2/99, each under 500; `.agent/plan.md` 49 lines,
under the AGENTS.md limit of 50; `.agent/handoff.md` 95 lines, over the 60 cap
and carrying the DECISION D15 stated-cause line, which is the sanctioned shape.
No deviations were declared and the reviewer found none.

Done: R-0312 — a hunk whose OLD COUNT is 0 now splices AFTER the line its
header names instead of one line before it, so a pure-insertion hunk lands
where the diff says and `@@ -0,0 +1 @@` prepends instead of silently appending.
A header that declares a pure insertion while its body consumes original lines
is rejected outright, and a negative splice index can no longer be reached. The
absent-count short form `@@ -2 +1,0 @@` still means a count of 1 and is
unchanged. Proved by value at the R11 gate in both directions and pinned by six
new tests, all six of which fail on the pre-fix applier. Resolved.

With R-0311 and R-0312 both closed, `_apply_hunks` places a hunk's content
correctly in both axes it can get wrong: WHERE inside the hunk an added line
goes, and WHERE in the file the hunk itself starts. Remedy deliberately does
not cross-check a hunk header's declared old count against the number of lines
its body actually consumes when that count is 1 or more: models routinely
miscount headers while quoting content exactly, and this applier's strictness
is deliberately spent on CONTENT — every context and removal line is compared
against the real file — rather than on arithmetic a wrong-but-harmless header
would fail. The count is read only to decide the zero-insertion case, where it
is the sole available signal.

- R-0315 (Medium, F111 R11, feature file allows what the applicator refuses):
  `docs/roadmap/features/T2_F111.md` states under "Edge cases & assumption
  defaults (A9)" that new-file creation inside a diff is ALLOWED if the path
  passes fences, and that only deletions require the full-file path in v1. The
  code disagrees: `_apply_unified_diff` returns early with
  `f"{diff.path}: file not found for diff"` and sets `success = False` whenever
  `full.is_file()` is false, so a diff that creates a file can never apply, and
  a model that correctly answers a repair with a new-file hunk gets a failed
  apply rather than a created file. Found by the reviewer while gating R11, not
  by a test. Note the interaction with R-0312: a new-file diff is exactly the
  `@@ -0,0 +1,N @@` shape whose placement R11 just fixed, so the two would meet
  in the same code path the moment the file-existence guard is lifted. This is
  NOT a defect R11 introduced and NOT one R11 should have fixed — its change
  set was the header computation — but T002's apply half runs straight into it,
  so it is registered before that round rather than discovered during it. R13
  decides: either implement creation behind the fence check as the feature file
  says, or amend the feature file to match v1 reality under §4.7 and say why.
  Do not let R13 pick silently. OPEN.

### DECISION F111 D6 (2026-08-13) — new-file creation stays on the full-file path
Chosen for finding R-0315: amend the feature file to match v1 reality rather
than lift the applicator's file-existence guard. `_apply_unified_diff` keeps
requiring `full.is_file()`, so a creation diff fails the apply and the round
falls back to the full-file path — the route deletions already take. Three
reasons. The feature file lists applicator semantics under Do not touch, and
teaching the diff applicator to create files is exactly a semantics change.
A creation diff carries no existing content for the strict context check to
validate against, so the one guarantee this applier sells — every context and
removal line compared against the real file — buys nothing on that path. And
the full-file path already creates files through `_apply_file_op`'s `create`
action, under the same durable snapshot and the same rollback. Alternatives
considered: (a) implement creation behind the fence check, as the A9 sentence
said — rejected on the three reasons above; (b) leave the contradiction on disk
and let T003 discover it — rejected, that is how R-0315 was born. Reverse this
decision by deleting the D6 section of docs/roadmap/features/T2_F111.md and
restoring the A9 sentence.
Done: R-0315 — the feature file no longer allows what the applicator refuses.
DECISION F111 D6 keeps `_apply_unified_diff`'s file-existence guard and amends
the A9 sentence instead, so creation and deletion now take the same full-file
route in v1. Verified at the R13 gate BY VALUE: a `--- /dev/null` answer with
`@@ -0,0 +1,2 @@` returns mode `full_fallback` and `fallback_reason` exactly
`apply_failed:new.py: file not found for diff`, with no file created — so the
mechanism that fires is the guard the amended A9 sentence names, not a snapshot
block, which would have made that text wrong. Pinned by test_diff_repair_apply
::test_new_file_creation_diff_falls_back_instead_of_creating. Resolved.

- R-0316 (Medium, F111 R13, a fallback reports a clean tree it cannot
  guarantee): `diff_repair_apply.apply_diff_repair` returns `files_modified=0`
  on every `apply_failed:` path, and its docstring states that the durable
  snapshot restores "every touched file when a hunk conflicts". Both hold only
  while the rollback SUCCEEDS. `source_apply._rollback_from_snapshot` catches
  OSError per entry and, when a blob cannot be read or a target cannot be
  written, appends `rollback_incomplete (N file(s)): …` to the errors and
  leaves those files half-restored; `result.success` is already False, so
  nothing else marks the difference. A caller then reads `applied=False,
  files_modified=0` and concludes the tree is untouched while it is not —
  the exact failure class this feature's Done criterion names. The information
  is not lost, the string rides in `errors`, but the summary field contradicts
  it and T003 will emit that field as per-round evidence. Reviewer-caused: the
  R13 step block ordered `files_modified=0` unconditionally, so this is a
  defect of the spec, not of the round that executed it faithfully. Fix
  direction: carry the rollback outcome as its own field, or refuse to zero
  `files_modified` when an error names `rollback_incomplete` — never by
  widening `_apply_hunks`. OPEN.

### R13 — PASS (2026-08-13)
Reviewed by the main session over 34319061..9a17fad2. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: the worker's permission layer refused `cmp` and refused every
command naming `.remedy-wt/`, so it declared the gap instead of faking a result
and the reviewer ran the comparison itself. `.remedy-wt/f111r13/BLOCK`,
`.agent/authored/f111-r13-1.md` and `.agent/last_block.md` are all three
byte-identical at 18502 bytes, sha256
f35907a250068b81c3c5b6216b2fcd68220674d997aadb40d3ce869fadc622f0;
`.remedy-wt/f111r13/PLAN` and `.agent/plan.md` identical at 2124 bytes. Both
authored appends landed verbatim and exactly once each. Scope: exactly the nine
ordered paths, `source_apply.py` untouched, R-0313 untouched, and no call site
added — `grep -rn diff_repair_apply packages/ apps/` returns one line, the
docstring pointer.

The all-or-nothing claim proved BY MUTATION, not by colour. In a disposable
worktree at HEAD the reviewer replaced the body of `_rollback_from_snapshot`
with an immediate `return` and re-ran the new test file:
`test_conflicting_hunk_falls_back_and_leaves_both_files_untouched` FAILED with
`assert b'LINE1\nline2\n' == b'line1\nline2\n'` while the other five passed. So
the first file really is written before the second hunk conflicts, and the
rollback really is what restores it — the test is load-bearing, not vacuously
green. Worktree removed and pruned before this verdict.

DECISION D6 was checked against behaviour rather than against its own prose: a
creation diff returns `apply_failed:new.py: file not found for diff` with a
non-empty snapshot id and no file created, so the guard the amended A9 sentence
names is the mechanism that actually fires.

Tests, each re-run by the reviewer: 54 for the three scoped files, 294 for
tests/docs/ (the docs-round gate this change set requires), 42 for the
golden-path canary. Markers: 1 D6 heading, 1 landed marker, `Done:` still 7 on
the file the round handed back. Caps: per-commit insertions
320/299/18/19/174/262/108, each under 500; `.agent/plan.md` 43 lines under the
50 cap; `.agent/handoff.md` 109 lines over the 60 cap and carrying the DECISION
D15 stated-cause line, which is the sanctioned shape. `git status --porcelain`
empty, one worktree, `0	0` against the remote. The handback stated C7's own
insertions as a bound rather than a count, twice and with two different bounds
(`≤148` and "at most 152"); both are true of the real 108 and neither is a
false claim, so it is noted here and not registered. One finding registered:
R-0316, and it is the reviewer's own spec defect, not the worker's.

Done: R-0313 — a blank context line stripped to "" no longer rejects an
otherwise valid diff. `normalize_diff_blank_context` gives the space back on
the RESPONSE side, where the hunk's declared budget still distinguishes body
from tail, and `diff_repair_response_to_patch` splits the normalised text.
`_apply_hunks` is unchanged, so the trailing-"" trap that would have made the
last hunk over-consume is structurally out of reach: the walk uses
`splitlines()`, which never produces the phantom. Verified at the R14 gate by
value, in both directions: `_apply_hunks('a\n\nb\n', diff)` returns None on the
raw stripped diff and 'a\n\nB\n' on the normalised one, and the normaliser is
byte-identity on a diff that needs no repair. Resolved — with the separator
defect it introduced registered separately as R-0317.

- R-0317 (Medium, F111 R14, the blank-context fix eats a file separator):
  `normalize_diff_blank_context` treats a bare "" as a blank context line
  whenever the open hunk still has an old AND a new line left to spend. A model
  that OVER-DECLARES its hunk counts — which this file already records as
  routine, in the D5 note on why the applier does not cross-check headers —
  leaves budget unspent at the end of its body, so the BLANK LINE SEPARATING
  TWO FILE SECTIONS is converted to " " and rides into
  `split_diff_by_path` as a trailing context line of the FIRST file. Measured
  at the R15 gate on the repository's own `DIFF_ONE_FILE` shape
  (`@@ -1,3 +1,3 @@` over a body spending two old and two new lines): the raw
  first section applies to 'import os\nvalue = 1\nmore = 3\n' and returns
  'import os\nvalue = 2\nmore = 3\n', while the normalised section returns
  None. So R14 closed R-0313 and opened a new instance of the same class — a
  valid multi-file answer rejected — for every first file whose hunk is not at
  end of file. Direction is SAFE (rejection, never corruption), and where the
  hunk IS at EOF both forms still apply identically, which is why no test
  caught it. The R14 worker found the contradiction while writing the ordered
  case 3, refused to assert a false property, implemented the production code
  unweakened and declared the deviation — correct on every count. Reviewer-
  caused: the R14 step block specified the budget rule and nothing else. Fix
  direction: a "" is body only when the next NON-BLANK line is also body — not
  a `---`/`+++`/`diff ` header and not end of input — so a separator and a
  trailing artifact both stay untouched. OPEN.

### R14 — PASS (2026-08-13)
Reviewed by the main session over 9a17fad2..48c6340e. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.remedy-wt/f111r14/BLOCK`, `.agent/authored/f111-r14-1.md` and
`.agent/last_block.md` are byte-identical at 17418 bytes, sha256
1113f75d07f29bd2bb1218a1f793a5917636c0dd55f2d0a3291bc4af8a9ddaaf, and
`.remedy-wt/f111r14/PLAN` matches `.agent/plan.md` at 2008 bytes. Markers:
`^Landed:` 0, `^Done:` 8, `^- R-0` 41, `^### R13 — PASS` 1. Scope: exactly the
eight ordered paths; `source_apply.py` and `diff_repair_apply.py` untouched.

R-0313 proved closed BY VALUE, both directions: `_apply_hunks('a\n\nb\n', …)`
returns None on the raw stripped diff and 'a\n\nB\n' on the normalised one, and
`normalize_diff_blank_context(DIFF_ONE_FILE)` is byte-identical to its input.
Tests re-run by the reviewer: 68 for the three diff-repair files, 55 for the
applier tier — unmoved, as the applier was not touched — and 42 for the
golden-path canary. Per-commit insertions 293/224/70/96/102/104, each under
500. `git status --porcelain` empty, one worktree, `0	0` against the remote.

The declared deviation is UPHELD and is the round's best work. The block
ordered a case-3 test asserting that
`DIFF_ONE_FILE + "\n" + <second section>` normalises to itself. The reviewer
re-measured it: it does not — the separator "" becomes " " — because
`DIFF_ONE_FILE` declares `@@ -1,3 +1,3 @@` over a body that spends only two old
and two new lines, so the hunk still has budget at the separator and the
ordered step-4 rule fires exactly as written. The worker implemented the
production code verbatim and unweakened, proved the ordered PROPERTY with a
first section whose header matches its body, wrote the measurement into that
test's docstring and escalated for a ruling instead of quietly changing either
side. That is the response the split workflow exists to produce.

Registered from it: R-0317. The reviewer measured its real cost — the raw
first section applies to a file that continues past the hunk and returns
'import os\nvalue = 2\nmore = 3\n', while the normalised section returns None —
so R14 closed one instance of "a valid answer rejected" and opened another.
Safe direction, no corruption, and invisible to any test whose first hunk sits
at end of file, which is why it survived a green round. It is the reviewer's
spec defect, not the worker's, and R15 repairs it.

Also noted, not registered: the `#` comment above the fall-through branch in
`diff_repair_response.py` writes `"\\ No newline at end of file"` with a
doubled backslash, where a comment needs one — `source_apply.py` writes it
correctly. The worker reported it and declined to add an unordered seventh
commit that would have broken the mandated C1-C6 item-status shape; that
judgement was right, and R15 carries the fix as an ordered item.

Done: R-0316 — the diff-repair seam no longer reports a clean tree it cannot
guarantee. `apply_diff_repair` reads the applicator's own error strings for
`rollback_incomplete`, carries the flag on `DiffRepairApplyResult`, and passes
`apply_result.files_modified` through instead of a hardcoded 0 when the restore
did not finish. Verified at the R16 gate by mutation, inside a disposable
worktree that was removed before the verdict: reverting that one expression to
`files_modified=0` fails exactly
`test_incomplete_rollback_reports_the_real_count_not_a_clean_tree` with
`assert 0 == 1`, so the test pins the behaviour rather than describing it. The
complete-rollback direction is pinned in the same round by the two assertions
added to `test_conflicting_hunk_falls_back_and_leaves_both_files_untouched`
(`rollback_incomplete is False`, `files_modified == 0`), so "always report a
count" cannot satisfy the pair. Noted, not registered: the count is the
applicator's total for the attempt, not the number of files whose restore
actually failed, so it over-reports rather than under-reports — the safe
direction for a seam whose whole purpose is to stop under-claiming damage.
Resolved.

Done: R-0317 — the blank-context repair no longer eats a file separator.
`_blank_line_is_hunk_body` scans forward from the blank for the first non-blank
entry and returns False at `---`, `+++`, `diff ` or end of input, so the
rewrite branch now needs the lookahead as well as the budget. Verified at the
R16 gate by value and by mutation, both re-run by the reviewer on this machine:
`normalize_diff_blank_context` is byte-identity on the two-file over-declared
shape, `split_diff_by_path` returns both sections, and the first section
applies to 'import os\nvalue = 1\nmore = 3\n' returning
'import os\nvalue = 2\nmore = 3\n' — where before the fix it returned None.
Deleting the `_blank_line_is_hunk_body(lines, index + 1)` conjunct in a
disposable worktree fails exactly the three tests R15 added for it and nothing
else. R-0313 stays closed under the same probe: 'a\n\nB\n'. Resolved.

### R15 — PASS (2026-08-13)
Reviewed by the main session over 48c6340e..d457219a. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport is
the PRIMARY cmp proof, not the digest fallback: the previous session's
scratchpad originals survived in `.remedy-wt/f111r15/`, and
`cmp .remedy-wt/f111r15/BLOCK .agent/authored/f111-r15-1.md`,
`cmp .remedy-wt/f111r15/BLOCK .agent/last_block.md` and
`cmp .remedy-wt/f111r15/PLAN .agent/plan.md` all exit 0. The three live_review
appends each occur exactly once in the file, in the ordered sequence. Markers
counted: nine `Done:` lines, 42 registered findings, one R14 gate heading, zero
unreviewed `Landed:` lines. Scope: exactly the nine ordered paths. Per-commit
insertions 341/266/81/40/49/91/92, each under 500. `git status --porcelain`
empty, one worktree, and 0 ahead and 0 behind the remote.

Tests re-run by the reviewer: 71 for the three diff-repair files (was 68), 55
for the applier tier — unmoved, as the applier was not touched — and 42 for the
golden-path canary. Both value probes reproduce exactly: the normaliser is
byte-identity on the two-file over-declared shape and its first section applies
to 'import os\nvalue = 2\nmore = 3\n', and R-0313 still yields 'a\n\nB\n'.
Mutation red-proofs ran inside a disposable git worktree, which was removed
before this verdict: deleting the `_blank_line_is_hunk_body` conjunct fails
exactly the three R-0317 tests, and reverting `files_modified` to a hardcoded 0
fails exactly the one R-0316 test. Both fixes are pinned, not merely present.

Both of the round's declared notes are upheld. The "Nine proofs" docstring line
was a sentence this round's own edits falsified, and correcting it inside a
file the block already ordered is right. The block did say "EXACTLY these eight
paths" over an enumeration of nine; the enumeration was operative and the
worker read it that way. That is a defect in the R15 block, which the reviewer
wrote, and it is noted here rather than registered because the round lost
nothing to it.

Also noted, not registered: R15 fixed R-0316 and R-0317 without the unreviewed-
fix marker §4.4 describes, because the R15 block itself gated that marker to
zero. The property §4.4 protects is that an unreviewed fix must never read as
resolved; leaving both entries at OPEN under-claims rather than over-claims, so
the property held, and the information the marker carries was in the handoff.
The rule stands unchanged for the next round that lands a fix ahead of its
verdict.

DECISION F111 D7 (2026-08-13, reviewer, authored for R16) — the repair-mode
knobs are keyword arguments on `run_builder_bridge_loop`, not a new config
module. The feature file asks for "Config: repair.diff_mode (default on),
context margin lines". This repository has no `packages/config`, and the loop
already takes its bounds as keyword arguments (`max_cycles`, `autonomy_level`),
so `diff_mode: bool = True` and `diff_margin_lines: int = 3` join them there.
Alternative considered and rejected for v1: a settings record read from disk,
which would add a new contract, a new file format and new tests to a slice
whose whole job is wiring. Reverse this decision by moving the two arguments
into a settings record and deleting this paragraph.

### R16 — PASS (2026-08-13)
Reviewed by the main session over d457219a..c0ed5dd1. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.agent/authored/f111-r16-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 18501 bytes, 316 lines, sha256
c361c291408ccbc09c051ccedc08859de0111c70c3a43189670cccd5945a880a, and no line
carries trailing whitespace. `.agent/plan.md` was compared against the TEXT-D
slice extracted from the committed authored file and is identical at 42 lines,
under the 50-line cap. Each authored text occurs exactly once in
`.agent/live_review.md`. Markers counted: eleven resolution paragraphs, 42
registered findings, one R15 gate heading, zero unreviewed-fix markers. Scope:
exactly the seven ordered paths. Per-commit insertions 316/287/82/70/142/102,
each under 500. `git status --porcelain` empty, one worktree, and 0 ahead and
0 behind the remote.

Tests re-run by the reviewer: 9 for the repair loop (was 6), 71 for the three
diff-repair files — unmoved — and 42 for the golden-path canary. The new
module-level `diff_repair` import was checked for fallout across the nine test
files that import `builder_bridge`: 137 passed, 1 skipped, no cycle. The
helper resolves to exactly two hits, the def at line 269 and the single call
site at line 412.

The reviewer ran an INDEPENDENT value probe the block did not order, on a
margin the tests never assert: driving the loop with `diff_margin_lines=1` over
a patch naming line 3 only returns `repair_mode` `diff` with `start_line` 2 and
`end_line` 4, and the carried text is post-apply SOURCE, not diff text. So the
margin argument is genuinely plumbed and not merely defaulted. The emitted
metadata was read directly and carries `cycle`, `mode`, `hunk_count`,
`total_chars` and `omitted` — counts only, no hunk text, exactly as the block's
deliberate absence claims.

A second reviewer mutation, also unordered, ran inside a disposable git
worktree that was removed before this verdict: flipping the `diff_mode` default
from True to False fails two of the three new tests. The feature file's
"Config: repair.diff_mode (default on)" is therefore pinned by the suite rather
than only asserted in prose. The worker's own ordered mutation is confirmed as
reported — neutralising the helper fails five tests, three of them pre-existing
ones that now traverse the default-on path, and the diff-mode-off test stays
green, which is the correct signature.

The declared handoff overage is upheld: 105 lines with the DECISION D15
stated-cause line naming the mandated content, no section dropped. The ordered
pre-C4 key-set check was performed and reported with its real result (32 hits,
none pinning an exact key set), which is the shape §4.8 asks for.

DECISION F111 D8 (2026-08-13, reviewer, authored for R17) — the apply-side diff
channel attaches INSIDE `run_builder_bridge`, as a branch in Stage 1 and Stage
3 only, and not as a second pipeline in the loop. The loop decodes the answer
and passes a `DiffRepairResponse` in; the bridge converts it with
`diff_repair_response_to_patch` into the same `StructuredPatch` shape Stage 1
already produces, so the approval gate, the intent creation, the test stage and
DECISION F111 D3's range source all keep exactly one implementation. Only the
applicator call differs. Alternatives considered and rejected: routing the diff
through `apply_structured_patch` after conversion, which would bypass
`apply_diff_repair`'s fence precheck and its named fallback reasons; and
running a parallel apply-and-test path in the loop, which would duplicate the
approval gate and the test stage. Reverse this decision by deleting the
`diff_response` argument and moving the branch into the loop.

DECISION F111 D9 (2026-08-13, reviewer, authored for R17) — "token actuals" are
recorded as PAYLOAD CHARACTER COUNTS in v1, never as token numbers. This
repository has no tokenizer: a search of `packages/` for a token-counting
function returns nothing, so any field named `tokens` would carry a fabricated
number, which is a block condition under §4.5. `select_repair_hunks` already
returns `total_chars`, and the R18 comparison test records
`diff_payload_chars` against `full_file_payload_chars`. The names say chars
because the values are chars. Alternative considered and rejected for v1:
adding a tokenizer dependency, which would put a new third-party contract into
a wiring slice. Reverse this decision by wiring a real tokenizer and renaming
the fields in the same commit — never renaming them alone.
