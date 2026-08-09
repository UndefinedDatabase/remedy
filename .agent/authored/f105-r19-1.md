── STEP R19 — F105 · record the R18 gate and close the session ───────────────
Goal:        Pay the gate R18 earned — the first round on this branch to land
             production code — register the one defect the review found, and
             close the session with a handoff. NO feature work: this round is
             deliberately state-only so that the round left ungated at the
             session boundary is the cheap one, not the one with code in it.
Bundle:      C1a save block · C1b mirror block · C2 findings · C3 gate record ·
             C4 state.
Change:      `.agent/authored/f105-r19-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. NO production file, NO test file.
Constraints: AGENTS.md is the highest authority. DECISION F105 D5 governs the
             commit split and the 400-line cap; this block is 230 lines,
             measured by the reviewer before delegation. Every authored text is
             SLICED out of `.agent/authored/f105-r19-1.md` between its markers,
             never retyped; no marker line may enter a target file. `Done:` and
             gate text is the reviewer's — apply it verbatim. Per DECISION F105
             D6 the plan rewrite is this round's LAST commit and needs no
             deviation line. Never force-push, never work on main, no PR.
Done when:   Gates A-E below pass with real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────────────────────

## C1a — save this block, alone

Copy `.remedy-wt/f105-r19-1.block.md` to `.agent/authored/f105-r19-1.md`, not
editing a byte, and commit that file ALONE:

    chore(f105): save the R19 block verbatim

## C1b — mirror it to last_block.md, alone

Copy the same bytes to `.agent/last_block.md`. Commit that file ALONE:

    chore(f105): mirror the R19 block to last_block

## C2 — findings persist FIRST

Apply pairs A and B to `.agent/live_review.md`, commit alone:

    chore(f105): register R-0248

Pair A is APPEND-shaped: prove FROM 1x before and 1x after, and each TO-only
line 1x after. Pair B is a REWRITE: FROM 1x before / 0x after, TO 0x before /
1x after.

===BEGIN PAIR_A_FROM===
  finding is pasted from that command's own output in the same sitting. OPEN.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  finding is pasted from that command's own output in the same sitting. OPEN.
- R-0248 (Low, F105 R18, defect in a DECISION's account of its own mechanism):
  DECISION F105 D6, landed this round, says the Commit Gate's plan check is met
  for a round's intermediate commits by `.agent/last_block.md`, "which carries
  the round's plan verbatim and is committed BEFORE any of them at C1b". C1a
  commits `.agent/authored/<round>.md` and C1a runs BEFORE C1b — D5 split them
  in that order precisely so the block is counted once. So exactly one commit
  per round, the first, is not covered by the mechanism D6 names, and D6's
  "before any of them" is false for it. The worker declared the gap rather than
  reordering, which was right: reordering C1a after C1b would defeat D5. The
  SUBSTANCE of D6 is unaffected — C1a adds a file that is a verbatim copy of
  the block, so the plan of record and the commit agree by construction, which
  is the very thing D6 argues makes the mechanism sound. What is wrong is the
  word "any", which overclaims coverage a reader can falsify in one `git log`.
  Fix: D6's sentence names C1b onward, and states that C1a is covered by being
  the block's own verbatim copy rather than by `.agent/last_block.md`. Amend the
  entry in place, in the round that next touches `.agent/decisions.md`. OPEN.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0248.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0249.
===END PAIR_B_TO===

## C3 — record the R18 gate

Apply pair C to `.agent/live_review.md`, commit alone:

    chore(f105): record the R18 gate

===BEGIN PAIR_C_FROM===
  moment the round resumed. `LAST_REVIEWED_SHA` advances efd66b68 -> 70156f31.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
  moment the round resumed. `LAST_REVIEWED_SHA` advances efd66b68 -> 70156f31.
- Reviewer gate on R18 (2026-08-09, same session, paid in-session and NOT
  deferred because R18 is the first round on this branch to land production
  code): PASS. Range `70156f31..HEAD` at c65d663e, SEVEN commits, EIGHT paths,
  exactly the block's declared change set. Insertions from `git log --numstat`:
  400, 296, 18, 27, 38, 246 and 91, each under 500; C1b's 296 is the verbatim
  rewrite of one state file. Transport: `.remedy-wt/f105-r18-2.block.md`,
  `.agent/authored/f105-r18-2.md` and `.agent/last_block.md` all hash to
  a89262c0, both `cmp` exit 0, 400 lines — exactly D5's cap, measured before
  delegation. Application proved disk to disk by the reviewer's own script: all
  SIX pairs land in their declared shape, A, B, D, E, F appending with FROM
  surviving 1x and TO fresh 1x, C rewriting the header with its FROM gone; zero
  marker LINES in `.agent/live_review.md`, `.agent/decisions.md` or
  `.agent/plan.md`; `.agent/plan.md` equals its slice byte for byte, 46 lines,
  sha256 2b80abaf. Nothing else entered the state files: of 51, 32 and 13 added
  lines across the three, every one traces to an authored TO slice and the stray
  count is 0.
  The production claim was checked without using the worker's test as evidence.
  `_PRE_MIGRATION_PLAN_TEMPLATE` is byte-identical to `_PLAN_PROMPT_TEMPLATE` as
  it stood at 70156f31 — same sha256 ca5f325d after normalising only the
  constant's NAME, and the two exec to equal values — so the golden is pinned to
  the real prior text and not to a retyped copy of it. Reconstructing the OLD
  builder from 70156f31 and rendering both: on two different intakes, the new
  composition reordered back into template order equals the old render exactly,
  the lengths match, and the sorted part SETS are equal. Content equality modulo
  ordering therefore holds against the pre-migration code itself, not merely
  against a constant in a test file. The cacheable-prefix payoff was measured,
  not asserted: two calls differing only in intake now share a 1437-character
  prefix of a 1505-character prompt, and only `plan_intake` changes hash.
  Gates re-run by the reviewer, real exit codes: golden 5 passed; bundled
  clarification + prompt segments 60 passed, identical to the pre-round baseline
  of 60 so the migration added no test to that pair and removed none; state
  contracts 4 passed / 47 deselected; `tests/docs/` 294 passed; canary 42
  passed; integrity `passed=True`, `fail_count=0` over 5 checks. Beyond the
  block's gates the reviewer ran the FULL `tests/orchestration/` suite — 10452
  passed, 7 skipped, exit 0 in 661s — plus every test file that names
  `flight_plan`, 309 and 487 passed, so the new keyword-only seam broke no
  caller. Mutation red-proofs were re-run by the reviewer in a fresh disposable
  worktree, not taken from the handback: M1 rank swap, M2 dropped trailing
  newline, M3 deleted `plan_repo_facts` — each RED, each with the block's
  expected named test among the failures, and the suite green again after every
  revert. Worktree removed and pruned; `git status --porcelain` empty,
  `git worktree list` the primary alone, HEAD equal to origin.
  All six declared deviations ACCEPTED. Deviation 4's `passed:false` on
  `relevant_untracked` before the C5 commit is the check working as designed on
  a not-yet-committed new file, not a failure. Deviation 3's added docstring
  exceeds what the block mandated but documents the seam the block introduced
  and touches no caller; kept. The 115-line handoff is inside DECISION D15: it
  declares its own count, names the cap and names the mandated content, and
  `wc -l` returns the number it declares. One defect found, R-0248, in DECISION
  D6's account of its own mechanism. `LAST_REVIEWED_SHA` advances
  70156f31 -> c65d663e.
===END PAIR_C_TO===

## C4 — state

Replace `.agent/plan.md` with the text between the markers below, VERBATIM and
whole, then rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
This is the round's LAST commit. Commit both:

    chore(f105): update the plan and close the session with the R19 handoff

Then `git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR:
F105's PR comes at CLOSURE.

