# Handoff — F110 Model routing by task class, round 15

## Session

SESSION 5 of feature F110 · round 15 · rounds so far 15

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed at the C4 SHA
  below, NO pull request open (`gh pr list --state open` answered `[]`).
- Base of this round: `970ffc27` (F110 R14 C5). HEAD before the handback:
  `f14b0d34` (C3).
- Merge base (`git merge-base main HEAD`, unchanged by this round):
  `6f2230cea29af36a75fea253afc10f4dfe5a79f0`.
- Fortschritt: THE INTEGRATION GATE THIS FEATURE OWES BEFORE CLOSURE WAS RUN.
  `docs/agents/integration_gate.md` steps 1-5 ran against the branch (C2's
  tree — C0a-C2 touch only `.agent/`, so the code under test is the code at
  `970ffc27`) and against the merge base in a throwaway worktree, with the
  three OPEN findings the block named applied to the procedure:
  - **R-0591** — every `shutil.copytree` of `apps/ui/node_modules` and
    `apps/ui/dist` into the base worktree passed `symlinks=True` explicitly.
    `apps/ui/node_modules` copied 44839 entries, 27 of them symlinks (23 the
    `node_modules/.bin` npm shims), all 27 PRESERVED. `apps/ui/dist` copied 5
    entries, 0 symlinks.
  - **R-0736** — after copying, every file under the base worktree's
    `apps/ui/dist` had its mtime ADVANCED (to `1788447634.57`) past that
    worktree's own checkout stamp (max `apps/ui/src` mtime in that tree:
    `1788447609.02`). `_frontend_is_stale()`, evaluated by loading
    `packages/orchestration/ui_server.py` from INSIDE the base worktree, read
    **False** before the base run started.
  - **R-0590** — both comparison sets were attributed unconditionally. The
    branch-only set (`comm -13`) is empty, so nothing to attribute there. The
    base-only set (`comm -23`) holds 2 ids; both were serially re-run at the
    base worktree (xdist disabled) and both PASS (`2 passed in 0.60s`),
    classifying them as the XDIST-FLAKE class (F135/F052) — a hard-coded
    0.5s perf ceiling blown by 16-way parallel contention, and an unscoped
    `pgrep` orphan-process check that can match a sibling xdist worker's own
    subprocess. A grep for `model_routing|role_config|task_class` over both
    test files returns no match: neither reaches F110 code. See
    `.agent/gate_f110_r15/attribution.txt`.
  - **Branch run**: `19487 passed, 23 skipped, 0 failed`, exit 0, 158.29s
    (reported) / 158.71s (measured).
  - **Base run**: `2 failed, 18935 passed, 20 skipped`, exit 1
    (`ExitCode.TESTS_FAILED`), 243.46s (reported) / 243.93s (measured). Both
    failures attributed to the XDIST-FLAKE class above, neither coupled to
    F110 code.
  - **branch_only.txt**: 0 lines. **fixed_by_branch.txt**: 2 lines (the two
    attributed base-only ids). **NO BLOCKER**: the branch-only set — the only
    set that can produce one per `integration_gate.md` step 4 — is empty.
  - Parity verified as an EVENT (R-0444): every `apps/ui/dist` mtime in the
    base worktree is identical before and after the run and falls OUTSIDE the
    run's wall-clock window (`1788447658.92`..`1788447902.85`); accompanying
    content digest identical before/after. PARITY HOLDS.
  - Evidence landed under `.agent/gate_f110_r15/`: `gate_summary.txt`,
    `branch_run_tail.txt`, `branch_failed.txt`, `base_run_tail.txt`,
    `base_failed.txt`, `branch_only.txt`, `fixed_by_branch.txt`,
    `parity_mtime.txt`, `attribution.txt` — the same 9-file set
    `.agent/gate_f109_r17/` established, none named `.log`.
  - Round 14's PASS verdict, the resolution of `R-0789` and one prose slip
    (about the round 14 block sending the worker into the reviewer's own
    scratch directory without a reserved namespace) were booked in C2, per
    operator amendment amend0827-process-diet rule 1.
  - THIS ROUND CHANGED NO CODE. `git diff --stat 970ffc27..f14b0d34 --
    packages/ apps/ tests/ docs/` is EMPTY — the change set's "measures, does
    not change" clause, measured at G8.
