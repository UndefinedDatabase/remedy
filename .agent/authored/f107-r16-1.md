── STEP integration gate (completion, 3rd attempt) / F107 R16 ──
Goal:        Run the F107 integration gate to completion and commit its evidence:
             fresh full-suite runs on this branch and at the merge base 2e4142c3,
             the base worktree REBUILT from scratch and its UI parity proven to a
             file at the moment it is established, every branch-only and base-only
             id attributed by direct evidence, the whole run committed under
             `.agent/gate_f107_r16/`. R13, R14 and R15 each lost their session to
             this one step; the gate is the ONLY thing F107 still lacks.
Bundle:      C1 save this block · C2 mirror it · C3 the reviewer's findings and
             gate record · C4 the gate runs + their evidence dir · C5 plan ·
             C6 handoff.
Change:      exactly these FIVE tracked paths, nothing else:
             .agent/authored/f107-r16-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, three pairs below and NOTHING else)
             .agent/gate_f107_r16/** (new dir, C4)
             .agent/plan.md (C5, full replacement by slice PLAN16)
             .agent/handoff.md (C6)
             Plus ONE untracked move that belongs to no commit, done first:
             `.agent/gate_f107_r15/` leaves the repository (step 0 below).

State you are resuming, verified by the reviewer against the files themselves,
not quoted from a summary:
 - HEAD is 513a8c58, branch feature/f107-context-compiler-v2, EIGHT commits ahead
   of origin's d7dd12b6 — R13's, R14's and R15's state commits were never pushed.
   Your single push at C6 covers all of them.
 - R13, R14 and R15's committed state is gated PASS; C3 below records that gate.
   `.agent/live_review.md` header reads "Next free ID: R-0288" and carries
   `^Done:` 9x, `^Landed:` 0x, `^## Steps` 1x, `^<<<` 0x. 16 findings are OPEN.
 - `.agent/plan.md` and `.agent/handoff.md` BOTH still describe R12. That is
   R14's and R15's unfinished tail; your C5 and C6 replace them. Do not read
   either file as current state.
 - THE BASE WORKTREE IS GONE. `git worktree list` is the primary checkout alone
   and `git branch --list 'tmp/*'` is empty — R15's cleanup ran and succeeded.
   You BUILD a new one; there is no reuse path this round.
 - `.agent/gate_f107_r15/` EXISTS, UNTRACKED, and holds FIVE of the ten mandated
   evidence files from R15's dead session. It is NOT this round's evidence and no
   number in it may be reported as yours. Its superset — the raw logs, the exit
   codes, the drivers — survives at `.remedy-wt/gate-scratch/f107-r15/`, which is
   gitignored and which you leave untouched.
 - Loose files directly under `.remedy-wt/` (branch_run_full.txt, base_failed.txt,
   comm_*.txt, dist_hashes_raw.txt and the rest) belong to an EARLIER feature's
   gate. Not evidence, not to be copied, not to be quoted.

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase, revert, or delete
   any branch other than the throwaway `tmp/base-gate` this block manages.
 - NO PRODUCTION CODE, NO TEST CODE, NO DOCS MOVE THIS ROUND.
   `git diff --stat 513a8c58..HEAD -- packages apps tests docs` must be EMPTY at
   handback. This round measures; it does not repair.
 - DO NOT repair the five failing `[reviewer]` parametrizations in
   `tests/orchestration/test_role_conventions.py`. They fail at the merge base
   too, they are registered as R-0286, and repairing them here would mix an
   unrelated fix into a feature branch (AGENTS.md Core Workflow).
 - A red integration gate is NOT repaired here either. If a BRANCH-ONLY failure
   is reproducible and coupled to F107 code, STOP after C4, record it in the
   evidence, and hand back — that fix is its own reviewer-gated round
   (integration_gate.md step 4).
 - Do NOT create a PR, do NOT run the closure evidence job or the review zip, do
   NOT edit docs/roadmap/STATUS.md. Closure is the next round.
 - Do NOT write a `Done:` or `Landed:` line of your own anywhere. The `Done:`
   verb belongs to reviewer-authored text alone.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line, path or count that does not exist, STOP that item, do
   the safe thing, and DECLARE the correction in the handback. A declared
   deviation costs nothing; an undeclared one costs the round.

Detail for C3 — three pairs, applied to `.agent/live_review.md`, nothing else in
that file changes:
 - HDR16: REWRITE. FROM occurs exactly 1x before the edit; after it, FROM 0x and
   TO 1x, both counted LINE-ANCHORED on `^> Branch:.*Next free ID: R-0288` and
   `^> Branch:.*Next free ID: R-0289` so that the R-0288 finding's own text
   cannot pollute the count.
 - LRF16: APPEND — its TO literally CONTAINS its FROM, so no "FROM 0x" is
   attainable or ordered. Prove instead: FROM exactly 1x, and each TO-ONLY line
   exactly 1x AMONG THE LINES C3's DIFF ADDS.
 - LRG16: APPEND, same shape, same proof.
 - The three FROM texts each occur exactly 1x in the file at 513a8c58; the
   reviewer measured that before emitting. Apply them in one commit.

Detail for C4 — the gate. `docs/agents/integration_gate.md` governs and you read
it first; what follows pins this run's specifics and OVERRIDES nothing in it.
 - Scratch dir: `.remedy-wt/gate-scratch/f107-r16/`. Create it. EVERY log that
   grows while a suite runs is written THERE, outside the repo worktree, and only
   the finished trimmed evidence is copied in (R-0176: a log growing inside the
   repo changes the worktree digest mid-run and reddens the manifest-identity ids
   as false positives).
 - R-0288, this round's governing lesson: EVERY command whose output is evidence
   is redirected into its scratch file AS IT RUNS, with its exit code captured on
   the same line or the next. A value that exists only in your terminal is a
   value that does not exist. This applies to the worktree add, the copies, the
   touch, the hashes and the mtime listings — not only to the two pytest runs.
 - Evidence file names end in `.txt`, never `.log` (R-0169: `.gitignore` drops
   `*.log` silently and the review-zip guard rejects any `\.log$` member).
 - Your tooling may cap a single foreground command below a run's duration. The
   branch suite took 156 s and the base suite 124 s at R15. Give each run an
   explicit timeout well above that, or start it detached with its output
   redirected into the scratch dir and poll for the exit code. NEVER abandon a
   half-finished suite and NEVER report a partial log as a result. A run still
   going after 15 minutes is a problem to report, not to wait out.

 1. BRANCH RUN, from the repo root at the C3 head with a clean tree:
    `python3 -m pytest -n auto -q`. Record in `branch_run.txt`: cwd, the real
    `git rev-parse HEAD`, branch, the exact command, start/end UTC, the raw TAIL
    (last ~25 lines), `PYTEST_EXIT_CODE` and wall_clock_seconds. Then
    `grep '^FAILED' <log> | sort > .agent/gate_f107_r16/branch_failed.txt` — an
    empty file if there are none, created either way.
 2. BASE WORKTREE, built fresh:
    `git worktree add -b tmp/base-gate .remedy-wt/base-gate 2e4142c3`
    A THROWAWAY BRANCH, never detached: the self-dogfood branch guard refuses a
    detached HEAD by design (DECISION D3). Verify `rev-parse HEAD` ==
    2e4142c3ac72042ac4d704da252db263e48dcba3, `branch --show-current` ==
    tmp/base-gate, `status --porcelain` empty.
    Restore UI parity BY COPY, never by symlink — the auto-build runs npm install
    and writes THROUGH a symlink into the primary checkout (F053 R3 evidence):
    `cp -a apps/ui/node_modules .remedy-wt/base-gate/apps/ui/node_modules` and
    `cp -a apps/ui/dist .remedy-wt/base-gate/apps/ui/dist` (305M and 376K here).
    THEN the step R13's base run lacked, and the reason it was worthless: make
    every `apps/ui/dist` entry NEWER than the base worktree's sources —
    `find .remedy-wt/base-gate/apps/ui/dist -exec touch {} +`. `git worktree add`
    gives `apps/ui/src/**` fresh checkout mtimes newer than a copied
    `dist/index.html`, the staleness check fires, and `REMEDY_UI_NO_AUTO_BUILD=1`
    then refuses the rebuild it just asked for; seven `tests/ui_server/
    test_live_state.py` ids failed at base for that one mechanical reason.
    Touching dist restores the primary checkout's mtime ordering and changes no
    byte — the content hash is what proves it.
    Record `base_worktree.txt`: every command above with its REAL exit code, in
    order, written to the file as you go.
 3. PARITY PROOF into `dist_hashes.txt`, written as it is measured:
    the aggregate CONTENT hash `find apps/ui/dist -type f -print0 | sort -z |
    xargs -0 sha256sum | sha256sum`, for BOTH the base worktree and the primary
    checkout, BEFORE and AFTER the base run — four values — plus, for the base
    worktree before the run, the newest `apps/ui/src` mtime and the newest and
    oldest `apps/ui/dist` mtimes, proving the ordering. A changed PRIMARY hash
    means something wrote through: STOP and report it. A changed BASE hash voids
    the parity claim and forces per-id attribution instead.
 4. BASE RUN, from the base worktree root:
    `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q`
    Record `base_run.txt` and `base_failed.txt` exactly as step 1 did.
 5. COMPARE, into `comm_branch_only_failures.txt` (`comm -13 base_failed.txt
    branch_failed.txt`) and `comm_base_only_failures.txt` (`comm -23`). Both
    created even when empty.
 6. ATTRIBUTE, into `attribution.txt`, following the shape of the accepted
    `.agent/gate_f105_r49/attribution.txt` — read it; it is the precedent, not a
    template to copy blindly. It carries: the headline numbers for both runs with
    real exit codes and wall clock; the collected-test delta between branch and
    base with its cause; the two `comm` counts; and a PER-ID verdict table in
    which EVERY id from BOTH comm files appears exactly once, none silently
    absent. For every BRANCH-ONLY id: serial re-run of the exact node id —
    serial-pass means the xdist-flake class (record, not a blocker); serial-fail
    means reproduce it at the merge base before blaming F107. For every BASE-ONLY
    id: name the missing artifact or the mechanism per id by direct evidence, or
    it counts as a genuine base failure and blocks the verdict.
    ADD a COMMON FAILURES section: the ids failing in BOTH runs, with their
    count, named as R-0286 and explicitly NOT charged to F107. Say plainly there
    that they are why both runs exit 1. A common failure appears in NEITHER comm
    file and does not block the verdict.
    End the file with the line `VERDICT IS NOT ISSUED HERE` and the reason
    (integration_gate.md step 5: only the reviewer issues the gate verdict).
 7. CLEAN UP, into `worktree_cleanup.txt`: `git worktree remove --force
    .remedy-wt/base-gate`, `git worktree prune`, `git branch -D tmp/base-gate`,
    then `git worktree list` and `git branch --list 'tmp/*'` as proof, with the
    real exit codes. The primary checkout satisfies `git status --porcelain`
    empty afterwards.
 8. Keep each evidence file small: TAILS and lists, never a full 16k-test log. If
    any single evidence file would exceed 400 lines, trim it to the head and tail
    with an explicit `[... N lines elided ...]` marker.
 Evidence files, all directly under `.agent/gate_f107_r16/`, named exactly:
 branch_run.txt, branch_failed.txt, base_worktree.txt, dist_hashes.txt,
 base_run.txt, base_failed.txt, comm_branch_only_failures.txt,
 comm_base_only_failures.txt, attribution.txt, worktree_cleanup.txt. Every one is
 created even when its content is empty.
 BOTH runs are EXPECTED to exit 1 on the five common `[reviewer]` ids of R-0286.

Detail for C5 and C6:
 - Replace `.agent/plan.md` ENTIRELY with slice PLAN16 below; verify its sha256
   against the marker and `cmp` the file against the extracted slice.
 - Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries:
   feature and round; branch; the per-commit changed-files table for C1-C6; the
   verification table below with REAL exit codes and counted values; BOTH gate
   headline numbers with their wall clocks; the branch-only, base-only AND
   common-failure counts; the open-findings count with its IDs; and the next
   expected action (closure per docs/roadmap/STATUS_closure_protocol.md). Keep it
   under 100 lines; if the MANDATED content genuinely does not fit, exceed the
   cap and carry the DECISION D15 "Deviations, declared" line naming the real
   line count and the specific mandated content that caused it. Never drop a
   section to fit.

<<<BEGIN SLICE HDR16FROM sha256=e30850b93fa81a2759aa1571653d97ce569fc39d8852567c4fc0d0d09349b6d6 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0288.
<<<END SLICE HDR16FROM>>>

<<<BEGIN SLICE HDR16TO sha256=3f4ce8a2b70acd9c653effcdaee0454ee1905ccd449c112c3a5e333c06451f22 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0289.
<<<END SLICE HDR16TO>>>

<<<BEGIN SLICE LRF16FROM sha256=40626389e4f0e8c64cc8cc58cacf2e564dd9c1c17e35dd84cb4ab56f0d832aca lines=2>>>
  block. Recorded, not repaired here — editing an agent-governance document is
  outside this feature's change set. OPEN.
<<<END SLICE LRF16FROM>>>

<<<BEGIN SLICE LRF16TO sha256=c497c71212197d2efa8851d75f346b9f42d3cc73e5bc6599c709425cc0081692 lines=19>>>
  block. Recorded, not repaired here — editing an agent-governance document is
  outside this feature's change set. OPEN.
- R-0288 (Medium, F107 R15 integration gate): the R15 gate ran BOTH suites to
  completion in `.remedy-wt/gate-scratch/f107-r15/` and then lost its session
  before the evidence reached the repository. Its scalar outputs survived —
  exit codes, wall clocks, UTC stamps, the two full logs and the three comm
  lists — because the run drivers redirected them into files. The three parity
  steps did not survive: `mtimes.sh`, `touch_dist.sh` and `dist_hash.sh`
  printed to stdout only. Their output was the SOLE proof that the base
  worktree's `apps/ui/dist` was byte-identical to the primary checkout's and
  mtime-newer than its own sources, so `base_worktree.txt` and
  `dist_hashes.txt` became unrecoverable the moment the session died and the
  worktree was removed. A base run whose parity cannot be shown is not a
  comparison, and an empty `comm -23` proves parity only if you already trust
  the run that produced it. Rule, forward-looking: every gate step that
  produces evidence redirects it to its scratch file AS IT RUNS — a step whose
  only record is a terminal is a step that did not happen. R16 re-runs the
  whole gate from a rebuilt base worktree rather than transcribe a
  half-provable one. OPEN.
<<<END SLICE LRF16TO>>>

<<<BEGIN SLICE LRG16FROM sha256=458f7a6255c926650626c4243904ced93463883f957e111663ab8a29673be942 lines=2>>>
  the conflict it declared was the block's, not the worker's.
  `LAST_REVIEWED_SHA` advances 04154822 -> d7dd12b6.
<<<END SLICE LRG16FROM>>>

<<<BEGIN SLICE LRG16TO sha256=0896bccd01c1e3e49f39de51712fc611ef0315b76aa4eba93b9841850086abae lines=33>>>
  the conflict it declared was the block's, not the worker's.
  `LAST_REVIEWED_SHA` advances 04154822 -> d7dd12b6.
- Reviewer gate on R13, R14 and R15 (2026-08-12): PASS on all three, gated
  together by the reviewer of a NEW session because not one of them survived
  to write a handback. Range d7dd12b6..513a8c58 = eight commits over exactly
  four `.agent/` paths and nothing else: `git diff --stat 43e05108..HEAD --
  packages apps tests docs` is EMPTY and `git diff --name-only 43e05108..HEAD`
  returns `.agent/authored/f107-r15-1.md` and `.agent/last_block.md` alone.
  Transport by the PRIMARY shape, re-run here against the surviving
  `.remedy-wt/` originals rather than read from any summary:
  `.agent/authored/f107-r13-1.md` sha256 5fd436727e378348a182b30d459753cd… at
  280 lines, `f107-r14-1.md` cfb52b3917f3fed9639ceeb32b946373… at 278,
  `f107-r15-1.md` b1c8acaca006e1aa149814bdd12337cb… at 208 — each the value its
  own original's BLOCK_SHA256 trailer declares — and `cmp
  .agent/authored/f107-r15-1.md .agent/last_block.md` exits 0 and silent.
  `git show --numstat 43e05108 -- .agent/live_review.md` reads `29  1`, the
  single deletion being the header rewrite, and every anchored count holds on
  disk under this reviewer's own run: `^> Branch:.*Next free ID: R-0288` 1,
  `^- R-0286` 1, `^- R-0287` 1, `^Done:` 9, `^Landed:` 0, `^## Steps` 1,
  `^<<<` 0. Insertions per commit 280, 223, 56, 278, 156, 29, 208 and 147 —
  each under 500.
  WHAT DID NOT LAND, stated plainly because three rounds of state commits with
  no gate behind them is exactly what a false-progress record looks like: NO
  GATE EVIDENCE EXISTS. R13 and R14 died before their gate ran. R15's gate DID
  run — both suites, to completion — but died while copying its trimmed
  evidence into the repository, leaving five of the ten mandated files and no
  `attribution.txt`. Two of the missing five cannot be reconstructed at all
  (R-0288), so this reviewer treats R15's C3 as NOT DONE rather than as
  evidence to transcribe, and R16 re-runs the gate against a rebuilt base
  worktree. The surviving `.agent/gate_f107_r15/` is untracked partial output,
  never committed and now superseded; R16 moves it out of the repository
  rather than delete it, so the dead session's raw record stays readable.
  `LAST_REVIEWED_SHA` advances d7dd12b6 -> 513a8c58.
<<<END SLICE LRG16TO>>>

<<<BEGIN SLICE PLAN16 sha256=d14a4ec29602bd0a25bcc473ab2429b984fc426c16df81c783ee982d4f7b86a6 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0289. R13, R14 and R15 reviewed PASS at 513a8c58.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R16 — the integration gate per docs/agents/integration_gate.md, re-run whole
after R13, R14 and R15 each lost their session to it. Fresh full-suite runs on
the branch and at the merge base 2e4142c3, the base worktree REBUILT and its
UI parity proven to a file as it is established, every id in both comm files
attributed, the evidence committed under `.agent/gate_f107_r16/`. T001-T004 are
complete and reviewed; no production, test or docs file moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR. The five
   pre-existing `[reviewer]` failures (R-0286) are carried as a documented
   risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END SLICE PLAN16>>>

PROCEDURE — in this order, one commit per numbered step:
 0. BEFORE ANYTHING ELSE, and in NO commit: prove
    `.remedy-wt/gate-scratch/f107-r15/` exists and holds branch_full.txt and
    base_full.txt, then MOVE the in-repo partial out of the repository:
    `mv .agent/gate_f107_r15 .remedy-wt/gate-scratch/f107-r15-partial-in-repo`
    Record both commands with their real exit codes in the handback. Do not
    delete anything. `git status --porcelain` is 0 lines afterwards — confirm it
    before you touch a tracked file.
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r16-1.md`. The expected
    digest is the BLOCK_SHA256 line the reviewer original
    `.remedy-wt/f107-r16-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two — exit 0 and
    silent. Commit C2.
 3. Apply the three C3 pairs to `.agent/live_review.md`. Commit C3. This is the
    head the branch run measures.
 4. Run the gate exactly as Detail-C4 prescribes, then commit the evidence dir as
    C4. Nothing outside `.agent/gate_f107_r16/` changes in this commit.
 5. Replace `.agent/plan.md` entirely with slice PLAN16. Commit C5.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C6. Push the branch.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r16-1.md .agent/last_block.md` -> exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Every slice body recomputes to its BEGIN-marker digest at its declared line
    count. Report SLICES=<n> MISMATCH=0.
 c. C3's pair proofs: `git show --numstat <C3> -- .agent/live_review.md` for the
    totals; `grep -c '^> Branch:.*Next free ID: R-0288'` -> 0 and
    `grep -c '^> Branch:.*Next free ID: R-0289'` -> 1 on the file; each LRF16 and
    LRG16 TO-ONLY line exactly 1x among that commit's ADDED lines. Also on the
    file afterwards: `^- R-0288` 1, `^Done:` 9, `^Landed:` 0, `^## Steps` 1,
    `^<<<` 0 — and `^<<<` 0 in `.agent/plan.md` and `.agent/handoff.md` too.
 d. THE GATE ITSELF. Report, as raw values, for BOTH runs: the exact command, the
    passed/skipped/failed counts, the pytest exit code, the wall clock and the
    HEAD sha the run measured. Report the two comm counts and the common-failure
    count. Report, per branch-only id, its serial re-run result. Report the four
    dist content hashes and the three mtimes of step 3. The gate is GREEN for the
    reviewer only if the PRIMARY dist hash is unchanged across the base run, the
    BASE dist hash is unchanged across it, every branch-only id is either absent
    or attributed to the xdist-flake class by a serial pass, every base-only id
    is attributed to the environment class by named direct evidence, and every
    common failure is one of R-0286's five `[reviewer]` ids.
 e. `sha256sum .agent/plan.md` == the PLAN16 marker digest; `cmp` against the
    extracted slice -> exit 0, silent; the file is 29 lines.
 f. Canary, in the primary checkout after the base worktree is gone:
    `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
 g. `git diff --stat 513a8c58..HEAD -- packages apps tests docs` -> EMPTY output.
 h. `git diff --name-only 513a8c58..HEAD` -> exactly the paths of the Change list
    and nothing else. The fifth tracked path, `.agent/handoff.md`, arrives with
    C6, so a measurement taken before C6 legitimately shows four plus the gate
    dir — say which you measured.
 i. `git status --porcelain` -> 0 lines; `git worktree list` -> the primary
    checkout ALONE; `git branch --list 'tmp/*'` -> empty; HEAD ==
    origin/feature/f107-context-compiler-v2 after the push; insertions per
    commit, each < 500 (the gate dir included — trim evidence if it would not
    fit, per Detail-C4 step 8).
 j. `remedy integrity check --json` -> record the verdict verbatim. It is a
    closure precondition (STATUS_closure_protocol.md precondition 3) and the next
    round needs the value; a non-PASS is REPORTED, not repaired here. If the
    command is unavailable or refused in your environment, record the exact error
    text instead — an absent value is a finding, a reported failure is not.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering step 0 and C1-C6, and every gate above with its real exit code and
counted value. Declare any deviation.
──────────────────────────────────────────────────────────────
