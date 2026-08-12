── STEP R1/~10 — F107 Context compiler v2 ────────────────────────────────────
Goal:        Claim F107, sweep the closure candidate into finding R-0270, and
             reset the session state files. No production code this round.
Bundle:      Branch creation; C1 authored-block save; C2 last_block mirror;
             C3 STATUS claim; C4 live_review reset (registers R-0270);
             C5 candidates sweep; C6 plan rewrite; C7 context rewrite;
             C8 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             docs/roadmap/STATUS.md (one line, FROM→TO below),
             .agent/authored/f107-r1-1.md (new),
             .agent/last_block.md, .agent/live_review.md,
             .agent/candidates.md, .agent/plan.md, .agent/context.md,
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full — self-review loop before every commit, small
             commits, no leading-slash tokens or absolute paths in commit
             subjects. Do NOT create a PR. Never touch main. Never write a
             `Done:` line in live_review (reviewer-only text). Apply every
             authored slice byte for byte after verifying its sha256; if a
             hash does not match, STOP and hand back the mismatch — never
             retype or repair authored text. Scratch files go under
             .remedy-wt/ only (never /tmp), and are never committed.

PROCEDURE (in order, one commit per item):

0. Preconditions: `git status --porcelain` empty; `git branch --show-current`
   is main; `git log -1 --format=%h` is 2e4142c3 (else `git pull --ff-only`
   first; if it still differs, STOP and hand back).
   Then: `git checkout -b feature/f107-context-compiler-v2`

1. C1 — save THIS ENTIRE step block, from the "── STEP" line above through
   the final line of this block, byte for byte, as .agent/authored/f107-r1-1.md.
   Then verify every slice against its marker digest before anything is
   applied. Extraction recipe for slice NAME:
     sed -n '/^<<<BEGIN SLICE NAME /,/^<<<END SLICE NAME>>>$/p' \
       .agent/authored/f107-r1-1.md | sed '1d;$d' > .remedy-wt/f107-r1-NAME.check
     sha256sum .remedy-wt/f107-r1-NAME.check   # must equal the marker digest
   All six slices must verify (LR, CAND, PLAN, CTX, SFROM, STO).
   Commit: chore(f107): save the R1 claim step block verbatim

2. C2 — copy .agent/authored/f107-r1-1.md over .agent/last_block.md;
   `cmp .agent/authored/f107-r1-1.md .agent/last_block.md` must be silent.
   Commit: chore(f107): mirror the R1 block into last_block