- A stall was reported mid-round from outside this session, claiming the base
  worktree pytest run had hung (identical xdist worker CPU times sampled a
  few minutes apart). Investigated directly rather than accepted: at the time
  of the report the run had ALREADY completed — `base_meta.txt` and
  `base_run_full.txt` both carried a fresh mtime written before the report
  arrived, the meta file's own `start_epoch`/`end_epoch` pair matched pytest's
  self-reported wall clock exactly, the log tail showed an ordinary clean
  completion with full tracebacks (something a hung process cannot produce),
  and a live `ps aux` check at investigation time found no `run_base.py`, no
  pytest, no xdist worker process anywhere on the box. The sampled PIDs were
  almost certainly this same run's workers observed near its natural end,
  when most had gone idle waiting on the last stragglers — indistinguishable
  from a hang only if sampled without checking the run's own completion
  artifacts. No corrective action was taken because none was needed; this is
  recorded here as a DEVIATION-free false alarm rather than silently dropped.
- `.agent/STOP` read from disk TWICE, as constraint 2 orders: before the
  first commit (C0a) and again before this handback (C4). ABSENT both times.
- `.agent/decisions.md`, `.agent/candidates.md` and
  `docs/roadmap/features/T3_F110.md` were NOT touched, per constraint 10.
  `.agent/candidates.md` is still EMPTY.

## Range

Base `970ffc27` → head `f14b0d34` for every gate below; C4 is this handback
and its own numbers belong to the next ledger entry (§3 item 14).

## Commits

| # | SHA | Subject | Files | +/- |
|---|-----|---------|-------|-----|
| C0a | `298a1580` | F110 R15 C0a: save round 15 block verbatim | `.agent/authored/f110-r15.md` | +307 / -0 |
| C0b | `42976190` | F110 R15 C0b: mirror the committed authored file to last_block.md | `.agent/last_block.md` | +234 / -326 |
| C1 | `fb111342` | F110 R15 C1: apply PLAN15 to plan.md | `.agent/plan.md` | +17 / -18 |
| C2 | `8a45ea10` | F110 R15 C2: append RECORD15 to live_review.md and SLIPS15 to prose_slips.md | `.agent/live_review.md` (+5/-1), `.agent/prose_slips.md` (+3/-1) | +8 / -2 |
| C3 | `f14b0d34` | F110 R15 C3: integration gate evidence under .agent/gate_f110_r15/ | 9 files under `.agent/gate_f110_r15/` (see below) | +321 / -0 |
| C4 | (this commit) | F110 R15 C4: the round 15 handback | `.agent/handoff.md` | — |

C3 file-by-file (`git diff --numstat f14b0d34^..f14b0d34`):
`attribution.txt` +67/-0, `base_failed.txt` +2/-0, `base_run_tail.txt`
+60/-0, `branch_failed.txt` +0/-0, `branch_only.txt` +0/-0,
`branch_run_tail.txt` +60/-0, `fixed_by_branch.txt` +2/-0, `gate_summary.txt`
+99/-0, `parity_mtime.txt` +31/-0.

Per-commit insertions, the `+` column only (DECISION F104 D1), cell by cell
against the table above: C0a 307, C0b 234, C1 17, C2 8, C3 321. Every one is
under 500. C0b is additionally a verbatim full-file rewrite of a single
`.agent/**` state file and exempt under DECISION F104 D1; it does not need
the exemption, being 234.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | block saved verbatim by `shutil.copyfile`; digest unchanged across scratch original, saved copy and mirror |
| C0b | done | mirrored from the COMMITTED authored file by `shutil.copyfile` |
| C1 | done | PLAN15 extracted by delimiter index, plus the target's one trailing newline |
| C2 | done | RECORD15 and SLIPS15 appended, each as `\n\n` + slice, target's no-trailing-newline convention preserved |
| C3 | done | 9-file evidence set committed under `.agent/gate_f110_r15/`, matching the F109 R17 file set |
| C4 | done | this handback |
| R-0591 | applied | `symlinks=True` explicit on both `copytree` calls; 27/27 node_modules symlinks preserved, 0/0 dist symlinks (none to preserve) |
| R-0736 | applied | base-worktree `apps/ui/dist` mtimes advanced past the worktree's own checkout stamp; `_frontend_is_stale()` read False from inside that tree before the run |
| R-0590 | applied | both `branch_only.txt` (empty) and `fixed_by_branch.txt` (2 ids) attributed by direct evidence; see `attribution.txt` |
| G1 TRANSPORT | pass | exit 0; single digest across scratch original, authored copy, mirror |
| G2 THE PLAN | pass | exit 0 on extraction+newline `cmp`; bare extraction differs as expected |
| G3 THE RECORD APPENDS | pass | byte arithmetic, prefix, second-reader and negative-control checks all pass on both files |
| G4 THE BRANCH RUN | pass | 19487 passed, 23 skipped, 0 failed, exit 0 |
| G5 THE BASE RUN | pass (parity) | parity restored and verified as an event; run itself surfaced 2 base-only failures, both attributed below |
| G6 COMPARISON + ATTRIBUTION | pass, no blocker | branch_only empty; fixed_by_branch's 2 ids both attributed to XDIST-FLAKE, neither coupled to F110 code |
| G7 EVIDENCE DIRECTORY | pass | 9 files committed, 0 named `.log` |
| G8 TREE/COMMITS/SWEEP | pass | tree clean, worktree/branch cleaned up, code-path diff empty, all insertions under 500 |

