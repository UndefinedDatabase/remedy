── STEP T004 part 2b-i / F107 R10 — the size record and the missing docs ──
Goal:        The whole-file size comparison gets the writer its omissions
             sibling already has, and the `remedy job context` view shipped in
             R9 gets the documentation AGENTS.md requires (finding R-0279).
Bundle:      C1 save this block · C2 mirror it · C3 apply the six authored
             live_review pairs · C4 the size-comparison export + writer ·
             C5 its tests · C6 the user guide + the two index rows ·
             C7 plan · C8 handoff.
Change:      exactly these nine paths, nothing else:
             .agent/authored/f107-r10-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs targeting it ONLY)
             packages/orchestration/context_compiler.py (C4)
             tests/orchestration/test_context_compiler.py (C5, appended cases)
             docs/guides/job-context-view-user-guide-v0.md (new, C6)
             docs/README.md (C6, the IDXQ and IDXG pairs ONLY)
             .agent/plan.md (C7, full replacement by slice PLAN10)
             .agent/handoff.md (C8)

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase or revert.
 - Do-not-touch (docs/roadmap/features/T2_F107.md): prompt composition,
   retrieval/embedding approaches, repo-map features. Reject any TS parser
   dependency. Do NOT edit `docs/roadmap/ROADMAP.md`.
 - Do NOT change the SELECTION behaviour: `compile_task_context`, the tier
   assignment, the budget demotion and `compare_context_size` itself are frozen
   this round. C4 ADDS an export and a writer beside the existing ones and
   changes no existing return value.
 - Do NOT touch `apps/cli/commands/job_context_cmd.py`. Wiring the two records
   into a task's evidence directory is R11, not this round.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line or field that does not exist, STOP that item, do the
   safe thing, and DECLARE the correction in the handback — that is wanted
   behaviour, not a deviation. Four findings already record reviewer citation
   errors, two of them registered by the pairs in this very block.

Detail for C4 — packages/orchestration/context_compiler.py:
 - Add `CONTEXT_SIZE_FILENAME = "context_size.json"` directly beside
   `OMITTED_CONTEXT_FILENAME` (context_compiler.py:931), with the same kind of
   `#:` comment: a BARE FILENAME, never a path, because where the file sits is
   the caller's decision.
 - Add `export_context_size_comparison_json(comparison: ContextSizeComparison)
   -> dict[str, Any]` beside `compare_context_size` (context_compiler.py:1012),
   returning exactly the four fields `whole_file_tokens`, `compiled_tokens`,
   `saved_tokens`, `saved_ratio` as plain JSON types. NEVER round or clamp:
   `saved_tokens` may be negative and `saved_ratio` is 0.0 only when the
   baseline is 0 — the dataclass docstring at context_compiler.py:997 says why,
   and the export must not quietly disagree with it.
 - Add `write_context_size_comparison_json(comparison, target_path: Path) ->
   Path`, mirroring `write_omitted_context_json` (context_compiler.py:904)
   exactly: create the parent directory, `json.dumps(..., indent=2)` plus a
   trailing newline, write nowhere but where the caller pointed, return the
   path it wrote.
 - `write_omitted_context_json`'s docstring calls itself "The ONLY writing
   function in this module" (context_compiler.py:907). That sentence becomes
   FALSE with C4. Correct BOTH docstrings to say there are now two writers and
   that neither picks its own location. A stale absolute claim is worse than no
   claim: the next reader trusts it.
 - Add the three new names to the module docstring's Public API list
   (context_compiler.py:70-93) in the position that matches the code order.
   That list is how this repo's readers find the module's surface.

