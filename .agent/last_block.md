── STEP R19/20 — F107 Context compiler v2 ─────────────
Goal:        Persist the R18 gate and two new findings, resolve R-0291 and
             R-0292, close the third path of the unparseable blind spot
             (R-0293), and write the feature file's `## Built State` section,
             which closure precondition 4 requires and which does not exist.
Bundle:      C1 save block · C2 mirror · C3 gate, findings and resolutions
             persist FIRST · C4 the R-0293 repair plus its test · C5 the
             Built State section · C6 plan and handoff.
Change:      `.agent/authored/f107-r19-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `packages/orchestration/context_compiler.py` ·
             `tests/orchestration/test_context_compiler.py` ·
             `docs/roadmap/features/T2_F107.md` · `.agent/plan.md` ·
             `.agent/handoff.md`. Eight paths, nothing else. No `apps/`, no
             `pingpong_loop.py`, no README.md, no STATUS.md, no
             `.agent/decisions.md`.
Constraints: AGENTS.md in full. Insertions per commit under 500. Commit
             subjects carry no leading-slash tokens and no absolute paths.
             Push after every commit. Do NOT touch `docs/roadmap/ROADMAP.md`.
             Do NOT edit the module docstring: its tier paragraph already
             states the unparseable rule for every non-tier-1 path, and after
             C4 that sentence is true of all three paths rather than two.
Done when:   gates A-J below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content that caused it, per AGENTS.md DECISION D15).

C1 — the block you are executing was handed to you as
`.remedy-wt/f107-r19-1.block.md`. Copy it, do not retype it:
`cp .remedy-wt/f107-r19-1.block.md .agent/authored/f107-r19-1.md`, then
`cmp .remedy-wt/f107-r19-1.block.md .agent/authored/f107-r19-1.md` (silent,
exit 0). Record `wc -l` and `sha256sum` of the saved file. Commit alone, push:
  chore(f107): save the R19 step block verbatim

C2 — `cp .agent/authored/f107-r19-1.md .agent/last_block.md`, then
`cmp .agent/authored/f107-r19-1.md .agent/last_block.md` (silent, exit 0).
Commit alone, then push:
  chore(f107): mirror the R19 block into last block

C3 — GATE AND FINDINGS PERSIST FIRST (planner_reviewer_prompt.md §4.4)
PAIR_HDR is a REWRITE. In `.agent/live_review.md` replace the one line:
<<<BEGIN PAIR_HDR_FROM>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0293.
<<<END PAIR_HDR_FROM>>>
<<<BEGIN PAIR_HDR_TO>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0295.
<<<END PAIR_HDR_TO>>>

PAIR_LRF is an APPEND: the TO's first line IS the FROM, the last line of the
R-0292 entry. Everything after that first line is new text inserted directly
beneath it, still inside the `## Findings` list.
<<<BEGIN PAIR_LRF_FROM>>>
  not bar the repair.
<<<END PAIR_LRF_FROM>>>
<<<BEGIN PAIR_LRF_TO>>>
  not bar the repair.
- R-0293 (Medium, F107 R19, found at the R18 gate by probing the code the R18
  block did not name): the unparseable blind spot R-0292 recorded lives in
  THREE selector paths, and R18 closed two. The budget path — phase A of
  `compile_task_context`, `packages/orchestration/context_compiler.py:866-880`
  — demotes the largest FULL tier-2 file to signatures, calls
  `_signature_render_text`, and appends only an `OMISSION_REASON_BUDGET` /
  `_OUTCOME_SIGNATURES` record. When that file cannot be parsed, its signature
  rendering is `""` exactly as in R-0292, and the record blames the budget for
  a blank the budget did not cause: the file would have rendered empty under an
  infinite budget too. Reachable, and probed rather than argued — a root with
  `app.py` (tier 1, padded) importing `broken.py` (tier 2, small, `def broken(:`)
  compiled at a budget one token under the unconstrained total puts
  `('broken.py', 2, 'signatures', 0)` in `included` with exactly one record,
  `('broken.py', 2, 'budget', 'signatures')`, and no `unparseable` record. The
  same reviewer-side omission produced this gap and R-0292's repair scope: the
  R18 block named the tier-2 over-cap path and the tier-3 path from a reading
  of the module, without enumerating every call site that renders signatures.
  Fixed in THIS round, on the same ground R-0292 was: F107's own module against
  F107's own Edge-cases clause.
