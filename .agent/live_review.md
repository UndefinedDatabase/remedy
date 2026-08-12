# Live Review — F107 Context compiler v2

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0280.

## Findings

- R-0221 (Low, carried from F103 through F104 and F105):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite — costing every integration
  gate phantom base-only failures through `_frontend_is_stale()` (exactly
  seven at the F105 R49 gate, all attributed). Not this feature's code;
  AGENTS.md Scope Control bars the "while I'm here" edit; routed to the F252
  flake-debt class. OPEN.
- R-0239 (Low, carried from F105): a reviewer-authored gate citation named a
  path that does not exist. The worker caught it, ran the real path and
  declared the correction, so nothing was skipped and no number is wrong. It
  stays open as the record of the citation-accuracy lesson, not as
  outstanding work. OPEN.
- R-0247 (Low, carried from F105): a reviewer-authored finding cited a line
  count of 101 where the file was 100. The substance was untouched and the
  finding's own subject was fixed. Same class as R-0239, same reason for
  staying open. OPEN.
- R-0262 (Low, carried from F105): `plan_job_llm` composes its prompt OUTSIDE
  the `try` that turns a provider failure into a renderable result, so a
  raising composer escapes the function. Pre-existing, real, and deliberately
  outside F105's change set — F105 moved composition, it did not own error
  handling. OPEN.
- R-0265 (Medium, carried from F105): a provider that reports usage but no
  cache field leaves a measured-looking `0` the token ledger cannot
  distinguish from a real zero. Documented in
  `docs/system/cache-optimal-prompt-ordering-v1.md` rather than worked
  around; the fix belongs to the actuals producer. OPEN.
- R-0266 (Medium, carried from F105): the token ledger's `role` is a
  hardcoded `builder` in production data, so a per-role split of production
  rows is one bucket. `remedy stats cache` prints that limit in its own
  output instead of burying it. The fix is a producer change. OPEN.
- R-0268 (Low, carried from F105): a `.agent/STOP` file carries no
  provenance — nothing distinguishes an operator stop from any other writer.
  Belongs to the self-drive protocol, not to prompt composition. OPEN.
- R-0270 (Medium, F107 R1, registered from `.agent/candidates.md` per
  STATUS_closure_protocol.md "Closure-candidate findings"): the review zip
  packages the gitignored scratch tree `.remedy-wt/`.
  `scripts/make_review_zip.sh` prunes `.git`, `.data`, caches and root-level
  `remedy-job-evidence-*` directories, but it sweeps the working tree with
  `find` and never consults `.gitignore` — measured at the F105 R50 gate:
  1091 of the 3646 members of
  `remedy-review-20260812-092055-READY_FOR_REVIEW.zip` come from
  `.remedy-wt/`. Three measured consequences. (1) A PRIOR feature's complete
  evidence bundle ships inside the package — 114 members under
  `.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure/` —
  which is exactly what the root-level exclusion exists to prevent; nesting
  one level deeper evades it. (2) The current bundle is packaged twice: 339
  authoritative members under `evidence/current/` plus 334 raw copies under
  `.remedy-wt/f105_closure_evidence/`. (3) 244 packaged scratch members
  contain the literal local path `/home/decodeux` while the manifest reports
  `external_paths_detected: []` — the local-path scanner reads evidence
  fields, not packaged tree members. The package itself stayed valid
  (`package_status` READY_FOR_REVIEW, alignment PASS), which is why this was
  a candidate and not a closure blocker. The fix belongs to
  `scripts/make_review_zip.sh` and docs/agents/self_drive_protocol.md
  together — it is neither F107's code nor F107's scope. OPEN.
- R-0271 (Low, F107 R3): `packages/orchestration/context_compiler.py` imports
  `Iterable` from `typing`, which ruff reports as UP035. The repo's ruff
  baseline already carries 24 other errors, so no gate turns red and nothing
  is blocked — but this one is F107's own new code, it is one line, and the
  module is open for editing in R4 anyway, so it is cheaper to clear than to
  carry. RESOLVED at the R4 gate (2026-08-12) — the `Done:` text closing it is
  the last entry of this file.
