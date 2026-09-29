# Handback — F042 round 3: book F042 R2, record D3, mount the seam

## Session

SESSION 1 of feature F042 · round 3 · rounds so far 3. Context self-assessment: after writing this
handoff and before pushing, roughly one-fifth of the session's context budget remained.

## Range

Review of `fc744e0e0`..`<this C6 commit>`. C1a (`7b43522bf`), C1b (`6b5c0e996`), C1c (`f388d7605`),
C2 (`c7efe533d`), C3 (`01158bb9e`), C4 (`be2bfc24f`) and C5 (`ea05e500e`) are all content commits;
C6 (this handoff commit) is written and pushed last, per the write-once rule.

## Commits

### 7b43522bf F042 R3 C1a: copy round 3 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r3-block.md | +317/-0 | copy of this round's block, byte for byte |
| .agent/authored/f042-r3-plan.md | +28/-0 | copy of the plan.md payload, byte for byte |

Expected by the block: 317 + 28 = 345; measured: 345. Match. Under the 500-line stop threshold.

### 6b5c0e996 F042 R3 C1b: copy round 3 records and tests diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r3-records.diff | +68/-0 | copy of the records.diff payload, byte for byte |
| .agent/authored/f042-r3-tests.diff | +134/-0 | copy of the tests.diff payload, byte for byte |

Expected by the block: 202; measured: 202 (68+134). Match.

### f388d7605 F042 R3 C1c: copy the round 3 render harness into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r3-render_drive.mjs | +176/-0 | copy of render_drive.mjs, byte for byte |
| .agent/authored/f042-r3-render_index.html | +11/-0 | copy of render_index.html, byte for byte |
| .agent/authored/f042-r3-render_main.tsx | +61/-0 | copy of render_main.tsx, byte for byte |
| .agent/authored/f042-r3-render_measure.py | +187/-0 | copy of render_measure.py, byte for byte |
| .agent/authored/f042-r3-render_vite.config.mjs | +28/-0 | copy of render_vite.config.mjs, byte for byte |

Expected by the block: 463; measured: 463 (176+11+61+187+28). Match.

### c7efe533d F042 R3 C2: book F042 R2, record D3 and its assumption line, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +41/-0 | `git apply` of records.diff: DECISION F042 D3 appended |
| .agent/live_review.md | +2/-0 | `git apply` of records.diff: F042 R2 gate entry appended |
| docs/ui/design_reference/assumption_log.md | +1/-0 | `git apply` of records.diff: the F042 kicker/empty-face assumption line |
| .agent/plan.md | +8/-9 | rewritten to the plan.md payload (`shutil.copyfile`) |

Expected by the block: 41/0 decisions.md, 2/0 live_review.md, 1/0 assumption_log.md, 8/9 plan.md;
measured: identical. Match. `.agent/plan.md` verified byte-identical to the plan.md payload (sha256
`68325b9727ea9db1c5d7d3658aea96a4e61c87b3f6afdc27ee333602b40256fa`, both sides) before staging.

### 01158bb9e F042 R3 C3: mount one project context, key the shell by project and job, switch in the rail
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/RemedyApp.tsx | +83/-14 | S5: address state, `openAddress`, `onSwitched`/`pushState`, `popstate` listener, faces, one `ProjectProvider` |
| apps/ui/src/api/cockpitAddress.ts | +43/-0 | NEW, S1: `CockpitAddress`, `CockpitFace`, `addressFromSearch`, `cockpitFaceOf`, `shellKeyOf` |
| apps/ui/src/components/rail/LeftBrandRail.tsx | +2/-1 | S4: one import line, kicker line replaced with `<ProjectSwitcher fallback={...} />` |
| apps/ui/src/components/shell/ProjectProvider.tsx | +79/-0 | NEW, S2: the one context, two keyed loads, one switch gate, memoised value |
| apps/ui/src/components/shell/ProjectSwitcher.module.css | +31/-0 | NEW, S3: kicker/select styling, `--remedy-*` tokens only |
| apps/ui/src/components/shell/ProjectSwitcher.tsx | +42/-0 | NEW, S3: `PROJECT_SWITCHER_LABEL`, `MISSING_FOLDER_MARK`, `NO_ACTIVE_PROJECT_OPTION`, `ProjectSwitcher` |

