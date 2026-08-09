── STEP R22 / F105 — record the R21 gate, settle the schema tail, migrate site 5 ────
Goal:        Put the R21 gate on disk; settle the deferred schema-tail question
             as DECISION F105 D9 with a test that PROVES the prefix claim; then
             take migration-order step 5, `_build_builder_prompt`, under a
             content-equality golden.
Bundle:      C1a save block · C1b mirror · C2 live_review (R21 gate) ·
             C3 DECISION D9 + its prefix pin · C4 the site-5 migration + its
             golden · C5 plan.md + handoff.md
Change:      exactly these paths, nothing else —
             `.agent/authored/f105-r22-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`, `packages/orchestration/pingpong_loop.py`,
             `tests/orchestration/test_prompt_segments.py`,
             `tests/orchestration/test_builder_prompt_golden.py` (new).
Constraints: Prompt CONTENT does not change — only its composition. Do not edit
             AGENTS.md, `docs/roadmap/ROADMAP.md`, or any other builder. Do not
             touch `_build_reviewer_prompt` (that is step 6). No `docs/` path is
             in this change set, so the docs-round gate does NOT apply. Every
             red-proof runs ONLY in a disposable `git worktree`.
Handback:    completion report + rewrite `.agent/handoff.md` (cap 60 lines, or a
             DECISION D15 stated-cause line naming the mandated content).
──────────────────────────────────────────────────────────────────────────────

## Commit order

### C1a — save the block, ALONE
Save this block verbatim to `.agent/authored/f105-r22-1.md`, nothing else.
    git commit -m "chore(f105): save the R22 block verbatim"

### C1b — mirror to last_block
`cp .agent/authored/f105-r22-1.md .agent/last_block.md`, commit alone.
    git commit -m "chore(f105): mirror the R22 block to last_block"

### C2 — live_review: the R21 gate
Apply PAIR_A to `.agent/live_review.md`. One commit.
    git commit -m "chore(f105): record the R21 gate"

### C3 — the schema-tail decision and its pin
Apply PAIR_B to `.agent/decisions.md`. In the SAME commit add the pin test
described under "C3 spec" below to `tests/orchestration/test_prompt_segments.py`.
    git commit -m "test(f105): pin the schema tail as a delimiter-joined suffix"

### C4 — migration-order step 5
`packages/orchestration/pingpong_loop.py` + the new golden
`tests/orchestration/test_builder_prompt_golden.py`, per "C4 spec" below.
    git commit -m "refactor(f105): compose the builder prompt from segments"

### C5 — plan and handoff
Apply PAIR_C to `.agent/plan.md` (full replacement). Rewrite `.agent/handoff.md`.
    git commit -m "chore(f105): update the plan and hand back R22"

Then `git push -u origin feature/f105-cache-optimal-prompt-ordering`.

## C3 spec — DECISION D9's pin

D9 (PAIR_B) rules that the structured-call schema tail does NOT become a
registered segment in T003. That ruling rests on one property: the tail is a
SUFFIX joined with exactly `PROMPT_SEGMENT_DELIMITER`, so a composed manifest
describes a strict PREFIX of the bytes sent and the cacheable prefix is
untouched. Today that property is a claim. Add ONE test class to
`tests/orchestration/test_prompt_segments.py` that proves it:

- `native_schema_prompt(base)` starts with `base + PROMPT_SEGMENT_DELIMITER`
  and is strictly longer than `base`.
- `build_schema_prompt(<any schema model already imported by that test file, or
  a two-field local pydantic model>, base)` does the same.
- Both hold with a retry hint passed as well — the hint extends the SUFFIX and
  never the prefix, so `prompt.startswith(base)` still holds.

Import `PROMPT_SEGMENT_DELIMITER` from `packages.orchestration.prompt_segments`
rather than writing `"\n\n"` — the point of the test is that the two constants
are the same constant.

## C4 spec — migrate `_build_builder_prompt`

The reviewer verified before authoring this block that the decomposition below
reproduces today's render BYTE FOR BYTE in pre-migration order across all 64
combinations of the six optional arguments. It is satisfiable; a mismatch is a
real defect, not a bad spec.

### Segments — name, rank, and which of today's `parts` entries it owns

