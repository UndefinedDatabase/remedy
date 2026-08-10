── STEP R34 — F105 ───────────────────────────────────────────
Goal:        Unblock and finish what R33 could not: repair the file-wide source
             guard that made a correct second call site unsatisfiable, label the
             CLI's orchestrator provider, document why the gauntlet's stays
             unlabelled, and put the missing check on disk so the class stops
             recurring.
Bundle:      C1 save this block · C2 the R33 gate record, findings R-0258 and
             R-0259, DECISIONs D12 and D13 · C3 checklist item 7 · C4 the guard
             repair · C5 the CLI label and the gauntlet's declared absence ·
             C6 the source guard for the run command · C7 plan and handback.
Change:      `.agent/authored/f105-r34-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`, `docs/agents/planner_reviewer_prompt.md`,
             `tests/orchestration/test_mission_compiler.py`,
             `apps/cli/commands/mission_cmd.py`,
             `packages/orchestration/gauntlet_runner.py`,
             `tests/orchestration/test_orchestrator_loop.py`. Nothing else.
Constraints: Do NOT move the misfiled R-0257 block this round — R-0259 is
             REGISTERED here and fixed in its own round, so this round's
             live_review diff stays readable.
             Do NOT change `run_mission`, the recorder, or the sink: R33 gated
             PASS and its behaviour is settled.
             The guard repair must be GREEN at C4, before the label lands at C5.
             Commit in the stated order for that reason.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r34-1.block.md`
      `.agent/authored/f105-r34-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — the R33 gate record, two findings, two decisions (own commit, two files)
  Four pairs. PAIR_A, PAIR_B and PAIR_C target `.agent/live_review.md`;
  PAIR_D targets `.agent/decisions.md`. Declared shapes, to be MEASURED not
  assumed: PAIR_A REWRITE, PAIR_B REWRITE, PAIR_C CONTAINS-FROM (append),
  PAIR_D CONTAINS-FROM (append). For each rewrite prove FROM 0x and TO 1x
  after the write; for each append prove FROM exactly 1x and count the TO-only
  ADDED lines over THIS commit's diff FOR THAT PATH
  (`git show --numstat <C2> -- <path>`). Report strays per path, both
  directions. PAIR_A and PAIR_B both edit live_review.md, so that path's added
  and removed counts must reconcile against BOTH pairs together, not one.

<<<PAIR_A_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0258.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0260.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  `run_intake`, so it is its own round. OPEN.

## Steps
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  `run_intake`, so it is its own round. OPEN.

- R-0258 (Medium, F105 R33, reviewer-authored defect): the R33 block ordered
  `provider="ollama", provider_kind="ollama"` onto the `run_mission` call in
  `apps/cli/commands/mission_cmd.py` while
  `tests/orchestration/test_mission_compiler.py:1210` already asserted
  `source.count('provider_kind="ollama"') == 1` over the WHOLE of that file. The
  second label is CORRECT and makes the count 2, so the ordered change and the
  existing suite could not both hold. The R33 worker applied the edit, measured
  `assert 2 == 1`, reverted it and declared the deviation rather than landing a
  red test or editing a file outside its change set — which was right on both
  counts. Reproduced by the reviewer in a disposable worktree at af35adbc: the
  edit applied verbatim yields exactly that failure and
  `grep -c 'provider_kind="ollama"'` prints 2. Cost: C4 item 3 and C5 test 4 of
  R33 unlanded, and both `run_mission` callers still writing unlabelled rows.
  This is the SEVENTH instance of the unsatisfiable-gate class across F104 and
  F105 and the first whose counting gate lives in a test file the block never
  names: DECISION F105 D8's items 1-4 read the block, item 5 the code it points
  at, item 6 the file it writes into, and none of them reads the TESTS that
  already guard that file. Fix: a seventh checklist item, and repair the guard
  into a per-call-site assertion so a second labelled call site is allowed.
  OPEN.
