── STEP CLOSURE PRECONDITION 4 — F112 Prompt budget per task class ─────────
Round 22 · session continuing F112 · base `042d3683` (F112 R21 C4, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 21's PASS verdict (RECORD21, given verbatim below, already
  independently re-verified by the reviewer — do not re-derive it), then
  append a "Built State — what F112 delivered" section to
  `docs/roadmap/features/T3_F112.md`, which currently has none
  (closure precondition 4, docs/roadmap/STATUS_closure_protocol.md).
  No production code touched.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r22.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD21 to `.agent/live_review.md`
  C2   apply PLAN22 to `.agent/plan.md`
  C3   append BUILT_STATE to `docs/roadmap/features/T3_F112.md`
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r22.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `docs/roadmap/features/T3_F112.md`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/` is touched, and no OTHER
  file under `docs/` is touched.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE — never edit, retype or
     re-wrap one. If a slice looks wrong, apply it anyway and DECLARE the
     problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C4. If it exists at either reading: finish the commit in
     hand, write the handback, push, and stop.
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN22 is applied
     as an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD21_bytes` — ONE newline, no
     blank line. Confirm the byte immediately before the append point
     yourself before writing, per this feature's own established
     convention since R14.
  4. `docs/roadmap/features/T3_F112.md` is a NORMAL markdown doc file and
     ends WITH a trailing newline (unlike the `.agent/**` files above —
     do not confuse the two conventions). Append BUILT_STATE to it as
     `current_bytes + b"\n" + BUILT_STATE_bytes + b"\n"` — ONE blank line
     before the new section's heading, and the file ends with exactly one
     trailing newline afterward, matching how `docs/roadmap/features/T3_F110.md`'s
     own "## Built State — what F110 delivered" section was appended
     (read that file yourself to confirm the shape if useful — read-only,
     it is not part of this round's change set).
  5. Do NOT run `ruff`. You MAY run `python3 -m pytest tests/docs/ -q` as
     a sanity check after C3 if you want extra confidence the doc change
     doesn't break a doc-structure test, but it is not a required gate
     below and its result does not gate this round either way (this is a
     pure content append to an existing, already-indexed feature file —
     no new page, no README index entry needed).
  6. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
     are NOT touched.
  7. A sentence THIS ROUND makes stale, anywhere inside the change set, is
     repaired in the commit that falsifies it. One outside the change set
     is DECLARED in the handback and left alone.
  8. NEVER force-push, never work on `main`, create NO pull request, merge
     nothing.

THIS ROUND'S PARAMETERS, measured by the reviewer at `042d3683` before
this block was authored:
  LIVE_REVIEW PRE-C1     `.agent/live_review.md` measures 2293718 bytes,
                         ending WITHOUT a trailing newline.
  RECORD21 LENGTH        5338 bytes (measure this yourself against the
                         committed authored file's own extracted slice).
  POST-C1 EXPECTED       2293718 + 1 + 5338 = 2299057 bytes.
  HEADER SHAPE           lines matching `^Gate: F\d+ R\d+ — ` currently
                         number 268; matching `^Gate: F112 R21 — `
                         currently 0. Expected after C1: 269 and 1.
  OPEN SET               350 registered, 72 `Done:`, 278 open. UNMOVED by
                         this round's append (RECORD21 adds evidence to
                         `R-0784` in prose only — no id is minted, no
                         `Done:` line is written by this round). Reconfirm
                         on both sides of C1.
  PLAN.MD PRE-C2         45 lines (`wc -l`), ends WITHOUT a trailing
                         newline, currently holds PLAN21 (2025 bytes).
  T3_F112.MD PRE-C3      3970 bytes, ends WITH a trailing newline, 74
                         lines (`wc -l`), no `## Built State` heading
                         anywhere in it yet (`grep -c '^## Built State'`
                         answers 0).
  BUILT_STATE LENGTH     3520 bytes (measure this yourself against the
                         committed authored file's own extracted slice).
  POST-C3 EXPECTED       3970 + 1 + 3520 + 1 = 7495 bytes.

<<<BEGIN RECORD21>>>
Gate: F112 R21 — the round 21 entry, closure precondition 6's run step (no production code touched in the primary checkout). VERDICT PASS, over the range `e9b9c46e..042d3683` (commits C0a `60fd935c`, C0b `1e07cfa0`, C1 `e822388f`, C2 `7bea3efc`, C3 `1b9ac1ca` — five real content commits — plus handback commit `042d3683`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r21.md` and `HEAD:.agent/last_block.md` both print blob `e16ce65ac9e224eadc20396e0d0f2bbfa9162eb2`, reproduced directly; `wc -l` reproduced 250. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL: PLAN21 extracted from the committed authored file (2025 bytes) compared byte-for-byte against `.agent/plan.md` at C2 — equal, 2025 bytes both sides, no trailing newline, `## Goal` / `## Next Steps` each exactly once. THE RECORD APPEND AT C1 (booking RECORD20) HELD BYTE-IDENTICAL, WITH ONE DECLARED CORRECTION TO THE REVIEWER'S OWN PRIOR ARITHMETIC: the block's own params paragraph had pinned RECORD20's length at 2953 bytes, but the slice extracted from the committed authored file measures 2954 bytes — the reviewer's own pre-emission byte count was wrong by one, not a transport defect; the worker correctly applied the slice byte-for-byte as extracted rather than trusting the reviewer's stale numeral (checklist item 9's own lesson, here caught on the reviewer's side rather than a citation). Reproduced independently: pre-append `.agent/live_review.md` measured 2290763 bytes at `e9b9c46e`, RECORD20 extracted measured 2954 bytes, appended as one newline plus RECORD20, post-append measured 2293718 bytes exactly matching `2290763 + 1 + 2954`; the pre-append content is an exact byte prefix; the file still ends WITHOUT a trailing newline; the open set recomputed mechanically read 350 registered / 72 `Done:` / 278 open on both sides, and lines matching `^Gate: F\d+ R\d+ — ` read 268 after C1 with exactly one matching `^Gate: F112 R20 — `. THE RUN AT C3 WAS REAL, NOT SIMULATED: `run_next_self_use_item` was invoked exactly as ordered (default budgets, default role resolution, no `"fake"` override), ran for 116.86 seconds against the local `ollama` provider (`muse-glimmer:latest`, `execution_config` recording `builder='ollama'`/`reviewer='ollama'`, source `cli` for both — confirmed independently by the reviewer's own re-read of `resolve_role_config` before this block was authored and unchanged at the time of the run), and returned (did not raise) a `JobPlan` for job `848fc4c67d7b405b`: `status='blocked'`, task T001 `final_status='repair_exhausted'`, `reviewer_verdict='fail'`, both repair rounds spent, nothing promoted, `consumed_by` correctly left unset this round. `describe_self_use_run_defects(result)` returned exactly two strings, quoted verbatim in `.agent/selfuse_f112/run.txt`: `job 848fc4c67d7b405b (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. THE EVIDENCE COPY IS BYTE-IDENTICAL, reproduced independently by the reviewer: `sha256sum .agent/selfuse_f112/SU-007.md` reads `6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd` — the SAME digest as `.agent/selfuse_f110/SU-006.md`, expected and not a copy error, because SU-006 and SU-007 render the identical R-0418 ledger paragraph verbatim and only their `job_id`s differ. CLEANUP REPRODUCED INDEPENDENTLY: `.remedy-wt/selfuse-f112-run` is absent; `.remedy-wt/job-848fc4c67d7b405b` exists, retained and untouched by this round; the two untracked driver-script scratch files are gone; `git diff --stat e9b9c46e..042d3683 -- packages/ apps/ tests/ docs/` and the same range over `scripts/self_use_queue.json` are both empty; every commit's insertion count is under 500. CLOSURE PRECONDITION 6's REGISTRATION OBLIGATION, DISCHARGED PER §3 ITEM 30: the open set was searched for this defect before any id was considered. `R-0784` (registered F109 R19, OPEN, evidence already added once by F110 R16 on job `6f74dd7367704fd5`) already describes exactly this class — a self-use run against `R-0418` (a reviewer-block-authoring-practice finding no builder can fix in code) blocking at the normal approval gate. This is the SAME defect recurring a THIRD time, on a THIRD job (`848fc4c67d7b405b`), on a THIRD feature branch, with the SAME proximate trigger F109's own original instance had — `repair_exhausted` after both repair rounds spent, rather than F110's `review_inconsistent` after one. Per item 30 this evidence is ADDED TO `R-0784` here rather than minted as a third id; `R-0784` remains OPEN, its fix unchanged and still owed to F258's generator (a tier-1 filter for reviewer-practice findings, or an explicit acceptance that some generated items will honestly block), not to F112. NO NEW ID IS MINTED, so the open set is unmoved at 278 (350 registered, 72 `Done:`). THE OUTCOME IS A NORMAL APPROVAL-GATE RESULT, NOT A ROUND FAILURE: the self-use rail executed end to end against a real local provider and correctly refused to promote unfinished work. NO PRODUCTION CODE WAS TOUCHED IN THE PRIMARY CHECKOUT. Closure precondition 6 is now DISCHARGED for F112 pending only the `consumed_by=F112` edit, which lands in the closure commit itself, not in this round.
<<<END RECORD21>>>

<<<BEGIN PLAN22>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use item SU-007 run round 21
(RECORD21: VERDICT PASS, booked this round; R-0784 gained a third
occurrence, no new id). Round 22 lands the Built State section
(precondition 4) and re-confirms remaining preconditions before closure.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 22 books RECORD21, then appends a "Built State — what F112
delivered" section to `docs/roadmap/features/T3_F112.md` (precondition
4 — the file has none yet). `remedy integrity_gate.run_integrity_checks()`
already reads all-PASS (precondition 3, reviewer-confirmed pre-round).
No production code touched.

## Next Steps

- Precondition 6's `consumed_by=F112` edit to `scripts/self_use_queue.json`
  lands in the closure commit itself, alongside STATUS/README.
- Evidence job (`job_evidence.create_manual_completion_bundle`), then the
  mandatory fresh review zip, per
  docs/roadmap/STATUS_closure_protocol.md steps 1-2.
- STATUS line authored by the reviewer, applied by the worker; README
  capability sync in the SAME commit (R-0154 pin).
- Final closure commit + PR; merge deferred to the next feature's start.

## Risks

- Split children inherit the parent's full files_hint and re-escalate
  themselves (harmlessly — DECISION F112 D8's own MEASURED section).
- The Design section's "raise cap" / "proceed-overcap once" options are
  deliberately unbuilt (DECISION F112 D9).
- R-0767 stays OPEN on the model-routing seam this feature's config
  borrows from; unrelated to F112.
- R-0784 (self-use/R-0418 curation gap) is OPEN and belongs to F258, not
  F112 — do not attempt to fix it here.
<<<END PLAN22>>>

<<<BEGIN BUILT_STATE>>>
## Built State — what F112 delivered

T001-T003 give every task a class-scoped input-token ceiling the context
compiler enforces via its existing demotion cascade, with a task-split
decision as the fallback when even tier-1 content alone cannot fit —
never a silently truncated prompt.

- `packages/orchestration/prompt_budget.py` — `resolve_task_class_cap`
  resolves one `TaskClassCapResolution` per call, precedence configured
  per-class cap (`config.prompt_budget.task_class_caps[class]`) over
  configured global default (`config.prompt_budget.default_cap`) over the
  shipped `DEFAULT_FALLBACK_CAP_TOKENS=24000` (matching
  `context_compiler.DEFAULT_CONTEXT_TOKEN_BUDGET`). Reuses
  `model_routing.TASK_CLASS_TIERS` as the ONE task-class vocabulary — a
  class routing does not recognize is refused outright, never silently
  capped. `validate_prompt_budget_config` enforces a hard floor,
  `MIN_TASK_CLASS_CAP_TOKENS=2000`, below which a cap could never hold a
  usable prompt.
- `packages/orchestration/context_compiler.py` —
  `fit_task_context_to_class_cap` (`ClassBudgetFit`) resolves the class's
  cap via `resolve_task_class_cap`, then runs the EXISTING
  `compile_task_context` demotion cascade unchanged at that budget — no
  new selection logic, only the class-specific number the cascade already
  enforces. `fits` is False exactly when tier-1 content alone still
  exceeds the cap after every tier-2/tier-3 candidate has been demoted or
  dropped, carrying `tier1_tokens`/`cap_tokens`/`task_class` for the
  `cannot_fit` decision.
- `packages/orchestration/pingpong_job.py` (`run_job`'s per-task loop,
  ~line 2434) — every task with a `files_hint` is fit to its class cap
  before `run_pingpong` runs. On fit: the task's own files/candidates and
  the resolved cap are used unchanged. On `cannot_fit`:
  `escalation.enqueue_task_decision` raises a `task_decision` (question
  "task context exceeds its class cap", the single option `"split task"`,
  `safe_default="split task"`, `impact` carrying the tier1/cap/class
  arithmetic verbatim — DECISION F112 D9), `auto_apply_safe_default`
  answers it unattended, and on "split task"
  `task_granularity.split_one_task` splits the oversized task into
  children inserted immediately after it in `job.tasks`; the parent is
  marked `TASK_SPLIT`, persisted, and skipped — never run truncated.
  `task_granularity.py`'s split heuristics themselves are UNFORKED, per
  the feature file's Do-not-touch.
- Design's "raise cap for this job" / "proceed-overcap once" options are
  deliberately UNBUILT (DECISION F112 D9): no audit or attended-mode seam
  exists anywhere in this codebase to hook them to today.
- Split children inherit the parent's full `files_hint` and so can
  re-escalate themselves against the SAME cap — harmless and MEASURED
  (DECISION F112 D8), not a defect: a child that still cannot fit splits
  again rather than running truncated.
- Tests: `tests/orchestration/test_class_prompt_budget.py` (24 cases,
  mutation-verified — resolver precedence, floor/vocabulary validation)
  and the two `context_compiler` fixtures naming the acceptance criteria
  directly, `test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded`
  and `test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic`.
- Full-suite integration gate PASSED (round 19): branch 19546 passed / 23
  skipped / 0 failed against merge base `5c28c674`, one base-only
  xdist-flake attributed, not coupled to F112 code.
<<<END BUILT_STATE>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading. Every gate runs at a commit STRICTLY
EARLIER than C4.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r22.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r22.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.
   Report `wc -l .agent/authored/f112-r22.md`.

G2 THE PLAN — extract PLAN22 by delimiter, compare byte-for-byte against
   `.agent/plan.md` at C2 — must be equal. Report `wc -l .agent/plan.md`
   (must be under 50), no trailing newline, `## Goal` and `## Next Steps`
   each exactly once.

G3 THE RECORD APPEND — extract RECORD21 by delimiter, report its byte
   length (expected 5338 — if it does not match, DECLARE the mismatch,
   apply the extracted bytes as-is, do not silently adjust the arithmetic
   below to compensate). Report the arithmetic
   `2293718 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL (flip one
   byte, recompute, report `False`), lines matching `^Gate: F112 R21 — `
   before (0) and after (1) C1, and registered/`Done:`/open counts on both
   sides (expected UNMOVED 350/72/278).

G4 THE BUILT STATE APPEND — extract BUILT_STATE by delimiter, report its
   byte length (expected 3520 — if it does not match, DECLARE the
   mismatch and apply the extracted bytes as-is). Report
   `docs/roadmap/features/T3_F112.md`'s pre-C3 size (expected 3970,
   ending WITH a trailing newline) and post-C3 size, with the arithmetic
   `3970 + 1 + <len> + 1 = <total>` against the real post-append size.
   Report the byte-prefix property (pre-C3 content is an exact prefix of
   post-C3 content) and that the file still ends WITH exactly one trailing
   newline (not zero, not two). Report `grep -c '^## Built State'` before
   (0) and after (1).

G5 THE TREE AND THE COMMITS — `git status --porcelain` immediately before
   C4 is staged — EMPTY. `git diff --stat 042d3683..<C3> -- packages/
   apps/ tests/` — must be EMPTY, and the same range over `docs/` other
   than `docs/roadmap/features/T3_F112.md` must also be EMPTY. PER-COMMIT
   INSERTIONS (the `+` column) for C0a through C3, each confirmed under
   500 by `git show --stat`.

Handback: rewrite `.agent/handoff.md` in full — feature and round, session
number, branch, base and head SHAs, per-commit changed-files table, ONE
line per gate above with its real reading, the item-status table
AGENTS.md mandates, deviations, the open-findings count (expected 278,
unmoved), and the next expected action (evidence job, review zip, STATUS
line, README sync, closure commit, PR — per PLAN22's Next Steps). It has
NO length cap. Do not write a `Done:` or `Gate:` paragraph anywhere
beyond applying RECORD21 verbatim. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══