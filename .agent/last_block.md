── STEP R18 — F105 · migration-order step 3 ──────────────────────────────────
Goal:        Record the R17 gate, resolve what R17 earned, settle R-0242, and
             migrate `flight_plan.py::_build_plan_prompt` to registered
             segments behind a content-equality golden — the third of the six
             T003 builders.
Bundle:      C0 restore · C1a save · C1b mirror · C2 findings · C3 gate record
             · C4 DECISION D6 and R-0242 · C5 migration and golden · C6 state.
Change:      `.agent/authored/f105-r18-2.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`,
             `packages/orchestration/flight_plan.py`,
             `tests/orchestration/test_plan_prompt_golden.py`,
             `.agent/plan.md`, `.agent/handoff.md`. Nothing else.
Constraints: AGENTS.md is the highest authority. DECISION F105 D5 governs the
             commit split and the 400-line cap; this block is 400 lines,
             measured by the reviewer before delegation. Every authored text is
             SLICED out of `.agent/authored/f105-r18-2.md` between its markers,
             never retyped; no marker line may enter a target file. `Done:`
             text is the reviewer's — it is authored below, so apply it
             verbatim. Prompt CONTENT does not change; only its composition.
             Never force-push, never work on main, create no PR.
Done when:   Gates A-H below pass with real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────────────────────

## C0 — restore the tree this block was authored against, NO commit

A first R18 attempt halted on an operator `.agent/STOP`, applied nothing, and
died before its halt commit landed; `.agent/STOP` is already gone. Preserve the
two modified files, then restore — do NOT commit them and do NOT edit them:

    cp .agent/handoff.md .remedy-wt/f105-r18-attempt1-handoff.md
    cp .agent/plan.md    .remedy-wt/f105-r18-attempt1-plan.md
    git checkout -- .agent/handoff.md .agent/plan.md
    git status --porcelain          # EMPTY before C1a

## C1a — save this block, alone

Copy `.remedy-wt/f105-r18-2.block.md` to `.agent/authored/f105-r18-2.md`, not
editing a byte, and commit that file ALONE:

    chore(f105): save the R18 block verbatim

## C1b — mirror it to last_block.md, alone

Copy the same bytes to `.agent/last_block.md`. Commit that file ALONE:

    chore(f105): mirror the R18 block to last_block

## C2 — findings persist FIRST

Apply pairs A, B and C to `.agent/live_review.md`, commit alone:

    chore(f105): resolve R-0245 and register R-0247

Pairs A and B are APPEND-shaped: prove FROM 1x before and 1x after, and each
TO-only line 1x after. Pair C is a REWRITE: FROM 1x before / 0x after, TO 0x
before / 1x after.

===BEGIN PAIR_A_FROM===
  covering an ordered bundle carries the item-status table. OPEN.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  covering an ordered bundle carries the item-status table. OPEN.
  Done: R-0245 (resolved at the R17 gate, 2026-08-09). `.agent/handoff.md` is
  92 lines; `wc -l` returns 92, and the file's opening section declares that
  same number, names the AGENTS.md cap it exceeds and names the mandated content
  that caused the overage. The item-status table is present with all five bundle
  items, and both halves of the fix landed in the file that survives the
  session. RESOLVED.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
