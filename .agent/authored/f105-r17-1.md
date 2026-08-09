── STEP R17 — F105 · session-terminator round ────────────────────────────────
Goal:        Persist the R16 gate and its findings, resolve what R16 actually
             earned, and close this session with a handoff. NO builder is
             migrated: R17 is a record round by design, not by cap pressure.
Bundle:      C1a save block · C1b mirror block · C2 findings · C3 gate record ·
             C4 plan + session-end handoff.
Change:      `.agent/authored/f105-r17-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. No production code this round.
Constraints: AGENTS.md is the highest authority. DECISION F105 D5 governs the
             commit split and the 400-line cap; this block is 257 lines,
             measured by the reviewer before delegation. Every authored text is
             SLICED out of `.agent/authored/f105-r17-1.md` between its markers,
             never retyped; no marker line may enter a target file. `Done:` text
             is the reviewer's — it is authored below, so apply it verbatim.
             Never force-push, never work on main, create no PR.
Done when:   Gates A-E below pass with real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────────────────────

## C1a — save this block, alone

Copy `.remedy-wt/f105-r17-1.block.md` to `.agent/authored/f105-r17-1.md`, not
editing a byte, and commit that file ALONE:

    chore(f105): save the R17 block verbatim

## C1b — mirror it to last_block.md, alone

Copy the same bytes to `.agent/last_block.md`. Commit that file ALONE:

    chore(f105): mirror the R17 block to last_block

## C2 — findings persist FIRST

Apply pairs A, B and C to `.agent/live_review.md`, commit alone:

    chore(f105): resolve R-0243 and R-0244 and register R-0245 and R-0246

Pairs A and B are APPEND-shaped: prove FROM 1x before and 1x after, and each
TO-only line 1x after. Pair C is a REWRITE: FROM 1x before / 0x after, TO 0x
before / 1x after.

===BEGIN PAIR_A_FROM===
  which was resolved on a landing and not on a promise.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  which was resolved on a landing and not on a promise.
  Done: R-0243 (resolved at the R16 gate, 2026-08-09). The condition this
  finding set for itself — one block landing a gate record AND a feature change
  — was met by R16 at 399 authored lines under DECISION F105 D5's cap of 400:
  the R15 gate record, two registrations, two DECISIONS, and migration-order
  step 2 with its golden, out of a single block, in seven commits whose largest
  is 399 insertions and none of which exceeds 500. The reviewer confirmed the
  counts from `git log --numstat` rather than from the handback. The forced
  split is gone because the block is no longer counted twice. RESOLVED.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
  the authored plan slice is counted before it is emitted and lands at 49 lines
  or fewer. Applied at C6 of this block. OPEN until it lands.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
  the authored plan slice is counted before it is emitted and lands at 49 lines
  or fewer. Applied at C6 of this block. OPEN until it lands.
  Done: R-0244 (resolved at the R16 gate, 2026-08-09). `.agent/plan.md` is 47
  lines and equals its authored slice byte for byte, sha256 8029c8ca on both
  sides, confirmed by the reviewer on disk. Inside the AGENTS.md cap with two
  lines to spare. RESOLVED.
- R-0245 (Low, F105 R16, worker record defect): `.agent/handoff.md` is 101 lines
  against the AGENTS.md cap of 60 — 100 where per-commit tables of more than
  five commits require it — and declares neither the overage nor its line count.
  DECISION D15 permits a stated-cause overage precisely so that a long handoff
  stays honest, and it requires the file to name its actual length and the
  mandated content that caused it; the R15 handoff did exactly that at 135
  lines. The same file also omits the item-status table AGENTS.md requires of
  every completion report covering an ordered bundle. The worker DID put one in
  its completion report to the reviewer, but that report dies with the session
  and the file is the only channel that survives it. Nothing is padded and
  nothing is fabricated; what is missing is the declaration and the table. Fix:
  a handoff over cap states its line count and its cause, and every handoff
  covering an ordered bundle carries the item-status table. OPEN.
- R-0246 (Low, F105 R16, reviewer-authored defect): `build_mission_prompt`'s
  docstring still ends "``None`` reproduces today's prompt byte for byte".
  Before R16 that sentence was about the `max_milestones` parameter alone and
  was unambiguous. After a migration whose entire point is that segment ORDER
  changed while segment BYTES did not, a reader landing on that line — and it is
  exactly where a search for "did the migration change the prompt?" lands — can
  read it as a claim that the byte SEQUENCE was preserved, which is false. The
  R16 block mandated that the docstring be kept unchanged, so the defect is the
  reviewer's and not the worker's. Fix: the sentence says what it means — a
  `None` cap reproduces the pre-R-0197 milestone ceiling, while the composed
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
===END PAIR_B_TO===

===BEGIN PAIR_C_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0245.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0247.
===END PAIR_C_TO===

## C3 — record the R16 gate

Apply pair D to `.agent/live_review.md`, commit alone:

    chore(f105): record the R16 gate

Pair D is APPEND-shaped. Same proof obligation as pairs A and B.

===BEGIN PAIR_D_FROM===
  later round, exactly as intake split across R11 and R12. R16's own gate is
  owed at R17.
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
  later round, exactly as intake split across R11 and R12. R16's own gate is
  owed at R17.
- Reviewer gate on R16 (2026-08-09): PASS, and it is the first PASS on this
  branch over a round that carried production code. Range `ed5b2421..HEAD` at
  efd66b68, SEVEN commits, EIGHT paths, exactly the block's declared change set
  with nothing beside it. Per-commit insertions from `git log --numstat`: 399,
  366, 24, 35, 55, 255 (73 + 182) and 88 (63 + 25) — each under 500, so D5's
  exemption for C1b was not even load bearing this round. Transport: the
  reviewer's surviving original `.remedy-wt/f105-r16-1.block.md`,
  `.agent/authored/f105-r16-1.md` and `.agent/last_block.md` all hash to
  744fe981, both `cmp` runs exit 0, 399 lines against D5's cap of 400.
  Application proved disk to disk: of the 59 lines added to
  `.agent/live_review.md` and the 55 added to `.agent/decisions.md`, all 114
  occur verbatim in the authored file and 0 are missing; the single removed line
  is exactly pair B's FROM; no `===BEGIN` or `===END` marker reached any target
  file. `.agent/plan.md` equals its authored slice, sha256 8029c8ca both sides.
  The golden's frozen `_PRE_MIGRATION_MISSION_TEMPLATE` was diffed by the
  reviewer against `git show ed5b2421:packages/orchestration/mission_compiler.py`
  lines 78-108 and is byte-identical — 31 lines, exit 0 — so the golden pins the
  real pre-migration prompt and not a retyping of it. `grep` for
  `_MISSION_PROMPT_TEMPLATE` across `packages/ apps/ tests/` returns only the
  golden's own docstring, so the migration left no straggler, and
  `build_mission_prompt`'s one production caller at `mission_compiler.py:338` is
  untouched. Gates re-run by the reviewer with real exit codes: the golden 5
  passed; `test_mission_compiler.py` + `test_prompt_segments.py` 135 passed,
  the same 135 the reviewer measured at ed5b2421 BEFORE the round; state
  contracts 4 passed / 47 deselected; `tests/docs/` 294 passed; canary 42
  passed; integrity `passed=True`, `fail_count=0` over 5 checks;
  `git status --porcelain` empty; `git worktree list` the primary alone; HEAD
  equal to origin. The reviewer re-ran mutation M3 independently in a disposable
  worktree at efd66b68 and reproduced the worker's result exactly — dropping the
  schema directive's trailing newline turns the same THREE named tests RED — and
  added a fourth axis the round did not claim: deleting the `mission_repo_facts`
  registration turns SIX tests RED, including one pre-existing
  `test_mission_compiler.py` test, so the golden is load bearing on segment loss
  as well as on order, wording and that one byte. The worktree was removed and
  pruned before this verdict. All five declared deviations ACCEPTED. Deviations
  3 and 4 are better than what was asked for: literal whole-string equality is
  impossible once composition reorders, and the reordered-join assertion is the
  strongest true reading; and reporting the no-op statement swap as control M0
  instead of dressing it up as a red proof is the honesty this loop runs on.
  Two defects found, R-0245 and R-0246, one the worker's record and one the
  reviewer's own text. R-0243 and R-0244 RESOLVE here.
  `LAST_REVIEWED_SHA` advances ed5b2421 -> efd66b68.
- R17: the session-terminator round — R-0243 and R-0244 resolved, R-0245 and
  R-0246 registered, the R16 gate recorded, the session-end handoff written. The
  session ends at its DECLARED TWO-ROUND CAP (R16 building, R17 recording) under
  docs/agents/self_drive_protocol.md G7. R17 ends a SESSION, not the branch, so
  its own gate is OWED and the next session's reviewer records it first
  (§4.13 as corrected by R-0233). No production code changed this round.
===END PAIR_D_TO===

## C4 — plan and session-end handoff

Replace `.agent/plan.md` with the text between the markers below, VERBATIM and
whole, then rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
Commit both:

    chore(f105): close the session with the R17 handoff

Your handoff MUST fix R-0245 in its own shape: state its line count and the
mandated content causing any overage, and carry an item-status table covering
C1a, C1b, C2, C3 and C4. Then
`git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR.

