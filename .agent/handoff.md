# Handback — F022 Live cost ticker · Runde 15 (das Integration Gate)

Fortschritt: ~95 % (T001 fertig · T002 fertig · T003 fertig — diese Runde baut
             nichts, sie MISST: das Integration Gate ueber die ganze Suite, plus
             das R14-Urteil auf Platte) — Schaetzung

Branch `feature/f022-live-cost-ticker`. Round base `8d5c73c4`.
Deviations, declared: this handback is 147 lines, over the 60-line cap the
block sets, under DECISION D15 — the cause is the mandated per-commit tables for
6 commits, the 15 one-line gate rows, the 6-row item-status table and the
ordered-sequence deviations §4 requires in prose.

## Range

Review of `8d5c73c4`..`HEAD` (C4 below).

## Commits

### 94873415 chore(state): save the F022 R15 step block as authored text (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r15.md | +296/-0 | the block file copied byte-for-byte |

### bee7ca97 chore(state): mirror the F022 R15 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +195/-292 | same bytes, from the C0a blob; full-file rewrite |

### a97dfac3 docs(state): point the F022 plan at R15, the integration gate (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15/-16 | PLANF022R15 replaces the file whole |

### 0486eddf docs(state): record the F022 R14 verdict and the R-0672 recurrence (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | LEDGER15 appended, two paragraphs |

### 36a43e04 test(gate): record the F022 R15 integration gate evidence (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f022_r15/ | +474/-0 | 11 files: attribution.txt 176, base_failed.txt 63, controls.txt 46, base_run.txt 39, summary.txt 37, auto_build_neutralization.txt 32, branch_run.txt 31, comm.txt 21, parity.txt 19, canary.txt 10, branch_failed.txt 0 |

### C4 docs(state): hand back the F022 R15 integration gate round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file; a handoff cannot table its own commit |

## External actions

`git worktree add -b tmp/f022-r15-base .remedy-wt/f022r15-base c34ef32b` → ok, ON
A BRANCH per constraint 5. `git worktree add -b tmp/f022-r15-ctl
.remedy-wt/f022r15-ctl HEAD` → ok, for the G5 and G12 controls. `git worktree
remove --force` on both → ok; `git worktree prune`; `git branch -D
tmp/f022-r15-base tmp/f022-r15-ctl` → both deleted; `git worktree list` back to 1
line. `gh pr list --state open --json number,headRefName` → `[]`. `git push` →
after C4. No PR created, nothing merged.

## Verification

One line per gate; the transcripts stay in `.agent/gate_f022_r15/` (R-0582).

