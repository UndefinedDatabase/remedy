── STEP R36 — F105 ───────────────────────────
Goal:        Relocate the misfiled R-0257 block so the R30 gate record closes
             with its own advance line (R-0259), correct the two guard-window
             comments that claim more precision than the code has (R-0260),
             and record the R35 reviewer gate.
Bundle:      C1 save this block · C2 the byte-preserving MOVE · C3 the R35 gate
             record plus both `Landed:` lines · C4 the two comment fixes ·
             C5 plan and handoff.
Change:      `.agent/authored/f105-r36-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
             `tests/orchestration/test_mission_compiler.py`,
             `tests/orchestration/test_orchestrator_loop.py`. Nothing else.
             No production code: the two test edits change COMMENT and
             DOCSTRING TEXT only — no executable line moves.
Constraints: Do not touch `packages/`, `apps/` or `docs/`. Do not reflow any
             line you were not given a pair for. C2 changes the ORDER of lines
             in `.agent/live_review.md` and NOTHING else: no `Landed:` line, no
             wording fix, no whitespace change may ride in that commit, or its
             multiset proof is void. Do not change the number 200 in either
             guard — R-0260 is fixed by making the comments true, not by
             retuning a window whose guarded property is already proved.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r36-1.block.md`
      `.agent/authored/f105-r36-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — MOVE the misfiled R-0257 block (own commit, one file, order-only)
  The block is 27 lines. It BEGINS at the whole line in ANCHOR_BLOCK_FIRST and
  ENDS at the whole line in ANCHOR_BLOCK_LAST — measured unique in
  `.agent/live_review.md`, 1x each, at lines 1596 and 1622.
  Remove those 27 lines from where they sit under `## Steps` and re-insert
  them, BYTES UNCHANGED and in the same order, directly AFTER the whole line in
  ANCHOR_DEST_AFTER — measured unique, line 590, the last line of R-0260 and
  therefore the last line of `## Findings`.
  Do it with a script under `.remedy-wt/`, never by retyping: match all three
  anchors as WHOLE lines, assert each occurs exactly 1x BEFORE the edit, and
  fail loudly rather than guess if any count is not 1.
  Why this matters: the block was inserted INSIDE the R30 gate record, so that
  record's ``LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.` line is
  orphaned 27 lines below the record it closes, directly under a `Done:`
  paragraph it does not belong to. After the move, that advance line follows
  its own gate record again and `## Findings` holds only findings.

<<<ANCHOR_BLOCK_FIRST>>>
- R-0257 (Medium, F105 R30, reviewer-authored defect): the R30 block lifted
<<<END_ANCHOR_BLOCK_FIRST>>>

<<<ANCHOR_BLOCK_LAST>>>
  the regression cannot return silently the way it arrived.
<<<END_ANCHOR_BLOCK_LAST>>>

<<<ANCHOR_DEST_AFTER>>>
  which covers the call and a little after". OPEN.
<<<END_ANCHOR_DEST_AFTER>>>

C3 — the R35 gate record and both `Landed:` lines (own commit, one file)
  Apply PAIR_S to `.agent/live_review.md`. Declared shape, to be MEASURED not
  assumed: CONTAINS-FROM — the TO opens with the FROM line verbatim and appends
  below it. Prove FROM exactly 1x after the write.
  Then add, in the SAME commit, two `Landed:` lines you author yourself
  (§4.4: a worker marks a landed fix `Landed: R-XXXX — <one line: what
  changed, which commit>` and never writes a `Done:` paragraph):
    · directly AFTER the whole line in ANCHOR_R0259_TAIL, one line for R-0259
      naming the C2 commit;
    · directly AFTER the whole line in ANCHOR_DEST_AFTER, one line for R-0260
      naming the C4 commit.
  Both anchors are measured unique. Note the ordering consequence and check it
  after the write: ANCHOR_DEST_AFTER is also C2's insertion point, so R-0260's
  `Landed:` line lands BETWEEN R-0260's `OPEN.` line and the block C2 moved
  there. That is the correct position — the line belongs to R-0260.
  Because you author these two lines, they are NOT hash-stamped; they are also
  the only text in this round you may word yourself.

<<<ANCHOR_R0259_TAIL>>>
  bury this round's real diff under a 27-line relocation. OPEN.
<<<END_ANCHOR_R0259_TAIL>>>