- R-0259 (Medium, F105 R31, reviewer-authored defect): the R-0257 finding block
  sits at lines 1528-1554 of `.agent/live_review.md`, under `## Steps` instead
  of under `## Findings` — the R-0231 class in the mirror direction, and the
  second instance of it on this branch. It is worse than misplacement: the block
  was inserted INSIDE the R30 gate record, so that record's concluding
  ``LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.` line is orphaned at 1555,
  27 lines below the record it belongs to and directly beneath R-0257's
  resolution text. A reader parsing the round history attributes R30's advance
  to R-0257's `Done:` paragraph. R-0231's own resolution claimed "`## Findings`
  holds only findings again", and that invariant is broken again in the other
  direction. Fix: MOVE lines 1528-1554 to the end of `## Findings`, bytes
  unchanged, so the R30 record closes with its own advance line — proved as a
  MOVE and not a retype, the block occurring exactly 1x before and 1x after.
  Registered here, fixed in its own round: doing it inside this commit would
  bury this round's real diff under a 27-line relocation. OPEN.

## Steps
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  `LAST_REVIEWED_SHA` advances 9bd3a3e7 -> cab89962.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  `LAST_REVIEWED_SHA` advances 9bd3a3e7 -> cab89962.
- R33: SPLIT round — the orchestrator prompt's call evidence: a per-iteration
  recorder carrying the segment manifest, and the sink appending to the
  mission's `prompt_trace.jsonl` from inside `run_mission` (DECISION D11).
- Reviewer gate on R33 (2026-08-10): PASS, with one declared deviation accepted
  and its cause registered as R-0258 against the REVIEWER, not the worker.
  Range `cab89962..af35adbc` = eight commits, read as a real diff: eight paths,
  every one on the block's Change line, `mission_cmd.py` absent by the declared
  deviation; insertions per commit 293, 232, 79, 27, 55, 105, 2 — each under
  500. Transport disk to disk against the reviewer's surviving original: all
  three of `.remedy-wt/f105-r33-1.block.md`, `.agent/authored/f105-r33-1.md`
  and `.agent/last_block.md` carry
  `d6d9d2a8e0d03d646021ed101d7c5b83dacce65b66dc75c74e5ea92306f40d80`, every
  `cmp` silent, 293 lines against D5's cap of 400.
  The code was read bottom-up rather than taken from the report. The append sits
  in a `finally`, so a call that RAISES still leaves its evidence before the
  boundary turns the fault into a terminal — the ledger's durability, which a
  single flush after the loop would not have given. The recorder is rebuilt per
  iteration from that iteration's `ComposedPrompt`, and `_observe_call` is
  defined and consumed inside the same iteration, so no manifest can describe
  earlier bytes and the closure has no late-binding hazard. `on_call` is CHAINED
  rather than replaced. The two new module-level imports introduce no cycle:
  `prompt_trace` imports only `prompt_segments`.
  Gates re-run by THIS reviewer with real exit codes: the scoped gate
  `201 passed in 1.15s` including the frozen prompt golden, so the composed
  BYTES did not move; the three caller suites `152 passed in 38.12s`;
  `tests/docs/` `294 passed in 0.30s`; the dashboard contract
  `70 passed in 3.96s`; the canary `42 passed in 19.46s`; `git status
  --porcelain` empty and `git worktree list` the primary alone.
  All three red-proofs reproduced by the reviewer in a disposable worktree at
  af35adbc with `PYTHONDONTWRITEBYTECODE=1`, each reverted and the revert proved
  by an empty `git diff --stat`, worktree removed and pruned. Baseline
  `3 passed in 0.33s`. M1, deleting the `append_trace_jsonl` call:
  `2 failed, 1 passed`, the two named tests RED. M2,
  `append_trace_jsonl` -> `write_trace_jsonl`: `1 failed, 2 passed`, only
  `test_a_second_run_appends_rather_than_truncating` RED — so the append is
  pinned as the writer, not merely used. M3 as ORDERED was unrunnable and the
  worker said so; the reviewer applied the ordered edit anyway to test the
  worker's account of WHY, and it failed exactly as reported.
  The handback's own corrections hold: the R-0149 self-reference exception it
  cites for the trailing bookkeeping commit is really in
  docs/agents/handback_template.md, and its note that D11 and PAIR_C's Next
  Steps understate the gap by one caller is correct — both reviewer-authored,
  applied verbatim, and this round repairs the substance, not the wording.
  `LAST_REVIEWED_SHA` advances cab89962 -> af35adbc.
