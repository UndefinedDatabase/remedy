── STEP integration gate (completion, 2nd attempt) / F107 R15 ──
Goal:        Run the F107 integration gate to completion — fresh full-suite runs
             on this branch and at the merge base 2e4142c3, the base worktree's
             UI mtime parity actually neutralized, every branch-only and
             base-only id attributed by direct evidence, the whole run committed
             as evidence under `.agent/gate_f107_r15/`. R14 landed its three
             state commits and then lost its session before the gate ran; the
             gate is the ONLY thing R14 left unfinished.
Bundle:      C1 save this block · C2 mirror it · C3 the gate runs + their
             evidence dir · C4 plan · C5 handoff.
Change:      exactly these FIVE paths, nothing else:
             .agent/authored/f107-r15-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/gate_f107_r15/** (new dir, C3)
             .agent/plan.md (C4, full replacement by slice PLAN15)
             .agent/handoff.md (C5)
             `.agent/live_review.md` IS NOT IN THE CHANGE SET AND IS NOT TOUCHED
             THIS ROUND. R-0286 and R-0287 already landed at 43e05108 and the
             reviewer verified them before writing this block. Register, edit or
             resolve no finding anywhere.

State you are resuming, verified by the reviewer against the files themselves,
not quoted from a summary:
 - HEAD is 43e05108, branch feature/f107-context-compiler-v2, tree clean, SIX
   commits ahead of origin's d7dd12b6 — R13's and R14's state commits were never
   pushed. Your single push at C5 covers all of them.
 - R14's C1/C2/C3 are gated PASS. `.agent/authored/f107-r14-1.md` and
   `.agent/last_block.md` both sha256 to
   cfb52b3917f3fed9639ceeb32b946373baec1ff68671b2860fe532b326bec2ec at 278 lines
   — the value the reviewer original's trailer declares. C3's numstat on
   `.agent/live_review.md` is `29 1`. That file's header reads "Next free ID:
   R-0288" and it carries `^- R-0286` 1x, `^- R-0287` 1x, `^Done:` 9x,
   `^Landed:` 0x, `^## Steps` 1x, `^<<<` 0x.
 - `.agent/plan.md` still describes R12: that is R14's unfinished C5 and your C4
   replaces it. `.agent/handoff.md` still describes R12 for the same reason and
   your C5 rewrites it. Neither file is stale by accident — do not treat their
   contents as current state.
 - The base worktree R13 left behind is INTACT and REUSABLE as far as the
   reviewer could see read-only: `git -C .remedy-wt/base-gate rev-parse HEAD` ==
   2e4142c3ac72042ac4d704da252db263e48dcba3, `branch --show-current` ==
   tmp/base-gate, `status --porcelain` 0 lines, and both `apps/ui/dist` and
   `apps/ui/node_modules` exist inside it. Verify all of that yourself anyway,
   and take the rebuild path if any check fails.
 - `.agent/gate_f107_r14/` DOES NOT EXIST — no gate evidence was ever written by
   R13 or R14. Loose files under `.remedy-wt/` (branch_run_full.txt,
   base_failed.txt, comm_*.txt, dist_hashes_raw.txt and the rest) belong to an
   EARLIER feature's gate. They are NOT this feature's evidence, they are NOT to
   be copied into the repo, and no number in them may be reported as this
   round's. Every value you record comes from a run you performed.

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase, revert, or delete
   any branch other than the throwaway `tmp/base-gate` this block manages.
 - NO PRODUCTION CODE, NO TEST CODE, NO DOCS MOVE THIS ROUND.
   `git diff --stat 43e05108..HEAD -- packages apps tests docs` must be EMPTY at
   handback. This round measures; it does not repair.
 - DO NOT repair the five failing `[reviewer]` parametrizations in
   `tests/orchestration/test_role_conventions.py`. They fail at the merge base
   too, they are registered as R-0286, and repairing them here would mix an
   unrelated fix into a feature branch (AGENTS.md Core Workflow).
 - A red integration gate is NOT repaired here either. If a BRANCH-ONLY failure
   is reproducible and coupled to F107 code, STOP after C3, record it in the
   evidence, and hand back — that fix is its own reviewer-gated round
   (integration_gate.md step 4).
 - Do NOT create a PR, do NOT run the closure evidence job or the review zip, do
   NOT edit docs/roadmap/STATUS.md. Closure is the next round.
 - Do NOT write a `Done:` or `Landed:` line of your own anywhere.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line, path or count that does not exist, STOP that item, do
   the safe thing, and DECLARE the correction in the handback. A declared
   deviation costs nothing; an undeclared one costs the round.

Detail for C3 — the gate. Read TWO files before you start; both govern:
 (1) `docs/agents/integration_gate.md` — the canonical procedure.
 (2) `.agent/authored/f107-r14-1.md`, its "Detail for C4" section at lines
     52-127 — the run-specific procedure, already reviewer-checked and still
     correct. Read it from that committed path (it landed at 60187d87), NOT from
     `.agent/last_block.md`, which your own C2 overwrites.
 THREE OVERRIDES apply to that section. Nothing else about it changes:
 (i)   the evidence dir is `.agent/gate_f107_r15/`, not `.agent/gate_f107_r14/`,
       everywhere it appears — evidence belongs to the round that produced it.
 (ii)  the scratch dir is `.remedy-wt/gate-scratch/f107-r15/`, not the r13 or r14
       path. Create it. Every log that GROWS while a suite runs is written there,
       outside the repo worktree, and only the finished trimmed evidence is
       copied in (R-0176).
 (iii) it says the branch run happens "at the C3 head"; in THIS round the branch
       run happens at the C2 head, because this round has no live_review commit
       and its numbering shifts by one. The requirement is unchanged: a clean
       tree, and the real `git rev-parse HEAD` recorded in `branch_run.txt`.
 Evidence files, all directly under `.agent/gate_f107_r15/`, named exactly:
 branch_run.txt, branch_failed.txt, base_worktree.txt, dist_hashes.txt,
 base_run.txt, base_failed.txt, comm_branch_only_failures.txt,
 comm_base_only_failures.txt, attribution.txt, worktree_cleanup.txt. Every one
 is created even when its content is empty. `.txt` only, never `.log` (R-0169).
 Runtime expectation, from the accepted F105 R49 precedent (read
 `.agent/gate_f105_r49/attribution.txt` and `.agent/gate_f105_r49/dist_hashes.txt`
 — that gate is the shape to follow, not a file to copy): branch ~99 s and base
 ~144 s wall clock with `-n auto`. A run still going after 15 minutes is a
 problem to report, not to wait out. If your tooling caps a single foreground
 command below the run's duration, start the run detached with its output
 redirected into the scratch dir and poll for the exit code — never abandon a
 half-finished suite and never report a partial log as a result.
 BOTH runs are EXPECTED to exit 1 on the five common `[reviewer]` ids of R-0286.
 A common failure appears in NEITHER comm file and does NOT block the verdict;
 attribution.txt must say so in its own COMMON FAILURES section and name R-0286.

Detail for C4 and C5:
 - Replace `.agent/plan.md` ENTIRELY with slice PLAN15 below; verify its sha256
   against the marker and `cmp` the file against the extracted slice.
 - Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries:
   feature and round; branch; the per-commit changed-files table for C1-C5; the
   verification table below with REAL exit codes and counted values; BOTH gate
   headline numbers with their wall clocks; the branch-only, base-only AND
   common-failure counts; the open-findings count with its IDs; and the next
   expected action (closure per docs/roadmap/STATUS_closure_protocol.md). Keep
   it under 100 lines; if the MANDATED content genuinely does not fit, exceed
   the cap and carry the DECISION D15 "Deviations, declared" line naming the
   real line count and the specific mandated content that caused it. Never drop
   a section to fit.

<<<BEGIN SLICE PLAN15 sha256=c1c7b811aa40ec94e35a186761e2ba85fb71a0f0a686ce3b5f8a48f34bf00ae8 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0288. R14's state commits reviewed PASS at 43e05108.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R15 — the integration gate per docs/agents/integration_gate.md, completing what
R13 and R14 both began and lost to dead sessions: fresh full-suite runs on the
branch and at the merge base 2e4142c3 with the base worktree's UI mtime parity
actually neutralized, every id in both comm files attributed, the evidence
committed under `.agent/gate_f107_r15/`. T001-T004 are complete and reviewed;
no production, test or docs file moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR. The five
   pre-existing `[reviewer]` failures (R-0286) are carried as a documented
   risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END SLICE PLAN15>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r15-1.md`. The expected
    digest is the BLOCK_SHA256 line the reviewer original
    `.remedy-wt/f107-r15-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two — exit 0 and
    silent. Commit C2. This is the head the branch run measures.
 3. Run the gate exactly as Detail-C3 prescribes, then commit the evidence dir
    as C3. Nothing outside `.agent/gate_f107_r15/` changes in this commit.
 4. Replace `.agent/plan.md` entirely with slice PLAN15. Commit C4.
 5. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C5. Push the branch.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r15-1.md .agent/last_block.md` -> exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. The PLAN15 slice body recomputes to its BEGIN-marker digest at its declared
    line count of 29.
 c. THE GATE ITSELF. Report, as raw values, for BOTH runs: the exact command,
    the passed/skipped/failed counts, the pytest exit code, the wall clock and
    the HEAD sha the run measured. Report the two comm counts and the
    common-failure count. Report, per branch-only id, its serial re-run result.
    The gate is GREEN for the reviewer only if every branch-only id is either
    absent or attributed to the xdist-flake class by a serial pass, AND every
    base-only id is attributed to the environment class by named direct
    evidence, AND every common failure is one of R-0286's five `[reviewer]` ids.
 d. `sha256sum .agent/plan.md` == the PLAN15 marker digest; `cmp` against the
    extracted slice -> exit 0, silent; the file is 29 lines.
 e. Canary, in the primary checkout after the base worktree is gone:
    `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
 f. `git diff --stat 43e05108..HEAD -- packages apps tests docs` -> EMPTY output.
 g. `git diff --name-only 43e05108..HEAD` -> exactly the paths of the Change
    list and nothing else; `.agent/live_review.md` does NOT appear in it. The
    fifth path, `.agent/handoff.md`, arrives with C5, so a measurement taken
    before C5 legitimately shows four plus the gate dir — say which you measured.
 h. `git status --porcelain` -> 0 lines; `git worktree list` -> the primary
    checkout ALONE; `git branch --list 'tmp/*'` -> empty; HEAD ==
    origin/feature/f107-context-compiler-v2 after the push; insertions per
    commit, each < 500 (the gate dir included — trim evidence if it would not
    fit, per Detail-C3).
 i. `remedy integrity check --json` -> record the verdict verbatim. It is a
    closure precondition (STATUS_closure_protocol.md precondition 3) and the
    next round needs the value; a non-PASS is REPORTED, not repaired here. If
    the command is unavailable or refused in your environment, record the exact
    error text instead — an absent value is a finding, a reported failure is not.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C5, and every gate above with its real exit code and counted
value. Declare any deviation.
──────────────────────────────────────────────────────────────