3. C3 — STATUS claim, REWRITE shape (FROM and TO are disjoint single lines).
   In docs/roadmap/STATUS.md replace the exact line SFROM with the exact
   line STO (both verified by hash in step 1; apply from the .check files,
   not by retyping). Proof: FROM 0x and TO 1x in the file after the edit;
   `git show --numstat HEAD -- docs/roadmap/STATUS.md` reads `1 1`.
   Gate (same commit's tree): `python3 -m pytest tests/docs/ -q` exit 0.
   Commit: chore(f107): claim F107 in the ledger

4. C4 — replace .agent/live_review.md ENTIRELY with slice LR:
   `cp .remedy-wt/f107-r1-LR.check .agent/live_review.md`
   `cmp .remedy-wt/f107-r1-LR.check .agent/live_review.md` silent.
   This reset registers R-0270 and carries the seven open F105 findings.
   Commit: chore(f107): reset live_review and register R-0270

5. C5 — replace .agent/candidates.md ENTIRELY with slice CAND (same cp+cmp
   pattern). Commit: chore(f107): empty candidates after the R-0270 sweep

6. C6 — replace .agent/plan.md ENTIRELY with slice PLAN (cp+cmp).
   Commit: chore(f107): rewrite plan for F107

7. C7 — replace .agent/context.md ENTIRELY with slice CTX (cp+cmp).
   Commit: chore(f107): rewrite context for F107

8. C8 — rewrite .agent/handoff.md yourself (your text, not authored): ≤60
   lines, containing feature+round (F107 R1), branch, a per-commit SHA table
   (C1–C8; C8 marks itself self-ref), a changed-files table, the real gate
   results from "Done when" below (command + exit code + the counted number,
   no verdict words), the open-findings count (8) with next free ID R-0271,
   an item-status table over C1–C8, and next expected action: R2 = T001
   import-neighbor graphs. Commit: chore(f107): rewrite handoff for R1
   Then push: `git push -u origin feature/f107-context-compiler-v2`

Done when (run each, record command + real exit code + counted value):
  a. sha256sum over all six .check files — each equals its marker digest;
     cmp of authored vs last_block silent.
  b. grep -c -F -- '- [~] F107 — Context compiler v2' docs/roadmap/STATUS.md → 1
     grep -c -F -- '- [ ] F107' docs/roadmap/STATUS.md → 0 (exit 1 is the pass)
  c. cmp silent for each of: live_review vs LR.check, candidates vs
     CAND.check, plan vs PLAN.check, context vs CTX.check.
  d. grep -c '^## Steps' .agent/live_review.md → 1
     grep -c '^<<<' on each of live_review.md, candidates.md, plan.md,
     context.md, handoff.md → 0 each (grep exit 1 is the pass; the authored
     file and last_block legitimately contain markers and are NOT counted)
     wc -l < .agent/plan.md → 29 (< 50)
  e. python3 -m pytest tests/docs/ -q → exit 0 (run at C3; rerun at HEAD)
  f. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0
  g. git status --porcelain → empty; HEAD == origin/feature/f107-context-compiler-v2
  h. insertions per commit (git log --numstat): each < 500; the single-file
     .agent state rewrites are exempt by AGENTS.md D1 but report the numbers.
Handback:    completion report in your final message (tables + raw gate
             results) — .agent/handoff.md rewritten as C8. Do not merge,
             do not open a PR, do not touch .agent/decisions.md this round.

<<<BEGIN SLICE SFROM sha256=a113d2c3c2fa799564e1d9af51607ec04087281a6ca0c340638cfb62b309d6d3 lines=1>>>
- [ ] F107 — Context compiler v2
<<<END SLICE SFROM>>>

<<<BEGIN SLICE STO sha256=ddd72c5d2947bfb02c067d78e0b3b082af0cf63a6346500394dde1af9625c8a7 lines=1>>>
- [~] F107 — Context compiler v2
<<<END SLICE STO>>>

<<<BEGIN SLICE LR sha256=0241279cef46d4c52a0a806e49eb58ec2bfd1ab2b8552cb5c4cf003bfe079343 lines=77>>>
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
<<<END SLICE LR>>>

<<<BEGIN SLICE CAND sha256=38210869c250cd821ca8c6fd8a3975058e6e8b98567150bbb045cdce6d31e26f lines=11>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(empty — the single F105 candidate was registered as finding R-0270 in
`.agent/live_review.md` at F107 R1, 2026-08-12.)
<<<END SLICE CAND>>>

<<<BEGIN SLICE PLAN sha256=f2a55d555164a3a7474c315f26486114109342b532cf443d06213c8a46fdada7 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0271.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R1 (this round): claim F107 `[~]` in docs/roadmap/STATUS.md, reset
.agent/live_review.md, register R-0270 from .agent/candidates.md and
empty that file, rewrite plan and context. No production code this round.

## Next Steps
1. R2 — T001 import-neighbor graphs: Python via ast, TS/JS via the
   documented line-level scanner; unit tests on fixture trees (cycles,
   relative imports, index files).
2. T002 — signature extractors for both languages + size caps + goldens.
3. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
4. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
5. Integration gate, then closure per STATUS_closure_protocol.md.
<<<END SLICE PLAN>>>

<<<BEGIN SLICE CTX sha256=ac1e6c049350f70ee03063ac9f07e67a32c8149c7ba408e96839aad34a809eda lines=42>>>
# Context — F107 Context compiler v2

## Active Branch
feature/f107-context-compiler-v2, cut from main at 2e4142c3 after PR #191
was merged at the Open PR Gate. F107 is claimed `[~]` under Rule A5 as the
first `[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use, Tier 2).

## Scope
In: packages/orchestration/context_compiler.py — import-neighbor graphs
(Python via ast, TS/JS via a documented line-level import scanner),
signature extractors, the tiered selector (the tier table of
docs/roadmap/features/T2_F107.md is the contract), budget demotion,
omitted_context.json, segment integration and the `remedy job context`
debugging view. Tests under tests/orchestration/test_context_compiler.py.

Out, per the feature file's Do-not-touch: prompt composition (the segment
registry owns it), retrieval/embedding approaches, repo-map features.
No TS parser dependency — reject any diff adding one; the line scanner is
an honestly documented heuristic.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/,
  and production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable
  git worktree, so resource safety stays intact and no background pytest
  process is ever left running.
- Dynamic imports and string-based requires are invisible to v1 — a
  documented limitation with the files_hint escape hatch (A9 defaults in
  the feature file).

## Steps
R1 claim, candidate sweep and state reset → R2 T001 import-neighbor
graphs → T002 signature extractors → T003 tiered selector + budget
demotion + omissions writer → T004 segment integration + CLI view +
end-to-end fixture → integration gate → closure.
<<<END SLICE CTX>>>
