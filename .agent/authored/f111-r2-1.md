── STEP R2/~12 — F111 Diff-only repair ───────────────────────────────────────
Goal:        Record the R1 gate and DECISION F111 D1, amend the feature file
             with the seam D1 picks, and build T001's hunk selection helper
             with its unit tests.
Bundle:      C1 block save; C2 last_block mirror; C3 live_review append;
             C4 feature-file append; C5 T001 helper + tests; C6 plan rewrite;
             C7 handoff. Push after EVERY commit.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r2-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             docs/roadmap/features/T2_F111.md,
             packages/orchestration/diff_repair.py (new),
             tests/orchestration/test_diff_repair.py (new).
             Do NOT touch pingpong_loop.py, builder_bridge.py,
             repair_context.py, source_apply.py, review_scope.py or any other
             existing production file this round — T001 is a NEW pure module
             with no call sites yet; wiring is a later round.
Constraints: AGENTS.md in full. Apply authored slices by COPYING the verified
             scratch file; never retype or reflow authored text. Do NOT
             create a PR, do NOT merge, never touch main, never force-push.
             Never write a `Done:` line in live_review. Reuse, do not
             duplicate: `review_scope._parse_diff` already turns a unified
             diff into per-file line ranges and `source_apply._apply_hunks`
             is already a strict hunk applier — this round adds NEITHER a
             diff parser NOR a diff applier, and a new `@@` regex anywhere in
             the change set is a defect. Scratch stays under .remedy-wt/.

AUTHORED SLICES — already on disk, written by the reviewer:
  .remedy-wt/f111r2/LRG   sha256=acef0bc3f01616e7c6b05831d6262c12fa23bf0b32f8197d3690c42f427ab4a7  append to .agent/live_review.md
  .remedy-wt/f111r2/FF    sha256=81a907957dd70df10a37c84226d1047d903e3ff190e71be35c0217d82edc66a6  append to docs/roadmap/features/T2_F111.md
  .remedy-wt/f111r2/PLAN  sha256=c7982c61b653ec97632c2bec7f40608cd19901afa2028763f9d37aa14519c5f6  replaces .agent/plan.md
  .remedy-wt/f111r2/BLOCK = this entire step block, byte for byte

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is b0ab8e09.
   Verify all four scratch digests. Any mismatch => STOP and hand back.

1. C1 — `cp .remedy-wt/f111r2/BLOCK .agent/authored/f111-r2-1.md`; `cmp`
   silent. Commit: chore(f111): save the R2 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r2-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R2 block into last block   -> push

3. C3 — APPEND slice LRG to the END of .agent/live_review.md:
   `cat .remedy-wt/f111r2/LRG >> .agent/live_review.md`
   This is a PURE APPEND: the proof is
   `git show --numstat <C3> -- .agent/live_review.md` reading `51 0` — 51
   added, 0 deleted. A nonzero delete column means the file was rewritten
   instead of appended: STOP and hand back.
   Commit: chore(f111): record the R1 gate and DECISION D1   -> push

4. C4 — APPEND slice FF to the END of docs/roadmap/features/T2_F111.md:
   `cat .remedy-wt/f111r2/FF >> docs/roadmap/features/T2_F111.md`
   Proof: `git show --numstat <C4> -- docs/roadmap/features/T2_F111.md`
   reads `17 0`. Gate in this same commit's tree:
   `python3 -m pytest tests/docs/ -q` exit 0.
   Commit: chore(f111): amend the feature file with the D1 seam   -> push

5. C5 — T001. Create packages/orchestration/diff_repair.py, a PURE module
   with no imports from pingpong_loop, builder_bridge or source_apply.
   Put a one-line WHY comment directly above each definition (AGENTS.md
   Code Discoverability). Public API, exactly:

     @dataclass(frozen=True)
     class RepairHunk:
         path: str        # repo-relative, exactly as the caller gave it
         start_line: int  # 1-based inclusive, AFTER margin expansion
         end_line: int    # 1-based inclusive, AFTER margin expansion
         text: str        # the exact source lines, newline-joined

     @dataclass(frozen=True)
     class RepairHunkSelection:
         hunks: tuple[RepairHunk, ...]
         omitted: tuple[tuple[str, str], ...]  # (path, reason)
         total_chars: int

     def select_repair_hunks(
         repo_root: Path,
         changed_line_ranges: Mapping[str, Sequence[Sequence[int]]],
         *,
         margin_lines: int = 3,
         max_total_chars: int = 20000,
     ) -> RepairHunkSelection:

   Behaviour contract, each clause pinned by its own test:
   (1) Each [start, end] expands to [max(1, start - margin_lines),
       min(<last line>, end + margin_lines)] — always clamped, never out of
       bounds.
   (2) Within one file, expanded ranges that overlap OR are adjacent merge
       into a single hunk, so no source line is carried twice.
   (3) Hunks are sorted by (path, start_line) — deterministic output.
   (4) A file whose bytes contain a NUL or that fails UTF-8 decoding is
       omitted with reason "binary" and never raises.
   (5) A path that does not exist under repo_root is omitted with reason
       "missing".
   (6) Hunks are admitted in sorted order while total_chars stays within
       max_total_chars; anything not admitted is omitted with reason
       "budget". total_chars is the sum of the admitted hunks' text lengths
       and never exceeds the cap.
   (7) margin_lines=0 returns exactly the requested lines.
   (8) A path whose range list is empty is omitted with reason "no_ranges".

   Create tests/orchestration/test_diff_repair.py covering clauses 1-8, one
   test per clause minimum, plus a test asserting a hunk's `text` equals the
   exact source lines. Use bare `tmp_path` as repo_root — no `git init`, no
   fixtures beyond tmp_path, matching tests/orchestration/test_fences.py.
   Commit: feat(f111): add the repair hunk selection helper   -> push

