── STEP R29 (session close) — F105 ────────────────────────────
Goal:        Record the R28 reviewer gate on disk and end the session with a
             handoff that names exactly where the next session starts.
Bundle:      C1 save this block · C2 the R28 gate record · C3 plan and the
             session-ending handoff.
Change:      `.agent/authored/f105-r29-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. No production code, no tests, no docs this round.
Constraints: State-file-only round. Do not touch `packages/`, `apps/`, `tests/`
             or `docs/`. Do not reflow any line you were not given a pair for.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r29-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` both plus `cmp`; digest in the handback.

C2 — the R28 gate record (own commit)
  Apply PAIR_A to `.agent/live_review.md`. It is APPEND-shaped (the TO contains
  the FROM verbatim as its prefix): prove FROM exactly 1x, plus the TO-only
  ADDED-LINE count from this commit's diff and the stray count. Do NOT use a
  whole-file count.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances d0ebba63 -> 73259d7a.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances d0ebba63 -> 73259d7a.
- R28: SPLIT round — record the R27 gate, resolve R-0255, register R-0256, add
  `append_trace_jsonl` beside the per-job trace writer and wire the replan site
  with it so a replan records its flight-plan manifest without truncating the
  traces the job's first run wrote.
- Reviewer gate on R28 (2026-08-10): PASS. Range `73259d7a..55550615`, seven
  commits, read as a real diff: only the eight paths the block named.
  `write_trace_jsonl` is untouched, as the block required — the new function is
  a sibling, not a parameter on the old one. Insertions per commit 368, 263, 57,
  51, 25, 63, 1 — each under 500, and the authored block is 368 lines against
  DECISION F105 D5's cap of 400, counted this time rather than estimated.
  Transport under the §4.9 digest fallback: `.agent/authored/f105-r28-1.md` and
  `.agent/last_block.md` both recompute to
  `c323410875ab8da7313a988a79d6f74e0976ba3320721b0d8f0ad35808df7fe2`, `cmp`
  silent, 368 lines each — the digest the handback declared.
  All seven pairs re-sliced from the COMMITTED authored file by the reviewer's
  own marker-LINE reader and measured disk to disk: declared shape equals
  measured shape for every one, appends at FROM 1x, rewrites at FROM 0x after
  and TO 1x, and PAIR_H byte-equal to `.agent/plan.md` at 41 lines against the
  cap of 50. Diff-scoped accounting per §4.9: `.agent/live_review.md` ADDED 57,
  `packages/orchestration/prompt_trace.py` ADDED 13,
  `tests/orchestration/test_prompt_trace.py` ADDED 38,
  `apps/cli/commands/do_cmd.py` ADDED 25 — strays 0 in all four. No ADDED line
  came from outside a TO slice.
  Gates re-run by THIS reviewer with real exit codes: `tests/orchestration/`
  `10502 passed, 7 skipped in 703.66s` — three more than R27's 10499, the three
  tests this round adds; `tests/cli/` `1329 passed in 261.91s`;
  `test_prompt_trace.py` `41 passed`; `tests/docs/` `294 passed`; the dashboard
  contract `70 passed`; the canary `42 passed`.
  BOTH red-proofs reproduced by the reviewer in a disposable worktree at
  55550615, with `PYTHONDONTWRITEBYTECODE=1` because the worker's own first
  attempt showed CPython's `(mtime, size)` `.pyc` validation accepting a stale
  cache when a same-length revert lands in the same clock second — a real
  diagnosis, honestly declared, and worth remembering for every future
  same-length mutation. M1: `append_trace_jsonl`'s `path.open("a")` changed to
  `path.open("w")` turns exactly one test RED,
  `test_appending_traces_keeps_the_earlier_ones`, at `1 failed, 40 passed`. M2:
  after reverting M1, deleting the `on_call=` argument from the REPLAN call only
  turns exactly one test RED, `test_the_replan_path_records_and_appends_its_traces`,
  at `1 failed, 40 passed`, with `git diff --stat` showing
  `apps/cli/commands/do_cmd.py` alone — so M1 was genuinely reverted and the two
  mutants are independent. Worktree removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Noted, not held against the round: the replan guard asserts
  `source.count("on_call=make_flight_plan_call_recorder(") == 2`, so it pins BOTH
  wiring sites and any future round that intentionally rewires either must update
  that count. The worker flagged this itself rather than letting the next round
  discover it.
  `LAST_REVIEWED_SHA` advances 73259d7a -> 55550615.
<<<END_PAIR_A_TO>>>

C3 — plan and the session-ending handoff (own commit)
  Apply PAIR_B to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` as the SESSION-ENDING handoff.
  The handoff must state, in its own words and with real numbers:
  the feature and round (F105 R29, session close); the branch; the commit SHAs
  of this round; a changed-files table with one row per path; the item-status
  table over C1a/C1b/C2/C3; the gate table with REAL exit codes and REAL output;
  the open-findings count and their IDs; and the next expected action for the
  next session, which is: gate R29 over `55550615..HEAD`, then the round that
  wires `on_call` for the mission and orchestrator prompts.
  It must also say plainly that R29 itself carries NO on-disk gate entry by
  construction — it is the round that writes the record, so it cannot record a
  verdict on itself (docs/agents/planner_reviewer_prompt.md §4.13). That absence
  is the terminator; the next session gates it and no repair round is opened for
  it. Keep the handoff under 60 lines, or carry a DECISION D15 "Deviations,
  declared" line naming the real count and the mandated content that caused it.

<<<PAIR_B_PLAN>>>
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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated,
each under its own golden, and both `do_cmd` flight-plan call sites now reach
call evidence — the first through `write_trace_jsonl`, the replan through
`append_trace_jsonl`, which exists because the trace file is per JOB and a
second command would otherwise truncate the first.
R28 is GATED; `LAST_REVIEWED_SHA` is 55550615. R29 is the session-close round:
it records the R28 gate and writes the handoff, and by construction carries no
gate entry on itself (§4.13) — the next session gates it.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- `on_call` for the mission and orchestrator prompts — `mission_cmd.py:187`,
  `mission_cmd.py:362`, `gauntlet_runner.py:505`. None has an evidence sink
  today, so each needs its sink named before it is wired.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
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
<<<END_PAIR_B_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on `.agent/authored/f105-r29-1.md` and
    `.agent/last_block.md`; `cmp` them. Digest in the handback.
  B size: `wc -l .agent/authored/f105-r29-1.md`.
  C application: PAIR_A in `.agent/live_review.md` — APPEND, prove FROM exactly
    1x plus the TO-only ADDED-LINE count from `git show --numstat` and the stray
    count. PAIR_B: `cmp` the applied `.agent/plan.md` against the sliced PAIR_B;
    `wc -l .agent/plan.md` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in `.agent/live_review.md`
    and `.agent/plan.md` — each count must be 0. The count is over marker LINES
    on purpose (DECISION F105 D8 item 2).
  E state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  F canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  G no-code proof: `git diff --stat 55550615..HEAD` must show paths under
    `.agent/` ONLY — no `packages/`, no `apps/`, no `tests/`, no `docs/`. NO
    mutation red-proof is ordered or run this round: nothing executable changes,
    so there is no branch to mutate (DECISION F105 D10, D8 checklist item 5).
  H hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 55550615..HEAD` with the `+` column per commit.
Handback:    completion report + the session-ending `.agent/handoff.md` described
             in C3. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