<<<END_PAIR_C_TO>>>

<<<PAIR_D_FROM>>>
`run_mission`, and flushing a caller-owned `traces` list in each of the two
callers instead.
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
`run_mission`, and flushing a caller-owned `traces` list in each of the two
callers instead.

D12 — §3's pre-emission checklist gains a SEVENTH item: before ordering a change
that ADDS a string to a file, grep the suite for tests that COUNT that string
over that whole file. R33 lost two of its items to a guard nobody looked at:
`test_mission_compiler.py` asserted `source.count('provider_kind="ollama"') == 1`
over all of `mission_cmd.py`, so a correct second call site could not land
(finding R-0258, the seventh instance of the unsatisfiable-gate class).

The four earlier items read the block's own bytes, item 5 reads the code the
block points at, item 6 reads the file the block writes into. This one reads the
TESTS that already guard that file — a fourth place, which is why it is a
seventh item and not a clause bolted onto item 6.

The alternative — forbid file-wide `source.count(...)` guards outright — was
rejected: they are the only cheap way to pin a CLI wiring line no behavioural
test reaches (F105 R28 introduced them deliberately). The defect is the SCOPE,
not the technique, so the rule is "scope the guard to its call site".

Reverse this decision by deleting this entry and §3 checklist item 7.

D13 — Remedy deliberately does NOT label the provider on the gauntlet's
`run_mission` call. D11 left it as "a one-line round"; reading the call site
retires that plan. `apps/cli/commands/mission_cmd.py` can honestly name Ollama
because `_orchestrator_call_fn` is unconditionally `make_structured_call_fn`.
The gauntlet's call_fn arrives through `deps.move_call_fn()`, a substitutable
seam whose default is Ollama but whose whole purpose is being replaced, so a
hardcoded label there would write a guess into evidence every time a caller
substituted the seam.

An EMPTY label already means "the caller did not name it", which `run_mission`'s
docstring states, and which is exactly true of the gauntlet. Unlabelled is
honest; mislabelled is not, and this repository records unmeasured cost as
unmeasured rather than estimating it into the record.

The alternative — thread a provider label through the deps object so the
gauntlet reports the provider it actually used — is the RIGHT fix and is not
rejected, only deferred: it is a deps-shape change, not a one-liner, and F105 is
about prompt composition. The absence is documented at the call site so a reader
searching for the missing label finds the reason instead of a gap.

Reverse this decision by threading the label through `GauntletDeps` and passing
it at that call site.
<<<END_PAIR_D_TO>>>

C3 — checklist item 7 (own commit, docs/agents/planner_reviewer_prompt.md)
  PAIR_E, CONTAINS-FROM (append after item 6, before the "Why this is on disk"
  paragraph). This is the R-0258 fix. Prove FROM 1x and count TO-only added
  lines over this commit's diff.

<<<PAIR_E_FROM>>>
     three separate checks (finding R-0253).
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
     three separate checks (finding R-0253).
  7. **Source guards the block never names.** Before ordering a change that ADDS
     a string to a file, grep the suite for tests that COUNT that string over
     that WHOLE file (`rg -l '<basename>' tests/`, then read every `count(` and
     `== 1` assertion in what it returns). An existing
     `source.count('...') == 1` guard makes a correct SECOND call site
     unsatisfiable, and the worker cannot repair it without leaving its change
     set — so the round loses the item and spends a deviation proving a reviewer
     mistake. Items 1-4 read the block, item 5 the code the block points at,
     item 6 the file the block writes into, and this one the tests that already
     guard that file: four different places, four checks (finding R-0258).
     Such guards are worth keeping — they pin CLI wiring no behavioural test
     reaches — so scope them to their call site rather than deleting them.