- R-0294 (Low, F107 R19, reviewer-side process defect): the R18 block was
  emitted without the §3 pre-emission checklist being run on its final bytes,
  and two of the seven items caught it after the fact rather than before.
  Item 1, size: the block is 407 lines against the cap of 400 (DECISION F105
  D5), so the worker had to apply an oversize block byte for byte and declare
  gate B RED on a round that did nothing wrong. Item 2, no self-counting gate:
  gate C ordered `Next free ID: R-0290` to be 0x in `.agent/live_review.md`
  while the block's own PAIR_LRG_TO writes that string into that same file at
  line 905, quoting the R17 gate's own marker as evidence — unmeetable by
  construction, and the sixth recurrence of that item's class across F104,
  F105 and F107. Neither cost a repair round, because the worker reported both
  RED honestly instead of massaging a number; that honesty is what kept a
  process defect from becoming a data defect. Registered against the reviewer
  role, not the worker. Forward-looking fix, already applied to THIS block:
  count the lines and re-read every zero-gate against every TO in the same
  block before emission, mechanically, on the final bytes.
<<<END PAIR_LRF_TO>>>

PAIR_LRG is an APPEND: the TO's first line IS the FROM, the last line of the
R17 gate entry. The new gate entry goes directly beneath it.
<<<BEGIN PAIR_LRG_FROM>>>
  `LAST_REVIEWED_SHA` advances 5c808a59 -> 54d05e37.
<<<END PAIR_LRG_FROM>>>
<<<BEGIN PAIR_LRG_TO>>>
  `LAST_REVIEWED_SHA` advances 5c808a59 -> 54d05e37.
- Reviewer gate on R18 (2026-08-12): PASS. Range `54d05e37..6e1970c4` = seven
  commits over the ten paths the R18 Change line names and no others; `git diff
  --numstat` reads 407/0, 381/259, 113/1, 33/6 and 70/0, 3/2 and 1/1, 54/0,
  23/19 and 113/124, so every commit's insertions stand far under 500.
  Transport, shape stated because it is NOT the primary one: no reviewer
  scratch original for R18 survives — `.remedy-wt/` holds F105-era block files
  only — and the saved block carries no BEGIN-marker digest, so neither the
  cmp-against-scratchpad proof nor the §4.9 digest fallback was available to
  this reviewer. What IS proved: `.agent/authored/f107-r18-1.md` and
  `.agent/last_block.md` are byte-identical at 407 lines, both hashing to
  6d1ea116f1f33c97682e5cf26267ef28304c4b7c1bb64a520763d9f22425dd39, and this
  reviewer read the saved block against the disk item by item rather than
  trusting the handback. Two gates were RED and are accepted as declared, both
  now registered as R-0294: the block's 407 lines against the 400 cap, and gate
  C's first clause, whose string the block's own gate text writes at line 905.
  The append shapes are exact: C3 adds 113 and removes 1, and PAIR_LRF_TO's 79
  TO-only lines plus PAIR_LRG_TO's 33 plus the one-line header rewrite account
  for all 113, leaving no stray. Every remaining gate was RE-RUN here, not
  read: `test_context_compiler.py` collects 64 and passes, up from the 61 the
  R17 gate recorded, `test_context_compiler_e2e.py` and
  `tests/cli/test_job_context_cmd.py` pass 15 together, `tests/docs/` passes
  294, the canary `python3 -m pytest tests/cli/test_golden_path.py -q` returns
  42 passed in 19.66s, and `python3 -m ruff check` over the two changed Python
  files returns "All checks passed!". The vocabulary edits hold on disk: the
  old reason list is 0x and the new one 1x in the feature file, the old guide
  clause is 0x and the new one 1x, DECISION F107 D1 and D2 each occur once with
  D1's heading immediately after its anchor at `.agent/decisions.md:4248-4250`,
  and `^<<<` is 0 across all eight touched files. `git status --porcelain` is
  empty, `git worktree list` shows the primary checkout alone, `git rev-list
  --left-right --count` against the remote is `0 0`, and `gh pr list --state
  open` returns an empty list. R-0291 and R-0292 are resolved below. One new
  code finding came out of this gate rather than out of the handback: probing
  the selector's third signature path showed the R18 repair reached two of
  three, which is R-0293 above, so the registered count returns to 20 open.
  `LAST_REVIEWED_SHA` advances 54d05e37 -> 6e1970c4.
<<<END PAIR_LRG_TO>>>

