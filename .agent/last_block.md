── STEP R16 tail completion / F107 R17 ──
Goal:        Land the tail R16 never reached — the reviewer's R16 PASS gate and
             the F107 integration-gate verdict, finding R-0289, `.agent/plan.md`
             and `.agent/handoff.md` — and get twelve unpushed commits onto
             origin. R16 ran the integration gate to completion and the reviewer
             has gated it GREEN; what is missing is the record of it and a push.
Bundle:      C1 save this block · C2 mirror it · C3 the reviewer's four pairs ·
             C4 plan · C5 handoff. PUSH AFTER EVERY COMMIT.
Change:      exactly these FIVE tracked paths, nothing else:
             .agent/authored/f107-r17-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs below and NOTHING else)
             .agent/plan.md (C4, full replacement by slice PLAN17)
             .agent/handoff.md (C5)
             No new directory, no evidence dir, no untracked file left behind.

State you are resuming, verified by the reviewer against the files themselves,
not quoted from any summary:
 - HEAD is 5c808a59, branch feature/f107-context-compiler-v2, TWELVE commits
   ahead of origin's d7dd12b6. R13, R14, R15 and R16 all committed and not one
   of them pushed. Your first push covers all twelve.
 - R16's C1-C4 landed and are gated PASS; C3 below is that gate's record. R16's
   own C5 and C6 never landed — the session died after C4.
 - `.agent/plan.md` and `.agent/handoff.md` BOTH still describe R12. That is
   R16's unfinished tail; your C4 and C5 replace them. Do not read either file
   as current state, and do not carry any number out of them.
 - THE INTEGRATION GATE IS DONE AND GREEN. Its ten evidence files are committed
   under `.agent/gate_f107_r16/` and the reviewer re-derived the decisive
   numbers from the raw scratch logs. DO NOT RUN THE FULL SUITE THIS ROUND.
 - `.agent/live_review.md` header reads "Next free ID: R-0289" and carries
   `^Done:` 9x, `^Landed:` 0x, `^## Steps` 1x, `^<<<` 0x. 26 findings are
   registered, 9 are resolved, 17 are OPEN.
 - `git status --porcelain` is 0 lines, `git worktree list` is the primary
   checkout alone and `git branch --list 'tmp/*'` is empty. Keep all three true.

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, clean tree at handback. Never work on main, never
   force-push, never amend, rebase, revert or delete any branch.
 - PUSH AFTER EVERY COMMIT: `git push -u origin feature/f107-context-compiler-v2`
   after C1, after C2, after C3, after C4 and after C5 — not once at the end.
   That is R-0289, the finding this round registers, and the round that
   registers a finding does not repeat it.
 - NO PRODUCTION CODE, NO TEST CODE, NO DOCS, NO ROADMAP FILE MOVES.
   `git diff --stat 5c808a59..HEAD -- packages apps tests docs` must be EMPTY at
   handback. This round records; it does not build and it does not repair.
 - Do NOT re-run the integration gate, do NOT build a base worktree, do NOT
   create a PR, do NOT run the closure evidence job or the review zip, do NOT
   edit docs/roadmap/STATUS.md. Closure is the next round.
 - Do NOT repair the five failing `[reviewer]` parametrizations in
   `tests/orchestration/test_role_conventions.py`. They fail at the merge base
   too, they are registered as R-0286, and repairing them here would mix an
   unrelated fix into a feature branch (AGENTS.md Core Workflow).
 - Do NOT write a `Done:` or `Landed:` line of your own anywhere. The `Done:`
   line inside slice DONE17TO is reviewer-authored: apply it, never compose one.
 - Verify every claim against the file before you write it. If anything below
   names a path, line, symbol or count that does not exist, STOP that item, do
   the safe thing, and DECLARE the correction in the handback. A declared
   deviation costs nothing; an undeclared one costs the round.

