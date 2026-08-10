── STEP R32 (session close) — F105 ────────────────────────────
Goal:        Record the R31 reviewer gate on disk, resolve the two findings
             whose fixes have landed and been verified, and end the session
             with a handoff that names exactly where the next one starts.
Bundle:      C1 save this block · C2 the R31 gate record and the two
             resolutions · C3 plan and the session-ending handoff.
Change:      `.agent/authored/f105-r32-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. No production code, no tests, no docs this round.
Constraints: State-file-only round. Do not touch `packages/`, `apps/`, `tests/`
             or `docs/`. Do not reflow any line you were not given a pair for.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r32-1.block.md`
      `.agent/authored/f105-r32-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — the R31 gate record and the two resolutions (own commit)
  Three pairs against `.agent/live_review.md`, all in this one commit.
  PAIR_A is APPEND-shaped — prove FROM exactly 1x plus the TO-only ADDED-LINE
  count over this commit's diff. PAIR_B and PAIR_C are also APPEND-shaped (each
  TO opens with its FROM verbatim). Do NOT use a whole-file count for any of
  them; scope every count to this commit's ADDED lines (§4.9). Report the total
  stray count across all three.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.
- R31: SPLIT round — fix R-0257, name the mission-plan evidence sink in
  `plan_mission`, label the provider from `remedy mission plan`, and pin all of
  it with `TestMissionPlanEvidenceSink`.
- Reviewer gate on R31 (2026-08-10): PASS. Range `0ba30611..9bd3a3e7` = seven
  commits, read as a real diff: eight paths, exactly the ones the block named;
  insertions per commit 384, 257, 53, 13, 17, 67, 58 — each under 500.
  Transport disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r31-1.block.md`, `.agent/authored/f105-r31-1.md` and
  `.agent/last_block.md` all three
  `8833261bcf731bec965fbcd52ff7aa8339141a5ae076397cfeee41232f307003`, both
  `cmp` runs silent, 384 lines against DECISION F105 D5's cap of 400.
  All eight pairs re-sliced from the COMMITTED authored file by the reviewer's
  own whole-line marker reader; declared shape equals measured shape for every
  one. PAIR_A FROM 1x with 52 TO-only lines; C2 ADDS 53 and REMOVES 1, the
  extra add and the single removal both PAIR_B's, so strays 0 in both
  directions. PAIR_C, D, E and F all FROM 0x after and TO 1x, with C3's 12
  added / 7 removed and C4's 12 added / 2 removed on the compiler and 5 added
  on the CLI all accounted for by their TOs. PAIR_G FROM 1x with 66 TO-only
  against 67 ADDED. PAIR_H byte-equal to `.agent/plan.md` at 42 lines against
  the cap of 50. Exactly two additions sit outside a TO in the whole round and
  the block named both in advance: the `Landed: R-0257` line and the
  `from packages.orchestration import mission_compiler` test import.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'` = 0
  in all five targets; `test_mission_compiler.py` + `test_mission_prompt_golden.py`
  `126 passed in 0.65s`; the three caller suites `78 passed in 1.23s`;
  `tests/cli/` `1329 passed in 261.30s`; `tests/docs/` `294 passed in 0.30s`;
  the dashboard contract `70 passed in 4.31s`; the canary `42 passed in 19.46s`;
  `git status --porcelain` empty and `git worktree list` the primary alone.
  BOTH red-proofs reproduced by the reviewer in a disposable worktree at
  db3bdef3 with `PYTHONDONTWRITEBYTECODE=1`. M1: `append_trace_jsonl` swapped
  for `write_trace_jsonl` in `plan_mission`'s import AND call turns exactly one
  test RED, `test_a_recompile_appends_rather_than_truncating`, at
  `1 failed, 120 passed in 0.60s`. M2: after reverting M1 — `git diff --stat`
  empty, so the revert is proved — deleting `traces=prompt_traces,` turns
  exactly two RED, `test_planning_writes_the_trace_into_the_evidence_dir` and
  the recompile test, at `2 failed, 119 passed in 0.74s`. Worktree removed and
  pruned. The handback's 71-line handoff carries its DECISION D15 stated-cause
  line and drops no mandated section, which is the rule, not an exception.
  `LAST_REVIEWED_SHA` advances 0ba30611 -> 9bd3a3e7.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  `None` cap reproduces the pre-R-0197 milestone ceiling, while the composed
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  `None` cap reproduces the pre-R-0197 milestone ceiling, while the composed
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
  Done: R-0246 (2026-08-10) — RESOLVED at F105 R30, commit 39da9b61. The
  docstring now says "reproduces the pre-R-0197 milestone CEILING — not the
  pre-migration byte SEQUENCE", and states that the composed order differs at
  every value of `max_milestones`, `None` included. Verified by the reviewer
  against the real diff, not the handback: the sentence a reader searching for
  "did the migration change the prompt?" lands on can no longer be read as a
  claim about byte order.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  Landed: R-0257 — composition moved back inside the try at C3 of R31.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  Landed: R-0257 — composition moved back inside the try at C3 of R31.
  Done: R-0257 (2026-08-10) — RESOLVED at F105 R31, commit 3d37567f.
  `compose_mission_prompt` and the recorder wiring both sit inside the `try`
  again, so a composition failure returns to being `_fallback(goal,
  hint=f"provider error: {exc}")`. Re-proved by the reviewer at 9bd3a3e7 with
  the composer monkeypatched to raise: `source="deterministic"`,
  `error_hint="provider error: composition blew up"` — the pre-R30 behaviour
  exactly. `test_a_failing_composer_still_yields_the_fallback` now pins it, so
  the regression cannot return silently the way it arrived.
