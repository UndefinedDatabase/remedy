# Live Review — F107 Context compiler v2

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0271.

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
  carry. OPEN.

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