## External actions

- NO pull request created. NOTHING merged. NO force-push. No work on `main`.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  answered `[]`.
- One disposable worktree created and destroyed: `.remedy-wt/base-gate` on
  throwaway branch `tmp/base-gate`, at merge base
  `6f2230cea29af36a75fea253afc10f4dfe5a79f0`. Removed by its EXACT path with
  `git worktree remove` plus `git worktree prune`; `tmp/base-gate` branch
  deleted with `git branch -D`; `ls -d .remedy-wt/base-gate` afterwards
  reports no such file; `git ls-files .remedy-wt` is EMPTY.
- The five `.remedy-wt/job-*` worktrees in `git worktree list` are
  PRE-EXISTING and none is of this round's making.
- No `remedy.toml` sits in the repository root.

## Verification

One line per gate, with its real exit code, captured through
`bash -c '<cmd>; echo "REAL_EXIT=$?"'` where a shell exit code applies, and
via the Python return value otherwise (the sandbox denies shell `VAR=x cmd`,
`env`, `export ...;` and `cp`, so pytest ran as a library call and copies ran
through `shutil`).

- **G1 TRANSPORT — exit 0.** `filecmp.cmp` (shallow=False) between
  `remedy-review-r9-scratch/f110-r15.md` and `.agent/authored/f110-r15.md` →
  `True` (REAL_EXIT=0 equivalent). ONE sha256 digest,
  `754dbb5c2d40cd2577ee1e85722e55fe5851f4251093d7023c191f8f046dbd3e`, repeated
  identically for the scratch original, `.agent/authored/f110-r15.md` and
  `.agent/last_block.md`. `wc -l .agent/authored/f110-r15.md` = 307. This
  claims nothing about any other bytes.
- **G2 THE PLAN — exit 0.** PLAN15 extracted from the COMMITTED authored
  file by `list.index` on its `<<<BEGIN PLAN15>>>` / `<<<END PLAN15>>>`
  marker lines (41 lines, 1916 bytes). The extraction PLUS ONE TRAILING
  NEWLINE byte-equals `.agent/plan.md` → True (exit 0 equivalent); the bare
  extraction does NOT equal `.agent/plan.md` → False, exactly the one byte
  the target's convention adds. `wc -l .agent/plan.md` = 41 (under 50).
  `grep -c '^## Goal'` = 1. `grep -c '^## Next Steps'` = 1.
- **G3 THE RECORD APPENDS — exit 0 on every check.**
  `.agent/live_review.md`: base 2222266 bytes at `970ffc27`, ending WITHOUT a
  newline; RECORD15 is 3 lines / 6735 bytes; arithmetic
  `2222266 + 2 + 6735 = 2229003` against a real size of 2229003; the pre-C2
  content is an exact byte PREFIX (True); the file still ends without a
  newline (True). SECOND READER over the WHOLE appended region: the script
  COUNTED N = 2 paragraphs in the slice (the `Gate: F110 R14 —...` paragraph
  and the `Done: R-0789 —...` paragraph) and compared the LAST 2 blank-line
  units of the whole file against them IN ORDER — match True. NEGATIVE
  CONTROL on the FIRST appended paragraph: byte 0 flipped in a COPY, the
  second reader REJECTED it (match False); the real file was never written.
  HEADER SHAPE (§3 item 26): lines starting with the slice's own
  `Gate: F110 R14 — the round 14 entry.` prefix — BEFORE C2 = 0, AFTER C2 = 1.
  `.agent/prose_slips.md`: base 64121 bytes, no trailing newline; SLIPS15 is
  1 line / 926 bytes; `64121 + 2 + 926 = 65049` against a real 65049; prefix
  True; still no trailing newline; second reader N = 1, match True; negative
  control REJECTED.
  THE OPEN SET, recomputed mechanically from the file and never carried
  forward: 350 paragraphs matching `^- R-\d+ — ` over 350 UNIQUE registered
  ids; 74 lines matching `^Done: R-\d+ — ` over 72 UNIQUE resolved ids — the
  two-line gap is the known `R-0721` / `R-0725` double-`Done:` pair; open set
  = 350 − 72 = **278**. `R-0767` in the open set: True. `R-0789` in the open
  set: False (RECORD15 carries the `Done:` paragraph that resolves it, so
  this reading proves the resolution landed rather than merely having been
  written).