- G1 exit 0 — `.agent/STOP` absent, read from disk before C0a and again before C4; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3.
- G2 exit 0 — five readings EQUAL: sha256 `639788e02382…6ad8`, 29128 bytes, 296 lines, over the scratch `.remedy-wt/f022-r15.md`, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk, and the delegation's digest; C0a and C0b resolve to the SAME git blob `3f1d412d`.
- G3 exit 0 — the extractor over the COMMITTED C0a blob, matching the line-anchored `<<<SLICE ` / `<<<END ` markers, found 2 of each and printed 2 slices over 47 CONTENT lines (PLANF022R15 44, LEDGER15 3); TOTAL 296, PROSE 249 — constraint 10's 296/47/249 reproduce exactly, nothing to reconcile.
- G4 exit 0 — `.agent/plan.md` at `a97dfac3` is 2508 bytes = PLANF022R15's 2507 + exactly one newline; NEGATIVE CONTROL against the BARE slice is FALSE; `^## Goal$` 1x and `^## Next Steps$` 1x in that file; `wc -l` 44 ≤ 50.
- G5 exit 0, control rejected — reader (a): the C1 blob of `.agent/live_review.md` is a byte-exact PREFIX and the remainder is 9861 = 1 + LEDGER15's 9859 + 1. Reader (b), an independent blank-line splitter: N = 2 paragraphs, 276 → 278 units, the LAST 2 equal the slice's 2 IN ORDER. NEGATIVE CONTROL in `.remedy-wt/f022r15-ctl`: BYTE offset 574400, inside the FIRST appended paragraph's byte span [574174, 578439), flipped 116 → 84 (`2 R14, in the review` → `2 R14, in The review`) — BOTH readers REJECT the mutant while BOTH ACCEPT the true file.
- G6 exit 0 — in `.agent/live_review.md`, base `8d5c73c4` → C2 `0486eddf`: `^- R-\d+ — ` 234 → 234, all DISTINCT at both, MAXIMUM `R-0673` at both; ids ADDED and ids REMOVED are both the EMPTY SET, so NO ID WAS MINTED; `^Done: R-` 2 → 2 over `R-0653` and `R-0670`; `^Landed: ` 0 → 0; `^Recurrence: R-` 8 → 9 over 8 DISTINCT ids at both, the ninth line being a SECOND `R-0672`; `^Gate: R` 14 → 15 over 14 → 15 distinct keys, gaining exactly `R14`; `^- R-0672 — ` exactly 1 at both. Every base reference numeral the block states reproduced.
- G7 exit 0 — the BRANCH RUN, `python3 -m pytest -n auto -q` from the repository root in the PRIMARY checkout at C2: `17722 passed, 20 skipped in 177.04s`, wall 177.6 s, and 0 lines matching `^FAILED` in `branch_failed.txt`.
- G8 exit 1 — the BASE RUN, identical command, in the branch worktree `tmp/f022-r15-base` at `c34ef32b` with `REMEDY_UI_NO_AUTO_BUILD=1` and parity restored FIRST by `shutil.copytree(src, dst, symlinks=True)`: `63 failed, 17588 passed, 20 skipped in 162.61s`, wall 163.1 s, 63 lines matching `^FAILED` in `base_failed.txt`. RED CONTROL for the restore: symlinks under `apps/ui/node_modules/.bin` counted 0 in the base worktree before the copy (the directory was absent) and 23 after, equal to the primary's 23.
- G9 exit 0, PARITY CLAIM VOID — all 3 files under the base worktree's `apps/ui/dist` carry an mtime INSIDE the run window 1787467222.256 .. 1787467385.399; both asset FILENAMES changed (`index-CQ9qmyYl.css`/`index-DKdEM9lB.js` → `index-DCl1uvTK.css`/`index-DNUAMteT.js`) and no sha256 matched its pre-run value, so this is a real REBUILD FROM BASE SOURCES about 100 s in, not a byte-identical one. Per-id attribution of every `comm -23` id was therefore mandatory and was performed.
- G10 exit 0 twice — `comm -13 base_failed.txt branch_failed.txt`, the BRANCH-ONLY set, count 0 and the list EMPTY; `comm -23`, the BASE-ONLY set, count 63 and the list identical to `base_failed.txt`. An independent python set difference over the same two files agrees in BOTH directions.
- G11 — THE BRANCH-ONLY SET IS EMPTY, reported as the reading it is and not as a discharge: 0 ids, so no serial re-run, no flake to classify and NO BLOCKER under constraint 4. All 63 base-only ids are attributed to ONE environment class by three evidences: `_frontend_is_stale()` returns True in the base worktree at the copied `dist/index.html` mtime (92 of 92 `apps/ui/src` files newer) and False at the post-run mtime; 63 of 63 failure sections carry BOTH `Failed: Server did not start in time` and `ERROR: React UI not built.`; and all 63 ids, re-run SERIALLY at `c34ef32b` once the artifact was fresh, gave exit 0 and `63 passed in 8.02s`.
- G12 exit 0 — the CANARY, `python3 -m pytest tests/cli/test_golden_path.py -q` in the PRIMARY checkout at C2: `42 passed in 20.43s`, matching the block's reference figure of 42. RED CONTROL in `.remedy-wt/f022r15-ctl`: line 71's `assert "State: planned" in out` was mutated to a non-existent state → exit 1, `1 failed, 41 passed in 20.55s`, the `^FAILED` line naming `TestDoMission::test_do_mission_creates_planned_job`.
- G13 exit 0 — the 5 commits BEFORE C4, every one single-parent; insertions 296, 195, 15, 4 and 474, each under the 500 cap; the range `8d5c73c4..HEAD` touches 15 paths, range−ChangeSet is EMPTY and ChangeSet−range is exactly `.agent/handoff.md` (C4's own, still pending); `git show --numstat` agrees cell by cell with every `## Commits` row above; the LINE-ANCHORED `^<<<SLICE ` and `^<<<END ` each count 0 in `.agent/plan.md` and 0 in `.agent/live_review.md`; `git ls-files .remedy-wt` 0; `git worktree list` 1 line with `tmp/f022-r15-base` and `tmp/f022-r15-ctl` both deleted; the round's 5 reflog rows all carry the action `commit` — amend 0, rebase 0, cherry 0.
- G14 exit 0 — `gh pr list --state open --json number,headRefName` printed, verbatim, `[]`. No PR created and nothing merged; the closure protocol creates the PR at R16.
- G15 — CHECKED, NO RESIDUAL. Re-measured at C3: `git merge-base` IS `c34ef32b` and that commit's subject names pull request #211; the ceiling `R-0673` still holds in `.agent/live_review.md`; R-0672, R-0625, R-0431, R-0413, R-0533, R-0364, R-0622, R-0665, R-0495 and R-0574 are each exactly one `^- R-\d+ — ` record there; `^- R-0526 — ` and `^- R-0530 — ` are each 0; `^Recurrence: R-0672 ` is 2; R-0672's body still carries the sentence LEDGER15 quotes; D8's paragraph in `.agent/decisions.md` still says "its three cases" and still closes with the universal LEDGER15 calls false; the diff `c2e78b32..318a85a1` still adds 4 lines matching `^\+\s*it\(` to `apps/ui/src/api/remedyApi.test.ts`; R14's transport values (sha256 `1c827a3f…b5b5`, 30949 bytes, 393 lines, blob `ac070803`), its plan's 2608 bytes and its remainders 5004 and 4512 all reproduce; the 61 shipped non-test `.ts`/`.tsx` files under `apps/ui/src` still put the four figure fields in exactly `costMetric.ts` with comments stripped, with `costReconciliation.ts` naming one raw; and `git ls-files` matches 0 paths containing `assumption`, so R-0665's premise holds. NOT RE-MEASURED: PLANF022R15's `npm run lint` sentence — that same file states it is NOT a gate (R-0622).

## Authored-text proofs

Two slices were extracted PROGRAMMATICALLY by their marker LINES out of the
COMMITTED C0a blob and applied byte for byte, never retyped and never reflowed:
PLANF022R15 2507 B and LEDGER15 9859 B. The disk-to-disk equality is G2, G4
(with the bare-slice control FALSE) and G5 (two independent readers plus a
byte-flip control). The 11 files under `.agent/gate_f022_r15/` are NOT slices:
they are my own measurements, generated from the JSON the runs produced, exactly
as the block's "What C3 writes" section requires.

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: none. C0a, C0b, C1, C2, C3 and C4 landed exactly as
  constraint 3 fixes them — no extra commit, none dropped, no reordering.
- A SECOND DISPOSABLE WORKTREE. Constraint 5 names `tmp/f022-r15-base` only; G5
  and G12 each order a control "in a disposable worktree" without naming one, so
  `tmp/f022-r15-ctl` was created at `0486eddf` to host both. Both worktrees were
  removed and both branches deleted (G13).
- GATE ORDER. G7-G12 PRODUCE the files C3 commits, so their RUNS necessarily
  precede C3; G1-G6 and G13-G15 ran after C3 and before C4 as the block directs.
- CONSTRAINT 6 ORDERED THE COPY ROUTE, AND THE COPY ROUTE IS WHAT PRODUCED ALL
  63 BASE-ONLY FAILURES. It was applied as written per constraint 1.
  `shutil.copytree` copies with `copy2`, which PRESERVES the source mtime, so the
  copied `apps/ui/dist/index.html` (mtime 1787467082) landed OLDER than every one
  of the base worktree's 92 freshly checked-out `apps/ui/src` files (newest
  1787467200); `_frontend_is_stale()` fired, and `REMEDY_UI_NO_AUTO_BUILD=1`
  turned the auto-build into `sys.exit(1)` before the UI server could bind.
  `.agent/gate_f021_r38/parity.txt` records that same copy route producing 78
  base-only failures at `24a6b899` and the BUILD route producing 0. Not repaired:
  constraint 4 forbids it, and G10's attribution obligation was discharged instead.