Detail for C3 — FOUR pairs, applied to `.agent/live_review.md` in this order,
and nothing else in that file changes:
 - HDR17: REWRITE. Its FROM occurs exactly 1x before the edit; after it, counted
   LINE-ANCHORED, `^> Branch:.*Next free ID: R-0289` is 0 and
   `^> Branch:.*Next free ID: R-0290` is 1 — anchored so that the R-0289
   finding's own body cannot pollute either count.
 - LRF17: APPEND — its TO literally CONTAINS its FROM, so no "FROM 0x" is
   attainable or ordered. Prove instead: FROM exactly 1x, and each TO-ONLY line
   exactly 1x AMONG THE LINES C3's DIFF ADDS.
 - LRG17: APPEND, same shape, same proof.
 - DONE17: APPEND, same shape, same proof. It lands at the end of the file.
 - The four FROM texts each occur exactly 1x in the file at 5c808a59; the
   reviewer measured that before emitting this block.

Detail for C4 and C5:
 - Replace `.agent/plan.md` ENTIRELY with slice PLAN17; verify its sha256
   against the slice's BEGIN marker and `cmp` the file against the extracted
   slice.
 - Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries:
   feature and round; branch; the per-commit changed-files table for C1-C5;
   every gate in Done-when with its REAL exit code and counted value; the
   integration gate's two headline numbers as recorded by R16 (quoted as R16's,
   since you did not run them); the open-findings count with its IDs; the
   item-status table for C1-C5; and the next expected action (closure per
   docs/roadmap/STATUS_closure_protocol.md). Keep it under 100 lines; if the
   MANDATED content genuinely does not fit, exceed the cap and carry the
   DECISION D15 "Deviations, declared" line naming the real line count and the
   specific mandated content that caused it. Never drop a section to fit.

<<<BEGIN SLICE HDR17FROM sha256=3f4ce8a2b70acd9c653effcdaee0454ee1905ccd449c112c3a5e333c06451f22 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0289.
<<<END SLICE HDR17FROM>>>

<<<BEGIN SLICE HDR17TO sha256=729ad0119977a97e681843e348e554c72f834a81c7446312d3a96fbd8f6f5950 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0290.
<<<END SLICE HDR17TO>>>

<<<BEGIN SLICE LRF17FROM sha256=933ee9218bb67aeea2b702169867eeb6ae96d31e46fb79eec922341536aae529 lines=2>>>
  whole gate from a rebuilt base worktree rather than transcribe a
  half-provable one. OPEN.
<<<END SLICE LRF17FROM>>>

<<<BEGIN SLICE LRF17TO sha256=b7fe6cfaa97301f3f858867e1e613bd5f34b69d3b14558715a7ab33f3b322f3d lines=16>>>
  whole gate from a rebuilt base worktree rather than transcribe a
  half-provable one. OPEN.
- R-0289 (Medium, F107 R16): the R16 block ordered its ONLY push at C6, the
  last commit of the round. The session died after C4, so twelve commits — the
  entire committed output of R13, R14, R15 and R16, the complete
  integration-gate evidence included — sat on local disk alone, invisible to
  the operator and one disk failure from gone. AGENTS.md Push Discipline reads
  "After committing: git push -u origin <branch>", not "after the last commit
  of the round". Four consecutive sessions have now died mid-round, which makes
  the tail of a round the least likely part to run and therefore the worst
  possible home for the only durability step a round has. The R16 block was
  otherwise careful — it redirected every gate value to a file precisely
  because a session might die — and then staked the survival of all of it on
  reaching its own last step. Rule, forward-looking: a round pushes after EVERY
  commit; a block that names a single push at its last step is authoring the
  loss it will later have to report. OPEN.
<<<END SLICE LRF17TO>>>

<<<BEGIN SLICE LRG17FROM sha256=4a660c3fb71ac060a1133eea6253ae3cf38564b23ac1d73070ff3117ab533b07 lines=2>>>
  rather than delete it, so the dead session's raw record stays readable.
  `LAST_REVIEWED_SHA` advances d7dd12b6 -> 513a8c58.
<<<END SLICE LRG17FROM>>>

<<<BEGIN SLICE LRG17TO sha256=6782ed9e82e97251d8abce7e16babe2476f33d7e3c6606e21453c9998b1f842b lines=42>>>
  rather than delete it, so the dead session's raw record stays readable.
  `LAST_REVIEWED_SHA` advances d7dd12b6 -> 513a8c58.
