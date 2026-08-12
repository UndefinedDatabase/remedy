── STEP R33 — F105 ───────────────────────────────────────────
Goal:        Give the ORCHESTRATOR prompt the call evidence the other three
             migrated sites already have: a per-iteration recorder that carries
             the segment manifest, and a sink that appends every provider call
             to the mission's `prompt_trace.jsonl` from INSIDE `run_mission`.
Bundle:      C1 save this block · C2 the R32 gate record and DECISION D11 ·
             C3 the recorder and compose-once · C4 the sink and the CLI provider
             label · C5 the tests · C6 plan and handback.
Change:      `.agent/authored/f105-r33-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`, `packages/orchestration/orchestrator_loop.py`,
             `apps/cli/commands/mission_cmd.py`,
             `tests/orchestration/test_orchestrator_loop.py`. Nothing else.
Constraints: Prompt BYTES do not change — `test_orchestrator_prompt_golden.py`
             asserts `==` against the frozen render and must stay green.
             Do NOT remove or re-sign `build_orchestrator_prompt`; two test
             modules import it. Do NOT touch `gauntlet_runner.py` this round.
             Do NOT introduce a shared constant for `"prompt_trace.jsonl"`:
             ten sites already spell it inline and a repo-wide rename is
             forbidden churn (AGENTS.md Code Discoverability, FORWARD-LOOKING).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r33-1.block.md`
      `.agent/authored/f105-r33-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — the R32 gate record and DECISION D11 (own commit, two files)
  PAIR_A appends to `.agent/live_review.md`; PAIR_B appends to
  `.agent/decisions.md`. Both are APPEND-shaped: each TO opens with its FROM
  verbatim. For each, prove FROM exactly 1x in its target and count the
  TO-only ADDED lines over THIS commit's diff FOR THAT PATH
  (`git show --numstat a-commit -- path`), never a whole-file count (§4.9).
  Report the stray count per path, both directions.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 0ba30611 -> 9bd3a3e7.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 0ba30611 -> 9bd3a3e7.
- R32: session-close round — record the R31 gate, resolve R-0246 and R-0257,
  write the session-ending handoff. State files only.
- Reviewer gate on R32 (2026-08-10): PASS. Range `9bd3a3e7..cab89962` = four
  commits, read as a real diff: five paths, every one under `.agent/`, exactly
  the ones the block named; insertions per commit 196, 129, 54, 47 — each under
  500. Transport disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r32-1.block.md`, `.agent/authored/f105-r32-1.md` and
  `.agent/last_block.md` all three
  `56173ae6acaf147af639b03200b9398df3158598b086dc686df68e34131cb78f`, all three
  `cmp` runs silent, 196 lines against DECISION F105 D5's cap of 400.
  All three C2 pairs re-sliced from the COMMITTED authored file by the
  reviewer's own whole-line marker reader: declared shape equals measured shape
  for every one — each TO opens with its FROM verbatim, so all three are APPEND
  as declared. FROM exactly 1x in the target both before and after the write,
  TO exactly 1x after. TO-only lines 39 + 7 + 8 = 54; the commit ADDS 54 and
  REMOVES 0 over `.agent/live_review.md`, so strays are 0 in both directions
  and no added line sits outside a TO. PAIR_D byte-equal to the applied
  `.agent/plan.md` at 43 lines against the cap of 50; the handoff is 59 lines
  against the cap of 60.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'`
  prints `0` in `.agent/live_review.md` and `0` in `.agent/plan.md` (rc 1, the
  honest no-match); `tests/docs/` `294 passed in 0.30s`; the dashboard contract
  `70 passed in 4.11s`; the canary `42 passed in 19.44s`; `git status
  --porcelain` empty and `git worktree list` the primary alone. Gate H is
  re-measured here AFTER the C3 commit the handback could not measure itself,
  and it is clean — the declared D15 deviation was a timing statement, not a
  gap. No mutation red-proof: nothing executable changed, so there is no branch
  to mutate (DECISION F105 D10).
  The record's own claims were spot-checked against git rather than read: the
  R31 gate line's "seven commits, eight paths" and its per-commit insertions
  384, 257, 53, 13, 17, 67, 58 are exact, and both resolution commits it names
  exist and touch the file it says they do — 39da9b61 for R-0246, 3d37567f for
  R-0257.
  The open-findings count of 4 was re-derived, not accepted: R-0221, R-0239,
  R-0247 and R-0256 carry no resolution. Four further entries also carry no
  `Done: R-XXXX` line of their own and are nevertheless closed — R-0240 and
  R-0241 share one `Done:` paragraph filed under R-0241, and R-0250 and R-0252
  were resolved inline as DECISIONs D8 and D10. Both of those deferred their
  proof to "the NEXT session's gate", which is this one: §3 of
  docs/agents/planner_reviewer_prompt.md carries the checklist as items 1-6,
  including item 5's reachability rule (D10) and item 6's target-content rule,
  and it reads as intended. Both are therefore closed on evidence, not on
  assertion. A mechanical `Done:`-grep undercounts resolutions by four; that is
  a property of this file's format, not a defect of R32, and it is recorded
  here so no later reader re-derives it as a finding.
  `LAST_REVIEWED_SHA` advances 9bd3a3e7 -> cab89962.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
