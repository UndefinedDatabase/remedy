── STEP T003 migration-order step 2 / R16 — F105 ─────────────────────────────
Goal:        Record the R15 gate, settle the cap that stalled two rounds, and
             move `mission_compiler.py::build_mission_prompt` onto the prompt-
             segment registry under a new content-equality golden. This is the
             first block on this branch that carries a gate record AND a feature
             change, which is R-0243's resolution condition.
Bundle:      C1a save block · C1b mirror block · C2 findings · C3 gate record ·
             C4 decisions D4+D5 · C5 the migration + its golden · C6 state.
Change:      `.agent/authored/f105-r16-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`,
             `packages/orchestration/mission_compiler.py`,
             `tests/orchestration/test_mission_prompt_golden.py` (new),
             `.agent/plan.md`, `.agent/handoff.md`. Nothing else.
Constraints: AGENTS.md is the highest authority. DECISION F105 D5 below governs
             this block's own commit split and its 400-line cap; this block is
             399 lines, measured by the reviewer before delegation. Prompt
             CONTENT does not change — only composition. Every authored text is
             SLICED out of `.agent/authored/f105-r16-1.md` between its markers,
             never retyped. The pre-migration template is obtained with
             `git show` and sliced by line index, never retyped. `Done:` text is
             reserved for the reviewer; mark a landed fix `Landed: R-XXXX`.
             Mutation red-proofs run ONLY in a disposable `git worktree`
             (self_drive_protocol G5). Never force-push, never work on main.
Done when:   Gates A-H below all pass with real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────────────────────

## C1a — save this block, alone

Copy `.remedy-wt/f105-r16-1.block.md` to `.agent/authored/f105-r16-1.md`, not
editing a byte, and commit that file ALONE:

    chore(f105): save the R16 block verbatim

## C1b — mirror it to last_block.md, alone

Copy the same bytes to `.agent/last_block.md`. Commit that file ALONE:

    chore(f105): mirror the R16 block to last_block

Under DECISION F105 D5 (C4) C1b is a verbatim rewrite of a SINGLE `.agent/**`
state file named in the AGENTS.md Commit Discipline exemption, so its insertions
are exempt. C1a is NOT exempt and must stay under 500; it is 399.

## C2 — findings persist FIRST

Apply pairs A and B to `.agent/live_review.md`, commit alone:

    chore(f105): register R-0244 and amend R-0243

Pair A is APPEND-shaped: the TO contains the FROM verbatim. Prove FROM 1x before
and 1x after, and each TO-only added line 1x after. Pair B is a REWRITE: FROM
and TO are disjoint, so prove FROM 1x before / 0x after and TO 0x before / 1x
after.

===BEGIN PAIR_A_FROM===
  reviewer-written record the worker copies from scratch, the way this block's
  own bytes already travel. OPEN.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  reviewer-written record the worker copies from scratch, the way this block's
  own bytes already travel. OPEN.
  Fix chosen at the R15 gate (2026-08-09) as DECISION F105 D5, written at C4 of
  this block: the block stops being counted twice. C1 splits into C1a, which
  commits `.agent/authored/<round>.md` alone and counts its N insertions against
  the AGENTS.md 500 cap, and C1b, which rewrites `.agent/last_block.md` alone —
  the verbatim rewrite of a SINGLE `.agent/**` state file named in the AGENTS.md
  Commit Discipline exemption, and therefore exempt exactly as written, with no
  rule reinterpreted. D2's rejected alternative is not revived: the block still
  meets a 500-line ceiling at C1a, so the pressure keeping blocks short survives
  and only the doubling artifact goes. The cap moves 240 -> 400. R-0243 stays
  OPEN until a round lands a gate record AND a feature change out of one block —
  the condition R16 is built to meet, held to the same discipline as R-0238,
  which was resolved on a landing and not on a promise.
- R-0244 (Low, F105 R15, reviewer-authored defect): the authored `.agent/plan.md`
  text is 54 lines against the AGENTS.md plan.md rule "keep it short (<50
  lines)". The R14 plan was 49 and inside it; R15 regressed past it while
  compressing its block four times, so the lines the block saved were spent in
  the state file instead. The worker declared the overage and correctly refused
  to trim reviewer-authored text, so the defect is the reviewer's alone.
  AGENTS.md is the highest authority and no rule of it may be weakened by an
  authoring convenience; a plan outgrowing its own cap is also the first symptom
  of a plan turning into a log, which is what the cap exists to prevent. Fix:
  the authored plan slice is counted before it is emitted and lands at 49 lines
  or fewer. Applied at C6 of this block. OPEN until it lands.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0244.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0245.
===END PAIR_B_TO===

## C3 — record the R15 gate

Apply pair C to `.agent/live_review.md`, commit alone:

    chore(f105): record the R15 gate

