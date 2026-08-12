── STEP R1/~12 — F111 Diff-only repair ───────────────────────────────────────
Goal:        Claim F111, reset the session state files, and carry the 22 open
             F107 findings forward. No production code this round.
Bundle:      Branch creation; C1 authored-block save; C2 last_block mirror;
             C3 STATUS claim; C4 live_review reset; C5 plan rewrite;
             C6 context rewrite; C7 handoff rewrite; push after EVERY commit.
Change:      EXACTLY these paths and nothing else:
             docs/roadmap/STATUS.md (one line, SFROM->STO below),
             .agent/authored/f111-r1-1.md (new),
             .agent/last_block.md, .agent/live_review.md,
             .agent/plan.md, .agent/context.md,
             .agent/handoff.md (your handback rewrite).
             Do NOT touch .agent/candidates.md (already empty, verified by the
             reviewer), .agent/decisions.md, or any file under packages/,
             apps/ or tests/.
Constraints: AGENTS.md in full — self-review loop before every commit, small
             commits, no leading-slash tokens or absolute paths in commit
             subjects. Do NOT create a PR. Do NOT merge. Never touch main.
             Never write a `Done:` line in live_review (reviewer-only text).
             Never force-push. Apply every authored slice by COPYING the
             verified scratch file — never retype authored text, never
             reflow it. If a sha256 does not match, STOP and hand back the
             mismatch. Scratch stays under .remedy-wt/ and is never
             committed.

AUTHORED SLICES — already on disk, written by the reviewer:
  .remedy-wt/f111r1/SFROM  sha256=6c498f9cda12cfb5ba8f4665570575d9e9f7d9cbc49b55df406056b7933ca307  lines=1
  .remedy-wt/f111r1/STO    sha256=ee7930206fc3754b459dfdbd02116aea300e61598604e0946e5aa26ae63e6fc2  lines=1
  .remedy-wt/f111r1/LR     sha256=1e9458ff50519853258df7789fd48d5a93e2351e98e089c0e11c901bf10fde18  lines=111
  .remedy-wt/f111r1/PLAN   sha256=b2bf03236f9a1b5e93c230c49120363d41ca8d44ab93ea587e58f351ae86a030  lines=37
  .remedy-wt/f111r1/CTX    sha256=3994fc02270c2457cbf3981c083f5ded75e7b8b3ce48fc27f9c9acd704fdc9d8  lines=45
  .remedy-wt/f111r1/BLOCK  = this entire step block, byte for byte

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions. `git status --porcelain` empty; `git branch --show-current`
   is main; `git log -1 --format=%h` is 4e0b762e. If any differs, STOP and
   hand back — do not "fix" it. Then verify all six scratch digests with
   `sha256sum -c` style comparison against the table above. Any mismatch =>
   STOP. Then: `git checkout -b feature/f111-diff-only-repair`

1. C1 — `cp .remedy-wt/f111r1/BLOCK .agent/authored/f111-r1-1.md`, then
   `cmp .remedy-wt/f111r1/BLOCK .agent/authored/f111-r1-1.md` (must be
   silent, exit 0). Commit: chore(f111): save the R1 claim step block
   verbatim   -> push

2. C2 — `cp .agent/authored/f111-r1-1.md .agent/last_block.md`, then
   `cmp .agent/authored/f111-r1-1.md .agent/last_block.md` silent.
   Commit: chore(f111): mirror the R1 block into last block   -> push

3. C3 — STATUS claim, REWRITE shape (SFROM and STO are disjoint single
   lines). In docs/roadmap/STATUS.md replace the single line whose bytes
   equal SFROM with the bytes of STO. Apply from the scratch files, not by
   retyping. Proofs, all recorded: SFROM 0x and STO 1x in the file after the
   edit, and `git show --numstat HEAD -- docs/roadmap/STATUS.md` reads `1 1`.
   Gate in this same commit's tree: `python3 -m pytest tests/docs/ -q`
   exit 0. Commit: chore(f111): claim F111 in the ledger   -> push

4. C4 — `cp .remedy-wt/f111r1/LR .agent/live_review.md`, then `cmp` silent.
   This reset carries the 22 open F107 findings and sets Next free ID
   R-0298. Commit: chore(f111): reset live review for F111   -> push

5. C5 — `cp .remedy-wt/f111r1/PLAN .agent/plan.md`, then `cmp` silent.
   Commit: chore(f111): rewrite the plan for F111   -> push

6. C6 — `cp .remedy-wt/f111r1/CTX .agent/context.md`, then `cmp` silent.
   Commit: chore(f111): rewrite the context for F111   -> push

7. C7 — rewrite .agent/handoff.md YOURSELF (your own text, not authored):
   <=60 lines, containing feature+round (F111 R1), branch, a per-commit SHA
   table (C1-C7; C7 marks itself self-referential), a changed-files table,
   the real gate results from "Done when" below (command + real exit code +
   the counted value, no verdict words), the open-findings count (22) with
   next free ID R-0298, an item-status table over C1-C7 with every item
   present exactly once, and next expected action: R2 = the repair-path
   DECISION plus T001 hunk selection.
   Commit: chore(f111): rewrite the handoff for R1   -> push