- R-0272 (Low, F107 R5): the R5 step block specified tier 2 as
  `build_import_neighbor_graph(...)` yielding "every `files` entry", but
  `ImportNeighbors` has no `files` field — its neighbor tuple is named
  `resolved` (the T001 dataclass in
  `packages/orchestration/context_compiler.py`). The worker implemented
  `resolved`, which is correct, so nothing on disk is wrong and no work is
  outstanding. Registered as the record of the citation-accuracy lesson, the
  same class as R-0239 and R-0247: a reviewer-authored contract must name
  fields that exist. OPEN.
- R-0273 (Medium, F107 R6): a CompiledContext compiled with a NON-DEFAULT
  `line_cap` is RENDERED at the module default, so the budget's numbers stop
  describing the text that would actually be sent.
  `render_compiled_context_text` calls `_signature_render_text(root, path,
  DEFAULT_SIGNATURE_LINE_CAP)` unconditionally, while `compile_task_context`
  estimated every signatures file at the CALLER's `line_cap`
  (`packages/orchestration/context_compiler.py`). Measured by the reviewer on
  a three-file fixture at `line_cap=3`: `compiled.estimated_tokens` reads 25
  while the rendered text estimates at 128 — 5.1x — and `compare_context_size`
  reports `saved_ratio=0.84`, a saving that does not exist. Both the budget
  enforcement and the size comparison therefore rest on a figure that does not
  describe the segment. The cause is the R6 step block, which fixed the
  rendering signature at `(root, compiled)` with no cap; the worker followed
  that contract and DISCLOSED the consequence in its handback instead of
  widening scope, which is exactly the right worker behavior and is why this
  is a finding against the contract, not against the round. No caller passes a
  custom cap today, so nothing on disk is wrong yet — but T004 part 2 is the
  first caller and must not inherit it. Fixed in R7 per DECISION D-F107-2.
  OPEN.
- R-0274 (Low, F107 R7): the R7 step block CONTRADICTED ITSELF about where the
  `Landed: R-0273` line belongs. Its Change line scoped `.agent/live_review.md`
  to "authored pairs LRF3 and LR6 in C3 only", while PROCEDURE step 8 directed
  the worker to write the `Landed:` line and carry it in commit C5. The same
  step also asked for "which commit" INSIDE the very commit that writes the
  line, which no commit can satisfy: a commit cannot contain its own SHA. The
  worker read both, applied the safe reading, named the commit by subject
  instead of by SHA, and DISCLOSED both points in its handback rather than
  guessing silently — the wanted behavior, and the reason neither cost a round.
  Fourth entry in the contract-accuracy class after R-0239, R-0247 and R-0272:
  a reviewer-authored block must not contradict itself and must not order a
  value that cannot exist. OPEN.
- R-0275 (Low, F107 R8-close): the R8 handoff reported commit C2's `+/-` column
  as the file's before/after LINE COUNTS, `218/328`, where
  `git show --numstat 627ca2c9 -- .agent/last_block.md` returns `169	279`; gate
  g then repeated the same 218 in its per-commit insertion list. Nothing rests
  on the error — both readings are far under 500, and a verbatim rewrite of a
  single `.agent/**` state file is cap-exempt outright (AGENTS.md Commit
  Discipline, DECISION F104 D1) — but a `+/-` column is a counted value and the
  counting rule names one measure, the `+` column of the diff. Worker-side
  member of the contract-accuracy class after R-0239, R-0247, R-0272 and
  R-0274: every number in the return channel is the output of the command it
  claims to come from. OPEN.