Detail for C5 — tests/orchestration/test_context_compiler.py (append only):
 Assert on REAL VALUES, never truthiness, and never re-derive an expected
 number with the same expression the code uses. Cover at least:
 1. the export carries the four real figures of a fixture comparison;
 2. a NEGATIVE `saved_tokens` survives the export unclamped;
 3. a zero baseline exports `saved_ratio` exactly 0.0 and no fabricated ratio;
 4. the writer creates a missing parent directory and the file round-trips
    through `json.loads` to the same four values;
 5. the writer returns the path it wrote, and `CONTEXT_SIZE_FILENAME` is
    `"context_size.json"` — the same shape as the existing
    `OMITTED_CONTEXT_FILENAME` case at test_context_compiler.py:963.

Detail for C6 — the docs, which discharge finding R-0279:
 - New `docs/guides/job-context-view-user-guide-v0.md`. Write it from the CODE,
   not from this block: read `apps/cli/commands/job_context_cmd.py` and state
   what it really does. It MUST cover: the invocation form; that the compiled
   scope is exactly the task's `inputs["flight"]["files_hint"]` and that job
   fence globs are deliberately NOT consulted; how `--task` resolves (planned id
   first, then task-UUID prefix, never a guess); the exit codes 0/1/2/3; the two
   candidate-listing branches (`git ls-files` and the filesystem-walk fallback)
   and that the output names which one ran; the `--json` field list; and that
   the command writes nothing to disk. Include one REAL invocation with its REAL
   output — run it, do not compose it by hand.
 - Register it in `docs/README.md` with the IDXQ and IDXG pairs below, which are
   the quick-find row and the guides-table row. Apply them by exact-string
   replacement; both are APPEND-shaped.

<<<BEGIN SLICE HDRFROM sha256=969938dbfbdb7a576cf8b0b68c4144ab60b0703e3266b46e8f18847bb5a1dc3d lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0277.
<<<END SLICE HDRFROM>>>
<<<BEGIN SLICE HDRTO sha256=9e0d720df7cbda0d59aa86945a0af066dba0d54226f23dfa52f9a9e15a94449f lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0280.
<<<END SLICE HDRTO>>>
<<<BEGIN SLICE LRF6FROM sha256=01fa41b1effb8b7b4a03162d9c5959138f8c0aec2276dac325c87139cd6e819d lines=1>>>
  reviewer confirms the applied value.
<<<END SLICE LRF6FROM>>>
<<<BEGIN SLICE LRF6TO sha256=32d977f8cf630468228f022938584ea20a6e72f00b633d8619fbd9a00b7a21df lines=29>>>
  reviewer confirms the applied value.
- R-0277 (Low, F107 R9): the R9 block's procedure step 1 ordered the saved bytes
  verified "against BLOCK_SHA256 below", but no such line exists inside the
  region that same step orders saved — `grep -n BLOCK_SHA256
  .agent/last_block.md` returns only the two prose references at lines 221 and
  242. The digest lives on line 277 of the reviewer original
  `.remedy-wt/f107-r9-1.block.md`, one line PAST the block body, so the gate was
  meetable only against an artifact the block never names. The worker met it
  there and DECLARED the correction, which is the wanted behaviour. Fixed
  forward: the R10 block states where the digest lives instead of saying
  "below". OPEN until a reviewer confirms the new wording landed.
- R-0278 (Medium, F107 R9): gate c ordered `grep -c 'Next free ID: R-0271'` -> 0
  over `.agent/live_review.md` while slice LRF5TO of the SAME block wrote that
  exact string into that same file, inside R-0276's body, which quotes the stale
  value it reports. The gate was unmeetable by construction; the worker reported
  the real 1 and edited nothing to move it, which is correct under the block's
  own "verify every claim" constraint. Seventh recurrence of the
  self-counting-gate class that docs/agents/planner_reviewer_prompt.md §3
  pre-emission checklist item 2 exists to stop, and the first inside F107. The
  standing fix is the one the R10 block uses: a zero-gate over a string any TO
  slice writes is scoped to the ANCHOR LINE (`^> Branch:.*R-0271`), never to the
  whole file. OPEN.
