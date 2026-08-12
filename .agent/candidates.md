# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- The review zip packages the gitignored scratch tree `.remedy-wt/` · source
  feature: F105 · date: 2026-08-12 — measured by the reviewer at the R50 gate
  against `remedy-review-20260812-092055-READY_FOR_REVIEW.zip`: 1091 of its
  3646 members come from `.remedy-wt/`. `scripts/make_review_zip.sh` prunes
  `.git`, `.data`, caches and ROOT-LEVEL `remedy-job-evidence-*` directories,
  but it sweeps the working tree with `find` and never consults `.gitignore`.
  Three measured consequences. (1) A PRIOR feature's complete evidence bundle
  ships inside the package — 114 members under
  `.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure/` —
  which is exactly what the root-level exclusion exists to prevent; nesting
  one level deeper evades it. (2) The current bundle is packaged twice: 339
  authoritative members under `evidence/current/` plus 334 raw copies under
  `.remedy-wt/f105_closure_evidence/`. (3) 244 packaged scratch members
  contain the literal local path `/home/decodeux`, while the manifest reports
  `external_paths_detected: []` — the local-path scanner reads evidence
  fields, not packaged tree members, so the same class of leak that packaged
  the FIRST R50 zip attempt as BLOCKED_EVIDENCE rides undetected in the
  second. The package itself remains valid and authoritative:
  `package_status` is READY_FOR_REVIEW, `packaged_evidence_job_id` is
  `f105-closure`, and `review_subject_evidence_alignment` is PASS — which is
  why this is a candidate and not a closure blocker. It is neither F105's
  code nor F105's scope: `.remedy-wt/` exists only because self-drive scratch
  cannot be written to `/tmp` on this machine, so the fix belongs to
  `scripts/make_review_zip.sh` and docs/agents/self_drive_protocol.md
  together.