- R-0276 (Medium, F107 R8-close): this file's own header line 8 reads
  `Next free ID: R-0271` while R-0271, R-0272, R-0273 and R-0274 all exist in
  the Findings section above it — stale since R3 registered R-0271.
  `.agent/plan.md` and `.agent/handoff.md` both carry the correct R-0275, so
  the one carrier that OWNS the sequence is the one that is wrong, and it is
  the carrier a reviewer reads to allocate an ID
  (docs/agents/planner_reviewer_prompt.md §4.4, "IDs continue
  monotonically"). A session that trusted the header would reuse R-0271 and
  silently overwrite a live finding. Fixed in this round: the header now reads
  R-0277, allocated past the two findings this gate registers. OPEN until the
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

## Steps

R1 claim, candidate sweep and state reset → R2 T001 import-neighbor graphs
(Python via ast, TS/JS via the documented line scanner) → T002 signature
extractors + size caps + goldens → T003 tiered selector + budget demotion +
omissions writer → T004 segment integration + `remedy job context` CLI view +
end-to-end fixture task → integration gate → closure per
docs/roadmap/STATUS_closure_protocol.md.

- Reviewer gate on R1 (2026-08-12): PASS. Range 2e4142c3..d2b962af = eight
  commits touching exactly the eight paths the R1 block named — no production
  code, no test module, no docs beyond the one STATUS.md line. Transport by
  the primary shape: `cmp` of every applied state file against the reviewer's
  surviving `.remedy-wt/` originals silent; the block original, the committed
  `.agent/authored/f107-r1-1.md` and `.agent/last_block.md` byte-identical at
  274 lines. The claim commit's numstat for STATUS.md reads `1 1`, the TO line
  counts 1x and the FROM 0x after the edit. Every scoped gate was RE-RUN by
  the reviewer instead of read from the handback: `python3 -m pytest
  tests/docs/ -q` returns 294 passed, the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c '^## Steps'` is 1 and `grep -c '^<<<'` is 0 across the five state
  files, `.agent/plan.md` is 29 lines, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. Insertions per commit 274, 265,
  1, 62, 2, 22, 30, 53 — each under 500. R-0270 is registered and
  `.agent/candidates.md` is empty, so the feature-claim block condition is
  discharged. `LAST_REVIEWED_SHA` advances 2e4142c3 -> d2b962af.

- Reviewer gate on R2 (2026-08-12): PASS, partial round — `.agent/STOP`
  truncated it after the module commit and the worker declared the truncation
  (guardrail G6, docs/agents/self_drive_protocol.md). Range d2b962af..5a9951d5
  is six commits touching six of the seven paths the R2 block named; the
  seventh, tests/orchestration/test_context_compiler.py, is the declared skip.
  Transport by the primary shape: `cmp` of the surviving reviewer original
  `.remedy-wt/f107-r2-1.block.md` against the committed
  `.agent/authored/f107-r2-1.md` is silent, and so is the authored copy
  against `.agent/last_block.md` — all three 182 lines. Both slice bodies
  recompute to their BEGIN-marker digests, the PLAN body is byte-equal to
  `.agent/plan.md`, and the LRAPP body is the verbatim tail of this file. That
  pair was APPEND-shaped and `git show --numstat 72d79079` reads `19 0`: zero
  deletions, which proves the FROM line was never edited. Every scoped gate
  was RE-RUN by the reviewer instead of read from the handback — the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c` for the Steps heading is 1, `.agent/plan.md` is 28 lines,
  `git status --porcelain` is empty, `git worktree list` shows the primary
  checkout alone, and HEAD equals `origin/feature/f107-context-compiler-v2`.
  Insertions per commit 182, 155, 19, 10, 302, 49 — each under 500. Gate d
  could not run at all, because the round's own test module is the missing
  seventh path: `packages/orchestration/context_compiler.py` is REVIEWED AND
  PROBED BUT NOT GATED. The reviewer probe, on a throwaway fixture tree under
  `.remedy-wt/`, reproduced every case the T001 contract names — absolute
  import, from-module against from-symbol, single- and double-dot relative,
  two-file cycle terminating, stdlib to external, SyntaxError and missing file
  to parse_failed, no self-listing, './x' beating an x/index.ts sibling,
  './dir' to dir/index.ts, export-from, require(), .tsx and .jsx, 'react'
  external, an escaping specifier external, and a graph that is sorted,
  deduplicated, twice-equal and parse_failed on an unknown suffix — but a
  reviewer probe is not committed evidence and this file does not treat it as
  any. R3 commits that test module and R3's gate d is what certifies the
  module; until it is green, no verdict here claims T001 is test-covered.
  Recorded as an observation and not a finding: the R2 handoff is 62 lines
  where the R2 block asked for 60, which AGENTS.md permits outright for a
  per-commit table of more than five commits, and this one has six.
  `LAST_REVIEWED_SHA` advances d2b962af -> 5a9951d5.

- Reviewer gate on R3 (2026-08-12): PASS. Range 5a9951d5..ef64cf72 = six
  commits touching exactly the six paths the R3 block named. Transport by the
  primary shape: `cmp` of the reviewer original `.remedy-wt/f107-r3-1.block.md`
  against the committed `.agent/authored/f107-r3-1.md` silent, and the authored
  copy against `.agent/last_block.md` silent, all 232 lines; both slice bodies
  recompute to their BEGIN-marker digests, PLAN2 is byte-equal to
  `.agent/plan.md` and LR2 is the verbatim tail of this file. The LR2 pair was
  APPEND-shaped and `git show --numstat 0dbdaa83` reads `37 0` — zero
  deletions. No worker-authored `Done:` line exists in this file. Gates were
  RE-RUN by the reviewer rather than read from the handback: the T001 gate
  `python3 -m pytest tests/orchestration/test_context_compiler.py -q` returns
  16 passed, the canary returns 42 passed, `.agent/plan.md` is 29 lines, the
  Steps heading count is 1, `git status --porcelain` is empty and
  `git worktree list` shows the primary checkout alone. Insertions per commit
  232, 189, 37, 7, 274, 63 — each under 500. The 16 test functions carry all
  26 numbered obligations of the R3 contract, each as an equality assertion on
  real values rather than a truthiness check, and the deliberate external
  renderings ('os', 'typing.Iterable', '...x', '../../escape', 'react') are
  pinned verbatim. The reviewer ran TWO independent mutation probes in a
  disposable worktree at ef64cf72, one of them deliberately different from the
  worker's: removing the self-discard line reddens exactly
  `test_python_file_importing_its_own_module_name_does_not_list_itself`, and
  swapping the TS candidate order reproduces the worker's reported failure
  `AssertionError: assert ('x/index.ts',) == ('x.ts',)` in
  `test_typescript_suffix_candidate_beats_index_file_candidate` — so the
  handback's probe evidence is confirmed true and the goldens bite. That
  worktree was removed and pruned before this verdict. The 75-line handoff is
  a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md permits for a per-commit table of more than five commits. T001 is
  now test-covered on the branch and the R2 ungated-module caveat is
  discharged. `LAST_REVIEWED_SHA` advances 5a9951d5 -> ef64cf72.
- Reviewer gate on R4 (2026-08-12): PASS. Range ef64cf72..2c75bddf = eight
  commits touching exactly the seven paths the R4 block named. Transport by the
  PRIMARY shape, the reviewer original having survived the session boundary:
  `sha256sum` of `.remedy-wt/f107-r4-1.block.md`, of the committed
  `.agent/authored/f107-r4-1.md` and of `.agent/last_block.md` returns
  7cf9a5f065db… for all three. This session's permission layer denies `cmp`,
  so byte identity was proven by digest instead — strictly stronger than the
  ordered check, never weaker. All three slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF fac600cb… 7 lines, LR3
  1dc20c0b… 33 lines, PLAN3 4b98f108… 29 lines), and `sha256sum
  .agent/plan.md` returns that same PLAN3 digest: the plan on disk IS the
  authored slice, not a retype of it. The C3 pair was ANCHOR-PRESERVING and
  `git show --numstat 657b98fb -- .agent/live_review.md` reads `38  0` — zero
  deletions; both FROM lines occur exactly 1x in the file and 0x among the 38
  added lines, and every TO-only line of both slices occurs exactly 1x among
  those added lines, with no strays. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 29 passed (the 16
  frozen T001 tests plus 13 new), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!" — which is
  what closes R-0271 — `.agent/plan.md` is 29 lines, the Steps heading count
  is 1, `grep -c '^<<<'` is 0 across all three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 326, 280, 38, 2, 11, 242, 271, 80 — each under 500. The 13 test
  functions carry all 13 numbered obligations of the R4 contract as exact
  tuple equalities rather than truthiness checks, and the goldens are
  mechanically captured rather than hand-written — `limit: int=10` is
  `ast.unparse` spacing, which no human would type on purpose. The reviewer
  ran THREE mutation probes in a disposable worktree at 2c75bddf, two of them
  deliberately different from the worker's: turning the size cap's `<=` into
  `<` reddens exactly `test_fits_inline_size_cap_is_inclusive_at_the_cap_and`
  `_false_when_absent` with `AssertionError: assert False is True`, and
  deleting the nested-declaration recursion line reddens exactly the Python
  whole-file golden and
  `test_python_file_without_any_docstring_renders_headers_only`. The worker's
  own probe reproduces verbatim — `1 failed, 28 passed`, failing
  `test_typescript_signature_golden_renders_exported_lines_only` on
  `'export function renderWidget(id: string): void {' !=` the same line
  without its brace — so the handback's probe evidence is confirmed TRUE
  rather than taken on trust. That worktree was removed and pruned before this
  verdict and `git worktree list` shows the primary alone. The 96-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits; both declared deviations are accurate and
  neither weakens a proof. No new findings this round.
  `LAST_REVIEWED_SHA` advances ef64cf72 -> 2c75bddf.