Pair C is APPEND-shaped. Same proof obligation as pair A.

===BEGIN PAIR_C_FROM===
  migration and DECISION F105 D4 move to R16. The session revised its declared
  cap from two rounds to three, stated in this block rather than taken
  silently, and R15's own gate is owed at R16.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
  migration and DECISION F105 D4 move to R16. The session revised its declared
  cap from two rounds to three, stated in this block rather than taken
  silently, and R15's own gate is owed at R16.
- Reviewer gate on R15 (2026-08-09): PASS. Range `73e159b7..HEAD` at ed5b2421,
  four commits, FIVE paths, all under `.agent/`. Per-commit insertions read by
  the reviewer from `git log --numstat`: 388 (227 + 161), 38, 26 and 96
  (66 + 30) — each under the 500 cap. The R15 handoff left C4's number to the
  completion report; it is 96, derived here rather than accepted. Transport is
  proved against a SURVIVING original: `.remedy-wt/f105-r15-1.block.md`,
  `.agent/authored/f105-r15-1.md` and `.agent/last_block.md` all hash to
  b0bbc7d6, both `cmp` runs exit 0, at 227 lines / 14333 bytes, 13 under D2's
  cap. Application is proved disk to disk, not by retype: of the 64 lines the
  range adds to `.agent/live_review.md`, 64 occur verbatim in the authored file
  and 0 are missing, and the single removed line is exactly pair B's FROM, so
  the rewrite landed where it was aimed and nowhere else. `.agent/plan.md`
  equals its authored slice at block lines 155-208, sha256 4fb762f5 both sides.
  Gates re-run by the reviewer with real exit codes: state contracts 4 passed /
  47 deselected; `tests/docs/` 294 passed; canary `tests/cli/test_golden_path.py`
  42 passed; integrity `passed=True`, `fail_count=0` over 5 checks;
  `git status --porcelain` empty; `git worktree list` the primary alone; HEAD
  equal to origin. Deviations 1, 2 and 5 ACCEPTED — the D15 handoff overage is
  mandated content only, the `bash -c` exit-code transport was re-run directly
  by the reviewer with identical results, and `.remedy-wt/` is ignored at
  `.gitignore:235` with nothing tracked. Deviation 3 is R-0242's own declared
  condition and stays with it. Deviation 4 is NOT waved through: a 54-line
  `.agent/plan.md` breaks an AGENTS.md rule, and it is registered as R-0244. One
  defect found, the reviewer's own. `LAST_REVIEWED_SHA` advances
  73e159b7 -> ed5b2421.