PAIR_DONE is an APPEND at the END of the file: the TO's first line IS the FROM,
which is the current last line of `.agent/live_review.md`. The two resolutions
go directly beneath it, each separated by one blank line.
<<<BEGIN PAIR_DONE_FROM>>>
findings 18 -> 17.
<<<END PAIR_DONE_FROM>>>
<<<BEGIN PAIR_DONE_TO>>>
findings 18 -> 17.

Done: R-0291 — RESOLVED. The finding asked for the operator-visible record
§4.7 requires of a spec deviation, not for the deferred code. That record is on
disk: `.agent/decisions.md:4250` carries `## DECISION F107 D1 (2026-08-12) —
two Design bullets are DEFERRED, on the record`, naming both gaps — no
production caller for `register_compiled_context_segment`, and a CLI tier 1
that is the files_hint alone — with the chosen option, the two alternatives
that were rejected and the concrete reversal condition. This reviewer read the
committed text rather than the handback's summary of it, and confirmed the
heading sits immediately after its anchor with one blank line between. The
deferral is now visible where an operator looks instead of only in a module
docstring. Open findings 20 -> 19.

Done: R-0292 — RESOLVED for the two paths it names, with the third split out as
R-0293 rather than folded in silently. `OMISSION_REASON_UNPARSEABLE` exists
beside the other four constants; the tier-2 over-cap path and the tier-3 path
both obtain the `FileSignatures` object once, estimate from its own rendered
lines, and append an `unparseable` record when `parse_failed` is set, while
tier 1 stays exempt. Three tests pin exactly that — the tier-3 file carried
empty with one record, the over-cap tier-2 file carrying both `size` and
`unparseable` and no others, and the unparseable tier-1 file carried whole with
none — and the suite this reviewer re-ran collects 64 where it collected 61.
The fifth reason reached the vocabulary test, the feature file's Design
enumeration and the user guide in the same round as the code, so no reader
meets a word the plan does not carry. Open findings 19 -> 18.
<<<END PAIR_DONE_TO>>>
Commit, then push:
  chore(f107): record the R18 gate, R-0293, R-0294 and two resolutions

C4 — the R-0293 repair, in `packages/orchestration/context_compiler.py` and
`tests/orchestration/test_context_compiler.py`. You write this code.

1. In phase A of `compile_task_context` (the `while` loop that demotes the
   largest full tier-2 file, currently around lines 866-880), stop rendering
   through `_signature_render_text`. Obtain the `FileSignatures` object once
   via `extract_file_signatures(root, victim, line_cap)`, build the rendering
   from its `.lines` for the estimate exactly as the tier-2 and tier-3 paths
   now do, and when `parse_failed` is True append, AFTER the existing budget
   record:
       OmissionRecord(victim, TIER_NEIGHBOR, OMISSION_REASON_UNPARSEABLE, _OUTCOME_SIGNATURES)
   The file still stays in `chosen` with its `"signatures"` rendering. The
   existing budget record is unchanged and still appended for every demotion.
2. Do not delete `_signature_render_text`: `render_compiled_context_text` still
   calls it, and its behaviour must not change.
3. Add exactly ONE test to `tests/orchestration/test_context_compiler.py`,
   placed beside the three unparseable tests added in R18 and named for what it
   pins — that a budget-demoted tier-2 file which cannot be parsed carries both
   records. Build the fixture with the existing `_write_tree` idiom: a tier-1
   `app.py` that imports a tier-2 `broken.py` whose body is `def broken(:` and
   which is the largest full tier-2 file, plus enough padding in `app.py` that
   the demotion of `broken.py` alone brings the total under the budget. Take
   the budget the way `test_budget_demotes_the_largest_tier_two_file_first`
   does — compile once unconstrained, then pass
   `token_budget=unconstrained.estimated_tokens - 1` — so no hand-picked
   number can drift. Assert that `broken.py` is in `included` with rendering
   `"signatures"`, and that the records for that path are exactly the two,
   `("budget", "signatures")` and `("unparseable", "signatures")`, in whatever
   order the selector appends them.

Run, and record the real output:
  python3 -m pytest tests/orchestration/test_context_compiler.py -q
  python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q
  python3 -m ruff check packages/orchestration/context_compiler.py tests/orchestration/test_context_compiler.py
Commit, then push:
  fix(f107): record an unparseable omission on the budget demotion path