- Reviewer gate on R16 (2026-08-12): PASS, and the F107 INTEGRATION GATE IS
  GREEN. Range 513a8c58..5c808a59 = four commits over thirteen paths, every one
  under `.agent/`: `git diff --stat 513a8c58..5c808a59 -- packages apps tests
  docs` is EMPTY. Transport re-run here rather than quoted:
  `.agent/authored/f107-r16-1.md` and `.agent/last_block.md` both sha256
  39e6cb447d679ff3777e162f9832c489a49e72a5ab02aa60b7fde14db9650963 at 369
  lines — the value the surviving original `.remedy-wt/f107-r16-1.block.md`
  declares on the trailer one line past its saved region — and `cmp` between
  them exits 0 and silent. All seven slice bodies recompute to their
  BEGIN-marker digests at their declared line counts: SLICES=7 MISMATCH=0. C3
  is byte-exact, checked by extracting both sides from the diff and comparing
  the lists: its 49 added lines equal HDR16TO plus the TO-only tails of LRF16
  and LRG16 exactly, and its single deleted line is HDR16FROM.
  THE GATE ITSELF. Branch run at d94b0c97, `python3 -m pytest -n auto -q` ->
  exit 1, 5 failed / 16533 passed / 19 skipped, 221 s. Base run at the merge
  base 2e4142c3 in a rebuilt `tmp/base-gate` worktree,
  `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` -> exit 1, 5 failed
  / 16457 passed / 19 skipped, 155 s. This reviewer recomputed the decisive
  comparison from the RAW scratch logs instead of the trimmed evidence:
  `grep -c '^FAILED'` is 5 in both `.remedy-wt/gate-scratch/f107-r16/
  branch_full.txt` and `base_full.txt`, the two committed FAILED lists are
  byte-identical (md5 cbf4dd9c85afafaf20aba2e38f940cee each), and therefore
  branch-only 0, base-only 0, common 5. The five common ids are R-0286's
  `[reviewer]` parametrizations, failing at a merge base where no F107 commit
  exists — not charged to F107, and the reason both runs exit 1. UI parity
  holds: four identical `apps/ui/dist` aggregate content hashes
  fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 (base and
  primary, before and after) with dist mtimes newer than src, so the seven-id
  `tests/ui_server/test_live_state.py` environment class of R-0221 does not
  appear in this gate at all. The collected-test delta 16557 - 16481 = 76
  equals the 76 tests `--collect-only` counts across the three test files F107
  adds, so it is F107's own coverage and not a selection difference. Wall clock
  221 s and 155 s, both inside the ~5 min budget, so no perf pass is indicated.
  Per docs/agents/integration_gate.md step 5 the verdict is the reviewer's and
  it is PASS, the five R-0286 ids carried as a documented risk.
  WHAT DID NOT LAND: C5 (`.agent/plan.md`) and C6 (`.agent/handoff.md` and the
  push). The session died after C4. Both files still describe R12 and the
  branch stood twelve commits ahead of origin at review time — registered here
  as R-0289. R17 lands that tail and nothing else.
  `LAST_REVIEWED_SHA` advances 513a8c58 -> 5c808a59.
<<<END SLICE LRG17TO>>>

<<<BEGIN SLICE DONE17FROM sha256=463f6ba886cb1e27f5d16ba127b65561e2798a2e702667d84e80794228976307 lines=2>>>
fails on `assert 265 == 899`. A bypass can no longer satisfy the feature's Done
sentence. Open findings 14 -> 13.
<<<END SLICE DONE17FROM>>>

<<<BEGIN SLICE DONE17TO sha256=3c5370e2c8f342a0a099e090b86c540bdc518e0b6c4d810480ebfe54e370990e lines=19>>>
fails on `assert 265 == 899`. A bypass can no longer satisfy the feature's Done
sentence. Open findings 14 -> 13.

Done: R-0288 — RESOLVED. The parity proof R15 could not show exists on disk for
R16, and this reviewer read the files rather than the summary that describes
them. `.agent/gate_f107_r16/base_worktree.txt` records the `git worktree add -b
tmp/base-gate`, both `cp -a` copies, the `find ... -exec touch {} +` and the
three identity checks, each with its real exit code; `dist_hashes.txt` carries
the four aggregate `apps/ui/dist` content hashes — base before, base after,
primary before, primary after, all
fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 — plus the
newest-src, newest-dist and oldest-dist mtimes that prove the ordering the R13
base run lacked. Ten of the ten mandated evidence files are committed, where
R15 left five and no `attribution.txt`. The forward-looking rule the finding
states held in practice: every number in those ten files also exists in the
gitignored raw record at `.remedy-wt/gate-scratch/f107-r16/`, which is why this
reviewer could re-derive the gate's decisive comparison from `branch_full.txt`
and `base_full.txt` directly instead of trusting the trimmed copies. Open
findings 18 -> 17.
<<<END SLICE DONE17TO>>>