- Reviewer gate on R5 (2026-08-12): PASS. Range 2c75bddf..54bc56c2 = seven
  commits touching exactly the seven paths the R5 block named. The round spanned
  TWO worker sessions: a prior worker committed C1-C6 and ended before PROCEDURE
  step 7, and this session's worker ran the mutation probe, re-verified the disk
  state and committed C7 alone. The single-writer rule held throughout — the
  reviewer wrote nothing, and no existing commit was amended, rebased, reverted
  or reordered. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r5-1.block.md` against `.agent/authored/f107-r5-1.md`, and of
  that copy against `.agent/last_block.md`, is silent, and all three sha256 to
  220d64ec8aa4… at 393 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (FIX1FROM 06f8ce67… 1 line,
  FIX1TO 547f5a52… 2, LR4FROM 3541d8ff… 1, LR4TO b07a255e… 53, PLAN4 320c4890…
  28), and `cmp .agent/plan.md` against the extracted PLAN4 body is silent: the
  plan on disk IS the authored slice, not a retype of it. Both C3 pairs were
  REWRITES and `git show --numstat 4860115e -- .agent/live_review.md` reads
  `55  2` — both FROM strings now occur 0x, each of the 2 FIX1TO and 53 LR4TO
  lines occurs exactly 1x among the 55 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer rather than read
  from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 42 passed (the 29
  frozen T001+T002 tests plus 13 new T003 tests), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!",
  `.agent/plan.md` is 28 lines, the Steps heading count is 1, the stray-marker
  count is 0 across the three state files, `git status --porcelain` is empty,
  HEAD equals `origin/feature/f107-context-compiler-v2`, and `git worktree list`
  shows the primary checkout alone. Insertions per commit 393, 322, 55, 11, 351,
  284, 76 — each under 500. The 13 new test functions carry all 13 numbered
  obligations of the R5 contract as exact equality assertions on real values,
  and every token figure is asserted against a direct `estimate_text_tokens`
  call rather than against a hand-copied number. The reviewer ran THREE mutation
  probes in a disposable worktree at 54bc56c2, two of them deliberately
  different from the worker's: pointing budget phase B at TIER_NEIGHBOR instead
  of TIER_DISTANT reddens exactly
  `test_budget_omits_tier_three_before_it_omits_tier_two` and
  `test_tier_one_is_never_cut_by_the_budget_and_the_overflow_is_reported`, while
  suppressing the tier-4 distance records reddens exactly the tier-assignment
  test, the export-keys test and the completeness test. The worker's own probe
  reproduces verbatim — `1 failed, 41 passed`, failing
  `test_budget_demotes_the_largest_tier_two_file_first` on `At index 1 diff:`
  the big neighbor rendering `full` where the test requires `signatures` — so
  the handback's probe evidence is confirmed TRUE rather than taken on trust.
  That worktree was removed and pruned before this verdict. The 95-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits. One new finding, R-0272, is registered above.
  Recorded as an observation and NOT as a finding: `context_compiler.py` still
  has no caller outside its own test module, because T003 is a library layer by
  design and T004 is the round that wires it — a green gate here is not yet a
  working feature, and no verdict in this file claims otherwise.
  `LAST_REVIEWED_SHA` advances 2c75bddf -> 54bc56c2.
- Reviewer gate on R6 (2026-08-12): PASS, with one new finding. Range
  54bc56c2..861eb371 = seven commits touching exactly the seven paths the R6
  block named. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r6-1.block.md` against `.agent/authored/f107-r6-1.md`, and
  of that copy against `.agent/last_block.md`, is silent, and all three sha256
  to c263869d4444… at 364 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF2FROM 2bb66673… 1 line,
  LRF2TO 830262c1… 10, LR5FROM b96097af… 1, LR5TO 98b340c5… 51, PLAN5
  27f9c8ef… 28), and `sha256sum .agent/plan.md` returns that same PLAN5
  digest. Both C3 pairs were APPEND-shaped and were proven as such rather than
  as rewrites: `git show --numstat 2afec22b -- .agent/live_review.md` reads
  `59  0` — ZERO deletions, which is what proves neither anchor line was
  edited — each FROM still occurs exactly 1x in the file, each of the 9 LRF2TO
  and 50 LR5TO TO-only lines occurs exactly 1x among the 59 added lines, and 0
  added lines belong to neither body. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 52 passed (the 42
  frozen tests plus 10 new), `tests/orchestration/test_prompt_segments.py`
  returns 25 passed — that module's suite was gated because this round imports
  from it for the first time — the canary `tests/cli/test_golden_path.py`
  returns 42 passed, `python3 -m ruff check` over the module and its test file
  returns "All checks passed!", `.agent/plan.md` is 28 lines, the Steps
  heading count is 1, `grep -c '^- R-0272'` is 1, the stray-marker count is 0
  across the three state files, `git status --porcelain` is empty, HEAD equals
  `origin/feature/f107-context-compiler-v2` and `git worktree list` shows the
  primary checkout alone. Insertions per commit 364, 285, 59, 10, 162, 190, 75
  — each under 500. The reviewer ran FOUR mutation probes in a disposable
  worktree at 861eb371, three of them deliberately different from the
  worker's: collapsing the block separator from a blank line to a single
  newline and dropping the tier number from the header line each redden
  exactly `test_render_compiled_context_text_builds_one_block_per_included`
  `_file`, and making the zero-baseline ratio guard return a fabricated 1.0
  reddens exactly `test_compare_context_size_reports_no_ratio_for_a_zero`
  `_baseline`. The worker's own probe reproduces verbatim — moving the
  registered rank from JOB_CONTEXT to TASK gives `2 failed, 50 passed`,
  reddening the segment-rank test and the manifest-row test — so the
  handback's probe evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. All three declared
  deviations are accurate: the 100-line handoff sits exactly at the AGENTS.md
  D15 ceiling with its stated cause, the greedy `rstrip` is the reading that
  actually delivers the stated invariant, and the two docstring header updates
  are inside files the change set already names. What the round did NOT do is
  the finding: the worker's third disclosure — that a custom `line_cap` is
  rendered at the module default — is real, is larger than the note implied,
  and was MEASURED by the reviewer rather than accepted as written. It is
  registered above as R-0273 and R7 fixes it. Recorded as an observation and
  not a finding: `context_compiler.py` still has no caller outside its own
  test module, so F107 remains a library that is not yet wired to anything a
  user can run. `LAST_REVIEWED_SHA` advances 54bc56c2 -> 861eb371.