C5 — the Built State section. PAIR_BS is an APPEND at the END of
`docs/roadmap/features/T2_F107.md`: the TO's first line IS the FROM, which is
the file's current last line. The section goes directly beneath it.
<<<BEGIN PAIR_BS_FROM>>>
tests/orchestration/test_context_compiler.py.
<<<END PAIR_BS_FROM>>>
<<<BEGIN PAIR_BS_TO>>>
tests/orchestration/test_context_compiler.py.

## Built State (R1-R19, branch feature/f107-context-compiler-v2)

Built and reviewed as `packages/orchestration/context_compiler.py`, one module
carrying four layers, plus one CLI view. Stdlib only: no TS parser dependency
was added, as the orchestrator brief requires.

- **T001 — import-neighbor graphs.** `python_import_neighbors` uses `ast`:
  absolute and relative imports resolved against the importing file's package,
  and `from pkg import name` disambiguated between name-is-a-module and
  name-is-a-symbol by looking at the tree on disk.
  `typescript_import_neighbors` is a line-level regex scanner over
  import/export/require lines, documented at the module head as a heuristic
  with three named v1 limitations (multi-line statements, dynamic `import()`,
  commented-out imports). `build_import_neighbor_graph` maps paths to
  `ImportNeighbors`, whose resolved/external split is a sorted deduplicated
  tuple, so the same tree always yields the same graph. Both scanners are pure
  per-file computation and never follow a neighbor's own imports, which is why
  cyclic imports terminate by construction.
- **T002 — signature extractors and size caps.** `python_file_signatures`
  renders class/def/async-def headers with docstring first lines;
  `typescript_file_signatures` renders exported symbol lines;
  `extract_file_signatures` dispatches by suffix and sets `parse_failed` when
  no extractor could read the file. `fits_inline_size_cap` decides full versus
  signatures at `DEFAULT_INLINE_SIZE_CAP_BYTES` = 16384, and rendering is
  capped at `DEFAULT_SIGNATURE_LINE_CAP` = 200 lines, the cap each
  `CompiledContext` carries so its text and its estimate describe the same
  bytes.
- **T003 — tiered selector, budget demotion, omissions record.**
  `compile_task_context(root, fenced_paths, repo_paths)` assigns the tier
  table's four tiers, walks exactly two graph hops, and never walks a tree
  itself — the caller supplies the candidate listing. Over
  `DEFAULT_CONTEXT_TOKEN_BUDGET` = 24000 it demotes in three phases: the
  largest full tier-2 file to signatures, then distant files, then neighbors,
  never truncating a file mid-content. Every decision appends an
  `OmissionRecord(path, tier, reason, outcome)` with a five-word reason
  vocabulary — `budget`, `distance`, `binary`, `size`, `unparseable` — and an
  outcome that says whether the file is gone or merely reduced, a distinction
  the reason alone cannot carry. `write_omitted_context_json` writes
  `omitted_context.json` where its caller points it.
- **T004 — segment, size comparison, CLI view.**
  `render_compiled_context_text` renders the selection, and
  `register_compiled_context_segment` registers it into a
  `PromptSegmentRegistry` at rank `JOB_CONTEXT` under the name
  `compiled_context`, so composition stays with F105's registry and this
  feature owns selection alone. `compare_context_size` and
  `write_context_size_comparison_json` record the whole-files baseline against
  the compiled cost as `context_size.json`. `remedy job context <id> --task
  <tid>` (`apps/cli/commands/job_context_cmd.py`) is the debugging view, with
  exit codes 0 compiled, 1 unknown job, 2 no usable target repo and 3 task not
  resolved — a task is never guessed. It is documented for operators in
  `docs/guides/job-context-view-user-guide-v0.md`.
- **The DONE sentence, end to end.**
  `tests/orchestration/test_context_compiler_e2e.py` runs the same fixture task
  twice through the fake provider, whole-files and compiled: both reach
  `staged_review_passed`, the compiled context is strictly smaller, and its
  reported length is pinned to the exact bytes the compiler itself produces, so
  a run that bypassed compilation entirely cannot pass by being smaller for an
  unrelated reason. Suites: 65 selector and unit tests, 6 end-to-end, 9 CLI.
- **Deliberately not built here** (DECISION F107 D1, `.agent/decisions.md`):
  `register_compiled_context_segment` has no production caller yet — the run
  path passes a rendered context string and a category label, and the segment
  manifest is not written into run evidence; and the CLI's tier-1 seed is the
  task's `files_hint` alone, without the F017 fence allow-globs the Design
  names. Both deferrals are documented at the source and are reversible
  without changing the Design bullets, which already describe the intended end
  state.