- R-0279 (Medium, F107 R9): `remedy job context` shipped as user-facing
  behaviour with no entry anywhere under `docs/` — no guide, no row in the
  `docs/README.md` index — because the R9 block's Change list was nine paths
  "and nothing else", none under docs/. AGENTS.md Documentation Updates orders
  docs when a feature introduces new behaviour, so the omission is the
  REVIEWER's: the worker flagged the absence in its handoff instead of widening
  scope, which is exactly right. R10 C6 fixes it. OPEN.
<<<END SLICE LRF6TO>>>
<<<BEGIN SLICE LR9FROM sha256=4abc6ab4f4f7930c510230c0938d9075412745eb79d67d9fd842c02cf679c3dc lines=1>>>
  advances 6acb3f04 -> 7acb406d.
<<<END SLICE LR9FROM>>>
<<<BEGIN SLICE LR9TO sha256=fc6bc0dbb0b2da266eda197605105566ecf511127e44be4b93be077e367633ed lines=38>>>
  advances 6acb3f04 -> 7acb406d.

- Reviewer gate on R9 (2026-08-12): PASS. Range 7acb406d..f86bda87 = eight
  commits touching exactly the nine paths the R9 block named. C1-C7 were made by
  the previous session's worker and C8 by this session's; the handoff says so and
  it changes nothing about the evidence. Transport by the PRIMARY shape: the
  reviewer original `.remedy-wt/f107-r9-1.block.md` survives at 277 lines, its
  first 17862 bytes `cmp` silent against BOTH `.agent/authored/f107-r9-1.md` and
  `.agent/last_block.md`, and all three sha256 to f8e42fd684fe2367… at 276 lines
  — the value the original's own trailer declares. All nine slice bodies
  recompute to their BEGIN-marker digests at their declared lengths (HDRFROM
  dfab3095… 1L, HDRTO 969938db… 1L, LRF5FROM 21a6a3f6… 1L, LRF5TO 21a8b66c… 23L,
  LR8FROM 686e2302… 1L, LR8TO 4894b692… 34L, LRDFROM 62450c77… 6L, LRDTO
  39b40890… 12L, PLAN9 33ad2144… 28L), and `sha256sum .agent/plan.md` returns
  that PLAN9 digest over 28 lines. Each pair was proven by ITS OWN shape rather
  than asserted: `git show --numstat 61adb419 -- .agent/live_review.md` reads
  `68  7`, the seven deletions being HDRFROM's 1 line plus LRDFROM's 6 — both
  REWRITES, whose FROM lines now occur 0x and whose TO lines occur 1x — while the
  two APPENDS keep their FROM exactly 1x and their 22 and 33 TO-only lines each
  occur exactly 1x among the 68 added lines, with 0 added lines belonging to no
  TO body. Every scoped gate was RE-RUN by this reviewer rather than read from
  the handback: 9 passed on the new CLI test module, 505 passed on the catalog
  and grouped-CLI suites, 42 passed on the canary, `ruff check` "All checks
  passed!", `git status --porcelain` empty, `git worktree list` the primary
  checkout alone, HEAD == origin/feature/f107-context-compiler-v2, and insertions
  per commit 276, 253, 68, 273, 19, 231, 12, 254 — each under 500. GATE h WAS
  RE-RUN, not read: with `REMEDY_DATA_DIR` pointed at the worker's scratch data
  root, `remedy job context 994eb8d1-… --task T001` reproduces the handoff's
  stdout line for line (164/24000 tokens; tier 1 src/payment_gateway.py full,
  tier 2 src/retry_policy.py full, tier 3 src/clock_source.py signatures;
  README.md and src/invoice_report.py omitted for distance), `--json` reproduces
  the same values, `--task T999` exits 3 with `Error: no task matches --task
  'T999'`, and a spot-check the block did not order — resolving the same task by
  its UUID prefix `52c783f1` — reaches the identical task. F107 HAS A CALLER and
  is no longer a library. All five declared deviations re-measured accurate, and
  TWO of them are reviewer errors, registered above as R-0277 and R-0278; the
  docs gap the worker flagged rather than silently fixed is R-0279.
  `LAST_REVIEWED_SHA` advances 7acb406d -> f86bda87.