<<<END_PAIR_E_TO>>>

C4 — the guard repair (own commit, tests/orchestration/test_mission_compiler.py)
  PAIR_F, REWRITE. This commit must be GREEN on its own: run
  `python3 -m pytest tests/orchestration/test_mission_compiler.py -q` BEFORE
  moving on, and record the count. The window is 200 characters, which covers
  the plan call's own two lines and nothing after them.

<<<PAIR_F_FROM>>>
        assert source.count('provider_kind="ollama"') == 1
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
        # Scoped to THIS call site rather than counted over the whole file: a
        # SECOND labelled call in the same module is correct and must not turn
        # this red (R-0258, which cost F105 R33 two items). The window is the
        # call expression itself, so a label that drifts to another call no
        # longer satisfies the guard.
        planned = source.index("outcome = plan_mission(")
        assert 'provider_kind="ollama"' in source[planned:planned + 200]
<<<END_PAIR_F_TO>>>

C5 — the CLI label and the gauntlet's declared absence (own commit, two files)
  PAIR_G, REWRITE, against `apps/cli/commands/mission_cmd.py`. PAIR_H,
  CONTAINS-FROM, against `packages/orchestration/gauntlet_runner.py`.

<<<PAIR_G_FROM>>>
    result = run_mission(mission.id, limits, project_id=project_id,
                         call_fn=call_fn)
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
    # `_orchestrator_call_fn` is unconditionally `make_structured_call_fn`,
    # which is Ollama-backed, so the provider is named here exactly as the plan
    # site above names it. Under `--no-llm` there is no call and so no trace to
    # label. The label reaches the prompt trace through `run_mission`'s own
    # per-iteration recorder (DECISION F105 D11).
    result = run_mission(mission.id, limits, project_id=project_id,
                         call_fn=call_fn,
                         provider="ollama", provider_kind="ollama")
<<<END_PAIR_G_TO>>>