- **G4 STEP 1, THE BRANCH RUN — exit 0.** WARM-BUILD precondition asserted
  FIRST: `apps/ui/dist/index.html` exists, mtime `1788057215.85`, exceeding
  the newest `apps/ui/src` file's mtime `1788057023.74` (True — warm, no cold
  build owed). `pytest.main(["-n", "auto", "-q"])` from the repository root,
  NO environment variable set: `19487 passed, 23 skipped` in `158.29s
  (0:02:38)`, exit `ExitCode.OK` (0), 158.71s measured around the call.
  `branch_failed.txt` (sorted `^FAILED` lines): 0 lines. Written to
  `branch_run_tail.txt` and `branch_failed.txt`, both copied into
  `.agent/gate_f110_r15/` after the run exited.
- **G5 STEP 2, THE BASE RUN — exit 1 (`ExitCode.TESTS_FAILED`), parity
  holds.** Worktree created exactly as specified:
  `git worktree add -b tmp/base-gate .remedy-wt/base-gate
  6f2230cea29af36a75fea253afc10f4dfe5a79f0`. Parity restored BEFORE the run:
  `apps/ui/node_modules` copytree(symlinks=True) — 44839 entries, 27 symlinks
  preserved; `apps/ui/dist` copytree(symlinks=True) — 5 entries, 0 symlinks;
  dist mtimes advanced to `1788447634.57`, past the worktree's checkout stamp
  `1788447609.02`; `_frontend_is_stale()` evaluated from inside the base
  worktree read **False** before the run. `REMEDY_UI_NO_AUTO_BUILD` set
  in-process, then `pytest.main(["-n", "auto", "-q"])` from
  `.remedy-wt/base-gate`: `2 failed, 18935 passed, 20 skipped` in `243.46s
  (0:04:03)`, exit `ExitCode.TESTS_FAILED` (1), 243.93s measured around the
  call. `base_failed.txt`: 2 lines (`test_review_bundle_runtime.py::...
  test_timeout_raises_with_cleanup`,
  `test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget`).
  PARITY AS AN EVENT: every `apps/ui/dist` file's mtime is IDENTICAL before
  and after the run and OUTSIDE the run window `1788447658.92`..
  `1788447902.85`; accompanying sha256 content digest identical before/after
  (`ef09e3072d59b1d6fa7ea7ea0bd13aabaafb52674b9dbad58a8e2a615236f445`).
  PARITY HOLDS. Written to `parity_mtime.txt`.
- **G6 STEPS 3 AND 4, COMPARISON AND ATTRIBUTION — no blocker.**
  `comm`-equivalent set arithmetic: `branch_only.txt` (in branch, not base) =
  0 lines; `fixed_by_branch.txt` (in base, not branch) = 2 lines — the same 2
  ids `base_failed.txt` lists, since `branch_failed.txt` is empty. Both sets
  ATTRIBUTED UNCONDITIONALLY per R-0590: `branch_only.txt` is empty, nothing
  to attribute, no blocker possible from that set (the only set
  `integration_gate.md` step 4 can turn into one). `fixed_by_branch.txt`'s 2
  ids: both SERIALLY RE-RUN at the base worktree (`-p no:xdist`) → `2 passed
  in 0.60s`, classifying both XDIST-FLAKE (F135/F052) — a fixed 0.5s perf
  ceiling under 16-way parallel contention, and an unscoped `pgrep -f
  apps.cli.grouped.*--help` matching a sibling worker's own subprocess.
  `grep -n 'model_routing|role_config|task_class'` over both test files:
  exit 1 (no match) — neither reaches F110 code. Written to
  `attribution.txt`.