Expected by the block (informational, the reviewer's own version of S1-S5): 64/13 RemedyApp.tsx,
45/0 cockpitAddress.ts, 2/1 LeftBrandRail.tsx, 66/0 ProjectProvider.tsx, 30/0
ProjectSwitcher.module.css, 44/0 ProjectSwitcher.tsx — an independent writing of the same clauses;
LeftBrandRail.tsx matches exactly, the other five are close but not identical (see Deviations).
Total this commit: 280 insertions, 15 deletions — well under the 500-line cap, so S1 to S5 landed
in ONE commit and no split was needed.

### be2bfc24f F042 R3 C4: add the reviewer's tests for the cockpit address and the switcher wiring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/cockpitAddress.test.ts | +61/-0 | NEW FILE, `git apply` of tests.diff, unedited |
| tests/ui_contracts/test_project_switcher_wiring.py | +61/-0 | NEW FILE, `git apply` of tests.diff, unedited |

### ea05e500e F042 R3 C5: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r3-mutations.py | +164/-0 | the G5 red-proof tool: 8 mutations (a1-a3, w1, h1-h4), vitest/pytest/harness runners, control first/last |

### (this commit) F042 R3 C6: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per the write-once rule (a handoff cannot table the commit that writes it) |

## External actions

`git push -u origin feature/f042-multi-project-cockpit` after C6: real outcome reported in the
worker's final reply, since this file cannot record a push that follows it.

No pull request created or merged this round: the block orders NOTHING IS MERGED (constraint 6);
`gh pr list` before and after this round's work read empty.

`git worktree add --detach .remedy-wt/f042-r3-mut ea05e500e` for G5 (clean checkout at C5), then
`os.symlink` of the primary's `apps/ui/node_modules` into the worktree's `apps/ui/node_modules`
(`target_is_directory=True`), then `python3 -B .agent/authored/f042-r3-mutations.py <worktree>`,
then `os.unlink` of that symlink, `git worktree remove --force .remedy-wt/f042-r3-mut` and `git
worktree prune` as G5's last action. `git worktree list | wc -l` read 66 at BEFORE ANYTHING ELSE
step 4 and 66 again after the removal and prune — unchanged.

## Verification

BEFORE ANYTHING ELSE — `.agent/STOP`: `ls` reported "No such file or directory" (absent). `pwd`
`/home/decodeux/Repos/remedy`. `git status --porcelain` empty. `git branch --show-current`
`feature/f042-multi-project-cockpit`. `git log --oneline -1` `fc744e0e0` — all matching. Block
bytes: measured 317 lines / sha256
`d3922fafd2311b3948e8b2ccaf16dc5858f174703e597b35ccb86278848795f4`, matching both readings given in
the delegation message exactly. `git worktree list | wc -l`: 66.

PAYLOADS — measured against the table, all eight matched exactly: `records.diff` 68 lines / 15078
bytes / `ad06cd990f407fc6f33c7315509cd782d4a13bee39bb1be05c6f8d0a1b078744`; `tests.diff` 134 lines /
5862 bytes / `53bf5b398814a6819f26277f1d96aefff6367158d63743c385bb3df39ef6d821`; `plan.md` 28 lines
/ 952 bytes / `68325b9727ea9db1c5d7d3658aea96a4e61c87b3f6afdc27ee333602b40256fa`; `render_index.html`
11 lines / 243 bytes / `224210b87c232ba002b0371bc54a6bb871dabaf13f23784ecd06573303d83363`;
`render_main.tsx` 61 lines / 3029 bytes /
`32178e171a74d09949494198421bc5a585d2a0dac8b887e8a7969100597ee7e9`; `render_vite.config.mjs` 28
lines / 744 bytes / `6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a`;
`render_drive.mjs` 176 lines / 8416 bytes /
`318bb9178f81094465d84384bb752011a196866e4f401f9d17bc71e3aec62681`; `render_measure.py` 187 lines
/ 6499 bytes / `263344b3e2e569a16118bb2330945ce0462b2beb8a4b18977080fc5f4edc7232`.

G1 TRANSPORT — every payload's measured lines/bytes/sha256 matched the table (above). Each
`.agent/authored/f042-r3-*` copy, read back with `git show <commit>:<path>`, is byte-identical to
its source (block copy against `.remedy-wt/f042-r3/block.md`, each other payload against
`.remedy-wt/f042-r3-payloads/<name>`): all nine comparisons matched exactly (Python `==` over the
raw bytes), sha256 equal on both sides in every row.

G2 THE RECORDS AND THE TESTS — every sha256 in the block's G2 table, read with `git show
<commit>:<path>` at the commit named, equal the reviewer's reading exactly: `.agent/decisions.md`
at C2 2483692 bytes / `be0127feff848dbc95fde2bd2a44939f0d82a7bf869b04f117aedf60737a2623`;
`.agent/live_review.md` at C2 312699 bytes /
`72c16195ab1033610fef80782503bdf20e0d444ddd425d59689a9159976f900e`; `.agent/plan.md` at C2 952
bytes / `68325b9727ea9db1c5d7d3658aea96a4e61c87b3f6afdc27ee333602b40256fa`;
`docs/ui/design_reference/assumption_log.md` at C2 29374 bytes /
`25fa266deedf7468356516ffc7cacccd9b22c0ab94b558fe6fa5bf1e40adec4e`;
`apps/ui/src/api/cockpitAddress.test.ts` at C4 2708 bytes /
`e6ecb94effd833120eeac570b22f506fc5e16fddbe4715137547c6b280b01329`;
`tests/ui_contracts/test_project_switcher_wiring.py` at C4 2562 bytes /
`84937461a784e2817d3ea0d6edd79280b5fe1773bf63dba5cf91fee91ba28eb3` — all six equal the block's
table exactly. `open_finding_ids` (from `scripts/rotate_live_review.py`) over `.agent/live_review.md`
at C2: `['R-1107']`, matching the reviewer's stated reading exactly. `git diff --name-only
f388d7605 c7efe533d` names exactly `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/ui/design_reference/assumption_log.md` — exactly the C2 paths of the table.

G3 THE CODE AND THE TESTS — `python3 -m ruff check tests/ui_contracts/test_project_switcher_wiring.py
.agent/authored/f042-r3-mutations.py .agent/authored/f042-r3-render_measure.py`: `All checks
passed!`, real exit 0. `apps/ui/node_modules/.bin/eslint src/RemedyApp.tsx src/api/cockpitAddress.ts
src/api/cockpitAddress.test.ts src/components/shell/ProjectProvider.tsx
src/components/shell/ProjectSwitcher.tsx src/components/rail/LeftBrandRail.tsx` run with `apps/ui`
as working directory: no output, real exit 0. `git show --numstat 01158bb9e`: 83/14 RemedyApp.tsx,
43/0 cockpitAddress.ts, 2/1 LeftBrandRail.tsx, 79/0 ProjectProvider.tsx, 31/0
ProjectSwitcher.module.css, 42/0 ProjectSwitcher.tsx (see C3 table above); the whole `RemedyApp.tsx`
and `LeftBrandRail.tsx` diffs at C3 are reported verbatim in the worker's final reply.

The serial pytest run at C5, in the primary checkout: `bash -c 'python3 -m pytest -q
-p no:cacheprovider -rs <the round's 11-target selection> 2>&1 | tail -10; echo
"REAL_EXIT=${PIPESTATUS[0]}"'` read `1757 passed, 5 skipped in 94.24s (0:01:34)`, `REAL_EXIT=0`.
This differs from the reviewer's `1754 passed, 8 skipped` by exactly the variance the block itself
predicts: this checkout's `node_modules` already carries the toolchain (unlike the reviewer's fresh
simulation worktree), so the vitest-node and `tests/ui_contracts/test_ui_lint.py:30` (x2)
toolchain-absent skips the reviewer saw did not fire here — those three ran and passed instead;
only the five named skips printed: `tests/ui_contracts/test_graph_architecture.py:441` and `:484`,
`tests/ui_contracts/test_ux_quality.py:507` and `:543` (all four D3 quarantine) and
`tests/test_agent_tooling.py:43` (D12), and the `-rs` summary printed exactly those five `SKIPPED`
lines. `test_typescript_compiles`
(`tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract`) and `test_vitest_passes`
(`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation`) both PASSED (re-run
together: `2 passed`, real exit 0); through the primary's own binaries, `tsc --noEmit` over
`apps/ui/src` read exit 0, and the whole vitest suite read `Test Files 95 passed | 1 skipped (96)`,
`Tests 1940 passed | 5 skipped (1945)` at exit 0 — matching the reviewer's `1940 passed | 5 skipped
over 96 files` reading exactly, and `src/api/cockpitAddress.test.ts` inside it read `9 tests`,
matching the reviewer's reading exactly.

Node count by `--collect-only -q`: `tests/ui_contracts/test_project_switcher_wiring.py` 5, matching
the reviewer's reading exactly. `python3 -m apps.cli.main integrity check --json`: all six checks
(`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`) `"status": "pass"`, `fail_count` 0, `"ok": true`, real
exit 0.

G4 THE RENDER — `python3 -B .agent/authored/f042-r3-render_measure.py /home/decodeux/Repos/remedy`
at C5, in the primary checkout: `vite build` succeeded (2117 modules, 2.21s), server and Chrome
started, `drive.mjs` ran all eight checks: R-a through R-h each printed `PASS` with its detail
object, final line `RENDER: 8 of 8 checks pass`, both Chrome and the server stopped by their
recorded pids (`SIGTERM`, both reported "stopped"), work dir removed, `drive.mjs exit code: 0`,
overall real exit 0 — matching the reviewer's own `8 of 8` reading exactly. The screenshot at
`/home/decodeux/Repos/remedy/.remedy-wt/f042-r3-render-switcher.png` (322367 bytes), read
immediately after this run and before G5 could overwrite it: it shows the cockpit's empty-project
face on the light cockpit background — a centred, labelled "PROJECT" native select reading "alpha"
above the centred sentence "This project has no jobs yet.", with no dashboard, spinner or rail
visible, matching the `?token=t&project=alpha&focus=n1&level=2` address R-a opens.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f042-r3-mut ea05e500e` (clean checkout at
C5), the `apps/ui/node_modules` symlink added, then `python3 -B .agent/authored/f042-r3-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f042-r3-mut`. Whole output (reported again verbatim in the
worker's final reply): control (first) vitest exit=0 failed=0, pytest exit=0 failed=0, harness
exit=0 `RENDER: 8 of 8 checks pass`; a1 exit=1 failed=1 restored byte-identical: True; a2 exit=1
failed=1 restored byte-identical: True; a3 exit=1 failed=1 restored byte-identical: True; w1 exit=1
failed=1 restored byte-identical: True; h1 exit=1 `RENDER: 5 of 8 checks pass` restored
byte-identical: True; h2 exit=1 `RENDER: 6 of 8 checks pass` restored byte-identical: True; h3
exit=1 "no RENDER line" restored byte-identical: True (the mutated Back step leaves the harness
page, exactly as the block predicts for h3 — an exit 1 all the same, caught); h4 exit=1 `RENDER: 7
of 8 checks pass` restored byte-identical: True; control (last) vitest exit=0 failed=0, pytest
exit=0 failed=0, harness exit=0 `RENDER: 8 of 8 checks pass`; final line `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: True`. Every one of the eight mutations exited non-zero — none stayed green.
Symlink removed with `os.unlink`, `git worktree remove --force .remedy-wt/f042-r3-mut` then `git
worktree prune`, both real exit 0; `git worktree list | wc -l` read 66 afterward, matching the step
4 reading.

## Authored-text proofs

Every `.agent/authored/f042-r3-*` copy (block, plan.md, records.diff, tests.diff, the five
render_* files) is byte-identical, read back from the commit that added it (`git show
<commit>:<path>`), to its source under `.remedy-wt/f042-r3-payloads/` or `.remedy-wt/f042-r3/block.md`
— see G1 above, all nine comparisons matched by direct byte comparison and equal sha256 on both
sides. `records.diff` and `tests.diff` were each applied unedited with `git apply` (real exit 0 on
both `--check` and the real apply, reported per-file above); the resulting file hashes at their
commits matched the reviewer's G2 table exactly (see G2). `.agent/plan.md` was rewritten from its
payload with `shutil.copyfile`, then verified byte-identical at C2 against the table's hash (see
G2).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C2 | done | |
| C3 | done | S1-S5 written against the reviewer's tests and the render harness; G3/G4/G5 below prove them |
| C4 | done | tests.diff applied unedited, 5 pytest + 9 vitest tests passed against unedited code |
| C5 | done | mutation tool written and used by G5 before this commit closes |
| C6 | done | this handback |
| G1 | done | all 9 authored copies byte-identical to source |
| G2 | done | all 6 hashes, the open-id set and the C1c..C2 diff all matched |
| G3 | done | ruff clean, eslint clean, 1757 passed / 5 skipped at exit 0 (variance from the reviewer's count explained and expected), the pytest node count and the vitest counts matched, integrity clean |
| G4 | done | render harness read 8 of 8 checks pass at exit 0, screenshot read and described |
| G5 | done | all 8 mutations caught, all 8 restores byte-identical, both controls green |

## Deviations & assumptions

None from the block's ordered commit sequence: C1a, C1b, C1c, C2, C3, C4, C5, C6 executed in that
exact order, no commit was split, reordered or added, and every commit stayed well under the
500-line cap (largest: C3 at 280 insertions).

C3's own file sizes: `apps/ui/src/components/rail/LeftBrandRail.tsx` (+2/-1) matched the reviewer's
own reading exactly. The other five files of S1-S5 were written independently against their
clauses and the reviewer's tests/harness: `apps/ui/src/RemedyApp.tsx` (+83/-14, reviewer 64/13),
`apps/ui/src/api/cockpitAddress.ts` (+43/-0, reviewer 45/0),
`apps/ui/src/components/shell/ProjectProvider.tsx` (+79/-0, reviewer 66/0),
`apps/ui/src/components/shell/ProjectSwitcher.module.css` (+31/-0, reviewer 30/0),
`apps/ui/src/components/shell/ProjectSwitcher.tsx` (+42/-0, reviewer 44/0) — an independent
composition of the same spec clauses, informational only per the block's own reading of C3's line
("the reviewer's own version ... read ..."). No functional behaviour changed as a result of this
independent authoring: G3 (lint/tsc/vitest/pytest), G4 (the render harness) and G5 (all eight
mutations turning red and every control green) all passed against this code as written, on the
first attempt, with no repair round needed.

No payload was retyped or edited; both `.diff` files were applied with `git apply` verbatim,
`--check` exit 0 before every real apply. No test was edited to pass and no gate result was papered
over.

One explained (not block-violating) variance, flagged in G3 above: the round's own pytest selection
read `1757 passed, 5 skipped` where the reviewer's simulation read `1754 passed, 8 skipped`. The
block itself states this may happen and names the exact mechanism — a fresh simulation worktree
lacks the installed toolchain, this checkout has it — which is exactly what the three missing
`SKIPPED` lines (the vitest node and the two toolchain-absent `test_ui_lint.py:30` skips) show. Not
treated as a red gate.

Assumption: DECISION F042 D3's "the round's whole tracked path set" (constraint 3) is read as fixed
by the block's own enumeration, and no path outside it was touched; `git diff --name-only fc744e0e0`
at the branch tip after C6 names exactly the `.agent/authored/f042-r3-*` copies and tool, the two
paths `records.diff`/`tests.diff` edit, `.agent/plan.md`, the six S1-S5 files, `.agent/handoff.md` —
reported in full in the worker's final reply.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of this round (F042 round 3).
3. T003: the home grid, the cards, the empty-state invite, deep links across projects and the
   end-to-end run.

Open findings: 1. Operator questions open: 1.