<<<PAIR_H_FROM>>>
            result = deps.run_mission(
<<<END_PAIR_H_FROM>>>

<<<PAIR_H_TO>>>
            # Remedy deliberately does NOT name the provider here, so these
            # rows reach evidence unlabelled (DECISION F105 D13). The CLI site
            # can name Ollama because its call_fn is always
            # `make_structured_call_fn`; this call_fn arrives through `deps`, a
            # seam whose purpose is being substituted, so a hardcoded label
            # would write a guess into evidence. An empty label already means
            # "the caller did not name it", which is what happened.
            result = deps.run_mission(
<<<END_PAIR_H_TO>>>

C6 — the source guard for the run command (own commit,
     tests/orchestration/test_orchestrator_loop.py)
  Add a fourth test to `TestOrchestratorEvidenceSink`, the one R33 could not
  write. It reads `apps/cli/commands/mission_cmd.py` and asserts that
  `provider_kind="ollama"` appears WITHIN the `result = run_mission(` call
  expression — scoped to that call site, per checklist item 7, never a file-wide
  count. Docstring: it exists because tests 1-3 drive `run_mission` directly and
  stay green if the CLI stops passing the label, and it is formatting-sensitive
  by nature, the same declared trade-off as
  `test_the_cli_names_the_provider_it_planned_with`.
  Do NOT assert anything about `gauntlet_runner.py`: its absence of a label is
  deliberate (D13) and pinning an absence would freeze a decision that is meant
  to be reversible.

C7 — plan and handback (own commit)
  Apply PAIR_I to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
  branch, this round's commit SHAs, a changed-files table with one row per path,
  the item-status table over C1a/C1b/C2/C3/C4/C5/C6/C7, the gate table with REAL
  exit codes and REAL output, the open-findings count with their IDs, and the
  next expected action. Under 60 lines, or carry a DECISION D15 "Deviations,
  declared" line naming the real count and the mandated content that caused it.

<<<PAIR_I_PLAN>>>
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
R33 is GATED; `LAST_REVIEWED_SHA` is af35adbc. Call evidence reaches four
prompts: both `do_cmd` flight-plan sites, `remedy mission plan`, and the
orchestrator loop, whose sink lives inside `run_mission` so both callers inherit
it (DECISION D11).
R34 repairs what blocked R33: the file-wide source guard becomes a per-call-site
assertion (R-0258), §3 gains checklist item 7, `remedy mission run` names its
provider, and the gauntlet's absence of a label is documented as deliberate
(DECISION D13) rather than left as a pending one-line round.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0259.
No PR; one is created at CLOSURE.

## Next Steps
- R-0259: MOVE the misfiled R-0257 block (live_review.md 1528-1554) to the end
  of `## Findings`, bytes unchanged, so the R30 gate record closes with its own
  `LAST_REVIEWED_SHA` line. A state-file round of its own.
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
<<<END_PAIR_I_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r34-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r34-1.md`. Cap 400 (DECISION F105 D5).
  C application: per-pair, with the DECLARED shape MEASURED — PAIR_A, PAIR_B,
    PAIR_F and PAIR_G are REWRITEs (FROM 0x after, TO 1x after); PAIR_C, PAIR_D,
    PAIR_E and PAIR_H are CONTAINS-FROM (FROM 1x, plus the TO-only ADDED-line
    count from `git show --numstat <commit> -- <path>` and the stray count over
    that path's ADDED lines in that commit). PAIR_I: `cmp` the applied
    `.agent/plan.md` against the sliced text; `wc -l` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in `.agent/live_review.md`,
    `.agent/decisions.md`, `.agent/plan.md` and
    `docs/agents/planner_reviewer_prompt.md` — 0 each.
  E the guard repair alone, AT C4 before the label lands:
    `python3 -m pytest tests/orchestration/test_mission_compiler.py -q`.
  F scoped round gate, after C6: `python3 -m pytest
    tests/orchestration/test_mission_compiler.py
    tests/orchestration/test_orchestrator_loop.py
    tests/orchestration/test_orchestrator_prompt_golden.py -q`.
  G caller suites: `python3 -m pytest tests/cli/test_mission_cmd.py
    tests/orchestration/test_gauntlet_runner.py
    tests/orchestration/test_mission_e2e.py -q`.
  H docs and state contract: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
    `docs/` changes this round, so the docs gate is not optional.
  I canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J red-proofs — ONLY in a disposable `git worktree` at HEAD, with
    `PYTHONDONTWRITEBYTECODE=1`, each reverted and the revert proved by an empty
    `git diff --stat` before the next, worktree removed and pruned:
    M1 delete `provider="ollama", provider_kind="ollama"` from the
       `run_mission` call in `mission_cmd.py` — expect the C6 test RED and
       `test_the_cli_names_the_provider_it_planned_with` GREEN, which together
       prove the two guards are scoped to different call sites.
    M2 move the label from the `run_mission` call to the `plan_mission` call, so
       the file-wide count is 2 either way — expect the C6 test RED. This is the
       proof the repaired guard is per-call-site and not a disguised count.
    If a mutation comes back GREEN, report the real colour and STOP the round
    there.
  K hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat <base>..HEAD` with the `+` column per commit, each
    under 500.
  L no scope drift: `git diff --name-only <base>..HEAD` lists exactly the eleven
    paths the Change line names, and nothing else.
Handback:    completion report + the rewritten `.agent/handoff.md` described in
             C7. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