<<<END_PAIR_C_TO>>>

C3 — plan and the session-ending handoff (own commit)
  Apply PAIR_D to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` as the SESSION-ENDING handoff. It must state, in its own
  words and with real numbers: the feature and round (F105 R32, session close);
  the branch; this round's commit SHAs; a changed-files table with one row per
  path; the item-status table over C1a/C1b/C2/C3; the gate table with REAL exit
  codes and REAL output; the open-findings count and their IDs; and the next
  expected action for the next session, which is: gate R32 over
  `9bd3a3e7..HEAD`, then the round that wires `on_call` for the orchestrator
  prompt at `mission_cmd.py:362` into `run_mission`.
  It must also say plainly that R32 itself carries NO on-disk gate entry by
  construction — it is the round that writes the record, so it cannot record a
  verdict on itself (docs/agents/planner_reviewer_prompt.md §4.13). That
  absence is the terminator; the next session gates it and no repair round is
  opened for it. Keep the handoff under 60 lines, or carry a DECISION D15
  "Deviations, declared" line naming the real count and the mandated content
  that caused it.

<<<PAIR_D_PLAN>>>
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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
Call evidence now reaches three prompts: both `do_cmd` flight-plan sites — the
first through `write_trace_jsonl`, the replan through `append_trace_jsonl` — and
`remedy mission plan`, composed ONCE inside `compile_mission_plan` and appended
to the mission's evidence dir.
R31 is GATED; `LAST_REVIEWED_SHA` is 9bd3a3e7. R32 is the session-close round:
it records the R31 gate, resolves R-0246 and R-0257, and writes the handoff. By
construction it carries no gate entry on itself (§4.13) — the next session gates
it over `9bd3a3e7..HEAD`.
Open findings: R-0221, R-0239, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- The orchestrator prompt — `mission_cmd.py:362` into `run_mission`, then
  `gauntlet_runner.py:505`. Neither has an evidence sink today; R30 and R31 are
  the shape to copy, in that order: manifest first, sink second.
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_D_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r32-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r32-1.md`. Cap 400 (DECISION F105 D5).
  C application: PAIR_A, PAIR_B and PAIR_C are all APPEND — FROM exactly 1x
    each, plus the TO-only ADDED-LINE count from `git show --numstat` and the
    stray count over this commit's ADDED lines. PAIR_D: `cmp` the applied
    `.agent/plan.md` against the sliced text; `wc -l` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in `.agent/live_review.md`
    and `.agent/plan.md` — 0 each.
  E state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  F canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  G no-code proof: `git diff --stat 9bd3a3e7..HEAD` must show paths under
    `.agent/` ONLY. NO mutation red-proof is ordered or run this round: nothing
    executable changes, so there is no branch to mutate (DECISION F105 D10,
    D8 checklist item 5).
  H hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 9bd3a3e7..HEAD` with the `+` column per commit,
    each under 500.
Handback:    completion report + the session-ending `.agent/handoff.md`
             described in C3. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