<<<END SLICE LR9TO>>>
<<<BEGIN SLICE LRD2FROM sha256=c87e031cc573e191ef8e1a731979bb7492786f63ea6467c6d66dbb75db5d68ad lines=1>>>
not drift. Open findings 11 -> 10.
<<<END SLICE LRD2FROM>>>
<<<BEGIN SLICE LRD2TO sha256=7662036beb9d62537a5ab5098e4de5d3ad33c67eaa33177f8991ecf355676552 lines=14>>>
not drift. Open findings 11 -> 10.

Done: R-0275 — RESOLVED. The R8 handoff text that carried the wrong `218/328` no
longer exists on disk (C8 of R9 rewrote the file), and the class did not recur:
this reviewer re-measured every `+/-` cell of the R9 handoff against `git show
--numstat` and all eight agree — 276/0, 253/195, 68/7, 273/0, 17/0 plus 2/1,
231/0, 12/12 and C8's own 254/94 — with the insertion column, not a line count,
in every cell. Open findings 15 -> 14.

Done: R-0276 — RESOLVED. `.agent/live_review.md` line 8 read `Next free ID:
R-0277.` at f86bda87, measured line-scoped so that the finding's own quotation of
the stale string cannot pollute the count: `grep -c '^> Branch:.*Next free ID:
R-0271'` is 0 and the R-0277 form is 1. The one carrier that owns the ID sequence
is correct again, and this round allocates past it. Open findings 14 -> 13.
<<<END SLICE LRD2TO>>>
<<<BEGIN SLICE IDXQFROM sha256=8b420a66b19722a4161b7461cebccf9ef76b77631e6756c9ce8847ce0f0e17fa lines=1>>>
| job budget | [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | system |
<<<END SLICE IDXQFROM>>>
<<<BEGIN SLICE IDXQTO sha256=6876d1e0cc9c1cdc43341be7d3fc2bc6c9e0a527c16f217b0eff75ea2c4e3e8d lines=2>>>
| job budget | [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | system |
| job context | [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | guide |
<<<END SLICE IDXQTO>>>
<<<BEGIN SLICE IDXGFROM sha256=4e4f9bb99ed3ab282395666ddc036aff1cd9472585dc09b0334d1c23f5447c0a lines=1>>>
| [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | Running dogfood jobs *(overnight superseded)* |
<<<END SLICE IDXGFROM>>>
<<<BEGIN SLICE IDXGTO sha256=cca85dad51044213c14c229fd3d3e3202a4662c32663a609d183df2a38f22162 lines=2>>>
| [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | Running dogfood jobs *(overnight superseded)* |
| [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | What one task's compiled context carries and what was omitted |
<<<END SLICE IDXGTO>>>
<<<BEGIN SLICE PLAN10 sha256=fd7a81e44608c5a956071a996cc50a2eaa843f0464977a7c95993dac1b245c28 lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0280. R9 reviewed PASS at f86bda87.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R10 — T004 part 2b-i: the size comparison gets the writer its omissions
sibling already has (`write_context_size_comparison_json`), and the
`remedy job context` view shipped in R9 gets the docs AGENTS.md requires —
a user guide plus its two rows in the `docs/README.md` index (finding
R-0279). No behaviour of the compiler's selection changes this round.

## Next Steps
1. R11 — T004 part 2b-ii: the end-to-end fixture task solved by the fake
   provider with the compiled context as its JOB_CONTEXT segment, writing
   both records into the task's evidence directory.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md; the branch has no PR
   yet, it is created at closure and never merged in the same session.
<<<END SLICE PLAN10>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r10-1.md`. The expected
    digest is the BLOCK_SHA256 line that the reviewer original
    `.remedy-wt/f107-r10-1.block.md` carries as its LAST line — that trailer sits
    one line PAST the region you save, and is not part of the saved bytes
    (finding R-0277 exists because the R9 block said "below" instead of this).
    Verify BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the six pairs to their targets by exact-string replacement of the FROM
    body with the TO body, verifying each slice's sha256 BEFORE use. HDR is a
    REWRITE (FROM and TO are disjoint); LRF6, LR9, LRD2, IDXQ and IDXG are
    APPENDS (each TO literally contains its FROM). The first four target
    `.agent/live_review.md`, IDXQ and IDXG target `docs/README.md`. Commit C3
    alone — findings persist before any code moves.
 4. C4, C5, C6 in that order, each its own commit, self-review loop before each.
 5. Replace `.agent/plan.md` entirely with slice PLAN10; `cmp` and `sha256sum`
    against the marker. Commit C7.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` (≤60 lines, or a declared
    stated-cause overage per AGENTS.md D15) and commit C8. Push.
 7. Do NOT write a `Done:` line of your own. If something lands that a finding
    covers, write `Landed: R-XXXX — <one line>` and nothing else.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r10-1.md .agent/last_block.md` → exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Each of the thirteen slice bodies recomputes to its BEGIN-marker digest at
    its declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` → the deletion column is
    exactly 1, because HDR is the only REWRITE targeting that file;
    `git show --numstat <C3> -- docs/README.md` → deletion column exactly 0.
    Then, LINE-ANCHORED so no finding body that quotes a string can pollute a
    count (finding R-0278): against `.agent/live_review.md`,
    `grep -c '^> Branch:.*Next free ID: R-0280'` → 1;
    `grep -c '^> Branch:.*Next free ID: R-0277'` → 0;
    `grep -c '^- R-0277'` → 1; `grep -c '^- R-0278'` → 1; `grep -c '^- R-0279'`
    → 1; `grep -c '^Done:'` → 4; `grep -c '^Landed:'` → 0;
    `grep -c '^## Steps'` → 1; `grep -c '^<<<'` → 0 (also 0 in
    `.agent/plan.md`, `.agent/handoff.md` and `docs/README.md`).
 d. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → exit 0,
    and report the passed count (it was 55 before this round).
 e. `python3 -m pytest tests/cli/test_job_context_cmd.py -q` → exit 0, 9 passed.
 f. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed.
 g. Docs-round gate, because this change set includes `docs/`:
    `python3 -m pytest tests/docs/ -q` → exit 0, with the count.
 h. `python3 -m ruff check packages/orchestration/context_compiler.py
    tests/orchestration/test_context_compiler.py` → exit 0.
 i. PROBE, inside a disposable `git worktree` at HEAD and nowhere else: drop the
    trailing newline from `write_context_size_comparison_json`'s write, and
    report WHICH tests fail and how many, or report that none do. A green probe
    is a true answer about a gap in C5, not a failure — report it either way,
    then remove and prune the worktree.
 j. THE REAL RUN, and this one decides the round: in a scratch directory under
    the gitignored `.remedy-wt/`, compile a real fixture repo's context, call
    `write_context_size_comparison_json`, and paste the resulting JSON file
    VERBATIM into the handoff together with the `whole_file_tokens` and
    `compiled_tokens` figures it contains. A passing test is not this gate.
 k. `git status --porcelain` → empty; `git worktree list` → primary checkout
    alone; HEAD == origin/feature/f107-context-compiler-v2; insertions per
    commit, each < 500.
 l. `git diff --name-only f86bda87..HEAD` → exactly the nine paths of the Change
    list, nothing else.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C8, and every gate above with its real exit code and counted
value. Declare any deviation; a declared deviation costs nothing, an undeclared
one costs the round.
──────────────────────────────────────────────────────────────