<<<PAIR_S_FROM>>>
  `LAST_REVIEWED_SHA` advances af35adbc -> 28fe51c3.
<<<END_PAIR_S_FROM>>>

<<<PAIR_S_TO>>>
  `LAST_REVIEWED_SHA` advances af35adbc -> 28fe51c3.
- R35: session-close round — record the R34 gate, resolve R-0258 with
  reviewer-authored text, register R-0260, and write the session-ending
  handoff. State-file-only; no mutation red-proof ordered or run.
- Reviewer gate on R35 (2026-08-10): PASS, by the reviewer of the FOLLOWING
  session. R35 was the last round of a SESSION, not of the branch, so it does
  get an on-disk entry: §4.13's terminator clause covers the last round of a
  BRANCH, and R35's own handoff correctly named this gate as the next action
  rather than claiming a verdict on itself.
  Range `28fe51c3..bcfb12e3` = four commits, five paths, every one under
  `.agent/` — `git diff --name-only` lists exactly the five the block named,
  nothing under `packages/`, `apps/`, `tests/` or `docs/`. Insertions per
  commit 242, 168, 81 and 61, each under 500; the 168/324 one is the
  single-state-file verbatim rewrite AGENTS.md exempts from the churn reading
  anyway.
  Transport disk to disk against the reviewer's surviving original — the
  PRIMARY proof shape, not the §4.9 digest fallback:
  `.remedy-wt/f105-r35-1.block.md`, `.agent/authored/f105-r35-1.md` and
  `.agent/last_block.md` all three carry
  `b14899d9c8b57331e26b27546ece4352a4b33ebac6831aa4d2f2ed98195ddc96`, both
  `cmp` runs silent, 242 lines against DECISION F105 D5's cap of 400.
  All five pairs re-sliced from the COMMITTED authored file by this reviewer's
  own whole-line marker reader: declared shape equals measured shape for every
  one. PAIR_A and PAIR_C are REWRITEs at FROM 0x / TO 1x; PAIR_B and PAIR_D are
  CONTAINS-FROM at FROM 1x; PAIR_E is byte-equal to the applied
  `.agent/plan.md` at 44 lines against the cap of 50. The four live_review
  pairs share ONE path in ONE commit and so reconcile TOGETHER against
  `+81/-1`: of the 81 added lines not one comes from outside a TO, and the
  single removed line is PAIR_A's FROM. Strays 0 in both directions, line
  multisets taken against `git show -U0`.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'`
  prints 0 in both written targets; `tests/docs/` `294 passed in 0.25s`; the
  dashboard contract `70 passed in 4.14s`; the canary `42 passed in 19.64s`;
  `git status --porcelain` empty and `git worktree list` the primary alone at
  this verdict.
  No red-proof was ordered or run, and that is the correct call rather than an
  omission: the round changed nothing executable, so there is no branch to
  mutate (D8 checklist item 5, DECISION F105 D10).
  `LAST_REVIEWED_SHA` advances 28fe51c3 -> bcfb12e3.
<<<END_PAIR_S_TO>>>

C4 — the two guard-window comments (own commit, two files)
  PAIR_F against `tests/orchestration/test_mission_compiler.py` and PAIR_G
  against `tests/orchestration/test_orchestrator_loop.py`. Declared shapes, to
  be MEASURED not assumed: both REWRITE. Prove FROM 0x and TO 1x after each
  write. Comment and docstring text only — no executable line changes, so no
  mutation red-proof is ordered this round either (D8 checklist item 5): the
  guards' behaviour is deliberately identical before and after, and both were
  already proved red-on-mutation at R34.

<<<PAIR_F_FROM>>>
        # Scoped to THIS call site rather than counted over the whole file: a
        # SECOND labelled call in the same module is correct and must not turn
        # this red (R-0258, which cost F105 R33 two items). The window is the
        # call expression itself, so a label that drifts to another call no
        # longer satisfies the guard.
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
        # Scoped to THIS call site rather than counted over the whole file: a
        # SECOND labelled call in the same module is correct and must not turn
        # this red (R-0258, which cost F105 R33 two items). The window is 200
        # characters from the call's start, which is the call plus 71
        # characters of what follows it — measured, not the call expression
        # exactly (R-0260). That is enough for the job the guard has: the run
        # site's label sits 7335 characters away, far outside this window, so a
        # label that drifts to that call no longer satisfies this one.
<<<END_PAIR_F_TO>>>