- **G7 THE EVIDENCE DIRECTORY — exit 0.** `.agent/gate_f110_r15/` created
  and committed with exactly 9 files, matching `.agent/gate_f109_r17/`'s set:
  `gate_summary.txt`, `branch_run_tail.txt`, `branch_failed.txt`,
  `base_run_tail.txt`, `base_failed.txt`, `branch_only.txt`,
  `fixed_by_branch.txt`, `parity_mtime.txt`, `attribution.txt`. `ls -la` and
  `git ls-files .agent/gate_f110_r15` both list the same 9 names. Count of
  committed members ending `.log`: 0.
- **G8 THE TREE, THE COMMITS AND THE SWEEP — exit 0 on every check.**
  `git status --porcelain` immediately before C4 was staged: EMPTY.
  `git worktree list`: no worktree of this round's making survives (the five
  `.remedy-wt/job-*` entries are pre-existing). `git branch --list 'tmp/*'`:
  EMPTY. `ls -d .remedy-wt/base-gate`: no such file. `git ls-files
  .remedy-wt`: EMPTY. `ls remedy.toml`: no such file.
  `git diff --stat 970ffc27..f14b0d34 -- packages/ apps/ tests/ docs/`:
  EMPTY. PER-COMMIT INSERTIONS, `+` column only, C0a through C3, cell by
  cell against the `## Commits` table above: 307, 234, 17, 8, 321 — each
  confirmed under 500. C4's own numbers are not this gate's business (§3
  item 14 routes them to the next ledger entry).

## Deviations & assumptions

- NO deviation from the block's change set. Every path written is one of the
  seven the change set names, and nothing outside them was touched — G8's
  empty sweep over `packages/`, `apps/`, `tests/` and `docs/` is that claim
  measured.
- NO slice was edited, retyped or re-wrapped. No conflict between a slice
  and the repository was found, so constraint 1's declaration route was not
  needed.
- A stall report arrived mid-round from outside this session, claiming the
  base-worktree pytest run had hung. It was investigated and found to be a
  false alarm — the run had already completed cleanly by the time the report
  was made, evidenced by fresh completion-artifact timestamps, a matching
  wall-clock reading between the meta file and pytest's own self-report, a
  log tail showing an ordinary finish with full tracebacks, and a live
  process check finding nothing still running. No process was killed, no run
  was repeated, and no gate was weakened; this is recorded per constraint 1's
  spirit (declare rather than silently resolve) even though it was not a
  slice conflict.
- `ruff` was NOT run, per constraint 5; this round writes no code and the
  change set names no `.py` file.
- The two base-only failures are recorded as MEASURED results, not
  suppressed or waived: both are on the ledger in `attribution.txt` and
  `gate_summary.txt` with their classification and direct evidence, exactly
  as R-0590 asks, even though neither blocks the gate.

## Next

Open findings: **278** (350 unique registered − 72 unique resolved).
`R-0767` is in that set; `R-0789` is now OUT of it, resolved by RECORD15's
`Done:` paragraph. `.agent/candidates.md` is EMPTY.

Next expected action, in this order:
1. Phase 1 rule 1 — read `.agent/STOP` from disk. It was absent at both
   readings this round.
2. Phase 1 rule 2 — the Open PR Gate. `gh pr list --state open` answered
   `[]` this round; no PR was created.
3. Review round 15 over `970ffc27..HEAD` and issue the gate verdict — GREEN
   or a blocker — which the next round's first commit books. As measured
   here: the branch run is clean (0 failed) and the only red ids are 2
   base-only failures both attributed to the XDIST-FLAKE class with no
   coupling to F110 code, so no blocker was found by this round's own
   measurement. The verdict itself belongs to the reviewer.
4. Then the CLOSURE SEQUENCE, which takes two rounds, runs the one §3
   checklist consolidation pass DECISION F110 D1 carries into it, needs an
   evidence job and a FRESH review zip, and updates the Design and
   Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.
5. Then the STATUS line and the closure pull request, which the operator
   merges at the next feature's Open PR Gate.

SESSION 5 is at ONE delegated round so far; F110 stands at 15 rounds against
the 25-round soft limit, so the limit is NOT reached and no scope report is
owed.