- Reviewer gate on R7 (2026-08-12): PASS. Range 861eb371..6acb3f04 = eight
  commits touching exactly the seven paths the R7 block named. Transport by the
  PRIMARY shape: `cmp` of `.remedy-wt/f107-r7-1.block.md` against
  `.agent/authored/f107-r7-1.md` and against `.agent/last_block.md` is silent,
  all three at 328 lines, and all five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF3FROM 4ad9497d… 1 line,
  LRF3TO e3fdd106… 20, LR6FROM d85c84ac… 1, LR6TO dac43442… 50, PLAN6
  047fcc7a… 28); `sha256sum .agent/plan.md` returns that same PLAN6 digest.
  Both C3 pairs were APPEND-shaped and proven as such: `git show --numstat
  4909b1b1 -- .agent/live_review.md` reads `68  0` — ZERO deletions — each FROM
  still occurs exactly 1x, each of the 19 LRF3TO and 49 LR6TO TO-only lines
  occurs exactly 1x among the 68 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer: the module suite
  returns 55 passed (the 52 frozen tests plus 3 new), the canary returns 42
  passed, `python3 -m ruff check` returns "All checks passed!", `.agent/plan.md`
  is 28 lines, the Steps heading count is 1, `grep -c '^- R-0273'` is 1, the
  stray-marker count is 0 across the three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 328, 255, 68, 9, 16, 113, 75, 18 — each under 500. THE FIX WAS
  MEASURED, not read: the reviewer re-ran the same three-file fixture at
  `line_cap=3` that produced the R-0273 numbers, and the rendered text's
  estimate falls from 128 tokens to 46 against an `estimated_tokens` of 25 —
  the 5.1x divergence is gone. The residual 21-token gap is the block HEADER
  lines the renderer adds, it is the same ~20 tokens at the default cap, and it
  is therefore uniform overhead rather than cap drift; it is recorded here as
  an observation for R8's evidence work, NOT as a finding, because
  `estimated_tokens` is documented as a sum over file contents and the headers
  are one bounded line per included file. The reviewer ran TWO probes in a
  disposable worktree at 6acb3f04 and both reproduce the worker's numbers
  verbatim: putting the renderer back on the module default gives `1 failed, 54
  passed` on `test_signature_blocks_render_at_the_cap_the_context_was_compiled`
  `_at`, and storing the default in the constructor instead of the caller's cap
  gives `3 failed, 52 passed` — so the regression test genuinely bites and the
  handback's evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. Both declared deviations
  are accepted. The 114-line handoff exceeds even the D15 100-line ceiling, and
  the cause is mandated content this reviewer ORDERED — gate i was required to
  carry both step-7 transcripts with failing test names and assertion texts —
  so it is a stated-cause overage and not verbosity; no section was dropped.
  The eighth commit is the right call and not a scope breach: it corrects a
  stale grep line number in the handoff, touches only a path the Change line
  already names, and was made in its own commit because amending C7 is
  forbidden — leaving a false counted value in the return channel would have
  been the worse error. One new finding, R-0274, is registered above for the
  block's own self-contradiction. `LAST_REVIEWED_SHA` advances 861eb371 ->
  6acb3f04.

