# Handoff — F106 Session resume instead of rebuild

## Session

SESSION 6 of feature F106 · round 20 · second round of this session

## Range

Branch `feature/f106-session-resume`, base `6a64c1c4` (round 19's own C4
handoff, closure precondition 4 MET) through `HEAD` at commit time (round
20, 3 content commits: C0a/C0b, C1, C2; this handoff is C3/the 4th commit
of the round).

## Round 20 summary — closure precondition 6 advanced (NOT yet MET): SU-003 RUN for real, blocked on a provider-dispatch gap

Round 20 planned and RAN the self-use queue's next pending item, **SU-003**
("Give apps/ui's ESLint config a TypeScript parser"), through the real job
path (`self_use_job.plan_next_self_use_item` then
`self_use_runner.run_next_self_use_item`) to the normal approval gate,
inside an isolated worktree with an isolated `REMEDY_DATA_DIR`
(`.remedy-wt/f106-r20-selfuse/data`, gitignored scratch). The run was
never promoted and `scripts/self_use_queue.json` was READ only, never
written — confirmed byte-identical before/after.

**The run resolved the real product default provider (`ollama`, via
`role_config.resolve_role_config`, confirming DECISION-driving fix
`cfd72734`/R-0757 behaves as designed on this branch) but then BLOCKED
before any provider call was made.** Root cause, independently
reproduced by this worker outside the job entirely:
`packages/orchestration/pingpong_provider.py:1591-1599`'s
`create_provider(name, *, model="")` recognises only three provider
names — `"fake"`, `"claude"`, `"claude-cli"` — and raises
`RuntimeError: Unknown provider: 'ollama'. Available: fake, claude,
claude-cli"` for anything else. `_create_provider_with_cwd` in
`pingpong_loop.py` routes any non-`"claude-cli"` name straight into
`create_provider()`, so a genuinely-resolved
`role_config.DEFAULT_PROVIDER = "ollama"` can never reach a real
provider through this path — regardless of ollama actually being
reachable (confirmed at `http://localhost:11434`, `muse-glimmer:latest`
pulled, and recorded as such in the job's own persisted
`run_manifest.input_snapshot`). T001 ended `final_status=
provider_unavailable` with zero rounds recorded ("no_rounds": the
provider object is never even constructed). Per this round's own step
block, **finding registration for this is explicitly DEFERRED to round
21** — no R-id is minted this round; the raw evidence is recorded
honestly in `.agent/gate_f106_r20/self_use_run.txt` instead.

- `scripts/self_use_queue.json` sha256 before = after =
  `a72e6be87432e0fa90aa334d41010f3512ef3fca790ba903d28d3582ea1abfa2`
  (matches the block's own expected value; confirmed BEFORE running, per
  constraint 3a, and again after).
- The persisted `JobPlan` (`job_id f76686b8435640e9`,
  `.remedy-wt/f106-r20-selfuse/data/task_jobs/f76686b8435640e9/job.json`)
  was independently RELOADED in a fresh `python3` process via
  `pingpong_job.load_job_plan` under the same `REMEDY_DATA_DIR` — every
  field (`job_id`, `status`, `error`, `isolation_mode`,
  `execution_config`, `budgets`, both tasks' `status`/`final_status`/
  `error`/`test_passed`/`reviewer_verdict`) reproduced byte-identical to
  the in-memory run result, confirmed by a programmatic field-by-field
  comparison (`ALL MATCH: True`), not merely restated.
- `describe_self_use_run_defects()` on the reloaded `JobPlan` was
  independently recomputed and is **NON-EMPTY, 2 entries** — full text
  below, quoted verbatim from the evidence file.
- No path under `packages/`, `apps/`, `tests/`, `docs/`, `scripts/`
  changed this round. `scripts/self_use_queue.json`'s `consumed_by` edit
  remains a closure-commit act (DECISION F257 D2), not this round's.

## Changed files (C0a-C2, this round)

