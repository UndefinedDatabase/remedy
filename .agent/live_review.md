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

## Steps

R1 claim, candidate sweep and state reset → R2 T001 import-neighbor graphs
(Python via ast, TS/JS via the documented line scanner) → T002 signature
extractors + size caps + goldens → T003 tiered selector + budget demotion +
omissions writer → T004 segment integration + `remedy job context` CLI view +
end-to-end fixture task → integration gate → closure per
docs/roadmap/STATUS_closure_protocol.md.