The handoff states plainly that R19 is the SESSION TERMINATOR, that its own
gate is owed to the next session's reviewer, and that R19 changed no production
file — so the owed gate covers state only.

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
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`) and
3 (`flight_plan.py`) are COMPLETE and GATED, each with its own content-equality
golden. `LAST_REVIEWED_SHA` is c65d663e. R19 is the session terminator and
changed no production file, so only its state is ungated. Open findings:
R-0221, R-0239, R-0246, R-0247, R-0248. No PR; one is created at CLOSURE.

## Next Steps
- R20 gates R19 FIRST, then takes migration-order step 4,
  `orchestrator_loop.py::build_orchestrator_system_prompt`.
- Then steps 5 and 6, ONE builder per round, each with its own golden:
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Fix R-0248 in the round that next touches `.agent/decisions.md`, and R-0246
  in the round that next touches `mission_compiler.py`.
- Register the Phase-0 gap the R17 gate records: the protocol gives no
  disposition for a tree a dead session left dirty. Not yet a DECISION.
- The mission and plan manifests reach call evidence in their own later round:
  no production caller passes `on_call` to `plan_mission`
  (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`) and none passes it to
  `plan_job_llm` (`apps/cli/commands/do_cmd.py:253` and `:2860`).
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Three of the six builders still reach no call evidence, so F105's every-role
  acceptance line is met for intake only.
===END PLAN_MD===

## Done when — gates A-E, real exit codes recorded

    A  cmp .remedy-wt/f105-r19-1.block.md .agent/authored/f105-r19-1.md
       cmp .agent/authored/f105-r19-1.md .agent/last_block.md
    B  wc -l .agent/authored/f105-r19-1.md          # 230, under D5's 400
    C  grep -c "^- R-0248 " .agent/live_review.md   # exactly 1
       grep -c "^- Reviewer gate on R18 " .agent/live_review.md   # exactly 1
       sed -n 8p .agent/live_review.md              # ends "Next free ID: R-0249."
    D  python3 -m pytest tests/orchestration/test_test_runner.py -q \
         -k "live_review or context_md or plan_md"
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/cli/test_golden_path.py -q          # canary
       python3 -m apps.cli.grouped integrity check --json
    E  git status --porcelain                       # EMPTY
       git worktree list                            # primary alone
       git log --numstat --format='%h %s' c65d663e..HEAD

No mutation red-proof is owed: this round changes nothing executable. Do NOT
create a worktree. Do NOT touch any file outside the change set above.

Report the per-commit changed-files table with real +/- numbers, the gate table
with real exit codes, the pair proofs (shape, FROM/TO counts) for A, B and C,
the item-status table over C1a-C4, and every deviation with its reason.