- R-0247 (Low, F105 R17, reviewer-authored defect in a finding's own citation):
  R-0245 opens "`.agent/handoff.md` is 101 lines". The file is 100:
  `git show efd66b68:.agent/handoff.md | wc -l` returns 100 and the blob ends in
  a newline, so no counting convention closes the gap — the number came from a
  draft, not from the command that produced it. The SUBSTANCE is untouched: 100
  exceeds the cap of 60 exactly as 101 would, and the missing declaration and
  item-status table are what the finding was about, both of which R17 fixed.
  Wrong is a cited number the reader cannot reproduce — the R-0234 and R-0239
  class, third instance on this branch, and each time it costs a run deciding
  between a typo and a file that changed underneath. Fix: any count entering a
  finding is pasted from that command's own output in the same sitting. OPEN.
===END PAIR_B_TO===

===BEGIN PAIR_C_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0247.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0248.
===END PAIR_C_TO===

## C3 — record the R17 gate

Apply pair D to `.agent/live_review.md`, commit alone:

    chore(f105): record the R17 gate

===BEGIN PAIR_D_FROM===
  its own gate is OWED and the next session's reviewer records it first
  (§4.13 as corrected by R-0233). No production code changed this round.
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
  its own gate is OWED and the next session's reviewer records it first
  (§4.13 as corrected by R-0233). No production code changed this round.
- Reviewer gate on R17 (2026-08-09, opening a NEW session under
  docs/agents/self_drive_protocol.md): PASS. The owed gate is paid first, before
  any new work was planned. Range `efd66b68..HEAD` at 70156f31: FIVE commits,
  FIVE paths, all under `.agent/`, the block's declared change set exactly, no
  production code. Insertions from `git log --numstat`: 257, 160, 38, 48, 65
  (51 + 14), each under 500; C1b's 160 needed no D5 exemption. Transport:
  `.remedy-wt/f105-r17-1.block.md`, `.agent/authored/f105-r17-1.md` and
  `.agent/last_block.md` all hash to 8db0b6d7, both `cmp` exit 0, 257 lines
  under D5's 400. Application proved disk to disk by the reviewer's own script:
  each of the four TO slices occurs in `.agent/live_review.md` exactly ONCE;
  A, B, D are appends whose FROM survives 1x, C is the header rewrite whose FROM
  is gone; no marker LINE reached a target — the one `===BEGIN` present is a
  finding quoting the token in prose. `.agent/plan.md` at 70156f31 equals its
  slice byte for byte, sha256 49527b18, 48 lines; R-0244's claim re-checked, the
  file at efd66b68 is 47 lines and hashes to 8029c8ca as stated. Gates re-run,
  real exit codes: state contracts 4 passed / 47 deselected; `tests/docs/` 294
  passed; canary 42 passed; integrity `passed=True`, `fail_count=0` over 5
  checks; `git worktree list` primary alone; HEAD equal to origin. All five
  declared deviations ACCEPTED; no mutation red-proof owed, nothing executable
  changed. R-0245 RESOLVES here; one defect found, R-0247, the reviewer's own.
  `git status --porcelain` was NOT empty: a first R18 attempt halted on an
  operator `.agent/STOP`, applied nothing, and died before its halt commit
  landed, leaving `.agent/handoff.md` and `.agent/plan.md` uncommitted; 70156f31
  and the R17 range are untouched by it. Disposition for a dirty Phase 0 tree:
  COPY the pair to `.remedy-wt/`, then restore to HEAD, never commit it — its
  plan.md reads BLOCKED, which the Commit Gate's item 1 would make false the
  moment the round resumed. `LAST_REVIEWED_SHA` advances efd66b68 -> 70156f31.
===END PAIR_D_TO===

## C4 — settle R-0242

Append pair E to `.agent/decisions.md` and pair F to `.agent/live_review.md`.
Commit both together:

    chore(f105): record DECISION F105 D6 and resolve R-0242

===BEGIN PAIR_E_FROM===
Reverse this decision by deleting this entry, and restore D2's 240 with it.
===END PAIR_E_FROM===

===BEGIN PAIR_E_TO===
Reverse this decision by deleting this entry, and restore D2's 240 with it.

## DECISION F105 D6 — the plan rewrite closes a round (2026-08-09)

Context: finding R-0242, open since R14 and declared as a deviation by every
worker since. AGENTS.md's Commit Gate item 1 verifies `.agent/plan.md` against
the current work before EVERY commit. Every block on this branch rewrites
`.agent/plan.md` in its LAST commit, so the intermediate commits of a round
carry the PREVIOUS round's plan. Read literally, each of those commits fails
item 1; read as the branch has actually run for eighteen rounds, none of them
does. An unpersisted convention is exactly the class this loop registers as a
finding, so it gets a rule or it gets abandoned.

D6 — within one delegated round, `.agent/plan.md` is rewritten in the round's
LAST commit and the Commit Gate's plan check is satisfied for the round's
intermediate commits by `.agent/last_block.md`, which carries the round's plan
verbatim and is committed BEFORE any of them at C1b. The plan of record for an
in-flight round is the block; `.agent/plan.md` states where the FEATURE stands,
and mid-round it stands nowhere new yet.

The alternative — rewrite `.agent/plan.md` first — was rejected because it
makes the file claim work that has not landed. A plan that reads "step 3 is
complete" in the commit before step 3 is written is a worse record than one
that is a round behind, and it would resolve R-0242 by manufacturing the
overclaim class this repository's Proof Chain exists to prevent. Being one
round behind is visible and honest; being one round ahead is not.

Scope: one round, one worker. It exempts nothing across rounds — a round that
ends without rewriting `.agent/plan.md` still fails item 1, and D6 is not a
licence to leave the file stale. Blocks stop declaring the ordering as a
deviation and cite this entry instead.

Reverse this decision by deleting this entry.
===END PAIR_E_TO===

===BEGIN PAIR_F_FROM===
  inventing a rule in a terminator round is how unreviewed conventions start.
  OPEN.
===END PAIR_F_FROM===

===BEGIN PAIR_F_TO===
  inventing a rule in a terminator round is how unreviewed conventions start.
  OPEN.
  Done: R-0242 (2026-08-09) — RESOLVED as DECISION F105 D6, recorded in
  `.agent/decisions.md` at this round's C4. The convention is on disk with its
  reason and scope: within one round the plan rewrite closes the round, and the
  Commit Gate's plan check is met for the intermediate commits by
  `.agent/last_block.md`, which lands at C1b before any of them. D6 takes the
  exempting branch and says why the earlier-rewrite branch was refused.
===END PAIR_F_TO===

## C5 — the migration and its golden

Commit both files together:

    chore(f105): compose the flight plan prompt from registered segments

### C5.1 the golden FIRST

Create `tests/orchestration/test_plan_prompt_golden.py`, modelled on the
existing `tests/orchestration/test_mission_prompt_golden.py` — read that file
first and follow its shape, its docstring discipline and its naming.

Its frozen `_PRE_MIGRATION_PLAN_TEMPLATE` is obtained with
`git show 70156f31:packages/orchestration/flight_plan.py`, sliced by LINE INDEX
(lines 39-72, the `_PLAN_PROMPT_TEMPLATE` assignment) and pasted in whole. Not
one byte is retyped. Its docstring states, as the mission golden's does, that
the constant must NEVER be edited to make a failing test pass.

Determinism NEEDS the new seam here, and that is why this site is third in the
migration order rather than second: `_build_plan_prompt` calls
`repo_facts_block()` itself, which reads the working directory, so a golden
pinned in CI would differ from one pinned locally. Pass an explicit
single-paragraph `project_facts` and a SMALL fixed intake dict whose
`json.dumps(..., indent=2)` contains no blank line, so splitting a rendered
prompt on the segment delimiter yields exactly one part per segment.

Tests, at least these five:
1. the composed segment SET equals the pre-migration parts modulo ordering —
   `sorted(composed_parts) == sorted(frozen_parts)` and the sorted manifest
   hashes equal the sorted frozen-part hashes;
2. the rules now compose AHEAD of the intake: `## Rules` precedes `## Intake`
   in the composed text and follows it in the frozen render, and the composed
   text equals `"\n\n".join([system, rules, repo_facts, intake, directive])`
   sliced out of the frozen render's own parts;
3. manifest names and ranks are exactly `("plan_system", "plan_rules",
   "plan_repo_facts", "plan_intake", "plan_schema_directive")` with ranks
   `(0, 1, 2, 4, 5)`;
4. the rules, system and directive segments are INTAKE-INDEPENDENT: two calls
   with different intake dicts give identical hashes for those three and a
   different hash for `plan_intake`. That is the cacheable-prefix claim this
   migration exists to make, and unlike the mission rules these bytes carry no
   caller-varied parameter, so the claim is unconditional here;
5. `_build_plan_prompt(intake, project_facts=...)` equals
   `compose_flight_plan_prompt(intake, project_facts=...).text`, and
   reordering the composed parts back into the pre-migration order reproduces
   the frozen render BYTE FOR BYTE — trailing newline included.

### C5.2 the migration

In `packages/orchestration/flight_plan.py`, replace the single
`_PLAN_PROMPT_TEMPLATE` with five module constants whose bytes are SLICED out of
the existing template, never retyped, split at its blank lines:

- `_PLAN_SYSTEM_SEGMENT` — template lines 40-42 (`You are a project planner …
  and token band estimates.`), rank SYSTEM. A plain constant, not a template.
- `_PLAN_INTAKE_TEMPLATE` — `## Intake` + `{intake_json}`, rank TASK.
- `_PLAN_REPO_FACTS_TEMPLATE` — `## Repo Facts` + `{repo_facts}`, rank DOSSIER.
- `_PLAN_RULES_SEGMENT` — `## Rules` through `… that is the default.`, rank
  CONVENTIONS. It carries NO placeholder, so it is a plain constant and is
  never `.format`ted — do not add braces and do not escape anything.
- `_PLAN_SCHEMA_DIRECTIVE_SEGMENT` — `Return ONLY a JSON object matching the
  flight_plan_v1 schema.` followed by a TRAILING NEWLINE. That newline is load
  bearing: the old template ended with one, `compose_prompt_segments` adds none,
  and dropping it is a one-byte content change that test 5 will catch. Also a
  plain constant.

Add `compose_flight_plan_prompt(intake_dict, *, project_facts="")
-> ComposedPrompt`, mirroring `mission_compiler.py`'s `compose_mission_prompt`:
build a `PromptSegmentRegistry`, register the five segments in the order listed
above, and return `compose_prompt_segments(registry.registered_segments())`.
Rank order then composes system · rules · repo facts · intake · directive.

`_build_plan_prompt` keeps its name and its positional parameter, GAINS the
keyword-only `project_facts: str = ""` seam, and becomes
`return compose_flight_plan_prompt(intake_dict, project_facts=project_facts).text`.
The default `""` falls back to `repo_facts_block()` inside the composer exactly
as `build_mission_prompt` does, so `plan_job_llm` at line 347 and the three
existing `test_bundled_clarification.py` callers are unaffected and stay green
without edit. Do NOT edit those tests.

Above `_PLAN_RULES_SEGMENT` put the one-line WHY comment AGENTS.md's
discoverability rules require, naming that these bytes carry no caller-varied
parameter and are therefore stable across every planner call; above
`compose_flight_plan_prompt` put the kind `compose_mission_prompt` carries,
naming what moved and why, and stating that the segment BYTES are unchanged and
only their ORDER differs.

Do NOT touch `plan_job_llm`, `map_flight_plan_to_tasks`, `replan`, the
clarification helpers, or any caller. Do NOT add `on_call` wiring and do NOT
route the manifest into evidence — that is its own later round, and this round's
acceptance says nothing about it.

## C6 — state

Replace `.agent/plan.md` with the text between the markers below, VERBATIM and
whole, then rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
Per DECISION F105 D6 this is the round's LAST commit and needs no deviation
line. Commit both:

    chore(f105): update the plan and write the R18 handoff

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
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`) and
3 (`flight_plan.py`) are COMPLETE, each with its own content-equality golden;
step 3 also added the `project_facts` seam its golden needed.
`LAST_REVIEWED_SHA` is 70156f31 — R18's own gate is owed. Open findings:
R-0221, R-0239, R-0246, R-0247. No PR; one is created at CLOSURE.

## Next Steps
- R19 gates R18 FIRST, then takes migration-order step 4,
  `orchestrator_loop.py::build_orchestrator_system_prompt`.
- R19 also registers the Phase-0 gap the R17 gate records: the protocol gives
  no disposition for a tree a dead session left dirty. Not yet a DECISION.
- Then steps 5 and 6, ONE builder per round, each with its own golden:
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Fix R-0246 in the same round that next touches `mission_compiler.py`: the
  docstring's "byte for byte" sentence now reads as a claim about composition.
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

## Done when — gates A-H, real exit codes recorded

    A  cmp .remedy-wt/f105-r18-2.block.md .agent/authored/f105-r18-2.md
       cmp .agent/authored/f105-r18-2.md .agent/last_block.md
    B  wc -l .agent/authored/f105-r18-2.md          # 400, exactly D5's cap
    C  grep -c "^- R-0247 " .agent/live_review.md   # exactly 1
       grep -c "^## DECISION F105 D6 " .agent/decisions.md   # exactly 1
       sed -n 8p .agent/live_review.md              # ends "Next free ID: R-0248."
    D  python3 -m pytest tests/orchestration/test_plan_prompt_golden.py -q
       python3 -m pytest tests/orchestration/test_bundled_clarification.py \
         tests/orchestration/test_prompt_segments.py -q     # 60 before this round
    E  python3 -m pytest tests/orchestration/test_test_runner.py -q \
         -k "live_review or context_md or plan_md"
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/cli/test_golden_path.py -q          # canary
       python3 -m apps.cli.grouped integrity check --json
    F  git status --porcelain                       # EMPTY
       git worktree list                            # primary alone
       git log --numstat --format='%h %s' 70156f31..HEAD
    G  BASELINE, measured BEFORE any edit, at 70156f31 — the reviewer measured
       60 passed, exit 0, at this session's probe; confirm it still reads 60:
       python3 -m pytest tests/orchestration/test_bundled_clarification.py \
         tests/orchestration/test_prompt_segments.py -q
       Gate D's second command must return the same number plus nothing — the
       golden is a new FILE, so it adds to D's first command only.
    H  MUTATION red-proofs, in a DISPOSABLE `git worktree` only (G5), each
       reverted before the next, the worktree removed and pruned before the
       handback. Report which named tests turn RED for each:
       M1  register `plan_intake` at rank CONVENTIONS so it composes ahead of
           the rules — expect the ordering test RED.
       M2  drop the trailing newline from `_PLAN_SCHEMA_DIRECTIVE_SEGMENT` —
           expect the byte-for-byte test RED.
       M3  delete the `plan_repo_facts` registration — expect the segment-set
           test RED.
       If any mutation leaves the suite GREEN, that is the finding: report it
       as such and do not adjust the mutation until it goes red.

Report the per-commit changed-files table with real +/- numbers, the gate table
with real exit codes, the pair proofs (shape, FROM/TO counts) for A through F,
the item-status table over C0-C6, and every deviation with its reason.