- Reviewer gate on R8-close (2026-08-12, first gate of a NEW session; the
  round it certifies was the terminating round of the previous one, so per
  docs/agents/planner_reviewer_prompt.md §4.13 its verdict had lived only in
  `.agent/handoff.md` until now): PASS. Range 6acb3f04..7acb406d = five commits
  touching exactly the five paths the R8 block named — no production code, no
  test module, no docs. Transport by the PRIMARY shape: the reviewer original
  `.remedy-wt/f107-r8-1.block.md` survived the session boundary, `cmp` against
  `.agent/authored/f107-r8-1.md` and against `.agent/last_block.md` is silent,
  and all three sha256 to 607d240a3a067a4c… at 218 lines. All five slice bodies
  recompute to their BEGIN-marker digests at their declared lengths (LRF4FROM
  d129628f… 1 line, LRF4TO b36108ed… 13, LR7FROM cdc1e3cf… 1, LR7TO 47bc40dd…
  48, PLAN7 a065b87c… 28), and `sha256sum .agent/plan.md` returns that same
  PLAN7 digest over 28 lines. Both C3 pairs were APPEND-shaped and proven as
  such rather than asserted: `git show --numstat 3e704610 -- .agent/live_review.md`
  reads `59  0` — ZERO deletions, so neither anchor was edited — each FROM
  occurs exactly 1x in the file, each of the 12 LRF4TO and 47 LR7TO TO-only
  lines occurs exactly 1x among the 59 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by this reviewer rather than read
  from the handback: `python3 -m pytest tests/orchestration/test_context_compiler.py -q`
  returns 55 passed, the canary `python3 -m pytest tests/cli/test_golden_path.py -q`
  returns 42 passed, `grep -c '^## Steps'` is 1, `grep -c '^- R-0274'` is 1,
  `grep -c '^Done:'` is 1 and `grep -c '^Landed:'` is 1, the stray-marker count
  is 0 across the three state files, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. One counted value in the handback
  did NOT survive re-measurement and is registered above as R-0275: C2's real
  numstat is `169 279`, not the reported `218/328`. The verdict is PASS anyway
  and deliberately so — the error is in the report of a commit that is
  cap-exempt by construction, every other figure re-measured true, and the
  round's substance (transport, application, gates) is verified correct. The
  stale next-free-ID header this gate also found is R-0276. `LAST_REVIEWED_SHA`
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

Done: R-0271 — RESOLVED. `packages/orchestration/context_compiler.py` now reads
`from collections.abc import Iterable` (commit b52b1c3c, numstat `1 1`), and the
reviewer's own re-run of `python3 -m ruff check` over that module and its test
file returns exit 0 with "All checks passed!" — zero errors, where the same
command reported UP035 before the fix. Open findings 9 -> 8.

Done: R-0273 — RESOLVED. `CompiledContext` carries a fifth field `line_cap`,
`compile_task_context` sets it from the caller's cap, and
`render_compiled_context_text` renders signature bodies at `compiled.line_cap`
instead of `DEFAULT_SIGNATURE_LINE_CAP` (commit e0f0a0d1 "fix(f107): render
signatures at the compiled line cap", C5 of R7). The fix was MEASURED, not
read: on the same three-file fixture at `line_cap=3` that produced the finding,
the rendered text's estimate falls from 128 tokens to 46 against an
`estimated_tokens` of 25, so the 5.1x divergence is gone, and two mutation
probes in a disposable worktree put the module back to red (1 failed / 3
failed) — the regression test genuinely bites. The residual 21-token gap is the
one header line the renderer adds per included file, uniform at every cap and
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
