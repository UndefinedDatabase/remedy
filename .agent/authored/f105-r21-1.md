── STEP R21 / F105 — closing round of this session ────────────
Goal:        Gate R20 on disk; resolve R-0249; register and FIX the
             unsatisfiable-gate class that has now cost five rounds across
             F104 and F105; bring `.agent/plan.md` back under its cap.
Bundle:      C1a save block · C1b mirror · C2 live_review (R20 gate, R-0249
             resolution, R-0250, next free ID) · C3 the process fix in
             docs/agents/planner_reviewer_prompt.md + DECISION F105 D8 ·
             C4 plan.md + handoff.md
Change:      exactly these paths, nothing else —
             `.agent/authored/f105-r21-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`, `docs/agents/planner_reviewer_prompt.md`.
Constraints: No production file, no test file. Do not edit AGENTS.md. Do not
             touch `docs/roadmap/ROADMAP.md`. This round's change set includes
             `docs/`, so the docs-round gate applies (see Done when D).
Handback:    completion report + rewrite `.agent/handoff.md`. This is the
             SESSION TERMINATOR: its own gate is owed to the next session's
             reviewer, per docs/agents/planner_reviewer_prompt.md §4.13. Say so
             in the handoff and do NOT open a repair round to close it.
───────────────────────────────────────────────────────────────

## Commit order

### C1a — save the block, ALONE
    git commit -m "chore(f105): save the R21 block verbatim"

### C1b — mirror to last_block
`cp .agent/authored/f105-r21-1.md .agent/last_block.md`, commit alone.
    git commit -m "chore(f105): mirror the R21 block to last_block"

### C2 — live_review: R20 gate, R-0249 resolved, R-0250 registered
Apply PAIR_A, PAIR_B, PAIR_C to `.agent/live_review.md`. One commit.
    git commit -m "chore(f105): record the R20 gate and register R-0250"

### C3 — the process fix
Apply PAIR_D to `docs/agents/planner_reviewer_prompt.md` and PAIR_E to
`.agent/decisions.md`. One commit — the rule and the DECISION that installs it
belong together.
    git commit -m "chore(f105): add the pre-emission block checklist and record DECISION D8"

### C4 — plan and handoff
Apply PAIR_F to `.agent/plan.md` (full replacement). Rewrite `.agent/handoff.md`.
    git commit -m "chore(f105): update the plan and close the session with the R21 handoff"

Then `git push -u origin feature/f105-cache-optimal-prompt-ordering`.

## Done when (run every command; record REAL exit codes and real output)

A. `sha256sum .agent/authored/f105-r21-1.md .agent/last_block.md` equal;
   `cmp` on the pair exits 0.
B. `wc -l .agent/authored/f105-r21-1.md` — must be <= 400. Report the number
   whatever it is; do not round it.
C. Application, per target file:
   `grep -c '^  Done: R-0249 ' .agent/live_review.md` -> 1
   `grep -c '^- R-0250 ' .agent/live_review.md` -> 1
   `grep -c '^- Reviewer gate on R20 ' .agent/live_review.md` -> 1
   `sed -n '8p' .agent/live_review.md` -> ends `Next free ID: R-0251.`
   `grep -c 'Pre-emission block checklist' docs/agents/planner_reviewer_prompt.md` -> 1
   `grep -c '^## DECISION F105 D8 ' .agent/decisions.md` -> 1
   `grep -c '^===BEGIN\|^===END' .agent/live_review.md .agent/decisions.md .agent/plan.md docs/agents/planner_reviewer_prompt.md` -> 0 for all four
   `wc -l .agent/plan.md` -> must be < 50. Report the number.
D. Docs-round gate (this round touches `docs/`):
   `python3 -m pytest tests/docs/ -q` (baseline 294 passed)
   `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` (baseline 70)
E. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` (baseline 42).
F. No red-proof is owed: this round changes no executable file. Say that
   explicitly rather than leaving the row blank, and create NO worktree.
G. After the C4 commit: `git status --porcelain` empty; `git worktree list`
   shows the primary alone; `git log --numstat 9cb128d7..HEAD` — report the `+`
   column per commit, each under 500.

## PAIR shapes, declared at authoring time

| Pair | Target | Shape |
|---|---|---|
| A | live_review | REWRITE — the TO drops the FROM's trailing " OPEN." |
| B | live_review | REWRITE |
| C | live_review | APPEND — TO contains FROM verbatim as its prefix |
| D | planner_reviewer_prompt | APPEND |
| E | decisions | APPEND |
| F | plan | full replacement, byte-for-byte equal to the slice |

REWRITE proof: FROM 0x after, TO 1x after. APPEND proof: FROM 1x after, each
TO-only line at least 1x. Every state/docs commit also reports its stray count
— added lines tracing to no authored TO slice — which must be 0.

===BEGIN PAIR_A_FROM===
  fix lands in this round's plan rewrite; the next gate verifies it and
  resolves this entry. OPEN.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  fix lands in this round's plan rewrite; the next gate verifies it and
  resolves this entry.
  Done: R-0249 — fixed at F105 R20 and verified at R21. `.agent/plan.md` now
  reads "step 4 covers `build_orchestrator_prompt` AND its system half
  `build_orchestrator_system_prompt`", so the plan and the migration order name
  the same work. The reviewer confirmed the wider reading was the correct one
  by reconstructing the pre-migration builders from
  `git show 04a3396d:packages/orchestration/orchestrator_loop.py` and diffing
  both renders: had only the inner function migrated, the outer f-string would
  still have concatenated a composed prompt with a raw `# Mission state`
  header, and the manifest would have described 3852 of 3861 characters instead
  of all of them. RESOLVED.
- R-0250 (Medium, F105 R20, reviewer-authored gates that cannot be satisfied):
  R20's block carried FOUR defects, all in reviewer-authored text and all
  correctly caught, declared and worked around by the worker rather than
  silently absorbed. (1) The block was 471 lines against DECISION D5's cap of
  400, and because a worker must save the block verbatim it could not be fixed
  downstream. (2) The authored `.agent/plan.md` replacement was 56 lines
  against AGENTS.md's <50, and a slice required to apply byte for byte cannot
  be trimmed by the applier — so a reviewer defect landed a live rule violation
  on disk. (3) Done-when C required
  `grep -c 'committed BEFORE any of them at C1b' .agent/decisions.md` to be 0,
  while the same block's PAIR_D_TO deliberately wrote that phrase into that
  same file as a quotation of the retired text: unsatisfiable by construction.
  (4) PAIR_F was declared APPEND when its TO edits the FROM line, making it a
  REWRITE. Defect (3) is the FIFTH instance of its class across F104 R11 and
  F105, and each instance costs a round a deviation that proves a reviewer
  mistake rather than a worker one. The common cause is that all four checks
  are mechanical, are known, and lived only in reviewer session memory — the A1
  trap named in docs/agents/planner_reviewer_prompt.md §0. Fix: a pre-emission
  checklist in that file's §3, installed as DECISION F105 D8 in the same round
  as this entry, so the next reviewer runs the checks off disk instead of
  remembering them. Fixed and resolved in this same round; the NEXT session's
  gate verifies the rule is on disk and reads as intended.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0250.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0251.
===END PAIR_B_TO===

===BEGIN PAIR_C_FROM===
  R-0249. `LAST_REVIEWED_SHA` advances c65d663e -> 04a3396d.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
  R-0249. `LAST_REVIEWED_SHA` advances c65d663e -> 04a3396d.