<<<BEGIN SLICE PLAN17 sha256=d40eabc5d461b094b53b462c9b0dc9215f92e36072124dadd26d5a8608ae9f29 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0290. R16 reviewed PASS at 5c808a59.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R17 — land the tail R16 never reached: the reviewer's R16 PASS gate and the
F107 integration-gate verdict, finding R-0289, this plan and the handoff, and
push the branch. T001-T004 are complete and reviewed. The integration gate ran
at R16 and is GREEN — branch and base fail the same five R-0286 ids, zero
branch-only, zero base-only — with its evidence committed under
`.agent/gate_f107_r16/`. No production, test, docs or roadmap file moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR. The five
   pre-existing `[reviewer]` failures (R-0286) are carried as a documented
   risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END SLICE PLAN17>>>

PROCEDURE — in this order, one commit per numbered step, push after each:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r17-1.md`. The expected
    digest is the BLOCK_SHA256 line the reviewer original
    `.remedy-wt/f107-r17-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1, push.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two — exit 0 and
    silent. Commit C2, push.
 3. Apply the four C3 pairs to `.agent/live_review.md`. Commit C3, push.
 4. Replace `.agent/plan.md` entirely with slice PLAN17. Commit C4, push.
 5. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C5. Push.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r17-1.md .agent/last_block.md` -> exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Every slice body recomputes to its BEGIN-marker digest at its declared line
    count. Report SLICES=<n> MISMATCH=0.
 c. C3's pair proofs: `git show --numstat <C3> -- .agent/live_review.md` for the
    totals; on the file afterwards
    `grep -c '^> Branch:.*Next free ID: R-0289'` -> 0,
    `grep -c '^> Branch:.*Next free ID: R-0290'` -> 1, `^- R-0289` -> 1,
    `^Done:` -> 10, `^Landed:` -> 0, `^## Steps` -> 1, `^<<<` -> 0 — and
    `^<<<` -> 0 in `.agent/plan.md` and `.agent/handoff.md` too. Plus: each
    TO-ONLY line of LRF17, LRG17 and DONE17 exactly 1x among C3's ADDED lines.
 d. `sha256sum .agent/plan.md` == the PLAN17 marker digest; `cmp` against the
    extracted slice -> exit 0, silent; the file is 29 lines.
 e. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0,
    42 passed. This is the ONLY suite this round runs.
 f. `git diff --stat 5c808a59..HEAD -- packages apps tests docs` -> EMPTY.
 g. `git diff --name-only 5c808a59..HEAD` -> exactly the paths of the Change
    list and nothing else. The fifth path, `.agent/handoff.md`, arrives with C5,
    so a measurement taken before C5 legitimately shows four — say which you
    measured.
 h. `git status --porcelain` -> 0 lines; `git worktree list` -> the primary
    checkout ALONE; `git branch --list 'tmp/*'` -> empty; HEAD ==
    origin/feature/f107-context-compiler-v2 after the final push, and
    `git rev-list --left-right --count origin/feature/f107-context-compiler-v2...HEAD`
    -> `0	0`; insertions per commit, each < 500.
 i. `remedy integrity check --json` -> record the verdict verbatim. It is a
    closure precondition (STATUS_closure_protocol.md precondition 3) and the
    next round needs the value; a non-PASS is REPORTED, not repaired here. This
    reviewer's own attempt in this environment was REFUSED by the tool sandbox
    with the exact text `This command requires approval` and no verdict was
    produced. If yours is refused the same way, record that text verbatim as the
    gate's result and move on — do NOT route around the refusal, do NOT retry it
    under another shell, and do NOT report an absent value as a PASS.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C5, and every gate above with its real exit code and counted
value. Declare any deviation.
──────────────────────────────────────────────────────────────