- R16: the round that ends the record-only stall — the R15 gate recorded, R-0244
  registered, R-0243 amended with its chosen fix, DECISIONS F105 D4 and D5
  written, and migration-order step 2,
  `mission_compiler.py::build_mission_prompt`, moved onto the registry under a
  new `tests/orchestration/test_mission_prompt_golden.py`. The mission manifest
  does NOT reach call evidence this round: no production caller passes `on_call`
  to `plan_mission` (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`), so that seam is its own
  later round, exactly as intake split across R11 and R12. R16's own gate is
  owed at R17.
===END PAIR_C_TO===

## C4 — the two decisions

Apply pair D to `.agent/decisions.md`, commit alone:

    chore(f105): record DECISION F105 D4 and D5

Pair D is APPEND-shaped and its FROM is the file's last three lines. Anchor on
all three: the closing sentence alone occurs many times in this file.

===BEGIN PAIR_D_FROM===
at R13, the first `.agent/`-only round after it.

Reverse this decision by deleting this entry.
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
at R13, the first `.agent/`-only round after it.

Reverse this decision by deleting this entry.

## DECISION F105 D4 — the mission rules segment is CAP-SCOPED (2026-08-09)

`build_mission_prompt` interpolates `{max_milestones}` into the middle of its
rules list, and `packages/orchestration/gauntlet_runner.py:505` varies that cap
per caller (`max_milestones=len(order.milestones) + 1`). Registering the rules
as a rank-1 CONVENTIONS segment therefore cannot make the F105 acceptance claim
"identical prefix bytes across consecutive calls within a role" true
unconditionally. It is true PER CAP VALUE.

A byte-preserving split into a constant head and a parameterised tail was
considered and rejected: both interpolations sit mid-list, the segment delimiter
is a plain blank line (DECISION F105 D1), and the rules list contains no blank
line to split on. Any split reaching them would insert bytes the pre-migration
prompt does not have — precisely the content change T003 must not make.

D4 — the rules are registered WHOLE as `mission_rules`, and the cap scoping is
made visible instead of assumed. A one-line WHY comment sits directly above the
constant, where a reader searches, and
`tests/orchestration/test_mission_prompt_golden.py` pins the scope: equal caps
produce an identical `mission_rules` hash, different caps produce different
`mission_rules` hashes while every other segment hash is unchanged. The claim
becomes testable rather than hopeful, and its honest limit is on disk.

Reverse this decision by deleting this entry.

## DECISION F105 D5 — the step block is counted once, cap 400 (2026-08-09)

Context: finding R-0243. DECISION F105 D2 caps a step block at 240 lines because
C1 wrote the block to BOTH `.agent/authored/<round>.md` and
`.agent/last_block.md` in ONE commit, so N authored lines cost 2N insertions
against the AGENTS.md 500 cap. But the mandated record content of a reviewed
round — the gate verdict, the registrations and resolutions, the header pair and
the verbatim `.agent/plan.md` — costs roughly 150 lines before any feature work
is described, leaving under 90 for instruction. R14 and R15 both degraded into
record-only rounds and merged no feature change. The cap had begun doing harm.

D5 — C1 splits in two. C1a commits `.agent/authored/<round>.md` ALONE and its N
insertions count normally against the 500 cap. C1b rewrites
`.agent/last_block.md` ALONE, which is the verbatim rewrite of a SINGLE
`.agent/**` state file named in the AGENTS.md Commit Discipline exemption list,
and is therefore exempt exactly as written. The step-block cap becomes 400
authored lines, measured by the reviewer BEFORE delegation and stated in the
block itself.

This does not revive the alternative D2 rejected. D2 declined to exempt the C1
PAIR from counting, on the ground that block length is a free authorial choice
and an exemption would remove the only pressure keeping blocks short. That
pressure survives in full: C1a still meets the 500-line ceiling and 400 sits 100
under it. What ends is the DOUBLE counting, an accounting artifact of writing one
artifact twice in one commit rather than any measure of how long the block is.
Splitting an oversize commit is also the remedy AGENTS.md prescribes in its own
words, so no rule is reinterpreted and no exemption is widened.

Reverse this decision by deleting this entry, and restore D2's 240 with it.
===END PAIR_D_TO===

## C5 — the migration and its golden

Commit both files together:

    chore(f105): compose the mission prompt from registered segments

### C5.1 the golden FIRST

Create `tests/orchestration/test_mission_prompt_golden.py`, modelled on the
existing `tests/orchestration/test_intake_prompt_golden.py` — read that file
first and follow its shape, its docstring discipline and its naming.

Its frozen `_PRE_MIGRATION_MISSION_TEMPLATE` is obtained with
`git show ed5b2421:packages/orchestration/mission_compiler.py`, sliced by LINE
INDEX (lines 77-108, the `_MISSION_PROMPT_TEMPLATE` assignment) and pasted in
whole. Not one byte is retyped. Its docstring states, as the intake golden's
does, that the constant must NEVER be edited to make a failing test pass.

Determinism without a new seam: pass an explicit single-paragraph
`project_facts` and a single-line `goal`, so splitting a rendered prompt on the
segment delimiter yields exactly one part per segment. That `build_mission_prompt`
already accepts `project_facts` is why this site is second in the migration order.

Tests, at least these five:
1. the composed segment SET equals the pre-migration parts modulo ordering —
   `sorted(composed_parts) == sorted(frozen_parts)` and the sorted manifest
   hashes equal the sorted frozen-part hashes, exactly the intake golden's
   first test;
2. the rules now compose AHEAD of the goal: `Rules` precedes `## Mission Goal`
   in the composed text and follows it in the frozen render, and the composed
   text equals `"\n\n".join([system, rules, repo_facts, goal, directive])`
   sliced out of the frozen render's own parts;
3. manifest names and ranks are exactly
   `("mission_system", "mission_rules", "mission_repo_facts", "mission_goal",
   "mission_schema_directive")` with ranks `(0, 1, 2, 4, 5)`;
4. D4's cap scoping: two calls at the SAME `max_milestones` give an identical
   `mission_rules` hash; two calls at DIFFERENT caps give different
   `mission_rules` hashes while all four other segment hashes are unchanged;
5. `build_mission_prompt(...) == compose_mission_prompt(...).text` for both a
   `None` cap and an explicit cap, and the `None` cap reproduces the frozen
   render BYTE FOR BYTE — including its trailing newline.

### C5.2 the migration

In `packages/orchestration/mission_compiler.py`, replace the single
`_MISSION_PROMPT_TEMPLATE` with five module constants whose bytes are SLICED out
of the existing template, never retyped, split at its blank lines:

- `_MISSION_SYSTEM_SEGMENT` — template lines 78-79 (`You are compiling …
  reach it.`), rank SYSTEM.
- `_MISSION_GOAL_TEMPLATE` — `## Mission Goal` + `{goal}`, rank TASK.
- `_MISSION_REPO_FACTS_TEMPLATE` — `## Repo Facts` + `{repo_facts}`, rank
  DOSSIER.
- `_MISSION_RULES_TEMPLATE` — `## Rules` through `… never deletes, overwrites or
  migrates.`, rank CONVENTIONS. Keep its `{{` / `}}` escapes exactly as they
  stand: this constant is now `.format`ted on its own.
- `_MISSION_SCHEMA_DIRECTIVE_TEMPLATE` — `Return ONLY a JSON object matching the
  {schema_v} schema.` followed by a TRAILING NEWLINE. That newline is load
  bearing: the old template ended with one, `compose_prompt_segments` adds none,
  and dropping it is a one-byte content change that test 5 will catch.

Add `compose_mission_prompt(goal, *, project_facts="", max_milestones=None)
-> ComposedPrompt`, mirroring `packages/orchestration/intake.py`'s
`compose_intake_prompt`: build a `PromptSegmentRegistry`, register the five
segments in the order listed above, and return
`compose_prompt_segments(registry.registered_segments())`. Rank order then
composes system · rules · repo facts · goal · directive.
`build_mission_prompt` keeps its signature, its docstring and every caller, and
becomes `return compose_mission_prompt(...).text`.

Above the rules constant put the one-line WHY comment D4 requires, naming the
cap scoping; above `compose_mission_prompt` put the kind the intake composer
carries, naming what moved and why.

Do NOT touch `resolve_milestone_cap`, `_capped_draft_model`,
`compile_mission_plan`, `plan_mission`, or any caller. Do NOT add `on_call`
wiring — that is a later round.

## C6 — state

Replace `.agent/plan.md` with the text between the markers below, VERBATIM and
whole, then rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
Commit both:

    chore(f105): update the plan and write the R16 handoff

Then `git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR:
F105's PR comes at CLOSURE.

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
(R-0241). Step 1, `intake.py::_build_intake_prompt`, is COMPLETE. R16 records
the R15 gate and takes migration-order step 2,
`mission_compiler.py::build_mission_prompt`, in ONE block under DECISION F105
D5, which counts the block once and caps it at 400. `LAST_REVIEWED_SHA` is
ed5b2421. Open findings: R-0221, R-0239, R-0242, R-0243, R-0244. No PR; one is
created at CLOSURE. The candidates file is empty.

## Next Steps
- R17 gates R16, then takes migration-order step 3,
  `flight_plan.py::_build_plan_prompt`, which needs a `repo_facts` injection
  seam before its golden can be deterministic.
- Then migration-order steps 4 to 6, ONE builder per round, each with its own
  golden: `orchestrator_loop.py::build_orchestrator_prompt`, then
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- The mission manifest reaches call evidence in its own later round: no
  production caller passes `on_call` to `plan_mission`
  (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`), so that seam is a separate
  change from this composition move.
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

## Done when — gates A-H, real exit codes recorded

Run each and record the REAL exit code and trimmed output in the handoff.

    A  cmp .remedy-wt/f105-r16-1.block.md .agent/authored/f105-r16-1.md
       cmp .agent/authored/f105-r16-1.md .agent/last_block.md
    B  wc -l .agent/authored/f105-r16-1.md          # 399, at or under D5's 400
    C  grep -c "^- R-0244 " .agent/live_review.md   # exactly 1
       sed -n 8p .agent/live_review.md              # ends "Next free ID: R-0245."
    D  python3 -m pytest tests/orchestration/test_mission_prompt_golden.py -q
    E  python3 -m pytest tests/orchestration/test_mission_compiler.py \
         tests/orchestration/test_prompt_segments.py -q   # 135 before AND after
    F  python3 -m pytest tests/orchestration/test_test_runner.py -q \
         -k "live_review or context_md or plan_md"
       python3 -m pytest tests/docs/ -q
    G  python3 -m pytest tests/cli/test_golden_path.py -q          # canary
       python3 -m apps.cli.grouped integrity check --json
    H  git status --porcelain                       # EMPTY
       git worktree list                            # primary alone
       git log --numstat --format='%h %s' ed5b2421..HEAD   # each commit's +

Mutation red-proof, MANDATORY, in a disposable worktree at HEAD and nowhere else
(self_drive_protocol G5): prove the new golden is load bearing on all three axes
— reorder two registrations, change ONE word inside the rules constant, and drop
the trailing newline from the schema-directive constant — recording how many
tests each turns RED. Remove and prune the worktree BEFORE the handback.

Report in the handoff: the changed-files table per commit with real +/- numbers,
the gate table above with real exit codes, the pair proofs (shape, FROM/TO
counts) for A, B, C and D, the three mutation results, an item-status table
covering C1a, C1b, C2, C3, C4, C5 and C6, and every deviation you took with its
reason. A `Done:` paragraph is the reviewer's to write — mark anything you land
`Landed: R-XXXX` and nothing else.