- Reviewer gate on R20 (2026-08-09, same session): PASS. Range
  `04a3396d..HEAD` at 9cb128d7, SIX commits, EIGHT paths, exactly the block's
  declared change set. Insertions from `git log --numstat`: 471, 422, 58, 89,
  232, 59 and 98, each under 500.
  The production claim was checked WITHOUT using the worker's golden as
  evidence. The reviewer reconstructed the pre-migration builders directly from
  `git show 04a3396d:packages/orchestration/orchestrator_loop.py`, confirmed the
  frozen f-string anchor is present in that source, rendered both the system
  prompt and the full prompt against two different contexts, and compared byte
  for byte: equal in every case, lengths 3861 and 3865. This site is therefore
  the first of the six whose migration is byte-EXACT rather than equal modulo
  ordering, which is what its pre-existing rank order made possible. The
  manifest reads `[('orchestrator_system', 0), ('orchestrator_protocol', 1),
  ('orchestrator_mission_state', 3)]`, ranks non-decreasing; across two
  contexts the two stable hashes are equal and only the mission-state hash
  differs; the shared prefix measures 3852 of 3861 characters, 99.77%, and runs
  past the end of the protocol segment; and the two-entry system manifest is
  the exact prefix of the three-entry one. The cache payoff is measured, not
  asserted.
  Gates re-run by the reviewer with real exit codes: the golden, the loop suite
  and the segment suite together 220 passed — 6 + 192 + 22, and 192 is
  unchanged from the pre-round baseline, so the migration added no test to the
  loop file and removed none; canary plus `tests/docs/` together 336 passed —
  42 + 294. A mutation red-proof of the REVIEWER's own choosing, distinct from
  the worker's three, ran in a disposable worktree at HEAD: M4 changed
  `orchestrator_mission_state`'s rank from JOB_CONTEXT to CONVENTIONS, which
  leaves the composed TEXT byte-identical because equal ranks tie-break on
  registration order. A text-only golden would have passed it.
  `test_manifest_carries_the_three_declared_segments_in_rank_order` went RED
  with `At index 2 diff: 1 != 3`, the suite returned to 6 passed on revert, and
  the worktree was removed and pruned — so the golden pins the declared rank
  and not merely the bytes. `git status --porcelain` empty and
  `git worktree list` the primary alone at the verdict.
  All seven declared deviations ACCEPTED. Deviation 7's `_register_orchestrator_prefix`
  helper exceeds what the block asked for and is kept as an improvement on it:
  it makes the manifest-prefix property hold by construction rather than by two
  registration lists agreeing, and the block's actual constraint — that
  `compose_orchestrator_prompt` build its own registry and list all three
  entries — holds. Deviation 5's adaptation of golden test 5 is correct and the
  block was wrong: a shared prefix cannot end exactly at the protocol segment,
  because the next segment opens with a constant header. Deviations 1-4 are the
  reviewer's own authoring defects, not the worker's, and are registered
  together as R-0250 rather than charged to this round. The handback declared
  every one of them, including two gates it could not satisfy, instead of
  reporting green — which is the behaviour the gate exists to reward.
  `LAST_REVIEWED_SHA` advances 04a3396d -> 9cb128d7.
===END PAIR_C_TO===

===BEGIN PAIR_D_FROM===
  Handback:    completion report + rewrite .agent/handoff.md
  ──────────────────────────────────────────────────────────────
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
  Handback:    completion report + rewrite .agent/handoff.md
  ──────────────────────────────────────────────────────────────

- **Pre-emission block checklist (DECISION F105 D8, finding R-0250).** Run all
  four checks mechanically, on the FINAL bytes, after the last edit, before any
  block leaves the reviewer. Each one has already cost this repository a round.
  1. **Size.** Count the block's lines. Over 400 (DECISION F105 D5) → split or
     cut BEFORE emitting. A worker must save the block verbatim, so an oversize
     block cannot be fixed downstream; it becomes a declared deviation on a
     round that did nothing wrong.
  2. **No self-counting gate.** A "must be 0" done-when may not count a string
     that any TO slice in the same block writes into that same file. Check every
     zero-gate against every TO that targets its file — including TOs that quote
     retired text on purpose, which is exactly how the R-0250 instance arose.
     Zero-gates over transport MARKER lines stay safe, because markers never
     reach a target file.
  3. **Cap-bounded replacements.** Count every authored full-replacement text
     against its own file's cap before emission: `.agent/plan.md` under 50 lines
     (AGENTS.md), `.agent/handoff.md` under 60 or carrying a DECISION D15
     stated-cause line. A worker required to apply a slice byte for byte cannot
     trim it, so an oversize replacement lands a live rule violation on disk and
     the worker is right to declare it rather than fix it.
  4. **Pair shape, verified not asserted.** Declare a pair APPEND only after
     checking that the TO literally CONTAINS the FROM (§4.9). A TO that edits
     the FROM line at all — dropping a trailing "OPEN.", rewrapping, changing
     punctuation — is a REWRITE, and mislabelling it makes the worker prove the
     wrong property.
  Why this is on disk and not a habit: item 2 has recurred five times across
  F104 and F105, and R20 hit all four items in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
