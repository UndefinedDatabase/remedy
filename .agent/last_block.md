── STEP integration gate (completion) / F107 R14 ──────────────
Goal:        Finish the integration gate R13 began and lost to a dead session:
             fresh full-suite runs on this branch and at the merge base
             2e4142c3, the base worktree's UI parity ACTUALLY neutralized this
             time, every base-only id attributed by direct evidence, the whole
             run committed as evidence under `.agent/gate_f107_r14/`. The two
             new findings reach `.agent/live_review.md` FIRST, so nothing is
             lost if this session dies mid-suite too.
Bundle:      C1 save this block · C2 mirror it · C3 apply the two authored
             live_review pairs · C4 the gate runs + their evidence dir · C5 plan
             · C6 handoff.
Change:      exactly these SIX paths, nothing else:
             .agent/authored/f107-r14-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the two pairs below ONLY)
             .agent/gate_f107_r14/** (new dir, C4)
             .agent/plan.md (C5, full replacement by slice PLAN14)
             .agent/handoff.md (C6)

State you are resuming, verified by the reviewer before this block was written:
R13's C1, C2 and C3 are already committed (ee461db7, 708d3306, 5468be28) and
their transport proof holds — `.agent/authored/f107-r13-1.md` and
`.agent/last_block.md` both sha256 to 5fd436727e378348a1… , the value the
reviewer original's trailer declares. R13 died during its C4. Its scratch under
`.remedy-wt/gate-scratch/f107-r13/` and the base worktree it left behind are
NOT evidence and are NOT to be copied anywhere. HEAD is 5468be28 and the branch
is one commit behind origin's d7dd12b6 push — pushing at C6 covers all of it.

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase, revert or delete a
   branch other than the throwaway `tmp/base-gate` this block manages.
 - NO PRODUCTION CODE, NO TEST CODE MOVES THIS ROUND. `packages/`, `apps/` and
   `tests/` are frozen: `git diff --stat 5468be28..HEAD -- packages apps tests`
   must be EMPTY at handback. This round measures; it does not repair.
 - DO NOT repair the five failing `[reviewer]` ids in
   `tests/orchestration/test_role_conventions.py`. They fail at the merge base
   too, they are registered below as R-0286, and fixing them here would mix an
   unrelated fix into a feature branch (AGENTS.md Core Workflow).
 - A red integration gate is NOT repaired here either. If a BRANCH-ONLY failure
   is reproducible and coupled to F107 code, STOP after C4, record it, and hand
   back — the fix is its own reviewer-gated round (integration_gate.md step 4).
 - Do NOT create a PR, do NOT run the closure evidence job or the review zip,
   do NOT edit docs/roadmap/STATUS.md. Closure is the next round.
 - Do NOT write a `Done:` or `Landed:` line of your own anywhere.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line, path or count that does not exist, STOP that item, do
   the safe thing, and DECLARE the correction in the handback. A declared
   deviation costs nothing; an undeclared one costs the round.

Detail for C4 — the gate, per docs/agents/integration_gate.md. Read that file
first; it governs, and what follows only pins this run's specifics.
 - Run logs are written OUTSIDE the repo worktree while a suite runs and copied
   into `.agent/gate_f107_r14/` only after the run exits (R-0176: a log growing
   inside the repo changes the worktree digest mid-run and reddens the
   manifest-identity ids as false positives). Use the gitignored
   `.remedy-wt/gate-scratch/f107-r14/` as the scratch dir.
 - Evidence file names end in `.txt`, never `.log` (R-0169: `.gitignore` drops
   `*.log` and the review-zip guard rejects any `\.log$` member).
 1. BRANCH RUN, from the repo root with a clean tree at the C3 head:
    `python3 -m pytest -n auto -q`. Record in `branch_run.txt`: cwd, HEAD sha,
    branch, the exact command, start/end UTC, the raw TAIL (last ~25 lines),
    `PYTEST_EXIT_CODE` and wall_clock_seconds. Then
    `grep '^FAILED' <log> | sort > .agent/gate_f107_r14/branch_failed.txt`
    (an empty file if there are none — create it either way).
 2. BASE RUN. A worktree at 2e4142c3 on branch `tmp/base-gate` ALREADY EXISTS at
    `.remedy-wt/base-gate`, left by the dead R13 session. VERIFY all three
    before reusing it: `git -C .remedy-wt/base-gate rev-parse HEAD` ==
    2e4142c3ac72042ac4d704da252db263e48dcba3, `git -C .remedy-wt/base-gate
    status --porcelain` empty, and `git -C .remedy-wt/base-gate branch
    --show-current` == tmp/base-gate. If ANY check fails: `git worktree remove
    --force .remedy-wt/base-gate`, `git worktree prune`, `git branch -D
    tmp/base-gate`, then `git worktree add -b tmp/base-gate .remedy-wt/base-gate
    2e4142c3`. Record in `base_worktree.txt` which path you took and the real
    exit codes — a THROWAWAY BRANCH, never detached: the self-dogfood branch
    guard refuses a detached HEAD by design (DECISION D3).
    Restore UI parity BY COPY, never by symlink (the auto-build writes THROUGH a
    symlink into the primary checkout): ensure `apps/ui/node_modules` and
    `apps/ui/dist` exist in the base worktree, `cp -a` from the primary checkout
    if either is missing or if the dist content hash differs.
    THEN THE STEP R13 LACKED, and the reason its base run was worthless: after
    the copy, make every `apps/ui/dist` entry NEWER than the base worktree's
    sources — `find .remedy-wt/base-gate/apps/ui/dist -exec touch {} +`. R13's
    base run failed seven `tests/ui_server/test_live_state.py` ids for one
    mechanical reason: `git worktree add` gave `apps/ui/src/**` fresh checkout
    mtimes (18:09) newer than the copied `dist/index.html` (18:06), the
    staleness check fired, and `REMEDY_UI_NO_AUTO_BUILD=1` then refused the
    rebuild it asked for. Touching dist restores the mtime ordering the primary
    checkout has and changes no byte — the content hash proves it.
    Record in `dist_hashes.txt`, by `find apps/ui/dist -type f -print0 | sort -z
    | xargs -0 sha256sum | sha256sum`, the aggregate CONTENT hash of
    `apps/ui/dist` BEFORE and AFTER the base run for BOTH the base worktree and
    the primary checkout, plus — for the base worktree, before the run — the
    newest source mtime and the dist mtime, proving the ordering. A changed
    PRIMARY hash means something wrote through: stop and report it. A changed
    BASE hash voids the parity claim and forces per-id attribution instead.
    Then, from the base worktree root: `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m
    pytest -n auto -q`. Record `base_run.txt` and `base_failed.txt` the same way
    as step 1.
 3. COMPARE, into `comm_branch_only_failures.txt` (`comm -13 base_failed.txt
    branch_failed.txt`) and `comm_base_only_failures.txt` (`comm -23`). Both
    files are created even when empty.
 4. ATTRIBUTE, into `attribution.txt`, following the shape of the accepted
    `.agent/gate_f105_r49/attribution.txt` (read it — it is the precedent, not a
    template to copy blindly). It carries: the headline numbers for both runs
    with real exit codes and wall clock; the collected-test delta between branch
    and base with its cause; the two `comm` counts; and a PER-ID verdict table
    in which EVERY id from BOTH comm files appears exactly once, none silently
    absent. For every BRANCH-ONLY id: serial re-run of the exact node id —
    serial-pass means the xdist-flake class (record, not a blocker); serial-fail
    means reproduce it at the merge base before blaming F107. For every
    BASE-ONLY id: name the missing artifact or the mechanism per id by direct
    evidence, or it counts as a genuine base failure and blocks the verdict.
    ADD a COMMON FAILURES section the F105 precedent has no equivalent of: the
    ids that fail in BOTH runs, with their count, named as R-0286 and explicitly
    NOT charged to F107. Say plainly there that they are why both runs exit 1.
    End the file with the line `VERDICT IS NOT ISSUED HERE` and the reason
    (integration_gate.md step 5: only the reviewer issues the gate verdict).
 5. CLEAN UP, into `worktree_cleanup.txt`: `git worktree remove --force
    .remedy-wt/base-gate`, `git worktree prune`, `git branch -D tmp/base-gate`,
    then `git worktree list` and `git branch --list 'tmp/*'` as proof, with the
    real exit codes. The primary checkout satisfies `git status --porcelain`
    empty afterwards.
 6. Keep each evidence file small: TAILS and lists, never a full 16k-test log.
    If any single evidence file would exceed 400 lines, trim it to the head and
    tail with an explicit `[... N lines elided ...]` marker.

Detail for C5 and C6:
 - Replace `.agent/plan.md` entirely with slice PLAN14; `cmp` and `sha256sum`
   against the marker.
 - Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It must
   carry: feature and round, branch, the per-commit changed-files table for
   C1-C6, the verification table below with REAL exit codes and counted values,
   BOTH gate headline numbers, the branch-only, base-only AND common-failure
   counts, the open-findings count with its IDs, and the next expected action
   (closure per docs/roadmap/STATUS_closure_protocol.md). Keep it under 100
   lines; if the mandated content genuinely does not fit, exceed the cap and
   carry the DECISION D15 "Deviations, declared" line naming the real line count
   and the specific mandated content that caused it. Never drop a section to fit.

<<<BEGIN SLICE HDR5FROM sha256=7e5c39d424ecde0c939bc254410e6ce2a3e7381f8df9c5313ac0319b928ee8c5 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0286.
<<<END SLICE HDR5FROM>>>
<<<BEGIN SLICE HDR5TO sha256=e30850b93fa81a2759aa1571653d97ce569fc39d8852567c4fc0d0d09349b6d6 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0288.
<<<END SLICE HDR5TO>>>
<<<BEGIN SLICE LRF10FROM sha256=aef358c081af72086e98cfc79586351eb1cb93abce261974b62dbdb07dca01b8 lines=1>>>
  a zero-gate over `^Landed:` is safe only in a round that lands no fix. OPEN.
<<<END SLICE LRF10FROM>>>
<<<BEGIN SLICE LRF10TO sha256=1e57596a36608d3ee3b0ed4bb2a1531e76653175ba954684aeb4d1527f31c39e lines=29>>>
  a zero-gate over `^Landed:` is safe only in a round that lands no fix. OPEN.

- R-0286 (Medium, F107 R13 integration gate): the full suite is RED at the merge
  base 2e4142c3 and on this branch with the SAME five ids — every `[reviewer]`
  parametrization in `tests/orchestration/test_role_conventions.py` — because
  `docs/agents/reviewer_conventions.md` estimates 954 tokens against the 800-token
  cap `packages/orchestration/role_conventions.py` declares, so composing the
  segment raises `PromptSegmentError` before any assertion in those tests runs.
  It is pre-existing and not F107's: the document last changed at merge a85e82f5
  ("keep both sections", +17 lines), an ancestor of the merge base, and
  `git diff 2e4142c3..HEAD` touches neither that document nor
  `role_conventions.py` nor `prompt_segments.py`. F107 does not repair it —
  AGENTS.md Core Workflow bars mixing an unrelated fix into a feature branch —
  and the gate verdict is unaffected, because ids failing in BOTH runs are
  common failures and appear in neither comm file. The severity is Medium and
  not High deliberately: a High finding sets `high_blockers_open`, which blocks
  `remedy integrity check`, the review zip and therefore this feature's closure,
  charging F107 for a defect that landed on `main` before the branch was cut.
  The reviewer prompt-segment path stays broken in production until a follow-up
  trims the document under its cap or raises the cap on purpose. OPEN.
- R-0287 (Low, F107 R13 integration gate): `docs/agents/planner_reviewer_prompt.md`
  §4.4 routes every severity decision to "the canonical scale in
  review_protocol.md", but no `docs/agents/review_protocol.md` exists on disk.
  The repository's severity scale therefore has no carrier, and every Low,
  Medium and High in this file was assigned from precedent rather than from a
  written rule. Same citation-accuracy class as R-0239 and R-0247, one level up:
  the dangling pointer sits in a governing document instead of in a round's
  block. Recorded, not repaired here — editing an agent-governance document is
  outside this feature's change set. OPEN.
<<<END SLICE LRF10TO>>>
<<<BEGIN SLICE PLAN14 sha256=f9762e6bbcc159e02632043746b3ac8cf83e50d7884979af5103c3fd4834584e lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0288. R12 reviewed PASS at d7dd12b6.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R14 — the integration gate per docs/agents/integration_gate.md, completing what
R13 began before its session died mid-run: fresh full-suite runs on the branch
and at the merge base 2e4142c3 with the base worktree's UI parity actually
neutralized, every base-only id attributed, the evidence committed under
`.agent/gate_f107_r14/`. Findings R-0286 and R-0287 land first. T001-T004 are
complete and reviewed; no production code moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR. The five
   pre-existing `[reviewer]` failures (R-0286) are carried as a documented
   risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END SLICE PLAN14>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r14-1.md`. The expected
    digest is the BLOCK_SHA256 line the reviewer original
    `.remedy-wt/f107-r14-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the two pairs to `.agent/live_review.md` by exact-string replacement
    of the FROM body with the TO body, verifying each slice's sha256 BEFORE use
    and checking that each FROM occurs exactly 1x before you replace it. HDR5 is
    a REWRITE (FROM and TO are disjoint); LRF10 is an APPEND (its TO literally
    CONTAINS its FROM). Commit C3 alone. Do not touch this file again for the
    rest of the round.
 4. Run the gate exactly as Detail-C4 prescribes, then commit the evidence dir
    as C4. The branch run happens at the C3 head with a clean tree.
 5. Replace `.agent/plan.md` entirely with slice PLAN14. Commit C5.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C6. Push the branch.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r14-1.md .agent/last_block.md` -> exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Each of the five slice bodies recomputes to its BEGIN-marker digest at its
    declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` -> the deletion column is
    exactly 1, HDR5 being the only REWRITE. Then, LINE-ANCHORED:
    `grep -c '^> Branch:.*Next free ID: R-0288'` -> 1;
    `grep -c '^> Branch:.*Next free ID: R-0286'` -> 0; `grep -c '^- R-0286'` ->
    1; `grep -c '^- R-0287'` -> 1; `grep -c '^Done:'` -> 9;
    `grep -c '^Landed:'` -> 0; `grep -c '^## Steps'` -> 1; `grep -c '^<<<'` -> 0
    (also 0 in `.agent/plan.md` and `.agent/handoff.md`).
 d. THE GATE ITSELF. Report, as raw values, for BOTH runs: the exact command,
    the passed/skipped/failed counts, the pytest exit code and the wall clock.
    Report the two comm counts and the common-failure count. Report, per
    branch-only id, its serial re-run result. The gate is GREEN for the reviewer
    only if every branch-only id is either absent or attributed to the
    xdist-flake class by a serial pass, and every base-only id is attributed to
    the environment class by named direct evidence.
 e. `sha256sum .agent/plan.md` == the PLAN14 marker digest; `cmp` against the
    extracted slice -> exit 0, silent; the file is 29 lines.
 f. Canary, in the primary checkout after the worktree is gone:
    `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
 g. `git diff --stat 5468be28..HEAD -- packages apps tests` -> EMPTY output.
 h. `git status --porcelain` -> empty; `git worktree list` -> the primary
    checkout ALONE; `git branch --list 'tmp/*'` -> empty; HEAD ==
    origin/feature/f107-context-compiler-v2 after the push; insertions per
    commit, each < 500.
 i. `git diff --name-only 5468be28..HEAD` -> exactly the paths of the Change
    list and nothing else (the sixth, `.agent/handoff.md`, arrives with C6, so
    a measurement taken before C6 legitimately shows five plus the gate dir —
    say which you measured).
 j. `remedy integrity check --json` -> record the verdict verbatim. This is a
    closure precondition (STATUS_closure_protocol.md precondition 3) and the
    next round needs the value; a non-PASS is reported, not repaired here. If
    the command is unavailable or refused in your environment, record the exact
    error text instead — an absent value is a finding, a reported failure is not.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C6, and every gate above with its real exit code and counted
value. Declare any deviation.
──────────────────────────────────────────────────────────────