| Path | Change | Commit |
|---|---|---|
| `.agent/authored/f106-r20.md` | new (verbatim block save) | `9d11c316` |
| `.agent/last_block.md` | rewrite (mirror of block) | `9d11c316` |
| `.agent/plan.md` | rewrite (PLAN20) | `4b49af98` |
| `.agent/gate_f106_r20/self_use_run.txt` | new (real self-use run evidence) | `6e1f4fe0` |
| `.agent/handoff.md` | rewrite (this file) | (C3, this commit) |

No path under `packages/`, `apps/`, `tests/`, `docs/`, `scripts/` changed
this round.

## The full `describe_self_use_run_defects` answer (quoted verbatim)

```
(
  "job f76686b8435640e9 (blocked): task_T001_gate_failed: final_status=provider_unavailable; no_rounds",
  "T001 (blocked): completion_gate_failed: final_status=provider_unavailable; no_rounds",
)
```

Two entries: the job's own `error` field, then T001's own `error` field
(T002 never ran — `status='skipped'`, blank `error`, contributes nothing
per the function's own documented behaviour of one string per task with a
non-blank `error`, in task order).

## Full `execution_config` and per-task outcome (real values, both from the in-memory run AND the independent reload — identical)

```
execution_config: builder='ollama' (source='cli'), reviewer='ollama' (source='cli'),
                   builder_model='' (source='default'), reviewer_model='' (source='default')
num_tasks = 2
  task T001: status='blocked' final_status='provider_unavailable'
             error='completion_gate_failed: final_status=provider_unavailable; no_rounds'
             test_passed=None reviewer_verdict=''
  task T002: status='skipped' final_status='' error='' test_passed=None reviewer_verdict=''
```

`isolation_mode = worktree`. `budgets = {'max_total_tokens': None,
'max_provider_calls': 6, 'max_wall_clock_minutes': None, 'max_cost_usd':
0.5, 'deadline': None}`. `budget_actuals = None` (zero provider calls were
ever made — the block before any call). `job.status = blocked`, `job.error
= task_T001_gate_failed: final_status=provider_unavailable; no_rounds`.

## Verification — this round's own gate results (real numbers, self-run)

- **G1 TRANSPORT**: `.agent/authored/f106-r20.md` and `.agent/last_block.md`
  both sha256
  `5527a7a5e5bfc23d8f1e449af5c0ccfecc1dd62120bd97e5783d815af3f63918`,
  equal to `.remedy-wt/f106-r20-block.md` as saved (three-way sha256sum
  comparison, single digest, all three equal).
- **G2 THE PLAN**: `.agent/plan.md` sha256
  `b33239536b736b4b89d164fe2159ec2bf824ae35bf5b2f2c1b4848c5fb761a1e`, **41
  lines** (`wc -l`), **2122 bytes** (`wc -c`), holds `## Goal` (line 6) and
  `## Next Steps` (line 27) — matches the block's stated digest/line
  count/byte count exactly.
- **G3 THE SELF-USE RUN**: `.agent/gate_f106_r20/self_use_run.txt` exists;
  its `job_id` (`f76686b8435640e9`), `status` (`blocked`), `error`
  (`task_T001_gate_failed: final_status=provider_unavailable; no_rounds`),
  `isolation_mode` (`worktree`), `execution_config` and both tasks'
  fields all REPRODUCED exactly from an independent reload of the
  persisted `JobPlan` in a fresh `python3` process (programmatic
  comparison, `ALL MATCH: True`) — not merely restated from the in-memory
  run. Queue sha256 before = after =
  `a72e6be87432e0fa90aa334d41010f3512ef3fca790ba903d28d3582ea1abfa2`, all
  three values equal.