Done when (run each; record the command, its real exit code, and the counted
value — never the word "green"):
  a. sha256sum of each of the six scratch files equals the table above;
     cmp BLOCK vs .agent/authored/f111-r1-1.md silent; cmp authored vs
     .agent/last_block.md silent.
  b. `grep -c -F -x -- '- [~] F111 — Diff-only repair' docs/roadmap/STATUS.md`
     -> 1
     `grep -c -F -x -- '- [ ] F111 — Diff-only repair' docs/roadmap/STATUS.md`
     -> 0 (grep exit 1 IS the pass here)
     `git show --numstat <C3> -- docs/roadmap/STATUS.md` -> `1 1`
  c. cmp silent for each: live_review vs LR, plan vs PLAN, context vs CTX.
  d. `grep -c '^## Steps' .agent/live_review.md` -> 1
     `grep -c '^- R-0' .agent/live_review.md` -> 22
     `grep -c '^<<<'` -> 0 on EACH of .agent/live_review.md, .agent/plan.md,
     .agent/context.md, .agent/handoff.md, docs/roadmap/STATUS.md
     (grep exit 1 is the pass; the authored file and last_block are NOT
     counted — they legitimately carry the block's own text)
     `wc -l < .agent/plan.md` -> 37 (cap 50)
     `wc -l < .agent/context.md` -> 45
  e. `python3 -m pytest tests/docs/ -q` -> exit 0 (run at C3, rerun at HEAD)
  f. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0 (canary)
  g. `git status --porcelain` -> empty output
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0`
  h. per-commit insertions from `git log --numstat`: report each; each must
     be < 500. The single-file .agent state rewrites are exempt by AGENTS.md
     DECISION F104 D1 but report their numbers anyway.
Handback:    completion report in your final message (tables + the raw gate
             results above) and .agent/handoff.md rewritten as C7. Do not
             merge, do not open a PR, do not touch .agent/decisions.md or
             .agent/candidates.md this round.

<<<BEGIN SLICE SFROM sha256=6c498f9cda12cfb5ba8f4665570575d9e9f7d9cbc49b55df406056b7933ca307 lines=1>>>
- [ ] F111 — Diff-only repair
<<<END SLICE SFROM>>>

<<<BEGIN SLICE STO sha256=ee7930206fc3754b459dfdbd02116aea300e61598604e0946e5aa26ae63e6fc2 lines=1>>>
- [~] F111 — Diff-only repair
<<<END SLICE STO>>>

<<<BEGIN SLICE LR sha256=1e9458ff50519853258df7789fd48d5a93e2351e98e089c0e11c901bf10fde18 lines=111>>>
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
<<<END SLICE LR>>>

<<<BEGIN SLICE PLAN sha256=b2bf03236f9a1b5e93c230c49120363d41ca8d44ab93ea587e58f351ae86a030 lines=37>>>
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0298. Last reviewed SHA: none yet (R1 in flight).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R1 — claim F111, reset the session state files, and carry the 22 open F107
findings forward. No production code this round: which repair path owns the
response-side diff channel is not yet settled, and R2 opens with that
DECISION rather than guessing.

## Next Steps
1. R2 — the repair-path DECISION, its feature-file amendment, and T001: the
   hunk selection helper plus unit tests.
2. T002 — response schema, fence pre-check, strict apply with conflict
   fallback.
3. T003 — wiring into repair rounds, mode and token evidence, a fixture
   comparison recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The ping-pong repair round's builder is an agentic CLI that edits staging
  itself: `BuilderOutput` carries no patch field and `apply_structured_patch`
  is never called from `pingpong_loop.py`. The prompt-side saving is
  reachable there; the response-side diff channel is not. R2 settles this as
  a recorded DECISION, never as a silent re-plan.
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate must compare base against branch, not read absolute
  green.
<<<END SLICE PLAN>>>

<<<BEGIN SLICE CTX sha256=3994fc02270c2457cbf3981c083f5ded75e7b8b3ce48fc27f9c9acd704fdc9d8 lines=45>>>
# Context — F111 Diff-only repair

## Active Branch
feature/f111-diff-only-repair, cut from main at 4e0b762e after PR #193 was
merged at the Open PR Gate. F111 is claimed `[~]` under Rule A5 as the first
`[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use, Tier 2).

## Scope
In: what a repair round SENDS and ACCEPTS — a hunk selection helper
(line-range slicing with a configurable context margin), a versioned
unified-diff response schema, a fence pre-check before any apply, strict
apply with an all-or-nothing conflict fallback to the full-file round, and
per-round mode and token evidence. Tests under
tests/orchestration/test_diff_repair.py.

Out, per the feature file's Do-not-touch: repair round counts and policy,
applicator semantics, and session resume. No fuzzy diff application — v1
requires exact context matches, and no implementation may shell out to
`patch` or `git apply` with fuzz enabled. Deletions stay on the full-file
path in v1; new-file creation inside a diff is allowed if the path passes
fences.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/, and production
  code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- A round pushes after EVERY commit, not once at its last step (R-0289).
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable
  git worktree, so resource safety stays intact and no background pytest
  process is ever left running.
- Build on what exists, do not duplicate it: `review_scope._parse_diff`
  already parses a unified diff into per-file new-file line ranges, and
  `source_apply._apply_hunks` is already a strict, non-fuzzy hunk applier
  that returns None on any context mismatch.

## Steps
R1 claim and state reset → R2 repair-path DECISION plus T001 hunk selection →
T002 response schema, fence pre-check and apply fallback → T003 wiring, mode
and token evidence → integration gate → closure.
<<<END SLICE CTX>>>