Reverse this decision by deleting this entry and §3 checklist item 5.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
Reverse this decision by deleting this entry and §3 checklist item 5.

D11 — the orchestrator prompt's evidence sink lives INSIDE `run_mission`, not
in `remedy mission run`. The mission-plan site put its sink in `plan_mission`,
a package function, and `.agent/plan.md` carried the orchestrator site as two
rounds: `mission_cmd.py` first, `gauntlet_runner.py` second. Reading the
callers dissolved the second round. `run_mission` has TWO production callers —
`apps/cli/commands/mission_cmd.py:366` and `packages/orchestration/
gauntlet_runner.py:514` through `deps.run_mission` — and it already owns the
mission's evidence directory, because `append_ledger_entry` writes the ledger
into it every iteration. A sink in the CLI would have left every gauntlet run
with no orchestrator prompt evidence at all, and the gate would have been green
the whole time: the F104 R-0220 class, where the caller is the thing nobody
checked.

Placing it in `run_mission` also settles WHEN the write happens. The loop has
several return paths and a boundary that turns a raise into a terminal, so a
single flush after the loop would lose the calls a crashed or stopped run had
already made. The append therefore happens per iteration, immediately after the
provider call, exactly as the ledger entry does a few lines away — one
durability rule for both records of the same iteration.

The alternative — flush once from each caller, copying `plan_mission` literally
— was rejected on both counts: it duplicates the sink per caller and it trades
the ledger's durability for a shape that only looks consistent.

Consequence, stated so it is not mistaken for an omission: the gauntlet's
orchestrator rows land in evidence from this round on, but carry an EMPTY
provider label until `gauntlet_runner.py:514` names it. Unlabeled is honest;
mislabeled would not be. That is a one-line round, no longer a wiring round.

Reverse this decision by deleting this entry, dropping the append from
`run_mission`, and flushing a caller-owned `traces` list in each of the two
callers instead.
<<<END_PAIR_B_TO>>>

C3 — the recorder and compose-once (own commit, orchestrator_loop.py)
  1. Add `make_orchestrator_call_recorder(traces, composed, *, provider="",
     provider_kind="")` beside `compose_orchestrator_prompt`, returning the
     `Callable[[int, str, bool, str], None]` that `run_structured_call`'s
     `on_call` seam expects. Copy `make_mission_plan_call_recorder`
     (`mission_compiler.py:258`) exactly: one `build_trace_entry` per call,
     `composed_prompt=composed` so the manifest travels, `role="orchestrator"`,
     `prompt_kind`/`phase` = `"orchestrator-retry"` when `is_parse_retry` else
     `"orchestrator"`, `transport_attempt=attempt`,
     `is_transport_retry=False`. `build_trace_entry` comes from
     `packages.orchestration.prompt_trace`; `ComposedPrompt` is ALREADY
     imported at module level (line 52) — do not re-import it.
     The one-line WHY above the definition says why the recorder lives in this
     module: the manifest and the prompt it describes cannot drift apart.
  2. At the provider call inside the loop (currently
     `build_orchestrator_prompt(context, repo_root)` at line 1074) compose
     ONCE per iteration instead: `composed = compose_orchestrator_prompt(
     context, repo_root)` and pass `composed.text`. The JOB_CONTEXT segment
     changes every iteration, so the recorder is rebuilt every iteration from
     THAT iteration's `composed` — a recorder hoisted out of the loop would
     label iteration N's bytes with iteration 1's manifest.
  3. `run_mission` gains `provider: str = ""` and `provider_kind: str = ""`
     keyword-only parameters, documented in the existing Seams docstring.
  4. The caller's `on_call` is NOT dropped. Chain: the recorder fires first,
     then the caller's `on_call` if it is not None. A silently ignored
     documented parameter is a defect even when no caller passes it today.

C4 — the sink and the CLI provider label (own commit, two files)
  1. In `run_mission`, per iteration: collect that iteration's entries in a
     fresh list and `append_trace_jsonl` them to
     `mission_evidence_dir(pid, mission_id, root) / "prompt_trace.jsonl"`
     as soon as the provider call has returned OR raised — the boundary
     `except Exception` must not swallow the evidence of a call that was
     really made. `mission_evidence_dir` is already imported at line 47;
     `append_trace_jsonl` comes from `packages.orchestration.prompt_trace`.
     APPEND, never write: the mission-plan traces are already in that file
     (`mission_compiler.py:765`) and every run is another command against the
     same mission. A write would destroy both.
  2. Nothing is written when no call was made. The `call_fn is None` terminal
     must leave no trace file behind, the same rule the plan site's
     `test_no_provider_leaves_no_trace_file` pins.
  3. `apps/cli/commands/mission_cmd.py:366`: pass `provider="ollama",
     provider_kind="ollama"` to `run_mission`, with the one-line WHY the plan
     site already carries at line 187 — `make_structured_call_fn` is
     Ollama-backed, and under `--no-llm` there is no call and so no trace to
     label.