- **G4 THE DEFECTS TUPLE**: `describe_self_use_run_defects()` on the
  independently reloaded `JobPlan`, recomputed directly by this worker (not
  trusted from the evidence file's own text), answers the exact 2-entry
  tuple quoted above — matching the evidence file's recorded text exactly.
- **G5 THE QUEUE UNTOUCHED**: `git status --porcelain -- scripts/` → empty
  (real, re-run at handoff time). `git diff --stat 6a64c1c4..HEAD --
  scripts/` → empty (real, re-run at handoff time; `6a64c1c4` is round 19's
  own HEAD / this round's base).
- **G6 THE TREE**: `git status --porcelain` → empty (after this handoff
  commit). Per-commit insertions (`git diff --numstat <c>^..<c>`): C0a/C0b
  120+103=223 (exempt: verbatim `.agent/**` state-file saves), C1 24, C2
  69 — all well under 500 regardless of exemption. Canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`: real exit **0**,
  **42 passed** in 20.47s. HEAD to be pushed and confirmed equal to
  `origin/feature/f106-session-resume` immediately after this commit.

## Deviations & assumptions

- None from the block's own procedure. One genuine, unexpected RUN OUTCOME
  (not a deviation from instructions): the resolved provider was the real
  `ollama` product default exactly as the block anticipated as the likely
  path, but the run still blocked pre-provider-call on the
  `create_provider()` name-dispatch gap described above — this is evidence
  the block explicitly asked to be recorded honestly rather than treated
  as a failure of this round, and it was recorded, not smoothed over or
  retried under `builder_name="fake"` (the block explicitly forbids that
  substitution).
- `execution_config.builder_source` / `reviewer_source` read `'cli'`
  rather than `'default'`, even though nothing on the CLI supplied an
  override this round: `self_use_runner.run_next_self_use_item` resolves
  the role config itself and then forwards the resolved provider name as
  an explicit `builder_name=`/`reviewer_name=` keyword into `run_job()`,
  and `run_job()`'s own bookkeeping cannot distinguish "explicitly passed
  by a human via a CLI flag" from "explicitly passed by
  `self_use_runner`'s own composition" — both look like an explicit
  keyword to `run_job()`, so both get labelled `'cli'`. Noted here as a
  labelling quirk observed while reading the evidence, not registered as
  a finding this round (finding registration is deferred to round 21 for
  everything this run surfaced).

## Next

1. **Closure precondition 6 is NOT YET MET.** Round 21 must read this
   round's real evidence (`.agent/gate_f106_r20/self_use_run.txt`, and the
   full `describe_self_use_run_defects` answer quoted above) and either:
   (a) register a finding for the `create_provider()` "ollama" name-gap
   this round surfaced (root cause independently reproduced above:
   `packages/orchestration/pingpong_provider.py:1591-1599`'s
   `create_provider()` has no `"ollama"` branch, so
   `role_config.DEFAULT_PROVIDER = "ollama"` can never reach a real
   provider through the self-use/job-run path), searching the open ledger
   first per checklist item 30 before minting a new R-id; or (b) state
   explicitly that, on reflection, nothing here warrants a new finding
   (unlikely given the evidence, but the round's own call to make). Only
   after that step is precondition 6 fully MET.
2. `scripts/self_use_queue.json`'s `consumed_by` edit for SU-003 itself
   still waits for the closure commit, per DECISION F257 D2 — SU-003 was
   RUN this round, not marked consumed, exactly as instructed.
3. After precondition 6 closes: evidence job, review zip, STATUS line,
   PR — the closure algorithm's remaining steps. The closure commit also
   still owes DECISION F106 D2's `.agent/candidates.md` entry (job/mission
   resume deferral, text given in full inside DECISION F106 D2 in
   `.agent/live_review.md`).
4. Open-findings ledger: **321 registered / 60 resolved / 21 decisions**
   (UNCHANGED this round — this round mints no R-id, per its own explicit
   instruction to defer registration to round 21).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | SU-003 run for real; blocked pre-provider-call on `create_provider()`'s missing `"ollama"` branch; evidence committed; finding registration deferred to round 21 per block instruction |
| C3 | done | this handoff |