- G9's REBUILD IS THE R-0169/R-0444 CLASS RECURRING — `REMEDY_UI_NO_AUTO_BUILD=1`
  was set and the base `dist` was rebuilt anyway, so the variable did not reach
  the path that built it. Reported, not minted: an id is the reviewer's to mint.
- TWO CONTROLS BEYOND THE ORDERED SET, because both headline readings this round
  are EMPTY: a `^FAILED` extractor liveness control (a synthetic one-pass
  one-fail module run OUTSIDE the repository, exit 1, extractor found 1 line) and
  a `comm` route control (a synthetic pair putting exactly 1 id in each
  direction). Both are recorded in `controls.txt`.
- TWO OF MY OWN FIRST G15 READINGS WERE WRONG-SET READINGS, NOT STALENESS, and
  are named so nobody re-derives them: "61 shipped `.ts`/`.tsx` files" counts the
  NON-TEST set (81 with tests, 61 without), and D8's closing universal is present
  but WRAPS a line, so a single-line grep misses it. Both LEDGER15 sentences
  re-measure TRUE.
- The canary ran twice, both exit 0 and both `42 passed`; the second run exists
  only because the first did not capture its own metadata. Nothing else ran twice,
  and no two pytest processes were ever alive at once.
- No measurement of mine differed from a reference numeral the block states for
  the round base `8d5c73c4`, so nothing needed reconciling under constraint 9.
- WALL CLOCK: branch 177.6 s and base 163.1 s, both under the ~5 min threshold of
  docs/agents/integration_gate.md step 5, so no perf-pass note is raised.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 the R14 verdict and two recurrences | done | |
| C3 the gate evidence | done | 11 files under `.agent/gate_f022_r15/` |
| C4 the handback | done | this commit |

## Next

1. Phase 1 rule 1 FIRST: re-read `.agent/STOP` from disk before anything else.
2. Gate R15 — this round is ungated and its verdict is the next round's C1.
3. R16, closure, per docs/roadmap/STATUS_closure_protocol.md. G11 found NO
   blocker: the branch-only set is empty, so no repair round stands between here
   and closure.