===END PAIR_D_TO===

===BEGIN PAIR_E_FROM===
when it does it declares the staleness window it is accepting, in its own
entry.

Reverse this decision by deleting this entry.
===END PAIR_E_FROM===

===BEGIN PAIR_E_TO===
when it does it declares the staleness window it is accepting, in its own
entry.

Reverse this decision by deleting this entry.

## DECISION F105 D8 — the pre-emission block checklist (2026-08-09)

Context: finding R-0250. Round 20's authored block carried four defects, every
one of them mechanical and every one of them catchable by looking at the block's
own bytes before sending it: it ran 471 lines against DECISION D5's 400-line
cap; its `.agent/plan.md` replacement ran 56 lines against AGENTS.md's <50; one
of its done-when gates required a grep to return 0 for a phrase the same block
deliberately wrote into that same file; and one pair was declared APPEND when
its TO edits the FROM line. The worker caught all four, declared all four, and
worked around them correctly — the round was not damaged. What it cost was a
round's worth of deviations spent proving reviewer mistakes, and the
zero-gate defect was the fifth of its kind across F104 and F105.

D8 — the four checks become a numbered checklist in
docs/agents/planner_reviewer_prompt.md §3, run mechanically on a block's final
bytes before it is emitted. Recurrence, not severity, is the argument: no single
instance of these justifies a rule, and five instances of one of them do. The
checks are cheap — three counts and one substring test — and they are the kind
of thing a reviewer is certain it will remember and then does not.

The alternative, a validator script that lints a block before emission, was
rejected FOR NOW rather than on the merits. It would be strictly better, and it
would also be production code written by the reviewer role to police the
reviewer role, which the split workflow does not currently have a shape for. If
the checklist proves insufficient, that script is the next move and this entry
is where it should be argued.

Scope: reviewer-authored blocks. It adds no obligation to workers and changes
no verification tier. It is a pre-flight check on text the reviewer is about to
send, nothing more.

Reverse this decision by deleting this entry and the §3 checklist it installs.
===END PAIR_E_TO===

===BEGIN PAIR_F===
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
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`),
3 (`flight_plan.py`) and 4 (`orchestrator_loop.py` — BOTH
`build_orchestrator_prompt` and its system half) are COMPLETE and GATED, each
with its own golden. `LAST_REVIEWED_SHA` is 9cb128d7. R21 is the session
terminator: it changed no production file, so only its state and docs are
ungated. Open findings: R-0221, R-0239, R-0246, R-0247. No PR; one is created
at CLOSURE.

## Next Steps
- R22 gates R21 FIRST (state + docs only, no red-proof owed), then takes
  migration-order step 5, `pingpong_loop.py::_build_builder_prompt` — twelve
  conditional parts and a `"\n".join` whose blank-line runs must be reproduced
  exactly. Highest-risk site so far; give it a fresh session.
- Then step 6, `pingpong_loop.py::_build_reviewer_prompt`, last and highest
  content-equality risk of the six.
- BEFORE step 5, decide whether the schema tail from `build_schema_prompt` /
  `native_schema_prompt` becomes a registered rank-4 segment. Until then every
  manifest for sites 1-4 describes a strict prefix of the bytes actually sent.
- ONE later round wires `on_call` for all three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator, deferred by R20), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Register the Phase-0 gap the R17 gate records: the protocol gives no
  disposition for a tree a dead session left dirty. Not yet a DECISION.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Four of the six migrated builders still reach no call evidence, so F105's
  every-role acceptance line is met for intake only until that round lands.
===END PAIR_F===