===BEGIN PLAN_MD===
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). Migration-order steps 1 (`intake.py::_build_intake_prompt`) and 2
(`mission_compiler.py::build_mission_prompt`) are COMPLETE and gated, each with
its own content-equality golden. DECISION F105 D5 ended the record-only stall:
the step block is counted once and capped at 400, so R16 carried a gate record
AND a migration in one block. `LAST_REVIEWED_SHA` is efd66b68. Open findings:
R-0221, R-0239, R-0242, R-0245, R-0246. No PR; one is created at CLOSURE.

## Next Steps
- R18 gates R17 FIRST — R17's own gate is owed — then takes migration-order
  step 3, `flight_plan.py::_build_plan_prompt`, which needs a `repo_facts`
  injection seam before its golden can be deterministic.
- Then migration-order steps 4 to 6, ONE builder per round, each with its own
  golden: `orchestrator_loop.py::build_orchestrator_prompt`, then
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Fix R-0246 in the same round that next touches `mission_compiler.py`: the
  docstring's "byte for byte" sentence now reads as a claim about composition.
- The mission and plan manifests reach call evidence in their own later round:
  no production caller passes `on_call` to `plan_mission`
  (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`).
- Settle R-0242: whether intra-round commits are exempt from the AGENTS.md
  Commit Gate plan.md check, or the plan rewrite moves earlier in the block.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Four of the six builders still reach no call evidence, so F105's every-role
  acceptance line is met for intake only.
===END PLAN_MD===

## Done when — gates A-E, real exit codes recorded

    A  cmp .remedy-wt/f105-r17-1.block.md .agent/authored/f105-r17-1.md
       cmp .agent/authored/f105-r17-1.md .agent/last_block.md
    B  wc -l .agent/authored/f105-r17-1.md          # 257, at or under D5's 400
    C  grep -c "^- R-0245 " .agent/live_review.md   # exactly 1
       grep -c "^- R-0246 " .agent/live_review.md   # exactly 1
       sed -n 8p .agent/live_review.md              # ends "Next free ID: R-0247."
    D  python3 -m pytest tests/orchestration/test_test_runner.py -q \
         -k "live_review or context_md or plan_md"
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/cli/test_golden_path.py -q          # canary
       python3 -m apps.cli.grouped integrity check --json
    E  git status --porcelain                       # EMPTY
       git worktree list                            # primary alone
       git log --numstat --format='%h %s' efd66b68..HEAD

No mutation red-proof this round: nothing executable changed. Report the
per-commit changed-files table with real +/- numbers, the gate table with real
exit codes, the pair proofs (shape, FROM/TO counts) for A, B, C and D, the
item-status table, and every deviation with its reason.