| Segment | Rank | Owns (today's parts, in order) |
|---|---|---|
| `builder_system` | 0 SYSTEM | `_BUILDER_SYSTEM`, then the bare `"\n"` |
| `builder_scope_contract` | 2 DOSSIER | `f"{scope_contract}\n\n"` (optional) |
| `builder_context` | 3 JOB_CONTEXT | `context`, then the bare `"\n"` |
| `builder_staged_state` | 3 JOB_CONTEXT | the `## Current Staged State` part |
| `builder_staged_diff` | 3 JOB_CONTEXT | the `## Current Staged Diff` part |
| `builder_test_result` | 3 JOB_CONTEXT | the `## Test Result` part |
| `builder_task` | 4 TASK | the `## Task (Round N)` part |
| `builder_task_body` | 4 TASK | the `## Detailed Task Instructions` part |
| `builder_repair` | 5 STEERING | the repair header, the rules block, and every finding line INCLUDING the trailing `""` entries |
| `builder_directive` | 5 STEERING | `"\nProvide your changes and a summary of what you did."` |

Every optional segment keeps EXACTLY today's condition, including the two that
are gated on `findings` as well as their own value (`safe_diff and findings`,
`test_result and findings`). Reproduce those conditions, do not simplify them.

### The boundary rule — the one thing that is easy to get wrong

Today the parts are joined with `"\n"`. Segments join with
`PROMPT_SEGMENT_DELIMITER`, which is `"\n\n"`. So each boundary must give back
exactly one newline. Build each segment's text as `"\n".join(its own parts)`,
then for every segment except the LAST:

- if that text ends with `"\n"`, drop that one trailing newline;
- else if the NEXT segment's text starts with `"\n"`, drop that one leading
  newline instead;
- else the boundary is illegal — raise rather than guess. It cannot happen for
  the decomposition above, and an assertion is how a future edit finds out.

Do not normalise any other whitespace. The blank-line runs in today's output
(four newlines after the system block, three before the directive) are CONTENT;
flattening them would change the prompt, which this feature forbids.

### Shape of the code

Mirror `orchestrator_loop.py` (the site-4 precedent):

- `compose_builder_prompt(...) -> ComposedPrompt` takes exactly today's
  signature, registers the segments through `PromptSegmentRegistry`, and returns
  `compose_prompt_segments(registry.registered_segments())`.
- `_build_builder_prompt(...)` keeps its signature and its callers, and becomes
  `return compose_builder_prompt(...).text`.
- A one-line WHY comment sits directly above `compose_builder_prompt` naming
  the two rank inversions this migration fixes (see below) and stating that the
  golden is therefore equal-modulo-ordering, not byte-exact.

### What the reorder changes, stated so the golden can assert it

Two inversions exist today and rank order fixes both:

1. `builder_scope_contract` (rank 2) currently follows `builder_context`
   (rank 3) and now precedes it.
2. `builder_staged_state`, `builder_staged_diff` and `builder_test_result`
   (rank 3) currently follow `builder_task` (rank 4) and now precede it.

Two existing assertions constrain this and BOTH still hold — verify, do not
assume: `tests/cli/test_scope_plan.py` asserts the scope contract precedes the
goal and precedes the task body; `tests/cli/test_task_input.py` asserts the
system block precedes the task body.

### The golden — `tests/orchestration/test_builder_prompt_golden.py`

Follow `tests/orchestration/test_plan_prompt_golden.py` as the idiom, including
its module docstring's standing warning that the frozen constant is NEVER edited
to make a failing test pass. This site has no single template to freeze, so
freeze the RENDER instead: capture `_build_builder_prompt`'s output at
`54049e6b` for the fixtures below by running

    git show 54049e6b:packages/orchestration/pingpong_loop.py

into a disposable worktree (or `git stash`-free equivalent) and rendering there;
do not retype the prompt text by hand. State in the docstring which commit the
frozen renders come from and how they were obtained.

Fixtures: two `ReviewFinding`s, one with `required_fix` and one without; short
literal values for `context`, `goal`, `staged_state`, `safe_diff`, `task_body`,
`scope_contract`, `test_result`; `round_number=7`.

Assertions, at minimum:

1. **Content equality, four shapes.** For (a) minimal, (b) scope+task_body,
   (c) staged_state only, (d) everything: the composed segment TEXTS are a
   permutation of the frozen render's parts, and reassembling them in the
   pre-migration order equals the frozen render BYTE FOR BYTE.
2. **Rank order.** `tuple(entry.rank for entry in composed.manifest)` is
   non-decreasing in every shape, and the full shape's names are exactly the
   ten above in rank order.
3. **The inversions are really fixed.** In the full shape,
   `composed.text.index("APPROVED")`-style positional checks are NOT enough —
   assert on the manifest: `builder_scope_contract` precedes `builder_context`,
   and all three rank-3 job-context segments precede `builder_task`.
4. **The cacheable prefix, measured.** Compose twice with the SAME goal,
   task_body and scope_contract but a DIFFERENT `staged_state` and
   `round_number`. `builder_system` and `builder_scope_contract` keep identical
   hashes; `builder_staged_state` and `builder_task` do not. Report — as an
   assertion on a number, not a comment — how far the shared prefix reaches.
5. **`_build_builder_prompt` returns the composed text**, for every shape.

Note for the handback, not a defect to fix here: `builder_task` embeds
`## Task (Round N)`, so the round number makes the rank-4 task segment volatile
across rounds of the same job. Assertion 4 will show the shared prefix ending at
the scope contract because of it. Say so in the handback; do NOT change it in
this round — splitting the round number out is a CONTENT change and needs its
own decision.

## Done when (run every command; record REAL exit codes and real output)

A. `sha256sum .agent/authored/f105-r22-1.md .agent/last_block.md` equal;
   `cmp` on the pair exits 0.
B. `wc -l .agent/authored/f105-r22-1.md` — report the number.
C. Application, per target file:
   `grep -c '^- Reviewer gate on R21 ' .agent/live_review.md` -> 1
   `grep -c '^## DECISION F105 D9 ' .agent/decisions.md` -> 1
   `grep -c '^===BEGIN\|^===END' .agent/live_review.md .agent/decisions.md .agent/plan.md` -> 0 for all three
   `wc -l .agent/plan.md` -> must be < 50. Report the number.
D. Round gate:
   `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`
   `python3 -m pytest tests/orchestration/test_prompt_segments.py -q` (baseline 22)
   `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_cli.py tests/orchestration/test_repair_loop.py -q`
   `python3 -m pytest tests/cli/test_scope_plan.py tests/cli/test_task_input.py -q`
   Report each count. The pingpong/repair/scope/task_input counts must be
   UNCHANGED from before the round — record the before-numbers first, by running
   these same commands BEFORE C4.
E. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` (baseline 42).
F. Red-proof, in a DISPOSABLE `git worktree` at HEAD, never the primary checkout.
   Two mutations, each reverted, each reported with the test that went RED:
   M1 — change `builder_scope_contract`'s rank from DOSSIER to STEERING. A
   rank-order test must go RED. If only a text test catches it, say so: that
   means the golden pins bytes and not rank.
   M2 — in the boundary rule, drop the "else if the next segment starts with a
   newline" branch. A content-equality shape must go RED.
   Then `git worktree remove` and `git worktree prune`, and show
   `git worktree list` as the primary alone.
G. `git status --porcelain` empty after C5; `git log --numstat 54049e6b..HEAD` —
   report the `+` column per commit, each under 500.
H. State explicitly in the handback whether assertion 4's shared prefix ends at
   the scope contract, and give the number it measured.

## PAIR shapes, declared at authoring time

| Pair | Target | Shape |
|---|---|---|
| A | live_review | APPEND — TO contains FROM verbatim as its prefix |
| B | decisions | APPEND — TO contains FROM verbatim as its prefix |
| C | plan | full replacement, byte-for-byte equal to the slice |

APPEND proof: FROM exactly 1x after, each TO-ONLY line at least 1x. Every
state commit also reports its stray count — added lines tracing to no authored
TO slice — which must be 0.

===BEGIN PAIR_A_FROM===
  together as R-0250 rather than charged to this round. The handback declared
  every one of them, including two gates it could not satisfy, instead of
  reporting green — which is the behaviour the gate exists to reward.
  `LAST_REVIEWED_SHA` advances 04a3396d -> 9cb128d7.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  together as R-0250 rather than charged to this round. The handback declared
  every one of them, including two gates it could not satisfy, instead of
  reporting green — which is the behaviour the gate exists to reward.
  `LAST_REVIEWED_SHA` advances 04a3396d -> 9cb128d7.
- Reviewer gate on R21 (2026-08-09, next session): PASS. Range
  `9cb128d7..HEAD` at 54049e6b, SIX commits, SEVEN paths, exactly the block's
  declared change set plus the declared correction commit. Insertions per
  `git log --numstat`: 328, 242, 80, 62, 60, 9 — each under 500.
  All seven gates were re-run by the reviewer, not read from the handback.
  A: both files sha256 `a97328127a09dfaf…`, `cmp` silent. B: 328 lines, under
  the 400 cap. C: the four greps returned 1/1/1/1, line 8 ends
  `Next free ID: R-0251.`, the two doc greps returned 1/1, and the BEGIN/END
  marker count is 0 in all four target files. D: `tests/docs/` 294 passed,
  `test_dashboard_contract.py` 70 passed. E: canary 42 passed. F: no red-proof
  owed and none faked — the change set contains no executable file. G:
  `git status --porcelain` empty, `git worktree list` the primary alone.
  The pair shapes were re-measured rather than accepted: A and B REWRITE with
  FROM 0x and TO 1x, C, D and E APPEND with FROM 1x and TO 1x — five for five
  against the declared table. Stray added lines were recomputed from the
  authored TO slices against the real diffs of both content commits: 80 added
  and 0 stray at C2, 62 added and 0 stray at C3. PAIR_F's slice and
  `.agent/plan.md` are byte-identical at sha256 `d263bfd059ab0798…`.
  All three declared deviations ACCEPTED. Deviation 1 — `.agent/plan.md` at 50
  lines against AGENTS.md's <50 — is confirmed as the reviewer's defect and not
  the worker's: the PAIR_F slice is itself 50 lines, so an applier required to
  match it byte for byte could not have complied with both. It is the second
  live instance of the R-0250 class, and it is repaired by this round's plan
  rewrite rather than registered again. Deviation 3's fifth commit is the right
  call: the alternative to correcting a false `+50/-57` row was a force-push,
  which G2 forbids outright.
  R-0250's own resolution asked the next gate to verify the rule reached disk
  and reads as intended. It did: docs/agents/planner_reviewer_prompt.md §3 now
  carries the four-item pre-emission checklist, and this round's block was
  written against it — item 1 caught the size before emission and item 2 was run
  against every zero-gate in Done-when C.
  `LAST_REVIEWED_SHA` advances 9cb128d7 -> 54049e6b.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
Reverse this decision by deleting this entry and the §3 checklist it installs.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
Reverse this decision by deleting this entry and the §3 checklist it installs.

## DECISION F105 D9 — the schema tail stays outside the registry (2026-08-09)

Context: `.agent/plan.md` has carried, since R17, an open question that step 5
was not allowed to start without: does the schema tail appended by
`packages/orchestration/structured_outputs.py` — `build_schema_prompt` in
legacy mode, `native_schema_prompt` in native mode — become a registered rank-4
segment? Until it is answered, every T003 manifest describes fewer bytes than
the call actually sent, which sounds like an overclaim.

D9 — it does NOT become a registered segment during T003. Three reasons, in
order of weight.

1. It is appended by `run_structured_call`, shared infrastructure that every
   structured caller in the repository reaches, not by any of the six builders.
   Registering it there widens T003's change set from one builder per round to
   every structured call site, which AGENTS.md Scope Control bars.
2. It cannot affect the property T003 exists to create. The tail is a SUFFIX
   joined with exactly `PROMPT_SEGMENT_DELIMITER`, so the composed text is a
   strict PREFIX of the bytes sent and the cacheable prefix is byte-identical
   either way.
3. Its bytes are attempt-dependent — the parse-retry hint is part of them — so
   its honest rank is 5 STEERING, which sorts last. Registering it would move
   nothing.

What the decision COSTS is the honesty of the manifest, and that is paid in the
same round rather than deferred: the C3 pin turns reason 2 from a claim into a
test. A manifest that is a proven strict prefix is a true statement about the
call; an unproven one is the overclaim the plan was right to flag.

Rejected alternative: register the tail now at the structured-call layer. It is
the correct end state and it is where a follow-up should put it — but it is a
different feature's change set, and doing it inside a per-builder migration
round would mix a refactor of shared infrastructure with a feature step, which
AGENTS.md Commit Discipline forbids in one commit and Scope Control forbids in
one round.

Scope: T003 only. It adds no obligation to workers, changes no verification
tier, and leaves the tail exactly where it is today.

Reverse this decision by deleting this entry; the pin test in
`tests/orchestration/test_prompt_segments.py` stays useful either way.
===END PAIR_B_TO===

===BEGIN PAIR_C===
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
(R-0241). Migration-order steps 1-4 are COMPLETE and GATED, each with its own
golden. R21 is GATED and `LAST_REVIEWED_SHA` is 54049e6b. R22 records that
gate, settles the schema-tail question as DECISION F105 D9 with a test that
proves the strict-prefix claim, and takes migration-order step 5,
`pingpong_loop.py::_build_builder_prompt`. Open findings: R-0221, R-0239,
R-0246, R-0247. No PR; one is created at CLOSURE.

## Next Steps
- R23 gates R22, then takes step 6, `_build_reviewer_prompt` — last of the six
  and the highest content-equality risk: two mutually exclusive branches and
  three reviewer-role strings that all reach evidence.
- ONE later round wires `on_call` for the three sites lacking call evidence:
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
- Step 5 crosses two rank boundaries, so its golden is equal-modulo-ordering,
  never byte-exact. The reviewer proved the decomposition byte-exact in
  pre-migration order over all 64 option combinations before authoring the
  block, so a mismatch there is a real regression and not a bad spec.
===END PAIR_C===