<<<PAIR_G_FROM>>>
        Scoped to THIS call site, never a file-wide count: the plan call in the
        same module carries its own label, and a count would make one of the two
        guards unsatisfiable (checklist item 7, finding R-0258).
<<<END_PAIR_G_FROM>>>

<<<PAIR_G_TO>>>
        Scoped to THIS call site, never a file-wide count: the plan call in the
        same module carries its own label, and a count would make one of the two
        guards unsatisfiable (checklist item 7, finding R-0258). The window is
        200 characters from the call's start, which is the call plus 27
        characters of what follows it — measured, not the call expression
        exactly (R-0260). It stays 7335 characters clear of the plan call's
        label, which is the property this guard exists to hold.
<<<END_PAIR_G_TO>>>

C5 — plan and handoff (own commit)
  Apply PAIR_P to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`. The handoff states, in your own words and with real
  numbers: feature and round (F105 R36); the branch; this round's commit SHAs;
  a changed-files table with one row per path; the item-status table over
  C1a/C1b/C2/C3/C4/C5; the gate table with REAL exit codes and REAL output;
  the open-findings count and their IDs; and the next expected action, which
  is: gate R36 over `bcfb12e3..HEAD`, then the R-0256 round (compose once, not
  twice — a signature change on `plan_job_llm` and `run_intake`).
  Keep it under 60 lines, or carry a DECISION D15 "Deviations, declared" line
  naming the real count and the mandated content that caused it.

<<<PAIR_P_PLAN>>>
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
R35 is GATED; `LAST_REVIEWED_SHA` is bcfb12e3. Call evidence reaches four
prompts: both `do_cmd` flight-plan sites, `remedy mission plan`, and the
orchestrator loop, whose sink lives inside `run_mission` so both callers inherit
it (DECISION D11). `remedy mission run` names its provider; the gauntlet's stays
unlabelled on purpose (DECISION D13).
R36 is the housekeeping round: it MOVES the misfiled R-0257 block to the end of
`## Findings` (R-0259), makes both guard-window comments say what the code
actually does (R-0260), and records the R35 gate. No production code.
Open findings: R-0221, R-0239, R-0247, R-0256 — plus R-0259 and R-0260, whose
fixes land this round and await the reviewer's `Done:` text.
No PR; one is created at CLOSURE.

## Next Steps
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round — the next one.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on the reviewer original in `.remedy-wt/`,
    `.agent/authored/f105-r36-1.md` and `.agent/last_block.md`; `cmp` all three.
  B size: `wc -l .agent/authored/f105-r36-1.md`. Cap 400 (DECISION F105 D5).
  C application, four parts:
    C2 the MOVE, three proofs together — `git show --numstat <C2> --
      .agent/live_review.md` is 27 added and 27 removed; the file's LINE
      MULTISET is unchanged, proved by comparing
      `git show <C2>^:.agent/live_review.md | sort | sha256sum` against
      `git show <C2>:.agent/live_review.md | sort | sha256sum` — the two
      digests must be EQUAL, which is what "bytes unchanged, order only" means;
      and `grep -c '^- R-0257 (Medium'` in `.agent/live_review.md` is 1 both
      before and after.
    PAIR_S CONTAINS-FROM: FROM exactly 1x after the write.
    PAIR_F and PAIR_G REWRITE: FROM 0x and TO 1x after each write.
    PAIR_P: `cmp` the applied `.agent/plan.md` against the sliced text; `wc -l`
      must be under 50.
  D marker leakage, LINE-anchored: `grep -c -E '^<<<'` in
    `.agent/live_review.md`, `.agent/plan.md`,
    `tests/orchestration/test_mission_compiler.py` and
    `tests/orchestration/test_orchestrator_loop.py` — 0 each.
  E state-file contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  F scoped round gate: `python3 -m pytest
    tests/orchestration/test_mission_compiler.py
    tests/orchestration/test_orchestrator_loop.py -q`.
  G canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  H comments-only proof for C4: `git show <C4> -- <both test files>` and show
    that every added and removed line begins, after its indentation, with `#`
    or is docstring prose inside the existing docstring — no `assert`, no
    `source.index`, no `200` changed. Paste the real diff lines.
  I hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat bcfb12e3..HEAD` with the `+` column per commit,
    each under 500.
Handback:    completion report + the rewritten `.agent/handoff.md` described in
             C5. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