C5 — the tests (own commit, test_orchestrator_loop.py)
  Add `TestOrchestratorEvidenceSink`, copying the shape of
  `TestMissionPlanEvidenceSink` (`tests/orchestration/test_mission_compiler.py:
  1162`). Use the existing module `mission` fixture and its `tmp_path` root;
  read the rows back from
  `mission_evidence_dir(PROJECT, mission.id, tmp_path) / "prompt_trace.jsonl"`.
  Four tests, no more:
  1. one run with a provider writes one row per call, and that row carries
     `role == "orchestrator"`, the provider label, and a NON-EMPTY
     `segment_manifest`;
  2. a SECOND run against the same mission APPENDS — the row count grows and
     the first run's rows survive. This is the test that pins the writer
     choice, so it must genuinely make two calls;
  3. `call_fn=None` leaves NO trace file: the no-provider terminal invents no
     evidence;
  4. a source guard that `remedy mission run` names its provider, copying
     `test_the_cli_names_the_provider_it_planned_with` and its declared
     formatting-sensitivity trade-off. It exists because tests 1-3 drive
     `run_mission` directly and stay green if the CLI stops passing the label.

C6 — plan and handback (own commit)
  Apply PAIR_C to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
  branch, this round's commit SHAs, a changed-files table with one row per
  path, the item-status table over C1a/C1b/C2/C3/C4/C5/C6, the gate table with
  REAL exit codes and REAL output, the open-findings count with their IDs, and
  the next expected action. Under 60 lines, or carry a DECISION D15
  "Deviations, declared" line naming the real count and the mandated content
  that caused it.

<<<PAIR_C_PLAN>>>
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
R32 is GATED; `LAST_REVIEWED_SHA` is cab89962.
R33 gives the ORCHESTRATOR prompt its call evidence: a per-iteration recorder
in `orchestrator_loop.py` carrying the segment manifest, and the sink appending
to the mission's `prompt_trace.jsonl` from INSIDE `run_mission` rather than
from a caller (DECISION F105 D11), so both callers —
`mission_cmd.py:366` and `gauntlet_runner.py:514` — inherit it.
Call evidence then reaches four prompts: both `do_cmd` flight-plan sites,
`remedy mission plan`, and the orchestrator loop.
Open findings: R-0221, R-0239, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- Name the gauntlet's provider at `gauntlet_runner.py:514`: its orchestrator
  rows reach evidence from R33 on but carry an empty label. One line, not a
  wiring round (DECISION F105 D11).
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
<<<END_PAIR_C_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r33-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r33-1.md`. Cap 400 (DECISION F105 D5).
  C application: PAIR_A and PAIR_B are APPEND, in DIFFERENT files, both in C2 —
    FROM exactly 1x in its own target, plus the TO-only ADDED-line count from
    `git show --numstat <C2> -- <path>` and the stray count over that path's
    ADDED lines in that commit. PAIR_C: `cmp` the applied `.agent/plan.md`
    against the sliced text; `wc -l` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in
    `.agent/live_review.md`, `.agent/decisions.md` and `.agent/plan.md` — 0 each.
  E scoped round gate: `python3 -m pytest tests/orchestration/
    test_orchestrator_loop.py tests/orchestration/test_orchestrator_prompt_golden.py -q`.
    The golden is in the gate because the prompt BYTES must not move.
  F caller suites: `python3 -m pytest tests/cli/test_mission_cmd.py
    tests/orchestration/test_gauntlet_runner.py
    tests/orchestration/test_mission_e2e.py -q`.
  G state-file contract: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  H canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  I red-proofs — ONLY in a disposable `git worktree` at HEAD, with
    `PYTHONDONTWRITEBYTECODE=1`, removed and pruned before the handback, and
    each one reverted (`git diff --stat` empty) before the next is applied:
    M1 delete the `append_trace_jsonl` call in `run_mission` — expect test 1
       and test 2 of C5 RED; report the exact counts.
    M2 swap `append_trace_jsonl` for `write_trace_jsonl` — expect C5 test 2
       RED and test 1 GREEN; report the exact counts.
    M3 delete `provider="ollama"` from the `run_mission` call in
       `mission_cmd.py` — expect C5 test 4 RED.
    If any mutation comes back GREEN, report the real colour and STOP the
    round there. A green mutation is evidence about the test, not a nuisance.
  J hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat <base>..HEAD` with the `+` column per commit,
    each under 500.
  K no scope drift: `git diff --name-only <base>..HEAD` lists exactly the nine
    paths the Change line names, and nothing else.
Handback:    completion report + the rewritten `.agent/handoff.md` described in
             C6. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