<<<END PAIR_BS_TO>>>
Commit, then push:
  docs(f107): record the built state of the context compiler

C6 — plan and handoff. Replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0295. R18 reviewed PASS at 6e1970c4.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R19 — the last round before closure. The R18 gate is recorded, R-0291 and
R-0292 are resolved, R-0293 (the budget-demotion path shared the unparseable
blind spot) is registered and repaired with one test, R-0294 records the
reviewer-side pre-emission checklist miss, and the feature file now carries the
`## Built State` section closure precondition 4 requires. T001-T004 are
complete and reviewed; the integration gate ran at R16 and is GREEN, with its
evidence committed under `.agent/gate_f107_r16/`.

## Next Steps
1. R20 — closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the reviewer-authored STATUS line, the README capability
   sync in the same commit, then the PR. The five pre-existing `[reviewer]`
   failures (R-0286) are carried as a documented risk, so the closure verdict is
   PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with: feature and round,
branch, the commit SHAs of C1-C5, a changed-files table, the item-status table
for C1-C6, the REAL results of gates A-J, the open-findings count, and the next
expected action. The state block repeats the operator brief's Fortschritt line
verbatim:
  Fortschritt: ~96 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · R19 im Review · Closure offen) — Schätzung
Commit, then push:
  chore(f107): rewrite the plan and handoff for R19

GATES — run every one, record the real output and the real exit code
A transport: `cmp` of the scratch original against `.agent/authored/f107-r19-1.md`
  (silent, exit 0), that file's `wc -l` and `sha256sum`, and the C2 `cmp`
  against `.agent/last_block.md` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400 (DECISION F105 D5).
C pairs, after C3, in `.agent/live_review.md`: `^> Branch:.*Next free ID:
  R-0293` is 0 and `^> Branch:.*Next free ID: R-0295` is 1; `^- R-0293`,
  `^- R-0294`, `^Done: R-0291`, `^Done: R-0292` and `Reviewer gate on R18` are
  each 1; `^Done:` is 12 and `^Landed:` is 0. All four pairs are APPEND-shaped
  except PAIR_HDR, so prove them as such: each FROM line stays exactly 1x, and
  every TO-ONLY line occurs exactly 1x AMONG THE LINES C3's OWN DIFF ADDS.
  Report added/removed from `git show --numstat <C3> -- .agent/live_review.md`
  and the count of added lines belonging to no TO body (must be 0).
D built state: `grep -c '^## Built State' docs/roadmap/features/T2_F107.md` is
  1, `git show --numstat <C5> -- docs/roadmap/features/T2_F107.md` reports 0
  deletions, and the file's previous last line is still its 1x anchor.
E marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/handoff.md`, `docs/roadmap/features/T2_F107.md`,
  `packages/orchestration/context_compiler.py` and
  `tests/orchestration/test_context_compiler.py` (`grep -c` exits 1 on absence
  — that exit 1 is the pass).
F scoped suites: `python3 -m pytest tests/orchestration/test_context_compiler.py
  -q`, `python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q`,
  `python3 -m pytest tests/cli/test_job_context_cmd.py -q` and `python3 -m
  pytest tests/docs/ -q` — exit code and pass count for each. State the new
  collected count of `test_context_compiler.py` (64 before this round, one test
  added).
G red-proof, in a DISPOSABLE `git worktree` at HEAD and nowhere else
  (planner_reviewer_prompt.md §4.10): revert ONLY the `if
  signatures.parse_failed:` append you add in C4's phase A, run the single new
  test, and report whether it fails and with what message. Remove and prune the
  worktree, then show `git worktree list` and `git status --porcelain` proving
  the primary checkout is clean.
H canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
I lint: `python3 -m ruff check packages/orchestration/context_compiler.py
  tests/orchestration/test_context_compiler.py`.
J tree, push and scope: `git status --porcelain` empty, `git worktree list` the
  primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only 6e1970c4..HEAD` lists exactly the eight paths the Change
  line names, insertions per commit each under 500, and `gh pr list --state
  open` still returns an empty list. Also run `remedy plan status` and `remedy
  plan next` once and paste their real output into the handback — the planner's
  sandbox refuses those two commands, so this is the session's only Phase 0
  probe of them.
── END OF BLOCK ─────────────