6. C6 — `cp .remedy-wt/f111r2/PLAN .agent/plan.md`; `cmp` silent.
   Commit: chore(f111): rewrite the plan for R2   -> push

7. C7 — rewrite .agent/handoff.md yourself (your own text): <=60 lines,
   feature+round (F111 R2), branch, per-commit SHA table (C1-C7, C7
   self-referential), changed-files table, the real gate results below
   (command + real exit code + counted value), open findings 22 / next free
   ID R-0298, an item-status table over C1-C7 with each item exactly once,
   and next expected action: R3 = wire the selected hunks into the repair
   context. Commit: chore(f111): rewrite the handoff for R2   -> push

MUTATION RED-PROOF (run AFTER C7, inside a disposable worktree ONLY — never
in the primary checkout, AGENTS.md/protocol G5):
  `git worktree add .remedy-wt/r2mut HEAD`
  In that worktree only, change the clamp in select_repair_hunks from
  `max(1, start - margin_lines)` to `start - margin_lines`, then run
  `python3 -m pytest tests/orchestration/test_diff_repair.py -q` there.
  The start-of-file clamp test MUST go RED. Record the real exit code and
  the failing test id. Then `git worktree remove --force .remedy-wt/r2mut`
  and `git worktree prune`. Report `git worktree list` afterwards and
  confirm `git status --porcelain` in the primary checkout is still empty.
  If the mutation does NOT go red, say so plainly — that is a real finding
  about the test, not something to massage.

Done when (record command + real exit code + counted value; never the word
"green"):
  a. four scratch digests match; cmp BLOCK vs authored silent; cmp authored
     vs last_block silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `51 0`
     `git show --numstat <C4> -- docs/roadmap/features/T2_F111.md` -> `17 0`
  c. `grep -c '^### DECISION F111 D1' .agent/live_review.md` -> 1
     `grep -c '^### R1 — PASS' .agent/live_review.md` -> 1
     `grep -c '^- R-0' .agent/live_review.md` -> 22 (unchanged; this round
     registers no finding)
     `grep -c '^Done:' .agent/live_review.md` -> 0 (exit 1 is the pass)
  d. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0;
     report the number of tests collected and passed.
  e. `python3 -m pytest tests/docs/ -q` -> exit 0 (run at C4, rerun at HEAD)
  f. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0 (canary)
  g. `rg -c '@@' packages/orchestration/diff_repair.py` -> 0 (exit 1 is the
     pass: this round adds no diff parser)
     `rg -n 'import' packages/orchestration/diff_repair.py` -> must NOT name
     pingpong_loop, builder_bridge, source_apply or review_scope
  h. mutation red-proof result as specified above, plus `git worktree list`
     and `git status --porcelain` empty.
  i. `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0`; per-commit insertions each < 500.
Handback:    completion report (tables + raw gate results) and
             .agent/handoff.md rewritten as C7. Do not merge, do not open a
             PR, do not touch .agent/candidates.md or .agent/decisions.md.

<<<BEGIN SLICE LRG sha256=acef0bc3f01616e7c6b05831d6262c12fa23bf0b32f8197d3690c42f427ab4a7 lines=51>>>

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
<<<END SLICE LRG>>>

<<<BEGIN SLICE FF sha256=81a907957dd70df10a37c84226d1047d903e3ff190e71be35c0217d82edc66a6 lines=17>>>

## Built State — scope amendment (DECISION F111 D1, 2026-08-13)
The repair loop this feature changes is the BOUNDED REPAIR LOOP in
`packages/orchestration/builder_bridge.py` (`run_bounded_repair_loop`), whose
cycle is build → bridge → test → repair-context → rebuild. Its bridge already
parses a `BuilderOutput` into a `StructuredPatch` and applies it through
`apply_structured_patch`, so the response-side diff channel attaches there and
flows through the existing fenced applicator exactly as "How it fits"
requires. The prompt-side hunk selection attaches to the repair context built
by `packages/orchestration/repair_context.py`.
`packages/orchestration/pingpong_loop.py` is explicitly NOT in scope: its
builder is an agentic CLI that edits the staging tree itself, `BuilderOutput`
carries no patch field on that path, and no applicator is invoked there.
Giving it a diff-shaped response would require a new provider contract and a
change to applicator semantics, both listed under Do not touch. Remedy
deliberately does not route ping-pong repairs through the diff channel in v1
for that reason.
<<<END SLICE FF>>>

<<<BEGIN SLICE PLAN sha256=c7982c61b653ec97632c2bec7f40608cd19901afa2028763f9d37aa14519c5f6 lines=38>>>
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0298. Last reviewed SHA: b0ab8e09 (R1 PASS).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R2 — record the R1 gate and DECISION F111 D1, amend the feature file with the
seam the DECISION picks, and build T001: the hunk selection helper in the new
`packages/orchestration/diff_repair.py` with unit tests. D1 settles that the
response side attaches to `builder_bridge` (which already applies a parsed
patch through the fenced applicator) and the prompt side to
`repair_context`; `pingpong_loop` is out of scope and the feature file now
says so.

## Next Steps
1. T001 rest — wire the selected hunks into the repair context the bounded
   repair loop feeds to the next build call.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback.
3. T003 — mode and token evidence per repair round, plus a fixture comparison
   recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate must compare base against branch, never read absolute
  green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, not duplicated — a third `@@` regex in the tree would be a
  finding.
<<<END SLICE PLAN>>>
