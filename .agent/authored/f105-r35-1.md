── STEP R35 (session close) — F105 ───────────────────────────
Goal:        Record the R34 reviewer gate on disk, resolve R-0258, register the
             one Low finding R34 surfaced, and end the session with a handoff
             that names exactly where the next one starts.
Bundle:      C1 save this block · C2 the R34 gate record, the R-0258 resolution
             and R-0260 · C3 plan and the session-ending handoff.
Change:      `.agent/authored/f105-r35-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. No production code, no tests, no docs this round.
Constraints: State-file-only round. Do not touch `packages/`, `apps/`, `tests/`
             or `docs/`. Do not reflow any line you were not given a pair for.
             Do NOT move the misfiled R-0257 block: R-0259 stays OPEN and is
             fixed in its own round, next session.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r35-1.block.md`
      `.agent/authored/f105-r35-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — the R34 gate record, the R-0258 resolution, R-0260 (own commit, one file)
  Four pairs, all against `.agent/live_review.md`, all in this one commit.
  Declared shapes, to be MEASURED not assumed: PAIR_A REWRITE, PAIR_B
  CONTAINS-FROM, PAIR_C REWRITE, PAIR_D CONTAINS-FROM. For each rewrite prove
  FROM 0x and TO 1x after the write; for each CONTAINS-FROM prove FROM exactly
  1x. All four touch ONE path in ONE commit, so reconcile that path's ADDED and
  REMOVED counts against ALL FOUR pairs together (§4.9) — and count a line that
  appears in both a FROM and its TO as diff CONTEXT, not as an add and a
  remove: git emits only changed lines, so expecting otherwise manufactures
  phantom strays (the reviewer hit exactly that on R34 and it was the
  measurement, not the round).

<<<PAIR_A_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0260.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0261.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  into a per-call-site assertion so a second labelled call site is allowed.
  OPEN.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  into a per-call-site assertion so a second labelled call site is allowed.
  OPEN.
  Done: R-0258 (2026-08-10) — RESOLVED at F105 R34, commits 3c651516 and
  083a42d3. §3 of docs/agents/planner_reviewer_prompt.md now carries a SEVENTH
  pre-emission item: grep the suite for tests that COUNT a string over a whole
  file before ordering a change that adds that string. The guard that caused
  this is repaired in the same feature — `test_the_cli_names_the_provider_it_
  planned_with` asserts the label inside a window anchored at its own call site
  instead of `source.count(...) == 1` over all of `mission_cmd.py`. Verified by
  the reviewer against the real diff and by measurement, not from the handback:
  the file-wide count of `provider_kind="ollama"` is now 2 and the suite is
  green, which is precisely the state the old guard made impossible. The two
  call sites are 7335 characters apart, so neither window can see the other's
  label, and both R34 mutations went red as ordered — M1 taking only the run
  guard down while the plan guard stayed green, which is the property "scoped to
  its own call site" means. The remaining imprecision is registered separately
  as R-0260 and does not reopen this one.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  Registered here, fixed in its own round: doing it inside this commit would
  bury this round's real diff under a 27-line relocation. OPEN.

## Steps
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  Registered here, fixed in its own round: doing it inside this commit would
  bury this round's real diff under a 27-line relocation. OPEN.
- R-0260 (Low, F105 R34, reviewer-authored defect): the two per-call-site guard
  comments claim more precision than the code has. The authored comment says
  "The window is the call expression itself", and the run-site test repeats the
  shape, but a 200-character window from `outcome = plan_mission(` overshoots
  that call by 71 characters — measured, not estimated — spilling into
  `except MissionPlanInProgressError as exc:` and the first characters of the
  next `print(`; the run site overshoots its 173-character call by 27. The
  guarded PROPERTY holds and was proved to hold: the call sites are 7335
  characters apart, so no window reaches the other's label, and both mutations
  went red. So this is an inaccurate claim on disk, not a broken test — but it
  is a comment written to teach the next reader what the guard pins, landed by
  the very round whose subject was guards that promise more than they check.
  The R34 worker measured the overshoot and declared it rather than silently
  tightening the constant, which was right: the wording is the reviewer's.
  Fix: bound each window at its call's closing parenthesis instead of a magic
  200, or correct both comments to say "200 characters from the call's start,
  which covers the call and a little after". OPEN.

## Steps
<<<END_PAIR_C_TO>>>

<<<PAIR_D_FROM>>>
  `LAST_REVIEWED_SHA` advances cab89962 -> af35adbc.
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
  `LAST_REVIEWED_SHA` advances cab89962 -> af35adbc.
- R34: SPLIT round — repair the file-wide source guard into a per-call-site
  assertion, install §3 checklist item 7, label the provider on
  `remedy mission run`, and document the gauntlet's absent label as deliberate.
- Reviewer gate on R34 (2026-08-10): PASS. Range `af35adbc..28fe51c3` = eight
  commits, read as a real diff: eleven paths, exactly the ones the block named;
  insertions per commit 398, 334, 123, 12, 7, 14, 17, 85 — each under 500.
  Transport disk to disk against the reviewer's surviving original: all three of
  `.remedy-wt/f105-r34-1.block.md`, `.agent/authored/f105-r34-1.md` and
  `.agent/last_block.md` carry
  `6d816a6434c6d98cdaafca3df7654580d2c5985abdef65398c9eccb8fb97c14e`, every
  `cmp` silent, 398 lines against D5's cap of 400.
  All eight FROM/TO pairs re-sliced from the COMMITTED authored file by the
  reviewer's own whole-line marker reader: declared shape equals measured shape
  for every one, four REWRITEs at FROM 0x / TO 1x and four CONTAINS-FROM at
  FROM 1x / TO 1x. PAIR_I byte-equal to the applied `.agent/plan.md` at 43 lines
  against the cap of 50. Strays 0 in both directions on all five written paths
  once the accounting is right: PAIR_H is a PREPEND, so its TO-only lines are
  the LEADING seven, and a line carried unchanged through a REWRITE is diff
  CONTEXT rather than an add plus a remove. The reviewer's first pass modelled
  both wrongly and reported three phantom strays against a round that had none;
  the corrected pass reconciles `+81/-1` on live_review.md, `+42/-0` on
  decisions.md, `+12/-0` on the prompt doc, `+7/-1` on the compiler test,
  `+7/-1` on the CLI and `+7/-0` on the gauntlet exactly.
  Gates re-run by THIS reviewer with real exit codes: the scoped gate
  `323 passed in 1.69s`, the frozen prompt golden inside it, so the composed
  BYTES still have not moved; the three caller suites `152 passed in 38.17s`;
  `tests/docs/` `294 passed in 0.25s`; the dashboard contract
  `70 passed in 3.92s`; the canary `42 passed in 19.55s`; `grep -c -E '^<<<'`
  prints 0 in all four written targets; `git status --porcelain` empty and
  `git worktree list` the primary alone.
  Both red-proofs reproduced by the reviewer in a disposable worktree at
  28fe51c3 with `PYTHONDONTWRITEBYTECODE=1`, each reverted and the revert proved
  by an empty `git diff --stat`, worktree removed and pruned. Baseline
  `2 passed in 0.39s`. M1, deleting the label from the `run_mission` call: the
  run guard RED and the plan guard GREEN — the two guards watch different call
  sites, which is the whole point of the repair. M2, moving the label onto the
  `plan_mission` call: the run guard RED, so the repaired guard is per-call-site
  and not a disguised count.
  The block's own C4-before-C5 ordering was honoured and matters: the repaired
  guard was green at 083a42d3, BEFORE the second label landed at f3968dfd, so
  the suite was never red between two commits of this round.
  The worker's declared deviation is ACCEPTED and is not a defect of the round:
  the 200-character window overshoots its call, the worker measured that instead
  of quietly shrinking the constant, and the wording is the reviewer's. It is
  registered as R-0260 rather than absorbed. The 120-line handoff carries its
  DECISION D15 stated-cause line and drops no mandated section, which is the
  rule and not an exception.
  `LAST_REVIEWED_SHA` advances af35adbc -> 28fe51c3.
<<<END_PAIR_D_TO>>>

C3 — plan and the session-ending handoff (own commit)
  Apply PAIR_E to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` as the SESSION-ENDING handoff. It must state, in its own
  words and with real numbers: the feature and round (F105 R35, session close);
  the branch; this round's commit SHAs; a changed-files table with one row per
  path; the item-status table over C1a/C1b/C2/C3; the gate table with REAL exit
  codes and REAL output; the open-findings count and their IDs; and the next
  expected action for the next session, which is: gate R35 over
  `28fe51c3..HEAD`, then the R-0259 relocation round.
  It must also say plainly that R35 itself carries NO on-disk gate entry by
  construction — it is the round that writes the record, so it cannot record a
  verdict on itself (docs/agents/planner_reviewer_prompt.md §4.13). That absence
  is the terminator of this session, not an omission; the next session gates it
  and no repair round is opened for it.
  Keep the handoff under 60 lines, or carry a DECISION D15 "Deviations,
  declared" line naming the real count and the mandated content that caused it.

<<<PAIR_E_PLAN>>>
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
R34 is GATED; `LAST_REVIEWED_SHA` is 28fe51c3. Call evidence reaches four
prompts: both `do_cmd` flight-plan sites, `remedy mission plan`, and the
orchestrator loop, whose sink lives inside `run_mission` so both callers inherit
it (DECISION D11). `remedy mission run` names its provider; the gauntlet's stays
unlabelled on purpose (DECISION D13).
R35 is the session-close round: it records the R34 gate, resolves R-0258,
registers R-0260 and writes the handoff. By construction it carries no gate
entry on itself (§4.13) — the next session gates it over `28fe51c3..HEAD`.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0259, R-0260.
No PR; one is created at CLOSURE.

## Next Steps
- R-0259: MOVE the misfiled R-0257 block to the end of `## Findings`, bytes
  unchanged, so the R30 gate record closes with its own `LAST_REVIEWED_SHA`
  line. Bundle R-0260's window fix with it — both are small and neither touches
  production code.
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
<<<END_PAIR_E_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r35-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r35-1.md`. Cap 400 (DECISION F105 D5).
  C application: PAIR_A and PAIR_C are REWRITEs (FROM 0x after, TO 1x after);
    PAIR_B and PAIR_D are CONTAINS-FROM (FROM 1x). All four land in ONE commit
    against ONE path, so reconcile that commit's ADDED and REMOVED counts
    against all four together, treating a line unchanged across a FROM/TO as
    context. PAIR_E: `cmp` the applied `.agent/plan.md` against the sliced
    text; `wc -l` must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in
    `.agent/live_review.md` and `.agent/plan.md` — 0 each.
  E state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  F canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  G no-code proof: `git diff --stat 28fe51c3..HEAD` must show paths under
    `.agent/` ONLY. NO mutation red-proof is ordered or run this round: nothing
    executable changes, so there is no branch to mutate (DECISION F105 D10,
    D8 checklist item 5).
  H hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 28fe51c3..HEAD` with the `+` column per commit,
    each under 500.
Handback:    completion report + the session-ending `.agent/handoff.md`
             described in C3. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
